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

for HOOK in "pre-commit" "post-commit" "post-merge" "post-push-async"
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

# this is too fiddly to try and set dynamically but we should endeavour to
# keep the example below up to date with reality (20160128/thisisaaronland)

if [ -f ${HOOKS}/hooks.cfg ]
then
    echo "There is already a hooks.cfg file in place"
else 
    cp ${HOOKS}/hooks.cfg.example ${HOOKS}/hooks.cfg
    echo "created ${HOOKS}/hooks.cfg but YOU WILL NEED TO UPDATE IT with installation specific information; see documentation for details"
fi

git config alias.xpush '!git push $1 $2 && ${HOOK}/post-push-async'

cd -
exit 0
