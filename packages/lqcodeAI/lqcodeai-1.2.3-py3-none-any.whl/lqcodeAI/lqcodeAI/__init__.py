"""
名称:绿旗编程AI课程SDK

说明:这个模块提供了与绿旗编程AI服务交互的接口。
"""

from .types import PoetryResult, WeatherResult, BilibiliResult, IdiomsResult, SnackPropsResult
from .ai_poetry import PoetryAI
from .ai_weather import WeatherAI
from .ai_biliranking import BilibiliAI
from .ai_idioms import IdiomsAI
from .config import Config
from .ai_chatroom import ChatRoomAI
from .ai_snackprops import SnackPropsAI
class LqcodeAI:
    """绿旗编程AI功能的主要接口类"""
    
    def __init__(self, config=None):
        self.config = config or Config()
        self.poetry_ai = PoetryAI(self.config)
        self.weather_ai = WeatherAI(self.config)
        self.bilibili_ai = BilibiliAI(self.config)
        self.idioms_ai = IdiomsAI(self.config)
        self.chatroom_ai = ChatRoomAI(self.config)
        self.snackprops_ai = SnackPropsAI(self.config)
    def ai_poetry(self, password: str, message: str) -> PoetryResult:
        """生成藏头诗"""
        return self.poetry_ai.ai_poetry(password, message)
    
    def ai_weather(self, password: str, message: str) -> WeatherResult:
        """查询天气信息"""
        return self.weather_ai.ai_weather(password, message)
        
    def ai_biliranking(self, password: str) -> BilibiliResult:
        """获取B站热榜"""
        return self.bilibili_ai.ai_bilibili(password)
        
    def ai_idioms(self, password: str, message: str) -> IdiomsResult:
        """进行成语接龙"""
        return self.idioms_ai.ai_idioms(password, message)
    
    def ai_snackprops(self, password: str, preferences: str = "甜食") -> SnackPropsResult:
        """零食道具"""
        return self.snackprops_ai.ai_snackprops(password, preferences)
# 创建单例实例
lq = LqcodeAI()

# 导出类和实例
__all__ = [
    'ChatRoomAI',
    'PoetryAI',
    'WeatherAI',
    'IdiomsAI',
    'BilibiliAI',
    'lq'
] 