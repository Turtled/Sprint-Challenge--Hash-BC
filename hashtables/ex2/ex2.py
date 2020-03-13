#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_retrieve)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = []

    for i in range(len(tickets)):
        hash_table_insert(hashtable, tickets[i].source, tickets[i].destination)

    current_source = "NONE"
    for i in range(length):
        destination = hash_table_retrieve(hashtable, current_source)
        if current_source is not "NONE":
            route.append(current_source)

        #set the new source to the current destination
        current_source = hash_table_retrieve(hashtable, current_source)

    return route

