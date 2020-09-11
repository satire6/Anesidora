#!/usr/bin/perl -w
use strict;
use File::Copy;
use publish_subs;

my $OS = getOS; 

# script to publish files from builds to remote server
sub usage()
{
    print "Usage: perl $0 [dev|qa|live|test] [user]\n";
    print "\t[dev|qa|live|test] specifies build type\n"
    	. "\t[user] string specifying target upload user name\n";
    exit(1);
}

if($#ARGV+1 < 1) {
    usage();
}

my $build_targ = $ARGV[0];

my $pub_user = $ARGV[1];
if (!defined($pub_user)) 
{
    $pub_user = $ENV{USER};
}

if ($pub_user eq "dlo") 
{
    $pub_user='toonpub';
}

my $pub_series = getPubSeries($pub_user);

# setup base directory
#
my $TOONTOWN  = "$ENV{TOONTOWN}";
my $TTMODELS  = "$ENV{TTMODELS}";
my $TLAUNCHER = "$ENV{TLAUNCHER}";
my $PUBLISH   = "$ENV{TOONTOWN}/src/publish";

die("Not attached to TOONTOWN tree")  if $TOONTOWN  eq "";
die("Not attached to TTMODELS tree")  if $TTMODELS  eq "";
die("Not attached to TLAUNCHER tree") if $TLAUNCHER eq "";

my $DCTOONTOWN  = decygwin($TOONTOWN);
my $DCTLAUNCHER = decygwin($TLAUNCHER);

my $language="english";

# Pick a release type
#
my $upload_dir = "";
my $installer;
my $sa;
 
if($OS ne 'Darwin') { $sa = "$TLAUNCHER/Launcher1/Toontown/ToontownLauncher.exe"; }

if ($build_targ eq "dev") 
{
    $upload_dir = "/dev";
	
    if($OS ne 'Darwin') { $installer = "$PUBLISH/Toontown-setup_DEV.exe"; }
    else                { $installer = "$PUBLISH/Toontown-setup_DEV.dmg"; $sa = "$TLAUNCHER/Launcher-Mac/build/Release/ToontownOnline_DEV.zip"; }
}
elsif ($build_targ eq "qa") 
{
    $upload_dir = "/qa";
    if($OS ne 'Darwin') { $installer = "$PUBLISH/Toontown-setup_QA.exe"; }
    else                { $installer = "$PUBLISH/Toontown-setup_QA.dmg"; $sa = "$TLAUNCHER/Launcher-Mac/build/Release/ToontownOnline_QA.zip"; }
}
elsif ($build_targ eq "test") 
{
    $upload_dir = "/test";
    if($OS ne 'Darwin') { $installer = "$PUBLISH/Toontown-setup_TEST.exe"; }
    else                { $installer = "$PUBLISH/Toontown-setup_TEST.dmg"; $sa = "$TLAUNCHER/Launcher-Mac/build/Release/ToontownOnline_TEST.zip"; }
}
elsif ($build_targ eq "live") 
{
    $upload_dir = "";
    if($OS ne 'Darwin') { $installer = "$PUBLISH/Toontown-setup.exe"; }
    else                { $installer = "$PUBLISH/Toontown-setup.dmg"; $sa = "$TLAUNCHER/Launcher-Mac/build/Release/ToontownOnline.zip"; }
}
else 
{
    print "$build_targ not recognized!";
    usage();
}

my $DCsa = decygwin($sa);

my ($pub_path, $win_pub_path);
my $web_publish_dir = "/c/publish-web-launcher/toontown/download/$language/currentVersion$upload_dir";

if ($OS ne 'Darwin') 
{
    $pub_path = "/c/ttown-persist/$language";
}
else 
{
    $pub_path = "~/ttown-persist/$language";
    $win_pub_path = "/c/ttown-persist/$language";
}
if (! -e $pub_path) {
    docmd("mkdir -p $pub_path")
}

# Build the installer
docmd("./build_client_installer.pl $build_targ $pub_user");

############################### PHASE FILES ##################################
my @phasepath;
my @phasepathzip;

