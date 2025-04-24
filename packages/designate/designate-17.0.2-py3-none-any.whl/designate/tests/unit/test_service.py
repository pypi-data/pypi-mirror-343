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
import errno
import socket
from unittest import mock

from oslo_config import cfg
from oslo_config import fixture as cfg_fixture
from oslo_service import service
import oslotest.base

from designate.common import profiler
from designate.mdns import handler
from designate import policy
from designate import rpc
from designate import service as designate_service
from designate import utils

CONF = cfg.CONF


class TestBaseService(oslotest.base.BaseTestCase):
    def tearDown(self):
        designate_service._launcher = None
        super(TestBaseService, self).tearDown()

    @mock.patch.object(service, 'launch')
    def test_serve(self, mock_service_launch):
        server = mock.Mock()
        designate_service.serve(server)

        mock_service_launch.assert_called_with(
            mock.ANY, server, workers=None, restart_method='mutate'
        )

    @mock.patch.object(service, 'launch')
    def test_serve_twice(self, _):
        server = mock.Mock()
        designate_service.serve(server)
        self.assertRaisesRegex(
            RuntimeError,
            r'serve\(\) can only be called once',
            designate_service.serve, server
        )

    @mock.patch.object(rpc, 'cleanup')
    @mock.patch.object(service, 'launch')
    def test_wait(self, mock_service_launch, mock_rpc_cleanup):
        server = mock.Mock()

        designate_service.serve(server)
        designate_service.wait()

        mock_service_launch.assert_called_with(
            mock.ANY, server, workers=None, restart_method='mutate'
        )
        mock_rpc_cleanup.assert_called()

    @mock.patch.object(rpc, 'cleanup')
    @mock.patch.object(service, 'launch')
    def test_wait_keyboard_interrupt(self, mock_service_launch,
                                     mock_rpc_cleanup):
        server = mock.Mock()
        mock_launcher = mock.Mock()
        mock_service_launch.return_value = mock_launcher
        mock_launcher.wait.side_effect = [KeyboardInterrupt]

        designate_service.serve(server)
        designate_service.wait()

        mock_rpc_cleanup.assert_called()


@mock.patch.object(policy, 'init')
@mock.patch.object(rpc, 'init')
@mock.patch.object(profiler, 'setup_profiler')
class TestServiceInit(oslotest.base.BaseTestCase):
    def test_service_init(self, mock_setup_profiler, mock_rpc_init,
                          mock_policy_init):
        service = designate_service.Service('test-service')

        mock_policy_init.assert_called_once()
        mock_rpc_init.assert_called_once()
        mock_setup_profiler.assert_called_once()

        self.assertEqual('test-service', service.name)

    def test_rpc_service_init(self, mock_setup_profiler, mock_rpc_init,
                              mock_policy_init):
        service = designate_service.RPCService(
            'test-rpc-service', 'test-topic'
        )

        mock_policy_init.assert_called_once()
        mock_rpc_init.assert_called_once()
        mock_setup_profiler.assert_called_once()

        self.assertEqual([service], service.endpoints)
        self.assertEqual('test-topic', service.rpc_topic)
        self.assertEqual('test-rpc-service', service.name)


class TestRpcService(oslotest.base.BaseTestCase):
    @mock.patch.object(policy, 'init')
    @mock.patch.object(rpc, 'init')
    @mock.patch.object(profiler, 'setup_profiler')
    def setUp(self, mock_setup_profiler, mock_rpc_init,
              mock_policy_init):
        super(TestRpcService, self).setUp()
        self.service = designate_service.RPCService(
            'test-rpc-service', 'test-topic'
        )

        mock_policy_init.assert_called_once()
        mock_rpc_init.assert_called_once()
        mock_setup_profiler.assert_called_once()

    @mock.patch.object(rpc, 'get_server')
    @mock.patch.object(rpc, 'get_notifier')
    def test_rpc_service_start(self, mock_rpc_get_server,
                               mock_rpc_get_notifier):
        self.assertIsNone(self.service.start())

        mock_rpc_get_server.assert_called_once()
        mock_rpc_get_notifier.assert_called_once()

        self.service.rpc_server.start.assert_called_once()

    @mock.patch.object(rpc, 'get_server')
    @mock.patch.object(rpc, 'get_notifier')
    def test_rpc_service_stop(self, mock_rpc_get_server,
                              mock_rpc_get_notifier):
        self.assertIsNone(self.service.start())

        mock_rpc_get_server.assert_called_once()
        mock_rpc_get_notifier.assert_called_once()

        self.assertIsNone(self.service.stop())

        self.service.rpc_server.stop.assert_called_once()

    def test_rpc_service_wait(self):
        self.assertIsNone(self.service.wait())


