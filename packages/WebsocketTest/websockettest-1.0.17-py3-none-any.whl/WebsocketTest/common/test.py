import websockets
from functools import cached_property
import asyncio
from WebsocketTest.common.utils import *
import allure
from pathlib import Path
from WebsocketTest.common.Assertion import Assert
import pytest
import traceback


CASE_PATH = Path.cwd().resolve().joinpath("data/case_data.xlsx")
@pytest.fixture
def sheet_name(request):
    """动态获取 sheet_name"""
    service = request.config.getoption("--service")
    project = request.config.getoption("--project")
    return f"{project}_{service}"

@pytest.fixture
def case_suite(sheet_name):
    """生成测试数据"""
    return gen_case_suite(CASE_PATH, sheet_name)

class BaseApiTest:
    def test(self, case_suite, setup_env):
        """测试用例执行模板"""
        try:
            params = merge_dicts(case_suite, setup_env)
            runner = self.API_TEST_RUNNER_CLASS(**params)
            runner.run()
            self._record_allure_report(runner)
            self._execute_assertions(runner, case_suite)
        except Exception as e:
            self._record_error(e)
            raise