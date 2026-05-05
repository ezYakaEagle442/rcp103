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
from .IMessage import IMessage
from net.lecnam.rcp103.tp2.Message import Message
from net.lecnam.rcp103.tp2.EventType import EventType

try:
    print("+++ START EventImpl fire")
    msg = Message(1, "Test message", "Alice", "Bob")
    impl = EventImpl(1, msg, "SEND_MSG", datetime.datetime.now())
    horodatage = impl.get_event_time()
    print("+++ result = " + str(horodatage))
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
