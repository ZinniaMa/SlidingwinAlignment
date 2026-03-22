import re

def pdb_root(x):
    s = x.strip()
    s = re.sub(r'^pdb:', '', s, flags=re.I)       
    s = s.replace('.', '_')                       
    m = re.search(r'([0-9][A-Za-z0-9]{3})', s)
    return m.group(1).lower() if m else s.lower()