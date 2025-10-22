#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from api.models import Patient, Contact, Address, Appointment

# Criar alguns dados de teste
def create_test_data():
    # Criar endereço
    endereco = Address.objects.create(
        cep="12345678",
        logradouro="Rua das Flores",
        numero="123",
        bairro="Centro",
        cidade="São Paulo",
        estado="SP"
    )
    
    # Criar contato
    contato = Contact.objects.create(
        tipo="celular",
        numero="11999999999",
        is_whatsapp=True
    )
    
    # Criar paciente
    paciente = Patient.objects.create(
        nome="João Silva",
        email="joao@email.com",
        cpf="12345678901",
        endereco=endereco,
        status="ativo"
    )
    
    # Adicionar contato ao paciente
    paciente.contatos.add(contato)
    
    # Criar agendamento
    Appointment.objects.create(
        paciente=paciente,
        data="2025-10-23",
        horario="14:00",
        tipo="Consulta",
        status="agendado",
        duracao=60
    )
    
    print("Dados de teste criados com sucesso!")

if __name__ == "__main__":
    create_test_data()