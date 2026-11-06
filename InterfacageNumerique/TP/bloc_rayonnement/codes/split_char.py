# -*- coding: utf-8 -*-
"""
Split string of characters in Python

***************************************************************

Creation 2026/11/06
@author: julien.villemejane <julien.villemejane@institutoptique.fr>
LEnsE / https://lense.institutoptique.fr/
"""

data_string = 'A1,20.5,58;A2,54.2,60'

data_split1 = data_string.split(',')
data_split2 = data_string.split(';')

print(data_split1)
print(data_split2)