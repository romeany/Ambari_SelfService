#!/usr/bin/env python

"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from resource_management import *

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()

kibana_download_dir = '/tmp/kibana_tmp'
kibana_download = config['configurations']['kibana-env']['kibana_download']

kibana_install_log = format("{kibana_download_dir}/kibana-install.log")

kibana_user = 'root'
kibana_group = 'root'

server_port = config['configurations']['kibana-config']['server.port']
server_host = config['configurations']['kibana-config']['server.host']
server_name = config['configurations']['kibana-config']['server.name']
elasticsearch_url = config['configurations']['kibana-config']['elasticsearch.url']

kibana_conf_dir = config['configurations']['kibana-env']['kibana_conf_dir']
