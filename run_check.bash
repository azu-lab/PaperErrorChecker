#!/bin/bash

### echo usage
function show_usage () {
    echo "Usage: $0 [-h]"
    echo "          [-s <path of dir> or --source_directory <path of dir>]"
    exit 0;
}


### initialize option variables
SOURCE_DIR="${PWD}"


### parse command options
OPT=`getopt -o hs: -l help,source_directory: -- "$@"`

if [ $? != 0 ] ; then
    echo "[Error] Option parsing processing is failed." 1>&2
    show_usage
    exit 1
fi

eval set -- "$OPT"

while true
do
    case $1 in
    -h | --help)
        show_usage;
        shift
        ;;
    -s | --sourcne_directory-dir)
        SOURCE_DIR="$2"
        shift 2
        ;;
    --)
        shift
        break
        ;;
    esac
done


### run check
TEX_FILES=$( find ${SOURCE_DIR} -name "*.tex" )



echo "---- [Error] [Don't use 'in this paper' in abstract] ----"
grep --color -zoP "\\\\begin\{abstract\}[\s\S]*\\\\end{abstract}" ${TEX_FILES} | grep --color "in this paper"

