# ui/chapter.py - 章节数据类
class Chapter:
    """章节数据"""

    def __init__(self, id, title, text, speech_file, image_file=None, text_file=None):
        """
        初始化章节

        Args:
            id: 章节ID，如 "H01"
            title: 章节标题，如 "南湖红船"
            text: 解说文本（简短描述，用于UI显示）
            speech_file: 语音文件路径
            image_file: 章节专属背景图片路径（可选）
            text_file: 完整解说词文本文件路径（可选）
        """
        self.id = id
        self.title = title
        self.text = text
        self.speech_file = speech_file
        self.image_file = image_file
        self.text_file = text_file