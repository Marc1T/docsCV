# FAQBot

Système de questions/réponses intelligent.

::: chatbot.faq_bot.FAQBot
    options:
      heading_level: 2
      show_source: true
      members:
        - __init__
        - _load_faq
        - _preprocess_text
        - _initialize_vectorizer
        - get_response
        - reload_faq

## Workflow NLP

mermaid
flowchart TD
    A[Question utilisateur] --> B[Prétraitement]
    B --> C[Vectorisation TF-IDF]
    C --> D[Calcul similarité]
    D --> E[Sélection réponse]
    E --> F[Retour réponse]


## Processus de prétraitement

1. Conversion en minuscules
2. Suppression de la ponctuation
3. Tokenisation
4. Suppression des stopwords
5. Stemming

## Exemple de configuration

python
bot = FAQBot(config_manager, logger)
response = bot.get_response("Comment changer de caméra ?")
print(response)  # Affiche la réponse appropriée


## Paramètres

- `similarity_threshold`: Seuil de confiance (0.5 par défaut)
- `faq_data`: Liste structurée des questions/réponses


## Intégration dans mkdocs.yml

Mettez à jour votre configuration pour inclure toute l'API :

yaml
nav:
  - Accueil: index.md
  - Guide Utilisateur:
    - Installation: guide/installation.md
    - Utilisation: guide/usage.md
  - Implémentation Technique:
    - Architecture: implementation/architecture.md
    - Détection Gestuelle: implementation/gesture-detection.md
    - Interface: implementation/ui-system.md
    - Configuration: implementation/config-management.md
    - FAQ Intelligente: implementation/faq-system.md
  - Référence API:
    - Core:
      - Gesture Detection: api-reference/core/gesture_detection.md
      - Hand Recognition: api-reference/core/hand_recognition.md
      - Gesture Controller: api-reference/core/gesture_controller.md
    - Interface:
      - Main Window: api-reference/interface/main_window.md
      - Video Thread: api-reference/interface/video_thread.md
      - Settings Dialog: api-reference/interface/settings_dialog.md
      - About Dialog: api-reference/interface/about_dialog.md
    - Utilitaires:
      - Config Manager: api-reference/utils/config_manager.md
      - Logger: api-reference/utils/logger.md
      - Helpers: api-reference/utils/helpers.md
    - Chatbot:
      - FAQ Bot: api-reference/chatbot/faq_bot.md
