#!/usr/bin/env python3
"""
EcoCycle - Enhanced ASCII Art Module
Contains enhanced ASCII art with animations and advanced display elements.

This module builds on the original ascii_art.py but adds features like:
- Loading animations using yaspin
- Animated progress bars using rich
- ASCII animation sequences for achievements
- Mascot animations for eco-tips
- Social media share card generator
- Interactive menus with highlight animations
"""

import os
import sys
import time
import random
import logging
import platform
import shutil
from typing import List, Optional, Any, Dict, Tuple

try:
    import colorama
    from colorama import Fore, Style
    colorama.init()
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class DummyFore:
        GREEN = ""
        BLUE = ""
        CYAN = ""
        YELLOW = ""
        RED = ""
        WHITE = ""
        MAGENTA = ""
        RESET = ""
    
    class DummyStyle:
        BRIGHT = ""
        RESET_ALL = ""
    
    Fore = DummyFore()
    Style = DummyStyle()

# Optional rich library for enhanced progress bars and tables
try:
    import rich
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    # Create dummy classes to avoid attribute errors
    class DummyConsole:
        def print(self, *args, **kwargs): print(*args)
    
    class DummyTable:
        def add_column(self, *args, **kwargs): pass
        def add_row(self, *args, **kwargs): pass
    
    class DummyText:
        def __init__(self, *args, **kwargs): pass
    
    class DummyPanel:
        def __init__(self, *args, **kwargs): pass
    
    class DummyRich:
        console = DummyConsole()
        table = DummyTable
        text = DummyText
        panel = DummyPanel
    
    rich = DummyRich()

# Optional blessed library for terminal control and animations
try:
    import blessed
    HAS_BLESSED = True
except ImportError:
    HAS_BLESSED = False

# Optional yaspin for loading spinners
try:
    from yaspin import yaspin
    from yaspin.spinners import Spinners
    HAS_YASPIN = True
except ImportError:
    HAS_YASPIN = False

# Get terminal dimensions
terminal_width, terminal_height = shutil.get_terminal_size((80, 24))

# ASCII Art Header
HEADER_ART = f"""
{Fore.CYAN}
 ______     ______     ______     ______     __  __     ______     __         ______    
/\  ___\   /\  ___\   /\  __ \   /\  ___\   /\ \_\ \   /\  ___\   /\ \       /\  ___\   
\ \  __\   \ \ \____  \ \ \/\ \  \ \ \____  \ \____ \  \ \ \____  \ \ \____  \ \  __\   
 \ \_____\  \ \_____\  \ \_____\  \ \_____\  \/\_____\  \ \_____\  \ \_____\  \ \_____\ 
  \/_____/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/ 
                 
Cycle into a greener tomorrow
{Style.RESET_ALL}"""

# Terminal capabilities
def init_terminal():
    """Initialize the terminal capabilities for enhanced display."""
    if HAS_BLESSED:
        return blessed.Terminal()
    return None

term = init_terminal()

# Basic functions from original ascii_art.py
def display_header() -> None:
    """Display the ASCII art header for EcoCycle."""
    print(HEADER_ART)
    print(f"{Fore.CYAN}{'-' * terminal_width}{Style.RESET_ALL}")

def clear_screen() -> None:
    """Clear the terminal screen in a cross-platform way."""
    if HAS_BLESSED and term:
        print(term.home + term.clear)
    else:
        os.system('cls' if platform.system() == 'Windows' else 'clear')

def display_section_header(title: str) -> None:
    """Display a section header with a title."""
    display_spacer()
    if HAS_BLESSED and term:
        print(term.bold + f"{Fore.CYAN}===== {title} ====={Style.RESET_ALL}" + term.normal)
    else:
        print(f"{Fore.CYAN}===== {title} ====={Style.RESET_ALL}")
    display_spacer()

def display_spacer() -> None:
    """Display a single line of space."""
    print()

def display_success_message(message: str) -> None:
    """Display a success message."""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def display_error_message(message: str) -> None:
    """Display an error message."""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def display_warning_message(message: str) -> None:
    """Display a warning message."""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

def display_info_message(message: str) -> None:
    """Display an information message."""
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

def display_loading_message(message: str) -> None:
    """Display a loading message."""
    print(f"{Fore.CYAN}⟳ {message}...{Style.RESET_ALL}")

