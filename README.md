# RedisSearch + RedisJSON Demo

A demo exploring realistic data from mobile phone users across India, using RediSearch and RedisJSON modules of Redis Enterprise

## Demo Features

- ~2.5 million JSON documents (approx 1 KB / doc)
- RedisJSON Features
    - JSON SET and GET documents, with nesting and GEO data
    - JSON OBJKEYS and OBJLEN features
    - Deleting JSON Documents
- RediSearch Features
    - DROP and CREATE Index on JSON Documents
    - Information of Indexes
    - Querying TAG and TEXT fields
    - Aggregations
        - GROUPING, SORTING 
        - Aggregation over Time based data
        - Aggregation over Geo Location data

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