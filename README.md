# 42 Trainer (bêta)

Appli d'entraînement **locale** pour l'école 42 : une mini-moulinette (norminette + compilation
+ tests) avec XP, niveaux, série quotidienne, défi du jour, succès et **mode examen**.
Contenu actuel : la **libft** selon le sujet **v19.3** (43 exercices : partie 1 libc, partie 2 fonctions en plus,
partie 3 **listes chaînées**, désormais obligatoire : il n'y a plus de bonus), **18 cours** avec quiz,
un mode **enchaînement** et un mode **examen**.

## Lancer
Double-clique sur **`Lancer 42 Trainer.bat`**. Une fenêtre noire s'ouvre (le serveur) et ton
navigateur affiche l'appli sur `http://localhost:4242`. Ferme la fenêtre noire pour arrêter.
Un deuxième double-clic ne fait rien de mal : il rouvre simplement la page.

Prérequis (déjà installés sur ce PC) : Python 3, gcc (WinLibs), norminette (`pip install norminette`).
Si `gcc` ou `norminette` sont introuvables, la page **Réglages** le dit.

## Comment ça marche
1. Tu choisis un exercice, tu écris `ft_xxx.c` dans l'éditeur (l'en-tête 42 est ajouté tout seul).
2. **Rendre** : le serveur lance dans l'ordre
   - la détection de fonctions interdites,
   - `norminette` (en parallèle),
   - `gcc -Wall -Wextra -Werror`,
   - des tests C (comparés à la libc ou à des valeurs de référence), avec détection de crash, de
     boucle infinie et de **fuites mémoire** (le `malloc` est surveillé, y compris quand il échoue).
3. Un exercice est **validé** seulement si tout est OK (norme comprise, comme à l'école).

## Cours, enchaînement
- **📚 Cours** : 18 cours dans un **parcours ordonné** (niveau + durée) : compiler/Makefile, mémoire (pile/tas), ASCII, chaînes, const/size_t, pointeurs, chercher/comparer, memmove, strlcpy/strlcat, malloc, atoi/itoa, ft_split, récursivité, write, pointeurs de fonction, **listes chaînées**, norme, déboguer. Chaque cours : explications pas à pas, **pièges classiques**, mini-exercices avec correction repliée, « à retenir », **visualiseurs interactifs** quand ils aident, et un quiz de 5 questions corrigé par le serveur (+15 XP au premier sans-faute). Le contenu est dans `catalog/lessons.py` (base) et `catalog/lessons_more.py` (approfondissements, nouveaux cours, ordre). Pas de vraies vidéos (je ne peux pas en produire) : ces animations interactives les remplacent.
- **🔬 Fonction par fonction** (catégorie à part) : un cours pour **chacune des 43 fonctions** de la libft : rôle, code complet numéroté, **explication ligne par ligne**, cas limites, exemple déroulé à la main, pièges. Chaque cours montre une solution complète (celle de `runtime/ref`) : essaie l'exercice avant de lire. Le contenu est dans `catalog/func_courses.py` ; `tools/e2e.py` vérifie que chaque ligne de code est expliquée.
- **⚡ Enchaînement** : un exercice **de la partie 1** au hasard ; dès qu'il est validé, un autre arrive. 2 passes par série, bonus de combo à la fin (10/30/60/100/150 XP).

## XP et niveaux
- XP de base : 20 / 35 / 55 / 80 selon le niveau de l'exercice (★ à ★★★★).
- Bonus : du premier coup +20 %, sans indice +20 %, série de jours (+5 %/jour, max +30 %), défi du jour +50 %.
- Chaque indice utilisé : −20 % (jamais en dessous de 40 %).
- Refaire un exercice déjà validé : petite XP de **révision** (10 %, 5 par jour max) qui compte aussi pour la série.
- Niveau N atteint à `50·N·(N−1)` XP (100, 300, 600, 1000…). Titres : Cadet → Légende 42.
- **Examen** : 2 h, 4 niveaux (un exercice à la fois, tiré au hasard), norme non vérifiée, pas d'indices,
  pénalité d'attente après 3 échecs. 25 XP par niveau, +100 si les 4 sont réussis ; seuls les 3 premiers examens du jour rapportent de l'XP.

## Fichiers
```
server.py        serveur local (127.0.0.1 uniquement)
engine.py        la moulinette (norminette, gcc, tests, limites de temps/sortie)
game.py          XP, niveaux, série, succès, examen
catalog/         les exercices (libft_p1.py, libft_p2.py, libft_p3.py) : ajoute-en en copiant une fiche
runtime/         harnais de test C + solutions de référence (runtime/ref)
tools/selftest.py  vérifie que les solutions de référence passent ET que 55 solutions fausses sont refusées
web/             l'interface (HTML/CSS/JS, aucune dépendance)
data/            TA progression (progress.json), tes idées (ideas.json), réglages (config.json)
```
Vérifier que tout fonctionne : `python tools/selftest.py` (~5 min) et `python tools/e2e.py` (API, examen, pénalités, sans toucher à ta progression).

## Ajouter un exercice
Dans `catalog/libft_p2.py` (ou `libft_p3.py` pour les listes), copie une fiche `add(ex(...))` : prototype, résumé, exemples, tests C
(`void run(void)` avec `CHECK("description", condition)`), fonctions autorisées, indices.
Mets une solution de référence dans `runtime/ref/` et relance `tools/selftest.py`.

## Honnêteté : limites de la bêta
- **Ce n'est pas la vraie moulinette.** Les tests sont écrits ici ; celle de l'école peut être plus
  stricte ou différente. Valide aussi avec le sujet de ton projet et un testeur public.
- Pas de `valgrind` sous Windows : les fuites sont détectées via un `malloc` surveillé (couvre les
  fuites classiques, pas les accès mémoire invalides).
- Windows ≠ Linux : `long` fait 32 bits ici (les tests le prennent en compte) ; certains détails
  de la libc diffèrent. Les cas flous (ex. `NULL` en entrée) ne sont **pas** testés exprès.
- Seule la libft est dans le catalogue pour l'instant. **Absent** : `get_next_line`, `ft_printf`,
  Born2beroot, exercices d'exam « Rank 02 »… Le sujet utilisé est la libft v19.3 (listes obligatoires,
  `is*` qui renvoient exactement 1/0, `ft_calloc(0, x)` non NULL, `ft_lstsize` en `unsigned int`).
  Les solutions de référence des `ft_lst*` ne servent qu'à faire fonctionner les tests (elles ne sont pas dans ton dépôt).
- L'éditeur est simple (pas de coloration syntaxique, pas d'autocomplétion).

## Idées pour la suite
Utilise la page **💡 Idées / retours** de l'appli : tout est écrit dans `data/ideas.json`.
Pistes déjà notées : exercices d'examen type Rank 02/03, mode révision
(refaire les exercices ratés), statistiques par fonction, coloration syntaxique, `get_next_line`.
