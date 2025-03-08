import os
import argparse
import json
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import numpy as np
import pandas as pd
import torch
import whisper
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Download necessary NLTK data
nltk.download('vader_lexicon', quiet=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sentiment_analyzer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("audio_sentiment")

class SentimentResult:
    def __init__(self, scores: Dict[str, float]):
        self.positive = scores["pos"]
        self.neutral = scores["neu"]
        self.negative = scores["neg"]
        self.compound = scores["compound"]
        self.label = self.get_label(scores["compound"])

    @staticmethod
    def get_label(compound: float) -> str:
        if compound >= 0.05:
            return "Positive"
        elif compound <= -0.05:
            return "Negative"
        return "Neutral"

    def to_dict(self):
        return {
            "positive": self.positive,
            "neutral": self.neutral,
            "negative": self.negative,
            "compound": self.compound,
            "label": self.label,
        }

class AudioSentimentAnalyzer:
    def __init__(self, whisper_model_size: str = "base", sentiment_model: str = "vader", output_dir: str = "results", language: Optional[str] = None):
        self.whisper_model_size = whisper_model_size
        self.sentiment_model_name = sentiment_model
        self.output_dir = Path(output_dir)
        self.language = language
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Loading Whisper model: {whisper_model_size}")
        self.whisper_model = whisper.load_model(whisper_model_size)

        self._load_sentiment_model(sentiment_model)

    def _load_sentiment_model(self, model_name: str) -> None:
        if model_name == "vader":
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        elif model_name == "transformers":
            self.sentiment_analyzer = pipeline("sentiment-analysis")
        else:
            raise ValueError(f"Unsupported sentiment model: {model_name}")

    def analyze_sentiment(self, text: str) -> SentimentResult:
        scores = self.sentiment_analyzer.polarity_scores(text) if self.sentiment_model_name == "vader" else {"compound": 0, "pos": 0, "neu": 1, "neg": 0}
        return SentimentResult(scores)
    
    def transcribe_audio(self, audio_path: str) -> List[Dict[str, str]]:
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

    def process_file(self, audio_path: str) -> Optional[Dict]:
        try:
            logger.info(f"Processing {audio_path}")
            conversation = self.transcribe_audio(audio_path)
            if not conversation:
                logger.warning(f"No transcription generated for {audio_path}")
                return None
            
            analyzed_conversation = []
            for entry in conversation:
                sentiment_result = self.analyze_sentiment(entry["text"])
                analyzed_conversation.append({
                    "speaker": entry["speaker"],
                    "text": entry["text"],
                    "sentiment": sentiment_result.to_dict()
                })
            
            result_data = {
                "file": audio_path,
                "conversation": analyzed_conversation
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
    parser = argparse.ArgumentParser(description="Audio Sentiment Analysis with Speaker Classification")
    parser.add_argument("input", help="Path to an audio file to analyze")
    parser.add_argument("--sentiment_model", choices=["vader", "transformers"], default="vader", help="Choose sentiment model (vader or transformers)")
    args = parser.parse_args()

    analyzer = AudioSentimentAnalyzer(sentiment_model=args.sentiment_model)
    result = analyzer.process_file(args.input)

    if result:
        print(json.dumps(result, indent=2))
