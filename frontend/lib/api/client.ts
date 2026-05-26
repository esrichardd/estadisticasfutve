/**
 * Cliente HTTP para llamadas al backend desde Server Components.
 *
 * Las variables BACKEND_API_URL y BACKEND_API_KEY son privadas del servidor:
 * no llevan prefijo NEXT_PUBLIC_ y nunca se exponen al browser.
 *
 * Uso:
 *   import { backendFetch } from "@/lib/api/client";
 *   const data = await backendFetch("/views/home/summary?season=2026&tournament=Apertura");
 */

const BACKEND_API_URL = process.env.BACKEND_API_URL;
const BACKEND_API_KEY = process.env.BACKEND_API_KEY;

if (!BACKEND_API_URL) {
  throw new Error("BACKEND_API_URL no está definida en las variables de entorno.");
}
if (!BACKEND_API_KEY) {
  throw new Error("BACKEND_API_KEY no está definida en las variables de entorno.");
}

export async function backendFetch<T>(path: string): Promise<T> {
  const url = `${BACKEND_API_URL}/api/v1${path}`;

  const res = await fetch(url, {
    headers: {
      "x-api-key": BACKEND_API_KEY!,
      "Content-Type": "application/json",
    },
    // Next.js cache: sin caché por defecto para datos en tiempo real.
    // Ajustar con next: { revalidate: N } si se quiere ISR en el futuro.
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(
      `Backend error ${res.status} en ${url}: ${await res.text()}`
    );
  }

  return res.json() as Promise<T>;
}
