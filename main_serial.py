from guizero import App, PushButton, Slider, Text
from PIL import Image
from rpi_backlight import Backlight as bl
import RPi.GPIO as GPIO
import serial
import time
import subprocess

ser = serial.Serial("/dev/ttyACM0", 9600)
time.sleep(2) #wait for the serial connection to initialize

GPIO.setmode(GPIO.BOARD) #Sets the mode to use GPIO physical pin locations 
GPIO.setwarnings(False) #Stops all GPIO pin warnings

path = '/home/pi/TouchScreenRelayPanel/' #The path of the pyton program and button photos
#Initial states of the circuits, used to monitor if they are ON or OFF
Fog_Lights_State = 0
Light_Bar_State = 0
Backup_Lights_State = 0
Truck_Bed_Lights_State = 0
Rock_Lights_State = 0
Ditch_Lights_State = 0
Air_Compressor_State = 0
Winch_State = 0
Button_9_State = 0
Button_10_State = 0
Button_11_State = 0
Button_12_State = 0
Button_13_State = 0
Button_14_State = 0
Button_15_State = 0
Button_16_State = 0
Trail_Lights_State = 0
Recovery_State = 0
Button_19_State = 0
Button_20_State = 0
Night_Trail_State = 0


def Fog_Lights_Callback(): # Fog Lights Callback, turns ON and OFF the Fog Lights relay
    global Fog_Lights_State, Fog_Lights
    if Fog_Lights_State == 0: #If the Fog Lights are OFF and the button is pressed, the Fog Lights turn ON
        Fog_Lights_State = 1 # Changes the state of the Fog lights to track if it is on 
        Fog_Lights.image = path + 'Fog_Lights_On.png' # Changes the image on the touch screen when pressed
        ser.write(b'0\n') # Sends a '0' to the arduino over serial to turn on the relay
    else: #If the Fog Lights are ON and the button is pressed, the Figh Lights turns OFF
        Fog_Lights_State = 0 # Changes the state of the Fog,ights to track if it is off
        Fog_Lights.image = path + 'Fog_Lights_Off.png' # Changes the image on the touch screen when pressed
        ser.write(b'1\n') # Sends a '1' to the arduino over serial to turn off the relay

def Light_Bar_Callback(): #Light Barr Callback, tusn ON and OFF the Light Bar relay
    global Light_Bar_State, Light_Bar
    if Light_Bar_State == 0: #If the Light Bar is OFF and the button is pressed, the Light Bar turns ON
        Light_Bar_State = 1
        Light_Bar.image = path + 'Light_Bar_On.png'
        ser.write(b'2\n')
    else: #If the Light Bar is ON and the button is pressed, the Light Bar turns OFF
        Light_Bar_State = 0
        Light_Bar.image = path + 'Light_Bar_Off.png'
        ser.write(b'3\n')

def Ditch_Lights_Callback(): #Ditch Light Callback, turns ON and OFF the Ditch Lights relay
    global Ditch_Lights_State, Ditch_Lights
    if Ditch_Lights_State == 0: #If the Ditch Lights are OFF and the button is pressed, the Ditch Lights turn ON
        Ditch_Lights_State = 1
        Ditch_Lights.image = path + 'Ditch_Lights_On.png'
        ser.write(b'4\n')
    else: #If the Ditch Lights are ON and the button is pressed, the Ditch Lights turn OFF
        Ditch_Lights_State = 0
        Ditch_Lights.image = path + 'Ditch_Lights_Off.png'
        ser.write(b'5\n')

def Backup_Lights_Callback(): #Backup Lights Callback, turns ON and OFF the Backup Lights relay
    global Backup_Lights_State, Backup_Lights
    if Backup_Lights_State == 0: #If the Backup Lights are OFF and the button is pressed, the Backup Lights turn ON
        Backup_Lights_State = 1
        Backup_Lights.image = path + 'Backup_Lights_On.png'
        ser.write(b'6\n')
    else: #If the Backup Lights are ON and the button is pressed, the Backup Lights turn OFF
        Backup_Lights_State = 0
        Backup_Lights.image = path + 'Backup_Lights_Off.png'
        ser.write(b'7\n')
        
