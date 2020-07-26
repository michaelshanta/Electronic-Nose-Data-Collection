# Electronic-Nose-Data-Collection
Instructions to setup the data collection server using MQTT.


# Initial Server Setup
DigitalOcean was used to create the server as they offer $50 free credit for students.
Configuration:  `1 GB Memory / 25 GB Disk / LON1 - Ubuntu 18.04.3 (LTS) x64`

### Root Login
To log into your server, you will need to know your server’s public IP address. You will also need the password or, if you installed an SSH key for authentication, the private key for the “root” user’s account. The IP address for this project is 167.172.48.6.
```
ssh root@your_server_ip
```


### Create new User
Once you are logged in as root, we’re prepared to add the new user account that we will use to log in from now on.
```
adduser Michael
```

### Add Privileges 
Add the new user account to the sudo group (so they can use the sudo command to perform administrative tasks).
```
usermod -aG sudo Michael
```
Now your user can run commands with superuser privileges! 

### Login as the new user
Before you logout of the root account, open a new terminal and make sure you can SSH in using the new account.
```
ssh Michael@your_server_ip
```
Then logout!

### Setup a Firewall
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

MQTT provides lightweight publish/subscribe communication to “Internet of Things” (IoT) devices such as our Cyber Sniffer.
Mosquitto is a popular MQTT server (or broker, in MQTT parlance) that has great community support and is easy to install and configure.

**You will need a Domain name pointed at your server!** Throughout the dissertation period I have used www.enose.ml. As of July 2020, this domain name is no longer available as it has been purchased by someone else. 
I will be using www.enose.ga instead. I've found www.freenom.com to be a good source for free domain names.
Follow this guide to setup Domain names on DigitalOcean: https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars

Test you have setup your Domain name correctly by SSHing to it instead of using the IP address, for example:
```
ssh michael@enose.ga
```

## Install MOSQUITTO
Login as the sudo user and use apt-get to install mosquitto:
```
sudo apt-get install mosquitto mosquitto-clients
```

### Test Mosquitto Installation
The MQTT protocol uses topics. To test we have installed this correctly, open a new terminal, login and subscribe to a topic, "test".
```
mosquitto_sub -h localhost -t test
```
-h is used to specify the hostname of the MQTT server, and -t is the topic name. You’ll see no output after hitting ENTER because mosquitto_sub is waiting for messages to arrive. Switch back to the other terminal and publish a message:
```
mosquitto_pub -h localhost -t test -m "hello I am the cyber sniffer"
```

You should see the messaege `"hello I am the cyber sniffer"` in the subscribed terminal. Stop subscribing by pressing CTRL+C.

### Configure Mosquitto
**For development and testing purposes, we will not be securing the server with SSL. The prefered way to do this would be with LetsEncrypt as they offer free certificates**

To prevent other devious members of the Engineering School from sabotaging the project, lets protect MQTT requests with passwords.
This command will prompt you to enter a password for the specified username, and place the results in /etc/mosquitto/passwd.
```
sudo mosquitto_passwd -c /etc/mosquitto/passwd michael
```

Create a configuration file with:
```
sudo nano /etc/mosquitto/conf.d/default.conf
```
The file should be empty when opened with `nano`.
Paste the follwing:
```
allow_anonymous false
password_file /etc/mosquitto/passwd
```
This forces a username and a password to be used when conneting to the broker.

Apply the changes by restarting mosquitto:
```
sudo systemctl restart mosquitto
```
You can test this works using the mosquitto_pub command with the -u and -P flags.

Add the following to the default.conf file using `sudo nano /etc/mosquitto/conf.d/default.conf`:
```
...
listener 1883 localhost

listener 1884
protocol mqtt

listener 8083
protocol websockets
```

Here we added 3 listener blocks. 
The first, listener 1883 localhost, updates the default MQTT listener on port 1883,the standard unencrypted MQTT port. The localhost portion of the line instructs Mosquitto to only bind this port to the localhost interface, so it’s not accessible externally. External requests would have been blocked by our firewall anyway, but it’s good to be explicit.
We then open choose 1884 as this is what I have configured the enose to use.
8083 is for websockets which helps with debugging when using tools such as Paho Client (https://www.eclipse.org/paho/clients/js/utility/).

Apply and restart:
```
sudo systemctl restart mosquitto
```

Open the added ports:
```
sudo ufw allow 1884
sudo ufw allow 8083
```

You can test these work by using a websocket client such as Paho to connect over 8083.
MQTTLens (https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm/related?hl=en) a Google Chrome extension is great for testing MQTT connections. 














