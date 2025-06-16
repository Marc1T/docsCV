# MainWindow

Fenêtre principale de l'application.

::: interface.main_window.MainWindow
    options:
      heading_level: 2
      show_source: true
      members:
        - __init__
        - _init_ui
        - _setup_toolbar
        - _setup_video_tab
        - _setup_faq_tab
        - _setup_status_bar
        - update_video_frame
        - _start_detection
        - _stop_detection

## Description

La classe `MainWindow` :
- Crée l'interface utilisateur principale avec PyQt5
- Gère les onglets vidéo et FAQ
- Contrôle la barre d'outils et la barre d'état
- Connecte les signaux des threads aux slots d'UI

## Structure UI

mermaid
classDiagram
    class MainWindow {
        +QTabWidget tab_widget
        +VideoThread video_thread
        +QLabel video_label
        +QComboBox camera_combo
        +QTextEdit faq_input
        +QTextEdit faq_output
        +init_ui()
        +update_video_frame()
        +_start_detection()
        +_stop_detection()
    }
    
    MainWindow --> VideoThread
    MainWindow --> SettingsDialog


## Signaux et Slots

| Signal                     | Slot                      | Description                          |
|----------------------------|---------------------------|--------------------------------------|
| `video_thread.frame_signal`| `update_video_frame`      | Met à jour l'affichage vidéo         |
| `camera_combo.currentIndexChanged`| `_change_camera`    | Change la caméra sélectionnée        |
| `faq_button.clicked`       | `_send_faq_question`      | Traite la question FAQ               |

