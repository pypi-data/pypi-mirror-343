


set -e

echo "========================================="
echo "Publishing MCPS package to PyPI using tox"
echo "========================================="

echo "Cleaning old builds..."
tox -e clean

echo "Building package..."
tox -e build

export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-AgEIcHlwaS5vcmcCJDI0ODliNzE1LTQ2MTgtNDJiMC1hNmU2LTA4YWIzYjBhMWZhNQACKlszLCJkZGJiYTdkNi1iNGZjLTRkNjgtOTVmMC1iMzQ5M2RlYTY3YjYiXQAABiDYxIdfJAVhUfFPHLeCU4IJt07WKNMPqAaI_K7RQTiWiA"
export TWINE_REPOSITORY="pypi"

echo "Publishing package to PyPI..."
tox -e publish -- --repository pypi

echo "========================================="
echo "Package published successfully!"
echo "========================================="
