cd /code
mkdir -p /build /var/log/glusterfs
cat <<EOF > /etc/yum.repos.d/gluster-build.repo
[gluster-build]
name = Gluster Build
baseurl = file:///opt/qa/rpm
EOF
/usr/sbin/rpcbind -w
mknod /dev/loop0 b 7 0
mknod /dev/loop1 b 7 0
mknod /dev/loop2 b 7 0
dnf install -y --nogpgcheck glusterfs-server glusterfs-fuse glusterfs-api glusterfs-api-devel glusterfs-cli glusterfs-debuginfo glusterfs-devel glusterfs-libs glusterfs-regression-tests
/opt/qa/regression.sh -- tests/basic
