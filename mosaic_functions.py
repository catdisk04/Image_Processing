from PIL import Image
from pexels_api import API
import urllib, requests
from io import BytesIO
import csv
import bs4 as bs

#used by get_images_pexel function
tiles = dict()

apikeylist = ['563492ad6f917000010000018c0523427c5441e19326cdea5e6da603', '563492ad6f9170000100000114025aa23fdd4934993c6b313780ed85', '563492ad6f917000010000014f008258012d4dd7b4a6fcce857642af']
PEXELS_API_KEY = apikeylist[2]

def load_tiles(tiles_file):
    
    global getty_tiles
    
    with open(tiles_file, 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            getty_tiles[row[0]] = (row[1], row[2], row[3])
            
            
    
    
    return None

def get_divisions(im_x, im_y, num_div_x, num_div_y):
    """
    for segregating a given im_x by im_y img into num_div_x groups along x axis 
    and num_div_y groups along the y axis. 

    Parameters
    ----------
    im_x : int
    im_y : int
    num_div_x : int
    num_div_y : int

    Returns
    -------
    D : dict
        dictionary mappping each divisions to list of top left and bottom right 
        pixels of original image that belong to the division.
        each pixel is represented as cartesian coordinates.

    """
    
    if im_x % num_div_x != 0 or im_y % num_div_y != 0:
        print("Number of divisions must be a divisor of the respective dimension")
        return None
    
    l_x = list(range(im_x // num_div_x))
    l_y = list(range(im_y // num_div_y))
        
    D=dict()
    
    for x in range(num_div_x):
        for y in range(num_div_y):
            x_list, y_list = [], []
            for a in l_x:
                x_list.append(a + (x * (im_x // num_div_x)))
            
            for b in l_y:
                y_list.append(b + (y * (im_y // num_div_y)))
            
            result = [(x_list[0], y_list[0]), (x_list[-1], y_list[-1])]
            
            D[(x, y)] = result[:]
    return D


def get_avg_rgb(Image_obj):
    """
    returns avg rgb value of all pixels in a Image obj
    

    Parameters
    ----------
    Image_obj : Image

    Returns
    -------
    tuple
        avg rgb value of image.

    """
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

# print(get_divisions(10, 10, 5, 5))

def divide_image(im, num_div_x, num_div_y):
    """
    divides image into constituent blocks that have to become mosaic
    tiles and maps position  of each block to its avg color

    Parameters
    ----------
    im : Image
        image to be divided.
    num_div_x : int
        number of divisions along x axis.
    num_div_y : int
        number of divisions along y axis.

    Returns
    -------
    result_colors : dict
        dict mapping position of block to avg volor of block as a rgb tuple.

    """
    size = im.size
    D = get_divisions(size[0], size[1], num_div_x, num_div_y)
    result_images = dict()
    result_colors = dict()
    
    for key in D.keys():
        val = D[key]
        
        #+1 to address white lines issue between joined images
        area = (val[0][0], val[0][1], val[1][0]+1, val[1][1]+1)
        result_images[key] = im.crop(area).copy()
        result_colors[key] = get_avg_rgb(result_images[key])
    
    return result_colors
            
            
def join_image(images_dict, cartesian_dict):
    """
    to check divide_image function

    Parameters
    ----------
    images_dict : dict
        dict mapping position to image.
    cartesian_dict : int
        position dict .

    Returns
    -------
    None.
    Shows the result image

    """
    
    size_one_image = list(images_dict.values())[0].size
    
    l1, l2 = [], []
    for i in images_dict.keys():
        l1.append(i[0])
        l2.append(i[1])
    num_x_divs = max(l1) + 1
    num_y_divs = max(l2) + 1
    # print("num_x: ", num_x_divs, "num_y: ", num_y_divs)
    
    result_size = ((size_one_image[0])*(num_x_divs),( size_one_image[1])*(num_y_divs))
    # print(result_size)
    
    result_image = Image.new('RGB', result_size)
    
    for key in images_dict.keys():
        # print(cartesian_dict[key])
        # print(images_dict[key].size)
        result_image.paste(images_dict[key], cartesian_dict[key][0])
    
    result_image.show()

def rgb_to_hex(color_tup):
    """
    converts rgb tuple to hex value

    Parameters
    ----------
    color_tup : tuple
        rgb tuple.

    Returns
    -------
    string
        hex value of rgb tuple.

    """
    r, g, b = color_tup
    return ('{:X}{:X}{:X}').format(r, g, b)

def get_image_pexel(color_tup, block_x, block_y, query = "dog", img_size = 'small', n = 4):
    """
    
    
    

    Parameters
    ----------
    color_tup : tup
        rgb value tuple.
    block_x : int
        number of blocks in a x_axis row.
    block_y : int
        number of blocks in a y_axis row.
    query : str, optional
        query to search for images. The default is "dog".
    img_size : str, optional
        quality of image to be retrieved. The default is 'small'.
    n : int, optional
        to reduce the number of unique rgb values. The default is 16.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    r,g, b = color_tup
    r = (r//n)*n
    g = (g//n)*n
    b = (b//n)*n
    color_tup = (r, g, b)
    
    if color_tup in tiles.keys():
        return tiles[color_tup]
    
    hex_col = rgb_to_hex(color_tup)
    # print(hex_col)
    api = API(PEXELS_API_KEY)
    api.search(query, page=1, results_per_page=10, color = hex_col)
    photos = api.get_entries()
    # print(photos)
    url=  photos[0]['src'][img_size]
    response = requests.get(url)
    
    img = Image.open(BytesIO(response.content)).resize((block_x, block_y))
    
    if color_tup not in tiles.keys():
        tiles[color_tup] = img.copy()
    
    return img

def get_image_getty(color_tup, block_x, block_y, n = 16, tiles_file = 'tiles_final_2.csv'):
    
    r,g, b = color_tup
    r = (r//n)*n
    g = (g//n)*n
    b = (b//n)*n
    color_tup = (r, g, b)
    
    try:
        getty_tiles
    except:
        load_tiles(tiles_file)
    
    def get_image_from_getty_code(code):
        
        url = 'https://www.gettyimages.in/photos/' + str(code)
        
        source = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(source,'lxml')
    
        img_url = soup.find("picture").find("source").get("srcset")
        
        image = Image.open(BytesIO(requests.get(img_url).content), )
        
        return image

        
        
        
        return
    
    
    
    
    return


def num_different_colors(im, block_x, block_y):
    """
    

    Parameters
    ----------
    im : Image
        DESCRIPTION.
    block_x : int
        DESCRIPTION.
    block_y : inr
        DESCRIPTION.

    Returns
    -------
    int
        number of dstinct avg colors of blocks.

    """

    img_x, img_y = im.size
    
    num_div_x = img_x//block_x
    num_div_y = img_y//block_y
    
    image_colors_dict = divide_image(im, num_div_x, num_div_y)
    
    l = []
    
    for i in image_colors_dict.values():
        if rgb_to_hex(i) not in l:
            l.append(rgb_to_hex(i))
    print(l)
    return len(l)

def generate_mosiac(image, block_x, block_y, query= "dog"):
    """
    

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    block_x : TYPE
        DESCRIPTION.
    block_y : TYPE
        DESCRIPTION.
    query : TYPE, optional
        DESCRIPTION. The default is "dog".

    Returns
    -------
    result_image : TYPE
        DESCRIPTION.

    """
    
    img_x, img_y = image.size
    if img_x % block_x != 0 or img_y % block_y != 0:
        print("Use different block size. divisibility issues.")
        return 
    # print(num_different_colors(image, block_x, block_y))
    
    num_div_x = img_x//block_x
    num_div_y = img_y//block_y
    # print("nums: ")
    # print(num_div_x, num_div_y)
    
    positions_dict = get_divisions(img_x, img_y, num_div_x, num_div_y)
    image_colors_dict = divide_image(image, num_div_x, num_div_y)
    
    result_image = Image.new('RGB', image.size)
    
    num = 0
    for index in positions_dict.keys():
        num += 1
        print("index: ", num)
        block_image = get_image_pexel(image_colors_dict[index], block_x, block_y, query)
        # print(positions_dict[index])
        result_image.paste(block_image, positions_dict[index][0])
    
    result_image.show()    
    
    return result_image


    
    
    
    
    
    
    

        