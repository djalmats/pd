
###################################################################### APRESENTAÇÃO TÉCNICA ######################################################################

Ferramentas utilizadas:

Pentaho 8.3 (ETL tool da Hitachi)
SGBD PostgreSQL 12.0
Docker 2.2.0.0

Premissa: Base de dados armazenados localmente.

A ideia foi utiliar ferramentas simples e open-sources para produzir de maneira rápida a estrutura de carga e focar no modelo de dados.

Através de simples conectores, o Pentaho fez a leitura dos arquivos json e escreveu nas tabelas do PostgreSQL. Os demais jobs envolvidos foram considerando os sources e targets do mesmo banco.

O banco de dados foi o único "dockerizado" dessa solução. Foi criado um modelo simples, sem a presença de muitos objetos de banco como sequências ou "restrições" de integridade referencial. Isso quer dizer que a garantia ACID foi outorgada aos processos, o que garante uma maior velocidade às cargas em caso de alta volumetria.

Para inicializar os processos, seguir os passos abaixo:

STEP 01:

Para subir a instancia do PostgreSQL, basta baixar o Docker e na pasta onde salvou o arquivo "docker-compose.yml" (disponível no repositório do Github) digitar o comando "docker-compose up".

STEP 02:

Executar o Pentaho e criar duas variáveis no arquivo de propriedades do Kettle, que fica em Edit -> Edit the kettle.properties file:

ETL_FILE_JSON_PATH_A = /Users/<usuario>/Desktop/PD/datasets/base_a
ETL_ROOT_PATH = /Users/<usuario>/Desktop/PD/etl/

No job principal (main_job.kjb) executar o job através da seta "Run Options".

O SQL Command "create_objects" só precisa ser executado apenas uma única vez, pois ele serve para criar as estruturas do modelo físico. Após a execução inicial, favor desabilitar a hop.






###################################################################### APRESENTAÇÃO FUNCIONAL ######################################################################

No intuito de analisar aspectos sobre o usuário e suas atividades na plataforma da PD, foi construído um modelo multidimensional "Star Schema" para apresentar algumas métricas relativas.

Foi criada uma camada de extração dos arquivos e carga em tabelas físicas e outras duas, uma voltada à carga nas quatro tabelas dimensões e outra nas duas tabelas fatos.

Não inseri nesse contexto a dimensão de tempo, mesmo sendo primordial, por considerar que com essa amostra, a ideia principal era obter insigths mais significativos e não evolutivos. Também tomei algumas decisões mais limpas, como por exemplo não criar um processo de "slow change dimension" para o catálogo de usuários, assim como preferi manter o modelo sem nenhuma dimensão snowflake.

Sendo assim, a estratégia apresentada no projeto é de carga full, podendo ser facilmente readaptada para o modo incremental baseado em datas, uma vez que esse ponto fosse definido com mais critério.

Houve algumas inferências quanto aos dados apenas como aplicação didática, como por exemplo a regra artificial que criei estipulando que o tempo de uma sessão dura até o início da outra aberta pelo mesmo usuário, considerando a plataforma e, caso não haja uma próxima sessão, a finalização se dá no término do dia corrente.

Apliquei algumas regras também de limpeza de dados, principalmente nos domínios universidade, curso e disciplina que apresentavam bastante duplicidades e registros inconsistentes.

Abaixo, um breve dicionário de dados explicando as métricas produzidas:

Fact User Information (dw.ft_user_info)

platform_id - Código da Plataforma
state_id - Código do Estado (UF)
university_id - Código da Universidade
course_id - Código do Curso
n_students_total - Número Total de Estudantes
n_students_subscribers - Número de Estudantes Assinantes
n_students_subscribers_monthly - Número de Estudantes Assinantes com Plano Mensal
n_students_subscribers_yearly - Número de Estudantes Assinantes com Plano Anual
n_days_to_premium_conversion - Tempo (em dias) de conversão considerando o perído decorrido entra o cadastro na plataforma e data de quando a categoria premium foi assinada.

Fact User Activity (dw.ft_user_activity)

platform_id - Código da Plataforma
state_id - Código do Estado (UF)
n_session_time - Tempo médio de audiência no site
n_session_time_subscribers - Tempo médio de audiência no site considerando apenas assinantes
