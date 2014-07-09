import sys

last_written = 0

def overwrite_line(text, newline=False):
    global last_written
    if newline:
        sys.stdout.write('\n')
        last_written = 0
    if last_written > 0:
        sys.stdout.write('\r')
    text_len = len(text)
    sys.stdout.write(text)
    if text_len < last_written:
        clear = last_written - text_len
        sys.stdout.write(' ' * clear)
        sys.stdout.write('\b' * clear)

    last_written = text_len
    sys.stdout.flush()

def append_line(text):
    global last_written
    last_written += len(text)
    sys.stdout.write(text)
    sys.stdout.flush()