# Enhanced animation functions
def display_loading_animation(message: str, duration: float = 2.0) -> None:
    """
    Display a loading animation with a message.
    
    Args:
        message: Message to display during loading
        duration: How long to show the animation in seconds
    """
    if HAS_YASPIN:
        # Use yaspin for a nice loading spinner
        with yaspin(Spinners.dots, text=f"{Fore.CYAN}{message}...{Style.RESET_ALL}") as sp:
            time.sleep(duration)
            sp.ok("✓")
    else:
        # Fallback to simple animation
        display_loading_message(message)
        time.sleep(duration)
        print(f"{Fore.GREEN}✓ Complete{Style.RESET_ALL}")

def display_typing_animation(text: str, delay: float = 0.03) -> None:
    """
    Display text with a typing animation effect.
    
    Args:
        text: Text to display
        delay: Delay between characters in seconds
    """
    if HAS_BLESSED and term:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    else:
        # Fallback if blessed is not available
        print(text)

def display_animated_menu(title: str, options: List[str], current_selection: Optional[int] = None) -> None:
    """
    Display a menu with options and optional animation.
    
    Args:
        title: The title of the menu
        options: List of options to display
        current_selection: Index of currently selected option (for highlighting)
    """
    display_section_header(title)
    
    if HAS_RICH:
        console = rich.console.Console()
        for i, option in enumerate(options, 1):
            if current_selection is not None and i-1 == current_selection:
                console.print(f"  [bold cyan]{i}. {option}[/bold cyan]")
            else:
                console.print(f"  {i}. {option}")
    else:
        # Fallback to standard formatted output
        for i, option in enumerate(options, 1):
            if current_selection is not None and i-1 == current_selection:
                print(f"  {Fore.CYAN}{Style.BRIGHT}{i}. {option}{Style.RESET_ALL}")
            else:
                print(f"  {i}. {option}")
    
    display_spacer()

# Compatibility function to match the original ascii_art.py interface
def display_menu(title: str, options: List[str], current_selection: Optional[int] = None) -> None:
    """
    Display a menu with options (compatibility function).
    
    Args:
        title: The title of the menu
        options: List of options to display
        current_selection: Index of currently selected option (for highlighting)
    """
    display_animated_menu(title, options, current_selection)

def display_data_table(headers: List[str], data: List[List[Any]], title: Optional[str] = None) -> None:
    """
    Display a formatted data table with enhanced formatting if available.
    
    Args:
        headers: The column headers
        data: List of rows, where each row is a list of values
        title: Title to display above the table
    """
    if title:
        display_info_message(title)
    
    if HAS_RICH:
        # Use Rich for enhanced tables
        console = rich.console.Console()
        table = rich.table.Table(show_header=True, header_style="bold cyan")
        
        # Add columns
        for header in headers:
            table.add_column(header)
        
        # Add rows
        for row in data:
            table.add_row(*[str(cell) for cell in row])
        
        # Print the table
        console.print(table)
    else:
        # Fallback to simple formatting
        if "tabulate" in sys.modules:
            from tabulate import tabulate
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            # Very basic table formatting
            print(" | ".join(headers))
            print("-" * (sum(len(h) for h in headers) + 3 * (len(headers) - 1)))
            for row in data:
                print(" | ".join(str(cell) for cell in row))
    
    display_spacer()

def display_progress_bar(value: float, total: float, width: int = 50, title: Optional[str] = None) -> None:
    """
    Display a progress bar.
    
    Args:
        value: Current value
        total: Maximum value
        width: Width of the progress bar
        title: Title to display above the progress bar
    """
    if title:
        print(title)
    
    percent = min(1.0, value / total) if total > 0 else 0
    filled_width = int(width * percent)
    
    bar = f"{Fore.GREEN}{'█' * filled_width}{Fore.WHITE}{'░' * (width - filled_width)}{Style.RESET_ALL}"
    percent_text = f"{Fore.CYAN}{percent * 100:.1f}%{Style.RESET_ALL}"
    
    print(f"{bar} {percent_text}")

