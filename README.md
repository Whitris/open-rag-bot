# Open RAG Chatbot

A modular chatbot framework powered by Retrieval-Augmented Generation (RAG).
Ask questions about your documents and get context-aware, LLM-generated answers.

## Features

- **Retrieval-Augmented Generation (RAG):** Answers are grounded in your own documents, not just LLM training data.
- **Modular design:** Switch between different LLM and embedding providers (OpenAI, Groq, etc.) with a single config change.
- **Flexible document ingestion:** Easily add your PDFs or text files to the knowledge base.
- **Fast search:** Uses FAISS for efficient vector search and retrieval.
- **Two interfaces:** Use from the command line (CLI) or via a modern Streamlit webapp.
- **Tested and extensible:** Includes unit tests and a clean codebase for easy customization.

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/rag-chatbot.git
cd rag-chatbot
```

### 2. Install dependencies (recommended: PDM)

```bash
pip install pdm
pdm install
```

If you prefer classic pip:

```bash
pip install -r requirements.txt
```

### 3. Configure environment
Copy .env.example to .env and add your API keys (see instructions in the next section).

### 4. Prepare your documents
Place your PDF or text files in the folder specified by input_dir (see src/config/settings.py or .env).

### 5. Build the index

```bash
pdm run python -m src.cli build-index
```

### 6. Start the chatbot

Command-line interface (CLI)
```bash
pdm run python -m src.cli chat "What is the deadline for application?"
```

Webapp
```bash
pdm run streamlit run src/app/main.py
```

## Environment variables

All sensitive settings (like API keys and provider selection) are managed via environment variables.

- Copy the example file:
```bash
cp src/config/.env.example src/config/.env
```
- Edit src/config/.env to add your credentials and preferences.

### Main variables  
| Variable             | Description                       | Example      |
|----------------------|-----------------------------------|--------------|
| OPENAI_API_KEY       | Your OpenAI API key               | sk-...       |
| GROQ_API_KEY         | Your Groq API key                 | gsk_...      |
| EMBEDDING_PROVIDER   | Embedding provider to use         | openai/groq  |
| LLM_PROVIDER         | LLM provider to use               | openai/groq  |


Other settings (such as file paths) can be changed in src/config/settings.py or overridden with environment variables if needed.

## Folder structure

```markdown
rag-chatbot/
│
├── src/
│ ├── app/ # Streamlit webapp
│ ├── core/ # Core logic: retrieval, prompt, loader
│ ├── services/ # LLM & embedding clients (OpenAI, Groq, etc)
│ ├── data/ # Data processing scripts and utilities
│ └── config/ # Settings, .env, config files
│
├── tests/ # Unit and integration tests
├── data/ # Local, non-versioned data (indexed files, outputs)
├── requirements.txt
├── pyproject.toml
├── README.md
└── .gitignore
```

## Test and development

This project includes unit and integration tests to ensure correctness and maintainability.

### Running tests

To run all tests with [pytest](https://pytest.org/):

```bash
pdm run pytest
```

or, if using classic pip:

```bash
pytest
```

### Code style

We recommend using [ruff](https://docs.astral.sh/ruff/) and [black](https://black.readthedocs.io/en/stable/) for linting and formatting (optional):

```bash
pdm add --dev black ruff
pdm run black src/ tests/
pdm run ruff src/ tests/
```

## Contributing

Contributions, suggestions, and pull requests are welcome!  
If you find a bug or want to propose an enhancement, open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.

## Contact

For questions, suggestions, or professional inquiries:

- GitHub issues: [GitHub Issues](https://github.com/whitris/open-rag-chatbot/issues)
- Email: <nicola.marcantognini@outlook.com>
- LinkedIn: [My LinkedIn Profile](https://www.linkedin.com/in/nicola-marcantognini/)

Feel free to open an issue or reach out directly!

## Credits

Built by [Whitris](https://github.com/Whitris).

This project makes use of:
- [Streamlit](https://streamlit.io/) for the web interface
- [FAISS](https://github.com/facebookresearch/faiss) for vector search
- [Typer](https://typer.tiangolo.com/) for the CLI
- [OpenAI](https://platform.openai.com/) and [Groq](https://console.groq.com/) APIs for LLM and embeddings


![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![MIT License](https://img.shields.io/badge/license-MIT-green.svg)

