# git-whosonfirst-data

Git related utilities for Who's On First Data

## Important

This is still very much a work in progress. Depending on when you read these words the code included here might be wonky or even completely broken. It _should_ work as of this writing but I bet you could find a way to make things get weird if you wanted to. Good times.

## Install

```
install.sh /path/to/your/whosonfirst-data-repo
```

## Git hooks

### pre-commit

Validate and format documents before commiting them, updating the relevant [placetype-specific meta files](https://github.com/whosonfirst/whosonfirst-data/tree/master/meta) along the way.

### post-commit

This is the part that will append the updated files (exported WOF documents and meta files) to the current commit. [Because Git](https://stackoverflow.com/questions/3284292/can-a-git-hook-automatically-add-files-to-the-commit) and because trying to find a clever-er solution to the problem began to grow [yak-hair](https://en.wiktionary.org/wiki/yak_shaving), like a Wookie. _If someone knows a better way to do this please let us know._

## Example

_Please write me._

## See also

* https://github.com/whosonfirst/whosonfirst-data
* https://stackoverflow.com/questions/1797074/local-executing-hook-after-a-git-push#3466589
