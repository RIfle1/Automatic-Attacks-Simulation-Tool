cs_stopped = False

def start_process():
    global cs_stopped
    cs_stopped = False

def stop_process():
    global cs_stopped
    cs_stopped = True

def is_stopped():
    return cs_stopped
