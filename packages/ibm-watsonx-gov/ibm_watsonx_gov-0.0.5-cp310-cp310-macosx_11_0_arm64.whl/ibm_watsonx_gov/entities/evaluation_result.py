# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


from typing import Annotated, Any

import pandas as pd
from pydantic import BaseModel, Field

from ibm_watsonx_gov.entities.base_classes import BaseMetricResult


class RecordMetricResult(BaseMetricResult):
    record_id: Annotated[str, Field(
        description="The record identifier.", examples=["record1"])]
    record_timestamp: Annotated[str | None, Field(
        description="The record timestamp.", examples=["2025-01-01T00:00:00.000000Z"], default=None)]


class ToolMetricResult(RecordMetricResult):
    tool_name: Annotated[str, Field(
        title="Tool Name", description="Name of the tool for which this result is computed.")]
    execution_count: Annotated[int, Field(
        title="Execution count", description="The execution count for this tool name.", gt=0, default=1)]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            return False

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) == \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            raise NotImplemented

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) < \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            raise NotImplemented

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) > \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            raise NotImplemented

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) <= \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            raise NotImplemented

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) >= \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)


class AggregateMetricResult(BaseMetricResult):
    min: float | None = None
    max: float | None = None
    mean: float | None = None
    total_records: int
    record_level_metrics: list[RecordMetricResult] = []


class MetricsEvaluationResult(BaseModel):
    metrics_result: list[AggregateMetricResult]

    def to_json(self, indent: int | None = None, **kwargs):
        """
        Transform the metrics evaluation result to a json.
        The kwargs are passed to the model_dump_json method of pydantic model. All the arguments supported by pydantic model_dump_json can be passed.

        Args:
            indent (int, optional): The indentation level for the json. Defaults to None.

        Returns:
            string of the result json.
        """
        if kwargs.get("exclude_unset") is None:
            kwargs["exclude_unset"] = True
        return self.model_dump_json(
            exclude={
                "metrics_result": {
                    "__all__": {
                        "record_level_metrics": {
                            "__all__": {"provider", "name", "method", "group"}
                        }
                    }
                }
            },
            indent=indent,
            **kwargs,
        )

    def to_df(self, data: pd.DataFrame | None = None) -> pd.DataFrame:
        """
        Transform the metrics evaluation result to a dataframe.

        Args:
            data (pd.DataFrame): the input dataframe, when passed will be concatenated to the metrics result

        Returns:
            pd.DataFrame: new dataframe of the input and the evaluated metrics
        """
        values_dict: dict[str, list[float | str | bool]] = {}
        for result in self.metrics_result:
            values_dict[f"{result.name}.{result.method}" if result.method else result.name] = [
                record_metric.value for record_metric in result.record_level_metrics]

        if data is None:
            return pd.DataFrame.from_dict(values_dict)
        else:
            return pd.concat([data, pd.DataFrame.from_dict(values_dict)], axis=1)

    def to_dict(self) -> list[dict]:
        """
        Transform the metrics evaluation result to a list of dict containing the record level metrics.
        """
        result = []
        for aggregate_metric_result in self.metrics_result:
            for record_level_metric_result in aggregate_metric_result.record_level_metrics:
                result.append(record_level_metric_result.model_dump())
        return result
