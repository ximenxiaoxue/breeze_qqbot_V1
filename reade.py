import pandas 
data =pandas.read_excel("words\word.xlsx")
word = data.loc[:, 'question']
print(word)