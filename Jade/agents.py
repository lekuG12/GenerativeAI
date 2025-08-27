import os
import pygame
import tempfile
from pathlib import Path

# Option 1: Use Windows SAPI (Built-in, Windows only)
def use_windows_sapi(text):
    """Use Windows Speech API - No API key required"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # Optional: Set voice properties
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Female voice (index 1)
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)
        
        engine.say(text)
        engine.runAndWait()
        print("Speech completed using Windows SAPI")
    except ImportError:
        print("pyttsx3 not installed. Run: pip install pyttsx3")
    except Exception as e:
        print(f"Error with Windows SAPI: {e}")



# # Option 3: Use Azure Cognitive Services (Free tier available)
# def use_azure_tts(text, subscription_key, region):
#     """Use Azure TTS - Requires free Azure account"""
#     try:
#         import azure.cognitiveservices.speech as speechsdk
        
#         speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
#         speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        
#         audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
#         synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
#         result = synthesizer.speak_text_async(text).get()
        
#         if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#             print("Speech completed using Azure TTS")
#         else:
#             print(f"Azure TTS error: {result.reason}")
            
#     except ImportError:
#         print("Azure Speech SDK not installed. Run: pip install azure-cognitiveservices-speech")
#     except Exception as e:
#         print(f"Error with Azure TTS: {e}")


if __name__ == "__main__":
    text = "Hello, this is a test from the alternative TTS solutions. It's great to be here."

    with open('D:/Smoke_IT/GenerativeAI/Jade/talker.txt', 'r') as outer:

        fileSpeech = outer.read()
    
    use_windows_sapi(fileSpeech)
        
    
    
    # Option 3: Azure TTS (Requires free Azure account)
    # azure_key = "your_azure_subscription_key"
    # azure_region = "your_azure_region"  # e.g., "eastus"
    # use_azure_tts(text, azure_key, azure_region)
    