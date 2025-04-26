# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# API configuration
API_KEY = None
NERD_COMPUTE_ENDPOINT = "https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute"
DEBUG_MODE = False

def set_nerd_compute_api_key(api_key):
    """Set the API key programmatically."""
    global API_KEY
    API_KEY = api_key

def set_debug_mode(debug_mode):
    """Enable or disable debug mode."""
    global DEBUG_MODE
    DEBUG_MODE = debug_mode