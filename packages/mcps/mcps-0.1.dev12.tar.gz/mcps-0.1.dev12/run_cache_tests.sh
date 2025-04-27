
set -e

echo "========================================"
echo "Testing message and log caching"
echo "========================================"

echo "Installing dependencies..."
pip install -q pytest pytest-asyncio

echo -e "\n========================================"
echo "Running cache tests..."
echo "========================================"
PYTHONPATH=$PWD pytest -xvs tests/utils/cache/test_cache.py

echo -e "\nTest completed successfully!"
echo "========================================"
