from flask import Flask, render_template, request, send_from_directory
from summarize import summarize_text

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    summary = {"timestamp": "Today", "text": "Hello World!"}  # Just some example data
    if request.method == "POST":
        # Here you can add logic to change the summary based on user input, if you want
        article_choice = request.form.get("article")
        summary["text"] = "You selected: " + article_choice  # Just an example
    return render_template("dashboard.html", summary=summary)


@app.route("/pictures/<filename>")
def serve_image(filename):
    return send_from_directory("pictures", filename)


if __name__ == "__main__":
    app.run(debug=True)
