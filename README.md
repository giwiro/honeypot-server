# honeypot-server
```
 _                                        _   
| |                                      | |  
| |__   ___  _ __   ___ _   _ _ __   ___ | |_             __         .' '.
| '_ \ / _ \| '_ \ / _ \ | | | '_ \ / _ \| __|          _/__)        .   .       .
| | | | (_) | | | |  __/ |_| | |_) | (_) | |_          (8|)_}}- .      .        .
|_| |_|\___/|_| |_|\___|\__, | .__/ \___/ \__|          `\__)    '. . ' ' .  . '
                         __/ | |              
                        |___/|_|              
```
Ansible project to set up cowie, a ssh honeypot, and extract auth tries and established session information.

## Interest Files


## Deploy in real server

In order to deploy this project in a real server, there are some requirements you need to take care:
- Server's operating system: CentOS 7
- Have ansible-playbook installed
- Allow root ssh login in the server (It should be the default behaviour)

### 1. Create a file named `production` where you put the ip and port, this file should look alike the local file at the root of the project

```yaml
# file: production
[honeypot]
192.168.1.69 ansible_ssh_port=22
```

NOTE: The cowrie mysql password is hardcoded on `group_vars` folder inside `honeypot.yml` file. Feel free to change the password, but
I think it won't represent any actual thread since the mysql service is not listening on any public ip and it can only be accessed when
you are already in the server.

```yaml
...
# Cowrie
cowrie_user: cowrie

cowrie_mysql_name: cowrie
cowrie_mysql_user: cowrie
cowrie_mysql_password: wGEw?%44mTm.>6KW  # <---- This line
...
```

### 2. Proceed to run the playbook. It will ask you for the root password.

```console
$ ansible-playbook -u root -i production site.yml --ask-pass
```

### 3. Create a user (apart from `root` and `cowrie`) to manage the access to the server and give sudo permissions
Just replace `<username>` by the actual username you want to use

```console
$ adduser <username>
$ passwd <username>
$ usermod -aG wheel <username>
```

### 4. Remove root ssh login access

In this file `/etc/ssh/sshd_config` you will find this:
```
...
#PermitRootLogin yes
...
```

Please change it to this:
```
...
PermitRootLogin no
...
```

