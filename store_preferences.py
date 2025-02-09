def save_user_preferences(user_id: str, preferences: dict):
    """Stores or updates user preferences in MongoDB."""
    collection.update_one(
        {"user_id": user_id},
        {"$set": {"preferences": preferences}},
        upsert=True
    )

# Example usage
save_user_preferences("123", {"language": "English", "theme": "dark"})
