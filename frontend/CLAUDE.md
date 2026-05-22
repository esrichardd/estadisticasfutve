# Frontend — Estadísticas FUTVE

## Lenguaje

- Código: inglés.
- Variables, funciones, tipos y archivos: inglés.
- UI visible al usuario: español neutro.
- Comentarios en código: inglés.

## Stack

- Next.js App Router.
- React 19.
- TypeScript strict.
- Tailwind CSS v4.
- `lucide-react` para iconos.

## Arquitectura

Usar arquitectura por feature.

```txt
app/
  page.tsx
  layout.tsx
  globals.css

features/
  [feature]/
    api/
    components/
    types/
    utils/

components/
  ui/
```

Reglas:

- `app/[route]/page.tsx` debe ser delgado.
- Las rutas componen secciones, no contienen lógica pesada.
- La lógica de datos de una feature vive en `features/[feature]/api`.
- Los tipos de una feature viven en `features/[feature]/types`.
- Los componentes genéricos viven en `components/ui`.
- No mezclar fetch, transformación de datos y UI visual en el mismo componente.

## Naming

| Elemento           | Convención | Ejemplo                 |
| ------------------ | ---------- | ----------------------- |
| Componentes React  | PascalCase | `StandingsTable.tsx`    |
| Hooks              | camelCase  | `useRoundTabs`          |
| Funciones          | camelCase  | `getHomeStandings`      |
| Tipos TypeScript   | PascalCase | `StandingRow`           |
| Archivos API/utils | kebab-case | `get-home-standings.ts` |
| Carpetas           | kebab-case | `match-detail`          |

## React

- Server Components por defecto.
- Usar `"use client"` solo si hay hooks, eventos, refs o APIs del browser.
- Aislar interactividad en componentes pequeños.
- No convertir una pantalla completa en Client Component si solo una sección necesita estado.
- No pasar funciones no serializables desde Server Components a Client Components.

## Data Fetching

- Los fetchers viven en `features/[feature]/api`.
- Los componentes visuales no deben hacer `fetch` directo.
- Los mocks viven cerca del fetcher.
- Cambiar de mock a API real no debe requerir tocar la UI.
- Queries independientes deben resolverse en paralelo cuando aplique.
- El frontend formatea datos, pero no debe duplicar reglas de negocio complejas.

## Suspense y Skeletons

Usar `Suspense` granular por sección.

No crear archivos separados de skeleton.

Cada componente que necesite loading state debe usar una variante `skeleton` con discriminated union:

```tsx
type Props = { skeleton: true } | { skeleton?: false; data: Data };

export function Component(props: Props) {
  if (props.skeleton) {
    return <div className="skeleton ..." />;
  }

  return <div>{props.data.name}</div>;
}
```

En `page.tsx`:

```tsx
<Suspense fallback={<Component skeleton />}>
  <ComponentData />
</Suspense>
```

Si el componente usa hooks, extraer la lógica a un componente interno:

```tsx
function ComponentInner({ data }: { data: Data }) {
  const [open, setOpen] = useState(false);
  return <div>{data.name}</div>;
}

export function Component(props: Props) {
  if (props.skeleton) return <div className="skeleton ..." />;
  return <ComponentInner data={props.data} />;
}
```

## TypeScript

- No usar `any`.
- Tipar contratos de API explícitamente.
- Mantener tipos grandes fuera de componentes visuales.
- Preferir discriminated unions para variantes.
- Usar imports de tipo con `import type`.

## Diseño

La UI debe sentirse como un dashboard deportivo premium.

Principios:

- Dark mode como base.
- Layout compacto, denso y legible.
- Jerarquía clara para datos importantes.
- Acentos vinotinto y dorado.
- Verde para estados positivos.
- Rojo para estados negativos.
- Gris para estados neutros.
- Tablas compactas con números alineados.
- Usar escudos, avatares o identificadores visuales cuando aplique.

Evitar:

- Estética SaaS genérica.
- Demasiado blanco.
- Cards grandes con poco contenido.
- Hero marketing innecesario.
- Texto visible explicando cómo usar la interfaz.
- Decoración sin función.

## Tailwind y CSS

- Tokens globales en `app/globals.css`.
- Preferir tokens sobre colores hardcodeados.
- Usar clases como:
  - `bg-background`
  - `bg-card`
  - `text-foreground`
  - `text-muted-foreground`
  - `text-secondary`
  - `border-border`
- CSS global solo para tokens, base styles, animaciones y utilidades compartidas.
- Evitar CSS global específico de una feature.

## Dependencias

- Usar `lucide-react` para iconos.
- No agregar librerías UI pesadas sin justificación.
- No instalar sistemas completos de componentes si componentes propios bastan.
- Si se agrega una dependencia, actualizar `package.json`.

## Fuentes

- Se puede usar `next/font/google`.
- Si el build falla por red, preferir `next/font/local` o fuente del sistema.

## Performance

- Mantener bajo el bundle cliente.
- No usar `"use client"` innecesariamente.
- Evitar cálculos pesados en render.
- Usar `Suspense` por secciones.
- Evitar fetch serial cuando los datos son independientes.

## Antes de cerrar

- No dejar imports muertos.
- Verificar que los textos visibles estén en español.
- Verificar que código, tipos y archivos estén en inglés.
- Mantener skeletons como variante del componente.
- No introducir dependencias innecesarias.
- Reportar si no se pudo ejecutar lint/build.
