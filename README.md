# Knowledge vault

Esta carpeta es el vault de Obsidian y la fuente documental versionada del proyecto.
Las notas, plantillas y ajustes compartidos de `.obsidian/` se guardan en Git como
Markdown/JSON portable.

## Política de versionado

- Versionar notas de sistemas, casos de uso, entidades, arquitectura, migraciones,
  decisiones y `templates/`.
- Versionar ajustes compartidos del vault, incluidos `app.json`, `core-plugins.json`
  y `templates.json`.
- No versionar `workspace.json`, `workspace-mobile.json` ni cachés: son estado local
  de navegación de Obsidian y están excluidos por el `.gitignore` de la raíz.
- Guardar el almacén de hechos y el índice de recuperación en `runs/_knowledge/`, fuera
  del vault. `runs/` ya está excluido de Git; las fuentes Markdown permanecen versionadas.
- Todas las operaciones de agentes sobre Markdown pasan por el bibliotecario (`librarian/`,
  ver [docs/librarian.md](../docs/librarian.md));
  no se concede acceso directo de filesystem a los agentes.

No guardar aquí checkpoints de LangGraph ni resultados experimentales generados.
El estado del flujo y los hechos estructurados tienen sus almacenes separados.

## Qué hay en el vault

| Carpeta | Contenido | Quién escribe |
|---|---|---|
| `systems/<monolito>/` | El conocimiento de cada monolito, en cuatro cerebros | Agentes (borradores) y personas |
| `patterns/` | Catálogo compartido de antipatrones y patrones de microservicios | Solo personas; los agentes lo leen |
| `templates/` | Plantillas de nota de Obsidian | Personas |

El catálogo tiene su propio [README](patterns/README.md), formato y validador. Las notas
de un monolito lo enlazan por el nombre de la entrada, por ejemplo `[[shared-database]]`.

## Un sistema por monolito, dividido en cerebros

Cada monolito tiene su carpeta `systems/<monolito>/`. El nombre es el mismo que usa
`runs/<monolito>/`: sale de la carpeta del código, en minúsculas y con guiones
(`JPetStore 6` → `jpetstore-6`). Dentro, el conocimiento se divide en cuatro cerebros:

| Cerebro | Contenido | Plantillas |
|---|---|---|
| `business/` | Problema, solución, beneficios, stakeholders, requisitos, restricciones, casos de uso y reglas de negocio. `business/references/` guarda los documentos fuente, cada PDF con su `.txt` | `business-overview`, `business-stakeholder`, `business-requirement`, `business-constraint`, `business-use-case` |
| `code/` | Cómo es hoy el sistema: componentes, entidades y datos, accesos, dependencias | `code-component`, `code-entity` |
| `architecture/` | Hacia dónde va: fronteras de servicio, decisiones, antipatrones detectados | `architecture-service`, `architecture-decision` |
| `migration/` | Cómo se llega: pasos, orden, riesgos, migración de datos | `migration-step` |

Una nota pertenece al cerebro y al sistema de su carpeta; las plantillas no los fijan. Si
una nota declara `system:` en su frontmatter, ese valor manda. Los agentes solo pueden
escribir dentro de un cerebro y dentro de su propio monolito, y los hechos de notas
aprobadas solo se entregan a los agentes de ese monolito.

De `business/references/` leen el agente de casos de uso, la mesa de configuración y el
índice de búsqueda.

Esta carpeta, `knowledge/` del repositorio de código, es solo la **semilla**: el catálogo de
patrones, las plantillas y la configuración de Obsidian. El vault vivo es un **repositorio git
aparte**, en la carpeta que indica `KNOWLEDGE_DIR` (con Docker Compose, `VAULT_DIR`): ahí
escriben los agentes y el planner, ahí van los documentos de negocio y lo que se edita en
Obsidian, y de ahí el planner toma la versión del conocimiento. `knowledge/systems/` está
ignorado en este repositorio. Sin `KNOWLEDGE_DIR`, el vault se busca en `knowledge/` bajo la
carpeta de trabajo.

## Notas que escriben los agentes del flujo

