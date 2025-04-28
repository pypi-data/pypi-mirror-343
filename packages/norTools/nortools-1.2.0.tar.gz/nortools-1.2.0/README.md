# norTools

`norTools` is a Python package that provides utilities for handling operations with arguments, dictionaries, and displaying data on a graphical screen using Flet.

---

## Features

- **Dam Class**: Perform operations with arguments and extra values.
- **Dictor Class**: A dynamic dictionary-like structure with nested capabilities.
- **ScreenOpp Class**: Display data on a graphical screen using Flet.

---

## Installation

### Install Locally
To install the package locally, navigate to the project directory and run:
```bash
pip install .
```

### Install from PyPI (if published)
To install the package from PyPI:
```bash
pip install norTools
```

---

## Usage

### 1. Dam Class
Perform operations with arguments and extra values.

```python
from norTools import Dam

dam_instance = Dam()
result = dam_instance.opp("example", extra=42)
print(result)  # Output: 42
```

### 2. Dictor Class
A dynamic dictionary-like structure.

```python
from norTools import Dictor

dictor_instance = Dictor()
dictor_instance["key"] = "value"
print(dictor_instance["key"])  # Output: value
```

### 3. ScreenOpp Class
Display data on a graphical screen.

```python
from norTools import ScreenOpp

screen = ScreenOpp(name="Example Name", datas_="Example Data", page="Example Page")
screen.display()
```

---

## Dependencies

- **Flet**: Used for graphical screen rendering.
- **Python 3.6 or higher**

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Development

### Setting Up the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/norTools.git
   ```
2. Navigate to the project directory:
   ```bash
   cd norTools
   ```
3. Install the package locally:
   ```bash
   pip install .
   ```

### Running Tests
Add your test scripts and run them using:
```bash
python -m unittest discover
```

---

## Documentation

To generate documentation using Sphinx:
1. Navigate to the `docs` folder:
   ```bash
   cd docs
   ```
2. Build the documentation:
   ```bash
   sphinx-build -b html . _build/html
   ```
3. Open `_build/html/index.html` in your browser.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

**Syed**

Feel free to contribute to this project by submitting issues or pull requests!