from database import add_events_to_database, search_events
from events import get_all_events


def get_ai_recommendations(user_query, number_of_results=5):

    add_events_to_database()

    results = search_events(user_query, number_of_results)

    recommendations = []

    if results["metadatas"]:
        for metadata in results["metadatas"][0]:

            # Find the complete event from events.py
            for event in get_all_events():

                if (
                    event["name"] == metadata["name"]
                    and event["location"] == metadata["location"]
                ):
                    recommendations.append(event)
                    break

    return recommendations