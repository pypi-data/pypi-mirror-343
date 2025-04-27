(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_docmanager-extension_lib_index_js"],{

/***/ "../packages/docmanager-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/docmanager-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "savingStatusPlugin": () => (/* binding */ savingStatusPlugin),
/* harmony export */   "pathStatusPlugin": () => (/* binding */ pathStatusPlugin),
/* harmony export */   "downloadPlugin": () => (/* binding */ downloadPlugin),
/* harmony export */   "openBrowserTabPlugin": () => (/* binding */ openBrowserTabPlugin),
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
/* harmony import */ var _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/docprovider */ "webpack/sharing/consume/default/@jupyterlab/docprovider/@jupyterlab/docprovider");
/* harmony import */ var _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_10__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module docmanager-extension
 */











/**
 * The command IDs used by the document manager plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.clone = 'docmanager:clone';
    CommandIDs.deleteFile = 'docmanager:delete-file';
    CommandIDs.newUntitled = 'docmanager:new-untitled';
    CommandIDs.open = 'docmanager:open';
    CommandIDs.openBrowserTab = 'docmanager:open-browser-tab';
    CommandIDs.reload = 'docmanager:reload';
    CommandIDs.rename = 'docmanager:rename';
    CommandIDs.del = 'docmanager:delete';
    CommandIDs.restoreCheckpoint = 'docmanager:restore-checkpoint';
    CommandIDs.save = 'docmanager:save';
    CommandIDs.saveAll = 'docmanager:save-all';
    CommandIDs.saveAs = 'docmanager:save-as';
    CommandIDs.download = 'docmanager:download';
    CommandIDs.toggleAutosave = 'docmanager:toggle-autosave';
    CommandIDs.showInFileBrowser = 'docmanager:show-in-file-browser';
})(CommandIDs || (CommandIDs = {}));
/**
 * The id of the document manager plugin.
 */
const docManagerPluginId = '@jupyterlab/docmanager-extension:plugin';
/**
 * The default document manager provider.
 */
const docManagerPlugin = {
    id: docManagerPluginId,
    provides: _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs,
        _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_4__.IDocumentProviderFactory
    ],
    activate: (app, settingRegistry, translator, status, palette, labShell, sessionDialogs, docProviderFactory) => {
        var _a;
        const trans = translator.load('jupyterlab');
        const manager = app.serviceManager;
        const contexts = new WeakSet();
        const opener = {
            open: (widget, options) => {
                if (!widget.id) {
                    widget.id = `document-manager-${++Private.id}`;
                }
                widget.title.dataset = Object.assign({ type: 'document-title' }, widget.title.dataset);
                if (!widget.isAttached) {
                    app.shell.add(widget, 'main', options || {});
                }
                app.shell.activateById(widget.id);
                // Handle dirty state for open documents.
                const context = docManager.contextForWidget(widget);
                if (context && !contexts.has(context)) {
                    if (status) {
                        handleContext(status, context);
                    }
                    contexts.add(context);
                }
            }
        };
        const registry = app.docRegistry;
        const when = app.restored.then(() => void 0);
        const docManager = new _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.DocumentManager({
            registry,
            manager,
            opener,
            when,
            setBusy: (_a = (status && (() => status.setBusy()))) !== null && _a !== void 0 ? _a : undefined,
            sessionDialogs: sessionDialogs || undefined,
            translator,
            collaborative: true,
            docProviderFactory: docProviderFactory !== null && docProviderFactory !== void 0 ? docProviderFactory : undefined
        });
        // Register the file operations commands.
        addCommands(app, docManager, opener, settingRegistry, translator, labShell, palette);
        // Keep up to date with the settings registry.
        const onSettingsUpdated = (settings) => {
            // Handle whether to autosave
            const autosave = settings.get('autosave').composite;
            docManager.autosave =
                autosave === true || autosave === false ? autosave : true;
            app.commands.notifyCommandChanged(CommandIDs.toggleAutosave);
            // Handle autosave interval
            const autosaveInterval = settings.get('autosaveInterval').composite;
            docManager.autosaveInterval = autosaveInterval || 120;
            // Handle last modified timestamp check margin
            const lastModifiedCheckMargin = settings.get('lastModifiedCheckMargin')
                .composite;
            docManager.lastModifiedCheckMargin = lastModifiedCheckMargin || 500;
            // Handle default widget factory overrides.
            const defaultViewers = settings.get('defaultViewers').composite;
            const overrides = {};
            // Filter the defaultViewers and file types for existing ones.
            Object.keys(defaultViewers).forEach(ft => {
                if (!registry.getFileType(ft)) {
                    console.warn(`File Type ${ft} not found`);
                    return;
                }
                if (!registry.getWidgetFactory(defaultViewers[ft])) {
                    console.warn(`Document viewer ${defaultViewers[ft]} not found`);
                }
                overrides[ft] = defaultViewers[ft];
            });
            // Set the default factory overrides. If not provided, this has the
            // effect of unsetting any previous overrides.
            (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.each)(registry.fileTypes(), ft => {
                try {
                    registry.setDefaultWidgetFactory(ft.name, overrides[ft.name]);
                }
                catch (_a) {
                    console.warn(`Failed to set default viewer ${overrides[ft.name]} for file type ${ft.name}`);
                }
            });
        };
        // Fetch the initial state of the settings.
        Promise.all([settingRegistry.load(docManagerPluginId), app.restored])
            .then(([settings]) => {
            settings.changed.connect(onSettingsUpdated);
            onSettingsUpdated(settings);
        })
            .catch((reason) => {
            console.error(reason.message);
        });
        // Register a fetch transformer for the settings registry,
        // allowing us to dynamically populate a help string with the
        // available document viewers and file types for the default
        // viewer overrides.
        settingRegistry.transform(docManagerPluginId, {
            fetch: plugin => {
                // Get the available file types.
                const fileTypes = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.toArray)(registry.fileTypes())
                    .map(ft => ft.name)
                    .join('    \n');
                // Get the available widget factories.
                const factories = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.toArray)(registry.widgetFactories())
                    .map(f => f.name)
                    .join('    \n');
                // Generate the help string.
                const description = trans.__(`Overrides for the default viewers for file types.
Specify a mapping from file type name to document viewer name, for example:

defaultViewers: {
  markdown: "Markdown Preview"
}

If you specify non-existent file types or viewers, or if a viewer cannot
open a given file type, the override will not function.

Available viewers:
%1

Available file types:
%2`, factories, fileTypes);
                const schema = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(plugin.schema);
                schema.properties.defaultViewers.description = description;
                return Object.assign(Object.assign({}, plugin), { schema });
            }
        });
        // If the document registry gains or loses a factory or file type,
        // regenerate the settings description with the available options.
        registry.changed.connect(() => settingRegistry.reload(docManagerPluginId));
        return docManager;
    }
};
/**
 * A plugin for adding a saving status item to the status bar.
 */
const savingStatusPlugin = {
    id: '@jupyterlab/docmanager-extension:saving-status',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.IStatusBar],
    activate: (_, docManager, labShell, translator, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const saving = new _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.SavingStatus({ docManager, translator });
        // Keep the currently active widget synchronized.
        saving.model.widget = labShell.currentWidget;
        labShell.currentChanged.connect(() => {
            saving.model.widget = labShell.currentWidget;
        });
        statusBar.registerStatusItem(savingStatusPlugin.id, {
            item: saving,
            align: 'middle',
            isActive: () => saving.model !== null && saving.model.status !== null,
            activeStateChanged: saving.model.stateChanged
        });
    }
};
/**
 * A plugin providing a file path widget to the status bar.
 */
const pathStatusPlugin = {
    id: '@jupyterlab/docmanager-extension:path-status',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.IStatusBar],
    activate: (_, docManager, labShell, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const path = new _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.PathStatus({ docManager });
        // Keep the file path widget up-to-date with the application active widget.
        path.model.widget = labShell.currentWidget;
        labShell.currentChanged.connect(() => {
            path.model.widget = labShell.currentWidget;
        });
        statusBar.registerStatusItem(pathStatusPlugin.id, {
            item: path,
            align: 'right',
            rank: 0
        });
    }
};
/**
 * A plugin providing download commands in the file menu and command palette.
 */
const downloadPlugin = {
    id: '@jupyterlab/docmanager-extension:download',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, docManager, palette) => {
        const trans = translator.load('jupyterlab');
        const { commands, shell } = app;
        const isEnabled = () => {
            const { currentWidget } = shell;
            return !!(currentWidget && docManager.contextForWidget(currentWidget));
        };
        commands.addCommand(CommandIDs.download, {
            label: trans.__('Download'),
            caption: trans.__('Download the file to your computer'),
            isEnabled,
            execute: () => {
                // Checks that shell.currentWidget is valid:
                if (isEnabled()) {
                    const context = docManager.contextForWidget(shell.currentWidget);
                    if (!context) {
                        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title: trans.__('Cannot Download'),
                            body: trans.__('No context found for current widget!'),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('OK') })]
                        });
                    }
                    return context.download();
                }
            }
        });
        const category = trans.__('File Operations');
        if (palette) {
            palette.addItem({ command: CommandIDs.download, category });
        }
    }
};
/**
 * A plugin providing open-browser-tab commands.
 *
 * This is its own plugin in case you would like to disable this feature.
 * e.g. jupyter labextension disable @jupyterlab/docmanager-extension:open-browser-tab
 *
 * Note: If disabling this, you may also want to disable:
 * @jupyterlab/filebrowser-extension:open-browser-tab
 */
