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
