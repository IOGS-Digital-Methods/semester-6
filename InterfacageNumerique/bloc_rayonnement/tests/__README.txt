Diagramme de Rayonnement / Test de la maquette
==============================================
	LEnsE / Julien VILLEMEJANE


Ces fichiers binaires sont prévus pour tester les fonctionnalités des maquettes
de travaux pratiques utilisées au Laboratoire d'Enseignement Expérimental de
l'Institut d'Optique.

Ils ont été compilés avec MBED-OS v6.17 pour des cartes Nucléo L476RG.


Liste des fichiers
==================

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