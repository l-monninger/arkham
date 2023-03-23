import React, {FC, ReactElement, useState} from 'react';
import { ChevronDown, ChevronUp } from "react-bootstrap-icons";

export const LABELDOWN_CLASSNAMES : string[] = [ ];
export const LABELDOWN_STYLE : React.CSSProperties = {
    padding : "4px"
};

export type LabeldownProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    Up ? : React.ReactNode;
    Down ? : React.ReactNode;
    up ? : boolean;
    Label ? : React.ReactNode;
    Content ? : React.ReactNode;
};

export const Labeldown : FC<LabeldownProps>  = (props) =>{

    const [up, setUp] = useState(props.up||false);
    
    const _Up = props.Up??<ChevronUp/>
    const _Down = props.Down??<ChevronDown/>
    const _Which = !up ? _Up : _Down;

    return (
        <div
        className={[...!props.overrideClasses ? LABELDOWN_CLASSNAMES : [], ...props.classNames||[]].join(" ")}
        style={{...!props.overrideStyle ? LABELDOWN_STYLE : {}, ...props.style}}>
            <div
            className='hcr'
            onClick={()=>setUp(!up)}
            style={{
                display : "grid",
                gridTemplateColumns : "9fr 1fr",
                alignContent : "center",
                alignItems : "center",
                cursor : "pointer"
            }}>
                <div style={{
                    display : "grid",
                    justifyItems : "left",
                    justifyContent : "left"
                }}>
                    {props.Label}
                </div>
                <div style={{
                    display : "grid",
                    justifyItems : "right",
                    justifyContent : "right"
                }}>
                    <div>
                        {_Which}
                    </div>
                </div>
            </div>
            {!up && <div style={{
                width : "100%",
                overflowX : "scroll"
            }}>
                {props.Content}
            </div>}
        </div>
    )
};