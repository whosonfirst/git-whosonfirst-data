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

for HOOK in "post-push" "post-merge"
do
    if [ -f ${GITHOOKS}/${HOOK} ]
    then
	echo "remove ${GITHOOKS}/${HOOK} (cleaning up old git hooks)"
	rm ${GITHOOKS}/${HOOK}
    fi
done

for HOOK in "pre-commit" "post-commit"
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

cd -
exit 0
