# Starter Project

uild a microservice that takes in TSV (tab-separated values, similar to CSV) File URL as input, and calculates the total value of the items in it.

curl -X POST 'https://{api}.execute-api.us-east-1.amazonaws.com/prod/v1' -H 'x-api-key:{api_key}' -H 'content-type:application/json' -d '{"url":"https://etix-pdf-dev.s3.amazonaws.com/9147_10832__0-10-5_7-5-2019.txt"}'

curl -X GET 'https://{api}.execute-api.us-east-1.amazonaws.com/prod/v1/jobs/{job_id}' -H 'x-api-key:{api-key}'
