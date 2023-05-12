import pyaudio
from pydub import AudioSegment
import wave

class MusicPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.stream = None

    def open_file(self):
        if self.filename.endswith('.mp3'):
            # 使用第三方库 Pydub 将 MP3 转换为 WAV
            pass
        elif self.filename.endswith('.wav'):
            self.wav_file = wave.open(self.filename, 'rb')
            self.sample_rate = self.wav_file.getframerate()
            self.channels = self.wav_file.getnchannels()
        else:
            raise Exception('Unsupported file type')

    def play(self):
        self.open_file()
        p = pyaudio.PyAudio()
        self.stream = p.open(format=p.get_format_from_width(self.wav_file.getsampwidth()),
            channels=self.channels,
            rate=self.sample_rate,
            output=True)

        data = self.wav_file.readframes(1024)
        while data:
            self.stream.write(data)
            data = self.wav_file.readframes(1024)

        self.stop()

    def stop(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.wav_file.close()

class NonBlockingPlayer:
    def __init__(self):
        self.file_path = None
        self.is_playing = False
        self.is_paused = False
        self.is_stopped = False
        self.audio_stream = None
        self.audio_segment = None
        self.sound_frame = 0
        self.p = pyaudio.PyAudio()

    def play(self, filePath):
        if (self.is_playing):
            self.is_stopped = True

        self.file_path = filePath
        self.audio_segment = AudioSegment.from_file(self.file_path)
        self.is_playing = True
        self.is_paused = False
        self.is_stopped = False
        self.audio_stream = self.p.open(
            format=self.p.get_format_from_width(self.audio_segment.sample_width),
            channels=self.audio_segment.channels,
            rate=self.audio_segment.frame_rate,
            output=True,
            stream_callback=self.callback
        )
        self.audio_stream.start_stream()

    def callback(self, in_data, frame_count, time_info, status):
        if self.stopped:
            return None, pyaudio.paComplete
        if self.paused:
            return bytes(frame_count * self.audio_segment.sample_width * self.audio_segment.channels), pyaudio.paContinue
        data = self.audio_segment.raw_data[self.audio_segment_frame:self.sound_frame + frame_count * self.sound.sample_width * self.sound.channels]
        self.sound_frame += frame_count * self.sound.sample_width * self.sound.channels
        if not data:
            self.stop()
            return None, pyaudio.paComplete
        return data, pyaudio.paContinue

    def callback(self, in_data, frame_count, time_info, status):
        if self.stopped:
            return None, pyaudio.paComplete
        if self.paused:
            return bytes(frame_count * self.sound.sample_width * self.sound.channels), pyaudio.paContinue
        data = self.sound_chunks[self.sound_frame].raw_data
        self.sound_frame += 1
        if self.sound_frame == len(self.sound_chunks):
            self.stop()
        return data, pyaudio.paContinue
    
    def pause(self):
        if self.is_playing and not self.is_paused:
            self.is_paused = True
            self.audio_stream.stop_stream()

    def resume(self):
        if self.is_playing and self.is_paused:
            self.is_paused = False
            self.audio_stream.start_stream()

    def stop(self):
        if self.is_playing:
            self.is_playing = False
            self.is_stopped = True
            if self.audio_stream is not None:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
                self.p.terminate()
# 测试
if __name__ == '__main__':
    file_path = 'test.mp3'
    player = NonBlockingPlayer(file_path)
    player.play()
    input("Press Enter to pause...")
    player.pause()
    input("Press Enter to resume...")
    player.resume()
    input("Press Enter to stop...")
    player.stop()

if __name__ == '__main__':
    player = MusicPlayer('test.mp3')
    player.play()
