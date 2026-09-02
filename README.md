# Atlas des marchés européens

Carte interactive de l'électricité et du gaz en Europe, construite **uniquement sur des
données ouvertes**. Survol : la valeur du jour. Clic : zone de dépôt, hub gaz, pages
officielles du gestionnaire de réseau et spécificités locales de cotation.

Deux groupes, cinq indicateurs, tous issus de données ouvertes :

| Groupe | Indicateur | Unité | Source |
|---|---|---|---|
| Électricité | Prix day-ahead J-1 | €/MWh | ENTSO-E, documentType A44 |
| Électricité | Consommation J-1 | GWh | ENTSO-E, documentType A65 |
| Gaz | Remplissage des stockages | % | GIE AGSI+ |
| Gaz | Soutirage net J-1 | GWh | GIE AGSI+ (échelle divergente) |
| Gaz | Remplissage terminaux GNL | % | GIE ALSI |

Le sélecteur est à deux niveaux : on choisit d'abord l'énergie, puis l'indicateur qui
colore la carte. Le panneau de droite affiche **tous** les indicateurs disponibles pour
le pays, quelle que soit la couche active — celui qui colore la carte est mis en avant.

## Deux vues

Un sélecteur **Carte / Actualité** en haut à droite.

**Carte** — la carte occupe la largeur, un panneau compact à droite donne la valeur du
jour, les cinq indicateurs et les références. Sous la carte, une bande pleine largeur en
trois colonnes : spécificités locales, liens utiles, actualité du pays. Le détail se
déploie horizontalement plutôt qu'en une longue colonne.

**Actualité** — le fil complet, filtrable par thème (monétaire, réseau, presse) et par
pays. Chaque titre porte son thème, son pays le cas échéant, sa source et son âge.

**Règle de droit respectée sans exception : titre, source, horodatage et lien vers
l'article original. Jamais le corps du texte, jamais un extrait long.** C'est l'usage
pour lequel les éditeurs publient des flux RSS.

Sources :

- flux RSS/Atom curés, déclarés dans `src/feeds.py` — institutions européennes,
  gestionnaires de réseau, régulateurs, banques centrales pour la politique monétaire
- GDELT DOC 2.0 (gratuit, sans clé) en socle par pays et pour le fil monde, ce qui
  garantit que la page n'est jamais vide même si des flux RSS tombent

Aucun abonnement payant n'est nécessaire. Les API de presse commerciales ne donnent
généralement accès qu'au titre et à un résumé court, avec des conditions d'affichage
strictes : elles achètent du volume, pas des droits supplémentaires.

### Valider les flux

Les URL de `src/feeds.py` n'ont pas pu être testées depuis l'environnement de
développement. Avant le premier vrai run :

```bash
python3 fetch_news.py --check
```

Le rapport indique, flux par flux, ceux qui répondent et ceux à corriger ou retirer.
Passe leur champ `verified` à `True` au fur et à mesure.

### Fil de démonstration

Tant que `data/news.json` n'est pas alimenté — ou si la page est ouverte en `file://`,
où le navigateur interdit la lecture des fichiers voisins — la page affiche un petit fil
d'exemple intégré au HTML, signalé par un point rouge et la mention « fil de
démonstration ». Il disparaît dès le premier run de `fetch_news.py`.

Aucun prix sous licence commerciale n'est collecté ni redistribué. Les prix de settlement
restent accessibles via les liens vers les pages officielles, dans le panneau de droite.

## Langues

Bascule FR / EN en haut à droite. La langue est mémorisée dans l'URL, donc partageable :

- `…/index.html#fr`
- `…/index.html#en`

Sans ancre, la page suit la langue du navigateur et retombe sur le français.

Tout le texte traduisible vit à deux endroits :

- l'interface, dans l'objet `T` en haut de `src/t_js.html` — deux blocs `fr` et `en`
- le contenu pays, dans `src/countries_*.py` : `name`, les notes de liens et `notes`
  portent chacun une clé `fr` et une clé `en`, côte à côte pour éviter les désynchronisations

---

## Mise en route

