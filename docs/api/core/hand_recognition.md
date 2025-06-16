# Hand Recognition

Classes et enums pour la reconnaissance des gestes.

::: core.hand_recognition.Gest
    options:
      heading_level: 2

::: core.hand_recognition.HLabel
    options:
      heading_level: 2

::: core.hand_recognition.HandRecognizer
    options:
      heading_level: 2
      show_source: true
      members:
        - __init__
        - update_hand_result
        - get_signed_dist
        - get_dist
        - get_dz
        - set_finger_state
        - get_gesture

## Description

Ce module contient :
- Les enums `Gest` et `HLabel` pour représenter les gestes et les mains
- La classe `HandRecognizer` qui analyse les landmarks pour identifier les gestes
- L'algorithme de classification basé sur les distances entre les landmarks

## Logique de reconnaissance

python
def get_gesture(self):
    # Calculer les distances caractéristiques
    dist_index = self.get_dist([8, 5])  # Index
    dist_middle = self.get_dist([12, 9])  # Majeur
    
    # Calculer les ratios
    ratio_index = dist_index / dist_middle
    
    # Classifier selon les seuils
    if ratio_index > self.vgest_threshold:
        return Gest.V_GEST
    elif self.get_pinch_strength() > self.pinch_threshold:
        return Gest.PINCH_MAJOR
    # ...


## Table des gestes

| Geste             | Description                      | Landmarks caractéristiques          |
|-------------------|----------------------------------|-------------------------------------|
| `V_GEST`          | Signe "V" avec index et majeur   | Distance élevée entre (8,12) et (5,9) |
| `PINCH_MAJOR`     | Pince avec pouce et index        | Distance faible entre 4 et 8        |
| `FIST`            | Main fermée                      | Tous les doigts repliés             |
| `PALM`            | Main ouverte                     | Tous les doigts étendus             |
