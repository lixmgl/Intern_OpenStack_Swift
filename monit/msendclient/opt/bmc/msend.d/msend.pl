#!/usr/bin/perl
################################################################################
#                                                                              #
#                                     ,Hb.                                     #
#                                   ,HMMMMb.                                   #
#                                 ,HMMMMMMMMb.                                 #
#                               ,HMMMMMMMMMMMMb.                               #
#                             ,HMMMMMMMMMMMMMMMMb.                             #
#                           ,HMMMMMMMMMMMMMMMMMMMMb.                           #
#                         ,HMMMM|   M|          MMMMb.                         #
#                       ,HMMMMMM|   M|          MMMMMMb.                       #
#                     ,HMMMMMMMM|   MH###   |###MMMMMMMMb.                     #
#                   ,HMMMMMMMMMM|   MMMMM   |MMMMMMMMMMMMMb.                   #
#                 ,HMMMMMMMMMMMM|   MMMMM   |MMMMMMMMMMMMMMMb.                 #
#               ,HMMMMMMMMMMMMMM|   MMMMM   |MMMMMMMMMMMMMMMMMb.               #
#             ,HMMMMMMMMMMMMMMMM|   MMMMM   |MMMMMMMMMMMMMMMMMMMb.             #
#           ,HMMMMMMMMMMMMMMMMMM|   MMMMM   |MMMMMMMMMMMMMMMMMMMMMb.           #
#           `#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMH'            #
#            .ooooooooooooooooooooooooooooooooooooooooooooooooo'               #
#      |MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM        #
#      |MMM|  `MMMMMT   MMMMMMMMMMMMMMMMMMM |MMMMMMMMMMMMMMMMMMMMMMMMMM        #
#      |MMM| . |MMMH .  MMH"""`H?"MM*"""HM" `"MM*'"`"#MMR"*'TM*'"`*MMMM        #
#      |MMM| |? 9MM'.M  M? ,o#o,  M| ,#__Mo ,oH'.odbo `MM  oHT .#boHMMM        #
#      |MMM| |M.`MT dM  T  MMMMM  Mb_ `"*MM |M| `""""' |M |MMM\. ""HMMM        #
#      |MMM| |MH ` |MM  H. *MMM*  M""H#. ]M |ML -q##p--HM |MMP"9M| |MMM        #
#      |MMM| |MML .MMM  MH\. ".,, Mb. ' ,MH |MMb\ `'.,HMH |MMH\  .,HMMM        #
#      |MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM        #
#                               .ooooooooooooo,                                #
#                                `*MMMMMMMMMH'                                 #
#                                  `*HMMMM*'                                   #
#                                     `H*'                                     #
#                                                                              #
# Purpose  : MasterCell Lightweight Perl Sender                                #
# Author   : Patrice Parmentier (ppa@itmasters.com)                            #
# Fixer    : Dennis Durling (dedurlin@cisco.com)                               #
# Date     : June 25th, 2002 ppa                                               #
# Revision : July 18th, 2002 ppa                                               #
# Revision : May 18th, 2012 dedurlin                                           #
#          : Added features to work with bppm v8.5                             #
#                                                                              #
# (C) Copyright 2002 IT Masters, All Rights Reserved                           #
#                                                                              #
################################################################################

use strict;
# use warnings; # *must* be commented for older Perl versions

use Getopt::Std;

################################################################################

my %args;

################################################################################

sub ITM_VERSION   () { "3.0.1 (Zeus Beta)" }
sub ITM_BUILD     () { "July 18th, 2002" }
sub ITM_COPYRIGHT () { "(c) Copyright 1998-2002 IT Masters, All Rights Reserved" }

################################################################################
#
# Error messages ! unlike modules, arguments begin at $_[0] !
#
################################################################################

sub ERR_CELLNAME     { "Cannot get information about cell '$_[0]' in directory file\n" }
sub ERR_CLI          { "Invalid argument(s): $_[0]\n" }
sub ERR_DONOTHING () { "No event input (eg {SourceFile}, '-' or -a Class) is provided" }
sub ERR_FILECLASS () { "{SourceFile} argument (or '-') is not compatible with -a, -b, -m, -o or -r options" }
sub ERR_FILESTDIN () { "{SourceFile} argument is not compatible with '-' (read from standard input)" }
sub ERR_GETHOSTBYNAME { "gethostbyname failed on '$_[0]': $!\n" }
sub ERR_HOSTNAME     { "Cannot get the hostname of the local machine: $!" }
sub ERR_MISSINGCLASS () { "Class (-a options) is missing" }
sub ERR_OPEN         { "Cannot open file '$_[0]': $!\n" }
sub ERR_SOCKCLOSE    { "Couldn't disconnect on '$_[0]:$_[1]': $!\n" }
sub ERR_SOCKCONNECT  { "Couldn't connect to '$_[0]:$_[1]': $!\n" }
sub ERR_SOCKPRINT    { "Print failed on socket: $!\n" }

