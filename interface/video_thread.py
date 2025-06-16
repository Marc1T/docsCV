# interface/video_thread.py
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from typing import Any
from core.gesture_detection import GestureDetector
from core.hand_recognition import HandRecognizer, HLabel, Gest
from core.gesture_controller import GestureController
from utils.helpers import opencv_to_qimage
import cv2, time
import numpy as np

class VideoThread(QThread):
    # Signal mis à jour pour inclure frame, geste et action
    frame_signal = pyqtSignal(QImage, str, str)

    def __init__(self, config: Any, logger: Any) -> None:
        super().__init__()
        self.config = config
        self.logger = logger
        self.running = False
        self.detector = GestureDetector(config, logger)
        self.hand_major = HandRecognizer(config, logger, HLabel.MAJOR)
        self.hand_minor = HandRecognizer(config, logger, HLabel.MINOR)
        self.controller = GestureController(config, logger)
        self.opencv_to_qimage = opencv_to_qimage        # Référence à la fonction utilitaire
        self.logger.info("VideoThread initialisé")

    def run(self) -> None:
        try:
            if not self.detector.start():
                self.logger.error("Échec démarrage détecteur")
                return
            
            frame_count = 0
            fps = 0
            last_time = time.time()

            self.running = True
            while self.running:
                image, results = self.detector.process_frame()
                q_image = opencv_to_qimage(image) # type: ignore
                if image is None or results is None:
                    self.logger.debug("Frame ou résultats manquants")
                    self.frame_signal.emit(q_image, "Aucun", "Aucune action")
                    continue

                gest_name = "Aucun"
                action = "Aucune action"
                if results.multi_hand_landmarks:
                    self.hand_major.update_hand_result(self.detector.major_hand)
                    self.hand_minor.update_hand_result(self.detector.minor_hand)
                    self.hand_major.set_finger_state()
                    self.hand_minor.set_finger_state()
                    gest_name_minor = self.hand_minor.get_gesture()
                    gest_name_major = self.hand_major.get_gesture()

                    if gest_name_minor == Gest.PINCH_MINOR:
                        gest_name = gest_name_minor.name
                        action = self.config.get_gesture_action(gest_name)
                        self.controller.handle_gesture(gest_name_minor, self.hand_minor.hand_result, HLabel.MINOR)
                    elif gest_name_major != Gest.PALM:
                        gest_name = gest_name_major.name
                        action = self.config.get_gesture_action(gest_name)
                        self.controller.handle_gesture(gest_name_major, self.hand_major.hand_result, HLabel.MAJOR)
                
                # Calcul des FPS
                frame_count += 1
                if time.time() - last_time >= 1.0:  # Toutes les secondes
                    fps = frame_count
                    frame_count = 0
                    last_time = time.time()
                    
                # Si l'option est activée
                if self.config.get_setting("DISPLAY", "show_fps", "False").lower() == "true":
                    q_image = self._draw_fps(image, fps)

                self.frame_signal.emit(q_image, gest_name, action)
                self.msleep(int(self.config.get_setting("DEFAULT", "frame_delay_ms", 30)))

        except Exception as e:
            self.logger.error(f"Erreur thread vidéo : {e}")
        finally:
            self._cleanup()

    def stop(self) -> None:
        if self.running:  # Vérifier si le thread est actif
            self.running = False
            self.detector.stop()
            self.quit()  # Signale au thread qu'il doit s'arrêter
            self.wait()  # Assure l'arrêt propre
            self.logger.info("VideoThread arrêté")

    def update_camera(self, camera_index: int) -> bool:
        try:
            was_running = self.isRunning()
            if was_running:
                self.stop()  # Arrêt propre avec wait()
                self.wait(500)
            
            success = self.detector.update_camera(camera_index)
            
            if was_running and success:
                self.start()  # Redémarrage seulement si nécessaire
                
            return success
        except Exception as e:
            self.logger.error(f"Erreur changement caméra: {e}")
            return False

    def _cleanup(self) -> None:
        self.detector.stop()
        self.running = False
        self.logger.info("Ressources vidéo libérées")
    
    def _draw_fps(self, frame: np.ndarray, fps: int) -> QImage:
        """Gère le dessin du FPS et la conversion en QImage"""
        try:
            from utils.helpers import draw_fps, opencv_to_qimage
            frame_with_fps = draw_fps(frame.copy(), fps)
            return opencv_to_qimage(frame_with_fps)
        except Exception as e:
            self.logger.error(f"Erreur traitement FPS: {str(e)}")
            return self.opencv_to_qimage(frame)  # Retourne l'image originale en cas d'erreur