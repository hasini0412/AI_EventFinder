import chromadb
from sentence_transformers import SentenceTransformer
from events import get_all_events

# Create AI embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create ChromaDB
client = chromadb.PersistentClient(path="event_chroma_db")

collection = client.get_or_create_collection(
    name="events"
)


def add_events_to_database():

    events = get_all_events()

    # Avoid adding duplicate events
    if collection.count() >= len(events):
        return

    documents = []
    ids = []
    metadatas = []

    for event in events:

        document = f"""
        {event['name']}
        {event['type']}
        {event['location']}
        {event['date']}
        {event['start_time']} to {event['end_time']}
        Adult price {event['adult_price']}
        Child price {event['child_price']}
        Dress code {event['dress_code']}
        Activities {', '.join(event['activities'])}
        {event['description']}
        """

        documents.append(document)
        ids.append(str(event["id"]))

        metadatas.append({
            "name": event["name"],
            "type": event["type"],
            "location": event["location"],
            "date": event["date"]
        })

    # Convert events into AI embeddings
    embeddings = model.encode(documents).tolist()

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )


def search_events(query, number_of_results=5):

    # Convert user's question into an embedding
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=number_of_results
    )

    return results