# This class will do the actual transcription of the audo file
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
#from google.cloud import speech_v1p1beta1 as speech_beta #This is for word confidence beta
#--note: Currently just foundation, will need to change it to apply to our purpose.

class Transcribr:

    def __init__(self, speech_file, gcs_uri):
        self.speech_file = speech_file
        self.gcs_uri = gcs_uri

    #https://cloud.google.com/speech-to-text/docs/word-confidence credits
    #Added features are writing to separate file with low-confidence words w/ timestamp
    def trasncribe_gcs_with_features(self, gcs_uri):
        from google.cloud import speech_v1p1beta1 as speech_beta
        client = speech_beta.SpeechClient()

        speech_file = 'resources/Google_Gnome.wav'

        with open(speech_file, 'rb') as audio_file:
            content = audio_file.read()

        audio = speech_beta.types.RecognitionAudio(content=content)

        #encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        #may need this? it uses .FLAC instead of .LINEAR16
        config = speech_beta.types.RecognitionConfig(
            encoding=speech_beta.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
            enable_word_confidence=True,
            enable_word_time_offsets=True)

        operation = client.long_running_recognize(config, audio)
        #response = client.recognize(config, audio)

        result = operation.result(timeout=90) #not sure what this does tbh

        output = open("output.txt", "w+")
        output2 = open("feature.txt", "w+")

        for i, word in enumerate(result.results):
            output.write(word + " ")
        output.close

        #May need to print these out to understand structure of using both word confidence & offset
        for result in result.results:
            alt = result.alternatives[0] #I want to print this later to understand it better
            #write to file
            word = alt.words[0].word
            conf = alt.words[0].confidence
            unknown_format = alt.transcript
            word_info = word.word
            start_time = word_info.start_time.seconds + word_info.start_time.nanos * 1e-9
            end_time = word_info.end_time.seconds + word_info.end_time.nanos * 1e-9

            if(conf < .5):
                output2.write(word + " : " + start_time + "\n\r")

            """
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time.seconds + word_info.start_time.nanos * 1e-9
                end_time = word_info.end_time.seconds + word_info.end_time.nanos * 1e-9
            """
        output2.close

    
    #https://cloud.google.com/speech-to-text/docs/async-recognize credits
    def transcribe_gcs(self, gcs_uri):
        """Asynchronously transcribes the audio file specified by the gcs_uri."""
        client = speech.SpeechClient()

        audio = types.RecognitionAudio(uri=gcs_uri)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            language_code='en-US')

        operation = client.long_running_recognize(config, audio)

        print('Waiting for operation to complete...')
        response = operation.result(timeout=90)

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            print(u'Transcript: {}'.format(result.alternatives[0].transcript))
            print('Confidence: {}'.format(result.alternatives[0].confidence))
        
        output = open("output.txt", "w+")

        for i, word in enumerate(result.results):
            output.write(word + " ")
        output.close
