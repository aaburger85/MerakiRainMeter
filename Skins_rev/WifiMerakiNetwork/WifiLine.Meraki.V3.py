import subprocess
import json
import urllib.request
from subprocess import Popen, PIPE
wifioutput = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('UTF-8').splitlines()
wificonnected = '    Network type           : Infrastructure'

status= ('lightgreen','yellow','red')
props = ('Signal','Radio','BSSID:','SSID:','Transmit', 'Receive','Channel')
networkArr = ('IP', 'Subnet', 'Default')
data = []
ndata = []

def format_data(line):
	for prop in props: 
		if (prop in str(line)):
			signal = line,
			tuplesignal = [tuple(i.split(': ')) for i in signal]
			signaldict = dict((x, y) for x, y in tuplesignal)
			signaldict = {k.strip():  v for k,v in signaldict.items()}
			# print(signaldict) # for debug use to see values with there prop
			return signaldict[prop.replace(":","")]

if wificonnected in wifioutput:
	for line in wifioutput:
		pLine = format_data(line)
		if pLine is not None:
			data.append(pLine)
		else: 
			pass
		
		print ("Quality:", data[0], "|", "Band:", data[1], "|", "SSID:", data[3], "|", "BSSID:", data[2], "|", "Tx/Rx Rate:", data[4], "/", data[5], "Mbps", "|", "Channel:", data[6])
else:
	print("Disconnected")

def network_func(line):
	for n in networkArr:
		if n in str(line):
			tupleIP = [tuple(i.split(': ')) for i in line]
			ipdict = dict((x, y) for x, y in tupleIP)
			ipdict = {k.strip(): v for k,v in ipdict.items()}
			# print(ipdict) # for debug use to see values with there prop
			return ipdict[n.replace(":", "")]


ipoutput = subprocess.check_output(['netsh', 'interface', 'ipv4', 'show', 'addresses', 'name=Wi-Fi']).decode('UTF-8').splitlines()
dhcpconnected = '    DHCP enabled:                         Yes'

if wificonnected in wifioutput:
	if dhcpconnected in ipoutput:
		for line in ipoutput:
			nLine = network_func(line)
			if nLine is not None:
				ndata.append(nLine.lstrip(' '))
			else:
				pass
		print("IP Address:", ndata[0], "|", "Subnet:", ndata[1], "|", "Gateway:", ndata[2])
	else:
		print("Static or Disconnected")
else:
	print("No IP Address")

########################## Meraki AP Detection and Info #######################################################
try:  
		apresp = urllib.request.urlopen('http://ap.meraki.com/index.json').read()
		merakiapjson = json.loads(apresp)
		if 'error' not in merakiapjson:
				SignaldB = merakiapjson['client']['rssi']
				MerakiNetwork = merakiapjson['config']['network_name']
				MerakiAP = merakiapjson['config']['node_name']
				MerakiModel = merakiapjson['config']['product_model']
				MerakiAPIP = merakiapjson['connection_state']['wired_ip']
				print ("SNR at AP:", SignaldB,"dB","|","AP Name:", MerakiAP,"|","AP IP:", MerakiAPIP, "|", "AP Model:", MerakiModel, "|", "Meraki Network:", MerakiNetwork)
		else:
				print("Not Connected to an MR")
except:
		print ("Not Connected to an MR")
################################ Meraki Switch Detection and Info ###################################################
try:
		switchresp = urllib.request.urlopen('http://switch.meraki.com/index.json').read()
		merakiswitchjson = json.loads(switchresp)
		if 'error' not in merakiswitchjson:
				SwitchName = merakiswitchjson['config']['node_name']
				SwitchModel = merakiswitchjson['config']['product_model']
				SwitchIP = merakiswitchjson['connection_state']['wired_ip']
				SwitchVLAN = merakiswitchjson['client']['vlan']
				SwitchPort = merakiswitchjson['client']['port']
				print("Port:", SwitchPort, "|", "VLAN:", SwitchVLAN, "|", "Switch Name:", SwitchName, "|", "Switch IP:", SwitchIP, "|", "Switch Model:", SwitchModel)
		else:
				print("Not Connected to an MS")
except:
		print ("Not Connected to an MS")
############################# Meraki Firewall Detection and Info ################################################################
try:
		firewallresp = urllib.request.urlopen('http://wired.meraki.com/index.json').read()
		merakifirewalljson = json.loads(firewallresp)
		if 'error' not in merakifirewalljson:
				FirewallName = merakifirewalljson['config']['node_name']
				FirewallModel = merakifirewalljson['config']['product_model']
				FirewallIP = merakifirewalljson['connection_state']['wired_ip']
				print("Firewall Name:", FirewallName, "|", "Firewall IP:", FirewallIP, "|", "Model:", FirewallModel)
		else:
				print("Not Connected to an MX")
except:
		print ("Not Connected to an MX")
