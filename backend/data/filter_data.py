import pandas as pd

class filter_data(object):

	def data_filter(self,*args):
		dataset = pd.read_csv('data/raw_dataset.csv')
		source = args[0]
		filtered_dataset = dataset['source'] == source
		filtered_text = dataset[filtered_dataset]['text']
		return filtered_text

	def file_write(self,*args):
		filename = args[0]
		data = self.data_filter(filename)
		with open('data/'+filename+'.txt', 'w') as file:
			for line in data:
				file.write(line)
			file.close()

if __name__ == '__main__':
	file = filter_data()
	file.file_write('human')
	file.file_write('robot')
	
	
