def summarize_chat_history(user_id: str):
    """Summarizes a user's chat history using OpenAI."""
    history = get_chat_history(user_id)
    
    if len(history) < 3:
        return history  # No need to summarize if chat is short
    
    summary_prompt = "Summarize this conversation briefly:\n" + str(history)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": summary_prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# Example usage
print(summarize_chat_history("123"))