const openBrowserTabPlugin = {
    id: '@jupyterlab/docmanager-extension:open-browser-tab',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager],
    activate: (app, translator, docManager) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        commands.addCommand(CommandIDs.openBrowserTab, {
            execute: args => {
                const path = typeof args['path'] === 'undefined' ? '' : args['path'];
                if (!path) {
                    return;
                }
                return docManager.services.contents.getDownloadUrl(path).then(url => {
                    const opened = window.open();
                    if (opened) {
                        opened.opener = null;
                        opened.location.href = url;
                    }
                    else {
                        throw new Error('Failed to open new browser tab.');
                    }
                });
            },
            icon: args => args['icon'] || '',
            label: () => trans.__('Open in New Browser Tab')
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    docManagerPlugin,
    pathStatusPlugin,
    savingStatusPlugin,
    downloadPlugin,
    openBrowserTabPlugin
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/* Widget to display the revert to checkpoint confirmation. */
class RevertConfirmWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__.Widget {
    /**
     * Construct a new revert confirmation widget.
     */
    constructor(checkpoint, trans, fileType = 'notebook') {
        super({
            node: Private.createRevertConfirmNode(checkpoint, fileType, trans)
        });
    }
}
// Returns the file type for a widget.
function fileType(widget, docManager) {
    if (!widget) {
        return 'File';
    }
    const context = docManager.contextForWidget(widget);
    if (!context) {
        return '';
    }
    const fts = docManager.registry.getFileTypesForPath(context.path);
    return fts.length && fts[0].displayName ? fts[0].displayName : 'File';
}
/**
 * Add the file operations commands to the application's command registry.
 */
function addCommands(app, docManager, opener, settingRegistry, translator, labShell, palette) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const category = trans.__('File Operations');
    const isEnabled = () => {
        const { currentWidget } = shell;
        return !!(currentWidget && docManager.contextForWidget(currentWidget));
    };
    const isWritable = () => {
        const { currentWidget } = shell;
        if (!currentWidget) {
            return false;
        }
        const context = docManager.contextForWidget(currentWidget);
        return !!(context &&
            context.contentsModel &&
            context.contentsModel.writable);
    };
    // If inside a rich application like JupyterLab, add additional functionality.
    if (labShell) {
        addLabCommands(app, docManager, labShell, opener, translator);
    }
    commands.addCommand(CommandIDs.deleteFile, {
        label: () => `Delete ${fileType(shell.currentWidget, docManager)}`,
        execute: args => {
            const path = typeof args['path'] === 'undefined' ? '' : args['path'];
            if (!path) {
                const command = CommandIDs.deleteFile;
                throw new Error(`A non-empty path is required for ${command}.`);
            }
            return docManager.deleteFile(path);
        }
    });
    commands.addCommand(CommandIDs.newUntitled, {
        execute: args => {
            // FIXME-TRANS: Localizing args['error']?
            const errorTitle = args['error'] || trans.__('Error');
            const path = typeof args['path'] === 'undefined' ? '' : args['path'];
            const options = {
                type: args['type'],
                path
            };
            if (args['type'] === 'file') {
                options.ext = args['ext'] || '.txt';
            }
            return docManager.services.contents
                .newUntitled(options)
                .catch(error => (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(errorTitle, error));
        },
        label: args => args['label'] || `New ${args['type']}`
    });
    commands.addCommand(CommandIDs.open, {
        execute: args => {
            const path = typeof args['path'] === 'undefined' ? '' : args['path'];
            const factory = args['factory'] || void 0;
            const kernel = args === null || args === void 0 ? void 0 : args.kernel;
            const options = args['options'] || void 0;
            return docManager.services.contents
                .get(path, { content: false })
                .then(() => docManager.openOrReveal(path, factory, kernel, options));
        },
        icon: args => args['icon'] || '',
        label: args => (args['label'] || args['factory']),
        mnemonic: args => args['mnemonic'] || -1
    });
    commands.addCommand(CommandIDs.reload, {
        label: () => trans.__('Reload %1 from Disk', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Reload contents from disk'),
        isEnabled,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (!isEnabled()) {
                return;
            }
            const context = docManager.contextForWidget(shell.currentWidget);
            const type = fileType(shell.currentWidget, docManager);
            if (!context) {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Cannot Reload'),
                    body: trans.__('No context found for current widget!'),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Ok') })]
                });
            }
            if (context.model.dirty) {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Reload %1 from Disk', type),
                    body: trans.__('Are you sure you want to reload the %1 from the disk?', type),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Cancel') }),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Reload') })
                    ]
                }).then(result => {
                    if (result.button.accept && !context.isDisposed) {
                        return context.revert();
                    }
                });
            }
            else {
                if (!context.isDisposed) {
                    return context.revert();
                }
            }
        }
    });
    commands.addCommand(CommandIDs.restoreCheckpoint, {
        label: () => trans.__('Revert %1 to Checkpoint', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Revert contents to previous checkpoint'),
        isEnabled,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (!isEnabled()) {
                return;
            }
            const context = docManager.contextForWidget(shell.currentWidget);
            if (!context) {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Cannot Revert'),
                    body: trans.__('No context found for current widget!'),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Ok') })]
                });
            }
            return context.listCheckpoints().then(checkpoints => {
                if (checkpoints.length < 1) {
                    return;
                }
                const lastCheckpoint = checkpoints[checkpoints.length - 1];
                if (!lastCheckpoint) {
                    return;
                }
                const type = fileType(shell.currentWidget, docManager);
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Revert %1 to checkpoint', type),
                    body: new RevertConfirmWidget(lastCheckpoint, trans, type),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Cancel') }),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Revert') })
                    ]
                }).then(result => {
                    if (context.isDisposed) {
                        return;
                    }
                    if (result.button.accept) {
                        if (context.model.readOnly) {
                            return context.revert();
                        }
                        return context.restoreCheckpoint().then(() => context.revert());
                    }
                });
            });
        }
    });
    commands.addCommand(CommandIDs.save, {
        label: () => trans.__('Save %1', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Save and create checkpoint'),
        isEnabled: isWritable,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (isEnabled()) {
                const context = docManager.contextForWidget(shell.currentWidget);
                if (!context) {
                    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                        title: trans.__('Cannot Save'),
                        body: trans.__('No context found for current widget!'),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Ok') })]
                    });
                }
                else {
                    if (context.model.readOnly) {
                        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title: trans.__('Cannot Save'),
                            body: trans.__('Document is read-only'),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Ok') })]
                        });
                    }
                    return context
                        .save()
                        .then(() => context.createCheckpoint())
                        .catch(err => {
                        // If the save was canceled by user-action, do nothing.
                        // FIXME-TRANS: Is this using the text on the button or?
                        if (err.message === 'Cancel') {
                            return;
                        }
                        throw err;
                    });
                }
            }
        }
    });
    commands.addCommand(CommandIDs.saveAll, {
        label: () => trans.__('Save All'),
        caption: trans.__('Save all open documents'),
        isEnabled: () => {
            return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.some)((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.map)(shell.widgets('main'), w => docManager.contextForWidget(w)), c => { var _a, _b; return (_b = (_a = c === null || c === void 0 ? void 0 : c.contentsModel) === null || _a === void 0 ? void 0 : _a.writable) !== null && _b !== void 0 ? _b : false; });
        },
        execute: () => {
            const promises = [];
            const paths = new Set(); // Cache so we don't double save files.
            (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.each)(shell.widgets('main'), widget => {
                const context = docManager.contextForWidget(widget);
                if (context && !context.model.readOnly && !paths.has(context.path)) {
                    paths.add(context.path);
                    promises.push(context.save());
                }
            });
            return Promise.all(promises);
        }
    });
    commands.addCommand(CommandIDs.saveAs, {
        label: () => trans.__('Save %1 As…', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Save with new path'),
        isEnabled,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (isEnabled()) {
                const context = docManager.contextForWidget(shell.currentWidget);
                if (!context) {
                    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                        title: trans.__('Cannot Save'),
                        body: trans.__('No context found for current widget!'),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Ok') })]
                    });
                }
                return context.saveAs();
            }
        }
    });
    commands.addCommand(CommandIDs.toggleAutosave, {
        label: trans.__('Autosave Documents'),
        isToggled: () => docManager.autosave,
        execute: () => {
            const value = !docManager.autosave;
            const key = 'autosave';
            return settingRegistry
                .set(docManagerPluginId, key, value)
                .catch((reason) => {
                console.error(`Failed to set ${docManagerPluginId}:${key} - ${reason.message}`);
            });
        }
    });
    if (palette) {
        [
            CommandIDs.reload,
            CommandIDs.restoreCheckpoint,
            CommandIDs.save,
            CommandIDs.saveAs,
            CommandIDs.toggleAutosave
        ].forEach(command => {
            palette.addItem({ command, category });
        });
    }
}
function addLabCommands(app, docManager, labShell, opener, translator) {
    const trans = translator.load('jupyterlab');
    const { commands } = app;
    // Returns the doc widget associated with the most recent contextmenu event.
    const contextMenuWidget = () => {
        var _a;
        const pathRe = /[Pp]ath:\s?(.*)\n?/;
        const test = (node) => { var _a; return !!((_a = node['title']) === null || _a === void 0 ? void 0 : _a.match(pathRe)); };
        const node = app.contextMenuHitTest(test);
        const pathMatch = node === null || node === void 0 ? void 0 : node['title'].match(pathRe);
        return ((_a = (pathMatch && docManager.findWidget(pathMatch[1], null))) !== null && _a !== void 0 ? _a : 
        // Fall back to active doc widget if path cannot be obtained from event.
        labShell.currentWidget);
    };
    // Returns `true` if the current widget has a document context.
    const isEnabled = () => {
        const { currentWidget } = labShell;
        return !!(currentWidget && docManager.contextForWidget(currentWidget));
    };
    commands.addCommand(CommandIDs.clone, {
        label: () => trans.__('New View for %1', fileType(contextMenuWidget(), docManager)),
        isEnabled,
        execute: args => {
            const widget = contextMenuWidget();
            const options = args['options'] || {
                mode: 'split-right'
            };
            if (!widget) {
                return;
            }
            // Clone the widget.
            const child = docManager.cloneWidget(widget);
            if (child) {
                opener.open(child, options);
            }
        }
    });
    commands.addCommand(CommandIDs.rename, {
        label: () => {
            let t = fileType(contextMenuWidget(), docManager);
            if (t) {
                t = ' ' + t;
            }
            return trans.__('Rename%1…', t);
        },
        isEnabled,
        execute: () => {
            // Implies contextMenuWidget() !== null
            if (isEnabled()) {
                const context = docManager.contextForWidget(contextMenuWidget());
                return (0,_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.renameDialog)(docManager, context.path);
            }
        }
    });
    commands.addCommand(CommandIDs.del, {
        label: () => trans.__('Delete %1', fileType(contextMenuWidget(), docManager)),
        isEnabled,
        execute: async () => {
            // Implies contextMenuWidget() !== null
            if (isEnabled()) {
                const context = docManager.contextForWidget(contextMenuWidget());
                if (!context) {
                    return;
                }
                const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Delete'),
                    body: trans.__('Are you sure you want to delete %1', context.path),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Cancel') }),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Delete') })
                    ]
                });
                if (result.button.accept) {
                    await app.commands.execute('docmanager:delete-file', {
                        path: context.path
                    });
                }
            }
        }
    });
    commands.addCommand(CommandIDs.showInFileBrowser, {
        label: () => trans.__('Show in File Browser'),
        isEnabled,
        execute: async () => {
            const widget = contextMenuWidget();
            const context = widget && docManager.contextForWidget(widget);
            if (!context) {
                return;
            }
            // 'activate' is needed if this command is selected in the "open tabs" sidebar
            await commands.execute('filebrowser:activate', { path: context.path });
            await commands.execute('filebrowser:go-to-path', { path: context.path });
        }
    });
}
/**
 * Handle dirty state for a context.
 */
