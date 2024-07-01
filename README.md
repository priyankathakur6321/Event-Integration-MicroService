# Event Integration Microservice

This microservice integrates with an external provider's API to fetch events and exposes an endpoint to filter events based on time range. It is developed using Python and Flask.

## Overview

This microservice fetches event data from an external provider's API, stores the data locally, and exposes an API endpoint to retrieve events within a specified time range (`starts_at` to `ends_at`). Events are fetched periodically to ensure up-to-date data availability.

## Setup

### Prerequisites

- Python 3.x installed on your machine.
- `pip` package manager to install Python dependencies.
- Internet access to fetch data from the external provider's API.

### Installation

1. Clone the repository:

   ```
   git clone <repository_url>
   cd <your_dir>

2.  Install dependencies:

    ````
    pip install -r requirements.txt
    ````
    
## Usage

### Running the Application

1.  Start the Flask application:

    ````
    python main.py
    ````
    This will start the Flask development server.

2.  The application will start fetching events from the external provider\'s API periodically in a separate thread.

### Accessing the API

Once the application is running, you can access the API endpoint to
retrieve events within a specified time range.

Example using curl:

```
curl -X GET 'http://localhost:5000/events?starts_at=2023-01-01T00:00:00&ends_at=2023-12-31T23:59:59\'
```
Replace http://localhost:5000 with your actual server URL if deploying
elsewhere.

## API Documentation

### GET  `/events`

Retrieves events within the specified time range.

**Parameters:**

-   starts_at: Start date and time (ISO format: YYYY-MM-DDTHH:MM:SS)

-   ends_at: End date and time (ISO format: YYYY-MM-DDTHH:MM:SS)

**Response:**

-   JSON array of events matching the specified time range.

Example response:


```
[
  {
    "base_event_id": "291",
    "event_end_date": "2021-06-30T22:00:00",
    "event_start_date": "2021-06-30T21:00:00",
    "title": "Camela en concierto"
  }
]
```
## OR
```
[
  {
    "base_event_id": "322",
    "event_end_date": "2021-02-10T21:30:00",
    "event_start_date": "2021-02-10T20:00:00",
    "title": "Pantomima Full"
  }
]
```

