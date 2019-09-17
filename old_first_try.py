#https://www.apriorit.com/dev-blog/615-qa-gui-testing-windows-python-pywinauto
#Nuitka compiler
from pywinauto.application import Application
import pywinauto
import re 
import win32gui
import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import socket
import subprocess
import os
import time
from PIL import Image
from PIL import ImageGrab
import glob
cparm_file='C:\BCIHomeSystemFiles\VA_BCI2000\parms\communicator_directx_15.prm'
bci_prog_dir = 'C:\BCIHomeSystemFiles\VA_BCI2000\prog\\'
bci_parm_dir = 'C:\\BCIHomeSystemFiles\\VA_BCI2000\\parms\\'
proc_source=None
proc_P3SignalProcessing=None
proc_P3Speller=None
bci2000_port_read = 20320 #
netv_udp_ip = "127.0.0.1"
netv_udp_port = 12000
netv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#Create a UDP socket
#clientSocket = socket(AF_INET, SOCK_DGRAM)
#Set a timeout value of 1 second
#clientSocket.settimeout(1)
#Ping to server
message = 'test'
offset_x=1600-150
offset_y=900-160
def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

def start_page_active():
   while True:
      try:
         start_hdle=pywinauto.findwindows.find_windows(title_re = '.*Page\s+Set.*', class_name='TOBIICOMMUNICATOR5')[0]
         print("found window", start_hdle)
         time.sleep(1)
         return True
      except (Exception) as e: 
         print ("didnt find Page set window")   
         time.sleep(1)
         return False
old_page_text="";

def page_change():
  global old_page_text
  curr_page = win32gui.FindWindow("TOBIICOMMUNICATOR5",None)
  curr_page_text=win32gui.GetWindowText(curr_page)
  print("curr_page_text is ",curr_page_text, " and old_page_text is ",old_page_text)
  if(curr_page_text == old_page_text):
    return False   
  else:
    old_page_text = curr_page_text;
    return True


def start_bci2000(cparm_file):  
  os.system("launch_operat.bat " + cparm_file)
  proc_source=subprocess.Popen([bci_prog_dir + "SignalGenerator.exe"," 127.0.0.1"])
  print("proc_source.pid=",proc_source.pid)
  proc_P3SignalProcessing=subprocess.Popen([bci_prog_dir + "P3SignalProcessing.exe"," 127.0.0.1"])
  print("proc_P3Speller.pid=",proc_P3SignalProcessing.pid)
  proc_P3Speller=subprocess.Popen([bci_prog_dir + "P3Speller.exe"," 127.0.0.1"])
  time.sleep(1)
#  exit()

def kill_bci2000():    
  os.system("taskkill /f /im SignalGenerator.exe")
  os.system("taskkill /f /im P3SignalProcessing.exe")
  os.system("taskkill /f /im P3Speller.exe")
  os.system('c:\\BCIHomeSystemFiles\\BCIAddons\\bin\\UDPSend.exe 127.0.0.1 20321 "Running 0"')
  os.system("taskkill /f /im operat.exe")
  
def get_closest_parm(number_of_buttons):
  file_list=glob.glob(bci_parm_dir + "communicator_directx_*.prm")
  found = False
  filename = None
  result   = 10000000    # a large number
  for f in file_list:
    match = re.search('_(\d+)\.prm$', str(f))
    if match :  
#      print(f)
       num = int(match.group(1))
       if (num >= int(number_of_buttons)) and ( num < result ):
         found = True
         result = num
         filename = f
  return filename

def get_buttons():
  buttons=main_dlg.descendants(control_type='Button')
  my_buttons=[]
  for btn in buttons:
    if (bool(re.match('(Minimize|Maximize|Close)',str(btn.element_info.name)))): 
      pass
    else:	
      my_buttons.append(btn)
  print(len(my_buttons))
  print(len(buttons))
#  for btn in my_buttons:
#    print(btn.element_info.rectangle,btn.element_info.name) 
  return(my_buttons)

def netv_send(netv_msg):
  netv_socket.sendto(netv_msg.encode(), (netv_udp_ip, netv_udp_port))

