#include "serial.h"

static size_t read(uint8_t *buffer, size_t count)
{
    (void)buffer;
    (void)count;
    return 0;
}

static size_t write(const uint8_t *buffer, size_t count)
{
    (void)buffer;
    (void)count;
    return 0;
}

static int close(void)
{
    return 0;
}

int linux_serial_init(struct serial_api *serial)
{
    serial->read = read;
    serial->write = write;
    serial->close = close;
    return 0;
}
