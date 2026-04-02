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

The user draws a mathematical expression on a canvas in the frontend. The image is sent to this backend, which passes it through a deep learning model trained on the [MathWriting dataset](https://huggingface.co/datasets/deepcopy/MathWriting-human). The model recognizes the expression and returns a LaTeX string. SymPy then evaluates the result where applicable — solving equations, evaluating integrals, derivatives, summations, and products, and simplifying plain expressions.

## Related Repositories

| Repo | Description |
|------|-------------|
| [Frontend](https://github.com/ApekshyaKoirala/MathematicalExpressionRecognizerFrontend) | Next.js canvas interface |
|[Training Repo](https://github.com/binit-awasthi/hmer?tab=readme-ov-file#-live-demo) | DL model training script|
| [Model](https://www.kaggle.com/models/binitawasthi/hmer) | DL model on kaggle |

## Architecture

```
Frontend (Next.js)
    │
    │  PNG/JPEG via multipart/form-data
    ▼
FastAPI Backend  ◄── this repo
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

## Project Structure

```
MathExpressionAPI/
├── main.py                  # root entry point — run from here
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

### Installation

```bash
git clone https://github.com/ArunAryal/MathematicalExpressionAPI
cd MathematicalExpressionAPI
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
MODEL_PATH=backend/models/hmer.pt
API_V1_STR=/api/v1
FRONTEND_ORIGIN=http://localhost:3000
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

### Model

The API automatically downloads the trained PyTorch model on startup if it is not found at the `MODEL_PATH` location. This requires your Kaggle API credentials to be set in the `.env` file because the model will be fetched from the [model training repo](https://www.kaggle.com/models/binitawasthi/hmer).

1. Log in to your [Kaggle](https://www.kaggle.com/) account.
2. Go to your Account Settings and hit **"Create New Token"** to download `kaggle.json`.
3. Open `kaggle.json` to find your `username` and `key`, and paste them into your `.env` file.

Alternatively, you can manually place the model at the path specified by `MODEL_PATH` (default: `backend/models/hmer.pt`), and the API will skip the download step.

### Running

```bash
uv run main.py
```

API docs available at `http://localhost:8000/docs`

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

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.