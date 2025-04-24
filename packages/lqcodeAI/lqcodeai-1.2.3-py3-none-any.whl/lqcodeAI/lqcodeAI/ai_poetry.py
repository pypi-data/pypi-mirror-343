from typing import Any, Dict
from .base import BaseAI
from .types import PoetryResult

class PoetryAI(BaseAI):
    """藏头诗AI功能"""
    
    def ai_poetry(self, password: str, message: str = "李梅") -> PoetryResult:
        """生成藏头诗
        
        Args:
            password: 访问密码
            message: 藏头诗内容，默认为"李梅"
            
        Returns:
            PoetryResult: 包含诗和解释的字典
            
        Raises:
            ValueError: 当输入参数无效时
        """
        if not password or not isinstance(password, str):
            raise ValueError("password必须是有效的字符串")
        if not message or not isinstance(message, str):
            raise ValueError("message必须是有效的字符串")
            
        parameters = {
            "input": message,
            "choose": "AI_POETY",
        }
        result = self._execute_workflow(password, parameters, max_retries=5)
        if "error" in result:
            return {"poem": result["error"], "explanation": ""}
        return result

    def _parse_output(self, output: Any) -> PoetryResult:
        """解析藏头诗输出
        
        Args:
            output: 工作流返回的输出
            
        Returns:
            PoetryResult: 解析后的结果
        """
        if isinstance(output, dict):
            return {
                "poem": output.get('poety', ""),
                "explanation": output.get('explain', "")
            }
        return {"poem": str(output), "explanation": ""} 