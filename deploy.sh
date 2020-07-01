docker rm -f huginn_agents
docker build -t deagle/agents:stable .

docker run --d \
    --name huginn_agents \
    --network=huginn-net \
    --restart always \
    -p 5800:5000 \
    deagle/agents:stable
