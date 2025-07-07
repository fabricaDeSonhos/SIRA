'use client'
 import {useState} from 'react'
 
export default function Lista(){
    
    const [contador, setContador] = useState(0)
    consta [caixa, setCaixa] = useState("")


    function somar(){
        setContador(contador + caixa)
    }

    function hadleCaixa(e){
        setCaixa(e.target.value)
    }

    function atualizarCaixa(e){
        setCaixa(Number(e.target.value))
    }  

    return (
        <div> 
            
            <p>{contador}</p>
            <input className="border" type="text" 
                onChange={atualizarCaixa} /> 
            <button onClick={somar}>Somar</button>     

        
            <h1 className="text-3xl font-bold underline">
                Hello worldaaaaaaaaa!
            </h1>
            
            <p className="text-lg text-gray-700">
                Welcome to your Next.js app!
            </p>
        </div>
    )
}
