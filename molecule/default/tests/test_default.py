import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_installed_packages(host):
    assert host.package('nginx').is_installed


def test_running_services(host):
    svc = host.service('nginx')
    assert svc.is_running
    assert svc.is_enabled


# expected ports listening
# note testing port binding, not firewall/network security group rules
def test_port_bindings(host):
    assert host.socket('tcp://0.0.0.0:80').is_listening
