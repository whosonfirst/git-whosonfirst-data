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

This is the part that will append the updated files (exported WOF documents and meta files) to the current commit. [Because Git](https://stackoverflow.com/questions/3284292/can-a-git-hook-automatically-add-files-to-the-commit) and because trying to find a clever-er solution to the problem began to grow [yak-hair](https://en.wiktionary.org/wiki/yak_shaving), like a Wookie. _If someone knows a better way to do this please let us know._

### pre-push

We don't define any specific `pre-push` hooks at this point because [git-lfs](https://github.com/whosonfirst/whosonfirst-data/#git-and-large-files) already installs one and I haven't decided how best we should play with it.

### post-push

This is where we attempt to upload the updated WOF documents to a Mapzen / Who's On First (AWS) S3 bucket.

#### it's complicated

Git doesn't actually support _post_ push hooks so you will need to install this as part of a Git (push) alias and invoke the alias explicitly when you push to a branch. To install the alias you would do the following _from_ your copy of the [whosonfirst-data]() repository.

```
$> git config alias.xpush '!git push $1 $2 && /usr/local/mapzen/git-whosonfirst-data/hooks/post-push'
```

You should adjust the name of `xpush` alias and the path the `post-push` script as necessary to reflect the reality of your setup. When you're ready to commit changes you would type:

```
git xpush origin <branch>
```

Which will do the usual `git push origin <branch>` dance and _then_ invoke the `post-push` hook. As of this writing the hook is not smart enough to check for, or limit itself, to a specific branch being pushed to.

#### it's actually more complicated...

There is where the post-push hook will _attempt_ to upload modified files to S3 if it's been configured correctly, which means passing a few extra arguments to the `post-push` script when you define your Git alias. These are:

* --s3
* --s3-bucket _the name of the S3 bucket you're uploading to_
* --s3-prefix _the name of any additional sub-directories inside the S3 bucket where files should be written (optional)_
* --s3-credentials _the path your AWS S3 credentials as described in this [handy blog post](http://blogs.aws.amazon.com/security/post/Tx3D6U6WSFGOK2H/A-New-and-Standardized-Way-to-Manage-Credentials-in-the-AWS-SDKs) (optional)_

For example

```
/usr/local/mapzen/git-whosonfirst-data/hooks/post-push --s3 --s3-bucket whosonfirst.mapzen.com --s3-prefix data --s3-credentials ~/.aws/credentials
```

The default `post-push` hook implements transfers to S3 using the [py-mapzen-whosonfirst-aws](/usr/local/mapzen/git-whosonfirst-data/hooks/post-push) library and copies files over synchronously. Which is likely to be slow and cumbersome if you're commiting lots and lots of files.

This could probably be sped up using multiple processes but that work is being developed in a `post-push-async` hook that will use the [go-whosonfirst-s3](https://github.com/whosonfirst/go-whosonfirst-s3) package to transfer files in a background process. That work is not finished, as of this writing.

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
INFO:root:git commit --amend -C HEAD --no-verify
INFO:root:[master 8feb927] update more wof:name per issue #164
 Date: Thu Nov 12 22:01:07 2015 +0000
 12 files changed, 80 insertions(+), 80 deletions(-)

[master 7ce3399] update more wof:name per issue #164
 10 files changed, 60 insertions(+), 60 deletions(-)
```

## Caveats

All the hooks in this repository are written in Python so that we can take advantage of [the existing library code for wrangling Who's on First documents](https://github.com/whosonfirst?utf8=%E2%9C%93&query=py-). In the meantime the `*-hook` files in this repository perform some gynmnastics to account for the reality that Git is as weird as it is powerful.

If you find yourself adding functionality to any of the files in this repository please ensure that WOF-speific functionality is made part of a new or existing library that can be _invoked_ from the Git hooks but not defined in them.

The Git hooks should be the place where all the Git related magic and voodoo is kept isolated from all other WOF related logic.

## See also

* https://github.com/whosonfirst/whosonfirst-data
* https://stackoverflow.com/questions/1797074/local-executing-hook-after-a-git-push#3466589
