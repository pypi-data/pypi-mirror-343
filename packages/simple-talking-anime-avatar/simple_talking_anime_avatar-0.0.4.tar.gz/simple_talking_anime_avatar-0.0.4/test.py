# from simple_talking_anime_avatar import get_image_speaking, get_speaker_video

import cv2

from src.simple_talking_anime_avatar.avatar_gen import get_image_speaking

image_avatar_speaking_u = get_image_speaking("u")
cv2.imwrite("test.png", image_avatar_speaking_u)

import pyttsx3

from src.simple_talking_anime_avatar.speech_to_vid import get_speaker_video

engine = pyttsx3.init()
voices = engine.getProperty("voices")

engine.setProperty("rate", 110)

engine.setProperty("voice", "com.apple.voice.compact.en-AU.Karen")

engine.say("Hello everyone! This is a test of speaking avatar python package.")
engine.save_to_file(
    "Hello everyone! This is a test of speaking avatar python package.", "test.wav"
)
engine.runAndWait()

get_speaker_video("test.mp4", "test.wav", 30)
