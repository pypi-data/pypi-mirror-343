# Strynova Django Tailwind CSS

A Django package for integrating Tailwind CSS v4 into your Django projects.

## Features

- Easy integration of Tailwind CSS v4 in Django projects
- Template tags for including Tailwind CSS
- Built-in management command for compiling Tailwind CSS
- Bundled tailwindcss CLI - no need to install Node.js or npm!
- Customizable configuration
- No static files included - you define where your CSS files should be stored

## Installation

```bash
pip install strynova-dj-tailwindcss
```

## Configuration

1. Add `strynova_dj_tailwindcss` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'strynova_dj_tailwindcss',
    # ...
]
```

2. Configure Tailwind CSS settings in your `settings.py` (required):

```python
# Tailwind CSS Settings
TAILWIND_INPUT_PATH = 'path/to/input.css'  # Path to the input CSS file (required)
TAILWIND_OUTPUT_PATH = 'path/to/output.css'  # Path to the output CSS file (required)
TAILWIND_CLI_PATH = None  # Path to the tailwindcss CLI executable (optional, will use bundled executable if not specified)
```

Note: Both `TAILWIND_INPUT_PATH` and `TAILWIND_OUTPUT_PATH` are required. If the input.css file doesn't exist, it will be created automatically with the proper tailwindcss import statement.

3. No need to install Tailwind CSS or the CLI separately - they are bundled with the package!

## Usage

### Compiling Tailwind CSS

Before using Tailwind CSS in your templates, you need to compile it. The package includes a management command to do this:

```bash
# Build Tailwind CSS once
python manage.py tailwind

# Watch for changes and rebuild automatically
python manage.py tailwind --watch
```

You can also specify custom input and output paths that will override the settings:

```bash
python manage.py tailwind --input path/to/input.css --output path/to/output.css
```

Note: Either the settings in `settings.py` or command line arguments must be provided. If the input file doesn't exist, it will be created automatically with the proper tailwindcss import statement.

### Basic Usage

In your templates, load the template tags and use them to include Tailwind CSS:

```html
{% load tailwind_tags %}

<!DOCTYPE html>
<html>
<head>
    <title>My Django App</title>
    {% tailwind_css %}
</head>
<body>
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold text-blue-500">Hello, Tailwind CSS!</h1>
        <button class="btn-primary">Click Me</button>
    </div>
</body>
</html>
```

### Using the Filter

You can also use the `tailwind_class` filter to add Tailwind CSS classes to existing class attributes:

```html
<div class="{{ existing_classes|tailwind_class:'bg-blue-500 text-white' }}">
    This div has both existing classes and Tailwind CSS classes.
</div>
```

## Development

### Prerequisites

- Python 3.7+
- Django 3.2+

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/strynova/strynova_dj_tailwindcss.git
cd strynova_dj_tailwindcss
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

3. Build Tailwind CSS:
```bash
python manage.py tailwind
```

4. For development, you can watch for changes:
```bash
python manage.py tailwind --watch
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
