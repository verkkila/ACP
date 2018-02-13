# ACP - Drone Sensing
## Applied Computing Project

* Teemu Ikävalko 2476629 teemu.ikavalko@student.oulu.fi (Project manager)
* Arttu Vuosku 2463849 juvuosku@student.oulu.fi
* Mauri Miettinen 2437710 mauri.miettinen@student.oulu.fi
* Valtteri Erkkilä 2425531 valtteri.erkkila@gmail.com

 #### Date of submission NO

---

# Table of Contents

1. Introduction
2. Glossary
3. Implementation Process
4. Software Architecture
5. Data Structures
6. Hardware Documentation
7. Third Party Materials
8. Security and Privacy
9. Project Risk Assessment
10. References
11. Contributions

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

# Glossary (FIXME: ARE THESE NECESSARY?)

* Drone
	* Unmanned remote controlled aerial vehicle (MOT Englanti © Kielikone Oy & Gummerus Kustannus Oy)
* Sensor
	* "Electronic component, module or a sybsystem whose purpose is to detect events or changes in environment" [Wikipedia Sensor](https://en.wikipedia.org/wiki/Sensor)

* Microcontroller
	* Small computer used in simple calculations usually on a single circuit. [Wikipedia Microcontroller](https://en.wikipedia.org/wiki/Microcontroller)
	
* Electronic nose
	* A device intended to detect odors [Wikipedia Electronic nose](https://en.wikipedia.org/wiki/Electronic_nose)

---

# Implementation Process
1. Locating correctly working and easily optaineable sensor and development platform
2. Manufacturing sensor support structure in Fablan using Lasercutter
3. Development of Simulation software and how to input sensor readings to it
4. Logging sensor readings into text file

---

# Software Architecture

* Arduino script connects to Arduino baseplate (and hence, sensors) and reads sensors
* Custom Python API uses serial communication to receive sensor data from Arduino
* Python script connects to API, processes data and sends it to Unreal-based AirSim simulation
* Airsim provides a Python interface to a virtual drone simulation

---

# Python API

* ArduinoSensors.py
* object
* FIXME VALTTERI
* Functions
    * get_left and such??

---

# Python Movement Control

* "drone_control_simulation.py"
* 3rd party Python libraries AirSimClient, parse (random, sys, getopt, datetime from standard)
* Uses AirSimClient to communicate with the Unreal process
* Object oriented approach: select with command line arguments
    * imported ArduinoSensors: Real time data collecting
        * Raises error if unable to connect to sensor array
    * FakeArduinoSensors: ArduinoSensosrs pseudo-duplicate for synthetic data for testing
        * DroneSensor objects calculate intensity from distance to an imaginary fire -> exponential!
    * PlaybackArduinoSensors: ArduinoSensor pseudo-duplicate for playback of collected data logs
* Raises error if Unreal environment not available
* Main software loop, run until opposite intensity difference is below threshold
    * Create smell direction vectors from sensor intensities
    * Issue appropriate movement commands to virtual drone
    * Read new sensor values, real or fake
* On completion, hover over final location

---

# Hardware Documentation
* Grove MQ2 multipurpose gas sensor (whole array concist 4 of these)
	* Sensors readings depends heavily on ambient temperature and wind conditions usage possible only in controlled environments
* Arduido base development kit

---

# Third Party Materials

* AirSim ([https://github.com/Microsoft/AirSim](https://github.com/Microsoft/AirSim))
    * Python API library implementation (latest, pre-release)
    * "Neighbourhood" virtual environment v1.1.6

---

# Security and Privacy

* Very intimate software-to-software communication: security?
    * No wireless communication in test configuration -> attacks only on endpoints
    * IRL scenario -> multiple components connected wirelessly -> encryption! key negotiation!
* No private data storage -> low-risk environment

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

# References

---

# Contributions
FIXME
* Teemu Ikävalko (11h, 26%): General Design and managing tasks
* Mauri Miettinen (19h, 44%): System design
* Valtteri Erkkilä (9h, 21%): Sensor research
* Arttu Vuosku (4h , 9%): Looking for articles and instructions

