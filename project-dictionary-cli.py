import json
from difflib import get_close_matches, SequenceMatcher

data = json.load(open("../words/data.json"))

history = []

def save_history_to_file(history):
    with open("history.txt", "a", encoding="utf-8") as file:
        for i, (word, meanings) in enumerate(history, 1):
            file.write(f"{i}. {word}\n")
            for j, meaning in enumerate(meanings, 1):
                file.write(f"   {j}) {meaning}\n")
        file.write("-" * 40 + "\n")

def describe(word):
    if word.capitalize() in data:
        return data[word.capitalize()]

    if word.upper() in data:
        return data[word.upper()]

    word = word.lower()

    if word in data:
        return data[word]

    elif get_close_matches(word, data.keys()):
        word_list = get_close_matches(word, data.keys(), 10)

        print("Did you mean one of these words?")
        for index, item in enumerate(word_list, 1):
            ratio = round(SequenceMatcher(None, word, item).ratio(), 4) * 100
            print(f"{index}. {item} ({ratio:.2f}%)")

        while True:
            opt = input("Choose option number: ")
            if not opt.isdigit():
                print("Please enter a number.")
                continue

            opt = int(opt)
            if 1 <= opt <= len(word_list):
                chosen_word = word_list[opt - 1]
                print(f"Chosen word: {chosen_word}")
                return data[chosen_word]
            else:
                print(f"Please choose between 1 and {len(word_list)}.")
    else:
        return ["Can't find the word."]


while True:
    user_input = input("Enter a word (or type 'exit' to quit): ").strip()

    if user_input.lower() == "exit":
        save_history_to_file(history)
        print("History saved to file. Exiting program...")
        break

    result = describe(user_input)

    history.append((user_input, result))

    print("Definition(s):")
    for i, definition in enumerate(result, 1):
        print(f"{i}. {definition}")