### 1. Token ENTSO-E

1. Créer un compte sur <https://transparency.entsoe.eu/>
2. Envoyer un mail à **transparency@entsoe.eu**, objet **« RESTful API access »**,
   avec l'adresse du compte dans le corps du message
3. Compter environ 3 jours ouvrés
4. Une fois validé : *My Account* → générer le token (un seul actif à la fois)

### 2. Clé GIE (optionnelle, pour la couche gaz)

Créer un compte sur <https://agsi.gie.eu/account> et récupérer la clé API.
La même clé donne accès à AGSI+ (stockages) et à ALSI (terminaux GNL).

### 3. Secrets du dépôt

Dans GitHub : *Settings → Secrets and variables → Actions → New repository secret*

- `ENTSOE_TOKEN`
- `GIE_KEY`  *(l'ancien nom `AGSI_KEY` reste accepté)*

### 4. Publication

*Settings → Pages → Source : Deploy from a branch → main / (root)*

La page sera servie à `https://<compte>.github.io/<dépôt>/`.

### 5. Première exécution

*Actions → Mise à jour quotidienne des données → Run workflow*, puis
*Mise à jour du fil d'actualité → Run workflow*.

Ensuite tout tourne seul : les données de marché à 07:15 UTC chaque jour, le fil
d'actualité toutes les 4 heures. Chaque job écrit son fichier dans `data/`,
reconstruit `index.html` si nécessaire, et ne commit que s'il y a du changement.

Tant que `data/prices.json` est vide, la page bascule automatiquement sur des valeurs de
démonstration, signalées par un point rouge et la mention « valeur fictive ».

---

## En local

```bash
python3 build.py                 # régénère index.html
python3 -m http.server 8000      # puis ouvrir http://localhost:8000
```

Ouvrir `index.html` directement en `file://` fonctionne aussi, mais le navigateur
bloquera la lecture de `data/prices.json` : la page restera en mode démonstration.

Pour tester la récupération sans attendre l'Action :

```bash
export ENTSOE_TOKEN=...
export GIE_KEY=...
python3 fetch_data.py
```

---

## Structure

```
build.py              assemble index.html
fetch_data.py         appelle ENTSO-E + GIE, écrit data/prices.json
fetch_news.py         agrège les flux RSS + GDELT, écrit data/news.json
src/feeds.py          liste des sources d'actualité et mots-clés de tagging
src/countries_a.py    métadonnées pays — Europe de l'Ouest
src/countries_b.py    métadonnées pays — Ibérie, Italie, Europe centrale et du Sud-Est
src/countries_c.py    métadonnées pays — Nordiques, Baltes, Balkans
src/p1..p7.html       feuilles de style
src/t_body.html       structure de la page
src/t_js*.html        logique carte et panneau
data/paths.json       géométrie SVG (Natural Earth, projection conique conforme)
data/prices.json      données du jour, écrites par fetch_data.py
data/news.json        titres du fil, écrits par fetch_news.py
```

---

## À corriger

Les zones de dépôt, codes EIC, hubs et **spécificités locales** ont été rédigés à partir
de connaissances générales. Ils sont perfectibles et c'est là que ton expertise fait la
différence : tout est dans `src/countries_*.py`, un dictionnaire Python lisible.

Points à vérifier en priorité :

- les codes EIC des zones de dépôt (une erreur donne une série vide, visible dans les
  logs de l'Action)
- les pays multi-zones — Italie, Norvège, Suède, Danemark — où une seule zone est
  représentée : `IT-Nord`, `NO2`, `SE3`, `DK1`
- l'appariement bourse spot / hub gaz pour l'Europe du Sud-Est
- les notes de spécificités, qui sont le vrai contenu de valeur de la carte

## Suites possibles

- couche flux physiques gaz depuis la plateforme de transparence ENTSOG
- part renouvelable de la production, via ENTSO-E documentType A75
- couche prix d'équilibrage gaz publiés par les GRT au titre du règlement 312/2014
- historique : chaque commit archive une journée, de quoi construire des séries longues
  sans dépendre de la profondeur d'historique des API
