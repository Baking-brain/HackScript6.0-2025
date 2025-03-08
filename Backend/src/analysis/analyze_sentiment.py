import os
import argparse
import json
import logging
from pathlib import Path
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download necessary NLTK data
nltk.download('vader_lexicon', quiet=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sentiment_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("sentiment_analysis")

class SentimentAnalyzer:
    def __init__(self, output_dir: str = "sentiment_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text: str):
        scores = self.sentiment_analyzer.polarity_scores(text)
        label = "Positive" if scores["compound"] >= 0.05 else "Negative" if scores["compound"] <= -0.05 else "Neutral"
        return {"positive": scores["pos"], "neutral": scores["neu"], "negative": scores["neg"], "compound": scores["compound"], "label": label}

    def process_transcription(self, transcription_file: str):
        try:
            with open(transcription_file, "r") as f:
                transcription_data = json.load(f)
            
            conversation = transcription_data.get("conversation", [])
            analyzed_conversation = []
            
            for entry in conversation:
                sentiment = self.analyze_sentiment(entry["text"])
                analyzed_conversation.append({"speaker": entry["speaker"], "text": entry["text"], "sentiment": sentiment})
            
            result_data = {
                "file": transcription_data["file"],
                "conversation": analyzed_conversation
            }
            
            output_path = self.output_dir / f"{Path(transcription_file).stem}_sentiment.json"
            with open(output_path, "w") as f:
                json.dump(result_data, f, indent=4)
            
            logger.info(f"Sentiment analysis completed. Results saved to {output_path}")
            return result_data
        except Exception as e:
            logger.error(f"Error processing transcription {transcription_file}: {str(e)}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sentiment Analysis of Transcriptions")
    parser.add_argument("input", help="Path to a transcription JSON file")
    args = parser.parse_args()

    analyzer = SentimentAnalyzer()
    result = analyzer.process_transcription(args.input)

    if result:
        print(json.dumps(result, indent=2))
