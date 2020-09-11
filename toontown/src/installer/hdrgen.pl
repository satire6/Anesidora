#!/usr/local/bin/perl

# pre-build script to generate ActiveX installer files based on build type (TestServer/Release)
# build_type should be 'test' or 'release'
if($#ARGV<1) {
    print "Usage: perl $0 [BUILD_TYPE] [FILE_TYPE] [output_dir] [language]\n";
    exit(1);
}

$argnum=0;
$case_insensitive = 0;

$build_type =  $ARGV[$argnum++];
$file_type = $ARGV[$argnum++];
$output_dir = $ARGV[$argnum++];
$language = $ARGV[$argnum++];

if (! $language) {
    print "defaulting to ENGLISH language\n";
    $language = 'english';
}

$make_rc = 0;
$make_idl = 0;
$make_inf = 0;
$make_rgs = 0;
$make_ver_hdr = 0;

if($file_type eq 'all') {
  $make_rc = 1;
  $make_idl = 1;
  $make_inf = 1;
  $make_rgs = 1;
  $make_ver_hdr = 1;
} elsif($file_type eq 'inf') {
  $make_inf = 1;
} elsif($file_type eq 'rc') {
  $make_rc = 1;
} elsif($file_type eq 'ver_h') {
  $make_ver_hdr = 1;
} elsif($file_type eq 'rgs') {
  $make_rgs = 1;
} elsif($file_type eq 'idl') {
  $make_idl = 1;
} else {
  die "unrecognized file_type argument: $file_type\n";
}

$ver_filename = 'version.txt';
$basename="installer";

$rc_template_file=$basename."_template.rc";
$rc_output_file=$output_dir."\\".$basename.".rc";

$rgs_template_file=$basename."_template.rgs";
$rgs_output_file=$output_dir."\\".$basename.".rgs";

$idl_template_file=$basename."_template.idl";
$idl_output_file=$output_dir."\\".$basename.".idl";

$inf_template_file=$basename."_template.inf";

$ver_hdr_template_file = $basename."Version_template.h";
$ver_hdr_output_file = $output_dir."\\".$basename."Version.h";

if($build_type eq 'test') {
  $version_description = "Toontown TestServer Installer Module";
  $ttinst_name = "tt_test";
  $ttinst_iconfilename="toontown.ico";

  $InstallerCtrlInterface_guid="B76AF6CD-935F-4cc2-BC88-3DB5B066C7A7";
  $InstallerCtrl_TypeLib_guid="27CD518F-635E-45de-B0E3-BF43C13402C7";
  $InstallerCtrl_guid="FF791555-FDAC-43ab-B792-389E4CC0A6E5";
  $InstallerCtrl_helpstr="Toontown TestServer Installer Control";

  # this is what user sees in explorer
  $rgs_controlname="Toontown TestServer Installer ActiveX Control";

  if ($language && $language ne 'english') {
      print "\n********\nWARNING: non-English test ActiveX not supported!\n********\n\n";
      exit(-1);
  }
  
} else {
  $version_description = 'Toontown IE Module';
  $ttinst_iconfilename='minnie.ico';
  $InstallerCtrl_helpstr='Toontown Installer Control';
  $ttinst_name = 'ttinst';

  # this is what user sees in explorer
  $rgs_controlname="Toontown IE Helper";

  if ($language && $language ne 'english') {
    $ttinst_name .= "-$language";
    $version_description .= ' ' . ucfirst($language);
    $InstallerCtrl_helpstr .= ' '. ucfirst($language);
    $rgs_controlname .= ' '. ucfirst($language);
  }

  if ($language eq 'castillian') {
    $InstallerCtrlInterface_guid='09D1BDC5-0BF2-4235-B888-7D8BAD8FCBC6';
    $InstallerCtrl_TypeLib_guid='95A38B48-9E36-41d2-964C-2E9CCC2CE6B6';
    $InstallerCtrl_guid='F9669F87-7B97-41fb-85FA-597C58FDE7BE';
  }
  elsif ($language eq 'japanese') {
    $InstallerCtrlInterface_guid='7B4EE901-D405-45f7-8B69-042D9F3C4DBC';
    $InstallerCtrl_TypeLib_guid='7444B902-8DDF-4dc9-88A6-13BAB2BD3225';
    $InstallerCtrl_guid='E76AABC4-07F4-47c3-BC55-B16119A793CF';
  }
  elsif ($language eq 'german') {
    $InstallerCtrlInterface_guid='E1779D0B-DE27-4c4a-B656-828A061C7029';
    $InstallerCtrl_TypeLib_guid='C3B84B6D-1E84-4c3c-88C2-695557F30DA0';
    $InstallerCtrl_guid='95BD7A59-567A-4fe1-A412-FCEC29428E42';
  }
  elsif ($language eq 'portuguese') {
    $InstallerCtrlInterface_guid='A4C3733E-5FA0-419f-8156-B577D557761B';
    $InstallerCtrl_TypeLib_guid='9CCE9A38-1821-42e9-B6D0-2EA00AF03FD9';
    $InstallerCtrl_guid='31CB2F01-72C2-4cf4-B265-450E8817B039';
  }
  elsif ($language eq 'french') {
    $InstallerCtrlInterface_guid='9C830340-C0C9-44d8-A7A1-A28CC585A792';
    $InstallerCtrl_TypeLib_guid='FD094E16-BFCA-4230-ADF8-071D53BA04C4';
    $InstallerCtrl_guid='63308B48-F435-42fd-AB0A-3564C7BEF9D7';
  }
  else { # English
    $InstallerCtrlInterface_guid="0D3CB678-6C50-4D6C-BA4E-602AAEAD0FDF";
    $InstallerCtrl_TypeLib_guid="A24C823E-A1BD-4C03-972E-1B1D715B8397";
    $InstallerCtrl_guid="C02226EB-A5D7-4B1F-BD7E-635E46C2288D";
  }
}

