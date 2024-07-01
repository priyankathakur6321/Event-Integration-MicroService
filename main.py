import threading
import time
import requests
from flask import Flask, request, jsonify
from datetime import datetime
from xml.etree import ElementTree as ET

app = Flask(__name__)

# Global dictionary to store event data
events_data = {}

# External provider URL
provider_url = "https://provider.code-challenge.feverup.com/api/events"


# Fetch data from the external provider and store in events_data
def fetch_events_from_provider():
    try:
        response = requests.get(provider_url)
        if response.status_code == 200:
            parse_events_from_xml(response.text)
        else:
            print(f"Failed to fetch events from provider. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events from provider: {e}")


# Parse XML response and store relevant event data
def parse_events_from_xml(xml_text):
    try:
        root = ET.fromstring(xml_text)
        for base_event in root.findall('.//base_event'):
            base_event_id = base_event.get('base_event_id')
            sell_mode = base_event.get('sell_mode')
            if sell_mode == 'online':
                event_elem = base_event.find('.//event')
                if event_elem is not None:
                    event_start_date_str = event_elem.get('event_start_date')
                    event_end_date_str = event_elem.get('event_end_date')
                    event_start_date = datetime.strptime(event_start_date_str, "%Y-%m-%dT%H:%M:%S")
                    event_end_date = datetime.strptime(event_end_date_str, "%Y-%m-%dT%H:%M:%S")

                    events_data[base_event_id] = {
                        'title': base_event.get('title'),
                        'event_start_date': event_start_date,
                        'event_end_date': event_end_date
                    }
                else:
                    print(f"No event element found for base_event_id={base_event_id}")
            else:
                print(f"Skipping base_event_id={base_event_id} with sell_mode={sell_mode}")
    except Exception as e:
        print(f"Error parsing XML: {e}")


# Endpoint to fetch events within a specified time range
@app.route('/events', methods=['GET'])
def get_events():
    starts_at_str = request.args.get('starts_at')
    ends_at_str = request.args.get('ends_at')

    if not starts_at_str or not ends_at_str:
        return jsonify({'error': 'Please provide starts_at and ends_at parameters in ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

    try:
        starts_at = datetime.fromisoformat(starts_at_str)
        ends_at = datetime.fromisoformat(ends_at_str)
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

    filtered_events = []
    for event_id, event_details in events_data.items():
        event_start_date = event_details['event_start_date']
        event_end_date = event_details['event_end_date']

        # Check if event overlaps with the specified time range
        if starts_at <= event_end_date and ends_at >= event_start_date:
            filtered_events.append({
                'base_event_id': event_id,
                'title': event_details['title'],
                'event_start_date': event_start_date.isoformat(),
                'event_end_date': event_end_date.isoformat()
            })

    return jsonify(filtered_events)


# Function to fetch events periodically
def periodic_fetch():
    while True:
        fetch_events_from_provider()
        print(f'Fetching events... {len(events_data)}')
        time.sleep(5)  # Sleep for 5 minutes


if __name__ == '__main__':
    # Start the periodic fetching in a separate thread
    thread = threading.Thread(target=periodic_fetch)
    thread.start()

    # Run the Flask app
    app.run(debug=True)
