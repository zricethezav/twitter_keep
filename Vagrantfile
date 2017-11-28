# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  

  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |vb|
    vb.cpus = 4
    vb.memory = "4096"
    vb.linked_clone = true
    vb.name = "twitter_keep"
  end

  projects_root_dir = File.join("/opt", "twitter_keep")

  config.vm.provision "shell", name: "Update-Package-List", inline: <<-SHELL
    apt-get update
  SHELL

  config.vm.provision "shell", name: "Installing PostgreSQL with PostGIS", path: "vagrant-tools/install_postgres.sh"

  config.vm.provision "shell", name: "Updating VM's profile", inline: <<-SHELL
    source_line="source /home/vagrant/twitter_keep/vagrant-tools/shell-include.sh"
    echo ${source_line}
    grep -q "^${source_line}" /home/vagrant/.bashrc || \
        echo "${source_line}" >> /home/vagrant/.bashrc
  SHELL

  config.vm.provision "shell", name: "Setting up Env", path: "vagrant-tools/setup_env.sh"

  config.vm.provision "shell", name: "Project-Setup", inline: <<-SHELL
    mkdir -p #{projects_root_dir}
    if [ ! -L /home/vagrant/twitter_keep ]; then
        ln -s #{projects_root_dir} /home/vagrant
    fi 
    chown -R vagrant: #{projects_root_dir}

  SHELL


  if File.directory?(File.absolute_path('../twitter_keep'))
    config.vm.synced_folder File.absolute_path('../twitter_keep'), projects_root_dir
  end


end
