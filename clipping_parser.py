"""
Copyright 2021 Yijia Chen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from typing import Dict, List
from datetime import datetime


class Clipping(object):
    def __init__(self):
        self.title: str = ''
        self.authors: List[str] = []
        self.is_chinese: bool = False
        self.is_not: bool = False
        self.location: str = ''
        self.datetime: datetime = None
        self.text: str = ''
        self.note: Clipping = None
    
    def __repr__(self) -> str:
        return self.text + ', loc. ' + self.location + ', ' + str(self.datetime)

    def __str__(self) -> str:
        return self.text + ', loc. ' + self.location + ', ' + str(self.datetime)


class Book(object):
    def __init__(self, title, authors):
        self.title: str = title
        self.authors: List[str] = authors
        self.datetime: datetime = datetime.min # set to oldest possible time
        self.clippings: List[Clipping] = []

    def add(self, clipping):
        self.clippings.append(clipping)
        if clipping.datetime > self.datetime:
            self.datetime = clipping.datetime # update to time of newest clipping
    
    def __repr__(self) -> str:
        return self.title + ', by ' + ', '.join(self.authors) + '\n\n' + '\n\n'.join([str(cli) for cli in self.clippings])

    def __str__(self) -> str:
        return self.title + ', by ' + ', '.join(self.authors) + '\n' + '\n'.join([str(cli) for cli in self.clippings])


class ClippingParser(object):
    def __init__(self):
        self.clippings: List[Clipping] = []
        self.books: Dict[str, Book] = {}

    def export(self, f_out_name: str):
        with open(f_out_name, 'w+') as f:
            books = sorted(list(self.books.values()), key=lambda b: b.datetime, reverse=True)

            for b in books:
                f.write('### ' + repr(b) + '\n\n')

    def parse(self, f_in_name: str = 'My Clippings.txt') -> Dict[str, Book]:
        with open(f_in_name, 'r+') as f:
            lines = f.readlines()
            clipping = Clipping()
            line_count_within_clipping = 0

            for line in lines:
                line = line.strip()

                if line_count_within_clipping == 0:
                    last_open_paren_index = line.rfind('(')
                    clipping.title = line[:last_open_paren_index-1]
                    clipping.authors = self.find_all_authors(line[last_open_paren_index+1:-1])

                elif line_count_within_clipping == 1:
                    separator_index = line.find('|')
                    clipping.is_chinese = line[2] == '您'
                    clipping.is_note = self.get_mode(line[:separator_index-1])
                    clipping.location = self.get_location(line[:separator_index-1], clipping.is_chinese)
                    clipping.datetime = self.get_datetime(line[separator_index+1:], clipping.is_chinese)

                elif line_count_within_clipping == 3: # skips empty line
                    clipping.text = line

                elif '==========' in line.strip(): # end of clipping
                    if clipping.is_note:
                        last_highlight = self.clippings[-1]
                        assert not last_highlight.is_note
                        self.clippings[-1].note = clipping # attach note to last highlight
                    else:
                        if clipping.title not in self.books:
                            self.books[clipping.title] = Book(clipping.title, clipping.authors)
                        self.books[clipping.title].add(clipping)
                        self.clippings.append(clipping)
                    
                    clipping = Clipping()
                    line_count_within_clipping = -1

                elif line:
                    if clipping.text:
                        clipping.text += '\n\n' + line

                line_count_within_clipping += 1

        return self.books 

    def find_all_authors(self, str: str) -> List[str]:
        if len(str) == 0:
            raise ValueError("Authors should not be empty.")

        authors = []
        breaks = [i for i, ch in enumerate(str) if ch == ';']
        last_break = 0

        for br in breaks:
            author = str[last_break:br]
            comma_index = author.find(',')

            if comma_index > 0:
                authors.append(author[comma_index+2:] + ' ' + author[:comma_index])
            else:
                authors.append(author)

            last_break = br + 1

        return authors

    def get_mode(self, str: str) -> bool:
        return 'Note' in str or '笔记' in str 

    def get_location(self, str: str, is_chinese: bool) -> str:
        str = str.strip()

        if is_chinese:
            return str[str.find('#')+1:str.find('的')]
        else:
            return str[str.rfind('n')+1:].strip()

    def get_datetime(self, str: str, is_chinese: bool) -> datetime:
        str = str.strip()
        
        if is_chinese:
            ampm_index = str.find('午')
            str += ' am' if '上午' in str else ' pm' # hacky way to determine am/pm in Chinese

            date = datetime.strptime(str[:str.find('星')], '添加于 %Y年%m月%d日').date()
            time = datetime.strptime(str[ampm_index+1:], '%I:%M:%S %p').time()
            return datetime.combine(date, time)
        else:
            return datetime.strptime(str, 'Added on %A, %B %d, %Y %I:%M:%S %p')