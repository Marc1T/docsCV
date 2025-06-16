# interface/main_window.py
"""
Point d'entrée de GestureMouseApp.
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTextEdit, QTabWidget, QToolBar, QAction, QStatusBar,
    QMessageBox, QCheckBox, QApplication
)
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import Qt, QSize
from typing import Any, Optional
import os
from chatbot.faq_bot import FAQBot
from interface.video_thread import VideoThread

class MainWindow(QMainWindow):
    def __init__(self, config: Any, logger: Any, faq_bot: FAQBot, video_thread: Optional[VideoThread] = None) -> None:
        super().__init__()
        self.config = config
        self.logger = logger
        self.faq_bot = faq_bot
        self.video_thread = video_thread or VideoThread(config, logger)
        self.video_label = None
        self.camera_combo : Optional[QComboBox] = None
        self.faq_input = None
        self.faq_output = None
        self.landmarks_checkbox = None
        self._init_ui()
        self.logger.info("MainWindow initialisée")
        self.setStyleSheet(self.config.get_setting("UI", "stylesheet", ""))

    def _init_ui(self) -> None:
        try:
            self.setWindowTitle("GestureMouseApp")
            self.setWindowIcon(QIcon("assets/logo.png"))
            self.resize(700, 500)

            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QVBoxLayout(central_widget)
            
            self.tab_widget = QTabWidget()
            main_layout.addWidget(self.tab_widget)
            
            self._setup_video_tab()
            self._setup_faq_tab()
            self._setup_toolbar()
            self._setup_status_bar()

        except Exception as e:
            self.logger.error(f"Erreur initialisation UI : {e}")
            raise

    def _setup_toolbar(self) -> None:
        toolbar = QToolBar("Barre d'outils")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        actions = [
            ("Démarrer", "play.png", "Ctrl+D", self._start_detection),
            ("Arrêter", "stop.png", "Ctrl+S", self._stop_detection),
            ("Paramètres", "settings.png", "", self._open_settings),
            ("Aide", "help.png", "", self._open_faq),
            ("À propos", "info.png", "", self._open_about),
            ("Quitter", "exit.png", "Ctrl+Q", self.close)
        ]
        
        for text, icon, shortcut, callback in actions:
            action = QAction(QIcon(f"assets/{icon}"), text, self)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(callback)
            toolbar.addAction(action)
            if text == "Démarrer":
                self.action_start = action
            elif text == "Arrêter":
                self.action_stop = action
                self.action_stop.setEnabled(False)
        
        toolbar.addSeparator()
        
        self.landmarks_checkbox = QCheckBox("Afficher landmarks")
        show_landmarks = self.config.get_setting("DEFAULT", "show_landmarks", "True").lower() == "true"
        self.landmarks_checkbox.setChecked(show_landmarks)
        self.landmarks_checkbox.stateChanged.connect(self._toggle_landmarks)
        toolbar.addWidget(self.landmarks_checkbox)

    def _setup_video_tab(self) -> None:
        video_tab = QWidget()
        video_layout = QVBoxLayout(video_tab)
        
        video_controls = QHBoxLayout()
        self.camera_combo = QComboBox()
        self._update_camera_list()
        self.camera_combo.currentIndexChanged.connect(self._change_camera)
        
        video_controls.addWidget(QLabel("Caméra :"))
        video_controls.addWidget(self.camera_combo)
        video_controls.addStretch()
        video_layout.addLayout(video_controls)
        
        self.video_label = QLabel("Aucun flux vidéo")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setStyleSheet("border: 1px solid #CCCCCC;")
        video_layout.addWidget(self.video_label)
        
        self.tab_widget.addTab(video_tab, "Vidéo")

    def _setup_faq_tab(self) -> None:
        faq_tab = QWidget()
        faq_layout = QVBoxLayout(faq_tab)
        
        self.faq_input = QTextEdit()
        self.faq_input.setPlaceholderText("Posez votre question ici...")
        self.faq_input.setFixedHeight(100)
        
        faq_button = QPushButton("Envoyer")
        faq_button.clicked.connect(self._send_faq_question)
        
        self.faq_output = QTextEdit()
        self.faq_output.setReadOnly(True)
        self.faq_output.setPlaceholderText("Réponses du chatbot FAQ...")
        
        faq_layout.addWidget(QLabel("Question :"))
        faq_layout.addWidget(self.faq_input)
        faq_layout.addWidget(faq_button)
        faq_layout.addWidget(QLabel("Réponse :"))
        faq_layout.addWidget(self.faq_output)
        
        self.tab_widget.addTab(faq_tab, "FAQ")

    def _setup_status_bar(self) -> None:
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self.gesture_label = QLabel("Geste: Aucun")
        self.action_label = QLabel("Action: Aucune")
        
        self.statusBar.addPermanentWidget(self.gesture_label)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(self.action_label)
        
        self.statusBar.showMessage("Prêt", 3000)

    def _toggle_landmarks(self, state: int) -> None:
        show = state == Qt.CheckState.Checked
        self.config.set_setting("DEFAULT", "show_landmarks", str(show))
        if self.video_thread and hasattr(self.video_thread.detector, 'show_landmarks'):
            self.video_thread.detector.show_landmarks = show
        self.logger.info(f"Landmarks {'activés' if show else 'désactivés'}")

    def update_video_frame(self, q_image: QImage, gesture: str, action: str) -> None:
        try:
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap.scaled( # type: ignore
                self.video_label.size(),               # type: ignore
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
            self.gesture_label.setText(f"Geste: {gesture}")
            self.action_label.setText(f"Action: {action}")
        except Exception as e:
            self.logger.error(f"Erreur mise à jour vidéo : {e}")

    def _update_camera_list(self) -> None:
        cameras = self.config.get_available_cameras()
        self.camera_combo.clear() # type: ignore
        for index in cameras:
            self.camera_combo.addItem(f"Caméra {index}", index) # type: ignore
        current_index = int(self.config.get_setting("DEFAULT", "camera_index", 0))
        idx = self.camera_combo.findData(int(current_index)) # type: ignore
        if idx >= 0:
            self.camera_combo.setCurrentIndex(idx) # type: ignore

    def _start_detection(self) -> None:
        if self.video_thread and not self.video_thread.isRunning():
            self.video_thread.frame_signal.connect(self.update_video_frame)
            self.video_thread.start()
            self.action_start.setEnabled(False)
            self.action_stop.setEnabled(True)
            self.statusBar.showMessage("Détection démarrée", 3000) # type: ignore
            self.logger.info("Détection démarrée")

    def _stop_detection(self) -> None:
        if self.video_thread and self.video_thread.isRunning():
            try:
                self.video_thread.frame_signal.disconnect(self.update_video_frame)  # Déconnexion avant arrêt
                self.video_thread.stop()
                while self.video_thread.isRunning():  # Attente active sécurisée
                    QApplication.processEvents()
                self.video_label.clear() # type: ignore
                self.video_label.setText("Flux vidéo arrêté") # type: ignore
            except Exception as e:
                self.logger.error(f"Erreur lors de l'arrêt du thread vidéo : {e}")

        self.statusBar.showMessage("Détection arrêtée", 3000) # type: ignore
        self.action_start.setEnabled(True)
        self.action_stop.setEnabled(False)
        self.logger.info("Détection arrêtée")

    def _change_camera(self, index: int) -> None:
        if index >= 0 and self.video_thread:
            camera_index = self.camera_combo.itemData(index)    # type: ignore
            self.video_thread.update_camera(camera_index)
            self.config.set_setting("DEFAULT", "camera_index", camera_index)
            self.logger.info(f"Caméra changée : {camera_index}")

    def _send_faq_question(self) -> None:
        question = self.faq_input.toPlainText().strip() # type: ignore
        if question:
            response = self.faq_bot.get_response(question)
            self.faq_output.setText(response or "Aucune réponse trouvée.") # type: ignore
            self.logger.info(f"FAQ - Question: {question}")

    def _open_settings(self) -> None:
        from interface.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.config, self.logger, self)
        if dialog.exec_():
            self._update_camera_list()
            self.logger.info("Paramètres mis à jour")
            
    def _open_faq(self) -> None:
        self.tab_widget.setCurrentIndex(1)

    def _open_about(self) -> None:
        from interface.about_dialog import AboutDialog
        AboutDialog(self).exec_()

    def closeEvent(self, a0) -> None:
        self._stop_detection()
        self.logger.info("Application fermée")
        a0.accept() # type: ignore