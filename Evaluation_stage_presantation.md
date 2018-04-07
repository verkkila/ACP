# ACP - Drone Sensing
## Applied Computing Project

* Teemu Ikävalko 2476629 teemu.ikavalko@student.oulu.fi (Project manager)
* Arttu Vuosku 2463849 juvuosku@student.oulu.fi
* Mauri Miettinen 2437710 mauri.miettinen@student.oulu.fi
* Valtteri Erkkilä 2425531 valtteri.erkkila@gmail.com

 #### Date of submission XX.XX.2018

---

# Table of contents
* Introduction
* Glossary
* Evaluation process
* Setup


---

# Introduction
* Design a drone that can detect and follow odors	
* Useful in detecting and locating pollution or fires
![Drone](http://image.helipal.com/dji-inspire-1-v2-big001.jpg)

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

# Evaluation Process

* Likert scale based questionnaire to find out how important people think this is
* Analysis of data logs and performance

---

# Setup

* Likert-based questionnaire
    * Focus group discussion?
    * Objective: measure general interest
    * Test procedure:
        * Recruit participants via friends
        * Google forms with an introduction and link to our presentable material
        * Rating task
    * Environment: Fully internet-based, anonymous
    * Participants: People from many areas of study
    * Data collection: Qualitative base questions rated into quantifiable interest measurement
* System module/integration testing
    * Procedure
    * Environment
    * Participants
    * Data collection
    * Features tested
    
---

# Data & Results

HERE PICTURE FROM QUESTIONNAIRE

---

# Analysis

* Overview
* Scalability
    * Simplistic but modular 
    * Any component can be easily replaced and/or fine tuned
    * Only bottleneck is the drone itself -> funtionality
* Fault tolerance:
    * If data lost in transfer, software does not function
* Security
    * No user data processed, purely software -> privacy concerns minimal
    * Technically possible to use malware to for example cath data during transfer
        * Python garbage collection?
        * Straight from USB?

---

# References

---

# Contributions

* Teemu Ikävalko (Xh, XX%): General Design and managing tasks
* Mauri Miettinen (Xh, XX%): System design
* Valtteri Erkkilä (Xh, XX%): Sensor research
* Arttu Vuosku (Xh, XX%): Looking for articles and instructions


