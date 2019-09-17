from PIL import ImageGrab
import win32gui
import time
toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

comm = [(hwnd, title) for hwnd, title in winlist if 'communicator' in title.lower()]
# just grab the hwnd for first window matching firefox
comm = comm[0]
hwnd = comm[0]

win32gui.SetForegroundWindow(hwnd)
bbox = win32gui.GetWindowRect(hwnd)
print(bbox)
img = ImageGrab.grab(bbox)
img.save("comm.png")
