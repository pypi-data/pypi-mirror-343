
set -e

echo "========================================"
echo "Testing MCPS CLI with agent commands"
echo "========================================"

echo "Installing dependencies..."
pip install -q -e .

echo -e "\n========================================"
echo "Testing agent discovery commands..."
echo "========================================"

mkdir -p ~/.mcps/agents/test-agent-001
mkdir -p ~/.mcps/agents/test-agent-002

cat > ~/.mcps/agents/test-agent-001/config.json << EOF
{
  "agent_id": "test-agent-001",
  "name": "Test Agent 1",
  "description": "A test agent for CLI testing",
  "version": "1.0.0",
  "capabilities": ["text", "cli"],
  "required_tools": [],
  "model_type": "python",
  "created_at": "2025-04-26T12:00:00Z",
  "updated_at": "2025-04-26T12:00:00Z",
  "owner": "mcps-team",
  "tags": ["test"],
  "config": {
    "runtime": "python"
  }
}
EOF

cat > ~/.mcps/agents/test-agent-002/config.json << EOF
{
  "agent_id": "test-agent-002",
  "name": "Test Agent 2",
  "description": "Another test agent for CLI testing",
  "version": "1.0.0",
  "capabilities": ["text", "websocket"],
  "required_tools": [],
  "model_type": "python",
  "created_at": "2025-04-26T12:00:00Z",
  "updated_at": "2025-04-26T12:00:00Z",
  "owner": "mcps-team",
  "tags": ["test"],
  "config": {
    "runtime": "python"
  }
}
EOF

cat > ~/.mcps/agents/test-agent-001/main.py << EOF
import sys
import json

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "No query provided"
    print(f"Test agent 1 received: {query}")
    return {"result": f"Processed by test-agent-001: {query}"}

if __name__ == "__main__":
    result = main()
    with open("output.json", "w") as f:
        json.dump(result, f)
EOF

cat > ~/.mcps/agents/test-agent-002/main.py << EOF
import sys
import json

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "No query provided"
    print(f"Test agent 2 received: {query}")
    return {"result": f"Processed by test-agent-002: {query}"}

if __name__ == "__main__":
    result = main()
    with open("output.json", "w") as f:
        json.dump(result, f)
EOF

echo -e "\nTesting 'mcps agent list'..."
python -m mcps.cli.commands.basic agent list --data-dir ~/.mcps/agents

echo -e "\nTesting 'mcps agent query'..."
python -m mcps.cli.commands.basic agent query "test agent" --data-dir ~/.mcps/agents

echo -e "\nTesting 'mcps agent capabilities'..."
python -m mcps.cli.commands.basic agent capabilities "text,cli" --data-dir ~/.mcps/agents

echo -e "\nTesting 'mcps agent info'..."
python -m mcps.cli.commands.basic agent info test-agent-001 --data-dir ~/.mcps/agents

echo -e "\n========================================"
echo "Testing agent lifecycle commands..."
echo "========================================"

echo -e "\nTesting 'mcps agent deploy'..."
python -m mcps.cli.commands.basic agent deploy test-agent-001 --data-dir ~/.mcps/agents

MOCK_DEPLOY_ID="test-deployment-001"
echo "Using mock deployment ID: $MOCK_DEPLOY_ID"

echo -e "\nTesting 'mcps agent start'..."
python -m mcps.cli.commands.basic agent start $MOCK_DEPLOY_ID --data-dir ~/.mcps/agents

echo -e "\nTesting 'mcps agent status'..."
python -m mcps.cli.commands.basic agent status $MOCK_DEPLOY_ID --data-dir ~/.mcps/agents

echo -e "\nTesting 'mcps agent run'..."
python -m mcps.cli.commands.basic agent run $MOCK_DEPLOY_ID "Hello from CLI test" --data-dir ~/.mcps/agents

echo -e "\nTesting 'mcps agent stop'..."
python -m mcps.cli.commands.basic agent stop $MOCK_DEPLOY_ID --data-dir ~/.mcps/agents

echo -e "\nTesting 'mcps agent cleanup'..."
python -m mcps.cli.commands.basic agent cleanup $MOCK_DEPLOY_ID --data-dir ~/.mcps/agents

echo -e "\nTest completed successfully!"
echo "========================================"
