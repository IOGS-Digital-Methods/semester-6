#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Outils Numériques / Semestre 5 / Institut d'Optique

Classe simple / Redéfinition fonction __str__

Created on 09/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

import datetime

class Animal:
	""" object class Animal
	"""	
	def __init__(self, name:str="Hello", birthyear:int=2000):
		""" Animal class constructor
		:name: name of the animal
		:birthyear: year of birth of the animal
		"""
		self.name = name
		self.birthyear = birthyear
		
	def __str__(self):
		""" Animal class display
		"""
		return f"Animal [ {self.name} ] born in {self.birthyear}"
		
	def move(self):
		print(f"\t[ {self.name} ] is moving")
		
	def get_age(self) -> int:
		return datetime.date.today().year - self.birthyear
        
        

# Test of the class Animal
if __name__ == '__main__':
    animal1 = Animal()
    print("Animal 1 Name = ", animal1.name)
    animal2 = Animal("Garfield")
    print("Animal 2 Name = ", animal2.name)
    
    print(animal1)
    
    print(f"Animal 2 is {animal2.get_age()} years old")