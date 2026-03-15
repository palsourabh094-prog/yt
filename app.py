"""
YouTube Transcript API - Flask Web Server
A REST API for extracting YouTube transcripts
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os
from functools import wraps
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['JSON_SORT_KEYS'] = False
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


def extract_video_id(url: str) -> str:
    """
    Extract video ID from various YouTube URL formats.
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


def handle_errors(f):
    """Decorator to handle and format errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': f'{type(e).__name__}: {str(e)}'
            }), 400
    return decorated_function


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/', methods=['GET'])
def index():
    """API documentation and health check"""
    return jsonify({
        'status': 'success',
        'message': 'YouTube Transcript API is running!',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'This page',
            'POST /api/transcript': 'Get transcript from YouTube video',
            'GET /api/transcript': 'Get transcript from YouTube video (query params)',
            'POST /api/list-transcripts': 'List available transcripts for a video',
            'GET /health': 'Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    })


@app.route('/api/transcript', methods=['POST', 'GET'])
@handle_errors
def get_transcript():
    """
    Get transcript from YouTube video
    """
    
    # Get parameters from POST or GET
    if request.method == 'POST':
        data = request.get_json() or {}
        url = data.get('url', '').strip()
        language = data.get('language', 'en').strip()
        preserve_formatting = data.get('preserve_formatting', False)
    else:
        url = request.args.get('url', '').strip()
        language = request.args.get('language', 'en').strip()
        preserve_formatting = request.args.get('preserve_formatting', 'false').lower() == 'true'
    
    # Validate input
    if not url:
        return jsonify({
            'status': 'error',
            'error': 'Missing required parameter: url'
        }), 400
    
    try:
        # Extract video ID
        video_id = extract_video_id(url)
        
        # Fetch transcript
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(
            video_id,
            languages=[language],
            preserve_formatting=preserve_formatting
        )
        
        # Convert to raw data
        try:
            raw_transcript = transcript.to_raw_data()
        except (AttributeError, TypeError):
            raw_transcript = list(transcript)
        
        return jsonify({
            'status': 'success',
            'video_id': video_id,
            'language': language,
            'transcript': raw_transcript,
            'snippet_count': len(raw_transcript)
        }), 200
    
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'error': f'URL Error: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'{type(e).__name__}: {str(e)}'
        }), 500


@app.route('/api/list-transcripts', methods=['POST', 'GET'])
@handle_errors
def list_transcripts():
    """
    List all available transcripts for a video
    """
    
    # Get URL from POST or GET
    if request.method == 'POST':
        data = request.get_json() or {}
        url = data.get('url', '').strip()
    else:
        url = request.args.get('url', '').strip()
    
    if not url:
        return jsonify({
            'status': 'error',
            'error': 'Missing required parameter: url'
        }), 400
    
    try:
        # Extract video ID
        video_id = extract_video_id(url)
        
        # List transcripts
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        
        # Format response
        available_transcripts = []
        for transcript in transcript_list:
            available_transcripts.append({
                'language': transcript.language,
                'language_code': transcript.language_code,
                'is_generated': transcript.is_generated,
                'is_translatable': transcript.is_translatable
            })
        
        return jsonify({
            'status': 'success',
            'video_id': video_id,
            'transcripts': available_transcripts,
            'transcript_count': len(available_transcripts)
        }), 200
    
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'error': f'URL Error: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'{type(e).__name__}: {str(e)}'
        }), 500


@app.route('/api/transcript/text', methods=['POST', 'GET'])
@handle_errors
def get_transcript_as_text():
    """
    Get transcript as plain text (no timestamps)
    """
    
    # Get parameters
    if request.method == 'POST':
        data = request.get_json() or {}
        url = data.get('url', '').strip()
        language = data.get('language', 'en').strip()
    else:
        url = request.args.get('url', '').strip()
        language = request.args.get('language', 'en').strip()
    
    if not url:
        return jsonify({
            'status': 'error',
            'error': 'Missing required parameter: url'
        }), 400
    
    try:
        # Extract video ID
        video_id = extract_video_id(url)
        
        # Fetch transcript
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=[language])
        
        # Convert to raw data
        try:
            raw_transcript = transcript.to_raw_data()
        except (AttributeError, TypeError):
            raw_transcript = list(transcript)
        
        # Combine text
        full_text = ' '.join([item['text'] for item in raw_transcript])
        
        return jsonify({
            'status': 'success',
            'video_id': video_id,
            'language': language,
            'text': full_text
        }), 200
    
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'error': f'URL Error: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'{type(e).__name__}: {str(e)}'
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'error': 'Endpoint not found',
        'message': 'Visit GET / for API documentation'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("🎥 YouTube Transcript API Server Starting...")
    print(f"📍 Running on http://localhost:{PORT}")
    print(f"📖 Visit http://localhost:{PORT}/ for documentation")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
