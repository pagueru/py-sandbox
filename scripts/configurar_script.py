#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

import os
import sys

def configurar_path():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    return sys.path

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#