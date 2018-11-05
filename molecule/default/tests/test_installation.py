"""
Role tests
"""

import os
import pytest

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('name', [
    ('ferm'),
    ('iptables'),
])
def test_packages(host, name):
    """
    Test packages installed
    """

    assert host.package(name).is_installed


def test_files_and_folders(host):
    """
    Test files and folders properties
    """

    config_folder = '/etc/ferm'

    if host.system_info.distribution == 'centos':
        config_folder = '/etc'

    config_file = host.file('{}/ferm.conf'.format(config_folder))

    assert config_file.is_file
    assert config_file.user == 'root'
    assert config_file.group == 'root'
    assert config_file.mode == 0o400


def test_firewall_rules(host):
    """
    Test firewall rules
    """

    expected_rules = [
        '-P INPUT DROP',
        '-P FORWARD DROP',
        '-P OUTPUT ACCEPT',
        '-A INPUT -m state --state INVALID -j DROP',
        '-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT',
        '-A INPUT -i lo -j ACCEPT',
        '-A INPUT -p icmp -j ACCEPT',
        '-A INPUT -p udp -m udp --dport 500 -j ACCEPT',
        '-A INPUT -p esp -j ACCEPT',
        '-A INPUT -p ah -j ACCEPT',
        '-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT',
        '-A FORWARD -m state --state INVALID -j DROP',
        '-A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT',
        '-A OUTPUT -m state --state INVALID -j DROP',
        '-A OUTPUT -m state --state RELATED,ESTABLISHED -j ACCEPT',
    ]

    assert host.check_output('iptables -S').split("\n") == expected_rules
