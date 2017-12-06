#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#if defined _WIN32
#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
#elif defined __unix
#include <unistd.h>
#endif

#include "serial.h"

#if defined _WIN32
    start_serial_fn *start_serial = windows_serial_init;
#elif defined __unix
    start_serial_fn *start_serial = linux_serial_init;
#else
    start_serial_fn *start_serial = NULL
#endif

struct serial_api serial;

int main(void)
{
    float sensor_data[4];
    int i = 0;

    memset(sensor_data, 0, 4*sizeof(sensor_data[0]));
    if (start_serial == NULL) {
        return 1;
    }
    if (start_serial(&serial) != 0) {
        return 2;
    }
    while (i < 10) {
        if (serial.read((uint8_t*)sensor_data, 4*sizeof(sensor_data[0])) != 0) {
            continue;
        }
        ++i;
        printf("%.2f ", sensor_data[0]);
        printf("%.2f ", sensor_data[1]);
        printf("%.2f ", sensor_data[2]);
        printf("%.2f ", sensor_data[3]);
        printf("\n");
#if defined _WIN32
        Sleep(500);
#elif defined __unix
        usleep(500*1000);
#endif
    }
    serial.close();
    return 0;
}
