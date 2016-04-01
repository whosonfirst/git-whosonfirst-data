# git-whosonfirst-data

Git related utilities for Who's On First Data

## Important

This is still very much a work in progress. Depending on when you read these words the code included here might be wonky or even completely broken. It _should_ work as of this writing but I bet you could find a way to make things get weird if you wanted to. Good times.

## Dependencies

Currently this repository lacks a handy script for installing dependencies so the easiest way to deal with this is to install the [py-mapzen-whosonfirst](https://github.com/whosonfirst/py-mapzen-whosonfirst) bundle which will install everything you need (and a few things you don't).

If you are using asynchronous `post-push` hooks (described below) you will also need to install:

* https://github.com/whosonfirst/go-whosonfirst-s3
* https://github.com/whosonfirst/slackcat

Having to do this is _not_ a feature. We'll figure something out eventually.

## Install

To install the `pre-commit` and `post-commit` hooks you will need to copy both files to the `.git/hooks` folder in your copy of [whosonfirst-data](https://github.com/whosonfirst/whosonfirst-data). You can also symlink them so that updates and changes to the source will take effect immediately. For example:

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

### post-push-async

This is where we attempt to upload the updated WOF documents to a Mapzen / Who's On First (AWS) S3 bucket, index things in Elasticsearch, regenerate bundles and whatever else we dream up next. The important part is that these all happen asynchronously and the `post-push-async` command doesn't wait for any single command to complete.

#### It's complicated

Git doesn't actually support _post_ push hooks so you will need to install this as part of a Git (push) alias and invoke the alias explicitly when you push to a branch. To install the alias you would do the following _from_ your copy of the [whosonfirst-data]() repository.

```
$> git config alias.xpush '!git push $1 $2 && /usr/local/mapzen/git-whosonfirst-data/hooks/post-push-async'
```

You should adjust the name of `xpush` alias and the path the `post-push-async` script as necessary to reflect the reality of your setup. When you're ready to commit changes you would type:

```
$> git xpush origin <branch>
```

Which will do the usual `git push origin <branch>` dance and _then_ invoke the `post-push-async` hook. As of this writing the hook is not smart enough to check for, or limit itself, to a specific branch being pushed to.

#### It's actually more complicated...

The `post-push-async` command actually invokes a number of different processes (asynchronously) that each need their own configuration variables. These variables are stored in a standard `.ini` config file. By default the `post-push-async` script looks for a config file named `hooks.cfg` in its parent directory. You can specify an alternate path using the `-c` or `--config` argument.

Here's a sample config file:

```
[post-push]
s3=_(boolean) copy updated files to S3_
s3_bucket=_(string) the name of the S3 bucket you're uploading to_
s3_prefix=_(string) the name of any additional sub-directories inside the S3 bucket where files should be written (optional)_
s3_credentials=(string) _the path your AWS S3 credentials as described in this [handy blog post](http://blogs.aws.amazon.com/security/post/Tx3D6U6WSFGOK2H/A-New-and-Standardized-Way-to-Manage-Credentials-in-the-AWS-SDKs), optional_
es=_(boolean) index updated files in Elasticsearch_
es_host=_(string) the host of the Elasticsearch endpoint you want to index WOF documents in_
es_port=_(int) the port of the Elasticsearch endpoint you want to index WOF documents in_
slack=_(boolean) send a message to a Slack channel (using the WOF fork of slackcat) once all the transfers are complete, optional_
slack_config=_(string) the path to your slackcat config file_
bundle=_(boolean) generate new bundles for updated files_
bundle_dest=_(string) where to store bundles, locally_
```

For example

When the hooks is run you might see something like this printed to STDOUT:

```
INFO:root:getting ready to /usr/local/mapzen/go-whosonfirst-s3/bin/wof-sync-files -bucket whosonfirst.mapzen.com -root /usr/local/data/whosonfirst-data/data -file-list /tmp/tmp3zHxja -tidy -slack -slack-config /usr/local/mapzen/slackcat/.slackcat.conf
INFO:root:launched with PID 9629
```

And then you if you looked for that PID you'd see:

```
$> ps -p 9629
PID TTY          TIME CMD
9629 pts/8    00:00:08 wof-sync-files
```

And then in (some number of seconds) the following woudl get written to STDOUT (and to slack if so configured):

```
[wof-sync-files] 23:16:44.105606 [status] Scheduled 733 Completed 733 Success 634 Error 0 Skipped 99 Time 15.623659793s
```

#### Don't forget

You'll need to tell Git about the `post-push-async` hook like this:

```
$> git config alias.xpush '!git push $1 $2 && /usr/local/mapzen/git-whosonfirst-data/hooks/post-push'
```

### But wait... There's more!!!

All of the Git hooks (including `post-push-async`) can be told to process changes from a custom `--start-commit` and `--end-commit` hash. This is useful for processing changes from pull requests that pre-date `HEAD`. For example:

```
./.git/hooks/post-push-async --start-commit 3e55e3031ae8086fb88c2db8b79027e25c42ee8a
```

### Example

#### Update a file

```
$> /usr/local/bin/wof-exportify -s /usr/local/mapzen/whosonfirst-data/data/ -i 101756549
INFO:root:writing /usr/local/mapzen/whosonfirst-data/data/101/756/549/101756549.geojson
```

_The `wof-exportify` script will simply format a WOF record and update its lastmodified date, which is useful way of triggering a pointless change when necessary._

#### Commit your changes

```
$> git commit -m "update lastmodified (testing git hooks)" .
INFO:root:invoking git-whosonfirst-mapzen pre-commit hooks for 9373a8fd7b4eb87baca445b9a7eb1a3a3053412f
INFO:root:validating /usr/local/data/whosonfirst-data/data/101/756/549/101756549.geojson
INFO:root:formatting and exportifying /usr/local/data/whosonfirst-data/data/101/756/549/101756549.geojson
INFO:root:writing /usr/local/data/whosonfirst-data/data/101/756/549/101756549.geojson
INFO:root:rebuild meta file for placetype locality with one update
INFO:root:copy /usr/local/data/whosonfirst-data/meta/wof-locality-20151113.csv to /usr/local/data/whosonfirst-data/meta/wof-locality-latest.csv
INFO:root:writing /usr/local/data/whosonfirst-data/.commit to disk to be processed by the post-commit hook
INFO:root:invoking git-whosonfirst-mapzen post-commit hooks for 596aceddc0f982f97cd6bdf6f9dec6c31d2b6b02
INFO:root:/usr/local/data/whosonfirst-data/.commit exists, so I am going to look for files that have been modified
INFO:root:git add data/101/756/549/101756549.geojson meta/wof-locality-20151113.csv meta/wof-locality-latest.csv
INFO:root:invoking git-whosonfirst-mapzen post-commit hooks for 413a5d74c82ae6f3f843d785bb7b5668245688cd
INFO:root:git commit --amend -C HEAD --no-verify
INFO:root:[master 413a5d7] update lastmodified (testing git hooks)
 Date: Fri Nov 13 22:28:18 2015 +0000
 3 files changed, 3 insertions(+), 3 deletions(-)

INFO:root:nothing else in this commit that we need to apply post-commit hooks to
[master 596aced] update lastmodified (testing git hooks)
 1 file changed, 1 insertion(+), 1 deletion(-)
```

#### Push the commit

Remember we're actually _xpush_-ing the changes per the discussion about the `post-push` hook and Git aliases.

```
$> git xpush origin master
Counting objects: 9, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (8/8), done.
Writing objects: 100% (9/9), 1.79 KiB | 0 bytes/s, done.
Total 9 (delta 7), reused 0 (delta 0)
To git@github.com:whosonfirst/whosonfirst-data.git
   9373a8f..413a5d7  master -> master
INFO:root:invoking git-whosonfirst-mapzen post-push hooks for 413a5d74c82ae6f3f843d785bb7b5668245688cd
INFO:root:copy /usr/local/data/whosonfirst-data/data/101/756/549/101756549.geojson to S3
```

## Examples

### Here's an example of a commit failing validation

```
$> git commit -m "update airport codes, names and hierarchy for LIS" .
INFO:root:invoking git-whosonfirst-mapzen pre-commit hooks for ae168390228fa69fdc8b5f1319f33d505c543685
INFO:root:validating /usr/local/data/whosonfirst-data/data/102/535/643/102535643.geojson
ERROR:root:failed to open /usr/local/data/whosonfirst-data/data/102/535/643/102535643.geojson because No JSON object could be decoded
ERROR:root:/usr/local/data/whosonfirst-data/data/102/535/643/102535643.geojson FAILED validation test
ERROR:root:validation report is:
# debug

# info

# warning

# ok

* False

# error

* failed to open /usr/local/data/whosonfirst-data/data/102/535/643/102535643.geojson because No JSON object could be decoded
```

The problem in this case was an array whose last item had a trailing `,` which is a fatal JSON error. Unfortunately Python's JSON library is not terribly informative about _what_ prevents a file from being decoded so that level of snooping will remain your responsibility.

## Caveats

All the hooks in this repository are written in Python so that we can take advantage of [the existing library code for wrangling Who's on First documents](https://github.com/whosonfirst?utf8=%E2%9C%93&query=py-). In the meantime the `*-hook` files in this repository perform some gynmnastics to account for the reality that Git is as weird as it is powerful.

If you find yourself adding functionality to any of the files in this repository please ensure that WOF-speific functionality is made part of a new or existing library that can be _invoked_ from the Git hooks but not defined in them.

The Git hooks should be the place where all the Git related magic and voodoo is kept isolated from all other WOF related logic.

## See also

* https://github.com/whosonfirst/whosonfirst-data
* https://stackoverflow.com/questions/1797074/local-executing-hook-after-a-git-push#3466589
