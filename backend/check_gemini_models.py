"""
Check available Gemini models and their status
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"Using API Key: {api_key[:20]}...")

genai.configure(api_key=api_key)

print("\n=== Available Gemini Models ===\n")

try:
    # List all available models
    models = genai.list_models()
    
    vision_models = []
    for model in models:
        # Check if model supports vision (generateContent with images)
        if 'generateContent' in model.supported_generation_methods:
            vision_models.append(model.name)
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print(f"  Methods: {model.supported_generation_methods}")
            print()
    
    if not vision_models:
        print("❌ No vision-capable models found!")
    else:
        print(f"\n=== Testing Vision Models ===\n")
        
        # Test each vision model
        for model_name in vision_models[:3]:  # Test first 3
            print(f"\nTesting {model_name}...")
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say 'Hello' if you're working")
                print(f"✓ {model_name} is working!")
                print(f"  Response: {response.text[:50]}...")
            except Exception as e:
                print(f"✗ {model_name} failed: {str(e)}")
                
except Exception as e:
    print(f"Error listing models: {str(e)}")
    print("\nTrying direct model access...")
    
    # Try specific models directly
    test_models = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.0-flash-exp",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro",
        "models/gemini-2.0-flash-exp"
    ]
    
    for model_name in test_models:
        print(f"\nTesting {model_name}...")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'OK' if working")
            print(f"✓ {model_name} works!")
            print(f"  Response: {response.text[:50]}")
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg:
                print(f"✗ {model_name}: 503 Service Unavailable (high demand)")
            elif "404" in error_msg:
                print(f"✗ {model_name}: 404 Not Found")
            elif "429" in error_msg:
                print(f"✗ {model_name}: 429 Quota Exceeded")
            else:
                print(f"✗ {model_name}: {error_msg[:100]}")
