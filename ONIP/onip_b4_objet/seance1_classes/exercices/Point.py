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
    
    def __init__(self, x_init=0, y_init=0, name_init=''):
        self.name = name_init
        self.x = x_init
        self.y = y_init
        
    def __str__(self):
        return f'Point {self.name} - X={self.x} / Y={self.y}'
    
    def rename(self, value):
        self.name = value



if __name__ == '__main__':
    pointA = Point()
    print(pointA)
    pointA.rename('A')
    print(pointA)
    
    pointB = Point(2, 3, 'B')
    print(pointB)