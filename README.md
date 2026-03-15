# YouTube Transcript API 🎥

A Python application that extracts transcripts/subtitles from YouTube videos using the YouTube Transcript API.

## Features ✨

- 📝 Extract transcripts from any YouTube video
- 🌍 Support for multiple languages
- 🔗 Accept various YouTube URL formats
- ⏱️ Display timestamps with transcript text
- 🎯 Interactive and command-line modes
- ❌ Graceful error handling

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Navigate to the project directory
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run without arguments to use interactive mode:

```bash
python main.py
```

Then follow the prompts to enter your YouTube URL and language preference.

### Command Line Mode

```bash
# Basic usage (English transcript)
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"

# With specific language
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" de

# Without timestamps
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" en --no-timestamps
```

### Supported URL Formats

- Full YouTube URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Short YouTube URL: `https://youtu.be/dQw4w9WgXcQ`
- Video ID only: `dQw4w9WgXcQ`

### Language Codes

Common language codes:
- `en` - English (default)
- `de` - German
- `fr` - French
- `es` - Spanish
- `it` - Italian
- `pt` - Portuguese
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese (Simplified)

## Output

The transcript is displayed with:
- 🎯 Video ID
- 🌍 Language information
- 📊 Total number of transcript snippets
- ⏱️ Timestamps (optional)
- 📄 Full transcript text

## Example Output

```
🎥 YouTube Transcript API
============================================================

Enter a YouTube URL or video ID:
Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Or: https://youtu.be/dQw4w9WgXcQ
Or: dQw4w9WgXcQ

🔗 URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
🌍 Language code (default: en): en

📝 Fetching transcript for video ID: dQw4w9WgXcQ

✅ Transcript retrieved successfully!
Video ID: dQw4w9WgXcQ
Language: en
Snippets: 142

============================================================
TRANSCRIPT:
============================================================

[0.00s] Never gonna give you up
[3.50s] Never gonna let you down
[7.00s] Never gonna run around
...
```

## API Reference

### `get_transcript(url, language='en')`

Fetches a transcript from a YouTube video.

**Parameters:**
- `url` (str): YouTube URL or video ID
- `language` (str): Language code (default: 'en')

**Returns:**
- Dictionary containing:
  - `status`: 'success' or 'error'
  - `video_id`: The extracted video ID
  - `language`: The requested language
  - `transcript`: List of transcript snippets
  - `snippet_count`: Number of snippets
  - `error`: Error message (if applicable)

### `extract_video_id(url)`

Extracts video ID from various YouTube URL formats.

**Parameters:**
- `url` (str): YouTube URL or video ID

**Returns:**
- Video ID (str)

**Raises:**
- `ValueError`: If URL format is invalid

## Error Handling

The application handles various errors gracefully:
- Invalid URL formats
- Network connectivity issues
- Video not found
- No transcript available
- IP blocking (can use proxies)

## Limitations

- ⚠️ YouTube may block requests from cloud providers or high-request IPs
- Some videos may not have transcripts available
- Automatically generated subtitles may have lower accuracy
- Cookie authentication is currently not supported

## Troubleshooting

### "RequestBlocked" or "IpBlocked" Error

If you encounter IP blocking:

1. Use a proxy service (e.g., Webshare)
2. Add delays between requests
3. Try from a different network

### Video has no transcript

- Check if transcripts are available for that video
- Try with a different language
- Verify the video ID is correct

## Dependencies

- **youtube-transcript-api**: Core library for fetching transcripts
- **requests**: HTTP library for web requests

## License

MIT License

## Resources

- [YouTube Transcript API Documentation](https://github.com/jdepoix/youtube-transcript-api)
- [YouTube Documentation](https://developers.google.com/youtube)
