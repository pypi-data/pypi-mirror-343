(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_fileeditor-extension_lib_index_js"],{

/***/ "../packages/fileeditor-extension/lib/commands.js":
/*!********************************************************!*\
  !*** ../packages/fileeditor-extension/lib/commands.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "FACTORY": () => (/* binding */ FACTORY),
/* harmony export */   "Commands": () => (/* binding */ Commands)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




const autoClosingBracketsNotebook = 'notebook:toggle-autoclosing-brackets';
const autoClosingBracketsConsole = 'console:toggle-autoclosing-brackets';
/**
 * The command IDs used by the fileeditor plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'fileeditor:create-new';
    CommandIDs.createNewMarkdown = 'fileeditor:create-new-markdown-file';
    CommandIDs.changeFontSize = 'fileeditor:change-font-size';
    CommandIDs.lineNumbers = 'fileeditor:toggle-line-numbers';
    CommandIDs.lineWrap = 'fileeditor:toggle-line-wrap';
    CommandIDs.changeTabs = 'fileeditor:change-tabs';
    CommandIDs.matchBrackets = 'fileeditor:toggle-match-brackets';
    CommandIDs.autoClosingBrackets = 'fileeditor:toggle-autoclosing-brackets';
    CommandIDs.autoClosingBracketsUniversal = 'fileeditor:toggle-autoclosing-brackets-universal';
    CommandIDs.createConsole = 'fileeditor:create-console';
    CommandIDs.replaceSelection = 'fileeditor:replace-selection';
    CommandIDs.runCode = 'fileeditor:run-code';
    CommandIDs.runAllCode = 'fileeditor:run-all';
    CommandIDs.markdownPreview = 'fileeditor:markdown-preview';
    CommandIDs.undo = 'fileeditor:undo';
    CommandIDs.redo = 'fileeditor:redo';
    CommandIDs.cut = 'fileeditor:cut';
    CommandIDs.copy = 'fileeditor:copy';
    CommandIDs.paste = 'fileeditor:paste';
    CommandIDs.selectAll = 'fileeditor:select-all';
})(CommandIDs || (CommandIDs = {}));
/**
 * The name of the factory that creates editor widgets.
 */
const FACTORY = 'Editor';
const userSettings = [
    'autoClosingBrackets',
    'cursorBlinkRate',
    'fontFamily',
    'fontSize',
    'lineHeight',
    'lineNumbers',
    'lineWrap',
    'matchBrackets',
    'readOnly',
    'insertSpaces',
    'tabSize',
    'wordWrapColumn',
    'rulers',
    'codeFolding'
];
function filterUserSettings(config) {
    const filteredConfig = Object.assign({}, config);
    // Delete parts of the config that are not user settings (like handlePaste).
    for (let k of Object.keys(config)) {
        if (!userSettings.includes(k)) {
            delete config[k];
        }
    }
    return filteredConfig;
}
let config = filterUserSettings(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.CodeEditor.defaultConfig);
/**
 * A utility class for adding commands and menu items,
 * for use by the File Editor extension or other Editor extensions.
 */
var Commands;
(function (Commands) {
    /**
     * Accessor function that returns the createConsole function for use by Create Console commands
     */
    function getCreateConsoleFunction(commands) {
        return async function createConsole(widget, args) {
            var _a;
            const options = args || {};
            const console = await commands.execute('console:create', {
                activate: options['activate'],
                name: (_a = widget.context.contentsModel) === null || _a === void 0 ? void 0 : _a.name,
                path: widget.context.path,
                preferredLanguage: widget.context.model.defaultKernelLanguage,
                ref: widget.id,
                insertMode: 'split-bottom'
            });
            widget.context.pathChanged.connect((sender, value) => {
                var _a;
                console.session.setPath(value);
                console.session.setName((_a = widget.context.contentsModel) === null || _a === void 0 ? void 0 : _a.name);
            });
        };
    }
    /**
     * Update the setting values.
     */
    function updateSettings(settings, commands) {
        config = filterUserSettings(Object.assign(Object.assign({}, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.CodeEditor.defaultConfig), settings.get('editorConfig').composite));
        // Trigger a refresh of the rendered commands
        commands.notifyCommandChanged();
    }
    Commands.updateSettings = updateSettings;
    /**
     * Update the settings of the current tracker instances.
     */
    function updateTracker(tracker) {
        tracker.forEach(widget => {
            updateWidget(widget.content);
        });
    }
    Commands.updateTracker = updateTracker;
    /**
     * Update the settings of a widget.
     * Skip global settings for transient editor specific configs.
     */
    function updateWidget(widget) {
        const editor = widget.editor;
        let editorOptions = {};
        Object.keys(config).forEach((key) => {
            editorOptions[key] = config[key];
        });
        editor.setOptions(editorOptions);
    }
    Commands.updateWidget = updateWidget;
    /**
     * Wrapper function for adding the default File Editor commands
     */
    function addCommands(commands, settingRegistry, trans, id, isEnabled, tracker, browserFactory) {
        // Add a command to change font size.
        addChangeFontSizeCommand(commands, settingRegistry, trans, id);
        addLineNumbersCommand(commands, settingRegistry, trans, id, isEnabled);
        addWordWrapCommand(commands, settingRegistry, trans, id, isEnabled);
        addChangeTabsCommand(commands, settingRegistry, trans, id);
        addMatchBracketsCommand(commands, settingRegistry, trans, id, isEnabled);
        addAutoClosingBracketsCommand(commands, settingRegistry, trans, id);
        addReplaceSelectionCommand(commands, tracker, trans, isEnabled);
        addCreateConsoleCommand(commands, tracker, trans, isEnabled);
        addRunCodeCommand(commands, tracker, trans, isEnabled);
        addRunAllCodeCommand(commands, tracker, trans, isEnabled);
        addMarkdownPreviewCommand(commands, tracker, trans);
        // Add a command for creating a new text file.
        addCreateNewCommand(commands, browserFactory, trans);
        // Add a command for creating a new Markdown file.
        addCreateNewMarkdownCommand(commands, browserFactory, trans);
        addUndoCommand(commands, tracker, trans, isEnabled);
        addRedoCommand(commands, tracker, trans, isEnabled);
        addCutCommand(commands, tracker, trans, isEnabled);
        addCopyCommand(commands, tracker, trans, isEnabled);
        addPasteCommand(commands, tracker, trans, isEnabled);
        addSelectAllCommand(commands, tracker, trans, isEnabled);
    }
    Commands.addCommands = addCommands;
    /**
     * Add a command to change font size for File Editor
     */
    function addChangeFontSizeCommand(commands, settingRegistry, trans, id) {
        commands.addCommand(CommandIDs.changeFontSize, {
            execute: args => {
                const delta = Number(args['delta']);
                if (Number.isNaN(delta)) {
                    console.error(`${CommandIDs.changeFontSize}: delta arg must be a number`);
                    return;
                }
                const style = window.getComputedStyle(document.documentElement);
                const cssSize = parseInt(style.getPropertyValue('--jp-code-font-size'), 10);
                const currentSize = config.fontSize || cssSize;
                config.fontSize = currentSize + delta;
                return settingRegistry
                    .set(id, 'editorConfig', config)
                    .catch((reason) => {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                });
            },
            label: args => {
                var _a;
                if (((_a = args.delta) !== null && _a !== void 0 ? _a : 0) > 0) {
                    return args.isMenu
                        ? trans.__('Increase Text Editor Font Size')
                        : trans.__('Increase Font Size');
                }
                else {
                    return args.isMenu
                        ? trans.__('Decrease Text Editor Font Size')
                        : trans.__('Decrease Font Size');
                }
            }
        });
    }
    Commands.addChangeFontSizeCommand = addChangeFontSizeCommand;
    /**
     * Add the Line Numbers command
     */
    function addLineNumbersCommand(commands, settingRegistry, trans, id, isEnabled) {
        commands.addCommand(CommandIDs.lineNumbers, {
            execute: () => {
                config.lineNumbers = !config.lineNumbers;
                return settingRegistry
                    .set(id, 'editorConfig', config)
                    .catch((reason) => {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                });
            },
            isEnabled,
            isToggled: () => config.lineNumbers,
            label: trans.__('Line Numbers')
        });
    }
    Commands.addLineNumbersCommand = addLineNumbersCommand;
    /**
     * Add the Word Wrap command
     */
    function addWordWrapCommand(commands, settingRegistry, trans, id, isEnabled) {
        commands.addCommand(CommandIDs.lineWrap, {
            execute: args => {
                config.lineWrap = args['mode'] || 'off';
                return settingRegistry
                    .set(id, 'editorConfig', config)
                    .catch((reason) => {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                });
            },
            isEnabled,
            isToggled: args => {
                const lineWrap = args['mode'] || 'off';
                return config.lineWrap === lineWrap;
            },
            label: trans.__('Word Wrap')
        });
    }
    Commands.addWordWrapCommand = addWordWrapCommand;
    /**
     * Add command for changing tabs size or type in File Editor
     */
    function addChangeTabsCommand(commands, settingRegistry, trans, id) {
        commands.addCommand(CommandIDs.changeTabs, {
            label: args => {
                var _a;
                if (args.insertSpaces) {
                    return trans._n('Spaces: %1', 'Spaces: %1', (_a = args.size) !== null && _a !== void 0 ? _a : 0);
                }
                else {
                    return trans.__('Indent with Tab');
                }
            },
            execute: args => {
                config.tabSize = args['size'] || 4;
                config.insertSpaces = !!args['insertSpaces'];
                return settingRegistry
                    .set(id, 'editorConfig', config)
                    .catch((reason) => {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                });
            },
            isToggled: args => {
                const insertSpaces = !!args['insertSpaces'];
                const size = args['size'] || 4;
                return config.insertSpaces === insertSpaces && config.tabSize === size;
            }
        });
    }
    Commands.addChangeTabsCommand = addChangeTabsCommand;
    /**
     * Add the Match Brackets command
     */
    function addMatchBracketsCommand(commands, settingRegistry, trans, id, isEnabled) {
        commands.addCommand(CommandIDs.matchBrackets, {
            execute: () => {
                config.matchBrackets = !config.matchBrackets;
                return settingRegistry
                    .set(id, 'editorConfig', config)
                    .catch((reason) => {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                });
            },
            label: trans.__('Match Brackets'),
            isEnabled,
            isToggled: () => config.matchBrackets
        });
    }
    Commands.addMatchBracketsCommand = addMatchBracketsCommand;
    /**
     * Add the Auto Close Brackets for Text Editor command
     */
    function addAutoClosingBracketsCommand(commands, settingRegistry, trans, id) {
        commands.addCommand(CommandIDs.autoClosingBrackets, {
            execute: args => {
                var _a;
                config.autoClosingBrackets = !!((_a = args['force']) !== null && _a !== void 0 ? _a : !config.autoClosingBrackets);
                return settingRegistry
                    .set(id, 'editorConfig', config)
                    .catch((reason) => {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                });
            },
            label: trans.__('Auto Close Brackets for Text Editor'),
            isToggled: () => config.autoClosingBrackets
        });
        commands.addCommand(CommandIDs.autoClosingBracketsUniversal, {
            execute: () => {
                const anyToggled = commands.isToggled(CommandIDs.autoClosingBrackets) ||
                    commands.isToggled(autoClosingBracketsNotebook) ||
                    commands.isToggled(autoClosingBracketsConsole);
                // if any auto closing brackets options is toggled, toggle both off
                if (anyToggled) {
                    void commands.execute(CommandIDs.autoClosingBrackets, {
                        force: false
                    });
                    void commands.execute(autoClosingBracketsNotebook, { force: false });
                    void commands.execute(autoClosingBracketsConsole, { force: false });
                }
                else {
                    // both are off, turn them on
                    void commands.execute(CommandIDs.autoClosingBrackets, {
                        force: true
                    });
                    void commands.execute(autoClosingBracketsNotebook, { force: true });
                    void commands.execute(autoClosingBracketsConsole, { force: true });
                }
            },
            label: trans.__('Auto Close Brackets'),
            isToggled: () => commands.isToggled(CommandIDs.autoClosingBrackets) ||
                commands.isToggled(autoClosingBracketsNotebook) ||
                commands.isToggled(autoClosingBracketsConsole)
        });
    }
    Commands.addAutoClosingBracketsCommand = addAutoClosingBracketsCommand;
    /**
     * Add the replace selection for text editor command
     */
    function addReplaceSelectionCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.replaceSelection, {
            execute: args => {
                var _a, _b;
                const text = args['text'] || '';
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                (_b = (_a = widget.content.editor).replaceSelection) === null || _b === void 0 ? void 0 : _b.call(_a, text);
            },
            isEnabled,
            label: trans.__('Replace Selection in Editor')
        });
    }
    Commands.addReplaceSelectionCommand = addReplaceSelectionCommand;
    /**
     * Add the Create Console for Editor command
     */
    function addCreateConsoleCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.createConsole, {
            execute: args => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                return getCreateConsoleFunction(commands)(widget, args);
            },
            isEnabled,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.consoleIcon,
            label: trans.__('Create Console for Editor')
        });
    }
    Commands.addCreateConsoleCommand = addCreateConsoleCommand;
    /**
     * Add the Run Code command
     */
    function addRunCodeCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.runCode, {
            execute: () => {
                var _a;
                // Run the appropriate code, taking into account a ```fenced``` code block.
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                let code = '';
                const editor = widget.editor;
                const path = widget.context.path;
                const extension = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.extname(path);
                const selection = editor.getSelection();
                const { start, end } = selection;
                let selected = start.column !== end.column || start.line !== end.line;
                if (selected) {
                    // Get the selected code from the editor.
                    const start = editor.getOffsetAt(selection.start);
                    const end = editor.getOffsetAt(selection.end);
                    code = editor.model.value.text.substring(start, end);
                }
                else if (_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.MarkdownCodeBlocks.isMarkdown(extension)) {
                    const { text } = editor.model.value;
                    const blocks = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.MarkdownCodeBlocks.findMarkdownCodeBlocks(text);
                    for (const block of blocks) {
                        if (block.startLine <= start.line && start.line <= block.endLine) {
                            code = block.code;
                            selected = true;
                            break;
                        }
                    }
                }
                if (!selected) {
                    // no selection, submit whole line and advance
                    code = editor.getLine(selection.start.line);
                    const cursor = editor.getCursorPosition();
                    if (cursor.line + 1 === editor.lineCount) {
                        const text = editor.model.value.text;
                        editor.model.value.text = text + '\n';
                    }
                    editor.setCursorPosition({
                        line: cursor.line + 1,
                        column: cursor.column
                    });
                }
                const activate = false;
                if (code) {
                    return commands.execute('console:inject', { activate, code, path });
                }
                else {
                    return Promise.resolve(void 0);
                }
            },
            isEnabled,
            label: trans.__('Run Code')
        });
    }
    Commands.addRunCodeCommand = addRunCodeCommand;
    /**
     * Add the Run All Code command
     */
    function addRunAllCodeCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.runAllCode, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                let code = '';
                const editor = widget.editor;
                const text = editor.model.value.text;
                const path = widget.context.path;
                const extension = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.extname(path);
                if (_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.MarkdownCodeBlocks.isMarkdown(extension)) {
                    // For Markdown files, run only code blocks.
                    const blocks = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.MarkdownCodeBlocks.findMarkdownCodeBlocks(text);
                    for (const block of blocks) {
                        code += block.code;
                    }
                }
                else {
                    code = text;
                }
                const activate = false;
                if (code) {
                    return commands.execute('console:inject', { activate, code, path });
                }
                else {
                    return Promise.resolve(void 0);
                }
            },
            isEnabled,
            label: trans.__('Run All Code')
        });
    }
    Commands.addRunAllCodeCommand = addRunAllCodeCommand;
    /**
     * Add markdown preview command
     */
    function addMarkdownPreviewCommand(commands, tracker, trans) {
        commands.addCommand(CommandIDs.markdownPreview, {
            execute: () => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                const path = widget.context.path;
                return commands.execute('markdownviewer:open', {
                    path,
                    options: {
                        mode: 'split-right'
                    }
                });
            },
            isVisible: () => {
                const widget = tracker.currentWidget;
                return ((widget && _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.extname(widget.context.path) === '.md') || false);
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.markdownIcon,
            label: trans.__('Show Markdown Preview')
        });
    }
    Commands.addMarkdownPreviewCommand = addMarkdownPreviewCommand;
    /**
     * Add undo command
     */
    function addUndoCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.undo, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                widget.editor.undo();
            },
            isEnabled: () => {
                var _a;
                if (!isEnabled()) {
                    return false;
                }
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return false;
                }
                // Ideally enable it when there are undo events stored
                // Reference issue #8590: Code mirror editor could expose the history of undo/redo events
                return true;
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.undoIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Undo')
        });
    }
    Commands.addUndoCommand = addUndoCommand;
    /**
     * Add redo command
     */
    function addRedoCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.redo, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                widget.editor.redo();
            },
            isEnabled: () => {
                var _a;
                if (!isEnabled()) {
                    return false;
                }
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return false;
                }
                // Ideally enable it when there are redo events stored
                // Reference issue #8590: Code mirror editor could expose the history of undo/redo events
                return true;
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.redoIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Redo')
        });
    }
    Commands.addRedoCommand = addRedoCommand;
    /**
     * Add cut command
     */
    function addCutCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.cut, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                const editor = widget.editor;
                const text = getTextSelection(editor);
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Clipboard.copyToSystem(text);
                editor.replaceSelection && editor.replaceSelection('');
            },
            isEnabled: () => {
                var _a;
                if (!isEnabled()) {
                    return false;
                }
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return false;
                }
                // Enable command if there is a text selection in the editor
                return isSelected(widget.editor);
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.cutIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Cut')
        });
    }
    Commands.addCutCommand = addCutCommand;
    /**
     * Add copy command
     */
    function addCopyCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.copy, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                const editor = widget.editor;
                const text = getTextSelection(editor);
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Clipboard.copyToSystem(text);
            },
            isEnabled: () => {
                var _a;
                if (!isEnabled()) {
                    return false;
                }
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return false;
                }
                // Enable command if there is a text selection in the editor
                return isSelected(widget.editor);
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.copyIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Copy')
        });
    }
    Commands.addCopyCommand = addCopyCommand;
    /**
     * Add paste command
     */
    function addPasteCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.paste, {
            execute: async () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                const editor = widget.editor;
                // Get data from clipboard
                const clipboard = window.navigator.clipboard;
                const clipboardData = await clipboard.readText();
                if (clipboardData) {
                    // Paste data to the editor
                    editor.replaceSelection && editor.replaceSelection(clipboardData);
                }
            },
            isEnabled: () => { var _a; return Boolean(isEnabled() && ((_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content)); },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.pasteIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Paste')
        });
    }
    Commands.addPasteCommand = addPasteCommand;
    /**
     * Add select all command
     */
    function addSelectAllCommand(commands, tracker, trans, isEnabled) {
        commands.addCommand(CommandIDs.selectAll, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                const editor = widget.editor;
                editor.execCommand('selectAll');
            },
            isEnabled: () => { var _a; return Boolean(isEnabled() && ((_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content)); },
            label: trans.__('Select All')
        });
    }
    Commands.addSelectAllCommand = addSelectAllCommand;
    /**
     * Helper function to check if there is a text selection in the editor
     */
    function isSelected(editor) {
        const selectionObj = editor.getSelection();
        const { start, end } = selectionObj;
        const selected = start.column !== end.column || start.line !== end.line;
        return selected;
    }
    /**
     * Helper function to get text selection from the editor
     */
    function getTextSelection(editor) {
        const selectionObj = editor.getSelection();
        const start = editor.getOffsetAt(selectionObj.start);
        const end = editor.getOffsetAt(selectionObj.end);
        const text = editor.model.value.text.substring(start, end);
        return text;
    }
    /**
     * Function to create a new untitled text file, given the current working directory.
     */
    function createNew(commands, cwd, ext = 'txt') {
        return commands
            .execute('docmanager:new-untitled', {
            path: cwd,
            type: 'file',
            ext
        })
            .then(model => {
            if (model != undefined) {
                return commands.execute('docmanager:open', {
                    path: model.path,
                    factory: FACTORY
                });
            }
        });
    }
    /**
     * Add the New File command
     *
     * Defaults to Text/.txt if file type data is not specified
     */
    function addCreateNewCommand(commands, browserFactory, trans) {
        commands.addCommand(CommandIDs.createNew, {
            label: args => {
                var _a, _b;
                if (args.isPalette) {
                    return (_a = args.paletteLabel) !== null && _a !== void 0 ? _a : trans.__('New Text File');
                }
                return (_b = args.launcherLabel) !== null && _b !== void 0 ? _b : trans.__('Text File');
            },
            caption: args => { var _a; return (_a = args.caption) !== null && _a !== void 0 ? _a : trans.__('Create a new text file'); },
            icon: args => {
                var _a;
                return args.isPalette
                    ? undefined
                    : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon.resolve({
                        icon: (_a = args.iconName) !== null && _a !== void 0 ? _a : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.textEditorIcon
                    });
            },
            execute: args => {
                var _a;
                const cwd = args.cwd || browserFactory.defaultBrowser.model.path;
                return createNew(commands, cwd, (_a = args.fileExt) !== null && _a !== void 0 ? _a : 'txt');
            }
        });
    }
    Commands.addCreateNewCommand = addCreateNewCommand;
    /**
     * Add the New Markdown File command
     */
    function addCreateNewMarkdownCommand(commands, browserFactory, trans) {
        commands.addCommand(CommandIDs.createNewMarkdown, {
            label: args => args['isPalette']
                ? trans.__('New Markdown File')
                : trans.__('Markdown File'),
            caption: trans.__('Create a new markdown file'),
            icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.markdownIcon),
            execute: args => {
                const cwd = args['cwd'] || browserFactory.defaultBrowser.model.path;
                return createNew(commands, cwd, 'md');
            }
        });
    }
    Commands.addCreateNewMarkdownCommand = addCreateNewMarkdownCommand;
    /**
     * Wrapper function for adding the default launcher items for File Editor
     */
    function addLauncherItems(launcher, trans) {
        addCreateNewToLauncher(launcher, trans);
        addCreateNewMarkdownToLauncher(launcher, trans);
    }
    Commands.addLauncherItems = addLauncherItems;
    /**
     * Add Create New Text File to the Launcher
     */
    function addCreateNewToLauncher(launcher, trans) {
        launcher.add({
            command: CommandIDs.createNew,
            category: trans.__('Other'),
            rank: 1
        });
    }
    Commands.addCreateNewToLauncher = addCreateNewToLauncher;
    /**
     * Add Create New Markdown to the Launcher
     */
    function addCreateNewMarkdownToLauncher(launcher, trans) {
        launcher.add({
            command: CommandIDs.createNewMarkdown,
            category: trans.__('Other'),
            rank: 2
        });
    }
    Commands.addCreateNewMarkdownToLauncher = addCreateNewMarkdownToLauncher;
    /**
     * Add ___ File items to the Launcher for common file types associated with available kernels
     */
    function addKernelLanguageLauncherItems(launcher, trans, availableKernelFileTypes) {
        for (let ext of availableKernelFileTypes) {
            launcher.add({
                command: CommandIDs.createNew,
                category: trans.__('Other'),
                rank: 3,
                args: ext
            });
        }
    }
    Commands.addKernelLanguageLauncherItems = addKernelLanguageLauncherItems;
    /**
     * Wrapper function for adding the default items to the File Editor palette
     */
    function addPaletteItems(palette, trans) {
        addChangeTabsCommandsToPalette(palette, trans);
        addCreateNewCommandToPalette(palette, trans);
        addCreateNewMarkdownCommandToPalette(palette, trans);
        addChangeFontSizeCommandsToPalette(palette, trans);
    }
    Commands.addPaletteItems = addPaletteItems;
    /**
     * Add commands to change the tab indentation to the File Editor palette
     */
    function addChangeTabsCommandsToPalette(palette, trans) {
        const paletteCategory = trans.__('Text Editor');
        const args = {
            insertSpaces: false,
            size: 4
        };
        const command = CommandIDs.changeTabs;
        palette.addItem({ command, args, category: paletteCategory });
        for (const size of [1, 2, 4, 8]) {
            const args = {
                insertSpaces: true,
                size
            };
            palette.addItem({ command, args, category: paletteCategory });
        }
    }
    Commands.addChangeTabsCommandsToPalette = addChangeTabsCommandsToPalette;
    /**
     * Add a Create New File command to the File Editor palette
     */
    function addCreateNewCommandToPalette(palette, trans) {
        const paletteCategory = trans.__('Text Editor');
        palette.addItem({
            command: CommandIDs.createNew,
            args: { isPalette: true },
            category: paletteCategory
        });
    }
    Commands.addCreateNewCommandToPalette = addCreateNewCommandToPalette;
    /**
     * Add a Create New Markdown command to the File Editor palette
     */
    function addCreateNewMarkdownCommandToPalette(palette, trans) {
        const paletteCategory = trans.__('Text Editor');
        palette.addItem({
            command: CommandIDs.createNewMarkdown,
            args: { isPalette: true },
            category: paletteCategory
        });
    }
    Commands.addCreateNewMarkdownCommandToPalette = addCreateNewMarkdownCommandToPalette;
    /**
     * Add commands to change the font size to the File Editor palette
     */
    function addChangeFontSizeCommandsToPalette(palette, trans) {
        const paletteCategory = trans.__('Text Editor');
        const command = CommandIDs.changeFontSize;
        let args = { delta: 1 };
        palette.addItem({ command, args, category: paletteCategory });
        args = { delta: -1 };
        palette.addItem({ command, args, category: paletteCategory });
    }
    Commands.addChangeFontSizeCommandsToPalette = addChangeFontSizeCommandsToPalette;
    /**
     * Add New ___ File commands to the File Editor palette for common file types associated with available kernels
     */
    function addKernelLanguagePaletteItems(palette, trans, availableKernelFileTypes) {
        const paletteCategory = trans.__('Text Editor');
        for (let ext of availableKernelFileTypes) {
            palette.addItem({
                command: CommandIDs.createNew,
                args: Object.assign(Object.assign({}, ext), { isPalette: true }),
                category: paletteCategory
            });
        }
    }
    Commands.addKernelLanguagePaletteItems = addKernelLanguagePaletteItems;
    /**
     * Wrapper function for adding the default menu items for File Editor
     */
    function addMenuItems(menu, commands, tracker, trans, consoleTracker, sessionDialogs) {
        // Add undo/redo hooks to the edit menu.
        addUndoRedoToEditMenu(menu, tracker);
        // Add editor view options.
        addEditorViewerToViewMenu(menu, tracker);
        // Add a console creator the the file menu.
        addConsoleCreatorToFileMenu(menu, commands, tracker, trans);
        // Add a code runner to the run menu.
        if (consoleTracker) {
            addCodeRunnersToRunMenu(menu, commands, tracker, consoleTracker, trans, sessionDialogs);
        }
    }
    Commands.addMenuItems = addMenuItems;
    /**
     * Add Create New ___ File commands to the File menu for common file types associated with available kernels
     */
    function addKernelLanguageMenuItems(menu, availableKernelFileTypes) {
        for (let ext of availableKernelFileTypes) {
            menu.fileMenu.newMenu.addItem({
                command: CommandIDs.createNew,
                args: ext,
                rank: 30
            });
        }
    }
    Commands.addKernelLanguageMenuItems = addKernelLanguageMenuItems;
    /**
     * Add File Editor undo and redo widgets to the Edit menu
     */
    function addUndoRedoToEditMenu(menu, tracker) {
        menu.editMenu.undoers.add({
            tracker,
            undo: widget => {
                widget.content.editor.undo();
            },
            redo: widget => {
                widget.content.editor.redo();
            }
        });
    }
    Commands.addUndoRedoToEditMenu = addUndoRedoToEditMenu;
    /**
     * Add a File Editor editor viewer to the View Menu
     */
    function addEditorViewerToViewMenu(menu, tracker) {
        menu.viewMenu.editorViewers.add({
            tracker,
            toggleLineNumbers: widget => {
                const lineNumbers = !widget.content.editor.getOption('lineNumbers');
                widget.content.editor.setOption('lineNumbers', lineNumbers);
            },
            toggleWordWrap: widget => {
                const oldValue = widget.content.editor.getOption('lineWrap');
                const newValue = oldValue === 'off' ? 'on' : 'off';
                widget.content.editor.setOption('lineWrap', newValue);
            },
            toggleMatchBrackets: widget => {
                const matchBrackets = !widget.content.editor.getOption('matchBrackets');
                widget.content.editor.setOption('matchBrackets', matchBrackets);
            },
            lineNumbersToggled: widget => widget.content.editor.getOption('lineNumbers'),
            wordWrapToggled: widget => widget.content.editor.getOption('lineWrap') !== 'off',
            matchBracketsToggled: widget => widget.content.editor.getOption('matchBrackets')
        });
    }
    Commands.addEditorViewerToViewMenu = addEditorViewerToViewMenu;
    /**
     * Add a File Editor console creator to the File menu
     */
    function addConsoleCreatorToFileMenu(menu, commands, tracker, trans) {
        const createConsole = getCreateConsoleFunction(commands);
        menu.fileMenu.consoleCreators.add({
            tracker,
            createConsoleLabel: (n) => trans.__('Create Console for Editor'),
            createConsole
        });
    }
    Commands.addConsoleCreatorToFileMenu = addConsoleCreatorToFileMenu;
    /**
     * Add a File Editor code runner to the Run menu
     */
    function addCodeRunnersToRunMenu(menu, commands, tracker, consoleTracker, trans, sessionDialogs) {
        menu.runMenu.codeRunners.add({
            tracker,
            runLabel: (n) => trans.__('Run Code'),
            runAllLabel: (n) => trans.__('Run All Code'),
            restartAndRunAllLabel: (n) => trans.__('Restart Kernel and Run All Code'),
            isEnabled: current => !!consoleTracker.find(widget => { var _a; return ((_a = widget.sessionContext.session) === null || _a === void 0 ? void 0 : _a.path) === current.context.path; }),
            run: () => commands.execute(CommandIDs.runCode),
            runAll: () => commands.execute(CommandIDs.runAllCode),
            restartAndRunAll: current => {
                const widget = consoleTracker.find(widget => { var _a; return ((_a = widget.sessionContext.session) === null || _a === void 0 ? void 0 : _a.path) === current.context.path; });
                if (widget) {
                    return (sessionDialogs || _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.sessionContextDialogs)
                        .restart(widget.sessionContext)
                        .then(restarted => {
                        if (restarted) {
                            void commands.execute(CommandIDs.runAllCode);
                        }
                        return restarted;
                    });
                }
            }
        });
    }
    Commands.addCodeRunnersToRunMenu = addCodeRunnersToRunMenu;
})(Commands || (Commands = {}));


