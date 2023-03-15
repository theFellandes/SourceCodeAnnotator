// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const path = require('path');
const { spawn } = require('child_process');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	async function comment_file(engine) {
		// Get the active text editor
		const activeEditor = vscode.window.activeTextEditor;
		if (!activeEditor) {
			vscode.window.showErrorMessage('No active editor found!');
			return;
		}

		// Get the code and send it to Annotator
		// const text = activeEditor.document.getText();

		// Get the URI (Uniform Resource Identifier) for the file that is open in the editor
		const fileUri = activeEditor.document.uri;
		// Convert the URI to a file path
		const filePath = fileUri.fsPath;

		vscode.window.showInformationMessage('LazyDoc is thinking...')
		const pythonProcess = await spawn('python', ['-u', path.join(__dirname, 'vscode_main.py'), engine, filePath]);

		// This listener 
		pythonProcess.stdout.on('data', (data) => {
			const wholeDocumentRange = activeEditor.document.validateRange(new vscode.Range(0, 0, Number.MAX_SAFE_INTEGER, Number.MAX_SAFE_INTEGER));
			activeEditor.edit((editBuilder) => {
				editBuilder.replace(wholeDocumentRange, `${data}`);
			});
		});

		pythonProcess.on('close', (code) => {
			console.log(`child process exited with code ${code}`);
		});
	}

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	// console.log('Congratulations, your extension "lazydoc" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('lazydoc.commentCurrentFileChatGPT', function () {
		comment_file('chatgpt')
	});

	context.subscriptions.push(disposable);

	disposable = vscode.commands.registerCommand('lazydoc.commentCurrentFile', async function () {
		comment_file('lazydoc')
	});

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
function deactivate() { }

module.exports = {
	activate,
	deactivate
}
