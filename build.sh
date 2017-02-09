#!/bin/bash
DOCKER_PATH="${PWD}"
QA_PATH="${DOCKER_PATH}/qa"
RPM_PATH="${QA_PATH}/rpm"

mkdir "${QA_PATH}"
rm -rf "${RPM_PATH}"
mkdir "${RPM_PATH}"
cd ../glusterfs
./autogen.sh
./configure --enable-fusermount
cd extras/LinuxRPM
make prep srcrpm
sudo mock -r 'fedora-25-x86_64' --resultdir="${RPM_PATH}" --cleanup-after --rebuild glusterfs*src.rpm
createrepo_c "${RPM_PATH}"

