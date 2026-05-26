# Datos

Estructura sugerida para datasets de importacion:

- `seeds/`: datos pequenos, curados y versionables.
- `raw/`: datos crudos descargados o copiados desde fuentes externas.
- `normalized/`: datos intermedios ya limpiados para importadores.
- `archive/`: copias historicas locales si se necesita trazabilidad.

Por defecto, solo `seeds/` deberia considerarse parte estable del proyecto.
