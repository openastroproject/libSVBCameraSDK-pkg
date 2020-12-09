#!/bin/bash

version=`cat version`

rm -fr libsvbcamerasdk-$version
rm -fr libsvbcamerasdk_*
rm -fr libsvbcamerasdk-dev_*
rm -f debfiles/compat
rm -f debfiles/patches/*
rm -f *.ddeb
