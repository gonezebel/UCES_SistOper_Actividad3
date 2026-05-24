# Propuesta de paginas nuevas - Actividad 4 Parte 2

Fuente analizada: `01_Consigna/actividad obligatoria nro. 3 - parte 2.pdf`

## Criterio general

La Parte 2 pide una presentacion altamente visual sobre gestion de alta demanda y concurrencia. Para cumplir la consigna sin modificar las paginas existentes, conviene sumar un bloque nuevo de navegacion despues de la seccion actual de Round Robin y antes de la conclusion, o bien como grupo separado "Actividad 4 / Parte 2".

Las paginas actuales ya cubren seleccion del sistema, aislamiento, paginacion, MMU y Round Robin en un contexto de aula. Las paginas nuevas deberian profundizar en:

- swapping y memoria virtual en renderizado 3D;
- fallos de pagina y reemplazo de paginas;
- algoritmos FIFO, LRU y Clock;
- Round Robin aplicado al servidor de examenes;
- sincronizacion con semaforos y prevencion de condiciones de carrera.

## Pagina nueva 1: Parte 2 / Contexto de alta demanda

Objetivo: presentar el escenario de la academia en semana de entregas finales.

Contenido sugerido:

- Terminales ejecutando renders 3D pesados.
- Examenes online interactivos comunicandose con el servidor central.
- Riesgo doble: saturacion de RAM en las terminales y concurrencia en el servidor.

Visual sugerido:

- Diagrama de dos zonas: "Terminales de alumnos" y "Servidor central".
- Flechas simultaneas desde muchas terminales hacia el servidor.
- Indicadores de presion: RAM alta, cola de peticiones, archivo de calificaciones compartido.

Interaccion sugerida:

- Slider "cantidad de alumnos".
- Slider "peso del render".
- Indicador que muestre cuando la RAM fisica se agota y empieza la memoria virtual.

## Pagina nueva 2: Memoria virtual y swapping

Objetivo: explicar como el sistema operativo evita el colapso cuando la RAM fisica no alcanza.

Contenido sugerido:

- Swapping como traslado temporal de paginas entre RAM y disco.
- La memoria virtual simula mas memoria disponible que la RAM fisica real.
- El beneficio es continuidad de ejecucion; el costo es menor rendimiento por acceso a disco.

Visual sugerido:

- Mapa con tres bloques: proceso de render, RAM fisica y area de swap en disco.
- Animacion paso a paso:
  1. El render solicita mas memoria.
  2. La RAM se llena.
  3. El SO mueve paginas poco necesarias al disco.
  4. La pagina requerida entra en RAM.

Interaccion sugerida:

- Control para variar RAM fisica disponible.
- Control para variar paginas demandadas por el render.
- Medidor "rendimiento esperado" que baje cuando crece el uso de swap.

## Pagina nueva 3: Fallos de pagina y reemplazo

Objetivo: mostrar que ocurre cuando una pagina requerida no esta en memoria fisica.

Contenido sugerido:

- Definicion de fallo de pagina.
- Necesidad de elegir una victima cuando no hay marcos libres.
- Relacion entre politica de reemplazo y rendimiento.

Visual sugerido:

- Tabla de marcos de memoria.
- Secuencia de referencias de paginas.
- Marcado visual para: acierto, fallo de pagina, pagina expulsada y pagina cargada.

Interaccion sugerida:

- Campo o selector con una cadena de referencias, por ejemplo `7, 0, 1, 2, 0, 3, 0, 4`.
- Selector de cantidad de marcos.
- Contador de fallos de pagina.

## Pagina nueva 4: Algoritmos FIFO, LRU y Clock

Objetivo: comparar los criterios de seleccion pedidos por la consigna.

Contenido sugerido:

- FIFO: expulsa la pagina que lleva mas tiempo en memoria.
- LRU: expulsa la pagina menos usada recientemente.
- Clock: mejora FIFO usando un bit de referencia para dar segunda oportunidad.

Visual sugerido:

- Tres columnas comparativas con la misma secuencia de referencias.
- En FIFO: cola de llegada.
- En LRU: orden por uso reciente.
- En Clock: circulo con puntero y bits de referencia.

