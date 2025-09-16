import {useId} from 'react'
import styles from './form.module.css'

export function Input({type="text", desc, value, name}) {
  const id = useId()
  return (
    <div id={ id} className={styles.input}>
      <label htmlFor={ id }>{ desc }</label>
      <input id={id} name={name} type={type} defaultValue={value}/>
    </div>
  )

}

export function Select({desc, options, value, name}) {

  const id = useId()
  return (
    <div id={id} className={styles.select}>
      <label htmlFor={ id }>{ desc }</label>
      <select id={id} defaultValue={value} name={name}>
        {options.map(o => <option key={o}>{o}</option>)}
      </select>
    </div>
  )
}

export function Checkbox({desc,checked=false, setChecked}) {
  const id = useId()
  return (
    <div className={styles.checkbox}>
      <input id={id} type="checkbox" defaultChecked={checked} onChange={e => {setChecked(e.target.checked);}}/>
      <label htmlFor={ id }>{ " " +  desc }</label>
    </div>
  )
}
export function Button({desc, color, onClick, submit}) {
  if (!color)
    color = "inativo"
  const color_style = {
    backgroundColor: `var(--${color}-light`,
    color: `var(--${color})`,
    border: `2px solid var(--${color})`
  }
  return (<button style={color_style} className={styles.button + " "} type={submit ? "submit" : "button" } onClick={onClick}>{desc}</button>)
}
