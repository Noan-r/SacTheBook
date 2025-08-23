# 🔄 Synchronisation GitHub - SacTheBook

## 📋 Vue d'ensemble

SacTheBook intègre maintenant une fonctionnalité de synchronisation avec GitHub qui permet de sauvegarder automatiquement les modifications des ouvertures d'échecs en ligne tout en conservant la fonctionnalité hors ligne.

## ✨ Fonctionnalités

### 🔄 Synchronisation Automatique
- **Sauvegarde automatique** : Chaque modification (ajout, édition, suppression) est automatiquement synchronisée vers GitHub
- **Fonctionnalité hors ligne** : L'application continue de fonctionner même sans connexion GitHub
- **Synchronisation manuelle** : Boutons pour synchroniser manuellement vers/depuis GitHub

### 🛡️ Sécurité et Fiabilité
- **Vérification des changements** : Seules les modifications réelles sont synchronisées
- **Gestion des erreurs** : Messages d'erreur clairs en cas de problème
- **Statut en temps réel** : Affichage du statut de la configuration GitHub

## 🚀 Configuration

### 1. Créer un Token GitHub

1. Allez sur [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Cliquez sur "Generate new token (classic)"
3. Donnez un nom au token (ex: "SacTheBook Sync")
4. Sélectionnez les permissions :
   - `repo` (accès complet aux repositories)
5. Cliquez sur "Generate token"
6. **Copiez le token** (il ne sera plus visible après)

### 2. Configuration des Variables d'Environnement

#### Pour le Développement Local
Créez un fichier `.env` à la racine du projet :

```env
GITHUB_TOKEN=ghp_votre_token_ici
GITHUB_REPO=Noan-r/SacTheBook
GITHUB_BRANCH=master
GITHUB_FILE_PATH=data/openings.json
```

#### Pour Render (Déploiement)
Dans les paramètres de votre service Render :

1. Allez dans "Environment"
2. Ajoutez les variables :
   - `GITHUB_TOKEN` = votre token GitHub
   - `GITHUB_REPO` = Noan-r/SacTheBook (ou votre repo)
   - `GITHUB_BRANCH` = master
   - `GITHUB_FILE_PATH` = data/openings.json

### 3. Installation des Dépendances

```bash
pip install -r requirements.txt
```

## 🎯 Utilisation

### Interface Utilisateur
1. Allez dans **Settings** (page des paramètres)
2. Une nouvelle section **"Synchronisation GitHub"** apparaît en haut
3. Le statut de la configuration s'affiche automatiquement

### Boutons de Synchronisation
- **📤 Synchroniser vers GitHub** : Envoie les modifications locales vers GitHub
- **📥 Synchroniser depuis GitHub** : Récupère les modifications depuis GitHub

### Synchronisation Automatique
- ✅ **Ajout d'ouverture** → Synchronisation automatique
- ✅ **Ajout de variation** → Synchronisation automatique
- ✅ **Édition de variation** → Synchronisation automatique
- ✅ **Suppression de variation** → Synchronisation automatique
- ✅ **Suppression d'ouverture** → Synchronisation automatique

## 🔧 Fonctionnement Technique

### Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interface     │    │   Flask App     │    │   GitHub API    │
│   Utilisateur   │◄──►│   (Backend)     │◄──►│   (Repository)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Fichier JSON  │
                       │   (Local)       │
                       └─────────────────┘
```

### Flux de Données
1. **Modification locale** → Sauvegarde dans `data/openings.json`
2. **Synchronisation automatique** → Envoi vers GitHub via API
3. **Commit automatique** → Création d'un commit avec les changements
4. **Feedback utilisateur** → Affichage du statut de synchronisation

### Gestion des Erreurs
- **Token invalide** → Désactivation de la synchronisation
- **Repository inaccessible** → Message d'erreur clair
- **Conflit de fichiers** → Gestion automatique des versions
- **Problème réseau** → Retry automatique

## 🛠️ Dépannage

### Problèmes Courants

#### ❌ "GitHub non configuré"
**Cause** : Token GitHub manquant ou invalide
**Solution** : Vérifiez que `GITHUB_TOKEN` est correctement configuré

#### ❌ "Repository non trouvé"
**Cause** : Mauvais nom de repository ou permissions insuffisantes
**Solution** : Vérifiez `GITHUB_REPO` et les permissions du token

#### ❌ "Erreur de synchronisation"
**Cause** : Problème réseau ou API GitHub indisponible
**Solution** : Réessayez plus tard ou vérifiez la connectivité

### Logs de Débogage
Les logs de synchronisation apparaissent dans la console du serveur :
```
DEBUG: Synchronisation GitHub: {'success': True, 'message': 'Données synchronisées vers GitHub'}
```

## 🔒 Sécurité

### Bonnes Pratiques
- ✅ **Token privé** : Ne partagez jamais votre token GitHub
- ✅ **Permissions minimales** : Utilisez seulement les permissions nécessaires
- ✅ **Rotation régulière** : Changez votre token périodiquement
- ✅ **Variables d'environnement** : Utilisez des variables d'environnement, pas de hardcoding

### Permissions Requises
- `repo` : Accès complet aux repositories (lecture/écriture)

## 📈 Avantages

### Pour les Utilisateurs
- ✅ **Sauvegarde automatique** : Plus de perte de données
- ✅ **Synchronisation multi-appareils** : Accès depuis n'importe où
- ✅ **Historique des modifications** : Suivi des changements via Git
- ✅ **Fonctionnalité hors ligne** : Travail possible sans connexion

### Pour les Développeurs
- ✅ **Backup automatique** : Sauvegarde des données utilisateur
- ✅ **Versioning** : Historique complet des modifications
- ✅ **Collaboration** : Possibilité de partager des ouvertures
- ✅ **Récupération** : Restauration facile en cas de problème

## 🎉 Conclusion

La synchronisation GitHub transforme SacTheBook en une application moderne avec sauvegarde automatique tout en conservant sa simplicité d'utilisation. Les utilisateurs peuvent maintenant travailler en toute confiance, sachant que leurs données sont sauvegardées et synchronisées automatiquement.
