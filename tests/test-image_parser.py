import setup
from Parser.parser_baseclass import Parser
from Parser.image_parser import ImageParser

prs = Parser()  #test o chuj chodzi z polimorfizmem potem usune
iprs = ImageParser((256, 256))
prs = iprs
print(prs.parse("data/Lenna.png"))