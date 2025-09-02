import { Open_Sans, Source_Code_Pro} from "next/font/google";
import "./css/globals.css";

const sans = Open_Sans({
  variable: "--font-sans",
  subsets: ["latin"],
});

const mono = Source_Code_Pro({
  variable: "--font-monospace",
  subsets: ["latin"],
});

export const metadata = {
  title: "SIRA - Sistema de Reserva de Ambiente",
  description: "SIRA - Sistemas de Reserva de Ambientes um projeto de extensão para o IFC campus Blumenau, um sistema visando resolver o problema de alocações de salas de informática do campus ",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-br">
      <body className={`${sans.variable} ${mono.variable}`}>
        {children}
      </body>
    </html>
  );
}
