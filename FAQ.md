# ❓ Frequently Asked Questions

## Instalação

**P: Preciso de Python 3.11?**
R: Sim, a aplicação requer Python 3.11 ou superior. Versões anteriores não são suportadas.

**P: Como instalar em Windows?**
R: Abra Command Prompt ou PowerShell e siga os passos em QUICKSTART.md

**P: Posso usar um ambiente Conda?**
R: Sim, crie um ambiente `conda create -n tools4me python=3.11` e ative antes de instalar requirements.

**P: Qual é o tamanho das dependências?**
R: Aproximadamente 200-300 MB após instalação completa.

## Uso

**P: Qual o formato de entrada aceito?**
R: CSV ou Excel (.xlsx, .xls). Ambos funcionam igualmente bem.

**P: A coluna "nome" é obrigatória?**
R: Sim, é a única coluna obrigatória. Outras são opcionais.

**P: Posso processar múltiplas planilhas?**
R: Atualmente uma por vez. Você pode processar sequencialmente salvando entre elas.

**P: Quanto tempo leva para processar 1000 contatos?**
R: Aproximadamente 8-15 horas dependendo da velocidade da internet e configuração.

**P: A aplicação funciona offline?**
R: Não, precisa de internet para buscar dados do LinkedIn.

**P: Posso interromper o processamento?**
R: Sim, clique "⏹ Parar" e ele parará no próximo contato.

**P: Os dados originais são modificados?**
R: Não, um novo arquivo é criado com os dados enriquecidos.

## Cache

**P: O que é o cache?**
R: Armazena resultados de buscas anteriores para evitar repetir buscas.

**P: Onde fica o cache?**
R: Em `data/search_cache.json`

**P: Quanto espaço o cache ocupa?**
R: Tipicamente 5-50 MB dependendo do número de buscas.

**P: Posso limpar o cache manualmente?**
R: Sim, clique "🗑 Limpar Cache" na interface ou delete `data/search_cache.json`.

**P: O cache expira?**
R: Atualmente não, mas você pode limpar manualmente conforme necessário.

**P: Posso compartilhar o cache entre computadores?**
R: Sim, copie `data/search_cache.json` entre máquinas para reutilizar resultados.

## Qualidade de Dados

**P: Qual o score mínimo aceitável?**
R: 0.5 é o padrão, mas recomenda-se revisar scores abaixo de 0.7.

**P: Por que alguns contatos não foram encontrados?**
R: Podem estar com nome muito diferente, empresa desconhecida ou perfil privado.

**P: Como melhorar a taxa de sucesso?**
R: 
- Verifique a grafia do nome (acentuação)
- Adicione empresa quando possível
- Aumente o timeout se tiver internet lenta

**P: Posso confiar em scores baixos (0.5-0.6)?**
R: Não recomendado. Revise manualmente antes de usar.

**P: O que significa "duvidoso"?**
R: Score entre 0.5-0.7, indica incerteza. Revise antes de usar.

## Performance

**P: Como aumentar a velocidade?**
R: Aumente `max_threads` e reduza `delay_min`/`delay_max` em config/settings.py

**P: Qual é o máximo de threads recomendado?**
R: 5-10 é seguro. Mais que isso pode causar bloqueios.

**P: Por que está lento?**
R: Pode ser internet, configurações conservadoras, ou LinkedIn bloqueando.

**P: Posso processar em paralelo em múltiplos computadores?**
R: Não nativamente, mas pode-se dividir o arquivo e processar em cada um.

**P: Qual a melhor hora para processar?**
R: Noites/madrugadas quando há menos tráfego de internet.

## Erros Comuns

**P: "No module named 'customtkinter'"**
R: Execute `pip install customtkinter`

**P: "Invalid file format"**
R: Verifique se é CSV ou Excel válido. Tente reconverter.

**P: "Connection timeout"**
R: Aumente o timeout em config/settings.py ou verifique sua internet.

**P: "LinkedIn profile not found"**
R: Normal, nem todo perfil está público ou indexado.

**P: "Permission denied" ao salvar**
R: Verifique permissões da pasta. Tente salvar em outra local.

## Deployment

**P: Posso fazer deploy no Render?**
R: Sim, siga guia em DEPLOYMENT.md

**P: Qual plano do Render preciso?**
R: Free funciona mas é lento. Pro (7$/mês) é recomendado.

**P: Posso fazer deploy no meu servidor?**
R: Sim, use Docker ou siga guia de Systemd.

**P: Preciso de banco de dados?**
R: Não, tudo é arquivo local.

**P: Posso criar uma versão web?**
R: Sim, pode usar Streamlit ou FastAPI (veja ADVANCED_GUIDE.md).

## Dados Pessoais

**P: A aplicação armazena dados em nuvem?**
R: Não, tudo fica local na máquina.

**P: Posso usar com dados de clientes?**
R: Sim, mas certifique-se de ter consentimento e cumprir LGPD/GDPR.

**P: Os dados são criptografados?**
R: Não, mas você pode criptografar o arquivo de saída.

**P: Posso deletar dados após exportar?**
R: Sim, delete o arquivo de entrada após salvar o resultado.

## Funcionalidades

**P: Posso buscar por email também?**
R: Não nesta versão, mas está em roadmap.

**P: Posso validar números de telefone?**
R: Não, escopo atual é LinkedIn apenas.

**P: Posso integrar com CRM?**
R: Não nativamente, mas pode exportar CSV e importar manualmente.

**P: Posso adicionar novos campos de busca?**
R: Sim, edite `search_service.py` conforme documentado em ADVANCED_GUIDE.md

**P: Posso usar API oficial do LinkedIn?**
R: Não está implementado, mas é possível conforme ADVANCED_GUIDE.md

## Suporte

**P: Como reportar um bug?**
R: Abra uma issue no GitHub com logs de `logs/app.log`

**P: Como sugerir uma feature?**
R: Abra uma discussion ou issue no GitHub.

**P: Há comunidade de usuários?**
R: Ainda não, mas usuários podem se conectar via GitHub Discussions.

**P: A aplicação é open source?**
R: Sim, respeitando licença do projeto.

**P: Posso clonar e modificar?**
R: Sim, conforme termos da licença.

## Segurança

**P: A aplicação é segura?**
R: Sim, não armazena senhas e usa padrões de segurança.

**P: Posso usar com dados confidenciais?**
R: Sim, dados ficam locais. Recomenda-se usar em rede privada.

**P: Há risco de bloqueio por LinkedIn?**
R: Sim, se usar com muita agressividade. Mantenha delays adequados.

**P: Como evitar bloqueios?**
R: Não aumente excessivamente threads/reducir delays, processe em off-peak hours.

## Licença

**P: Qual é a licença?**
R: Proprietary com uso permitido sob certos termos.

**P: Posso comercializar?**
R: Consulte termos da licença ou proprietário.

**P: Posso distribuir modificações?**
R: Depende da licença específica do projeto.

---

**Não encontrou sua pergunta?** 
Abra uma issue no GitHub ou consulte README.md e ARCHITECTURE.md.
