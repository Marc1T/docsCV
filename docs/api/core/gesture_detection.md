# GestureDetector

Classe responsable de la capture vidéo et de la détection des mains avec MediaPipe.

::: core.gesture_detection.GestureDetector
    options:
      heading_level: 2
      show_source: true
      show_root_heading: true
      members:
        - __init__
        - start
        - stop
        - update_camera
        - process_frame
        - _classify_hands

## Description

La classe `GestureDetector` encapsule toute la logique de capture vidéo et de détection des mains :
- Initialise la capture vidéo avec OpenCV
- Utilise MediaPipe pour détecter les mains dans chaque frame
- Identifie la main dominante et non dominante
- Fournit les résultats de détection à d'autres composants

## Exemple d'utilisation

python
from core.gesture_detection import GestureDetector
from utils.config_manager import ConfigManager

config = ConfigManager()
detector = GestureDetector(config, logger)

if detector.start():
    frame, results = detector.process_frame()
    # Traiter les résultats...


## Diagramme de séquence

mermaid
sequenceDiagram
    participant App
    participant GestureDetector
    participant MediaPipe
    participant OpenCV
    
    App->>GestureDetector: start()
    GestureDetector->>OpenCV: VideoCapture()
    loop Frame Processing
        GestureDetector->>OpenCV: read()
        GestureDetector->>MediaPipe: process()
        MediaPipe-->>GestureDetector: results
        GestureDetector-->>App: (frame, results)
    end
    App->>GestureDetector: stop()
    GestureDetector->>OpenCV: release()
```
```