"""
When you run from the project root, just pipe to the src directory
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.__main__ import main

main()
