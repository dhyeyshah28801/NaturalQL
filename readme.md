Certainly! Here is your `README.md` in markdown format, ready to use:

```markdown
# Audio-to-SQL Database Manager

A Streamlit application that lets you record natural language audio queries, transcribe them to text, generate SQL using LLMs, and visualize the results from your database-all with multi-database support and schema-aware context reduction.

---

## Features

- 🎤 **Record Audio:** Simple Streamlit UI for recording/uploading audio queries.
- 📝 **Speech-to-Text:** Transcribe queries using advanced ASR models (e.g., Wav2Vec).
- 🗄️ **Multi-DB Support:** Connects to SQLite, MySQL, or PostgreSQL using environment variables.
- 📊 **Visualize Data:** Interactive bar, line, and pie charts for query results.
- 🧠 **Schema-Aware SQL Generation:** Extracts and reduces database schema context for accurate, efficient LLM-powered SQL generation.
- 🛠️ **Error Handling:** Robust error handling and user feedback throughout the workflow.

---

## How It Works

1. **Database Initialization:**  
   The app reads environment variables to connect to your chosen database (SQLite/MySQL/PostgreSQL).

2. **Audio Recording:**  
   Users record or upload an audio query via the Streamlit interface.

3. **Transcription:**  
   The audio is transcribed into text using a speech recognition model.

4. **Schema Extraction & Reduction:**  
   The current database schema is fetched and reduced to relevant tables/columns based on the transcription.

5. **SQL Generation:**  
   The reduced schema and transcription are sent to an LLM, which generates an appropriate SQL query.

6. **Query Execution & Visualization:**  
   The SQL is executed, and results are displayed as interactive charts and tables.

---

## Setup

### 1. Clone the Repository

```
git clone https://github.com/yourusername/audio-to-sql-db-manager.git
cd audio-to-sql-db-manager
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file (or set these in your environment):

```
# Choose one: sqlite, mysql, or postgresql
DB_TYPE=sqlite (Other options include mysql and postgresql)

# SQLite
API_KEY= YOUR_API_KEY

DB_TYPE=mysql # Currently supporting mysql and postgresql

# For SQLite Database
SQLITE_PATH=./data/dataset.db #Path from root of the project

# FOR SQL DBs
DB_USER=root # Update with actual username
DB_PASSWORD=root # Update with actual password
DB_HOST=localhost # Update with actual host
DB_PORT=3306 # Update with actual port
DB_NAME=nuestro_amazon # Update with actual database name
```

### 4. Run the App

```
streamlit run app.py
```

---

## Example Usage

1. Open the Streamlit app in your browser.
2. Record or upload an audio query (e.g., “Show the number of products in each category”).
3. View the transcribed text, generated SQL, and the resulting data visualization.

---

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── models/
│   ├── wav2vec.py         # ASR model and tokenizer
│   ├── schemaFetch.py     # Schema extraction logic
│   └── generator.py       # LLM-based SQL generation
├── data/
│   └── dataFetcher.py     # Database query utilities
├── requirements.txt
├── README.md
└── .env
```

---

## Extending & Customizing

- **Add new database support:** Extend the schema fetcher and connection logic.
- **Swap transcription model:** Replace or upgrade the ASR model in `models/wav2vec.py`.
- **Improve charting:** Add more visualization types or custom dashboards.

---

## License

MIT License

---

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [PyTorch](https://pytorch.org/)
- [OpenAI](https://openai.com/) or [Hugging Face Transformers](https://huggingface.co/transformers/)
- [pymysql](https://pymysql.readthedocs.io/en/latest/)
- [psycopg2](https://www.psycopg.org/)

---

**Enjoy querying your database with your voice!**
