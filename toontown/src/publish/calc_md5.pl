#!/usr/bin/perl -w
use strict;

my $rv = "";
my $path = $ARGV[0];

my $OS = `uname -s`;
chomp $OS;
$OS =~ /([\w]+)/;
$OS = $1;

my $MD5;

if ($OS ne 'Darwin') {
    $MD5 = 'check_md5.exe';
}
else {
#    $MD5 = 'check_md5';
    $MD5 = 'md5';
}
my ($md5_line, $filesize);

unless (-e $path) {
    print "";
    exit(0);
}

if ($OS ne 'Darwin') {
#    $md5_line = `$MD5 -d \`cygpath -w $path\``;
    $md5_line = `$MD5 \`cygpath -w $path\``;
}
else {
#    $md5_line = `$MD5 -d $path`;
    $md5_line = `$MD5 $path`;
}
$filesize = -s $path;
chomp $md5_line;
#$md5_line =~ /([\w|\.]+) (\d+) (\d+) (\d+) (\d+)/; 
#print "$1 $filesize $2 $3 $4 $5\n";

if ($OS eq 'Darwin') {
    $md5_line =~ /\/?([\w|\.]+)\) = ([\w\d]+)/; 
    print "$1 $filesize $2\n";
}
else
{
    $md5_line =~ /([\w|\.]+) ([\w\d]+)/; 
    print "$1 $filesize $2\n";
}

0;
