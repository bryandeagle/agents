docker rm -f huginn_agents
docker build -t deagle/agents:stable .

docker run --init -d \
    --name huginn_agents \
    --restart always \
    -p 5800:5000 \
    deagle/agents:stable
