# Inside Terminal, check version and install python packages
python3 --version
sudo apt update
sudo apt install python3-pip
sudo apt install python3-pip install pillow # for images handling

mkdir vehicleTrackingApp # create a project directory
cd vehicleTrackingApp # open directory path
python3 -m venv myenv # create a virtual environment for the project
source myenv/bin/activate # activate the virtual environment
pip install django # install django
django-admin startproject vehicleTrackingApp # start django project

python3 ./vehicleTrackingApp/manage.py runserver
# go to the browser http://127.0.0.1.8000/ to Test if django project is properely setup 

ctrl+c

# Create Applications
cd vehicleTrackingApp
python3 manage.py startapp add_vehicles
python3 manage.py startapp vehicles
python3 manage.py startapp dashboard
python3 manage.py startapp ticketing

# register Applications inside vehicleTrackingApp/settings.py file:
INSTALLED_APPS = [
    ...
    'add_vehicles',
    'dashboard',
    'ticketing',
    'vehicles',
    

    ....
    ALLOWED_HOSTS =[]
    
    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'
    
    STATIC_URL = 'static/'
    STATIC_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media' # creates media folder inside the root
]
