# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from processor.rules.mozilla_transform_rules import (
    ESRVersionRewrite,
    PluginContentURL,
    ProductRule,
    ProductRewrite
)

from tests.testlib import _

class TestESRVersionRewrite:

    def test_everything_we_hoped_for(self, cannonical_raw_crash):
        raw_crash = cannonical_raw_crash
        raw_crash['ReleaseChannel'] = 'esr'
        ESRVersionRewrite()(_, raw_crash, _, _)

        assert raw_crash['Version'] == '12.0esr'

    def test_wrong_crash(self, cannonical_raw_crash):
        raw_crash = cannonical_raw_crash
        ESRVersionRewrite()(_, raw_crash, _, _)

        assert raw_crash['Version'] == '12.0' # unchanged

    def test_this_is_really_broken(self, cannonical_raw_crash):
        raw_crash = cannonical_raw_crash
        raw_crash['ReleaseChannel'] = 'esr'
        del raw_crash['Version']

        with pytest.raises(KeyError) as failure:
            ESRVersionRewrite()(_, raw_crash, _, _)

        assert (failure.value.args[0] ==
            '"Version" missing from esr release raw_crash')


class TestPluginContentURL:

    def test_everything_we_hoped_for(self, cannonical_raw_crash):
        raw_crash = cannonical_raw_crash
        raw_crash['PluginContentURL'] = 'http://mozilla.com'
        raw_crash['URL'] = 'http://google.com'
        PluginContentURL()(_, raw_crash, _, _)

        assert raw_crash['URL'] == 'http://mozilla.com'

    def test_wrong_crash(self, cannonical_raw_crash):
        raw_crash = cannonical_raw_crash
        raw_crash['URL'] = 'http://google.com'
        PluginContentURL()(_, raw_crash, _, _)

        assert raw_crash['URL'] == 'http://google.com' # unchanged


class TestProductRewrite:

    def test_everything_we_hoped_for(self, cannonical_raw_crash):
        raw_crash = cannonical_raw_crash
        ProductRewrite()(_, raw_crash, _, _)

        assert raw_crash['ProductName'] == 'FennecAndroid'

    def test_wrong_crash(self, cannonical_raw_crash):
        raw_crash = cannonical_raw_crash
        raw_crash['ProductID'] = 'arbitrary-garbage-from-the-network'
        ProductRewrite()(_, raw_crash, _, _)

        assert raw_crash['ProductName'] == 'Firefox' # unchanged


class TestProductRule:

    def test_everything_we_hoped_for(self, cannonical_raw_crash,
        cannonical_processed_crash):

        raw_crash = cannonical_raw_crash
        processed_crash = cannonical_processed_crash

        ProductRule()(_, raw_crash, _, processed_crash)

        assert processed_crash['product'] == 'Firefox'
        assert processed_crash['version'] == '12.0'
        assert (processed_crash['productid'] ==
            '{ec8030f7-c20a-464f-9b0e-13a3a9e97384}')
        assert processed_crash['distributor'] == 'Mozilla'
        assert processed_crash['distributor_version'] == '12.0'
        assert processed_crash['release_channel'] == 'release'
        assert processed_crash['build'] == '20120420145725'
