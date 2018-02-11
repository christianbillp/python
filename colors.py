#%% Import libraries
import numpy as np
import PIL.Image

#%% Load image, resize and convert to grayscale

# Set resize height
width = 200
height = 200

# Set list of mask picture names
masks = ['mask1.png', 'mask2.png']

# Set source image filename
source = 'colors.png'

# Load source image, convert to grayscale and resize 
im = np.array(PIL.Image.open(source).convert('LA').resize((width, height), PIL.Image.ANTIALIAS) )[:,:,0]

results = []
for maskfile in masks:
    mask = np.array(PIL.Image.open(maskfile).convert('LA').resize((width, height), PIL.Image.ANTIALIAS))[:,:,0]
    mask[mask > 0] = 1      # Set all positive mask values to 1    
    maskeddata = im * mask  # Apply mask by multiplying arrays
    results.append(np.mean([int(i) for row in maskeddata for i in row if i != 0]))


for i, result in enumerate(results):
    print("Mean value for '{}': {}".format(masks[i], result))

