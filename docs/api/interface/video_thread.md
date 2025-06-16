# VideoThread

Thread pour le traitement vidéo en arrière-plan.

::: interface.video_thread.VideoThread
    options:
      heading_level: 2
      show_source: true
      members:
        - __init__
        - run
        - stop
        - update_camera
        - _cleanup

## Description

Cette classe :
- Hérite de QThread pour exécution en arrière-plan
- Capture et traite les frames vidéo en continu
- Émet un signal avec les résultats pour mise à jour UI
- Gère le changement de caméra à chaud

## Cycle de vie du thread

mermaid
stateDiagram-v2
    [*] --> Stopped
    Stopped --> Running : start()
    Running --> Processing : run()
    Processing --> Emitting : frame traitée
    Emitting --> Processing : frame suivante
    Running --> Stopped : stop()
    Stopped --> [*]


## Signal émis

python
frame_signal = pyqtSignal(QImage, str, str)


Paramètres :
1. `QImage` - Image à afficher
2. `str` - Nom du geste détecté
3. `str` - Action exécutée

