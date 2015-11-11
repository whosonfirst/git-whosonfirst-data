# git-whosonfirst-data

Git related utilities for Who's On First Data

## Git hooks

### pre-commit

Validate and format a document before commiting it.

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

## See also

* https://github.com/whosonfirst/whosonfirst-data