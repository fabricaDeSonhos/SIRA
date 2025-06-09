import {useId} from 'react'
import styles from './form.module.css'

export function Input({type="text", desc, value, name}) {
  const id = useId()
  return (
    <div id={ id} className={styles.input}>
      <label htmlFor={ id }>{ desc }</label>
      <input id={id} name={name} type={type} value={value}/>
    </div>
  )

}

export function Select({desc, options, value, name}) {

  const id = useId()
  return (
    <div id={id} className={styles.select}>
      <label htmlFor={ id }>{ desc }</label>
      <select id={id} value={value} name={name}>
        {options.map(o => <option>{o}</option>)}
      </select>
    </div>
  )
}

export function Checkbox({desc,checked=false, setChecked}) {
  const id = useId()
  return (
    <div id={ id} className={styles.chekbox}>
      <input id={id} type="checkbox" defaultChecked={checked} onChange={e => {setChecked(e.target.checked);}}/>
      <label htmlFor={ id }>{ " " +  desc }</label>
    </div>
  )
}
export function Button({desc, highlight, onClick, submit}) {
  const highlight_class = highlight ? styles.highlight : ""
  return (<button className={styles.button + " " + highlight_class} type={submit ? "submit" : "button" } onClick={onClick}>{desc}</button>)
}
