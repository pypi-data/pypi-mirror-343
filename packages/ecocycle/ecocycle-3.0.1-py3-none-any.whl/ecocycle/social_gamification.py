"""
EcoCycle - Social Gamification Module
Provides functionality for social sharing, achievements, and gamification.
"""
import os
import json
import logging
import time
import random
import re
import datetime
import webbrowser
from typing import Dict, List, Optional, Any, Tuple, Union

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

# Import utilities
import utils
import ascii_art
import eco_tips

logger = logging.getLogger(__name__)

# Constants
ACHIEVEMENTS_FILE = "achievements.json"
LEADERBOARD_FILE = "leaderboard.json"
CHALLENGES_FILE = "challenges.json"

# Define achievements
ACHIEVEMENTS = [
    {
        "id": "first_ride",
        "name": "First Pedal",
        "description": "Complete your first cycling trip",
        "requirement": {"total_trips": 1},
        "points": 10,
        "icon": "🚲"
    },
    {
        "id": "eco_warrior",
        "name": "Eco Warrior",
        "description": "Save 10kg of CO2 through cycling",
        "requirement": {"total_co2_saved": 10},
        "points": 25,
        "icon": "🌿"
    },
    {
        "id": "distance_10",
        "name": "Road Explorer",
        "description": "Cycle a total of 10km",
        "requirement": {"total_distance": 10},
        "points": 15,
        "icon": "🗺️"
    },
    {
        "id": "distance_50",
        "name": "Distance Champion",
        "description": "Cycle a total of 50km",
        "requirement": {"total_distance": 50},
        "points": 30,
        "icon": "🏆"
    },
    {
        "id": "distance_100",
        "name": "Century Rider",
        "description": "Cycle a total of 100km",
        "requirement": {"total_distance": 100},
        "points": 50,
        "icon": "💯"
    },
    {
        "id": "calories_1000",
        "name": "Calorie Burner",
        "description": "Burn 1000 calories through cycling",
        "requirement": {"total_calories": 1000},
        "points": 20,
        "icon": "🔥"
    },
    {
        "id": "co2_saved_50",
        "name": "Climate Guardian",
        "description": "Save 50kg of CO2 through cycling",
        "requirement": {"total_co2_saved": 50},
        "points": 40,
        "icon": "🌍"
    },
    {
        "id": "co2_saved_100",
        "name": "Carbon Crusher",
        "description": "Save 100kg of CO2 through cycling",
        "requirement": {"total_co2_saved": 100},
        "points": 75,
        "icon": "♻️"
    },
    {
        "id": "trips_10",
        "name": "Regular Rider",
        "description": "Complete 10 cycling trips",
        "requirement": {"total_trips": 10},
        "points": 25,
        "icon": "🚴"
    },
    {
        "id": "trips_50",
        "name": "Devoted Cyclist",
        "description": "Complete 50 cycling trips",
        "requirement": {"total_trips": 50},
        "points": 100,
        "icon": "👑"
    }
]

# Define challenges
CHALLENGES = [
    {
        "id": "week_challenge_1",
        "name": "Weekly Distance Challenge",
        "description": "Cycle at least 20km this week",
        "requirement": {"weekly_distance": 20},
        "points": 30,
        "duration": 7,  # days
        "icon": "📏"
    },
    {
        "id": "week_challenge_2",
        "name": "CO2 Saver of the Week",
        "description": "Save at least 5kg of CO2 this week",
        "requirement": {"weekly_co2_saved": 5},
        "points": 35,
        "duration": 7,  # days
        "icon": "🌲"
    },
    {
        "id": "month_challenge_1",
        "name": "Monthly Cycling Streak",
        "description": "Cycle at least 15 times this month",
        "requirement": {"monthly_trips": 15},
        "points": 100,
        "duration": 30,  # days
        "icon": "📅"
    }
]


