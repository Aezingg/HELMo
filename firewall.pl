#!/usr/bin/perl

use strict;
my $IPTABLES="/usr/sbin/iptables";
my $INTERNAL_NETWORK="192.168.144.0/22";
my $DEVICE_NETWORK="enp036";
my $PORTS_TCP="21,22,50000:50500";
my $PORTS_UDP="53";

### Reset all rules ###
`$IPTABLES -F`;
`$IPTABLES -X`;
`$IPTABLES –t nat –F`;


### INPUT ### 

`$IPTABLES -A INPUT -i lo -j ACCEPT`;
`$IPTABLES -A INPUT -i $DEVICE_NETWORK -s $INTERNAL_NETWORK -p icmp -j
ACCEPT`;
`$IPTABLES -A INPUT -i $DEVICE_NETWORK -p tcp -m state --state NEW -m
multiport --dports $PORTS_TCP -j ACCEPT`;
`$IPTABLES -A INPUT -i $DEVICE_NETWORK -p udp -m multiport --dports
$PORTS_UDP -j ACCEPT`;
`$IPTABLES -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT`;
`$IPTABLES -A INPUT -j LOG`;
`$IPTABLES -P INPUT DROP`;

### FORWARD ### 

`$IPTABLES -P FORWARD DROP`;

### OUTPUT ###

`$IPTABLES -P OUTPUT ACCEPT`;