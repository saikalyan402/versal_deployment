from application.initial_scripts.schedules_script import start_scheduler
from application import create_app
from waitress import serve

app = create_app()

if __name__ == '__main__':
    start_scheduler()
#    serve(app, host='127.0.0.1', port=5000)  # No debug parameter
