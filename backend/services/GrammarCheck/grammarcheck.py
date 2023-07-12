from flask import Flask, render_template, request, jsonify, Blueprint
import requests
from language_tool_python import LanguageTool
from pylatexenc.latex2text import LatexNodes2Text

grammarCheckerBlueprint = Blueprint('GrammarChecker',__name__)
tool = LanguageTool('en-US')  # Create a LanguageTool instance

# LanguageTool API endpoint for grammar checking
api_url = 'https://languagetool.org/api/v2/check'


def convert_latex(latex_code):
    text = LatexNodes2Text().latex_to_text(latex_code)
    return text

@grammarCheckerBlueprint.route("/check-grammar", methods=["POST"])
def check_grammar():
    # Get the LaTeX document from the request
    latex_document = request.json.get("latex_code")
    # Convert LaTex to simple text
    text = convert_latex(latex_document)

    # Specify the parameters for the LanguageTool API
    params = {
        "text": text,
        "language": "en-US", # ONLY ENG SUPPORTED
        "disabledRules": "WHITESPACE_RULE"
    }

    # Send a POST request to the LanguageTool API
    response = requests.post(api_url, params=params)

    # Parse the response
    errors = response.json().get("matches")

    # Extract error details
    result = []
    for error in errors:
        result.append({
            "originalText": text,
            "message": error.get("message"),
            "context": error.get("context").get("text"),
            "offset": error.get("offset"),
            "length": error.get("length"),
            "result": {
                "incorrect-word": text[error.get("offset"): error.get("offset") + error.get("length")],
                "replacements": error.get("replacements", [])
                }
        })

    return jsonify(result), 200