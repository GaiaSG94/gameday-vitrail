# PAGES — Vitrail

> Les pages se déduisent du produit (`IDEE.md`) et des 4 critères du jury. Statuts : à dessiner / en revue / validée.

| # | Page | Rôle | Contenu clé | Statut |
|---|---|---|---|---|
| 1 | **Post** | Donner envie depuis le feed, en 5 secondes | En-tête du post, vitrail du jour éteint (silhouette en plomb), motif du jour, nombre de vitraux allumés aujourd'hui, série du joueur, bouton « Start » | à dessiner |
| 2 | **Jeu** *(page principale)* | Poser les 8 pièces de verre en respectant les contraintes de lumière | Vitrail du jour (8 cases sous plomb), 8 pièces (2 par verre), 3 contraintes de lumière avec leur état, faisceau de soleil, bouton « Let the light in » | **en revue (V1, 3 directions)** |
| 3 | **Carte de fin** | Récompenser : le vitrail terminé s'allume | Vitrail allumé, résultat (temps), série, rang du jour, invitation à commenter en un geste, compte à rebours avant le prochain vitrail | à dessiner |
| 4 | **Séries & classement** | Faire revenir demain | Série en cours et record, calendrier des vitraux du mois, classement du jour, chiffres de la communauté | à dessiner |

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
- « Let the light in » vérifie : si tout est juste, le vitrail s'allume (carte de fin). Sinon, la contrainte cassée et le plomb fautif s'allument en rouge.

## Questions produit ouvertes

1. La lecture ci-dessus (cases fixes, on choisit le verre) est-elle la bonne ? L'autre lecture possible : des pièces de formes différentes à emboîter, façon puzzle.
2. Le résultat de la carte de fin est-il le **temps**, le **nombre d'essais** de « Let the light in », ou les deux ? Les planches montrent le temps et le nombre d'essais.
3. Les erreurs : nombre d'essais illimité, ou limité (par ex. 3) avec série cassée au-delà ?
4. « Scores de la communauté » : compteur de vitraux allumés du jour + temps médian, ou classement nominatif ? Les planches montrent les deux en petit.
