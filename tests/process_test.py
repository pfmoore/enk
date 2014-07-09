import enk.process
import sys

def test_lines():
    p = enk.process.process_lines([sys.executable, '-c', 'print("Hello\\nworld")'])
    assert next(p) == 'Hello\n'
    assert next(p) == 'world\n'
