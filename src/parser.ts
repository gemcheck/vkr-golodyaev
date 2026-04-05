export type NodeType =
    | 'function'
    | 'variable'
    | 'parameter'
    | 'keyword'
    | 'string'
    | 'number'
    | 'boolean'
    | 'comment';

export interface Node {
    type: NodeType;
    name: string;
    line: number;
}

export function parse(text: string): Node[] {
    const lines = text.split(/\r?\n/);
    const nodes: Node[] = [];

    for (let i = 0; i < lines.length; i++) {
        const fullLine = lines[i];

        // Ищем комментарий
        const commentMatch = fullLine.match(/#(.*)/);
        if (commentMatch) {
            nodes.push({
                type: 'comment',
                name: commentMatch[0],
                line: i
            });
        }

        // Для остального парсинга берем только часть до комментария
        let line = fullLine.split('#')[0];

        if (!line) continue;
        // 5 - Строки (в кавычках)
        const stringRegex = /("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')/g;

        let strMatch;
        while ((strMatch = stringRegex.exec(line)) !== null) {
            nodes.push({ 
                type: 'string', 
                name: strMatch[0], 
                line: i 
            });
        }
        
        // 1 - функция
        if (line.startsWith('def ')) {
            const match = line.match(/def (\w+)\((.*?)\)/);
            if (match) {
                const [, name, params] = match;
                nodes.push({ type: 'function', name, line: i });

                params.split(',').forEach(p => {
                    const param = p.trim();
                    if (param) {
                        nodes.push({ type: 'parameter', name: param, line: i });
                    }
                });
            }
        }

        
        
        // 2 - ключевые слова
        const keywords = ['def', 'with', 'class','for', 'return', 'if', 'while', 'import', 'as', 'elif', 'else', 'in', 'from'];
        for (const kw of keywords) {
            const regex = new RegExp(`\\b${kw}\\b`);
            if (regex.test(line)) {
                nodes.push({ type: 'keyword', name: kw, line: i });
            }
        }

        // 3 - встроенные функции
        const callMatches = line.matchAll(/\b(\w+)\s*\(/g);
        for (const match of callMatches) {
            const name = match[1];
            
            if (!keywords.includes(name)) {
                nodes.push({ type: 'function', name: name, line: i });
                
            }
        }

        // 4 - переменные
        const assignMatch = line.match(/^\s*(\w+)\s*=/); 
        if (assignMatch) {
            nodes.push({
                type: 'variable',
                name: assignMatch[1],
                line: i
            });
        }



        // 6 - Числа (целые и с плавающей точкой)
        const numberMatches = line.matchAll(/\b\d+(\.\d+)?\b/g);
        for (const match of numberMatches) {
            nodes.push({ type: 'number', name: match[0], line: i });
        }

        // 7 - Boolean (True/False)
        const boolMatches = line.matchAll(/\b(True|False|None)\b/g);
        for (const match of boolMatches) {
            nodes.push({ type: 'boolean', name: match[0], line: i });
        }
    }

    return nodes;
}