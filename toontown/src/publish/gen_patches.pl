#!/usr/bin/perl -w
use strict;
use publish_subs;

use constant SIZE_INDEX => 7;

# this is a %. If the size of all the patches that you would need to get current is > than this
# percentage of a full download, just do the full download instead.
use constant SIZE_THRESHOLD => .8;
my @cleanup_files; #array to hold temporary files that will get deleted

my $bzip = "bzip2";
my $MD5 = "$ENV{TOONTOWN}/src/publish/calc_md5.pl";
my $BUILD_PATCH = "$ENV{PANDA}/built/bin/build_patch.exe";
my $PATCHER_VER = "patcher.ver"; #patcher.ver is located in the content dir

sub unbzip
{
    my ($source) = @_;
    my ($dest) = $source;
    $dest =~ s/\.bz2$//;

    print "unzipping $source to $dest\n";
    die if $source eq $dest;

    unlink($dest);
    docmd("$bzip -d -k $source");
}

sub bzip
{
    my ($source) = @_;
    my ($dest) = $source . ".bz2";

    print "zipping $source to $dest\n";
    die if $source eq $dest;

    unlink($dest);
    docmd("$bzip -k2 $source");
}

# returns the file size and md5 checksum of the specified input file
sub calc_md5
{
    my ($path) = @_;
    my $md5_line;

    #print "Calculating md5 for $path\n";

    return "" unless (-e $path);

    #print "$path\n";
    $md5_line = `$MD5 $path`;
    chomp $md5_line;
    
    my @info = split(/\s+/, $md5_line);

    print "(file, size, md5) = ($path, $info[1], $info[2])\n";
    
    return ($info[1], $info[2]);
}



sub cleanup
{
    my (@files) = @_;

    print "\n\n************** CleanUp\n\n";
    
    foreach my $file(@files)
    {
        print "removing file $file\n";
        unlink($file);
    }
    print "\n\n************** CleanUp\n\n";

}

sub generate_patch
{
    my ($old, $new) = @_;

    docmd("$BUILD_PATCH $old $new");
}

