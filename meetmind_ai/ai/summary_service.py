import requests


def generate_summary(transcript):

    prompt = f"""
    Summarize the following meeting transcript in simple text.

    Include:
    - Meeting Summary
    - Key Discussion Points
    - Important Decisions
    - Next Steps

    Keep the response short, clean, and easy to understand.

    Transcript:
    {transcript}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]