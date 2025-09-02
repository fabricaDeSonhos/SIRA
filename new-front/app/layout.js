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

const hsl = (name, hue, saturation, lightness) => { 
  const obj = {}
  obj[`--${name}`] = `hsl(${hue} ${saturation*100}% ${lightness*100}%)`
  obj[`--${name}-light`] = `hsl(from var(--${name}) h s 90%)`

  return obj
}

const colors = {
   ...hsl("krimson", 0   , .63  , .43),
   ...hsl("bordo"  , 330 , 1    , .19),
   ...hsl("roxo"   , 280 , 1    , .15),
   ...hsl("preto"  , 0   , 0    , .06),
   ...hsl("azul"   , 226 , .73  , .30),
   ...hsl("prata"  , 211 , .30  , .10),
   ...hsl("verde"  , 120 , 1    , .15),
   ...hsl("ouro"   , 44  , .97  , .54),
   ...hsl("ebony"  , 29  , .67  , .15)


}



const curso = (curso, color) => { 
  const obj = {}
  obj[`--${curso}`] = `var(--${color})`
  obj[`--${curso}-light`] = `var(--${color}-light)`

  return obj
}
const cursoColors = {

      ...curso("bcc"           , "bordo"),
      ...curso("pedagogia"     , "roxo"),
      ...curso("bee"           , "preto"),
      ...curso("medio"         , "verde"),
      ...curso("info"          , "azul"),
      ...curso("eletromecanica", "prata"),
      ...curso("mecatronica"   , "ebony"),
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-br">
      <body className={`${sans.variable} ${mono.variable}`} style={{...colors, ...cursoColors}}>
        {children}
      </body>
    </html>
  );
}
