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