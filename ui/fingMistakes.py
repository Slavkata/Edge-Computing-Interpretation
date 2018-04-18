import enchant
from enchant.checker import SpellChecker
a = "You are a very nice guy with a nice tomahawk"
chkr = enchant.checker.SpellChecker("en_GB")
chkr.set_text(a)
for err in chkr:
    print(err.word)
    sug = err.suggest()[0]
    err.replace(sug)

c = chkr.get_text()#returns corrected text
print (c)
 
