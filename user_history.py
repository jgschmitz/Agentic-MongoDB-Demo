def get_chat_history(user_id: str):
    """Fetches chat history for a given user from MongoDB."""
    history = list(collection.find({"user_id": user_id}).sort("timestamp", 1))
    return [{"user": h["user_message"], "ai": h["ai_response"]} for h in history]

# Example usage
print(get_chat_history("123"))
