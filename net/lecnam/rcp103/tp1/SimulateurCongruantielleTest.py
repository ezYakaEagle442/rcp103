#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/tp1/SimulateurCongruantielleTest.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.tp1.SimulateurCongruantielleTest
# sous Windows/PowerShell: python SimulateurCongruantielleTest.py

import traceback
import logging

from net.lecnam.rcp103.tp1.SimulateurCongruantielle import SimulateurCongruantielle

try:
    print("+++ START SimulateurCongruantielleTest fire")
    impl =  SimulateurCongruantielle()
    
    # use case 1
    result = impl.calculUniformDiscrete()
    impl.displayFigures(result)

    # use case 2
    result = impl.calculUniformContinuous()
    impl.displayFigures(result)

    # use case 3
    result = impl.calculNormal()
    impl.displayFigures(result)

    # use case 4
    result = impl.calculExp()
    impl.displayFigures(result)
    
    # use case 5
    result = impl.displayFigures(result)
    
    print("+++ result = " + str(result))
    print("+++ END SimulateurTest ignite")

except RuntimeError as error:
    print("Erreur au Runtime dans SimulateurCongruantielleTest")
    print(f"A {type(error).__name__} has occurred.")
    exit(42)
except Exception as exception :
        print("Exception dans SimulateurCongruantielleTest/Main")
        print(f"A {type(exception).__name__} has occurred.")
        print("")
        traceback.print_exc()
        print("")
        print(exception)
        exit(42)
