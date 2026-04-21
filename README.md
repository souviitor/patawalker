# 🐾 PataWalker — Sistema de Dog Walker

Sistema web multiplataforma (Web, iOS, Android) para gerenciamento de serviços de dog walker.

## 🚀 Tecnologias

- **Backend:** Python + Flask
- **Banco de Dados:** PostgreSQL
- **Autenticação:** Flask-Login
- **Pagamentos:** Mercado Pago
- **Frontend:** HTML5 + CSS3 + JavaScript (responsivo, PWA-ready)
- **Deploy:** Docker + Docker Compose

---

## 📁 Estrutura do Projeto

```
dogwalker/
├── app.py                  # Aplicação Flask principal
├── config.py               # Configurações
├── init_db.py              # Script de inicialização do banco
├── requirements.txt        # Dependências Python
├── Dockerfile
├── docker-compose.yml
├── models/
│   └── models.py           # Modelos do banco de dados
├── routes/
│   ├── auth.py             # Login, cadastro, logout
│   ├── user.py             # Área do tutor
│   ├── admin.py            # Painel administrativo
│   ├── services.py         # Agendamentos e serviços
│   └── main.py             # Rota raiz
├── templates/
│   ├── base.html           # Template base (menu lateral, header)
│   ├── auth/               # Login e cadastro
│   ├── user/               # Área do usuário
│   ├── admin/              # Painel admin
│   └── services/           # Telas de serviços
└── static/
    ├── css/                # Estilos adicionais
    ├── js/                 # Scripts adicionais
    ├── img/                # Imagens e logo
    ├── audio/              # Música ambiente (ambient.mp3)
    └── uploads/            # Fotos de pets e vacinas
```

---

## ⚙️ Instalação

### Opção 1 — Docker (Recomendado)

```bash
# Clone e entre na pasta
cd dogwalker

# Copie o .env
cp .env.example .env
# Edite .env com suas chaves do Mercado Pago

# Suba os containers
docker-compose up -d

# Inicialize o banco
docker-compose exec web python init_db.py
```

Acesse: http://localhost:5000

### Opção 2 — Manual

```bash
# 1. Instale dependências
pip install -r requirements.txt

# 2. Configure PostgreSQL
# Crie o banco: dogwalker_db
# Usuário: dogwalker_user / Senha: dogwalker_pass

# 3. Configure variáveis de ambiente
export DATABASE_URL="postgresql://dogwalker_user:dogwalker_pass@localhost:5432/dogwalker_db"
export SECRET_KEY="sua-chave-secreta-aqui"
export MP_ACCESS_TOKEN="seu-token-mercadopago"
export MP_PUBLIC_KEY="sua-public-key-mercadopago"

# 4. Inicialize o banco
python init_db.py

# 5. Inicie o servidor
python app.py
```

---

## 🔐 Acesso Inicial

| Tipo | Email | Senha |
|------|-------|-------|
| Admin | admin@patawalker.com.br | admin123 |

> ⚠️ **IMPORTANTE:** Troque a senha do admin imediatamente após o primeiro login!

---

## 💳 Mercado Pago

1. Acesse https://www.mercadopago.com.br/developers
2. Crie um app e obtenha suas credenciais
3. Configure no `.env`:
   ```
   MP_ACCESS_TOKEN=APP_USR-...
   MP_PUBLIC_KEY=APP_USR-...
   ```

---

## 🎵 Música Ambiente

Coloque um arquivo `ambient.mp3` na pasta `static/audio/`.
O player aparece no header para usuários (não admin) com opção de mute.

---

## 📱 Responsividade

- **Desktop:** Menu lateral fixo com todas as opções
- **Mobile/Tablet:** Menu hamburger deslizante (PWA-ready)
- **Dark Mode:** Toggle no header, salvo em localStorage

---

## 🗄️ Banco de Dados — Modelos Principais

| Tabela | Descrição |
|--------|-----------|
| `users` | Tutores e administradores |
| `pets` | Informações dos pets |
| `service_plans` | Planos P, M e G configurados pelo admin |
| `walk_durations` | Durações de passeio avulso com preços |
| `service_orders` | Pedidos de serviço e agendamentos |
| `financial_records` | Controle financeiro (entradas/saídas) |
| `app_settings` | Configurações gerais do sistema |

---

## 📊 Funcionalidades Admin

- Dashboard com KPIs em tempo real
- Relatórios filtrável por período
- **Exportação para Excel** (cadastros + pedidos)
- Configuração de planos P, M, G (preço, duração, descrição)
- Configuração de durações de passeio avulso
- Controle financeiro (entradas, saídas, reembolsos)
- Gestão de usuários

## 🐕 Funcionalidades Tutor

- Cadastro simples com foto do pet
- Dashboard com carrossel de serviços + música ambiente
- Foto do pet como marca d'água no fundo
- Agendamento de planos semanais (P/M/G com dias e horário)
- Agendamento de passeios avulsos com calendário
- Cancelamento com reembolso automático (>24h)
- Acompanhamento ao veterinário
- Compras de ração/medicamentos
- Histórico completo de passeios
- Dark/Light mode

---

## 🔄 Política de Reembolso

Cancelamentos com **mais de 24 horas de antecedência** geram reembolso automático via Mercado Pago. Cancelamentos tardios não são reembolsados.

---

## 🚀 Deploy em Produção

Recomendamos:
- **Servidor:** VPS com Ubuntu 22.04
- **Web Server:** Nginx como proxy reverso
- **Process Manager:** Gunicorn
- **SSL:** Let's Encrypt (Certbot)

```bash
# Instale gunicorn
pip install gunicorn

# Execute
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

---

Desenvolvido com ❤️ para o PataWalker 🐾
