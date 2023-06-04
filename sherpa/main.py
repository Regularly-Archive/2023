import sys

import speech_recognition as sr
from pathlib import Path
import os, json, time
import wave
import numpy as np

try:
    import sounddevice as sd
except ImportError as e:
    print("Please install sounddevice first. You can use")
    print()
    print("  pip install sounddevice")
    print()
    print("to install it")
    sys.exit(-1)

import sherpa_ncnn


def create_recognizer():
    # Please replace the model files if needed.
    # See https://k2-fsa.github.io/sherpa/ncnn/pretrained_models/index.html
    # for download links.
    recognizer = sherpa_ncnn.Recognizer(
        tokens="./sherpa-ncnn/sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23/tokens.txt",
        encoder_param="./sherpa-ncnn/sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23/encoder_jit_trace-pnnx.ncnn.param",
        encoder_bin="./sherpa-ncnn/sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23/encoder_jit_trace-pnnx.ncnn.bin",
        decoder_param="./sherpa-ncnn/sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23/decoder_jit_trace-pnnx.ncnn.param",
        decoder_bin="./sherpa-ncnn/sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23/decoder_jit_trace-pnnx.ncnn.bin",
        joiner_param="./sherpa-ncnn/sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23/joiner_jit_trace-pnnx.ncnn.param",
        joiner_bin="./sherpa-ncnn/sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23/joiner_jit_trace-pnnx.ncnn.bin",
        num_threads=4,
    )
    return recognizer


def main():
    print("Started! Please speak")
    recognizer = create_recognizer()
    sample_rate = recognizer.sample_rate
    samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms
    last_result = ""
    with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
        while True:
            samples, _ = s.read(samples_per_read)  # a blocking read
            samples = samples.reshape(-1)
            recognizer.accept_waveform(sample_rate, samples)
            result = recognizer.text
            if last_result != result:
                last_result = result
                print(result)

def main2():
    sherpa_recognizer = create_recognizer()
    recoginzer = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        result=[]
        recoginzer.adjust_for_ambient_noise(source, duration=1)
        audio = recoginzer.listen(source, timeout=120, phrase_time_limit=None)
        timestamp = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
        file_name = f"{timestamp}.wav"
        file_name = os.path.join(Path.home(), file_name)

        with open(file_name, "wb") as f:
            f.write(audio.get_wav_data())
        
        with wave.open(file_name) as f:
            # Note: If wave_file_sample_rate is different from
            # recognizer.sample_rate, we will do resampling inside sherpa-ncnn
            wave_file_sample_rate = f.getframerate()
            num_channels = f.getnchannels()
            assert f.getsampwidth() == 2, f.getsampwidth()  # it is in bytes
            num_samples = f.getnframes()
            samples = f.readframes(num_samples)
            samples_int16 = np.frombuffer(samples, dtype=np.int16)
            samples_int16 = samples_int16.reshape(-1, num_channels)[:, 0]
            samples_float32 = samples_int16.astype(np.float32)

            samples_float32 = samples_float32 / 32768

        # simulate streaming
            chunk_size = int(0.1 * wave_file_sample_rate)  # 0.1 seconds
            start = 0
            while start < samples_float32.shape[0]:
                end = start + chunk_size
                end = min(end, samples_float32.shape[0])
                sherpa_recognizer.accept_waveform(wave_file_sample_rate, samples_float32[start:end])
                start = end
                text = sherpa_recognizer.text
                if text:
                    result.append(text)

                # simulate streaming by sleeping
                time.sleep(0.1)

            tail_paddings = np.zeros(int(wave_file_sample_rate * 0.5), dtype=np.float32)
            sherpa_recognizer.accept_waveform(wave_file_sample_rate, tail_paddings)
            sherpa_recognizer.input_finished()
            text = sherpa_recognizer.text
            if text:
                result.append(text)

            print(''.join(result))


if __name__ == "__main__":
    devices = sd.query_devices()
    print(devices)
    default_input_device_idx = sd.default.device[0]
    print(f'Use default device: {devices[default_input_device_idx]["name"]}')

    try:
        main2()
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")