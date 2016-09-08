require 'serverspec'

if ENV['TRAVIS']
    set :backend, :exec
end

describe 'ferm Ansible role' do

if ['debian', 'ubuntu'].include?(os[:family])
    describe 'Specific Debian and Ubuntu family checks' do

        it 'install role packages' do
            packages = Array[ 'ferm', 'iptables' ]

                packages.each do |pkg_name|
                    expect(package(pkg_name)).to be_installed
                end
            end

        end

        describe file('/etc/ferm/ferm.conf') do
            it { should exist }
            it { should be_file }
            it { should be_mode 400 }
            it { should be_owned_by 'root' }
            it { should be_grouped_into'root' }
        end
    end
end

describe iptables do
  it { should have_rule('-P INPUT ACCEPT') }
  it { should have_rule('-P FORWARD DROP') }
  it { should have_rule('-P OUTPUT ACCEPT') }
  it { should have_rule('-A INPUT -m state --state INVALID -j DROP') }
  it { should have_rule('-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT') }
  it { should have_rule('-A INPUT -i lo -j ACCEPT') }
  it { should have_rule('-A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT') }
  it { should have_rule('-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT') }
  it { should have_rule('-A INPUT -j DROP') }
end
