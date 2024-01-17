import openai

with open("news_samples.txt", errors="ignore") as stream:
    samples = stream.readlines()

with open("../gpt_keys/keys.txt") as stream:
    keys = list(map(lambda x: x.rstrip("\n", ), stream.readlines()))
    chat = openai.OpenAI(api_key=keys[0], organization=keys[1]).chat.completions

subtypes = ("Flood", "Drought", "Disease", "Earthquake")


def classify_new(new_dict_arg):
    classifier_client = openai.OpenAI(api_key=keys[0], organization=keys[1])
    response = classifier_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system",
                       "content": "You are a news articles classifying tool. The following messages will contain"
                                  "news articles parsed as python dictionaries, and you must classify them into one of "
                                  f"the following categories: {subtypes}\n."
                                  "Return a single string containing the category.\n"
                                  "Return 'None' if not sure"},
                  {"role": "user",
                   "content": new_dict_arg}])
    return response.choices[0].message.content


for sample in samples:
    print(f"Classifing {sample}")
    result = classify_new(sample.rstrip("\n"))
    print(result)
