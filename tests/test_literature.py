from pathlib import Path

import pytest

from personalab.literature import extract_evidence, read_document, validate_evidence


def test_unicode_quotes_preserve_exact_source_offsets_and_hash():
    text = '背景介绍。合作偏好影响行为。\nRisk tolerance matters in choices.'
    rows = extract_evidence(text, 'teaching.txt', ['合作', 'risk'])
    assert len(rows) == 2
    assert rows[0]['quote'] == '合作偏好影响行为。'
    assert rows[0]['start'] == 5
    assert text[rows[0]['start']:rows[0]['end']] == rows[0]['quote']
    assert len(rows[0]['document_sha256']) == 64
    assert rows[0]['review_status'] == 'candidate_requires_human_review'
    assert validate_evidence(text, rows[0]['start'], rows[0]['end'], rows[0]['quote'])
    assert not validate_evidence(text, 5, 6, 'invented citation')
    assert not validate_evidence(text, -2, 6, text[-2:6])


def test_read_text_and_reject_unsupported_or_oversized_documents(tmp_path):
    text = tmp_path / 'source.txt'
    text.write_text('合作 evidence', encoding='utf-8')
    assert read_document(text) == '合作 evidence'
    bad = tmp_path / 'source.exe'
    bad.write_bytes(b'abc')
    with pytest.raises(ValueError, match='supported'):
        read_document(bad)
    text.write_bytes(b'x' * (2_000_001))
    with pytest.raises(ValueError, match='large'):
        read_document(text)


def test_pdf_loading_has_page_anchors(tmp_path):
    # Minimal PDF with selectable text, independent of a PDF creation dependency.
    contents = b'BT /F1 12 Tf 72 720 Td (Cooperation helps.) Tj ET'
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>', b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>', b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>', b'<< /Length ' + str(len(contents)).encode() + b' >>\nstream\n' + contents + b'\nendstream']
    data = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f'{i} 0 obj\n'.encode() + obj + b'\nendobj\n')
    xref = len(data)
    data.extend(b'xref\n0 6\n0000000000 65535 f \n')
    for offset in offsets[1:]:
        data.extend(f'{offset:010d} 00000 n \n'.encode())
    data.extend(f'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF'.encode())
    path = tmp_path / 'source.pdf'
    path.write_bytes(data)
    text = read_document(Path(path))
    assert '[page 1]' in text
    rows = extract_evidence(text, 'source.pdf', ['cooperation'])
    assert rows[0]['page'] == 1
    assert 'Cooperation helps.' in rows[0]['quote']


def test_no_keyword_match_produces_no_evidence():
    assert extract_evidence('nothing relevant.', 'source', ['合作']) == []
