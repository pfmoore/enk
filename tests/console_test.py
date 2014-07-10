from enk.console import overwrite_line, append_line, ScreenLine

def test_overwrite(capsys):
    # New line - no CR
    overwrite_line("Test 1")
    out, err = capsys.readouterr()
    assert out == 'Test 1'
    overwrite_line("Test 2")
    out, err = capsys.readouterr()
    assert out == '\rTest 2'
    overwrite_line("Test 12")
    out, err = capsys.readouterr()
    assert out == '\rTest 12'
    overwrite_line("Test 1")
    out, err = capsys.readouterr()
    assert out == '\rTest 1 \b'
    append_line("OK")
    out, err = capsys.readouterr()
    assert out == 'OK'
    # New line - no CR
    overwrite_line("Test 1", newline=True)
    out, err = capsys.readouterr()
    assert out == '\nTest 1'

def padding(n):
    return (" " * n) + ("\b" * n)

def dummy_termsize():
    return 10, 10

def test_screenline_init(monkeypatch, capsys):
    monkeypatch.setattr('shutil.get_terminal_size', dummy_termsize)
    s = ScreenLine()
    s.show("")
    out, err = capsys.readouterr()
    assert out == "\r" + padding(9)
    assert err == ""

def test_screenline_write(monkeypatch, capsys):
    monkeypatch.setattr('shutil.get_terminal_size', dummy_termsize)
    s = ScreenLine()
    s.show("OK")
    out, err = capsys.readouterr()
    assert out == "\r" + "OK" + padding(7)
    assert err == ""

def test_screenline_optimise_second_write(monkeypatch, capsys):
    monkeypatch.setattr('shutil.get_terminal_size', dummy_termsize)
    s = ScreenLine()
    s.show("")
    out, err = capsys.readouterr()
    s.show("Hello")
    out, err = capsys.readouterr()
    assert out == "\r" + "Hello"
    assert err == ""

def test_screenline_toolong(monkeypatch, capsys):
    monkeypatch.setattr('shutil.get_terminal_size', dummy_termsize)
    s = ScreenLine()
    s.show("")
    out, err = capsys.readouterr()
    s.show("This is longer than six characters")
    out, err = capsys.readouterr()
    assert out == "\r" + "This i..."
    assert err == ""

def test_screenline_contextmgr(monkeypatch, capsys):
    monkeypatch.setattr('shutil.get_terminal_size', dummy_termsize)
    with ScreenLine() as s:
        s.show("Test")
    out, err = capsys.readouterr()
    assert out == "\r" + "Test" + padding(5) + "\n"
    assert err == ""

def test_screenline_final(monkeypatch, capsys):
    monkeypatch.setattr('shutil.get_terminal_size', dummy_termsize)
    with ScreenLine(final="OK") as s:
        s.show("Test")
    out, err = capsys.readouterr()
    assert out == "\r" + "Test" + padding(5) + " OK\n"
    assert err == ""
