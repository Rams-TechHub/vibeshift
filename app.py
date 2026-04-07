import os
import shutil
from flask import Flask, request, send_file, jsonify
from spleeter.separator import Separator
from pedalboard import Pedalboard, Lowpass, HighpassFilter, Reverb, Gain, Compressor
from pedalboard.io import AudioFile
import librosa
import soundfile as sf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize Spleeter (2 stems: vocals + accompaniment)
# Note: This will download the model on first run.
separator = Separator('spleeter:2stems')

def apply_lofi_effects(input_path, output_path):
    """Lo-Fi: Slow, Warm, Muffled."""
    y, sr = librosa.load(input_path, sr=None)
    y_slow = librosa.effects.time_stretch(y, rate=0.85)
    temp_path = "temp_lofi.wav"
    sf.write(temp_path, y_slow, sr)

    with AudioFile(temp_path) as f:
        with AudioFile(output_path, 'w', f.samplerate, f.num_channels) as o:
            board = Pedalboard([
                Lowpass(cutoff_frequency_hz=1200),
                Reverb(room_size=0.25),
                Gain(gain_db=1)
            ])
            o.write(board(f.read(f.frames), f.samplerate))
    os.remove(temp_path)

def apply_dance_effects(input_path, output_path):
    """Dance: Fast, Compressed, Bass-heavy."""
    y, sr = librosa.load(input_path, sr=None)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    
    # Target high energy 128 BPM
    rate = 128.0 / float(tempo) if tempo > 0 else 1.2
    y_fast = librosa.effects.time_stretch(y, rate=rate)
    
    temp_path = "temp_dance.wav"
    sf.write(temp_path, y_fast, sr)

    with AudioFile(temp_path) as f:
        with AudioFile(output_path, 'w', f.samplerate, f.num_channels) as o:
            board = Pedalboard([
                Compressor(threshold_db=-18, ratio=4),
                Gain(gain_db=4) # Simulating a punchy output
            ])
            o.write(board(f.read(f.frames), f.samplerate))
    os.remove(temp_path)

def apply_acoustic_effects(input_path, output_path):
    """Unplugged: Clean Vocals, Deep Reverb, Noisy Mid-boost."""
    with AudioFile(input_path) as f:
        with AudioFile(output_path, 'w', f.samplerate, f.num_channels) as o:
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=100), # Remove low rumble
                Reverb(room_size=0.6, wet_level=0.4),   # Large hall feel
                Gain(gain_db=2)
            ])
            o.write(board(f.read(f.frames), f.samplerate))

@app.route('/transform', methods=['POST'])
def transform_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    style = request.form.get('style', 'lofi') 
    
    # Save original
    input_filename = file.filename
    safe_name = "".join([c for c in input_filename if c.isalnum() or c in ('.','_')]).rstrip()
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
    file.save(input_path)

    try:
        # Step 1: AI Separation
        separator.separate_to_file(input_path, app.config['OUTPUT_FOLDER'])
        
        # Paths based on Spleeter's output structure
        folder_name = os.path.splitext(safe_name)[0]
        vocals_path = os.path.join(app.config['OUTPUT_FOLDER'], folder_name, 'vocals.wav')
        acc_path = os.path.join(app.config['OUTPUT_FOLDER'], folder_name, 'accompaniment.wav')
        
        final_output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"VibeShift_{style}_{safe_name}")

        # Step 2: Apply Routing Logic
        if style == 'lofi':
            apply_lofi_effects(acc_path, final_output_path)
        elif style == 'dance':
            apply_dance_effects(acc_path, final_output_path)
        elif style == 'unplugged':
            # Unplugged focuses on processing the VOCALS stem
            apply_acoustic_effects(vocals_path, final_output_path)
        else:
            return jsonify({"error": "Style not supported"}), 400

        # Step 3: Cleanup Spleeter folder to save space
        shutil.rmtree(os.path.join(app.config['OUTPUT_FOLDER'], folder_name))

        return send_file(final_output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Using threaded=True to handle multiple AI requests if needed
    app.run(debug=True, port=5000, threaded=True)
