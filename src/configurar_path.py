#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

import os
import sys

def configurar_path():
    try: 
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    except Exception as e:
        print(e) 
    return sys.path

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#