def find_closest_button(c_buttons,bx,by): # return index of the closest button starts at zero
  print("bx=",bx," by=",by)
  smallest = 1000000000 #a large number
  found=False
  for i in range(len(c_buttons)):
    bleft=getattr(c_buttons[i].element_info.rectangle, 'left')
    bright=getattr(c_buttons[i].element_info.rectangle, 'right')
    btop=getattr(c_buttons[i].element_info.rectangle, 'top')
    bbottom=getattr(c_buttons[i].element_info.rectangle, 'bottom')
    cntr_x=int((bleft + bright)/2)
    cntr_y=int((btop + bbottom)/2)
    print(bleft,bright,btop,bbottom)
    if((bx > bleft) and (bx < bright) and (by > btop) and (by < bbottom)):
      found=True
      print("found a button close")
      cur_distance = ((cntr_x-bx)*(cntr_x-bx)) + ((cntr_y-by)*(cntr_y-by))
      if(cur_distance < smallest):
        smallest=cur_distance
        cur_close=i
  if(found):
    return(cur_close)
  else:
    return(-1)

def get_selection(c_buttons):
  sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
  sock.bind(("127.0.0.1", bci2000_port_read))
  poll_cnt=0
  p3=0
  selection_found = False
  while True:
    poll_cnt+=1
    if poll_cnt == 750:
      poll_cnt = 0
      curr_selection, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
      print ("received message:", curr_selection)
      if (bool( re.match('.*mouse\sat.*',str(curr_selection)))):
        print (curr_selection)
        match = re.search('.*mouse\sat\sx=(\d+)\sand\sy=(\d+).*',str(curr_selection))
        x=match.group(1)
        y=match.group(2)
        print ("Directx mouse at ",x," and ",y)
        closest_button=find_closest_button(c_buttons,int(x),int(y))
        print("closest button is ",closest_button)
#        killall()
        return(closest_button)
      if(bool(re.match('(.*PhaseInSequence\s+3.*)',str(curr_selection)))):
        p3=1
      elif ((p3==1) and (bool(re.match('.*SelectedTarget.*',str(curr_selection)))) 
      and not (bool(re.match('.*SelectedTarget\s0.*',str(curr_selection)))) 
      and not selection_found):
        id=re.search('.*SelectedTarget\s(\d+).*',str(curr_selection))
        print("selection was ",int(id.group(1))-1)
#        killall()
        return int(id.group(1))-1
      elif (bool(re.match('(.*PhaseInSequence\s+2.*)',str(curr_selection)))):
        selection_found = False
        p3=0
      elif (bool(re.match('(.*PhaseInSequence\s+1.*)',str(curr_selection)))): 
        selection_found = False
        p3=0
 
def update_netv_coords(comm5_buttons):
  for i in range(len(comm5_buttons)): 
    bleft=getattr(comm5_buttons[i].element_info.rectangle, 'left')
    bright=getattr(comm5_buttons[i].element_info.rectangle, 'right')
    btop=getattr(comm5_buttons[i].element_info.rectangle, 'top')
    bbottom=getattr(comm5_buttons[i].element_info.rectangle, 'bottom')
    face_x=int((bleft + bright)/2 - 20)
    face_y=int((btop + bbottom)/2 - 5)
    msg="Alter_coordxy," + str(i+1) + "," + str(face_x) + "," + str(face_y)
    netv_send(msg)
    print(msg)



def update_display_new_page(mypng):
  msg="Change_background_texture,mycomm.png"
  netv_send(msg)

def killall():
  kill_bci2000()
  os.system("taskkill /f /im Communicator.exe")
  os.system("taskkill /f /im SpriteWithTimer.exe")
  
cparm_file='C:\\Users\\steve\\Desktop\\python3\\communicator_directx_15.prm'
#start_bci2000(cparm_file)  
#time.sleep(5)
#kill_bci2000() 
#print ("filename is ",get_closest_parm(,bci_parm_dir))
#exit()
#get around UAC problems
#kill_bci2000()
#start_bci2000(cparm_file)
#get_selection()
#kill_bci2000()
#exit()

