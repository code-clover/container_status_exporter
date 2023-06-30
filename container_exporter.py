from prometheus_client import start_http_server, Gauge
import docker
import time
import socket

client = docker.from_env()

start_http_server(8001)
print("Prometheus exporter started on port 8001")

metric = Gauge('container_status','Boolean value for container status',['container_name','docker_node'])

docker_node = socket.gethostname()

while True:
  containers = client.containers.list(all)

  for i in containers:
    name = i.name
    status = i.status

    if status != "running":
      status = 1
    else:
      status = 0

    label_values = {'container_name' : name, 'docker_node' : docker_node}

    metric.labels(**label_values).set(status)

    time.sleep(5)

