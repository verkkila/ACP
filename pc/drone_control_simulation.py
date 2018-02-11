from AirSimClient import *
import random
import sys, getopt
import ArduinoSensors
from parse import *
import time

# This script represents the drone remote controller wih the other components being:
# 1. A fire_location
# 2. Four DroneSensors
# 3. A DroneArduino base plate
# 4. A MultirotorClient simulating the drone

fire_location = Vector3r(100,100,1.5)
MAX_REPEATS = 5 #maximum fake arduino changes
SENSOR_DIST = 0.05 #How far away the fake sensors are from the fake baseplate
ARD_HEIGHT = 0.05 #how far down fake Arduino is from the drone center
SMELL_DROPRATE_PERC = 0.99 #how much lower the fake smell is per one meter traveled, EXPONENTIAL DECREASE
INTENSITY_THRESH = 3 #what is the intensity threshold from 0-11 that drone won't try to exceed by movement
DRONE_VELOCITY = 5
FLIGHT_HEIGHT = 10
HELP_TEXT = "Use -f or --fake if you want to run a fake demo arduino"

class DroneSensor:
	'''
	Simulates a single sensor
	'''
	def __init__(self, arduino, relativepos):
		self.arduino = arduino
		self.relativepos = relativepos

	def getIntensity(self):
		'''
		Simulates data gathering
		Calculates intensity exponentially via distance to target
		'''
		mypos = Vector3r(self.arduino.getPosition().x_val + self.relativepos.x_val,self.arduino.getPosition().y_val + self.relativepos.y_val, self.arduino.getPosition().z_val + self.relativepos.z_val)
		distance = math.sqrt(math.pow(mypos.x_val - fire_location.x_val, 2) + math.pow(mypos.y_val - fire_location.y_val, 2) + math.pow(mypos.z_val - fire_location.z_val, 2))
		intensity = 11/(11 * math.pow(SMELL_DROPRATE_PERC, distance))
		return intensity
			

class FakeArduinoSensors:
	'''
	Simulates the Arduino object
	'''
	def __init__(self, drone, relativepos):
		self.sensor_front = DroneSensor(self,Vector3r(SENSOR_DIST,0,0))
		self.sensor_left = DroneSensor(self,Vector3r(0,-SENSOR_DIST,0))
		self.sensor_right = DroneSensor(self,Vector3r(0,SENSOR_DIST,0))
		self.sensor_back = DroneSensor(self,Vector3r(-SENSOR_DIST,0,0))
		self.drone = drone
		self.relativepos = relativepos
	
	def getPosition(self):
		resultvector = Vector3r()
		resultvector.x_val = self.drone.getPosition().x_val + self.relativepos.x_val
		resultvector.y_val = self.drone.getPosition().y_val + self.relativepos.y_val
		resultvector.z_val = self.drone.getPosition().z_val + self.relativepos.z_val
		return resultvector
	
	def get_front(self):
		return self.sensor_front.getIntensity()

	def get_left(self):
		return self.sensor_left.getIntensity()

	def get_right(self):
		return self.sensor_right.getIntensity()

	def get_back(self):
		return self.sensor_back.getIntensity()

class FakeArduinoSensors:
	'''
	Simulates the Arduino object
	'''
	def __init__(self, drone, relativepos):
		self.sensor_front = DroneSensor(self,Vector3r(SENSOR_DIST,0,0))
		self.sensor_left = DroneSensor(self,Vector3r(0,-SENSOR_DIST,0))
		self.sensor_right = DroneSensor(self,Vector3r(0,SENSOR_DIST,0))
		self.sensor_back = DroneSensor(self,Vector3r(-SENSOR_DIST,0,0))
		self.drone = drone
		self.relativepos = relativepos
	
	def getPosition(self):
		resultvector = Vector3r()
		resultvector.x_val = self.drone.getPosition().x_val + self.relativepos.x_val
		resultvector.y_val = self.drone.getPosition().y_val + self.relativepos.y_val
		resultvector.z_val = self.drone.getPosition().z_val + self.relativepos.z_val
		return resultvector
	
	def get_front(self):
		return self.sensor_front.getIntensity()

	def get_left(self):
		return self.sensor_left.getIntensity()

	def get_right(self):
		return self.sensor_right.getIntensity()

	def get_back(self):
		return self.sensor_back.getIntensity()

class PlaybackArduinoSensors:
    '''
    Plays a recorded file
    '''
    def __init__(self, drone, myfile):
        iterable = open(myfile,"r")
        for i in iterable.readlines():
            parsed = parse("INFO:arduino:{}: {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}", i)
            if parsed!=None:
                print(parsed.fixed)
        self.drone = drone
        
    def get_front(self):
        return 0

    def get_left(self):
        return 0

    def get_right(self):
        return 0

    def get_back(self):
        return 0

client = MultirotorClient()
mode = 0
arduino = None
playfile = None
try:
    opts, args = getopt.getopt(sys.argv[1:],"hfp:",["help","fake","playback:"])
except getopt.GetoptError:
    print(HELP_TEXT)
    sys.exit(2)
else:
    for opt,arg in opts:
        if opt in ('-h','--help'):
            print(HELP_TEXT)
            sys.exit(2)
        elif opt in ("-f", "--fake"):
            mode = 1
        else:
            playfile = arg
            mode = 2

if mode==1:
    arduino = FakeArduinoSensors(client,Vector3r(0,0,ARD_HEIGHT))
    print("Fake Arduino initialized")
elif mode==2:
    arduino = PlaybackArduinoSensors(client, playfile)
else:
    arduino = ArduinoSensors.ArduinoSensors()
    if not arduino.open():
        print("Arduino not found!")
        sys.exit(1)
    else:
        print("Arduino initialized!")

client.enableApiControl(True)
client.armDisarm(True)
client.takeoff()
client.moveToPosition(0, 0, -FLIGHT_HEIGHT, 5)

a,b,c,d = arduino.get_front(), arduino.get_left(), arduino.get_right(), arduino.get_back()
while a > INTENSITY_THRESH and b > INTENSITY_THRESH and c > INTENSITY_THRESH and d > INTENSITY_THRESH:
    vx_unscaled = a - d
    vy_unscaled = c - b
    scale_factor = math.sqrt(math.pow(vx_unscaled, 2) + math.pow(vy_unscaled, 2)) #normalization
    
    client.moveByVelocity(-vx_unscaled/scale_factor*DRONE_VELOCITY, -vy_unscaled/scale_factor*DRONE_VELOCITY, -1*np.sign(FLIGHT_HEIGHT+client.getPosition().z_val), 0.3, DrivetrainType.ForwardOnly)
    
    a,b,c,d = arduino.get_front(), arduino.get_left(), arduino.get_right(), arduino.get_back()
    if mode==1 and random.randint(1,500)==1 and MAX_REPEATS>0:
        fire_location = Vector3r(100*(random.random() * 2 - 1),100*(random.random() * 2 - 1),1.5)
        MAX_REPEATS -= 5
        print("New FIRE", fire_location.x_val, fire_location.y_val)
print("Reached maximum distance from target!")
client.hover()
