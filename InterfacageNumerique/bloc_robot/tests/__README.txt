Robot Joy-It Joy Car / Test de la maquette
==========================================
	LEnsE / Julien VILLEMEJANE


Ces fichiers binaires sont prévus pour tester les fonctionnalités des maquettes
de travaux pratiques utilisées au Laboratoire d'Enseignement Expérimental de
l'Institut d'Optique.

Ils ont été compilés avec MBED-OS v6.17 pour des cartes Nucléo L476RG.


Liste des fichiers
==================

_IntNum_robot_ultras.NUCLEO_L476RG_in_cm.bin
	Test du capteur à ultrason. 
	Nécessite d'ouvrir un moniteur Série à 9600 bauds.
	Affiche la distance en cm régulièrement.

_IntNum_robot_neoled.NUCLEO_L476RG.bin
	Test du phare 1.
	Allume d'une première couleur le phare, puis l'éteint, puis l'allume 
	dans une seconde couleur puis l'éteint à nouveau.
	
_IntNum_rayon_servo.NUCLEO_L476RG_pos_1500.bin
	Test du servomoteur.
	Positionne le servomoteur en position central. (1500 us sur 20 ms)
	
_IntNum_rayon_servo.NUCLEO_L476RG_fade_pos.bin
	Test du servomoteur.
	Positionne le servomoteur à des angles différents (1200 us à 1800 us)
	de manière répétée (Fade).