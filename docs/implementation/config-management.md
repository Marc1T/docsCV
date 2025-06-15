# Gestion de Configuration

## Système Hiérarchique

```
graph LR
    A[settings.ini] --> B[Paramètres généraux]
    A --> C[Paramètres UI]
    A --> D[Paramètres détection]
    E[gestures.json] --> F[Mapping gestes-actions]
    G[faq.json] --> H[Questions/Réponses]
```

## Chargement et Validation

Le ConfigManager valide tous les paramètres :

```python
def validate_param(self, key: str, value: Any) -> Any:
    rules = {
        "sensitivity": (int, 0, 100),
        "threshold": (float, 0.1, 1.0)
    }
    
    if key in rules:
        param_type, min_val, max_val = rules[key]
        val = param_type(value)
        return clamp(val, min_val, max_val)
```

## Mécanisme de Fallback

1. Tente de lire la valeur configurée
2. Si absente ou invalide, utilise la valeur par défaut
3. Enregistre un avertissement dans les logs
