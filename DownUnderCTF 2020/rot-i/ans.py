from string import ascii_lowercase, ascii_uppercase
msg = "Ypw'zj zwufpp hwu txadjkcq dtbtyu kqkwxrbvu! Mbz cjzg kv IAJBO{ndldie_al_aqk_jjrnsxee}. Xzi utj gnn olkd qgq ftk ykaqe uei mbz ocrt qi ynlu, etrm mff'n wij bf wlny mjcj :)."


def deCryPt(msg):
    out = ''
    for i, c in enumerate(msg):
        if c in ascii_lowercase:
            alph = ascii_lowercase
        elif c in ascii_uppercase:
            alph = ascii_uppercase
        else:
            out += c
            continue
        out += alph[(alph.index(c) - i) % len(alph)]
    return out

print(deCryPt(msg))
#You've solved the beginner crypto challenge! The flag is DUCTF{crypto_is_fun_kjqlptzy}. Now get out some pen and paper for the rest of them, they won't all be this easy :).

