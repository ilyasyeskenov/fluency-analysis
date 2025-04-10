import os
import shutil
from myprosody1 import myprosody
from pydub import AudioSegment
from scipy.io import wavfile

class Fluency:
    """
    The class receives 2 inputs:

    filename - name of the audio file as string (include extension)
    audio_path - full_path to the audio file
    
    To get the results, just run get_result() function
    
    """

    def __init__(self, filename, audio_path):
        self.filename = filename
        self.audio_path = audio_path

    def read_audio(self):
        """Read and prepare the audio file for analysis."""

        output_path = os.path.abspath("./myprosody1/myprosody/dataset/audioFiles/")

        # Check if the input file is a WAV file
        if not self.filename.lower().endswith('.wav'):

            out_audio = os.path.join(output_path, self.filename[:-3] + "wav")
            audio = AudioSegment.from_file(self.audio_path)
            audio.export(out_audio, format="wav")
            
        else:
            # If it's already a WAV file, copy it to the output location
            out_audio = os.path.join(output_path, self.filename)
            shutil.copy(self.audio_path, out_audio)
            print(f"Copied '{self.audio_path}' to '{out_audio}'.")

        # Read the WAV file
        sample_rate, audio_data = wavfile.read(out_audio)

        # Check sample rate and bit depth
        audio = AudioSegment.from_wav(out_audio)

        if sample_rate != 48000:
            print(f"Warning: Sample rate is {sample_rate} Hz, expected 48,000 Hz. Adjusting...")
            audio = audio.set_frame_rate(48000)  # Set sample rate to 48 kHz
            audio.export(out_audio, format="wav", codec="pcm_s24le")

        bit_depth = audio.sample_width * 8  # Convert sample width to bit depth
        if bit_depth < 24 or bit_depth > 32:
            print(f"Warning: Bit depth is {bit_depth} bits, expected between 24 and 32 bits. Adjusting...")
            audio = audio.set_sample_width(3)  # Set to 24 bits (3 bytes)
            audio.export(out_audio, format="wav", codec="pcm_s24le")

        print("Audio file is ready to be analyzed.")
    
    def get_result(self):
        # Get final results as dictionary

        self.read_audio()
        abs_path = os.path.abspath("./myprosody1/myprosody")
        result = myprosody.mysptotal1(self.filename[:-3] + "wav", abs_path)
        result = {key: float(value) if isinstance(value, str) and value.replace('.', '', 1).isdigit() else value for key, value in result.items()}
    
        return result