# Touch Screen Relay Panel
In this project, I've designed and built a relay control panel based on the raspberryPi board and 5" dsi touchscreen. \

In this work, I've used 2 8ch relay boards connected to an arduino mega communicating over USB serial connection. \

It is assumed you have a working knowledge of python and the raspberry pi including linux as well as Arduino programming

## Parts used
Raspberry Pi 3B and accessories
FREENOVE 5 Inch Touch Screen https://www.amazon.com/dp/B0B455LDKH?psc=1&ref=ppx_yo2ov_dt_b_product_details
Arduino Mega 2560 with USB cable
2X 8 Channel Relay Boards
3D printed Case designed by hiruna https://www.thingiverse.com/thing:5488963

## Preparing the raspberryPi
1. Clone the github repository using the following command
    ```
    git clone https://github.com/fierrojulian/TouchScreenRelayPanel.git
    ``` 
2. Install [guizero](https://lawsie.github.io/guizero/about/). Open new terminal (Ctrl+t) and enter:
   ```
   sudo pip3 install guizero
   ```
5. After Raspbian is installed we will need to add the main program (main.py) to the raspberryPi autostart using crontab ([tip](https://raspberrypi.stackexchange.com/questions/8734/execute-script-on-start-up)). \
Open new terminal (Ctrl+t) and enter the following command:
    ```
    sudo crontab -e
    ```
    Select to open using nano. Add the following line to the end of the file:
    ```
    @reboot python3 /home/pi/TouchScreenRelayPanel/main.py &
    ```
    close and save using Ctrl+x and enter Y.

At this point the program should run every time the raspberryPi is starts.

## Possible modifications
By replacing the images of the button, new type of button can be created.

## Points for discussion
1. I believe that the project can also be implemented using the raspberryPi zero.

## Authors
**Julian Fierro, with inspiration from Ron Berenstein** - [website](http://ronberenstein.com/index.html)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
