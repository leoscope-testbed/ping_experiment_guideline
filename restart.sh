echo 'Stopping existing instance of leotest...'
sudo docker stop leotest 

echo 'Removing existing containers...'
sudo docker rm leotest 

echo 'Rebuilding leotest image...'
sudo docker build . -t leotest

echo 'Starting leotest container...'
sudo docker run --network host --cap-add CAP_NET_ADMIN --name leotest -v /home/leotest/leotest-testbed-v2/job_workdir:/artifacts -t -d leotest