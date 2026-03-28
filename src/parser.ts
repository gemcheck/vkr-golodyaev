export type NodeType = 'function' | 'variable' | 'parameter' | 'call';

export interface Node {
    type: NodeType;
    name: string;
    line: number;
}

export function parse(text: string): Node[] {
    const lines = text.split('\n');
    const nodes: Node[] = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // функция
        if (line.startsWith('def ')) {
            const match = line.match(/def (\w+)\((.*?)\)/);
            if (match) {
                const [, name, params] = match;

                nodes.push({ type: 'function', name, line: i });

                // параметры
                params.split(',').forEach(p => {
                    const param = p.trim();
                    if (param) {
                        nodes.push({
                            type: 'parameter',
                            name: param,
                            line: i
                        });
                    }
                });
            }
        }

        // переменные
        const assignMatch = line.match(/^(\w+)\s*=/);
        if (assignMatch) {
            nodes.push({
                type: 'variable',
                name: assignMatch[1],
                line: i
            });
        }

        // вызовы функций
        const callMatch = line.match(/(\w+)\(/);
        if (callMatch && !line.startsWith('def')) {
            nodes.push({
                type: 'call',
                name: callMatch[1],
                line: i
            });
        }
    }

    return nodes;
}