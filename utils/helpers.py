# utils/helpers.py
"""
Fonctions utilitaires pour GestureMouseApp.
"""

from typing import Optional, Tuple, Any
import cv2
import numpy as np
from PyQt5.QtGui import QImage
import pyautogui
import logging

def opencv_to_qimage(frame: np.ndarray) -> QImage:
    """
    Convertit une image OpenCV (BGR) en QImage pour PyQt5 de manière robuste.

    Args:
        frame (np.ndarray): Image OpenCV (format BGR, RGB ou grayscale).

    Returns:
        QImage: Image convertie pour affichage dans PyQt5.

    Raises:
        ValueError: Si le format d'image n'est pas supporté.
    """
    try:
        if frame is None or not isinstance(frame, np.ndarray):
            raise ValueError("L'image d'entrée doit être un tableau numpy valide")

        h, w = frame.shape[:2]
        
        # Gestion des différents formats d'image
        if len(frame.shape) == 2:  # Grayscale
            return QImage(frame.data, w, h, w, QImage.Format_Grayscale8)
        elif frame.shape[2] == 3:  # BGR/RGB
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return QImage(rgb_image.data, w, h, 3 * w, QImage.Format_RGB888)
        elif frame.shape[2] == 4:  # BGRA/RGBA
            rgba_image = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
            return QImage(rgba_image.data, w, h, 4 * w, QImage.Format_RGBA8888)
        else:
            raise ValueError(f"Format d'image non supporté: {frame.shape}")
            
    except Exception as e:
        logging.error(f"Erreur conversion OpenCV vers QImage: {str(e)}")
        raise ValueError(f"Erreur conversion image: {str(e)}") from e

def draw_fps(frame: np.ndarray, fps: int) -> np.ndarray:
    """
    Dessine le compteur FPS sur une image OpenCV.

    Args:
        frame (np.ndarray): Image OpenCV (format BGR).
        fps (int): Valeur FPS à afficher.

    Returns:
        np.ndarray: Image avec FPS dessiné.
    """
    try:
        if frame is None or not isinstance(frame, np.ndarray):
            raise ValueError("Image invalide pour dessiner FPS")
            
        fps_text = f"FPS: {fps}"
        cv2.putText(frame, fps_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        return frame
    except Exception as e:
        logging.error(f"Erreur dessin FPS: {str(e)}")
        return frame
    
def validate_landmarks(landmarks: Any, min_count: int = 21) -> bool:
    """
    Valide si les landmarks MediaPipe sont corrects.

    Args:
        landmarks (Any): Landmarks MediaPipe.
        min_count (int): Nombre minimum de landmarks requis.

    Returns:
        bool: True si valide, False sinon.
    """
    try:
        if landmarks is None or not hasattr(landmarks, "landmark") or len(landmarks.landmark) < min_count:
            return False
        return True
    except Exception:
        return False

def camera_to_screen_coords(
    x: float, y: float, frame_width: int, frame_height: int
) -> Tuple[int, int]:
    """
    Convertit les coordonnées caméra normalisées en coordonnées écran.

    Args:
        x (float): Coordonnée x normalisée (0 à 1).
        y (float): Coordonnée y normalisée (0 à 1).
        frame_width (int): Largeur de la frame caméra.
        frame_height (int): Hauteur de la frame caméra.

    Returns:
        Tuple[int, int]: Coordonnées écran (x, y).
    """
    try:
        screen_width, screen_height = pyautogui.size()
        # Ajuster pour centrer et refléter (caméra peut être inversée)
        screen_x = int((1 - x) * screen_width)
        screen_y = int(y * screen_height)
        # Limiter aux bornes de l'écran
        screen_x = max(0, min(screen_x, screen_width - 1))
        screen_y = max(0, min(screen_y, screen_height - 1))
        return screen_x, screen_y
    except Exception as e:
        raise ValueError(f"Erreur conversion coordonnées : {e}")
    
def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Limite une valeur entre min_val et max_val inclus.

    Args:
        value (float): Valeur à limiter.
        min_val (float): Valeur minimum.
        max_val (float): Valeur maximum.

    Returns:
        float: Valeur limitée.
    """
    return max(min_val, min(max_val, value))