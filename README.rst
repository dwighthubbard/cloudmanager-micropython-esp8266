Micropython ESP8266 Flash image with cloudmanager
=================================================

This package provides a utility to flash an esp8266 board such as a nodemcu  or
wemos d1 board with Micropython.  It will optionally configure networking and
set up the board to run cloudmanager or webrepl at start.

Requirements
============

This Utility requires python 2.7.9+ and is installed using the python pip package manager.

Mac OSX requirements
--------------------

On Mac OSX you may need to install the device driver for the usb to serial converter chip
to interface with your board.

For NodeMCU boards, you will need to install the SiLabs [serial driver for the chip](https://www.silabs.com/products/mcu/Pages/USBtoUARTBridgeVCPDrivers.aspx) ([direct link](https://www.silabs.com/Support%20Documents/Software/Mac_OSX_VCP_Driver.zip))

For Wemos D1 boards, you will need to intall the [CH340 USB to UART driver](https://www.wemos.cc/downloads) ([direct link](https://www.wemos.cc/downloads/CH34x_Install_mac.zip))

Installation
============

Install the package using the python pip tool

.. code-block:: console

    $ pip install cloudmanager_micropython_esp8266
    
Flashing a board
================

The **flash_esp_image** utility will flash a micropython image to the board and optionally configure it.

To just flash the image to the board, if the are no other serial devices installed
----------------------------------------------------------------------------------

This is the simplest option, the utility will attempt to guess the serial port the device is on and flash it.

1. Plug the board into the usb port
2. Run the **flash_esp_image** utility without arguments.

.. code-block:: console

    $ flash_esp_image 
    esptool.py --port /dev/ttyUSB0 --baud 115200 erase_flash
    esptool.py v1.2.1
    Connecting...
    Running Cesanta flasher stub...
    Erasing flash (this may take a while)...
    Erase took 9.1 seconds
    esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --verify --flash_size=32m --flash_mode=qio 0 /tmp/cloudmanager-micropython-esp8266/local/lib/python2.7/site-packages/cloudmanager_micropython_esp8266/firmware/firmware-combined.bin
    esptool.py v1.2.1
    Connecting...
    Running Cesanta flasher stub...
    Flash params set to 0x0040
    Writing 557056 @ 0x0... 19456 (3 %)
    557056 (100 %)
    Wrote 557056 bytes at 0x0 in 48.3 seconds (92.3 kbit/s)...
    Leaving...
    Verifying just-written flash...
    Verifying 0x8734c (553804) bytes @ 0x00000000 in flash against /tmp/cloudmanager-micropython-esp8266/local/lib/python2.7/site-packages/cloudmanager_micropython_esp8266/firmware/firmware-combined.bin...
    -- verify OK (digest matched)
    $

The board should now be flashed with micropython and the micropython repl prompt will be available on the serial port.

Flash the board and configure it to automatically start as a cloudmanager client
--------------------------------------------------------------------------------

1. Plug the board into the usb port
2. Run the **flash_esp_image** utility with the arguments to configure the network and cloudmanager.

The following example starts a cloudmanager server on the default port and tells the board to connect to wifi network "mywifi" using wpa password of "wifipassword" and register with a cloudmanager server at our address "192.168.1.127" running on the default port of "18266" as a device named "nodemcu1" 

.. code-block:: console

    $ mbm server-start
    $ mbm board-list
    $ flash_esp_image --wifi_ssid mywifi --wifi_password mywifipassword --cloudmanager_server 192.168.1.127 --cloudmanager_port 18266 --name nodemcu1 
    esptool.py --port /dev/ttyUSB0 --baud 115200 erase_flash
    esptool.py v1.2.1
    Connecting...
    Running Cesanta flasher stub...
    Erasing flash (this may take a while)...
    Erase took 9.0 seconds
    esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --verify --flash_size=32m --flash_mode=qio 0 /tmp/cloudmanager-micropython-esp8266/local/lib/python2.7/site-packages/cloudmanager_micropython_esp8266/firmware/firmware-combined.bin
    esptool.py v1.2.1
    Connecting...
    Running Cesanta flasher stub...
    Flash params set to 0x0040
    Writing 557056 @ 0x0... 557056 (100 %)
    Wrote 557056 bytes at 0x0 in 48.3 seconds (92.3 kbit/s)...
    Leaving...
    Verifying just-written flash...
    Verifying 0x8734c (553804) bytes @ 0x00000000 in flash against /tmp/cloudmanager-micropython-esp8266/local/lib/python2.7/site-packages/cloudmanager_micropython_esp8266/firmware/firmware-combined.bin...
    -- verify OK (digest matched)
    >>> 
    >>> import os
    >>> os.mkdir('etc')
    >>> from bootconfig.config import get, set
    >>> set('wifi_ssid', 'mywifi')
    >>> set('wifi_password', 'mywifipassword')
    >>> set('redis_server', '192.168.1.127')
    >>> set('redis_port', '18266')
    >>> set('name', 'nodemcu1')
    >>> import bootconfig.service
    >>> bootconfig.service.autostart()
    >>> import redis_cloudclient.service
    >>> redis_cloudclient.service.autostart()
    >>> import machine
    >>> machine.reset()
    $ mbm board-list
    Platform   Name                                               State     
    esp8266    nodemcu1                                           idle      
    $


It's now possible to use the **mbm** utility to upload/run code on the board.

Connecting to the serial terminal
=================================

The **esp_terminal** command is a simple terminal program that will automatically connect the the micropython repl over usb/serial using the same device and port as the **flash_esp_image** utility.

.. code-block:: console

    $ esp_terminal
    MicroPython v1.8.5-124-gbc4441a on 2016-11-06; ESP module with ESP8266
    Type "help()" for more information.
    >>>
 