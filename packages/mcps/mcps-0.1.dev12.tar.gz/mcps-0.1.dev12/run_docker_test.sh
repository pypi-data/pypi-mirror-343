
set -e

echo "========================================"
echo "Testing Docker sandbox runtime"
echo "========================================"

echo "Docker containers before test:"
docker ps -a

echo -e "\nDocker images before test:"
docker images

echo -e "\n========================================"
echo "Running Docker sandbox test..."
echo "========================================"
python examples/docker_sandbox_test.py

echo -e "\n========================================"
echo "Docker containers after test (should be cleaned up):"
docker ps -a

echo -e "\nTest completed successfully!"
echo "========================================"
