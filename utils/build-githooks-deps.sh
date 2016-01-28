#!/bin/sh

# HEY LOOK. THIS IS NOT GENERIC CODE WITH EXTENSIBLE PATHS. IT WILL
# BE ONE DAY BUT TODAY IT ASSUMES A BUNCH OF THINGS ARE INSTALLED IN
# A BUNCH OF VERY SPECIFIC PLACES (20160128/thisisaaronland)

# rebuild wof-sync-files for:
# https://github.com/whosonfirst/git-whosonfirst-data

GITWOF="/usr/local/mapzen/git-whosonfirst-data/"
BIN="${GITWOF}bin/"

###################################################################

cd /usr/local/mapzen/go-whosonfirst-s3                                                                                                                            
export GOPATH=`pwd`                                                                                                                                               

echo "build for OS X"

if [ -f ${BIN}/osx/wof-sync-files ]
then
    mv ${BIN}/osx/wof-sync-files ${BIN}/osx/wof-sync-files.bak
fi

export GOOS='darwin'
export GOARCH='amd64'

go build -o ${BIN}/osx/wof-sync-files cmd/wof-sync-files.go                                                                   

echo "build for Windows"

if [ -f ${BIN}/windows/wof-sync-files ]
then
    mv ${BIN}/windows/wof-sync-files ${BIN}/windows/wof-sync-files.bak
fi

export GOOS='windows'
export GOARCH='amd64'
                                                                                               
go build -o ${BIN}/windows/wof-sync-files cmd/wof-sync-files.go                                                               

echo "build for Linux"

if [ -f ${BIN}/linux/wof-sync-files ]
then
    mv ${BIN}/linux/wof-sync-files ${BIN}/linux/wof-sync-files.bak
fi

export GOOS='linux'                                                                                                                                               
export GOARCH='amd64'

go build -o ${BIN}/linux/wof-sync-files cmd/wof-sync-files.go 

###################################################################

cd /usr/local/mapzen/go-whosonfirst-clone                                                                                                
export GOPATH=`pwd`                                                                                                                                               

echo "build for OS X"

if [ -f ${BIN}/osx/wof-clone-metafiles ]
then
    mv ${BIN}/osx/wof-clone-metafiles ${BIN}/osx/wof-clone-metafiles.bak
fi

export GOOS='darwin'
export GOARCH='amd64'

go build -o ${BIN}/osx/wof-clone-metafiles cmd/wof-clone-metafiles.go                                                                   

echo "build for Windows"

if [ -f ${BIN}/windows/wof-clone-metafiles ]
then
    mv ${BIN}/windows/wof-clone-metafiles ${BIN}/windows/wof-clone-metafiles.bak
fi

export GOOS='windows'
export GOARCH='amd64'
                                                                                               
go build -o ${BIN}/windows/wof-clone-metafiles cmd/wof-clone-metafiles.go                                                               

echo "build for Linux"

if [ -f ${BIN}/linux/wof-clone-metafiles ]
then
    mv ${BIN}/linux/wof-clone-metafiles ${BIN}/linux/wof-clone-metafiles.bak
fi

export GOOS='linux'                                                                                                                                               
export GOARCH='amd64'

go build -o ${BIN}/linux/wof-clone-metafiles cmd/wof-clone-metafiles.go 

###################################################################

cd /usr/local/mapzen/py-mapzen-whosonfirst-bundles

cp scripts/wof-bundle-placetypes ${BIN}/osx/wof-bundle-placetypes
cp scripts/wof-bundle-placetypes ${BIN}/windows/wof-bundle-placetypes
cp scripts/wof-bundle-placetypes ${BIN}/linux/wof-bundle-placetypes

###################################################################

cd /usr/local/mapzen/py-mapzen-whosonfirst-search

cp scripts/wof-es-index-filelist ${BIN}/osx/wof-es-index-filelist
cp scripts/wof-es-index-filelist ${BIN}/windows/wof-es-index-filelist
cp scripts/wof-es-index-filelist ${BIN}/linux/wof-es-index-filelist

###################################################################

echo "all done"
exit 0
