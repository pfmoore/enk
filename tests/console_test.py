from enk.console import overwrite_line, append_line

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
