#!/usr/bin/env python3
#
# Copyright (C) 2021 VyOS maintainers and contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or later as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import sys
import unittest

from base_vyostest_shim import VyOSUnitTestSHIM

from vyos.configsession import ConfigSessionError
from vyos.ifconfig import Section
from vyos.util import process_named_running
from vyos.util import cmd

PROCESS_NAME = 'ospfd'
base_path = ['protocols', 'ospf']

route_map = 'foo-bar-baz10'

log = logging.getLogger('TestProtocolsOSPF')

class TestProtocolsOSPF(VyOSUnitTestSHIM.TestCase):
    def setUp(self):
        self.cli_set(['policy', 'route-map', route_map, 'rule', '10', 'action', 'permit'])
        self.cli_set(['policy', 'route-map', route_map, 'rule', '20', 'action', 'permit'])

    def tearDown(self):
        # Check for running process
        self.assertTrue(process_named_running(PROCESS_NAME))
        self.cli_delete(['policy', 'route-map', route_map])
        self.cli_delete(base_path)
        self.cli_commit()

    def test_ospf_01_defaults(self):
        # commit changes
        self.cli_set(base_path)
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f'router ospf', frrconfig)
        self.assertIn(f' auto-cost reference-bandwidth 100', frrconfig)
        self.assertIn(f' timers throttle spf 200 1000 10000', frrconfig) # defaults

    def test_ospf_02_simple(self):
        router_id = '127.0.0.1'
        abr_type = 'ibm'
        bandwidth = '1000'
        metric = '123'

        self.cli_set(base_path + ['auto-cost', 'reference-bandwidth', bandwidth])
        self.cli_set(base_path + ['parameters', 'router-id', router_id])
        self.cli_set(base_path + ['parameters', 'abr-type', abr_type])
        self.cli_set(base_path + ['log-adjacency-changes', 'detail'])
        self.cli_set(base_path + ['default-metric', metric])

        # commit changes
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f'router ospf', frrconfig)
        self.assertIn(f' auto-cost reference-bandwidth {bandwidth}', frrconfig)
        self.assertIn(f' ospf router-id {router_id}', frrconfig)
        self.assertIn(f' ospf abr-type {abr_type}', frrconfig)
        self.assertIn(f' timers throttle spf 200 1000 10000', frrconfig) # defaults
        self.assertIn(f' default-metric {metric}', frrconfig)


    def test_ospf_03_access_list(self):
        acl = '100'
        seq = '10'
        protocols = ['bgp', 'connected', 'isis', 'kernel', 'rip', 'static']

        self.cli_set(['policy', 'access-list', acl, 'rule', seq, 'action', 'permit'])
        self.cli_set(['policy', 'access-list', acl, 'rule', seq, 'source', 'any'])
        self.cli_set(['policy', 'access-list', acl, 'rule', seq, 'destination', 'any'])
        for ptotocol in protocols:
            self.cli_set(base_path + ['access-list', acl, 'export', ptotocol])

        # commit changes
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f'router ospf', frrconfig)
        self.assertIn(f' timers throttle spf 200 1000 10000', frrconfig) # defaults
        for ptotocol in protocols:
            self.assertIn(f' distribute-list {acl} out {ptotocol}', frrconfig) # defaults
        self.cli_delete(['policy', 'access-list', acl])


    def test_ospf_04_default_originate(self):
        seq = '100'
        metric = '50'
        metric_type = '1'

        self.cli_set(base_path + ['default-information', 'originate', 'metric', metric])
        self.cli_set(base_path + ['default-information', 'originate', 'metric-type', metric_type])
        self.cli_set(base_path + ['default-information', 'originate', 'route-map', route_map])

        # commit changes
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f'router ospf', frrconfig)
        self.assertIn(f' timers throttle spf 200 1000 10000', frrconfig) # defaults
        self.assertIn(f' default-information originate metric {metric} metric-type {metric_type} route-map {route_map}', frrconfig)

        # Now set 'always'
        self.cli_set(base_path + ['default-information', 'originate', 'always'])
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f' default-information originate always metric {metric} metric-type {metric_type} route-map {route_map}', frrconfig)


    def test_ospf_05_options(self):
        global_distance = '128'
        intra_area = '100'
        inter_area = '110'
        external = '120'
        on_startup = '30'
        on_shutdown = '60'
        refresh = '50'

        self.cli_set(base_path + ['distance', 'global', global_distance])
        self.cli_set(base_path + ['distance', 'ospf', 'external', external])
        self.cli_set(base_path + ['distance', 'ospf', 'intra-area', intra_area])

        self.cli_set(base_path + ['max-metric', 'router-lsa', 'on-startup', on_startup])
        self.cli_set(base_path + ['max-metric', 'router-lsa', 'on-shutdown', on_shutdown])

        self.cli_set(base_path + ['mpls-te', 'enable'])
        self.cli_set(base_path + ['refresh', 'timers', refresh])

        # commit changes
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f'router ospf', frrconfig)
        self.assertIn(f' mpls-te on', frrconfig)
        self.assertIn(f' mpls-te router-address 0.0.0.0', frrconfig) # default
        self.assertIn(f' distance {global_distance}', frrconfig)
        self.assertIn(f' distance ospf intra-area {intra_area} external {external}', frrconfig)
        self.assertIn(f' max-metric router-lsa on-startup {on_startup}', frrconfig)
        self.assertIn(f' max-metric router-lsa on-shutdown {on_shutdown}', frrconfig)
        self.assertIn(f' refresh timer {refresh}', frrconfig)


        # enable inter-area
        self.cli_set(base_path + ['distance', 'ospf', 'inter-area', inter_area])
        self.cli_commit()

        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f' distance ospf intra-area {intra_area} inter-area {inter_area} external {external}', frrconfig)


    def test_ospf_06_neighbor(self):
        priority = '10'
        poll_interval = '20'
        neighbors = ['1.1.1.1', '2.2.2.2', '3.3.3.3']
        for neighbor in neighbors:
            self.cli_set(base_path + ['neighbor', neighbor, 'priority', priority])
            self.cli_set(base_path + ['neighbor', neighbor, 'poll-interval', poll_interval])

        # commit changes
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f'router ospf', frrconfig)
        for neighbor in neighbors:
            self.assertIn(f' neighbor {neighbor} priority {priority} poll-interval {poll_interval}', frrconfig) # default


    def test_ospf_07_passive_interface(self):
        self.cli_set(base_path + ['passive-interface', 'default'])
        interfaces = Section.interfaces('ethernet')
        for interface in interfaces:
            self.cli_set(base_path + ['passive-interface-exclude', interface])

        # commit changes
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        try:
            self.assertIn(f'router ospf', frrconfig)
            self.assertIn(f' passive-interface default', frrconfig) # default
            for interface in interfaces:
                self.assertIn(f' no passive-interface {interface}', frrconfig) # default
        except:
            log.debug(frrconfig)
            log.debug(cmd('sudo dmesg'))
            log.debug(cmd('sudo cat /var/log/messages'))
            log.debug(cmd('vtysh -c "show run"'))
            self.fail('Now we can hopefully see why OSPF fails!')

    def test_ospf_08_redistribute(self):
        metric = '15'
        metric_type = '1'
        redistribute = ['bgp', 'connected', 'isis', 'kernel', 'rip', 'static']

        for protocol in redistribute:
            self.cli_set(base_path + ['redistribute', protocol, 'metric', metric])
            self.cli_set(base_path + ['redistribute', protocol, 'route-map', route_map])
            self.cli_set(base_path + ['redistribute', protocol, 'metric-type', metric_type])

        # commit changes
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        try:
            self.assertIn(f'router ospf', frrconfig)
            for protocol in redistribute:
                self.assertIn(f' redistribute {protocol} metric {metric} metric-type {metric_type} route-map {route_map}', frrconfig)
        except:
            log.debug(frrconfig)
            log.debug(cmd('sudo dmesg'))
            log.debug(cmd('sudo cat /var/log/messages'))
            log.debug(cmd('vtysh -c "show run"'))
            self.fail('Now we can hopefully see why OSPF fails!')

    def test_ospf_09_virtual_link(self):
        networks = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
        area = '10'
        shortcut = 'enable'
        virtual_link = '192.0.2.1'
        hello = '6'
        retransmit = '5'
        transmit = '5'
        dead = '40'

        self.cli_set(base_path + ['area', area, 'shortcut', shortcut])
        self.cli_set(base_path + ['area', area, 'virtual-link', virtual_link, 'hello-interval', hello])
        self.cli_set(base_path + ['area', area, 'virtual-link', virtual_link, 'retransmit-interval', retransmit])
        self.cli_set(base_path + ['area', area, 'virtual-link', virtual_link, 'transmit-delay', transmit])
        self.cli_set(base_path + ['area', area, 'virtual-link', virtual_link, 'dead-interval', dead])
        for network in networks:
            self.cli_set(base_path + ['area', area, 'network', network])

        # commit changes
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f'router ospf', frrconfig)
        self.assertIn(f' area {area} shortcut {shortcut}', frrconfig)
        self.assertIn(f' area {area} virtual-link {virtual_link} hello-interval {hello} retransmit-interval {retransmit} transmit-delay {transmit} dead-interval {dead}', frrconfig)
        for network in networks:
            self.assertIn(f' network {network} area {area}', frrconfig)


    def test_ospf_10_interface_configuration(self):
        interfaces = Section.interfaces('ethernet')
        password = 'vyos1234'
        bandwidth = '10000'
        cost = '150'
        network = 'point-to-point'
        priority = '200'

        for interface in interfaces:
            self.cli_set(base_path + ['interface', interface, 'authentication', 'plaintext-password', password])
            self.cli_set(base_path + ['interface', interface, 'bandwidth', bandwidth])
            self.cli_set(base_path + ['interface', interface, 'bfd'])
            self.cli_set(base_path + ['interface', interface, 'cost', cost])
            self.cli_set(base_path + ['interface', interface, 'mtu-ignore'])
            self.cli_set(base_path + ['interface', interface, 'network', network])
            self.cli_set(base_path + ['interface', interface, 'priority', priority])

        # commit changes
        self.cli_commit()

        for interface in interfaces:
            config = self.getFRRconfig(f'interface {interface}')
            self.assertIn(f'interface {interface}', config)
            self.assertIn(f' ip ospf authentication-key {password}', config)
            self.assertIn(f' ip ospf bfd', config)
            self.assertIn(f' ip ospf cost {cost}', config)
            self.assertIn(f' ip ospf mtu-ignore', config)
            self.assertIn(f' ip ospf network {network}', config)
            self.assertIn(f' ip ospf priority {priority}', config)
            self.assertIn(f' bandwidth {bandwidth}', config)


    def test_ospf_11_vrfs(self):
        # It is safe to assume that when the basic VRF test works, all
        # other OSPF related features work, as we entirely inherit the CLI
        # templates and Jinja2 FRR template.
        table = '1000'
        vrf = 'blue'
        vrf_base = ['vrf', 'name', vrf]
        vrf_iface = 'eth1'
        self.cli_set(vrf_base + ['table', table])
        self.cli_set(vrf_base + ['protocols', 'ospf', 'interface', vrf_iface])
        self.cli_set(['interfaces', 'ethernet', vrf_iface, 'vrf', vrf])

        # Also set a default VRF OSPF config
        self.cli_set(base_path)
        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f'router ospf', frrconfig)
        self.assertIn(f' auto-cost reference-bandwidth 100', frrconfig)
        self.assertIn(f' timers throttle spf 200 1000 10000', frrconfig) # defaults

        frrconfig = self.getFRRconfig(f'router ospf vrf {vrf}')
        self.assertIn(f'router ospf vrf {vrf}', frrconfig)
        self.assertIn(f' auto-cost reference-bandwidth 100', frrconfig)
        self.assertIn(f' timers throttle spf 200 1000 10000', frrconfig) # defaults

        self.cli_delete(['vrf', 'name', vrf])
        self.cli_delete(['interfaces', 'ethernet', vrf_iface, 'vrf'])


    def test_ospf_12_zebra_route_map(self):
        # Implemented because of T3328
        self.cli_set(base_path + ['route-map', route_map])
        # commit changes
        self.cli_commit()

        # Verify FRR configuration
        zebra_route_map = f'ip protocol ospf route-map {route_map}'
        frrconfig = self.getFRRconfig(zebra_route_map)
        self.assertIn(zebra_route_map, frrconfig)

        # Remove the route-map again
        self.cli_delete(base_path + ['route-map'])
        # commit changes
        self.cli_commit()

        # Verify FRR configuration
        frrconfig = self.getFRRconfig(zebra_route_map)
        self.assertNotIn(zebra_route_map, frrconfig)

    def test_ospf_13_interface_area(self):
        area = '0'
        interfaces = Section.interfaces('ethernet')

        self.cli_set(base_path + ['area', area, 'network', '10.0.0.0/8'])
        for interface in interfaces:
            self.cli_set(base_path + ['interface', interface, 'area', area])

        # we can not have bot area network and interface area set
        with self.assertRaises(ConfigSessionError):
            self.cli_commit()
        self.cli_delete(base_path + ['area', area, 'network'])

        self.cli_commit()

        # Verify FRR ospfd configuration
        frrconfig = self.getFRRconfig('router ospf')
        self.assertIn(f'router ospf', frrconfig)

        for interface in interfaces:
            config = self.getFRRconfig(f'interface {interface}')
            self.assertIn(f'interface {interface}', config)
            self.assertIn(f' ip ospf area {area}', config)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main(verbosity=2)
