import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a file for the fine-tuning data
training_file = openai.File.create(
  file=open("data/final/bangers_finetuning_data_prepared_chat.jsonl", "rb"),
  purpose='fine-tune'
)

# Create a fine-tuning job
openai.FineTuningJob.create(training_file=training_file.id, 
                            model="gpt-3.5-turbo", 
                            suffix="text-to-banger-chat-v2")
