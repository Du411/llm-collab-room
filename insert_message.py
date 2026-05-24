import datetime
from pymongo import MongoClient

class ChatMessage:
    def __init__(self, session_id: str, message_content: str):
        self.session_id = session_id
        self.message_content = message_content
        self.created_at_utc = datetime.datetime.now(datetime.timezone.utc)

    def to_document(self) -> dict:
        return {
            "sessionId": self.session_id,
            "message": self.message_content,
            "timestamp": self.created_at_utc
        }

class ChatMessageRepository:
    def __init__(self, mongo_client: MongoClient, database_name: str, collection_name: str):
        self.collection = mongo_client[database_name][collection_name]

    def insert_chat_message(self, chat_message: ChatMessage) -> str:
        result = self.collection.insert_one(chat_message.to_document())
        return str(result.inserted_id)

if __name__ == "__main__":
    mongo_connection_uri = "mongodb://localhost:27017"
    database_name = "llm-collab-db"
    collection_name = "chat_history"
    
    mongo_client = MongoClient(mongo_connection_uri)
    chat_message_repository = ChatMessageRepository(
        mongo_client=mongo_client,
        database_name=database_name,
        collection_name=collection_name
    )
    
    chat_message_to_insert = ChatMessage(
        session_id="session_12345",
        message_content="Hello, this is a test message for MongoDB integration."
    )
    
    inserted_document_id = chat_message_repository.insert_chat_message(chat_message_to_insert)
    print(f"Success: {inserted_document_id}")
