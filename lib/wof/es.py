#!/usr/bin/env python
# -*-python-*-

import os
import sys
import logging
import subprocess
import tempfile

"""
$> cat .changed-* | sort | uniq | grep geojson | /path/to/git-whosonfirst-data/bin/wof/es.py -r `pwd` -c /path/to/git-whosonfirst-data/hooks/hooks.cfg -S /path/to/wof-es-index-filelist
INFO:root:getting ready to /path/to/git-whosonfirst-data/bin/linux/wof-es-index-filelist --host 9.9.9.9 --port 9200 --tidy /tmp/tmpzjGb3B
INFO:root:launched with PID 1488
acope@workhorse-1:/usr/local/data/whosonfirst-data$ WARNING:root:remove tag 'ne:fips_10_' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:gdp_md_est' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:geou_dif' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:pop_est' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:su_dif' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:adm0_dif' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:level' because ES suffers from E_EXCESSIVE_CLEVERNESS
"""

def index_files(root, files, index_tool, cfg):

    es_host = cfg.get('post-push', 'es_host')
    es_port = cfg.get('post-push', 'es_port')
    es_index = cfg.get('post-push', 'es_index')
    
    """
    do_slack = cfg.getboolean('post-push', 'slack')
    slack_config = None
    
    if do_slack and cfg.has_option('post-push', 'slack_config'):
    slack_config = cfg.get('post-push', 'slack_config')
    slack_config = os.path.abspath(slack_config)
    """
    
    fh = tempfile.NamedTemporaryFile(delete=False)
    tmpfile = fh.name
    
    fh.write("\n".join(files))
    fh.close()
    
    cmd = [
        index_tool,
        "--host", es_host,
        "--port", es_port,
        "--index", es_index,
        "--tidy"
    ]

    """
    if do_slack:
    cmd.extend([
    "--slack"
    ])
    
    if slack_config:
    cmd.extend([
    "--slack-config",
    slack_config,
    ])
    """
    
    cmd.append(tmpfile)
    
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
