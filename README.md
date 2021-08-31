Proxy specific ports from virtualbox instance on Ubuntu host.

- Create hostonly virtualbox network adapter
```
vboxmanage list hostonlyifs
vboxmanage hostonlyif create
vboxmanage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0
vboxmanage list dhcpservers
```
- Remove DHCP servers if listed
```
vboxmanage dhcpserver modify --netname HostInterfaceNetworking-vboxnet0 --disable
```
- Assign hostonly network if to VBox instance
- On the host install dnsmasq and start DHCP only server
```
sudo apt install dnsmasq
# Add the following to /etc/dnsmasq.conf
### CUT ###
domain-needed
bogus-priv
no-poll

interface=vboxnet0

dhcp-range=192.168.56.101,192.168.56.200,96h
dhcp-option=option:router,192.168.56.1
dhcp-option=option:dns-server,192.168.56.1
### CUT ###
sudo dnsmasq -d -z -i vboxnet0
```
- Guest VM is now on a private NAT
- We need to setup routing to connect guest VM to internet
- First we enable packet forwarding
```
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv4.conf.all.send_redirects=0
```
- Now we enable routing rules to connect NAT to internet or our proxy
```
# List current NAT setup
sudo iptables -t nat -L
# Flush current chains
sudo iptables -t nat -F
# Setup default to route out our internet facing interface
sudo iptables -t nat -A POSTROUTING -o enxd03745bfb213 -j MASQUERADE
# Intercept the ports of interest to pass to our MITM proxy
sudo iptables -t nat -A PREROUTING -i vboxnet0 -p tcp --dport 11110 -j REDIRECT --to-port 8080
# List current NAT setup
sudo iptables -t nat -L
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         
REDIRECT   tcp  --  anywhere             anywhere             tcp dpt:11110 redir ports 8080

Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
MASQUERADE  all  --  anywhere             anywhere
```
- Verify the guest VM is getting a valid IP address in the 192.168.56.xxx range
- If not something is wrong. Check dnsmasq output.
- Verify the guest VM can access the internet (redirected port will not work yet).
- Start proxy server
- I used this poor mans proxy as my service in question was using ADH without certs. For HTTPS you'd be better suited by mitmproxy or sslsplit.
```
# Terminal 1
mkfifo request response
openssl s_server -cipher 'ADH-AES128-SHA:@SECLEVEL=0' -accept *:8080 -nocert -quiet < response | tee -a request | xxd

# Terminal 2 (same dir)
openssl s_client -tls1 -cipher 'ADH-AES128-SHA:@SECLEVEL=0' -connect 192.168.1.17:11110 -noservername -quiet < request | tee -a response | xxd
```
