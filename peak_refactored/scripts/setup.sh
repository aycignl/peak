#!/bin/bash
# PEAK System Setup Script

set -e

echo "🚀 Setting up PEAK System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
print_status "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
if [ "$1" = "--dev" ]; then
    print_status "Installing development dependencies..."
    pip install -r requirements-dev.txt
fi

# Install the package in development mode
print_status "Installing PEAK package in development mode..."
pip install -e .

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs cache

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your configuration"
else
    print_status ".env file already exists"
fi

# Set up pre-commit hooks if in dev mode
if [ "$1" = "--dev" ]; then
    print_status "Setting up pre-commit hooks..."
    pre-commit install
fi

# Run basic tests to verify installation
print_status "Running basic verification tests..."
if python -c "from peak.config.settings import Settings; Settings()"; then
    print_status "✅ PEAK system setup completed successfully!"
else
    print_error "❌ Setup verification failed"
    exit 1
fi

echo ""
print_status "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Add your data files to the data/ directory"
echo "3. Run 'python examples/basic_usage.py' to test the system"
echo "4. Check the documentation in docs/ for more information"

if [ "$1" = "--dev" ]; then
    echo ""
    print_status "Development setup complete. Additional commands:"
    echo "• Run tests: make test"
    echo "• Format code: make format"
    echo "• Check lint: make lint"
    echo "• Build docs: make docs"
fi

echo ""
print_status "🎉 Welcome to PEAK!"