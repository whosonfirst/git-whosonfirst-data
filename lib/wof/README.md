# shared tools

_This is wet paint. Proceed with caution._

## dot-changed files

These are generated by the `post-merge` commit hook.

```
$> ls -a ./.changed-*

.changed-7b3124c08ea67dc2db88f513e75cc1d2491563c2-3cee3a1dae437ac1f428617c00c55e9c76832162
.changed-7b3124c08ea67dc2db88f513e75cc1d2491563c2-827deccdfdf6801a21c76d4cbbec41a04bf6b14e
.changed-7b3124c08ea67dc2db88f513e75cc1d2491563c2-a0dfe77330c8115b6326ac5f0904fdbe33a8d67f
.changed-ee52452c2ee73a3fc49d545932703e78885bc351-0e4974d28b688cff3ae53ebc7ce1e44c5de0ea6a
.changed-ee52452c2ee73a3fc49d545932703e78885bc351-adee0dbd797c1ab58061aad93485c3d3cabcc9ea
.changed-ee52452c2ee73a3fc49d545932703e78885bc351-d9bb5c65687783ab866b7e26b4bfcf9424dc1476
```

## dot-changed files (de-duped)

```
$> cat .changed-* | sort | uniq | grep geojson 

data/101/723/183/101723183.geojson
data/101/748/047/101748047.geojson
data/101/750/467/101750467.geojson
data/856/327/15/85632715.geojson
data/856/811/39/85681139.geojson
data/856/811/47/85681147.geojson
data/856/817/33/85681733.geojson
data/858/685/17/85868517.geojson
data/859/309/05/85930905.geojson
data/859/361/77/85936177.geojson
data/859/369/89/85936989.geojson
data/859/475/23/85947523.geojson
data/859/726/99/85972699.geojson
```

## validating files

```
$> cat .changed-* | sort | uniq | grep geojson | /path/to/git-whosonfirst-data/lib/wof/validate.py -r `pwd`

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
```

Or

```
import sys
sys.append("/path/to/git-whosonfirst-data/lib")

import wof.validate
ok = wof.validate.validate_files(repo, files)
```

## updating meta files

```
$> cat .changed-* | sort | uniq | grep geojson | /path/to/git-whosonfirst-data/lib/wof/meta.py -r `pwd`

INFO:root:rebuild meta file for placetype country with one update
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-country-20160512.csv to /usr/local/data/whosonfirst-data/meta/wof-country-latest.csv
INFO:root:rebuild meta file for placetype region with 3 updates
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-region-20160512.csv to /usr/local/data/whosonfirst-data/meta/wof-region-latest.csv
INFO:root:rebuild meta file for placetype neighbourhood with one update
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-neighbourhood-20160512.csv to /usr/local/data/whosonfirst-data/meta/wof-neighbourhood-latest.csv
INFO:root:rebuild meta file for placetype locality with 8 updates
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-locality-20160512.csv to /usr/local/data/whosonfirst-data/meta/wof-locality-latest.csv
INFO:root:modified: /usr/local/data/whosonfirst-data/meta/wof-country-latest.csv;/usr/local/data/whosonfirst-data/meta/wof-region-latest.csv;/usr/local/data/whosonfirst-data/meta/wof-neighbourhood-latest.csv;/usr/local/data/whosonfirst-data/meta/wof-locality-latest.csv
INFO:root:created: /usr/local/data/whosonfirst-data/meta/wof-country-20160512.csv;/usr/local/data/whosonfirst-data/meta/wof-region-20160512.csv;/usr/local/data/whosonfirst-data/meta/wof-neighbourhood-20160512.csv;/usr/local/data/whosonfirst-data/meta/wof-locality-20160512.csv
INFO:root:all done
```

Or:

```
import sys
sys.append("/path/to/git-whosonfirst-data/lib")

import wof.meta
modified, created = wof.meta.update_metafiles(repo, files)
```

## updating concordances

```
$> cat .changed-* | sort | uniq | grep geojson | /path/to/git-whosonfirst-data/lib/wof/concordances.py -r `pwd`

INFO:root:count updated: 13 count updated w/ updated concordances: 0
INFO:root:all done
```

Or:

```
import sys
sys.append("/path/to/git-whosonfirst-data/lib")

import wof.concordances
modified, created = wof.concordances.update_concordances(repo, files)
```

## syncing to S3

```
$> cat .changed-* | sort | uniq | grep geojson | /path/to/git-whosonfirst-data/lib/wof/s3.py -r `pwd` -c /path/to/git-whosonfirst-data/hooks/hooks.cfg -S /path/to/wof-sync-files

INFO:root:launched with PID 2553
[wof-sync-files] 22:19:26.685129 [info] creating a new Sync thing-y with 200 processes
[wof-sync-files] 22:19:26.694070 [info] Scheduled 0 Completed 0 Success 0 Error 0 Skipped 0 Retried 0 Goroutines 207 Time 48.113
µs
```

