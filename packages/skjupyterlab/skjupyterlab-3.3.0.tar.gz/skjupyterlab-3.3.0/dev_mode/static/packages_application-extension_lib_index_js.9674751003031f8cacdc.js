(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_application-extension_lib_index_js"],{

/***/ "../packages/application-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/application-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DEFAULT_CONTEXT_ITEM_RANK": () => (/* binding */ DEFAULT_CONTEXT_ITEM_RANK),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/property-inspector */ "webpack/sharing/consume/default/@jupyterlab/property-inspector/@jupyterlab/property-inspector");
/* harmony import */ var _jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_12__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module application-extension
 */













/**
 * Default context menu item rank
 */
const DEFAULT_CONTEXT_ITEM_RANK = 100;
/**
 * The command IDs used by the application plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.activateNextTab = 'application:activate-next-tab';
    CommandIDs.activatePreviousTab = 'application:activate-previous-tab';
    CommandIDs.activateNextTabBar = 'application:activate-next-tab-bar';
    CommandIDs.activatePreviousTabBar = 'application:activate-previous-tab-bar';
    CommandIDs.close = 'application:close';
    CommandIDs.closeOtherTabs = 'application:close-other-tabs';
    CommandIDs.closeRightTabs = 'application:close-right-tabs';
    CommandIDs.closeAll = 'application:close-all';
    CommandIDs.setMode = 'application:set-mode';
    CommandIDs.toggleMode = 'application:toggle-mode';
    CommandIDs.toggleLeftArea = 'application:toggle-left-area';
    CommandIDs.toggleRightArea = 'application:toggle-right-area';
    CommandIDs.togglePresentationMode = 'application:toggle-presentation-mode';
    CommandIDs.tree = 'router:tree';
    CommandIDs.switchSidebar = 'sidebar:switch';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin to register the commands for the main application.
 */
const mainCommands = {
    id: '@jupyterlab/application-extension:commands',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, labShell, palette) => {
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Main Area');
        // Add Command to override the JLab context menu.
        commands.addCommand(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEndContextMenu.contextMenu, {
            label: trans.__('Shift+Right Click for Browser Menu'),
            isEnabled: () => false,
            execute: () => void 0
        });
        // Returns the widget associated with the most recent contextmenu event.
        const contextMenuWidget = () => {
            const test = (node) => !!node.dataset.id;
            const node = app.contextMenuHitTest(test);
            if (!node) {
                // Fall back to active widget if path cannot be obtained from event.
                return shell.currentWidget;
            }
            const matches = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.toArray)(shell.widgets('main')).filter(widget => widget.id === node.dataset.id);
            if (matches.length < 1) {
                return shell.currentWidget;
            }
            return matches[0];
        };
        // Closes an array of widgets.
        const closeWidgets = (widgets) => {
            widgets.forEach(widget => widget.close());
        };
        // Find the tab area for a widget within a specific dock area.
        const findTab = (area, widget) => {
            switch (area.type) {
                case 'split-area': {
                    const iterator = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.iter)(area.children);
                    let tab = null;
                    let value;
                    do {
                        value = iterator.next();
                        if (value) {
                            tab = findTab(value, widget);
                        }
                    } while (!tab && value);
                    return tab;
                }
                case 'tab-area': {
                    const { id } = widget;
                    return area.widgets.some(widget => widget.id === id) ? area : null;
                }
                default:
                    return null;
            }
        };
        // Find the tab area for a widget within the main dock area.
        const tabAreaFor = (widget) => {
            var _a;
            const layout = labShell === null || labShell === void 0 ? void 0 : labShell.saveLayout();
            const mainArea = layout === null || layout === void 0 ? void 0 : layout.mainArea;
            if (!mainArea || _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('mode') !== 'multiple-document') {
                return null;
            }
            const area = (_a = mainArea.dock) === null || _a === void 0 ? void 0 : _a.main;
            if (!area) {
                return null;
            }
            return findTab(area, widget);
        };
        // Returns an array of all widgets to the right of a widget in a tab area.
        const widgetsRightOf = (widget) => {
            const { id } = widget;
            const tabArea = tabAreaFor(widget);
            const widgets = tabArea ? tabArea.widgets || [] : [];
            const index = widgets.findIndex(widget => widget.id === id);
            if (index < 0) {
                return [];
            }
            return widgets.slice(index + 1);
        };
        commands.addCommand(CommandIDs.close, {
            label: () => trans.__('Close Tab'),
            isEnabled: () => {
                const widget = contextMenuWidget();
                return !!widget && widget.title.closable;
            },
            execute: () => {
                const widget = contextMenuWidget();
                if (widget) {
                    widget.close();
                }
            }
        });
        commands.addCommand(CommandIDs.closeOtherTabs, {
            label: () => trans.__('Close All Other Tabs'),
            isEnabled: () => {
                // Ensure there are at least two widgets.
                const iterator = shell.widgets('main');
                return !!iterator.next() && !!iterator.next();
            },
            execute: () => {
                const widget = contextMenuWidget();
                if (!widget) {
                    return;
                }
                const { id } = widget;
                const otherWidgets = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.toArray)(shell.widgets('main')).filter(widget => widget.id !== id);
                closeWidgets(otherWidgets);
            }
        });
        commands.addCommand(CommandIDs.closeRightTabs, {
            label: () => trans.__('Close Tabs to Right'),
            isEnabled: () => !!contextMenuWidget() &&
                widgetsRightOf(contextMenuWidget()).length > 0,
            execute: () => {
                const widget = contextMenuWidget();
                if (!widget) {
                    return;
                }
                closeWidgets(widgetsRightOf(widget));
            }
        });
        if (labShell) {
            commands.addCommand(CommandIDs.activateNextTab, {
                label: trans.__('Activate Next Tab'),
                execute: () => {
                    labShell.activateNextTab();
                }
            });
            commands.addCommand(CommandIDs.activatePreviousTab, {
                label: trans.__('Activate Previous Tab'),
                execute: () => {
                    labShell.activatePreviousTab();
                }
            });
            commands.addCommand(CommandIDs.activateNextTabBar, {
                label: trans.__('Activate Next Tab Bar'),
                execute: () => {
                    labShell.activateNextTabBar();
                }
            });
            commands.addCommand(CommandIDs.activatePreviousTabBar, {
                label: trans.__('Activate Previous Tab Bar'),
                execute: () => {
                    labShell.activatePreviousTabBar();
                }
            });
            commands.addCommand(CommandIDs.closeAll, {
                label: trans.__('Close All Tabs'),
                execute: () => {
                    labShell.closeAll();
                }
            });
            commands.addCommand(CommandIDs.toggleLeftArea, {
                label: () => trans.__('Show Left Sidebar'),
                execute: () => {
                    if (labShell.leftCollapsed) {
                        labShell.expandLeft();
                    }
                    else {
                        labShell.collapseLeft();
                        if (labShell.currentWidget) {
                            labShell.activateById(labShell.currentWidget.id);
                        }
                    }
                },
                isToggled: () => !labShell.leftCollapsed,
                isVisible: () => !labShell.isEmpty('left')
            });
            commands.addCommand(CommandIDs.toggleRightArea, {
                label: () => trans.__('Show Right Sidebar'),
                execute: () => {
                    if (labShell.rightCollapsed) {
                        labShell.expandRight();
                    }
                    else {
                        labShell.collapseRight();
                        if (labShell.currentWidget) {
                            labShell.activateById(labShell.currentWidget.id);
                        }
                    }
                },
                isToggled: () => !labShell.rightCollapsed,
                isVisible: () => !labShell.isEmpty('right')
            });
            commands.addCommand(CommandIDs.togglePresentationMode, {
                label: () => trans.__('Presentation Mode'),
                execute: () => {
                    labShell.presentationMode = !labShell.presentationMode;
                },
                isToggled: () => labShell.presentationMode,
                isVisible: () => true
            });
            commands.addCommand(CommandIDs.setMode, {
                isVisible: args => {
                    const mode = args['mode'];
                    return mode === 'single-document' || mode === 'multiple-document';
                },
                execute: args => {
                    const mode = args['mode'];
                    if (mode === 'single-document' || mode === 'multiple-document') {
                        labShell.mode = mode;
                        return;
                    }
                    throw new Error(`Unsupported application shell mode: ${mode}`);
                }
            });
            commands.addCommand(CommandIDs.toggleMode, {
                label: trans.__('Simple Interface'),
                isToggled: () => labShell.mode === 'single-document',
                execute: () => {
                    const args = labShell.mode === 'multiple-document'
                        ? { mode: 'single-document' }
                        : { mode: 'multiple-document' };
                    return commands.execute(CommandIDs.setMode, args);
                }
            });
        }
        if (palette) {
            [
                CommandIDs.activateNextTab,
                CommandIDs.activatePreviousTab,
                CommandIDs.activateNextTabBar,
                CommandIDs.activatePreviousTabBar,
                CommandIDs.close,
                CommandIDs.closeAll,
                CommandIDs.closeOtherTabs,
                CommandIDs.closeRightTabs,
                CommandIDs.toggleLeftArea,
                CommandIDs.toggleRightArea,
                CommandIDs.togglePresentationMode,
                CommandIDs.toggleMode
            ].forEach(command => palette.addItem({ command, category }));
        }
    }
};
/**
 * The main extension.
 */
const main = {
    id: '@jupyterlab/application-extension:main',
    requires: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IWindowResolver,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.ITreeResolver
    ],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IConnectionLost],
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ITreePathUpdater,
    activate: (app, router, resolver, translator, treeResolver, connectionLost) => {
        const trans = translator.load('jupyterlab');
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${main.id} must be activated in JupyterLab.`);
        }
        // These two internal state variables are used to manage the two source
        // of the tree part of the URL being updated: 1) path of the active document,
        // 2) path of the default browser if the active main area widget isn't a document.
        let _docTreePath = '';
        let _defaultBrowserTreePath = '';
        function updateTreePath(treePath) {
            // Wait for tree resolver to finish before updating the path because it use the PageConfig['treePath']
            void treeResolver.paths.then(() => {
                _defaultBrowserTreePath = treePath;
                if (!_docTreePath) {
                    const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getUrl({ treePath });
                    const path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.parse(url).pathname;
                    router.navigate(path, { skipRouting: true });
                    // Persist the new tree path to PageConfig as it is used elsewhere at runtime.
                    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.setOption('treePath', treePath);
                }
            });
        }
        // Requiring the window resolver guarantees that the application extension
        // only loads if there is a viable window name. Otherwise, the application
        // will short-circuit and ask the user to navigate away.
        const workspace = resolver.name;
        console.debug(`Starting application in workspace: "${workspace}"`);
        // If there were errors registering plugins, tell the user.
        if (app.registerPluginErrors.length !== 0) {
            const body = (react__WEBPACK_IMPORTED_MODULE_12__.createElement("pre", null, app.registerPluginErrors.map(e => e.message).join('\n')));
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Error Registering Plugins'), {
                message: body
            });
        }
        // If the application shell layout is modified,
        // trigger a refresh of the commands.
        app.shell.layoutModified.connect(() => {
            app.commands.notifyCommandChanged();
        });
        // Watch the mode and update the page URL to /lab or /doc to reflect the
        // change.
        app.shell.modeChanged.connect((_, args) => {
            const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getUrl({ mode: args });
            const path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.parse(url).pathname;
            router.navigate(path, { skipRouting: true });
            // Persist this mode change to PageConfig as it is used elsewhere at runtime.
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.setOption('mode', args);
        });
        // Wait for tree resolver to finish before updating the path because it use the PageConfig['treePath']
        void treeResolver.paths.then(() => {
            // Watch the path of the current widget in the main area and update the page
            // URL to reflect the change.
            app.shell.currentPathChanged.connect((_, args) => {
                const maybeTreePath = args.newValue;
                const treePath = maybeTreePath || _defaultBrowserTreePath;
                const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getUrl({ treePath: treePath });
                const path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.parse(url).pathname;
                router.navigate(path, { skipRouting: true });
                // Persist the new tree path to PageConfig as it is used elsewhere at runtime.
                _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.setOption('treePath', treePath);
                _docTreePath = maybeTreePath;
            });
        });
        // If the connection to the server is lost, handle it with the
        // connection lost handler.
        connectionLost = connectionLost || _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ConnectionLost;
        app.serviceManager.connectionFailure.connect((manager, error) => connectionLost(manager, error, translator));
        const builder = app.serviceManager.builder;
        const build = () => {
            return builder
                .build()
                .then(() => {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Build Complete'),
                    body: (react__WEBPACK_IMPORTED_MODULE_12__.createElement("div", null,
                        trans.__('Build successfully completed, reload page?'),
                        react__WEBPACK_IMPORTED_MODULE_12__.createElement("br", null),
                        trans.__('You will lose any unsaved changes.'))),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({
                            label: trans.__('Reload Without Saving'),
                            actions: ['reload']
                        }),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Save and Reload') })
                    ],
                    hasClose: true
                });
            })
                .then(({ button: { accept, actions } }) => {
                if (accept) {
                    void app.commands
                        .execute('docmanager:save')
                        .then(() => {
                        router.reload();
                    })
                        .catch(err => {
                        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Save Failed'), {
                            message: react__WEBPACK_IMPORTED_MODULE_12__.createElement("pre", null, err.message)
                        });
                    });
                }
                else if (actions.includes('reload')) {
                    router.reload();
                }
            })
                .catch(err => {
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Build Failed'), {
                    message: react__WEBPACK_IMPORTED_MODULE_12__.createElement("pre", null, err.message)
                });
            });
        };
        if (builder.isAvailable && builder.shouldCheck) {
            void builder.getStatus().then(response => {
                if (response.status === 'building') {
                    return build();
                }
                if (response.status !== 'needed') {
                    return;
                }
                const body = (react__WEBPACK_IMPORTED_MODULE_12__.createElement("div", null,
                    trans.__('JupyterLab build is suggested:'),
                    react__WEBPACK_IMPORTED_MODULE_12__.createElement("br", null),
                    react__WEBPACK_IMPORTED_MODULE_12__.createElement("pre", null, response.message)));
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Build Recommended'),
                    body,
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Build') })
                    ]
                }).then(result => (result.button.accept ? build() : undefined));
            });
        }
        return updateTreePath;
    },
    autoStart: true
};
/**
 * Plugin to build the context menu from the settings.
 */
const contextMenuPlugin = {
    id: '@jupyterlab/application-extension:context-menu',
    autoStart: true,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    activate: (app, settingRegistry, translator) => {
        const trans = translator.load('jupyterlab');
        function createMenu(options) {
            const menu = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.RankedMenu(Object.assign(Object.assign({}, options), { commands: app.commands }));
            if (options.label) {
                menu.title.label = trans.__(options.label);
            }
            return menu;
        }
        // Load the context menu lately so plugins are loaded.
        app.started
            .then(() => {
            return Private.loadSettingsContextMenu(app.contextMenu, settingRegistry, createMenu, translator);
        })
            .catch(reason => {
            console.error('Failed to load context menu items from settings registry.', reason);
        });
    }
};
/**
 * Check if the application is dirty before closing the browser tab.
 */
const dirty = {
    id: '@jupyterlab/application-extension:dirty',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    activate: (app, translator) => {
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${dirty.id} must be activated in JupyterLab.`);
        }
        const trans = translator.load('jupyterlab');
        const message = trans.__('Are you sure you want to exit JupyterLab?\n\nAny unsaved changes will be lost.');
        // The spec for the `beforeunload` event is implemented differently by
        // the different browser vendors. Consequently, the `event.returnValue`
        // attribute needs to set in addition to a return value being returned.
        // For more information, see:
        // https://developer.mozilla.org/en/docs/Web/Events/beforeunload
        window.addEventListener('beforeunload', event => {
            if (app.status.isDirty) {
                return (event.returnValue = message);
            }
        });
    }
};
/**
 * The default layout restorer provider.
 */
