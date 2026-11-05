# E05 — Mise en service de l'ADXL345 et validation de la cadence d'échantillonnage

**Dates** : 1er et 5 novembre 2026
**Opérateur** : Maxence
**Phase du projet** : 1 — acquisition

---

## 1. Objectif

Mettre en service la chaîne d'acquisition (accéléromètre ADXL345 relié à un ESP32 en SPI) et vérifier qu'elle permet d'échantillonner les trois axes à 3200 Hz avec un intervalle régulier entre deux mesures.

**Hypothèse** : l'ESP32 lit les trois axes en moins de 312,5 µs (période correspondant à 3200 Hz), et une boucle cadencée par l'horloge de la carte permet de tenir cet intervalle à ±1 % près.

**Motivation** : les scripts d'analyse (E01 à E04) supposent des échantillons parfaitement espacés dans le temps. Si l'intervalle réel varie, les fréquences calculées par la FFT sont faussées. La régularité doit donc être vérifiée avant toute campagne de mesure.

## 2. Moyens

| Élément | Valeur |
|---|---|
| Carte | ESP32 WROOM-32, interface USB CH340 |
| Capteur | Module GY-291 (puce ADXL345) |
| Liaison | SPI, 4 fils, câbles Dupont sur breadboard |
| Environnement | PlatformIO, framework Arduino |
| Liaison série | 115 200 bauds |
| Code | `firmware/src/main.cpp` |
| Commit | *(à compléter)* |

**Câblage**

| ADXL345 | ESP32 | Rôle |
|---|---|---|
| VCC | 3V3 | alimentation |
| GND | GND | masse |
| CS | GPIO 5 | sélection du composant |
| SDO | GPIO 19 | MISO (capteur → ESP32) |
| SDA | GPIO 23 | MOSI (ESP32 → capteur) |
| SCL | GPIO 18 | horloge SPI |

## 3. Conditions

- Capteur posé à plat sur la table, au repos, sans source de vibration.
- Registres du capteur : DATA_FORMAT = 0x08 (pleine résolution, ±2 g, SPI 4 fils), POWER_CTL = 0x08 (mode mesure), BW_RATE = 0x0F (3200 Hz).
- SPI matériel de l'ESP32, mode 3, 1 MHz.
- Pour chaque configuration : série de 1000 lectures, horodatées avec `micros()` (résolution 1 µs). On calcule ensuite le minimum, le maximum et la moyenne des 999 écarts entre lectures successives.
- Aucune autre tâche ne tourne sur la carte (pas de WiFi, pas de carte SD).

## 4. Résultats

### 4.1 Mise en service

La mise en service a demandé plusieurs corrections successives.

