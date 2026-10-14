# Khurram's AI

A Streamlit website prototype for a Pakistani school tutor (Classes 1–10), with extra focus on Classes 9 and 10.

## Files
- `app.py` — website and chat logic
- `requirements.txt` — Python dependencies

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Connect a Hugging Face model
1. Create a Hugging Face access token with the permissions required for Inference Providers.
2. In Streamlit Community Cloud, open your app's **Settings → Secrets** and add:

```toml
HF_TOKEN = "your_hugging_face_token"
HF_MODEL = "Qwen/Qwen2.5-7B-Instruct"
```

The selected model must be available through your Hugging Face Inference Providers account. Availability, provider access, and free quotas can change. Never commit your token to GitHub or put it directly in `app.py`.

## Deploy
1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and optionally this README.
3. Go to https://share.streamlit.io/ and deploy the repository, choosing `app.py`.
4. Add `HF_TOKEN` and `HF_MODEL` under app Secrets.

## Important
This is a starter app, not a verified all-board curriculum database. For accurate answers aligned with a specific current textbook, add permitted textbook content and a retrieval system. AI responses can be wrong; students should check exam-critical answers against their current textbooks and teachers.
