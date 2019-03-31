# gen_go_struct.py

generate golang struct entity from mysql database.

## usage

```shell
python gen_go_struct.py [-h] [-u USER] [-s SERVER] [-p PORT] -d DATABASE
                        [-t TABLE] [-j]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  db user name
  -s SERVER, --server SERVER
                        db server
  -p PORT, --port PORT  db port
  -d DATABASE, --database DATABASE
                        database name
  -t TABLE, --table TABLE
                        table name
  -j, --json            add json tag
  ```