"""
Role tests
"""

import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize('name', [
    ('ferm'),
    ('iptables'),
])
def test_packages(host, name):
    """
    Test packages installed
    """

    assert host.package(name).is_installed


@pytest.mark.parametrize('item_type,path,user,group,mode', [
    ('file', '/etc/ferm/ferm.conf', 'root', 'root', 0o400),
])
def test_files_and_folders(host, item_type, path, user, group, mode):
    """
    Test files and folders properties
    """

    current_item = host.file(path)

    if item_type == 'directry':
        assert current_item.is_directory
    elif item_type == 'file':
        assert current_item.is_file

    assert current_item.user == user
    assert current_item.group == group
    assert current_item.mode == mode


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
