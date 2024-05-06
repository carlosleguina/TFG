from tqdm.notebook import tqdm
tqdm.pandas()
from user import User
from embeddings import Embeddings
import random

DATA_PATH = "../Data/"
QUESTIONS = ["Aspecto: ¿Cómo describirías su aspecto?",
"Olor: ¿Qué me puedes decir sobre su olor?",
"Textura: ¿Cómo describirías su textura?",
"Sabor: ¿Qué me puedes decir sobre su sabor?",
"Color: ¿Cómo describirías su color?",
"Dureza: ¿Qué tan duro es?",
"Dulzura: ¿Puedes comentar sobre su nivel de dulzura?"]

QUESTIONS_DIC = {
    'aspecto': ['¿Cómo describirías el aspecto general de la galleta?', '¿Qué me puedes decir sobre su aspecto?', '¿Qué te ha parecido el aspecto de la galleta?', '¿Cómo describirías su aspecto?', 'Háblame del aspecto de la galleta...','¿Qué más puedes decirme sobre cómo se ve la galleta?', '¿Qué te ha parecido llamativo de la apariencia?'],
    'olor': ['¿Cómo influye el olor en tu percepción de la galleta?','¿Puedes describir las diferentes notas o aromas que percibes?','¿Qué me puedes decir sobre su olor?', '¿Qué te ha parecido el olor de la galleta?', '¿Cómo describirías su olor?', 'Háblame del olor de la galleta...','¿Cómo huele la galleta?', '¿Qué más puedes decirme sobre el olor?'],
    'textura': ['¿Cómo describirías la textura de la galleta al tocarla?','¿Qué me puedes decir sobre su textura?', '¿Qué te ha parecido la textura de la galleta?', '¿Cómo describirías su textura?', 'Háblame de la textura de la galleta...','¿Qué más puedes decirme sobre la textura?'],
    'sabor': ['¿Cómo describirías el sabor de la galleta?', '¿Qué me puedes decir sobre su sabor?', '¿Qué te ha parecido el sabor de la galleta?', '¿Cómo describirías su sabor?', 'Háblame de su sabor...','¿Qué es lo que más te ha llamado la atención del sabor?'],
    'color': ['¿Cómo describirías el color de la galleta?', '¿Qué me puedes decir sobre su color?', '¿Qué te ha parecido el color de la galleta?', '¿Cómo describirías su color?', 'Háblame del color de la galleta...','¿Qué más puedes decirme sobre el color?', '¿Qué te ha gustado del color de la galleta?', 'Y del color, ¿qué me dices?'],
    'dureza': ['¿Cómo describirías la dureza de la galleta?', '¿Cómo de dura te ha parecido la galleta?', '¿Qué te ha parecido la dureza de la galleta?', '¿Qué me puedes decir sobre la dureza de la galleta?', 'Háblame de la dureza de la galleta...', '¿Y qué me dices de la dureza?', '¿Qué te ha gustado la dureza de la galleta?'],
    'dulzor': ['¿Cómo describirías la dulzor de la galleta?', '¿Cómo describirías la dulzor de la galleta?', '¿Qué te ha parece el nivel de dulzor de la galleta?', 'Bueno, ¿qué te ha parecido la dulzor de la galleta?', 'Ahora hablame de la dulzor de la galleta...', '¿Qué te ha parecido la dulzor de la galleta?', '¿Cómo de dulce te parece la galleta?']
}
AVAILABLE_FIELDS = ["aspecto", "olor", "textura", "sabor", "color", "dureza", "dulzor"]


embedding = Embeddings()
def get_sampled_questions():
    string = ''
    for question in QUESTIONS:
        string = string + question+ '\n'
    return string

class Bot:
    def __init__(self):
        self.conversation_history = [
            {"role": "assistant", "content": "¿Cúal es tu código de consumidor?"}]

        self.first_answer = None
        self.missing_fields = []
        self.last_field = None
        
        self.opinion = None
        
        self.user = User()
        self.similarity_table = None

    def get_categories_table(self):
        return embedding.get_categories_table()
    def get_conversation_history(self):
        return self.conversation_history

    def reset_conversation_history(self):
        self.conversation_history = [
            {"role": "assistant", "content": "¿Cúal es tu código de consumidor?"}]
    
    def get_first_answer(self):
        return self.first_answer
       
    def set_first_answer(self, opinion):
        
        self.opinion = opinion
        self.user.set_opinion(opinion)
        self.first_answer = True

    def get_missing_fields(self):
        return self.missing_fields

    def set_missing_fields(self):
        self.similarity_table.sort_values(by="similitud", ascending=True)
        self.missing_fields = self.similarity_table[abs(self.similarity_table["similitud"]) < 0.19].index.tolist()
        self.user.set_missing_fields(self.missing_fields)

    def set_similarity_table(self):
        # Create a copy of the DataFrame slice to avoid SettingWithCopyWarning
        embedding.set_similarity_table(self.opinion)
        self.similarity_table = embedding.get_similarity_table()
    def get_opinion(self):
        return self.opinion

    def get_similarity_table(self):
        return self.similarity_table
    
    def query_message(self, missing_field) -> str:
        """Return a message for GPT, with relevant source texts pulled from a dataframe."""
        introduction = 'Utiliza los siguientes ejemplos como guía para hacer una única pregunta, solo la pregunta, sobre los campos que faltan. Si no quedan campos, simplemente dí "Muchas gracias por rellenar el formulario"'
        
        sampled_questions = f"Ejemplo de preguntas: {get_sampled_questions()}"

        message = introduction
        next_field = f'\n\nCampo que falta:\n"""\n{missing_field}\n"""'
        return message + sampled_questions + next_field
    
    def set_last_field(self, field):
        self.last_field = field

    def get_last_field(self):
        return self.last_field

    def ask(
        self,
        print_message: bool = False,
    ) -> str:
        """Responde una consulta utilizando GPT y un marco de datos de textos e incrustaciones relevantes."""

        if(len(self.missing_fields) == 0):
            return "Muchas gracias por rellenar el formulario"
            
        else:
            missing_field = self.missing_fields.pop(0)
            self.set_last_field(missing_field)
            message = random.choice(QUESTIONS_DIC[missing_field])
            if print_message:
                print(message)
            self.first_answer = False
            return message
    
    def get_last_field(self):
        return self.last_field
    def re_ask(self, print_message: bool = False,):
        
        message = random.choice(QUESTIONS_DIC[self.last_field])
        if print_message:
            print(message)
        self.first_answer = False
        return message


    def add_conversation(self,role,
                        content
                        ):
        """
        Adds a message to the conversation history.

        Parameters:
        - role (str): The role of the message sender ("user" or "assistant").
        - content (str): The content of the message.
        """
        self.conversation_history.append({"role": role, "content": content})

    def start(self, opinion):
        self.set_first_answer(opinion)
        self.set_similarity_table()
        self.set_missing_fields()
        for field in AVAILABLE_FIELDS:
            if field not in self.missing_fields:
                self.user.set_available_fields(field, self.opinion)

    def set_consumer_code(self, consumer_code):
        self.user.set_consumer_code(consumer_code)
        self.add_conversation('assistant', '¿Cuál es tu código de galleta?')
    
    def set_cookie_code(self, cookie_code):
        self.user.set_cookie_code(cookie_code)
        self.add_conversation('assistant', '¡Déjame tu opinión sobre la galleta!')

    def get_cookie_code(self):
        return self.user.get_cookie_code()
