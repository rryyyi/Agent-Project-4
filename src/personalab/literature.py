"""Conservative keyword extraction with verifiable source anchors, not semantic claims."""

import hashlib
import re
from pathlib import Path

MAX_BYTES = 2_000_000
MAX_CHARS = 2_000_000


def read_document(path: Path) -> str:
    if path.suffix.lower() not in {".txt", ".md", ".pdf"}:
        raise ValueError("supported document types: .txt, .md, .pdf")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("document too large (2 MB limit)")
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(path)
        if len(reader.pages) > 100:
            raise ValueError("document too large (100 page limit)")
        parts = []
        total = 0
        for number, page in enumerate(reader.pages, 1):
            text = f"[page {number}]\n" + (page.extract_text() or "")
            total += len(text)
            if total > MAX_CHARS:
                raise ValueError("extracted document too large")
            parts.append(text)
        return "\n".join(parts)
    return path.read_text(encoding="utf-8-sig")


def validate_evidence(text: str, start: int, end: int, quote: str) -> bool:
    return 0 <= start < end <= len(text) and text[start:end] == quote


def extract_evidence(text: str, source: str, keywords: list[str]) -> list[dict]:
    if len(text) > MAX_CHARS:
        raise ValueError("document too large")
    words = [word.strip().casefold() for word in keywords if word.strip()]
    if not words:
        raise ValueError("at least one nonempty keyword is required")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    rows = []
    for match in re.finditer(r"[^。！？.!?\n]+[。！？.!?]?", text):
        quote = match.group().strip()
        if not quote or quote.startswith("[page ") or not any(word in quote.casefold() for word in words):
            continue
        start = match.start() + len(match.group()) - len(match.group().lstrip())
        end = start + len(quote)
        anchors = list(re.finditer(r"\[page (\d+)\]", text[:start]))
        rows.append(
            {
                "source": source,
                "document_sha256": digest,
                "start": start,
                "end": end,
                "quote": quote,
                "page": int(anchors[-1].group(1)) if anchors else None,
                "matched_keywords": [word for word in words if word in quote.casefold()],
                "method": "deterministic_keyword_sentence_extraction",
                "review_status": "candidate_requires_human_review",
            }
        )
        if len(rows) >= 100:
            break
    return rows
