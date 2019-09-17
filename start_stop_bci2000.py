import os
import time
import win32gui
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

def start_bci2000(parm_file):  
  os.system("launch_operat.bat " + parm_file)
#  proc_source=subprocess.Popen([bci_prog_dir + "SignalGenerator.exe"," 127.0.0.1"])
#  print("proc_source.pid=",proc_source.pid)
#  proc_P3SignalProcessing=subprocess.Popen([bci_prog_dir + "P3SignalProcessing.exe"," 127.0.0.1"])
#  print("proc_P3Speller.pid=",proc_P3SignalProcessing.pid)
#  proc_P3Speller=subprocess.Popen([bci_prog_dir + "P3Speller.exe"," 127.0.0.1"])
  time.sleep(1)
  if(wait_move_window('OPER',-1200,0) == 0):
    print ("could not mover oper")
  wait_move_window("TVisGraphForm",-1400,0)
  wait_move_window("TVisForm",-1500,0)
  wait_move_window("TForm",-1450,0)
#  exit()

def kill_bci2000():
  os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})
  os.system("taskkill /f /im operat.exe")
  print("tried to kill operat")
  os.system('C:\\Users\\steve\\Desktop\\python3\\killbci2000.bat')  
  os.system("taskkill /f /im SignalGenerator.exe")
  os.system("taskkill /f /im P3SignalProcessing.exe")
  os.system("taskkill /f /im P3Speller.exe")
  print("about send udp to kill oper")
  time.sleep(2)
  os.system('c:\\BCIHomeSystemFiles\\BCIAddons\\bin\\UDPSend.exe 127.0.0.1 20321 "Running 0"')
  print("just sent udp")
  os.system("taskkill /f /im operat.exe")
  os.environ.update({"__COMPAT_LAYER":""})

cparm_file='C:\\Users\\steve\\Desktop\\python3\\communicator_directx_15.prm'
start_bci2000(cparm_file)  
time.sleep(10)
kill_bci2000() 