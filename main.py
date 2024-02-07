# NOTE: this example requires PyAudio because it uses the Microphone class
# Install openai and google sdk libraries

import os
import speech_recognition as sr
import google.cloud.texttospeech as tts
import openai

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Path/to/cred.json"
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""/Path/to/cred.json"""
openai.api_key = "YOUR_OPENIA_API_KEY"
import json

def text_to_wav(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = f"{voice_name}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')



# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Google Cloud Speech

try:
    result = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language="ar-MA")
    print("Google Cloud Speech thinks you said " + result)
    

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"""Act as an expert Arabic to English Translator\n translate this ambigous sentence:'{result}', don't explain""",
    max_tokens=300
    )
    
    print(response.choices[0].text)
    text_to_wav("en-US-Wavenet-C", response.choices[0].text)
    
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))

