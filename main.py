import numpy as np
# import scipy.sparse
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
# from scipy import signal
import tkinter as tk
from tkinter import filedialog
import re
import shadowStudyForm


# color_palette = [site1color,site2color,site3color,site4color,site5color,site6color,site7color]
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

    mixed_shadow = np.dstack(
        (mixed_shadow_r.reshape(h, w), mixed_shadow_g.reshape(h, w), mixed_shadow_b.reshape(h, w)))

    return mixed_shadow


def addContrast(image):
    """To be implement later"""


def colorShadow(site_shadow,color):

    h, w, c = site_shadow.shape

    site_shadow_r = site_shadow[:, :, 0].flatten()
    site_shadow_g = site_shadow[:, :, 1].flatten()
    site_shadow_b = site_shadow[:, :, 2].flatten()

    mixed_shadow_r = np.where(np.logical_or(site_shadow_r < 200,np.logical_or(site_shadow_g < 200,site_shadow_b < 200)), color[0], 255)
    mixed_shadow_g = np.where(np.logical_or(site_shadow_r < 200,np.logical_or(site_shadow_g < 200,site_shadow_b < 200)), color[1], 255)
    mixed_shadow_b = np.where(np.logical_or(site_shadow_r < 200,np.logical_or(site_shadow_g < 200,site_shadow_b < 200)), color[2], 255)

    return np.dstack((mixed_shadow_r.reshape(h, w), mixed_shadow_g.reshape(h, w), mixed_shadow_b.reshape(h, w)))

def multiplyOverlay(mixed_shadow,base,ratio):
    final =  mixed_shadow*base//255
    return final*ratio+base*(1-ratio)

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
            mixed_shadow = context_shadow
            for i in range(1,len(file_names_List)):
                site_shadow = np.array(Image.open(file_names_List[i]).convert('RGB'))
                site_shadow = colorShadow(site_shadow,input.color_palette[i-1])
                mixed_shadow = shadowMix(site_shadow, mixed_shadow)


            res = lighter_shadow_on_roof(base,multiplyOverlay(mixed_shadow, base,input.shadow_multiply_ratio),input.roof_lighter_ratio).astype(np.uint8)
            image = Image.fromarray(res,'RGB')
            # export file name

            export_file_name = "res/"+date + "_" + time + ".jpg"
            image.save(export_file_name)
            print(export_file_name," saved!!")


def test():
    shadow_multiply_ratio = 0.7
    roof_lighter_ratio = 0.5

    # Applicant Proposal
    # (204,112,40)
    # Under Construction
    # (108,130,166)
    # City Planner Proposed
    # (0,74,151)
    # Approved/ Not yet Constructed
    # (0,152,146)
    # As of Right
    # (203 ,51, 100)
    # Alternate Colour for use
    # (255 ,221 ,21)
    # Heritage
    # (189 ,181, 141)
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



__init__()
# test()