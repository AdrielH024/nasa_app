## NASA Articles Summary API (Minimal)

- Simple FastAPI service exposing `GET /articles?tag=...`.
- Plug in your existing summarization service inside `app/services/summarizer.py`.

### Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open: `http://localhost:8000/articles?tag=exemplo`

### Integration

- Replace the mock in `app/services/summarizer.py#get_article_summaries` with your real service call.
- Keep the return structure: a list of objects with `title`, `link`, `summary_for_dummies`.
