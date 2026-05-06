#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/EventImplTest.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.tp2.EventImplTest
# sous Windows/PowerShell: python EventImplTest.py

from datetime import datetime
import traceback
import logging

from net.lecnam.rcp103.tp2.EventImpl import EventImpl
from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.MessageImpl import MessageImpl
from net.lecnam.rcp103.tp2.EventType import EventType

try:
    print("+++ START EventImpl fire")
    msg = MessageImpl(1, "Alice", "Bob", 1.13)
    impl = EventImpl(1, msg, "SEND_MSG", 1.13) # SEND_MSG_ZZZ will force test to fail
    horodatage = impl.get_event_time()
    print("+++ result = " + str(horodatage))
    res = impl.print_event()
    print("+++ pretty print = " + str(res))
    print("+++ END EventImpl ignite")

except RuntimeError as error:
    print("Erreur au Runtime dans EventImpl")
    print(f"A {type(error).__name__} has occurred.")
    exit(42)
except Exception as exception :
        print("Exception dans EventImpl/Main")
        print(f"A {type(exception).__name__} has occurred.")
        print("")
        traceback.print_exc()
        print("")
        print(exception)
        exit(42)
