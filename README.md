# git-whosonfirst-data

Git related utilities for Who's On First Data

## Important

This is still very much a work in progress. Depending on when you read these words the code included here might be wonky or even completely broken. It _should_ work as of this writing but I bet you could find a way to make things get weird if you wanted to. Good times.

## Dependencies

Currently this repository lacks a handy script for installing dependencies so you will need to ensure that recent versions of the following are installed:

* https://github.com/whosonfirst/py-mapzen-whosonfirst-utils
* https://github.com/whosonfirst/py-mapzen-whosonfirst-export
* https://github.com/whosonfirst/py-mapzen-whosonfirst-validator
* https://github.com/whosonfirst/py-mapzen-whosonfirst-aws

Having to do this is _not_ a feature. We'll figure something out eventually.

## Install

To install the pre-commit and post-commit hooks you will need to copy both files to the `.git/hooks` folder in your copy of [whosonfirst-data](https://github.com/whosonfirst/whosonfirst-data). You can also symlink them so that updates and changes to the source will take effect immediately. For example:

```
$> ln -s /usr/local/mapzen/git-whosonfirst-data/hooks/pre-commit /usr/local/mapzen/whosonfirst-data/.git/hooks/pre-commit
$> ln -s /usr/local/mapzen/git-whosonfirst-data/hooks/post-commit /usr/local/mapzen/whosonfirst-data/.git/hooks/post-commit
```

## Git hooks

### pre-commit

Validate and format documents before commiting them, updating the relevant [placetype-specific meta files](https://github.com/whosonfirst/whosonfirst-data/tree/master/meta) along the way.


### post-commit

This is the part that will append the updated files (exported WOF documents and meta files) to the current commit. [Because Git](https://stackoverflow.com/questions/3284292/can-a-git-hook-automatically-add-files-to-the-commit) and because the problem started growing yak-hair like a Wookie. _If someone knows a better way to do this please let us know._ Additionally this will attempt to upload the updated WOF documents to a Mapzen / Who's On First (AWS) S3 bucket.

#### it's complicated...

Or rather it will attempt to upload them if the hook thinks it knows [where to find your AWS credentials](http://blogs.aws.amazon.com/security/post/Tx3D6U6WSFGOK2H/A-New-and-Standardized-Way-to-Manage-Credentials-in-the-AWS-SDKs). Or rather it will attempt to upload them _and fail_ unless you have suitable credentials for the bucket. Which is hard-coded to be _out_ bucket. Which is not ideal.

Then again neither is doing transfers as a synchronous and blocking operation during the post-commit phase. All of this still needs to be sorted out (there are lots of [notes and comments in the source code](https://github.com/whosonfirst/git-whosonfirst-data/blob/master/hooks/post-commit) if you're curious) so expect this stuff to change in the short-to-medium term.

### pre-push

We don't define any specific `pre-push` hooks at this point because [git-lfs](https://github.com/whosonfirst/whosonfirst-data/#git-and-large-files) already installs one and I haven't decided how best we should play with it.

### Example

```
$> git commit -m "update more wof:name per issue #164" .
INFO:root:invoking git-whosonfirst-mapzen pre-commit hooks for 31bfc6ac70811258faa2fa8fbbfd7f77910c22f3
INFO:root:processing commit hash 31bfc6ac70811258faa2fa8fbbfd7f77910c22f3
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/819/91/85681991.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/819/91/85681991.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/819/91/85681991.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/819/99/85681999.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/819/99/85681999.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/819/99/85681999.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/820/11/85682011.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/820/11/85682011.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/820/11/85682011.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/820/15/85682015.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/820/15/85682015.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/820/15/85682015.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/820/21/85682021.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/820/21/85682021.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/820/21/85682021.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/820/37/85682037.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/820/37/85682037.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/820/37/85682037.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/820/53/85682053.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/820/53/85682053.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/820/53/85682053.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/821/39/85682139.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/821/39/85682139.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/821/39/85682139.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/821/43/85682143.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/821/43/85682143.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/821/43/85682143.geojson
INFO:root:validating /usr/local/data/whosonfirst-data/data/856/821/49/85682149.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/856/821/49/85682149.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/856/821/49/85682149.geojson
INFO:root:rebuild meta file for placetype region with 10 updates
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-region-20151112.csv to /usr/local/data/whosonfirst-data/meta/wof-region-latest.csv
INFO:root:invoking git-whosonfirst-mapzen post-commit hooks for 7ce339954f26a9b416b57ff9bbd816cf7dcba3ef
INFO:root:/usr/local/data/whosonfirst-data/.commit exists, so I am going to look for files that have been modified
INFO:root:git add data/856/819/91/85681991.geojson data/856/819/99/85681999.geojson data/856/820/11/85682011.geojson data/856/820/15/85682015.geojson data/856/820/21/85682021.geojson data/856/820/37/85682037.geojson data/856/820/53/85682053.geojson data/856/821/39/85682139.geojson data/856/821/43/85682143.geojson data/856/821/49/85682149.geojson meta/wof-region-20151112.csv meta/wof-region-latest.csv
INFO:root:invoking git-whosonfirst-mapzen post-commit hooks for 8feb92712c7c65c6b694543ca40921d530d6b9e3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/819/91/85681991.geojson to S3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/819/99/85681999.geojson to S3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/820/11/85682011.geojson to S3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/820/15/85682015.geojson to S3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/820/21/85682021.geojson to S3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/820/37/85682037.geojson to S3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/820/53/85682053.geojson to S3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/821/39/85682139.geojson to S3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/821/43/85682143.geojson to S3
INFO:root:copy /usr/local/data/whosonfirst-data/data/856/821/49/85682149.geojson to S3
INFO:root:git commit --amend -C HEAD --no-verify
INFO:root:[master 8feb927] update more wof:name per issue #164
 Date: Thu Nov 12 22:01:07 2015 +0000
 12 files changed, 80 insertions(+), 80 deletions(-)

[master 7ce3399] update more wof:name per issue #164
 10 files changed, 60 insertions(+), 60 deletions(-)
```

## Caveats

The pre- and post- hooks are both written in Python so that we can take advantage of [the existing library code for wrangling Who's on First documents](https://github.com/whosonfirst?utf8=%E2%9C%93&query=py-). In the meantime the `*-hook` files in this repository perform some gynmnastics to account for the reality that Git is as weird as it is powerful.

If you find yourself adding functionality to any of the files in this repository please ensure that WOF-speific functionality is made part of a new or existing library that can be _invoked_ from the Git hooks but not defined in them.

The Git hooks should be the place where all the Git related magic and voodoo is kept isolated from all other WOF related logic.

## See also

* https://github.com/whosonfirst/whosonfirst-data
* https://stackoverflow.com/questions/1797074/local-executing-hook-after-a-git-push