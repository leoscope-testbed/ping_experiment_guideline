echo "Installing docker..."
sudo apt-get install -y docker.io

echo "Installing Leotest dependencies..."
python3 -m pip install -r requirements.txt

echo "Building Leotest image..."
docker build . -t <tag name>

echo "Done."