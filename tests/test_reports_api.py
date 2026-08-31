"""
Testes de integração e unitários para as rotas de exportação de relatórios (PDF/Excel).
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.reports import generate_pdf_report, generate_excel_report, filter_data, compute_summary_by_block

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer mock-token"}


def test_generate_pdf_report_unit(sample_report_data):
    rooms, allocations = sample_report_data
    pdf_bytes = generate_pdf_report(rooms, allocations)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # Valida assinatura do cabeçalho PDF
    assert pdf_bytes.startswith(b"%PDF")


def test_generate_excel_report_unit(sample_report_data):
    rooms, allocations = sample_report_data
    excel_bytes = generate_excel_report(rooms, allocations)
    assert isinstance(excel_bytes, bytes)
    assert len(excel_bytes) > 0


def test_filter_data_helper(sample_report_data):
    rooms, allocations = sample_report_data
    # Filtrar por bloco BLOCO_A
    f_rooms, f_allocs = filter_data(rooms, allocations, block_id="BLOCO_A")
    assert len(f_rooms) == 2
    assert all(r["block_id"] == "BLOCO_A" for r in f_rooms)

    # Filtrar por turno M
    f_rooms_m, f_allocs_m = filter_data(rooms, allocations, shift="M")
    assert len(f_allocs_m) == 1
    assert f_allocs_m[0]["time_slot"] == "M1"


def test_compute_summary_by_block(sample_report_data):
    rooms, allocations = sample_report_data
    summary = compute_summary_by_block(rooms, allocations)
    assert len(summary) == 2  # BLOCO_A e BLOCO_B
    bloco_a = next(s for s in summary if s["block_id"] == "BLOCO_A")
    assert bloco_a["total_rooms"] == 2
    assert bloco_a["total_capacity"] == 65
    assert bloco_a["occupied_slots"] == 2


def test_export_pdf_unauthorized():
    res = client.get("/api/v1/reports/occupancy/pdf")
    assert res.status_code == 401


def test_export_excel_unauthorized():
    res = client.get("/api/v1/reports/occupancy/excel")
    assert res.status_code == 401


def test_export_pdf_success():
    res = client.get("/api/v1/reports/occupancy/pdf", headers=AUTH_HEADERS)
    assert res.status_code == 200
    assert "application/pdf" in res.headers.get("content-type", "")
    assert res.content.startswith(b"%PDF")


def test_export_excel_success():
    res = client.get("/api/v1/reports/occupancy/excel", headers=AUTH_HEADERS)
    assert res.status_code == 200
    content_type = res.headers.get("content-type", "")
    assert "spreadsheet" in content_type or "octet-stream" in content_type or "csv" in content_type


def test_export_pdf_filtered():
    res = client.get("/api/v1/reports/occupancy/pdf?block_id=BLOCO_A&shift=M", headers=AUTH_HEADERS)
    assert res.status_code == 200
    assert res.content.startswith(b"%PDF")


def test_generate_pdf_with_teacher_allocations():
    rooms = [{"id": "r1", "block_id": "BLOCO_A", "name": "Sala 101", "capacity": 30, "room_type": "common", "is_accessible": True}]
    allocations = [{"id": "a1", "room_id": "r1", "time_slot": "M1"}]
    teacher_allocs = [
        {"teacher_name": "Bruno Souza", "subject": "Filosofia", "room_name": "Sala 101 (BLOCO_A)", "shift": "M", "sub_slot": 1},
        {"teacher_name": "Ana Clara", "subject": "Física I", "room_name": "Sala 102 (BLOCO_A)", "shift": "T", "sub_slot": 2}
    ]
    pdf_bytes = generate_pdf_report(rooms, allocations, teacher_allocations=teacher_allocs)
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")


def test_generate_excel_with_teacher_allocations():
    rooms = [{"id": "r1", "block_id": "BLOCO_A", "name": "Sala 101", "capacity": 30, "room_type": "common", "is_accessible": True}]
    allocations = [{"id": "a1", "room_id": "r1", "time_slot": "M1"}]
    teacher_allocs = [
        {"teacher_name": "Bruno Souza", "subject": "Filosofia", "room_name": "Sala 101 (BLOCO_A)", "shift": "M", "sub_slot": 1},
        {"teacher_name": "Ana Clara", "subject": "Física I", "room_name": "Sala 102 (BLOCO_A)", "shift": "T", "sub_slot": 2}
    ]
    excel_bytes = generate_excel_report(rooms, allocations, teacher_allocations=teacher_allocs)
    assert isinstance(excel_bytes, bytes)
    assert len(excel_bytes) > 0


def test_get_reports_summary_endpoint():
    response = client.get("/api/v1/reports/summary", headers={"Authorization": "Bearer mock-token"})
    assert response.status_code == 200
    data = response.json()
    assert "room_occupancy" in data
    assert "teacher_reports" in data


def test_export_teacher_pdf_endpoint():
    response = client.get("/api/v1/reports/teacher/prof-givaldo/pdf", headers={"Authorization": "Bearer mock-token"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0

