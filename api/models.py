from django.db import models
from django.core.validators import RegexValidator


class Address(models.Model):
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade}/{self.estado}"


class Contact(models.Model):
    TIPO_CHOICES = [
        ('celular', 'Celular'),
        ('residencial', 'Telefone Residencial'),
        ('trabalho', 'Telefone Trabalho'),
        ('outro', 'Outro'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    numero = models.CharField(max_length=20)
    is_whatsapp = models.BooleanField(default=False)
    observacao = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.numero}"


class Patient(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    # Dados Pessoais
    nome = models.CharField(max_length=255)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        default='99999999999',
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='CPF deve conter exatamente 11 dígitos numéricos'
            )
        ]
    )
    rg = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    
    # Contatos
    email = models.EmailField(blank=True, null=True)
    contatos = models.ManyToManyField(Contact, related_name='pacientes', blank=True)
    
    # Endereço
    endereco = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='pacientes', blank=True, null=True)
    
    # Informações Adicionais
    profissao = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Anamnesis(models.Model):
    paciente = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='anamnese')
    data_atualizacao = models.DateTimeField(auto_now=True)
    problemas_saude = models.TextField(blank=True, null=True)
    medicamentos = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    cirurgias = models.TextField(blank=True, null=True)
    ultima_consulta_dentista = models.DateField(blank=True, null=True)
    motivo_ultima_consulta = models.CharField(max_length=255, blank=True, null=True)
    experiencia_tratamento = models.TextField(blank=True, null=True)
    fumante = models.BooleanField(default=False)
    alcool = models.BooleanField(default=False)
    frequencia_escovacao = models.CharField(max_length=50, blank=True, null=True)
    usa_fio_dental = models.BooleanField(default=False)
    sensibilidade_dental = models.BooleanField(default=False)
    sangramento_gengival = models.BooleanField(default=False)
    ranger_dentes = models.BooleanField(default=False)
    dores_articulacao = models.BooleanField(default=False)
    gestante = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    hipertensao = models.BooleanField(default=False)
    problemas_cardiacos = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Anamnese - {self.paciente.nome}"


class Appointment(models.Model):
    paciente = models.ForeignKey(Patient, related_name="agendamentos", on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.CharField(max_length=10)
    tipo = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('remarcado', 'Remarcado'),
        ('nao_compareceu', 'Não Compareceu'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado')
    observacoes = models.TextField(blank=True, null=True)
    duracao = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.paciente.nome} - {self.data} {self.horario}"
