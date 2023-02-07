from mosaic_functions import *
import time

im = Image.open("test_bird.jpg").convert("RGB")

im_r = generate_mosiac(im, 10, 10, query = 'flowers')
im_r.save('result_image_10.8.22(2).jpg')