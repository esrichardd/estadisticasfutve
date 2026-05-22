## Imported Claude Cowork project instructions

## Flujo de trabajo obligatorio

Antes de ejecutar cualquier código, presenta un plan paso a paso detallado de lo que vas a hacer y **espera mi confirmación explícita ("GO")** antes de proceder. Sin GO, no ejecutes nada.

---

## Contexto permanente del proyecto

Siempre ten en cuenta el contenido de estos archivos como referencia base para cualquier decisión técnica:

- **Arquitectura del backend:** `./backend/docs/architecture/README.md`
- **Arquitectura de base de datos:** `./backend/docs/database/README.md`
- **Guía de contribución:** `./CONTRIBUTING.md`

---

## Cambios core → documentación

Cuando realices cualquier cambio core, **antes de cerrar la tarea**, pregúntame si deseo actualizar la documentación correspondiente y muéstrame un ejemplo concreto de cómo quedaría el cambio redactado.

Se consideran cambios core, entre otros:

- Modificaciones a modelos de datos
- Nuevas migraciones o cambios en esquemas de base de datos
- Cambios en la arquitectura del backend (nuevos servicios, módulos, patrones)
- Cambios en dependencias principales o configuración del proyecto

**Formato esperado al preguntar:**
> "¿Deseas agregar este cambio a la documentación? Así quedaría:
> [ejemplo del fragmento a añadir o modificar]"
