#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Outils Numériques / Semestre 6 / Institut d'Optique

Classe simple / Redéfinition fonction __str__

Created on 09/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

import datetime

class Animal:
	""" object class Animal
	"""	
	def __init__(self, name:str, birthyear:int=2000):
		""" Animal class constructor
		:param name: name of the animal
		:param birthyear: year of birth of the animal. Default 2000.
		"""
		self.name = name
		self.birthyear = birthyear
		
	def __str__(self):
		""" Animal class display
		"""
		str = f"Animal [ {self.name} ] born in {self.birthyear}"
		str += f" ({self.get_age()} yo)"
		return str
		
	def move(self):
		print(f"\t[ {self.name} ] is moving")
		
	def get_age(self) -> int:
		return datetime.date.today().year - self.birthyear
        
        
# Test of the class Animal
animal1 = Animal("Felix", 2021)
print("Animal 1 Name = ", animal1.name)
animal1.name = "John"   # Modifying name of the animal
print("Animal 1 Name = ", animal1.name)
animal1.move()          # Calling a method of the Animal class

# New instance of Animal
animal2 = Animal("Garfield")
print("Animal 2 Name = ", animal2.name)
print(f"Animal 2 is {animal2.get_age()} years old")


print(animal1)

# List with objects
animaux = []
animaux.append(animal1)
animaux.append(animal2)
print(f"Name of animal [0] = {animaux[0].name}")