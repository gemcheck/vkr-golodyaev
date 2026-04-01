import { Node, NodeType } from './parser';

export interface SymbolInfo {
    type: NodeType;
    line: number;
    scope: string;
}

export interface AnalysisResult {
    symbolTable: {
        [key: string]: SymbolInfo;
    };
}

export function analyze(nodes: Node[]): AnalysisResult {
    const symbolTable: Record<string, SymbolInfo> = {};
    let currentScope = 'global';

    nodes.forEach(node => {
        
        if (node.type === 'function') {
            currentScope = node.name;
            symbolTable[`${node.name}_global`] = { type: 'function', line: node.line, scope: 'global' };
        } 
        else if (node.type === 'parameter' || node.type === 'variable') {
            symbolTable[`${node.name}_${currentScope}`] = { 
                type: node.type, 
                line: node.line, 
                scope: currentScope 
            };
        } 
        else {
            
            symbolTable[`${node.name}_global`] = { 
                type: node.type, 
                line: node.line, 
                scope: 'global' 
            };
        }
    });
    
    return { symbolTable };
}