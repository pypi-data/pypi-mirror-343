
set -e

echo "========================================"
echo "Testing agent discovery and Docker integration"
echo "========================================"

echo "Installing dependencies..."
pip install -q docker grpcio grpcio-tools protobuf websockets pytest pytest-asyncio

mkdir -p data/cache

echo -e "\n========================================"
echo "Running agent Docker test..."
echo "========================================"
python examples/agent_discovery_docker.py

echo -e "\nTest completed successfully!"
echo "========================================"
