
# for processing logs created by installer data passed to hardware.php

# need a test-coverage mode and a config survey mode

$logfilename=$ARGV[0];

if($logfilename eq '') {
   $logfilename = "hardware.log";
}

if(!(-e $logfilename)) {
  die "input log '".$logfilename."' doesnt exist!\n";
}

sub ignored_field() {
  $name = $_[0];
  if($name eq 'Date') {   # string itself only for humans to read in 1 rec
     return 1;
  }

  return 0;
}

$recstart_marker = "---start-of-hardware---";
$recend_marker = "---end---";
open (LOGFILE, $logfilename) or die "Unable to open ".$logfilename." for reading!";

print "Reading logfile: ",$logfilename,"\n";

$reccnt=0;
$rec_added=0;
$skipped_disney=0;
$skipped_same=0;
$skipped_other=0;

for(;1;) {  # perl's do-until loops dont like 'last' and 'next' for some weird reason (see dox)
  $line = <LOGFILE>;
  if(!$line) {
     last;
  }

chop($line);
if($line eq '') {
    next;
}

if($line =~ /^$recstart_marker$/) {
     $reccnt++;

     # read in 1 record

     @curfields=();
     $curIP = "Unknown";
     $curMACAddr = "Unknown";
     $curAccountName = "Unknown";
     $numLogins = 0;

     for(;1;) {
        # first read in whole record, then see if we already have an entry for this IP-MAC id
        $line = <LOGFILE>;
        chop($line);

        if($line eq '') {
           next;
        }

        if((!$line) || ($line =~ /^$recend_marker$/)) {
           last;
        }

        # hack, eventually this field will disappear
        if($line =~ /^User Agent/) {
           next;
        }

        # hack, eventually this field will disappear
        if($line =~ /^IP\:/) {
           next;
        }


        # make sure fnames have no whitespace or this wont work!
        if(!($line =~ /^(\S+)\:(.*)$/)) {
           die "badly formatted line: ".$line."\n";
        }

        my $fieldname = $1;
        my $linetail = $2;

        my $fieldvalue = '';

        if($linetail =~ /^(\S)$/) {
           # make sure this pattern matches 1char fieldval correctly as well as regular case!
           $fieldvalue = $1;
           goto FOUNDFIELDS;  # no elseif
        }

        if($linetail =~ /^\s*$/) {
           # empty fieldval
           # $fieldvalue = '';
           goto FOUNDFIELDS;
        }

        if($linetail =~ /^(\s*)(\S+.*\S+)(\s*)$/) {
           $fieldvalue = $2;
        } else {
            die "badly formatted linetail: ".$linetail."\n";
        }

        FOUNDFIELDS:

        if(&ignored_field($fieldname)) {
           next;
        }

        if($fieldname eq 'IPAddr') {
           $curIP = $fieldvalue;
           #next;  cant skip this, need to enter it to detect dup recs
        }
        if($fieldname eq 'MACAddr') {
           $curMACAddr = $fieldvalue;
           #next;  cant skip this, need to enter it to detect dup recs
        }

        if($fieldname eq 'AccountName') {
           $curAccountName = $fieldvalue;
           # next;  AccountName should be number of logins I guess
        } 
           
        if($fieldname eq 'NumLogins') {
           $curNumLogins = $fieldvalue;
           next;
        } 
           
        if($fieldname eq 'VideoRamBytes') {
            # just store MB val
            $fieldvalue=&RoundUpToPow2($fieldvalue) >> 20;  #slow?
        } 

        if($fieldname eq 'GfxApiUsedID') {
            # fix installer bug, sometimes outputs bogus value for 'unknown' 0
            if($fieldvalue>10) {
              $fieldvalue=0;
            }
        }

        push @curfields,($fieldname,$fieldvalue);
     }
     #print "@curfields\n";

     # for now, just take 1 entry from a given pc

     # for testing coverage purposes, want to include disney pcs.
     # for customer hw surveys, want to exclude them

     if($curIP =~ /^10\.196\.143+/) {
         #print "skipping VR machine: ".$curIP.", AccountName: ".$curAccountName."\n";
         $skipped_disney++;
         next;
     }
     if($curIP =~ /^10\.196+/) {
         #print "skipping disney machine: ".$curIP.", AccountName: ".$curAccountName."\n";
         $skipped_disney++;
         next;
     }

     $recID="$curIP.$curMACAddr";
     if($recID eq '.') {
        # IPAddr and MAC address were empty, so just merge all account records I guess
        # bad if they're using from 2 diffferent machines w/same loginname, you ignore 2nd machine
        $recID=$curAccountName;
        if($recID eq '') {
           $skipped_other++;
           print "skipping un-IDable record #".$reccnt."\n";
           next;
        }
     }
     # update accounts map
     $accounts{$recID}=($curAccountName,$accounts{$recID}[1]+$curNumLogins);

     # skipping is really only correct for reporting about certain fields that dont change over multiple runs.
     # errorcodes may change of course.  need to handle those I suppose
     if(defined($machines{$recID})) {
         # print "skipping duplicate record for recID: ".$recID."\n";
         $skipped_same++;
         next;
     } else {
        # indicate which machines we've already processed
        $machines{$recID}=1;
     }

     $recs_added++;

     # add fieldvals to map

     for($i=0;$i<=$#curfields;$i=$i+2)
     {
        my $fieldname =  $curfields[$i];
        my $fieldvalue = $curfields[$i+1];

        if(defined($fields{$fieldname}{$fieldvalue})) {
           $curcount=$fields{$fieldname}{$fieldvalue};
           $curcount=$curcount+1;
           $fields{$fieldname}{$fieldvalue}=$curcount;
        } else {
           $fields{$fieldname}{$fieldvalue}=1;
        }
        # print $fieldname."[".$fieldname."]=".$fields{$fieldname}{$fieldvalue}."\n";
     }
   }

#otherwise is the line blank or garbage b/w records?
# just for dbg
#if($reccnt>10) { last; }
}
close(LOGFILE);
print "Processed ".$reccnt." records\n";
print "Discarded ".($skipped_same)." same-machine records and ".$skipped_disney." disney-machine records\n";
if($skipped_other>0) {
   print "Discarded ".$skipped_other." other records\n";
}
$total_usedrecs=$reccnt-$skipped_same-$skipped_disney-$skipped_other;
print "These stats are for remaining ".$total_usedrecs." recs.\n";

## now print out a report for each field

# prints out whole DB!!
#while ( ($key, $value) = each %fields) {
#       print "$key = $value\n";
#       while ( ($key2, $value2) = each %{$value}) {
#               print "$key2 = $value2\n";
#       }
#    }

#sub printbinaryfield() {
#   $fieldname = $_[0];
#
#   print $fieldname.":\n";
#   $truecnt=$fields{$fieldname}{1};
#   $falsecnt=$fields{$fieldname}{0};
#   printf "\tYes:  %7d  %10.1f%\n",$truecnt,($truecnt/$total_usedrecs)*100;
#   printf "\tNo:   %7d  %10.1f%\n",$falsecnt,($falsecnt/$total_usedrecs)*100;
#   print "\n";
#}

# for fields with a relative small possible # of values
sub printfield {
   $fieldname = $_[0];
   $fieldtype = $_[1];
   $sorttype = $_[2];
   $sortorder = $_[3];
   $valnamemap = $_[4];
   $title = $_[5];
   $valnamemap_usehexkeys = $_[7];

   @fieldwidths = @{$_[6]};
   $fname_width = '';
   $fcnt_width = '';
   $fpct_width = '';
   #print "fieldwidths=@fieldwidths\n";
   if(@fieldwidths ne '') {
     $fname_width = @fieldwidths->[0];  #for this one, really need a option to compute max length of keystr
     $fcnt_width =  @fieldwidths->[1];
     $fpct_width =  @fieldwidths->[2];
     #print "xxx fname_width=".@fieldwidths->[0].", fcnt_width=".@fieldwidths->[1].", fpct_width=".@fieldwidths->[2]."\n";
   }
   if($fname_width eq '') {
     $fname_width = 20;
   }
   if($fcnt_width eq '') {
     $fcnt_width = 7;
   }
   if($fpct_width eq '') {
      $fpct_width = 10;
   }

   #print "fname_width=".$fname_width.", fcnt_width=".$fcnt_width.", fpct_width=".$fpct_width."\n";

   # fieldtype should be 'i' or 's'
   # sorttype should be 'val' or 'key'
   # sortorder should be 'highcountfirst' or 'strorder'
   # valnamemap should be a hashtable or null
   #$valnamemap_usehexkeys: if 1, valnamemap keys are hex strs that need to be converted to ints before using

   if($title eq '') {
      $title = $fieldname;
   }

   print "\n=============================\n";
   print "$title:\n";

   @Vals = ();

   if($sortorder eq 'strorder') {
      # sort using strcmps, so '55' < '7', etc
      # sort in inverse order by default, so "z" first, then "a"
      if($sorttype eq 'key') {
         @Vals = sort (keys %{$fields{$fieldname}});
      } else {
         @Vals = sort { $fields{$fieldname}{$b} cmp $fields{$fieldname}{$a} }
                      keys %{$fields{$fieldname}};
      }
   } else {
      # sort treating values as integers, highest first so 55 > 7
      if($sorttype eq 'key') {
         die "error, cant sort highcountfirst by keys since keys are always strings!";
      }

      # <=> is a -1,0,1 sort cmp func for integers

      @Vals = sort { $fields{$fieldname}{$b} <=> $fields{$fieldname}{$a} }
                      keys %{$fields{$fieldname}};
   }

   foreach my $val (@Vals) {
      $cnt = $fields{$fieldname}{$val};

      if($valnamemap ne '') {
         $vkey = $val;
         if($valnamemap_usehexkeys) {
            $vkey=hex($val);
         }

         if(defined(${$valnamemap}{$vkey})) {
            $valname = ${$valnamemap}{$vkey};
         } else {
            $valname = "Unknown";
         }

         $val=$valname." (".$val.")";
      }

      $pf_fmtstr="%".$fname_width.$fieldtype." %".$fcnt_width."d %".$fpct_width.".2f%\n";
      #print "pf_fmtstr=".$pf_fmtstr."\n";

      printf $pf_fmtstr,$val,$cnt,($cnt/$total_usedrecs)*100;
   }
}

sub MakeRoundedField() {
   my $fieldname=$_[0];
   my $rndfieldname=$_[0]."Rounded";
   my $round_chunksize=$_[1];

   # see http://www.perldoc.com/perl5.6/pod/perlreftut.html
   # round float to nearest 64MB boundary for categorization

   $sumtotal=0;
   $totalentries=0;

   # sort by int val is done to facilitate median computation traversal
   # <=> is a -1,0,1 sort cmp func for integers
   @Vals = sort { $a <=> $b }
               keys %{$fields{$fieldname}};

   #print "@Vals\n";

   foreach my $val (@Vals) {

      my $tmp = $val/$round_chunksize;
      my $rounded_val = int(0.5 + $tmp)*$round_chunksize;
      $origval_count = $fields{$fieldname}{$val};
      $sumtotal+=$val*$origval_count;
      $totalentries+=$origval_count;

      if(defined($fields{$rndfieldname}{$rounded_val})) {
         $fields{$rndfieldname}{$rounded_val}+=$origval_count;
      } else {
         $fields{$rndfieldname}{$rounded_val}=$origval_count;
      }
   }

   $averages{$fieldname}=int(0.5+($sumtotal/$totalentries));
   #print "avg=".$averages{$fieldname}."\n";

   $median_entrynum=$totalentries/2;
   $num_entries_traversed=0;
   foreach my $val (@Vals) {
      $origval_count = $fields{$fieldname}{$val};
      $num_entries_traversed+=$origval_count;
      if($num_entries_traversed>=$median_entrynum) {
          $medians{$fieldname}=$val;
          last;
      }
   }
}

sub ComputeAverageandMedian() {
   my $fieldname=$_[0];

   # see http://www.perldoc.com/perl5.6/pod/perlreftut.html
   # round float to nearest 64MB boundary for categorization

   $sumtotal=0;
   $totalentries=0;

   # sort by int val is done to facilitate median computation traversal
   # <=> is a -1,0,1 sort cmp func for integers
   @Vals = sort { $a <=> $b }
               keys %{$fields{$fieldname}};

   #print "@Vals\n";

   foreach my $val (@Vals) {
      $origval_count = $fields{$fieldname}{$val};
      $sumtotal+=$val*$origval_count;
      $totalentries+=$origval_count;
   }

   $averages{$fieldname}=$sumtotal/$totalentries;
   #print "avg=".$averages{$fieldname}."\n";


   # have to do a 2nd traversal for median computation, since we dont know $totalentries until after 1st pass
   $median_entrynum=$totalentries/2;
   $num_entries_traversed=0;
   foreach my $val (@Vals) {
      $origval_count = $fields{$fieldname}{$val};
      $num_entries_traversed+=$origval_count;
      if($num_entries_traversed>=$median_entrynum) {
          $medians{$fieldname}=$val;
          last;
      }
   }
}

sub RoundUpToPow2() {
   my $val=$_[0];

   if(($val & ($val-1))==0) {
      return $val;
   } else {
          $tmpval = $val;
          # if it's it's not already a pow-of-2
          #find the high '1', or compute log(n)  # see http://groups.google.com/groups?hl=en&lr=&ie=UTF-8&selm=6ncl5p%24f5q%241%40cscnews.csc.calpoly.edu&rnum=1
          $i = 0;
          if(($tmpval & 0xffff0000)){
             $i = 16;
             $tmpval >>= 16;
          }

          if($tmpval & 0xFF00) {
             $i |= 8;
             $tmpval >>= 8;
          }

          if($tmpval & 0xF0) {
             $i |= 4;
             $tmpval >>= 4;
          }

          if($tmpval & 0xC) {
             $i |= 2;
             $tmpval >>= 2;
          }

          $highbitpos = ($i | ($tmpval >> 1));
          return (1 << ($highbitpos+1));
   }
}

print "\n*** Report for non-disney machines ***\n\n";

&inittables();

&MakeRoundedField('RamMegsTotal',64);
&MakeRoundedField('CpuMhz',100);
&MakeRoundedField('DiskSpaceMegsFree',1000);

&printfield('LangID','s','val','highcountfirst', {%langIDmap}, 'Languages',[40,'',''],1);
&printfield('LocaleID','s','val','highcountfirst', {%langIDmap}, 'Locales',[40,'',''],1);
&printfield('KeyboardLayout','s','val','highcountfirst', {%langIDmap}, 'Keyboard Layouts',[40,'',''],1);
&printfield('NumMonitors','i','val');
&printfield('NumCpus','i','val');
&printfield('VideoCardVendorIDHex','s','val', 'highcountfirst', {%vidcardvendornames}, 'VideoCard Vendors');
&printfield('VideoCardName','s','val', 'highcountfirst','','VideoCard Name',[50,'','']);
&printfield('UsingLAN','s','val','strorder',{%yesnostrmap},'Using high-speed network connection');
&printfield('UserIsAdmin','s','val','strorder',{%yesnostrmap},'User is NT Administrator');
&printfield('UsingHTTPProxy','s','val','strorder',{%yesnostrmap},'Using HTTP Proxy Server');
&printfield('IsPaid','s','val','strorder',{%yesnostrmap},'Is Paid User');
&printfield('OSID','s','val','highcountfirst',{%OSIDnames},'Operating Systems');
&printfield('OS','s','val','highcountfirst','','OS Full Name',[64,5,6]);
&printfield('DXInstalledVer','s','val','highcountfirst','','DirectX Version Installed');
&printfield('IEVersion','s','val','highcountfirst','','IE Version');
&printfield('GfxApiSuggestedID','s','val','highcountfirst',{%GAPInames},'Graphics API suggested by Installer');
&printfield('GfxApiUsedID','s','val','highcountfirst',{%GAPInames},'Graphics API being used');

&printfield('LastScreenMode','s','val','highcountfirst','','Last Screen Mode Used');  # this was buggy in test DB
&printfield('CpuMaker','s','val');
&printfield('CpuType','s','val');

&printfield('RamMegsTotalRounded','s','val','highcountfirst','','Total Machine RAM Megabytes');
printf "\n%20s %7d MB\n","Average RAM:",$averages{'RamMegsTotal'};
printf "%20s %7d MB\n","Median RAM:",$medians{'RamMegsTotal'};

&printfield('CpuMhzRounded','s','val',,'highcountfirst','','CPU Mhz');
printf "\n%20s %7d Mhz\n","Average CPU Mhz:",$averages{'CpuMhz'};
printf "%20s %7d Mhz\n","Median CPU Mhz:",$medians{'CpuMhz'};


&printfield('DiskSpaceMegsFreeRounded','s','val',,'highcountfirst','','Disk Space Free (in Megabytes)');
printf "\n%20s %7.1f Gigs\n","Average Disk Space Free:",$averages{'DiskSpaceMegsFree'}/1000;
printf "%20s %7.1f Gigs\n","Median Disk Space Free:",$medians{'DiskSpaceMegsFree'}/1000;

# need to use only the driver file name, perhaps?
#&printfield('MidiOutDevices','s','val');
#&printfield('DSoundDevices','s','val');


&ComputeAverageandMedian('VideoRamBytes');
&printfield('VideoRamBytes','s','val',,'highcountfirst','','Video RAM (in Megabytes)');
printf "\n%20s %7d MB\n","Average Video RAM:",$averages{'VideoRamBytes'};
printf "%20s %7d MB\n","Median Video RAM:",$medians{'VideoRamBytes'};


&printfield('VideoCardDriverDateYear','s','val');

# need test-coverage mode to tabulate these.  these make no sense per machine?  per run?
#FinalNonErrorState:0
#InstallerErrorPnt:0
#PandaErrorCode:0


sub inittables {

%yesnostrmap = ( 1 => "Yes", 0 => "No", );

%langIDmap = (
0x0000 => "Language Neutral",
0x007f => "LOCALE_INVARIANT Lang",
0x0400 => "Process or User Default Language",
0x0800 => "System Default Language",
0x0436 => "Afrikaans",
0x041c => "Albanian",
0x0401 => "Arabic (Saudi Arabia)",
0x0801 => "Arabic (Iraq)",
0x0c01 => "Arabic (Egypt)",
0x1001 => "Arabic (Libya)",
0x1401 => "Arabic (Algeria)",
0x1801 => "Arabic (Morocco)",
0x1c01 => "Arabic (Tunisia)",
0x2001 => "Arabic (Oman)",
0x2401 => "Arabic (Yemen)",
0x2801 => "Arabic (Syria)",
0x2c01 => "Arabic (Jordan)",
0x3001 => "Arabic (Lebanon)",
0x3401 => "Arabic (Kuwait)",
0x3801 => "Arabic (U.A.E.)",
0x3c01 => "Arabic (Bahrain)",
0x4001 => "Arabic (Qatar)",
0x042b => "Armenian",
0x042c => "Azeri (Latin)",
0x082c => "Azeri (Cyrillic)",
0x042d => "Basque",
0x0423 => "Belarusian",
0x0402 => "Bulgarian",
0x0455 => "Burmese",
0x0403 => "Catalan",
0x0404 => "Chinese (Taiwan)",
0x0804 => "Chinese (PRC)",
0x0c04 => "Chinese (Hong Kong SAR, PRC)",
0x1004 => "Chinese (Singapore)",
0x1404 => "Chinese (Macau SAR)",
0x041a => "Croatian",
0x0405 => "Czech",
0x0406 => "Danish",
0x0465 => "Divehi",
0x0413 => "Dutch (Netherlands)",
0x0813 => "Dutch (Belgium)",
0x0409 => "English (United States)",
0x0809 => "English (United Kingdom)",
0x0c09 => "English (Australian)",
0x1009 => "English (Canadian)",
0x1409 => "English (New Zealand)",
0x1809 => "English (Ireland)",
0x1c09 => "English (South Africa)",
0x2009 => "English (Jamaica)",
0x2409 => "English (Caribbean)",
0x2809 => "English (Belize)",
0x2c09 => "English (Trinidad)",
0x3009 => "English (Zimbabwe)",
0x3409 => "English (Philippines)",
0x0425 => "Estonian",
0x0438 => "Faeroese",
0x0429 => "Farsi",
0x040b => "Finnish",
0x040c => "French (Standard)",
0x080c => "French (Belgian)",
0x0c0c => "French (Canadian)",
0x100c => "French (Switzerland)",
0x140c => "French (Luxembourg)",
0x180c => "French (Monaco)",
0x0456 => "Galician",
0x0437 => "Georgian",
0x0407 => "German (Standard)",
0x0807 => "German (Switzerland)",
0x0c07 => "German (Austria)",
0x1007 => "German (Luxembourg)",
0x1407 => "German (Liechtenstein)",
0x0408 => "Greek",
0x0447 => "Gujarati",
0x040d => "Hebrew",
0x0439 => "Hindi",
0x040e => "Hungarian",
0x040f => "Icelandic",
0x0421 => "Indonesian",
0x0410 => "Italian (Standard)",
0x0810 => "Italian (Switzerland)",
0x0411 => "Japanese",
0x044b => "Kannada",
0x0457 => "Konkani",
0x0412 => "Korean",
0x0812 => "Korean",
0x0440 => "Kyrgyz",
0x0426 => "Latvian",
0x0427 => "Lithuanian",
0x0827 => "Lithuanian (Classic)",
0x042f => "FYRO Macedonian",
0x043e => "Malay (Malaysian)",
0x083e => "Malay (Brunei Darussalam)",
0x044e => "Marathi",
0x0450 => "Mongolian",
0x0414 => "Norwegian (Bokmal)",
0x0814 => "Norwegian (Nynorsk)",
0x0415 => "Polish",
0x0416 => "Portuguese (Brazil)",
0x0816 => "Portuguese (Portugal)",
0x0446 => "Punjabi",
0x0418 => "Romanian",
0x0419 => "Russian",
0x044f => "Sanskrit",
0x0c1a => "Serbian (Cyrillic)",
0x081a => "Serbian (Latin)",
0x041b => "Slovak",
0x0424 => "Slovenian",
0x040a => "Spanish (Spain, Traditional Sort)",
0x080a => "Spanish (Mexican)",
0x0c0a => "Spanish (Spain, Modern Sort)",
0x100a => "Spanish (Guatemala)",
0x140a => "Spanish (Costa Rica)",
0x180a => "Spanish (Panama)",
0x1c0a => "Spanish (Dominican Republic)",
0x200a => "Spanish (Venezuela)",
0x240a => "Spanish (Colombia)",
0x280a => "Spanish (Peru)",
0x2c0a => "Spanish (Argentina)",
0x300a => "Spanish (Ecuador)",
0x340a => "Spanish (Chile)",
0x380a => "Spanish (Uruguay)",
0x3c0a => "Spanish (Paraguay)",
0x400a => "Spanish (Bolivia)",
0x440a => "Spanish (El Salvador)",
0x480a => "Spanish (Honduras)",
0x4c0a => "Spanish (Nicaragua)",
0x500a => "Spanish (Puerto Rico)",
0x0430 => "Sutu",
0x0441 => "Swahili (Kenya)",
0x041d => "Swedish",
0x081d => "Swedish (Finland)",
0x045a => "Syriac",
0x0449 => "Tamil",
0x0444 => "Tatar (Tatarstan)",
0x044a => "Telugu",
0x041e => "Thai",
0x041f => "Turkish",
0x0422 => "Ukrainian",
0x0420 => "Urdu (Pakistan)",
0x0820 => "Urdu (India)",
0x0443 => "Uzbek (Latin)",
0x0843 => "Uzbek (Cyrillic)",
0x042a => "Vietnamese",
);

%vidcardvendoraliases = ('0x12D2' => "0x10DE");


# will this work for multiple aliases, or just eval the last item in list?
%vidcardvendoraliases_reverse = ("0x10DE",('0x12D2'));

%vidcardvendornames = (  '0x10DE' => "Nvidia",
                         '0x104A' => "PowerVR",
                         '0x5333' => "S3",
                         '0x102B' => "Matrox",
                         '0x1039' => "SiS",
                         '0x8086' => "Intel",
                         '0x12D2' => "Nvidia (STB)",
                         '0x121A' => "3Dfx",
                         '0x3D3D' => "3D Labs",
                         '0x1002' => "ATI",
                         '0x1023' => "Trident",
                         '0x14AF' => "Guillemot",  # ship kyro and nvidia, at least
                         '0x1102' => "Creative Labs",  # ?
                         '0x1163' => "Rendition",
                         '0x1013' => "Cirrus Logic",
                         '0x104C' => "Texas Instr.",  # usually alias 4 3d labs permedia?
                         );

# from installer/sysinfodefs.h
%OSIDnames = (  '0' => 'Unknown',
                '1' => 'Windows 95',
                '2' => 'Windows 98',
                '3' => 'Windows ME',
                '4' => 'Windows NT',
                '5' => 'Windows 2000',
                '6' => 'Windows XP',
                '7' => 'Windows Server 2003'
                );
%GAPInames = ( '0' => 'Unknown',
               '1' => 'OpenGL',
               '3' => 'DirectX 3',
               '5' => 'DirectX 5',
               '6' => 'DirectX 6',
               '7' => 'DirectX 7.0',
               '8' => 'DirectX 8.0',
               '9' => 'DirectX 8.1',
              '10' => 'DirectX 9',
           );
}

