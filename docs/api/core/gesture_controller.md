# GestureController

Contrôle les actions système basées sur les gestes détectés.

::: core.gesture_controller.GestureController
    options:
      heading_level: 2
      show_source: true
      members:
        - __init__
        - get_pinch_y_lv
        - get_pinch_x_lv
        - change_system_volume
        - change_system_brightness
        - scroll_vertical
        - scroll_horizontal
        - get_position
        - pinch_control_init
        - pinch_control
        - handle_gesture

## Description

La classe `GestureController` :
- Transforme les gestes en actions système
- Contrôle la souris, le clavier, le volume et la luminosité
- Implémente un système de "pinch control" pour les gestes continus

## Mapping des actions

| Geste             | Action                          | Méthode associée                 |
|-------------------|----------------------------------|----------------------------------|
| `V_GEST`          | Déplacement curseur             | `get_position()`                 |
| `FIST`            | Clic maintenu                   | `handle_gesture()`               |
| `PINCH_MINOR`     | Défilement                      | `scroll_vertical/horizontal()`   |
| `PINCH_MAJOR`     | Volume/luminosité               | `change_system_volume/brightness()` |

## Séquence d'exécution

mermaid
sequenceDiagram
    participant HandRecognition
    participant GestureController
    participant Système
    
    HandRecognition->>GestureController: get_gesture()
    GestureController->>GestureController: handle_gesture()
    alt Geste PINCH
        GestureController->>GestureController: pinch_control()
        GestureController->>Système: action_continue()
    else Autre geste
        GestureController->>Système: action_ponctuelle()
    end
```
```
