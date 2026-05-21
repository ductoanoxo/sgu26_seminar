import sys
import os

# Add the service directory to sys.path
service_dir = "/home/traductoan/Seminar_Final/services/nl2sql-service"
sys.path.append(service_dir)

# Set the working directory to the service dir so it finds .env
os.chdir(service_dir)

try:
    from core.config import get_settings
    settings = get_settings()
    print("Settings loaded successfully!")
    print(f"GEMINI_API_KEY: {settings.GEMINI_API_KEY[:5]}...")
    print(f"GEMINI_KEYS: {settings.GEMINI_KEYS}")
    
    # Test validator with a plain string
    print("\nTesting validator with manual environment override...")
    os.environ["GEMINI_KEYS"] = "key1, key2"
    # Need to clear cache or re-instantiate
    from core.config import Settings
    s2 = Settings()
    print(f"Parsed GEMINI_KEYS from 'key1, key2': {s2.GEMINI_KEYS}")
    
    os.environ["GEMINI_KEYS"] = '["key3", "key4"]'
    s3 = Settings()
    print(f"Parsed GEMINI_KEYS from '[\"key3\", \"key4\"]': {s3.GEMINI_KEYS}")

except Exception as e:
    print(f"Error loading settings: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
