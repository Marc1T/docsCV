# Premiers pas

## Calibration initiale

```mermaid
sequenceDiagram
    Utilisateur->>Application: Lance l'application
    Application->>Utilisateur: Affiche l'assistant de calibration
    Utilisateur->>Application: Effectue les gestes demandés
    Application->>Système: Calcule les paramètres optimaux
    Système-->>Application: Confirme la calibration
    Application-->>Utilisateur: Prêt à l'emploi
```

## Interface principale

```mermaid
graph TD
    A[Barre d'outils] --> B[Contrôles vidéo]
    A --> C[Paramètres]
    A --> D[Aide]
    E[Onglet Vidéo] --> F[Flux caméra]
    E --> G[Statut détection]
    H[Onglet FAQ] --> I[Chatbot]
    H --> J[Base de connaissances]
```

## Gestes fondamentaux

| Geste | Visualisation | Action |
|-------|---------------|--------|
| **V_GEST** | ![V_GEST](assets/gesture-v.png) | Déplacement curseur |
| **FIST** | ![FIST](assets/gesture-fist.png) | Clic maintenu |
| **PINCH** | ![PINCH](assets/gesture-pinch.png) | Défilement |
