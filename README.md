# Dental Backend Django

Django backend com DRF para o sistema de agendamentos dentários.

## Problemas Identificados e Soluções

### 1. Configuração do Backend

**Problemas encontrados:**
- Estrutura de dados diferente entre frontend e backend
- Frontend estava fazendo chamadas para localhost:5000 (Node.js antigo)
- Campos de dados não correspondiam

**Soluções aplicadas:**
- Ajustada interface TypeScript no frontend para corresponder aos modelos Django
- URLs de API já configuradas para http://127.0.0.1:8000
- Modificadas as permissions para AllowAny temporariamente para testes

### 2. Setup e Execução

**Passo a passo:**

1. **Instalar dependências:**
```bash
cd c:\Users\Eduardo\Desktop\Dental\dental-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Criar migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Criar superuser (opcional):**
```bash
python manage.py createsuperuser
```

4. **Criar dados de teste:**
```bash
python create_test_data.py
```

5. **Executar servidor:**
```bash
python manage.py runserver
```

### 3. Endpoints Disponíveis

- **Pacientes:** http://127.0.0.1:8000/api/pacientes/
- **Agendamentos:** http://127.0.0.1:8000/api/agendamentos/
- **Admin:** http://127.0.0.1:8000/admin/
- **Auth JWT:** http://127.0.0.1:8000/api/auth/token/

### 4. Estrutura de Dados

**Paciente (Patient):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "cpf": "12345678901",
  "endereco": {
    "logradouro": "Rua das Flores",
    "numero": "123",
    "cidade": "São Paulo",
    "estado": "SP"
  },
  "contatos": [
    {
      "tipo": "celular",
      "numero": "11999999999",
      "is_whatsapp": true
    }
  ]
}
```

**Agendamento (Appointment):**
```json
{
  "id": 1,
  "paciente": 1,
  "paciente_nome": "João Silva",
  "data": "2025-10-23",
  "horario": "14:00",
  "tipo": "Consulta",
  "status": "agendado",
  "duracao": 60
}
```

### 5. Mudanças no Frontend

**Ajustes já realizados:**
- Interface TypeScript atualizada para corresponder aos modelos Django
- Renderização dos dados de pacientes ajustada para usar `endereco` e `contatos`
- Removidos campos obsoletos como `ultimaConsulta` e `proximaConsulta`

**Para testar:**
1. Execute o backend Django (passos acima)
2. Execute o frontend Next.js
3. Verifique se as páginas de pacientes e agendamentos carregam corretamente

### 6. Próximos Passos

- [ ] Implementar autenticação JWT no frontend
- [ ] Adicionar validações nos formulários
- [ ] Criar páginas de edição de pacientes
- [ ] Implementar filtros avançados
- [ ] Adicionar tratamento de erros mais robusto

### 7. Testando se está funcionando

**Teste 1: API diretamente no navegador**
```
http://127.0.0.1:8000/api/pacientes/
http://127.0.0.1:8000/api/agendamentos/
```
Deve retornar JSON com dados.

**Teste 2: Com PowerShell**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/pacientes/" -Method GET
```

**Teste 3: Logs do console**
Abra o console do navegador (F12) e veja os logs detalhados que foram adicionados.

**Se os testes acima funcionarem mas o frontend não:**
- Verifique o console do navegador para erros
- Veja o arquivo TROUBLESHOOTING.md no projeto frontend
- Verifique se ambos (backend e frontend) estão rodando
