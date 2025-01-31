# -*- coding: utf-8 -*-
"""
Class Rectangle to describe a rectangle from 2 points in a 2D space

Modifications
-------------
    Creation on 2024/02/01


Authors
-------
    Julien VILLEMEJANE

"""

from Point import *

class Rectangle:
    """Class to represent a rectangle with the coordinates of its opposite vertex, given as :class:`Point`

    :param name: Name of the point. Default ''
    :type name: str
    :param tl_p: top left vertex of the rectangle. Default : None
    :type tl_p: class:`Point`, optional
    :param br_p: bottom right vertex of the rectangle. Default : None
    :type br_p: class:`Point`, optional
    """
    
    def __init__(self, tl_point=None, br_point=None, name_init=''):
        self.name = name_init
        self.tl_p = tl_point
        self.br_p = br_point
        
    def __str__(self):        
        """Display with print method
        """
        return f'Rectangle {self.name} \n\t Top Left={self.tl_p} \n\t Bottom Right={self.br_p}'
    
    def rename(self, value):        
        """Renames the rectangle
        
        :param value: Name of the rectangle
        :type value: str
        """
        self.name = value



if __name__ == '__main__':
    rectA = Rectangle()
    print(rectA)
    rectA.rename('First Rect')
    print(rectA)
    
    
    