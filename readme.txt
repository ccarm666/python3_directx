In this readme find for hardware and software requirements; and directions for: collecting calibration data; developing and loading calibration coefficients, and running the TD Communicator5 program

1. hardware and software requirements
monitor 1 is the smaller
monitor 2 is the larger
monitor 2 is to the left of monitor 1 and monitor 1 is set as the main display (check by right clicking on desktop and then clicking on "display settings")
the main monitor must be 1600x900

c:\users\bci\desktop\python3\weights_directx_28.prm or any 28 character parm with just numbers

2. collecting Calibration data
To develop weights run (do a cd to C:\Users\bci\Desktop\python3)
"comm5_driver_directx.py collect" in a cmd.exe window (this is in C:\Users\bci\Desktop\python3)
the png file displayed is python3\tobii_alphabet_scaled.png
the dat files must be in 
At the end of the weights run close Spritewithtimer window and bci2000

3. Developing Weights
Check data in C:\Users\bci\Desktop\training_data ## requirements.
to use the p300_gui run call_matlab_gui.pl - Shortcut on the desktop it will pickup the weights from desktop\training_data directory and create mud and prm files

4. drop template prm file on directx\make_parms_directx.bat or directx\make_parms_directx_siggen.bat

5. to run the the directx communicator 5 application: 
desktop\python3\comm5_driver_directx.py from a cmd window no longer need an adminstrative window

6. to end kill communicator5 window or exit appication by clicking (wait for faces to flash before you click)

I put the new software into desktop\python3.
The parm files are there too.
I edited the make_parms_directx.pl and the  make_parms_directx.bat(both in desktop\python3)
The  make_parms_directx.pl automatically adds the prm file from desktop\training_data so all you have to do is drop a template file onto make_parms_directx.bat any ( parm file with the correct settings like communicator_directx_56.prm (no weights)and it will create all of the  communicator_directx_xx.prm in  desktop\python3 

so now the desktop\python3 directory has
all of the  communicator_directx_xx files
make_parms_directx.bat 
make_parms_directx.pl 
check _parms_directx.pl   
and the 
faceX_org.png files from which it create the faceX.png files of the correct size
it also has a  tobii_alpha_1600x900.jpg from which it make the  tobii_alphabet_scaled.png which is use as the picture in the weights section of comm5_driver_directx.py

to run the program just cd desktop\python3 and type   comm5_driver_directx.py.
to collect weights  just cd desktop\python3 and type   comm5_driver_directx.py.collect

I'll let you create the shortcuts 
-Steve
