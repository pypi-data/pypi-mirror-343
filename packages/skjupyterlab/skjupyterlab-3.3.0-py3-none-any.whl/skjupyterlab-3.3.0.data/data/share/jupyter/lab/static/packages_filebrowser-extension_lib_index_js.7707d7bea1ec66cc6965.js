(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_filebrowser-extension_lib_index_js"],{

/***/ "../packages/filebrowser-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/filebrowser-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "fileUploadStatus": () => (/* binding */ fileUploadStatus),
/* harmony export */   "launcherToolbarButton": () => (/* binding */ launcherToolbarButton),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands/@lumino/commands");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_lumino_commands__WEBPACK_IMPORTED_MODULE_11__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module filebrowser-extension
 */












/**
 * The command IDs used by the file browser plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.copy = 'filebrowser:copy';
    CommandIDs.copyDownloadLink = 'filebrowser:copy-download-link';
    // For main browser only.
    CommandIDs.createLauncher = 'filebrowser:create-main-launcher';
    CommandIDs.cut = 'filebrowser:cut';
    CommandIDs.del = 'filebrowser:delete';
    CommandIDs.download = 'filebrowser:download';
    CommandIDs.duplicate = 'filebrowser:duplicate';
    // For main browser only.
    CommandIDs.hideBrowser = 'filebrowser:hide-main';
    CommandIDs.goToPath = 'filebrowser:go-to-path';
    CommandIDs.goUp = 'filebrowser:go-up';
    CommandIDs.openPath = 'filebrowser:open-path';
    CommandIDs.open = 'filebrowser:open';
    CommandIDs.openBrowserTab = 'filebrowser:open-browser-tab';
    CommandIDs.paste = 'filebrowser:paste';
    CommandIDs.createNewDirectory = 'filebrowser:create-new-directory';
    CommandIDs.createNewFile = 'filebrowser:create-new-file';
    CommandIDs.createNewMarkdownFile = 'filebrowser:create-new-markdown-file';
    CommandIDs.rename = 'filebrowser:rename';
    // For main browser only.
    CommandIDs.copyShareableLink = 'filebrowser:share-main';
    // For main browser only.
    CommandIDs.copyPath = 'filebrowser:copy-path';
    CommandIDs.showBrowser = 'filebrowser:activate';
    CommandIDs.shutdown = 'filebrowser:shutdown';
    // For main browser only.
    CommandIDs.toggleBrowser = 'filebrowser:toggle-main';
    CommandIDs.toggleNavigateToCurrentDirectory = 'filebrowser:toggle-navigate-to-current-directory';
    CommandIDs.toggleLastModified = 'filebrowser:toggle-last-modified';
    CommandIDs.search = 'filebrowser:search';
    CommandIDs.toggleHiddenFiles = 'filebrowser:toggle-hidden-files';
})(CommandIDs || (CommandIDs = {}));
/**
 * The file browser namespace token.
 */
const namespace = 'filebrowser';
/**
 * The default file browser extension.
 */
const browser = {
    id: '@jupyterlab/filebrowser-extension:browser',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ITreePathUpdater,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette
    ],
    autoStart: true,
    activate: async (app, factory, translator, restorer, settingRegistry, treePathUpdater, commandPalette) => {
        const trans = translator.load('jupyterlab');
        const browser = factory.defaultBrowser;
        // Let the application restorer track the primary file browser (that is
        // automatically created) for restoration of application state (e.g. setting
        // the file browser as the current side bar widget).
        //
        // All other file browsers created by using the factory function are
        // responsible for their own restoration behavior, if any.
        if (restorer) {
            restorer.add(browser, namespace);
        }
        // Navigate to preferred-dir trait if found
        const preferredPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('preferredPath');
        if (preferredPath) {
            await browser.model.cd(preferredPath);
        }
        addCommands(app, factory, translator, settingRegistry, commandPalette);
        // Show the current file browser shortcut in its title.
        const updateBrowserTitle = () => {
            const binding = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.find)(app.commands.keyBindings, b => b.command === CommandIDs.toggleBrowser);
            if (binding) {
                const ks = _lumino_commands__WEBPACK_IMPORTED_MODULE_11__.CommandRegistry.formatKeystroke(binding.keys.join(' '));
                browser.title.caption = trans.__('File Browser (%1)', ks);
            }
            else {
                browser.title.caption = trans.__('File Browser');
            }
        };
        updateBrowserTitle();
        app.commands.keyBindingChanged.connect(() => {
            updateBrowserTitle();
        });
        void Promise.all([app.restored, browser.model.restored]).then(() => {
            if (treePathUpdater) {
                browser.model.pathChanged.connect((sender, args) => {
                    treePathUpdater(args.newValue);
                });
            }
            let navigateToCurrentDirectory = false;
            let showLastModifiedColumn = true;
            let useFuzzyFilter = true;
            let showHiddenFiles = false;
            if (settingRegistry) {
                void settingRegistry
                    .load('@jupyterlab/filebrowser-extension:browser')
                    .then(settings => {
                    settings.changed.connect(settings => {
                        navigateToCurrentDirectory = settings.get('navigateToCurrentDirectory').composite;
                        browser.navigateToCurrentDirectory = navigateToCurrentDirectory;
                    });
                    navigateToCurrentDirectory = settings.get('navigateToCurrentDirectory').composite;
                    browser.navigateToCurrentDirectory = navigateToCurrentDirectory;
                    settings.changed.connect(settings => {
                        showLastModifiedColumn = settings.get('showLastModifiedColumn')
                            .composite;
                        browser.showLastModifiedColumn = showLastModifiedColumn;
                    });
                    showLastModifiedColumn = settings.get('showLastModifiedColumn')
                        .composite;
                    browser.showLastModifiedColumn = showLastModifiedColumn;
                    settings.changed.connect(settings => {
                        useFuzzyFilter = settings.get('useFuzzyFilter')
                            .composite;
                        browser.useFuzzyFilter = useFuzzyFilter;
                    });
                    useFuzzyFilter = settings.get('useFuzzyFilter')
                        .composite;
                    browser.useFuzzyFilter = useFuzzyFilter;
                    settings.changed.connect(settings => {
                        showHiddenFiles = settings.get('showHiddenFiles')
                            .composite;
                        browser.showHiddenFiles = showHiddenFiles;
                    });
                    showHiddenFiles = settings.get('showHiddenFiles')
                        .composite;
                    browser.showHiddenFiles = showHiddenFiles;
                });
            }
        });
    }
};
/**
 * The default file browser factory provider.
 */
const factory = {
    id: '@jupyterlab/filebrowser-extension:factory',
    provides: _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    optional: [_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6__.IStateDB, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.ITreeResolver],
    activate: async (app, docManager, translator, state, router, tree) => {
        const { commands } = app;
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({ namespace });
        const createFileBrowser = (id, options = {}) => {
            var _a;
            const model = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.FilterFileBrowserModel({
                translator: translator,
                auto: (_a = options.auto) !== null && _a !== void 0 ? _a : true,
                manager: docManager,
                driveName: options.driveName || '',
                refreshInterval: options.refreshInterval,
                state: options.state === null
                    ? undefined
                    : options.state || state || undefined
            });
            const restore = options.restore;
            const widget = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.FileBrowser({ id, model, restore, translator });
            // Track the newly created file browser.
            void tracker.add(widget);
            return widget;
        };
        // Manually restore and load the default file browser.
        const defaultBrowser = createFileBrowser('filebrowser', {
            auto: false,
            restore: false
        });
        void Private.restoreBrowser(defaultBrowser, commands, router, tree);
        return { createFileBrowser, defaultBrowser, tracker };
    }
};
/**
 * A plugin providing download + copy download link commands in the context menu.
 *
 * Disabling this plugin will NOT disable downloading files from the server.
 * Users will still be able to retrieve files from the file download URLs the
 * server provides.
 */
const downloadPlugin = {
    id: '@jupyterlab/filebrowser-extension:download',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    autoStart: true,
    activate: (app, factory, translator) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        const { tracker } = factory;
        commands.addCommand(CommandIDs.download, {
            execute: () => {
                const widget = tracker.currentWidget;
                if (widget) {
                    return widget.download();
                }
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.downloadIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Download')
        });
        commands.addCommand(CommandIDs.copyDownloadLink, {
            execute: () => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                return widget.model.manager.services.contents
                    .getDownloadUrl(widget.selectedItems().next().path)
                    .then(url => {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(url);
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.copyIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Copy Download Link'),
            mnemonic: 0
        });
    }
};
/**
 * A plugin to add the file browser widget to an ILabShell
 */
const browserWidget = {
    id: '@jupyterlab/filebrowser-extension:widget',
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, docManager, factory, translator, labShell) => {
        const { commands } = app;
        const { defaultBrowser: browser, tracker } = factory;
        const trans = translator.load('jupyterlab');
        // Set attributes when adding the browser to the UI
        browser.node.setAttribute('role', 'region');
        browser.node.setAttribute('aria-label', trans.__('File Browser Section'));
        browser.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.folderSkIcon;
        labShell.add(browser, 'left', { rank: 100 });
        commands.addCommand(CommandIDs.showBrowser, {
            execute: args => {
                const path = args.path || '';
                const browserForPath = Private.getBrowserForPath(path, factory);
                // Check for browser not found
                if (!browserForPath) {
                    return;
                }
                // Shortcut if we are using the main file browser
                if (browser === browserForPath) {
                    labShell.activateById(browser.id);
                    return;
                }
                else {
                    const areas = ['left', 'right'];
                    for (const area of areas) {
                        const it = labShell.widgets(area);
                        let widget = it.next();
                        while (widget) {
                            if (widget.contains(browserForPath)) {
                                labShell.activateById(widget.id);
                                return;
                            }
                            widget = it.next();
                        }
                    }
                }
            }
        });
        commands.addCommand(CommandIDs.hideBrowser, {
            execute: () => {
                const widget = tracker.currentWidget;
                if (widget && !widget.isHidden) {
                    labShell.collapseLeft();
                }
            }
        });
        // If the layout is a fresh session without saved data and not in single document
        // mode, open file browser.
        void labShell.restored.then(layout => {
            if (layout.fresh && labShell.mode !== 'single-document') {
                void commands.execute(CommandIDs.showBrowser, void 0);
            }
        });
        void Promise.all([app.restored, browser.model.restored]).then(() => {
            function maybeCreate() {
                // Create a launcher if there are no open items.
                if (labShell.isEmpty('main') &&
                    commands.hasCommand('launcher:create')) {
                    void Private.createLauncher(commands, browser);
                }
            }
            // When layout is modified, create a launcher if there are no open items.
            labShell.layoutModified.connect(() => {
                maybeCreate();
            });
            // Whether to automatically navigate to a document's current directory
            labShell.currentChanged.connect(async (_, change) => {
                if (browser.navigateToCurrentDirectory && change.newValue) {
                    const { newValue } = change;
                    const context = docManager.contextForWidget(newValue);
                    if (context) {
                        const { path } = context;
                        try {
                            await Private.navigateToPath(path, factory, translator);
                        }
                        catch (reason) {
                            console.warn(`${CommandIDs.goToPath} failed to open: ${path}`, reason);
                        }
                    }
                }
            });
            maybeCreate();
        });
    }
};
/**
 * The default file browser share-file plugin
 *
 * This extension adds a "Copy Shareable Link" command that generates a copy-
 * pastable URL. This url can be used to open a particular file in JupyterLab,
 * handy for emailing links or bookmarking for reference.
 *
 * If you need to change how this link is generated (for instance, to copy a
 * /user-redirect URL for JupyterHub), disable this plugin and replace it
 * with another implementation.
 */
const shareFile = {
    id: '@jupyterlab/filebrowser-extension:share-file',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    autoStart: true,
    activate: (app, factory, translator) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        const { tracker } = factory;
        commands.addCommand(CommandIDs.copyShareableLink, {
            execute: () => {
                const widget = tracker.currentWidget;
                const model = widget === null || widget === void 0 ? void 0 : widget.selectedItems().next();
                if (!model) {
                    return;
                }
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getUrl({
                    workspace: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.defaultWorkspace,
                    treePath: model.path,
                    toShare: true
                }));
            },
            isVisible: () => !!tracker.currentWidget &&
                (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.toArray)(tracker.currentWidget.selectedItems()).length === 1,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.linkIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Copy Shareable Link')
        });
    }
};
/**
 * The "Open With" context menu.
 *
 * This is its own plugin in case you would like to disable this feature.
 * e.g. jupyter labextension disable @jupyterlab/filebrowser-extension:open-with
 */
const openWithPlugin = {
    id: '@jupyterlab/filebrowser-extension:open-with',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory],
    autoStart: true,
    activate: (app, factory) => {
        const { docRegistry } = app;
        const { tracker } = factory;
        function updateOpenWithMenu(contextMenu) {
            var _a, _b;
            const openWith = (_b = (_a = contextMenu.menu.items.find(item => {
                var _a;
                return item.type === 'submenu' &&
                    ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-contextmenu-open-with';
            })) === null || _a === void 0 ? void 0 : _a.submenu) !== null && _b !== void 0 ? _b : null;
            if (!openWith) {
                return; // Bail early if the open with menu is not displayed
            }
            // clear the current menu items
            openWith.clearItems();
            // get the widget factories that could be used to open all of the items
            // in the current filebrowser selection
            const factories = tracker.currentWidget
                ? Private.OpenWith.intersection((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.map)(tracker.currentWidget.selectedItems(), i => {
                    return Private.OpenWith.getFactories(docRegistry, i);
                }))
                : new Set();
            // make new menu items from the widget factories
            factories.forEach(factory => {
                openWith.addItem({
                    args: { factory: factory },
                    command: CommandIDs.open
                });
            });
        }
        app.contextMenu.opened.connect(updateOpenWithMenu);
    }
};
/**
 * The "Open in New Browser Tab" context menu.
 *
 * This is its own plugin in case you would like to disable this feature.
 * e.g. jupyter labextension disable @jupyterlab/filebrowser-extension:open-browser-tab
 *
 * Note: If disabling this, you may also want to disable:
 * @jupyterlab/docmanager-extension:open-browser-tab
 */