# since these files exist in user dir, dont want to change existing name,
# and dont want name to conflict with each other, so user different ones
# for test&release & different regions
$ttinst_filename = "$ttinst_name.dll";
$inf_output_file = "$output_dir\\$ttinst_name.inf";

my $verstr = '';
open VERFILE, $ver_filename or die "can't read ".$ver_filename." $!";
while(<VERFILE>) {
  chomp;
  $_ =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)(\s+(\w+))*/;
  #
  # $1 = 1, $2 = deployment, $3 = feature version, $4 = buildnum
  # $6 = language/deployment
  #
  if ($6 eq $language) {
    $verstr = "$1.$2.$3.$4";

    $installerver_A = $1;
    $installerver_B = $2;
    $installerver_C = $3;
    $installerver_D = $4;
    break;
  }
}
close VERFILE;

$verstr_commas = $verstr;
$verstr_commas =~ s/\./\,/g;

if(!(-e $output_dir)) {
   mkdir($output_dir,0755);
}

if ($make_rc) {
   ################  RC FILE ###################

   print "writing $verstr $rc_output_file\n";

   open IN, $rc_template_file or die "can't read ".$rc_template_file." $!";
   open OUT, ">$rc_output_file" or die "can't create ".$rc_output_file.": $!";
   binmode IN;
   binmode OUT;

   while(<IN>) {
      s/VERNUM_COMMA_SEPARATORS/$verstr_commas/g;
      s/TTINST_FILENAME/$ttinst_filename/g;
      s/TTINST_FILE_DESCRIPTION/$version_description/g;
      s/TTINST_ICONFILENAME/$ttinst_iconfilename/g;
      print OUT;
   }

   close OUT;
   close IN;
}

if ($make_ver_hdr) {
   ################  installerVersion.h FILE ###################

   print "writing $verstr $ver_hdr_output_file\n";
   open IN, $ver_hdr_template_file or die "can't read ".$ver_hdr_template_file." $!";
   open OUT, ">$ver_hdr_output_file" or die "can't create ".$ver_hdr_output_file.": $!";
   binmode IN;
   binmode OUT;

   while(<IN>) {
      s/INSTALLERVER_A/$installerver_A/g;
      s/INSTALLERVER_B/$installerver_B/g;
      s/INSTALLERVER_C/$installerver_C/g;
      s/INSTALLERVER_D/$installerver_D/g;
      print OUT;
   }

   close OUT;
   close IN;
}

if ($make_idl) {
      ################  IDL FILE ###################

      open IN, $idl_template_file or die "can't read ".$idl_template_file." $!";
      open OUT, ">$idl_output_file" or die "can't create ".$idl_output_file.": $!";
      binmode IN;
      binmode OUT;

      print "writing $verstr $idl_output_file\n";

      while(<IN>) {
         s/INSTALLERCTRL_INTERFACEGUID/$InstallerCtrlInterface_guid/g;
         s/INSTALLERCTRL_TYPELIBGUID/$InstallerCtrl_TypeLib_guid/g;
         s/INSTALLERCTRL_GUID/$InstallerCtrl_guid/g;
         s/INSTALLERCTRL_HELPSTR/$InstallerCtrl_helpstr/g;
         print OUT;
      }

      close OUT;
      close IN;
}

if ($make_rgs) {
      ################  RGS FILE ###################
      open IN, $rgs_template_file or die "can't read ".$rgs_template_file." $!";
      open OUT, ">$rgs_output_file" or die "can't create ".$rgs_output_file.": $!";
      binmode IN;
      binmode OUT;

      print "writing $verstr $rgs_output_file\n";

      while(<IN>) {
         s/INSTALLERCTRL_TYPELIBGUID/$InstallerCtrl_TypeLib_guid/g;
         s/INSTALLERCTRL_GUID/$InstallerCtrl_guid/g;
         s/ACTIVEX_CONTROLNAME/$rgs_controlname/g;
         print OUT;
      }

      close OUT;
      close IN;
}

if ($make_inf) {
   ################  INF FILE ###################
   open IN, $inf_template_file or die "can't read ".$inf_template_file." $!";
   open OUT, ">$inf_output_file" or die "can't create ".$inf_output_file.": $!";
   binmode IN;
   binmode OUT;

   print "writing $verstr $inf_output_file\n";

   while(<IN>) {
      s/VERNUM_COMMA_SEPARATORS/$verstr_commas/g;
      s/TTINST_FILENAME/$ttinst_filename/g;
      s/INSTALLERCTRL_GUID/$InstallerCtrl_guid/g;
      print OUT;
   }

   close OUT;
   close IN;
}

