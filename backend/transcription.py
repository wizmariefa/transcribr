from os import path
import io
import speech_recognition as sr

def transcribe_file(audio_file):
    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # read the entire audio file

    output = open('output.txt', 'w+')

    # recognize speech using Sphinx
    try:
        output.write(r.recognize_sphinx(audio))
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    
    return output