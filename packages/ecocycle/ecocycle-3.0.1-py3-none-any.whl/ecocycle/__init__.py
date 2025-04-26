"""
EcoCycle - Cycle into a greener tomorrow

A comprehensive Python-based cycling and sustainability tracking application that 
empowers users to monitor their environmental impact through innovative features 
and interactive tools.

Core Features:
- Cycling activity tracking with detailed statistics
- Environmental impact calculations and carbon footprint analysis
- Weather integration and cycling route planning
- Personalized eco-challenges with goal tracking
- AI-powered cycling route recommendations (requires Gemini API)
- Data visualization with charts and progress tracking
- Social sharing and achievement gamification
- Customizable notification system with multiple delivery options
- Export functionality with multiple format options (CSV, JSON, PDF)
- Secure local and cloud-based (Google Sheets) data storage
"""

VERSION = "3.0.1"
__author__ = "Shirish Pothi"

# Import and expose the main_program function at the module level
try:
    from .main import main as main_program
except ImportError:
    # Handle the case when running directly
    from main import main as main_program

# Define what symbols are exported when using "from ecocycle import *"
__all__ = ['main_program', 'VERSION']