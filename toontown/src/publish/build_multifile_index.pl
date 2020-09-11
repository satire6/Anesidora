#!/usr/bin/perl -w
use strict;
use Cwd;

use constant TEMP_DIR => '/tmp';

my $MD5 = "$ENV{TOONTOWN}/src/publish/calc_md5.pl";

sub addDirList
{
    my ($dir, $path_string) = @_;

    #store cwd for restoration later
    my $cwd = cwd();

    chdir($dir) || die("Unable to cd to $dir");

    my @files=<*>;

    foreach my $file(@files)
    {
        if(-d $file) #if it's a directory...
        {
            addDirList($file, $path_string . $file . "/");
        }
        else
        {
            addFile($file, $path_string . $file);
        }
    }          

    #restore cwd
    chdir($cwd);
}

sub addFile
{
    my ($filename, $filepath) = @_;

    my ($size, $md5) = calc_md5($filename);

    print OUT "$filepath $size $md5\n";    

}

# returns the file size and md5 checksum of the specified input file
sub calc_md5
{
    my ($path) = @_;
    my $md5_line;

    print "Calculating md5 for $path\n";

    return "" unless (-e $path);

    #print "$path\n";
    $md5_line = `$MD5 $path`;
    chomp $md5_line;
    
    my @info = split(/\s+/, $md5_line);

    print "(file, size, md5) = ($path, $info[1], $info[2])\n";
    
    return ($info[1], $info[2]);
}

########################################################################################
###
###       MAIN PROGRAM IS BELOW
###
########################################################################################

if(@ARGV!=1)
{
    print "INVALID # OF ARGUMENTS\n";
    print "usage: $0 multifile\n";
    print "NOTE: you should run this from the directory that contains the multifile\n";
    die();
}

my $multifile = $ARGV[0];

my @mf_split=split(/\./, $multifile);
my $mf_stubname = $mf_split[0];

# We assume that the CWD that this script is called from is the directory with the appropriate
# phase file in it.
my $cwd=cwd();
my $multifile_path = $cwd . "/" . $multifile;

if(!(-e $multifile))
{
    die("$multifile not found in |" . cwd() . "| ....dying\n\n");
}

my $tmp_dir = TEMP_DIR . "/" . $multifile;

# if the directory exists...blast it
if(-d $tmp_dir)
{
    print "removing $tmp_dir\n";
    `rm -rf $tmp_dir`;
}

# create a temporary directory for our extraction purposes
mkdir($tmp_dir);

chdir($tmp_dir);

print "extracting the contents of $multifile_path to $tmp_dir\n\n";
`multify -xf "$multifile_path"`;

my $index_filename = "$mf_stubname\_index.txt";
my $outfile = TEMP_DIR . "/$index_filename";

open OUT, ">$outfile" or die("Unable to open $outfile for output.");

addDirList(".", "");

close OUT;

chdir(TEMP_DIR);

# add the newly created index file to the multifile
print "Adding $index_filename to $multifile_path\n";
`multify -rf "$multifile_path" "$index_filename"`;


# change back to $cwd so that we can remove the temporary extraction directory
chdir($cwd);

# remove the temporary extract directory
`rm -rf $tmp_dir`;


# remove the index file
#unlink($outfile);
