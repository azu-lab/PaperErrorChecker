#!/bin/bash


### echo usage
function show_usage () {
    echo "Usage: $0 [-h]"
    echo "          [-d <path of dir> or --check_dir <path of dir>]"
    echo "          [-f <format name> or --format <format name>]"
    exit 0;
}


### initialize option variables
CHECK_DIR=""
FORMAT="conference"
PYTHON_SCRIPT_DIR="$(dirname $0)/src"


### parse command options
OPT=`getopt -o hd:f: -l help,check_dir:format: -- "$@"`


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
    -d | --check_dir)
        CHECK_DIR="$2"
        shift 2
        ;;
    -f | --format)
        FORMAT="$2"
        shift 2
        ;;
    --)
        shift
        break
        ;;
    esac
done


### run checker
export PYTHONPATH="$(dirname $0)/"
python3 ${PYTHON_SCRIPT_DIR}/run_checker.py --check_dir "${CHECK_DIR}" --format "${FORMAT}"


if [ $? -ne 0 ]; then
    echo "$0 is Failed."
else
    echo "$0 is successfully completed." 1>&2
fi


# EOF