const layout = {
    id: '@jupyterlab/application-extension:layout',
    requires: [_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__.IStateDB, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    activate: (app, state, labShell, settingRegistry, translator) => {
        const first = app.started;
        const registry = app.commands;
        const restorer = new _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.LayoutRestorer({ connector: state, first, registry });
        void restorer.fetch().then(saved => {
            labShell.restoreLayout(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('mode'), saved);
            labShell.layoutModified.connect(() => {
                void restorer.save(labShell.saveLayout());
            });
            Private.activateSidebarSwitcher(app, labShell, settingRegistry, translator, saved);
        });
        return restorer;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer
};
/**
 * The default URL router provider.
 */
const router = {
    id: '@jupyterlab/application-extension:router',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths],
    activate: (app, paths) => {
        const { commands } = app;
        const base = paths.urls.base;
        const router = new _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.Router({ base, commands });
        void app.started.then(() => {
            // Route the very first request on load.
            void router.route();
            // Route all pop state events.
            window.addEventListener('popstate', () => {
                void router.route();
            });
        });
        return router;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter
};
/**
 * The default tree route resolver plugin.
 */
const tree = {
    id: '@jupyterlab/application-extension:tree-resolver',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter],
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.ITreeResolver,
    activate: (app, router) => {
        const { commands } = app;
        const set = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_10__.DisposableSet();
        const delegate = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.PromiseDelegate();
        const treePattern = new RegExp('/(lab|doc)(/workspaces/[a-zA-Z0-9-_]+)?(/tree/.*)?');
        set.add(commands.addCommand(CommandIDs.tree, {
            execute: async (args) => {
                var _a;
                if (set.isDisposed) {
                    return;
                }
                const query = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.queryStringToObject((_a = args.search) !== null && _a !== void 0 ? _a : '');
                const browser = query['file-browser-path'] || '';
                // Remove the file browser path from the query string.
                delete query['file-browser-path'];
                // Clean up artifacts immediately upon routing.
                set.dispose();
                delegate.resolve({ browser, file: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('treePath') });
            }
        }));
        set.add(router.register({ command: CommandIDs.tree, pattern: treePattern }));
        // If a route is handled by the router without the tree command being
        // invoked, resolve to `null` and clean up artifacts.
        const listener = () => {
            if (set.isDisposed) {
                return;
            }
            set.dispose();
            delegate.resolve(null);
        };
        router.routed.connect(listener);
        set.add(new _lumino_disposable__WEBPACK_IMPORTED_MODULE_10__.DisposableDelegate(() => {
            router.routed.disconnect(listener);
        }));
        return { paths: delegate.promise };
    }
};
/**
 * The default URL not found extension.
 */
const notfound = {
    id: '@jupyterlab/application-extension:notfound',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    activate: (_, paths, router, translator) => {
        const trans = translator.load('jupyterlab');
        const bad = paths.urls.notFound;
        if (!bad) {
            return;
        }
        const base = router.base;
        const message = trans.__('The path: %1 was not found. JupyterLab redirected to: %2', bad, base);
        // Change the URL back to the base application URL.
        router.navigate('');
        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Path Not Found'), { message });
    },
    autoStart: true
};
/**
 * Change the favicon changing based on the busy status;
 */
const busy = {
    id: '@jupyterlab/application-extension:faviconbusy',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus],
    activate: async (_, status) => {
        status.busySignal.connect((_, isBusy) => {
            const favicon = document.querySelector(`link[rel="icon"]${isBusy ? '.idle.favicon' : '.busy.favicon'}`);
            if (!favicon) {
                return;
            }
            const newFavicon = document.querySelector(`link${isBusy ? '.busy.favicon' : '.idle.favicon'}`);
            if (!newFavicon) {
                return;
            }
            // If we have the two icons with the special classes, then toggle them.
            if (favicon !== newFavicon) {
                favicon.rel = '';
                newFavicon.rel = 'icon';
                // Firefox doesn't seem to recognize just changing rel, so we also
                // reinsert the link into the DOM.
                newFavicon.parentNode.replaceChild(newFavicon, newFavicon);
            }
        });
    },
    autoStart: true
};
/**
 * The default JupyterLab application shell.
 */
const shell = {
    id: '@jupyterlab/application-extension:shell',
    activate: (app) => {
        if (!(app.shell instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.LabShell)) {
            throw new Error(`${shell.id} did not find a LabShell instance.`);
        }
        return app.shell;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell
};
/**
 * The default JupyterLab application status provider.
 */
const status = {
    id: '@jupyterlab/application-extension:status',
    activate: (app) => {
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${status.id} must be activated in JupyterLab.`);
        }
        return app.status;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus
};
/**
 * The default JupyterLab application-specific information provider.
 *
 * #### Notes
 * This plugin should only be used by plugins that specifically need to access
 * JupyterLab application information, e.g., listing extensions that have been
 * loaded or deferred within JupyterLab.
 */
const info = {
    id: '@jupyterlab/application-extension:info',
    activate: (app) => {
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${info.id} must be activated in JupyterLab.`);
        }
        return app.info;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab.IInfo
};
/**
 * The default JupyterLab paths dictionary provider.
 */
