# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Annotated

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self

from ibm_watsonx_gov.entities.credentials import (OpenAICredentials,
                                                  WxAICredentials)
from ibm_watsonx_gov.entities.enums import ModelProviderType


class ModelProvider(BaseModel):
    type_: ModelProviderType = Field(alias="type")


class WxAIModelProvider(ModelProvider):
    type_: ModelProviderType = Field(
        default=ModelProviderType.IBM_WATSONX_AI,
        alias="type"
    )
    credentials: WxAICredentials | None = None

    @model_validator(mode="after")
    def create_credentials_from_env(self) -> Self:
        if self.credentials is None:
            try:
                self.credentials = WxAICredentials.create_from_env()
            except ValueError:
                self.credentials = None
        return self


class OpenAIModelProvider(ModelProvider):
    type_: ModelProviderType = ModelProviderType.OPENAI
    credentials: Annotated[OpenAICredentials | None, Field(
        description="OpenAI credentials. This can also be set by using `OPENAI_API_KEY` environment variable.", default=None)]

    @model_validator(mode="after")
    def create_credentials_from_env(self) -> Self:
        if self.credentials is None:
            self.credentials = OpenAICredentials.create_from_env()
        return self


class CustomModelProvider(ModelProvider):
    type_: ModelProviderType = Field(
        default=ModelProviderType.CUSTOM,
        alias="type",
    )
