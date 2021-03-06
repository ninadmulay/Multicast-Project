#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, setLogLevel, info
from mininet.cli import CLI
from mininet.node import Node
from mininet.link import Link, TCLink 
from mininet.util import dumpNodeConnections
import threading
import sys, time

import cleanup
from printer import *
from packet import *
#from topoFinal import topoFinal

"""
def startServer():
    (net.hosts[0]).cmd('python /home/mininet/comnet2_2020/comnetsii_package/udpServer.py &')
    (net.hosts[1]).cmd('python /home/mininet/comnet2_2020/comnetsii_package/udpServerHost.py &')
    (net.hosts[2]).cmd('python /home/mininet/comnet2_2020/comnetsii_package/udpServerHost.py &')
"""

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class topoFinal( Topo ):
    #Custom topology Example 1
    #Create a Mininet Environment
    def build( self, **_opts ):

	info( "*** Creating Routers\n" )
	
	routers = [ self.addNode( 'r%d' % n, cls=LinuxRouter, 
				  ip='192.168.1.%d/24' % n ) 
				  for n in range(201,208) ]

	info( "*** Creating Router Links\n" )
	self.addLink( routers[routers.index('r201')], routers[routers.index('r202')],
		intfName1='r201-eth0' )
	self.addLink( routers[routers.index('r201')], routers[routers.index('r203')],
		intfName1='r201-eth1' )
	self.addLink( routers[routers.index('r201')], routers[routers.index('r204')],
		intfName1='r201-eth2' )
	self.addLink( routers[routers.index('r202')], routers[routers.index('r205')],
		intfName1='r202-eth1' )
	self.addLink( routers[routers.index('r203')], routers[routers.index('r206')],
		intfName1='r203-eth1' )
	self.addLink( routers[routers.index('r204')], routers[routers.index('r207')],
		intfName1='r204-eth1' )
	self.addLink( routers[routers.index('r205')], routers[routers.index('r206')],
		intfName1='r205-eth1' )
	self.addLink( routers[routers.index('r206')], routers[routers.index('r207')],
		intfName1='r206-eth2' )

	info( "*** Creating Hosts\n" )
	hosts = [ self.addHost( 'h%d' % n, 
				ip='192.168.1.%d/24' % n )
				for n in range(101,105) ]

	info( "*** Creating Host Links\n" )
	self.addLink( hosts[hosts.index('h101')], routers[routers.index('r201')],
		intfName1='h101-eth0' )    
	self.addLink( hosts[hosts.index('h102')], routers[routers.index('r205')],
		intfName1='h102-eth0' )
	self.addLink( hosts[hosts.index('h103')], routers[routers.index('r206')],
		intfName1='h103-eth0' )
	self.addLink( hosts[hosts.index('h104')], routers[routers.index('r207')],
		intfName1='h104-eth0' )
    
def run():
    
    #Setup topo and list information
    topo = topoFinal()
    net = Mininet( topo=topo, controller=None, link=TCLink )
    net.start()

    info( "*** Setup routes on all devices" )
    #Host routes
    net['h101'].cmd( 'route add -net 192.168.1.0/24 gw {}'.format(net['r201'].IP()) ) 
    net['h102'].cmd( 'route add -net 192.168.1.0/24 gw {}'.format(net['r205'].IP()) ) 
    net['h103'].cmd( 'route add -net 192.168.1.0/24 gw {}'.format(net['r206'].IP()) ) 
    net['h104'].cmd( 'route add -net 192.168.1.0/24 gw {}'.format(net['r207'].IP()) ) 
   
    #Router r201 routes
    net['r201'].cmd( 'ip route add {}/32 dev r201-eth0'.format(net['r202'].IP()) )
    net['r201'].cmd( 'ip route add {}/32 dev r201-eth1'.format(net['r203'].IP()) )
    net['r201'].cmd( 'ip route add {}/32 dev r201-eth2'.format(net['r204'].IP()) )
    net['r201'].cmd( 'ip route add {}/32 dev r201-eth3'.format(net['h101'].IP()) )

    #Router r202 routes
    net['r202'].cmd( 'ip route add {}/32 dev r202-eth0'.format(net['r201'].IP()) )
    net['r202'].cmd( 'ip route add {}/32 dev r202-eth1'.format(net['r205'].IP()) )

    #Router r203 routes
    net['r203'].cmd( 'ip route add {}/32 dev r203-eth0'.format(net['r201'].IP()) )
    net['r203'].cmd( 'ip route add {}/32 dev r203-eth1'.format(net['r206'].IP()) )

    #Router r204 routes
    net['r204'].cmd( 'ip route add {}/32 dev r204-eth0'.format(net['r201'].IP()) )
    net['r204'].cmd( 'ip route add {}/32 dev r204-eth1'.format(net['r207'].IP()) )
    
    #Router r205 routes
    net['r205'].cmd( 'ip route add {}/32 dev r205-eth0'.format(net['r202'].IP()) )
    net['r205'].cmd( 'ip route add {}/32 dev r205-eth1'.format(net['r206'].IP()) )
    net['r205'].cmd( 'ip route add {}/32 dev r205-eth2'.format(net['h102'].IP()) ) 
    
    #Router r206 routes
    net['r206'].cmd( 'ip route add {}/32 dev r206-eth0'.format(net['r203'].IP()) )
    net['r206'].cmd( 'ip route add {}/32 dev r206-eth1'.format(net['r205'].IP()) )
    net['r206'].cmd( 'ip route add {}/32 dev r206-eth2'.format(net['r207'].IP()) )
    net['r206'].cmd( 'ip route add {}/32 dev r206-eth3'.format(net['h103'].IP()) )
    
    #Router r206 routes
    net['r207'].cmd( 'ip route add {}/32 dev r207-eth0'.format(net['r204'].IP()) )
    net['r207'].cmd( 'ip route add {}/32 dev r207-eth1'.format(net['r206'].IP()) )
    net['r207'].cmd( 'ip route add {}/32 dev r207-eth2'.format(net['h104'].IP()) )
    
    #DEBUGGING INFO    
    info( "\n\n" )
    info( "*** List host IPs\n" )
    get_host_ips(net)
    info( "*** List all routes\n" )
    for node in net.hosts:
	print(node.cmd('route -n'))
    info( "*** Dumping host connections\n" )
    dumpNodeConnections(net.hosts)
    info( "*** Pinging all devices\n" )
    #net.pingAll()
    
    CLI( net )
    net.stop()

