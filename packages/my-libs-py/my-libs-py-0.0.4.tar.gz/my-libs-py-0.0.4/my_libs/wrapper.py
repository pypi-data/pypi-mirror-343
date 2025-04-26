from pyspark.sql.functions import col, regexp_extract, to_date, row_number, input_file_name, when, trim, regexp_replace, udf, lit
from pyspark.sql.window import Window
from pyspark.sql.types import StringType
import re
from pyspark.sql import DataFrame


class clean_data():

    def change_null_string(df):

        string_columns = [col_name for col_name, data_type in df.dtypes if data_type == 'string']
        df = df.na.fill('-', subset = string_columns)

        return df


    def change_null_numeric(df, type):

        numeric_columns = [col_name for col_name, data_type in df.dtypes if data_type == type]
        
        df = df.na.fill(0, subset=numeric_columns)

        return df
    

    def organize_data(df, column_id):
        
        df = df.withColumn("file_name", input_file_name())
        df = df.withColumn("file_date", regexp_extract(col("file_name"), r'\d{4}-\d{2}-\d{2}', 0))
        df = df.withColumn("file_date", to_date(col("file_date"), "yyyy-MM-dd"))

        window_spec = Window.partitionBy(column_id).orderBy(col("file_date").desc())

        df = df.withColumn("row_number", row_number().over(window_spec))

        df = df.withColumn("status", when(col("row_number") == 1, "ativo").otherwise("inativo"))
        df = df.drop("row_number")

        return df


    def remove_extra_spaces(df):

        string_cols = [col_name for col_name, col_type in df.dtypes if col_type == 'string']

        for col_name in string_cols:

            df = df.withColumn(col_name, regexp_replace(trim(col(col_name)), r'\s+', ' '))
            
        return df

class transform_data():

    def convert_currency_column(df, col_name):

        df = df.withColumn(col_name, regexp_replace(col(col_name), "[^0-9,R\\$]", ""))
        df = df.withColumn(col_name, regexp_replace(col(col_name), "R\\$", ""))
        df = df.withColumn(col_name, regexp_replace(col(col_name), "\\.", ""))
        df = df.withColumn(col_name, regexp_replace(col(col_name), ",", "."))
        df = df.withColumn(col_name, col(col_name).cast("double"))

        return df
    

    def extract_memory(df, column_name):

        
        def extract_memory_info(info):

            if isinstance(info, str) and info:
                padrao = r'(\d+)\s*(G[Bb])'
                resultado = re.search(padrao, info, re.IGNORECASE)
                if resultado:
                    return resultado.group(0)
            return '-'

        extrair_memoria_udf = udf(extract_memory_info, StringType())
        return df.withColumn('memoria', extrair_memoria_udf(col(column_name)))
    

    def type_monetary(df: DataFrame, column: str) -> DataFrame:

        df = df.withColumn(
            "moeda",
            when(
                col(column).contains("R$"),
                lit("R$")
            ).when(
                col(column).rlike(r"[$€£¥]"),
                regexp_extract(col(column), r"([$€£¥])", 1)
            ).otherwise(lit("moeda não identificada"))
        )
        return df
    
