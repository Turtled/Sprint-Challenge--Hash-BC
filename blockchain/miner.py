import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

last_proof_checked = 0
progress_before_aborted = 0

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number new_proof such that the last six digits of hash(previous_proof) are equal
    to the first six digits of hash(new_proof)
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    global last_proof_checked
    global progress_before_aborted

    #What if we started our proof NOT at 0? That way we might get lucky and get a coin before the students with faster computers.
    #How would we know when to give up and stop counting? How would we know where to start the proof?

    #looking at api/full_chain, it looks like proofs aren't usually larger than about 6 billion. We could start proof at 3 billion and stop if we don't find it before 7. 

    proof = 2500000000000#random starting point, hopefully no one else started here too

    if last_proof_checked == last_proof:
        #We gave up too soon last time! No one has found the proof yet. Let's continue from where we left off.
        print(f"{last_proof} has still not been found by other miners, continuing where we previously gave up at ({progress_before_aborted}).\n\n")
        proof = progress_before_aborted

    last_proof_checked = last_proof

    give_up = proof + 750000

    print(f"Searching for next proof between {proof:,} and {give_up:,}. That's a total of {(give_up - proof):,} guesses.\n\n")

    last_proof_hash =  hashlib.sha256(str(last_proof).encode()).hexdigest()

    while True:
        guess = str(proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        if valid_proof(last_proof_hash, guess_hash):
            break
        
        if proof > give_up:
            print("Gave up since it took a long time and someone else has probably already found it before us\n\n")
            progress_before_aborted = proof
            return None

        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start) + "\n\n")
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    #print ("Checking if the last six characters of " + str(last_hash) + " match the first six characters of " + str(proof))
    #print (str(last_hash)[len(last_hash) - 6:] + " " + str(proof)[:6])

    if str(last_hash)[len(last_hash) - 6:] == str(proof)[:6]:
        return True

    return False


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()

    time_lost_to_endpoints = 0

    # Run forever until interrupted
    while True:

        start = timer()

        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()

        if data.get('proof') == last_proof_checked:
            time_lost_to_endpoints += timer() - start
            print("We just gave up too soon, and wasted time checking /last_proof again. Total time lost to this: " + str(time_lost_to_endpoints))
            print("Adjust give_up to get this value as low as possible while still not wasting time mining while other's have already found it.\n\n")

        new_proof = proof_of_work(data.get('proof'))

        if new_proof is None:
            continue

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n================COIN FOUND=================\n\nTotal coins mined during this run: " + str(coins_mined) + "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        else:
            print(data.get('message'))
