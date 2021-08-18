import json
import pickle

import colorama
import numpy as np
from tensorflow import keras

from database import add_interaction

colorama.init()
from colorama import Fore, Style


# Load the intents data:
with open("intents.json") as json_file:
    data = json.load(json_file)


def chat():
    # Load the trained model:
    model = keras.models.load_model("chat_model")

    # Load the tokenizer object:
    with open("tokenizer.pickle", "rb") as handle:
        tokenizer = pickle.load(handle)

    # Load the label encoder object:
    with open("label_encoder.pickle", "rb") as enc:
        label_encoder = pickle.load(enc)

    # Define parameters:
    max_length = 20

    # Event loop:
    while True:
        # Console out user's input
        print(Fore.GREEN + "You: ", Style.RESET_ALL, end="")
        # Store 
        user_input = input()

        # Handle exit command:
        if (user_input.lower() in ['quit', 'exit', 'stop']):
            # Add the interaction to the database:
            add_interaction(user_input, 'Bye bye!')
            # Console out the exit message:
            print(Fore.LIGHTBLUE_EX + "Chatbot: " + Style.RESET_ALL,
                  "Bye bye!")
            break

        response = model.predict(keras.preprocessing.sequence.pad_sequences(
                                    tokenizer.texts_to_sequences([user_input]),
                                    maxlen=max_length,
                                    truncating='post')
                                 )
        tag = label_encoder.inverse_transform([np.argmax(response)])
        
        for i in data['intents']:
            if (i['tag'] == tag):
                # Pick a random response with the determined intent:
                bot_response = np.random.choice(i['responses'])
                # Add the interaction to the database:
                add_interaction(user_input, bot_response)
                # Console out the response:
                print(Fore.LIGHTBLUE_EX + "Chatbot: " + Style.RESET_ALL,
                      bot_response)


# Our driver code:
if __name__ == "__main__":
    # Print the welcome message:
    print(Fore.YELLOW + 
          "You can begin messaging the bot. Type 'quit' to end the session." +
          Style.RESET_ALL)

    # Launch our chat function:
    chat()
