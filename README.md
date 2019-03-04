# Ping to csv

## One command (Windows / Linux)

Getting started :

1. Clone the repository

```
$ git clone https://github.com/ferreolgodebarge/latency.git

$ cd latency
```

2. You will have this structure

Tree:

```
latency
|__latency.py
|__hosts
```

3. Edit `hosts` file with the server you need to ping

4. You can execute this command :

```
$ python latency.py <input_file> <number_of_pings>
```

ex. : ```python latency.py hosts 5 ```

5. You will have a csv output with ping summary :

Output tree:

```
latency
|__latency.py
|__hosts
|__ping_output.csv
```

Tested with :

- python 3.6.6 / Linux Ubuntu
- python 3.7.2 / Windows 10
