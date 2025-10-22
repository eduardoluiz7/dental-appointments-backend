# Endpoints da API

## 1. Pacientes (`/api/pacientes/`)

### GET /api/pacientes/
Lista todos os pacientes
```json
# Endpoints da API

Este documento lista os endpoints disponíveis no projeto e exemplos de JSON de resposta.

Base URL: http://127.0.0.1:8000/api/

## 0. Autenticação

### POST /api/auth/login/
Endpoint customizado que retorna os tokens JWT (access/refresh) e dados do usuário.

Request (exemplo):
```json
{
  "username": "admin",
  "password": "sua-senha"
}
```

Response (exemplo):
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>",
  "user": { "id": 1, "username": "admin", "email": "admin@example.com" }
}
```

Além desse endpoint, o projeto também expõe os endpoints padrão do SimpleJWT:
- `POST /api/auth/token/` (TokenObtainPairView)
- `POST /api/auth/token/refresh/` (TokenRefreshView)


## 1. Pacientes (`/api/pacientes/`)

### GET /api/pacientes/
Lista todos os pacientes

Response (exemplo):
```json
[]
```

### POST /api/pacientes/
Cria um novo paciente. Se o payload incluir `endereco`, ele será criado aninhado.

Request (exemplo):
```json
{
  "nome": "João Silva",
  "cpf": "12345678901",
  "data_nascimento": "1990-01-01",
  "sexo": "M",
  "email": "joao@example.com",
  "endereco": {
    "cep": "12345678",
    "logradouro": "Rua Example",
    "numero": "123",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "estado": "SP"
  }
}
```

Response (criação):
```json
{
  "id": 1,
  "nome": "João Silva",
  "cpf": "12345678901",
  "rg": null,
  "data_nascimento": "1990-01-01",
  "sexo": "M",
  "email": "joao@example.com",
  "contatos": [],
  "endereco": { "id": 1, "cep": "12345678", "logradouro": "Rua Example", "numero": "123", "bairro": "Centro", "cidade": "São Paulo", "estado": "SP" },
  "status": "ativo",
  "data_cadastro": "2025-10-21T10:00:00Z"
}
```

### GET /api/pacientes/{id}/
Retorna um paciente específico (serializador principal)

### GET /api/pacientes/{id}/detalhes/
Retorna detalhes completos do paciente: dados pessoais, contatos, endereço e anamnese (se existir).

Response (exemplo resumido):
```json
{
  "id": 1,
  "nome": "João Silva",
  "cpf": "12345678901",
  "rg": null,
  "data_nascimento": "1990-01-01",
  "sexo": "M",
  "sexo_display": "Masculino",
  "email": "joao@example.com",
  "status": "ativo",
  "status_display": "Ativo",
  "data_cadastro": "2025-10-21T10:00:00Z",
  "contatos": [ /* lista de contatos */ ],
  "endereco": { /* endereço */ },
  "anamnese": { /* anamnese completa ou null */ }
}
```

### POST /api/pacientes/{id}/add_contact/
Adiciona um contato ao paciente.

Request (exemplo):
```json
{ "tipo": "celular", "numero": "11999999999", "is_whatsapp": true }
```

### GET /api/pacientes/{id}/contacts/
Lista os contatos associados ao paciente.

### GET /api/pacientes/{id}/anamnesis/
Retorna a anamnese (se existir) do paciente.


## 2. Agendamentos (`/api/agendamentos/`)

### GET /api/agendamentos/
Lista todos os agendamentos

Response (exemplo):
```json
[]
```

### POST /api/agendamentos/
Cria um agendamento. Payload básico:
```json
{
  "paciente": 1,
  "data": "2025-10-21",
  "horario": "14:30",
  "tipo": "Consulta de rotina",
  "duracao": 30
}
```

### GET /api/agendamentos/{id}/detalhes/
Retorna detalhes do agendamento, inclusive dados básicos do paciente e os campos mais relevantes da anamnese.

Response (exemplo resumido):
```json
{
  "agendamento": { /* dados do agendamento */ },
  "paciente": { /* dados básicos do paciente + contatos */ },
  "anamnese": { /* alergias, medicamentos, sinais relevantes */ }
}
```

### GET /api/agendamentos/proximas/?data=YYYY-MM-DD
Filtra os agendamentos pela data informada.


## 3. Endereços (`/api/enderecos/`)

### GET /api/enderecos/
Lista todos os endereços.

### POST /api/enderecos/
Cria um endereço.


## 4. Contatos (`/api/contatos/`)

### GET /api/contatos/?paciente={id}
Lista contatos, opcionalmente filtrando por paciente.

### POST /api/contatos/
Cria um contato.


## 5. Anamneses (`/api/anamneses/`)

### GET /api/anamneses/?paciente={id}
Lista anamneses, opcionalmente filtrando por paciente.

### POST /api/anamneses/
Cria a anamnese para um paciente (campos médicos e odontológicos).


## Comportamento REST padrão
Todos os endpoints acima suportam as operações padrão do REST quando aplicável:
- `GET /` - listar
- `POST /` - criar
- `GET /{id}/` - detalhe
- `PUT /{id}/` - atualizar completamente
- `PATCH /{id}/` - atualizar parcialmente
- `DELETE /{id}/` - remover


## Parâmetros de filtro (resumo)
- Pacientes: `?search=` (busca por nome, email, cpf)
- Agendamentos: `?data=`, `?status=`, `?busca=` (busca por paciente/nome/tipo)
- Contatos: `?paciente=` (filtra contatos por paciente)
- Anamneses: `?paciente=` (filtra anamnese por paciente)
