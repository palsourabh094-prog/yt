"""
Example usage of the YouTube Transcript API
"""

from main import get_transcript, print_transcript

# Example 1: Using a full YouTube URL
print("Example 1: Using full YouTube URL")
print("-" * 60)
url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
result = get_transcript(url, language='en')
print_transcript(result, show_timestamps=True)

print("\n\n")

# Example 2: Using a short URL
print("Example 2: Using short URL")
print("-" * 60)
url = "https://youtu.be/jNQXAC9IVRw"
result = get_transcript(url, language='en')
print_transcript(result, show_timestamps=False)

print("\n\n")

# Example 3: Using just the video ID
print("Example 3: Using video ID only")
print("-" * 60)
url = "jNQXAC9IVRw"
result = get_transcript(url, language='en')
if result['status'] == 'success':
    print(f"Successfully fetched {result['snippet_count']} snippets")
else:
    print(f"Error: {result['error']}")
