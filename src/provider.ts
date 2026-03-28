import * as vscode from 'vscode';
import { parse } from './parser';
import { analyze } from './analyzer';

export class SemanticProvider implements vscode.DocumentSemanticTokensProvider {

    legend = new vscode.SemanticTokensLegend([
        'function',
        'variable',
        'parameter'
    ]);

    provideDocumentSemanticTokens(
        document: vscode.TextDocument
    ): vscode.ProviderResult<vscode.SemanticTokens> {

        const text = document.getText();

        const nodes = parse(text);
        const symbols = analyze(nodes);

        const builder = new vscode.SemanticTokensBuilder(this.legend);

        const lines = text.split('\n');

        for (let lineIndex = 0; lineIndex < lines.length; lineIndex++) {
            const line = lines[lineIndex];

            for (const name in symbols) {
                const symbol = symbols[name];
                const index = line.indexOf(name);

                if (index !== -1) {
                    let tokenType = 0;

                    if (symbol.type === 'function') tokenType = 0;
                    if (symbol.type === 'variable') tokenType = 1;
                    if (symbol.type === 'parameter') tokenType = 2;

                    builder.push(
                        lineIndex,
                        index,
                        name.length,
                        tokenType,
                        0
                    );
                }
            }
        }

        return builder.build();
    }
}