# Module: **GptParser**

<!--class_GptParser-->
## Class: `GptParser`
Class wrapping the `openai` api calls. (Thread safe i think).
This class is not meat to be instanciated.

Requires a set of keys to be provided in `root/gpt_keys`. 
If the keys are not provided a `FileNotFound` exception is raised during the initialization of the class

<!--methods-->
## Public Interface
### `classify(new_arg: dict, categories_arg: list) -> str | None:`
See docstring

### `extract_json(new_arg: dict, search_parameters_arg: list) -> str | None:`
See docstring

<!--dependencies-->
## Dependencies (see .toml file)
- openai API