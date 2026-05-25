# 🔐 Security API - Sistema de Autenticação com JWT

Uma API REST completa de autenticação construída com **Django** e **Django REST Framework**, com suporte para JWT, reset de password por email e CORS.

---

## 📋 Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Estrutura do Projecto](#estrutura-do-projecto)
- [Rotas da API](#rotas-da-api)
- [Autenticação JWT](#autenticação-jwt)
- [Segurança](#segurança)
- [Testes](#testes)

---

## ✨ Características

✅ **Autenticação JWT** - Access tokens (10 min) e refresh tokens (7 dias)  
✅ **Registro de Utilizadores** - Criação de contas com validação  
✅ **Login/Logout** - Com blacklist de tokens  
✅ **Perfil do Utilizador** - Visualizar dados autenticados  
✅ **Alteração de Password** - Com verificação da password antiga  
✅ **Atualização de Perfil** - Editar dados do utilizador  
✅ **Reset de Password** - Via email com token personalizado  
✅ **CORS Ativo** - Para frontends em `localhost:3000` e outros  
✅ **Email Personalizado** - Configurado com Gmail SMTP

---

## 📦 Requisitos

- Python 3.8+
- Django 6.0.5
- Django REST Framework 3.17.1
- Virtualenv

---

## 🚀 Instalação

### 1️⃣ Clone ou configure o projecto

```bash
cd /home/benilson/Documentos/security
```

### 2️⃣ Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Execute as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Crie um superutilizador (opcional)

```bash
python manage.py createsuperuser
```

### 6️⃣ Inicie o servidor

```bash
python manage.py runserver 8000
```

A API estará disponível em: **http://localhost:8000/api/v1/**

---

## ⚙️ Configuração

### Ficheiros Principais

| Ficheiro             | Descrição                               |
| -------------------- | --------------------------------------- |
| `auth/settings.py`   | Configurações gerais (CORS, JWT, Email) |
| `auth/urls.py`       | Rotas principais                        |
| `api/urls.py`        | Rotas da API                            |
| `api/views.py`       | Lógica dos endpoints                    |
| `api/models.py`      | Modelos (User customizado)              |
| `api/serializers.py` | Serializers para validação              |
| `api/signals.py`     | Signal para reset de password por email |

### Variáveis de Ambiente Importantes

```python
# auth/settings.py

# Email
EMAIL_HOST_USER = 'seu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua_app_password'

# JWT
ACCESS_TOKEN_LIFETIME = timedelta(minutes=10)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]
```

---

## 📁 Estrutura do Projecto

```
security/
├── auth/                      # Configurações Django
│   ├── settings.py           # Configurações (CORS, JWT, Email, etc)
│   ├── urls.py               # Rotas principais
│   ├── wsgi.py
│   └── asgi.py
├── api/                       # Aplicação de autenticação
│   ├── models.py             # User model customizado
│   ├── views.py              # Endpoints da API
│   ├── urls.py               # Rotas da API
│   ├── serializers.py        # Validação de dados
│   ├── signals.py            # Email de reset de password
│   ├── admin.py
│   └── migrations/
├── db.sqlite3                 # Base de dados
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔌 Rotas da API

Todas as rotas começam com: **`http://localhost:8000/api/v1/`**

### 1️⃣ Registro (Criar Conta)

```http
POST /api/v1/register/
Content-Type: application/json

{
  "username": "joao123",
  "email": "joao@example.com",
  "password": "SenhaForte123!",
  "password2": "SenhaForte123!",
  "first_name": "João",
  "last_name": "Silva"
}
```

**Resposta (201 Created):**

```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "joao123",
    "email": "joao@example.com",
    "first_name": "João",
    "last_name": "Silva"
  }
}
```

---

### 2️⃣ Login (Obter Tokens)

```http
POST /api/v1/login/
Content-Type: application/json

{
  "username": "joao123",
  "password": "SenhaForte123!"
}
```

**Resposta (200 OK):**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 3️⃣ Renovar Token (Refresh)

```http
POST /api/v1/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Resposta (200 OK):**

```json
{
  "access": "novo_access_token..."
}
```

---

### 4️⃣ Perfil do Utilizador (Requer Autenticação)

```http
GET /api/v1/perfil/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Resposta (200 OK):**

```json
{
  "username": "joao123",
  "email": "joao@example.com",
  "first_name": "João",
  "last_name": "Silva",
  "date_joined": "2026-05-25T10:30:00Z",
  "last_login": "2026-05-25T12:00:00Z"
}
```

---

### 5️⃣ Logout (Blacklist Token)

```http
POST /api/v1/logout/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Resposta (205 Reset Content):**

```json
{
  "message": "User logged out successfully"
}
```

---

### 6️⃣ Alterar Password (Requer Autenticação)

```http
PATCH /api/v1/ChangePassword/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "old_password": "SenhaForte123!",
  "new_password": "NovaSenha456!"
}
```

**Resposta (200 OK):**

```json
{
  "message": "Password changed successfully"
}
```

---

### 7️⃣ Atualizar Perfil (Requer Autenticação)

```http
PATCH /api/v1/update-profile/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "first_name": "João Carlos",
  "last_name": "Silva Santos",
  "email": "novo_email@example.com"
}
```

**Resposta (200 OK):**

```json
{
  "message": "Profile updated successfully",
  "user": {
    "username": "joao123",
    "email": "novo_email@example.com",
    "first_name": "João Carlos",
    "last_name": "Silva Santos"
  }
}
```

---

### 8️⃣ Reset de Password (Sem Autenticação)

```http
POST /api/password_reset/
Content-Type: application/json

{
  "email": "joao@example.com"
}
```

**Processo:**

1. Email é enviado automaticamente com um token
2. Usa esse token para confirmar o reset

**Resposta (200 OK):**

```json
{
  "status": "success"
}
```

---

### 9️⃣ Confirmar Reset de Password

```http
POST /api/password_reset/confirm/
Content-Type: application/json

{
  "token": "abc123token...",
  "password": "NovaSenha789!"
}
```

**Resposta (200 OK):**

```json
{
  "status": "success"
}
```

---

## 🔐 Autenticação JWT

### Como Funciona

1. **Login** → Recebe `access_token` + `refresh_token`
2. **Requests** → Envia `Authorization: Bearer <access_token>`
3. **Token Expira** → Usa `refresh_token` para obter novo `access_token`
4. **Logout** → Token é adicionado à blacklist

### Tempos de Expiração

- **Access Token:** 10 minutos
- **Refresh Token:** 7 dias

### Exemplo com cURL

```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8000/api/v1/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"joao123","password":"SenhaForte123!"}' | jq -r '.access')

# 2. Usar token
curl -X GET http://localhost:8000/api/v1/perfil/ \
  -H "Authorization: Bearer $TOKEN"

# 3. Renovar token
curl -X POST http://localhost:8000/api/v1/token/refresh/ \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$REFRESH_TOKEN\"}"
```

---

## 🛡️ Segurança

### ✅ Implementado

| Feature              | Descrição                                 |
| -------------------- | ----------------------------------------- |
| **Password Hashing** | Algoritmo PBKDF2 (Django padrão)          |
| **Token Blacklist**  | Logout invalida tokens                    |
| **CORS**             | Controlo de origens (localhost:3000, etc) |
| **HTTPS Ready**      | Pronto para produção com SSL              |
| **Email Verificado** | Sinal para emails personalizados          |

### 🔧 Configurações de Segurança

```python
# settings.py

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]
```

---

## 📧 Email (Reset de Password)

### Configuração Gmail

1. Ativa 2FA na conta Gmail
2. Cria uma **App Password** em: https://myaccount.google.com/apppasswords
3. Copia a password gerada
4. Atualiza `settings.py`:

```python
EMAIL_HOST_USER = 'seu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'app_password_aqui'
```

### Email Personalizado

O email de reset tem este formato:

```
Assunto: 🔐 Reset da tua Password

