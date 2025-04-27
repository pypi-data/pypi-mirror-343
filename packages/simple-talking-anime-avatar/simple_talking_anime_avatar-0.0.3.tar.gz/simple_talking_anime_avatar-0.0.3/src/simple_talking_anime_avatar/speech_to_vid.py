import cv2
import librosa
import whisper_timestamped as whisper
from whisper.tokenizer import get_tokenizer


def get_audio_duration(file_path):
    """
    Retrieves the duration of an audio file in seconds.

    Args:
      file_path: Path to the audio file.

    Returns:
      The duration of the audio file in seconds.
    """
    duration = librosa.get_duration(path=file_path)
    return duration


def get_speaker_video(output_video_path, audio_file_name, fps):
    """_summary_

    Args:
        output_video_path (_type_): _description_
        audio_file_name (_type_): _description_
        length_audio (_type_): _description_
        min_desired_length (_type_): _description_
        fps (_type_): _description_
    """
    tokenizer = get_tokenizer(
        multilingual=False
    )  # use multilingual=True if using multilingual model
    number_tokens = [
        i
        for i in range(tokenizer.eot)
        if (
            all(c in "0123456789" for c in tokenizer.decode([i]).removeprefix(" "))
            and len(tokenizer.decode([i]).strip()) > 0
        )
    ]
    audio_duration = get_audio_duration(audio_file_name)
    audio = whisper.load_audio(audio_file_name)
    model = whisper.load_model(
        "tiny"
    )  # Choose model size: tiny, base, small, medium, large
    data = whisper.transcribe(
        model, audio, language="en", suppress_tokens=[-1] + number_tokens
    )

    from avatar_gen import get_image_speaking

    # frame_height, frame_width, channels = cv_img.shape

    word_i = 0
    segment_id = 0

    img = get_image_speaking()
    height, width, layers = img.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for .mp4
    vid_out = cv2.VideoWriter(output_video_path, fourcc, fps, (height, width))

    pronunce_letter = " "

    for i_frame in range(0, (fps * audio_duration)):

        timestamp = i_frame / fps

        word_text = data["segments"][segment_id]["words"][word_i]["text"]
        word_start = data["segments"][segment_id]["words"][word_i]["start"]
        word_end = data["segments"][segment_id]["words"][word_i]["end"]

        # print(word_start)
        # print(word_end)

        if word_end <= timestamp:
            if word_i < len(data["segments"][segment_id]["words"]) - 1:
                word_i += 1
            else:
                if segment_id < len(data["segments"]) - 1:
                    segment_id += 1
                    word_i = 0

        if word_start <= timestamp and word_end > timestamp:
            letter_i = int(
                len(word_text) / (word_end - word_start) * (timestamp - word_start)
            )

            pronunce_letter = word_text[letter_i].lower()

            if len(word_text) > letter_i:
                if word_text[letter_i : letter_i + 2].lower() in [
                    "sh",
                    "th",
                    "ee",
                    "ch",
                ]:
                    pronunce_letter = word_text[letter_i : letter_i + 2].lower()

        else:
            pronunce_letter = " "

        frame = get_image_speaking(pronunce_letter)

        vid_out.write(frame)

    vid_out.release()


# dummy commit 5
