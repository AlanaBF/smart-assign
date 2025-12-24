# Smart-Assign Documentation

This directory contains the Sphinx documentation for the Smart-Assign project.

## Prerequisites

- Python 3.7+
- Virtual environment (recommended)

## Setup Instructions

### 1. Virtual Environment Setup

**Windows:**
```powershell
cd ..\backend
python -m venv .venv
.venv\Scripts\activate.ps1
```

**macOS/Linux:**
```bash
cd ../backend
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

Install all required packages including Sphinx:

```powershell
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `sphinx` - Core documentation generator
- `sphinx-autodoc-typehints` - Type hints support
- `furo` - Modern theme with dark/light mode (currently used)
- `sphinx_book_theme` - Book-like appearance theme  
- `pydata_sphinx_theme` - Data science focused theme
- All other project dependencies

## Building Documentation

### Windows PowerShell Commands

Always make sure your virtual environment is activated first:

```powershell
# Navigate to docs directory
cd ..\docs

# Build HTML documentation
.\make.bat html

# Clean build files (removes _build directory)
.\make.bat clean

# View all available build formats
.\make.bat help
```

### macOS/Linux Terminal Commands

For macOS or Linux systems:

```bash
# Navigate to backend directory and set up virtual environment
cd ../backend
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to docs directory
cd ../docs

# Build HTML documentation
make html

# Clean build files
make clean

# View all available build formats
make help
```

### Alternative Direct Command

```powershell
sphinx-build -b html . _build/html
```

## Viewing Documentation

After building, your documentation will be available at:

**Windows:**
```
docs\_build\html\index.html
```

**macOS/Linux:**
```
docs/_build/html/index.html
```

**To view:**

**Windows:**
1. Navigate to `docs\_build\html\` in Windows Explorer
2. Double-click `index.html` to open in your default browser
3. Or copy the full path and paste into browser address bar

**macOS:**
1. Navigate to `docs/_build/html/` in Finder
2. Double-click `index.html` to open in your default browser
3. Or use terminal: `open docs/_build/html/index.html`

**Linux:**
1. Navigate to `docs/_build/html/` in your file manager
2. Double-click `index.html` to open in your default browser
3. Or use terminal: `xdg-open docs/_build/html/index.html`

## Documentation Structure

```
docs/
├── README.md              # This file
├── conf.py               # Sphinx configuration
├── index.rst             # Main documentation page
├── Makefile             # Unix make commands
├── make.bat             # Windows batch commands
├── backend/
│   └── index.rst        # Backend API documentation
├── _build/              # Generated documentation (created after build)
│   └── html/
│       └── index.html   # Main HTML documentation
├── _static/             # Static files (CSS, JS, images)
└── _templates/          # Custom templates (if needed)
```

## Configuration

The main configuration is in `conf.py`:

- **Project Info**: Name, author, version
- **Extensions**: Auto-documentation, type hints, etc.
- **Theme**: Currently using `sphinx_book_theme` theme
- **Autodoc Settings**: Automatic documentation from Python docstrings

## Adding Documentation

### 1. Add Docstrings to Python Files

Add docstrings to your Python functions and classes:

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description of the function.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    pass
```

### 2. Update Documentation Files

- Edit `index.rst` to add new sections
- Create new `.rst` files for additional pages
- Update `backend/index.rst` to include new modules

### 3. Rebuild Documentation

**Windows:**
```powershell
.\make.bat html
```

**macOS/Linux:**
```bash
make html
```

## Supported Formats

Sphinx can generate documentation in multiple formats:

- **HTML** (`.\make.bat html`) - Web-friendly format
- **PDF** (`.\make.bat latexpdf`) - Requires LaTeX installation
- **EPUB** (`.\make.bat epub`) - E-book format
- **Text** (`.\make.bat text`) - Plain text format

## Troubleshooting

### Common Issues

1. **"make is not recognized" (Windows)**
   - Use `.\make.bat` instead of `make` on Windows

2. **"python3: command not found" (macOS/Linux)**
   - Try `python` instead of `python3`
   - Install Python 3: `brew install python3` (macOS) or use your package manager

3. **Permission denied on virtual environment activation (macOS/Linux)**
   - Make sure the activate script is executable: `chmod +x .venv/bin/activate`

4. **Theme errors**
   - Check `conf.py` for theme compatibility
   - Default `alabaster` theme works with all Sphinx versions

5. **Module import errors**
   - Ensure your virtual environment is activated
   - Check that the backend directory is in the Python path (configured in `conf.py`)

6. **Missing static directory warning**
   - Create `_static` directory if it doesn't exist

### Build Warnings

Some warnings are normal and don't affect functionality:
- `sphinx-autodoc-typehints` deprecation warnings
- `paramref` role warnings from external packages

## Customization

### Changing Theme

The documentation currently uses the **Sphinx Book Theme** (book-like appearance, great for tutorials). You can easily switch to other themes:

#### **Simple Method: Edit conf.py**

1. Open `conf.py` 
2. Find line ~25: `html_theme = 'sphinx_book_theme'`
3. Replace `'sphinx_book_theme'` with any theme name from the list below
4. Save and rebuild:
   - **Windows**: `.\make.bat html`
   - **macOS/Linux**: `make html`

**Example:**
```python
html_theme = 'furo'  # Just change the theme name!
```

#### **Available Themes:**

1. **`furo`** - Modern, clean with dark/light mode toggle
2. **`sphinx_book_theme`** ⭐ *(Current)* - Book-like appearance, great for tutorials
3. **`pydata_sphinx_theme`** - Data science focused (used by pandas, NumPy)
4. **`alabaster`** - Minimal, classic Sphinx theme
5. **`classic`** - Traditional Sphinx appearance
6. **`nature`** - Green nature theme
7. **`pyramid`** - Clean, modern built-in theme
8. **`sphinxdoc`** - Sphinx's own documentation style

#### **Advanced: Environment-based Theme**

For dynamic theme switching, you can use environment variables in `conf.py`:

```python
import os
html_theme = os.getenv('SPHINX_THEME', 'sphinx_book_theme')  # Defaults to current theme
```

Then set in your environment:

**Windows:**
```powershell
$env:SPHINX_THEME = "furo"
.\make.bat html
```

**macOS/Linux:**
```bash
export SPHINX_THEME="furo"
make html
```

#### **Theme Customization**

For Furo theme, add custom colors to `conf.py`:

```python
html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#336699",
        "color-brand-content": "#336699",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4CAF50",
        "color-brand-content": "#4CAF50",
    },
}
```

### Adding Extensions

Add to `extensions` list in `conf.py`:
```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    # Add new extensions here
]
```

## Automation

### Continuous Documentation

You can automate documentation builds:

1. Add to your CI/CD pipeline
2. Use GitHub Actions or similar
3. Host on GitHub Pages, ReadTheDocs, etc.

### Example GitHub Actions Workflow

```yaml
name: Build Documentation
on: [push, pull_request]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    - name: Build docs
      run: |
        cd docs
        make html
```

## Best Practices

1. **Always use virtual environment**
2. **Write comprehensive docstrings**
3. **Rebuild docs after code changes**
4. **Keep documentation up to date with code**
5. **Use type hints for better auto-documentation**
6. **Test documentation builds in CI/CD**

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [NumPy Style Docstrings](https://numpydoc.readthedocs.io/en/latest/format.html)