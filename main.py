import numpy as np
# import scipy.sparse
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
from skimage import feature, filters
from skimage.color import rgb2gray
from scipy import ndimage
from scipy.ndimage import convolve
import tkinter as tk
from tkinter import filedialog
import re
import shadowStudyForm
import cv


############ ----------  IMAGE PROCESSING ----------- ############
def shadowMix(site_shadow, context_shadow):
    """
 site_shadow: site shadow image array
 context_shadow: context shadow image array
 """
    h, w, c = site_shadow.shape
    x, y = np.meshgrid(np.arange(w), np.arange(h))

    context_shadow_r = context_shadow[:, :, 0].flatten()
    context_shadow_g = context_shadow[:, :, 1].flatten()
    context_shadow_b = context_shadow[:, :, 2].flatten()

    site_shadow_r = site_shadow[:, :, 0].flatten()
    site_shadow_g = site_shadow[:, :, 1].flatten()
    site_shadow_b = site_shadow[:, :, 2].flatten()

    mixed_shadow_r = np.where(np.logical_or(context_shadow_r < 200,np.logical_or(context_shadow_g < 200,context_shadow_b < 200)), context_shadow_r, site_shadow_r)
    mixed_shadow_g = np.where(np.logical_or(context_shadow_r < 200,np.logical_or(context_shadow_g < 200,context_shadow_b < 200)), context_shadow_g, site_shadow_g)
    mixed_shadow_b = np.where(np.logical_or(context_shadow_r < 200,np.logical_or(context_shadow_g < 200,context_shadow_b < 200)), context_shadow_b, site_shadow_b)

    net_shadow_r = np.where(np.logical_or(context_shadow_r < 200,np.logical_or(context_shadow_g < 200,context_shadow_b < 200)), 255, site_shadow_r)
    net_shadow_g = np.where(np.logical_or(context_shadow_r < 200,np.logical_or(context_shadow_g < 200,context_shadow_b < 200)), 255, site_shadow_g)
    net_shadow_b = np.where(np.logical_or(context_shadow_r < 200,np.logical_or(context_shadow_g < 200,context_shadow_b < 200)), 255, site_shadow_b)

    mixed_shadow = np.dstack(
        (mixed_shadow_r.reshape(h, w), mixed_shadow_g.reshape(h, w), mixed_shadow_b.reshape(h, w)))

    net_shadow = np.dstack(
        (net_shadow_r.reshape(h, w), net_shadow_g.reshape(h, w), net_shadow_b.reshape(h, w)))

    return mixed_shadow,net_shadow

def colorShadow(site_shadow,color):

    h, w, c = site_shadow.shape

    site_shadow_r = site_shadow[:, :, 0].flatten()
    site_shadow_g = site_shadow[:, :, 1].flatten()
    site_shadow_b = site_shadow[:, :, 2].flatten()

    mixed_shadow_r = np.where(np.logical_or(site_shadow_r < 200,np.logical_or(site_shadow_g < 200,site_shadow_b < 200)), color[0], 255)
    mixed_shadow_g = np.where(np.logical_or(site_shadow_r < 200,np.logical_or(site_shadow_g < 200,site_shadow_b < 200)), color[1], 255)
    mixed_shadow_b = np.where(np.logical_or(site_shadow_r < 200,np.logical_or(site_shadow_g < 200,site_shadow_b < 200)), color[2], 255)

    return np.dstack((mixed_shadow_r.reshape(h, w), mixed_shadow_g.reshape(h, w), mixed_shadow_b.reshape(h, w)))


def addContrast(image):
    h, w, c = image.shape

    site_shadow_r = image[:, :, 0].flatten()
    site_shadow_g = image[:, :, 1].flatten()
    site_shadow_b = image[:, :, 2].flatten()

    mixed_shadow_r = np.where(np.logical_or(site_shadow_r < 250,np.logical_or(site_shadow_g < 250,site_shadow_b < 250)), 0, 255)
    mixed_shadow_g = np.where(np.logical_or(site_shadow_r < 250,np.logical_or(site_shadow_g < 250,site_shadow_b < 250)), 0, 255)
    mixed_shadow_b = np.where(np.logical_or(site_shadow_r < 250,np.logical_or(site_shadow_g < 250,site_shadow_b < 250)), 0, 255)

    return np.dstack((mixed_shadow_r.reshape(h, w), mixed_shadow_g.reshape(h, w), mixed_shadow_b.reshape(h, w)))


