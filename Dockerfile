FROM fedora
MAINTAINER "Nigel Babu" nigelb@redhat.com
#RUN dnf install -y epel-release
RUN dnf install -y git autoconf automake gcc libtool bison flex make rpm-build mock python-devel libaio-devel librdmacm-devel libattr-devel libxml2-devel readline-devel openssl-devel libibverbs-devel fuse-devel glib2-devel userspace-rcu-devel libacl-devel sqlite-devel lvm2-devel attr nfs-utils dbench yajl psmisc bind-utils perl-Test-Harness xfsprogs pyxattr procps-ng which perl-TAP-Harness-JUnit perl-TAP-Formatter-JUnit
RUN dnf install -y hostname gdb
RUN mkdir -p /code /opt/qa
VOLUME ['/code', '/opt/qa']
COPY run-regression.sh /run-regression.sh
CMD /run-regression.sh
