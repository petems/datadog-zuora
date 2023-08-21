import datetime
import json
import ssl
import time
from logging import info

import urllib3
from checks import AgentCheck


class SnaplogicTest(AgentCheck):

  def _disable_ssl_verification(self):
    try:
      _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
      # Legacy Python that doesn't verify HTTPS certificates by default
      pass
    else:
      # Handle target environment that doesn't support HTTPS verification
      ssl._create_default_https_context = _create_unverified_https_context

  def _check_connection(self, full_url, headers):
    http = urllib3.PoolManager()
    self.log.info("Attempting connection to {full_url} with {headers}".format(full_url=full_url, headers=headers))
    response = http.request('GET', full_url, headers = headers)
    if response.status != 200:
      self.log.error("Error Connecting: {status} - {data}".format(status=response.status, data=response.data))
      return
    else:
      self.log.info("Success Connecting")

  def _check_api_health(self, url, auth_headers):

    metric_http = urllib3.PoolManager()

    api_health_check_url = url + "/system-health/api-requests/volume-summary?startTime=2023-08-19T13%3A45%2B0000&endTime=2023-08-20T13%3A45%2B0000"

    response = metric_http.request('GET', api_health_check_url, headers = auth_headers)

    json_response = json.loads(response.data)

    response_data = json_response["data"]

    tags_list = {}

    self.log.info("API Health Check Response: {data}".format(data=response_data))

    length = len(response_data)

    for i in range(length):
      self.log.info(response_data[i])

      tags_list["path"] = response_data[i]["path"]
      tags_list["httpMethod"] = response_data[i]["httpMethod"]

      success_count = response_data[i]["success"]

      tags = self.dict_to_string_tags(tags_list)

      metric_name = 'zuora.system_health.success'
      self.log.info("Metric name: {metric_name}, tags = {tags}".format(metric_name=metric_name, tags=tags))

      self.gauge(name=metric_name, value=success_count, tags=tags)

  def _validate_instance(self, instance):
    for key in ['base_url', 'oauth_token']:
      if key not in instance:
        raise Exception("Config '{}' must be specified".format(key))

  def dict_to_string_tags(self, dict_to_convert):
    array_of_tag_strings = []
    for key, value in dict_to_convert.items():
      metric_string = '{key}:{value}'.format(key = key, value = value)
      array_of_tag_strings.append(metric_string)
    return array_of_tag_strings

  def check(self, instances):
    self._validate_instance(instances)

    # appears to be a temporary cert issue sometimes:
    self._disable_ssl_verification()

    zuora_url = instances['base_url']

    full_url = "https://" + zuora_url

    api_check_url = full_url + "/system-health/api-requests/volume-summary?startTime=2023-08-19T13%3A45%2B0000&endTime=2023-08-20T13%3A45%2B0000"

    auth = "Bearer " + instances['oauth_token']

    auth_headers = {'Authorization': auth}

    self._check_connection(api_check_url, auth_headers)

    # 1 Current Metrics to send
    # API Health: https://www.zuora.com/developer/api-references/api/tag/API-Health/

    self._check_api_health(full_url, auth_headers)
    
