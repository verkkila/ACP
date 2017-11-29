#include <stdio.h>
#include <stdlib.h>
#define WIN32_LEAN_AND_MEAN
#include <Windows.h>

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
    float read_floats[4];

    if (start_serial == NULL) {
        return 1;
    }
    if (start_serial(&serial) != 0) {
        return 2;
    }
    while (true) {
        size_t read_bytes = 0;
        read_bytes = serial.read((uint8_t*)read_floats, 4*4);
        if (read_bytes != 4*4)
            continue;
        printf("%.2f ", read_floats[0]);
        printf("%.2f ", read_floats[1]);
        printf("%.2f ", read_floats[2]);
        printf("%.2f ", read_floats[3]);
        printf("\n");
#ifdef _WIN32
        Sleep(500);
#endif
    }
    serial.close();
    return 0;
}
