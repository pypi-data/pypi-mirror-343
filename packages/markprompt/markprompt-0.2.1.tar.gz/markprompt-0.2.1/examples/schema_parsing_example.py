"""
使用 MarkPrompt 的 response_format 和 schema 解析功能的示例。
"""

import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field

from openai import OpenAI

from markprompt import MarkPromptClient
from markprompt.core.logger import setup_logger

# 配置日志
logger = setup_logger(__name__)

# OpenAI配置
api_key = os.environ.get("OPENAI_API_KEY", "sk-...")  # 替换为你的API密钥
base_url = "http://127.0.0.1:10240/v1"  # 或你的自定义基础URL

openai = OpenAI()

# 定义响应模型
class MovieReview(BaseModel):
    """电影评论结构"""
    title: str = Field(description="电影标题")
    year: int = Field(description="电影发行年份")
    rating: float = Field(description="评分（0-10）")
    review: str = Field(description="评论内容")
    pros: List[str] = Field(description="优点列表")
    cons: List[str] = Field(description="缺点列表")
    recommended: bool = Field(description="是否推荐")
    suitable_for: Optional[List[str]] = Field(None, description="适合人群")


# 定义简单的模板内容（由于无法访问 prompts 目录，这里直接使用字符串）
template_content = """---
metadata:
  name: 电影评论家
  description: 根据用户输入的电影名称生成详细评论
provider:
  name: default
generation_config:
  model: gpt-4.1
  temperature: 0.7
---

你是一个专业电影评论家。请根据用户提供的电影名称，提供详细的评论。

system:
请以专业电影评论家的身份，根据用户提供的电影名称，编写一篇详细的评论。

user:
{{user_input}}
"""


def demonstrate_schema_parsing():
    """演示 Schema 解析功能"""
    # 创建一个临时模板文件
    import tempfile
    import inspect
    import json  # 在函数内部再次导入以确保访问
    
    # 打印调试信息
    print("\n===== MovieReview 类信息 =====")
    print(f"MovieReview 是否是 BaseModel 的子类: {issubclass(MovieReview, BaseModel)}")
    print(f"MovieReview.__class__.__name__: {MovieReview.__class__.__name__}")
    print(f"MovieReview 类的 MRO: {[cls.__name__ for cls in MovieReview.mro()]}")
    print(f"MovieReview Schema: {json.dumps(MovieReview.model_json_schema(), indent=2, ensure_ascii=False)}")
    print("\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 写入模板文件
        template_path = os.path.join(temp_dir, "movie_reviewer.md")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)
        
        # 创建客户端
        client = MarkPromptClient(
            template_dir=temp_dir,
            client=openai
        )
       
        try:
            # 准备用户问题
            user_question = "请评价电影《泰坦尼克号》"

            # 使用 schema 解析
            print("\n正在生成带结构的电影评论...")
            try:
                response = client.generate(
                    "movie_reviewer",  # 使用电影评论模板
                    user_question,  # 用户问题
                    response_format=MovieReview,  # 传递 BaseModel
                    verbose=True  # 启用详细日志
                )
            except Exception as e:
                print(f"生成过程中出现错误: {e}")
                # 尝试使用 JSON 模式提供更多信息
                response = client.generate(
                    "movie_reviewer",  # 使用电影评论模板
                    user_question,  # 用户问题
                    response_format={"type": "json_object", "schema": MovieReview.model_json_schema()},
                    verbose=True  # 启用详细日志
                )
            
            # 输出结果
            print("\n===== 结构化电影评论 =====")
            print(f"\n返回类型: {type(response)}")
            
            # 处理不同类型的响应
            if hasattr(response, 'choices') and len(response.choices) > 0:
                # 标准OpenAI响应
                print(f"\n原始返回内容: {response.choices[0].message.content}")
                # 尝试解析JSON
                try:
                    content = response.choices[0].message.content
                    movie_data = json.loads(content)
                    review = MovieReview(**movie_data)
                    print(f"\n解析后的MovieReview对象: {review}")
                except Exception as e:
                    print(f"解析JSON失败: {e}")
            elif hasattr(response, 'model_dump'):
                # Pydantic 模型
                print(f"\n解析后的MovieReview对象: {response}")
                print(f"\n模型JSON: {response.model_dump_json()}")
            else:
                # 其他类型
                print(f"\n无法识别的响应类型: {response}")
            
            # 查看并打印 response 中的原始内容
            print(f"\nresponse 类型: {type(response)}")
            print(f"response 可用方法和属性: {dir(response)[:10]}...")
            
            movie_review = None
            
            # 方法1: 尝试直接从ParsedChatCompletion中提取model对象
            try:
                if hasattr(response, 'model') and response.model is not None:
                    print(f"\n尝试访问 response.model: {response.model}")
                    # 如果返回的是ParsedChatCompletion[MovieReview]对象，其model属性可能包含所需的数据
            except Exception as e:
                print(f"\n访问 model 属性失败: {str(e)}")
                
            # 方法2: 尝试直接访问response.choices[0].message.content并解析JSON
            try:
                if hasattr(response, 'choices') and response.choices:
                    print(f"\n尝试通过 choices[0].message.content 获取数据")
                    json_str = response.choices[0].message.content
                    import json
                    data = json.loads(json_str)
                    movie_review = MovieReview(**data)
                    print(f"\n成功从 JSON 构建 MovieReview 对象: {movie_review.__class__.__name__}")
            except Exception as e:
                print(f"\n通过 choices 获取数据失败: {str(e)}")
                
            # 方法3: 如枟response自身就已经是相关类型，尝试直接使用
            if not movie_review and hasattr(response, 'model_dump'):
                try:
                    print("\n尝试调用 model_dump获取数据")
                    data = response.model_dump()
                    print(f"model_dump 返回内容: {data.keys() if isinstance(data, dict) else 'Not a dict'}")                    
                    if 'choices' in data and data['choices']:
                        content = data['choices'][0]['message']['content']
                        if isinstance(content, str):
                            data = json.loads(content)
                            movie_review = MovieReview(**data)
                            print(f"\n成功从model_dump结果中提取并构建 MovieReview")
                except Exception as e:
                    print(f"\n使用 model_dump 提取数据失败: {str(e)}")
                
            if movie_review:
                print("\n===== 提取后的电影信息 =====")
                try:
                    print(f"电影: {movie_review.title} ({movie_review.year})")
                    print(f"评分: {movie_review.rating}/10")
                    print(f"推荐: {'是' if movie_review.recommended else '否'}")
                    print(f"优点: {', '.join(movie_review.pros)}")
                    print(f"缺点: {', '.join(movie_review.cons)}")
                    print(f"适合人群: {', '.join(movie_review.suitable_for or ['所有人'])}")
                    print(f"评论: {movie_review.review}")
                except Exception as e:
                    print(f"\n获取属性时出错: {str(e)}")
                    # 打印对象结构
                    print(f"\n对象属性: {dir(movie_review)}")
                    
            else:
                print("\n无法提取结构化数据。返回对象属性:")
                print(dir(response))
            
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            logger.error("处理过程中发生错误", {
                "error": str(e),
                "traceback": error_traceback
            })
            print(f"\n错误详情: {str(e)}")
            print(error_traceback)


if __name__ == "__main__":
    demonstrate_schema_parsing()
