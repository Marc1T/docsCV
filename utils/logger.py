# utils/logger.py
"""
Système de journalisation pour GestureMouseApp.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional, Any
from PyQt5.QtCore import QObject, pyqtSignal

class QtHandler(QObject, logging.Handler):
    """
    Handler pour émettre les logs critiques à l'UI via PyQt5.

    Attributes:
        log_signal (pyqtSignal): Signal émettant les messages de log.
        flushOnClose (bool): Indique si flush est requis à la fermeture.
    """
    log_signal = pyqtSignal(str)
    flushOnClose = False  # Désactiver flush à la fermeture

    def __init__(self) -> None:
        QObject.__init__(self)
        logging.Handler.__init__(self)

    def emit(self, record: logging.LogRecord) -> None:
        """Émet le message de log via le signal."""
        if record.levelno >= logging.WARNING:
            msg = self.format(record)
            self.log_signal.emit(msg)

class Logger:
    """
    Fournit un logger configurable pour journalisation centralisée.

    Attributes:
        logger (logging.Logger): Instance du logger.
        config (Any): Gestionnaire de configuration (optionnel).
        qt_handler (QtHandler): Handler pour l’UI.
    """

    def __init__(self, config_manager: Optional[Any] = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = config_manager
        self.qt_handler = QtHandler()
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure le logger avec les paramètres depuis config_manager ou par défaut."""
        try:
            # Paramètres par défaut
            level_name = "INFO"
            level = logging.INFO
            log_file = "logs/app.log"
            log_to_file = True
            log_format = "%(asctime)s [%(levelname)s] %(message)s"

            # Si config_manager est disponible, lire les paramètres
            if self.config:
                from utils.config_manager import ConfigManager  # Import différé
                if isinstance(self.config, ConfigManager):
                    level_name = self.config.get_setting("LOGGING", "log_level", "INFO").upper()
                    level = getattr(logging, level_name, logging.INFO)
                    log_file = self.config.get_setting("LOGGING", "log_file", "logs/app.log")
                    log_to_file = self.config.get_setting("LOGGING", "log_to_file", "True").lower() == "true"
                    # Restaurer les % simples
                    raw_format = self.config.get_setting("LOGGING", "log_format", log_format)
                    log_format = raw_format.replace("%%", "%")

            # Reset handlers
            self.logger.handlers.clear()
            self.logger.setLevel(level)

            # Formatter
            formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
            formatter.default_msec_format = "%s.%03d"

            # Handler console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # Handler fichier
            if log_to_file:
                try:
                    if not os.path.exists(os.path.dirname(log_file)):
                        os.makedirs(os.path.dirname(log_file))
                    file_handler = RotatingFileHandler(
                        log_file,
                        maxBytes=5 * 1024 * 1024,  # 5MB
                        backupCount=3  # Garder 3 fichiers de backup
                    )
                    file_handler.setFormatter(formatter)
                    self.logger.addHandler(file_handler)
                except Exception as e:
                    print(f"Erreur configuration fichier log : {e}")
                    self.logger.warning(f"Erreur configuration fichier log : {e}")

            # Handler PyQt5 pour UI
            self.qt_handler.setFormatter(formatter)
            self.logger.addHandler(self.qt_handler)

            self.logger.info(f"Logger initialisé (niveau={level_name}, fichier={log_file})")
        except Exception as e:
            print(f"Erreur initialisation logger : {e}")
            raise

    def get_log_signal(self):
        """Retourne le signal pour les logs UI."""
        return self.qt_handler.log_signal

    def set_log_level(self, level: str) -> None:
        """Reconfigure le niveau de log dynamiquement."""
        try:
            level = level.upper()
            if hasattr(logging, level):
                self.logger.setLevel(getattr(logging, level))
                if self.config:
                    from utils.config_manager import ConfigManager  # Import différé
                    if isinstance(self.config, ConfigManager):
                        self.config.set_setting("LOGGING", "log_level", level)
                self.logger.info(f"Niveau de log changé : {level}")
            else:
                raise ValueError(f"Niveau de log invalide : {level}")
        except Exception as e:
            self.logger.error(f"Erreur changement niveau de log : {e}")
            raise

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.critical(msg, *args, **kwargs)