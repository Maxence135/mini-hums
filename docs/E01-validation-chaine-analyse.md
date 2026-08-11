# E01 — Validation de la chaîne d'analyse sur signal simulé

**Date** : 11 août 2026
**Phase du projet** : 1 — préparation, avant réception du matériel

---

## 1. Objectif

Vérifier que la chaîne de traitement (FFT + normalisation d'amplitude) restitue correctement les composantes fréquentielles d'un signal dont la composition est connue a priori, avant de l'appliquer à des données réelles.

**Hypothèse testée** : un signal construit comme la somme de deux sinusoïdes d'amplitudes connues et d'un bruit gaussien doit produire un spectre où les deux amplitudes sont retrouvées à moins de 5 % près.

## 2. Moyens

| Élément | Valeur |
|---|---|
| Environnement | Python 3.x, numpy, matplotlib, scipy |
| Script | `analyse/01_signal_simule.py` |
| Commit | *(à compléter : hash du commit)* |
| Matériel | Aucun — simulation numérique |

## 3. Conditions

| Paramètre | Valeur |
|---|---|
| Fréquence d'échantillonnage Fs | 3200 Hz |
| Durée | 1,0 s |
| Nombre d'échantillons N | 3200 |
| Résolution fréquentielle (Fs/N) | 3,125 Hz |
| Fréquence de Nyquist (Fs/2) | 1600 Hz |
| Fenêtrage | Hann |

**Composition du signal injecté** :

| Composante | Fréquence | Amplitude |
|---|---|---|
| Fondamentale (1×) | 25,0 Hz | 0,30 g |
| Harmonique d'ordre 2 (2×) | 50,0 Hz | 0,10 g |
| Bruit gaussien | large bande | σ = 0,05 g |

## 4. Résultats

### 4.1 Domaine temporel

Signal périodique de période 40 ms, amplitude crête ≈ 0,4 g, crête-à-crête ≈ 0,85 g. Forme d'onde stable d'une période à l'autre, texture bruitée d'environ ±0,05 g. Légère asymétrie entre la montée et la descente, suggérant la présence d'une harmonique d'ordre 2 — non quantifiable dans ce domaine.

### 4.2 Domaine fréquentiel

| Grandeur mesurée | Valeur | Valeur attendue | Écart |
|---|---|---|---|
| Fréquence du pic 1× | 25,0 Hz | 25,0 Hz | 0 % |
| Amplitude du pic 1× | 0,300 g | 0,300 g | < 1 % |
| Fréquence du pic 2× | 50,0 Hz | 50,0 Hz | 0 % |
| Amplitude du pic 2× | 0,100 g | 0,100 g | < 1 % |
| Plancher de bruit | ≈ 0,003 g | — | — |
| Rapport signal/bruit | ≈ 100 (40 dB) | — | — |

Aucune harmonique d'ordre supérieur détectée. Plancher de bruit plat sur toute la bande analysée, sans structure fréquentielle.

*(Figures : `docs/figures/E01_temporel.png`, `docs/figures/E01_spectre.png`)*

## 5. Analyse

Les amplitudes restituées correspondent aux valeurs injectées à moins de 1 % près : **la chaîne de traitement et la normalisation d'amplitude sont validées**.

L'écart d'échelle entre les deux domaines est notable. Dans le domaine temporel, le bruit (σ = 0,05 g) représente environ un sixième de l'amplitude du fondamental et masque visuellement l'harmonique. Dans le domaine fréquentiel, son énergie étant répartie sur toute la bande, il retombe à 0,003 g — soit un rapport de 100 avec le pic principal. Cette dilution du bruit est le mécanisme qui rend détectables des composantes invisibles à l'œil sur la forme d'onde.

La signature obtenue (1× dominant, 2× à 33 %, sans harmoniques d'ordre supérieur) correspond à celle attendue d'un balourd. Elle sert de référence pour l'interprétation des essais réels.

## 6. Limites

- Le bruit simulé est gaussien et parfaitement blanc, ce qui est une idéalisation. Le bruit réel comportera des composantes structurées (parasites secteur à 50 Hz, résonances de la structure).
- L'échantillonnage simulé est parfaitement régulier. La régularité de l'échantillonnage réel devra être caractérisée séparément (essai E02).
- Fs et N étant fixés, la résolution de 3,125 Hz ne permet pas de séparer deux composantes plus proches que cet écart.

## 7. Conclusion

Chaîne d'analyse validée. Elle peut être appliquée aux données réelles sans modification. **Prochaine étape** : validation de la régularité de l'échantillonnage sur ESP32 (E02), à la réception du matériel.
