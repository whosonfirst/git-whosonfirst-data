#!/usr/bin/env python
# -*-python-*-

"""
$> cat .changed-* | sort | uniq | grep geojson | ./lib/wof/validate.py -r `pwd`
INFO:root:validating /usr/local/data/whosonfirst-data/data/101/723/183/101723183.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/101/748/047/101748047.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/101/750/467/101750467.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/327/15/85632715.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/811/39/85681139.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/811/47/85681147.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/817/33/85681733.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/858/685/17/85868517.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/859/309/05/85930905.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/859/361/77/85936177.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/859/369/89/85936989.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/859/475/23/85947523.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/859/726/99/85972699.geojson
INFO:root:all done
"""

import os
import sys
import logging
import StringIO

import mapzen.whosonfirst.validator

def validate_files(root, files):

    vld = mapzen.whosonfirst.validator.validator()
    
    for rel_path in files:
        
        abs_path = os.path.join(root, rel_path)
        logging.info("validating %s" % abs_path)
        
        rpt = vld.validate_file(abs_path)
        
        if not rpt.ok():
            
            logging.error("%s FAILED validation test" % abs_path)
            
            # sudo make the following less bad...
            # (20151111/thisisaaronland)
            
            fh = StringIO.StringIO()
            rpt.print_report(fh)
            fh.seek(0)
            
            logging.error("validation report is:\n%s" % "".join(fh.readlines()))
            return False

    return True
            

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

    if not validate_files(root, files):
        sys.exit(1)
         
    logging.info("all done")
    sys.exit(0)
