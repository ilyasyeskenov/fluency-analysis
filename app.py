from flask import Flask, request, jsonify
import os
from fluency.fluency import Fluency

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])

def analyze_audio():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file to a temporary location
    audio_path = os.path.join('./uploads', file.filename)
    file.save(audio_path)
    
    # Create an instance of the Fluency class
    fluency = Fluency(filename=file.filename, audio_path=audio_path)
    
    # Get results
    try:
        result = fluency.get_result()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # Return the result as a JSON response
    return jsonify(result)

if __name__ == '__main__':
    # Ensure uploads directory exists
    os.makedirs('./uploads', exist_ok=True)
    
    app.run(debug=True)


