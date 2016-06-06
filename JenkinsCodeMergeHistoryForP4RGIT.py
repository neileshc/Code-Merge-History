#!/usr/bin/env python
"""
SYNOPSIS

    Script to fetch the commit history for GIT repo and Perforce in HTML

DESCRIPTION

    This script fetches the commit history for given repo from GIT and Perforce with Jenkins as
    CI system. This script can be called from Jenkins with passing simple parameters such as Repo
    name and the time since when you wnat to pull in history and generates HTML file.

AUTHOR

    Neilesh Chorkhalikar (cns.nilesh@gmail.com)

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    1.0.0
"""

import os
import time
import sys
import csv
import string

a = time.strftime("%Y/%m/%d")
workspace = os.environ['WORKSPACE'] if ('WORKSPACE' in os.environ) else ''
sinceHours = os.environ['SINCE_HOURS'] if ('SINCE_HOURS' in os.environ) else ''
gitRepoHistory = 'git log --date=relative --pretty="%%an, %%cn, %%cr, %%H, %%s" --since="since %s hours ago" >> Repo.csv' % (sinceHours)

def convertCsvToHtml(csvName):
    with open(csvName, 'r') as f:
        # Open the CSV file for reading
        reader = csv.reader(f)
        Changes = 0
        for row in reader:
            Changes += 1

        if Changes > 2:
            print "Totol Changes merged : %d" %Changes
        else:
            print "No changes merged"
            return

        f.seek(0)
        # Create the HTML file for output
        htmlfile = open(workspace+'/Result.html',"a")

        # initialize rownum variable
        rownum = 0

        htmlfile.write('<style>')
        htmlfile.write('table { ')
        htmlfile.write('display: table;')
        htmlfile.write('border-collapse: separate;')
        htmlfile.write('border-spacing: 0px;')
        htmlfile.write('border-color: green;')
        htmlfile.write('}')
        htmlfile.write('</style>')

        # write <table> tag
        htmlfile.write('<table border="1">')
        htmlfile.write('<br>')

        # generate table contents
        for row in reader: # Read a single row from the CSV file

        # write header row. assumes first row in csv contains header
            if rownum <= 1:
                htmlfile.write('<tr>') # write <tr> tag
                if rownum == 1:
                    htmlfile.write('<td bgcolor="grey">' + 'S. No.' + '</td>')
                else:
                    htmlfile.write('<td>' + '' + '</td>')
                for column in row:
                    if rownum == 0:
                        htmlfile.write('<td colspan="5" align="center" bgcolor="grey">' + column + '</td>')
                    else:
                        htmlfile.write('<th bgcolor="grey">' + column + '</th>')
                htmlfile.write('</tr>')

            #write all other rows
            else:
                htmlfile.write('<tr>')
                htmlfile.write('<td align="center">' + str(rownum-1) + '</td>')
                for column in row:
                    htmlfile.write('<td align="center">' + column + '</td>')
                htmlfile.write('</tr>')

            #increment row count
            rownum += 1

    htmlfile.write('<br>')
    # write </table> tag
    htmlfile.write('</table>')
    # print results to shell
    print "Created " + str(rownum) + " row table."
    return

os.chdir(workspace+'/Repo')
os.system('echo Repo Client Merges >> Repo.csv')
os.system('echo Author, +2Reviewer, Merged, Hash, Commit_details >> Repo.csv')
os.system(gitRepoHistory)
convertCsvToHtml('Repo.csv');

os.chdir(workspace)
os.system('echo Perforce Check ins Repo >> P4Repo.csv')
os.system('echo CL Details >> P4Repo.csv')
os.system('p4 changes -s submitted //Repo/...@'+a+':00:00:00,@now >> P4Repo.csv')
convertCsvToHtml('P4Repo.csv');
