from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to find an event by ID
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

# GET / - Serve a JSON welcome message
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Events API"}), 200

# GET /events - Return all events as a JSON array
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    
    # Validate that title is provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Generate new ID (max ID + 1)
    new_id = max([event.id for event in events], default=0) + 1
    
    # Create new event
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<int:event_id> - Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    
    # Find the event by ID
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Validate that title is provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Update the event
    event.title = data["title"]
    
    return jsonify(event.to_dict()), 200

# DELETE /events/<int:event_id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event by ID
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Remove the event
    events.remove(event)
    
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
