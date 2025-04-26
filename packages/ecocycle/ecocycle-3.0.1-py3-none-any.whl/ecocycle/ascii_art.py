"""
EcoCycle - ASCII Art Module
Contains the ASCII art for the application header and other decorative elements.
"""
import os
import sys
import platform
import shutil
import time
import random
import threading
from typing import List, Optional, Any, Dict, Tuple, Callable

# Try to import colorama for cross-platform terminal colors
try:
    from colorama import Fore, Style, init
    init()
    COLOR_AVAILABLE = True
except ImportError:
    COLOR_AVAILABLE = False
    
    # Create dummy color classes for when colorama is not available
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

# Try to import rich for fancy progress bars and tables
try:
    import rich.progress
    from rich.console import Console
    from rich.panel import Panel
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

# Try to import blessed for terminal animations
try:
    import blessed
    BLESSED_AVAILABLE = True
    term = blessed.Terminal()
except ImportError:
    BLESSED_AVAILABLE = False
    term = None

# Try to import yaspin for spinners
try:
    from yaspin import yaspin
    from yaspin.spinners import Spinners
    YASPIN_AVAILABLE = True
except ImportError:
    YASPIN_AVAILABLE = False


def display_header() -> None:
    """Display the ASCII art header for EcoCycle."""
    header = rf"""
{Fore.GREEN}{Style.BRIGHT}
 ______     ______     ______     ______     __  __     ______     __         ______    
/\  ___\   /\  ___\   /\  __ \   /\  ___\   /\ \_\ \   /\  ___\   /\ \       /\  ___\   
\ \  __\   \ \ \____  \ \ \/\ \  \ \ \____  \ \____ \  \ \ \____  \ \ \____  \ \  __\   
 \ \_____\  \ \_____\  \ \_____\  \ \_____\  \/\_____\  \ \_____\  \ \_____\  \ \_____\ 
  \/_____/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/ 
                                                                                                   
{Fore.BLUE}Cycle into a greener tomorrow{Style.RESET_ALL}"""
    
    terminal_width = shutil.get_terminal_size().columns
    print(header)
    print(f"{Fore.CYAN}{'-' * terminal_width}{Style.RESET_ALL}")


def clear_screen() -> None:
    """Clear the terminal screen in a cross-platform way. """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def display_section_header(title: str) -> None:
    """Display a section header with a title."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {title} ==={Style.RESET_ALL}\n")


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
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def display_loading_message(message: str) -> None:
    """Display a loading message."""
    if RICH_AVAILABLE:
        with rich.progress.Progress(
            "[progress.description]{task.description}",
            rich.progress.BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            transient=True
        ) as progress:
            task = progress.add_task(f"[cyan]{message}[/cyan]", total=100)
            while not progress.finished:
                progress.update(task, advance=0.9)
                time.sleep(0.01)
    else:
        print(f"{Fore.BLUE}{message}...{Style.RESET_ALL}")
        # Simple ASCII spinner fallback
        for _ in range(10):
            for c in "|/-\\":
                sys.stdout.write(f"\r{message}... {c}")
                sys.stdout.flush()
                time.sleep(0.1)
        print()


def display_menu(title: str, options: List[str], current_selection: Optional[int] = None) -> None:
    """
    Display a menu with options.
    
    Args:
        title (str): The title of the menu
        options (list): List of options to display
        current_selection (int, optional): Index of currently selected option (for highlighting)
    """
    display_section_header(title)
    
    # Display "0. Exit" option first
    print(f"  {Fore.YELLOW}0. Exit{Style.RESET_ALL}")
    
    for i, option in enumerate(options):
        if i == current_selection:
            print(f"{Fore.GREEN}{Style.BRIGHT}> {i + 1}. {option}{Style.RESET_ALL}")
        else:
            print(f"  {i + 1}. {option}")
    
    print()


def display_data_table(headers: List[str], data: List[List[Any]], title: Optional[str] = None) -> None:
    """
    Display a formatted data table.
    
    Args:
        headers (list): The column headers
        data (list): List of rows, where each row is a list of values
        title (str, optional): Title to display above the table
    """
    if RICH_AVAILABLE:
        try:
            from rich.console import Console
            from rich.table import Table
            
            console = Console()
            table = Table(title=title)
            
            # Add columns
            for header in headers:
                table.add_column(header, style="cyan")
            
            # Add rows
            for row in data:
                table.add_row(*[str(cell) for cell in row])
            
            console.print(table)
            return
        except ImportError:
            # Fall back to simple table if rich isn't fully available
            pass
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print title if provided
    if title:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
    
    # Print headers
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(f"{Fore.CYAN}{Style.BRIGHT}{header_row}{Style.RESET_ALL}")
    
    # Print separator
    separator = "-+-".join("-" * w for w in col_widths)
    print(separator)
    
    # Print data rows
    for row in data:
        row_str = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(row_str)
    
    print()


def display_progress_bar(value: float, total: float, width: int = 50, title: Optional[str] = None) -> None:
    """
    Display a progress bar.
    
    Args:
        value (float): Current value
        total (float): Maximum value
        width (int): Width of the progress bar
        title (str, optional): Title to display above the progress bar
    """
    if RICH_AVAILABLE:
        try:
            import rich.progress
            
            # Create a Rich progress bar that will disappear after completion
            with rich.progress.Progress(
                "[progress.description]{task.description}",
                rich.progress.BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                "[progress.completed]/{task.total}",
                transient=True
            ) as progress:
                task = progress.add_task(f"[cyan]{title or 'Progress'}[/cyan]", total=total)
                progress.update(task, completed=value)
                time.sleep(0.5)  # Give a moment to see the progress
            return
        except ImportError:
            # Fall back to simple progress bar if rich isn't fully available
            pass
    
    # Calculate percentage and number of filled blocks
    percentage = min(100, int(100 * value / total))
    filled_blocks = int(width * value / total)
    
    # If title is provided, display it
    if title:
        print(f"{title}: ", end="")
    
    # Create the progress bar string
    bar = f"{Fore.GREEN}{'█' * filled_blocks}{Fore.WHITE}{'░' * (width - filled_blocks)}{Style.RESET_ALL}"
    
    # Display the progress bar with percentage
    print(f"{bar} {percentage}% ({value:.1f}/{total:.1f})")


if __name__ == "__main__":
    # Test ASCII art functions
    clear_screen()
    display_header()
    
    display_section_header("Menu Test")
    options = ["Log a cycling trip", "View statistics", "Environmental impact", "Settings", "Exit"]
    display_menu("Main Menu", options, 2)
    
    display_section_header("Message Types")
    display_success_message("Operation completed successfully")
    display_error_message("Something went wrong")
    display_warning_message("This action may take a while")
    display_info_message("The system is ready")
    
    display_section_header("Loading Animation")
    display_loading_message("Loading data")
    
    display_section_header("Progress Bar")
    display_progress_bar(75, 100, title="Download Progress")
    
    display_section_header("Data Table")
    headers = ["Date", "Distance (km)", "CO2 Saved (kg)", "Calories"]
    data = [
        ["2023-04-10", 12.5, 2.88, 450],
        ["2023-04-11", 8.3, 1.91, 350],
        ["2023-04-12", 15.2, 3.50, 560],
        ["2023-04-13", 5.7, 1.31, 220]
    ]
    display_data_table(headers, data, "Recent Cycling Activities")