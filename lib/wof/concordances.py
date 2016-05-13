#!/usr/bin/env python
# -*-python-*-

"""
cat .changed-* | sort | uniq | grep geojson | ./wof-update-concordances -r `pwd`
INFO:root:count updated: 13 count updated w/ updated concordances: 0
INFO:root:all done
"""

import os
import sys
import logging

import mapzen.whosonfirst.utils
import mapzen.whosonfirst.diff

def update_concordances(root, files):

    data = os.path.join(root, "data")
    meta = os.path.join(root, "meta")
    
    diff = mapzen.whosonfirst.diff.compare(source=root)
    updated_concordances = []
    
    for path in files:
        
        path = os.path.abspath(path)
        
        id, ignore = mapzen.whosonfirst.utils.parse_filename(path)
        
        try:
            report = diff.report(id)
            
            if report['concordances'] == True:
                updated_concordances.append(path)
                
        except Exception, e:
            logging.warning("failed to generate report for %s, because %s" % (path, e))

    logging.info("count updated: %d count updated w/ updated concordances: %d" % (len(files), len(updated_concordances)))

    modified = []
    created = []

    if len(updated_concordances):
       
        concordances_kwargs = {
            'paths': 'relative',
            'prefix': data,
        }
        
        modified, created = mapzen.whosonfirst.utils.update_concordances_metafile(meta, updated_concordances, **concordances_kwargs)

    return modified, created

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

    modified, created = update_concordances(root, files)
        
    # where to send output... if at all?

    logging.info("all done")
    sys.exit(0)
