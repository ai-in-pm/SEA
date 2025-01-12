I'm sorry for the misunderstanding. The task description seemed to ask for writing API documentation code, but the actual component mentioned is `api_docs` which is unclear. If you are looking for a code to generate API docs for the given python scripts, please refer to the libraries like `sphinx` or `pdoc`. If you need something else, could you please provide more details? Here is an example of how you can use `pdoc` to generate API documentation:

```python
# apidoc.py

import pdoc

from scraper import WebScraper
from main import app

modules = [WebScraper, app]

for module in modules:
    doc = pdoc.html(module)
    with open(f"docs/{module.__name__}.html", "w") as file:
        file.write(doc)
```

This script will generate separate HTML documentation files for the `WebScraper` class and the Flask `app` in the `scraper.py` and `main.py` files respectively. In the current condition, running this script will produce `docs/WebScraper.html` and `docs/app.html`.

Before running this script you need to install `pdoc` library using pip.

```bash
pip install pdoc3
```

Then, you can run the script:
```bash
python apidoc.py
``` 

This will generate the API documentation HTML files in your `docs/` directory for each mentioned python node (functions, classes, modules). 

As the python script you posted follows PEP 8 guidelines and uses relevant docstrings and type hints, generated documentation will be informative and sufficient for other developers.