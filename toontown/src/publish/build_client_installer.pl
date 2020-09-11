#!/usr/bin/perl -w
use strict;
use File::Copy;
use publish_subs;

if(@ARGV<1)
{
    print "$0 usage:\n";
    print "\t $0 target user language\n";
    print "\ttarget can be any of [dev|test|qa|live]\n";
    print "\tuser is optional\n";
    exit(1); 
}

my $build_targ = $ARGV[0];
my $pub_user   = $ARGV[1];
my $language   = $ARGV[2];
if (!defined($pub_user)) 
{
    $pub_user = $ENV{USER};
}

if(!defined($language))
{
    $language="English";
}

my $pub_series=getPubSeries($pub_user);

my $TOONTOWN   = "$ENV{TOONTOWN}";
my $TLAUNCHER = "$ENV{TLAUNCHER}";
my $DCTOONTOWN   = decygwin($TOONTOWN);
my $DCTLAUNCHER = decygwin($TLAUNCHER);


# Make sure that we're attached to the correct trees
if(!$TLAUNCHER)
{
    print "ERROR: not attached to LAUNCHER tree...dying!\n\n";
    exit(1);
}

if(!$TOONTOWN)
{
    print "ERROR: not attached to TOONTOWN tree...dying!\n\n";
    exit(1);
}

my $OS = getOS();

my ($NSIS, $paramtxt_path);
my (@NSIS_paths) = ('/c/apps/development/NSIS/makensis.exe', '/c/Program Files/NSIS/makensis.exe');

if($OS ne 'Darwin')
{
    $paramtxt_path='parameters.txt';
    for(my $i=0; $i<@NSIS_paths && !defined($NSIS); $i++) 
    {
        if(-e $NSIS_paths[$i])
        {
            $NSIS="\"" . $NSIS_paths[$i] . "\"" ; #enclose it in quotes in case the path has spaces
        }
    }

    if(!$NSIS)
    {
        print "ERROR: Unable to locate NSIS.\n\n";
        exit(1);
    }

    print "NSIS:           |$NSIS|\n";
}
else
{
    $paramtxt_path="$TLAUNCHER/Launcher-Mac/build/Release/Launcher.app/Contents/MacOS/parameters.txt";
}




print "TOONTOWN:       |$TOONTOWN|\n";
print "TLAUNCHER:      |$TLAUNCHER|\n";
print "publish user:   |$pub_user|\n";
print "publish series: |$pub_series|\n";
print "build type:     |$build_targ|\n";
print "paramtxt_path:  |$paramtxt_path|\n";
print "language:       |$language|\n";

my $PRODVER = " " . uc($build_targ);
my $PRODREL = "_" . uc($build_targ);

if ($build_targ eq "qa")
{
    copy("parameters_QA.txt", $paramtxt_path) or die "copy failed: $!";
}
elsif ($build_targ eq "qa2")
{
    copy("parameters_QA2.txt", $paramtxt_path) or die "copy failed: $!";
}
elsif ($build_targ eq "dev")
{
    copy("parameters_DEV.txt", $paramtxt_path) or die "copy failed: $!";
}
elsif ($build_targ eq "uk_qa")
{
    $language = "English_UK";
    copy("parameters_UK_QA.txt", $paramtxt_path) or die "copy failed: $!";
}
elsif ($build_targ eq "uk_live")
{
    $language = "English_UK";
    $PRODREL = "_UK";
    copy("parameters_UK.txt", $paramtxt_path) or die "copy failed: $!";
}
elsif ($build_targ eq "test")
{
    copy("parameters_TEST.txt", $paramtxt_path) or die "copy failed: $!";
}
elsif ($build_targ eq "live")
{
    $PRODVER='';
    $PRODREL=''; 
    # live doesn't get a parameters.txt file, but check and delete it if there is one
    if( -e $paramtxt_path)
    {
        unlink($paramtxt_path);
    }
   
}
else # must be dev
{
    # Insert the appropriate series number in parameters.txt.
    my $dl_series = $pub_series + 20;
    docmd("sed s/DL_SERIES/$dl_series/g <parameters_DEV.txt >$paramtxt_path");
}


if($OS ne 'Darwin')
{
    # run NSIS
    docmd("$NSIS /V3 /DTOONTOWN=$DCTOONTOWN /DTLAUNCHER=$DCTLAUNCHER /DPRODUCT_VERSION=\"$PRODVER\" /DPRODUCT_RELEASE=\"$PRODREL\" /DLANGUAGE=\"$language\" Toontown-installer.nsi");
}
else
{
    # copy to deployment specific directory
    docmd("rsync -atv --delete-after $TLAUNCHER/Launcher-Mac/build/Release/Launcher.app/ $TLAUNCHER/Launcher-Mac/build/Release/Toontown$PRODREL.app");
   
    # copy to a temp directory and then zip it up...this is needed for self-patching the Launcher application
    docmd("mkdir $TLAUNCHER/Launcher-Mac/build/Release/temp/");
    docmd("rsync -atv --delete-after $TLAUNCHER/Launcher-Mac/build/Release/Launcher.app/ $TLAUNCHER/Launcher-Mac/build/Release/temp/Toontown$PRODREL.app");
    docmd("ditto -ck $TLAUNCHER/Launcher-Mac/build/Release/temp/ $TLAUNCHER/Launcher-Mac/build/Release/Toontown$PRODREL.zip");
    docmd("rm -rf $TLAUNCHER/Launcher-Mac/build/Release/temp/");

    #docmd("$TOONTOWN/src/publish/makeDMG.pl -compressionLevel 9 -slaRsrcFile $TOONTOWN/src/publish/SLA.r -dmgName Toontown-setup$PRODREL -volName Toontown$PRODREL $TLAUNCHER/Launcher-Mac/build/Release/Toontown$PRODREL.app");
    docmd("$TOONTOWN/src/publish/makeDMG.pl -compressionLevel 9 -slaRsrcFile $TOONTOWN/src/publish/SLA.r -internetEnabled -dmgName Toontown-setup$PRODREL -volName Toontown$PRODREL $TLAUNCHER/Launcher-Mac/build/Release/Toontown$PRODREL.app");
}

# remove parameters.txt if we copied one in the above steps
if(-e "$paramtxt_path")
{
    unlink($paramtxt_path);
}
