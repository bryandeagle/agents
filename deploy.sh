docker rm -f huginn_agents
docker build -t deagle/agents:stable .

docker run --init \
    --name huginn_agents \
    --network=huginn-net \
    --restart always \
    -p 80:5000 \
    deagle/agents:stable
