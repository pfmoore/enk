from enk.filegen import build_files
import stat
import textwrap

def test_empty_file(tmpdir):
    defn = textwrap.dedent("""
        name: foo
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo').check()
    assert (tmpdir / 'foo').size() == 0

def test_empty_directory(tmpdir):
    defn = textwrap.dedent("""
        name: foo
        directory: yes
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo').check(dir=1)

def test_trailing_slash(tmpdir):
    defn = textwrap.dedent("""
        name: foo/
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo').check(dir=1)

def test_set_content(tmpdir):
    defn = textwrap.dedent("""
        name: foo
        content: bar
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo').read() == 'bar'

def test_encoding(tmpdir):
    defn = textwrap.dedent("""
        name: foo
        content: \xa3
        encoding: latin-1
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo').read() == '\xa3'

def test_encoding_utf8(tmpdir):
    defn = textwrap.dedent("""
        name: foo
        content: \xa3
        encoding: utf-8
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo').read() == '\xc2\xa3'

def test_default_encoding_is_utf8(tmpdir):
    defn = textwrap.dedent("""
        name: foo
        content: \xa3
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo').read() == '\xc2\xa3'

def test_non_ascii_filename(tmpdir):
    defn = textwrap.dedent("""
        name: foo\xa3
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo\xa3').check()

def test_multiple_files(tmpdir):
    defn = textwrap.dedent("""
        name: foo
        ---
        name: bar
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo').check()
    assert (tmpdir / 'bar').check()

def test_indented_content(tmpdir):
    defn = textwrap.dedent("""
        name: foo
        content: |
          Line 1
            Line 2
          Line 3
    """)
    build_files(defn, cwd=str(tmpdir))
    assert (tmpdir / 'foo').read() == "Line 1\n  Line 2\nLine 3\n"

