# Quantum Finance Platform

> Hybrid quantum-classical machine learning framework for financial modeling,
> risk simulation, and trading strategies.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

Follow these steps to set up a local development environment:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-root>
   ```
2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   - Copy `consolidated.env.template` to `.env` and populate required values
   - Set `PORT` (default 5002) and any quantum API credentials (e.g.,
     `IBM_QUANTUM_TOKEN`)

## Prerequisites

- Python 3.8 or higher
- `pip` package manager
- Access to real quantum API credentials (e.g., IBM Quantum Experience token)

## Installation

All required Python packages are listed in `requirements.txt`. Run:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Flask API

1. **Set the PORT** (optional, defaults to 5002):
   ```bash
   export PORT=5002
   ```
2. **Start the backend service**:
   ```bash
   python src/quantum_finance/backend/app.py
   ```

### API Endpoints

- **POST /predict**\
  Input: JSON with `data` array\
  Output: JSON with `prediction` array

- **POST /feedback**\
  Input: JSON with `prediction` and `isPositive`\
  Output: `{ status: 'success' }` on valid feedback

- **GET /admin/insights**\
  Input: No body (localhost only)\
  Output: Health metrics and API improvement recommendations

## Directory Structure

```
.
├── backend/                       # Low-level simulation interface & logs
├── src/                           # Core source code
│   ├── quantum_finance/          # ML & quantum modules
│   │   └── backend/               # Flask API & ML framework
│   └── quantum_finance.egg-info/ # Packaging metadata
├── tests/                         # Unit, integration, and e2e tests
├── error_mitigation_results/      # Historical experiment outputs
├── logs/                          # Runtime logs and artifacts
└── README.md                      # Project overview and instructions
```

## Testing

Run all tests with `pytest`:

```bash
pytest --maxfail=1 --disable-warnings -q --cov=./ --cov-report=html --cov-fail-under=100
```

Coverage report HTML will be generated in the `htmlcov/` directory after tests.

Ensure you have copied `consolidated.env.template` to `.env` and populated
required environment variables before running tests.

## Contributing

Contributions are welcome! Please open issues or submit pull requests. Refer to
`CONTRIBUTING.md`
