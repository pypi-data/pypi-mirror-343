#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EcoCycle - Carbon Footprint Module
Provides functionality for calculating and recommending carbon footprint reductions.
"""

import logging
import random
import time
from datetime import datetime

try:
    from tqdm import tqdm
    import colorama
    from colorama import Fore, Style
    from tabulate import tabulate
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False

# Try to use enhanced ASCII art if available
try:
    import enhanced_ascii_art as ascii_art
    ENHANCED_UI = True
except ImportError:
    import ascii_art
    ENHANCED_UI = False

# Import specific functions for convenience
from ascii_art import display_section_header, display_success_message, display_error_message, display_info_message

class CarbonFootprint:
    """Calculator and recommender for carbon footprint reduction."""
    
    def __init__(self, user_manager=None, sheets_manager=None):
        """Initialize the carbon footprint calculator."""
        self.user_manager = user_manager
        self.sheets_manager = sheets_manager
        
        # Constants for carbon calculations
        self.car_emissions_per_km = 0.192  # kg CO2 per km
        self.bus_emissions_per_km = 0.105  # kg CO2 per km
        self.train_emissions_per_km = 0.041  # kg CO2 per km
        self.plane_emissions_per_km = 0.255  # kg CO2 per km
        
        # Average emissions for various activities (kg CO2 per unit)
        self.emissions_data = {
            'beef_meal': 6.6,  # per meal
            'chicken_meal': 1.8,  # per meal
            'vegetarian_meal': 0.5,  # per meal
            'vegan_meal': 0.3,  # per meal
            'hot_shower': 2.5,  # per 10 min shower
            'washing_machine': 0.6,  # per load
            'dishwasher': 0.4,  # per cycle
            'computer_usage': 0.1,  # per hour
            'tv_usage': 0.08,  # per hour
            'home_heating': 7.5,  # per day (average)
            'air_conditioning': 10.5,  # per day (average)
        }
        
        # User's carbon footprint data (to be collected)
        self.user_footprint = {}
        
    def calculate_carbon_footprint(self):
        """Calculate and display a user's carbon footprint."""
        if not HAS_DEPENDENCIES:
            display_error_message("Required dependencies not available. Please install tqdm, colorama and tabulate.")
            return
        
        display_section_header("Carbon Footprint Calculator")
        
        # Get username (default to last used if available)
        if self.user_manager and self.user_manager.get_current_user():
            default_username = self.user_manager.get_current_user()
            username = input(f"Enter username [{default_username}]: ").strip()
            if not username:
                username = default_username
        else:
            username = input("Enter username: ").strip()
        
        if not username:
            display_error_message("Username cannot be empty.")
            return
        
        # Initialize or retrieve user's footprint data
        self.user_footprint = self._get_user_footprint(username)
        
        # Collect user input for footprint calculation
        display_info_message("Please answer these questions to calculate your carbon footprint")
        
        self._collect_transportation_data()
        self._collect_food_data()
        self._collect_home_data()
        
        # Calculate the total carbon footprint
        display_info_message("Calculating your carbon footprint...")
        
        # Use enhanced loading animation if available
        if ENHANCED_UI and hasattr(ascii_art, 'display_loading_animation'):
            ascii_art.display_loading_animation("Processing carbon footprint data", 1.5)
        else:
            # Fall back to tqdm if available
            with tqdm(total=100, desc="Processing", unit="%") as pbar:
                time.sleep(1)  # Simulate calculation time
                pbar.update(100)
        
        total_footprint = self._calculate_total_footprint()
        
        # Display the results
        self._display_footprint_results(total_footprint)
        
        # Save the footprint data
        if self.sheets_manager:
            try:
                self._save_footprint_data(username, total_footprint)
                display_success_message("Carbon footprint data saved.")
            except Exception as e:
                logging.error(f"Error saving carbon footprint data: {e}", exc_info=True)
                display_error_message("Could not save carbon footprint data.")
        
        # Generate personalized recommendations
        self._display_recommendations()
        
        input("\nPress Enter to continue...")
    
    def _get_user_footprint(self, username):
        """Get or initialize user's footprint data."""
        # If we have a sheets manager, try to retrieve existing data
        if self.sheets_manager:
            try:
                # Try to get existing footprint data for this user
                # This would typically be stored in a separate sheet or table
                # For now, return an empty dictionary as placeholder
                return {}
            except Exception as e:
                logging.error(f"Error retrieving carbon footprint data: {e}", exc_info=True)
                return {}
        
        # If no data is available, return empty dictionary
        return {}
    
    def _collect_transportation_data(self):
        """Collect transportation-related carbon footprint data."""
        print(f"\n{Fore.CYAN}Transportation:{Style.RESET_ALL}")
        
        # Daily commute
        try:
            commute_distance = float(input("How many kilometers do you commute daily (total round trip)? ").strip() or "10")
            
            print("\nWhat is your primary mode of transportation?")
            print("1. Car")
            print("2. Public transportation (bus)")
            print("3. Public transportation (train/subway)")
            print("4. Bicycle or walking")
            
            mode_choice = input("Enter choice (1-4): ").strip() or "1"
            self.user_footprint['commute_mode'] = mode_choice
            self.user_footprint['commute_distance'] = commute_distance
            
            # Long distance travel
            flights_per_year = int(input("\nHow many one-way flights do you take per year? ").strip() or "2")
            avg_flight_distance = float(input("What's the average distance of your flights (in km)? ").strip() or "2000")
            
            self.user_footprint['flights_per_year'] = flights_per_year
            self.user_footprint['avg_flight_distance'] = avg_flight_distance
            
            # Car usage apart from commuting
            car_km_per_week = float(input("\nHow many kilometers do you drive for non-commuting purposes per week? ").strip() or "50")
            self.user_footprint['car_km_per_week'] = car_km_per_week
            
        except ValueError:
            display_error_message("Please enter numeric values for distances.")
            # Set default values
            self.user_footprint['commute_mode'] = "1"
            self.user_footprint['commute_distance'] = 10
            self.user_footprint['flights_per_year'] = 2
            self.user_footprint['avg_flight_distance'] = 2000
            self.user_footprint['car_km_per_week'] = 50
    
    def _collect_food_data(self):
        """Collect food-related carbon footprint data."""
        print(f"\n{Fore.CYAN}Food Consumption:{Style.RESET_ALL}")
        
        try:
            print("How many meals per week do you eat that contain:")
            beef_meals = int(input("Beef? ").strip() or "3")
            chicken_meals = int(input("Chicken or pork? ").strip() or "5")
            vegetarian_meals = int(input("Vegetarian (with dairy/eggs)? ").strip() or "7")
            vegan_meals = int(input("Vegan (plant-based only)? ").strip() or "6")
            
            self.user_footprint['beef_meals'] = beef_meals
            self.user_footprint['chicken_meals'] = chicken_meals
            self.user_footprint['vegetarian_meals'] = vegetarian_meals
            self.user_footprint['vegan_meals'] = vegan_meals
            
            # Food waste
            food_waste_percent = int(input("\nWhat percentage of your food do you typically waste? ").strip() or "15")
            self.user_footprint['food_waste_percent'] = food_waste_percent
            
        except ValueError:
            display_error_message("Please enter numeric values for meal counts.")
            # Set default values
            self.user_footprint['beef_meals'] = 3
            self.user_footprint['chicken_meals'] = 5
            self.user_footprint['vegetarian_meals'] = 7
            self.user_footprint['vegan_meals'] = 6
            self.user_footprint['food_waste_percent'] = 15
    
    def _collect_home_data(self):
        """Collect home-related carbon footprint data."""
        print(f"\n{Fore.CYAN}Home Energy Usage:{Style.RESET_ALL}")
        
        try:
            # Heating and cooling
            heating_months = int(input("How many months per year do you use heating? ").strip() or "5")
            ac_months = int(input("How many months per year do you use air conditioning? ").strip() or "3")
            
            # Water usage
            shower_minutes = float(input("\nHow many minutes is your average shower? ").strip() or "10")
            showers_per_week = int(input("How many showers do you take per week? ").strip() or "7")
            
            # Appliance usage
            laundry_loads = int(input("\nHow many loads of laundry do you do per week? ").strip() or "3")
            dishwasher_cycles = int(input("How many dishwasher cycles do you run per week? ").strip() or "4")
            
            # Electronics
            computer_hours = float(input("\nHow many hours per day do you use computers/devices? ").strip() or "8")
            tv_hours = float(input("How many hours per day do you watch TV? ").strip() or "2")
            
            # Store all the values
            self.user_footprint.update({
                'heating_months': heating_months,
                'ac_months': ac_months,
                'shower_minutes': shower_minutes,
                'showers_per_week': showers_per_week,
                'laundry_loads': laundry_loads,
                'dishwasher_cycles': dishwasher_cycles,
                'computer_hours': computer_hours,
                'tv_hours': tv_hours
            })
            
        except ValueError:
            display_error_message("Please enter numeric values for all questions.")
            # Set default values
            self.user_footprint.update({
                'heating_months': 5,
                'ac_months': 3,
                'shower_minutes': 10,
                'showers_per_week': 7,
                'laundry_loads': 3,
                'dishwasher_cycles': 4,
                'computer_hours': 8,
                'tv_hours': 2
            })
    
    def _calculate_total_footprint(self):
        """Calculate the total carbon footprint based on collected data."""
        # Transportation emissions
        transport_emissions = self._calculate_transportation_emissions()
        
        # Food emissions
        food_emissions = self._calculate_food_emissions()
        
        # Home emissions
        home_emissions = self._calculate_home_emissions()
        
        # Total annual footprint
        total = {
            'transportation': transport_emissions,
            'food': food_emissions,
            'home': home_emissions,
            'total': transport_emissions + food_emissions + home_emissions
        }
        
        return total
    
    def _calculate_transportation_emissions(self):
        """Calculate transportation-related emissions."""
        commute_emissions = 0
        commute_distance = self.user_footprint.get('commute_distance', 10)
        commute_mode = self.user_footprint.get('commute_mode', '1')
        
        # Calculate based on commute mode
        if commute_mode == '1':  # Car
            commute_emissions = commute_distance * self.car_emissions_per_km
        elif commute_mode == '2':  # Bus
            commute_emissions = commute_distance * self.bus_emissions_per_km
        elif commute_mode == '3':  # Train
            commute_emissions = commute_distance * self.train_emissions_per_km
        elif commute_mode == '4':  # Bicycle/walking
            commute_emissions = 0
        
        # Annual commute emissions (assuming 250 working days)
        annual_commute = commute_emissions * 250
        
        # Flight emissions
        flights_per_year = self.user_footprint.get('flights_per_year', 2)
        avg_flight_distance = self.user_footprint.get('avg_flight_distance', 2000)
        flight_emissions = flights_per_year * avg_flight_distance * self.plane_emissions_per_km
        
        # Other car usage
        car_km_per_week = self.user_footprint.get('car_km_per_week', 50)
        other_car_emissions = car_km_per_week * self.car_emissions_per_km * 52  # annual
        
        total_transport = annual_commute + flight_emissions + other_car_emissions
        return total_transport
    
    def _calculate_food_emissions(self):
        """Calculate food-related emissions."""
        # Get meal counts
        beef_meals = self.user_footprint.get('beef_meals', 3)
        chicken_meals = self.user_footprint.get('chicken_meals', 5)
        vegetarian_meals = self.user_footprint.get('vegetarian_meals', 7)
        vegan_meals = self.user_footprint.get('vegan_meals', 6)
        
        # Calculate weekly emissions
        weekly_emissions = (
            beef_meals * self.emissions_data['beef_meal'] +
            chicken_meals * self.emissions_data['chicken_meal'] +
            vegetarian_meals * self.emissions_data['vegetarian_meal'] +
            vegan_meals * self.emissions_data['vegan_meal']
        )
        
        # Account for food waste
        food_waste_percent = self.user_footprint.get('food_waste_percent', 15)
        food_waste_factor = 1 + (food_waste_percent / 100)
        
        # Calculate annual food emissions
        annual_food_emissions = weekly_emissions * 52 * food_waste_factor
        
        return annual_food_emissions
    
    def _calculate_home_emissions(self):
        """Calculate home-related emissions."""
        # Heating and cooling
        heating_months = self.user_footprint.get('heating_months', 5)
        ac_months = self.user_footprint.get('ac_months', 3)
        
        heating_emissions = heating_months * 30 * self.emissions_data['home_heating']
        ac_emissions = ac_months * 30 * self.emissions_data['air_conditioning']
        
        # Water usage
        shower_minutes = self.user_footprint.get('shower_minutes', 10)
        showers_per_week = self.user_footprint.get('showers_per_week', 7)
        
        shower_factor = shower_minutes / 10  # emissions are per 10 min shower
        shower_emissions = shower_factor * self.emissions_data['hot_shower'] * showers_per_week * 52
        
        # Appliance usage
        laundry_loads = self.user_footprint.get('laundry_loads', 3)
        dishwasher_cycles = self.user_footprint.get('dishwasher_cycles', 4)
        
        laundry_emissions = laundry_loads * self.emissions_data['washing_machine'] * 52
        dishwasher_emissions = dishwasher_cycles * self.emissions_data['dishwasher'] * 52
        
        # Electronics
        computer_hours = self.user_footprint.get('computer_hours', 8)
        tv_hours = self.user_footprint.get('tv_hours', 2)
        
        computer_emissions = computer_hours * self.emissions_data['computer_usage'] * 365
        tv_emissions = tv_hours * self.emissions_data['tv_usage'] * 365
        
        total_home = heating_emissions + ac_emissions + shower_emissions + laundry_emissions + dishwasher_emissions + computer_emissions + tv_emissions
        
        return total_home
    
    def _display_footprint_results(self, footprint):
        """Display the calculated carbon footprint results."""
        total = footprint['total']
        transportation = footprint['transportation']
        food = footprint['food']
        home = footprint['home']
        
        # Display the total
        print(f"\n{Fore.GREEN}Your Annual Carbon Footprint:{Style.RESET_ALL}")
        
        # Enhanced visualization with progress bars if available
        if ENHANCED_UI and hasattr(ascii_art, 'display_animated_progress_bar'):
            # Display enhanced progress bars showing the contribution of each category
            print("\nCategory Breakdown:")
            
            # Transportation bar (animated)
            transport_percent = transportation / total * 100
            ascii_art.display_animated_progress_bar(
                transportation, total, 50, 
                f"Transportation: {transportation:.2f} kg CO2 ({transport_percent:.1f}%)", 
                0.5, True
            )
            
            # Food bar (animated)
            food_percent = food / total * 100
            ascii_art.display_animated_progress_bar(
                food, total, 50, 
                f"Food: {food:.2f} kg CO2 ({food_percent:.1f}%)", 
                0.5, True
            )
            
            # Home bar (animated)
            home_percent = home / total * 100
            ascii_art.display_animated_progress_bar(
                home, total, 50, 
                f"Home Energy: {home:.2f} kg CO2 ({home_percent:.1f}%)", 
                0.5, True
            )
            
            # Total bar (non-animated)
            ascii_art.display_progress_bar(
                total, total, 50, 
                f"TOTAL: {total:.2f} kg CO2 (100%)"
            )
        else:
            # Format as a table (traditional display)
            data = [
                ["Transportation", f"{transportation:.2f} kg CO2", f"{(transportation/total)*100:.1f}%"],
                ["Food", f"{food:.2f} kg CO2", f"{(food/total)*100:.1f}%"],
                ["Home Energy", f"{home:.2f} kg CO2", f"{(home/total)*100:.1f}%"],
                ["TOTAL", f"{total:.2f} kg CO2", "100%"]
            ]
            
            print(tabulate(data, headers=["Category", "CO2 Emissions", "Percentage"], tablefmt="grid"))
        
        # Compare to averages
        average_annual = 5000  # kg CO2 (simplified average)
        
        # Visualize comparison if enhanced UI is available
        if ENHANCED_UI and hasattr(ascii_art, 'display_animated_progress_bar'):
            print("\nComparison to Average:")
            ascii_art.display_animated_progress_bar(
                total, average_annual * 2, 50, 
                f"Your Footprint vs. Average ({average_annual} kg CO2)", 
                1.0, True
            )
        
        # Feedback message
        if total < average_annual * 0.5:
            print(f"\n{Fore.GREEN}Your carbon footprint is significantly lower than average. Great job!{Style.RESET_ALL}")
        elif total < average_annual:
            print(f"\n{Fore.GREEN}Your carbon footprint is lower than average. Nice work!{Style.RESET_ALL}")
        elif total < average_annual * 1.5:
            print(f"\n{Fore.YELLOW}Your carbon footprint is slightly higher than average.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}Your carbon footprint is higher than average.{Style.RESET_ALL}")
    
    def _save_footprint_data(self, username, footprint):
        """Save the carbon footprint data to Google Sheets."""
        if not self.sheets_manager:
            return
        
        # Format data for saving
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [
            username,
            timestamp,
            str(footprint['total']),
            str(footprint['transportation']),
            str(footprint['food']),
            str(footprint['home'])
        ]
        
        # Save to a specific sheet - in a real implementation, this would be saved to a dedicated sheet
        sheet_name = "CarbonFootprint"
        try:
            # Ensure the sheet exists
            # This would be implemented in a real application
            # self.sheets_manager._ensure_sheets_exist([sheet_name])
            
            # Append the data
            # self.sheets_manager.append_row(sheet_name, row_data)
            pass
        except Exception as e:
            logging.error(f"Error saving carbon footprint data: {e}", exc_info=True)
            raise
    
    def _display_recommendations(self):
        """Display personalized recommendations based on the carbon footprint calculation."""
        print(f"\n{Fore.CYAN}Personalized Carbon Reduction Recommendations:{Style.RESET_ALL}")
        
        recommendations = []
        
        # Transportation recommendations
        commute_mode = self.user_footprint.get('commute_mode', '1')
        if commute_mode == '1':  # Car
            recommendations.append("🚲 Switch to cycling for your daily commute. Could save ~3 kg CO2 per day.")
            recommendations.append("🚌 Consider using public transportation. Could reduce emissions by up to 50%.")
        
        flights_per_year = self.user_footprint.get('flights_per_year', 2)
        if flights_per_year >= 4:
            recommendations.append("✈️ Consider reducing air travel or carbon offsetting. Air travel has high impact.")
        
        car_km_per_week = self.user_footprint.get('car_km_per_week', 50)
        if car_km_per_week > 100:
            recommendations.append("🚗 Try to consolidate car trips and reduce non-essential travel.")
        
        # Food recommendations
        beef_meals = self.user_footprint.get('beef_meals', 3)
        if beef_meals >= 3:
            recommendations.append("🥩 Reducing beef consumption by 50% could save ~10 kg CO2 weekly.")
        
        food_waste_percent = self.user_footprint.get('food_waste_percent', 15)
        if food_waste_percent > 10:
            recommendations.append("🍎 Reducing food waste has multiple benefits. Try meal planning.")
        
        # Home recommendations
        shower_minutes = self.user_footprint.get('shower_minutes', 10)
        if shower_minutes > 8:
            recommendations.append("🚿 Shorter showers can save water and energy. Aim for 5 minutes.")
        
        heating_months = self.user_footprint.get('heating_months', 5)
        ac_months = self.user_footprint.get('ac_months', 3)
        if heating_months + ac_months > 6:
            recommendations.append("🌡️ Adjust thermostat by 1-2 degrees to save significant energy.")
        
        laundry_loads = self.user_footprint.get('laundry_loads', 3)
        if laundry_loads > 2:
            recommendations.append("👕 Wash full loads of laundry and use cold water when possible.")
        
        computer_hours = self.user_footprint.get('computer_hours', 8)
        tv_hours = self.user_footprint.get('tv_hours', 2)
        if computer_hours + tv_hours > 8:
            recommendations.append("💡 Reduce device usage and ensure they're power-efficient.")
        
        # Add cycling-specific recommendations
        recommendations.append("🚴 Each additional 10 km cycled instead of driving saves ~2 kg CO2.")
        recommendations.append("🌿 Join a local cycling advocacy group to promote sustainable transport.")
        
        # Display the recommendations
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"{i}. {rec}")
        
        # Add a cycling challenge
        print(f"\n{Fore.GREEN}Cycling Challenge:{Style.RESET_ALL}")
        print("Try replacing 50% of your car trips under 5 km with cycling.")
        print(f"Potential annual CO2 savings: {(car_km_per_week * 0.25 * 52 * self.car_emissions_per_km):.2f} kg")
        
        # Progress tracking suggestion
        print(f"\n{Fore.YELLOW}Track Your Progress:{Style.RESET_ALL}")
        print("Return to the Carbon Footprint Calculator monthly to see your improvements!")

    def generate_recommendations(self):
        """Generate and display personalized carbon footprint reduction recommendations."""
        if not HAS_DEPENDENCIES:
            display_error_message("Required dependencies not available. Please install tqdm, colorama and tabulate.")
            return
        
        display_section_header("Carbon Footprint Recommendations")
        
        # Get username
        if self.user_manager and self.user_manager.get_current_user():
            default_username = self.user_manager.get_current_user()
            username = input(f"Enter username [{default_username}]: ").strip()
            if not username:
                username = default_username
        else:
            username = input("Enter username: ").strip()
        
        if not username:
            display_error_message("Username cannot be empty.")
            return
        
        # Check if we have footprint data for this user
        has_data = False
        
        # If we have a sheets manager, try to retrieve existing data
        if self.sheets_manager:
            try:
                # In a real implementation, would check if user has footprint data
                # For now, we'll simulate asking some quick questions
                has_data = False
            except Exception as e:
                logging.error(f"Error retrieving carbon footprint data: {e}", exc_info=True)
                has_data = False
        
        if not has_data:
            # Ask a few quick questions to generate basic recommendations
            display_info_message("Please answer a few questions to get personalized recommendations")
            
            try:
                print("\nWhat's your primary mode of transportation?")
                print("1. Car")
                print("2. Public transportation")
                print("3. Bicycle or walking")
                print("4. Mix of different modes")
                
                mode_choice = input("Enter choice (1-4): ").strip() or "1"
                
                print("\nHow many days per week do you currently cycle?")
                cycling_days = int(input("Enter number (0-7): ").strip() or "1")
                
                print("\nWhich area would you like to focus on for carbon reduction?")
                print("1. Transportation")
                print("2. Home energy use")
                print("3. Food choices")
                print("4. Overall lifestyle")
                
                focus_area = input("Enter choice (1-4): ").strip() or "1"
                
                # Generate recommendations based on these simple inputs
                self._display_quick_recommendations(mode_choice, cycling_days, focus_area)
            except ValueError:
                display_error_message("Please enter valid numeric choices.")
                # Use defaults
                self._display_quick_recommendations("1", 1, "1")
        else:
            # Generate detailed recommendations based on saved data
            self._display_recommendations()
        
        input("\nPress Enter to continue...")
    
    def _display_quick_recommendations(self, mode_choice, cycling_days, focus_area):
        """Display quick recommendations based on minimal input."""
        print(f"\n{Fore.CYAN}Quick Carbon Reduction Recommendations:{Style.RESET_ALL}")
        
        recommendations = []
        
        # Transportation recommendations based on current mode
        if mode_choice == "1":  # Car
            recommendations.append("🚲 Try cycling for trips under 5 km - each kilometer cycled saves ~0.2 kg CO2.")
            recommendations.append("🚌 Consider carpooling or public transit 1-2 days per week.")
            recommendations.append("🛣️ Plan efficient routes to minimize unnecessary driving.")
        elif mode_choice == "2":  # Public transit
            recommendations.append("🚆 Great choice! Public transit reduces emissions significantly.")
            recommendations.append("🚲 Consider cycling to transit stops for first/last mile connectivity.")
            recommendations.append("🚶 Walking short distances is even better than transit for zero emissions.")
        elif mode_choice == "3":  # Already cycling/walking
            recommendations.append("🌟 Excellent! You're already using low-carbon transportation.")
            recommendations.append("🏆 Set a challenge to increase your cycling days each month.")
            recommendations.append("👥 Encourage friends and family to join your cycling habits.")
        else:  # Mix
            recommendations.append("🚲 Identify which car trips could be replaced with cycling.")
            recommendations.append("📅 Try scheduling specific days as car-free days each week.")
            recommendations.append("🔄 Consider intermodal travel - combine cycling with public transit.")
        
        # Recommendations based on current cycling frequency
        if cycling_days < 2:
            recommendations.append("🚴 Set a goal to cycle one additional day per week this month.")
            recommendations.append("🧠 Start with short, easy routes to build confidence.")
        elif cycling_days < 5:
            recommendations.append("📈 Great cycling habits! Consider adding one more cycling day.")
            recommendations.append("🔧 Ensure your bike is well-maintained for efficient riding.")
        else:
            recommendations.append("🏅 You're a cycling champion! Share your routes with others.")
            recommendations.append("🌱 Calculate and celebrate your carbon savings from cycling.")
        
        # Focus area recommendations
        if focus_area == "1":  # Transportation
            recommendations.append("🚗 Keep a travel diary to identify trips that could be replaced with cycling.")
            recommendations.append("🔌 If considering a new vehicle, look into electric or hybrid options.")
            recommendations.append("✈️ Reduce air travel when possible or use offsetting programs.")
        elif focus_area == "2":  # Home energy
            recommendations.append("💡 Switch to LED light bulbs and turn off lights when not in use.")
            recommendations.append("🌡️ Adjust your thermostat by just 1-2 degrees for significant savings.")
            recommendations.append("🔌 Unplug devices instead of leaving them on standby.")
        elif focus_area == "3":  # Food
            recommendations.append("🥩 Reduce meat consumption, especially beef, for major carbon savings.")
            recommendations.append("🌽 Try having one plant-based day per week as a starting point.")
            recommendations.append("🛒 Buy local, seasonal produce to reduce food miles.")
        else:  # Overall
            recommendations.append("📝 Track your carbon footprint monthly using EcoCycle's tools.")
            recommendations.append("🛍️ Consider the lifecycle emissions when making purchasing decisions.")
            recommendations.append("♻️ Improve recycling habits and aim to reduce overall waste.")
        
        # Display the recommendations
        for i, rec in enumerate(recommendations[:8], 1):
            print(f"{i}. {rec}")
        
        # Add a cycling challenge based on current cycling days
        target_days = min(cycling_days + 2, 7)
        co2_savings = (target_days - cycling_days) * 10 * 0.192  # 10km per day average
        
        print(f"\n{Fore.GREEN}Cycling Challenge:{Style.RESET_ALL}")
        print(f"Increase your cycling from {cycling_days} to {target_days} days per week.")
        print(f"Potential weekly CO2 savings: {co2_savings:.2f} kg")
        print(f"Potential annual CO2 savings: {co2_savings * 52:.2f} kg")
        
        # Final encouragement
        print(f"\n{Fore.YELLOW}Every small change adds up to significant impact over time!{Style.RESET_ALL}")