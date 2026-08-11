import numpy as np
import matplotlib.pyplot as plt



#Partie 1 : génération d'un signal vibratoire simulé

FS = 3200          # fréquence d'échantillonnage en Hz
DUREE = 1.0        # durée du signal en secondes (s)
F_ROT = 25.0       # fréquence de rotation : 25 Hz = 1500 tr/min => tr/min:60 = Hz

t = np.arange(0, DUREE, 1 / FS)     # les instants de mesure (début, fin, pas)

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



#Partie 2 : analyse fréquentielle avec la FFT

N = len(signal)
fenetre = np.hanning(N)  # fenêtre de Hanning

spectre = np.fft.rfft(signal * fenetre)
freqs = np.fft.rfftfreq(N, 1 / FS)

#Correction de l'amplitude du spectre : x2 (spectre replié) et compensation de la fenêtre
amplitude = 2 * np.abs(spectre) / np.sum(fenetre)

plt.figure(figsize=(10, 4))
plt.plot(freqs, amplitude)
plt.xlim(0, 200)
plt.xlabel("Fréquence (Hz)"); plt.ylabel("Amplitude (g)")
plt.title("Spectre — les défauts deviennent lisibles")
plt.grid(alpha=0.3)
plt.tight_layout(); plt.show()

for cible in [F_ROT, 2 * F_ROT]:
    i = np.argmin(np.abs(freqs - cible))
    print(f"Pic à {freqs[i]:6.1f} Hz → amplitude {amplitude[i]:.3f} g")



#Partie 3 : effet du fenêtrage sur la fuite spectrale

F_ROT2 = 25.4     # fréquence non-multiple donc un cas réaliste

sig2 = 0.30 * np.sin(2 * np.pi * F_ROT2 * t)

spec_sans = 2 * np.abs(np.fft.rfft(sig2)) / N
spec_avec = 2 * np.abs(np.fft.rfft(sig2 * fenetre)) / np.sum(fenetre)

plt.figure(figsize=(10, 4))
plt.plot(freqs, spec_sans, label="Sans fenêtrage")
plt.plot(freqs, spec_avec, label="Avec fenêtre de Hann")
plt.xlim(0, 60); plt.yscale("log")
plt.xlabel("Fréquence (Hz)"); plt.ylabel("Amplitude (g)")
plt.title("Effet du fenêtrage sur la fuite spectrale")
plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout(); plt.show()