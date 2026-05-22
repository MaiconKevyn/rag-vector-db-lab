# Comparacao

| Criterio | Qdrant | Pinecone |
| --- | --- | --- |
| Modelo de deploy | Local, self-hosted ou cloud | Cloud gerenciado |
| Open source | Sim, core OSS | Nao, plataforma proprietaria |
| Primeiro uso ideal | Desenvolvimento local e controle fino | Prototipos cloud e operacao gerenciada |
| Setup local | Docker Compose | Nao aplicavel |
| Filtros por metadados | Sim, payload filters | Sim, metadata filters |
| Hybrid search | Suportado por recursos de sparse/dense vectors | Suportado por recursos gerenciados da plataforma |
| Escala operacional | Depende da operacao do cluster | Gerenciada pelo provedor |
| SQL e joins | Nao e banco relacional | Nao e banco relacional |
| Esforco operacional | Medio em self-hosted, baixo em cloud | Baixo para o usuario da plataforma |
| Custo inicial | Zero localmente | Depende do plano cloud |
| Melhor fit | Times que querem controle, local-first e portabilidade | Times que querem gerenciado, velocidade cloud e menos operacao |
| Risco principal | Operar infraestrutura propria em producao | Dependencia do provedor |

Use Qdrant primeiro quando o objetivo for aprender o pipeline completo localmente. Use Pinecone para comparar a experiencia com uma plataforma cloud gerenciada e entender os pontos de operacao que deixam de ser responsabilidade da aplicacao.