if __name__ == '__main__':
    cleanup.cleanup()
    setLogLevel( 'info' )  # for CLI output
    run()

    """
    net[ 'r201' ].cmd( 'ip route add 192.168.1.2/32 dev r1-eth2' )
    net[ 'r201' ].cmd( 'ip route add 192.168.1.11/32 dev r1-eth0' )
    net[ 'r201' ].cmd( 'route add -net 192.168.1.0/24 gw 192.168.1.11' )
    
    net[ 'r202' ].cmd( 'ip route add 192.168.1.3/32 dev r2-eth1' )
    net[ 'r202' ].cmd( 'ip route add 192.168.1.10/32 dev r2-eth0' )
    net[ 'r202' ].cmd( 'route add -net 192.168.1.0/24 gw 192.168.1.10' )
    """
    
    """
    net[ 'r1' ].cmd( 'ip addr add 192.168.4.1 dev r1-eth1' )
    net[ 'r2' ].cmd( 'ip addr add 192.168.2.2 dev r2-eth2' )
    net[ 'r2' ].cmd( 'ip addr add 192.168.3.2 dev r2-eth3' )
    
    net[ 'r1' ].cmd( 'ip route add 192.168.4.0/24 dev r1-eth1' )
    net[ 'r2' ].cmd( 'ip route add 192.168.2.0/24 dev r2-eth2' )
    net[ 'r2' ].cmd( 'ip route add 192.168.3.0/24 dev r2-eth3' )
    net[ 'r2' ].cmd( 'ip route add 192.168.4.0/24 dev r2-eth1' )
    
    net[ 'r1' ].cmd( 'route add default gw 192.168.4.2 r1-eth1' )
    
    info( '\n\n' )
    info( '*** List host IPs\n' )
    get_host_ips(net)
    info( '*** List host MACs\n' )
    get_host_macs(net)
    #info( '*** List host Interfaces\n' )
    #get_interfaces(net)
    net.pingAll()
    info( "*** Dumping host connections\n" )
    dumpNodeConnections(net.hosts)
    info( "*** List host routes\n")
    for node in net.hosts:
	print(node.cmd('route -n'))
    #info( "*** List host interfaces\n")
    #for node in net.hosts:
	#print(node.cmd('ip a'))



    print(net[ 'r1' ].cmd('python /home/mininet/comnet2_2020/comnetsii_package/udpServerRouter.py'))
    net[ 'r2' ].cmd('python udpServerRouter.py')
    net[ 'h2' ].cmd('python udpServerHost.py')
    sleep(20)
    print(net[ 'h1' ].cmd('python udpClient.py'))



    #Packet Example
    packet = create_packet(1, 101, 102, 1, 'I am a comnetsii packet')
    print(packet)
    pkttype, pktlen, dst, src, seq = read_header(packet)
    print(pkttype, pktlen, dst, src, seq)
    mydata = read_data(packet)
    print(mydata)
    
    #Start servers on nodes
    startServer()

    #5 Ping test
    print(net.hosts[1].cmd('echo hi'))
    #print((net.hosts[1]).cmd('python udpClient.py'))


    CLI( net )
    net.stop()
    """
