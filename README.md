# Local-RAG-Chat-Assistant
Local AI Assistant using flask and Ollama model (llama3)

## Setup
- First fork or clone the project
```sh
git clone https://github.com/cack195/Local-RAG-Chat-Assistant.git
```

### Install Ollama and Download Models
- Follow the [installation guide for Ollama](https://github.com/ollama/ollama?tab=readme-ov-file#macos).
- Next, download the language models (LLMs) you plan to use:

    ```sh
    ollama pull phi3
    ollama pull llama3
    ollama pull nomic-embed-text
    ```

### Set Up a Virtual Environment
- Create a Python virtual environment:

    ```sh
    python3 -m venv venv
    ```

- Activate the virtual environment:

    ```sh
    source venv/bin/activate
    ```

### Install Required Libraries
Install the necessary Python libraries:

```sh
pip install -r requirements.txt
```

### Start PgVector
Ensure [Docker Desktop](https://docs.docker.com/get-docker/) is installed first.
- Start PgVector using Docker:
```sh
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```
### launch the Application
- Run the following command
```sh
python3 app.py
```
- Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser to view the local RAG app.
- You can add websites or PDFs and ask questions.
