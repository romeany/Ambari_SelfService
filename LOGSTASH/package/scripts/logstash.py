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

class Logstash(Script):

    # Install Logstash
    def install(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        env.set_params(params)

        # Install dependent packages
        self.install_packages(env)

        # Create Logstash download tmp dir
        Directory([params.logstash_download_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.logstash_user,
                  group=params.logstash_group,
                  create_parents=True
                 )

        # Create empty Logstash install log
        File(params.logstash_install_log,
             mode=0644,
             owner=params.logstash_user,
             group=params.logstash_group,
             content=''
            )

        # Download Logstash
        cmd = format("cd {logstash_download_dir}; wget {logstash_download} -O logstash.rpm -a {logstash_install_log}")
        #cmd = "cd /var/www/html/ambari/;cp logstash-5.4.3.rpm logstash.rpm"
        Execute(cmd)

        # Install Logstash
        #cmd = "cd /var/www/html/ambari; rpm -Uvh logstash.rpm"
        #cmd = "cd /var/www/html/ambari; rpm --install logstash.rpm"
        cmd = format("cd {logstash_download_dir}; rpm --install logstash.rpm")
        Execute(cmd)

        cmd = "systemctl enable logstash.service"
        Execute(cmd)

        # Remove Logstash installation file
        cmd = format("rm -rf {logstash_download_dir}")
        Execute(cmd, user=params.logstash_user)

        Execute('echo "Install complete"')


    def stop(self, env):
        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # Stop Logstash
        cmd = 'systemctl stop logstash.service'
        Execute(cmd)

        if os.path.isfile(status_params.logstash_pid_file):
            sudo.unlink(status_params.logstash_pid_file)
        print 'Stop logstash complete'

    def start(self, env):

        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the status_params.logstash_pid_file property as
        #  format('{logstash_pid_file}')
        env.set_params(status_params)

        # Start Logstash
        cmd = 'systemctl start logstash.service'
        Execute(cmd)

        cmd = format("mkdir -p {logstash_pid_dir}")
        Execute(cmd)

        cmd = "pid=`ps -ef|awk '/\/etc\/logstash/{if ($3==1){print $2}}'`; if [ ! -z $pid ] ; then echo $pid > /var/run/logstash/logstash.pid ; fi"
        Execute(cmd)

        print 'Start logstash complete'


    def status(self, env):

        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the status_params.logstash_pid_file property as
        #  format('{logstash_pid_file}')
        env.set_params(status_params)

        #cmd = 'systemctl status logstash.service'

        cmd = "pid=`ps -ef|awk '/\/etc\/logstash/{if ($3==1){print $2}}'`; if [ ! -z $pid ] ; then echo $pid > /var/run/logstash/logstash.pid ; fi"
        Execute(cmd)

        # Use built-in method to check status using pidfile
        check_process_status(status_params.logstash_pid_file)

        print 'Status of the Logstash'


if __name__ == "__main__":
    Logstash().execute()
