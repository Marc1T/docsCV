## **– Installation et configuration**  
### **1️⃣ Installation rapide**  
Exécutez ces commandes :  
```bash
git clone https://github.com/Marc1T/GestureMouseApp.git
cd GestureMouseApp
pip install -r requirements.txt
```
💡 **Cela installe toutes les dépendances automatiquement**.  

---

### **2️⃣ Vérification après installation**
✅ **Tester la caméra** : Ouvrez l’application et vérifiez si la vidéo s’affiche correctement  
✅ **Lancer GestureMouseApp** :  
```bash
python main.py
```
🚀 **Si tout fonctionne, vous êtes prêt à utiliser les gestes !**  

---

### **3️⃣ Mise à jour de l’application**  
Il est recommandé de **mettre à jour régulièrement** GestureMouseApp pour bénéficier des **dernières corrections et améliorations**.  

✔ **Mettre à jour les dépendances** :  
```bash
pip install --upgrade -r requirements.txt
```

✔ **Mettre à jour le projet** (via GitHub) :  
```bash
git pull origin main
```

✔ **Vérifier la version actuelle** :  
Consultez `settings.ini`, où **`app_version`** est spécifié.

💡 **Si vous rencontrez un problème après une mise à jour**, consultez les logs dans **`logs/app.log`** pour voir d’éventuelles erreurs.

---