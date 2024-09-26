# AWS


## Redis Installation in EC2

* sudo yum install gcc
* wget http://download.redis.io/redis-stable.tar.gz
* tar xvzf redis-stable.tar.gz
* cd redis-stable
* make
* cd src
* chmod a+x redis-cli
* ./redis-cli
* exit
* ./redis-cli -h demo.pmrf6q.ng.0001.use1.cache.amazonaws.com -p 6379 (make sure Both encryption in transit and at rest are disabled at the time of creations)
* set a "hello abhi"
* get a
