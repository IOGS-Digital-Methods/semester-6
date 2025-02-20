Diagramme de Rayonnement / Test de la maquette
==============================================
	LEnsE / Julien VILLEMEJANE


Ces fichiers binaires sont prévus pour tester les fonctionnalités des maquettes
de travaux pratiques utilisées au Laboratoire d'Enseignement Expérimental de
l'Institut d'Optique.

Ils ont été compilés avec MBED-OS v6.17 pour des cartes Nucléo L476RG.


Liste des fichiers
==================

_IntNum_rayon_sw_leds.NUCLEO_L476RG.bin
	Test des bouton-poussoirs et des LEDs de la carte.
	L'appui sur SW1 change l'état de LED1, sur SW2 de LED2.
	L'appui sur le bouton de la carte Nucléo éteint la LED de la carte Nucléo.

_IntNum_rayon_pot_leds.NUCLEO_L476RG.bin
	Test du potentiomètre et des sorties PWM.
	Le potentiomètre RV1 modifie l'intensité lumineuse de la LED2.
	Les bouton-poussoirs SW1 et SW2 modifient l'intensité lumineuse de la LED1.

_IntNum_rayon_spi_led.NUCLEO_L476RG_200mA.bin
_IntNum_rayon_spi_led.NUCLEO_L476RG_13mA.bin
	Test de la commande de la LED de puissance - alimentation réglée à 200mA max
	Applique un courant de 200mA (ou 13 mA) dans la LED.
	
_IntNum_rayon_servo.NUCLEO_L476RG_pos_1500.bin
	Test du servomoteur.
	Positionne le servomoteur en position central. (1500 us sur 20 ms)
	
_IntNum_rayon_servo.NUCLEO_L476RG_fade_pos.bin
	Test du servomoteur.
	Positionne le servomoteur à des angles différents (1200 us à 1800 us)
	de manière répétée (Fade).