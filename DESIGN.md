# DESIGN — Vitrail (gameday-vitrail)

> Journal de design. Versions datées, jamais écrasées. Tenu par Claude (directeur artistique), à partir de `PROMPT-DESIGN.md`.

## V2 — 2026-11-18 · Direction « Gothique » (3D, architecturale, lumière et matière)

**Statut : en attente de validation de Gaia.**

Retour de Gaia : « fais un style 3D, architectural et gothique, avec beaucoup plus de détails, et un travail minutieux des jeux de lumière et de matière ».
Planche : `G-DESIGN/planches/v2/01-gothique.html`, page Jeu, avec les cadres desktop 1440 × 900 et mobile 390 × 844 et la bande d'états. Les planches V1 restent en archive.

### Architecture
- Baie en lancette dans un mur en appareil : joints de mortier avec arête claire, cordons horizontaux au niveau des chapiteaux et de l'appui.
- Trois rouleaux d'archivolte modelés (ombre, corps, arête de lumière) séparés par des gorges profondes. Larmier terminé par deux culots en rosace.
- Colonnettes : base à trois tores, fût avec bague, chapiteau à crochets, tailloir.
- Appui en glacis avec ombre portée, plinthe, dallage en perspective vers un point de fuite.

### Matière
- Pierre : relief calculé par le navigateur (bruit et lumière diffuse venant du haut-gauche, `feDiffuseLighting`). Deux grains, un pour les parements, un plus fin pour les moulures.
- Verre : dégradé d'épaisseur (centre clair, bords sombres), stries étirées, marbrures, bulles.
- Grisaille peinte : nervures des pétales et des feuilles, losanges sur l'arc, mandorles sur les socles. Elle est visible, très pâle, sur le verre clair encore vide, si bien que le motif se lit avant toute couleur.
- Plomb en profil H (ombre portée, corps, arête claire) avec soudures métalliques aux nœuds.

### Lumière
- La nef est sombre (vignettage fort) et la baie est la seule source.
- Halo de lumière transmise autour du verre posé et rebond coloré sur les archivoltes et le mur.
- Faisceaux volumétriques du vitrail vers le sol, teintés par les pièces qu'ils traversent, avec de la poussière en suspension.
- **Le vitrail se projette sur le dallage** (miroir, cisaillé) : la projection change à chaque pièce posée. C'est un retour visuel du jeu, pas seulement un décor.
- Le faisceau de la règle II garde ses repères sur le verre.

### Interface
- Deux plaques de pierre gravées à sommet en arc brisé, cernées d'un filet doré : à gauche le titre et les règles, à droite la série, le chrono, les pièces et le bouton.
- Titre en lettres dorées (Noto Serif Display italique), chiffres romains dorés, texte gravé.
- Les pièces reposent sur une corniche et projettent sur la pierre une ombre de leur couleur.
- Bouton à l'état « prêt » en plaque dorée biseautée.
- Le compteur communautaire est gravé dans une dalle du sol, en perspective.
- Accent unique : l'or. Le rouge d'erreur sert seulement à la contrainte cassée.

### Outil
`G-DESIGN/_src/gothic.py` (scène, plaques, éclats, fleuron), branché sur `build.py`. La source est `_src/v2/01-gothique.src.html`. Le fichier généré pèse ~370 Ko, polices comprises, et ne fait aucune requête réseau.

### Points à surveiller
- Coût de rendu : les filtres de relief sont lourds. En production, il faudra une image pré-rendue de l'architecture et garder en direct seulement le verre, la projection et les faisceaux.
- Le faisceau principal passe devant les cases du bas : elles restent lisibles, à vérifier en jeu.

## V1 — 2026-11-18 · Exploration de la page principale (« Jeu »)

**Statut : en attente de validation de Gaia (étape B du process, on s'arrête ici).**

### Fait
- `G-DESIGN/REFS.md` : Gapsy Studio et Igloo Inc. ouverts et décodés.
  - Gapsy n'est pas une « scène sombre » comme le disait le brief : c'est une galerie blanche balayée de faisceaux de jour en diagonale, avec une seule couleur saturée. Principes retenus : le faisceau comme structure, un seul objet coloré, l'œuvre accrochée dans un lieu.
  - Igloo : la scène 3D plante dans le navigateur intégré, je l'ai complétée par la fiche Awwwards du site. Principes retenus : la lumière sort par les joints, la matière avant la couleur, un monde monochrome, l'info secondaire en micro-texte dans les coins.
- `G-DESIGN/PAGES.md` : 4 pages proposées (Post, Jeu, Carte de fin, Séries & classement). Hypothèse de jeu posée pour dessiner (cases fixes, 2 pièces par verre, 3 contraintes de lumière à solution unique), plus 4 questions produit ouvertes.
- 3 planches de la page **Jeu**. Chacune montre le cadre desktop 1440 × 900 (post déplié sur un feed neutre) et le cadre mobile 390 × 844 côte à côte, avec une bande d'états des composants (vitrail vide, erreur, juste ; pièce posable, en main, épuisée ; contrainte qui tient, en cours, cassée ; bouton en attente, prêt, appuyé, refus) :
  - `G-DESIGN/planches/v1/01-nef.html` : direction de départ poussée au bout. Charbon et plomb, faisceau de jour en diagonale, flaques de couleur au sol. Titres en Noto Serif Display, interface en Inter. Accent unique : or pâle de la lumière.
  - `G-DESIGN/planches/v1/02-atelier.html` : **s'écarte du brief**. L'atelier du verrier en plein jour. Carton au crayon sur table lumineuse ; le plomb n'apparaît que sous les pièces posées. Fraunces + Space Grotesk. Accent unique : l'encre graphite.
  - `G-DESIGN/planches/v1/03-nocturne.html` : le vitrail vu du dehors, la nuit. Monde ardoise et givre, les joints brillent quand le verre est posé, la couleur coule sur le sol. Archivo condensée très grasse + JetBrains Mono rangée dans les coins. Accent unique : la lumière chaude des joints.
- Outil : `G-DESIGN/_src/build.py` génère les planches à partir de `_src/*.src.html`. Le vitrail (géométrie, solution, faisceau), les pièces et l'habillage du feed sont définis une seule fois. Les polices (OFL, dans `_src/fonts/`) sont embarquées en base64 : chaque planche s'ouvre en double-clic, sans réseau.

### Données de démo communes
Window Nº 23, mardi 18 novembre, motif *The Lily*. 8 cases : arc, pétale gauche, pétale droit, bouton, feuille gauche, feuille droite, socle gauche, socle droit. Verres : ruby, cobalt, emerald, amber, 2 de chaque.
Contraintes : (I) même verre jamais sur un même plomb ; (II) le faisceau rencontre cobalt, puis emerald, puis ruby, puis amber ; (III) ruby couronne l'arc.
État figé : 5 pièces posées sur 8, emerald en main au-dessus du pétale droit, faisceau 3 / 4, chrono 01:12, série 6, 2,841 vitraux allumés aujourd'hui, temps médian 2:47.

### Écarts au brief, assumés
- Palette « 4 teintes de verre » respectée. Les hex des verres changent d'une direction à l'autre, pour tenir sur fond sombre ou clair.
- La direction 02 abandonne le charbon et la serif à fort contraste (Fraunces est une serif douce). C'est la direction « qui s'écarte » demandée au §5.
- Une couleur d'erreur (rouge) existe en plus de l'accent. Elle ne sert qu'à l'état « contrainte cassée ».
