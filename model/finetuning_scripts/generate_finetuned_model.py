import os
import time
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a file for the fine-tuning data
training_file = openai.File.create(
  file=open("data/final/bangers_finetuning_data_prepared_chat.jsonl", "rb"),
  purpose='fine-tune'
)

# Wait for the file to be processed
training_file = openai.File.retrieve(training_file.id)
while training_file.status != 'processed':
    training_file = openai.File.retrieve(training_file.id)
    print("File processing...")
    time.sleep(30)

# Create a fine-tuning job
ft_job = openai.FineTuningJob.create(training_file=training_file.id, 
                                     model="gpt-3.5-turbo", 
                                     suffix="text-to-banger-v2")

# Wait for the fine-tuning job to be processed
ft_job = openai.FineTuningJob.retrieve(ft_job.id)
print("Fine-tuning job started...")
print(ft_job)

while ft_job.status != 'succeeded':
    ft_job = openai.FineTuningJob.retrieve(ft_job.id)
    time.sleep(30)

print("Fine-tuned model finished training")
print(ft_job)