Or:

```
import sys
sys.append("/path/to/git-whosonfirst-data/lib")

import ConfigParser
import wof.s3

sync_tool='/path/to/wof-sync-files'
cfg = ConfigParser.read(...)

pid = wof.s3.sync_files(root, files, sync_tool, cfg)
```

## syncing to ES (Elasticsearch)

```
$> cat .changed-* | sort | uniq | grep geojson | /path/to/git-whosonfirst-data/lib/wof/es.py -r `pwd` -c /path/to/git-whosonfirst-data/hooks/hooks.cfg -S /path/to/wof-es-index-filelist

INFO:root:getting ready to /path/to/git-whosonfirst-data/bin/linux/wof-es-index-filelist --host 9.9.9.9 --port 9200 --tidy /tmp/tmpzjGb3B
INFO:root:launched with PID 1488
WARNING:root:remove tag 'ne:fips_10_' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:gdp_md_est' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:geou_dif' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:pop_est' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:su_dif' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:adm0_dif' because ES suffers from E_EXCESSIVE_CLEVERNESS
WARNING:root:remove tag 'ne:level' because ES suffers from E_EXCESSIVE_CLEVERNESS
```

Or:

```
import sys
sys.append("/path/to/git-whosonfirst-data/lib")

import ConfigParser
import wof.es

index_tool='/path/to/wof-es-index-filelist'
cfg = ConfigParser.read(...)

pid = wof.es.index_files(root, files, index_tool, cfg)
```

## updating bundle files

```
$> cat .changed-* | sort | uniq | grep geojson | /path/to/git-whosonfirst-data/lib/wof/bundles.py -r `pwd` -c /path/to/git-whosonfirst-data/hooks/hooks.cfg -B /path/to/git-whosonfirst-data/bin/linux/wof-bundle-placetypes -C /path/to/git-whosonfirst-data/bin/linux/wof-clone-metafiles

INFO:root:getting ready to /path/to/git-whosonfirst-data/bin/linux/wof-bundle-placetypes -s /usr/local/data/whosonfirst-data -d /usr/local/data/whosonfirst-bundles -S lat\
est --wof-clone /path/to/git-whosonfirst-data/bin/linux/wof-clone-metafiles --aws-bucket whosonfirst.mapzen.com
INFO:root:launched with PID 3628
/usr/local/data/whosonfirst-data$ INFO:root:bundle dependency (latest)
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
INFO:root:['/path/to/git-whosonfirst-data/bin/linux/wof-clone-metafiles', '-source', 'file:///usr/local/data/whosonfirst-data/data', '-dest', '/usr/local/data/whosonfirst-bundles/wof-localadmin-latest-bundle/data', '/usr/local/data/whosonfirst-data/meta/wof-localadmin-latest.csv']
[wof-clone-metafiles] 22:47:39.685526 [info] scheduled: 1442 completed: 1433 success: 1433 error: 0 skipped: 0 to retry: 0 goroutines: 50 time: 999.659469ms

[wof-clone-metafiles] 22:47:40.685731 [info] scheduled: 3393 completed: 3385 success: 3385 error: 0 skipped: 0 to retry: 0 gorou
tines: 48 time: 1.999876812s
[wof-clone-metafiles] 22:47:41.685901 [info] scheduled: 5240 completed: 5233 success: 5233 error: 0 skipped: 0 to retry: 0 goroutines: 49 time: 3.000047008s
[wof-clone-metafiles] 22:47:42.686067 [info] scheduled: 6925 completed: 6909 success: 6909 error: 0 skipped: 0 to retry: 0 goroutines: 59 time: 4.000210415s
[wof-clone-metafiles] 22:47:43.686278 [info] scheduled: 8863 completed: 8851 success: 8851 error: 0 skipped: 0 to retry: 0 goroutines: 52 time: 5.000391587s
[wof-clone-metafiles] 22:47:44.686461 [info] scheduled: 10292 completed: 10288 success: 10288 error: 0 skipped: 0 to retry: 0 goroutines: 44 time: 6.000593192s
[wof-clone-metafiles] 22:47:45.686644 [info] scheduled: 11767 completed: 11754 success: 11754 error: 0 skipped: 0 to retry: 0 goroutines: 54 time: 7.000776242
... and so on
```

Or:

```
import sys
sys.append("/path/to/git-whosonfirst-data/lib")

import ConfigParser
import wof.bundles

bundle_tool='wof-bundle-placetypes'
clone_tool='wof-clone-metafiles'
cfg = ConfigParser.read(...)

pid = wof.bundles.update_bundles(root, bundle_tool, clone_tool, cfg)
```