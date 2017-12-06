#ifndef SERIAL_H_INCLUDED
#define SERIAL_H_INCLUDED

#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>
#include <stdio.h>
#include "ringbuf.h"

struct serial_api {
    size_t (*read)(uint8_t *buffer, size_t count);
    size_t (*write)(const uint8_t *buffer, size_t count);
    int (*close)(void);
};

typedef int (start_serial_fn)(struct serial_api *serial);

int windows_serial_init(struct serial_api *serial);
int linux_serial_init(struct serial_api *serial);

#endif
