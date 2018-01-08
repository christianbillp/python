#%%
import win32api, win32con
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


#%%
import pyautogui
import time

def go_back():
    click(2316, 12)

def get_position():
    pyautogui.position()

def buy_wire():
    click(99, 586)

def buy_auto_clipper():
    click(115, 640)

def make_paperclip():
    click(122,257)

def run_tour():
    click(734, 633)
    click(901, 500)
    go_back()

def compute():
    click(391, 506)

#%%
for _ in range(1000):
    compute()
go_back()
#%%
for _ in range(10):
    buy_wire()
go_back()

#%%
for _ in range(2000):
    make_paperclip()
#    time.sleep(0.0005)

go_back()
#%%
for _ in range(10):
    buy_auto_clipper()
go_back()
#%%
import pyscreenshot as ImageGrab




#%%
from PIL import Image
import pytesseract
import re
im = ImageGrab.grab(bbox = (77,200, 353,535)) # X1,Y1,X2,Y2
im.save('screenshot.png')

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

result = pytesseract.image_to_string(Image.open('screenshot.png'))

#%%
m = re.findall(r'\d+', result)
paperclips = (''.join([m[0],m[1],m[2]]).strip('\n'))
funds = (''.join([m[4],m[5]]).strip('\n'))

print(paperclips)
print(funds)





