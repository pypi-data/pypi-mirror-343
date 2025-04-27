(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_debugger-extension_lib_index_js"],{

/***/ "../packages/debugger-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/debugger-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/debugger */ "webpack/sharing/consume/default/@jupyterlab/debugger/@jupyterlab/debugger");
/* harmony import */ var _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole/@jupyterlab/logconsole");
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module debugger-extension
 */














/**
 * A plugin that provides visual debugging support for consoles.
 */
const consoles = {
    id: '@jupyterlab/debugger-extension:consoles',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, debug, consoleTracker, labShell) => {
        const handler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Handler({
            type: 'console',
            shell: app.shell,
            service: debug
        });
        const updateHandlerAndCommands = async (widget) => {
            const { sessionContext } = widget;
            await sessionContext.ready;
            await handler.updateContext(widget, sessionContext);
            app.commands.notifyCommandChanged();
        };
        if (labShell) {
            labShell.currentChanged.connect(async (_, update) => {
                const widget = update.newValue;
                if (!(widget instanceof _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.ConsolePanel)) {
                    return;
                }
                await updateHandlerAndCommands(widget);
            });
            return;
        }
        consoleTracker.currentChanged.connect(async (_, consolePanel) => {
            if (consolePanel) {
                void updateHandlerAndCommands(consolePanel);
            }
        });
    }
};
/**
 * A plugin that provides visual debugging support for file editors.
 */
const files = {
    id: '@jupyterlab/debugger-extension:files',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__.IEditorTracker],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, debug, editorTracker, labShell) => {
        const handler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Handler({
            type: 'file',
            shell: app.shell,
            service: debug
        });
        const activeSessions = {};
        const updateHandlerAndCommands = async (widget) => {
            const sessions = app.serviceManager.sessions;
            try {
                const model = await sessions.findByPath(widget.context.path);
                if (!model) {
                    return;
                }
                let session = activeSessions[model.id];
                if (!session) {
                    // Use `connectTo` only if the session does not exist.
                    // `connectTo` sends a kernel_info_request on the shell
                    // channel, which blocks the debug session restore when waiting
                    // for the kernel to be ready
                    session = sessions.connectTo({ model });
                    activeSessions[model.id] = session;
                }
                await handler.update(widget, session);
                app.commands.notifyCommandChanged();
            }
            catch (_a) {
                return;
            }
        };
        if (labShell) {
            labShell.currentChanged.connect(async (_, update) => {
                const widget = update.newValue;
                if (!(widget instanceof _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7__.DocumentWidget)) {
                    return;
                }
                const content = widget.content;
                if (!(content instanceof _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__.FileEditor)) {
                    return;
                }
                await updateHandlerAndCommands(widget);
            });
        }
        editorTracker.currentChanged.connect(async (_, documentWidget) => {
            await updateHandlerAndCommands(documentWidget);
        });
    }
};
/**
 * A plugin that provides visual debugging support for notebooks.
 */
const notebooks = {
    id: '@jupyterlab/debugger-extension:notebooks',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.INotebookTracker, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, service, notebookTracker, translator, labShell, palette) => {
        const handler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Handler({
            type: 'notebook',
            shell: app.shell,
            service
        });
        const trans = translator.load('jupyterlab');
        app.commands.addCommand(_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs.restartDebug, {
            label: trans.__('Restart Kernel and Debug…'),
            caption: trans.__('Restart Kernel and Debug…'),
            isEnabled: () => {
                return service.isStarted;
            },
            execute: async () => {
                const state = service.getDebuggerState();
                console.log(state.cells);
                const { context, content } = notebookTracker.currentWidget;
                await service.stop();
                const restarted = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.sessionContextDialogs.restart(context.sessionContext);
                if (restarted) {
                    await service.restoreDebuggerState(state);
                    await handler.updateWidget(notebookTracker.currentWidget, notebookTracker.currentWidget.sessionContext.session);
                    await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookActions.runAll(content, context.sessionContext);
                }
            }
        });
        const updateHandlerAndCommands = async (widget) => {
            const { sessionContext } = widget;
            await sessionContext.ready;
            await handler.updateContext(widget, sessionContext);
            app.commands.notifyCommandChanged();
        };
        if (labShell) {
            labShell.currentChanged.connect(async (_, update) => {
                const widget = update.newValue;
                if (!(widget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel)) {
                    return;
                }
                await updateHandlerAndCommands(widget);
            });
            return;
        }
        if (palette) {
            palette.addItem({
                category: 'Notebook Operations',
                command: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs.restartDebug
            });
        }
        notebookTracker.currentChanged.connect(async (_, notebookPanel) => {
            await updateHandlerAndCommands(notebookPanel);
        });
    }
};
/**
 * A plugin that provides a debugger service.
 */
const service = {
    id: '@jupyterlab/debugger-extension:service',
    autoStart: true,
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerConfig],
    optional: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSources],
    activate: (app, config, debuggerSources) => new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Service({
        config,
        debuggerSources,
        specsManager: app.serviceManager.kernelspecs
    })
};
/**
 * A plugin that provides a configuration with hash method.
 */
const configuration = {
    id: '@jupyterlab/debugger-extension:config',
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerConfig,
    autoStart: true,
    activate: () => new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Config()
};
/**
 * A plugin that provides source/editor functionality for debugging.
 */
const sources = {
    id: '@jupyterlab/debugger-extension:sources',
    autoStart: true,
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSources,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerConfig, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices],
    optional: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.INotebookTracker, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__.IEditorTracker],
    activate: (app, config, editorServices, notebookTracker, consoleTracker, editorTracker) => {
        return new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Sources({
            config,
            shell: app.shell,
            editorServices,
            notebookTracker,
            consoleTracker,
            editorTracker
        });
    }
};
/*
 * A plugin to open detailed views for variables.
 */
const variables = {
    id: '@jupyterlab/debugger-extension:variables',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager],
    activate: (app, service, translator, themeManager) => {
        const trans = translator.load('jupyterlab');
        const { commands, shell } = app;
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'debugger/inspect-variable'
        });
        const CommandIDs = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs;
        commands.addCommand(CommandIDs.inspectVariable, {
            label: trans.__('Inspect Variable'),
            caption: trans.__('Inspect Variable'),
            execute: async (args) => {
                var _a, _b;
                const { variableReference } = args;
                if (!variableReference || variableReference === 0) {
                    return;
                }
                const variables = await service.inspectVariable(variableReference);
                const title = args.title;
                const id = `jp-debugger-variable-${title}`;
                if (!variables ||
                    variables.length === 0 ||
                    tracker.find(widget => widget.id === id)) {
                    return;
                }
                const model = service.model.variables;
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                    content: new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.VariablesGrid({
                        model,
                        commands,
                        scopes: [{ name: title, variables }],
                        themeManager
                    })
                });
                widget.addClass('jp-DebuggerVariables');
                widget.id = id;
                widget.title.icon = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.variableIcon;
                widget.title.label = `${(_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.name} - ${title}`;
                void tracker.add(widget);
                model.changed.connect(() => widget.dispose());
                shell.add(widget, 'main', {
                    mode: tracker.currentWidget ? 'split-right' : 'split-bottom'
                });
            }
        });
    }
};
/**
 * Debugger sidebar provider plugin.
 */
