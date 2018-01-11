# Vagrant

Preparation scripts for for [xenial-pho](https://app.vagrantup.com/phonetworks/boxes/xenial-pho) Vagrant box.

## Install

Download and install [Vagrant](https://vagrantup.com). Then:

```
vagrant init phonetworks/xenial-pho
vagrant up
```

## Warning

The dpkg and rpm package sources under the [src/](https://github.com/phonetworks/vagrant/tree/master/src) folder have not been checked, and are not guaranteed to work. The Vagrant box is built for, and guaranteed to work with Ubuntu 16.04 only. 

## Cleanup

After every modification, the following should be run to make sure the box is clean:

```shell
sudo apt-get clean
rm ~/.rediscli_history 
rm ~/.neo4j/.neo4j_history 
rm ~/.php_history
sudo dd if=/dev/zero of=/EMPTY bs=1M
sudo rm -f /EMPTY
cat /dev/null > ~/.bash_history && history -c && exit
```

## License

MIT, see [LICENSE](https://github.com/phonetworks/vagrant/blob/master/LICENSE).
