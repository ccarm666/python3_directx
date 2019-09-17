import subprocess
import os
import time
import re
bci_prog_dir = 'C:\\BCIHomeSystemFiles\\VA_BCI2000\\prog\\'
cparm_file='C:\\BCIHomeSystemFiles\\VA_BCI2000\\parms\\communicator_directx_15.prm'
def start_bci2000(cparm_file):
  print(bci_prog_dir + "operat.exe")
  print(' --OnConnect' + '"-LOAD PARAMETERFILE ' +  cparm_file + ';SETCONFIG"')
  print(' --OnSuspend "-QUIT"')
  print(' --OnSetConfig \"-SET STATE Running 1\"')
  oper_prog_str=bci_prog_dir + "operat.exe"
  oper_connect_str=' --OnConnect' + '" -LOAD PARAMETERFILE' +  cparm_file + ';SETCONFIG"'
  oper_suspend_str=' --OnSuspend " -QUIT"'
  oper_setconfig_str=' --OnSetConfig " -SET STATE Running 1"'
  args=oper_connect_str+oper_suspend_str+oper_setconfig_str
  print("args is",args)
  print(oper_prog_str,oper_connect_str,oper_suspend_str,oper_setconfig_str)
  #proc_operat=subprocess.Popen([oper_prog_str,oper_connect_str,oper_suspend_str,oper_setconfig_str])
  #proc_operat=subprocess.Popen([oper_prog_str,oper_connect_str])
  #proc_operat=subprocess.Popen([oper_prog_str,])
 # print("proc_operat.pid=",proc_operat.pid) 
  proc_operat=subprocess.Popen([re.escape('C:\BCIHomeSystemFiles\VA_BCI2000\prog\operat.exe'), re.escape(' --OnConnect "-LOAD PARAMETERFILE C:\BCIHomeSystemFiles\VA_BCI2000\parms\communicator_directx_28.prm;SETCONFIG"')])
 #os.system('C:\BCIHomeSystemFiles\VA_BCI2000\prog\operat.exe --OnConnect "-LOAD PARAMETERFILE C:\BCIHomeSystemFiles\VA_BCI2000\parms\communicator_directx_28.prm;SETCONFIG"')
 # os.system(P3Speller_SigGen.bat')
 #  prog=C:\BCIHomeSystemFiles\VA_BCI2000\prog\operat.exe   progArgs=C:\BCIHomeSystemFiles\VA_BCI2000\prog\operate.exe --OnConnect "-LOAD PARAMETERFILE C:\BCIHomeSystemFiles\VA_BCI2000\parms\communicator_directx_15.prm;SETCONFIG"  --OnSuspend "-QUIT"  --OnSetConfig "-SET STATE Running 1"  progDir= C:\BCIHomeSystemFiles\VA_BCI2000\prog\
#$proc_source = mySystem($bci_prog_dir . 'SignalGenerator.exe',$bci_prog_dir . 'SignalGenerator.exe' . '127.0.0.1',$bci_prog_dir);
  proc_source=subprocess.Popen([bci_prog_dir + "SignalGenerator.exe"," 127.0.0.1"])
  print("proc_source.pid=",proc_source.pid)
#  $proc_P3SignalProcessing = mySystem($bci_prog_dir . 'P3SignalProcessing.exe',$bci_prog_dir . 'P3SignalProcessing.exe' . '127.0.0.1',$bci_prog_dir);
  proc_P3SignalProcessing=subprocess.Popen([bci_prog_dir + "P3SignalProcessing.exe"," 127.0.0.1"])
  print("proc_P3Speller.pid=",proc_P3SignalProcessing.pid)
  # # proc_operat = subprocess.Popen([(bci_prog_dir + 'operat.exe',"--OnConnect \"-LOAD PARAMETERFILE ",  cparm_file + \";SETCONFIG\ ",  "--OnSuspend ", \""-QUIT"\ ", "--OnSetConfig ","\"-SET STATE Running 1\"",$bci_prog_dir])
#$proc_P3Speller = mySystem($bci_prog_dir . 'P3Speller.exe',$bci_prog_dir . 'P3Speller.exe' . ' 127.0.0.1',$bci_prog_dir);
  proc_P3Speller=subprocess.Popen([bci_prog_dir + "P3Speller.exe"," 127.0.0.1"])
  time.sleep(10)
  exit()

start_bci2000(cparm_file)  