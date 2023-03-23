import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { useBlocks } from './data/blocks'
import { BlockCell } from './presentation/assemblies/Block/BlockCell'

function App() {

  const blocks = useBlocks();
  console.log(blocks)

  return (
    <div className="App">
      <div style={{
        width : "100vw",
        height : "100vh",
        overflowY : "scroll",
        padding : "20px",
        textAlign : "left"
      }}>
          <h1>Arkham Intelligence <span style={{
            fontSize : 28
          }}>(Take-home Assessment)</span></h1>
          <hr style={{
            // width : "100%",
          }} color='#FFFFFF'/>
          {blocks.map((block)=>{
            return <BlockCell expanded={true} style={{
              width : "94%",
              overflowX : "scroll"
            }} key={block.id} block={block}/>
          })}
      </div>
    </div>
  )
}

export default App
