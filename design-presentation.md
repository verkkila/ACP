# ACP - Drone Sensing
## Applied Computing Project

* Teemu Ikävalko 2476629 teemu.ikavalko@student.oulu.fi (Project manager)
* Arttu Vuosku 2463849 juvuosku@student.oulu.fi
* Mauri Miettinen 2437710 mauri.miettinen@student.oulu.fi
* Valtteri Erkkilä 2425531 valtteri.erkkila@gmail.com

 #### Date of submission 03.11.2017

---

# Purpose and motivation

![Drone](http://image.helipal.com/dji-inspire-1-v2-big001.jpg)

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
	* "Electronic component, module or a sybsystem whose purpose is to detect events or changes in environment" [Wikipedia Sensor](https://en.wikipedia.org/wiki/Sensor)

* Microcontroller
	* Small computer used in simple calculations usually on a single circuit. [Wikipedia Microcontroller](https://en.wikipedia.org/wiki/Microcontroller)
* Electronic nose
	* A device intended to detect odors [Wikipedia Electronic nose](https://en.wikipedia.org/wiki/Electronic_nose)
---

# Design Process
* We started by looking at previous research, specifically scientific studies and commercial products.
    - The studies gave us insight about how different odors can be identified.
    - The commercial products gave us information about different types of sensors.
* Next, we searched for suitable sensor equipment as well as development and simulation software.
    - We found plenty of options in both areas.
* After receiving the preliminary specifications from the TA, we narrowed our scope.
* Finally, we made a decision about the microcontroller and sensors we were going to use.

---

# Previous research
[FOODsniffer](http://www.myfoodsniffer.com) Electronic nose for checking if food is fresh and safe to eat.

[Sensor drone for aerial odor mapping for agriculture and security services](http://ieeexplore.ieee.org/abstract/document/7561340/?reload=true) Similar project using drone for odor mapping in agriculture.

[The eNose company](http://www.enose.nl/) Company that is specialiced in making portable and lightweight sensor applications.

[Air quality monitor using arduino](https://plot.ly/arduino/air-quality-tutorial/)

[Development of a Portable Electronic Nose System for the Detection and Classification of Fruity Odors](http://www.mdpi.com/1424-8220/10/10/9179/htm) Certain smells have "odor print"

[Concept of an electronic nose](http://www.enose.nl/rd/technology/) Multi-dimensional sensor arrays with broad odor recognition



---

# Scenario & Use case
* Scenario
	* Detecting and locating forest fires from the air
	* Drone can be easily deployed on site and start automatic search for a possible fire
	* Drone has live video feed from which the operator on the ground can verify that fire is starting or going.
* Possible use case
	* Operator activates drone and sensor
	* Drone starts automatic search procedure to find fires based on sensor data
	* Fire source activates sensor and gives drone movent commands to follow the gas trail
	* Operator verifies drone findings via onboard camera and live video to report forward

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
	* When connection is lost activation of fly home procedure begins

* All components offer extensive documentation and UI -> easy to develop
* Clear system design

---

# References

Definition for a drone: MOT Englanti © Kielikone Oy & Gummerus Kustannus Oy

[Wikipedia Electronic nose](https://en.wikipedia.org/wiki/Electronic_nose)

[Wikipedia Microcontroller](https://en.wikipedia.org/wiki/Microcontroller)

[Wikipedia Sensor](https://en.wikipedia.org/wiki/Sensor)


[Air Sensor Guidebook - United States Environmental Protection Agency](https://cfpub.epa.gov/si/si_public_file_download.cfm?p_download_id=519616)


[FOODsniffer](http://www.myfoodsniffer.com) Electronic nose for checking if food is fresh and safe to eat.

[Sensor drone for aerial odor mapping for agriculture and security services](http://ieeexplore.ieee.org/abstract/document/7561340/?reload=true) Similar project using drone for odor mapping in agriculture.

[The eNose company](http://www.enose.nl/) Company that is specialiced in making portable and lightweight sensor applications.

[Air quality monitor using arduino](https://plot.ly/arduino/air-quality-tutorial/)

[Development of a Portable Electronic Nose System for the Detection and Classification of Fruity Odors](http://www.mdpi.com/1424-8220/10/10/9179/htm) Certain smells have "odor print"

[Concept of an electronic nose](http://www.enose.nl/rd/technology/) Multi-dimensional sensor arrays with broad odor recognition

---

# Contributions

* Teemu Ikävalko (11h, 26%): General Design and managing tasks
* Mauri Miettinen (19h, 44%): System design
* Valtteri Erkkilä (9h, 21%): Sensor research
* Arttu Vuosku (4h , 9%): Looking for information

