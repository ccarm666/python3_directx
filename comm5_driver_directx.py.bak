#https://www.apriorit.com/dev-blog/615-qa-gui-testing-windows-python-pywinauto
#Nuitka compiler
import linecache
import sys
from pywinauto.application import Application
import pywinauto
import re 
import win32gui,win32process
#from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import socket
import subprocess
import os
import time
from PIL import Image,ImageGrab
import glob
cparm_file='C:\BCIHomeSystemFiles\VA_BCI2000\parms\communicator_directx_15.prm'
bci_prog_dir = 'C:\BCIHomeSystemFiles\VA_BCI2000\prog\\'
bci_parm_dir = 'C:\BCIHomeSystemFiles\VA_BCI2000\parms\\'
proc_source=None
proc_P3SignalProcessing=None
proc_P3Speller=None
proc_operat = None
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
#offset_x=1600-150
#offset_y=900-160

def collect_weights():
    matrix_xoff=int(scalex*20);
    matrix_yoff=int(scaley*150);
    xdelta=int(scalex*152);
    ydelta=int(scaley*140);
    im = Image.open("tobii_alpha_1600x900.jpg")
    imrs = im.resize((int(scalex*1059),int(scaley*700)))
    imrs.save("tobii_alphabet_scaled.png")
    width, height = imrs.size
    print ("width is",width, " and height is",height)
    curr_desktop=os.environ['USERPROFILE'] + '\Desktop'
    process_st=subprocess.Popen(['..\python3\Release\SpriteWithTimer.exe',  'tobii_alphabet_scaled.png',str(width),str(height)])
    time.sleep(1)
#    update_display_new_page("tobii_alphabet_scaled.png",width,height) 
    dx_app = Application().connect(process=process_st.pid)
#    time.sleep(1)
    for i in range(0,28):
      row=int(i/7);
      col=(i % 7);
      msg="Alter_coordxy," + str(i+1) + "," + str(col*xdelta+matrix_xoff) + "," + str(row*ydelta+matrix_yoff)
      netv_send(msg)
    dx_app.top_window().set_focus()
    start_bci2000("weights_directx_28.prm")
    dx_app.top_window().set_focus()
    exit(1)
    
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

def get_window_pid(wclass):
    hwnd = win32gui.FindWindow(wclass, None)
    threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid

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

def wait_move_window(wclass_name,xpos,ypos):
  count=30
  not_found=True
  while(bool(not_found)):  
    hnd=win32gui.FindWindow(wclass_name,None)
    if(hnd != 0):
      not_found=False
      crwm = win32gui.GetClientRect(hnd)
      win32gui.MoveWindow(hnd,xpos,ypos,crwm[2]-crwm[0], crwm[3]-crwm[1],True) 
      return(hnd)
    count-=count
    time.sleep(1)
    if(count == 0):
      break
  return(None)
  
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


def start_bci2000(parm_file):
  global weights_mode      
# os.system("launch_operat.bat " + parm_file)
  if(weights_mode):
    proc_operat = subprocess.Popen('''C:\BCIHomeSystemFiles\VA_BCI2000\prog\operat.exe --OnConnect "-LOAD PARAMETERFILE ''' + parm_file + ''';SETCONFIG" --OnSuspend "-QUIT" --OnSetConfig "-SET STATE Running 1"''')
  else:
    proc_operat = subprocess.Popen('''C:\BCIHomeSystemFiles\VA_BCI2000\prog\operat.exe --OnConnect "-LOAD PARAMETERFILE ''' + parm_file + ''';SETCONFIG" --OnSuspend "-QUIT" --OnSetConfig "-SET STATE Running 1"'''
, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)  
  proc_source=subprocess.Popen([bci_prog_dir + "SignalGenerator.exe"," 127.0.0.1"])
#  proc_source=subprocess.Popen([bci_prog_dir + "gUSBampSource.exe"," 127.0.0.1"])
  print("proc_source.pid=",proc_source.pid)
  proc_P3SignalProcessing=subprocess.Popen([bci_prog_dir + "P3SignalProcessing.exe"," 127.0.0.1"])
  print("proc_P3Speller.pid=",proc_P3SignalProcessing.pid)
  proc_P3Speller=subprocess.Popen([bci_prog_dir + "P3Speller.exe"," 127.0.0.1"])
