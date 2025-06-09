function zeroPad(num, places) {
  var zero = places - num.toString().length + 1;
  return Array(+(zero > 0 && zero)).join("0") + num;
}

export function tempo_para_texto(horas, minutos) {
  return zeroPad(horas, 2) + ":" + zeroPad(minutos, 2)
}

export function hora_para_texto(hora) {
  const parte_inteira = Math.floor(hora)
  const parte_decimal = hora - parte_inteira
  
  const minutos = Math.floor(parte_decimal*60)

  return tempo_para_texto(parte_inteira, minutos)
}


export function tempo_para_número(tempo) {
  const hora    = Number(tempo.split(":")[0])
  const minutos = Number(tempo.split(":")[1])

  return hora + minutos/60

}
