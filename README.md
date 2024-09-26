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


# Memcache installation on EC2

* sudo yum install -y libevent libevent-devel
* sudo yum install -y gcc make
* sudo wget http://www.memcached.org/files/memcached-1.4.24.tar.gz
* sudo tar xvzf memcached-1.4.24.tar.gz
* cd memcached-1.4.24
* sudo ./configure --enable-64bit
* sudo make && sudo make install

* sudo yum install -y telnet
* telnet demo-memcache.pmrf6q.cfg.use1.cache.amazonaws.com 11211
* set my_key 0 60 5
* hello
* get my_key
* quit
