#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/MessageImplTest.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.tp2.MessageImplTest
# sous Windows/PowerShell: python MessageImplTest.py

from datetime import datetime
import traceback
import logging

from net.lecnam.rcp103.tp2.EventImpl import EventImpl
from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.MessageImpl import MessageImpl

try:
    print("+++ START MessageImplTest fire")
    impl = MessageImpl(1, "Alice", "Bob", 1.21)
    src = impl.get_source()
    dst = impl.get_destination()
    print(f"Source: {src}, Destination: {dst}")
    res = impl.print_message()
    print("+++ Pretty print = " + str(res))   
    print("+++ END MessageImplTest ignite")

except RuntimeError as error:
    print("Erreur au Runtime dans MessageImplTest")
    print(f"A {type(error).__name__} has occurred.")
    exit(42)
except Exception as exception :
        print("Exception dans MessageImplTest/Main")
        print(f"A {type(exception).__name__} has occurred.")
        print("")
        traceback.print_exc()
        print("")
        print(exception)
        exit(42)
