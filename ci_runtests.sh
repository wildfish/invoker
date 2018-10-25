#!/usr/bin/env bash

set -e

if [ -n "${TRAVIS_TAG}" ]; then
    PACKAGE_VERSION=`python -c "from __future__ import print_function; from invoker import __version__; print(__version__)"`

    if [ "${TRAVIS_TAG}" != "${PACKAGE_VERSION}" ]; then
        echo "Tag version (${TRAVIS_TAG}) is not equal to the package tag (${PACKAGE_VERSION})"
        exit 1
    fi
fi

tox