#  time.sleep(1)
  wait_move_window("TDisplayForm",-2200,0)  
  wait_move_window("TVisGraphForm",-1400,0)
  wait_move_window("TVisForm",-1500,0)
  wait_move_window("TForm",-1450,0)
#  time.sleep()
#  kill_bci2000()
# exit()


def get_closest_parm(number_of_buttons):
  file_list=glob.glob("communicator_directx_*.prm")
  found = False
  filename = None
  result   = 10000000    # a large number
  for f in file_list:
    match = re.search('_(\d+)\.prm$', str(f))
    if match :  
       print(f)
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
  netv_socket.sendto(netv_msg.encode(),(netv_udp_ip, netv_udp_port))

def find_closest_button(c_buttons,bx,by): # return index of the closest button starts at zero
  smallest = 1000000000 #a large number
  found=False  
  for i in range(len(c_buttons)):    
    bleft=getattr(c_buttons[i].element_info.rectangle, 'left')-offset_x
    bright=getattr(c_buttons[i].element_info.rectangle, 'right')-offset_x
    btop=getattr(c_buttons[i].element_info.rectangle, 'top')-offset_y
    bbottom=getattr(c_buttons[i].element_info.rectangle, 'bottom')-offset_y
    cntr_x=int((bleft + bright)/2)
    cntr_y=int((btop + bbottom)/2)
    if((bx > bleft) and (bx < bright) and (by > btop) and (by < bbottom)):
      found=True
      cur_distance = ((cntr_x-bx)*(cntr_x-bx)) + ((cntr_y-by)*(cntr_y-by))
      if(cur_distance < smallest):
        smallest=cur_distance
        cur_close=i
  if(found):
    return(cur_close)
  else:
    return(-1)

def get_selection(comm5_buttons):
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
#      print ("received message:", curr_selection)
      if (bool( re.match('.*mouse\sat.*',str(curr_selection)))):
        print (curr_selection)
        match = re.search('.*mouse\sat\sx=(\d+)\sand\sy=(\d+).*',str(curr_selection))
        x=match.group(1)
        y=match.group(2)
#        print ("Directx mouse at ",x," and ",y)
        closest_button=find_closest_button(comm5_buttons,int(x),int(y))
        print("closest button is ",closest_button)
        return(closest_button)
      if(bool(re.match('(.*PhaseInSequence\s+3.*)',str(curr_selection)))):
        p3=1
      elif ((p3==1) and (bool(re.match('.*SelectedTarget.*',str(curr_selection)))) 
      and not (bool(re.match('.*SelectedTarget\s0.*',str(curr_selection)))) 
      and not selection_found):
        id=re.search('.*SelectedTarget\s(\d+).*',str(curr_selection))
        print("selection was ",int(id.group(1))-1)
        return int(id.group(1))-1
      elif (bool(re.match('(.*PhaseInSequence\s+2.*)',str(curr_selection)))):
        selection_found = False
        p3=0
      elif (bool(re.match('(.*PhaseInSequence\s+1.*)',str(curr_selection)))): 
        selection_found = False
        p3=0
 
def update_netv_coords(comm5_buttons):
  netv_send("Reset_coordxy")
  for i in range(len(comm5_buttons)): 
    bleft=getattr(comm5_buttons[i].element_info.rectangle, 'left')
    bright=getattr(comm5_buttons[i].element_info.rectangle, 'right')
    btop=getattr(comm5_buttons[i].element_info.rectangle, 'top')
    bbottom=getattr(comm5_buttons[i].element_info.rectangle, 'bottom')
    face_x=int((bleft + bright)/2 - (face_width/2))-offset_x
    face_y=int((btop + bbottom)/2 - (face_width*1.3/2))-offset_y
    msg="Alter_coordxy," + str(i+1) + "," + str(face_x) + "," + str(face_y)
    netv_send(msg)
#    print(msg)       



def update_display_new_page(mypng,xsize,ysize):
#  msg="Change_background_texture,mycomm.png" + "," + str(xsize) + "," + str(ysize)
  msg="Change_background_texture,"+ mypng + "," + "," + str(xsize) + "," + str(ysize)
  netv_send(msg)
  time.sleep(1)