os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})
os.system("taskkill /f /im communicator.exe")
time.sleep(1) #sleep to allow communicator.exe to exit if it has been terminated 
process = subprocess.Popen(['C:\Program Files (x86)\Tobii Dynavox\Communicator 5\communicator.exe'])
print("communicator process pid is ",process.pid)
while not start_page_active():
 time.sleep(1)
while start_page_active():
  time.sleep(1)	  
time.sleep(1)
app = Application(backend="uia").connect(title_re=".*Communicator.*")
#app.wait('visible', timeout=20)
hdle=win32gui.FindWindow("TOBIICOMMUNICATOR5",None)
im = ImageGrab.grab()
width, height = im.size
time.sleep(1)
im.save("mycomm.png")
time.sleep(1)
process_st=subprocess.Popen(['..\directx\Release\SpriteWithTimer.exe',  'mycomm.png',str(width),str(height)])
Sp_hdle=win32gui.FindWindow("SpriteUpdateWithTimer",None)
#time.sleep(20)
dx_app = Application().connect(process=process_st.pid)
while True:
  hdle=win32gui.FindWindow("TOBIICOMMUNICATOR5",None)
  if(hdle == 0):
    print("cant find TOBIICOMMUNICATOR5")
    break  
  print("handle is ",hdle)
  win32gui.SetForegroundWindow(hdle)
  cr = win32gui.GetClientRect(hdle)
  im = ImageGrab.grab()
  width, height = im.size
  offset_x=width-150
  offset_y=height-160
  print(width,height)
  im.save("mycomm.png")
  time.sleep(1)
  win32gui.SetForegroundWindow(Sp_hdle)
  time.sleep(5)
  update_display_new_page("mycomm.png") 
  main_dlg = app.window(title_re=".*Communicator.*")
  old_page= win32gui.FindWindow("TOBIICOMMUNICATOR5",None)
  old_page_text=win32gui.GetWindowText(old_page)
  the_buttons = get_buttons()
#  update_netv_coords(the_buttons)
  time.sleep(30)
#  exit()
#  win32gui.MoveWindow(hdle,offset_x,offset_y,cr[2]-cr[0], cr[3]-cr[1],True)
  update_netv_coords(the_buttons)
#  dx_app.top_window().set_focus()
#des=main_dlg.descendants()
#  buttons=main_dlg.descendants(control_type='Button')
  
#my_buttons=[]
#for btn in buttons:
#  if (bool(re.match('(Minimize|Maximize|Close)',str(btn.element_info.name)))): 
#   pass
#  else:	
#   my_buttons.append(btn)
#print(len(my_buttons))
#print(len(buttons))
 # the_buttons = get_buttons()
 # update_netv_coords(the_buttons)
#print("the buttons is ",len(the_buttons)," long")

#for btn in the_buttons:
# print(btn.element_info.rectangle,btn.element_info.name)
# for side in ("top", "left", "right", "bottom"):
#            sideValue = getattr(btn.element_info.rectangle, side)
#            print(sideValue)
#if page_change():
#  print ("page_changed")
#the_buttons[1].click() 
#time.sleep(3)
#if page_change():
#  print ("page_changed")
#  the_buttons = get_buttons()
# for btn in the_buttons:
#    print(btn.element_info.rectangle,btn.element_info.name)
#exit()
#os.system('..\\directx\\Release\\SpriteWithTimer.exe ' + 'mycomm.png ' + str(width) + " " + str(height))
#dx_process = subprocess.Popen(['..\\directx\\Release\\SpriteWithTimer.exe','mycomm.png',str(width),str(height)])
  start_bci2000(get_closest_parm(len(the_buttons)))
 
#while(dx_app.is_process_running()):

  sel=get_selection(the_buttons)
  kill_bci2000
  if((sel > 0) and (sel <= (len(the_buttons)))):
#    hdle=win32gui.FindWindow("TOBIICOMMUNICATOR5",None)
#    win32gui.MoveWindow(hdle,0,0,cr[2]-cr[0], cr[3]-cr[1],True) 
    time.sleep(1)
    the_buttons[int(sel)].click() 
    time.sleep(1)
killall()
exit() 