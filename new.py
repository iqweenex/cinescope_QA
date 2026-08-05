from dotenv import load_dotenv
import os

load_dotenv()

print("ADMIN_EMAIL:", os.getenv("ADMIN_EMAIL"))
print("ADMIN_PASSWORD:", os.getenv("ADMIN_PASSWORD"))