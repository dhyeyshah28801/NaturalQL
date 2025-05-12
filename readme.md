# Audio-to-SQL Database Manager

Transform your voice into database queries! This Streamlit application allows you to record natural language audio, transcribe it, generate SQL using Large Language Models (LLMs), and visualize the results from your database. It features multi-database support and intelligent, schema-aware context reduction for accurate SQL generation.

---

## ✨ Features

-   🎤 **Record Audio:** Simple and intuitive Streamlit UI for recording or uploading audio queries.
-   📝 **Speech-to-Text:** Accurate transcription of audio queries using advanced ASR models (e.g., Wav2Vec).
-   🗄️ **Multi-DB Support:** Seamlessly connects to SQLite, MySQL, or PostgreSQL using environment variables.
-   📊 **Visualize Data:** Interactive bar, line, and pie charts to explore query results.
-   🧠 **Schema-Aware SQL Generation:** Extracts and reduces database schema context, feeding only relevant information to the LLM for efficient and precise SQL generation.
-   🛠️ **Error Handling:** Robust error handling and clear user feedback throughout the workflow.

---

## ⚙️ How It Works

1.  **Database Initialization:** The application reads environment variables to connect to your specified database (SQLite, MySQL, or PostgreSQL).
2.  **Audio Recording & Upload:** Users record their query using their microphone or upload an existing audio file via the Streamlit interface.
3.  **Transcription:** The uploaded/recorded audio is processed by a speech recognition model, converting speech to text.
4.  **Schema Extraction & Context Reduction:** The system fetches the current schema of the connected database. This schema is then intelligently reduced to include only tables and columns likely relevant to the transcribed query.
5.  **SQL Generation with LLM:** The transcribed query and the reduced, relevant schema context are provided to a Large Language Model (LLM), which generates the appropriate SQL query.
6.  **Query Execution & Visualization:** The generated SQL query is executed against the database. The results are then fetched and displayed to the user through interactive charts and tables.

---

## 🚀 Getting Started

### 1. Clone the Repository

```
git clone https://github.com/dhyeyshah28801/NaturalQL
cd audio-to-sql-db-manager
*(Replace `yourusername/audio-to-sql-db-manager.git` with your actual repository URL)*
```
### 2. Install Dependencies

It's recommended to create a virtual environment first:
```
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```
Then install the required packages:
```
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory of the project. This file will store your configuration settings. Below is a template; fill in the details relevant to your setup.

```
API_KEY=YOUR_API_KEY

DB_TYPE=mysql # Currently supporting mysql, sqlite and postgresql

// For SQLite Database
SQLITE_PATH=./data/dataset.db #Path from root of the project

// FOR SQL DBs
DB_USER=root # Update with actual username
DB_PASSWORD=root # Update with actual password
DB_HOST=localhost # Update with actual host
DB_PORT=3306 # Update with actual port
DB_NAME=nuestro_amazon # Update with actual database name
```

### 4. Run the Application
```

streamlit run app.py

```
The application should now be accessible in your web browser, usually at `http://localhost:8501`.

## 🔧 Extending & Customizing

-   **Database Support:** Add connectors for other SQL or NoSQL databases by extending `schemaFetch.py` and `dataFetcher.py`.
-   **ASR Model:** Experiment with different speech-to-text models or services by modifying `wav2vec.py`.
-   **LLM Integration:** Swap out the LLM or adjust prompting strategies in `generator.py`.
-   **Visualization:** Introduce new chart types or customize existing ones using Streamlit's rich component library.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details (if you have one, otherwise state the license).

---

## 🙏 Acknowledgments

-   [Streamlit](https://streamlit.io/) for the awesome app framework.
-   [PyTorch](https://pytorch.org/) and [Hugging Face Transformers](https://huggingface.co/transformers/) for model capabilities.
-   [OpenAI](https://openai.com/) (or other LLM providers) for language model integration.
-   Database connector libraries: [pymysql](https://pymysql.readthedocs.io/en/latest/), [psycopg2](https://www.psycopg.org/).

---

**Happy voice-querying!**