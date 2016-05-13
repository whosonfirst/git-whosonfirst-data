#!/usr/bin/env python
# -*-python-*-

import os
import sys
import logging
import subprocess
import tempfile

"""
$> cat .changed-* | sort | uniq | grep geojson | /path/to/git-whosonfirst-data/bin/wof/bundles.py -r `pwd` -c /path/to/git-whosonfi\
rst-data/hooks/hooks.cfg -B /path/to/git-whosonfirst-data/bin/linux/wof-bundle-placetypes -C /path/to/git-whosonfirst-data/bin/linux/wof-clone-metafiles
INFO:root:getting ready to /path/to/git-whosonfirst-data/bin/linux/wof-bundle-placetypes -s /usr/local/data/whosonfirst-data -d /usr/local/data/whosonfirst-bundles -S lat\
est --wof-clone /path/to/git-whosonfirst-data/bin/linux/wof-clone-metafiles --aws-bucket whosonfirst.mapzen.com
INFO:root:launched with PID 3628
acope@workhorse-1:/usr/local/data/whosonfirst-data$ INFO:root:bundle dependency (latest)
INFO:root:['sha1sum', '/usr/local/data/whosonfirst-data/meta/wof-dependency-latest.csv']
INFO:root:nothing has changed, skipping wof-dependency-latest-bundle
INFO:root:bundle metroarea (latest)
INFO:root:['sha1sum', '/usr/local/data/whosonfirst-data/meta/wof-metroarea-latest.csv']
INFO:root:nothing has changed, skipping wof-metroarea-latest-bundle
INFO:root:bundle planet (latest)
INFO:root:['sha1sum', '/usr/local/data/whosonfirst-data/meta/wof-planet-latest.csv']
INFO:root:nothing has changed, skipping wof-planet-latest-bundle
INFO:root:bundle address (latest)
INFO:root:['sha1sum', '/usr/local/data/whosonfirst-data/meta/wof-address-latest.csv']
INFO:root:nothing has changed, skipping wof-address-latest-bundle
INFO:root:bundle continent (latest)
INFO:root:['sha1sum', '/usr/local/data/whosonfirst-data/meta/wof-continent-latest.csv']
INFO:root:nothing has changed, skipping wof-continent-latest-bundle
INFO:root:bundle microhood (latest)
INFO:root:['sha1sum', '/usr/local/data/whosonfirst-data/meta/wof-microhood-latest.csv']
INFO:root:nothing has changed, skipping wof-microhood-latest-bundle
INFO:root:bundle borough (latest)
INFO:root:['sha1sum', '/usr/local/data/whosonfirst-data/meta/wof-borough-latest.csv']
INFO:root:nothing has changed, skipping wof-borough-latest-bundle
INFO:root:bundle macrohood (latest)
INFO:root:['sha1sum', '/usr/local/data/whosonfirst-data/meta/wof-macrohood-latest.csv']
INFO:root:nothing has changed, skipping wof-macrohood-latest-bundle
INFO:root:bundle localadmin (latest)
INFO:root:['sha1sum', '/usr/local/data/whosonfirst-data/meta/wof-localadmin-latest.csv']
INFO:root:remove directory /usr/local/data/whosonfirst-bundles/wof-localadmin-latest-bundle
INFO:root:remove file /usr/local/data/whosonfirst-bundles/wof-localadmin-latest-bundle.tar.bz2
INFO:root:mkdir /usr/local/data/whosonfirst-bundles/wof-localadmin-latest-bundle/data
INFO:root:['/path/to/git-whosonfirst-data/bin/linux/wof-clone-metafiles', '-source', 'file:///usr/local/data/whosonfirst-data/data', '-dest', '/usr/local/data/whosonfirst\
-bundles/wof-localadmin-latest-bundle/data', '/usr/local/data/whosonfirst-data/meta/wof-localadmin-latest.csv']
[wof-clone-metafiles] 22:47:39.685526 [info] scheduled: 1442 completed: 1433 success: 1433 error: 0 skipped: 0 to retry: 0 goroutines: 50 time: 999.659469ms

acope@workhorse-1:/usr/local/data/whosonfirst-data$ [wof-clone-metafiles] 22:47:40.685731 [info] scheduled: 3393 completed: 3385 success: 3385 error: 0 skipped: 0 to retry: 0 gorou\
tines: 48 time: 1.999876812s
[wof-clone-metafiles] 22:47:41.685901 [info] scheduled: 5240 completed: 5233 success: 5233 error: 0 skipped: 0 to retry: 0 goroutines: 49 time: 3.000047008s
[wof-clone-metafiles] 22:47:42.686067 [info] scheduled: 6925 completed: 6909 success: 6909 error: 0 skipped: 0 to retry: 0 goroutines: 59 time: 4.000210415s
[wof-clone-metafiles] 22:47:43.686278 [info] scheduled: 8863 completed: 8851 success: 8851 error: 0 skipped: 0 to retry: 0 goroutines: 52 time: 5.000391587s
[wof-clone-metafiles] 22:47:44.686461 [info] scheduled: 10292 completed: 10288 success: 10288 error: 0 skipped: 0 to retry: 0 goroutines: 44 time: 6.000593192s
[wof-clone-metafiles] 22:47:45.686644 [info] scheduled: 11767 completed: 11754 success: 11754 error: 0 skipped: 0 to retry: 0 goroutines: 54 time: 7.000776242
... and so on
"""

def update_bundles(root, bundle_tool, clone_tool, cfg):

    bundle_dest = cfg.get('post-push', 'bundle_dest')
    bundle_dest = os.path.abspath(bundle_dest)
    
    s3_bucket = cfg.get('post-push', 's3_bucket')

    cmd = [
        bundle_tool, 
        "-s", root,
        "-d", bundle_dest,
        "-S", "latest",
        "--wof-clone", clone_tool,
        "--aws-bucket", s3_bucket,
    ]

    s3_credentials = None
    
    if cfg.has_option('post-push', 's3_credentials'):
        s3_crendentials = cfg.get('post-push', 's3_credentials')

    if s3_credentials:
        cmd.extend(["--aws-creds", s3_credentials])
        
    str_cmd = " ".join(cmd)
    logging.info("getting ready to %s" % str_cmd)
    
    p = subprocess.Popen(cmd)
    pid = p.pid
    
    logging.info("launched with PID %s" % (pid))
    return pid

if __name__ == '__main__':
            
    import optparse
    import ConfigParser

    opt_parser = optparse.OptionParser()
    
    opt_parser.add_option('-r', '--repo', dest='repo', action='store', default=None, help='')
    opt_parser.add_option('-c', '--config', dest='config', action='store', default=None, help='')
    opt_parser.add_option('-B', '--bundle-tool', dest='bundle_tool', action='store', default=None, help='')
    opt_parser.add_option('-C', '--clone-tool', dest='clone_tool', action='store', default=None, help='')

    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')

    options, ignore = opt_parser.parse_args()

    if options.verbose:	
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    path_config = os.path.abspath(options.config)

    cfg = ConfigParser.ConfigParser()
    cfg.read(path_config)

    repo = options.repo
    root = os.path.abspath(repo)

    bundle_tool = os.path.abspath(options.bundle_tool)
    clone_tool = os.path.abspath(options.clone_tool)

    update_bundles(root, bundle_tool, clone_tool, cfg)
    sys.exit(0)