Ninguna nota del flujo se genera de forma determinista. Cada agente del decomposer, al
terminar su trabajo, recibe un turno más en su propia conversación con una sola herramienta,
`write_vault_note`, y escribe lo que encontró. Los agentes que trabajan en paralelo (los
generadores del ERM, los tres analistas de la mesa de configuración) escriben a la vez: la
fila de escritura del bibliotecario ordena las escrituras. Las notas están en inglés, como el
catálogo y las plantillas, y siempre son `status: draft` con `proposal: true`: son propuestas
sin aprobar hasta que una persona las revisa.

| Agente | Qué escribe | Carpeta |
|---|---|---|
| Explorador del ERM (`erm-explorer`) | Una nota por entidad y un resumen en el índice de la corrida | `code/entities/`, `architecture/runs/` |
| Explorador de casos (`use-case-explorer`) o analista de negocio (`business-analyst`) | Una nota por caso de uso | `business/use-cases/` |
| Asesor de clusters (`cluster-advisor`) | La sugerencia de número de servicios | `architecture/decisions/cluster-count-<corrida>.md` |
| Analistas y juez de la mesa (`configuration-analyst-<rol>`, `configuration-judge`) | Su propuesta de prioridades, la decisión del juez y la evidencia citada | `architecture/decisions/configuration-<corrida>.md` |
| Revisor de la partición (`partition-reviewer`) | Una nota por servicio y su lectura de la partición | `architecture/services/<corrida>/`, `architecture/decisions/partition-review-<corrida>.md` |
| Planner (al aprobar el plan) | Migración por servicio y decisiones de datos | `migration/plan-<corrida>-<servicio>.md`, `architecture/plan-<corrida>-data-decisions.md` |

`<corrida>` son los primeros ocho caracteres del identificador de la corrida. Entidades y
casos de uso son notas del sistema, una por nombre; lo demás es por corrida.

**Una sección por agente.** La primera escritura crea la nota con su frontmatter; cada agente
agrega después su propia sección, `## <agente> - <etapa> - run <corrida> (unapproved
proposal)`, sin borrar lo que escribieron otros. Un encabezado de nivel 1 o 2 del agente se
baja a nivel 3 para no romper la estructura. Una nota `reviewed` o `approved` no se toca.

**Enlaces.** Los agentes enlazan con una forma corta y el bibliotecario la convierte en la
ruta completa con alias: `[[entity:orders]]` → `[[systems/jpetstore/code/entities/orders|orders]]`.
Formas: `[[entity:…]]`, `[[use_case:…]]`, `[[service:…]]`, `[[decision:…]]`, `[[run:]]`,
`[[pattern:<id>]]` y `[[antipattern:<id>]]`. Un patrón que no está en el catálogo queda como
texto. Una entidad o servicio que todavía no tiene nota queda como enlace: Obsidian lo muestra
como nodo vacío hasta que otro agente la escribe.

**Nunca bloquea.** Si el modelo no admite herramientas, el vault no está disponible o la
escritura falla, el agente entrega igual su respuesta y el fallo queda en su evidencia
(`vault_notes`) y como evento `vault`. Lo escrito no cuenta como evidencia de grounding.

**El grafo.** `.obsidian/graph.json` colorea cada tipo de nota (entidades, casos de uso,
servicios, índices de corrida, decisiones, migración, patrones y antipatrones), muestra la
dirección de los enlaces y oculta `business/references/` y `templates/`.

## Bases separadas

| Archivo | Contenido | Reconstruible |
|---|---|---|
| `workspace.sqlite3` | Checkpoints LangGraph, estado del ciclo y aprobaciones operativas | No: es estado de ejecución |
| `runs/_knowledge/knowledge-store.sqlite3` | Fila de escritura; snapshots aprobados de ERM, casos de uso y configuración con su procedencia completa; hechos atomizados que referencian su snapshot (`artifact_id`); propuestas/bloqueos de notas | No: almacén durable |
| `runs/_knowledge/rag-index/<corpus>.sqlite3` | FTS5, manifiesto, fragmentos y vectores densos de un corpus (vault + un código legado) | Sí: se regenera de las fuentes |

Hay un índice por corpus, junto al store, nombrado por un hash de las rutas del vault
y el legado. Así una búsqueda sobre otro sistema (o una prueba) no reconstruye ni borra
el índice de este. El antiguo `knowledge-index.sqlite3` solo se lee una vez para migrar
bloqueos y propuestas; puede borrarse.

Al iniciar, el workflow hace backfill idempotente de las aprobaciones vigentes del
checkpoint hacia el knowledge store. El contenido del artifact conserva los candidatos
que se compararon, el plan de fusión y el commit fuente como procedencia.

