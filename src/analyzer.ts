import { Node } from './parser';

export type SymbolType = 'function' | 'variable' | 'parameter';

export interface SymbolInfo {
    type: SymbolType;
    scope: string;
    line: number;
}

export function analyze(nodes: Node[]) {
    const symbolTable: Record<string, SymbolInfo> = {};

    let currentScope = 'global';

    for (const node of nodes) {
        if (node.type === 'function') {
            currentScope = node.name;

            symbolTable[node.name] = {
                type: 'function',
                scope: 'global',
                line: node.line
            };
        }

        if (node.type === 'parameter') {
            symbolTable[node.name] = {
                type: 'parameter',
                scope: currentScope,
                line: node.line
            };
        }

        if (node.type === 'variable') {
            symbolTable[node.name] = {
                type: 'variable',
                scope: currentScope,
                line: node.line
            };
        }
    }

    return symbolTable;
}