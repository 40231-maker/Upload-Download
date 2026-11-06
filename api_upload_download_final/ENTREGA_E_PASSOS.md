# Checklist de entrega — AD Deploy de API no Render

## Arquivos preparados

- [x] Código Flask organizado em controllers, models, routes e database.
- [x] Persistência dos metadados dos uploads no SQLite.
- [x] Validação de extensões, tamanho e nomes duplicados.
- [x] `requirements.txt`.
- [x] `README.md` com instalação, rotas, testes e deploy.
- [x] `render.yaml` com comandos de build e start.
- [x] `.gitignore` e `.python-version`.
- [x] Testes automatizados básicos.

## O que você ainda precisa executar na sua conta

- [ ] Instalar Python e Git, se ainda não estiverem instalados.
- [ ] Rodar `pip install -r requirements.txt`.
- [ ] Rodar `python -m unittest discover -s tests -v` e confirmar que os testes passam.
- [ ] Criar um repositório no GitHub e enviar o conteúdo desta pasta.
- [ ] Criar o Web Service no Render ligado ao repositório.
- [ ] Aguardar o deploy e abrir `https://SUA-API.onrender.com/health`.
- [ ] Testar upload e download na URL pública.
- [ ] Entregar a URL pública no Google Classroom.

## Configuração do Render

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Health Check Path: `/health`

## Teste público após deploy

1. Abra `https://SUA-API.onrender.com/health`. Esperado: `{"status":"ok"}`.
2. No Postman/Insomnia, faça `POST https://SUA-API.onrender.com/uploads/upload`.
3. Em Body, escolha `form-data`; crie uma chave `file`, altere o tipo para File e selecione um `.txt` de até 30 KB.
4. Esperado: HTTP `201` e JSON com o nome do arquivo.
5. Faça `GET https://SUA-API.onrender.com/downloads/download/NOME_DO_ARQUIVO`.
6. Confirme que o arquivo é baixado.

**Atenção:** o deploy real, a URL pública e os testes na infraestrutura do Render só podem ser confirmados depois que o serviço for criado na sua conta. Em instâncias com disco efêmero, os arquivos e o banco podem não persistir entre reinicializações/deploys.