def Truck_Bed_Lights_Callback(): #Truck Bed Lights Callback, turns ON and OFF the Truck Bed Lights relay
    global Truck_Bed_Lights_State, Truck_Bed_Lights
    if Truck_Bed_Lights_State == 0: #If the Truck Bed  Lights are OFF and the button is pressed, the Truck Bed Lights turn ON
        Truck_Bed_Lights_State = 1
        Truck_Bed_Lights.image = path + 'Truck_Bed_Lights_On.png'
        ser.write(b'8\n')
    else: #If the Truck Bed  Lights are ON and the button is pressed, the Truck Bed Lights turn OFF
        Truck_Bed_Lights_State = 0
        Truck_Bed_Lights.image = path + 'Truck_Bed_Lights_Off.png'
        ser.write(b'9\n')
        
def Rock_Lights_Callback(): #Rock Lights Callback, turns ON and OFF the Rock Lights relay
    global Rock_Lights_State, Rock_Lights
    if Rock_Lights_State == 0: #If the Rock Lights are OFF and the button is pressed, the Rock Lights turn ON
        Rock_Lights_State = 1
        Rock_Lights.image = path + 'Rock_Lights_On.png'
        ser.write(b'A\n')
    else: #If the Rock Lights are ON and the button is pressed, the Rock Lights turn OFF
        Rock_Lights_State = 0
        Rock_Lights.image = path + 'Rock_Lights_Off.png'
        ser.write(b'B\n')

def Air_Compressor_Callback(): #Air Compressor Callback, tusn ON and OFF the Air Compressor relay
    global Air_Compressor_State, Air_Compressor
    if Air_Compressor_State == 0: #If the Air Compressor is OFF and the button is pressed, the Air Compressor turns ON
        Air_Compressor_State = 1
        Air_Compressor.image = path + 'Air_Compressor_On.png'
        ser.write(b'C\n')
    else: #If the Air Compressor is ON and the button is pressed, the Air Compressor turns OFF
        Air_Compressor_State = 0
        Air_Compressor.image = path + 'Air_Compressor_Off.png'
        ser.write(b'D\n')
        
def Winch_Callback(): #Winch Callback, turns ON and OFF the Winch relay
    global Winch_State, Winch
    if Winch_State == 0: #If the Winch is OFF and the button is pressed, the Winch turns ON
        Winch_State = 1
        Winch.image = path + 'Winch_On.png'
        ser.write(b'E\n')
    else: #If the Winch is ON and the button is pressed, the Winch turns OFF
        Winch_State = 0
        Winch.image = path + 'Winch_Off.png'
        ser.write(b'F\n')
        
def Button_9_Callback(): #Button 15 Callback, turns ON and OFF the Button 15 relay
    global Button_9_State, Button_9
    if Button_9_State == 0: #If Button 15 is OFF and the button is pressed, Button 15 turns ON
        Button_9_State = 1
        Button_9.image = path + 'Spare_On.png'
        ser.write(b'G\n')
    else: #If Button 15 is ON and the button is pressed, Button 15 turns OFF
        Button_9_State = 0
        Button_9.image = path + 'Spare_Off.png'
        ser.write(b'H\n')
        
def Button_10_Callback(): #Button 16 Callback, turns ON and OFF the Button 16 relay
    global Button_10_State, Button_10
    if Button_10_State == 0: #If Button 16 is OFF and the button is pressed, Button 16 turns ON
        Button_10_State = 1
        Button_10.image = path + 'Spare_On.png'
        ser.write(b'I\n')
    else: #If Button 16 is ON and the button is pressed, Button 16 turns OFF
        Button_10_State = 0
        Button_10.image = path + 'Spare_Off.png'
        ser.write(b'J\n')
        
