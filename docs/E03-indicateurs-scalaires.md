# E03 — Sensibilité des indicateurs scalaires aux types de défaut

**Date** : 11 août 2026
**Phase du projet** : 1 — préparation, avant réception du matériel

---

## 1. Objectif

Déterminer la sensibilité respective des indicateurs scalaires usuels (RMS, valeur crête, facteur de crête, kurtosis, skewness) à deux familles de défauts mécaniques distinctes : une aggravation du balourd et l'apparition de chocs répétitifs de type écaillage de roulement.

**Hypothèse testée** : aucun indicateur scalaire pris isolément ne permet de détecter les deux familles de défauts. Les indicateurs d'énergie répondent au balourd, les indicateurs de forme répondent aux chocs, et la réciproque est fausse dans les deux cas.

**Motivation** : les essais E01 et E02 ont validé la chaîne d'analyse spectrale, qui produit environ 1600 valeurs par mesure. Cette représentation n'est pas exploitable pour une surveillance continue ni pour un calcul embarqué en temps réel. Il est nécessaire de réduire chaque acquisition à un petit nombre de grandeurs, sous réserve que cette réduction préserve l'information utile à la détection.

## 2. Moyens

| Élément | Valeur |
|---|---|
| Environnement | Python 3.x, numpy, scipy.stats, matplotlib |
| Script | `analyse/01_signal_simule.py` (bloc 4) |
| Commit | *(à compléter)* |
| Matériel | Aucun — simulation numérique |

## 3. Conditions

| Paramètre | Valeur |
|---|---|
| Fréquence d'échantillonnage Fs | 3200 Hz |
| Durée | 1,0 s |
| Fréquence de rotation | 25 Hz (1500 tr/min) |
| Graine du générateur aléatoire | 42 |
| Bruit | gaussien, écart-type 0,05 g |

Trois signaux ont été construits à partir d'un même tirage de bruit, afin que les écarts observés ne soient imputables qu'aux modifications volontaires.

| Cas | Composition |
|---|---|
| Sain | 0,30 g à 25 Hz + 0,10 g à 50 Hz + bruit |
| Balourd | 0,90 g à 25 Hz + 0,10 g à 50 Hz + bruit |
| Chocs | signal sain + impulsions amorties, 89 par seconde |

Les impulsions du cas « Chocs » sont modélisées par une oscillation à 1200 Hz (résonance de structure) sous enveloppe exponentielle décroissante de constante de temps 2 ms, d'amplitude initiale 0,5 g. La fréquence de répétition de 89 Hz n'est pas un multiple entier de la fréquence de rotation, conformément à la signature d'un défaut de piste de roulement.

Le cas « Balourd » ne diffère du cas sain que par l'amplitude de la composante 1×, toutes les autres grandeurs étant maintenues identiques.

## 4. Résultats

| Indicateur | Sain | Balourd | Chocs | Écart balourd | Écart chocs |
|---|---|---|---|---|---|
| RMS (g) | 0,229 | 0,642 | 0,252 | **+180 %** | +10 % |
| Crête (g) | 0,480 | 1,071 | 0,836 | +123 % | +74 % |
| Facteur de crête | 2,096 | 1,668 | 3,316 | **−20 %** | **+58 %** |
| Kurtosis | −1,128 | −1,448 | −0,645 | −28 % | **+43 %** |
| Skewness | −0,024 | −0,005 | 0,042 | — | — |

Figure : `docs/figures/E03_indicateurs.png` (représentation temporelle des trois signaux, fenêtre 0–0,2 s)

L'inspection visuelle de la figure montre que le cas « Balourd » conserve la forme et la période du cas sain avec une amplitude accrue, tandis que le cas « Chocs » présente une amplitude comparable au cas sain assortie de transitoires brefs et régulièrement espacés.

## 5. Analyse

**Comportement du RMS.** L'augmentation de 180 % sur le balourd correspond au triplement de l'amplitude de la composante dominante. Sur le cas à chocs, l'augmentation de 10 % s'explique par la faible énergie des impulsions : brèves et peu nombreuses, elles ne contribuent que marginalement à la moyenne quadratique. Un écart de cet ordre est du même niveau que les variations attendues sur une machine réelle sous l'effet de la charge ou de la température, et ne constitue donc pas un critère de détection exploitable.

