import os
needle_list=['info@greenfixexteriorcare.co.uk','Get in touch to open an account','mailto:']
for root,dirs,files in os.walk('.'):
    for f in files:
        path=os.path.join(root,f)
        try:
            with open(path,encoding='utf-8',errors='ignore') as fh:
                text=fh.read()
        except Exception:
            continue
        hits=[]
        for i,l in enumerate(text.splitlines(),1):
            for n in needle_list:
                if n in l:
                    hits.append((i,l.strip()))
        if hits:
            print('FILE:',path)
            for ln in hits:
                print('  L',ln[0],':',ln[1])
