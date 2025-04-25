# July

Proof-of-Work (PoW) Security Measure to protect your flask apps from Bots and Scrapers

## Setup

Simply set up July in a Flask App by typing

```python
from flask import Flask
from flask_july import Flask_July

app = Flask(__name__)
app.config["SECRET_KEY"] = "Super Secret!"
july = Flask_July(app)
```

By default, once your app runs, it will show something like
![this](/img/1.png)

(Don't worry! Anything under /static is always allowed to be accessed)


But what if you don't wanna include *every* Path? Well, using the below code, you can set up exclusions

```py
july = Flask_July(app)


@july.validate
def validate_fn():
    if request.path.startswith("/no-bots-pls"): return True
```

In the Age of AI Scrapers, it's a feature that has *almost* been forgotten about, since it was only a sign, never a cop. However, in the Times of Web 2.0,
developers would put up a little something called "robots.txt".

Now, Flask-July was originally meant to be a solution that did not allow entry to *anywhere* except for explicitly allowed paths. However, I've come to the conclusion that it would be smart for July to allow entry to the places robots.txt allows.

```python
july = Flask_July(app, enable_robots=True, robotsfile="robots.txt", create_route=True) # Robots.txt should exist in that path.
# If "create_route" is set to true, July *will* create a route at /robots.txt, if not it won't.
```
