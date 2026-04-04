# Handwritten Mathematical Expression Recognition (HMER System)

![Python](https://img.shields.io/badge/python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

A full-stack application for recognizing and solving handwritten mathematical expressions. Draw an expression on the canvas, and the app recognizes it, evaluates it, and renders the result — no typing required.

## Table of Contents

- [Overview](#overview)
- [Related Repositories](#related-repositories)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Contributors](#contributors)
- [License](#license)

## Overview

The user draws a mathematical expression on the canvas in the frontend. The image is sent to the FastAPI backend, which passes it through a deep learning model trained on the [MathWriting dataset](https://huggingface.co/datasets/deepcopy/MathWriting-human). The model is automatically downloaded from Kaggle on first startup — no manual setup required. The model recognizes the expression and returns a LaTeX string. SymPy then evaluates the result where applicable — solving equations, evaluating integrals, derivatives, summations, and products, and simplifying plain expressions.

## Related Repositories

| Repo | Description |
|------|-------------|
| [Training Repo](https://github.com/binit-awasthi/hmer?tab=readme-ov-file#-live-demo) | DL model training script |
| [Model](https://www.kaggle.com/models/binitawasthi/hmer) | DL model on Kaggle |

## Architecture

```
Frontend (Next.js)
    │
    │  PNG/JPEG via multipart/form-data
    ▼
FastAPI Backend
    │
    ├── image_utils.py      → validates and loads image as torch tensor
    ├── model_service.py    → runs inference (PyTorch CNN-Transformer)
    ├── model_downloader.py → auto-downloads model from Kaggle if not present
    ├── math_service.py     → evaluates equations, integrals, derivatives,
    │                         summations, products, and plain expressions
    │
    └── returns LaTeX string + evaluated result (if applicable)
```

## Tech Stack

- **FastAPI** — API framework
- **PyTorch** — model loading and inference
- **SymPy** — equation solving and expression evaluation
- **Pillow** — image loading and preprocessing
- **Pydantic v2** — request/response validation
- **kagglehub** — automatic model downloading
- **uv** — package management
- **Next.js** — frontend canvas interface

## Project Structure

```
MathExpressionAPI/
├── main.py                  # root entry point — run from here
├── frontend/                # Next.js canvas interface
│   ├── src/
│   │   ├── app/             # Next.js app router pages
│   │   ├── components/      # CanvasArea, CanvasControl, Instructions
│   │   ├── services/        # predictionService.ts — API calls
│   │   ├── styles/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   └── next.config.ts
└── backend/
    ├── app/
    │   ├── api/v1/endpoints/
    │   │   └── predict.py       # POST /api/v1/predict/
    │   ├── core/
    │   │   ├── config.py        # settings via pydantic-settings
    │   │   └── vocab.py         # model vocabulary and tokenization
    │   ├── schemas/
    │   │   └── predict.py       # PredictResponse schema
    │   ├── services/
    │   │   ├── model_service.py # PyTorch model loading and inference
    │   │   └── math_service.py  # SymPy expression evaluation
    │   ├── utils/
    │   │   ├── image_utils.py       # image validation and tensor conversion
    │   │   └── model_downloader.py  # Kaggle model auto-downloader
    │   └── main.py              # FastAPI app, lifespan, router registration
    ├── models/                  # hmer.pt lives here (not tracked by git)
    └── tests/
        └── api/v1/
            ├── test_predict.py
            ├── test_image_utils.py
            └── test_model_service.py
```

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- Node.js 18+
- npm

### Installation

```bash
git clone https://github.com/ArunAryal/MathematicalExpressionAPI
cd MathematicalExpressionAPI
```

**Backend:**

```bash
uv sync
```

**Frontend:**

```bash
cd frontend
npm install
```

### Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
APP_NAME=MathExpressionAPI
DEBUG=True
MODEL_PATH=backend/models/hmer.pt
API_V1_STR=/api/v1
FRONTEND_ORIGIN=http://localhost:3000
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

### Model

The model is automatically downloaded from Kaggle on first startup. No manual download required. You only need your Kaggle API credentials in the `.env` file.

1. Log in to your [Kaggle](https://www.kaggle.com/) account.
2. Go to your Account Settings and hit **"Create New Token"** to download `kaggle.json`.
3. Open `kaggle.json` to find your `username` and `key`, and paste them into your `.env` file.

Alternatively, you can manually place the model at the path specified by `MODEL_PATH` (default: `backend/models/hmer.pt`), and the API will skip the download step.

### Running

Start both the backend and frontend in separate terminals.

**Backend** (from repo root):

```bash
uv run main.py
```

API docs available at `http://localhost:8000/docs`

**Frontend** (from `frontend/`):

```bash
cd frontend
npm run dev
```

App available at `http://localhost:3000`

## API Reference

### `POST /api/v1/predict/`

Accepts a PNG or JPEG image via multipart form data.

**Request:**

| Field | Type | Description |
|-------|------|-------------|
| `file` | PNG or JPEG image | Canvas image of handwritten math expression |

**Response:**

```json
{
  "latex": "x + 2 = 5",
  "is_equation": true,
  "result": "3"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `latex` | string | Recognized LaTeX string |
| `is_equation` | boolean | Whether the expression is an equation |
| `result` | string or null | Evaluated result if applicable, null otherwise |

**Error Responses:**

| Status | Description |
|--------|-------------|
| `400` | Invalid image file or unsupported content type |
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
| `test_predict_expression` | Plain expression is simplified and result is returned |
| `test_predict_equation` | Equation is solved and result is returned |
| `test_predict_invalid_file` | Invalid image bytes are rejected with 400 |
| `test_predict_wrong_content_type` | Unsupported content type is rejected with 400 |
| `test_predict_jpeg_accepted` | JPEG images are accepted |
| `test_process_image_output_shape` | Preprocessed tensor shape is correct |
| `test_process_image_values_normalized` | Pixel values are normalized between 0 and 1 |
| `test_process_image_returns_tensor` | Output is a torch tensor |
| `test_model_load_bad_path` | Bad model path raises an error |
| `test_predict_returns_string` | Model predict returns a string |
| `test_predict_raises_if_model_not_loaded` | Predict raises if model not loaded |

## Contributors

| Name | Role |
|------|------|
| [Arun Aryal](https://github.com/ArunAryal) | Backend |
| [Apekshya Koirala](https://github.com/ApekshyaKoirala) | Frontend |
| [Binit Awasthi](https://github.com/binit-awasthi) | Model Training |

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.