class SocialGamification:
    """Social sharing and gamification features for EcoCycle."""
    
    def __init__(self, user_manager=None, sheets_manager=None):
        """Initialize the social gamification module."""
        self.user_manager = user_manager
        self.sheets_manager = sheets_manager
        
        # Load achievements and challenges
        self.achievements = self._load_achievements()
        self.challenges = self._load_challenges()
        self.leaderboard = self._load_leaderboard()
    
    def _load_achievements(self) -> List[Dict]:
        """Load achievements from file or use defaults."""
        if os.path.exists(ACHIEVEMENTS_FILE):
            try:
                with open(ACHIEVEMENTS_FILE, 'r') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading achievements: {e}")
        return ACHIEVEMENTS
    
    def _save_achievements(self) -> bool:
        """Save achievements to file."""
        try:
            with open(ACHIEVEMENTS_FILE, 'w') as file:
                json.dump(self.achievements, file, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving achievements: {e}")
            return False
    
    def _load_challenges(self) -> List[Dict]:
        """Load challenges from file or use defaults."""
        if os.path.exists(CHALLENGES_FILE):
            try:
                with open(CHALLENGES_FILE, 'r') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading challenges: {e}")
        return CHALLENGES
    
    def _save_challenges(self) -> bool:
        """Save challenges to file."""
        try:
            with open(CHALLENGES_FILE, 'w') as file:
                json.dump(self.challenges, file, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving challenges: {e}")
            return False
    
    def _load_leaderboard(self) -> Dict:
        """Load leaderboard from file."""
        if os.path.exists(LEADERBOARD_FILE):
            try:
                with open(LEADERBOARD_FILE, 'r') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading leaderboard: {e}")
        
        # Create default leaderboard
        return {
            "distance": {},
            "co2_saved": {},
            "eco_points": {},
            "trips": {},
            "last_updated": datetime.datetime.now().isoformat()
        }
    
    def _save_leaderboard(self) -> bool:
        """Save leaderboard to file."""
        try:
            self.leaderboard["last_updated"] = datetime.datetime.now().isoformat()
            with open(LEADERBOARD_FILE, 'w') as file:
                json.dump(self.leaderboard, file, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving leaderboard: {e}")
            return False
    
    def run_social_features(self):
        """Run the social and gamification features interactive interface."""
        while True:
            ascii_art.clear_screen()
            ascii_art.display_header()
            ascii_art.display_section_header("Social & Gamification")
            
            # Check if user is authenticated
            if not self.user_manager or not self.user_manager.is_authenticated():
                print(f"{ascii_art.Fore.YELLOW}You need to be logged in to access social features.{ascii_art.Style.RESET_ALL}")
                print("\nOptions:")
                print("1. Return to Main Menu")
                
                choice = input("\nSelect an option: ")
                if choice == "1":
                    break
                continue
            
            # Display menu options
            print(f"{ascii_art.Fore.CYAN}Welcome to the EcoCycle Social Hub, {self.user_manager.get_current_user().get('name')}!{ascii_art.Style.RESET_ALL}")
            print("1. View Achievements")
            print("2. View Leaderboard")
            print("3. Active Challenges")
            print("4. Share Stats")
            print("5. Generate Achievement Card")
            print("6. Community Impact Stats")
            print("7. Return to Main Menu")
            
            choice = input("\nSelect an option (1-7): ")
            
            if choice == "1":
                self.view_achievements()
            elif choice == "2":
                self.view_leaderboard()
            elif choice == "3":
                self.view_challenges()
            elif choice == "4":
                self.share_stats()
            elif choice == "5":
                self.generate_achievement_card()
            elif choice == "6":
                self.view_community_impact()
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
    
    def view_achievements(self):
        """View user achievements and progress."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Your Achievements")
        
        user = self.user_manager.get_current_user()
        username = user.get('username')
        
        # Get user stats
        stats = user.get('stats', {})
        total_trips = stats.get('total_trips', 0)
        total_distance = stats.get('total_distance', 0.0)
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        total_calories = stats.get('total_calories', 0)
        
        # Get user achieved achievements
        user_achievements = user.get('achievements', [])
        
        # Calculate eco points
        eco_points = sum(a.get('points', 0) for a in self.achievements if a.get('id') in user_achievements)
        
        # Format user stats for display
        print(f"User: {user.get('name', username)}")
        print(f"Eco Points: {ascii_art.Fore.GREEN}{eco_points}{ascii_art.Style.RESET_ALL}")
        print(f"Level: {self._calculate_level(eco_points)[0]}")
        
        # Display stats
        if TABULATE_AVAILABLE:
            stats_table = [
                ["Total Trips", total_trips],
                ["Total Distance", utils.format_distance(total_distance)],
                ["CO2 Saved", utils.format_co2(total_co2_saved)],
                ["Calories Burned", utils.format_calories(total_calories)]
            ]
            print(f"\n{tabulate(stats_table, headers=['Stat', 'Value'], tablefmt='simple')}")
        else:
            print("\nYour Stats:")
            print(f"Total Trips: {total_trips}")
            print(f"Total Distance: {utils.format_distance(total_distance)}")
            print(f"CO2 Saved: {utils.format_co2(total_co2_saved)}")
            print(f"Calories Burned: {utils.format_calories(total_calories)}")
        
        # Display achievements
        print(f"\n{ascii_art.Fore.CYAN}Achievements Earned:{ascii_art.Style.RESET_ALL}")
        earned_count = 0
        
        for achievement in self.achievements:
            achievement_id = achievement.get('id')
            name = achievement.get('name')
            description = achievement.get('description')
            points = achievement.get('points', 0)
            icon = achievement.get('icon', '🏅')
            requirement = achievement.get('requirement', {})
            
            # Check if user has earned the achievement
            if achievement_id in user_achievements:
                print(f"{ascii_art.Fore.GREEN}✓ {icon} {name} - {description} (+{points} points){ascii_art.Style.RESET_ALL}")
                earned_count += 1
            else:
                # Calculate progress
                progress = 0
                max_value = 0
                
                for req_key, req_value in requirement.items():
                    if req_key == 'total_trips':
                        progress = total_trips
                        max_value = req_value
                    elif req_key == 'total_distance':
                        progress = total_distance
                        max_value = req_value
                    elif req_key == 'total_co2_saved':
                        progress = total_co2_saved
                        max_value = req_value
                    elif req_key == 'total_calories':
                        progress = total_calories
                        max_value = req_value
                
                if max_value > 0:
                    progress_pct = min(100, int((progress / max_value) * 100))
                    print(f"{icon} {name} - {description} (+{points} points)")
                    print(f"   Progress: {progress_pct}% ({progress}/{max_value})")
        
        if earned_count == 0:
            print("No achievements earned yet. Keep cycling to unlock achievements!")
        
        # Show available achievements to earn
        print(f"\n{ascii_art.Fore.CYAN}Next Achievements to Aim For:{ascii_art.Style.RESET_ALL}")
        shown_next = 0
        
        for achievement in self.achievements:
            if achievement.get('id') not in user_achievements:
                if shown_next < 3:  # Only show top 3 next achievements
                    name = achievement.get('name')
                    description = achievement.get('description')
                    points = achievement.get('points', 0)
                    print(f"🎯 {name} - {description} (+{points} points)")
                    shown_next += 1
        
        # Show progress to next level
        current_level, points_for_next = self._calculate_level(eco_points)
        next_level = current_level + 1
        
        if points_for_next > 0:
            print(f"\nPoints needed for Level {next_level}: {points_for_next}")
        
        # Random eco tip
        tip = eco_tips.get_random_tip()
        print(f"\n{ascii_art.Fore.YELLOW}Eco Tip: {tip.get('tip')}{ascii_art.Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")
    
    def view_leaderboard(self):
        """View global leaderboard."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Leaderboard")
        
        # Update leaderboard first
        self._update_leaderboard()
        
        # Sort leaderboard data
        top_distance = sorted(self.leaderboard["distance"].items(), key=lambda x: x[1], reverse=True)[:10]
        top_co2_saved = sorted(self.leaderboard["co2_saved"].items(), key=lambda x: x[1], reverse=True)[:10]
        top_eco_points = sorted(self.leaderboard["eco_points"].items(), key=lambda x: x[1], reverse=True)[:10]
        top_trips = sorted(self.leaderboard["trips"].items(), key=lambda x: x[1], reverse=True)[:10]
        
        current_user = self.user_manager.get_current_user().get('username')
        
        # Display leaderboards
        choice = "1"  # Default
        while choice in ["1", "2", "3", "4"]:
            ascii_art.clear_screen()
            ascii_art.display_header()
            
            if choice == "1":
                # Distance leaderboard
                ascii_art.display_section_header("Distance Leaderboard")
                
                if TABULATE_AVAILABLE:
                    table_data = []
                    for idx, (username, distance) in enumerate(top_distance, 1):
                        is_current = username == current_user
                        username_display = f"{ascii_art.Fore.GREEN}{username}{ascii_art.Style.RESET_ALL}" if is_current else username
                        table_data.append([idx, username_display, utils.format_distance(distance)])
                    print(tabulate(table_data, headers=["Rank", "User", "Distance"], tablefmt="simple"))
                else:
                    for idx, (username, distance) in enumerate(top_distance, 1):
                        is_current = username == current_user
                        username_display = f"{ascii_art.Fore.GREEN}{username}{ascii_art.Style.RESET_ALL}" if is_current else username
                        print(f"{idx}. {username_display}: {utils.format_distance(distance)}")
                
                # Find user's position
                if current_user:
                    full_distance = sorted(self.leaderboard["distance"].items(), key=lambda x: x[1], reverse=True)
                    for idx, (username, _) in enumerate(full_distance, 1):
                        if username == current_user:
                            print(f"\nYour rank: {idx} of {len(full_distance)}")
                            break
            
            elif choice == "2":
                # CO2 saved leaderboard
                ascii_art.display_section_header("CO2 Saved Leaderboard")
                
                if TABULATE_AVAILABLE:
                    table_data = []
                    for idx, (username, co2) in enumerate(top_co2_saved, 1):
                        is_current = username == current_user
                        username_display = f"{ascii_art.Fore.GREEN}{username}{ascii_art.Style.RESET_ALL}" if is_current else username
                        table_data.append([idx, username_display, utils.format_co2(co2)])
                    print(tabulate(table_data, headers=["Rank", "User", "CO2 Saved"], tablefmt="simple"))
                else:
                    for idx, (username, co2) in enumerate(top_co2_saved, 1):
                        is_current = username == current_user
                        username_display = f"{ascii_art.Fore.GREEN}{username}{ascii_art.Style.RESET_ALL}" if is_current else username
                        print(f"{idx}. {username_display}: {utils.format_co2(co2)}")
                
                # Find user's position
                if current_user:
                    full_co2 = sorted(self.leaderboard["co2_saved"].items(), key=lambda x: x[1], reverse=True)
                    for idx, (username, _) in enumerate(full_co2, 1):
                        if username == current_user:
                            print(f"\nYour rank: {idx} of {len(full_co2)}")
                            break
            
            elif choice == "3":
                # Eco points leaderboard
                ascii_art.display_section_header("Eco Points Leaderboard")
                
                if TABULATE_AVAILABLE:
                    table_data = []
                    for idx, (username, points) in enumerate(top_eco_points, 1):
                        is_current = username == current_user
                        username_display = f"{ascii_art.Fore.GREEN}{username}{ascii_art.Style.RESET_ALL}" if is_current else username
                        level, _ = self._calculate_level(points)
                        table_data.append([idx, username_display, points, f"Level {level}"])
                    print(tabulate(table_data, headers=["Rank", "User", "Points", "Level"], tablefmt="simple"))
                else:
                    for idx, (username, points) in enumerate(top_eco_points, 1):
                        is_current = username == current_user
                        username_display = f"{ascii_art.Fore.GREEN}{username}{ascii_art.Style.RESET_ALL}" if is_current else username
                        level, _ = self._calculate_level(points)
                        print(f"{idx}. {username_display}: {points} points (Level {level})")
                
                # Find user's position
                if current_user:
                    full_points = sorted(self.leaderboard["eco_points"].items(), key=lambda x: x[1], reverse=True)
                    for idx, (username, _) in enumerate(full_points, 1):
                        if username == current_user:
                            print(f"\nYour rank: {idx} of {len(full_points)}")
                            break
            
            elif choice == "4":
                # Trips leaderboard
                ascii_art.display_section_header("Most Trips Leaderboard")
                
                if TABULATE_AVAILABLE:
                    table_data = []
                    for idx, (username, trips) in enumerate(top_trips, 1):
                        is_current = username == current_user
                        username_display = f"{ascii_art.Fore.GREEN}{username}{ascii_art.Style.RESET_ALL}" if is_current else username
                        table_data.append([idx, username_display, trips])
                    print(tabulate(table_data, headers=["Rank", "User", "Trips"], tablefmt="simple"))
                else:
                    for idx, (username, trips) in enumerate(top_trips, 1):
                        is_current = username == current_user
                        username_display = f"{ascii_art.Fore.GREEN}{username}{ascii_art.Style.RESET_ALL}" if is_current else username
                        print(f"{idx}. {username_display}: {trips} trips")
                
                # Find user's position
                if current_user:
                    full_trips = sorted(self.leaderboard["trips"].items(), key=lambda x: x[1], reverse=True)
                    for idx, (username, _) in enumerate(full_trips, 1):
                        if username == current_user:
                            print(f"\nYour rank: {idx} of {len(full_trips)}")
                            break
            
            # Show leaderboard options
            print("\nLeaderboard Options:")
            print("1. Distance Leaderboard")
            print("2. CO2 Saved Leaderboard")
            print("3. Eco Points Leaderboard")
            print("4. Most Trips Leaderboard")
            print("5. Return to Social Hub")
            
            choice = input("\nSelect an option (1-5): ")
    
    def view_challenges(self):
        """View and manage active challenges."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Challenges")
        
        user = self.user_manager.get_current_user()
        username = user.get('username')
        
        # Get user's active challenges
        active_challenges = user.get('active_challenges', [])
        completed_challenges = user.get('completed_challenges', [])
        
        # Display active challenges
        if active_challenges:
            print(f"{ascii_art.Fore.CYAN}{ascii_art.Style.BRIGHT}Active Challenges:{ascii_art.Style.RESET_ALL}")
            
            for challenge_id in active_challenges:
                # Find challenge details
                challenge = next((c for c in self.challenges if c.get('id') == challenge_id), None)
                if not challenge:
                    continue
                
                name = challenge.get('name')
                description = challenge.get('description')
                points = challenge.get('points', 0)
                icon = challenge.get('icon', '🏆')
                requirement = challenge.get('requirement', {})
                
                # Get start date and calculate end date
                started_at = user.get('challenge_dates', {}).get(challenge_id, '')
                if started_at:
                    try:
                        started_date = datetime.datetime.fromisoformat(started_at)
                        duration_days = challenge.get('duration', 7)
                        end_date = started_date + datetime.timedelta(days=duration_days)
                        days_left = (end_date - datetime.datetime.now()).days + 1
                        
                        if days_left > 0:
                            date_str = f"{days_left} days left"
                        else:
                            date_str = "Ends today"
                    except ValueError:
                        date_str = "Date unknown"
                else:
                    date_str = "Date unknown"
                
                # Calculate progress
                progress = self._calculate_challenge_progress(username, challenge)
                
                print(f"{icon} {name} - {description} (+{points} points)")
                print(f"   Progress: {progress}% - {date_str}")
        else:
            print("No active challenges.")
        
        # Display completed challenges
        if completed_challenges:
            print(f"\n{ascii_art.Fore.GREEN}{ascii_art.Style.BRIGHT}Completed Challenges:{ascii_art.Style.RESET_ALL}")
            
            for challenge_id in completed_challenges:
                # Find challenge details
                challenge = next((c for c in self.challenges if c.get('id') == challenge_id), None)
                if not challenge:
                    continue
                
                name = challenge.get('name')
                description = challenge.get('description')
                points = challenge.get('points', 0)
                icon = challenge.get('icon', '🏆')
                
                # Get completion date
                completed_at = user.get('challenge_completion_dates', {}).get(challenge_id, '')
                if completed_at:
                    try:
                        completed_date = datetime.datetime.fromisoformat(completed_at)
                        date_str = completed_date.strftime("%Y-%m-%d")
                    except ValueError:
                        date_str = "Date unknown"
                else:
                    date_str = "Date unknown"
                
                print(f"{icon} {name} - {description} (+{points} points)")
                print(f"   Completed on: {date_str}")
        
        # Available challenges to join
        print(f"\n{ascii_art.Fore.YELLOW}{ascii_art.Style.BRIGHT}Available Challenges:{ascii_art.Style.RESET_ALL}")
        available_challenges = [c for c in self.challenges 
                              if c.get('id') not in active_challenges 
                              and c.get('id') not in completed_challenges]
        
        if available_challenges:
            for i, challenge in enumerate(available_challenges, 1):
                name = challenge.get('name')
                description = challenge.get('description')
                points = challenge.get('points', 0)
                icon = challenge.get('icon', '🏆')
                duration = challenge.get('duration', 7)
                
                print(f"{i}. {icon} {name} - {description} (+{points} points)")
                print(f"   Duration: {duration} days")
        else:
            print("No available challenges at the moment. Check back later!")
        
        # Challenge options
        print("\nOptions:")
        print("1. Join a Challenge")
        print("2. Abandon an Active Challenge")
        print("3. Return to Social Hub")
        
        choice = input("\nSelect an option (1-3): ")
        
        if choice == "1" and available_challenges:
            # Join a challenge
            challenge_num = input(f"Enter challenge number to join (1-{len(available_challenges)}): ")
            try:
                idx = int(challenge_num) - 1
                if 0 <= idx < len(available_challenges):
                    challenge = available_challenges[idx]
                    challenge_id = challenge.get('id')
                    
                    # Add to active challenges
                    if 'active_challenges' not in user:
                        user['active_challenges'] = []
                    user['active_challenges'].append(challenge_id)
                    
                    # Record start date
                    if 'challenge_dates' not in user:
                        user['challenge_dates'] = {}
                    user['challenge_dates'][challenge_id] = datetime.datetime.now().isoformat()
                    
                    # Save user data
                    if self.user_manager.save_users():
                        print(f"You've joined the '{challenge.get('name')}' challenge!")
                    else:
                        print("Error saving challenge data.")
                else:
                    print("Invalid challenge number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        elif choice == "2" and active_challenges:
            # Abandon a challenge
            print("\nActive Challenges:")
            for i, challenge_id in enumerate(active_challenges, 1):
                challenge = next((c for c in self.challenges if c.get('id') == challenge_id), None)
                if challenge:
                    print(f"{i}. {challenge.get('name')}")
            
            challenge_num = input(f"Enter challenge number to abandon (1-{len(active_challenges)}): ")
            try:
                idx = int(challenge_num) - 1
                if 0 <= idx < len(active_challenges):
                    challenge_id = active_challenges[idx]
                    challenge = next((c for c in self.challenges if c.get('id') == challenge_id), None)
                    
                    # Remove from active challenges
                    user['active_challenges'].remove(challenge_id)
                    
                    # Remove start date
                    if 'challenge_dates' in user and challenge_id in user['challenge_dates']:
                        del user['challenge_dates'][challenge_id]
                    
                    # Save user data
                    if self.user_manager.save_users():
                        print(f"You've abandoned the '{challenge.get('name')}' challenge.")
                    else:
                        print("Error saving challenge data.")
                else:
                    print("Invalid challenge number.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number.")
        
        input("\nPress Enter to continue...")
    
    def share_stats(self):
        """Share cycling stats on social media or via export."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Share Your Stats")
        
        user = self.user_manager.get_current_user()
        
        # Get user stats
        stats = user.get('stats', {})
        total_trips = stats.get('total_trips', 0)
        total_distance = stats.get('total_distance', 0.0)
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        total_calories = stats.get('total_calories', 0)
        
        # Format user stats for sharing
        share_text = f"I've cycled {utils.format_distance(total_distance)} with EcoCycle!\n"
        share_text += f"🌍 Saved {utils.format_co2(total_co2_saved)} of CO2 emissions\n"
        share_text += f"🔥 Burned {utils.format_calories(total_calories)}\n"
        share_text += f"🚴 Completed {total_trips} cycling trips\n"
        share_text += "\n#EcoCycle #SustainableMobility #CyclingLife"
        
        # Display share text
        print("Here's what we'll share:")
        print("-" * 50)
        print(share_text)
        print("-" * 50)
        
        # Sharing options
        print("\nHow would you like to share?")
        print("1. Generate Shareable Image")
        print("2. Generate QR Code")
        print("3. Copy Text to Clipboard")
        print("4. Return to Social Hub")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == "1":
            # Generate shareable image
            if not PIL_AVAILABLE:
                print("The PIL/Pillow library is required for generating images.")
                print("Please install it with: pip install pillow")
                input("\nPress Enter to continue...")
                return
            
            print("\nGenerating shareable image...")
            image_path = self._generate_share_image(user)
            
            if image_path:
                print(f"Image saved to: {image_path}")
                
                print("\nOptions:")
                print("1. Open image")
                print("2. Return to Social Hub")
                
                open_choice = input("\nSelect an option (1-2): ")
                if open_choice == "1":
                    try:
                        if os.path.exists(image_path):
                            webbrowser.open(f"file://{os.path.abspath(image_path)}")
                        else:
                            print("Error: Image file not found.")
                    except Exception as e:
                        logger.error(f"Error opening image: {e}")
                        print(f"Error opening image: {str(e)}")
            else:
                print("Error generating image.")
        
        elif choice == "2":
            # Generate QR code
            if not QRCODE_AVAILABLE:
                print("The qrcode library is required for generating QR codes.")
                print("Please install it with: pip install qrcode[pil]")
                input("\nPress Enter to continue...")
                return
            
            print("\nGenerating QR code...")
            
            try:
                # Create a QR code containing the share text
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(share_text)
                qr.make(fit=True)
                
                # Create an image from the QR Code
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Save the image
                filename = f"ecocycle_qr_{int(time.time())}.png"
                img.save(filename)
                
                print(f"QR code saved to: {filename}")
                
                print("\nOptions:")
                print("1. Open QR code")
                print("2. Return to Social Hub")
                
                open_choice = input("\nSelect an option (1-2): ")
                if open_choice == "1":
                    try:
                        if os.path.exists(filename):
                            webbrowser.open(f"file://{os.path.abspath(filename)}")
                        else:
                            print("Error: QR code file not found.")
                    except Exception as e:
                        logger.error(f"Error opening QR code: {e}")
                        print(f"Error opening QR code: {str(e)}")
            
            except Exception as e:
                logger.error(f"Error generating QR code: {e}")
                print(f"Error generating QR code: {str(e)}")
        
        elif choice == "3":
            # Copy text to clipboard
            # In a real app, we'd use pyperclip or similar for this, 
            # but for now we'll just display the text for copying
            print("\nCopy the following text to share:")
            print("-" * 50)
            print(share_text)
            print("-" * 50)
            
            print("\nText is ready to be copied manually.")
        
        input("\nPress Enter to continue...")
    
    def _generate_share_image(self, user):
        """Generate a shareable image with user stats."""
        try:
            # Get user data
            username = user.get('username')
            name = user.get('name', username)
            stats = user.get('stats', {})
            total_trips = stats.get('total_trips', 0)
            total_distance = stats.get('total_distance', 0.0)
            total_co2_saved = stats.get('total_co2_saved', 0.0)
            total_calories = stats.get('total_calories', 0)
            
            # Create a new image
            width, height = 1000, 600
            image = Image.new('RGB', (width, height), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            # Draw background
            draw.rectangle([(0, 0), (1000, 120)], fill=(76, 175, 80))  # Green header
            
            # Try to load fonts (if available)
            try:
                # On different systems, fonts may be in different locations
                # Try a few common fonts
                title_font = ImageFont.truetype("Arial Bold.ttf", 36)
            except IOError:
                try:
                    title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
                except IOError:
                    title_font = ImageFont.load_default()
            
            try:
                subtitle_font = ImageFont.truetype("Arial.ttf", 24)
            except IOError:
                try:
                    subtitle_font = ImageFont.truetype("DejaVuSans.ttf", 24)
                except IOError:
                    subtitle_font = ImageFont.load_default()
            
            try:
                stats_font = ImageFont.truetype("Arial Bold.ttf", 48)
            except IOError:
                try:
                    stats_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
                except IOError:
                    stats_font = ImageFont.load_default()
            
            try:
                label_font = ImageFont.truetype("Arial.ttf", 20)
            except IOError:
                try:
                    label_font = ImageFont.truetype("DejaVuSans.ttf", 20)
                except IOError:
                    label_font = ImageFont.load_default()
            
            # Draw title
            draw.text((20, 25), "EcoCycle Stats", fill=(255, 255, 255), font=title_font)
            draw.text((20, 75), f"Cycling achievements for {name}", fill=(255, 255, 255), font=subtitle_font)
            
            # Draw stats section
            stats_y = 150
            icon_size = 50
            
            # Distance
            draw.text((60, stats_y), "🚲", fill=(76, 175, 80), font=stats_font)
            draw.text((120, stats_y), utils.format_distance(total_distance), fill=(0, 0, 0), font=stats_font)
            draw.text((120, stats_y + 60), "Distance Cycled", fill=(100, 100, 100), font=label_font)
            
            # CO2 Saved
            stats_y += 120
            draw.text((60, stats_y), "🌍", fill=(76, 175, 80), font=stats_font)
            draw.text((120, stats_y), utils.format_co2(total_co2_saved), fill=(0, 0, 0), font=stats_font)
            draw.text((120, stats_y + 60), "CO2 Emissions Saved", fill=(100, 100, 100), font=label_font)
            
            # Calories
            stats_y += 120
            draw.text((60, stats_y), "🔥", fill=(76, 175, 80), font=stats_font)
            draw.text((120, stats_y), utils.format_calories(total_calories), fill=(0, 0, 0), font=stats_font)
            draw.text((120, stats_y + 60), "Calories Burned", fill=(100, 100, 100), font=label_font)
            
            # Trips
            stats_y += 120
            draw.text((60, stats_y), "🚴", fill=(76, 175, 80), font=stats_font)
            draw.text((120, stats_y), str(total_trips), fill=(0, 0, 0), font=stats_font)
            draw.text((120, stats_y + 60), "Cycling Trips", fill=(100, 100, 100), font=label_font)
            
            # Date
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            draw.text((width - 200, height - 40), f"Generated: {current_date}", fill=(150, 150, 150), font=label_font)
            
            # Save the image
            filename = f"ecocycle_stats_{username}_{int(time.time())}.png"
            image.save(filename)
            
            return filename
        
        except Exception as e:
            logger.error(f"Error generating share image: {e}")
            return None
    
    def generate_achievement_card(self):
        """Generate an achievement card for sharing."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Achievement Card")
        
        if not PIL_AVAILABLE:
            print("The PIL/Pillow library is required for generating achievement cards.")
            print("Please install it with: pip install pillow")
            input("\nPress Enter to continue...")
            return
        
        user = self.user_manager.get_current_user()
        username = user.get('username')
        
        # Get user achievements
        user_achievements = user.get('achievements', [])
        
        if not user_achievements:
            print("You haven't earned any achievements yet.")
            print("Keep cycling to unlock achievements that you can showcase!")
            input("\nPress Enter to continue...")
            return
        
        # Get user stats and eco points
        stats = user.get('stats', {})
        total_trips = stats.get('total_trips', 0)
        total_distance = stats.get('total_distance', 0.0)
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        
        eco_points = sum(a.get('points', 0) for a in self.achievements if a.get('id') in user_achievements)
        level, _ = self._calculate_level(eco_points)
        
        # Display achievements
        print(f"{ascii_art.Fore.CYAN}Your Achievements:{ascii_art.Style.RESET_ALL}")
        achievements_data = []
        
        for idx, achievement_id in enumerate(user_achievements, 1):
            achievement = next((a for a in self.achievements if a.get('id') == achievement_id), {})
            name = achievement.get('name', 'Unknown')
            description = achievement.get('description', 'No description')
            points = achievement.get('points', 0)
            icon = achievement.get('icon', '🏅')
            
            achievements_data.append({
                'idx': idx,
                'id': achievement_id,
                'name': name,
                'description': description,
                'points': points,
                'icon': icon
            })
            
            print(f"{idx}. {icon} {name} - {description} (+{points} points)")
        
        # Let user choose which achievement to feature
        print("\nSelect an achievement to feature on your card:")
        achievement_num = input(f"Enter achievement number (1-{len(achievements_data)}): ")
        
        try:
            idx = int(achievement_num) - 1
            if 0 <= idx < len(achievements_data):
                achievement = achievements_data[idx]
                
                print(f"\nGenerating achievement card for: {achievement['name']}...")
                
                if TQDM_AVAILABLE:
                    # Use tqdm to show a progress bar
                    for _ in tqdm(range(10), desc="Generating"):
                        time.sleep(0.1)
                else:
                    print("Generating...")
                    time.sleep(1)
                
                # Generate the image
                try:
                    # Create a new image
                    width, height = 1000, 600
                    image = Image.new('RGB', (width, height), color=(245, 245, 245))
                    draw = ImageDraw.Draw(image)
                    
                    # Draw background and border
                    draw.rectangle([(0, 0), (width, height)], fill=(245, 245, 245))
                    draw.rectangle([(20, 20), (width-20, height-20)], outline=(76, 175, 80), width=5)
                    
                    # Try to load fonts (if available)
                    try:
                        title_font = ImageFont.truetype("Arial Bold.ttf", 40)
                    except IOError:
                        try:
                            title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
                        except IOError:
                            title_font = ImageFont.load_default()
                    
                    try:
                        subtitle_font = ImageFont.truetype("Arial.ttf", 28)
                    except IOError:
                        try:
                            subtitle_font = ImageFont.truetype("DejaVuSans.ttf", 28)
                        except IOError:
                            subtitle_font = ImageFont.load_default()
                    
                    try:
                        achievement_font = ImageFont.truetype("Arial Bold.ttf", 56)
                    except IOError:
                        try:
                            achievement_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 56)
                        except IOError:
                            achievement_font = ImageFont.load_default()
                    
                    try:
                        stats_font = ImageFont.truetype("Arial.ttf", 24)
                    except IOError:
                        try:
                            stats_font = ImageFont.truetype("DejaVuSans.ttf", 24)
                        except IOError:
                            stats_font = ImageFont.load_default()
                    
                    # Draw title
                    draw.text((50, 50), "EcoCycle Achievement", fill=(76, 175, 80), font=title_font)
                    
                    # Draw user info
                    draw.text((50, 110), f"Cyclist: {user.get('name', username)}", fill=(100, 100, 100), font=subtitle_font)
                    draw.text((50, 150), f"Level {level} • {eco_points} Eco Points", fill=(76, 175, 80), font=subtitle_font)
                    
                    # Draw achievement
                    icon_text = achievement['icon']
                    draw.text((width/2 - 150, 220), icon_text, fill=(76, 175, 80), font=achievement_font)
                    draw.text((width/2 - 80, 230), achievement['name'], fill=(50, 50, 50), font=achievement_font)
                    
                    # Draw description
                    draw.text((width/2 - len(achievement['description'])*6, 310), achievement['description'], fill=(100, 100, 100), font=subtitle_font)
                    
                    # Draw stats
                    stats_y = 380
                    draw.text((50, stats_y), f"🚲 Total Distance: {utils.format_distance(total_distance)}", fill=(50, 50, 50), font=stats_font)
                    draw.text((50, stats_y + 40), f"🌍 CO2 Saved: {utils.format_co2(total_co2_saved)}", fill=(50, 50, 50), font=stats_font)
                    draw.text((50, stats_y + 80), f"🚴 Trips Completed: {total_trips}", fill=(50, 50, 50), font=stats_font)
                    
                    # Draw promotional text
                    draw.text((width/2 - 160, height - 70), "Join me in cycling for a greener planet!", fill=(76, 175, 80), font=subtitle_font)
                    
                    # Generate filename and save
                    filename = f"ecocycle_achievement_{username}_{achievement['id']}_{int(time.time())}.png"
                    image.save(filename)
                    
                    print(f"Achievement card saved to: {filename}")
                    
                    # Ask if they want to open the image
                    print("\nOptions:")
                    print("1. Open image")
                    print("2. Return to Social Hub")
                    
                    open_choice = input("\nSelect an option (1-2): ")
                    if open_choice == "1":
                        try:
                            if os.path.exists(filename):
                                webbrowser.open(f"file://{os.path.abspath(filename)}")
                            else:
                                print("Error: Image file not found.")
                        except Exception as e:
                            logger.error(f"Error opening image: {e}")
                            print(f"Error opening image: {str(e)}")
                
                except Exception as e:
                    logger.error(f"Error generating achievement card: {e}")
                    print(f"Error generating achievement card: {str(e)}")
            else:
                print("Invalid achievement number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        
        input("\nPress Enter to continue...")
    
    def view_community_impact(self):
        """View the community's collective environmental impact."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Community Impact")
        
        # Update leaderboard to ensure we have the latest stats
        self._update_leaderboard()
        
        # Calculate community totals
        total_distance = sum(self.leaderboard.get("distance", {}).values())
        total_co2_saved = sum(self.leaderboard.get("co2_saved", {}).values())
        total_trips = sum(self.leaderboard.get("trips", {}).values())
        
        # Determine average stats
        num_users = len(self.leaderboard.get("distance", {}))
        if num_users > 0:
            avg_distance = total_distance / num_users
            avg_co2_saved = total_co2_saved / num_users
            avg_trips = total_trips / num_users
        else:
            avg_distance = 0
            avg_co2_saved = 0
            avg_trips = 0
        
        # Calculate real-world equivalents
        trees_required = total_co2_saved / 20  # One tree absorbs about 20kg CO2 per year
        car_distance = total_co2_saved / 0.13  # Average car emits about 130g CO2 per km
        
        # Display community totals
        print(f"{ascii_art.Fore.GREEN}{ascii_art.Style.BRIGHT}Community Totals:{ascii_art.Style.RESET_ALL}")
        
        if TABULATE_AVAILABLE:
            totals_table = [
                ["Total Distance", utils.format_distance(total_distance)],
                ["Total CO2 Saved", utils.format_co2(total_co2_saved)],
                ["Total Trips", total_trips]
            ]
            print(tabulate(totals_table, headers=['Metric', 'Value'], tablefmt='simple'))
        else:
            print(f"Total Distance: {utils.format_distance(total_distance)}")
            print(f"Total CO2 Saved: {utils.format_co2(total_co2_saved)}")
            print(f"Total Trips: {total_trips}")
        
        # Display averages
        print(f"\n{ascii_art.Fore.CYAN}{ascii_art.Style.BRIGHT}User Averages:{ascii_art.Style.RESET_ALL}")
        
        if TABULATE_AVAILABLE:
            avg_table = [
                ["Average Distance", utils.format_distance(avg_distance)],
                ["Average CO2 Saved", utils.format_co2(avg_co2_saved)],
                ["Average Trips", f"{avg_trips:.1f}"]
            ]
            print(tabulate(avg_table, headers=['Metric', 'Value'], tablefmt='simple'))
        else:
            print(f"Average Distance: {utils.format_distance(avg_distance)}")
            print(f"Average CO2 Saved: {utils.format_co2(avg_co2_saved)}")
            print(f"Average Trips: {avg_trips:.1f}")
        
        # Display environmental impact
        print(f"\n{ascii_art.Fore.GREEN}{ascii_art.Style.BRIGHT}Environmental Impact:{ascii_art.Style.RESET_ALL}")
        print(f"The CO2 saved is equivalent to:")
        print(f"- The annual CO2 absorption of {trees_required:.1f} trees")
        print(f"- Emissions from driving {car_distance:.1f} km in an average car")
        print(f"- {(total_co2_saved / 5):.1f} flights from London to Paris")
        
        # Show community achievements
        print(f"\n{ascii_art.Fore.YELLOW}{ascii_art.Style.BRIGHT}Community Achievements:{ascii_art.Style.RESET_ALL}")
        
        # Define community milestones
        milestones = [
            {"name": "First Steps", "description": "Community's first 100km cycled", "threshold": 100, "metric": "distance"},
            {"name": "Growing Movement", "description": "Community reaches 500km total distance", "threshold": 500, "metric": "distance"},
            {"name": "Distance Milestone", "description": "Community reaches 1,000km total distance", "threshold": 1000, "metric": "distance"},
            {"name": "Climate Action", "description": "Community saves 100kg of CO2", "threshold": 100, "metric": "co2_saved"},
            {"name": "Major Impact", "description": "Community saves 500kg of CO2", "threshold": 500, "metric": "co2_saved"},
            {"name": "Carbon Crusher", "description": "Community saves 1,000kg of CO2", "threshold": 1000, "metric": "co2_saved"},
            {"name": "Active Community", "description": "Community completes 100 cycling trips", "threshold": 100, "metric": "trips"},
            {"name": "Dedicated Community", "description": "Community completes 500 cycling trips", "threshold": 500, "metric": "trips"},
        ]
        
        # Check which milestones have been achieved
        achieved_milestones = []
        upcoming_milestones = []
        
        for milestone in milestones:
            if milestone["metric"] == "distance" and total_distance >= milestone["threshold"]:
                achieved_milestones.append(milestone)
            elif milestone["metric"] == "co2_saved" and total_co2_saved >= milestone["threshold"]:
                achieved_milestones.append(milestone)
            elif milestone["metric"] == "trips" and total_trips >= milestone["threshold"]:
                achieved_milestones.append(milestone)
            else:
                # Calculate progress
                if milestone["metric"] == "distance":
                    progress = (total_distance / milestone["threshold"]) * 100
                    upcoming_milestones.append((milestone, progress))
                elif milestone["metric"] == "co2_saved":
                    progress = (total_co2_saved / milestone["threshold"]) * 100
                    upcoming_milestones.append((milestone, progress))
                elif milestone["metric"] == "trips":
                    progress = (total_trips / milestone["threshold"]) * 100
                    upcoming_milestones.append((milestone, progress))
        
        # Display achieved milestones
        if achieved_milestones:
            for milestone in achieved_milestones:
                print(f"✅ {milestone['name']}: {milestone['description']}")
        else:
            print("No community milestones achieved yet.")
        
        # Display upcoming milestones
        if upcoming_milestones:
            # Sort by progress (descending)
            upcoming_milestones.sort(key=lambda x: x[1], reverse=True)
            
            print(f"\n{ascii_art.Fore.CYAN}{ascii_art.Style.BRIGHT}Next Milestones:{ascii_art.Style.RESET_ALL}")
            
            # Show top 3 upcoming milestones
            for milestone, progress in upcoming_milestones[:3]:
                print(f"🔜 {milestone['name']}: {milestone['description']}")
                print(f"   Progress: {progress:.1f}%")
        
        # Display last update time
        last_updated = self.leaderboard.get("last_updated", "Unknown")
        if isinstance(last_updated, str) and re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', last_updated):
            try:
                update_time = datetime.datetime.fromisoformat(last_updated)
                update_str = update_time.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                update_str = last_updated
        else:
            update_str = last_updated
        
        print(f"\nLast updated: {update_str}")
        
        input("\nPress Enter to continue...")
    
    def _update_leaderboard(self) -> None:
        """Update the leaderboard with current user data."""
        if not self.user_manager:
            return
        
        # Get all users
        users = self.user_manager.users
        
        # Clear leaderboard data
        self.leaderboard["distance"] = {}
        self.leaderboard["co2_saved"] = {}
        self.leaderboard["eco_points"] = {}
        self.leaderboard["trips"] = {}
        
        # Iterate through users and update stats
        for username, user_data in users.items():
            # Skip guest user
            if user_data.get('is_guest', False):
                continue
            
            # Get user stats
            stats = user_data.get('stats', {})
            
            # Update distance leaderboard
            total_distance = stats.get('total_distance', 0.0)
            self.leaderboard["distance"][username] = total_distance
            
            # Update CO2 saved leaderboard
            total_co2_saved = stats.get('total_co2_saved', 0.0)
            self.leaderboard["co2_saved"][username] = total_co2_saved
            
            # Update trips leaderboard
            total_trips = stats.get('total_trips', 0)
            self.leaderboard["trips"][username] = total_trips
            
            # Update eco points leaderboard
            user_achievements = user_data.get('achievements', [])
            eco_points = sum(a.get('points', 0) for a in self.achievements if a.get('id') in user_achievements)
            self.leaderboard["eco_points"][username] = eco_points
        
        # Save leaderboard
        self._save_leaderboard()
    
    def check_achievements(self, username: str) -> List[Dict]:
        """
        Check if a user has earned any new achievements.
        
        Args:
            username (str): Username to check
            
        Returns:
            list: List of newly earned achievements
        """
        if not self.user_manager:
            return []
        
        # Get user data
        if username not in self.user_manager.users:
            return []
        
        user = self.user_manager.users[username]
        stats = user.get('stats', {})
        
        # Get current achievements
        current_achievements = user.get('achievements', [])
        
        # Get stats
        total_trips = stats.get('total_trips', 0)
        total_distance = stats.get('total_distance', 0.0)
        total_co2_saved = stats.get('total_co2_saved', 0.0)
        total_calories = stats.get('total_calories', 0)
        
        # Check for new achievements
        new_achievements = []
        
        for achievement in self.achievements:
            achievement_id = achievement.get('id')
            
            # Skip if already earned
            if achievement_id in current_achievements:
                continue
            
            # Check requirements
            requirement = achievement.get('requirement', {})
            achieved = True
            
            for req_key, req_value in requirement.items():
                if req_key == 'total_trips' and total_trips < req_value:
                    achieved = False
                elif req_key == 'total_distance' and total_distance < req_value:
                    achieved = False
                elif req_key == 'total_co2_saved' and total_co2_saved < req_value:
                    achieved = False
                elif req_key == 'total_calories' and total_calories < req_value:
                    achieved = False
            
            if achieved:
                # Add to new achievements
                new_achievements.append(achievement)
                
                # Add to user's achievements
                if 'achievements' not in user:
                    user['achievements'] = []
                
                user['achievements'].append(achievement_id)
        
        # Save if any new achievements
        if new_achievements and self.user_manager.save_users():
            return new_achievements
        
        return []
    
    def check_challenge_progress(self, username: str) -> List[Dict]:
        """
        Check if a user has completed any active challenges.
        
        Args:
            username (str): Username to check
            
        Returns:
            list: List of completed challenges
        """
        if not self.user_manager:
            return []
        
        # Get user data
        if username not in self.user_manager.users:
            return []
        
        user = self.user_manager.users[username]
        active_challenges = user.get('active_challenges', [])
        
        # No active challenges
        if not active_challenges:
            return []
        
        # Check each challenge
        completed_challenges = []
        
        for challenge_id in list(active_challenges):  # Copy list to avoid modification issues during iteration
            # Find challenge details
            challenge = next((c for c in self.challenges if c.get('id') == challenge_id), None)
            if not challenge:
                continue
            
            # Check if challenge has ended
            start_date_str = user.get('challenge_dates', {}).get(challenge_id)
            if not start_date_str:
                continue
            
            try:
                start_date = datetime.datetime.fromisoformat(start_date_str)
                duration_days = challenge.get('duration', 7)
                end_date = start_date + datetime.timedelta(days=duration_days)
                
                # If challenge has ended, check if it was completed
                if datetime.datetime.now() > end_date:
                    progress = self._calculate_challenge_progress(username, challenge)
                    
                    if progress >= 100:
                        # Challenge completed
                        completed_challenges.append(challenge)
                        
                        # Move to completed challenges
                        if 'completed_challenges' not in user:
                            user['completed_challenges'] = []
                        
                        if challenge_id not in user['completed_challenges']:
                            user['completed_challenges'].append(challenge_id)
                        
                        # Record completion date
                        if 'challenge_completion_dates' not in user:
                            user['challenge_completion_dates'] = {}
                        
                        user['challenge_completion_dates'][challenge_id] = datetime.datetime.now().isoformat()
                        
                        # Award eco points
                        points = challenge.get('points', 0)
                        if 'challenge_points' not in user:
                            user['challenge_points'] = 0
                        
                        user['challenge_points'] += points
                    
                    # Remove from active challenges
                    active_challenges.remove(challenge_id)
                    user['active_challenges'] = active_challenges
            
            except (ValueError, TypeError) as e:
                logger.error(f"Error checking challenge dates: {e}")
                continue
        
        # Save if any changes
        if completed_challenges:
            self.user_manager.save_users()
        
        return completed_challenges
    
    def _calculate_challenge_progress(self, username: str, challenge: Dict) -> float:
        """
        Calculate a user's progress on a challenge.
        
        Args:
            username (str): Username
            challenge (dict): Challenge details
            
        Returns:
            float: Progress percentage (0-100)
        """
        if not self.user_manager or username not in self.user_manager.users:
            return 0
        
        user = self.user_manager.users[username]
        stats = user.get('stats', {})
        trips = stats.get('trips', [])
        
        requirement = challenge.get('requirement', {})
        challenge_id = challenge.get('id')
        
        # Get challenge start date
        start_date_str = user.get('challenge_dates', {}).get(challenge_id)
        if not start_date_str:
            return 0
        
        try:
            start_date = datetime.datetime.fromisoformat(start_date_str)
            duration_days = challenge.get('duration', 7)
            end_date = start_date + datetime.timedelta(days=duration_days)
            
            # Filter trips within challenge period
            challenge_trips = []
            for trip in trips:
                trip_date_str = trip.get('date')
                if not trip_date_str:
                    continue
                
                try:
                    trip_date = datetime.datetime.fromisoformat(trip_date_str)
                    if start_date <= trip_date <= end_date:
                        challenge_trips.append(trip)
                except ValueError:
                    continue
            
            # Calculate progress based on requirement type
            for req_key, req_value in requirement.items():
                if req_key == 'weekly_distance':
                    # Calculate total distance in challenge period
                    total_distance = sum(trip.get('distance', 0) for trip in challenge_trips)
                    return min(100, (total_distance / req_value) * 100)
                
                elif req_key == 'weekly_co2_saved':
                    # Calculate total CO2 saved in challenge period
                    total_co2 = sum(trip.get('co2_saved', 0) for trip in challenge_trips)
                    return min(100, (total_co2 / req_value) * 100)
                
                elif req_key == 'weekly_trips':
                    # Count trips in challenge period
                    trip_count = len(challenge_trips)
                    return min(100, (trip_count / req_value) * 100)
                
                elif req_key == 'monthly_trips':
                    # Count trips in challenge period
                    trip_count = len(challenge_trips)
                    return min(100, (trip_count / req_value) * 100)
            
            return 0
        
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating challenge progress: {e}")
            return 0
    
    def _calculate_level(self, points: int) -> Tuple[int, int]:
        """
        Calculate user level based on eco points.
        
        Args:
            points (int): Eco points
            
        Returns:
            tuple: (current_level, points_needed_for_next_level)
        """
        # Level thresholds
        level_thresholds = [0, 50, 125, 225, 350, 500, 700, 950, 1250, 1600, 2000]
        
        # Find current level
        current_level = 1
        for i, threshold in enumerate(level_thresholds):
            if points >= threshold:
                current_level = i + 1
            else:
                break
        
        # Calculate points needed for next level
        if current_level < len(level_thresholds):
            next_threshold = level_thresholds[current_level]
            points_needed = next_threshold - points
        else:
            # At max level
            points_needed = 0
        
        return current_level, points_needed


def run_social_features(user_manager_instance=None, sheets_manager_instance=None):
    """
    Run the social gamification features as a standalone module.
    
    Args:
        user_manager_instance: Optional user manager
        sheets_manager_instance: Optional sheets manager
    """
    social = SocialGamification(user_manager_instance, sheets_manager_instance)
    social.run_social_features()


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run social features
    run_social_features()