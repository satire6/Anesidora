#!/usr/local/bin/perl

# script to make cab files from activeX build (TestServer/Release)
if($#ARGV<1) {
    print "Usage: perl $0 [debug|release] [testserver|releaseserver] [language] [rebuild]\n";
    print "\t[Opt[#]/debug|release] specifies build type\n"
    	. "\t[testserver|releaseserver] specifies target server type\n"
		. "\t[language] specifies region language\n";
#    print "\t[rebuild] runs {ppremake,make cleanall,make} for specified build & server type\n";
    exit(1);
}

sub check_exist() {
   $filename = shift;
   if(!(-e $filename)) {
      die "$filename does not exist!\n";
   }
}

$argnum = 0;
$build_type =  $ARGV[$argnum++];
$server_type = $ARGV[$argnum++];
$language = $ARGV[$argnum++];
if ($argnum <= $#ARGV) {
   $do_rebuild = $ARGV[$argnum++];
}

# relative *_DIR paths assume it is run from ~/toontown/installer/installertoontown/activex

$ACTIVEX_NAME="ttinst";
if($server_type eq 'testserver') {
   $ACTIVEX_NAME="tt_test";
   $BUILD_SUFFIX="-test";
   $TESTSERVER_NAME = " TestServer";
}

if ($language && ($language ne 'english')) {
   $BUILD_SUFFIX = "$BUILD_SUFFIX-$language";
   $ACTIVEX_NAME= "$ACTIVEX_NAME-$language";
}

$OPTNUM="4";
if(($build_type eq 'debug') || ($build_type eq '1')) {
   $OPTNUM=1;
   $ENV{'PANDA_OPTIMIZE'}='1';
} elsif(($build_type eq 'release') || ($build_type eq '4')) {
   $OPTNUM=4;
   $ENV{'PANDA_OPTIMIZE'}='4';
} elsif ($build_type eq '2') {
   $OPTNUM=$build_type;
   $ENV{'PANDA_OPTIMIZE'}=$build_type;
} elsif ($build_type eq '3') {
   $OPTNUM=$build_type;
   $ENV{'PANDA_OPTIMIZE'}=$build_type;
}

$odir_platform="Cygwin";
if($ENV{'PPREMAKE_PLATFORM'} ne '')  {
$odir_platform=$ENV{'PPREMAKE_PLATFORM'};
}
# mimic what's in dtool/Config.pp defn of ODIR
$BUILD_DIR = "Opt".$OPTNUM."-".$odir_platform.$BUILD_SUFFIX;

&check_exist($BUILD_DIR);
&check_exist($BUILD_DIR."/".$ACTIVEX_NAME.".dll");
&check_exist($BUILD_DIR."/".$ACTIVEX_NAME.".inf");

# must cd to output dir because cabarc always encodes full relative paths, and we dont want any paths
# in the cab archives, should just be the flat file list
# otherwise unpack will fail when subdirs dont exist

chdir($BUILD_DIR);

# g: should be \\mover\vol01\fat\bit
$SIGN_DIR="$ENV{WINTOOLS}/sdk/ms_platform_sdk/Bin";
$VERISIGN_DIR="//cred.wdig.com/verisign_credentials/WaltDisneyCompany";
#$VERISIGN_DIR="//sesrccdfile01.woc.prod.<something>/verisign_credentials/WaltDisneyCompany";

#unlink("$ACTIVEX_NAME.cab");

chdir("..");
system("make -f vista.mk");
exit(0);

$signname = '';
if ($language ne 'english') {
	$signname = ' '. ucfirst($language);
}

$cab_cmd="$SIGN_DIR/Cabarc -s 6144 n $ACTIVEX_NAME.cab $ACTIVEX_NAME.dll $ACTIVEX_NAME.inf";
$sign_cmd="$SIGN_DIR/signcode -spc $VERISIGN_DIR/mycredentials.spc -v $VERISIGN_DIR/myprivatekey.pvk -n \"Toontown$TESTSERVER_NAME Installer$signname\" -t http://timestamp.verisign.com/scripts/timstamp.dll $ACTIVEX_NAME.cab";
print "$cab_cmd\n";
$retval=system($cab_cmd);
if($retval!=0) {
  die "Error creating $ACTIVEX_NAME.cab\n";
}
print "$sign_cmd\n";
$retval=system($sign_cmd);
if($retval!=0) {
  print "Error signing $ACTIVEX_NAME.cab\n";
}
chdir("..");
