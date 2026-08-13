# E04 — Suivi des indicateurs scalaires sur un essai de dégradation réel (dataset IMS)

**Date** : 13 août 2026
**Phase du projet** : 1 — préparation, avant réception du matériel

---

## 1. Objectif

Vérifier sur des données de dégradation réelles la capacité des indicateurs scalaires caractérisés en E03 à révéler l'évolution d'un défaut de roulement, et déterminer l'antériorité de la réponse du kurtosis par rapport à celle du RMS.

**Hypothèses testées** :
1. Le kurtosis franchit un critère de détection avant le RMS sur un défaut naissant de roulement.
2. Le kurtosis présente une décroissance en phase terminale, alors que le RMS continue de croître.
3. Une mesure isolée ne permet pas d'identifier un roulement en cours de dégradation ; seule l'évolution temporelle le permet.

**Motivation** : les essais E01 à E03 reposent sur des signaux simulés, construits à partir des phénomènes que l'on cherche à détecter. La validation de la méthode sur des mesures indépendantes est nécessaire avant de l'appliquer au banc du projet. Le recours à un jeu de données public permet en outre de disposer d'un historique de dégradation complet, qu'un essai mené dans le cadre du projet ne pourra pas produire.

## 2. Moyens

| Élément | Valeur |
|---|---|
| Environnement | Python 3.x, numpy, scipy.stats, matplotlib |
| Script | `analyse/02_dataset_nasa.py` (blocs 1 à 4) |
| Commit | *(à compléter)* |
| Données | IMS Bearing Data Set, essai n°2 |
| Matériel | Aucun — exploitation de données existantes |

**Source des données** : J. Lee, H. Qiu, G. Yu, J. Lin, and Rexnord Technical Services (2007). IMS, University of Cincinnati, « Bearing Data Set », NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA.

## 3. Conditions

**Banc d'essai** (d'après la documentation du jeu de données)

| Paramètre | Valeur |
|---|---|
| Configuration | 4 roulements sur un arbre unique, entraînement par courroies |
| Vitesse de rotation | 2000 tr/min, maintenue constante |
| Charge radiale | 6000 lb, appliquée par un mécanisme à ressort |
| Roulements | Rexnord ZA-2115, double rangée, 16 rouleaux par rangée |
| Diamètre primitif | 2,815 in |
| Diamètre de rouleau | 0,331 in |
| Angle de contact | 15,17° |
| Lubrification | forcée |
| Capteurs | accéléromètres PCB 353B33, un par palier |

**Acquisition**

| Paramètre | Valeur |
|---|---|
| Fréquence d'échantillonnage | 20 000 Hz |
| Points par enregistrement | 20 480 (soit 1,024 s) |
| Intervalle entre enregistrements | 10 min |
| Nombre de fichiers | 984 |
| Durée totale | 12 février 2004 10:32 au 19 février 2004 06:22, soit environ 164 h |
| Format | ASCII, 4 colonnes (une par palier) |
| Système d'acquisition | NI DAQ Card 6062E |

**Issue de l'essai** : défaillance de la bague extérieure du roulement 1. Les roulements 2, 3 et 4 ne présentent pas de défaillance déclarée à l'issue de l'essai et constituent donc une référence saine acquise dans les mêmes conditions.

**Traitement appliqué** : pour chacun des 984 fichiers et chacun des 4 canaux, calcul du RMS et du kurtosis sur le signal centré, sans fenêtrage ni filtrage préalable. Le tableau de descripteurs obtenu est de dimension 984 × 8.

**Critère de détection.** Une période de référence est définie sur les premiers enregistrements. La moyenne et l'écart-type de l'indicateur y sont calculés, et le seuil est fixé à moyenne + 3 écarts-types. La détection est déclarée au premier instant où l'indicateur dépasse ce seuil pendant *n* enregistrements consécutifs, l'exigence de persistance servant à écarter les dépassements ponctuels dus à la dispersion.

Deux paramètres ont été explorés : la longueur de la période de référence (600 enregistrements, soit 100 h ; et 500, soit 83 h) et le nombre d'enregistrements consécutifs *n* (3, 6, 12 et 24).

## 4. Résultats

### 4.1 Vérification de la structure des données

La lecture du premier fichier confirme les caractéristiques annoncées : tableau de dimension (20480, 4), durée 1,024 s. Le nombre de fichiers relevé dans le répertoire est de 984, conforme à la documentation.

Figure : `docs/figures/E04_signaux_bruts_4_roulements.png` (signaux temporels des 4 paliers, premier fichier, fenêtre 0–50 ms)

