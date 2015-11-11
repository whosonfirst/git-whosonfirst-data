# git-whosonfirst-data

Git related utilities for Who's On First Data

## Git hooks

### pre-commit

Validate and format documents before commiting them, updating the relevant [placetype-specific meta files](https://github.com/whosonfirst/whosonfirst-data/tree/master/meta) along the way. For example:

```
$> git commit -m "add inception date" .
INFO:root:invoking git-whosonfirst-mapzen pre-commit hooks
INFO:root:validating /usr/local/data/whosonfirst-data/data/102/061/079/102061079.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/102/061/079/102061079.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/102/061/079/102061079.geojson
INFO:root:rebuild meta file for placetype neighbourhood with one update
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-neighbourhood-20151111.csv to /usr/local/data/whosonfirst-data/meta/wof-neighbourhood-latest.csv
[master 40de3d2] add inception date
 3 files changed, 4 insertions(+), 4 deletions(-)
```

To install the pre-commit hook you will need to copy (or symlink) the [hooks/pre-commit](hooks/pre-commit) file to the `.git/hooks` folder in your copy of [whosonfirst-data](https://github.com/whosonfirst/whosonfirst-data). For example:

```
$> ln -s /usr/local/mapzen/git-whosonfirst-data/hooks/pre-commit /usr/local/mapzen/whosonfirst-data/.git/hooks/pre-commit
```

## See also

* https://github.com/whosonfirst/whosonfirst-data