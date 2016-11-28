===============
Unittest README
===============

These test the Processor code. We use the py.test test runner.

Contents of this directory::

    conftest.py -- holds py.test fixtures
    test_*.py   -- a test file


Run these tests from the repository root using::

    make test


To run a single test or group of tests or with different options, do::

    make shell


This gives you a bash shell in the docker container where you can more easily
do test runs and debugging.
