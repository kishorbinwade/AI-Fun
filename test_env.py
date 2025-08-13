from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Test if the API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"✅ API Key loaded successfully!")
    print(f"Key starts with: {api_key[:10]}...")
    print(f"Key length: {len(api_key)} characters")
else:
    print("❌ API Key not found!")
    
print(f"Environment: {os.getenv('ENVIRONMENT', 'Not found')}")
print(f"Debug: {os.getenv('DEBUG', 'Not found')}")

