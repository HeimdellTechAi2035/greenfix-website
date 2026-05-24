import re, json
p='c:/Users/andre/Desktop/greenfix website/index.html'
s=open(p,encoding='utf-8').read()
# count H1
h1s=re.findall(r'<h1[^>]*>(.*?)</h1>',s,flags=re.I|re.S)
print('H1 count:',len(h1s))
if h1s:
    print('H1 text:', re.sub(r'<[^>]+?>','',h1s[0]).strip())
# extract JSON-LD
scripts=re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',s,flags=re.I|re.S)
print('JSON-LD blocks found:',len(scripts))
valid=True
for i,block in enumerate(scripts,1):
    try:
        data=json.loads(block)
        print(i,'OK type=',data.get('@type'))
    except Exception as e:
        valid=False
        print(i,'INVALID:',e)
print('All JSON-LD valid:',valid)
