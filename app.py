from flask import Flask, request, jsonify, send_file
import os


from model import OpenAIModel
from translator import PDFTranslator

app = Flask(__name__)


@app.route("/translate", methods=["POST"])
def translate():
    # Validate the file
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "" or not file.filename.endswith(".pdf"):
        return jsonify({"error": "No selected file or file is not a PDF"}), 400

    # Validate openaiModel
    openai_model = request.form.get("openaiModel")
    if not openai_model:
        return jsonify({"error": "openaiModel parameter is required"}), 400

    # Validate targetLanguage
    target_language = request.form.get("targetLanguage")
    if not target_language:
        return jsonify({"error": "targetLanguage parameter is required"}), 400

    model = OpenAIModel(model=openai_model, api_key=os.getenv("OPENAI_API_KEY"))
    translator = PDFTranslator(model)
    translated_pdf = translator.translate_pdf(file, target_language=target_language)

    return send_file(
        translated_pdf,
        as_attachment=True,
        download_name=f"{file.filename}_translated.pdf",
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    app.run(debug=True)
