from subprocess import Popen, PIPE, STDOUT

def process_lines(args, **kw):
    # Ignore args we will supply
    kw['args'] = args
    kw['stdout'] = PIPE
    kw['stderr'] = STDOUT
    kw['universal_newlines'] = True

    with Popen(**kw) as proc:
        for line in proc.stdout:
            yield line
