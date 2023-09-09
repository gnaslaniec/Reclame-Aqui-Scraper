class Reclamacao:
    def __init__(self, url, texto, titulo, local, data_hora, status, problem_type, product_type, category):
        self.url = url
        self.texto = texto
        self.titulo = titulo
        self.local = local
        self.data_hora = data_hora
        self.status = status
        self.problem_type = problem_type
        self.product_type = product_type
        self.category = category

    def to_dict(self):
        return vars(self)
