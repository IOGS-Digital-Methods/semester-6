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

class Point:
    """Class to represent a point with its coordinates in a two-dimensional space

    :param name: Name of the point. Default ''
    :type name: str
    :param x: X coordinate of the Point. Default 0
    :type x: float number
    :param y: Y coordinate of the Point. Default 0
    :type y: float number
    """
    
    def __init__(self, x_init=0, y_init=0, name_init=''):
        """Constructor method
        """
        self.name = name_init
        self.x = x_init
        self.y = y_init
        
    def __str__(self):        
        """Display with print method
        """
        return f'Point {self.name} - X={self.x} / Y={self.y}'
    
    def rename(self, value):
        """Renames the point
        
        :param value: Name of the point
        :type value: str
        """
        self.name = value

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