# from simple_talking_anime_avatar import get_image_speaking, get_speaker_video

import cv2

from src.simple_talking_anime_avatar.avatar_gen import get_image_speaking
from src.simple_talking_anime_avatar.speech_to_vid import get_speaker_video

image_avatar_speaking_u = get_image_speaking("u")
cv2.imwrite("test.png", image_avatar_speaking_u)

import pyttsx3

engine = pyttsx3.init()

engine.save_to_file("Hello World", "test.wav")
engine.runAndWait()

get_speaker_video("test.mp4", "test.wav", 30)
