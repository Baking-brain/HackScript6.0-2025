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

# Data class for structured sentiment results
class SentimentResult:
    def __init__(self, scores: Dict[str, float], entities: Dict[str, float]):
        self.positive = scores["pos"]
        self.neutral = scores["neu"]
        self.negative = scores["neg"]
        self.compound = scores["compound"]
        self.label = self.get_label(scores["compound"])
        self.entity_analysis = entities  # Named entity-based sentiment

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
            "entity_analysis": self.entity_analysis
        }

class AudioSentimentAnalyzer:
    def __init__(self, whisper_model_size: str = "base", sentiment_model: str = "vader", output_dir: str = "results", language: Optional[str] = None):
        self.whisper_model_size = whisper_model_size
        self.sentiment_model_name = sentiment_model
        self.output_dir = Path(output_dir)
        self.language = language
        
        # Create necessary directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "json").mkdir(exist_ok=True)
        (self.output_dir / "transcripts").mkdir(exist_ok=True)
        (self.output_dir / "visualizations").mkdir(exist_ok=True)

        # Load Whisper model
        logger.info(f"Loading Whisper model: {whisper_model_size}")
        self.whisper_model = whisper.load_model(whisper_model_size)

        # Load sentiment analysis model
        self._load_sentiment_model(sentiment_model)

        # Load Named Entity Recognition (NER) model
        logger.info("Loading Named Entity Recognition (NER) model")
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

    def _load_sentiment_model(self, model_name: str) -> None:
        if model_name == "vader":
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        elif model_name == "transformers":
            self.sentiment_analyzer = pipeline("sentiment-analysis")
        else:
            raise ValueError(f"Unsupported sentiment model: {model_name}")

    def analyze_sentiment(self, text: str) -> SentimentResult:
        if self.sentiment_model_name == "vader":
            scores = self.sentiment_analyzer.polarity_scores(text)
        elif self.sentiment_model_name == "transformers":
            result = self.sentiment_analyzer(text)[0]
            scores = {"compound": result["score"], "pos": 0, "neu": 0, "neg": 0}
            if result["label"] == "POSITIVE":
                scores["pos"] = result["score"]
            else:
                scores["neg"] = result["score"]
        else:
            scores = {"compound": 0, "pos": 0, "neu": 1, "neg": 0}

        entities = self.extract_named_entities(text)
        return SentimentResult(scores, entities)
    
    def extract_named_entities(self, text: str) -> Dict[str, float]:
        entities = self.ner_pipeline(text)
        entity_sentiments = {entity['word']: np.random.uniform(-1, 1) for entity in entities}  # Simulated sentiment values
        return entity_sentiments

    def transcribe_audio(self, audio_path: str) -> Tuple[str, float, str]:
        try:
            result = self.whisper_model.transcribe(audio_path, language=self.language, verbose=False)
            return result["text"], result["segments"][0]["end"], result.get("language", "en")
        except Exception as e:
            logger.error(f"Error transcribing {audio_path}: {str(e)}")
            return "", 0.0, "unknown"

    def process_file(self, audio_path: str) -> Optional[Dict]:
        try:
            logger.info(f"Processing {audio_path}")
            transcription, duration, detected_language = self.transcribe_audio(audio_path)
            if not transcription:
                logger.warning(f"No transcription generated for {audio_path}")
                return None

            sentiment_result = self.analyze_sentiment(transcription)

            result_data = {
                "file": audio_path,
                "transcription": transcription,
                "sentiment": sentiment_result.label,
                "entities": sentiment_result.entity_analysis,
                "duration": duration,
                "language": detected_language
            }

            # Save JSON result
            json_output_path = self.output_dir / f"json/{Path(audio_path).stem}.json"
            with open(json_output_path, "w") as f:
                json.dump(result_data, f, indent=4)

            logger.info(f"Processed {audio_path} successfully. Results saved to {json_output_path}")
            return result_data
        except Exception as e:
            logger.error(f"Error processing {audio_path}: {str(e)}")
            return None

    def generate_report(self, results: List[Dict]) -> None:
        if not results:
            logger.warning("No results to generate report from")
            return
        df = pd.DataFrame(results)
        df.to_csv(self.output_dir / "summary.csv", index=False)
        logger.info(f"Analysis complete. Results saved to {self.output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Audio Sentiment Analysis Tool")
    parser.add_argument("input", help="Path to an audio file to analyze")
    parser.add_argument("--sentiment_model", choices=["vader", "transformers"], default="vader", help="Choose sentiment model (vader or transformers)")
    args = parser.parse_args()

    analyzer = AudioSentimentAnalyzer(sentiment_model=args.sentiment_model)
    result = analyzer.process_file(args.input)

    if result:
        print(json.dumps(result, indent=2))
