# MissMecha

**MissMecha** is a Python package for the **systematic simulation, visualization, and evaluation** of missing data mechanisms.  
It provides a **unified and principled interface** to generate, inspect, and analyze missingness — supporting research, benchmarking, and education.

Documentation: [https://echoid.github.io/MissMecha/](https://echoid.github.io/MissMecha/)

---

## Highlights

- **All About Missing Mechanisms**
  - Simulate **MCAR**, **MAR**, and **MNAR** with flexible configuration
  - Currently includes:
    - `3×` MCAR strategies
    - `8×` MAR strategies
    - `6×` MNAR strategies
    - Experimental support for **categorical** and **time series** missingness

- **Missingness Pattern Visualization**
  - Visual tools to **observe missing patterns**
  - Helps diagnose potential mechanism types (e.g., MCAR vs. MAR)

- **Flexible Generator Interface**
  - Column-wise or global simulation
  - `fit` / `transform` scikit-learn style API
  - Supports custom rates, dependencies, and label-based logic

- **Evaluation Toolkit**
  - Metrics including **MSE**, **MAE**, **RMSE**, and our custom **AvgERR**
  - Built-in support for **Little’s MCAR test**

- **SimpleSmartImputer**
  - Lightweight imputer that detects **numerical** vs. **categorical** columns
  - Applies mean/mode imputation with transparent diagnostics

---

## Motivation

Working with missing data often involves **disjointed code and inconsistent assumptions**.

**MissMecha** solves this by consolidating diverse missingness simulation strategies — across MCAR, MAR, and MNAR — into one consistent, structured Python framework.

> Whether you're exploring datasets, designing simulations, or teaching statistics —  
> MissMecha helps you simulate and analyze missingness with clarity and control.

---

## ⚡ Quick Preview

```python
from missmecha import MissMechaGenerator
import numpy as np

X = np.random.rand(100, 5)

generator = MissMechaGenerator(
    mechanism="mar", mechanism_type=1, missing_rate=0.3
)
X_missing = generator.fit_transform(X)
```

Or configure per-column:

```python
generator = MissMechaGenerator(
    info={
        0: {"mechanism": "mcar", "type": 1, "rate": 0.3},
        1: {"mechanism": "mnar", "type": 2, "rate": 0.4}
    }
)
X_missing = generator.fit_transform(X)
```

---

## Documentation & Demos

- Full documentation: [https://echoid.github.io/MissMecha/](https://echoid.github.io/MissMecha/)


---

## Installation

```bash
pip install missmecha-py
```

> Available on [PyPI](https://pypi.org/project/missmecha-py/) under the name `missmecha-py`.

---

## Author

Developed by **Youran Zhou**, PhD Candidate @ Deakin University  

---

## License

MIT License
```

---