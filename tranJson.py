import json
from array import array
from ROOT import TH2D, TFile

#jsonf='ScaleFactors_Muon_highPt_RECO_2017_schemaV2.json'
#jsonf='ScaleFactors_Muon_highPt_ID_2017_schemaV2.json'
jsonf='ScaleFactors_Muon_highPt_ISO_2017_schemaV2.json'
all_values = []
ptbin=[]
etabin=[]

def extract_specific_values(node, keys):
  if isinstance(node, dict):
    values = []
    if 'edges' in node and 'input' in node and node['input']=='abseta':
      etabin.extend(node['edges'])
    #if 'edges' in node and 'input' in node and node['input']=='p':
    if 'edges' in node and 'input' in node and node['input']=='pt':
      ptbin.extend(node['edges'])
    if 'key' in node and node['key'] in keys:
      values.append(node['value'])
    else:
      for key in node:
        values.extend(extract_specific_values(node[key], keys))
    return values
  elif isinstance(node, list):
    values = []
    for item in node:
      values.extend(extract_specific_values(item, keys))
    return values
  else:
    return []

target_keys = ["nominal", "systup", "systdown"]

with open(jsonf, 'r') as fin:
  data=fin.read()
  lines=json.loads(data)
  keys=lines.keys()
  for key, value in lines.items():
    if not key=='corrections':continue
    for correction in value:
      all_values.extend(extract_specific_values(correction,target_keys))

ptbin=sorted(set(ptbin))
ptbin[-1]=2000.

#h1=TH2D('highptRECO','highptRECO',len(ptbin)-1,array('d',ptbin),len(etabin)-1,array('d',etabin))
#h2=TH2D('highptRECOUp','highptRECOUp',len(ptbin)-1,array('d',ptbin),len(etabin)-1,array('d',etabin))
#h3=TH2D('highptRECODo','highptRECODo',len(ptbin)-1,array('d',ptbin),len(etabin)-1,array('d',etabin))

#h1=TH2D('highptID','highptID',len(ptbin)-1,array('d',ptbin),len(etabin)-1,array('d',etabin))
#h2=TH2D('highptIDUp','highptIDUp',len(ptbin)-1,array('d',ptbin),len(etabin)-1,array('d',etabin))
#h3=TH2D('highptIDDo','highptIDDo',len(ptbin)-1,array('d',ptbin),len(etabin)-1,array('d',etabin))

h1=TH2D('highptISO','highptISO',len(ptbin)-1,array('d',ptbin),len(etabin)-1,array('d',etabin))
h2=TH2D('highptISOUp','highptISOUp',len(ptbin)-1,array('d',ptbin),len(etabin)-1,array('d',etabin))
h3=TH2D('highptISODo','highptISODo',len(ptbin)-1,array('d',ptbin),len(etabin)-1,array('d',etabin))

#f1=TFile.Open('reco.root','recreate')
#f1=TFile.Open('id.root','recreate')
f1=TFile.Open('iso.root','recreate')

all_values.extend(all_values[-3:])

print(all_values)
print(len(all_values))
for iy in range(len(etabin)-1):
  for ix in range(len(ptbin)-1):
    h1.SetBinContent(ix+1,iy+1,all_values[3*(ix)+3*(len(ptbin)-1)*(iy)])
    h2.SetBinContent(ix+1,iy+1,all_values[3*(ix)+3*(len(ptbin)-1)*(iy)+1])
    h3.SetBinContent(ix+1,iy+1,all_values[3*(ix)+3*(len(ptbin)-1)*(iy)+2])

f1.cd()
h1.Write()
h2.Write()
h3.Write()
f1.Close()
