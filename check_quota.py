"""Check Gemini API quota status"""
import os
import sys
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

# Load environment
load_dotenv('backend/.env')
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print('ERROR: GEMINI_API_KEY not found in backend/.env')
    sys.exit(1)

print(f'✅ API Key loaded: {api_key[:15]}...\n')

try:
    from google import genai
    
    # Initialize client
    client = genai.Client(api_key=api_key)
    
    # First, list available models
    print('📋 Available models:')
    try:
        models = client.models.list()
        for model in models:
            print(f'  • {model.name}')
        print()
    except Exception as e:
        print(f'  Could not list models: {e}\n')
    
    # Make a minimal test call (using gemini-3.6-flash from your ai_service.py)
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents='Say OK'
    )
    
    print('✅ GEMINI API IS WORKING!')
    print(f'Response: {response.text[:50]}\n')
    print('📊 Your Quota Status: ACTIVE ✓\n')
    print('Free Tier Limits (Gemini 3.6 Flash):')
    print('  • 15 requests per minute')
    print('  • 1 million tokens per minute')
    print('  • 1,500 requests per day\n')
    
    # Calculate time until daily reset
    pt_tz = pytz.timezone('America/Los_Angeles')
    now_pt = datetime.now(pt_tz)
    midnight_pt = (now_pt + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time_diff = midnight_pt - now_pt
    hours = int(time_diff.total_seconds() // 3600)
    minutes = int((time_diff.total_seconds() % 3600) // 60)
    
    print('⏰ Daily Quota Reset:')
    print(f'  Current time (PT): {now_pt.strftime("%H:%M:%S")}')
    print(f'  Resets at: Midnight Pacific Time (00:00 PT)')
    print(f'  Time until reset: {hours} hours {minutes} minutes\n')
    print('📈 Check detailed usage: https://aistudio.google.com/apikey')
    
except Exception as e:
    error_msg = str(e)
    print(f'❌ API ERROR: {error_msg}\n')
    
    if '429' in error_msg or 'quota' in error_msg.lower() or 'resource_exhausted' in error_msg.lower():
        print('⚠️  QUOTA EXCEEDED\n')
        pt_tz = pytz.timezone('America/Los_Angeles')
        now_pt = datetime.now(pt_tz)
        midnight_pt = (now_pt + timedelta(days=1)).replace(hour=0, minute=0, second=0)
        time_diff = midnight_pt - now_pt
        hours = int(time_diff.total_seconds() // 3600)
        minutes = int((time_diff.total_seconds() % 3600) // 60)
        
        print(f'⏰ Daily quota resets in: {hours} hours {minutes} minutes')
        print('   Reset time: Midnight Pacific Time (00:00 PT)\n')
        print('💡 Options:')
        print('  1. Wait for daily reset')
        print('  2. Upgrade to paid tier: https://ai.google.dev/pricing')
        print('  3. Use a different API key')
    elif '401' in error_msg or 'invalid' in error_msg.lower():
        print('❌ Invalid API key')
        print('Get a new key: https://aistudio.google.com/apikey')
    elif '403' in error_msg:
        print('❌ API access forbidden')
        print('Check your Google Cloud project settings')