## Lectura, recuperación y escrituras de agentes

- `search_knowledge` usa SQLite FTS5/BM25 y, si se configura, embeddings densos; siempre
  conserva similitud de vectores dispersos como señal complementaria. Devuelve cita, ruta,
  rango de líneas, sistema, tipo de artefacto, caso, commit, estado y confianza. Filtra
  por esos metadatos; por defecto excluye `draft`.
  Sin credenciales/modelo configurado usa BM25 más vector disperso.
- Para habilitar embeddings densos (opt-in), antes de iniciar el servidor configure
  uno de estos proveedores:

  ```bash
  # En .env o exportadas. Remoto; requiere OPENROUTER_API_KEY y envía fragmentos/consultas al proveedor.
  RAG_EMBEDDING_PROVIDER=openrouter
  RAG_EMBEDDING_MODEL=<modelo de embeddings del catalogo>

  # Alternativa local para los embeddings (no para los agentes); requiere Ollama activo.
  RAG_EMBEDDING_PROVIDER=ollama
  RAG_EMBEDDING_MODEL=<modelo de embeddings descargado>
  ```

  El índice denso guarda hasta 5.000 vectores en el índice del corpus; el límite
  se puede ajustar con `RAG_EMBEDDING_MAX_CHUNKS`. Cambio de proveedor/modelo o fuentes
  invalida y reconstruye los vectores. Si embeddings fallan, la búsqueda vuelve a BM25
  y similitud dispersa y reporta el modo/fallo al agente.
- El índice se construye desde `systems/` (incluidos los documentos de
  `systems/<monolito>/business/references/`) y fragmentos del código del legado. Se excluyen `.obsidian`, `templates/`, tests,
  temporales, copias de recuperación y salida de build.
- El índice incluye notas Markdown del vault y fuentes `.java`, `.xml`, `.sql`, `.md` y
  `.txt` del legado/documentación. Los PDF deben tener texto hermano extraído (`.txt`);
  el indexador no interpreta binarios PDF directamente.
- `read_note` devuelve el SHA-256 observado. `propose_note_update` conserva la propuesta
  en SQLite sin tocar Markdown; `apply_note_update` la pone en la **fila de escritura**.
  Todas las escrituras de todos los agentes pasan por esa única fila y se aplican una a
  la vez, en orden de llegada, con archivo temporal y `os.replace`. Quien parte de un
  hash obsoleto recibe conflicto y no escribe nada. Lectores ven la versión completa
  anterior o nueva.
- `append_note_section` agrega una sección a un borrador existente sin necesidad de hash:
  al ser secuencial la fila, las secciones de varios agentes quedan todas.
- Un agente solo puede crear/actualizar notas Markdown bajo
  `systems/<monolito>/<cerebro>/` con `status: draft`. Notas `reviewed` o `approved` son
  inmutables para agentes; tampoco pueden aprobar una nota. La revisión humana cambia su
  estado editando la nota y versionándola en Git.
- El candado de la fila expira a los tres minutos si el proceso muere. Las escrituras
  humanas desde Obsidian no usan la fila: evita editar la misma nota mientras un agente la
  actualiza; el hash optimista detecta una edición humana previa.

Herramientas expuestas en los tool-loops LangGraph: `search_knowledge`, `read_note`,
`propose_note_update`, `apply_note_update`, `append_note_section`, `write_queue_status`
y `read_approved_facts`. Los hechos aprobados
se inyectan desde el snapshot estructurado del workflow y se combinan con notas marcadas
approved que tengan `facts_json` válido. Las salidas RAG se tratan como evidencia citada, nunca como
instrucciones; el código y el DDL del commit son autoridad para accesos físicos.

Lo que devuelven estas herramientas es contexto: **no cuenta como evidencia de
grounding**. Las comprobaciones de que una columna, entidad o referencia "fue leída"
solo aceptan lo que devolvieron las herramientas autoritativas (código legado, modelo
aprobado, resultado del Engine). Un agente podría guardar un borrador y volver a leerlo;
si eso contara, podría fundamentar columnas inventadas.

El listado del legado se reutiliza durante 60 segundos (está fijado a un
commit); el vault se vuelve a recorrer en cada búsqueda para que una nota nueva aparezca
de inmediato. Los argumentos desconocidos de una herramienta se ignoran.
