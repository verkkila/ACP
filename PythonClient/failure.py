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

fire_locations = [Vector3r(100,100,1.5)]
SENSOR_DIST = 0.05
ARD_HEIGHT = 0.05

class DroneSensor:
	def __init__(self, arduino, relativepos):
		self.arduino = arduino
		self.relativepos = relativepos

	def getData(self):
		pass

class DroneArduino:
	def __init__(self, drone, relativepos):
		self.sensor_front = DroneSensor(self,Vector3r(SENSOR_DIST,0,0))
		self.sensor_left = DroneSensor(self,Vector3r(0,-SENSOR_DIST,0))
		self.sensor_right = DroneSensor(self,Vector3r(0,SENSOR_DIST,0))
		self.sensot_back = DroneSensor(self,Vector3r(-SENSOR_DIST,0,0))
		self.drone = drone
		self.relativepos = relativepos
	
	def getPosition(self):
		resultvector = Vector3r(0,0,0)
		resultvector.x_val = self.drone.getPosition().x_val + self.relativepos.x_val
		resultvector.y_val = self.drone.getPosition().y_val + self.relativepos.y_val
		resultvector.z_val = self.drone.getPosition().z_val + self.relativepos.z_val
		return resultvector

client = MultirotorClient()
client.enableApiControl(True)
client.armDisarm(True)
client.takeoff()
arduino = DroneArduino(client,Vector3r(0,0,ARD_HEIGHT))
#print("DRONE",client.getPosition().x_val,client.getPosition().y_val,client.getPosition().z_val)
#print("ARDUINO",arduino.getPosition().x_val,arduino.getPosition().y_val,arduino.getPosition().z_val)
client.land()
client.armDisarm(False)
client.enableApiControl(False)
