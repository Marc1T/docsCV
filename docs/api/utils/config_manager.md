# ConfigManager

Gestion centralisée de la configuration.

::: utils.config_manager.ConfigManager
    options:
      heading_level: 2
      show_source: true
      members:
        - __init__
        - _load_config
        - _create_default_config
        - _load_gestures
        - _create_default_gestures
        - _load_faq
        - _create_default_faq
        - validate_param
        - get_setting
        - set_setting
        - get_gesture_action
        - set_gesture_action
        - get_faq_data
        - get_available_cameras
        - reset_to_default
        - reload

## Structure des fichiers

### settings.ini
ini
[DEFAULT]
camera_index = 0
show_landmarks = True
sensitivity = 50

[UI]
stylesheet = "QMainWindow { ... }"

[LOGGING]
log_level = INFO


### gestures.json
json
{
    "V_GEST": "move_cursor",
    "FIST": "mouse_down",
    "PINCH_MINOR": "scroll"
}


## Workflow de chargement

mermaid
graph LR
    A[Démarrage] --> B[Charger settings.ini]
    A --> C[Charger gestures.json]
    A --> D[Charger faq.json]
    B --> E[Valider paramètres]
    C --> F[Initialiser mapping gestes]
    D --> G[Préparer données FAQ]
    E --> H[Config prête]


## Méthodes clés

- `get_setting()`: Récupère un paramètre avec validation
- `set_setting()`: Modifie un paramètre et sauvegarde
- `get_available_cameras()`: Détecte les caméras accessibles

