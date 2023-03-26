import React, { useEffect, useReducer, useState } from "react";
import { Block } from "../../util/block";

export const getBlocksConnection = ()=>{
    return new WebSocket(`${import.meta.env.VITE_BLOCKS_SOCKET}/blocks`)
}

export const useBlocks = (size : number = 5) : Block[] =>{

    const [needsSocket, setNeedsSocket] = useState(true);
    const [blocks, addBlock] = useReducer((oldBlocks : Block[], block : Block) : Block[]=>{
        const _blocks = oldBlocks.slice(0, size-1);
        console.log(block, oldBlocks, oldBlocks.slice(0, size-1));
        return [
            block,
            ..._blocks
        ]

    }, [])

    useEffect(()=>{

        let timeout : number | undefined = undefined;
        
        if(needsSocket){

            let ws = getBlocksConnection();
            ws.onmessage = (msg)=>{
                
                addBlock(JSON.parse(msg.data) as Block)
            }
            ws.onclose = ()=>{
                
                timeout = setTimeout(()=>{
                    setNeedsSocket(true)
                }, 500);
                
            }   
    
            setNeedsSocket(false)
        }

        return ()=>{
            if(timeout) clearTimeout(timeout);
        }

    }, [needsSocket])

    return blocks
}