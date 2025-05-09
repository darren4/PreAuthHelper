from main_runner import process

import asyncio
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/completeform", methods=["POST"])
async def complete_form():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    audio_bytes = file.read()

    output = await process(audio_bytes)
    if not output:
        print(f"Error empty output")
        output = ""
    return {
        "output": output
    }

if __name__ == "__main__":
    app.run(debug=True)
