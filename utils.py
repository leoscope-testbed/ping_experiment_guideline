import datetime
import subprocess

def time_now():
    now = datetime.datetime.utcnow()
    return now

def execute(name, *args, **kwargs):
    opts = [name]
    for arg in args:
        opts.append(arg)
    
    for key, val in kwargs.items():
        opts.append('-%s' % key)
        opts.append(val)      

    print(opts)
    starttime = time_now()
    output = subprocess.run(opts,
                        text=True,
                        capture_output=True)
    endtime = time_now()
    return starttime, endtime, output
