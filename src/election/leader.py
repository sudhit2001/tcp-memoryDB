from replication.client import connect_replicas
from election.sender import start_heartbeat
import cluster.state as state


def become_primary():

    if state.ROLE == "primary":
        return

    state.ROLE = "primary"

    print("================================")
    print("I am the new PRIMARY")
    print("================================")

    print("Connecting to replicas...")

    connect_replicas()

    print("Replica connections established.")

    start_heartbeat()