Interaccion sugerida:

- Boton "siguiente referencia".
- Selector de algoritmo.
- Resumen final con cantidad de fallos y lectura ejecutiva: simpleza, precision y costo de implementacion.

## Pagina nueva 5: Round Robin en el servidor de examenes

Objetivo: reutilizar el concepto de quantum, pero aplicado al servidor central que procesa envios simultaneos.

Contenido sugerido:

- Cada peticion de alumno entra en una cola.
- El servidor atiende cada peticion durante un quantum.
- Si una peticion no termina, vuelve al final de la cola.
- Evita que un envio pesado bloquee a los demas.

Visual sugerido:

- Cola circular de peticiones.
- Linea de tiempo del servidor.
- Diferenciar envios livianos, medianos y pesados.

Interaccion sugerida:

- Slider de quantum.
- Sliders para tamano de respuestas de alumnos.
- Tabla con tiempo de finalizacion y espera por alumno.

Nota: existe una pagina de Round Robin para CPU en clase. Esta nueva pagina no deberia reemplazarla; deberia enfocar el mismo algoritmo en la concurrencia del servidor de examenes.

## Pagina nueva 6: Sincronizacion, semaforos y condiciones de carrera

Objetivo: explicar por que el archivo central de calificaciones requiere acceso controlado.

Contenido sugerido:

- Riesgo: multiples procesos escriben notas al mismo archivo al mismo tiempo.
- Condicion de carrera: el resultado depende del orden no controlado de ejecucion.
- Semaforo/mutex: permite que solo una escritura critica ocurra por vez.

Visual sugerido:

- Dos caminos:
  - "Sin sincronizacion": escrituras superpuestas, nota perdida o archivo inconsistente.
  - "Con semaforo": cola de espera, entrada a seccion critica, liberacion del recurso.

Interaccion sugerida:

- Toggle "usar semaforo".
- Simulacion de 3 a 5 alumnos intentando escribir notas.
- Resultado visible: archivo consistente o conflicto de escritura.

## Pagina nueva 7: Cierre de Parte 2

Objetivo: cerrar la respuesta integrando memoria virtual, reemplazo, planificacion y sincronizacion.

Contenido sugerido:

- Swapping sostiene la ejecucion cuando la RAM no alcanza.
- FIFO, LRU y Clock deciden que paginas salen de memoria.
- Round Robin distribuye atencion del servidor de forma equitativa.
- Semaforos evitan corrupcion de datos compartidos.

Visual sugerido:

- Mapa final del sistema: terminal, RAM, disco, servidor, cola RR y archivo de calificaciones.
- Checklist de riesgos mitigados:
  - colapso por falta de RAM;
  - demasiados fallos de pagina;
  - bloqueo por peticiones pesadas;
  - condiciones de carrera.

## Orden recomendado en la app

Sin alterar las paginas actuales, el sidebar podria sumar al final:

- `Parte 2 / Contexto de alta demanda`
- `Parte 2 / Memoria virtual y swapping`
- `Parte 2 / Reemplazo de paginas`
- `Parte 2 / FIFO, LRU y Clock`
- `Parte 2 / Round Robin en servidor`
- `Parte 2 / Semaforos y carrera`
- `Parte 2 / Cierre integrador`

## Alcance de implementacion sugerido

Primera iteracion:

- Agregar las paginas nuevas como funciones separadas.
- No modificar funciones existentes.
- Extender solamente el router/sidebar para que las paginas nuevas sean accesibles.
- Reutilizar componentes actuales: `phase_header`, `context_card`, `mini_card`, tablas y estilos de tarjetas.

Segunda iteracion:

- Agregar simuladores visuales de reemplazo de paginas.
- Agregar animacion simple para Clock.
- Agregar simulacion de condicion de carrera con y sin semaforo.

## Riesgos a cuidar

- No mezclar la Parte 2 con las paginas previas de la Actividad 3.
- No reemplazar la pagina actual de Round Robin; crear una version especifica para servidor de examenes.
- Evitar texto largo sin visuales, porque el PDF pide esquemas o animaciones propias.
- Mantener el cierre actual intacto y agregar un cierre nuevo para Parte 2.
