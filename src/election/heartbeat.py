import time

last_heartbeat = time.time()

primary_seen = False

def received():
    global last_heartbeat
    global primary_seen
    last_heartbeat = time.time()
    primary_seen = True
