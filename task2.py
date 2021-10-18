import pandas as pd
import tabula
from zipfile import ZipFile
def data_table_processing(tables):
  if isinstance(tables, list):
    return large_table(tables)
  else:
    return single_table(tables)

def single_table(table):
  table.columns = table.iloc[0]
  table = table[table.columns[-1]].str.split(" ", expand=True)
  table = table.drop(table.columns[2:], axis=1)
  col = dict(zip(table.columns, ["Código", "Descrição da categoria"]))
  table.rename(columns=col, inplace=True)
  table = table.dropna(subset=table.columns, axis=0)
  table = table[1:]
  return table
def large_table(table_list):
  table_list[0].columns = table_list[0].iloc[0] # first line of the table will be the header
  table_list[0] = table_list[0][1:] # removing the repeated line, which now is the header
  for index in range(1,len(table_list)):
    table_list[index]=table_list[index].columns.to_frame().T.append(table_list[index], ignore_index=False)
    table_list[index].columns = table_list[index].iloc[0]
    col=dict(zip(table_list[index].columns, table_list[0].columns))
    table_list[index].rename(columns=col, inplace=True)

  return pd.concat(table_list)

if __name__ == "__main__":
    pdf_file='padrao_tiss_componente_organizacional_202108.pdf'
    pgs_to_read="108-114"
    table_list=tabula.read_pdf(pdf_file, pages=pgs_to_read)
    csv_filename1 = table_list[0].columns[-1]
    csv_filename2 = table_list[1].columns[-1]
    csv_filename3 = table_list[-1].columns[-1]

    t30 = data_table_processing(table_list[0])
    t31 = data_table_processing(table_list[1:len(table_list)-1])
    t32 = data_table_processing(table_list[-1]) 
    
    t30.to_csv(f"{csv_filename1}.csv", index=False)
    t31.to_csv(f"{csv_filename2}.csv", index=False)
    t32.to_csv(f"{csv_filename3}.csv", index=False)
