#!/bin/bash
set -e
cd /code
mkdir -p /build /var/log/glusterfs
mkdir -p /run/rpcbind/
cat <<EOF > /etc/yum.repos.d/gluster-build.repo
[gluster-build]
name = Gluster Build
baseurl = file:///opt/qa/rpm
EOF
# Run rpcbind for gNFS
/usr/sbin/rpcbind -w

mknod /dev/loop0 -m0660 b 7 0 || true
mknod /dev/loop1 -m0660 b 7 1 || true
mknod /dev/loop2 -m0660 b 7 2 || true
mknod /dev/loop3 -m0660 b 7 3 || true
mknod /dev/loop4 -m0660 b 7 4 || true
mknod /dev/loop5 -m0660 b 7 5 || true
mknod /dev/loop6 -m0660 b 7 6 || true
mknod /dev/loop7 -m0660 b 7 7 || true
mknod /dev/loop8 -m0660 b 7 8 || true
mknod /dev/loop9 -m0660 b 7 9 || true
mknod /dev/loop10 -m0660 b 7 10 || true
mknod /dev/loop11 -m0660 b 7 11 || true
mknod /dev/loop12 -m0660 b 7 12 || true
mknod /dev/loop13 -m0660 b 7 13 || true

dnf install -y --nogpgcheck glusterfs-server glusterfs-fuse glusterfs-api glusterfs-api-devel glusterfs-cli glusterfs-debuginfo glusterfs-devel glusterfs-libs glusterfs-regression-tests
if [ -z "$1" ]
then
    echo "No chunk specified"
    exit 1
fi
chunk=$(cat /opt/qa/chunks/$1)
/opt/qa/regression.sh -- $chunk
