
## **– API du projet**  
### **1️⃣ Introduction**
L’API interne de **GestureMouseApp** permet aux développeurs d’**interagir avec les modules** pour :
✅ Détecter et interpréter les gestes ✋  
✅ Personnaliser les actions du système 🖱️  
✅ Modifier les paramètres utilisateur ⚙️  
✅ Étendre la reconnaissance des mains 🛠️  

---

### **2️⃣ Classes et méthodes principales**
📌 Voici les composants clés de l’API :

#### **🖐 GestureDetector (`core/gesture_detection.py`)**
✅ Capture le flux vidéo  
✅ Analyse les landmarks des mains  
✅ Retourne les positions pour la reconnaissance  

```python
class GestureDetector:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.hands = mp.solutions.hands.Hands()

    def process_frame(self, frame):
        results = self.hands.process(frame)
        return results.multi_hand_landmarks
```

📌 **Utilisation** :
```python
detector = GestureDetector(config, logger)
landmarks = detector.process_frame(frame)
print(landmarks)  # Liste des positions des doigts
```

---

#### **✋ HandRecognizer (`core/hand_recognition.py`)**
✅ Détecte la posture des doigts  
✅ Détermine le geste en cours  
✅ Optimise la reconnaissance des actions  

```python
class HandRecognizer:
    def __init__(self, config, logger, label):
        self.label = label  # MAJOR ou MINOR
        self.hand_result = None
        self.fingers = []

    def update_hand_result(self, hand_data):
        self.hand_result = hand_data

    def set_finger_state(self):
        self.fingers = [
            1 if tip.y < pip.y else 0
            for tip, pip in zip(self.hand_result.landmark[4:], self.hand_result.landmark[0:])
        ]

    def get_gesture(self):
        if self.fingers == [0, 1, 1, 1, 1]:
            return "V_GEST"
        elif self.fingers == [0, 0, 0, 0, 0]:
            return "FIST"
        return "UNKNOWN"
```

📌 **Utilisation** :
```python
hand_rec = HandRecognizer(config, logger, "MAJOR")
hand_rec.update_hand_result(hand_data)
gesture = hand_rec.get_gesture()
print(gesture)  # Geste détecté
```

---

#### **🖱 GestureController (`core/gesture_controller.py`)**
✅ Gère l’exécution des commandes système  
✅ Envoie des actions à l’interface utilisateur  
✅ Interagit avec le curseur et les raccourcis  

```python
import pyautogui

class GestureController:
    def handle_gesture(self, gesture_name):
        if gesture_name == "V_GEST":
            pyautogui.moveTo(500, 300)
        elif gesture_name == "PINCH_MAJOR":
            pyautogui.press("volume_up")
```

📌 **Utilisation** :
```python
controller = GestureController()
controller.handle_gesture("V_GEST")  # Déplace la souris
```

---

✨ **Avec ces modules, vous pouvez interagir et étendre GestureMouseApp !**  
📌 **Passons maintenant à `dev/extensions.md`, qui explique comment ajouter de nouvelles fonctionnalités !** 🚀  

---

