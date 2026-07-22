import sys
import os

# Add root folder to sys.path so it can find models, routes, etc.
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app import create_app

app = create_app()
