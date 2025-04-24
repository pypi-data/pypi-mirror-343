from typing import TypedDict

class PoetryResult(TypedDict):
    """藏头诗结果类型"""
    poem: str
    explanation: str

class WeatherResult(TypedDict):
    """天气查询结果类型"""
    weather_info: str
    explanation: str

class BilibiliResult(TypedDict):
    """B站热榜结果类型"""
    ranking: str

class IdiomsResult(TypedDict):
    """成语接龙结果类型"""
    idiom: str
    explanation: str

class SnackPropsResult(TypedDict):
    """零食推荐结果类型"""
    recommendations: str
    explanation: str 