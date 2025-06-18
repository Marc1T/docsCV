# interface/about_dialog.py
"""
Dialogue À propos pour GestureMouseApp.
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class AboutDialog(QDialog):
    """
    Dialogue affichant les informations sur l'application.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialise l'interface du dialogue."""
        self.setWindowTitle("À propos de GestureMouseApp")
        self.setWindowIcon(QIcon("assets/info.png"))
        self.setFixedSize(300, 200)

        layout = QVBoxLayout(self)

        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        info_label = QLabel(
            "GestureMouseApp v1.0\n"
            "Contrôlez votre souris avec des gestes !\n"
            "Développé par NANKOULI Marc Thierry et\n"
            "equipe de Touchless\n"
            "© 2025"
        )
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)