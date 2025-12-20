export function Texto() {}

Texto.limitado = (texto, limite) => {
  const texto_passou_do_limite  = texto && texto.length > limite
  if (texto_passou_do_limite)
    return texto.substr(0,limite-3) + "..."
  return texto
}

Texto.titleCase = (str) => {
  return str.toLowerCase().replace(/\b\w/g, s => s.toUpperCase());
}
