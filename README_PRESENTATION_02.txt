
###################################################################### APRESENTAÇÃO TÉCNICA ######################################################################

Ferramentas utilizadas:
Python3
Apache Spark
Amazon ERM (Elastic Map Reduce) 5.28.0
Amazon S3 (Simple Storage Service)
Apache Zeppelin (Notebook para Testes)

Premissa: Base de dados armazenados no S3 e bibliotecas instaladas (pyspark e datetime).

Foi escrito um script em python com as bibliotecas necessárias para leitura de arquivos JSON diretamente do file sotrage experimentado, no caso o AWS S3.

Como exemplo, todos os arquivos foram lidos, carregados e registrados como DataFrames.

Ao final dessa leitura, foi criada uma etapa de escrita também no S3, onde o output de dados encontra-se no formato "orc" com compressão "snappy" e pode ser normalmente lido por uma tabela de um metastore Hive, por exemplo.

Os testes foram realizados utilizando o Apache Zeppelin.

Para inicializar os processos, salvar o dataset no S3 e, passar o nome do bucket como parâmtero.

Exemplo de disparo no EMR: 

spark-submit /<folder>/part_02.py bucket_name






###################################################################### APRESENTAÇÃO FUNCIONAL ######################################################################

À título apenas de demonstração, foi criada um métrica que apresenta as campanhas de marketing que mais foram impactantes no nosso público assinante.
Sabe-se que "marketing_campaign" não é uma campanha de marketing propriamente dita e sim um elemento da constituição do UTM. Entretanto, para fins didáticos, foi adotada com esse propósito.