Aucune composante périodique n'est identifiable à l'œil sur les signaux bruts, malgré une fréquence de rotation de 33,3 Hz. Les quatre paliers présentent des amplitudes distinctes, comprises entre ±0,25 g (palier 4) et ±0,5 g (palier 3).

### 4.2 Indicateurs au premier enregistrement (t = 0)

| Roulement | RMS (g) | Crête (g) | Facteur de crête | Kurtosis |
|---|---|---|---|---|
| 1 | 0,073 | 0,464 | 6,318 | 0,629 |
| 2 | 0,090 | 0,500 | 5,556 | 0,507 |
| 3 | 0,108 | 1,038 | 9,568 | **3,213** |
| 4 | 0,053 | 0,254 | 4,777 | 0,066 |

Le roulement 3 présente à cet instant les valeurs les plus élevées de kurtosis et de facteur de crête, sans rapport avec l'issue de l'essai.

### 4.3 Évolution sur la durée de l'essai

Figure : `docs/figures/E04_tendances_rms_kurtosis_7j.png`

| Grandeur | Roulement 1 | Roulements 2, 3, 4 |
|---|---|---|
| RMS initial | ≈ 0,08 g | 0,05 à 0,11 g |
| RMS maximal | ≈ 0,72 g | ≈ 0,20 g |
| Rapport max/initial | ≈ 9 | ≈ 2 |
| Kurtosis initial | 0,63 | 0,07 à 3,21 |
| Kurtosis maximal | ≈ 14 | ≈ 4 |

**Chronologie observée sur le roulement 1**

| Instant approximatif | Observation |
|---|---|
| 0 – 100 h | RMS et kurtosis stables, comparables aux autres paliers |
| 100 – 115 h | Croissance du kurtosis, RMS encore stable |
| ≈ 118 h | Première augmentation du RMS |
| 125 – 145 h | Décroissance du kurtosis, RMS en croissance continue |
| 150 – 164 h | Croissance simultanée des deux indicateurs, valeurs maximales atteintes |
| ≈ 164 h | Chute brutale de tous les canaux |

**Roulement 3** : kurtosis compris entre 1 et 3 sur toute la durée de l'essai, avec une dispersion importante d'un enregistrement à l'autre, sans tendance croissante identifiable.

**Événements affectant simultanément les quatre canaux** : des discontinuités du RMS sont observées vers 118 h et vers 140 h sur l'ensemble des paliers. La chute finale à environ 164 h affecte également les quatre canaux.

### 4.4 Instants de détection sur le roulement 1

Période de référence de 600 enregistrements (100 h) :

| *n* consécutifs | RMS | Kurtosis | Écart |
|---|---|---|---|
| 3 | fichier 578 — 96,3 h | fichier 647 — 107,8 h | 11,5 h |
| 6 | fichier 578 — 96,3 h | fichier 647 — 107,8 h | 11,5 h |
| 12 | fichier 585 — 97,5 h | fichier 647 — 107,8 h | 10,3 h |
| 24 | fichier 585 — 97,5 h | fichier 670 — 111,7 h | 14,2 h |

Période de référence de 500 enregistrements (83 h), *n* = 6 :

| Indicateur | Détection | Écart |
|---|---|---|
| RMS | fichier 532 — 88,7 h | — |
| Kurtosis | fichier 647 — 107,8 h | 19,1 h |

Dans les cinq configurations, le RMS franchit le critère avant le kurtosis.

Un critère sans exigence de persistance (*n* = 1) place la détection du kurtosis au fichier 3, soit 0,5 h, et celle du RMS au fichier 571.

## 5. Analyse

**Antériorité du kurtosis : hypothèse infirmée.** Le RMS franchit le critère avant le kurtosis, dans toutes les configurations testées. L'écart est de 11,5 h avec la référence de 100 h, et de 19,1 h avec celle de 83 h. L'hypothèse 1 n'est pas vérifiée sur cet essai.

Une lecture graphique préalable avait conclu l'inverse. Elle comparait le décollage du kurtosis à la marche du RMS vers 118 h, alors que la dérive du RMS avait commencé bien avant. C'est cette erreur qui a motivé la mise en place du critère chiffré du §3.

**Pourquoi le kurtosis perd.** Le raisonnement théorique reste juste : un écaillage naissant produit des chocs brefs et peu énergétiques, que le RMS ne voit pas et que le kurtosis voit. Deux raisons peuvent expliquer qu'on ne l'observe pas ici.

