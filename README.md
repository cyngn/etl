ETL
===

Collection of scripts to do things with data

nginx-to-json.py
----------------

Converts an nginx access log to JSON format that matches fluentd.  Outputs files to the "out" directory in your working directory.  Assumes your data will be partitioned by date, using the "dt" field.  Each file created should be approximately 128MB before compression.

```
pv /var/log/nginx/access.log | python nginx-to-json.py nginx.access
```
