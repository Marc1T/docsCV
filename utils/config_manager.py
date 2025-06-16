# utils/config_manager.py
import configparser
import json
import os
from typing import Any, Dict, Optional, Tuple, List
import cv2

class ConfigError(Exception):
    """Exception personnalisée pour les erreurs de configuration."""
    pass

class ConfigManager:
    """
    Gère la lecture/écriture des fichiers de configuration.

    Attributes:
        config (configparser.ConfigParser): Parser pour settings.ini.
        gestures (Dict[str, str]): Mappings geste-action depuis gestures.json.
        faq_data (List[Dict[str, str]]): Données FAQ depuis faq.json.
        settings_file (str): Chemin vers settings.ini.
        gestures_file (str): Chemin vers gestures.json.
        faq_file (str): Chemin vers faq.json.
        param_rules (Dict[str, Tuple[type, Any, Any]]): Règles de validation (type, min, max).
    """

    def __init__(
        self,
        settings_file: str = "config/settings.ini",
        gestures_file: str = "config/gestures.json",
        faq_file: str = "config/faq.json"
    ) -> None:
        self.config = configparser.ConfigParser()
        self.gestures: Dict[str, str] = {}
        self.faq_data: List[Dict[str, str]] = []
        self.settings_file = settings_file
        self.gestures_file = gestures_file
        self.faq_file = faq_file
        self.param_rules = {
            "sensitivity": (int, 0, 100),
            "threshold": (int, 0, 100),
            "gesture_ratio_threshold": (float, 0.1, 1.0),
            "pinch_dist_threshold": (float, 0.01, 0.1),
            "vgest_ratio_threshold": (float, 1.0, 2.5),
            "dz_threshold": (float, 0.05, 0.5),
            "min_frames_confirm": (int, 1, 10),
            "brightness_step": (float, 0.01, 0.1),
            "volume_step": (float, 0.01, 0.1),
            "scroll_amount": (int, 50, 500),
            "cursor_min_dist": (int, 10, 100),
            "cursor_max_dist": (int, 500, 2000),
            "cursor_min_ratio": (float, 0.01, 0.5),
            "cursor_max_ratio": (float, 1.0, 5.0),
            "pinch_threshold": (float, 0.1, 1.0),
            "pinch_frames": (int, 1, 10),
            "frame_delay_ms": (int, 10, 100),
            "gesture_window_size": (int, 3, 10),
            "frame_skip": (int, 1, 5),
            "reconnect_attempts": (int, 1, 5),
            "debounce_ms": (int, 50, 1000),
            "cursor_dead_zone": (float, 0.0, 50.0),
            "status_bar_timeout": (int, 1000, 10000),
            "similarity_threshold": (float, 0.1, 1.0),
        }
        self._load_config()
        self._load_gestures()
        self._load_faq()

    def _load_config(self) -> None:
        """Charge settings.ini, crée le fichier s'il n'existe pas."""
        try:
            if not os.path.exists(os.path.dirname(self.settings_file)):
                os.makedirs(os.path.dirname(self.settings_file))
            if not os.path.exists(self.settings_file):
                self._create_default_config()
            self.config.read(self.settings_file, encoding="utf-8")
        except Exception as e:
            raise ConfigError(f"Erreur chargement {self.settings_file} : {e}")

    def _create_default_config(self) -> None:
        """Crée un settings.ini par défaut."""
        self.config["DEFAULT"] = {
            "camera_index": "0",
            "detection_mode": "Main",
            "dominant_hand": "Droite",
            "sensitivity": "50",
            "threshold": "50",
            "show_landmarks": "True",
            "gesture_ratio_threshold": "0.5",
            "pinch_dist_threshold": "0.05",
            "vgest_ratio_threshold": "1.7",
            "dz_threshold": "0.1",
            "min_frames_confirm": "5",
            "brightness_step": "0.02",
            "volume_step": "0.02",
            "scroll_amount": "120",
            "cursor_min_dist": "25",
            "cursor_max_dist": "900",
            "cursor_min_ratio": "0.07",
            "cursor_max_ratio": "2.1",
            "pinch_threshold": "0.3",
            "pinch_frames": "5",
            "frame_delay_ms": "30",
            "app_version": "1.0",
            "gesture_window_size": "5",
            "frame_skip": "1",
            "reconnect_attempts": "3",
            "debounce_ms": "200",
            "cursor_dead_zone": "10.0",
            "status_bar_timeout": "5000",
        }
        self.config["UI"] = {
            "stylesheet": """
                QMainWindow { background-color: #FFFFFF; }
                QDialog { background-color: #FFFFFF; color: #333333; font-family: Arial; }
                QLabel { color: #333333; font-size: 14px; }
                QComboBox, QCheckBox, QRadioButton, QTextEdit, QLineEdit {
                    color: #333333; background-color: #F5F5F5; border: 1px solid #CCCCCC; padding: 5px;
                }
                QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 20px; }
                QPushButton {
                    background-color: #4CAF50; color: white; border: none;
                    padding: 8px 16px; border-radius: 4px; font-size: 14px;
                }
                QPushButton:hover { background-color: #45A049; }
                QTextEdit, QLineEdit { border-radius: 4px; }
                QToolBar { background-color: #F0F0F0; border: none; }
                QStatusBar { background-color: #F0F0F0; color: #333333; }
                QTabWidget::pane { border: 1px solid #CCCCCC; }
                QTabBar::tab { background-color: #E0E0E0; color: #333333; padding: 8px 16px; }
                QTabBar::tab:selected { background-color: #FFFFFF; border-bottom: 2px solid #4CAF50; }
            """
        }
        self.config["FAQ"] = {
            "similarity_threshold": "0.5"
        }
        self.config["LOGGING"] = {
            "log_level": "INFO",
            "log_file": "logs/app.log",
            "log_to_file": "True",
            "log_format": "%%(asctime)s [%%(levelname)s] %%(message)s"
        }
        with open(self.settings_file, "w", encoding="utf-8") as f:
            self.config.write(f)

    def _load_gestures(self) -> None:
        """Charge gestures.json, crée le fichier s'il n'existe pas."""
        try:
            if not os.path.exists(os.path.dirname(self.gestures_file)):
                os.makedirs(os.path.dirname(self.gestures_file))
            if not os.path.exists(self.gestures_file):
                self._create_default_gestures()
            with open(self.gestures_file, "r", encoding="utf-8") as f:
                self.gestures = json.load(f)
        except Exception as e:
            raise ConfigError(f"Erreur chargement {self.gestures_file} : {e}")

    def _create_default_gestures(self) -> None:
        """Crée un gestures.json par défaut."""
        default_gestures = {
            "V_GEST": "move_cursor",
            "FIST": "mouse_down",
            "MID": "click",
            "INDEX": "click_right",
            "TWO_FINGER_CLOSED": "double_click",
            "PINCH_MINOR": "scroll",
            "PINCH_MAJOR": "change_volume"
        }
        with open(self.gestures_file, "w", encoding="utf-8") as f:
            json.dump(default_gestures, f, indent=4)

    def _load_faq(self) -> None:
        """Charge faq.json, crée le fichier s'il n'existe pas."""
        try:
            if not os.path.exists(os.path.dirname(self.faq_file)):
                os.makedirs(os.path.dirname(self.faq_file))
            if not os.path.exists(self.faq_file):
                self._create_default_faq()
            with open(self.faq_file, "r", encoding="utf-8") as f:
                self.faq_data = json.load(f)
        except Exception as e:
            raise ConfigError(f"Erreur chargement {self.faq_file} : {e}")

    def _create_default_faq(self) -> None:
        """Crée un faq.json par défaut."""
        default_faq = [
            {
                "question": "Comment démarrer la détection des gestes ?",
                "answer": "Cliquez sur le bouton 'Démarrer' dans la fenêtre principale ou utilisez le raccourci clavier Ctrl+D. Assurez-vous que votre caméra est connectée."
            },
            {
                "question": "Quels gestes sont pris en charge ?",
                "answer": "Les gestes incluent V_GEST (déplacer le curseur), FIST (clic maintenu), MID (clic gauche), INDEX (clic droit), TWO_FINGER_CLOSED (double clic), PINCH_MINOR (défilement), PINCH_MAJOR (changer le volume)."
            },
            {
                "question": "Comment changer la main dominante ?",
                "answer": "Allez dans Paramètres > Général, sélectionnez 'Droite' ou 'Gauche' pour la main dominante, puis cliquez sur 'Appliquer'."
            },
            {
                "question": "Pourquoi la détection ne fonctionne pas ?",
                "answer": "Vérifiez que votre caméra est connectée et sélectionnée dans Paramètres > Caméra. Assurez-vous que l'éclairage est suffisant et que vos mains sont visibles."
            },
            {
                "question": "Comment ajuster la vitesse ?",
                "answer": "Dans Paramètres > Détection, ajustez le curseur 'Vitesse' ou modifiez les paramètres correspondants dans config/settings.py."
            }
        ]
        with open(self.faq_file, "w", encoding="utf-8") as f:
            json.dump(default_faq, f, indent=4, ensure_ascii=False)

    def validate_param(self, key: str, value: Any) -> Any:
        """Valide un paramètre selon ses règles (type, min, max)."""
        if key not in self.param_rules:
            return value
        param_type, min_val, max_val = self.param_rules[key]
        try:
            if param_type is int:
                val = int(float(value))
            elif param_type is float:
                val = float(value)
            else:
                val = value
            if min_val is not None and val < min_val:
                raise ValueError(f"{key} ({val}) < min ({min_val})")
            if max_val is not None and val > max_val:
                raise ValueError(f"{key} ({val}) > max ({max_val})")
            return val
        except (ValueError, TypeError) as e:
            raise ConfigError(f"Paramètre invalide {key} : {e}")

    def get_setting(self, section: str, key: str, default: Any = None) -> Any:
        """Récupère un paramètre avec validation."""
        try:
            if section not in self.config:
                return default
            if key not in self.config[section]:
                return default
            value = self.config[section][key]
            return self.validate_param(key, value)
        except Exception as e:
            raise ConfigError(f"Erreur lecture {section}.{key} : {e}")

    def set_setting(self, section: str, key: str, value: Any) -> None:
        """Définit un paramètre avec validation et sauvegarde."""
        try:
            validated_value = self.validate_param(key, value)
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = str(validated_value)
            with open(self.settings_file, "w", encoding="utf-8") as f:
                self.config.write(f)
        except Exception as e:
            raise ConfigError(f"Erreur écriture {section}.{key} : {e}")

    def get_gesture_action(self, gesture: str) -> Optional[str]:
        """Récupère l’action associée à un geste."""
        return self.gestures.get(gesture)

    def set_gesture_action(self, gesture: str, action: str) -> None:
        """Définit une action pour un geste et sauvegarde."""
        try:
            self.gestures[gesture] = action
            with open(self.gestures_file, "w", encoding="utf-8") as f:
                json.dump(self.gestures, f, indent=4)
        except Exception as e:
            raise ConfigError(f"Erreur écriture geste {gesture} : {e}")

    def get_faq_data(self) -> List[Dict[str, str]]:
        """Retourne les données FAQ."""
        return self.faq_data

    def get_available_cameras(self) -> List[int]:
        """Liste les indices des caméras disponibles."""
        cameras = []
        index = 0
        while index < 5:  # Tester jusqu'à 5 caméras max
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                cameras.append(index)
                cap.release()
            else:
                cap.release()
            index += 1
        return cameras

    def reset_to_default(self) -> None:
        """Réinitialise les fichiers de configuration aux valeurs par défaut."""
        try:
            if os.path.exists(self.settings_file):
                os.remove(self.settings_file)
            # if os.path.exists(self.gestures_file):
            #     os.remove(self.gestures_file)
            # if os.path.exists(self.faq_file):
            #     os.remove(self.faq_file)
            self._create_default_config()
            # self._create_default_gestures()
            # self._create_default_faq()
            self._load_config()
            # self._load_gestures()
            # self._load_faq()
        except Exception as e:
            raise ConfigError(f"Erreur réinitialisation configurations : {e}")

    def reload(self) -> None:
        """Recharge les fichiers de configuration en mémoire."""
        self._load_config()
        # self._load_gestures()
        # self._load_faq()