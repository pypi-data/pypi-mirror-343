
set -e

echo "========================================"
echo "Testing global cache strategy"
echo "========================================"

echo "Installing dependencies..."
pip install -q pytest pytest-asyncio

echo -e "\n========================================"
echo "Running cache manager example..."
echo "========================================"
python examples/cache_manager_example.py

echo -e "\n========================================"
echo "Running cache manager tests..."
echo "========================================"
pytest -xvs tests/config/test_cache.py

echo -e "\nTest completed successfully!"
echo "========================================"
