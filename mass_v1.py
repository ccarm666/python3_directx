import win32gui
from ctypes import oledll
from ctypes import byref

#installed by easy_install comtypes
from comtypes import POINTER
from comtypes.automation import IDispatch
import comtypes.client.dynamic as comDy
import time
#obtain hwnd of application
time.sleep(10)
hwnd = win32gui.FindWindow(None, "Notepad")
#hwnd = win32gui.FindWindow("Communicator5",None)

def winfun(hwnd, lparam):
    allHwnd.append(hwnd)
#naughty global variable
allHwnd = []
#call winfun to populate allHwnd with all the child hwnds
win32gui.EnumChildWindows(hwnd, winfun, None)

for childHwnd in allHwnd:
    OBJID_NATIVEOM = -16
    p = POINTER(IDispatch)()
    try:
        oledll.oleacc.AccessibleObjectFromWindow(childHwnd, OBJID_NATIVEOM, byref(IDispatch._iid_), byref(p))
        window = comDy.Dispatch(p)
        CATIA = window.application
        print('winner winner hwnd: '+str(childHwnd))
        print(CATIA)
    except:
        print('No dice')
#lots of 'No dice' printed with one successful COMObject when the application is Word or Excel.
#only lots of 'No Dice' when running on everything else
