# datadog-zuora

A quick Proof-of-concept to take metrics from the Zuora API

For now, it just takes the System Health Metric (# API Health: https://www.zuora.com/developer/api-references/api/tag/API-Health/) and submits the success count as a custom metric

## Running a test

```shell
docker-compose build
docker-compose up
```

Example Response

```shell
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | CORE | INFO | (pkg/collector/python/datadog_agent.go:127 in LogMessage) | zuora:8c357c292fc1cef5 | (zuora.py:25) | Attempting connection to https://rest.sandbox.eu.zuora.com/system-health/api-requests/volume-summary?startTime=2023-08-19T13%3A45%2B0000&endTime=2023-08-20T13%3A45%2B0000 with {'Authorization': 'Bearer ***************************98192'}
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | CORE | INFO | (pkg/collector/python/datadog_agent.go:127 in LogMessage) | zuora:8c357c292fc1cef5 | (zuora.py:31) | Success Connecting
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | PROCESS | INFO | (collector.go:238 in logCheckDuration) | Finished container check #4 in 3.247051ms
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | CORE | INFO | (pkg/collector/python/datadog_agent.go:127 in LogMessage) | zuora:8c357c292fc1cef5 | (zuora.py:47) | API Health Check Response: [{'path': '/objects/definitions/default', 'httpMethod': 'GET', 'success': 20, 'error': 0, 'total': 20}, {'path': '/v1/connections', 'httpMethod': 'GET', 'success': 31, 'error': 0, 'total': 31}, {'path': 'soap:query', 'httpMethod': 'POST', 'success': 49, 'error': 0, 'total': 49}]
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | CORE | INFO | (pkg/collector/python/datadog_agent.go:127 in LogMessage) | zuora:8c357c292fc1cef5 | (zuora.py:52) | {'path': '/objects/definitions/default', 'httpMethod': 'GET', 'success': 20, 'error': 0, 'total': 20}
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | CORE | INFO | (pkg/collector/python/datadog_agent.go:127 in LogMessage) | zuora:8c357c292fc1cef5 | (zuora.py:62) | Metric name: zuora.system_health.success, tags = ['path:/objects/definitions/default', 'httpMethod:GET']
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | CORE | INFO | (pkg/collector/python/datadog_agent.go:127 in LogMessage) | zuora:8c357c292fc1cef5 | (zuora.py:52) | {'path': '/v1/connections', 'httpMethod': 'GET', 'success': 31, 'error': 0, 'total': 31}
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | CORE | INFO | (pkg/collector/python/datadog_agent.go:127 in LogMessage) | zuora:8c357c292fc1cef5 | (zuora.py:62) | Metric name: zuora.system_health.success, tags = ['path:/v1/connections', 'httpMethod:GET']
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | CORE | INFO | (pkg/collector/python/datadog_agent.go:127 in LogMessage) | zuora:8c357c292fc1cef5 | (zuora.py:52) | {'path': 'soap:query', 'httpMethod': 'POST', 'success': 49, 'error': 0, 'total': 49}
datadog-zuora-datadog-1  | 2023-08-24 10:45:58 UTC | CORE | INFO | (pkg/collector/python/datadog_agent.go:127 in LogMessage) | zuora:8c357c292fc1cef5 | (zuora.py:62) | Metric name: zuora.system_health.success, tags = ['path:soap:query', 'httpMethod:POST'
```

Example Graph of custom Metric in Datadog:

![Dashboard Example](https://github.com/petems/datadog-zuora/assets/1064715/3c24412a-d5a7-4325-880c-96aa4f335031)