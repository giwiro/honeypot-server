# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANT_API_VERSION = "2"

Vagrant.configure(VAGRANT_API_VERSION) do |config|
    config.vm.define "honeypot", primary: true do |machine|
        config.vm.box = "centos/7"
        config.vm.hostname = "honeypot.box"
        config.vm.network "public_network", ip: "192.168.2.100"
        # config.vm.network "forwarded_port", guest: 443, host: 443
        # config.vm.network "forwarded_port", guest: 8080, host: 8080
        config.ssh.forward_agent = true

        config.vm.provider :virtualbox do |v|
            v.memory = 1024
            v.cpus = 2
            v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
            v.customize ["modifyvm", :id, "--ioapic", "on"]
        end

        # We do it manually
        #
        # config.vm.provision "ansible" do |ansible|
        #    ansible.playbook = "provisioning/playbook.yml"
        #    ansible.inventory_path = "provisioning/hosts"
        #    ansible.become = true
        # end
    end
end

