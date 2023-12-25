import openai

with open("news_samples.txt") as stream:
    samples = stream.readlines()

with open("gpt_key.txt") as stream:
    keys = list(map(lambda x: x.rstrip("\n", ), stream.readlines()))
    chat = openai.OpenAI(api_key=keys[0], organization=keys[1]).chat.completions

subtypes = ("Flood", "Drought", "Disease")


def classify_new():
    """Consumer coroutine"""
    classifier = openai.OpenAI(api_key=keys[0],
                               organization=keys[1]).chat.completions
    classifier.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system",
                   "message": "You are a news articles classifying tool. The following messages will contain"
                              "news articles parsed as python dictionaries, and you must classify them into one of "
                              f"the following categories: {subtypes}\n."
                              "Return a single string containing the category.\n"
                              "Return 'None' if not sure"}]
    )
    # classifier_lock = Lock()  # i think it's not needed due to GIL
    while True:
        response = classifier.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                       "message": (yield)}]
        )


new_classifier = classify_new()
next(new_classifier)
for sample in samples:
    result = new_classifier.send(sample.rstrip("\n"))
    print(result.choices[0].message.content)