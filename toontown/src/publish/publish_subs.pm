#!/usr/bin/perl -w

####################################################################
####################################################################
## publish_subs.pm: 
##      A collection of sub routines used in the publish process,
##      collected into one file so that we aren't duplicating code.
##
####################################################################
####################################################################

use strict;
use Exporter;

use vars qw(@ISA @EXPORT);
@ISA = qw(Exporter);
@EXPORT = qw(decygwin docmd getOS getPubSeries);

####################################################################
####################################################################
# Add your publish series to this list and commit to CVS           #
my %pub_series;                                                    #
$pub_series{'toonpub'  } = 1400;                                   #
$pub_series{'drose'    } = 2000;                                   #
$pub_series{'shochet'  } = 3000;                                   #
$pub_series{'jhancock' } = 3400;                                   #
$pub_series{'piratepub'} = 3400;                                   #
$pub_series{'webell'}    = 3200;                                   #
$pub_series{'gphilip'}   = 3300;                                   #
####################################################################
####################################################################

sub decygwin
{
    my ($oldvalue) = @_;
    print "oldvalue=$oldvalue\n";
    die if $oldvalue eq "";

    my $OS = getOS();

    if ($OS eq 'Darwin') {
        return $oldvalue;
    }

    my ($newvalue) = `cygpath -m "$oldvalue"`;

    # strip leading and trailing whitespace
    $newvalue =~ s/^\s*(.*?)\s*$/$1/;
    
    return $newvalue;
}

sub docmd
{
    my ($cmd) = @_;

    print "$cmd\n";
    system("$cmd");
    die if $? != 0;
}

sub getOS
{
    my $OS = `uname -s`;
    chomp $OS;
    $OS =~ /([\w]+)/;
    $OS = $1;

    return $OS;
}

sub getPubSeries
{
    my ($user) = @_;

    if(defined($pub_series{$user}))
    {
        return $pub_series{$user} 
    }
    else
    {
        print "Unknown user '$user'....dying";
        exit(1);
    }
}
