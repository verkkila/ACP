#include <SPI.h>

#define SENSOR_A0 0
#define SENSOR_A1 1
#define SENSOR_A2 2
#define SENSOR_A3 3

float sensor_values[4] = {};
float sensor_voltages[4] = {};

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensor_values[SENSOR_A0] = analogRead(SENSOR_A0);
  sensor_values[SENSOR_A1] = analogRead(SENSOR_A1);
  sensor_values[SENSOR_A2] = analogRead(SENSOR_A2);
  sensor_values[SENSOR_A3] = analogRead(SENSOR_A3);
  
  sensor_voltages[SENSOR_A0] = sensor_values[SENSOR_A0]/1024.f*5.0f;
  sensor_voltages[SENSOR_A1] = sensor_values[SENSOR_A1]/1024.f*5.0f;
  sensor_voltages[SENSOR_A2] = sensor_values[SENSOR_A2]/1024.f*5.0f;
  sensor_voltages[SENSOR_A3] = sensor_values[SENSOR_A3]/1024.f*5.0f;
  
  Serial.print(sensor_voltages[SENSOR_A0]);
  Serial.print(" | ");
  Serial.print(sensor_voltages[SENSOR_A1]);
  Serial.print(" | ");
  Serial.print(sensor_voltages[SENSOR_A2]);
  Serial.print(" | ");
  Serial.print(sensor_voltages[SENSOR_A3]);
  Serial.print("\n");
  delay(1000);
}
