# Electronic-Nose-Data-Collection
Instructions to setup the data collection server using MQTT.


# Initial Server Setup
DigitalOcean was used to create the server as they offer $50 free credit for students.
Configuration:  `1 GB Memory / 25 GB Disk / LON1 - Ubuntu 18.04.3 (LTS) x64`

## Root Login
To log into your server, you will need to know your server’s public IP address. You will also need the password or, if you installed an SSH key for authentication, the private key for the “root” user’s account. The IP address for this project is 167.172.48.6.
```
ssh root@your_server_ip
```


## Create new User
Once you are logged in as root, we’re prepared to add the new user account that we will use to log in from now on.
```
adduser Michael
```

## Add Privileges 
Add the new user account to the sudo group (so they can use the sudo command to perform administrative tasks).
```
usermod -aG sudo Michael
```
Now your user can run commands with superuser privileges! 

## Login as the new user
Before you logout of the root account, open a new terminal and make sure you can SSH in using the new account.
```
ssh Michael@your_server_ip
```
Then logout!

## Setup a Firewall
The UFW Firewall makes sure only connections to certain services are allowed.
We can see which services are allowed to connect by typing
```
sudo ufw app list
```
The output should look something like this:
```
Available applications:
  OpenSSH
```
OpenSSH is the service allowing us to connect to the server.
We need to make sure that the firewall allows SSH connections so that we can log back in next time. We can allow these connections by typing:
```
sudo ufw allow OpenSSH
```
Then enable the firewall:
```
sudo ufw enable
```
You can check the allowed connections with 
```
sudo ufw status
```
The server is now ready to become an MQTT Broker

# Install and Secure the Mosquitto MQTT Messaging Broker






