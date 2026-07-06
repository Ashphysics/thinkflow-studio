# Final Submission Checklist

## 1. Codebase & Repository
- [ ] `GOOGLE_API_KEY` is not hardcoded anywhere (Check `app/config/providers.py` and `app/ui/app.py`).
- [ ] `.env` is listed in `.gitignore`.
- [ ] Repository is public.
- [ ] Topics and Description are set on GitHub.
- [ ] Release v1.0.0 is published.

## 2. Documentation
- [ ] `README.md` has the YouTube link and screenshots injected.
- [ ] `docs/architecture/*.md` Mermaid diagrams render correctly on GitHub.
- [ ] `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` are present.

## 3. Deployment
- [ ] `docker-compose up` builds and runs cleanly on a fresh machine.
- [ ] The Streamlit UI loads on `http://localhost:8501`.
- [ ] Submitting a prompt successfully triggers the MCP subprocess.
- [ ] SQLite database `thinkflow_memory.db` is correctly generated and persists across container restarts (using volumes).

## 4. Kaggle Submission
- [ ] Kaggle notebook/dataset is created.
- [ ] `kaggle_writeup.md` is pasted into the Kaggle description.
- [ ] YouTube video is uploaded and linked.
- [ ] Cover image is uploaded to Kaggle.
- [ ] Open Source license (MIT) is selected in Kaggle settings.
