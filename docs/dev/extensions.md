## **– Ajout de nouvelles fonctionnalités**  

### **1️⃣ Introduction**
Vous pouvez facilement **ajouter de nouveaux gestes** et **personnaliser les actions système** grâce à **l’architecture modulaire** de GestureMouseApp.

✅ **Ajouter un nouveau geste dans `gestures.json`**  
✅ **Développer une logique de reconnaissance dans `gesture_controller.py`**  
✅ **Adapter l’interface utilisateur si nécessaire**  

---

### **2️⃣ Ajouter un geste personnalisé**
📌 **Exemple : Ajouter un geste "Zoom avant"** (a noter que le zoom est deja ajoute) 

1️⃣ **Définir le geste dans `gestures.json`** :
```json
{
    "ZOOM_IN": "zoom_plus"
}
```

2️⃣ **Implémenter la détection dans `gesture_controller.py`** :
```python
class GestureController:
    def handle_gesture(self, gesture_name):
        if gesture_name == "ZOOM_IN":
            pyautogui.hotkey("ctrl", "+")
```

📌 **Utilisation** :
```python
controller = GestureController()
controller.handle_gesture("ZOOM_IN")  # Zoom avant
```

---

### **3️⃣ Ajouter un mode de détection avancée**
✅ **Étendre `gesture_detection.py`** pour intégrer **détection multi-mains**  
✅ **Modifier `hand_recognition.py`** pour gérer **gestes combinés**  

📌 **Exemple : Double-pinch détecté sur les deux mains**  
```python
class HandRecognizer:
    def get_gesture(self):
        if self.fingers == [0, 0, 0, 0, 1] and self.label == "MAJOR":
            return "PINCH_MAJOR"
        elif self.fingers == [0, 0, 0, 0, 1] and self.label == "MINOR":
            return "PINCH_MINOR"
        return "UNKNOWN"
```
💡 **Cela permet d’interpréter les gestes séparément pour une plus grande précision** !

---

### **4️⃣ Améliorer la réactivité**
Pour **optimiser la détection**, ajustez les **paramètres de `settings.ini`** :

📌 **Modifier le seuil de détection** :
```ini
[DEFAULT]
sensitivity = 90
threshold = 45
```

---
✨ **Avec ces améliorations, vous pouvez étendre GestureMouseApp et l’adapter à vos besoins !** 