#!/usr/bin/perl

# This is a script that can be used to pull the bad words list out of the perforce repository. It
# uses the perforce http interface so you don't have to install the perforce client. The files end
# up in your cwd, so take note of where you are running it from

use strict;
use warnings;
use LWP::Simple;
use LWP::UserAgent;

my $perforce_base_url      = 'http://perforce.corp.dig.com:8082';
my $label                  = 'BADWORD_RELEASE_CANDIDATE';
my $perforce_path          = '//p4-doldisl/ChatFilters/dirtyword/ProductionLists/'; # must end with trailing slash
my $escaped_perforce_path  = $perforce_path;
   $escaped_perforce_path  =~s/\//\\\//g; # replace '/' with '\/' because this var is used in a regex
my $url_label              = sprintf('%s/@md=d&cd=%s&c=xkd&cdf=@/%s?ac=118', $perforce_base_url, $perforce_path, $label);
my $url_file_details       = $perforce_base_url . '/@md=d&cd=%s&c=9o2@%s%s?ac=22'; # has 3 %s in it: perforce_path, perforce_path, filename

my %filenames = getFileNames($url_label, $escaped_perforce_path);

foreach my $file(sort keys %filenames)
{
    printf ("%s is on version %3d of %s\n", $label, $filenames{$file}, $file);
    getFile($file, $filenames{$file});
}


sub getFile
{
    my ($file, $version) = @_;

    unlink($file) if (-e $file);

    my $url = getUrlForVersion($file, $version);

    my $content = getFileHttp($url, $file);

    if(!(-e $file))
    {
        print STDERR "ERROR fetching version $version of file $file from url $url\n";
    }
    else
    {
        my $is_empty = 0;

        open IN, "<$file" or die("Can't open $file for input");

        while(my $line=<IN>)
        {
            if($line=~m/File not found, or file is empty/)
            {
                $is_empty = 1;
            }
        }

        close IN;

        if($is_empty)
        {
            print STDERR "WARNING: file is empty-> $file\n";
            unlink($file);
            system("touch $file");
        }
               
    }
}

# given a filename and a revision number, it returns the url so you can grab the file
sub getUrlForVersion
{
    my ($file, $version) = @_;

    my $url = sprintf($url_file_details, $perforce_path, $perforce_path, $file);
    
    my $content = getFileHttp($url);

    my @lines=split(/\n/, $content);

    foreach my $line(@lines)
    {
        if($line=~m/<a href="(.+)" title="Open file in browser">(\d+)<\/a>/ )
        {
            # the url is absolute, but lacks host/port
            my $rel_url = $1;
            my $ver     = $2;

            if($ver == $version)
            {
                return $perforce_base_url . $rel_url;
            }
        }
    }
}


# returns associative array of filename->revision number
sub getFileNames
{
    my ($url, $p4path) = @_;

    my $content = getFileHttp($url);

    my @lines = split(/\n/, $content);

    my %files;

    foreach my $line(@lines)
    {
        if($line=~m/${escaped_perforce_path}(.+.txt)#(\d+)/)
        {
            $files{$1}=$2;
        }
    }

    return %files; 

} 

# Function:    getFileHttp
# Description: gets $url. If $outputFile is specified, it writes the contents
#              to that file, else it returns the contents
sub getFileHttp
{
    my ($url, $outputFile) = @_;
    
    my $ua = new LWP::UserAgent;  #user agent

    if(defined($outputFile))
    {
        my $response = $ua-> get($url, ':content_file' => $outputFile);
    }
    else
    {
        my $content = get($url);
        return $content;
    }
}

