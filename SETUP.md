# Setup & Running Guide 🚀

## Problem: AttributeError: 'YouTubeTranscriptApi' object has no attribute 'fetch'

This error occurs when running with the system Python instead of the virtual environment.

## Solution: Use the Virtual Environment

### Option 1: Activate the virtual environment (Recommended)

```bash
source .venv/bin/activate
python main.py
```

### Option 2: Use the full path

```bash
.venv/bin/python main.py
```

### Option 3: Use the run script (Easiest)

```bash
./run.sh
```

Or with arguments:
```bash
./run.sh "https://youtu.be/VIDEO_ID" en
```

## Why This Matters

The YouTube Transcript API is installed in the **virtual environment** (`.venv`), not in the system Python.

- ❌ `python3 main.py` - Uses system Python (no packages installed)
- ✅ `.venv/bin/python main.py` - Uses virtual environment Python (has all packages)
- ✅ `./run.sh` - Uses virtual environment Python (via the run script)

## Verify Installation

To check if packages are installed in the virtual environment:

```bash
.venv/bin/python -c "import youtube_transcript_api; print('✅ Installed')"
```

## Next Steps

Now that it's working, you can:

1. **Interactive Mode:**
   ```bash
   ./run.sh
   ```

2. **Command Line Mode:**
   ```bash
   ./run.sh "https://youtu.be/VIDEO_ID"
   ```

3. **Different Language:**
   ```bash
   ./run.sh "https://youtu.be/VIDEO_ID" de
   ```

## Files Structure

```
untitled folder/
├── main.py              ← Main application
├── .venv/               ← Virtual environment (has packages)
├── requirements.txt     ← Package list
├── run.sh              ← Easy run script
├── README.md           ← Full documentation
└── QUICKSTART.md       ← Quick start guide
```

Enjoy transcripting! 🎉
