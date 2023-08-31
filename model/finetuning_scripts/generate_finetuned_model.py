import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a file for the fine-tuning data
openai.File.create(
  file=open("data/final/bangers_finetuning_data_prepared_chat.jsonl", "rb"),
  purpose='fine-tune'
)

# Create a fine-tuning job
openai.FineTuningJob.create(training_file="data/final/bangers_finetuning_data_prepared_chat.jsonl", model="gpt-3.5-turbo")
