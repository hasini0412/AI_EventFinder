from events import get_all_events


def check_availability(event_id, adults, children):
    event = None

    for e in get_all_events():
        if e["id"] == event_id:
            event = e
            break

    if event is None:
        return False, "Event not found."

    total_people = adults + children

    if total_people <= 0:
        return False, "Please select at least one person."

    if total_people > event["available_seats"]:
        return False, f"Only {event['available_seats']} seats are available."

    return True, "Seats are available."


def calculate_price(event, adults, children):
    adult_cost = adults * event["adult_price"]
    child_cost = children * event["child_price"]

    return adult_cost + child_cost


def create_booking(event_id, name, adults, children):

    event = None

    for e in get_all_events():
        if e["id"] == event_id:
            event = e
            break

    if event is None:
        return {
            "success": False,
            "message": "Event not found."
        }

    total_people = adults + children

    if total_people <= 0:
        return {
            "success": False,
            "message": "Please select at least one person."
        }

    if total_people > event["available_seats"]:
        return {
            "success": False,
            "message": "Not enough seats available."
        }

    total_price = calculate_price(event, adults, children)

    # Reduce available seats
    event["available_seats"] -= total_people

    return {
        "success": True,
        "message": "Demo booking confirmed!",
        "name": name,
        "event": event["name"],
        "adults": adults,
        "children": children,
        "total_people": total_people,
        "total_price": total_price,
        "remaining_seats": event["available_seats"]
    }