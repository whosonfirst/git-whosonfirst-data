#!/bin/sh

PYTHON=`which python`

WHOAMI=`${PYTHON} -c 'import sys; import os; print os.path.abspath(sys.argv[1])' $0`
ROOT=`dirname ${WHOAMI}`
HOOKS="${ROOT}/hooks"

WOFDATA=$1
GITHOOKS="${WOFDATA}/.git/hooks"

# Basic sanity checking

if [ "${WOFDATA}" = "" ]
then
    echo "you forgot to specify where you whosonfirst-data directory is"
    exit 1
fi

if [ ! -d ${WOFDATA} ]
then
    echo "${WOFDATA} does not exist!"
    exit 1
fi

if [ ! -d ${GITHOOKS} ]
then
    echo "${GITHOOKS} does not exist!"
    exit 1
fi

# Install the hooks

for HOOK in "pre-commit" "post-commit" "post-push-async"
do

    if [ -f ${GITHOOKS}/${HOOK} ]
    then
	echo "move ${GITHOOKS}/${HOOK} to ${GITHOOKS}/${HOOK}.old"
	mv ${GITHOOKS}/${HOOK} ${GITHOOKS}/${HOOK}.old
    fi

    if [ -L ${GITHOOKS}/${HOOK} ]
    then
	echo "remove symlink to ${GITHOOKS}/${HOOK}"
	rm ${GITHOOKS}/${HOOK}
    fi

    echo "symlink ${HOOKS}/${HOOK} to ${GITHOOKS}/${HOOK}"
    ln -s ${HOOKS}/${HOOK}  ${GITHOOKS}/${HOOK}
done

# Add some default configs
# https://git-scm.com/docs/git-config

cd ${WOFDATA}
git config --add http.postBuffer 52428800

# this is too fiddly to try and set dynamically but we should endeavour to
# keep the example below up to date with reality (20160128/thisisaaronland)
# git config alias.xpush '!git push $1 $2 && /YOUR/PATH/TO/git-whosonfirst-data/hooks/post-push-async --s3 --s3-bucket YOUR-S3-BUCKET --s3-prefix YOUR-S3_PREFIX --es --es-host YOUR.ELASTICSEARCH.HOST --slack --slack-config /PATH/TO/YOU/.slackcat.conf --verbose --bundle --bundle-dest /PATH/TO/YOU/whosonfirst-bundles/'

cd -


echo "post-push aliases have been installed (in ${GITHOOKS}) not NOT ADDED to .git config file - you will need to do that yourself; see documentation for details"
exit 0
