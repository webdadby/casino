from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Supabase client
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

ROULETTE_COLORS = {
    0: "green",
    1: "red", 2: "black", 3: "red", 4: "black", 5: "red", 6: "black", 7: "red", 8: "black",
    9: "red", 10: "black", 11: "black", 12: "red", 13: "black", 14: "red", 15: "black",
    16: "red", 17: "black", 18: "red", 19: "red", 20: "black", 21: "red", 22: "black",
    23: "red", 24: "black", 25: "red", 26: "black", 27: "red", 28: "black", 29: "black",
    30: "red", 31: "black", 32: "red", 33: "black", 34: "red", 35: "black", 36: "red"
}

def save_number(number):
    """Save a number to the database"""
    try:
        print(f"Trying to save number: {number}")
        color = ROULETTE_COLORS.get(number)
        print(f"Color for number {number}: {color}")
        
        data = supabase.table('roulette_numbers').insert({
            "number": number,
            "color": color
        }).execute()
        
        print(f"Save response: {data}")
        return True
    except Exception as e:
        print(f"Error saving number: {e}")
        print(f"Error type: {type(e)}")
        return False

def get_last_numbers(limit=50):
    """Get the last N numbers from the database"""
    try:
        print(f"Getting last {limit} numbers from database")
        response = supabase.table('roulette_numbers')\
            .select('*')\
            .order('id', desc=True)\
            .limit(limit)\
            .execute()
        
        if response and response.data:
            print(f"Raw database response: {response.data}")
            return response.data
        else:
            print("No numbers found in database")
            return []
    except Exception as e:
        print(f"Error getting last numbers: {e}")
        print(f"Error type: {type(e)}")
        return []