const openBrowserTabPlugin = {
    id: '@jupyterlab/filebrowser-extension:open-browser-tab',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    autoStart: true,
    activate: (app, factory, translator) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const { tracker } = factory;
        commands.addCommand(CommandIDs.openBrowserTab, {
            execute: () => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                return Promise.all((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.toArray)((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.map)(widget.selectedItems(), item => {
                    return commands.execute('docmanager:open-browser-tab', {
                        path: item.path
                    });
                })));
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.skAddIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Open in New Browser Tab'),
            mnemonic: 0
        });
    }
};
/**
 * A plugin providing file upload status.
 */
const fileUploadStatus = {
    id: '@jupyterlab/filebrowser-extension:file-upload-status',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7__.IStatusBar],
    activate: (app, browser, translator, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const item = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.FileUploadStatus({
            tracker: browser.tracker,
            translator
        });
        statusBar.registerStatusItem('@jupyterlab/filebrowser-extension:file-upload-status', {
            item,
            align: 'middle',
            isActive: () => {
                return !!item.model && item.model.items.length > 0;
            },
            activeStateChanged: item.model.stateChanged
        });
    }
};
/**
 * A plugin to add a launcher button to the file browser toolbar
 */
const launcherToolbarButton = {
    id: '@jupyterlab/filebrowser-extension:launcher-toolbar-button',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    activate: (app, factory, translator) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const { defaultBrowser: browser } = factory;
        // Add a launcher toolbar item.
        const launcher = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.skAddIcon,
            onClick: () => {
                if (commands.hasCommand('launcher:create')) {
                    return Private.createLauncher(commands, browser);
                }
            },
            tooltip: trans.__('New Launcher'),
            actualOnClick: true
        });
        browser.toolbar.insertItem(0, 'launch', launcher);
    }
};
/**
 * Add the main file browser commands to the application's command registry.
 */
function addCommands(app, factory, translator, settingRegistry, commandPalette) {
    const trans = translator.load('jupyterlab');
    const { docRegistry: registry, commands } = app;
    const { defaultBrowser: browser, tracker } = factory;
    commands.addCommand(CommandIDs.del, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.delete();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.closeIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Delete'),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.copy, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.copy();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.copyIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Copy'),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.cut, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.cut();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.cutIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Cut')
    });
    commands.addCommand(CommandIDs.duplicate, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.duplicate();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.copyIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Duplicate')
    });
    commands.addCommand(CommandIDs.goToPath, {
        execute: async (args) => {
            var _a;
            const path = args.path || '';
            const showBrowser = !((_a = args === null || args === void 0 ? void 0 : args.dontShowBrowser) !== null && _a !== void 0 ? _a : false);
            try {
                const item = await Private.navigateToPath(path, factory, translator);
                if (item.type !== 'directory' && showBrowser) {
                    const browserForPath = Private.getBrowserForPath(path, factory);
                    if (browserForPath) {
                        browserForPath.clearSelectedItems();
                        const parts = path.split('/');
                        const name = parts[parts.length - 1];
                        if (name) {
                            await browserForPath.selectItemByName(name);
                        }
                    }
                }
            }
            catch (reason) {
                console.warn(`${CommandIDs.goToPath} failed to go to: ${path}`, reason);
            }
            if (showBrowser) {
                return commands.execute(CommandIDs.showBrowser, { path });
            }
        }
    });
    commands.addCommand(CommandIDs.goUp, {
        label: 'go up',
        execute: async () => {
            const browserForPath = Private.getBrowserForPath('', factory);
            if (!browserForPath) {
                return;
            }
            const { model } = browserForPath;
            await model.restored;
            if (model.path === model.rootPath) {
                return;
            }
            try {
                await model.cd('..');
            }
            catch (reason) {
                console.warn(`${CommandIDs.goUp} failed to go to parent directory of ${model.path}`, reason);
            }
        }
    });
    commands.addCommand(CommandIDs.openPath, {
        label: args => args.path ? trans.__('Open %1', args.path) : trans.__('Open from Path…'),
        caption: args => args.path ? trans.__('Open %1', args.path) : trans.__('Open from path'),
        execute: async (args) => {
            var _a;
            let path;
            if (args === null || args === void 0 ? void 0 : args.path) {
                path = args.path;
            }
            else {
                path = (_a = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getText({
                    label: trans.__('Path'),
                    placeholder: '/path/relative/to/jlab/root',
                    title: trans.__('Open Path'),
                    okLabel: trans.__('Open')
                })).value) !== null && _a !== void 0 ? _a : undefined;
            }
            if (!path) {
                return;
            }
            try {
                const trailingSlash = path !== '/' && path.endsWith('/');
                if (trailingSlash) {
                    // The normal contents service errors on paths ending in slash
                    path = path.slice(0, path.length - 1);
                }
                const browserForPath = Private.getBrowserForPath(path, factory);
                const { services } = browserForPath.model.manager;
                const item = await services.contents.get(path, {
                    content: false
                });
                if (trailingSlash && item.type !== 'directory') {
                    throw new Error(`Path ${path}/ is not a directory`);
                }
                await commands.execute(CommandIDs.goToPath, {
                    path,
                    dontShowBrowser: args.dontShowBrowser
                });
                if (item.type === 'directory') {
                    return;
                }
                return commands.execute('docmanager:open', { path });
            }
            catch (reason) {
                if (reason.response && reason.response.status === 404) {
                    reason.message = trans.__('Could not find path: %1', path);
                }
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Cannot open'), reason);
            }
        }
    });
    // Add the openPath command to the command palette
    if (commandPalette) {
        commandPalette.addItem({
            command: CommandIDs.openPath,
            category: trans.__('File Operations')
        });
    }
    commands.addCommand(CommandIDs.open, {
        execute: args => {
            const factory = args['factory'] || void 0;
            const widget = tracker.currentWidget;
            if (!widget) {
                return;
            }
            const { contents } = widget.model.manager.services;
            return Promise.all((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.toArray)((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.map)(widget.selectedItems(), item => {
                if (item.type === 'directory') {
                    const localPath = contents.localPath(item.path);
                    return widget.model.cd(`/${localPath}`);
                }
                return commands.execute('docmanager:open', {
                    factory: factory,
                    path: item.path
                });
            })));
        },
        icon: args => {
            var _a;
            const factory = args['factory'] || void 0;
            if (factory) {
                // if an explicit factory is passed...
                const ft = registry.getFileType(factory);
                // ...set an icon if the factory name corresponds to a file type name...
                // ...or leave the icon blank
                return (_a = ft === null || ft === void 0 ? void 0 : ft.icon) === null || _a === void 0 ? void 0 : _a.bindprops({ stylesheet: 'menuItem' });
            }
            else {
                return _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.folderSkIcon.bindprops({ stylesheet: 'menuItem' });
            }
        },
        // FIXME-TRANS: Is this localizable?
        label: args => (args['label'] || args['factory'] || trans.__('Open')),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.paste, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.paste();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.pasteIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Paste'),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.createNewDirectory, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.createNewDirectory();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.newFolderIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('New Folder')
    });
    commands.addCommand(CommandIDs.createNewFile, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.createNewFile({ ext: 'txt' });
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.textEditorIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('New File')
    });
    commands.addCommand(CommandIDs.createNewMarkdownFile, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.createNewFile({ ext: 'md' });
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.markdownIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('New Markdown File')
    });
    commands.addCommand(CommandIDs.rename, {
        execute: args => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.rename();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.editIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Rename'),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.copyPath, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (!widget) {
                return;
            }
            const item = widget.selectedItems().next();
            if (!item) {
                return;
            }
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(item.path);
        },
        isVisible: () => !!tracker.currentWidget &&
            tracker.currentWidget.selectedItems().next !== undefined,
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.fileIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Copy Path')
    });
    commands.addCommand(CommandIDs.shutdown, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.shutdownKernels();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.stopIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Shut Down Kernel')
    });
    commands.addCommand(CommandIDs.toggleBrowser, {
        execute: () => {
            if (browser.isHidden) {
                return commands.execute(CommandIDs.showBrowser, void 0);
            }
            return commands.execute(CommandIDs.hideBrowser, void 0);
        }
    });
    commands.addCommand(CommandIDs.createLauncher, {
        label: trans.__('New Launcher'),
        execute: () => Private.createLauncher(commands, browser)
    });
    if (settingRegistry) {
        commands.addCommand(CommandIDs.toggleNavigateToCurrentDirectory, {
            label: trans.__('Show Active File in File Browser'),
            isToggled: () => browser.navigateToCurrentDirectory,
            execute: () => {
                const value = !browser.navigateToCurrentDirectory;
                const key = 'navigateToCurrentDirectory';
                return settingRegistry
                    .set('@jupyterlab/filebrowser-extension:browser', key, value)
                    .catch((reason) => {
                    console.error(`Failed to set navigateToCurrentDirectory setting`);
                });
            }
        });
    }
    commands.addCommand(CommandIDs.toggleLastModified, {
        label: trans.__('Show Last Modified Column'),
        isToggled: () => browser.showLastModifiedColumn,
        execute: () => {
            const value = !browser.showLastModifiedColumn;
            const key = 'showLastModifiedColumn';
            if (settingRegistry) {
                return settingRegistry
                    .set('@jupyterlab/filebrowser-extension:browser', key, value)
                    .catch((reason) => {
                    console.error(`Failed to set showLastModifiedColumn setting`);
                });
            }
        }
    });
    commands.addCommand(CommandIDs.toggleHiddenFiles, {
        label: trans.__('Show Hidden Files'),
        isToggled: () => browser.showHiddenFiles,
        isVisible: () => _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('allow_hidden_files') === 'true',
        execute: () => {
            const value = !browser.showHiddenFiles;
            const key = 'showHiddenFiles';
            if (settingRegistry) {
                return settingRegistry
                    .set('@jupyterlab/filebrowser-extension:browser', key, value)
                    .catch((reason) => {
                    console.error(`Failed to set showHiddenFiles setting`);
                });
            }
        }
    });
    commands.addCommand(CommandIDs.search, {
        label: trans.__('Search on File Names'),
        execute: () => alert('search')
    });
    if (commandPalette) {
        commandPalette.addItem({
            command: CommandIDs.toggleNavigateToCurrentDirectory,
            category: trans.__('File Operations')
        });
    }
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Create a launcher for a given filebrowser widget.
     */
    function createLauncher(commands, browser) {
        const { model } = browser;
        return commands
            .execute('launcher:create', { cwd: model.path })
            .then((launcher) => {
            model.pathChanged.connect(() => {
                if (launcher.content) {
                    launcher.content.cwd = model.path;
                }
            }, launcher);
            return launcher;
        });
    }
    Private.createLauncher = createLauncher;
    /**
     * Get browser object given file path.
     */
    function getBrowserForPath(path, factory) {
        const { defaultBrowser: browser, tracker } = factory;
        const driveName = browser.model.manager.services.contents.driveName(path);
        if (driveName) {
            const browserForPath = tracker.find(_path => _path.model.driveName === driveName);
            if (!browserForPath) {
                // warn that no filebrowser could be found for this driveName
                console.warn(`${CommandIDs.goToPath} failed to find filebrowser for path: ${path}`);
                return;
            }
            return browserForPath;
        }
        // if driveName is empty, assume the main filebrowser
        return browser;
    }
    Private.getBrowserForPath = getBrowserForPath;
    /**
     * Navigate to a path or the path containing a file.
     */
    async function navigateToPath(path, factory, translator) {
        const trans = translator.load('jupyterlab');
        const browserForPath = Private.getBrowserForPath(path, factory);
        if (!browserForPath) {
            throw new Error(trans.__('No browser for path'));
        }
        const { services } = browserForPath.model.manager;
        const localPath = services.contents.localPath(path);
        await services.ready;
        const item = await services.contents.get(path, { content: false });
        const { model } = browserForPath;
        await model.restored;
        if (item.type === 'directory') {
            await model.cd(`/${localPath}`);
        }
        else {
            await model.cd(`/${_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.dirname(localPath)}`);
        }
        return item;
    }
    Private.navigateToPath = navigateToPath;
    /**
     * Restores file browser state and overrides state if tree resolver resolves.
     */
    async function restoreBrowser(browser, commands, router, tree) {
        const restoring = 'jp-mod-restoring';
        browser.addClass(restoring);
        if (!router) {
            await browser.model.restore(browser.id);
            await browser.model.refresh();
            browser.removeClass(restoring);
            return;
        }
        const listener = async () => {
            router.routed.disconnect(listener);
            const paths = await (tree === null || tree === void 0 ? void 0 : tree.paths);
            if ((paths === null || paths === void 0 ? void 0 : paths.file) || (paths === null || paths === void 0 ? void 0 : paths.browser)) {
                // Restore the model without populating it.
                await browser.model.restore(browser.id, false);
                if (paths.file) {
                    await commands.execute(CommandIDs.openPath, {
                        path: paths.file,
                        dontShowBrowser: true
                    });
                }
                if (paths.browser) {
                    await commands.execute(CommandIDs.openPath, {
                        path: paths.browser,
                        dontShowBrowser: true
                    });
                }
            }
            else {
                await browser.model.restore(browser.id);
                await browser.model.refresh();
            }
            browser.removeClass(restoring);
        };
        router.routed.connect(listener);
    }
    Private.restoreBrowser = restoreBrowser;
})(Private || (Private = {}));
/**
 * Export the plugins as default.
 */
