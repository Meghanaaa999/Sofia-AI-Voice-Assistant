import time
import pyttsx3
import eel
import sounddevice as sd
import numpy as np
import wave
import tempfile
import os

# Try to import speech_recognition, fallback to alternative
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    #print(voices)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takeCommand():
    if SPEECH_RECOGNITION_AVAILABLE:
        try:
            import pyaudio
            return takeCommandOriginal()
        except ImportError:
            pass
    
    # Fallback: Use sounddevice for audio capture
    return takeCommandAlternative()

def takeCommandOriginal():
    """Original implementation using speech_recognition"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)
    
    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en')
        print(f'User said: {query}')
        time.sleep(2)
        eel.DisplayMessage(query)
    except Exception as e:
        return ""
    
    return query.lower()

def takeCommandAlternative():
    """Alternative implementation using sounddevice"""
    print('Listening...')
    eel.DisplayMessage('Listening...')
    
    try:
        # Record audio for 5 seconds
        duration = 5
        sample_rate = 16000
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        
        # Convert to 16-bit PCM
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_path = tmp_file.name
            with wave.open(tmp_path, 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_int16.tobytes())
        
        # Try to use Google Speech Recognition via speech_recognition
        # If that fails, return empty string
        try:
            r = sr.Recognizer()
            with sr.AudioFile(tmp_path) as source:
                audio = r.record(source)
            query = r.recognize_google(audio, language='en')
            print(f'User said: {query}')
            time.sleep(2)
            eel.DisplayMessage(query)
            os.unlink(tmp_path)
            return query.lower()
        except Exception as e:
            print(f"Recognition failed: {e}")
            os.unlink(tmp_path)
            return ""
            
    except Exception as e:
        print(f"Audio capture failed: {e}")
        return ""

# text = takeCommand()

# speak(text)
@eel.expose
def allCommands():
    query = takeCommand()
    print(query)

    if 'open' in query:
        from engine.features import openCommand
        openCommand(query)

    elif 'on youtube':
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        print('Not run')


    eel.ShowHood()

@eel.expose
def ProcessTextCommand(query):
    """Process text input from the chatbox"""
    if not query or query.strip() == "":
        return
    
    query = query.lower().strip()
    print(f"Text command: {query}")
    eel.DisplayMessage(query)
    
    if 'open' in query:
        from engine.features import openCommand
        openCommand(query)
    elif 'on youtube' in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        # For other queries, use Hugging Face API for response
        from engine.features import chatWithAI
        chatWithAI(query)
    
    eel.ShowHood()

    