def Button_11_Callback(): #Button 17 Callback, turns ON and OFF the Button 17 relay
    global Button_11_State, Button_11
    if Button_11_State == 0: #If Button 17 is OFF and the button is pressed, Button 17 turns ON
        Button_11_State = 1
        Button_11.image = path + 'Spare_On.png'
        ser.write(b'K\n')
    else: #If Button 17 is ON and the button is pressed, the Button 17 turns OFF
        Button_11_State = 0
        Button_11.image = path + 'Spare_Off.png'
        ser.write(b'L\n')
        
def Button_12_Callback(): #Button 17 Callback, turns ON and OFF the Button 17 relay
    global Button_12_State, Button_12
    if Button_12_State == 0: #If Button 17 is OFF and the button is pressed, Button 17 turns ON
        Button_12_State = 1
        Button_12.image = path + 'Spare_On.png'
        ser.write(b'M\n')
    else: #If Button 17 is ON and the button is pressed, the Button 17 turns OFF
        Button_12_State = 0
        Button_12.image = path + 'Spare_Off.png'
        ser.write(b'N\n')
        
def Button_13_Callback(): #Button 8 Callback, turns ON and OFF the Button 8 relay
    global Button_13_State, Button_9
    if Button_13_State == 0: #If Button 8 is OFF and the button is pressed, Button 8 turns ON
        Button_13_State = 1
        Button_13.image = path + 'Spare_On.png'
        ser.write(b'O\n')
    else: #If Button 8 is ON and the button is pressed, Button 15 turns OFF
        Button_13_State = 0
        Button_13.image = path + 'Spare_Off.png'
        ser.write(b'P\n')
        
def Button_14_Callback(): #Button 8 Callback, turns ON and OFF the Button 8 relay
    global Button_14_State, Button_9
    if Button_14_State == 0: #If Button 8 is OFF and the button is pressed, Button 8 turns ON
        Button_14_State = 1
        Button_14.image = path + 'Spare_On.png'
        ser.write(b'Q\n')
    else: #If Button 8 is ON and the button is pressed, Button 15 turns OFF
        Button_14_State = 0
        Button_14.image = path + 'Spare_Off.png'
        ser.write(b'R\n')
        
def Button_15_Callback(): #Button 8 Callback, turns ON and OFF the Button 8 relay
    global Button_15_State, Button_9
    if Button_15_State == 0: #If Button 8 is OFF and the button is pressed, Button 8 turns ON
        Button_15_State = 1
        Button_15.image = path + 'Spare_On.png'
        ser.write(b'S\n')
    else: #If Button 8 is ON and the button is pressed, Button 15 turns OFF
        Button_15_State = 0
        Button_15.image = path + 'Spare_Off.png'
        ser.write(b'T\n')
        
def Button_16_Callback(): #Button 8 Callback, turns ON and OFF the Button 8 relay
    global Button_16_State, Button_9
    if Button_16_State == 0: #If Button 8 is OFF and the button is pressed, Button 8 turns ON
        Button_16_State = 1
        Button_16.image = path + 'Spare_On.png'
        ser.write(b'U\n')
    else: #If Button 8 is ON and the button is pressed, Button 15 turns OFF
        Button_16_State = 0
        Button_16.image = path + 'Spare_Off.png'
        ser.write(b'V\n')
        
