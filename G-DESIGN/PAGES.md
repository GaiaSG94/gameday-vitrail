# PAGES — Vitrail

> Les pages se déduisent du produit (`IDEE.md`) et des 4 critères du jury. Statuts : à dessiner / en revue / validée.

| # | Page | Rôle | Contenu clé | Statut |
|---|---|---|---|---|
| 1 | **Post** | Donner envie depuis le feed, en 5 secondes | En-tête du post, vitrail du jour éteint (silhouette en plomb), motif du jour, nombre de vitraux allumés aujourd'hui, série du joueur, bouton « Start » | en revue (V2 · `planches/v2/02-post.html`) |
| 2 | **Jeu** *(page principale)* | Poser les 8 pièces de verre en respectant les contraintes de lumière | Vitrail du jour (8 cases sous plomb), 8 pièces (2 par verre), 3 contraintes de lumière avec leur état, faisceau de soleil, bouton « Let the light in » | **validée (V2 Gothique · `planches/v2/01-gothique.html`)** |
| 3 | **Carte de fin** | Récompenser : le vitrail terminé s'allume | Vitrail allumé, résultat (temps), série, rang du jour, invitation à commenter en un geste, compte à rebours avant le prochain vitrail | en revue (V2 · `planches/v2/03-carte-de-fin.html`) |
| 4 | **Séries & classement** | Faire revenir demain | Série en cours et record, calendrier des vitraux du mois, classement du jour, chiffres de la communauté | en revue (V2 · `planches/v2/04-series-classement.html`) |

Pas d'autre page : pas de tutoriel séparé (règle lisible sur l'écran Jeu, critère « lisible en 5 secondes »), pas d'écran de réglages (non prévu dans `IDEE.md`).

## Hypothèse de jeu utilisée pour les planches (à valider)

`IDEE.md` dit seulement « 8 glass pieces, one motif, light constraints ». Pour dessiner un écran vrai, j'ai pris cette lecture. **Je ne la tranche pas : à confirmer ou corriger.**

- Le vitrail du jour est un dessin fixe en plomb, découpé en **8 cases**. Motif du jour : *The Lily* (arc, 2 pétales, bouton, 2 feuilles, 2 socles).
- Le joueur a **8 pièces de verre**, **2 par couleur** : ruby, cobalt, emerald, amber. Il les pose une par une dans les cases (toucher une pièce, toucher une case).
- **3 contraintes de lumière** par jour, tirées de la seed. Celles des planches (solution unique, vérifiée) :
  1. *No two pieces of the same glass share a lead line.*
  2. *The sunbeam meets cobalt, then emerald, then ruby, then amber.* (Le faisceau traverse 4 cases : pétale gauche, feuille gauche, feuille droite, socle droit.)
  3. *Ruby crowns the arch.*
  Solution : arc ruby · pétale gauche cobalt · pétale droit emerald · bouton amber · feuille gauche emerald · feuille droite ruby · socle gauche cobalt · socle droit amber.
- État figé des planches Jeu : 5 pièces posées sur 8 (arc, pétale gauche, bouton, 2 feuilles), emerald en main au-dessus du pétale droit, restent cobalt et amber. Chrono 01:12, série 6, 2,841 vitraux allumés aujourd'hui.
- Suite des données (étape C) : allumé en 2:31 au premier essai, rang 312 sur 2,842, série 7 (record), 14 vitraux sur 18 en novembre (manqués les 3, 6, 9 et 11), prochain vitrail dans 09:14:22. Mercredi 18 novembre 2026.
- « Let the light in » vérifie : si tout est juste, le vitrail s'allume (carte de fin). Sinon, la contrainte cassée et le plomb fautif s'allument en rouge.

## Questions produit ouvertes

1. La lecture ci-dessus (cases fixes, on choisit le verre) est-elle la bonne ? L'autre lecture possible : des pièces de formes différentes à emboîter, façon puzzle.
2. Le résultat de la carte de fin est-il le **temps**, le **nombre d'essais** de « Let the light in », ou les deux ? Les planches montrent le temps et le nombre d'essais.
3. Les erreurs : nombre d'essais illimité, ou limité (par ex. 3) avec série cassée au-delà ?
4. « Scores de la communauté » : compteur de vitraux allumés du jour + temps médian, ou classement nominatif ? Les planches montrent les deux en petit.

## Hypothèses ajoutées à l'étape C (à confirmer)

5. Le post peut avoir trois états dans le feed : à jouer, en cours (reprise), déjà allumé (compte à rebours).
6. « Comment » ouvre le champ de commentaire du post avec une ligne sans spoiler déjà écrite. Rien n'est posté automatiquement.
7. Le classement a deux onglets : plus rapides du jour, plus longues séries.
8. Le calendrier montre le mois en cours. Chaque jour allumé reprend les couleurs de la solution de ce jour-là. Sur les planches, la silhouette est la même pour tous les jours : en vrai, chaque jour aura son motif.
