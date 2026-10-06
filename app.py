import streamlit as st
from events import get_all_events
from ai_recommender import get_ai_recommendations
from ollama_assistant import ask_ollama
from booking import check_availability, calculate_price, create_booking

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="AI Event Finder",
    page_icon="🎉",
    layout="wide"
)
st.subheader("🤖 AI Event Recommendation")

ai_query = st.text_input(
    "What kind of event are you looking for?",
    placeholder="Example: I want a traditional dance night"
)

if ai_query:

    recommendations = get_ai_recommendations(ai_query, 5)

    st.write("### 🎯 Recommended Events")

    if recommendations:

        for event in recommendations:

            st.success(
                f"🎉 {event['name']}\n\n"
                f"📍 {event['location']}\n\n"
                f"📅 {event['date']}\n\n"
                f"⏰ {event['start_time']} - {event['end_time']}\n\n"
                f"🎟️ Adult: ₹{event['adult_price']} | "
                f"Child: ₹{event['child_price']}"
            )

    else:
        st.warning("No matching events found.")

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("🎉 AI Event Finder")
st.caption(
    "Discover events in Hyderabad using AI-powered recommendations, "
    "event search and demo booking."
)
st.info(
    "💡 Try the AI recommendation box with natural language, "
    "for example: 'I want a traditional dance night' "
    "or 'Suggest a family event.'"
)
st.write("Find the best events in Hyderabad based on your interests.")

st.divider()


# -------------------------------------------------
# LOAD EVENTS
# -------------------------------------------------

events = get_all_events()


# -------------------------------------------------
# SEARCH
# -------------------------------------------------

st.subheader("🔎 Search Events")

search = st.text_input(
    "Search by event, activity, location or interest",
    placeholder="Example: Dandiya, music, food, traditional..."
)


# -------------------------------------------------
# FILTERS
# -------------------------------------------------

st.subheader("🎯 Filters")

col1, col2, col3 = st.columns(3)

with col1:
    event_types = sorted(
        list(set(event["type"] for event in events))
    )

    selected_type = st.selectbox(
        "Event Type",
        ["All"] + event_types
    )


with col2:
    locations = sorted(
        list(set(event["location"] for event in events))
    )

    selected_location = st.selectbox(
        "Location",
        ["All"] + locations
    )


with col3:
    max_price = st.slider(
        "Maximum Adult Ticket Price",
        min_value=0,
        max_value=1000,
        value=1000,
        step=50
    )


st.divider()


# -------------------------------------------------
# FILTER EVENTS
# -------------------------------------------------

filtered_events = []

for event in events:

    # Search filter
    if search:

        search_text = (
            event["name"]
            + " "
            + event["type"]
            + " "
            + event["location"]
            + " "
            + event["dress_code"]
            + " "
            + event["description"]
            + " "
            + " ".join(event["activities"])
        ).lower()

        if search.lower() not in search_text:
            continue

    # Type filter
    if selected_type != "All":
        if event["type"] != selected_type:
            continue

    # Location filter
    if selected_location != "All":
        if event["location"] != selected_location:
            continue

    # Price filter
    if event["adult_price"] > max_price:
        continue

    filtered_events.append(event)


# -------------------------------------------------
# RESULT COUNT
# -------------------------------------------------

st.subheader(
    f"🎟️ {len(filtered_events)} Event(s) Found"
)


# -------------------------------------------------
# DISPLAY EVENT CARDS
# -------------------------------------------------

if len(filtered_events) == 0:

    st.warning(
        "No events found. Try changing your search or filters."
    )

else:

    for event in filtered_events:

        with st.container(border=True):

            st.subheader(
                f"🎉 {event['name']}"
            )

            col1, col2, col3 = st.columns(3)

            # -----------------------------
            # EVENT INFORMATION
            # -----------------------------

            with col1:

                st.write(
                    f"📍 **Location:** {event['location']}"
                )

                st.write(
                    f"📅 **Date:** {event['date']}"
                )

                st.write(
                    f"⏰ **Time:** "
                    f"{event['start_time']} - "
                    f"{event['end_time']}"
                )

                st.write(
                    f"🎭 **Type:** {event['type']}"
                )


            # -----------------------------
            # PRICE INFORMATION
            # -----------------------------

            with col2:

                st.write(
                    f"🎟️ **Adult:** "
                    f"₹{event['adult_price']}"
                )

                st.write(
                    f"👧 **Child:** "
                    f"₹{event['child_price']}"
                )

                st.write(
                    f"👗 **Dress Code:** "
                    f"{event['dress_code']}"
                )

                st.write(
                    f"🟢 **Available Seats:** "
                    f"{event['available_seats']}"
                )


            # -----------------------------
            # ACTIVITIES
            # -----------------------------

            with col3:

                st.write("🎯 **Activities:**")

                for activity in event["activities"]:

                    st.write(
                        f"• {activity}"
                    )


            st.write(
                f"📝 {event['description']}"
            )

            st.button(
                "🎟️ View / Book",
                key=f"view_{event['id']}"
            )
st.divider()

st.subheader("🤖 Ask AI Event Assistant")

user_question = st.text_input(
    "Ask anything about events",
    placeholder="Example: Which event is good for a family?"
)

if user_question:
    with st.spinner("🤖 AI is thinking..."):
        answer = ask_ollama(user_question)

    st.info(answer)

st.divider()

st.subheader("🎟️ Demo Event Booking")

all_events = get_all_events()

event_names = [event["name"] for event in all_events]

selected_event_name = st.selectbox(
    "Select an event",
    event_names
)

selected_event = next(
    event for event in all_events
    if event["name"] == selected_event_name
)

st.write(f"📍 **Location:** {selected_event['location']}")
st.write(f"📅 **Date:** {selected_event['date']}")
st.write(f"⏰ **Time:** {selected_event['start_time']} - {selected_event['end_time']}")
st.write(f"💺 **Available Seats:** {selected_event['available_seats']}")

adults = st.number_input(
    "Number of Adults",
    min_value=0,
    max_value=10,
    value=1
)

children = st.number_input(
    "Number of Children",
    min_value=0,
    max_value=10,
    value=0
)

total_price = calculate_price(
    selected_event,
    adults,
    children
)

st.write(f"💰 **Total Price: ₹{total_price}**")

if st.button("Check Availability"):

    available, message = check_availability(
        selected_event["id"],
        adults,
        children
    )

    if available:
        st.success(message)
    else:
        st.error(message)


name = st.text_input("Enter your name")

if st.button("🎫 Confirm Demo Booking"):

    if not name:
        st.warning("Please enter your name.")

    else:

        result = create_booking(
            selected_event["id"],
            name,
            adults,
            children
        )

        if result["success"]:

            st.success("🎉 Demo booking confirmed!")

            st.write(f"👤 **Name:** {result['name']}")
            st.write(f"🎉 **Event:** {result['event']}")
            st.write(f"👨 **Adults:** {result['adults']}")
            st.write(f"👧 **Children:** {result['children']}")
            st.write(f"💰 **Total Price:** ₹{result['total_price']}")
            st.write(f"💺 **Remaining Seats:** {result['remaining_seats']}")

        else:
            st.error(result["message"])