const plugins = [
    factory,
    browser,
    shareFile,
    fileUploadStatus,
    downloadPlugin,
    browserWidget,
    launcherToolbarButton,
    openWithPlugin,
    openBrowserTabPlugin
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
(function (Private) {
    let OpenWith;
    (function (OpenWith) {
        /**
         * Get the factories for the selected item
         *
         * @param docRegistry Application document registry
         * @param item Selected item model
         * @returns Available factories for the model
         */
        function getFactories(docRegistry, item) {
            var _a;
            const factories = docRegistry
                .preferredWidgetFactories(item.path)
                .map(f => f.name);
            const notebookFactory = (_a = docRegistry.getWidgetFactory('notebook')) === null || _a === void 0 ? void 0 : _a.name;
            if (notebookFactory &&
                item.type === 'notebook' &&
                factories.indexOf(notebookFactory) === -1) {
                factories.unshift(notebookFactory);
            }
            return factories;
        }
        OpenWith.getFactories = getFactories;
        /**
         * Return the intersection of multiple arrays.
         *
         * @param iter Iterator of arrays
         * @returns Set of common elements to all arrays
         */
        function intersection(iter) {
            // pop the first element of iter
            const first = iter.next();
            // first will be undefined if iter is empty
            if (!first) {
                return new Set();
            }
            // "initialize" the intersection from first
            const isect = new Set(first);
            // reduce over the remaining elements of iter
            return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.reduce)(iter, (isect, subarr) => {
                // filter out all elements not present in both isect and subarr,
                // accumulate result in new set
                return new Set(subarr.filter(x => isect.has(x)));
            }, isect);
        }
        OpenWith.intersection = intersection;
    })(OpenWith = Private.OpenWith || (Private.OpenWith = {}));
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZmlsZWJyb3dzZXItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQVM4QjtBQVNIO0FBQzhCO0FBQ0Y7QUFPekI7QUFHOEI7QUFDaEI7QUFDSTtBQUNHO0FBZ0JuQjtBQUN1QztBQUN2QjtBQUduRDs7R0FFRztBQUNILElBQVUsVUFBVSxDQTREbkI7QUE1REQsV0FBVSxVQUFVO0lBQ0wsZUFBSSxHQUFHLGtCQUFrQixDQUFDO0lBRTFCLDJCQUFnQixHQUFHLGdDQUFnQyxDQUFDO0lBRWpFLHlCQUF5QjtJQUNaLHlCQUFjLEdBQUcsa0NBQWtDLENBQUM7SUFFcEQsY0FBRyxHQUFHLGlCQUFpQixDQUFDO0lBRXhCLGNBQUcsR0FBRyxvQkFBb0IsQ0FBQztJQUUzQixtQkFBUSxHQUFHLHNCQUFzQixDQUFDO0lBRWxDLG9CQUFTLEdBQUcsdUJBQXVCLENBQUM7SUFFakQseUJBQXlCO0lBQ1osc0JBQVcsR0FBRyx1QkFBdUIsQ0FBQztJQUV0QyxtQkFBUSxHQUFHLHdCQUF3QixDQUFDO0lBRXBDLGVBQUksR0FBRyxtQkFBbUIsQ0FBQztJQUUzQixtQkFBUSxHQUFHLHVCQUF1QixDQUFDO0lBRW5DLGVBQUksR0FBRyxrQkFBa0IsQ0FBQztJQUUxQix5QkFBYyxHQUFHLDhCQUE4QixDQUFDO0lBRWhELGdCQUFLLEdBQUcsbUJBQW1CLENBQUM7SUFFNUIsNkJBQWtCLEdBQUcsa0NBQWtDLENBQUM7SUFFeEQsd0JBQWEsR0FBRyw2QkFBNkIsQ0FBQztJQUU5QyxnQ0FBcUIsR0FBRyxzQ0FBc0MsQ0FBQztJQUUvRCxpQkFBTSxHQUFHLG9CQUFvQixDQUFDO0lBRTNDLHlCQUF5QjtJQUNaLDRCQUFpQixH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Y2M2OTY1LmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgZmlsZWJyb3dzZXItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlNoZWxsLFxuICBJTGF5b3V0UmVzdG9yZXIsXG4gIElSb3V0ZXIsXG4gIElUcmVlUGF0aFVwZGF0ZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIENsaXBib2FyZCxcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBJbnB1dERpYWxvZyxcbiAgTWFpbkFyZWFXaWRnZXQsXG4gIHNob3dFcnJvck1lc3NhZ2UsXG4gIFRvb2xiYXJCdXR0b24sXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgUGFnZUNvbmZpZywgUGF0aEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJRG9jdW1lbnRNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlcic7XG5pbXBvcnQgeyBEb2N1bWVudFJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHtcbiAgRmlsZUJyb3dzZXIsXG4gIEZpbGVVcGxvYWRTdGF0dXMsXG4gIEZpbHRlckZpbGVCcm93c2VyTW9kZWwsXG4gIElGaWxlQnJvd3NlckZhY3Rvcnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXInO1xuaW1wb3J0IHsgTGF1bmNoZXIgfSBmcm9tICdAanVweXRlcmxhYi9sYXVuY2hlcic7XG5pbXBvcnQgeyBDb250ZW50cyB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVN0YXRlREIgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7IElTdGF0dXNCYXIgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0dXNiYXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQge1xuICBza0FkZEljb24sXG4gIGNsb3NlSWNvbixcbiAgY29weUljb24sXG4gIGN1dEljb24sXG4gIGRvd25sb2FkSWNvbixcbiAgZWRpdEljb24sXG4gIGZpbGVJY29uLFxuICBmb2xkZXJTa0ljb24sXG4gIGxpbmtJY29uLFxuICBtYXJrZG93bkljb24sXG4gIG5ld0ZvbGRlckljb24sXG4gIHBhc3RlSWNvbixcbiAgc3RvcEljb24sXG4gIHRleHRFZGl0b3JJY29uXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgZmluZCwgSUl0ZXJhdG9yLCBtYXAsIHJlZHVjZSwgdG9BcnJheSB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHsgQ29udGV4dE1lbnUgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBmaWxlIGJyb3dzZXIgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjb3B5ID0gJ2ZpbGVicm93c2VyOmNvcHknO1xuXG4gIGV4cG9ydCBjb25zdCBjb3B5RG93bmxvYWRMaW5rID0gJ2ZpbGVicm93c2VyOmNvcHktZG93bmxvYWQtbGluayc7XG5cbiAgLy8gRm9yIG1haW4gYnJvd3NlciBvbmx5LlxuICBleHBvcnQgY29uc3QgY3JlYXRlTGF1bmNoZXIgPSAnZmlsZWJyb3dzZXI6Y3JlYXRlLW1haW4tbGF1bmNoZXInO1xuXG4gIGV4cG9ydCBjb25zdCBjdXQgPSAnZmlsZWJyb3dzZXI6Y3V0JztcblxuICBleHBvcnQgY29uc3QgZGVsID0gJ2ZpbGVicm93c2VyOmRlbGV0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGRvd25sb2FkID0gJ2ZpbGVicm93c2VyOmRvd25sb2FkJztcblxuICBleHBvcnQgY29uc3QgZHVwbGljYXRlID0gJ2ZpbGVicm93c2VyOmR1cGxpY2F0ZSc7XG5cbiAgLy8gRm9yIG1haW4gYnJvd3NlciBvbmx5LlxuICBleHBvcnQgY29uc3QgaGlkZUJyb3dzZXIgPSAnZmlsZWJyb3dzZXI6aGlkZS1tYWluJztcblxuICBleHBvcnQgY29uc3QgZ29Ub1BhdGggPSAnZmlsZWJyb3dzZXI6Z28tdG8tcGF0aCc7XG5cbiAgZXhwb3J0IGNvbnN0IGdvVXAgPSAnZmlsZWJyb3dzZXI6Z28tdXAnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuUGF0aCA9ICdmaWxlYnJvd3NlcjpvcGVuLXBhdGgnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuID0gJ2ZpbGVicm93c2VyOm9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuQnJvd3NlclRhYiA9ICdmaWxlYnJvd3NlcjpvcGVuLWJyb3dzZXItdGFiJztcblxuICBleHBvcnQgY29uc3QgcGFzdGUgPSAnZmlsZWJyb3dzZXI6cGFzdGUnO1xuXG4gIGV4cG9ydCBjb25zdCBjcmVhdGVOZXdEaXJlY3RvcnkgPSAnZmlsZWJyb3dzZXI6Y3JlYXRlLW5ldy1kaXJlY3RvcnknO1xuXG4gIGV4cG9ydCBjb25zdCBjcmVhdGVOZXdGaWxlID0gJ2ZpbGVicm93c2VyOmNyZWF0ZS1uZXctZmlsZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGNyZWF0ZU5ld01hcmtkb3duRmlsZSA9ICdmaWxlYnJvd3NlcjpjcmVhdGUtbmV3LW1hcmtkb3duLWZpbGUnO1xuXG4gIGV4cG9ydCBjb25zdCByZW5hbWUgPSAnZmlsZWJyb3dzZXI6cmVuYW1lJztcblxuICAvLyBGb3IgbWFpbiBicm93c2VyIG9ubHkuXG4gIGV4cG9ydCBjb25zdCBjb3B5U2hhcmVhYmxlTGluayA9ICdmaWxlYnJvd3NlcjpzaGFyZS1tYWluJztcblxuICAvLyBGb3IgbWFpbiBicm93c2VyIG9ubHkuXG4gIGV4cG9ydCBjb25zdCBjb3B5UGF0aCA9ICdmaWxlYnJvd3Nlcjpjb3B5LXBhdGgnO1xuXG4gIGV4cG9ydCBjb25zdCBzaG93QnJvd3NlciA9ICdmaWxlYnJvd3NlcjphY3RpdmF0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNodXRkb3duID0gJ2ZpbGVicm93c2VyOnNodXRkb3duJztcblxuICAvLyBGb3IgbWFpbiBicm93c2VyIG9ubHkuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVCcm93c2VyID0gJ2ZpbGVicm93c2VyOnRvZ2dsZS1tYWluJztcblxuICBleHBvcnQgY29uc3QgdG9nZ2xlTmF2aWdhdGVUb0N1cnJlbnREaXJlY3RvcnkgPVxuICAgICdmaWxlYnJvd3Nlcjp0b2dnbGUtbmF2aWdhdGUtdG8tY3VycmVudC1kaXJlY3RvcnknO1xuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVMYXN0TW9kaWZpZWQgPSAnZmlsZWJyb3dzZXI6dG9nZ2xlLWxhc3QtbW9kaWZpZWQnO1xuXG4gIGV4cG9ydCBjb25zdCBzZWFyY2ggPSAnZmlsZWJyb3dzZXI6c2VhcmNoJztcblxuICBleHBvcnQgY29uc3QgdG9nZ2xlSGlkZGVuRmlsZXMgPSAnZmlsZWJyb3dzZXI6dG9nZ2xlLWhpZGRlbi1maWxlcyc7XG59XG5cbi8qKlxuICogVGhlIGZpbGUgYnJvd3NlciBuYW1lc3BhY2UgdG9rZW4uXG4gKi9cbmNvbnN0IG5hbWVzcGFjZSA9ICdmaWxlYnJvd3Nlcic7XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgZmlsZSBicm93c2VyIGV4dGVuc2lvbi5cbiAqL1xuY29uc3QgYnJvd3NlcjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpicm93c2VyJyxcbiAgcmVxdWlyZXM6IFtJRmlsZUJyb3dzZXJGYWN0b3J5LCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbXG4gICAgSUxheW91dFJlc3RvcmVyLFxuICAgIElTZXR0aW5nUmVnaXN0cnksXG4gICAgSVRyZWVQYXRoVXBkYXRlcixcbiAgICBJQ29tbWFuZFBhbGV0dGVcbiAgXSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIGZhY3Rvcnk6IElGaWxlQnJvd3NlckZhY3RvcnksXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGwsXG4gICAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5IHwgbnVsbCxcbiAgICB0cmVlUGF0aFVwZGF0ZXI6IElUcmVlUGF0aFVwZGF0ZXIgfCBudWxsLFxuICAgIGNvbW1hbmRQYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4gICk6IFByb21pc2U8dm9pZD4gPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgYnJvd3NlciA9IGZhY3RvcnkuZGVmYXVsdEJyb3dzZXI7XG5cbiAgICAvLyBMZXQgdGhlIGFwcGxpY2F0aW9uIHJlc3RvcmVyIHRyYWNrIHRoZSBwcmltYXJ5IGZpbGUgYnJvd3NlciAodGhhdCBpc1xuICAgIC8vIGF1dG9tYXRpY2FsbHkgY3JlYXRlZCkgZm9yIHJlc3RvcmF0aW9uIG9mIGFwcGxpY2F0aW9uIHN0YXRlIChlLmcuIHNldHRpbmdcbiAgICAvLyB0aGUgZmlsZSBicm93c2VyIGFzIHRoZSBjdXJyZW50IHNpZGUgYmFyIHdpZGdldCkuXG4gICAgLy9cbiAgICAvLyBBbGwgb3RoZXIgZmlsZSBicm93c2VycyBjcmVhdGVkIGJ5IHVzaW5nIHRoZSBmYWN0b3J5IGZ1bmN0aW9uIGFyZVxuICAgIC8vIHJlc3BvbnNpYmxlIGZvciB0aGVpciBvd24gcmVzdG9yYXRpb24gYmVoYXZpb3IsIGlmIGFueS5cbiAgICBpZiAocmVzdG9yZXIpIHtcbiAgICAgIHJlc3RvcmVyLmFkZChicm93c2VyLCBuYW1lc3BhY2UpO1xuICAgIH1cblxuICAgIC8vIE5hdmlnYXRlIHRvIHByZWZlcnJlZC1kaXIgdHJhaXQgaWYgZm91bmRcbiAgICBjb25zdCBwcmVmZXJyZWRQYXRoID0gUGFnZUNvbmZpZy5nZXRPcHRpb24oJ3ByZWZlcnJlZFBhdGgnKTtcbiAgICBpZiAocHJlZmVycmVkUGF0aCkge1xuICAgICAgYXdhaXQgYnJvd3Nlci5tb2RlbC5jZChwcmVmZXJyZWRQYXRoKTtcbiAgICB9XG5cbiAgICBhZGRDb21tYW5kcyhhcHAsIGZhY3RvcnksIHRyYW5zbGF0b3IsIHNldHRpbmdSZWdpc3RyeSwgY29tbWFuZFBhbGV0dGUpO1xuXG4gICAgLy8gU2hvdyB0aGUgY3VycmVudCBmaWxlIGJyb3dzZXIgc2hvcnRjdXQgaW4gaXRzIHRpdGxlLlxuICAgIGNvbnN0IHVwZGF0ZUJyb3dzZXJUaXRsZSA9ICgpID0+IHtcbiAgICAgIGNvbnN0IGJpbmRpbmcgPSBmaW5kKFxuICAgICAgICBhcHAuY29tbWFuZHMua2V5QmluZGluZ3MsXG4gICAgICAgIGIgPT4gYi5jb21tYW5kID09PSBDb21tYW5kSURzLnRvZ2dsZUJyb3dzZXJcbiAgICAgICk7XG4gICAgICBpZiAoYmluZGluZykge1xuICAgICAgICBjb25zdCBrcyA9IENvbW1hbmRSZWdpc3RyeS5mb3JtYXRLZXlzdHJva2UoYmluZGluZy5rZXlzLmpvaW4oJyAnKSk7XG4gICAgICAgIGJyb3dzZXIudGl0bGUuY2FwdGlvbiA9IHRyYW5zLl9fKCdGaWxlIEJyb3dzZXIgKCUxKScsIGtzKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGJyb3dzZXIudGl0bGUuY2FwdGlvbiA9IHRyYW5zLl9fKCdGaWxlIEJyb3dzZXInKTtcbiAgICAgIH1cbiAgICB9O1xuICAgIHVwZGF0ZUJyb3dzZXJUaXRsZSgpO1xuICAgIGFwcC5jb21tYW5kcy5rZXlCaW5kaW5nQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHVwZGF0ZUJyb3dzZXJUaXRsZSgpO1xuICAgIH0pO1xuXG4gICAgdm9pZCBQcm9taXNlLmFsbChbYXBwLnJlc3RvcmVkLCBicm93c2VyLm1vZGVsLnJlc3RvcmVkXSkudGhlbigoKSA9PiB7XG4gICAgICBpZiAodHJlZVBhdGhVcGRhdGVyKSB7XG4gICAgICAgIGJyb3dzZXIubW9kZWwucGF0aENoYW5nZWQuY29ubmVjdCgoc2VuZGVyLCBhcmdzKSA9PiB7XG4gICAgICAgICAgdHJlZVBhdGhVcGRhdGVyKGFyZ3MubmV3VmFsdWUpO1xuICAgICAgICB9KTtcbiAgICAgIH1cblxuICAgICAgbGV0IG5hdmlnYXRlVG9DdXJyZW50RGlyZWN0b3J5OiBib29sZWFuID0gZmFsc2U7XG4gICAgICBsZXQgc2hvd0xhc3RNb2RpZmllZENvbHVtbjogYm9vbGVhbiA9IHRydWU7XG4gICAgICBsZXQgdXNlRnV6enlGaWx0ZXI6IGJvb2xlYW4gPSB0cnVlO1xuICAgICAgbGV0IHNob3dIaWRkZW5GaWxlczogYm9vbGVhbiA9IGZhbHNlO1xuXG4gICAgICBpZiAoc2V0dGluZ1JlZ2lzdHJ5KSB7XG4gICAgICAgIHZvaWQgc2V0dGluZ1JlZ2lzdHJ5XG4gICAgICAgICAgLmxvYWQoJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpicm93c2VyJylcbiAgICAgICAgICAudGhlbihzZXR0aW5ncyA9PiB7XG4gICAgICAgICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3Qoc2V0dGluZ3MgPT4ge1xuICAgICAgICAgICAgICBuYXZpZ2F0ZVRvQ3VycmVudERpcmVjdG9yeSA9IHNldHRpbmdzLmdldChcbiAgICAgICAgICAgICAgICAnbmF2aWdhdGVUb0N1cnJlbnREaXJlY3RvcnknXG4gICAgICAgICAgICAgICkuY29tcG9zaXRlIGFzIGJvb2xlYW47XG4gICAgICAgICAgICAgIGJyb3dzZXIubmF2aWdhdGVUb0N1cnJlbnREaXJlY3RvcnkgPSBuYXZpZ2F0ZVRvQ3VycmVudERpcmVjdG9yeTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgbmF2aWdhdGVUb0N1cnJlbnREaXJlY3RvcnkgPSBzZXR0aW5ncy5nZXQoXG4gICAgICAgICAgICAgICduYXZpZ2F0ZVRvQ3VycmVudERpcmVjdG9yeSdcbiAgICAgICAgICAgICkuY29tcG9zaXRlIGFzIGJvb2xlYW47XG4gICAgICAgICAgICBicm93c2VyLm5hdmlnYXRlVG9DdXJyZW50RGlyZWN0b3J5ID0gbmF2aWdhdGVUb0N1cnJlbnREaXJlY3Rvcnk7XG5cbiAgICAgICAgICAgIHNldHRpbmdzLmNoYW5nZWQuY29ubmVjdChzZXR0aW5ncyA9PiB7XG4gICAgICAgICAgICAgIHNob3dMYXN0TW9kaWZpZWRDb2x1bW4gPSBzZXR0aW5ncy5nZXQoJ3Nob3dMYXN0TW9kaWZpZWRDb2x1bW4nKVxuICAgICAgICAgICAgICAgIC5jb21wb3NpdGUgYXMgYm9vbGVhbjtcbiAgICAgICAgICAgICAgYnJvd3Nlci5zaG93TGFzdE1vZGlmaWVkQ29sdW1uID0gc2hvd0xhc3RNb2RpZmllZENvbHVtbjtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgc2hvd0xhc3RNb2RpZmllZENvbHVtbiA9IHNldHRpbmdzLmdldCgnc2hvd0xhc3RNb2RpZmllZENvbHVtbicpXG4gICAgICAgICAgICAgIC5jb21wb3NpdGUgYXMgYm9vbGVhbjtcblxuICAgICAgICAgICAgYnJvd3Nlci5zaG93TGFzdE1vZGlmaWVkQ29sdW1uID0gc2hvd0xhc3RNb2RpZmllZENvbHVtbjtcblxuICAgICAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KHNldHRpbmdzID0+IHtcbiAgICAgICAgICAgICAgdXNlRnV6enlGaWx0ZXIgPSBzZXR0aW5ncy5nZXQoJ3VzZUZ1enp5RmlsdGVyJylcbiAgICAgICAgICAgICAgICAuY29tcG9zaXRlIGFzIGJvb2xlYW47XG4gICAgICAgICAgICAgIGJyb3dzZXIudXNlRnV6enlGaWx0ZXIgPSB1c2VGdXp6eUZpbHRlcjtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgdXNlRnV6enlGaWx0ZXIgPSBzZXR0aW5ncy5nZXQoJ3VzZUZ1enp5RmlsdGVyJylcbiAgICAgICAgICAgICAgLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgICAgICAgYnJvd3Nlci51c2VGdXp6eUZpbHRlciA9IHVzZUZ1enp5RmlsdGVyO1xuXG4gICAgICAgICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3Qoc2V0dGluZ3MgPT4ge1xuICAgICAgICAgICAgICBzaG93SGlkZGVuRmlsZXMgPSBzZXR0aW5ncy5nZXQoJ3Nob3dIaWRkZW5GaWxlcycpXG4gICAgICAgICAgICAgICAgLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgICAgICAgICBicm93c2VyLnNob3dIaWRkZW5GaWxlcyA9IHNob3dIaWRkZW5GaWxlcztcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgc2hvd0hpZGRlbkZpbGVzID0gc2V0dGluZ3MuZ2V0KCdzaG93SGlkZGVuRmlsZXMnKVxuICAgICAgICAgICAgICAuY29tcG9zaXRlIGFzIGJvb2xlYW47XG5cbiAgICAgICAgICAgIGJyb3dzZXIuc2hvd0hpZGRlbkZpbGVzID0gc2hvd0hpZGRlbkZpbGVzO1xuICAgICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGZpbGUgYnJvd3NlciBmYWN0b3J5IHByb3ZpZGVyLlxuICovXG5jb25zdCBmYWN0b3J5OiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUZpbGVCcm93c2VyRmFjdG9yeT4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXItZXh0ZW5zaW9uOmZhY3RvcnknLFxuICBwcm92aWRlczogSUZpbGVCcm93c2VyRmFjdG9yeSxcbiAgcmVxdWlyZXM6IFtJRG9jdW1lbnRNYW5hZ2VyLCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSVN0YXRlREIsIElSb3V0ZXIsIEp1cHl0ZXJGcm9udEVuZC5JVHJlZVJlc29sdmVyXSxcbiAgYWN0aXZhdGU6IGFzeW5jIChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBkb2NNYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHN0YXRlOiBJU3RhdGVEQiB8IG51bGwsXG4gICAgcm91dGVyOiBJUm91dGVyIHwgbnVsbCxcbiAgICB0cmVlOiBKdXB5dGVyRnJvbnRFbmQuSVRyZWVSZXNvbHZlciB8IG51bGxcbiAgKTogUHJvbWlzZTxJRmlsZUJyb3dzZXJGYWN0b3J5PiA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IHRyYWNrZXIgPSBuZXcgV2lkZ2V0VHJhY2tlcjxGaWxlQnJvd3Nlcj4oeyBuYW1lc3BhY2UgfSk7XG4gICAgY29uc3QgY3JlYXRlRmlsZUJyb3dzZXIgPSAoXG4gICAgICBpZDogc3RyaW5nLFxuICAgICAgb3B0aW9uczogSUZpbGVCcm93c2VyRmFjdG9yeS5JT3B0aW9ucyA9IHt9XG4gICAgKSA9PiB7XG4gICAgICBjb25zdCBtb2RlbCA9IG5ldyBGaWx0ZXJGaWxlQnJvd3Nlck1vZGVsKHtcbiAgICAgICAgdHJhbnNsYXRvcjogdHJhbnNsYXRvcixcbiAgICAgICAgYXV0bzogb3B0aW9ucy5hdXRvID8/IHRydWUsXG4gICAgICAgIG1hbmFnZXI6IGRvY01hbmFnZXIsXG4gICAgICAgIGRyaXZlTmFtZTogb3B0aW9ucy5kcml2ZU5hbWUgfHwgJycsXG4gICAgICAgIHJlZnJlc2hJbnRlcnZhbDogb3B0aW9ucy5yZWZyZXNoSW50ZXJ2YWwsXG4gICAgICAgIHN0YXRlOlxuICAgICAgICAgIG9wdGlvbnMuc3RhdGUgPT09IG51bGxcbiAgICAgICAgICAgID8gdW5kZWZpbmVkXG4gICAgICAgICAgICA6IG9wdGlvbnMuc3RhdGUgfHwgc3RhdGUgfHwgdW5kZWZpbmVkXG4gICAgICB9KTtcbiAgICAgIGNvbnN0IHJlc3RvcmUgPSBvcHRpb25zLnJlc3RvcmU7XG4gICAgICBjb25zdCB3aWRnZXQgPSBuZXcgRmlsZUJyb3dzZXIoeyBpZCwgbW9kZWwsIHJlc3RvcmUsIHRyYW5zbGF0b3IgfSk7XG5cbiAgICAgIC8vIFRyYWNrIHRoZSBuZXdseSBjcmVhdGVkIGZpbGUgYnJvd3Nlci5cbiAgICAgIHZvaWQgdHJhY2tlci5hZGQod2lkZ2V0KTtcblxuICAgICAgcmV0dXJuIHdpZGdldDtcbiAgICB9O1xuXG4gICAgLy8gTWFudWFsbHkgcmVzdG9yZSBhbmQgbG9hZCB0aGUgZGVmYXVsdCBmaWxlIGJyb3dzZXIuXG4gICAgY29uc3QgZGVmYXVsdEJyb3dzZXIgPSBjcmVhdGVGaWxlQnJvd3NlcignZmlsZWJyb3dzZXInLCB7XG4gICAgICBhdXRvOiBmYWxzZSxcbiAgICAgIHJlc3RvcmU6IGZhbHNlXG4gICAgfSk7XG4gICAgdm9pZCBQcml2YXRlLnJlc3RvcmVCcm93c2VyKGRlZmF1bHRCcm93c2VyLCBjb21tYW5kcywgcm91dGVyLCB0cmVlKTtcblxuICAgIHJldHVybiB7IGNyZWF0ZUZpbGVCcm93c2VyLCBkZWZhdWx0QnJvd3NlciwgdHJhY2tlciB9O1xuICB9XG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHByb3ZpZGluZyBkb3dubG9hZCArIGNvcHkgZG93bmxvYWQgbGluayBjb21tYW5kcyBpbiB0aGUgY29udGV4dCBtZW51LlxuICpcbiAqIERpc2FibGluZyB0aGlzIHBsdWdpbiB3aWxsIE5PVCBkaXNhYmxlIGRvd25sb2FkaW5nIGZpbGVzIGZyb20gdGhlIHNlcnZlci5cbiAqIFVzZXJzIHdpbGwgc3RpbGwgYmUgYWJsZSB0byByZXRyaWV2ZSBmaWxlcyBmcm9tIHRoZSBmaWxlIGRvd25sb2FkIFVSTHMgdGhlXG4gKiBzZXJ2ZXIgcHJvdmlkZXMuXG4gKi9cbmNvbnN0IGRvd25sb2FkUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXItZXh0ZW5zaW9uOmRvd25sb2FkJyxcbiAgcmVxdWlyZXM6IFtJRmlsZUJyb3dzZXJGYWN0b3J5LCBJVHJhbnNsYXRvcl0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBmYWN0b3J5OiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IHsgdHJhY2tlciB9ID0gZmFjdG9yeTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5kb3dubG9hZCwge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICAgIHJldHVybiB3aWRnZXQuZG93bmxvYWQoKTtcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIGljb246IGRvd25sb2FkSWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdEb3dubG9hZCcpXG4gICAgfSk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY29weURvd25sb2FkTGluaywge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIHdpZGdldC5tb2RlbC5tYW5hZ2VyLnNlcnZpY2VzLmNvbnRlbnRzXG4gICAgICAgICAgLmdldERvd25sb2FkVXJsKHdpZGdldC5zZWxlY3RlZEl0ZW1zKCkubmV4dCgpIS5wYXRoKVxuICAgICAgICAgIC50aGVuKHVybCA9PiB7XG4gICAgICAgICAgICBDbGlwYm9hcmQuY29weVRvU3lzdGVtKHVybCk7XG4gICAgICAgICAgfSk7XG4gICAgICB9LFxuICAgICAgaWNvbjogY29weUljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnQ29weSBEb3dubG9hZCBMaW5rJyksXG4gICAgICBtbmVtb25pYzogMFxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHRvIGFkZCB0aGUgZmlsZSBicm93c2VyIHdpZGdldCB0byBhbiBJTGFiU2hlbGxcbiAqL1xuY29uc3QgYnJvd3NlcldpZGdldDogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjp3aWRnZXQnLFxuICByZXF1aXJlczogW0lEb2N1bWVudE1hbmFnZXIsIElGaWxlQnJvd3NlckZhY3RvcnksIElUcmFuc2xhdG9yLCBJTGFiU2hlbGxdLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcixcbiAgICBmYWN0b3J5OiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGxcbiAgKTogdm9pZCA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IHsgZGVmYXVsdEJyb3dzZXI6IGJyb3dzZXIsIHRyYWNrZXIgfSA9IGZhY3Rvcnk7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIC8vIFNldCBhdHRyaWJ1dGVzIHdoZW4gYWRkaW5nIHRoZSBicm93c2VyIHRvIHRoZSBVSVxuICAgIGJyb3dzZXIubm9kZS5zZXRBdHRyaWJ1dGUoJ3JvbGUnLCAncmVnaW9uJyk7XG4gICAgYnJvd3Nlci5ub2RlLnNldEF0dHJpYnV0ZSgnYXJpYS1sYWJlbCcsIHRyYW5zLl9fKCdGaWxlIEJyb3dzZXIgU2VjdGlvbicpKTtcbiAgICBicm93c2VyLnRpdGxlLmljb24gPSBmb2xkZXJTa0ljb247XG5cbiAgICBsYWJTaGVsbC5hZGQoYnJvd3NlciwgJ2xlZnQnLCB7IHJhbms6IDEwMCB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zaG93QnJvd3Nlciwge1xuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IHBhdGggPSAoYXJncy5wYXRoIGFzIHN0cmluZykgfHwgJyc7XG4gICAgICAgIGNvbnN0IGJyb3dzZXJGb3JQYXRoID0gUHJpdmF0ZS5nZXRCcm93c2VyRm9yUGF0aChwYXRoLCBmYWN0b3J5KTtcblxuICAgICAgICAvLyBDaGVjayBmb3IgYnJvd3NlciBub3QgZm91bmRcbiAgICAgICAgaWYgKCFicm93c2VyRm9yUGF0aCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICAvLyBTaG9ydGN1dCBpZiB3ZSBhcmUgdXNpbmcgdGhlIG1haW4gZmlsZSBicm93c2VyXG4gICAgICAgIGlmIChicm93c2VyID09PSBicm93c2VyRm9yUGF0aCkge1xuICAgICAgICAgIGxhYlNoZWxsLmFjdGl2YXRlQnlJZChicm93c2VyLmlkKTtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgY29uc3QgYXJlYXM6IElMYWJTaGVsbC5BcmVhW10gPSBbJ2xlZnQnLCAncmlnaHQnXTtcbiAgICAgICAgICBmb3IgKGNvbnN0IGFyZWEgb2YgYXJlYXMpIHtcbiAgICAgICAgICAgIGNvbnN0IGl0ID0gbGFiU2hlbGwud2lkZ2V0cyhhcmVhKTtcbiAgICAgICAgICAgIGxldCB3aWRnZXQgPSBpdC5uZXh0KCk7XG4gICAgICAgICAgICB3aGlsZSAod2lkZ2V0KSB7XG4gICAgICAgICAgICAgIGlmICh3aWRnZXQuY29udGFpbnMoYnJvd3NlckZvclBhdGgpKSB7XG4gICAgICAgICAgICAgICAgbGFiU2hlbGwuYWN0aXZhdGVCeUlkKHdpZGdldC5pZCk7XG4gICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIHdpZGdldCA9IGl0Lm5leHQoKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5oaWRlQnJvd3Nlciwge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIGlmICh3aWRnZXQgJiYgIXdpZGdldC5pc0hpZGRlbikge1xuICAgICAgICAgIGxhYlNoZWxsLmNvbGxhcHNlTGVmdCgpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBJZiB0aGUgbGF5b3V0IGlzIGEgZnJlc2ggc2Vzc2lvbiB3aXRob3V0IHNhdmVkIGRhdGEgYW5kIG5vdCBpbiBzaW5nbGUgZG9jdW1lbnRcbiAgICAvLyBtb2RlLCBvcGVuIGZpbGUgYnJvd3Nlci5cbiAgICB2b2lkIGxhYlNoZWxsLnJlc3RvcmVkLnRoZW4obGF5b3V0ID0+IHtcbiAgICAgIGlmIChsYXlvdXQuZnJlc2ggJiYgbGFiU2hlbGwubW9kZSAhPT0gJ3NpbmdsZS1kb2N1bWVudCcpIHtcbiAgICAgICAgdm9pZCBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMuc2hvd0Jyb3dzZXIsIHZvaWQgMCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICB2b2lkIFByb21pc2UuYWxsKFthcHAucmVzdG9yZWQsIGJyb3dzZXIubW9kZWwucmVzdG9yZWRdKS50aGVuKCgpID0+IHtcbiAgICAgIGZ1bmN0aW9uIG1heWJlQ3JlYXRlKCkge1xuICAgICAgICAvLyBDcmVhdGUgYSBsYXVuY2hlciBpZiB0aGVyZSBhcmUgbm8gb3BlbiBpdGVtcy5cbiAgICAgICAgaWYgKFxuICAgICAgICAgIGxhYlNoZWxsLmlzRW1wdHkoJ21haW4nKSAmJlxuICAgICAgICAgIGNvbW1hbmRzLmhhc0NvbW1hbmQoJ2xhdW5jaGVyOmNyZWF0ZScpXG4gICAgICAgICkge1xuICAgICAgICAgIHZvaWQgUHJpdmF0ZS5jcmVhdGVMYXVuY2hlcihjb21tYW5kcywgYnJvd3Nlcik7XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgLy8gV2hlbiBsYXlvdXQgaXMgbW9kaWZpZWQsIGNyZWF0ZSBhIGxhdW5jaGVyIGlmIHRoZXJlIGFyZSBubyBvcGVuIGl0ZW1zLlxuICAgICAgbGFiU2hlbGwubGF5b3V0TW9kaWZpZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgIG1heWJlQ3JlYXRlKCk7XG4gICAgICB9KTtcblxuICAgICAgLy8gV2hldGhlciB0byBhdXRvbWF0aWNhbGx5IG5hdmlnYXRlIHRvIGEgZG9jdW1lbnQncyBjdXJyZW50IGRpcmVjdG9yeVxuICAgICAgbGFiU2hlbGwuY3VycmVudENoYW5nZWQuY29ubmVjdChhc3luYyAoXywgY2hhbmdlKSA9PiB7XG4gICAgICAgIGlmIChicm93c2VyLm5hdmlnYXRlVG9DdXJyZW50RGlyZWN0b3J5ICYmIGNoYW5nZS5uZXdWYWx1ZSkge1xuICAgICAgICAgIGNvbnN0IHsgbmV3VmFsdWUgfSA9IGNoYW5nZTtcbiAgICAgICAgICBjb25zdCBjb250ZXh0ID0gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KG5ld1ZhbHVlKTtcbiAgICAgICAgICBpZiAoY29udGV4dCkge1xuICAgICAgICAgICAgY29uc3QgeyBwYXRoIH0gPSBjb250ZXh0O1xuICAgICAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgICAgYXdhaXQgUHJpdmF0ZS5uYXZpZ2F0ZVRvUGF0aChwYXRoLCBmYWN0b3J5LCB0cmFuc2xhdG9yKTtcbiAgICAgICAgICAgIH0gY2F0Y2ggKHJlYXNvbikge1xuICAgICAgICAgICAgICBjb25zb2xlLndhcm4oXG4gICAgICAgICAgICAgICAgYCR7Q29tbWFuZElEcy5nb1RvUGF0aH0gZmFpbGVkIHRvIG9wZW46ICR7cGF0aH1gLFxuICAgICAgICAgICAgICAgIHJlYXNvblxuICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIG1heWJlQ3JlYXRlKCk7XG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgZmlsZSBicm93c2VyIHNoYXJlLWZpbGUgcGx1Z2luXG4gKlxuICogVGhpcyBleHRlbnNpb24gYWRkcyBhIFwiQ29weSBTaGFyZWFibGUgTGlua1wiIGNvbW1hbmQgdGhhdCBnZW5lcmF0ZXMgYSBjb3B5LVxuICogcGFzdGFibGUgVVJMLiBUaGlzIHVybCBjYW4gYmUgdXNlZCB0byBvcGVuIGEgcGFydGljdWxhciBmaWxlIGluIEp1cHl0ZXJMYWIsXG4gKiBoYW5keSBmb3IgZW1haWxpbmcgbGlua3Mgb3IgYm9va21hcmtpbmcgZm9yIHJlZmVyZW5jZS5cbiAqXG4gKiBJZiB5b3UgbmVlZCB0byBjaGFuZ2UgaG93IHRoaXMgbGluayBpcyBnZW5lcmF0ZWQgKGZvciBpbnN0YW5jZSwgdG8gY29weSBhXG4gKiAvdXNlci1yZWRpcmVjdCBVUkwgZm9yIEp1cHl0ZXJIdWIpLCBkaXNhYmxlIHRoaXMgcGx1Z2luIGFuZCByZXBsYWNlIGl0XG4gKiB3aXRoIGFub3RoZXIgaW1wbGVtZW50YXRpb24uXG4gKi9cbmNvbnN0IHNoYXJlRmlsZTogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpzaGFyZS1maWxlJyxcbiAgcmVxdWlyZXM6IFtJRmlsZUJyb3dzZXJGYWN0b3J5LCBJVHJhbnNsYXRvcl0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBmYWN0b3J5OiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IHsgdHJhY2tlciB9ID0gZmFjdG9yeTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb3B5U2hhcmVhYmxlTGluaywge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIGNvbnN0IG1vZGVsID0gd2lkZ2V0Py5zZWxlY3RlZEl0ZW1zKCkubmV4dCgpO1xuICAgICAgICBpZiAoIW1vZGVsKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgQ2xpcGJvYXJkLmNvcHlUb1N5c3RlbShcbiAgICAgICAgICBQYWdlQ29uZmlnLmdldFVybCh7XG4gICAgICAgICAgICB3b3Jrc3BhY2U6IFBhZ2VDb25maWcuZGVmYXVsdFdvcmtzcGFjZSxcbiAgICAgICAgICAgIHRyZWVQYXRoOiBtb2RlbC5wYXRoLFxuICAgICAgICAgICAgdG9TaGFyZTogdHJ1ZVxuICAgICAgICAgIH0pXG4gICAgICAgICk7XG4gICAgICB9LFxuICAgICAgaXNWaXNpYmxlOiAoKSA9PlxuICAgICAgICAhIXRyYWNrZXIuY3VycmVudFdpZGdldCAmJlxuICAgICAgICB0b0FycmF5KHRyYWNrZXIuY3VycmVudFdpZGdldC5zZWxlY3RlZEl0ZW1zKCkpLmxlbmd0aCA9PT0gMSxcbiAgICAgIGljb246IGxpbmtJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0NvcHkgU2hhcmVhYmxlIExpbmsnKVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBcIk9wZW4gV2l0aFwiIGNvbnRleHQgbWVudS5cbiAqXG4gKiBUaGlzIGlzIGl0cyBvd24gcGx1Z2luIGluIGNhc2UgeW91IHdvdWxkIGxpa2UgdG8gZGlzYWJsZSB0aGlzIGZlYXR1cmUuXG4gKiBlLmcuIGp1cHl0ZXIgbGFiZXh0ZW5zaW9uIGRpc2FibGUgQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXItZXh0ZW5zaW9uOm9wZW4td2l0aFxuICovXG5jb25zdCBvcGVuV2l0aFBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpvcGVuLXdpdGgnLFxuICByZXF1aXJlczogW0lGaWxlQnJvd3NlckZhY3RvcnldLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQsIGZhY3Rvcnk6IElGaWxlQnJvd3NlckZhY3RvcnkpOiB2b2lkID0+IHtcbiAgICBjb25zdCB7IGRvY1JlZ2lzdHJ5IH0gPSBhcHA7XG4gICAgY29uc3QgeyB0cmFja2VyIH0gPSBmYWN0b3J5O1xuXG4gICAgZnVuY3Rpb24gdXBkYXRlT3BlbldpdGhNZW51KGNvbnRleHRNZW51OiBDb250ZXh0TWVudSkge1xuICAgICAgY29uc3Qgb3BlbldpdGggPVxuICAgICAgICBjb250ZXh0TWVudS5tZW51Lml0ZW1zLmZpbmQoXG4gICAgICAgICAgaXRlbSA9PlxuICAgICAgICAgICAgaXRlbS50eXBlID09PSAnc3VibWVudScgJiZcbiAgICAgICAgICAgIGl0ZW0uc3VibWVudT8uaWQgPT09ICdqcC1jb250ZXh0bWVudS1vcGVuLXdpdGgnXG4gICAgICAgICk/LnN1Ym1lbnUgPz8gbnVsbDtcblxuICAgICAgaWYgKCFvcGVuV2l0aCkge1xuICAgICAgICByZXR1cm47IC8vIEJhaWwgZWFybHkgaWYgdGhlIG9wZW4gd2l0aCBtZW51IGlzIG5vdCBkaXNwbGF5ZWRcbiAgICAgIH1cblxuICAgICAgLy8gY2xlYXIgdGhlIGN1cnJlbnQgbWVudSBpdGVtc1xuICAgICAgb3BlbldpdGguY2xlYXJJdGVtcygpO1xuXG4gICAgICAvLyBnZXQgdGhlIHdpZGdldCBmYWN0b3JpZXMgdGhhdCBjb3VsZCBiZSB1c2VkIHRvIG9wZW4gYWxsIG9mIHRoZSBpdGVtc1xuICAgICAgLy8gaW4gdGhlIGN1cnJlbnQgZmlsZWJyb3dzZXIgc2VsZWN0aW9uXG4gICAgICBjb25zdCBmYWN0b3JpZXMgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXRcbiAgICAgICAgPyBQcml2YXRlLk9wZW5XaXRoLmludGVyc2VjdGlvbjxzdHJpbmc+KFxuICAgICAgICAgICAgbWFwKHRyYWNrZXIuY3VycmVudFdpZGdldC5zZWxlY3RlZEl0ZW1zKCksIGkgPT4ge1xuICAgICAgICAgICAgICByZXR1cm4gUHJpdmF0ZS5PcGVuV2l0aC5nZXRGYWN0b3JpZXMoZG9jUmVnaXN0cnksIGkpO1xuICAgICAgICAgICAgfSlcbiAgICAgICAgICApXG4gICAgICAgIDogbmV3IFNldDxzdHJpbmc+KCk7XG5cbiAgICAgIC8vIG1ha2UgbmV3IG1lbnUgaXRlbXMgZnJvbSB0aGUgd2lkZ2V0IGZhY3Rvcmllc1xuICAgICAgZmFjdG9yaWVzLmZvckVhY2goZmFjdG9yeSA9PiB7XG4gICAgICAgIG9wZW5XaXRoLmFkZEl0ZW0oe1xuICAgICAgICAgIGFyZ3M6IHsgZmFjdG9yeTogZmFjdG9yeSB9LFxuICAgICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMub3BlblxuICAgICAgICB9KTtcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGFwcC5jb250ZXh0TWVudS5vcGVuZWQuY29ubmVjdCh1cGRhdGVPcGVuV2l0aE1lbnUpO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBcIk9wZW4gaW4gTmV3IEJyb3dzZXIgVGFiXCIgY29udGV4dCBtZW51LlxuICpcbiAqIFRoaXMgaXMgaXRzIG93biBwbHVnaW4gaW4gY2FzZSB5b3Ugd291bGQgbGlrZSB0byBkaXNhYmxlIHRoaXMgZmVhdHVyZS5cbiAqIGUuZy4ganVweXRlciBsYWJleHRlbnNpb24gZGlzYWJsZSBAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246b3Blbi1icm93c2VyLXRhYlxuICpcbiAqIE5vdGU6IElmIGRpc2FibGluZyB0aGlzLCB5b3UgbWF5IGFsc28gd2FudCB0byBkaXNhYmxlOlxuICogQGp1cHl0ZXJsYWIvZG9jbWFuYWdlci1leHRlbnNpb246b3Blbi1icm93c2VyLXRhYlxuICovXG5jb25zdCBvcGVuQnJvd3NlclRhYlBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpvcGVuLWJyb3dzZXItdGFiJyxcbiAgcmVxdWlyZXM6IFtJRmlsZUJyb3dzZXJGYWN0b3J5LCBJVHJhbnNsYXRvcl0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBmYWN0b3J5OiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHsgdHJhY2tlciB9ID0gZmFjdG9yeTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuQnJvd3NlclRhYiwge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4gUHJvbWlzZS5hbGwoXG4gICAgICAgICAgdG9BcnJheShcbiAgICAgICAgICAgIG1hcCh3aWRnZXQuc2VsZWN0ZWRJdGVtcygpLCBpdGVtID0+IHtcbiAgICAgICAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoJ2RvY21hbmFnZXI6b3Blbi1icm93c2VyLXRhYicsIHtcbiAgICAgICAgICAgICAgICBwYXRoOiBpdGVtLnBhdGhcbiAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICB9KVxuICAgICAgICAgIClcbiAgICAgICAgKTtcbiAgICAgIH0sXG4gICAgICBpY29uOiBza0FkZEljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnT3BlbiBpbiBOZXcgQnJvd3NlciBUYWInKSxcbiAgICAgIG1uZW1vbmljOiAwXG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gcHJvdmlkaW5nIGZpbGUgdXBsb2FkIHN0YXR1cy5cbiAqL1xuZXhwb3J0IGNvbnN0IGZpbGVVcGxvYWRTdGF0dXM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246ZmlsZS11cGxvYWQtc3RhdHVzJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lGaWxlQnJvd3NlckZhY3RvcnksIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJU3RhdHVzQmFyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBicm93c2VyOiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHN0YXR1c0JhcjogSVN0YXR1c0JhciB8IG51bGxcbiAgKSA9PiB7XG4gICAgaWYgKCFzdGF0dXNCYXIpIHtcbiAgICAgIC8vIEF1dG9tYXRpY2FsbHkgZGlzYWJsZSBpZiBzdGF0dXNiYXIgbWlzc2luZ1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBpdGVtID0gbmV3IEZpbGVVcGxvYWRTdGF0dXMoe1xuICAgICAgdHJhY2tlcjogYnJvd3Nlci50cmFja2VyLFxuICAgICAgdHJhbnNsYXRvclxuICAgIH0pO1xuXG4gICAgc3RhdHVzQmFyLnJlZ2lzdGVyU3RhdHVzSXRlbShcbiAgICAgICdAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246ZmlsZS11cGxvYWQtc3RhdHVzJyxcbiAgICAgIHtcbiAgICAgICAgaXRlbSxcbiAgICAgICAgYWxpZ246ICdtaWRkbGUnLFxuICAgICAgICBpc0FjdGl2ZTogKCkgPT4ge1xuICAgICAgICAgIHJldHVybiAhIWl0ZW0ubW9kZWwgJiYgaXRlbS5tb2RlbC5pdGVtcy5sZW5ndGggPiAwO1xuICAgICAgICB9LFxuICAgICAgICBhY3RpdmVTdGF0ZUNoYW5nZWQ6IGl0ZW0ubW9kZWwuc3RhdGVDaGFuZ2VkXG4gICAgICB9XG4gICAgKTtcbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0byBhZGQgYSBsYXVuY2hlciBidXR0b24gdG8gdGhlIGZpbGUgYnJvd3NlciB0b29sYmFyXG4gKi9cbmV4cG9ydCBjb25zdCBsYXVuY2hlclRvb2xiYXJCdXR0b246IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246bGF1bmNoZXItdG9vbGJhci1idXR0b24nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSUZpbGVCcm93c2VyRmFjdG9yeSwgSVRyYW5zbGF0b3JdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIGZhY3Rvcnk6IElGaWxlQnJvd3NlckZhY3RvcnksXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKSA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBkZWZhdWx0QnJvd3NlcjogYnJvd3NlciB9ID0gZmFjdG9yeTtcblxuICAgIC8vIEFkZCBhIGxhdW5jaGVyIHRvb2xiYXIgaXRlbS5cbiAgICBjb25zdCBsYXVuY2hlciA9IG5ldyBUb29sYmFyQnV0dG9uKHtcbiAgICAgIGljb246IHNrQWRkSWNvbixcbiAgICAgIG9uQ2xpY2s6ICgpID0+IHtcbiAgICAgICAgaWYgKGNvbW1hbmRzLmhhc0NvbW1hbmQoJ2xhdW5jaGVyOmNyZWF0ZScpKSB7XG4gICAgICAgICAgcmV0dXJuIFByaXZhdGUuY3JlYXRlTGF1bmNoZXIoY29tbWFuZHMsIGJyb3dzZXIpO1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAgdG9vbHRpcDogdHJhbnMuX18oJ05ldyBMYXVuY2hlcicpLFxuICAgICAgYWN0dWFsT25DbGljazogdHJ1ZVxuICAgIH0pO1xuICAgIGJyb3dzZXIudG9vbGJhci5pbnNlcnRJdGVtKDAsICdsYXVuY2gnLCBsYXVuY2hlcik7XG4gIH1cbn07XG5cbi8qKlxuICogQWRkIHRoZSBtYWluIGZpbGUgYnJvd3NlciBjb21tYW5kcyB0byB0aGUgYXBwbGljYXRpb24ncyBjb21tYW5kIHJlZ2lzdHJ5LlxuICovXG5mdW5jdGlvbiBhZGRDb21tYW5kcyhcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIGZhY3Rvcnk6IElGaWxlQnJvd3NlckZhY3RvcnksXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsLFxuICBjb21tYW5kUGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuKTogdm9pZCB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgZG9jUmVnaXN0cnk6IHJlZ2lzdHJ5LCBjb21tYW5kcyB9ID0gYXBwO1xuICBjb25zdCB7IGRlZmF1bHRCcm93c2VyOiBicm93c2VyLCB0cmFja2VyIH0gPSBmYWN0b3J5O1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5kZWwsIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5kZWxldGUoKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGljb246IGNsb3NlSWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgIGxhYmVsOiB0cmFucy5fXygnRGVsZXRlJyksXG4gICAgbW5lbW9uaWM6IDBcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNvcHksIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5jb3B5KCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpY29uOiBjb3B5SWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgIGxhYmVsOiB0cmFucy5fXygnQ29weScpLFxuICAgIG1uZW1vbmljOiAwXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jdXQsIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5jdXQoKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGljb246IGN1dEljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ0N1dCcpXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5kdXBsaWNhdGUsIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5kdXBsaWNhdGUoKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGljb246IGNvcHlJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdEdXBsaWNhdGUnKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuZ29Ub1BhdGgsIHtcbiAgICBleGVjdXRlOiBhc3luYyBhcmdzID0+IHtcbiAgICAgIGNvbnN0IHBhdGggPSAoYXJncy5wYXRoIGFzIHN0cmluZykgfHwgJyc7XG4gICAgICBjb25zdCBzaG93QnJvd3NlciA9ICEoYXJncz8uZG9udFNob3dCcm93c2VyID8/IGZhbHNlKTtcbiAgICAgIHRyeSB7XG4gICAgICAgIGNvbnN0IGl0ZW0gPSBhd2FpdCBQcml2YXRlLm5hdmlnYXRlVG9QYXRoKHBhdGgsIGZhY3RvcnksIHRyYW5zbGF0b3IpO1xuICAgICAgICBpZiAoaXRlbS50eXBlICE9PSAnZGlyZWN0b3J5JyAmJiBzaG93QnJvd3Nlcikge1xuICAgICAgICAgIGNvbnN0IGJyb3dzZXJGb3JQYXRoID0gUHJpdmF0ZS5nZXRCcm93c2VyRm9yUGF0aChwYXRoLCBmYWN0b3J5KTtcbiAgICAgICAgICBpZiAoYnJvd3NlckZvclBhdGgpIHtcbiAgICAgICAgICAgIGJyb3dzZXJGb3JQYXRoLmNsZWFyU2VsZWN0ZWRJdGVtcygpO1xuICAgICAgICAgICAgY29uc3QgcGFydHMgPSBwYXRoLnNwbGl0KCcvJyk7XG4gICAgICAgICAgICBjb25zdCBuYW1lID0gcGFydHNbcGFydHMubGVuZ3RoIC0gMV07XG4gICAgICAgICAgICBpZiAobmFtZSkge1xuICAgICAgICAgICAgICBhd2FpdCBicm93c2VyRm9yUGF0aC5zZWxlY3RJdGVtQnlOYW1lKG5hbWUpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSBjYXRjaCAocmVhc29uKSB7XG4gICAgICAgIGNvbnNvbGUud2FybihgJHtDb21tYW5kSURzLmdvVG9QYXRofSBmYWlsZWQgdG8gZ28gdG86ICR7cGF0aH1gLCByZWFzb24pO1xuICAgICAgfVxuICAgICAgaWYgKHNob3dCcm93c2VyKSB7XG4gICAgICAgIHJldHVybiBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMuc2hvd0Jyb3dzZXIsIHsgcGF0aCB9KTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5nb1VwLCB7XG4gICAgbGFiZWw6ICdnbyB1cCcsXG4gICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3QgYnJvd3NlckZvclBhdGggPSBQcml2YXRlLmdldEJyb3dzZXJGb3JQYXRoKCcnLCBmYWN0b3J5KTtcbiAgICAgIGlmICghYnJvd3NlckZvclBhdGgpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgeyBtb2RlbCB9ID0gYnJvd3NlckZvclBhdGg7XG5cbiAgICAgIGF3YWl0IG1vZGVsLnJlc3RvcmVkO1xuICAgICAgaWYgKG1vZGVsLnBhdGggPT09IG1vZGVsLnJvb3RQYXRoKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHRyeSB7XG4gICAgICAgIGF3YWl0IG1vZGVsLmNkKCcuLicpO1xuICAgICAgfSBjYXRjaCAocmVhc29uKSB7XG4gICAgICAgIGNvbnNvbGUud2FybihcbiAgICAgICAgICBgJHtDb21tYW5kSURzLmdvVXB9IGZhaWxlZCB0byBnbyB0byBwYXJlbnQgZGlyZWN0b3J5IG9mICR7bW9kZWwucGF0aH1gLFxuICAgICAgICAgIHJlYXNvblxuICAgICAgICApO1xuICAgICAgfVxuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW5QYXRoLCB7XG4gICAgbGFiZWw6IGFyZ3MgPT5cbiAgICAgIGFyZ3MucGF0aCA/IHRyYW5zLl9fKCdPcGVuICUxJywgYXJncy5wYXRoKSA6IHRyYW5zLl9fKCdPcGVuIGZyb20gUGF0aOKApicpLFxuICAgIGNhcHRpb246IGFyZ3MgPT5cbiAgICAgIGFyZ3MucGF0aCA/IHRyYW5zLl9fKCdPcGVuICUxJywgYXJncy5wYXRoKSA6IHRyYW5zLl9fKCdPcGVuIGZyb20gcGF0aCcpLFxuICAgIGV4ZWN1dGU6IGFzeW5jIGFyZ3MgPT4ge1xuICAgICAgbGV0IHBhdGg6IHN0cmluZyB8IHVuZGVmaW5lZDtcbiAgICAgIGlmIChhcmdzPy5wYXRoKSB7XG4gICAgICAgIHBhdGggPSBhcmdzLnBhdGggYXMgc3RyaW5nO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcGF0aCA9XG4gICAgICAgICAgKFxuICAgICAgICAgICAgYXdhaXQgSW5wdXREaWFsb2cuZ2V0VGV4dCh7XG4gICAgICAgICAgICAgIGxhYmVsOiB0cmFucy5fXygnUGF0aCcpLFxuICAgICAgICAgICAgICBwbGFjZWhvbGRlcjogJy9wYXRoL3JlbGF0aXZlL3RvL2psYWIvcm9vdCcsXG4gICAgICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnT3BlbiBQYXRoJyksXG4gICAgICAgICAgICAgIG9rTGFiZWw6IHRyYW5zLl9fKCdPcGVuJylcbiAgICAgICAgICAgIH0pXG4gICAgICAgICAgKS52YWx1ZSA/PyB1bmRlZmluZWQ7XG4gICAgICB9XG4gICAgICBpZiAoIXBhdGgpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc3QgdHJhaWxpbmdTbGFzaCA9IHBhdGggIT09ICcvJyAmJiBwYXRoLmVuZHNXaXRoKCcvJyk7XG4gICAgICAgIGlmICh0cmFpbGluZ1NsYXNoKSB7XG4gICAgICAgICAgLy8gVGhlIG5vcm1hbCBjb250ZW50cyBzZXJ2aWNlIGVycm9ycyBvbiBwYXRocyBlbmRpbmcgaW4gc2xhc2hcbiAgICAgICAgICBwYXRoID0gcGF0aC5zbGljZSgwLCBwYXRoLmxlbmd0aCAtIDEpO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IGJyb3dzZXJGb3JQYXRoID0gUHJpdmF0ZS5nZXRCcm93c2VyRm9yUGF0aChwYXRoLCBmYWN0b3J5KSE7XG4gICAgICAgIGNvbnN0IHsgc2VydmljZXMgfSA9IGJyb3dzZXJGb3JQYXRoLm1vZGVsLm1hbmFnZXI7XG4gICAgICAgIGNvbnN0IGl0ZW0gPSBhd2FpdCBzZXJ2aWNlcy5jb250ZW50cy5nZXQocGF0aCwge1xuICAgICAgICAgIGNvbnRlbnQ6IGZhbHNlXG4gICAgICAgIH0pO1xuICAgICAgICBpZiAodHJhaWxpbmdTbGFzaCAmJiBpdGVtLnR5cGUgIT09ICdkaXJlY3RvcnknKSB7XG4gICAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBQYXRoICR7cGF0aH0vIGlzIG5vdCBhIGRpcmVjdG9yeWApO1xuICAgICAgICB9XG4gICAgICAgIGF3YWl0IGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5nb1RvUGF0aCwge1xuICAgICAgICAgIHBhdGgsXG4gICAgICAgICAgZG9udFNob3dCcm93c2VyOiBhcmdzLmRvbnRTaG93QnJvd3NlclxuICAgICAgICB9KTtcbiAgICAgICAgaWYgKGl0ZW0udHlwZSA9PT0gJ2RpcmVjdG9yeScpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoJ2RvY21hbmFnZXI6b3BlbicsIHsgcGF0aCB9KTtcbiAgICAgIH0gY2F0Y2ggKHJlYXNvbikge1xuICAgICAgICBpZiAocmVhc29uLnJlc3BvbnNlICYmIHJlYXNvbi5yZXNwb25zZS5zdGF0dXMgPT09IDQwNCkge1xuICAgICAgICAgIHJlYXNvbi5tZXNzYWdlID0gdHJhbnMuX18oJ0NvdWxkIG5vdCBmaW5kIHBhdGg6ICUxJywgcGF0aCk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHNob3dFcnJvck1lc3NhZ2UodHJhbnMuX18oJ0Nhbm5vdCBvcGVuJyksIHJlYXNvbik7XG4gICAgICB9XG4gICAgfVxuICB9KTtcbiAgLy8gQWRkIHRoZSBvcGVuUGF0aCBjb21tYW5kIHRvIHRoZSBjb21tYW5kIHBhbGV0dGVcbiAgaWYgKGNvbW1hbmRQYWxldHRlKSB7XG4gICAgY29tbWFuZFBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLm9wZW5QYXRoLFxuICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdGaWxlIE9wZXJhdGlvbnMnKVxuICAgIH0pO1xuICB9XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW4sIHtcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGZhY3RvcnkgPSAoYXJnc1snZmFjdG9yeSddIGFzIHN0cmluZykgfHwgdm9pZCAwO1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IHsgY29udGVudHMgfSA9IHdpZGdldC5tb2RlbC5tYW5hZ2VyLnNlcnZpY2VzO1xuICAgICAgcmV0dXJuIFByb21pc2UuYWxsKFxuICAgICAgICB0b0FycmF5KFxuICAgICAgICAgIG1hcCh3aWRnZXQuc2VsZWN0ZWRJdGVtcygpLCBpdGVtID0+IHtcbiAgICAgICAgICAgIGlmIChpdGVtLnR5cGUgPT09ICdkaXJlY3RvcnknKSB7XG4gICAgICAgICAgICAgIGNvbnN0IGxvY2FsUGF0aCA9IGNvbnRlbnRzLmxvY2FsUGF0aChpdGVtLnBhdGgpO1xuICAgICAgICAgICAgICByZXR1cm4gd2lkZ2V0Lm1vZGVsLmNkKGAvJHtsb2NhbFBhdGh9YCk7XG4gICAgICAgICAgICB9XG5cbiAgICAgICAgICAgIHJldHVybiBjb21tYW5kcy5leGVjdXRlKCdkb2NtYW5hZ2VyOm9wZW4nLCB7XG4gICAgICAgICAgICAgIGZhY3Rvcnk6IGZhY3RvcnksXG4gICAgICAgICAgICAgIHBhdGg6IGl0ZW0ucGF0aFxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfSlcbiAgICAgICAgKVxuICAgICAgKTtcbiAgICB9LFxuICAgIGljb246IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgZmFjdG9yeSA9IChhcmdzWydmYWN0b3J5J10gYXMgc3RyaW5nKSB8fCB2b2lkIDA7XG4gICAgICBpZiAoZmFjdG9yeSkge1xuICAgICAgICAvLyBpZiBhbiBleHBsaWNpdCBmYWN0b3J5IGlzIHBhc3NlZC4uLlxuICAgICAgICBjb25zdCBmdCA9IHJlZ2lzdHJ5LmdldEZpbGVUeXBlKGZhY3RvcnkpO1xuICAgICAgICAvLyAuLi5zZXQgYW4gaWNvbiBpZiB0aGUgZmFjdG9yeSBuYW1lIGNvcnJlc3BvbmRzIHRvIGEgZmlsZSB0eXBlIG5hbWUuLi5cbiAgICAgICAgLy8gLi4ub3IgbGVhdmUgdGhlIGljb24gYmxhbmtcbiAgICAgICAgcmV0dXJuIGZ0Py5pY29uPy5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIGZvbGRlclNrSWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pO1xuICAgICAgfVxuICAgIH0sXG4gICAgLy8gRklYTUUtVFJBTlM6IElzIHRoaXMgbG9jYWxpemFibGU/XG4gICAgbGFiZWw6IGFyZ3MgPT5cbiAgICAgIChhcmdzWydsYWJlbCddIHx8IGFyZ3NbJ2ZhY3RvcnknXSB8fCB0cmFucy5fXygnT3BlbicpKSBhcyBzdHJpbmcsXG4gICAgbW5lbW9uaWM6IDBcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnBhc3RlLCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICBpZiAod2lkZ2V0KSB7XG4gICAgICAgIHJldHVybiB3aWRnZXQucGFzdGUoKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGljb246IHBhc3RlSWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgIGxhYmVsOiB0cmFucy5fXygnUGFzdGUnKSxcbiAgICBtbmVtb25pYzogMFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY3JlYXRlTmV3RGlyZWN0b3J5LCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICBpZiAod2lkZ2V0KSB7XG4gICAgICAgIHJldHVybiB3aWRnZXQuY3JlYXRlTmV3RGlyZWN0b3J5KCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpY29uOiBuZXdGb2xkZXJJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdOZXcgRm9sZGVyJylcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNyZWF0ZU5ld0ZpbGUsIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5jcmVhdGVOZXdGaWxlKHsgZXh0OiAndHh0JyB9KTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGljb246IHRleHRFZGl0b3JJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdOZXcgRmlsZScpXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jcmVhdGVOZXdNYXJrZG93bkZpbGUsIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5jcmVhdGVOZXdGaWxlKHsgZXh0OiAnbWQnIH0pO1xuICAgICAgfVxuICAgIH0sXG4gICAgaWNvbjogbWFya2Rvd25JY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdOZXcgTWFya2Rvd24gRmlsZScpXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZW5hbWUsIHtcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcblxuICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICByZXR1cm4gd2lkZ2V0LnJlbmFtZSgpO1xuICAgICAgfVxuICAgIH0sXG4gICAgaWNvbjogZWRpdEljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ1JlbmFtZScpLFxuICAgIG1uZW1vbmljOiAwXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb3B5UGF0aCwge1xuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGl0ZW0gPSB3aWRnZXQuc2VsZWN0ZWRJdGVtcygpLm5leHQoKTtcbiAgICAgIGlmICghaXRlbSkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIENsaXBib2FyZC5jb3B5VG9TeXN0ZW0oaXRlbS5wYXRoKTtcbiAgICB9LFxuICAgIGlzVmlzaWJsZTogKCkgPT5cbiAgICAgICEhdHJhY2tlci5jdXJyZW50V2lkZ2V0ICYmXG4gICAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQuc2VsZWN0ZWRJdGVtcygpLm5leHQgIT09IHVuZGVmaW5lZCxcbiAgICBpY29uOiBmaWxlSWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgIGxhYmVsOiB0cmFucy5fXygnQ29weSBQYXRoJylcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNodXRkb3duLCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICBpZiAod2lkZ2V0KSB7XG4gICAgICAgIHJldHVybiB3aWRnZXQuc2h1dGRvd25LZXJuZWxzKCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpY29uOiBzdG9wSWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgIGxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duIEtlcm5lbCcpXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVCcm93c2VyLCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgaWYgKGJyb3dzZXIuaXNIaWRkZW4pIHtcbiAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5zaG93QnJvd3Nlciwgdm9pZCAwKTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5oaWRlQnJvd3Nlciwgdm9pZCAwKTtcbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jcmVhdGVMYXVuY2hlciwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnTmV3IExhdW5jaGVyJyksXG4gICAgZXhlY3V0ZTogKCkgPT4gUHJpdmF0ZS5jcmVhdGVMYXVuY2hlcihjb21tYW5kcywgYnJvd3NlcilcbiAgfSk7XG5cbiAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVOYXZpZ2F0ZVRvQ3VycmVudERpcmVjdG9yeSwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdTaG93IEFjdGl2ZSBGaWxlIGluIEZpbGUgQnJvd3NlcicpLFxuICAgICAgaXNUb2dnbGVkOiAoKSA9PiBicm93c2VyLm5hdmlnYXRlVG9DdXJyZW50RGlyZWN0b3J5LFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB2YWx1ZSA9ICFicm93c2VyLm5hdmlnYXRlVG9DdXJyZW50RGlyZWN0b3J5O1xuICAgICAgICBjb25zdCBrZXkgPSAnbmF2aWdhdGVUb0N1cnJlbnREaXJlY3RvcnknO1xuICAgICAgICByZXR1cm4gc2V0dGluZ1JlZ2lzdHJ5XG4gICAgICAgICAgLnNldCgnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXItZXh0ZW5zaW9uOmJyb3dzZXInLCBrZXksIHZhbHVlKVxuICAgICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCBuYXZpZ2F0ZVRvQ3VycmVudERpcmVjdG9yeSBzZXR0aW5nYCk7XG4gICAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMudG9nZ2xlTGFzdE1vZGlmaWVkLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdTaG93IExhc3QgTW9kaWZpZWQgQ29sdW1uJyksXG4gICAgaXNUb2dnbGVkOiAoKSA9PiBicm93c2VyLnNob3dMYXN0TW9kaWZpZWRDb2x1bW4sXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3QgdmFsdWUgPSAhYnJvd3Nlci5zaG93TGFzdE1vZGlmaWVkQ29sdW1uO1xuICAgICAgY29uc3Qga2V5ID0gJ3Nob3dMYXN0TW9kaWZpZWRDb2x1bW4nO1xuICAgICAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgICAgICByZXR1cm4gc2V0dGluZ1JlZ2lzdHJ5XG4gICAgICAgICAgLnNldCgnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXItZXh0ZW5zaW9uOmJyb3dzZXInLCBrZXksIHZhbHVlKVxuICAgICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCBzaG93TGFzdE1vZGlmaWVkQ29sdW1uIHNldHRpbmdgKTtcbiAgICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVIaWRkZW5GaWxlcywge1xuICAgIGxhYmVsOiB0cmFucy5fXygnU2hvdyBIaWRkZW4gRmlsZXMnKSxcbiAgICBpc1RvZ2dsZWQ6ICgpID0+IGJyb3dzZXIuc2hvd0hpZGRlbkZpbGVzLFxuICAgIGlzVmlzaWJsZTogKCkgPT4gUGFnZUNvbmZpZy5nZXRPcHRpb24oJ2FsbG93X2hpZGRlbl9maWxlcycpID09PSAndHJ1ZScsXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3QgdmFsdWUgPSAhYnJvd3Nlci5zaG93SGlkZGVuRmlsZXM7XG4gICAgICBjb25zdCBrZXkgPSAnc2hvd0hpZGRlbkZpbGVzJztcbiAgICAgIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICAgICAgcmV0dXJuIHNldHRpbmdSZWdpc3RyeVxuICAgICAgICAgIC5zZXQoJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpicm93c2VyJywga2V5LCB2YWx1ZSlcbiAgICAgICAgICAuY2F0Y2goKHJlYXNvbjogRXJyb3IpID0+IHtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoYEZhaWxlZCB0byBzZXQgc2hvd0hpZGRlbkZpbGVzIHNldHRpbmdgKTtcbiAgICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zZWFyY2gsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1NlYXJjaCBvbiBGaWxlIE5hbWVzJyksXG4gICAgZXhlY3V0ZTogKCkgPT4gYWxlcnQoJ3NlYXJjaCcpXG4gIH0pO1xuXG4gIGlmIChjb21tYW5kUGFsZXR0ZSkge1xuICAgIGNvbW1hbmRQYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy50b2dnbGVOYXZpZ2F0ZVRvQ3VycmVudERpcmVjdG9yeSxcbiAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnRmlsZSBPcGVyYXRpb25zJylcbiAgICB9KTtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIG1vZHVsZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBsYXVuY2hlciBmb3IgYSBnaXZlbiBmaWxlYnJvd3NlciB3aWRnZXQuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gY3JlYXRlTGF1bmNoZXIoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICBicm93c2VyOiBGaWxlQnJvd3NlclxuICApOiBQcm9taXNlPE1haW5BcmVhV2lkZ2V0PExhdW5jaGVyPj4ge1xuICAgIGNvbnN0IHsgbW9kZWwgfSA9IGJyb3dzZXI7XG5cbiAgICByZXR1cm4gY29tbWFuZHNcbiAgICAgIC5leGVjdXRlKCdsYXVuY2hlcjpjcmVhdGUnLCB7IGN3ZDogbW9kZWwucGF0aCB9KVxuICAgICAgLnRoZW4oKGxhdW5jaGVyOiBNYWluQXJlYVdpZGdldDxMYXVuY2hlcj4pID0+IHtcbiAgICAgICAgbW9kZWwucGF0aENoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgICAgaWYgKGxhdW5jaGVyLmNvbnRlbnQpIHtcbiAgICAgICAgICAgIGxhdW5jaGVyLmNvbnRlbnQuY3dkID0gbW9kZWwucGF0aDtcbiAgICAgICAgICB9XG4gICAgICAgIH0sIGxhdW5jaGVyKTtcbiAgICAgICAgcmV0dXJuIGxhdW5jaGVyO1xuICAgICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGJyb3dzZXIgb2JqZWN0IGdpdmVuIGZpbGUgcGF0aC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBnZXRCcm93c2VyRm9yUGF0aChcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgZmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeVxuICApOiBGaWxlQnJvd3NlciB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3QgeyBkZWZhdWx0QnJvd3NlcjogYnJvd3NlciwgdHJhY2tlciB9ID0gZmFjdG9yeTtcbiAgICBjb25zdCBkcml2ZU5hbWUgPSBicm93c2VyLm1vZGVsLm1hbmFnZXIuc2VydmljZXMuY29udGVudHMuZHJpdmVOYW1lKHBhdGgpO1xuXG4gICAgaWYgKGRyaXZlTmFtZSkge1xuICAgICAgY29uc3QgYnJvd3NlckZvclBhdGggPSB0cmFja2VyLmZpbmQoXG4gICAgICAgIF9wYXRoID0+IF9wYXRoLm1vZGVsLmRyaXZlTmFtZSA9PT0gZHJpdmVOYW1lXG4gICAgICApO1xuXG4gICAgICBpZiAoIWJyb3dzZXJGb3JQYXRoKSB7XG4gICAgICAgIC8vIHdhcm4gdGhhdCBubyBmaWxlYnJvd3NlciBjb3VsZCBiZSBmb3VuZCBmb3IgdGhpcyBkcml2ZU5hbWVcbiAgICAgICAgY29uc29sZS53YXJuKFxuICAgICAgICAgIGAke0NvbW1hbmRJRHMuZ29Ub1BhdGh9IGZhaWxlZCB0byBmaW5kIGZpbGVicm93c2VyIGZvciBwYXRoOiAke3BhdGh9YFxuICAgICAgICApO1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBicm93c2VyRm9yUGF0aDtcbiAgICB9XG5cbiAgICAvLyBpZiBkcml2ZU5hbWUgaXMgZW1wdHksIGFzc3VtZSB0aGUgbWFpbiBmaWxlYnJvd3NlclxuICAgIHJldHVybiBicm93c2VyO1xuICB9XG5cbiAgLyoqXG4gICAqIE5hdmlnYXRlIHRvIGEgcGF0aCBvciB0aGUgcGF0aCBjb250YWluaW5nIGEgZmlsZS5cbiAgICovXG4gIGV4cG9ydCBhc3luYyBmdW5jdGlvbiBuYXZpZ2F0ZVRvUGF0aChcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgZmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApOiBQcm9taXNlPENvbnRlbnRzLklNb2RlbD4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgYnJvd3NlckZvclBhdGggPSBQcml2YXRlLmdldEJyb3dzZXJGb3JQYXRoKHBhdGgsIGZhY3RvcnkpO1xuICAgIGlmICghYnJvd3NlckZvclBhdGgpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcih0cmFucy5fXygnTm8gYnJvd3NlciBmb3IgcGF0aCcpKTtcbiAgICB9XG4gICAgY29uc3QgeyBzZXJ2aWNlcyB9ID0gYnJvd3NlckZvclBhdGgubW9kZWwubWFuYWdlcjtcbiAgICBjb25zdCBsb2NhbFBhdGggPSBzZXJ2aWNlcy5jb250ZW50cy5sb2NhbFBhdGgocGF0aCk7XG5cbiAgICBhd2FpdCBzZXJ2aWNlcy5yZWFkeTtcbiAgICBjb25zdCBpdGVtID0gYXdhaXQgc2VydmljZXMuY29udGVudHMuZ2V0KHBhdGgsIHsgY29udGVudDogZmFsc2UgfSk7XG4gICAgY29uc3QgeyBtb2RlbCB9ID0gYnJvd3NlckZvclBhdGg7XG4gICAgYXdhaXQgbW9kZWwucmVzdG9yZWQ7XG4gICAgaWYgKGl0ZW0udHlwZSA9PT0gJ2RpcmVjdG9yeScpIHtcbiAgICAgIGF3YWl0IG1vZGVsLmNkKGAvJHtsb2NhbFBhdGh9YCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIGF3YWl0IG1vZGVsLmNkKGAvJHtQYXRoRXh0LmRpcm5hbWUobG9jYWxQYXRoKX1gKTtcbiAgICB9XG4gICAgcmV0dXJuIGl0ZW07XG4gIH1cblxuICAvKipcbiAgICogUmVzdG9yZXMgZmlsZSBicm93c2VyIHN0YXRlIGFuZCBvdmVycmlkZXMgc3RhdGUgaWYgdHJlZSByZXNvbHZlciByZXNvbHZlcy5cbiAgICovXG4gIGV4cG9ydCBhc3luYyBmdW5jdGlvbiByZXN0b3JlQnJvd3NlcihcbiAgICBicm93c2VyOiBGaWxlQnJvd3NlcixcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIHJvdXRlcjogSVJvdXRlciB8IG51bGwsXG4gICAgdHJlZTogSnVweXRlckZyb250RW5kLklUcmVlUmVzb2x2ZXIgfCBudWxsXG4gICk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IHJlc3RvcmluZyA9ICdqcC1tb2QtcmVzdG9yaW5nJztcblxuICAgIGJyb3dzZXIuYWRkQ2xhc3MocmVzdG9yaW5nKTtcblxuICAgIGlmICghcm91dGVyKSB7XG4gICAgICBhd2FpdCBicm93c2VyLm1vZGVsLnJlc3RvcmUoYnJvd3Nlci5pZCk7XG4gICAgICBhd2FpdCBicm93c2VyLm1vZGVsLnJlZnJlc2goKTtcbiAgICAgIGJyb3dzZXIucmVtb3ZlQ2xhc3MocmVzdG9yaW5nKTtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCBsaXN0ZW5lciA9IGFzeW5jICgpID0+IHtcbiAgICAgIHJvdXRlci5yb3V0ZWQuZGlzY29ubmVjdChsaXN0ZW5lcik7XG5cbiAgICAgIGNvbnN0IHBhdGhzID0gYXdhaXQgdHJlZT8ucGF0aHM7XG4gICAgICBpZiAocGF0aHM/LmZpbGUgfHwgcGF0aHM/LmJyb3dzZXIpIHtcbiAgICAgICAgLy8gUmVzdG9yZSB0aGUgbW9kZWwgd2l0aG91dCBwb3B1bGF0aW5nIGl0LlxuICAgICAgICBhd2FpdCBicm93c2VyLm1vZGVsLnJlc3RvcmUoYnJvd3Nlci5pZCwgZmFsc2UpO1xuICAgICAgICBpZiAocGF0aHMuZmlsZSkge1xuICAgICAgICAgIGF3YWl0IGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5vcGVuUGF0aCwge1xuICAgICAgICAgICAgcGF0aDogcGF0aHMuZmlsZSxcbiAgICAgICAgICAgIGRvbnRTaG93QnJvd3NlcjogdHJ1ZVxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG4gICAgICAgIGlmIChwYXRocy5icm93c2VyKSB7XG4gICAgICAgICAgYXdhaXQgY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLm9wZW5QYXRoLCB7XG4gICAgICAgICAgICBwYXRoOiBwYXRocy5icm93c2VyLFxuICAgICAgICAgICAgZG9udFNob3dCcm93c2VyOiB0cnVlXG4gICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGF3YWl0IGJyb3dzZXIubW9kZWwucmVzdG9yZShicm93c2VyLmlkKTtcbiAgICAgICAgYXdhaXQgYnJvd3Nlci5tb2RlbC5yZWZyZXNoKCk7XG4gICAgICB9XG4gICAgICBicm93c2VyLnJlbW92ZUNsYXNzKHJlc3RvcmluZyk7XG4gICAgfTtcbiAgICByb3V0ZXIucm91dGVkLmNvbm5lY3QobGlzdGVuZXIpO1xuICB9XG59XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbXG4gIGZhY3RvcnksXG4gIGJyb3dzZXIsXG4gIHNoYXJlRmlsZSxcbiAgZmlsZVVwbG9hZFN0YXR1cyxcbiAgZG93bmxvYWRQbHVnaW4sXG4gIGJyb3dzZXJXaWRnZXQsXG4gIGxhdW5jaGVyVG9vbGJhckJ1dHRvbixcbiAgb3BlbldpdGhQbHVnaW4sXG4gIG9wZW5Ccm93c2VyVGFiUGx1Z2luXG5dO1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcblxubmFtZXNwYWNlIFByaXZhdGUge1xuICBleHBvcnQgbmFtZXNwYWNlIE9wZW5XaXRoIHtcbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIGZhY3RvcmllcyBmb3IgdGhlIHNlbGVjdGVkIGl0ZW1cbiAgICAgKlxuICAgICAqIEBwYXJhbSBkb2NSZWdpc3RyeSBBcHBsaWNhdGlvbiBkb2N1bWVudCByZWdpc3RyeVxuICAgICAqIEBwYXJhbSBpdGVtIFNlbGVjdGVkIGl0ZW0gbW9kZWxcbiAgICAgKiBAcmV0dXJucyBBdmFpbGFibGUgZmFjdG9yaWVzIGZvciB0aGUgbW9kZWxcbiAgICAgKi9cbiAgICBleHBvcnQgZnVuY3Rpb24gZ2V0RmFjdG9yaWVzKFxuICAgICAgZG9jUmVnaXN0cnk6IERvY3VtZW50UmVnaXN0cnksXG4gICAgICBpdGVtOiBDb250ZW50cy5JTW9kZWxcbiAgICApOiBBcnJheTxzdHJpbmc+IHtcbiAgICAgIGNvbnN0IGZhY3RvcmllcyA9IGRvY1JlZ2lzdHJ5XG4gICAgICAgIC5wcmVmZXJyZWRXaWRnZXRGYWN0b3JpZXMoaXRlbS5wYXRoKVxuICAgICAgICAubWFwKGYgPT4gZi5uYW1lKTtcbiAgICAgIGNvbnN0IG5vdGVib29rRmFjdG9yeSA9IGRvY1JlZ2lzdHJ5LmdldFdpZGdldEZhY3RvcnkoJ25vdGVib29rJyk/Lm5hbWU7XG4gICAgICBpZiAoXG4gICAgICAgIG5vdGVib29rRmFjdG9yeSAmJlxuICAgICAgICBpdGVtLnR5cGUgPT09ICdub3RlYm9vaycgJiZcbiAgICAgICAgZmFjdG9yaWVzLmluZGV4T2Yobm90ZWJvb2tGYWN0b3J5KSA9PT0gLTFcbiAgICAgICkge1xuICAgICAgICBmYWN0b3JpZXMudW5zaGlmdChub3RlYm9va0ZhY3RvcnkpO1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gZmFjdG9yaWVzO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJldHVybiB0aGUgaW50ZXJzZWN0aW9uIG9mIG11bHRpcGxlIGFycmF5cy5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBpdGVyIEl0ZXJhdG9yIG9mIGFycmF5c1xuICAgICAqIEByZXR1cm5zIFNldCBvZiBjb21tb24gZWxlbWVudHMgdG8gYWxsIGFycmF5c1xuICAgICAqL1xuICAgIGV4cG9ydCBmdW5jdGlvbiBpbnRlcnNlY3Rpb248VD4oaXRlcjogSUl0ZXJhdG9yPEFycmF5PFQ+Pik6IFNldDxUPiB7XG4gICAgICAvLyBwb3AgdGhlIGZpcnN0IGVsZW1lbnQgb2YgaXRlclxuICAgICAgY29uc3QgZmlyc3QgPSBpdGVyLm5leHQoKTtcbiAgICAgIC8vIGZpcnN0IHdpbGwgYmUgdW5kZWZpbmVkIGlmIGl0ZXIgaXMgZW1wdHlcbiAgICAgIGlmICghZmlyc3QpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBTZXQ8VD4oKTtcbiAgICAgIH1cblxuICAgICAgLy8gXCJpbml0aWFsaXplXCIgdGhlIGludGVyc2VjdGlvbiBmcm9tIGZpcnN0XG4gICAgICBjb25zdCBpc2VjdCA9IG5ldyBTZXQoZmlyc3QpO1xuICAgICAgLy8gcmVkdWNlIG92ZXIgdGhlIHJlbWFpbmluZyBlbGVtZW50cyBvZiBpdGVyXG4gICAgICByZXR1cm4gcmVkdWNlKFxuICAgICAgICBpdGVyLFxuICAgICAgICAoaXNlY3QsIHN1YmFycikgPT4ge1xuICAgICAgICAgIC8vIGZpbHRlciBvdXQgYWxsIGVsZW1lbnRzIG5vdCBwcmVzZW50IGluIGJvdGggaXNlY3QgYW5kIHN1YmFycixcbiAgICAgICAgICAvLyBhY2N1bXVsYXRlIHJlc3VsdCBpbiBuZXcgc2V0XG4gICAgICAgICAgcmV0dXJuIG5ldyBTZXQoc3ViYXJyLmZpbHRlcih4ID0+IGlzZWN0Lmhhcyh4KSkpO1xuICAgICAgICB9LFxuICAgICAgICBpc2VjdFxuICAgICAgKTtcbiAgICB9XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0=