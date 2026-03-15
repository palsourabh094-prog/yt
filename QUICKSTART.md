# Quick Start Guide 🚀

Get up and running with the YouTube Transcript API in 3 minutes!

## Step 1: Install Dependencies

The Python virtual environment and dependencies are already set up for you.

```bash
# If you need to reinstall, run:
pip3 install -r requirements.txt
```

## Step 2: Run the API

### Option A: Interactive Mode (Recommended for beginners)

Simply run:

```bash
python3 main.py
```

You'll be prompted to:
1. Enter a YouTube URL or video ID
2. Specify the language (defaults to English)

Then sit back and watch your transcript appear! ✨

### Option B: Command Line Mode (For automation)

```bash
# Get English transcript
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Get German transcript
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" de

# Get transcript without timestamps
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" en --no-timestamps
```

## Step 3: Use in Your Own Code

```python
from main import get_transcript

# Fetch transcript
result = get_transcript("https://www.youtube.com/watch?v=VIDEO_ID", language='en')

# Access the data
if result['status'] == 'success':
    for snippet in result['transcript']:
        print(f"{snippet['start']:.2f}s: {snippet['text']}")
else:
    print(f"Error: {result['error']}")
```

## Supported URL Formats

All these work:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
dQw4w9WgXcQ
```

## Common Language Codes

| Language | Code |
|----------|------|
| English | en |
| German | de |
| French | fr |
| Spanish | es |
| Italian | it |
| Japanese | ja |
| Korean | ko |
| Chinese | zh |

See README.md for more languages.

## Troubleshooting

### Problem: "No transcripts found"
- Solution: Not all videos have transcripts. Try another video.

### Problem: "IpBlocked" error
- Solution: YouTube is blocking your IP. Try from a different network or use a VPN.

### Problem: Can't find video ID
- Solution: Your URL might be wrong. Copy directly from YouTube's address bar.

## Need Help?

Check the full README.md for complete API documentation, advanced features, and integration examples.

Happy transcripting! 🎉
