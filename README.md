# Huginn Agents
I'm using Flask to host some simple REST APIs for custom Huginn agents. Learn more about Huginn [here](https://github.com/huginn/huginn).

## Installing
```
python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Testing
```
python -m pytest tests/
```

## Deploying

### Build & Run Flask Docker Container
```
docker rm -f huginn_agents
docker build -t deagle/agents:stable .
docker run --init --name huginn_agents --restart always -d -p 5800:5000 deagle/agents:stable
```
