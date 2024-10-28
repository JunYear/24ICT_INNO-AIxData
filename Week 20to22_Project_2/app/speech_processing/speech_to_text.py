import speech_recognition as sr
from pydub import AudioSegment

def convert_audio(file_path):
    print(f"Converting audio: {file_path}")
    sound = AudioSegment.from_file(file_path)
    sound = sound.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    converted_path = file_path.replace(".wav", "_converted.wav")
    sound.export(converted_path, format="wav")
    print(f"Converted audio saved at: {converted_path}")
    return converted_path

def speech_to_text(file_path):
    recognizer = sr.Recognizer()
    converted_path = convert_audio(file_path)
    audio_file = sr.AudioFile(converted_path)
    result_text = []

    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source)  # 주변 소음에 맞게 조정
        audio_length = source.DURATION  # 전체 오디오 길이 (초 단위)
        chunk_duration = 5  # 각 청크 길이를 5초로 설정

        # 오디오 파일을 청크 단위로 나누어 인식
        for i in range(0, int(audio_length), chunk_duration):
            audio = recognizer.record(source, duration=chunk_duration)
            try:
                text = recognizer.recognize_google(audio, language='ko-KR')
                result_text.append(text)
                print(f"Recognized text chunk: {text}")
            except sr.UnknownValueError:
                result_text.append("[인식 불가]")
                print("Chunk recognition failed.")
            except sr.RequestError as e:
                print(f"RequestError during recognition: {e}")
                return f"음성 인식 서비스에 접근할 수 없습니다.; {e}"

    final_text = ' '.join(result_text)
    print(f"Final recognized text: {final_text}")
    return final_text
