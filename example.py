from clipping_parser import ClippingParser

parser = ClippingParser()
books = parser.parse('My Clippings.txt')
parser.export('output.txt')