$phasepath[0]  = "$pub_path/phase_1.mf";
$phasepath[1]  = "$pub_path/phase_2.mf";
$phasepath[2]  = "$pub_path/phase_3.mf";
$phasepath[3]  = "$pub_path/phase_3.5.mf";
$phasepath[4]  = "$pub_path/phase_4.mf";
$phasepath[5]  = "$pub_path/phase_5.mf";
$phasepath[6]  = "$pub_path/phase_5.5.mf";
$phasepath[7]  = "$pub_path/phase_6.mf";
$phasepath[8]  = "$pub_path/phase_7.mf";
$phasepath[9]  = "$pub_path/phase_8.mf";
$phasepath[10] = "$pub_path/phase_9.mf";
$phasepath[11] = "$pub_path/phase_10.mf";
$phasepath[12] = "$pub_path/phase_11.mf";
$phasepath[13] = "$pub_path/phase_12.mf";
$phasepath[14] = "$pub_path/phase_13.mf";


for(my $i=0; $i<@phasepath; $i++)
{
    $phasepathzip[$i]="$phasepath[$i].bz2";
}
############################### PHASE FILES ##################################


print "OS:                   |$OS|\n";
print "Standalone directory: |$sa|\n";
print "installer:            |$installer|\n";
print "TOONTOWN:             |$DCTOONTOWN|\n";
print "TLAUNCHER:            |$DCTLAUNCHER|\n";
print "pub user:             |$pub_user|\n";
print "pub series:           |$pub_series|\n";

sub do_copy
{
    my ($destdir, @files) = @_;
    foreach my $file (@files) 
    {
        next unless $file;
        docmd("rsync -atv $file $destdir");
    }
}

sub do_patch
{  
    my($dir) = @_;

    print "\n\nRunning gen_patches.pl in directory $dir\n\n";

    docmd("./gen_patches.pl $dir");

    print "\n\nDone building patches for $dir\n\n";
}

sub do_upload
{
    if($OS ne 'Darwin')
    {
        docmd("mkdir -p $web_publish_dir/");
        docmd("mkdir -p $web_publish_dir/content");

        my $cpdest = "$web_publish_dir/";

        print "compressing $sa\n";
        system("upx -9 --force \"$DCsa\"");

        print "cp'ing $sa to |$cpdest/content|\n";
        do_copy("$cpdest/content", $sa);

        print "cp'ing $installer to |$cpdest|\n";
        do_copy($cpdest, $installer);

        $cpdest = "$web_publish_dir/content";
        print "cp'ing ";
        foreach my $file(@phasepathzip) { print "$file "; } 
        print "to |$cpdest|\n";

        do_copy($cpdest, @phasepathzip);
        do_patch($cpdest);

        my $remote_host = "ttown4.online.disney.com";
        my $remote_dir = "/toontown/web/toontown-$pub_series/download/$language/currentVersion/${upload_dir}/";

        # ensure that permissions are set correctly on download bits
        docmd("chmod -R 755 $web_publish_dir");

        print "rsyncing to $remote_host\n";
        docmd("rsync -rtv --progress -e ssh -C --include='*.exe' --delete ${web_publish_dir}/ ${pub_user}\@${remote_host}:${remote_dir}");

=head1 commented this out to not step on the pirate's publish
        # this assumes that if you're publishing as piratepub that you want the models uploaded
#        if ($build_targ eq "live" || $pub_user eq 'piratepub') 
#        { 
#            print "rsyncing pmodels\n";
#            my $excludes = "--exclude=audio/ --exclude=maps/ --exclude=shadow_pal/ --exclude='*.ico' --exclude='*.cur'";
#            $remote_dir = "/pirates64/pmodels";
#            docmd("rsync -rtv --progress -e ssh -C --include='*.exe' --delete $excludes $PMODELS/built/ ${pub_user}\@${remote_host}:${remote_dir}");
#        } 
=cut

    }
    else 
    {
        my $remote_host = "10.196.143.103"; # jhancock's build box

        print "rsyncing $installer to $remote_host\n";
        docmd("rsync -atv --progress $installer $remote_host:${web_publish_dir}/");

        print "rsyncing $sa to $remote_host\n";
        docmd("rsync -atv --progress $sa $remote_host:${web_publish_dir}/content");

        print "rsyncing phase_1OSX.mf to $remote_host\n";
        docmd("rsync -atv --progress ${pub_path}/phase_1OSX.mf.bz2 $remote_host:$win_pub_path");
    }
    return 0;
}

if (do_upload()) {
    print "\ncopy failed!\n";
}
else {
    print "\ncopy succeeded!\n";
}

0;
