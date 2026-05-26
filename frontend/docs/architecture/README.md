# Arquitectura del Frontend — EstadisticasFutve

Guia de referencia para entender como esta organizado el frontend, como fluyen los datos y como se maneja la internacionalizacion.

---

## Indice

- [Principio central](#principio-central)
- [Stack](#stack)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Flujo de render](#flujo-de-render)
- [Capas](#capas)
  - [app/ — Rutas y composicion](#app--rutas-y-composicion)
  - [features/ — Codigo por dominio](#features--codigo-por-dominio)
  - [components/ui/ — UI reutilizable](#componentsui--ui-reutilizable)
  - [lib/ — Infraestructura compartida](#lib--infraestructura-compartida)
  - [proxy.ts — Redireccion previa a la ruta](#proxyts--redireccion-previa-a-la-ruta)
- [Internacionalizacion](#internacionalizacion)
- [Data fetching](#data-fetching)
- [Server y Client Components](#server-y-client-components)
- [Reglas de dependencia](#reglas-de-dependencia)

---

## Principio central

El frontend usa arquitectura por feature. Las rutas componen pantallas, las features contienen UI y datos de dominio, y `lib/` contiene infraestructura compartida.

```txt
app/        -> rutas, layouts, metadata y composicion de pantallas
features/   -> UI, fetchers, types y utils por dominio o pantalla
components/ -> componentes genericos reutilizables
lib/        -> utilidades transversales del frontend
```

La regla de oro: una ruta debe ser delgada. Si una pantalla crece, la logica vive dentro de su feature o en una utilidad transversal bien delimitada.

---

## Stack

- Next.js App Router.
- React 19.
- TypeScript strict.
- Tailwind CSS v4.
- `lucide-react` para iconos.
- i18n propio con rutas `[locale]` y diccionarios JSON.

---

## Estructura de carpetas

```txt
frontend/
├── app/
│   ├── [locale]/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   └── globals.css
│
├── features/
│   └── [feature]/
│       ├── api/
│       ├── components/
│       ├── types/
│       └── utils/
│
├── components/
│   └── ui/
│
├── lib/
│   ├── i18n/
│   │   ├── config.ts
│   │   ├── format.ts
│   │   ├── get-dictionary.ts
│   │   └── dictionaries/
│   │       └── [locale].json
│   └── api/
│       └── client.ts
│
├── public/
└── proxy.ts
```

### Convencion general

- `app/` contiene rutas, layouts, metadata y composicion de pantallas.
- `features/[feature]/` contiene codigo especifico de una pantalla o dominio.
- `features/[feature]/api/` contiene fetchers o adaptadores de datos.
- `features/[feature]/components/` contiene componentes visuales de esa feature.
- `features/[feature]/types/` contiene contratos TypeScript de esa feature.
- `features/[feature]/utils/` contiene helpers locales de esa feature.
- `components/ui/` contiene componentes genericos reutilizables.
- `lib/` contiene infraestructura compartida del frontend.
- `public/` contiene assets estaticos.
- `proxy.ts` contiene logica que corre antes de resolver la ruta.

---

## Flujo de render

```txt
Request
   ↓
proxy.ts
   ↓
/[locale]
   ↓
app/[locale]/layout.tsx
   ↓
app/[locale]/page.tsx
   ↓
features/[feature]/*
```

Ejemplo conceptual:

```txt
GET /en
  -> proxy.ts valida que la ruta ya tiene locale
  -> app/[locale]/layout.tsx valida `en`, define <html lang="en"> y metadata
  -> app/[locale]/page.tsx carga el diccionario y compone la pantalla
  -> features/[feature]/components renderiza cada seccion
```

Si la ruta no tiene idioma:

```txt
GET /
  -> proxy.ts redirige a /es o al idioma negociado
```

---

## Capas

### `app/` — Rutas y composicion

Contiene los archivos especiales de Next.js: `layout.tsx`, `page.tsx`, `globals.css` y futuras rutas.

Responsabilidades:

- Definir rutas.
- Validar parametros de ruta como `locale`.
- Definir metadata.
- Cargar diccionarios o configuracion necesaria para la pantalla.
- Componer secciones de features.
- Usar `Suspense` granular cuando una pantalla tenga secciones independientes.

Regla: `app/` no debe contener logica pesada de UI, transformacion de datos o reglas de negocio.

---

### `features/` — Codigo por dominio

Cada feature agrupa su propia UI, fetchers, tipos y helpers locales.

```txt
features/[feature]/
├── api/
├── components/
├── types/
└── utils/
```

Responsabilidades:

- `api/`: obtener o adaptar datos para la feature.
- `components/`: renderizar la UI especifica de la feature.
- `types/`: definir contratos TypeScript de la feature.
- `utils/`: helpers que solo tienen sentido dentro de esa feature.

Regla: si un helper empieza a servir a varias features, debe moverse a `lib/`.

---

### `components/ui/` — UI reutilizable

Contiene componentes genericos sin conocimiento del dominio FUTVE.

Ejemplos:

- `Skeleton`.
- Botones genericos.
- Inputs genericos.
- Componentes visuales base reutilizables.

Regla: estos componentes no deben importar desde `features/`.

---

### `lib/` — Infraestructura compartida

Contiene utilidades transversales del frontend que no pertenecen a una feature concreta.

Ejemplos actuales o esperados:

```txt
lib/i18n/
lib/api/
lib/env/
lib/auth/
```

Regla: `lib/` puede ser usado por `app/` y por `features/`, pero debe mantenerse libre de UI especifica de una pantalla.

#### `lib/api/client.ts` — Cliente HTTP del backend

Es el unico punto donde se leen las variables privadas del servidor (`BACKEND_API_URL`, `BACKEND_API_KEY`) y se construye el header `x-api-key`. Todos los fetchers de `features/*/api/` deben importar desde aqui.

```ts
import { backendFetch } from "@/lib/api/client";
const data = await backendFetch<MiTipo>("/views/home/summary?season=2026&tournament=Apertura");
```

Caracteristicas:

- `BACKEND_API_URL` y `BACKEND_API_KEY` son variables privadas del servidor. No llevan prefijo `NEXT_PUBLIC_` y nunca se exponen al browser.
- En Docker, `BACKEND_API_URL` apunta al nombre del servicio interno (`http://backend:8000`). En local, apunta a `http://localhost:8000`.
- `cache: "no-store"` por defecto. Usar `next: { revalidate: N }` si se quiere ISR en el futuro.
- Lanza error descriptivo si el backend responde con status no-OK, incluyendo la URL y el cuerpo de la respuesta.

Regla: ningun componente ni fetcher debe leer `BACKEND_API_KEY` directamente. Todo pasa por `backendFetch`.

---

### `proxy.ts` — Redireccion previa a la ruta

`proxy.ts` corre antes de que Next.js resuelva la ruta. En Next.js 16 reemplaza el nombre historico de `middleware.ts`.

Responsabilidades actuales:

- Detectar si una URL ya contiene un locale soportado.
- Leer `NEXT_LOCALE` cuando exista.
- Revisar `Accept-Language` para elegir idioma preferido.
- Redirigir rutas sin locale hacia `/{locale}`.

Regla: `proxy.ts` debe mantenerse delgado. La configuracion reusable vive en `lib/i18n`.

---

## Internacionalizacion

La internacionalizacion vive en `lib/i18n` y no pertenece a una feature concreta.

```txt
lib/i18n/
├── config.ts
├── format.ts
├── get-dictionary.ts
└── dictionaries/
    └── [locale].json
```

### Rutas

Las rutas publicas estan prefijadas por idioma:

```txt
/es
/en
```

`proxy.ts` redirige rutas sin locale hacia el idioma por defecto o negociado:

```txt
/          -> /es
/equipos   -> /es/equipos
/en        -> se mantiene
/es        -> se mantiene
```

### Configuracion

`lib/i18n/config.ts` define:

- locales soportados.
- locale por defecto.
- locales de formato para `Intl`.
- helper de validacion de locale.

Cada locale soportado debe tener un diccionario correspondiente en `lib/i18n/dictionaries/`.

### Diccionarios

Los textos visibles de UI viven en JSON:

```txt
lib/i18n/dictionaries/es.json
lib/i18n/dictionaries/en.json
```

Los diccionarios se organizan por area:

```txt
metadata
shell
home
```

Cuando se agregue una nueva feature con textos visibles, debe agregarse una rama nueva dentro del diccionario.

### Server y Client Components

Los Server Components pueden cargar diccionarios con:

```ts
getDictionary(locale);
```

Los Client Components no deben importar diccionarios completos. Reciben solo los labels que necesitan por props.

Esto mantiene bajo el bundle cliente y evita acoplar componentes interactivos a la infraestructura de traduccion.

### Que se traduce

Se traducen:

- Navegacion.
- Metadata.
- Titulos de secciones.
- Labels.
- Estados visibles.
- Mensajes vacios.
- Textos de accesibilidad.
- Formatos de fecha/hora.

No se traducen en frontend:

- Nombres de equipos.
- Nombres de jugadores.
- Nombres de torneos.
- Nombres de fases o jornadas provenientes de la API.
- Sedes.
- Datos persistidos del dominio.

Si en el futuro se necesita traducir datos persistidos, debe disenarse desde backend y base de datos.

---

## Data fetching

Los fetchers viven en:

```txt
features/[feature]/api/
```

Reglas:

- Los componentes visuales no deben hacer `fetch` directo.
- Cambiar de mock a API real no debe requerir tocar la UI visual ni los tipos.
- Queries independientes deben resolverse en paralelo cuando aplique.
- El frontend puede formatear datos (ej. ISO UTC → string display-ready), pero no debe duplicar reglas de negocio complejas.
- Todos los fetchers reales usan `backendFetch` de `lib/api/client.ts`. Nunca leen variables de entorno directamente.
- Si la respuesta del backend no coincide con el tipo TypeScript, se adapta en el fetcher con un objeto intermedio. No se modifican el tipo ni el componente visual.

---

## Server y Client Components

Los componentes son Server Components por defecto.

Usar `"use client"` solo cuando el componente necesite:

- estado local.
- eventos del usuario.
- refs.
- APIs del browser.
- efectos.

Regla: no convertir una pantalla completa en Client Component si solo una parte pequena necesita interactividad.

Cuando un Client Component necesita traducciones, debe recibir labels serializables por props.

---

## Reglas de dependencia

```txt
app/              -> puede importar features, components/ui y lib
features/         -> puede importar components/ui y lib
features/api      -> no debe importar componentes visuales
components/ui     -> no debe importar features
lib/              -> no debe importar features ni UI especifica
proxy.ts          -> debe importar solo configuracion/utilidades transversales
```

La direccion debe ir de lo especifico hacia lo compartido, no al reves.

```txt
app
 ↓
features
 ↓
components/ui + lib
```

Cuando una utilidad local empieza a tener uso transversal, se mueve hacia `lib/`.
