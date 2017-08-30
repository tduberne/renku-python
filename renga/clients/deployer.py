# -*- coding: utf-8 -*-
#
# Copyright 2017 Swiss Data Science Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Client for deployer service."""

import requests

from ._datastructures import namedtuple
from ._utils import return_response

from renga.clients._datastructures import Endpoint, EndpointMixin

Context = namedtuple('Context', ['id', 'spec'])
"""Deployer execution context."""

Execution = namedtuple('Execution', ['id', 'engine', 'namespace'])
"""Deployer execution object."""


class DeployerClient(EndpointMixin):
    """Client for the deployer service."""

    contexts_endpoint = Endpoint('/api/deployer/contexts')
    context_endpoint = Endpoint('/api/deployer/contexts/{}')
    executions_endpoint = Endpoint('/api/deployer/contexts/{}/executions')
    execution_endpoint = Endpoint('/api/deployer/contexts/{0}/executions/{1}')
    execution_logs_endpoint = Endpoint('/api/deployer/'
                                       'contexts/{0}/executions/{1}/logs')
    execution_ports_endpoint = Endpoint('/api/deployer/'
                                        'contexts/{0}/executions/{1}/ports')

    def list_contexts(self, access_token):
        """List all known contexts."""
        r = requests.get(
            self.contexts_endpoint,
            headers={'Authorization': 'Bearer {0}'.format(access_token)})

        return return_response(r, ok_code=200, return_json=True)

    def create_context(self, spec, access_token):
        """Create a new deployment context."""
        r = requests.post(
            self.contexts_endpoint,
            headers={'Authorization': 'Bearer {0}'.format(access_token)},
            json=spec)

        return return_response(r, ok_code=201, return_json=True)

    def list_executions(self, context_id, access_token):
        """List all executions of a given context."""
        r = requests.get(
            self.executions_endpoint.format(context_id),
            headers={'Authorization': 'Bearer {0}'.format(access_token)})

        return return_response(r, ok_code=200, return_json=True)

    def create_execution(self, context_id, engine, access_token):
        """Create an execution of a context on a given engine."""
        r = requests.post(
            self.executions_endpoint.format(context_id),
            headers={'Authorization': 'Bearer {0}'.format(access_token)},
            json={'engine': engine})

        return return_response(r, ok_code=201, return_json=True)

    def delete_execution(self, context_id, execution_id):
        """Delete an execution."""
        r = requests.delete(
            self.execution_endpoint.format(context_id, execution_id),
            headers={'Authorization': 'Bearer {0}'.format(access_token)})

        return return_response(r, ok_code=200)

    def get_logs(self, context_id, execution_id, access_token):
        """Retrieve logs of an execution."""
        r = request.get(
            self.execution_logs_endpoint.format(context_id, execution_id),
            headers={'Authorization': 'Bearer {0}'.format(access_token)})

        return return_response(r, ok_code=200, return_json=True)

    def get_ports(self, context_id, execution_id, access_token):
        """Retrieve port mappings for an execution."""
        r = request.get(
            self.execution_ports_endpoint.format(context_id, execution_id),
            headers={'Authorization': 'Bearer {0}'.format(access_token)})

        return return_response(r, ok_code=200, return_json=True)
