
# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


from ibm_cloud_sdk_core.authenticators import (CloudPakForDataAuthenticator,
                                               IAMAuthenticator)
from ibm_watson_openscale import APIClient as WOSClient

from ibm_watsonx_gov.entities.credentials import Credentials
from ibm_watsonx_gov.utils.url_mapping import WOS_URL_MAPPING


class APIClient():
    """
    The IBM watsonx.governance sdk client. It is required to access the watsonx.governance APIs.
    """

    def __init__(self, credentials: Credentials | None = None):
        self.credentials = credentials

        if self.credentials.version:
            authenticator = CloudPakForDataAuthenticator(url=self.credentials.url,
                                                         username=self.credentials.username,
                                                         apikey=self.credentials.api_key,
                                                         disable_ssl_verification=self.credentials.disable_ssl
                                                         )
        else:
            url_map = WOS_URL_MAPPING.get(self.credentials.url)
            if not url_map:
                raise ValueError(
                    f"Invalid url {self.credentials.url}. Please provide openscale service url.")

            authenticator = IAMAuthenticator(apikey=self.credentials.api_key,
                                             url=url_map.iam_url,
                                             disable_ssl_verification=self.credentials.disable_ssl)

        self.wos_client = WOSClient(
            authenticator=authenticator,
            service_url=self.credentials.url,
            service_instance_id=self.credentials.service_instance_id,
        )

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Setter for credentials object. If not provided, it will create a credentials object from environment variables.
        """
        if not credentials:
            self._credentials = Credentials.create_from_env()
        else:
            self._credentials = credentials
