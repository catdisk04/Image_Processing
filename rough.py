# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:29:11 2022

@author: aldis
"""
from PIL import Image

import urllib, requests
import bs4 as bs
from io import BytesIO
from mosaic_functions import *
import csv

image = Image.open("test_bird.jpg").convert('RGB')

image_dict = divide_image(image, 10, 10)

colors_list = list(set(image_dict.values()))

def distance(tup1, tup2):
    
    return ((tup1[0] - tup2[0])**2 + (tup1[1] - tup2[1])**2 + (tup1[2] - tup2[2])**2)**0.5

differences = []

got_colors= []

print(len(colors_list))

for color in colors_list:
    got_color= get_avg_rgb(get_image_pexel(color, 10,10))
    got_colors.append(got_color)
    differences.append(distance(color, got_color))

print("len(slorslist): ", len(colors_list))
print("###")
print("avg difference: ", sum(differences)/len(differences))
print("###")
print("differences: ", differences)
print("###")
print("colors gotten: ", got_colors)
print("###")
print("colors_list: ", colors_list)
    