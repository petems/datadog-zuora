FROM datadog/agent:latest
ADD ./zuora.yaml /etc/datadog-agent/conf.d/zuora.yaml
ADD ./zuora.py /etc/datadog-agent/checks.d/zuora.py

