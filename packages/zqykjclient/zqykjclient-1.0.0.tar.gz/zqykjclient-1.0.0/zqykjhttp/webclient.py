from typing import Dict, List

import requests
from requests.exceptions import HTTPError


def _handle_response(response: requests.Response):
    try:
        response.raise_for_status()
    except HTTPError as e:
        # 尝试解析错误详情
        try:
            error_info = response.json()
            raise FinanceAPIError(
                f"API request failed: {error_info.get('message', 'Unknown error')}",
                status_code=response.status_code,
                detail=error_info
            ) from e
        except ValueError:
            raise FinanceAPIError(
                f"API request failed with status {response.status_code}",
                status_code=response.status_code
            ) from e
    return response.json().get('result')


class ModelClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get_rule_info(self, rule_id: str) -> Dict:
        """获取规则详情"""
        url = f"{self.base_url}/finance/model-sys/outapi/rule/{rule_id}"
        response = self.session.get(url, timeout=self.timeout)
        return _handle_response(response)

    def list_rules(self) -> List[Dict]:
        """获取已发布规则列表"""
        url = f"{self.base_url}/finance/model-sys/outapi/rule/list"
        response = self.session.get(url, timeout=self.timeout)
        return _handle_response(response)

    def get_model_info(self, model_id: str) -> Dict:
        """获取模型详情"""
        url = f"{self.base_url}/finance/model-sys/outapi/model/{model_id}"
        response = self.session.get(url, timeout=self.timeout)
        return _handle_response(response)

    def list_models(self) -> List[Dict]:
        """获取所有模型列表"""
        url = f"{self.base_url}/finance/model-sys/outapi/model/list"
        response = self.session.get(url, timeout=self.timeout)
        return _handle_response(response)

    def get_task_info(self, task_id: str) -> Dict:
        """获取任务详情"""
        url = f"{self.base_url}/finance/model-sys/outapi/task/{task_id}"
        response = self.session.get(url, timeout=self.timeout)
        return _handle_response(response)

    def stop_task(self, task_id: str) -> None:
        """终止任务"""
        url = f"{self.base_url}/finance/model-sys/outapi/task/stop/{task_id}"
        response = self.session.get(url, timeout=self.timeout)
        _handle_response(response)

    # 以下方法处理协议相关接口
    def get_rule_protocol(self, rule_id: str) -> Dict:
        """获取规则协议"""
        url = f"{self.base_url}/finance/model-sys/outapi/task/rule/{rule_id}/protocol"
        response = self.session.post(url, timeout=self.timeout)
        return _handle_response(response)

    def execute_rule_protocol(self, protocol_data: Dict) -> str:
        """执行规则协议"""
        url = f"{self.base_url}/finance/model-sys/outapi/task/rule/execute"
        response = self.session.post(url, json=protocol_data, timeout=self.timeout)
        return _handle_response(response)

    def get_model_protocol(self, model_id: str) -> Dict:
        """获取模型协议"""
        url = f"{self.base_url}/finance/model-sys/outapi/task/model/{model_id}/protocol"
        response = self.session.post(url, timeout=self.timeout)
        return _handle_response(response)

    def execute_model_protocol(self, protocol_data: Dict) -> str:
        """执行模型协议"""
        url = f"{self.base_url}/finance/model-sys/outapi/task/model/execute"
        response = self.session.post(url, json=protocol_data, timeout=self.timeout)
        return _handle_response(response)


class FinanceAPIError(Exception):
    """自定义API异常"""

    def __init__(self, message: str, status_code: int = None, detail: Dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail
