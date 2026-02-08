from flask import Flask, render_template, request
import os
import threading
import webbrowser
import random

app = Flask(__name__)

ME_IMAGES = [
    "me1.jpeg",
    "me2.JPG",
    "me3.JPG",
    "me4.JPG",
]
CAT_IMAGES = [
    "cat1.jpeg",
    "cat2.jpeg",
]

TRAP_MESSAGES = [
    "I knew you would pick the cat. Nice try 😌",
    "I see where your priorities are.",
    "You chose… betrayal.",
    "The cat has been notified.",
    "The cat says hi. Also, you failed the test.",
    "Plot twist: the cat wrote this test.",
]

INCOMPLETE_MESSAGES = [
    "Almost! You picked some, but not all. Try again.",
    "Close, but you missed a few. The cat is watching.",
    "Partial credit. Full heart requires all four.",
]

SUCCESS_MESSAGES = [
    "Correct choice. Will you be my Valentine?",
    "Flawless. A+ Valentine behavior.",
    "You passed the vibe check. Be my Valentine?",
]


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


@app.route("/", methods=["GET"])
def index():
    images = ME_IMAGES + CAT_IMAGES
    random.shuffle(images)
    return render_template("index.html", images=images)


@app.route("/submit", methods=["POST"])
def submit():
    selected = request.form.getlist("selected")
    selected_set = set(selected)

    picked_cat = any(img in selected_set for img in CAT_IMAGES)
    picked_all_me = all(img in selected_set for img in ME_IMAGES) and len(selected_set) == len(ME_IMAGES)

    if picked_cat:
        message = random.choice(TRAP_MESSAGES)
        return render_template("result.html", success=False, message=message)

    if not picked_all_me:
        message = random.choice(INCOMPLETE_MESSAGES)
        return render_template("result.html", success=False, message=message, incomplete=True)

    message = random.choice(SUCCESS_MESSAGES)
    return render_template("result.html", success=True, message=message)


@app.route("/answer", methods=["POST"])
def answer():
    choice = request.form.get("choice", "")
    if choice == "yes":
        message = "I'll take it. We'll work on the energy next week ;)"
    else:
        message = "LOVE THE ENERGY. Keep it up till next week ;)"

    return render_template("final.html", message=message)


if __name__ == "__main__":
    auto_open = os.environ.get("AUTO_OPEN", "1") == "1"
    running_on_render = bool(os.environ.get("RENDER") or os.environ.get("RENDER_SERVICE_ID"))
    if auto_open and not running_on_render:
        threading.Timer(1.0, open_browser).start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