def display_animated_progress_bar(value: float, total: float, width: int = 50, 
                                  title: Optional[str] = None, duration: float = 1.0,
                                  show_elapsed: bool = False) -> None:
    """
    Display an animated progress bar that fills up over time.
    
    Args:
        value: Current value
        total: Maximum value
        width: Width of the progress bar
        title: Title to display above the progress bar
        duration: Duration of the animation in seconds
        show_elapsed: Whether to show elapsed time
    """
    if HAS_RICH:
        # Use Rich for high-quality progress bars
        console = rich.console.Console()
        
        if title:
            console.print(title)
        
        final_percent = min(100.0, (value / total * 100)) if total > 0 else 0
        
        # Create a list of columns, removing None values
        columns = [
            rich.progress.TextColumn("[cyan]{task.description}"),
            rich.progress.BarColumn(),
            rich.progress.TextColumn("[magenta]{task.percentage:>3.0f}%")
        ]
        if show_elapsed:
            columns.append(rich.progress.TimeRemainingColumn())
        
        with rich.progress.Progress(*columns, console=console) as progress:
            task = progress.add_task("", total=100)
            
            start_time = time.time()
            while not progress.finished:
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    progress.update(task, completed=final_percent)
                    break
                else:
                    # Calculate how far we should be in the animation
                    current = min(final_percent, (elapsed / duration) * final_percent)
                    progress.update(task, completed=current)
                    time.sleep(0.05)  # Small update interval for smooth animation
    else:
        # Fallback to simple progress bar with steps
        if title:
            print(title)
        
        final_percent = min(1.0, value / total) if total > 0 else 0
        steps = 10  # Number of animation steps
        
        for i in range(steps + 1):
            # Clear the previous bar
            if i > 0 and not HAS_BLESSED:
                sys.stdout.write("\r")
            
            # Calculate current animation step percent
            current_percent = min(final_percent, final_percent * (i / steps))
            filled_width = int(width * current_percent)
            
            bar = f"{Fore.GREEN}{'█' * filled_width}{Fore.WHITE}{'░' * (width - filled_width)}{Style.RESET_ALL}"
            percent_text = f"{Fore.CYAN}{current_percent * 100:.1f}%{Style.RESET_ALL}"
            
            sys.stdout.write(f"{bar} {percent_text}")
            sys.stdout.flush()
            
            if i < steps:
                time.sleep(duration / steps)
        
        # End with a newline
        print()

