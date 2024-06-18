from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from typing import List
from phi.document import Document
from phi.document.reader.pdf import PDFReader
from phi.document.reader.website import WebsiteReader
from phi.utils.log import logger

from assistant import get_rag_assistant

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    llm_model = session.get('llm_model', 'llama3')
    embeddings_model = session.get('embeddings_model', 'nomic-embed-text')
    return render_template('index.html', llm_model=llm_model, embeddings_model=embeddings_model)

# @app.route('/set_model', methods=['POST'])
# def set_model():
#     session['llm_model'] = request.form['llm_model']
#     session['embeddings_model'] = request.form['embeddings_model']
#     session.pop('rag_assistant_run_id', None)
#     return redirect(url_for('home'))

@app.route('/upload_url', methods=['POST'])
def upload_url():
    input_url = request.form['input_url']
    if input_url:
        assistant = get_assistant()
        scraper = WebsiteReader(max_links=2, max_depth=1)
        web_documents: List[Document] = scraper.read(input_url)
        if web_documents:
            assistant.knowledge_base.load_documents(web_documents, upsert=True)
    return redirect(url_for('home'))

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return redirect(url_for('home'))
    uploaded_file = request.files['pdf_file']
    if uploaded_file:
        assistant = get_assistant()
        reader = PDFReader()
        rag_documents: List[Document] = reader.read(uploaded_file)
        if rag_documents:
            assistant.knowledge_base.load_documents(rag_documents, upsert=True)
    return redirect(url_for('home'))

@app.route('/clear_knowledge_base', methods=['POST'])
def clear_knowledge_base():
    assistant = get_assistant()
    assistant.knowledge_base.vector_db.clear()
    return redirect(url_for('home'))

@app.route('/new_run', methods=['POST'])
def new_run():
    session.pop('rag_assistant_run_id', None)
    return redirect(url_for('home'))

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.form['prompt']
    assistant = get_assistant()
    response = ""
    for delta in assistant.run(prompt):
        response += delta
    return jsonify({"response": response})

def get_assistant():
    llm_model = session.get('llm_model', 'llama3')
    embeddings_model = session.get('embeddings_model', 'nomic-embed-text')
    run_id = session.get('rag_assistant_run_id')
    assistant = get_rag_assistant(llm_model=llm_model, embeddings_model=embeddings_model, run_id=run_id)
    if 'rag_assistant_run_id' not in session:
        session['rag_assistant_run_id'] = assistant.run_id
    return assistant

if __name__ == '__main__':
    app.run(debug=True)
