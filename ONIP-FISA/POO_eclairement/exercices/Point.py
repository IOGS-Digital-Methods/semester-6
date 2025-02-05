# -*- coding: utf-8 -*-
"""
Class Point to describe a point in a 2D space

Modifications
-------------
    Creation on 2024/02/01


Authors
-------
    Julien VILLEMEJANE

"""

import numpy as np

class Point:
    """Class to represent a point with its coordinates in a two-dimensional space

    :param name: Name of the point. Default ''
    :type name: str
    :param x: X coordinate of the Point. Default 0
    :type x: float number
    :param y: Y coordinate of the Point. Default 0
    :type y: float number
    """
    
    def __init__(self, x_init: float=0, y_init: float=0, name_init: str='') -> None:
        """Constructor method
        """
        self.name: str = name_init
        self.x: float = x_init
        self.y: float = y_init
        
    def __str__(self) -> str:        
        """Display with print method
        """
        return f'p_{self.name} ( {self.x}, {self.y} )'

    
    def rename(self, value: str) -> None:
        """Renames the point
        
        :param value: Name of the point
        :type value: str
        """
        self.name = value
        
    def distance(self, point: 'Point' = None) -> None:
        """Return the distance between this point and the point given as parameter.
        
        :param point: Point to calculate the distance.
        :type point: Point
        :return: Return the distance between this point and the point given as parameter.
        :rtype: float
        
        """
        if point is None:
            return np.sqrt((self.x**2) + (self.y**2))
        else:
            return np.sqrt(((self.x-point.x)**2) + ((self.y-point.y)**2))

    def move(self, x_new, y_new):
        """Changes the coordonate of the point
        
        :param x_new: new X coordinate of the Point
        :type x_new: float number
        :param y_new: new Y coordinate of the Point
        :type y_new: float number
        """
        self.x = x_new
        self.y = y_new


if __name__ == '__main__':
    pointA = Point()
    print(pointA)
    pointA.rename('A')
    print(pointA)
    
    pointB = Point(2, 3, 'B')
    print(pointB)
    
    print(pointB.distance(pointA))
    
    
    pA = Point(3, 6, 'A')
    pB = Point(0, 10, 'B')
    print(pA.distance(pB))