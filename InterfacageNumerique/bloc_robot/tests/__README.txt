Robot Joy-It Joy Car / Test de la maquette
==========================================
	LEnsE / Julien VILLEMEJANE


Ces fichiers binaires sont prévus pour tester les fonctionnalités des maquettes
de travaux pratiques utilisées au Laboratoire d'Enseignement Expérimental de
l'Institut d'Optique.

Ils ont été compilés avec MBED-OS v6.17 pour des cartes Nucléo L476RG.


Liste des fichiers
==================

_IntNum_robot_sw_leds.NUCLEO_L476RG.bin
	Test des bouton-poussoirs et des LEDs de la carte.
	L'appui sur SW1 change l'état de LED1, sur SW2 de LED2.
	L'appui sur le bouton de la carte Nucléo éteint la LED de la carte Nucléo.

_IntNum_robot_pot_leds.NUCLEO_L476RG.bin
	Test du potentiomètre et des sorties PWM.
	Le potentiomètre RV1 modifie l'intensité lumineuse de la LED2.
	Les bouton-poussoirs SW1 et SW2 modifient l'intensité lumineuse de la LED1.

_IntNum_robot_line_sensor.NUCLEO_L476RG.bin
	Test des capteurs de ligne R, C, L.
	Nécessite d'ouvrir un moniteur Série à 9600 bauds.
	Affiche la valeur de chacun des capteurs.

_IntNum_robot_ultras.NUCLEO_L476RG_in_cm.bin
	Test du capteur à ultrason. L'alimentation externe doit être branchée.
	Nécessite d'ouvrir un moniteur Série à 9600 bauds.
	Affiche la distance en cm régulièrement.

_IntNum_robot_neoled.NUCLEO_L476RG.bin
	Test des 4 phares.
	Fait varier les couleurs des 4 phares toutes les 500 ms.

_IntNum_robot_motors.NUCLEO_L476RG.bin
	Test des moteurs L et R. L'alimentation externe doit être branchée.
	Les moteurs tournent à vitesse constante (RC = 0.7).
	L'appui sur le bouton-poussoir bleu de la carte stoppe les moteurs.
	Le bouton SW2 change la direction du moteur gauche.
	Le bouton SW1 change la direction du moteur droit.

_IntNum_robot_servo.NUCLEO_L476RG_pos_1500.bin
	Test du servomoteur. L'alimentation externe doit être branchée.
	Positionne le servomoteur en position central. (1500 us sur 20 ms)
	
_IntNum_robot_servo.NUCLEO_L476RG_fade_pos.bin
	Test du servomoteur. L'alimentation externe doit être branchée.
	Positionne le servomoteur à des angles différents (1200 us à 1800 us)
	de manière répétée (Fade).