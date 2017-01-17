# Gluster Regressions Docker
This repo aims to help run the gluster regression tests in Docker. This Docker
container will install gluster rpms from a specified location, mount the
glusterfs repo as a volume inside the container and run the tests against the
installed binaries. This will help parallelize the tests inside Docker in the
near future for developer boxes.

We're using the latest released Fedora rather than CentOS to get the latest
versions of libraries.

## How to run
Build the containers. We'll eventually provide them off the hub, but for now
we're making too many changes to make it useful to provide the container off
the hub.

    sudo docker build -t gluster-test .

Build the packages and place them in `qa/rpm`. The `build.sh` script should do
it for you. I assume that you have cloned glusterfs and this repo in the same
folder. In that case, `build.sh` should Just Work.

To run the container, you need to mount two volumes
* At /code, mount the path to glusterfs repo
* At /opt/qa, mount the path to the qa folder in this repo

This is how the command looks in my computer:

    sudo docker run --privileged -v ~/code/glusterfs:/code -v ~/code/gluster-docker/qa:/opt/qa gluster-test

You need a privileged container so that extended attributes can be applied to
the filesystem
