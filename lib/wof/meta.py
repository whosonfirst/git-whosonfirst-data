#!/usr/bin/env python
# -*-python-*-

"""
cat .changed-* | sort | uniq | grep geojson | ./wof-update-metafiles -r `pwd`
INFO:root:rebuild meta file for placetype country with one update
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-country-20160512.csv to /usr/local/data/whosonfirst-data/meta/wof-country-latest.csv
INFO:root:rebuild meta file for placetype region with 3 updates
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-region-20160512.csv to /usr/local/data/whosonfirst-data/meta/wof-region-latest.csv
INFO:root:rebuild meta file for placetype neighbourhood with one update
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-neighbourhood-20160512.csv to /usr/local/data/whosonfirst-data/meta/wof-neighbourhood-latest.csv
INFO:root:rebuild meta file for placetype locality with 8 updates
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-locality-20160512.csv to /usr/local/data/whosonfirst-data/meta/wof-locality-latest.csv
INFO:root:modified: /usr/local/data/whosonfirst-data/meta/wof-country-latest.csv;/usr/local/data/whosonfirst-data/meta/wof-region-latest.csv;/usr/local/data/whosonfirst-data/meta/w\
of-neighbourhood-latest.csv;/usr/local/data/whosonfirst-data/meta/wof-locality-latest.csv
INFO:root:created: /usr/local/data/whosonfirst-data/meta/wof-country-20160512.csv;/usr/local/data/whosonfirst-data/meta/wof-region-20160512.csv;/usr/local/data/whosonfirst-data/met\
a/wof-neighbourhood-20160512.csv;/usr/local/data/whosonfirst-data/meta/wof-locality-20160512.csv
INFO:root:all done
"""

import os
import sys
import logging
import StringIO

import mapzen.whosonfirst.utils

def update_metafiles(root, files):

    data = os.path.join(root, "data")
    meta = os.path.join(root, "meta")
    
    meta_kwargs = {
        'paths': 'relative',
        'prefix': data,
    }

    return mapzen.whosonfirst.utils.update_placetype_metafiles(meta, files, **meta_kwargs)

if __name__ == '__main__':

    import optparse
    opt_parser = optparse.OptionParser()
    
    opt_parser.add_option('-r', '--repo', dest='repo', action='store', default=None, help='')
    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')

    options, files = opt_parser.parse_args()

    if options.verbose:	
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if len(files) == 0:
        
        for ln in sys.stdin:
            ln = ln.strip()
            files.append(ln)

    repo = options.repo
    root = os.path.abspath(repo)

    modified, created = update_metafiles(root, files)

    logging.info("modified: %s" % ";".join(modified))
    logging.info("created: %s" % ";".join(created))

    # where to send output... if at all?

    logging.info("all done")
    sys.exit(0)
