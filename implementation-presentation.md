# ACP - Drone Sensing
## Applied Computing Project

* Teemu Ikävalko 2476629 teemu.ikavalko@student.oulu.fi (Project manager)
* Arttu Vuosku 2463849 juvuosku@student.oulu.fi
* Mauri Miettinen 2437710 mauri.miettinen@student.oulu.fi
* Valtteri Erkkilä 2425531 valtteri.erkkila@gmail.com

 #### Date of submission 16.2.2018

---

# Table of Contents

1. Introduction
2. Glossary
3. Implementation Process
4. Software Architecture
5. Hardware Documentation
6. Third Party Materials
7. Security and Privacy
8. Project Risk Assessment
9. References
10. Contributions

---

# Introduction

![Drone](http://image.helipal.com/dji-inspire-1-v2-big001.jpg)
* Design a drone that can detect and follow odors	
* Useful in detecting and locating pollution or fires
* System design & organization
    * Sensor array (Arduino) -> Sensor API (C) -> FlightSim API (Python) -> Microsoft FlightSim (Unreal Engine)
* Constraints and assumptions
    * No physical drone available!
    * No need for height changes/obstacle detection
    * Ideal work environment

---

# Glossary

* Drone
	* Unmanned remote controlled aerial vehicle (MOT Englanti © Kielikone Oy & Gummerus Kustannus Oy)
* Sensor
	* "Electronic component, module or a subsystem whose purpose is to detect events or changes in environment" [Wikipedia Sensor](https://en.wikipedia.org/wiki/Sensor)

* Microcontroller
	* Small computer used in simple calculations usually on a single circuit. [Wikipedia Microcontroller](https://en.wikipedia.org/wiki/Microcontroller)
	
* Electronic nose
	* A device intended to detect odors [Wikipedia Electronic nose](https://en.wikipedia.org/wiki/Electronic_nose)

---

# Implementation Process
1. Locating correctly working and easily obtainable sensor and development platform
2. Manufacturing sensor support structure in FabLab using a lasercutter
3. Development of Simulation software and how to input sensor readings to it
4. Logging sensor readings into text file

---

# Software Architecture

* Arduino script connects to Arduino baseplate (and hence, sensors) and reads sensors
* Custom Python API uses serial communication to receive sensor data from Arduino
* Python script connects to API, processes data and sends it to Unreal-based AirSim simulation
* AirSim provides a Python interface to a virtual drone simulation

---

# Serial communication API (Python)

* ArduinoSensors.py
* Handles serial communication with the Arduino:
    * Python sends a byte to the Arduino, which notifies the Arduino to read the sensors (every one of them).
    * The Arduino then sends back an array of sensor data to the Python script.
* Exposes an interface to the user:
    * Function for reading every sensor (e.g. get_front()), as well as opening and closing the serial connection.
    * Only requests a sensor read if necessary (i.e. two calls two the same function would result in two reads, whereas calls to different functions would be done with one read (second result is cached from the first read, expires over time)).
    * Inefficient, subject to change.

---

# Python Movement Control

* "drone_control_simulation.py"
* 3rd party Python libraries AirSimClient, parse (random, sys, getopt, datetime from standard)
* Uses AirSimClient to communicate with the Unreal process
* Object oriented approach: select with command line arguments (none, -f/--fake, -p/--playback <file>)
    * imported ArduinoSensors.py: Real time data collecting
        * Raises error if unable to connect to sensor array
    * FakeArduinoSensors: ArduinoSensors imitation providing synthetic data for testing
        * DroneSensor objects calculate intensity from distance to an imaginary fire -> exponential!
    * PlaybackArduinoSensors: ArduinoSensor imitation for playback of collected data logs
* Raises error if Unreal environment not available
* Main software loop, run until opposite intensity difference (top-bottom, left-right) is below threshold
    * Create smell direction vectors from sensor intensities
    * Issue appropriate movement commands to virtual drone
    * Read new sensor values, real or fake
* On completion, hover over final location

---

# Hardware Documentation
![Sensors](https://github.com/verkkila/ACP/blob/implementation-presentation/sensors.png)
* Arduino UNO 3
	* Calculates usable values from the sensor readings (which are voltages) and communicates with the computer
* Grove Base Shield
	* Connects the sensors to the Arduino
* 4x Grove MQ2 multipurpose gas sensor
	* Intented for gases, but will detect anything that increases conductivity in air (no information about concentrations for unknown substances)
	* Readings affected by environmental factors (humidity, temperature, wind)
	* Can be calibrated to the current environment however (setting the baseline)

---

# Third Party Materials

* AirSim ([https://github.com/Microsoft/AirSim](https://github.com/Microsoft/AirSim))
    * Python API library implementation (latest, pre-release)
    * "Neighbourhood" virtual environment v1.1.6 (required for function)

---

# Security and Privacy

* Very intimate software-to-software communication: security?
    * No wireless communication in test configuration -> attacks only on endpoints
    * IRL scenario -> multiple components connected wirelessly -> encryption! key negotiation!
* No private data storage -> low-risk environment
* Possibility of malicious entity to input large amount of gas for sensor readings in an attempt to steal or corrupt drone and sensor array in real world testing

---

# Project Risk Assessment

* Overall low-risk environment
* Drone damage: catastrophic, impossible
    * Preventative: virtual drone
    * Corrective: Component switching?
* Software data corruption: catastrophic, unlikely
    * Preventative: GitHub, multiple local copies
    * Corrective: Well thought system design -> redo if needed
* Software update for 3rd party software breaks functionality: moderate, unlikely
    * Preventative: Use stable released versions, functionality testing
    * Corrective: Documentation, modularity
* Damage to sensor array: Major, unlikely
    * Preventative: Careful handling, non-corrosive and non-dangerous testing chemicals
    * Corrective: Use measured data to replicate/simulate?

---

# References  (Work still on progress here)
[Arduino Uno](https://store.arduino.cc/usa/arduino-uno-rev3)

[Base shield V2 (for connection between arduino and sensors)](https://www.seeedstudio.com/Base-Shield-V2-p-1378.html?cPath=98_16)

[Grove - Gas Sensor MQ2](https://www.seeedstudio.com/Grove-Gas-Sensor%28MQ2%29-p-937.html)

[MQ-2 Gas Sensor datasheet](https://www.google.fi/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0ahUKEwijyOary6rZAhUF66QKHSyWCjwQFggtMAE&url=https%3A%2F%2Fwww.mouser.com%2Fds%2F2%2F321%2F605-00008-MQ-2-Datasheet-370464.pdf&usg=AOvVaw1K74YZPB3jOkxLKm4s2Kaa)

Definition for a drone: MOT Englanti © Kielikone Oy & Gummerus Kustannus Oy

[Wikipedia Electronic nose](https://en.wikipedia.org/wiki/Electronic_nose)

[Wikipedia Microcontroller](https://en.wikipedia.org/wiki/Microcontroller)

[Wikipedia Sensor](https://en.wikipedia.org/wiki/Sensor)

[Air quality monitor using arduino](https://plot.ly/arduino/air-quality-tutorial/)


---

# Contributions
FIXME
* Teemu Ikävalko (26h, xx%): Sensor support design and construction in fablab, general managing task + powerpoint
* Mauri Miettinen (31h, xx%): Python movement control, simulator functionality assessment
* Valtteri Erkkilä (32h, xx%): Sensor testing and serial API implementation
* Arttu Vuosku (9h , 9%): Planning testing phase

