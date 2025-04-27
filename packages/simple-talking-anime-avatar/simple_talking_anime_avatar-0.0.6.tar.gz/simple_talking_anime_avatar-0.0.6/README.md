# simple_talking_anime_avatar
Simple python package to generate talking anime avatar video.

![Talking avatar example](https://github.com/snow884/simple_talking_anime_avatar/raw/master/speaking_avatar_example.gif "Speaking avatar gif")

## Installation

```
pip install simple_talking_anime_avatar
```

## Usage

Here is how to use this package to generate an image of a woman pronuncing the letter 'u'
```
import cv2

from src.simple_talking_anime_avatar.avatar_gen import get_image_speaking

image_avatar_speaking_u = get_image_speaking("u")
cv2.imwrite("speaking_avatar_u.png", image_avatar_speaking_u)
```

This will generate an image looking something like this:

![Pronuncing u](https://github.com/snow884/simple_talking_anime_avatar/raw/master/speaking_avatar_u.png "Pronuncing u")

Here is how to generate the video at the top using the library pyttsx3. Note that pyttsx3 works differently on different systems. There is also other packages for generating speech from text.
```

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
```