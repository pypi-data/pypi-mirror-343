"""
EcoCycle - Weather and Route Planner Module
Provides functionality for checking weather conditions and planning cycling routes.
"""
import os
import json
import time
import logging
import re
import webbrowser
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

# Import utilities
import utils
import ascii_art

logger = logging.getLogger(__name__)

# Constants
WEATHER_CACHE_EXPIRY = 60 * 60  # 1 hour in seconds
DEFAULT_COORDINATES = {
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "Chicago": (41.8781, -87.6298),
    "London": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050),
    "Tokyo": (35.6762, 139.6503),
    "Sydney": (-33.8688, 151.2093),
    "Rio de Janeiro": (-22.9068, -43.1729),
    "Cairo": (30.0444, 31.2357)
}
WEATHER_CACHE_FILE = "weather_cache.json"
ROUTES_CACHE_FILE = "routes_cache.json"
OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "")
MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN", "")


class WeatherRoutePlanner:
    """
    Weather and route planner for cyclists.
    Provides functionality to check weather conditions and plan cycling routes.
    """
    
    def __init__(self, user_manager=None):
        """Initialize the weather and route planner."""
        self.user_manager = user_manager
        self.weather_cache = self._load_cache(WEATHER_CACHE_FILE)
        self.routes_cache = self._load_cache(ROUTES_CACHE_FILE)
    
    def _load_cache(self, cache_file: str) -> Dict:
        """Load cache from file."""
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading cache from {cache_file}: {e}")
        return {}
    
    def _save_cache(self, cache_data: Dict, cache_file: str) -> bool:
        """Save cache to file."""
        try:
            with open(cache_file, 'w') as file:
                json.dump(cache_data, file, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving cache to {cache_file}: {e}")
            return False
    
    def _is_cache_valid(self, cache_key: str, cache_data: Dict) -> bool:
        """Check if cached data is still valid (not expired)."""
        if cache_key not in cache_data:
            return False
        
        cached_time = cache_data[cache_key].get("timestamp", 0)
        current_time = time.time()
        
        return current_time - cached_time < WEATHER_CACHE_EXPIRY
    
    def run_planner(self, user_manager_instance=None):
        """Run the weather and route planner interactive interface."""
        if user_manager_instance:
            self.user_manager = user_manager_instance
        
        while True:
            ascii_art.clear_screen()
            ascii_art.display_header()
            ascii_art.display_section_header("Weather and Route Planner")
            
            # Display menu options
            print("1. Check Weather Forecast")
            print("2. Plan Cycling Route")
            print("3. View Saved Routes")
            print("4. Cycling Impact Calculator")
            print("5. Return to Main Menu")
            
            choice = input("\nSelect an option (1-5): ")
            
            if choice == "1":
                self.check_weather()
            elif choice == "2":
                self.plan_route()
            elif choice == "3":
                self.view_saved_routes()
            elif choice == "4":
                self.cycling_impact_calculator()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
    
    def check_weather(self):
        """Check weather forecast for cycling."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Weather Forecast")
        
        if not REQUESTS_AVAILABLE:
            print("The requests library is required for weather forecast functionality.")
            print("Please install it with: pip install requests")
            input("\nPress Enter to continue...")
            return
        
        # Get location
        print("Enter location (city name or 'current' for current location):")
        location = input("> ")
        
        if location.lower() == "current":
            # Try to get current location via IP
            try:
                ip_info = requests.get("https://ipinfo.io/json").json()
                coordinates = ip_info.get("loc", "").split(",")
                if len(coordinates) == 2:
                    lat, lon = float(coordinates[0]), float(coordinates[1])
                    print(f"Location detected: {ip_info.get('city', 'Unknown')}, {ip_info.get('region', '')}")
                else:
                    print("Could not determine your location. Using New York as default.")
                    lat, lon = DEFAULT_COORDINATES["New York"]
            except Exception as e:
                logger.error(f"Error getting location: {e}")
                print("Could not determine your location. Using New York as default.")
                lat, lon = DEFAULT_COORDINATES["New York"]
        else:
            # Try to get coordinates for the city name
            if location in DEFAULT_COORDINATES:
                lat, lon = DEFAULT_COORDINATES[location]
            else:
                # Use OpenWeatherMap Geocoding API
                if not OPENWEATHERMAP_API_KEY:
                    print("OpenWeatherMap API key not set. Using New York as default.")
                    lat, lon = DEFAULT_COORDINATES["New York"]
                else:
                    try:
                        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={OPENWEATHERMAP_API_KEY}"
                        geo_response = requests.get(geo_url)
                        geo_data = geo_response.json()
                        
                        if geo_data and len(geo_data) > 0:
                            lat = geo_data[0]["lat"]
                            lon = geo_data[0]["lon"]
                            print(f"Location found: {geo_data[0].get('name', location)}, {geo_data[0].get('country', '')}")
                        else:
                            print(f"Could not find coordinates for {location}. Using New York as default.")
                            lat, lon = DEFAULT_COORDINATES["New York"]
                    except Exception as e:
                        logger.error(f"Error getting coordinates: {e}")
                        print(f"Error finding location: {str(e)}")
                        print("Using New York as default.")
                        lat, lon = DEFAULT_COORDINATES["New York"]
        
        # Check cache for weather data
        cache_key = f"{lat},{lon}"
        if self._is_cache_valid(cache_key, self.weather_cache):
            weather_data = self.weather_cache[cache_key]["data"]
            print("\nRetrieved weather from cache.")
        else:
            # Get weather data from API
            if not OPENWEATHERMAP_API_KEY:
                print("OpenWeatherMap API key not set. Please set it in your environment variables.")
                print("Example: export OPENWEATHERMAP_API_KEY=your_api_key")
                print("\nUsing sample weather data for demonstration.")
                weather_data = self._get_sample_weather_data()
            else:
                try:
                    # Get current weather
                    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHERMAP_API_KEY}"
                    weather_response = requests.get(weather_url)
                    current_weather = weather_response.json()
                    
                    # Get forecast
                    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHERMAP_API_KEY}"
                    forecast_response = requests.get(forecast_url)
                    forecast = forecast_response.json()
                    
                    # Combine data
                    weather_data = {
                        "current": current_weather,
                        "forecast": forecast
                    }
                    
                    # Cache the data
                    self.weather_cache[cache_key] = {
                        "data": weather_data,
                        "timestamp": time.time()
                    }
                    self._save_cache(self.weather_cache, WEATHER_CACHE_FILE)
                    
                except Exception as e:
                    logger.error(f"Error getting weather data: {e}")
                    print(f"Error retrieving weather data: {str(e)}")
                    print("\nUsing sample weather data for demonstration.")
                    weather_data = self._get_sample_weather_data()
        
        # Display weather data
        self._display_weather(weather_data)
        
        # Option to plan a route based on weather
        print("\nOptions:")
        print("1. Plan a cycling route for this location")
        print("2. Return to Weather and Route Planner")
        
        option = input("> ")
        if option == "1":
            self.plan_route(lat, lon)
    
    def _get_sample_weather_data(self) -> Dict:
        """
        Return sample weather data for demonstration purposes.
        Used when API key is not available.
        """
        # Generate weather data based on the current date
        current_date = datetime.now()
        
        # Create sample current weather
        current_weather = {
            "name": "Sample City",
            "main": {
                "temp": 22.5,
                "feels_like": 23.0,
                "temp_min": 20.0,
                "temp_max": 25.0,
                "humidity": 65
            },
            "wind": {
                "speed": 3.5,
                "deg": 180
            },
            "weather": [
                {
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ]
        }
        
        # Create sample forecast
        forecast_list = []
        weather_types = ["Clear", "Clouds", "Rain", "Clear", "Clear"]
        descriptions = ["clear sky", "scattered clouds", "light rain", "clear sky", "clear sky"]
        icons = ["01d", "03d", "10d", "01d", "01d"]
        
        for i in range(5):
            forecast_date = current_date + timedelta(days=i)
            
            # Morning forecast (9 AM)
            morning = forecast_date.replace(hour=9, minute=0, second=0)
            forecast_list.append({
                "dt": int(morning.timestamp()),
                "main": {
                    "temp": 20.0 + i,
                    "feels_like": 21.0 + i,
                    "temp_min": 18.0 + i,
                    "temp_max": 22.0 + i,
                    "humidity": 70 - i * 2
                },
                "wind": {
                    "speed": 3.0 + (i * 0.5),
                    "deg": 180 + (i * 10)
                },
                "weather": [
                    {
                        "main": weather_types[i],
                        "description": descriptions[i],
                        "icon": icons[i]
                    }
                ],
                "dt_txt": morning.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Afternoon forecast (3 PM)
            afternoon = forecast_date.replace(hour=15, minute=0, second=0)
            forecast_list.append({
                "dt": int(afternoon.timestamp()),
                "main": {
                    "temp": 24.0 + i,
                    "feels_like": 25.0 + i,
                    "temp_min": 22.0 + i,
                    "temp_max": 27.0 + i,
                    "humidity": 60 - i * 2
                },
                "wind": {
                    "speed": 4.0 + (i * 0.5),
                    "deg": 200 + (i * 10)
                },
                "weather": [
                    {
                        "main": weather_types[i],
                        "description": descriptions[i],
                        "icon": icons[i]
                    }
                ],
                "dt_txt": afternoon.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return {
            "current": current_weather,
            "forecast": {"list": forecast_list}
        }
    
    def _display_weather(self, weather_data: Dict) -> None:
        """Display weather data in a formatted way."""
        try:
            # Display current weather
            current = weather_data.get("current", {})
            city_name = current.get("name", "Unknown Location")
            current_temp = current.get("main", {}).get("temp", 0)
            feels_like = current.get("main", {}).get("feels_like", 0)
            humidity = current.get("main", {}).get("humidity", 0)
            wind_speed = current.get("wind", {}).get("speed", 0)
            wind_direction = current.get("wind", {}).get("deg", 0)
            weather_main = current.get("weather", [{}])[0].get("main", "Unknown")
            weather_desc = current.get("weather", [{}])[0].get("description", "")
            
            # Convert to imperial if user preference is set
            use_imperial = False
            if self.user_manager and self.user_manager.is_authenticated():
                use_imperial = self.user_manager.get_user_preference("use_imperial", False)
            
            if use_imperial:
                temp_unit = "°F"
                speed_unit = "mph"
                current_temp = utils.celsius_to_fahrenheit(current_temp)
                feels_like = utils.celsius_to_fahrenheit(feels_like)
                wind_speed = utils.kmh_to_mph(wind_speed)
            else:
                temp_unit = "°C"
                speed_unit = "km/h"
            
            # Format wind direction
            direction = self._get_wind_direction(wind_direction)
            
            # Print current weather
            print(f"\n{ascii_art.Fore.CYAN}{ascii_art.Style.BRIGHT}Current Weather for {city_name}{ascii_art.Style.RESET_ALL}")
            print(f"Temperature: {current_temp:.1f}{temp_unit} (Feels like: {feels_like:.1f}{temp_unit})")
            print(f"Conditions: {weather_main} - {weather_desc}")
            print(f"Humidity: {humidity}%")
            print(f"Wind: {wind_speed:.1f} {speed_unit} {direction}")
            
            # Get cycling recommendation
            recommendation = self._get_cycling_recommendation(current_temp, weather_main, wind_speed)
            print(f"\n{ascii_art.Fore.YELLOW}Cycling Recommendation: {recommendation}{ascii_art.Style.RESET_ALL}")
            
            # Show forecast for next few days
            forecast = weather_data.get("forecast", {}).get("list", [])
            if forecast:
                print(f"\n{ascii_art.Fore.CYAN}{ascii_art.Style.BRIGHT}5-Day Forecast{ascii_art.Style.RESET_ALL}")
                
                # Group forecast by day
                daily_forecast = {}
                for item in forecast:
                    date_txt = item.get("dt_txt", "")
                    if not date_txt:
                        continue
                    
                    # Extract date part
                    date = date_txt.split(" ")[0]
                    
                    # Skip today (already shown in current weather)
                    if date == datetime.now().strftime("%Y-%m-%d"):
                        continue
                    
                    if date not in daily_forecast:
                        daily_forecast[date] = []
                    
                    daily_forecast[date].append(item)
                
                # Show one item per day (preferably afternoon)
                for date, items in sorted(daily_forecast.items()):
                    # Prefer afternoon forecast (around 12-15)
                    best_item = items[0]
                    for item in items:
                        time_txt = item.get("dt_txt", "").split(" ")[1]
                        if "12:" in time_txt or "15:" in time_txt:
                            best_item = item
                            break
                    
                    # Display forecast for this day
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    day_name = date_obj.strftime("%A")
                    temp = best_item.get("main", {}).get("temp", 0)
                    weather = best_item.get("weather", [{}])[0].get("main", "Unknown")
                    desc = best_item.get("weather", [{}])[0].get("description", "")
                    
                    if use_imperial:
                        temp = utils.celsius_to_fahrenheit(temp)
                    
                    print(f"{day_name}: {temp:.1f}{temp_unit} - {weather} ({desc})")
        
        except Exception as e:
            logger.error(f"Error displaying weather data: {e}")
            print(f"Error displaying weather data: {str(e)}")
    
    def _get_wind_direction(self, degrees: float) -> str:
        """Convert wind direction in degrees to cardinal direction."""
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                     "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def _get_cycling_recommendation(self, temp: float, weather: str, wind_speed: float) -> str:
        """Get cycling recommendation based on weather conditions."""
        # Bad weather conditions
        if weather in ["Thunderstorm", "Tornado", "Hurricane", "Snow", "Sleet", "Hail"]:
            return "Not recommended - Dangerous weather conditions"
        
        if weather in ["Heavy Rain", "Freezing Rain"]:
            return "Not recommended - Heavy rain conditions"
        
        # Temperature considerations
        if temp < 0:
            return "Challenging - Very cold, dress in layers and protect extremities"
        
        if temp < 5:
            return "Challenging - Cold conditions, dress warmly"
        
        if temp > 35:
            return "Challenging - Very hot, stay hydrated and avoid midday rides"
        
        # Wind considerations
        if wind_speed > 40:
            return "Not recommended - Dangerously high winds"
        
        if wind_speed > 25:
            return "Challenging - Strong winds, be cautious"
        
        # Light rain
        if weather in ["Rain", "Drizzle"]:
            return "Fair - Light rain, use fenders and water-resistant gear"
        
        # Ideal conditions
        if 10 <= temp <= 25 and weather in ["Clear", "Clouds", "Mist"] and wind_speed < 15:
            return "Excellent - Ideal conditions for cycling"
        
        # Good conditions
        if 5 <= temp <= 30 and weather not in ["Rain", "Drizzle"] and wind_speed < 20:
            return "Good - Favorable conditions for cycling"
        
        # Default
        return "Fair - Acceptable conditions but be prepared"
    
    def plan_route(self, start_lat=None, start_lon=None):
        """Plan a cycling route."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Route Planner")
        
        if not FOLIUM_AVAILABLE:
            print("The folium library is required for route planning visualization.")
            print("Please install it with: pip install folium")
            input("\nPress Enter to continue...")
            return
        
        # Get start and end locations
        if start_lat is None or start_lon is None:
            print("Enter starting location (city or landmark):")
            start_location = input("> ")
            start_coords = self._get_coordinates(start_location)
            if not start_coords:
                print("Could not find starting location.")
                input("\nPress Enter to continue...")
                return
        else:
            start_coords = (start_lat, start_lon)
        
        print("Enter destination (city or landmark):")
        end_location = input("> ")
        end_coords = self._get_coordinates(end_location)
        if not end_coords:
            print("Could not find destination.")
            input("\nPress Enter to continue...")
            return
        
        # Calculate route distance
        start_lat, start_lon = start_coords
        end_lat, end_lon = end_coords
        direct_distance = utils.calculate_distance(start_lat, start_lon, end_lat, end_lon)
        
        print(f"\nDirect distance: {utils.format_distance(direct_distance)}")
        
        # Get route info
        route_info = self._get_route(start_coords, end_coords)
        if route_info:
            distance = route_info.get("distance", direct_distance)
            duration = route_info.get("duration", direct_distance * 4)  # Estimate 15 km/h
            elevation = route_info.get("elevation", 0)
            
            print(f"Route distance: {utils.format_distance(distance)}")
            print(f"Estimated duration: {duration:.0f} minutes")
            if elevation:
                print(f"Elevation gain: {elevation:.0f} meters")
        else:
            print("Could not get detailed route information.")
            print("Using direct distance for calculations.")
            distance = direct_distance
            duration = direct_distance * 4  # Estimate 15 km/h
        
        # Save route if user wants
        print("\nWould you like to save this route? (y/n)")
        save = input("> ")
        if save.lower() == "y":
            name = input("Enter a name for this route: ")
            self._save_route(name, start_coords, end_coords, distance, duration)
        
        # Generate map
        map_path = self._generate_route_map(start_coords, end_coords, f"Route: {direct_distance:.1f} km")
        if map_path:
            print(f"\nRoute map saved to: {map_path}")
            
            # Open map in browser if user wants
            print("Open map in browser? (y/n)")
            open_map = input("> ")
            if open_map.lower() == "y":
                try:
                    webbrowser.open(f"file://{os.path.abspath(map_path)}")
                except Exception as e:
                    logger.error(f"Error opening map in browser: {e}")
                    print(f"Error opening map: {str(e)}")
        
        # Calculate eco impact
        print("\nCalculating environmental impact...")
        self.calculate_cycling_eco_impact(distance)
        
        input("\nPress Enter to continue...")
    
    def _get_coordinates(self, location: str) -> Optional[Tuple[float, float]]:
        """Get coordinates for a location name."""
        # Check if it's a default location
        if location in DEFAULT_COORDINATES:
            return DEFAULT_COORDINATES[location]
        
        # Try using OpenWeatherMap Geocoding API
        if OPENWEATHERMAP_API_KEY and REQUESTS_AVAILABLE:
            try:
                geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={OPENWEATHERMAP_API_KEY}"
                geo_response = requests.get(geo_url)
                geo_data = geo_response.json()
                
                if geo_data and len(geo_data) > 0:
                    lat = geo_data[0]["lat"]
                    lon = geo_data[0]["lon"]
                    return (lat, lon)
            except Exception as e:
                logger.error(f"Error getting coordinates: {e}")
        
        # If we get here, we couldn't get coordinates
        return None
    
    def _get_route(self, start_coords: Tuple[float, float], end_coords: Tuple[float, float]) -> Optional[Dict]:
        """Get route information between two coordinates."""
        # Check cache first
        cache_key = f"{start_coords[0]},{start_coords[1]}-{end_coords[0]},{end_coords[1]}"
        if cache_key in self.routes_cache:
            return self.routes_cache[cache_key]
        
        # If we have MapBox API key, use their directions API
        if MAPBOX_ACCESS_TOKEN and REQUESTS_AVAILABLE:
            try:
                url = f"https://api.mapbox.com/directions/v5/mapbox/cycling/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?geometries=geojson&access_token={MAPBOX_ACCESS_TOKEN}"
                response = requests.get(url)
                data = response.json()
                
                if "routes" in data and len(data["routes"]) > 0:
                    route = data["routes"][0]
                    distance = route["distance"] / 1000  # Convert to kilometers
                    duration = route["duration"] / 60    # Convert to minutes
                    
                    # Get elevation data (this would require additional API calls in a real app)
                    elevation = 0  # Placeholder
                    
                    route_info = {
                        "distance": distance,
                        "duration": duration,
                        "elevation": elevation
                    }
                    
                    # Cache the route
                    self.routes_cache[cache_key] = route_info
                    self._save_cache(self.routes_cache, ROUTES_CACHE_FILE)
                    
                    return route_info
            except Exception as e:
                logger.error(f"Error getting route: {e}")
        
        # Otherwise, provide a simple estimation
        direct_distance = utils.calculate_distance(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
        route_distance = direct_distance * 1.3  # Add 30% for non-direct routes
        
        # Default speed of 15 km/h
        duration = route_distance / 15 * 60  # Convert to minutes
        
        route_info = {
            "distance": route_distance,
            "duration": duration,
            "elevation": 0
        }
        
        # Cache the route
        self.routes_cache[cache_key] = route_info
        self._save_cache(self.routes_cache, ROUTES_CACHE_FILE)
        
        return route_info
    
    def _save_route(self, name: str, start_coords: Tuple[float, float], end_coords: Tuple[float, float], 
                   distance: float, duration: float) -> bool:
        """Save a route to the user's saved routes."""
        if not self.user_manager or not self.user_manager.is_authenticated():
            print("You need to be logged in to save routes.")
            return False
        
        # Get user's saved routes
        user = self.user_manager.get_current_user()
        if "saved_routes" not in user:
            user["saved_routes"] = []
        
        # Create route object
        route = {
            "name": name,
            "start_coords": start_coords,
            "end_coords": end_coords,
            "distance": distance,
            "duration": duration,
            "date_saved": datetime.now().isoformat()
        }
        
        # Add to saved routes
        user["saved_routes"].append(route)
        
        # Save user data
        if self.user_manager.save_users():
            print(f"Route '{name}' saved successfully!")
            return True
        else:
            print("Error saving route.")
            return False
    
    def view_saved_routes(self):
        """View and manage saved routes."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Saved Routes")
        
        if not self.user_manager or not self.user_manager.is_authenticated():
            print("You need to be logged in to view saved routes.")
            input("\nPress Enter to continue...")
            return
        
        # Get user's saved routes
        user = self.user_manager.get_current_user()
        routes = user.get("saved_routes", [])
        
        if not routes:
            print("You don't have any saved routes.")
            input("\nPress Enter to continue...")
            return
        
        # Display routes
        print(f"You have {len(routes)} saved routes:")
        
        for i, route in enumerate(routes, 1):
            name = route.get("name", "Unnamed Route")
            distance = route.get("distance", 0)
            date_saved = route.get("date_saved", "Unknown date")
            
            # Format date if it's a valid ISO format
            if isinstance(date_saved, str) and re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', date_saved):
                try:
                    date_obj = datetime.fromisoformat(date_saved)
                    date_saved = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    pass
            
            print(f"{i}. {name} - {distance:.1f} km (saved on {date_saved})")
        
        # Menu options
        print("\nOptions:")
        print("1. View route details")
        print("2. Generate map for a route")
        print("3. Delete a route")
        print("4. Return to Route Planner")
        
        choice = input("\nSelect an option: ")
        
        if choice == "1":
            # View route details
            route_number = input("Enter route number to view: ")
            try:
                route_index = int(route_number) - 1
                if 0 <= route_index < len(routes):
                    self._display_route_details(routes[route_index])
                else:
                    print("Invalid route number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            
            input("\nPress Enter to continue...")
            self.view_saved_routes()  # Return to saved routes menu
            
        elif choice == "2":
            # Generate map
            route_number = input("Enter route number to generate map for: ")
            try:
                route_index = int(route_number) - 1
                if 0 <= route_index < len(routes):
                    route = routes[route_index]
                    map_path = self._generate_route_map(
                        route.get("start_coords"), 
                        route.get("end_coords"),
                        route.get("name", "Route")
                    )
                    if map_path:
                        print(f"\nRoute map saved to: {map_path}")
                        
                        # Open map in browser if user wants
                        print("Open map in browser? (y/n)")
                        open_map = input("> ")
                        if open_map.lower() == "y":
                            try:
                                webbrowser.open(f"file://{os.path.abspath(map_path)}")
                            except Exception as e:
                                logger.error(f"Error opening map in browser: {e}")
                                print(f"Error opening map: {str(e)}")
                else:
                    print("Invalid route number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
            input("\nPress Enter to continue...")
            self.view_saved_routes()  # Return to saved routes menu
            
        elif choice == "3":
            # Delete route
            route_number = input("Enter route number to delete: ")
            try:
                route_index = int(route_number) - 1
                if 0 <= route_index < len(routes):
                    route_name = routes[route_index].get("name", "Unnamed Route")
                    confirm = input(f"Are you sure you want to delete route '{route_name}'? (y/n): ")
                    
                    if confirm.lower() == "y":
                        routes.pop(route_index)
                        if self.user_manager.save_users():
                            print(f"Route '{route_name}' deleted successfully!")
                        else:
                            print("Error deleting route.")
                else:
                    print("Invalid route number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
            input("\nPress Enter to continue...")
            self.view_saved_routes()  # Return to saved routes menu
    
    def _display_route_details(self, route: Dict):
        """Display detailed information about a route."""
        name = route.get("name", "Unnamed Route")
        distance = route.get("distance", 0)
        duration = route.get("duration", 0)
        date_saved = route.get("date_saved", "Unknown date")
        start_coords = route.get("start_coords", (0, 0))
        end_coords = route.get("end_coords", (0, 0))
        
        # Format date if it's a valid ISO format
        if isinstance(date_saved, str) and re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', date_saved):
            try:
                date_obj = datetime.fromisoformat(date_saved)
                date_saved = date_obj.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                pass
        
        print("\nRoute Details:")
        print(f"Name: {name}")
        print(f"Distance: {distance:.1f} km")
        print(f"Estimated duration: {duration:.0f} minutes")
        print(f"Date saved: {date_saved}")
        print(f"Starting coordinates: {start_coords[0]:.6f}, {start_coords[1]:.6f}")
        print(f"Ending coordinates: {end_coords[0]:.6f}, {end_coords[1]:.6f}")
        
        # Calculate some additional stats
        avg_speed = distance / (duration / 60) if duration > 0 else 0
        calories = utils.calculate_calories(distance, avg_speed, 70)  # Assume 70kg rider
        co2_saved = utils.calculate_co2_saved(distance)
        
        print("\nEstimated Statistics:")
        print(f"Average speed: {avg_speed:.1f} km/h")
        print(f"Calories burned (70kg rider): {calories}")
        print(f"CO2 emissions saved: {co2_saved:.2f} kg")
    
    def _generate_route_map(self, start_coords: Tuple[float, float], end_coords: Tuple[float, float], 
                           title: str = "Cycling Route") -> Optional[str]:
        """Generate a route map between two points and save it as HTML."""
        if not FOLIUM_AVAILABLE:
            return None
        
        try:
            # Calculate center point
            center_lat = (start_coords[0] + end_coords[0]) / 2
            center_lon = (start_coords[1] + end_coords[1]) / 2
            
            # Create map
            cycling_map = folium.Map(location=[center_lat, center_lon], zoom_start=10)
            
            # Add markers
            folium.Marker(
                location=[start_coords[0], start_coords[1]],
                popup="Start",
                icon=folium.Icon(icon="play", color="green")
            ).add_to(cycling_map)
            
            folium.Marker(
                location=[end_coords[0], end_coords[1]],
                popup="End",
                icon=folium.Icon(icon="stop", color="red")
            ).add_to(cycling_map)
            
            # Add a simple line for the route
            folium.PolyLine(
                locations=[[start_coords[0], start_coords[1]], [end_coords[0], end_coords[1]]],
                color="blue",
                weight=5,
                opacity=0.8
            ).add_to(cycling_map)
            
            # Add title
            folium.map.Marker(
                [start_coords[0], start_coords[1]],
                icon=folium.DivIcon(
                    icon_size=(150, 36),
                    icon_anchor=(75, 60),
                    html=f'<div style="font-size: 14pt; font-weight: bold; color: blue">{title}</div>'
                )
            ).add_to(cycling_map)
            
            # Save map
            filename = f"route_map_{int(time.time())}.html"
            cycling_map.save(filename)
            
            return filename
        
        except Exception as e:
            logger.error(f"Error generating map: {e}")
            print(f"Error generating map: {str(e)}")
            return None
    
    def cycling_impact_calculator(self):
        """Calculate environmental and health impact of cycling."""
        ascii_art.clear_screen()
        ascii_art.display_header()
        ascii_art.display_section_header("Cycling Impact Calculator")
        
        print("Calculate the environmental and health benefits of your cycling:")
        
        # Get input distance and frequency
        try:
            distance = float(input("Average cycling distance per trip (km): "))
            trips_per_week = float(input("Number of trips per week: "))
            
            # Get optional inputs or use defaults
            weight = 70.0  # default weight in kg
            weight_input = input("Your weight (kg) [default: 70]: ")
            if weight_input:
                weight = float(weight_input)
            
            speed = 15.0  # default speed in km/h
            speed_input = input("Your average cycling speed (km/h) [default: 15]: ")
            if speed_input:
                speed = float(speed_input)
            
            print("\nCalculating impacts...")
            
            # Calculate weekly, monthly, yearly distances
            weekly_distance = distance * trips_per_week
            monthly_distance = weekly_distance * 4.33  # Average weeks per month
            yearly_distance = weekly_distance * 52
            
            # Calculate savings and benefits
            weekly_co2 = utils.calculate_co2_saved(weekly_distance)
            monthly_co2 = utils.calculate_co2_saved(monthly_distance)
            yearly_co2 = utils.calculate_co2_saved(yearly_distance)
            
            calories_per_trip = utils.calculate_calories(distance, speed, int(weight))
            weekly_calories = calories_per_trip * trips_per_week
            monthly_calories = weekly_calories * 4.33
            yearly_calories = weekly_calories * 52
            
            # Display results
            print("\nYour Cycling Impact:")
            print(f"\nDistance:")
            print(f"Per week: {weekly_distance:.1f} km")
            print(f"Per month: {monthly_distance:.1f} km")
            print(f"Per year: {yearly_distance:.1f} km")
            
            print(f"\nCalories Burned:")
            print(f"Per trip: {calories_per_trip}")
            print(f"Per week: {weekly_calories:.0f}")
            print(f"Per month: {monthly_calories:.0f}")
            print(f"Per year: {yearly_calories:.0f}")
            
            print(f"\nCO2 Emissions Saved:")
            print(f"Per week: {weekly_co2:.2f} kg")
            print(f"Per month: {monthly_co2:.2f} kg")
            print(f"Per year: {yearly_co2:.2f} kg")
            
            # Calculate equivalents
            trees_yearly = yearly_co2 / 20  # One tree absorbs about 20kg CO2 per year
            car_km = yearly_co2 / 0.13  # Average car emits about 130g CO2 per km
            
            print("\nYearly CO2 Savings Equivalent to:")
            print(f"- The CO2 absorbed by {trees_yearly:.1f} trees")
            print(f"- The emissions from driving {car_km:.1f} km in an average car")
            
            # Health benefits
            print("\nEstimated Health Benefits:")
            print("- Improved cardiovascular health")
            print("- Reduced risk of heart disease and stroke")
            print("- Improved mental wellbeing")
            print("- Better sleep quality")
            print("- Strengthened immune system")
            
            # Weight loss estimation (very rough - 7700 kcal = 1kg fat)
            if yearly_calories > 0:
                weight_loss = yearly_calories / 7700
                print(f"\nPotential yearly weight loss: {weight_loss:.1f} kg (if calories not replaced)")
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        
        input("\nPress Enter to continue...")
    
    def calculate_cycling_eco_impact(self, distance: float) -> None:
        """Calculate and display environmental impact of a cycling trip."""
        # Calculate CO2 savings
        co2_saved = utils.calculate_co2_saved(distance)
        
        # Calculate fuel savings (rough estimate - 7 liters per 100 km for average car)
        fuel_saved = distance * 0.07  # liters
        
        # Calculate money saved (rough estimate - average fuel price $1.5 per liter)
        money_saved = fuel_saved * 1.5  # dollars
        
        # Display results
        print("\nEnvironmental Impact of Your Cycling Trip:")
        print(f"CO2 emissions saved: {co2_saved:.2f} kg")
        print(f"Fuel saved: {fuel_saved:.2f} liters")
        print(f"Money saved on fuel: ${money_saved:.2f}")
        
        # Show equivalents
        trees_day = co2_saved / 0.055  # One tree absorbs about 20kg CO2 per year = 0.055kg per day
        light_bulbs = co2_saved / 0.1  # 100W light bulb for 24 hours ~ 0.1kg CO2
        
        print("\nThis is equivalent to:")
        print(f"- The daily CO2 absorption of {trees_day:.1f} trees")
        print(f"- The emissions from {light_bulbs:.1f} 100W light bulbs running for 24 hours")


def run_planner(user_manager_instance=None):
    """
    Run the weather and route planner as a standalone module.
    
    Args:
        user_manager_instance: Optional user manager for accessing user preferences
    """
    planner = WeatherRoutePlanner(user_manager_instance)
    planner.run_planner()


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the planner
    run_planner()