const sidebar = {
    id: '@jupyterlab/debugger-extension:sidebar',
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSidebar,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__.ISettingRegistry],
    autoStart: true,
    activate: async (app, service, editorServices, translator, themeManager, settingRegistry) => {
        const { commands } = app;
        const CommandIDs = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs;
        const callstackCommands = {
            registry: commands,
            continue: CommandIDs.debugContinue,
            terminate: CommandIDs.terminate,
            next: CommandIDs.next,
            stepIn: CommandIDs.stepIn,
            stepOut: CommandIDs.stepOut,
            evaluate: CommandIDs.evaluate
        };
        const sidebar = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Sidebar({
            service,
            callstackCommands,
            editorServices,
            themeManager,
            translator
        });
        if (settingRegistry) {
            const setting = await settingRegistry.load(main.id);
            const updateSettings = () => {
                var _a, _b, _c, _d;
                const filters = setting.get('variableFilters').composite;
                const kernel = (_d = (_c = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '';
                if (kernel && filters[kernel]) {
                    sidebar.variables.filter = new Set(filters[kernel]);
                }
            };
            updateSettings();
            setting.changed.connect(updateSettings);
            service.sessionChanged.connect(updateSettings);
        }
        return sidebar;
    }
};
/**
 * The main debugger UI plugin.
 */
const main = {
    id: '@jupyterlab/debugger-extension:main',
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSidebar, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSources,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9__.ILoggerRegistry
    ],
    autoStart: true,
    activate: async (app, service, sidebar, editorServices, translator, palette, debuggerSources, labShell, restorer, loggerRegistry) => {
        var _a;
        const trans = translator.load('jupyterlab');
        const { commands, shell, serviceManager } = app;
        const { kernelspecs } = serviceManager;
        const CommandIDs = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs;
        // First check if there is a PageConfig override for the extension visibility
        const alwaysShowDebuggerExtension = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PageConfig.getOption('alwaysShowDebuggerExtension').toLowerCase() ===
            'true';
        if (!alwaysShowDebuggerExtension) {
            // hide the debugger sidebar if no kernel with support for debugging is available
            await kernelspecs.ready;
            const specs = (_a = kernelspecs.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs;
            if (!specs) {
                return;
            }
            const enabled = Object.keys(specs).some(name => { var _a, _b, _c; return !!((_c = (_b = (_a = specs[name]) === null || _a === void 0 ? void 0 : _a.metadata) === null || _b === void 0 ? void 0 : _b['debugger']) !== null && _c !== void 0 ? _c : false); });
            if (!enabled) {
                return;
            }
        }
        // get the mime type of the kernel language for the current debug session
        const getMimeType = async () => {
            var _a, _b, _c;
            const kernel = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel;
            if (!kernel) {
                return '';
            }
            const info = (await kernel.info).language_info;
            const name = info.name;
            const mimeType = (_c = editorServices === null || editorServices === void 0 ? void 0 : editorServices.mimeTypeService.getMimeTypeByLanguage({ name })) !== null && _c !== void 0 ? _c : '';
            return mimeType;
        };
        const rendermime = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__.RenderMimeRegistry({ initialFactories: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__.standardRendererFactories });
        commands.addCommand(CommandIDs.evaluate, {
            label: trans.__('Evaluate Code'),
            caption: trans.__('Evaluate Code'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.evaluateIcon,
            isEnabled: () => {
                return service.hasStoppedThreads();
            },
            execute: async () => {
                var _a, _b, _c;
                const mimeType = await getMimeType();
                const result = await _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Dialogs.getCode({
                    title: trans.__('Evaluate Code'),
                    okLabel: trans.__('Evaluate'),
                    cancelLabel: trans.__('Cancel'),
                    mimeType,
                    rendermime
                });
                const code = result.value;
                if (!result.button.accept || !code) {
                    return;
                }
                const reply = await service.evaluate(code);
                if (reply) {
                    const data = reply.result;
                    const path = (_b = (_a = service === null || service === void 0 ? void 0 : service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.path;
                    const logger = path ? (_c = loggerRegistry === null || loggerRegistry === void 0 ? void 0 : loggerRegistry.getLogger) === null || _c === void 0 ? void 0 : _c.call(loggerRegistry, path) : undefined;
                    if (logger) {
                        // print to log console of the notebook currently being debugged
                        logger.log({ type: 'text', data, level: logger.level });
                    }
                    else {
                        // fallback to printing to devtools console
                        console.debug(data);
                    }
                }
            }
        });
        commands.addCommand(CommandIDs.debugContinue, {
            label: trans.__('Continue'),
            caption: trans.__('Continue'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.continueIcon,
            isEnabled: () => {
                return service.hasStoppedThreads();
            },
            execute: async () => {
                await service.continue();
                commands.notifyCommandChanged();
            }
        });
        commands.addCommand(CommandIDs.terminate, {
            label: trans.__('Terminate'),
            caption: trans.__('Terminate'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.terminateIcon,
            isEnabled: () => {
                return service.hasStoppedThreads();
            },
            execute: async () => {
                await service.restart();
                commands.notifyCommandChanged();
            }
        });
        commands.addCommand(CommandIDs.next, {
            label: trans.__('Next'),
            caption: trans.__('Next'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.stepOverIcon,
            isEnabled: () => {
                return service.hasStoppedThreads();
            },
            execute: async () => {
                await service.next();
            }
        });
        commands.addCommand(CommandIDs.stepIn, {
            label: trans.__('Step In'),
            caption: trans.__('Step In'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.stepIntoIcon,
            isEnabled: () => {
                return service.hasStoppedThreads();
            },
            execute: async () => {
                await service.stepIn();
            }
        });
        commands.addCommand(CommandIDs.stepOut, {
            label: trans.__('Step Out'),
            caption: trans.__('Step Out'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.stepOutIcon,
            isEnabled: () => {
                return service.hasStoppedThreads();
            },
            execute: async () => {
                await service.stepOut();
            }
        });
        service.eventMessage.connect((_, event) => {
            commands.notifyCommandChanged();
            if (labShell && event.event === 'initialized') {
                labShell.activateById(sidebar.id);
            }
        });
        service.sessionChanged.connect(_ => {
            commands.notifyCommandChanged();
        });
        if (restorer) {
            restorer.add(sidebar, 'debugger-sidebar');
        }
        sidebar.node.setAttribute('role', 'region');
        sidebar.node.setAttribute('aria-label', trans.__('Debugger section'));
        shell.add(sidebar, 'right');
        if (palette) {
            const category = trans.__('Debugger');
            [
                CommandIDs.debugContinue,
                CommandIDs.terminate,
                CommandIDs.next,
                CommandIDs.stepIn,
                CommandIDs.stepOut,
                CommandIDs.evaluate
            ].forEach(command => {
                palette.addItem({ command, category });
            });
        }
        if (debuggerSources) {
            const { model } = service;
            const readOnlyEditorFactory = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.ReadOnlyEditorFactory({
                editorServices
            });
            const onCurrentFrameChanged = (_, frame) => {
                var _a, _b, _c, _d, _e, _f, _g, _h, _j;
                debuggerSources
                    .find({
                    focus: true,
                    kernel: (_d = (_c = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '',
                    path: (_g = (_f = (_e = service.session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.path) !== null && _g !== void 0 ? _g : '',
                    source: (_j = (_h = frame === null || frame === void 0 ? void 0 : frame.source) === null || _h === void 0 ? void 0 : _h.path) !== null && _j !== void 0 ? _j : ''
                })
                    .forEach(editor => {
                    requestAnimationFrame(() => {
                        _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.EditorHandler.showCurrentLine(editor, frame.line);
                    });
                });
            };
            const onCurrentSourceOpened = (_, source, breakpoint) => {
                var _a, _b, _c, _d, _e, _f, _g;
                if (!source) {
                    return;
                }
                const { content, mimeType, path } = source;
                const results = debuggerSources.find({
                    focus: true,
                    kernel: (_d = (_c = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '',
                    path: (_g = (_f = (_e = service.session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.path) !== null && _g !== void 0 ? _g : '',
                    source: path
                });
                if (results.length > 0) {
                    if (breakpoint && typeof breakpoint.line !== 'undefined') {
                        results.forEach(editor => {
                            if (editor instanceof _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_3__.CodeMirrorEditor) {
                                editor.scrollIntoViewCentered({
                                    line: breakpoint.line - 1,
                                    ch: breakpoint.column || 0
                                });
                            }
                            else {
                                editor.revealPosition({
                                    line: breakpoint.line - 1,
                                    column: breakpoint.column || 0
                                });
                            }
                        });
                    }
                    return;
                }
                const editorWrapper = readOnlyEditorFactory.createNewEditor({
                    content,
                    mimeType,
                    path
                });
                const editor = editorWrapper.editor;
                const editorHandler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.EditorHandler({
                    debuggerService: service,
                    editor,
                    path
                });
                editorWrapper.disposed.connect(() => editorHandler.dispose());
                debuggerSources.open({
                    label: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PathExt.basename(path),
                    caption: path,
                    editorWrapper
                });
                const frame = service.model.callstack.frame;
                if (frame) {
                    _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.EditorHandler.showCurrentLine(editor, frame.line);
                }
            };
            model.callstack.currentFrameChanged.connect(onCurrentFrameChanged);
            model.sources.currentSourceOpened.connect(onCurrentSourceOpened);
            model.breakpoints.clicked.connect(async (_, breakpoint) => {
                var _a;
                const path = (_a = breakpoint.source) === null || _a === void 0 ? void 0 : _a.path;
                const source = await service.getSource({
                    sourceReference: 0,
                    path
                });
                onCurrentSourceOpened(null, source, breakpoint);
            });
        }
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    service,
    consoles,
    files,
    notebooks,
    variables,
    sidebar,
    main,
    sources,
    configuration
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZGVidWdnZXItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTzhCO0FBT0g7QUFDMkI7QUFDQztBQUNVO0FBQ1I7QUFPOUI7QUFDMkI7QUFDVztBQUNYO0FBSzNCO0FBSUU7QUFFK0I7QUFDVDtBQUV0RDs7R0FFRztBQUNILE1BQU0sUUFBUSxHQUFnQztJQUM1QyxFQUFFLEVBQUUseUNBQXlDO0lBQzdDLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQUMsMkRBQVMsRUFBRSxnRUFBZSxDQUFDO0lBQ3RDLFFBQVEsRUFBRSxDQUFDLDhEQUFTLENBQUM7SUFDckIsUUFBUSxFQUFFLENBQ1IsR0FBb0IsRUFDcEIsS0FBZ0IsRUFDaEIsY0FBK0IsRUFDL0IsUUFBMEIsRUFDMUIsRUFBRTtRQUNGLE1BQU0sT0FBTyxHQUFHLElBQUksa0VBQWdCLENBQUM7WUFDbkMsSUFBSSxFQUFFLFNBQVM7WUFDZixLQUFLLEVBQUUsR0FBRyxDQUFDLEtBQUs7WUFDaEIsT0FBTyxFQUFFLEtBQUs7U0FDZixDQUFDLENBQUM7UUFFSCxNQUFNLHdCQUF3QixHQUFHLEtBQUssRUFDcEMsTUFBb0IsRUFDTCxFQUFFO1lBQ2pCLE1BQU0sRUFBRSxjQUFjLEVBQUUsR0FBRyxNQUFNLENBQUM7WUFDbEMsTUFBTSxjQUFjLENBQUMsS0FBSyxDQUFDO1lBQzNCLE1BQU0sT0FBTyxDQUFDLGFBQWEsQ0FBQyxNQUFNLEVBQUUsY0FBYyxDQUFDLENBQUM7WUFDcEQsR0FBRyxDQUFDLFFBQVEsQ0FBQyxvQkFBb0IsRUFBRSxDQUFDO1FBQ3RDLENBQUMsQ0FBQztRQUVGLElBQUksUUFBUSxFQUFFO1lBQ1osUUFB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MmFjMzMxYjdlODgxYzI1MjMuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBkZWJ1Z2dlci1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGFiU2hlbGwsXG4gIElMYXlvdXRSZXN0b3JlcixcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBJVGhlbWVNYW5hZ2VyLFxuICBNYWluQXJlYVdpZGdldCxcbiAgc2Vzc2lvbkNvbnRleHREaWFsb2dzLFxuICBXaWRnZXRUcmFja2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElFZGl0b3JTZXJ2aWNlcyB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0IHsgQ29kZU1pcnJvckVkaXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVtaXJyb3InO1xuaW1wb3J0IHsgQ29uc29sZVBhbmVsLCBJQ29uc29sZVRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9jb25zb2xlJztcbmltcG9ydCB7IFBhZ2VDb25maWcsIFBhdGhFeHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHtcbiAgRGVidWdnZXIsXG4gIElEZWJ1Z2dlcixcbiAgSURlYnVnZ2VyQ29uZmlnLFxuICBJRGVidWdnZXJTaWRlYmFyLFxuICBJRGVidWdnZXJTb3VyY2VzXG59IGZyb20gJ0BqdXB5dGVybGFiL2RlYnVnZ2VyJztcbmltcG9ydCB7IERvY3VtZW50V2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgRmlsZUVkaXRvciwgSUVkaXRvclRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9maWxlZWRpdG9yJztcbmltcG9ydCB7IElMb2dnZXJSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL2xvZ2NvbnNvbGUnO1xuaW1wb3J0IHtcbiAgSU5vdGVib29rVHJhY2tlcixcbiAgTm90ZWJvb2tBY3Rpb25zLFxuICBOb3RlYm9va1BhbmVsXG59IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcbmltcG9ydCB7XG4gIHN0YW5kYXJkUmVuZGVyZXJGYWN0b3JpZXMgYXMgaW5pdGlhbEZhY3RvcmllcyxcbiAgUmVuZGVyTWltZVJlZ2lzdHJ5XG59IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgU2Vzc2lvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbi8qKlxuICogQSBwbHVnaW4gdGhhdCBwcm92aWRlcyB2aXN1YWwgZGVidWdnaW5nIHN1cHBvcnQgZm9yIGNvbnNvbGVzLlxuICovXG5jb25zdCBjb25zb2xlczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2RlYnVnZ2VyLWV4dGVuc2lvbjpjb25zb2xlcycsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJRGVidWdnZXIsIElDb25zb2xlVHJhY2tlcl0sXG4gIG9wdGlvbmFsOiBbSUxhYlNoZWxsXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBkZWJ1ZzogSURlYnVnZ2VyLFxuICAgIGNvbnNvbGVUcmFja2VyOiBJQ29uc29sZVRyYWNrZXIsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgaGFuZGxlciA9IG5ldyBEZWJ1Z2dlci5IYW5kbGVyKHtcbiAgICAgIHR5cGU6ICdjb25zb2xlJyxcbiAgICAgIHNoZWxsOiBhcHAuc2hlbGwsXG4gICAgICBzZXJ2aWNlOiBkZWJ1Z1xuICAgIH0pO1xuXG4gICAgY29uc3QgdXBkYXRlSGFuZGxlckFuZENvbW1hbmRzID0gYXN5bmMgKFxuICAgICAgd2lkZ2V0OiBDb25zb2xlUGFuZWxcbiAgICApOiBQcm9taXNlPHZvaWQ+ID0+IHtcbiAgICAgIGNvbnN0IHsgc2Vzc2lvbkNvbnRleHQgfSA9IHdpZGdldDtcbiAgICAgIGF3YWl0IHNlc3Npb25Db250ZXh0LnJlYWR5O1xuICAgICAgYXdhaXQgaGFuZGxlci51cGRhdGVDb250ZXh0KHdpZGdldCwgc2Vzc2lvbkNvbnRleHQpO1xuICAgICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKCk7XG4gICAgfTtcblxuICAgIGlmIChsYWJTaGVsbCkge1xuICAgICAgbGFiU2hlbGwuY3VycmVudENoYW5nZWQuY29ubmVjdChhc3luYyAoXywgdXBkYXRlKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IHVwZGF0ZS5uZXdWYWx1ZTtcbiAgICAgICAgaWYgKCEod2lkZ2V0IGluc3RhbmNlb2YgQ29uc29sZVBhbmVsKSkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBhd2FpdCB1cGRhdGVIYW5kbGVyQW5kQ29tbWFuZHMod2lkZ2V0KTtcbiAgICAgIH0pO1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnNvbGVUcmFja2VyLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QoYXN5bmMgKF8sIGNvbnNvbGVQYW5lbCkgPT4ge1xuICAgICAgaWYgKGNvbnNvbGVQYW5lbCkge1xuICAgICAgICB2b2lkIHVwZGF0ZUhhbmRsZXJBbmRDb21tYW5kcyhjb25zb2xlUGFuZWwpO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHRoYXQgcHJvdmlkZXMgdmlzdWFsIGRlYnVnZ2luZyBzdXBwb3J0IGZvciBmaWxlIGVkaXRvcnMuXG4gKi9cbmNvbnN0IGZpbGVzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZGVidWdnZXItZXh0ZW5zaW9uOmZpbGVzJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lEZWJ1Z2dlciwgSUVkaXRvclRyYWNrZXJdLFxuICBvcHRpb25hbDogW0lMYWJTaGVsbF0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZGVidWc6IElEZWJ1Z2dlcixcbiAgICBlZGl0b3JUcmFja2VyOiBJRWRpdG9yVHJhY2tlcixcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCBoYW5kbGVyID0gbmV3IERlYnVnZ2VyLkhhbmRsZXIoe1xuICAgICAgdHlwZTogJ2ZpbGUnLFxuICAgICAgc2hlbGw6IGFwcC5zaGVsbCxcbiAgICAgIHNlcnZpY2U6IGRlYnVnXG4gICAgfSk7XG5cbiAgICBjb25zdCBhY3RpdmVTZXNzaW9uczoge1xuICAgICAgW2lkOiBzdHJpbmddOiBTZXNzaW9uLklTZXNzaW9uQ29ubmVjdGlvbjtcbiAgICB9ID0ge307XG5cbiAgICBjb25zdCB1cGRhdGVIYW5kbGVyQW5kQ29tbWFuZHMgPSBhc3luYyAoXG4gICAgICB3aWRnZXQ6IERvY3VtZW50V2lkZ2V0XG4gICAgKTogUHJvbWlzZTx2b2lkPiA9PiB7XG4gICAgICBjb25zdCBzZXNzaW9ucyA9IGFwcC5zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucztcbiAgICAgIHRyeSB7XG4gICAgICAgIGNvbnN0IG1vZGVsID0gYXdhaXQgc2Vzc2lvbnMuZmluZEJ5UGF0aCh3aWRnZXQuY29udGV4dC5wYXRoKTtcbiAgICAgICAgaWYgKCFtb2RlbCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBsZXQgc2Vzc2lvbiA9IGFjdGl2ZVNlc3Npb25zW21vZGVsLmlkXTtcbiAgICAgICAgaWYgKCFzZXNzaW9uKSB7XG4gICAgICAgICAgLy8gVXNlIGBjb25uZWN0VG9gIG9ubHkgaWYgdGhlIHNlc3Npb24gZG9lcyBub3QgZXhpc3QuXG4gICAgICAgICAgLy8gYGNvbm5lY3RUb2Agc2VuZHMgYSBrZXJuZWxfaW5mb19yZXF1ZXN0IG9uIHRoZSBzaGVsbFxuICAgICAgICAgIC8vIGNoYW5uZWwsIHdoaWNoIGJsb2NrcyB0aGUgZGVidWcgc2Vzc2lvbiByZXN0b3JlIHdoZW4gd2FpdGluZ1xuICAgICAgICAgIC8vIGZvciB0aGUga2VybmVsIHRvIGJlIHJlYWR5XG4gICAgICAgICAgc2Vzc2lvbiA9IHNlc3Npb25zLmNvbm5lY3RUbyh7IG1vZGVsIH0pO1xuICAgICAgICAgIGFjdGl2ZVNlc3Npb25zW21vZGVsLmlkXSA9IHNlc3Npb247XG4gICAgICAgIH1cbiAgICAgICAgYXdhaXQgaGFuZGxlci51cGRhdGUod2lkZ2V0LCBzZXNzaW9uKTtcbiAgICAgICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKCk7XG4gICAgICB9IGNhdGNoIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgIH07XG5cbiAgICBpZiAobGFiU2hlbGwpIHtcbiAgICAgIGxhYlNoZWxsLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QoYXN5bmMgKF8sIHVwZGF0ZSkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB1cGRhdGUubmV3VmFsdWU7XG4gICAgICAgIGlmICghKHdpZGdldCBpbnN0YW5jZW9mIERvY3VtZW50V2lkZ2V0KSkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGNvbnRlbnQgPSB3aWRnZXQuY29udGVudDtcbiAgICAgICAgaWYgKCEoY29udGVudCBpbnN0YW5jZW9mIEZpbGVFZGl0b3IpKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGF3YWl0IHVwZGF0ZUhhbmRsZXJBbmRDb21tYW5kcyh3aWRnZXQpO1xuICAgICAgfSk7XG4gICAgfVxuXG4gICAgZWRpdG9yVHJhY2tlci5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KGFzeW5jIChfLCBkb2N1bWVudFdpZGdldCkgPT4ge1xuICAgICAgYXdhaXQgdXBkYXRlSGFuZGxlckFuZENvbW1hbmRzKFxuICAgICAgICAoZG9jdW1lbnRXaWRnZXQgYXMgdW5rbm93bikgYXMgRG9jdW1lbnRXaWRnZXRcbiAgICAgICk7XG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gdGhhdCBwcm92aWRlcyB2aXN1YWwgZGVidWdnaW5nIHN1cHBvcnQgZm9yIG5vdGVib29rcy5cbiAqL1xuY29uc3Qgbm90ZWJvb2tzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZGVidWdnZXItZXh0ZW5zaW9uOm5vdGVib29rcycsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJRGVidWdnZXIsIElOb3RlYm9va1RyYWNrZXIsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJTGFiU2hlbGwsIElDb21tYW5kUGFsZXR0ZV0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgc2VydmljZTogSURlYnVnZ2VyLFxuICAgIG5vdGVib29rVHJhY2tlcjogSU5vdGVib29rVHJhY2tlcixcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsIHwgbnVsbCxcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4gICkgPT4ge1xuICAgIGNvbnN0IGhhbmRsZXIgPSBuZXcgRGVidWdnZXIuSGFuZGxlcih7XG4gICAgICB0eXBlOiAnbm90ZWJvb2snLFxuICAgICAgc2hlbGw6IGFwcC5zaGVsbCxcbiAgICAgIHNlcnZpY2VcbiAgICB9KTtcblxuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoRGVidWdnZXIuQ29tbWFuZElEcy5yZXN0YXJ0RGVidWcsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnUmVzdGFydCBLZXJuZWwgYW5kIERlYnVn4oCmJyksXG4gICAgICBjYXB0aW9uOiB0cmFucy5fXygnUmVzdGFydCBLZXJuZWwgYW5kIERlYnVn4oCmJyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgcmV0dXJuIHNlcnZpY2UuaXNTdGFydGVkO1xuICAgICAgfSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgY29uc3Qgc3RhdGUgPSBzZXJ2aWNlLmdldERlYnVnZ2VyU3RhdGUoKTtcbiAgICAgICAgY29uc29sZS5sb2coc3RhdGUuY2VsbHMpO1xuICAgICAgICBjb25zdCB7IGNvbnRleHQsIGNvbnRlbnQgfSA9IG5vdGVib29rVHJhY2tlci5jdXJyZW50V2lkZ2V0ITtcblxuICAgICAgICBhd2FpdCBzZXJ2aWNlLnN0b3AoKTtcbiAgICAgICAgY29uc3QgcmVzdGFydGVkID0gYXdhaXQgc2Vzc2lvbkNvbnRleHREaWFsb2dzIS5yZXN0YXJ0KFxuICAgICAgICAgIGNvbnRleHQuc2Vzc2lvbkNvbnRleHRcbiAgICAgICAgKTtcbiAgICAgICAgaWYgKHJlc3RhcnRlZCkge1xuICAgICAgICAgIGF3YWl0IHNlcnZpY2UucmVzdG9yZURlYnVnZ2VyU3RhdGUoc3RhdGUpO1xuICAgICAgICAgIGF3YWl0IGhhbmRsZXIudXBkYXRlV2lkZ2V0KFxuICAgICAgICAgICAgbm90ZWJvb2tUcmFja2VyLmN1cnJlbnRXaWRnZXQhLFxuICAgICAgICAgICAgbm90ZWJvb2tUcmFja2VyLmN1cnJlbnRXaWRnZXQhLnNlc3Npb25Db250ZXh0LnNlc3Npb25cbiAgICAgICAgICApO1xuICAgICAgICAgIGF3YWl0IE5vdGVib29rQWN0aW9ucy5ydW5BbGwoY29udGVudCwgY29udGV4dC5zZXNzaW9uQ29udGV4dCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbnN0IHVwZGF0ZUhhbmRsZXJBbmRDb21tYW5kcyA9IGFzeW5jIChcbiAgICAgIHdpZGdldDogTm90ZWJvb2tQYW5lbFxuICAgICk6IFByb21pc2U8dm9pZD4gPT4ge1xuICAgICAgY29uc3QgeyBzZXNzaW9uQ29udGV4dCB9ID0gd2lkZ2V0O1xuICAgICAgYXdhaXQgc2Vzc2lvbkNvbnRleHQucmVhZHk7XG4gICAgICBhd2FpdCBoYW5kbGVyLnVwZGF0ZUNvbnRleHQod2lkZ2V0LCBzZXNzaW9uQ29udGV4dCk7XG4gICAgICBhcHAuY29tbWFuZHMubm90aWZ5Q29tbWFuZENoYW5nZWQoKTtcbiAgICB9O1xuXG4gICAgaWYgKGxhYlNoZWxsKSB7XG4gICAgICBsYWJTaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KGFzeW5jIChfLCB1cGRhdGUpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdXBkYXRlLm5ld1ZhbHVlO1xuICAgICAgICBpZiAoISh3aWRnZXQgaW5zdGFuY2VvZiBOb3RlYm9va1BhbmVsKSkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBhd2FpdCB1cGRhdGVIYW5kbGVyQW5kQ29tbWFuZHMod2lkZ2V0KTtcbiAgICAgIH0pO1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICBjYXRlZ29yeTogJ05vdGVib29rIE9wZXJhdGlvbnMnLFxuICAgICAgICBjb21tYW5kOiBEZWJ1Z2dlci5Db21tYW5kSURzLnJlc3RhcnREZWJ1Z1xuICAgICAgfSk7XG4gICAgfVxuXG4gICAgbm90ZWJvb2tUcmFja2VyLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QoXG4gICAgICBhc3luYyAoXywgbm90ZWJvb2tQYW5lbDogTm90ZWJvb2tQYW5lbCkgPT4ge1xuICAgICAgICBhd2FpdCB1cGRhdGVIYW5kbGVyQW5kQ29tbWFuZHMobm90ZWJvb2tQYW5lbCk7XG4gICAgICB9XG4gICAgKTtcbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0aGF0IHByb3ZpZGVzIGEgZGVidWdnZXIgc2VydmljZS5cbiAqL1xuY29uc3Qgc2VydmljZTogSnVweXRlckZyb250RW5kUGx1Z2luPElEZWJ1Z2dlcj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZGVidWdnZXItZXh0ZW5zaW9uOnNlcnZpY2UnLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJRGVidWdnZXIsXG4gIHJlcXVpcmVzOiBbSURlYnVnZ2VyQ29uZmlnXSxcbiAgb3B0aW9uYWw6IFtJRGVidWdnZXJTb3VyY2VzXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBjb25maWc6IElEZWJ1Z2dlci5JQ29uZmlnLFxuICAgIGRlYnVnZ2VyU291cmNlczogSURlYnVnZ2VyLklTb3VyY2VzIHwgbnVsbFxuICApID0+XG4gICAgbmV3IERlYnVnZ2VyLlNlcnZpY2Uoe1xuICAgICAgY29uZmlnLFxuICAgICAgZGVidWdnZXJTb3VyY2VzLFxuICAgICAgc3BlY3NNYW5hZ2VyOiBhcHAuc2VydmljZU1hbmFnZXIua2VybmVsc3BlY3NcbiAgICB9KVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0aGF0IHByb3ZpZGVzIGEgY29uZmlndXJhdGlvbiB3aXRoIGhhc2ggbWV0aG9kLlxuICovXG5jb25zdCBjb25maWd1cmF0aW9uOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SURlYnVnZ2VyLklDb25maWc+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2RlYnVnZ2VyLWV4dGVuc2lvbjpjb25maWcnLFxuICBwcm92aWRlczogSURlYnVnZ2VyQ29uZmlnLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoKSA9PiBuZXcgRGVidWdnZXIuQ29uZmlnKClcbn07XG5cbi8qKlxuICogQSBwbHVnaW4gdGhhdCBwcm92aWRlcyBzb3VyY2UvZWRpdG9yIGZ1bmN0aW9uYWxpdHkgZm9yIGRlYnVnZ2luZy5cbiAqL1xuY29uc3Qgc291cmNlczogSnVweXRlckZyb250RW5kUGx1Z2luPElEZWJ1Z2dlci5JU291cmNlcz4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZGVidWdnZXItZXh0ZW5zaW9uOnNvdXJjZXMnLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJRGVidWdnZXJTb3VyY2VzLFxuICByZXF1aXJlczogW0lEZWJ1Z2dlckNvbmZpZywgSUVkaXRvclNlcnZpY2VzXSxcbiAgb3B0aW9uYWw6IFtJTm90ZWJvb2tUcmFja2VyLCBJQ29uc29sZVRyYWNrZXIsIElFZGl0b3JUcmFja2VyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBjb25maWc6IElEZWJ1Z2dlci5JQ29uZmlnLFxuICAgIGVkaXRvclNlcnZpY2VzOiBJRWRpdG9yU2VydmljZXMsXG4gICAgbm90ZWJvb2tUcmFja2VyOiBJTm90ZWJvb2tUcmFja2VyIHwgbnVsbCxcbiAgICBjb25zb2xlVHJhY2tlcjogSUNvbnNvbGVUcmFja2VyIHwgbnVsbCxcbiAgICBlZGl0b3JUcmFja2VyOiBJRWRpdG9yVHJhY2tlciB8IG51bGxcbiAgKTogSURlYnVnZ2VyLklTb3VyY2VzID0+IHtcbiAgICByZXR1cm4gbmV3IERlYnVnZ2VyLlNvdXJjZXMoe1xuICAgICAgY29uZmlnLFxuICAgICAgc2hlbGw6IGFwcC5zaGVsbCxcbiAgICAgIGVkaXRvclNlcnZpY2VzLFxuICAgICAgbm90ZWJvb2tUcmFja2VyLFxuICAgICAgY29uc29sZVRyYWNrZXIsXG4gICAgICBlZGl0b3JUcmFja2VyXG4gICAgfSk7XG4gIH1cbn07XG4vKlxuICogQSBwbHVnaW4gdG8gb3BlbiBkZXRhaWxlZCB2aWV3cyBmb3IgdmFyaWFibGVzLlxuICovXG5jb25zdCB2YXJpYWJsZXM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kZWJ1Z2dlci1leHRlbnNpb246dmFyaWFibGVzJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lEZWJ1Z2dlciwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lUaGVtZU1hbmFnZXJdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHNlcnZpY2U6IElEZWJ1Z2dlcixcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICB0aGVtZU1hbmFnZXI6IElUaGVtZU1hbmFnZXIgfCBudWxsXG4gICkgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8RGVidWdnZXIuVmFyaWFibGVzR3JpZD4+KHtcbiAgICAgIG5hbWVzcGFjZTogJ2RlYnVnZ2VyL2luc3BlY3QtdmFyaWFibGUnXG4gICAgfSk7XG4gICAgY29uc3QgQ29tbWFuZElEcyA9IERlYnVnZ2VyLkNvbW1hbmRJRHM7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaW5zcGVjdFZhcmlhYmxlLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0luc3BlY3QgVmFyaWFibGUnKSxcbiAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdJbnNwZWN0IFZhcmlhYmxlJyksXG4gICAgICBleGVjdXRlOiBhc3luYyBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgeyB2YXJpYWJsZVJlZmVyZW5jZSB9ID0gYXJncztcbiAgICAgICAgaWYgKCF2YXJpYWJsZVJlZmVyZW5jZSB8fCB2YXJpYWJsZVJlZmVyZW5jZSA9PT0gMCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCB2YXJpYWJsZXMgPSBhd2FpdCBzZXJ2aWNlLmluc3BlY3RWYXJpYWJsZShcbiAgICAgICAgICB2YXJpYWJsZVJlZmVyZW5jZSBhcyBudW1iZXJcbiAgICAgICAgKTtcblxuICAgICAgICBjb25zdCB0aXRsZSA9IGFyZ3MudGl0bGUgYXMgc3RyaW5nO1xuICAgICAgICBjb25zdCBpZCA9IGBqcC1kZWJ1Z2dlci12YXJpYWJsZS0ke3RpdGxlfWA7XG4gICAgICAgIGlmIChcbiAgICAgICAgICAhdmFyaWFibGVzIHx8XG4gICAgICAgICAgdmFyaWFibGVzLmxlbmd0aCA9PT0gMCB8fFxuICAgICAgICAgIHRyYWNrZXIuZmluZCh3aWRnZXQgPT4gd2lkZ2V0LmlkID09PSBpZClcbiAgICAgICAgKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgbW9kZWwgPSBzZXJ2aWNlLm1vZGVsLnZhcmlhYmxlcztcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gbmV3IE1haW5BcmVhV2lkZ2V0PERlYnVnZ2VyLlZhcmlhYmxlc0dyaWQ+KHtcbiAgICAgICAgICBjb250ZW50OiBuZXcgRGVidWdnZXIuVmFyaWFibGVzR3JpZCh7XG4gICAgICAgICAgICBtb2RlbCxcbiAgICAgICAgICAgIGNvbW1hbmRzLFxuICAgICAgICAgICAgc2NvcGVzOiBbeyBuYW1lOiB0aXRsZSwgdmFyaWFibGVzIH1dLFxuICAgICAgICAgICAgdGhlbWVNYW5hZ2VyXG4gICAgICAgICAgfSlcbiAgICAgICAgfSk7XG4gICAgICAgIHdpZGdldC5hZGRDbGFzcygnanAtRGVidWdnZXJWYXJpYWJsZXMnKTtcbiAgICAgICAgd2lkZ2V0LmlkID0gaWQ7XG4gICAgICAgIHdpZGdldC50aXRsZS5pY29uID0gRGVidWdnZXIuSWNvbnMudmFyaWFibGVJY29uO1xuICAgICAgICB3aWRnZXQudGl0bGUubGFiZWwgPSBgJHtzZXJ2aWNlLnNlc3Npb24/LmNvbm5lY3Rpb24/Lm5hbWV9IC0gJHt0aXRsZX1gO1xuICAgICAgICB2b2lkIHRyYWNrZXIuYWRkKHdpZGdldCk7XG4gICAgICAgIG1vZGVsLmNoYW5nZWQuY29ubmVjdCgoKSA9PiB3aWRnZXQuZGlzcG9zZSgpKTtcbiAgICAgICAgc2hlbGwuYWRkKHdpZGdldCwgJ21haW4nLCB7XG4gICAgICAgICAgbW9kZTogdHJhY2tlci5jdXJyZW50V2lkZ2V0ID8gJ3NwbGl0LXJpZ2h0JyA6ICdzcGxpdC1ib3R0b20nXG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIERlYnVnZ2VyIHNpZGViYXIgcHJvdmlkZXIgcGx1Z2luLlxuICovXG5jb25zdCBzaWRlYmFyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SURlYnVnZ2VyLklTaWRlYmFyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kZWJ1Z2dlci1leHRlbnNpb246c2lkZWJhcicsXG4gIHByb3ZpZGVzOiBJRGVidWdnZXJTaWRlYmFyLFxuICByZXF1aXJlczogW0lEZWJ1Z2dlciwgSUVkaXRvclNlcnZpY2VzLCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSVRoZW1lTWFuYWdlciwgSVNldHRpbmdSZWdpc3RyeV0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IGFzeW5jIChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzZXJ2aWNlOiBJRGVidWdnZXIsXG4gICAgZWRpdG9yU2VydmljZXM6IElFZGl0b3JTZXJ2aWNlcyxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICB0aGVtZU1hbmFnZXI6IElUaGVtZU1hbmFnZXIgfCBudWxsLFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSB8IG51bGxcbiAgKTogUHJvbWlzZTxJRGVidWdnZXIuSVNpZGViYXI+ID0+IHtcbiAgICBjb25zdCB7IGNvbW1hbmRzIH0gPSBhcHA7XG4gICAgY29uc3QgQ29tbWFuZElEcyA9IERlYnVnZ2VyLkNvbW1hbmRJRHM7XG5cbiAgICBjb25zdCBjYWxsc3RhY2tDb21tYW5kcyA9IHtcbiAgICAgIHJlZ2lzdHJ5OiBjb21tYW5kcyxcbiAgICAgIGNvbnRpbnVlOiBDb21tYW5kSURzLmRlYnVnQ29udGludWUsXG4gICAgICB0ZXJtaW5hdGU6IENvbW1hbmRJRHMudGVybWluYXRlLFxuICAgICAgbmV4dDogQ29tbWFuZElEcy5uZXh0LFxuICAgICAgc3RlcEluOiBDb21tYW5kSURzLnN0ZXBJbixcbiAgICAgIHN0ZXBPdXQ6IENvbW1hbmRJRHMuc3RlcE91dCxcbiAgICAgIGV2YWx1YXRlOiBDb21tYW5kSURzLmV2YWx1YXRlXG4gICAgfTtcblxuICAgIGNvbnN0IHNpZGViYXIgPSBuZXcgRGVidWdnZXIuU2lkZWJhcih7XG4gICAgICBzZXJ2aWNlLFxuICAgICAgY2FsbHN0YWNrQ29tbWFuZHMsXG4gICAgICBlZGl0b3JTZXJ2aWNlcyxcbiAgICAgIHRoZW1lTWFuYWdlcixcbiAgICAgIHRyYW5zbGF0b3JcbiAgICB9KTtcblxuICAgIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICAgIGNvbnN0IHNldHRpbmcgPSBhd2FpdCBzZXR0aW5nUmVnaXN0cnkubG9hZChtYWluLmlkKTtcbiAgICAgIGNvbnN0IHVwZGF0ZVNldHRpbmdzID0gKCk6IHZvaWQgPT4ge1xuICAgICAgICBjb25zdCBmaWx0ZXJzID0gc2V0dGluZy5nZXQoJ3ZhcmlhYmxlRmlsdGVycycpLmNvbXBvc2l0ZSBhcyB7XG4gICAgICAgICAgW2tleTogc3RyaW5nXTogc3RyaW5nW107XG4gICAgICAgIH07XG4gICAgICAgIGNvbnN0IGtlcm5lbCA9IHNlcnZpY2Uuc2Vzc2lvbj8uY29ubmVjdGlvbj8ua2VybmVsPy5uYW1lID8/ICcnO1xuICAgICAgICBpZiAoa2VybmVsICYmIGZpbHRlcnNba2VybmVsXSkge1xuICAgICAgICAgIHNpZGViYXIudmFyaWFibGVzLmZpbHRlciA9IG5ldyBTZXQ8c3RyaW5nPihmaWx0ZXJzW2tlcm5lbF0pO1xuICAgICAgICB9XG4gICAgICB9O1xuICAgICAgdXBkYXRlU2V0dGluZ3MoKTtcbiAgICAgIHNldHRpbmcuY2hhbmdlZC5jb25uZWN0KHVwZGF0ZVNldHRpbmdzKTtcbiAgICAgIHNlcnZpY2Uuc2Vzc2lvbkNoYW5nZWQuY29ubmVjdCh1cGRhdGVTZXR0aW5ncyk7XG4gICAgfVxuXG4gICAgcmV0dXJuIHNpZGViYXI7XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIG1haW4gZGVidWdnZXIgVUkgcGx1Z2luLlxuICovXG5jb25zdCBtYWluOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZGVidWdnZXItZXh0ZW5zaW9uOm1haW4nLFxuICByZXF1aXJlczogW0lEZWJ1Z2dlciwgSURlYnVnZ2VyU2lkZWJhciwgSUVkaXRvclNlcnZpY2VzLCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbXG4gICAgSUNvbW1hbmRQYWxldHRlLFxuICAgIElEZWJ1Z2dlclNvdXJjZXMsXG4gICAgSUxhYlNoZWxsLFxuICAgIElMYXlvdXRSZXN0b3JlcixcbiAgICBJTG9nZ2VyUmVnaXN0cnlcbiAgXSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHNlcnZpY2U6IElEZWJ1Z2dlcixcbiAgICBzaWRlYmFyOiBJRGVidWdnZXIuSVNpZGViYXIsXG4gICAgZWRpdG9yU2VydmljZXM6IElFZGl0b3JTZXJ2aWNlcyxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsLFxuICAgIGRlYnVnZ2VyU291cmNlczogSURlYnVnZ2VyLklTb3VyY2VzIHwgbnVsbCxcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsIHwgbnVsbCxcbiAgICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbCxcbiAgICBsb2dnZXJSZWdpc3RyeTogSUxvZ2dlclJlZ2lzdHJ5IHwgbnVsbFxuICApOiBQcm9taXNlPHZvaWQ+ID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsLCBzZXJ2aWNlTWFuYWdlciB9ID0gYXBwO1xuICAgIGNvbnN0IHsga2VybmVsc3BlY3MgfSA9IHNlcnZpY2VNYW5hZ2VyO1xuICAgIGNvbnN0IENvbW1hbmRJRHMgPSBEZWJ1Z2dlci5Db21tYW5kSURzO1xuXG4gICAgLy8gRmlyc3QgY2hlY2sgaWYgdGhlcmUgaXMgYSBQYWdlQ29uZmlnIG92ZXJyaWRlIGZvciB0aGUgZXh0ZW5zaW9uIHZpc2liaWxpdHlcbiAgICBjb25zdCBhbHdheXNTaG93RGVidWdnZXJFeHRlbnNpb24gPVxuICAgICAgUGFnZUNvbmZpZy5nZXRPcHRpb24oJ2Fsd2F5c1Nob3dEZWJ1Z2dlckV4dGVuc2lvbicpLnRvTG93ZXJDYXNlKCkgPT09XG4gICAgICAndHJ1ZSc7XG4gICAgaWYgKCFhbHdheXNTaG93RGVidWdnZXJFeHRlbnNpb24pIHtcbiAgICAgIC8vIGhpZGUgdGhlIGRlYnVnZ2VyIHNpZGViYXIgaWYgbm8ga2VybmVsIHdpdGggc3VwcG9ydCBmb3IgZGVidWdnaW5nIGlzIGF2YWlsYWJsZVxuICAgICAgYXdhaXQga2VybmVsc3BlY3MucmVhZHk7XG4gICAgICBjb25zdCBzcGVjcyA9IGtlcm5lbHNwZWNzLnNwZWNzPy5rZXJuZWxzcGVjcztcbiAgICAgIGlmICghc3BlY3MpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgZW5hYmxlZCA9IE9iamVjdC5rZXlzKHNwZWNzKS5zb21lKFxuICAgICAgICBuYW1lID0+ICEhKHNwZWNzW25hbWVdPy5tZXRhZGF0YT8uWydkZWJ1Z2dlciddID8/IGZhbHNlKVxuICAgICAgKTtcbiAgICAgIGlmICghZW5hYmxlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgfVxuXG4gICAgLy8gZ2V0IHRoZSBtaW1lIHR5cGUgb2YgdGhlIGtlcm5lbCBsYW5ndWFnZSBmb3IgdGhlIGN1cnJlbnQgZGVidWcgc2Vzc2lvblxuICAgIGNvbnN0IGdldE1pbWVUeXBlID0gYXN5bmMgKCk6IFByb21pc2U8c3RyaW5nPiA9PiB7XG4gICAgICBjb25zdCBrZXJuZWwgPSBzZXJ2aWNlLnNlc3Npb24/LmNvbm5lY3Rpb24/Lmtlcm5lbDtcbiAgICAgIGlmICgha2VybmVsKSB7XG4gICAgICAgIHJldHVybiAnJztcbiAgICAgIH1cbiAgICAgIGNvbnN0IGluZm8gPSAoYXdhaXQga2VybmVsLmluZm8pLmxhbmd1YWdlX2luZm87XG4gICAgICBjb25zdCBuYW1lID0gaW5mby5uYW1lO1xuICAgICAgY29uc3QgbWltZVR5cGUgPVxuICAgICAgICBlZGl0b3JTZXJ2aWNlcz8ubWltZVR5cGVTZXJ2aWNlLmdldE1pbWVUeXBlQnlMYW5ndWFnZSh7IG5hbWUgfSkgPz8gJyc7XG4gICAgICByZXR1cm4gbWltZVR5cGU7XG4gICAgfTtcblxuICAgIGNvbnN0IHJlbmRlcm1pbWUgPSBuZXcgUmVuZGVyTWltZVJlZ2lzdHJ5KHsgaW5pdGlhbEZhY3RvcmllcyB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5ldmFsdWF0ZSwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdFdmFsdWF0ZSBDb2RlJyksXG4gICAgICBjYXB0aW9uOiB0cmFucy5fXygnRXZhbHVhdGUgQ29kZScpLFxuICAgICAgaWNvbjogRGVidWdnZXIuSWNvbnMuZXZhbHVhdGVJY29uLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiB7XG4gICAgICAgIHJldHVybiBzZXJ2aWNlLmhhc1N0b3BwZWRUaHJlYWRzKCk7XG4gICAgICB9LFxuICAgICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgICBjb25zdCBtaW1lVHlwZSA9IGF3YWl0IGdldE1pbWVUeXBlKCk7XG4gICAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IERlYnVnZ2VyLkRpYWxvZ3MuZ2V0Q29kZSh7XG4gICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdFdmFsdWF0ZSBDb2RlJyksXG4gICAgICAgICAgb2tMYWJlbDogdHJhbnMuX18oJ0V2YWx1YXRlJyksXG4gICAgICAgICAgY2FuY2VsTGFiZWw6IHRyYW5zLl9fKCdDYW5jZWwnKSxcbiAgICAgICAgICBtaW1lVHlwZSxcbiAgICAgICAgICByZW5kZXJtaW1lXG4gICAgICAgIH0pO1xuICAgICAgICBjb25zdCBjb2RlID0gcmVzdWx0LnZhbHVlO1xuICAgICAgICBpZiAoIXJlc3VsdC5idXR0b24uYWNjZXB0IHx8ICFjb2RlKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IHJlcGx5ID0gYXdhaXQgc2VydmljZS5ldmFsdWF0ZShjb2RlKTtcbiAgICAgICAgaWYgKHJlcGx5KSB7XG4gICAgICAgICAgY29uc3QgZGF0YSA9IHJlcGx5LnJlc3VsdDtcbiAgICAgICAgICBjb25zdCBwYXRoID0gc2VydmljZT8uc2Vzc2lvbj8uY29ubmVjdGlvbj8ucGF0aDtcbiAgICAgICAgICBjb25zdCBsb2dnZXIgPSBwYXRoID8gbG9nZ2VyUmVnaXN0cnk/LmdldExvZ2dlcj8uKHBhdGgpIDogdW5kZWZpbmVkO1xuXG4gICAgICAgICAgaWYgKGxvZ2dlcikge1xuICAgICAgICAgICAgLy8gcHJpbnQgdG8gbG9nIGNvbnNvbGUgb2YgdGhlIG5vdGVib29rIGN1cnJlbnRseSBiZWluZyBkZWJ1Z2dlZFxuICAgICAgICAgICAgbG9nZ2VyLmxvZyh7IHR5cGU6ICd0ZXh0JywgZGF0YSwgbGV2ZWw6IGxvZ2dlci5sZXZlbCB9KTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgLy8gZmFsbGJhY2sgdG8gcHJpbnRpbmcgdG8gZGV2dG9vbHMgY29uc29sZVxuICAgICAgICAgICAgY29uc29sZS5kZWJ1ZyhkYXRhKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5kZWJ1Z0NvbnRpbnVlLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0NvbnRpbnVlJyksXG4gICAgICBjYXB0aW9uOiB0cmFucy5fXygnQ29udGludWUnKSxcbiAgICAgIGljb246IERlYnVnZ2VyLkljb25zLmNvbnRpbnVlSWNvbixcbiAgICAgIGlzRW5hYmxlZDogKCkgPT4ge1xuICAgICAgICByZXR1cm4gc2VydmljZS5oYXNTdG9wcGVkVGhyZWFkcygpO1xuICAgICAgfSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgYXdhaXQgc2VydmljZS5jb250aW51ZSgpO1xuICAgICAgICBjb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZCgpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRlcm1pbmF0ZSwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdUZXJtaW5hdGUnKSxcbiAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdUZXJtaW5hdGUnKSxcbiAgICAgIGljb246IERlYnVnZ2VyLkljb25zLnRlcm1pbmF0ZUljb24sXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgcmV0dXJuIHNlcnZpY2UuaGFzU3RvcHBlZFRocmVhZHMoKTtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGF3YWl0IHNlcnZpY2UucmVzdGFydCgpO1xuICAgICAgICBjb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZCgpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm5leHQsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnTmV4dCcpLFxuICAgICAgY2FwdGlvbjogdHJhbnMuX18oJ05leHQnKSxcbiAgICAgIGljb246IERlYnVnZ2VyLkljb25zLnN0ZXBPdmVySWNvbixcbiAgICAgIGlzRW5hYmxlZDogKCkgPT4ge1xuICAgICAgICByZXR1cm4gc2VydmljZS5oYXNTdG9wcGVkVGhyZWFkcygpO1xuICAgICAgfSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgYXdhaXQgc2VydmljZS5uZXh0KCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc3RlcEluLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1N0ZXAgSW4nKSxcbiAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdTdGVwIEluJyksXG4gICAgICBpY29uOiBEZWJ1Z2dlci5JY29ucy5zdGVwSW50b0ljb24sXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgcmV0dXJuIHNlcnZpY2UuaGFzU3RvcHBlZFRocmVhZHMoKTtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGF3YWl0IHNlcnZpY2Uuc3RlcEluKCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc3RlcE91dCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdTdGVwIE91dCcpLFxuICAgICAgY2FwdGlvbjogdHJhbnMuX18oJ1N0ZXAgT3V0JyksXG4gICAgICBpY29uOiBEZWJ1Z2dlci5JY29ucy5zdGVwT3V0SWNvbixcbiAgICAgIGlzRW5hYmxlZDogKCkgPT4ge1xuICAgICAgICByZXR1cm4gc2VydmljZS5oYXNTdG9wcGVkVGhyZWFkcygpO1xuICAgICAgfSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgYXdhaXQgc2VydmljZS5zdGVwT3V0KCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBzZXJ2aWNlLmV2ZW50TWVzc2FnZS5jb25uZWN0KChfLCBldmVudCk6IHZvaWQgPT4ge1xuICAgICAgY29tbWFuZHMubm90aWZ5Q29tbWFuZENoYW5nZWQoKTtcbiAgICAgIGlmIChsYWJTaGVsbCAmJiBldmVudC5ldmVudCA9PT0gJ2luaXRpYWxpemVkJykge1xuICAgICAgICBsYWJTaGVsbC5hY3RpdmF0ZUJ5SWQoc2lkZWJhci5pZCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBzZXJ2aWNlLnNlc3Npb25DaGFuZ2VkLmNvbm5lY3QoXyA9PiB7XG4gICAgICBjb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZCgpO1xuICAgIH0pO1xuXG4gICAgaWYgKHJlc3RvcmVyKSB7XG4gICAgICByZXN0b3Jlci5hZGQoc2lkZWJhciwgJ2RlYnVnZ2VyLXNpZGViYXInKTtcbiAgICB9XG5cbiAgICBzaWRlYmFyLm5vZGUuc2V0QXR0cmlidXRlKCdyb2xlJywgJ3JlZ2lvbicpO1xuICAgIHNpZGViYXIubm9kZS5zZXRBdHRyaWJ1dGUoJ2FyaWEtbGFiZWwnLCB0cmFucy5fXygnRGVidWdnZXIgc2VjdGlvbicpKTtcblxuICAgIHNoZWxsLmFkZChzaWRlYmFyLCAncmlnaHQnKTtcblxuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdEZWJ1Z2dlcicpO1xuICAgICAgW1xuICAgICAgICBDb21tYW5kSURzLmRlYnVnQ29udGludWUsXG4gICAgICAgIENvbW1hbmRJRHMudGVybWluYXRlLFxuICAgICAgICBDb21tYW5kSURzLm5leHQsXG4gICAgICAgIENvbW1hbmRJRHMuc3RlcEluLFxuICAgICAgICBDb21tYW5kSURzLnN0ZXBPdXQsXG4gICAgICAgIENvbW1hbmRJRHMuZXZhbHVhdGVcbiAgICAgIF0uZm9yRWFjaChjb21tYW5kID0+IHtcbiAgICAgICAgcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZCwgY2F0ZWdvcnkgfSk7XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBpZiAoZGVidWdnZXJTb3VyY2VzKSB7XG4gICAgICBjb25zdCB7IG1vZGVsIH0gPSBzZXJ2aWNlO1xuICAgICAgY29uc3QgcmVhZE9ubHlFZGl0b3JGYWN0b3J5ID0gbmV3IERlYnVnZ2VyLlJlYWRPbmx5RWRpdG9yRmFjdG9yeSh7XG4gICAgICAgIGVkaXRvclNlcnZpY2VzXG4gICAgICB9KTtcblxuICAgICAgY29uc3Qgb25DdXJyZW50RnJhbWVDaGFuZ2VkID0gKFxuICAgICAgICBfOiBJRGVidWdnZXIuTW9kZWwuSUNhbGxzdGFjayxcbiAgICAgICAgZnJhbWU6IElEZWJ1Z2dlci5JU3RhY2tGcmFtZVxuICAgICAgKTogdm9pZCA9PiB7XG4gICAgICAgIGRlYnVnZ2VyU291cmNlc1xuICAgICAgICAgIC5maW5kKHtcbiAgICAgICAgICAgIGZvY3VzOiB0cnVlLFxuICAgICAgICAgICAga2VybmVsOiBzZXJ2aWNlLnNlc3Npb24/LmNvbm5lY3Rpb24/Lmtlcm5lbD8ubmFtZSA/PyAnJyxcbiAgICAgICAgICAgIHBhdGg6IHNlcnZpY2Uuc2Vzc2lvbj8uY29ubmVjdGlvbj8ucGF0aCA/PyAnJyxcbiAgICAgICAgICAgIHNvdXJjZTogZnJhbWU/LnNvdXJjZT8ucGF0aCA/PyAnJ1xuICAgICAgICAgIH0pXG4gICAgICAgICAgLmZvckVhY2goZWRpdG9yID0+IHtcbiAgICAgICAgICAgIHJlcXVlc3RBbmltYXRpb25GcmFtZSgoKSA9PiB7XG4gICAgICAgICAgICAgIERlYnVnZ2VyLkVkaXRvckhhbmRsZXIuc2hvd0N1cnJlbnRMaW5lKGVkaXRvciwgZnJhbWUubGluZSk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9KTtcbiAgICAgIH07XG5cbiAgICAgIGNvbnN0IG9uQ3VycmVudFNvdXJjZU9wZW5lZCA9IChcbiAgICAgICAgXzogSURlYnVnZ2VyLk1vZGVsLklTb3VyY2VzIHwgbnVsbCxcbiAgICAgICAgc291cmNlOiBJRGVidWdnZXIuU291cmNlLFxuICAgICAgICBicmVha3BvaW50PzogSURlYnVnZ2VyLklCcmVha3BvaW50XG4gICAgICApOiB2b2lkID0+IHtcbiAgICAgICAgaWYgKCFzb3VyY2UpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgeyBjb250ZW50LCBtaW1lVHlwZSwgcGF0aCB9ID0gc291cmNlO1xuICAgICAgICBjb25zdCByZXN1bHRzID0gZGVidWdnZXJTb3VyY2VzLmZpbmQoe1xuICAgICAgICAgIGZvY3VzOiB0cnVlLFxuICAgICAgICAgIGtlcm5lbDogc2VydmljZS5zZXNzaW9uPy5jb25uZWN0aW9uPy5rZXJuZWw/Lm5hbWUgPz8gJycsXG4gICAgICAgICAgcGF0aDogc2VydmljZS5zZXNzaW9uPy5jb25uZWN0aW9uPy5wYXRoID8/ICcnLFxuICAgICAgICAgIHNvdXJjZTogcGF0aFxuICAgICAgICB9KTtcbiAgICAgICAgaWYgKHJlc3VsdHMubGVuZ3RoID4gMCkge1xuICAgICAgICAgIGlmIChicmVha3BvaW50ICYmIHR5cGVvZiBicmVha3BvaW50LmxpbmUgIT09ICd1bmRlZmluZWQnKSB7XG4gICAgICAgICAgICByZXN1bHRzLmZvckVhY2goZWRpdG9yID0+IHtcbiAgICAgICAgICAgICAgaWYgKGVkaXRvciBpbnN0YW5jZW9mIENvZGVNaXJyb3JFZGl0b3IpIHtcbiAgICAgICAgICAgICAgICAoZWRpdG9yIGFzIENvZGVNaXJyb3JFZGl0b3IpLnNjcm9sbEludG9WaWV3Q2VudGVyZWQoe1xuICAgICAgICAgICAgICAgICAgbGluZTogKGJyZWFrcG9pbnQubGluZSBhcyBudW1iZXIpIC0gMSxcbiAgICAgICAgICAgICAgICAgIGNoOiBicmVha3BvaW50LmNvbHVtbiB8fCAwXG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgZWRpdG9yLnJldmVhbFBvc2l0aW9uKHtcbiAgICAgICAgICAgICAgICAgIGxpbmU6IChicmVha3BvaW50LmxpbmUgYXMgbnVtYmVyKSAtIDEsXG4gICAgICAgICAgICAgICAgICBjb2x1bW46IGJyZWFrcG9pbnQuY29sdW1uIHx8IDBcbiAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfVxuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBlZGl0b3JXcmFwcGVyID0gcmVhZE9ubHlFZGl0b3JGYWN0b3J5LmNyZWF0ZU5ld0VkaXRvcih7XG4gICAgICAgICAgY29udGVudCxcbiAgICAgICAgICBtaW1lVHlwZSxcbiAgICAgICAgICBwYXRoXG4gICAgICAgIH0pO1xuICAgICAgICBjb25zdCBlZGl0b3IgPSBlZGl0b3JXcmFwcGVyLmVkaXRvcjtcbiAgICAgICAgY29uc3QgZWRpdG9ySGFuZGxlciA9IG5ldyBEZWJ1Z2dlci5FZGl0b3JIYW5kbGVyKHtcbiAgICAgICAgICBkZWJ1Z2dlclNlcnZpY2U6IHNlcnZpY2UsXG4gICAgICAgICAgZWRpdG9yLFxuICAgICAgICAgIHBhdGhcbiAgICAgICAgfSk7XG4gICAgICAgIGVkaXRvcldyYXBwZXIuZGlzcG9zZWQuY29ubmVjdCgoKSA9PiBlZGl0b3JIYW5kbGVyLmRpc3Bvc2UoKSk7XG5cbiAgICAgICAgZGVidWdnZXJTb3VyY2VzLm9wZW4oe1xuICAgICAgICAgIGxhYmVsOiBQYXRoRXh0LmJhc2VuYW1lKHBhdGgpLFxuICAgICAgICAgIGNhcHRpb246IHBhdGgsXG4gICAgICAgICAgZWRpdG9yV3JhcHBlclxuICAgICAgICB9KTtcblxuICAgICAgICBjb25zdCBmcmFtZSA9IHNlcnZpY2UubW9kZWwuY2FsbHN0YWNrLmZyYW1lO1xuICAgICAgICBpZiAoZnJhbWUpIHtcbiAgICAgICAgICBEZWJ1Z2dlci5FZGl0b3JIYW5kbGVyLnNob3dDdXJyZW50TGluZShlZGl0b3IsIGZyYW1lLmxpbmUpO1xuICAgICAgICB9XG4gICAgICB9O1xuXG4gICAgICBtb2RlbC5jYWxsc3RhY2suY3VycmVudEZyYW1lQ2hhbmdlZC5jb25uZWN0KG9uQ3VycmVudEZyYW1lQ2hhbmdlZCk7XG4gICAgICBtb2RlbC5zb3VyY2VzLmN1cnJlbnRTb3VyY2VPcGVuZWQuY29ubmVjdChvbkN1cnJlbnRTb3VyY2VPcGVuZWQpO1xuICAgICAgbW9kZWwuYnJlYWtwb2ludHMuY2xpY2tlZC5jb25uZWN0KGFzeW5jIChfLCBicmVha3BvaW50KSA9PiB7XG4gICAgICAgIGNvbnN0IHBhdGggPSBicmVha3BvaW50LnNvdXJjZT8ucGF0aDtcbiAgICAgICAgY29uc3Qgc291cmNlID0gYXdhaXQgc2VydmljZS5nZXRTb3VyY2Uoe1xuICAgICAgICAgIHNvdXJjZVJlZmVyZW5jZTogMCxcbiAgICAgICAgICBwYXRoXG4gICAgICAgIH0pO1xuICAgICAgICBvbkN1cnJlbnRTb3VyY2VPcGVuZWQobnVsbCwgc291cmNlLCBicmVha3BvaW50KTtcbiAgICAgIH0pO1xuICAgIH1cbiAgfVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbnMgYXMgZGVmYXVsdC5cbiAqL1xuY29uc3QgcGx1Z2luczogSnVweXRlckZyb250RW5kUGx1Z2luPGFueT5bXSA9IFtcbiAgc2VydmljZSxcbiAgY29uc29sZXMsXG4gIGZpbGVzLFxuICBub3RlYm9va3MsXG4gIHZhcmlhYmxlcyxcbiAgc2lkZWJhcixcbiAgbWFpbixcbiAgc291cmNlcyxcbiAgY29uZmlndXJhdGlvblxuXTtcblxuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcbiJdLCJzb3VyY2VSb290IjoiIn0=