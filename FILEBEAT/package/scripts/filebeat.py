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

class Filebeat(Script):

    # Install Filebeat
    def install(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        env.set_params(params)

        # Install dependent packages
        self.install_packages(env)

        # Create Filebeat download tmp dir
        Directory([params.filebeat_download_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.filebeat_user,
                  group=params.filebeat_group,
                  create_parents=True
                 )

        # Create empty Filebeat install log
        File(params.filebeat_install_log,
             mode=0644,
             owner=params.filebeat_user,
             group=params.filebeat_group,
             content=''
            )

        # Download Filebeat
        cmd = format("cd {filebeat_download_dir}; wget {filebeat_download} -O filebeat.rpm -a {filebeat_install_log}")
        #cmd = "cd /var/www/html/ambari/;cp filebeat-5.4.3.rpm filebeat.rpm"
        Execute(cmd)

        # Install Filebeat
        #cmd = "cd /var/www/html/ambari; rpm -Uvh filebeat.rpm"
        #cmd = "cd /var/www/html/ambari; rpm --install filebeat.rpm"
        cmd = format("cd {filebeat_download_dir}; rpm --install filebeat.rpm")
        Execute(cmd)

        cmd = "chkconfig --add filebeat"
        Execute(cmd)
        # Remove Filebeat installation file
        cmd = format("rm -rf {filebeat_download_dir}")
        Execute(cmd, user=params.filebeat_user)

        Execute('echo "Install complete"')


    def stop(self, env):

        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # Stop Filebeat
        cmd = '/etc/init.d/filebeat stop'
        Execute(cmd)

        if os.path.isfile(status_params.filebeat_pid_file):
            sudo.unlink(status_params.filebeat_pid_file)
        print 'Stop filebeat complete'

    def start(self, env):
        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the status_params.filebeat_pid_file property as
        #  format('{filebeat_pid_file}')
        env.set_params(status_params)

        # Start Filebeat
        cmd = '/etc/init.d/filebeat start'
        Execute(cmd)

        cmd = format("mkdir -p {filebeat_pid_dir}")
        Execute(cmd)

        cmd = "pid=`ps -ef|awk '/\/etc\/filebeat/{if ($3==1){print $2}}'`; if [ ! -z $pid ] ; then echo $pid > /var/run/filebeat/filebeat.pid ; fi"
        Execute(cmd)

        print 'Start filebeat complete'


    def status(self, env):

        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the status_params.filebeat_pid_file property as
        #  format('{filebeat_pid_file}')
        env.set_params(status_params)

        #cmd = format("/etc/init.d/filebeat status")

        cmd = "pid=`ps -ef|awk '/\/etc\/filebeat/{if ($3==1){print $2}}'`; if [ ! -z $pid ] ; then echo $pid > /var/run/filebeat/filebeat.pid ; fi"
        Execute(cmd)

        # Use built-in method to check status using pidfile
        check_process_status(status_params.filebeat_pid_file)

        print 'Status of the Filebeat'

if __name__ == "__main__":
    Filebeat().execute()
