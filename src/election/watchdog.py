import threading
import time
import election.heartbeat as heartbeat
from election.failover import is_node_alive
from election.leader import become_primary
import os

TIMEOUT = 5


def watchdog():

    print("Watchdog started")

    while True:

        if not heartbeat.primary_seen:

            print("Waiting for primary...")

            time.sleep(1)

            continue

        elapsed = time.time() - heartbeat.last_heartbeat

        print(f"Watchdog: {elapsed:.2f}")

        if elapsed > TIMEOUT:
            print("Primary timeout detected!")
                
            node_id = int(os.getenv("NODE_ID"))

            if node_id == 2:

                become_primary()

            else:

                alive = is_node_alive("replica1", 5001)

                if alive:

                    print("Replica1 is alive.")
                    print("Waiting for new primary.")

                else:

                    become_primary()

            break

        time.sleep(1)


def start_watchdog():

    thread = threading.Thread(
        target=watchdog,
        daemon=True,
        name="Watchdog"
    )

    thread.start()
