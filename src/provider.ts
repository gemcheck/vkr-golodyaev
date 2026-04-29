import * as vscode from 'vscode';
import { parse } from './parser';
import { analyze } from './analyzer';

export class SemanticProvider implements vscode.DocumentSemanticTokensProvider {

    readonly legend = new vscode.SemanticTokensLegend([
        'function', 
        'variable', 
        'parameter', 
        'keyword', 
        'string', 
        'number', 
        'boolean',
        'comment'
    ]);

provideDocumentSemanticTokens(document: vscode.TextDocument): vscode.ProviderResult<vscode.SemanticTokens> {
        const text = document.getText();
        const nodes = parse(text);
        const { symbolTable } = analyze(nodes);
        const builder = new vscode.SemanticTokensBuilder(this.legend);
        const lines = text.split(/\r?\n/);

        const typeMap: Record<string, number> = {
            'function': 0, 'variable': 1, 'parameter': 2, 'keyword': 3, 
            'string': 4, 'number': 5, 'boolean': 6, 'comment': 7
        };

        // 1. Собираем все токены документа в единый массив
        
        const allTokens: { line: number, start: number, length: number, type: number }[] = [];

        let currentScope = 'global';

        lines.forEach((lineText, lineIndex) => {
            if (lineText.trim().length > 0 && !lineText.startsWith(' ') && !lineText.startsWith('\t')) {
                currentScope = 'global';
            }
            const funcMatch = lineText.match(/^\s*def\s+(\w+)/);
            if (funcMatch) {
                currentScope = funcMatch[1];
            }

            const commentIndex = lineText.indexOf('#');

            nodes.filter(n => n.line === lineIndex && ['string', 'number', 'boolean', 'comment'].includes(n.type))
                 .forEach(node => {
                    let startPos = 0;
                    while ((startPos = lineText.indexOf(node.name, startPos)) !== -1) {
                        allTokens.push({
                            line: lineIndex,
                            start: startPos,
                            length: node.name.length,
                            type: typeMap[node.type]
                        });
                        startPos += node.name.length;
                    }
                 });

            const words = lineText.matchAll(/\b(\w+)\b/g);
            for (const match of words) {
                const word = match[0];
                const start = match.index!;

                const isInsideLiteral = allTokens.some(t => 
                    t.line === lineIndex && 
                    t.type === typeMap['string'] && 
                    start >= t.start && 
                    (start + word.length) <= (t.start + t.length)
                );

                if (isInsideLiteral) continue;

                let symbol = symbolTable[`${word}_${currentScope}`]
                
                if (!symbol) {
                    symbol = symbolTable[`${word}_global`];
                }

                if (!symbol) {
                    const node = nodes.find(n => n.name === word);
                    if (node) {
                        symbol = { type: node.type, scope: 'global', line: node.line };
                    }
                }

                symbol = symbolTable[`${word}_${currentScope}`] || symbolTable[`${word}_global`];

                if (symbol) {
                    allTokens.push({
                        line: lineIndex,
                        start: start,
                        length: word.length,
                        type: typeMap[symbol.type]
                    });
                }
            }
        });

        // 2. Сортируем: сначала по номеру строки, затем по индексу начала
        allTokens.sort((a, b) => {
            if (a.line === b.line) {
                return a.start - b.start;
            }
            return a.line - b.line;
        });

        // 3. Передаем в builder с защитой от дубликатов (перекрытий)
        let lastLine = -1;
        let lastStart = -1;

        for (const token of allTokens) {
            if (token.line !== lastLine) {
                lastLine = token.line;
                lastStart = -1; 
            }
            
            // Добавляем токен только если он не перекрывает предыдущий
            if (token.start > lastStart) {
                builder.push(token.line, token.start, token.length, token.type, 0);
                lastStart = token.start;
            }
        }

        return builder.build();
    }
}