D'abord, le kurtosis est beaucoup plus dispersé que le RMS — ses courbes sont visiblement plus bruitées. Or le critère fixe le seuil à trois écarts-types de la référence : plus un indicateur fluctue, plus son seuil est haut, et plus il lui faut une dérive marquée pour le franchir durablement. Le critère pénalise donc l'indicateur le plus bruité. Ce n'est pas le kurtosis qui est en cause, c'est le couple indicateur-critère.

Ensuite, le signal est utilisé brut. En analyse de roulements, on applique habituellement un filtrage passe-haut et une démodulation d'enveloppe pour isoler les chocs du reste du signal. Ces traitements avantagent le kurtosis, et ils n'ont pas été appliqués ici.

**Ce qu'il faut en retenir.** Le kurtosis reste utile : les deux autres résultats de cette fiche le montrent. Mais on ne peut pas décider à l'avance quel indicateur détectera en premier — cela dépend du critère, du prétraitement et du type de défaut. Sur le banc du projet, les deux seront donc suivis sans préférence, et comparés sur les données réelles.

**Un dépassement isolé ne veut rien dire.** Sans exigence de durée, le critère détecte le kurtosis à 0,5 h et le RMS à 95,2 h — deux instants situés dans la période supposée saine. Ce ne sont pas des dégradations, seulement des pics de bruit : sur 984 mesures, dépasser une fois trois écarts-types est normal. Exiger que le dépassement dure fait donc partie du critère, ce n'est pas un raffinement.

**Le résultat ne tient pas à un réglage.** Multiplier par huit la durée exigée (de 3 à 24 mesures) déplace la détection de 1,2 h pour le RMS et 3,9 h pour le kurtosis, soit moins de 4 % de l'essai. L'ordre entre les deux ne change jamais.

Les valeurs se figent par paliers : 578 pour n = 3 et 6, puis 585 pour n = 12 et 24. Signe que le dépassement est franchement installé à ces instants, et non marginal.

Le kurtosis bouge environ trois fois plus que le RMS quand on change le réglage — logique, puisqu'il est plus dispersé et met donc plus de temps à tenir un dépassement continu.

**La période de référence fausse le résultat.** En la raccourcissant de 100 h à 83 h, la détection du RMS avance de 7,6 h, alors que celle du kurtosis ne bouge pas. La raison : le RMS avait déjà commencé à dériver avant 100 h. L'inclure dans la référence gonflait la moyenne et l'écart-type, donc le seuil. Le kurtosis, lui, était encore stable, sa référence n'était pas polluée.

Cela révèle un problème de fond : **pour délimiter la période saine, il faudrait déjà savoir quand la dégradation commence — c'est-à-dire ce qu'on cherche à trouver.** En exploitation on s'en sort en prenant la référence à la mise en service, quand la machine est neuve. Ici, aucun repère de ce genre : le choix de 100 h était arbitraire.

Pour le banc du projet, la conséquence est simple : la référence sera enregistrée dès les premiers essais, sur un montage sain par construction, et non découpée après coup dans l'historique.

**Le kurtosis redescend en fin de vie.** Hypothèse 2 vérifiée. Entre 125 et 145 h, le kurtosis du roulement 1 baisse alors que le RMS continue de monter. Explication : la zone écaillée s'étend, les chocs deviennent trop nombreux et trop rapprochés pour rester des événements isolés. Ils forment une excitation continue, la distribution des amplitudes redevient gaussienne, et le kurtosis retombe vers zéro. L'indicateur perd donc sa sensibilité au moment où le défaut devient grave.

Conséquence pour le système : **une baisse du kurtosis ne signifie jamais que la machine va mieux.** Elle ne s'interprète qu'en regardant l'historique et le RMS en parallèle. Suivre les deux n'est pas redondant, c'est nécessaire.

**Une mesure isolée ne suffit pas.** Hypothèse 3 vérifiée, et le roulement 3 l'illustre bien. Au premier enregistrement, il avait le kurtosis le plus élevé des quatre (3,21 contre 0,07 à 0,63) et le plus fort facteur de crête. Comparer les paliers entre eux à cet instant l'aurait désigné comme suspect — et aurait manqué le roulement 1.

Or son niveau reste stable pendant les sept jours. Ce n'était pas une dégradation, mais sa signature propre : montage, position du capteur, chargement local.

Chaque point de mesure a donc besoin de sa propre référence, établie sur une période saine. La détection porte sur l'écart à cette référence, jamais sur une valeur absolue ni sur une comparaison entre paliers.

**Certaines variations touchent les quatre roulements en même temps.** Les sauts de RMS vers 118 h et 140 h apparaissent sur les quatre canaux. Un défaut localisé n'a aucune raison de faire ça. La documentation indique que les écarts d'horodatage correspondent à des reprises après interruption : le plus probable est donc un changement de conditions au redémarrage — charge, température d'huile, remise en route.

