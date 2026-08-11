import numpy as np
import matplotlib.pyplot as plt

FS = 3200          # fréquence d'échantillonnage en Hz
DUREE = 1.0        # durée du signal en secondes (s)
F_ROT = 25.0       # fréquence de rotation : 25 Hz = 1500 tr/min => tr/min:60 = Hz

t = np.arange(0, DUREE, 1 / FS)     # les instants de mesure

signal = (
    0.30 * np.sin(2 * np.pi * F_ROT * t)          # 1× : balourd résiduel
    + 0.10 * np.sin(2 * np.pi * 2 * F_ROT * t)    # 2× : léger désalignement
    + 0.05 * np.random.randn(len(t))              # bruit de mesure
)

print(f"{len(t)} échantillons, pas de temps = {1/FS*1e6:.1f} µs")

plt.figure(figsize=(10, 3))
plt.plot(t[:400], signal[:400])
plt.xlabel("Temps (s)"); plt.ylabel("Accélération (g)")
plt.title("Signal vibratoire simulé — vue temporelle")
plt.tight_layout(); plt.show()