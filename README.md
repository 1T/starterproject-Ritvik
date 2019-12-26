# Starter Project

Build a microservice that takes in TSV (tab-separated values, similar to CSV) File URL as input, and calculates the total value of the items in it.

## Params (Body)
* `url` - The complete URL path to the TSV (tab-separated) file


## Usage


### Sample
> The below is a sample invocation, included here for reference purposes.

```
curl -X POST 'https://{api}.execute-api.us-east-1.amazonaws.com/prod/v1' -H 'x-api-key:{api_key}' -H 'content-type:application/json' \
  -d '{"url":"https://etix-pdf-dev.s3.amazonaws.com/9147_10832__0-10-5_7-5-2019.txt"}'
```

### Actual
> The following is a live invocation that should return a successful response.
```
curl -X POST 'https://2msxgbd0l2.execute-api.us-east-1.amazonaws.com/prod/v1' \
  -H 'x-api-key: my-really-long-api-key' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://etix-pdf-dev.s3.amazonaws.com/9147_10832__0-10-5_7-5-2019.txt"}'
```
