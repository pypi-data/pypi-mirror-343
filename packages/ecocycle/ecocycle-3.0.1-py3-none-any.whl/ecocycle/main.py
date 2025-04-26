"""
EcoCycle - Main Application Module
A command-line dashboard for cycling and environmental data tracking
with Google Sheets integration.
"""
import os
import sys
import logging
import argparse
import getpass
import importlib.util
import subprocess
import random
import time
import json
import hmac
import hashlib
from logging.handlers import RotatingFileHandler
from user_manager import SESSION_FILE, SESSION_SECRET_ENV_VAR
from typing import Dict, List, Optional, Any, Tuple, Union

if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm'

# --- Define Log Directory and File Path ---
# Determine the project root directory (where main.py is located)
project_root = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(project_root, 'Logs')
LOG_FILE = os.path.join(LOG_DIR, 'ecocycle.log')

try:
    # Create the directory if it doesn't exist.
    # os.makedirs creates parent directories as needed.
    # exist_ok=True prevents an error if the directory already exists.
    os.makedirs(LOG_DIR, exist_ok=True)
    # Optional: Print a message to confirm (useful for debugging)
    # print(f"Log directory '{LOG_DIR}' checked/created.", file=sys.stderr)
except OSError as e:
    # Handle potential errors during directory creation (e.g., permissions)
    print(f"Error: Could not create log directory '{LOG_DIR}'. {e}", file=sys.stderr)
    # Decide if you want to exit or continue without file logging
    # sys.exit(1) # Uncomment to exit if log dir creation fails
except Exception as e:
    print(f"Unexpected error creating log directory '{LOG_DIR}': {e}", file=sys.stderr)
    # sys.exit(1)

# Configure logger
logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO, # Keep overall level at INFO for file logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/ecocycle.log')
        # We will configure the StreamHandler separately
    ]
)

# Configure console handler separately to control its level
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.ERROR) # Set console level to ERROR
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the root logger
logging.getLogger('').addHandler(console_handler)

# Create a separate debug log file
debug_handler = logging.FileHandler('Logs/ecocycle_debug.log')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(debug_handler)

# Constants
REQUIRED_PACKAGES = ['colorama']
OPTIONAL_PACKAGES = ['dotenv', 'requests', 'tqdm', 'tabulate', 'matplotlib', 'folium']
GOOGLE_SHEETS_AVAILABLE = False


def setup_environment():
    """Set up environment variables from .env file."""
    try:
        import dotenv
        dotenv.load_dotenv()
        logger.info("Environment variables loaded from .env file")
    except ImportError:
        logger.warning("python-dotenv not installed, environment variables not loaded from .env file")


def is_package_installed(package_name):
    """Checks if a package is installed without importing it."""
    return importlib.util.find_spec(package_name) is not None


