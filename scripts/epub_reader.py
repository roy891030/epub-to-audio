"""
# 啟動虛擬環境（每次開新終端機都要執行）
source venv/bin/activate

# 之後如果要在其他電腦重建相同環境
pip install -r requirements.txt
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPUB 讀取器
功能：讀取 EPUB 檔案，提取文字內容和元數據
"""

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path


class EPUBReader:
    """EPUB 電子書讀取器"""
    
    def __init__(self, epub_path):
        """
        初始化讀取器
        
        Args:
            epub_path: EPUB 檔案路徑
        """
        self.epub_path = Path(epub_path)
        self.book = None
        self.metadata = {}
        self.chapters = []
        
    def load(self):
        """載入 EPUB 檔案"""
        try:
            self.book = epub.read_epub(str(self.epub_path))
            print(f"✓ 成功載入: {self.epub_path.name}")
            return True
        except Exception as e:
            print(f"✗ 載入失敗: {e}")
            return False
    
    def extract_metadata(self):
        """提取書籍元數據"""
        if not self.book:
            print("請先載入 EPUB 檔案")
            return None
        
        try:
            # 提取基本資訊
            title = self.book.get_metadata('DC', 'title')
            creator = self.book.get_metadata('DC', 'creator')
            language = self.book.get_metadata('DC', 'language')
            publisher = self.book.get_metadata('DC', 'publisher')
            
            self.metadata = {
                'title': title[0][0] if title else 'Unknown',
                'author': creator[0][0] if creator else 'Unknown',
                'language': language[0][0] if language else 'Unknown',
                'publisher': publisher[0][0] if publisher else 'Unknown',
                'filename': self.epub_path.name
            }
            
            print("\n=== 書籍資訊 ===")
            print(f"書名: {self.metadata['title']}")
            print(f"作者: {self.metadata['author']}")
            print(f"語言: {self.metadata['language']}")
            print(f"出版社: {self.metadata['publisher']}")
            
            return self.metadata
            
        except Exception as e:
            print(f"提取元數據時發生錯誤: {e}")
            return None
    
    def clean_text(self, text):
        """
        清理文字內容
        
        Args:
            text: 原始文字
            
        Returns:
            清理後的文字
        """
        # 移除多餘的換行
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # 移除多餘的空白
        text = re.sub(r' +', ' ', text)
        # 移除行首行尾空白
        text = text.strip()
        
        return text
    
    def extract_chapters(self):
        """提取所有章節內容"""
        if not self.book:
            print("請先載入 EPUB 檔案")
            return None
        
        print("\n=== 開始提取章節 ===")
        self.chapters = []
        chapter_num = 0
        
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # 解析 HTML 內容
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                
                # 移除 script 和 style 標籤
                for script in soup(['script', 'style']):
                    script.decompose()
                
                # 提取文字
                text = soup.get_text(separator='\n')
                text = self.clean_text(text)
                
                # 過濾太短的內容（可能是空白頁或版權頁）
                if len(text) > 100:
                    chapter_num += 1
                    
                    # 嘗試從內容中提取章節標題
                    lines = text.split('\n')
                    chapter_title = lines[0][:50] if lines else f"Chapter {chapter_num}"
                    
                    chapter_data = {
                        'number': chapter_num,
                        'title': chapter_title,
                        'filename': item.get_name(),
                        'content': text,
                        'word_count': len(text),
                        'char_count': len(text)
                    }
                    
                    self.chapters.append(chapter_data)
                    print(f"  [{chapter_num}] {chapter_title[:40]}... ({len(text)} 字)")
        
        print(f"\n✓ 共提取 {len(self.chapters)} 個章節")
        return self.chapters
    
    def get_full_text(self):
        """取得完整書籍文字"""
        if not self.chapters:
            self.extract_chapters()
        
        return '\n\n'.join([chapter['content'] for chapter in self.chapters])
    
    def get_statistics(self):
        """取得書籍統計資訊"""
        if not self.chapters:
            self.extract_chapters()
        
        total_chars = sum(chapter['char_count'] for chapter in self.chapters)
        total_words = sum(chapter['word_count'] for chapter in self.chapters)
        
        stats = {
            'total_chapters': len(self.chapters),
            'total_characters': total_chars,
            'total_words': total_words,
            'avg_chapter_length': total_chars // len(self.chapters) if self.chapters else 0
        }
        
        print("\n=== 統計資訊 ===")
        print(f"總章節數: {stats['total_chapters']}")
        print(f"總字數: {stats['total_characters']:,}")
        print(f"平均每章字數: {stats['avg_chapter_length']:,}")
        
        return stats
    
    def save_to_txt(self, output_path):
        """
        儲存為純文字檔
        
        Args:
            output_path: 輸出檔案路徑
        """
        try:
            output_path = Path(output_path)
            full_text = self.get_full_text()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"書名: {self.metadata.get('title', 'Unknown')}\n")
                f.write(f"作者: {self.metadata.get('author', 'Unknown')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(full_text)
            
            print(f"\n✓ 已儲存為: {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ 儲存失敗: {e}")
            return False
    
    def save_chapters_json(self, output_path):
        """
        儲存章節資訊為 JSON 格式
        
        Args:
            output_path: 輸出檔案路徑
        """
        try:
            output_path = Path(output_path)
            
            data = {
                'metadata': self.metadata,
                'statistics': self.get_statistics(),
                'chapters': self.chapters
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 已儲存 JSON: {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ 儲存 JSON 失敗: {e}")
            return False


def main():
    """主程式"""
    # 取得專案根目錄
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    
    # 設定路徑
    input_file = project_dir / "input" / "高效原力：用愉悅心態激發生產力，做更多重要的事 (阿里 · 阿布達爾 (Dr Ali Abdaal)) (Z-Library).epub"
    output_txt = project_dir / "output" / "book_content.txt"
    output_json = project_dir / "output" / "book_data.json"
    
    # 建立讀取器
    print("=== EPUB 讀取器 ===\n")
    reader = EPUBReader(input_file)
    
    # 載入並處理
    if reader.load():
        reader.extract_metadata()
        reader.extract_chapters()
        reader.get_statistics()
        
        # 儲存結果
        reader.save_to_txt(output_txt)
        reader.save_chapters_json(output_json)
        
        print("\n✓ 處理完成！")
        print(f"\n下一步建議：")
        print(f"1. 查看 output/book_content.txt 檢查內容")
        print(f"2. 查看 output/book_data.json 了解章節結構")
        print(f"3. 準備進行內容分析和 LLM 處理")


if __name__ == "__main__":
    main()