# Categories

The `categories.json` file acts as a config file for the `Categories.py` module (and by extension, to `Disaster.py`)

## Structure
The idea is the following:
- Each category is a 'type' the new can fall into. (eg: flood, earthquake, etc)
- Each category acs as a key to a list of questions especific to said category. For example, 
if the new belongs to the earthquake cateogry, one migth want to ask for its magnitude.

Each question will be a dictionary containing 3 string fields:
- `"parameter_name"`: Name of the parameter (eg: `"Lethal victims"`)
- `"question"`: Question the AI must answer (eg: `"How many people died?"`)
- `"format"`: Format the answer is expected to be in (eg: `"int"`)

Note: rn the only implemented formats are strings (str), integers (int), and dates (date)

## Examples
For examples check the presets in `categories.json`