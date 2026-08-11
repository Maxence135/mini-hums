# E02 — Caractérisation de la fuite spectrale et effet du fenêtrage

**Date** : 11 août 2026
**Opérateur** : Maxence
**Phase du projet** : 1 — préparation, avant réception du matériel

---

## 1. Objectif

Quantifier la fuite spectrale introduite par la FFT lorsque la fréquence du signal ne coïncide pas avec un point de la grille d'analyse, et mesurer la réduction apportée par un fenêtrage de Hann.

**Hypothèse testée** : pour un signal sinusoïdal pur dont la fréquence tombe entre deux raies de la grille, l'application d'une fenêtre de Hann réduit d'au moins deux ordres de grandeur l'énergie apparente aux fréquences éloignées du pic, sans déplacer celui-ci.

**Motivation** : l'essai E01 utilisait une fréquence coïncidant exactement avec la grille (25,0 Hz pour une résolution de 3,125 Hz), configuration qui masque le phénomène. Le fenêtrage y était appliqué mais son effet n'était pas observable.

## 2. Moyens

| Élément | Valeur |
|---|---|
| Environnement | Python 3.x, numpy, matplotlib |
| Script | `analyse/01_signal_simule.py` (bloc 3) |
| Commit | *(à compléter)* |
| Matériel | Aucun — simulation numérique |

## 3. Conditions

| Paramètre | Valeur |
|---|---|
| Fréquence d'échantillonnage Fs | 3200 Hz |
| Durée | 1,0 s |
| Nombre d'échantillons N | 3200 |
| Résolution fréquentielle (Fs/N) | 3,125 Hz |
| Signal | sinusoïde pure, sans bruit ni harmonique |
| Fréquence du signal | 25,4 Hz (grille voisine : 25,000 et 28,125 Hz) |
| Amplitude injectée | 0,30 g |
| Traitements comparés | FFT brute / FFT avec fenêtre de Hann |
| Échelle d'affichage | logarithmique en ordonnée |

Le signal a été volontairement réduit à une seule composante afin d'isoler le phénomène : la présence de bruit ou d'harmoniques n'aurait pas permis de distinguer la fuite du contenu réel du signal.

## 4. Résultats

| Grandeur | Sans fenêtrage | Avec fenêtre de Hann |
|---|---|---|
| Position du pic | ≈ 25,4 Hz | ≈ 25,4 Hz |
| Amplitude au sommet | ≈ 0,29 g | ≈ 0,29 g |
| Niveau à 20 Hz (−5 Hz du pic) | ≈ 2×10⁻² g | ≈ 5×10⁻³ g |
| Niveau à 40 Hz (+15 Hz du pic) | ≈ 7×10⁻³ g | ≈ 3×10⁻⁵ g |
| Niveau à 60 Hz (+35 Hz du pic) | ≈ 5×10⁻³ g | ≈ 2×10⁻⁶ g |
| Largeur du pic à sa base | plus étroite | légèrement plus large |

Sans fenêtrage, le spectre présente une structure en jupe qui ne redescend pas en dessous de 10⁻³ g sur toute la bande observée (0–60 Hz), alors que le signal ne contient qu'une seule composante. Avec fenêtrage, les flancs décroissent rapidement et atteignent 10⁻⁶ g à 35 Hz du pic.

Figure : `docs/figures/E02_fenetrage.png`

## 5. Analyse

**Origine du phénomène.** La FFT traite le segment analysé comme s'il se répétait périodiquement à l'infini. Lorsque la fréquence du signal n'est pas un multiple entier de la résolution, la fin du segment ne raccorde pas avec son début ; cette discontinuité artificielle est interprétée comme une transition brutale, dont le contenu fréquentiel s'étale sur l'ensemble du spectre. L'énergie observée loin du pic n'existe donc pas dans le signal : c'est un artefact de la méthode d'analyse.

**Gain apporté par le fenêtrage.** La fenêtre de Hann annule progressivement le signal à ses deux extrémités, supprimant la discontinuité. Le gain en dynamique atteint un facteur d'environ 200 à 15 Hz du pic, et dépasse 10³ à 35 Hz.

**Coût associé.** Le pic fenêtré est légèrement plus large à sa base : la résolution, c'est-à-dire la capacité à séparer deux composantes de fréquences voisines, est dégradée. En revanche l'exactitude n'est pas affectée — la position et l'amplitude du pic sont inchangées.

**Portée pour le projet.** Le compromis est nettement favorable dans le cadre d'une surveillance vibratoire. Les composantes à distinguer (1×, 2×, 3×) sont espacées de la fréquence de rotation, soit plusieurs dizaines de hertz, ce qui rend la perte de résolution sans conséquence. En revanche, un défaut naissant présente une amplitude de deux à trois ordres de grandeur inférieure à celle du pic principal : sans fenêtrage, la jupe du fondamental (≈ 10⁻² g pour un pic à 0,3 g) le masquerait entièrement. Le fenêtrage conditionne donc directement la capacité de détection précoce, qui est l'objet du système.

**Erreur d'amplitude résiduelle.** L'amplitude lue au sommet (≈ 0,29 g) est légèrement inférieure à celle injectée (0,30 g). La fréquence tombant entre deux raies, son énergie se répartit sur les raies voisines et aucune ne reçoit la totalité. Ce phénomène, dit de *scalloping*, atteint jusqu'à −1,4 dB dans le cas le plus défavorable avec une fenêtre de Hann.

## 6. Limites

- Une seule fenêtre a été évaluée. D'autres profils (Hamming, Blackman, flat-top) offrent des compromis différents entre dynamique, largeur de lobe et exactitude d'amplitude ; leur comparaison n'a pas été menée.
- Le signal est parfaitement stationnaire. Sur une machine réelle, les variations de vitesse pendant l'acquisition élargissent les pics par un mécanisme distinct de la fuite spectrale, non traité ici.
- Les niveaux relevés dans la section 4 sont des lectures graphiques, non des mesures extraites numériquement.
- L'erreur de scalloping n'a pas été mesurée systématiquement en fonction de l'écart à la grille.

## 7. Conclusion

Hypothèse validée : le fenêtrage de Hann réduit la fuite spectrale de plus de deux ordres de grandeur sans déplacer le pic. Il est retenu comme traitement systématique avant toute FFT dans la suite du projet.

Conséquence pour l'extraction des indicateurs : l'amplitude d'une composante ne sera pas lue au sommet de son pic mais obtenue par sommation de l'énergie sur une bande étroite autour de la fréquence visée, afin de s'affranchir de l'erreur de scalloping.

**Prochaine étape** : caractérisation des indicateurs scalaires (RMS, facteur de crête, kurtosis) et de leur sensibilité respective aux différents types de défaut (E03).
