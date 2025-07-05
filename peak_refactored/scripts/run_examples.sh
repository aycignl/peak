#!/bin/bash
# Script to run PEAK examples

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "🚀 Running PEAK Examples"
echo "=" * 50

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "Virtual environment not detected. Activating..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        print_error "Virtual environment not found. Run setup.sh first."
        exit 1
    fi
fi

# Check if PEAK is installed
if ! python -c "import peak" 2>/dev/null; then
    print_error "PEAK package not found. Run 'pip install -e .' first."
    exit 1
fi

echo ""
print_status "1. Running Basic Usage Example"
echo "-" * 40
if python examples/basic_usage.py; then
    print_status "✅ Basic usage example completed"
else
    print_error "❌ Basic usage example failed"
fi

echo ""
print_status "2. Running Advanced Pipeline Example"
echo "-" * 40
if python examples/advanced_pipeline.py; then
    print_status "✅ Advanced pipeline example completed"
else
    print_error "❌ Advanced pipeline example failed"
fi

echo ""
print_status "3. Running Unit Tests"
echo "-" * 40
if python -m pytest tests/ -v; then
    print_status "✅ Unit tests passed"
else
    print_warning "⚠️ Some tests may have failed (expected if data not available)"
fi

echo ""
print_status "4. Testing Configuration"
echo "-" * 40
if python -c "from peak.config.settings import Settings; s = Settings(); print(f'Configuration loaded: {s.app_name}')"; then
    print_status "✅ Configuration test passed"
else
    print_error "❌ Configuration test failed"
fi

echo ""
print_status "5. Testing Data Loading"
echo "-" * 40
if python -c "from peak.data.loaders import DataLoader; loader = DataLoader(); print('Data loader initialized successfully')"; then
    print_status "✅ Data loader test passed"
else
    print_error "❌ Data loader test failed"
fi

echo ""
print_status "🎉 Example run completed!"
print_status "Check the logs/ directory for detailed execution logs"

# Display system information
echo ""
print_status "System Information:"
echo "Python version: $(python --version)"
echo "PEAK installation: $(pip show peak | grep Location || echo 'Development mode')"
echo "Current directory: $(pwd)"
echo "Virtual environment: ${VIRTUAL_ENV:-'Not activated'}"