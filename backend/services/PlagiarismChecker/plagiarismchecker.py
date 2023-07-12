from flask import request, jsonify, Blueprint
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import re
from pylatexenc.latex2text import LatexNodes2Text

plagiarismCheckerBlueprint = Blueprint('PlagiarismChecker',__name__)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

GOOGLE_API_KEY = 'AIzaSyCa6wGu9Cg3kN9l9KIOWg9BnFup9WraN4o'
SEARCH_ENGINE_ID = '82b92bb892ad94a2b'

def preprocess_text(text):
    # Remove LaTeX commands and special characters
    text = re.sub(r'\\[^a-zA-Z]+\{[^\}]+\}', '', text)
    text = re.sub(r'\\[^a-zA-Z]+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Return preprocessed text
    return ' '.join(tokens)

def calculate_similarity(text1, text2):
    # Preprocess the texts
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)

    # Vectorize the preprocessed texts
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])

    # Calculate cosine similarity between the vectors
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    return similarity

def search_text(query):
    url = f'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}'
    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        search_results = [item['snippet'] for item in data['items']]
        return search_results

    return []

def convert_latex(latex_code):
    text = LatexNodes2Text().latex_to_text(latex_code)
    return text

def check_plagiarism_with_search(latex_doc, threshold=0, num_results=5):
    search_results = search_text(latex_doc)[:num_results]

    similarity_scores = []
    for result in search_results:
        similarity = calculate_similarity(latex_doc, result)
        similarity_scores.append(similarity)
    if len(similarity_scores) > 0:
        average_similarity = sum(similarity_scores) / len(similarity_scores)
    else:
        average_similarity = 0
    if average_similarity >= threshold:
        return True, average_similarity
    else:
        return False, average_similarity

@plagiarismCheckerBlueprint.route('/api/check-plagiarism', methods=['POST'])
def plagiarism_check():
    latex_document = request.json.get("latex_code")
    text = convert_latex(latex_document)
    is_plagiarized = False
    score = 0
    try:
        is_plagiarized, score = check_plagiarism_with_search(text)
    except Exception as e:
        print(e)
    finally:
        response = {
            'is_plagiarized': is_plagiarized,
            'score': score
        }
        return jsonify(response)