(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_apputils-extension_lib_index_js"],{

/***/ "../packages/apputils-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/apputils-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "toggleHeader": () => (/* binding */ toggleHeader),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/polling */ "webpack/sharing/consume/default/@lumino/polling/@lumino/polling");
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_polling__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _palette__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./palette */ "../packages/apputils-extension/lib/palette.js");
/* harmony import */ var _settingsplugin__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./settingsplugin */ "../packages/apputils-extension/lib/settingsplugin.js");
/* harmony import */ var _themesplugins__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./themesplugins */ "../packages/apputils-extension/lib/themesplugins.js");
/* harmony import */ var _workspacesplugin__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./workspacesplugin */ "../packages/apputils-extension/lib/workspacesplugin.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module apputils-extension
 */














/**
 * The interval in milliseconds before recover options appear during splash.
 */
const SPLASH_RECOVER_TIMEOUT = 12000;
/**
 * The command IDs used by the apputils plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.loadState = 'apputils:load-statedb';
    CommandIDs.print = 'apputils:print';
    CommandIDs.reset = 'apputils:reset';
    CommandIDs.resetOnLoad = 'apputils:reset-on-load';
    CommandIDs.runFirstEnabled = 'apputils:run-first-enabled';
    CommandIDs.runAllEnabled = 'apputils:run-all-enabled';
    CommandIDs.toggleHeader = 'apputils:toggle-header';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default command palette extension.
 */
const palette = {
    id: '@jupyterlab/apputils-extension:palette',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    provides: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    activate: (app, translator, settingRegistry) => {
        return _palette__WEBPACK_IMPORTED_MODULE_10__.Palette.activate(app, translator, settingRegistry);
    }
};
/**
 * The default command palette's restoration extension.
 *
 * #### Notes
 * The command palette's restoration logic is handled separately from the
 * command palette provider extension because the layout restorer dependency
 * causes the command palette to be unavailable to other extensions earlier
 * in the application load cycle.
 */
const paletteRestorer = {
    id: '@jupyterlab/apputils-extension:palette-restorer',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    activate: (app, restorer, translator) => {
        _palette__WEBPACK_IMPORTED_MODULE_10__.Palette.restore(app, restorer, translator);
    }
};
/**
 * The default window name resolver provider.
 */
const resolver = {
    id: '@jupyterlab/apputils-extension:resolver',
    autoStart: true,
    provides: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IWindowResolver,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter],
    activate: async (app, paths, router) => {
        const { hash, search } = router.current;
        const query = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.queryStringToObject(search || '');
        const solver = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WindowResolver();
        const workspace = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('workspace');
        const treePath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('treePath');
        const mode = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('mode') === 'multiple-document' ? 'lab' : 'doc';
        // This is used as a key in local storage to refer to workspaces, either the name
        // of the workspace or the string PageConfig.defaultWorkspace. Both lab and doc modes share the same workspace.
        const candidate = workspace ? workspace : _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.defaultWorkspace;
        const rest = treePath ? _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join('tree', treePath) : '';
        try {
            await solver.resolve(candidate);
            return solver;
        }
        catch (error) {
            // Window resolution has failed so the URL must change. Return a promise
            // that never resolves to prevent the application from loading plugins
            // that rely on `IWindowResolver`.
            return new Promise(() => {
                const { base } = paths.urls;
                const pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
                const random = pool[Math.floor(Math.random() * pool.length)];
                let path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(base, mode, 'workspaces', `auto-${random}`);
                path = rest ? _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(path, _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.encodeParts(rest)) : path;
                // Reset the workspace on load.
                query['reset'] = '';
                const url = path + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.objectToQueryString(query) + (hash || '');
                router.navigate(url, { hard: true });
            });
        }
    }
};
/**
 * The default splash screen provider.
 */
const splash = {
    id: '@jupyterlab/apputils-extension:splash',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    provides: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISplashScreen,
    activate: (app, translator) => {
        const trans = translator.load('jupyterlab');
        const { commands, restored } = app;
        // Create splash element and populate it.
        const splash = document.createElement('div');
        const galaxy = document.createElement('div');
        const logo = document.createElement('div');
        splash.id = 'jupyterlab-splash';
        galaxy.id = 'galaxy';
        logo.id = 'main-logo';
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.jupyterFaviconIcon.element({
            container: logo,
            stylesheet: 'splash'
        });
        galaxy.appendChild(logo);
        ['1', '2', '3'].forEach(id => {
            const moon = document.createElement('div');
            const planet = document.createElement('div');
            moon.id = `moon${id}`;
            moon.className = 'moon orbit';
            planet.id = `planet${id}`;
            planet.className = 'planet';
            moon.appendChild(planet);
            galaxy.appendChild(moon);
        });
        splash.appendChild(galaxy);
        // Create debounced recovery dialog function.
        let dialog;
        const recovery = new _lumino_polling__WEBPACK_IMPORTED_MODULE_9__.Throttler(async () => {
            if (dialog) {
                return;
            }
            dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog({
                title: trans.__('Loading…'),
                body: trans.__(`The loading screen is taking a long time.
Would you like to clear the workspace or keep waiting?`),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Keep Waiting') }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Clear Workspace') })
                ]
            });
            try {
                const result = await dialog.launch();
                dialog.dispose();
                dialog = null;
                if (result.button.accept && commands.hasCommand(CommandIDs.reset)) {
                    return commands.execute(CommandIDs.reset);
                }
                // Re-invoke the recovery timer in the next frame.
                requestAnimationFrame(() => {
                    // Because recovery can be stopped, handle invocation rejection.
                    void recovery.invoke().catch(_ => undefined);
                });
            }
            catch (error) {
                /* no-op */
            }
        }, { limit: SPLASH_RECOVER_TIMEOUT, edge: 'trailing' });
        // Return ISplashScreen.
        let splashCount = 0;
        return {
            show: (light = true) => {
                splash.classList.remove('splash-fade');
                splash.classList.toggle('light', light);
                splash.classList.toggle('dark', !light);
                splashCount++;
                document.body.appendChild(splash);
                // Because recovery can be stopped, handle invocation rejection.
                void recovery.invoke().catch(_ => undefined);
                return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_8__.DisposableDelegate(async () => {
                    await restored;
                    if (--splashCount === 0) {
                        void recovery.stop();
                        if (dialog) {
                            dialog.dispose();
                            dialog = null;
                        }
                        splash.classList.add('splash-fade');
                        window.setTimeout(() => {
                            document.body.removeChild(splash);
                        }, 200);
                    }
                });
            }
        };
    }
};
const print = {
    id: '@jupyterlab/apputils-extension:print',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    activate: (app, translator) => {
        const trans = translator.load('jupyterlab');
        app.commands.addCommand(CommandIDs.print, {
            label: trans.__('Print…'),
            isEnabled: () => {
                const widget = app.shell.currentWidget;
                return _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Printing.getPrintFunction(widget) !== null;
            },
            execute: async () => {
                const widget = app.shell.currentWidget;
                const printFunction = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Printing.getPrintFunction(widget);
                if (printFunction) {
                    await printFunction();
                }
            }
        });
    }
};
const toggleHeader = {
    id: '@jupyterlab/apputils-extension:toggle-header',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, palette) => {
        const trans = translator.load('jupyterlab');
        const category = trans.__('Main Area');
        app.commands.addCommand(CommandIDs.toggleHeader, {
            label: trans.__('Show Header Above Content'),
            isEnabled: () => app.shell.currentWidget instanceof _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget &&
                app.shell.currentWidget.contentHeader.widgets.length > 0,
            isToggled: () => {
                const widget = app.shell.currentWidget;
                return widget instanceof _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget
                    ? !widget.contentHeader.isHidden
                    : false;
            },
            execute: async () => {
                const widget = app.shell.currentWidget;
                if (widget instanceof _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget) {
                    widget.contentHeader.setHidden(!widget.contentHeader.isHidden);
                }
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.toggleHeader, category });
        }
    }
};
/**
 * Update the browser title based on the workspace and the current
 * active item.
 */
async function updateTabTitle(workspace, db, name) {
    var _a, _b;
    const data = await db.toJSON();
    let current = (_b = (_a = data['layout-restorer:data']) === null || _a === void 0 ? void 0 : _a.main) === null || _b === void 0 ? void 0 : _b.current;
    if (current === undefined) {
        document.title = `${_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('appName') || 'JupyterLab'}${workspace.startsWith('auto-') ? ` (${workspace})` : ``}`;
    }
    else {
        // File name from current path
        let currentFile = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.basename(current.split(':')[1]);
        // Truncate to first 12 characters of current document name + ... if length > 15
        currentFile =
            currentFile.length > 15
                ? currentFile.slice(0, 12).concat(`…`)
                : currentFile;
        // Number of restorable items that are either notebooks or editors
        const count = Object.keys(data).filter(item => item.startsWith('notebook') || item.startsWith('editor')).length;
        if (workspace.startsWith('auto-')) {
            document.title = `${currentFile} (${workspace}${count > 1 ? ` : ${count}` : ``}) - ${name}`;
        }
        else {
            document.title = `${currentFile}${count > 1 ? ` (${count})` : ``} - ${name}`;
        }
    }
}
/**
 * The default state database for storing application state.
 *
 * #### Notes
 * If this extension is loaded with a window resolver, it will automatically add
 * state management commands, URL support for `clone` and `reset`, and workspace
 * auto-saving. Otherwise, it will return a simple in-memory state database.
 */
const state = {
    id: '@jupyterlab/apputils-extension:state',
    autoStart: true,
    provides: _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__.IStateDB,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IWindowResolver],
    activate: (app, paths, router, translator, resolver) => {
        const trans = translator.load('jupyterlab');
        if (resolver === null) {
            return new _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__.StateDB();
        }
        let resolved = false;
        const { commands, name, serviceManager } = app;
        const { workspaces } = serviceManager;
        const workspace = resolver.name;
        const transform = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_7__.PromiseDelegate();
        const db = new _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__.StateDB({ transform: transform.promise });
        const save = new _lumino_polling__WEBPACK_IMPORTED_MODULE_9__.Debouncer(async () => {
            const id = workspace;
            const metadata = { id };
            const data = await db.toJSON();
            await workspaces.save(id, { data, metadata });
        });
        // Any time the local state database changes, save the workspace.
        db.changed.connect(() => void save.invoke(), db);
        db.changed.connect(() => updateTabTitle(workspace, db, name));
        commands.addCommand(CommandIDs.loadState, {
            execute: async (args) => {
                // Since the command can be executed an arbitrary number of times, make
                // sure it is safe to call multiple times.
                if (resolved) {
                    return;
                }
                const { hash, path, search } = args;
                const { urls } = paths;
                const query = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.queryStringToObject(search || '');
                const clone = typeof query['clone'] === 'string'
                    ? query['clone'] === ''
                        ? _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(urls.base, urls.app)
                        : _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(urls.base, urls.app, 'workspaces', query['clone'])
                    : null;
                const source = clone || workspace || null;
                if (source === null) {
                    console.error(`${CommandIDs.loadState} cannot load null workspace.`);
                    return;
                }
                try {
                    const saved = await workspaces.fetch(source);
                    // If this command is called after a reset, the state database
                    // will already be resolved.
                    if (!resolved) {
                        resolved = true;
                        transform.resolve({ type: 'overwrite', contents: saved.data });
                    }
                }
                catch ({ message }) {
                    console.warn(`Fetching workspace "${workspace}" failed.`, message);
                    // If the workspace does not exist, cancel the data transformation
                    // and save a workspace with the current user state data.
                    if (!resolved) {
                        resolved = true;
                        transform.resolve({ type: 'cancel', contents: null });
                    }
                }
                if (source === clone) {
                    // Maintain the query string parameters but remove `clone`.
                    delete query['clone'];
                    const url = path + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.objectToQueryString(query) + hash;
                    const cloned = save.invoke().then(() => router.stop);
                    // After the state has been cloned, navigate to the URL.
                    void cloned.then(() => {
                        router.navigate(url);
                    });
                    return cloned;
                }
                // After the state database has finished loading, save it.
                await save.invoke();
            }
        });
        commands.addCommand(CommandIDs.reset, {
            label: trans.__('Reset Application State'),
            execute: async ({ reload }) => {
                await db.clear();
                await save.invoke();
                if (reload) {
                    router.reload();
                }
            }
        });
        commands.addCommand(CommandIDs.resetOnLoad, {
            execute: (args) => {
                const { hash, path, search } = args;
                const query = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.queryStringToObject(search || '');
                const reset = 'reset' in query;
                const clone = 'clone' in query;
                if (!reset) {
                    return;
                }
                // If the state database has already been resolved, resetting is
                // impossible without reloading.
                if (resolved) {
                    return router.reload();
                }
                // Empty the state database.
                resolved = true;
                transform.resolve({ type: 'clear', contents: null });
                // Maintain the query string parameters but remove `reset`.
                delete query['reset'];
                const url = path + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.objectToQueryString(query) + hash;
                const cleared = db.clear().then(() => save.invoke());
                // After the state has been reset, navigate to the URL.
                if (clone) {
                    void cleared.then(() => {
                        router.navigate(url, { hard: true });
                    });
                }
                else {
                    void cleared.then(() => {
                        router.navigate(url);
                    });
                }
                return cleared;
            }
        });
        router.register({
            command: CommandIDs.loadState,
            pattern: /.?/,
            rank: 30 // High priority: 30:100.
        });
        router.register({
            command: CommandIDs.resetOnLoad,
            pattern: /(\?reset|\&reset)($|&)/,
            rank: 20 // High priority: 20:100.
        });
        return db;
    }
};
/**
 * The default session context dialogs extension.
 */
const sessionDialogs = {
    id: '@jupyterlab/apputils-extension:sessionDialogs',
    provides: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs,
    autoStart: true,
    activate: () => {
        return _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.sessionContextDialogs;
    }
};
/**
 * Utility commands
 */
const utilityCommands = {
    id: '@jupyterlab/apputils-extension:utilityCommands',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    autoStart: true,
    activate: (app, translator) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        commands.addCommand(CommandIDs.runFirstEnabled, {
            label: trans.__('Run First Enabled Command'),
            execute: args => {
                const commands = args.commands;
                const commandArgs = args.args;
                const argList = Array.isArray(args);
                for (let i = 0; i < commands.length; i++) {
                    const cmd = commands[i];
                    const arg = argList ? commandArgs[i] : commandArgs;
                    if (app.commands.isEnabled(cmd, arg)) {
                        return app.commands.execute(cmd, arg);
                    }
                }
            }
        });
        commands.addCommand(CommandIDs.runAllEnabled, {
            label: trans.__('Run All Enabled Commands Passed as Args'),
            execute: async (args) => {
                const commands = args.commands;
                const commandArgs = args.args;
                const argList = Array.isArray(args);
                const errorIfNotEnabled = args.errorIfNotEnabled;
                for (let i = 0; i < commands.length; i++) {
                    const cmd = commands[i];
                    const arg = argList ? commandArgs[i] : commandArgs;
                    if (app.commands.isEnabled(cmd, arg)) {
                        await app.commands.execute(cmd, arg);
                    }
                    else {
                        if (errorIfNotEnabled) {
                            console.error(`${cmd} is not enabled.`);
                        }
                    }
                }
            }
        });
    }
};
/**
 * The default HTML sanitizer.
 */
const sanitizer = {
    id: '@jupyter/apputils-extension:sanitizer',
    autoStart: true,
    provides: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISanitizer,
    activate: () => {
        return _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.defaultSanitizer;
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    palette,
    paletteRestorer,
    print,
    resolver,
    sanitizer,
    _settingsplugin__WEBPACK_IMPORTED_MODULE_11__.settingsPlugin,
    state,
    splash,
    sessionDialogs,
    _themesplugins__WEBPACK_IMPORTED_MODULE_12__.themesPlugin,
    _themesplugins__WEBPACK_IMPORTED_MODULE_12__.themesPaletteMenuPlugin,
    toggleHeader,
    utilityCommands,
    _workspacesplugin__WEBPACK_IMPORTED_MODULE_13__.workspacesPlugin
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "../packages/apputils-extension/lib/palette.js":
/*!*****************************************************!*\
  !*** ../packages/apputils-extension/lib/palette.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Palette": () => (/* binding */ Palette)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands/@lumino/commands");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_commands__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/







/**
 * The command IDs used by the apputils extension.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.activate = 'apputils:activate-command-palette';
})(CommandIDs || (CommandIDs = {}));
const PALETTE_PLUGIN_ID = '@jupyterlab/apputils-extension:palette';
/**
 * A thin wrapper around the `CommandPalette` class to conform with the
 * JupyterLab interface for the application-wide command palette.
 */
class Palette {
    /**
     * Create a palette instance.
     */
    constructor(palette, translator) {
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = this.translator.load('jupyterlab');
        this._palette = palette;
        this._palette.title.label = '';
        this._palette.title.caption = trans.__('Command Palette');
    }
    /**
     * The placeholder text of the command palette's search input.
     */
    set placeholder(placeholder) {
        this._palette.inputNode.placeholder = placeholder;
    }
    get placeholder() {
        return this._palette.inputNode.placeholder;
    }
    /**
     * Activate the command palette for user input.
     */
    activate() {
        this._palette.activate();
    }
    /**
     * Add a command item to the command palette.
     *
     * @param options - The options for creating the command item.
     *
     * @returns A disposable that will remove the item from the palette.
     */
    addItem(options) {
        const item = this._palette.addItem(options);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_5__.DisposableDelegate(() => {
            this._palette.removeItem(item);
        });
    }
}
/**
 * A namespace for `Palette` statics.
 */
(function (Palette) {
    /**
     * Activate the command palette.
     */
    function activate(app, translator, settingRegistry) {
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const palette = Private.createPalette(app, translator);
        const modalPalette = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ModalCommandPalette({ commandPalette: palette });
        let modal = false;
        palette.node.setAttribute('role', 'region');
        palette.node.setAttribute('aria-label', trans.__('Command Palette Section'));
        shell.add(palette, 'left', { rank: 300 });
        if (settingRegistry) {
            const loadSettings = settingRegistry.load(PALETTE_PLUGIN_ID);
            const updateSettings = (settings) => {
                const newModal = settings.get('modal').composite;
                if (modal && !newModal) {
                    palette.parent = null;
                    modalPalette.detach();
                    shell.add(palette, 'left', { rank: 300 });
                }
                else if (!modal && newModal) {
                    palette.parent = null;
                    modalPalette.palette = palette;
                    palette.show();
                    modalPalette.attach();
                }
                modal = newModal;
            };
            Promise.all([loadSettings, app.restored])
                .then(([settings]) => {
                updateSettings(settings);
                settings.changed.connect(settings => {
                    updateSettings(settings);
                });
            })
                .catch((reason) => {
                console.error(reason.message);
            });
        }
        // Show the current palette shortcut in its title.
        const updatePaletteTitle = () => {
            const binding = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.find)(app.commands.keyBindings, b => b.command === CommandIDs.activate);
            if (binding) {
                const ks = _lumino_commands__WEBPACK_IMPORTED_MODULE_4__.CommandRegistry.formatKeystroke(binding.keys.join(' '));
                palette.title.caption = trans.__('Commands (%1)', ks);
            }
            else {
                palette.title.caption = trans.__('Commands');
            }
        };
        updatePaletteTitle();
        app.commands.keyBindingChanged.connect(() => {
            updatePaletteTitle();
        });
        commands.addCommand(CommandIDs.activate, {
            execute: () => {
                if (modal) {
                    modalPalette.activate();
                }
                else {
                    shell.activateById(palette.id);
                }
            },
            label: trans.__('Activate Command Palette')
        });
        palette.inputNode.placeholder = trans.__('SEARCH');
        return new Palette(palette, translator);
    }
    Palette.activate = activate;
    /**
     * Restore the command palette.
     */
    function restore(app, restorer, translator) {
        const palette = Private.createPalette(app, translator);
        // Let the application restorer track the command palette for restoration of
        // application state (e.g. setting the command palette as the current side bar
        // widget).
        restorer.add(palette, 'command-palette');
    }
    Palette.restore = restore;
})(Palette || (Palette = {}));
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The private command palette instance.
     */
    let palette;
    /**
     * Create the application-wide command palette.
     */
    function createPalette(app, translator) {
        if (!palette) {
            // use a renderer tweaked to use inline svg icons
            palette = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.CommandPalette({
                commands: app.commands,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.CommandPaletteSvg.defaultRenderer
            });
            palette.id = 'command-palette';
            palette.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.paletteIcon;
            const trans = translator.load('jupyterlab');
            palette.title.label = trans.__('Commands');
        }
        return palette;
    }
    Private.createPalette = createPalette;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/apputils-extension/lib/settingconnector.js":
