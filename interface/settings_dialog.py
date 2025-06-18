# interface/settings_dialog.py
"""
Dialogue des paramètres avec gestion robuste des erreurs et mise à jour dynamique.
Ce module gère la configuration de l'application, y compris la sélection de la caméra,
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSlider,
    QRadioButton, QPushButton, QGroupBox, QMessageBox, QCheckBox, QWidget
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from typing import Any, Optional

class SettingsDialog(QDialog):
    """
    Dialogue des paramètres avec gestion robuste des erreurs et mise à jour dynamique.

    Attributes:
        config (Any): Gestionnaire de configuration
        logger (Any): Logger pour journalisation
        parent (Optional[QWidget]): Widget parent
    """

    def __init__(self, config: Any, logger: Any, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.config = config
        self.logger = logger
        self._init_ui()
        self.logger.info("SettingsDialog initialisé")

    def _init_ui(self) -> None:
        """Initialise l'interface avec gestion des erreurs."""
        try:
            self.setWindowTitle("Paramètres")
            self.setWindowIcon(QIcon("assets/settings.png"))
            self.setFixedSize(450, 600)  # Taille légèrement augmentée

            main_layout = QVBoxLayout(self)

            # Section Caméra
            self._setup_camera_section(main_layout)

            # Section Main Dominante
            self._setup_handedness_section(main_layout)

            # Section Sensibilité
            self._setup_sensitivity_section(main_layout)

            # Section Affichage
            self._setup_display_section(main_layout)

            # Boutons d'action
            self._setup_action_buttons(main_layout)

        except Exception as e:
            self.logger.error(f"Erreur initialisation UI: {str(e)}")
            raise RuntimeError(f"Erreur initialisation des paramètres: {str(e)}")

    def _setup_camera_section(self, layout: QVBoxLayout) -> None:
        """Configure la section de sélection de caméra."""
        camera_group = QGroupBox("Configuration Caméra")
        camera_layout = QVBoxLayout()

        self.camera_combo = QComboBox()
        cameras = self.config.get_available_cameras()
        
        if not cameras:
            self.logger.warning("Aucune caméra détectée")
            self.camera_combo.addItem("Aucune caméra détectée", -1)
        else:
            for index in cameras:
                self.camera_combo.addItem(f"Caméra {index}", index)

        current_cam = int(self.config.get_setting("DEFAULT", "camera_index", 0))
        idx = self.camera_combo.findData(current_cam)
        self.camera_combo.setCurrentIndex(idx if idx >= 0 else 0)

        camera_layout.addWidget(QLabel("Caméra disponible:"))
        camera_layout.addWidget(self.camera_combo)

        # Checkbox pour l'affichage des landmarks
        self.landmarks_check = QCheckBox("Afficher les points de repère (landmarks)")
        show_landmarks = self.config.get_setting("DEFAULT", "show_landmarks", "True").lower() == "true"
        self.landmarks_check.setChecked(show_landmarks)
        camera_layout.addWidget(self.landmarks_check)

        camera_group.setLayout(camera_layout)
        layout.addWidget(camera_group)

    def _setup_handedness_section(self, layout: QVBoxLayout) -> None:
        """Configure la section de sélection de main dominante."""
        hand_group = QGroupBox("Configuration Main")
        hand_layout = QHBoxLayout()

        self.right_hand = QRadioButton("Droite")
        self.left_hand = QRadioButton("Gauche")
        
        dominant_hand = self.config.get_setting("DEFAULT", "dominant_hand", "Droite")
        self.right_hand.setChecked(dominant_hand == "Droite")
        self.left_hand.setChecked(dominant_hand == "Gauche")

        hand_layout.addWidget(self.right_hand)
        hand_layout.addWidget(self.left_hand)
        hand_group.setLayout(hand_layout)
        layout.addWidget(hand_group)

    def _setup_sensitivity_section(self, layout: QVBoxLayout) -> None:
        """Configure les contrôles de sensibilité."""
        sensitivity_group = QGroupBox("Paramètres de Sensibilité")
        sensitivity_layout = QVBoxLayout()

        # Sensibilité générale
        self.sensitivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.sensitivity_slider.setRange(1, 100)
        self.sensitivity_slider.setValue(
            int(self.config.get_setting("DEFAULT", "sensitivity", 50))
        )
        self.sensitivity_label = QLabel(f"Sensibilité: {self.sensitivity_slider.value()}%")
        self.sensitivity_slider.valueChanged.connect(
            lambda v: self.sensitivity_label.setText(f"Sensibilité: {v}%")
        )

        # Seuil de détection
        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setRange(1, 100)
        self.threshold_slider.setValue(
            int(self.config.get_setting("DEFAULT", "threshold", 50))
        )
        self.threshold_label = QLabel(f"Seuil de détection: {self.threshold_slider.value()}%")
        self.threshold_slider.valueChanged.connect(
            lambda v: self.threshold_label.setText(f"Seuil de détection: {v}%")
        )

        sensitivity_layout.addWidget(self.sensitivity_label)
        sensitivity_layout.addWidget(self.sensitivity_slider)
        sensitivity_layout.addSpacing(15)
        sensitivity_layout.addWidget(self.threshold_label)
        sensitivity_layout.addWidget(self.threshold_slider)
        sensitivity_group.setLayout(sensitivity_layout)
        layout.addWidget(sensitivity_group)

    def _setup_display_section(self, layout: QVBoxLayout) -> None:
        """Configure les options d'affichage."""
        display_group = QGroupBox("Options d'Affichage")
        display_layout = QVBoxLayout()

        self.fps_check = QCheckBox("Afficher le FPS")
        show_fps = self.config.get_setting("DISPLAY", "show_fps", "False").lower() == "true"
        self.fps_check.setChecked(show_fps)

        display_layout.addWidget(self.fps_check)
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)

    def _setup_action_buttons(self, layout: QVBoxLayout) -> None:
        """Configure les boutons d'actions."""
        button_layout = QHBoxLayout()

        self.apply_btn = QPushButton(QIcon("assets/apply.png"), "Appliquer")
        self.apply_btn.clicked.connect(self._apply_settings)
        
        cancel_btn = QPushButton(QIcon("assets/cancel.png"), "Annuler")
        cancel_btn.clicked.connect(self.reject)
        
        reset_btn = QPushButton(QIcon("assets/reset.png"), "Par Défaut")
        reset_btn.clicked.connect(self._reset_to_default)

        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(reset_btn)
        layout.addLayout(button_layout)

    def _apply_settings(self) -> None:
        """Applique les paramètres modifiés."""
        try:
            # Validation de la caméra
            cam_index = self.camera_combo.currentData()
            if cam_index is None or cam_index == -1:
                raise ValueError("Aucune caméra valide sélectionnée")

            # Enregistrement des paramètres
            settings = {
                "camera_index": str(cam_index),
                "dominant_hand": "Droite" if self.right_hand.isChecked() else "Gauche",
                "sensitivity": str(self.sensitivity_slider.value()),
                "threshold": str(self.threshold_slider.value()),
                "show_landmarks": str(self.landmarks_check.isChecked()),
                "show_fps": str(self.fps_check.isChecked())
            }

            # Arrêter proprement le thread vidéo
            if hasattr(self.parent(), 'video_thread'):
                self.parent()._stop_detection() # type: ignore
            
            # Appliquer les nouveaux paramètres
            for key, value in settings.items():
                self.config.set_setting("DEFAULT" if key != "show_fps" else "DISPLAY", key, value)

            # 4. Redémarrer avec les nouveaux paramètres
            if hasattr(self.parent(), 'video_thread'):
                self.parent()._start_detection() # type: ignore
                
        except Exception as e:
            self.logger.error(f"Erreur application paramètres: {e}")
            QMessageBox.critical(self, "Erreur", f"Impossible d'appliquer : {e}")

    def _reset_to_default(self):
        try:
            # 1. Confirmation utilisateur
            if QMessageBox.Yes != QMessageBox.question(
                self, "Confirmation", 
                "Cela réinitialisera tous les paramètres et redémarrera le flux. Continuer?",
                QMessageBox.Yes | QMessageBox.No
            ):
                return

            # 2. Sauvegarde de l'état actuel
            was_running = hasattr(self.parent(), 'video_thread') and self.parent().video_thread.isRunning() # type: ignore
            
            # 3. Arrêt propre
            if was_running:
                self.parent()._stop_detection() # type: ignore

            # 4. Réinitialisation
            self.config.reset_to_default()
            self._update_ui_from_config()  # Méthode à créer pour mettre à jour l'UI

            # 5. Redémarrage
            if was_running:
                self.parent()._start_detection() # type: ignore

            QMessageBox.information(self, "Succès", "Paramètres réinitialisés avec succès")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de la réinitialisation : {e}")
            self.logger.error(f"Reset failed: {str(e)}")
    
    def _update_ui_from_config(self) -> None:
        """
        Met à jour l'interface utilisateur avec les valeurs actuelles de la configuration.
        Gère tous les widgets du dialogue de paramètres.
        """
        try:
            # 1. Mise à jour de la caméra
            current_cam = int(self.config.get_setting("DEFAULT", "camera_index", 0))
            cam_index = self.camera_combo.findData(current_cam)
            if cam_index >= 0:
                self.camera_combo.setCurrentIndex(cam_index)
            else:
                self.logger.warning(f"Caméra configurée {current_cam} non trouvée dans la liste")

            # 2. Mise à jour de la main dominante
            dominant_hand = self.config.get_setting("DEFAULT", "dominant_hand", "Droite")
            self.right_hand.setChecked(dominant_hand == "Droite")
            self.left_hand.setChecked(dominant_hand == "Gauche")

            # 3. Mise à jour des sliders
            sensitivity = int(self.config.get_setting("DEFAULT", "sensitivity", 50))
            self.sensitivity_slider.setValue(sensitivity)
            self.sensitivity_label.setText(f"Sensibilité: {sensitivity}%")

            threshold = int(self.config.get_setting("DEFAULT", "threshold", 50))
            self.threshold_slider.setValue(threshold)
            self.threshold_label.setText(f"Seuil de détection: {threshold}%")

            # 4. Mise à jour des checkboxes
            show_landmarks = self.config.get_setting("DEFAULT", "show_landmarks", "True").lower() == "true"
            self.landmarks_check.setChecked(show_landmarks)

            show_fps = self.config.get_setting("DISPLAY", "show_fps", "False").lower() == "true"
            self.fps_check.setChecked(show_fps)

            self.logger.debug("UI mise à jour depuis la configuration")

        except Exception as e:
            self.logger.error(f"Erreur mise à jour UI depuis config: {str(e)}")
            # Réinitialisation d'urgence des valeurs par défaut
            self.camera_combo.setCurrentIndex(0)
            self.right_hand.setChecked(True)
            self.sensitivity_slider.setValue(50)
            self.threshold_slider.setValue(50)
            self.landmarks_check.setChecked(True)
            self.fps_check.setChecked(False)
            raise RuntimeError(f"Erreur critique dans _update_ui_from_config: {str(e)}")