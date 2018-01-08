# %%
import win32api, win32con
import pyautogui
import time


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)# -*- coding: utf-8 -*-

def go_back():
    click(2316, 12)

def get_position():
    pyautogui.position()

#%%
for _ in range(1000):
    click(972, 503)
go_back()