C'est un vrai problème de conception. Un système qui surveille seulement l'écart à la référence aurait crié à l'anomalie sur les quatre paliers. Il faut donc pouvoir distinguer une dérive commune, due aux conditions, d'une dérive isolée, due à un défaut. Deux moyens : suivre plusieurs points de mesure à la fois, et enregistrer en parallèle la température et le courant moteur.

**La fin de l'essai.** L'effondrement des indicateurs sur les quatre canaux vers 164 h correspond à l'arrêt du banc. Ces derniers enregistrements ne sont pas des mesures de fonctionnement et devront être écartés.

**La réduction de données fonctionne.** Les 20 millions de points par canal ont été ramenés à 984 valeurs par indicateur, sans perdre l'information de dégradation — un facteur 20 000. C'est ce qui rend possible à la fois le calcul embarqué et le suivi de tendance sur longue durée. Le choix d'un vecteur de plusieurs indicateurs plutôt que d'un seul est également confirmé.

## 6. Limites

- Un seul essai a été exploité, comportant un seul mode de défaillance (bague extérieure). Les essais 1 et 3 du jeu de données, qui portent sur d'autres modes, n'ont pas été traités.
- Les instants de la chronologie du §4.3 sont des lectures graphiques ; seuls ceux du §4.4 résultent d'un critère explicite.
- Le critère de détection est appliqué au seul roulement 1. Il n'a pas été vérifié qu'il ne se déclenche pas sur les roulements sains, ce qui aurait permis d'estimer un taux de fausse alarme.
- Aucun prétraitement n'a été appliqué avant le calcul des indicateurs. Le filtrage passe-haut et la démodulation d'enveloppe, usuels en analyse de roulements, favorisent les indicateurs de choc et n'ont pas été évalués.
- Le seuil est fixé à trois écarts-types sans justification autre que l'usage. Sa valeur n'a pas fait l'objet d'une analyse de sensibilité.
- Deux indicateurs seulement ont été suivis. Le facteur de crête, calculé au premier enregistrement, n'a pas été inclus dans la boucle.
- Aucune analyse fréquentielle n'a été menée. Les fréquences caractéristiques du roulement (BPFO, BPFI, BSF), calculables à partir de la géométrie fournie, n'ont pas été vérifiées sur les spectres.
- L'interprétation des discontinuités communes comme des reprises d'essai est une hypothèse, non vérifiée dans les horodatages des fichiers.
- Le régime est constant sur toute la durée de l'essai (vitesse et charge fixes). Le comportement des indicateurs sous régime variable, qui sera celui du banc du projet, n'est pas caractérisé ici.
- Aucun seuil de détection n'a été établi.

## 7. Conclusion

Deux des trois hypothèses sont vérifiées. Le kurtosis décroît en phase terminale alors que le RMS poursuit sa croissance, et aucune mesure isolée ne permet d'identifier le palier défaillant.

L'hypothèse d'antériorité du kurtosis est infirmée : avec le critère retenu, le RMS détecte 11,5 h à 19,1 h avant lui selon la période de référence. Ce résultat porte sur le couple indicateur-critère et sur cet essai ; il n'établit pas une infériorité générale du kurtosis, dont l'intérêt diagnostique est confirmé par ailleurs dans cette fiche.

La méthode d'extraction de descripteurs développée en E01–E03 sur signaux simulés est donc applicable à des mesures réelles et y produit un résultat exploitable.

**Décisions retenues pour la suite** :
- le suivi portera sur l'écart à une référence propre à chaque point de mesure, établie sur une période de fonctionnement sain, et non sur des valeurs absolues ;
- le RMS et le kurtosis seront suivis conjointement, sans qu'aucun ne soit présumé plus précoce, la décroissance du second n'étant interprétable qu'au regard du premier ;
- tout critère de détection comportera une exigence de persistance, un dépassement ponctuel de seuil n'étant pas significatif ;
- la référence saine sera constituée dès les premiers essais du banc, et non extraite a posteriori d'un historique ;
- des grandeurs d'ambiance seront enregistrées en parallèle des vibrations afin de distinguer les dérives communes des dérives isolées ;
- les enregistrements correspondant aux phases d'arrêt seront écartés.

**Prochaines étapes** :
- calcul des fréquences caractéristiques du roulement ZA-2115 et vérification de leur présence dans les spectres du roulement 1 aux différents stades de dégradation (E05) ;
- à réception du matériel, mise en œuvre de la chaîne d'acquisition ESP32 et vérification de la régularité de l'échantillonnage (E06).
