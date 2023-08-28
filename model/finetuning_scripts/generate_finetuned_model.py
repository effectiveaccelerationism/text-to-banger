import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a file for the fine-tuning data
openai.File.create(
  file=open("data/final/bangers_finetuning_data.json", "rb"),
  purpose='fine-tune'
)

# Create a fine-tuning job
openai.FineTuningJob.create(training_file="text-to-banger-v2", model="gpt-3.5-turbo")
