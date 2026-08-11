# Mini-HUMS — surveillance vibratoire d'une machine tournante

Système embarqué de détection d'anomalies mécaniques par analyse vibratoire,
inspiré des HUMS (Health and Usage Monitoring Systems) aéronautiques.

**Matériel** : ESP32, accéléromètre ADXL345, carte SD, INA219, DS18B20
**Banc d'essai** : ventilateur 120 mm à roulements à billes

## État d'avancement
- [x] Structure du projet et environnement
- [ ] Chaîne d'acquisition à cadence fixe (3200 Hz)
- [ ] Stockage local et télémétrie
- [ ] Traitement du signal (FFT, indicateurs)
- [ ] Campagne d'essais avec défauts contrôlés
- [ ] Détection d'anomalies

## Structure
- `firmware/` — code embarqué ESP32 (PlatformIO)
- `analyse/` — traitement et modèles (Python)
- `donnees/` — enregistrements
- `docs/` — notes, schémas, résultats
