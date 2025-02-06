import multiprocessing
import os
import openai

from dotenv import load_dotenv

load_dotenv()  # This loads the .env file into the environment

openai.api_key = os.getenv('OPENAI_API_KEY')

max_requests = 1000
max_requests_jitter = 50
log_file = "-"
bind = "127.0.0.1:50505"  # 50505

if os.getenv("RUNNING_IN_PRODUCTION"):
    workers = (multiprocessing.cpu_count() * 2) + 1
    threads = workers
else:
    reload = True
    workers = 2
    threads = 2

timeout = 120
