from typing import Any, Dict
from .base import BaseAI
from .types import BilibiliResult

class BilibiliAI(BaseAI):
    """B站热榜AI功能"""
    
    def ai_bilibili(self, password: str) -> BilibiliResult:
        """获取B站热榜
        
        Args:
            password: 访问密码
            
        Returns:
            BilibiliResult: 包含热榜信息的字典
            
        Raises:
            ValueError: 当输入参数无效时
        """
        if not password or not isinstance(password, str):
            raise ValueError("password必须是有效的字符串")
            
        parameters = {
            "choose": "AI_BLRANKING",
            "input": "1"
        }
        
        result = self._execute_workflow(password, parameters, max_retries=5)
        
        if "error" in result:
            return {"ranking": result["error"]}
        return result

    def _parse_output(self, output: Any) -> BilibiliResult:
        """解析B站热榜输出
        
        Args:
            output: 工作流返回的输出
            
        Returns:
            BilibiliResult: 解析后的结果
        """
        if isinstance(output, dict):
            if 'data' in output and 'list' in output['data']:
                # 提取热搜列表
                hot_list = output['data']['list']
                # 将热搜列表转换为字符串格式
                ranking_text = "\n".join([
                    f"{i+1}. {item['show_name']}"
                    for i, item in enumerate(hot_list)
                ])
                return {"ranking": ranking_text}
            return {"ranking": str(output)}
        elif isinstance(output, str):
            return {"ranking": output}
        return {"ranking": str(output)} 