#!/bin/sh

# HEY LOOK. THIS IS NOT GENERIC CODE WITH EXTENSIBLE PATHS. IT WILL
# BE ONE DAY BUT TODAY IT ASSUMES A BUNCH OF THINGS ARE INSTALLED IN
# A BUNCH OF VERY SPECIFIC PLACES (20160128/thisisaaronland)

# rebuild wof-sync-files for:
# https://github.com/whosonfirst/git-whosonfirst-data

SOURCES=$1

GITWOF="${SOURCES}/git-whosonfirst-data/"
BIN="${GITWOF}bin/"

###################################################################

if [ ! -d ${SOURCES} ]
then
    echo "Missing sources"
    exit 1
fi

###################################################################

# go things

for PAIR in go-whosonfirst-s3#wof-sync-files go-whosonfirst-clone#wof-clone-metafiles
do

    REPO=`echo ${PAIR} | awk -F '#' '{print $1}'`
    TOOL=`echo ${PAIR} | awk -F '#' '{print $2}'`

    ROOT=${SOURCES}/${REPO}
    cd ${ROOT}

    export GOPATH="${ROOT}"                                                                                                                                              
    export GOARCH='amd64'

    for OS in darwin windows linux
    do 
	
	export GOOS="${OS}"
	echo "build ${TOOL} for ${OS}"
	go build -o ${BIN}${OS}/${TOOL} cmd/${TOOL}.go
    done
done

###################################################################

# python things

for PAIR in py-mapzen-whosonfirst-bundles#wof-bundle-placetypes py-mapzen-whosonfirst-search#wof-es-index-filelist
do

    REPO=`echo ${PAIR} | awk -F '#' '{print $1}'`
    TOOL=`echo ${PAIR} | awk -F '#' '{print $2}'`

    ROOT=${SOURCES}/${REPO}
    cd ${ROOT}

    for OS in darwin windows linux
    do 
	echo "clone ${TOOL} for ${OS}"
	cp scripts/${TOOL} ${BIN}${OS}/${TOOL}
    done

done

###################################################################

echo "all done"
exit 0
