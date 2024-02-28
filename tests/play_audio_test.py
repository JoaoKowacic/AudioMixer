import unittest
import numpy as np
import sounddevice as sd
import soundfile as sf
from unittest.mock import MagicMock
from mixer.play_audio import Play

class TestPlay(unittest.TestCase):

    def setUp(self):
        self.player = Play()

    def test_list_play_devices(self):
        # Mocking sd.query_devices to return a sample list of devices
        sd.query_devices = MagicMock(return_value=[
            {'name': 'Device 1', 'hostapi': 0, 'index': 0},
            {'name': 'Device 2', 'hostapi': 0, 'index': 1}
        ])
        devices = self.player.list_play_devices()
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]['name'], 'Device 1')
        self.assertEqual(devices[1]['name'], 'Device 2')

    def test_frequency_generator(self):
        frequency = 440  # 440 Hz
        fs = 44100  # 44.1 kHz
        duration = 1  # 1 second
        audio = self.player.frequency_generator(frequency, fs, duration)
        self.assertEqual(len(audio), fs * duration)

    def test_read_audio_file(self):
        # Provide a sample path to an audio file
        path = 'sample_audio.wav'
        audio_data = np.random.rand(44100)  # Generate random audio data
        sf.read = MagicMock(return_value=(audio_data, 44100))
        result = self.player.read_audio_file(path)
        self.assertTrue('audio' in result)
        self.assertTrue('fs' in result)
        self.assertEqual(len(result['audio']), len(audio_data))
        self.assertEqual(result['fs'], 44100)

    # Assuming that play_audio function depends on sd.OutputStream, it is better to mock it.
    def test_play_audio(self):
        fs = 44100  # Sample rate
        audio = np.random.randint(-32768, 32767, fs)  # Generate random audio data
        self.player.device = 0  # Set a sample device index
        with unittest.mock.patch('sounddevice.OutputStream') as mock_output_stream:
            mock_stream = MagicMock()
            mock_output_stream.return_value.__enter__ = MagicMock(return_value=mock_stream)
            self.player.play_audio(fs, audio)
            mock_stream.write.assert_called_once_with(audio)
            mock_stream.start.assert_called_once()

if __name__ == '__main__':
    unittest.main()