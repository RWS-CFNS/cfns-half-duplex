# Multi Connectivity: Half-Duplex

This project is part of the proof of concept Multi Connectivity. The purpose of this project is to validate
new DAB+ messages. With the contained data an acknowledgement needs to be send back with
the use of multiple wireless connections. For more information read the thesis (500770588-Afstudeerrapport-final.docx) on the OneDrive.

This application interfaces with dab-receiver, cap-dab-server and cfns-webapp.
See the diagram below.

![Integration with other CFNS systems](integration.png)

## Features

Following features are provided

- Read provided devices and settings from devices.csv
- Observe folder for identifying new DAB+ message
- Read content of DAB+ message
- Sending acknowledgement by AIS, LoRaWAN and LTE, WiFi
- Supported interfaces: UART, I2C, Socket and SPI
- Share information from DAB+ messages on request using an interface
- Select the best technology to acknowledge DAB+ messages

## Requirements

### Libraries

- [Watchdog](https://pypi.org/project/watchdog/)
- [aisutils](https://github.com/schwehr/noaadata) 
- [argparse](https://docs.python.org/3/library/argparse.html)
- [csv](https://docs.python.org/3/library/csv.html)


### Hardware

- Raspberry Pi 4B
- True Heading AIS Class A Base Station
- Sodaq One Rev3
- Pycom FiPy

## Setups
In order for the system being able to acknowledge DAB+ messages using the supported hardware and technologies you need to set them up first. The following section will guide you setting up the different technologies for the different hardware.

### Wifi Setup
1. Follow the setup for the server in the repository: [Wifi6_confirmation_server](https://github.com/PoCDAB/Wifi6_confirmation_server).
1. Follow the setup for WiFi in the repository: [cfns-hd-fipy](https://github.com/PoCDAB/cfns-hd-fipy).
2. Make sure that [devices.csv](devices.csv) contains the following at the first line:
````text
name,branch,model,interface_type,address,setting,technology,priority
````
3. If you want to only use WiFi remove everything from the file except for the first line. After that add the following to the file directly below the first line:
````text
FiPy,Pycom,FiPy,2,192.168.178.11,8000,Wifi,1
````
4. If you want to add WiFi to the list of technologies the system can use. Add the line shown above directly below the other files. Also make sure that the other devices/technologies are supported and described properly.
5. In this example the IP-adres of the server running on the FiPy is: 192.168.178.11 and port 8000. Check this with the socket information you use. This information can be found in the file [Server.py](https://github.com/PoCDAB/cfns-hd-fipy/blob/main/Server.py) in the repository: [cfns-hd-fipy](https://github.com/PoCDAB/cfns-hd-fipy).
6. If nothing went wrong you have succesfully set up WiFi on the FiPy.

### LoRaWAN (FiPy) Setup
1. Follow the setup for LoRaWAN in the repository: [cfns-hd-fipy](https://github.com/PoCDAB/cfns-hd-fipy).
2. Make sure that [devices.csv](devices.csv) contains the following at the first line:
````text
name,branch,model,interface_type,address,setting,technology,priority
````
3. If you want to only use LoRaWAN remove everything from the file except for the first line. After that add the following to the file directly below the first line:
````text
FiPy,Pycom,FiPy,2,192.168.178.11,8000,LoRa,2
````
4. If you want to add LoRaWAN to the list of technologies the system can use. Add the line shown above directly below the other files. Also make sure that the other devices/technologies are supported and described properly.
5. In this example the IP-adres of the server running on the FiPy is: 192.168.178.11 and port 8000. Check this with the socket information you use. This information can be found in the file [Server.py](https://github.com/PoCDAB/cfns-hd-fipy/blob/main/Server.py) in the repository: [cfns-hd-fipy](https://github.com/PoCDAB/cfns-hd-fipy).
6. If nothing went wrong you have succesfully set up LoRaWAN on the FiPy.

### LoRaWAN (Sodaq One) Setup
1. Follow the setup for LoRaWAN in the repository: [cfns-hd-so](https://github.com/PoCDAB/cfns-hd-so).
2. Make sure that [devices.csv](devices.csv) contains the following at the first line:
````text
name,branch,model,interface_type,address,setting,technology,priority
````
3. If you want to only use LoRaWAN remove everything from the file except for the first line. After that add the following to the file directly below the first line:
````text
LoRaWANTransponder,SODAQ,Sodaq One,1, 4,,LoRa,3
````
4. If you want to add LTE to the list of technologies the system can use. Add the line shown above directly below the other files. Also make sure that the other devices/technologies are supported and described properly. It is correct that there are two comma's between 4 and LoRa.
5. In this example the I2C address is 4 change this to the I2C address the Sodaq One uses in your setup. 
6. To change the I2C address change line 179 of [Half-Duplex_SodaqOne.ino](https://github.com/PoCDAB/cfns-hd-so/blob/main/Half-Duplex_SodaqOne/Half-Duplex_SodaqOne.ino) which can be found in the repository: [cfns-hd-so](https://github.com/PoCDAB/cfns-hd-so) and in [devices.csv](devices.csv) at step 3 of this guide.

### LTE (CAT-M1) Setup
1. Follow the setup for LTE in the repository: [cfns-hd-fipy](https://github.com/PoCDAB/cfns-hd-fipy).
2. Make sure that [devices.csv](devices.csv) contains the following at the first line:
````text
name,branch,model,interface_type,address,setting,technology,priority
````
3. If you want to only use LoRaWAN remove everything from the file except for the first line. After that add the following to the file directly below the first line:
````text
FiPy,Pycom,FiPy,2,192.168.178.11,8000,LTE,4
````
4. If you want to add LTE to the list of technologies the system can use. Add the line shown above directly below the other files. Also make sure that the other devices/technologies are supported and described properly.
5. In this example the IP-adres of the server running on the FiPy is: 192.168.178.11 and port 8000. Check this with the socket information you use. This information can be found in the file [Server.py](https://github.com/PoCDAB/cfns-hd-fipy/blob/main/Server.py) in the repository: [cfns-hd-fipy](https://github.com/PoCDAB/cfns-hd-fipy).
6. If nothing went wrong you have succesfully set up LTE on the FiPy.

### AIS Setup
1. Connect The True Heading AIS Base Station to the Raspberry Pi by USB.
2. Make sure that [devices.csv](devices.csv) contains the following at the first line:
````text
name,branch,model,interface_type,address,setting,technology,priority
````
3. If you want to only use AIS remove everything from the file except for the first line. After that add the following to the file directly below the first line:
````text
AIS Base Station,True Heading,Carbon Pro,0,/dev/ttyACM0,38400,AIS,0
````
4. If you want to add AIS to the list of technologies the system can use. Add the line shown above directly below the other files. Also make sure that the other devices/technologies are supported and described properly.
5. Furthermore make sure that _/dev/ttyACM0_ is being used by the FiPy for the AIS device.
6. To check this unplug the Base Station from the Raspberry Pi and run the following command on the Raspberry Pi:
````text
ls /dev/tty*
````
7. Plug the Base Station back in and rerun the command. Then see which _/dev/tty_ was added and that is the USB port the Base Station uses.
8. Use that _/dev/tty_ in [devices.csv](devices.csv).
9. You have succesfully setup AIS.

## DAB+ File Format
When a DAB+ message is received it will be stored as a .txt file in the folder [correct](correct). To simulate a message coming in a file can be made and put in that folder. The file needs to contain the following in order:
- DAB id.
- Message type.
- Category.
- X coordinate
- Y coordinate
- other data

The DAB id must be a positive integer and it is used to distinguish the different message from each other. The message type must also be an integer but it must be between 1 and 4 with both those numbers included to have a function. Some technologies support different types of acknowledgment. To figure out what message type to use see the files for the corresponding device/technology. Then you must specify the category for the different options see [Category.py](Category.py). If the the category is _location_ you must specify an X and Y coordinate otherwise you can leave these lines empty. The rest of the lines can you be used for other data such as the CAP message if the category is CAP.

## Acknowledging a DAB+ message
1. First, follow the setup of the technologies you want to the system to use for acknowledging DAB+ message (see [Setups](## Setups). You can add technologies later even when the system is running as long as you follow the corresponding setup(s).
2. Run [main.py](main.py) with the following command on the Raspberry Pi:
````python
python3 main.py ./devices.csv ./correct
````
3. Either send a DAB+ message to the Raspberry Pi or simulate a message coming in. To simulate a DAB+ message coming in add a .txt file in [correct](correct) according to the format specified in [DAB+ File Format](## DAB+ File Format).
4. Watchdog observer detects a new DAB+ message and reads the content.
5. The system starts the acknowledgment process by choosing the best technology available at that moment.
6. The system will send the acknowledgment information the device that will acknowledge the DAB+ message using the chosen technology.
7. The chosen hardware will send the acknowlegdment
8. If the technology is not AIS the device will let the system onboard know the acknowledgment is succeeded or not.
9. Finally the system will update the status of the file.  

## Requesting data from the system using the interface
In order for the interface to the onboard systems in this section specified as the interface to work the minimal requirement is for the system to be running. The interface will only start if the rest of the system is started as well.

### Testing if client and interface work
This section explains you how to test if the interface and the client are functioning properly.

1. Turn on the system by running the following command on the Raspberry Pi in this case [devices.csv](devices.csv) can contain only the required first line:
````python
python3 main.py ./devices.csv ./correct
````
2. Open [client_template.py](client_interface/client_templat.py) and make sure the socket information specified in the client.connect statement contains the socket information that corresponds to the socket information of the interface runs on.
3. Check if the client and the interface are on the same network.
4. Make sure the message looks as followed:
````python
message = json.dumps({"request_type": "test"}).encode()
````
5. If everything checks out, run the [client_template.py](client_interface/client_templat.py) script. Either on the Raspberry Pi itself or another device on the same network that has python installed.
6. The client will request the test data from the interface of the system and display it on the screen. If the result looks the same as in the method _build_information_dict_ of class _TestRequest_ in [Request.py](Request.py)

### How to request data
To request other types of data then the test data follow the process specified above. Only instead of using the message shown in step 4 use the following message to get all the data that you have not requested:
````python
message = json.dumps({"request_type": "latest"}).encode()
````

To request the data of a specific category use the following message:
````python
message = json.dumps({"request_type": "by_category","category": "other"}).encode()
````
The valid options are specified in [Category.py](Category.py) and can be specified in the place of _other_.

Finally to request the test data you can use the message described in step 4 of [Testing if client and interface work](### Testing if client and interface work).

# Credit
Credit to Kurt Schwehr and Google for [AISutils](https://github.com/schwehr/noaadata).
