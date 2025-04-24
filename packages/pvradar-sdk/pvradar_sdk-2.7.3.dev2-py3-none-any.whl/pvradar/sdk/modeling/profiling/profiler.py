import time
from dataclasses import asdict
from typing import Any, Callable, Optional

from ...display.jupyter_helpers import display_flowchart, FlowchartRenderer
from ...display.describe import ObjectDescription
from ...common.pandas_utils import is_series_or_frame
from ..base_model_context import BaseModelContext
from .profiling_types import ModelRunStats
from .origin_collector import origin_collector_output_filter
from ...display.flowchart import origin_tree_to_flowchart


class PvradarProfiler:
    def __init__(self, context: BaseModelContext):
        self.context = context
        self.original_run = context.run
        self.model_stats_dict: dict[str, ModelRunStats] = {}
        self._wrap_context_run()
        self._add_origin_collector()
        self.last_result: Any = None

    def _add_origin_collector(self):
        for filter in self.context.output_filters:
            if filter == origin_collector_output_filter:
                return
        self.context.output_filters.append(origin_collector_output_filter)

    def _remove_origin_collector(self):
        self.context.output_filters = [
            filter for filter in self.context.output_filters if filter != origin_collector_output_filter
        ]

    def _wrap_context_run(self):
        def run_with_profiler(model: Callable | str, *args, **kwargs):
            start_time = time.time()
            result = self.original_run(model, *args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time

            model_wrapper = self.context.wrap_model(model)
            model_name = model_wrapper.name

            if model_name not in self.model_stats_dict:
                self.model_stats_dict[model_name] = ModelRunStats(model_name)
            model_stat = self.model_stats_dict[model_name]
            model_stat.sum_execution_time += execution_time
            model_stat.call_count += 1
            if model_stat.min_execution_time is None or model_stat.min_execution_time > execution_time:
                model_stat.min_execution_time = execution_time
            if model_stat.max_execution_time is None or model_stat.max_execution_time < execution_time:
                model_stat.max_execution_time = execution_time

            if is_series_or_frame(result):
                result.attrs['model_run_stats'] = asdict(model_stat)

            self.last_result = result
            return result

        self.context.run = run_with_profiler

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.context.run = self.original_run
        self._remove_origin_collector()

    def stats_summary(self, top: Optional[int] = None) -> ObjectDescription:
        # get stats list ordered by total execution time
        stats_list = list(self.model_stats_dict.values())
        stats_list.sort(key=lambda x: x.sum_execution_time, reverse=True)

        result = ''

        counter = 0
        for model_stat in stats_list:
            result += f'{model_stat.model_name.ljust(50)}: {model_stat.sum_execution_time:.3f}s\n'
            if model_stat.call_count > 1:
                result += (
                    f'  times: {model_stat.call_count}'.ljust(15)
                    + f'(min: {model_stat.min_execution_time:.6f}s, '.ljust(15)
                    + f'max: {model_stat.max_execution_time:.6f}s)'.ljust(15)
                    + '\n'
                )
            if top and counter >= top:
                break
            counter += 1

        return ObjectDescription(result)

    def make_flowchart_script(
        self,
        resource: Any = None,
        *,
        show_execution_time: bool = False,
        use_theme: bool | str = True,
        show_model_name: bool = False,
        show_use_count: bool = False,
        carry_over_letters: int = 30,
        max_depth: Optional[int] = None,
        show_nested_databases: bool = False,
    ) -> str:
        if resource is None:
            resource = self.last_result
        if not is_series_or_frame(resource):
            raise ValueError(
                f'Resource must be a pandas Series or DataFrame, since origins are collected in attrs, got: {resource.__class__.__name__}'
            )
        script = origin_tree_to_flowchart(
            resource,
            model_stats_dict=self.model_stats_dict if show_execution_time else None,
            use_theme=use_theme,
            show_model_name=show_model_name,
            show_use_count=show_use_count,
            carry_over_letters=carry_over_letters,
            max_depth=max_depth,
            show_nested_databases=show_nested_databases,
        )
        return script

    @staticmethod
    def wrap(context: BaseModelContext):
        return PvradarProfiler(context)

    def display_flowchart(
        self,
        show_execution_time: bool = False,
        use_theme: bool | str = True,
        show_model_name: bool = False,
        show_use_count: bool = False,
        carry_over_letters: int = 30,
        max_depth: Optional[int] = None,
        show_nested_databases: bool = False,
        renderer: Optional[FlowchartRenderer] = None,
    ):
        flowchart_script = self.make_flowchart_script(
            self.last_result,
            show_execution_time=show_execution_time,
            use_theme=use_theme,
            show_model_name=show_model_name,
            show_use_count=show_use_count,
            carry_over_letters=carry_over_letters,
            max_depth=max_depth,
            show_nested_databases=show_nested_databases,
        )
        display_flowchart(flowchart_script, renderer=renderer)
