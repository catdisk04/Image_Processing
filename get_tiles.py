import urllib, requests
import bs4 as bs
import time
import random
import csv
from PIL import Image
from io import BytesIO

index = 0
def get_noun():
    global index
    result = []
    with open('nouns.txt') as file:
        lines = file.read().split()
        result = lines[index]
        index += 1
    
        
    return result

tile_file = open("tiles.csv", 'w', newline = '')
tiles_writer = csv.writer(tile_file)
tiles_writer.writerow(['img_code', 'avg_r', 'avg_g', 'avg_b'])

def get_avg_rgb(Image_obj):
    im = Image_obj
    r, g, b = im.split()
    l = [r, g, b]
    b = []
    for i in l:
        b.append(list(i.getdata()))
    avg = []
    for i in b:
        avg.append(sum(i)//len(i))
    return tuple(avg)


error_counter = 0

for i in range(500):
    print(i)
    url = "https://www.gettyimages.in/photos/" + get_noun()
    # print(url)      
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source,'lxml')
    
    images_html = soup.find_all('a', class_ = 'MosaicAsset-module__link___wwW2J')[:20]
    for image in images_html:
        try:
            target = image.get('target')
            image_url = image.find('source').get('srcset')
            request= requests.get(image_url)
            image_obj = Image.open(BytesIO(request.content))
            rgb = get_avg_rgb(image_obj)
            tiles_writer.writerow([target, rgb[0], rgb[1], rgb[2]])
            # print([target, rgb[0], rgb[1], rgb[2]])
        except:
            error_counter += 1
        

tile_file.close()
print('errors: ', error_counter())