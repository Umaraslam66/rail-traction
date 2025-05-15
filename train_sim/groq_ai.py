import os
import requests

def groq_chat(messages, model="llama3-70b-8192", api_key=None):
    """
    Call Groq API for chat completion.
    Args:
        messages (list): List of {"role": "user"|"system"|"assistant", "content": str}
        model (str): Model name (e.g., llama3-70b-8192)
        api_key (str): Groq API key (default: from env GROQ_API_KEY)
    Returns:
        str: AI response
    """
    api_key = api_key or os.getenv("GROQ_API_KEY") or "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"
    if not api_key:
        return "[Groq API key not set]"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Groq API error: {e}]"

def ai_summarize_simulation(results_dict, user_prompt=None):
    """
    Use Groq to summarize simulation results and optionally answer a user prompt.
    """
    sys_msg = {"role": "system", "content": "You are a helpful railway simulation expert. Summarize the following simulation results and answer the user's question if provided."}
    user_msg = {"role": "user", "content": f"Simulation results: {results_dict}\n{user_prompt or ''}"}
    return groq_chat([sys_msg, user_msg])

def ai_parse_requirements(nl_requirements):
    """
    Use Groq to parse natural language requirements into structured simulation constraints.
    """
    sys_msg = {"role": "system", "content": "You are an expert at converting railway requirements into structured simulation constraints. Output as JSON."}
    user_msg = {"role": "user", "content": f"Requirements: {nl_requirements}"}
    return groq_chat([sys_msg, user_msg])
