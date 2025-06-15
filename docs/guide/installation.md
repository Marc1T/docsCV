# Installation

## Prérequis

- Windows 10/11 (64-bit)
- Webcam compatible
- [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

## Méthodes d'installation

### Installation à partir du code source

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/Marc1T/gestureControl.git
   cd GestureMouseApp

2. Créer un environnement virtuel :
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Lancer l'application :
   ```bash
   python main.py
   ```

### Installation via l'exécutable

1. Télécharger la dernière version depuis [GitHub Releases](https://github.com/Marc1T/gestureControl.git/release)
2. Exécuter `GestureMouseApp-Setup.exe`
3. Suivre les instructions d'installation

### Installation avec pip
```bash
pip install gesturemouseapp
gesturemouseapp
```

## Vérification de l'installation

Après installation, lancez l'application et vérifiez :

1. La webcam est détectée
2. Les gestes sont reconnus dans l'onglet Vidéo
3. Le chatbot répond aux questions dans l'onglet FAQ
