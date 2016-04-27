setwd('c:/Data/Temp/2/statistics/')

data=read.table('GPCR2.dat',header = 1,sep = '\t')

th_v2r=1.2 #high/low luminescence threshold for V2RRluc
th_casr=0.3 #high/low luminescence threshold for CaSRRLuc

model_v2r=lm(BRETratio~0+Acceptor:Fluorescence+Acceptor:Fluorescence:(Luminescence<th_v2r),data[data[,'Donor']=='V2RRLuc',])

p_v2r=summary(model_v2r)$coefficients[c(7,8,9,10,11,12),4]
p_v2r=p.adjust(p_v2r,method = 'BH')

model_casr=lm(BRETratio~0+Acceptor:Fluorescence+Acceptor:Fluorescence:(Luminescence<th_casr),data[data[,'Donor']=='CaSRRLuc',])

p_casr=summary(model_casr)$coefficients[c(7,8,9,10,11,12),4]
p_casr=p.adjust(p_casr,method = 'BH')

print('V2RRLuc p values after Benjamini-Hochberg correction:')
print(p_v2r)
print('CaSRRLuc p values after Benjamini-Hochberg correction:')
print(p_casr)