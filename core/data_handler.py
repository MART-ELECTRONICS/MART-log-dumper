from pandas import read_csv as read


def read_csv(filename):
	df = read(filename,index_col=0, skiprows = [0,2])
	return df

def get_column_names(filename):
	df = read(filename, index_col=0, skiprows = [0,2])
	return list(df.columns)

def map_units(filename):
	doc = open(filename, encoding = 'utf-8')
	lines = doc.readlines()
	titles = lines[1].strip().replace('"', '').split(',')
	units = lines[2].strip().replace('"', '').split(',')
	return {titles[i].strip(): units[i].strip() for i in range(len(titles))}
