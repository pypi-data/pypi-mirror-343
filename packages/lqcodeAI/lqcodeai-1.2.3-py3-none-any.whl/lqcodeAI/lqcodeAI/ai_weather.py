from typing import Any, Dict
from .base import BaseAI
from .types import WeatherResult

class WeatherAI(BaseAI):
    """天气查询AI功能"""
    
    def ai_weather(self, password: str, message: str = "北京") -> WeatherResult:
        """查询天气信息
        
        Args:
            password: 访问密码
            message: 城市名称，默认为"北京"
            
        Returns:
            WeatherResult: 包含天气信息和解释的字典
            
        Raises:
            ValueError: 当输入参数无效时
        """
        if not password or not isinstance(password, str):
            raise ValueError("password必须是有效的字符串")
        if not message or not isinstance(message, str):
            raise ValueError("message必须是有效的字符串")
            
        parameters = {
            "input": message,
            "choose": "AI_WEATHER",
        }
        result = self._execute_workflow(password, parameters)
        if "error" in result:
            return {"weather_info": result["error"], "explanation": ""}
        return result

    def _parse_output(self, output: Any) -> WeatherResult:
        """解析天气数据输出
        
        Args:
            output: 工作流返回的输出
            
        Returns:
            WeatherResult: 解析后的结果
        """
        if isinstance(output, dict) and 'data' in output:
            data_list = output['data']
            if isinstance(data_list, list) and len(data_list) > 0:
                weather_data = data_list[0]
                weather_info = f"""
城市：{weather_data.get('city', '未知')}
天气：{weather_data.get('weather_day', "未知")}
温度：{weather_data.get('temp_low', '?')}~{weather_data.get('temp_high', '?')}℃
湿度：{weather_data.get('humidity', '?')}%
风力：{weather_data.get('wind_dir_day', '未知')}{weather_data.get('wind_level_day', '?')}级
日期：{weather_data.get('predict_date', '未知')}
"""
                explanation = f"""
天气提示：
白天：{weather_data.get('weather_day', '未知')}
夜间：{weather_data.get('wind_dir_night', '未知')}{weather_data.get('wind_level_night', '?')}级
"""
                return {
                    "weather_info": weather_info,
                    "explanation": explanation
                }
        return {"weather_info": "无法解析天气数据", "explanation": ""} 