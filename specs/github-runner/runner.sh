#!/bin/bash

# use public GitHub by default
GITHUB_BASE_URL=${GITHUB_BASE_URL:-https://github.com}
GITHUB_API_URL=${GITHUB_API_URL:-https://api.github.com}

RUNNER_TEMPLATE_DIR=${RUNNER_TEMPLATE_DIR:-/usr/lib/github-runner}
RUNNER_SYMLINK_BINARIES=${RUNNER_SYMLINK_BINARIES:-"false"}


acquire_github_token() {
    if [ -z "${GITHUB_PAT}" ] ; then
        echo "not acquiring new registration token since we have to PAT set"
    else
        echo "getting registration token"
        url=${GITHUB_API_URL}/repos/${RUNNER_REPOSITORY}/actions/runners/registration-token
        reply=$(curl -X POST -H "Accept: application/vnd.github+json" -H "Authorization: Bearer ${GITHUB_PAT}" ${url})
        echo ${reply}
        GITHUB_TOKEN=$(echo ${reply} | jq -r .token)
    fi
}

remove_runner() {
    echo "removing runner"
    ./config.sh remove --token ${GITHUB_TOKEN}
}

usage() {
    echo "no usage info yet"
}

fail() {
    msg=$1
    echo ${msg} >&1
    usage
    echo "Terminating." >&2
    exit 1
}

OPTS=$(getopt -o h --long api-url:,base-url:,help,labels:,name:,pat:,repo:,sym-link,tarball:,top-dir: -n $0 -- "$@")
if [ $? != 0 ] ; then
    usage
    echo "Terminating." >&2
    exit 1
fi

eval set -- "$OPTS"

while true; do
    case "$1" in
        --api-url)         GITHUB_API_URL=${2} ; shift 2 ;;
        --base-url)        GITHUB_BASE_URL=${2} ; shift 2 ;;
        -h)                usage ; exit 0 ;;
        --labels)          RUNNER_LABELS=${2} ; shift 2 ;;
        --name)            RUNNER_NAME=${2} ; shift 2 ;;
        --pat)             GITHUB_PAT=${2} ; shift 2 ;;
        --repo)            RUNNER_REPOSITORY=${2} ; shift 2 ;;
        --symlink)         RUNNER_SYMLINK_BINARIES="true" ; shift ;;
        --tarball)         RUNNER_TARBALL=${2} ; shift 2 ;;
        --top-dir)         RUNNER_TOP_DIR=${2} ; shift 2 ;;
        *)                 break ;;
    esac
done

[ -z ${GITHUB_API_URL} ] && fail "no API URL set"
[ -z ${GITHUB_BASE_URL} ] && fail "no base URL set"
[ -z ${RUNNER_NAME} ] && fail "no name set"
[ -z ${RUNNER_REPOSITORY} ] && fail "no repository set"
[ -z ${RUNNER_TARBALL} ] && fail "no tarball set"

[ -z ${RUNNER_TOP_DIR} ] && RUNNER_TOP_DIR=.


DIRECTORY=${RUNNER_TOP_DIR}/${RUNNER_NAME}
[ -d ${DIRECTORY} ] || mkdir -p ${DIRECTORY}
cd ${DIRECTORY}

if [ -d ${RUNNER_TEMPLATE_DIR} ] ; then
    # make sure dir is valid
    essentials="config.sh run.sh bin externals"
    for f in ${essential} ; do
        [ -f ${RUNNER_TEMPLATE_DIR}/$f ] || fail "no $f in ${RUNNER_TEMPLATE_DIR}"
    done

    for d in bin externals ; do
        [ -d $d ] && rm -rf $d
        # symlink does not work, see https://github.com/actions/runner/issues/3760
        if [ "${RUNNER_SYMLINK_BINARIES}" == "true" ] ; then
            ln -fs ${RUNNER_TEMPLATE_DIR}/$d .
        else
            cp -r ${RUNNER_TEMPLATE_DIR}/$d .
        fi
    done

    for f in $(ls ${RUNNER_TEMPLATE_DIR} | grep -v '^bin$\|^externals$') ; do
        cp ${RUNNER_TEMPLATE_DIR}/$f .
    done
else
    [ -f ${RUNNER_TARBALL} ] || fail "file '${RUNNER_TARBALL}' does not exist"
    RUNNER_TARBALL=$(realpath ${RUNNER_TARBALL})

    tar zxf ${RUNNER_TARBALL}
fi


if [ ! -z "${GITHUB_PAT}" ] ; then
    acquire_github_token
fi
[ -z ${GITHUB_TOKEN} ] && fail "no token or GITHUB_PAT set"

# clean up any eventual previous instance, may fail
# if first time instance, or already properly cleaned up
remove_runner

./config.sh \
    --disableupdate \
    --unattended \
    --url ${GITHUB_BASE_URL}/${RUNNER_REPOSITORY} \
    --token ${GITHUB_TOKEN} \
    --labels name:${RUNNER_NAME},os:$(. /etc/os-release && echo "$ID-$VERSION_ID")${RUNNER_LABELS:+,${RUNNER_LABELS}} \
    --name ${RUNNER_NAME}@$(hostname)

trap 'acquire_github_token; remove_runner; exit 130' INT
trap 'acquire_github_token; remove_runner; exit 143' TERM

./run.sh & wait $!
