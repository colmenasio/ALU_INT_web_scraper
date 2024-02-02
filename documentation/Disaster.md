# Module: **Disaster**

<!--class_Disaster-->
## Class: `Disaster`
Each instance of this class will contain a single new. 
Its atributes act will ether contain data or be None, depending on the structure of the new.

The methods provided by the class are meant to use the defined attributes to "fill" 
the remaining ones in-place until the instance is ready to be sent to a database

Note that, for now, they type of news classified and they information extracted from said news 
is defined within the class attributes

### Use example:
Suppose we have a new and know nothing about it. We can initialize an instance:
```py
a = Disaster(raw_data_arg = {"title": title, "body": body})
```
Then we deduce the category fo the new:
```py
a.classify()
```
Now de are ready to extract the data in json format and send it to the database
```py
a.extract_data()
a.save_to_database()
```
If, for example, we knew beforehand that the thype of new was a "flood" new, 
we could have specified it during the instanciation and then `classify()` call 
would be innecesary
```py
a = Disaster(raw_data_arg = {"title": title, "body": body}, category_arg = "flood")
# a.classify() is no longer necessary
a.extract_data()
a.save_to_database()
```

### Instance Attributes
- `self.raw_data`: Dictionary with two keys: "title" and "body". Self-explanatory
- `self.category`: String containing the cateogry of the new
- `self.data_arg`: Json-formatted string ready to be sent to the database

<!--dependencies-->
## Dependencies (see .toml file)
- module: GptParser.py
- module: CustomException.py