function handleContext(status, context) {
    let disposable = null;
    const onStateChanged = (sender, args) => {
        if (args.name === 'dirty') {
            if (args.newValue === true) {
                if (!disposable) {
                    disposable = status.setDirty();
                }
            }
            else if (disposable) {
                disposable.dispose();
                disposable = null;
            }
        }
    };
    void context.ready.then(() => {
        context.model.stateChanged.connect(onStateChanged);
        if (context.model.dirty) {
            disposable = status.setDirty();
        }
    });
    context.disposed.connect(() => {
        if (disposable) {
            disposable.dispose();
        }
    });
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * A counter for unique IDs.
     */
    Private.id = 0;
    function createRevertConfirmNode(checkpoint, fileType, trans) {
        const body = document.createElement('div');
        const confirmMessage = document.createElement('p');
        const confirmText = document.createTextNode(trans.__('Are you sure you want to revert the %1 to the latest checkpoint? ', fileType));
        const cannotUndoText = document.createElement('strong');
        cannotUndoText.textContent = trans.__('This cannot be undone.');
        confirmMessage.appendChild(confirmText);
        confirmMessage.appendChild(cannotUndoText);
        const lastCheckpointMessage = document.createElement('p');
        const lastCheckpointText = document.createTextNode(trans.__('The checkpoint was last updated at: '));
        const lastCheckpointDate = document.createElement('p');
        const date = new Date(checkpoint.last_modified);
        lastCheckpointDate.style.textAlign = 'center';
        lastCheckpointDate.textContent =
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.format(date, 'dddd, MMMM Do YYYY, h:mm:ss a') +
                ' (' +
                _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.formatHuman(date) +
                ')';
        lastCheckpointMessage.appendChild(lastCheckpointText);
        lastCheckpointMessage.appendChild(lastCheckpointDate);
        body.appendChild(confirmMessage);
        body.appendChild(lastCheckpointMessage);
        return body;
    }
    Private.createRevertConfirmNode = createRevertConfirmNode;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jbWFuYWdlci1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTzhCO0FBT0g7QUFDNkI7QUFPM0I7QUFDbUM7QUFHSjtBQUNaO0FBQ3NCO0FBQ1o7QUFDakI7QUFFSDtBQUV6Qzs7R0FFRztBQUNILElBQVUsVUFBVSxDQThCbkI7QUE5QkQsV0FBVSxVQUFVO0lBQ0wsZ0JBQUssR0FBRyxrQkFBa0IsQ0FBQztJQUUzQixxQkFBVSxHQUFHLHdCQUF3QixDQUFDO0lBRXRDLHNCQUFXLEdBQUcseUJBQXlCLENBQUM7SUFFeEMsZUFBSSxHQUFHLGlCQUFpQixDQUFDO0lBRXpCLHlCQUFjLEdBQUcsNkJBQTZCLENBQUM7SUFFL0MsaUJBQU0sR0FBRyxtQkFBbUIsQ0FBQztJQUU3QixpQkFBTSxHQUFHLG1CQUFtQixDQUFDO0lBRTdCLGNBQUcsR0FBRyxtQkFBbUIsQ0FBQztJQUUxQiw0QkFBaUIsR0FBRywrQkFBK0IsQ0FBQztJQUVwRCxlQUFJLEdBQUcsaUJBQWlCLENBQUM7SUFFekIsa0JBQU8sR0FBRyxxQkFBcUIsQ0FBQztJQUVoQyxpQkFBTSxHQUFHLG9CQUFvQixDQUFDO0lBRTlCLG1CQUFRLEdBQUcscUJBQXFCLENBQUM7SUFFakMseUJBQWMsR0FBRyw0QkFBNEIsQ0FBQztJQUU5Qyw0QkFBaUIsR0FBRyxpQ0FBaUMsQ0FBQztBQUNyRSxDQUFDLEVBOUJTLFVBQVUsS0FBVixVQUFVLFFBOEJuQjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxrQkFBa0IsR0FBRyx5Q0FBeUMsQ0FBQztBQUVyRTs7R0FFRztBQUNILE1BQU0sZ0JBQWdCLEdBQTRDO0lBQ2hFLEVBQUUsRUFBRSxrQkFBa0I7SUFD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Q0FBQyxjQUFjLENBQUMsQ0FBQztRQUNqQyxJQUFJLENBQUMsV0FBVyxDQUFDLHFCQUFxQixDQUFDLENBQUM7UUFDeEMsT0FBTyxJQUFJLENBQUM7SUFDZCxDQUFDO0lBdENlLCtCQUF1QiwwQkFzQ3RDO0FBQ0gsQ0FBQyxFQTdDUyxPQUFPLEtBQVAsT0FBTyxRQTZDaEIiLCJmaWxlIjoicGFja2FnZXNfZG9jbWFuYWdlci1leHRlbnNpb25fbGliX2luZGV4X2pzLjc4MWEyNDBmOGIzMTQzYWI2YWQ2LmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgZG9jbWFuYWdlci1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGFiU2hlbGwsXG4gIElMYWJTdGF0dXMsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIERpYWxvZyxcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBJU2Vzc2lvbkNvbnRleHREaWFsb2dzLFxuICBzaG93RGlhbG9nLFxuICBzaG93RXJyb3JNZXNzYWdlXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElDaGFuZ2VkQXJncywgVGltZSB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBEb2N1bWVudE1hbmFnZXIsXG4gIElEb2N1bWVudE1hbmFnZXIsXG4gIFBhdGhTdGF0dXMsXG4gIHJlbmFtZURpYWxvZyxcbiAgU2F2aW5nU3RhdHVzXG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY21hbmFnZXInO1xuaW1wb3J0IHsgSURvY3VtZW50UHJvdmlkZXJGYWN0b3J5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcHJvdmlkZXInO1xuaW1wb3J0IHsgRG9jdW1lbnRSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IENvbnRlbnRzLCBLZXJuZWwgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElTdGF0dXNCYXIgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0dXNiYXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIFRyYW5zbGF0aW9uQnVuZGxlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgZWFjaCwgbWFwLCBzb21lLCB0b0FycmF5IH0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHsgSlNPTkV4dCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIGRvY3VtZW50IG1hbmFnZXIgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjbG9uZSA9ICdkb2NtYW5hZ2VyOmNsb25lJztcblxuICBleHBvcnQgY29uc3QgZGVsZXRlRmlsZSA9ICdkb2NtYW5hZ2VyOmRlbGV0ZS1maWxlJztcblxuICBleHBvcnQgY29uc3QgbmV3VW50aXRsZWQgPSAnZG9jbWFuYWdlcjpuZXctdW50aXRsZWQnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuID0gJ2RvY21hbmFnZXI6b3Blbic7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5Ccm93c2VyVGFiID0gJ2RvY21hbmFnZXI6b3Blbi1icm93c2VyLXRhYic7XG5cbiAgZXhwb3J0IGNvbnN0IHJlbG9hZCA9ICdkb2NtYW5hZ2VyOnJlbG9hZCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlbmFtZSA9ICdkb2NtYW5hZ2VyOnJlbmFtZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGRlbCA9ICdkb2NtYW5hZ2VyOmRlbGV0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlc3RvcmVDaGVja3BvaW50ID0gJ2RvY21hbmFnZXI6cmVzdG9yZS1jaGVja3BvaW50JztcblxuICBleHBvcnQgY29uc3Qgc2F2ZSA9ICdkb2NtYW5hZ2VyOnNhdmUnO1xuXG4gIGV4cG9ydCBjb25zdCBzYXZlQWxsID0gJ2RvY21hbmFnZXI6c2F2ZS1hbGwnO1xuXG4gIGV4cG9ydCBjb25zdCBzYXZlQXMgPSAnZG9jbWFuYWdlcjpzYXZlLWFzJztcblxuICBleHBvcnQgY29uc3QgZG93bmxvYWQgPSAnZG9jbWFuYWdlcjpkb3dubG9hZCc7XG5cbiAgZXhwb3J0IGNvbnN0IHRvZ2dsZUF1dG9zYXZlID0gJ2RvY21hbmFnZXI6dG9nZ2xlLWF1dG9zYXZlJztcblxuICBleHBvcnQgY29uc3Qgc2hvd0luRmlsZUJyb3dzZXIgPSAnZG9jbWFuYWdlcjpzaG93LWluLWZpbGUtYnJvd3Nlcic7XG59XG5cbi8qKlxuICogVGhlIGlkIG9mIHRoZSBkb2N1bWVudCBtYW5hZ2VyIHBsdWdpbi5cbiAqL1xuY29uc3QgZG9jTWFuYWdlclBsdWdpbklkID0gJ0BqdXB5dGVybGFiL2RvY21hbmFnZXItZXh0ZW5zaW9uOnBsdWdpbic7XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgZG9jdW1lbnQgbWFuYWdlciBwcm92aWRlci5cbiAqL1xuY29uc3QgZG9jTWFuYWdlclBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElEb2N1bWVudE1hbmFnZXI+ID0ge1xuICBpZDogZG9jTWFuYWdlclBsdWdpbklkLFxuICBwcm92aWRlczogSURvY3VtZW50TWFuYWdlcixcbiAgcmVxdWlyZXM6IFtJU2V0dGluZ1JlZ2lzdHJ5LCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbXG4gICAgSUxhYlN0YXR1cyxcbiAgICBJQ29tbWFuZFBhbGV0dGUsXG4gICAgSUxhYlNoZWxsLFxuICAgIElTZXNzaW9uQ29udGV4dERpYWxvZ3MsXG4gICAgSURvY3VtZW50UHJvdmlkZXJGYWN0b3J5XG4gIF0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHN0YXR1czogSUxhYlN0YXR1cyB8IG51bGwsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsIHwgbnVsbCxcbiAgICBzZXNzaW9uRGlhbG9nczogSVNlc3Npb25Db250ZXh0RGlhbG9ncyB8IG51bGwsXG4gICAgZG9jUHJvdmlkZXJGYWN0b3J5OiBJRG9jdW1lbnRQcm92aWRlckZhY3RvcnkgfCBudWxsXG4gICk6IElEb2N1bWVudE1hbmFnZXIgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgbWFuYWdlciA9IGFwcC5zZXJ2aWNlTWFuYWdlcjtcbiAgICBjb25zdCBjb250ZXh0cyA9IG5ldyBXZWFrU2V0PERvY3VtZW50UmVnaXN0cnkuQ29udGV4dD4oKTtcbiAgICBjb25zdCBvcGVuZXI6IERvY3VtZW50TWFuYWdlci5JV2lkZ2V0T3BlbmVyID0ge1xuICAgICAgb3BlbjogKHdpZGdldCwgb3B0aW9ucykgPT4ge1xuICAgICAgICBpZiAoIXdpZGdldC5pZCkge1xuICAgICAgICAgIHdpZGdldC5pZCA9IGBkb2N1bWVudC1tYW5hZ2VyLSR7KytQcml2YXRlLmlkfWA7XG4gICAgICAgIH1cbiAgICAgICAgd2lkZ2V0LnRpdGxlLmRhdGFzZXQgPSB7XG4gICAgICAgICAgdHlwZTogJ2RvY3VtZW50LXRpdGxlJyxcbiAgICAgICAgICAuLi53aWRnZXQudGl0bGUuZGF0YXNldFxuICAgICAgICB9O1xuICAgICAgICBpZiAoIXdpZGdldC5pc0F0dGFjaGVkKSB7XG4gICAgICAgICAgYXBwLnNoZWxsLmFkZCh3aWRnZXQsICdtYWluJywgb3B0aW9ucyB8fCB7fSk7XG4gICAgICAgIH1cbiAgICAgICAgYXBwLnNoZWxsLmFjdGl2YXRlQnlJZCh3aWRnZXQuaWQpO1xuXG4gICAgICAgIC8vIEhhbmRsZSBkaXJ0eSBzdGF0ZSBmb3Igb3BlbiBkb2N1bWVudHMuXG4gICAgICAgIGNvbnN0IGNvbnRleHQgPSBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQod2lkZ2V0KTtcbiAgICAgICAgaWYgKGNvbnRleHQgJiYgIWNvbnRleHRzLmhhcyhjb250ZXh0KSkge1xuICAgICAgICAgIGlmIChzdGF0dXMpIHtcbiAgICAgICAgICAgIGhhbmRsZUNvbnRleHQoc3RhdHVzLCBjb250ZXh0KTtcbiAgICAgICAgICB9XG4gICAgICAgICAgY29udGV4dHMuYWRkKGNvbnRleHQpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfTtcbiAgICBjb25zdCByZWdpc3RyeSA9IGFwcC5kb2NSZWdpc3RyeTtcbiAgICBjb25zdCB3aGVuID0gYXBwLnJlc3RvcmVkLnRoZW4oKCkgPT4gdm9pZCAwKTtcbiAgICBjb25zdCBkb2NNYW5hZ2VyID0gbmV3IERvY3VtZW50TWFuYWdlcih7XG4gICAgICByZWdpc3RyeSxcbiAgICAgIG1hbmFnZXIsXG4gICAgICBvcGVuZXIsXG4gICAgICB3aGVuLFxuICAgICAgc2V0QnVzeTogKHN0YXR1cyAmJiAoKCkgPT4gc3RhdHVzLnNldEJ1c3koKSkpID8/IHVuZGVmaW5lZCxcbiAgICAgIHNlc3Npb25EaWFsb2dzOiBzZXNzaW9uRGlhbG9ncyB8fCB1bmRlZmluZWQsXG4gICAgICB0cmFuc2xhdG9yLFxuICAgICAgY29sbGFib3JhdGl2ZTogdHJ1ZSxcbiAgICAgIGRvY1Byb3ZpZGVyRmFjdG9yeTogZG9jUHJvdmlkZXJGYWN0b3J5ID8/IHVuZGVmaW5lZFxuICAgIH0pO1xuXG4gICAgLy8gUmVnaXN0ZXIgdGhlIGZpbGUgb3BlcmF0aW9ucyBjb21tYW5kcy5cbiAgICBhZGRDb21tYW5kcyhcbiAgICAgIGFwcCxcbiAgICAgIGRvY01hbmFnZXIsXG4gICAgICBvcGVuZXIsXG4gICAgICBzZXR0aW5nUmVnaXN0cnksXG4gICAgICB0cmFuc2xhdG9yLFxuICAgICAgbGFiU2hlbGwsXG4gICAgICBwYWxldHRlXG4gICAgKTtcblxuICAgIC8vIEtlZXAgdXAgdG8gZGF0ZSB3aXRoIHRoZSBzZXR0aW5ncyByZWdpc3RyeS5cbiAgICBjb25zdCBvblNldHRpbmdzVXBkYXRlZCA9IChzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MpID0+IHtcbiAgICAgIC8vIEhhbmRsZSB3aGV0aGVyIHRvIGF1dG9zYXZlXG4gICAgICBjb25zdCBhdXRvc2F2ZSA9IHNldHRpbmdzLmdldCgnYXV0b3NhdmUnKS5jb21wb3NpdGUgYXMgYm9vbGVhbiB8IG51bGw7XG4gICAgICBkb2NNYW5hZ2VyLmF1dG9zYXZlID1cbiAgICAgICAgYXV0b3NhdmUgPT09IHRydWUgfHwgYXV0b3NhdmUgPT09IGZhbHNlID8gYXV0b3NhdmUgOiB0cnVlO1xuICAgICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKENvbW1hbmRJRHMudG9nZ2xlQXV0b3NhdmUpO1xuXG4gICAgICAvLyBIYW5kbGUgYXV0b3NhdmUgaW50ZXJ2YWxcbiAgICAgIGNvbnN0IGF1dG9zYXZlSW50ZXJ2YWwgPSBzZXR0aW5ncy5nZXQoJ2F1dG9zYXZlSW50ZXJ2YWwnKS5jb21wb3NpdGUgYXNcbiAgICAgICAgfCBudW1iZXJcbiAgICAgICAgfCBudWxsO1xuICAgICAgZG9jTWFuYWdlci5hdXRvc2F2ZUludGVydmFsID0gYXV0b3NhdmVJbnRlcnZhbCB8fCAxMjA7XG5cbiAgICAgIC8vIEhhbmRsZSBsYXN0IG1vZGlmaWVkIHRpbWVzdGFtcCBjaGVjayBtYXJnaW5cbiAgICAgIGNvbnN0IGxhc3RNb2RpZmllZENoZWNrTWFyZ2luID0gc2V0dGluZ3MuZ2V0KCdsYXN0TW9kaWZpZWRDaGVja01hcmdpbicpXG4gICAgICAgIC5jb21wb3NpdGUgYXMgbnVtYmVyIHwgbnVsbDtcbiAgICAgIGRvY01hbmFnZXIubGFzdE1vZGlmaWVkQ2hlY2tNYXJnaW4gPSBsYXN0TW9kaWZpZWRDaGVja01hcmdpbiB8fCA1MDA7XG5cbiAgICAgIC8vIEhhbmRsZSBkZWZhdWx0IHdpZGdldCBmYWN0b3J5IG92ZXJyaWRlcy5cbiAgICAgIGNvbnN0IGRlZmF1bHRWaWV3ZXJzID0gc2V0dGluZ3MuZ2V0KCdkZWZhdWx0Vmlld2VycycpLmNvbXBvc2l0ZSBhcyB7XG4gICAgICAgIFtmdDogc3RyaW5nXTogc3RyaW5nO1xuICAgICAgfTtcbiAgICAgIGNvbnN0IG92ZXJyaWRlczogeyBbZnQ6IHN0cmluZ106IHN0cmluZyB9ID0ge307XG4gICAgICAvLyBGaWx0ZXIgdGhlIGRlZmF1bHRWaWV3ZXJzIGFuZCBmaWxlIHR5cGVzIGZvciBleGlzdGluZyBvbmVzLlxuICAgICAgT2JqZWN0LmtleXMoZGVmYXVsdFZpZXdlcnMpLmZvckVhY2goZnQgPT4ge1xuICAgICAgICBpZiAoIXJlZ2lzdHJ5LmdldEZpbGVUeXBlKGZ0KSkge1xuICAgICAgICAgIGNvbnNvbGUud2FybihgRmlsZSBUeXBlICR7ZnR9IG5vdCBmb3VuZGApO1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBpZiAoIXJlZ2lzdHJ5LmdldFdpZGdldEZhY3RvcnkoZGVmYXVsdFZpZXdlcnNbZnRdKSkge1xuICAgICAgICAgIGNvbnNvbGUud2FybihgRG9jdW1lbnQgdmlld2VyICR7ZGVmYXVsdFZpZXdlcnNbZnRdfSBub3QgZm91bmRgKTtcbiAgICAgICAgfVxuICAgICAgICBvdmVycmlkZXNbZnRdID0gZGVmYXVsdFZpZXdlcnNbZnRdO1xuICAgICAgfSk7XG4gICAgICAvLyBTZXQgdGhlIGRlZmF1bHQgZmFjdG9yeSBvdmVycmlkZXMuIElmIG5vdCBwcm92aWRlZCwgdGhpcyBoYXMgdGhlXG4gICAgICAvLyBlZmZlY3Qgb2YgdW5zZXR0aW5nIGFueSBwcmV2aW91cyBvdmVycmlkZXMuXG4gICAgICBlYWNoKHJlZ2lzdHJ5LmZpbGVUeXBlcygpLCBmdCA9PiB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgcmVnaXN0cnkuc2V0RGVmYXVsdFdpZGdldEZhY3RvcnkoZnQubmFtZSwgb3ZlcnJpZGVzW2Z0Lm5hbWVdKTtcbiAgICAgICAgfSBjYXRjaCB7XG4gICAgICAgICAgY29uc29sZS53YXJuKFxuICAgICAgICAgICAgYEZhaWxlZCB0byBzZXQgZGVmYXVsdCB2aWV3ZXIgJHtvdmVycmlkZXNbZnQubmFtZV19IGZvciBmaWxlIHR5cGUgJHtcbiAgICAgICAgICAgICAgZnQubmFtZVxuICAgICAgICAgICAgfWBcbiAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9O1xuXG4gICAgLy8gRmV0Y2ggdGhlIGluaXRpYWwgc3RhdGUgb2YgdGhlIHNldHRpbmdzLlxuICAgIFByb21pc2UuYWxsKFtzZXR0aW5nUmVnaXN0cnkubG9hZChkb2NNYW5hZ2VyUGx1Z2luSWQpLCBhcHAucmVzdG9yZWRdKVxuICAgICAgLnRoZW4oKFtzZXR0aW5nc10pID0+IHtcbiAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KG9uU2V0dGluZ3NVcGRhdGVkKTtcbiAgICAgICAgb25TZXR0aW5nc1VwZGF0ZWQoc2V0dGluZ3MpO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICBjb25zb2xlLmVycm9yKHJlYXNvbi5tZXNzYWdlKTtcbiAgICAgIH0pO1xuXG4gICAgLy8gUmVnaXN0ZXIgYSBmZXRjaCB0cmFuc2Zvcm1lciBmb3IgdGhlIHNldHRpbmdzIHJlZ2lzdHJ5LFxuICAgIC8vIGFsbG93aW5nIHVzIHRvIGR5bmFtaWNhbGx5IHBvcHVsYXRlIGEgaGVscCBzdHJpbmcgd2l0aCB0aGVcbiAgICAvLyBhdmFpbGFibGUgZG9jdW1lbnQgdmlld2VycyBhbmQgZmlsZSB0eXBlcyBmb3IgdGhlIGRlZmF1bHRcbiAgICAvLyB2aWV3ZXIgb3ZlcnJpZGVzLlxuICAgIHNldHRpbmdSZWdpc3RyeS50cmFuc2Zvcm0oZG9jTWFuYWdlclBsdWdpbklkLCB7XG4gICAgICBmZXRjaDogcGx1Z2luID0+IHtcbiAgICAgICAgLy8gR2V0IHRoZSBhdmFpbGFibGUgZmlsZSB0eXBlcy5cbiAgICAgICAgY29uc3QgZmlsZVR5cGVzID0gdG9BcnJheShyZWdpc3RyeS5maWxlVHlwZXMoKSlcbiAgICAgICAgICAubWFwKGZ0ID0+IGZ0Lm5hbWUpXG4gICAgICAgICAgLmpvaW4oJyAgICBcXG4nKTtcbiAgICAgICAgLy8gR2V0IHRoZSBhdmFpbGFibGUgd2lkZ2V0IGZhY3Rvcmllcy5cbiAgICAgICAgY29uc3QgZmFjdG9yaWVzID0gdG9BcnJheShyZWdpc3RyeS53aWRnZXRGYWN0b3JpZXMoKSlcbiAgICAgICAgICAubWFwKGYgPT4gZi5uYW1lKVxuICAgICAgICAgIC5qb2luKCcgICAgXFxuJyk7XG4gICAgICAgIC8vIEdlbmVyYXRlIHRoZSBoZWxwIHN0cmluZy5cbiAgICAgICAgY29uc3QgZGVzY3JpcHRpb24gPSB0cmFucy5fXyhcbiAgICAgICAgICBgT3ZlcnJpZGVzIGZvciB0aGUgZGVmYXVsdCB2aWV3ZXJzIGZvciBmaWxlIHR5cGVzLlxuU3BlY2lmeSBhIG1hcHBpbmcgZnJvbSBmaWxlIHR5cGUgbmFtZSB0byBkb2N1bWVudCB2aWV3ZXIgbmFtZSwgZm9yIGV4YW1wbGU6XG5cbmRlZmF1bHRWaWV3ZXJzOiB7XG4gIG1hcmtkb3duOiBcIk1hcmtkb3duIFByZXZpZXdcIlxufVxuXG5JZiB5b3Ugc3BlY2lmeSBub24tZXhpc3RlbnQgZmlsZSB0eXBlcyBvciB2aWV3ZXJzLCBvciBpZiBhIHZpZXdlciBjYW5ub3Rcbm9wZW4gYSBnaXZlbiBmaWxlIHR5cGUsIHRoZSBvdmVycmlkZSB3aWxsIG5vdCBmdW5jdGlvbi5cblxuQXZhaWxhYmxlIHZpZXdlcnM6XG4lMVxuXG5BdmFpbGFibGUgZmlsZSB0eXBlczpcbiUyYCxcbiAgICAgICAgICBmYWN0b3JpZXMsXG4gICAgICAgICAgZmlsZVR5cGVzXG4gICAgICAgICk7XG4gICAgICAgIGNvbnN0IHNjaGVtYSA9IEpTT05FeHQuZGVlcENvcHkocGx1Z2luLnNjaGVtYSk7XG4gICAgICAgIHNjaGVtYS5wcm9wZXJ0aWVzIS5kZWZhdWx0Vmlld2Vycy5kZXNjcmlwdGlvbiA9IGRlc2NyaXB0aW9uO1xuICAgICAgICByZXR1cm4geyAuLi5wbHVnaW4sIHNjaGVtYSB9O1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gSWYgdGhlIGRvY3VtZW50IHJlZ2lzdHJ5IGdhaW5zIG9yIGxvc2VzIGEgZmFjdG9yeSBvciBmaWxlIHR5cGUsXG4gICAgLy8gcmVnZW5lcmF0ZSB0aGUgc2V0dGluZ3MgZGVzY3JpcHRpb24gd2l0aCB0aGUgYXZhaWxhYmxlIG9wdGlvbnMuXG4gICAgcmVnaXN0cnkuY2hhbmdlZC5jb25uZWN0KCgpID0+IHNldHRpbmdSZWdpc3RyeS5yZWxvYWQoZG9jTWFuYWdlclBsdWdpbklkKSk7XG5cbiAgICByZXR1cm4gZG9jTWFuYWdlcjtcbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiBmb3IgYWRkaW5nIGEgc2F2aW5nIHN0YXR1cyBpdGVtIHRvIHRoZSBzdGF0dXMgYmFyLlxuICovXG5leHBvcnQgY29uc3Qgc2F2aW5nU3RhdHVzUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlci1leHRlbnNpb246c2F2aW5nLXN0YXR1cycsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJRG9jdW1lbnRNYW5hZ2VyLCBJTGFiU2hlbGwsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJU3RhdHVzQmFyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBfOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcixcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHN0YXR1c0JhcjogSVN0YXR1c0JhciB8IG51bGxcbiAgKSA9PiB7XG4gICAgaWYgKCFzdGF0dXNCYXIpIHtcbiAgICAgIC8vIEF1dG9tYXRpY2FsbHkgZGlzYWJsZSBpZiBzdGF0dXNiYXIgbWlzc2luZ1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBzYXZpbmcgPSBuZXcgU2F2aW5nU3RhdHVzKHsgZG9jTWFuYWdlciwgdHJhbnNsYXRvciB9KTtcblxuICAgIC8vIEtlZXAgdGhlIGN1cnJlbnRseSBhY3RpdmUgd2lkZ2V0IHN5bmNocm9uaXplZC5cbiAgICBzYXZpbmcubW9kZWwhLndpZGdldCA9IGxhYlNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgbGFiU2hlbGwuY3VycmVudENoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICBzYXZpbmcubW9kZWwhLndpZGdldCA9IGxhYlNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgfSk7XG5cbiAgICBzdGF0dXNCYXIucmVnaXN0ZXJTdGF0dXNJdGVtKHNhdmluZ1N0YXR1c1BsdWdpbi5pZCwge1xuICAgICAgaXRlbTogc2F2aW5nLFxuICAgICAgYWxpZ246ICdtaWRkbGUnLFxuICAgICAgaXNBY3RpdmU6ICgpID0+IHNhdmluZy5tb2RlbCAhPT0gbnVsbCAmJiBzYXZpbmcubW9kZWwuc3RhdHVzICE9PSBudWxsLFxuICAgICAgYWN0aXZlU3RhdGVDaGFuZ2VkOiBzYXZpbmcubW9kZWwhLnN0YXRlQ2hhbmdlZFxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHByb3ZpZGluZyBhIGZpbGUgcGF0aCB3aWRnZXQgdG8gdGhlIHN0YXR1cyBiYXIuXG4gKi9cbmV4cG9ydCBjb25zdCBwYXRoU3RhdHVzUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlci1leHRlbnNpb246cGF0aC1zdGF0dXMnLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSURvY3VtZW50TWFuYWdlciwgSUxhYlNoZWxsXSxcbiAgb3B0aW9uYWw6IFtJU3RhdHVzQmFyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBfOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcixcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsLFxuICAgIHN0YXR1c0JhcjogSVN0YXR1c0JhciB8IG51bGxcbiAgKSA9PiB7XG4gICAgaWYgKCFzdGF0dXNCYXIpIHtcbiAgICAgIC8vIEF1dG9tYXRpY2FsbHkgZGlzYWJsZSBpZiBzdGF0dXNiYXIgbWlzc2luZ1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBwYXRoID0gbmV3IFBhdGhTdGF0dXMoeyBkb2NNYW5hZ2VyIH0pO1xuXG4gICAgLy8gS2VlcCB0aGUgZmlsZSBwYXRoIHdpZGdldCB1cC10by1kYXRlIHdpdGggdGhlIGFwcGxpY2F0aW9uIGFjdGl2ZSB3aWRnZXQuXG4gICAgcGF0aC5tb2RlbCEud2lkZ2V0ID0gbGFiU2hlbGwuY3VycmVudFdpZGdldDtcbiAgICBsYWJTaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHBhdGgubW9kZWwhLndpZGdldCA9IGxhYlNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgfSk7XG5cbiAgICBzdGF0dXNCYXIucmVnaXN0ZXJTdGF0dXNJdGVtKHBhdGhTdGF0dXNQbHVnaW4uaWQsIHtcbiAgICAgIGl0ZW06IHBhdGgsXG4gICAgICBhbGlnbjogJ3JpZ2h0JyxcbiAgICAgIHJhbms6IDBcbiAgICB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiBwcm92aWRpbmcgZG93bmxvYWQgY29tbWFuZHMgaW4gdGhlIGZpbGUgbWVudSBhbmQgY29tbWFuZCBwYWxldHRlLlxuICovXG5leHBvcnQgY29uc3QgZG93bmxvYWRQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kb2NtYW5hZ2VyLWV4dGVuc2lvbjpkb3dubG9hZCcsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvciwgSURvY3VtZW50TWFuYWdlcl0sXG4gIG9wdGlvbmFsOiBbSUNvbW1hbmRQYWxldHRlXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBkb2NNYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCB7IGNvbW1hbmRzLCBzaGVsbCB9ID0gYXBwO1xuICAgIGNvbnN0IGlzRW5hYmxlZCA9ICgpID0+IHtcbiAgICAgIGNvbnN0IHsgY3VycmVudFdpZGdldCB9ID0gc2hlbGw7XG4gICAgICByZXR1cm4gISEoY3VycmVudFdpZGdldCAmJiBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQoY3VycmVudFdpZGdldCkpO1xuICAgIH07XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmRvd25sb2FkLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0Rvd25sb2FkJyksXG4gICAgICBjYXB0aW9uOiB0cmFucy5fXygnRG93bmxvYWQgdGhlIGZpbGUgdG8geW91ciBjb21wdXRlcicpLFxuICAgICAgaXNFbmFibGVkLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAvLyBDaGVja3MgdGhhdCBzaGVsbC5jdXJyZW50V2lkZ2V0IGlzIHZhbGlkOlxuICAgICAgICBpZiAoaXNFbmFibGVkKCkpIHtcbiAgICAgICAgICBjb25zdCBjb250ZXh0ID0gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KHNoZWxsLmN1cnJlbnRXaWRnZXQhKTtcbiAgICAgICAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgICAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdDYW5ub3QgRG93bmxvYWQnKSxcbiAgICAgICAgICAgICAgYm9keTogdHJhbnMuX18oJ05vIGNvbnRleHQgZm91bmQgZm9yIGN1cnJlbnQgd2lkZ2V0IScpLFxuICAgICAgICAgICAgICBidXR0b25zOiBbRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdPSycpIH0pXVxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfVxuICAgICAgICAgIHJldHVybiBjb250ZXh0LmRvd25sb2FkKCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0ZpbGUgT3BlcmF0aW9ucycpO1xuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kOiBDb21tYW5kSURzLmRvd25sb2FkLCBjYXRlZ29yeSB9KTtcbiAgICB9XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gcHJvdmlkaW5nIG9wZW4tYnJvd3Nlci10YWIgY29tbWFuZHMuXG4gKlxuICogVGhpcyBpcyBpdHMgb3duIHBsdWdpbiBpbiBjYXNlIHlvdSB3b3VsZCBsaWtlIHRvIGRpc2FibGUgdGhpcyBmZWF0dXJlLlxuICogZS5nLiBqdXB5dGVyIGxhYmV4dGVuc2lvbiBkaXNhYmxlIEBqdXB5dGVybGFiL2RvY21hbmFnZXItZXh0ZW5zaW9uOm9wZW4tYnJvd3Nlci10YWJcbiAqXG4gKiBOb3RlOiBJZiBkaXNhYmxpbmcgdGhpcywgeW91IG1heSBhbHNvIHdhbnQgdG8gZGlzYWJsZTpcbiAqIEBqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpvcGVuLWJyb3dzZXItdGFiXG4gKi9cbmV4cG9ydCBjb25zdCBvcGVuQnJvd3NlclRhYlBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2RvY21hbmFnZXItZXh0ZW5zaW9uOm9wZW4tYnJvd3Nlci10YWInLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3IsIElEb2N1bWVudE1hbmFnZXJdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIGRvY01hbmFnZXI6IElEb2N1bWVudE1hbmFnZXJcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCB7IGNvbW1hbmRzIH0gPSBhcHA7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW5Ccm93c2VyVGFiLCB7XG4gICAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgcGF0aCA9XG4gICAgICAgICAgdHlwZW9mIGFyZ3NbJ3BhdGgnXSA9PT0gJ3VuZGVmaW5lZCcgPyAnJyA6IChhcmdzWydwYXRoJ10gYXMgc3RyaW5nKTtcblxuICAgICAgICBpZiAoIXBhdGgpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4gZG9jTWFuYWdlci5zZXJ2aWNlcy5jb250ZW50cy5nZXREb3dubG9hZFVybChwYXRoKS50aGVuKHVybCA9PiB7XG4gICAgICAgICAgY29uc3Qgb3BlbmVkID0gd2luZG93Lm9wZW4oKTtcbiAgICAgICAgICBpZiAob3BlbmVkKSB7XG4gICAgICAgICAgICBvcGVuZWQub3BlbmVyID0gbnVsbDtcbiAgICAgICAgICAgIG9wZW5lZC5sb2NhdGlvbi5ocmVmID0gdXJsO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoJ0ZhaWxlZCB0byBvcGVuIG5ldyBicm93c2VyIHRhYi4nKTtcbiAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgICAgfSxcbiAgICAgIGljb246IGFyZ3MgPT4gKGFyZ3NbJ2ljb24nXSBhcyBzdHJpbmcpIHx8ICcnLFxuICAgICAgbGFiZWw6ICgpID0+IHRyYW5zLl9fKCdPcGVuIGluIE5ldyBCcm93c2VyIFRhYicpXG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbXG4gIGRvY01hbmFnZXJQbHVnaW4sXG4gIHBhdGhTdGF0dXNQbHVnaW4sXG4gIHNhdmluZ1N0YXR1c1BsdWdpbixcbiAgZG93bmxvYWRQbHVnaW4sXG4gIG9wZW5Ccm93c2VyVGFiUGx1Z2luXG5dO1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcblxuLyogV2lkZ2V0IHRvIGRpc3BsYXkgdGhlIHJldmVydCB0byBjaGVja3BvaW50IGNvbmZpcm1hdGlvbi4gKi9cbmNsYXNzIFJldmVydENvbmZpcm1XaWRnZXQgZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IHJldmVydCBjb25maXJtYXRpb24gd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3IoXG4gICAgY2hlY2twb2ludDogQ29udGVudHMuSUNoZWNrcG9pbnRNb2RlbCxcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGUsXG4gICAgZmlsZVR5cGU6IHN0cmluZyA9ICdub3RlYm9vaydcbiAgKSB7XG4gICAgc3VwZXIoe1xuICAgICAgbm9kZTogUHJpdmF0ZS5jcmVhdGVSZXZlcnRDb25maXJtTm9kZShjaGVja3BvaW50LCBmaWxlVHlwZSwgdHJhbnMpXG4gICAgfSk7XG4gIH1cbn1cblxuLy8gUmV0dXJucyB0aGUgZmlsZSB0eXBlIGZvciBhIHdpZGdldC5cbmZ1bmN0aW9uIGZpbGVUeXBlKHdpZGdldDogV2lkZ2V0IHwgbnVsbCwgZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcik6IHN0cmluZyB7XG4gIGlmICghd2lkZ2V0KSB7XG4gICAgcmV0dXJuICdGaWxlJztcbiAgfVxuICBjb25zdCBjb250ZXh0ID0gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KHdpZGdldCk7XG4gIGlmICghY29udGV4dCkge1xuICAgIHJldHVybiAnJztcbiAgfVxuICBjb25zdCBmdHMgPSBkb2NNYW5hZ2VyLnJlZ2lzdHJ5LmdldEZpbGVUeXBlc0ZvclBhdGgoY29udGV4dC5wYXRoKTtcbiAgcmV0dXJuIGZ0cy5sZW5ndGggJiYgZnRzWzBdLmRpc3BsYXlOYW1lID8gZnRzWzBdLmRpc3BsYXlOYW1lIDogJ0ZpbGUnO1xufVxuXG4vKipcbiAqIEFkZCB0aGUgZmlsZSBvcGVyYXRpb25zIGNvbW1hbmRzIHRvIHRoZSBhcHBsaWNhdGlvbidzIGNvbW1hbmQgcmVnaXN0cnkuXG4gKi9cbmZ1bmN0aW9uIGFkZENvbW1hbmRzKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcixcbiAgb3BlbmVyOiBEb2N1bWVudE1hbmFnZXIuSVdpZGdldE9wZW5lcixcbiAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgbGFiU2hlbGw6IElMYWJTaGVsbCB8IG51bGwsXG4gIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGxcbik6IHZvaWQge1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCB7IGNvbW1hbmRzLCBzaGVsbCB9ID0gYXBwO1xuICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdGaWxlIE9wZXJhdGlvbnMnKTtcbiAgY29uc3QgaXNFbmFibGVkID0gKCkgPT4ge1xuICAgIGNvbnN0IHsgY3VycmVudFdpZGdldCB9ID0gc2hlbGw7XG4gICAgcmV0dXJuICEhKGN1cnJlbnRXaWRnZXQgJiYgZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KGN1cnJlbnRXaWRnZXQpKTtcbiAgfTtcblxuICBjb25zdCBpc1dyaXRhYmxlID0gKCkgPT4ge1xuICAgIGNvbnN0IHsgY3VycmVudFdpZGdldCB9ID0gc2hlbGw7XG4gICAgaWYgKCFjdXJyZW50V2lkZ2V0KSB7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuICAgIGNvbnN0IGNvbnRleHQgPSBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQoY3VycmVudFdpZGdldCk7XG4gICAgcmV0dXJuICEhKFxuICAgICAgY29udGV4dCAmJlxuICAgICAgY29udGV4dC5jb250ZW50c01vZGVsICYmXG4gICAgICBjb250ZXh0LmNvbnRlbnRzTW9kZWwud3JpdGFibGVcbiAgICApO1xuICB9O1xuXG4gIC8vIElmIGluc2lkZSBhIHJpY2ggYXBwbGljYXRpb24gbGlrZSBKdXB5dGVyTGFiLCBhZGQgYWRkaXRpb25hbCBmdW5jdGlvbmFsaXR5LlxuICBpZiAobGFiU2hlbGwpIHtcbiAgICBhZGRMYWJDb21tYW5kcyhhcHAsIGRvY01hbmFnZXIsIGxhYlNoZWxsLCBvcGVuZXIsIHRyYW5zbGF0b3IpO1xuICB9XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmRlbGV0ZUZpbGUsIHtcbiAgICBsYWJlbDogKCkgPT4gYERlbGV0ZSAke2ZpbGVUeXBlKHNoZWxsLmN1cnJlbnRXaWRnZXQsIGRvY01hbmFnZXIpfWAsXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBwYXRoID1cbiAgICAgICAgdHlwZW9mIGFyZ3NbJ3BhdGgnXSA9PT0gJ3VuZGVmaW5lZCcgPyAnJyA6IChhcmdzWydwYXRoJ10gYXMgc3RyaW5nKTtcblxuICAgICAgaWYgKCFwYXRoKSB7XG4gICAgICAgIGNvbnN0IGNvbW1hbmQgPSBDb21tYW5kSURzLmRlbGV0ZUZpbGU7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcihgQSBub24tZW1wdHkgcGF0aCBpcyByZXF1aXJlZCBmb3IgJHtjb21tYW5kfS5gKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBkb2NNYW5hZ2VyLmRlbGV0ZUZpbGUocGF0aCk7XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubmV3VW50aXRsZWQsIHtcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIC8vIEZJWE1FLVRSQU5TOiBMb2NhbGl6aW5nIGFyZ3NbJ2Vycm9yJ10/XG4gICAgICBjb25zdCBlcnJvclRpdGxlID0gKGFyZ3NbJ2Vycm9yJ10gYXMgc3RyaW5nKSB8fCB0cmFucy5fXygnRXJyb3InKTtcbiAgICAgIGNvbnN0IHBhdGggPVxuICAgICAgICB0eXBlb2YgYXJnc1sncGF0aCddID09PSAndW5kZWZpbmVkJyA/ICcnIDogKGFyZ3NbJ3BhdGgnXSBhcyBzdHJpbmcpO1xuICAgICAgY29uc3Qgb3B0aW9uczogUGFydGlhbDxDb250ZW50cy5JQ3JlYXRlT3B0aW9ucz4gPSB7XG4gICAgICAgIHR5cGU6IGFyZ3NbJ3R5cGUnXSBhcyBDb250ZW50cy5Db250ZW50VHlwZSxcbiAgICAgICAgcGF0aFxuICAgICAgfTtcblxuICAgICAgaWYgKGFyZ3NbJ3R5cGUnXSA9PT0gJ2ZpbGUnKSB7XG4gICAgICAgIG9wdGlvbnMuZXh0ID0gKGFyZ3NbJ2V4dCddIGFzIHN0cmluZykgfHwgJy50eHQnO1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gZG9jTWFuYWdlci5zZXJ2aWNlcy5jb250ZW50c1xuICAgICAgICAubmV3VW50aXRsZWQob3B0aW9ucylcbiAgICAgICAgLmNhdGNoKGVycm9yID0+IHNob3dFcnJvck1lc3NhZ2UoZXJyb3JUaXRsZSwgZXJyb3IpKTtcbiAgICB9LFxuICAgIGxhYmVsOiBhcmdzID0+IChhcmdzWydsYWJlbCddIGFzIHN0cmluZykgfHwgYE5ldyAke2FyZ3NbJ3R5cGUnXSBhcyBzdHJpbmd9YFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3Blbiwge1xuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgcGF0aCA9XG4gICAgICAgIHR5cGVvZiBhcmdzWydwYXRoJ10gPT09ICd1bmRlZmluZWQnID8gJycgOiAoYXJnc1sncGF0aCddIGFzIHN0cmluZyk7XG4gICAgICBjb25zdCBmYWN0b3J5ID0gKGFyZ3NbJ2ZhY3RvcnknXSBhcyBzdHJpbmcpIHx8IHZvaWQgMDtcbiAgICAgIGNvbnN0IGtlcm5lbCA9IChhcmdzPy5rZXJuZWwgYXMgdW5rbm93bikgYXMgS2VybmVsLklNb2RlbCB8IHVuZGVmaW5lZDtcbiAgICAgIGNvbnN0IG9wdGlvbnMgPVxuICAgICAgICAoYXJnc1snb3B0aW9ucyddIGFzIERvY3VtZW50UmVnaXN0cnkuSU9wZW5PcHRpb25zKSB8fCB2b2lkIDA7XG4gICAgICByZXR1cm4gZG9jTWFuYWdlci5zZXJ2aWNlcy5jb250ZW50c1xuICAgICAgICAuZ2V0KHBhdGgsIHsgY29udGVudDogZmFsc2UgfSlcbiAgICAgICAgLnRoZW4oKCkgPT4gZG9jTWFuYWdlci5vcGVuT3JSZXZlYWwocGF0aCwgZmFjdG9yeSwga2VybmVsLCBvcHRpb25zKSk7XG4gICAgfSxcbiAgICBpY29uOiBhcmdzID0+IChhcmdzWydpY29uJ10gYXMgc3RyaW5nKSB8fCAnJyxcbiAgICBsYWJlbDogYXJncyA9PiAoYXJnc1snbGFiZWwnXSB8fCBhcmdzWydmYWN0b3J5J10pIGFzIHN0cmluZyxcbiAgICBtbmVtb25pYzogYXJncyA9PiAoYXJnc1snbW5lbW9uaWMnXSBhcyBudW1iZXIpIHx8IC0xXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZWxvYWQsIHtcbiAgICBsYWJlbDogKCkgPT5cbiAgICAgIHRyYW5zLl9fKFxuICAgICAgICAnUmVsb2FkICUxIGZyb20gRGlzaycsXG4gICAgICAgIGZpbGVUeXBlKHNoZWxsLmN1cnJlbnRXaWRnZXQsIGRvY01hbmFnZXIpXG4gICAgICApLFxuICAgIGNhcHRpb246IHRyYW5zLl9fKCdSZWxvYWQgY29udGVudHMgZnJvbSBkaXNrJyksXG4gICAgaXNFbmFibGVkLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIC8vIENoZWNrcyB0aGF0IHNoZWxsLmN1cnJlbnRXaWRnZXQgaXMgdmFsaWQ6XG4gICAgICBpZiAoIWlzRW5hYmxlZCgpKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGNvbnRleHQgPSBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQoc2hlbGwuY3VycmVudFdpZGdldCEpO1xuICAgICAgY29uc3QgdHlwZSA9IGZpbGVUeXBlKHNoZWxsLmN1cnJlbnRXaWRnZXQhLCBkb2NNYW5hZ2VyKTtcbiAgICAgIGlmICghY29udGV4dCkge1xuICAgICAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdDYW5ub3QgUmVsb2FkJyksXG4gICAgICAgICAgYm9keTogdHJhbnMuX18oJ05vIGNvbnRleHQgZm91bmQgZm9yIGN1cnJlbnQgd2lkZ2V0IScpLFxuICAgICAgICAgIGJ1dHRvbnM6IFtEaWFsb2cub2tCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ09rJykgfSldXG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgICAgaWYgKGNvbnRleHQubW9kZWwuZGlydHkpIHtcbiAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnUmVsb2FkICUxIGZyb20gRGlzaycsIHR5cGUpLFxuICAgICAgICAgIGJvZHk6IHRyYW5zLl9fKFxuICAgICAgICAgICAgJ0FyZSB5b3Ugc3VyZSB5b3Ugd2FudCB0byByZWxvYWQgdGhlICUxIGZyb20gdGhlIGRpc2s/JyxcbiAgICAgICAgICAgIHR5cGVcbiAgICAgICAgICApLFxuICAgICAgICAgIGJ1dHRvbnM6IFtcbiAgICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0NhbmNlbCcpIH0pLFxuICAgICAgICAgICAgRGlhbG9nLndhcm5CdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ1JlbG9hZCcpIH0pXG4gICAgICAgICAgXVxuICAgICAgICB9KS50aGVuKHJlc3VsdCA9PiB7XG4gICAgICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0ICYmICFjb250ZXh0LmlzRGlzcG9zZWQpIHtcbiAgICAgICAgICAgIHJldHVybiBjb250ZXh0LnJldmVydCgpO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBpZiAoIWNvbnRleHQuaXNEaXNwb3NlZCkge1xuICAgICAgICAgIHJldHVybiBjb250ZXh0LnJldmVydCgpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVzdG9yZUNoZWNrcG9pbnQsIHtcbiAgICBsYWJlbDogKCkgPT5cbiAgICAgIHRyYW5zLl9fKFxuICAgICAgICAnUmV2ZXJ0ICUxIHRvIENoZWNrcG9pbnQnLFxuICAgICAgICBmaWxlVHlwZShzaGVsbC5jdXJyZW50V2lkZ2V0LCBkb2NNYW5hZ2VyKVxuICAgICAgKSxcbiAgICBjYXB0aW9uOiB0cmFucy5fXygnUmV2ZXJ0IGNvbnRlbnRzIHRvIHByZXZpb3VzIGNoZWNrcG9pbnQnKSxcbiAgICBpc0VuYWJsZWQsXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgLy8gQ2hlY2tzIHRoYXQgc2hlbGwuY3VycmVudFdpZGdldCBpcyB2YWxpZDpcbiAgICAgIGlmICghaXNFbmFibGVkKCkpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgY29udGV4dCA9IGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldChzaGVsbC5jdXJyZW50V2lkZ2V0ISk7XG4gICAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnQ2Fubm90IFJldmVydCcpLFxuICAgICAgICAgIGJvZHk6IHRyYW5zLl9fKCdObyBjb250ZXh0IGZvdW5kIGZvciBjdXJyZW50IHdpZGdldCEnKSxcbiAgICAgICAgICBidXR0b25zOiBbRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdPaycpIH0pXVxuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBjb250ZXh0Lmxpc3RDaGVja3BvaW50cygpLnRoZW4oY2hlY2twb2ludHMgPT4ge1xuICAgICAgICBpZiAoY2hlY2twb2ludHMubGVuZ3RoIDwgMSkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBsYXN0Q2hlY2twb2ludCA9IGNoZWNrcG9pbnRzW2NoZWNrcG9pbnRzLmxlbmd0aCAtIDFdO1xuICAgICAgICBpZiAoIWxhc3RDaGVja3BvaW50KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IHR5cGUgPSBmaWxlVHlwZShzaGVsbC5jdXJyZW50V2lkZ2V0LCBkb2NNYW5hZ2VyKTtcbiAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnUmV2ZXJ0ICUxIHRvIGNoZWNrcG9pbnQnLCB0eXBlKSxcbiAgICAgICAgICBib2R5OiBuZXcgUmV2ZXJ0Q29uZmlybVdpZGdldChsYXN0Q2hlY2twb2ludCwgdHJhbnMsIHR5cGUpLFxuICAgICAgICAgIGJ1dHRvbnM6IFtcbiAgICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0NhbmNlbCcpIH0pLFxuICAgICAgICAgICAgRGlhbG9nLndhcm5CdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ1JldmVydCcpIH0pXG4gICAgICAgICAgXVxuICAgICAgICB9KS50aGVuKHJlc3VsdCA9PiB7XG4gICAgICAgICAgaWYgKGNvbnRleHQuaXNEaXNwb3NlZCkge1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgIH1cbiAgICAgICAgICBpZiAocmVzdWx0LmJ1dHRvbi5hY2NlcHQpIHtcbiAgICAgICAgICAgIGlmIChjb250ZXh0Lm1vZGVsLnJlYWRPbmx5KSB7XG4gICAgICAgICAgICAgIHJldHVybiBjb250ZXh0LnJldmVydCgpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgcmV0dXJuIGNvbnRleHQucmVzdG9yZUNoZWNrcG9pbnQoKS50aGVuKCgpID0+IGNvbnRleHQucmV2ZXJ0KCkpO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zYXZlLCB7XG4gICAgbGFiZWw6ICgpID0+IHRyYW5zLl9fKCdTYXZlICUxJywgZmlsZVR5cGUoc2hlbGwuY3VycmVudFdpZGdldCwgZG9jTWFuYWdlcikpLFxuICAgIGNhcHRpb246IHRyYW5zLl9fKCdTYXZlIGFuZCBjcmVhdGUgY2hlY2twb2ludCcpLFxuICAgIGlzRW5hYmxlZDogaXNXcml0YWJsZSxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAvLyBDaGVja3MgdGhhdCBzaGVsbC5jdXJyZW50V2lkZ2V0IGlzIHZhbGlkOlxuICAgICAgaWYgKGlzRW5hYmxlZCgpKSB7XG4gICAgICAgIGNvbnN0IGNvbnRleHQgPSBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQoc2hlbGwuY3VycmVudFdpZGdldCEpO1xuICAgICAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgICAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0Nhbm5vdCBTYXZlJyksXG4gICAgICAgICAgICBib2R5OiB0cmFucy5fXygnTm8gY29udGV4dCBmb3VuZCBmb3IgY3VycmVudCB3aWRnZXQhJyksXG4gICAgICAgICAgICBidXR0b25zOiBbRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdPaycpIH0pXVxuICAgICAgICAgIH0pO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGlmIChjb250ZXh0Lm1vZGVsLnJlYWRPbmx5KSB7XG4gICAgICAgICAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnQ2Fubm90IFNhdmUnKSxcbiAgICAgICAgICAgICAgYm9keTogdHJhbnMuX18oJ0RvY3VtZW50IGlzIHJlYWQtb25seScpLFxuICAgICAgICAgICAgICBidXR0b25zOiBbRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdPaycpIH0pXVxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgcmV0dXJuIGNvbnRleHRcbiAgICAgICAgICAgIC5zYXZlKClcbiAgICAgICAgICAgIC50aGVuKCgpID0+IGNvbnRleHQhLmNyZWF0ZUNoZWNrcG9pbnQoKSlcbiAgICAgICAgICAgIC5jYXRjaChlcnIgPT4ge1xuICAgICAgICAgICAgICAvLyBJZiB0aGUgc2F2ZSB3YXMgY2FuY2VsZWQgYnkgdXNlci1hY3Rpb24sIGRvIG5vdGhpbmcuXG4gICAgICAgICAgICAgIC8vIEZJWE1FLVRSQU5TOiBJcyB0aGlzIHVzaW5nIHRoZSB0ZXh0IG9uIHRoZSBidXR0b24gb3I/XG4gICAgICAgICAgICAgIGlmIChlcnIubWVzc2FnZSA9PT0gJ0NhbmNlbCcpIHtcbiAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgdGhyb3cgZXJyO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zYXZlQWxsLCB7XG4gICAgbGFiZWw6ICgpID0+IHRyYW5zLl9fKCdTYXZlIEFsbCcpLFxuICAgIGNhcHRpb246IHRyYW5zLl9fKCdTYXZlIGFsbCBvcGVuIGRvY3VtZW50cycpLFxuICAgIGlzRW5hYmxlZDogKCkgPT4ge1xuICAgICAgcmV0dXJuIHNvbWUoXG4gICAgICAgIG1hcChzaGVsbC53aWRnZXRzKCdtYWluJyksIHcgPT4gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KHcpKSxcbiAgICAgICAgYyA9PiBjPy5jb250ZW50c01vZGVsPy53cml0YWJsZSA/PyBmYWxzZVxuICAgICAgKTtcbiAgICB9LFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHByb21pc2VzOiBQcm9taXNlPHZvaWQ+W10gPSBbXTtcbiAgICAgIGNvbnN0IHBhdGhzID0gbmV3IFNldDxzdHJpbmc+KCk7IC8vIENhY2hlIHNvIHdlIGRvbid0IGRvdWJsZSBzYXZlIGZpbGVzLlxuICAgICAgZWFjaChzaGVsbC53aWRnZXRzKCdtYWluJyksIHdpZGdldCA9PiB7XG4gICAgICAgIGNvbnN0IGNvbnRleHQgPSBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQod2lkZ2V0KTtcbiAgICAgICAgaWYgKGNvbnRleHQgJiYgIWNvbnRleHQubW9kZWwucmVhZE9ubHkgJiYgIXBhdGhzLmhhcyhjb250ZXh0LnBhdGgpKSB7XG4gICAgICAgICAgcGF0aHMuYWRkKGNvbnRleHQucGF0aCk7XG4gICAgICAgICAgcHJvbWlzZXMucHVzaChjb250ZXh0LnNhdmUoKSk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgICAgcmV0dXJuIFByb21pc2UuYWxsKHByb21pc2VzKTtcbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zYXZlQXMsIHtcbiAgICBsYWJlbDogKCkgPT5cbiAgICAgIHRyYW5zLl9fKCdTYXZlICUxIEFz4oCmJywgZmlsZVR5cGUoc2hlbGwuY3VycmVudFdpZGdldCwgZG9jTWFuYWdlcikpLFxuICAgIGNhcHRpb246IHRyYW5zLl9fKCdTYXZlIHdpdGggbmV3IHBhdGgnKSxcbiAgICBpc0VuYWJsZWQsXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgLy8gQ2hlY2tzIHRoYXQgc2hlbGwuY3VycmVudFdpZGdldCBpcyB2YWxpZDpcbiAgICAgIGlmIChpc0VuYWJsZWQoKSkge1xuICAgICAgICBjb25zdCBjb250ZXh0ID0gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KHNoZWxsLmN1cnJlbnRXaWRnZXQhKTtcbiAgICAgICAgaWYgKCFjb250ZXh0KSB7XG4gICAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdDYW5ub3QgU2F2ZScpLFxuICAgICAgICAgICAgYm9keTogdHJhbnMuX18oJ05vIGNvbnRleHQgZm91bmQgZm9yIGN1cnJlbnQgd2lkZ2V0IScpLFxuICAgICAgICAgICAgYnV0dG9uczogW0RpYWxvZy5va0J1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnT2snKSB9KV1cbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gY29udGV4dC5zYXZlQXMoKTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVBdXRvc2F2ZSwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnQXV0b3NhdmUgRG9jdW1lbnRzJyksXG4gICAgaXNUb2dnbGVkOiAoKSA9PiBkb2NNYW5hZ2VyLmF1dG9zYXZlLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHZhbHVlID0gIWRvY01hbmFnZXIuYXV0b3NhdmU7XG4gICAgICBjb25zdCBrZXkgPSAnYXV0b3NhdmUnO1xuICAgICAgcmV0dXJuIHNldHRpbmdSZWdpc3RyeVxuICAgICAgICAuc2V0KGRvY01hbmFnZXJQbHVnaW5JZCwga2V5LCB2YWx1ZSlcbiAgICAgICAgLmNhdGNoKChyZWFzb246IEVycm9yKSA9PiB7XG4gICAgICAgICAgY29uc29sZS5lcnJvcihcbiAgICAgICAgICAgIGBGYWlsZWQgdG8gc2V0ICR7ZG9jTWFuYWdlclBsdWdpbklkfToke2tleX0gLSAke3JlYXNvbi5tZXNzYWdlfWBcbiAgICAgICAgICApO1xuICAgICAgICB9KTtcbiAgICB9XG4gIH0pO1xuXG4gIGlmIChwYWxldHRlKSB7XG4gICAgW1xuICAgICAgQ29tbWFuZElEcy5yZWxvYWQsXG4gICAgICBDb21tYW5kSURzLnJlc3RvcmVDaGVja3BvaW50LFxuICAgICAgQ29tbWFuZElEcy5zYXZlLFxuICAgICAgQ29tbWFuZElEcy5zYXZlQXMsXG4gICAgICBDb21tYW5kSURzLnRvZ2dsZUF1dG9zYXZlXG4gICAgXS5mb3JFYWNoKGNvbW1hbmQgPT4ge1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZCwgY2F0ZWdvcnkgfSk7XG4gICAgfSk7XG4gIH1cbn1cblxuZnVuY3Rpb24gYWRkTGFiQ29tbWFuZHMoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBkb2NNYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyLFxuICBsYWJTaGVsbDogSUxhYlNoZWxsLFxuICBvcGVuZXI6IERvY3VtZW50TWFuYWdlci5JV2lkZ2V0T3BlbmVyLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuKTogdm9pZCB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcblxuICAvLyBSZXR1cm5zIHRoZSBkb2Mgd2lkZ2V0IGFzc29jaWF0ZWQgd2l0aCB0aGUgbW9zdCByZWNlbnQgY29udGV4dG1lbnUgZXZlbnQuXG4gIGNvbnN0IGNvbnRleHRNZW51V2lkZ2V0ID0gKCk6IFdpZGdldCB8IG51bGwgPT4ge1xuICAgIGNvbnN0IHBhdGhSZSA9IC9bUHBdYXRoOlxccz8oLiopXFxuPy87XG4gICAgY29uc3QgdGVzdCA9IChub2RlOiBIVE1MRWxlbWVudCkgPT4gISFub2RlWyd0aXRsZSddPy5tYXRjaChwYXRoUmUpO1xuICAgIGNvbnN0IG5vZGUgPSBhcHAuY29udGV4dE1lbnVIaXRUZXN0KHRlc3QpO1xuXG4gICAgY29uc3QgcGF0aE1hdGNoID0gbm9kZT8uWyd0aXRsZSddLm1hdGNoKHBhdGhSZSk7XG4gICAgcmV0dXJuIChcbiAgICAgIChwYXRoTWF0Y2ggJiYgZG9jTWFuYWdlci5maW5kV2lkZ2V0KHBhdGhNYXRjaFsxXSwgbnVsbCkpID8/XG4gICAgICAvLyBGYWxsIGJhY2sgdG8gYWN0aXZlIGRvYyB3aWRnZXQgaWYgcGF0aCBjYW5ub3QgYmUgb2J0YWluZWQgZnJvbSBldmVudC5cbiAgICAgIGxhYlNoZWxsLmN1cnJlbnRXaWRnZXRcbiAgICApO1xuICB9O1xuXG4gIC8vIFJldHVybnMgYHRydWVgIGlmIHRoZSBjdXJyZW50IHdpZGdldCBoYXMgYSBkb2N1bWVudCBjb250ZXh0LlxuICBjb25zdCBpc0VuYWJsZWQgPSAoKSA9PiB7XG4gICAgY29uc3QgeyBjdXJyZW50V2lkZ2V0IH0gPSBsYWJTaGVsbDtcbiAgICByZXR1cm4gISEoY3VycmVudFdpZGdldCAmJiBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQoY3VycmVudFdpZGdldCkpO1xuICB9O1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jbG9uZSwge1xuICAgIGxhYmVsOiAoKSA9PlxuICAgICAgdHJhbnMuX18oJ05ldyBWaWV3IGZvciAlMScsIGZpbGVUeXBlKGNvbnRleHRNZW51V2lkZ2V0KCksIGRvY01hbmFnZXIpKSxcbiAgICBpc0VuYWJsZWQsXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSBjb250ZXh0TWVudVdpZGdldCgpO1xuICAgICAgY29uc3Qgb3B0aW9ucyA9IChhcmdzWydvcHRpb25zJ10gYXMgRG9jdW1lbnRSZWdpc3RyeS5JT3Blbk9wdGlvbnMpIHx8IHtcbiAgICAgICAgbW9kZTogJ3NwbGl0LXJpZ2h0J1xuICAgICAgfTtcbiAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIC8vIENsb25lIHRoZSB3aWRnZXQuXG4gICAgICBjb25zdCBjaGlsZCA9IGRvY01hbmFnZXIuY2xvbmVXaWRnZXQod2lkZ2V0KTtcbiAgICAgIGlmIChjaGlsZCkge1xuICAgICAgICBvcGVuZXIub3BlbihjaGlsZCwgb3B0aW9ucyk7XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVuYW1lLCB7XG4gICAgbGFiZWw6ICgpID0+IHtcbiAgICAgIGxldCB0ID0gZmlsZVR5cGUoY29udGV4dE1lbnVXaWRnZXQoKSwgZG9jTWFuYWdlcik7XG4gICAgICBpZiAodCkge1xuICAgICAgICB0ID0gJyAnICsgdDtcbiAgICAgIH1cbiAgICAgIHJldHVybiB0cmFucy5fXygnUmVuYW1lJTHigKYnLCB0KTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZCxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAvLyBJbXBsaWVzIGNvbnRleHRNZW51V2lkZ2V0KCkgIT09IG51bGxcbiAgICAgIGlmIChpc0VuYWJsZWQoKSkge1xuICAgICAgICBjb25zdCBjb250ZXh0ID0gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KGNvbnRleHRNZW51V2lkZ2V0KCkhKTtcbiAgICAgICAgcmV0dXJuIHJlbmFtZURpYWxvZyhkb2NNYW5hZ2VyLCBjb250ZXh0IS5wYXRoKTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5kZWwsIHtcbiAgICBsYWJlbDogKCkgPT5cbiAgICAgIHRyYW5zLl9fKCdEZWxldGUgJTEnLCBmaWxlVHlwZShjb250ZXh0TWVudVdpZGdldCgpLCBkb2NNYW5hZ2VyKSksXG4gICAgaXNFbmFibGVkLFxuICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgIC8vIEltcGxpZXMgY29udGV4dE1lbnVXaWRnZXQoKSAhPT0gbnVsbFxuICAgICAgaWYgKGlzRW5hYmxlZCgpKSB7XG4gICAgICAgIGNvbnN0IGNvbnRleHQgPSBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQoY29udGV4dE1lbnVXaWRnZXQoKSEpO1xuICAgICAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgc2hvd0RpYWxvZyh7XG4gICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdEZWxldGUnKSxcbiAgICAgICAgICBib2R5OiB0cmFucy5fXygnQXJlIHlvdSBzdXJlIHlvdSB3YW50IHRvIGRlbGV0ZSAlMScsIGNvbnRleHQucGF0aCksXG4gICAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnQ2FuY2VsJykgfSksXG4gICAgICAgICAgICBEaWFsb2cud2FybkJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnRGVsZXRlJykgfSlcbiAgICAgICAgICBdXG4gICAgICAgIH0pO1xuXG4gICAgICAgIGlmIChyZXN1bHQuYnV0dG9uLmFjY2VwdCkge1xuICAgICAgICAgIGF3YWl0IGFwcC5jb21tYW5kcy5leGVjdXRlKCdkb2NtYW5hZ2VyOmRlbGV0ZS1maWxlJywge1xuICAgICAgICAgICAgcGF0aDogY29udGV4dC5wYXRoXG4gICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zaG93SW5GaWxlQnJvd3Nlciwge1xuICAgIGxhYmVsOiAoKSA9PiB0cmFucy5fXygnU2hvdyBpbiBGaWxlIEJyb3dzZXInKSxcbiAgICBpc0VuYWJsZWQsXG4gICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gY29udGV4dE1lbnVXaWRnZXQoKTtcbiAgICAgIGNvbnN0IGNvbnRleHQgPSB3aWRnZXQgJiYgZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KHdpZGdldCk7XG4gICAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuXG4gICAgICAvLyAnYWN0aXZhdGUnIGlzIG5lZWRlZCBpZiB0aGlzIGNvbW1hbmQgaXMgc2VsZWN0ZWQgaW4gdGhlIFwib3BlbiB0YWJzXCIgc2lkZWJhclxuICAgICAgYXdhaXQgY29tbWFuZHMuZXhlY3V0ZSgnZmlsZWJyb3dzZXI6YWN0aXZhdGUnLCB7IHBhdGg6IGNvbnRleHQucGF0aCB9KTtcbiAgICAgIGF3YWl0IGNvbW1hbmRzLmV4ZWN1dGUoJ2ZpbGVicm93c2VyOmdvLXRvLXBhdGgnLCB7IHBhdGg6IGNvbnRleHQucGF0aCB9KTtcbiAgICB9XG4gIH0pO1xufVxuXG4vKipcbiAqIEhhbmRsZSBkaXJ0eSBzdGF0ZSBmb3IgYSBjb250ZXh0LlxuICovXG5mdW5jdGlvbiBoYW5kbGVDb250ZXh0KFxuICBzdGF0dXM6IElMYWJTdGF0dXMsXG4gIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dFxuKTogdm9pZCB7XG4gIGxldCBkaXNwb3NhYmxlOiBJRGlzcG9zYWJsZSB8IG51bGwgPSBudWxsO1xuICBjb25zdCBvblN0YXRlQ2hhbmdlZCA9IChzZW5kZXI6IGFueSwgYXJnczogSUNoYW5nZWRBcmdzPGFueT4pID0+IHtcbiAgICBpZiAoYXJncy5uYW1lID09PSAnZGlydHknKSB7XG4gICAgICBpZiAoYXJncy5uZXdWYWx1ZSA9PT0gdHJ1ZSkge1xuICAgICAgICBpZiAoIWRpc3Bvc2FibGUpIHtcbiAgICAgICAgICBkaXNwb3NhYmxlID0gc3RhdHVzLnNldERpcnR5KCk7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSBpZiAoZGlzcG9zYWJsZSkge1xuICAgICAgICBkaXNwb3NhYmxlLmRpc3Bvc2UoKTtcbiAgICAgICAgZGlzcG9zYWJsZSA9IG51bGw7XG4gICAgICB9XG4gICAgfVxuICB9O1xuICB2b2lkIGNvbnRleHQucmVhZHkudGhlbigoKSA9PiB7XG4gICAgY29udGV4dC5tb2RlbC5zdGF0ZUNoYW5nZWQuY29ubmVjdChvblN0YXRlQ2hhbmdlZCk7XG4gICAgaWYgKGNvbnRleHQubW9kZWwuZGlydHkpIHtcbiAgICAgIGRpc3Bvc2FibGUgPSBzdGF0dXMuc2V0RGlydHkoKTtcbiAgICB9XG4gIH0pO1xuICBjb250ZXh0LmRpc3Bvc2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgIGlmIChkaXNwb3NhYmxlKSB7XG4gICAgICBkaXNwb3NhYmxlLmRpc3Bvc2UoKTtcbiAgICB9XG4gIH0pO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIG1vZHVsZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBIGNvdW50ZXIgZm9yIHVuaXF1ZSBJRHMuXG4gICAqL1xuICBleHBvcnQgbGV0IGlkID0gMDtcblxuICBleHBvcnQgZnVuY3Rpb24gY3JlYXRlUmV2ZXJ0Q29uZmlybU5vZGUoXG4gICAgY2hlY2twb2ludDogQ29udGVudHMuSUNoZWNrcG9pbnRNb2RlbCxcbiAgICBmaWxlVHlwZTogc3RyaW5nLFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApOiBIVE1MRWxlbWVudCB7XG4gICAgY29uc3QgYm9keSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIGNvbnN0IGNvbmZpcm1NZXNzYWdlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgncCcpO1xuICAgIGNvbnN0IGNvbmZpcm1UZXh0ID0gZG9jdW1lbnQuY3JlYXRlVGV4dE5vZGUoXG4gICAgICB0cmFucy5fXyhcbiAgICAgICAgJ0FyZSB5b3Ugc3VyZSB5b3Ugd2FudCB0byByZXZlcnQgdGhlICUxIHRvIHRoZSBsYXRlc3QgY2hlY2twb2ludD8gJyxcbiAgICAgICAgZmlsZVR5cGVcbiAgICAgIClcbiAgICApO1xuICAgIGNvbnN0IGNhbm5vdFVuZG9UZXh0ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnc3Ryb25nJyk7XG4gICAgY2Fubm90VW5kb1RleHQudGV4dENvbnRlbnQgPSB0cmFucy5fXygnVGhpcyBjYW5ub3QgYmUgdW5kb25lLicpO1xuXG4gICAgY29uZmlybU1lc3NhZ2UuYXBwZW5kQ2hpbGQoY29uZmlybVRleHQpO1xuICAgIGNvbmZpcm1NZXNzYWdlLmFwcGVuZENoaWxkKGNhbm5vdFVuZG9UZXh0KTtcblxuICAgIGNvbnN0IGxhc3RDaGVja3BvaW50TWVzc2FnZSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ3AnKTtcbiAgICBjb25zdCBsYXN0Q2hlY2twb2ludFRleHQgPSBkb2N1bWVudC5jcmVhdGVUZXh0Tm9kZShcbiAgICAgIHRyYW5zLl9fKCdUaGUgY2hlY2twb2ludCB3YXMgbGFzdCB1cGRhdGVkIGF0OiAnKVxuICAgICk7XG4gICAgY29uc3QgbGFzdENoZWNrcG9pbnREYXRlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgncCcpO1xuICAgIGNvbnN0IGRhdGUgPSBuZXcgRGF0ZShjaGVja3BvaW50Lmxhc3RfbW9kaWZpZWQpO1xuICAgIGxhc3RDaGVja3BvaW50RGF0ZS5zdHlsZS50ZXh0QWxpZ24gPSAnY2VudGVyJztcbiAgICBsYXN0Q2hlY2twb2ludERhdGUudGV4dENvbnRlbnQgPVxuICAgICAgVGltZS5mb3JtYXQoZGF0ZSwgJ2RkZGQsIE1NTU0gRG8gWVlZWSwgaDptbTpzcyBhJykgK1xuICAgICAgJyAoJyArXG4gICAgICBUaW1lLmZvcm1hdEh1bWFuKGRhdGUpICtcbiAgICAgICcpJztcblxuICAgIGxhc3RDaGVja3BvaW50TWVzc2FnZS5hcHBlbmRDaGlsZChsYXN0Q2hlY2twb2ludFRleHQpO1xuICAgIGxhc3RDaGVja3BvaW50TWVzc2FnZS5hcHBlbmRDaGlsZChsYXN0Q2hlY2twb2ludERhdGUpO1xuXG4gICAgYm9keS5hcHBlbmRDaGlsZChjb25maXJtTWVzc2FnZSk7XG4gICAgYm9keS5hcHBlbmRDaGlsZChsYXN0Q2hlY2twb2ludE1lc3NhZ2UpO1xuICAgIHJldHVybiBib2R5O1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9