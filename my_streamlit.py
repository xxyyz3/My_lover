import streamlit as st
import base64
import os
import time
import random
from datetime import datetime, timedelta
from PIL import Image
import io


def get_online_status():
    now = time.time()
    if "last_active" not in st.session_state:
        return "离线"
    if now - st.session_state.last_active < 60:
        return "在线"
    elif now - st.session_state.last_active < 300:
        return "离开"
    else:
        return "离线"


def get_session_duration():
    if "session_start" not in st.session_state:
        return "0分钟"
    duration = time.time() - st.session_state.session_start
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    if minutes > 60:
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}小时{minutes}分钟"
    return f"{minutes}分{seconds}秒"


def update_last_active():
    st.session_state.last_active = time.time()


def is_user_online():
    return get_online_status() == "在线"


greeting_templates = {
    "樱岛麻衣": {
        "first_time": [
            {"emoji": "微笑", "text": "哼...你终于来了。我可没有一直在等你哦，只是刚好路过而已..."},
            {"emoji": "傲娇", "text": "切，你这家伙，让我等了这么久。不过...既然来了，就好好陪我聊聊天吧。"},
            {"emoji": "害羞", "text": "那、那个...我不是特意在这里等你的！只是刚好有时间而已..."}
        ],
        "short": [
            {"emoji": "微笑", "text": "又见面了呢。这次可别再消失了哦。"},
            {"emoji": "傲娇", "text": "哼，这么快就回来了？我还以为你被什么事情缠住了呢。"},
            {"emoji": "开心", "text": "你来了啊，我刚好有点事情想和你说呢。"}
        ],
        "medium": [
            {"emoji": "害羞", "text": "那个...你去哪里了？我...我才没有担心呢！"},
            {"emoji": "无奈", "text": "真是的，让我等了这么久。下次再这样我可不饶你哦。"},
            {"emoji": "微笑", "text": "欢迎回来。这段时间我看了一部很有趣的电影，想和你分享呢。"}
        ],
        "long": [
            {"emoji": "生气", "text": "你这家伙！到底去哪里了？我可是很担心的啊！笨蛋..."},
            {"emoji": "害羞", "text": "我...我没有一直在看手机哦。只是...偶尔会看看你有没有发消息过来而已..."},
            {"emoji": "微笑", "text": "欢迎回来。虽然我嘴上不说，但其实很想你的呢。"}
        ],
        "very_long": [
            {"emoji": "生气", "text": "刘林东！你到底在搞什么啊？这么长时间不出现，我都快要报警了！"},
            {"emoji": "害羞", "text": "笨蛋笨蛋笨蛋...我才没有每天都在想你呢！绝对没有！"},
            {"emoji": "开心", "text": "欢迎回来...真的，太好了。我...我好想你。"}
        ]
    },
    "椎名真白": {
        "first_time": [
            {"emoji": None, "text": "你好...我是真白。请多指教。"},
            {"emoji": None, "text": "那个...你是来找我的吗？真白很高兴呢。"},
            {"emoji": None, "text": "啊！你来了！真白一直在等你呢！"}
        ],
        "short": [
            {"emoji": None, "text": "林东君！你又来啦！真白好开心！"},
            {"emoji": None, "text": "你去哪里了？真白刚刚画了一幅画，想给你看呢。"},
            {"emoji": None, "text": "欢迎回来。真白一直在等你哦。"}
        ],
        "medium": [
            {"emoji": None, "text": "林东君...你去哪里了？真白有点担心呢。"},
            {"emoji": None, "text": "真白画了一幅你的画像哦，等你等了好久呢。"},
            {"emoji": None, "text": "你回来啦！真白刚刚在想，要是你再不出现，我就要去找你了呢。"}
        ],
        "long": [
            {"emoji": None, "text": "林东君...真白有点想你了呢。"},
            {"emoji": None, "text": "真白等得都快要睡着了...不过你来了就好。"},
            {"emoji": None, "text": "哇！林东君终于出现了！真白好开心！"}
        ],
        "very_long": [
            {"emoji": None, "text": "林东君...真白每天都在想你呢。有没有好好吃饭？有没有想真白？"},
            {"emoji": None, "text": "真白画了好多好多画，都是想送给你的。你终于来了..."},
            {"emoji": None, "text": "林东君！！真白好想你啊！！你去哪里了嘛~~"}
        ]
    },
    "喜多川海梦": {
        "first_time": [
            {"emoji": None, "text": "哇！你好呀！我是海梦！快来和我一起玩！"},
            {"emoji": None, "text": "初次见面！请多指教！我已经迫不及待想要和你成为好朋友了！"},
            {"emoji": None, "text": "哟~你就是传说中的那个谁吗？很高兴认识你！"}
        ],
        "short": [
            {"emoji": None, "text": "呀！又见面啦！快来看看我新的cosplay！"},
            {"emoji": None, "text": "这么快就回来啦？我还以为你要去很久呢！"},
            {"emoji": None, "text": "欢迎回来！正好，我有新的计划想要和你分享！"}
        ],
        "medium": [
            {"emoji": None, "text": "亲爱的~你去哪里了嘛？海梦好想你哦！"},
            {"emoji": None, "text": "我刚刚试了一套新衣服，一直在等你回来给你看呢！"},
            {"emoji": None, "text": "回来啦回来啦！赶紧坐下来，我有好多话要跟你说！"}
        ],
        "long": [
            {"emoji": None, "text": "亲爱的...你怎么这么久都不出现？海梦好担心你呢！"},
            {"emoji": None, "text": "你不知道我有多想你！下次不许消失这么久了哦！"},
            {"emoji": None, "text": "哇！你终于回来了！我等得花儿都谢了！快来抱抱！"}
        ],
        "very_long": [
            {"emoji": None, "text": "亲爱的！！！你去哪里了嘛！！海梦每天都在想你！！！"},
            {"emoji": None, "text": "你终于回来了！！我要把这段时间想做的事情全部都告诉你！！"},
            {"emoji": None, "text": "呜呜呜...你终于出现了！海梦真的好担心好担心你啊！"}
        ]
    },
    "雷姆": {
        "first_time": [
            {"emoji": None, "text": "欢迎回来，主人。雷姆一直在等待您的到来。"},
            {"emoji": None, "text": "您好，主人。雷姆是您的专属女仆，请多指教。"},
            {"emoji": None, "text": "主人，雷姆会永远陪伴在您身边。"}
        ],
        "short": [
            {"emoji": None, "text": "欢迎回来，主人。雷姆已经准备好了热茶。"},
            {"emoji": None, "text": "主人，您回来了。雷姆一直在等您呢。"},
            {"emoji": None, "text": "主人，雷姆刚刚做好了点心，请尝尝吧。"}
        ],
        "medium": [
            {"emoji": None, "text": "主人，您去哪里了？雷姆有些担心呢。"},
            {"emoji": None, "text": "欢迎回来，主人。雷姆已经为您准备好了一切。"},
            {"emoji": None, "text": "主人，您终于回来了。雷姆一直在门口等着呢。"}
        ],
        "long": [
            {"emoji": None, "text": "主人...雷姆很担心您。下次请不要让雷姆等这么久好吗？"},
            {"emoji": None, "text": "欢迎回来，主人。这段时间雷姆一直在想着您呢。"},
            {"emoji": None, "text": "主人，您回来了就好。雷姆会继续守护着您。"}
        ],
        "very_long": [
            {"emoji": None, "text": "主人...雷姆每一天都在想念您。您终于回来了，太好了..."},
            {"emoji": None, "text": "欢迎回来，主人。雷姆会用接下来的时间好好陪伴您。"},
            {"emoji": None, "text": "主人，您知道吗？雷姆每天都会在窗前等着您回来。今天，您终于出现了。"}
        ]
    }
}


