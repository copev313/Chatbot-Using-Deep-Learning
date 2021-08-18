import mongoengine as db
from dotenv import load_dotenv
import os


class Interactions(db.Document):
    user_message = db.StringField(required=True)
    bot_response = db.StringField(required=True)


def add_interaction(user_message: str, bot_response: str) -> None:
    try:
        load_dotenv()
        db.connect(host=os.environ.get('MONGO_HOST'))
        interaction = Interactions(
            user_message=user_message, bot_response=bot_response)
        interaction.save()

    except Exception as e: 
        print(e)

    finally:
        db.disconnect()
