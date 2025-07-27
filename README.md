# Assistente pessoal inteligente
Inteligência artificial local que pode se personalizada com suas informações

## Execução do projeto
- Baixe a CLI do [Ollama](https://ollama.com/download)
- Baixe o modelo utilizado no projeto [llama 3.1](https://ollama.com/library/llama3.1) com `ollama run llama3.1`

Na IDE de sua preferência, execute os comandos:\
`python3 -m venv venv` *Pode ser necessário trocar o ambiente de execução na IDE\
`source venv/bin/activate` Comando específico para Linux\
`pip install -r requirements.txt`

Crie o arquivo `base_de_conhecimento.txt`

Execute o arquivo `main.py`

## Como personalizar o modelo?
- Crie a pasta `to-add` e adicione arquivos `pdf` (apenas). Execute o programa com a opção de adicionar documentos.\
*Remova os arquivos já adicionados dessa pasta para não ter conflitos.\
*Caso precise importar novamente um arquivo com o mesmo nome, exclua o nome do arquivo em `base_de_conhecimento.txt`

## Utilização
- Opção 1 para adicionar documentos
- Opção 2 para conversar com o Assistente
- Opção 3 para encerrar o programa\
*Na interação com o Assitente, digite "-exit" para finalizar a conversa

### Observações
Projeto testado com o processador i7 12 Gen, 32 GB RAM, AD107GLM RTX 1000 Ada Generation

### Referências
https://github.com/pdichone/ollama-fundamentals
