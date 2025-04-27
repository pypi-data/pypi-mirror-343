(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_console-extension_lib_index_js"],{

/***/ "../packages/console-extension/lib/foreign.js":
/*!****************************************************!*\
  !*** ../packages/console-extension/lib/foreign.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "foreign": () => (/* binding */ foreign),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The console widget tracker provider.
 */
const foreign = {
    id: '@jupyterlab/console-extension:foreign',
    requires: [_jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__.IConsoleTracker, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: activateForeign,
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (foreign);
function activateForeign(app, tracker, settingRegistry, translator, palette) {
    const trans = translator.load('jupyterlab');
    const { shell } = app;
    tracker.widgetAdded.connect((sender, widget) => {
        const console = widget.console;
        const handler = new _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__.ForeignHandler({
            sessionContext: console.sessionContext,
            parent: console
        });
        Private.foreignHandlerProperty.set(console, handler);
        // Property showAllKernelActivity configures foreign handler enabled on start.
        void settingRegistry
            .get('@jupyterlab/console-extension:tracker', 'showAllKernelActivity')
            .then(({ composite }) => {
            const showAllKernelActivity = composite;
            handler.enabled = showAllKernelActivity;
        });
        console.disposed.connect(() => {
            handler.dispose();
        });
    });
    const { commands } = app;
    const category = trans.__('Console');
    const toggleShowAllActivity = 'console:toggle-show-all-kernel-activity';
    // Get the current widget and activate unless the args specify otherwise.
    function getCurrent(args) {
        const widget = tracker.currentWidget;
        const activate = args['activate'] !== false;
        if (activate && widget) {
            shell.activateById(widget.id);
        }
        return widget;
    }
    commands.addCommand(toggleShowAllActivity, {
        label: args => trans.__('Show All Kernel Activity'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            const handler = Private.foreignHandlerProperty.get(current.console);
            if (handler) {
                handler.enabled = !handler.enabled;
            }
        },
        isToggled: () => {
            var _a;
            return tracker.currentWidget !== null &&
                !!((_a = Private.foreignHandlerProperty.get(tracker.currentWidget.console)) === null || _a === void 0 ? void 0 : _a.enabled);
        },
        isEnabled: () => tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget
    });
    if (palette) {
        palette.addItem({
            command: toggleShowAllActivity,
            category,
            args: { isPalette: true }
        });
    }
}
/*
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property for a console's foreign handler.
     */
    Private.foreignHandlerProperty = new _lumino_properties__WEBPACK_IMPORTED_MODULE_4__.AttachedProperty({
        name: 'foreignHandler',
        create: () => undefined
    });
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/console-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../packages/console-extension/lib/index.js ***!
  \**************************************************/
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
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _foreign__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./foreign */ "../packages/console-extension/lib/foreign.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module console-extension
 */















/**
 * The command IDs used by the console plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.autoClosingBrackets = 'console:toggle-autoclosing-brackets';
    CommandIDs.create = 'console:create';
    CommandIDs.clear = 'console:clear';
    CommandIDs.runUnforced = 'console:run-unforced';
    CommandIDs.runForced = 'console:run-forced';
    CommandIDs.linebreak = 'console:linebreak';
    CommandIDs.interrupt = 'console:interrupt-kernel';
    CommandIDs.restart = 'console:restart-kernel';
    CommandIDs.closeAndShutdown = 'console:close-and-shutdown';
    CommandIDs.open = 'console:open';
    CommandIDs.inject = 'console:inject';
    CommandIDs.changeKernel = 'console:change-kernel';
    CommandIDs.enterToExecute = 'console:enter-to-execute';
    CommandIDs.shiftEnterToExecute = 'console:shift-enter-to-execute';
    CommandIDs.interactionMode = 'console:interaction-mode';
    CommandIDs.replaceSelection = 'console:replace-selection';
})(CommandIDs || (CommandIDs = {}));
/**
 * The console widget tracker provider.
 */
const tracker = {
    id: '@jupyterlab/console-extension:tracker',
    provides: _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__.IConsoleTracker,
    requires: [
        _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__.ConsolePanel.IContentFactory,
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_7__.IRenderMimeRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__.ISettingRegistry,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_9__.ITranslator
    ],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__.IMainMenu,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_5__.ILauncher,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs
    ],
    activate: activateConsole,
    autoStart: true
};
/**
 * The console widget content factory.
 */
const factory = {
    id: '@jupyterlab/console-extension:factory',
    provides: _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__.ConsolePanel.IContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__.ConsolePanel.ContentFactory({ editorFactory });
    }
};
/**
 * Export the plugins as the default.
 */
const plugins = [factory, tracker, _foreign__WEBPACK_IMPORTED_MODULE_14__.default];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * Activate the console extension.
 */
