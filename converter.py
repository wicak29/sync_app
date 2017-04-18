import re

update_str = "UPDATE daerah3 SET kode='PDG', nama='Padang' WHERE iddaerah=11 AND kode='PDG' OR kode='DPS';"
print "Update syntax: ", update_str

# UPSERT INTO daerah3 (iddaerah, kode, nama) VALUES (11, 'PDG', 'Padang')

update_split = update_str.split()
print "split UPDATE: ", update_split

# Get table name
tabel = update_split[1]
print "tabel: ", tabel

kolom = [None]*100
value = [None]*100

# get kolom and value betwen SET and WHERE
fields = re.findall(r'SET(.*?)WHERE', update_str)
# print fields
kol_val = fields[0].split(',')
# print kol_val
for i in range(len(kol_val)):
	tmp = kol_val[i]
	tmp_rmv_space = tmp.replace(" ","")
	tmp_split = tmp_rmv_space.split('=')
	print tmp_split
	kolom[i] = tmp_split[0]
	value[i] = tmp_split[1]

# get kolom and value after WHERE
last_pos = len(kol_val)
split_where = update_str.split('WHERE')[1]
split_where = split_where.replace("AND","#")
split_where = split_where.replace("OR","#")
split_where = split_where.replace(" ","")
print 'after where: ', split_where
kol_val2 = split_where.split('#')
for i in range(len(kol_val2)):
	tmp = kol_val2[i]
	tmp_split = tmp.split('=')
	kolom[last_pos+i] = tmp_split[0]
	value[last_pos+i] = tmp_split[1]

print kolom
print value