class TestDNSService(oslotest.base.BaseTestCase):
    def setUp(self):
        super(TestDNSService, self).setUp()
        self.useFixture(cfg_fixture.Config(CONF))

        self.tg = mock.Mock()
        self.storage = mock.Mock()
        self.application = handler.RequestHandler(self.storage, self.tg)

        self.service = designate_service.DNSService(
            self.application, self.tg,
            CONF['service:mdns'].listen,
            CONF['service:mdns'].tcp_backlog,
            CONF['service:mdns'].tcp_recv_timeout,
        )
        self.service._running = mock.Mock()

    def test_service_init(self):
        self.assertEqual(CONF['service:mdns'].listen, self.service.listen)
        self.assertEqual(
            CONF['service:mdns'].tcp_backlog, self.service.tcp_backlog
        )
        self.assertEqual(
            CONF['service:mdns'].tcp_recv_timeout,
            self.service.tcp_recv_timeout
        )

    @mock.patch.object(utils, 'bind_tcp')
    @mock.patch.object(utils, 'bind_udp')
    def test_service_start(self, mock_bind_udp, mock_bind_tcp):
        self.service.start()

        mock_bind_udp.assert_called_with('0.0.0.0', 5354)
        mock_bind_tcp.assert_called_with(
            '0.0.0.0', 5354, CONF['service:mdns'].tcp_backlog
        )

    def test_service_stop(self):
        mock_sock_tcp = mock.Mock()
        mock_sock_udp = mock.Mock()

        self.service._dns_socks_tcp = [mock_sock_tcp]
        self.service._dns_socks_udp = [mock_sock_udp]

        self.service.stop()

        mock_sock_tcp.close.assert_called_once()
        mock_sock_udp.close.assert_called_once()

    def test_handle_tcp(self):
        self.service._running.is_set.side_effect = [True, True, False]

        mock_client = mock.Mock()
        addr = ('192.0.2.1', 5353, '127.0.0.1', 5353)

        mock_sock_tcp = mock.Mock()
        mock_sock_tcp.accept.return_value = (mock_client, addr)

        self.assertIsNone(self.service._dns_handle_tcp(mock_sock_tcp))

        mock_sock_tcp.accept.assert_called()
        mock_client.settimeout.assert_called()

    def test_handle_tcp_handle_errors(self):
        self.service._running.is_set.side_effect = [True, True, True, False]

        mock_sock_tcp = mock.Mock()
        mock_sock_tcp.accept.side_effect = [
            socket.timeout(), socket.error(errno.EACCES), Exception()
        ]

        self.assertIsNone(self.service._dns_handle_tcp(mock_sock_tcp))

        mock_sock_tcp.accept.assert_called()

    def test_handle_tcp_without_timeout(self):
        CONF.set_override('tcp_recv_timeout', 0, 'service:mdns')

        self.service = designate_service.DNSService(
            self.application, self.tg,
            CONF['service:mdns'].listen,
            CONF['service:mdns'].tcp_backlog,
            CONF['service:mdns'].tcp_recv_timeout,
        )
        self.service._running = mock.Mock()
        self.service._running.is_set.side_effect = [True, True, False]

        mock_client = mock.Mock()
        addr = ('192.0.2.1', 5353)

        mock_sock_tcp = mock.Mock()
        mock_sock_tcp.accept.return_value = (mock_client, addr)

        self.assertIsNone(self.service._dns_handle_tcp(mock_sock_tcp))

        mock_sock_tcp.accept.assert_called()
        mock_client.settimeout.assert_not_called()

    def test_handle_tcp_running_not_set(self):
        mock_sock_tcp = mock.Mock()
        self.service._running.is_set.side_effect = [False]
        self.assertIsNone(self.service._dns_handle_tcp(mock_sock_tcp))

    def test_handle_udp(self):
        self.service._running.is_set.side_effect = [True, True, False]

        mock_client = mock.Mock()
        addr = ('192.0.2.1', 5353)

        mock_sock_udp = mock.Mock()
        mock_sock_udp.recvfrom.return_value = (mock_client, addr)

        self.assertIsNone(self.service._dns_handle_udp(mock_sock_udp))

        mock_sock_udp.recvfrom.assert_called()

    def test_handle_udp_handle_errors(self):
        self.service._running.is_set.side_effect = [True, True, True, False]

        mock_sock_tcp = mock.Mock()
        mock_sock_tcp.recvfrom.side_effect = [
            socket.timeout(), socket.error(errno.EACCES), Exception()
        ]

        self.assertIsNone(self.service._dns_handle_udp(mock_sock_tcp))

        mock_sock_tcp.recvfrom.assert_called()
