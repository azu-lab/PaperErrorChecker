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
OPT=`getopt -o s: -l source_directory: -- "$@"`

if [ $? != 0 ] ; then
    echo "[Error] Option parsing processing is failed." 1>&2
    show_usage
    exit 1
fi

eval set -- "$OPT"

while true
do
    case $1 in
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

echo "---- [Error] [Insert a period] ----"
grep --color -ne "et al " ${TEX_FILES}
grep --color -Ene "Fig[^u\.]" -Ene "Eq[^s\.]" -Ene "Eqs[^\.]" ${TEX_FILES}

echo "---- [Error] [Insert a comma] ----"
grep --color -ne "However " -ne "In addtion" -ne "Additionally" -ne "Therefore " ${TEX_FILES}
grep --color -ine "Otherwise " ${TEX_FILES}
grep --color -Fn "e.g. " -Fn "i.e. " ${TEX_FILES}

echo "---- [Error] [Insert a half-width space] ----"
grep --color -Ene "[0-9]+ms " -Ene "\S+\\\\cite" -Ene "[a-zA-Z]+\(" -Ene "\)[a-zA-Z]+" ${TEX_FILES}
grep --color -Ene "ROS2" ${TEX_FILES}

echo "---- [Error] [Insert a tilde] ----"
grep --color -ne "Fig\.[^~]" -ne "Figure[^~]" -ne "Eq\.[^~]" -ne "Table[^s~]" -ne "Algorithm[^s~]" ${TEX_FILES}

echo "---- [Error] [Remove a half-width space] ----"
grep --color -Ene "[0-9] \\\\%" -ne " : " ${TEX_FILES}

echo "---- [Error] [Remove the article] ----"
grep --color -ixne "each a" -ixne "each an" -ixne "each the" ${TEX_FILES}
grep --color -ine "a Fig" -ine "the Fig" -ine "a table" -ine "the table" -ine "a section" -ine "the section" ${TEX_FILES}

echo "---- [Error] [Don't use present progressive form] ----"
grep --color -ne "existing" -ne "having" ${TEX_FILES}

echo "---- [Error] [Not a conjunction] ----"
grep --color -ne ", however" -ne ", therefore" -ne ", then" -ne ", thus" -ne ", thereby" ${TEX_FILES}

echo "---- [Error] [Don't use at the beginning of a sentence] ----"
grep --color -ne "And" -ne "But" -ne "Also" ${TEX_FILES}

echo "---- [Error] [Don't use a shortened form] ----"
grep --color -ne "don't" -ne "hasn't" -ne "doesn't" -ne "can't" ${TEX_FILES}

echo "---- [Error] [Don't use colloquial or casual expression] ----"
grep --color -ixne "so" -ixne "very" -ixne "etc" ${TEX_FILES}

echo "---- [Error] [Don't use subjective expression] ----"
grep --color -ixne "think" ${TEX_FILES}

echo "---- [Error] [Don't use a gender term] ----"
grep --color -ixne "elderly people" -ixne "man" -ixne "women" ${TEX_FILES}

echo "---- [Error] [Spell out the numbers] ----"
for i in $( seq 1 9 )
do
    grep --color -xne "${i}" ${TEX_FILES}
done

echo "---- [Error] [Corrected to the appropriate article] ----"
grep --color -ine "an self" ${TEX_FILES}

echo "---- [Error] ['==' -> '='] ----"
grep --color -ne "==" ${TEX_FILES}

echo "---- [Error] ['<=' or '>=' -> '\leq' or '\geq'] ----"
grep --color -ne "<=" -ne ">=" ${TEX_FILES}

echo "---- [Error] ['Acknowledgements' -> 'Acknowledgments'] ----"
grep --color -ine "Acknowledgements" ${TEX_FILES}

echo "---- [Warning] ['a lot of' -> 'many' or 'much'] ----"
grep --color -ine "a lot of" ${TEX_FILES}

echo "---- [Warning] [Don't use ambiguous expression] ----"
grep --color -ine "it is" -ine "there is" -ixne "you" -ixne "your" -ine "people" ${TEX_FILES}
grep --color -ine "several" -ine "good" -inxe "get" ${TEX_FILES}

echo "---- [Best effort] [Reduce use of 'We' and 'I'] ----"
grep --color -xine "we" -xine "I" ${TEX_FILES}

# Azumi lab.
echo "---- [Azumi lab.] ['self-driving car' -> 'autonomous vehicles'] ----"
grep --color -ine "self-driving car" ${TEX_FILES}

echo "---- [Azumi lab.] ['was proposed' -> 'has been proposed'] ----"
grep --color -ine "was proposed" ${TEX_FILES}

echo "---- [Azumi lab.] ['GPS' -> 'Global Navigation Satellite System (GNSS)'] ----"
grep --color -ine "GPS" ${TEX_FILES}

echo "---- [Azumi lab.] [Don't use 'previous work'] ----"
grep --color -ine "previous work" ${TEX_FILES}

# Enago
echo "---- [Enago] ['about' -> 'approximately'] ----"
grep --color -ine "about" ${TEX_FILES}

echo "---- [Enago] ['correctly' -> 'accurately'] ----"
grep --color -ine "correctly" ${TEX_FILES}

echo "---- [Enago] ['purpose' -> 'objective'] ----"
grep --color -ine "purpose" ${TEX_FILES}

echo "---- [Enago] ['In addition' -> 'Additionally'] ----"
grep --color -ine "In addition" ${TEX_FILES}
