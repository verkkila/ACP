#ifndef RINGBUF_H_INCLUDED
#define RINGBUF_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <string.h>

struct ringbuf {
    uint8_t *buf;
    uint8_t *head, *tail;
    size_t size;
};

struct ringbuf *ringbuf_new(size_t capacity);
void ringbuf_free(struct ringbuf **rb);
void ringbuf_reset(struct ringbuf *rb);
size_t ringbuf_read(struct ringbuf *rb, uint8_t *buf, size_t count);
size_t ringbuf_write(struct ringbuf *rb, const uint8_t *buf, size_t count);

#endif
