import os

os.environ["MONITOR_SERVICE_NAME"] = "otlp_example"
os.environ["LOGFIRE_WRITE_TOKEN"] = (
    "Your logfire write token, "
    "create guide refer to "
    "https://logfire.pydantic.dev/docs/how-to-guides/create-write-tokens/"
)

import aworld.trace as trace
from aworld.logs.util import logger

@trace.func_span(span_name="test_func", attributes={"test_attr": "test_value"}, extract_args=["param1"], add_attr = "add_attr_value")
def traced_func(param1: str = None, param2: int = None):
    logger.info("this is a traced func")
    traced_func2(param1="func2_param1_value", param2=222)
    traced_func3(param1="func3_param1_value", param2=333)

@trace.func_span(span_name="test_func_2", add_attr = "add_attr_value")
def traced_func2(param1: str = None, param2: int = None):
    logger.info("this is a traced func2")

@trace.func_span
def traced_func3(param1: str = None, param2: int = None):
    logger.info("this is a traced func3")

def main():

    logger.info("this is a no trace log")

    trace.auto_tracing("examples.trace.*", 0.01)

    with trace.span("hello") as span:
        span.set_attribute("parent_test_attr", "pppppp")
        logger.info("hello aworld")
        with trace.span("child hello") as span2:
            span2.set_attribute("child_test_attr", "cccccc")
            logger.info("child hello aworld")
            current_span = trace.get_current_span()
            logger.info("trace_id=%s", current_span.get_trace_id())

    traced_func(param1="func1_param1_value", param2=111)

    # from examples.trace.autotrace_demo import TestClassB
    # b = TestClassB()
    # b.classb_function_1()
    # b.classb_function_2()
    # b.classb_function_1()
    # b.classb_function_2()


if __name__ == "__main__":
    main()
