#include <SPI.h>

#define SENSOR_A0 0
#define SENSOR_A1 1
#define SENSOR_A2 2
#define SENSOR_A3 3

#define NUM_CALIBRATION_READS 100

static float R0[4] = {};

float get_voltage(float sensor_value)
{
  return sensor_value/1024.f*5.f;
}

float get_resistance(float sensor_voltage)
{
  return (5.0 - sensor_voltage) / sensor_voltage;
}

void setup()
{
  float sensor_averages[4] = {0.f, 0.f, 0.f, 0.f};
  float RS_air[4] = {0.f, 0.f, 0.f, 0.f};
  
  Serial.begin(9600);

  while (!Serial) {
    ;
  }

  /*Calibrate sensors by measuring the resistance of clean air*/
  for (int i = 0; i < NUM_CALIBRATION_READS; ++i) {
    sensor_averages[SENSOR_A0] += analogRead(SENSOR_A0);
    sensor_averages[SENSOR_A1] += analogRead(SENSOR_A1);
    sensor_averages[SENSOR_A2] += analogRead(SENSOR_A2);
    sensor_averages[SENSOR_A3] += analogRead(SENSOR_A3);
  }
  sensor_averages[SENSOR_A0] /= NUM_CALIBRATION_READS;
  sensor_averages[SENSOR_A1] /= NUM_CALIBRATION_READS;
  sensor_averages[SENSOR_A2] /= NUM_CALIBRATION_READS;
  sensor_averages[SENSOR_A3] /= NUM_CALIBRATION_READS;

  RS_air[SENSOR_A0] = get_resistance(get_voltage(sensor_averages[SENSOR_A0]));
  RS_air[SENSOR_A1] = get_resistance(get_voltage(sensor_averages[SENSOR_A1]));
  RS_air[SENSOR_A2] = get_resistance(get_voltage(sensor_averages[SENSOR_A2]));
  RS_air[SENSOR_A3] = get_resistance(get_voltage(sensor_averages[SENSOR_A3]));

  /*R0 = resistance in clean air*/
  R0[SENSOR_A0] = RS_air[SENSOR_A0]/9.8f;
  R0[SENSOR_A1] = RS_air[SENSOR_A1]/9.8f;
  R0[SENSOR_A2] = RS_air[SENSOR_A2]/9.8f;
  R0[SENSOR_A3] = RS_air[SENSOR_A3]/9.8f;
}

void loop()
{
  int sensor_values[4] = {0, 0, 0, 0};
  float ratios[4] = {0.f, 0.f, 0.f, 0.f};
  int incoming_byte = 0;

  if (Serial.available() > 0) {
    int in_byte = Serial.read();
    sensor_values[SENSOR_A0] = analogRead(SENSOR_A0);
    sensor_values[SENSOR_A1] = analogRead(SENSOR_A1);
    sensor_values[SENSOR_A2] = analogRead(SENSOR_A2);
    sensor_values[SENSOR_A3] = analogRead(SENSOR_A3);
  
    /*Ratio of "contaminated" air to clean air*/
    ratios[SENSOR_A0] = get_resistance(get_voltage(sensor_values[SENSOR_A0])) / R0[SENSOR_A0];
    ratios[SENSOR_A1] = get_resistance(get_voltage(sensor_values[SENSOR_A1])) / R0[SENSOR_A1];
    ratios[SENSOR_A2] = get_resistance(get_voltage(sensor_values[SENSOR_A2])) / R0[SENSOR_A2];
    ratios[SENSOR_A3] = get_resistance(get_voltage(sensor_values[SENSOR_A3])) / R0[SENSOR_A3];
  
    Serial.write((uint8_t*)ratios, sizeof(float) * 4);
    Serial.write('\n');
  }
}

