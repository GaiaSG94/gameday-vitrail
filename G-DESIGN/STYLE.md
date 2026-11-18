# STYLE — Vitrail (V2 « Gothique », validé le 2026-11-18)

> Système visuel de Vitrail. La référence est la page Jeu validée : `G-DESIGN/planches/v2/01-gothique.html`.
> Les sources sont uniques : la CSS dans `G-DESIGN/_src/v2/gothic.css`, la scène dans `G-DESIGN/_src/gothic.py`, la géométrie et la solution du vitrail dans `G-DESIGN/_src/build.py`. On corrige le style à un seul endroit, puis `python3 G-DESIGN/_src/build.py`.

## Principe

Une nef sombre, une baie gothique, un seul vrai éclairage : le soleil qui traverse le vitrail. La couleur est la récompense. Tant qu'une pièce n'est pas posée, le verre est clair et le motif n'est qu'une grisaille pâle. L'interface est gravée dans la pierre, et l'or est son unique accent.

## Palette

| Rôle | Valeur | Usage |
|---|---|---|
| Nef | `#0d0c0a` | Fond de scène, tout autour de la baie |
| Pierre (parement) | `#47423a` + relief calculé | Mur en appareil |
| Pierre (sol) | `#3a362f` + relief calculé | Dallage en perspective |
| Pierre (moulure) | `#77705f` + grain fin | Archivoltes, larmier, colonnettes, appui, corniche |
| Plaque | `#3a352d` + relief, dégradé vers le noir 45 % | Fonds des panneaux d'interface |
| Plomb | `#1d1f24`, arête `#4f555f`, soudures en dégradé métal | Lignes du vitrail |
| Or (accent unique) | `#d8b26a` · clair `#f2d593` · sombre `#9c7330` | Titres dorés, chiffres romains, filets, bouton prêt, sélection, « holding » |
| Soleil | `#ffe9bf` | Faisceaux, poussière, repères de la règle de lumière (jamais dans l'UI texte) |
| Parchemin | `#ebe1cd` | Texte courant |
| Gravé | `#cfc4ae` + ombre gravée | Texte posé sur la pierre |
| Atténué | `#a39780` / `#6f6555` | Texte secondaire / désactivé |
| Erreur | `#ff5a4e` | Seulement une contrainte cassée et le plomb fautif |
| Verres | ruby `#a3112b` · cobalt `#1b42b8` · emerald `#0b7d55` · amber `#dc8c0c` | Seules couleurs saturées de l'écran. Toujours avec leur nom ou un losange |

Le verre est rendu par un dégradé radial (centre éclairci de 55 % vers `#fff6dc`, bords assombris de 42 %). Les verres ne servent jamais de couleur d'interface.

## Typographie

| Niveau | Style |
|---|---|
| Titre doré | Noto Serif Display italique, 36–60 px, dégradé or, ombre gravée (`.gild`) |
| Chiffre héros | Noto Serif Display, 40–76 px, chiffres alignés, dorés |
| Chiffre secondaire | Noto Serif Display, 22–30 px, gravé (`.eng`) |
| Petites capitales | Inter 600, 9,5–10,5 px, interlettrage 0,16–0,2 em, or (`.sc`) |
| Texte | Inter 400, 12–13,5 px, interligne 1,42, gravé |
| Chiffres romains des règles | Noto Serif Display, 15–19 px, or |
| Bouton | Noto Serif Display 500, capitales, 13–15 px, interlettrage 0,1–0,12 em |
| Inscription au sol | Noto Serif Display, capitales, 19 px, interlettrage 0,32 em, perspective `rotateX(58°)` |

Les polices sont OFL et embarquées, et doivent l'être aussi en production (CSP Devvit, aucune requête externe).

## Grille

- **Vue étendue desktop (1040 × 768)** : trois travées. Plaque gauche 262 px (identité du jour, règles ou résultat), baie au centre (vitrail de 232 px de large, colonnettes à ±108 unités du vitrail), plaque droite 262 px (chiffres, pièces, action). Marges de 30 px, haut des plaques à 34 px, sol à 568 px.
- **Vue inline (Post) desktop** : 720 × 420. Baie de 130 px au centre, texte doré sur la nef de part et d'autre, un seul bouton.
- **Mobile 390 × 844 (752 utiles)** : une colonne. En-tête de 60 px, scène de ~400 px (vitrail de 142 px), puis les plaques rectangulaires empilées. Tout tient sans défiler.
- Les plaques ont un sommet en arc brisé sur desktop et sont rectangulaires sur mobile. Filet doré à 9 px du bord.

## Composants

| Composant | Règle |
|---|---|
| Baie (`GOTH`) | Trois rouleaux d'archivolte, larmier à rosaces, colonnettes, appui en glacis, mur en appareil, dallage. La pierre est éclairée du haut-gauche |
| Vitrail | 8 cases sous plomb en H avec soudures. Verre posé : épaisseur, stries, bulles, grisaille brune. Verre clair : sombre, grisaille à 10 % |
| Projection au sol | Miroir du vitrail cisaillé vers la droite, flouté. Change à chaque pièce posée |
| Faisceaux | Partent du bas de la baie vers le sol, teintés par les pièces, avec de la poussière en suspension |
| Plaque (`GTAB`) | Pierre en relief, biseau clair en haut à gauche et sombre en bas à droite, filet doré gravé, ombre portée |
| Règle de lumière | Chiffre romain doré, texte gravé, statut en petites capitales avec losange |
| Corniche + éclat (`GCHIP`) | Les pièces posées sur une corniche de pierre, avec leur ombre colorée |
| Bouton | Attente : gravé, filet or 28 %. Prêt : plaque dorée biseautée. Appuyé : enfoncé de 2 px. Refus : filet rouge |
| Fleuron | Quadrilobe doré entre deux filets. Sépare les sections d'une plaque |
| Classement (`.lb`) | Lignes gravées, rang en serif, ma ligne surlignée d'or avec un trait à gauche |
| Mini-lancette (`MINI`) | Un vitrail par jour dans le calendrier : allumé, aujourd'hui (anneau or), manqué (verre clair), à venir (niche en pointillés) |

## Mouvement

- **Poser une pièce** : l'éclat monte de 6 px en main (150 ms). Une fois posé, le verre passe de clair à coloré en 400 ms (`ease-out`). Au même moment, sa tache apparaît sur le sol et son halo sur la pierre.
- **Case visée** : pointillés or qui défilent (1,4 s, en boucle).
- **Faisceau** : poussière qui dérive lentement (20–40 s par particule), rien d'autre ne bouge au repos.
- **Let the light in, juste** : le soleil monte en 1,2 s, puis le vitrail s'embrase et la projection se sature. La carte de fin entre par un fondu de 600 ms.
- **Refus** : le plomb fautif pulse deux fois en rouge (2 × 250 ms) et la règle cassée passe en rouge. Pas de secousse d'écran.
- Avec `prefers-reduced-motion` : pas de poussière, transitions de 0 à 150 ms.

## États

| Élément | États |
|---|---|
| Case | vide (verre clair) · visée (pointillés or) · posée · fautive (plomb rouge) |
| Pièce | posable · en main (cadre or, levée) · épuisée (contour pointillé) |
| Règle | en cours (losange vide, « 3 of 4 ») · tient (losange or) · cassée (losange rouge) |
| Bouton | attente (« · 3 » pièces restantes) · prêt · appuyé · refus |
| Jour (calendrier) | allumé · aujourd'hui · manqué · à venir |
| Post | à jouer · en cours (reprise) · déjà allumé |

## Interdits propres au style

- Pas de deuxième couleur d'accent. Le soleil `#ffe9bf` n'est pas de l'UI.
- Pas de verre coloré hors du vitrail, des éclats, des losanges de légende et des mini-lancettes.
- Pas de texte posé directement sur le verre.
- Pas de motif « Reddit » : ni mascotte, ni karma, ni orange.
