import numpy as np
import matplotlib.pyplot as plt



# Partie 1 : génération d'un signal vibratoire simulé

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

spectre = np.fft.rfft(signal * fenetre) # le fenêtrage ici n'est techniquement pas necessaire car les conditions sont idéales
freqs = np.fft.rfftfreq(N, 1 / FS)

# Correction de l'amplitude du spectre : x2 (spectre replié) et compensation de la fenêtre
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



# Partie 3 : effet du fenêtrage sur la fuite spectrale

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



# Partie 4 : indicateurs statistiques du signal

from scipy.stats import kurtosis, skew

def indicateurs(x):
    x = x - np.mean(x)                 # on retire la composante continue (ici np.mean(x) est la moyenne du signal, n'étant pas la vibration on l'a retire)
    rms   = np.sqrt(np.mean(x**2))     # valeur efficace = energie du signal     (RMS = Root Mean Square)
    crete = np.max(np.abs(x))          # plus grande excursion
    return {
        "RMS":              rms,
        "Crete":            crete,
        "Facteur de crete": crete / rms,
        "Kurtosis":         kurtosis(x, fisher=True),
        "Skewness":         skew(x),
    }

rng   = np.random.default_rng(42)  #On garantit la reproductibilité des résultats en fixant la graine du générateur de nombres aléatoires
bruit = 0.05 * rng.standard_normal(len(t))

# a) machine saine
sain = 0.30*np.sin(2*np.pi*F_ROT*t) + 0.10*np.sin(2*np.pi*2*F_ROT*t) + bruit

# b) balourd aggrave : le 1x est triple, le reste ne bouge pas
balourd = 0.90*np.sin(2*np.pi*F_ROT*t) + 0.10*np.sin(2*np.pi*2*F_ROT*t) + bruit

# c) ecaillage de roulement : chocs brefs, repetitifs, amortis
chocs  = sain.copy() # sans le .copy, on aurait modifié le signal sain
F_CHOC = 89.0        # frequence de repetition des chocs (Hz)
TAU    = 0.002       # amortissement du choc (s)
for k in range(int(F_CHOC*DUREE)):
    t0  = k / F_CHOC
    idx = t >= t0
    chocs[idx] += 0.5*np.exp(-(t[idx]-t0)/TAU)*np.sin(2*np.pi*1200*(t[idx]-t0))

for nom, sig in [("Sain", sain), ("Balourd", balourd), ("Chocs", chocs)]:
    v = indicateurs(sig)
    print(f"{nom:10s} " + "  ".join(f"{k}={val:7.3f}" for k, val in v.items())) #ici c'est purement cosmetique, un print(nom,v) aurait suffit, mais moins lisible

fig, axes = plt.subplots(3, 1, figsize=(11, 7), sharex=True)
for ax, (nom, sig) in zip(axes, [("Sain", sain), ("Balourd", balourd), ("Chocs", chocs)]):
    ax.plot(t, sig, lw=0.8)
    ax.set_ylabel("a (g)")
    ax.set_title(nom, loc="left", fontsize=10)
    ax.grid(alpha=0.3)
axes[-1].set_xlabel("Temps (s)")
axes[-1].set_xlim(0, 0.2)
plt.tight_layout()
plt.show()