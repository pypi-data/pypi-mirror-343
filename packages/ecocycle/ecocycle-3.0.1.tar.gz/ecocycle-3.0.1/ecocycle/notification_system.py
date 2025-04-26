"""
EcoCycle - Notification System Module
Provides functionality for sending notifications and reminders to users.
"""
import os
import json
import logging
import time
import re
import datetime
from typing import Dict, List, Optional, Any, Tuple, Union
import webbrowser

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

# Import utilities
import utils
import ascii_art
import eco_tips
import smtplib
import ssl
from email.message import EmailMessage
EMAIL_SENDER = os.environ.get("GMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")


logger = logging.getLogger(__name__)

# Constants
NOTIFICATION_SETTINGS_FILE = "notification_settings.json"
NOTIFICATION_LOGS_FILE = "Logs/notification_logs.json"
EMAIL_TEMPLATES_DIR = "email_templates"


class NotificationSystem:
    """Notification system for EcoCycle application."""
    
    def __init__(self, user_manager=None, sheets_manager=None):
        """Initialize the notification system."""
        self.user_manager = user_manager
        self.sheets_manager = sheets_manager
        
        # Create directories if they don't exist
        os.makedirs(EMAIL_TEMPLATES_DIR, exist_ok=True)
        
        # Load notification settings
        self.notification_settings = self._load_notification_settings()
        self.notification_logs = self._load_notification_logs()
        
        # Create notification templates if they don't exist
        self._create_default_templates()
    
    def _load_notification_settings(self) -> Dict:
        """Load notification settings from file."""
        if os.path.exists(NOTIFICATION_SETTINGS_FILE):
            try:
                with open(NOTIFICATION_SETTINGS_FILE, 'r') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading notification settings: {e}")
        
        # Create default settings
        default_settings = {
            "default": {
                "email_notifications": False,
                "sms_notifications": False,
                "achievement_notifications": True,
                "weekly_summary": True,
                "eco_tips": True,
                "reminder_frequency": "weekly"  # none, daily, weekly, monthly
            }
        }
        
        # Save default settings
        with open(NOTIFICATION_SETTINGS_FILE, 'w') as file:
            json.dump(default_settings, file, indent=2)
        
        return default_settings
    
    def _save_notification_settings(self) -> bool:
        """Save notification settings to file."""
        try:
            with open(NOTIFICATION_SETTINGS_FILE, 'w') as file:
                json.dump(self.notification_settings, file, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving notification settings: {e}")
            return False
    
    def _load_notification_logs(self) -> Dict:
        """Load notification logs from file."""
        if os.path.exists(NOTIFICATION_LOGS_FILE):
            try:
                with open(NOTIFICATION_LOGS_FILE, 'r') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading notification logs: {e}")
        
        # Create default logs
        default_logs = {
            "email_logs": [],
            "sms_logs": [],
            "app_logs": []
        }
        
        # Save default logs
        with open(NOTIFICATION_LOGS_FILE, 'w') as file:
            json.dump(default_logs, file, indent=2)
        
        return default_logs
    
    def _save_notification_logs(self) -> bool:
        """Save notification logs to file."""
        try:
            with open(NOTIFICATION_LOGS_FILE, 'w') as file:
                json.dump(self.notification_logs, file, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving notification logs: {e}")
            return False
    
    def _create_default_templates(self) -> None:
        """Create default email templates if they don't exist."""
        templates = {
            "welcome_email.txt": """Welcome to EcoCycle, {name}!
            
Thank you for joining our community of eco-friendly cyclists. Together, we're making a difference for our planet, one bike ride at a time.

Your EcoCycle account is now active and ready to use. You can start logging your cycling trips right away and track your positive environmental impact.

Here are some quick tips to get started:
1. Log your cycling trips regularly to track your progress
2. Check your carbon footprint reduction in the statistics section
3. Use the weather and route planning features to plan your rides
4. Share your achievements with friends and family

Happy cycling!

The EcoCycle Team
""",
            "achievement_notification.txt": """Congratulations, {name}!

You've earned a new achievement: {achievement_name}

{achievement_description}

You've earned {points} eco points for this achievement. Keep up the great work!

View all your achievements in the EcoCycle app.

The EcoCycle Team
""",
            "weekly_summary.txt": """Weekly Cycling Summary for {name}

Week: {start_date} to {end_date}

Your weekly stats:
- Trips completed: {trips_count}
- Total distance: {total_distance}
- CO2 saved: {co2_saved}
- Calories burned: {calories_burned}

{comparison_text}

Eco Tip of the Week:
{eco_tip}

Keep cycling for a greener planet!

The EcoCycle Team
""",
            "reminder.txt": """Hello {name},

It's been a while since your last cycle trip. Don't forget to log your cycling activities to track your environmental impact.

Your last recorded trip was on {last_trip_date}.

Ready to get back on the saddle? The weather forecast for tomorrow is {weather_forecast}.

The EcoCycle Team
"""
        }
        
        for filename, content in templates.items():
            file_path = os.path.join(EMAIL_TEMPLATES_DIR, filename)
            if not os.path.exists(file_path):
                try:
                    with open(file_path, 'w') as file:
                        file.write(content)
                except Exception as e:
                    logger.error(f"Error creating template {filename}: {e}")
    
    def run_notification_manager(self):
        """Run the notification system interactive interface."""
        while True:
            ascii_art.clear_screen()
            ascii_art.display_header()
            ascii_art.display_section_header("Notification Manager")
            
            # Check if user is authenticated
            if not self.user_manager or not self.user_manager.is_authenticated():
                print(f"{ascii_art.Fore.YELLOW}You need to be logged in to access notification settings.{ascii_art.Style.RESET_ALL}")
                print("\nOptions:")
                print("1. Return to Main Menu")
                
                choice = input("\nSelect an option: ")
                if choice == "1":
                    break
                continue
            
            # Get current user
            user = self.user_manager.get_current_user()
            username = user.get('username')
            name = user.get('name', username)
            
            # Get user's notification settings
            if username not in self.notification_settings:
                # Copy default settings for this user
                self.notification_settings[username] = self.notification_settings["default"].copy()
                self._save_notification_settings()
            
            user_settings = self.notification_settings[username]
            
            # Display current settings
            print(f"{ascii_art.Fore.CYAN}Current Notification Settings for {name}:{ascii_art.Style.RESET_ALL}")
            print(f"Email Notifications: {ascii_art.Fore.GREEN if user_settings['email_notifications'] else ascii_art.Fore.RED}{user_settings['email_notifications']}{ascii_art.Style.RESET_ALL}")
            print(f"SMS Notifications: {ascii_art.Fore.GREEN if user_settings['sms_notifications'] else ascii_art.Fore.RED}{user_settings['sms_notifications']}{ascii_art.Style.RESET_ALL}")
            print(f"Achievement Notifications: {ascii_art.Fore.GREEN if user_settings['achievement_notifications'] else ascii_art.Fore.RED}{user_settings['achievement_notifications']}{ascii_art.Style.RESET_ALL}")
            print(f"Weekly Summary: {ascii_art.Fore.GREEN if user_settings['weekly_summary'] else ascii_art.Fore.RED}{user_settings['weekly_summary']}{ascii_art.Style.RESET_ALL}")
            print(f"Eco Tips: {ascii_art.Fore.GREEN if user_settings['eco_tips'] else ascii_art.Fore.RED}{user_settings['eco_tips']}{ascii_art.Style.RESET_ALL}")
            print(f"Reminder Frequency: {ascii_art.Fore.CYAN}{user_settings['reminder_frequency']}{ascii_art.Style.RESET_ALL}")
            
            # Show contact information if available
            email = user.get('email', 'Not set')
            phone = user.get('phone', 'Not set')
            
            print(f"\n{ascii_art.Fore.CYAN}Contact Information:{ascii_art.Style.RESET_ALL}")
            print(f"Email: {ascii_art.Fore.GREEN if email != 'Not set' else ascii_art.Fore.RED}{email}{ascii_art.Style.RESET_ALL}")
            print(f"Phone: {ascii_art.Fore.GREEN if phone != 'Not set' else ascii_art.Fore.RED}{phone}{ascii_art.Style.RESET_ALL}")
            
            # Menu options
            print("\nOptions:")
            print("1. Update Notification Settings")
            print("2. Update Contact Information")
            print("3. View Notification History")
            print("4. Test Notifications")
            print("5. Return to Main Menu")
            
            choice = input("\nSelect an option (1-5): ")
            
            if choice == "1":
                self.update_notification_settings(username)
            elif choice == "2":
                self.update_contact_information(username)
            elif choice == "3":
                self.view_notification_history(username)
            elif choice == "4":
                self.test_notifications(username)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
    
    def update_notification_settings(self, username: str) -> None:
        """Update notification settings for a user."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Update Notification Settings")
        
        user_settings = self.notification_settings[username]
        
        # Display current settings
        print(f"{ascii_art.Fore.CYAN}Current Settings:{ascii_art.Style.RESET_ALL}")
        print(f"1. Email Notifications: {user_settings['email_notifications']}")
        print(f"2. SMS Notifications: {user_settings['sms_notifications']}")
        print(f"3. Achievement Notifications: {user_settings['achievement_notifications']}")
        print(f"4. Weekly Summary: {user_settings['weekly_summary']}")
        print(f"5. Eco Tips: {user_settings['eco_tips']}")
        print(f"6. Reminder Frequency: {user_settings['reminder_frequency']}")
        print("7. Return to Notification Manager")
        
        choice = input("\nSelect a setting to update (1-7): ")
        
        if choice == "1":
            new_value = input("Enable email notifications? (y/n): ")
            user_settings['email_notifications'] = new_value.lower() == 'y'
            
            # Check if email is set
            user = self.user_manager.get_current_user()
            if user_settings['email_notifications'] and user.get('email', '') == '':
                print(f"{ascii_art.Fore.YELLOW}Warning: You have enabled email notifications but no email address is set.{ascii_art.Style.RESET_ALL}")
                print("Please update your contact information to receive email notifications.")
        
        elif choice == "2":
            new_value = input("Enable SMS notifications? (y/n): ")
            user_settings['sms_notifications'] = new_value.lower() == 'y'
            
            # Check if phone is set
            user = self.user_manager.get_current_user()
            if user_settings['sms_notifications'] and user.get('phone', '') == '':
                print(f"{ascii_art.Fore.YELLOW}Warning: You have enabled SMS notifications but no phone number is set.{ascii_art.Style.RESET_ALL}")
                print("Please update your contact information to receive SMS notifications.")
        
        elif choice == "3":
            new_value = input("Enable achievement notifications? (y/n): ")
            user_settings['achievement_notifications'] = new_value.lower() == 'y'
        
        elif choice == "4":
            new_value = input("Enable weekly summary? (y/n): ")
            user_settings['weekly_summary'] = new_value.lower() == 'y'
        
        elif choice == "5":
            new_value = input("Enable eco tips? (y/n): ")
            user_settings['eco_tips'] = new_value.lower() == 'y'
        
        elif choice == "6":
            print("Reminder frequency options:")
            print("1. None (no reminders)")
            print("2. Daily")
            print("3. Weekly")
            print("4. Monthly")
            
            freq_choice = input("Select a reminder frequency (1-4): ")
            
            if freq_choice == "1":
                user_settings['reminder_frequency'] = "none"
            elif freq_choice == "2":
                user_settings['reminder_frequency'] = "daily"
            elif freq_choice == "3":
                user_settings['reminder_frequency'] = "weekly"
            elif freq_choice == "4":
                user_settings['reminder_frequency'] = "monthly"
            else:
                print("Invalid choice. Reminder frequency not updated.")
        
        elif choice == "7":
            return
        
        else:
            print("Invalid choice. Settings not updated.")
            input("\nPress Enter to continue...")
            return
        
        # Save updated settings
        self._save_notification_settings()
        print(f"{ascii_art.Fore.GREEN}Settings updated successfully.{ascii_art.Style.RESET_ALL}")
        input("\nPress Enter to continue...")
    
    def update_contact_information(self, username: str) -> None:
        """Update contact information for a user."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Update Contact Information")
        
        user = self.user_manager.get_current_user()
        
        # Display current contact info
        current_email = user.get('email', '')
        current_phone = user.get('phone', '')
        
        print(f"{ascii_art.Fore.CYAN}Current Contact Information:{ascii_art.Style.RESET_ALL}")
        print(f"Email: {current_email if current_email else 'Not set'}")
        print(f"Phone: {current_phone if current_phone else 'Not set'}")
        
        # Options
        print("\nOptions:")
        print("1. Update Email")
        print("2. Update Phone")
        print("3. Return to Notification Manager")
        
        choice = input("\nSelect an option (1-3): ")
        
        if choice == "1":
            new_email = input("Enter your email address: ")
            
            # Simple email validation
            if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email) and new_email != '':
                print(f"{ascii_art.Fore.RED}Invalid email format. Email not updated.{ascii_art.Style.RESET_ALL}")
            else:
                user['email'] = new_email
                if self.user_manager.save_users():
                    print(f"{ascii_art.Fore.GREEN}Email updated successfully.{ascii_art.Style.RESET_ALL}")
                else:
                    print(f"{ascii_art.Fore.RED}Error updating email.{ascii_art.Style.RESET_ALL}")
        
        elif choice == "2":
            new_phone = input("Enter your phone number (e.g., +1234567890): ")
            
            # Simple phone validation
            if not re.match(r"^\+?[0-9]{10,15}$", new_phone) and new_phone != '':
                print(f"{ascii_art.Fore.RED}Invalid phone format. Phone not updated.{ascii_art.Style.RESET_ALL}")
            else:
                user['phone'] = new_phone
                if self.user_manager.save_users():
                    print(f"{ascii_art.Fore.GREEN}Phone updated successfully.{ascii_art.Style.RESET_ALL}")
                else:
                    print(f"{ascii_art.Fore.RED}Error updating phone.{ascii_art.Style.RESET_ALL}")
        
        elif choice == "3":
            return
        
        else:
            print("Invalid choice.")
        
        input("\nPress Enter to continue...")
    
    def view_notification_history(self, username: str) -> None:
        """View notification history for a user."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Notification History")
        
        # Filter logs for this user
        email_logs = [log for log in self.notification_logs['email_logs'] if log.get('username') == username]
        sms_logs = [log for log in self.notification_logs['sms_logs'] if log.get('username') == username]
        app_logs = [log for log in self.notification_logs['app_logs'] if log.get('username') == username]
        
        # Sort logs by timestamp (newest first)
        email_logs.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        sms_logs.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        app_logs.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        
        while True:
            ascii_art.clear_screen()
            ascii_art.display_header()
            ascii_art.display_section_header("Notification History")
            
            print("Select log type to view:")
            print("1. Email Notifications")
            print("2. SMS Notifications")
            print("3. In-App Notifications")
            print("4. Return to Notification Manager")
            
            choice = input("\nSelect an option (1-4): ")
            
            if choice == "1":
                # Show email logs
                if not email_logs:
                    print("No email notification history found.")
                else:
                    print(f"\n{ascii_art.Fore.CYAN}Email Notification History ({len(email_logs)} records):{ascii_art.Style.RESET_ALL}")
                    for i, log in enumerate(email_logs[:10], 1):  # Show last 10
                        timestamp = log.get('timestamp', 0)
                        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'Unknown'
                        subject = log.get('subject', 'No subject')
                        status = log.get('status', 'Unknown')
                        
                        status_color = ascii_art.Fore.GREEN if status == 'success' else ascii_art.Fore.RED
                        print(f"{i}. [{date_str}] {subject} - Status: {status_color}{status}{ascii_art.Style.RESET_ALL}")
            
            elif choice == "2":
                # Show SMS logs
                if not sms_logs:
                    print("No SMS notification history found.")
                else:
                    print(f"\n{ascii_art.Fore.CYAN}SMS Notification History ({len(sms_logs)} records):{ascii_art.Style.RESET_ALL}")
                    for i, log in enumerate(sms_logs[:10], 1):  # Show last 10
                        timestamp = log.get('timestamp', 0)
                        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'Unknown'
                        message_preview = log.get('message', 'No message')[:30] + "..." if len(log.get('message', '')) > 30 else log.get('message', 'No message')
                        status = log.get('status', 'Unknown')
                        
                        status_color = ascii_art.Fore.GREEN if status == 'success' else ascii_art.Fore.RED
                        print(f"{i}. [{date_str}] {message_preview} - Status: {status_color}{status}{ascii_art.Style.RESET_ALL}")
            
            elif choice == "3":
                # Show app logs
                if not app_logs:
                    print("No in-app notification history found.")
                else:
                    print(f"\n{ascii_art.Fore.CYAN}In-App Notification History ({len(app_logs)} records):{ascii_art.Style.RESET_ALL}")
                    for i, log in enumerate(app_logs[:10], 1):  # Show last 10
                        timestamp = log.get('timestamp', 0)
                        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'Unknown'
                        notification_type = log.get('type', 'Unknown')
                        message_preview = log.get('message', 'No message')[:30] + "..." if len(log.get('message', '')) > 30 else log.get('message', 'No message')
                        
                        print(f"{i}. [{date_str}] {notification_type}: {message_preview}")
            
            elif choice == "4":
                break
            
            else:
                print("Invalid choice.")
            
            input("\nPress Enter to continue...")
    
    def test_notifications(self, username: str) -> None:
        """Test sending notifications to a user."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Test Notifications")
        
        user = self.user_manager.get_current_user()
        name = user.get('name', username)
        user_settings = self.notification_settings[username]
        
        print("Select notification type to test:")
        print("1. Email Notification")
        print("2. SMS Notification")
        print("3. Achievement Notification")
        print("4. Return to Notification Manager")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == "1":
            # Test email notification
            if not user_settings['email_notifications']:
                print(f"{ascii_art.Fore.YELLOW}Warning: Email notifications are disabled in your settings.{ascii_art.Style.RESET_ALL}")
            
            email = user.get('email', '')
            if not email:
                print(f"{ascii_art.Fore.RED}Error: No email address set. Please update your contact information.{ascii_art.Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
            
            print(f"Sending test email to: {email}")
            
            if TQDM_AVAILABLE:
                for _ in tqdm(range(5), desc="Sending email"):
                    time.sleep(0.3)
            else:
                print("Sending email...")
                time.sleep(1.5)

            success = self.send_email(
                username=username,
                to_email=email,
                subject="EcoCycle Test Email",
                message_body=f"Hello {name},\n\nThis is a test email from EcoCycle to verify your notification settings.\n\nThe EcoCycle Team"
            )
            
            if success:
                print(f"{ascii_art.Fore.GREEN}Test email sent successfully!{ascii_art.Style.RESET_ALL}")
                print(f"Check {email} for the test email.")
            else:
                print(f"{ascii_art.Fore.RED}Error sending test email.{ascii_art.Style.RESET_ALL}")
                print("Please check your email settings and try again.")

        elif choice == "2":
            # Test SMS notification
            if not user_settings['sms_notifications']:
                print(f"{ascii_art.Fore.YELLOW}Warning: SMS notifications are disabled in your settings.{ascii_art.Style.RESET_ALL}")

            phone = user.get('phone', '')
            if not phone:
                print(f"{ascii_art.Fore.RED}Error: No phone number set. Please update your contact information.{ascii_art.Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return

            print(f"Sending test SMS to: {phone}")

            if TQDM_AVAILABLE:
                for _ in tqdm(range(5), desc="Sending SMS"):
                    time.sleep(0.3)
            else:
                print("Sending SMS...")
                time.sleep(1.5)

            # In a real application, we would use an SMS service like Twilio
            # For this demo, we'll simulate sending an SMS
            success = self._simulate_send_sms(
                username=username,
                to_phone=phone,
                message=f"EcoCycle: Hello {name}, this is a test SMS to verify your notification settings."
            )

            if success:
                print(f"{ascii_art.Fore.GREEN}Test SMS sent successfully!{ascii_art.Style.RESET_ALL}")
                print(f"Check your phone {phone} for the test SMS.")
            else:
                print(f"{ascii_art.Fore.RED}Error sending test SMS.{ascii_art.Style.RESET_ALL}")
                print("Please check your phone settings and try again.")
        
        elif choice == "3":
            # Test achievement notification
            if not user_settings['achievement_notifications']:
                print(f"{ascii_art.Fore.YELLOW}Warning: Achievement notifications are disabled in your settings.{ascii_art.Style.RESET_ALL}")
            
            # Create a test achievement
            test_achievement = {
                "name": "Test Achievement",
                "description": "This is a test achievement to verify your notification settings.",
                "points": 15,
                "icon": "🧪"
            }
            
            # Log a test achievement notification
            self._log_app_notification(
                username=username,
                notification_type="achievement",
                message=f"You've earned the {test_achievement['name']} achievement! {test_achievement['description']}"
            )
            
            print(f"{ascii_art.Fore.GREEN}Test achievement notification created!{ascii_art.Style.RESET_ALL}")
            print("You can view it in your notification history.")
            
            # If email notifications are enabled, also send an email
            if user_settings['email_notifications']:
                email = user.get('email', '')
                if email:
                    print(f"Sending achievement email to: {email}")
                    
                    # Read achievement template
                    template_path = os.path.join(EMAIL_TEMPLATES_DIR, "achievement_notification.txt")
                    if os.path.exists(template_path):
                        with open(template_path, 'r') as file:
                            template = file.read()
                        
                        # Replace placeholders
                        message = template.replace("{name}", name)
                        message = message.replace("{achievement_name}", test_achievement['name'])
                        message = message.replace("{achievement_description}", test_achievement['description'])
                        message = message.replace("{points}", str(test_achievement['points']))
                        
                        # Send email
                        self._simulate_send_email(
                            username=username,
                            to_email=email,
                            subject="EcoCycle Achievement Unlocked!",
                            message=message
                        )
            
            # If SMS notifications are enabled, also send an SMS
            if user_settings['sms_notifications']:
                phone = user.get('phone', '')
                if phone:
                    print(f"Sending achievement SMS to: {phone}")
                    
                    # Send SMS
                    self._simulate_send_sms(
                        username=username,
                        to_phone=phone,
                        message=f"EcoCycle: Congratulations {name}! You've earned the {test_achievement['name']} achievement (+{test_achievement['points']} points)."
                    )
        
        elif choice == "4":
            return
        
        else:
            print("Invalid choice.")
        
        input("\nPress Enter to continue...")

    def send_email(self, username: str, to_email: str, subject: str, message_body: str) -> bool:
        """
        Actually sends an email using Gmail SMTP.
        """
        SENDER_EMAIL = os.environ.get("GMAIL_SENDER")
        SENDER_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

        if not SENDER_EMAIL or not SENDER_PASSWORD:
            logger.error("Email sending failed: Sender email or password not configured.")
            # Log failure status
            self._log_email_attempt(username, to_email, subject, message_body, "failed", "Configuration missing")
            return False

        if not to_email:
            logger.error(f"Email sending failed for {username}: No recipient email address.")
            # Log failure status (optional, as it might not be logged if no address)
            return False

        msg = EmailMessage()
        msg.set_content(message_body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email

        context = ssl.create_default_context()
        status = "failed"
        error_msg = ""

        try:
            # Connect to Gmail's SMTP server
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                smtp.send_message(msg)
            logger.info(f"Successfully sent email to {to_email} for user {username}")
            status = "success"
            result = True

        except smtplib.SMTPAuthenticationError:
            logger.error(f"SMTP Authentication Error for {SENDER_EMAIL}. Check email/password.")
            error_msg = "SMTP Authentication Error"
            result = False
        except smtplib.SMTPException as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            error_msg = str(e)
            result = False
        except Exception as e:
            logger.error(f"Unexpected error sending email to {to_email}: {e}")
            error_msg = str(e)
            result = False

        # Log the attempt (regardless of success/failure)
        self._log_email_attempt(username, to_email, subject, message_body, status, error_msg)

        return result

    def _log_email_attempt(self, username, to_email, subject, message, status, error=""):
        """Helper function to log email attempts consistently."""
        log_entry = {
            "username": username,
            "to_email": to_email,
            "subject": subject,
            # Consider not logging the full message body for privacy/log size
            # "message": message,
            "timestamp": time.time(),
            "status": status
        }
        if error:
            log_entry["error"] = error

        self.notification_logs['email_logs'].append(log_entry)
        self._save_notification_logs()  # Be mindful of frequent writes if sending many emails

    # --- In test_notifications, change the call ---
    # Replace:
    # success = self._simulate_send_email(...)
    # With:
    # success = self._send_real_email(...)

    def _send_real_sms_via_email(self, username: str, to_phone: str, carrier_gateway: str, message_body: str) -> bool:
        """
        Sends an SMS by emailing the carrier's SMS gateway.
        Requires knowing the carrier gateway domain. VERY UNRELIABLE.
        Uses the same email credentials as _send_real_email.
        """
        SENDER_EMAIL = os.environ.get("GMAIL_SENDER")
        SENDER_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

        if not SENDER_EMAIL or not SENDER_PASSWORD:
            logger.error("SMS sending via Email failed: Sender email or password not configured.")
            self._log_sms_attempt(username, to_phone, message_body, "failed", "Email Configuration missing")
            return False

        if not to_phone or not carrier_gateway:
            logger.error(f"SMS sending via Email failed for {username}: Missing phone number or carrier gateway.")
            self._log_sms_attempt(username, to_phone, message_body, "failed", "Missing phone/gateway")
            return False

        # Basic cleaning of phone number (remove non-digits)
        cleaned_phone = re.sub(r'\D', '', to_phone)
        if not cleaned_phone:
            logger.error(f"SMS sending via Email failed for {username}: Invalid phone number format '{to_phone}'.")
            self._log_sms_attempt(username, to_phone, message_body, "failed", "Invalid phone format")
            return False

        # Construct the gateway email address
        recipient_email = f"{cleaned_phone}@{carrier_gateway}"
        logger.info(f"Attempting to send SMS via Email to: {recipient_email}")

        # Create the email message (SMS content is the body, subject often ignored/prepended)
        msg = EmailMessage()
        # Keep the body short, as gateways often have low limits
        msg.set_content(message_body[:150])  # Limit length just in case
        msg['Subject'] = ""  # Subject is often ignored or adds clutter to SMS
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email

        context = ssl.create_default_context()
        status = "failed"
        error_msg = ""
        result = False

        try:
            # Connect and send using the same SMTP logic as email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                smtp.send_message(msg)
            logger.info(f"Successfully sent SMS via Email gateway for user {username} to {recipient_email}")
            status = "success"
            result = True

        except smtplib.SMTPAuthenticationError:
            logger.error(
                f"SMTP Authentication Error for {SENDER_EMAIL} while sending SMS via Email. Check email/password.")
            error_msg = "SMTP Authentication Error"
            result = False
        except smtplib.SMTPException as e:
            logger.error(f"Error sending SMS via Email gateway to {recipient_email}: {e}")
            error_msg = str(e)
            result = False
        except Exception as e:
            logger.error(f"Unexpected error sending SMS via Email gateway to {recipient_email}: {e}")
            error_msg = str(e)
            result = False

        # Log the attempt
        self._log_sms_attempt(username, to_phone, message_body, status, error_msg)

        return result

    def _log_sms_attempt(self, username, to_phone, message, status, error=""):
        """Helper function to log SMS attempts consistently."""
        log_entry = {
            "username": username,
            "to_phone": to_phone,
            # Consider not logging the full message body for privacy/log size
            # "message": message,
            "method": "email_gateway",  # Indicate how it was sent
            "timestamp": time.time(),
            "status": status
        }
        if error:
            log_entry["error"] = error

        # Ensure sms_logs exists
        if 'sms_logs' not in self.notification_logs:
            self.notification_logs['sms_logs'] = []

        self.notification_logs['sms_logs'].append(log_entry)
        self._save_notification_logs()  # Be mindful of frequent writes
    
    def _log_app_notification(self, username: str, notification_type: str, message: str) -> None:
        """
        Log an in-app notification.
        
        Args:
            username (str): Recipient username
            notification_type (str): Type of notification (achievement, reminder, etc.)
            message (str): Notification message
        """
        log_entry = {
            "username": username,
            "type": notification_type,
            "message": message,
            "timestamp": time.time(),
            "read": False
        }
        
        self.notification_logs['app_logs'].append(log_entry)
        self._save_notification_logs()
    
    def generate_weekly_summary(self, username: str) -> bool:
        """
        Generate and send a weekly cycling summary for a user.
        
        Args:
            username (str): Username to generate summary for
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if username not in self.notification_settings:
            return False
        
        user_settings = self.notification_settings[username]
        if not user_settings['weekly_summary']:
            return False  # Weekly summary disabled
        
        user = self.user_manager.users.get(username)
        if not user:
            return False
        
        name = user.get('name', username)
        email = user.get('email', '')
        
        # Skip if no email and email notifications are enabled
        if user_settings['email_notifications'] and not email:
            return False
        
        # Get user's cycling data for the last week
        stats = user.get('stats', {})
        trips = stats.get('trips', [])
        
        # Calculate date range for last week
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=7)
        
        # Filter trips for last week
        weekly_trips = []
        for trip in trips:
            date_str = trip.get('date', '')
            if not date_str:
                continue
            
            try:
                trip_date = datetime.datetime.fromisoformat(date_str).date()
                if start_date <= trip_date <= end_date:
                    weekly_trips.append(trip)
            except (ValueError, TypeError):
                continue
        
        # Calculate weekly totals
        trips_count = len(weekly_trips)
        total_distance = sum(trip.get('distance', 0) for trip in weekly_trips)
        co2_saved = sum(trip.get('co2_saved', 0) for trip in weekly_trips)
        calories_burned = sum(trip.get('calories', 0) for trip in weekly_trips)
        
        # Skip if no trips this week
        if trips_count == 0:
            return False
        
        # Compare with previous week
        prev_start_date = start_date - datetime.timedelta(days=7)
        prev_end_date = end_date - datetime.timedelta(days=7)
        
        prev_trips = []
        for trip in trips:
            date_str = trip.get('date', '')
            if not date_str:
                continue
            
            try:
                trip_date = datetime.datetime.fromisoformat(date_str).date()
                if prev_start_date <= trip_date <= prev_end_date:
                    prev_trips.append(trip)
            except (ValueError, TypeError):
                continue
        
        prev_distance = sum(trip.get('distance', 0) for trip in prev_trips)
        
        # Create comparison text
        comparison_text = ""
        if prev_distance > 0:
            pct_change = ((total_distance - prev_distance) / prev_distance) * 100
            if pct_change > 0:
                comparison_text = f"Great job! You cycled {pct_change:.1f}% more than last week."
            elif pct_change < 0:
                comparison_text = f"You cycled {abs(pct_change):.1f}% less than last week. Let's aim higher next week!"
            else:
                comparison_text = "You maintained the same cycling distance as last week. Consistency is key!"
        else:
            comparison_text = "This is your first week of cycling data. Great start!"
        
        # Get a random eco tip
        eco_tip = eco_tips.get_random_tip().get('tip')
        
        # Format dates
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Format statistics
        total_distance_str = utils.format_distance(total_distance)
        co2_saved_str = utils.format_co2(co2_saved)
        calories_burned_str = utils.format_calories(calories_burned)
        
        # Read template
        template_path = os.path.join(EMAIL_TEMPLATES_DIR, "weekly_summary.txt")
        if os.path.exists(template_path):
            with open(template_path, 'r') as file:
                template = file.read()
            
            # Replace placeholders
            message = template.replace("{name}", name)
            message = message.replace("{start_date}", start_date_str)
            message = message.replace("{end_date}", end_date_str)
            message = message.replace("{trips_count}", str(trips_count))
            message = message.replace("{total_distance}", total_distance_str)
            message = message.replace("{co2_saved}", co2_saved_str)
            message = message.replace("{calories_burned}", calories_burned_str)
            message = message.replace("{comparison_text}", comparison_text)
            message = message.replace("{eco_tip}", eco_tip)
            
            # Send email if enabled
            if user_settings['email_notifications'] and email:
                self._simulate_send_email(
                    username=username,
                    to_email=email,
                    subject=f"Your EcoCycle Weekly Summary ({start_date_str} to {end_date_str})",
                    message=message
                )
            
            # Send SMS if enabled
            if user_settings['sms_notifications'] and user.get('phone'):
                sms_message = f"EcoCycle Weekly Summary: You completed {trips_count} trips, cycling {total_distance_str} and saving {co2_saved_str} of CO2! Keep it up!"
                self._simulate_send_sms(
                    username=username,
                    to_phone=user.get('phone'),
                    message=sms_message
                )
            
            # Log in-app notification
            self._log_app_notification(
                username=username,
                notification_type="weekly_summary",
                message=f"Your weekly cycling summary is ready! You cycled {total_distance_str} this week."
            )
            
            return True
        
        return False
    
    def send_achievement_notification(self, username: str, achievement: Dict) -> bool:
        """
        Send a notification for a new achievement.
        
        Args:
            username (str): Username to notify
            achievement (dict): Achievement details
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if username not in self.notification_settings:
            return False
        
        user_settings = self.notification_settings[username]
        if not user_settings['achievement_notifications']:
            return False  # Achievement notifications disabled
        
        user = self.user_manager.users.get(username)
        if not user:
            return False
        
        name = user.get('name', username)
        achievement_name = achievement.get('name', 'Unknown Achievement')
        achievement_description = achievement.get('description', 'No description')
        achievement_points = achievement.get('points', 0)
        
        # Log in-app notification
        self._log_app_notification(
            username=username,
            notification_type="achievement",
            message=f"Congratulations! You've earned the {achievement_name} achievement: {achievement_description}"
        )
        
        # Send email if enabled
        if user_settings['email_notifications'] and user.get('email'):
            # Read template
            template_path = os.path.join(EMAIL_TEMPLATES_DIR, "achievement_notification.txt")
            if os.path.exists(template_path):
                with open(template_path, 'r') as file:
                    template = file.read()
                
                # Replace placeholders
                message = template.replace("{name}", name)
                message = message.replace("{achievement_name}", achievement_name)
                message = message.replace("{achievement_description}", achievement_description)
                message = message.replace("{points}", str(achievement_points))
                
                self._simulate_send_email(
                    username=username,
                    to_email=user.get('email'),
                    subject=f"EcoCycle Achievement Unlocked: {achievement_name}",
                    message=message
                )
        
        # Send SMS if enabled
        if user_settings['sms_notifications'] and user.get('phone'):
            sms_message = f"EcoCycle: Congratulations {name}! You've earned the {achievement_name} achievement (+{achievement_points} points)."
            self._simulate_send_sms(
                username=username,
                to_phone=user.get('phone'),
                message=sms_message
            )
        
        return True
    
    def send_reminder(self, username: str) -> bool:
        """
        Send a reminder to users who haven't logged a trip recently.
        
        Args:
            username (str): Username to remind
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if username not in self.notification_settings:
            return False
        
        user_settings = self.notification_settings[username]
        if user_settings['reminder_frequency'] == 'none':
            return False  # Reminders disabled
        
        user = self.user_manager.users.get(username)
        if not user:
            return False
        
        name = user.get('name', username)
        
        # Get user's trip data
        stats = user.get('stats', {})
        trips = stats.get('trips', [])
        
        # Find the latest trip date
        latest_trip_date = None
        for trip in trips:
            date_str = trip.get('date', '')
            if not date_str:
                continue
            
            try:
                trip_date = datetime.datetime.fromisoformat(date_str).date()
                if latest_trip_date is None or trip_date > latest_trip_date:
                    latest_trip_date = trip_date
            except (ValueError, TypeError):
                continue
        
        # If no trips or latest trip is recent, skip reminder
        if latest_trip_date is None:
            # If no trips at all, only remind once a week
            today = datetime.date.today()
            if user_settings['reminder_frequency'] != 'weekly' and today.weekday() != 0:  # Only on Mondays
                return False
        else:
            days_since_last_trip = (datetime.date.today() - latest_trip_date).days
            
            # Check if reminder is due based on frequency setting
            if user_settings['reminder_frequency'] == 'daily' and days_since_last_trip < 2:
                return False
            elif user_settings['reminder_frequency'] == 'weekly' and days_since_last_trip < 7:
                return False
            elif user_settings['reminder_frequency'] == 'monthly' and days_since_last_trip < 30:
                return False
        
        # Format last trip date
        last_trip_date_str = latest_trip_date.strftime("%Y-%m-%d") if latest_trip_date else "Never"
        
        # Get weather forecast (in a real app, we would use the weather API)
        weather_forecast = "sunny with a high of 22°C, perfect for cycling"
        
        # Read template
        template_path = os.path.join(EMAIL_TEMPLATES_DIR, "reminder.txt")
        if os.path.exists(template_path):
            with open(template_path, 'r') as file:
                template = file.read()
            
            # Replace placeholders
            message = template.replace("{name}", name)
            message = message.replace("{last_trip_date}", last_trip_date_str)
            message = message.replace("{weather_forecast}", weather_forecast)
            
            # Send email if enabled
            if user_settings['email_notifications'] and user.get('email'):
                self._simulate_send_email(
                    username=username,
                    to_email=user.get('email'),
                    subject="EcoCycle Cycling Reminder",
                    message=message
                )
            
            # Send SMS if enabled
            if user_settings['sms_notifications'] and user.get('phone'):
                days_text = f"It's been {days_since_last_trip} days since your last cycling trip." if latest_trip_date else "You haven't logged any cycling trips yet."
                sms_message = f"EcoCycle: Hello {name}! {days_text} The forecast for tomorrow is {weather_forecast}. Let's get cycling!"
                self._simulate_send_sms(
                    username=username,
                    to_phone=user.get('phone'),
                    message=sms_message
                )
            
            # Log in-app notification
            self._log_app_notification(
                username=username,
                notification_type="reminder",
                message=f"Time to get cycling! {weather_forecast}."
            )
            
            return True
        
        return False
    
    def send_daily_eco_tip(self, username: str) -> bool:
        """
        Send a daily eco tip to a user.
        
        Args:
            username (str): Username to send tip to
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if username not in self.notification_settings:
            return False
        
        user_settings = self.notification_settings[username]
        if not user_settings['eco_tips']:
            return False  # Eco tips disabled
        
        user = self.user_manager.users.get(username)
        if not user:
            return False
        
        name = user.get('name', username)
        
        # Get today's eco tip
        tip = eco_tips.get_tip_of_the_day().get('tip')
        
        # Log in-app notification
        self._log_app_notification(
            username=username,
            notification_type="eco_tip",
            message=f"Eco Tip: {tip}"
        )
        
        # Send email if enabled
        if user_settings['email_notifications'] and user.get('email'):
            message = f"Hello {name},\n\nHere's your EcoCycle eco tip for today:\n\n{tip}\n\nSmall changes make a big difference for our planet!\n\nThe EcoCycle Team"
            self._simulate_send_email(
                username=username,
                to_email=user.get('email'),
                subject="EcoCycle Daily Eco Tip",
                message=message
            )
        
        # Send SMS if enabled
        if user_settings['sms_notifications'] and user.get('phone'):
            sms_message = f"EcoCycle Eco Tip: {tip}"
            self._simulate_send_sms(
                username=username,
                to_phone=user.get('phone'),
                message=sms_message
            )
        
        return True
    
    def process_scheduled_notifications(self) -> int:
        """
        Process all scheduled notifications for all users.
        
        Returns:
            int: Number of notifications sent
        """
        if not self.user_manager:
            return 0
        
        sent_count = 0
        today = datetime.date.today()
        
        # Process for each user
        for username, user in self.user_manager.users.items():
            # Skip guest user
            if user.get('is_guest', False):
                continue
            
            # Check if user has notification settings
            if username not in self.notification_settings:
                # Copy default settings for this user
                self.notification_settings[username] = self.notification_settings["default"].copy()
                self._save_notification_settings()
            
            # Daily eco tip (if enabled)
            if self.notification_settings[username]['eco_tips']:
                if self.send_daily_eco_tip(username):
                    sent_count += 1
            
            # Weekly summary (if it's Sunday and enabled)
            if today.weekday() == 6 and self.notification_settings[username]['weekly_summary']:
                if self.generate_weekly_summary(username):
                    sent_count += 1
            
            # Reminders based on frequency
            if self.notification_settings[username]['reminder_frequency'] != 'none':
                reminder_frequency = self.notification_settings[username]['reminder_frequency']
                
                # Daily reminders
                if reminder_frequency == 'daily':
                    if self.send_reminder(username):
                        sent_count += 1
                
                # Weekly reminders (on Mondays)
                elif reminder_frequency == 'weekly' and today.weekday() == 0:
                    if self.send_reminder(username):
                        sent_count += 1
                
                # Monthly reminders (on 1st of the month)
                elif reminder_frequency == 'monthly' and today.day == 1:
                    if self.send_reminder(username):
                        sent_count += 1
        
        return sent_count


def run_notification_manager(user_manager=None, sheets_manager=None):
    """
    Run the notification manager as a standalone module.
    
    Args:
        user_manager: User manager instance
        sheets_manager: Sheets manager instance
    """
    notification_system = NotificationSystem(user_manager, sheets_manager)
    notification_system.run_notification_manager()


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run notification manager
    run_notification_manager()