# ACP - Drone Sensing
## Applied Computing Project

* Teemu Ikävalko 2476629 teemu.ikavalko@student.oulu.fi (Project manager)
* Arttu Vuosku 2463849 juvuosku@student.oulu.fi
* Mauri Miettinen 2437710 mauri.miettinen@student.oulu.fi
* Valtteri Erkkilä 2425531 valtteri.erkkila@gmail.com

 #### Date of submission xx.yy.zzzz

---

# Purpose and motivation

![Drone](https://www5.djicdn.com/assets/images/products/inspire-1/banner-product-333577d35493a3213ead13b4f8056e42.png)

* Design a drone that can detect and follow odors
	* For instance locating a starting forest fire 
* Usefulness in detecting and locating pollution or fires

---

# Table of contents
0. Cover page
1. Purpose of the project
2. Glossary
3. Design Process
4. Previous research
5. Scenario & Use cases
6. System design
7. References
8. Contributions

---

# Glossary
* Drone
	* Unmanned remote controlled aerial vehicle (MOT Englanti © Kielikone Oy & Gummerus Kustannus Oy)
* Sensor
	* Electronic component, module or a sybsystem whose purpose is to detect events or changes in environment [Source](https://en.wikipedia.org/wiki/Sensor)

TODO

---

# Design Process
1. Searching for other similar types of studies
2. Where to find the neccessary sensor and simulation eguipment plus software
3. Preliminary specs from TA
4. Decision about sensors and simulators

---

# Previous research
[FOODsniffer](http://www.myfoodsniffer.com) Electronic nose for checking if food is fresh and safe to eat.

[Sensor drone for aerial odor mapping for agriculture and security services](http://ieeexplore.ieee.org/abstract/document/7561340/?reload=true) Similar project using drone for odor mapping in agriculture.

[The eNose company](http://www.enose.nl/) Company that is specialiced in making portable and lightweight sensor applications.

[Air quality monitor using arduino](https://plot.ly/arduino/air-quality-tutorial/)

[Development of a Portable Electronic Nose System for the Detection and Classification of Fruity Odors](http://www.mdpi.com/1424-8220/10/10/9179/htm) Certain smells have "odor print"

[Concept of an electronic nose](http://www.enose.nl/rd/technology/) Multi-dimensional sensor arrays with broad odor recognition

TODO

---

# Scenario & Use cases
* Scenario
	* Detecting and locating forest fires from the air
	* Drone can be easily deployed on site and start automatic search for a possible fire
	* Drone has live video feed from which the operator on the ground can verify that fire is starting or going.
* Possible use case
	* Drone and sensor are activated on the ground and Drone starts automatic search procedure
	* Drone finds a potential fire and starts to fly to it
	* Operator on the ground verifies drones findings using onboard camera and live video. 

---

# System design

* 4 base components with subcomponents
    * Drone
		* Receives movement orders from remote
	* Sensor array + microcontroller
		* Attaches to drone
		* Microcontroller program receives and processes data from sensor array
		* Sends data wirelessly to Android device using built-in libraries
	* Android device
		* Purpose-built android application (developed via DJI mobile SDK) receives sensor data and picks movement commands accordingly
		* Android application interacts with DJI drone control software and gives the drone commands
	* Remote control device
		* Signal amplification
* Developmental questions:
	* How to map sensor array data into directions?
	* Design flight patterns based on direction of pollutant?

---

# Risks and analysis

* Drone damage from testing (Major impact, unlikely) -> use simulator
* Software mostly focused on android device...Disconnect? Delay? (Medium impact, unlikely) -> testing
* Connection problems? (Major impact, possible) -> testing

* All components offer extensive documentation and UI -> easy to develop
* Clear system design

---

# References
[Wikipedia Electronic nose](https://en.wikipedia.org/wiki/Electronic_nose)

[Wikipedia Sensor](https://en.wikipedia.org/wiki/Sensor)

Air Sensor Guidebook - EPA (United States Environmental Protection Agency)

TODO

---

# Contributions

