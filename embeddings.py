from transformers import AutoModel, AutoTokenizer
from numpy.linalg import norm
import os
import pandas as pd
import numpy as np


AVAILABLE_FIELDS = ["aspecto", "olor", "textura", "sabor", "color", "dureza", "dulzor"]
DESCRIPTION_FIELDS = ["Aspecto: apariencia visual. Esto puede incluir características como su forma, tamaño, color, y la presencia de cualquier adorno o decoración.",
                      "Olor: Impresión que los efluvios producen en el olfato. Aquello que es capaz de producir olor.Esperanza, promesa u oferta de algo.",
                      "Textura: cómo se siente la galleta al tacto y al comerla. Esto puede incluir características como su dureza, suavidad, crujiente, esponjosidad, rugosidad, entre otras.",
                      "Sabor: Sensación que ciertos cuerpos producen en el órgano del gusto.Impresión que algo produce en el ánimo.Propiedad que tienen algunas cosas de parecerse a otras con que se las compara.",
                      "Color: Sensación producida por los rayos luminosos que impresionan los órganos visuales y que depende de la longitud de onda. Usado también como femenino",
                      "Dureza: Cualidad de duro.",
                      "Dulzor: percepción de sabor dulce que se experimenta al comerla. Este sabor dulce generalmente proviene de los azúcares o edulcorantes utilizados en la receta de la galleta."]
EMBEDDINGS_TABLE_PATH = "Data/tabla_de_categorias.csv"
DATA_PATH = "Data/"

def save_embeddings(df, embeddings_col, file_path):
        # Asegurarse de que la columna de embeddings existe
    if embeddings_col not in df.columns:
        raise ValueError(f"The column {embeddings_col} does not exist in the DataFrame.")

    # Convertir los arrays de embeddings directamente en la columna deseada a una cadena de texto
    df[embeddings_col] = df[embeddings_col].apply(lambda x: ' '.join(format(f, '.8f') for f in x))

    # Guardar el DataFrame
    df.to_csv(file_path, index=False)
    
def load_embeddings(file_path):
    df = pd.read_csv(file_path)
    # Convertir las cadenas en la columna 'Embeddings' a arrays de Numpy
    df['embeddings'] = df['embeddings'].apply(lambda x: np.fromstring(x, sep=' '))
    return df

class Embeddings:
    def __init__(self):
        self.model =  AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-es', trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained('jinaai/jina-embeddings-v2-base-es')
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        if not os.path.exists(EMBEDDINGS_TABLE_PATH):
            self.categories = self.load_categories()
        else:
            self.categories = load_embeddings(EMBEDDINGS_TABLE_PATH)
        self.similarity_table = pd.DataFrame(index= self.categories['categorias'])
        self.similarity_table['similitud'] = np.nan
    
    def load_categories(self):
        categories_table = pd.DataFrame(AVAILABLE_FIELDS, columns=["categorias"])
        categories_table['definicion'] = DESCRIPTION_FIELDS
        categories_table['embeddings'] = categories_table['definicion'].apply(self.get_embedding)
        save_embeddings(categories_table, 'embeddings', EMBEDDINGS_TABLE_PATH)
        return categories_table
    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()
        return embeddings.flatten()
    def set_similarity_table(self, opinion):
        texts = opinion.split('.')
        matrix= self.categories['embeddings'].apply(lambda x: self.cosine_similarity(x,self.model.encode(texts)))
        for i, categoria in enumerate(self.similarity_table.index):
            self.similarity_table.loc[categoria, 'similitud'] = matrix[i].max()
    def get_similarity_table(self):
        return self.similarity_table
    def get_categories_table(self):
        return self.categories
    def cosine_similarity(self, a, b):
        if isinstance(a, str):
         # Separar los elementos por espacios y convertir a float
         a = np.array([float(x) for x in a.split()], dtype='float32')
    
    # Si 'b' es una cadena, hacer lo mismo
        if isinstance(b, str):
            b = np.array([float(x) for x in b.split()], dtype='float32')
        return (a @ b.T) / (norm(a)*norm(b))
    
    def get_embedding(self,text):
        text = text.replace("/n", " ")
        response = self.model.encode(text)
        return response