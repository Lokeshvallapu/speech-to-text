import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import moviepy.editor as mp
import speech_recognition as sr
import whisper
from pydub import AudioSegment

app = Flask(__name__)

recognizer = sr.Recognizer()

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def load_whisper():
     import whisper
     return whisper.load_model("base")


# Convert audio to wav
def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(output_file, format="wav")


# Extract audio from video
def extract_audio_from_video(video_path):
    video = mp.VideoFileClip(video_path)
    audio_path = os.path.join(UPLOAD_FOLDER, "video_audio.wav")
    video.audio.write_audiofile(audio_path)
    video.close()
    return audio_path


@app.route("/", methods=["GET", "POST"])
def index():

    transcript = ""
    message = ""

    if request.method == "POST":

            input_type = request.form.get("input_type")

    try:

            # Load Whisper model only when needed
            model = load_whisper()

            # MICROPHONE
            if input_type == "microphone":

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)

                mic_path = os.path.join(UPLOAD_FOLDER, "mic_audio.wav")

                with open(mic_path, "wb") as f:
                    f.write(audio.get_wav_data())

                result = model.transcribe(mic_path)
                transcript = result["text"]

            # AUDIO FILE
            elif input_type == "audio_file":

                file = request.files.get("audio_file")

                if file and file.filename != "":

                    filename = secure_filename(file.filename)

                    file_path = os.path.join(UPLOAD_FOLDER, filename)

                    file.save(file_path)

                    wav_path = os.path.join(UPLOAD_FOLDER, "converted.wav")

                    convert_to_wav(file_path, wav_path)

                    result = model.transcribe(wav_path)

                    transcript = result["text"]

                else:
                    message = "Please upload an audio file"

            # VIDEO FILE
            elif input_type == "video_file":

                file = request.files.get("video_file")

                if file and file.filename != "":

                    filename = secure_filename(file.filename)

                    file_path = os.path.join(UPLOAD_FOLDER, filename)

                    file.save(file_path)

                    audio_path = extract_audio_from_video(file_path)

                    result = model.transcribe(audio_path)

                    transcript = result["text"]

                else:
                    message = "Please upload a video file"

    except Exception as e:

        message = str(e)

    # ALWAYS return a response
    return render_template("index.html", transcript=transcript, message=message)


if __name__ == "__main__":
    app.run(debug=True)