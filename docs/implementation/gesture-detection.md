
# Détection et Reconnaissance des Gestes

## Pipeline de Traitement

1. Capture vidéo avec OpenCV
2. Détection des mains avec MediaPipe
3. Extraction des landmarks (21 points par main)
4. Classification des gestes
5. Mapping geste → action

## Algorithme de Reconnaissance

```python
def get_gesture(self):
    # 1. Calcul des distances entre les landmarks
    dist_index = self.get_dist([8, 5])  # Index
    dist_middle = self.get_dist([12, 9])  # Majeur
    
    # 2. Calcul des ratios caractéristiques
    ratio_index = dist_index / dist_middle
    
    # 3. Classification basée sur les seuils
    if ratio_index > self.vgest_threshold:
        return Gest.V_GEST
    elif self.get_pinch_strength() > self.pinch_threshold:
        return Gest.PINCH_MAJOR
    # ...
```

## Défis et Solutions

**Problème** : Variabilité des gestes entre utilisateurs  
**Solution** : Seuils configurables dans `settings.ini`

**Problème** : Latence du traitement  
**Solution** : Thread séparé pour le traitement vidéo

**Problème** : Faux positifs  
**Solution** : Validation sur plusieurs frames (min_frames_confirm)