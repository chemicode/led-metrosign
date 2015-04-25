#!/usr/bin/perl -w
#This program is supposed to take input from other programs and files
#and sends them to the led sign via it's api.  
#Refreshing the sign is done through cron, and shell scripting
#Data is taken from STDIN...this is my first perl program...
#The trick is this requires both the Device::MiniLED 
#and Device::SerialPort Libraries. And must point to the correct dir's
#Created December 2014
#Author Brian Thomson

use strict;
use warnings;
use lib '/home/pi/lib/Device-MiniLED-1.03/lib/';
use lib '/home/pi/perl5/lib/perl5/arm-linux-gnueabihf-thread-multi-64int/';
use Device::MiniLED;
my $sign=Device::MiniLED->new(devicetype => "sign");
while (<STDIN>)
{
my $text=$_;
chomp($text);
#print "$text\n";
$sign->addMsg(
	data => $text,
	effect => "hold",
	speed => 3
	);
}
$sign->send(device => "/dev/ttyUSB0");
