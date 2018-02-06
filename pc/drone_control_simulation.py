from AirSimClient import *
import random

'''
This script represents the drone remote controller wih the other components being:
1. A fire_location
2. Four DroneSensors
3. A DroneArduino base plate
4. A MultirotorClient simulating the drone
'''

fire_location = Vector3r(100,100,1.5)
SENSOR_DIST = 0.05 #How far away the sensors are from baseplate
ARD_HEIGHT = 0.05 #how far down Arduino is from the drone center
SMELL_DROPRATE_PERC = 0.99 #how much lower the smell is per one meter traveled, EXPONENTIAL DECREASE
MAX_INTENSITY_THRESH = 9 #what is the intensity threshold from 0-11 that drone won't try to exceed by movement
DRONE_VELOCITY = 5
FLIGHT_HEIGHT = 10 

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
		intensity = 11 * math.pow(SMELL_DROPRATE_PERC, distance)
		return intensity
			

class DroneArduino:
	'''
	Simulates the Arduino base plate
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
	
	def getData(self):
		'''
		Simulates querying the intensity value for each sensor
		'''
		return self.sensor_front.getIntensity(), self.sensor_left.getIntensity(), self.sensor_right.getIntensity(), self.sensor_back.getIntensity()

client = MultirotorClient()
client.enableApiControl(True)
client.armDisarm(True)
client.takeoff()
arduino = DroneArduino(client,Vector3r(0,0,ARD_HEIGHT))
client.moveToPosition(0, 0, -FLIGHT_HEIGHT, 5)

a,b,c,d = arduino.getData()
while a < MAX_INTENSITY_THRESH and b < MAX_INTENSITY_THRESH and c < MAX_INTENSITY_THRESH and d < MAX_INTENSITY_THRESH:
	vx_unscaled = a - d
	vy_unscaled = c - b
	scale_factor = math.sqrt(math.pow(vx_unscaled, 2) + math.pow(vy_unscaled, 2)) #normalization
	print("DRONE",client.getPosition().x_val,client.getPosition().y_val,client.getPosition().z_val)
	
	client.moveByVelocity(vx_unscaled/scale_factor*DRONE_VELOCITY, vy_unscaled/scale_factor*DRONE_VELOCITY, -1*np.sign(FLIGHT_HEIGHT+client.getPosition().z_val), 0.3, DrivetrainType.ForwardOnly)
	
	a,b,c,d = arduino.getData()
	if random.randint(1,500)==1:
		fire_location = Vector3r(100*(random.random() * 2 - 1),100*(random.random() * 2 - 1),1.5)
		print("New FIRE", fire_location.x_val, fire_location.y_val)

client.hover()
client.land()
#client.armDisarm(False)
#client.enableApiControl(False)