/*!**************************************************************!*\
  !*** ../packages/apputils-extension/lib/settingconnector.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SettingConnector": () => (/* binding */ SettingConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/polling */ "webpack/sharing/consume/default/@lumino/polling/@lumino/polling");
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_polling__WEBPACK_IMPORTED_MODULE_2__);



/**
 * A data connector for fetching settings.
 *
 * #### Notes
 * This connector adds a query parameter to the base services setting manager.
 */
class SettingConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_1__.DataConnector {
    constructor(connector) {
        super();
        this._throttlers = Object.create(null);
        this._connector = connector;
    }
    /**
     * Fetch settings for a plugin.
     * @param id - The plugin ID
     *
     * #### Notes
     * The REST API requests are throttled at one request per plugin per 100ms.
     */
    fetch(id) {
        const throttlers = this._throttlers;
        if (!(id in throttlers)) {
            throttlers[id] = new _lumino_polling__WEBPACK_IMPORTED_MODULE_2__.Throttler(() => this._connector.fetch(id), 100);
        }
        return throttlers[id].invoke();
    }
    async list(query = 'all') {
        const { isDeferred, isDisabled } = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.Extension;
        const { ids, values } = await this._connector.list();
        if (query === 'all') {
            return { ids, values };
        }
        return {
            ids: ids.filter(id => !isDeferred(id) && !isDisabled(id)),
            values: values.filter(({ id }) => !isDeferred(id) && !isDisabled(id))
        };
    }
    async save(id, raw) {
        await this._connector.save(id, raw);
    }
}


/***/ }),

/***/ "../packages/apputils-extension/lib/settingsplugin.js":
/*!************************************************************!*\
  !*** ../packages/apputils-extension/lib/settingsplugin.js ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "settingsPlugin": () => (/* binding */ settingsPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _settingconnector__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./settingconnector */ "../packages/apputils-extension/lib/settingconnector.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



/**
 * The default setting registry provider.
 */
const settingsPlugin = {
    id: '@jupyterlab/apputils-extension:settings',
    activate: async (app) => {
        const { isDisabled } = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.Extension;
        const connector = new _settingconnector__WEBPACK_IMPORTED_MODULE_2__.SettingConnector(app.serviceManager.settings);
        const registry = new _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.SettingRegistry({
            connector,
            plugins: (await connector.list('active')).values
        });
        // If there are plugins that have schemas that are not in the setting
        // registry after the application has restored, try to load them manually
        // because otherwise, its settings will never become available in the
        // setting registry.
        void app.restored.then(async () => {
            const plugins = await connector.list('all');
            plugins.ids.forEach(async (id, index) => {
                if (isDisabled(id) || id in registry.plugins) {
                    return;
                }
                try {
                    await registry.load(id);
                }
                catch (error) {
                    console.warn(`Settings failed to load for (${id})`, error);
                    if (plugins.values[index].schema['jupyter.lab.transform']) {
                        console.warn(`This may happen if {autoStart: false} in (${id}) ` +
                            `or if it is one of the deferredExtensions in page config.`);
                    }
                }
            });
        });
        return registry;
    },
    autoStart: true,
    provides: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry
};


/***/ }),

/***/ "../packages/apputils-extension/lib/themesplugins.js":
/*!***********************************************************!*\
  !*** ../packages/apputils-extension/lib/themesplugins.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "themesPlugin": () => (/* binding */ themesPlugin),
/* harmony export */   "themesPaletteMenuPlugin": () => (/* binding */ themesPaletteMenuPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/






var CommandIDs;
(function (CommandIDs) {
    CommandIDs.changeTheme = 'apputils:change-theme';
    CommandIDs.themeScrollbars = 'apputils:theme-scrollbars';
    CommandIDs.changeFont = 'apputils:change-font';
    CommandIDs.incrFontSize = 'apputils:incr-font-size';
    CommandIDs.decrFontSize = 'apputils:decr-font-size';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default theme manager provider.
 */
const themesPlugin = {
    id: '@jupyterlab/apputils-extension:themes',
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISplashScreen],
    activate: (app, settings, paths, translator, splash) => {
        const trans = translator.load('jupyterlab');
        const host = app.shell;
        const commands = app.commands;
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getBaseUrl(), paths.urls.themes);
        const key = themesPlugin.id;
        const manager = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ThemeManager({
            key,
            host,
            settings,
            splash: splash !== null && splash !== void 0 ? splash : undefined,
            url
        });
        // Keep a synchronously set reference to the current theme,
        // since the asynchronous setting of the theme in `changeTheme`
        // can lead to an incorrect toggle on the currently used theme.
        let currentTheme;
        manager.themeChanged.connect((sender, args) => {
            // Set data attributes on the application shell for the current theme.
            currentTheme = args.newValue;
            document.body.dataset.jpThemeLight = String(manager.isLight(currentTheme));
            document.body.dataset.jpThemeName = currentTheme;
            if (document.body.dataset.jpThemeScrollbars !==
                String(manager.themeScrollbars(currentTheme))) {
                document.body.dataset.jpThemeScrollbars = String(manager.themeScrollbars(currentTheme));
            }
            commands.notifyCommandChanged(CommandIDs.changeTheme);
        });
        commands.addCommand(CommandIDs.changeTheme, {
            label: args => {
                const theme = args['theme'];
                const displayName = manager.getDisplayName(theme);
                return args['isPalette']
                    ? trans.__('Use Theme: %1', displayName)
                    : displayName;
            },
            isToggled: args => args['theme'] === currentTheme,
            execute: args => {
                const theme = args['theme'];
                if (theme === manager.theme) {
                    return;
                }
                return manager.setTheme(theme);
            }
        });
        commands.addCommand(CommandIDs.themeScrollbars, {
            label: trans.__('Theme Scrollbars'),
            isToggled: () => manager.isToggledThemeScrollbars(),
            execute: () => manager.toggleThemeScrollbars()
        });
        commands.addCommand(CommandIDs.changeFont, {
            label: args => args['enabled'] ? `${args['font']}` : trans.__('waiting for fonts'),
            isEnabled: args => args['enabled'],
            isToggled: args => manager.getCSS(args['key']) === args['font'],
            execute: args => manager.setCSSOverride(args['key'], args['font'])
        });
        commands.addCommand(CommandIDs.incrFontSize, {
            label: args => {
                switch (args.key) {
                    case 'code-font-size':
                        return trans.__('Increase Code Font Size');
                    case 'content-font-size1':
                        return trans.__('Increase Content Font Size');
                    case 'ui-font-size1':
                        return trans.__('Increase UI Font Size');
                    default:
                        return trans.__('Increase Font Size');
                }
            },
            execute: args => manager.incrFontSize(args['key'])
        });
        commands.addCommand(CommandIDs.decrFontSize, {
            label: args => {
                switch (args.key) {
                    case 'code-font-size':
                        return trans.__('Decrease Code Font Size');
                    case 'content-font-size1':
                        return trans.__('Decrease Content Font Size');
                    case 'ui-font-size1':
                        return trans.__('Decrease UI Font Size');
                    default:
                        return trans.__('Decrease Font Size');
                }
            },
            execute: args => manager.decrFontSize(args['key'])
        });
        return manager;
    },
    autoStart: true,
    provides: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager
};
/**
 * The default theme manager's UI command palette and main menu functionality.
 *
 * #### Notes
 * This plugin loads separately from the theme manager plugin in order to
 * prevent blocking of the theme manager while it waits for the command palette
 * and main menu to become available.
 */
const themesPaletteMenuPlugin = {
    id: '@jupyterlab/apputils-extension:themes-palette-menu',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu],
    activate: (app, manager, translator, palette, mainMenu) => {
        const trans = translator.load('jupyterlab');
        // If we have a main menu, add the theme manager to the settings menu.
        if (mainMenu) {
            void app.restored.then(() => {
                var _a;
                const isPalette = false;
                const themeMenu = (_a = mainMenu.settingsMenu.items.find(item => {
                    var _a;
                    return item.type === 'submenu' &&
                        ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-settings-apputilstheme';
                })) === null || _a === void 0 ? void 0 : _a.submenu;
                // choose a theme
                if (themeMenu) {
                    manager.themes.forEach((theme, index) => {
                        themeMenu.insertItem(index, {
                            command: CommandIDs.changeTheme,
                            args: { isPalette, theme }
                        });
                    });
                }
            });
        }
        // If we have a command palette, add theme switching options to it.
        if (palette) {
            void app.restored.then(() => {
                const category = trans.__('Theme');
                const command = CommandIDs.changeTheme;
                const isPalette = true;
                // choose a theme
                manager.themes.forEach(theme => {
                    palette.addItem({ command, args: { isPalette, theme }, category });
                });
                // toggle scrollbar theming
                palette.addItem({ command: CommandIDs.themeScrollbars, category });
                // increase/decrease code font size
                palette.addItem({
                    command: CommandIDs.incrFontSize,
                    args: {
                        key: 'code-font-size'
                    },
                    category
                });
                palette.addItem({
                    command: CommandIDs.decrFontSize,
                    args: {
                        key: 'code-font-size'
                    },
                    category
                });
                // increase/decrease content font size
                palette.addItem({
                    command: CommandIDs.incrFontSize,
                    args: {
                        key: 'content-font-size1'
                    },
                    category
                });
                palette.addItem({
                    command: CommandIDs.decrFontSize,
                    args: {
                        key: 'content-font-size1'
                    },
                    category
                });
                // increase/decrease ui font size
                palette.addItem({
                    command: CommandIDs.incrFontSize,
                    args: {
                        key: 'ui-font-size1'
                    },
                    category
                });
                palette.addItem({
                    command: CommandIDs.decrFontSize,
                    args: {
                        key: 'ui-font-size1'
                    },
                    category
                });
            });
        }
    },
    autoStart: true
};


/***/ }),

/***/ "../packages/apputils-extension/lib/workspacesplugin.js":
/*!**************************************************************!*\
  !*** ../packages/apputils-extension/lib/workspacesplugin.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "workspacesPlugin": () => (/* binding */ workspacesPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








var CommandIDs;
(function (CommandIDs) {
    CommandIDs.saveWorkspace = 'workspace-ui:save';
    CommandIDs.saveWorkspaceAs = 'workspace-ui:save-as';
})(CommandIDs || (CommandIDs = {}));
const WORKSPACE_NAME = 'jupyterlab-workspace';
const WORKSPACE_EXT = '.' + WORKSPACE_NAME;
const LAST_SAVE_ID = 'workspace-ui:lastSave';
const ICON_NAME = 'jp-JupyterIcon';
/**
 * The workspace MIME renderer and save plugin.
 */
