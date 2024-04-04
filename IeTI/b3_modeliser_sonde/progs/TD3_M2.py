import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Définition des paramètres du système
R = 1e6
Rs = 9e6
C = 125e-9
Cs = 5e-9
# Cs = 50e-9
# Cs = C*R/Rs

# Création de la fonction de transfert du système
num = [Rs*Cs*R/(R+Rs), R/(R+Rs)]
den = [R*Rs/(R+Rs)*(C+Cs), 1]
system = signal.TransferFunction(num, den)

# Calcul de la réponse en fréquence
w = np.logspace(-1, 4, 1000)
w, mag, phase = signal.bode(system, w)

# Tracé du diagramme en gain
plt.figure()
plt.semilogx(w, mag)
plt.title('Diagramme en gain')
plt.xlabel('Pulsation (rad/s)')
plt.ylabel('Gain (dB)')
plt.grid()
plt.grid(which='both', linestyle='--')
plt.grid(which='minor', alpha=0.2)
plt.grid(which='major', alpha=0.5)

# Tracé du diagramme en phase
plt.figure()
plt.semilogx(w, phase)
plt.title('Diagramme en phase')
plt.xlabel('Pulsation (rad/s)')
plt.ylabel('Phase (degrés)')
plt.grid()
plt.grid(which='both', linestyle='--')
plt.grid(which='minor', alpha=0.2)
plt.grid(which='major', alpha=0.5)

plt.show()
