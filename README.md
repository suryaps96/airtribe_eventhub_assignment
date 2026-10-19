# EventHub – Event Management API

EventHub is a REST API built with Django REST Framework for managing events and reservations. It supports event management, reservation tracking, seat availability, and reservation cancellation.

## Features

- Create, retrieve, update, and delete events.
- Filter events by status and venue.
- Create and view reservations, with filtering by event.
- Automatically update seat availability when reservations are created or cancelled.
- Validate reservation requests to prevent invalid bookings.
- Cancel reservations through a dedicated API endpoint.
- Log request methods, paths, response status codes, and processing times using custom middleware.

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite (default Django database)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/suryaps96/airtribe_eventhub_assignment
cd airtribe_eventhub_assignment
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install django djangorestframework
```

If the project includes a `requirements.txt`, use:

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET, POST | `/api/events/` | List and create events |
| GET, PUT, PATCH, DELETE | `/api/events/<id>/` | Retrieve, update, or delete an event |
| GET, POST | `/api/reservations/` | List and create reservations |
| GET, PUT, PATCH, DELETE | `/api/reservations/<id>/` | Retrieve, update, or delete a reservation |
| POST | `/api/reservations/<id>/cancel/` | Cancel a reservation |

### Filtering

Events can be filtered by status or venue:

```text
/api/events/?status=upcoming
/api/events/?venue=Chennai
/api/events/?status=upcoming&venue=Chennai
```

Reservations can be filtered by event:

```text
/api/reservations/?event_id=1
```

## Design Decision

### Dedicated Reservation Cancellation Endpoint

I implemented reservation cancellation as a dedicated `POST /api/reservations/<id>/cancel/` endpoint instead of treating cancellation as a regular update.

This keeps the business logic explicit: cancelling a reservation restores the reserved seats to the associated event. The endpoint also checks whether the reservation has already been cancelled, preventing the same seats from being restored more than once.

I chose this approach to make the API easier to understand and help maintain consistency between reservation status and event seat availability.

## Validation and Seat Management

- Reservations must request at least one seat.
- Reservations are only allowed for eligible events with sufficient available seats.
- Available seats decrease when a reservation is created.
- Available seats are restored when a reservation is cancelled.
- Repeated cancellation is rejected to prevent incorrect seat counts.
- Event seat availability is validated against total capacity.

## Testing

The API was tested using Postman, covering:

- Event and reservation CRUD operations.
- Filtering by event status, venue, and event ID.
- Reservation validation and seat availability.
- Reservation cancellation and repeated cancellation.
- Invalid resource IDs and error responses.

Django's system check can be run with:

```bash
python manage.py check
```

---

Built as a backend project to practise Django REST Framework, REST API design, serializers, validation, custom ViewSet actions, and middleware.
e