**Comportement du facteur de crête.** La diminution observée sur le balourd mérite attention car elle est contre-intuitive. L'amplification de la composante sinusoïdale fait croître simultanément la valeur crête et le RMS, de sorte que leur rapport converge vers celui d'une sinusoïde pure (√2 ≈ 1,41). Un balourd aggravé rend donc le signal plus régulier, et non plus impulsif. Sur le cas à chocs, l'augmentation de 58 % traduit directement la présence de valeurs extrêmes sans augmentation correspondante de l'énergie.

**Comportement du kurtosis.** Les trois valeurs sont négatives : le kurtosis d'une sinusoïde pure vaut −1,5, valeur minimale de l'indicateur, et cette composante domine dans les trois signaux. Seule la variation est interprétable. Le balourd déplace l'indicateur vers −1,45, c'est-à-dire vers un caractère plus purement sinusoïdal. Les chocs le déplacent en sens inverse, vers −0,645. Le kurtosis élevant les écarts à la puissance quatre avant moyennage, une valeur trois fois supérieure à la normale pèse 81 fois plus dans son calcul contre 9 fois dans celui du RMS ; cette non-linéarité est ce qui confère à l'indicateur sa sensibilité aux impulsions rares.

**Skewness.** Les valeurs relevées sont proches de zéro dans les trois cas et ne présentent pas d'écart exploitable. Ce résultat était attendu : les signaux simulés sont symétriques par construction. L'indicateur est conservé dans le vecteur, son coût de calcul étant négligeable, mais aucune valeur de détection ne lui est attribuée à ce stade.

**Complémentarité.** Les résultats confirment l'hypothèse. Un système de surveillance fondé sur le seul RMS détecterait le balourd sans ambiguïté et ne verrait pas le défaut de roulement. Un système fondé sur le seul kurtosis ferait l'inverse, et signalerait de surcroît une amélioration apparente en cas d'aggravation du balourd. La détection doit donc reposer sur un vecteur d'indicateurs et non sur une grandeur unique.

**Évolution attendue en exploitation.** En maintenance conditionnelle, l'indicateur n'est pas interprété par sa valeur absolue mais par sa dérive au cours du temps, à conditions de fonctionnement comparables. Le kurtosis présente à cet égard un comportement non monotone documenté : il croît dès les premiers stades d'écaillage, puis décroît en fin de vie lorsque les chocs deviennent suffisamment nombreux et continus pour que la distribution des amplitudes redevienne quasi gaussienne. Une décroissance du kurtosis après une phase de croissance ne doit donc pas être interprétée comme un retour à la normale. Le RMS, qui croît de manière monotone avec la dégradation, prend le relais dans cette phase tardive. Cette complémentarité temporelle renforce la nécessité du suivi conjoint des deux indicateurs.

## 6. Limites

- Les défauts sont simulés selon des modèles simplifiés. L'amplitude, la constante d'amortissement et la fréquence de résonance retenues pour les chocs sont plausibles mais non calibrées sur une mesure réelle.
- Un seul niveau de gravité a été testé par type de défaut. On ne sait donc pas comment les indicateurs évoluent quand le défaut s'aggrave.
- Les signaux sont parfaitement stationnaires, sans variation de vitesse ni de température. Sur banc réel, ces facteurs introduiront une dispersion des indicateurs en l'absence de tout défaut, dispersion qu'il faudra quantifier pour fixer des seuils.
- Les deux défauts ont été testés séparément. Leur combinaison, plus représentative d'une machine dégradée, n'a pas été étudiée.
- Aucun essai de répétabilité n'a été mené : un seul tirage de bruit a été utilisé.

## 7. Conclusion

Hypothèse validée. Le RMS répond au balourd et non aux chocs ; le facteur de crête et le kurtosis répondent aux chocs et sont indifférents, voire trompeurs, sur le balourd.

Décision retenue pour la suite du projet : chaque acquisition sera réduite à un vecteur de descripteurs comprenant les indicateurs temporels caractérisés ici (RMS, valeur crête, facteur de crête, kurtosis, skewness) complétés par les amplitudes des composantes 1× et 2× extraites du spectre. Ce vecteur constituera l'entrée commune des trois niveaux de détection prévus : seuillage simple, distance de Mahalanobis, puis autoencodeur.

**Prochaine étape** : vérification de la méthode sur un essai de dégradation réel à partir d'un jeu de données public (E04).
