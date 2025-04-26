"""
EcoCycle - User Manager Module
Handles user authentication, registration, and profile management.
"""
import os
import json
import getpass
import logging
import hashlib
import base64
import re
import time
import shutil
import bcrypt
from datetime import datetime
import webbrowser
import threading
import socketserver
import http.server
from typing import Dict, List, Optional, Any, Union
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urlparse, parse_qs

# Constants for Google OAuth
CLIENT_SECRETS_FILE = "/Users/shirishpothi/PycharmProjects/ecocycle/Google Auth Client Secret.json"
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
REDIRECT_URI = 'http://localhost:8080/' # Must match one in Google Cloud Console

logger = logging.getLogger(__name__)

# --- Constants ---
DEFAULT_USERS_FILE = "users.json"
SALT_LENGTH = 16
DEFAULT_ITERATIONS = 100000
SESSION_FILE = "session.json"
SESSION_SECRET_ENV_VAR = "SESSION_SECRET_KEY"


class UserManager:
    """Manages user authentication and profiles."""
    
    def __init__(self, sheets_manager=None):
        """
        Initialize the UserManager.
        
        Args:
            sheets_manager: Optional sheets manager for user data storage in Google Sheets
        """
        self.users = {}
        self.current_user = None
        self.sheets_manager = sheets_manager
        self.google_auth_lock = threading.Lock() # Lock for thread safety during auth
        
        # Ensure users file directory exists
        os.makedirs(os.path.dirname(DEFAULT_USERS_FILE) if os.path.dirname(DEFAULT_USERS_FILE) else '.', exist_ok=True)
        
        # Load existing users
        self.load_users()
        
        # Create a guest user if it doesn't exist
        if 'guest' not in self.users:
            self.users['guest'] = {
                'username': 'guest',
                'name': 'Guest User',
                'is_guest': True,
                'stats': {
                    'total_trips': 0,
                    'total_distance': 0.0,
                    'total_co2_saved': 0.0,
                    'total_calories': 0
                },
                'preferences': {}
            }
            self.save_users()
    
    def load_users(self) -> None:
        """Load users from local file or Google Sheets."""
        # Try to load from Google Sheets first if available
        if self.sheets_manager and self.sheets_manager.is_available():
            users = self.sheets_manager.get_users()
            if users:
                self.users = users
                logger.info("Users loaded from Google Sheets")
                return
        
        # Fall back to local file
        self._load_local_users()
    
    def _load_local_users(self) -> None:
        """
        Load users from local JSON file with enhanced security practices.
        
        - Uses atomic file operations where possible
        - Validates file content structure
        - Uses secure file permissions
        """
        if os.path.exists(DEFAULT_USERS_FILE):
            try:
                # Check file size before loading to prevent memory issues
                file_size = os.path.getsize(DEFAULT_USERS_FILE)
                if file_size > 10 * 1024 * 1024:  # 10MB limit
                    logger.error(f"Users file {DEFAULT_USERS_FILE} is too large ({file_size} bytes). Possible corruption or attack.")
                    self.users = {}
                    return
                
                # Load and parse the file
                with open(DEFAULT_USERS_FILE, 'r') as file:
                    data = json.load(file)
                
                # Validate the structure of the loaded data
                if not isinstance(data, dict):
                    logger.error(f"Invalid users file format. Expected dictionary, got {type(data).__name__}")
                    self.users = {}
                    return
                
                # Basic validation of user entries
                for username, user_data in list(data.items()):
                    if not isinstance(user_data, dict):
                        logger.warning(f"Removing invalid user entry for '{username}': not a dictionary")
                        del data[username]
                        continue
                    
                    # Ensure required fields exist with proper types
                    if 'username' not in user_data or user_data['username'] != username:
                        logger.warning(f"Fixing inconsistent username for '{username}'")
                        user_data['username'] = username
                    
                    # Ensure stats and preferences dictionaries exist
                    if 'stats' not in user_data or not isinstance(user_data['stats'], dict):
                        logger.warning(f"Initializing missing stats for user '{username}'")
                        user_data['stats'] = {
                            'total_trips': 0,
                            'total_distance': 0.0,
                            'total_co2_saved': 0.0,
                            'total_calories': 0,
                            'trips': []
                        }
                    
                    if 'preferences' not in user_data or not isinstance(user_data['preferences'], dict):
                        logger.warning(f"Initializing missing preferences for user '{username}'")
                        user_data['preferences'] = {}
                
                self.users = data
                logger.info(f"Users loaded from {DEFAULT_USERS_FILE} ({len(self.users)} users)")
                
                # Try to fix file permissions if needed
                try:
                    if os.name != 'nt':  # Skip on Windows
                        current_mode = os.stat(DEFAULT_USERS_FILE).st_mode
                        secure_mode = 0o600  # Only owner can read/write
                        if (current_mode & 0o777) != secure_mode:
                            os.chmod(DEFAULT_USERS_FILE, secure_mode)
                            logger.info(f"Fixed file permissions for {DEFAULT_USERS_FILE}")
                except Exception as perm_error:
                    logger.warning(f"Unable to set secure file permissions: {perm_error}")
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in users file: {e}")
                self.users = {}
                
                # Backup the corrupted file
                backup_file = f"{DEFAULT_USERS_FILE}.corrupted.{int(time.time())}"
                try:
                    shutil.copy2(DEFAULT_USERS_FILE, backup_file)
                    logger.info(f"Backed up corrupted users file to {backup_file}")
                except Exception as backup_error:
                    logger.error(f"Failed to backup corrupted users file: {backup_error}")
                
            except Exception as e:
                logger.error(f"Error loading users from file: {e}")
                self.users = {}
        else:
            logger.info(f"Users file {DEFAULT_USERS_FILE} not found, starting with empty users")
            self.users = {}
    
    def save_users(self) -> bool:
        """Save users to local file or Google Sheets."""
        # Try to save to Google Sheets if available
        if self.sheets_manager and self.sheets_manager.is_available():
            if self.sheets_manager.save_users(self.users):
                logger.info("Users saved to Google Sheets")
                
                # Also save to local file as backup
                self._save_local_users()
                return True
        
        # Fall back to local file
        return self._save_local_users()
    
    def _save_local_users(self) -> bool:
        """
        Save users to local JSON file with enhanced security practices.

        - Uses atomic write operations to prevent data corruption
        - Sets appropriate file permissions
        - Backs up previous version before overwriting
        """
        # First backup the existing file if it exists
        try:
            if os.path.exists(DEFAULT_USERS_FILE):
                backup_file = f"{DEFAULT_USERS_FILE}.bak"
                shutil.copy2(DEFAULT_USERS_FILE, backup_file)
                logger.debug(f"Backed up users file to {backup_file}")
        except Exception as e:
            logger.warning(f"Failed to create backup of users file: {e}")

        # Use a temporary file to write the data, then rename it
        # This ensures an atomic operation and prevents data corruption
        temp_file = f"{DEFAULT_USERS_FILE}.tmp"
        try:
            # Write to temporary file first
            with open(temp_file, 'w') as file:
                json.dump(self.users, file, indent=2)
                # --- FIX START ---
                # Ensure Python's buffers are written to the OS buffer
                file.flush()
                # Ensure the OS buffer is written to disk
                os.fsync(file.fileno())
                # --- FIX END ---

            # Now the 'with' block has exited, and the file is closed.
            # Proceed with the atomic rename.
            if os.name == 'nt':  # Windows
                # Windows requires special handling for atomic replace
                if os.path.exists(DEFAULT_USERS_FILE):
                    # This might fail if the file is locked, but it's the standard way
                    os.replace(temp_file, DEFAULT_USERS_FILE)
                else:
                    os.rename(temp_file, DEFAULT_USERS_FILE)
            else:  # Unix-like
                os.rename(temp_file, DEFAULT_USERS_FILE)

            # Set secure file permissions on Unix-like systems
            if os.name != 'nt':
                try:
                    os.chmod(DEFAULT_USERS_FILE, 0o600)  # Owner read/write only
                except Exception as perm_error:
                     logger.warning(f"Could not set permissions on {DEFAULT_USERS_FILE}: {perm_error}")


            logger.info(f"Users saved to {DEFAULT_USERS_FILE}")
            return True

        except Exception as e:
            logger.error(f"Error saving users to file: {e}")
            # Clean up temporary file if it exists
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as cleanup_error:
                    logger.error(f"Error removing temporary file {temp_file}: {cleanup_error}")
            return False

    def _get_google_user_info(self, credentials):
        """Fetches user info from Google People API using credentials."""
        try:
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            logger.info(f"Fetched Google user info for: {user_info.get('email')}")
            return user_info
        except HttpError as e:
            logger.error(f"Error fetching Google user info: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching Google user info: {e}", exc_info=True)
            return None

    def _authenticate_with_google(self) -> bool:
        """Handles the Google OAuth 2.0 flow."""
        # Placeholder for the actual OAuth flow logic
        # This will involve starting a local server, opening a browser, etc.
        logger.info("Starting Google OAuth flow.")
        
        # --- Start of OAuth Flow Implementation ---
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        flow.redirect_uri = REDIRECT_URI

        # Use a simple local server to handle the redirect
        auth_code = None
        server_started = threading.Event()
        server_shutdown = threading.Event()

        class OAuthCallbackHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                nonlocal auth_code
                # --- CHANGE START ---
                # Parse the URL and query string robustly
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)
                code_list = query_params.get('code') # Returns a list or None

                if code_list: # Check if 'code' parameter exists
                    auth_code = code_list[0] # Get the first code value
                # --- CHANGE END ---
                    # Instead of sending 200 OK with HTML, send 302 Redirect
                    self.send_response(302)
                    self.send_header('Location', 'https://ecocycle-auth-success.lovable.app/')
                    self.end_headers()
                    # No body needed for redirect
                    # --- CHANGE END ---
                    logger.info("Authorization code received successfully. Redirecting browser.")
                    # Signal that the server can shut down
                    server_shutdown.set()
                else: # No code found in query parameters
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Authentication failed or cancelled.")
                    logger.warning("OAuth callback received without authorization code.")
                    server_shutdown.set()

        httpd = None
        server_thread = None
        try:
            # Find an available port starting from 8080
            port = 8080
            while True:
                try:
                    httpd = socketserver.TCPServer(("localhost", port), OAuthCallbackHandler)
                    flow.redirect_uri = f'http://localhost:{port}/'
                    logger.info(f"Local OAuth server starting on port {port}")
                    break
                except OSError as e:
                    if e.errno == 98: # Address already in use
                        logger.warning(f"Port {port} already in use, trying next port.")
                        port += 1
                        if port > 8090: # Limit port search range
                            logger.error("Could not find an available port between 8080 and 8090.")
                            return False
                    else:
                        logger.error(f"Error starting local server: {e}", exc_info=True)
                        return False
            
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            server_started.set() # Signal server is ready (though serve_forever blocks)

            auth_url, _ = flow.authorization_url(prompt='select_account')
            print(f'\nPlease authorize EcoCycle in your browser: {auth_url}')
            webbrowser.open(auth_url)

            # Wait for the server thread to signal shutdown (code received or error)
            server_shutdown.wait(timeout=120) # Wait up to 2 minutes for user action

        except Exception as e:
            logger.error(f"Error during OAuth setup or browser launch: {e}", exc_info=True)
            return False
        finally:
            if httpd:
                httpd.shutdown() # Stop the server
                httpd.server_close()
                logger.info("Local OAuth server stopped.")
            if server_thread and server_thread.is_alive():
                server_thread.join(timeout=2)
                if server_thread.is_alive():
                    logger.warning("OAuth server thread did not terminate cleanly.")

        if not auth_code:
            logger.error("Failed to retrieve authorization code.")
            return False

        try:
            # Exchange code for credentials
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            logger.info("Successfully exchanged authorization code for credentials.")

            # Fetch user info
            user_info = self._get_google_user_info(credentials)
            if not user_info or 'email' not in user_info:
                logger.error("Failed to fetch user info or email from Google.")
                return False

            google_email = user_info['email']
            google_name = user_info.get('name', google_email) # Use name if available, else email
            google_id = user_info.get('id')

            # Check if user exists, if not, register them
            if google_email not in self.users:
                logger.info(f"New user via Google: {google_email}. Registering...")
                # Store minimal info, no password hash for Google users
                self.users[google_email] = {
                    'username': google_email, # Add username field explicitly
                    'name': google_name,
                    'email': google_email, # Store email as well
                    'password_hash': None, # Indicate Google login
                    'salt': None, # No salt for Google login
                    'google_id': google_id,
                    'is_admin': False,
                    'is_guest': False,
                    'registration_date': datetime.now().isoformat(),
                    'stats': {
                        'total_trips': 0,
                        'total_distance': 0.0,
                        'total_co2_saved': 0.0,
                        'total_calories': 0,
                        'trips': []
                    },
                    'preferences': {}
                }
                if not self.save_users():
                    logger.error(f"Failed to save new Google user {google_email} to users file.")
                    # Decide if login should proceed despite save failure (maybe)
                    # For now, let's fail the login if we can't save the user
                    return False
            else:
                # Update existing user's Google ID if missing
                if 'google_id' not in self.users[google_email] or not self.users[google_email]['google_id']:
                    self.users[google_email]['google_id'] = google_id
                    self.save_users() # Save the updated ID
                logger.info(f"Existing user {google_email} logged in via Google.")

            self.current_user = google_email
            # Optionally store credentials (e.g., for refresh tokens) - BE CAREFUL WITH SECURITY
            # self._save_google_credentials(credentials) 
            return True

        except Exception as e:
            logger.error(f"Error during token exchange or user processing: {e}", exc_info=True)
            return False
        # --- End of OAuth Flow Implementation ---

    # --- Session Management ---
    def _get_session_secret(self):
        """Retrieves the session secret key from environment variables."""
        secret = os.environ.get(SESSION_SECRET_ENV_VAR)
        if not secret:
            # Log critically, as session security relies on this
            logger.critical(f"{SESSION_SECRET_ENV_VAR} environment variable not set. Session persistence will be insecure or fail.")
            # Optionally, raise an exception or return a specific value if the key is absolutely mandatory
            # raise ValueError(f"{SESSION_SECRET_ENV_VAR} not set!")
            return None
        return secret.encode('utf-8') # Return as bytes for HMAC

    def _calculate_verifier(self, username):
        """Calculates the session verifier hash using HMAC-SHA256."""
        secret = self._get_session_secret()
        if not secret or not username:
            logger.error("Cannot calculate verifier: Missing secret key or username.")
            return None
        # Use a context prefix to prevent potential misuse of the hash
        message = f"session-user:{username}".encode('utf-8')
        try:
            verifier = hmac.new(secret, message, hashlib.sha256).hexdigest()
            return verifier
        except Exception as e:
            logger.error(f"Error calculating HMAC verifier: {e}")
            return None

    def _save_session(self, username):
        """Saves the current username and session verifier to the session file."""
        verifier = self._calculate_verifier(username)
        if not verifier:
            logger.error("Could not calculate session verifier. Aborting session save.")
            return False # Indicate failure

        session_data = {
            "username": username,
            "session_verifier": verifier
        }
        try:
            with open(SESSION_FILE, 'w') as f:
                json.dump(session_data, f)
            logger.info(f"Session saved for user '{username}' to {SESSION_FILE}")
            # Set permissions (optional, good practice on Linux/macOS)
            if os.name != 'nt':
                try:
                    os.chmod(SESSION_FILE, 0o600) # Read/write only for owner
                except Exception as perm_error:
                    logger.warning(f"Could not set permissions on {SESSION_FILE}: {perm_error}")
            return True # Indicate success
        except Exception as e:
            logger.error(f"Failed to write session to {SESSION_FILE}: {e}")
            return False # Indicate failure

    def _clear_session(self, expected_user=None):
        """
        Removes the session file. If expected_user is provided,
        optionally checks if the file belongs to that user before clearing.
        """
        if not os.path.exists(SESSION_FILE):
            logger.debug("No session file to clear.")
            return

        # Optional safety check: only clear if it matches the user logging out
        if expected_user:
            try:
                with open(SESSION_FILE, 'r') as f:
                    data = json.load(f)
                # Check if username exists and matches before clearing
                if data.get("username") != expected_user:
                    logger.warning(f"Session file user '{data.get('username')}' does not match expected user '{expected_user}' during logout/clear. Not clearing.")
                    return # Don't clear if it's not the user we expected
            except FileNotFoundError:
                 logger.debug("Session file disappeared before user check during clear.")
                 return # File is gone anyway
            except (json.JSONDecodeError, KeyError, TypeError) as read_err:
                logger.warning(f"Could not read/parse session file {SESSION_FILE} for user check before clearing: {read_err}. Proceeding to clear.")
                # Proceed to clear anyway, as the file is likely corrupt

        # Clear the file
        try:
            os.remove(SESSION_FILE)
            logger.info(f"Session file {SESSION_FILE} removed.")
        except FileNotFoundError:
             logger.debug("Session file disappeared before removal attempt.")
        except Exception as e:
            logger.error(f"Failed to remove session file {SESSION_FILE}: {e}")

    # --- End Session Management ---
    
    def authenticate(self) -> bool:
        """
        Authenticate a user through username/password or Google authentication.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        print("\nAuthentication")
        print("1. Login with username and password")
        print("2. Login as guest")
        print("3. Register new user")
        print("4. Login with Google")
        print("5. Cancel")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice == '1':
            # Login with username/password
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            
            if self._verify_credentials(username, password):
                self.current_user = username
                logger.info(f"User {username} authenticated successfully")

                logger.debug(f"Attempting to save session for user '{username}'")
                if not self._save_session(username):
                    # Log failure but still allow login for this session
                    logger.error(
                        "CRITICAL: Failed to save session state after login. User will need to log in again next time.")

                print(f"Welcome back, {self.users[username].get('name', username)}!")
                return True
            else:
                logger.warning(f"Failed authentication attempt for username: {username}")
                print("Invalid username or password.")
                self.current_user = None
                return False
                
        elif choice == '2':
            # Login as guest
            self.current_user = 'guest'
            logger.info("Guest user authenticated")
            print("Logged in as guest user.")
            self._clear_session()
            return True
            
        elif choice == '3':
            # Register and save new user
            registration_successful = self.register_new_user()
            if registration_successful:
                # Assuming successful registration means authentication is complete
                # The actual logic might depend on whether register_new_user logs the user in
                return True # Added missing indented block
        
        elif choice == '4':
            # Login with Google
            print("\nAttempting Google Login...")
            # Acquire lock to prevent concurrent Google auth flows if somehow triggered
            with self.google_auth_lock:
                success = self._authenticate_with_google()
            
            if success:
                # _authenticate_with_google now handles user creation/update and sets self.current_user
                logger.info(f"User {self.current_user} authenticated via Google")
                print(f"Welcome, {self.users.get(self.current_user, {}).get('name', self.current_user)}!")
                
                # Save session after successful Google login
                logger.debug(f"Attempting to save session for Google user '{self.current_user}'")
                if not self._save_session(self.current_user):
                    logger.error("CRITICAL: Failed to save session state after Google login.")
                    # Decide if login should still proceed? For now, let it proceed but log error.
                return True
            else:
                logger.warning("Google authentication failed.")
                print("Google authentication failed.")
                self.current_user = None # Ensure current_user is None on failure
                self._clear_session() # Clear any potentially lingering session info
                return False
            
        elif choice == '5':
            # Cancel
            print("Authentication cancelled.")
            self.current_user = None
            return False

        else:
            # Invalid choice handling (if needed, otherwise the original cancel logic fits here)
            print("Invalid choice.") # Or keep the original cancel logic if appropriate
            self.current_user = None
            return False
    
    def register_new_user(self) -> bool:
        """
        Register a new user with enhanced security validation.
        
        Returns:
            bool: True if registration successful, False otherwise
        """
        print("\nRegister New User")
        
        # Get user information with enhanced validation
        while True:
            username = input("Username (letters, numbers, underscore only): ").strip()
            
            # Check if username is empty
            if not username:
                print("Username cannot be empty.")
                continue
                
            # Check length constraints (prevent too long usernames)
            if len(username) < 3:
                print("Username must be at least 3 characters long.")
                continue
            
            if len(username) > 32:
                print("Username cannot exceed 32 characters.")
                continue
                
            # Check character constraints (prevent injection)
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                print("Username must contain only letters, numbers, and underscores.")
                continue
                
            # Check if username exists
            if username in self.users:
                print("Username already exists. Please choose another.")
                continue
            
            # Check for reserved names
            reserved_names = ['admin', 'system', 'root', 'administrator', 'guest']
            if username.lower() in reserved_names:
                print(f"Username '{username}' is reserved. Please choose another.")
                continue
                
            break
        
        # Full name validation
        name = input("Full Name: ").strip()
        if not name:
            name = username  # Default to username if name is empty
        
        # Email validation
        while True:
            email = input("Email (optional): ").strip()
            if not email:
                email = None  # Make it explicitly None if empty
                break
                
            # Simple email validation regex
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                print("Invalid email format. Please enter a valid email or leave empty.")
                continue
                
            break
        
        # Get and confirm password with enhanced security requirements
        while True:
            password = getpass.getpass("Password: ")
            
            # Check password length
            if len(password) < 8:
                print("Password must be at least 8 characters long.")
                continue
            
            # Check password strength
            has_uppercase = any(c.isupper() for c in password)
            has_lowercase = any(c.islower() for c in password)
            has_number = any(c.isdigit() for c in password)
            has_special = any(not c.isalnum() for c in password)
            
            if not (has_uppercase and has_lowercase and has_number):
                print("Password must contain at least one uppercase letter, one lowercase letter, and one number.")
                continue
                
            if not has_special:
                print("Warning: Adding a special character will make your password stronger.")
                confirm_weak = input("Continue with this password anyway? (y/n): ")
                if confirm_weak.lower() != 'y':
                    continue
                
            confirm_password = getpass.getpass("Confirm Password: ")
            if password != confirm_password:
                print("Passwords do not match.")
                continue
                
            break
        
        # Generate salt and hash password
        salt = self._generate_salt()
        password_hash = self._hash_password(password, salt)
        
        # Create user
        self.users[username] = {
            'username': username,
            'name': name,
            'email': email if email else None,
            'password_hash': password_hash,
            'salt': salt,
            'is_admin': False,
            'is_guest': False,
            'stats': {
                'total_trips': 0,
                'total_distance': 0.0,
                'total_co2_saved': 0.0,
                'total_calories': 0,
                'trips': []
            },
            'preferences': {}
        }
        
        # Save users
        if self.save_users():
            # Set current user
            self.current_user = username
            
            print(f"User {username} registered successfully!")
            return True
        else:
            print("Error saving user information.")
            return False
    
    def _verify_credentials(self, username: str, password: str) -> bool:
        """
        Verify username and password.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        if username not in self.users:
            return False
        
        user = self.users[username]
        
        # Guest user can't login with password
        if user.get('is_guest', False):
            return False
        
        # Get stored hash and salt
        stored_hash = user.get('password_hash')
        salt = user.get('salt')
        
        if not stored_hash or not salt:
            return False
        
        # Hash the provided password
        calculated_hash = self._hash_password(password, salt)
        
        # Compare hashes
        return calculated_hash == stored_hash
    
    def _generate_salt(self) -> str:
        """
        Generate a random salt for password hashing.
        
        Returns:
            str: Base64-encoded salt
        """
        salt_bytes = os.urandom(SALT_LENGTH)
        return base64.b64encode(salt_bytes).decode('utf-8')
    
    def _hash_password(self, password: str, salt: str) -> str:
        """
        Hash a password with salt using PBKDF2.
        
        Args:
            password (str): Password to hash
            salt (str): Base64-encoded salt
            
        Returns:
            str: Base64-encoded password hash
        """
        # Decode salt from base64
        salt_bytes = base64.b64decode(salt)
        
        # Hash the password
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt_bytes,
            DEFAULT_ITERATIONS
        )
        
        # Encode the key in base64
        return base64.b64encode(key).decode('utf-8')
    
    def get_current_user(self) -> Dict:
        """
        Get the currently authenticated user.
        
        Returns:
            dict: User data or empty dict if no user is authenticated
        """
        if self.current_user and self.current_user in self.users:
            return self.users[self.current_user]
        return {}
    
    def is_authenticated(self) -> bool:
        """
        Check if a user is currently authenticated.
        
        Returns:
            bool: True if a user is authenticated, False otherwise
        """
        return self.current_user is not None and self.current_user in self.users
    
    def is_guest(self) -> bool:
        """
        Check if the current user is a guest.
        
        Returns:
            bool: True if current user is a guest, False otherwise
        """
        if not self.is_authenticated():
            return False
        
        return self.users[self.current_user].get('is_guest', False)
    
    def is_admin(self) -> bool:
        """
        Check if the current user is an admin.
        
        Returns:
            bool: True if current user is an admin, False otherwise
        """
        if not self.is_authenticated():
            return False
        
        return self.users[self.current_user].get('is_admin', False)
    
    def update_user_stats(self, distance: float, co2_saved: float, calories: int) -> bool:
        """
        Update user statistics.
        
        Args:
            distance (float): Distance in kilometers
            co2_saved (float): CO2 saved in kilograms
            calories (int): Calories burned
            
        Returns:
            bool: True if stats were updated, False otherwise
        """
        if not self.is_authenticated():
            return False
        
        # Get current user
        user = self.users[self.current_user]
        
        # Ensure stats dictionary exists
        if 'stats' not in user:
            user['stats'] = {
                'total_trips': 0,
                'total_distance': 0.0,
                'total_co2_saved': 0.0,
                'total_calories': 0,
                'trips': []
            }
        
        # Ensure trips list exists
        if 'trips' not in user['stats']:
            user['stats']['trips'] = []
        
        # Create trip data
        trip = {
            'date': datetime.now().isoformat(),
            'distance': distance,
            'duration': 0.0,  # This would be set properly in the calling code
            'co2_saved': co2_saved,
            'calories': calories
        }
        
        # Add trip to trips list
        user['stats']['trips'].append(trip)
        
        # Update totals
        user['stats']['total_trips'] = user['stats'].get('total_trips', 0) + 1
        user['stats']['total_distance'] = user['stats'].get('total_distance', 0.0) + distance
        user['stats']['total_co2_saved'] = user['stats'].get('total_co2_saved', 0.0) + co2_saved
        user['stats']['total_calories'] = user['stats'].get('total_calories', 0) + calories
        
        # Save updated user data
        return self.save_users()
    
    def update_user_preference(self, key: str, value: Any) -> bool:
        """
        Update a user preference.
        
        Args:
            key (str): Preference key
            value: Preference value
            
        Returns:
            bool: True if preference was updated, False otherwise
        """
        if not self.is_authenticated():
            return False
        
        # Get current user
        user = self.users[self.current_user]
        
        # Ensure preferences dictionary exists
        if 'preferences' not in user:
            user['preferences'] = {}
        
        # Update preference
        user['preferences'][key] = value
        
        # Save updated user data
        return self.save_users()
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """
        Get a user preference.
        
        Args:
            key (str): Preference key
            default: Default value if preference not found
            
        Returns:
            Preference value or default
        """
        if not self.is_authenticated():
            return default
        
        # Get current user
        user = self.users[self.current_user]
        
        # Get preference value
        if 'preferences' in user and key in user['preferences']:
            return user['preferences'][key]
        
        return default
    
    def logout(self) -> None:
        """Log out the current user and clear the session."""
        logged_out_user = self.current_user  # Store username before clearing
        if logged_out_user:
            logger.info(f"User '{logged_out_user}' logged out")
            self._clear_session(expected_user=logged_out_user)  # Clear the session file
            self.current_user = None
            logger.info("Logout complete.")
        else:
            logger.debug("Logout called but no user was logged in.")
            # Ensure session file is cleared even if current_user was somehow None
            self._clear_session()


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test UserManager
    manager = UserManager()
    
    # Create a new admin user (for testing purposes)
    if 'admin' not in manager.users:
        print("Creating admin user...")
        
        # Generate admin credentials
        manager.users['admin'] = {
            'username': 'admin',
            'name': 'Administrator',
            'email': 'admin@example.com',
            'is_admin': True,
            'is_guest': False,
            'salt': manager._generate_salt(),
            'stats': {
                'total_trips': 0,
                'total_distance': 0.0,
                'total_co2_saved': 0.0,
                'total_calories': 0,
                'trips': []
            },
            'preferences': {}
        }
        
        # Set admin password (hard-coded for this test only)
        manager.users['admin']['password_hash'] = manager._hash_password('adminpass', manager.users['admin']['salt'])
        
        # Save users
        manager.save_users()
        print("Admin user created with username 'admin' and password 'adminpass'")
    
    # Test authentication
    success = manager.authenticate()
    print(f"Authentication {'successful' if success else 'failed'}")
    
    if success:
        print(f"Current user: {manager.get_current_user().get('name')}")
        print(f"Is admin: {manager.is_admin()}")
        print(f"Is guest: {manager.is_guest()}")
        
        # Test updating user preferences
        manager.update_user_preference('theme', 'dark')
        print(f"Theme preference: {manager.get_user_preference('theme')}")
        
        # Test updating user stats
        manager.update_user_stats(10.5, 2.42, 300)
        user = manager.get_current_user()
        print(f"User stats: {user['stats']}")
        
        # Test logout
        manager.logout()
        print(f"After logout - Is authenticated: {manager.is_authenticated()}")