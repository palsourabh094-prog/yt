"""
YouTube Transcript API - Main application
Accepts a YouTube URL and returns the transcript
"""

from youtube_transcript_api import YouTubeTranscriptApi
import re
import sys


def extract_video_id(url: str) -> str:
    """
    Extract video ID from various YouTube URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - VIDEO_ID (direct ID)
    """
    # If it's just the video ID, return it
    if len(url) == 11 and url.isalnum():
        return url
    
    # Extract from youtube.com URL
    match = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)
    
    # Extract from youtu.be URL
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)
    
    raise ValueError(f"Invalid YouTube URL: {url}")


def get_transcript(url: str, language: str = 'en') -> dict:
    """
    Fetch transcript from a YouTube video.
    
    Args:
        url: YouTube URL or video ID
        language: Language code (default: 'en' for English)
    
    Returns:
        Dictionary containing transcript data
    """
    try:
        # Extract video ID from URL
        video_id = extract_video_id(url)
        print(f"📝 Fetching transcript for video ID: {video_id}")
        
        # Initialize API
        ytt_api = YouTubeTranscriptApi()
        
        # Fetch transcript
        transcript = ytt_api.fetch(video_id, languages=[language])
        
        return {
            'status': 'success',
            'video_id': video_id,
            'language': language,
            'transcript': transcript.to_raw_data() if hasattr(transcript, 'to_raw_data') else transcript,
            'snippet_count': len(transcript)
        }
    
    except ValueError as e:
        return {
            'status': 'error',
            'error': f'URL Error: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': f'{type(e).__name__}: {str(e)}'
        }


def print_transcript(result: dict, show_timestamps: bool = True) -> None:
    """
    Pretty print the transcript result.
    
    Args:
        result: Result dictionary from get_transcript()
        show_timestamps: Whether to show start times
    """
    if result['status'] == 'error':
        print(f"\n❌ Error: {result['error']}")
        return
    
    print(f"\n✅ Transcript retrieved successfully!")
    print(f"Video ID: {result['video_id']}")
    print(f"Language: {result['language']}")
    print(f"Snippets: {result['snippet_count']}")
    print("\n" + "="*60)
    print("TRANSCRIPT:")
    print("="*60 + "\n")
    
    for item in result['transcript']:
        if show_timestamps:
            start_time = f"[{item['start']:.2f}s]"
            print(f"{start_time} {item['text']}")
        else:
            print(item['text'])


def main():
    """Main entry point"""
    print("🎥 YouTube Transcript API")
    print("="*60)
    
    if len(sys.argv) > 1:
        # Get URL from command line argument
        url = sys.argv[1]
        language = sys.argv[2] if len(sys.argv) > 2 else 'en'
        show_timestamps = '--no-timestamps' not in sys.argv
        
        result = get_transcript(url, language)
        print_transcript(result, show_timestamps)
    else:
        # Interactive mode
        print("\nEnter a YouTube URL or video ID:")
        print("Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("Or: https://youtu.be/dQw4w9WgXcQ")
        print("Or: dQw4w9WgXcQ\n")
        
        url = input("🔗 URL: ").strip()
        language = input("🌍 Language code (default: en): ").strip() or 'en'
        
        result = get_transcript(url, language)
        print_transcript(result, show_timestamps=True)


if __name__ == '__main__':
    main()