sub addInfoToVer
{
    my ($file_to_patch, $latest_version, $latest_file, $size_latest, $md5_latest, $size_last, $md5_last, $patch_file) = @_;

    my $line;
    my $flag;

    print "Adding information to patcher.ver for $file_to_patch\n";

    open IN, "<$PATCHER_VER" or die("Unable to open $PATCHER_VER for input.");
    open OUT, ">$PATCHER_VER\.temp" or die("Unable to open $PATCHER_VER.temp for output.");

    while($line=<IN>)
    {
        chomp($line);
        if($line=~m/FILE_$file_to_patch\.current=/)
        {
            print OUT "FILE_$file_to_patch.current=v1.$latest_version\n";
        }
        elsif($line=~m/^\#$file_to_patch/)
        {
            print OUT "$line\n";
            $flag=1;
            while($flag)
            {
                $line=<IN>;
                chomp($line);
                if(!($line=~m/\w+/)) 
                {
                    $flag=0;
                }
                elsif (!($line=~m/FILE_$file_to_patch\.v1\.$latest_version\=/))
                { 
                    print OUT "$line\n"; 
                }
            }

            print OUT "FILE_$file_to_patch.v1.$latest_version=$size_latest $md5_latest\n\n";
        }
        elsif($line=~m/^\#patches $file_to_patch/ && defined($patch_file))
        {
            print OUT "$line\n";
            $flag=1;
            while($flag)
            {
                $line=<IN>;
                chomp($line);
                if(!($line=~m/\w+/)) { $flag=0;             }
                else                 { print OUT "$line\n"; }
            }

            print OUT "PFILE_$file_to_patch.v1.$latest_version.pch=$size_last $md5_last $size_latest $md5_latest\n\n";

        }
        else
        {
            print OUT "$line\n";
        }
    }

    close IN;
    close OUT;
    
    docmd("dos2unix $PATCHER_VER.temp");
    docmd("mv $PATCHER_VER.temp $PATCHER_VER");
}

sub removeInfoFromVer
{
    my ($file) = @_;

    #print "Removing patcher.ver info for file $file\n";

    my ($line, $beginning_line); 

    if($file=~m/\.pch$/) { $beginning_line = "PFILE"; }
    else                 { $beginning_line = "FILE";  }

    open IN, "<$PATCHER_VER" or die("Unable to open $PATCHER_VER for input.");
    open OUT, ">$PATCHER_VER\.temp" or die("Unable to open $PATCHER_VER.temp for output.");

    while($line=<IN>)
    {
        if(!($line=~m/^$beginning_line\_$file=/))
        {
            print OUT $line;
        }
    }

    close IN;
    close OUT;
    
    docmd("dos2unix $PATCHER_VER.temp");
    docmd("mv $PATCHER_VER.temp $PATCHER_VER");
}
sub removeOldPatches
{
    my ($file, $current_file_size) = @_;

    my ($i, @fileattribs, $cum_patch, $size_threshold);

    print "Checking patches for $file to see if we can toss any old patches\n";

    #my $fileglob = $file . ".v1.*.pch.bz2";

    my @files=<$file.v1.*.pch.bz2>;

    @files = sort_versioned_file_array(@files);

    $cum_patch = 0;
    $size_threshold = int(SIZE_THRESHOLD * $current_file_size);

    for($i=0; $i<@files; $i++)
    {
        @fileattribs = stat($files[$i]);
        $cum_patch+=$fileattribs[SIZE_INDEX];

        print "$files[$i] $cum_patch\n";

        
        if($cum_patch > $size_threshold)
        {
            #print "this file should be deleted $files[$i] $cum_patch $size_threshold\n";
            $files[$i]=~m/(.+)\.bz2/;
            removeInfoFromVer($1);            # remove the info from patcher.ver
            push(@cleanup_files, $files[$i]); # mark the file for deletion

        }
    }
}

sub removeOldPhaseFiles
{
    my ($file, $currentVersion) = @_;

    my @files=<$file.v1.*.bz2>;

    foreach my $phasefile(@files)
    {
        if($phasefile=~m/$file\.v1\.(\d+)\.bz2/)
        {
            if($1 != $currentVersion)
            {
                $phasefile=~m/(.+)\.bz2/;
                removeInfoFromVer($1); # remove the info from patcher.ver
                push(@cleanup_files, $phasefile);
            }
        }
    }
}

# sorts the array into descending order
sub sort_versioned_file_array
{
    
    my (@sub_array) = @_;

    my ($i, $j, $temp);

    for($i=0; $i<@sub_array; $i++)
    {
        for($j=@sub_array-1; $j>=$i+1; $j--)
        {
            #if($fbinarray[$j] lt $fbinarray[$j-1])
            if(versioned_file_compare($sub_array[$j], $sub_array[$j-1])>0)
            {
                $temp=$sub_array[$j];
                $sub_array[$j]=$sub_array[$j-1];
                $sub_array[$j-1]=$temp;
            }
        }
    }

    return (@sub_array);
}

sub versioned_file_compare
{
    my ($file1, $file2) = @_;

    #print "called with file1=$file1 file2=$file2\n";
    my($version1, $version2, $result);

    if($file1=~m/\.v1\.(\d+)\./)
    {
        $version1 = $1;
        #print "version1=$version1\n";
    }

    if($file2=~m/\.v1\.(\d+)\./)
    {
        $version2 = $1;
        #print "version2=$version2\n";
    }

    if(defined($version1) && defined($version2))
    {
        if($version1 < $version2)  { $result = -1; }
        if($version1 == $version2) { $result = 0;  }
        if($version1 > $version2)  { $result = 1;  }

        #print "i'm in here....result = $result\n\n";
    }

    return $result;
}

########################################################################################
###
###       MAIN PROGRAM IS BELOW
###
########################################################################################

if(@ARGV != 1)
{
    print "$0: Script to generate patches.\n";
    print "\tusage: $0 directory\n";
    exit(1);
}

my $dir = $ARGV[0];

chdir($dir) || die("Unable to change directories to $dir");

#my ($size, $md5)=calc_md5("phase_3.mf.v1.2.bz2");
#print "size=$size md5=$md5\n";
#exit();


my @files_in_dir = <*>;

my @files_to_patch = ("phase_1.mf", "phase_1OSX.mf", "phase_2.mf", "phase_2OSX.mf", "phase_3.mf", "phase_3.5.mf", "phase_4.mf", "phase_5.mf", "phase_5.5.mf", "phase_6.mf", "phase_7.mf", "phase_8.mf", "phase_9.mf", "phase_10.mf", "phase_11.mf", "phase_12.mf", "phase_13.mf"); 

my %do_patch;

$do_patch{"phase_1.mf"}    = 1;
$do_patch{"phase_1OSX.mf"} = 1;
$do_patch{"phase_2.mf"}    = 1;
$do_patch{"phase_2OSX.mf"} = 1;
$do_patch{"phase_3.mf"}    = 1;
$do_patch{"phase_3.5.mf"}  = 1;
$do_patch{"phase_4.mf"}    = 1;
$do_patch{"phase_5.mf"}    = 1;
$do_patch{"phase_5.5.mf"}  = 1;
$do_patch{"phase_6.mf"}    = 1;
$do_patch{"phase_7.mf"}    = 1;
$do_patch{"phase_8.mf"}    = 1;
$do_patch{"phase_9.mf"}    = 1;
$do_patch{"phase_10.mf"}   = 1;
$do_patch{"phase_11.mf"}   = 1;
$do_patch{"phase_12.mf"}   = 1;
$do_patch{"phase_13.mf"}   = 1;

my ($last_ver, $currentVersion);
my $patch_file;
my $patch_file_bz2;
my $zipped_size_current;
my @file_attribs;

foreach my $file_to_patch(@files_to_patch)
{
    $last_ver = -1;
    foreach my $file(@files_in_dir)
    {
        if($file=~m/^$file_to_patch\.v1.(\d+)\.bz2/)
        {
            if($1>$last_ver)
            {
                $last_ver = $1;
            }

        }
    }

    my $latest_version = $last_ver+1;
    my $latest_file_bz2    = $file_to_patch . ".v1." . $latest_version . ".bz2";
    my $last_file_bz2      = $file_to_patch . ".v1." . $last_ver . ".bz2";

    my $latest_file = $file_to_patch . ".v1." . $latest_version;
    my $last_file   = $file_to_patch . ".v1." . $last_ver;
    
    
    print "renaming $file_to_patch.bz2 to $latest_file_bz2\n";
    rename("$file_to_patch.bz2", $latest_file_bz2);

    push(@cleanup_files, $latest_file);
    unbzip($latest_file_bz2);
    my ($size_latest, $md5_latest) = calc_md5($latest_file);

    my ($size_last, $md5_last);
    if($last_ver == -1)
    {
        # No previous version. $beginning_line = "FILE_"; }
        $size_last = 0;
        $zipped_size_current = 0;
        $md5_last = "";
    }
    else
    {
        push(@cleanup_files, $last_file);
        unbzip($last_file_bz2);
        ($size_last, $md5_last)     = calc_md5($last_file);
        @file_attribs = stat($last_file_bz2);
        $zipped_size_current = $file_attribs[SIZE_INDEX];
    }

    if($md5_latest eq $md5_last)
    {
        #remove the file, because it hasn't changed for this publish
        push(@cleanup_files, $latest_file_bz2);

        # Even though it hasn't changed, we want to make sure the info
        # in patcher.ver is up-to-date.
        addInfoToVer($file_to_patch, $last_ver, $last_file, $size_last, $md5_last, undef, undef, undef);
        $currentVersion = $last_ver;
    }
    else
    {
        if($last_ver != -1 && defined($do_patch{$file_to_patch}))
        {
            generate_patch($last_file, $latest_file);
            $patch_file = $latest_file . ".pch";
            bzip($patch_file);
            push(@cleanup_files, $patch_file);
            $patch_file_bz2 = $patch_file . ".bz2";
            @file_attribs = stat($latest_file_bz2);
            $zipped_size_current = $file_attribs[SIZE_INDEX];

            addInfoToVer($file_to_patch, $latest_version, $latest_file, $size_latest, $md5_latest, $size_last, $md5_last, $patch_file);
            $currentVersion = $latest_version;
        }
        else #we don't patch the file, but if it changed, we still need to add its info to patcher.ver
        {
            addInfoToVer($file_to_patch, $latest_version, $latest_file, $size_latest, $md5_latest, undef, undef, undef);
        }

    }

    # check to see if there are any old patches we can remove
    removeOldPatches($file_to_patch, $zipped_size_current);
    removeOldPhaseFiles($file_to_patch, $currentVersion);

    print "\n\n";
    
}

cleanup(@cleanup_files);

exit(0);
