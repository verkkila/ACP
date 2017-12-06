#ifdef __unix
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <pthread.h>
#include <sys/poll.h>
#include <stdbool.h>
#include <string.h>
#include <signal.h>
#include "serial.h"

static pthread_t serial_reader;
static int device_fd;
static struct ringbuf *rx_buffer;
static int serial_polling_active;
static pthread_mutex_t rx_buffer_lock = PTHREAD_MUTEX_INITIALIZER;

static size_t linux_read(uint8_t *buffer, size_t count)
{
    ssize_t read_bytes;
    if (!buffer || device_fd < 0) {
        return 0;
    }
    if (pthread_mutex_trylock(&rx_buffer_lock) != 0) {

    } else {
        read_bytes = ringbuf_read_from(rx_buffer, 'B', buffer, count);
        pthread_mutex_unlock(&rx_buffer_lock);
    }
    return read_bytes < 0 ? 0 : read_bytes;
}

static size_t linux_write(const uint8_t *buffer, size_t count)
{
    ssize_t written_bytes;
    written_bytes = write(device_fd, buffer, count);
    return written_bytes < 0 ? 0 : written_bytes;
}

static int linux_close(void)
{
    serial_polling_active = 0;
    pthread_join(serial_reader, NULL);
    ringbuf_free(&rx_buffer);
    return close(device_fd);
}

static int set_interface_attributes(int fd, int speed)
{
    struct termios serial_settings;
    memset(&serial_settings, 0, sizeof(serial_settings));
    if (tcgetattr(fd, &serial_settings) != 0) {
        return 1;
    }
    cfsetospeed(&serial_settings, speed);
    cfsetispeed(&serial_settings, speed);

    serial_settings.c_cflag |= (CLOCAL | CREAD);
    serial_settings.c_cflag &= ~CSIZE;
    serial_settings.c_cflag |= CS8;
    serial_settings.c_cflag &= ~PARENB;
    serial_settings.c_cflag &= ~CSTOPB;
    serial_settings.c_cflag &= ~CRTSCTS;

    serial_settings.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON);
    serial_settings.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
    serial_settings.c_oflag &= ~OPOST;

    serial_settings.c_cc[VMIN] = 1;
    serial_settings.c_cc[VTIME] = 1; /*100ms*/

    if (tcsetattr(fd, TCSANOW, &serial_settings) != 0) {
        return 2;
    }
    return 0;
}

static void *linux_serial_poll(void *params)
{
    int pollrc;
    struct pollfd serial_fds[0];
    serial_fds[0].fd = device_fd;
    serial_fds[0].events = POLLIN;
    pollrc = poll(serial_fds, 1, 1000);
    if (pollrc < 0) {
        return NULL;
    } else if (pollrc > 0) {
        while (serial_polling_active) {
            if (serial_fds[0].revents & POLLIN) {
                uint8_t read_char;
                ssize_t ret;

                ret = read(device_fd, &read_char, 1);
                if (ret > 0) {
                    pthread_mutex_lock(&rx_buffer_lock);
                    ringbuf_write(rx_buffer, &read_char, 1);
                    pthread_mutex_unlock(&rx_buffer_lock);
                }
            }
        }
    }
    (void)params;
    return NULL;
}

int linux_serial_init(struct serial_api *serial)
{
    /*TODO: no hardcoding of device name*/
    device_fd = open("/dev/ttyACM0", O_RDWR | O_NOCTTY);
    if (device_fd < 0) {
        return 1;
    }
    if (set_interface_attributes(device_fd, B9600) != 0) {
        return 2;
    }
    rx_buffer = ringbuf_new(512);
    if (!rx_buffer) {
        return 3;
    }
    serial_polling_active = 1;
    if (pthread_create(&serial_reader, NULL, linux_serial_poll, NULL) != 0) {
        return 4;
    }
    serial->read = linux_read;
    serial->write = linux_write;
    serial->close = linux_close;
    return 0;
}
#endif
