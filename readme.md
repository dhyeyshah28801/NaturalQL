Audio-to-SQL Database Manager
Audio-to-SQL Database Manager is an interactive Streamlit application that empowers users to query their databases using natural language audio. The app transcribes speech to text, generates SQL with LLMs, executes the query, and visualizes the results-all with support for multiple database backends and intelligent schema context reduction.

🚀 Features
🎤 Audio Input: Record or upload audio queries directly in the browser.

📝 Speech-to-Text: Accurate transcription using advanced ASR models (e.g., Wav2Vec).

🗄️ Multi-Database Support: Connects to SQLite, MySQL, or PostgreSQL using environment variables.

🤖 LLM-powered SQL Generation: Translates natural language into SQL, leveraging schema context.

📉 Data Visualization: Interactive bar, line, and pie charts for query results.

🛡️ Robust Error Handling: User-friendly feedback for errors and edge cases.

🛠️ Getting Started
1. Clone the Repository
bash
git clone https://github.com/yourusername/audio-to-sql-db-manager.git
cd audio-to-sql-db-manager
2. Install Dependencies
bash
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the project root with the following (edit as needed):

text
# Database type: sqlite, mysql, or postgresql
DB_TYPE=sqlite

# For SQLite
SQLITE_PATH=./data/dataset.db

# For MySQL/PostgreSQL
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306          # 5432 for PostgreSQL
DB_NAME=yourdatabase

# (Optional) API keys for LLMs or ASR models if required
API_KEY=your_api_key
4. Run the Application
bash
streamlit run app.py
🖥️ Usage
Open the Streamlit app in your browser (usually at localhost:8501).

Record or upload an audio query (e.g., “Show the number of products in each category”).

The app will:

Transcribe your speech

Generate and display the SQL query

Execute the query and visualize the results

📁 Project Structure
text
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
🔧 Customization
Add new database support: Extend the schema fetcher and connection logic.

Swap transcription model: Replace or upgrade the ASR model in models/wav2vec.py.

Enhance visualization: Add more chart types or dashboard features.

📜 License
This project is licensed under the MIT License.

🙏 Acknowledgments
Streamlit

PyTorch

OpenAI / Hugging Face Transformers

pymysql

psycopg2

Query your database with your voice-intuitively and efficiently!