def lighter_shadow_on_roof(base,mixed_shadow,ratio):
    h, w, c = base.shape
    base_r = base[:,:,0].flatten()
    base_g = base[:,:,1].flatten()
    base_b = base[:,:,2].flatten()
    mixed_shadow_r = mixed_shadow[:,:,0].flatten()
    mixed_shadow_g = mixed_shadow[:,:,1].flatten()
    mixed_shadow_b = mixed_shadow[:,:,2].flatten()

    mixed_shadow_r = np.where(np.logical_and(np.logical_and(base_r>180,base_r<190), np.logical_and(base_r==base_g,base_r==base_b)),ratio *mixed_shadow_r+(1-ratio)*base_r,mixed_shadow_r)
    mixed_shadow_g = np.where(np.logical_and(np.logical_and(base_r>180,base_r<190), np.logical_and(base_r==base_g,base_r==base_b)),ratio *mixed_shadow_g+(1-ratio)*base_g,mixed_shadow_g)
    mixed_shadow_b = np.where(np.logical_and(np.logical_and(base_r>180,base_r<190), np.logical_and(base_r==base_g,base_r==base_b)),ratio *mixed_shadow_b+(1-ratio)*base_b,mixed_shadow_b)

    return np.dstack((mixed_shadow_r.reshape(h, w), mixed_shadow_g.reshape(h, w), mixed_shadow_b.reshape(h, w)))

def multiplyOverlay(mixed_shadow,base,ratio):
    final =  mixed_shadow*base//255
    return final*ratio+base*(1-ratio)

def shadowOutline(shadow,width):

    h, w, c = shadow.shape
    # copy a new shadow array
    outline = np.full((h,w,c),255)
    if width == 0:
        return outline

    # Normalization of shadow, make it value 0-255
    shadow_normalized = addContrast(shadow)/255

    # extract edge map
    edge = feature.canny(rgb2gray(shadow_normalized),sigma= 1.5,low_threshold = 0.5,high_threshold= 0.8).flatten()

    # extract orientation
    x_ori, y_ori = sobel_gradient(rgb2gray(shadow_normalized))

    x_ori = x_ori.flatten()[edge == True]
    y_ori = y_ori.flatten()[edge == True]


    # make x_ori, and y_ori descrete (0 ,-1 ,1)
    x_ori = np.sign(x_ori).astype(int)
    y_ori = np.sign(y_ori).astype(int)

    # color shadow edge

    x,y = np.meshgrid(np.arange(w),np.arange(h))
    x_edge = x.flatten()[edge== True]
    y_edge = y.flatten()[edge== True]

    outline[y_edge,x_edge,0] = 0
    outline[y_edge, x_edge, 1] = 0
    outline[y_edge, x_edge, 2] = 0

    for i in range(width-1):
        y_edge = np.where(np.logical_and((y_edge-y_ori)>= 0,(y_edge-y_ori)<h ),y_edge-y_ori,y_edge)
        x_edge = np.where(np.logical_and((x_edge - x_ori) >= 0, (x_edge - x_ori) < w), x_edge - x_ori, x_edge)
        outline[y_edge,x_edge,0] = 0
        outline[y_edge, x_edge, 1] = 0
        outline[y_edge, x_edge, 2] = 0
        # Intent to close the little gap between line, but not too much effective
        close_line(outline,x_edge,y_edge,0,0,0)

    return outline

############ ----------  HELPER FUNCTIONS ----------- ############
def sobel_gradient(gray_image):
    # Define custom 5x5 Sobel kernels
    sobel_kernel_x_5x5 = np.array([
        [-1, -2, 0, 2, 1],
        [-4, -8, 0, 8, 4],
        [-6, -12, 0, 12, 6],
        [-4, -8, 0, 8, 4],
        [-1, -2, 0, 2, 1]
    ]) / 48

    sobel_kernel_y_5x5 = np.array([
        [-1, -4, -6, -4, -1],
        [-2, -8, -12, -8, -2],
        [0, 0, 0, 0, 0],
        [2, 8, 12, 8, 2],
        [1, 4, 6, 4, 1]
    ]) / 48

    # Compute gradients along the x and y axes
    sobel_x = convolve(gray_image, sobel_kernel_x_5x5)
    sobel_y = convolve(gray_image, sobel_kernel_y_5x5)
    return sobel_x,sobel_y

def close_line(image,x_points,y_points,r,g,b):
    #gnerate a binary edge map
    edge = np.full((image.shape[0],image.shape[1]),0)
    edge[y_points,x_points] = 1
    edge = ndimage.binary_closing(edge)
    edge = edge.flatten()
    x,y = np.meshgrid(np.arange(image.shape[1]),np.arange(image.shape[0]))
    x = x.flatten()[edge== 1]
    y = y.flatten()[edge == 1]
    image[y,x,0] = r
    image[y,x,1] = g
    image[y,x,2] = b


############ ----------  DATA MANAGEMENT ----------- ############
def select_file():
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Open a file dialog and get the selected file's path
    file_path = filedialog.askopenfilenames()

    return file_path

