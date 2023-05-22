class CommandCard:
    @classmethod
    def helpCard(cls, bookNumber: int = None, commandList: str = None):
        card_message = [
            {
                "type": "card",
                "theme": "none",
                "size": "lg",
                "color": "#4169E1",
                "modules": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain-text",
                            "content": f"| 获取帮助 | - {bookNumber}"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "kmarkdown",
                            "content": f"{commandList}"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain-text",
                                "content": "-由清云工作室强力支持"
                            }
                        ]
                    }
                ]
            }
        ]
        return card_message

    @classmethod
    def mainCard(cls, userAvatar: str = None, userName: str = None, identityGroup: str = None):
        card_message = [
            {
                "type": "card",
                "theme": "none",
                "size": "lg",
                "color": "#6495ED",
                "modules": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain-text",
                            "content": "用户主页"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain-text",
                                "content": "当前用户:"
                            },
                            {
                                "type": "image",
                                "src": f"{userAvatar}"
                            },
                            {
                                "type": "plain-text",
                                "content": f"{userName}#{identityGroup}"
                            }
                        ]
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "paragraph",
                            "cols": 2,
                            "fields": [
                                {
                                    "type": "kmarkdown",
                                    "content": "**当前等级:**12"
                                },
                                {
                                    "type": "kmarkdown",
                                    "content": "**经验值:**10/12"
                                }
                            ]
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "paragraph",
                            "cols": 2,
                            "fields": [
                                {
                                    "type": "kmarkdown",
                                    "content": "**积分:**10"
                                },
                                {
                                    "type": "kmarkdown",
                                    "content": "**清云账号:**已绑定"
                                }
                            ]
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain-text",
                                "content": "日常功能"
                            }
                        ]
                    },
                    {
                        "type": "action-group",
                        "elements": [
                            {
                                "type": "button",
                                "theme": "primary",
                                "value": "签到",
                                "click": "return-val",
                                "text": {
                                    "type": "plain-text",
                                    "content": "签到"
                                }
                            },
                            {
                                "type": "button",
                                "theme": "primary",
                                "value": "www.qfc.cn",
                                "click": "link",
                                "text": {
                                    "type": "plain-text",
                                    "content": "前往官网"
                                }
                            },
                            {
                                "type": "button",
                                "theme": "primary",
                                "value": "www.qingyun.com",
                                "click": "link",
                                "text": {
                                    "type": "plain-text",
                                    "content": "绑定清云账号"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
        return card_message

    @classmethod
    def shoutCard(cls, userName: str = None, text: str = None, userAvatar: str = None, channelId: str = None):
        shout_card = [
            {
                "type": "card",
                "theme": "none",
                "size": "lg",
                "color": "#6495ED",
                "modules": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain-text",
                            "content": "全服喊话"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain-text",
                                "content": f"{userName}:"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "kmarkdown",
                            "content": f"**{text}**"
                        },
                        "mode": "left",
                        "accessory": {
                            "type": "image",
                            "src": f"{userAvatar}",
                            "size": "lg"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "kmarkdown",
                                "content": f"(chn){channelId}(chn)"
                            }
                        ]
                    }
                ]
            }
        ]
        return shout_card


class ErrorCard:
    @classmethod
    def paramError(cls):
        param_error = [
            {
                "type": "card",
                "theme": "none",
                "size": "lg",
                "modules": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain-text",
                            "content": "参数错误"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "kmarkdown",
                            "content": "(font)您使用该指令的参数过多或过少(font)[warning]"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "kmarkdown",
                            "content": "您可以使用`/help`来获取帮助"
                        }
                    }
                ]
            }
        ]
        return param_error
