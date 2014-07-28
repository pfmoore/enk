from subprocess import Popen, PIPE, STDOUT

def process_lines(args, **kw):
    # Ignore args we will supply
    kw['args'] = args
    kw['stdout'] = PIPE
    kw['stderr'] = STDOUT
    kw['universal_newlines'] = True

    proc = Popen(**kw)
    try:
        for line in proc.stdout:
            yield line
    finally:
        if proc.stdout:
            proc.stdout.close()
        if proc.stderr:
            proc.stderr.close()
        if proc.stdin:
            proc.stdin.close()
        # Wait for the process to terminate, to avoid zombies.
        proc.wait()
