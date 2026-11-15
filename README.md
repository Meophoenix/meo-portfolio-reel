# Portfolio Reel: frame-accurate HTML/CSS motion, exported to MP4

A 108.75 s, 1080x1920 (9:16), 30 fps portfolio reel for Eniola "MEO" Ogundele. It is built with plain HTML, CSS and JavaScript, rendered frame by frame in headless Chromium, with a soundtrack synthesised in Python and muxed by FFmpeg.

## What it renders
11 scenes on one master timeline (hook and name reveal, role words, flyer fan, brand-guideline walkthroughs, app screens, client flyers, close and contact card). It uses masked text reveals, 3D-tilted device mockups, cubic-bezier easing, glass UI chips, an SVG easing curve that draws itself, and a cursor that "clicks" through the UI.

## What drives the output
- `render(t)` in `film2.html` is a pure function of time `t` (seconds). Nothing runs on a clock, so every frame is deterministic.
- Scene start times (`T`, `ROLE`) and keyframe tracks (`TRK`, `kf`, `kk`) set the timing. Easing curves come from `bez()`.
- `assets.js` is the image manifest (name and pixel size for each screen, flyer and guideline page). The images are in `assets/`.
- `audio3.py` builds the audio from the same scene times: a 128 BPM beat, pads, plucks, whooshes, impacts and UI clicks, all synthesised with NumPy and SciPy.

## Export to video
```bash
pip install -r requirements.txt && playwright install chromium
./render.sh                 # full reel -> Eniola_Portfolio_Reel_9x16.mp4
FRAMES=90 ./render.sh t.mp4 # 3-second test render
```
1. `capg.py` opens `film2.html` in Playwright, calls `render(f/30)` for each frame, waits for images to decode, and saves a JPEG screenshot.
2. `audio3.py` writes `raw3.wav`.
3. FFmpeg encodes the frames to H.264 (CRF 18, yuv420p), adds AAC audio, and writes the MP4.

Single stills: `python3 capg.py stills 2.0,30.0,100.0 out/`. Overlap and legibility check: `python3 aud.py`.
