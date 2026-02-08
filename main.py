import time
from src.ask_ai import ask

QUESTION = "Who are you"
start = time.time()
ans = ask(QUESTION)
print("ans: ", ans, time.time() - start)
