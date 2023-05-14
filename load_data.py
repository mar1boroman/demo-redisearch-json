import redis
import argparse
from rich.progress import track
import json
import multiprocessing
from typing import List

def main():
  parser = argparse.ArgumentParser()

  parser.add_argument(
      "host",
      help='''
      Redis Enterprise Host
      '''
  )
  parser.add_argument(
      "port",
      help='''
      Redis Enterprise Port
      '''
  )
  parser.add_argument(
      "-u",
      "--username",
      help='''
      Redis Enterprise Username
      '''
  )
  parser.add_argument(
      "-x",
      "--password",
      help='''
      Redis Enterprise Password
      '''
  )

  args = parser.parse_args()

  redis_port = args.port
  redis_host = args.host
  redis_username = args.username
  redis_password = args.password
  
  r = redis.Redis(host=redis_host, port=redis_port, username=redis_username, password=redis_password)
  print(f"Flushing existing data from Redis database \n {redis_host}:{redis_port}")
  r.flushdb()
  print("All existing data deleted")
  # p = r.pipeline()

  processes = []
  
  
  with open('wireless.json', 'r') as f:
    data = json.load(f)
    p = r.pipeline()
    for index, record in track(enumerate(data),description='Reading data from the JSON file',transient=True):
      for k,v in record.items():
          p.json().set(k,'$',v)
      if index > 0 and index%350000 == 0:
        print(f"Number of records read : {index}")
        prc = multiprocessing.Process(target=p.execute)
        processes.append(prc)
        p = r.pipeline()
        
    print(f"Number of records in pipeline : {index}")
    prc = multiprocessing.Process(target=p.execute)
    processes.append(prc)
  
  
  for proc in processes:
    print(f"Starting process {proc}")
    proc.start()
  
  for proc in processes:
    proc.join()

  print('Data Load complete!')

if __name__ == "__main__":
    main()
    
  
