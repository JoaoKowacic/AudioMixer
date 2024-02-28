import sounddevice as sd
import soundfile as sf
import numpy as np

class Play:
    def __init__(self) -> None:
        pass
    
    def list_play_devices(self) -> list:
        output_devices = sd.query_devices(kind='output')
        devices = []
        for output_device in output_devices:
            if output_device['hostapi'] == 0:
                devices.append({'name':output_device['name'], 'index': output_device['index']})
        
        return devices
    
    def define_device(self, device:int) -> None:
        self.device = device

    def frequency_generator(self, frequency:int, fs:int, duration:int) -> np.ndarray:
        t = np.linspace(0, duration, duration * fs, False)
        note = np.sin(frequency * t * 2 * np.pi)
        audio = note * (2**15 - 1) / np.max(np.abs(note))
        audio = audio.astype(np.int16)
        return audio
     
    def read_audio_file(self, path:str) -> dict:
        data, samplerate = sf.read(path)

        return {'audio': data, 'fs': samplerate}

    def play_audio(self, fs:int, audio:np.ndarray, dtype='int16') -> None:
        with sd.OutputStream(samplerate=fs, device=self.device, channels=2, dtype=dtype) as play:
            play.write(audio)
            play.start()
    