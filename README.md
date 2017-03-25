# Raspberry pi temperature controller notes

The goal of this project is to provide a more or less simple thermal controller for an infrared heating unit.  The physical location does not have internet access, so the unit must provide 100% of it’s own network connectivity. This is not difficult:  just configure the Raspberry PI to be a stand alone wireless access point.  

Also, the building is infrequently used.  There is no set schedule.  Therefore the device need only turn the heat on for a specific time and turn it off the rest of the time.  Therefore there is no repeat requirement.

The same idea could be used for controlling air conditioning.  However, the relays used are not capable of handling the load of an AC unit.  An additional relay and some AC wiring would be required.

Parts list:
1. Raspberry PI model B
1. DS18B20 temperature sensor (others may be substituted). This project used SunFounder’s PC board to eliminate the need for a breadboard or other circuit board to hold the DS18B20.
1. Jbtek 4 Channel DC 5V Relay module
1. Jumper wires
1. Case for Raspberry PI, relay and temperature sensor boards.  I 3D printed one from ABS.  The STL files are posted as part of this project.
1. Android smart phone with Android 4.4 or higher 

## Wiring up the devices

Pin out:
for pin ID’s on Raspberry, see:
<https://elementztechblog.wordpress.com/2014/09/09/controlling-relay-boards-using-raspberrypi/>
<https://pinout.xyz/pinout/pin19_gpio10#>
<table><tr>
<td>Physical pin</td>
<td>BCM/GPIO #</td>
<td>Connected to</td>
<tr><td>1</td><td></td><td>DS18b20 temperature: VCC (3.3V)</td></tr>
<tr><td>2</td><td></td><td>Relay board VCC (5V)</td></tr>
<tr><td>6</td><td></td><td>Relay board GND</td></tr>
<tr><td>7</td><td>GPIO4</td><td>DS18b20 temperature: SIG</td></tr>
<tr><td>9</td><td></td><td>DS18b20 temperature: GND</td></tr>
<tr><td>11</td><td>GPIO17</td><td>Relay board: IN1</td></tr>
<tr><td>13</td><td>GPIO27</td><td>Relay board: IN2</td></tr>
<tr><td>15</td><td>GPIO22</td><td>Relay board: IN3</td></tr>
<tr><td>19</td><td>GPIO10</td><td>Relay board: IN4</td></tr>
</tr></table>

Old pinout of Raspberry PI:
![](https://elementztechblog.files.wordpress.com/2014/09/raspberry-pi-gpio.png)
Basic article on controlling the relays:
<https://elementztechblog.wordpress.com/2014/09/09/controlling-relay-boards-using-raspberrypi/>

Quick & dirty how to get the temperature value:
<http://raspberrywebserver.com/gpio/connecting-a-temperature-sensor-to-gpio.html>

