#!/usr/bin/env python
# -*-python-*-

import os
import sys
import logging
import subprocess
import tempfile

"""
$> cat .changed-* | sort | uniq | grep geojson | /path/to/git-whosonfirst-data/bin/wof/s3.py -r `pwd` -c /path/to/git-whosonfirst-data/hooks/hooks.cfg -S /path/to/wof-sync-files
INFO:root:launched with PID 2553
[wof-sync-files] 22:19:26.685129 [info] creating a new Sync thing-y with 200 processes
acope@workhorse-1:/usr/local/data/whosonfirst-data$ [wof-sync-files] 22:19:26.694070 [info] Scheduled 0 Completed 0 Success 0 Error 0 Skipped 0 Retried 0 Goroutines 207 Time 48.113us
"""

def sync_files(root, files, sync_tool, cfg):

    data = os.path.join(root, "data")

    fh = tempfile.NamedTemporaryFile(delete=False)
    tmpfile = fh.name

    fh.write("\n".join(files))
    fh.close()

    s3_bucket = cfg.get('post-push', 's3_bucket')

    s3_prefix = None
    s3_credentials = None
    
    loglevel = "info"
    tidy = True

    if cfg.has_option('post-push', 's3_prefix'):
        s3_prefix = cfg.get('post-push', 's3_prefix')
                
    if cfg.has_option('post-push', 's3_credentials'):
        s3_crendentials = cfg.get('post-push', 's3_credentials')

    cmd = [
        sync_tool,
        "-bucket", s3_bucket,
        "-root", root,
        "-processes", "200",
        "-file-list", tmpfile,
        "-loglevel", loglevel
    ]

    if tidy:
        cmd.append("-tidy")	# this will unlink tmpfile
    
    if s3_prefix:
        cmd.extend(["-prefix", s3_prefix])
    else:
        cmd.extend(["-prefix", ""])

    if s3_credentials:
        cmd.extend(["-credentials", s3_credentials])
        
    """
    if do_slack:
    cmd.extend([
    "-slack"
    ])
    
    if slack_config:
    cmd.extend([
    "-slack-config",
    slack_config,
    ])
    """

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
    opt_parser.add_option('-S', '--sync-tool', dest='sync_tool', action='store', default=None, help='')

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

    path_config = os.path.abspath(options.config)

    cfg = ConfigParser.ConfigParser()
    cfg.read(path_config)

    repo = options.repo
    root = os.path.abspath(repo)

    sync_tool = os.path.abspath(options.sync_tool)

    sync_files(root, files, sync_tool, cfg)
    sys.exit(0)
