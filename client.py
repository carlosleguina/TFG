from openai import OpenAI


GPT_MODEL = "gpt-3.5-turbo"


# def query_message(self, missing_field) -> str:
#     """Return a message for GPT, with relevant source texts pulled from a dataframe."""
#     introduction = 'Utiliza los siguientes ejemplos como guía para hacer una única pregunta, solo la pregunta, sobre los campos que faltan. Si no quedan campos, simplemente dí "Muchas gracias por rellenar el formulario"'
    
#     sampled_questions = f"Ejemplo de preguntas: {get_sampled_questions()}"
#     message = introduction
#     next_field = f'\n\nCampo que falta:\n"""\n{missing_field}\n"""'
#     return message + sampled_questions + next_field
# def ask(
#     self,
#     print_message: bool = False,
# ) -> str:
#     """Responde una consulta utilizando GPT y un marco de datos de textos e incrustaciones relevantes."""
    
#     if self.categories_table is None:
#         self.categories_table = self.load_categories()
    
#     if(len(self.missing_fields) == 0):
#         return "Muchas gracias por rellenar el formulario"
        
#     else:
#         missing_field = self.missing_fields.pop(0)
#         message = self.query_message(missing_field)
#         if print_message:
#             print(message)
#         messages = [
#             {"role": "assistant", "content": "Eres un asistente muy útil que únicamente genera una única pregunta sobre el campo que se le pide basandote en unas plantillas de preguntas."},
#             {"role": "user", "content": message},
#         ]
#         response = self.client.chat(messages)
#         response_message = response.choices[0].message.content
#         self.first_answer = False
#         return response_message

class Client:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    def chat(self, messages):
        return self.client.chat.completions.create(
                model=GPT_MODEL,
                messages= messages,
                temperature=1
            )