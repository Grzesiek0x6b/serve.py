serve.py
==========

Set up simple http server to share files.
Files will be downloadable from http://HOST:PORT/ALIAS

## Usage
```
$ serve.py --help
```
```
Usage: serve.py [options] ALIAS=FILEPATH ...

Set up simple http server to share files. Files will be downloadable from
http://HOST:PORT/ALIAS

Options:
  -h, --help            show this help message and exit
  -a HOST, --addr=HOST  Host on which server will listen. Predefined values:
                        'local' (for 127.0.0.1), 'public' (find public ip of
                        machine), 'any' (listen on any address) [default:
                        local].
  -p PORT, --port=PORT  Port on which server will listen [default: 8080].
```

### Usage example
To host your ```.bashrc``` and ```.profile``` files on your public ip and port 80, run
```
$ serve.py -a public -p 80 mybash=$HOME/.bashrc myprof=$HOME/.profile
```
You will see message similar to
```Added http://YOUR_IP:80/mybash -> /home/YOUR_USER/.bashrc```
so visit http://YOUR_IP:80/mybash on different machine to get your .bashrc file.

## Requirements
* Python (2.7 or 3.x)
* CherryPy

