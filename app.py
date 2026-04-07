import os
from flask import Flask, request, send_file, jsonify
from spleeter.separator import Separator
from pedalboard import Pedalboard, Lowpass, Reverb, Gain
from pedalboard.io import AudioFile
import librosa
import soundfile as sf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize Spleeter (2stems = vocals + accompaniment)
separator = Separator('spleeter:2stems')

def apply_lofi_effects(input_path, output_path):
    """Applies Lo-Fi aesthetics: Slows down, Low-pass filter, and Reverb."""
    # 1. Load with Librosa to change speed
    y, sr = librosa.load(input_path, sr=None)
    
    # Slow down by 10% for that chilled vibe
    y_slow = librosa.effects.time_stretch(y, rate=0.9)
    
    # Save temporary slowed version for Pedalboard
    temp_slow = "temp_slow.wav"
    sf.write(temp_slow, y_slow, sr)

    # 2. Apply Pedalboard effects
    with AudioFile(temp_slow) as f:
        with AudioFile(output_path, 'w', f.samplerate, f.num_channels) as o:
            # Lowpass cuts highs, Reverb adds space, Gain balances it
            board = Pedalboard([
                Lowpass(cutoff_frequency_hz=1500),
                Reverb(room_size=0.3),
                Gain(gain_db=2)
            ])
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)
                processed_chunk = board(chunk, f.samplerate, reset=False)
                o.write(processed_chunk)
    
    os.remove(temp_slow)

@app.route('/transform', methods=['POST'])
def transform_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    style = request.form.get('style', 'lofi') # default to lofi
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(input_path)

    # Step 1: Separate Stems
    # Spleeter creates a folder named after the file
    separator.separate_to_file(input_path, app.config['OUTPUT_FOLDER'])
    
    # Step 2: Identify the accompaniment (instrumental) track
    filename_no_ext = os.path.splitext(file.filename)[0]
    instrumental_path = os.path.join(app.config['OUTPUT_FOLDER'], filename_no_ext, 'accompaniment.wav')
    final_output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"VibeShift_{filename_no_ext}_{style}.wav")

    # Step 3: Apply Style Logic
    if style == 'lofi':
        apply_lofi_effects(instrumental_path, final_output_path)
    
    return send_file(final_output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
