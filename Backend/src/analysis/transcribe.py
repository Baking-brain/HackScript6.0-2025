import os
import argparse
import json
import logging
from pathlib import Path
import whisper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("transcription.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("audio_transcription")

class AudioTranscriber:
    def __init__(self, whisper_model_size: str = "base", output_dir: str = "transcriptions", language: str = None):
        self.whisper_model_size = whisper_model_size
        self.output_dir = Path(output_dir)
        self.language = language
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Loading Whisper model: {whisper_model_size}")
        self.whisper_model = whisper.load_model(whisper_model_size)

    def transcribe_audio(self, audio_path: str):
        try:
            result = self.whisper_model.transcribe(audio_path, language=self.language, verbose=False)
            segments = result.get("segments", [])
            
            conversation = []
            for i, segment in enumerate(segments):
                text = segment["text"]
                speaker = "Bot" if i % 2 == 0 else "Human"
                conversation.append({"speaker": speaker, "text": text})
            
            return conversation
        except Exception as e:
            logger.error(f"Error transcribing {audio_path}: {str(e)}")
            return []

    def process_file(self, audio_path: str):
        try:
            logger.info(f"Processing {audio_path}")
            conversation = self.transcribe_audio(audio_path)
            if not conversation:
                logger.warning(f"No transcription generated for {audio_path}")
                return None
            
            result_data = {
                "file": audio_path,
                "conversation": conversation
            }
            
            json_output_path = self.output_dir / f"{Path(audio_path).stem}.json"
            with open(json_output_path, "w") as f:
                json.dump(result_data, f, indent=4)
            
            logger.info(f"Processed {audio_path} successfully. Results saved to {json_output_path}")
            return result_data
        except Exception as e:
            logger.error(f"Error processing {audio_path}: {str(e)}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Transcription with Speaker Classification")
    parser.add_argument("input", help="Path to an audio file to transcribe")
    args = parser.parse_args()

    transcriber = AudioTranscriber()
    result = transcriber.process_file(args.input)

    if result:
        print(json.dumps(result, indent=2))
