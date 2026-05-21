# Comparacao

| Criterio | Qdrant | Pinecone |
| --- | --- | --- |
| Modelo operacional | Local ou cloud | Cloud gerenciado |
| Melhor primeiro uso | Desenvolvimento local e controle fino | Prototipos cloud e operacao gerenciada |
| Setup local | Docker Compose | Nao aplicavel |
| Filtros por metadados | Sim | Sim |
| Custo inicial | Zero localmente | Depende do plano cloud |
| Risco principal | Operar infraestrutura propria em producao | Dependencia do provedor |

Use Qdrant primeiro quando o objetivo for aprender o pipeline completo localmente. Use Pinecone para comparar a experiencia com uma plataforma cloud gerenciada e entender os pontos de operacao que deixam de ser responsabilidade da aplicacao.
