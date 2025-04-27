
set -e

echo "========================================"
echo "Testing agent lifecycle management"
echo "========================================"

echo "Installing dependencies..."
pip install -q grpcio grpcio-tools protobuf websockets pytest pytest-asyncio

mkdir -p tests/agents/lifecycle/data/basic_agent
mkdir -p tests/agents/lifecycle/data/grpc_agent
mkdir -p tests/agents/lifecycle/data/websocket_agent

echo -e "\n========================================"
echo "Running lifecycle tests..."
echo "========================================"
pytest -xvs tests/agents/lifecycle/

echo -e "\nTest completed successfully!"
echo "========================================"
