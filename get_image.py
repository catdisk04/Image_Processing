# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:29:26 2022

@author: aldis
"""

import time
import bs4 as bs
import urllib.request



def rgb_to_hex(color_tup):
    r, g, b = color_tup
    return ('{:X}{:X}{:X}').format(r, g, b)

def get_image(color_tup):
    
    hex_col = rgb_to_hex(color_tup)
    url = 'https://www.pexels.com/search/dog/?color=' + hex_col
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    source = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(source,'lxml')
    
    image_div = soup.find("div", class_="BreakpointGrid_item__erUQQ")
    
    image_link = image_div.find("img").get("src")
    
    return image_link
print(get_image((76, 175, 80)))