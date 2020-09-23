from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import speech_recognition as sr
from speech_recognition import UnknownValueError

app = Flask(__name__)
app.secret_key = 'super secret'

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    filenames = ""
    lang = request.form.get("language")

    if lang == "Choose language":
        flash("please select your language")
        return redirect(request.url)

    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            flash("please select your file")
            return redirect(request.url)

        file = request.files["file"]
        filenames = file.filename
        if file.filename == "":
            flash("please select your file")
            return redirect(request.url)
            
        if file:
            try:
                recognizer = sr.Recognizer()
                audioFile = sr.AudioFile(file)
                with audioFile as source:
                    data = recognizer.record(source)
                transcript = recognizer.recognize_google(data, language=lang)
                print(transcript)
                print(file.filename)
                print(lang)
            except Exception as e:
                if e == ValueError:
                    flash("please select .wav file")
                    return redirect(request.url)
                elif e == UnknownValueError:
                    flash("can not transcribe your file")
                    return redirect(request.url)


    return render_template("index.html", transcript=transcript, lang=lang, filenames=filenames)

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500
    
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