class test_data():

    def df_not_empty(df):

        is_empty = df.isEmpty()

        print(f'Está vazio? {is_empty}')

        assert is_empty == False

        count_lines_df = df.count()

        print(f'Quantidade de linhas: {count_lines_df}')

        assert count_lines_df != 0 


    def schema_equals_df_schema(df,schema):

        df_columns_list_names = df.schema.fieldNames()

        schema_columns_list_names = schema.fieldNames()

        diferences_array = ['| Nome Dataframe | Nome Schema | Coluna |']

        for i, name in enumerate(df_columns_list_names):

            if name != schema_columns_list_names[i]:

                diferences_array.append(f'| {name} | {schema_columns_list_names[i]} | {i_+ 1} |')

        print('Nomes')

        print(f'Nomes colunas dataframes: \n{df_columns_list_names}')

        print(f'Nomes colunas schema: \n{schema_columns_list_names}')

        if(len(diferences_array) > 1):

            print(f'Diferença ({len(diferences_array) - 1}):')

            for item in diferences_array:

                print(item)

        assert df_columns_list_names == schema_columns_list_names

        df_columns_list_types = [field.dataType for field in df.schema.fields]

        schema_columns_list_types = [field.dataType for field in schema.fields]

        diferences_array = ['| Tipo Dataframe | Tipo Schema | Coluna |']

        for i, _type in enumerate(df_columns_list_types):

            if _type != schema_columns_list_types[i]:

                diferences_array.append(f'| {_type} | {schema_columns_list_types[i]} | {i_+ 1} |')

        print('Tipos')

        print(f'Tipos colunas dataframes: \n{df_columns_list_types}')

        print(f'Tipos colunas schema: \n{schema_columns_list_types}')

        if(len(diferences_array) > 1):

            print(f'Diferença ({len(diferences_array) - 1}):')

            for item in diferences_array:

                print(item)

        assert df_columns_list_types == schema_columns_list_types


    def count_df_filtered_filter(df,filter):

        df_filter = df.filter(filter)

        count_lines_filtered = df_filter.count()

        df_unfilter = df.filter(~filter)

        count_lines_unfiltered = df_unfilter.count()

        count_lines_df = df.count()

        print(f'Quantidade de linhas filtradas: {count_lines_filtered}')

        print(f'Quantidade de linhas não filtradas: {count_lines_unfiltered}')

        print(f'Quantidade de linhas totais: {count_lines_df}')

        print(f'Resultado: {count_lines_filtered + count_lines_unfiltered} = {count_lines_df}')

        assert (count_lines_filtered + count_lines_unfiltered) == count_lines_df


    def count_df_filtered_is_not_null(df,column):

        df_filter = df.filter(col(column).isNotNull())

        count_lines_filtered = df_filter.count()

        df_unfilter = df.filter(col(column).isNull())

        count_lines_unfiltered = df_unfilter.count()

        count_lines_df = df.count()

        print(f'Quantidade de linhas não nulas: {count_lines_filtered}')

        print(f'Quantidade de linhas nulas: {count_lines_unfiltered}')

        print(f'Quantidade de linhas toais: {count_lines_df}')

        print(f'Resultado: {count_lines_filtered + count_lines_unfiltered} = {count_lines_df}')

        assert (count_lines_filtered + count_lines_unfiltered) == count_lines_df


    def count_union_df(df_union, df_list):

        count_lines_df_list = 0

        for df in df_list:
            count_lines_df_list += df.count()

        count_lines_df_union = df_union.count()

        print(f'Quantidade de linhas da lista de Dataframes: {count_lines_df_list}')

        print(f'Quantidade de linhas do Dataframe Resultante: {count_lines_df_union}')

        print(f'Diferença entre lista de dataframes e dataframe resultante: {count_lines_df_list - count_lines_df_union}')

        assert count_lines_df_list == count_lines_df_union


    def list_names_equal_df_names(df,list_name):

        df_columns_list_names = df.schema.fieldNames()

        diferences_array = ['| Nome Dataframe | Nome Lista | Coluna |']

        for i, name in enumerate(df_columns_list_names):

            if name != list_name[i]:

                diferences_array.append(f'| {name} | {list_name[i]} | {i + 1} |')

        print('Nomes')

        print(f'Nomes colunas dataframe:\n{df_columns_list_names}')

        print(f'Lista de nomes:\n{list_name}')

        if(len(diferences_array) > 1):

            print(f'Diferenças ({len(diferences_array) - 1}):')

            for item in diferences_array:

                print(item)

        assert df_columns_list_names == list_name


    def number_columns_list_names_and_df(df,list_names):

        len_columns_df = len(df.schema)

        len_list_names = len(list_names)

        print(f'Número de colunas dataframe: {len_columns_df}')

        print(f'Número de nomes lista> {len_list_names}')

        print(f'Diferença colunas dataframe e nomes lista: {len_columns_df - len_list_names}')

        assert len_columns_df == len_list_names


 