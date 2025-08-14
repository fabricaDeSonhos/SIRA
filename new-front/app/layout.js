import { Geist, Geist_Mono } from "next/font/google";
import "./css/globals.css";
import Header from "./components/header";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "SIRA - Sistema de Reserva de Ambiente",
  description:
    "SIRA - Sistemas de Reserva de Ambientes um projeto de extensão para o IFC campus Blumenau, um sistema visando resolver o problema de alocações de salas de informática do campus ",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-br">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        <Header />
        {children}
      </body>
    </html>
  );
}