def Trail_Lights_Callback():
    global Trail_Lights_State, Trail_Lights
    if Trail_Lights_State == 0:
        Trail_Lights_State = 1
        Trail_Lights.image = path + 'Trail_Lights_On.png'
        if Fog_Lights_State == 1:
            if Light_Bar_State == 1:
                if Ditch_Lights_State == 1:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 1:
                    Ditch_Lights_Callback()
                else:
                    Ditch_Lights_Callback()
                    Rock_Lights_Callback()
            elif Ditch_Lights_State == 1:
                if Light_Bar_State == 1:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 1:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Rock_Lights_Callback()
            elif Rock_Lights_State == 1:
                if Light_Bar_State == 1:
                    Ditch_Lights_Callback()
                elif Ditch_Lights_State == 1:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Ditch_Lights_Callback()
            else:
                Light_Bar_Callback()
                Ditch_Lights_Callback()
                Rock_Lights_Callback()
        elif Light_Bar_State == 1:
            if Fog_Lights_State == 1:
                if Ditch_Lights_State == 1:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 1:
                    Ditch_Lights_Callback()
                else:
                    Ditch_Lights_Callback()
                    Rock_Lights_Callback()
            elif Ditch_Lights_State == 1:
                if Fog_Lights_State == 1:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 1:
                    Fog_Lights_Callback()
                else:
                    Fog_Lights_Callback()
                    Rock_Lights_Callback()
            elif Rock_Lights_State == 1:
                if Fog_Lights_State == 1:
                    Ditch_Lights_Callback()
                elif Ditch_Lights_State == 1:
                    Fog_Lights_Callback()
                else:
                    Fog_Lights_Callback()
                    Ditch_Lights_Callback()
            else:
                Fog_Lights_Callback()
                Ditch_Lights_Callback()
                Rock_Lights_Callback()
        elif Ditch_Lights_State == 1:
            if Light_Bar_State == 1:
                if Fog_Lights_State == 1:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 1:
                    Fog_Lights_Callback()
                else:
                    Ditch_Lights_Callback()
                    Rock_Lights_Callback()
            elif Fog_Lights_State == 1:
                if Light_Bar_State == 1:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 1:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Rock_Lights_Callback()
            elif Rock_Lights_State == 1:
                if Light_Bar_State == 1:
                    Fog_Lights_Callback()
                elif Fog_Lights_State == 1:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Fog_Lights_Callback()
            else:
                Light_Bar_Callback()
                Fog_Lights_Callback()
                Rock_Lights_Callback()
        elif Rock_Lights_State == 1:
            if Light_Bar_State == 1:
                if Ditch_Lights_State == 1:
                    Fog_Lights_Callback()
                elif Rock_Lights_State == 1:
                    Ditch_Lights_Callback()
                else:
                    Ditch_Lights_Callback()
                    Fog_Lights_Callback()
            elif Ditch_Lights_State == 1:
                if Light_Bar_State == 1:
                    Fog_Lights_Callback()
                elif Rock_Lights_State == 1:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Fog_Lights_Callback()
            elif Fog_Lights_State == 1:
                if Light_Bar_State == 1:
                    Ditch_Lights_Callback()
                elif Ditch_Lights_State == 1:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Ditch_Lights_Callback()
            else:
                Light_Bar_Callback()
                Ditch_Lights_Callback()
                Fog_Lights_Callback()
        else:
            Fog_Lights_Callback()
            Light_Bar_Callback()
            Ditch_Lights_Callback()
            Rock_Lights_Callback()
    else:
        Trail_Lights_State = 0
        Trail_Lights.image = path + 'Trail_Lights_Off.png'
        if Fog_Lights_State == 0:
            if Light_Bar_State == 0:
                if Ditch_Lights_State == 0:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 0:
                    Ditch_Lights_Callback()
                else:
                    Ditch_Lights_Callback()
                    Rock_Lights_Callback()
            elif Ditch_Lights_State == 0:
                if Light_Bar_State == 0:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 0:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Rock_Lights_Callback()
            elif Rock_Lights_State == 0:
                if Light_Bar_State == 0:
                    Ditch_Lights_Callback()
                elif Ditch_Lights_State == 0:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Ditch_Lights_Callback()
            else:
                Light_Bar_Callback()
                Ditch_Lights_Callback()
                Rock_Lights_Callback()
        elif Light_Bar_State == 0:
            if Fog_Lights_State == 0:
                if Ditch_Lights_State == 0:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 0:
                    Ditch_Lights_Callback()
                else:
                    Ditch_Lights_Callback()
                    Rock_Lights_Callback()
            elif Ditch_Lights_State == 0:
                if Fog_Lights_State == 0:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 0:
                    Fog_Lights_Callback()
                else: 
                    Fog_Lights_Callback()
                    Rock_Lights_Callback()
            elif Rock_Lights_State == 0:
                if Fog_Lights_State == 0:
                    Ditch_Lights_Callback()
                elif Ditch_Lights_State == 0:
                    Fog_Lights_Callback()
                else:
                    Fog_Lights_Callback()
                    Ditch_Lights_Callback()
            else:
                Fog_Lights_Callback()
                Ditch_Lights_Callback()
                Rock_Lights_Callback()
        elif Ditch_Lights_State == 0:
            if Fog_Lights_State == 0:
                if Light_Bar_State == 0:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 0:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Rock_Lights_Callback()
            elif Light_Bar_State == 0:
                if Fog_Lights_State == 0:
                    Rock_Lights_Callback()
                elif Rock_Lights_State == 0:
                    Fog_Lights_Callback()
                else:
                    Fog_Lights_Callback()
                    Rock_Lights_Callback()
            elif Rock_Lights_State == 0:
                if Fog_Lights_State == 0:
                    Light_Bar_Callback()
                elif Light_Bar_State == 0:
                    Fog_Lights_Callback()
                else:
                    Fog_Lights_Callback()
                    Light_Bar_Callback()
            else:
                Fog_Lights_Callback()
                Light_Bar_Callback()
                Rock_Lights_Callback()
        elif Rock_Lights_State == 0:
            if Fog_Lights_State == 0:
                if Light_Bar_State == 0:
                    Ditch_Lights_Callback()
                elif Ditch_Lights_State == 0:
                    Light_Bar_Callback()
                else:
                    Light_Bar_Callback()
                    Ditch_Lights_Callback()
            elif Light_Bar_State == 0:
                if Fog_Lights_State == 0:
                    Ditch_Lights_Callback()
                elif Ditch_Lights_State == 0:
                    Fog_Lights_Callback()
                else:
                    Fog_Lights_Callback()
                    Ditch_Lights_Callback()
            elif Ditch_Lights_State == 0:
                if Fog_Lights_State == 0:
                    Light_Bar_Callback()
                elif Light_Bar_Callback == 0:
                    Fog_Lights_Callback()
                else:
                    Fog_Lights_Callback()
                    Light_Bar_Callback()
            else:
                Fog_Lights_Callback()
                Light_Bar_Callback()
                Ditch_Lights_Callback()
        else:
            Fog_Lights_Callback()
            Light_Bar_Callback()
            Ditch_Lights_Callback()
            Rock_Lights_Callback()
        
