from AirSimClient import *

#client = MultirotorClient()
#client.confirmConnection()
#client.enableApiControl(True)
#client.armDisarm(True)
#
#AirSimClientBase.wait_key('Press any key to takeoff')
#client.takeoff()
#
#
#client.moveToPosition(-5, 5, -5, 5)
#client.moveToPosition(0, 0, -1, 1)
#client.land()
#client.armDisarm(False)
#
#client.enableApiControl(False)

fire_location = Vector3r(100,100,1.5)
SENSOR_DIST = 0.05 #How far away the sensors are from baseplate
ARD_HEIGHT = 0.05 #how far down Arduino is from the drone center
SMELL_DROPRATE_PERC = 0.99 #how much lower the smell is per one meter traveled, EXPONENTIAL DECREASE
MAX_INTENSITY = 10 #what is the intensity from 0-11 that means the drone won't get any closer


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
print("DRONE",client.getPosition().x_val,client.getPosition().y_val,client.getPosition().z_val)
print("ARDUINO",arduino.getPosition().x_val,arduino.getPosition().y_val,arduino.getPosition().z_val)
a,b,c,d = arduino.getData()
print(a, b, c, d)
client.land()
client.armDisarm(False)
client.enableApiControl(False)
