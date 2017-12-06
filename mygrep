#!/usr/bin/perl

=head1 NAME

 mygrep - Perl grep, a grep using Perl regular expressions

=head1 SYNOPSIS

 mygrep [-Ehilncmrtvz] [-[Ff] regex] [-p regex] [-s #] <regex> [filename...]

=head1 OPTIONS

 -E Print Examples coming from Expert users
 -h Print this help message
 -i Ignore upper/lower case distinction during comparisons.
 -l Print only the names of files with matching lines, separated by 
    NEWLINE characters. Does not repeat the names of files when the 
    pattern is found more than once.
 -n Precede each line by its line number in the file (first line is 1).
 -c Precede each match by its byte offset in the file (first offset is 0).
 -m Show only the matched part of string, i.e., $& in the Perl expression
 -r Search directories recusively
 -s # Select and print only the #-th match (can be range) in the file
 -t Search text files only
 -v Print all lines except those that contain the pattern
 -z Files that are compressed or gziped will be uncompressed before
    searching

The following options are only useful in conjunction with the C<-r> option:

 -f regex Search only files that match regex
 -F regex Same as option -f, but case sensitive
 -p regex `prune', i.e., do not examine any directories or files in the
           directory structure below the directory matching regex (case
           sensitive).

=head1 DESCRIPTION

The program searches files for a pattern and prints all lines that contain
that pattern. Instead of the standard regular expressions, the program uses
Perl regular expressions.

Be careful using the characters $, *,  [, ^, |, (, ),  and \ because they
are also meaningful  to the shell.  It  is  safest to enclose  the entire
regular-expression in single quotes '...'.

If no files are specified, standard  input is assumed.  Normally, each line
found is copied to  standard output.  The file name  is printed before each
line found if there is more than one input file.

<regex> is a Perl regular expression. This means you have to quote all
special characters: +?.*^$()[]{}|\

The C<-s> option prints only the n-th match in the file(s). You can specify a
range as an argument to C<-s> or you can specify multiple occurences. The
following example prints the first ten matches of "^Subject" from the mbox file:

 $ mygrep -s 1-10 ^Subject mbox

The next example prints only the 1th, 3rd and 20th match of "^Subject" from the
mbox file:

 $ mygrep -s 1,3,20 ^Subject mbox

Mixing of both `,' and `-' is not yet implemented!

Other examples:

If you want to find the string $Id: in all your RCS sources, but
you don't want to search the files below the RCS directories, use:

 $ mygrep -r -p RCS '\$Id:' ~/Sources

A second example searches all FORTRAN files (ending with .for) for the
occurence of TBTOPN. Also, from the search pattern we see that comment lines
(starting with [Cc]) are rejected. The search is case insensitive and we want
only the names of the files that match (option C<-l>).

 $ mygrep -rli -F "\.for$" "^[^Cc].*TBTOPN" .

=head1 EXAMPLES FOR THE C<-m> OPTION

The option C<-m> is useful for searching a binary file. If you search binary
files with the normal grep program, you get complete garbage on your screen if
there is a match because a line for grep is everything until a newline
character. You obviously only want to see the matched part of this garbage.

Suppose you want to search a FITS file for the keyword FILENAME and the value:

 $ mygrep -m "FILENAME= '[^']+'" <FITS file...>

The output will only contain the matched part, e.g.,

 FILENAME= 'SWER07200660'

If you want to look for more than one pattern, you can use the `|' operator for
Perl regular expressions:

 $ mygrep -m "FILENAME= '[^']+'|OBJECT  = '[^']+'" *

The output will then look something like:

 swer07200660.fits.0504:FILENAME= 'SWER07200660'
 swer07200660.fits.0504:OBJECT  = 'HD100546'
 swer10400424.fits.0538:FILENAME= 'SWER10400424'
 swer10400424.fits.0538:OBJECT  = 'HD104237'

=head2 A few more examples on `C<-m>'

Find all words and/or sentences longer than three characters.  Be careful,
only alphanumeric characters and spaces are matched in this example.

  $ mygrep -m "[\w\s]{4,}" <file...>

Emulate the unix `C<strings>' command

  $ mygrep -m "[\040-\176]{4,}" <file...>

=head1 IMPLEMENTATION

For all possible combinations of options, the program first builds three
sorts of Perl code:

=over 3

=item 1.

Output code which is stored in the variable $output_code. This string
contains the Perl source to print the matched line.

=item 2.

Open code which is stored in the variable $ope_code. This string
contains the Perl source to open each file. If the option C<-z> is
specified, the file is opened through a pipe from gzip.

=item 3.

Wanted code which is stored in the variable $wanted_code. This string
contains the Perl source for the search engine and open the files using
$wanted_code;

=back

If the option C<-r> is specified, this Perl code is called using the function
find() from the module File::Find.

If the option C<-r> is not specified, all the files are specified on the
commandline or lines are read from STDIN or a pipe. In this case, the above
Perl code is called directly by the program.

=head1 AUTHOR

Rik Huygen (rik dot huygen at kuleuven dot be)

=head1 VERSION

 $Id: mygrep,v 1.17 1998/02/17 08:56:50 rik Exp rik $

=cut

use Getopt::Std;
use File::Find;
use File::Basename;

getopt ('spfF');

($program = $0) =~ s#^.*/##;

$usage = <<__USAGE__;

Perl grep, a grep using Perl regular expressions and allow recursive search

usage: $program [-Ehilncmrtvz] [-[Ff] regex] [-p regex] [-s #]
             <regex> [filename...]

  -E Print Examples coming from Expert users
  -h Print this help message
  -i Ignore upper/lower case distinction during comparisons.
  -l Print only the names of files with matching lines, separated by NEWLINE
     characters.  Does not repeat the names of files when the pattern is found
     more than once.
  -n Precede each line by its line number in the file (first line is 1).
  -c Precede each match by its byte offset in the file (first offset is 0).
  -m Show only the matched part of string, i.e., \$& in the Perl expression
  -r Search directories recusively
  -s # Select and print only the #-th match (can be range) in the file
  -t Search text files only
  -v Print all lines except those that contain the pattern
  -z Files that are compressed or gziped will be uncompressed before searching

  The following options are only useful in conjunction with the -r option:

  -f regex Search only files that match regex
  -F regex Same as option -f, but case sensitive
  -p regex `prune', i.e., do not examine any directories or files in the
           directory structure below the directory matching regex (case
           sensitive).

  <regex> is a Perl regular expression. This means you have to quote all special
  characters: \+\?\.\*\^\$\(\)\[\]\{\}\|\\

  For example, if you want to find the string \$Id: in all your RCS sources, but
  you don't want to search the files below the RCS directories, use:

    \$ $program -r -p RCS '\\\$Id:' ~/Sources

  A second example searches all FORTRAN files (ending with .for) for the
  occurence of TBTOPN. Also, from the search pattern we see that comment lines
  (starting with [Cc]) are rejected. The search is case insensitive and we want
  only the names of the files that match (option -l).

    \$ $program -rli -F "\.for\$" "^[^Cc].*TBTOPN" .

__USAGE__

$examples = <<__EXAMPLES__;

EXAMPLES FOR THE -s OPTION

The -s option prints only the n-th match in the file(s). You can specify a range
as an argument to -s or you can specify multiple occurences. The following
example prints the first ten matches of "^Subject" from the mbox file:

 $ mygrep -s 1-10 ^Subject mbox

The next example prints only the 1th, 3rd and 20th match of "^Subject" from the
mbox file:

 $ mygrep -s 1,3,20 ^Subject mbox

Mixing of both `,' and `-' is not yet implemented!

EXAMPLES FOR THE -m OPTION

The option -m is useful for searching a binary file. If you search binary files
with the normal grep program, you get complete garbage on your screen if there
is a match because a line for grep is everything until a newline character. You
obviously only want to see the matched part of this garbage.

Suppose you want to search a FITS file for the keyword FILENAME and the value:

  \$ $program -m "FILENAME= '[^']+'" <FITS file...>

The output will only contain the matched part, e.g.,

  FILENAME= 'SWER07200660'

If you want to look for more than one pattern, you can use the `|' operator for
Perl regular expressions:

  \$ $program -m "FILENAME= '[^']+'|OBJECT  = '[^']+'" *

The output will then look something like:

  swer07200660.fits.0504:FILENAME= 'SWER07200660'
  swer07200660.fits.0504:OBJECT  = 'HD100546'
  swer10400424.fits.0538:FILENAME= 'SWER10400424'
  swer10400424.fits.0538:OBJECT  = 'HD104237'

A few more examples on `-m':

  # Find all words and/or sentences longer than three characters.  Be careful,
  # only alphanumeric characters and spaces are matched in this example.
  \$ $program -m "[\\w\\s]{4,}" <file...>

  # Emulate the unix `strings' command
  \$ $program -m "[\\040-\\176]{4,}" <file...>

__EXAMPLES__

die $usage if $opt_h;
die $examples if $opt_E;

$pattern = shift @ARGV;
$pattern =~ s/!/\\!/g;          # protect the delimiter in the regexp

die $usage unless $pattern;

$lineno  = 0;
$flags   = 'o';
$flags  .= 'i' if $opt_i;
$flags  .= 'g' if $opt_m;

@files   = @ARGV ? @ARGV : '-';
$nfiles  = $#files + 1;

$print_fn = 1 if $nfiles > 1 or $opt_r;

$opt_r = 0 unless $opt_r;
$opt_v = 0 unless $opt_v;
$opt_n = 0 unless $opt_n;
$opt_c = 0 unless $opt_c;
$opt_m = 0 unless $opt_m;
$opt_t = 0 unless $opt_t;
$opt_l = 0 unless $opt_l;
$opt_s = 0 unless $opt_s;

if ($opt_F) {
  $files_wanted = $opt_F;
  $fwf = 'o';              # Files Wanted Flag
}

if ($opt_f) {              # Overwrite $opt_F settings!
  $files_wanted = $opt_f;
  $fwf = 'oi';             # Files Wanted Flag
}

warn "WARNING: use a regular expression for options -f and -F, don't start with a '*'!\n"
  if $files_wanted =~ /^\*/;

unless ($opt_F or $opt_f) {
  $files_wanted = ".*";
  $fwf = 'o';
}

build_output_code ();
#  print "Begin Output Code\n";
#  print $output_code;
#  print "End Output Code\n";

build_open_code ();
#  print "Begin Open Code\n";
#  print $open_code;
#  print "End Open Code\n";

build_wanted_code ();
#  print "Begin Wanted Code\n";
#  print $wanted_code;
#  print "End Wanted Code\n";


if ( $opt_r ) {
  find (\&wanted, @files);
}
else {
  foreach ( @files ) {

    next if $opt_t and -B;

    $name = $_;
    $dir = '.';

    eval $wanted_code;
    die $@ if $@;
  }
}

# ------------------------------ SERVICE ROUTINES ------------------------------

sub max {
  my (@values) = @_;
  my ($max) = 0;

  foreach ( @values ) {
    $max = $_ if $_ > $max;
  }
  $max;
}

sub build_output_code {

  # $oline is the output line generated from $line.

  # And what about a combination of `,' and `-'?
  # How to implement the option: -s 1-10,15 ?

  if ($opt_s =~ /[\-]/) {
    ($min, $max) = split (/[\-]/, $opt_s);
    $last = " if \$match >= $min and \$match <= $max; last if \$match > $max";
  }
  elsif ($opt_s =~ /[\,]/) {
    @to_match = split (/[\,]/, $opt_s);
    $max = max (@to_match);
    $last = " if grep ((\$match == \$_), \@to_match); last if \$match > $max";
  }
  elsif ($opt_s) {
    $last = ", last if \$match == $opt_s;";
  }

  SWITCH: {
    if ($opt_l) {
      $output_code = <<"      __END_CODE__";
        print "\$name\\n";
        last;                 # only print filename once if match
      __END_CODE__
      last SWITCH;
    }

    if ($print_fn and $opt_n) {
      $output_code = <<"      __END_CODE__";
        \$match++;
        print ("\$name:\$lineno:\$oline") $last;
      __END_CODE__
      last SWITCH;
    }

    if ($print_fn) {
      $output_code = <<"      __END_CODE__";
        \$match++;
        print ("\$name:\$oline") $last;
      __END_CODE__
      last SWITCH;
    }

    if ($opt_n) {
      $output_code = <<"      __END_CODE__";
        \$match++;
        print ("\$lineno:\$oline") $last;
      __END_CODE__
      last SWITCH;
    }

    if ($opt_c) {
      $output_code = <<"      __END_CODE__";
        \$match++;
        print ("\$offset:\$oline") $last;
      __END_CODE__
      last SWITCH;
    }

    $output_code = <<"    __END_CODE__";
      \$match++;
      print ("\$oline") $last;
    __END_CODE__
    
  }
}

sub build_open_code {

  if ($opt_z) {
    $open_code = <<"    __END_CODE__";
      if ( /\\.(gz|tgz|Z)/o ) {
        open (FILE, "gzip -dc \$_ |") or do {
          warn "$program: Can't gzip and open \$name: \$!\\n";
          return;
        };
      }
      else {
        open (FILE, \$_) or do {
          warn "$program: Can't open \$name: \$!\\n";
          return;
        };
      }
    __END_CODE__
  }
  else {
    $open_code =  <<"      __END_CODE__";
      open (FILE, \$_) or do {
        warn "$program: Can't open \$name: \$!\\n";
        return;
      };
      __END_CODE__
  }
}

sub build_wanted_code {

  $wanted_code = <<"  __END_CODE__";

    return unless \$name =~ /$files_wanted/$fwf;

    unless ( -d ) {

      $open_code;

      \$lineno = 0;
      \$match = 0;
      \$_offset = 0 if $opt_c;
      while (\$line = <FILE>) {

        \$lineno++;
        \$_offset += length (\$line);

        if ( $opt_m ) {
          while (\$line =~ m!$pattern!$flags) {
            \$oline = "\$&\n";
            \$offset = \$_offset - length (\$&.\$');
            unless ( $opt_v ) {
              $output_code;
            };
          }
        }
        else {
          if ( \$line =~ m!$pattern!$flags ) {
            unless ( $opt_v ) {
              \$oline = \$line;
              $output_code;
            };
          }
          elsif ( $opt_v ) {
            \$oline = \$line;
            $output_code;
          }
        }
      }

      close FILE;
    }

  __END_CODE__

}

sub wanted {

  return if $opt_t and -B;

  local ($line);
  local ($name) = $File::Find::name;
  local ($dir)  = $File::Find::dir;

  if (basename ($dir) =~ /$opt_p/) {
    $prune = $File::Find::prune = 1;
  }
  else {
    $prune = $File::Find::prune = 0;
  }

  eval $wanted_code unless $prune;
  die $@ if $@;
}

# ----------------------------------- EOF -----------------------------------
