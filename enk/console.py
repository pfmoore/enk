import sys
import shutil

PY2_DEFAULT_TERMINAL_SIZE = 80
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

class ScreenLine:
    def __init__(self, final=""):
        try:
            self.length, ignore = shutil.get_terminal_size()
        except AttributeError:
            # Python 2 has no shutil.get_terminal_size()
            self.length = PY2_DEFAULT_TERMINAL_SIZE
        # Assume the line is dirty, so clear it on first write
        self.written = self.length - 1
        self.final = final
    def show(self, line):
        # Tidy up the input. Remove trailing space, and ignore all except the
        # last line
        line = line.rstrip()
        line = line.split("\n")[-1]
        # Truncate to screen width or less
        # Leave 4 chars, 3 for ... and 1 to avoid wrapping
        if len(line) > self.length - 4:
            line = line[:self.length - 4] + '...'
        sys.stdout.write('\r')
        text_len = len(line)
        sys.stdout.write(line)
        if text_len < self.written:
            clear = self.written - text_len
            sys.stdout.write(' ' * clear)
            sys.stdout.write('\b' * clear)
        self.written = text_len
        sys.stdout.flush()
    def finish(self, text=None):
        if not text:
            text = self.final
        if text:
            sys.stdout.write(" ")
        sys.stdout.write(text + "\n")
        sys.stdout.flush()
        self.written = 0
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, tb):
        self.finish()
