import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Définition des paramètres du système (boucle ouverte)
GBP = 3e5 # Gain bande-passante
K1 = 1e5  # Gain

# Création des fonctions de transfert des deux systèmes (boucle ouverte/fermée)
tau1 = K1/(2*np.pi*GBP)
num1 = [K1]
den1 = [tau1, 1]
system1 = signal.TransferFunction(num1, den1)

num2 = [K1/(1+K1)]
den2 = [tau1/(1+K1), 1]
system2 = signal.TransferFunction(num2, den2)

# Calcul de la réponse en fréquence des deux systèmes (boucle ouverte/fermée)
w = np.logspace(-1, 9, 1000)
w, mag1, phase1 = signal.bode(system1, w)
w, mag2, phase2 = signal.bode(system2, w)

# Tracé des diagrammes en gain
plt.figure()
plt.semilogx(w, mag1, label='Boucle ouverte')
plt.semilogx(w, mag2, label='Boucle fermée')
plt.title('Diagramme en gain')
plt.xlabel('Pulsation (rad/s)')
plt.ylabel('Gain (dB)')
plt.legend()
plt.grid()
plt.grid(which='both', linestyle='--')
plt.grid(which='minor', alpha=0.2)
plt.grid(which='major', alpha=0.5)

# Tracé des diagrammes en phase
plt.figure()
plt.semilogx(w, phase1, label='Boucle ouverte')
plt.semilogx(w, phase2, label='Boucle fermée')
plt.title('Diagramme en phase')
plt.xlabel('Pulsation (rad/s)')
plt.ylabel('Phase (degrés)')
plt.legend()
plt.grid()
plt.grid(which='both', linestyle='--')
plt.grid(which='minor', alpha=0.2)
plt.grid(which='major', alpha=0.5)

plt.show()
