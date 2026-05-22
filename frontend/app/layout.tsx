import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Estadísticas FUTVE - Liga FUTVE 2026",
  description:
    "El portal de estadísticas del fútbol venezolano. Tabla de posiciones, resultados, goleadores y más de la Liga FUTVE.",
  keywords:
    "fútbol venezolano, liga FUTVE, estadísticas, tabla de posiciones, Táchira, Caracas FC",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`${inter.variable} bg-background dark`}>
      <body className="min-h-screen bg-background font-sans text-foreground antialiased">
        {children}
      </body>
    </html>
  );
}