const workspacesPlugin = {
    id: '@jupyterlab/apputils-extension:workspaces',
    autoStart: true,
    requires: [
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IWindowResolver,
        _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__.IStateDB,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths
    ],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter],
    activate: (app, fbf, resolver, state, translator, paths, router) => {
        // The workspace factory creates dummy widgets to load a new workspace.
        const factory = new Private.WorkspaceFactory({
            workspaces: app.serviceManager.workspaces,
            router,
            state,
            translator,
            paths
        });
        const trans = translator.load('jupyterlab');
        app.docRegistry.addFileType({
            name: WORKSPACE_NAME,
            contentType: 'file',
            fileFormat: 'text',
            displayName: trans.__('JupyterLab workspace File'),
            extensions: [WORKSPACE_EXT],
            mimeTypes: ['text/json'],
            iconClass: ICON_NAME
        });
        app.docRegistry.addWidgetFactory(factory);
        app.commands.addCommand(CommandIDs.saveWorkspaceAs, {
            label: trans.__('Save Current Workspace As…'),
            execute: async () => {
                const data = app.serviceManager.workspaces.fetch(resolver.name);
                await Private.saveAs(fbf.defaultBrowser, app.serviceManager.contents, data, state, translator);
            }
        });
        app.commands.addCommand(CommandIDs.saveWorkspace, {
            label: trans.__('Save Current Workspace'),
            execute: async () => {
                const { contents } = app.serviceManager;
                const data = app.serviceManager.workspaces.fetch(resolver.name);
                const lastSave = (await state.fetch(LAST_SAVE_ID));
                if (lastSave === undefined) {
                    await Private.saveAs(fbf.defaultBrowser, contents, data, state, translator);
                }
                else {
                    await Private.save(lastSave, contents, data, state);
                }
            }
        });
    }
};
var Private;
(function (Private) {
    /**
     * Save workspace to a user provided location
     */
    async function save(userPath, contents, data, state) {
        let name = userPath.split('/').pop();
        // Add extension if not provided or remove extension from name if it was.
        if (name !== undefined && name.includes('.')) {
            name = name.split('.')[0];
        }
        else {
            userPath = userPath + WORKSPACE_EXT;
        }
        // Save last save location, for save button to work
        await state.save(LAST_SAVE_ID, userPath);
        const resolvedData = await data;
        resolvedData.metadata.id = `${name}`;
        await contents.save(userPath, {
            type: 'file',
            format: 'text',
            content: JSON.stringify(resolvedData)
        });
    }
    Private.save = save;
    /**
     * Ask user for location, and save workspace.
     * Default location is the current directory in the file browser
     */
    async function saveAs(browser, contents, data, state, translator) {
        var _a;
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator;
        const lastSave = await state.fetch(LAST_SAVE_ID);
        let defaultName;
        if (lastSave === undefined) {
            defaultName = 'new-workspace';
        }
        else {
            defaultName = (_a = lastSave.split('/').pop()) === null || _a === void 0 ? void 0 : _a.split('.')[0];
        }
        const defaultPath = browser.model.path + '/' + defaultName + WORKSPACE_EXT;
        const userPath = await getSavePath(defaultPath, translator);
        if (userPath) {
            await save(userPath, contents, data, state);
        }
    }
    Private.saveAs = saveAs;
    /**
     * This widget factory is used to handle double click on workspace
     */
    class WorkspaceFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3__.ABCWidgetFactory {
        /**
         * Construct a widget factory that uploads a workspace and navigates to it.
         *
         * @param options - The instantiation options for a `WorkspaceFactory`.
         */
        constructor(options) {
            const trans = (options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
            super({
                name: trans.__('Workspace loader'),
                fileTypes: [WORKSPACE_NAME],
                defaultFor: [WORKSPACE_NAME],
                readOnly: true
            });
            this._application = options.paths.urls.app;
            this._router = options.router;
            this._state = options.state;
            this._workspaces = options.workspaces;
        }
        /**
         * Loads the workspace into load, and jump to it
         * @param context This is used queried to query the workspace content
         */
        createNewWidget(context) {
            // Save a file's contents as a workspace and navigate to that workspace.
            void context.ready.then(async () => {
                const file = context.model;
                const workspace = file.toJSON();
                const path = context.path;
                const id = workspace.metadata.id;
                // Save the file contents as a workspace.
                await this._workspaces.save(id, workspace);
                // Save last save location for the save command.
                await this._state.save(LAST_SAVE_ID, path);
                // Navigate to new workspace.
                const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(this._application, 'workspaces', id);
                if (this._router) {
                    this._router.navigate(url, { hard: true });
                }
                else {
                    document.location.href = url;
                }
            });
            return dummyWidget(context);
        }
    }
    Private.WorkspaceFactory = WorkspaceFactory;
    /**
     * Returns a dummy widget with disposed content that doesn't render in the UI.
     *
     * @param context - The file context.
     */
    function dummyWidget(context) {
        const widget = new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3__.DocumentWidget({ content: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__.Widget(), context });
        widget.content.dispose();
        return widget;
    }
    /**
     * Ask user for a path to save to.
     * @param defaultPath Path already present when the dialog is shown
     */
    async function getSavePath(defaultPath, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const saveBtn = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Save') });
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Save Current Workspace As…'),
            body: new SaveWidget(defaultPath),
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Cancel') }), saveBtn]
        });
        if (result.button.label === trans.__('Save')) {
            return result.value;
        }
        else {
            return null;
        }
    }
    /**
     * A widget that gets a file path from a user.
     */
    class SaveWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__.Widget {
        /**
         * Gets a modal node for getting save location. Will have a default to the current opened directory
         * @param path Default location
         */
        constructor(path) {
            super({ node: createSaveNode(path) });
        }
        /**
         * Gets the save path entered by the user
         */
        getValue() {
            return this.node.value;
        }
    }
    /**
     * Create the node for a save widget.
     */
    function createSaveNode(path) {
        const input = document.createElement('input');
        input.value = path;
        return input;
    }
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvYXBwdXRpbHMtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvYXBwdXRpbHMtZXh0ZW5zaW9uL3NyYy9wYWxldHRlLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9hcHB1dGlscy1leHRlbnNpb24vc3JjL3NldHRpbmdjb25uZWN0b3IudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2FwcHV0aWxzLWV4dGVuc2lvbi9zcmMvc2V0dGluZ3NwbHVnaW4udHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2FwcHV0aWxzLWV4dGVuc2lvbi9zcmMvdGhlbWVzcGx1Z2lucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvYXBwdXRpbHMtZXh0ZW5zaW9uL3NyYy93b3Jrc3BhY2VzcGx1Z2luLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBTzhCO0FBYUg7QUFDc0M7QUFDTDtBQUNQO0FBQ0Y7QUFDUztBQUNYO0FBQ0k7QUFDRDtBQUNuQjtBQUNjO0FBQ3NCO0FBQ2xCO0FBRXREOztHQUVHO0FBQ0gsTUFBTSxzQkFBc0IsR0FBRyxLQUFLLENBQUM7QUFFckM7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FjbkI7QUFkRCxXQUFVLFVBQVU7SUFDTCxvQkFBUyxHQUFHLHVCQUF1QixDQUFDO0lBRXBDLGdCQUFLLEdBQUcsZ0JBQWdCLENBQUM7SUFFekIsZ0JBQUssR0FBRyxn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QUFDLElBQVk7UUFDbEMsTUFBTSxLQUFLLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyxPQUFPLENBQUMsQ0FBQztRQUM5QyxLQUFLLENBQUMsS0FBSyxHQUFHLElBQUksQ0FBQztRQUNuQixPQUFPLEtBQUssQ0FBQztJQUNmLENBQUM7QUFDSCxDQUFDLEVBdE1TLE9BQU8sS0FBUCxPQUFPLFFBc01oQiIsImZpbGUiOiJwYWNrYWdlc19hcHB1dGlscy1leHRlbnNpb25fbGliX2luZGV4X2pzLmI2OWNlN2JhZTQxZDc4MmZlNDJiLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBhcHB1dGlscy1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGF5b3V0UmVzdG9yZXIsXG4gIElSb3V0ZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIGRlZmF1bHRTYW5pdGl6ZXIsXG4gIERpYWxvZyxcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBJU2FuaXRpemVyLFxuICBJU2Vzc2lvbkNvbnRleHREaWFsb2dzLFxuICBJU3BsYXNoU2NyZWVuLFxuICBJV2luZG93UmVzb2x2ZXIsXG4gIE1haW5BcmVhV2lkZ2V0LFxuICBQcmludGluZyxcbiAgc2Vzc2lvbkNvbnRleHREaWFsb2dzLFxuICBXaW5kb3dSZXNvbHZlclxufSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBQYWdlQ29uZmlnLCBQYXRoRXh0LCBVUkxFeHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJU3RhdGVEQiwgU3RhdGVEQiB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXRlZGInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBqdXB5dGVyRmF2aWNvbkljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFByb21pc2VEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IERpc3Bvc2FibGVEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBEZWJvdW5jZXIsIFRocm90dGxlciB9IGZyb20gJ0BsdW1pbm8vcG9sbGluZyc7XG5pbXBvcnQgeyBQYWxldHRlIH0gZnJvbSAnLi9wYWxldHRlJztcbmltcG9ydCB7IHNldHRpbmdzUGx1Z2luIH0gZnJvbSAnLi9zZXR0aW5nc3BsdWdpbic7XG5pbXBvcnQgeyB0aGVtZXNQYWxldHRlTWVudVBsdWdpbiwgdGhlbWVzUGx1Z2luIH0gZnJvbSAnLi90aGVtZXNwbHVnaW5zJztcbmltcG9ydCB7IHdvcmtzcGFjZXNQbHVnaW4gfSBmcm9tICcuL3dvcmtzcGFjZXNwbHVnaW4nO1xuXG4vKipcbiAqIFRoZSBpbnRlcnZhbCBpbiBtaWxsaXNlY29uZHMgYmVmb3JlIHJlY292ZXIgb3B0aW9ucyBhcHBlYXIgZHVyaW5nIHNwbGFzaC5cbiAqL1xuY29uc3QgU1BMQVNIX1JFQ09WRVJfVElNRU9VVCA9IDEyMDAwO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBhcHB1dGlscyBwbHVnaW4uXG4gKi9cbm5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IGxvYWRTdGF0ZSA9ICdhcHB1dGlsczpsb2FkLXN0YXRlZGInO1xuXG4gIGV4cG9ydCBjb25zdCBwcmludCA9ICdhcHB1dGlsczpwcmludCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlc2V0ID0gJ2FwcHV0aWxzOnJlc2V0JztcblxuICBleHBvcnQgY29uc3QgcmVzZXRPbkxvYWQgPSAnYXBwdXRpbHM6cmVzZXQtb24tbG9hZCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJ1bkZpcnN0RW5hYmxlZCA9ICdhcHB1dGlsczpydW4tZmlyc3QtZW5hYmxlZCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJ1bkFsbEVuYWJsZWQgPSAnYXBwdXRpbHM6cnVuLWFsbC1lbmFibGVkJztcblxuICBleHBvcnQgY29uc3QgdG9nZ2xlSGVhZGVyID0gJ2FwcHV0aWxzOnRvZ2dsZS1oZWFkZXInO1xufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGNvbW1hbmQgcGFsZXR0ZSBleHRlbnNpb24uXG4gKi9cbmNvbnN0IHBhbGV0dGU6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJQ29tbWFuZFBhbGV0dGU+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcHV0aWxzLWV4dGVuc2lvbjpwYWxldHRlJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgcHJvdmlkZXM6IElDb21tYW5kUGFsZXR0ZSxcbiAgb3B0aW9uYWw6IFtJU2V0dGluZ1JlZ2lzdHJ5XSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsXG4gICkgPT4ge1xuICAgIHJldHVybiBQYWxldHRlLmFjdGl2YXRlKGFwcCwgdHJhbnNsYXRvciwgc2V0dGluZ1JlZ2lzdHJ5KTtcbiAgfVxufTtcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBjb21tYW5kIHBhbGV0dGUncyByZXN0b3JhdGlvbiBleHRlbnNpb24uXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhlIGNvbW1hbmQgcGFsZXR0ZSdzIHJlc3RvcmF0aW9uIGxvZ2ljIGlzIGhhbmRsZWQgc2VwYXJhdGVseSBmcm9tIHRoZVxuICogY29tbWFuZCBwYWxldHRlIHByb3ZpZGVyIGV4dGVuc2lvbiBiZWNhdXNlIHRoZSBsYXlvdXQgcmVzdG9yZXIgZGVwZW5kZW5jeVxuICogY2F1c2VzIHRoZSBjb21tYW5kIHBhbGV0dGUgdG8gYmUgdW5hdmFpbGFibGUgdG8gb3RoZXIgZXh0ZW5zaW9ucyBlYXJsaWVyXG4gKiBpbiB0aGUgYXBwbGljYXRpb24gbG9hZCBjeWNsZS5cbiAqL1xuY29uc3QgcGFsZXR0ZVJlc3RvcmVyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMtZXh0ZW5zaW9uOnBhbGV0dGUtcmVzdG9yZXInLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSUxheW91dFJlc3RvcmVyLCBJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlcixcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApID0+IHtcbiAgICBQYWxldHRlLnJlc3RvcmUoYXBwLCByZXN0b3JlciwgdHJhbnNsYXRvcik7XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgd2luZG93IG5hbWUgcmVzb2x2ZXIgcHJvdmlkZXIuXG4gKi9cbmNvbnN0IHJlc29sdmVyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SVdpbmRvd1Jlc29sdmVyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHB1dGlscy1leHRlbnNpb246cmVzb2x2ZXInLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJV2luZG93UmVzb2x2ZXIsXG4gIHJlcXVpcmVzOiBbSnVweXRlckZyb250RW5kLklQYXRocywgSVJvdXRlcl0sXG4gIGFjdGl2YXRlOiBhc3luYyAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgcGF0aHM6IEp1cHl0ZXJGcm9udEVuZC5JUGF0aHMsXG4gICAgcm91dGVyOiBJUm91dGVyXG4gICkgPT4ge1xuICAgIGNvbnN0IHsgaGFzaCwgc2VhcmNoIH0gPSByb3V0ZXIuY3VycmVudDtcbiAgICBjb25zdCBxdWVyeSA9IFVSTEV4dC5xdWVyeVN0cmluZ1RvT2JqZWN0KHNlYXJjaCB8fCAnJyk7XG4gICAgY29uc3Qgc29sdmVyID0gbmV3IFdpbmRvd1Jlc29sdmVyKCk7XG4gICAgY29uc3Qgd29ya3NwYWNlID0gUGFnZUNvbmZpZy5nZXRPcHRpb24oJ3dvcmtzcGFjZScpO1xuICAgIGNvbnN0IHRyZWVQYXRoID0gUGFnZUNvbmZpZy5nZXRPcHRpb24oJ3RyZWVQYXRoJyk7XG4gICAgY29uc3QgbW9kZSA9XG4gICAgICBQYWdlQ29uZmlnLmdldE9wdGlvbignbW9kZScpID09PSAnbXVsdGlwbGUtZG9jdW1lbnQnID8gJ2xhYicgOiAnZG9jJztcbiAgICAvLyBUaGlzIGlzIHVzZWQgYXMgYSBrZXkgaW4gbG9jYWwgc3RvcmFnZSB0byByZWZlciB0byB3b3Jrc3BhY2VzLCBlaXRoZXIgdGhlIG5hbWVcbiAgICAvLyBvZiB0aGUgd29ya3NwYWNlIG9yIHRoZSBzdHJpbmcgUGFnZUNvbmZpZy5kZWZhdWx0V29ya3NwYWNlLiBCb3RoIGxhYiBhbmQgZG9jIG1vZGVzIHNoYXJlIHRoZSBzYW1lIHdvcmtzcGFjZS5cbiAgICBjb25zdCBjYW5kaWRhdGUgPSB3b3Jrc3BhY2UgPyB3b3Jrc3BhY2UgOiBQYWdlQ29uZmlnLmRlZmF1bHRXb3Jrc3BhY2U7XG4gICAgY29uc3QgcmVzdCA9IHRyZWVQYXRoID8gVVJMRXh0LmpvaW4oJ3RyZWUnLCB0cmVlUGF0aCkgOiAnJztcbiAgICB0cnkge1xuICAgICAgYXdhaXQgc29sdmVyLnJlc29sdmUoY2FuZGlkYXRlKTtcbiAgICAgIHJldHVybiBzb2x2ZXI7XG4gICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgIC8vIFdpbmRvdyByZXNvbHV0aW9uIGhhcyBmYWlsZWQgc28gdGhlIFVSTCBtdXN0IGNoYW5nZS4gUmV0dXJuIGEgcHJvbWlzZVxuICAgICAgLy8gdGhhdCBuZXZlciByZXNvbHZlcyB0byBwcmV2ZW50IHRoZSBhcHBsaWNhdGlvbiBmcm9tIGxvYWRpbmcgcGx1Z2luc1xuICAgICAgLy8gdGhhdCByZWx5IG9uIGBJV2luZG93UmVzb2x2ZXJgLlxuICAgICAgcmV0dXJuIG5ldyBQcm9taXNlPElXaW5kb3dSZXNvbHZlcj4oKCkgPT4ge1xuICAgICAgICBjb25zdCB7IGJhc2UgfSA9IHBhdGhzLnVybHM7XG4gICAgICAgIGNvbnN0IHBvb2wgPVxuICAgICAgICAgICdhYmNkZWZnaGlqa2xtbm9wcXJzdHV2d3h5ekFCQ0RFRkdISUpLTE1OT1BRUlNUVVZXWFlaMDEyMzQ1Njc4OSc7XG4gICAgICAgIGNvbnN0IHJhbmRvbSA9IHBvb2xbTWF0aC5mbG9vcihNYXRoLnJhbmRvbSgpICogcG9vbC5sZW5ndGgpXTtcbiAgICAgICAgbGV0IHBhdGggPSBVUkxFeHQuam9pbihiYXNlLCBtb2RlLCAnd29ya3NwYWNlcycsIGBhdXRvLSR7cmFuZG9tfWApO1xuICAgICAgICBwYXRoID0gcmVzdCA/IFVSTEV4dC5qb2luKHBhdGgsIFVSTEV4dC5lbmNvZGVQYXJ0cyhyZXN0KSkgOiBwYXRoO1xuXG4gICAgICAgIC8vIFJlc2V0IHRoZSB3b3Jrc3BhY2Ugb24gbG9hZC5cbiAgICAgICAgcXVlcnlbJ3Jlc2V0J10gPSAnJztcblxuICAgICAgICBjb25zdCB1cmwgPSBwYXRoICsgVVJMRXh0Lm9iamVjdFRvUXVlcnlTdHJpbmcocXVlcnkpICsgKGhhc2ggfHwgJycpO1xuICAgICAgICByb3V0ZXIubmF2aWdhdGUodXJsLCB7IGhhcmQ6IHRydWUgfSk7XG4gICAgICB9KTtcbiAgICB9XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgc3BsYXNoIHNjcmVlbiBwcm92aWRlci5cbiAqL1xuY29uc3Qgc3BsYXNoOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SVNwbGFzaFNjcmVlbj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMtZXh0ZW5zaW9uOnNwbGFzaCcsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIHByb3ZpZGVzOiBJU3BsYXNoU2NyZWVuLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kLCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcikgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBjb21tYW5kcywgcmVzdG9yZWQgfSA9IGFwcDtcblxuICAgIC8vIENyZWF0ZSBzcGxhc2ggZWxlbWVudCBhbmQgcG9wdWxhdGUgaXQuXG4gICAgY29uc3Qgc3BsYXNoID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgY29uc3QgZ2FsYXh5ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgY29uc3QgbG9nbyA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuXG4gICAgc3BsYXNoLmlkID0gJ2p1cHl0ZXJsYWItc3BsYXNoJztcbiAgICBnYWxheHkuaWQgPSAnZ2FsYXh5JztcbiAgICBsb2dvLmlkID0gJ21haW4tbG9nbyc7XG5cbiAgICBqdXB5dGVyRmF2aWNvbkljb24uZWxlbWVudCh7XG4gICAgICBjb250YWluZXI6IGxvZ28sXG5cbiAgICAgIHN0eWxlc2hlZXQ6ICdzcGxhc2gnXG4gICAgfSk7XG5cbiAgICBnYWxheHkuYXBwZW5kQ2hpbGQobG9nbyk7XG4gICAgWycxJywgJzInLCAnMyddLmZvckVhY2goaWQgPT4ge1xuICAgICAgY29uc3QgbW9vbiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgICAgY29uc3QgcGxhbmV0ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG5cbiAgICAgIG1vb24uaWQgPSBgbW9vbiR7aWR9YDtcbiAgICAgIG1vb24uY2xhc3NOYW1lID0gJ21vb24gb3JiaXQnO1xuICAgICAgcGxhbmV0LmlkID0gYHBsYW5ldCR7aWR9YDtcbiAgICAgIHBsYW5ldC5jbGFzc05hbWUgPSAncGxhbmV0JztcblxuICAgICAgbW9vbi5hcHBlbmRDaGlsZChwbGFuZXQpO1xuICAgICAgZ2FsYXh5LmFwcGVuZENoaWxkKG1vb24pO1xuICAgIH0pO1xuXG4gICAgc3BsYXNoLmFwcGVuZENoaWxkKGdhbGF4eSk7XG5cbiAgICAvLyBDcmVhdGUgZGVib3VuY2VkIHJlY292ZXJ5IGRpYWxvZyBmdW5jdGlvbi5cbiAgICBsZXQgZGlhbG9nOiBEaWFsb2c8dW5rbm93bj4gfCBudWxsO1xuICAgIGNvbnN0IHJlY292ZXJ5ID0gbmV3IFRocm90dGxlcihcbiAgICAgIGFzeW5jICgpID0+IHtcbiAgICAgICAgaWYgKGRpYWxvZykge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGRpYWxvZyA9IG5ldyBEaWFsb2coe1xuICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnTG9hZGluZ+KApicpLFxuICAgICAgICAgIGJvZHk6IHRyYW5zLl9fKGBUaGUgbG9hZGluZyBzY3JlZW4gaXMgdGFraW5nIGEgbG9uZyB0aW1lLlxuV291bGQgeW91IGxpa2UgdG8gY2xlYXIgdGhlIHdvcmtzcGFjZSBvciBrZWVwIHdhaXRpbmc/YCksXG4gICAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnS2VlcCBXYWl0aW5nJykgfSksXG4gICAgICAgICAgICBEaWFsb2cud2FybkJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnQ2xlYXIgV29ya3NwYWNlJykgfSlcbiAgICAgICAgICBdXG4gICAgICAgIH0pO1xuXG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgZGlhbG9nLmxhdW5jaCgpO1xuICAgICAgICAgIGRpYWxvZy5kaXNwb3NlKCk7XG4gICAgICAgICAgZGlhbG9nID0gbnVsbDtcbiAgICAgICAgICBpZiAocmVzdWx0LmJ1dHRvbi5hY2NlcHQgJiYgY29tbWFuZHMuaGFzQ29tbWFuZChDb21tYW5kSURzLnJlc2V0KSkge1xuICAgICAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5yZXNldCk7XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgLy8gUmUtaW52b2tlIHRoZSByZWNvdmVyeSB0aW1lciBpbiB0aGUgbmV4dCBmcmFtZS5cbiAgICAgICAgICByZXF1ZXN0QW5pbWF0aW9uRnJhbWUoKCkgPT4ge1xuICAgICAgICAgICAgLy8gQmVjYXVzZSByZWNvdmVyeSBjYW4gYmUgc3RvcHBlZCwgaGFuZGxlIGludm9jYXRpb24gcmVqZWN0aW9uLlxuICAgICAgICAgICAgdm9pZCByZWNvdmVyeS5pbnZva2UoKS5jYXRjaChfID0+IHVuZGVmaW5lZCk7XG4gICAgICAgICAgfSk7XG4gICAgICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgICAgLyogbm8tb3AgKi9cbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIHsgbGltaXQ6IFNQTEFTSF9SRUNPVkVSX1RJTUVPVVQsIGVkZ2U6ICd0cmFpbGluZycgfVxuICAgICk7XG5cbiAgICAvLyBSZXR1cm4gSVNwbGFzaFNjcmVlbi5cbiAgICBsZXQgc3BsYXNoQ291bnQgPSAwO1xuICAgIHJldHVybiB7XG4gICAgICBzaG93OiAobGlnaHQgPSB0cnVlKSA9PiB7XG4gICAgICAgIHNwbGFzaC5jbGFzc0xpc3QucmVtb3ZlKCdzcGxhc2gtZmFkZScpO1xuICAgICAgICBzcGxhc2guY2xhc3NMaXN0LnRvZ2dsZSgnbGlnaHQnLCBsaWdodCk7XG4gICAgICAgIHNwbGFzaC5jbGFzc0xpc3QudG9nZ2xlKCdkYXJrJywgIWxpZ2h0KTtcbiAgICAgICAgc3BsYXNoQ291bnQrKztcbiAgICAgICAgZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChzcGxhc2gpO1xuXG4gICAgICAgIC8vIEJlY2F1c2UgcmVjb3ZlcnkgY2FuIGJlIHN0b3BwZWQsIGhhbmRsZSBpbnZvY2F0aW9uIHJlamVjdGlvbi5cbiAgICAgICAgdm9pZCByZWNvdmVyeS5pbnZva2UoKS5jYXRjaChfID0+IHVuZGVmaW5lZCk7XG5cbiAgICAgICAgcmV0dXJuIG5ldyBEaXNwb3NhYmxlRGVsZWdhdGUoYXN5bmMgKCkgPT4ge1xuICAgICAgICAgIGF3YWl0IHJlc3RvcmVkO1xuICAgICAgICAgIGlmICgtLXNwbGFzaENvdW50ID09PSAwKSB7XG4gICAgICAgICAgICB2b2lkIHJlY292ZXJ5LnN0b3AoKTtcblxuICAgICAgICAgICAgaWYgKGRpYWxvZykge1xuICAgICAgICAgICAgICBkaWFsb2cuZGlzcG9zZSgpO1xuICAgICAgICAgICAgICBkaWFsb2cgPSBudWxsO1xuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICBzcGxhc2guY2xhc3NMaXN0LmFkZCgnc3BsYXNoLWZhZGUnKTtcbiAgICAgICAgICAgIHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgICAgICAgZG9jdW1lbnQuYm9keS5yZW1vdmVDaGlsZChzcGxhc2gpO1xuICAgICAgICAgICAgfSwgMjAwKTtcbiAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH07XG4gIH1cbn07XG5cbmNvbnN0IHByaW50OiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMtZXh0ZW5zaW9uOnByaW50JyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZCwgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IpID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucHJpbnQsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnUHJpbnTigKYnKSxcbiAgICAgIGlzRW5hYmxlZDogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSBhcHAuc2hlbGwuY3VycmVudFdpZGdldDtcbiAgICAgICAgcmV0dXJuIFByaW50aW5nLmdldFByaW50RnVuY3Rpb24od2lkZ2V0KSAhPT0gbnVsbDtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0O1xuICAgICAgICBjb25zdCBwcmludEZ1bmN0aW9uID0gUHJpbnRpbmcuZ2V0UHJpbnRGdW5jdGlvbih3aWRnZXQpO1xuICAgICAgICBpZiAocHJpbnRGdW5jdGlvbikge1xuICAgICAgICAgIGF3YWl0IHByaW50RnVuY3Rpb24oKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG5leHBvcnQgY29uc3QgdG9nZ2xlSGVhZGVyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMtZXh0ZW5zaW9uOnRvZ2dsZS1oZWFkZXInLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZV0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgY29uc3QgY2F0ZWdvcnk6IHN0cmluZyA9IHRyYW5zLl9fKCdNYWluIEFyZWEnKTtcbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRvZ2dsZUhlYWRlciwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdTaG93IEhlYWRlciBBYm92ZSBDb250ZW50JyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+XG4gICAgICAgIGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0IGluc3RhbmNlb2YgTWFpbkFyZWFXaWRnZXQgJiZcbiAgICAgICAgYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQuY29udGVudEhlYWRlci53aWRnZXRzLmxlbmd0aCA+IDAsXG4gICAgICBpc1RvZ2dsZWQ6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIHJldHVybiB3aWRnZXQgaW5zdGFuY2VvZiBNYWluQXJlYVdpZGdldFxuICAgICAgICAgID8gIXdpZGdldC5jb250ZW50SGVhZGVyLmlzSGlkZGVuXG4gICAgICAgICAgOiBmYWxzZTtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0O1xuICAgICAgICBpZiAod2lkZ2V0IGluc3RhbmNlb2YgTWFpbkFyZWFXaWRnZXQpIHtcbiAgICAgICAgICB3aWRnZXQuY29udGVudEhlYWRlci5zZXRIaWRkZW4oIXdpZGdldC5jb250ZW50SGVhZGVyLmlzSGlkZGVuKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kOiBDb21tYW5kSURzLnRvZ2dsZUhlYWRlciwgY2F0ZWdvcnkgfSk7XG4gICAgfVxuICB9XG59O1xuXG4vKipcbiAqIFVwZGF0ZSB0aGUgYnJvd3NlciB0aXRsZSBiYXNlZCBvbiB0aGUgd29ya3NwYWNlIGFuZCB0aGUgY3VycmVudFxuICogYWN0aXZlIGl0ZW0uXG4gKi9cbmFzeW5jIGZ1bmN0aW9uIHVwZGF0ZVRhYlRpdGxlKHdvcmtzcGFjZTogc3RyaW5nLCBkYjogSVN0YXRlREIsIG5hbWU6IHN0cmluZykge1xuICBjb25zdCBkYXRhOiBhbnkgPSBhd2FpdCBkYi50b0pTT04oKTtcbiAgbGV0IGN1cnJlbnQ6IHN0cmluZyA9IGRhdGFbJ2xheW91dC1yZXN0b3JlcjpkYXRhJ10/Lm1haW4/LmN1cnJlbnQ7XG4gIGlmIChjdXJyZW50ID09PSB1bmRlZmluZWQpIHtcbiAgICBkb2N1bWVudC50aXRsZSA9IGAke1BhZ2VDb25maWcuZ2V0T3B0aW9uKCdhcHBOYW1lJykgfHwgJ0p1cHl0ZXJMYWInfSR7XG4gICAgICB3b3Jrc3BhY2Uuc3RhcnRzV2l0aCgnYXV0by0nKSA/IGAgKCR7d29ya3NwYWNlfSlgIDogYGBcbiAgICB9YDtcbiAgfSBlbHNlIHtcbiAgICAvLyBGaWxlIG5hbWUgZnJvbSBjdXJyZW50IHBhdGhcbiAgICBsZXQgY3VycmVudEZpbGU6IHN0cmluZyA9IFBhdGhFeHQuYmFzZW5hbWUoY3VycmVudC5zcGxpdCgnOicpWzFdKTtcbiAgICAvLyBUcnVuY2F0ZSB0byBmaXJzdCAxMiBjaGFyYWN0ZXJzIG9mIGN1cnJlbnQgZG9jdW1lbnQgbmFtZSArIC4uLiBpZiBsZW5ndGggPiAxNVxuICAgIGN1cnJlbnRGaWxlID1cbiAgICAgIGN1cnJlbnRGaWxlLmxlbmd0aCA+IDE1XG4gICAgICAgID8gY3VycmVudEZpbGUuc2xpY2UoMCwgMTIpLmNvbmNhdChg4oCmYClcbiAgICAgICAgOiBjdXJyZW50RmlsZTtcbiAgICAvLyBOdW1iZXIgb2YgcmVzdG9yYWJsZSBpdGVtcyB0aGF0IGFyZSBlaXRoZXIgbm90ZWJvb2tzIG9yIGVkaXRvcnNcbiAgICBjb25zdCBjb3VudDogbnVtYmVyID0gT2JqZWN0LmtleXMoZGF0YSkuZmlsdGVyKFxuICAgICAgaXRlbSA9PiBpdGVtLnN0YXJ0c1dpdGgoJ25vdGVib29rJykgfHwgaXRlbS5zdGFydHNXaXRoKCdlZGl0b3InKVxuICAgICkubGVuZ3RoO1xuXG4gICAgaWYgKHdvcmtzcGFjZS5zdGFydHNXaXRoKCdhdXRvLScpKSB7XG4gICAgICBkb2N1bWVudC50aXRsZSA9IGAke2N1cnJlbnRGaWxlfSAoJHt3b3Jrc3BhY2V9JHtcbiAgICAgICAgY291bnQgPiAxID8gYCA6ICR7Y291bnR9YCA6IGBgXG4gICAgICB9KSAtICR7bmFtZX1gO1xuICAgIH0gZWxzZSB7XG4gICAgICBkb2N1bWVudC50aXRsZSA9IGAke2N1cnJlbnRGaWxlfSR7XG4gICAgICAgIGNvdW50ID4gMSA/IGAgKCR7Y291bnR9KWAgOiBgYFxuICAgICAgfSAtICR7bmFtZX1gO1xuICAgIH1cbiAgfVxufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IHN0YXRlIGRhdGFiYXNlIGZvciBzdG9yaW5nIGFwcGxpY2F0aW9uIHN0YXRlLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIElmIHRoaXMgZXh0ZW5zaW9uIGlzIGxvYWRlZCB3aXRoIGEgd2luZG93IHJlc29sdmVyLCBpdCB3aWxsIGF1dG9tYXRpY2FsbHkgYWRkXG4gKiBzdGF0ZSBtYW5hZ2VtZW50IGNvbW1hbmRzLCBVUkwgc3VwcG9ydCBmb3IgYGNsb25lYCBhbmQgYHJlc2V0YCwgYW5kIHdvcmtzcGFjZVxuICogYXV0by1zYXZpbmcuIE90aGVyd2lzZSwgaXQgd2lsbCByZXR1cm4gYSBzaW1wbGUgaW4tbWVtb3J5IHN0YXRlIGRhdGFiYXNlLlxuICovXG5jb25zdCBzdGF0ZTogSnVweXRlckZyb250RW5kUGx1Z2luPElTdGF0ZURCPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHB1dGlscy1leHRlbnNpb246c3RhdGUnLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJU3RhdGVEQixcbiAgcmVxdWlyZXM6IFtKdXB5dGVyRnJvbnRFbmQuSVBhdGhzLCBJUm91dGVyLCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSVdpbmRvd1Jlc29sdmVyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBwYXRoczogSnVweXRlckZyb250RW5kLklQYXRocyxcbiAgICByb3V0ZXI6IElSb3V0ZXIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcmVzb2x2ZXI6IElXaW5kb3dSZXNvbHZlciB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIGlmIChyZXNvbHZlciA9PT0gbnVsbCkge1xuICAgICAgcmV0dXJuIG5ldyBTdGF0ZURCKCk7XG4gICAgfVxuXG4gICAgbGV0IHJlc29sdmVkID0gZmFsc2U7XG4gICAgY29uc3QgeyBjb21tYW5kcywgbmFtZSwgc2VydmljZU1hbmFnZXIgfSA9IGFwcDtcbiAgICBjb25zdCB7IHdvcmtzcGFjZXMgfSA9IHNlcnZpY2VNYW5hZ2VyO1xuICAgIGNvbnN0IHdvcmtzcGFjZSA9IHJlc29sdmVyLm5hbWU7XG4gICAgY29uc3QgdHJhbnNmb3JtID0gbmV3IFByb21pc2VEZWxlZ2F0ZTxTdGF0ZURCLkRhdGFUcmFuc2Zvcm0+KCk7XG4gICAgY29uc3QgZGIgPSBuZXcgU3RhdGVEQih7IHRyYW5zZm9ybTogdHJhbnNmb3JtLnByb21pc2UgfSk7XG4gICAgY29uc3Qgc2F2ZSA9IG5ldyBEZWJvdW5jZXIoYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3QgaWQgPSB3b3Jrc3BhY2U7XG4gICAgICBjb25zdCBtZXRhZGF0YSA9IHsgaWQgfTtcbiAgICAgIGNvbnN0IGRhdGEgPSBhd2FpdCBkYi50b0pTT04oKTtcbiAgICAgIGF3YWl0IHdvcmtzcGFjZXMuc2F2ZShpZCwgeyBkYXRhLCBtZXRhZGF0YSB9KTtcbiAgICB9KTtcblxuICAgIC8vIEFueSB0aW1lIHRoZSBsb2NhbCBzdGF0ZSBkYXRhYmFzZSBjaGFuZ2VzLCBzYXZlIHRoZSB3b3Jrc3BhY2UuXG4gICAgZGIuY2hhbmdlZC5jb25uZWN0KCgpID0+IHZvaWQgc2F2ZS5pbnZva2UoKSwgZGIpO1xuICAgIGRiLmNoYW5nZWQuY29ubmVjdCgoKSA9PiB1cGRhdGVUYWJUaXRsZSh3b3Jrc3BhY2UsIGRiLCBuYW1lKSk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubG9hZFN0YXRlLCB7XG4gICAgICBleGVjdXRlOiBhc3luYyAoYXJnczogSVJvdXRlci5JTG9jYXRpb24pID0+IHtcbiAgICAgICAgLy8gU2luY2UgdGhlIGNvbW1hbmQgY2FuIGJlIGV4ZWN1dGVkIGFuIGFyYml0cmFyeSBudW1iZXIgb2YgdGltZXMsIG1ha2VcbiAgICAgICAgLy8gc3VyZSBpdCBpcyBzYWZlIHRvIGNhbGwgbXVsdGlwbGUgdGltZXMuXG4gICAgICAgIGlmIChyZXNvbHZlZCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IHsgaGFzaCwgcGF0aCwgc2VhcmNoIH0gPSBhcmdzO1xuICAgICAgICBjb25zdCB7IHVybHMgfSA9IHBhdGhzO1xuICAgICAgICBjb25zdCBxdWVyeSA9IFVSTEV4dC5xdWVyeVN0cmluZ1RvT2JqZWN0KHNlYXJjaCB8fCAnJyk7XG4gICAgICAgIGNvbnN0IGNsb25lID1cbiAgICAgICAgICB0eXBlb2YgcXVlcnlbJ2Nsb25lJ10gPT09ICdzdHJpbmcnXG4gICAgICAgICAgICA/IHF1ZXJ5WydjbG9uZSddID09PSAnJ1xuICAgICAgICAgICAgICA/IFVSTEV4dC5qb2luKHVybHMuYmFzZSwgdXJscy5hcHApXG4gICAgICAgICAgICAgIDogVVJMRXh0LmpvaW4odXJscy5iYXNlLCB1cmxzLmFwcCwgJ3dvcmtzcGFjZXMnLCBxdWVyeVsnY2xvbmUnXSlcbiAgICAgICAgICAgIDogbnVsbDtcbiAgICAgICAgY29uc3Qgc291cmNlID0gY2xvbmUgfHwgd29ya3NwYWNlIHx8IG51bGw7XG5cbiAgICAgICAgaWYgKHNvdXJjZSA9PT0gbnVsbCkge1xuICAgICAgICAgIGNvbnNvbGUuZXJyb3IoYCR7Q29tbWFuZElEcy5sb2FkU3RhdGV9IGNhbm5vdCBsb2FkIG51bGwgd29ya3NwYWNlLmApO1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgY29uc3Qgc2F2ZWQgPSBhd2FpdCB3b3Jrc3BhY2VzLmZldGNoKHNvdXJjZSk7XG5cbiAgICAgICAgICAvLyBJZiB0aGlzIGNvbW1hbmQgaXMgY2FsbGVkIGFmdGVyIGEgcmVzZXQsIHRoZSBzdGF0ZSBkYXRhYmFzZVxuICAgICAgICAgIC8vIHdpbGwgYWxyZWFkeSBiZSByZXNvbHZlZC5cbiAgICAgICAgICBpZiAoIXJlc29sdmVkKSB7XG4gICAgICAgICAgICByZXNvbHZlZCA9IHRydWU7XG4gICAgICAgICAgICB0cmFuc2Zvcm0ucmVzb2x2ZSh7IHR5cGU6ICdvdmVyd3JpdGUnLCBjb250ZW50czogc2F2ZWQuZGF0YSB9KTtcbiAgICAgICAgICB9XG4gICAgICAgIH0gY2F0Y2ggKHsgbWVzc2FnZSB9KSB7XG4gICAgICAgICAgY29uc29sZS53YXJuKGBGZXRjaGluZyB3b3Jrc3BhY2UgXCIke3dvcmtzcGFjZX1cIiBmYWlsZWQuYCwgbWVzc2FnZSk7XG5cbiAgICAgICAgICAvLyBJZiB0aGUgd29ya3NwYWNlIGRvZXMgbm90IGV4aXN0LCBjYW5jZWwgdGhlIGRhdGEgdHJhbnNmb3JtYXRpb25cbiAgICAgICAgICAvLyBhbmQgc2F2ZSBhIHdvcmtzcGFjZSB3aXRoIHRoZSBjdXJyZW50IHVzZXIgc3RhdGUgZGF0YS5cbiAgICAgICAgICBpZiAoIXJlc29sdmVkKSB7XG4gICAgICAgICAgICByZXNvbHZlZCA9IHRydWU7XG4gICAgICAgICAgICB0cmFuc2Zvcm0ucmVzb2x2ZSh7IHR5cGU6ICdjYW5jZWwnLCBjb250ZW50czogbnVsbCB9KTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cblxuICAgICAgICBpZiAoc291cmNlID09PSBjbG9uZSkge1xuICAgICAgICAgIC8vIE1haW50YWluIHRoZSBxdWVyeSBzdHJpbmcgcGFyYW1ldGVycyBidXQgcmVtb3ZlIGBjbG9uZWAuXG4gICAgICAgICAgZGVsZXRlIHF1ZXJ5WydjbG9uZSddO1xuXG4gICAgICAgICAgY29uc3QgdXJsID0gcGF0aCArIFVSTEV4dC5vYmplY3RUb1F1ZXJ5U3RyaW5nKHF1ZXJ5KSArIGhhc2g7XG4gICAgICAgICAgY29uc3QgY2xvbmVkID0gc2F2ZS5pbnZva2UoKS50aGVuKCgpID0+IHJvdXRlci5zdG9wKTtcblxuICAgICAgICAgIC8vIEFmdGVyIHRoZSBzdGF0ZSBoYXMgYmVlbiBjbG9uZWQsIG5hdmlnYXRlIHRvIHRoZSBVUkwuXG4gICAgICAgICAgdm9pZCBjbG9uZWQudGhlbigoKSA9PiB7XG4gICAgICAgICAgICByb3V0ZXIubmF2aWdhdGUodXJsKTtcbiAgICAgICAgICB9KTtcblxuICAgICAgICAgIHJldHVybiBjbG9uZWQ7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBBZnRlciB0aGUgc3RhdGUgZGF0YWJhc2UgaGFzIGZpbmlzaGVkIGxvYWRpbmcsIHNhdmUgaXQuXG4gICAgICAgIGF3YWl0IHNhdmUuaW52b2tlKCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVzZXQsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnUmVzZXQgQXBwbGljYXRpb24gU3RhdGUnKSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICh7IHJlbG9hZCB9OiB7IHJlbG9hZDogYm9vbGVhbiB9KSA9PiB7XG4gICAgICAgIGF3YWl0IGRiLmNsZWFyKCk7XG4gICAgICAgIGF3YWl0IHNhdmUuaW52b2tlKCk7XG4gICAgICAgIGlmIChyZWxvYWQpIHtcbiAgICAgICAgICByb3V0ZXIucmVsb2FkKCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZXNldE9uTG9hZCwge1xuICAgICAgZXhlY3V0ZTogKGFyZ3M6IElSb3V0ZXIuSUxvY2F0aW9uKSA9PiB7XG4gICAgICAgIGNvbnN0IHsgaGFzaCwgcGF0aCwgc2VhcmNoIH0gPSBhcmdzO1xuICAgICAgICBjb25zdCBxdWVyeSA9IFVSTEV4dC5xdWVyeVN0cmluZ1RvT2JqZWN0KHNlYXJjaCB8fCAnJyk7XG4gICAgICAgIGNvbnN0IHJlc2V0ID0gJ3Jlc2V0JyBpbiBxdWVyeTtcbiAgICAgICAgY29uc3QgY2xvbmUgPSAnY2xvbmUnIGluIHF1ZXJ5O1xuXG4gICAgICAgIGlmICghcmVzZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICAvLyBJZiB0aGUgc3RhdGUgZGF0YWJhc2UgaGFzIGFscmVhZHkgYmVlbiByZXNvbHZlZCwgcmVzZXR0aW5nIGlzXG4gICAgICAgIC8vIGltcG9zc2libGUgd2l0aG91dCByZWxvYWRpbmcuXG4gICAgICAgIGlmIChyZXNvbHZlZCkge1xuICAgICAgICAgIHJldHVybiByb3V0ZXIucmVsb2FkKCk7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBFbXB0eSB0aGUgc3RhdGUgZGF0YWJhc2UuXG4gICAgICAgIHJlc29sdmVkID0gdHJ1ZTtcbiAgICAgICAgdHJhbnNmb3JtLnJlc29sdmUoeyB0eXBlOiAnY2xlYXInLCBjb250ZW50czogbnVsbCB9KTtcblxuICAgICAgICAvLyBNYWludGFpbiB0aGUgcXVlcnkgc3RyaW5nIHBhcmFtZXRlcnMgYnV0IHJlbW92ZSBgcmVzZXRgLlxuICAgICAgICBkZWxldGUgcXVlcnlbJ3Jlc2V0J107XG5cbiAgICAgICAgY29uc3QgdXJsID0gcGF0aCArIFVSTEV4dC5vYmplY3RUb1F1ZXJ5U3RyaW5nKHF1ZXJ5KSArIGhhc2g7XG4gICAgICAgIGNvbnN0IGNsZWFyZWQgPSBkYi5jbGVhcigpLnRoZW4oKCkgPT4gc2F2ZS5pbnZva2UoKSk7XG5cbiAgICAgICAgLy8gQWZ0ZXIgdGhlIHN0YXRlIGhhcyBiZWVuIHJlc2V0LCBuYXZpZ2F0ZSB0byB0aGUgVVJMLlxuICAgICAgICBpZiAoY2xvbmUpIHtcbiAgICAgICAgICB2b2lkIGNsZWFyZWQudGhlbigoKSA9PiB7XG4gICAgICAgICAgICByb3V0ZXIubmF2aWdhdGUodXJsLCB7IGhhcmQ6IHRydWUgfSk7XG4gICAgICAgICAgfSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgdm9pZCBjbGVhcmVkLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgcm91dGVyLm5hdmlnYXRlKHVybCk7XG4gICAgICAgICAgfSk7XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4gY2xlYXJlZDtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIHJvdXRlci5yZWdpc3Rlcih7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLmxvYWRTdGF0ZSxcbiAgICAgIHBhdHRlcm46IC8uPy8sXG4gICAgICByYW5rOiAzMCAvLyBIaWdoIHByaW9yaXR5OiAzMDoxMDAuXG4gICAgfSk7XG5cbiAgICByb3V0ZXIucmVnaXN0ZXIoe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5yZXNldE9uTG9hZCxcbiAgICAgIHBhdHRlcm46IC8oXFw/cmVzZXR8XFwmcmVzZXQpKCR8JikvLFxuICAgICAgcmFuazogMjAgLy8gSGlnaCBwcmlvcml0eTogMjA6MTAwLlxuICAgIH0pO1xuXG4gICAgcmV0dXJuIGRiO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IHNlc3Npb24gY29udGV4dCBkaWFsb2dzIGV4dGVuc2lvbi5cbiAqL1xuY29uc3Qgc2Vzc2lvbkRpYWxvZ3M6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJU2Vzc2lvbkNvbnRleHREaWFsb2dzPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHB1dGlscy1leHRlbnNpb246c2Vzc2lvbkRpYWxvZ3MnLFxuICBwcm92aWRlczogSVNlc3Npb25Db250ZXh0RGlhbG9ncyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKCkgPT4ge1xuICAgIHJldHVybiBzZXNzaW9uQ29udGV4dERpYWxvZ3M7XG4gIH1cbn07XG5cbi8qKlxuICogVXRpbGl0eSBjb21tYW5kc1xuICovXG5jb25zdCB1dGlsaXR5Q29tbWFuZHM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHB1dGlscy1leHRlbnNpb246dXRpbGl0eUNvbW1hbmRzJyxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZCwgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IpID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucnVuRmlyc3RFbmFibGVkLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1J1biBGaXJzdCBFbmFibGVkIENvbW1hbmQnKSxcbiAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgICBjb25zdCBjb21tYW5kczogc3RyaW5nW10gPSBhcmdzLmNvbW1hbmRzIGFzIHN0cmluZ1tdO1xuICAgICAgICBjb25zdCBjb21tYW5kQXJnczogYW55ID0gYXJncy5hcmdzO1xuICAgICAgICBjb25zdCBhcmdMaXN0ID0gQXJyYXkuaXNBcnJheShhcmdzKTtcbiAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCBjb21tYW5kcy5sZW5ndGg7IGkrKykge1xuICAgICAgICAgIGNvbnN0IGNtZCA9IGNvbW1hbmRzW2ldO1xuICAgICAgICAgIGNvbnN0IGFyZyA9IGFyZ0xpc3QgPyBjb21tYW5kQXJnc1tpXSA6IGNvbW1hbmRBcmdzO1xuICAgICAgICAgIGlmIChhcHAuY29tbWFuZHMuaXNFbmFibGVkKGNtZCwgYXJnKSkge1xuICAgICAgICAgICAgcmV0dXJuIGFwcC5jb21tYW5kcy5leGVjdXRlKGNtZCwgYXJnKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5ydW5BbGxFbmFibGVkLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1J1biBBbGwgRW5hYmxlZCBDb21tYW5kcyBQYXNzZWQgYXMgQXJncycpLFxuICAgICAgZXhlY3V0ZTogYXN5bmMgYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IGNvbW1hbmRzOiBzdHJpbmdbXSA9IGFyZ3MuY29tbWFuZHMgYXMgc3RyaW5nW107XG4gICAgICAgIGNvbnN0IGNvbW1hbmRBcmdzOiBhbnkgPSBhcmdzLmFyZ3M7XG4gICAgICAgIGNvbnN0IGFyZ0xpc3QgPSBBcnJheS5pc0FycmF5KGFyZ3MpO1xuICAgICAgICBjb25zdCBlcnJvcklmTm90RW5hYmxlZDogYm9vbGVhbiA9IGFyZ3MuZXJyb3JJZk5vdEVuYWJsZWQgYXMgYm9vbGVhbjtcbiAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCBjb21tYW5kcy5sZW5ndGg7IGkrKykge1xuICAgICAgICAgIGNvbnN0IGNtZCA9IGNvbW1hbmRzW2ldO1xuICAgICAgICAgIGNvbnN0IGFyZyA9IGFyZ0xpc3QgPyBjb21tYW5kQXJnc1tpXSA6IGNvbW1hbmRBcmdzO1xuICAgICAgICAgIGlmIChhcHAuY29tbWFuZHMuaXNFbmFibGVkKGNtZCwgYXJnKSkge1xuICAgICAgICAgICAgYXdhaXQgYXBwLmNvbW1hbmRzLmV4ZWN1dGUoY21kLCBhcmcpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBpZiAoZXJyb3JJZk5vdEVuYWJsZWQpIHtcbiAgICAgICAgICAgICAgY29uc29sZS5lcnJvcihgJHtjbWR9IGlzIG5vdCBlbmFibGVkLmApO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IEhUTUwgc2FuaXRpemVyLlxuICovXG5jb25zdCBzYW5pdGl6ZXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJU2FuaXRpemVyPiA9IHtcbiAgaWQ6ICdAanVweXRlci9hcHB1dGlscy1leHRlbnNpb246c2FuaXRpemVyJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSVNhbml0aXplcixcbiAgYWN0aXZhdGU6ICgpID0+IHtcbiAgICByZXR1cm4gZGVmYXVsdFNhbml0aXplcjtcbiAgfVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbnMgYXMgZGVmYXVsdC5cbiAqL1xuY29uc3QgcGx1Z2luczogSnVweXRlckZyb250RW5kUGx1Z2luPGFueT5bXSA9IFtcbiAgcGFsZXR0ZSxcbiAgcGFsZXR0ZVJlc3RvcmVyLFxuICBwcmludCxcbiAgcmVzb2x2ZXIsXG4gIHNhbml0aXplcixcbiAgc2V0dGluZ3NQbHVnaW4sXG4gIHN0YXRlLFxuICBzcGxhc2gsXG4gIHNlc3Npb25EaWFsb2dzLFxuICB0aGVtZXNQbHVnaW4sXG4gIHRoZW1lc1BhbGV0dGVNZW51UGx1Z2luLFxuICB0b2dnbGVIZWFkZXIsXG4gIHV0aWxpdHlDb21tYW5kcyxcbiAgd29ya3NwYWNlc1BsdWdpblxuXTtcbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG4iLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cblxuaW1wb3J0IHsgSUxheW91dFJlc3RvcmVyLCBKdXB5dGVyRnJvbnRFbmQgfSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBJQ29tbWFuZFBhbGV0dGUsXG4gIElQYWxldHRlSXRlbSxcbiAgTW9kYWxDb21tYW5kUGFsZXR0ZVxufSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IENvbW1hbmRQYWxldHRlU3ZnLCBwYWxldHRlSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgZmluZCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHsgRGlzcG9zYWJsZURlbGVnYXRlLCBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBDb21tYW5kUGFsZXR0ZSB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIGFwcHV0aWxzIGV4dGVuc2lvbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgYWN0aXZhdGUgPSAnYXBwdXRpbHM6YWN0aXZhdGUtY29tbWFuZC1wYWxldHRlJztcbn1cblxuY29uc3QgUEFMRVRURV9QTFVHSU5fSUQgPSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMtZXh0ZW5zaW9uOnBhbGV0dGUnO1xuXG4vKipcbiAqIEEgdGhpbiB3cmFwcGVyIGFyb3VuZCB0aGUgYENvbW1hbmRQYWxldHRlYCBjbGFzcyB0byBjb25mb3JtIHdpdGggdGhlXG4gKiBKdXB5dGVyTGFiIGludGVyZmFjZSBmb3IgdGhlIGFwcGxpY2F0aW9uLXdpZGUgY29tbWFuZCBwYWxldHRlLlxuICovXG5leHBvcnQgY2xhc3MgUGFsZXR0ZSBpbXBsZW1lbnRzIElDb21tYW5kUGFsZXR0ZSB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBwYWxldHRlIGluc3RhbmNlLlxuICAgKi9cbiAgY29uc3RydWN0b3IocGFsZXR0ZTogQ29tbWFuZFBhbGV0dGUsIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcikge1xuICAgIHRoaXMudHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIHRoaXMuX3BhbGV0dGUgPSBwYWxldHRlO1xuICAgIHRoaXMuX3BhbGV0dGUudGl0bGUubGFiZWwgPSAnJztcbiAgICB0aGlzLl9wYWxldHRlLnRpdGxlLmNhcHRpb24gPSB0cmFucy5fXygnQ29tbWFuZCBQYWxldHRlJyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHBsYWNlaG9sZGVyIHRleHQgb2YgdGhlIGNvbW1hbmQgcGFsZXR0ZSdzIHNlYXJjaCBpbnB1dC5cbiAgICovXG4gIHNldCBwbGFjZWhvbGRlcihwbGFjZWhvbGRlcjogc3RyaW5nKSB7XG4gICAgdGhpcy5fcGFsZXR0ZS5pbnB1dE5vZGUucGxhY2Vob2xkZXIgPSBwbGFjZWhvbGRlcjtcbiAgfVxuICBnZXQgcGxhY2Vob2xkZXIoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fcGFsZXR0ZS5pbnB1dE5vZGUucGxhY2Vob2xkZXI7XG4gIH1cblxuICAvKipcbiAgICogQWN0aXZhdGUgdGhlIGNvbW1hbmQgcGFsZXR0ZSBmb3IgdXNlciBpbnB1dC5cbiAgICovXG4gIGFjdGl2YXRlKCk6IHZvaWQge1xuICAgIHRoaXMuX3BhbGV0dGUuYWN0aXZhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSBjb21tYW5kIGl0ZW0gdG8gdGhlIGNvbW1hbmQgcGFsZXR0ZS5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgb3B0aW9ucyBmb3IgY3JlYXRpbmcgdGhlIGNvbW1hbmQgaXRlbS5cbiAgICpcbiAgICogQHJldHVybnMgQSBkaXNwb3NhYmxlIHRoYXQgd2lsbCByZW1vdmUgdGhlIGl0ZW0gZnJvbSB0aGUgcGFsZXR0ZS5cbiAgICovXG4gIGFkZEl0ZW0ob3B0aW9uczogSVBhbGV0dGVJdGVtKTogSURpc3Bvc2FibGUge1xuICAgIGNvbnN0IGl0ZW0gPSB0aGlzLl9wYWxldHRlLmFkZEl0ZW0ob3B0aW9ucyBhcyBDb21tYW5kUGFsZXR0ZS5JSXRlbU9wdGlvbnMpO1xuICAgIHJldHVybiBuZXcgRGlzcG9zYWJsZURlbGVnYXRlKCgpID0+IHtcbiAgICAgIHRoaXMuX3BhbGV0dGUucmVtb3ZlSXRlbShpdGVtKTtcbiAgICB9KTtcbiAgfVxuXG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfcGFsZXR0ZTogQ29tbWFuZFBhbGV0dGU7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGBQYWxldHRlYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFBhbGV0dGUge1xuICAvKipcbiAgICogQWN0aXZhdGUgdGhlIGNvbW1hbmQgcGFsZXR0ZS5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhY3RpdmF0ZShcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsXG4gICk6IElDb21tYW5kUGFsZXR0ZSB7XG4gICAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHBhbGV0dGUgPSBQcml2YXRlLmNyZWF0ZVBhbGV0dGUoYXBwLCB0cmFuc2xhdG9yKTtcbiAgICBjb25zdCBtb2RhbFBhbGV0dGUgPSBuZXcgTW9kYWxDb21tYW5kUGFsZXR0ZSh7IGNvbW1hbmRQYWxldHRlOiBwYWxldHRlIH0pO1xuICAgIGxldCBtb2RhbCA9IGZhbHNlO1xuXG4gICAgcGFsZXR0ZS5ub2RlLnNldEF0dHJpYnV0ZSgncm9sZScsICdyZWdpb24nKTtcbiAgICBwYWxldHRlLm5vZGUuc2V0QXR0cmlidXRlKFxuICAgICAgJ2FyaWEtbGFiZWwnLFxuICAgICAgdHJhbnMuX18oJ0NvbW1hbmQgUGFsZXR0ZSBTZWN0aW9uJylcbiAgICApO1xuICAgIHNoZWxsLmFkZChwYWxldHRlLCAnbGVmdCcsIHsgcmFuazogMzAwIH0pO1xuXG4gICAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgICAgY29uc3QgbG9hZFNldHRpbmdzID0gc2V0dGluZ1JlZ2lzdHJ5LmxvYWQoUEFMRVRURV9QTFVHSU5fSUQpO1xuICAgICAgY29uc3QgdXBkYXRlU2V0dGluZ3MgPSAoc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzKTogdm9pZCA9PiB7XG4gICAgICAgIGNvbnN0IG5ld01vZGFsID0gc2V0dGluZ3MuZ2V0KCdtb2RhbCcpLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgICBpZiAobW9kYWwgJiYgIW5ld01vZGFsKSB7XG4gICAgICAgICAgcGFsZXR0ZS5wYXJlbnQgPSBudWxsO1xuICAgICAgICAgIG1vZGFsUGFsZXR0ZS5kZXRhY2goKTtcbiAgICAgICAgICBzaGVsbC5hZGQocGFsZXR0ZSwgJ2xlZnQnLCB7IHJhbms6IDMwMCB9KTtcbiAgICAgICAgfSBlbHNlIGlmICghbW9kYWwgJiYgbmV3TW9kYWwpIHtcbiAgICAgICAgICBwYWxldHRlLnBhcmVudCA9IG51bGw7XG4gICAgICAgICAgbW9kYWxQYWxldHRlLnBhbGV0dGUgPSBwYWxldHRlO1xuICAgICAgICAgIHBhbGV0dGUuc2hvdygpO1xuICAgICAgICAgIG1vZGFsUGFsZXR0ZS5hdHRhY2goKTtcbiAgICAgICAgfVxuICAgICAgICBtb2RhbCA9IG5ld01vZGFsO1xuICAgICAgfTtcblxuICAgICAgUHJvbWlzZS5hbGwoW2xvYWRTZXR0aW5ncywgYXBwLnJlc3RvcmVkXSlcbiAgICAgICAgLnRoZW4oKFtzZXR0aW5nc10pID0+IHtcbiAgICAgICAgICB1cGRhdGVTZXR0aW5ncyhzZXR0aW5ncyk7XG4gICAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KHNldHRpbmdzID0+IHtcbiAgICAgICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgICAgICB9KTtcbiAgICAgICAgfSlcbiAgICAgICAgLmNhdGNoKChyZWFzb246IEVycm9yKSA9PiB7XG4gICAgICAgICAgY29uc29sZS5lcnJvcihyZWFzb24ubWVzc2FnZSk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIC8vIFNob3cgdGhlIGN1cnJlbnQgcGFsZXR0ZSBzaG9ydGN1dCBpbiBpdHMgdGl0bGUuXG4gICAgY29uc3QgdXBkYXRlUGFsZXR0ZVRpdGxlID0gKCkgPT4ge1xuICAgICAgY29uc3QgYmluZGluZyA9IGZpbmQoXG4gICAgICAgIGFwcC5jb21tYW5kcy5rZXlCaW5kaW5ncyxcbiAgICAgICAgYiA9PiBiLmNvbW1hbmQgPT09IENvbW1hbmRJRHMuYWN0aXZhdGVcbiAgICAgICk7XG4gICAgICBpZiAoYmluZGluZykge1xuICAgICAgICBjb25zdCBrcyA9IENvbW1hbmRSZWdpc3RyeS5mb3JtYXRLZXlzdHJva2UoYmluZGluZy5rZXlzLmpvaW4oJyAnKSk7XG4gICAgICAgIHBhbGV0dGUudGl0bGUuY2FwdGlvbiA9IHRyYW5zLl9fKCdDb21tYW5kcyAoJTEpJywga3MpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcGFsZXR0ZS50aXRsZS5jYXB0aW9uID0gdHJhbnMuX18oJ0NvbW1hbmRzJyk7XG4gICAgICB9XG4gICAgfTtcbiAgICB1cGRhdGVQYWxldHRlVGl0bGUoKTtcbiAgICBhcHAuY29tbWFuZHMua2V5QmluZGluZ0NoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICB1cGRhdGVQYWxldHRlVGl0bGUoKTtcbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5hY3RpdmF0ZSwge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBpZiAobW9kYWwpIHtcbiAgICAgICAgICBtb2RhbFBhbGV0dGUuYWN0aXZhdGUoKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBzaGVsbC5hY3RpdmF0ZUJ5SWQocGFsZXR0ZS5pZCk7XG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0FjdGl2YXRlIENvbW1hbmQgUGFsZXR0ZScpXG4gICAgfSk7XG5cbiAgICBwYWxldHRlLmlucHV0Tm9kZS5wbGFjZWhvbGRlciA9IHRyYW5zLl9fKCdTRUFSQ0gnKTtcblxuICAgIHJldHVybiBuZXcgUGFsZXR0ZShwYWxldHRlLCB0cmFuc2xhdG9yKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXN0b3JlIHRoZSBjb21tYW5kIHBhbGV0dGUuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcmVzdG9yZShcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICk6IHZvaWQge1xuICAgIGNvbnN0IHBhbGV0dGUgPSBQcml2YXRlLmNyZWF0ZVBhbGV0dGUoYXBwLCB0cmFuc2xhdG9yKTtcbiAgICAvLyBMZXQgdGhlIGFwcGxpY2F0aW9uIHJlc3RvcmVyIHRyYWNrIHRoZSBjb21tYW5kIHBhbGV0dGUgZm9yIHJlc3RvcmF0aW9uIG9mXG4gICAgLy8gYXBwbGljYXRpb24gc3RhdGUgKGUuZy4gc2V0dGluZyB0aGUgY29tbWFuZCBwYWxldHRlIGFzIHRoZSBjdXJyZW50IHNpZGUgYmFyXG4gICAgLy8gd2lkZ2V0KS5cbiAgICByZXN0b3Jlci5hZGQocGFsZXR0ZSwgJ2NvbW1hbmQtcGFsZXR0ZScpO1xuICB9XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgbW9kdWxlIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogVGhlIHByaXZhdGUgY29tbWFuZCBwYWxldHRlIGluc3RhbmNlLlxuICAgKi9cbiAgbGV0IHBhbGV0dGU6IENvbW1hbmRQYWxldHRlO1xuXG4gIC8qKlxuICAgKiBDcmVhdGUgdGhlIGFwcGxpY2F0aW9uLXdpZGUgY29tbWFuZCBwYWxldHRlLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZVBhbGV0dGUoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKTogQ29tbWFuZFBhbGV0dGUge1xuICAgIGlmICghcGFsZXR0ZSkge1xuICAgICAgLy8gdXNlIGEgcmVuZGVyZXIgdHdlYWtlZCB0byB1c2UgaW5saW5lIHN2ZyBpY29uc1xuICAgICAgcGFsZXR0ZSA9IG5ldyBDb21tYW5kUGFsZXR0ZSh7XG4gICAgICAgIGNvbW1hbmRzOiBhcHAuY29tbWFuZHMsXG4gICAgICAgIHJlbmRlcmVyOiBDb21tYW5kUGFsZXR0ZVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgIH0pO1xuICAgICAgcGFsZXR0ZS5pZCA9ICdjb21tYW5kLXBhbGV0dGUnO1xuICAgICAgcGFsZXR0ZS50aXRsZS5pY29uID0gcGFsZXR0ZUljb247XG4gICAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgICAgcGFsZXR0ZS50aXRsZS5sYWJlbCA9IHRyYW5zLl9fKCdDb21tYW5kcycpO1xuICAgIH1cblxuICAgIHJldHVybiBwYWxldHRlO1xuICB9XG59XG4iLCJpbXBvcnQgeyBQYWdlQ29uZmlnIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgRGF0YUNvbm5lY3RvciwgSURhdGFDb25uZWN0b3IgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7IFRocm90dGxlciB9IGZyb20gJ0BsdW1pbm8vcG9sbGluZyc7XG5cbi8qKlxuICogQSBkYXRhIGNvbm5lY3RvciBmb3IgZmV0Y2hpbmcgc2V0dGluZ3MuXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhpcyBjb25uZWN0b3IgYWRkcyBhIHF1ZXJ5IHBhcmFtZXRlciB0byB0aGUgYmFzZSBzZXJ2aWNlcyBzZXR0aW5nIG1hbmFnZXIuXG4gKi9cbmV4cG9ydCBjbGFzcyBTZXR0aW5nQ29ubmVjdG9yIGV4dGVuZHMgRGF0YUNvbm5lY3RvcjxcbiAgSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luLFxuICBzdHJpbmdcbj4ge1xuICBjb25zdHJ1Y3Rvcihjb25uZWN0b3I6IElEYXRhQ29ubmVjdG9yPElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbiwgc3RyaW5nPikge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5fY29ubmVjdG9yID0gY29ubmVjdG9yO1xuICB9XG5cbiAgLyoqXG4gICAqIEZldGNoIHNldHRpbmdzIGZvciBhIHBsdWdpbi5cbiAgICogQHBhcmFtIGlkIC0gVGhlIHBsdWdpbiBJRFxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBSRVNUIEFQSSByZXF1ZXN0cyBhcmUgdGhyb3R0bGVkIGF0IG9uZSByZXF1ZXN0IHBlciBwbHVnaW4gcGVyIDEwMG1zLlxuICAgKi9cbiAgZmV0Y2goaWQ6IHN0cmluZyk6IFByb21pc2U8SVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luIHwgdW5kZWZpbmVkPiB7XG4gICAgY29uc3QgdGhyb3R0bGVycyA9IHRoaXMuX3Rocm90dGxlcnM7XG4gICAgaWYgKCEoaWQgaW4gdGhyb3R0bGVycykpIHtcbiAgICAgIHRocm90dGxlcnNbaWRdID0gbmV3IFRocm90dGxlcigoKSA9PiB0aGlzLl9jb25uZWN0b3IuZmV0Y2goaWQpLCAxMDApO1xuICAgIH1cbiAgICByZXR1cm4gdGhyb3R0bGVyc1tpZF0uaW52b2tlKCk7XG4gIH1cblxuICBhc3luYyBsaXN0KFxuICAgIHF1ZXJ5OiAnYWN0aXZlJyB8ICdhbGwnID0gJ2FsbCdcbiAgKTogUHJvbWlzZTx7IGlkczogc3RyaW5nW107IHZhbHVlczogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luW10gfT4ge1xuICAgIGNvbnN0IHsgaXNEZWZlcnJlZCwgaXNEaXNhYmxlZCB9ID0gUGFnZUNvbmZpZy5FeHRlbnNpb247XG4gICAgY29uc3QgeyBpZHMsIHZhbHVlcyB9ID0gYXdhaXQgdGhpcy5fY29ubmVjdG9yLmxpc3QoKTtcblxuICAgIGlmIChxdWVyeSA9PT0gJ2FsbCcpIHtcbiAgICAgIHJldHVybiB7IGlkcywgdmFsdWVzIH07XG4gICAgfVxuXG4gICAgcmV0dXJuIHtcbiAgICAgIGlkczogaWRzLmZpbHRlcihpZCA9PiAhaXNEZWZlcnJlZChpZCkgJiYgIWlzRGlzYWJsZWQoaWQpKSxcbiAgICAgIHZhbHVlczogdmFsdWVzLmZpbHRlcigoeyBpZCB9KSA9PiAhaXNEZWZlcnJlZChpZCkgJiYgIWlzRGlzYWJsZWQoaWQpKVxuICAgIH07XG4gIH1cblxuICBhc3luYyBzYXZlKGlkOiBzdHJpbmcsIHJhdzogc3RyaW5nKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgYXdhaXQgdGhpcy5fY29ubmVjdG9yLnNhdmUoaWQsIHJhdyk7XG4gIH1cblxuICBwcml2YXRlIF9jb25uZWN0b3I6IElEYXRhQ29ubmVjdG9yPElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbiwgc3RyaW5nPjtcbiAgcHJpdmF0ZSBfdGhyb3R0bGVyczogeyBba2V5OiBzdHJpbmddOiBUaHJvdHRsZXIgfSA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG59XG4iLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cblxuaW1wb3J0IHtcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgUGFnZUNvbmZpZyB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5LCBTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgU2V0dGluZ0Nvbm5lY3RvciB9IGZyb20gJy4vc2V0dGluZ2Nvbm5lY3Rvcic7XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgc2V0dGluZyByZWdpc3RyeSBwcm92aWRlci5cbiAqL1xuZXhwb3J0IGNvbnN0IHNldHRpbmdzUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SVNldHRpbmdSZWdpc3RyeT4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMtZXh0ZW5zaW9uOnNldHRpbmdzJyxcbiAgYWN0aXZhdGU6IGFzeW5jIChhcHA6IEp1cHl0ZXJGcm9udEVuZCk6IFByb21pc2U8SVNldHRpbmdSZWdpc3RyeT4gPT4ge1xuICAgIGNvbnN0IHsgaXNEaXNhYmxlZCB9ID0gUGFnZUNvbmZpZy5FeHRlbnNpb247XG4gICAgY29uc3QgY29ubmVjdG9yID0gbmV3IFNldHRpbmdDb25uZWN0b3IoYXBwLnNlcnZpY2VNYW5hZ2VyLnNldHRpbmdzKTtcblxuICAgIGNvbnN0IHJlZ2lzdHJ5ID0gbmV3IFNldHRpbmdSZWdpc3RyeSh7XG4gICAgICBjb25uZWN0b3IsXG4gICAgICBwbHVnaW5zOiAoYXdhaXQgY29ubmVjdG9yLmxpc3QoJ2FjdGl2ZScpKS52YWx1ZXNcbiAgICB9KTtcblxuICAgIC8vIElmIHRoZXJlIGFyZSBwbHVnaW5zIHRoYXQgaGF2ZSBzY2hlbWFzIHRoYXQgYXJlIG5vdCBpbiB0aGUgc2V0dGluZ1xuICAgIC8vIHJlZ2lzdHJ5IGFmdGVyIHRoZSBhcHBsaWNhdGlvbiBoYXMgcmVzdG9yZWQsIHRyeSB0byBsb2FkIHRoZW0gbWFudWFsbHlcbiAgICAvLyBiZWNhdXNlIG90aGVyd2lzZSwgaXRzIHNldHRpbmdzIHdpbGwgbmV2ZXIgYmVjb21lIGF2YWlsYWJsZSBpbiB0aGVcbiAgICAvLyBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgIHZvaWQgYXBwLnJlc3RvcmVkLnRoZW4oYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3QgcGx1Z2lucyA9IGF3YWl0IGNvbm5lY3Rvci5saXN0KCdhbGwnKTtcbiAgICAgIHBsdWdpbnMuaWRzLmZvckVhY2goYXN5bmMgKGlkLCBpbmRleCkgPT4ge1xuICAgICAgICBpZiAoaXNEaXNhYmxlZChpZCkgfHwgaWQgaW4gcmVnaXN0cnkucGx1Z2lucykge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgYXdhaXQgcmVnaXN0cnkubG9hZChpZCk7XG4gICAgICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgICAgY29uc29sZS53YXJuKGBTZXR0aW5ncyBmYWlsZWQgdG8gbG9hZCBmb3IgKCR7aWR9KWAsIGVycm9yKTtcbiAgICAgICAgICBpZiAocGx1Z2lucy52YWx1ZXNbaW5kZXhdLnNjaGVtYVsnanVweXRlci5sYWIudHJhbnNmb3JtJ10pIHtcbiAgICAgICAgICAgIGNvbnNvbGUud2FybihcbiAgICAgICAgICAgICAgYFRoaXMgbWF5IGhhcHBlbiBpZiB7YXV0b1N0YXJ0OiBmYWxzZX0gaW4gKCR7aWR9KSBgICtcbiAgICAgICAgICAgICAgICBgb3IgaWYgaXQgaXMgb25lIG9mIHRoZSBkZWZlcnJlZEV4dGVuc2lvbnMgaW4gcGFnZSBjb25maWcuYFxuICAgICAgICAgICAgKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH0pO1xuXG4gICAgcmV0dXJuIHJlZ2lzdHJ5O1xuICB9LFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJU2V0dGluZ1JlZ2lzdHJ5XG59O1xuIiwiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG5cbmltcG9ydCB7XG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgSVNwbGFzaFNjcmVlbixcbiAgSVRoZW1lTWFuYWdlcixcbiAgVGhlbWVNYW5hZ2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFBhZ2VDb25maWcsIFVSTEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJTWFpbk1lbnUgfSBmcm9tICdAanVweXRlcmxhYi9tYWlubWVudSc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjaGFuZ2VUaGVtZSA9ICdhcHB1dGlsczpjaGFuZ2UtdGhlbWUnO1xuXG4gIGV4cG9ydCBjb25zdCB0aGVtZVNjcm9sbGJhcnMgPSAnYXBwdXRpbHM6dGhlbWUtc2Nyb2xsYmFycyc7XG5cbiAgZXhwb3J0IGNvbnN0IGNoYW5nZUZvbnQgPSAnYXBwdXRpbHM6Y2hhbmdlLWZvbnQnO1xuXG4gIGV4cG9ydCBjb25zdCBpbmNyRm9udFNpemUgPSAnYXBwdXRpbHM6aW5jci1mb250LXNpemUnO1xuXG4gIGV4cG9ydCBjb25zdCBkZWNyRm9udFNpemUgPSAnYXBwdXRpbHM6ZGVjci1mb250LXNpemUnO1xufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IHRoZW1lIG1hbmFnZXIgcHJvdmlkZXIuXG4gKi9cbmV4cG9ydCBjb25zdCB0aGVtZXNQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJVGhlbWVNYW5hZ2VyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHB1dGlscy1leHRlbnNpb246dGhlbWVzJyxcbiAgcmVxdWlyZXM6IFtJU2V0dGluZ1JlZ2lzdHJ5LCBKdXB5dGVyRnJvbnRFbmQuSVBhdGhzLCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSVNwbGFzaFNjcmVlbl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgcGF0aHM6IEp1cHl0ZXJGcm9udEVuZC5JUGF0aHMsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgc3BsYXNoOiBJU3BsYXNoU2NyZWVuIHwgbnVsbFxuICApOiBJVGhlbWVNYW5hZ2VyID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IGhvc3QgPSBhcHAuc2hlbGw7XG4gICAgY29uc3QgY29tbWFuZHMgPSBhcHAuY29tbWFuZHM7XG4gICAgY29uc3QgdXJsID0gVVJMRXh0LmpvaW4oUGFnZUNvbmZpZy5nZXRCYXNlVXJsKCksIHBhdGhzLnVybHMudGhlbWVzKTtcbiAgICBjb25zdCBrZXkgPSB0aGVtZXNQbHVnaW4uaWQ7XG4gICAgY29uc3QgbWFuYWdlciA9IG5ldyBUaGVtZU1hbmFnZXIoe1xuICAgICAga2V5LFxuICAgICAgaG9zdCxcbiAgICAgIHNldHRpbmdzLFxuICAgICAgc3BsYXNoOiBzcGxhc2ggPz8gdW5kZWZpbmVkLFxuICAgICAgdXJsXG4gICAgfSk7XG5cbiAgICAvLyBLZWVwIGEgc3luY2hyb25vdXNseSBzZXQgcmVmZXJlbmNlIHRvIHRoZSBjdXJyZW50IHRoZW1lLFxuICAgIC8vIHNpbmNlIHRoZSBhc3luY2hyb25vdXMgc2V0dGluZyBvZiB0aGUgdGhlbWUgaW4gYGNoYW5nZVRoZW1lYFxuICAgIC8vIGNhbiBsZWFkIHRvIGFuIGluY29ycmVjdCB0b2dnbGUgb24gdGhlIGN1cnJlbnRseSB1c2VkIHRoZW1lLlxuICAgIGxldCBjdXJyZW50VGhlbWU6IHN0cmluZztcblxuICAgIG1hbmFnZXIudGhlbWVDaGFuZ2VkLmNvbm5lY3QoKHNlbmRlciwgYXJncykgPT4ge1xuICAgICAgLy8gU2V0IGRhdGEgYXR0cmlidXRlcyBvbiB0aGUgYXBwbGljYXRpb24gc2hlbGwgZm9yIHRoZSBjdXJyZW50IHRoZW1lLlxuICAgICAgY3VycmVudFRoZW1lID0gYXJncy5uZXdWYWx1ZTtcbiAgICAgIGRvY3VtZW50LmJvZHkuZGF0YXNldC5qcFRoZW1lTGlnaHQgPSBTdHJpbmcoXG4gICAgICAgIG1hbmFnZXIuaXNMaWdodChjdXJyZW50VGhlbWUpXG4gICAgICApO1xuICAgICAgZG9jdW1lbnQuYm9keS5kYXRhc2V0LmpwVGhlbWVOYW1lID0gY3VycmVudFRoZW1lO1xuICAgICAgaWYgKFxuICAgICAgICBkb2N1bWVudC5ib2R5LmRhdGFzZXQuanBUaGVtZVNjcm9sbGJhcnMgIT09XG4gICAgICAgIFN0cmluZyhtYW5hZ2VyLnRoZW1lU2Nyb2xsYmFycyhjdXJyZW50VGhlbWUpKVxuICAgICAgKSB7XG4gICAgICAgIGRvY3VtZW50LmJvZHkuZGF0YXNldC5qcFRoZW1lU2Nyb2xsYmFycyA9IFN0cmluZyhcbiAgICAgICAgICBtYW5hZ2VyLnRoZW1lU2Nyb2xsYmFycyhjdXJyZW50VGhlbWUpXG4gICAgICAgICk7XG4gICAgICB9XG5cbiAgICAgIGNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKENvbW1hbmRJRHMuY2hhbmdlVGhlbWUpO1xuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNoYW5nZVRoZW1lLCB7XG4gICAgICBsYWJlbDogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IHRoZW1lID0gYXJnc1sndGhlbWUnXSBhcyBzdHJpbmc7XG4gICAgICAgIGNvbnN0IGRpc3BsYXlOYW1lID0gbWFuYWdlci5nZXREaXNwbGF5TmFtZSh0aGVtZSk7XG4gICAgICAgIHJldHVybiBhcmdzWydpc1BhbGV0dGUnXVxuICAgICAgICAgID8gdHJhbnMuX18oJ1VzZSBUaGVtZTogJTEnLCBkaXNwbGF5TmFtZSlcbiAgICAgICAgICA6IGRpc3BsYXlOYW1lO1xuICAgICAgfSxcbiAgICAgIGlzVG9nZ2xlZDogYXJncyA9PiBhcmdzWyd0aGVtZSddID09PSBjdXJyZW50VGhlbWUsXG4gICAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgdGhlbWUgPSBhcmdzWyd0aGVtZSddIGFzIHN0cmluZztcbiAgICAgICAgaWYgKHRoZW1lID09PSBtYW5hZ2VyLnRoZW1lKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBtYW5hZ2VyLnNldFRoZW1lKHRoZW1lKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50aGVtZVNjcm9sbGJhcnMsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnVGhlbWUgU2Nyb2xsYmFycycpLFxuICAgICAgaXNUb2dnbGVkOiAoKSA9PiBtYW5hZ2VyLmlzVG9nZ2xlZFRoZW1lU2Nyb2xsYmFycygpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4gbWFuYWdlci50b2dnbGVUaGVtZVNjcm9sbGJhcnMoKVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNoYW5nZUZvbnQsIHtcbiAgICAgIGxhYmVsOiBhcmdzID0+XG4gICAgICAgIGFyZ3NbJ2VuYWJsZWQnXSA/IGAke2FyZ3NbJ2ZvbnQnXX1gIDogdHJhbnMuX18oJ3dhaXRpbmcgZm9yIGZvbnRzJyksXG4gICAgICBpc0VuYWJsZWQ6IGFyZ3MgPT4gYXJnc1snZW5hYmxlZCddIGFzIGJvb2xlYW4sXG4gICAgICBpc1RvZ2dsZWQ6IGFyZ3MgPT4gbWFuYWdlci5nZXRDU1MoYXJnc1sna2V5J10gYXMgc3RyaW5nKSA9PT0gYXJnc1snZm9udCddLFxuICAgICAgZXhlY3V0ZTogYXJncyA9PlxuICAgICAgICBtYW5hZ2VyLnNldENTU092ZXJyaWRlKGFyZ3NbJ2tleSddIGFzIHN0cmluZywgYXJnc1snZm9udCddIGFzIHN0cmluZylcbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5pbmNyRm9udFNpemUsIHtcbiAgICAgIGxhYmVsOiBhcmdzID0+IHtcbiAgICAgICAgc3dpdGNoIChhcmdzLmtleSkge1xuICAgICAgICAgIGNhc2UgJ2NvZGUtZm9udC1zaXplJzpcbiAgICAgICAgICAgIHJldHVybiB0cmFucy5fXygnSW5jcmVhc2UgQ29kZSBGb250IFNpemUnKTtcbiAgICAgICAgICBjYXNlICdjb250ZW50LWZvbnQtc2l6ZTEnOlxuICAgICAgICAgICAgcmV0dXJuIHRyYW5zLl9fKCdJbmNyZWFzZSBDb250ZW50IEZvbnQgU2l6ZScpO1xuICAgICAgICAgIGNhc2UgJ3VpLWZvbnQtc2l6ZTEnOlxuICAgICAgICAgICAgcmV0dXJuIHRyYW5zLl9fKCdJbmNyZWFzZSBVSSBGb250IFNpemUnKTtcbiAgICAgICAgICBkZWZhdWx0OlxuICAgICAgICAgICAgcmV0dXJuIHRyYW5zLl9fKCdJbmNyZWFzZSBGb250IFNpemUnKTtcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4gbWFuYWdlci5pbmNyRm9udFNpemUoYXJnc1sna2V5J10gYXMgc3RyaW5nKVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmRlY3JGb250U2l6ZSwge1xuICAgICAgbGFiZWw6IGFyZ3MgPT4ge1xuICAgICAgICBzd2l0Y2ggKGFyZ3Mua2V5KSB7XG4gICAgICAgICAgY2FzZSAnY29kZS1mb250LXNpemUnOlxuICAgICAgICAgICAgcmV0dXJuIHRyYW5zLl9fKCdEZWNyZWFzZSBDb2RlIEZvbnQgU2l6ZScpO1xuICAgICAgICAgIGNhc2UgJ2NvbnRlbnQtZm9udC1zaXplMSc6XG4gICAgICAgICAgICByZXR1cm4gdHJhbnMuX18oJ0RlY3JlYXNlIENvbnRlbnQgRm9udCBTaXplJyk7XG4gICAgICAgICAgY2FzZSAndWktZm9udC1zaXplMSc6XG4gICAgICAgICAgICByZXR1cm4gdHJhbnMuX18oJ0RlY3JlYXNlIFVJIEZvbnQgU2l6ZScpO1xuICAgICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICByZXR1cm4gdHJhbnMuX18oJ0RlY3JlYXNlIEZvbnQgU2l6ZScpO1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAgZXhlY3V0ZTogYXJncyA9PiBtYW5hZ2VyLmRlY3JGb250U2l6ZShhcmdzWydrZXknXSBhcyBzdHJpbmcpXG4gICAgfSk7XG5cbiAgICByZXR1cm4gbWFuYWdlcjtcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSVRoZW1lTWFuYWdlclxufTtcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCB0aGVtZSBtYW5hZ2VyJ3MgVUkgY29tbWFuZCBwYWxldHRlIGFuZCBtYWluIG1lbnUgZnVuY3Rpb25hbGl0eS5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiBUaGlzIHBsdWdpbiBsb2FkcyBzZXBhcmF0ZWx5IGZyb20gdGhlIHRoZW1lIG1hbmFnZXIgcGx1Z2luIGluIG9yZGVyIHRvXG4gKiBwcmV2ZW50IGJsb2NraW5nIG9mIHRoZSB0aGVtZSBtYW5hZ2VyIHdoaWxlIGl0IHdhaXRzIGZvciB0aGUgY29tbWFuZCBwYWxldHRlXG4gKiBhbmQgbWFpbiBtZW51IHRvIGJlY29tZSBhdmFpbGFibGUuXG4gKi9cbmV4cG9ydCBjb25zdCB0aGVtZXNQYWxldHRlTWVudVBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcHV0aWxzLWV4dGVuc2lvbjp0aGVtZXMtcGFsZXR0ZS1tZW51JyxcbiAgcmVxdWlyZXM6IFtJVGhlbWVNYW5hZ2VyLCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUNvbW1hbmRQYWxldHRlLCBJTWFpbk1lbnVdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElUaGVtZU1hbmFnZXIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgICBtYWluTWVudTogSU1haW5NZW51IHwgbnVsbFxuICApOiB2b2lkID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgLy8gSWYgd2UgaGF2ZSBhIG1haW4gbWVudSwgYWRkIHRoZSB0aGVtZSBtYW5hZ2VyIHRvIHRoZSBzZXR0aW5ncyBtZW51LlxuICAgIGlmIChtYWluTWVudSkge1xuICAgICAgdm9pZCBhcHAucmVzdG9yZWQudGhlbigoKSA9PiB7XG4gICAgICAgIGNvbnN0IGlzUGFsZXR0ZSA9IGZhbHNlO1xuXG4gICAgICAgIGNvbnN0IHRoZW1lTWVudSA9IG1haW5NZW51LnNldHRpbmdzTWVudS5pdGVtcy5maW5kKFxuICAgICAgICAgIGl0ZW0gPT5cbiAgICAgICAgICAgIGl0ZW0udHlwZSA9PT0gJ3N1Ym1lbnUnICYmXG4gICAgICAgICAgICBpdGVtLnN1Ym1lbnU/LmlkID09PSAnanAtbWFpbm1lbnUtc2V0dGluZ3MtYXBwdXRpbHN0aGVtZSdcbiAgICAgICAgKT8uc3VibWVudTtcblxuICAgICAgICAvLyBjaG9vc2UgYSB0aGVtZVxuICAgICAgICBpZiAodGhlbWVNZW51KSB7XG4gICAgICAgICAgbWFuYWdlci50aGVtZXMuZm9yRWFjaCgodGhlbWUsIGluZGV4KSA9PiB7XG4gICAgICAgICAgICB0aGVtZU1lbnUuaW5zZXJ0SXRlbShpbmRleCwge1xuICAgICAgICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLmNoYW5nZVRoZW1lLFxuICAgICAgICAgICAgICBhcmdzOiB7IGlzUGFsZXR0ZSwgdGhlbWUgfVxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH1cblxuICAgIC8vIElmIHdlIGhhdmUgYSBjb21tYW5kIHBhbGV0dGUsIGFkZCB0aGVtZSBzd2l0Y2hpbmcgb3B0aW9ucyB0byBpdC5cbiAgICBpZiAocGFsZXR0ZSkge1xuICAgICAgdm9pZCBhcHAucmVzdG9yZWQudGhlbigoKSA9PiB7XG4gICAgICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ1RoZW1lJyk7XG4gICAgICAgIGNvbnN0IGNvbW1hbmQgPSBDb21tYW5kSURzLmNoYW5nZVRoZW1lO1xuICAgICAgICBjb25zdCBpc1BhbGV0dGUgPSB0cnVlO1xuXG4gICAgICAgIC8vIGNob29zZSBhIHRoZW1lXG4gICAgICAgIG1hbmFnZXIudGhlbWVzLmZvckVhY2godGhlbWUgPT4ge1xuICAgICAgICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNvbW1hbmQsIGFyZ3M6IHsgaXNQYWxldHRlLCB0aGVtZSB9LCBjYXRlZ29yeSB9KTtcbiAgICAgICAgfSk7XG5cbiAgICAgICAgLy8gdG9nZ2xlIHNjcm9sbGJhciB0aGVtaW5nXG4gICAgICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNvbW1hbmQ6IENvbW1hbmRJRHMudGhlbWVTY3JvbGxiYXJzLCBjYXRlZ29yeSB9KTtcblxuICAgICAgICAvLyBpbmNyZWFzZS9kZWNyZWFzZSBjb2RlIGZvbnQgc2l6ZVxuICAgICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuaW5jckZvbnRTaXplLFxuICAgICAgICAgIGFyZ3M6IHtcbiAgICAgICAgICAgIGtleTogJ2NvZGUtZm9udC1zaXplJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgY2F0ZWdvcnlcbiAgICAgICAgfSk7XG4gICAgICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5kZWNyRm9udFNpemUsXG4gICAgICAgICAgYXJnczoge1xuICAgICAgICAgICAga2V5OiAnY29kZS1mb250LXNpemUnXG4gICAgICAgICAgfSxcbiAgICAgICAgICBjYXRlZ29yeVxuICAgICAgICB9KTtcbiAgICAgICAgLy8gaW5jcmVhc2UvZGVjcmVhc2UgY29udGVudCBmb250IHNpemVcbiAgICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLmluY3JGb250U2l6ZSxcbiAgICAgICAgICBhcmdzOiB7XG4gICAgICAgICAgICBrZXk6ICdjb250ZW50LWZvbnQtc2l6ZTEnXG4gICAgICAgICAgfSxcbiAgICAgICAgICBjYXRlZ29yeVxuICAgICAgICB9KTtcbiAgICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLmRlY3JGb250U2l6ZSxcbiAgICAgICAgICBhcmdzOiB7XG4gICAgICAgICAgICBrZXk6ICdjb250ZW50LWZvbnQtc2l6ZTEnXG4gICAgICAgICAgfSxcbiAgICAgICAgICBjYXRlZ29yeVxuICAgICAgICB9KTtcbiAgICAgICAgLy8gaW5jcmVhc2UvZGVjcmVhc2UgdWkgZm9udCBzaXplXG4gICAgICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5pbmNyRm9udFNpemUsXG4gICAgICAgICAgYXJnczoge1xuICAgICAgICAgICAga2V5OiAndWktZm9udC1zaXplMSdcbiAgICAgICAgICB9LFxuICAgICAgICAgIGNhdGVnb3J5XG4gICAgICAgIH0pO1xuICAgICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuZGVjckZvbnRTaXplLFxuICAgICAgICAgIGFyZ3M6IHtcbiAgICAgICAgICAgIGtleTogJ3VpLWZvbnQtc2l6ZTEnXG4gICAgICAgICAgfSxcbiAgICAgICAgICBjYXRlZ29yeVxuICAgICAgICB9KTtcbiAgICAgIH0pO1xuICAgIH1cbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQge1xuICBJUm91dGVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBEaWFsb2csIElXaW5kb3dSZXNvbHZlciwgc2hvd0RpYWxvZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFVSTEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBBQkNXaWRnZXRGYWN0b3J5LFxuICBEb2N1bWVudFJlZ2lzdHJ5LFxuICBEb2N1bWVudFdpZGdldCxcbiAgSURvY3VtZW50V2lkZ2V0XG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IEZpbGVCcm93c2VyLCBJRmlsZUJyb3dzZXJGYWN0b3J5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXInO1xuaW1wb3J0IHtcbiAgQ29udGVudHNNYW5hZ2VyLFxuICBXb3Jrc3BhY2UsXG4gIFdvcmtzcGFjZU1hbmFnZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgSVN0YXRlREIgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbm5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IHNhdmVXb3Jrc3BhY2UgPSAnd29ya3NwYWNlLXVpOnNhdmUnO1xuXG4gIGV4cG9ydCBjb25zdCBzYXZlV29ya3NwYWNlQXMgPSAnd29ya3NwYWNlLXVpOnNhdmUtYXMnO1xufVxuXG5jb25zdCBXT1JLU1BBQ0VfTkFNRSA9ICdqdXB5dGVybGFiLXdvcmtzcGFjZSc7XG5jb25zdCBXT1JLU1BBQ0VfRVhUID0gJy4nICsgV09SS1NQQUNFX05BTUU7XG5jb25zdCBMQVNUX1NBVkVfSUQgPSAnd29ya3NwYWNlLXVpOmxhc3RTYXZlJztcbmNvbnN0IElDT05fTkFNRSA9ICdqcC1KdXB5dGVySWNvbic7XG5cbi8qKlxuICogVGhlIHdvcmtzcGFjZSBNSU1FIHJlbmRlcmVyIGFuZCBzYXZlIHBsdWdpbi5cbiAqL1xuZXhwb3J0IGNvbnN0IHdvcmtzcGFjZXNQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHB1dGlscy1leHRlbnNpb246d29ya3NwYWNlcycsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtcbiAgICBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIElXaW5kb3dSZXNvbHZlcixcbiAgICBJU3RhdGVEQixcbiAgICBJVHJhbnNsYXRvcixcbiAgICBKdXB5dGVyRnJvbnRFbmQuSVBhdGhzXG4gIF0sXG4gIG9wdGlvbmFsOiBbSVJvdXRlcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZmJmOiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHJlc29sdmVyOiBJV2luZG93UmVzb2x2ZXIsXG4gICAgc3RhdGU6IElTdGF0ZURCLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHBhdGhzOiBKdXB5dGVyRnJvbnRFbmQuSVBhdGhzLFxuICAgIHJvdXRlcjogSVJvdXRlciB8IG51bGxcbiAgKTogdm9pZCA9PiB7XG4gICAgLy8gVGhlIHdvcmtzcGFjZSBmYWN0b3J5IGNyZWF0ZXMgZHVtbXkgd2lkZ2V0cyB0byBsb2FkIGEgbmV3IHdvcmtzcGFjZS5cbiAgICBjb25zdCBmYWN0b3J5ID0gbmV3IFByaXZhdGUuV29ya3NwYWNlRmFjdG9yeSh7XG4gICAgICB3b3Jrc3BhY2VzOiBhcHAuc2VydmljZU1hbmFnZXIud29ya3NwYWNlcyxcbiAgICAgIHJvdXRlcixcbiAgICAgIHN0YXRlLFxuICAgICAgdHJhbnNsYXRvcixcbiAgICAgIHBhdGhzXG4gICAgfSk7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIGFwcC5kb2NSZWdpc3RyeS5hZGRGaWxlVHlwZSh7XG4gICAgICBuYW1lOiBXT1JLU1BBQ0VfTkFNRSxcbiAgICAgIGNvbnRlbnRUeXBlOiAnZmlsZScsXG4gICAgICBmaWxlRm9ybWF0OiAndGV4dCcsXG4gICAgICBkaXNwbGF5TmFtZTogdHJhbnMuX18oJ0p1cHl0ZXJMYWIgd29ya3NwYWNlIEZpbGUnKSxcbiAgICAgIGV4dGVuc2lvbnM6IFtXT1JLU1BBQ0VfRVhUXSxcbiAgICAgIG1pbWVUeXBlczogWyd0ZXh0L2pzb24nXSxcbiAgICAgIGljb25DbGFzczogSUNPTl9OQU1FXG4gICAgfSk7XG4gICAgYXBwLmRvY1JlZ2lzdHJ5LmFkZFdpZGdldEZhY3RvcnkoZmFjdG9yeSk7XG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zYXZlV29ya3NwYWNlQXMsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnU2F2ZSBDdXJyZW50IFdvcmtzcGFjZSBBc+KApicpLFxuICAgICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgICBjb25zdCBkYXRhID0gYXBwLnNlcnZpY2VNYW5hZ2VyLndvcmtzcGFjZXMuZmV0Y2gocmVzb2x2ZXIubmFtZSk7XG4gICAgICAgIGF3YWl0IFByaXZhdGUuc2F2ZUFzKFxuICAgICAgICAgIGZiZi5kZWZhdWx0QnJvd3NlcixcbiAgICAgICAgICBhcHAuc2VydmljZU1hbmFnZXIuY29udGVudHMsXG4gICAgICAgICAgZGF0YSxcbiAgICAgICAgICBzdGF0ZSxcbiAgICAgICAgICB0cmFuc2xhdG9yXG4gICAgICAgICk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNhdmVXb3Jrc3BhY2UsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnU2F2ZSBDdXJyZW50IFdvcmtzcGFjZScpLFxuICAgICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgICBjb25zdCB7IGNvbnRlbnRzIH0gPSBhcHAuc2VydmljZU1hbmFnZXI7XG4gICAgICAgIGNvbnN0IGRhdGEgPSBhcHAuc2VydmljZU1hbmFnZXIud29ya3NwYWNlcy5mZXRjaChyZXNvbHZlci5uYW1lKTtcbiAgICAgICAgY29uc3QgbGFzdFNhdmUgPSAoYXdhaXQgc3RhdGUuZmV0Y2goTEFTVF9TQVZFX0lEKSkgYXMgc3RyaW5nO1xuICAgICAgICBpZiAobGFzdFNhdmUgPT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgIGF3YWl0IFByaXZhdGUuc2F2ZUFzKFxuICAgICAgICAgICAgZmJmLmRlZmF1bHRCcm93c2VyLFxuICAgICAgICAgICAgY29udGVudHMsXG4gICAgICAgICAgICBkYXRhLFxuICAgICAgICAgICAgc3RhdGUsXG4gICAgICAgICAgICB0cmFuc2xhdG9yXG4gICAgICAgICAgKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBhd2FpdCBQcml2YXRlLnNhdmUobGFzdFNhdmUsIGNvbnRlbnRzLCBkYXRhLCBzdGF0ZSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcbiAgfVxufTtcblxubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogU2F2ZSB3b3Jrc3BhY2UgdG8gYSB1c2VyIHByb3ZpZGVkIGxvY2F0aW9uXG4gICAqL1xuICBleHBvcnQgYXN5bmMgZnVuY3Rpb24gc2F2ZShcbiAgICB1c2VyUGF0aDogc3RyaW5nLFxuICAgIGNvbnRlbnRzOiBDb250ZW50c01hbmFnZXIsXG4gICAgZGF0YTogUHJvbWlzZTxXb3Jrc3BhY2UuSVdvcmtzcGFjZT4sXG4gICAgc3RhdGU6IElTdGF0ZURCXG4gICk6IFByb21pc2U8dm9pZD4ge1xuICAgIGxldCBuYW1lID0gdXNlclBhdGguc3BsaXQoJy8nKS5wb3AoKTtcblxuICAgIC8vIEFkZCBleHRlbnNpb24gaWYgbm90IHByb3ZpZGVkIG9yIHJlbW92ZSBleHRlbnNpb24gZnJvbSBuYW1lIGlmIGl0IHdhcy5cbiAgICBpZiAobmFtZSAhPT0gdW5kZWZpbmVkICYmIG5hbWUuaW5jbHVkZXMoJy4nKSkge1xuICAgICAgbmFtZSA9IG5hbWUuc3BsaXQoJy4nKVswXTtcbiAgICB9IGVsc2Uge1xuICAgICAgdXNlclBhdGggPSB1c2VyUGF0aCArIFdPUktTUEFDRV9FWFQ7XG4gICAgfVxuXG4gICAgLy8gU2F2ZSBsYXN0IHNhdmUgbG9jYXRpb24sIGZvciBzYXZlIGJ1dHRvbiB0byB3b3JrXG4gICAgYXdhaXQgc3RhdGUuc2F2ZShMQVNUX1NBVkVfSUQsIHVzZXJQYXRoKTtcblxuICAgIGNvbnN0IHJlc29sdmVkRGF0YSA9IGF3YWl0IGRhdGE7XG4gICAgcmVzb2x2ZWREYXRhLm1ldGFkYXRhLmlkID0gYCR7bmFtZX1gO1xuICAgIGF3YWl0IGNvbnRlbnRzLnNhdmUodXNlclBhdGgsIHtcbiAgICAgIHR5cGU6ICdmaWxlJyxcbiAgICAgIGZvcm1hdDogJ3RleHQnLFxuICAgICAgY29udGVudDogSlNPTi5zdHJpbmdpZnkocmVzb2x2ZWREYXRhKVxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEFzayB1c2VyIGZvciBsb2NhdGlvbiwgYW5kIHNhdmUgd29ya3NwYWNlLlxuICAgKiBEZWZhdWx0IGxvY2F0aW9uIGlzIHRoZSBjdXJyZW50IGRpcmVjdG9yeSBpbiB0aGUgZmlsZSBicm93c2VyXG4gICAqL1xuICBleHBvcnQgYXN5bmMgZnVuY3Rpb24gc2F2ZUFzKFxuICAgIGJyb3dzZXI6IEZpbGVCcm93c2VyLFxuICAgIGNvbnRlbnRzOiBDb250ZW50c01hbmFnZXIsXG4gICAgZGF0YTogUHJvbWlzZTxXb3Jrc3BhY2UuSVdvcmtzcGFjZT4sXG4gICAgc3RhdGU6IElTdGF0ZURCLFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApOiBQcm9taXNlPHZvaWQ+IHtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCBsYXN0U2F2ZSA9IGF3YWl0IHN0YXRlLmZldGNoKExBU1RfU0FWRV9JRCk7XG5cbiAgICBsZXQgZGVmYXVsdE5hbWU7XG4gICAgaWYgKGxhc3RTYXZlID09PSB1bmRlZmluZWQpIHtcbiAgICAgIGRlZmF1bHROYW1lID0gJ25ldy13b3Jrc3BhY2UnO1xuICAgIH0gZWxzZSB7XG4gICAgICBkZWZhdWx0TmFtZSA9IChsYXN0U2F2ZSBhcyBzdHJpbmcpLnNwbGl0KCcvJykucG9wKCk/LnNwbGl0KCcuJylbMF07XG4gICAgfVxuXG4gICAgY29uc3QgZGVmYXVsdFBhdGggPSBicm93c2VyLm1vZGVsLnBhdGggKyAnLycgKyBkZWZhdWx0TmFtZSArIFdPUktTUEFDRV9FWFQ7XG4gICAgY29uc3QgdXNlclBhdGggPSBhd2FpdCBnZXRTYXZlUGF0aChkZWZhdWx0UGF0aCwgdHJhbnNsYXRvcik7XG5cbiAgICBpZiAodXNlclBhdGgpIHtcbiAgICAgIGF3YWl0IHNhdmUodXNlclBhdGgsIGNvbnRlbnRzLCBkYXRhLCBzdGF0ZSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFRoaXMgd2lkZ2V0IGZhY3RvcnkgaXMgdXNlZCB0byBoYW5kbGUgZG91YmxlIGNsaWNrIG9uIHdvcmtzcGFjZVxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIFdvcmtzcGFjZUZhY3RvcnkgZXh0ZW5kcyBBQkNXaWRnZXRGYWN0b3J5PElEb2N1bWVudFdpZGdldD4ge1xuICAgIC8qKlxuICAgICAqIENvbnN0cnVjdCBhIHdpZGdldCBmYWN0b3J5IHRoYXQgdXBsb2FkcyBhIHdvcmtzcGFjZSBhbmQgbmF2aWdhdGVzIHRvIGl0LlxuICAgICAqXG4gICAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgaW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBhIGBXb3Jrc3BhY2VGYWN0b3J5YC5cbiAgICAgKi9cbiAgICBjb25zdHJ1Y3RvcihvcHRpb25zOiBXb3Jrc3BhY2VGYWN0b3J5LklPcHRpb25zKSB7XG4gICAgICBjb25zdCB0cmFucyA9IChvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3IpLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICAgIHN1cGVyKHtcbiAgICAgICAgbmFtZTogdHJhbnMuX18oJ1dvcmtzcGFjZSBsb2FkZXInKSxcbiAgICAgICAgZmlsZVR5cGVzOiBbV09SS1NQQUNFX05BTUVdLFxuICAgICAgICBkZWZhdWx0Rm9yOiBbV09SS1NQQUNFX05BTUVdLFxuICAgICAgICByZWFkT25seTogdHJ1ZVxuICAgICAgfSk7XG4gICAgICB0aGlzLl9hcHBsaWNhdGlvbiA9IG9wdGlvbnMucGF0aHMudXJscy5hcHA7XG4gICAgICB0aGlzLl9yb3V0ZXIgPSBvcHRpb25zLnJvdXRlcjtcbiAgICAgIHRoaXMuX3N0YXRlID0gb3B0aW9ucy5zdGF0ZTtcbiAgICAgIHRoaXMuX3dvcmtzcGFjZXMgPSBvcHRpb25zLndvcmtzcGFjZXM7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogTG9hZHMgdGhlIHdvcmtzcGFjZSBpbnRvIGxvYWQsIGFuZCBqdW1wIHRvIGl0XG4gICAgICogQHBhcmFtIGNvbnRleHQgVGhpcyBpcyB1c2VkIHF1ZXJpZWQgdG8gcXVlcnkgdGhlIHdvcmtzcGFjZSBjb250ZW50XG4gICAgICovXG4gICAgcHJvdGVjdGVkIGNyZWF0ZU5ld1dpZGdldChcbiAgICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dFxuICAgICk6IElEb2N1bWVudFdpZGdldCB7XG4gICAgICAvLyBTYXZlIGEgZmlsZSdzIGNvbnRlbnRzIGFzIGEgd29ya3NwYWNlIGFuZCBuYXZpZ2F0ZSB0byB0aGF0IHdvcmtzcGFjZS5cbiAgICAgIHZvaWQgY29udGV4dC5yZWFkeS50aGVuKGFzeW5jICgpID0+IHtcbiAgICAgICAgY29uc3QgZmlsZSA9IGNvbnRleHQubW9kZWw7XG4gICAgICAgIGNvbnN0IHdvcmtzcGFjZSA9IChmaWxlLnRvSlNPTigpIGFzIHVua25vd24pIGFzIFdvcmtzcGFjZS5JV29ya3NwYWNlO1xuICAgICAgICBjb25zdCBwYXRoID0gY29udGV4dC5wYXRoO1xuICAgICAgICBjb25zdCBpZCA9IHdvcmtzcGFjZS5tZXRhZGF0YS5pZDtcblxuICAgICAgICAvLyBTYXZlIHRoZSBmaWxlIGNvbnRlbnRzIGFzIGEgd29ya3NwYWNlLlxuICAgICAgICBhd2FpdCB0aGlzLl93b3Jrc3BhY2VzLnNhdmUoaWQsIHdvcmtzcGFjZSk7XG5cbiAgICAgICAgLy8gU2F2ZSBsYXN0IHNhdmUgbG9jYXRpb24gZm9yIHRoZSBzYXZlIGNvbW1hbmQuXG4gICAgICAgIGF3YWl0IHRoaXMuX3N0YXRlLnNhdmUoTEFTVF9TQVZFX0lELCBwYXRoKTtcblxuICAgICAgICAvLyBOYXZpZ2F0ZSB0byBuZXcgd29ya3NwYWNlLlxuICAgICAgICBjb25zdCB1cmwgPSBVUkxFeHQuam9pbih0aGlzLl9hcHBsaWNhdGlvbiwgJ3dvcmtzcGFjZXMnLCBpZCk7XG4gICAgICAgIGlmICh0aGlzLl9yb3V0ZXIpIHtcbiAgICAgICAgICB0aGlzLl9yb3V0ZXIubmF2aWdhdGUodXJsLCB7IGhhcmQ6IHRydWUgfSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgZG9jdW1lbnQubG9jYXRpb24uaHJlZiA9IHVybDtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgICByZXR1cm4gZHVtbXlXaWRnZXQoY29udGV4dCk7XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfYXBwbGljYXRpb246IHN0cmluZztcbiAgICBwcml2YXRlIF9yb3V0ZXI6IElSb3V0ZXIgfCBudWxsO1xuICAgIHByaXZhdGUgX3N0YXRlOiBJU3RhdGVEQjtcbiAgICBwcml2YXRlIF93b3Jrc3BhY2VzOiBXb3Jrc3BhY2VNYW5hZ2VyO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgbmFtZXNwYWNlIGZvciBgV29ya3NwYWNlRmFjdG9yeWBcbiAgICovXG4gIGV4cG9ydCBuYW1lc3BhY2UgV29ya3NwYWNlRmFjdG9yeSB7XG4gICAgLyoqXG4gICAgICogSW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBhIGBXb3Jrc3BhY2VGYWN0b3J5YFxuICAgICAqL1xuICAgIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgICAgcGF0aHM6IEp1cHl0ZXJGcm9udEVuZC5JUGF0aHM7XG4gICAgICByb3V0ZXI6IElSb3V0ZXIgfCBudWxsO1xuICAgICAgc3RhdGU6IElTdGF0ZURCO1xuICAgICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gICAgICB3b3Jrc3BhY2VzOiBXb3Jrc3BhY2VNYW5hZ2VyO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm5zIGEgZHVtbXkgd2lkZ2V0IHdpdGggZGlzcG9zZWQgY29udGVudCB0aGF0IGRvZXNuJ3QgcmVuZGVyIGluIHRoZSBVSS5cbiAgICpcbiAgICogQHBhcmFtIGNvbnRleHQgLSBUaGUgZmlsZSBjb250ZXh0LlxuICAgKi9cbiAgZnVuY3Rpb24gZHVtbXlXaWRnZXQoY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0KTogSURvY3VtZW50V2lkZ2V0IHtcbiAgICBjb25zdCB3aWRnZXQgPSBuZXcgRG9jdW1lbnRXaWRnZXQoeyBjb250ZW50OiBuZXcgV2lkZ2V0KCksIGNvbnRleHQgfSk7XG4gICAgd2lkZ2V0LmNvbnRlbnQuZGlzcG9zZSgpO1xuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cblxuICAvKipcbiAgICogQXNrIHVzZXIgZm9yIGEgcGF0aCB0byBzYXZlIHRvLlxuICAgKiBAcGFyYW0gZGVmYXVsdFBhdGggUGF0aCBhbHJlYWR5IHByZXNlbnQgd2hlbiB0aGUgZGlhbG9nIGlzIHNob3duXG4gICAqL1xuICBhc3luYyBmdW5jdGlvbiBnZXRTYXZlUGF0aChcbiAgICBkZWZhdWx0UGF0aDogc3RyaW5nLFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApOiBQcm9taXNlPHN0cmluZyB8IG51bGw+IHtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHNhdmVCdG4gPSBEaWFsb2cub2tCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ1NhdmUnKSB9KTtcbiAgICBjb25zdCByZXN1bHQgPSBhd2FpdCBzaG93RGlhbG9nKHtcbiAgICAgIHRpdGxlOiB0cmFucy5fXygnU2F2ZSBDdXJyZW50IFdvcmtzcGFjZSBBc+KApicpLFxuICAgICAgYm9keTogbmV3IFNhdmVXaWRnZXQoZGVmYXVsdFBhdGgpLFxuICAgICAgYnV0dG9uczogW0RpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0NhbmNlbCcpIH0pLCBzYXZlQnRuXVxuICAgIH0pO1xuICAgIGlmIChyZXN1bHQuYnV0dG9uLmxhYmVsID09PSB0cmFucy5fXygnU2F2ZScpKSB7XG4gICAgICByZXR1cm4gcmVzdWx0LnZhbHVlO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQSB3aWRnZXQgdGhhdCBnZXRzIGEgZmlsZSBwYXRoIGZyb20gYSB1c2VyLlxuICAgKi9cbiAgY2xhc3MgU2F2ZVdpZGdldCBleHRlbmRzIFdpZGdldCB7XG4gICAgLyoqXG4gICAgICogR2V0cyBhIG1vZGFsIG5vZGUgZm9yIGdldHRpbmcgc2F2ZSBsb2NhdGlvbi4gV2lsbCBoYXZlIGEgZGVmYXVsdCB0byB0aGUgY3VycmVudCBvcGVuZWQgZGlyZWN0b3J5XG4gICAgICogQHBhcmFtIHBhdGggRGVmYXVsdCBsb2NhdGlvblxuICAgICAqL1xuICAgIGNvbnN0cnVjdG9yKHBhdGg6IHN0cmluZykge1xuICAgICAgc3VwZXIoeyBub2RlOiBjcmVhdGVTYXZlTm9kZShwYXRoKSB9KTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXRzIHRoZSBzYXZlIHBhdGggZW50ZXJlZCBieSB0aGUgdXNlclxuICAgICAqL1xuICAgIGdldFZhbHVlKCk6IHN0cmluZyB7XG4gICAgICByZXR1cm4gKHRoaXMubm9kZSBhcyBIVE1MSW5wdXRFbGVtZW50KS52YWx1ZTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIHRoZSBub2RlIGZvciBhIHNhdmUgd2lkZ2V0LlxuICAgKi9cbiAgZnVuY3Rpb24gY3JlYXRlU2F2ZU5vZGUocGF0aDogc3RyaW5nKTogSFRNTEVsZW1lbnQge1xuICAgIGNvbnN0IGlucHV0ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaW5wdXQnKTtcbiAgICBpbnB1dC52YWx1ZSA9IHBhdGg7XG4gICAgcmV0dXJuIGlucHV0O1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9