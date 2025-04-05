import requests
import json

TOKEN = "6BUN2E52FMXELO5GFO4P"  # Replace with your valid API token
EVENT_IDS = ["1249049413419","1198120172689","1115886609889","1242209625429","140043603187","1258012141179","955125936387","1257753337089","1199613940589","1260409040369","97765875365","1216160933089","1105445730939","1232817543459","1281132314239","1245862029869","1276556688419","789210799747","1227454713089","1044740435767"]

def fetch_event_details(event_id):
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            event = response.json()
            
            # Fetch Organizer Details
            organizer_id = event.get('organizer_id', 'N/A')
            organizer_name = "N/A"
            if organizer_id != 'N/A':
                organizer_url = f"https://www.eventbriteapi.com/v3/organizers/{organizer_id}/"
                organizer_response = requests.get(organizer_url, headers=headers)
                if organizer_response.status_code == 200:
                    organizer_data = organizer_response.json()
                    organizer_name = organizer_data.get("name", "N/A")
            
            # Fetch Venue Details
            venue_id = event.get('venue_id', None)
            venue_details = "N/A"
            if venue_id:
                venue_url = f"https://www.eventbriteapi.com/v3/venues/{venue_id}/"
                venue_response = requests.get(venue_url, headers=headers)
                if venue_response.status_code == 200:
                    venue_data = venue_response.json()
                    venue_details = f"{venue_data.get('name', 'N/A')}, {venue_data.get('address', {}).get('localized_address_display', 'N/A')}"

            print("\n Event Details:")
            print(f" Name: {event.get('name', {}).get('text', 'N/A')}")
            print(f" ID: {event.get('id', 'N/A')}")
            print(f" Start: {event.get('start', {}).get('local', 'N/A')}")
            print(f" End: {event.get('end', {}).get('local', 'N/A')}")
            print(f" Location: {venue_details}")
            print(f" Organizer: {organizer_name}")
            print(f" URL: {event.get('url', 'N/A')}")
            print(f" Description: {event.get('description', {}).get('text', 'N/A')}")
            logo = event.get('logo')
            image_url = logo.get('original', {}).get('url', 'N/A') if logo else 'N/A'
            print(f" Image: {image_url}\n")

        
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON response for Event ID {event_id}.")
    else:
        print(f"Error fetching Event ID {event_id}: {response.status_code} {response.text}")

# Fetch details for all event IDs
for event_id in EVENT_IDS:
    fetch_event_details(event_id)