def kill_bci2000(): 
  os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})  
  os.system('''c:\\BCIHomeSystemFiles\\BCIAddons\\bin\\UDPSend.exe 127.0.0.1 20321 "Running 0"''')  
  print("tried to kill operat")
  os.system("taskkill /f /im SignalGenerator.exe")
  os.system("taskkill /f /im P3SignalProcessing.exe")
  os.system("taskkill /f /im P3Speller.exe")
  os.environ.update({"__COMPAT_LAYER":""})

def killall():
  os.system("taskkill /f /im Communicator.exe")
  os.system("taskkill /f /im SpriteWithTimer.exe")
  kill_bci2000()

def kill_bci2000_directx():
  os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})
  kill_bci2000()
  os.system("taskkill /f /im SpriteWithTimer.exe")
  os.environ.update({"__COMPAT_LAYER":""})

def resize_faces(widthinpixels):
   for j in range(1, 7):
     fname= "face" + str(j)
     imrs=Image.open(fname + '''_org.png''')
     new_imrs=imrs.resize((widthinpixels,int(get_aspect(fname + '''_org.png''')*widthinpixels)))
     new_imrs.save(fname + '''.png''',"PNG")
  
   
   
def get_aspect(filename):
  imga = Image.open(filename)
  twidth, theight = imga.size
  return(theight/twidth)
  
  
from win32api import GetSystemMetrics
mon_width = GetSystemMetrics(0)
mon_height = GetSystemMetrics(1)
scalex=mon_width/1600
scaley=mon_height/900
width=mon_width
height=mon_height
offset_x=int(width-150*mon_width/1600)
offset_y=int(height-160*mon_height/900)
print(width,height)
face_width=int(100*(width/1600)) # scaled so it is 100 pixel for 1600x900 display
resize_faces(face_width)
cparm_file='C:\\Users\\steve\\Desktop\\python3\\communicator_directx_15.prm'
weights_mode=False
if(len(sys.argv) > 1):
  print(len(sys.argv)-1," arguments")
  weights_mode=True
  collect_weights()
  exit(1)


os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})
os.system("taskkill /f /im communicator.exe")
#killall()
time.sleep(1) #sleep to allow communicator.exe to exit if it has been terminated 
process = subprocess.Popen(['C:\Program Files (x86)\Tobii Dynavox\Communicator 5\communicator.exe'])
print("communicator process pid is ",process.pid)
os.environ.update({"__COMPAT_LAYER":""})
while not start_page_active():
 time.sleep(1)
while start_page_active():
  time.sleep(1)	  
time.sleep(1)
while start_page_active():
  time.sleep(1)	
  
app = Application(backend="uia").connect(title_re=".*Communicator.*")
first_time = True

try:
 while True:
  hdle=win32gui.FindWindow("TOBIICOMMUNICATOR5",None)
  if(first_time == False):
     win32gui.MoveWindow(hdle,0,0,mon_width,mon_height,True) 
  if(hdle == 0):
    break  
  print("handle is ",hdle)
  time.sleep(1)
  cr = win32gui.GetClientRect(hdle)
  im = ImageGrab.grab()
  im.save("mycomm.png")
#  time.sleep(1)
  if(first_time):
    process_st=subprocess.Popen(['.\Release\SpriteWithTimer.exe',  'mycomm.png',str(width),str(height)])
    first_time = False
    dx_app = Application().connect(process=process_st.pid)
  else:
    update_display_new_page("mycomm.png",width,height) 
  dx_app.top_window().set_focus()
  win32gui.MoveWindow(hdle,offset_x,offset_y,cr[2]-cr[0], cr[3]-cr[1],True) 
  main_dlg = app.window(title_re=".*Communicator.*")
  old_page= win32gui.FindWindow("TOBIICOMMUNICATOR5",None)
  old_page_text=win32gui.GetWindowText(old_page)
  buttons=main_dlg.descendants(control_type='Button')
  the_buttons = get_buttons()
  update_netv_coords(the_buttons)
  start_bci2000(get_closest_parm(len(the_buttons)))
  dx_app.top_window().set_focus()
  sel=get_selection(the_buttons)
#  time.sleep(300)
  kill_bci2000()
  if((sel > -1) and (sel < (len(the_buttons)))):
    hdle=win32gui.FindWindow("TOBIICOMMUNICATOR5",None)
    time.sleep(1)
    the_buttons[int(sel)].click() 
#    time.sleep(1)
except Exception as e:
 PrintException()
 print("in exception")
 killall()
 exit() 