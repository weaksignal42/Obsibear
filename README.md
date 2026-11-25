# Obsibear

Thèmes Obsidian **personnels** qui reproduisent des thèmes de [Bear](https://bear.app) (Shiny Frog) : couleurs, typographie, tags en pastille, code, tâches, tableaux.

| Thème | Dossier | État |
|---|---|---|
| Olive Dunk | `themes/olive-dunk/` | Mode clair, utilisé au quotidien (Mac, iPhone, iPad) |

## ⚠️ Projet strictement personnel

- Les valeurs de couleur et de mise en page viennent des fichiers `.theme` livrés dans Bear.app (`BearCore.framework/Resources`).
- Les thèmes utilisent les **polices propriétaires de Bear** (Bear Sans UI, Bear Sans UI Heading, basées sur Clarika) et Roboto Mono.
- **Les polices ne sont pas dans ce dépôt.** `build.py` les lit dans l'application Bear installée et les intègre aux thèmes au moment de la construction. `dist/` et tout fichier de police sont exclus par `.gitignore`.
- Ces thèmes ne sont **pas destinés à être publiés** ni partagés (pas de thème communautaire Obsidian, pas de dépôt public).

## Construire et installer

Prérequis : Bear installé dans `/Applications`, Python 3.

```bash
pip install -r requirements.txt
python3 build.py --install "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyBrain"
```

Les thèmes sont construits dans `dist/<Nom>/`, puis copiés dans `.obsidian/themes/<Nom>/` du coffre. Le coffre étant synchronisé par iCloud, ils arrivent tels quels sur iPhone et iPad, polices comprises. `python3 build.py olive-dunk` ne construit qu'un thème.

Dans Obsidian : Réglages → Apparence → Thèmes.

## Structure

| Fichier | Rôle |
|---|---|
| `themes/<thème>/theme.css` | Le thème, sans les polices |
| `themes/<thème>/manifest.json` | Manifeste Obsidian (le champ `name` donne le nom du dossier installé) |
| `build.py` | Ajoute les polices de Bear (woff2 en base64) et installe les thèmes |
| `dist/` | Thèmes construits (non versionné) |

Pour ajouter un thème : créer `themes/<nouveau>/` avec `theme.css` et `manifest.json` ; les polices sont ajoutées automatiquement (familles `Olive Bear Sans`, `Olive Bear Sans Heading`, `Olive Roboto Mono`).

## Olive Dunk

Sections de `themes/olive-dunk/theme.css` :

1. Palette Olive Dunk (`--od-*`, valeurs exactes de Bear)
2. Échelle de base Obsidian
3. Fonds · 4. Texte · 5. Typographie · 6. Liens · 7. Listes et tâches · 8. Tags · 9. Code · 10. Citations, séparateurs, tableaux · 11. Barre latérale
12. Ajustements fins façon Bear
13. Survols et info-bulles lisibles
14. Taille du texte de l'interface (`--od-ui-adjust`)

### Choix faits

- **Mode clair uniquement.** Olive Dunk n'existe qu'en clair dans Bear ; les mêmes couleurs s'appliquent quand Obsidian est en mode sombre. Toutes les couleurs passent par les variables `--od-*` : un mode sombre pourra être ajouté plus tard dans un bloc `.theme-dark` séparé.
- **Texte des notes identique à Bear** : 15 px, interligne 1,5, titres en échelle modulaire 1,125, couleur `#2b6451`, graisse 600 (graisse réelle de la police de titre de Bear).
- **Interface agrandie** : Bear Sans a des minuscules plus petites que la police système d'Apple ; `font-size-adjust: 0.51` agrandit l'interface (menus, barre latérale) sans toucher aux notes. `0.53` = équivalent police système.
- **Survols et info-bulles** rendus plus contrastés que les valeurs brutes de Bear, trop pâles dans Obsidian.

### Palette de référence (Bear)

| Rôle | Couleur |
|---|---|
| Fond | `#fbfaf0` |
| Fond secondaire | `#f6f6e9` |
| Barre latérale | `#e6e5de` |
| Sélection barre latérale | `#c4d6cd` |
| Texte | `#423f37` |
| Texte secondaire | `#617872` |
| Titres | `#2b6451` |
| Liens | `#28816a` |
| Accent | `#95afa3` |
| Sélection | `#b2d2c7` |
| Tags | fond `#d6e0d6`, texte `#59544a` |
| Code | fond `#f1f1e2` |
| Surlignage | fond `#fbc7c2`, texte `#300703` |
