#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/SimulateurTest.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.SimulateurTest
# sous Windows/PowerShell: python SimulateurTest.py

import traceback
import logging

from net.lecnam.rcp103.SimulateurImpl import SimulateurImpl

try:
    print("+++ START SimulateurTest fire")
    impl =  SimulateurImpl("Toto", 21, 42)
    result = impl.calcul(6,7)
    print("+++ result = " + str(result))
    print("+++ END SimulateurTest ignite")

except RuntimeError as error:
    print("Erreur au Runtime dans SimulateurTest")
    print(f"A {type(error).__name__} has occurred.")
    exit(42)
except Exception as exception :
        print("Exception dans SimulateurTest/Main")
        print(f"A {type(exception).__name__} has occurred.")
        print("")
        traceback.print_exc()
        print("")
        print(exception)
        exit(42)