Olá,

Recebemos um pedido para redefinir a tua password.

Clica no link abaixo para continuar:

http://127.0.0.1:8000/api/v1/password_reset/confirm/?token=abc123...

Se não foste tu, ignora este email.
```

---

## 🧪 Testes

### Teste 1: Fluxo Completo de Autenticação

```bash
# 1. Registrar
curl -X POST http://localhost:8000/api/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste123",
    "email": "teste@example.com",
    "password": "Teste123!",
    "password2": "Teste123!",
    "first_name": "Teste",
    "last_name": "User"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/v1/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste123",
    "password": "Teste123!"
  }'

# 3. Obter Perfil
curl -X GET http://localhost:8000/api/v1/perfil/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

### Teste 2: CORS

```javascript
// No browser (localhost:3000)
fetch("http://localhost:8000/api/v1/login/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  credentials: "include",
  body: JSON.stringify({
    username: "teste123",
    password: "Teste123!",
  }),
})
  .then((r) => r.json())
  .then(console.log);
```

---

## 🐛 Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'rest_framework'`

```bash
pip install -r requirements.txt
```

### Erro: `CORS errors` no frontend

Verifica se a origem está em `CORS_ALLOWED_ORIGINS` em `settings.py`

### Erro: Email não é enviado

1. Verifica `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD`
2. Ativa "Less secure apps" (Google)
3. Testa com: `python manage.py shell`

```python
from django.core.mail import send_mail
send_mail('Test', 'Body', 'from@example.com', ['to@example.com'])
```

---

## 📚 Dependências

```
Django==6.0.5
djangorestframework==3.17.1
djangorestframework_simplejwt==5.5.1
django-rest-passwordreset==1.5.0
django-cors-headers==4.9.0
drf-spectacular==0.29.0
PyJWT==2.12.1
```

---

## 🚀 Próximos Passos (Melhorias Futuras)

- [ ] Two-Factor Authentication (2FA)
- [ ] OAuth2 (Google, GitHub)
- [ ] Swagger UI automático
- [ ] Tests automatizados
- [ ] Deploy em produção (Heroku, Railway)
- [ ] Frontend React/Vue
- [ ] Documentação OpenAPI completa

---

## 📝 Licença

Este projecto é open-source e está disponível para uso pessoal e educacional.

---

## 👨‍💻 Autor

Benilson Kanza Benito

**Data:** 25 de Maio de 2026

---

---

**Última atualização:** 25/05/2026
