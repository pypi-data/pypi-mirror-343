"""
EcoCycle - Command Line Interface Module
Provides a command-line interface for interacting with EcoCycle features.
"""
import os
import sys
import logging
import argparse
import json
import datetime
from typing import Dict, List, Optional, Any, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/ecocycle_cli.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Constants
CONFIG_FILE = ".ecocycle.config"
VERSION = "3.0.0"


def display_version():
    """Display the application version."""
    print(f"EcoCycle version {VERSION}")
    print("Cycle into a greener tomorrow")
    print("Copyright 2025")


def load_config() -> Dict:
    """Load configuration from file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error(f"Error parsing config file: {CONFIG_FILE}")
            return {}
    return {}


def save_config(config: Dict) -> bool:
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False


def verify_dependencies(required_only: bool = False) -> List[str]:
    """
    Verify that all dependencies are installed.
    Returns a list of missing dependencies.
    """
    import importlib.util
    
    # Define required and optional dependencies
    required = ['colorama']
    optional = ['requests', 'folium', 'matplotlib', 'numpy', 'plotly', 
                'tabulate', 'pillow', 'qrcode', 'fpdf', 'tqdm', 
                'python-dotenv', 'google-api-python-client', 'sendgrid', 'twilio']
    
    # Check which packages to verify
    to_check = required if required_only else required + optional
    
    # Check each package
    missing = []
    for package in to_check:
        # Handle hyphenated package names
        import_name = package.replace('-', '_')
        
        # Special case for google-api-python-client
        if package == 'google-api-python-client':
            import_name = 'googleapiclient'
        
        if importlib.util.find_spec(import_name) is None:
            missing.append(package)
    
    return missing


def run_doctor():
    """
    Run system diagnostics and fix common issues.
    """
    print("EcoCycle Doctor - System Diagnostics")
    print("====================================")
    
    # Check Python version
    print(f"\nPython Version: {sys.version}")
    python_version = tuple(map(int, sys.version.split()[0].split('.')))
    if python_version < (3, 7):
        print("WARNING: Python 3.7 or newer is recommended")
    
    # Check dependencies
    print("\nChecking dependencies...")
    missing_required = verify_dependencies(required_only=True)
    missing_optional = [pkg for pkg in verify_dependencies() if pkg not in missing_required]
    
    if missing_required:
        print(f"CRITICAL: Missing required dependencies: {', '.join(missing_required)}")
        print("These packages are required for basic functionality.")
        install = input("Would you like to install them now? (y/n): ")
        if install.lower() == 'y':
            import subprocess
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_required)
                print("Required dependencies installed successfully.")
            except subprocess.CalledProcessError:
                print("Error installing required dependencies. Please install manually.")
    else:
        print("All required dependencies are installed.")
    
    if missing_optional:
        print(f"\nMissing optional dependencies: {', '.join(missing_optional)}")
        print("These packages enable additional features but are not required.")
        install = input("Would you like to install them now? (y/n): ")
        if install.lower() == 'y':
            import subprocess
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_optional)
                print("Optional dependencies installed successfully.")
            except subprocess.CalledProcessError:
                print("Error installing optional dependencies. Please install manually.")
    else:
        print("All optional dependencies are installed.")
    
    # Check configuration
    print("\nChecking configuration...")
    config = load_config()
    if not config:
        print("No configuration found. A new one will be created when needed.")
    else:
        print("Configuration file found.")
        
        # Check for common configuration issues
        if 'user_preferences' not in config:
            print("WARNING: user_preferences section is missing from configuration")
        
        if 'last_sync' in config and isinstance(config['last_sync'], (int, float)):
            last_sync = datetime.datetime.fromtimestamp(config['last_sync'])
            print(f"Last data synchronization: {last_sync}")
    
    # Check data files
    print("\nChecking data files...")
    data_files = ['users.json', 'notification_settings.json', 'notification_logs.json']
    for file in data_files:
        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    json.load(f)
                print(f"✓ {file} exists and is valid JSON")
            except json.JSONDecodeError:
                print(f"✗ {file} exists but contains invalid JSON")
        else:
            print(f"✗ {file} does not exist (will be created when needed)")
    
    # Check log files
    print("\nChecking log files...")
    log_files = ['ecocycle.log', 'ecocycle_debug.log', 'ecocycle_web.log', 'ecocycle_cli.log']
    for file in log_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} exists ({size} bytes)")
            if size > 10 * 1024 * 1024:  # 10 MB
                print(f"  WARNING: Log file {file} is very large ({size // (1024*1024)} MB)")
                rotate = input(f"  Would you like to rotate {file}? (y/n): ")
                if rotate.lower() == 'y':
                    backup = f"{file}.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    try:
                        os.rename(file, backup)
                        print(f"  Log file rotated to {backup}")
                    except Exception as e:
                        print(f"  Error rotating log file: {e}")
        else:
            print(f"✗ {file} does not exist (will be created when needed)")
    
    # Check for updates
    print("\nChecking for updates...")
    try:
        # Use packaging version comparison if available
        import packaging.version
        
        # In a real application, this would make an API call to check for updates
        # This is just a placeholder
        current_version = packaging.version.parse(VERSION)
        latest_version = packaging.version.parse(VERSION)  # Would get from API
        
        if latest_version > current_version:
            print(f"A new version is available: {latest_version} (current: {current_version})")
            print("Run 'python -m ecocycle update' to update.")
        else:
            print(f"You have the latest version ({VERSION}).")
    except ImportError:
        print("Could not check for updates (packaging module not installed).")
    
    print("\nDiagnostics completed.")


def run_update():
    """
    Update the application to the latest version.
    """
    print("EcoCycle Update")
    print("==============")
    
    print("Checking for updates...")
    
    # In a real application, this would check for updates and update if needed
    # This is just a placeholder
    print(f"Current version: {VERSION}")
    print(f"Latest version: {VERSION}")
    print("You have the latest version.")
    print("\nNo update required.")


def handle_log_command(args):
    """
    Handle the 'log' command to log a cycling trip.
    """
    # Import necessary modules
    try:
        import main
        user_manager = main.import_local_modules()['user_manager'].UserManager()
        
        # Check if user is authenticated
        if not user_manager.is_authenticated():
            print("You need to be logged in to log a cycling trip.")
            print("Please run 'python main.py' and log in first.")
            return
        
        # Get trip details from command arguments or prompt for them
        date = args.date
        if not date:
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d")
        
        distance = args.distance
        if distance is None:
            distance = float(input("Distance (km): "))
        
        duration = args.duration
        if duration is None:
            duration = float(input("Duration (minutes): "))
        
        # Get user weight from preferences or prompt for it
        weight = user_manager.get_user_preference('weight_kg', None)
        if weight is None:
            weight = float(input("Your weight (kg) for calorie calculation: "))
            user_manager.update_user_preference('weight_kg', weight)
        
        # Calculate stats
        import utils
        speed = utils.calculate_average_speed(distance, duration)
        calories = utils.calculate_calories(distance, speed, int(weight))
        co2_saved = utils.calculate_co2_saved(distance)
        
        # Display trip summary
        print("\nTrip Summary:")
        print(f"Date: {date}")
        print(f"Distance: {utils.format_distance(distance)}")
        print(f"Duration: {duration:.1f} minutes")
        print(f"Average Speed: {speed:.1f} km/h")
        print(f"Calories Burned: {utils.format_calories(calories)}")
        print(f"CO2 Saved: {utils.format_co2(co2_saved)}")
        
        # Confirm and save
        if not args.yes:
            confirm = input("\nSave this trip? (y/n): ")
            save = confirm.lower() == 'y'
        else:
            save = True
            print("\nAutomatically saving trip...")
        
        if save:
            # Update user stats
            if user_manager.update_user_stats(distance, co2_saved, calories):
                print("Trip saved successfully!")
            else:
                print("Error saving trip data.")
        else:
            print("Trip not saved.")
    
    except ImportError as e:
        print(f"Error: Required modules not available - {e}")
        print("Please run 'python -m ecocycle doctor' to diagnose.")
    except Exception as e:
        print(f"Error logging trip: {e}")


def handle_stats_command(args):
    """
    Handle the 'stats' command to view cycling statistics.
    """
    # Import necessary modules
    try:
        import main
        modules = main.import_local_modules()
        user_manager = modules['user_manager'].UserManager()
        
        # Check if user is authenticated
        if not user_manager.is_authenticated():
            print("You need to be logged in to view statistics.")
            print("Please run 'python main.py' and log in first.")
            return
        
        # Get user stats
        user = user_manager.get_current_user()
        stats = user.get('stats', {})
        
        if not stats or not stats.get('total_trips', 0):
            print("No cycling data recorded yet.")
            return
        
        # Display overall stats
        print("Cycling Statistics")
        print("=================")
        
        name = user.get('name', user.get('username', 'Unknown'))
        print(f"Statistics for: {name}")
        
        total_trips = stats.get('total_trips', 0)
        total_distance = stats.get('total_distance', 0.0)
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        total_calories = stats.get('total_calories', 0)
        
        print(f"\nTotal Trips: {total_trips}")
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
        
        # Display recent trips if available and not in summary mode
        if not args.summary:
            trips = stats.get('trips', [])
            if trips:
                print("\nRecent Trips:")
                print("-------------")
                
                # Get recent trips (up to 10)
                recent_trips = trips[-10:] if len(trips) > 10 else trips
                
                # Check if tabulate is available for nicer output
                try:
                    from tabulate import tabulate
                    headers = ["Date", "Distance (km)", "Duration (min)", "CO2 Saved (kg)", "Calories"]
                    data = []
                    
                    for trip in reversed(recent_trips):  # Show most recent first
                        date = trip.get('date', 'Unknown').split('T')[0]  # Extract date part
                        distance = trip.get('distance', 0.0)
                        duration = trip.get('duration', 0.0)
                        co2_saved = trip.get('co2_saved', 0.0)
                        calories = trip.get('calories', 0)
                        
                        data.append([date, f"{distance:.1f}", f"{duration:.1f}", f"{co2_saved:.2f}", calories])
                    
                    print(tabulate(data, headers=headers, tablefmt="grid"))
                except ImportError:
                    # Fallback to simple output if tabulate is not available
                    for trip in reversed(recent_trips):  # Show most recent first
                        date = trip.get('date', 'Unknown').split('T')[0]  # Extract date part
                        distance = trip.get('distance', 0.0)
                        co2_saved = trip.get('co2_saved', 0.0)
                        calories = trip.get('calories', 0)
                        
                        print(f"{date}: {distance:.1f} km, {co2_saved:.2f} kg CO2, {calories} calories")
        
        # If visualization flag is set, try to open data visualization module
        if args.visualize:
            try:
                import data_visualization
                print("\nStarting data visualization...")
                data_visualization.run_visualization(user_manager)
            except ImportError:
                print("\nData visualization module not available.")
                print("Please install required dependencies with 'python -m ecocycle doctor'.")
    
    except ImportError as e:
        print(f"Error: Required modules not available - {e}")
        print("Please run 'python -m ecocycle doctor' to diagnose.")
    except Exception as e:
        print(f"Error viewing statistics: {e}")


def handle_weather_command(args):
    """
    Handle the 'weather' command to check weather for cycling.
    """
    # Import necessary modules
    try:
        import main
        import weather_route_planner
        
        # Initialize modules
        user_manager = main.import_local_modules()['user_manager'].UserManager()
        weather_planner = weather_route_planner.WeatherRoutePlanner(user_manager)
        
        location = args.location
        if not location:
            print("Checking weather for cycling...")
            weather_planner.check_weather()
        else:
            print(f"Checking weather for cycling in {location}...")
            weather_planner.check_weather(location)
    
    except ImportError as e:
        print(f"Error: Required modules not available - {e}")
        print("Please run 'python -m ecocycle doctor' to diagnose.")
    except Exception as e:
        print(f"Error checking weather: {e}")


def handle_routes_command(args):
    """
    Handle the 'routes' command to manage cycling routes.
    """
    # Import necessary modules
    try:
        import main
        import weather_route_planner
        
        # Initialize modules
        user_manager = main.import_local_modules()['user_manager'].UserManager()
        weather_planner = weather_route_planner.WeatherRoutePlanner(user_manager)
        
        if args.action == "plan":
            print("Planning a cycling route...")
            weather_planner.plan_route()
        elif args.action == "list":
            print("Listing saved routes...")
            weather_planner.view_saved_routes()
        elif args.action == "impact":
            print("Calculating cycling impact...")
            weather_planner.cycling_impact_calculator()
        else:
            print("Invalid action. Use 'plan', 'list', or 'impact'.")
    
    except ImportError as e:
        print(f"Error: Required modules not available - {e}")
        print("Please run 'python -m ecocycle doctor' to diagnose.")
    except Exception as e:
        print(f"Error managing routes: {e}")


def handle_config_command(args):
    """
    Handle the 'config' command to configure application settings.
    """
    config = load_config()
    
    if args.list:
        print("Current Configuration:")
        print("=====================")
        if config:
            # Prettify the output
            print(json.dumps(config, indent=2))
        else:
            print("Configuration is empty.")
        
        return
    
    if args.get:
        key = args.get
        if key in config:
            print(f"{key}: {json.dumps(config[key], indent=2)}")
        else:
            print(f"Key '{key}' not found in configuration.")
        
        return
    
    if args.set:
        key, value = args.set
        
        # Try to parse value as JSON for numbers, booleans, etc.
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            # If not valid JSON, treat as string
            pass
        
        # Update config
        config[key] = value
        if save_config(config):
            print(f"Configuration updated: {key} = {value}")
        else:
            print("Error saving configuration.")
        
        return
    
    # If no specific action, show help
    print("Use --list to show all configuration values.")
    print("Use --get KEY to show a specific configuration value.")
    print("Use --set KEY VALUE to set a configuration value.")


def handle_export_command(args):
    """
    Handle the 'export' command to export cycling data.
    """
    # Import necessary modules
    try:
        import main
        modules = main.import_local_modules()
        user_manager = modules['user_manager'].UserManager()
        
        # Check if user is authenticated
        if not user_manager.is_authenticated():
            print("You need to be logged in to export data.")
            print("Please run 'python main.py' and log in first.")
            return
        
        # Get user data
        user = user_manager.get_current_user()
        stats = user.get('stats', {})
        
        if not stats or not stats.get('total_trips', 0):
            print("No cycling data to export.")
            return
        
        # Determine output file path
        output_path = args.output
        if not output_path:
            date_str = datetime.datetime.now().strftime("%Y%m%d")
            username = user.get('username', 'unknown')
            output_path = f"ecocycle_export_{username}_{date_str}.{args.format}"
        
        # Export data
        if args.format == 'csv':
            export_to_csv(user, output_path)
        elif args.format == 'json':
            export_to_json(user, output_path)
        elif args.format == 'pdf':
            export_to_pdf(user, output_path)
        else:
            print(f"Unsupported format: {args.format}")
    
    except ImportError as e:
        print(f"Error: Required modules not available - {e}")
        print("Please run 'python -m ecocycle doctor' to diagnose.")
    except Exception as e:
        print(f"Error exporting data: {e}")


def export_to_csv(user, output_path):
    """Export user data to CSV file."""
    import csv
    
    stats = user.get('stats', {})
    trips = stats.get('trips', [])
    
    try:
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Date', 'Distance (km)', 'Duration (min)', 'CO2 Saved (kg)', 'Calories'])
            
            # Write trip data
            for trip in trips:
                date = trip.get('date', '')
                distance = trip.get('distance', 0.0)
                duration = trip.get('duration', 0.0)
                co2_saved = trip.get('co2_saved', 0.0)
                calories = trip.get('calories', 0)
                
                writer.writerow([date, distance, duration, co2_saved, calories])
        
        print(f"Data exported to CSV: {output_path}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")


def export_to_json(user, output_path):
    """Export user data to JSON file."""
    try:
        # Create a clean export structure
        export_data = {
            'user': {
                'username': user.get('username', ''),
                'name': user.get('name', ''),
                'email': user.get('email', ''),
                'export_date': datetime.datetime.now().isoformat()
            },
            'stats': user.get('stats', {})
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Data exported to JSON: {output_path}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")


def export_to_pdf(user, output_path):
    """Export user data to PDF file."""
    try:
        from fpdf import FPDF
        import utils
        
        username = user.get('username', 'unknown')
        name = user.get('name', username)
        stats = user.get('stats', {})
        trips = stats.get('trips', [])
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Add header
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "EcoCycle Data Export", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"User: {name}", ln=True, align="C")
        pdf.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
        
        # Add summary
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Cycling Summary", ln=True)
        
        pdf.set_font("Arial", "", 12)
        total_trips = stats.get('total_trips', 0)
        total_distance = stats.get('total_distance', 0.0)
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        total_calories = stats.get('total_calories', 0)
        
        pdf.cell(0, 8, f"Total Trips: {total_trips}", ln=True)
        pdf.cell(0, 8, f"Total Distance: {utils.format_distance(total_distance)}", ln=True)
        pdf.cell(0, 8, f"Total CO2 Saved: {utils.format_co2(total_co2_saved)}", ln=True)
        pdf.cell(0, 8, f"Total Calories Burned: {utils.format_calories(total_calories)}", ln=True)
        
        # Add trip table
        if trips:
            pdf.ln(10)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Trip History", ln=True)
            
            # Table headers
            pdf.set_font("Arial", "B", 10)
            pdf.cell(40, 10, "Date", border=1)
            pdf.cell(30, 10, "Distance (km)", border=1)
            pdf.cell(30, 10, "Duration (min)", border=1)
            pdf.cell(40, 10, "CO2 Saved (kg)", border=1)
            pdf.cell(40, 10, "Calories", border=1, ln=True)
            
            # Table rows
            pdf.set_font("Arial", "", 10)
            for trip in trips:
                date = trip.get('date', '').split('T')[0]  # Extract date part
                distance = trip.get('distance', 0.0)
                duration = trip.get('duration', 0.0)
                co2_saved = trip.get('co2_saved', 0.0)
                calories = trip.get('calories', 0)
                
                pdf.cell(40, 8, date, border=1)
                pdf.cell(30, 8, f"{distance:.1f}", border=1)
                pdf.cell(30, 8, f"{duration:.1f}", border=1)
                pdf.cell(40, 8, f"{co2_saved:.2f}", border=1)
                pdf.cell(40, 8, f"{calories}", border=1, ln=True)
        
        # Output the PDF
        pdf.output(output_path)
        print(f"Data exported to PDF: {output_path}")
    
    except ImportError:
        print("Error: fpdf library not available.")
        print("Please install it with 'pip install fpdf'.")
    except Exception as e:
        print(f"Error exporting to PDF: {e}")


def handle_social_command(args):
    """
    Handle the 'social' command to manage social features.
    """
    # Import necessary modules
    try:
        import main
        import social_gamification
        
        # Initialize modules
        user_manager = main.import_local_modules()['user_manager'].UserManager()
        
        # Check if user is authenticated
        if not user_manager.is_authenticated() or user_manager.is_guest():
            print("You need to be logged in (with a registered account) to use social features.")
            print("Please run 'python main.py' and log in first.")
            return
        
        # Run the social gamification module
        social_gamification.run_social_features(user_manager)
    
    except ImportError as e:
        print(f"Error: Required modules not available - {e}")
        print("Please run 'python -m ecocycle doctor' to diagnose.")
    except Exception as e:
        print(f"Error with social features: {e}")


def handle_notifications_command(args):
    """
    Handle the 'notifications' command to manage notifications.
    """
    # Import necessary modules
    try:
        import main
        import notification_system
        
        # Initialize modules
        user_manager = main.import_local_modules()['user_manager'].UserManager()
        
        # Check if user is authenticated
        if not user_manager.is_authenticated():
            print("You need to be logged in to manage notifications.")
            print("Please run 'python main.py' and log in first.")
            return
        
        # Run the notification system module
        notification_system.run_notification_manager(user_manager)
    
    except ImportError as e:
        print(f"Error: Required modules not available - {e}")
        print("Please run 'python -m ecocycle doctor' to diagnose. ")
    except Exception as e:
        print(f"Error with notifications: {e}")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='EcoCycle - Cycle into a greener tomorrow')
    subparsers = parser.add_subparsers(dest='command', help='command')
    
    # Run command (default)
    run_parser = subparsers.add_parser('run', help='Run the main application')
    
    # Log command
    log_parser = subparsers.add_parser('log', help='Log a cycling trip')
    log_parser.add_argument('--date', help='Trip date (YYYY-MM-DD, defaults to today)')
    log_parser.add_argument('--distance', type=float, help='Trip distance in kilometers')
    log_parser.add_argument('--duration', type=float, help='Trip duration in minutes')
    log_parser.add_argument('-y', '--yes', action='store_true', help='Automatically save without confirmation')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='View cycling statistics')
    stats_parser.add_argument('--summary', action='store_true', help='Show only summary statistics')
    stats_parser.add_argument('--visualize', '-v', action='store_true', help='Open data visualization')
    
    # Weather command
    weather_parser = subparsers.add_parser('weather', help='Check weather for cycling')
    weather_parser.add_argument('--location', help='Location to check weather for')
    
    # Routes command
    routes_parser = subparsers.add_parser('routes', help='Manage cycling routes')
    routes_parser.add_argument('action', choices=['plan', 'list', 'impact'], help='Action to perform')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configure application settings')
    config_parser.add_argument('--list', action='store_true', help='List all configuration values')
    config_parser.add_argument('--get', metavar='KEY', help='Get a configuration value')
    config_parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'), help='Set a configuration value')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export cycling data')
    export_parser.add_argument('--format', choices=['csv', 'json', 'pdf'], default='csv', help='Export format')
    export_parser.add_argument('--output', help='Output file path')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update the application')
    
    # Doctor command
    doctor_parser = subparsers.add_parser('doctor', help='Run system diagnostics')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Display version information')
    
    # Social command
    social_parser = subparsers.add_parser('social', help='Manage social features')
    
    # Notifications command
    notifications_parser = subparsers.add_parser('notifications', help='Manage notifications')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'run' or args.command is None:
        # Run the main program
        import main
        main.main()
    elif args.command == 'log':
        handle_log_command(args)
    elif args.command == 'stats':
        handle_stats_command(args)
    elif args.command == 'weather':
        handle_weather_command(args)
    elif args.command == 'routes':
        handle_routes_command(args)
    elif args.command == 'config':
        handle_config_command(args)
    elif args.command == 'export':
        handle_export_command(args)
    elif args.command == 'update':
        run_update()
    elif args.command == 'doctor':
        run_doctor()
    elif args.command == 'version':
        display_version()
    elif args.command == 'social':
        handle_social_command(args)
    elif args.command == 'notifications':
        handle_notifications_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()