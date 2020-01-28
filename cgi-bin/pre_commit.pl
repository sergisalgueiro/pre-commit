#!/usr/bin/perl -w

use warnings;
use strict;

use CGI;

my $cgi = CGI->new();
print $cgi->header('application/json');
my $commitDescription = $cgi->param('log');
my $commitFiles = $cgi->param('changed');
my @files = qw(version.var hardware.hw);
my $lock = 0;

if (not defined $commitDescription or $commitDescription eq '')
{
        print "{\"action\":\"deny\", \"reason\":\"Commit log empty\"}\n";
        exit 0;
}

if ( grep($commitFiles =~ /$_/, @files ) ) 
{
    $lock = 1;
}
else
{
    $lock = 0;
}

if ($lock)
{
    if ($commitDescription =~ /I know what I\'m doing/)
    {
            print "{\"action\":\"allow\"}\n";
    }
    else
    {
            print "{\"action\":\"deny\", \"reason\":\"You are trying to commit dangerous files: [@files]. Remove them from commit,\n or type \"I know what I\'m doing\" in the commit log\"}\n";
    }
}
else
{
    print "{\"action\":\"allow\"}\n";
}
exit 0;
