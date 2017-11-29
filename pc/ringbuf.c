#include "ringbuf.h"

static size_t ringbuf_buffer_size(const struct ringbuf *rb)
{
    return rb->size;
}

static uint8_t *ringbuf_end(const struct ringbuf *rb)
{
    return rb->buf + ringbuf_buffer_size(rb);
}

static uint8_t *ringbuf_next_position(struct ringbuf *rb, uint8_t *p)
{
    assert((p >= rb->buf) && (p < ringbuf_end(rb)));
    return rb->buf + ((++p - rb->buf) % ringbuf_buffer_size(rb));
}

static size_t ringbuf_distance_to_head(struct ringbuf *rb)
{
    if (rb->tail <= rb->head) {
        return rb->head - rb->tail;
    } else {
        return (ringbuf_end(rb) - rb->tail) + (rb->head - rb->buf);
    }
}

struct ringbuf *ringbuf_new(size_t capacity)
{
    struct ringbuf *rb = malloc(sizeof(struct ringbuf));
    if (!rb) {
        return NULL;
    }
    rb->size = capacity + 1;
    rb->buf = malloc(rb->size);
    if (!rb->buf) {
        free(rb);
        return NULL;
    }
    ringbuf_reset(rb);
    return rb;
}

void ringbuf_free(struct ringbuf **rb)
{
    free((*rb)->buf);
    free(*rb);
    *rb = NULL;
}

void ringbuf_reset(struct ringbuf *rb)
{
    rb->head = rb->tail = rb->buf;
}

size_t ringbuf_read(struct ringbuf *rb, uint8_t *buf, size_t count)
{
    size_t read_bytes = 0;
    if (!rb || !buf) {
        return 0;
    }
    
    if (ringbuf_distance_to_head(rb) >= count) {
        while (count--) {
            *buf = *(rb->tail);
            rb->tail = ringbuf_next_position(rb, rb->tail);
            ++buf;
            ++read_bytes;
        }
    }
    return read_bytes;
}

size_t ringbuf_write(struct ringbuf *rb, const uint8_t *buf, size_t count)
{
    size_t written_bytes = 0;
    if (!rb || !buf) {
        return 0;
    }

    while (count--) {
        *(rb->head) = *buf;
        rb->head = ringbuf_next_position(rb, rb->head);
        ++buf;
        ++written_bytes;
    }
    return written_bytes;
}