def Recovery_Callback():
    global Recovery_State, Recovery, Night_Trail_State
    if Recovery_State == 0:
        Recovery_State = 1
        Recovery.image = path + 'Recovery_On.png'
        if Trail_Lights_State == 1:
            if Backup_Lights_State == 1:
                if Truck_Bed_Lights_State == 1:
                    if Air_Compressor_State == 1: 
                        Winch_Callback()
                        Night_Trail_State = 1
                    elif Winch_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                    else:
                        Air_Compressor_Callback()
                        Winch_Callback()
                        Night_Trail_State = 1
                elif Air_Compressor_State == 1:
                    if Truck_Bed_Lights_State ==1:
                        Winch_Callback()
                        Night_Trail_State = 1
                    elif Winch_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Truck_Bed_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 1
                elif Winch_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                    elif Air_Compressor_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Truck_Bed_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                else:
                    Truck_Bed_Lights_Callback()
                    Air_Compressor_Callback()
                    Winch_Callback()
                    Night_Trail_State = 1
            elif Truck_Bed_Lights_State == 1:
                if Backup_Lights_State == 1:
                    if Air_Compressor_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 1
                    elif Winch_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                    else:
                        Air_Compressor_Callback()
                        Winch_Callback()
                        Night_Trail_State = 1
                elif Air_Compressor_State == 1:
                    if Backup_Lights_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 1
                    elif Winch_State == 1:
                        Backup_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Backup_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 1
                elif Winch_State == 1:
                    if Backup_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                    elif Air_Compressor_State == 1:
                        Backup_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Backup_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                else:
                    Backup_Lights_Callback()
                    Air_Compressor_Callback()
                    Winch_Callback()
                    Night_Trail_State = 1
            elif Air_Compressor_State == 1:
                if Backup_Lights_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 1
                    elif Winch_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Truck_Bed_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 1
                elif Truck_Bed_Lights_State == 1:
                    if Backup_Lights_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 1
                    elif Winch_State == 1:
                        Backup_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Backup_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 1
                elif Winch_State == 1:
                    if Backup_Lights_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 1
                    elif Truck_Bed_Lights_State == 1:
                        Backup_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Backup_Lights_Callback()
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 1
                else:
                    Backup_Lights_Callback()
                    Truck_Bed_Lights_Callback()
                    Winch_Callback()
                    Night_Trail_State = 1
            elif Winch_State == 1:
                if Backup_Lights_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                    elif Air_Compressor_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Truck_Bed_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                elif Truck_Bed_Lights_State == 1:
                    if Backup_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                    elif Air_Compressor_State == 1:
                        Backup_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Backup_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 1
                elif Air_Compressor_State == 1:
                    if Backup_Lights_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State =1
                    elif Truck_Bed_Lights_State == 1:
                        Backup_Lights_Callback()
                        Night_Trail_State = 1
                    else:
                        Backup_Lights_Callback()
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 1
                else:
                    Backup_Lights_Callback()
                    Truck_Bed_Lights_Callback()
                    Air_Compressor_Callback()
                    Night_Trail_State = 1
            else:
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
                Night_Trail_State = 1
        elif Backup_Lights_State == 1:
            if Trail_Lights_State == 1:
                if Truck_Bed_Lights_State == 1:
                    if Air_Compressor_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    else:
                        Air_Compressor_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Air_Compressor_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Truck_Bed_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Winch_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    elif Air_Compressor_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Truck_Bed_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                else:
                    Truck_Bed_Lights_Callback()
                    Air_Compressor_Callback()
                    Winch_Callback()
                    Night_Trail_State = 0
            elif Truck_Bed_Lights_State == 1:
                if Trail_Lights_State == 1:
                    if Air_Compressor_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    else:
                        Air_Compressor_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Air_Compressor_State == 1:
                    if Trail_Lights_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Winch_State == 1:
                    if Trail_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    elif Air_Compressor_State == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                else:
                    Trail_Lights_Callback()
                    Air_Compressor_Callback()
                    Winch_Callback()
                    Night_Trail_State = 0
            elif Air_Compressor_State == 1:
                if Trail_Lights_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Truck_Bed_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Truck_Bed_Lights_State == 1:
                    if Trail_Lights_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Winch_State == 1:
                    if Trail_Lights_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 0
                    elif Truck_Bed_Lights_State == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 0
                else:
                    Trail_Lights_Callback()
                    Truck_Bed_Lights_Callback()
                    Winch_Callback()
                    Night_Trail_State = 0
            elif Winch_State == 1:
                if Trail_Lights_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    elif Air_Compressor_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Truck_Bed_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                elif Truck_Bed_Lights_State == 1:
                    if Trail_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    elif Air_Compressor_State == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                elif Air_Compressor_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    elif Truck_Bed_Lights_State == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Truck_Bed_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                else:
                    Trail_Lights_Callback()
                    Truck_Bed_Lights_Callback()
                    Air_Compressor_Callback()
                    Night_Trail_State = 0
            else:
                Trail_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
                Night_Trail_State = 0
        elif Truck_Bed_Lights_State == 1:
            if Trail_Lights_State == 1:
                if Truck_Bed_Lights_State == 1:
                    if Air_Compressor_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    else:
                        Air_Compressor_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Air_Compressor_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Truck_Bed_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Winch_State == 1:
                    if Truck_Bed_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    elif Air_Compressor_State == 1:
                        Truck_Bed_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Truck_Bed_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                else:
                    Truck_Bed_Lights_Callback()
                    Air_Compressor_Callback()
                    Winch_Callback()
                    Night_Trail_State = 0
            elif Backup_Lights_State == 1:
                if Trail_Lights_State == 1:
                    if Air_Compressor_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    else:
                        Air_Compressor_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Air_Compressor_State == 1:
                    if Trail_Lights_State == 1:
                        Winch_Callback()
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Winch_State == 1:
                    if Trail_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    elif Air_Compressor_State == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                else:
                    Trail_Lights_Callback()
                    Air_Compressor_Callback()
                    Winch_Callback()
                    Night_Trail_State = 0
            elif Air_Compressor_State == 1:
                if Trail_Lights_State == 1:
                    if Backup_Lights_State == 1:
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Night_Trail_State = 0
                    else:
                        Backup_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Backup_Lights_State == 1:
                    if Trail_Lights_State == 1:
                        Night_Trail_State = 0
                    elif Winch_State == 1:
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Winch_Callback()
                        Night_Trail_State = 0
                elif Winch_State == 1:
                    if Trail_Lights_State == 1:
                        Night_Trail_State = 0
                    elif Backup_Lights_State == 1:
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Backup_Lights_Callback()
                        Night_Trail_State = 0
                else:
                    Trail_Lights_Callback()
                    Backup_Lights_Callback()
                    Winch_Callback()
                    Night_Trail_State = 0
            elif Winch_State == 1:
                if Trail_Lights_State == 1:
                    if Backup_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    elif Air_Compressor_State == 1:
                        Backup_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Backup_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                elif Backup_Lights_State == 1:
                    if Trail_Lights_State == 1:
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                    elif Air_Compressor_State == 1:
                        Backup_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Air_Compressor_Callback()
                        Night_Trail_State = 0
                elif Air_Compressor_State == 1:
                    if Trail_Lights_State == 1:
                        Backup_Lights_Callback()
                        Night_Trail_State = 0
                    elif Backup_Lights_On == 1:
                        Trail_Lights_Callback()
                        Night_Trail_State = 0
                    else:
                        Trail_Lights_Callback()
                        Backup_Lights_Callback()
                        Night_Trail_State = 0
                else:
                    Trail_Lights_Callback()
                    Backup_Lights_Callback()
                    Air_Compressor_Callback()
                    Night_Trail_State = 0
            else:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
                Night_Trail_State = 0
        elif Air_Compressor_State == 1:
            if Trail_Lights_State == 1:
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
                Night_Trail_State = 0
            elif Backup_Lights_State == 1:
                Trail_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
                Night_Trail_State = 0
            elif Truck_Bed_Lights_State == 1:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Winch_Callback()
                Night_Trail_State = 0
            elif Winch_State == 1:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Night_Trail_State = 0
            else:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
                Night_Trail_State = 0
        elif Winch_State == 1:
            if Trail_Lights_State == 1:
                Truck_Bed_Lights_Callback()
                Backup_Lights_Callback()
                Air_Compressor_Callback()
                Night_Trail_State = 0
            elif Backup_Lights_State == 1:
                Trail_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Night_Trail_State = 0
            elif Truck_Bed_Lights_State == 1:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Air_Compressor_Callback()
                Night_Trail_State = 0
            elif Air_Compressor_State == 1:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Night_Trail_State = 0
            else:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Night_Trail_State = 0
        else:
            Trail_Lights_Callback()
            Backup_Lights_Callback()
            Truck_Bed_Lights_Callback()
            Air_Compressor_Callback()
            Winch_Callback()
            Night_Trail_State = 0
    else:
        Recovery_State = 0
        Recovery.image = path + 'Recovery_Off.png'
        if Night_Trail_State == 1:
            if Backup_Lights_State == 0:
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
            elif Truck_Bed_Lights_State == 0:
                Backup_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
            elif Air_Compressor_State == 0:
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Winch_Callback()
            elif Winch_State == 0:
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
            else:
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
        else:
            if Trail_Lights_State == 0:
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
            elif Backup_Lights_State == 0:
                Trail_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
            elif Truck_Bed_Lights_State == 0:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()
            elif Air_Compressor_State == 0:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Winch_Callback()
            elif Winch_State == 0:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
            else:
                Trail_Lights_Callback()
                Backup_Lights_Callback()
                Truck_Bed_Lights_Callback()
                Air_Compressor_Callback()
                Winch_Callback()

