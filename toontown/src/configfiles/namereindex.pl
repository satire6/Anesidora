#!/usr/local/bin/perl -w
use strict;

my $filename;

die "No file specified\n" unless $filename = $ARGV[0];
open (INFILE, '<:encoding(utf8)', $filename) or die "Can't open $filename for reading\n";
open (OUTFILE, '>:encoding(utf8)', "$filename.sorted");
binmode (STDOUT, ":encoding(iso-8859-1)");
#binmode (STDOUT, ":encoding(utf7)");

my %namelist;
my $isthere;
while(<INFILE>)
{
    # ignore lines starting with #
    if ( $_ =~ /^\s*#/) {
#        print "ignoring $_";
        next;
    }

    chomp;										# remove linefeed
    $_ =~ /^(\d+)\*(\d+)\*(.*?)\s*$/;			# break up into tokens
    #print "index:$1; gender:$2; name:$3\n";
    print "warning: 1 letter name\n" if (length($3) == 1);

    # create list of unique names, with associated gender 
    $isthere = exists($namelist{$3}{$2});

    if (not $isthere)
        { $namelist{$3}{$2} = 1; }
    else
    {
        $namelist{$3}{$2}++;
        print "# warning: duplicate name $3 in class $2 - x",$namelist{$3}{$2},"\n";
    }
}

# convert %namelist into list printable as "gender name", even if name crosses genders
my ($name, %genderlist, $gender, @genders, $genders);
foreach $name (sort keys %namelist) {
    (@genders) = (sort keys %{$namelist{$name}});
    $genders = $#genders;
    foreach $gender (@genders) {
        $genderlist{$gender}{$name} = $genders;        # populate genders with names and duplicate count
    }
}

my ($gcount, $index) = (0,0);
foreach $gender (sort keys %genderlist) {
    foreach $name (sort keys %{$genderlist{$gender}}) {
        print OUTFILE "# warning: cross-gender duplicate\n" if ($genderlist{$gender}{$name} > 1);
        print OUTFILE "# warning: one-letter name\n" if (length($name) == 1);
        print OUTFILE "$index*$gender*$name\n";         # dump it out to file
        $index++;
    }
}
