from typing import Any, Dict
from .base import BaseAI
from .types import IdiomsResult

class IdiomsAI(BaseAI):
    """成语接龙AI功能"""
    
    def ai_idioms(self, password: str, message: str = "一马当先") -> IdiomsResult:
        """进行成语接龙
        
        Args:
            password: 访问密码
            message: 起始成语，默认为"一马当先"
            
        Returns:
            IdiomsResult: 包含接龙结果和解释的字典
            
        Raises:
            ValueError: 当输入参数无效时
        """
        if not password or not isinstance(password, str):
            raise ValueError("password必须是有效的字符串")
        if not message or not isinstance(message, str):
            raise ValueError("message必须是有效的字符串")
            
        parameters = {
            "input": message,
            "choose": "AI_IDIOMS",
        }
        result = self._execute_workflow(password, parameters, max_retries=5)
        if "error" in result:
            return {"idiom": result["error"], "explanation": ""}
        return result

    def _parse_output(self, output: Any) -> IdiomsResult:
        """解析成语接龙输出
        
        Args:
            output: 工作流返回的输出
            
        Returns:
            IdiomsResult: 解析后的结果
        """
        if isinstance(output, dict):
            if 'data' in output:
                # 从data字段获取成语
                idiom = output['data']
                # 生成简单的解释
                explanation = f"这个成语的意思是：{idiom}。"
                return {
                    "idiom": idiom,
                    "explanation": explanation
                }
            return {
                "idiom": output.get('idiom', ""),
                "explanation": output.get('explain', "")
            }
        return {"idiom": str(output), "explanation": ""}
