from datetime import datetime,timedelta
from application.model.model import User, db
from apscheduler.schedulers.background import BackgroundScheduler



def daily_scheduled_task():
    print(f"Task ran at midnight! Current time: {datetime.now()}")
    
    # Defined the threshold for inactivity (30 days ago)
    threshold_date = datetime.now() - timedelta(days=30)

    try :
        users = User.query.filter(User.last_login_at < threshold_date, User.active == True).all()
        for user in users:
            if user.last_login_at and user.last_login_at < threshold_date:
                # Mark the user as inactive
                user.active = False
                # Set the unactived_at time
                user.unactived_at = datetime.now()
                print(f"User {user.email} has been marked inactive.")
        
        # Commit changes to the database
        db.session.commit()
    except Exception as e:
        print(e)
        
def weekly_scheduled_task():
    print(f"Task ran at saturday(midnight)! Current time: {datetime.now()}")
    
    try:
        users = User.query.filter(User.no_of_logins > 0).all()
        for user in users:
            user.no_of_logins = 0
            print(f"User {user.email} login count reset to 0.")
        
        db.session.commit()
    except Exception as e:
        print(e)
    
        
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_scheduled_task, 'cron', hour=20, minute=0)  # Runs at midnight
    scheduler.add_job(weekly_scheduled_task, 'cron', day_of_week='fri', hour=20, minute=0) # Runs every week on sunday midnight
    scheduler.start()
    
