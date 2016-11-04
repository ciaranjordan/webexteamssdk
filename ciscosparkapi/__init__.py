# -*- coding: utf-8 -*-
"""Python API wrapper for the Cisco Spark APIs."""


from __future__ import absolute_import
from builtins import object
from six import string_types

import os

from .exceptions import ciscosparkapiException, SparkApiError
from .restsession import RestSession
from .api.accesstokens import AccessToken, AccessTokensAPI
from .api.people import Person, PeopleAPI
from .api.rooms import Room, RoomsAPI
from .api.memberships import Membership, MembershipsAPI
from .api.messages import Message, MessagesAPI
from .api.teams import Team, TeamsAPI
from .api.teammemberships import TeamMembership, TeamMembershipsAPI
from .api.webhooks import Webhook, WebhooksAPI


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"


# Versioneer version control
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


DEFAULT_BASE_URL = 'https://api.ciscospark.com/v1/'
DEFAULT_TIMEOUT = 60


class CiscoSparkAPI(object):
    """Cisco Spark API wrapper.

    Creates a 'session' for all API calls through a created CiscoSparkAPI
    object.  The 'session' handles authentication, provides the needed headers,
    and checks all responses for error conditions.

    CiscoSparkAPI wraps all of the individual Cisco Spark APIs and represents
    them in a simple hierarchical structure.

    :CiscoSparkAPI: :class:`people <PeopleAPI>`

                    :class:`rooms <RoomsAPI>`

                    :class:`memberships <MembershipsAPI>`

                    :class:`messages <MessagesAPI>`

                    :class:`teams <TeamsAPI>`

                    :class:`team_memberships <TeamMembershipsAPI>`

                    :class:`webhooks <WebhooksAPI>`

                    :class:`access_tokens <AccessTokensAPI>`

    """

    def __init__(self, access_token=None, base_url=DEFAULT_BASE_URL,
                 timeout=DEFAULT_TIMEOUT):
        """Create a new CiscoSparkAPI object.

        An access token must be used when interacting with the Cisco Spark API.
        This package supports two methods for you to provide that access token:

          1. You may manually specify the access token via the access_token
             argument, when creating a new CiscoSparkAPI object.

          2. If an access_token argument is not supplied, the package checks
             for a SPARK_ACCESS_TOKEN environment variable.

        A ciscosparkapiException is raised if an access token is not provided
        via one of these two methods.

        Args:
            access_token(string_types): The access token to be used for API
                calls to the Cisco Spark service.  Defaults to checking for a
                SPARK_ACCESS_TOKEN environment variable.
            base_url(string_types): The base URL to be prefixed to the
                individual API endpoint suffixes.
                Defaults to ciscosparkapi.DEFAULT_BASE_URL.
            timeout(int): Timeout (in seconds) for RESTful HTTP requests.
                Defaults to ciscosparkapi.DEFAULT_TIMEOUT.

        Returns:
            CiscoSparkAPI: A new CiscoSparkAPI object.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If an access token is not provided via the
                access_token argument or SPARK_ACCESS_TOKEN environment
                variable.

        """
        # Process args
        assert access_token is None or isinstance(access_token, string_types)
        assert isinstance(base_url, string_types)
        assert isinstance(timeout, int)
        spark_access_token = os.environ.get('SPARK_ACCESS_TOKEN', None)
        access_token = access_token if access_token else spark_access_token
        if not access_token:
            error_message = "You must provide an access token to interact " \
                            "with the Cisco Spark APIs, either via the " \
                            "access_token argument or via a " \
                            "SPARK_ACCESS_TOKEN environment variable.  " \
                            "None provided."
            raise ciscosparkapiException(error_message)
        session_args = {u'timeout': timeout}

        # Create the API session
        # All of the API calls associated with a CiscoSparkAPI object will
        # leverage a single RESTful 'session' connecting to the Cisco Spark
        # cloud.
        self._session = RestSession(access_token, base_url, **session_args)

        # Spark API wrappers
        self.people = PeopleAPI(self._session)
        self.rooms = RoomsAPI(self._session)
        self.memberships = MembershipsAPI(self._session)
        self.messages = MessagesAPI(self._session)
        self.teams = TeamsAPI(self._session)
        self.team_memberships = TeamMembershipsAPI(self._session)
        self.webhooks = WebhooksAPI(self._session)
        self.access_tokens = AccessTokensAPI(self.base_url, timeout=timeout)

    @property
    def access_token(self):
        return self._session.access_token

    @property
    def base_url(self):
        return self._session.base_url

    @property
    def timeout(self):
        return self._session.timeout
