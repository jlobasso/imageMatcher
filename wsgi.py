import sys
sys.path.insert(0, '/var/www/imageMatcher/backend')
from serverBakend import app

if __name__ == "__main__":
    app.run()