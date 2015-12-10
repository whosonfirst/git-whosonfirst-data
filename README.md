# git-whosonfirst-data

Git related utilities for Who's On First Data

## Important

This is still very much a work in progress. Depending on when you read these words the code included here might be wonky or even completely broken. It _should_ work as of this writing but I bet you could find a way to make things get weird if you wanted to. Good times.

## Dependencies

Currently this repository lacks a handy script for installing dependencies so you will need to ensure that recent versions of the following are installed:

* https://github.com/whosonfirst/py-mapzen-whosonfirst-utils
* https://github.com/whosonfirst/py-mapzen-whosonfirst-export
* https://github.com/whosonfirst/py-mapzen-whosonfirst-validator
* https://github.com/whosonfirst/py-mapzen-whosonfirst-search
* https://github.com/whosonfirst/py-mapzen-whosonfirst-aws

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

### post-push

This is where we attempt to upload the updated WOF documents to a Mapzen / Who's On First (AWS) S3 bucket.

#### It's complicated

Git doesn't actually support _post_ push hooks so you will need to install this as part of a Git (push) alias and invoke the alias explicitly when you push to a branch. To install the alias you would do the following _from_ your copy of the [whosonfirst-data]() repository.

```
$> git config alias.xpush '!git push $1 $2 && /usr/local/mapzen/git-whosonfirst-data/hooks/post-push <options>'
```

You should adjust the name of `xpush` alias and the path the `post-push` script as necessary to reflect the reality of your setup. When you're ready to commit changes you would type:

```
$> git xpush origin <branch>
```

Which will do the usual `git push origin <branch>` dance and _then_ invoke the `post-push` hook. As of this writing the hook is not smart enough to check for, or limit itself, to a specific branch being pushed to.

#### It's actually more complicated...

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

### post-push-async

#### Did we mention it's complicated?

In order to speed things up and not make you sit there waiting for a whole bunch of files to be transferred to S3 before you can do anymore work there is also `post-push-async` hook. This uses the [go-whosonfirst-s3](https://github.com/whosonfirst/go-whosonfirst-s3) package to transfer files in a background process. Like the `post-push` hook described above you will need to pass a few extra arguments specific to your setup to make it all work. These are:

##### S3 (uploading)

* --s3
* --s3-bucket _the name of the S3 bucket you're uploading to_
* --s3-prefix _the name of any additional sub-directories inside the S3 bucket where files should be written (optional)_
* --s3-credentials _the path your AWS S3 credentials as described in this [handy blog post](http://blogs.aws.amazon.com/security/post/Tx3D6U6WSFGOK2H/A-New-and-Standardized-Way-to-Manage-Credentials-in-the-AWS-SDKs) (optional)_

##### Elasticsearch (indexing)

* --es
* --es-host _the host of the Elasticsearch endpoint you want to index WOF documents in (default is localhost)_
* --es-port _the port of the Elasticsearch endpoint you want to index WOF documents in (default is 9200)_

##### Slack (notifications when things are done)

* --slack _send a message to a Slack channel (using the WOF fork of slackcat) once all the transfers are complete (optional)_
* --slack-config _the path to your slackcat config file (optional)_

For example

```
/usr/local/mapzen/git-whosonfirst-data/hooks/post-push-async --s3 --s3-bucket whosonfirst.mapzen.com --s3-prefix data --s3-credentials ~/.aws/credentials --slack --slack-config ~/.slackcat.conf 
```

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

Just like the `post-push` hook/alias you'll need to tell Git about the `post-push-async` hook like this:

```
$> git config alias.xpush '!git push $1 $2 && /usr/local/mapzen/git-whosonfirst-data/hooks/post-push <options>'
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

## Caveats

All the hooks in this repository are written in Python so that we can take advantage of [the existing library code for wrangling Who's on First documents](https://github.com/whosonfirst?utf8=%E2%9C%93&query=py-). In the meantime the `*-hook` files in this repository perform some gynmnastics to account for the reality that Git is as weird as it is powerful.

If you find yourself adding functionality to any of the files in this repository please ensure that WOF-speific functionality is made part of a new or existing library that can be _invoked_ from the Git hooks but not defined in them.

The Git hooks should be the place where all the Git related magic and voodoo is kept isolated from all other WOF related logic.

## See also

* https://github.com/whosonfirst/whosonfirst-data
* https://stackoverflow.com/questions/1797074/local-executing-hook-after-a-git-push#3466589