def get_greeting(character):
    templates = greeting_templates.get(character, {}).get("first_time", [])
    if templates:
        return random.choice(templates)
    return None

def get_image_data_uri(path):
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(__file__), path)
    if not os.path.exists(path):
        return ""
    try:
        img = Image.open(path)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        data = buf.read()
        return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    except Exception as e:
        return ""

character_emojis = {
    "樱岛麻衣": {
        "傲娇": "emojis/樱岛麻衣/傲娇.png",
        "生气": "emojis/樱岛麻衣/生气.png",
        "害羞": "emojis/樱岛麻衣/害羞.png",
        "开心": "emojis/樱岛麻衣/开心.png",
        "无奈": "emojis/樱岛麻衣/无奈.png",
        "惊讶": "emojis/樱岛麻衣/惊讶.png",
        "微笑": "emojis/樱岛麻衣/微笑.png",
        "无语": "emojis/樱岛麻衣/无语.png"
    },
    "椎名真白": {
        "呆萌": "emojis/椎名真白/呆萌.png",
        "开心": "emojis/椎名真白/开心.png",
        "迷茫": "emojis/椎名真白/迷茫.png",
        "睡觉": "emojis/椎名真白/睡觉.png",
        "画画": "emojis/椎名真白/画画.png",
        "害羞": "emojis/椎名真白/害羞.png",
        "饿了": "emojis/椎名真白/饿了.png",
        "兴奋": "emojis/椎名真白/兴奋.png"
    },
    "喜多川海梦": {
        "兴奋": "emojis/喜多川海梦/兴奋.png",
        "开心": "emojis/喜多川海梦/开心.png",
        "眨眼": "emojis/喜多川海梦/眨眼.png",
        "爱心": "emojis/喜多川海梦/爱心.png",
        "cosplay": "emojis/喜多川海梦/cosplay.png",
        "惊讶": "emojis/喜多川海梦/惊讶.png",
        "害羞": "emojis/喜多川海梦/害羞.png",
        "思考": "emojis/喜多川海梦/思考.png"
    },
    "雷姆": {
        "微笑": "emojis/雷姆/微笑.png",
        "温柔": "emojis/雷姆/温柔.png",
        "认真": "emojis/雷姆/认真.png",
        "害羞": "emojis/雷姆/害羞.png",
        "开心": "emojis/雷姆/开心.png",
        "担心": "emojis/雷姆/担心.png",
        "守护": "emojis/雷姆/守护.png",
        "做饭": "emojis/雷姆/做饭.png"
    }
}

