class Pentateuco:
    def __init__(self):
        self.livros = [
            "Gênesis",
            "Êxodo",
            "Levítico",
            "Números",
            "Deuteronômio"
        ]

    def __str__(self):
        return ", ".join(self.livros)
    
class LivrosHistoricos:
    def __init__(self):
        self.livros = [
            "Josué",
            "Juízes",
            "Rute",
            "1 Samuel",
            "2 Samuel",
            "1 Reis",
            "2 Reis",
            "1 Crônicas",
            "2 Crônicas",
            "Esdras",
            "Neemias",
            "Ester"
        ]

    def __str__(self):
        return ", ".join(self.livros)
    
class LivrosPoeticos:  
    def __init__(self):
        self.livros = [
            "Jó",
            "Salmos",
            "Provérbios",
            "Eclesiastes",
            "Cantares de Salomão"
        ]

    def __str__(self):
        return ", ".join(self.livros)
    
class ProfetasMaiores:
    def __init__(self):
        self.livros = [
            "Isaías",
            "Jeremias",
            "Lamentações",
            "Ezequiel",
            "Daniel"
        ]

    def __str__(self):
        return ", ".join(self.livros)
class ProfetasMenores:  
    def __init__(self):
        self.livros = [
            "Oséias",
            "Joel",
            "Amós",
            "Obadias",
            "Jonas",
            "Miquéias",
            "Naum",
            "Habacuque",
            "Sofonias",
            "Ageu",
            "Zacarias",
            "Malaquias"
        ]

    def __str__(self):
        return ", ".join(self.livros)
class Evangelhos:
    def __init__(self):
        self.livros = [
            "Mateus",
            "Marcos",
            "Lucas",
            "João"
        ]

    def __str__(self):
        return ", ".join(self.livros)
class CartasPaulinas:
    def __init__(self):
        self.livros = [
            "Romanos",
            "1 Coríntios",
            "2 Coríntios",
            "Gálatas",
            "Efésios",
            "Filipenses",
            "Colossenses",
            "1 Tessalonicenses",
            "2 Tessalonicenses",
            "1 Timóteo",
            "2 Timóteo",
            "Tito",
            "Filemom"
        ]

    def __str__(self):
        return ", ".join(self.livros)
class CartasGerais:
    def __init__(self):
        self.livros = [
            "Hebreus",
            "Tiago",
            "1 Pedro",
            "2 Pedro",
            "1 João",
            "2 João",
            "3 João",
            "Judas"
        ]

    def __str__(self):
        return ", ".join(self.livros)
class Apocalipse:
    def __init__(self):
        self.livros = [
            "Apocalipse"
        ]

    def __str__(self):
        return ", ".join(self.livros)
    
class AntigoTestamento:
    def __init__(self):
        self.livros = [
            "Pentateuco",
            "Livros Históricos",
            "Livros Poéticos",
            "Profetas Maiores",
            "Profetas Menores"
        ]

    def __str__(self):
        return ", ".join(self.livros)
class NovoTestamento:
    def __init__(self):
        self.livros = [
            "Evangelhos",
            "Cartas Paulinas",
            "Cartas Gerais",
            "Apocalipse"
        ]

    def __str__(self):
        return ", ".join(self.livros)   
    
class Biblia:
    def __init__(self):
        self.antigo_testamento = AntigoTestamento()
        self.novo_testamento = NovoTestamento()
        self.livros_da_biblia = [
            Pentateuco(),
            LivrosHistoricos(),
            LivrosPoeticos(),
            ProfetasMaiores(),
            ProfetasMenores(),
            Evangelhos(),
            CartasPaulinas(),
            CartasGerais(),
            Apocalipse()
        ]

    def __str__(self):
        return f"Antigo Testamento: {self.antigo_testamento}\nNovo Testamento: {self.novo_testamento}"
    def listar_livros(self):
        for categoria in self.livros_da_biblia:
            print(f"{categoria.__class__.__name__}: {categoria}")
    def listar_livros_antigo_testamento(self):
        for categoria in self.livros_da_biblia[:5]:
            print(f"{categoria.__class__.__name__}: {categoria}")
    def listar_livros_novo_testamento(self):
        for categoria in self.livros_da_biblia[5:]:
            print(f"{categoria.__class__.__name__}: {categoria}")
    def listar_livros_completo(self):
        for categoria in self.livros_da_biblia:
            print(f"{categoria.__class__.__name__}: {categoria}")
    def listar_livros_por_categoria(self, categoria):
        for livro in self.livros_da_biblia:
            if livro.__class__.__name__ == categoria:
                print(f"{livro.__class__.__name__}: {livro}")
    
    
                
if __name__ == "__main__":
    biblia = Biblia()
    print(biblia)
    print("\nLivros do Antigo Testamento:")
    biblia.listar_livros_antigo_testamento()
    print("\nLivros do Novo Testamento:")
    biblia.listar_livros_novo_testamento()
    print("\nLivros da Bíblia:")
    biblia.listar_livros()
    print("\nLivros da Bíblia por categoria:")
    biblia.listar_livros_por_categoria("Pentateuco")
    
