import subprocess
from unittest.mock import patch
import pytest
import os
from utils.voice import VoiceUtil

##os.environ["WHISPER_HOME"] = 'Path_of_whisper.cpp'
print(os.getenv('WHISPER_HOME'))

@pytest.mark.skip(reason="Test disabled")
def test_voice_to_text():
   
    test_file_dir = os.path.dirname(__file__)
    expected_text="transcribed text"
    audio_file = f'{test_file_dir}/test-audio.mp3'

    with open(f'{test_file_dir}/test-transcript.txt', 'r') as file:
        expected_text = file.read().strip()
    
    
    # Act
    result = VoiceUtil.voice_to_text(audio_file).strip()
    # Assert
    similarity = len(set(result.split()) & set(expected_text.split())) / float(len(set(expected_text.split())))
    assert similarity >= 0.8, f"Expected at least 80% similarity, but got {similarity * 100:.2f}%"
