#!/bin/bash


### echo usage
function show_usage () {
    echo "Usage: $0 [-h]"
    echo "          [-d <path of dir> or --check_dir <path of dir>]"
    exit 0;
}


### initialize option variables
CHECK_DIR="${PWD}/DAGs"
PYTHON_SCRIPT_DIR="$(dirname $0)/src"


### parse command options
OPT=`getopt -o hd: -l help,check_dir: -- "$@"`


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
    --)
        shift
        break
        ;;
    esac
done

# TODO: check check_dir


### run check
export PYTHONPATH="$(dirname $0)/"
python3 ${PYTHON_SCRIPT_DIR}/run_check.py --check_dir "${CHECK_DIR}"


if [ $? -ne 0 ]; then
    echo "$0 is Failed."
else
    echo "$0 is successfully completed." 1>&2
fi


# EOF
