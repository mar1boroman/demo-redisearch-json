# RedisSearch + RedisJSON Demo

A demo exploring realistic data from mobile phone users across India, using RediSearch and RedisJSON modules of Redis Enterprise

### Running the script from source

Download the repository

```bash
git clone https://github.com/mar1boroman/demo-redisearch-json.git && cd demo-redisearch-json
```

Prepare and activate the virtual environment

```bash
python3 -m venv .env && source .env/bin/activate
```

Install necessary libraries and dependencies

```bash
pip install -r requirements.txt
```

Unzip the data file to be used
```bash
gunzip wireless.json.gz
```

Follow the instructions at [Demo Instructions](./demo-instructions.md)