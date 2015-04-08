#!/bin/sh

ARGS=("$@")
NUM_ARGS=$#

if [ $NUM_ARGS -lt 1 ] ;
then
  SCRIPT_NAME=`basename $0` ;
  echo "Usage: $SCRIPT_NAME <filename.(w|j)ar>" ;
  exit ;
fi

CURRENT_DIR=`pwd`

ORIGIN_JAR_FULL_PATH=${ARGS[0]}
ORIGIN_JAR_NAME=$(basename $ORIGIN_JAR_FULL_PATH)

TEMP_PATH="/tmp"
TEMP_JAR_FULL_PATH="$TEMP_PATH/$ORIGIN_JAR_NAME"

EXTRACTION_DIR="$ORIGIN_JAR_NAME-dir"

cp $ORIGIN_JAR_FULL_PATH $TEMP_PATH
cd $TEMP_PATH

rm -rf $EXTRACTION_DIR

mkdir $EXTRACTION_DIR
cd $EXTRACTION_DIR

jar xf $TEMP_JAR_FULL_PATH
ls -laF .

echo "extractionDir:$TEMP_PATH/$EXTRACTION_DIR"

cd $CURRENT_DIR
