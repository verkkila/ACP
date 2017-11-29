#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
#include "serial.h"

static HANDLE COM_port = NULL;
static HANDLE event_handler_thread = NULL;
static bool event_handler_running = true;
static CRITICAL_SECTION rx_buffer_lock;
static struct ringbuf *rx_buffer;

static size_t read(uint8_t *buffer, size_t count)
{
    size_t read_bytes = 0;
    EnterCriticalSection(&rx_buffer_lock);
    read_bytes = ringbuf_read(rx_buffer, buffer, count);
    LeaveCriticalSection(&rx_buffer_lock);
    return read_bytes;
}

static size_t write(const uint8_t *buffer, size_t count)
{
    DWORD written_bytes = 0, ret = 0;
    ret = WriteFile(COM_port, buffer, count, &written_bytes, NULL);
    if (ret == FALSE) {
        /*error*/
        return 0;
    }
    return written_bytes;
}

static int close(void)
{
    DWORD exit_code;
    event_handler_running = false;
    WaitForSingleObject(event_handler_thread, INFINITE);
    GetExitCodeThread(event_handler_thread, &exit_code);
    CloseHandle(event_handler_thread);
    ringbuf_free(&rx_buffer);
    CloseHandle(COM_port);
    return 0;
}

static DWORD WINAPI windows_serial_poll(void *params)
{
    DWORD event_mask;
    assert(COM_port != INVALID_HANDLE_VALUE);
    if (!SetCommMask(COM_port, EV_RXCHAR)) {
        /*error*/
    }
    while (event_handler_running) {
        if (WaitCommEvent(COM_port, &event_mask, NULL)) {
            DWORD read_bytes;
            uint8_t read_char;
            do {
                if (ReadFile(COM_port, &read_char, 1, &read_bytes, NULL) != 0) {
                    if (read_bytes > 0) {
                        EnterCriticalSection(&rx_buffer_lock);
                        ringbuf_write(rx_buffer, &read_char, 1);
                        LeaveCriticalSection(&rx_buffer_lock);
                    }
                }
            } while (read_bytes > 0);
        }
    }
    (void)params;
    return 0;
}

int windows_serial_init(struct serial_api *serial)
{
    DCB dcb_conf;
    COMMTIMEOUTS comm_timeouts;
    /*TODO: no hardcoding for COM port*/
    COM_port = CreateFile("COM6", GENERIC_READ | GENERIC_WRITE, 0, 0, OPEN_EXISTING, 0, NULL);
    if (COM_port == INVALID_HANDLE_VALUE) {
        return 1;
    }
    if (GetCommState(COM_port, &dcb_conf)) {
        dcb_conf.BaudRate = 9600;
        dcb_conf.ByteSize = 8;
        dcb_conf.Parity = NOPARITY;
        dcb_conf.StopBits = ONESTOPBIT;
        dcb_conf.fBinary = TRUE;
        dcb_conf.fParity = TRUE;
    } else {
        /*error*/
        return 2;
    }
    if (!SetCommState(COM_port, &dcb_conf)) {
        /*error*/
        return 3;
    }
    if (GetCommTimeouts(COM_port, &comm_timeouts)) {
        comm_timeouts.ReadIntervalTimeout = 500;
        comm_timeouts.ReadTotalTimeoutConstant = 1000;
        comm_timeouts.ReadTotalTimeoutMultiplier = 1;
        comm_timeouts.WriteTotalTimeoutConstant = 1000;
        comm_timeouts.WriteTotalTimeoutMultiplier = 1;
    } else {
        /*error*/
        return 4;
    }
    if (!SetCommTimeouts(COM_port, &comm_timeouts)) {
        /*error*/
        return 5;
    }
    event_handler_thread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)windows_serial_poll, NULL, 0, NULL);

    rx_buffer = ringbuf_new(512);
    if (!rx_buffer) {
        return 6;
    }

    InitializeCriticalSection(&rx_buffer_lock);

    serial->read = read;
    serial->write = write;
    serial->close = close;
    return 0;
}
