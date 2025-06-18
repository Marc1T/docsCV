## **– Détection des gestes**  

### **🔍 Rôle du module**
Ce module est **le point d’entrée** du système de reconnaissance gestuelle.  
✅ Il **capture le flux vidéo** en temps réel 📹  
✅ Il **détecte les landmarks des mains** grâce à **MediaPipe** ✋  
✅ Il **transmet les données aux modules de reconnaissance et contrôle** 🖱  

---

### **⚙️ Fonctionnement interne**
Le module **analyse chaque frame vidéo**, détecte **les mains présentes**, et identifie **les points clés (landmarks)** pour interpréter les mouvements.

📌 **Flux de traitement** :
1️⃣ **Capture vidéo avec OpenCV** 🎥  
2️⃣ **Application du modèle MediaPipe** 🤖  
3️⃣ **Extraction des coordonnées des doigts** 🖐  
4️⃣ **Envoi des données à HandRecognizer pour l’analyse** 🔄  

💡 **Exemple de code – Détection des mains avec MediaPipe** :
```python
import cv2
import mediapipe as mp

class GestureDetector:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands()

    def process_frame(self, frame):
        """Analyse une image et détecte les mains."""
        results = self.hands.process(frame)
        return results.multi_hand_landmarks  # Retourne les points clés détectés
```

📌 **Utilisation du module** :
```python
detector = GestureDetector()
landmarks = detector.process_frame(frame)
print(landmarks)  # Liste des positions des doigts
```

---

### **🔗 Interaction avec les autres modules**
Le module **GestureDetector** transmet les données détectées à **HandRecognizer**, qui **interprète les gestes** en fonction des positions des doigts.

💡 **Exemple : Association avec HandRecognizer** :
```python
from core.hand_recognition import HandRecognizer

class GestureDetector:
    def __init__(self, config, logger):
        self.hand_major = HandRecognizer(config, logger, "MAJOR")

    def process_frame(self, frame):
        """Détecte les mains et analyse les gestes."""
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                self.hand_major.update_hand_result(hand)
                gesture = self.hand_major.get_gesture()
                return gesture  # Retourne le geste reconnu
        return None
```

---

### **📌 Optimisation et amélioration**
💡 **Astuces pour améliorer la détection des gestes** :
✔ **Améliorer la sensibilité** en ajustant `settings.ini` :
```ini
[DEFAULT]
threshold = 45  # Réduit le bruit et améliore la précision
sensitivity = 90
```
✔ **Éviter les erreurs dues à l’éclairage** 📸  
✔ **Limiter la latence en optimisant le traitement vidéo** 🔄  

---