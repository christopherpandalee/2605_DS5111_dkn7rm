from dotenv import load_dotenv

if load_dotenv():
    load_dotenv()
#else:
#    logging.info("No .env file set up.")

print(load_dotenv(override=True))
