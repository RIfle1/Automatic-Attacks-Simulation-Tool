stopped = False

def start_process():
    global stopped
    stopped = False

def stop_process():
    global stopped
    stopped = True

def is_stopped():
    return stopped
