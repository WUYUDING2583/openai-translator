# Prerequisites

- python 3.12
- Anaconda

# Install Dependencies

```bash
conda env create -f environment.yaml
```

# Start Dev

```bash
export OPENAI_API_KEY="your-openai-api-key"
python app.py
```

After running server, it will be hosted on `http://127.0.0.1:5000`

# Call translate API

```bash
curl -X POST "http://127.0.0.1:5000/translate" -F "file=@/your/file/path" -F "openaiModel=gpt-3.5-turbo" -F "targetLanguage=中文"
```
