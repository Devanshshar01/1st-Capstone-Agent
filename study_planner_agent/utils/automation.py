import datetime
import logging
from typing import Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
from tools.notification_tools import send_notification
from tools.progress_tools import calculate_progress_metrics
from tools.memory_tools import load_user_profile, save_user_profile

logger = logging.getLogger(__name__)

class AutomationEngine:
    """
    Handles all automation tasks for the study planner.
    Runs background jobs for reminders, progress tracking, and auto-rescheduling.
    """
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("Automation Engine initialized")
        
    def start_automation(self, user_id: str, schedule: Dict[str, Any]):
        """Start all automation tasks for a user's schedule."""
        # Schedule reminders for upcoming sessions
        self.schedule_reminders(user_id, schedule)
        
        # Schedule daily progress check
        self.schedule_progress_tracking(user_id)
        
        # Schedule auto-optimization
        self.schedule_auto_optimization(user_id)
        
        logger.info(f"Automation started for user {user_id}")
        
    def schedule_reminders(self, user_id: str, schedule: Dict[str, Any]):
        """Schedule notifications before each study session."""
        daily_schedule = schedule.get('daily_schedule', {})
        
        for date_str, sessions in daily_schedule.items():
            for session in sessions:
                # Parse session time
                session_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                start_time = session.get('start_time', '09:00')
                hour, minute = map(int, start_time.split(':'))
                
                session_datetime = session_date.replace(hour=hour, minute=minute)
                
                # Schedule reminder 15 minutes before
                reminder_time = session_datetime - datetime.timedelta(minutes=15)
                
                if reminder_time > datetime.datetime.now():
                    self.scheduler.add_job(
                        self.send_session_reminder,
                        'date',
                        run_date=reminder_time,
                        args=[user_id, session],
                        id=f"reminder_{user_id}_{date_str}_{start_time}"
                    )
                    
        logger.info(f"Scheduled {len(daily_schedule)} reminders for {user_id}")
        
    def send_session_reminder(self, user_id: str, session: Dict[str, Any]):
        """Send a notification for an upcoming session."""
        message = f"Study session starting in 15 minutes: {session['subject']} - {session['topic']}"
        send_notification(user_id, {
            "title": "📚 Study Session Reminder",
            "message": message
        })
        logger.info(f"Sent reminder to {user_id}: {message}")
        
    def schedule_progress_tracking(self, user_id: str):
        """Schedule daily progress tracking."""
        # Run every day at 8 PM
        self.scheduler.add_job(
            self.track_daily_progress,
            'cron',
            hour=20,
            minute=0,
            args=[user_id],
            id=f"progress_{user_id}"
        )
        logger.info(f"Scheduled daily progress tracking for {user_id}")
        
    def track_daily_progress(self, user_id: str):
        """Automatically track and update progress."""
        try:
            metrics = calculate_progress_metrics(user_id)
            profile = load_user_profile(user_id)
            
            if 'progress_history' not in profile:
                profile['progress_history'] = []
                
            profile['progress_history'].append({
                "date": datetime.date.today().isoformat(),
                "metrics": metrics
            })
            
            save_user_profile(user_id, profile)
            
            # Send daily summary
            send_notification(user_id, {
                "title": "📊 Daily Progress Update",
                "message": f"Overall progress: {int(metrics.get('overall_progress', 0) * 100)}%"
            })
            
            logger.info(f"Tracked daily progress for {user_id}")
        except Exception as e:
            logger.error(f"Error tracking progress: {e}")
            
    def schedule_auto_optimization(self, user_id: str):
        """Schedule automatic schedule optimization."""
        # Run every Sunday at 7 PM
        self.scheduler.add_job(
            self.optimize_schedule,
            'cron',
            day_of_week='sun',
            hour=19,
            minute=0,
            args=[user_id],
            id=f"optimize_{user_id}"
        )
        logger.info(f"Scheduled weekly optimization for {user_id}")
        
    def optimize_schedule(self, user_id: str):
        """Automatically optimize schedule based on performance."""
        try:
            profile = load_user_profile(user_id)
            
            # Analyze performance and adjust
            # This is a simplified version - in production, use ML/AI
            weak_areas = []
            metrics = calculate_progress_metrics(user_id)
            
            for subject, progress in metrics.get('subjects', {}).items():
                if progress < 0.5:  # Less than 50% progress
                    weak_areas.append(subject)
                    
            if weak_areas:
                message = f"Identified weak areas: {', '.join(weak_areas)}. Increasing study time for these subjects."
                send_notification(user_id, {
                    "title": "🎯 Schedule Optimized",
                    "message": message
                })
                
            logger.info(f"Optimized schedule for {user_id}")
        except Exception as e:
            logger.error(f"Error optimizing schedule: {e}")
            
    def auto_reschedule_missed(self, user_id: str, missed_session: Dict[str, Any]):
        """Automatically reschedule a missed session."""
        try:
            profile = load_user_profile(user_id)
            schedule = profile.get('current_schedule', {})
            daily_schedule = schedule.get('daily_schedule', {})
            
            # Find next available slot
            tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
            
            if tomorrow not in daily_schedule:
                daily_schedule[tomorrow] = []
                
            # Add makeup session
            makeup_session = missed_session.copy()
            makeup_session['topic'] = f"{makeup_session['topic']} (Makeup)"
            daily_schedule[tomorrow].append(makeup_session)
            
            profile['current_schedule']['daily_schedule'] = daily_schedule
            save_user_profile(user_id, profile)
            
            send_notification(user_id, {
                "title": "🔄 Session Rescheduled",
                "message": f"Automatically rescheduled: {missed_session['subject']} for tomorrow"
            })
            
            logger.info(f"Auto-rescheduled session for {user_id}")
        except Exception as e:
            logger.error(f"Error auto-rescheduling: {e}")
            
    def shutdown(self):
        """Gracefully shutdown the automation engine."""
        self.scheduler.shutdown()
        logger.info("Automation Engine shut down")