################################################################################

sub Header ()
  {
    print STDERR
      ("MasterCell ", ITM_VERSION,
       " Perl Simple Sender (build: ", ITM_BUILD, ")\n",
       ITM_COPYRIGHT, "\n");
  }

################################################################################

sub Usage
  {
    Header ();
    print STDERR <<EOS;

usage:

perl $0 [-a Class] [-f DirFile] [-h|-?] [-l HomeDir] [-n CellName[:cell2[:...]] | -n \@Host[:Port]] [-q] [-v] [- | {SourceFile} | -a Class [-b SlotSetValue] [-m Message] [-o Source] [-r Severity]]

-a Send object of class Class
-b Add SlotSetValue settings (format: "slot=value;...")
-f Directory file path (default: <MCELL_HOME>/etc/mcell.dir)
-h Print this help and exit
-l Home directory (eg <MCELL_HOME>)
-m Send event message to Message
-n Connect to server CellName - as defined in directory
   or on indicated host and port
-o Send event source to Source
-q quiet execution (no banner)
-r Send event severity to Severity
-v Verbose
-z Print version number and exit
-  Input from standard input stream
-H Set the local hostname (for mc_host)
-I Set the local IP (for mc_host_address)

EOS
    exit ($_[0] or 0);
  }

################################################################################
#
# BEGIN section. Check if libraries can be found and load them
#
################################################################################

BEGIN
  {
    # Get command line arguments

    defined (getopts ("a:b:f:h?l:m:n:o:H:I:qr:vz", \%args)) or Usage (1);

    if ($args{h} or $args{"?"}) { Usage }
    if ($args{z}) { Header (); exit (0); }

    # Check for not compatible arguments

    my $a = ($args{b} or $args{m} or $args{o} or $args{r});

    if (@ARGV and ($args{a} or $a))
      { print STDERR ERR_CLI(ERR_FILECLASS);    Usage (1) }
    if ($a and ! $args{a})
      { print STDERR ERR_CLI(ERR_MISSINGCLASS); Usage (1) }
    if (! $args{a} and ! @ARGV)
      { print STDERR ERR_CLI(ERR_DONOTHING);    Usage (1) }

    my ($file, $stin) = (0, 0);
    foreach (@ARGV) { (/^-$/ ? ($stin=1) : ($file=1)) }
    if ($file and $stin or $stin and @ARGV > 1)
      { print STDERR ERR_CLI(ERR_FILESTDIN);    Usage (1) }

    Header () unless $args{q};

    # Set MCELL_HOME environment variable - MCELL_HOME (or the corresponding
    # home directory) is not necessary here. It is set to the somewhat dummy
    # "." if it not available. Note that in this case, the MC:: perl modules
    # need to be found in the default perl library directory.

    if ($args{l}) { $ENV{MCELL_HOME} = $args{l} }
    $ENV{MCELL_HOME} or $ENV{MCELL_HOME} = ".";
    $ENV{MCELL_HOME} =~ s/\\/\//g; # Make MCELL_HOME to contain slashes
  }

################################################################################
#
# Main data
#
################################################################################

my $self_ =
  {
   args       => \%args,
   cells      => [],
   cinfos     => undef,
   server     => undef,
   port       => undef,
   _inet_addr => undef,
   _socket    => undef,
  };

################################################################################
#
# Simple version of the trace routine (verbose or not)
#
################################################################################

sub Trace
  {
    $args{v} or return 0;
    my $msg = (@_ ? shift : (caller(1))[3]);
    my ($pkg, $fln, $lnb) = (@_ ? caller (shift()) : caller);
    my ($s, $m, $h) = gmtime ();
    $m = "0$m" if $m < 10;
    $s = "0$s" if $s < 10;
    $h = "0$h" if $h < 10;
    print STDERR "$h:$m:$s $pkg:$lnb ";
    print STDERR "$msg" if ($msg ne "");
    print STDERR "\n" if $msg !~ /\n$/;
  }

################################################################################

sub END { Disconnect ($self_) }

################################################################################
#
# Main program
#
################################################################################

sub main ()
  {
    Trace ("Beginning main");

    # Initialize connection

    my $obj = bless ($self_, "main"); # Trick to run the main script as object
    $obj->InitSender;

    # Send the events

    if ($obj->{args}{a}) { $obj->SendCLIEvent; return 0 }
    while (my $file = shift @ARGV) { $obj->SendFileEvents ($file) }

    return 1;
  }

################################################################################

