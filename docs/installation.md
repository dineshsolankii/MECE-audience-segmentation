# Installation Guide

This guide will help you install and set up the MECE Audience Segmentation System.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mece-audience-segmentation
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python projects:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your configuration
nano .env  # or use your preferred editor
```

### 5. Verify Installation

Run the quick demo to verify everything is working:

```bash
python setup.py
```

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError` when running the application
- **Solution**: Make sure you're in the virtual environment and all dependencies are installed

**Issue**: Permission errors on macOS/Linux
- **Solution**: Use `python3` instead of `python` if you have both Python 2 and 3 installed

**Issue**: Package installation fails
- **Solution**: Update pip: `pip install --upgrade pip`

### Dependencies

The system requires the following Python packages:

- `pandas>=1.5.0` - Data manipulation and analysis
- `numpy>=1.21.0` - Numerical computing
- `python-dotenv>=0.19.0` - Environment variable management
- `scikit-learn>=1.1.0` - Machine learning utilities
- `matplotlib>=3.5.0` - Plotting and visualization
- `seaborn>=0.11.0` - Statistical data visualization
- `jupyter>=1.0.0` - Jupyter notebook support
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=3.0.0` - Coverage reporting
- `black>=22.0.0` - Code formatting
- `flake8>=4.0.0` - Linting
- `mypy>=0.950` - Type checking

## Development Setup

For development work, install additional development dependencies:

```bash
pip install -r requirements.txt
pip install black flake8 mypy pytest-cov
```

## Docker Installation (Optional)

If you prefer using Docker:

```bash
# Build the Docker image
docker build -t mece-segmentation .

# Run the application
docker run -it mece-segmentation python setup.py
```

## Next Steps

After installation, you can:

1. Read the [Usage Guide](usage.md) to learn how to use the system
2. Check the [API Reference](api_reference.md) for detailed documentation
3. Run the test suite: `pytest tests/`
4. Explore the example notebooks in the `notebooks/` directory
