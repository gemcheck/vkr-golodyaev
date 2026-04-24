export type NodeType = | 'function' | 'variable' | 'parameter' | 'keyword' | 'string' | 'number' | 'boolean' | 'comment';

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
        // 0 - Обработка строк (включая f-строки)
        const stringRegex = /(f)?(["'])(?:(?=(\\?))\3.)*?\2/g;
        let strMatch;

        while ((strMatch = stringRegex.exec(line)) !== null) {
            const fullMatch = strMatch[0];
            const isFString = strMatch[1] === 'f';

            if (isFString) {
                // Логика для f-строки: разбиваем на части
                let lastPos = 0;
                const braceRegex = /{(.*?)}/g;
                let braceMatch;

                while ((braceMatch = braceRegex.exec(fullMatch)) !== null) {
                    // Записываем текстовый фрагмент ДО скобки как строку
                    const textBefore = fullMatch.substring(lastPos, braceMatch.index);
                    if (textBefore) {
                        nodes.push({ type: 'string', name: textBefore, line: i });
                    }

                    // Выражение внутри {} — рекурсивно парсим как обычный код
                    // (Для простоты в ВКР можно просто пропустить его здесь, 
                    // чтобы основной цикл парсера по словам подхватил 'i' и 'get_fibonacci')
                    
                    // Записываем сами скобки как пунктуацию или ключевые слова (по желанию)
                    nodes.push({ type: 'keyword', name: '{', line: i });
                    nodes.push({ type: 'keyword', name: '}', line: i });

                    lastPos = braceMatch.index + braceMatch[0].length;
                }

                // Записываем остаток строки после последней скобки
                const textAfter = fullMatch.substring(lastPos);
                if (textAfter) {
                    nodes.push({ type: 'string', name: textAfter, line: i });
                }
            } else {
                // Обычная строка
                nodes.push({ type: 'string', name: fullMatch, line: i });
            }
        }
        
        // 1 - функция
        const funcMatch = line.match(/^\s*def\s+(\w+)\s*\((.*?)\)/);

        if (funcMatch) {
            const [fullMatch, funcName, paramsString] = funcMatch;
            
            // Сохраняем имя функции
            nodes.push({ type: 'function', name: funcName, line: i });
            console.log(`[Parser] Найдена функция: ${funcName} на строке ${i}`);

            // Разбираем параметры
            paramsString.split(',').forEach(p => {
                const trimmedParam = p.trim();
                if (trimmedParam) {
                    // Очищаем от аннотаций (: int) и дефолтных значений (=None)
                    const cleanNameMatch = trimmedParam.match(/^(\w+)/);
                    if (cleanNameMatch) {
                        const paramName = cleanNameMatch[1];
                        nodes.push({ type: 'parameter', name: paramName, line: i });
                        console.log(`[Parser] --- Параметр: ${paramName}`);
                    }
                }
            });
        }
      
        // 2 - ключевые слова
        const keywords = ['def', 'self', 'try', 'with', 'class', 'for', 
                        'return', 'if', 'while', 'import', 'as', 'elif', 
                        'else', 'in', 'from', 'except', 'finally',
                        'lambda'];
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
        const assignMatches = line.matchAll(/\b(\w+)\s*=[^=]/g); 
        for (const match of assignMatches) {
            nodes.push({
                type: 'variable',
                name: match[1],
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