## Description

This project helps you parse your Kindle highlights and notes into a readable, searchable format.

## How to Use

First, connect your Kindle to your computer using a USB cable. Once you open the drive, open 'documents' folder and copy the 'My Clippings.txt' file into this directory. Then simply run

```python
from clipping_parser import ClippingParser

parser = ClippingParser()
books = parser.parse('My Clippings.txt')
parser.export('output_filename.txt')
```

to export your highlights and notes. More improvements are to be made, and I welcome and appreciate contributions.

### Example (English)

Man's Search for Meaning (Viktor Frankl)
- Your Highlight on Location 79-82 | Added on Monday, March 29, 2021 12:39:51 AM

“Don’t aim at success—the more you aim at it and make it a target, the more you are going to miss it. For success, like happiness, cannot be pursued; it must ensue, and it only does so as the unintended side-effect of one’s dedication to a cause greater than oneself or as the by-product of one’s surrender to a person other than oneself. Happiness must happen, and the same holds for success: you have to let it happen by not caring about it.
==========
Man's Search for Meaning (Viktor Frankl)
- Your Note on Location 82 | Added on Monday, March 29, 2021 12:40:20 AM

Yooo this is the gold 
==========

### Example (Chinese)

The Power of Moments (Chip Heath;Dan Heath)
- 您在位置 #2984-2990的标注 | 添加于 2020年3月17日星期二 下午1:32:49

1. Stretching ourselves to discover our reach; 2. Being intentional about creating peaks (or Perfect Moments, in Eugene O’Kelly’s phrasing) in our personal lives; 3. Practicing courage by speaking honestly—and seeking partners who are responsive to us in the first place; 4. The value of connection (and the difficulty of creating peaks); 5. Creating moments of elevation and breaking the script to move beyond old patterns and habits.
==========

The Power of Moments (Chip Heath;Dan Heath)
- 您在位置 #2990 的笔记 | 添加于 2020年3月17日星期二 下午1:33:04

Such good advice!!!
==========