# Raspberry pi temperature controller notes

The goal of this project is to provide a simple to use thermal controller for an infrared heating unit that can turn on/off at a specific, non-repeating date and time.  

## Version 1 
The physical location does not have internet access, so the unit must provide 100% of it’s own network connectivity. This is not difficult:  just configure the Raspberry PI to be a stand alone wireless access point and give it a static IP address. 

Security is physical.  The steel sided building is basically a Faraday cage and there is no internet access inside. Therefore there is no requirement for authentication or encryption. Adding them would be a form of scope creep.  I'm not saying security isn't important: the device is physically secured.  Your location and circumstances may have different requirements and the Flask web application should be modified to include the correct level of security as needed, unless you want just want to ignore the lessons from Home Depot's break in through a HVAC system. 

## Version 2
The unit is intended to be connected to the internet.  The API is exposed to the brunt of the internet, so it must be made very secure, including limiting access. 

TODO:  have the unit get SSL certs from Let's Encrypt for fully accepted SSL certs automatically updated.

To make the use as simple as possible, new features
* A predictive thermal rise curve is used to calculate the time to temperature.  The unit turns on the amount of time predicted before the use date time.  No more guessing at when to turn the heat on to to pre-heat the building and no wasted fuel if building isn't used.
* A motion sensor is used to detect if there is any motion in the building.  If there is no motion by the motio time out value, the unit turns off.

Given the building is infrequently used, there is no set schedule.  Therefore the device need only turn the heat on at a specific time and turn it off the rest of the time.  Therefore there is no repeat requirement.  Your circumstances may be different. If so, fork the code and add your needs.

The same idea could be used for controlling air conditioning.  However, the relays used are not capable of handling the load of an AC unit.  An additional relay and some AC wiring would be required.

The case is 3D printed with ABS.  One of the advantages of printing in ABS is the parts may be bonded with acetone.  I did just this for the lower half of the case.  The top cover is held on by 4) #6-32 x 3/8 screws.  The middle spacer has threads molded/printed in for this.

Parts list:
1. Raspberry PI model B
1. DS18B20 temperature sensor (others may be substituted). This project used SunFounder’s PC board to eliminate the need for a breadboard or other circuit board to hold the DS18B20.
1. Jbtek 4 Channel DC 5V Relay module.  Make sure these are contact style.
1. HC-SR501 PIR MOTION DETECTOR
1. (20) Jumper wires 
1. (2) 5mm Blue LED
1. 270 ohm 1/4 Watt resistor
1. (4) #6-32 x 3/8 pan head screws 
1. (10) M2.5 x 4mm pan head screws 
1. Case for Raspberry PI, relay and temperature sensor boards.  The STL files are posted as part of this project.  Note:  you may need 2 of the middle spacers.  
1. Android smart phone with Android 4.4 or higher
1. Apple iPhone with iOS 11 or higher

The case base parts are bonded together.  One of the charateristics of ABS is it desolves in acetone.  A few drops bonds the lower case parts together. The cover is held on with the 4 #6 screws.

## Wiring up the devices

Pin out:
|Physical pin|BCM/GPIO|Connected to|
|------------|--------|------------|
|1||DS18b20 temperature: VCC (3.3V)|
|2||Relay board VCC (5V)|

<table border=1><tr>
<td>Physical pin</td>
<td>BCM/GPIO #</td>
<td>Connected to</td></tr>
<tr><td>1</td><td></td><td>DS18b20 temperature: VCC (3.3V)</td></tr>
<tr><td>2</td><td></td><td>Relay board VCC (5V)</td></tr>
<tr><td>4</td><td></td><td>PIR motion sensor 5V+</td></tr>
<tr><td>6</td><td></td><td>Relay board GND</td></tr>
<tr><td>7</td><td>GPIO4</td><td>DS18b20 temperature: SIG</td></tr>
<tr><td>9</td><td></td><td>DS18b20 temperature: GND</td></tr>
<tr><td>11</td><td>GPIO17</td><td>Relay board: IN1</td></tr>
<tr><td>12</td><td>GPIO18</td><td>Status LED</td></tr>
<tr><td>13</td><td>GPIO27</td><td>Relay board: IN2</td></tr>
<tr><td>14</td><td></td><td>Status LED GND</td></tr>
<tr><td>15</td><td>GPIO22</td><td>Relay board: IN3</td></tr>
<tr><td>16</td><td>GPIO23</td><td>PIR motion sensor</td></tr>
<tr><td>19</td><td>GPIO10</td><td>Relay board: IN4</td></tr>
<tr><td>20</td><td></td><td>PIR motion sensor GND</td></tr>
</table>

Pinout of Raspberry PI:
![](https://az835927.vo.msecnd.net/sites/iot/Resources/images/PinMappings/RP2_Pinout.png)

PIR motion sensor fact and how-to sheet:
<http://henrysbench.capnfatz.com/henrys-bench/arduino-sensors-and-input/arduino-hc-sr501-motion-sensor-tutorial/>

Turn the senitivity pot (on left) to max (clockwise) to detect motion ~7m away.

Turn the time delay pot (on right) to min (counter clockwise) so the motion detector's time delay is ~3 seconds.  Never set any time parameter to less than 6 seconds becuase it will only cause confussion due to false positives and negatives.  The reason is the motion sensor will not change state while it is in a time delay.

The as delivered motion sensors did not have a jumper for trigger selection.  It only had solder pads.  The high setting was used by soldering a jumper inplace.

Basic article on controlling the relays:
<https://elementztechblog.wordpress.com/2014/09/09/controlling-relay-boards-using-raspberrypi/>

Quick & dirty how to get the temperature value:
<http://raspberrywebserver.com/gpio/connecting-a-temperature-sensor-to-gpio.html>

The lower case 3D print in process:
![](http://moosewareinc.com//portfolio/images/3dprinted-parts/RaspberryPiControllerCase.jpeg)

Note the circuit board bosses have printed/molded threads and are filleted for stress relief.

The assembled unit:  
![](http://moosewareinc.com//portfolio/images/3dprinted-parts/TControllerCompleted.jpeg)

Installed and working:
![](http://moosewareinc.com//portfolio/images/3dprinted-parts/smart_thermostat_installed.jpeg)

A screen shot of the User Interface (UI)
![](http://moosewareinc.com//portfolio/images/Screenshot_1491054776.png)

