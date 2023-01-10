import json
from pathlib import Path
from typing import Union

import arabic_reshaper
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from wordcloud import WordCloud

from src.data import DATA_DIR


class ChatStatistics:
    """Generate chat statistic from a telegram chat json file
    """
    def __init__(self, chat_json: Union[str, Path]):
    
        # load chatdata
        logger.info(f"Loading chat data from {chat_json }")
        with open(chat_json) as f:
            self.chat_data = json.load(f)
            
        self.normalizer = Normalizer()
        
        # load stopwords
        stop_words = open(DATA_DIR / 'stopwords.txt').readlines()
        stop_words = list(map(str.strip, stop_words))
        self.stop_words = list(map(self.normalizer.normalize, stop_words))
    
    
    def generate_word_cloud(
        self,
        output_dir: Union[str, Path],
        width: int = 800, height: int = 600,
        max_font_size: int = 250,
        ):
        """Generate a word cloud from the chat data

        Args:
            output_dir (Union[str, Path]): path to output directory for word cloud image
        """
        
        text_content = ''

        for msg in self.chat_data['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                
                text_content += f" {' '.join(tokens)}"
        
        text_content  = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content[:100000])
        text_content = get_display(text_content)
        
        wordcloud = WordCloud(
                font_path=str(DATA_DIR / 'BHoma.ttf'),
                width=width, height=height,
                background_color='white',
                max_font_size= max_font_size
            ).generate(text_content)

        wordcloud.to_file(str(Path(output_dir) / 'wordcloud.png'))

if __name__ == "__main__":
    chat_stats = ChatStatistics(chat_json=DATA_DIR / 'pytopia.json')
    chat_stats.generate_word_cloud(DATA_DIR)
    print('Done!')
