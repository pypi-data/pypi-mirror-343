"""
EcoCycle - Data Visualization Module
Provides data visualization capabilities for cycling data and statistics.
"""
import os
import json
import logging
import time
import re
import datetime
from typing import Dict, List, Optional, Any, Tuple, Union
import webbrowser

# Try to import optional visualization libraries
try:
    import matplotlib
    # Use non-interactive backend (for headless environments)
    matplotlib.use('Agg')
    
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import numpy as np
    
    import plotly.graph_objects as go
    
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False

try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

# Import utilities
import utils
import ascii_art
import eco_tips

logger = logging.getLogger(__name__)

# Constants
VISUALIZATION_DIR = "visualizations"
REPORT_DIR = "reports"


class DataVisualization:
    """Data visualization features for EcoCycle."""
    
    def __init__(self, user_manager=None, sheets_manager=None):
        """Initialize the data visualization module."""
        self.user_manager = user_manager
        self.sheets_manager = sheets_manager
        
        # Create directories if they don't exist
        os.makedirs(VISUALIZATION_DIR, exist_ok=True)
        os.makedirs(REPORT_DIR, exist_ok=True)
    
    def run_visualization(self):
        """Run the data visualization interactive interface."""
        while True:
            ascii_art.clear_screen()
            ascii_art.display_header()
            ascii_art.display_section_header("Data Visualization")
            
            # Check if visualization libraries are available
            if not VISUALIZATION_AVAILABLE:
                print(f"{ascii_art.Fore.YELLOW}Visualization libraries (matplotlib, numpy, plotly) are required for this feature.{ascii_art.Style.RESET_ALL}")
                print("Please install them with: pip install matplotlib numpy plotly")
                print("\nOptions:")
                print("1. Return to Main Menu")
                
                choice = input("\nSelect an option: ")
                if choice == "1":
                    break
                continue
            
            # Check if user is authenticated
            if not self.user_manager or not self.user_manager.is_authenticated():
                print(f"{ascii_art.Fore.YELLOW}You need to be logged in to access data visualization features.{ascii_art.Style.RESET_ALL}")
                print("\nOptions:")
                print("1. Return to Main Menu")
                
                choice = input("\nSelect an option: ")
                if choice == "1":
                    break
                continue
            
            # Display menu options
            print(f"{ascii_art.Fore.CYAN}Data Visualization Options:{ascii_art.Style.RESET_ALL}")
            print("1. Activity Summary Dashboard")
            print("2. Trip History Analysis")
            print("3. Carbon Savings Visualization")
            print("4. Progress Over Time")
            print("5. Generate PDF Report")
            print("6. Export Data")
            print("7. Return to Main Menu")
            
            choice = input("\nSelect an option (1-7): ")
            
            if choice == "1":
                self.show_activity_summary()
            elif choice == "2":
                self.analyze_trip_history()
            elif choice == "3":
                self.visualize_carbon_savings()
            elif choice == "4":
                self.show_progress_over_time()
            elif choice == "5":
                self.generate_pdf_report()
            elif choice == "6":
                self.export_data()
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
    
    def show_activity_summary(self):
        """Show activity summary dashboard with key metrics and charts."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Activity Summary Dashboard")
        
        # Get user data
        user = self.user_manager.get_current_user()
        username = user.get('username')
        name = user.get('name', username)
        
        # Get user stats
        stats = user.get('stats', {})
        total_trips = stats.get('total_trips', 0)
        total_distance = stats.get('total_distance', 0.0)
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        total_calories = stats.get('total_calories', 0)
        trips = stats.get('trips', [])
        
        # Show key metrics
        print(f"{ascii_art.Fore.GREEN}Cycling Summary for {name}{ascii_art.Style.RESET_ALL}")
        print(f"Total Trips: {total_trips}")
        print(f"Total Distance: {utils.format_distance(total_distance)}")
        print(f"Total CO2 Saved: {utils.format_co2(total_co2_saved)}")
        print(f"Total Calories Burned: {utils.format_calories(total_calories)}")
        
        # Check if user has any trips
        if not trips:
            print("\nNo trip data available. Start logging your cycling trips to see visualizations!")
            input("\nPress Enter to continue...")
            return
        
        # Process trip data for visualization
        dates = []
        distances = []
        co2_saved = []
        calories = []
        
        print("\nProcessing trip data...")
        
        if TQDM_AVAILABLE:
            trip_iter = tqdm(trips)
        else:
            trip_iter = trips
            print(f"Processing {len(trips)} trips...")
        
        for trip in trip_iter:
            # Parse date
            date_str = trip.get('date')
            if not date_str:
                continue
            
            try:
                date = datetime.datetime.fromisoformat(date_str).date()
                dates.append(date)
                
                # Get trip data
                distance = trip.get('distance', 0.0)
                co2 = trip.get('co2_saved', 0.0)
                calorie = trip.get('calories', 0)
                
                distances.append(distance)
                co2_saved.append(co2)
                calories.append(calorie)
            except (ValueError, TypeError):
                # Skip trips with invalid date format
                continue
        
        # Exit if no valid trips were found
        if not dates:
            print("\nNo valid trip data available.")
            input("\nPress Enter to continue...")
            return
        
        # Create file names for plots
        summary_plot = os.path.join(VISUALIZATION_DIR, f"activity_summary_{username}_{int(time.time())}.png")
        
        print("\nGenerating activity summary visualization...")
        
        try:
            # Create a figure with 4 subplots
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f"Activity Summary for {name}", fontsize=16)
            
            # 1. Trips per day of week
            day_counts = np.zeros(7)  # 0 = Monday, 6 = Sunday
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for date in dates:
                day = date.weekday()  # 0 = Monday, 6 = Sunday
                day_counts[day] += 1
            
            axes[0, 0].bar(day_names, day_counts, color='skyblue')
            axes[0, 0].set_title('Trips by Day of Week')
            axes[0, 0].set_xlabel('Day')
            axes[0, 0].set_ylabel('Number of Trips')
            plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45)
            
            # 2. Distance distribution
            axes[0, 1].hist(distances, bins=10, color='green', alpha=0.7)
            axes[0, 1].set_title('Distance Distribution')
            axes[0, 1].set_xlabel('Distance (km)')
            axes[0, 1].set_ylabel('Frequency')
            
            # 3. CO2 saved over time (cumulative)
            sorted_dates = [date for _, date in sorted(zip(dates, dates))]
            sorted_co2 = [co2 for _, co2 in sorted(zip(dates, co2_saved))]
            
            cumulative_co2 = np.cumsum(sorted_co2)
            
            axes[1, 0].plot(sorted_dates, cumulative_co2, color='green', marker='o', linestyle='-', markersize=4)
            axes[1, 0].set_title('Cumulative CO2 Saved')
            axes[1, 0].set_xlabel('Date')
            axes[1, 0].set_ylabel('CO2 Saved (kg)')
            axes[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            plt.setp(axes[1, 0].xaxis.get_majorticklabels(), rotation=45)
            
            # 4. Calories burned per trip (last 10 trips)
            recent_dates = dates[-10:]
            recent_calories = calories[-10:]
            
            axes[1, 1].bar(recent_dates, recent_calories, color='orange')
            axes[1, 1].set_title('Calories Burned (Last 10 Trips)')
            axes[1, 1].set_xlabel('Date')
            axes[1, 1].set_ylabel('Calories')
            axes[1, 1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            plt.setp(axes[1, 1].xaxis.get_majorticklabels(), rotation=45)
            
            # Adjust layout and save the figure
            plt.tight_layout()
            plt.subplots_adjust(top=0.9)
            plt.savefig(summary_plot)
            plt.close()
            
            print(f"\nActivity summary visualization saved to: {summary_plot}")
            
            # Ask if user wants to view the visualization
            print("\nOptions:")
            print("1. View Visualization")
            print("2. Return to Data Visualization Menu")
            
            view_choice = input("\nSelect an option (1-2): ")
            if view_choice == "1":
                try:
                    webbrowser.open(f"file://{os.path.abspath(summary_plot)}")
                except Exception as e:
                    logger.error(f"Error opening visualization: {e}")
                    print(f"Error opening visualization: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error generating activity summary visualization: {e}")
            print(f"Error generating visualization: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def analyze_trip_history(self):
        """Analyze trip history with detailed visualizations."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Trip History Analysis")
        
        # Get user data
        user = self.user_manager.get_current_user()
        username = user.get('username')
        name = user.get('name', username)
        
        # Get user stats
        stats = user.get('stats', {})
        trips = stats.get('trips', [])
        
        # Check if user has any trips
        if not trips:
            print("No trip data available. Start logging your cycling trips to see visualizations!")
            input("\nPress Enter to continue...")
            return
        
        # Process trip data for visualization
        dates = []
        distances = []
        durations = []
        speeds = []  # km/h
        
        print("Processing trip data...")
        
        if TQDM_AVAILABLE:
            trip_iter = tqdm(trips)
        else:
            trip_iter = trips
            print(f"Processing {len(trips)} trips...")
        
        for trip in trip_iter:
            # Parse date
            date_str = trip.get('date')
            if not date_str:
                continue
            
            try:
                date = datetime.datetime.fromisoformat(date_str).date()
                dates.append(date)
                
                # Get trip data
                distance = trip.get('distance', 0.0)
                duration = trip.get('duration', 0.0)  # in minutes
                
                distances.append(distance)
                durations.append(duration)
                
                # Calculate speed (km/h)
                if duration > 0:
                    speed = (distance / duration) * 60  # convert to km/h
                else:
                    speed = 0
                speeds.append(speed)
                
            except (ValueError, TypeError):
                # Skip trips with invalid date format
                continue
        
        # Exit if no valid trips were found
        if not dates:
            print("\nNo valid trip data available.")
            input("\nPress Enter to continue...")
            return
        
        # Create file names for plots
        history_plot = os.path.join(VISUALIZATION_DIR, f"trip_history_{username}_{int(time.time())}.png")
        
        print("\nGenerating trip history visualization...")
        
        try:
            # Create a figure with 4 subplots
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f"Trip History Analysis for {name}", fontsize=16)
            
            # 1. Trip distances over time
            axes[0, 0].plot(dates, distances, color='blue', marker='o', linestyle='-', markersize=4)
            axes[0, 0].set_title('Trip Distances Over Time')
            axes[0, 0].set_xlabel('Date')
            axes[0, 0].set_ylabel('Distance (km)')
            axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Add moving average
            if len(distances) > 5:
                window = min(5, len(distances))
                distances_arr = np.array(distances)
                moving_avg = np.convolve(distances_arr, np.ones(window)/window, mode='valid')
                ma_dates = dates[window-1:]
                
                axes[0, 0].plot(ma_dates, moving_avg, color='red', linestyle='--', 
                           label=f'{window}-Trip Moving Avg')
                axes[0, 0].legend()
            
            # 2. Trip durations over time
            axes[0, 1].plot(dates, durations, color='green', marker='o', linestyle='-', markersize=4)
            axes[0, 1].set_title('Trip Durations Over Time')
            axes[0, 1].set_xlabel('Date')
            axes[0, 1].set_ylabel('Duration (minutes)')
            axes[0, 1].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # 3. Speed over time
            axes[1, 0].plot(dates, speeds, color='purple', marker='o', linestyle='-', markersize=4)
            axes[1, 0].set_title('Average Speed Over Time')
            axes[1, 0].set_xlabel('Date')
            axes[1, 0].set_ylabel('Speed (km/h)')
            axes[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # 4. Distance vs Duration scatter plot
            axes[1, 1].scatter(distances, durations, color='orange', alpha=0.7)
            axes[1, 1].set_title('Distance vs Duration')
            axes[1, 1].set_xlabel('Distance (km)')
            axes[1, 1].set_ylabel('Duration (minutes)')
            
            # Add best fit line
            if len(distances) > 1:
                fit = np.polyfit(distances, durations, 1)
                fit_fn = np.poly1d(fit)
                
                # Create line for plotting
                x_fit = np.linspace(min(distances), max(distances), 100)
                y_fit = fit_fn(x_fit)
                
                axes[1, 1].plot(x_fit, y_fit, 'r--', label=f'Best Fit ({fit[0]:.2f}x + {fit[1]:.2f})')
                axes[1, 1].legend()
            
            # Adjust layout and save the figure
            plt.tight_layout()
            plt.subplots_adjust(top=0.9)
            plt.savefig(history_plot)
            plt.close()
            
            print(f"\nTrip history visualization saved to: {history_plot}")
            
            # Ask if user wants to view the visualization
            print("\nOptions:")
            print("1. View Visualization")
            print("2. Return to Data Visualization Menu")
            
            view_choice = input("\nSelect an option (1-2): ")
            if view_choice == "1":
                try:
                    webbrowser.open(f"file://{os.path.abspath(history_plot)}")
                except Exception as e:
                    logger.error(f"Error opening visualization: {e}")
                    print(f"Error opening visualization: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error generating trip history visualization: {e}")
            print(f"Error generating visualization: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def visualize_carbon_savings(self):
        """Visualize carbon savings with comparisons and analytics."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Carbon Savings Visualization")
        
        # Get user data
        user = self.user_manager.get_current_user()
        username = user.get('username')
        name = user.get('name', username)
        
        # Get user stats
        stats = user.get('stats', {})
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        total_distance = stats.get('total_distance', 0.0)
        trips = stats.get('trips', [])
        
        # Check if user has any trips
        if not trips:
            print("No trip data available. Start logging your cycling trips to see visualizations!")
            input("\nPress Enter to continue...")
            return
        
        # Process trip data for visualization
        dates = []
        co2_saved = []
        
        print("Processing carbon data...")
        
        if TQDM_AVAILABLE:
            trip_iter = tqdm(trips)
        else:
            trip_iter = trips
            print(f"Processing {len(trips)} trips...")
        
        for trip in trip_iter:
            # Parse date
            date_str = trip.get('date')
            if not date_str:
                continue
            
            try:
                date = datetime.datetime.fromisoformat(date_str).date()
                dates.append(date)
                
                # Get CO2 data
                co2 = trip.get('co2_saved', 0.0)
                co2_saved.append(co2)
                
            except (ValueError, TypeError):
                # Skip trips with invalid date format
                continue
        
        # Exit if no valid trips were found
        if not dates:
            print("\nNo valid carbon data available.")
            input("\nPress Enter to continue...")
            return
        
        # Create file names for plots
        carbon_plot = os.path.join(VISUALIZATION_DIR, f"carbon_savings_{username}_{int(time.time())}.png")
        carbon_comparison = os.path.join(VISUALIZATION_DIR, f"carbon_comparison_{username}_{int(time.time())}.png")
        
        print("\nGenerating carbon savings visualization...")
        
        try:
            # Create the first figure - Carbon savings over time
            plt.figure(figsize=(10, 6))
            
            # Sort dates and corresponding CO2 values
            sorted_dates, sorted_co2 = zip(*sorted(zip(dates, co2_saved)))
            
            # Calculate cumulative CO2 savings
            cumulative_co2 = np.cumsum(sorted_co2)
            
            # Plot cumulative CO2 savings over time
            plt.plot(sorted_dates, cumulative_co2, color='green', marker='o', linestyle='-', markersize=6)
            plt.title(f'Cumulative CO2 Savings for {name}', fontsize=16)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('CO2 Saved (kg)', fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            plt.tick_params(axis='x', rotation=45)
            
            # Add annotations for key milestones
            milestones = [5, 10, 25, 50, 100, 250, 500]
            for milestone in milestones:
                if total_co2_saved >= milestone:
                    # Find closest point to this milestone
                    closest_idx = np.abs(np.array(cumulative_co2) - milestone).argmin()
                    milestone_date = sorted_dates[closest_idx]
                    milestone_co2 = cumulative_co2[closest_idx]
                    
                    plt.annotate(f'{milestone} kg', 
                                xy=(milestone_date, milestone_co2),
                                xytext=(10, 10),
                                textcoords='offset points',
                                arrowprops=dict(arrowstyle='->'))
            
            plt.tight_layout()
            plt.savefig(carbon_plot)
            plt.close()
            
            # Create the second figure - Carbon comparisons
            plt.figure(figsize=(12, 8))
            
            # Define equivalents
            car_km = total_co2_saved / 0.13  # kg CO2 per km in average car
            flights = total_co2_saved / 100  # Short flight (~100kg CO2)
            trees_days = total_co2_saved / 0.055  # One tree absorbs ~20kg CO2 per year = 0.055kg per day
            light_bulbs = total_co2_saved / 0.1  # 100W light bulb for 24 hours ~ 0.1kg CO2
            beef_kg = total_co2_saved / 27  # 1kg beef produces ~27kg CO2
            
            # Create comparison bar chart
            categories = ['Car Travel (km)', 'Short Flights', 'Tree-Days', 'Light Bulbs (24h)', 'Beef (kg)']
            values = [car_km, flights, trees_days, light_bulbs, beef_kg]
            
            plt.bar(categories, values, color=['grey', 'skyblue', 'green', 'yellow', 'red'])
            plt.title(f'CO2 Savings Equivalents for {name} ({total_co2_saved:.1f} kg)', fontsize=16)
            plt.ylabel('Equivalent Amount', fontsize=12)
            plt.grid(True, axis='y', linestyle='--', alpha=0.7)
            plt.tick_params(axis='x', rotation=45)
            
            # Add value labels on top of each bar
            for i, v in enumerate(values):
                plt.text(i, v + 0.1, f'{v:.1f}', ha='center')
            
            plt.tight_layout()
            plt.savefig(carbon_comparison)
            plt.close()
            
            print(f"\nCarbon savings visualizations saved to:")
            print(f"1. {carbon_plot}")
            print(f"2. {carbon_comparison}")
            
            # Display carbon savings stats
            print(f"\n{name}'s Carbon Savings Impact:")
            print(f"Total CO2 Saved: {total_co2_saved:.2f} kg")
            print(f"Equivalent to:")
            print(f"- Driving {car_km:.1f} km in an average car")
            print(f"- {flights:.2f} short-haul flights")
            print(f"- The daily absorption of {trees_days:.1f} trees")
            print(f"- Running {light_bulbs:.1f} light bulbs for 24 hours")
            print(f"- The production of {beef_kg:.1f} kg of beef")
            
            # Ask which visualization to view
            print("\nOptions:")
            print("1. View Carbon Savings Over Time")
            print("2. View Carbon Equivalents Comparison")
            print("3. Return to Data Visualization Menu")
            
            view_choice = input("\nSelect an option (1-3): ")
            
            if view_choice == "1":
                try:
                    webbrowser.open(f"file://{os.path.abspath(carbon_plot)}")
                except Exception as e:
                    logger.error(f"Error opening visualization: {e}")
                    print(f"Error opening visualization: {str(e)}")
            elif view_choice == "2":
                try:
                    webbrowser.open(f"file://{os.path.abspath(carbon_comparison)}")
                except Exception as e:
                    logger.error(f"Error opening visualization: {e}")
                    print(f"Error opening visualization: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error generating carbon savings visualization: {e}")
            print(f"Error generating visualization: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def show_progress_over_time(self):
        """Show progress metrics over time with trend analysis."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Progress Over Time")
        
        # Get user data
        user = self.user_manager.get_current_user()
        username = user.get('username')
        name = user.get('name', username)
        
        # Get user stats
        stats = user.get('stats', {})
        trips = stats.get('trips', [])
        
        # Check if user has any trips
        if not trips:
            print("No trip data available. Start logging your cycling trips to see visualizations!")
            input("\nPress Enter to continue...")
            return
        
        # Check if user has enough trips for meaningful analysis
        if len(trips) < 3:
            print("You need at least 3 trips for meaningful progress analysis.")
            print(f"Current number of trips: {len(trips)}")
            input("\nPress Enter to continue...")
            return
        
        # Process trip data for visualization
        dates = []
        distances = []
        speeds = []
        calories = []
        
        print("Processing trip data...")
        
        if TQDM_AVAILABLE:
            trip_iter = tqdm(trips)
        else:
            trip_iter = trips
            print(f"Processing {len(trips)} trips...")
        
        for trip in trip_iter:
            # Parse date
            date_str = trip.get('date')
            if not date_str:
                continue
            
            try:
                date = datetime.datetime.fromisoformat(date_str).date()
                dates.append(date)
                
                # Get trip data
                distance = trip.get('distance', 0.0)
                duration = trip.get('duration', 0.0)  # in minutes
                calorie = trip.get('calories', 0)
                
                distances.append(distance)
                calories.append(calorie)
                
                # Calculate speed (km/h)
                if duration > 0:
                    speed = (distance / duration) * 60  # convert to km/h
                else:
                    speed = 0
                speeds.append(speed)
                
            except (ValueError, TypeError):
                # Skip trips with invalid date format
                continue
        
        # Exit if not enough valid trips were found
        if len(dates) < 3:
            print("\nNot enough valid trip data available for progress analysis.")
            input("\nPress Enter to continue...")
            return
        
        # Sort all data by date
        sorted_data = sorted(zip(dates, distances, speeds, calories))
        sorted_dates = [d[0] for d in sorted_data]
        sorted_distances = [d[1] for d in sorted_data]
        sorted_speeds = [d[2] for d in sorted_data]
        sorted_calories = [d[3] for d in sorted_data]
        
        # Group data by month for monthly averages
        month_data = {}
        for date, distance, speed, calorie in sorted_data:
            month_key = date.strftime('%Y-%m')
            if month_key not in month_data:
                month_data[month_key] = {'distances': [], 'speeds': [], 'calories': []}
            
            month_data[month_key]['distances'].append(distance)
            month_data[month_key]['speeds'].append(speed)
            month_data[month_key]['calories'].append(calorie)
        
        # Calculate monthly averages
        months = []
        avg_distances = []
        avg_speeds = []
        avg_calories = []
        
        for month in sorted(month_data.keys()):
            months.append(datetime.datetime.strptime(month, '%Y-%m').date())
            avg_distances.append(sum(month_data[month]['distances']) / len(month_data[month]['distances']))
            avg_speeds.append(sum(month_data[month]['speeds']) / len(month_data[month]['speeds']))
            avg_calories.append(sum(month_data[month]['calories']) / len(month_data[month]['calories']))
        
        # Create file name for plot
        progress_plot = os.path.join(VISUALIZATION_DIR, f"progress_analysis_{username}_{int(time.time())}.png")
        
        print("\nGenerating progress analysis visualization...")
        
        try:
            # Create a figure with 4 subplots
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f"Progress Analysis for {name}", fontsize=16)
            
            # 1. Distance per trip with trend line
            axes[0, 0].plot(sorted_dates, sorted_distances, color='blue', marker='o', markersize=4, label='Distance')
            
            # Add trend line
            z = np.polyfit(range(len(sorted_dates)), sorted_distances, 1)
            p = np.poly1d(z)
            axes[0, 0].plot(sorted_dates, p(range(len(sorted_dates))), 'r--', label=f'Trend')
            
            axes[0, 0].set_title('Distance per Trip')
            axes[0, 0].set_xlabel('Date')
            axes[0, 0].set_ylabel('Distance (km)')
            axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            axes[0, 0].tick_params(axis='x', rotation=45)
            axes[0, 0].legend()
            
            # Calculate improvement
            if len(sorted_distances) >= 3:
                first_avg = sum(sorted_distances[:3]) / 3
                last_avg = sum(sorted_distances[-3:]) / 3
                pct_change = ((last_avg - first_avg) / first_avg) * 100 if first_avg > 0 else 0
                
                if pct_change >= 0:
                    change_text = f"Improvement: {pct_change:.1f}%"
                else:
                    change_text = f"Decrease: {abs(pct_change):.1f}%"
                
                axes[0, 0].text(0.05, 0.95, change_text, transform=axes[0, 0].transAxes, 
                           bbox=dict(facecolor='white', alpha=0.8))
            
            # 2. Average speed with trend line
            axes[0, 1].plot(sorted_dates, sorted_speeds, color='green', marker='o', markersize=4, label='Speed')
            
            # Add trend line
            z = np.polyfit(range(len(sorted_dates)), sorted_speeds, 1)
            p = np.poly1d(z)
            axes[0, 1].plot(sorted_dates, p(range(len(sorted_dates))), 'r--', label='Trend')
            
            axes[0, 1].set_title('Average Speed')
            axes[0, 1].set_xlabel('Date')
            axes[0, 1].set_ylabel('Speed (km/h)')
            axes[0, 1].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            axes[0, 1].tick_params(axis='x', rotation=45)
            axes[0, 1].legend()
            
            # Calculate improvement
            if len(sorted_speeds) >= 3:
                first_avg = sum(sorted_speeds[:3]) / 3
                last_avg = sum(sorted_speeds[-3:]) / 3
                pct_change = ((last_avg - first_avg) / first_avg) * 100 if first_avg > 0 else 0
                
                if pct_change >= 0:
                    change_text = f"Improvement: {pct_change:.1f}%"
                else:
                    change_text = f"Decrease: {abs(pct_change):.1f}%"
                
                axes[0, 1].text(0.05, 0.95, change_text, transform=axes[0, 1].transAxes, 
                           bbox=dict(facecolor='white', alpha=0.8))
            
            # 3. Monthly average distance
            axes[1, 0].bar(months, avg_distances, color='purple', width=20)
            axes[1, 0].set_title('Monthly Average Distance')
            axes[1, 0].set_xlabel('Month')
            axes[1, 0].set_ylabel('Avg Distance (km)')
            axes[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # 4. Monthly average speed
            axes[1, 1].bar(months, avg_speeds, color='orange', width=20)
            axes[1, 1].set_title('Monthly Average Speed')
            axes[1, 1].set_xlabel('Month')
            axes[1, 1].set_ylabel('Avg Speed (km/h)')
            axes[1, 1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            # Adjust layout and save the figure
            plt.tight_layout()
            plt.subplots_adjust(top=0.9)
            plt.savefig(progress_plot)
            plt.close()
            
            print(f"\nProgress analysis visualization saved to: {progress_plot}")
            
            # Calculate overall improvements
            if len(sorted_distances) >= 3 and len(sorted_speeds) >= 3:
                dist_first_avg = sum(sorted_distances[:3]) / 3
                dist_last_avg = sum(sorted_distances[-3:]) / 3
                dist_pct_change = ((dist_last_avg - dist_first_avg) / dist_first_avg) * 100 if dist_first_avg > 0 else 0
                
                speed_first_avg = sum(sorted_speeds[:3]) / 3
                speed_last_avg = sum(sorted_speeds[-3:]) / 3
                speed_pct_change = ((speed_last_avg - speed_first_avg) / speed_first_avg) * 100 if speed_first_avg > 0 else 0
                
                # Display summary
                print(f"\nProgress Summary for {name}:")
                
                print("\nDistance Improvement:")
                print(f"Initial average: {dist_first_avg:.1f} km")
                print(f"Current average: {dist_last_avg:.1f} km")
                print(f"Change: {'↑' if dist_pct_change >= 0 else '↓'} {abs(dist_pct_change):.1f}%")
                
                print("\nSpeed Improvement:")
                print(f"Initial average: {speed_first_avg:.1f} km/h")
                print(f"Current average: {speed_last_avg:.1f} km/h")
                print(f"Change: {'↑' if speed_pct_change >= 0 else '↓'} {abs(speed_pct_change):.1f}%")
            
            # Ask if user wants to view the visualization
            print("\nOptions:")
            print("1. View Visualization")
            print("2. Return to Data Visualization Menu")
            
            view_choice = input("\nSelect an option (1-2): ")
            if view_choice == "1":
                try:
                    webbrowser.open(f"file://{os.path.abspath(progress_plot)}")
                except Exception as e:
                    logger.error(f"Error opening visualization: {e}")
                    print(f"Error opening visualization: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error generating progress analysis visualization: {e}")
            print(f"Error generating visualization: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def generate_pdf_report(self):
        """Generate a comprehensive PDF report with all visualizations."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("PDF Report Generation")
        
        if not PDF_AVAILABLE:
            print("The FPDF library is required for generating PDF reports.")
            print("Please install it with: pip install fpdf")
            input("\nPress Enter to continue...")
            return
        
        # Get user data
        user = self.user_manager.get_current_user()
        username = user.get('username')
        name = user.get('name', username)
        
        # Get user stats
        stats = user.get('stats', {})
        total_trips = stats.get('total_trips', 0)
        total_distance = stats.get('total_distance', 0.0)
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        total_calories = stats.get('total_calories', 0)
        trips = stats.get('trips', [])
        
        # Check if user has any trips
        if not trips:
            print("No trip data available. Start logging your cycling trips to generate a report!")
            input("\nPress Enter to continue...")
            return
        
        # Define file name for the report
        report_file = os.path.join(REPORT_DIR, f"cycling_report_{username}_{datetime.date.today().strftime('%Y_%m_%d')}.pdf")
        
        # Create visualizations for the report
        print("\nGenerating visualizations for the report...")
        
        # First, generate the visualizations to include in the report
        vis_paths = {}
        
        try:
            # 1. Generate activity summary visualization
            activity_summary = os.path.join(VISUALIZATION_DIR, f"activity_summary_report_{username}.png")
            self._generate_activity_summary(user, activity_summary)
            vis_paths['activity_summary'] = activity_summary
            
            # 2. Generate carbon savings visualization
            carbon_viz = os.path.join(VISUALIZATION_DIR, f"carbon_savings_report_{username}.png")
            self._generate_carbon_visualization(user, carbon_viz)
            vis_paths['carbon_viz'] = carbon_viz
            
            # 3. Generate progress visualization (if enough trips)
            if len(trips) >= 3:
                progress_viz = os.path.join(VISUALIZATION_DIR, f"progress_report_{username}.png")
                self._generate_progress_visualization(user, progress_viz)
                vis_paths['progress_viz'] = progress_viz
        
        except Exception as e:
            logger.error(f"Error generating visualizations for report: {e}")
            print(f"Error generating visualizations: {str(e)}")
            input("\nPress Enter to continue...")
            return
        
        # Now create the PDF report
        print("\nGenerating PDF report...")
        
        try:
            # Create PDF
            pdf = FPDF()
            
            # Add a cover page
            pdf.add_page()
            pdf.set_font("Arial", "B", 24)
            pdf.cell(0, 20, "EcoCycle Cycling Report", ln=True, align="C")
            pdf.set_font("Arial", "", 16)
            pdf.cell(0, 15, f"For: {name}", ln=True, align="C")
            pdf.cell(0, 15, f"Generated on: {datetime.date.today().strftime('%B %d, %Y')}", ln=True, align="C")
            
            # Add logo or decorative element (if available)
            pdf.ln(20)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "EcoCycle - Cycle into a greener tomorrow", ln=True, align="C")
            
            # Summary page
            pdf.add_page()
            pdf.set_font("Arial", "B", 20)
            pdf.cell(0, 15, "Cycling Summary", ln=True)
            
            pdf.set_font("Arial", "B", 12)
            pdf.cell(60, 10, "Statistic", 1)
            pdf.cell(0, 10, "Value", 1, ln=True)
            
            pdf.set_font("Arial", "", 12)
            
            # Add summary statistics
            pdf.cell(60, 10, "Total Trips", 1)
            pdf.cell(0, 10, f"{total_trips}", 1, ln=True)
            
            pdf.cell(60, 10, "Total Distance", 1)
            pdf.cell(0, 10, f"{utils.format_distance(total_distance)}", 1, ln=True)
            
            pdf.cell(60, 10, "Total CO2 Saved", 1)
            pdf.cell(0, 10, f"{utils.format_co2(total_co2_saved)}", 1, ln=True)
            
            pdf.cell(60, 10, "Total Calories Burned", 1)
            pdf.cell(0, 10, f"{utils.format_calories(total_calories)}", 1, ln=True)
            
            # Calculate averages
            if total_trips > 0:
                avg_distance = total_distance / total_trips
                avg_co2_saved = total_co2_saved / total_trips
                avg_calories = total_calories / total_trips
                
                pdf.ln(10)
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "Trip Averages", ln=True)
                
                pdf.set_font("Arial", "B", 12)
                pdf.cell(60, 10, "Statistic", 1)
                pdf.cell(0, 10, "Value", 1, ln=True)
                
                pdf.set_font("Arial", "", 12)
                
                pdf.cell(60, 10, "Average Distance", 1)
                pdf.cell(0, 10, f"{avg_distance:.1f} km", 1, ln=True)
                
                pdf.cell(60, 10, "Average CO2 Saved", 1)
                pdf.cell(0, 10, f"{avg_co2_saved:.2f} kg", 1, ln=True)
                
                pdf.cell(60, 10, "Average Calories", 1)
                pdf.cell(0, 10, f"{avg_calories:.0f}", 1, ln=True)
            
            # Add activity summary visualization
            if 'activity_summary' in vis_paths and os.path.exists(vis_paths['activity_summary']):
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "Activity Summary", ln=True)
                pdf.image(vis_paths['activity_summary'], x=10, y=30, w=190)
            
            # Add carbon savings visualization
            if 'carbon_viz' in vis_paths and os.path.exists(vis_paths['carbon_viz']):
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "Carbon Savings", ln=True)
                pdf.image(vis_paths['carbon_viz'], x=10, y=30, w=190)
                
                # Add carbon equivalents
                car_km = total_co2_saved / 0.13
                flights = total_co2_saved / 100
                trees_days = total_co2_saved / 0.055
                
                pdf.ln(150)  # Move down past the image
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Environmental Impact", ln=True)
                
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 10, f"Your cycling has saved the equivalent of:", ln=True)
                pdf.cell(0, 10, f"- Driving {car_km:.1f} km in an average car", ln=True)
                pdf.cell(0, 10, f"- {flights:.2f} short-haul flights", ln=True)
                pdf.cell(0, 10, f"- The daily CO2 absorption of {trees_days:.1f} trees", ln=True)
            
            # Add progress visualization (if available)
            if 'progress_viz' in vis_paths and os.path.exists(vis_paths['progress_viz']):
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "Progress Over Time", ln=True)
                pdf.image(vis_paths['progress_viz'], x=10, y=30, w=190)
            
            # Add recent trips
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Recent Trips", ln=True)
            
            # Sort trips by date (newest first)
            recent_trips = sorted(trips, key=lambda x: x.get('date', ''), reverse=True)[:10]  # Get latest 10 trips
            
            if recent_trips:
                pdf.set_font("Arial", "B", 12)
                pdf.cell(40, 10, "Date", 1)
                pdf.cell(30, 10, "Distance", 1)
                pdf.cell(30, 10, "Duration", 1)
                pdf.cell(30, 10, "Speed", 1)
                pdf.cell(30, 10, "CO2 Saved", 1)
                pdf.cell(0, 10, "Calories", 1, ln=True)
                
                pdf.set_font("Arial", "", 10)
                
                for trip in recent_trips:
                    date_str = trip.get('date', '')
                    try:
                        if date_str:
                            date_obj = datetime.datetime.fromisoformat(date_str).date()
                            date_display = date_obj.strftime('%Y-%m-%d')
                        else:
                            date_display = "Unknown"
                    except ValueError:
                        date_display = "Unknown"
                    
                    distance = trip.get('distance', 0)
                    duration = trip.get('duration', 0)
                    co2 = trip.get('co2_saved', 0)
                    calories = trip.get('calories', 0)
                    
                    # Calculate speed
                    speed = 0
                    if duration > 0:
                        speed = (distance / duration) * 60  # km/h
                    
                    pdf.cell(40, 10, date_display, 1)
                    pdf.cell(30, 10, f"{distance:.1f} km", 1)
                    pdf.cell(30, 10, f"{duration:.0f} min", 1)
                    pdf.cell(30, 10, f"{speed:.1f} km/h", 1)
                    pdf.cell(30, 10, f"{co2:.2f} kg", 1)
                    pdf.cell(0, 10, f"{calories}", 1, ln=True)
            else:
                pdf.cell(0, 10, "No trip data available.", ln=True)
            
            # Add eco tips
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Eco Tips", ln=True)
            
            pdf.set_font("Arial", "", 12)
            pdf.ln(5)
            
            # Get some random tips
            tips = [eco_tips.get_random_tip() for _ in range(5)]
            
            for i, tip in enumerate(tips, 1):
                pdf.cell(0, 10, f"{i}. {tip.get('tip')}", ln=True)
                pdf.ln(5)
            
            # Final page with conclusion
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Conclusion", ln=True)
            
            pdf.set_font("Arial", "", 12)
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"Congratulations on your cycling journey, {name}! By cycling {utils.format_distance(total_distance)}, you've made a significant positive impact on your health and the environment.")
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"You've saved {utils.format_co2(total_co2_saved)} of CO2 emissions and burned {utils.format_calories(total_calories)} calories across {total_trips} trips.")
            pdf.ln(5)
            pdf.multi_cell(0, 10, "Keep up the great work and continue tracking your progress with EcoCycle!")
            
            # Output the PDF
            pdf.output(report_file)
            
            print(f"\nPDF report successfully generated: {report_file}")
            
            # Ask if user wants to open the report
            print("\nOptions:")
            print("1. Open PDF Report")
            print("2. Return to Data Visualization Menu")
            
            view_choice = input("\nSelect an option (1-2): ")
            if view_choice == "1":
                try:
                    webbrowser.open(f"file://{os.path.abspath(report_file)}")
                except Exception as e:
                    logger.error(f"Error opening PDF report: {e}")
                    print(f"Error opening PDF report: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            print(f"Error generating PDF report: {str(e)}")
        
        # Clean up temporary visualization files
        for path in vis_paths.values():
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
        
        input("\nPress Enter to continue...")
    
    def _generate_activity_summary(self, user, output_path):
        """Helper to generate activity summary visualization for reports."""
        username = user.get('username')
        name = user.get('name', username)
        
        # Get user stats
        stats = user.get('stats', {})
        trips = stats.get('trips', [])
        
        # Process trip data
        dates = []
        distances = []
        co2_saved = []
        calories = []
        
        for trip in trips:
            # Parse date
            date_str = trip.get('date')
            if not date_str:
                continue
            
            try:
                date = datetime.datetime.fromisoformat(date_str).date()
                dates.append(date)
                
                # Get trip data
                distance = trip.get('distance', 0.0)
                co2 = trip.get('co2_saved', 0.0)
                calorie = trip.get('calories', 0)
                
                distances.append(distance)
                co2_saved.append(co2)
                calories.append(calorie)
            except (ValueError, TypeError):
                continue
        
        # Check if enough data
        if not dates:
            raise ValueError("No valid trip data available")
        
        # Create a figure with 4 subplots
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        fig.suptitle(f"Activity Summary for {name}", fontsize=14)
        
        # 1. Trips per day of week
        day_counts = np.zeros(7)  # 0 = Monday, 6 = Sunday
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for date in dates:
            day = date.weekday()  # 0 = Monday, 6 = Sunday
            day_counts[day] += 1
        
        axes[0, 0].bar(day_names, day_counts, color='skyblue')
        axes[0, 0].set_title('Trips by Day of Week')
        axes[0, 0].set_xlabel('Day')
        axes[0, 0].set_ylabel('Number of Trips')
        
        # 2. Distance distribution
        axes[0, 1].hist(distances, bins=10, color='green', alpha=0.7)
        axes[0, 1].set_title('Distance Distribution')
        axes[0, 1].set_xlabel('Distance (km)')
        axes[0, 1].set_ylabel('Frequency')
        
        # 3. CO2 saved over time (cumulative)
        sorted_dates = [date for _, date in sorted(zip(dates, dates))]
        sorted_co2 = [co2 for _, co2 in sorted(zip(dates, co2_saved))]
        
        cumulative_co2 = np.cumsum(sorted_co2)
        
        axes[1, 0].plot(sorted_dates, cumulative_co2, color='green', marker='o', linestyle='-', markersize=3)
        axes[1, 0].set_title('Cumulative CO2 Saved')
        axes[1, 0].set_xlabel('Date')
        axes[1, 0].set_ylabel('CO2 Saved (kg)')
        axes[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
        plt.setp(axes[1, 0].xaxis.get_majorticklabels(), rotation=45)
        
        # 4. Calories burned per trip (last 10 trips)
        recent_dates = dates[-10:]
        recent_calories = calories[-10:]
        
        axes[1, 1].bar(recent_dates, recent_calories, color='orange')
        axes[1, 1].set_title('Calories Burned (Last 10 Trips)')
        axes[1, 1].set_xlabel('Date')
        axes[1, 1].set_ylabel('Calories')
        axes[1, 1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        plt.setp(axes[1, 1].xaxis.get_majorticklabels(), rotation=45)
        
        # Adjust layout and save the figure
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def _generate_carbon_visualization(self, user, output_path):
        """Helper to generate carbon savings visualization for reports."""
        username = user.get('username')
        name = user.get('name', username)
        
        # Get user stats
        stats = user.get('stats', {})
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        trips = stats.get('trips', [])
        
        # Process trip data
        dates = []
        co2_saved = []
        
        for trip in trips:
            # Parse date
            date_str = trip.get('date')
            if not date_str:
                continue
            
            try:
                date = datetime.datetime.fromisoformat(date_str).date()
                dates.append(date)
                
                # Get CO2 data
                co2 = trip.get('co2_saved', 0.0)
                co2_saved.append(co2)
                
            except (ValueError, TypeError):
                continue
        
        # Check if enough data
        if not dates:
            raise ValueError("No valid trip data available")
        
        # Define equivalents
        car_km = total_co2_saved / 0.13  # kg CO2 per km in average car
        flights = total_co2_saved / 100  # Short flight (~100kg CO2)
        trees_days = total_co2_saved / 0.055  # One tree absorbs ~20kg CO2 per year = 0.055kg per day
        light_bulbs = total_co2_saved / 0.1  # 100W light bulb for 24 hours ~ 0.1kg CO2
        beef_kg = total_co2_saved / 27  # 1kg beef produces ~27kg CO2
        
        # Create comparison bar chart
        plt.figure(figsize=(10, 6))
        
        categories = ['Car (km)', 'Flights', 'Tree-Days', 'Light Bulbs', 'Beef (kg)']
        values = [car_km, flights, trees_days, light_bulbs, beef_kg]
        
        plt.bar(categories, values, color=['grey', 'skyblue', 'green', 'yellow', 'red'])
        plt.title(f'CO2 Savings Equivalents for {name} ({total_co2_saved:.1f} kg)', fontsize=14)
        plt.ylabel('Equivalent Amount', fontsize=12)
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tick_params(axis='x', rotation=45)
        
        # Add value labels on top of each bar
        for i, v in enumerate(values):
            plt.text(i, v + 0.1, f'{v:.1f}', ha='center')
        
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def _generate_progress_visualization(self, user, output_path):
        """Helper to generate progress visualization for reports."""
        username = user.get('username')
        name = user.get('name', username)
        
        # Get user stats
        stats = user.get('stats', {})
        trips = stats.get('trips', [])
        
        # Process trip data
        dates = []
        distances = []
        speeds = []
        
        for trip in trips:
            # Parse date
            date_str = trip.get('date')
            if not date_str:
                continue
            
            try:
                date = datetime.datetime.fromisoformat(date_str).date()
                dates.append(date)
                
                # Get trip data
                distance = trip.get('distance', 0.0)
                duration = trip.get('duration', 0.0)  # in minutes
                
                distances.append(distance)
                
                # Calculate speed (km/h)
                if duration > 0:
                    speed = (distance / duration) * 60  # convert to km/h
                else:
                    speed = 0
                speeds.append(speed)
                
            except (ValueError, TypeError):
                continue
        
        # Check if enough data
        if len(dates) < 3:
            raise ValueError("Not enough valid trip data available for progress analysis")
        
        # Sort all data by date
        sorted_data = sorted(zip(dates, distances, speeds))
        sorted_dates = [d[0] for d in sorted_data]
        sorted_distances = [d[1] for d in sorted_data]
        sorted_speeds = [d[2] for d in sorted_data]
        
        # Create a figure with 2 subplots
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle(f"Progress Analysis for {name}", fontsize=14)
        
        # 1. Distance per trip with trend line
        axes[0].plot(sorted_dates, sorted_distances, color='blue', marker='o', markersize=3, label='Distance')
        
        # Add trend line
        z = np.polyfit(range(len(sorted_dates)), sorted_distances, 1)
        p = np.poly1d(z)
        axes[0].plot(sorted_dates, p(range(len(sorted_dates))), 'r--', label=f'Trend')
        
        axes[0].set_title('Distance Trend')
        axes[0].set_xlabel('Date')
        axes[0].set_ylabel('Distance (km)')
        axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].legend()
        
        # 2. Average speed with trend line
        axes[1].plot(sorted_dates, sorted_speeds, color='green', marker='o', markersize=3, label='Speed')
        
        # Add trend line
        z = np.polyfit(range(len(sorted_dates)), sorted_speeds, 1)
        p = np.poly1d(z)
        axes[1].plot(sorted_dates, p(range(len(sorted_dates))), 'r--', label='Trend')
        
        axes[1].set_title('Speed Trend')
        axes[1].set_xlabel('Date')
        axes[1].set_ylabel('Speed (km/h)')
        axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].legend()
        
        # Adjust layout and save the figure
        plt.tight_layout()
        plt.subplots_adjust(top=0.85)
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def export_data(self):
        """Export cycling data to various formats."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Export Data")
        
        # Get user data
        user = self.user_manager.get_current_user()
        username = user.get('username')
        
        # Get user stats
        stats = user.get('stats', {})
        trips = stats.get('trips', [])
        
        # Check if user has any trips
        if not trips:
            print("No trip data available to export.")
            input("\nPress Enter to continue...")
            return
        
        # Display export options
        print("Export Format Options:")
        print("1. CSV (Comma Separated Values)")
        print("2. JSON (JavaScript Object Notation)")
        print("3. Return to Data Visualization Menu")
        
        choice = input("\nSelect an option (1-3): ")
        
        if choice == "1":
            # Export to CSV
            filename = os.path.join(REPORT_DIR, f"cycling_data_{username}_{datetime.date.today().strftime('%Y_%m_%d')}.csv")
            
            try:
                with open(filename, 'w') as f:
                    # Write header
                    f.write("Date,Distance (km),Duration (min),CO2 Saved (kg),Calories Burned\n")
                    
                    # Write trip data
                    for trip in trips:
                        date_str = trip.get('date', '')
                        try:
                            if date_str:
                                date_obj = datetime.datetime.fromisoformat(date_str).date()
                                date_display = date_obj.strftime('%Y-%m-%d')
                            else:
                                date_display = "Unknown"
                        except ValueError:
                            date_display = "Unknown"
                        
                        distance = trip.get('distance', 0)
                        duration = trip.get('duration', 0)
                        co2 = trip.get('co2_saved', 0)
                        calories = trip.get('calories', 0)
                        
                        f.write(f"{date_display},{distance},{duration},{co2},{calories}\n")
                
                print(f"\nData successfully exported to CSV: {filename}")
                
                # Ask if user wants to open the file
                print("\nOptions:")
                print("1. Open CSV File (in default application)")
                print("2. Return to Data Visualization Menu")
                
                open_choice = input("\nSelect an option (1-2): ")
                if open_choice == "1":
                    try:
                        webbrowser.open(f"file://{os.path.abspath(filename)}")
                    except Exception as e:
                        logger.error(f"Error opening CSV file: {e}")
                        print(f"Error opening CSV file: {str(e)}")
            
            except Exception as e:
                logger.error(f"Error exporting to CSV: {e}")
                print(f"Error exporting to CSV: {str(e)}")
        
        elif choice == "2":
            # Export to JSON
            filename = os.path.join(REPORT_DIR, f"cycling_data_{username}_{datetime.date.today().strftime('%Y_%m_%d')}.json")
            
            try:
                # Prepare data
                export_data = {
                    "username": username,
                    "name": user.get('name', username),
                    "export_date": datetime.datetime.now().isoformat(),
                    "stats": stats
                }
                
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                print(f"\nData successfully exported to JSON: {filename}")
                
                # Ask if user wants to open the file
                print("\nOptions:")
                print("1. Open JSON File (in default application)")
                print("2. Return to Data Visualization Menu")
                
                open_choice = input("\nSelect an option (1-2): ")
                if open_choice == "1":
                    try:
                        webbrowser.open(f"file://{os.path.abspath(filename)}")
                    except Exception as e:
                        logger.error(f"Error opening JSON file: {e}")
                        print(f"Error opening JSON file: {str(e)}")
            
            except Exception as e:
                logger.error(f"Error exporting to JSON: {e}")
                print(f"Error exporting to JSON: {str(e)}")
        
        input("\nPress Enter to continue...")


def run_visualization(user_manager_instance=None, sheets_manager_instance=None):
    """
    Run the data visualization as a standalone module.
    
    Args:
        user_manager_instance: Optional user manager
        sheets_manager_instance: Optional sheets manager
    """
    visualizer = DataVisualization(user_manager_instance, sheets_manager_instance)
    visualizer.run_visualization()


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run visualization module
    run_visualization()