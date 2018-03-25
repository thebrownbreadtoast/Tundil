import pandas as pd

class filter_data(object):

	def data_filter(self,*args):
		dataset = pd.read_csv('training_data/raw_dataset.csv')
		source = args[0]
		filtered_dataset = dataset['source'] == source
		filtered_text = dataset[filtered_dataset]['text']
		return filtered_text

	def file_write(self,*args):
		filename = args[0]
		data = self.data_filter(filename)
		with open('training_data/'+filename+'.txt', 'w') as file:
			rows = 0
			for line in data:
				if rows <=2500:
					if filename == 'robot':
						file.write('akshay '+line+' dadwal'+'\n')
					else:
						file.write(line+'\n')
					rows +=1
				else:
					break
		file.close()
		print(rows,' added into ',filename)


if __name__ == '__main__':
	file = filter_data()
	file.file_write('human')
	file.file_write('robot')
	
	
