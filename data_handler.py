import pandas as pd


def read_csv(filename):
	df = pd.read_csv(filename,index_col=0, skiprows = [0,2])
	return df

def get_column_names(filename):
	df = pd.read_csv(filename, index_col=0, skiprows = [0,2])
	return list(df.columns)

def map_units(filename):
	doc = open('telemetry.csv', encoding = 'utf-8')
	lines = doc.readlines()
	titles = lines[1].strip().replace('"', '').split(',')
	units = lines[2].strip().replace('"', '').split(',')
	return {titles[i].strip(): units[i].strip() for i in range(len(titles))}
