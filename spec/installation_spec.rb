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
    end
end