const paths = {
    id: '@jupyterlab/apputils-extension:paths',
    activate: (app) => {
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${paths.id} must be activated in JupyterLab.`);
        }
        return app.paths;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths
};
/**
 * The default property inspector provider.
 */
const propertyInspector = {
    id: '@jupyterlab/application-extension:property-inspector',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3__.IPropertyInspectorProvider,
    activate: (app, labshell, translator, restorer) => {
        const trans = translator.load('jupyterlab');
        const widget = new _jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3__.SideBarPropertyInspectorProvider(labshell, undefined, translator);
        widget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.buildIcon;
        widget.title.caption = trans.__('Property Inspector');
        widget.id = 'jp-property-inspector';
        labshell.add(widget, 'right', { rank: 100 });
        if (restorer) {
            restorer.add(widget, 'jp-property-inspector');
        }
        return widget;
    }
};
const JupyterLogo = {
    id: '@jupyterlab/application-extension:logo',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, shell) => {
        const logo = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_11__.Widget();
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.jupyterIcon.element({
            container: logo.node,
            elementPosition: 'center',
            margin: '0px',
            height: 'auto',
            width: '120px'
        });
        logo.id = 'jp-MainLogo';
        shell.add(logo, 'top', { rank: 0 });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    contextMenuPlugin,
    dirty,
    main,
    mainCommands,
    layout,
    router,
    tree,
    notfound,
    busy,
    shell,
    status,
    info,
    paths,
    propertyInspector,
    JupyterLogo
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
var Private;
(function (Private) {
    async function displayInformation(trans) {
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Information'),
            body: trans.__('Context menu customization has changed. You will need to reload JupyterLab to see the changes.'),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Reload') })
            ]
        });
        if (result.button.accept) {
            location.reload();
        }
    }
    async function loadSettingsContextMenu(contextMenu, registry, menuFactory, translator) {
        var _a;
        const trans = translator.load('jupyterlab');
        const pluginId = contextMenuPlugin.id;
        let canonical;
        let loaded = {};
        /**
         * Populate the plugin's schema defaults.
         *
         * We keep track of disabled entries in case the plugin is loaded
         * after the menu initialization.
         */
        function populate(schema) {
            var _a, _b;
            loaded = {};
            const pluginDefaults = Object.keys(registry.plugins)
                .map(plugin => {
                var _a, _b;
                const items = (_b = (_a = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.context) !== null && _b !== void 0 ? _b : [];
                loaded[plugin] = items;
                return items;
            })
                .concat([(_b = (_a = schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.context) !== null && _b !== void 0 ? _b : []])
                .reduceRight((acc, val) => _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.reconcileItems(acc, val, true), []);
            // Apply default value as last step to take into account overrides.json
            // The standard default being [] as the plugin must use `jupyter.lab.menus.context`
            // to define their default value.
            schema.properties.contextMenu.default = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.reconcileItems(pluginDefaults, schema.properties.contextMenu.default, true)
                // flatten one level
                .sort((a, b) => { var _a, _b; return ((_a = a.rank) !== null && _a !== void 0 ? _a : Infinity) - ((_b = b.rank) !== null && _b !== void 0 ? _b : Infinity); });
        }
        // Transform the plugin object to return different schema than the default.
        registry.transform(pluginId, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.contextMenu) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    contextMenu: (_d = plugin.data.user.contextMenu) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    contextMenu: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.reconcileItems(defaults, user.contextMenu, false)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                return {
                    data: plugin.data,
                    id: plugin.id,
                    raw: plugin.raw,
                    schema: canonical,
                    version: plugin.version
                };
            }
        });
        // Repopulate the canonical variable after the setting registry has
        // preloaded all initial plugins.
        canonical = null;
        const settings = await registry.load(pluginId);
        const contextItems = (_a = settings.composite.contextMenu) !== null && _a !== void 0 ? _a : [];
        // Create menu item for non-disabled element
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.filterDisabledItems(contextItems).forEach(item => {
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.addContextItem(Object.assign({ 
                // We have to set the default rank because Lumino is sorting the visible items
                rank: DEFAULT_CONTEXT_ITEM_RANK }, item), contextMenu, menuFactory);
        });
        settings.changed.connect(() => {
            var _a;
            // As extension may change the context menu through API,
            // prompt the user to reload if the menu has been updated.
            const newItems = (_a = settings.composite.contextMenu) !== null && _a !== void 0 ? _a : [];
            if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepEqual(contextItems, newItems)) {
                void displayInformation(trans);
            }
        });
        registry.pluginChanged.connect(async (sender, plugin) => {
            var _a, _b, _c, _d;
            if (plugin !== pluginId) {
                // If the plugin changed its menu.
                const oldItems = (_a = loaded[plugin]) !== null && _a !== void 0 ? _a : [];
                const newItems = (_c = (_b = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _b === void 0 ? void 0 : _b.context) !== null && _c !== void 0 ? _c : [];
                if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepEqual(oldItems, newItems)) {
                    if (loaded[plugin]) {
                        // The plugin has changed, request the user to reload the UI
                        await displayInformation(trans);
                    }
                    else {
                        // The plugin was not yet loaded when the menu was built => update the menu
                        loaded[plugin] = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(newItems);
                        // Merge potential disabled state
                        const toAdd = (_d = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.reconcileItems(newItems, contextItems, false, false)) !== null && _d !== void 0 ? _d : [];
                        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.filterDisabledItems(toAdd).forEach(item => {
                            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.addContextItem(Object.assign({ 
                                // We have to set the default rank because Lumino is sorting the visible items
                                rank: DEFAULT_CONTEXT_ITEM_RANK }, item), contextMenu, menuFactory);
                        });
                    }
                }
            }
        });
    }
    Private.loadSettingsContextMenu = loadSettingsContextMenu;
    function activateSidebarSwitcher(app, labShell, settingRegistry, translator, initial) {
        const setting = '@jupyterlab/application-extension:sidebar';
        const trans = translator.load('jupyterlab');
        let overrides = {};
        const update = (_, layout) => {
            (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.each)(labShell.widgets('left'), widget => {
                var _a;
                if (overrides[widget.id] && overrides[widget.id] === 'right') {
                    labShell.add(widget, 'right');
                    if (layout && ((_a = layout.rightArea) === null || _a === void 0 ? void 0 : _a.currentWidget) === widget) {
                        labShell.activateById(widget.id);
                    }
                }
            });
            (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.each)(labShell.widgets('right'), widget => {
                var _a;
                if (overrides[widget.id] && overrides[widget.id] === 'left') {
                    labShell.add(widget, 'left');
                    if (layout && ((_a = layout.leftArea) === null || _a === void 0 ? void 0 : _a.currentWidget) === widget) {
                        labShell.activateById(widget.id);
                    }
                }
            });
        };
        // Fetch overrides from the settings system.
        void Promise.all([settingRegistry.load(setting), app.restored]).then(([settings]) => {
            overrides = (settings.get('overrides').composite ||
                {});
            settings.changed.connect(settings => {
                overrides = (settings.get('overrides').composite ||
                    {});
                update(labShell);
            });
            labShell.layoutModified.connect(update);
            update(labShell, initial);
        });
        // Add a command to switch a side panels's side
        app.commands.addCommand(CommandIDs.switchSidebar, {
            label: trans.__('Switch Sidebar Side'),
            execute: () => {
                // First, try to find the correct panel based on the application
                // context menu click. Bail if we don't find a sidebar for the widget.
                const contextNode = app.contextMenuHitTest(node => !!node.dataset.id);
                if (!contextNode) {
                    return;
                }
                const id = contextNode.dataset['id'];
                const leftPanel = document.getElementById('jp-left-stack');
                const node = document.getElementById(id);
                let side;
                if (leftPanel && node && leftPanel.contains(node)) {
                    side = 'right';
                }
                else {
                    side = 'left';
                }
                // Move the panel to the other side.
                return settingRegistry.set(setting, 'overrides', Object.assign(Object.assign({}, overrides), { [id]: side }));
            }
        });
    }
    Private.activateSidebarSwitcher = activateSidebarSwitcher;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvYXBwbGljYXRpb24tZXh0ZW5zaW9uL3NyYy9pbmRleC50c3giXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBaUI4QjtBQVFIO0FBQzZCO0FBSW5CO0FBQ3dDO0FBQ2pDO0FBQzBCO0FBTXRDO0FBQ3FCO0FBQ0s7QUFDVTtBQUNQO0FBQ2pDO0FBRS9COztHQUVHO0FBQ0ksTUFBTSx5QkFBeUIsR0FBRyxHQUFHLENBQUM7QUFFN0M7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FpQ25CO0FBakNELFdBQVUsVUFBVTtJQUNMLDBCQUFlLEdBQVcsK0JBQStCLENBQUM7SUFFMUQsOEJBQW1CLEdBQzlCLG1DQUFtQyxDQUFDO0lBRXpCLDZCQUFrQixHQUFXLG1DQUFtQyxDQUFDO0lBRWpFLGlDQUFzQixHQUNqQyx1Q0FBdUMsQ0FBQztJQUU3QixnQkFBSyxHQUFHLG1CQUFtQixDQUFDO0lBRTVCLHlCQUFjLEdBQUcsOEJBQThCLENBQUM7SUFFaEQseUJBQWMsR0FBRyw4QkFBOEIsQ0FBQztJQUVoRCxtQkFBUSxHQUFXLHVCQUF1QixDQUFDO0lBRTNDLGtCQUFPLEdBQVcsc0JBQXNCLENBQUM7SUFFekMscUJBQVUsR0FBVyx5QkFBeUIsQ0FBQztJQUUvQyx5QkFBYyxHQUFXLDhCQUE4QixDQUFDO0lBRXhELDBCQUFlLEdBQVcsK0JBQStCLENBQUM7SUFFMUQsaUNBQXNCLEdBQ2pDLHNDQUFzQyxDQUFDO0lBRTVCLGVBQUksR0FBVyxhQUFhLENBQUM7SUFFN0Isd0JBQWEsR0FBRyxnQkFBZ0IsQ0FBQztBQUNoRCxDQUFDLEVBakNTLFVBQVUsS0FBVixVQUFVLFFBaUNuQjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxZQUFZLEdBQWdDO0lBQ2hELEVB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RUQsb0NBQW9DO2dCQUNwQyxPQUFPLGVBQWUsQ0FBQyxHQUFHLENBQUMsT0FBTyxFQUFFLFdBQVcsa0NBQzFDLFNBQVMsS0FDWixDQUFDLEVBQUUsQ0FBQyxFQUFFLElBQUksSUFDVixDQUFDO1lBQ0wsQ0FBQztTQUNGLENBQUMsQ0FBQztJQUNMLENBQUM7SUExRWUsK0JBQXVCLDBCQTBFdEM7QUFDSCxDQUFDLEVBOVBTLE9BQU8sS0FBUCxPQUFPLFFBOFBoQiIsImZpbGUiOiJwYWNrYWdlc19hcHBsaWNhdGlvbi1leHRlbnNpb25fbGliX2luZGV4X2pzLjk2NzQ3NTEwMDMwMzFmOGNhY2RjLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgYXBwbGljYXRpb24tZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgQ29ubmVjdGlvbkxvc3QsXG4gIElDb25uZWN0aW9uTG9zdCxcbiAgSUxhYlNoZWxsLFxuICBJTGFiU3RhdHVzLFxuICBJTGF5b3V0UmVzdG9yZXIsXG4gIElSb3V0ZXIsXG4gIElUcmVlUGF0aFVwZGF0ZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kQ29udGV4dE1lbnUsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpbixcbiAgSnVweXRlckxhYixcbiAgTGFiU2hlbGwsXG4gIExheW91dFJlc3RvcmVyLFxuICBSb3V0ZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgRGlhbG9nLFxuICBJQ29tbWFuZFBhbGV0dGUsXG4gIElXaW5kb3dSZXNvbHZlcixcbiAgTWVudUZhY3RvcnksXG4gIHNob3dEaWFsb2csXG4gIHNob3dFcnJvck1lc3NhZ2Vcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgUGFnZUNvbmZpZywgVVJMRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIElQcm9wZXJ0eUluc3BlY3RvclByb3ZpZGVyLFxuICBTaWRlQmFyUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlclxufSBmcm9tICdAanVweXRlcmxhYi9wcm9wZXJ0eS1pbnNwZWN0b3InO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSwgU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElTdGF0ZURCIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc3RhdGVkYic7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgVHJhbnNsYXRpb25CdW5kbGUgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQge1xuICBidWlsZEljb24sXG4gIENvbnRleHRNZW51U3ZnLFxuICBqdXB5dGVySWNvbixcbiAgUmFua2VkTWVudVxufSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IGVhY2gsIGl0ZXIsIHRvQXJyYXkgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBKU09ORXh0LCBQcm9taXNlRGVsZWdhdGUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBEaXNwb3NhYmxlRGVsZWdhdGUsIERpc3Bvc2FibGVTZXQgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgRG9ja0xheW91dCwgRG9ja1BhbmVsLCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG4vKipcbiAqIERlZmF1bHQgY29udGV4dCBtZW51IGl0ZW0gcmFua1xuICovXG5leHBvcnQgY29uc3QgREVGQVVMVF9DT05URVhUX0lURU1fUkFOSyA9IDEwMDtcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgYXBwbGljYXRpb24gcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBhY3RpdmF0ZU5leHRUYWI6IHN0cmluZyA9ICdhcHBsaWNhdGlvbjphY3RpdmF0ZS1uZXh0LXRhYic7XG5cbiAgZXhwb3J0IGNvbnN0IGFjdGl2YXRlUHJldmlvdXNUYWI6IHN0cmluZyA9XG4gICAgJ2FwcGxpY2F0aW9uOmFjdGl2YXRlLXByZXZpb3VzLXRhYic7XG5cbiAgZXhwb3J0IGNvbnN0IGFjdGl2YXRlTmV4dFRhYkJhcjogc3RyaW5nID0gJ2FwcGxpY2F0aW9uOmFjdGl2YXRlLW5leHQtdGFiLWJhcic7XG5cbiAgZXhwb3J0IGNvbnN0IGFjdGl2YXRlUHJldmlvdXNUYWJCYXI6IHN0cmluZyA9XG4gICAgJ2FwcGxpY2F0aW9uOmFjdGl2YXRlLXByZXZpb3VzLXRhYi1iYXInO1xuXG4gIGV4cG9ydCBjb25zdCBjbG9zZSA9ICdhcHBsaWNhdGlvbjpjbG9zZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGNsb3NlT3RoZXJUYWJzID0gJ2FwcGxpY2F0aW9uOmNsb3NlLW90aGVyLXRhYnMnO1xuXG4gIGV4cG9ydCBjb25zdCBjbG9zZVJpZ2h0VGFicyA9ICdhcHBsaWNhdGlvbjpjbG9zZS1yaWdodC10YWJzJztcblxuICBleHBvcnQgY29uc3QgY2xvc2VBbGw6IHN0cmluZyA9ICdhcHBsaWNhdGlvbjpjbG9zZS1hbGwnO1xuXG4gIGV4cG9ydCBjb25zdCBzZXRNb2RlOiBzdHJpbmcgPSAnYXBwbGljYXRpb246c2V0LW1vZGUnO1xuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVNb2RlOiBzdHJpbmcgPSAnYXBwbGljYXRpb246dG9nZ2xlLW1vZGUnO1xuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVMZWZ0QXJlYTogc3RyaW5nID0gJ2FwcGxpY2F0aW9uOnRvZ2dsZS1sZWZ0LWFyZWEnO1xuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVSaWdodEFyZWE6IHN0cmluZyA9ICdhcHBsaWNhdGlvbjp0b2dnbGUtcmlnaHQtYXJlYSc7XG5cbiAgZXhwb3J0IGNvbnN0IHRvZ2dsZVByZXNlbnRhdGlvbk1vZGU6IHN0cmluZyA9XG4gICAgJ2FwcGxpY2F0aW9uOnRvZ2dsZS1wcmVzZW50YXRpb24tbW9kZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHRyZWU6IHN0cmluZyA9ICdyb3V0ZXI6dHJlZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHN3aXRjaFNpZGViYXIgPSAnc2lkZWJhcjpzd2l0Y2gnO1xufVxuXG4vKipcbiAqIEEgcGx1Z2luIHRvIHJlZ2lzdGVyIHRoZSBjb21tYW5kcyBmb3IgdGhlIG1haW4gYXBwbGljYXRpb24uXG4gKi9cbmNvbnN0IG1haW5Db21tYW5kczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpjb21tYW5kcycsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUxhYlNoZWxsLCBJQ29tbWFuZFBhbGV0dGVdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ01haW4gQXJlYScpO1xuXG4gICAgLy8gQWRkIENvbW1hbmQgdG8gb3ZlcnJpZGUgdGhlIEpMYWIgY29udGV4dCBtZW51LlxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoSnVweXRlckZyb250RW5kQ29udGV4dE1lbnUuY29udGV4dE1lbnUsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnU2hpZnQrUmlnaHQgQ2xpY2sgZm9yIEJyb3dzZXIgTWVudScpLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiBmYWxzZSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHZvaWQgMFxuICAgIH0pO1xuXG4gICAgLy8gUmV0dXJucyB0aGUgd2lkZ2V0IGFzc29jaWF0ZWQgd2l0aCB0aGUgbW9zdCByZWNlbnQgY29udGV4dG1lbnUgZXZlbnQuXG4gICAgY29uc3QgY29udGV4dE1lbnVXaWRnZXQgPSAoKTogV2lkZ2V0IHwgbnVsbCA9PiB7XG4gICAgICBjb25zdCB0ZXN0ID0gKG5vZGU6IEhUTUxFbGVtZW50KSA9PiAhIW5vZGUuZGF0YXNldC5pZDtcbiAgICAgIGNvbnN0IG5vZGUgPSBhcHAuY29udGV4dE1lbnVIaXRUZXN0KHRlc3QpO1xuXG4gICAgICBpZiAoIW5vZGUpIHtcbiAgICAgICAgLy8gRmFsbCBiYWNrIHRvIGFjdGl2ZSB3aWRnZXQgaWYgcGF0aCBjYW5ub3QgYmUgb2J0YWluZWQgZnJvbSBldmVudC5cbiAgICAgICAgcmV0dXJuIHNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IG1hdGNoZXMgPSB0b0FycmF5KHNoZWxsLndpZGdldHMoJ21haW4nKSkuZmlsdGVyKFxuICAgICAgICB3aWRnZXQgPT4gd2lkZ2V0LmlkID09PSBub2RlLmRhdGFzZXQuaWRcbiAgICAgICk7XG5cbiAgICAgIGlmIChtYXRjaGVzLmxlbmd0aCA8IDEpIHtcbiAgICAgICAgcmV0dXJuIHNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBtYXRjaGVzWzBdO1xuICAgIH07XG5cbiAgICAvLyBDbG9zZXMgYW4gYXJyYXkgb2Ygd2lkZ2V0cy5cbiAgICBjb25zdCBjbG9zZVdpZGdldHMgPSAod2lkZ2V0czogQXJyYXk8V2lkZ2V0Pik6IHZvaWQgPT4ge1xuICAgICAgd2lkZ2V0cy5mb3JFYWNoKHdpZGdldCA9PiB3aWRnZXQuY2xvc2UoKSk7XG4gICAgfTtcblxuICAgIC8vIEZpbmQgdGhlIHRhYiBhcmVhIGZvciBhIHdpZGdldCB3aXRoaW4gYSBzcGVjaWZpYyBkb2NrIGFyZWEuXG4gICAgY29uc3QgZmluZFRhYiA9IChcbiAgICAgIGFyZWE6IERvY2tMYXlvdXQuQXJlYUNvbmZpZyxcbiAgICAgIHdpZGdldDogV2lkZ2V0XG4gICAgKTogRG9ja0xheW91dC5JVGFiQXJlYUNvbmZpZyB8IG51bGwgPT4ge1xuICAgICAgc3dpdGNoIChhcmVhLnR5cGUpIHtcbiAgICAgICAgY2FzZSAnc3BsaXQtYXJlYSc6IHtcbiAgICAgICAgICBjb25zdCBpdGVyYXRvciA9IGl0ZXIoYXJlYS5jaGlsZHJlbik7XG4gICAgICAgICAgbGV0IHRhYjogRG9ja0xheW91dC5JVGFiQXJlYUNvbmZpZyB8IG51bGwgPSBudWxsO1xuICAgICAgICAgIGxldCB2YWx1ZTogRG9ja0xheW91dC5BcmVhQ29uZmlnIHwgdW5kZWZpbmVkO1xuICAgICAgICAgIGRvIHtcbiAgICAgICAgICAgIHZhbHVlID0gaXRlcmF0b3IubmV4dCgpO1xuICAgICAgICAgICAgaWYgKHZhbHVlKSB7XG4gICAgICAgICAgICAgIHRhYiA9IGZpbmRUYWIodmFsdWUsIHdpZGdldCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSB3aGlsZSAoIXRhYiAmJiB2YWx1ZSk7XG4gICAgICAgICAgcmV0dXJuIHRhYjtcbiAgICAgICAgfVxuICAgICAgICBjYXNlICd0YWItYXJlYSc6IHtcbiAgICAgICAgICBjb25zdCB7IGlkIH0gPSB3aWRnZXQ7XG4gICAgICAgICAgcmV0dXJuIGFyZWEud2lkZ2V0cy5zb21lKHdpZGdldCA9PiB3aWRnZXQuaWQgPT09IGlkKSA/IGFyZWEgOiBudWxsO1xuICAgICAgICB9XG4gICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICB9XG4gICAgfTtcblxuICAgIC8vIEZpbmQgdGhlIHRhYiBhcmVhIGZvciBhIHdpZGdldCB3aXRoaW4gdGhlIG1haW4gZG9jayBhcmVhLlxuICAgIGNvbnN0IHRhYkFyZWFGb3IgPSAod2lkZ2V0OiBXaWRnZXQpOiBEb2NrTGF5b3V0LklUYWJBcmVhQ29uZmlnIHwgbnVsbCA9PiB7XG4gICAgICBjb25zdCBsYXlvdXQgPSBsYWJTaGVsbD8uc2F2ZUxheW91dCgpO1xuICAgICAgY29uc3QgbWFpbkFyZWEgPSBsYXlvdXQ/Lm1haW5BcmVhO1xuICAgICAgaWYgKCFtYWluQXJlYSB8fCBQYWdlQ29uZmlnLmdldE9wdGlvbignbW9kZScpICE9PSAnbXVsdGlwbGUtZG9jdW1lbnQnKSB7XG4gICAgICAgIHJldHVybiBudWxsO1xuICAgICAgfVxuICAgICAgY29uc3QgYXJlYSA9IG1haW5BcmVhLmRvY2s/Lm1haW47XG4gICAgICBpZiAoIWFyZWEpIHtcbiAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICB9XG4gICAgICByZXR1cm4gZmluZFRhYihhcmVhLCB3aWRnZXQpO1xuICAgIH07XG5cbiAgICAvLyBSZXR1cm5zIGFuIGFycmF5IG9mIGFsbCB3aWRnZXRzIHRvIHRoZSByaWdodCBvZiBhIHdpZGdldCBpbiBhIHRhYiBhcmVhLlxuICAgIGNvbnN0IHdpZGdldHNSaWdodE9mID0gKHdpZGdldDogV2lkZ2V0KTogQXJyYXk8V2lkZ2V0PiA9PiB7XG4gICAgICBjb25zdCB7IGlkIH0gPSB3aWRnZXQ7XG4gICAgICBjb25zdCB0YWJBcmVhID0gdGFiQXJlYUZvcih3aWRnZXQpO1xuICAgICAgY29uc3Qgd2lkZ2V0cyA9IHRhYkFyZWEgPyB0YWJBcmVhLndpZGdldHMgfHwgW10gOiBbXTtcbiAgICAgIGNvbnN0IGluZGV4ID0gd2lkZ2V0cy5maW5kSW5kZXgod2lkZ2V0ID0+IHdpZGdldC5pZCA9PT0gaWQpO1xuICAgICAgaWYgKGluZGV4IDwgMCkge1xuICAgICAgICByZXR1cm4gW107XG4gICAgICB9XG4gICAgICByZXR1cm4gd2lkZ2V0cy5zbGljZShpbmRleCArIDEpO1xuICAgIH07XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY2xvc2UsIHtcbiAgICAgIGxhYmVsOiAoKSA9PiB0cmFucy5fXygnQ2xvc2UgVGFiJyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gY29udGV4dE1lbnVXaWRnZXQoKTtcbiAgICAgICAgcmV0dXJuICEhd2lkZ2V0ICYmIHdpZGdldC50aXRsZS5jbG9zYWJsZTtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IGNvbnRleHRNZW51V2lkZ2V0KCk7XG4gICAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgICB3aWRnZXQuY2xvc2UoKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNsb3NlT3RoZXJUYWJzLCB7XG4gICAgICBsYWJlbDogKCkgPT4gdHJhbnMuX18oJ0Nsb3NlIEFsbCBPdGhlciBUYWJzJyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgLy8gRW5zdXJlIHRoZXJlIGFyZSBhdCBsZWFzdCB0d28gd2lkZ2V0cy5cbiAgICAgICAgY29uc3QgaXRlcmF0b3IgPSBzaGVsbC53aWRnZXRzKCdtYWluJyk7XG4gICAgICAgIHJldHVybiAhIWl0ZXJhdG9yLm5leHQoKSAmJiAhIWl0ZXJhdG9yLm5leHQoKTtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IGNvbnRleHRNZW51V2lkZ2V0KCk7XG4gICAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IHsgaWQgfSA9IHdpZGdldDtcbiAgICAgICAgY29uc3Qgb3RoZXJXaWRnZXRzID0gdG9BcnJheShzaGVsbC53aWRnZXRzKCdtYWluJykpLmZpbHRlcihcbiAgICAgICAgICB3aWRnZXQgPT4gd2lkZ2V0LmlkICE9PSBpZFxuICAgICAgICApO1xuICAgICAgICBjbG9zZVdpZGdldHMob3RoZXJXaWRnZXRzKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jbG9zZVJpZ2h0VGFicywge1xuICAgICAgbGFiZWw6ICgpID0+IHRyYW5zLl9fKCdDbG9zZSBUYWJzIHRvIFJpZ2h0JyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+XG4gICAgICAgICEhY29udGV4dE1lbnVXaWRnZXQoKSAmJlxuICAgICAgICB3aWRnZXRzUmlnaHRPZihjb250ZXh0TWVudVdpZGdldCgpISkubGVuZ3RoID4gMCxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gY29udGV4dE1lbnVXaWRnZXQoKTtcbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY2xvc2VXaWRnZXRzKHdpZGdldHNSaWdodE9mKHdpZGdldCkpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgaWYgKGxhYlNoZWxsKSB7XG4gICAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuYWN0aXZhdGVOZXh0VGFiLCB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnQWN0aXZhdGUgTmV4dCBUYWInKSxcbiAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgIGxhYlNoZWxsLmFjdGl2YXRlTmV4dFRhYigpO1xuICAgICAgICB9XG4gICAgICB9KTtcblxuICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmFjdGl2YXRlUHJldmlvdXNUYWIsIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdBY3RpdmF0ZSBQcmV2aW91cyBUYWInKSxcbiAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgIGxhYlNoZWxsLmFjdGl2YXRlUHJldmlvdXNUYWIoKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5hY3RpdmF0ZU5leHRUYWJCYXIsIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdBY3RpdmF0ZSBOZXh0IFRhYiBCYXInKSxcbiAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgIGxhYlNoZWxsLmFjdGl2YXRlTmV4dFRhYkJhcigpO1xuICAgICAgICB9XG4gICAgICB9KTtcblxuICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmFjdGl2YXRlUHJldmlvdXNUYWJCYXIsIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdBY3RpdmF0ZSBQcmV2aW91cyBUYWIgQmFyJyksXG4gICAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgICBsYWJTaGVsbC5hY3RpdmF0ZVByZXZpb3VzVGFiQmFyKCk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuXG4gICAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY2xvc2VBbGwsIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdDbG9zZSBBbGwgVGFicycpLFxuICAgICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgICAgbGFiU2hlbGwuY2xvc2VBbGwoKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVMZWZ0QXJlYSwge1xuICAgICAgICBsYWJlbDogKCkgPT4gdHJhbnMuX18oJ1Nob3cgTGVmdCBTaWRlYmFyJyksXG4gICAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgICBpZiAobGFiU2hlbGwubGVmdENvbGxhcHNlZCkge1xuICAgICAgICAgICAgbGFiU2hlbGwuZXhwYW5kTGVmdCgpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBsYWJTaGVsbC5jb2xsYXBzZUxlZnQoKTtcbiAgICAgICAgICAgIGlmIChsYWJTaGVsbC5jdXJyZW50V2lkZ2V0KSB7XG4gICAgICAgICAgICAgIGxhYlNoZWxsLmFjdGl2YXRlQnlJZChsYWJTaGVsbC5jdXJyZW50V2lkZ2V0LmlkKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGlzVG9nZ2xlZDogKCkgPT4gIWxhYlNoZWxsLmxlZnRDb2xsYXBzZWQsXG4gICAgICAgIGlzVmlzaWJsZTogKCkgPT4gIWxhYlNoZWxsLmlzRW1wdHkoJ2xlZnQnKVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVSaWdodEFyZWEsIHtcbiAgICAgICAgbGFiZWw6ICgpID0+IHRyYW5zLl9fKCdTaG93IFJpZ2h0IFNpZGViYXInKSxcbiAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgIGlmIChsYWJTaGVsbC5yaWdodENvbGxhcHNlZCkge1xuICAgICAgICAgICAgbGFiU2hlbGwuZXhwYW5kUmlnaHQoKTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgbGFiU2hlbGwuY29sbGFwc2VSaWdodCgpO1xuICAgICAgICAgICAgaWYgKGxhYlNoZWxsLmN1cnJlbnRXaWRnZXQpIHtcbiAgICAgICAgICAgICAgbGFiU2hlbGwuYWN0aXZhdGVCeUlkKGxhYlNoZWxsLmN1cnJlbnRXaWRnZXQuaWQpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgaXNUb2dnbGVkOiAoKSA9PiAhbGFiU2hlbGwucmlnaHRDb2xsYXBzZWQsXG4gICAgICAgIGlzVmlzaWJsZTogKCkgPT4gIWxhYlNoZWxsLmlzRW1wdHkoJ3JpZ2h0JylcbiAgICAgIH0pO1xuXG4gICAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMudG9nZ2xlUHJlc2VudGF0aW9uTW9kZSwge1xuICAgICAgICBsYWJlbDogKCkgPT4gdHJhbnMuX18oJ1ByZXNlbnRhdGlvbiBNb2RlJyksXG4gICAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgICBsYWJTaGVsbC5wcmVzZW50YXRpb25Nb2RlID0gIWxhYlNoZWxsLnByZXNlbnRhdGlvbk1vZGU7XG4gICAgICAgIH0sXG4gICAgICAgIGlzVG9nZ2xlZDogKCkgPT4gbGFiU2hlbGwucHJlc2VudGF0aW9uTW9kZSxcbiAgICAgICAgaXNWaXNpYmxlOiAoKSA9PiB0cnVlXG4gICAgICB9KTtcblxuICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNldE1vZGUsIHtcbiAgICAgICAgaXNWaXNpYmxlOiBhcmdzID0+IHtcbiAgICAgICAgICBjb25zdCBtb2RlID0gYXJnc1snbW9kZSddIGFzIHN0cmluZztcbiAgICAgICAgICByZXR1cm4gbW9kZSA9PT0gJ3NpbmdsZS1kb2N1bWVudCcgfHwgbW9kZSA9PT0gJ211bHRpcGxlLWRvY3VtZW50JztcbiAgICAgICAgfSxcbiAgICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgICAgY29uc3QgbW9kZSA9IGFyZ3NbJ21vZGUnXSBhcyBzdHJpbmc7XG4gICAgICAgICAgaWYgKG1vZGUgPT09ICdzaW5nbGUtZG9jdW1lbnQnIHx8IG1vZGUgPT09ICdtdWx0aXBsZS1kb2N1bWVudCcpIHtcbiAgICAgICAgICAgIGxhYlNoZWxsLm1vZGUgPSBtb2RlO1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgIH1cbiAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYFVuc3VwcG9ydGVkIGFwcGxpY2F0aW9uIHNoZWxsIG1vZGU6ICR7bW9kZX1gKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVNb2RlLCB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnU2ltcGxlIEludGVyZmFjZScpLFxuICAgICAgICBpc1RvZ2dsZWQ6ICgpID0+IGxhYlNoZWxsLm1vZGUgPT09ICdzaW5nbGUtZG9jdW1lbnQnLFxuICAgICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgICAgY29uc3QgYXJncyA9XG4gICAgICAgICAgICBsYWJTaGVsbC5tb2RlID09PSAnbXVsdGlwbGUtZG9jdW1lbnQnXG4gICAgICAgICAgICAgID8geyBtb2RlOiAnc2luZ2xlLWRvY3VtZW50JyB9XG4gICAgICAgICAgICAgIDogeyBtb2RlOiAnbXVsdGlwbGUtZG9jdW1lbnQnIH07XG4gICAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5zZXRNb2RlLCBhcmdzKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuXG4gICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgIFtcbiAgICAgICAgQ29tbWFuZElEcy5hY3RpdmF0ZU5leHRUYWIsXG4gICAgICAgIENvbW1hbmRJRHMuYWN0aXZhdGVQcmV2aW91c1RhYixcbiAgICAgICAgQ29tbWFuZElEcy5hY3RpdmF0ZU5leHRUYWJCYXIsXG4gICAgICAgIENvbW1hbmRJRHMuYWN0aXZhdGVQcmV2aW91c1RhYkJhcixcbiAgICAgICAgQ29tbWFuZElEcy5jbG9zZSxcbiAgICAgICAgQ29tbWFuZElEcy5jbG9zZUFsbCxcbiAgICAgICAgQ29tbWFuZElEcy5jbG9zZU90aGVyVGFicyxcbiAgICAgICAgQ29tbWFuZElEcy5jbG9zZVJpZ2h0VGFicyxcbiAgICAgICAgQ29tbWFuZElEcy50b2dnbGVMZWZ0QXJlYSxcbiAgICAgICAgQ29tbWFuZElEcy50b2dnbGVSaWdodEFyZWEsXG4gICAgICAgIENvbW1hbmRJRHMudG9nZ2xlUHJlc2VudGF0aW9uTW9kZSxcbiAgICAgICAgQ29tbWFuZElEcy50b2dnbGVNb2RlXG4gICAgICBdLmZvckVhY2goY29tbWFuZCA9PiBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kLCBjYXRlZ29yeSB9KSk7XG4gICAgfVxuICB9XG59O1xuXG4vKipcbiAqIFRoZSBtYWluIGV4dGVuc2lvbi5cbiAqL1xuY29uc3QgbWFpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElUcmVlUGF0aFVwZGF0ZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjptYWluJyxcbiAgcmVxdWlyZXM6IFtcbiAgICBJUm91dGVyLFxuICAgIElXaW5kb3dSZXNvbHZlcixcbiAgICBJVHJhbnNsYXRvcixcbiAgICBKdXB5dGVyRnJvbnRFbmQuSVRyZWVSZXNvbHZlclxuICBdLFxuICBvcHRpb25hbDogW0lDb25uZWN0aW9uTG9zdF0sXG4gIHByb3ZpZGVzOiBJVHJlZVBhdGhVcGRhdGVyLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHJvdXRlcjogSVJvdXRlcixcbiAgICByZXNvbHZlcjogSVdpbmRvd1Jlc29sdmVyLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHRyZWVSZXNvbHZlcjogSnVweXRlckZyb250RW5kLklUcmVlUmVzb2x2ZXIsXG4gICAgY29ubmVjdGlvbkxvc3Q6IElDb25uZWN0aW9uTG9zdCB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIGlmICghKGFwcCBpbnN0YW5jZW9mIEp1cHl0ZXJMYWIpKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYCR7bWFpbi5pZH0gbXVzdCBiZSBhY3RpdmF0ZWQgaW4gSnVweXRlckxhYi5gKTtcbiAgICB9XG5cbiAgICAvLyBUaGVzZSB0d28gaW50ZXJuYWwgc3RhdGUgdmFyaWFibGVzIGFyZSB1c2VkIHRvIG1hbmFnZSB0aGUgdHdvIHNvdXJjZVxuICAgIC8vIG9mIHRoZSB0cmVlIHBhcnQgb2YgdGhlIFVSTCBiZWluZyB1cGRhdGVkOiAxKSBwYXRoIG9mIHRoZSBhY3RpdmUgZG9jdW1lbnQsXG4gICAgLy8gMikgcGF0aCBvZiB0aGUgZGVmYXVsdCBicm93c2VyIGlmIHRoZSBhY3RpdmUgbWFpbiBhcmVhIHdpZGdldCBpc24ndCBhIGRvY3VtZW50LlxuICAgIGxldCBfZG9jVHJlZVBhdGggPSAnJztcbiAgICBsZXQgX2RlZmF1bHRCcm93c2VyVHJlZVBhdGggPSAnJztcblxuICAgIGZ1bmN0aW9uIHVwZGF0ZVRyZWVQYXRoKHRyZWVQYXRoOiBzdHJpbmcpIHtcbiAgICAgIC8vIFdhaXQgZm9yIHRyZWUgcmVzb2x2ZXIgdG8gZmluaXNoIGJlZm9yZSB1cGRhdGluZyB0aGUgcGF0aCBiZWNhdXNlIGl0IHVzZSB0aGUgUGFnZUNvbmZpZ1sndHJlZVBhdGgnXVxuICAgICAgdm9pZCB0cmVlUmVzb2x2ZXIucGF0aHMudGhlbigoKSA9PiB7XG4gICAgICAgIF9kZWZhdWx0QnJvd3NlclRyZWVQYXRoID0gdHJlZVBhdGg7XG4gICAgICAgIGlmICghX2RvY1RyZWVQYXRoKSB7XG4gICAgICAgICAgY29uc3QgdXJsID0gUGFnZUNvbmZpZy5nZXRVcmwoeyB0cmVlUGF0aCB9KTtcbiAgICAgICAgICBjb25zdCBwYXRoID0gVVJMRXh0LnBhcnNlKHVybCkucGF0aG5hbWU7XG4gICAgICAgICAgcm91dGVyLm5hdmlnYXRlKHBhdGgsIHsgc2tpcFJvdXRpbmc6IHRydWUgfSk7XG4gICAgICAgICAgLy8gUGVyc2lzdCB0aGUgbmV3IHRyZWUgcGF0aCB0byBQYWdlQ29uZmlnIGFzIGl0IGlzIHVzZWQgZWxzZXdoZXJlIGF0IHJ1bnRpbWUuXG4gICAgICAgICAgUGFnZUNvbmZpZy5zZXRPcHRpb24oJ3RyZWVQYXRoJywgdHJlZVBhdGgpO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICAvLyBSZXF1aXJpbmcgdGhlIHdpbmRvdyByZXNvbHZlciBndWFyYW50ZWVzIHRoYXQgdGhlIGFwcGxpY2F0aW9uIGV4dGVuc2lvblxuICAgIC8vIG9ubHkgbG9hZHMgaWYgdGhlcmUgaXMgYSB2aWFibGUgd2luZG93IG5hbWUuIE90aGVyd2lzZSwgdGhlIGFwcGxpY2F0aW9uXG4gICAgLy8gd2lsbCBzaG9ydC1jaXJjdWl0IGFuZCBhc2sgdGhlIHVzZXIgdG8gbmF2aWdhdGUgYXdheS5cbiAgICBjb25zdCB3b3Jrc3BhY2UgPSByZXNvbHZlci5uYW1lO1xuXG4gICAgY29uc29sZS5kZWJ1ZyhgU3RhcnRpbmcgYXBwbGljYXRpb24gaW4gd29ya3NwYWNlOiBcIiR7d29ya3NwYWNlfVwiYCk7XG5cbiAgICAvLyBJZiB0aGVyZSB3ZXJlIGVycm9ycyByZWdpc3RlcmluZyBwbHVnaW5zLCB0ZWxsIHRoZSB1c2VyLlxuICAgIGlmIChhcHAucmVnaXN0ZXJQbHVnaW5FcnJvcnMubGVuZ3RoICE9PSAwKSB7XG4gICAgICBjb25zdCBib2R5ID0gKFxuICAgICAgICA8cHJlPnthcHAucmVnaXN0ZXJQbHVnaW5FcnJvcnMubWFwKGUgPT4gZS5tZXNzYWdlKS5qb2luKCdcXG4nKX08L3ByZT5cbiAgICAgICk7XG5cbiAgICAgIHZvaWQgc2hvd0Vycm9yTWVzc2FnZSh0cmFucy5fXygnRXJyb3IgUmVnaXN0ZXJpbmcgUGx1Z2lucycpLCB7XG4gICAgICAgIG1lc3NhZ2U6IGJvZHlcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIC8vIElmIHRoZSBhcHBsaWNhdGlvbiBzaGVsbCBsYXlvdXQgaXMgbW9kaWZpZWQsXG4gICAgLy8gdHJpZ2dlciBhIHJlZnJlc2ggb2YgdGhlIGNvbW1hbmRzLlxuICAgIGFwcC5zaGVsbC5sYXlvdXRNb2RpZmllZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZCgpO1xuICAgIH0pO1xuXG4gICAgLy8gV2F0Y2ggdGhlIG1vZGUgYW5kIHVwZGF0ZSB0aGUgcGFnZSBVUkwgdG8gL2xhYiBvciAvZG9jIHRvIHJlZmxlY3QgdGhlXG4gICAgLy8gY2hhbmdlLlxuICAgIGFwcC5zaGVsbC5tb2RlQ2hhbmdlZC5jb25uZWN0KChfLCBhcmdzOiBEb2NrUGFuZWwuTW9kZSkgPT4ge1xuICAgICAgY29uc3QgdXJsID0gUGFnZUNvbmZpZy5nZXRVcmwoeyBtb2RlOiBhcmdzIGFzIHN0cmluZyB9KTtcbiAgICAgIGNvbnN0IHBhdGggPSBVUkxFeHQucGFyc2UodXJsKS5wYXRobmFtZTtcbiAgICAgIHJvdXRlci5uYXZpZ2F0ZShwYXRoLCB7IHNraXBSb3V0aW5nOiB0cnVlIH0pO1xuICAgICAgLy8gUGVyc2lzdCB0aGlzIG1vZGUgY2hhbmdlIHRvIFBhZ2VDb25maWcgYXMgaXQgaXMgdXNlZCBlbHNld2hlcmUgYXQgcnVudGltZS5cbiAgICAgIFBhZ2VDb25maWcuc2V0T3B0aW9uKCdtb2RlJywgYXJncyBhcyBzdHJpbmcpO1xuICAgIH0pO1xuXG4gICAgLy8gV2FpdCBmb3IgdHJlZSByZXNvbHZlciB0byBmaW5pc2ggYmVmb3JlIHVwZGF0aW5nIHRoZSBwYXRoIGJlY2F1c2UgaXQgdXNlIHRoZSBQYWdlQ29uZmlnWyd0cmVlUGF0aCddXG4gICAgdm9pZCB0cmVlUmVzb2x2ZXIucGF0aHMudGhlbigoKSA9PiB7XG4gICAgICAvLyBXYXRjaCB0aGUgcGF0aCBvZiB0aGUgY3VycmVudCB3aWRnZXQgaW4gdGhlIG1haW4gYXJlYSBhbmQgdXBkYXRlIHRoZSBwYWdlXG4gICAgICAvLyBVUkwgdG8gcmVmbGVjdCB0aGUgY2hhbmdlLlxuICAgICAgYXBwLnNoZWxsLmN1cnJlbnRQYXRoQ2hhbmdlZC5jb25uZWN0KChfLCBhcmdzKSA9PiB7XG4gICAgICAgIGNvbnN0IG1heWJlVHJlZVBhdGggPSBhcmdzLm5ld1ZhbHVlIGFzIHN0cmluZztcbiAgICAgICAgY29uc3QgdHJlZVBhdGggPSBtYXliZVRyZWVQYXRoIHx8IF9kZWZhdWx0QnJvd3NlclRyZWVQYXRoO1xuICAgICAgICBjb25zdCB1cmwgPSBQYWdlQ29uZmlnLmdldFVybCh7IHRyZWVQYXRoOiB0cmVlUGF0aCB9KTtcbiAgICAgICAgY29uc3QgcGF0aCA9IFVSTEV4dC5wYXJzZSh1cmwpLnBhdGhuYW1lO1xuICAgICAgICByb3V0ZXIubmF2aWdhdGUocGF0aCwgeyBza2lwUm91dGluZzogdHJ1ZSB9KTtcbiAgICAgICAgLy8gUGVyc2lzdCB0aGUgbmV3IHRyZWUgcGF0aCB0byBQYWdlQ29uZmlnIGFzIGl0IGlzIHVzZWQgZWxzZXdoZXJlIGF0IHJ1bnRpbWUuXG4gICAgICAgIFBhZ2VDb25maWcuc2V0T3B0aW9uKCd0cmVlUGF0aCcsIHRyZWVQYXRoKTtcbiAgICAgICAgX2RvY1RyZWVQYXRoID0gbWF5YmVUcmVlUGF0aDtcbiAgICAgIH0pO1xuICAgIH0pO1xuXG4gICAgLy8gSWYgdGhlIGNvbm5lY3Rpb24gdG8gdGhlIHNlcnZlciBpcyBsb3N0LCBoYW5kbGUgaXQgd2l0aCB0aGVcbiAgICAvLyBjb25uZWN0aW9uIGxvc3QgaGFuZGxlci5cbiAgICBjb25uZWN0aW9uTG9zdCA9IGNvbm5lY3Rpb25Mb3N0IHx8IENvbm5lY3Rpb25Mb3N0O1xuICAgIGFwcC5zZXJ2aWNlTWFuYWdlci5jb25uZWN0aW9uRmFpbHVyZS5jb25uZWN0KChtYW5hZ2VyLCBlcnJvcikgPT5cbiAgICAgIGNvbm5lY3Rpb25Mb3N0IShtYW5hZ2VyLCBlcnJvciwgdHJhbnNsYXRvcilcbiAgICApO1xuXG4gICAgY29uc3QgYnVpbGRlciA9IGFwcC5zZXJ2aWNlTWFuYWdlci5idWlsZGVyO1xuICAgIGNvbnN0IGJ1aWxkID0gKCkgPT4ge1xuICAgICAgcmV0dXJuIGJ1aWxkZXJcbiAgICAgICAgLmJ1aWxkKClcbiAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnQnVpbGQgQ29tcGxldGUnKSxcbiAgICAgICAgICAgIGJvZHk6IChcbiAgICAgICAgICAgICAgPGRpdj5cbiAgICAgICAgICAgICAgICB7dHJhbnMuX18oJ0J1aWxkIHN1Y2Nlc3NmdWxseSBjb21wbGV0ZWQsIHJlbG9hZCBwYWdlPycpfVxuICAgICAgICAgICAgICAgIDxiciAvPlxuICAgICAgICAgICAgICAgIHt0cmFucy5fXygnWW91IHdpbGwgbG9zZSBhbnkgdW5zYXZlZCBjaGFuZ2VzLicpfVxuICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICksXG4gICAgICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oe1xuICAgICAgICAgICAgICAgIGxhYmVsOiB0cmFucy5fXygnUmVsb2FkIFdpdGhvdXQgU2F2aW5nJyksXG4gICAgICAgICAgICAgICAgYWN0aW9uczogWydyZWxvYWQnXVxuICAgICAgICAgICAgICB9KSxcbiAgICAgICAgICAgICAgRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdTYXZlIGFuZCBSZWxvYWQnKSB9KVxuICAgICAgICAgICAgXSxcbiAgICAgICAgICAgIGhhc0Nsb3NlOiB0cnVlXG4gICAgICAgICAgfSk7XG4gICAgICAgIH0pXG4gICAgICAgIC50aGVuKCh7IGJ1dHRvbjogeyBhY2NlcHQsIGFjdGlvbnMgfSB9KSA9PiB7XG4gICAgICAgICAgaWYgKGFjY2VwdCkge1xuICAgICAgICAgICAgdm9pZCBhcHAuY29tbWFuZHNcbiAgICAgICAgICAgICAgLmV4ZWN1dGUoJ2RvY21hbmFnZXI6c2F2ZScpXG4gICAgICAgICAgICAgIC50aGVuKCgpID0+IHtcbiAgICAgICAgICAgICAgICByb3V0ZXIucmVsb2FkKCk7XG4gICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgIC5jYXRjaChlcnIgPT4ge1xuICAgICAgICAgICAgICAgIHZvaWQgc2hvd0Vycm9yTWVzc2FnZSh0cmFucy5fXygnU2F2ZSBGYWlsZWQnKSwge1xuICAgICAgICAgICAgICAgICAgbWVzc2FnZTogPHByZT57ZXJyLm1lc3NhZ2V9PC9wcmU+XG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH0gZWxzZSBpZiAoYWN0aW9ucy5pbmNsdWRlcygncmVsb2FkJykpIHtcbiAgICAgICAgICAgIHJvdXRlci5yZWxvYWQoKTtcbiAgICAgICAgICB9XG4gICAgICAgIH0pXG4gICAgICAgIC5jYXRjaChlcnIgPT4ge1xuICAgICAgICAgIHZvaWQgc2hvd0Vycm9yTWVzc2FnZSh0cmFucy5fXygnQnVpbGQgRmFpbGVkJyksIHtcbiAgICAgICAgICAgIG1lc3NhZ2U6IDxwcmU+e2Vyci5tZXNzYWdlfTwvcHJlPlxuICAgICAgICAgIH0pO1xuICAgICAgICB9KTtcbiAgICB9O1xuXG4gICAgaWYgKGJ1aWxkZXIuaXNBdmFpbGFibGUgJiYgYnVpbGRlci5zaG91bGRDaGVjaykge1xuICAgICAgdm9pZCBidWlsZGVyLmdldFN0YXR1cygpLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICBpZiAocmVzcG9uc2Uuc3RhdHVzID09PSAnYnVpbGRpbmcnKSB7XG4gICAgICAgICAgcmV0dXJuIGJ1aWxkKCk7XG4gICAgICAgIH1cblxuICAgICAgICBpZiAocmVzcG9uc2Uuc3RhdHVzICE9PSAnbmVlZGVkJykge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGJvZHkgPSAoXG4gICAgICAgICAgPGRpdj5cbiAgICAgICAgICAgIHt0cmFucy5fXygnSnVweXRlckxhYiBidWlsZCBpcyBzdWdnZXN0ZWQ6Jyl9XG4gICAgICAgICAgICA8YnIgLz5cbiAgICAgICAgICAgIDxwcmU+e3Jlc3BvbnNlLm1lc3NhZ2V9PC9wcmU+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG5cbiAgICAgICAgdm9pZCBzaG93RGlhbG9nKHtcbiAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0J1aWxkIFJlY29tbWVuZGVkJyksXG4gICAgICAgICAgYm9keSxcbiAgICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgICBEaWFsb2cuY2FuY2VsQnV0dG9uKCksXG4gICAgICAgICAgICBEaWFsb2cub2tCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0J1aWxkJykgfSlcbiAgICAgICAgICBdXG4gICAgICAgIH0pLnRoZW4ocmVzdWx0ID0+IChyZXN1bHQuYnV0dG9uLmFjY2VwdCA/IGJ1aWxkKCkgOiB1bmRlZmluZWQpKTtcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gdXBkYXRlVHJlZVBhdGg7XG4gIH0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuLyoqXG4gKiBQbHVnaW4gdG8gYnVpbGQgdGhlIGNvbnRleHQgbWVudSBmcm9tIHRoZSBzZXR0aW5ncy5cbiAqL1xuY29uc3QgY29udGV4dE1lbnVQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246Y29udGV4dC1tZW51JyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lTZXR0aW5nUmVnaXN0cnksIElUcmFuc2xhdG9yXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKTogdm9pZCA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIGZ1bmN0aW9uIGNyZWF0ZU1lbnUob3B0aW9uczogSVNldHRpbmdSZWdpc3RyeS5JTWVudSk6IFJhbmtlZE1lbnUge1xuICAgICAgY29uc3QgbWVudSA9IG5ldyBSYW5rZWRNZW51KHsgLi4ub3B0aW9ucywgY29tbWFuZHM6IGFwcC5jb21tYW5kcyB9KTtcbiAgICAgIGlmIChvcHRpb25zLmxhYmVsKSB7XG4gICAgICAgIG1lbnUudGl0bGUubGFiZWwgPSB0cmFucy5fXyhvcHRpb25zLmxhYmVsKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBtZW51O1xuICAgIH1cblxuICAgIC8vIExvYWQgdGhlIGNvbnRleHQgbWVudSBsYXRlbHkgc28gcGx1Z2lucyBhcmUgbG9hZGVkLlxuICAgIGFwcC5zdGFydGVkXG4gICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgIHJldHVybiBQcml2YXRlLmxvYWRTZXR0aW5nc0NvbnRleHRNZW51KFxuICAgICAgICAgIGFwcC5jb250ZXh0TWVudSxcbiAgICAgICAgICBzZXR0aW5nUmVnaXN0cnksXG4gICAgICAgICAgY3JlYXRlTWVudSxcbiAgICAgICAgICB0cmFuc2xhdG9yXG4gICAgICAgICk7XG4gICAgICB9KVxuICAgICAgLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgIGNvbnNvbGUuZXJyb3IoXG4gICAgICAgICAgJ0ZhaWxlZCB0byBsb2FkIGNvbnRleHQgbWVudSBpdGVtcyBmcm9tIHNldHRpbmdzIHJlZ2lzdHJ5LicsXG4gICAgICAgICAgcmVhc29uXG4gICAgICAgICk7XG4gICAgICB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBDaGVjayBpZiB0aGUgYXBwbGljYXRpb24gaXMgZGlydHkgYmVmb3JlIGNsb3NpbmcgdGhlIGJyb3dzZXIgdGFiLlxuICovXG5jb25zdCBkaXJ0eTogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpkaXJ0eScsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQsIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yKTogdm9pZCA9PiB7XG4gICAgaWYgKCEoYXBwIGluc3RhbmNlb2YgSnVweXRlckxhYikpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgJHtkaXJ0eS5pZH0gbXVzdCBiZSBhY3RpdmF0ZWQgaW4gSnVweXRlckxhYi5gKTtcbiAgICB9XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBtZXNzYWdlID0gdHJhbnMuX18oXG4gICAgICAnQXJlIHlvdSBzdXJlIHlvdSB3YW50IHRvIGV4aXQgSnVweXRlckxhYj9cXG5cXG5BbnkgdW5zYXZlZCBjaGFuZ2VzIHdpbGwgYmUgbG9zdC4nXG4gICAgKTtcblxuICAgIC8vIFRoZSBzcGVjIGZvciB0aGUgYGJlZm9yZXVubG9hZGAgZXZlbnQgaXMgaW1wbGVtZW50ZWQgZGlmZmVyZW50bHkgYnlcbiAgICAvLyB0aGUgZGlmZmVyZW50IGJyb3dzZXIgdmVuZG9ycy4gQ29uc2VxdWVudGx5LCB0aGUgYGV2ZW50LnJldHVyblZhbHVlYFxuICAgIC8vIGF0dHJpYnV0ZSBuZWVkcyB0byBzZXQgaW4gYWRkaXRpb24gdG8gYSByZXR1cm4gdmFsdWUgYmVpbmcgcmV0dXJuZWQuXG4gICAgLy8gRm9yIG1vcmUgaW5mb3JtYXRpb24sIHNlZTpcbiAgICAvLyBodHRwczovL2RldmVsb3Blci5tb3ppbGxhLm9yZy9lbi9kb2NzL1dlYi9FdmVudHMvYmVmb3JldW5sb2FkXG4gICAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ2JlZm9yZXVubG9hZCcsIGV2ZW50ID0+IHtcbiAgICAgIGlmIChhcHAuc3RhdHVzLmlzRGlydHkpIHtcbiAgICAgICAgcmV0dXJuICgoZXZlbnQgYXMgYW55KS5yZXR1cm5WYWx1ZSA9IG1lc3NhZ2UpO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGxheW91dCByZXN0b3JlciBwcm92aWRlci5cbiAqL1xuY29uc3QgbGF5b3V0OiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUxheW91dFJlc3RvcmVyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246bGF5b3V0JyxcbiAgcmVxdWlyZXM6IFtJU3RhdGVEQiwgSUxhYlNoZWxsLCBJU2V0dGluZ1JlZ2lzdHJ5LCBJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgc3RhdGU6IElTdGF0ZURCLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwsXG4gICAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICkgPT4ge1xuICAgIGNvbnN0IGZpcnN0ID0gYXBwLnN0YXJ0ZWQ7XG4gICAgY29uc3QgcmVnaXN0cnkgPSBhcHAuY29tbWFuZHM7XG4gICAgY29uc3QgcmVzdG9yZXIgPSBuZXcgTGF5b3V0UmVzdG9yZXIoeyBjb25uZWN0b3I6IHN0YXRlLCBmaXJzdCwgcmVnaXN0cnkgfSk7XG5cbiAgICB2b2lkIHJlc3RvcmVyLmZldGNoKCkudGhlbihzYXZlZCA9PiB7XG4gICAgICBsYWJTaGVsbC5yZXN0b3JlTGF5b3V0KFxuICAgICAgICBQYWdlQ29uZmlnLmdldE9wdGlvbignbW9kZScpIGFzIERvY2tQYW5lbC5Nb2RlLFxuICAgICAgICBzYXZlZFxuICAgICAgKTtcbiAgICAgIGxhYlNoZWxsLmxheW91dE1vZGlmaWVkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICB2b2lkIHJlc3RvcmVyLnNhdmUobGFiU2hlbGwuc2F2ZUxheW91dCgpKTtcbiAgICAgIH0pO1xuICAgICAgUHJpdmF0ZS5hY3RpdmF0ZVNpZGViYXJTd2l0Y2hlcihcbiAgICAgICAgYXBwLFxuICAgICAgICBsYWJTaGVsbCxcbiAgICAgICAgc2V0dGluZ1JlZ2lzdHJ5LFxuICAgICAgICB0cmFuc2xhdG9yLFxuICAgICAgICBzYXZlZFxuICAgICAgKTtcbiAgICB9KTtcblxuICAgIHJldHVybiByZXN0b3JlcjtcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSUxheW91dFJlc3RvcmVyXG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IFVSTCByb3V0ZXIgcHJvdmlkZXIuXG4gKi9cbmNvbnN0IHJvdXRlcjogSnVweXRlckZyb250RW5kUGx1Z2luPElSb3V0ZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpyb3V0ZXInLFxuICByZXF1aXJlczogW0p1cHl0ZXJGcm9udEVuZC5JUGF0aHNdLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kLCBwYXRoczogSnVweXRlckZyb250RW5kLklQYXRocykgPT4ge1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb25zdCBiYXNlID0gcGF0aHMudXJscy5iYXNlO1xuICAgIGNvbnN0IHJvdXRlciA9IG5ldyBSb3V0ZXIoeyBiYXNlLCBjb21tYW5kcyB9KTtcblxuICAgIHZvaWQgYXBwLnN0YXJ0ZWQudGhlbigoKSA9PiB7XG4gICAgICAvLyBSb3V0ZSB0aGUgdmVyeSBmaXJzdCByZXF1ZXN0IG9uIGxvYWQuXG4gICAgICB2b2lkIHJvdXRlci5yb3V0ZSgpO1xuXG4gICAgICAvLyBSb3V0ZSBhbGwgcG9wIHN0YXRlIGV2ZW50cy5cbiAgICAgIHdpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdwb3BzdGF0ZScsICgpID0+IHtcbiAgICAgICAgdm9pZCByb3V0ZXIucm91dGUoKTtcbiAgICAgIH0pO1xuICAgIH0pO1xuXG4gICAgcmV0dXJuIHJvdXRlcjtcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSVJvdXRlclxufTtcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCB0cmVlIHJvdXRlIHJlc29sdmVyIHBsdWdpbi5cbiAqL1xuY29uc3QgdHJlZTogSnVweXRlckZyb250RW5kUGx1Z2luPEp1cHl0ZXJGcm9udEVuZC5JVHJlZVJlc29sdmVyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246dHJlZS1yZXNvbHZlcicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJUm91dGVyXSxcbiAgcHJvdmlkZXM6IEp1cHl0ZXJGcm9udEVuZC5JVHJlZVJlc29sdmVyLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHJvdXRlcjogSVJvdXRlclxuICApOiBKdXB5dGVyRnJvbnRFbmQuSVRyZWVSZXNvbHZlciA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IHNldCA9IG5ldyBEaXNwb3NhYmxlU2V0KCk7XG4gICAgY29uc3QgZGVsZWdhdGUgPSBuZXcgUHJvbWlzZURlbGVnYXRlPEp1cHl0ZXJGcm9udEVuZC5JVHJlZVJlc29sdmVyLlBhdGhzPigpO1xuXG4gICAgY29uc3QgdHJlZVBhdHRlcm4gPSBuZXcgUmVnRXhwKFxuICAgICAgJy8obGFifGRvYykoL3dvcmtzcGFjZXMvW2EtekEtWjAtOS1fXSspPygvdHJlZS8uKik/J1xuICAgICk7XG5cbiAgICBzZXQuYWRkKFxuICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRyZWUsIHtcbiAgICAgICAgZXhlY3V0ZTogYXN5bmMgKGFyZ3M6IElSb3V0ZXIuSUxvY2F0aW9uKSA9PiB7XG4gICAgICAgICAgaWYgKHNldC5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgY29uc3QgcXVlcnkgPSBVUkxFeHQucXVlcnlTdHJpbmdUb09iamVjdChhcmdzLnNlYXJjaCA/PyAnJyk7XG4gICAgICAgICAgY29uc3QgYnJvd3NlciA9IHF1ZXJ5WydmaWxlLWJyb3dzZXItcGF0aCddIHx8ICcnO1xuXG4gICAgICAgICAgLy8gUmVtb3ZlIHRoZSBmaWxlIGJyb3dzZXIgcGF0aCBmcm9tIHRoZSBxdWVyeSBzdHJpbmcuXG4gICAgICAgICAgZGVsZXRlIHF1ZXJ5WydmaWxlLWJyb3dzZXItcGF0aCddO1xuXG4gICAgICAgICAgLy8gQ2xlYW4gdXAgYXJ0aWZhY3RzIGltbWVkaWF0ZWx5IHVwb24gcm91dGluZy5cbiAgICAgICAgICBzZXQuZGlzcG9zZSgpO1xuXG4gICAgICAgICAgZGVsZWdhdGUucmVzb2x2ZSh7IGJyb3dzZXIsIGZpbGU6IFBhZ2VDb25maWcuZ2V0T3B0aW9uKCd0cmVlUGF0aCcpIH0pO1xuICAgICAgICB9XG4gICAgICB9KVxuICAgICk7XG4gICAgc2V0LmFkZChcbiAgICAgIHJvdXRlci5yZWdpc3Rlcih7IGNvbW1hbmQ6IENvbW1hbmRJRHMudHJlZSwgcGF0dGVybjogdHJlZVBhdHRlcm4gfSlcbiAgICApO1xuXG4gICAgLy8gSWYgYSByb3V0ZSBpcyBoYW5kbGVkIGJ5IHRoZSByb3V0ZXIgd2l0aG91dCB0aGUgdHJlZSBjb21tYW5kIGJlaW5nXG4gICAgLy8gaW52b2tlZCwgcmVzb2x2ZSB0byBgbnVsbGAgYW5kIGNsZWFuIHVwIGFydGlmYWN0cy5cbiAgICBjb25zdCBsaXN0ZW5lciA9ICgpID0+IHtcbiAgICAgIGlmIChzZXQuaXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBzZXQuZGlzcG9zZSgpO1xuICAgICAgZGVsZWdhdGUucmVzb2x2ZShudWxsKTtcbiAgICB9O1xuICAgIHJvdXRlci5yb3V0ZWQuY29ubmVjdChsaXN0ZW5lcik7XG4gICAgc2V0LmFkZChcbiAgICAgIG5ldyBEaXNwb3NhYmxlRGVsZWdhdGUoKCkgPT4ge1xuICAgICAgICByb3V0ZXIucm91dGVkLmRpc2Nvbm5lY3QobGlzdGVuZXIpO1xuICAgICAgfSlcbiAgICApO1xuXG4gICAgcmV0dXJuIHsgcGF0aHM6IGRlbGVnYXRlLnByb21pc2UgfTtcbiAgfVxufTtcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBVUkwgbm90IGZvdW5kIGV4dGVuc2lvbi5cbiAqL1xuY29uc3Qgbm90Zm91bmQ6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246bm90Zm91bmQnLFxuICByZXF1aXJlczogW0p1cHl0ZXJGcm9udEVuZC5JUGF0aHMsIElSb3V0ZXIsIElUcmFuc2xhdG9yXSxcbiAgYWN0aXZhdGU6IChcbiAgICBfOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgcGF0aHM6IEp1cHl0ZXJGcm9udEVuZC5JUGF0aHMsXG4gICAgcm91dGVyOiBJUm91dGVyLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICkgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgYmFkID0gcGF0aHMudXJscy5ub3RGb3VuZDtcblxuICAgIGlmICghYmFkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3QgYmFzZSA9IHJvdXRlci5iYXNlO1xuICAgIGNvbnN0IG1lc3NhZ2UgPSB0cmFucy5fXyhcbiAgICAgICdUaGUgcGF0aDogJTEgd2FzIG5vdCBmb3VuZC4gSnVweXRlckxhYiByZWRpcmVjdGVkIHRvOiAlMicsXG4gICAgICBiYWQsXG4gICAgICBiYXNlXG4gICAgKTtcblxuICAgIC8vIENoYW5nZSB0aGUgVVJMIGJhY2sgdG8gdGhlIGJhc2UgYXBwbGljYXRpb24gVVJMLlxuICAgIHJvdXRlci5uYXZpZ2F0ZSgnJyk7XG5cbiAgICB2b2lkIHNob3dFcnJvck1lc3NhZ2UodHJhbnMuX18oJ1BhdGggTm90IEZvdW5kJyksIHsgbWVzc2FnZSB9KTtcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIENoYW5nZSB0aGUgZmF2aWNvbiBjaGFuZ2luZyBiYXNlZCBvbiB0aGUgYnVzeSBzdGF0dXM7XG4gKi9cbmNvbnN0IGJ1c3k6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246ZmF2aWNvbmJ1c3knLFxuICByZXF1aXJlczogW0lMYWJTdGF0dXNdLFxuICBhY3RpdmF0ZTogYXN5bmMgKF86IEp1cHl0ZXJGcm9udEVuZCwgc3RhdHVzOiBJTGFiU3RhdHVzKSA9PiB7XG4gICAgc3RhdHVzLmJ1c3lTaWduYWwuY29ubmVjdCgoXywgaXNCdXN5KSA9PiB7XG4gICAgICBjb25zdCBmYXZpY29uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAgICAgYGxpbmtbcmVsPVwiaWNvblwiXSR7aXNCdXN5ID8gJy5pZGxlLmZhdmljb24nIDogJy5idXN5LmZhdmljb24nfWBcbiAgICAgICkgYXMgSFRNTExpbmtFbGVtZW50O1xuICAgICAgaWYgKCFmYXZpY29uKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IG5ld0Zhdmljb24gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICAgICBgbGluayR7aXNCdXN5ID8gJy5idXN5LmZhdmljb24nIDogJy5pZGxlLmZhdmljb24nfWBcbiAgICAgICkgYXMgSFRNTExpbmtFbGVtZW50O1xuICAgICAgaWYgKCFuZXdGYXZpY29uKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIC8vIElmIHdlIGhhdmUgdGhlIHR3byBpY29ucyB3aXRoIHRoZSBzcGVjaWFsIGNsYXNzZXMsIHRoZW4gdG9nZ2xlIHRoZW0uXG4gICAgICBpZiAoZmF2aWNvbiAhPT0gbmV3RmF2aWNvbikge1xuICAgICAgICBmYXZpY29uLnJlbCA9ICcnO1xuICAgICAgICBuZXdGYXZpY29uLnJlbCA9ICdpY29uJztcblxuICAgICAgICAvLyBGaXJlZm94IGRvZXNuJ3Qgc2VlbSB0byByZWNvZ25pemUganVzdCBjaGFuZ2luZyByZWwsIHNvIHdlIGFsc29cbiAgICAgICAgLy8gcmVpbnNlcnQgdGhlIGxpbmsgaW50byB0aGUgRE9NLlxuICAgICAgICBuZXdGYXZpY29uLnBhcmVudE5vZGUhLnJlcGxhY2VDaGlsZChuZXdGYXZpY29uLCBuZXdGYXZpY29uKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IEp1cHl0ZXJMYWIgYXBwbGljYXRpb24gc2hlbGwuXG4gKi9cbmNvbnN0IHNoZWxsOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUxhYlNoZWxsPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246c2hlbGwnLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kKSA9PiB7XG4gICAgaWYgKCEoYXBwLnNoZWxsIGluc3RhbmNlb2YgTGFiU2hlbGwpKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYCR7c2hlbGwuaWR9IGRpZCBub3QgZmluZCBhIExhYlNoZWxsIGluc3RhbmNlLmApO1xuICAgIH1cbiAgICByZXR1cm4gYXBwLnNoZWxsO1xuICB9LFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJTGFiU2hlbGxcbn07XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgSnVweXRlckxhYiBhcHBsaWNhdGlvbiBzdGF0dXMgcHJvdmlkZXIuXG4gKi9cbmNvbnN0IHN0YXR1czogSnVweXRlckZyb250RW5kUGx1Z2luPElMYWJTdGF0dXM+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpzdGF0dXMnLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kKSA9PiB7XG4gICAgaWYgKCEoYXBwIGluc3RhbmNlb2YgSnVweXRlckxhYikpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgJHtzdGF0dXMuaWR9IG11c3QgYmUgYWN0aXZhdGVkIGluIEp1cHl0ZXJMYWIuYCk7XG4gICAgfVxuICAgIHJldHVybiBhcHAuc3RhdHVzO1xuICB9LFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJTGFiU3RhdHVzXG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IEp1cHl0ZXJMYWIgYXBwbGljYXRpb24tc3BlY2lmaWMgaW5mb3JtYXRpb24gcHJvdmlkZXIuXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhpcyBwbHVnaW4gc2hvdWxkIG9ubHkgYmUgdXNlZCBieSBwbHVnaW5zIHRoYXQgc3BlY2lmaWNhbGx5IG5lZWQgdG8gYWNjZXNzXG4gKiBKdXB5dGVyTGFiIGFwcGxpY2F0aW9uIGluZm9ybWF0aW9uLCBlLmcuLCBsaXN0aW5nIGV4dGVuc2lvbnMgdGhhdCBoYXZlIGJlZW5cbiAqIGxvYWRlZCBvciBkZWZlcnJlZCB3aXRoaW4gSnVweXRlckxhYi5cbiAqL1xuY29uc3QgaW5mbzogSnVweXRlckZyb250RW5kUGx1Z2luPEp1cHl0ZXJMYWIuSUluZm8+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjppbmZvJyxcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZCkgPT4ge1xuICAgIGlmICghKGFwcCBpbnN0YW5jZW9mIEp1cHl0ZXJMYWIpKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYCR7aW5mby5pZH0gbXVzdCBiZSBhY3RpdmF0ZWQgaW4gSnVweXRlckxhYi5gKTtcbiAgICB9XG4gICAgcmV0dXJuIGFwcC5pbmZvO1xuICB9LFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBKdXB5dGVyTGFiLklJbmZvXG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IEp1cHl0ZXJMYWIgcGF0aHMgZGljdGlvbmFyeSBwcm92aWRlci5cbiAqL1xuY29uc3QgcGF0aHM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxKdXB5dGVyRnJvbnRFbmQuSVBhdGhzPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHB1dGlscy1leHRlbnNpb246cGF0aHMnLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kKTogSnVweXRlckZyb250RW5kLklQYXRocyA9PiB7XG4gICAgaWYgKCEoYXBwIGluc3RhbmNlb2YgSnVweXRlckxhYikpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgJHtwYXRocy5pZH0gbXVzdCBiZSBhY3RpdmF0ZWQgaW4gSnVweXRlckxhYi5gKTtcbiAgICB9XG4gICAgcmV0dXJuIGFwcC5wYXRocztcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSnVweXRlckZyb250RW5kLklQYXRoc1xufTtcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBwcm9wZXJ0eSBpbnNwZWN0b3IgcHJvdmlkZXIuXG4gKi9cbmNvbnN0IHByb3BlcnR5SW5zcGVjdG9yOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SVByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpwcm9wZXJ0eS1pbnNwZWN0b3InLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSUxhYlNoZWxsLCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUxheW91dFJlc3RvcmVyXSxcbiAgcHJvdmlkZXM6IElQcm9wZXJ0eUluc3BlY3RvclByb3ZpZGVyLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIGxhYnNoZWxsOiBJTGFiU2hlbGwsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCB3aWRnZXQgPSBuZXcgU2lkZUJhclByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXIoXG4gICAgICBsYWJzaGVsbCxcbiAgICAgIHVuZGVmaW5lZCxcbiAgICAgIHRyYW5zbGF0b3JcbiAgICApO1xuICAgIHdpZGdldC50aXRsZS5pY29uID0gYnVpbGRJY29uO1xuICAgIHdpZGdldC50aXRsZS5jYXB0aW9uID0gdHJhbnMuX18oJ1Byb3BlcnR5IEluc3BlY3RvcicpO1xuICAgIHdpZGdldC5pZCA9ICdqcC1wcm9wZXJ0eS1pbnNwZWN0b3InO1xuICAgIGxhYnNoZWxsLmFkZCh3aWRnZXQsICdyaWdodCcsIHsgcmFuazogMTAwIH0pO1xuICAgIGlmIChyZXN0b3Jlcikge1xuICAgICAgcmVzdG9yZXIuYWRkKHdpZGdldCwgJ2pwLXByb3BlcnR5LWluc3BlY3RvcicpO1xuICAgIH1cbiAgICByZXR1cm4gd2lkZ2V0O1xuICB9XG59O1xuXG5jb25zdCBKdXB5dGVyTG9nbzogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpsb2dvJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lMYWJTaGVsbF0sXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQsIHNoZWxsOiBJTGFiU2hlbGwpID0+IHtcbiAgICBjb25zdCBsb2dvID0gbmV3IFdpZGdldCgpO1xuICAgIGp1cHl0ZXJJY29uLmVsZW1lbnQoe1xuICAgICAgY29udGFpbmVyOiBsb2dvLm5vZGUsXG4gICAgICBlbGVtZW50UG9zaXRpb246ICdjZW50ZXInLFxuICAgICAgbWFyZ2luOiAnMHB4JywgLy8g5paw5biD5bGAbG9nbyDkv67mlLlcbiAgICAgIGhlaWdodDogJ2F1dG8nLFxuICAgICAgd2lkdGg6ICcxMjBweCdcbiAgICB9KTtcbiAgICBsb2dvLmlkID0gJ2pwLU1haW5Mb2dvJztcbiAgICBzaGVsbC5hZGQobG9nbywgJ3RvcCcsIHsgcmFuazogMCB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbnMgYXMgZGVmYXVsdC5cbiAqL1xuY29uc3QgcGx1Z2luczogSnVweXRlckZyb250RW5kUGx1Z2luPGFueT5bXSA9IFtcbiAgY29udGV4dE1lbnVQbHVnaW4sXG4gIGRpcnR5LFxuICBtYWluLFxuICBtYWluQ29tbWFuZHMsXG4gIGxheW91dCxcbiAgcm91dGVyLFxuICB0cmVlLFxuICBub3Rmb3VuZCxcbiAgYnVzeSxcbiAgc2hlbGwsXG4gIHN0YXR1cyxcbiAgaW5mbyxcbiAgcGF0aHMsXG4gIHByb3BlcnR5SW5zcGVjdG9yLFxuICBKdXB5dGVyTG9nb1xuXTtcblxuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcblxubmFtZXNwYWNlIFByaXZhdGUge1xuICB0eXBlIFNpZGViYXJPdmVycmlkZXMgPSB7IFtpZDogc3RyaW5nXTogJ2xlZnQnIHwgJ3JpZ2h0JyB9O1xuXG4gIGFzeW5jIGZ1bmN0aW9uIGRpc3BsYXlJbmZvcm1hdGlvbih0cmFuczogVHJhbnNsYXRpb25CdW5kbGUpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCByZXN1bHQgPSBhd2FpdCBzaG93RGlhbG9nKHtcbiAgICAgIHRpdGxlOiB0cmFucy5fXygnSW5mb3JtYXRpb24nKSxcbiAgICAgIGJvZHk6IHRyYW5zLl9fKFxuICAgICAgICAnQ29udGV4dCBtZW51IGN1c3RvbWl6YXRpb24gaGFzIGNoYW5nZWQuIFlvdSB3aWxsIG5lZWQgdG8gcmVsb2FkIEp1cHl0ZXJMYWIgdG8gc2VlIHRoZSBjaGFuZ2VzLidcbiAgICAgICksXG4gICAgICBidXR0b25zOiBbXG4gICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oKSxcbiAgICAgICAgRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdSZWxvYWQnKSB9KVxuICAgICAgXVxuICAgIH0pO1xuXG4gICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICBsb2NhdGlvbi5yZWxvYWQoKTtcbiAgICB9XG4gIH1cblxuICBleHBvcnQgYXN5bmMgZnVuY3Rpb24gbG9hZFNldHRpbmdzQ29udGV4dE1lbnUoXG4gICAgY29udGV4dE1lbnU6IENvbnRleHRNZW51U3ZnLFxuICAgIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIG1lbnVGYWN0b3J5OiAob3B0aW9uczogSVNldHRpbmdSZWdpc3RyeS5JTWVudSkgPT4gUmFua2VkTWVudSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHBsdWdpbklkID0gY29udGV4dE1lbnVQbHVnaW4uaWQ7XG4gICAgbGV0IGNhbm9uaWNhbDogSVNldHRpbmdSZWdpc3RyeS5JU2NoZW1hIHwgbnVsbDtcbiAgICBsZXQgbG9hZGVkOiB7IFtuYW1lOiBzdHJpbmddOiBJU2V0dGluZ1JlZ2lzdHJ5LklDb250ZXh0TWVudUl0ZW1bXSB9ID0ge307XG5cbiAgICAvKipcbiAgICAgKiBQb3B1bGF0ZSB0aGUgcGx1Z2luJ3Mgc2NoZW1hIGRlZmF1bHRzLlxuICAgICAqXG4gICAgICogV2Uga2VlcCB0cmFjayBvZiBkaXNhYmxlZCBlbnRyaWVzIGluIGNhc2UgdGhlIHBsdWdpbiBpcyBsb2FkZWRcbiAgICAgKiBhZnRlciB0aGUgbWVudSBpbml0aWFsaXphdGlvbi5cbiAgICAgKi9cbiAgICBmdW5jdGlvbiBwb3B1bGF0ZShzY2hlbWE6IElTZXR0aW5nUmVnaXN0cnkuSVNjaGVtYSkge1xuICAgICAgbG9hZGVkID0ge307XG4gICAgICBjb25zdCBwbHVnaW5EZWZhdWx0cyA9IE9iamVjdC5rZXlzKHJlZ2lzdHJ5LnBsdWdpbnMpXG4gICAgICAgIC5tYXAocGx1Z2luID0+IHtcbiAgICAgICAgICBjb25zdCBpdGVtcyA9XG4gICAgICAgICAgICByZWdpc3RyeS5wbHVnaW5zW3BsdWdpbl0hLnNjaGVtYVsnanVweXRlci5sYWIubWVudXMnXT8uY29udGV4dCA/P1xuICAgICAgICAgICAgW107XG4gICAgICAgICAgbG9hZGVkW3BsdWdpbl0gPSBpdGVtcztcbiAgICAgICAgICByZXR1cm4gaXRlbXM7XG4gICAgICAgIH0pXG4gICAgICAgIC5jb25jYXQoW3NjaGVtYVsnanVweXRlci5sYWIubWVudXMnXT8uY29udGV4dCA/PyBbXV0pXG4gICAgICAgIC5yZWR1Y2VSaWdodChcbiAgICAgICAgICAoXG4gICAgICAgICAgICBhY2M6IElTZXR0aW5nUmVnaXN0cnkuSUNvbnRleHRNZW51SXRlbVtdLFxuICAgICAgICAgICAgdmFsOiBJU2V0dGluZ1JlZ2lzdHJ5LklDb250ZXh0TWVudUl0ZW1bXVxuICAgICAgICAgICkgPT4gU2V0dGluZ1JlZ2lzdHJ5LnJlY29uY2lsZUl0ZW1zKGFjYywgdmFsLCB0cnVlKSxcbiAgICAgICAgICBbXVxuICAgICAgICApITtcblxuICAgICAgLy8gQXBwbHkgZGVmYXVsdCB2YWx1ZSBhcyBsYXN0IHN0ZXAgdG8gdGFrZSBpbnRvIGFjY291bnQgb3ZlcnJpZGVzLmpzb25cbiAgICAgIC8vIFRoZSBzdGFuZGFyZCBkZWZhdWx0IGJlaW5nIFtdIGFzIHRoZSBwbHVnaW4gbXVzdCB1c2UgYGp1cHl0ZXIubGFiLm1lbnVzLmNvbnRleHRgXG4gICAgICAvLyB0byBkZWZpbmUgdGhlaXIgZGVmYXVsdCB2YWx1ZS5cbiAgICAgIHNjaGVtYS5wcm9wZXJ0aWVzIS5jb250ZXh0TWVudS5kZWZhdWx0ID0gU2V0dGluZ1JlZ2lzdHJ5LnJlY29uY2lsZUl0ZW1zKFxuICAgICAgICBwbHVnaW5EZWZhdWx0cyxcbiAgICAgICAgc2NoZW1hLnByb3BlcnRpZXMhLmNvbnRleHRNZW51LmRlZmF1bHQgYXMgYW55W10sXG4gICAgICAgIHRydWVcbiAgICAgICkhXG4gICAgICAgIC8vIGZsYXR0ZW4gb25lIGxldmVsXG4gICAgICAgIC5zb3J0KChhLCBiKSA9PiAoYS5yYW5rID8/IEluZmluaXR5KSAtIChiLnJhbmsgPz8gSW5maW5pdHkpKTtcbiAgICB9XG5cbiAgICAvLyBUcmFuc2Zvcm0gdGhlIHBsdWdpbiBvYmplY3QgdG8gcmV0dXJuIGRpZmZlcmVudCBzY2hlbWEgdGhhbiB0aGUgZGVmYXVsdC5cbiAgICByZWdpc3RyeS50cmFuc2Zvcm0ocGx1Z2luSWQsIHtcbiAgICAgIGNvbXBvc2U6IHBsdWdpbiA9PiB7XG4gICAgICAgIC8vIE9ubHkgb3ZlcnJpZGUgdGhlIGNhbm9uaWNhbCBzY2hlbWEgdGhlIGZpcnN0IHRpbWUuXG4gICAgICAgIGlmICghY2Fub25pY2FsKSB7XG4gICAgICAgICAgY2Fub25pY2FsID0gSlNPTkV4dC5kZWVwQ29weShwbHVnaW4uc2NoZW1hKTtcbiAgICAgICAgICBwb3B1bGF0ZShjYW5vbmljYWwpO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgZGVmYXVsdHMgPSBjYW5vbmljYWwucHJvcGVydGllcz8uY29udGV4dE1lbnU/LmRlZmF1bHQgPz8gW107XG4gICAgICAgIGNvbnN0IHVzZXIgPSB7XG4gICAgICAgICAgY29udGV4dE1lbnU6IHBsdWdpbi5kYXRhLnVzZXIuY29udGV4dE1lbnUgPz8gW11cbiAgICAgICAgfTtcbiAgICAgICAgY29uc3QgY29tcG9zaXRlID0ge1xuICAgICAgICAgIGNvbnRleHRNZW51OiBTZXR0aW5nUmVnaXN0cnkucmVjb25jaWxlSXRlbXMoXG4gICAgICAgICAgICBkZWZhdWx0cyBhcyBJU2V0dGluZ1JlZ2lzdHJ5LklDb250ZXh0TWVudUl0ZW1bXSxcbiAgICAgICAgICAgIHVzZXIuY29udGV4dE1lbnUgYXMgSVNldHRpbmdSZWdpc3RyeS5JQ29udGV4dE1lbnVJdGVtW10sXG4gICAgICAgICAgICBmYWxzZVxuICAgICAgICAgIClcbiAgICAgICAgfTtcblxuICAgICAgICBwbHVnaW4uZGF0YSA9IHsgY29tcG9zaXRlLCB1c2VyIH07XG5cbiAgICAgICAgcmV0dXJuIHBsdWdpbjtcbiAgICAgIH0sXG4gICAgICBmZXRjaDogcGx1Z2luID0+IHtcbiAgICAgICAgLy8gT25seSBvdmVycmlkZSB0aGUgY2Fub25pY2FsIHNjaGVtYSB0aGUgZmlyc3QgdGltZS5cbiAgICAgICAgaWYgKCFjYW5vbmljYWwpIHtcbiAgICAgICAgICBjYW5vbmljYWwgPSBKU09ORXh0LmRlZXBDb3B5KHBsdWdpbi5zY2hlbWEpO1xuICAgICAgICAgIHBvcHVsYXRlKGNhbm9uaWNhbCk7XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIGRhdGE6IHBsdWdpbi5kYXRhLFxuICAgICAgICAgIGlkOiBwbHVnaW4uaWQsXG4gICAgICAgICAgcmF3OiBwbHVnaW4ucmF3LFxuICAgICAgICAgIHNjaGVtYTogY2Fub25pY2FsLFxuICAgICAgICAgIHZlcnNpb246IHBsdWdpbi52ZXJzaW9uXG4gICAgICAgIH07XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBSZXBvcHVsYXRlIHRoZSBjYW5vbmljYWwgdmFyaWFibGUgYWZ0ZXIgdGhlIHNldHRpbmcgcmVnaXN0cnkgaGFzXG4gICAgLy8gcHJlbG9hZGVkIGFsbCBpbml0aWFsIHBsdWdpbnMuXG4gICAgY2Fub25pY2FsID0gbnVsbDtcblxuICAgIGNvbnN0IHNldHRpbmdzID0gYXdhaXQgcmVnaXN0cnkubG9hZChwbHVnaW5JZCk7XG5cbiAgICBjb25zdCBjb250ZXh0SXRlbXM6IElTZXR0aW5nUmVnaXN0cnkuSUNvbnRleHRNZW51SXRlbVtdID1cbiAgICAgIChzZXR0aW5ncy5jb21wb3NpdGUuY29udGV4dE1lbnUgYXMgYW55KSA/PyBbXTtcblxuICAgIC8vIENyZWF0ZSBtZW51IGl0ZW0gZm9yIG5vbi1kaXNhYmxlZCBlbGVtZW50XG4gICAgU2V0dGluZ1JlZ2lzdHJ5LmZpbHRlckRpc2FibGVkSXRlbXMoY29udGV4dEl0ZW1zKS5mb3JFYWNoKGl0ZW0gPT4ge1xuICAgICAgTWVudUZhY3RvcnkuYWRkQ29udGV4dEl0ZW0oXG4gICAgICAgIHtcbiAgICAgICAgICAvLyBXZSBoYXZlIHRvIHNldCB0aGUgZGVmYXVsdCByYW5rIGJlY2F1c2UgTHVtaW5vIGlzIHNvcnRpbmcgdGhlIHZpc2libGUgaXRlbXNcbiAgICAgICAgICByYW5rOiBERUZBVUxUX0NPTlRFWFRfSVRFTV9SQU5LLFxuICAgICAgICAgIC4uLml0ZW1cbiAgICAgICAgfSxcbiAgICAgICAgY29udGV4dE1lbnUsXG4gICAgICAgIG1lbnVGYWN0b3J5XG4gICAgICApO1xuICAgIH0pO1xuXG4gICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIC8vIEFzIGV4dGVuc2lvbiBtYXkgY2hhbmdlIHRoZSBjb250ZXh0IG1lbnUgdGhyb3VnaCBBUEksXG4gICAgICAvLyBwcm9tcHQgdGhlIHVzZXIgdG8gcmVsb2FkIGlmIHRoZSBtZW51IGhhcyBiZWVuIHVwZGF0ZWQuXG4gICAgICBjb25zdCBuZXdJdGVtcyA9IChzZXR0aW5ncy5jb21wb3NpdGUuY29udGV4dE1lbnUgYXMgYW55KSA/PyBbXTtcbiAgICAgIGlmICghSlNPTkV4dC5kZWVwRXF1YWwoY29udGV4dEl0ZW1zLCBuZXdJdGVtcykpIHtcbiAgICAgICAgdm9pZCBkaXNwbGF5SW5mb3JtYXRpb24odHJhbnMpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgcmVnaXN0cnkucGx1Z2luQ2hhbmdlZC5jb25uZWN0KGFzeW5jIChzZW5kZXIsIHBsdWdpbikgPT4ge1xuICAgICAgaWYgKHBsdWdpbiAhPT0gcGx1Z2luSWQpIHtcbiAgICAgICAgLy8gSWYgdGhlIHBsdWdpbiBjaGFuZ2VkIGl0cyBtZW51LlxuICAgICAgICBjb25zdCBvbGRJdGVtcyA9IGxvYWRlZFtwbHVnaW5dID8/IFtdO1xuICAgICAgICBjb25zdCBuZXdJdGVtcyA9XG4gICAgICAgICAgcmVnaXN0cnkucGx1Z2luc1twbHVnaW5dIS5zY2hlbWFbJ2p1cHl0ZXIubGFiLm1lbnVzJ10/LmNvbnRleHQgPz8gW107XG4gICAgICAgIGlmICghSlNPTkV4dC5kZWVwRXF1YWwob2xkSXRlbXMsIG5ld0l0ZW1zKSkge1xuICAgICAgICAgIGlmIChsb2FkZWRbcGx1Z2luXSkge1xuICAgICAgICAgICAgLy8gVGhlIHBsdWdpbiBoYXMgY2hhbmdlZCwgcmVxdWVzdCB0aGUgdXNlciB0byByZWxvYWQgdGhlIFVJXG4gICAgICAgICAgICBhd2FpdCBkaXNwbGF5SW5mb3JtYXRpb24odHJhbnMpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAvLyBUaGUgcGx1Z2luIHdhcyBub3QgeWV0IGxvYWRlZCB3aGVuIHRoZSBtZW51IHdhcyBidWlsdCA9PiB1cGRhdGUgdGhlIG1lbnVcbiAgICAgICAgICAgIGxvYWRlZFtwbHVnaW5dID0gSlNPTkV4dC5kZWVwQ29weShuZXdJdGVtcyk7XG4gICAgICAgICAgICAvLyBNZXJnZSBwb3RlbnRpYWwgZGlzYWJsZWQgc3RhdGVcbiAgICAgICAgICAgIGNvbnN0IHRvQWRkID1cbiAgICAgICAgICAgICAgU2V0dGluZ1JlZ2lzdHJ5LnJlY29uY2lsZUl0ZW1zKFxuICAgICAgICAgICAgICAgIG5ld0l0ZW1zLFxuICAgICAgICAgICAgICAgIGNvbnRleHRJdGVtcyxcbiAgICAgICAgICAgICAgICBmYWxzZSxcbiAgICAgICAgICAgICAgICBmYWxzZVxuICAgICAgICAgICAgICApID8/IFtdO1xuICAgICAgICAgICAgU2V0dGluZ1JlZ2lzdHJ5LmZpbHRlckRpc2FibGVkSXRlbXModG9BZGQpLmZvckVhY2goaXRlbSA9PiB7XG4gICAgICAgICAgICAgIE1lbnVGYWN0b3J5LmFkZENvbnRleHRJdGVtKFxuICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgIC8vIFdlIGhhdmUgdG8gc2V0IHRoZSBkZWZhdWx0IHJhbmsgYmVjYXVzZSBMdW1pbm8gaXMgc29ydGluZyB0aGUgdmlzaWJsZSBpdGVtc1xuICAgICAgICAgICAgICAgICAgcmFuazogREVGQVVMVF9DT05URVhUX0lURU1fUkFOSyxcbiAgICAgICAgICAgICAgICAgIC4uLml0ZW1cbiAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICAgIGNvbnRleHRNZW51LFxuICAgICAgICAgICAgICAgIG1lbnVGYWN0b3J5XG4gICAgICAgICAgICAgICk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIGV4cG9ydCBmdW5jdGlvbiBhY3RpdmF0ZVNpZGViYXJTd2l0Y2hlcihcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsLFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBpbml0aWFsOiBJTGFiU2hlbGwuSUxheW91dFxuICApOiB2b2lkIHtcbiAgICBjb25zdCBzZXR0aW5nID0gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpzaWRlYmFyJztcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGxldCBvdmVycmlkZXM6IFNpZGViYXJPdmVycmlkZXMgPSB7fTtcbiAgICBjb25zdCB1cGRhdGUgPSAoXzogSUxhYlNoZWxsLCBsYXlvdXQ6IElMYWJTaGVsbC5JTGF5b3V0IHwgdm9pZCkgPT4ge1xuICAgICAgZWFjaChsYWJTaGVsbC53aWRnZXRzKCdsZWZ0JyksIHdpZGdldCA9PiB7XG4gICAgICAgIGlmIChvdmVycmlkZXNbd2lkZ2V0LmlkXSAmJiBvdmVycmlkZXNbd2lkZ2V0LmlkXSA9PT0gJ3JpZ2h0Jykge1xuICAgICAgICAgIGxhYlNoZWxsLmFkZCh3aWRnZXQsICdyaWdodCcpO1xuICAgICAgICAgIGlmIChsYXlvdXQgJiYgbGF5b3V0LnJpZ2h0QXJlYT8uY3VycmVudFdpZGdldCA9PT0gd2lkZ2V0KSB7XG4gICAgICAgICAgICBsYWJTaGVsbC5hY3RpdmF0ZUJ5SWQod2lkZ2V0LmlkKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgICAgZWFjaChsYWJTaGVsbC53aWRnZXRzKCdyaWdodCcpLCB3aWRnZXQgPT4ge1xuICAgICAgICBpZiAob3ZlcnJpZGVzW3dpZGdldC5pZF0gJiYgb3ZlcnJpZGVzW3dpZGdldC5pZF0gPT09ICdsZWZ0Jykge1xuICAgICAgICAgIGxhYlNoZWxsLmFkZCh3aWRnZXQsICdsZWZ0Jyk7XG4gICAgICAgICAgaWYgKGxheW91dCAmJiBsYXlvdXQubGVmdEFyZWE/LmN1cnJlbnRXaWRnZXQgPT09IHdpZGdldCkge1xuICAgICAgICAgICAgbGFiU2hlbGwuYWN0aXZhdGVCeUlkKHdpZGdldC5pZCk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9O1xuICAgIC8vIEZldGNoIG92ZXJyaWRlcyBmcm9tIHRoZSBzZXR0aW5ncyBzeXN0ZW0uXG4gICAgdm9pZCBQcm9taXNlLmFsbChbc2V0dGluZ1JlZ2lzdHJ5LmxvYWQoc2V0dGluZyksIGFwcC5yZXN0b3JlZF0pLnRoZW4oXG4gICAgICAoW3NldHRpbmdzXSkgPT4ge1xuICAgICAgICBvdmVycmlkZXMgPSAoc2V0dGluZ3MuZ2V0KCdvdmVycmlkZXMnKS5jb21wb3NpdGUgfHxcbiAgICAgICAgICB7fSkgYXMgU2lkZWJhck92ZXJyaWRlcztcbiAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KHNldHRpbmdzID0+IHtcbiAgICAgICAgICBvdmVycmlkZXMgPSAoc2V0dGluZ3MuZ2V0KCdvdmVycmlkZXMnKS5jb21wb3NpdGUgfHxcbiAgICAgICAgICAgIHt9KSBhcyBTaWRlYmFyT3ZlcnJpZGVzO1xuICAgICAgICAgIHVwZGF0ZShsYWJTaGVsbCk7XG4gICAgICAgIH0pO1xuICAgICAgICBsYWJTaGVsbC5sYXlvdXRNb2RpZmllZC5jb25uZWN0KHVwZGF0ZSk7XG4gICAgICAgIHVwZGF0ZShsYWJTaGVsbCwgaW5pdGlhbCk7XG4gICAgICB9XG4gICAgKTtcblxuICAgIC8vIEFkZCBhIGNvbW1hbmQgdG8gc3dpdGNoIGEgc2lkZSBwYW5lbHMncyBzaWRlXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zd2l0Y2hTaWRlYmFyLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1N3aXRjaCBTaWRlYmFyIFNpZGUnKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgLy8gRmlyc3QsIHRyeSB0byBmaW5kIHRoZSBjb3JyZWN0IHBhbmVsIGJhc2VkIG9uIHRoZSBhcHBsaWNhdGlvblxuICAgICAgICAvLyBjb250ZXh0IG1lbnUgY2xpY2suIEJhaWwgaWYgd2UgZG9uJ3QgZmluZCBhIHNpZGViYXIgZm9yIHRoZSB3aWRnZXQuXG4gICAgICAgIGNvbnN0IGNvbnRleHROb2RlOiBIVE1MRWxlbWVudCB8IHVuZGVmaW5lZCA9IGFwcC5jb250ZXh0TWVudUhpdFRlc3QoXG4gICAgICAgICAgbm9kZSA9PiAhIW5vZGUuZGF0YXNldC5pZFxuICAgICAgICApO1xuICAgICAgICBpZiAoIWNvbnRleHROb2RlKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgaWQgPSBjb250ZXh0Tm9kZS5kYXRhc2V0WydpZCddITtcbiAgICAgICAgY29uc3QgbGVmdFBhbmVsID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2pwLWxlZnQtc3RhY2snKTtcbiAgICAgICAgY29uc3Qgbm9kZSA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKGlkKTtcbiAgICAgICAgbGV0IHNpZGU6ICdsZWZ0JyB8ICdyaWdodCc7XG5cbiAgICAgICAgaWYgKGxlZnRQYW5lbCAmJiBub2RlICYmIGxlZnRQYW5lbC5jb250YWlucyhub2RlKSkge1xuICAgICAgICAgIHNpZGUgPSAncmlnaHQnO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHNpZGUgPSAnbGVmdCc7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBNb3ZlIHRoZSBwYW5lbCB0byB0aGUgb3RoZXIgc2lkZS5cbiAgICAgICAgcmV0dXJuIHNldHRpbmdSZWdpc3RyeS5zZXQoc2V0dGluZywgJ292ZXJyaWRlcycsIHtcbiAgICAgICAgICAuLi5vdmVycmlkZXMsXG4gICAgICAgICAgW2lkXTogc2lkZVxuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==