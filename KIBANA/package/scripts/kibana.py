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

import os
from resource_management import *
from resource_management.core import sudo

class Kibana(Script):

    # Install Kibana
    def install(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        env.set_params(params)

        # Install dependent packages
        self.install_packages(env)

        # Create Kibana download tmp dir
        Directory([params.kibana_download_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.kibana_user,
                  group=params.kibana_group,
                  create_parents=True
                 )

        # Create empty Kibana install log
        File(params.kibana_install_log,
             mode=0644,
             owner=params.kibana_user,
             group=params.kibana_group,
             content=''
            )

        # Download Kibana
        cmd = format("cd {kibana_download_dir}; wget {kibana_download} -O kibana.rpm -a {kibana_install_log}")
        #cmd = "cd /var/www/html/ambari/;cp kibana-5.4.3-x86_64.rpm kibana.rpm"
        Execute(cmd)

        # Install Kibana
        #cmd = "cd /var/www/html/ambari; rpm -Uvh kibana.rpm"
        #cmd = "cd /var/www/html/ambari; rpm --install kibana.rpm"
        cmd = format("cd {kibana_download_dir}; rpm --install kibana.rpm")
        Execute(cmd)

        cmd = "systemctl enable kibana.service"
        Execute(cmd)

        # Remove Kibana installation file
        cmd = format("rm -rf {kibana_download_dir}")
        Execute(cmd, user=params.kibana_user)

        Execute('echo "Install complete"')


    def configure(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.kibana_pid_file property as
        # format('{kibana_pid_file}')
        env.set_params(params)

        configurations = params.config['configurations']['kibana-config']

        File(format("{kibana_conf_dir}/kibana.yml"),content=Template("kibana.yml.j2",configurations=configurations),
             owner=params.kibana_user,group=params.kibana_group)

        Execute('echo "Configuration complete"')


    def stop(self, env):
        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # Stop Kibana
        cmd = 'systemctl stop kibana.service'
        Execute(cmd)

        if os.path.isfile(status_params.kibana_pid_file):
            sudo.unlink(status_params.kibana_pid_file)
        print 'Stop kibana complete'

    def start(self, env):

        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the status_params.kibana_pid_file property as
        #  format('{kibana_pid_file}')
        env.set_params(status_params)

        # Configure Kibana
        self.configure(env)

        # Start Kibana
        cmd = 'systemctl start kibana.service'
        Execute(cmd)

        cmd = format("mkdir -p {kibana_pid_dir}")
        Execute(cmd)

        cmd = "pid=`ps -ef|awk '/\/etc\/kibana/{if ($3==1){print $2}}'`; if [ ! -z $pid ] ; then echo $pid > /var/run/kibana/kibana.pid ; fi"
        Execute(cmd)

        print 'Start kibana complete'


    def status(self, env):

        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the status_params.kibana_pid_file property as
        #  format('{kibana_pid_file}')
        env.set_params(status_params)

        cmd = "pid=`ps -ef|awk '/\/etc\/kibana/{if ($3==1){print $2}}'`; if [ ! -z $pid ] ; then echo $pid > /var/run/kibana/kibana.pid ; fi"
        Execute(cmd)

        # Use built-in method to check status using pidfile
        check_process_status(status_params.kibana_pid_file)

        print 'Status of the kibana'


if __name__ == "__main__":
    Kibana().execute()
