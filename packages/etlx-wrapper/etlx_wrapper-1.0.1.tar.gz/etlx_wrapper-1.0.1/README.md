# ETLX Python Wrapper

**ETLX** is a modern and highly configurable ETL and reporting tool powered by DuckDB.  
This Python package provides a simple interface to run ETLX workflows directly from Python.

---

## 📦 Installation

Install the wrapper from PyPI:

```bash
pip install etlx-wrapper
```

### 🧩 Requirements

You also need the ETLX binary:

1. Download the latest binary for your platform from  
   [ETLX Releases](https://github.com/realdatadriven/etlx/releases)
2. Place it in your system `PATH`, or provide the binary path manually when using the wrapper.

---

## 🚀 Quick Start

```python
import datetime
from etlx import ETLX

_etlx = ETLX()
_etlx.config = "/path/to/config.md"
_etlx.only = "keyX"
_etlx.date = datetime.date.today()
_etlx.file = "data.csv"
_etlx.execute()
```

You can also pass the path to the ETLX binary if it's not in `PATH`:

```python
runner = ETLX(config="config.md", bin="/path/to/etlx-linux-amd64")
```

---

## 🔧 Features

- Runs full ETLX workflows from Python  
- Supports `.env` configuration  
- Automatically formats Python `date` objects  
- Compatible with advanced CLI options: `--only`, `--skip`, `--steps`, `--clean`, `--drop`, etc.

---

## 🧱 Learn More

Visit the [main project](https://github.com/realdatadriven/etlx) for full documentation, use cases, and advanced config examples.

---

## License

MIT
