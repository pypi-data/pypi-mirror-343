# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Author: Kiall Mac Innes <kiall@hpe.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from oslo_config import cfg
from oslo_log import log as logging

from designate.conf.mdns import DEFAULT_MDNS_PORT
from designate import dnsmiddleware
from designate import dnsutils
from designate.mdns import handler
from designate import service
from designate import storage
from designate import utils

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Service(service.Service):
    _dns_default_port = DEFAULT_MDNS_PORT

    def __init__(self):
        self._storage = None

        super(Service, self).__init__(
            self.service_name, threads=cfg.CONF['service:mdns'].threads,
        )
        self.dns_service = service.DNSService(
            self.dns_application, self.tg,
            cfg.CONF['service:mdns'].listen,
            cfg.CONF['service:mdns'].tcp_backlog,
            cfg.CONF['service:mdns'].tcp_recv_timeout,
        )

    def start(self):
        super(Service, self).start()
        self.dns_service.start()

    def stop(self, graceful=True):
        self.dns_service.stop()
        super(Service, self).stop(graceful)

    @property
    def storage(self):
        if not self._storage:
            self._storage = storage.get_storage()
        return self._storage

    @property
    def service_name(self):
        return 'mdns'

    @property
    @utils.cache_result
    def dns_application(self):
        # Create an instance of the RequestHandler class and wrap with
        # necessary middleware.
        application = handler.RequestHandler(self.storage, self.tg)
        application = dnsmiddleware.TsigInfoMiddleware(
            application, self.storage
        )
        application = dnsmiddleware.SerializationMiddleware(
            application, dnsutils.TsigKeyring(self.storage)
        )

        return application
