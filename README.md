# TestPilot AI

AI-powered Playwright testing platform with failure diagnosis.

Repository: https://github.com/0xyz-exe/testpilot-ai

## Screenshots

### 1. Test Execution & Run Overview
Tampilan ringkasan eksekusi pengujian menyajikan metrik pemantauan pipeline pengujian Playwright secara real-time lintas lingkungan (Staging, Production, Internal), matriks pengujian lintas mesin peramban (Chromium 130, Firefox 131, WebKit 18), kartu status proyek aktif dengan indikator pass rate dan fail rate terperinci, serta tabel riwayat run terbaru lengkap dengan badge status berkode warna (PASSED, FAILED, FLAKY), durasi eksekusi milidetik, tautan artefak (tangkapan layar PNG dan arsip trace ZIP), dan tombol aksi diagnosis instan.

![Test Execution & Run Overview](docs/screenshots/01_test_runs.png)

### 2. AI Root-Cause Failure Diagnosis
Antarmuka investigasi akar masalah kegagalan pengujian bertenaga AI mengkorelasikan berbagai lapisan bukti pengujian—termasuk timeout selektor Playwright, inspeksi mutasi pohon DOM, log konsol peramban, dan jejak lalu lintas jaringan HAR—untuk mengidentifikasi penyebab kegagalan dengan tingkat keyakinan terukur (98.4%), menyajikan rekomendasi patch kode Playwright otomatis dalam format visual git diff yang membandingkan kode lama versus kode perbaikan, serta menyediakan tombol aksi instan untuk menerapkan perbaikan dan memverifikasi ulang pengujian.

![AI Root-Cause Failure Diagnosis](docs/screenshots/02_ai_diagnosis.png)

### 3. Playwright Test Suite Management
Workspace manajemen suite pengujian menyediakan direktori hierarki suite dan kasus uji yang terstruktur di panel kiri, dilengkapi dengan generator uji bahasa alami berbasis model GPT-4o untuk menyintesis skenario pengujian Playwright web-first secara otomatis dari deskripsi kebutuhan pengguna, serta editor kode interaktif berfitur penyorotan sintaks TypeScript lengkap dengan kontrol sandbox eksekusi mandiri, pemformatan kode, dan penyimpanan revisi suite.

![Playwright Test Suite Management](docs/screenshots/03_test_editor.png)

### 4. Test Metrics & Diagnostic Reports
Dashboard analitik kualitas dan intelijen pengujian menyajikan metrik agregat kesehatan pipeline (248 run dieksekusi, pass rate global 92.7%, rasio flakiness 4.1%, dan rata-rata durasi 2.84 detik), matriks pelacakan uji flaky dengan visualisasi rekam jejak status 10 run terakhir beserta pola akar penyebab race condition, panel komparasi eksekusi berdampingan (*side-by-side run diff*), serta opsi ekspor laporan kepatuhan formal dalam format Allure, JUnit XML, dan PDF.

![Test Metrics & Diagnostic Reports](docs/screenshots/04_test_reports.png)

## Quick Start

### Backend Setup

Run these commands from the repository root (`testpilot-ai`), not from inside
the `backend` directory:

```bash
python -m venv backend\venv
backend\venv\Scripts\activate
python -m pip install -r backend\requirements.txt
python -m backend.init_db
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8001
```

If your terminal is already in `backend`, first return to the repository root:

```powershell
Set-Location ..
```

If `venv` already exists or Python reports a package import error involving
`pydantic_core`, recreate the environment before installing dependencies:

```powershell
deactivate
Remove-Item -Recurse -Force .\backend\venv
python -m venv .\backend\venv
.\backend\venv\Scripts\Activate.ps1
python -m pip install -r .\backend\requirements.txt
```

Backend: http://localhost:8001

### Test

```bash
curl http://localhost:8001/health
```

## Status

**Phase:** Milestone B (Core Implementation)

**Complete:**
- ✅ Requirements & architecture docs
- ✅ Database models
- ✅ Auth (register/login, bcrypt)
- ✅ Project CRUD routes
- ✅ URL validation & SSRF prevention

**Next:**
- Test execution worker
- Frontend React app
- Artifact storage

## Docs

- [PRD](docs/PRD.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Threat Model](docs/THREAT_MODEL.md)

## Note

Python 3.14 has limited package support. Use Python 3.11 or 3.12 for production.
