import json
import os
import subprocess
import uuid

MODEL = "ggml-large-v3-turbo-q5_0.bin"

class VoiceUtil:


    @staticmethod
    def voice_to_text(audio_file):
        WHISPER_ROOT = os.getenv('WHISPER_HOME', os.getcwd())
        MODEL_PATH = f"{WHISPER_ROOT}/models/{MODEL}"
        WHISPER_CMD = f"{WHISPER_ROOT}/build/bin/whisper-cli"
        
        temp_dir =os.getenv('STORY_APP_HOME', os.getcwd())+'/tmp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        output_file = f"{temp_dir}/{uuid.uuid4()}"

        # Check if the file exists
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f'Model file not found: {MODEL_PATH} \n')

        if not os.path.exists(audio_file):
            raise FileNotFoundError(f'Audio file not found: {audio_file} \n')
        
        ## output format: json
        full_command = f"{WHISPER_CMD} -m {MODEL_PATH} -f {audio_file} -oj -nt -of {output_file} -l auto"

        # Execute the command
        process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Running command: {full_command}")
        # Get the output and error (if any)
        output, error = process.communicate()
        print(f"Outputs: {error} \n {output}")
        processed_str = ""
        if os.path.exists(f"{output_file}.json"):
            with open(f"{output_file}.json", 'r') as file:
                ## read the json file and get value from all "text" elements under "transcription" 
                processed_str = ' '.join([transcription['text'] for transcription in json.load(file)['transcription']])
            os.remove(f"{output_file}.json")
        return processed_str.strip()

