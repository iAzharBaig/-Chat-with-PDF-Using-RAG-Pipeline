from flask import Flask, render_template, request, jsonify
from web_pipeline import WebPipeline

app = Flask(__name__)
pipeline = WebPipeline()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingest', methods=['POST'])
def ingest():
    urls = request.json.get('urls', [])
    try:
        pipeline.ingest_data(urls)
        return jsonify({'status': 'success', 'message': 'Data ingested successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query', '')
    try:
        response = pipeline.handle_query(user_query)
        return jsonify({'status': 'success', 'response': response})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
