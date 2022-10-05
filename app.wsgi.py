import sys

sys.path.insert(0, "/var/www/")
activate_this = '/bin/activate_this.sh'
with open(activate_this) as file:
    exec(file.read(), dict(__file__=activate_this.py))

from main import app as application