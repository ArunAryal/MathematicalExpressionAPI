# MathExpressionAPI

![Python](https://img.shields.io/badge/python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

A FastAPI backend for recognizing and solving handwritten mathematical expressions drawn on an HTML5 canvas.

## Table of Contents

- [Overview](#overview)
- [Related Repositories](#related-repositories)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Testing](#testing)
- [License](#license)

## Overview

The user draws a mathematical expression on a canvas in the frontend. The image is sent to this backend, which passes it through a deep learning model trained on the [CROHME dataset](https://tc11.cvc.uab.es/datasets/ICDAR2019-CROHME-TDR_1). The model recognizes the expression and returns a LaTeX string. If the expression is an equation, SymPy solves it automatically.

## Related Repositories

| Repo | Description |
|------|-------------|
| [Frontend](https://github.com/) | Next.js canvas interface [Under development]|
| [Model Training](https://github.com/) | DL model training on CROHME dataset [Under development]|

## Architecture

```
Frontend (Next.js)
    │
    │  PNG via multipart/form-data
    ▼
FastAPI Backend  ◄── this repo
    │
    ├── image_utils.py    → validates and loads image as numpy array
    ├── model_service.py  → runs inference (Keras model)
    ├── math_service.py   → detects equation vs expression, solves with SymPy
    │
    └── returns LaTeX string + solution (if equation)
```

## Tech Stack

- **FastAPI** — API framework
- **TensorFlow / Keras** — model loading and inference
- **SymPy** — equation solving
- **Pillow** — image loading and grayscale conversion
- **Pydantic v2** — request/response validation
- **uv** — package management

## Project Structure

```
backend/
├── app/
│   ├── api/v1/endpoints/
│   │   └── predict.py       # POST /api/v1/predict/
│   ├── core/
│   │   └── config.py        # settings via pydantic-settings
│   ├── schemas/
│   │   └── predict.py       # PredictResponse schema
│   ├── services/
│   │   ├── model_service.py # Keras model loading and inference
│   │   └── math_service.py  # SymPy equation detection and solving
│   ├── utils/
│   │   └── image_utils.py   # image validation and numpy conversion
│   └── main.py              # app entry point, lifespan, router registration
├── models/                  # place model.keras here (not tracked by git)
└── tests/
    └── api/v1/
        └── test_predict.py
```

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

### Installation

```bash
git clone https://github.com/ArunAryal/MathematicalExpressionAPI
cd MathematicalExpressionAPI/backend
uv sync
```

### Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
APP_NAME=MathExpressionAPI
DEBUG=True
MODEL_PATH=models/model.keras
API_V1_STR=/api/v1
FRONTEND_ORIGIN=http://localhost:3000
```

### Model

Place the trained Keras model at the path specified by `MODEL_PATH` (default: `models/model.keras`). The model file is not tracked by git — obtain it from the [model training repo](https://github.com/).

### Running

```bash
cd backend
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

## API Reference

### `POST /api/v1/predict/`

Accepts a PNG image via multipart form data.

**Request:**

| Field | Type | Description |
|-------|------|-------------|
| `file` | PNG image | Canvas image of handwritten math expression |

**Response:**

```json
{
  "latex": "x + 2 = 5",
  "is_equation": true,
  "result": "[3]"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `latex` | string | Recognized LaTeX string |
| `is_equation` | boolean | Whether the expression is an equation |
| `result` | string or null | Solution if equation, null if plain expression |

**Error Responses:**

| Status | Description |
|--------|-------------|
| `400` | Invalid image file or wrong content type |
| `500` | Internal server error |

### `GET /health`

Returns `{"status": "ok"}` if the server is running.

## Testing

Tests mock the model so no model file is required to run them.

```bash
cd backend
pytest tests/ -v
```

### Test Coverage

| Test | Description |
|------|-------------|
| `test_health` | Server boots and responds correctly |
| `test_predict_expression` | Plain expression returns correct response with no solution |
| `test_predict_equation` | Equation is solved and result is returned |
| `test_predict_invalid_file` | Invalid image bytes are rejected with 400 |
| `test_predict_wrong_content_type` | Non-PNG content type is rejected with 400 |

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