| Étape | Symptôme | Cause identifiée | Correction |
|---|---|---|---|
| 1 | Caractères illisibles sur le moniteur série | Moniteur à 9600 bauds, carte à 115 200 | `monitor_speed = 115200` dans `platformio.ini` |
| 2 | Capteur non détecté en SPI | Arguments du constructeur Adafruit dans le mauvais ordre (l'ordre attendu est horloge, MISO, MOSI, CS) | Ordre corrigé |
| 3 | Capteur détecté, mais X = Y = Z = 0 | Voir ci-dessous | Pilote SPI écrit à la main |

**Diagnostic de l'étape 3.** Lecture directe de trois registres :

| Registre | Adresse | Valeur attendue | Valeur lue |
|---|---|---|---|
| DEVID | 0x00 | 0xE5 | 0xE5 |
| BW_RATE | 0x2C | 0x0A (défaut) | 0x0A |
| POWER_CTL | 0x2D | 0x08 (écrit par la bibliothèque) | **0x00** |

Les lectures sont correctes mais l'écriture de POWER_CTL n'est pas prise en compte : le capteur reste en veille et ses registres de mesure valent 0. Le code source de la bibliothèque Adafruit montre qu'elle communique en SPI mode 1, alors que la fiche technique de l'ADXL345 impose le mode 3. Un pilote minimal a été écrit avec la bibliothèque SPI de l'ESP32 en mode 3 ; l'écriture de POWER_CTL est alors relue à 0x08.

**Remarque.** Avant la correction de l'étape 2, le capteur n'a pas non plus été détecté en I2C (scanner I2C sans résultat), avec deux modules et deux cartes. La cause de cet échec n'a pas été identifiée.

### 4.2 Mesure au repos

Capteur à plat, valeurs typiques en g :

| X | Y | Z | Norme |
|---|---|---|---|
| 0,02 | −0,07 | 0,877 | ≈ 0,88 |

La norme attendue est 1,00 g (gravité seule).

### 4.3 Cadence d'échantillonnage

| Configuration | Min (µs) | Max (µs) | Moy (µs) |
|---|---|---|---|
| A — Lecture à pleine vitesse, sans cadencement | 88 | 93 | 89 |
| B — Cadencé, horodatage après la lecture | 307 | 314 | 312 |
| C — Cadencé, horodatage avant la lecture | 288 | 314 | 312 |
| D — Cadencé, horodatage avant la lecture, départ décalé de 100 µs | 311 | 314 | 312 |

En configuration D, le premier écart (entre les lectures 0 et 1) vaut 312 µs.

Valeur cible : 312,5 µs.

**Principe du cadencement (B, C, D).** L'instant prévu pour la lecture *i* est calculé à partir du départ de la série : `cible = t0 + (i × 625) / 2`. Le programme attend dans une boucle `while` que `micros()` atteigne cette valeur, puis lance la lecture.

## 5. Analyse

**Temps de lecture.** Une lecture complète des trois axes prend 89 µs en moyenne (configuration A), soit 28 % de la période disponible. À 1 MHz, les 7 octets échangés (1 octet d'adresse et 6 octets de données) représentent 56 µs ; le reste correspond au traitement autour de l'échange. Il reste environ 220 µs par période pour d'autres tâches, ce qui laisse de la marge pour le stockage et la télémétrie. La fréquence SPI pourrait être portée à 5 MHz si cette marge devenait insuffisante.

**Choix du calcul de la cible.** La période de 312,5 µs n'est pas un nombre entier de microsecondes. Attendre 312 µs ou 313 µs après chaque lecture ferait dériver la fréquence (environ 3205 Hz ou 3195 Hz) avec une erreur qui s'accumulerait sur toute la série. Calculer chaque cible à partir du départ évite cette dérive : les écarts alternent entre 312 et 313 µs et la moyenne reste à 312,5 µs.

**Effet du point de mesure (B et C).** En configuration B, l'horodatage est pris après la lecture. L'écart mesuré inclut donc la variation de durée des lectures (88 à 93 µs), d'où la plage 307–314 µs, alors que les lectures démarrent à intervalle régulier. Le résultat dépend donc de l'endroit où l'on place la mesure du temps, et pas seulement du phénomène mesuré.

**Premier échantillon (C et D).** En configuration C, la valeur de 288 µs vient du premier écart. La cible de la lecture 0 est égale à `t0`, donc cette lecture ne passe pas par l'attente et part avec le retard d'entrée dans la boucle. Décaler le départ de 100 µs (configuration D) oblige toutes les lectures à attendre leur créneau, et le premier écart revient à 312 µs.

**Régularité obtenue (D).** Les écarts restent entre 311 et 314 µs. Cette dispersion s'explique par l'alternance 312/313 µs, la résolution de 1 µs de `micros()` et le temps de réaction de la boucle d'attente. L'erreur maximale est d'environ 2 µs, soit 0,6 % de la période. Pour une composante à 1000 Hz, bien au-delà des fréquences attendues sur le banc, un décalage de 2 µs correspond à une erreur de phase de 2π × 1000 × 2·10⁻⁶ ≈ 0,013 rad, soit environ 0,7°. Cette erreur est négligeable pour l'analyse spectrale prévue.

**Mesure au repos.** La norme mesurée (0,88 g) est inférieure de 12 % à la valeur attendue. Le capteur n'est donc pas seulement incliné : il y a un défaut de mesure. Deux explications sont possibles, un décalage de zéro (offset) sur l'axe Z ou une sensibilité inférieure à la valeur nominale. Un essai avec le capteur retourné permettra de les distinguer. Ce défaut n'a pas d'incidence sur les indicateurs vibratoires (RMS, kurtosis, FFT), calculés sur le signal centré, mais il devra être corrigé pour toute mesure absolue.

## 6. Limites

- La cadence est imposée par l'horloge de l'ESP32, alors que le capteur produit ses mesures selon sa propre horloge interne. Les deux ne sont pas synchronisées : sur une longue durée, certaines mesures peuvent être lues deux fois ou manquées. Ce point n'a pas été quantifié.
- Le contenu des mesures n'a pas été enregistré : on a seulement mesuré les instants de lecture. On n'a pas vérifié que chaque lecture renvoie bien une nouvelle valeur.
- L'attente active occupe entièrement le processeur. Les mesures ont été faites sans autre tâche ; le comportement avec la carte SD et le WiFi actifs reste à vérifier.
- Une seule série de 1000 lectures est rapportée par configuration.
- La cause de l'échec en I2C n'a pas été identifiée.
- L'erreur de mesure au repos (norme de 0,88 g) n'a pas été caractérisée.

## 7. Conclusion

Hypothèse vérifiée. Une lecture des trois axes prend 89 µs, et la boucle cadencée tient une période moyenne de 312 µs avec des écarts compris entre 311 et 314 µs, soit une précision de 0,6 %.

La chaîne d'acquisition fonctionne, sous réserve d'un pilote SPI écrit à la main : la bibliothèque Adafruit, qui utilise le mode SPI 1, ne permet pas d'écrire dans les registres du capteur.

**Décisions retenues pour la suite** :
- utiliser le pilote SPI en mode 3 à la place de la bibliothèque Adafruit ;
- calculer les instants de lecture à partir du départ de la série, et non de la lecture précédente ;
- horodater au déclenchement de la lecture et décaler le départ de la série ;
- toujours vérifier séparément le premier échantillon d'une série.

**Prochaines étapes** :
- essai capteur retourné pour séparer offset et sensibilité ;
- synchroniser la lecture sur le capteur (signal de donnée prête ou mémoire FIFO) plutôt que sur l'horloge de l'ESP32 ;
- enregistrer les mesures et les transférer vers le PC pour analyse en Python.
