import * as vscode from 'vscode';
import { SemanticProvider } from './provider';

export function activate(context: vscode.ExtensionContext) {
    console.log('✅ Extension "vkr-golodyaev" is now active!');

    // всплывающее окно при активации расширения
    vscode.window.showInformationMessage('Расширение "vkr-golodyaev" активировано!');

    // команда 1: Hello World
    const helloCommand = vscode.commands.registerCommand('vkr-golodyaev.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from vkr-golodyaev!');
        console.log('Hello World command executed');
    });

    // команда 2: Пример вывода текущего файла
    const currentFileCommand = vscode.commands.registerCommand('vkr-golodyaev.currentFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const fileName = editor.document.fileName;
            vscode.window.showInformationMessage(`Текущий файл: ${fileName}`);
            console.log(`Current file: ${fileName}`);
        } else {
            vscode.window.showWarningMessage('Нет открытого файла');
        }
    });

	const provider = new SemanticProvider();

    context.subscriptions.push(
        vscode.languages.registerDocumentSemanticTokensProvider(
            { language: 'python' },
            provider,
            provider.legend
        )
    );

    // маленькая метка справа снизу, чтобы видеть, что расширение работает
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = '$(pulse) VKR Active';
    statusBarItem.tooltip = 'Расширение vkr-golodyaev запущено';
    statusBarItem.show();

    // подписка на все ресурсы, чтобы корректно очищать при деактивации
    context.subscriptions.push(helloCommand, currentFileCommand, statusBarItem);
}

export function deactivate() {
    console.log('Extension "vkr-golodyaev" is now deactivated');
}