from typing import Any, Dict, List
import os

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Unified NASA Backend API", version="0.3.0")


# =========================
# Data-fetch stub (can be replaced by your own DB logic)
# =========================
async def fetch_data(tag: str | None = None) -> List[Dict[str, Any]]:
    example = [
        {
            "id": 1,
            "title": "Example NASA record",
            "tag": tag or "exemplo",
            "value": 42,
        }
    ]
    return example


# =========================
# /articles: summarize NASA CSV using Gemini
# =========================
@app.get("/articles")
async def list_articles(tag: str = Query(..., description="Tema/Subtema para filtrar artigos no CSV e resumir")):
    if not tag or not tag.strip():
        raise HTTPException(status_code=400, detail="tag is required")

    # Load dependencies lazily to keep startup fast if not used
    try:
        import pandas as pd  # type: ignore
        import google.generativeai as genai  # type: ignore
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to import deps: {exc}") from exc

    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        # Allow fallback to hardcoded key only if provided via code (not recommended). For safety, require env var.
        raise HTTPException(status_code=500, detail="Missing GENAI_API_KEY environment variable")

    try:
        genai.configure(api_key=api_key)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to configure GenAI: {exc}") from exc

    # Load CSV (limit rows for performance)
    try:
        df = pd.read_csv("Publicacoes_Classificadas.csv", nrows=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV 'Publicacoes_Classificadas.csv' not found in project root")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read CSV: {exc}") from exc

    pesquisa = tag.strip()

    # Build prompt
    try:
        subset = df[["Title", "Link", "Abstract", "Tema", "Subtema"]]
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"CSV missing required columns: {exc}") from exc

    # Keep a small window for prompt size
    table_text = subset.head(20).to_string(index=False).strip()
    prompt = (
        "Imagine you are a researcher and you need teatch cientific concepts in cientific articles for dummies, "
        "to find articles about a specific subject you should use NASA Articles in the csv bellow. "
        "They cannot be articles of another source, ONLY in the CSV bellow. you must search articles in Theme and Subtheme column "
        + pesquisa
        + " theme and summarize the articles that have the searched theme and also Title and link of the articles bellow.\n\n"
        + table_text
    )

    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        text = getattr(response, "text", None)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"GenAI request failed: {exc}") from exc

    if not text:
        raise HTTPException(status_code=502, detail="Empty response from GenAI")

    return JSONResponse({
        "tag": pesquisa,
        "summary": text,
    })


@app.get("/dados")
async def dados(tag: str | None = Query(None, description="Optional tag to filter data fetch")):
    try:
        data = await fetch_data(tag)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"data fetch failed: {exc}") from exc

    return JSONResponse({
        "tag": tag,
        "results": data,
    })