def Button_19_Callback():
    global Button_19_State, Button_19
    if Button_19_State == 0:
        Button_19_State = 1
        Button_19.image = path + 'Spare_On.png'
    else:
        Button_19_State = 0
        Button_19.image = path + 'Spare_Off.png'
        
def Button_20_Callback():
    global Button_20_State, Button_20
    if Button_20_State == 0:
        Button_20_State = 1
        Button_20.image = path + 'Spare_On.png'
    else:
        Button_20_State = 0
        Button_20.image = path + 'Spare_Off.png'
        
        
def screen_brightness(value):
    global slider
    value = slider.value
    subprocess.run(["sudo", "rpi-backlight", "--set-brightness", str(value)])

app = App(title="Keypad example", width=800, height=480, layout="grid")
app.bg='black'
Fog_Lights = PushButton(app, command=Fog_Lights_Callback, grid=[0,0], align='left', image = path + 'Fog_Lights_Off.png')
Light_Bar = PushButton(app, command=Light_Bar_Callback, grid=[1,0], align='left',image = path + 'Light_Bar_Off.png')
Ditch_Lights  = PushButton(app, command=Ditch_Lights_Callback, grid=[2,0], align='left',image = path + 'Ditch_Lights_Off.png')
Backup_Lights  = PushButton(app, command=Backup_Lights_Callback, grid=[3,0], align='left',image = path + 'Backup_Lights_Off.png')
Truck_Bed_Lights  = PushButton(app, command=Truck_Bed_Lights_Callback, grid=[4,0], align='left',image = path + 'Truck_Bed_Lights_Off.png')
Rock_Lights  = PushButton(app, command=Rock_Lights_Callback, grid=[0,1], align='left',image = path + 'Rock_Lights_Off.png')
Air_Compressor  = PushButton(app, command=Air_Compressor_Callback, grid=[1,1], align='left',image = path + 'Air_Compressor_Off.png')
Winch  = PushButton(app, command=Winch_Callback, grid=[2,1], align='left',image = path + 'Winch_Off.png')
Button_9  = PushButton(app, command=Button_9_Callback, grid=[3,1], align='left',image = path + 'Spare_Off.png')
Button_10  = PushButton(app, command=Button_10_Callback, grid=[4,1], align='left',image = path + 'Spare_Off.png')
Button_11  = PushButton(app, command=Button_11_Callback, grid=[0,2], align='left',image = path + 'Spare_Off.png')
Button_12  = PushButton(app, command=Button_12_Callback, grid=[1,2], align='left',image = path + 'Spare_Off.png')
Button_13  = PushButton(app, command=Button_13_Callback, grid=[2,2], align='left',image = path + 'Spare_Off.png')
Button_14  = PushButton(app, command=Button_14_Callback, grid=[3,2], align='left',image = path + 'Spare_Off.png')
Button_15  = PushButton(app, command=Button_15_Callback, grid=[4,2], align='left',image = path + 'Spare_Off.png')
Button_16  = PushButton(app, command=Button_16_Callback, grid=[0,3], align='left',image = path + 'Spare_Off.png')
Trail_Lights  = PushButton(app, command=Trail_Lights_Callback, grid=[1,3], align='left',image = path + 'Trail_Lights_Off.png')
Recovery  = PushButton(app, command=Recovery_Callback, grid=[2,3], align='left',image = path + 'Recovery_Off.png')
Button_19  = PushButton(app, command=Button_19_Callback, grid=[3,3], align='left',image = path + 'Spare_Off.png')
Button_20  = PushButton(app, command=Button_20_Callback, grid=[4,3], align='left',image = path + 'Spare_Off.png')

slider = Slider(app, command=screen_brightness, grid=[0,5,5,4], align='left', start=0, end=100)
slider.value='100'
slider.resize(800, 480)
slider.text_color='white'
slider.bg='black'

def main():
    app.tk.attributes("-fullscreen",True)
    app.tk.config(cursor='none')
    app.display()

if __name__ == '__main__':
    main()