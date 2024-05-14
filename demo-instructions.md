
# Creating a Redis Database

Create a Redis Enterprise database

Ensure that RediSearch and RedisJSON modules are enabled

# Load data

```bash
python load_data.py <HOST> <PORT>
```
or

```bash
python load_data.py -u <USERNAME> -x <PASSWORD> <HOST> <PORT>
```

# Redis JSON Operations

```sql
JSON.SET {wireless}:0 "$" '{
	"radio": "GSM",
	"mcc": 405,
	"mnc": 812,
	"lac": 404,
	"cid": 21802,
	"changeable_0": 0,
	"long": 75.873641967773,
	"lat": 30.895614624023,
	"range": 1000,
	"sample": 1,
	"changeable_1": 1,
	"created": 1455866914,
	"updated": 1455866914,
	"avgsignal": 0,
	"details": {
		"operator": "MyOperator",
		"circle": "Kerala"
	},
	"id": "0",
	"loc": ["75.873641967773, 30.895614624023"]
	}'
```

```sql
JSON.GET {wireless}:1 $.radio $.details.circle $.details.operator
```

```sql
JSON.SET {wireless}:1 "$.details.circle" '"Kochi"'
```

```sql
JSON.OBJKEYS {wireless}:1
```

```sql
JSON.OBJLEN {wireless}:1 $.details
```

```sql
JSON.DEL {wireless}:1
```

Full List of commands
https://redis.io/commands/?group=json

# RedisSearch

Full List of commands

https://redis.io/commands/?group=search

https://redis.io/commands/?group=suggestion

## Create Index

Note that the index will take about 5 minutes to index all the documents

```sql
FT.DROPINDEX idx:wireless

FT.CREATE idx:wireless
	ON JSON
	PREFIX 1 '{wireless}:'
	SCHEMA
		"$.id" as id NUMERIC
		"$.radio" as radio TAG SORTABLE
		"$.mcc" as mcc NUMERIC SORTABLE
		"$.mnc" as mnc NUMERIC SORTABLE
		"$.lac" as lac NUMERIC SORTABLE
		"$.cid" as cid NUMERIC SORTABLE
		"$.changeable_0" as changeable_0 NUMERIC SORTABLE
		"$.long" as long NUMERIC SORTABLE
		"$.lat" as lat NUMERIC SORTABLE
		"$.range" as range NUMERIC SORTABLE
		"$.sample" as sample NUMERIC SORTABLE
		"$.changelable_1" as changelable_1 NUMERIC SORTABLE
		"$.created" as created NUMERIC SORTABLE
		"$.updated" as updated NUMERIC SORTABLE
		"$.avgsignal" as avgsignal NUMERIC SORTABLE
		"$.details.operator" as operator TEXT SORTABLE
		"$.details.circle" as circle TEXT SORTABLE
		"$.loc" as loc GEO

FT.INFO idx:wireless
```

## TAG Fields 
```sql
FT.SEARCH idx:wireless "@radio:{'GSM'}"
```

```sql
FT.TAGVALS idx:wireless radio
```

## TEXT Search

```sql
FT.SEARCH idx:wireless @circle:"Kerala"
```


## Aggregation

Total number of users in Kerala

```sql
FT.AGGREGATE idx:wireless @circle:Kerala
	GROUPBY 1 @radio
	REDUCE COUNT 0 as count
    DIALECT 3
```
Website to get unix timestamps : https://www.epochconverter.com/

**Users created in 2015**

```sql
FT.SEARCH idx:wireless @created:[1420050600,1451586600]
```
The above query searches for all records with created field in 2015


**Number of users per operator in 2015**

```sql
FT.AGGREGATE idx:wireless @created:[1420050600,1451586600]
	GROUPBY 1 @operator 
		REDUCE COUNT 0 AS cnt 
	SORTBY 2 @cnt DESC
    DIALECT 3
```

**Anomaly Detection**

```sql
FT.SEARCH idx:wireless "@loc:[76.267303 9.931233 15 km]"
```

@loc:[76.267303  9.931233 5 km] -- Kochi

```sql
FT.AGGREGATE idx:wireless "@loc:[76.267303 9.931233 15 km]"
	GROUPBY 1 @circle
	REDUCE COUNT 0 as CNT
	SORTBY 2 @CNT DESC
    DIALECT 3
```

@loc:[72.877426 19.076090 5 km] -- Mumbai
```sql
FT.AGGREGATE idx:wireless "@loc:[72.877426 19.076090 15 km]"
	GROUPBY 1 @circle
	REDUCE COUNT 0 as CNT
	SORTBY 2 @CNT DESC
    DIALECT 3
```

Notice anything weird about the results? A fast way to detect anomalies in your data at real time or over huge volume of data (~2.5 mil records)
