docker rm -f huginn_agents
docker build -t deagle/agents:stable .

docker run -it \
    --name huginn_agents \
    --network=huginn-net \
    --restart always \
    -e PLAID_SECRET=84c82fd61f4e9ee0edd87806c37ab5 \
    -e ACCESS_TOKEN=access-development-62ceb466-3963-4b8b-9db9-030735fcf267 \
    -p 5800:5000 \
    deagle/agents:stable
