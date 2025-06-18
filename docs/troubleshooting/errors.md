## **Dépannage et Résolution des Problèmes**  

Dans cette section, nous allons aborder **les erreurs fréquentes** et leurs **solutions**, afin d’assurer un fonctionnement optimal de **GestureMouseApp**.

---

### **📂 `troubleshooting/errors.md` – Erreurs courantes et solutions**  

#### 🖥 **1️⃣ La caméra ne fonctionne pas**  
📌 **Problème** : L’application ne détecte pas votre webcam.  
✅ **Solutions** :  
- Vérifiez que votre **webcam est bien connectée**.  
- Changez la caméra via **l’onglet Vidéo** dans l’interface.  
- Testez avec **un autre périphérique** (USB externe).  
- Exécutez cette commande pour voir les caméras disponibles :  
```python
import cv2
index = 0
while index < 5:
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"Caméra {index} détectée")
    cap.release()
    index += 1
```

---

#### ✋ **2️⃣ Les gestes ne sont pas détectés**  
📌 **Problème** : Aucun geste n’est reconnu à l’écran.  
✅ **Solutions** :  
- Assurez-vous que votre **main est bien visible** dans le cadre.  
- **Améliorez l’éclairage** pour une meilleure reconnaissance.  
- **Ajustez la sensibilité** dans `settings.ini` :
```ini
[DEFAULT]
sensitivity = 90
threshold = 45
```
- Testez avec **une distance différente** (1-2 mètres de la caméra).  

---

#### 🔊 **3️⃣ Le curseur tremble ou bouge mal**  
📌 **Problème** : Mouvement imprécis du curseur.  
✅ **Solutions** :  
- Réglez les paramètres **`cursor_dead_zone`** et **`cursor_min_ratio`** dans `settings.ini`.  
- Ajustez **l’environnement lumineux** (évitez les reflets).  
- **Vérifiez la fréquence d’image** (`FPS`) dans `video_thread.py`.  

---

#### 🔧 **4️⃣ L’application plante ou affiche une erreur**  
📌 **Problème** : **Crash** ou **messages d’erreur** inattendus.  
✅ **Solutions** :  
- Consultez **`logs/app.log`** pour voir les erreurs.  
- Vérifiez que **toutes les dépendances sont bien installées** :
```bash
pip install -r requirements.txt
```
- Redémarrez **GestureMouseApp** après une mise à jour.  

---

✨ **Avec ces solutions, votre application devrait fonctionner sans problème !**  