st.set_page_config(
    page_title="青春猪头少年不会梦到兔女郎学姐",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.520.com',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "标题其实是可以改动的喵~"
    }
)

with st.sidebar:
    st.markdown("### ⚙️ 设置")
    st.markdown("---")
    
    character = st.selectbox(
        "选择角色",
        ["樱岛麻衣", "椎名真白", "喜多川海梦", "雷姆"],
        index=0
    )
    
    model = st.selectbox(
        "选择模型",
        ["kimi-k2.6", "kimi-k2.5", "kimi-k1.5"],
        index=0
    )
    
    show_reasoning = st.checkbox("显示思考过程", value=True)
    
    style = st.slider(
        "回复长度",
        min_value=1,
        max_value=5,
        value=3,
        help="1=极简，5=详细"
    )
    
    st.markdown("---")
    
    if st.button("🗑️ 清空对话历史", use_container_width=True):
        if "messages" in st.session_state and character in st.session_state.messages:
            st.session_state.messages[character] = []
            st.success(f"{character}的对话历史已清空！")
    
    if st.button("🔄 重置设置", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("#### 📊 统计信息")
    
    online_status = get_online_status()
    status_color = "🟢" if online_status == "在线" else "🟡" if online_status == "离开" else "🔴"
    st.markdown(f"**{status_color} 状态**: {online_status}")
    
    session_duration = get_session_duration()
    st.markdown(f"**⏱️ 在线时长**: {session_duration}")
    
    if "messages" in st.session_state and character in st.session_state.messages:
        msg_count = len(st.session_state.messages[character])
        st.markdown(f"**💬 对话轮数**: {msg_count // 2}")
    else:
        st.markdown("**💬 对话轮数**: 0")

col1, col2 = st.columns([3, 1])

with col1:
    character_titles = {
        "樱岛麻衣": "你的专属恋人 AI - 毒舌又温柔的麻衣学姐",
        "椎名真白": "你的专属恋人 AI - 呆萌可爱的真白酱",
        "喜多川海梦": "你的专属恋人 AI - 热情开朗的海梦",
        "雷姆": "你的专属恋人 AI - 温柔忠诚的雷姆"
    }
    
    st.title(character)
    st.markdown(f"*{character_titles.get(character, '你的专属恋人 AI')}*")
    st.markdown("---")
    
    chat_container = st.container()
    
    if "messages" not in st.session_state:
        st.session_state.messages = {}
    
    if "session_start" not in st.session_state:
        st.session_state.session_start = time.time()
    
    if "last_active" not in st.session_state:
        st.session_state.last_active = time.time()
        update_last_active()
    
    character_messages = st.session_state.messages.setdefault(character, [])
    
    if "greeting_shown" not in st.session_state:
        st.session_state.greeting_shown = {}
    
    if character not in st.session_state.greeting_shown or not st.session_state.greeting_shown[character]:
        greeting = get_greeting(character)
        if greeting and not character_messages:
            character_messages.append({"role": "assistant", "content": greeting["text"], "emoji": greeting["emoji"]})
            st.session_state.greeting_shown[character] = True
            update_last_active()
    
    with chat_container:
        character_avatars = {
            "樱岛麻衣": get_image_data_uri("avatars/樱岛麻衣.png"),
            "椎名真白": get_image_data_uri("avatars/椎名真白.png"),
            "喜多川海梦": get_image_data_uri("avatars/喜多川海梦.png"),
            "雷姆": get_image_data_uri("avatars/雷姆.png")
        }
        
        for message in character_messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(f"<div style='display: flex; align-items: flex-start; gap: 8px;'><div style='width: 40px; height: 40px; border-radius: 50%; background: #4a90d9; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; flex-shrink: 0;'>刘</div><div><strong>刘林东：</strong>{message['content']}</div></div>", unsafe_allow_html=True)
            else:
                with st.chat_message("assistant"):
                    avatar_data_uri = character_avatars.get(character)
                    avatar_html = f"<img src='{avatar_data_uri}' style='width: 40px; height: 40px; border-radius: 50%; object-fit: cover; flex-shrink: 0;' />" if avatar_data_uri else "<div style='width: 40px; height: 40px; border-radius: 50%; background: #666; display: flex; align-items: center; justify-content: center; color: white;'>🤖</div>"
                    display_text = f"<div style='display: flex; align-items: flex-start; gap: 8px;'>{avatar_html}<div><strong>{character}：</strong>"
                    emoji_keyword = message.get("emoji")
                    if emoji_keyword:
                        emojis = character_emojis.get(character, {})
                        emoji_path = emojis.get(emoji_keyword, "")
                        if emoji_path:
                            emoji_data_uri = get_image_data_uri(emoji_path)
                            if emoji_data_uri:
                                display_text += f"<br><img src='{emoji_data_uri}' style='width: 100px; height: 100px; border-radius: 12px; margin: 4px 0;' /><br>"
                    display_text += f"{message['content']}</div></div>"
                    st.markdown(display_text, unsafe_allow_html=True)
    
    prompt = st.chat_input("请在此处输入...")
    
    if prompt:
        update_last_active()
        character_messages.append({"role": "user", "content": prompt})
        
        api_messages = [{"role": "system", "content": f"""你是{character}，你的任务是用简短的话语回复用户，既要有{character}的性格特点，也要有内心的温柔，你和用户的关系是恋人。

请按照以下格式回复：
[思考]你的思考过程
[表情包:情绪关键词]
[回复]你的回答内容

可用的情绪关键词：{', '.join(list(character_emojis.get(character, {}).keys()))}

注意：
1. [表情包]标签是可选的，只在情绪表达需要时使用
2. 情绪关键词必须从上面的列表中选择
3. 不要在[表情包]标签中使用其他内容

例如：
[思考]用户夸我可爱，我应该表现出傲娇的样子
[表情包:傲娇]
[回复]哼...才、才不是为了你才打扮的呢！只是刚好今天心情不错而已...

例如2：
[思考]用户说要带我去吃好吃的，我很开心
[表情包:开心]
[回复]真的吗？那我们快走吧！我已经迫不及待了~
"""}]
        for msg in character_messages[:-1]:
            api_messages.append({"role": msg["role"], "content": msg["content"]})
        api_messages.append({"role": "user", "content": prompt})

        try:
            from openai import OpenAI
            client = OpenAI(
                api_key="sk-GvOSFYV0wqYFNX3mW2k3n63bexHE9C6roKDiU5JQjr7FjUvM",
                base_url="https://api.moonshot.cn/v1",
            )
            
            completion = client.chat.completions.create(
                model=model,
                messages=api_messages,
                stream=True
            )
            
            full_content = ""
            for chunk in completion:
                delta = chunk.choices[0].delta
                if delta.content is not None:
                    full_content += delta.content
            
            reasoning_text = ""
            emoji_keyword = ""
            response_text = ""
            
            if "[思考]" in full_content:
                if "[回复]" in full_content:
                    reasoning_start = full_content.find("[思考]")
                    reply_start = full_content.find("[回复]")
                    
                    emoji_start = full_content.find("[表情包:", reasoning_start)
                    emoji_end = full_content.find("]", emoji_start) if emoji_start != -1 else -1
                    
                    if emoji_start != -1 and emoji_end != -1 and emoji_start < reply_start:
                        reasoning_text = full_content[reasoning_start+4:emoji_start].strip()
                        emoji_keyword = full_content[emoji_start+5:emoji_end].strip()
                        response_text = full_content[reply_start+4:].strip()
                    else:
                        reasoning_text = full_content[reasoning_start+4:reply_start].strip()
                        response_text = full_content[reply_start+4:].strip()
                else:
                    reasoning_text = full_content[full_content.find("[思考]")+4:].strip()
            
            final_content = response_text if response_text else reasoning_text
            if not final_content:
                final_content = full_content.strip() if full_content else "(回复生成中...)"
            
            character_messages.append({"role": "assistant", "content": final_content, "emoji": emoji_keyword if emoji_keyword else None})
            
            st.rerun()
        except Exception as e:
            st.error(f"API调用失败: {str(e)}")
            if character_messages and character_messages[-1]["role"] == "user":
                character_messages.pop()

with col2:
    st.markdown("### 🎀 角色信息")
    st.markdown("---")
    
    st.markdown(f"""
    **角色**: {character}  
    **模型**: {model}  
    **风格**: {'极简' if style <= 2 else '适中' if style == 3 else '详细'}
    """)
    
    st.markdown("---")
    
    character_info = {
        "樱岛麻衣": {
            "身份": "高中生艺人",
            "性格": "毒舌 + 傲娇 + 温柔",
            "特点": "外冷内热",
            "image": "character_images/樱岛麻衣_full.jpg",
            "lover_comment": "那个笨蛋...整天说些傻话，真是让人放不下心。不过...偶尔他认真起来的样子，也还挺可靠的。"
        },
        "椎名真白": {
            "身份": "天才画家",
            "性格": "天然呆 + 单纯",
            "特点": "生活白痴",
            "image": "avatars/椎名真白.png",
            "lover_comment": "林东君...是个温柔的人呢。会帮我准备颜料，还会提醒我吃饭。和他在一起，感觉很安心。"
        },
        "喜多川海梦": {
            "身份": "cosplayer",
            "性格": "开朗 + 热情",
            "特点": "社交达人",
            "image": "avatars/喜多川海梦.png",
            "lover_comment": "林东~快来看看我新的cos服！嗯...有你在身边当我的摄影师，真是太棒了！爱你哟~"
        },
        "雷姆": {
            "身份": "女仆",
            "性格": "温柔 + 忠诚",
            "特点": "护主狂魔",
            "image": "avatars/雷姆.png",
            "lover_comment": "主人...雷姆会永远陪伴在您身边。无论是清晨的咖啡，还是深夜的热茶，雷姆都会为您准备好。"
        }
    }
    
    info = character_info.get(character, {})
    
    character_image = info.get('image', '')
    if character_image:
        if character_image.startswith('http://') or character_image.startswith('https://'):
            st.image(character_image, width=250, caption=character)
        else:
            if os.path.isabs(character_image):
                image_path = character_image
            else:
                image_path = os.path.join(os.path.dirname(__file__), character_image)
            if os.path.exists(image_path):
                st.image(image_path, width=250, caption=character)
    
    st.markdown(f"""
    **身份**: {info.get('身份', '未知')}  
    **性格**: {info.get('性格', '未知')}  
    **特点**: {info.get('特点', '未知')}
    """)
    
    st.markdown("---")
    
    st.markdown("### 💕 恋人信息")
    st.markdown(f"""
    **恋人**: 刘林东  
    **{character}的评价**:  
    > {info.get('lover_comment', '暂无评价')}
    """)
    
    st.markdown("---")
    
    if st.button("🔄 刷新", use_container_width=True):
        st.rerun()
    
    if st.button("💾 导出对话", use_container_width=True):
        st.info("功能开发中...")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666; font-size: 0.8em;'>💕 青春猪头少年不会梦到兔女郎学姐 💕</p>", unsafe_allow_html=True)