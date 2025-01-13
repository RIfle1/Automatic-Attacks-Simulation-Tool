_stopped = False

def start_process():
    global _stopped
    _stopped = False

def stop_process():
    global _stopped
    _stopped = True

def is_stopped():
    return _stopped
