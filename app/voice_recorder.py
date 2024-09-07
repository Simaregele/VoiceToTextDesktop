from PyQt6.QtCore import QThread, pyqtSignal
import pyaudio
import wave
from openai import OpenAI
from app.config import get_config_value
import os
import logging


class VoiceRecorderThread(QThread):
    finished = pyqtSignal(str)
    update_time = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        logging.debug("Инициализация VoiceRecorderThread")
        self.frames = []
        api_key = get_config_value('OPENAI_API_KEY', 'YOUR_DEFAULT_API_KEY')
        self.client = OpenAI(api_key=api_key)
        self.is_recording = True
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.TEMP_AUDIO_FILE = get_config_value('TEMP_AUDIO_FILE', 'temp_audio_')
        self.CHUNK_DURATION = 60  # длительность чанка в секундах

    def run(self):
        logging.debug("Запуск потока записи")
        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

            logging.info("Начало записи")
            seconds = 0
            while self.is_recording:
                data = stream.read(self.CHUNK)
                self.frames.append(data)
                if len(self.frames) % (self.RATE // self.CHUNK) == 0:
                    seconds += 1
                    self.update_time.emit(seconds)
                    logging.debug(f"Записано секунд: {seconds}")

            logging.info("Запись завершена")

            stream.stop_stream()
            stream.close()
            p.terminate()

            self.save_and_transcribe()
        except Exception as e:
            logging.error(f"Ошибка во время записи: {e}")

    def save_and_transcribe(self):
        logging.debug("Сохранение аудио и транскрибирование")
        try:
            chunks = self.split_into_chunks()
            transcriptions = []

            for i, chunk in enumerate(chunks):
                chunk_file = f"{self.TEMP_AUDIO_FILE}{i}.wav"
                self.save_chunk(chunk, chunk_file)

                with open(chunk_file, "rb") as audio_file:
                    transcription = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                transcriptions.append(transcription.text)

                os.remove(chunk_file)
                logging.debug(f"Чанк {i} транскрибирован и удален")

            full_transcription = " ".join(transcriptions)
            logging.debug(f"Полная транскрипция: {full_transcription}")

            self.finished.emit(full_transcription)
        except Exception as e:
            logging.error(f"Ошибка при сохранении или транскрибировании: {e}")

    def split_into_chunks(self):
        frames_per_chunk = self.CHUNK_DURATION * self.RATE // self.CHUNK
        return [self.frames[i:i + frames_per_chunk] for i in range(0, len(self.frames), frames_per_chunk)]

    def save_chunk(self, chunk, filename):
        wf = wave.open(filename, "wb")
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(chunk))
        wf.close()

    def stop(self):
        logging.debug("Остановка записи")
        self.is_recording = False