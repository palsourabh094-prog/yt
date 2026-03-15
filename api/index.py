"""YouTube Transcript API - Vercel Serverless"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re
from functools import wraps
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False

def extract_video_id(url: str) -> str:
    if len(url) == 11 and url.isalnum():
        return url
    match = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)
    raise ValueError(f"Invalid YouTube URL: {url}")

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'status': 'error', 'error': f'{type(e).__name__}: {str(e)}'}), 400
    return decorated_function

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'success', 'message': 'YouTube Transcript API on Vercel!', 'version': '1.0.0'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/transcript', methods=['POST', 'GET'])
@app.route('/transcript', methods=['POST', 'GET'])
@handle_errors
def get_transcript():
    if request.method == 'POST':
        data = request.get_json() or {}
        url = data.get('url', '').strip()
        language = data.get('language', 'en').strip()
    else:
        url = request.args.get('url', '').strip()
        language = request.args.get('language', 'en').strip()
    
    if not url:
        return jsonify({'status': 'error', 'error': 'Missing url parameter'}), 400
    
    video_id = extract_video_id(url)
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=[language])
    try:
        raw = transcript.to_raw_data()
    except:
        raw = list(transcript)
    
    return jsonify({
        'status': 'success',
        'video_id': video_id,
        'language': language,
        'transcript': raw,
        'snippet_count': len(raw)
    }), 200

@app.route('/api/list-transcripts', methods=['POST', 'GET'])
@app.route('/list-transcripts', methods=['POST', 'GET'])
@handle_errors
def list_transcripts():
    if request.method == 'POST':
        url = request.get_json().get('url', '').strip()
    else:
        url = request.args.get('url', '').strip()
    
    if not url:
        return jsonify({'status': 'error', 'error': 'Missing url parameter'}), 400
    
    video_id = extract_video_id(url)
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    
    transcripts = []
    for t in transcript_list:
        transcripts.append({
            'language': t.language,
            'language_code': t.language_code,
            'is_generated': t.is_generated,
            'is_translatable': t.is_translatable
        })
    
    return jsonify({'status': 'success', 'video_id': video_id, 'transcripts': transcripts}), 200

@app.route('/api/transcript/text', methods=['POST', 'GET'])
@app.route('/transcript/text', methods=['POST', 'GET'])
@handle_errors
def get_text():
    if request.method == 'POST':
        data = request.get_json() or {}
        url = data.get('url', '').strip()
        language = data.get('language', 'en').strip()
    else:
        url = request.args.get('url', '').strip()
        language = request.args.get('language', 'en').strip()
    
    if not url:
        return jsonify({'status': 'error', 'error': 'Missing url parameter'}), 400
    
    video_id = extract_video_id(url)
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=[language])
    
    try:
        raw = transcript.to_raw_data()
    except:
        raw = list(transcript)
    
    text = ' '.join([item['text'] for item in raw])
    return jsonify({'status': 'success', 'video_id': video_id, 'language': language, 'text': text}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({'status': 'error', 'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)


