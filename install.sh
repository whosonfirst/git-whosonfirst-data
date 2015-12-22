#!/bin/sh

PYTHON=`which python`

WHOAMI=`${PYTHON} -c 'import sys; import os; print os.path.abspath(sys.argv[1])' $0`
ROOT=`dirname ${WHOAMI}`
HOOKS="${ROOT}/hooks"

WOFDATA=$1
GITHOOKS="${WOFDATA}/.git/hooks"

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

echo "post-push aliases have NOT been installed you will need to do that yourself - see documentation for details"
exit 0
