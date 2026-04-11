from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route("/")
def home():
    url = "https://meme-api.com/gimme/wholesomememes"
    response = requests.request("GET", url, timeout=10)

    meme_data = response.json() if response.ok else {}
    meme_url = meme_data.get("url", "")
    subreddit = meme_data.get("subreddit", "Unknown")

    return render_template("meme.html", meme_url=meme_url, subreddit=subreddit)

if __name__ == "__main__":
    app.run(debug=True)