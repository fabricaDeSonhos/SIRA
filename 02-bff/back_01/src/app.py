
import os,sys
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
if rootDir not in sys.path: # add parent dir to paths
    sys.path.append(rootDir)

from src.config import *
from src.route.users import *
from src.route.rooms import *
from src.route.reservations import *

print("Application started successfully.")