def display_achievement_badge(achievement_type: str, level: int, description: str) -> None:
    """
    Display an animated achievement badge.
    
    Args:
        achievement_type: Type of achievement (distance, carbon, social, etc.)
        level: Level of the achievement (1-5)
        description: Text description of the achievement
    """
    # Badge frames for animation
    badge_frames = [
        f"  {Fore.YELLOW}★{Style.RESET_ALL}  ",
        f" {Fore.YELLOW}\\★/{Style.RESET_ALL} ",
        f"{Fore.YELLOW}==★=={Style.RESET_ALL}",
        f" {Fore.YELLOW}/★\\{Style.RESET_ALL} ",
        f"  {Fore.YELLOW}★{Style.RESET_ALL}  "
    ]
    
    # Badge levels
    level_colors = [
        Fore.WHITE,    # Level 1
        Fore.CYAN,     # Level 2
        Fore.GREEN,    # Level 3
        Fore.YELLOW,   # Level 4
        Fore.MAGENTA   # Level 5
    ]
    
    # Ensure level is in range
    level = max(1, min(5, level))
    level_color = level_colors[level-1]
    
    # Achievement type icons
    icons = {
        "distance": "🚲",
        "carbon": "🌱",
        "social": "🏆",
        "challenge": "🎯",
        "streak": "🔥",
        "default": "🎖️"
    }
    
    icon = icons.get(achievement_type.lower(), icons["default"])
    
    # Display animation
    if HAS_BLESSED and term:
        # Animated version with blessed
        print(f"\n{Fore.CYAN}NEW ACHIEVEMENT UNLOCKED!{Style.RESET_ALL}")
        print(f"{level_color}{icon} {description} {icon}{Style.RESET_ALL}")
        
        # Animate the badge
        for _ in range(3):  # Three animation cycles
            for frame in badge_frames:
                # Clear previous frame
                sys.stdout.write("\r" + " " * terminal_width + "\r")
                sys.stdout.flush()
                
                # Print level stars
                stars = "★" * level
                sys.stdout.write(f"{frame} {level_color}{stars}{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(0.1)
        
        # Final badge
        sys.stdout.write("\r" + " " * terminal_width + "\r")
        sys.stdout.flush()
        print(f"{level_color}{icon} {'★' * level} {description} {'★' * level} {icon}{Style.RESET_ALL}")
    else:
        # Static version without animation
        print(f"\n{Fore.CYAN}NEW ACHIEVEMENT UNLOCKED!{Style.RESET_ALL}")
        print(f"{level_color}{icon} {'★' * level} {description} {'★' * level} {icon}{Style.RESET_ALL}")
    
    print()

def display_mascot_animation(message: str) -> None:
    """
    Display an eco-mascot with a message.
    
    Args:
        message: Message for the mascot to display
    """
    mascot_frames = [
        f"{Fore.GREEN}  o/  {Style.RESET_ALL}",
        f"{Fore.GREEN} /|   {Style.RESET_ALL}",
        f"{Fore.GREEN}  |\\  {Style.RESET_ALL}",
        f"{Fore.GREEN}  /|  {Style.RESET_ALL}",
        f"{Fore.GREEN}  |\\  {Style.RESET_ALL}"
    ]
    
    bike_frames = [
        f"{Fore.CYAN} _o  {Style.RESET_ALL}",
        f"{Fore.CYAN} /\\_ {Style.RESET_ALL}",
        f"{Fore.CYAN} -O- {Style.RESET_ALL}",
        f"{Fore.CYAN} _/\\ {Style.RESET_ALL}",
        f"{Fore.CYAN} O_  {Style.RESET_ALL}"
    ]
    
    if HAS_BLESSED and term:
        # Animated version
        print(f"\n{Fore.GREEN}EcoCycle Mascot:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
        
        for _ in range(2):  # Two animation cycles
            for i in range(len(mascot_frames)):
                # Clear previous frame
                sys.stdout.write("\r" + " " * terminal_width + "\r")
                sys.stdout.flush()
                
                # Print mascot and bike
                sys.stdout.write(f"{mascot_frames[i]} {bike_frames[i]}")
                sys.stdout.flush()
                time.sleep(0.2)
        
        # Final state
        sys.stdout.write("\r" + " " * terminal_width + "\r")
        print(f"{Fore.GREEN}  o/  {Fore.CYAN} _o   {Fore.GREEN}EcoCycle!{Style.RESET_ALL}")
    else:
        # Static version
        print(f"\n{Fore.GREEN}EcoCycle Mascot:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  o/  {Fore.CYAN} _o   {Fore.GREEN}EcoCycle!{Style.RESET_ALL}")
    
    print()

def create_social_share_graphic(username: str, title: str, stats: Dict[str, Any]) -> str:
    """
    Create a social media share graphic using ASCII art.
    
    Args:
        username: Username to display
        title: Title of the achievement/share
        stats: Dictionary of stats to display
    
    Returns:
        The social share graphic as a multi-line string
    """
    # Border style options
    border_styles = {
        "single": {"tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│"},
        "double": {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"},
        "rounded": {"tl": "╭", "tr": "╮", "bl": "╰", "br": "╯", "h": "─", "v": "│"},
    }
    
    # Choose a border style
    border = border_styles["rounded"]
    
    # Calculate card dimensions
    width = min(50, terminal_width - 4)
    
    # Generate header
    header = f" {username} - {title} "
    header = header.center(width - 2)
    
    # Generate separator
    separator = border["h"] * (width - 2)
    
    # Build the card content
    lines = []
    lines.append(f"{border['tl']}{border['h'] * (width - 2)}{border['tr']}")
    lines.append(f"{border['v']}{header}{border['v']}")
    lines.append(f"{border['v']}{separator}{border['v']}")
    
    # Add stats
    for key, value in stats.items():
        stat_line = f" {key}: {value} "
        stat_line = stat_line.ljust(width - 2)
        lines.append(f"{border['v']}{stat_line}{border['v']}")
    
    # Add footer
    lines.append(f"{border['v']}{separator}{border['v']}")
    date_line = f" {time.strftime('%Y-%m-%d')} | EcoCycle "
    date_line = date_line.rjust(width - 2)
    lines.append(f"{border['v']}{date_line}{border['v']}")
    lines.append(f"{border['bl']}{border['h'] * (width - 2)}{border['br']}")
    
    # Combine into a single string
    graphic = "\n".join(lines)
    
    # Display the card with a "share" animation if supported
    if HAS_RICH:
        console = rich.console.Console()
        text = rich.text.Text(graphic)
        panel = rich.panel.Panel(
            text,
            title=f"[bold green]Share Your Achievement![/bold green]",
            subtitle="[cyan]EcoCycle - Cycle into a greener tomorrow[/cyan]"
        )
        console.print(panel)
    else:
        # Simple display
        print(f"{Fore.GREEN}Share Your Achievement!{Style.RESET_ALL}")
        print(graphic)
        print(f"{Fore.CYAN}EcoCycle - Cycle into a greener tomorrow{Style.RESET_ALL}")
    
    return graphic

def animate_route_on_map(points=None):
    """
    Display an ASCII art map with an animated cycling route.
    
    Args:
        points: Optional list of map points to animate through
                If None, a default route will be used
    """
    # Default simple ASCII map
    ascii_map = [
        "╭───────────────────────────────╮",
        "│                               │",
        "│    ┌─────┐                    │",
        "│    │     │   ┌────┐          │",
        "│    └─────┘   │    │          │",
        "│              └────┘          │",
        "│                              │",
        "│         ┌──────────┐         │",
        "│         │          │         │",
        "│   ┌─────┘          └────┐    │",
        "│   │                     │    │",
        "│   │                     │    │",
        "│   └─────────────────────┘    │",
        "│                              │",
        "╰──────────────────────────────╯"
    ]
    
    # Default route coordinates (x, y) where y is line index, x is character position
    default_route = [
        (5, 2), (5, 3), (5, 4), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
        (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 5), (15, 6),
        (15, 7), (15, 8), (15, 9), (15, 10), (15, 11), (15, 12),
        (16, 12), (17, 12), (18, 12), (19, 12), (20, 12), (21, 12),
        (22, 12), (23, 12), (24, 12), (25, 12), (26, 12)
    ]
    
    route = points if points else default_route
    
    if HAS_BLESSED and term:
        # Animate the route using blessed
        print(f"{Fore.CYAN}Cycling Route:{Style.RESET_ALL}")
        
        # First, print the map
        for line in ascii_map:
            print(line)
        
        # Animate the cyclist along the route
        cyclist_chars = ["🚲", "🚴", "🚵"]
        
        for i, (x, y) in enumerate(route):
            # Position cursor and print cyclist
            with term.location(x, y + 1):  # +1 for the header line
                sys.stdout.write(f"{Fore.GREEN}{cyclist_chars[i % len(cyclist_chars)]}{Style.RESET_ALL}")
                sys.stdout.flush()
            
            # If not the first point, mark the previous point as part of the path
            if i > 0:
                prev_x, prev_y = route[i-1]
                with term.location(prev_x, prev_y + 1):
                    sys.stdout.write(f"{Fore.CYAN}·{Style.RESET_ALL}")
                    sys.stdout.flush()
            
            time.sleep(0.1)
        
        # End with newlines to move cursor past the map
        print("\n" * 2)
    else:
        # Static version that prints the map with the route
        print(f"{Fore.CYAN}Cycling Route:{Style.RESET_ALL}")
        
        # Create a copy of the map to modify
        route_map = ascii_map.copy()
        
        # Add route markers
        for i, (x, y) in enumerate(route):
            # Make sure we don't go out of bounds
            if 0 <= y < len(route_map) and 0 <= x < len(route_map[y]):
                # Convert the line to a list for modification
                line = list(route_map[y])
                
                # Add route marker
                if i == len(route) - 1:
                    line[x] = f"{Fore.GREEN}X{Style.RESET_ALL}"  # Destination
                elif i == 0:
                    line[x] = f"{Fore.GREEN}O{Style.RESET_ALL}"  # Start
                else:
                    line[x] = f"{Fore.CYAN}·{Style.RESET_ALL}"  # Route point
                
                # Convert back to string
                route_map[y] = ''.join(line)
        
        # Print the map with the route
        for line in route_map:
            print(line)
        
        print()

# Main function to demonstrate the module
def main():
    """Demonstrate the enhanced ASCII art module."""
    clear_screen()
    display_header()
    
    display_section_header("Enhanced ASCII Art Demo")
    
    display_info_message("This module provides enhanced ASCII art with animations")
    display_success_message("Successfully loaded the module")
    display_warning_message("Remember to have the required dependencies installed for all features")
    
    # Test loading animation
    display_loading_animation("Loading demo features", 1.0)
    
    # Test animated menu
    options = ["View Statistics", "Log Cycling Trip", "Calculate Carbon Footprint"]
    display_animated_menu("Main Menu", options, 1)
    
    # Test progress bar
    display_animated_progress_bar(75, 100, 40, "Carbon Savings Progress", 1.5)
    
    # Test achievement badge
    display_achievement_badge("distance", 3, "100 km Milestone")
    
    # Test mascot
    display_mascot_animation("Remember to cycle safely and wear a helmet!")
    
    # Test social share
    create_social_share_graphic(
        "EcoCyclist",
        "Weekly Challenge Completed",
        {
            "Distance": "42.5 km",
            "CO2 Saved": "8.2 kg",
            "Calories Burned": "1250",
            "Achievements": "3 new badges"
        }
    )
    
    # Test route animation
    animate_route_on_map()
    
    display_info_message("Demo completed successfully!")

if __name__ == "__main__":
    main()