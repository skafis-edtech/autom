# Math VBE automatisation

This makes screenshots of problems specifically for 2024 pak. session math VBE.

## Packages

pip install pymupdf

pip install pillow

pip install numpy

## Instructions

1. Place 2024k.pdf VBE math file in input dir.
2.

## Info

Question numbers have font `Yantramanav` (pdffiller.com) (do they tho?)

General info about PDF (http://pdf-analyser.edpsciences.org)

`detect_fonts.py` shows used fonts like this:

````Fonts used in the PDF:
MT-Extra
ArialMT
Wingdings-Regular
TimesNewRomanPS-BoldMT
TimesNewRomanPSMT
Arial-BoldMT
SymbolMT
TimesNewRomanPS-ItalicMT
TimesNewRomanPS-BoldItalicMT
Calibri
Times New Roman TUR,Bold```
````

`text_content_analysis.py` prints out the text of pdf with specified fonts.

After analysis looks like numbers are in `Arial-BoldMT` font mostly.
