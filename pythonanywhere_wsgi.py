# +++++++++++ FLASK +++++++++++
import sys
import os

# Ajouter le chemin du projet au PYTHONPATH
path = '/home/Syllabic/SacTheBook'
if path not in sys.path:
    sys.path.append(path)

# Configuration Flask
from app import app as application

# Variables d'environnement pour PythonAnywhere
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = 'False'

# Application Flask
if __name__ == "__main__":
    application.run()
