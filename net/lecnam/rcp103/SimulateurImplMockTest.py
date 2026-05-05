#!/usr/bin/python3
# PYTHONPATH=. python3 net/lecnam/rcp103/SimulateurMockImplTest.py
# Use unittest.mock to create a mock SimulateurImpl for Mock testing
# https://docs.python.org/3/library/unittest.mock.html

import traceback
import logging

from unittest.mock import MagicMock
from net.lecnam.rcp103.SimulateurImpl import SimulateurImpl

# Create a mock instance of SimulateurImpl
mock_sim = MagicMock(spec=SimulateurImpl)

# Example: set return value for calcul
mock_sim.calcul.return_value = 1,42

# Use the mock in your test
result = mock_sim.calcul(1, 2)
print("Mocked calcul result:", result)  # Output: Mocked calcul result: 1,42

# You can also assert calls
mock_sim.calcul.assert_called_with(1, 2)