def install_packages(packages, essential=False):
    """
    Installs or upgrades a list of packages using pip.
    Handles errors and essential package requirements.
    Returns True if all essential packages are available/installed.
    """
    for package in packages:
        if not is_package_installed(package):
            logger.info(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                logger.info(f"Successfully installed {package}")
            except subprocess.CalledProcessError:
                logger.error(f"Failed to install {package}")
                if essential:
                    return False
    return True


def import_local_modules():
    """Import local modules after ensuring all dependencies are installed."""
    global GOOGLE_SHEETS_AVAILABLE
    
    # These are always required
    # Try to use enhanced ASCII art if available
    try:
        import enhanced_ascii_art as ascii_art
        # print("Using enhanced UI with animations") # Commented out
    except ImportError:
        import ascii_art
        print("Using standard UI (enhanced UI not available)")
    
    import utils
    import user_manager
    import eco_tips
    
    # Try to import optional modules
    try:
        import sheets_manager
        GOOGLE_SHEETS_AVAILABLE = sheets_manager.GOOGLE_SHEETS_AVAILABLE
    except ImportError:
        logger.warning("sheets_manager module not available")
        GOOGLE_SHEETS_AVAILABLE = False
    
    # Initialize module dictionary
    modules = {
        'ascii_art': ascii_art,
        'utils': utils,
        'user_manager': user_manager,
        'eco_tips': eco_tips,
        'sheets_manager': sheets_manager if GOOGLE_SHEETS_AVAILABLE else None
    }
    
    # Try to import new feature modules
    try:
        import eco_challenges
        modules['eco_challenges'] = eco_challenges
    except ImportError:
        logger.warning("eco_challenges module not available")
    
    try:
        import carbon_impact_tracker
        modules['carbon_impact_tracker'] = carbon_impact_tracker
    except ImportError:
        logger.warning("carbon_impact_tracker module not available")
    
    try:
        import ai_route_planner
        modules['ai_route_planner'] = ai_route_planner
    except ImportError:
        logger.warning("ai_route_planner module not available")
    
    return modules


def check_existing_session(user_manager_instance):
    """
    Checks for a saved session file, validates its contents using HMAC,
    and logs the user in if the session is valid and the user exists.

    Args:
        user_manager_instance: An initialized instance of UserManager.

    Returns:
        The username (str) if the session is valid, otherwise None.
    """
    logger.debug(f"Checking for existing session file: {SESSION_FILE}")
    if not os.path.exists(SESSION_FILE):
        logger.info("No existing session file found.")
        return None

    try:
        with open(SESSION_FILE, 'r') as f:
            session_data = json.load(f)

        stored_username = session_data.get("username")
        stored_verifier = session_data.get("session_verifier")

        if not stored_username or not stored_verifier:
            logger.warning(f"Session file {SESSION_FILE} is incomplete or corrupted. Clearing.")
            user_manager_instance._clear_session() # Clear invalid file
            return None

        logger.debug(f"Session file found for user '{stored_username}'. Verifying...")

        # --- Verification using HMAC ---
        secret = user_manager_instance._get_session_secret()
        if not secret:
             # Critical error logged within _get_session_secret
             logger.error("Cannot verify session: Secret key is missing. Clearing potentially invalid session.")
             user_manager_instance._clear_session() # Clear if key missing
             return None

        # Recalculate the expected verifier based on the stored username
        expected_verifier = user_manager_instance._calculate_verifier(stored_username)
        if not expected_verifier:
            logger.error(f"Could not calculate expected verifier for user '{stored_username}'. Clearing session.")
            user_manager_instance._clear_session()
            return None

        # Securely compare the stored and expected verifiers
        # hmac.compare_digest is crucial to prevent timing attacks
        if not hmac.compare_digest(stored_verifier, expected_verifier):
            logger.warning(f"Session verifier mismatch for user '{stored_username}'. Possible tampering or key change. Clearing session.")
            user_manager_instance._clear_session()
            return None
        # --- End Verification ---

        logger.debug(f"Session verifier for '{stored_username}' is valid.")

        # Final check: Does the user still exist in the user database?
        # Need to access the loaded users dictionary in UserManager
        if stored_username in user_manager_instance.users:
            logger.info(f"Found valid and verified session for user '{stored_username}'. Logging in automatically.")
            # Set the user as logged in within the UserManager instance
            user_manager_instance.current_user = stored_username
            return stored_username
        else:
            logger.warning(f"User '{stored_username}' from verified session file no longer exists in user data. Clearing session.")
            user_manager_instance._clear_session()
            return None

    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from session file {SESSION_FILE}. Clearing session.")
        user_manager_instance._clear_session()
        return None
    except FileNotFoundError:
        logger.info("Session file disappeared during check.")
        return None
    except Exception as e:
        # Catch other potential errors (permissions, etc.)
        logger.error(f"Error reading or verifying session file {SESSION_FILE}: {e}", exc_info=True)
        # Consider clearing the session file here too for safety, depending on the error
        # user_manager_instance._clear_session()
        return None


def show_main_menu(user_manager_instance):
    """Display the main menu and handle user input."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    eco_tips = modules['eco_tips']
    
    while True:
        ascii_art.clear_screen()
        ascii_art.display_header()
        
        # Show daily eco tip
        daily_tip = eco_tips.get_daily_tip()
        print(f"\n{ascii_art.Fore.GREEN}Eco Tip of the Day:{ascii_art.Style.RESET_ALL} {daily_tip}\n")
        
        # Display user info
        if user_manager_instance.is_authenticated():
            user = user_manager_instance.get_current_user()
            if user_manager_instance.is_guest():
                print(f"Logged in as: Guest User")
            else:
                name = user.get('name', user.get('username', 'Unknown'))
                print(f"Logged in as: {name}")
                
                # Show user stats if available
                stats = user.get('stats', {})
                if stats:
                    total_trips = stats.get('total_trips', 0)
                    total_distance = stats.get('total_distance', 0.0)
                    total_co2_saved = stats.get('total_co2_saved', 0.0)
                    total_calories = stats.get('total_calories', 0)
                    
                    print(f"Stats: {total_trips} trips, {total_distance:.1f} km, "
                          f"{total_co2_saved:.2f} kg CO2 saved, {total_calories} kcal burned")
        else:
            print("Not logged in")
        
        # Display menu options
        options = [
            "Log a cycling trip",
            "View statistics",
            "Calculate carbon footprint",
            "Weather and route planning",
            "Eco-challenges",
            "Settings and preferences",
            "Social sharing and achievements",
            "Manage notifications",
        ]
        
        # Add admin option for admin users
        if user_manager_instance.is_authenticated() and user_manager_instance.is_admin():
            options.append("Admin panel")
        
        # Add login/logout option
        if user_manager_instance.is_authenticated():
            options.append("Logout")
        else:
            options.append("Login")
        
        # Display menu with the yellow "0. Exit" option
        ascii_art.display_section_header("Main Menu")
        
        # Display "0. Exit" option first
        print(f"  {ascii_art.Fore.YELLOW}0. Exit{ascii_art.Style.RESET_ALL}")
        
        # Display other menu options
        for i, option in enumerate(options):
            print(f"  {i+1}. {option}")
        
        print()
        
        # Get user choice
        choice = input("Select an option (0-{}): ".format(len(options)))
        
        try:
            choice = int(choice)
            if choice == 0:  # Exit option
                ascii_art.clear_screen()
                ascii_art.display_header()
                print("\nThank you for using EcoCycle! Goodbye.")
                sys.exit(0)
            elif 1 <= choice <= len(options):
                if options[choice-1] == "Log a cycling trip":
                    log_cycling_trip(user_manager_instance)
                elif options[choice-1] == "View statistics":
                    view_statistics(user_manager_instance)
                elif options[choice-1] == "Calculate carbon footprint":
                    calculate_carbon_footprint(user_manager_instance)
                elif options[choice-1] == "Weather and route planning":
                    weather_route_planner(user_manager_instance)
                elif options[choice-1] == "Eco-challenges":
                    eco_challenges(user_manager_instance)
                elif options[choice-1] == "Settings and preferences":
                    settings_preferences(user_manager_instance)
                elif options[choice-1] == "Social sharing and achievements":
                    social_sharing(user_manager_instance)
                elif options[choice-1] == "Manage notifications":
                    notifications(user_manager_instance)
                elif options[choice-1] == "Admin panel":
                    admin_panel(user_manager_instance)
                elif options[choice-1] == "Login":
                    user_manager_instance.authenticate()
                elif options[choice-1] == "Logout":
                    user_manager_instance.logout()
                    print("Logged out successfully.")
                    input("Press Enter to continue...")
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")


def log_cycling_trip(user_manager_instance):
    """Log a new cycling trip."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    utils = modules['utils']
    
    ascii_art.clear_screen()
    ascii_art.display_header()
    ascii_art.display_section_header("Log Cycling Trip")
    
    # Check if user is authenticated
    if not user_manager_instance.is_authenticated():
        print("You need to log in to record cycling trips.")
        input("Press Enter to continue...")
        return
    
    # Get user data
    date = input("Date (YYYY-MM-DD, or press Enter for today): ")
    
    # Validate date format if provided
    if date:
        import re
        from datetime import datetime
        
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            ascii_art.display_error_message("Invalid date format. Use YYYY-MM-DD.")
            input("\nPress Enter to return to the main menu...")
            return
        
        # Verify it's a valid date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            ascii_art.display_error_message("Invalid date. Please enter a valid date.")
            input("\nPress Enter to return to the main menu...")
            return
    else:
        # Default to today
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Get trip data
    try:
        # Get and validate distance (must be positive)
        distance_input = input("Distance (km): ")
        distance = float(distance_input)
        if distance <= 0:
            raise ValueError("Distance must be positive")
        
        # Get and validate duration (must be positive)
        duration_input = input("Duration (minutes): ")
        duration = float(duration_input)
        if duration <= 0:
            raise ValueError("Duration must be positive")
        
        # Calculate average speed
        speed = utils.calculate_average_speed(distance, duration)
        
        # Get user weight from preferences or input
        weight = user_manager_instance.get_user_preference('weight_kg', None)
        if weight is None:
            weight_input = input("Your weight (kg) for calorie calculation: ")
            weight = float(weight_input)
            
            # Validate weight (must be positive and reasonable)
            if weight <= 0 or weight > 300:
                raise ValueError("Weight must be positive and reasonable")
                
            # Save weight to preferences
            user_manager_instance.update_user_preference('weight_kg', weight)
        
        # Calculate calories and CO2 saved
        calories = utils.calculate_calories(distance, speed, int(weight))
        co2_saved = utils.calculate_co2_saved(distance)
        
        # Display summary
        ascii_art.display_section_header("Trip Summary")
        print(f"Date: {date}")
        print(f"Distance: {utils.format_distance(distance)}")
        print(f"Duration: {duration:.1f} minutes")
        print(f"Average Speed: {speed:.1f} km/h")
        print(f"Calories Burned: {utils.format_calories(calories)}")
        print(f"CO2 Saved: {utils.format_co2(co2_saved)}")
        
        # Confirm and save
        confirm = input("\nSave this trip? (y/n): ")
        if confirm.lower() == 'y':
            # Update user stats
            if user_manager_instance.update_user_stats(distance, co2_saved, calories):
                ascii_art.display_success_message("Trip saved successfully!")
            else:
                ascii_art.display_error_message("Error saving trip data")
            
            # Log to Google Sheets if available
            if GOOGLE_SHEETS_AVAILABLE and modules['sheets_manager']:
                sheets_manager = modules['sheets_manager'].SheetsManager()
                trip_data = {
                    'date': date,
                    'distance': distance,
                    'duration': duration,
                    'calories': calories,
                    'co2_saved': co2_saved  # This matches the field name expected in sheets_manager.py
                }
                username = user_manager_instance.get_current_user().get('username', 'unknown')
                if sheets_manager.log_trip(username, trip_data):
                    ascii_art.display_success_message("Trip logged to Google Sheets!")
                else:
                    ascii_art.display_warning_message("Could not log trip to Google Sheets")
        else:
            print("Trip not saved.")
            
    except ValueError as e:
        # Provide more specific error message based on the exception
        error_msg = str(e)
        if "could not convert string to float" in error_msg:
            ascii_art.display_error_message("Invalid input. Please enter numeric values only.")
        else:
            # Use the specific error message from the validation checks
            ascii_art.display_error_message(f"Input validation error: {e}")
        
        # Log the specific error for debugging
        logger.debug(f"Input validation error in log_cycling_trip: {e}")
    except Exception as e:
        # Catch any unexpected errors
        error_msg = f"Unexpected error occurred: {e}"
        ascii_art.display_error_message(error_msg)
        logger.error(f"Unexpected error in log_cycling_trip: {e}", exc_info=True)
    
    input("\nPress Enter to return to the main menu...")


def view_statistics(user_manager_instance):
    """View user statistics."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    
    ascii_art.clear_screen()
    ascii_art.display_header()
    ascii_art.display_section_header("Statistics")
    
    # Check if user is authenticated
    if not user_manager_instance.is_authenticated():
        print("You need to log in to view statistics.")
        input("Press Enter to continue...")
        return
    
    # Get user stats
    user = user_manager_instance.get_current_user()
    stats = user.get('stats', {})
    
    if not stats or not stats.get('total_trips', 0):
        print("No cycling data recorded yet.")
        input("Press Enter to continue...")
        return
    
    # Display overall stats
    total_trips = stats.get('total_trips', 0)
    total_distance = stats.get('total_distance', 0.0)
    total_co2_saved = stats.get('total_co2_saved', 0.0)
    total_calories = stats.get('total_calories', 0)
    
    print(f"Total Trips: {total_trips}")
    print(f"Total Distance: {total_distance:.1f} km")
    print(f"Total CO2 Saved: {total_co2_saved:.2f} kg")
    print(f"Total Calories Burned: {total_calories}")
    
    # Calculate averages
    if total_trips > 0:
        avg_distance = total_distance / total_trips
        avg_co2_saved = total_co2_saved / total_trips
        avg_calories = total_calories / total_trips
        
        print(f"\nAverage Distance per Trip: {avg_distance:.1f} km")
        print(f"Average CO2 Saved per Trip: {avg_co2_saved:.2f} kg")
        print(f"Average Calories Burned per Trip: {avg_calories:.0f}")
    
    # Display recent trips if available
    trips = stats.get('trips', [])
    if trips:
        ascii_art.display_section_header("Recent Trips")
        
        # Extract recent trips (up to 5)
        recent_trips = trips[-5:] if len(trips) > 5 else trips
        
        # Prepare data for table
        headers = ["Date", "Distance (km)", "CO2 Saved (kg)", "Calories"]
        data = []
        
        for trip in reversed(recent_trips):  # Show most recent first
            date = trip.get('date', 'Unknown').split('T')[0]  # Extract date part
            distance = trip.get('distance', 0.0)
            co2_saved = trip.get('co2_saved', 0.0)
            calories = trip.get('calories', 0)
            
            data.append([date, f"{distance:.1f}", f"{co2_saved:.2f}", calories])
        
        # Display table
        ascii_art.display_data_table(headers, data)
    
    # Options for more detailed stats
    print("\nOptions:")
    print("1. Return to main menu")
    
    # Check if data visualization module is available
    try:
        import data_visualization
        print("2. View detailed charts and graphs")
        viz_available = True
    except ImportError:
        viz_available = False
    
    choice = input("\nSelect an option: ")
    
    if choice == "2" and viz_available:
        # Run the data visualization module
        data_visualization.run_visualization(user_manager_instance)
    else:
        # Return to main menu
        return


def eco_challenges(user_manager_instance):
    """Access the eco-challenges feature."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    
    ascii_art.clear_screen()
    ascii_art.display_header()
    ascii_art.display_section_header("Eco-Challenges")
    
    # Check if eco_challenges module is available
    try:
        if 'eco_challenges' in modules and modules['eco_challenges']:
            # Run the eco challenges module
            modules['eco_challenges'].run_eco_challenges(user_manager_instance, modules.get('sheets_manager'))
            return
    except Exception as e:
        logger.error(f"Error running eco challenges: {e}")
        pass  # Continue to basic implementation
    
    # Basic implementation if the module is not available
    print("Eco-challenges module not available.")
    print("\nEco-challenges help you track and achieve sustainability goals through:")
    print("- Weekly sustainability challenges")
    print("- Goal tracking and progress visualization")
    print("- Community challenges and leaderboards")
    print("- Personalized challenge suggestions")
    
    if user_manager_instance.is_authenticated():
        # Show basic challenge suggestions
        print("\nHere are some eco-challenges you can try:")
        print("1. Cycle to work/school every day this week")
        print("2. Replace one car trip with cycling every day")
        print("3. Track and reduce your carbon footprint by 10%")
        print("4. Cycle for leisure at least twice this week")
        print("5. Try a new cycling route to discover your area")
    else:
        print("\nYou need to log in to access personalized eco-challenges.")
                
    input("\nPress Enter to return to the main menu...")


def calculate_carbon_footprint(user_manager_instance):
    """Calculate user's carbon footprint and show alternatives."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    
    ascii_art.clear_screen()
    ascii_art.display_header()
    ascii_art.display_section_header("Carbon Footprint Calculator")
    
    # Check if enhanced carbon impact tracker is available
    try:
        if 'carbon_impact_tracker' in modules and modules['carbon_impact_tracker']:
            # Run the enhanced carbon impact tracker
            modules['carbon_impact_tracker'].run_carbon_tracker(user_manager_instance, modules.get('sheets_manager'))
            return
    except Exception as e:
        logger.error(f"Error running carbon impact tracker: {e}")
        pass  # Continue to try the basic module
    
    # Try to use the basic carbon footprint calculator
    try:
        import carbon_footprint
        
        # Run the carbon footprint module
        carbon_footprint.run_calculator(user_manager_instance)
    except ImportError:
        # Basic implementation if the module is not available
        print("Carbon footprint calculation module not available.")
        
        # Display user's cycling impact
        if user_manager_instance.is_authenticated():
            user = user_manager_instance.get_current_user()
            stats = user.get('stats', {})
            total_co2_saved = stats.get('total_co2_saved', 0.0)
            
            if total_co2_saved > 0:
                print(f"\nYour cycling has saved approximately {total_co2_saved:.2f} kg of CO2 emissions.")
                print("This is equivalent to:")
                
                # Calculate equivalents
                trees_month = total_co2_saved / 20  # One tree absorbs about 20kg CO2 per month
                car_km = total_co2_saved / 0.2  # Average car emits about 200g CO2 per km
                
                print(f"- The CO2 absorbed by {trees_month:.1f} trees in one month")
                print(f"- The emissions from driving {car_km:.1f} km in an average car")
            else:
                print("\nNo cycling data recorded yet. Start logging your trips to see your environmental impact!")
                
    input("\nPress Enter to return to the main menu...")


def weather_route_planner(user_manager_instance):
    """Check weather and plan cycling routes."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    
    ascii_art.clear_screen()
    ascii_art.display_header()
    ascii_art.display_section_header("Weather and Route Planner")
    
    # Show menu options for different route planning modes
    options = [
        "Check weather forecast for cycling",
        "Plan basic cycling routes",
        "AI-powered route recommendations"
    ]
    
    ascii_art.display_menu("Route Planning Options", options)
    
    choice = input("\nSelect an option (1-3) or press Enter for basic route planning: ")
    
    if choice == "1":
        # Weather forecast only
        try:
            import weather_route_planner
            weather_route_planner.check_weather(user_manager_instance)
        except (ImportError, AttributeError):
            print("Weather forecast module not available.")
            print("This feature requires the 'requests' package.")
            
            if not is_package_installed('requests'):
                install = input("Would you like to install the required package now? (y/n): ")
                if install.lower() == 'y':
                    install_packages(['requests'])
                    print("Please restart the application to use this feature.")
    
    elif choice == "3":
        # AI Route Planner
        try:
            if 'ai_route_planner' in modules and modules['ai_route_planner']:
                # Run the AI route planner
                modules['ai_route_planner'].run_ai_route_planner(user_manager_instance, modules.get('sheets_manager'))
            else:
                print("AI route planner module not available.")
                print("This feature requires the Google Generative AI package and API key.")
                
                if not is_package_installed('google-generativeai'):
                    install = input("Would you like to install the required package now? (y/n): ")
                    if install.lower() == 'y':
                        install_packages(['google-generativeai'])
                        print("Please restart the application to use this feature.")
                
                # Check if API key is available
                if os.environ.get('GEMINI_API_KEY') is None:
                    print("\nThe GEMINI_API_KEY environment variable is not set.")
                    print("You'll need to create a Google AI Studio account and obtain an API key.")
                    print("Then add it to your .env file as GEMINI_API_KEY=your_key_here")
        except Exception as e:
            logger.error(f"Error running AI route planner: {e}")
            print(f"Error running AI route planner: {e}")
    
    else:  # Default or "2": Basic route planner
        # Basic route planner
        try:
            import weather_route_planner
            
            # Run the weather and route planner module
            weather_route_planner.run_planner(user_manager_instance)
        except ImportError:
            # Basic implementation if the module is not available
            print("Weather and route planning module not available.")
            print("\nThis feature helps you check weather conditions and plan optimal cycling routes.")
            print("It requires additional dependencies like requests and folium.")
            
            # Check which dependencies are missing
            missing = []
            for pkg in ['requests', 'folium']:
                if not is_package_installed(pkg):
                    missing.append(pkg)
            
            if missing:
                print(f"\nMissing dependencies: {', '.join(missing)}")
                install = input("Would you like to install them now? (y/n): ")
                if install.lower() == 'y':
                    install_packages(missing)
                    print("Please restart the application to use this feature.")
        
    input("\nPress Enter to return to the main menu...")


def settings_preferences(user_manager_instance):
    """Manage user settings and preferences."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    
    # Check if user is authenticated
    if not user_manager_instance.is_authenticated():
        ascii_art.clear_screen()
        ascii_art.display_header()
        print("You need to log in to manage settings and preferences.")
        input("Press Enter to continue...")
        return
    
    while True:
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Settings and Preferences")
        
        # Get current preferences
        weight_kg = user_manager_instance.get_user_preference('weight_kg', 70)
        transport_mode = user_manager_instance.get_user_preference('default_transport_mode', 'bicycle')
        theme = user_manager_instance.get_user_preference('theme', 'default')
        notifications = user_manager_instance.get_user_preference('notifications_enabled', False)
        
        # Display current settings
        print("Current Settings:")
        print(f"1. Weight: {weight_kg} kg")
        print(f"2. Default Transport Mode: {transport_mode}")
        print(f"3. Theme: {theme}")
        print(f"4. Notifications: {'Enabled' if notifications else 'Disabled'}")
        print("5. Back to Main Menu")
        
        # Get user choice
        choice = input("\nSelect a setting to change (1-5): ")
        
        if choice == '1':
            # Change weight
            try:
                new_weight = float(input("Enter your weight in kg: "))
                user_manager_instance.update_user_preference('weight_kg', new_weight)
                ascii_art.display_success_message("Weight updated successfully!")
            except ValueError:
                ascii_art.display_error_message("Invalid input. Please enter a numeric value.")
        
        elif choice == '2':
            # Change default transport mode
            print("\nAvailable Transport Modes:")
            modes = ['bicycle', 'e-bike', 'scooter', 'skateboard']
            for i, mode in enumerate(modes, 1):
                print(f"{i}. {mode}")
            
            try:
                mode_choice = int(input("\nSelect a transport mode (1-4): "))
                if 1 <= mode_choice <= len(modes):
                    user_manager_instance.update_user_preference('default_transport_mode', modes[mode_choice-1])
                    ascii_art.display_success_message("Default transport mode updated successfully!")
                else:
                    ascii_art.display_error_message("Invalid selection.")
            except ValueError:
                ascii_art.display_error_message("Invalid input. Please enter a number.")
        
        elif choice == '3':
            # Change theme
            print("\nAvailable Themes:")
            themes = ['default', 'dark', 'eco', 'high-contrast']
            for i, theme in enumerate(themes, 1):
                print(f"{i}. {theme}")
            
            try:
                theme_choice = int(input("\nSelect a theme (1-4): "))
                if 1 <= theme_choice <= len(themes):
                    user_manager_instance.update_user_preference('theme', themes[theme_choice-1])
                    ascii_art.display_success_message("Theme updated successfully!")
                else:
                    ascii_art.display_error_message("Invalid selection.")
            except ValueError:
                ascii_art.display_error_message("Invalid input. Please enter a number.")
        
        elif choice == '4':
            # Toggle notifications
            new_setting = not notifications
            user_manager_instance.update_user_preference('notifications_enabled', new_setting)
            status = "enabled" if new_setting else "disabled"
            ascii_art.display_success_message(f"Notifications {status} successfully!")
        
        elif choice == '5':
            # Back to main menu
            break
        
        else:
            ascii_art.display_error_message("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


def social_sharing(user_manager_instance):
    """Manage social sharing and achievements with enhanced animations."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    
    ascii_art.clear_screen()
    ascii_art.display_header()
    ascii_art.display_section_header("Social Sharing and Achievements")
    
    # Check if social_gamification module is available
    try:
        import social_gamification
        
        # Run the social sharing and achievements module
        social_gamification.run_social_features(user_manager_instance)
    except ImportError:
        # Enhanced implementation if we have enhanced UI and user is authenticated
        if user_manager_instance.is_authenticated() and not user_manager_instance.is_guest():
            try:
                _display_enhanced_achievements(user_manager_instance, ascii_art)
                return
            except Exception as e:
                logger.warning(f"Error running enhanced achievements: {e}")
                # Fall back to basic implementation
        
        # Basic implementation if the module is not available or enhanced UI failed
        print("Social sharing and achievements module not available.")
        print("\nThis feature allows you to share your cycling achievements and connect with other cyclists.")
        print("It includes achievements, badges, challenges, and social sharing options.")
        
        if user_manager_instance.is_authenticated() and not user_manager_instance.is_guest():
            user = user_manager_instance.get_current_user()
            stats = user.get('stats', {})
            
            if stats and stats.get('total_trips', 0) > 0:
                # Show basic achievements based on stats
                total_trips = stats.get('total_trips', 0)
                total_distance = stats.get('total_distance', 0.0)
                
                print("\nYour Achievements:")
                
                if total_trips >= 1:
                    print("✓ First Ride - Completed your first cycling trip")
                
                if total_trips >= 5:
                    print("✓ Regular Rider - Logged 5 or more cycling trips")
                
                if total_trips >= 10:
                    print("✓ Dedicated Cyclist - Logged 10 or more cycling trips")
                
                if total_distance >= 50:
                    print("✓ Half Century - Cycled a total of 50 km or more")
                
                if total_distance >= 100:
                    print("✓ Century Rider - Cycled a total of 100 km or more")
        else:
            print("\nYou need to log in (with a registered account) to track achievements.")
    
    input("\nPress Enter to return to the main menu...")

def _display_enhanced_achievements(user_manager_instance, ascii_art):
    """Display enhanced achievements with animations."""
    user = user_manager_instance.get_current_user()
    stats = user.get('stats', {})
    
    # If we have no stats, show a message with the mascot
    if not stats or not stats.get('total_trips', 0):
        if hasattr(ascii_art, 'display_mascot_animation'):
            ascii_art.display_mascot_animation("Start cycling to earn achievements!")
        else:
            print("No achievements yet. Start cycling to earn achievements!")
        input("\nPress Enter to continue...")
        return
    
    # Calculate achievement levels based on stats
    total_trips = stats.get('total_trips', 0)
    total_distance = stats.get('total_distance', 0.0)
    total_co2_saved = stats.get('total_co2_saved', 0.0)
    total_calories = stats.get('total_calories', 0)
    
    # Display a fun loading animation
    if hasattr(ascii_art, 'display_loading_animation'):
        ascii_art.display_loading_animation("Loading your achievements", 1.5)
    
    # Determine achievements and show them with animation
    achievements = []
    
    # Trip count achievements
    if total_trips >= 10:
        achievements.append(("streak", 3, "Dedicated Cyclist"))
    elif total_trips >= 5:
        achievements.append(("streak", 2, "Regular Rider"))
    elif total_trips >= 1:
        achievements.append(("streak", 1, "First Ride"))
    
    # Distance achievements
    if total_distance >= 100:
        achievements.append(("distance", 3, "Century Rider"))
    elif total_distance >= 50:
        achievements.append(("distance", 2, "Half Century"))
    elif total_distance >= 10:
        achievements.append(("distance", 1, "Getting Started"))
    
    # CO2 savings achievements
    if total_co2_saved >= 20:
        achievements.append(("carbon_saver", 3, "Climate Hero"))
    elif total_co2_saved >= 10:
        achievements.append(("carbon_saver", 2, "Climate Guardian"))
    elif total_co2_saved >= 2:
        achievements.append(("carbon_saver", 1, "Climate Conscious"))
    
    # Display all achievements with animation
    if achievements:
        for achievement_type, level, name in achievements:
            if hasattr(ascii_art, 'display_achievement_badge'):
                ascii_art.display_achievement_badge(achievement_type, level, name)
                time.sleep(0.5)  # Pause between achievements
            else:
                print(f"✓ {name}")
    else:
        print("No achievements yet. Start cycling to earn achievements!")
    
    # Offer to generate a sharing graphic or view route animation
    print("\nShare options:")
    
    if hasattr(ascii_art, 'create_social_share_graphic'):
        print("1. Create shareable achievement graphic")
    else:
        print("1. Share achievements (not available in basic mode)")
        
    if hasattr(ascii_art, 'animate_route_on_map'):
        print("2. View animated cycling routes")
    else:
        print("2. View routes (not available in basic mode)")
        
    print("3. Return to main menu")
    
    choice = input("\nSelect an option: ")
    
    if choice == "1" and hasattr(ascii_art, 'create_social_share_graphic'):
        # Generate a shareable graphic
        username = user.get('username', 'EcoCyclist')
        # Find the highest achievement
        if achievements:
            top_achievement = max(achievements, key=lambda x: x[1])
            achievement_name = top_achievement[2]
        else:
            achievement_name = "EcoCycle User"
            
        # Display social share graphic
        ascii_art.create_social_share_graphic(
            username, 
            achievement_name, 
            {
                "Total Trips": total_trips,
                "Total Distance": f"{total_distance:.1f}",
                "CO2 Saved": f"{total_co2_saved:.1f}",
                "Calories Burned": total_calories
            }
        )
    elif choice == "2" and hasattr(ascii_art, 'animate_route_on_map'):
        # Show animated route visualization
        ascii_art.animate_route_on_map()
    elif choice in ["1", "2"]:
        print("\nThis feature is not available in basic mode.")


def notifications(user_manager_instance):
    """Manage user notifications."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    
    ascii_art.clear_screen()
    ascii_art.display_header()
    ascii_art.display_section_header("Notifications")
    
    # Check if notification_system module is available
    try:
        import notification_system
        
        # Run the notification system module
        notification_system.run_notification_manager(user_manager_instance)
    except ImportError:
        # Basic implementation if the module is not available
        print("Notification system module not available.")
        print("\nThis feature allows you to set up and manage notifications for:")
        print("- Cycling reminders")
        print("- Weather alerts for optimal cycling conditions")
        print("- Achievement and goal notifications")
        print("- Eco-tip of the day")
        
        # Check if user has enabled notifications
        if user_manager_instance.is_authenticated():
            notifications_enabled = user_manager_instance.get_user_preference('notifications_enabled', False)
            
            print(f"\nNotifications are currently {'enabled' if notifications_enabled else 'disabled'}.")
            
            toggle = input("Would you like to toggle notification settings? (y/n): ")
            if toggle.lower() == 'y':
                new_setting = not notifications_enabled
                user_manager_instance.update_user_preference('notifications_enabled', new_setting)
                status = "enabled" if new_setting else "disabled"
                ascii_art.display_success_message(f"Notifications {status} successfully!")
            
            # Mention external integrations
            print("\nExternal notification methods (email, SMS) require additional setup.")
            print("Install the notification_system module for full functionality.")
        else:
            print("\nYou need to log in to manage notification preferences.")
    
    input("\nPress Enter to return to the main menu...")


def admin_panel(user_manager_instance):
    """Admin panel for system management."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    
    ascii_art.clear_screen()
    ascii_art.display_header()
    ascii_art.display_section_header("Admin Panel")
    
    # Check if user is an admin
    if not user_manager_instance.is_admin():
        print("Access denied. Admin privileges required.")
        input("Press Enter to continue...")
        return
    
    # Check if admin_panel module is available
    try:
        import admin_panel
        
        # Run the admin panel module
        admin_panel.run_admin_panel(user_manager_instance)
    except ImportError:
        # Basic implementation if the module is not available
        print("Admin panel module not available.")
        print("\nThis panel provides system management capabilities for administrators.")
        print("Features include:")
        print("- User management")
        print("- System statistics")
        print("- Data management")
        print("- System configuration")
        
        # Provide basic user management
        print("\nRegistered Users:")
        users = user_manager_instance.users
        
        if users:
            # Prepare data for table
            headers = ["Username", "Name", "Admin", "Trips"]
            data = []
            
            for username, user_data in users.items():
                if username != 'guest':  # Skip guest user
                    name = user_data.get('name', 'Unknown')
                    is_admin = "Yes" if user_data.get('is_admin', False) else "No"
                    trips = user_data.get('stats', {}).get('total_trips', 0)
                    
                    data.append([username, name, is_admin, trips])
            
            # Display table
            ascii_art.display_data_table(headers, data)
        else:
            print("No registered users found.")
    
    input("\nPress Enter to return to the main menu...")


def handle_cli_arguments():
    """Parse command-line arguments and handle commands."""
    parser = argparse.ArgumentParser(description='EcoCycle - Cycle into a greener tomorrow')

    # Add subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='command')

    # 'run' command (default)
    run_parser = subparsers.add_parser('run', help='Run the main application')

    # 'stats' command
    stats_parser = subparsers.add_parser('stats', help='View statistics')
    stats_parser.add_argument('--user', help='Username to view stats for (admin only)')

    # 'weather' command
    weather_parser = subparsers.add_parser('weather', help='Check weather for cycling')
    weather_parser.add_argument('--location', help='Location to check weather for')

    # 'config' command
    config_parser = subparsers.add_parser('config', help='Configure application settings')
    config_parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'), help='Set a configuration value')
    config_parser.add_argument('--get', metavar='KEY', help='Get a configuration value')
    config_parser.add_argument('--list', action='store_true', help='List all configuration values')

    # 'export' command
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('--format', choices=['csv', 'json', 'pdf'], default='csv', help='Export format')
    export_parser.add_argument('--output', help='Output file path')

    # 'update' command
    update_parser = subparsers.add_parser('update', help='Update the application')
    update_parser.add_argument('--check', action='store_true', help='Check for updates')

    # 'help' command
    help_parser = subparsers.add_parser('help', help='Show help information')
    help_parser.add_argument('topic', nargs='?', help='Help topic')

    # 'doctor' command
    doctor_parser = subparsers.add_parser('doctor', help='Run system diagnostics')
    doctor_parser.add_argument('--fix', action='store_true', help='Attempt to fix issues')

    # Parse arguments
    args = parser.parse_args()

    # --- Initialize Managers and Check Session ---
    # Initialize modules and managers first, as they are needed by various commands and session checks
    modules = import_local_modules()
    user_manager_instance = modules['user_manager'].UserManager()

    # Create sheets manager if available
    sheets_manager_instance = None
    if GOOGLE_SHEETS_AVAILABLE:
        # Check if sheets_manager module was actually loaded
        if modules.get('sheets_manager'):
             try:
                 sheets_manager_instance = modules['sheets_manager'].SheetsManager()
                 # Attach sheets manager to user manager if available and initialized correctly
                 if sheets_manager_instance.is_available():
                     user_manager_instance.sheets_manager = sheets_manager_instance
             except Exception as sheet_init_error:
                  logger.error(f"Failed to initialize SheetsManager: {sheet_init_error}", exc_info=True)
                  # Ensure it's None if initialization failed
                  sheets_manager_instance = None
        else:
             logger.warning("Sheets manager module not imported or available.")


    # --- CRITICAL: Check for Session Secret Key ---
    # Do this *after* initializing UserManager
    if not user_manager_instance._get_session_secret():
         # Error logged in _get_session_secret. Provide user feedback.
         print("\n" + "="*50)
         print(" CRITICAL ERROR: Session Secret Key Not Found!")
         print(f" Please ensure the '{SESSION_SECRET_ENV_VAR}' variable is set")
         print(" in your .env file or environment variables.")
         print(" Session persistence is disabled or insecure.")
         print(" The application may not function correctly.")
         print("="*50 + "\n")
         # Decide whether to exit or continue with degraded functionality
         # return # Uncomment to exit if the key is mandatory

    # --- Check for Existing Valid Session ---
    logged_in_username = check_existing_session(user_manager_instance)
    # --- End Session Check ---


    # --- Handle Specific CLI Commands ---
    if args.command == 'stats':
        # Check if user is authenticated (via session) or needs to log in
        if not user_manager_instance.is_authenticated():
             print("Authentication required to view statistics.")
             if not user_manager_instance.authenticate():
                 print("Authentication failed. Cannot view statistics.")
                 return # Exit if auth fails

        # Proceed only if authenticated
        if user_manager_instance.is_authenticated():
            if args.user:
                # Check admin privileges to view other users' stats
                if user_manager_instance.is_admin():
                    print(f"Viewing stats for user: {args.user}")
                    # TODO: Implement logic to show stats for args.user
                    # You might need a method in UserManager like `get_user_stats(username)`
                    print("Viewing stats for specific user not yet fully implemented.")
                else:
                    print("Admin privileges required to view stats for other users.")
                    print("Showing stats for the current user instead.")
                    view_statistics(user_manager_instance) # Show current user's stats
            else:
                # Run interactive stats viewer for the current user
                view_statistics(user_manager_instance)

    elif args.command == 'weather':
        # Handle weather command (doesn't strictly require login, but might use preferences)
        try:
            # Import here to avoid circular dependency issues if weather module uses UserManager
            import weather_route_planner
            if args.location:
                # Pass None for user_manager if location is specified (no preferences needed)
                weather_route_planner.check_weather(None, location_override=args.location)
            else:
                # Pass the initialized user_manager_instance to use preferences
                weather_route_planner.run_planner(user_manager_instance)
        except ImportError:
            print("Weather and route planning module not available.")
        except Exception as e:
            logger.error(f"Error running weather command: {e}", exc_info=True)
            print(f"An error occurred while running the weather command: {e}")


    elif args.command == 'config':
        # Check if user is authenticated (via session) or needs to log in
        if not user_manager_instance.is_authenticated():
            print("Authentication required to manage configuration.")
            if not user_manager_instance.authenticate():
                 print("Authentication failed. Cannot manage configuration.")
                 return # Exit if auth fails

        # Proceed only if authenticated
        if user_manager_instance.is_authenticated():
            ascii_art = modules['ascii_art'] # Get ascii_art for messages
            if args.set:
                key, value = args.set
                if user_manager_instance.update_user_preference(key, value):
                    ascii_art.display_success_message(f"Configuration value '{key}' set to '{value}'")
                else:
                    ascii_art.display_error_message(f"Failed to set configuration value '{key}'.")
            elif args.get:
                value = user_manager_instance.get_user_preference(args.get)
                if value is not None:
                    print(f"{args.get}: {value}")
                else:
                    print(f"Configuration key '{args.get}' not found.")
            elif args.list:
                user = user_manager_instance.get_current_user() # Get full user data
                preferences = user.get('preferences', {})

                if preferences:
                    print("\nCurrent Configuration values:")
                    # Use display_data_table for better formatting
                    headers = ["Key", "Value"]
                    data = [[key, str(value)] for key, value in preferences.items()] # Convert value to string for table
                    ascii_art.display_data_table(headers, data)
                else:
                    print("No configuration values set.")
            else:
                 # Default action if no specific config flag is given (e.g., just 'ecocycle config')
                 print("Use --set, --get, or --list to manage configuration.")
                 config_parser.print_help()


    elif args.command == 'export':
        # Handle export command (implement actual export logic)
        print(f"Exporting data in {args.format} format")
        if args.output:
            print(f"Output file: {args.output}")
        else:
            print("Using default output file name.")
        print("Export feature not yet fully implemented.")
        # Example:
        # if user_manager_instance.is_authenticated():
        #     export_data(user_manager_instance, args.format, args.output)
        # else:
        #     print("Authentication required to export data.")

    elif args.command == 'update':
        # Handle update command (implement actual update logic)
        if args.check:
            print("Checking for updates...")
            print("Update check feature not yet implemented.")
        else:
            print("Updating application...")
            print("Update feature not yet implemented.")

    elif args.command == 'help':
        # Handle help command
        if args.topic:
            print(f"Help for topic: {args.topic}")
            # TODO: Implement topic-specific help
            print("Topic-specific help not yet implemented.")
        else:
            parser.print_help()

    elif args.command == 'doctor':
        # Handle doctor command
        perform_system_check(args.fix)

    # --- Default Action: Run Main Application UI ---
    else: # No specific command given, or 'run' command
        if logged_in_username:
            logger.info(f"User '{logged_in_username}' automatically logged in via session.")
            # Get user's display name safely
            user_data = user_manager_instance.users.get(logged_in_username, {})
            display_name = user_data.get('name', logged_in_username)
            print(f"\nWelcome back, {display_name}!")
            # Directly show the main menu
            show_main_menu(user_manager_instance)
        else:
            logger.info("No valid session found or CLI command specified. Proceeding to authentication.")
            # Attempt authentication first
            if user_manager_instance.authenticate():
                # If authentication is successful, show the main menu
                show_main_menu(user_manager_instance)
            else:
                # If authentication fails or is cancelled
                print("\nAuthentication failed or cancelled. Exiting application.")
                sys.exit(0) # Exit cleanly if auth fails/cancelled at start

# --- End of handle_cli_arguments function ---


def perform_system_check(fix_issues=False):
    """Perform basic system checks to ensure everything is working properly."""
    modules = import_local_modules()
    ascii_art = modules['ascii_art']
    
    ascii_art.clear_screen()
    ascii_art.display_header()
    ascii_art.display_section_header("System Check")
    
    issues = []
    
    # Check Python version
    import platform
    python_version = platform.python_version()
    required_version = (3, 6, 0)
    current_version = tuple(map(int, python_version.split('.')))
    
    if current_version >= required_version:
        ascii_art.display_success_message(f"Python version: {python_version} (compatible)")
    else:
        msg = f"Python version: {python_version} (incompatible, requires 3.6.0+)"
        issues.append(("python_version", msg))
        ascii_art.display_error_message(msg)
    
    # Check required packages
    for package in REQUIRED_PACKAGES:
        if is_package_installed(package):
            ascii_art.display_success_message(f"Package {package} is installed")
        else:
            msg = f"Package {package} is not installed"
            issues.append(("missing_package", package))
            ascii_art.display_error_message(msg)
    
    # Check optional packages
    for package in OPTIONAL_PACKAGES:
        if is_package_installed(package):
            ascii_art.display_success_message(f"Optional package {package} is installed")
        else:
            msg = f"Optional package {package} is not installed"
            ascii_art.display_warning_message(msg)
    
    # Check for .env file
    if os.path.exists('.env'):
        ascii_art.display_success_message(".env file exists")
    else:
        msg = ".env file not found (optional)"
        ascii_art.display_warning_message(msg)
        
        # Create .env file if fixing issues
        if fix_issues:
            try:
                with open('.env', 'w') as f:
                    f.write("# EcoCycle environment variables\n")
                    f.write("# Add your configuration below\n\n")
                ascii_art.display_success_message(".env file created")
            except Exception as e:
                ascii_art.display_error_message(f"Error creating .env file: {e}")
    
    # Check for essential files
    essential_files = ['main.py', 'utils.py', 'user_manager.py', 'eco_tips.py', 'ascii_art.py']
    for file in essential_files:
        if os.path.exists(file):
            ascii_art.display_success_message(f"Essential file {file} exists")
        else:
            msg = f"Essential file {file} not found"
            issues.append(("missing_file", file))
            ascii_art.display_error_message(msg)
    
    # Fix issues if requested
    if fix_issues and issues:
        ascii_art.display_section_header("Fixing Issues")
        
        for issue_type, issue_data in issues:
            if issue_type == "missing_package":
                ascii_art.display_info_message(f"Installing package: {issue_data}")
                install_packages([issue_data])
            elif issue_type == "missing_file":
                ascii_art.display_error_message(f"Cannot automatically create missing file: {issue_data}")
                
        # Re-run the check to see if issues were fixed
        ascii_art.display_info_message("Re-checking system after fixes...")
        if issues:
            # Wait a moment to show the message
            import time
            time.sleep(1)
            
            # Recursive call without fix_issues to prevent infinite loop
            perform_system_check(False)
    
    # Final summary
    if not issues:
        ascii_art.display_success_message("\nAll system checks passed! EcoCycle is ready to use.")
    else:
        if fix_issues:
            remaining_issues = sum(1 for issue_type, _ in issues 
                                if issue_type in ["missing_package", "missing_file"])
            if remaining_issues:
                ascii_art.display_warning_message(f"\n{remaining_issues} issues remain. Some manual intervention may be required.")
            else:
                ascii_art.display_success_message("\nAll issues fixed! EcoCycle is ready to use.")
        else:
            ascii_art.display_warning_message(f"\n{len(issues)} issues found. Run with --fix to attempt automatic fixes.")
    
    input("Press Enter to continue...")


def main():
    """Main application entry point for the EcoCycle CLI application."""
    # Check Python version
    if sys.version_info < (3, 6):
        print("Python 3.6 or higher is required to run EcoCycle.")
        sys.exit(1)
    
    # Install required packages if needed
    if not install_packages(REQUIRED_PACKAGES, True):
        print("Failed to install required packages. Please install them manually.")
        sys.exit(1)
    
    # Optional packages can be installed later as needed
    install_packages(OPTIONAL_PACKAGES, False)
    
    # Set up environment.
    setup_environment()
    
    # Start the application
    handle_cli_arguments()


if __name__ == "__main__":
    main()