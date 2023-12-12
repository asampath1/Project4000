from ai4bharat.transliteration import XlitEngine

e = XlitEngine("ta", beam_width=10)
out = e.translit_word("pallandu",topk=5)
print(out)
# output: {'ta': ['பல்லாண்டு', 'பல்லண்டு', 'பள்ளண்டு', 'பள்ளாண்டு', 'பல்லன்டு']}
