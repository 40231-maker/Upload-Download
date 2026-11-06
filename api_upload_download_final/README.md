# API de Upload e Download

API REST em Python com Flask para receber arquivos e disponibilizar seu download. O projeto utiliza SQLite para registrar os arquivos enviados.

## Funcionalidades

- Upload de arquivos por `multipart/form-data`.
- Download de arquivos enviados.
- Registro de nome e caminho do arquivo em banco SQLite.
- Validação de extensão, tamanho e nomes duplicados.
- Respostas em JSON e códigos HTTP adequados.
- Rota de saúde (`/health`) para monitoramento no Render.

## Tecnologias

Python 3.12, Flask, SQLite e Gunicorn.

## Executar localmente

É necessário ter Python 3.10 ou superior instalado.

1. Clone o repositório:
   ```bash
   git clone URL_DO_REPOSITORIO
   cd NOME_DA_PASTA
   ```
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
3. Ative o ambiente virtual:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Inicie a API:
   ```bash
   python app.py
   ```
6. Acesse `http://127.0.0.1:5000/` ou `http://127.0.0.1:5000/health`.

## Rotas da API

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Apresenta informações e rotas disponíveis |
| GET | `/health` | Informa se a API está ativa |
| POST | `/uploads/upload` | Recebe um arquivo |
| GET | `/downloads/download/<filename>` | Faz o download de um arquivo registrado |

### Fazer upload

Envie `POST /uploads/upload` como `multipart/form-data`, usando o campo chamado `file`.

Exemplo com cURL:

```bash
curl -X POST http://127.0.0.1:5000/uploads/upload -F "file=@exemplo.pdf"
```

Extensões permitidas: `png`, `jpg`, `jpeg`, `gif`, `pdf` e `txt`. O limite é de 30 KB por arquivo. A API não substitui arquivos com o mesmo nome.

### Fazer download

Depois de enviar um arquivo, utilize o nome retornado pela API:

```text
GET http://127.0.0.1:5000/downloads/download/NOME_DO_ARQUIVO
```

## Códigos HTTP principais

- `200`: consulta ou verificação de saúde concluída.
- `201`: upload realizado.
- `400`: arquivo ausente, nome vazio ou extensão não permitida.
- `404`: arquivo não encontrado.
- `409`: já existe arquivo com o mesmo nome.
- `413`: arquivo ou requisição acima do limite.
- `500`: erro interno ao salvar o arquivo.

## Testes automatizados

Com as dependências instaladas, execute na raiz do projeto:

```bash
python -m unittest discover -s tests -v
```

## Publicar no GitHub

1. Crie um repositório no GitHub.
2. Abra o terminal na pasta do projeto.
3. Execute:
   ```bash
   git init
   git add .
   git commit -m "Preparar API para deploy"
   git branch -M main
   git remote add origin URL_DO_REPOSITORIO
   git push -u origin main
   ```
   Substitua `URL_DO_REPOSITORIO` pela URL HTTPS do repositório que você criou.

## Deploy no Render

O arquivo `render.yaml` já descreve as configurações iniciais. Para configurar manualmente:

1. Entre no Render e escolha **New + > Web Service**.
2. Conecte o GitHub e selecione o repositório.
3. Selecione o ambiente Python.
4. Informe **Build Command**: `pip install -r requirements.txt`.
5. Informe **Start Command**: `gunicorn app:app`.
6. Configure **Health Check Path** como `/health`, se o campo estiver disponível.
7. Crie o Web Service e aguarde o término do deploy.
8. Abra a URL pública fornecida pelo Render e teste `/health`.

## Observação sobre armazenamento em produção

O projeto salva os arquivos enviados e o banco SQLite no sistema de arquivos local. Em hospedagens com sistema de arquivos efêmero, esses dados podem ser apagados em reinicializações ou novos deploys. Para manter os uploads permanentemente, configure um disco persistente no serviço de hospedagem e defina `UPLOAD_FOLDER` e `DATABASE_PATH` para caminhos dentro desse disco, ou utilize armazenamento externo. A disponibilidade e o custo do disco persistente dependem do plano atual do provedor.

## Estrutura de pastas

```text
.
├── app.py
├── controllers/
├── database/
├── models/
├── routes/
├── tests/
├── requirements.txt
├── render.yaml
└── README.md
```
