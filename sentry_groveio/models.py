"""
sentry_groveio.models
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by Matt Robenolt, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import forms

from sentry.conf import settings
from sentry.plugins import Plugin, register

import urllib
import urllib2
import logging
from django.utils import simplejson as json

logger = logging.getLogger('sentry.plugins.groveio')


class GroveIoOptionsForm(forms.Form):
    token = forms.CharField(help_text="Your Grove.io channel token.")
    service_name = forms.CharField(help_text="Name of the service (displayed in the message)", initial='Sentry')
    url = forms.CharField(help_text="(Optional) Service URL for the web client", required=False)
    icon_url = forms.CharField(help_text="(Optional) Icon for the service", required=False)


@register
class GroveIoMessage(Plugin):
    author = 'Matt Robenolt'
    author_url = 'https://github.com/mattrobenolt/sentry-groveio'
    title = 'Grove.io'
    slug = 'grove-io'
    conf_key = 'groveio'
    description = 'Send errors to Grove.io'
    version = '0.1.1'
    project_conf_form = GroveIoOptionsForm

    def is_configured(self, project):
        return all((self.get_option(k, project) for k in ('token', 'service_name')))

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        if not is_new:
            return
        token = self.get_option('token', event.project)
        service = self.get_option('service_name', event.project)
        if token and service:
            message = '[%s] %s: %s' % (event.server_name, event.get_level_display().upper(), event.error().encode('utf-8').split('\n')[0])
            self.send_payload(token, service, event, group, message)

    def send_payload(self, token, service, event, group, message):
        url = "https://grove.io/api/notice/%s/" % token
        values = {
            'service': service,
            'message': message,
            'url': '%s/%d/group/%d/' % (settings.URL_PREFIX, group.project_id, group.id),
            'icon_url': self.get_option('icon_url', event.project)
        }

        # Can we just use `requests' please?
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            logger.error('Could not connect to Grove.io')
        except urllib2.HTTPError, e:
            try:
                error = json.loads(e.read())
            except json.decoder.JSONDecodeError:
                logger.error('Something bad happened with Grove. :(')
            if 'error' in error:
                logger.error(error['error'])
            else:
                logger.error('Something bad happened with Grove. :(')
        response.read()
