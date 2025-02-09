def set_ttl_index():
    """Sets a TTL (Time-To-Live) index to auto-delete messages after 30 days."""
    collection.create_index("timestamp", expireAfterSeconds=2592000)  # 30 days

# Example usage
set_ttl_index()