async function activateConsole(app, contentFactory, editorServices, rendermime, settingRegistry, translator, restorer, browserFactory, mainMenu, palette, launcher, status, sessionDialogs) {
    const trans = translator.load('jupyterlab');
    const manager = app.serviceManager;
    const { commands, shell } = app;
    const category = trans.__('Console');
    sessionDialogs = sessionDialogs !== null && sessionDialogs !== void 0 ? sessionDialogs : _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.sessionContextDialogs;
    // Create a widget tracker for all console panels.
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'console'
    });
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.create,
            args: widget => {
                const { path, name, kernelPreference } = widget.console.sessionContext;
                return {
                    path,
                    name,
                    kernelPreference: Object.assign({}, kernelPreference)
                };
            },
            name: widget => { var _a; return (_a = widget.console.sessionContext.path) !== null && _a !== void 0 ? _a : _lumino_coreutils__WEBPACK_IMPORTED_MODULE_12__.UUID.uuid4(); },
            when: manager.ready
        });
    }
    // Add a launcher item if the launcher is available.
    if (launcher) {
        void manager.ready.then(() => {
            let disposables = null;
            const onSpecsChanged = () => {
                if (disposables) {
                    disposables.dispose();
                    disposables = null;
                }
                const specs = manager.kernelspecs.specs;
                if (!specs) {
                    return;
                }
                disposables = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_13__.DisposableSet();
                for (const name in specs.kernelspecs) {
                    const rank = name === specs.default ? 0 : Infinity;
                    const spec = specs.kernelspecs[name];
                    let kernelIconUrl = spec.resources['logo-64x64'];
                    disposables.add(launcher.add({
                        command: CommandIDs.create,
                        args: { isLauncher: true, kernelPreference: { name } },
                        category: trans.__('Console'),
                        rank,
                        kernelIconUrl,
                        metadata: {
                            kernel: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_12__.JSONExt.deepCopy(spec.metadata || {})
                        }
                    }));
                }
            };
            onSpecsChanged();
            manager.kernelspecs.specsChanged.connect(onSpecsChanged);
        });
    }
    /**
     * Create a console for a given path.
     */
    async function createConsole(options) {
        var _a;
        await manager.ready;
        const panel = new _jupyterlab_console__WEBPACK_IMPORTED_MODULE_3__.ConsolePanel(Object.assign({ manager,
            contentFactory, mimeTypeService: editorServices.mimeTypeService, rendermime,
            translator, setBusy: (_a = (status && (() => status.setBusy()))) !== null && _a !== void 0 ? _a : undefined }, options));
        const interactionMode = (await settingRegistry.get('@jupyterlab/console-extension:tracker', 'interactionMode')).composite;
        panel.console.node.dataset.jpInteractionMode = interactionMode;
        // Add the console panel to the tracker. We want the panel to show up before
        // any kernel selection dialog, so we do not await panel.session.ready;
        await tracker.add(panel);
        panel.sessionContext.propertyChanged.connect(() => {
            void tracker.save(panel);
        });
        shell.add(panel, 'main', {
            ref: options.ref,
            mode: options.insertMode,
            activate: options.activate !== false
        });
        return panel;
    }
    const mapOption = (editor, config, option) => {
        if (config[option] === undefined) {
            return;
        }
        switch (option) {
            case 'autoClosingBrackets':
                editor.setOption('autoClosingBrackets', config['autoClosingBrackets']);
                break;
            case 'cursorBlinkRate':
                editor.setOption('cursorBlinkRate', config['cursorBlinkRate']);
                break;
            case 'fontFamily':
                editor.setOption('fontFamily', config['fontFamily']);
                break;
            case 'fontSize':
                editor.setOption('fontSize', config['fontSize']);
                break;
            case 'lineHeight':
                editor.setOption('lineHeight', config['lineHeight']);
                break;
            case 'lineNumbers':
                editor.setOption('lineNumbers', config['lineNumbers']);
                break;
            case 'lineWrap':
                editor.setOption('lineWrap', config['lineWrap']);
                break;
            case 'matchBrackets':
                editor.setOption('matchBrackets', config['matchBrackets']);
                break;
            case 'readOnly':
                editor.setOption('readOnly', config['readOnly']);
                break;
            case 'insertSpaces':
                editor.setOption('insertSpaces', config['insertSpaces']);
                break;
            case 'tabSize':
                editor.setOption('tabSize', config['tabSize']);
                break;
            case 'wordWrapColumn':
                editor.setOption('wordWrapColumn', config['wordWrapColumn']);
                break;
            case 'rulers':
                editor.setOption('rulers', config['rulers']);
                break;
            case 'codeFolding':
                editor.setOption('codeFolding', config['codeFolding']);
                break;
        }
    };
    const setOption = (editor, config) => {
        if (editor === undefined) {
            return;
        }
        mapOption(editor, config, 'autoClosingBrackets');
        mapOption(editor, config, 'cursorBlinkRate');
        mapOption(editor, config, 'fontFamily');
        mapOption(editor, config, 'fontSize');
        mapOption(editor, config, 'lineHeight');
        mapOption(editor, config, 'lineNumbers');
        mapOption(editor, config, 'lineWrap');
        mapOption(editor, config, 'matchBrackets');
        mapOption(editor, config, 'readOnly');
        mapOption(editor, config, 'insertSpaces');
        mapOption(editor, config, 'tabSize');
        mapOption(editor, config, 'wordWrapColumn');
        mapOption(editor, config, 'rulers');
        mapOption(editor, config, 'codeFolding');
    };
    const pluginId = '@jupyterlab/console-extension:tracker';
    let interactionMode;
    let promptCellConfig;
    /**
     * Update settings for one console or all consoles.
     *
     * @param panel Optional - single console to update.
     */
    async function updateSettings(panel) {
        interactionMode = (await settingRegistry.get(pluginId, 'interactionMode'))
            .composite;
        promptCellConfig = (await settingRegistry.get(pluginId, 'promptCellConfig'))
            .composite;
        const setWidgetOptions = (widget) => {
            var _a;
            widget.console.node.dataset.jpInteractionMode = interactionMode;
            setOption((_a = widget.console.promptCell) === null || _a === void 0 ? void 0 : _a.editor, promptCellConfig);
        };
        if (panel) {
            setWidgetOptions(panel);
        }
        else {
            tracker.forEach(setWidgetOptions);
        }
    }
    settingRegistry.pluginChanged.connect((sender, plugin) => {
        if (plugin === pluginId) {
            void updateSettings();
        }
    });
    await updateSettings();
    // Apply settings when a console is created.
    tracker.widgetAdded.connect((sender, panel) => {
        void updateSettings(panel);
    });
    commands.addCommand(CommandIDs.autoClosingBrackets, {
        execute: async (args) => {
            var _a;
            promptCellConfig.autoClosingBrackets = !!((_a = args['force']) !== null && _a !== void 0 ? _a : !promptCellConfig.autoClosingBrackets);
            await settingRegistry.set(pluginId, 'promptCellConfig', promptCellConfig);
        },
        label: trans.__('Auto Close Brackets for Code Console Prompt'),
        isToggled: () => promptCellConfig.autoClosingBrackets
    });
    /**
     * Whether there is an active console.
     */
    function isEnabled() {
        return (tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget);
    }
    let command = CommandIDs.open;
    commands.addCommand(command, {
        execute: (args) => {
            const path = args['path'];
            const widget = tracker.find(value => {
                var _a;
                return ((_a = value.console.sessionContext.session) === null || _a === void 0 ? void 0 : _a.path) === path;
            });
            if (widget) {
                if (args.activate !== false) {
                    shell.activateById(widget.id);
                }
                return widget;
            }
            else {
                return manager.ready.then(() => {
                    const model = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_11__.find)(manager.sessions.running(), item => {
                        return item.path === path;
                    });
                    if (model) {
                        return createConsole(args);
                    }
                    return Promise.reject(`No running kernel session for path: ${path}`);
                });
            }
        }
    });
    command = CommandIDs.create;
    commands.addCommand(command, {
        label: args => {
            var _a, _b, _c, _d;
            if (args['isPalette']) {
                return trans.__('New Console');
            }
            else if (args['isLauncher'] && args['kernelPreference']) {
                const kernelPreference = args['kernelPreference'];
                // TODO: Lumino command functions should probably be allowed to return undefined?
                return ((_d = (_c = (_b = (_a = manager.kernelspecs) === null || _a === void 0 ? void 0 : _a.specs) === null || _b === void 0 ? void 0 : _b.kernelspecs[kernelPreference.name || '']) === null || _c === void 0 ? void 0 : _c.display_name) !== null && _d !== void 0 ? _d : '');
            }
            return trans.__('Console');
        },
        icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_10__.consoleIcon),
        execute: args => {
            var _a;
            const basePath = (_a = (args['basePath'] ||
                args['cwd'] || (browserFactory === null || browserFactory === void 0 ? void 0 : browserFactory.defaultBrowser.model.path))) !== null && _a !== void 0 ? _a : '';
            return createConsole(Object.assign({ basePath }, args));
        }
    });
    // Get the current widget and activate unless the args specify otherwise.
    function getCurrent(args) {
        const widget = tracker.currentWidget;
        const activate = args['activate'] !== false;
        if (activate && widget) {
            shell.activateById(widget.id);
        }
        return widget !== null && widget !== void 0 ? widget : null;
    }
    commands.addCommand(CommandIDs.clear, {
        label: trans.__('Clear Console Cells'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            current.console.clear();
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runUnforced, {
        label: trans.__('Run Cell (unforced)'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.console.execute();
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runForced, {
        label: trans.__('Run Cell (forced)'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.console.execute(true);
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.linebreak, {
        label: trans.__('Insert Line Break'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            current.console.insertLinebreak();
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.replaceSelection, {
        label: trans.__('Replace Selection in Console'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            const text = args['text'] || '';
            current.console.replaceSelection(text);
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.interrupt, {
        label: trans.__('Interrupt Kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.console.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.interrupt();
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restart, {
        label: trans.__('Restart Kernel…'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return sessionDialogs.restart(current.console.sessionContext, translator);
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.closeAndShutdown, {
        label: trans.__('Close and Shut Down…'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shut down the console?'),
                body: trans.__('Are you sure you want to close "%1"?', current.title.label),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton()]
            }).then(result => {
                if (result.button.accept) {
                    return current.console.sessionContext.shutdown().then(() => {
                        current.dispose();
                        return true;
                    });
                }
                else {
                    return false;
                }
            });
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.inject, {
        execute: args => {
            const path = args['path'];
            tracker.find(widget => {
                var _a;
                if (((_a = widget.console.sessionContext.session) === null || _a === void 0 ? void 0 : _a.path) === path) {
                    if (args['activate'] !== false) {
                        shell.activateById(widget.id);
                    }
                    void widget.console.inject(args['code'], args['metadata']);
                    return true;
                }
                return false;
            });
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.changeKernel, {
        label: trans.__('Change Kernel…'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return sessionDialogs.selectKernel(current.console.sessionContext, translator);
        },
        isEnabled
    });
    if (palette) {
        // Add command palette items
        [
            CommandIDs.create,
            CommandIDs.linebreak,
            CommandIDs.clear,
            CommandIDs.runUnforced,
            CommandIDs.runForced,
            CommandIDs.restart,
            CommandIDs.interrupt,
            CommandIDs.changeKernel,
            CommandIDs.closeAndShutdown
        ].forEach(command => {
            palette.addItem({ command, category, args: { isPalette: true } });
        });
    }
    if (mainMenu) {
        // Add a close and shutdown command to the file menu.
        mainMenu.fileMenu.closeAndCleaners.add({
            tracker,
            closeAndCleanupLabel: (n) => trans.__('Shutdown Console'),
            closeAndCleanup: (current) => {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Shut down the Console?'),
                    body: trans.__('Are you sure you want to close "%1"?', current.title.label),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton()]
                }).then(result => {
                    if (result.button.accept) {
                        return current.console.sessionContext.shutdown().then(() => {
                            current.dispose();
                        });
                    }
                    else {
                        return void 0;
                    }
                });
            }
        });
        // Add a kernel user to the Kernel menu
        mainMenu.kernelMenu.kernelUsers.add({
            tracker,
            restartKernelAndClearLabel: n => trans.__('Restart Kernel and Clear Console'),
            interruptKernel: current => {
                var _a;
                const kernel = (_a = current.console.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
                if (kernel) {
                    return kernel.interrupt();
                }
                return Promise.resolve(void 0);
            },
            restartKernel: current => sessionDialogs.restart(current.console.sessionContext, translator),
            restartKernelAndClear: current => {
                return sessionDialogs
                    .restart(current.console.sessionContext)
                    .then(restarted => {
                    if (restarted) {
                        current.console.clear();
                    }
                    return restarted;
                });
            },
            changeKernel: current => sessionDialogs.selectKernel(current.console.sessionContext, translator),
            shutdownKernel: current => current.console.sessionContext.shutdown()
        });
        // Add a code runner to the Run menu.
        mainMenu.runMenu.codeRunners.add({
            tracker,
            runLabel: (n) => trans.__('Run Cell'),
            run: current => current.console.execute(true)
        });
        // Add a clearer to the edit menu
        mainMenu.editMenu.clearers.add({
            tracker,
            clearCurrentLabel: (n) => trans.__('Clear Console Cell'),
            clearCurrent: (current) => {
                return current.console.clear();
            }
        });
    }
    // For backwards compatibility and clarity, we explicitly label the run
    // keystroke with the actual effected change, rather than the generic
    // "notebook" or "terminal" interaction mode. When this interaction mode
    // affects more than just the run keystroke, we can make this menu title more
    // generic.
    const runShortcutTitles = {
        notebook: trans.__('Execute with Shift+Enter'),
        terminal: trans.__('Execute with Enter')
    };
    // Add the execute keystroke setting submenu.
    commands.addCommand(CommandIDs.interactionMode, {
        label: args => runShortcutTitles[args['interactionMode']] || '',
        execute: async (args) => {
            const key = 'keyMap';
            try {
                await settingRegistry.set(pluginId, 'interactionMode', args['interactionMode']);
            }
            catch (reason) {
                console.error(`Failed to set ${pluginId}:${key} - ${reason.message}`);
            }
        },
        isToggled: args => args['interactionMode'] === interactionMode
    });
    if (mainMenu) {
        // Add kernel information to the application help menu.
        mainMenu.helpMenu.kernelUsers.add({
            tracker,
            getKernel: current => { var _a; return (_a = current.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel; }
        });
    }
    return tracker;
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29uc29sZS1leHRlbnNpb24vc3JjL2ZvcmVpZ24udHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvbnNvbGUtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBTUo7QUFNMUI7QUFDa0M7QUFDVDtBQUVBO0FBRXREOztHQUVHO0FBQ0ksTUFBTSxPQUFPLEdBQWdDO0lBQ2xELEVBQUUsRUFBRSx1Q0FBdUM7SUFDM0MsUUFBUSxFQUFFLENBQUMsZ0VBQWUsRUFBRSx5RUFBZ0IsRUFBRSxnRUFBVyxDQUFDO0lBQzFELFFBQVEsRUFBRSxDQUFDLGlFQUFlLENBQUM7SUFDM0IsUUFBUSxFQUFFLGVBQWU7SUFDekIsU0FBUyxFQUFFLElBQUk7Q0FDaEIsQ0FBQztBQUVGLGlFQUFlLE9BQU8sRUFBQztBQUV2QixTQUFTLGVBQWUsQ0FDdEIsR0FBb0IsRUFDcEIsT0FBd0IsRUFDeEIsZUFBaUMsRUFDakMsVUFBdUIsRUFDdkIsT0FBK0I7SUFFL0IsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUM1QyxNQUFNLEVBQUUsS0FBSyxFQUFFLEdBQUcsR0FBRyxDQUFDO0lBQ3RCLE9BQU8sQ0FBQyxXQUFXLENBQUMsT0FBTyxDQUFDLENBQUMsTUFBTSxFQUFFLE1BQU0sRUFBRSxFQUFFO1FBQzdDLE1BQU0sT0FBTyxHQUFHLE1BQU0sQ0FBQyxPQUFPLENBQUM7UUFFL0IsTUFBTSxPQUFPLEdBQUcsSUFBSSwrREFBYyxDQUFDO1lBQ2pDLGNBQWMsRUFBRSxPQUFPLENBQUMsY0FBYztZQUN0QyxNQUFNLEVBQUUsT0FBTztTQUNoQixDQUFDLENBQUM7UUFDSCxP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QUMsaUJBQWlCLENBQUMsS0FBSyxlQUFlO0tBQy9ELENBQUMsQ0FBQztJQUVILElBQUksUUFBUSxFQUFFO1FBQ1osdURBQXVEO1FBQ3ZELFFBQVEsQ0FBQyxRQUFRLENBQUMsV0FBVyxDQUFDLEdBQUcsQ0FBQztZQUNoQyxPQUFPO1lBQ1AsU0FBUyxFQUFFLE9BQU8sQ0FBQyxFQUFFLHdCQUFDLE9BQU8sQ0FBQyxjQUFjLENBQUMsT0FBTywwQ0FBRSxNQUFNO1NBQ3RCLENBQUMsQ0FBQztLQUMzQztJQUVELE9BQU8sT0FBTyxDQUFDO0FBQ2pCLENBQUMiLCJmaWxlIjoicGFja2FnZXNfY29uc29sZS1leHRlbnNpb25fbGliX2luZGV4X2pzLjA4ODViNzdmODM5NDNiNTljMjY0LmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJQ29tbWFuZFBhbGV0dGUgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQge1xuICBDb2RlQ29uc29sZSxcbiAgQ29uc29sZVBhbmVsLFxuICBGb3JlaWduSGFuZGxlcixcbiAgSUNvbnNvbGVUcmFja2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL2NvbnNvbGUnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBBdHRhY2hlZFByb3BlcnR5IH0gZnJvbSAnQGx1bWluby9wcm9wZXJ0aWVzJztcblxuLyoqXG4gKiBUaGUgY29uc29sZSB3aWRnZXQgdHJhY2tlciBwcm92aWRlci5cbiAqL1xuZXhwb3J0IGNvbnN0IGZvcmVpZ246IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9jb25zb2xlLWV4dGVuc2lvbjpmb3JlaWduJyxcbiAgcmVxdWlyZXM6IFtJQ29uc29sZVRyYWNrZXIsIElTZXR0aW5nUmVnaXN0cnksIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJQ29tbWFuZFBhbGV0dGVdLFxuICBhY3RpdmF0ZTogYWN0aXZhdGVGb3JlaWduLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbmV4cG9ydCBkZWZhdWx0IGZvcmVpZ247XG5cbmZ1bmN0aW9uIGFjdGl2YXRlRm9yZWlnbihcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHRyYWNrZXI6IElDb25zb2xlVHJhY2tlcixcbiAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuKTogdm9pZCB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgc2hlbGwgfSA9IGFwcDtcbiAgdHJhY2tlci53aWRnZXRBZGRlZC5jb25uZWN0KChzZW5kZXIsIHdpZGdldCkgPT4ge1xuICAgIGNvbnN0IGNvbnNvbGUgPSB3aWRnZXQuY29uc29sZTtcblxuICAgIGNvbnN0IGhhbmRsZXIgPSBuZXcgRm9yZWlnbkhhbmRsZXIoe1xuICAgICAgc2Vzc2lvbkNvbnRleHQ6IGNvbnNvbGUuc2Vzc2lvbkNvbnRleHQsXG4gICAgICBwYXJlbnQ6IGNvbnNvbGVcbiAgICB9KTtcbiAgICBQcml2YXRlLmZvcmVpZ25IYW5kbGVyUHJvcGVydHkuc2V0KGNvbnNvbGUsIGhhbmRsZXIpO1xuXG4gICAgLy8gUHJvcGVydHkgc2hvd0FsbEtlcm5lbEFjdGl2aXR5IGNvbmZpZ3VyZXMgZm9yZWlnbiBoYW5kbGVyIGVuYWJsZWQgb24gc3RhcnQuXG4gICAgdm9pZCBzZXR0aW5nUmVnaXN0cnlcbiAgICAgIC5nZXQoJ0BqdXB5dGVybGFiL2NvbnNvbGUtZXh0ZW5zaW9uOnRyYWNrZXInLCAnc2hvd0FsbEtlcm5lbEFjdGl2aXR5JylcbiAgICAgIC50aGVuKCh7IGNvbXBvc2l0ZSB9KSA9PiB7XG4gICAgICAgIGNvbnN0IHNob3dBbGxLZXJuZWxBY3Rpdml0eSA9IGNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgICBoYW5kbGVyLmVuYWJsZWQgPSBzaG93QWxsS2VybmVsQWN0aXZpdHk7XG4gICAgICB9KTtcblxuICAgIGNvbnNvbGUuZGlzcG9zZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICBoYW5kbGVyLmRpc3Bvc2UoKTtcbiAgICB9KTtcbiAgfSk7XG5cbiAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdDb25zb2xlJyk7XG4gIGNvbnN0IHRvZ2dsZVNob3dBbGxBY3Rpdml0eSA9ICdjb25zb2xlOnRvZ2dsZS1zaG93LWFsbC1rZXJuZWwtYWN0aXZpdHknO1xuXG4gIC8vIEdldCB0aGUgY3VycmVudCB3aWRnZXQgYW5kIGFjdGl2YXRlIHVubGVzcyB0aGUgYXJncyBzcGVjaWZ5IG90aGVyd2lzZS5cbiAgZnVuY3Rpb24gZ2V0Q3VycmVudChhcmdzOiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0KTogQ29uc29sZVBhbmVsIHwgbnVsbCB7XG4gICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgIGNvbnN0IGFjdGl2YXRlID0gYXJnc1snYWN0aXZhdGUnXSAhPT0gZmFsc2U7XG4gICAgaWYgKGFjdGl2YXRlICYmIHdpZGdldCkge1xuICAgICAgc2hlbGwuYWN0aXZhdGVCeUlkKHdpZGdldC5pZCk7XG4gICAgfVxuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cblxuICBjb21tYW5kcy5hZGRDb21tYW5kKHRvZ2dsZVNob3dBbGxBY3Rpdml0eSwge1xuICAgIGxhYmVsOiBhcmdzID0+IHRyYW5zLl9fKCdTaG93IEFsbCBLZXJuZWwgQWN0aXZpdHknKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSBnZXRDdXJyZW50KGFyZ3MpO1xuICAgICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGhhbmRsZXIgPSBQcml2YXRlLmZvcmVpZ25IYW5kbGVyUHJvcGVydHkuZ2V0KGN1cnJlbnQuY29uc29sZSk7XG4gICAgICBpZiAoaGFuZGxlcikge1xuICAgICAgICBoYW5kbGVyLmVuYWJsZWQgPSAhaGFuZGxlci5lbmFibGVkO1xuICAgICAgfVxuICAgIH0sXG4gICAgaXNUb2dnbGVkOiAoKSA9PlxuICAgICAgdHJhY2tlci5jdXJyZW50V2lkZ2V0ICE9PSBudWxsICYmXG4gICAgICAhIVByaXZhdGUuZm9yZWlnbkhhbmRsZXJQcm9wZXJ0eS5nZXQodHJhY2tlci5jdXJyZW50V2lkZ2V0LmNvbnNvbGUpXG4gICAgICAgID8uZW5hYmxlZCxcbiAgICBpc0VuYWJsZWQ6ICgpID0+XG4gICAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgIT09IG51bGwgJiZcbiAgICAgIHRyYWNrZXIuY3VycmVudFdpZGdldCA9PT0gc2hlbGwuY3VycmVudFdpZGdldFxuICB9KTtcblxuICBpZiAocGFsZXR0ZSkge1xuICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICBjb21tYW5kOiB0b2dnbGVTaG93QWxsQWN0aXZpdHksXG4gICAgICBjYXRlZ29yeSxcbiAgICAgIGFyZ3M6IHsgaXNQYWxldHRlOiB0cnVlIH1cbiAgICB9KTtcbiAgfVxufVxuXG4vKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQW4gYXR0YWNoZWQgcHJvcGVydHkgZm9yIGEgY29uc29sZSdzIGZvcmVpZ24gaGFuZGxlci5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBmb3JlaWduSGFuZGxlclByb3BlcnR5ID0gbmV3IEF0dGFjaGVkUHJvcGVydHk8XG4gICAgQ29kZUNvbnNvbGUsXG4gICAgRm9yZWlnbkhhbmRsZXIgfCB1bmRlZmluZWRcbiAgPih7XG4gICAgbmFtZTogJ2ZvcmVpZ25IYW5kbGVyJyxcbiAgICBjcmVhdGU6ICgpID0+IHVuZGVmaW5lZFxuICB9KTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGNvbnNvbGUtZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlN0YXR1cyxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBEaWFsb2csXG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgSVNlc3Npb25Db250ZXh0LFxuICBJU2Vzc2lvbkNvbnRleHREaWFsb2dzLFxuICBzZXNzaW9uQ29udGV4dERpYWxvZ3MsXG4gIHNob3dEaWFsb2csXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgQ29kZUVkaXRvciwgSUVkaXRvclNlcnZpY2VzIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQgeyBDb25zb2xlUGFuZWwsIElDb25zb2xlVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2NvbnNvbGUnO1xuaW1wb3J0IHsgSUZpbGVCcm93c2VyRmFjdG9yeSB9IGZyb20gJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyJztcbmltcG9ydCB7IElMYXVuY2hlciB9IGZyb20gJ0BqdXB5dGVybGFiL2xhdW5jaGVyJztcbmltcG9ydCB7XG4gIElFZGl0TWVudSxcbiAgSUZpbGVNZW51LFxuICBJSGVscE1lbnUsXG4gIElLZXJuZWxNZW51LFxuICBJTWFpbk1lbnUsXG4gIElSdW5NZW51XG59IGZyb20gJ0BqdXB5dGVybGFiL21haW5tZW51JztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBjb25zb2xlSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgZmluZCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7XG4gIEpTT05FeHQsXG4gIEpTT05PYmplY3QsXG4gIFJlYWRvbmx5SlNPTlZhbHVlLFxuICBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0LFxuICBVVUlEXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IERpc3Bvc2FibGVTZXQgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgRG9ja0xheW91dCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgZm9yZWlnbiBmcm9tICcuL2ZvcmVpZ24nO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBjb25zb2xlIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgYXV0b0Nsb3NpbmdCcmFja2V0cyA9ICdjb25zb2xlOnRvZ2dsZS1hdXRvY2xvc2luZy1icmFja2V0cyc7XG5cbiAgZXhwb3J0IGNvbnN0IGNyZWF0ZSA9ICdjb25zb2xlOmNyZWF0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGNsZWFyID0gJ2NvbnNvbGU6Y2xlYXInO1xuXG4gIGV4cG9ydCBjb25zdCBydW5VbmZvcmNlZCA9ICdjb25zb2xlOnJ1bi11bmZvcmNlZCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJ1bkZvcmNlZCA9ICdjb25zb2xlOnJ1bi1mb3JjZWQnO1xuXG4gIGV4cG9ydCBjb25zdCBsaW5lYnJlYWsgPSAnY29uc29sZTpsaW5lYnJlYWsnO1xuXG4gIGV4cG9ydCBjb25zdCBpbnRlcnJ1cHQgPSAnY29uc29sZTppbnRlcnJ1cHQta2VybmVsJztcblxuICBleHBvcnQgY29uc3QgcmVzdGFydCA9ICdjb25zb2xlOnJlc3RhcnQta2VybmVsJztcblxuICBleHBvcnQgY29uc3QgY2xvc2VBbmRTaHV0ZG93biA9ICdjb25zb2xlOmNsb3NlLWFuZC1zaHV0ZG93bic7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW4gPSAnY29uc29sZTpvcGVuJztcblxuICBleHBvcnQgY29uc3QgaW5qZWN0ID0gJ2NvbnNvbGU6aW5qZWN0JztcblxuICBleHBvcnQgY29uc3QgY2hhbmdlS2VybmVsID0gJ2NvbnNvbGU6Y2hhbmdlLWtlcm5lbCc7XG5cbiAgZXhwb3J0IGNvbnN0IGVudGVyVG9FeGVjdXRlID0gJ2NvbnNvbGU6ZW50ZXItdG8tZXhlY3V0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNoaWZ0RW50ZXJUb0V4ZWN1dGUgPSAnY29uc29sZTpzaGlmdC1lbnRlci10by1leGVjdXRlJztcblxuICBleHBvcnQgY29uc3QgaW50ZXJhY3Rpb25Nb2RlID0gJ2NvbnNvbGU6aW50ZXJhY3Rpb24tbW9kZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlcGxhY2VTZWxlY3Rpb24gPSAnY29uc29sZTpyZXBsYWNlLXNlbGVjdGlvbic7XG59XG5cbi8qKlxuICogVGhlIGNvbnNvbGUgd2lkZ2V0IHRyYWNrZXIgcHJvdmlkZXIuXG4gKi9cbmNvbnN0IHRyYWNrZXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJQ29uc29sZVRyYWNrZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvbnNvbGUtZXh0ZW5zaW9uOnRyYWNrZXInLFxuICBwcm92aWRlczogSUNvbnNvbGVUcmFja2VyLFxuICByZXF1aXJlczogW1xuICAgIENvbnNvbGVQYW5lbC5JQ29udGVudEZhY3RvcnksXG4gICAgSUVkaXRvclNlcnZpY2VzLFxuICAgIElSZW5kZXJNaW1lUmVnaXN0cnksXG4gICAgSVNldHRpbmdSZWdpc3RyeSxcbiAgICBJVHJhbnNsYXRvclxuICBdLFxuICBvcHRpb25hbDogW1xuICAgIElMYXlvdXRSZXN0b3JlcixcbiAgICBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIElNYWluTWVudSxcbiAgICBJQ29tbWFuZFBhbGV0dGUsXG4gICAgSUxhdW5jaGVyLFxuICAgIElMYWJTdGF0dXMsXG4gICAgSVNlc3Npb25Db250ZXh0RGlhbG9nc1xuICBdLFxuICBhY3RpdmF0ZTogYWN0aXZhdGVDb25zb2xlLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogVGhlIGNvbnNvbGUgd2lkZ2V0IGNvbnRlbnQgZmFjdG9yeS5cbiAqL1xuY29uc3QgZmFjdG9yeTogSnVweXRlckZyb250RW5kUGx1Z2luPENvbnNvbGVQYW5lbC5JQ29udGVudEZhY3Rvcnk+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvbnNvbGUtZXh0ZW5zaW9uOmZhY3RvcnknLFxuICBwcm92aWRlczogQ29uc29sZVBhbmVsLklDb250ZW50RmFjdG9yeSxcbiAgcmVxdWlyZXM6IFtJRWRpdG9yU2VydmljZXNdLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQsIGVkaXRvclNlcnZpY2VzOiBJRWRpdG9yU2VydmljZXMpID0+IHtcbiAgICBjb25zdCBlZGl0b3JGYWN0b3J5ID0gZWRpdG9yU2VydmljZXMuZmFjdG9yeVNlcnZpY2UubmV3SW5saW5lRWRpdG9yO1xuICAgIHJldHVybiBuZXcgQ29uc29sZVBhbmVsLkNvbnRlbnRGYWN0b3J5KHsgZWRpdG9yRmFjdG9yeSB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbnMgYXMgdGhlIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbZmFjdG9yeSwgdHJhY2tlciwgZm9yZWlnbl07XG5leHBvcnQgZGVmYXVsdCBwbHVnaW5zO1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBjb25zb2xlIGV4dGVuc2lvbi5cbiAqL1xuYXN5bmMgZnVuY3Rpb24gYWN0aXZhdGVDb25zb2xlKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgY29udGVudEZhY3Rvcnk6IENvbnNvbGVQYW5lbC5JQ29udGVudEZhY3RvcnksXG4gIGVkaXRvclNlcnZpY2VzOiBJRWRpdG9yU2VydmljZXMsXG4gIHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIHJlc3RvcmVyOiBJTGF5b3V0UmVzdG9yZXIgfCBudWxsLFxuICBicm93c2VyRmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeSB8IG51bGwsXG4gIG1haW5NZW51OiBJTWFpbk1lbnUgfCBudWxsLFxuICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsLFxuICBsYXVuY2hlcjogSUxhdW5jaGVyIHwgbnVsbCxcbiAgc3RhdHVzOiBJTGFiU3RhdHVzIHwgbnVsbCxcbiAgc2Vzc2lvbkRpYWxvZ3M6IElTZXNzaW9uQ29udGV4dERpYWxvZ3MgfCBudWxsXG4pOiBQcm9taXNlPElDb25zb2xlVHJhY2tlcj4ge1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCBtYW5hZ2VyID0gYXBwLnNlcnZpY2VNYW5hZ2VyO1xuICBjb25zdCB7IGNvbW1hbmRzLCBzaGVsbCB9ID0gYXBwO1xuICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdDb25zb2xlJyk7XG4gIHNlc3Npb25EaWFsb2dzID0gc2Vzc2lvbkRpYWxvZ3MgPz8gc2Vzc2lvbkNvbnRleHREaWFsb2dzO1xuXG4gIC8vIENyZWF0ZSBhIHdpZGdldCB0cmFja2VyIGZvciBhbGwgY29uc29sZSBwYW5lbHMuXG4gIGNvbnN0IHRyYWNrZXIgPSBuZXcgV2lkZ2V0VHJhY2tlcjxDb25zb2xlUGFuZWw+KHtcbiAgICBuYW1lc3BhY2U6ICdjb25zb2xlJ1xuICB9KTtcblxuICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gIGlmIChyZXN0b3Jlcikge1xuICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZSh0cmFja2VyLCB7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLmNyZWF0ZSxcbiAgICAgIGFyZ3M6IHdpZGdldCA9PiB7XG4gICAgICAgIGNvbnN0IHsgcGF0aCwgbmFtZSwga2VybmVsUHJlZmVyZW5jZSB9ID0gd2lkZ2V0LmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQ7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgcGF0aCxcbiAgICAgICAgICBuYW1lLFxuICAgICAgICAgIGtlcm5lbFByZWZlcmVuY2U6IHsgLi4ua2VybmVsUHJlZmVyZW5jZSB9XG4gICAgICAgIH07XG4gICAgICB9LFxuICAgICAgbmFtZTogd2lkZ2V0ID0+IHdpZGdldC5jb25zb2xlLnNlc3Npb25Db250ZXh0LnBhdGggPz8gVVVJRC51dWlkNCgpLFxuICAgICAgd2hlbjogbWFuYWdlci5yZWFkeVxuICAgIH0pO1xuICB9XG5cbiAgLy8gQWRkIGEgbGF1bmNoZXIgaXRlbSBpZiB0aGUgbGF1bmNoZXIgaXMgYXZhaWxhYmxlLlxuICBpZiAobGF1bmNoZXIpIHtcbiAgICB2b2lkIG1hbmFnZXIucmVhZHkudGhlbigoKSA9PiB7XG4gICAgICBsZXQgZGlzcG9zYWJsZXM6IERpc3Bvc2FibGVTZXQgfCBudWxsID0gbnVsbDtcbiAgICAgIGNvbnN0IG9uU3BlY3NDaGFuZ2VkID0gKCkgPT4ge1xuICAgICAgICBpZiAoZGlzcG9zYWJsZXMpIHtcbiAgICAgICAgICBkaXNwb3NhYmxlcy5kaXNwb3NlKCk7XG4gICAgICAgICAgZGlzcG9zYWJsZXMgPSBudWxsO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IHNwZWNzID0gbWFuYWdlci5rZXJuZWxzcGVjcy5zcGVjcztcbiAgICAgICAgaWYgKCFzcGVjcykge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBkaXNwb3NhYmxlcyA9IG5ldyBEaXNwb3NhYmxlU2V0KCk7XG4gICAgICAgIGZvciAoY29uc3QgbmFtZSBpbiBzcGVjcy5rZXJuZWxzcGVjcykge1xuICAgICAgICAgIGNvbnN0IHJhbmsgPSBuYW1lID09PSBzcGVjcy5kZWZhdWx0ID8gMCA6IEluZmluaXR5O1xuICAgICAgICAgIGNvbnN0IHNwZWMgPSBzcGVjcy5rZXJuZWxzcGVjc1tuYW1lXSE7XG4gICAgICAgICAgbGV0IGtlcm5lbEljb25VcmwgPSBzcGVjLnJlc291cmNlc1snbG9nby02NHg2NCddO1xuICAgICAgICAgIGRpc3Bvc2FibGVzLmFkZChcbiAgICAgICAgICAgIGxhdW5jaGVyLmFkZCh7XG4gICAgICAgICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuY3JlYXRlLFxuICAgICAgICAgICAgICBhcmdzOiB7IGlzTGF1bmNoZXI6IHRydWUsIGtlcm5lbFByZWZlcmVuY2U6IHsgbmFtZSB9IH0sXG4gICAgICAgICAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnQ29uc29sZScpLFxuICAgICAgICAgICAgICByYW5rLFxuICAgICAgICAgICAgICBrZXJuZWxJY29uVXJsLFxuICAgICAgICAgICAgICBtZXRhZGF0YToge1xuICAgICAgICAgICAgICAgIGtlcm5lbDogSlNPTkV4dC5kZWVwQ29weShcbiAgICAgICAgICAgICAgICAgIHNwZWMubWV0YWRhdGEgfHwge31cbiAgICAgICAgICAgICAgICApIGFzIFJlYWRvbmx5SlNPTlZhbHVlXG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0pXG4gICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgfTtcbiAgICAgIG9uU3BlY3NDaGFuZ2VkKCk7XG4gICAgICBtYW5hZ2VyLmtlcm5lbHNwZWNzLnNwZWNzQ2hhbmdlZC5jb25uZWN0KG9uU3BlY3NDaGFuZ2VkKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB1c2VkIHRvIGNyZWF0ZSBhIHdpZGdldC5cbiAgICovXG4gIGludGVyZmFjZSBJQ3JlYXRlT3B0aW9ucyBleHRlbmRzIFBhcnRpYWw8Q29uc29sZVBhbmVsLklPcHRpb25zPiB7XG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byBhY3RpdmF0ZSB0aGUgd2lkZ2V0LiAgRGVmYXVsdHMgdG8gYHRydWVgLlxuICAgICAqL1xuICAgIGFjdGl2YXRlPzogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSByZWZlcmVuY2Ugd2lkZ2V0IGlkIGZvciB0aGUgaW5zZXJ0IGxvY2F0aW9uLlxuICAgICAqXG4gICAgICogVGhlIGRlZmF1bHQgaXMgYG51bGxgLlxuICAgICAqL1xuICAgIHJlZj86IHN0cmluZyB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdGFiIGluc2VydCBtb2RlLlxuICAgICAqXG4gICAgICogQW4gaW5zZXJ0IG1vZGUgaXMgdXNlZCB0byBzcGVjaWZ5IGhvdyBhIHdpZGdldCBzaG91bGQgYmUgYWRkZWRcbiAgICAgKiB0byB0aGUgbWFpbiBhcmVhIHJlbGF0aXZlIHRvIGEgcmVmZXJlbmNlIHdpZGdldC5cbiAgICAgKi9cbiAgICBpbnNlcnRNb2RlPzogRG9ja0xheW91dC5JbnNlcnRNb2RlO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIGNvbnNvbGUgZm9yIGEgZ2l2ZW4gcGF0aC5cbiAgICovXG4gIGFzeW5jIGZ1bmN0aW9uIGNyZWF0ZUNvbnNvbGUob3B0aW9uczogSUNyZWF0ZU9wdGlvbnMpOiBQcm9taXNlPENvbnNvbGVQYW5lbD4ge1xuICAgIGF3YWl0IG1hbmFnZXIucmVhZHk7XG5cbiAgICBjb25zdCBwYW5lbCA9IG5ldyBDb25zb2xlUGFuZWwoe1xuICAgICAgbWFuYWdlcixcbiAgICAgIGNvbnRlbnRGYWN0b3J5LFxuICAgICAgbWltZVR5cGVTZXJ2aWNlOiBlZGl0b3JTZXJ2aWNlcy5taW1lVHlwZVNlcnZpY2UsXG4gICAgICByZW5kZXJtaW1lLFxuICAgICAgdHJhbnNsYXRvcixcbiAgICAgIHNldEJ1c3k6IChzdGF0dXMgJiYgKCgpID0+IHN0YXR1cy5zZXRCdXN5KCkpKSA/PyB1bmRlZmluZWQsXG4gICAgICAuLi4ob3B0aW9ucyBhcyBQYXJ0aWFsPENvbnNvbGVQYW5lbC5JT3B0aW9ucz4pXG4gICAgfSk7XG5cbiAgICBjb25zdCBpbnRlcmFjdGlvbk1vZGU6IHN0cmluZyA9IChcbiAgICAgIGF3YWl0IHNldHRpbmdSZWdpc3RyeS5nZXQoXG4gICAgICAgICdAanVweXRlcmxhYi9jb25zb2xlLWV4dGVuc2lvbjp0cmFja2VyJyxcbiAgICAgICAgJ2ludGVyYWN0aW9uTW9kZSdcbiAgICAgIClcbiAgICApLmNvbXBvc2l0ZSBhcyBzdHJpbmc7XG4gICAgcGFuZWwuY29uc29sZS5ub2RlLmRhdGFzZXQuanBJbnRlcmFjdGlvbk1vZGUgPSBpbnRlcmFjdGlvbk1vZGU7XG5cbiAgICAvLyBBZGQgdGhlIGNvbnNvbGUgcGFuZWwgdG8gdGhlIHRyYWNrZXIuIFdlIHdhbnQgdGhlIHBhbmVsIHRvIHNob3cgdXAgYmVmb3JlXG4gICAgLy8gYW55IGtlcm5lbCBzZWxlY3Rpb24gZGlhbG9nLCBzbyB3ZSBkbyBub3QgYXdhaXQgcGFuZWwuc2Vzc2lvbi5yZWFkeTtcbiAgICBhd2FpdCB0cmFja2VyLmFkZChwYW5lbCk7XG4gICAgcGFuZWwuc2Vzc2lvbkNvbnRleHQucHJvcGVydHlDaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgdm9pZCB0cmFja2VyLnNhdmUocGFuZWwpO1xuICAgIH0pO1xuXG4gICAgc2hlbGwuYWRkKHBhbmVsLCAnbWFpbicsIHtcbiAgICAgIHJlZjogb3B0aW9ucy5yZWYsXG4gICAgICBtb2RlOiBvcHRpb25zLmluc2VydE1vZGUsXG4gICAgICBhY3RpdmF0ZTogb3B0aW9ucy5hY3RpdmF0ZSAhPT0gZmFsc2VcbiAgICB9KTtcbiAgICByZXR1cm4gcGFuZWw7XG4gIH1cblxuICB0eXBlIGxpbmVXcmFwX3R5cGUgPSAnb2ZmJyB8ICdvbicgfCAnd29yZFdyYXBDb2x1bW4nIHwgJ2JvdW5kZWQnO1xuXG4gIGNvbnN0IG1hcE9wdGlvbiA9IChcbiAgICBlZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvcixcbiAgICBjb25maWc6IEpTT05PYmplY3QsXG4gICAgb3B0aW9uOiBzdHJpbmdcbiAgKSA9PiB7XG4gICAgaWYgKGNvbmZpZ1tvcHRpb25dID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgc3dpdGNoIChvcHRpb24pIHtcbiAgICAgIGNhc2UgJ2F1dG9DbG9zaW5nQnJhY2tldHMnOlxuICAgICAgICBlZGl0b3Iuc2V0T3B0aW9uKFxuICAgICAgICAgICdhdXRvQ2xvc2luZ0JyYWNrZXRzJyxcbiAgICAgICAgICBjb25maWdbJ2F1dG9DbG9zaW5nQnJhY2tldHMnXSBhcyBib29sZWFuXG4gICAgICAgICk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnY3Vyc29yQmxpbmtSYXRlJzpcbiAgICAgICAgZWRpdG9yLnNldE9wdGlvbihcbiAgICAgICAgICAnY3Vyc29yQmxpbmtSYXRlJyxcbiAgICAgICAgICBjb25maWdbJ2N1cnNvckJsaW5rUmF0ZSddIGFzIG51bWJlclxuICAgICAgICApO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2ZvbnRGYW1pbHknOlxuICAgICAgICBlZGl0b3Iuc2V0T3B0aW9uKCdmb250RmFtaWx5JywgY29uZmlnWydmb250RmFtaWx5J10gYXMgc3RyaW5nIHwgbnVsbCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnZm9udFNpemUnOlxuICAgICAgICBlZGl0b3Iuc2V0T3B0aW9uKCdmb250U2l6ZScsIGNvbmZpZ1snZm9udFNpemUnXSBhcyBudW1iZXIgfCBudWxsKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdsaW5lSGVpZ2h0JzpcbiAgICAgICAgZWRpdG9yLnNldE9wdGlvbignbGluZUhlaWdodCcsIGNvbmZpZ1snbGluZUhlaWdodCddIGFzIG51bWJlciB8IG51bGwpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2xpbmVOdW1iZXJzJzpcbiAgICAgICAgZWRpdG9yLnNldE9wdGlvbignbGluZU51bWJlcnMnLCBjb25maWdbJ2xpbmVOdW1iZXJzJ10gYXMgYm9vbGVhbik7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnbGluZVdyYXAnOlxuICAgICAgICBlZGl0b3Iuc2V0T3B0aW9uKCdsaW5lV3JhcCcsIGNvbmZpZ1snbGluZVdyYXAnXSBhcyBsaW5lV3JhcF90eXBlKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdtYXRjaEJyYWNrZXRzJzpcbiAgICAgICAgZWRpdG9yLnNldE9wdGlvbignbWF0Y2hCcmFja2V0cycsIGNvbmZpZ1snbWF0Y2hCcmFja2V0cyddIGFzIGJvb2xlYW4pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3JlYWRPbmx5JzpcbiAgICAgICAgZWRpdG9yLnNldE9wdGlvbigncmVhZE9ubHknLCBjb25maWdbJ3JlYWRPbmx5J10gYXMgYm9vbGVhbik7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnaW5zZXJ0U3BhY2VzJzpcbiAgICAgICAgZWRpdG9yLnNldE9wdGlvbignaW5zZXJ0U3BhY2VzJywgY29uZmlnWydpbnNlcnRTcGFjZXMnXSBhcyBib29sZWFuKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICd0YWJTaXplJzpcbiAgICAgICAgZWRpdG9yLnNldE9wdGlvbigndGFiU2l6ZScsIGNvbmZpZ1sndGFiU2l6ZSddIGFzIG51bWJlcik7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnd29yZFdyYXBDb2x1bW4nOlxuICAgICAgICBlZGl0b3Iuc2V0T3B0aW9uKCd3b3JkV3JhcENvbHVtbicsIGNvbmZpZ1snd29yZFdyYXBDb2x1bW4nXSBhcyBudW1iZXIpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3J1bGVycyc6XG4gICAgICAgIGVkaXRvci5zZXRPcHRpb24oJ3J1bGVycycsIGNvbmZpZ1sncnVsZXJzJ10gYXMgbnVtYmVyW10pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2NvZGVGb2xkaW5nJzpcbiAgICAgICAgZWRpdG9yLnNldE9wdGlvbignY29kZUZvbGRpbmcnLCBjb25maWdbJ2NvZGVGb2xkaW5nJ10gYXMgYm9vbGVhbik7XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfTtcblxuICBjb25zdCBzZXRPcHRpb24gPSAoXG4gICAgZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3IgfCB1bmRlZmluZWQsXG4gICAgY29uZmlnOiBKU09OT2JqZWN0XG4gICkgPT4ge1xuICAgIGlmIChlZGl0b3IgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBtYXBPcHRpb24oZWRpdG9yLCBjb25maWcsICdhdXRvQ2xvc2luZ0JyYWNrZXRzJyk7XG4gICAgbWFwT3B0aW9uKGVkaXRvciwgY29uZmlnLCAnY3Vyc29yQmxpbmtSYXRlJyk7XG4gICAgbWFwT3B0aW9uKGVkaXRvciwgY29uZmlnLCAnZm9udEZhbWlseScpO1xuICAgIG1hcE9wdGlvbihlZGl0b3IsIGNvbmZpZywgJ2ZvbnRTaXplJyk7XG4gICAgbWFwT3B0aW9uKGVkaXRvciwgY29uZmlnLCAnbGluZUhlaWdodCcpO1xuICAgIG1hcE9wdGlvbihlZGl0b3IsIGNvbmZpZywgJ2xpbmVOdW1iZXJzJyk7XG4gICAgbWFwT3B0aW9uKGVkaXRvciwgY29uZmlnLCAnbGluZVdyYXAnKTtcbiAgICBtYXBPcHRpb24oZWRpdG9yLCBjb25maWcsICdtYXRjaEJyYWNrZXRzJyk7XG4gICAgbWFwT3B0aW9uKGVkaXRvciwgY29uZmlnLCAncmVhZE9ubHknKTtcbiAgICBtYXBPcHRpb24oZWRpdG9yLCBjb25maWcsICdpbnNlcnRTcGFjZXMnKTtcbiAgICBtYXBPcHRpb24oZWRpdG9yLCBjb25maWcsICd0YWJTaXplJyk7XG4gICAgbWFwT3B0aW9uKGVkaXRvciwgY29uZmlnLCAnd29yZFdyYXBDb2x1bW4nKTtcbiAgICBtYXBPcHRpb24oZWRpdG9yLCBjb25maWcsICdydWxlcnMnKTtcbiAgICBtYXBPcHRpb24oZWRpdG9yLCBjb25maWcsICdjb2RlRm9sZGluZycpO1xuICB9O1xuXG4gIGNvbnN0IHBsdWdpbklkID0gJ0BqdXB5dGVybGFiL2NvbnNvbGUtZXh0ZW5zaW9uOnRyYWNrZXInO1xuICBsZXQgaW50ZXJhY3Rpb25Nb2RlOiBzdHJpbmc7XG4gIGxldCBwcm9tcHRDZWxsQ29uZmlnOiBKU09OT2JqZWN0O1xuXG4gIC8qKlxuICAgKiBVcGRhdGUgc2V0dGluZ3MgZm9yIG9uZSBjb25zb2xlIG9yIGFsbCBjb25zb2xlcy5cbiAgICpcbiAgICogQHBhcmFtIHBhbmVsIE9wdGlvbmFsIC0gc2luZ2xlIGNvbnNvbGUgdG8gdXBkYXRlLlxuICAgKi9cbiAgYXN5bmMgZnVuY3Rpb24gdXBkYXRlU2V0dGluZ3MocGFuZWw/OiBDb25zb2xlUGFuZWwpIHtcbiAgICBpbnRlcmFjdGlvbk1vZGUgPSAoYXdhaXQgc2V0dGluZ1JlZ2lzdHJ5LmdldChwbHVnaW5JZCwgJ2ludGVyYWN0aW9uTW9kZScpKVxuICAgICAgLmNvbXBvc2l0ZSBhcyBzdHJpbmc7XG4gICAgcHJvbXB0Q2VsbENvbmZpZyA9IChhd2FpdCBzZXR0aW5nUmVnaXN0cnkuZ2V0KHBsdWdpbklkLCAncHJvbXB0Q2VsbENvbmZpZycpKVxuICAgICAgLmNvbXBvc2l0ZSBhcyBKU09OT2JqZWN0O1xuXG4gICAgY29uc3Qgc2V0V2lkZ2V0T3B0aW9ucyA9ICh3aWRnZXQ6IENvbnNvbGVQYW5lbCkgPT4ge1xuICAgICAgd2lkZ2V0LmNvbnNvbGUubm9kZS5kYXRhc2V0LmpwSW50ZXJhY3Rpb25Nb2RlID0gaW50ZXJhY3Rpb25Nb2RlO1xuICAgICAgc2V0T3B0aW9uKHdpZGdldC5jb25zb2xlLnByb21wdENlbGw/LmVkaXRvciwgcHJvbXB0Q2VsbENvbmZpZyk7XG4gICAgfTtcblxuICAgIGlmIChwYW5lbCkge1xuICAgICAgc2V0V2lkZ2V0T3B0aW9ucyhwYW5lbCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRyYWNrZXIuZm9yRWFjaChzZXRXaWRnZXRPcHRpb25zKTtcbiAgICB9XG4gIH1cblxuICBzZXR0aW5nUmVnaXN0cnkucGx1Z2luQ2hhbmdlZC5jb25uZWN0KChzZW5kZXIsIHBsdWdpbikgPT4ge1xuICAgIGlmIChwbHVnaW4gPT09IHBsdWdpbklkKSB7XG4gICAgICB2b2lkIHVwZGF0ZVNldHRpbmdzKCk7XG4gICAgfVxuICB9KTtcbiAgYXdhaXQgdXBkYXRlU2V0dGluZ3MoKTtcblxuICAvLyBBcHBseSBzZXR0aW5ncyB3aGVuIGEgY29uc29sZSBpcyBjcmVhdGVkLlxuICB0cmFja2VyLndpZGdldEFkZGVkLmNvbm5lY3QoKHNlbmRlciwgcGFuZWwpID0+IHtcbiAgICB2b2lkIHVwZGF0ZVNldHRpbmdzKHBhbmVsKTtcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmF1dG9DbG9zaW5nQnJhY2tldHMsIHtcbiAgICBleGVjdXRlOiBhc3luYyBhcmdzID0+IHtcbiAgICAgIHByb21wdENlbGxDb25maWcuYXV0b0Nsb3NpbmdCcmFja2V0cyA9ICEhKFxuICAgICAgICBhcmdzWydmb3JjZSddID8/ICFwcm9tcHRDZWxsQ29uZmlnLmF1dG9DbG9zaW5nQnJhY2tldHNcbiAgICAgICk7XG4gICAgICBhd2FpdCBzZXR0aW5nUmVnaXN0cnkuc2V0KHBsdWdpbklkLCAncHJvbXB0Q2VsbENvbmZpZycsIHByb21wdENlbGxDb25maWcpO1xuICAgIH0sXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdBdXRvIENsb3NlIEJyYWNrZXRzIGZvciBDb2RlIENvbnNvbGUgUHJvbXB0JyksXG4gICAgaXNUb2dnbGVkOiAoKSA9PiBwcm9tcHRDZWxsQ29uZmlnLmF1dG9DbG9zaW5nQnJhY2tldHMgYXMgYm9vbGVhblxuICB9KTtcblxuICAvKipcbiAgICogV2hldGhlciB0aGVyZSBpcyBhbiBhY3RpdmUgY29uc29sZS5cbiAgICovXG4gIGZ1bmN0aW9uIGlzRW5hYmxlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gKFxuICAgICAgdHJhY2tlci5jdXJyZW50V2lkZ2V0ICE9PSBudWxsICYmXG4gICAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgPT09IHNoZWxsLmN1cnJlbnRXaWRnZXRcbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gb3BlbiBhIGNvbnNvbGUuXG4gICAqL1xuICBpbnRlcmZhY2UgSU9wZW5PcHRpb25zIGV4dGVuZHMgUGFydGlhbDxDb25zb2xlUGFuZWwuSU9wdGlvbnM+IHtcbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGFjdGl2YXRlIHRoZSBjb25zb2xlLiAgRGVmYXVsdHMgdG8gYHRydWVgLlxuICAgICAqL1xuICAgIGFjdGl2YXRlPzogYm9vbGVhbjtcbiAgfVxuXG4gIGxldCBjb21tYW5kID0gQ29tbWFuZElEcy5vcGVuO1xuICBjb21tYW5kcy5hZGRDb21tYW5kKGNvbW1hbmQsIHtcbiAgICBleGVjdXRlOiAoYXJnczogSU9wZW5PcHRpb25zKSA9PiB7XG4gICAgICBjb25zdCBwYXRoID0gYXJnc1sncGF0aCddO1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5maW5kKHZhbHVlID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlLmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbj8ucGF0aCA9PT0gcGF0aDtcbiAgICAgIH0pO1xuICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICBpZiAoYXJncy5hY3RpdmF0ZSAhPT0gZmFsc2UpIHtcbiAgICAgICAgICBzaGVsbC5hY3RpdmF0ZUJ5SWQod2lkZ2V0LmlkKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gd2lkZ2V0O1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIG1hbmFnZXIucmVhZHkudGhlbigoKSA9PiB7XG4gICAgICAgICAgY29uc3QgbW9kZWwgPSBmaW5kKG1hbmFnZXIuc2Vzc2lvbnMucnVubmluZygpLCBpdGVtID0+IHtcbiAgICAgICAgICAgIHJldHVybiBpdGVtLnBhdGggPT09IHBhdGg7XG4gICAgICAgICAgfSk7XG4gICAgICAgICAgaWYgKG1vZGVsKSB7XG4gICAgICAgICAgICByZXR1cm4gY3JlYXRlQ29uc29sZShhcmdzKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgcmV0dXJuIFByb21pc2UucmVqZWN0KGBObyBydW5uaW5nIGtlcm5lbCBzZXNzaW9uIGZvciBwYXRoOiAke3BhdGh9YCk7XG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZCA9IENvbW1hbmRJRHMuY3JlYXRlO1xuICBjb21tYW5kcy5hZGRDb21tYW5kKGNvbW1hbmQsIHtcbiAgICBsYWJlbDogYXJncyA9PiB7XG4gICAgICBpZiAoYXJnc1snaXNQYWxldHRlJ10pIHtcbiAgICAgICAgcmV0dXJuIHRyYW5zLl9fKCdOZXcgQ29uc29sZScpO1xuICAgICAgfSBlbHNlIGlmIChhcmdzWydpc0xhdW5jaGVyJ10gJiYgYXJnc1sna2VybmVsUHJlZmVyZW5jZSddKSB7XG4gICAgICAgIGNvbnN0IGtlcm5lbFByZWZlcmVuY2UgPSBhcmdzW1xuICAgICAgICAgICdrZXJuZWxQcmVmZXJlbmNlJ1xuICAgICAgICBdIGFzIElTZXNzaW9uQ29udGV4dC5JS2VybmVsUHJlZmVyZW5jZTtcbiAgICAgICAgLy8gVE9ETzogTHVtaW5vIGNvbW1hbmQgZnVuY3Rpb25zIHNob3VsZCBwcm9iYWJseSBiZSBhbGxvd2VkIHRvIHJldHVybiB1bmRlZmluZWQ/XG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgbWFuYWdlci5rZXJuZWxzcGVjcz8uc3BlY3M/Lmtlcm5lbHNwZWNzW2tlcm5lbFByZWZlcmVuY2UubmFtZSB8fCAnJ11cbiAgICAgICAgICAgID8uZGlzcGxheV9uYW1lID8/ICcnXG4gICAgICAgICk7XG4gICAgICB9XG4gICAgICByZXR1cm4gdHJhbnMuX18oJ0NvbnNvbGUnKTtcbiAgICB9LFxuICAgIGljb246IGFyZ3MgPT4gKGFyZ3NbJ2lzUGFsZXR0ZSddID8gdW5kZWZpbmVkIDogY29uc29sZUljb24pLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgYmFzZVBhdGggPVxuICAgICAgICAoKGFyZ3NbJ2Jhc2VQYXRoJ10gYXMgc3RyaW5nKSB8fFxuICAgICAgICAgIChhcmdzWydjd2QnXSBhcyBzdHJpbmcpIHx8XG4gICAgICAgICAgYnJvd3NlckZhY3Rvcnk/LmRlZmF1bHRCcm93c2VyLm1vZGVsLnBhdGgpID8/XG4gICAgICAgICcnO1xuICAgICAgcmV0dXJuIGNyZWF0ZUNvbnNvbGUoeyBiYXNlUGF0aCwgLi4uYXJncyB9KTtcbiAgICB9XG4gIH0pO1xuXG4gIC8vIEdldCB0aGUgY3VycmVudCB3aWRnZXQgYW5kIGFjdGl2YXRlIHVubGVzcyB0aGUgYXJncyBzcGVjaWZ5IG90aGVyd2lzZS5cbiAgZnVuY3Rpb24gZ2V0Q3VycmVudChhcmdzOiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0KTogQ29uc29sZVBhbmVsIHwgbnVsbCB7XG4gICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgIGNvbnN0IGFjdGl2YXRlID0gYXJnc1snYWN0aXZhdGUnXSAhPT0gZmFsc2U7XG4gICAgaWYgKGFjdGl2YXRlICYmIHdpZGdldCkge1xuICAgICAgc2hlbGwuYWN0aXZhdGVCeUlkKHdpZGdldC5pZCk7XG4gICAgfVxuICAgIHJldHVybiB3aWRnZXQgPz8gbnVsbDtcbiAgfVxuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jbGVhciwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnQ2xlYXIgQ29uc29sZSBDZWxscycpLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgY3VycmVudCA9IGdldEN1cnJlbnQoYXJncyk7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY3VycmVudC5jb25zb2xlLmNsZWFyKCk7XG4gICAgfSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJ1blVuZm9yY2VkLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSdW4gQ2VsbCAodW5mb3JjZWQpJyksXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBjdXJyZW50ID0gZ2V0Q3VycmVudChhcmdzKTtcbiAgICAgIGlmICghY3VycmVudCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICByZXR1cm4gY3VycmVudC5jb25zb2xlLmV4ZWN1dGUoKTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucnVuRm9yY2VkLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSdW4gQ2VsbCAoZm9yY2VkKScpLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgY3VycmVudCA9IGdldEN1cnJlbnQoYXJncyk7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgcmV0dXJuIGN1cnJlbnQuY29uc29sZS5leGVjdXRlKHRydWUpO1xuICAgIH0sXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5saW5lYnJlYWssIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0luc2VydCBMaW5lIEJyZWFrJyksXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBjdXJyZW50ID0gZ2V0Q3VycmVudChhcmdzKTtcbiAgICAgIGlmICghY3VycmVudCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBjdXJyZW50LmNvbnNvbGUuaW5zZXJ0TGluZWJyZWFrKCk7XG4gICAgfSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJlcGxhY2VTZWxlY3Rpb24sIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1JlcGxhY2UgU2VsZWN0aW9uIGluIENvbnNvbGUnKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSBnZXRDdXJyZW50KGFyZ3MpO1xuICAgICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IHRleHQ6IHN0cmluZyA9IChhcmdzWyd0ZXh0J10gYXMgc3RyaW5nKSB8fCAnJztcbiAgICAgIGN1cnJlbnQuY29uc29sZS5yZXBsYWNlU2VsZWN0aW9uKHRleHQpO1xuICAgIH0sXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5pbnRlcnJ1cHQsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0ludGVycnVwdCBLZXJuZWwnKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSBnZXRDdXJyZW50KGFyZ3MpO1xuICAgICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGtlcm5lbCA9IGN1cnJlbnQuY29uc29sZS5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw7XG4gICAgICBpZiAoa2VybmVsKSB7XG4gICAgICAgIHJldHVybiBrZXJuZWwuaW50ZXJydXB0KCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJlc3RhcnQsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Jlc3RhcnQgS2VybmVs4oCmJyksXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBjdXJyZW50ID0gZ2V0Q3VycmVudChhcmdzKTtcbiAgICAgIGlmICghY3VycmVudCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICByZXR1cm4gc2Vzc2lvbkRpYWxvZ3MhLnJlc3RhcnQoXG4gICAgICAgIGN1cnJlbnQuY29uc29sZS5zZXNzaW9uQ29udGV4dCxcbiAgICAgICAgdHJhbnNsYXRvclxuICAgICAgKTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY2xvc2VBbmRTaHV0ZG93biwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnQ2xvc2UgYW5kIFNodXQgRG93buKApicpLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgY3VycmVudCA9IGdldEN1cnJlbnQoYXJncyk7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICB0aXRsZTogdHJhbnMuX18oJ1NodXQgZG93biB0aGUgY29uc29sZT8nKSxcbiAgICAgICAgYm9keTogdHJhbnMuX18oXG4gICAgICAgICAgJ0FyZSB5b3Ugc3VyZSB5b3Ugd2FudCB0byBjbG9zZSBcIiUxXCI/JyxcbiAgICAgICAgICBjdXJyZW50LnRpdGxlLmxhYmVsXG4gICAgICAgICksXG4gICAgICAgIGJ1dHRvbnM6IFtEaWFsb2cuY2FuY2VsQnV0dG9uKCksIERpYWxvZy53YXJuQnV0dG9uKCldXG4gICAgICB9KS50aGVuKHJlc3VsdCA9PiB7XG4gICAgICAgIGlmIChyZXN1bHQuYnV0dG9uLmFjY2VwdCkge1xuICAgICAgICAgIHJldHVybiBjdXJyZW50LmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQuc2h1dGRvd24oKS50aGVuKCgpID0+IHtcbiAgICAgICAgICAgIGN1cnJlbnQuZGlzcG9zZSgpO1xuICAgICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgICAgfSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaW5qZWN0LCB7XG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBwYXRoID0gYXJnc1sncGF0aCddO1xuICAgICAgdHJhY2tlci5maW5kKHdpZGdldCA9PiB7XG4gICAgICAgIGlmICh3aWRnZXQuY29uc29sZS5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5wYXRoID09PSBwYXRoKSB7XG4gICAgICAgICAgaWYgKGFyZ3NbJ2FjdGl2YXRlJ10gIT09IGZhbHNlKSB7XG4gICAgICAgICAgICBzaGVsbC5hY3RpdmF0ZUJ5SWQod2lkZ2V0LmlkKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgdm9pZCB3aWRnZXQuY29uc29sZS5pbmplY3QoXG4gICAgICAgICAgICBhcmdzWydjb2RlJ10gYXMgc3RyaW5nLFxuICAgICAgICAgICAgYXJnc1snbWV0YWRhdGEnXSBhcyBKU09OT2JqZWN0XG4gICAgICAgICAgKTtcbiAgICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICB9KTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY2hhbmdlS2VybmVsLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdDaGFuZ2UgS2VybmVs4oCmJyksXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBjdXJyZW50ID0gZ2V0Q3VycmVudChhcmdzKTtcbiAgICAgIGlmICghY3VycmVudCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICByZXR1cm4gc2Vzc2lvbkRpYWxvZ3MhLnNlbGVjdEtlcm5lbChcbiAgICAgICAgY3VycmVudC5jb25zb2xlLnNlc3Npb25Db250ZXh0LFxuICAgICAgICB0cmFuc2xhdG9yXG4gICAgICApO1xuICAgIH0sXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGlmIChwYWxldHRlKSB7XG4gICAgLy8gQWRkIGNvbW1hbmQgcGFsZXR0ZSBpdGVtc1xuICAgIFtcbiAgICAgIENvbW1hbmRJRHMuY3JlYXRlLFxuICAgICAgQ29tbWFuZElEcy5saW5lYnJlYWssXG4gICAgICBDb21tYW5kSURzLmNsZWFyLFxuICAgICAgQ29tbWFuZElEcy5ydW5VbmZvcmNlZCxcbiAgICAgIENvbW1hbmRJRHMucnVuRm9yY2VkLFxuICAgICAgQ29tbWFuZElEcy5yZXN0YXJ0LFxuICAgICAgQ29tbWFuZElEcy5pbnRlcnJ1cHQsXG4gICAgICBDb21tYW5kSURzLmNoYW5nZUtlcm5lbCxcbiAgICAgIENvbW1hbmRJRHMuY2xvc2VBbmRTaHV0ZG93blxuICAgIF0uZm9yRWFjaChjb21tYW5kID0+IHtcbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNvbW1hbmQsIGNhdGVnb3J5LCBhcmdzOiB7IGlzUGFsZXR0ZTogdHJ1ZSB9IH0pO1xuICAgIH0pO1xuICB9XG5cbiAgaWYgKG1haW5NZW51KSB7XG4gICAgLy8gQWRkIGEgY2xvc2UgYW5kIHNodXRkb3duIGNvbW1hbmQgdG8gdGhlIGZpbGUgbWVudS5cbiAgICBtYWluTWVudS5maWxlTWVudS5jbG9zZUFuZENsZWFuZXJzLmFkZCh7XG4gICAgICB0cmFja2VyLFxuICAgICAgY2xvc2VBbmRDbGVhbnVwTGFiZWw6IChuOiBudW1iZXIpID0+IHRyYW5zLl9fKCdTaHV0ZG93biBDb25zb2xlJyksXG4gICAgICBjbG9zZUFuZENsZWFudXA6IChjdXJyZW50OiBDb25zb2xlUGFuZWwpID0+IHtcbiAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnU2h1dCBkb3duIHRoZSBDb25zb2xlPycpLFxuICAgICAgICAgIGJvZHk6IHRyYW5zLl9fKFxuICAgICAgICAgICAgJ0FyZSB5b3Ugc3VyZSB5b3Ugd2FudCB0byBjbG9zZSBcIiUxXCI/JyxcbiAgICAgICAgICAgIGN1cnJlbnQudGl0bGUubGFiZWxcbiAgICAgICAgICApLFxuICAgICAgICAgIGJ1dHRvbnM6IFtEaWFsb2cuY2FuY2VsQnV0dG9uKCksIERpYWxvZy53YXJuQnV0dG9uKCldXG4gICAgICAgIH0pLnRoZW4ocmVzdWx0ID0+IHtcbiAgICAgICAgICBpZiAocmVzdWx0LmJ1dHRvbi5hY2NlcHQpIHtcbiAgICAgICAgICAgIHJldHVybiBjdXJyZW50LmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQuc2h1dGRvd24oKS50aGVuKCgpID0+IHtcbiAgICAgICAgICAgICAgY3VycmVudC5kaXNwb3NlKCk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgcmV0dXJuIHZvaWQgMDtcbiAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0gYXMgSUZpbGVNZW51LklDbG9zZUFuZENsZWFuZXI8Q29uc29sZVBhbmVsPik7XG5cbiAgICAvLyBBZGQgYSBrZXJuZWwgdXNlciB0byB0aGUgS2VybmVsIG1lbnVcbiAgICBtYWluTWVudS5rZXJuZWxNZW51Lmtlcm5lbFVzZXJzLmFkZCh7XG4gICAgICB0cmFja2VyLFxuICAgICAgcmVzdGFydEtlcm5lbEFuZENsZWFyTGFiZWw6IG4gPT5cbiAgICAgICAgdHJhbnMuX18oJ1Jlc3RhcnQgS2VybmVsIGFuZCBDbGVhciBDb25zb2xlJyksXG4gICAgICBpbnRlcnJ1cHRLZXJuZWw6IGN1cnJlbnQgPT4ge1xuICAgICAgICBjb25zdCBrZXJuZWwgPSBjdXJyZW50LmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbj8ua2VybmVsO1xuICAgICAgICBpZiAoa2VybmVsKSB7XG4gICAgICAgICAgcmV0dXJuIGtlcm5lbC5pbnRlcnJ1cHQoKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKHZvaWQgMCk7XG4gICAgICB9LFxuICAgICAgcmVzdGFydEtlcm5lbDogY3VycmVudCA9PlxuICAgICAgICBzZXNzaW9uRGlhbG9ncyEucmVzdGFydChjdXJyZW50LmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQsIHRyYW5zbGF0b3IpLFxuICAgICAgcmVzdGFydEtlcm5lbEFuZENsZWFyOiBjdXJyZW50ID0+IHtcbiAgICAgICAgcmV0dXJuIHNlc3Npb25EaWFsb2dzIVxuICAgICAgICAgIC5yZXN0YXJ0KGN1cnJlbnQuY29uc29sZS5zZXNzaW9uQ29udGV4dClcbiAgICAgICAgICAudGhlbihyZXN0YXJ0ZWQgPT4ge1xuICAgICAgICAgICAgaWYgKHJlc3RhcnRlZCkge1xuICAgICAgICAgICAgICBjdXJyZW50LmNvbnNvbGUuY2xlYXIoKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHJldHVybiByZXN0YXJ0ZWQ7XG4gICAgICAgICAgfSk7XG4gICAgICB9LFxuICAgICAgY2hhbmdlS2VybmVsOiBjdXJyZW50ID0+XG4gICAgICAgIHNlc3Npb25EaWFsb2dzIS5zZWxlY3RLZXJuZWwoXG4gICAgICAgICAgY3VycmVudC5jb25zb2xlLnNlc3Npb25Db250ZXh0LFxuICAgICAgICAgIHRyYW5zbGF0b3JcbiAgICAgICAgKSxcbiAgICAgIHNodXRkb3duS2VybmVsOiBjdXJyZW50ID0+IGN1cnJlbnQuY29uc29sZS5zZXNzaW9uQ29udGV4dC5zaHV0ZG93bigpXG4gICAgfSBhcyBJS2VybmVsTWVudS5JS2VybmVsVXNlcjxDb25zb2xlUGFuZWw+KTtcblxuICAgIC8vIEFkZCBhIGNvZGUgcnVubmVyIHRvIHRoZSBSdW4gbWVudS5cbiAgICBtYWluTWVudS5ydW5NZW51LmNvZGVSdW5uZXJzLmFkZCh7XG4gICAgICB0cmFja2VyLFxuICAgICAgcnVuTGFiZWw6IChuOiBudW1iZXIpID0+IHRyYW5zLl9fKCdSdW4gQ2VsbCcpLFxuICAgICAgcnVuOiBjdXJyZW50ID0+IGN1cnJlbnQuY29uc29sZS5leGVjdXRlKHRydWUpXG4gICAgfSBhcyBJUnVuTWVudS5JQ29kZVJ1bm5lcjxDb25zb2xlUGFuZWw+KTtcblxuICAgIC8vIEFkZCBhIGNsZWFyZXIgdG8gdGhlIGVkaXQgbWVudVxuICAgIG1haW5NZW51LmVkaXRNZW51LmNsZWFyZXJzLmFkZCh7XG4gICAgICB0cmFja2VyLFxuICAgICAgY2xlYXJDdXJyZW50TGFiZWw6IChuOiBudW1iZXIpID0+IHRyYW5zLl9fKCdDbGVhciBDb25zb2xlIENlbGwnKSxcbiAgICAgIGNsZWFyQ3VycmVudDogKGN1cnJlbnQ6IENvbnNvbGVQYW5lbCkgPT4ge1xuICAgICAgICByZXR1cm4gY3VycmVudC5jb25zb2xlLmNsZWFyKCk7XG4gICAgICB9XG4gICAgfSBhcyBJRWRpdE1lbnUuSUNsZWFyZXI8Q29uc29sZVBhbmVsPik7XG4gIH1cblxuICAvLyBGb3IgYmFja3dhcmRzIGNvbXBhdGliaWxpdHkgYW5kIGNsYXJpdHksIHdlIGV4cGxpY2l0bHkgbGFiZWwgdGhlIHJ1blxuICAvLyBrZXlzdHJva2Ugd2l0aCB0aGUgYWN0dWFsIGVmZmVjdGVkIGNoYW5nZSwgcmF0aGVyIHRoYW4gdGhlIGdlbmVyaWNcbiAgLy8gXCJub3RlYm9va1wiIG9yIFwidGVybWluYWxcIiBpbnRlcmFjdGlvbiBtb2RlLiBXaGVuIHRoaXMgaW50ZXJhY3Rpb24gbW9kZVxuICAvLyBhZmZlY3RzIG1vcmUgdGhhbiBqdXN0IHRoZSBydW4ga2V5c3Ryb2tlLCB3ZSBjYW4gbWFrZSB0aGlzIG1lbnUgdGl0bGUgbW9yZVxuICAvLyBnZW5lcmljLlxuICBjb25zdCBydW5TaG9ydGN1dFRpdGxlczogeyBbaW5kZXg6IHN0cmluZ106IHN0cmluZyB9ID0ge1xuICAgIG5vdGVib29rOiB0cmFucy5fXygnRXhlY3V0ZSB3aXRoIFNoaWZ0K0VudGVyJyksXG4gICAgdGVybWluYWw6IHRyYW5zLl9fKCdFeGVjdXRlIHdpdGggRW50ZXInKVxuICB9O1xuXG4gIC8vIEFkZCB0aGUgZXhlY3V0ZSBrZXlzdHJva2Ugc2V0dGluZyBzdWJtZW51LlxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaW50ZXJhY3Rpb25Nb2RlLCB7XG4gICAgbGFiZWw6IGFyZ3MgPT4gcnVuU2hvcnRjdXRUaXRsZXNbYXJnc1snaW50ZXJhY3Rpb25Nb2RlJ10gYXMgc3RyaW5nXSB8fCAnJyxcbiAgICBleGVjdXRlOiBhc3luYyBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGtleSA9ICdrZXlNYXAnO1xuICAgICAgdHJ5IHtcbiAgICAgICAgYXdhaXQgc2V0dGluZ1JlZ2lzdHJ5LnNldChcbiAgICAgICAgICBwbHVnaW5JZCxcbiAgICAgICAgICAnaW50ZXJhY3Rpb25Nb2RlJyxcbiAgICAgICAgICBhcmdzWydpbnRlcmFjdGlvbk1vZGUnXSBhcyBzdHJpbmdcbiAgICAgICAgKTtcbiAgICAgIH0gY2F0Y2ggKHJlYXNvbikge1xuICAgICAgICBjb25zb2xlLmVycm9yKGBGYWlsZWQgdG8gc2V0ICR7cGx1Z2luSWR9OiR7a2V5fSAtICR7cmVhc29uLm1lc3NhZ2V9YCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc1RvZ2dsZWQ6IGFyZ3MgPT4gYXJnc1snaW50ZXJhY3Rpb25Nb2RlJ10gPT09IGludGVyYWN0aW9uTW9kZVxuICB9KTtcblxuICBpZiAobWFpbk1lbnUpIHtcbiAgICAvLyBBZGQga2VybmVsIGluZm9ybWF0aW9uIHRvIHRoZSBhcHBsaWNhdGlvbiBoZWxwIG1lbnUuXG4gICAgbWFpbk1lbnUuaGVscE1lbnUua2VybmVsVXNlcnMuYWRkKHtcbiAgICAgIHRyYWNrZXIsXG4gICAgICBnZXRLZXJuZWw6IGN1cnJlbnQgPT4gY3VycmVudC5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWxcbiAgICB9IGFzIElIZWxwTWVudS5JS2VybmVsVXNlcjxDb25zb2xlUGFuZWw+KTtcbiAgfVxuXG4gIHJldHVybiB0cmFja2VyO1xufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==