/***/ }),

/***/ "../packages/fileeditor-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/fileeditor-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Commands": () => (/* reexport safe */ _commands__WEBPACK_IMPORTED_MODULE_12__.Commands),
/* harmony export */   "tabSpaceStatus": () => (/* binding */ tabSpaceStatus),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./commands */ "../packages/fileeditor-extension/lib/commands.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module fileeditor-extension
 */














/**
 * The editor tracker extension.
 */
const plugin = {
    activate,
    id: '@jupyterlab/fileeditor-extension:plugin',
    requires: [
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__.ISettingRegistry,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.ITranslator
    ],
    optional: [
        _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__.IConsoleTracker,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__.ILauncher,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7__.IMainMenu,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs
    ],
    provides: _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_5__.IEditorTracker,
    autoStart: true
};
/**
 * A plugin that provides a status item allowing the user to
 * switch tabs vs spaces and tab widths for text editors.
 */
const tabSpaceStatus = {
    id: '@jupyterlab/fileeditor-extension:tab-space-status',
    autoStart: true,
    requires: [_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_5__.IEditorTracker, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.ITranslator],
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_9__.IStatusBar],
    activate: (app, editorTracker, settingRegistry, translator, statusBar) => {
        const trans = translator.load('jupyterlab');
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        // Create a menu for switching tabs vs spaces.
        const menu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_11__.Menu({ commands: app.commands });
        const command = 'fileeditor:change-tabs';
        const { shell } = app;
        const args = {
            insertSpaces: false,
            size: 4,
            name: trans.__('Indent with Tab')
        };
        menu.addItem({ command, args });
        for (const size of [1, 2, 4, 8]) {
            const args = {
                insertSpaces: true,
                size,
                name: trans._n('Spaces: %1', 'Spaces: %1', size)
            };
            menu.addItem({ command, args });
        }
        // Create the status item.
        const item = new _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_5__.TabSpaceStatus({ menu, translator });
        // Keep a reference to the code editor config from the settings system.
        const updateSettings = (settings) => {
            item.model.config = Object.assign(Object.assign({}, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.CodeEditor.defaultConfig), settings.get('editorConfig').composite);
        };
        void Promise.all([
            settingRegistry.load('@jupyterlab/fileeditor-extension:plugin'),
            app.restored
        ]).then(([settings]) => {
            updateSettings(settings);
            settings.changed.connect(updateSettings);
        });
        // Add the status item.
        statusBar.registerStatusItem('@jupyterlab/fileeditor-extension:tab-space-status', {
            item,
            align: 'right',
            rank: 1,
            isActive: () => {
                return (!!shell.currentWidget && editorTracker.has(shell.currentWidget));
            }
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [plugin, tabSpaceStatus];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * Activate the editor tracker plugin.
 */
function activate(app, editorServices, browserFactory, settingRegistry, translator, consoleTracker, palette, launcher, menu, restorer, sessionDialogs) {
    const id = plugin.id;
    const trans = translator.load('jupyterlab');
    const namespace = 'editor';
    const factory = new _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_5__.FileEditorFactory({
        editorServices,
        factoryOptions: {
            name: _commands__WEBPACK_IMPORTED_MODULE_12__.FACTORY,
            fileTypes: ['markdown', '*'],
            defaultFor: ['markdown', '*'] // it outranks the defaultRendered viewer.
        }
    });
    const { commands, restored, shell } = app;
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    const isEnabled = () => tracker.currentWidget !== null &&
        tracker.currentWidget === shell.currentWidget;
    const commonLanguageFileTypeData = new Map([
        [
            'python',
            [
                {
                    fileExt: 'py',
                    iconName: 'ui-components:python',
                    launcherLabel: trans.__('Python File'),
                    paletteLabel: trans.__('New Python File'),
                    caption: trans.__('Create a new Python file')
                }
            ]
        ],
        [
            'julia',
            [
                {
                    fileExt: 'jl',
                    iconName: 'ui-components:julia',
                    launcherLabel: trans.__('Julia File'),
                    paletteLabel: trans.__('New Julia File'),
                    caption: trans.__('Create a new Julia file')
                }
            ]
        ],
        [
            'R',
            [
                {
                    fileExt: 'r',
                    iconName: 'ui-components:r-kernel',
                    launcherLabel: trans.__('R File'),
                    paletteLabel: trans.__('New R File'),
                    caption: trans.__('Create a new R file')
                }
            ]
        ]
    ]);
    // Use available kernels to determine which common file types should have 'Create New' options in the Launcher, File Editor palette, and File menu
    const getAvailableKernelFileTypes = async () => {
        var _a, _b;
        const specsManager = app.serviceManager.kernelspecs;
        await specsManager.ready;
        let fileTypes = new Set();
        const specs = (_b = (_a = specsManager.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs) !== null && _b !== void 0 ? _b : {};
        Object.keys(specs).forEach(spec => {
            const specModel = specs[spec];
            if (specModel) {
                const exts = commonLanguageFileTypeData.get(specModel.language);
                exts === null || exts === void 0 ? void 0 : exts.forEach(ext => fileTypes.add(ext));
            }
        });
        return fileTypes;
    };
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: _commands__WEBPACK_IMPORTED_MODULE_12__.FACTORY }),
            name: widget => widget.context.path
        });
    }
    // Add a console creator to the File menu
    // Fetch the initial state of the settings.
    Promise.all([settingRegistry.load(id), restored])
        .then(([settings]) => {
        _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.updateSettings(settings, commands);
        _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.updateTracker(tracker);
        settings.changed.connect(() => {
            _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.updateSettings(settings, commands);
            _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.updateTracker(tracker);
        });
    })
        .catch((reason) => {
        console.error(reason.message);
        _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.updateTracker(tracker);
    });
    factory.widgetCreated.connect((sender, widget) => {
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        void tracker.add(widget);
        _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.updateWidget(widget.content);
    });
    app.docRegistry.addWidgetFactory(factory);
    // Handle the settings of new widgets.
    tracker.widgetAdded.connect((sender, widget) => {
        _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.updateWidget(widget.content);
    });
    _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.addCommands(commands, settingRegistry, trans, id, isEnabled, tracker, browserFactory);
    // Add a launcher item if the launcher is available.
    if (launcher) {
        _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.addLauncherItems(launcher, trans);
    }
    if (palette) {
        _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.addPaletteItems(palette, trans);
    }
    if (menu) {
        _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.addMenuItems(menu, commands, tracker, trans, consoleTracker, sessionDialogs);
    }
    getAvailableKernelFileTypes()
        .then(availableKernelFileTypes => {
        if (launcher) {
            _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.addKernelLanguageLauncherItems(launcher, trans, availableKernelFileTypes);
        }
        if (palette) {
            _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.addKernelLanguagePaletteItems(palette, trans, availableKernelFileTypes);
        }
        if (menu) {
            _commands__WEBPACK_IMPORTED_MODULE_12__.Commands.addKernelLanguageMenuItems(menu, availableKernelFileTypes);
        }
    })
        .catch((reason) => {
        console.error(reason.message);
    });
    return tracker;
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZmlsZWVkaXRvci1leHRlbnNpb24vc3JjL2NvbW1hbmRzLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9maWxlZWRpdG9yLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBUTdCO0FBQ3NCO0FBR2dCO0FBd0JqQztBQVFuQyxNQUFNLDJCQUEyQixHQUFHLHNDQUFzQyxDQUFDO0FBQzNFLE1BQU0sMEJBQTBCLEdBQUcscUNBQXFDLENBQUM7QUFDekU7O0dBRUc7QUFDSSxJQUFVLFVBQVUsQ0F5QzFCO0FBekNELFdBQWlCLFVBQVU7SUFDWixvQkFBUyxHQUFHLHVCQUF1QixDQUFDO0lBRXBDLDRCQUFpQixHQUFHLHFDQUFxQyxDQUFDO0lBRTFELHlCQUFjLEdBQUcsNkJBQTZCLENBQUM7SUFFL0Msc0JBQVcsR0FBRyxnQ0FBZ0MsQ0FBQztJQUUvQyxtQkFBUSxHQUFHLDZCQUE2QixDQUFDO0lBRXpDLHFCQUFVLEdBQUcsd0JBQXdCLENBQUM7SUFFdEMsd0JBQWEsR0FBRyxrQ0FBa0MsQ0FBQztJQUVuRCw4QkFBbUIsR0FBRyx3Q0FBd0MsQ0FBQztJQUUvRCx1Q0FBNEIsR0FDdkMsa0RBQWtELENBQUM7SUFFeEMsd0JBQWEsR0FBRywyQkFBMkIsQ0FBQztJQUU1QywyQkFBZ0IsR0FBRyw4QkFBOEIsQ0FBQztJQUVsRCxrQkFBTyxHQUFHLHFCQUFxQixDQUFDO0lBRWhDLHFCQUFVLEdBQUcsb0JBQW9CLENBQUM7SUFFbEMsMEJBQWUsR0FBRyw2QkFBNkIsQ0FBQztJQUVoRCxlQUFJLEdBQUcsaUJBQWlCLENBQUM7SUFFekIsZUFBSSxHQUFHLGlCQUFpQixDQUFDO0lBRXpCLGNBQUcsR0FBRyxnQkFBZ0IsQ0FBQztJQUV2QixlQUFJLEdBQUcsaUJBQWlCLENBQUM7SUFFekIsZ0JBQUssR0FBRyxrQkFBa0IsQ0FBQztJQUUzQixvQkFBUyxHQUFHLHVCQUF1QixDQUFDO0FBQ25ELENBQUMsRUF6Q2dCLFVBQVUsS0FBVixVQUFVLFFBeUMxQjtBQVVEOztHQUVHO0FBQ0ksTUFBTSxPQUFPLEdBQUcsUUFBUSxDQUFDO0FBRWhDLE1BQU0sWUFBWSxHQUFHO0lBQ25CLHFCQUFxQjtJQUNyQixpQkFBaUI7SUFDakIsWUFBWTtJQUNaLFVBQVU7SUFDVixZQUFZO0lBQ1osYUFBYTtJQUNiLFVBQVU7SUFDVixlQUFlO0lBQ2YsVUFBVTtJQUNWLGNBQWM7SUFDZCxTQUFTO0lBQ1QsZ0JBQWdCO0lBQ2hCLFFBQVE7SUFDUixhQUFhO0NBQ2QsQ0FBQztBQUVGLFNBQVMsa0JBQWtCLENBQUMsTUFBMEI7SUFDcEQsTUFBTSxjQUFjLHFCQUFRLE1BQU0sQ0FBRSxDQUFDO0lBQ3JDLDRFQUE0RTtJQUM1RSxLQUFLLElBQUksQ0FBQyxJQUFJLE1BQU0sQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLEVBQUU7UUFDakMsSUFBSSxDQUFDLFlBQVksQ0FBQyxRQUFRLENBQUMsQ0FBQyxDQUFDLEVBQUU7WUFDN0IsT0FBUSxNQUFjLENBQUMsQ0FBQyxDQUFDLENBQUM7U0FDM0I7S0FDRjtJQUNELE9BQU8sY0FBYyxDQUFDO0FBQ3hCLENBQUM7QUFFRCxJQUFJLE1BQU0sR0FBdUIsa0JBQWtCLENBQUMsNEVBQXdCLENBQUMsQ0FBQztBQUU5RTs7O0dBR0c7QUFDSSxJQUFVLFFBQVEsQ0E4cEN4QjtBQTlwQ0QsV0FBaUIsUUFBUTtJQUN2Qjs7T0FFRztJQUNILFNBQVMsd0JBQXdCLENBQy9CLFFBQXlCO1FBS3pCLE9BQU8sS0FBSyxVQUFVLGFBQWEsQ0FDakMsTUFBbUMsRUFDbkMsSUFBZ0M7O1lBRWhDLE1BQU0sT0FBTyxHQUFHLElBQUksSUFBSSxFQUFFLENBQUM7WUFDM0IsTUFBTSxPQUFPLEdBQUcsTUFBTSxRQUFRLENBQUMsT0FBTyxDQUFDLGdCQUFnQixFQUFFO2dCQUN2RCxRQUFRLEVBQUUsT0FBTyxDQUFDLFVBQVUsQ0FBQztnQkFDN0IsSUFBSSxRQUFFLE1BQU0sQ0FBQyxPQUFPLENBQUMsYUFBYSwwQ0FBRSxJQUFJO2dCQUN4QyxJQUFJLEVBQUUsTUFBTSxDQUFDLE9BQU8sQ0FBQyxJQUFJO2dCQUN6QixpQkFBaUIsRUFBRSxNQUFNLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxxQkFBcUI7Z0JBQzdELEdBQUcsRUFBRSxNQUFNLENBQUMsRUFBRTtnQkFDZCxVQUFVLEVBQUUsY0FBYzthQUMzQixDQUFDLENBQUM7WUFFSCxNQUFNLENBQUMsT0FBTyxDQUFDLFdBQVcsQ0FBQyxPQUFPLENBQUMsQ0FBQyxNQUFNLEVBQUUsS0FBSyxFQUFFLEVBQUU7O2dCQUNuRCxPQUFPLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxLQUFLLENBQUMsQ0FBQztnQkFDL0IsT0FBTyxDQUFDLE9BQU8sQ0FBQyxPQUFPLE9BQUMsTUFBTSxDQUFDLE9BQU8sQ0FBQyxhQUFhLDBDQUFFLElBQUksQ0FBQyxDQUFDO1lBQzlELENBQUMsQ0FBQyxDQUFDO1FBQ0wsQ0FBQyxDQUFDO0lBQ0osQ0FBQztJQUVEOztPQUVHO0lBQ0gsU0FBZ0IsY0FBYyxDQUM1QixRQUFvQyxFQUNwQyxRQUF5QjtRQUV6QixNQUFNLEdBQUcsa0JBQWtCLGlDQUN0Qiw0RUFBd0IsR0FDdkIsUUFBUSxDQUFDLEdBQUcsQ0FBQyxjQUFjLENBQUMsQ0FBQyxTQUF3QixFQUN6RCxDQUFDO1FBRUgsNkNBQTZDO1FBQzdDLFFBQVEsQ0FBQyxvQkFBb0IsRUFBRSxDQUFDO0lBQ2xDLENBQUM7SUFYZSx1QkFBYyxpQkFXN0I7SUFFRDs7T0FFRztJQUNILFNBQWdCLGFBQWEsQ0FDM0IsT0FBbUQ7UUFFbkQsT0FBTyxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsRUFBRTtZQUN2QixZQUFZLENBQUMsTUFBTSxDQUFDLE9BQU8sQ0FBQyxDQUFDO1FBQy9CLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQU5lLHNCQUFhLGdCQU01QjtJQUVEOzs7T0FHRztJQUNILFNBQWdCLFlBQVksQ0FBQyxNQUFrQjtRQUM3QyxNQUFNLE1BQU0sR0FBRyxNQUFNLENBQUMsTUFBTSxDQUFDO1FBQzdCLElBQUksYUFBYSxHQUFRLEVBQUUsQ0FBQztRQUM1QixNQUFNLENBQUMsSUFBSSxDQUFDLE1BQU0sQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDLEdBQTZCLEVBQUUsRUFBRTtZQUM1RCxhQUFhLENBQUMsR0FBRyxDQUFDLEdBQUcsTUFBTSxDQUFDLEdBQUcsQ0FBQyxDQUFDO1FBQ25DLENBQUMsQ0FBQyxDQUFDO1FBQ0gsTUFBTSxDQUFDLFVBQVUsQ0FBQyxhQUFhLENBQUMsQ0FBQztJQUNuQyxDQUFDO0lBUGUscUJBQVksZUFPM0I7SUFFRDs7T0FFRztJQUNILFNBQWdCLFdBQVcsQ0FDekIsUUFBeUIsRUFDekIsZUFBaUMsRUFDakMsS0FBd0IsRUFDeEIsRUFBVSxFQUNWLFNBQXdCLEVBQ3hCLE9BQW1ELEVBQ25ELGNBQW1DO1FBRW5DLHFDQUFxQztRQUNyQyx3QkFBd0IsQ0FBQyxRQUFRLEVBQUUsZUFBZSxFQUFFLEtBQUssRUFBRSxFQUFFLENBQUMsQ0FBQztRQUUvRCxxQkFBcUIsQ0FBQyxRQUFRLEVBQUUsZUFBZSxFQUFFLEtBQUssRUFBRSxFQUFFLEVBQUUsU0FBUyxDQUFDLENBQUM7UUFFdkUsa0JBQWtCLENBQUMsUUFBUSxFQUFFLGVBQWUsRUFBRSxLQUFLLEVBQUUsRUFBRSxFQUFFLFNBQVMsQ0FBQyxDQUFDO1FBRXBFLG9CQUFvQixDQUFDLFFBQVEsRUFBRSxlQUFlLEVBQUUsS0FBSyxFQUFFLEVBQUUsQ0FBQyxDQUFDO1FBRTNELHVCQUF1QixDQUFDLFFBQVEsRUFBRSxlQUFlLEVBQUUsS0FBSyxFQUFFLEVBQUUsRUFBRSxTQUFTLENBQUMsQ0FBQztRQUV6RSw2QkFBNkIsQ0FBQyxRQUFRLEVBQUUsZUFBZSxFQUFFLEtBQUssRUFBRSxFQUFFLENBQUMsQ0FBQztRQUVwRSwwQkFBMEIsQ0FBQyxRQUFRLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxTQUFTLENBQUMsQ0FBQztRQUVoRSx1QkFBdUIsQ0FBQyxRQUFRLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxTQUFTLENBQUMsQ0FBQztRQUU3RCxpQkFBaUIsQ0FBQyxRQUFRLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxTQUFTLENBQUMsQ0FBQztRQUV2RCxvQkFBb0IsQ0FBQyxRQUFRLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxTQUFTLENBQUMsQ0FBQztRQUUxRCx5QkFBeUIsQ0FBQyxRQUFRLEVBQUUsT0FBTyxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBRXBELDhDQUE4QztRQUM5QyxtQkFBbUIsQ0FBQyxRQUFRLEVBQUUsY0FBYyxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBRXJELGtEQUFrRDtRQUNsRCwyQkFBMkIsQ0FBQyxRQUFRLEVBQUUsY0FBYyxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBRTdELGNBQWMsQ0FBQyxRQUFRLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxTQUFTLENBQUMsQ0FBQztRQUVwRCxjQUFjLENBQUMsUUFBUSxFQUFFLE9BQU8sRUFBRSxLQUFLLEVBQUUsU0FBUyxDQUFDLENBQUM7UUFFcEQsYUFBYSxDQUFDLFFBQVEsRUFBRSxPQUFPLEVBQUUsS0FBSyxFQUFFLFNBQVMsQ0FBQyxDQUFDO1FBRW5ELGNBQWMsQ0FBQyxRQUFRLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxTQUFTLENBQUMsQ0FBQztRQUVwRCxlQUFlLENBQUMsUUFBUSxFQUFFLE9BQU8sRUFBRSxLQUFLLEVBQUUsU0FBUyxDQUFDLENBQUM7UUFFckQsbUJBQW1CLENBQUMsUUFBUSxFQUFFLE9BQU8sRUFBRSxLQUFLLEVBQUUsU0FBUyxDQUFDLENBQUM7SUFDM0QsQ0FBQztJQWpEZSxvQkFBVyxjQWlEMUI7SUFFRDs7T0FFRztJQUNILFNBQWdCLHdCQUF3QixDQUN0QyxRQUF5QixFQUN6QixlQUFpQyxFQUNqQyxLQUF3QixFQUN4QixFQUFVO1FBRVYsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsY0FBYyxFQUFFO1lBQzdDLE9BQU8sRUFBRSxJQUFJLENBQUMsRUFBRTtnQkFDZCxNQUFNLEtBQUssR0FBRyxNQUFNLENBQUMsSUFBSSxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUM7Z0JBQ3BDLElBQUksTUFBTSxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUMsRUFBRTtvQkFDdkIsT0FBTyxDQUFDLEtBQUssQ0FDWCxHQUFHLFVBQVUsQ0FBQyxjQUFjLDhCQUE4QixDQUMzRCxDQUFDO29CQUNGLE9BQU87aUJBQ1I7Z0JBQ0QsTUFBTSxLQUFLLEdBQUcsTUFBTSxDQUFDLGdCQUFnQixDQUFDLFFBQVEsQ0FBQyxlQUFlLENBQUMsQ0FBQztnQkFDaEUsTUFBTSxPQUFPLEdBQUcsUUFBUSxDQUN0QixLQUFLLENBQUMsZ0JBQWdCLENBQUMscUJBQXFCLENBQUMsRUFDN0MsRUFBRSxDQUNILENBQUM7Z0JBQ0YsTUFBTSxXQUFXLEdBQUcsTUFBTSxDQUFDLFFBQVEsSUFBSSxPQUFPLENBQUM7Z0JBQy9DLE1BQU0sQ0FBQyxRQUFRLEdBQUcsV0FBVyxHQUFHLEtBQUssQ0FBQztnQkFDdEMsT0FBTyxlQUFlO3FCQUNuQixHQUFHLENBQUMsRUFBRSxFQUFFLGNBQWMsRUFBRyxNQUFnQyxDQUFDO3FCQUMxRCxLQUFLLENBQUMsQ0FBQyxNQUFhLEVBQUUsRUFBRTtvQkFDdkIsT0FBTyxDQUFDLEtBQUssQ0FBQyxpQkFBaUIsRUFBRSxLQUFLLE1BQU0sQ0FBQyxPQUFPLEVBQUUsQ0FBQyxDQUFDO2dCQUMxRCxDQUFDLENBQUMsQ0FBQztZQUNQLENBQUM7WUFDRCxLQUFLLEVBQUUsSUFBSSxDQUFDLEVBQUU7O2dCQUNaLElBQUksT0FBQyxJQUFJLENBQUMsS0FBSyxtQ0FBSSxDQUFDLENBQUMsR0FBRyxDQUFDLEVBQUU7b0JBQ3pCLE9BQU8sSUFBSSxDQUFDLE1BQU07d0JBQ2hCLENBQUMsQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUFDLGdDQUFnQyxDQUFDO3dCQUM1QyxDQUFDLENBQUMsS0FBSyxDQUFDLEVBQUUsQ0FBQyxvQkFBb0IsQ0FBQyxDQUFDO2lCQUNwQztxQkFBTTtvQkFDTCxPQUFPLElBQUksQ0FBQyxNQUFNO3dCQUNoQixDQUFDLENBQUMsS0FBSyxDQUFDLEVBQUUsQ0FBQyxnQ0FBZ0MsQ0FBQzt3QkFDNUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsb0JBQW9CLENBQUMsQ0FBQztpQkFDcEM7WUFDSCxDQUFDO1NBQ0YsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQXhDZSxpQ0FBd0IsMkJBd0N2QztJQUVEOztPQUVHO0lBQ0gsU0FBZ0IscUJBQXFCLENBQ25DLFFBQXlCLEVBQ3pCLGVBQWlDLEVBQ2pDLEtBQXdCLEVBQ3hCLEVBQVUsRUFDVixTQUF3QjtRQUV4QixRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxXQUFXLEVBQUU7WUFDMUMsT0FBTyxFQUFFLEdBQUcsRUFBRTtnQkFDWixNQUFNLENBQUMsV0FBVyxHQUFHLENBQUMsTUFBTSxDQUFDLFdBQVcsQ0FBQztnQkFDekMsT0FBTyxlQUFlO3FCQUNuQixHQUFHLENBQUMsRUFBRSxFQUFFLGNBQWMsRUFBRyxNQUFnQyxDQUFDO3FCQUMxRCxLQUFLLENBQUMsQ0FBQyxNQUFhLEVBQUUsRUFBRTtvQkFDdkIsT0FBTyxDQUFDLEtBQUssQ0FBQyxpQkFBaUIsRUFBRSxLQUFLLE1BQU0sQ0FBQyxPQUFPLEVBQUUsQ0FBQyxDQUFDO2dCQUMxRCxDQUFDLENBQUMsQ0FBQztZQUNQLENBQUM7WUFDRCxTQUFTO1lBQ1QsU0FBUyxFQUFFLEdBQUcsRUFBRSxDQUFDLE1BQU0sQ0FBQyxXQUFXO1lBQ25DLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGNBQWMsQ0FBQztTQUNoQyxDQUFDLENBQUM7SUFDTCxDQUFDO0lBcEJlLDhCQUFxQix3QkFvQnBDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQixrQkFBa0IsQ0FDaEMsUUFBeUIsRUFDekIsZUFBaUMsRUFDakMsS0FBd0IsRUFDeEIsRUFBVSxFQUNWLFNBQXdCO1FBSXhCLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLFFBQVEsRUFBRTtZQUN2QyxPQUFPLEVBQUUsSUFBSSxDQUFDLEVBQUU7Z0JBQ2QsTUFBTSxDQUFDLFFBQVEsR0FBSSxJQUFJLENBQUMsTUFBTSxDQUFrQixJQUFJLEtBQUssQ0FBQztnQkFDMUQsT0FBTyxlQUFlO3FCQUNuQixHQUFHLENBQUMsRUFBRSxFQUFFLGNBQWMsRUFBRyxNQUFnQyxDQUFDO3FCQUMxRCxLQUFLLENBQUMsQ0FBQyxNQUFhLEVBQUUsRUFBRTtvQkFDdkIsT0FBTyxDQUFDLEtBQUssQ0FBQyxpQkFBaUIsRUFBRSxLQUFLLE1BQU0sQ0FBQyxPQUFPLEVBQUUsQ0FBQyxDQUFDO2dCQUMxRCxDQUFDLENBQUMsQ0FBQztZQUNQLENBQUM7WUFDRCxTQUFTO1lBQ1QsU0FBUyxFQUFFLElBQUksQ0FBQyxFQUFFO2dCQUNoQixNQUFNLFFBQVEsR0FBSSxJQUFJLENBQUMsTUFBTSxDQUFrQixJQUFJLEtBQUssQ0FBQztnQkFDekQsT0FBTyxNQUFNLENBQUMsUUFBUSxLQUFLLFFBQVEsQ0FBQztZQUN0QyxDQUFDO1lBQ0QsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsV0FBVyxDQUFDO1NBQzdCLENBQUMsQ0FBQztJQUNMLENBQUM7SUF6QmUsMkJBQWtCLHFCQXlCakM7SUFFRDs7T0FFRztJQUNILFNBQWdCLG9CQUFvQixDQUNsQyxRQUF5QixFQUN6QixlQUFpQyxFQUNqQyxLQUF3QixFQUN4QixFQUFVO1FBRVYsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsVUFBVSxFQUFFO1lBQ3pDLEtBQUssRUFBRSxJQUFJLENBQUMsRUFBRTs7Z0JBQ1osSUFBSSxJQUFJLENBQUMsWUFBWSxFQUFFO29CQUNyQixPQUFPLEtBQUssQ0FBQyxFQUFFLENBQ2IsWUFBWSxFQUNaLFlBQVksUUFDWCxJQUFJLENBQUMsSUFBZSxtQ0FBSSxDQUFDLENBQzNCLENBQUM7aUJBQ0g7cUJBQU07b0JBQ0wsT0FBTyxLQUFLLENBQUMsRUFBRSxDQUFDLGlCQUFpQixDQUFDLENBQUM7aUJBQ3BDO1lBQ0gsQ0FBQztZQUNELE9BQU8sRUFBRSxJQUFJLENBQUMsRUFBRTtnQkFDZCxNQUFNLENBQUMsT0FBTyxHQUFJLElBQUksQ0FBQyxNQUFNLENBQVksSUFBSSxDQUFDLENBQUM7Z0JBQy9DLE1BQU0sQ0FBQyxZQUFZLEdBQUcsQ0FBQyxDQUFDLElBQUksQ0FBQyxjQUFjLENBQUMsQ0FBQztnQkFDN0MsT0FBTyxlQUFlO3FCQUNuQixHQUFHLENBQUMsRUFBRSxFQUFFLGNBQWMsRUFBRyxNQUFnQyxDQUFDO3FCQUMxRCxLQUFLLENBQUMsQ0FBQyxNQUFhLEVBQUUsRUFBRTtvQkFDdkIsT0FBTyxDQUFDLEtBQUssQ0FBQyxpQkFBaUIsRUFBRSxLQUFLLE1BQU0sQ0FBQyxPQUFPLEVBQUUsQ0FBQyxDQUFDO2dCQUMxRCxDQUFDLENBQUMsQ0FBQztZQUNQLENBQUM7WUFDRCxTQUFTLEVBQUUsSUFBSSxDQUFDLEVBQUU7Z0JBQ2hCLE1BQU0sWUFBWSxHQUFHLENBQUMsQ0FBQyxJQUFJLENBQUMsY0FBYyxDQUFDLENBQUM7Z0JBQzVDLE1BQU0sSUFBSSxHQUFJLElBQUksQ0FBQyxNQUFNLENBQVksSUFBSSxDQUFDLENBQUM7Z0JBQzNDLE9BQU8sTUFBTSxDQUFDLFlBQVksS0FBSyxZQUFZLElBQUksTUFBTSxDQUFDLE9BQU8sS0FBSyxJQUFJLENBQUM7WUFDekUsQ0FBQztTQUNGLENBQUMsQ0FBQztJQUNMLENBQUM7SUFqQ2UsNkJBQW9CLHVCQWlDbkM7SUFFRDs7T0FFRztJQUNILFNBQWdCLHVCQUF1QixDQUNyQyxRQUF5QixFQUN6QixlQUFpQyxFQUNqQyxLQUF3QixFQUN4QixFQUFVLEVBQ1YsU0FBd0I7UUFFeEIsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsYUFBYSxFQUFFO1lBQzVDLE9BQU8sRUFBRSxHQUFHLEVBQUU7Z0JBQ1osTUFBTSxDQUFDLGFBQWEsR0FBRyxDQUFDLE1BQU0sQ0FBQyxhQUFhLENBQUM7Z0JBQzdDLE9BQU8sZUFBZTtxQkFDbkIsR0FBRyxDQUFDLEVBQUUsRUFBRSxjQUFjLEVBQUcsTUFBZ0MsQ0FBQztxQkFDMUQsS0FBSyxDQUFDLENBQUMsTUFBYSxFQUFFLEVBQUU7b0JBQ3ZCLE9BQU8sQ0FBQyxLQUFLLENBQUMsaUJBQWlCLEVBQUUsS0FBSyxNQUFNLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztnQkFDMUQsQ0FBQyxDQUFDLENBQUM7WUFDUCxDQUFDO1lBQ0QsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsZ0JBQWdCLENBQUM7WUFDakMsU0FBUztZQUNULFNBQVMsRUFBRSxHQUFHLEVBQUUsQ0FBQyxNQUFNLENBQUMsYUFBYTtTQUN0QyxDQUFDLENBQUM7SUFDTCxDQUFDO0lBcEJlLGdDQUF1QiwwQkFvQnRDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQiw2QkFBNkIsQ0FDM0MsUUFBeUIsRUFDekIsZUFBaUMsRUFDakMsS0FBd0IsRUFDeEIsRUFBVTtRQUVWLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLG1CQUFtQixFQUFFO1lBQ2xELE9BQU8sRUFBRSxJQUFJLENBQUMsRUFBRTs7Z0JBQ2QsTUFBTSxDQUFDLG1CQUFtQixHQUFHLENBQUMsQ0FBQyxPQUM3QixJQUFJLENBQUMsT0FBTyxDQUFDLG1DQUFJLENBQUMsTUFBTSxDQUFDLG1CQUFtQixDQUM3QyxDQUFDO2dCQUNGLE9BQU8sZUFBZTtxQkFDbkIsR0FBRyxDQUFDLEVBQUUsRUFBRSxjQUFjLEVBQUcsTUFBZ0MsQ0FBQztxQkFDMUQsS0FBSyxDQUFDLENBQUMsTUFBYSxFQUFFLEVBQUU7b0JBQ3ZCLE9BQU8sQ0FBQyxLQUFLLENBQUMsaUJBQWlCLEVBQUUsS0FBSyxNQUFNLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztnQkFDMUQsQ0FBQyxDQUFDLENBQUM7WUFDUCxDQUFDO1lBQ0QsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMscUNBQXFDLENBQUM7WUFDdEQsU0FBUyxFQUFFLEdBQUcsRUFBRSxDQUFDLE1BQU0sQ0FBQyxtQkFBbUI7U0FDNUMsQ0FBQyxDQUFDO1FBRUgsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsNEJBQTRCLEVBQUU7WUFDM0QsT0FBTyxFQUFFLEdBQUcsRUFBRTtnQkFDWixNQUFNLFVBQVUsR0FDZCxRQUFRLENBQUMsU0FBUyxDQUFDLFVBQVUsQ0FBQyxtQkFBbUIsQ0FBQztvQkFDbEQsUUFBUSxDQUFDLFNBQVMsQ0FBQywyQkFBMkIsQ0FBQztvQkFDL0MsUUFBUSxDQUFDLFNBQVMsQ0FBQywwQkFBMEIsQ0FBQyxDQUFDO2dCQUNqRCxtRUFBbUU7Z0JBQ25FLElBQUksVUFBVSxFQUFFO29CQUNkLEtBQUssUUFBUSxDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUMsbUJBQW1CLEVBQUU7d0JBQ3BELEtBQUssRUFBRSxLQUFLO3FCQUNiLENBQUMsQ0FBQztvQkFDSCxLQUFLLFFBQVEsQ0FBQyxPQUFPLENBQUMsMkJBQTJCLEVBQUUsRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLENBQUMsQ0FBQztvQkFDckUsS0FBSyxRQUFRLENBQUMsT0FBTyxDQUFDLDBCQUEwQixFQUFFLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxDQUFDLENBQUM7aUJBQ3JFO3FCQUFNO29CQUNMLDZCQUE2QjtvQkFDN0IsS0FBSyxRQUFRLENBQUMsT0FBTyxDQUFDLFVBQVUsQ0FBQyxtQkFBbUIsRUFBRTt3QkFDcEQsS0FBSyxFQUFFLElBQUk7cUJBQ1osQ0FBQyxDQUFDO29CQUNILEtBQUssUUFBUSxDQUFDLE9BQU8sQ0FBQywyQkFBMkIsRUFBRSxFQUFFLEtBQUssRUFBRSxJQUFJLEVBQUUsQ0FBQyxDQUFDO29CQUNwRSxLQUFLLFFBQVEsQ0FBQyxPQUFPLENBQUMsMEJBQTBCLEVBQUUsRUFBRSxLQUFLLEVBQUUsSUFBSSxFQUFFLENBQUMsQ0FBQztpQkFDcEU7WUFDSCxDQUFDO1lBQ0QsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMscUJBQXFCLENBQUM7WUFDdEMsU0FBUyxFQUFFLEdBQUcsRUFBRSxDQUNkLFFBQVEsQ0FBQyxTQUFTLENBQUMsVUFBVSxDQUFDLG1CQUFtQixDQUFDO2dCQUNsRCxRQUFRLENBQUMsU0FBUyxDQUFDLDJCQUEyQixDQUFDO2dCQUMvQyxRQUFRLENBQUMsU0FBUyxDQUFDLDBCQUEwQixDQUFDO1NBQ2pELENBQUMsQ0FBQztJQUNMLENBQUM7SUFqRGUsc0NBQTZCLGdDQWlENUM7SUFFRDs7T0FFRztJQUNILFNBQWdCLDBCQUEwQixDQUN4QyxRQUF5QixFQUN6QixPQUFtRCxFQUNuRCxLQUF3QixFQUN4QixTQUF3QjtRQUV4QixRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxnQkFBZ0IsRUFBRTtZQUMvQyxPQUFPLEVBQUUsSUFBSSxDQUFDLEVBQUU7O2dCQUNkLE1BQU0sSUFBSSxHQUFZLElBQUksQ0FBQyxNQUFNLENBQVksSUFBSSxFQUFFLENBQUM7Z0JBQ3BELE1BQU0sTUFBTSxHQUFHLE9BQU8sQ0FBQyxhQUFhLENBQUM7Z0JBQ3JDLElBQUksQ0FBQyxNQUFNLEVBQUU7b0JBQ1gsT0FBTztpQkFDUjtnQkFDRCxrQkFBTSxDQUFDLE9BQU8sQ0FBQyxNQUFNLEVBQUMsZ0JBQWdCLG1EQUFHLElBQUksRUFBRTtZQUNqRCxDQUFDO1lBQ0QsU0FBUztZQUNULEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLDZCQUE2QixDQUFDO1NBQy9DLENBQUMsQ0FBQztJQUNMLENBQUM7SUFsQmUsbUNBQTBCLDZCQWtCekM7SUFFRDs7T0FFRztJQUNILFNBQWdCLHVCQUF1QixDQUNyQyxRQUF5QixFQUN6QixPQUFtRCxFQUNuRCxLQUF3QixFQUN4QixTQUF3QjtRQUV4QixRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxhQUFhLEVBQUU7WUFDNUMsT0FBTyxFQUFFLElBQUksQ0FBQyxFQUFFO2dCQUNkLE1BQU0sTUFBTSxHQUFHLE9BQU8sQ0FBQyxhQUFhLENBQUM7Z0JBRXJDLElBQUksQ0FBQyxNQUFNLEVBQUU7b0JBQ1gsT0FBTztpQkFDUjtnQkFFRCxPQUFPLHdCQUF3QixDQUFDLFFBQVEsQ0FBQyxDQUFDLE1BQU0sRUFBRSxJQUFJLENBQUMsQ0FBQztZQUMxRCxDQUFDO1lBQ0QsU0FBUztZQUNULElBQUksRUFBRSxrRUFBVztZQUNqQixLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQywyQkFBMkIsQ0FBQztTQUM3QyxDQUFDLENBQUM7SUFDTCxDQUFDO0lBcEJlLGdDQUF1QiwwQkFvQnRDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQixpQkFBaUIsQ0FDL0IsUUFBeUIsRUFDekIsT0FBbUQsRUFDbkQsS0FBd0IsRUFDeEIsU0FBd0I7UUFFeEIsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsT0FBTyxFQUFFO1lBQ3RDLE9BQU8sRUFBRSxHQUFHLEVBQUU7O2dCQUNaLDJFQUEyRTtnQkFDM0UsTUFBTSxNQUFNLFNBQUcsT0FBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDO2dCQUU5QyxJQUFJLENBQUMsTUFBTSxFQUFFO29CQUNYLE9BQU87aUJBQ1I7Z0JBRUQsSUFBSSxJQUFJLEdBQXVCLEVBQUUsQ0FBQztnQkFDbEMsTUFBTSxNQUFNLEdBQUcsTUFBTSxDQUFDLE1BQU0sQ0FBQztnQkFDN0IsTUFBTSxJQUFJLEdBQUcsTUFBTSxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUM7Z0JBQ2pDLE1BQU0sU0FBUyxHQUFHLGtFQUFlLENBQUMsSUFBSSxDQUFDLENBQUM7Z0JBQ3hDLE1BQU0sU0FBUyxHQUFHLE1BQU0sQ0FBQyxZQUFZLEVBQUUsQ0FBQztnQkFDeEMsTUFBTSxFQUFFLEtBQUssRUFBRSxHQUFHLEVBQUUsR0FBRyxTQUFTLENBQUM7Z0JBQ2pDLElBQUksUUFBUSxHQUFHLEtBQUssQ0FBQyxNQUFNLEtBQUssR0FBRyxDQUFDLE1BQU0sSUFBSSxLQUFLLENBQUMsSUFBSSxLQUFLLEdBQUcsQ0FBQyxJQUFJLENBQUM7Z0JBRXRFLElBQUksUUFBUSxFQUFFO29CQUNaLHlDQUF5QztvQkFDekMsTUFBTSxLQUFLLEdBQUcsTUFBTSxDQUFDLFdBQVcsQ0FBQyxTQUFTLENBQUMsS0FBSyxDQUFDLENBQUM7b0JBQ2xELE1BQU0sR0FBRyxHQUFHLE1BQU0sQ0FBQyxXQUFXLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyxDQUFDO29CQUU5QyxJQUFJLEdBQUcsTUFBTSxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLFNBQVMsQ0FBQyxLQUFLLEVBQUUsR0FBRyxDQUFDLENBQUM7aUJBQ3REO3FCQUFNLElBQUksZ0ZBQTZCLENBQUMsU0FBUyxDQUFDLEVBQUU7b0JBQ25ELE1BQU0sRUFBRSxJQUFJLEVBQUUsR0FBRyxNQUFNLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQztvQkFDcEMsTUFBTSxNQUFNLEdBQUcsNEZBQXlDLENBQUMsSUFBSSxDQUFDLENBQUM7b0JBRS9ELEtBQUssTUFBTSxLQUFLLElBQUksTUFBTSxFQUFFO3dCQUMxQixJQUFJLEtBQUssQ0FBQyxTQUFTLElBQUksS0FBSyxDQUFDLElBQUksSUFBSSxLQUFLLENBQUMsSUFBSSxJQUFJLEtBQUssQ0FBQyxPQUFPLEVBQUU7NEJBQ2hFLElBQUksR0FBRyxLQUFLLENBQUMsSUFBSSxDQUFDOzRCQUNsQixRQUFRLEdBQUcsSUFBSSxDQUFDOzRCQUNoQixNQUFNO3lCQUNQO3FCQUNGO2lCQUNGO2dCQUVELElBQUksQ0FBQyxRQUFRLEVBQUU7b0JBQ2IsOENBQThDO29CQUM5QyxJQUFJLEdBQUcsTUFBTSxDQUFDLE9BQU8sQ0FBQyxTQUFTLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO29CQUM1QyxNQUFNLE1BQU0sR0FBRyxNQUFNLENBQUMsaUJBQWlCLEVBQUUsQ0FBQztvQkFDMUMsSUFBSSxNQUFNLENBQUMsSUFBSSxHQUFHLENBQUMsS0FBSyxNQUFNLENBQUMsU0FBUyxFQUFFO3dCQUN4QyxNQUFNLElBQUksR0FBRyxNQUFNLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUM7d0JBQ3JDLE1BQU0sQ0FBQyxLQUFLLENBQUMsS0FBSyxDQUFDLElBQUksR0FBRyxJQUFJLEdBQUcsSUFBSSxDQUFDO3FCQUN2QztvQkFDRCxNQUFNLENBQUMsaUJBQWlCLENBQUM7d0JBQ3ZCLElBQUksRUFBRSxNQUFNLENBQUMsSUFBSSxHQUFHLENBQUM7d0JBQ3JCLE1BQU0sRUFBRSxNQUFNLENBQUMsTUFBTTtxQkFDdEIsQ0FBQyxDQUFDO2lCQUNKO2dCQUVELE1BQU0sUUFBUSxHQUFHLEtBQUssQ0FBQztnQkFDdkIsSUFBSSxJQUFJLEVBQUU7b0JBQ1IsT0FBTyxRQUFRLENBQUMsT0FBTyxDQUFDLGdCQUFnQixFQUFFLEVBQUUsUUFBUSxFQUFFLElBQUksRUFBRSxJQUFJLEVBQUUsQ0FBQyxDQUFDO2lCQUNyRTtxQkFBTTtvQkFDTCxPQUFPLE9BQU8sQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDLENBQUMsQ0FBQztpQkFDaEM7WUFDSCxDQUFDO1lBQ0QsU0FBUztZQUNULEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQztTQUM1QixDQUFDLENBQUM7SUFDTCxDQUFDO0lBbEVlLDBCQUFpQixvQkFrRWhDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQixvQkFBb0IsQ0FDbEMsUUFBeUIsRUFDekIsT0FBbUQsRUFDbkQsS0FBd0IsRUFDeEIsU0FBd0I7UUFFeEIsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsVUFBVSxFQUFFO1lBQ3pDLE9BQU8sRUFBRSxHQUFHLEVBQUU7O2dCQUNaLE1BQU0sTUFBTSxTQUFHLE9BQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sQ0FBQztnQkFFOUMsSUFBSSxDQUFDLE1BQU0sRUFBRTtvQkFDWCxPQUFPO2lCQUNSO2dCQUVELElBQUksSUFBSSxHQUFHLEVBQUUsQ0FBQztnQkFDZCxNQUFNLE1BQU0sR0FBRyxNQUFNLENBQUMsTUFBTSxDQUFDO2dCQUM3QixNQUFNLElBQUksR0FBRyxNQUFNLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUM7Z0JBQ3JDLE1BQU0sSUFBSSxHQUFHLE1BQU0sQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDO2dCQUNqQyxNQUFNLFNBQVMsR0FBRyxrRUFBZSxDQUFDLElBQUksQ0FBQyxDQUFDO2dCQUV4QyxJQUFJLGdGQUE2QixDQUFDLFNBQVMsQ0FBQyxFQUFFO29CQUM1Qyw0Q0FBNEM7b0JBQzVDLE1BQU0sTUFBTSxHQUFHLDRGQUF5QyxDQUFDLElBQUksQ0FBQyxDQUFDO29CQUMvRCxLQUFLLE1BQU0sS0FBSyxJQUFJLE1BQU0sRUFBRTt3QkFDMUIsSUFBSSxJQUFJLEtBQUssQ0FBQyxJQUFJLENBQUM7cUJBQ3BCO2lCQUNGO3FCQUFNO29CQUNMLElBQUksR0FBRyxJQUFJLENBQUM7aUJBQ2I7Z0JBRUQsTUFBTSxRQUFRLEdBQUcsS0FBSyxDQUFDO2dCQUN2QixJQUFJLElBQUksRUFBRTtvQkFDUixPQUFPLFFBQVEsQ0FBQyxPQUFPLENBQUMsZ0JBQWdCLEVBQUUsRUFBRSxRQUFRLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxDQUFDLENBQUM7aUJBQ3JFO3FCQUFNO29CQUNMLE9BQU8sT0FBTyxDQUFDLE9BQU8sQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDO2lCQUNoQztZQUNILENBQUM7WUFDRCxTQUFTO1lBQ1QsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsY0FBYyxDQUFDO1NBQ2hDLENBQUMsQ0FBQztJQUNMLENBQUM7SUF4Q2UsNkJBQW9CLHVCQXdDbkM7SUFFRDs7T0FFRztJQUNILFNBQWdCLHlCQUF5QixDQUN2QyxRQUF5QixFQUN6QixPQUFtRCxFQUNuRCxLQUF3QjtRQUV4QixRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxlQUFlLEVBQUU7WUFDOUMsT0FBTyxFQUFFLEdBQUcsRUFBRTtnQkFDWixNQUFNLE1BQU0sR0FBRyxPQUFPLENBQUMsYUFBYSxDQUFDO2dCQUNyQyxJQUFJLENBQUMsTUFBTSxFQUFFO29CQUNYLE9BQU87aUJBQ1I7Z0JBQ0QsTUFBTSxJQUFJLEdBQUcsTUFBTSxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUM7Z0JBQ2pDLE9BQU8sUUFBUSxDQUFDLE9BQU8sQ0FBQyxxQkFBcUIsRUFBRTtvQkFDN0MsSUFBSTtvQkFDSixPQUFPLEVBQUU7d0JBQ1AsSUFBSSxFQUFFLGFBQWE7cUJBQ3BCO2lCQUNGLENBQUMsQ0FBQztZQUNMLENBQUM7WUFDRCxTQUFTLEVBQUUsR0FBRyxFQUFFO2dCQUNkLE1BQU0sTUFBTSxHQUFHLE9BQU8sQ0FBQyxhQUFhLENBQUM7Z0JBQ3JDLE9BQU8sQ0FDTCxDQUFDLE1BQU0sSUFBSSxrRUFBZSxDQUFDLE1BQU0sQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLEtBQUssS0FBSyxDQUFDLElBQUksS0FBSyxDQUNwRSxDQUFDO1lBQ0osQ0FBQztZQUNELElBQUksRUFBRSxtRUFBWTtZQUNsQixLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyx1QkFBdUIsQ0FBQztTQUN6QyxDQUFDLENBQUM7SUFDTCxDQUFDO0lBNUJlLGtDQUF5Qiw0QkE0QnhDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQixjQUFjLENBQzVCLFFBQXlCLEVBQ3pCLE9BQW1ELEVBQ25ELEtBQXdCLEVBQ3hCLFNBQXdCO1FBRXhCLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLElBQUksRUFBRTtZQUNuQyxPQUFPLEVBQUUsR0FBRyxFQUFFOztnQkFDWixNQUFNLE1BQU0sU0FBRyxPQUFPLENBQUMsYUFBYSwwQ0FBRSxPQUFPLENBQUM7Z0JBRTlDLElBQUksQ0FBQyxNQUFNLEVBQUU7b0JBQ1gsT0FBTztpQkFDUjtnQkFFRCxNQUFNLENBQUMsTUFBTSxDQUFDLElBQUksRUFBRSxDQUFDO1lBQ3ZCLENBQUM7WUFDRCxTQUFTLEVBQUUsR0FBRyxFQUFFOztnQkFDZCxJQUFJLENBQUMsU0FBUyxFQUFFLEVBQUU7b0JBQ2hCLE9BQU8sS0FBSyxDQUFDO2lCQUNkO2dCQUVELE1BQU0sTUFBTSxTQUFHLE9BQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sQ0FBQztnQkFFOUMsSUFBSSxDQUFDLE1BQU0sRUFBRTtvQkFDWCxPQUFPLEtBQUssQ0FBQztpQkFDZDtnQkFDRCxzREFBc0Q7Z0JBQ3RELHlGQUF5RjtnQkFDekYsT0FBTyxJQUFJLENBQUM7WUFDZCxDQUFDO1lBQ0QsSUFBSSxFQUFFLHlFQUFrQixDQUFDLEVBQUUsVUFBVSxFQUFFLFVBQVUsRUFBRSxDQUFDO1lBQ3BELEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLE1BQU0sQ0FBQztTQUN4QixDQUFDLENBQUM7SUFDTCxDQUFDO0lBakNlLHVCQUFjLGlCQWlDN0I7SUFFRDs7T0FFRztJQUNILFNBQWdCLGNBQWMsQ0FDNUIsUUFBeUIsRUFDekIsT0FBbUQsRUFDbkQsS0FBd0IsRUFDeEIsU0FBd0I7UUFFeEIsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsSUFBSSxFQUFFO1lBQ25DLE9BQU8sRUFBRSxHQUFHLEVBQUU7O2dCQUNaLE1BQU0sTUFBTSxTQUFHLE9BQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sQ0FBQztnQkFFOUMsSUFBSSxDQUFDLE1BQU0sRUFBRTtvQkFDWCxPQUFPO2lCQUNSO2dCQUVELE1BQU0sQ0FBQyxNQUFNLENBQUMsSUFBSSxFQUFFLENBQUM7WUFDdkIsQ0FBQztZQUNELFNBQVMsRUFBRSxHQUFHLEVBQUU7O2dCQUNkLElBQUksQ0FBQyxTQUFTLEVBQUUsRUFBRTtvQkFDaEIsT0FBTyxLQUFLLENBQUM7aUJBQ2Q7Z0JBRUQsTUFBTSxNQUFNLFNBQUcsT0FBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDO2dCQUU5QyxJQUFJLENBQUMsTUFBTSxFQUFFO29CQUNYLE9BQU8sS0FBSyxDQUFDO2lCQUNkO2dCQUNELHNEQUFzRDtnQkFDdEQseUZBQXlGO2dCQUN6RixPQUFPLElBQUksQ0FBQztZQUNkLENBQUM7WUFDRCxJQUFJLEVBQUUseUVBQWtCLENBQUMsRUFBRSxVQUFVLEVBQUUsVUFBVSxFQUFFLENBQUM7WUFDcEQsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsTUFBTSxDQUFDO1NBQ3hCLENBQUMsQ0FBQztJQUNMLENBQUM7SUFqQ2UsdUJBQWMsaUJBaUM3QjtJQUVEOztPQUVHO0lBQ0gsU0FBZ0IsYUFBYSxDQUMzQixRQUF5QixFQUN6QixPQUFtRCxFQUNuRCxLQUF3QixFQUN4QixTQUF3QjtRQUV4QixRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxHQUFHLEVBQUU7WUFDbEMsT0FBTyxFQUFFLEdBQUcsRUFBRTs7Z0JBQ1osTUFBTSxNQUFNLFNBQUcsT0FBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDO2dCQUU5QyxJQUFJLENBQUMsTUFBTSxFQUFFO29CQUNYLE9BQU87aUJBQ1I7Z0JBRUQsTUFBTSxNQUFNLEdBQUcsTUFBTSxDQUFDLE1BQTBCLENBQUM7Z0JBQ2pELE1BQU0sSUFBSSxHQUFHLGdCQUFnQixDQUFDLE1BQU0sQ0FBQyxDQUFDO2dCQUV0Qyx3RUFBc0IsQ0FBQyxJQUFJLENBQUMsQ0FBQztnQkFDN0IsTUFBTSxDQUFDLGdCQUFnQixJQUFJLE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxFQUFFLENBQUMsQ0FBQztZQUN6RCxDQUFDO1lBQ0QsU0FBUyxFQUFFLEdBQUcsRUFBRTs7Z0JBQ2QsSUFBSSxDQUFDLFNBQVMsRUFBRSxFQUFFO29CQUNoQixPQUFPLEtBQUssQ0FBQztpQkFDZDtnQkFFRCxNQUFNLE1BQU0sU0FBRyxPQUFPLENBQUMsYUFBYSwwQ0FBRSxPQUFPLENBQUM7Z0JBRTlDLElBQUksQ0FBQyxNQUFNLEVBQUU7b0JBQ1gsT0FBTyxLQUFLLENBQUM7aUJBQ2Q7Z0JBRUQsNERBQTREO2dCQUM1RCxPQUFPLFVBQVUsQ0FBQyxNQUFNLENBQUMsTUFBMEIsQ0FBQyxDQUFDO1lBQ3ZELENBQUM7WUFDRCxJQUFJLEVBQUUsd0VBQWlCLENBQUMsRUFBRSxVQUFVLEVBQUUsVUFBVSxFQUFFLENBQUM7WUFDbkQsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsS0FBSyxDQUFDO1NBQ3ZCLENBQUMsQ0FBQztJQUNMLENBQUM7SUFyQ2Usc0JBQWEsZ0JBcUM1QjtJQUVEOztPQUVHO0lBQ0gsU0FBZ0IsY0FBYyxDQUM1QixRQUF5QixFQUN6QixPQUFtRCxFQUNuRCxLQUF3QixFQUN4QixTQUF3QjtRQUV4QixRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxJQUFJLEVBQUU7WUFDbkMsT0FBTyxFQUFFLEdBQUcsRUFBRTs7Z0JBQ1osTUFBTSxNQUFNLFNBQUcsT0FBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDO2dCQUU5QyxJQUFJLENBQUMsTUFBTSxFQUFFO29CQUNYLE9BQU87aUJBQ1I7Z0JBRUQsTUFBTSxNQUFNLEdBQUcsTUFBTSxDQUFDLE1BQTBCLENBQUM7Z0JBQ2pELE1BQU0sSUFBSSxHQUFHLGdCQUFnQixDQUFDLE1BQU0sQ0FBQyxDQUFDO2dCQUV0Qyx3RUFBc0IsQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUMvQixDQUFDO1lBQ0QsU0FBUyxFQUFFLEdBQUcsRUFBRTs7Z0JBQ2QsSUFBSSxDQUFDLFNBQVMsRUFBRSxFQUFFO29CQUNoQixPQUFPLEtBQUssQ0FBQztpQkFDZDtnQkFFRCxNQUFNLE1BQU0sU0FBRyxPQUFPLENBQUMsYUFBYSwwQ0FBRSxPQUFPLENBQUM7Z0JBRTlDLElBQUksQ0FBQyxNQUFNLEVBQUU7b0JBQ1gsT0FBTyxLQUFLLENBQUM7aUJBQ2Q7Z0JBRUQsNERBQTREO2dCQUM1RCxPQUFPLFVBQVUsQ0FBQyxNQUFNLENBQUMsTUFBMEIsQ0FBQyxDQUFDO1lBQ3ZELENBQUM7WUFDRCxJQUFJLEVBQUUseUVBQWtCLENBQUMsRUFBRSxVQUFVLEVBQUUsVUFBVSxFQUFFLENBQUM7WUFDcEQsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsTUFBTSxDQUFDO1NBQ3hCLENBQUMsQ0FBQztJQUNMLENBQUM7SUFwQ2UsdUJBQWMsaUJBb0M3QjtJQUVEOztPQUVHO0lBQ0gsU0FBZ0IsZUFBZSxDQUM3QixRQUF5QixFQUN6QixPQUFtRCxFQUNuRCxLQUF3QixFQUN4QixTQUF3QjtRQUV4QixRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxLQUFLLEVBQUU7WUFDcEMsT0FBTyxFQUFFLEtBQUssSUFBSSxFQUFFOztnQkFDbEIsTUFBTSxNQUFNLFNBQUcsT0FBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDO2dCQUU5QyxJQUFJLENBQUMsTUFBTSxFQUFFO29CQUNYLE9BQU87aUJBQ1I7Z0JBRUQsTUFBTSxNQUFNLEdBQXVCLE1BQU0sQ0FBQyxNQUFNLENBQUM7Z0JBRWpELDBCQUEwQjtnQkFDMUIsTUFBTSxTQUFTLEdBQUcsTUFBTSxDQUFDLFNBQVMsQ0FBQyxTQUFTLENBQUM7Z0JBQzdDLE1BQU0sYUFBYSxHQUFXLE1BQU0sU0FBUyxDQUFDLFFBQVEsRUFBRSxDQUFDO2dCQUV6RCxJQUFJLGFBQWEsRUFBRTtvQkFDakIsMkJBQTJCO29CQUMzQixNQUFNLENBQUMsZ0JBQWdCLElBQUksTUFBTSxDQUFDLGdCQUFnQixDQUFDLGFBQWEsQ0FBQyxDQUFDO2lCQUNuRTtZQUNILENBQUM7WUFDRCxTQUFTLEVBQUUsR0FBRyxFQUFFLFdBQUMsY0FBTyxDQUFDLFNBQVMsRUFBRSxXQUFJLE9BQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sRUFBQztZQUN2RSxJQUFJLEVBQUUsMEVBQW1CLENBQUMsRUFBRSxVQUFVLEVBQUUsVUFBVSxFQUFFLENBQUM7WUFDckQsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsT0FBTyxDQUFDO1NBQ3pCLENBQUMsQ0FBQztJQUNMLENBQUM7SUE3QmUsd0JBQWUsa0JBNkI5QjtJQUVEOztPQUVHO0lBQ0gsU0FBZ0IsbUJBQW1CLENBQ2pDLFFBQXlCLEVBQ3pCLE9BQW1ELEVBQ25ELEtBQXdCLEVBQ3hCLFNBQXdCO1FBRXhCLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLFNBQVMsRUFBRTtZQUN4QyxPQUFPLEVBQUUsR0FBRyxFQUFFOztnQkFDWixNQUFNLE1BQU0sU0FBRyxPQUFPLENBQUMsYUFBYSwwQ0FBRSxPQUFPLENBQUM7Z0JBRTlDLElBQUksQ0FBQyxNQUFNLEVBQUU7b0JBQ1gsT0FBTztpQkFDUjtnQkFFRCxNQUFNLE1BQU0sR0FBRyxNQUFNLENBQUMsTUFBMEIsQ0FBQztnQkFDakQsTUFBTSxDQUFDLFdBQVcsQ0FBQyxXQUFXLENBQUMsQ0FBQztZQUNsQyxDQUFDO1lBQ0QsU0FBUyxFQUFFLEdBQUcsRUFBRSxXQUFDLGNBQU8sQ0FBQyxTQUFTLEVBQUUsV0FBSSxPQUFPLENBQUMsYUFBYSwwQ0FBRSxPQUFPLEVBQUM7WUFDdkUsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsWUFBWSxDQUFDO1NBQzlCLENBQUMsQ0FBQztJQUNMLENBQUM7SUFwQmUsNEJBQW1CLHNCQW9CbEM7SUFFRDs7T0FFRztJQUNILFNBQVMsVUFBVSxDQUFDLE1BQXdCO1FBQzFDLE1BQU0sWUFBWSxHQUFHLE1BQU0sQ0FBQyxZQUFZLEVBQUUsQ0FBQztRQUMzQyxNQUFNLEVBQUUsS0FBSyxFQUFFLEdBQUcsRUFBRSxHQUFHLFlBQVksQ0FBQztRQUNwQyxNQUFNLFFBQVEsR0FBRyxLQUFLLENBQUMsTUFBTSxLQUFLLEdBQUcsQ0FBQyxNQUFNLElBQUksS0FBSyxDQUFDLElBQUksS0FBSyxHQUFHLENBQUMsSUFBSSxDQUFDO1FBRXhFLE9BQU8sUUFBUSxDQUFDO0lBQ2xCLENBQUM7SUFFRDs7T0FFRztJQUNILFNBQVMsZ0JBQWdCLENBQUMsTUFBd0I7UUFDaEQsTUFBTSxZQUFZLEdBQUcsTUFBTSxDQUFDLFlBQVksRUFBRSxDQUFDO1FBQzNDLE1BQU0sS0FBSyxHQUFHLE1BQU0sQ0FBQyxXQUFXLENBQUMsWUFBWSxDQUFDLEtBQUssQ0FBQyxDQUFDO1FBQ3JELE1BQU0sR0FBRyxHQUFHLE1BQU0sQ0FBQyxXQUFXLENBQUMsWUFBWSxDQUFDLEdBQUcsQ0FBQyxDQUFDO1FBQ2pELE1BQU0sSUFBSSxHQUFHLE1BQU0sQ0FBQyxLQUFLLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsS0FBSyxFQUFFLEdBQUcsQ0FBQyxDQUFDO1FBRTNELE9BQU8sSUFBSSxDQUFDO0lBQ2QsQ0FBQztJQUVEOztPQUVHO0lBQ0gsU0FBUyxTQUFTLENBQ2hCLFFBQXlCLEVBQ3pCLEdBQVcsRUFDWCxNQUFjLEtBQUs7UUFFbkIsT0FBTyxRQUFRO2FBQ1osT0FBTyxDQUFDLHlCQUF5QixFQUFFO1lBQ2xDLElBQUksRUFBRSxHQUFHO1lBQ1QsSUFBSSxFQUFFLE1BQU07WUFDWixHQUFHO1NBQ0osQ0FBQzthQUNELElBQUksQ0FBQyxLQUFLLENBQUMsRUFBRTtZQUNaLElBQUksS0FBSyxJQUFJLFNBQVMsRUFBRTtnQkFDdEIsT0FBTyxRQUFRLENBQUMsT0FBTyxDQUFDLGlCQUFpQixFQUFFO29CQUN6QyxJQUFJLEVBQUUsS0FBSyxDQUFDLElBQUk7b0JBQ2hCLE9BQU8sRUFBRSxPQUFPO2lCQUNqQixDQUFDLENBQUM7YUFDSjtRQUNILENBQUMsQ0FBQyxDQUFDO0lBQ1AsQ0FBQztJQUVEOzs7O09BSUc7SUFDSCxTQUFnQixtQkFBbUIsQ0FDakMsUUFBeUIsRUFDekIsY0FBbUMsRUFDbkMsS0FBd0I7UUFFeEIsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsU0FBUyxFQUFFO1lBQ3hDLEtBQUssRUFBRSxJQUFJLENBQUMsRUFBRTs7Z0JBQ1osSUFBSSxJQUFJLENBQUMsU0FBUyxFQUFFO29CQUNsQixhQUFRLElBQUksQ0FBQyxZQUF1QixtQ0FBSSxLQUFLLENBQUMsRUFBRSxDQUFDLGVBQWUsQ0FBQyxDQUFDO2lCQUNuRTtnQkFDRCxhQUFRLElBQUksQ0FBQyxhQUF3QixtQ0FBSSxLQUFLLENBQUMsRUFBRSxDQUFDLFdBQVcsQ0FBQyxDQUFDO1lBQ2pFLENBQUM7WUFDRCxPQUFPLEVBQUUsSUFBSSxDQUFDLEVBQUUsd0JBQ2IsSUFBSSxDQUFDLE9BQWtCLG1DQUFJLEtBQUssQ0FBQyxFQUFFLENBQUMsd0JBQXdCLENBQUM7WUFDaEUsSUFBSSxFQUFFLElBQUksQ0FBQyxFQUFFOztnQkFDWCxXQUFJLENBQUMsU0FBUztvQkFDWixDQUFDLENBQUMsU0FBUztvQkFDWCxDQUFDLENBQUMsc0VBQWUsQ0FBQzt3QkFDZCxJQUFJLFFBQUcsSUFBSSxDQUFDLFFBQW1CLG1DQUFJLHFFQUFjO3FCQUNsRCxDQUFDO2FBQUE7WUFDUixPQUFPLEVBQUUsSUFBSSxDQUFDLEVBQUU7O2dCQUNkLE1BQU0sR0FBRyxHQUFHLElBQUksQ0FBQyxHQUFHLElBQUksY0FBYyxDQUFDLGNBQWMsQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDO2dCQUNqRSxPQUFPLFNBQVMsQ0FDZCxRQUFRLEVBQ1IsR0FBYSxRQUNaLElBQUksQ0FBQyxPQUFrQixtQ0FBSSxLQUFLLENBQ2xDLENBQUM7WUFDSixDQUFDO1NBQ0YsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQTdCZSw0QkFBbUIsc0JBNkJsQztJQUVEOztPQUVHO0lBQ0gsU0FBZ0IsMkJBQTJCLENBQ3pDLFFBQXlCLEVBQ3pCLGNBQW1DLEVBQ25DLEtBQXdCO1FBRXhCLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLGlCQUFpQixFQUFFO1lBQ2hELEtBQUssRUFBRSxJQUFJLENBQUMsRUFBRSxDQUNaLElBQUksQ0FBQyxXQUFXLENBQUM7Z0JBQ2YsQ0FBQyxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsbUJBQW1CLENBQUM7Z0JBQy9CLENBQUMsQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUFDLGVBQWUsQ0FBQztZQUMvQixPQUFPLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyw0QkFBNEIsQ0FBQztZQUMvQyxJQUFJLEVBQUUsSUFBSSxDQUFDLEVBQUUsQ0FBQyxDQUFDLElBQUksQ0FBQyxXQUFXLENBQUMsQ0FBQyxDQUFDLENBQUMsU0FBUyxDQUFDLENBQUMsQ0FBQyxtRUFBWSxDQUFDO1lBQzVELE9BQU8sRUFBRSxJQUFJLENBQUMsRUFBRTtnQkFDZCxNQUFNLEdBQUcsR0FBRyxJQUFJLENBQUMsS0FBSyxDQUFDLElBQUksY0FBYyxDQUFDLGNBQWMsQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDO2dCQUNwRSxPQUFPLFNBQVMsQ0FBQyxRQUFRLEVBQUUsR0FBYSxFQUFFLElBQUksQ0FBQyxDQUFDO1lBQ2xELENBQUM7U0FDRixDQUFDLENBQUM7SUFDTCxDQUFDO0lBakJlLG9DQUEyQiw4QkFpQjFDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQixnQkFBZ0IsQ0FDOUIsUUFBbUIsRUFDbkIsS0FBd0I7UUFFeEIsc0JBQXNCLENBQUMsUUFBUSxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBRXhDLDhCQUE4QixDQUFDLFFBQVEsRUFBRSxLQUFLLENBQUMsQ0FBQztJQUNsRCxDQUFDO0lBUGUseUJBQWdCLG1CQU8vQjtJQUVEOztPQUVHO0lBQ0gsU0FBZ0Isc0JBQXNCLENBQ3BDLFFBQW1CLEVBQ25CLEtBQXdCO1FBRXhCLFFBQVEsQ0FBQyxHQUFHLENBQUM7WUFDWCxPQUFPLEVBQUUsVUFBVSxDQUFDLFNBQVM7WUFDN0IsUUFBUSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsT0FBTyxDQUFDO1lBQzNCLElBQUksRUFBRSxDQUFDO1NBQ1IsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQVRlLCtCQUFzQix5QkFTckM7SUFFRDs7T0FFRztJQUNILFNBQWdCLDhCQUE4QixDQUM1QyxRQUFtQixFQUNuQixLQUF3QjtRQUV4QixRQUFRLENBQUMsR0FBRyxDQUFDO1lBQ1gsT0FBTyxFQUFFLFVBQVUsQ0FBQyxpQkFBaUI7WUFDckMsUUFBUSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsT0FBTyxDQUFDO1lBQzNCLElBQUksRUFBRSxDQUFDO1NBQ1IsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQVRlLHVDQUE4QixpQ0FTN0M7SUFFRDs7T0FFRztJQUNILFNBQWdCLDhCQUE4QixDQUM1QyxRQUFtQixFQUNuQixLQUF3QixFQUN4Qix3QkFBaUQ7UUFFakQsS0FBSyxJQUFJLEdBQUcsSUFBSSx3QkFBd0IsRUFBRTtZQUN4QyxRQUFRLENBQUMsR0FBRyxDQUFDO2dCQUNYLE9BQU8sRUFBRSxVQUFVLENBQUMsU0FBUztnQkFDN0IsUUFBUSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsT0FBTyxDQUFDO2dCQUMzQixJQUFJLEVBQUUsQ0FBQztnQkFDUCxJQUFJLEVBQUUsR0FBRzthQUNWLENBQUMsQ0FBQztTQUNKO0lBQ0gsQ0FBQztJQWJlLHVDQUE4QixpQ0FhN0M7SUFFRDs7T0FFRztJQUNILFNBQWdCLGVBQWUsQ0FDN0IsT0FBd0IsRUFDeEIsS0FBd0I7UUFFeEIsOEJBQThCLENBQUMsT0FBTyxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBRS9DLDRCQUE0QixDQUFDLE9BQU8sRUFBRSxLQUFLLENBQUMsQ0FBQztRQUU3QyxvQ0FBb0MsQ0FBQyxPQUFPLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFFckQsa0NBQWtDLENBQUMsT0FBTyxFQUFFLEtBQUssQ0FBQyxDQUFDO0lBQ3JELENBQUM7SUFYZSx3QkFBZSxrQkFXOUI7SUFFRDs7T0FFRztJQUNILFNBQWdCLDhCQUE4QixDQUM1QyxPQUF3QixFQUN4QixLQUF3QjtRQUV4QixNQUFNLGVBQWUsR0FBRyxLQUFLLENBQUMsRUFBRSxDQUFDLGFBQWEsQ0FBQyxDQUFDO1FBQ2hELE1BQU0sSUFBSSxHQUFlO1lBQ3ZCLFlBQVksRUFBRSxLQUFLO1lBQ25CLElBQUksRUFBRSxDQUFDO1NBQ1IsQ0FBQztRQUNGLE1BQU0sT0FBTyxHQUFHLFVBQVUsQ0FBQyxVQUFVLENBQUM7UUFDdEMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxFQUFFLE9BQU8sRUFBRSxJQUFJLEVBQUUsUUFBUSxFQUFFLGVBQWUsRUFBRSxDQUFDLENBQUM7UUFFOUQsS0FBSyxNQUFNLElBQUksSUFBSSxDQUFDLENBQUMsRUFBRSxDQUFDLEVBQUUsQ0FBQyxFQUFFLENBQUMsQ0FBQyxFQUFFO1lBQy9CLE1BQU0sSUFBSSxHQUFlO2dCQUN2QixZQUFZLEVBQUUsSUFBSTtnQkFDbEIsSUFBSTthQUNMLENBQUM7WUFDRixPQUFPLENBQUMsT0FBTyxDQUFDLEVBQUUsT0FBTyxFQUFFLElBQUksRUFBRSxRQUFRLEVBQUUsZUFBZSxFQUFFLENBQUMsQ0FBQztTQUMvRDtJQUNILENBQUM7SUFuQmUsdUNBQThCLGlDQW1CN0M7SUFFRDs7T0FFRztJQUNILFNBQWdCLDRCQUE0QixDQUMxQyxPQUF3QixFQUN4QixLQUF3QjtRQUV4QixNQUFNLGVBQWUsR0FBRyxLQUFLLENBQUMsRUFBRSxDQUFDLGFBQWEsQ0FBQyxDQUFDO1FBQ2hELE9BQU8sQ0FBQyxPQUFPLENBQUM7WUFDZCxPQUFPLEVBQUUsVUFBVSxDQUFDLFNBQVM7WUFDN0IsSUFBSSxFQUFFLEVBQUUsU0FBUyxFQUFFLElBQUksRUFBRTtZQUN6QixRQUFRLEVBQUUsZUFBZTtTQUMxQixDQUFDLENBQUM7SUFDTCxDQUFDO0lBVmUscUNBQTRCLCtCQVUzQztJQUVEOztPQUVHO0lBQ0gsU0FBZ0Isb0NBQW9DLENBQ2xELE9BQXdCLEVBQ3hCLEtBQXdCO1FBRXhCLE1BQU0sZUFBZSxHQUFHLEtBQUssQ0FBQyxFQUFFLENBQUMsYUFBYSxDQUFDLENBQUM7UUFDaEQsT0FBTyxDQUFDLE9BQU8sQ0FBQztZQUNkLE9BQU8sRUFBRSxVQUFVLENBQUMsaUJBQWlCO1lBQ3JDLElBQUksRUFBRSxFQUFFLFNBQVMsRUFBRSxJQUFJLEVBQUU7WUFDekIsUUFBUSxFQUFFLGVBQWU7U0FDMUIsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQVZlLDZDQUFvQyx1Q0FVbkQ7SUFFRDs7T0FFRztJQUNILFNBQWdCLGtDQUFrQyxDQUNoRCxPQUF3QixFQUN4QixLQUF3QjtRQUV4QixNQUFNLGVBQWUsR0FBRyxLQUFLLENBQUMsRUFBRSxDQUFDLGFBQWEsQ0FBQyxDQUFDO1FBQ2hELE1BQU0sT0FBTyxHQUFHLFVBQVUsQ0FBQyxjQUFjLENBQUM7UUFFMUMsSUFBSSxJQUFJLEdBQUcsRUFBRSxLQUFLLEVBQUUsQ0FBQyxFQUFFLENBQUM7UUFDeEIsT0FBTyxDQUFDLE9BQU8sQ0FBQyxFQUFFLE9BQU8sRUFBRSxJQUFJLEVBQUUsUUFBUSxFQUFFLGVBQWUsRUFBRSxDQUFDLENBQUM7UUFFOUQsSUFBSSxHQUFHLEVBQUUsS0FBSyxFQUFFLENBQUMsQ0FBQyxFQUFFLENBQUM7UUFDckIsT0FBTyxDQUFDLE9BQU8sQ0FBQyxFQUFFLE9BQU8sRUFBRSxJQUFJLEVBQUUsUUFBUSxFQUFFLGVBQWUsRUFBRSxDQUFDLENBQUM7SUFDaEUsQ0FBQztJQVplLDJDQUFrQyxxQ0FZakQ7SUFFRDs7T0FFRztJQUNILFNBQWdCLDZCQUE2QixDQUMzQyxPQUF3QixFQUN4QixLQUF3QixFQUN4Qix3QkFBaUQ7UUFFakQsTUFBTSxlQUFlLEdBQUcsS0FBSyxDQUFDLEVBQUUsQ0FBQyxhQUFhLENBQUMsQ0FBQztRQUNoRCxLQUFLLElBQUksR0FBRyxJQUFJLHdCQUF3QixFQUFFO1lBQ3hDLE9BQU8sQ0FBQyxPQUFPLENBQUM7Z0JBQ2QsT0FBTyxFQUFFLFVBQVUsQ0FBQyxTQUFTO2dCQUM3QixJQUFJLGtDQUFPLEdBQUcsS0FBRSxTQUFTLEVBQUUsSUFBSSxHQUFFO2dCQUNqQyxRQUFRLEVBQUUsZUFBZTthQUMxQixDQUFDLENBQUM7U0FDSjtJQUNILENBQUM7SUFiZSxzQ0FBNkIsZ0NBYTVDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQixZQUFZLENBQzFCLElBQWUsRUFDZixRQUF5QixFQUN6QixPQUFtRCxFQUNuRCxLQUF3QixFQUN4QixjQUFzQyxFQUN0QyxjQUE2QztRQUU3Qyx3Q0FBd0M7UUFDeEMscUJBQXFCLENBQUMsSUFBSSxFQUFFLE9BQU8sQ0FBQyxDQUFDO1FBRXJDLDJCQUEyQjtRQUMzQix5QkFBeUIsQ0FBQyxJQUFJLEVBQUUsT0FBTyxDQUFDLENBQUM7UUFFekMsMkNBQTJDO1FBQzNDLDJCQUEyQixDQUFDLElBQUksRUFBRSxRQUFRLEVBQUUsT0FBTyxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBRTVELHFDQUFxQztRQUNyQyxJQUFJLGNBQWMsRUFBRTtZQUNsQix1QkFBdUIsQ0FDckIsSUFBSSxFQUNKLFFBQVEsRUFDUixPQUFPLEVBQ1AsY0FBYyxFQUNkLEtBQUssRUFDTCxjQUFjLENBQ2YsQ0FBQztTQUNIO0lBQ0gsQ0FBQztJQTVCZSxxQkFBWSxlQTRCM0I7SUFFRDs7T0FFRztJQUNILFNBQWdCLDBCQUEwQixDQUN4QyxJQUFlLEVBQ2Ysd0JBQWlEO1FBRWpELEtBQUssSUFBSSxHQUFHLElBQUksd0JBQXdCLEVBQUU7WUFDeEMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDO2dCQUM1QixPQUFPLEVBQUUsVUFBVSxDQUFDLFNBQVM7Z0JBQzdCLElBQUksRUFBRSxHQUFHO2dCQUNULElBQUksRUFBRSxFQUFFO2FBQ1QsQ0FBQyxDQUFDO1NBQ0o7SUFDSCxDQUFDO0lBWGUsbUNBQTBCLDZCQVd6QztJQUVEOztPQUVHO0lBQ0gsU0FBZ0IscUJBQXFCLENBQ25DLElBQWUsRUFDZixPQUFtRDtRQUVuRCxJQUFJLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQyxHQUFHLENBQUM7WUFDeEIsT0FBTztZQUNQLElBQUksRUFBRSxNQUFNLENBQUMsRUFBRTtnQkFDYixNQUFNLENBQUMsT0FBTyxDQUFDLE1BQU0sQ0FBQyxJQUFJLEVBQUUsQ0FBQztZQUMvQixDQUFDO1lBQ0QsSUFBSSxFQUFFLE1BQU0sQ0FBQyxFQUFFO2dCQUNiLE1BQU0sQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLElBQUksRUFBRSxDQUFDO1lBQy9CLENBQUM7U0FDZ0QsQ0FBQyxDQUFDO0lBQ3ZELENBQUM7SUFiZSw4QkFBcUIsd0JBYXBDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQix5QkFBeUIsQ0FDdkMsSUFBZSxFQUNmLE9BQW1EO1FBRW5ELElBQUksQ0FBQyxRQUFRLENBQUMsYUFBYSxDQUFDLEdBQUcsQ0FBQztZQUM5QixPQUFPO1lBQ1AsaUJBQWlCLEVBQUUsTUFBTSxDQUFDLEVBQUU7Z0JBQzFCLE1BQU0sV0FBVyxHQUFHLENBQUMsTUFBTSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsU0FBUyxDQUFDLGFBQWEsQ0FBQyxDQUFDO2dCQUNwRSxNQUFNLENBQUMsT0FBTyxDQUFDLE1BQU0sQ0FBQyxTQUFTLENBQUMsYUFBYSxFQUFFLFdBQVcsQ0FBQyxDQUFDO1lBQzlELENBQUM7WUFDRCxjQUFjLEVBQUUsTUFBTSxDQUFDLEVBQUU7Z0JBQ3ZCLE1BQU0sUUFBUSxHQUFHLE1BQU0sQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLFNBQVMsQ0FBQyxVQUFVLENBQUMsQ0FBQztnQkFDN0QsTUFBTSxRQUFRLEdBQUcsUUFBUSxLQUFLLEtBQUssQ0FBQyxDQUFDLENBQUMsSUFBSSxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUM7Z0JBQ25ELE1BQU0sQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLFNBQVMsQ0FBQyxVQUFVLEVBQUUsUUFBUSxDQUFDLENBQUM7WUFDeEQsQ0FBQztZQUNELG1CQUFtQixFQUFFLE1BQU0sQ0FBQyxFQUFFO2dCQUM1QixNQUFNLGFBQWEsR0FBRyxDQUFDLE1BQU0sQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLFNBQVMsQ0FBQyxlQUFlLENBQUMsQ0FBQztnQkFDeEUsTUFBTSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsU0FBUyxDQUFDLGVBQWUsRUFBRSxhQUFhLENBQUMsQ0FBQztZQUNsRSxDQUFDO1lBQ0Qsa0JBQWtCLEVBQUUsTUFBTSxDQUFDLEVBQUUsQ0FDM0IsTUFBTSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsU0FBUyxDQUFDLGFBQWEsQ0FBQztZQUNoRCxlQUFlLEVBQUUsTUFBTSxDQUFDLEVBQUUsQ0FDeEIsTUFBTSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsU0FBUyxDQUFDLFVBQVUsQ0FBQyxLQUFLLEtBQUs7WUFDdkQsb0JBQW9CLEVBQUUsTUFBTSxDQUFDLEVBQUUsQ0FDN0IsTUFBTSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsU0FBUyxDQUFDLGVBQWUsQ0FBQztTQUNLLENBQUMsQ0FBQztJQUM3RCxDQUFDO0lBMUJlLGtDQUF5Qiw0QkEwQnhDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQiwyQkFBMkIsQ0FDekMsSUFBZSxFQUNmLFFBQXlCLEVBQ3pCLE9BQW1ELEVBQ25ELEtBQXdCO1FBRXhCLE1BQU0sYUFBYSxHQUVFLHdCQUF3QixDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBQ3hELElBQUksQ0FBQyxRQUFRLENBQUMsZUFBZSxDQUFDLEdBQUcsQ0FBQztZQUNoQyxPQUFPO1lBQ1Asa0JBQWtCLEVBQUUsQ0FBQyxDQUFTLEVBQUUsRUFBRSxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsMkJBQTJCLENBQUM7WUFDeEUsYUFBYTtTQUM0QyxDQUFDLENBQUM7SUFDL0QsQ0FBQztJQWRlLG9DQUEyQiw4QkFjMUM7SUFFRDs7T0FFRztJQUNILFNBQWdCLHVCQUF1QixDQUNyQyxJQUFlLEVBQ2YsUUFBeUIsRUFDekIsT0FBbUQsRUFDbkQsY0FBK0IsRUFDL0IsS0FBd0IsRUFDeEIsY0FBNkM7UUFFN0MsSUFBSSxDQUFDLE9BQU8sQ0FBQyxXQUFXLENBQUMsR0FBRyxDQUFDO1lBQzNCLE9BQU87WUFDUCxRQUFRLEVBQUUsQ0FBQyxDQUFTLEVBQUUsRUFBRSxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsVUFBVSxDQUFDO1lBQzdDLFdBQVcsRUFBRSxDQUFDLENBQVMsRUFBRSxFQUFFLENBQUMsS0FBSyxDQUFDLEVBQUUsQ0FBQyxjQUFjLENBQUM7WUFDcEQscUJBQXFCLEVBQUUsQ0FBQyxDQUFTLEVBQUUsRUFBRSxDQUNuQyxLQUFLLENBQUMsRUFBRSxDQUFDLGlDQUFpQyxDQUFDO1lBQzdDLFNBQVMsRUFBRSxPQUFPLENBQUMsRUFBRSxDQUNuQixDQUFDLENBQUMsY0FBYyxDQUFDLElBQUksQ0FDbkIsTUFBTSxDQUFDLEVBQUUsV0FBQyxvQkFBTSxDQUFDLGNBQWMsQ0FBQyxPQUFPLDBDQUFFLElBQUksTUFBSyxPQUFPLENBQUMsT0FBTyxDQUFDLElBQUksSUFDdkU7WUFDSCxHQUFHLEVBQUUsR0FBRyxFQUFFLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUMsT0FBTyxDQUFDO1lBQy9DLE1BQU0sRUFBRSxHQUFHLEVBQUUsQ0FBQyxRQUFRLENBQUMsT0FBTyxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUM7WUFDckQsZ0JBQWdCLEVBQUUsT0FBTyxDQUFDLEVBQUU7Z0JBQzFCLE1BQU0sTUFBTSxHQUFHLGNBQWMsQ0FBQyxJQUFJLENBQ2hDLE1BQU0sQ0FBQyxFQUFFLFdBQUMsb0JBQU0sQ0FBQyxjQUFjLENBQUMsT0FBTywwQ0FBRSxJQUFJLE1BQUssT0FBTyxDQUFDLE9BQU8sQ0FBQyxJQUFJLElBQ3ZFLENBQUM7Z0JBQ0YsSUFBSSxNQUFNLEVBQUU7b0JBQ1YsT0FBTyxDQUFDLGNBQWMsSUFBSSx1RUFBcUIsQ0FBQzt5QkFDN0MsT0FBTyxDQUFDLE1BQU0sQ0FBQyxjQUFjLENBQUM7eUJBQzlCLElBQUksQ0FBQyxTQUFTLENBQUMsRUFBRTt3QkFDaEIsSUFBSSxTQUFTLEVBQUU7NEJBQ2IsS0FBSyxRQUFRLENBQUMsT0FBTyxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsQ0FBQzt5QkFDOUM7d0JBQ0QsT0FBTyxTQUFTLENBQUM7b0JBQ25CLENBQUMsQ0FBQyxDQUFDO2lCQUNOO1lBQ0gsQ0FBQztTQUNtRCxDQUFDLENBQUM7SUFDMUQsQ0FBQztJQXBDZSxnQ0FBdUIsMEJBb0N0QztBQUNILENBQUMsRUE5cENnQixRQUFRLEtBQVIsUUFBUSxRQThwQ3hCOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDMXlDRCwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU04QjtBQUtIO0FBQ3VDO0FBQ2Y7QUFFUTtBQU05QjtBQUNpQjtBQUNBO0FBQ2M7QUFDWjtBQUNHO0FBRWY7QUFDdUI7QUFFeEI7QUFFdEM7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBMEM7SUFDcEQsUUFBUTtJQUNSLEVBQUUsRUFBRSx5Q0FBeUM7SUFDN0MsUUFBUSxFQUFFO1FBQ1IsbUVBQWU7UUFDZix3RUFBbUI7UUFDbkIseUVBQWdCO1FBQ2hCLGlFQUFXO0tBQ1o7SUFDRCxRQUFRLEVBQUU7UUFDUixnRUFBZTtRQUNmLGlFQUFlO1FBQ2YsMkRBQVM7UUFDVCwyREFBUztRQUNULG9FQUFlO1FBQ2Ysd0VBQXNCO0tBQ3ZCO0lBQ0QsUUFBUSxFQUFFLGtFQUFjO0lBQ3hCLFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRjs7O0dBR0c7QUFDSSxNQUFNLGNBQWMsR0FBZ0M7SUFDekQsRUFBRSxFQUFFLG1EQUFtRDtJQUN2RCxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxDQUFDLGtFQUFjLEVBQUUseUVBQWdCLEVBQUUsaUVBQVcsQ0FBQztJQUN6RCxRQUFRLEVBQUUsQ0FBQyw2REFBVSxDQUFDO0lBQ3RCLFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLGFBQTZCLEVBQzdCLGVBQWlDLEVBQ2pDLFVBQXVCLEVBQ3ZCLFNBQTRCLEVBQzVCLEVBQUU7UUFDRixNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQzVDLElBQUksQ0FBQyxTQUFTLEVBQUU7WUFDZCw2Q0FBNkM7WUFDN0MsT0FBTztTQUNSO1FBQ0QsOENBQThDO1FBQzlDLE1BQU0sSUFBSSxHQUFHLElBQUksa0RBQUksQ0FBQyxFQUFFLFFBQVEsRUFBRSxHQUFHLENBQUMsUUFBUSxFQUFFLENBQUMsQ0FBQztRQUNsRCxNQUFNLE9BQU8sR0FBRyx3QkFBd0IsQ0FBQztRQUN6QyxNQUFNLEVBQUUsS0FBSyxFQUFFLEdBQUcsR0FBRyxDQUFDO1FBQ3RCLE1BQU0sSUFBSSxHQUFlO1lBQ3ZCLFlBQVksRUFBRSxLQUFLO1lBQ25CLElBQUksRUFBRSxDQUFDO1lBQ1AsSUFBSSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsaUJBQWlCLENBQUM7U0FDbEMsQ0FBQztRQUNGLElBQUksQ0FBQyxPQUFPLENBQUMsRUFBRSxPQUFPLEVBQUUsSUFBSSxFQUFFLENBQUMsQ0FBQztRQUNoQyxLQUFLLE1BQU0sSUFBSSxJQUFJLENBQUMsQ0FBQyxFQUFFLENBQUMsRUFBRSxDQUFDLEVBQUUsQ0FBQyxDQUFDLEVBQUU7WUFDL0IsTUFBTSxJQUFJLEdBQWU7Z0JBQ3ZCLFlBQVksRUFBRSxJQUFJO2dCQUNsQixJQUFJO2dCQUNKLElBQUksRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFlBQVksRUFBRSxZQUFZLEVBQUUsSUFBSSxDQUFDO2FBQ2pELENBQUM7WUFDRixJQUFJLENBQUMsT0FBTyxDQUFDLEVBQUUsT0FBTyxFQUFFLElBQUksRUFBRSxDQUFDLENBQUM7U0FDakM7UUFFRCwwQkFBMEI7UUFDMUIsTUFBTSxJQUFJLEdBQUcsSUFBSSxrRUFBYyxDQUFDLEVBQUUsSUFBSSxFQUFFLFVBQVUsRUFBRSxDQUFDLENBQUM7UUFFdEQsdUVBQXVFO1FBQ3ZFLE1BQU0sY0FBYyxHQUFHLENBQUMsUUFBb0MsRUFBUSxFQUFFO1lBQ3BFLElBQUksQ0FBQyxLQUFNLENBQUMsTUFBTSxtQ0FDYiw0RUFBd0IsR0FDdkIsUUFBUSxDQUFDLEdBQUcsQ0FBQyxjQUFjLENBQUMsQ0FBQyxTQUF3QixDQUMxRCxDQUFDO1FBQ0osQ0FBQyxDQUFDO1FBQ0YsS0FBSyxPQUFPLENBQUMsR0FBRyxDQUFDO1lBQ2YsZUFBZSxDQUFDLElBQUksQ0FBQyx5Q0FBeUMsQ0FBQztZQUMvRCxHQUFHLENBQUMsUUFBUTtTQUNiLENBQUMsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLFFBQVEsQ0FBQyxFQUFFLEVBQUU7WUFDckIsY0FBYyxDQUFDLFFBQVEsQ0FBQyxDQUFDO1lBQ3pCLFFBQVEsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLGNBQWMsQ0FBQyxDQUFDO1FBQzNDLENBQUMsQ0FBQyxDQUFDO1FBRUgsdUJBQXVCO1FBQ3ZCLFNBQVMsQ0FBQyxrQkFBa0IsQ0FDMUIsbURBQW1ELEVBQ25EO1lBQ0UsSUFBSTtZQUNKLEtBQUssRUFBRSxPQUFPO1lBQ2QsSUFBSSxFQUFFLENBQUM7WUFDUCxRQUFRLEVBQUUsR0FBRyxFQUFFO2dCQUNiLE9BQU8sQ0FDTCxDQUFDLENBQUMsS0FBSyxDQUFDLGFBQWEsSUFBSSxhQUFhLENBQUMsR0FBRyxDQUFDLEtBQUssQ0FBQyxhQUFhLENBQUMsQ0FDaEUsQ0FBQztZQUNKLENBQUM7U0FDRixDQUNGLENBQUM7SUFDSixDQUFDO0NBQ0YsQ0FBQztBQUVGOztHQUVHO0FBQ0gsTUFBTSxPQUFPLEdBQWlDLENBQUMsTUFBTSxFQUFFLGNBQWMsQ0FBQyxDQUFDO0FBQ3ZFLGlFQUFlLE9BQU8sRUFBQztBQUV2Qjs7R0FFRztBQUNILFNBQVMsUUFBUSxDQUNmLEdBQW9CLEVBQ3BCLGNBQStCLEVBQy9CLGNBQW1DLEVBQ25DLGVBQWlDLEVBQ2pDLFVBQXVCLEVBQ3ZCLGNBQXNDLEVBQ3RDLE9BQStCLEVBQy9CLFFBQTBCLEVBQzFCLElBQXNCLEVBQ3RCLFFBQWdDLEVBQ2hDLGNBQTZDO0lBRTdDLE1BQU0sRUFBRSxHQUFHLE1BQU0sQ0FBQyxFQUFFLENBQUM7SUFDckIsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUM1QyxNQUFNLFNBQVMsR0FBRyxRQUFRLENBQUM7SUFDM0IsTUFBTSxPQUFPLEdBQUcsSUFBSSxxRUFBaUIsQ0FBQztRQUNwQyxjQUFjO1FBQ2QsY0FBYyxFQUFFO1lBQ2QsSUFBSSxFQUFFLCtDQUFPO1lBQ2IsU0FBUyxFQUFFLENBQUMsVUFBVSxFQUFFLEdBQUcsQ0FBQztZQUM1QixVQUFVLEVBQUUsQ0FBQyxVQUFVLEVBQUUsR0FBRyxDQUFDLENBQUMsMENBQTBDO1NBQ3pFO0tBQ0YsQ0FBQyxDQUFDO0lBQ0gsTUFBTSxFQUFFLFFBQVEsRUFBRSxRQUFRLEVBQUUsS0FBSyxFQUFFLEdBQUcsR0FBRyxDQUFDO0lBQzFDLE1BQU0sT0FBTyxHQUFHLElBQUksK0RBQWEsQ0FBOEI7UUFDN0QsU0FBUztLQUNWLENBQUMsQ0FBQztJQUNILE1BQU0sU0FBUyxHQUFHLEdBQUcsRUFBRSxDQUNyQixPQUFPLENBQUMsYUFBYSxLQUFLLElBQUk7UUFDOUIsT0FBTyxDQUFDLGFBQWEsS0FBSyxLQUFLLENBQUMsYUFBYSxDQUFDO0lBRWhELE1BQU0sMEJBQTBCLEdBQUcsSUFBSSxHQUFHLENBQTBCO1FBQ2xFO1lBQ0UsUUFBUTtZQUNSO2dCQUNFO29CQUNFLE9BQU8sRUFBRSxJQUFJO29CQUNiLFFBQVEsRUFBRSxzQkFBc0I7b0JBQ2hDLGFBQWEsRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGFBQWEsQ0FBQztvQkFDdEMsWUFBWSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsaUJBQWlCLENBQUM7b0JBQ3pDLE9BQU8sRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLDBCQUEwQixDQUFDO2lCQUM5QzthQUNGO1NBQ0Y7UUFDRDtZQUNFLE9BQU87WUFDUDtnQkFDRTtvQkFDRSxPQUFPLEVBQUUsSUFBSTtvQkFDYixRQUFRLEVBQUUscUJBQXFCO29CQUMvQixhQUFhLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxZQUFZLENBQUM7b0JBQ3JDLFlBQVksRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGdCQUFnQixDQUFDO29CQUN4QyxPQUFPLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyx5QkFBeUIsQ0FBQztpQkFDN0M7YUFDRjtTQUNGO1FBQ0Q7WUFDRSxHQUFHO1lBQ0g7Z0JBQ0U7b0JBQ0UsT0FBTyxFQUFFLEdBQUc7b0JBQ1osUUFBUSxFQUFFLHdCQUF3QjtvQkFDbEMsYUFBYSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsUUFBUSxDQUFDO29CQUNqQyxZQUFZLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxZQUFZLENBQUM7b0JBQ3BDLE9BQU8sRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLHFCQUFxQixDQUFDO2lCQUN6QzthQUNGO1NBQ0Y7S0FDRixDQUFDLENBQUM7SUFFSCxrSkFBa0o7SUFDbEosTUFBTSwyQkFBMkIsR0FBRyxLQUFLLElBQWlDLEVBQUU7O1FBQzFFLE1BQU0sWUFBWSxHQUFHLEdBQUcsQ0FBQyxjQUFjLENBQUMsV0FBVyxDQUFDO1FBQ3BELE1BQU0sWUFBWSxDQUFDLEtBQUssQ0FBQztRQUN6QixJQUFJLFNBQVMsR0FBRyxJQUFJLEdBQUcsRUFBaUIsQ0FBQztRQUN6QyxNQUFNLEtBQUssZUFBRyxZQUFZLENBQUMsS0FBSywwQ0FBRSxXQUFXLG1DQUFJLEVBQUUsQ0FBQztRQUNwRCxNQUFNLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsRUFBRTtZQUNoQyxNQUFNLFNBQVMsR0FBRyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7WUFDOUIsSUFBSSxTQUFTLEVBQUU7Z0JBQ2IsTUFBTSxJQUFJLEdBQUcsMEJBQTBCLENBQUMsR0FBRyxDQUFDLFNBQVMsQ0FBQyxRQUFRLENBQUMsQ0FBQztnQkFDaEUsSUFBSSxhQUFKLElBQUksdUJBQUosSUFBSSxDQUFFLE9BQU8sQ0FBQyxHQUFHLENBQUMsRUFBRSxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsR0FBRyxDQUFDLEVBQUU7YUFDMUM7UUFDSCxDQUFDLENBQUMsQ0FBQztRQUNILE9BQU8sU0FBUyxDQUFDO0lBQ25CLENBQUMsQ0FBQztJQUVGLDRCQUE0QjtJQUM1QixJQUFJLFFBQVEsRUFBRTtRQUNaLEtBQUssUUFBUSxDQUFDLE9BQU8sQ0FBQyxPQUFPLEVBQUU7WUFDN0IsT0FBTyxFQUFFLGlCQUFpQjtZQUMxQixJQUFJLEVBQUUsTUFBTSxDQUFDLEVBQUUsQ0FBQyxDQUFDLEVBQUUsSUFBSSxFQUFFLE1BQU0sQ0FBQyxPQUFPLENBQUMsSUFBSSxFQUFFLE9BQU8sRUFBRSwrQ0FBTyxFQUFFLENBQUM7WUFDakUsSUFBSSxFQUFFLE1BQU0sQ0FBQyxFQUFFLENBQUMsTUFBTSxDQUFDLE9BQU8sQ0FBQyxJQUFJO1NBQ3BDLENBQUMsQ0FBQztLQUNKO0lBRUQseUNBQXlDO0lBQ3pDLDJDQUEyQztJQUMzQyxPQUFPLENBQUMsR0FBRyxDQUFDLENBQUMsZUFBZSxDQUFDLElBQUksQ0FBQyxFQUFFLENBQUMsRUFBRSxRQUFRLENBQUMsQ0FBQztTQUM5QyxJQUFJLENBQUMsQ0FBQyxDQUFDLFFBQVEsQ0FBQyxFQUFFLEVBQUU7UUFDbkIsK0RBQXVCLENBQUMsUUFBUSxFQUFFLFFBQVEsQ0FBQyxDQUFDO1FBQzVDLDhEQUFzQixDQUFDLE9BQU8sQ0FBQyxDQUFDO1FBQ2hDLFFBQVEsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLEdBQUcsRUFBRTtZQUM1QiwrREFBdUIsQ0FBQyxRQUFRLEVBQUUsUUFBUSxDQUFDLENBQUM7WUFDNUMsOERBQXNCLENBQUMsT0FBTyxDQUFDLENBQUM7UUFDbEMsQ0FBQyxDQUFDLENBQUM7SUFDTCxDQUFDLENBQUM7U0FDRCxLQUFLLENBQUMsQ0FBQyxNQUFhLEVBQUUsRUFBRTtRQUN2QixPQUFPLENBQUMsS0FBSyxDQUFDLE1BQU0sQ0FBQyxPQUFPLENBQUMsQ0FBQztRQUM5Qiw4REFBc0IsQ0FBQyxPQUFPLENBQUMsQ0FBQztJQUNsQyxDQUFDLENBQUMsQ0FBQztJQUVMLE9BQU8sQ0FBQyxhQUFhLENBQUMsT0FBTyxDQUFDLENBQUMsTUFBTSxFQUFFLE1BQU0sRUFBRSxFQUFFO1FBQy9DLDZEQUE2RDtRQUM3RCxNQUFNLENBQUMsT0FBTyxDQUFDLFdBQVcsQ0FBQyxPQUFPLENBQUMsR0FBRyxFQUFFO1lBQ3RDLEtBQUssT0FBTyxDQUFDLElBQUksQ0FBQyxNQUFNLENBQUMsQ0FBQztRQUM1QixDQUFDLENBQUMsQ0FBQztRQUNILEtBQUssT0FBTyxDQUFDLEdBQUcsQ0FBQyxNQUFNLENBQUMsQ0FBQztRQUN6Qiw2REFBcUIsQ0FBQyxNQUFNLENBQUMsT0FBTyxDQUFDLENBQUM7SUFDeEMsQ0FBQyxDQUFDLENBQUM7SUFDSCxHQUFHLENBQUMsV0FBVyxDQUFDLGdCQUFnQixDQUFDLE9BQU8sQ0FBQyxDQUFDO0lBRTFDLHNDQUFzQztJQUN0QyxPQUFPLENBQUMsV0FBVyxDQUFDLE9BQU8sQ0FBQyxDQUFDLE1BQU0sRUFBRSxNQUFNLEVBQUUsRUFBRTtRQUM3Qyw2REFBcUIsQ0FBQyxNQUFNLENBQUMsT0FBTyxDQUFDLENBQUM7SUFDeEMsQ0FBQyxDQUFDLENBQUM7SUFFSCw0REFBb0IsQ0FDbEIsUUFBUSxFQUNSLGVBQWUsRUFDZixLQUFLLEVBQ0wsRUFBRSxFQUNGLFNBQVMsRUFDVCxPQUFPLEVBQ1AsY0FBYyxDQUNmLENBQUM7SUFFRixvREFBb0Q7SUFDcEQsSUFBSSxRQUFRLEVBQUU7UUFDWixpRUFBeUIsQ0FBQyxRQUFRLEVBQUUsS0FBSyxDQUFDLENBQUM7S0FDNUM7SUFFRCxJQUFJLE9BQU8sRUFBRTtRQUNYLGdFQUF3QixDQUFDLE9BQU8sRUFBRSxLQUFLLENBQUMsQ0FBQztLQUMxQztJQUVELElBQUksSUFBSSxFQUFFO1FBQ1IsNkRBQXFCLENBQ25CLElBQUksRUFDSixRQUFRLEVBQ1IsT0FBTyxFQUNQLEtBQUssRUFDTCxjQUFjLEVBQ2QsY0FBYyxDQUNmLENBQUM7S0FDSDtJQUVELDJCQUEyQixFQUFFO1NBQzFCLElBQUksQ0FBQyx3QkFBd0IsQ0FBQyxFQUFFO1FBQy9CLElBQUksUUFBUSxFQUFFO1lBQ1osK0VBQXVDLENBQ3JDLFFBQVEsRUFDUixLQUFLLEVBQ0wsd0JBQXdCLENBQ3pCLENBQUM7U0FDSDtRQUVELElBQUksT0FBTyxFQUFFO1lBQ1gsOEVBQXNDLENBQ3BDLE9BQU8sRUFDUCxLQUFLLEVBQ0wsd0JBQXdCLENBQ3pCLENBQUM7U0FDSDtRQUVELElBQUksSUFBSSxFQUFFO1lBQ1IsMkVBQW1DLENBQUMsSUFBSSxFQUFFLHdCQUF3QixDQUFDLENBQUM7U0FDckU7SUFDSCxDQUFDLENBQUM7U0FDRCxLQUFLLENBQUMsQ0FBQyxNQUFhLEVBQUUsRUFBRTtRQUN2QixPQUFPLENBQUMsS0FBSyxDQUFDLE1BQU0sQ0FBQyxPQUFPLENBQUMsQ0FBQztJQUNoQyxDQUFDLENBQUMsQ0FBQztJQUVMLE9BQU8sT0FBTyxDQUFDO0FBQ2pCLENBQUMiLCJmaWxlIjoicGFja2FnZXNfZmlsZWVkaXRvci1leHRlbnNpb25fbGliX2luZGV4X2pzLjU5YzRmMWU4ODFkMjhhMzI4MTQyLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQge1xuICBDbGlwYm9hcmQsXG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgSVNlc3Npb25Db250ZXh0RGlhbG9ncyxcbiAgc2Vzc2lvbkNvbnRleHREaWFsb2dzLFxuICBXaWRnZXRUcmFja2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IENvZGVFZGl0b3IgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlZWRpdG9yJztcbmltcG9ydCB7IENvZGVNaXJyb3JFZGl0b3IgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlbWlycm9yJztcbmltcG9ydCB7IElDb25zb2xlVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2NvbnNvbGUnO1xuaW1wb3J0IHsgTWFya2Rvd25Db2RlQmxvY2tzLCBQYXRoRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7IElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IElGaWxlQnJvd3NlckZhY3RvcnkgfSBmcm9tICdAanVweXRlcmxhYi9maWxlYnJvd3Nlcic7XG5pbXBvcnQgeyBGaWxlRWRpdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZmlsZWVkaXRvcic7XG5pbXBvcnQgeyBJTGF1bmNoZXIgfSBmcm9tICdAanVweXRlcmxhYi9sYXVuY2hlcic7XG5pbXBvcnQge1xuICBJRWRpdE1lbnUsXG4gIElGaWxlTWVudSxcbiAgSU1haW5NZW51LFxuICBJUnVuTWVudSxcbiAgSVZpZXdNZW51XG59IGZyb20gJ0BqdXB5dGVybGFiL21haW5tZW51JztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgVHJhbnNsYXRpb25CdW5kbGUgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQge1xuICBjb25zb2xlSWNvbixcbiAgY29weUljb24sXG4gIGN1dEljb24sXG4gIExhYkljb24sXG4gIG1hcmtkb3duSWNvbixcbiAgcGFzdGVJY29uLFxuICByZWRvSWNvbixcbiAgdGV4dEVkaXRvckljb24sXG4gIHVuZG9JY29uXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgQ29tbWFuZFJlZ2lzdHJ5IH0gZnJvbSAnQGx1bWluby9jb21tYW5kcyc7XG5pbXBvcnQge1xuICBKU09OT2JqZWN0LFxuICBSZWFkb25seUpTT05PYmplY3QsXG4gIFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3Rcbn0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuXG5jb25zdCBhdXRvQ2xvc2luZ0JyYWNrZXRzTm90ZWJvb2sgPSAnbm90ZWJvb2s6dG9nZ2xlLWF1dG9jbG9zaW5nLWJyYWNrZXRzJztcbmNvbnN0IGF1dG9DbG9zaW5nQnJhY2tldHNDb25zb2xlID0gJ2NvbnNvbGU6dG9nZ2xlLWF1dG9jbG9zaW5nLWJyYWNrZXRzJztcbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIGZpbGVlZGl0b3IgcGx1Z2luLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgY3JlYXRlTmV3ID0gJ2ZpbGVlZGl0b3I6Y3JlYXRlLW5ldyc7XG5cbiAgZXhwb3J0IGNvbnN0IGNyZWF0ZU5ld01hcmtkb3duID0gJ2ZpbGVlZGl0b3I6Y3JlYXRlLW5ldy1tYXJrZG93bi1maWxlJztcblxuICBleHBvcnQgY29uc3QgY2hhbmdlRm9udFNpemUgPSAnZmlsZWVkaXRvcjpjaGFuZ2UtZm9udC1zaXplJztcblxuICBleHBvcnQgY29uc3QgbGluZU51bWJlcnMgPSAnZmlsZWVkaXRvcjp0b2dnbGUtbGluZS1udW1iZXJzJztcblxuICBleHBvcnQgY29uc3QgbGluZVdyYXAgPSAnZmlsZWVkaXRvcjp0b2dnbGUtbGluZS13cmFwJztcblxuICBleHBvcnQgY29uc3QgY2hhbmdlVGFicyA9ICdmaWxlZWRpdG9yOmNoYW5nZS10YWJzJztcblxuICBleHBvcnQgY29uc3QgbWF0Y2hCcmFja2V0cyA9ICdmaWxlZWRpdG9yOnRvZ2dsZS1tYXRjaC1icmFja2V0cyc7XG5cbiAgZXhwb3J0IGNvbnN0IGF1dG9DbG9zaW5nQnJhY2tldHMgPSAnZmlsZWVkaXRvcjp0b2dnbGUtYXV0b2Nsb3NpbmctYnJhY2tldHMnO1xuXG4gIGV4cG9ydCBjb25zdCBhdXRvQ2xvc2luZ0JyYWNrZXRzVW5pdmVyc2FsID1cbiAgICAnZmlsZWVkaXRvcjp0b2dnbGUtYXV0b2Nsb3NpbmctYnJhY2tldHMtdW5pdmVyc2FsJztcblxuICBleHBvcnQgY29uc3QgY3JlYXRlQ29uc29sZSA9ICdmaWxlZWRpdG9yOmNyZWF0ZS1jb25zb2xlJztcblxuICBleHBvcnQgY29uc3QgcmVwbGFjZVNlbGVjdGlvbiA9ICdmaWxlZWRpdG9yOnJlcGxhY2Utc2VsZWN0aW9uJztcblxuICBleHBvcnQgY29uc3QgcnVuQ29kZSA9ICdmaWxlZWRpdG9yOnJ1bi1jb2RlJztcblxuICBleHBvcnQgY29uc3QgcnVuQWxsQ29kZSA9ICdmaWxlZWRpdG9yOnJ1bi1hbGwnO1xuXG4gIGV4cG9ydCBjb25zdCBtYXJrZG93blByZXZpZXcgPSAnZmlsZWVkaXRvcjptYXJrZG93bi1wcmV2aWV3JztcblxuICBleHBvcnQgY29uc3QgdW5kbyA9ICdmaWxlZWRpdG9yOnVuZG8nO1xuXG4gIGV4cG9ydCBjb25zdCByZWRvID0gJ2ZpbGVlZGl0b3I6cmVkbyc7XG5cbiAgZXhwb3J0IGNvbnN0IGN1dCA9ICdmaWxlZWRpdG9yOmN1dCc7XG5cbiAgZXhwb3J0IGNvbnN0IGNvcHkgPSAnZmlsZWVkaXRvcjpjb3B5JztcblxuICBleHBvcnQgY29uc3QgcGFzdGUgPSAnZmlsZWVkaXRvcjpwYXN0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNlbGVjdEFsbCA9ICdmaWxlZWRpdG9yOnNlbGVjdC1hbGwnO1xufVxuXG5leHBvcnQgaW50ZXJmYWNlIElGaWxlVHlwZURhdGEgZXh0ZW5kcyBSZWFkb25seUpTT05PYmplY3Qge1xuICBmaWxlRXh0OiBzdHJpbmc7XG4gIGljb25OYW1lOiBzdHJpbmc7XG4gIGxhdW5jaGVyTGFiZWw6IHN0cmluZztcbiAgcGFsZXR0ZUxhYmVsOiBzdHJpbmc7XG4gIGNhcHRpb246IHN0cmluZztcbn1cblxuLyoqXG4gKiBUaGUgbmFtZSBvZiB0aGUgZmFjdG9yeSB0aGF0IGNyZWF0ZXMgZWRpdG9yIHdpZGdldHMuXG4gKi9cbmV4cG9ydCBjb25zdCBGQUNUT1JZID0gJ0VkaXRvcic7XG5cbmNvbnN0IHVzZXJTZXR0aW5ncyA9IFtcbiAgJ2F1dG9DbG9zaW5nQnJhY2tldHMnLFxuICAnY3Vyc29yQmxpbmtSYXRlJyxcbiAgJ2ZvbnRGYW1pbHknLFxuICAnZm9udFNpemUnLFxuICAnbGluZUhlaWdodCcsXG4gICdsaW5lTnVtYmVycycsXG4gICdsaW5lV3JhcCcsXG4gICdtYXRjaEJyYWNrZXRzJyxcbiAgJ3JlYWRPbmx5JyxcbiAgJ2luc2VydFNwYWNlcycsXG4gICd0YWJTaXplJyxcbiAgJ3dvcmRXcmFwQ29sdW1uJyxcbiAgJ3J1bGVycycsXG4gICdjb2RlRm9sZGluZydcbl07XG5cbmZ1bmN0aW9uIGZpbHRlclVzZXJTZXR0aW5ncyhjb25maWc6IENvZGVFZGl0b3IuSUNvbmZpZyk6IENvZGVFZGl0b3IuSUNvbmZpZyB7XG4gIGNvbnN0IGZpbHRlcmVkQ29uZmlnID0geyAuLi5jb25maWcgfTtcbiAgLy8gRGVsZXRlIHBhcnRzIG9mIHRoZSBjb25maWcgdGhhdCBhcmUgbm90IHVzZXIgc2V0dGluZ3MgKGxpa2UgaGFuZGxlUGFzdGUpLlxuICBmb3IgKGxldCBrIG9mIE9iamVjdC5rZXlzKGNvbmZpZykpIHtcbiAgICBpZiAoIXVzZXJTZXR0aW5ncy5pbmNsdWRlcyhrKSkge1xuICAgICAgZGVsZXRlIChjb25maWcgYXMgYW55KVtrXTtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIGZpbHRlcmVkQ29uZmlnO1xufVxuXG5sZXQgY29uZmlnOiBDb2RlRWRpdG9yLklDb25maWcgPSBmaWx0ZXJVc2VyU2V0dGluZ3MoQ29kZUVkaXRvci5kZWZhdWx0Q29uZmlnKTtcblxuLyoqXG4gKiBBIHV0aWxpdHkgY2xhc3MgZm9yIGFkZGluZyBjb21tYW5kcyBhbmQgbWVudSBpdGVtcyxcbiAqIGZvciB1c2UgYnkgdGhlIEZpbGUgRWRpdG9yIGV4dGVuc2lvbiBvciBvdGhlciBFZGl0b3IgZXh0ZW5zaW9ucy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDb21tYW5kcyB7XG4gIC8qKlxuICAgKiBBY2Nlc3NvciBmdW5jdGlvbiB0aGF0IHJldHVybnMgdGhlIGNyZWF0ZUNvbnNvbGUgZnVuY3Rpb24gZm9yIHVzZSBieSBDcmVhdGUgQ29uc29sZSBjb21tYW5kc1xuICAgKi9cbiAgZnVuY3Rpb24gZ2V0Q3JlYXRlQ29uc29sZUZ1bmN0aW9uKFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnlcbiAgKTogKFxuICAgIHdpZGdldDogSURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+LFxuICAgIGFyZ3M/OiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0XG4gICkgPT4gUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIGFzeW5jIGZ1bmN0aW9uIGNyZWF0ZUNvbnNvbGUoXG4gICAgICB3aWRnZXQ6IElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPixcbiAgICAgIGFyZ3M/OiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0XG4gICAgKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICBjb25zdCBvcHRpb25zID0gYXJncyB8fCB7fTtcbiAgICAgIGNvbnN0IGNvbnNvbGUgPSBhd2FpdCBjb21tYW5kcy5leGVjdXRlKCdjb25zb2xlOmNyZWF0ZScsIHtcbiAgICAgICAgYWN0aXZhdGU6IG9wdGlvbnNbJ2FjdGl2YXRlJ10sXG4gICAgICAgIG5hbWU6IHdpZGdldC5jb250ZXh0LmNvbnRlbnRzTW9kZWw/Lm5hbWUsXG4gICAgICAgIHBhdGg6IHdpZGdldC5jb250ZXh0LnBhdGgsXG4gICAgICAgIHByZWZlcnJlZExhbmd1YWdlOiB3aWRnZXQuY29udGV4dC5tb2RlbC5kZWZhdWx0S2VybmVsTGFuZ3VhZ2UsXG4gICAgICAgIHJlZjogd2lkZ2V0LmlkLFxuICAgICAgICBpbnNlcnRNb2RlOiAnc3BsaXQtYm90dG9tJ1xuICAgICAgfSk7XG5cbiAgICAgIHdpZGdldC5jb250ZXh0LnBhdGhDaGFuZ2VkLmNvbm5lY3QoKHNlbmRlciwgdmFsdWUpID0+IHtcbiAgICAgICAgY29uc29sZS5zZXNzaW9uLnNldFBhdGgodmFsdWUpO1xuICAgICAgICBjb25zb2xlLnNlc3Npb24uc2V0TmFtZSh3aWRnZXQuY29udGV4dC5jb250ZW50c01vZGVsPy5uYW1lKTtcbiAgICAgIH0pO1xuICAgIH07XG4gIH1cblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBzZXR0aW5nIHZhbHVlcy5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiB1cGRhdGVTZXR0aW5ncyhcbiAgICBzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MsXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeVxuICApOiB2b2lkIHtcbiAgICBjb25maWcgPSBmaWx0ZXJVc2VyU2V0dGluZ3Moe1xuICAgICAgLi4uQ29kZUVkaXRvci5kZWZhdWx0Q29uZmlnLFxuICAgICAgLi4uKHNldHRpbmdzLmdldCgnZWRpdG9yQ29uZmlnJykuY29tcG9zaXRlIGFzIEpTT05PYmplY3QpXG4gICAgfSk7XG5cbiAgICAvLyBUcmlnZ2VyIGEgcmVmcmVzaCBvZiB0aGUgcmVuZGVyZWQgY29tbWFuZHNcbiAgICBjb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgc2V0dGluZ3Mgb2YgdGhlIGN1cnJlbnQgdHJhY2tlciBpbnN0YW5jZXMuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gdXBkYXRlVHJhY2tlcihcbiAgICB0cmFja2VyOiBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj5cbiAgKTogdm9pZCB7XG4gICAgdHJhY2tlci5mb3JFYWNoKHdpZGdldCA9PiB7XG4gICAgICB1cGRhdGVXaWRnZXQod2lkZ2V0LmNvbnRlbnQpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgc2V0dGluZ3Mgb2YgYSB3aWRnZXQuXG4gICAqIFNraXAgZ2xvYmFsIHNldHRpbmdzIGZvciB0cmFuc2llbnQgZWRpdG9yIHNwZWNpZmljIGNvbmZpZ3MuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gdXBkYXRlV2lkZ2V0KHdpZGdldDogRmlsZUVkaXRvcik6IHZvaWQge1xuICAgIGNvbnN0IGVkaXRvciA9IHdpZGdldC5lZGl0b3I7XG4gICAgbGV0IGVkaXRvck9wdGlvbnM6IGFueSA9IHt9O1xuICAgIE9iamVjdC5rZXlzKGNvbmZpZykuZm9yRWFjaCgoa2V5OiBrZXlvZiBDb2RlRWRpdG9yLklDb25maWcpID0+IHtcbiAgICAgIGVkaXRvck9wdGlvbnNba2V5XSA9IGNvbmZpZ1trZXldO1xuICAgIH0pO1xuICAgIGVkaXRvci5zZXRPcHRpb25zKGVkaXRvck9wdGlvbnMpO1xuICB9XG5cbiAgLyoqXG4gICAqIFdyYXBwZXIgZnVuY3Rpb24gZm9yIGFkZGluZyB0aGUgZGVmYXVsdCBGaWxlIEVkaXRvciBjb21tYW5kc1xuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZENvbW1hbmRzKFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnksXG4gICAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZSxcbiAgICBpZDogc3RyaW5nLFxuICAgIGlzRW5hYmxlZDogKCkgPT4gYm9vbGVhbixcbiAgICB0cmFja2VyOiBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4sXG4gICAgYnJvd3NlckZhY3Rvcnk6IElGaWxlQnJvd3NlckZhY3RvcnlcbiAgKTogdm9pZCB7XG4gICAgLy8gQWRkIGEgY29tbWFuZCB0byBjaGFuZ2UgZm9udCBzaXplLlxuICAgIGFkZENoYW5nZUZvbnRTaXplQ29tbWFuZChjb21tYW5kcywgc2V0dGluZ1JlZ2lzdHJ5LCB0cmFucywgaWQpO1xuXG4gICAgYWRkTGluZU51bWJlcnNDb21tYW5kKGNvbW1hbmRzLCBzZXR0aW5nUmVnaXN0cnksIHRyYW5zLCBpZCwgaXNFbmFibGVkKTtcblxuICAgIGFkZFdvcmRXcmFwQ29tbWFuZChjb21tYW5kcywgc2V0dGluZ1JlZ2lzdHJ5LCB0cmFucywgaWQsIGlzRW5hYmxlZCk7XG5cbiAgICBhZGRDaGFuZ2VUYWJzQ29tbWFuZChjb21tYW5kcywgc2V0dGluZ1JlZ2lzdHJ5LCB0cmFucywgaWQpO1xuXG4gICAgYWRkTWF0Y2hCcmFja2V0c0NvbW1hbmQoY29tbWFuZHMsIHNldHRpbmdSZWdpc3RyeSwgdHJhbnMsIGlkLCBpc0VuYWJsZWQpO1xuXG4gICAgYWRkQXV0b0Nsb3NpbmdCcmFja2V0c0NvbW1hbmQoY29tbWFuZHMsIHNldHRpbmdSZWdpc3RyeSwgdHJhbnMsIGlkKTtcblxuICAgIGFkZFJlcGxhY2VTZWxlY3Rpb25Db21tYW5kKGNvbW1hbmRzLCB0cmFja2VyLCB0cmFucywgaXNFbmFibGVkKTtcblxuICAgIGFkZENyZWF0ZUNvbnNvbGVDb21tYW5kKGNvbW1hbmRzLCB0cmFja2VyLCB0cmFucywgaXNFbmFibGVkKTtcblxuICAgIGFkZFJ1bkNvZGVDb21tYW5kKGNvbW1hbmRzLCB0cmFja2VyLCB0cmFucywgaXNFbmFibGVkKTtcblxuICAgIGFkZFJ1bkFsbENvZGVDb21tYW5kKGNvbW1hbmRzLCB0cmFja2VyLCB0cmFucywgaXNFbmFibGVkKTtcblxuICAgIGFkZE1hcmtkb3duUHJldmlld0NvbW1hbmQoY29tbWFuZHMsIHRyYWNrZXIsIHRyYW5zKTtcblxuICAgIC8vIEFkZCBhIGNvbW1hbmQgZm9yIGNyZWF0aW5nIGEgbmV3IHRleHQgZmlsZS5cbiAgICBhZGRDcmVhdGVOZXdDb21tYW5kKGNvbW1hbmRzLCBicm93c2VyRmFjdG9yeSwgdHJhbnMpO1xuXG4gICAgLy8gQWRkIGEgY29tbWFuZCBmb3IgY3JlYXRpbmcgYSBuZXcgTWFya2Rvd24gZmlsZS5cbiAgICBhZGRDcmVhdGVOZXdNYXJrZG93bkNvbW1hbmQoY29tbWFuZHMsIGJyb3dzZXJGYWN0b3J5LCB0cmFucyk7XG5cbiAgICBhZGRVbmRvQ29tbWFuZChjb21tYW5kcywgdHJhY2tlciwgdHJhbnMsIGlzRW5hYmxlZCk7XG5cbiAgICBhZGRSZWRvQ29tbWFuZChjb21tYW5kcywgdHJhY2tlciwgdHJhbnMsIGlzRW5hYmxlZCk7XG5cbiAgICBhZGRDdXRDb21tYW5kKGNvbW1hbmRzLCB0cmFja2VyLCB0cmFucywgaXNFbmFibGVkKTtcblxuICAgIGFkZENvcHlDb21tYW5kKGNvbW1hbmRzLCB0cmFja2VyLCB0cmFucywgaXNFbmFibGVkKTtcblxuICAgIGFkZFBhc3RlQ29tbWFuZChjb21tYW5kcywgdHJhY2tlciwgdHJhbnMsIGlzRW5hYmxlZCk7XG5cbiAgICBhZGRTZWxlY3RBbGxDb21tYW5kKGNvbW1hbmRzLCB0cmFja2VyLCB0cmFucywgaXNFbmFibGVkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSBjb21tYW5kIHRvIGNoYW5nZSBmb250IHNpemUgZm9yIEZpbGUgRWRpdG9yXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkQ2hhbmdlRm9udFNpemVDb21tYW5kKFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnksXG4gICAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZSxcbiAgICBpZDogc3RyaW5nXG4gICk6IHZvaWQge1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jaGFuZ2VGb250U2l6ZSwge1xuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IGRlbHRhID0gTnVtYmVyKGFyZ3NbJ2RlbHRhJ10pO1xuICAgICAgICBpZiAoTnVtYmVyLmlzTmFOKGRlbHRhKSkge1xuICAgICAgICAgIGNvbnNvbGUuZXJyb3IoXG4gICAgICAgICAgICBgJHtDb21tYW5kSURzLmNoYW5nZUZvbnRTaXplfTogZGVsdGEgYXJnIG11c3QgYmUgYSBudW1iZXJgXG4gICAgICAgICAgKTtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3Qgc3R5bGUgPSB3aW5kb3cuZ2V0Q29tcHV0ZWRTdHlsZShkb2N1bWVudC5kb2N1bWVudEVsZW1lbnQpO1xuICAgICAgICBjb25zdCBjc3NTaXplID0gcGFyc2VJbnQoXG4gICAgICAgICAgc3R5bGUuZ2V0UHJvcGVydHlWYWx1ZSgnLS1qcC1jb2RlLWZvbnQtc2l6ZScpLFxuICAgICAgICAgIDEwXG4gICAgICAgICk7XG4gICAgICAgIGNvbnN0IGN1cnJlbnRTaXplID0gY29uZmlnLmZvbnRTaXplIHx8IGNzc1NpemU7XG4gICAgICAgIGNvbmZpZy5mb250U2l6ZSA9IGN1cnJlbnRTaXplICsgZGVsdGE7XG4gICAgICAgIHJldHVybiBzZXR0aW5nUmVnaXN0cnlcbiAgICAgICAgICAuc2V0KGlkLCAnZWRpdG9yQ29uZmlnJywgKGNvbmZpZyBhcyB1bmtub3duKSBhcyBKU09OT2JqZWN0KVxuICAgICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCAke2lkfTogJHtyZWFzb24ubWVzc2FnZX1gKTtcbiAgICAgICAgICB9KTtcbiAgICAgIH0sXG4gICAgICBsYWJlbDogYXJncyA9PiB7XG4gICAgICAgIGlmICgoYXJncy5kZWx0YSA/PyAwKSA+IDApIHtcbiAgICAgICAgICByZXR1cm4gYXJncy5pc01lbnVcbiAgICAgICAgICAgID8gdHJhbnMuX18oJ0luY3JlYXNlIFRleHQgRWRpdG9yIEZvbnQgU2l6ZScpXG4gICAgICAgICAgICA6IHRyYW5zLl9fKCdJbmNyZWFzZSBGb250IFNpemUnKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXR1cm4gYXJncy5pc01lbnVcbiAgICAgICAgICAgID8gdHJhbnMuX18oJ0RlY3JlYXNlIFRleHQgRWRpdG9yIEZvbnQgU2l6ZScpXG4gICAgICAgICAgICA6IHRyYW5zLl9fKCdEZWNyZWFzZSBGb250IFNpemUnKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCB0aGUgTGluZSBOdW1iZXJzIGNvbW1hbmRcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhZGRMaW5lTnVtYmVyc0NvbW1hbmQoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlLFxuICAgIGlkOiBzdHJpbmcsXG4gICAgaXNFbmFibGVkOiAoKSA9PiBib29sZWFuXG4gICk6IHZvaWQge1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5saW5lTnVtYmVycywge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25maWcubGluZU51bWJlcnMgPSAhY29uZmlnLmxpbmVOdW1iZXJzO1xuICAgICAgICByZXR1cm4gc2V0dGluZ1JlZ2lzdHJ5XG4gICAgICAgICAgLnNldChpZCwgJ2VkaXRvckNvbmZpZycsIChjb25maWcgYXMgdW5rbm93bikgYXMgSlNPTk9iamVjdClcbiAgICAgICAgICAuY2F0Y2goKHJlYXNvbjogRXJyb3IpID0+IHtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoYEZhaWxlZCB0byBzZXQgJHtpZH06ICR7cmVhc29uLm1lc3NhZ2V9YCk7XG4gICAgICAgICAgfSk7XG4gICAgICB9LFxuICAgICAgaXNFbmFibGVkLFxuICAgICAgaXNUb2dnbGVkOiAoKSA9PiBjb25maWcubGluZU51bWJlcnMsXG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0xpbmUgTnVtYmVycycpXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIHRoZSBXb3JkIFdyYXAgY29tbWFuZFxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZFdvcmRXcmFwQ29tbWFuZChcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGUsXG4gICAgaWQ6IHN0cmluZyxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IGJvb2xlYW5cbiAgKTogdm9pZCB7XG4gICAgdHlwZSB3cmFwcGluZ01vZGUgPSAnb24nIHwgJ29mZicgfCAnd29yZFdyYXBDb2x1bW4nIHwgJ2JvdW5kZWQnO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmxpbmVXcmFwLCB7XG4gICAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgICAgY29uZmlnLmxpbmVXcmFwID0gKGFyZ3NbJ21vZGUnXSBhcyB3cmFwcGluZ01vZGUpIHx8ICdvZmYnO1xuICAgICAgICByZXR1cm4gc2V0dGluZ1JlZ2lzdHJ5XG4gICAgICAgICAgLnNldChpZCwgJ2VkaXRvckNvbmZpZycsIChjb25maWcgYXMgdW5rbm93bikgYXMgSlNPTk9iamVjdClcbiAgICAgICAgICAuY2F0Y2goKHJlYXNvbjogRXJyb3IpID0+IHtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoYEZhaWxlZCB0byBzZXQgJHtpZH06ICR7cmVhc29uLm1lc3NhZ2V9YCk7XG4gICAgICAgICAgfSk7XG4gICAgICB9LFxuICAgICAgaXNFbmFibGVkLFxuICAgICAgaXNUb2dnbGVkOiBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgbGluZVdyYXAgPSAoYXJnc1snbW9kZSddIGFzIHdyYXBwaW5nTW9kZSkgfHwgJ29mZic7XG4gICAgICAgIHJldHVybiBjb25maWcubGluZVdyYXAgPT09IGxpbmVXcmFwO1xuICAgICAgfSxcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnV29yZCBXcmFwJylcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgY29tbWFuZCBmb3IgY2hhbmdpbmcgdGFicyBzaXplIG9yIHR5cGUgaW4gRmlsZSBFZGl0b3JcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhZGRDaGFuZ2VUYWJzQ29tbWFuZChcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGUsXG4gICAgaWQ6IHN0cmluZ1xuICApOiB2b2lkIHtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY2hhbmdlVGFicywge1xuICAgICAgbGFiZWw6IGFyZ3MgPT4ge1xuICAgICAgICBpZiAoYXJncy5pbnNlcnRTcGFjZXMpIHtcbiAgICAgICAgICByZXR1cm4gdHJhbnMuX24oXG4gICAgICAgICAgICAnU3BhY2VzOiAlMScsXG4gICAgICAgICAgICAnU3BhY2VzOiAlMScsXG4gICAgICAgICAgICAoYXJncy5zaXplIGFzIG51bWJlcikgPz8gMFxuICAgICAgICAgICk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgcmV0dXJuIHRyYW5zLl9fKCdJbmRlbnQgd2l0aCBUYWInKTtcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgICBjb25maWcudGFiU2l6ZSA9IChhcmdzWydzaXplJ10gYXMgbnVtYmVyKSB8fCA0O1xuICAgICAgICBjb25maWcuaW5zZXJ0U3BhY2VzID0gISFhcmdzWydpbnNlcnRTcGFjZXMnXTtcbiAgICAgICAgcmV0dXJuIHNldHRpbmdSZWdpc3RyeVxuICAgICAgICAgIC5zZXQoaWQsICdlZGl0b3JDb25maWcnLCAoY29uZmlnIGFzIHVua25vd24pIGFzIEpTT05PYmplY3QpXG4gICAgICAgICAgLmNhdGNoKChyZWFzb246IEVycm9yKSA9PiB7XG4gICAgICAgICAgICBjb25zb2xlLmVycm9yKGBGYWlsZWQgdG8gc2V0ICR7aWR9OiAke3JlYXNvbi5tZXNzYWdlfWApO1xuICAgICAgICAgIH0pO1xuICAgICAgfSxcbiAgICAgIGlzVG9nZ2xlZDogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IGluc2VydFNwYWNlcyA9ICEhYXJnc1snaW5zZXJ0U3BhY2VzJ107XG4gICAgICAgIGNvbnN0IHNpemUgPSAoYXJnc1snc2l6ZSddIGFzIG51bWJlcikgfHwgNDtcbiAgICAgICAgcmV0dXJuIGNvbmZpZy5pbnNlcnRTcGFjZXMgPT09IGluc2VydFNwYWNlcyAmJiBjb25maWcudGFiU2l6ZSA9PT0gc2l6ZTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgdGhlIE1hdGNoIEJyYWNrZXRzIGNvbW1hbmRcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhZGRNYXRjaEJyYWNrZXRzQ29tbWFuZChcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGUsXG4gICAgaWQ6IHN0cmluZyxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IGJvb2xlYW5cbiAgKTogdm9pZCB7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm1hdGNoQnJhY2tldHMsIHtcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgY29uZmlnLm1hdGNoQnJhY2tldHMgPSAhY29uZmlnLm1hdGNoQnJhY2tldHM7XG4gICAgICAgIHJldHVybiBzZXR0aW5nUmVnaXN0cnlcbiAgICAgICAgICAuc2V0KGlkLCAnZWRpdG9yQ29uZmlnJywgKGNvbmZpZyBhcyB1bmtub3duKSBhcyBKU09OT2JqZWN0KVxuICAgICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCAke2lkfTogJHtyZWFzb24ubWVzc2FnZX1gKTtcbiAgICAgICAgICB9KTtcbiAgICAgIH0sXG4gICAgICBsYWJlbDogdHJhbnMuX18oJ01hdGNoIEJyYWNrZXRzJyksXG4gICAgICBpc0VuYWJsZWQsXG4gICAgICBpc1RvZ2dsZWQ6ICgpID0+IGNvbmZpZy5tYXRjaEJyYWNrZXRzXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIHRoZSBBdXRvIENsb3NlIEJyYWNrZXRzIGZvciBUZXh0IEVkaXRvciBjb21tYW5kXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkQXV0b0Nsb3NpbmdCcmFja2V0c0NvbW1hbmQoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlLFxuICAgIGlkOiBzdHJpbmdcbiAgKTogdm9pZCB7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmF1dG9DbG9zaW5nQnJhY2tldHMsIHtcbiAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgICBjb25maWcuYXV0b0Nsb3NpbmdCcmFja2V0cyA9ICEhKFxuICAgICAgICAgIGFyZ3NbJ2ZvcmNlJ10gPz8gIWNvbmZpZy5hdXRvQ2xvc2luZ0JyYWNrZXRzXG4gICAgICAgICk7XG4gICAgICAgIHJldHVybiBzZXR0aW5nUmVnaXN0cnlcbiAgICAgICAgICAuc2V0KGlkLCAnZWRpdG9yQ29uZmlnJywgKGNvbmZpZyBhcyB1bmtub3duKSBhcyBKU09OT2JqZWN0KVxuICAgICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCAke2lkfTogJHtyZWFzb24ubWVzc2FnZX1gKTtcbiAgICAgICAgICB9KTtcbiAgICAgIH0sXG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0F1dG8gQ2xvc2UgQnJhY2tldHMgZm9yIFRleHQgRWRpdG9yJyksXG4gICAgICBpc1RvZ2dsZWQ6ICgpID0+IGNvbmZpZy5hdXRvQ2xvc2luZ0JyYWNrZXRzXG4gICAgfSk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuYXV0b0Nsb3NpbmdCcmFja2V0c1VuaXZlcnNhbCwge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCBhbnlUb2dnbGVkID1cbiAgICAgICAgICBjb21tYW5kcy5pc1RvZ2dsZWQoQ29tbWFuZElEcy5hdXRvQ2xvc2luZ0JyYWNrZXRzKSB8fFxuICAgICAgICAgIGNvbW1hbmRzLmlzVG9nZ2xlZChhdXRvQ2xvc2luZ0JyYWNrZXRzTm90ZWJvb2spIHx8XG4gICAgICAgICAgY29tbWFuZHMuaXNUb2dnbGVkKGF1dG9DbG9zaW5nQnJhY2tldHNDb25zb2xlKTtcbiAgICAgICAgLy8gaWYgYW55IGF1dG8gY2xvc2luZyBicmFja2V0cyBvcHRpb25zIGlzIHRvZ2dsZWQsIHRvZ2dsZSBib3RoIG9mZlxuICAgICAgICBpZiAoYW55VG9nZ2xlZCkge1xuICAgICAgICAgIHZvaWQgY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLmF1dG9DbG9zaW5nQnJhY2tldHMsIHtcbiAgICAgICAgICAgIGZvcmNlOiBmYWxzZVxuICAgICAgICAgIH0pO1xuICAgICAgICAgIHZvaWQgY29tbWFuZHMuZXhlY3V0ZShhdXRvQ2xvc2luZ0JyYWNrZXRzTm90ZWJvb2ssIHsgZm9yY2U6IGZhbHNlIH0pO1xuICAgICAgICAgIHZvaWQgY29tbWFuZHMuZXhlY3V0ZShhdXRvQ2xvc2luZ0JyYWNrZXRzQ29uc29sZSwgeyBmb3JjZTogZmFsc2UgfSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgLy8gYm90aCBhcmUgb2ZmLCB0dXJuIHRoZW0gb25cbiAgICAgICAgICB2b2lkIGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5hdXRvQ2xvc2luZ0JyYWNrZXRzLCB7XG4gICAgICAgICAgICBmb3JjZTogdHJ1ZVxuICAgICAgICAgIH0pO1xuICAgICAgICAgIHZvaWQgY29tbWFuZHMuZXhlY3V0ZShhdXRvQ2xvc2luZ0JyYWNrZXRzTm90ZWJvb2ssIHsgZm9yY2U6IHRydWUgfSk7XG4gICAgICAgICAgdm9pZCBjb21tYW5kcy5leGVjdXRlKGF1dG9DbG9zaW5nQnJhY2tldHNDb25zb2xlLCB7IGZvcmNlOiB0cnVlIH0pO1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdBdXRvIENsb3NlIEJyYWNrZXRzJyksXG4gICAgICBpc1RvZ2dsZWQ6ICgpID0+XG4gICAgICAgIGNvbW1hbmRzLmlzVG9nZ2xlZChDb21tYW5kSURzLmF1dG9DbG9zaW5nQnJhY2tldHMpIHx8XG4gICAgICAgIGNvbW1hbmRzLmlzVG9nZ2xlZChhdXRvQ2xvc2luZ0JyYWNrZXRzTm90ZWJvb2spIHx8XG4gICAgICAgIGNvbW1hbmRzLmlzVG9nZ2xlZChhdXRvQ2xvc2luZ0JyYWNrZXRzQ29uc29sZSlcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgdGhlIHJlcGxhY2Ugc2VsZWN0aW9uIGZvciB0ZXh0IGVkaXRvciBjb21tYW5kXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkUmVwbGFjZVNlbGVjdGlvbkNvbW1hbmQoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICB0cmFja2VyOiBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4sXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlLFxuICAgIGlzRW5hYmxlZDogKCkgPT4gYm9vbGVhblxuICApOiB2b2lkIHtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVwbGFjZVNlbGVjdGlvbiwge1xuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IHRleHQ6IHN0cmluZyA9IChhcmdzWyd0ZXh0J10gYXMgc3RyaW5nKSB8fCAnJztcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICB3aWRnZXQuY29udGVudC5lZGl0b3IucmVwbGFjZVNlbGVjdGlvbj8uKHRleHQpO1xuICAgICAgfSxcbiAgICAgIGlzRW5hYmxlZCxcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnUmVwbGFjZSBTZWxlY3Rpb24gaW4gRWRpdG9yJylcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgdGhlIENyZWF0ZSBDb25zb2xlIGZvciBFZGl0b3IgY29tbWFuZFxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZENyZWF0ZUNvbnNvbGVDb21tYW5kKFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnksXG4gICAgdHJhY2tlcjogV2lkZ2V0VHJhY2tlcjxJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4+LFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IGJvb2xlYW5cbiAgKTogdm9pZCB7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNyZWF0ZUNvbnNvbGUsIHtcbiAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4gZ2V0Q3JlYXRlQ29uc29sZUZ1bmN0aW9uKGNvbW1hbmRzKSh3aWRnZXQsIGFyZ3MpO1xuICAgICAgfSxcbiAgICAgIGlzRW5hYmxlZCxcbiAgICAgIGljb246IGNvbnNvbGVJY29uLFxuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdDcmVhdGUgQ29uc29sZSBmb3IgRWRpdG9yJylcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgdGhlIFJ1biBDb2RlIGNvbW1hbmRcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhZGRSdW5Db2RlQ29tbWFuZChcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIHRyYWNrZXI6IFdpZGdldFRyYWNrZXI8SURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+PixcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGUsXG4gICAgaXNFbmFibGVkOiAoKSA9PiBib29sZWFuXG4gICk6IHZvaWQge1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5ydW5Db2RlLCB7XG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIC8vIFJ1biB0aGUgYXBwcm9wcmlhdGUgY29kZSwgdGFraW5nIGludG8gYWNjb3VudCBhIGBgYGZlbmNlZGBgYCBjb2RlIGJsb2NrLlxuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBsZXQgY29kZTogc3RyaW5nIHwgdW5kZWZpbmVkID0gJyc7XG4gICAgICAgIGNvbnN0IGVkaXRvciA9IHdpZGdldC5lZGl0b3I7XG4gICAgICAgIGNvbnN0IHBhdGggPSB3aWRnZXQuY29udGV4dC5wYXRoO1xuICAgICAgICBjb25zdCBleHRlbnNpb24gPSBQYXRoRXh0LmV4dG5hbWUocGF0aCk7XG4gICAgICAgIGNvbnN0IHNlbGVjdGlvbiA9IGVkaXRvci5nZXRTZWxlY3Rpb24oKTtcbiAgICAgICAgY29uc3QgeyBzdGFydCwgZW5kIH0gPSBzZWxlY3Rpb247XG4gICAgICAgIGxldCBzZWxlY3RlZCA9IHN0YXJ0LmNvbHVtbiAhPT0gZW5kLmNvbHVtbiB8fCBzdGFydC5saW5lICE9PSBlbmQubGluZTtcblxuICAgICAgICBpZiAoc2VsZWN0ZWQpIHtcbiAgICAgICAgICAvLyBHZXQgdGhlIHNlbGVjdGVkIGNvZGUgZnJvbSB0aGUgZWRpdG9yLlxuICAgICAgICAgIGNvbnN0IHN0YXJ0ID0gZWRpdG9yLmdldE9mZnNldEF0KHNlbGVjdGlvbi5zdGFydCk7XG4gICAgICAgICAgY29uc3QgZW5kID0gZWRpdG9yLmdldE9mZnNldEF0KHNlbGVjdGlvbi5lbmQpO1xuXG4gICAgICAgICAgY29kZSA9IGVkaXRvci5tb2RlbC52YWx1ZS50ZXh0LnN1YnN0cmluZyhzdGFydCwgZW5kKTtcbiAgICAgICAgfSBlbHNlIGlmIChNYXJrZG93bkNvZGVCbG9ja3MuaXNNYXJrZG93bihleHRlbnNpb24pKSB7XG4gICAgICAgICAgY29uc3QgeyB0ZXh0IH0gPSBlZGl0b3IubW9kZWwudmFsdWU7XG4gICAgICAgICAgY29uc3QgYmxvY2tzID0gTWFya2Rvd25Db2RlQmxvY2tzLmZpbmRNYXJrZG93bkNvZGVCbG9ja3ModGV4dCk7XG5cbiAgICAgICAgICBmb3IgKGNvbnN0IGJsb2NrIG9mIGJsb2Nrcykge1xuICAgICAgICAgICAgaWYgKGJsb2NrLnN0YXJ0TGluZSA8PSBzdGFydC5saW5lICYmIHN0YXJ0LmxpbmUgPD0gYmxvY2suZW5kTGluZSkge1xuICAgICAgICAgICAgICBjb2RlID0gYmxvY2suY29kZTtcbiAgICAgICAgICAgICAgc2VsZWN0ZWQgPSB0cnVlO1xuICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH1cblxuICAgICAgICBpZiAoIXNlbGVjdGVkKSB7XG4gICAgICAgICAgLy8gbm8gc2VsZWN0aW9uLCBzdWJtaXQgd2hvbGUgbGluZSBhbmQgYWR2YW5jZVxuICAgICAgICAgIGNvZGUgPSBlZGl0b3IuZ2V0TGluZShzZWxlY3Rpb24uc3RhcnQubGluZSk7XG4gICAgICAgICAgY29uc3QgY3Vyc29yID0gZWRpdG9yLmdldEN1cnNvclBvc2l0aW9uKCk7XG4gICAgICAgICAgaWYgKGN1cnNvci5saW5lICsgMSA9PT0gZWRpdG9yLmxpbmVDb3VudCkge1xuICAgICAgICAgICAgY29uc3QgdGV4dCA9IGVkaXRvci5tb2RlbC52YWx1ZS50ZXh0O1xuICAgICAgICAgICAgZWRpdG9yLm1vZGVsLnZhbHVlLnRleHQgPSB0ZXh0ICsgJ1xcbic7XG4gICAgICAgICAgfVxuICAgICAgICAgIGVkaXRvci5zZXRDdXJzb3JQb3NpdGlvbih7XG4gICAgICAgICAgICBsaW5lOiBjdXJzb3IubGluZSArIDEsXG4gICAgICAgICAgICBjb2x1bW46IGN1cnNvci5jb2x1bW5cbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGFjdGl2YXRlID0gZmFsc2U7XG4gICAgICAgIGlmIChjb2RlKSB7XG4gICAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoJ2NvbnNvbGU6aW5qZWN0JywgeyBhY3RpdmF0ZSwgY29kZSwgcGF0aCB9KTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKHZvaWQgMCk7XG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBpc0VuYWJsZWQsXG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1J1biBDb2RlJylcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgdGhlIFJ1biBBbGwgQ29kZSBjb21tYW5kXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkUnVuQWxsQ29kZUNvbW1hbmQoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICB0cmFja2VyOiBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4sXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlLFxuICAgIGlzRW5hYmxlZDogKCkgPT4gYm9vbGVhblxuICApOiB2b2lkIHtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucnVuQWxsQ29kZSwge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBsZXQgY29kZSA9ICcnO1xuICAgICAgICBjb25zdCBlZGl0b3IgPSB3aWRnZXQuZWRpdG9yO1xuICAgICAgICBjb25zdCB0ZXh0ID0gZWRpdG9yLm1vZGVsLnZhbHVlLnRleHQ7XG4gICAgICAgIGNvbnN0IHBhdGggPSB3aWRnZXQuY29udGV4dC5wYXRoO1xuICAgICAgICBjb25zdCBleHRlbnNpb24gPSBQYXRoRXh0LmV4dG5hbWUocGF0aCk7XG5cbiAgICAgICAgaWYgKE1hcmtkb3duQ29kZUJsb2Nrcy5pc01hcmtkb3duKGV4dGVuc2lvbikpIHtcbiAgICAgICAgICAvLyBGb3IgTWFya2Rvd24gZmlsZXMsIHJ1biBvbmx5IGNvZGUgYmxvY2tzLlxuICAgICAgICAgIGNvbnN0IGJsb2NrcyA9IE1hcmtkb3duQ29kZUJsb2Nrcy5maW5kTWFya2Rvd25Db2RlQmxvY2tzKHRleHQpO1xuICAgICAgICAgIGZvciAoY29uc3QgYmxvY2sgb2YgYmxvY2tzKSB7XG4gICAgICAgICAgICBjb2RlICs9IGJsb2NrLmNvZGU7XG4gICAgICAgICAgfVxuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGNvZGUgPSB0ZXh0O1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgYWN0aXZhdGUgPSBmYWxzZTtcbiAgICAgICAgaWYgKGNvZGUpIHtcbiAgICAgICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnY29uc29sZTppbmplY3QnLCB7IGFjdGl2YXRlLCBjb2RlLCBwYXRoIH0pO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUodm9pZCAwKTtcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIGlzRW5hYmxlZCxcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnUnVuIEFsbCBDb2RlJylcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgbWFya2Rvd24gcHJldmlldyBjb21tYW5kXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkTWFya2Rvd25QcmV2aWV3Q29tbWFuZChcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIHRyYWNrZXI6IFdpZGdldFRyYWNrZXI8SURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+PixcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGVcbiAgKTogdm9pZCB7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm1hcmtkb3duUHJldmlldywge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IHBhdGggPSB3aWRnZXQuY29udGV4dC5wYXRoO1xuICAgICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnbWFya2Rvd252aWV3ZXI6b3BlbicsIHtcbiAgICAgICAgICBwYXRoLFxuICAgICAgICAgIG9wdGlvbnM6IHtcbiAgICAgICAgICAgIG1vZGU6ICdzcGxpdC1yaWdodCdcbiAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgICAgfSxcbiAgICAgIGlzVmlzaWJsZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgKHdpZGdldCAmJiBQYXRoRXh0LmV4dG5hbWUod2lkZ2V0LmNvbnRleHQucGF0aCkgPT09ICcubWQnKSB8fCBmYWxzZVxuICAgICAgICApO1xuICAgICAgfSxcbiAgICAgIGljb246IG1hcmtkb3duSWNvbixcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnU2hvdyBNYXJrZG93biBQcmV2aWV3JylcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgdW5kbyBjb21tYW5kXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkVW5kb0NvbW1hbmQoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICB0cmFja2VyOiBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4sXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlLFxuICAgIGlzRW5hYmxlZDogKCkgPT4gYm9vbGVhblxuICApOiB2b2lkIHtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMudW5kbywge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICB3aWRnZXQuZWRpdG9yLnVuZG8oKTtcbiAgICAgIH0sXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgaWYgKCFpc0VuYWJsZWQoKSkge1xuICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgfVxuICAgICAgICAvLyBJZGVhbGx5IGVuYWJsZSBpdCB3aGVuIHRoZXJlIGFyZSB1bmRvIGV2ZW50cyBzdG9yZWRcbiAgICAgICAgLy8gUmVmZXJlbmNlIGlzc3VlICM4NTkwOiBDb2RlIG1pcnJvciBlZGl0b3IgY291bGQgZXhwb3NlIHRoZSBoaXN0b3J5IG9mIHVuZG8vcmVkbyBldmVudHNcbiAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICB9LFxuICAgICAgaWNvbjogdW5kb0ljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnVW5kbycpXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIHJlZG8gY29tbWFuZFxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZFJlZG9Db21tYW5kKFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnksXG4gICAgdHJhY2tlcjogV2lkZ2V0VHJhY2tlcjxJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4+LFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IGJvb2xlYW5cbiAgKTogdm9pZCB7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJlZG8sIHtcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50O1xuXG4gICAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgd2lkZ2V0LmVkaXRvci5yZWRvKCk7XG4gICAgICB9LFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiB7XG4gICAgICAgIGlmICghaXNFbmFibGVkKCkpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgICAgLy8gSWRlYWxseSBlbmFibGUgaXQgd2hlbiB0aGVyZSBhcmUgcmVkbyBldmVudHMgc3RvcmVkXG4gICAgICAgIC8vIFJlZmVyZW5jZSBpc3N1ZSAjODU5MDogQ29kZSBtaXJyb3IgZWRpdG9yIGNvdWxkIGV4cG9zZSB0aGUgaGlzdG9yeSBvZiB1bmRvL3JlZG8gZXZlbnRzXG4gICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgfSxcbiAgICAgIGljb246IHJlZG9JY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1JlZG8nKVxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBjdXQgY29tbWFuZFxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZEN1dENvbW1hbmQoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICB0cmFja2VyOiBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4sXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlLFxuICAgIGlzRW5hYmxlZDogKCkgPT4gYm9vbGVhblxuICApOiB2b2lkIHtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY3V0LCB7XG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGVkaXRvciA9IHdpZGdldC5lZGl0b3IgYXMgQ29kZU1pcnJvckVkaXRvcjtcbiAgICAgICAgY29uc3QgdGV4dCA9IGdldFRleHRTZWxlY3Rpb24oZWRpdG9yKTtcblxuICAgICAgICBDbGlwYm9hcmQuY29weVRvU3lzdGVtKHRleHQpO1xuICAgICAgICBlZGl0b3IucmVwbGFjZVNlbGVjdGlvbiAmJiBlZGl0b3IucmVwbGFjZVNlbGVjdGlvbignJyk7XG4gICAgICB9LFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiB7XG4gICAgICAgIGlmICghaXNFbmFibGVkKCkpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBFbmFibGUgY29tbWFuZCBpZiB0aGVyZSBpcyBhIHRleHQgc2VsZWN0aW9uIGluIHRoZSBlZGl0b3JcbiAgICAgICAgcmV0dXJuIGlzU2VsZWN0ZWQod2lkZ2V0LmVkaXRvciBhcyBDb2RlTWlycm9yRWRpdG9yKTtcbiAgICAgIH0sXG4gICAgICBpY29uOiBjdXRJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0N1dCcpXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGNvcHkgY29tbWFuZFxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZENvcHlDb21tYW5kKFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnksXG4gICAgdHJhY2tlcjogV2lkZ2V0VHJhY2tlcjxJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4+LFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IGJvb2xlYW5cbiAgKTogdm9pZCB7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNvcHksIHtcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50O1xuXG4gICAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgZWRpdG9yID0gd2lkZ2V0LmVkaXRvciBhcyBDb2RlTWlycm9yRWRpdG9yO1xuICAgICAgICBjb25zdCB0ZXh0ID0gZ2V0VGV4dFNlbGVjdGlvbihlZGl0b3IpO1xuXG4gICAgICAgIENsaXBib2FyZC5jb3B5VG9TeXN0ZW0odGV4dCk7XG4gICAgICB9LFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiB7XG4gICAgICAgIGlmICghaXNFbmFibGVkKCkpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBFbmFibGUgY29tbWFuZCBpZiB0aGVyZSBpcyBhIHRleHQgc2VsZWN0aW9uIGluIHRoZSBlZGl0b3JcbiAgICAgICAgcmV0dXJuIGlzU2VsZWN0ZWQod2lkZ2V0LmVkaXRvciBhcyBDb2RlTWlycm9yRWRpdG9yKTtcbiAgICAgIH0sXG4gICAgICBpY29uOiBjb3B5SWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdDb3B5JylcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgcGFzdGUgY29tbWFuZFxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZFBhc3RlQ29tbWFuZChcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIHRyYWNrZXI6IFdpZGdldFRyYWNrZXI8SURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+PixcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGUsXG4gICAgaXNFbmFibGVkOiAoKSA9PiBib29sZWFuXG4gICk6IHZvaWQge1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5wYXN0ZSwge1xuICAgICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBlZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvciA9IHdpZGdldC5lZGl0b3I7XG5cbiAgICAgICAgLy8gR2V0IGRhdGEgZnJvbSBjbGlwYm9hcmRcbiAgICAgICAgY29uc3QgY2xpcGJvYXJkID0gd2luZG93Lm5hdmlnYXRvci5jbGlwYm9hcmQ7XG4gICAgICAgIGNvbnN0IGNsaXBib2FyZERhdGE6IHN0cmluZyA9IGF3YWl0IGNsaXBib2FyZC5yZWFkVGV4dCgpO1xuXG4gICAgICAgIGlmIChjbGlwYm9hcmREYXRhKSB7XG4gICAgICAgICAgLy8gUGFzdGUgZGF0YSB0byB0aGUgZWRpdG9yXG4gICAgICAgICAgZWRpdG9yLnJlcGxhY2VTZWxlY3Rpb24gJiYgZWRpdG9yLnJlcGxhY2VTZWxlY3Rpb24oY2xpcGJvYXJkRGF0YSk7XG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IEJvb2xlYW4oaXNFbmFibGVkKCkgJiYgdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50KSxcbiAgICAgIGljb246IHBhc3RlSWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdQYXN0ZScpXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIHNlbGVjdCBhbGwgY29tbWFuZFxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZFNlbGVjdEFsbENvbW1hbmQoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICB0cmFja2VyOiBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4sXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlLFxuICAgIGlzRW5hYmxlZDogKCkgPT4gYm9vbGVhblxuICApOiB2b2lkIHtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2VsZWN0QWxsLCB7XG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGVkaXRvciA9IHdpZGdldC5lZGl0b3IgYXMgQ29kZU1pcnJvckVkaXRvcjtcbiAgICAgICAgZWRpdG9yLmV4ZWNDb21tYW5kKCdzZWxlY3RBbGwnKTtcbiAgICAgIH0sXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IEJvb2xlYW4oaXNFbmFibGVkKCkgJiYgdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50KSxcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnU2VsZWN0IEFsbCcpXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSGVscGVyIGZ1bmN0aW9uIHRvIGNoZWNrIGlmIHRoZXJlIGlzIGEgdGV4dCBzZWxlY3Rpb24gaW4gdGhlIGVkaXRvclxuICAgKi9cbiAgZnVuY3Rpb24gaXNTZWxlY3RlZChlZGl0b3I6IENvZGVNaXJyb3JFZGl0b3IpIHtcbiAgICBjb25zdCBzZWxlY3Rpb25PYmogPSBlZGl0b3IuZ2V0U2VsZWN0aW9uKCk7XG4gICAgY29uc3QgeyBzdGFydCwgZW5kIH0gPSBzZWxlY3Rpb25PYmo7XG4gICAgY29uc3Qgc2VsZWN0ZWQgPSBzdGFydC5jb2x1bW4gIT09IGVuZC5jb2x1bW4gfHwgc3RhcnQubGluZSAhPT0gZW5kLmxpbmU7XG5cbiAgICByZXR1cm4gc2VsZWN0ZWQ7XG4gIH1cblxuICAvKipcbiAgICogSGVscGVyIGZ1bmN0aW9uIHRvIGdldCB0ZXh0IHNlbGVjdGlvbiBmcm9tIHRoZSBlZGl0b3JcbiAgICovXG4gIGZ1bmN0aW9uIGdldFRleHRTZWxlY3Rpb24oZWRpdG9yOiBDb2RlTWlycm9yRWRpdG9yKSB7XG4gICAgY29uc3Qgc2VsZWN0aW9uT2JqID0gZWRpdG9yLmdldFNlbGVjdGlvbigpO1xuICAgIGNvbnN0IHN0YXJ0ID0gZWRpdG9yLmdldE9mZnNldEF0KHNlbGVjdGlvbk9iai5zdGFydCk7XG4gICAgY29uc3QgZW5kID0gZWRpdG9yLmdldE9mZnNldEF0KHNlbGVjdGlvbk9iai5lbmQpO1xuICAgIGNvbnN0IHRleHQgPSBlZGl0b3IubW9kZWwudmFsdWUudGV4dC5zdWJzdHJpbmcoc3RhcnQsIGVuZCk7XG5cbiAgICByZXR1cm4gdGV4dDtcbiAgfVxuXG4gIC8qKlxuICAgKiBGdW5jdGlvbiB0byBjcmVhdGUgYSBuZXcgdW50aXRsZWQgdGV4dCBmaWxlLCBnaXZlbiB0aGUgY3VycmVudCB3b3JraW5nIGRpcmVjdG9yeS5cbiAgICovXG4gIGZ1bmN0aW9uIGNyZWF0ZU5ldyhcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIGN3ZDogc3RyaW5nLFxuICAgIGV4dDogc3RyaW5nID0gJ3R4dCdcbiAgKSB7XG4gICAgcmV0dXJuIGNvbW1hbmRzXG4gICAgICAuZXhlY3V0ZSgnZG9jbWFuYWdlcjpuZXctdW50aXRsZWQnLCB7XG4gICAgICAgIHBhdGg6IGN3ZCxcbiAgICAgICAgdHlwZTogJ2ZpbGUnLFxuICAgICAgICBleHRcbiAgICAgIH0pXG4gICAgICAudGhlbihtb2RlbCA9PiB7XG4gICAgICAgIGlmIChtb2RlbCAhPSB1bmRlZmluZWQpIHtcbiAgICAgICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnZG9jbWFuYWdlcjpvcGVuJywge1xuICAgICAgICAgICAgcGF0aDogbW9kZWwucGF0aCxcbiAgICAgICAgICAgIGZhY3Rvcnk6IEZBQ1RPUllcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIHRoZSBOZXcgRmlsZSBjb21tYW5kXG4gICAqXG4gICAqIERlZmF1bHRzIHRvIFRleHQvLnR4dCBpZiBmaWxlIHR5cGUgZGF0YSBpcyBub3Qgc3BlY2lmaWVkXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkQ3JlYXRlTmV3Q29tbWFuZChcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIGJyb3dzZXJGYWN0b3J5OiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApOiB2b2lkIHtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY3JlYXRlTmV3LCB7XG4gICAgICBsYWJlbDogYXJncyA9PiB7XG4gICAgICAgIGlmIChhcmdzLmlzUGFsZXR0ZSkge1xuICAgICAgICAgIHJldHVybiAoYXJncy5wYWxldHRlTGFiZWwgYXMgc3RyaW5nKSA/PyB0cmFucy5fXygnTmV3IFRleHQgRmlsZScpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiAoYXJncy5sYXVuY2hlckxhYmVsIGFzIHN0cmluZykgPz8gdHJhbnMuX18oJ1RleHQgRmlsZScpO1xuICAgICAgfSxcbiAgICAgIGNhcHRpb246IGFyZ3MgPT5cbiAgICAgICAgKGFyZ3MuY2FwdGlvbiBhcyBzdHJpbmcpID8/IHRyYW5zLl9fKCdDcmVhdGUgYSBuZXcgdGV4dCBmaWxlJyksXG4gICAgICBpY29uOiBhcmdzID0+XG4gICAgICAgIGFyZ3MuaXNQYWxldHRlXG4gICAgICAgICAgPyB1bmRlZmluZWRcbiAgICAgICAgICA6IExhYkljb24ucmVzb2x2ZSh7XG4gICAgICAgICAgICAgIGljb246IChhcmdzLmljb25OYW1lIGFzIHN0cmluZykgPz8gdGV4dEVkaXRvckljb25cbiAgICAgICAgICAgIH0pLFxuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IGN3ZCA9IGFyZ3MuY3dkIHx8IGJyb3dzZXJGYWN0b3J5LmRlZmF1bHRCcm93c2VyLm1vZGVsLnBhdGg7XG4gICAgICAgIHJldHVybiBjcmVhdGVOZXcoXG4gICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgY3dkIGFzIHN0cmluZyxcbiAgICAgICAgICAoYXJncy5maWxlRXh0IGFzIHN0cmluZykgPz8gJ3R4dCdcbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgdGhlIE5ldyBNYXJrZG93biBGaWxlIGNvbW1hbmRcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhZGRDcmVhdGVOZXdNYXJrZG93bkNvbW1hbmQoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICBicm93c2VyRmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeSxcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGVcbiAgKTogdm9pZCB7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNyZWF0ZU5ld01hcmtkb3duLCB7XG4gICAgICBsYWJlbDogYXJncyA9PlxuICAgICAgICBhcmdzWydpc1BhbGV0dGUnXVxuICAgICAgICAgID8gdHJhbnMuX18oJ05ldyBNYXJrZG93biBGaWxlJylcbiAgICAgICAgICA6IHRyYW5zLl9fKCdNYXJrZG93biBGaWxlJyksXG4gICAgICBjYXB0aW9uOiB0cmFucy5fXygnQ3JlYXRlIGEgbmV3IG1hcmtkb3duIGZpbGUnKSxcbiAgICAgIGljb246IGFyZ3MgPT4gKGFyZ3NbJ2lzUGFsZXR0ZSddID8gdW5kZWZpbmVkIDogbWFya2Rvd25JY29uKSxcbiAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgICBjb25zdCBjd2QgPSBhcmdzWydjd2QnXSB8fCBicm93c2VyRmFjdG9yeS5kZWZhdWx0QnJvd3Nlci5tb2RlbC5wYXRoO1xuICAgICAgICByZXR1cm4gY3JlYXRlTmV3KGNvbW1hbmRzLCBjd2QgYXMgc3RyaW5nLCAnbWQnKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXcmFwcGVyIGZ1bmN0aW9uIGZvciBhZGRpbmcgdGhlIGRlZmF1bHQgbGF1bmNoZXIgaXRlbXMgZm9yIEZpbGUgRWRpdG9yXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkTGF1bmNoZXJJdGVtcyhcbiAgICBsYXVuY2hlcjogSUxhdW5jaGVyLFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApOiB2b2lkIHtcbiAgICBhZGRDcmVhdGVOZXdUb0xhdW5jaGVyKGxhdW5jaGVyLCB0cmFucyk7XG5cbiAgICBhZGRDcmVhdGVOZXdNYXJrZG93blRvTGF1bmNoZXIobGF1bmNoZXIsIHRyYW5zKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgQ3JlYXRlIE5ldyBUZXh0IEZpbGUgdG8gdGhlIExhdW5jaGVyXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkQ3JlYXRlTmV3VG9MYXVuY2hlcihcbiAgICBsYXVuY2hlcjogSUxhdW5jaGVyLFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApOiB2b2lkIHtcbiAgICBsYXVuY2hlci5hZGQoe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5jcmVhdGVOZXcsXG4gICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ090aGVyJyksXG4gICAgICByYW5rOiAxXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIENyZWF0ZSBOZXcgTWFya2Rvd24gdG8gdGhlIExhdW5jaGVyXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkQ3JlYXRlTmV3TWFya2Rvd25Ub0xhdW5jaGVyKFxuICAgIGxhdW5jaGVyOiBJTGF1bmNoZXIsXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICk6IHZvaWQge1xuICAgIGxhdW5jaGVyLmFkZCh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLmNyZWF0ZU5ld01hcmtkb3duLFxuICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdPdGhlcicpLFxuICAgICAgcmFuazogMlxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBfX18gRmlsZSBpdGVtcyB0byB0aGUgTGF1bmNoZXIgZm9yIGNvbW1vbiBmaWxlIHR5cGVzIGFzc29jaWF0ZWQgd2l0aCBhdmFpbGFibGUga2VybmVsc1xuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZEtlcm5lbExhbmd1YWdlTGF1bmNoZXJJdGVtcyhcbiAgICBsYXVuY2hlcjogSUxhdW5jaGVyLFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZSxcbiAgICBhdmFpbGFibGVLZXJuZWxGaWxlVHlwZXM6IEl0ZXJhYmxlPElGaWxlVHlwZURhdGE+XG4gICk6IHZvaWQge1xuICAgIGZvciAobGV0IGV4dCBvZiBhdmFpbGFibGVLZXJuZWxGaWxlVHlwZXMpIHtcbiAgICAgIGxhdW5jaGVyLmFkZCh7XG4gICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuY3JlYXRlTmV3LFxuICAgICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ090aGVyJyksXG4gICAgICAgIHJhbms6IDMsXG4gICAgICAgIGFyZ3M6IGV4dFxuICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFdyYXBwZXIgZnVuY3Rpb24gZm9yIGFkZGluZyB0aGUgZGVmYXVsdCBpdGVtcyB0byB0aGUgRmlsZSBFZGl0b3IgcGFsZXR0ZVxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZFBhbGV0dGVJdGVtcyhcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUsXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICk6IHZvaWQge1xuICAgIGFkZENoYW5nZVRhYnNDb21tYW5kc1RvUGFsZXR0ZShwYWxldHRlLCB0cmFucyk7XG5cbiAgICBhZGRDcmVhdGVOZXdDb21tYW5kVG9QYWxldHRlKHBhbGV0dGUsIHRyYW5zKTtcblxuICAgIGFkZENyZWF0ZU5ld01hcmtkb3duQ29tbWFuZFRvUGFsZXR0ZShwYWxldHRlLCB0cmFucyk7XG5cbiAgICBhZGRDaGFuZ2VGb250U2l6ZUNvbW1hbmRzVG9QYWxldHRlKHBhbGV0dGUsIHRyYW5zKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgY29tbWFuZHMgdG8gY2hhbmdlIHRoZSB0YWIgaW5kZW50YXRpb24gdG8gdGhlIEZpbGUgRWRpdG9yIHBhbGV0dGVcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhZGRDaGFuZ2VUYWJzQ29tbWFuZHNUb1BhbGV0dGUoXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlLFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApOiB2b2lkIHtcbiAgICBjb25zdCBwYWxldHRlQ2F0ZWdvcnkgPSB0cmFucy5fXygnVGV4dCBFZGl0b3InKTtcbiAgICBjb25zdCBhcmdzOiBKU09OT2JqZWN0ID0ge1xuICAgICAgaW5zZXJ0U3BhY2VzOiBmYWxzZSxcbiAgICAgIHNpemU6IDRcbiAgICB9O1xuICAgIGNvbnN0IGNvbW1hbmQgPSBDb21tYW5kSURzLmNoYW5nZVRhYnM7XG4gICAgcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZCwgYXJncywgY2F0ZWdvcnk6IHBhbGV0dGVDYXRlZ29yeSB9KTtcblxuICAgIGZvciAoY29uc3Qgc2l6ZSBvZiBbMSwgMiwgNCwgOF0pIHtcbiAgICAgIGNvbnN0IGFyZ3M6IEpTT05PYmplY3QgPSB7XG4gICAgICAgIGluc2VydFNwYWNlczogdHJ1ZSxcbiAgICAgICAgc2l6ZVxuICAgICAgfTtcbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNvbW1hbmQsIGFyZ3MsIGNhdGVnb3J5OiBwYWxldHRlQ2F0ZWdvcnkgfSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIENyZWF0ZSBOZXcgRmlsZSBjb21tYW5kIHRvIHRoZSBGaWxlIEVkaXRvciBwYWxldHRlXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkQ3JlYXRlTmV3Q29tbWFuZFRvUGFsZXR0ZShcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUsXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICk6IHZvaWQge1xuICAgIGNvbnN0IHBhbGV0dGVDYXRlZ29yeSA9IHRyYW5zLl9fKCdUZXh0IEVkaXRvcicpO1xuICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLmNyZWF0ZU5ldyxcbiAgICAgIGFyZ3M6IHsgaXNQYWxldHRlOiB0cnVlIH0sXG4gICAgICBjYXRlZ29yeTogcGFsZXR0ZUNhdGVnb3J5XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgQ3JlYXRlIE5ldyBNYXJrZG93biBjb21tYW5kIHRvIHRoZSBGaWxlIEVkaXRvciBwYWxldHRlXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkQ3JlYXRlTmV3TWFya2Rvd25Db21tYW5kVG9QYWxldHRlKFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSxcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGVcbiAgKTogdm9pZCB7XG4gICAgY29uc3QgcGFsZXR0ZUNhdGVnb3J5ID0gdHJhbnMuX18oJ1RleHQgRWRpdG9yJyk7XG4gICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuY3JlYXRlTmV3TWFya2Rvd24sXG4gICAgICBhcmdzOiB7IGlzUGFsZXR0ZTogdHJ1ZSB9LFxuICAgICAgY2F0ZWdvcnk6IHBhbGV0dGVDYXRlZ29yeVxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBjb21tYW5kcyB0byBjaGFuZ2UgdGhlIGZvbnQgc2l6ZSB0byB0aGUgRmlsZSBFZGl0b3IgcGFsZXR0ZVxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZENoYW5nZUZvbnRTaXplQ29tbWFuZHNUb1BhbGV0dGUoXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlLFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApOiB2b2lkIHtcbiAgICBjb25zdCBwYWxldHRlQ2F0ZWdvcnkgPSB0cmFucy5fXygnVGV4dCBFZGl0b3InKTtcbiAgICBjb25zdCBjb21tYW5kID0gQ29tbWFuZElEcy5jaGFuZ2VGb250U2l6ZTtcblxuICAgIGxldCBhcmdzID0geyBkZWx0YTogMSB9O1xuICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNvbW1hbmQsIGFyZ3MsIGNhdGVnb3J5OiBwYWxldHRlQ2F0ZWdvcnkgfSk7XG5cbiAgICBhcmdzID0geyBkZWx0YTogLTEgfTtcbiAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kLCBhcmdzLCBjYXRlZ29yeTogcGFsZXR0ZUNhdGVnb3J5IH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBOZXcgX19fIEZpbGUgY29tbWFuZHMgdG8gdGhlIEZpbGUgRWRpdG9yIHBhbGV0dGUgZm9yIGNvbW1vbiBmaWxlIHR5cGVzIGFzc29jaWF0ZWQgd2l0aCBhdmFpbGFibGUga2VybmVsc1xuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZEtlcm5lbExhbmd1YWdlUGFsZXR0ZUl0ZW1zKFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSxcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGUsXG4gICAgYXZhaWxhYmxlS2VybmVsRmlsZVR5cGVzOiBJdGVyYWJsZTxJRmlsZVR5cGVEYXRhPlxuICApOiB2b2lkIHtcbiAgICBjb25zdCBwYWxldHRlQ2F0ZWdvcnkgPSB0cmFucy5fXygnVGV4dCBFZGl0b3InKTtcbiAgICBmb3IgKGxldCBleHQgb2YgYXZhaWxhYmxlS2VybmVsRmlsZVR5cGVzKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLmNyZWF0ZU5ldyxcbiAgICAgICAgYXJnczogeyAuLi5leHQsIGlzUGFsZXR0ZTogdHJ1ZSB9LFxuICAgICAgICBjYXRlZ29yeTogcGFsZXR0ZUNhdGVnb3J5XG4gICAgICB9KTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogV3JhcHBlciBmdW5jdGlvbiBmb3IgYWRkaW5nIHRoZSBkZWZhdWx0IG1lbnUgaXRlbXMgZm9yIEZpbGUgRWRpdG9yXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkTWVudUl0ZW1zKFxuICAgIG1lbnU6IElNYWluTWVudSxcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIHRyYWNrZXI6IFdpZGdldFRyYWNrZXI8SURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+PixcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGUsXG4gICAgY29uc29sZVRyYWNrZXI6IElDb25zb2xlVHJhY2tlciB8IG51bGwsXG4gICAgc2Vzc2lvbkRpYWxvZ3M6IElTZXNzaW9uQ29udGV4dERpYWxvZ3MgfCBudWxsXG4gICk6IHZvaWQge1xuICAgIC8vIEFkZCB1bmRvL3JlZG8gaG9va3MgdG8gdGhlIGVkaXQgbWVudS5cbiAgICBhZGRVbmRvUmVkb1RvRWRpdE1lbnUobWVudSwgdHJhY2tlcik7XG5cbiAgICAvLyBBZGQgZWRpdG9yIHZpZXcgb3B0aW9ucy5cbiAgICBhZGRFZGl0b3JWaWV3ZXJUb1ZpZXdNZW51KG1lbnUsIHRyYWNrZXIpO1xuXG4gICAgLy8gQWRkIGEgY29uc29sZSBjcmVhdG9yIHRoZSB0aGUgZmlsZSBtZW51LlxuICAgIGFkZENvbnNvbGVDcmVhdG9yVG9GaWxlTWVudShtZW51LCBjb21tYW5kcywgdHJhY2tlciwgdHJhbnMpO1xuXG4gICAgLy8gQWRkIGEgY29kZSBydW5uZXIgdG8gdGhlIHJ1biBtZW51LlxuICAgIGlmIChjb25zb2xlVHJhY2tlcikge1xuICAgICAgYWRkQ29kZVJ1bm5lcnNUb1J1bk1lbnUoXG4gICAgICAgIG1lbnUsXG4gICAgICAgIGNvbW1hbmRzLFxuICAgICAgICB0cmFja2VyLFxuICAgICAgICBjb25zb2xlVHJhY2tlcixcbiAgICAgICAgdHJhbnMsXG4gICAgICAgIHNlc3Npb25EaWFsb2dzXG4gICAgICApO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgQ3JlYXRlIE5ldyBfX18gRmlsZSBjb21tYW5kcyB0byB0aGUgRmlsZSBtZW51IGZvciBjb21tb24gZmlsZSB0eXBlcyBhc3NvY2lhdGVkIHdpdGggYXZhaWxhYmxlIGtlcm5lbHNcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhZGRLZXJuZWxMYW5ndWFnZU1lbnVJdGVtcyhcbiAgICBtZW51OiBJTWFpbk1lbnUsXG4gICAgYXZhaWxhYmxlS2VybmVsRmlsZVR5cGVzOiBJdGVyYWJsZTxJRmlsZVR5cGVEYXRhPlxuICApOiB2b2lkIHtcbiAgICBmb3IgKGxldCBleHQgb2YgYXZhaWxhYmxlS2VybmVsRmlsZVR5cGVzKSB7XG4gICAgICBtZW51LmZpbGVNZW51Lm5ld01lbnUuYWRkSXRlbSh7XG4gICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuY3JlYXRlTmV3LFxuICAgICAgICBhcmdzOiBleHQsXG4gICAgICAgIHJhbms6IDMwXG4gICAgICB9KTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQWRkIEZpbGUgRWRpdG9yIHVuZG8gYW5kIHJlZG8gd2lkZ2V0cyB0byB0aGUgRWRpdCBtZW51XG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkVW5kb1JlZG9Ub0VkaXRNZW51KFxuICAgIG1lbnU6IElNYWluTWVudSxcbiAgICB0cmFja2VyOiBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj5cbiAgKTogdm9pZCB7XG4gICAgbWVudS5lZGl0TWVudS51bmRvZXJzLmFkZCh7XG4gICAgICB0cmFja2VyLFxuICAgICAgdW5kbzogd2lkZ2V0ID0+IHtcbiAgICAgICAgd2lkZ2V0LmNvbnRlbnQuZWRpdG9yLnVuZG8oKTtcbiAgICAgIH0sXG4gICAgICByZWRvOiB3aWRnZXQgPT4ge1xuICAgICAgICB3aWRnZXQuY29udGVudC5lZGl0b3IucmVkbygpO1xuICAgICAgfVxuICAgIH0gYXMgSUVkaXRNZW51LklVbmRvZXI8SURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+Pik7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgRmlsZSBFZGl0b3IgZWRpdG9yIHZpZXdlciB0byB0aGUgVmlldyBNZW51XG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYWRkRWRpdG9yVmlld2VyVG9WaWV3TWVudShcbiAgICBtZW51OiBJTWFpbk1lbnUsXG4gICAgdHJhY2tlcjogV2lkZ2V0VHJhY2tlcjxJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4+XG4gICk6IHZvaWQge1xuICAgIG1lbnUudmlld01lbnUuZWRpdG9yVmlld2Vycy5hZGQoe1xuICAgICAgdHJhY2tlcixcbiAgICAgIHRvZ2dsZUxpbmVOdW1iZXJzOiB3aWRnZXQgPT4ge1xuICAgICAgICBjb25zdCBsaW5lTnVtYmVycyA9ICF3aWRnZXQuY29udGVudC5lZGl0b3IuZ2V0T3B0aW9uKCdsaW5lTnVtYmVycycpO1xuICAgICAgICB3aWRnZXQuY29udGVudC5lZGl0b3Iuc2V0T3B0aW9uKCdsaW5lTnVtYmVycycsIGxpbmVOdW1iZXJzKTtcbiAgICAgIH0sXG4gICAgICB0b2dnbGVXb3JkV3JhcDogd2lkZ2V0ID0+IHtcbiAgICAgICAgY29uc3Qgb2xkVmFsdWUgPSB3aWRnZXQuY29udGVudC5lZGl0b3IuZ2V0T3B0aW9uKCdsaW5lV3JhcCcpO1xuICAgICAgICBjb25zdCBuZXdWYWx1ZSA9IG9sZFZhbHVlID09PSAnb2ZmJyA/ICdvbicgOiAnb2ZmJztcbiAgICAgICAgd2lkZ2V0LmNvbnRlbnQuZWRpdG9yLnNldE9wdGlvbignbGluZVdyYXAnLCBuZXdWYWx1ZSk7XG4gICAgICB9LFxuICAgICAgdG9nZ2xlTWF0Y2hCcmFja2V0czogd2lkZ2V0ID0+IHtcbiAgICAgICAgY29uc3QgbWF0Y2hCcmFja2V0cyA9ICF3aWRnZXQuY29udGVudC5lZGl0b3IuZ2V0T3B0aW9uKCdtYXRjaEJyYWNrZXRzJyk7XG4gICAgICAgIHdpZGdldC5jb250ZW50LmVkaXRvci5zZXRPcHRpb24oJ21hdGNoQnJhY2tldHMnLCBtYXRjaEJyYWNrZXRzKTtcbiAgICAgIH0sXG4gICAgICBsaW5lTnVtYmVyc1RvZ2dsZWQ6IHdpZGdldCA9PlxuICAgICAgICB3aWRnZXQuY29udGVudC5lZGl0b3IuZ2V0T3B0aW9uKCdsaW5lTnVtYmVycycpLFxuICAgICAgd29yZFdyYXBUb2dnbGVkOiB3aWRnZXQgPT5cbiAgICAgICAgd2lkZ2V0LmNvbnRlbnQuZWRpdG9yLmdldE9wdGlvbignbGluZVdyYXAnKSAhPT0gJ29mZicsXG4gICAgICBtYXRjaEJyYWNrZXRzVG9nZ2xlZDogd2lkZ2V0ID0+XG4gICAgICAgIHdpZGdldC5jb250ZW50LmVkaXRvci5nZXRPcHRpb24oJ21hdGNoQnJhY2tldHMnKVxuICAgIH0gYXMgSVZpZXdNZW51LklFZGl0b3JWaWV3ZXI8SURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+Pik7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgRmlsZSBFZGl0b3IgY29uc29sZSBjcmVhdG9yIHRvIHRoZSBGaWxlIG1lbnVcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhZGRDb25zb2xlQ3JlYXRvclRvRmlsZU1lbnUoXG4gICAgbWVudTogSU1haW5NZW51LFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnksXG4gICAgdHJhY2tlcjogV2lkZ2V0VHJhY2tlcjxJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4+LFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApOiB2b2lkIHtcbiAgICBjb25zdCBjcmVhdGVDb25zb2xlOiAoXG4gICAgICB3aWRnZXQ6IElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPlxuICAgICkgPT4gUHJvbWlzZTx2b2lkPiA9IGdldENyZWF0ZUNvbnNvbGVGdW5jdGlvbihjb21tYW5kcyk7XG4gICAgbWVudS5maWxlTWVudS5jb25zb2xlQ3JlYXRvcnMuYWRkKHtcbiAgICAgIHRyYWNrZXIsXG4gICAgICBjcmVhdGVDb25zb2xlTGFiZWw6IChuOiBudW1iZXIpID0+IHRyYW5zLl9fKCdDcmVhdGUgQ29uc29sZSBmb3IgRWRpdG9yJyksXG4gICAgICBjcmVhdGVDb25zb2xlXG4gICAgfSBhcyBJRmlsZU1lbnUuSUNvbnNvbGVDcmVhdG9yPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4pO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIEZpbGUgRWRpdG9yIGNvZGUgcnVubmVyIHRvIHRoZSBSdW4gbWVudVxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGFkZENvZGVSdW5uZXJzVG9SdW5NZW51KFxuICAgIG1lbnU6IElNYWluTWVudSxcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIHRyYWNrZXI6IFdpZGdldFRyYWNrZXI8SURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+PixcbiAgICBjb25zb2xlVHJhY2tlcjogSUNvbnNvbGVUcmFja2VyLFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZSxcbiAgICBzZXNzaW9uRGlhbG9nczogSVNlc3Npb25Db250ZXh0RGlhbG9ncyB8IG51bGxcbiAgKTogdm9pZCB7XG4gICAgbWVudS5ydW5NZW51LmNvZGVSdW5uZXJzLmFkZCh7XG4gICAgICB0cmFja2VyLFxuICAgICAgcnVuTGFiZWw6IChuOiBudW1iZXIpID0+IHRyYW5zLl9fKCdSdW4gQ29kZScpLFxuICAgICAgcnVuQWxsTGFiZWw6IChuOiBudW1iZXIpID0+IHRyYW5zLl9fKCdSdW4gQWxsIENvZGUnKSxcbiAgICAgIHJlc3RhcnRBbmRSdW5BbGxMYWJlbDogKG46IG51bWJlcikgPT5cbiAgICAgICAgdHJhbnMuX18oJ1Jlc3RhcnQgS2VybmVsIGFuZCBSdW4gQWxsIENvZGUnKSxcbiAgICAgIGlzRW5hYmxlZDogY3VycmVudCA9PlxuICAgICAgICAhIWNvbnNvbGVUcmFja2VyLmZpbmQoXG4gICAgICAgICAgd2lkZ2V0ID0+IHdpZGdldC5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5wYXRoID09PSBjdXJyZW50LmNvbnRleHQucGF0aFxuICAgICAgICApLFxuICAgICAgcnVuOiAoKSA9PiBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMucnVuQ29kZSksXG4gICAgICBydW5BbGw6ICgpID0+IGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5ydW5BbGxDb2RlKSxcbiAgICAgIHJlc3RhcnRBbmRSdW5BbGw6IGN1cnJlbnQgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSBjb25zb2xlVHJhY2tlci5maW5kKFxuICAgICAgICAgIHdpZGdldCA9PiB3aWRnZXQuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbj8ucGF0aCA9PT0gY3VycmVudC5jb250ZXh0LnBhdGhcbiAgICAgICAgKTtcbiAgICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICAgIHJldHVybiAoc2Vzc2lvbkRpYWxvZ3MgfHwgc2Vzc2lvbkNvbnRleHREaWFsb2dzKVxuICAgICAgICAgICAgLnJlc3RhcnQod2lkZ2V0LnNlc3Npb25Db250ZXh0KVxuICAgICAgICAgICAgLnRoZW4ocmVzdGFydGVkID0+IHtcbiAgICAgICAgICAgICAgaWYgKHJlc3RhcnRlZCkge1xuICAgICAgICAgICAgICAgIHZvaWQgY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLnJ1bkFsbENvZGUpO1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIHJldHVybiByZXN0YXJ0ZWQ7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0gYXMgSVJ1bk1lbnUuSUNvZGVSdW5uZXI8SURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+Pik7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGZpbGVlZGl0b3ItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBJQ29tbWFuZFBhbGV0dGUsXG4gIElTZXNzaW9uQ29udGV4dERpYWxvZ3MsXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgQ29kZUVkaXRvciwgSUVkaXRvclNlcnZpY2VzIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQgeyBJQ29uc29sZVRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9jb25zb2xlJztcbmltcG9ydCB7IElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IElGaWxlQnJvd3NlckZhY3RvcnkgfSBmcm9tICdAanVweXRlcmxhYi9maWxlYnJvd3Nlcic7XG5pbXBvcnQge1xuICBGaWxlRWRpdG9yLFxuICBGaWxlRWRpdG9yRmFjdG9yeSxcbiAgSUVkaXRvclRyYWNrZXIsXG4gIFRhYlNwYWNlU3RhdHVzXG59IGZyb20gJ0BqdXB5dGVybGFiL2ZpbGVlZGl0b3InO1xuaW1wb3J0IHsgSUxhdW5jaGVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbGF1bmNoZXInO1xuaW1wb3J0IHsgSU1haW5NZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvbWFpbm1lbnUnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJU3RhdHVzQmFyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgSlNPTk9iamVjdCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lbnUgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgQ29tbWFuZHMsIEZBQ1RPUlksIElGaWxlVHlwZURhdGEgfSBmcm9tICcuL2NvbW1hbmRzJztcblxuZXhwb3J0IHsgQ29tbWFuZHMgfSBmcm9tICcuL2NvbW1hbmRzJztcblxuLyoqXG4gKiBUaGUgZWRpdG9yIHRyYWNrZXIgZXh0ZW5zaW9uLlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJRWRpdG9yVHJhY2tlcj4gPSB7XG4gIGFjdGl2YXRlLFxuICBpZDogJ0BqdXB5dGVybGFiL2ZpbGVlZGl0b3ItZXh0ZW5zaW9uOnBsdWdpbicsXG4gIHJlcXVpcmVzOiBbXG4gICAgSUVkaXRvclNlcnZpY2VzLFxuICAgIElGaWxlQnJvd3NlckZhY3RvcnksXG4gICAgSVNldHRpbmdSZWdpc3RyeSxcbiAgICBJVHJhbnNsYXRvclxuICBdLFxuICBvcHRpb25hbDogW1xuICAgIElDb25zb2xlVHJhY2tlcixcbiAgICBJQ29tbWFuZFBhbGV0dGUsXG4gICAgSUxhdW5jaGVyLFxuICAgIElNYWluTWVudSxcbiAgICBJTGF5b3V0UmVzdG9yZXIsXG4gICAgSVNlc3Npb25Db250ZXh0RGlhbG9nc1xuICBdLFxuICBwcm92aWRlczogSUVkaXRvclRyYWNrZXIsXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0aGF0IHByb3ZpZGVzIGEgc3RhdHVzIGl0ZW0gYWxsb3dpbmcgdGhlIHVzZXIgdG9cbiAqIHN3aXRjaCB0YWJzIHZzIHNwYWNlcyBhbmQgdGFiIHdpZHRocyBmb3IgdGV4dCBlZGl0b3JzLlxuICovXG5leHBvcnQgY29uc3QgdGFiU3BhY2VTdGF0dXM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9maWxlZWRpdG9yLWV4dGVuc2lvbjp0YWItc3BhY2Utc3RhdHVzJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lFZGl0b3JUcmFja2VyLCBJU2V0dGluZ1JlZ2lzdHJ5LCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSVN0YXR1c0Jhcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZWRpdG9yVHJhY2tlcjogSUVkaXRvclRyYWNrZXIsXG4gICAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHN0YXR1c0JhcjogSVN0YXR1c0JhciB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBpZiAoIXN0YXR1c0Jhcikge1xuICAgICAgLy8gQXV0b21hdGljYWxseSBkaXNhYmxlIGlmIHN0YXR1c2JhciBtaXNzaW5nXG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIC8vIENyZWF0ZSBhIG1lbnUgZm9yIHN3aXRjaGluZyB0YWJzIHZzIHNwYWNlcy5cbiAgICBjb25zdCBtZW51ID0gbmV3IE1lbnUoeyBjb21tYW5kczogYXBwLmNvbW1hbmRzIH0pO1xuICAgIGNvbnN0IGNvbW1hbmQgPSAnZmlsZWVkaXRvcjpjaGFuZ2UtdGFicyc7XG4gICAgY29uc3QgeyBzaGVsbCB9ID0gYXBwO1xuICAgIGNvbnN0IGFyZ3M6IEpTT05PYmplY3QgPSB7XG4gICAgICBpbnNlcnRTcGFjZXM6IGZhbHNlLFxuICAgICAgc2l6ZTogNCxcbiAgICAgIG5hbWU6IHRyYW5zLl9fKCdJbmRlbnQgd2l0aCBUYWInKVxuICAgIH07XG4gICAgbWVudS5hZGRJdGVtKHsgY29tbWFuZCwgYXJncyB9KTtcbiAgICBmb3IgKGNvbnN0IHNpemUgb2YgWzEsIDIsIDQsIDhdKSB7XG4gICAgICBjb25zdCBhcmdzOiBKU09OT2JqZWN0ID0ge1xuICAgICAgICBpbnNlcnRTcGFjZXM6IHRydWUsXG4gICAgICAgIHNpemUsXG4gICAgICAgIG5hbWU6IHRyYW5zLl9uKCdTcGFjZXM6ICUxJywgJ1NwYWNlczogJTEnLCBzaXplKVxuICAgICAgfTtcbiAgICAgIG1lbnUuYWRkSXRlbSh7IGNvbW1hbmQsIGFyZ3MgfSk7XG4gICAgfVxuXG4gICAgLy8gQ3JlYXRlIHRoZSBzdGF0dXMgaXRlbS5cbiAgICBjb25zdCBpdGVtID0gbmV3IFRhYlNwYWNlU3RhdHVzKHsgbWVudSwgdHJhbnNsYXRvciB9KTtcblxuICAgIC8vIEtlZXAgYSByZWZlcmVuY2UgdG8gdGhlIGNvZGUgZWRpdG9yIGNvbmZpZyBmcm9tIHRoZSBzZXR0aW5ncyBzeXN0ZW0uXG4gICAgY29uc3QgdXBkYXRlU2V0dGluZ3MgPSAoc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzKTogdm9pZCA9PiB7XG4gICAgICBpdGVtLm1vZGVsIS5jb25maWcgPSB7XG4gICAgICAgIC4uLkNvZGVFZGl0b3IuZGVmYXVsdENvbmZpZyxcbiAgICAgICAgLi4uKHNldHRpbmdzLmdldCgnZWRpdG9yQ29uZmlnJykuY29tcG9zaXRlIGFzIEpTT05PYmplY3QpXG4gICAgICB9O1xuICAgIH07XG4gICAgdm9pZCBQcm9taXNlLmFsbChbXG4gICAgICBzZXR0aW5nUmVnaXN0cnkubG9hZCgnQGp1cHl0ZXJsYWIvZmlsZWVkaXRvci1leHRlbnNpb246cGx1Z2luJyksXG4gICAgICBhcHAucmVzdG9yZWRcbiAgICBdKS50aGVuKChbc2V0dGluZ3NdKSA9PiB7XG4gICAgICB1cGRhdGVTZXR0aW5ncyhzZXR0aW5ncyk7XG4gICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3QodXBkYXRlU2V0dGluZ3MpO1xuICAgIH0pO1xuXG4gICAgLy8gQWRkIHRoZSBzdGF0dXMgaXRlbS5cbiAgICBzdGF0dXNCYXIucmVnaXN0ZXJTdGF0dXNJdGVtKFxuICAgICAgJ0BqdXB5dGVybGFiL2ZpbGVlZGl0b3ItZXh0ZW5zaW9uOnRhYi1zcGFjZS1zdGF0dXMnLFxuICAgICAge1xuICAgICAgICBpdGVtLFxuICAgICAgICBhbGlnbjogJ3JpZ2h0JyxcbiAgICAgICAgcmFuazogMSxcbiAgICAgICAgaXNBY3RpdmU6ICgpID0+IHtcbiAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgISFzaGVsbC5jdXJyZW50V2lkZ2V0ICYmIGVkaXRvclRyYWNrZXIuaGFzKHNoZWxsLmN1cnJlbnRXaWRnZXQpXG4gICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICk7XG4gIH1cbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbcGx1Z2luLCB0YWJTcGFjZVN0YXR1c107XG5leHBvcnQgZGVmYXVsdCBwbHVnaW5zO1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBlZGl0b3IgdHJhY2tlciBwbHVnaW4uXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgZWRpdG9yU2VydmljZXM6IElFZGl0b3JTZXJ2aWNlcyxcbiAgYnJvd3NlckZhY3Rvcnk6IElGaWxlQnJvd3NlckZhY3RvcnksXG4gIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIGNvbnNvbGVUcmFja2VyOiBJQ29uc29sZVRyYWNrZXIgfCBudWxsLFxuICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsLFxuICBsYXVuY2hlcjogSUxhdW5jaGVyIHwgbnVsbCxcbiAgbWVudTogSU1haW5NZW51IHwgbnVsbCxcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGwsXG4gIHNlc3Npb25EaWFsb2dzOiBJU2Vzc2lvbkNvbnRleHREaWFsb2dzIHwgbnVsbFxuKTogSUVkaXRvclRyYWNrZXIge1xuICBjb25zdCBpZCA9IHBsdWdpbi5pZDtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgbmFtZXNwYWNlID0gJ2VkaXRvcic7XG4gIGNvbnN0IGZhY3RvcnkgPSBuZXcgRmlsZUVkaXRvckZhY3Rvcnkoe1xuICAgIGVkaXRvclNlcnZpY2VzLFxuICAgIGZhY3RvcnlPcHRpb25zOiB7XG4gICAgICBuYW1lOiBGQUNUT1JZLFxuICAgICAgZmlsZVR5cGVzOiBbJ21hcmtkb3duJywgJyonXSwgLy8gRXhwbGljaXRseSBhZGQgdGhlIG1hcmtkb3duIGZpbGVUeXBlIHNvXG4gICAgICBkZWZhdWx0Rm9yOiBbJ21hcmtkb3duJywgJyonXSAvLyBpdCBvdXRyYW5rcyB0aGUgZGVmYXVsdFJlbmRlcmVkIHZpZXdlci5cbiAgICB9XG4gIH0pO1xuICBjb25zdCB7IGNvbW1hbmRzLCByZXN0b3JlZCwgc2hlbGwgfSA9IGFwcDtcbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4oe1xuICAgIG5hbWVzcGFjZVxuICB9KTtcbiAgY29uc3QgaXNFbmFibGVkID0gKCkgPT5cbiAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgIT09IG51bGwgJiZcbiAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgPT09IHNoZWxsLmN1cnJlbnRXaWRnZXQ7XG5cbiAgY29uc3QgY29tbW9uTGFuZ3VhZ2VGaWxlVHlwZURhdGEgPSBuZXcgTWFwPHN0cmluZywgSUZpbGVUeXBlRGF0YVtdPihbXG4gICAgW1xuICAgICAgJ3B5dGhvbicsXG4gICAgICBbXG4gICAgICAgIHtcbiAgICAgICAgICBmaWxlRXh0OiAncHknLFxuICAgICAgICAgIGljb25OYW1lOiAndWktY29tcG9uZW50czpweXRob24nLFxuICAgICAgICAgIGxhdW5jaGVyTGFiZWw6IHRyYW5zLl9fKCdQeXRob24gRmlsZScpLFxuICAgICAgICAgIHBhbGV0dGVMYWJlbDogdHJhbnMuX18oJ05ldyBQeXRob24gRmlsZScpLFxuICAgICAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdDcmVhdGUgYSBuZXcgUHl0aG9uIGZpbGUnKVxuICAgICAgICB9XG4gICAgICBdXG4gICAgXSxcbiAgICBbXG4gICAgICAnanVsaWEnLFxuICAgICAgW1xuICAgICAgICB7XG4gICAgICAgICAgZmlsZUV4dDogJ2psJyxcbiAgICAgICAgICBpY29uTmFtZTogJ3VpLWNvbXBvbmVudHM6anVsaWEnLFxuICAgICAgICAgIGxhdW5jaGVyTGFiZWw6IHRyYW5zLl9fKCdKdWxpYSBGaWxlJyksXG4gICAgICAgICAgcGFsZXR0ZUxhYmVsOiB0cmFucy5fXygnTmV3IEp1bGlhIEZpbGUnKSxcbiAgICAgICAgICBjYXB0aW9uOiB0cmFucy5fXygnQ3JlYXRlIGEgbmV3IEp1bGlhIGZpbGUnKVxuICAgICAgICB9XG4gICAgICBdXG4gICAgXSxcbiAgICBbXG4gICAgICAnUicsXG4gICAgICBbXG4gICAgICAgIHtcbiAgICAgICAgICBmaWxlRXh0OiAncicsXG4gICAgICAgICAgaWNvbk5hbWU6ICd1aS1jb21wb25lbnRzOnIta2VybmVsJyxcbiAgICAgICAgICBsYXVuY2hlckxhYmVsOiB0cmFucy5fXygnUiBGaWxlJyksXG4gICAgICAgICAgcGFsZXR0ZUxhYmVsOiB0cmFucy5fXygnTmV3IFIgRmlsZScpLFxuICAgICAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdDcmVhdGUgYSBuZXcgUiBmaWxlJylcbiAgICAgICAgfVxuICAgICAgXVxuICAgIF1cbiAgXSk7XG5cbiAgLy8gVXNlIGF2YWlsYWJsZSBrZXJuZWxzIHRvIGRldGVybWluZSB3aGljaCBjb21tb24gZmlsZSB0eXBlcyBzaG91bGQgaGF2ZSAnQ3JlYXRlIE5ldycgb3B0aW9ucyBpbiB0aGUgTGF1bmNoZXIsIEZpbGUgRWRpdG9yIHBhbGV0dGUsIGFuZCBGaWxlIG1lbnVcbiAgY29uc3QgZ2V0QXZhaWxhYmxlS2VybmVsRmlsZVR5cGVzID0gYXN5bmMgKCk6IFByb21pc2U8U2V0PElGaWxlVHlwZURhdGE+PiA9PiB7XG4gICAgY29uc3Qgc3BlY3NNYW5hZ2VyID0gYXBwLnNlcnZpY2VNYW5hZ2VyLmtlcm5lbHNwZWNzO1xuICAgIGF3YWl0IHNwZWNzTWFuYWdlci5yZWFkeTtcbiAgICBsZXQgZmlsZVR5cGVzID0gbmV3IFNldDxJRmlsZVR5cGVEYXRhPigpO1xuICAgIGNvbnN0IHNwZWNzID0gc3BlY3NNYW5hZ2VyLnNwZWNzPy5rZXJuZWxzcGVjcyA/PyB7fTtcbiAgICBPYmplY3Qua2V5cyhzcGVjcykuZm9yRWFjaChzcGVjID0+IHtcbiAgICAgIGNvbnN0IHNwZWNNb2RlbCA9IHNwZWNzW3NwZWNdO1xuICAgICAgaWYgKHNwZWNNb2RlbCkge1xuICAgICAgICBjb25zdCBleHRzID0gY29tbW9uTGFuZ3VhZ2VGaWxlVHlwZURhdGEuZ2V0KHNwZWNNb2RlbC5sYW5ndWFnZSk7XG4gICAgICAgIGV4dHM/LmZvckVhY2goZXh0ID0+IGZpbGVUeXBlcy5hZGQoZXh0KSk7XG4gICAgICB9XG4gICAgfSk7XG4gICAgcmV0dXJuIGZpbGVUeXBlcztcbiAgfTtcblxuICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gIGlmIChyZXN0b3Jlcikge1xuICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZSh0cmFja2VyLCB7XG4gICAgICBjb21tYW5kOiAnZG9jbWFuYWdlcjpvcGVuJyxcbiAgICAgIGFyZ3M6IHdpZGdldCA9PiAoeyBwYXRoOiB3aWRnZXQuY29udGV4dC5wYXRoLCBmYWN0b3J5OiBGQUNUT1JZIH0pLFxuICAgICAgbmFtZTogd2lkZ2V0ID0+IHdpZGdldC5jb250ZXh0LnBhdGhcbiAgICB9KTtcbiAgfVxuXG4gIC8vIEFkZCBhIGNvbnNvbGUgY3JlYXRvciB0byB0aGUgRmlsZSBtZW51XG4gIC8vIEZldGNoIHRoZSBpbml0aWFsIHN0YXRlIG9mIHRoZSBzZXR0aW5ncy5cbiAgUHJvbWlzZS5hbGwoW3NldHRpbmdSZWdpc3RyeS5sb2FkKGlkKSwgcmVzdG9yZWRdKVxuICAgIC50aGVuKChbc2V0dGluZ3NdKSA9PiB7XG4gICAgICBDb21tYW5kcy51cGRhdGVTZXR0aW5ncyhzZXR0aW5ncywgY29tbWFuZHMpO1xuICAgICAgQ29tbWFuZHMudXBkYXRlVHJhY2tlcih0cmFja2VyKTtcbiAgICAgIHNldHRpbmdzLmNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgIENvbW1hbmRzLnVwZGF0ZVNldHRpbmdzKHNldHRpbmdzLCBjb21tYW5kcyk7XG4gICAgICAgIENvbW1hbmRzLnVwZGF0ZVRyYWNrZXIodHJhY2tlcik7XG4gICAgICB9KTtcbiAgICB9KVxuICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgY29uc29sZS5lcnJvcihyZWFzb24ubWVzc2FnZSk7XG4gICAgICBDb21tYW5kcy51cGRhdGVUcmFja2VyKHRyYWNrZXIpO1xuICAgIH0pO1xuXG4gIGZhY3Rvcnkud2lkZ2V0Q3JlYXRlZC5jb25uZWN0KChzZW5kZXIsIHdpZGdldCkgPT4ge1xuICAgIC8vIE5vdGlmeSB0aGUgd2lkZ2V0IHRyYWNrZXIgaWYgcmVzdG9yZSBkYXRhIG5lZWRzIHRvIHVwZGF0ZS5cbiAgICB3aWRnZXQuY29udGV4dC5wYXRoQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHZvaWQgdHJhY2tlci5zYXZlKHdpZGdldCk7XG4gICAgfSk7XG4gICAgdm9pZCB0cmFja2VyLmFkZCh3aWRnZXQpO1xuICAgIENvbW1hbmRzLnVwZGF0ZVdpZGdldCh3aWRnZXQuY29udGVudCk7XG4gIH0pO1xuICBhcHAuZG9jUmVnaXN0cnkuYWRkV2lkZ2V0RmFjdG9yeShmYWN0b3J5KTtcblxuICAvLyBIYW5kbGUgdGhlIHNldHRpbmdzIG9mIG5ldyB3aWRnZXRzLlxuICB0cmFja2VyLndpZGdldEFkZGVkLmNvbm5lY3QoKHNlbmRlciwgd2lkZ2V0KSA9PiB7XG4gICAgQ29tbWFuZHMudXBkYXRlV2lkZ2V0KHdpZGdldC5jb250ZW50KTtcbiAgfSk7XG5cbiAgQ29tbWFuZHMuYWRkQ29tbWFuZHMoXG4gICAgY29tbWFuZHMsXG4gICAgc2V0dGluZ1JlZ2lzdHJ5LFxuICAgIHRyYW5zLFxuICAgIGlkLFxuICAgIGlzRW5hYmxlZCxcbiAgICB0cmFja2VyLFxuICAgIGJyb3dzZXJGYWN0b3J5XG4gICk7XG5cbiAgLy8gQWRkIGEgbGF1bmNoZXIgaXRlbSBpZiB0aGUgbGF1bmNoZXIgaXMgYXZhaWxhYmxlLlxuICBpZiAobGF1bmNoZXIpIHtcbiAgICBDb21tYW5kcy5hZGRMYXVuY2hlckl0ZW1zKGxhdW5jaGVyLCB0cmFucyk7XG4gIH1cblxuICBpZiAocGFsZXR0ZSkge1xuICAgIENvbW1hbmRzLmFkZFBhbGV0dGVJdGVtcyhwYWxldHRlLCB0cmFucyk7XG4gIH1cblxuICBpZiAobWVudSkge1xuICAgIENvbW1hbmRzLmFkZE1lbnVJdGVtcyhcbiAgICAgIG1lbnUsXG4gICAgICBjb21tYW5kcyxcbiAgICAgIHRyYWNrZXIsXG4gICAgICB0cmFucyxcbiAgICAgIGNvbnNvbGVUcmFja2VyLFxuICAgICAgc2Vzc2lvbkRpYWxvZ3NcbiAgICApO1xuICB9XG5cbiAgZ2V0QXZhaWxhYmxlS2VybmVsRmlsZVR5cGVzKClcbiAgICAudGhlbihhdmFpbGFibGVLZXJuZWxGaWxlVHlwZXMgPT4ge1xuICAgICAgaWYgKGxhdW5jaGVyKSB7XG4gICAgICAgIENvbW1hbmRzLmFkZEtlcm5lbExhbmd1YWdlTGF1bmNoZXJJdGVtcyhcbiAgICAgICAgICBsYXVuY2hlcixcbiAgICAgICAgICB0cmFucyxcbiAgICAgICAgICBhdmFpbGFibGVLZXJuZWxGaWxlVHlwZXNcbiAgICAgICAgKTtcbiAgICAgIH1cblxuICAgICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgICAgQ29tbWFuZHMuYWRkS2VybmVsTGFuZ3VhZ2VQYWxldHRlSXRlbXMoXG4gICAgICAgICAgcGFsZXR0ZSxcbiAgICAgICAgICB0cmFucyxcbiAgICAgICAgICBhdmFpbGFibGVLZXJuZWxGaWxlVHlwZXNcbiAgICAgICAgKTtcbiAgICAgIH1cblxuICAgICAgaWYgKG1lbnUpIHtcbiAgICAgICAgQ29tbWFuZHMuYWRkS2VybmVsTGFuZ3VhZ2VNZW51SXRlbXMobWVudSwgYXZhaWxhYmxlS2VybmVsRmlsZVR5cGVzKTtcbiAgICAgIH1cbiAgICB9KVxuICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgY29uc29sZS5lcnJvcihyZWFzb24ubWVzc2FnZSk7XG4gICAgfSk7XG5cbiAgcmV0dXJuIHRyYWNrZXI7XG59XG4iXSwic291cmNlUm9vdCI6IiJ9