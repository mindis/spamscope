"""
Copyright 2016 Fedele Mantuano (https://twitter.com/fedelemantuano)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import absolute_import, print_function, unicode_literals
from bolts.abstracts import AbstractUrlsHandlerBolt

try:
    import simplejson as json
except ImportError:
    import json


class UrlsHandlerBody(AbstractUrlsHandlerBolt):
    outputs = ['sha256_random', 'with_urls', 'urls']

    def initialize(self, stormconf, context):
        super(UrlsHandlerBody, self).initialize(stormconf, context)

    def process(self, tup):
        sha256_mail_random = tup.values[0]
        with_urls = False
        urls_json = None

        try:
            mail = json.loads(tup.values[1])
            body = mail.get('body', None)
            with_urls, urls_json = self._extract_urls(body)

        except Exception as e:
            self.log(
                "Failed process urls for mail: {}".format(
                    sha256_mail_random
                ),
                level="error"
            )
            self.raise_exception(e, tup)

        finally:
            self.emit([sha256_mail_random, with_urls, urls_json])