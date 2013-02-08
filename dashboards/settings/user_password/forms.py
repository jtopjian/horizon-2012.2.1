# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pytz

from django import shortcuts
from django.conf import settings
from django.utils import translation
from django.contrib.auth import logout

from horizon import forms
from horizon import messages
from horizon import api

import requests
import json

class UserPasswordForm(forms.SelfHandlingForm):
    original_password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    new_password      = forms.CharField(max_length=50, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserPasswordForm, self).__init__(*args, **kwargs)

    def handle(self, request, data):
        response = shortcuts.redirect(request.build_absolute_uri())

        # variables
        user_id = request.session['user_id']
        username = request.session['username']

        # URLs
        keystone_url = api.url_for(request, 'identity', endpoint_type='publicURL')
        password_url = "%s/OS-KSCRUD/users/%s" % (keystone_url, user_id)
        token_url    = "%s/tokens" % keystone_url

        payload = {'user': {'original_password': data['original_password'], 'password': data['new_password']}}
        headers = {'X_Auth_Token': request.user.token.id, 'content-type': 'application/json'}
        r = requests.patch(password_url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
          messages.success(request, translation.ugettext("Password changed."))
          logout(request)
        else:
          messages.error(request, translation.ugettext("Password change failed."))

        return response
