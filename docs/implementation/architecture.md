# Architecture du Système

GestureMouseApp suit une architecture modulaire avec une séparation claire des responsabilités :

```mermaid
graph TD
    A[main.py] --> B[Interface]
    A --> C[Core]
    A --> D[Utils]
    B --> E[MainWindow]
    B --> F[VideoThread]
    C --> G[GestureDetection]
    C --> H[HandRecognition]
    C --> I[GestureController]
    D --> J[ConfigManager]
    D --> K[Logger]
```

## Composants Clés

1. **Couche Interface (PyQt5)** :
   - Gestion des fenêtres et dialogues
   - Thread vidéo pour le traitement en temps réel
   - Communication via les signaux/slots

2. **Couche Core (Logique Métier)** :
   - Détection des gestes avec MediaPipe
   - Reconnaissance des gestes spécifiques
   - Exécution des actions système

3. **Couche Utils (Services)** :
   - Gestion de configuration (INI/JSON)
   - Journalisation centralisée
   - Fonctions utilitaires

## Flux de Données

```mermaid
sequenceDiagram
    Utilisateur->>Interface: Interagit avec l'UI
    Interface->>VideoThread: Démarre le flux vidéo
    VideoThread->>GestureDetection: Envoie les frames
    GestureDetection->>HandRecognition: Analyse les landmarks
    HandRecognition->>GestureController: Identifie le geste
    GestureController->>Système: Exécute l'action
    GestureController->>Interface: Retourne le feedback
```

## Principes de Conception

- **Découplage** : Les modules communiquent via des interfaces définies
- **Configurable** : Tous les paramètres sont externalisés
- **Extensible** : Ajout facile de nouveaux gestes ou actions
- **Robuste** : Gestion d'erreurs à tous les niveaux