sub InitSender
  {
    Trace;
    my $self = shift;
    ! $self->{sender} or return 1;

    if (! $args{n}) {}
    elsif ($args{n} =~ /^\@(.*?)(?::(\d+))?$/)
      {
	$self->{server} = ($1 or undef);
	$self->{port}   = ($2 or undef);
      }
    else
      {
	my $cell = $args{n};
	if ($args{n} =~ /:/)
	  {
	    push (@{$self->{cells}}, split (":", $args{n}));
	    $cell = shift @{$self->{cells}}; # $self->{cells} contains "backup cells"
	  }

	$self->{cinfos} or $self->ReadMcellDir;
	my $info = $self->{cinfos}{$cell} or die ERR_CELLNAME ($cell);
	$self->{server} = $info->{address};
	$self->{port}   = $info->{port};
      }
  }

################################################################################

sub ReadMcellDir
  {
    Trace;
    my $self = shift;

    my $dirFile = ($self->{args}{f} or "$ENV{MCELL_HOME}/etc/mcell.dir");
    open (HFILE, "<$dirFile") or die ERR_OPEN ($dirFile);

    while (<HFILE>)
      {
	next if /^\s*([\#\!\%].*)?$/;      # Skip comment line
	chomp();

	/^\s*(cell|gateway[\.\w+]*|server) # Match type (eg cell or gateway)
	  \s+(\w+)                         # Cell name
	    \s+(\w+)                       # Encryption key (useless here)
	      \s+([\w\.\-]+):(\d+)           # Address:Port
		\s*([\#\!\%].*)?$/x        # Tolerate comments at end of line
	or ((print STDERR "$dirFile:$.: Cannot parse '$_'\n"), next);

	$self->{cinfos}{$2} = # Store all information, just in case
	  {type          => ($1 eq "server" ? "cell" : $1),
	   encryptionKey => $3,
	   address       => $4,
	   port          => $5};

	Trace ("Read $1 '$2': $4:$5");
      }
    close (HFILE);
  }

################################################################################

sub SendCLIEvent
  {
    Trace;
    my $self = shift;
    my $cn = $self->{args}{a} or return 0; # Classname

    my $ev = "$cn;";

    # Set slots

    if ($self->{args}{b})
      {
	$self->{args}{b} =~ s/^;+//;
	$self->{args}{b} =~ s/;+$//;
	$ev .= $self->{args}{b};
	$ev .= ";";
      }

    my $rv;
    if ($rv = \$self->{args}{m}, $$rv) { $$rv =~ s/\'/\'\'/g; $ev .=  "msg = '$$rv';" }
    if ($rv = \$self->{args}{o}, $$rv) { $$rv =~ s/\'/\'\'/g; $ev .=  "source = '$$rv';" }
    if ($rv = \$self->{args}{r}, $$rv) { $$rv =~ s/\'/\'\'/g; $ev .=  "severity = '$$rv';" }

    _SetDefaultSlots ($ev, $self->{args});
    $ev .= "END\n";
    _FilterComments ($ev); # mmh, who damn could put comments in option values?

    # Send the event

    $self->Send ($ev);
  }

################################################################################

sub SendFileEvents
  {
    my ($self, $file) = @_;

    my $h = \*STDIN;
    if ($file eq "-") { $h = \*STDIN }
    else { open ($h, "<$file") or die ERR_OPEN ($file) }

    my $buf = "";
    my $pos = 0;
    while (<$h>)
      {
	$buf .= $_;
	_FilterComments ($buf);
	next unless /END\s*\n$/; # Check the event only when END appears

	pos ($buf) = $pos;

	my $e = _CheckForEnd (\$buf) or next;
	my $ev = substr ($buf, 0, $e);

	$ev =~ s/END\s*\n$//;
	_SetDefaultSlots ($ev, $self->{args});
	$ev .= "END\n";

	$self->Send ($ev);

	$buf = substr ($buf, $e);
      }
    close ($h) unless $file eq "-";
  }

################################################################################

sub _CheckForEnd
  {
    my $r = shift;
    while (1)
      {
	return pos $$r if $$r =~ /\G[^\'\"]*;\s*END\s*\n/cgs;
	$$r =~ /\G.*?([\'\"])/gs or return 0;
	my $c = $1;
	$$r =~ /\G(?:[^$c]|$c$c)*?$c(?=[^$c])/gs or return 0;
      }
  }

sub _FilterComments
  {
    while ($_[0] =~ /([\'\"\#])/g)
      {
	my $c = $1;
	if ($c eq "\#") { if ($_[0] =~ s/(?:^|\n)\s*\#\G.*\n//) {pos $_[0]=0}}
	else { $_[0] =~ /\G(?:[^$c]|$c$c)*?$c(?=[^$c])/gs or return 1 }
      }
  }

################################################################################


################################################################################

sub _SetDefaultSlots {
    my $args = @_[1];
    my $mc_host;
    my $mc_host_address;
    if ($args{H}) {
        $mc_host=$args{H};
    }else{
        $mc_host=`hostname -A`;
    }
    if ($args{I}) {
        $mc_host_address=$args{I};
    }else{
        $mc_host_address=`ifconfig eth0|grep -w inet|awk -F: '{print \$2}'|awk '{print \$1}'`;
    }
    chomp($mc_host);
    $mc_host='mc_host='.$mc_host.';';
    chomp($mc_host_address);
    $mc_host_address='mc_host_address='.$mc_host_address.';';
    Trace;
    $_[0] .= "mc_arrival_time=" . time . ";" . $mc_host . $mc_host_address;
}

################################################################################
#
# Special routines for LS
#
################################################################################

use Socket;

################################################################################
#
# Constants
#
################################################################################

sub DEFAULT_PORT      () { 1828 }
sub HEADER_LENGTH_MAX () { 2000 } # For compliance with some 3rd party products ;o)

################################################################################

sub Connect
  {
    my ($self) = @_;
    ! defined ($self->{_socket}) or return 1;

    # Check for the server name (use the local host by default)

    $self->{server} or $self->{server} = hostname () or die ERR_HOSTNAME;
    $self->{port}   or $self->{port}   = DEFAULT_PORT;

    $self->InetAddr; # Create the internet address

    # Create the connection

    Trace ("Connecting socket on '$self->{server}:$self->{port}'");

    socket (HSOCK, PF_INET, SOCK_STREAM, getprotobyname('tcp'));
    $self->{_socket} = \*HSOCK;
    my $paddr = sockaddr_in ($self->{port}, $self->{_inet_addr});

    if (! connect ($self->{_socket}, $paddr))
      {
	undef $self->{_socket};
	@{$self->{cells}} # Have we backup cells?
	  or die ERR_SOCKCONNECT ($self->{server},$self->{port});

	Trace (ERR_SOCKCONNECT ($self->{server},$self->{port}));

	# Let's try the next cell on the list

	$args{n} = shift @{$self->{cells}};
	$self->InitSender;
	return $self->Connect;
      }

    Trace ("Connection to '$self->{server}:$self->{port}' established");

    # Make autoflush on ! It is mandatory because there cannot be any delay
    # between the connection time and the first event to send

    my $fh=select $self->{_socket}; $|=1; select $fh;

    return $self->{_socket};
  }

################################################################################

sub Disconnect
  {
    Trace;
    my $self = shift;
    return 1 if ! $self->{_socket};
    close $self->{_socket}
      or die ERR_SOCKCLOSE ($self->{server},$self->{port});
  }

################################################################################

sub InetAddr
  {
    Trace;
    my $self = shift;
    ! $self->{_inet_addr} or return $self->{_inet_addr};

    if ($self->{server} =~ /^[\dx]+(\.[\dx]+){3}$/)
      { $self->{_inet_addr} = inet_aton ($self->{server}) }
    else
      {
	my ($n, $a, $t, $l, @a) = gethostbyname ($self->{server})
	  or die ERR_GETHOSTBYNAME ($self->{server});

	@a <= 1 or
	  Trace
	    ("WARNING! Several interfaces have been found: " .
	     join (", ", map { inet_ntoa($_) } @a) .
	     ". The first address will be used (" .
	     inet_ntoa ($a[0]) . ")\n");

	Trace ("IP address of server: " . inet_ntoa ($a[0]));
	$self->{_inet_addr} = $a[0];
      }
    return $self->{_inet_addr};
  }

################################################################################

sub Send
  {
    Trace;
    my ($self, $ev) = @_;

    # Check or open the connection

    $self->Connect or return;

    # Send the event

    my $m = $ev;
    my $l = length $m;
    my $h = HEADER_LENGTH_MAX;

    Trace ("Sending message:\n$m");

    $h = HEADER_LENGTH_MAX;

    if ($l >= $h)
      {
	# Cut the packet in 2 parts if it is longer than HEADER_LENGTH_MAX

	my $l2 = $l-$h; # Length of packet 2

	Trace ("Cutting the packet in 2 parts");

	print { $self->{_socket} }
	  (pack ("a8 N7 a$h","<START>>",0,0,0,0,0,$l+1,$l+1,substr($m,0,$h)))
	    and print { $self->{_socket} } (pack ("a$l2 c",substr($m,$h),0x01))
	      or die ERR_SOCKPRINT;
      }
    else
      {
	print { $self->{_socket} }
	  pack ("a8 N7 a$l c","<START>>",0,0,0,0,0,$l+1,$l+1,$m,0x01)
	    or die ERR_SOCKPRINT;
      }
  }

################################################################################

exit main ();

################################################################################