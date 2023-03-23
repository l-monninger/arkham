import { Transaction } from "../transaction";

export interface Block {
    id : string;
    txs : Transaction[];
}