import React, {FC, ReactElement} from 'react';
import { Block } from '../../../util/block';
import { Labeldown } from '../../components/Labeldown/Labeldown';

export const BLOCK_CLASSNAMES : string[] = [ ];
export const BLOCK_STYLE : React.CSSProperties = {
};

export type BlockCellProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    block ? : Block;
    expanded ? : boolean;
};

export const BlockCell : FC<BlockCellProps>  = (props) =>{

    return (
        <Labeldown
            up={props.expanded}
            style={props.style}
            classNames={props.classNames}
            Label={<h2>Block {props.block?.id}</h2>}
            Content={<table style={{
                padding : "10px"
            }}>
                <thead>
                    <tr>
                        <th>
                            Tx. Hash
                        </th>
                        <th>
                            From
                        </th>
                        <th>
                            To
                        </th>
                        <th>
                            ETH
                        </th>
                        <th>
                            USD
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {(props.block?.txs??[]).map((tx)=>{
                        return <tr key={tx.hash} className='hcr'>
                            <td>
                                {tx.hash}
                            </td>
                            <td>
                                {tx.from_addr}
                            </td>
                            <td>
                                {tx.to_addr}
                            </td>
                            <td>
                                {tx.eth}
                            </td>
                            <td>
                                {tx.usd}
                            </td>
                        </tr>
                    })}
                </tbody>
            </table>}/>
    )
};