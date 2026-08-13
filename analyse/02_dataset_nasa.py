import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# BLOC 1 : lecture d'un fichier du dataset IMS

DOSSIER = Path(r"C:\Users\maxen\datasets\ims\4. Bearings\2nd_test")
FS      = 20000.0        # Hz, d'apres le readme du dataset

fichiers = sorted(DOSSIER.iterdir()) # ici on les tri par ordre alphabetique car ils sont au format année.mois.jour.heure.minute.seconde
print(f"{len(fichiers)} fichiers trouves")
print(f"premier : {fichiers[0].name}")
print(f"dernier  : {fichiers[-1].name}")

# lecture du premier fichier (machine encore saine)
data = np.loadtxt(fichiers[0])
print(f"forme du tableau : {data.shape}")

t = np.arange(data.shape[0]) / FS
print(f"duree du fichier : {t[-1]:.3f} s")

fig, axes = plt.subplots(4, 1, figsize=(11, 8), sharex=True, sharey=True)
for i, ax in enumerate(axes):
    ax.plot(t, data[:, i], lw=0.4)
    ax.set_ylabel("a (g)")
    ax.set_title(f"Roulement {i+1}", loc="left", fontsize=10)
    ax.grid(alpha=0.3)
axes[-1].set_xlabel("Temps (s)")
axes[-1].set_xlim(0, 0.05)
plt.tight_layout()
plt.show()


# BLOC 2 : Indicateur sur un fichier reel

from scipy.stats import kurtosis

def indicateurs(x):
    x = x - np.mean(x)                 
    rms   = np.sqrt(np.mean(x**2))     
    crete = np.max(np.abs(x))          
    return {
        "RMS":              rms,
        "Crete":            crete,
        "Facteur de crete": crete / rms,
        "Kurtosis":         kurtosis(x, fisher=True),
    }

for i in range(4):
    signal = data[:, i]
    v = indicateurs(signal)
    print(f"Roulement {i+1:2d} " + "  ".join(f"{k}={val:7.3f}" for k, val in v.items()))


# Bloc 3 : evolutions des indicateurs sur l'ensemble du dataset

resultat = []

for f in fichiers:
    d = np.loadtxt(f)
    ligne = []
    for i in range(4):
        signal = d[:, i]
        v = indicateurs(signal)
        ligne.append(v["RMS"])
        ligne.append(v["Kurtosis"])
    resultat.append(ligne)
    if len(resultat) %100 == 0:
        print(f"{len(resultat)} fichiers traites")

resultat = np.array(resultat)
print(resultat.shape)


# Bloc 4 : visualisation des evolutions

heures = np.arange(len(resultat)) * 10 / 60 # les fichiers sont espacés de 10 minutes, on convertit en heures

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

for i in range(4):
    ax1.plot(heures, resultat[:, 2*i], label= f"Roulement {i+1}", lw=1)
    ax2.plot(heures, resultat[:, 2*i + 1], label = f"Roulement {i+1}" , lw=1)

ax1.set_ylabel("RMS (g)")
ax1.set_title("Evolution du RMS", loc="left", fontsize=10)
ax1.legend()
ax1.grid(alpha=0.3)

ax2.set_ylabel("Kurtosis")
ax2.set_title("Evolution du Kurtosis", loc="left", fontsize=10)
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()
