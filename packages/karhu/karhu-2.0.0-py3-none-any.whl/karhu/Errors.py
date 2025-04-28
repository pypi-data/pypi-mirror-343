import re
from termcolor import colored
import traceback


class Errors:
    """
    A class to handle errors and exceptions in the application.
    """
    def format_rate_limit_error(error_message):
        """Format rate limit error with human-readable time."""

        # Extract seconds from error message
        wait_time_match = re.search(r'Please wait (\d+) seconds', str(error_message))
        
        if not wait_time_match:
            return f"Rate limit exceeded. Please try again later."
        
        wait_seconds = int(wait_time_match.group(1))
        
        # Convert to human-readable format
        hours, remainder = divmod(wait_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        time_parts = []
        if hours > 0:
            time_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            time_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds > 0 and not (hours > 0 and minutes > 0):  # Only show seconds if we don't have both hours and minutes
            time_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
        
        wait_time_formatted = " and ".join(time_parts)
        
        return f"Rate limit exceeded. Please wait {wait_time_formatted} before trying again."


    """
    A class to handle error logging and formatting.
    """
    @staticmethod
    def log_error(error_message, exception=None):
        """
        Log and format error messages.

        Args:
            error_message (str): A custom error message.
            exception (Exception, optional): The exception object to log.
        """
        print(colored(f"\n[Error] {error_message}", "red"))
        if exception:
            print(colored(f"Details: {str(exception)}", "yellow"))
            # print(colored(traceback.format_exc(), "yellow"))

    @staticmethod
    def handle_error(error_message, exception=None):
        """
        Handle errors by logging and optionally raising them.

        Args:
            error_message (str): A custom error message.
            exception (Exception, optional): The exception object to log.
        """
        Errors.log_error(error_message, exception)
        
        # Optionally, you can re-raise the exception if needed
        # raise exception