def split_by_date(files):
    dates = {}
    for file in files:
        date = file.split("_")[1]
        if date not in dates:
            dates[date] = []
        dates[date].append(file)
    return dates

def get_site_context_pairs(file_names):
    times = {}
    # Construct times dictionary
    for file_name in file_names:
        time = file_name[-6:-4]
        if time not in times:
            times[time] = []
        times[time].append(file_name)

    # Sort the value of times dictionary
    for time, file_names_list in times.items():
        file_names_list = sorted(file_names_list, key=sort_by_type)
    return times

def sort_by_type(string):
    if 'context' in string:
        return 0
    elif 'site' in string:
        site_num = int(string.split('_')[0].split('/')[-1][4:])
        return site_num+1
    else:
        return 999

def request_color_input(pairs):
    first_pair = next(iter(pairs.values()))
    n = len(first_pair)-1
    i = 0
    colors=[]
    while(i< n):
        while(1):
            color = input("Input your site{} color in RGBA format, or press q to terminate\n".format(i))
            if re.match(r"^\d+\s+\d+\s+\d+$", color):
                lst = []
                col = color.split(" ")
                lst.append(int(col[0].strip()))
                lst.append(int(col[1].strip()))
                lst.append(int(col[2].strip()))
                colors.append(lst)
                break
            elif color.strip()=="q":
                print("Program terminated")
                exit(1)
            else:
                print("Wrong color format!")
        i+=1
    return colors

def assign_colors(pairs,color_palette):
    first_pair = next(iter(pairs.values()))
    n = len(first_pair)-1
    return color_palette[:n]


def __init__():
    files = list(select_file())
    base_file=None
    # get tbe base file
    for file in files:
        if re.search(r"base",file):
            base_file = file
            files.remove(file)
            break
    if base_file == None:
        raise ValueError
    else :
        base = np.array(Image.open(base_file).convert('RGB'))

    # get user input
    input = shadowStudyForm.TinkerForm()
    input.advanced_visible = False
    input.mainloop()

    # split the list by date
    dates = split_by_date(files)

    # Loop over the dates
    for date,file_names in dates.items():
        pairs = get_site_context_pairs(file_names)

        # Build each pari
        for time, file_names_List in pairs.items():
            context_shadow = np.array(Image.open(file_names_List[0]).convert('RGB'))
            mixed_shadow = None
            for i in range(1,len(file_names_List)):
                site_shadow = np.array(Image.open(file_names_List[i]).convert('RGB'))
                site_shadow = colorShadow(site_shadow,input.color_palette[i-1])
                if i == 1:
                    mixed_shadow = site_shadow
                else:
                    mixed_shadow,_ = shadowMix(site_shadow,mixed_shadow)


            # mix with context
            mixed_shadow,net_shadow = shadowMix(mixed_shadow, context_shadow)
            # mix with base
            res = lighter_shadow_on_roof(base,multiplyOverlay(mixed_shadow, base,input.shadow_multiply_ratio),input.roof_lighter_ratio)
            # get shadow outline
            site_shadow_outline = shadowOutline(net_shadow,input.width)
            # add outline
            res,_ = shadowMix(res,site_shadow_outline)

            res = res.astype(np.uint8)
            image = Image.fromarray(res,'RGB')
            # export file name

            export_file_name = "res/"+date + "_" + time + ".jpg"
            image.save(export_file_name)
            print(export_file_name," saved!!")


def test():
    shadow_multiply_ratio = 0.7
    roof_lighter_ratio = 0.5

    site1color = (203 ,51, 100)
    site2color = (255 ,221 ,21)
    site3color = (0,74,151)
    site4color = (204,112,40)
    site5color = (70,255,250)
    site6color = (90,170,255)
    site7color = (170,110,255)
    color_palette = [site1color,site2color,site3color,site4color,site5color,site6color,site7color]

    base = np.array(Image.open("exports/base.jpg").convert('RGB'))
    site_shadow = np.array(Image.open("exports/site4_September21st_1018.jpg").convert('RGB'))
    context_shadow = np.array(Image.open("exports/context_September21st_1018.jpg").convert('RGB'))
    site_shadow = colorShadow(site_shadow,(204,112,40))
    mixed_shadow = shadowMix(site_shadow, context_shadow)
    res = multiplyOverlay(mixed_shadow, base,0.5)
    res = lighter_shadow_on_roof(base,res,roof_lighter_ratio).astype(np.uint8)
    image = Image.fromarray(res, 'RGB')
    image.save("test/test.jpg")

    # site_shadow = np.array(Image.open("exports/site1_September21st_0002.jpg").convert('RGB'),'f')
    # site_shadow = colorShadow(site_shadow,(160,112,40))
    # shadowOutline(site_shadow,4)


__init__()
# test()

