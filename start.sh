echo 'Starting leotest container...'
sudo docker run --network host --cap-add CAP_NET_ADMIN --name leotest -v /artifacts:/artifacts -t -d leotest

