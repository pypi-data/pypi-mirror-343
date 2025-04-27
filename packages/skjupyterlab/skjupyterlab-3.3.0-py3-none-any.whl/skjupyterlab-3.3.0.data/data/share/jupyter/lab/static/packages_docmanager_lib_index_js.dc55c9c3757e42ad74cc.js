(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_docmanager_lib_index_js"],{

/***/ "../packages/docmanager/lib/dialogs.js":
/*!*********************************************!*\
  !*** ../packages/docmanager/lib/dialogs.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "renameDialog": () => (/* binding */ renameDialog),
/* harmony export */   "renameFile": () => (/* binding */ renameFile),
/* harmony export */   "shouldOverwrite": () => (/* binding */ shouldOverwrite),
/* harmony export */   "isValidFileName": () => (/* binding */ isValidFileName)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * The class name added to file dialogs.
 */
const FILE_DIALOG_CLASS = 'jp-FileDialog';
/**
 * The class name added for the new name label in the rename dialog
 */
const RENAME_NEW_NAME_TITLE_CLASS = 'jp-new-name-title';
/**
 * Rename a file with a dialog.
 */
function renameDialog(manager, oldPath, translator) {
    translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
    const trans = translator.load('jupyterlab');
    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
        title: trans.__('Rename File'),
        body: new RenameHandler(oldPath),
        focusNodeSelector: 'input',
        buttons: [
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: trans.__('Cancel') }),
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: trans.__('Rename') })
        ]
    }).then(result => {
        if (!result.value) {
            return null;
        }
        if (!isValidFileName(result.value)) {
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)(trans.__('Rename Error'), Error(trans.__('"%1" is not a valid name for a file. Names must have nonzero length, and cannot include "/", "\\", or ":"', result.value)));
            return null;
        }
        const basePath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.dirname(oldPath);
        const newPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(basePath, result.value);
        return renameFile(manager, oldPath, newPath);
    });
}
/**
 * Rename a file, asking for confirmation if it is overwriting another.
 */
function renameFile(manager, oldPath, newPath) {
    return manager.rename(oldPath, newPath).catch(error => {
        if (error.message.indexOf('409') === -1) {
            throw error;
        }
        return shouldOverwrite(newPath).then(value => {
            if (value) {
                return manager.overwrite(oldPath, newPath);
            }
            return Promise.reject('File not renamed');
        });
    });
}
/**
 * Ask the user whether to overwrite a file.
 */
function shouldOverwrite(path, translator) {
    translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
    const trans = translator.load('jupyterlab');
    const options = {
        title: trans.__('Overwrite file?'),
        body: trans.__('"%1" already exists, overwrite?', path),
        buttons: [
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: trans.__('Cancel') }),
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: trans.__('Overwrite') })
        ]
    };
    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)(options).then(result => {
        return Promise.resolve(result.button.accept);
    });
}
/**
 * Test whether a name is a valid file name
 *
 * Disallows "/", "\", and ":" in file names, as well as names with zero length.
 */
function isValidFileName(name) {
    const validNameExp = /[\/\\:]/;
    return name.length > 0 && !validNameExp.test(name);
}
/**
 * A widget used to rename a file.
 */
class RenameHandler extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    /**
     * Construct a new "rename" dialog.
     */
    constructor(oldPath) {
        super({ node: Private.createRenameNode(oldPath) });
        this.addClass(FILE_DIALOG_CLASS);
        const ext = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.extname(oldPath);
        const value = (this.inputNode.value = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(oldPath));
        this.inputNode.setSelectionRange(0, value.length - ext.length);
    }
    /**
     * Get the input text node.
     */
    get inputNode() {
        return this.node.getElementsByTagName('input')[0];
    }
    /**
     * Get the value of the widget.
     */
    getValue() {
        return this.inputNode.value;
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Create the node for a rename handler.
     */
    function createRenameNode(oldPath, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const body = document.createElement('div');
        const existingLabel = document.createElement('label');
        existingLabel.textContent = trans.__('File Path');
        const existingPath = document.createElement('span');
        existingPath.textContent = oldPath;
        const nameTitle = document.createElement('label');
        nameTitle.textContent = trans.__('New Name');
        nameTitle.className = RENAME_NEW_NAME_TITLE_CLASS;
        const name = document.createElement('input');
        body.appendChild(existingLabel);
        body.appendChild(existingPath);
        body.appendChild(nameTitle);
        body.appendChild(name);
        return body;
    }
    Private.createRenameNode = createRenameNode;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/docmanager/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/docmanager/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "isValidFileName": () => (/* reexport safe */ _dialogs__WEBPACK_IMPORTED_MODULE_0__.isValidFileName),
/* harmony export */   "renameDialog": () => (/* reexport safe */ _dialogs__WEBPACK_IMPORTED_MODULE_0__.renameDialog),
/* harmony export */   "renameFile": () => (/* reexport safe */ _dialogs__WEBPACK_IMPORTED_MODULE_0__.renameFile),
/* harmony export */   "shouldOverwrite": () => (/* reexport safe */ _dialogs__WEBPACK_IMPORTED_MODULE_0__.shouldOverwrite),
/* harmony export */   "DocumentManager": () => (/* reexport safe */ _manager__WEBPACK_IMPORTED_MODULE_1__.DocumentManager),
/* harmony export */   "PathStatus": () => (/* reexport safe */ _pathstatus__WEBPACK_IMPORTED_MODULE_2__.PathStatus),
/* harmony export */   "SaveHandler": () => (/* reexport safe */ _savehandler__WEBPACK_IMPORTED_MODULE_3__.SaveHandler),
/* harmony export */   "SavingStatus": () => (/* reexport safe */ _savingstatus__WEBPACK_IMPORTED_MODULE_4__.SavingStatus),
/* harmony export */   "IDocumentManager": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_5__.IDocumentManager),
/* harmony export */   "DocumentWidgetManager": () => (/* reexport safe */ _widgetmanager__WEBPACK_IMPORTED_MODULE_6__.DocumentWidgetManager)
/* harmony export */ });
/* harmony import */ var _dialogs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./dialogs */ "../packages/docmanager/lib/dialogs.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./manager */ "../packages/docmanager/lib/manager.js");
/* harmony import */ var _pathstatus__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./pathstatus */ "../packages/docmanager/lib/pathstatus.js");
/* harmony import */ var _savehandler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./savehandler */ "../packages/docmanager/lib/savehandler.js");
/* harmony import */ var _savingstatus__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./savingstatus */ "../packages/docmanager/lib/savingstatus.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tokens */ "../packages/docmanager/lib/tokens.js");
/* harmony import */ var _widgetmanager__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widgetmanager */ "../packages/docmanager/lib/widgetmanager.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module docmanager
 */









/***/ }),

/***/ "../packages/docmanager/lib/manager.js":
/*!*********************************************!*\
  !*** ../packages/docmanager/lib/manager.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DocumentManager": () => (/* binding */ DocumentManager)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _savehandler__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./savehandler */ "../packages/docmanager/lib/savehandler.js");
/* harmony import */ var _widgetmanager__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./widgetmanager */ "../packages/docmanager/lib/widgetmanager.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.










/**
 * The document manager.
 *
 * #### Notes
 * The document manager is used to register model and widget creators,
 * and the file browser uses the document manager to create widgets. The
 * document manager maintains a context for each path and model type that is
 * open, and a list of widgets for each context. The document manager is in
 * control of the proper closing and disposal of the widgets and contexts.
 */
class DocumentManager {
    /**
     * Construct a new document manager.
     */
    constructor(options) {
        this._activateRequested = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_7__.Signal(this);
        this._contexts = [];
        this._isDisposed = false;
        this._autosave = true;
        this._autosaveInterval = 120;
        this._lastModifiedCheckMargin = 500;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        this.registry = options.registry;
        this.services = options.manager;
        this._collaborative = !!options.collaborative;
        this._dialogs = options.sessionDialogs || _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.sessionContextDialogs;
        this._docProviderFactory = options.docProviderFactory;
        this._opener = options.opener;
        this._when = options.when || options.manager.ready;
        const widgetManager = new _widgetmanager__WEBPACK_IMPORTED_MODULE_8__.DocumentWidgetManager({
            registry: this.registry,
            translator: this.translator
        });
        widgetManager.activateRequested.connect(this._onActivateRequested, this);
        this._widgetManager = widgetManager;
        this._setBusy = options.setBusy;
    }
    /**
     * A signal emitted when one of the documents is activated.
     */
    get activateRequested() {
        return this._activateRequested;
    }
    /**
     * Whether to autosave documents.
     */
    get autosave() {
        return this._autosave;
    }
    set autosave(value) {
        this._autosave = value;
        // For each existing context, start/stop the autosave handler as needed.
        this._contexts.forEach(context => {
            const handler = Private.saveHandlerProperty.get(context);
            if (!handler) {
                return;
            }
            if (value === true && !handler.isActive) {
                handler.start();
            }
            else if (value === false && handler.isActive) {
                handler.stop();
            }
        });
    }
    /**
     * Determines the time interval for autosave in seconds.
     */
    get autosaveInterval() {
        return this._autosaveInterval;
    }
    set autosaveInterval(value) {
        this._autosaveInterval = value;
        // For each existing context, set the save interval as needed.
        this._contexts.forEach(context => {
            const handler = Private.saveHandlerProperty.get(context);
            if (!handler) {
                return;
            }
            handler.saveInterval = value || 120;
        });
    }
    /**
     * Defines max acceptable difference, in milliseconds, between last modified timestamps on disk and client
     */
    get lastModifiedCheckMargin() {
        return this._lastModifiedCheckMargin;
    }
    set lastModifiedCheckMargin(value) {
        this._lastModifiedCheckMargin = value;
        // For each existing context, update the margin value.
        this._contexts.forEach(context => {
            context.lastModifiedCheckMargin = value;
        });
    }
    /**
     * Get whether the document manager has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the document manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        // Clear any listeners for our signals.
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_7__.Signal.clearData(this);
        // Close all the widgets for our contexts and dispose the widget manager.
        this._contexts.forEach(context => {
            return this._widgetManager.closeWidgets(context);
        });
        this._widgetManager.dispose();
        // Clear the context list.
        this._contexts.length = 0;
    }
    /**
     * Clone a widget.
     *
     * @param widget - The source widget.
     *
     * @returns A new widget or `undefined`.
     *
     * #### Notes
     *  Uses the same widget factory and context as the source, or returns
     *  `undefined` if the source widget is not managed by this manager.
     */
    cloneWidget(widget) {
        return this._widgetManager.cloneWidget(widget);
    }
    /**
     * Close all of the open documents.
     *
     * @returns A promise resolving when the widgets are closed.
     */
    closeAll() {
        return Promise.all(this._contexts.map(context => this._widgetManager.closeWidgets(context))).then(() => undefined);
    }
    /**
     * Close the widgets associated with a given path.
     *
     * @param path - The target path.
     *
     * @returns A promise resolving when the widgets are closed.
     */
    closeFile(path) {
        const close = this._contextsForPath(path).map(c => this._widgetManager.closeWidgets(c));
        return Promise.all(close).then(x => undefined);
    }
    /**
     * Get the document context for a widget.
     *
     * @param widget - The widget of interest.
     *
     * @returns The context associated with the widget, or `undefined` if no such
     * context exists.
     */
    contextForWidget(widget) {
        return this._widgetManager.contextForWidget(widget);
    }
    /**
     * Copy a file.
     *
     * @param fromFile - The full path of the original file.
     *
     * @param toDir - The full path to the target directory.
     *
     * @returns A promise which resolves to the contents of the file.
     */
    copy(fromFile, toDir) {
        return this.services.contents.copy(fromFile, toDir);
    }
    /**
     * Create a new file and return the widget used to view it.
     *
     * @param path - The file path to create.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    createNew(path, widgetName = 'default', kernel) {
        return this._createOrOpenDocument('create', path, widgetName, kernel);
    }
    /**
     * Delete a file.
     *
     * @param path - The full path to the file to be deleted.
     *
     * @returns A promise which resolves when the file is deleted.
     *
     * #### Notes
     * If there is a running session associated with the file and no other
     * sessions are using the kernel, the session will be shut down.
     */
    deleteFile(path) {
        return this.services.sessions
            .stopIfNeeded(path)
            .then(() => {
            return this.services.contents.delete(path);
        })
            .then(() => {
            this._contextsForPath(path).forEach(context => this._widgetManager.deleteWidgets(context));
            return Promise.resolve(void 0);
        });
    }
    /**
     * See if a widget already exists for the given path and widget name.
     *
     * @param path - The file path to use.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @returns The found widget, or `undefined`.
     *
     * #### Notes
     * This can be used to find an existing widget instead of opening
     * a new widget.
     */
    findWidget(path, widgetName = 'default') {
        const newPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.normalize(path);
        let widgetNames = [widgetName];
        if (widgetName === 'default') {
            const factory = this.registry.defaultWidgetFactory(newPath);
            if (!factory) {
                return undefined;
            }
            widgetNames = [factory.name];
        }
        else if (widgetName === null) {
            widgetNames = this.registry
                .preferredWidgetFactories(newPath)
                .map(f => f.name);
        }
        for (const context of this._contextsForPath(newPath)) {
            for (const widgetName of widgetNames) {
                if (widgetName !== null) {
                    const widget = this._widgetManager.findWidget(context, widgetName);
                    if (widget) {
                        return widget;
                    }
                }
            }
        }
        return undefined;
    }
    /**
     * Create a new untitled file.
     *
     * @param options - The file content creation options.
     */
    newUntitled(options) {
        if (options.type === 'file') {
            options.ext = options.ext || '.txt';
        }
        return this.services.contents.newUntitled(options);
    }
    /**
     * Open a file and return the widget used to view it.
     *
     * @param path - The file path to open.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    open(path, widgetName = 'default', kernel, options) {
        return this._createOrOpenDocument('open', path, widgetName, kernel, options);
    }
    /**
     * Open a file and return the widget used to view it.
     * Reveals an already existing editor.
     *
     * @param path - The file path to open.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    openOrReveal(path, widgetName = 'default', kernel, options) {
        const widget = this.findWidget(path, widgetName);
        if (widget) {
            this._opener.open(widget, options || {});
            return widget;
        }
        return this.open(path, widgetName, kernel, options || {});
    }
    /**
     * Overwrite a file.
     *
     * @param oldPath - The full path to the original file.
     *
     * @param newPath - The full path to the new file.
     *
     * @returns A promise containing the new file contents model.
     */
    overwrite(oldPath, newPath) {
        // Cleanly overwrite the file by moving it, making sure the original does
        // not exist, and then renaming to the new path.
        const tempPath = `${newPath}.${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.UUID.uuid4()}`;
        const cb = () => this.rename(tempPath, newPath);
        return this.rename(oldPath, tempPath)
            .then(() => {
            return this.deleteFile(newPath);
        })
            .then(cb, cb);
    }
    /**
     * Rename a file or directory.
     *
     * @param oldPath - The full path to the original file.
     *
     * @param newPath - The full path to the new file.
     *
     * @returns A promise containing the new file contents model.  The promise
     * will reject if the newPath already exists.  Use [[overwrite]] to overwrite
     * a file.
     */
    rename(oldPath, newPath) {
        return this.services.contents.rename(oldPath, newPath);
    }
    /**
     * Find a context for a given path and factory name.
     */
    _findContext(path, factoryName) {
        const normalizedPath = this.services.contents.normalize(path);
        return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.find)(this._contexts, context => {
            return (context.path === normalizedPath && context.factoryName === factoryName);
        });
    }
    /**
     * Get the contexts for a given path.
     *
     * #### Notes
     * There may be more than one context for a given path if the path is open
     * with multiple model factories (for example, a notebook can be open with a
     * notebook model factory and a text model factory).
     */
    _contextsForPath(path) {
        const normalizedPath = this.services.contents.normalize(path);
        return this._contexts.filter(context => context.path === normalizedPath);
    }
    /**
     * Create a context from a path and a model factory.
     */
    _createContext(path, factory, kernelPreference) {
        // TODO: Make it impossible to open two different contexts for the same
        // path. Or at least prompt the closing of all widgets associated with the
        // old context before opening the new context. This will make things much
        // more consistent for the users, at the cost of some confusion about what
        // models are and why sometimes they cannot open the same file in different
        // widgets that have different models.
        // Allow options to be passed when adding a sibling.
        const adopter = (widget, options) => {
            this._widgetManager.adoptWidget(context, widget);
            this._opener.open(widget, options);
        };
        const modelDBFactory = this.services.contents.getModelDBFactory(path) || undefined;
        const context = new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.Context({
            opener: adopter,
            manager: this.services,
            factory,
            path,
            kernelPreference,
            modelDBFactory,
            setBusy: this._setBusy,
            sessionDialogs: this._dialogs,
            collaborative: this._collaborative,
            docProviderFactory: this._docProviderFactory,
            lastModifiedCheckMargin: this._lastModifiedCheckMargin
        });
        const handler = new _savehandler__WEBPACK_IMPORTED_MODULE_9__.SaveHandler({
            context,
            saveInterval: this.autosaveInterval
        });
        Private.saveHandlerProperty.set(context, handler);
        void context.ready.then(() => {
            if (this.autosave) {
                handler.start();
            }
        });
        context.disposed.connect(this._onContextDisposed, this);
        this._contexts.push(context);
        return context;
    }
    /**
     * Handle a context disposal.
     */
    _onContextDisposed(context) {
        _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.ArrayExt.removeFirstOf(this._contexts, context);
    }
    /**
     * Get the widget factory for a given widget name.
     */
    _widgetFactoryFor(path, widgetName) {
        const { registry } = this;
        if (widgetName === 'default') {
            const factory = registry.defaultWidgetFactory(path);
            if (!factory) {
                return undefined;
            }
            widgetName = factory.name;
        }
        return registry.getWidgetFactory(widgetName);
    }
    /**
     * Creates a new document, or loads one from disk, depending on the `which` argument.
     * If `which==='create'`, then it creates a new document. If `which==='open'`,
     * then it loads the document from disk.
     *
     * The two cases differ in how the document context is handled, but the creation
     * of the widget and launching of the kernel are identical.
     */
    _createOrOpenDocument(which, path, widgetName = 'default', kernel, options) {
        const widgetFactory = this._widgetFactoryFor(path, widgetName);
        if (!widgetFactory) {
            return undefined;
        }
        const modelName = widgetFactory.modelName || 'text';
        const factory = this.registry.getModelFactory(modelName);
        if (!factory) {
            return undefined;
        }
        // Handle the kernel preference.
        const preference = this.registry.getKernelPreference(path, widgetFactory.name, kernel);
        let context;
        let ready = Promise.resolve(undefined);
        // Handle the load-from-disk case
        if (which === 'open') {
            // Use an existing context if available.
            context = this._findContext(path, factory.name) || null;
            if (!context) {
                context = this._createContext(path, factory, preference);
                // Populate the model, either from disk or a
                // model backend.
                ready = this._when.then(() => context.initialize(false));
            }
        }
        else if (which === 'create') {
            context = this._createContext(path, factory, preference);
            // Immediately save the contents to disk.
            ready = this._when.then(() => context.initialize(true));
        }
        else {
            throw new Error(`Invalid argument 'which': ${which}`);
        }
        const widget = this._widgetManager.createWidget(widgetFactory, context);
        this._opener.open(widget, options || {});
        // If the initial opening of the context fails, dispose of the widget.
        ready.catch(err => {
            widget.close();
        });
        return widget;
    }
    /**
     * Handle an activateRequested signal from the widget manager.
     */
    _onActivateRequested(sender, args) {
        this._activateRequested.emit(args);
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property for a context save handler.
     */
    Private.saveHandlerProperty = new _lumino_properties__WEBPACK_IMPORTED_MODULE_6__.AttachedProperty({
        name: 'saveHandler',
        create: () => undefined
    });
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/docmanager/lib/pathstatus.js":
/*!************************************************!*\
  !*** ../packages/docmanager/lib/pathstatus.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PathStatus": () => (/* binding */ PathStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A pure component for rendering a file path (or activity name).
 *
 * @param props - the props for the component.
 *
 * @returns a tsx component for a file path.
 */
function PathStatusComponent(props) {
    return react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__.TextItem, { source: props.name, title: props.fullPath });
}
/**
 * A status bar item for the current file path (or activity name).
 */
class PathStatus extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Construct a new PathStatus status item.
     */
    constructor(opts) {
        super(new PathStatus.Model(opts.docManager));
        this.node.title = this.model.path;
    }
    /**
     * Render the status item.
     */
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(PathStatusComponent, { fullPath: this.model.path, name: this.model.name }));
    }
}
/**
 * A namespace for PathStatus statics.
 */
(function (PathStatus) {
    /**
     * A VDomModel for rendering the PathStatus status item.
     */
    class Model extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
        /**
         * Construct a new model.
         *
         * @param docManager: the application document manager. Used to check
         *   whether the current widget is a document.
         */
        constructor(docManager) {
            super();
            /**
             * React to a title change for the current widget.
             */
            this._onTitleChange = (title) => {
                const oldState = this._getAllState();
                this._name = title.label;
                this._triggerChange(oldState, this._getAllState());
            };
            /**
             * React to a path change for the current document.
             */
            this._onPathChange = (_documentModel, newPath) => {
                const oldState = this._getAllState();
                this._path = newPath;
                this._name = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(newPath);
                this._triggerChange(oldState, this._getAllState());
            };
            this._path = '';
            this._name = '';
            this._widget = null;
            this._docManager = docManager;
        }
        /**
         * The current path for the application.
         */
        get path() {
            return this._path;
        }
        /**
         * The name of the current activity.
         */
        get name() {
            return this._name;
        }
        /**
         * The current widget for the application.
         */
        get widget() {
            return this._widget;
        }
        set widget(widget) {
            const oldWidget = this._widget;
            if (oldWidget !== null) {
                const oldContext = this._docManager.contextForWidget(oldWidget);
                if (oldContext) {
                    oldContext.pathChanged.disconnect(this._onPathChange);
                }
                else {
                    oldWidget.title.changed.disconnect(this._onTitleChange);
                }
            }
            const oldState = this._getAllState();
            this._widget = widget;
            if (this._widget === null) {
                this._path = '';
                this._name = '';
            }
            else {
                const widgetContext = this._docManager.contextForWidget(this._widget);
                if (widgetContext) {
                    this._path = widgetContext.path;
                    this._name = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(widgetContext.path);
                    widgetContext.pathChanged.connect(this._onPathChange);
                }
                else {
                    this._path = '';
                    this._name = this._widget.title.label;
                    this._widget.title.changed.connect(this._onTitleChange);
                }
            }
            this._triggerChange(oldState, this._getAllState());
        }
        /**
         * Get the current state of the model.
         */
        _getAllState() {
            return [this._path, this._name];
        }
        /**
         * Trigger a state change to rerender.
         */
        _triggerChange(oldState, newState) {
            if (oldState[0] !== newState[0] || oldState[1] !== newState[1]) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    PathStatus.Model = Model;
})(PathStatus || (PathStatus = {}));


/***/ }),

/***/ "../packages/docmanager/lib/savehandler.js":
/*!*************************************************!*\
  !*** ../packages/docmanager/lib/savehandler.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SaveHandler": () => (/* binding */ SaveHandler)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A class that manages the auto saving of a document.
 *
 * #### Notes
 * Implements https://github.com/ipython/ipython/wiki/IPEP-15:-Autosaving-the-IPython-Notebook.
 */
class SaveHandler {
    /**
     * Construct a new save handler.
     */
    constructor(options) {
        this._autosaveTimer = -1;
        this._minInterval = -1;
        this._interval = -1;
        this._isActive = false;
        this._inDialog = false;
        this._isDisposed = false;
        this._multiplier = 10;
        this._context = options.context;
        const interval = options.saveInterval || 120;
        this._minInterval = interval * 1000;
        this._interval = this._minInterval;
        // Restart the timer when the contents model is updated.
        this._context.fileChanged.connect(this._setTimer, this);
        this._context.disposed.connect(this.dispose, this);
    }
    /**
     * The save interval used by the timer (in seconds).
     */
    get saveInterval() {
        return this._interval / 1000;
    }
    set saveInterval(value) {
        this._minInterval = this._interval = value * 1000;
        if (this._isActive) {
            this._setTimer();
        }
    }
    /**
     * Get whether the handler is active.
     */
    get isActive() {
        return this._isActive;
    }
    /**
     * Get whether the save handler is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the save handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        clearTimeout(this._autosaveTimer);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
    /**
     * Start the autosaver.
     */
    start() {
        this._isActive = true;
        this._setTimer();
    }
    /**
     * Stop the autosaver.
     */
    stop() {
        this._isActive = false;
        clearTimeout(this._autosaveTimer);
    }
    /**
     * Set the timer.
     */
    _setTimer() {
        clearTimeout(this._autosaveTimer);
        if (!this._isActive) {
            return;
        }
        this._autosaveTimer = window.setTimeout(() => {
            this._save();
        }, this._interval);
    }
    /**
     * Handle an autosave timeout.
     */
    _save() {
        const context = this._context;
        // Trigger the next update.
        this._setTimer();
        if (!context) {
            return;
        }
        // Bail if the model is not dirty or the file is not writable, or the dialog
        // is already showing.
        const writable = context.contentsModel && context.contentsModel.writable;
        if (!writable || !context.model.dirty || this._inDialog) {
            return;
        }
        const start = new Date().getTime();
        context
            .save()
            .then(() => {
            if (this.isDisposed) {
                return;
            }
            const duration = new Date().getTime() - start;
            // New save interval: higher of 10x save duration or min interval.
            this._interval = Math.max(this._multiplier * duration, this._minInterval);
            // Restart the update to pick up the new interval.
            this._setTimer();
        })
            .catch(err => {
            // If the user canceled the save, do nothing.
            // FIXME-TRANS: Is this affected by localization?
            if (err.message === 'Cancel') {
                return;
            }
            // Otherwise, log the error.
            console.error('Error in Auto-Save', err.message);
        });
    }
}


/***/ }),

/***/ "../packages/docmanager/lib/savingstatus.js":
/*!**************************************************!*\
  !*** ../packages/docmanager/lib/savingstatus.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SavingStatus": () => (/* binding */ SavingStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A pure functional component for a Saving status item.
 *
 * @param props - the props for the component.
 *
 * @returns a tsx component for rendering the saving state.
 */
function SavingStatusComponent(props) {
    return react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { source: props.fileStatus });
}
/**
 * The amount of time (in ms) to retain the saving completed message
 * before hiding the status item.
 */
const SAVING_COMPLETE_MESSAGE_MILLIS = 2000;
/**
 * A VDomRenderer for a saving status item.
 */
class SavingStatus extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Create a new SavingStatus item.
     */
    constructor(opts) {
        super(new SavingStatus.Model(opts.docManager));
        const translator = opts.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        this._statusMap = {
            completed: trans.__('Saving completed'),
            started: trans.__('Saving started'),
            failed: trans.__('Saving failed')
        };
    }
    /**
     * Render the SavingStatus item.
     */
    render() {
        if (this.model === null || this.model.status === null) {
            return null;
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(SavingStatusComponent, { fileStatus: this._statusMap[this.model.status] }));
        }
    }
}
/**
 * A namespace for SavingStatus statics.
 */
(function (SavingStatus) {
    /**
     * A VDomModel for the SavingStatus item.
     */
    class Model extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
        /**
         * Create a new SavingStatus model.
         */
        constructor(docManager) {
            super();
            /**
             * React to a saving status change from the current document widget.
             */
            this._onStatusChange = (_documentModel, newStatus) => {
                this._status = newStatus;
                if (this._status === 'completed') {
                    setTimeout(() => {
                        this._status = null;
                        this.stateChanged.emit(void 0);
                    }, SAVING_COMPLETE_MESSAGE_MILLIS);
                    this.stateChanged.emit(void 0);
                }
                else {
                    this.stateChanged.emit(void 0);
                }
            };
            this._status = null;
            this._widget = null;
            this._status = null;
            this.widget = null;
            this._docManager = docManager;
        }
        /**
         * The current status of the model.
         */
        get status() {
            return this._status;
        }
        /**
         * The current widget for the model. Any widget can be assigned,
         * but it only has any effect if the widget is an IDocument widget
         * known to the application document manager.
         */
        get widget() {
            return this._widget;
        }
        set widget(widget) {
            const oldWidget = this._widget;
            if (oldWidget !== null) {
                const oldContext = this._docManager.contextForWidget(oldWidget);
                if (oldContext) {
                    oldContext.saveState.disconnect(this._onStatusChange);
                }
            }
            this._widget = widget;
            if (this._widget === null) {
                this._status = null;
            }
            else {
                const widgetContext = this._docManager.contextForWidget(this._widget);
                if (widgetContext) {
                    widgetContext.saveState.connect(this._onStatusChange);
                }
            }
        }
    }
    SavingStatus.Model = Model;
})(SavingStatus || (SavingStatus = {}));


/***/ }),

/***/ "../packages/docmanager/lib/tokens.js":
/*!********************************************!*\
  !*** ../packages/docmanager/lib/tokens.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IDocumentManager": () => (/* binding */ IDocumentManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The document registry token.
 */
const IDocumentManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/docmanager:IDocumentManager');


/***/ }),

/***/ "../packages/docmanager/lib/widgetmanager.js":
/*!***************************************************!*\
  !*** ../packages/docmanager/lib/widgetmanager.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DocumentWidgetManager": () => (/* binding */ DocumentWidgetManager)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging/@lumino/messaging");
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_messaging__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to document widgets.
 */
const DOCUMENT_CLASS = 'jp-Document';
/**
 * A class that maintains the lifecycle of file-backed widgets.
 */
class DocumentWidgetManager {
    /**
     * Construct a new document widget manager.
     */
    constructor(options) {
        this._activateRequested = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_7__.Signal(this);
        this._isDisposed = false;
        this._registry = options.registry;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
    }
    /**
     * A signal emitted when one of the documents is activated.
     */
    get activateRequested() {
        return this._activateRequested;
    }
    /**
     * Test whether the document widget manager is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the widget manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_7__.Signal.disconnectReceiver(this);
    }
    /**
     * Create a widget for a document and handle its lifecycle.
     *
     * @param factory - The widget factory.
     *
     * @param context - The document context object.
     *
     * @returns A widget created by the factory.
     *
     * @throws If the factory is not registered.
     */
    createWidget(factory, context) {
        const widget = factory.createNew(context);
        this._initializeWidget(widget, factory, context);
        return widget;
    }
    /**
     * When a new widget is created, we need to hook it up
     * with some signals, update the widget extensions (for
     * this kind of widget) in the docregistry, among
     * other things.
     */
    _initializeWidget(widget, factory, context) {
        Private.factoryProperty.set(widget, factory);
        // Handle widget extensions.
        const disposables = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__.DisposableSet();
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(this._registry.widgetExtensions(factory.name), extender => {
            const disposable = extender.createNew(widget, context);
            if (disposable) {
                disposables.add(disposable);
            }
        });
        Private.disposablesProperty.set(widget, disposables);
        widget.disposed.connect(this._onWidgetDisposed, this);
        this.adoptWidget(context, widget);
        context.fileChanged.connect(this._onFileChanged, this);
        context.pathChanged.connect(this._onPathChanged, this);
        void context.ready.then(() => {
            void this.setCaption(widget);
        });
    }
    /**
     * Install the message hook for the widget and add to list
     * of known widgets.
     *
     * @param context - The document context object.
     *
     * @param widget - The widget to adopt.
     */
    adoptWidget(context, widget) {
        const widgets = Private.widgetsProperty.get(context);
        widgets.push(widget);
        _lumino_messaging__WEBPACK_IMPORTED_MODULE_5__.MessageLoop.installMessageHook(widget, this);
        widget.addClass(DOCUMENT_CLASS);
        widget.title.closable = true;
        widget.disposed.connect(this._widgetDisposed, this);
        Private.contextProperty.set(widget, context);
    }
    /**
     * See if a widget already exists for the given context and widget name.
     *
     * @param context - The document context object.
     *
     * @returns The found widget, or `undefined`.
     *
     * #### Notes
     * This can be used to use an existing widget instead of opening
     * a new widget.
     */
    findWidget(context, widgetName) {
        const widgets = Private.widgetsProperty.get(context);
        if (!widgets) {
            return undefined;
        }
        return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.find)(widgets, widget => {
            const factory = Private.factoryProperty.get(widget);
            if (!factory) {
                return false;
            }
            return factory.name === widgetName;
        });
    }
    /**
     * Get the document context for a widget.
     *
     * @param widget - The widget of interest.
     *
     * @returns The context associated with the widget, or `undefined`.
     */
    contextForWidget(widget) {
        return Private.contextProperty.get(widget);
    }
    /**
     * Clone a widget.
     *
     * @param widget - The source widget.
     *
     * @returns A new widget or `undefined`.
     *
     * #### Notes
     *  Uses the same widget factory and context as the source, or throws
     *  if the source widget is not managed by this manager.
     */
    cloneWidget(widget) {
        const context = Private.contextProperty.get(widget);
        if (!context) {
            return undefined;
        }
        const factory = Private.factoryProperty.get(widget);
        if (!factory) {
            return undefined;
        }
        const newWidget = factory.createNew(context, widget);
        this._initializeWidget(newWidget, factory, context);
        return newWidget;
    }
    /**
     * Close the widgets associated with a given context.
     *
     * @param context - The document context object.
     */
    closeWidgets(context) {
        const widgets = Private.widgetsProperty.get(context);
        return Promise.all((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.toArray)((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.map)(widgets, widget => this.onClose(widget)))).then(() => undefined);
    }
    /**
     * Dispose of the widgets associated with a given context
     * regardless of the widget's dirty state.
     *
     * @param context - The document context object.
     */
    deleteWidgets(context) {
        const widgets = Private.widgetsProperty.get(context);
        return Promise.all((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.toArray)((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.map)(widgets, widget => this.onDelete(widget)))).then(() => undefined);
    }
    /**
     * Filter a message sent to a message handler.
     *
     * @param handler - The target handler of the message.
     *
     * @param msg - The message dispatched to the handler.
     *
     * @returns `false` if the message should be filtered, of `true`
     *   if the message should be dispatched to the handler as normal.
     */
    messageHook(handler, msg) {
        switch (msg.type) {
            case 'close-request':
                void this.onClose(handler);
                return false;
            case 'activate-request': {
                const context = this.contextForWidget(handler);
                if (context) {
                    this._activateRequested.emit(context.path);
                }
                break;
            }
            default:
                break;
        }
        return true;
    }
    /**
     * Set the caption for widget title.
     *
     * @param widget - The target widget.
     */
    async setCaption(widget) {
        const trans = this.translator.load('jupyterlab');
        const context = Private.contextProperty.get(widget);
        if (!context) {
            return;
        }
        const model = context.contentsModel;
        if (!model) {
            widget.title.caption = '';
            return;
        }
        return context
            .listCheckpoints()
            .then((checkpoints) => {
            if (widget.isDisposed) {
                return;
            }
            const last = checkpoints[checkpoints.length - 1];
            const checkpoint = last ? _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.Time.format(last.last_modified) : 'None';
            let caption = trans.__('Name: %1\nPath: %2\n', model.name, model.path);
            if (context.model.readOnly) {
                caption += trans.__('Read-only');
            }
            else {
                caption +=
                    trans.__('Last Saved: %1\n', _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.Time.format(model.last_modified)) +
                        trans.__('Last Checkpoint: %1', checkpoint);
            }
            widget.title.caption = caption;
        });
    }
    /**
     * Handle `'close-request'` messages.
     *
     * @param widget - The target widget.
     *
     * @returns A promise that resolves with whether the widget was closed.
     */
    async onClose(widget) {
        var _a;
        // Handle dirty state.
        const [shouldClose, ignoreSave] = await this._maybeClose(widget, this.translator);
        if (widget.isDisposed) {
            return true;
        }
        if (shouldClose) {
            if (!ignoreSave) {
                const context = Private.contextProperty.get(widget);
                if (!context) {
                    return true;
                }
                if ((_a = context.contentsModel) === null || _a === void 0 ? void 0 : _a.writable) {
                    await context.save();
                }
                else {
                    await context.saveAs();
                }
            }
            if (widget.isDisposed) {
                return true;
            }
            widget.dispose();
        }
        return shouldClose;
    }
    /**
     * Dispose of widget regardless of widget's dirty state.
     *
     * @param widget - The target widget.
     */
    onDelete(widget) {
        widget.dispose();
        return Promise.resolve(void 0);
    }
    /**
     * Ask the user whether to close an unsaved file.
     */
    _maybeClose(widget, translator) {
        var _a;
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        // Bail if the model is not dirty or other widgets are using the model.)
        const context = Private.contextProperty.get(widget);
        if (!context) {
            return Promise.resolve([true, true]);
        }
        let widgets = Private.widgetsProperty.get(context);
        if (!widgets) {
            return Promise.resolve([true, true]);
        }
        // Filter by whether the factories are read only.
        widgets = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.toArray)((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.filter)(widgets, widget => {
            const factory = Private.factoryProperty.get(widget);
            if (!factory) {
                return false;
            }
            return factory.readOnly === false;
        }));
        const factory = Private.factoryProperty.get(widget);
        if (!factory) {
            return Promise.resolve([true, true]);
        }
        const model = context.model;
        if (!model.dirty || widgets.length > 1 || factory.readOnly) {
            return Promise.resolve([true, true]);
        }
        const fileName = widget.title.label;
        const saveLabel = ((_a = context.contentsModel) === null || _a === void 0 ? void 0 : _a.writable) ? trans.__('Save')
            : trans.__('Save as');
        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
            title: trans.__('Save your work'),
            body: trans.__('Save changes in "%1" before closing?', fileName),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: trans.__('Cancel') }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: trans.__('Discard') }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: saveLabel })
            ]
        }).then(result => {
            return [result.button.accept, result.button.displayType === 'warn'];
        });
    }
    /**
     * Handle the disposal of a widget.
     */
    _widgetDisposed(widget) {
        const context = Private.contextProperty.get(widget);
        if (!context) {
            return;
        }
        const widgets = Private.widgetsProperty.get(context);
        if (!widgets) {
            return;
        }
        // Remove the widget.
        _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayExt.removeFirstOf(widgets, widget);
        // Dispose of the context if this is the last widget using it.
        if (!widgets.length) {
            context.dispose();
        }
    }
    /**
     * Handle the disposal of a widget.
     */
    _onWidgetDisposed(widget) {
        const disposables = Private.disposablesProperty.get(widget);
        disposables.dispose();
    }
    /**
     * Handle a file changed signal for a context.
     */
    _onFileChanged(context) {
        const widgets = Private.widgetsProperty.get(context);
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(widgets, widget => {
            void this.setCaption(widget);
        });
    }
    /**
     * Handle a path changed signal for a context.
     */
    _onPathChanged(context) {
        const widgets = Private.widgetsProperty.get(context);
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(widgets, widget => {
            void this.setCaption(widget);
        });
    }
}
/**
 * A private namespace for DocumentManager data.
 */
var Private;
(function (Private) {
    /**
     * A private attached property for a widget context.
     */
    Private.contextProperty = new _lumino_properties__WEBPACK_IMPORTED_MODULE_6__.AttachedProperty({
        name: 'context',
        create: () => undefined
    });
    /**
     * A private attached property for a widget factory.
     */
    Private.factoryProperty = new _lumino_properties__WEBPACK_IMPORTED_MODULE_6__.AttachedProperty({
        name: 'factory',
        create: () => undefined
    });
    /**
     * A private attached property for the widgets associated with a context.
     */
    Private.widgetsProperty = new _lumino_properties__WEBPACK_IMPORTED_MODULE_6__.AttachedProperty({
        name: 'widgets',
        create: () => []
    });
    /**
     * A private attached property for a widget's disposables.
     */
    Private.disposablesProperty = new _lumino_properties__WEBPACK_IMPORTED_MODULE_6__.AttachedProperty({
        name: 'disposables',
        create: () => new _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__.DisposableSet()
    });
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jbWFuYWdlci9zcmMvZGlhbG9ncy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jbWFuYWdlci9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2RvY21hbmFnZXIvc3JjL21hbmFnZXIudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2RvY21hbmFnZXIvc3JjL3BhdGhzdGF0dXMudHN4Iiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9kb2NtYW5hZ2VyL3NyYy9zYXZlaGFuZGxlci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jbWFuYWdlci9zcmMvc2F2aW5nc3RhdHVzLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jbWFuYWdlci9zcmMvdG9rZW5zLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9kb2NtYW5hZ2VyL3NyYy93aWRnZXRtYW5hZ2VyLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFaUI7QUFDNUI7QUFFc0I7QUFFN0I7QUFHekM7O0dBRUc7QUFDSCxNQUFNLGlCQUFpQixHQUFHLGVBQWUsQ0FBQztBQUUxQzs7R0FFRztBQUNILE1BQU0sMkJBQTJCLEdBQUcsbUJBQW1CLENBQUM7QUFnQnhEOztHQUVHO0FBQ0ksU0FBUyxZQUFZLENBQzFCLE9BQXlCLEVBQ3pCLE9B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QUFHLElBQUksZ0VBQWdCLENBR3JEO1FBQ0EsSUFBSSxFQUFFLGFBQWE7UUFDbkIsTUFBTSxFQUFFLEdBQUcsRUFBRSxDQUFDLElBQUksNkRBQWEsRUFBRTtLQUNsQyxDQUFDLENBQUM7QUFDTCxDQUFDLEVBNUNTLE9BQU8sS0FBUCxPQUFPLFFBNENoQiIsImZpbGUiOiJwYWNrYWdlc19kb2NtYW5hZ2VyX2xpYl9pbmRleF9qcy5kYzU1YzljMzc1N2U0MmFkNzRjYy5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgRGlhbG9nLCBzaG93RGlhbG9nLCBzaG93RXJyb3JNZXNzYWdlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgUGF0aEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBDb250ZW50cyB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgSURvY3VtZW50TWFuYWdlciB9IGZyb20gJy4vJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBmaWxlIGRpYWxvZ3MuXG4gKi9cbmNvbnN0IEZJTEVfRElBTE9HX0NMQVNTID0gJ2pwLUZpbGVEaWFsb2cnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIGZvciB0aGUgbmV3IG5hbWUgbGFiZWwgaW4gdGhlIHJlbmFtZSBkaWFsb2dcbiAqL1xuY29uc3QgUkVOQU1FX05FV19OQU1FX1RJVExFX0NMQVNTID0gJ2pwLW5ldy1uYW1lLXRpdGxlJztcblxuLyoqXG4gKiBBIHN0cmlwcGVkLWRvd24gaW50ZXJmYWNlIGZvciBhIGZpbGUgY29udGFpbmVyLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElGaWxlQ29udGFpbmVyIGV4dGVuZHMgSlNPTk9iamVjdCB7XG4gIC8qKlxuICAgKiBUaGUgbGlzdCBvZiBpdGVtIG5hbWVzIGluIHRoZSBjdXJyZW50IHdvcmtpbmcgZGlyZWN0b3J5LlxuICAgKi9cbiAgaXRlbXM6IHN0cmluZ1tdO1xuICAvKipcbiAgICogVGhlIGN1cnJlbnQgd29ya2luZyBkaXJlY3Rvcnkgb2YgdGhlIGZpbGUgY29udGFpbmVyLlxuICAgKi9cbiAgcGF0aDogc3RyaW5nO1xufVxuXG4vKipcbiAqIFJlbmFtZSBhIGZpbGUgd2l0aCBhIGRpYWxvZy5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHJlbmFtZURpYWxvZyhcbiAgbWFuYWdlcjogSURvY3VtZW50TWFuYWdlcixcbiAgb2xkUGF0aDogc3RyaW5nLFxuICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3Jcbik6IFByb21pc2U8Q29udGVudHMuSU1vZGVsIHwgbnVsbD4ge1xuICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgdGl0bGU6IHRyYW5zLl9fKCdSZW5hbWUgRmlsZScpLFxuICAgIGJvZHk6IG5ldyBSZW5hbWVIYW5kbGVyKG9sZFBhdGgpLFxuICAgIGZvY3VzTm9kZVNlbGVjdG9yOiAnaW5wdXQnLFxuICAgIGJ1dHRvbnM6IFtcbiAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0NhbmNlbCcpIH0pLFxuICAgICAgRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdSZW5hbWUnKSB9KVxuICAgIF1cbiAgfSkudGhlbihyZXN1bHQgPT4ge1xuICAgIGlmICghcmVzdWx0LnZhbHVlKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgaWYgKCFpc1ZhbGlkRmlsZU5hbWUocmVzdWx0LnZhbHVlKSkge1xuICAgICAgdm9pZCBzaG93RXJyb3JNZXNzYWdlKFxuICAgICAgICB0cmFucy5fXygnUmVuYW1lIEVycm9yJyksXG4gICAgICAgIEVycm9yKFxuICAgICAgICAgIHRyYW5zLl9fKFxuICAgICAgICAgICAgJ1wiJTFcIiBpcyBub3QgYSB2YWxpZCBuYW1lIGZvciBhIGZpbGUuIE5hbWVzIG11c3QgaGF2ZSBub256ZXJvIGxlbmd0aCwgYW5kIGNhbm5vdCBpbmNsdWRlIFwiL1wiLCBcIlxcXFxcIiwgb3IgXCI6XCInLFxuICAgICAgICAgICAgcmVzdWx0LnZhbHVlXG4gICAgICAgICAgKVxuICAgICAgICApXG4gICAgICApO1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICAgIGNvbnN0IGJhc2VQYXRoID0gUGF0aEV4dC5kaXJuYW1lKG9sZFBhdGgpO1xuICAgIGNvbnN0IG5ld1BhdGggPSBQYXRoRXh0LmpvaW4oYmFzZVBhdGgsIHJlc3VsdC52YWx1ZSk7XG4gICAgcmV0dXJuIHJlbmFtZUZpbGUobWFuYWdlciwgb2xkUGF0aCwgbmV3UGF0aCk7XG4gIH0pO1xufVxuXG4vKipcbiAqIFJlbmFtZSBhIGZpbGUsIGFza2luZyBmb3IgY29uZmlybWF0aW9uIGlmIGl0IGlzIG92ZXJ3cml0aW5nIGFub3RoZXIuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiByZW5hbWVGaWxlKFxuICBtYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyLFxuICBvbGRQYXRoOiBzdHJpbmcsXG4gIG5ld1BhdGg6IHN0cmluZ1xuKTogUHJvbWlzZTxDb250ZW50cy5JTW9kZWwgfCBudWxsPiB7XG4gIHJldHVybiBtYW5hZ2VyLnJlbmFtZShvbGRQYXRoLCBuZXdQYXRoKS5jYXRjaChlcnJvciA9PiB7XG4gICAgaWYgKGVycm9yLm1lc3NhZ2UuaW5kZXhPZignNDA5JykgPT09IC0xKSB7XG4gICAgICB0aHJvdyBlcnJvcjtcbiAgICB9XG4gICAgcmV0dXJuIHNob3VsZE92ZXJ3cml0ZShuZXdQYXRoKS50aGVuKHZhbHVlID0+IHtcbiAgICAgIGlmICh2YWx1ZSkge1xuICAgICAgICByZXR1cm4gbWFuYWdlci5vdmVyd3JpdGUob2xkUGF0aCwgbmV3UGF0aCk7XG4gICAgICB9XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZWplY3QoJ0ZpbGUgbm90IHJlbmFtZWQnKTtcbiAgICB9KTtcbiAgfSk7XG59XG5cbi8qKlxuICogQXNrIHRoZSB1c2VyIHdoZXRoZXIgdG8gb3ZlcndyaXRlIGEgZmlsZS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHNob3VsZE92ZXJ3cml0ZShcbiAgcGF0aDogc3RyaW5nLFxuICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3Jcbik6IFByb21pc2U8Ym9vbGVhbj4ge1xuICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICBjb25zdCBvcHRpb25zID0ge1xuICAgIHRpdGxlOiB0cmFucy5fXygnT3ZlcndyaXRlIGZpbGU/JyksXG4gICAgYm9keTogdHJhbnMuX18oJ1wiJTFcIiBhbHJlYWR5IGV4aXN0cywgb3ZlcndyaXRlPycsIHBhdGgpLFxuICAgIGJ1dHRvbnM6IFtcbiAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0NhbmNlbCcpIH0pLFxuICAgICAgRGlhbG9nLndhcm5CdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ092ZXJ3cml0ZScpIH0pXG4gICAgXVxuICB9O1xuICByZXR1cm4gc2hvd0RpYWxvZyhvcHRpb25zKS50aGVuKHJlc3VsdCA9PiB7XG4gICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZShyZXN1bHQuYnV0dG9uLmFjY2VwdCk7XG4gIH0pO1xufVxuXG4vKipcbiAqIFRlc3Qgd2hldGhlciBhIG5hbWUgaXMgYSB2YWxpZCBmaWxlIG5hbWVcbiAqXG4gKiBEaXNhbGxvd3MgXCIvXCIsIFwiXFxcIiwgYW5kIFwiOlwiIGluIGZpbGUgbmFtZXMsIGFzIHdlbGwgYXMgbmFtZXMgd2l0aCB6ZXJvIGxlbmd0aC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGlzVmFsaWRGaWxlTmFtZShuYW1lOiBzdHJpbmcpOiBib29sZWFuIHtcbiAgY29uc3QgdmFsaWROYW1lRXhwID0gL1tcXC9cXFxcOl0vO1xuICByZXR1cm4gbmFtZS5sZW5ndGggPiAwICYmICF2YWxpZE5hbWVFeHAudGVzdChuYW1lKTtcbn1cblxuLyoqXG4gKiBBIHdpZGdldCB1c2VkIHRvIHJlbmFtZSBhIGZpbGUuXG4gKi9cbmNsYXNzIFJlbmFtZUhhbmRsZXIgZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IFwicmVuYW1lXCIgZGlhbG9nLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob2xkUGF0aDogc3RyaW5nKSB7XG4gICAgc3VwZXIoeyBub2RlOiBQcml2YXRlLmNyZWF0ZVJlbmFtZU5vZGUob2xkUGF0aCkgfSk7XG4gICAgdGhpcy5hZGRDbGFzcyhGSUxFX0RJQUxPR19DTEFTUyk7XG4gICAgY29uc3QgZXh0ID0gUGF0aEV4dC5leHRuYW1lKG9sZFBhdGgpO1xuICAgIGNvbnN0IHZhbHVlID0gKHRoaXMuaW5wdXROb2RlLnZhbHVlID0gUGF0aEV4dC5iYXNlbmFtZShvbGRQYXRoKSk7XG4gICAgdGhpcy5pbnB1dE5vZGUuc2V0U2VsZWN0aW9uUmFuZ2UoMCwgdmFsdWUubGVuZ3RoIC0gZXh0Lmxlbmd0aCk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBpbnB1dCB0ZXh0IG5vZGUuXG4gICAqL1xuICBnZXQgaW5wdXROb2RlKCk6IEhUTUxJbnB1dEVsZW1lbnQge1xuICAgIHJldHVybiB0aGlzLm5vZGUuZ2V0RWxlbWVudHNCeVRhZ05hbWUoJ2lucHV0JylbMF0gYXMgSFRNTElucHV0RWxlbWVudDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHZhbHVlIG9mIHRoZSB3aWRnZXQuXG4gICAqL1xuICBnZXRWYWx1ZSgpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLmlucHV0Tm9kZS52YWx1ZTtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIENyZWF0ZSB0aGUgbm9kZSBmb3IgYSByZW5hbWUgaGFuZGxlci5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBjcmVhdGVSZW5hbWVOb2RlKFxuICAgIG9sZFBhdGg6IHN0cmluZyxcbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3JcbiAgKTogSFRNTEVsZW1lbnQge1xuICAgIHRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgICBjb25zdCBib2R5ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgY29uc3QgZXhpc3RpbmdMYWJlbCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2xhYmVsJyk7XG4gICAgZXhpc3RpbmdMYWJlbC50ZXh0Q29udGVudCA9IHRyYW5zLl9fKCdGaWxlIFBhdGgnKTtcbiAgICBjb25zdCBleGlzdGluZ1BhdGggPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdzcGFuJyk7XG4gICAgZXhpc3RpbmdQYXRoLnRleHRDb250ZW50ID0gb2xkUGF0aDtcblxuICAgIGNvbnN0IG5hbWVUaXRsZSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2xhYmVsJyk7XG4gICAgbmFtZVRpdGxlLnRleHRDb250ZW50ID0gdHJhbnMuX18oJ05ldyBOYW1lJyk7XG4gICAgbmFtZVRpdGxlLmNsYXNzTmFtZSA9IFJFTkFNRV9ORVdfTkFNRV9USVRMRV9DTEFTUztcbiAgICBjb25zdCBuYW1lID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaW5wdXQnKTtcblxuICAgIGJvZHkuYXBwZW5kQ2hpbGQoZXhpc3RpbmdMYWJlbCk7XG4gICAgYm9keS5hcHBlbmRDaGlsZChleGlzdGluZ1BhdGgpO1xuICAgIGJvZHkuYXBwZW5kQ2hpbGQobmFtZVRpdGxlKTtcbiAgICBib2R5LmFwcGVuZENoaWxkKG5hbWUpO1xuICAgIHJldHVybiBib2R5O1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBkb2NtYW5hZ2VyXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9kaWFsb2dzJztcbmV4cG9ydCAqIGZyb20gJy4vbWFuYWdlcic7XG5leHBvcnQgKiBmcm9tICcuL3BhdGhzdGF0dXMnO1xuZXhwb3J0ICogZnJvbSAnLi9zYXZlaGFuZGxlcic7XG5leHBvcnQgKiBmcm9tICcuL3NhdmluZ3N0YXR1cyc7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG5leHBvcnQgKiBmcm9tICcuL3dpZGdldG1hbmFnZXInO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJU2Vzc2lvbkNvbnRleHQsIHNlc3Npb25Db250ZXh0RGlhbG9ncyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFBhdGhFeHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSURvY3VtZW50UHJvdmlkZXJGYWN0b3J5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcHJvdmlkZXInO1xuaW1wb3J0IHtcbiAgQ29udGV4dCxcbiAgRG9jdW1lbnRSZWdpc3RyeSxcbiAgSURvY3VtZW50V2lkZ2V0XG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IENvbnRlbnRzLCBLZXJuZWwsIFNlcnZpY2VNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgQXJyYXlFeHQsIGZpbmQgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBVVUlEIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgQXR0YWNoZWRQcm9wZXJ0eSB9IGZyb20gJ0BsdW1pbm8vcHJvcGVydGllcyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgU2F2ZUhhbmRsZXIgfSBmcm9tICcuL3NhdmVoYW5kbGVyJztcbmltcG9ydCB7IElEb2N1bWVudE1hbmFnZXIgfSBmcm9tICcuL3Rva2Vucyc7XG5pbXBvcnQgeyBEb2N1bWVudFdpZGdldE1hbmFnZXIgfSBmcm9tICcuL3dpZGdldG1hbmFnZXInO1xuXG4vKipcbiAqIFRoZSBkb2N1bWVudCBtYW5hZ2VyLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIFRoZSBkb2N1bWVudCBtYW5hZ2VyIGlzIHVzZWQgdG8gcmVnaXN0ZXIgbW9kZWwgYW5kIHdpZGdldCBjcmVhdG9ycyxcbiAqIGFuZCB0aGUgZmlsZSBicm93c2VyIHVzZXMgdGhlIGRvY3VtZW50IG1hbmFnZXIgdG8gY3JlYXRlIHdpZGdldHMuIFRoZVxuICogZG9jdW1lbnQgbWFuYWdlciBtYWludGFpbnMgYSBjb250ZXh0IGZvciBlYWNoIHBhdGggYW5kIG1vZGVsIHR5cGUgdGhhdCBpc1xuICogb3BlbiwgYW5kIGEgbGlzdCBvZiB3aWRnZXRzIGZvciBlYWNoIGNvbnRleHQuIFRoZSBkb2N1bWVudCBtYW5hZ2VyIGlzIGluXG4gKiBjb250cm9sIG9mIHRoZSBwcm9wZXIgY2xvc2luZyBhbmQgZGlzcG9zYWwgb2YgdGhlIHdpZGdldHMgYW5kIGNvbnRleHRzLlxuICovXG5leHBvcnQgY2xhc3MgRG9jdW1lbnRNYW5hZ2VyIGltcGxlbWVudHMgSURvY3VtZW50TWFuYWdlciB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgZG9jdW1lbnQgbWFuYWdlci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IERvY3VtZW50TWFuYWdlci5JT3B0aW9ucykge1xuICAgIHRoaXMudHJhbnNsYXRvciA9IG9wdGlvbnMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLnJlZ2lzdHJ5ID0gb3B0aW9ucy5yZWdpc3RyeTtcbiAgICB0aGlzLnNlcnZpY2VzID0gb3B0aW9ucy5tYW5hZ2VyO1xuICAgIHRoaXMuX2NvbGxhYm9yYXRpdmUgPSAhIW9wdGlvbnMuY29sbGFib3JhdGl2ZTtcbiAgICB0aGlzLl9kaWFsb2dzID0gb3B0aW9ucy5zZXNzaW9uRGlhbG9ncyB8fCBzZXNzaW9uQ29udGV4dERpYWxvZ3M7XG4gICAgdGhpcy5fZG9jUHJvdmlkZXJGYWN0b3J5ID0gb3B0aW9ucy5kb2NQcm92aWRlckZhY3Rvcnk7XG5cbiAgICB0aGlzLl9vcGVuZXIgPSBvcHRpb25zLm9wZW5lcjtcbiAgICB0aGlzLl93aGVuID0gb3B0aW9ucy53aGVuIHx8IG9wdGlvbnMubWFuYWdlci5yZWFkeTtcblxuICAgIGNvbnN0IHdpZGdldE1hbmFnZXIgPSBuZXcgRG9jdW1lbnRXaWRnZXRNYW5hZ2VyKHtcbiAgICAgIHJlZ2lzdHJ5OiB0aGlzLnJlZ2lzdHJ5LFxuICAgICAgdHJhbnNsYXRvcjogdGhpcy50cmFuc2xhdG9yXG4gICAgfSk7XG4gICAgd2lkZ2V0TWFuYWdlci5hY3RpdmF0ZVJlcXVlc3RlZC5jb25uZWN0KHRoaXMuX29uQWN0aXZhdGVSZXF1ZXN0ZWQsIHRoaXMpO1xuICAgIHRoaXMuX3dpZGdldE1hbmFnZXIgPSB3aWRnZXRNYW5hZ2VyO1xuICAgIHRoaXMuX3NldEJ1c3kgPSBvcHRpb25zLnNldEJ1c3k7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHJlZ2lzdHJ5IHVzZWQgYnkgdGhlIG1hbmFnZXIuXG4gICAqL1xuICByZWFkb25seSByZWdpc3RyeTogRG9jdW1lbnRSZWdpc3RyeTtcblxuICAvKipcbiAgICogVGhlIHNlcnZpY2UgbWFuYWdlciB1c2VkIGJ5IHRoZSBtYW5hZ2VyLlxuICAgKi9cbiAgcmVhZG9ubHkgc2VydmljZXM6IFNlcnZpY2VNYW5hZ2VyLklNYW5hZ2VyO1xuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gb25lIG9mIHRoZSBkb2N1bWVudHMgaXMgYWN0aXZhdGVkLlxuICAgKi9cbiAgZ2V0IGFjdGl2YXRlUmVxdWVzdGVkKCk6IElTaWduYWw8dGhpcywgc3RyaW5nPiB7XG4gICAgcmV0dXJuIHRoaXMuX2FjdGl2YXRlUmVxdWVzdGVkO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdG8gYXV0b3NhdmUgZG9jdW1lbnRzLlxuICAgKi9cbiAgZ2V0IGF1dG9zYXZlKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9hdXRvc2F2ZTtcbiAgfVxuXG4gIHNldCBhdXRvc2F2ZSh2YWx1ZTogYm9vbGVhbikge1xuICAgIHRoaXMuX2F1dG9zYXZlID0gdmFsdWU7XG5cbiAgICAvLyBGb3IgZWFjaCBleGlzdGluZyBjb250ZXh0LCBzdGFydC9zdG9wIHRoZSBhdXRvc2F2ZSBoYW5kbGVyIGFzIG5lZWRlZC5cbiAgICB0aGlzLl9jb250ZXh0cy5mb3JFYWNoKGNvbnRleHQgPT4ge1xuICAgICAgY29uc3QgaGFuZGxlciA9IFByaXZhdGUuc2F2ZUhhbmRsZXJQcm9wZXJ0eS5nZXQoY29udGV4dCk7XG4gICAgICBpZiAoIWhhbmRsZXIpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgaWYgKHZhbHVlID09PSB0cnVlICYmICFoYW5kbGVyLmlzQWN0aXZlKSB7XG4gICAgICAgIGhhbmRsZXIuc3RhcnQoKTtcbiAgICAgIH0gZWxzZSBpZiAodmFsdWUgPT09IGZhbHNlICYmIGhhbmRsZXIuaXNBY3RpdmUpIHtcbiAgICAgICAgaGFuZGxlci5zdG9wKCk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogRGV0ZXJtaW5lcyB0aGUgdGltZSBpbnRlcnZhbCBmb3IgYXV0b3NhdmUgaW4gc2Vjb25kcy5cbiAgICovXG4gIGdldCBhdXRvc2F2ZUludGVydmFsKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX2F1dG9zYXZlSW50ZXJ2YWw7XG4gIH1cblxuICBzZXQgYXV0b3NhdmVJbnRlcnZhbCh2YWx1ZTogbnVtYmVyKSB7XG4gICAgdGhpcy5fYXV0b3NhdmVJbnRlcnZhbCA9IHZhbHVlO1xuXG4gICAgLy8gRm9yIGVhY2ggZXhpc3RpbmcgY29udGV4dCwgc2V0IHRoZSBzYXZlIGludGVydmFsIGFzIG5lZWRlZC5cbiAgICB0aGlzLl9jb250ZXh0cy5mb3JFYWNoKGNvbnRleHQgPT4ge1xuICAgICAgY29uc3QgaGFuZGxlciA9IFByaXZhdGUuc2F2ZUhhbmRsZXJQcm9wZXJ0eS5nZXQoY29udGV4dCk7XG4gICAgICBpZiAoIWhhbmRsZXIpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgaGFuZGxlci5zYXZlSW50ZXJ2YWwgPSB2YWx1ZSB8fCAxMjA7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogRGVmaW5lcyBtYXggYWNjZXB0YWJsZSBkaWZmZXJlbmNlLCBpbiBtaWxsaXNlY29uZHMsIGJldHdlZW4gbGFzdCBtb2RpZmllZCB0aW1lc3RhbXBzIG9uIGRpc2sgYW5kIGNsaWVudFxuICAgKi9cbiAgZ2V0IGxhc3RNb2RpZmllZENoZWNrTWFyZ2luKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX2xhc3RNb2RpZmllZENoZWNrTWFyZ2luO1xuICB9XG5cbiAgc2V0IGxhc3RNb2RpZmllZENoZWNrTWFyZ2luKHZhbHVlOiBudW1iZXIpIHtcbiAgICB0aGlzLl9sYXN0TW9kaWZpZWRDaGVja01hcmdpbiA9IHZhbHVlO1xuXG4gICAgLy8gRm9yIGVhY2ggZXhpc3RpbmcgY29udGV4dCwgdXBkYXRlIHRoZSBtYXJnaW4gdmFsdWUuXG4gICAgdGhpcy5fY29udGV4dHMuZm9yRWFjaChjb250ZXh0ID0+IHtcbiAgICAgIGNvbnRleHQubGFzdE1vZGlmaWVkQ2hlY2tNYXJnaW4gPSB2YWx1ZTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgd2hldGhlciB0aGUgZG9jdW1lbnQgbWFuYWdlciBoYXMgYmVlbiBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBkb2N1bWVudCBtYW5hZ2VyLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuXG4gICAgLy8gQ2xlYXIgYW55IGxpc3RlbmVycyBmb3Igb3VyIHNpZ25hbHMuXG4gICAgU2lnbmFsLmNsZWFyRGF0YSh0aGlzKTtcblxuICAgIC8vIENsb3NlIGFsbCB0aGUgd2lkZ2V0cyBmb3Igb3VyIGNvbnRleHRzIGFuZCBkaXNwb3NlIHRoZSB3aWRnZXQgbWFuYWdlci5cbiAgICB0aGlzLl9jb250ZXh0cy5mb3JFYWNoKGNvbnRleHQgPT4ge1xuICAgICAgcmV0dXJuIHRoaXMuX3dpZGdldE1hbmFnZXIuY2xvc2VXaWRnZXRzKGNvbnRleHQpO1xuICAgIH0pO1xuICAgIHRoaXMuX3dpZGdldE1hbmFnZXIuZGlzcG9zZSgpO1xuXG4gICAgLy8gQ2xlYXIgdGhlIGNvbnRleHQgbGlzdC5cbiAgICB0aGlzLl9jb250ZXh0cy5sZW5ndGggPSAwO1xuICB9XG5cbiAgLyoqXG4gICAqIENsb25lIGEgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gVGhlIHNvdXJjZSB3aWRnZXQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgbmV3IHdpZGdldCBvciBgdW5kZWZpbmVkYC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiAgVXNlcyB0aGUgc2FtZSB3aWRnZXQgZmFjdG9yeSBhbmQgY29udGV4dCBhcyB0aGUgc291cmNlLCBvciByZXR1cm5zXG4gICAqICBgdW5kZWZpbmVkYCBpZiB0aGUgc291cmNlIHdpZGdldCBpcyBub3QgbWFuYWdlZCBieSB0aGlzIG1hbmFnZXIuXG4gICAqL1xuICBjbG9uZVdpZGdldCh3aWRnZXQ6IFdpZGdldCk6IElEb2N1bWVudFdpZGdldCB8IHVuZGVmaW5lZCB7XG4gICAgcmV0dXJuIHRoaXMuX3dpZGdldE1hbmFnZXIuY2xvbmVXaWRnZXQod2lkZ2V0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbG9zZSBhbGwgb2YgdGhlIG9wZW4gZG9jdW1lbnRzLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgcmVzb2x2aW5nIHdoZW4gdGhlIHdpZGdldHMgYXJlIGNsb3NlZC5cbiAgICovXG4gIGNsb3NlQWxsKCk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiBQcm9taXNlLmFsbChcbiAgICAgIHRoaXMuX2NvbnRleHRzLm1hcChjb250ZXh0ID0+IHRoaXMuX3dpZGdldE1hbmFnZXIuY2xvc2VXaWRnZXRzKGNvbnRleHQpKVxuICAgICkudGhlbigoKSA9PiB1bmRlZmluZWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIENsb3NlIHRoZSB3aWRnZXRzIGFzc29jaWF0ZWQgd2l0aCBhIGdpdmVuIHBhdGguXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoIC0gVGhlIHRhcmdldCBwYXRoLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgcmVzb2x2aW5nIHdoZW4gdGhlIHdpZGdldHMgYXJlIGNsb3NlZC5cbiAgICovXG4gIGNsb3NlRmlsZShwYXRoOiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCBjbG9zZSA9IHRoaXMuX2NvbnRleHRzRm9yUGF0aChwYXRoKS5tYXAoYyA9PlxuICAgICAgdGhpcy5fd2lkZ2V0TWFuYWdlci5jbG9zZVdpZGdldHMoYylcbiAgICApO1xuICAgIHJldHVybiBQcm9taXNlLmFsbChjbG9zZSkudGhlbih4ID0+IHVuZGVmaW5lZCk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBkb2N1bWVudCBjb250ZXh0IGZvciBhIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldCAtIFRoZSB3aWRnZXQgb2YgaW50ZXJlc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBjb250ZXh0IGFzc29jaWF0ZWQgd2l0aCB0aGUgd2lkZ2V0LCBvciBgdW5kZWZpbmVkYCBpZiBubyBzdWNoXG4gICAqIGNvbnRleHQgZXhpc3RzLlxuICAgKi9cbiAgY29udGV4dEZvcldpZGdldCh3aWRnZXQ6IFdpZGdldCk6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dCB8IHVuZGVmaW5lZCB7XG4gICAgcmV0dXJuIHRoaXMuX3dpZGdldE1hbmFnZXIuY29udGV4dEZvcldpZGdldCh3aWRnZXQpO1xuICB9XG5cbiAgLyoqXG4gICAqIENvcHkgYSBmaWxlLlxuICAgKlxuICAgKiBAcGFyYW0gZnJvbUZpbGUgLSBUaGUgZnVsbCBwYXRoIG9mIHRoZSBvcmlnaW5hbCBmaWxlLlxuICAgKlxuICAgKiBAcGFyYW0gdG9EaXIgLSBUaGUgZnVsbCBwYXRoIHRvIHRoZSB0YXJnZXQgZGlyZWN0b3J5LlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2Ugd2hpY2ggcmVzb2x2ZXMgdG8gdGhlIGNvbnRlbnRzIG9mIHRoZSBmaWxlLlxuICAgKi9cbiAgY29weShmcm9tRmlsZTogc3RyaW5nLCB0b0Rpcjogc3RyaW5nKTogUHJvbWlzZTxDb250ZW50cy5JTW9kZWw+IHtcbiAgICByZXR1cm4gdGhpcy5zZXJ2aWNlcy5jb250ZW50cy5jb3B5KGZyb21GaWxlLCB0b0Rpcik7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IGZpbGUgYW5kIHJldHVybiB0aGUgd2lkZ2V0IHVzZWQgdG8gdmlldyBpdC5cbiAgICpcbiAgICogQHBhcmFtIHBhdGggLSBUaGUgZmlsZSBwYXRoIHRvIGNyZWF0ZS5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldE5hbWUgLSBUaGUgbmFtZSBvZiB0aGUgd2lkZ2V0IGZhY3RvcnkgdG8gdXNlLiAnZGVmYXVsdCcgd2lsbCB1c2UgdGhlIGRlZmF1bHQgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0ga2VybmVsIC0gQW4gb3B0aW9uYWwga2VybmVsIG5hbWUvaWQgdG8gb3ZlcnJpZGUgdGhlIGRlZmF1bHQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBjcmVhdGVkIHdpZGdldCwgb3IgYHVuZGVmaW5lZGAuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBmdW5jdGlvbiB3aWxsIHJldHVybiBgdW5kZWZpbmVkYCBpZiBhIHZhbGlkIHdpZGdldCBmYWN0b3J5XG4gICAqIGNhbm5vdCBiZSBmb3VuZC5cbiAgICovXG4gIGNyZWF0ZU5ldyhcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgd2lkZ2V0TmFtZSA9ICdkZWZhdWx0JyxcbiAgICBrZXJuZWw/OiBQYXJ0aWFsPEtlcm5lbC5JTW9kZWw+XG4gICk6IFdpZGdldCB8IHVuZGVmaW5lZCB7XG4gICAgcmV0dXJuIHRoaXMuX2NyZWF0ZU9yT3BlbkRvY3VtZW50KCdjcmVhdGUnLCBwYXRoLCB3aWRnZXROYW1lLCBrZXJuZWwpO1xuICB9XG5cbiAgLyoqXG4gICAqIERlbGV0ZSBhIGZpbGUuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoIC0gVGhlIGZ1bGwgcGF0aCB0byB0aGUgZmlsZSB0byBiZSBkZWxldGVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2Ugd2hpY2ggcmVzb2x2ZXMgd2hlbiB0aGUgZmlsZSBpcyBkZWxldGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIElmIHRoZXJlIGlzIGEgcnVubmluZyBzZXNzaW9uIGFzc29jaWF0ZWQgd2l0aCB0aGUgZmlsZSBhbmQgbm8gb3RoZXJcbiAgICogc2Vzc2lvbnMgYXJlIHVzaW5nIHRoZSBrZXJuZWwsIHRoZSBzZXNzaW9uIHdpbGwgYmUgc2h1dCBkb3duLlxuICAgKi9cbiAgZGVsZXRlRmlsZShwYXRoOiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5zZXJ2aWNlcy5zZXNzaW9uc1xuICAgICAgLnN0b3BJZk5lZWRlZChwYXRoKVxuICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICByZXR1cm4gdGhpcy5zZXJ2aWNlcy5jb250ZW50cy5kZWxldGUocGF0aCk7XG4gICAgICB9KVxuICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICB0aGlzLl9jb250ZXh0c0ZvclBhdGgocGF0aCkuZm9yRWFjaChjb250ZXh0ID0+XG4gICAgICAgICAgdGhpcy5fd2lkZ2V0TWFuYWdlci5kZWxldGVXaWRnZXRzKGNvbnRleHQpXG4gICAgICAgICk7XG4gICAgICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUodm9pZCAwKTtcbiAgICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFNlZSBpZiBhIHdpZGdldCBhbHJlYWR5IGV4aXN0cyBmb3IgdGhlIGdpdmVuIHBhdGggYW5kIHdpZGdldCBuYW1lLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aCAtIFRoZSBmaWxlIHBhdGggdG8gdXNlLlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0TmFtZSAtIFRoZSBuYW1lIG9mIHRoZSB3aWRnZXQgZmFjdG9yeSB0byB1c2UuICdkZWZhdWx0JyB3aWxsIHVzZSB0aGUgZGVmYXVsdCB3aWRnZXQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBmb3VuZCB3aWRnZXQsIG9yIGB1bmRlZmluZWRgLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgY2FuIGJlIHVzZWQgdG8gZmluZCBhbiBleGlzdGluZyB3aWRnZXQgaW5zdGVhZCBvZiBvcGVuaW5nXG4gICAqIGEgbmV3IHdpZGdldC5cbiAgICovXG4gIGZpbmRXaWRnZXQoXG4gICAgcGF0aDogc3RyaW5nLFxuICAgIHdpZGdldE5hbWU6IHN0cmluZyB8IG51bGwgPSAnZGVmYXVsdCdcbiAgKTogSURvY3VtZW50V2lkZ2V0IHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCBuZXdQYXRoID0gUGF0aEV4dC5ub3JtYWxpemUocGF0aCk7XG4gICAgbGV0IHdpZGdldE5hbWVzID0gW3dpZGdldE5hbWVdO1xuICAgIGlmICh3aWRnZXROYW1lID09PSAnZGVmYXVsdCcpIHtcbiAgICAgIGNvbnN0IGZhY3RvcnkgPSB0aGlzLnJlZ2lzdHJ5LmRlZmF1bHRXaWRnZXRGYWN0b3J5KG5ld1BhdGgpO1xuICAgICAgaWYgKCFmYWN0b3J5KSB7XG4gICAgICAgIHJldHVybiB1bmRlZmluZWQ7XG4gICAgICB9XG4gICAgICB3aWRnZXROYW1lcyA9IFtmYWN0b3J5Lm5hbWVdO1xuICAgIH0gZWxzZSBpZiAod2lkZ2V0TmFtZSA9PT0gbnVsbCkge1xuICAgICAgd2lkZ2V0TmFtZXMgPSB0aGlzLnJlZ2lzdHJ5XG4gICAgICAgIC5wcmVmZXJyZWRXaWRnZXRGYWN0b3JpZXMobmV3UGF0aClcbiAgICAgICAgLm1hcChmID0+IGYubmFtZSk7XG4gICAgfVxuXG4gICAgZm9yIChjb25zdCBjb250ZXh0IG9mIHRoaXMuX2NvbnRleHRzRm9yUGF0aChuZXdQYXRoKSkge1xuICAgICAgZm9yIChjb25zdCB3aWRnZXROYW1lIG9mIHdpZGdldE5hbWVzKSB7XG4gICAgICAgIGlmICh3aWRnZXROYW1lICE9PSBudWxsKSB7XG4gICAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdGhpcy5fd2lkZ2V0TWFuYWdlci5maW5kV2lkZ2V0KGNvbnRleHQsIHdpZGdldE5hbWUpO1xuICAgICAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgICAgIHJldHVybiB3aWRnZXQ7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiB1bmRlZmluZWQ7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHVudGl0bGVkIGZpbGUuXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIGZpbGUgY29udGVudCBjcmVhdGlvbiBvcHRpb25zLlxuICAgKi9cbiAgbmV3VW50aXRsZWQob3B0aW9uczogQ29udGVudHMuSUNyZWF0ZU9wdGlvbnMpOiBQcm9taXNlPENvbnRlbnRzLklNb2RlbD4ge1xuICAgIGlmIChvcHRpb25zLnR5cGUgPT09ICdmaWxlJykge1xuICAgICAgb3B0aW9ucy5leHQgPSBvcHRpb25zLmV4dCB8fCAnLnR4dCc7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLnNlcnZpY2VzLmNvbnRlbnRzLm5ld1VudGl0bGVkKG9wdGlvbnMpO1xuICB9XG5cbiAgLyoqXG4gICAqIE9wZW4gYSBmaWxlIGFuZCByZXR1cm4gdGhlIHdpZGdldCB1c2VkIHRvIHZpZXcgaXQuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoIC0gVGhlIGZpbGUgcGF0aCB0byBvcGVuLlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0TmFtZSAtIFRoZSBuYW1lIG9mIHRoZSB3aWRnZXQgZmFjdG9yeSB0byB1c2UuICdkZWZhdWx0JyB3aWxsIHVzZSB0aGUgZGVmYXVsdCB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSBrZXJuZWwgLSBBbiBvcHRpb25hbCBrZXJuZWwgbmFtZS9pZCB0byBvdmVycmlkZSB0aGUgZGVmYXVsdC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIGNyZWF0ZWQgd2lkZ2V0LCBvciBgdW5kZWZpbmVkYC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGZ1bmN0aW9uIHdpbGwgcmV0dXJuIGB1bmRlZmluZWRgIGlmIGEgdmFsaWQgd2lkZ2V0IGZhY3RvcnlcbiAgICogY2Fubm90IGJlIGZvdW5kLlxuICAgKi9cbiAgb3BlbihcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgd2lkZ2V0TmFtZSA9ICdkZWZhdWx0JyxcbiAgICBrZXJuZWw/OiBQYXJ0aWFsPEtlcm5lbC5JTW9kZWw+LFxuICAgIG9wdGlvbnM/OiBEb2N1bWVudFJlZ2lzdHJ5LklPcGVuT3B0aW9uc1xuICApOiBJRG9jdW1lbnRXaWRnZXQgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiB0aGlzLl9jcmVhdGVPck9wZW5Eb2N1bWVudChcbiAgICAgICdvcGVuJyxcbiAgICAgIHBhdGgsXG4gICAgICB3aWRnZXROYW1lLFxuICAgICAga2VybmVsLFxuICAgICAgb3B0aW9uc1xuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogT3BlbiBhIGZpbGUgYW5kIHJldHVybiB0aGUgd2lkZ2V0IHVzZWQgdG8gdmlldyBpdC5cbiAgICogUmV2ZWFscyBhbiBhbHJlYWR5IGV4aXN0aW5nIGVkaXRvci5cbiAgICpcbiAgICogQHBhcmFtIHBhdGggLSBUaGUgZmlsZSBwYXRoIHRvIG9wZW4uXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXROYW1lIC0gVGhlIG5hbWUgb2YgdGhlIHdpZGdldCBmYWN0b3J5IHRvIHVzZS4gJ2RlZmF1bHQnIHdpbGwgdXNlIHRoZSBkZWZhdWx0IHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIGtlcm5lbCAtIEFuIG9wdGlvbmFsIGtlcm5lbCBuYW1lL2lkIHRvIG92ZXJyaWRlIHRoZSBkZWZhdWx0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgY3JlYXRlZCB3aWRnZXQsIG9yIGB1bmRlZmluZWRgLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgZnVuY3Rpb24gd2lsbCByZXR1cm4gYHVuZGVmaW5lZGAgaWYgYSB2YWxpZCB3aWRnZXQgZmFjdG9yeVxuICAgKiBjYW5ub3QgYmUgZm91bmQuXG4gICAqL1xuICBvcGVuT3JSZXZlYWwoXG4gICAgcGF0aDogc3RyaW5nLFxuICAgIHdpZGdldE5hbWUgPSAnZGVmYXVsdCcsXG4gICAga2VybmVsPzogUGFydGlhbDxLZXJuZWwuSU1vZGVsPixcbiAgICBvcHRpb25zPzogRG9jdW1lbnRSZWdpc3RyeS5JT3Blbk9wdGlvbnNcbiAgKTogSURvY3VtZW50V2lkZ2V0IHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCB3aWRnZXQgPSB0aGlzLmZpbmRXaWRnZXQocGF0aCwgd2lkZ2V0TmFtZSk7XG4gICAgaWYgKHdpZGdldCkge1xuICAgICAgdGhpcy5fb3BlbmVyLm9wZW4od2lkZ2V0LCBvcHRpb25zIHx8IHt9KTtcbiAgICAgIHJldHVybiB3aWRnZXQ7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLm9wZW4ocGF0aCwgd2lkZ2V0TmFtZSwga2VybmVsLCBvcHRpb25zIHx8IHt9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBPdmVyd3JpdGUgYSBmaWxlLlxuICAgKlxuICAgKiBAcGFyYW0gb2xkUGF0aCAtIFRoZSBmdWxsIHBhdGggdG8gdGhlIG9yaWdpbmFsIGZpbGUuXG4gICAqXG4gICAqIEBwYXJhbSBuZXdQYXRoIC0gVGhlIGZ1bGwgcGF0aCB0byB0aGUgbmV3IGZpbGUuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSBjb250YWluaW5nIHRoZSBuZXcgZmlsZSBjb250ZW50cyBtb2RlbC5cbiAgICovXG4gIG92ZXJ3cml0ZShvbGRQYXRoOiBzdHJpbmcsIG5ld1BhdGg6IHN0cmluZyk6IFByb21pc2U8Q29udGVudHMuSU1vZGVsPiB7XG4gICAgLy8gQ2xlYW5seSBvdmVyd3JpdGUgdGhlIGZpbGUgYnkgbW92aW5nIGl0LCBtYWtpbmcgc3VyZSB0aGUgb3JpZ2luYWwgZG9lc1xuICAgIC8vIG5vdCBleGlzdCwgYW5kIHRoZW4gcmVuYW1pbmcgdG8gdGhlIG5ldyBwYXRoLlxuICAgIGNvbnN0IHRlbXBQYXRoID0gYCR7bmV3UGF0aH0uJHtVVUlELnV1aWQ0KCl9YDtcbiAgICBjb25zdCBjYiA9ICgpID0+IHRoaXMucmVuYW1lKHRlbXBQYXRoLCBuZXdQYXRoKTtcbiAgICByZXR1cm4gdGhpcy5yZW5hbWUob2xkUGF0aCwgdGVtcFBhdGgpXG4gICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgIHJldHVybiB0aGlzLmRlbGV0ZUZpbGUobmV3UGF0aCk7XG4gICAgICB9KVxuICAgICAgLnRoZW4oY2IsIGNiKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5hbWUgYSBmaWxlIG9yIGRpcmVjdG9yeS5cbiAgICpcbiAgICogQHBhcmFtIG9sZFBhdGggLSBUaGUgZnVsbCBwYXRoIHRvIHRoZSBvcmlnaW5hbCBmaWxlLlxuICAgKlxuICAgKiBAcGFyYW0gbmV3UGF0aCAtIFRoZSBmdWxsIHBhdGggdG8gdGhlIG5ldyBmaWxlLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgY29udGFpbmluZyB0aGUgbmV3IGZpbGUgY29udGVudHMgbW9kZWwuICBUaGUgcHJvbWlzZVxuICAgKiB3aWxsIHJlamVjdCBpZiB0aGUgbmV3UGF0aCBhbHJlYWR5IGV4aXN0cy4gIFVzZSBbW292ZXJ3cml0ZV1dIHRvIG92ZXJ3cml0ZVxuICAgKiBhIGZpbGUuXG4gICAqL1xuICByZW5hbWUob2xkUGF0aDogc3RyaW5nLCBuZXdQYXRoOiBzdHJpbmcpOiBQcm9taXNlPENvbnRlbnRzLklNb2RlbD4ge1xuICAgIHJldHVybiB0aGlzLnNlcnZpY2VzLmNvbnRlbnRzLnJlbmFtZShvbGRQYXRoLCBuZXdQYXRoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBGaW5kIGEgY29udGV4dCBmb3IgYSBnaXZlbiBwYXRoIGFuZCBmYWN0b3J5IG5hbWUuXG4gICAqL1xuICBwcml2YXRlIF9maW5kQ29udGV4dChcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgZmFjdG9yeU5hbWU6IHN0cmluZ1xuICApOiBQcml2YXRlLklDb250ZXh0IHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCBub3JtYWxpemVkUGF0aCA9IHRoaXMuc2VydmljZXMuY29udGVudHMubm9ybWFsaXplKHBhdGgpO1xuICAgIHJldHVybiBmaW5kKHRoaXMuX2NvbnRleHRzLCBjb250ZXh0ID0+IHtcbiAgICAgIHJldHVybiAoXG4gICAgICAgIGNvbnRleHQucGF0aCA9PT0gbm9ybWFsaXplZFBhdGggJiYgY29udGV4dC5mYWN0b3J5TmFtZSA9PT0gZmFjdG9yeU5hbWVcbiAgICAgICk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBjb250ZXh0cyBmb3IgYSBnaXZlbiBwYXRoLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZXJlIG1heSBiZSBtb3JlIHRoYW4gb25lIGNvbnRleHQgZm9yIGEgZ2l2ZW4gcGF0aCBpZiB0aGUgcGF0aCBpcyBvcGVuXG4gICAqIHdpdGggbXVsdGlwbGUgbW9kZWwgZmFjdG9yaWVzIChmb3IgZXhhbXBsZSwgYSBub3RlYm9vayBjYW4gYmUgb3BlbiB3aXRoIGFcbiAgICogbm90ZWJvb2sgbW9kZWwgZmFjdG9yeSBhbmQgYSB0ZXh0IG1vZGVsIGZhY3RvcnkpLlxuICAgKi9cbiAgcHJpdmF0ZSBfY29udGV4dHNGb3JQYXRoKHBhdGg6IHN0cmluZyk6IFByaXZhdGUuSUNvbnRleHRbXSB7XG4gICAgY29uc3Qgbm9ybWFsaXplZFBhdGggPSB0aGlzLnNlcnZpY2VzLmNvbnRlbnRzLm5vcm1hbGl6ZShwYXRoKTtcbiAgICByZXR1cm4gdGhpcy5fY29udGV4dHMuZmlsdGVyKGNvbnRleHQgPT4gY29udGV4dC5wYXRoID09PSBub3JtYWxpemVkUGF0aCk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgY29udGV4dCBmcm9tIGEgcGF0aCBhbmQgYSBtb2RlbCBmYWN0b3J5LlxuICAgKi9cbiAgcHJpdmF0ZSBfY3JlYXRlQ29udGV4dChcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgZmFjdG9yeTogRG9jdW1lbnRSZWdpc3RyeS5Nb2RlbEZhY3RvcnksXG4gICAga2VybmVsUHJlZmVyZW5jZT86IElTZXNzaW9uQ29udGV4dC5JS2VybmVsUHJlZmVyZW5jZVxuICApOiBQcml2YXRlLklDb250ZXh0IHtcbiAgICAvLyBUT0RPOiBNYWtlIGl0IGltcG9zc2libGUgdG8gb3BlbiB0d28gZGlmZmVyZW50IGNvbnRleHRzIGZvciB0aGUgc2FtZVxuICAgIC8vIHBhdGguIE9yIGF0IGxlYXN0IHByb21wdCB0aGUgY2xvc2luZyBvZiBhbGwgd2lkZ2V0cyBhc3NvY2lhdGVkIHdpdGggdGhlXG4gICAgLy8gb2xkIGNvbnRleHQgYmVmb3JlIG9wZW5pbmcgdGhlIG5ldyBjb250ZXh0LiBUaGlzIHdpbGwgbWFrZSB0aGluZ3MgbXVjaFxuICAgIC8vIG1vcmUgY29uc2lzdGVudCBmb3IgdGhlIHVzZXJzLCBhdCB0aGUgY29zdCBvZiBzb21lIGNvbmZ1c2lvbiBhYm91dCB3aGF0XG4gICAgLy8gbW9kZWxzIGFyZSBhbmQgd2h5IHNvbWV0aW1lcyB0aGV5IGNhbm5vdCBvcGVuIHRoZSBzYW1lIGZpbGUgaW4gZGlmZmVyZW50XG4gICAgLy8gd2lkZ2V0cyB0aGF0IGhhdmUgZGlmZmVyZW50IG1vZGVscy5cblxuICAgIC8vIEFsbG93IG9wdGlvbnMgdG8gYmUgcGFzc2VkIHdoZW4gYWRkaW5nIGEgc2libGluZy5cbiAgICBjb25zdCBhZG9wdGVyID0gKFxuICAgICAgd2lkZ2V0OiBJRG9jdW1lbnRXaWRnZXQsXG4gICAgICBvcHRpb25zPzogRG9jdW1lbnRSZWdpc3RyeS5JT3Blbk9wdGlvbnNcbiAgICApID0+IHtcbiAgICAgIHRoaXMuX3dpZGdldE1hbmFnZXIuYWRvcHRXaWRnZXQoY29udGV4dCwgd2lkZ2V0KTtcbiAgICAgIHRoaXMuX29wZW5lci5vcGVuKHdpZGdldCwgb3B0aW9ucyk7XG4gICAgfTtcbiAgICBjb25zdCBtb2RlbERCRmFjdG9yeSA9XG4gICAgICB0aGlzLnNlcnZpY2VzLmNvbnRlbnRzLmdldE1vZGVsREJGYWN0b3J5KHBhdGgpIHx8IHVuZGVmaW5lZDtcbiAgICBjb25zdCBjb250ZXh0ID0gbmV3IENvbnRleHQoe1xuICAgICAgb3BlbmVyOiBhZG9wdGVyLFxuICAgICAgbWFuYWdlcjogdGhpcy5zZXJ2aWNlcyxcbiAgICAgIGZhY3RvcnksXG4gICAgICBwYXRoLFxuICAgICAga2VybmVsUHJlZmVyZW5jZSxcbiAgICAgIG1vZGVsREJGYWN0b3J5LFxuICAgICAgc2V0QnVzeTogdGhpcy5fc2V0QnVzeSxcbiAgICAgIHNlc3Npb25EaWFsb2dzOiB0aGlzLl9kaWFsb2dzLFxuICAgICAgY29sbGFib3JhdGl2ZTogdGhpcy5fY29sbGFib3JhdGl2ZSxcbiAgICAgIGRvY1Byb3ZpZGVyRmFjdG9yeTogdGhpcy5fZG9jUHJvdmlkZXJGYWN0b3J5LFxuICAgICAgbGFzdE1vZGlmaWVkQ2hlY2tNYXJnaW46IHRoaXMuX2xhc3RNb2RpZmllZENoZWNrTWFyZ2luXG4gICAgfSk7XG4gICAgY29uc3QgaGFuZGxlciA9IG5ldyBTYXZlSGFuZGxlcih7XG4gICAgICBjb250ZXh0LFxuICAgICAgc2F2ZUludGVydmFsOiB0aGlzLmF1dG9zYXZlSW50ZXJ2YWxcbiAgICB9KTtcbiAgICBQcml2YXRlLnNhdmVIYW5kbGVyUHJvcGVydHkuc2V0KGNvbnRleHQsIGhhbmRsZXIpO1xuICAgIHZvaWQgY29udGV4dC5yZWFkeS50aGVuKCgpID0+IHtcbiAgICAgIGlmICh0aGlzLmF1dG9zYXZlKSB7XG4gICAgICAgIGhhbmRsZXIuc3RhcnQoKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgICBjb250ZXh0LmRpc3Bvc2VkLmNvbm5lY3QodGhpcy5fb25Db250ZXh0RGlzcG9zZWQsIHRoaXMpO1xuICAgIHRoaXMuX2NvbnRleHRzLnB1c2goY29udGV4dCk7XG4gICAgcmV0dXJuIGNvbnRleHQ7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY29udGV4dCBkaXNwb3NhbC5cbiAgICovXG4gIHByaXZhdGUgX29uQ29udGV4dERpc3Bvc2VkKGNvbnRleHQ6IFByaXZhdGUuSUNvbnRleHQpOiB2b2lkIHtcbiAgICBBcnJheUV4dC5yZW1vdmVGaXJzdE9mKHRoaXMuX2NvbnRleHRzLCBjb250ZXh0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHdpZGdldCBmYWN0b3J5IGZvciBhIGdpdmVuIHdpZGdldCBuYW1lLlxuICAgKi9cbiAgcHJpdmF0ZSBfd2lkZ2V0RmFjdG9yeUZvcihcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgd2lkZ2V0TmFtZTogc3RyaW5nXG4gICk6IERvY3VtZW50UmVnaXN0cnkuV2lkZ2V0RmFjdG9yeSB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3QgeyByZWdpc3RyeSB9ID0gdGhpcztcbiAgICBpZiAod2lkZ2V0TmFtZSA9PT0gJ2RlZmF1bHQnKSB7XG4gICAgICBjb25zdCBmYWN0b3J5ID0gcmVnaXN0cnkuZGVmYXVsdFdpZGdldEZhY3RvcnkocGF0aCk7XG4gICAgICBpZiAoIWZhY3RvcnkpIHtcbiAgICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICAgIH1cbiAgICAgIHdpZGdldE5hbWUgPSBmYWN0b3J5Lm5hbWU7XG4gICAgfVxuICAgIHJldHVybiByZWdpc3RyeS5nZXRXaWRnZXRGYWN0b3J5KHdpZGdldE5hbWUpO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZXMgYSBuZXcgZG9jdW1lbnQsIG9yIGxvYWRzIG9uZSBmcm9tIGRpc2ssIGRlcGVuZGluZyBvbiB0aGUgYHdoaWNoYCBhcmd1bWVudC5cbiAgICogSWYgYHdoaWNoPT09J2NyZWF0ZSdgLCB0aGVuIGl0IGNyZWF0ZXMgYSBuZXcgZG9jdW1lbnQuIElmIGB3aGljaD09PSdvcGVuJ2AsXG4gICAqIHRoZW4gaXQgbG9hZHMgdGhlIGRvY3VtZW50IGZyb20gZGlzay5cbiAgICpcbiAgICogVGhlIHR3byBjYXNlcyBkaWZmZXIgaW4gaG93IHRoZSBkb2N1bWVudCBjb250ZXh0IGlzIGhhbmRsZWQsIGJ1dCB0aGUgY3JlYXRpb25cbiAgICogb2YgdGhlIHdpZGdldCBhbmQgbGF1bmNoaW5nIG9mIHRoZSBrZXJuZWwgYXJlIGlkZW50aWNhbC5cbiAgICovXG4gIHByaXZhdGUgX2NyZWF0ZU9yT3BlbkRvY3VtZW50KFxuICAgIHdoaWNoOiAnb3BlbicgfCAnY3JlYXRlJyxcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgd2lkZ2V0TmFtZSA9ICdkZWZhdWx0JyxcbiAgICBrZXJuZWw/OiBQYXJ0aWFsPEtlcm5lbC5JTW9kZWw+LFxuICAgIG9wdGlvbnM/OiBEb2N1bWVudFJlZ2lzdHJ5LklPcGVuT3B0aW9uc1xuICApOiBJRG9jdW1lbnRXaWRnZXQgfCB1bmRlZmluZWQge1xuICAgIGNvbnN0IHdpZGdldEZhY3RvcnkgPSB0aGlzLl93aWRnZXRGYWN0b3J5Rm9yKHBhdGgsIHdpZGdldE5hbWUpO1xuICAgIGlmICghd2lkZ2V0RmFjdG9yeSkge1xuICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9XG4gICAgY29uc3QgbW9kZWxOYW1lID0gd2lkZ2V0RmFjdG9yeS5tb2RlbE5hbWUgfHwgJ3RleHQnO1xuICAgIGNvbnN0IGZhY3RvcnkgPSB0aGlzLnJlZ2lzdHJ5LmdldE1vZGVsRmFjdG9yeShtb2RlbE5hbWUpO1xuICAgIGlmICghZmFjdG9yeSkge1xuICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9XG5cbiAgICAvLyBIYW5kbGUgdGhlIGtlcm5lbCBwcmVmZXJlbmNlLlxuICAgIGNvbnN0IHByZWZlcmVuY2UgPSB0aGlzLnJlZ2lzdHJ5LmdldEtlcm5lbFByZWZlcmVuY2UoXG4gICAgICBwYXRoLFxuICAgICAgd2lkZ2V0RmFjdG9yeS5uYW1lLFxuICAgICAga2VybmVsXG4gICAgKTtcblxuICAgIGxldCBjb250ZXh0OiBQcml2YXRlLklDb250ZXh0IHwgbnVsbDtcbiAgICBsZXQgcmVhZHk6IFByb21pc2U8dm9pZD4gPSBQcm9taXNlLnJlc29sdmUodW5kZWZpbmVkKTtcblxuICAgIC8vIEhhbmRsZSB0aGUgbG9hZC1mcm9tLWRpc2sgY2FzZVxuICAgIGlmICh3aGljaCA9PT0gJ29wZW4nKSB7XG4gICAgICAvLyBVc2UgYW4gZXhpc3RpbmcgY29udGV4dCBpZiBhdmFpbGFibGUuXG4gICAgICBjb250ZXh0ID0gdGhpcy5fZmluZENvbnRleHQocGF0aCwgZmFjdG9yeS5uYW1lKSB8fCBudWxsO1xuICAgICAgaWYgKCFjb250ZXh0KSB7XG4gICAgICAgIGNvbnRleHQgPSB0aGlzLl9jcmVhdGVDb250ZXh0KHBhdGgsIGZhY3RvcnksIHByZWZlcmVuY2UpO1xuICAgICAgICAvLyBQb3B1bGF0ZSB0aGUgbW9kZWwsIGVpdGhlciBmcm9tIGRpc2sgb3IgYVxuICAgICAgICAvLyBtb2RlbCBiYWNrZW5kLlxuICAgICAgICByZWFkeSA9IHRoaXMuX3doZW4udGhlbigoKSA9PiBjb250ZXh0IS5pbml0aWFsaXplKGZhbHNlKSk7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmICh3aGljaCA9PT0gJ2NyZWF0ZScpIHtcbiAgICAgIGNvbnRleHQgPSB0aGlzLl9jcmVhdGVDb250ZXh0KHBhdGgsIGZhY3RvcnksIHByZWZlcmVuY2UpO1xuICAgICAgLy8gSW1tZWRpYXRlbHkgc2F2ZSB0aGUgY29udGVudHMgdG8gZGlzay5cbiAgICAgIHJlYWR5ID0gdGhpcy5fd2hlbi50aGVuKCgpID0+IGNvbnRleHQhLmluaXRpYWxpemUodHJ1ZSkpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYEludmFsaWQgYXJndW1lbnQgJ3doaWNoJzogJHt3aGljaH1gKTtcbiAgICB9XG5cbiAgICBjb25zdCB3aWRnZXQgPSB0aGlzLl93aWRnZXRNYW5hZ2VyLmNyZWF0ZVdpZGdldCh3aWRnZXRGYWN0b3J5LCBjb250ZXh0KTtcbiAgICB0aGlzLl9vcGVuZXIub3Blbih3aWRnZXQsIG9wdGlvbnMgfHwge30pO1xuXG4gICAgLy8gSWYgdGhlIGluaXRpYWwgb3BlbmluZyBvZiB0aGUgY29udGV4dCBmYWlscywgZGlzcG9zZSBvZiB0aGUgd2lkZ2V0LlxuICAgIHJlYWR5LmNhdGNoKGVyciA9PiB7XG4gICAgICB3aWRnZXQuY2xvc2UoKTtcbiAgICB9KTtcblxuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGFuIGFjdGl2YXRlUmVxdWVzdGVkIHNpZ25hbCBmcm9tIHRoZSB3aWRnZXQgbWFuYWdlci5cbiAgICovXG4gIHByaXZhdGUgX29uQWN0aXZhdGVSZXF1ZXN0ZWQoXG4gICAgc2VuZGVyOiBEb2N1bWVudFdpZGdldE1hbmFnZXIsXG4gICAgYXJnczogc3RyaW5nXG4gICk6IHZvaWQge1xuICAgIHRoaXMuX2FjdGl2YXRlUmVxdWVzdGVkLmVtaXQoYXJncyk7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX2FjdGl2YXRlUmVxdWVzdGVkID0gbmV3IFNpZ25hbDx0aGlzLCBzdHJpbmc+KHRoaXMpO1xuICBwcml2YXRlIF9jb250ZXh0czogUHJpdmF0ZS5JQ29udGV4dFtdID0gW107XG4gIHByaXZhdGUgX29wZW5lcjogRG9jdW1lbnRNYW5hZ2VyLklXaWRnZXRPcGVuZXI7XG4gIHByaXZhdGUgX3dpZGdldE1hbmFnZXI6IERvY3VtZW50V2lkZ2V0TWFuYWdlcjtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xuICBwcml2YXRlIF9hdXRvc2F2ZSA9IHRydWU7XG4gIHByaXZhdGUgX2F1dG9zYXZlSW50ZXJ2YWwgPSAxMjA7XG4gIHByaXZhdGUgX2xhc3RNb2RpZmllZENoZWNrTWFyZ2luID0gNTAwO1xuICBwcml2YXRlIF93aGVuOiBQcm9taXNlPHZvaWQ+O1xuICBwcml2YXRlIF9zZXRCdXN5OiAoKCkgPT4gSURpc3Bvc2FibGUpIHwgdW5kZWZpbmVkO1xuICBwcml2YXRlIF9kaWFsb2dzOiBJU2Vzc2lvbkNvbnRleHQuSURpYWxvZ3M7XG4gIHByaXZhdGUgX2RvY1Byb3ZpZGVyRmFjdG9yeTogSURvY3VtZW50UHJvdmlkZXJGYWN0b3J5IHwgdW5kZWZpbmVkO1xuICBwcml2YXRlIF9jb2xsYWJvcmF0aXZlOiBib29sZWFuO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBkb2N1bWVudCBtYW5hZ2VyIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgRG9jdW1lbnRNYW5hZ2VyIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gaW5pdGlhbGl6ZSBhIGRvY3VtZW50IG1hbmFnZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBBIGRvY3VtZW50IHJlZ2lzdHJ5IGluc3RhbmNlLlxuICAgICAqL1xuICAgIHJlZ2lzdHJ5OiBEb2N1bWVudFJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogQSBzZXJ2aWNlIG1hbmFnZXIgaW5zdGFuY2UuXG4gICAgICovXG4gICAgbWFuYWdlcjogU2VydmljZU1hbmFnZXIuSU1hbmFnZXI7XG5cbiAgICAvKipcbiAgICAgKiBBIHdpZGdldCBvcGVuZXIgZm9yIHNpYmxpbmcgd2lkZ2V0cy5cbiAgICAgKi9cbiAgICBvcGVuZXI6IElXaWRnZXRPcGVuZXI7XG5cbiAgICAvKipcbiAgICAgKiBBIHByb21pc2UgZm9yIHdoZW4gdG8gc3RhcnQgdXNpbmcgdGhlIG1hbmFnZXIuXG4gICAgICovXG4gICAgd2hlbj86IFByb21pc2U8dm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIGNhbGxlZCB3aGVuIGEga2VybmVsIGlzIGJ1c3kuXG4gICAgICovXG4gICAgc2V0QnVzeT86ICgpID0+IElEaXNwb3NhYmxlO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHByb3ZpZGVyIGZvciBzZXNzaW9uIGRpYWxvZ3MuXG4gICAgICovXG4gICAgc2Vzc2lvbkRpYWxvZ3M/OiBJU2Vzc2lvbkNvbnRleHQuSURpYWxvZ3M7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG5cbiAgICAvKipcbiAgICAgKiBBIGZhY3RvcnkgbWV0aG9kIGZvciB0aGUgZG9jdW1lbnQgcHJvdmlkZXIuXG4gICAgICovXG4gICAgZG9jUHJvdmlkZXJGYWN0b3J5PzogSURvY3VtZW50UHJvdmlkZXJGYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0aGUgY29udGV4dCBzaG91bGQgYmUgY29sbGFib3JhdGl2ZS5cbiAgICAgKiBJZiB0cnVlLCB0aGUgY29udGV4dCB3aWxsIGNvbm5lY3QgdGhyb3VnaCB5anNfd3Nfc2VydmVyIHRvIHNoYXJlIGluZm9ybWF0aW9uIGlmIHBvc3NpYmxlLlxuICAgICAqL1xuICAgIGNvbGxhYm9yYXRpdmU/OiBib29sZWFuO1xuICB9XG5cbiAgLyoqXG4gICAqIEFuIGludGVyZmFjZSBmb3IgYSB3aWRnZXQgb3BlbmVyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJV2lkZ2V0T3BlbmVyIHtcbiAgICAvKipcbiAgICAgKiBPcGVuIHRoZSBnaXZlbiB3aWRnZXQuXG4gICAgICovXG4gICAgb3BlbihcbiAgICAgIHdpZGdldDogSURvY3VtZW50V2lkZ2V0LFxuICAgICAgb3B0aW9ucz86IERvY3VtZW50UmVnaXN0cnkuSU9wZW5PcHRpb25zXG4gICAgKTogdm9pZDtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIEFuIGF0dGFjaGVkIHByb3BlcnR5IGZvciBhIGNvbnRleHQgc2F2ZSBoYW5kbGVyLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IHNhdmVIYW5kbGVyUHJvcGVydHkgPSBuZXcgQXR0YWNoZWRQcm9wZXJ0eTxcbiAgICBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQsXG4gICAgU2F2ZUhhbmRsZXIgfCB1bmRlZmluZWRcbiAgPih7XG4gICAgbmFtZTogJ3NhdmVIYW5kbGVyJyxcbiAgICBjcmVhdGU6ICgpID0+IHVuZGVmaW5lZFxuICB9KTtcblxuICAvKipcbiAgICogQSB0eXBlIGFsaWFzIGZvciBhIHN0YW5kYXJkIGNvbnRleHQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogV2UgZGVmaW5lIHRoaXMgYXMgYW4gaW50ZXJmYWNlIG9mIGEgc3BlY2lmaWMgaW1wbGVtZW50YXRpb24gc28gdGhhdCB3ZSBjYW5cbiAgICogdXNlIHRoZSBpbXBsZW1lbnRhdGlvbi1zcGVjaWZpYyBmdW5jdGlvbnMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDb250ZXh0IGV4dGVuZHMgQ29udGV4dDxEb2N1bWVudFJlZ2lzdHJ5LklNb2RlbD4ge1xuICAgIC8qIG5vIG9wICovXG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgVkRvbU1vZGVsLCBWRG9tUmVuZGVyZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBQYXRoRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7IERvY3VtZW50UmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9kb2NyZWdpc3RyeSc7XG5pbXBvcnQgeyBUZXh0SXRlbSB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXR1c2Jhcic7XG5pbXBvcnQgeyBUaXRsZSwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBJRG9jdW1lbnRNYW5hZ2VyIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBQYXRoU3RhdHVzQ29tcG9uZW50IHN0YXRpY3MuXG4gKi9cbm5hbWVzcGFjZSBQYXRoU3RhdHVzQ29tcG9uZW50IHtcbiAgLyoqXG4gICAqIFRoZSBwcm9wcyBmb3IgcmVuZGVyaW5nIGEgUGF0aFN0YXR1c0NvbXBvbmVudC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVByb3BzIHtcbiAgICAvKipcbiAgICAgKiBUaGUgZnVsbCBwYXRoIGZvciBhIGRvY3VtZW50LlxuICAgICAqL1xuICAgIGZ1bGxQYXRoOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2hvcnRlciBuYW1lIGZvciBhIGRvY3VtZW50IG9yIGFjdGl2aXR5LlxuICAgICAqL1xuICAgIG5hbWU6IHN0cmluZztcbiAgfVxufVxuXG4vKipcbiAqIEEgcHVyZSBjb21wb25lbnQgZm9yIHJlbmRlcmluZyBhIGZpbGUgcGF0aCAob3IgYWN0aXZpdHkgbmFtZSkuXG4gKlxuICogQHBhcmFtIHByb3BzIC0gdGhlIHByb3BzIGZvciB0aGUgY29tcG9uZW50LlxuICpcbiAqIEByZXR1cm5zIGEgdHN4IGNvbXBvbmVudCBmb3IgYSBmaWxlIHBhdGguXG4gKi9cbmZ1bmN0aW9uIFBhdGhTdGF0dXNDb21wb25lbnQoXG4gIHByb3BzOiBQYXRoU3RhdHVzQ29tcG9uZW50LklQcm9wc1xuKTogUmVhY3QuUmVhY3RFbGVtZW50PFBhdGhTdGF0dXNDb21wb25lbnQuSVByb3BzPiB7XG4gIHJldHVybiA8VGV4dEl0ZW0gc291cmNlPXtwcm9wcy5uYW1lfSB0aXRsZT17cHJvcHMuZnVsbFBhdGh9IC8+O1xufVxuXG4vKipcbiAqIEEgc3RhdHVzIGJhciBpdGVtIGZvciB0aGUgY3VycmVudCBmaWxlIHBhdGggKG9yIGFjdGl2aXR5IG5hbWUpLlxuICovXG5leHBvcnQgY2xhc3MgUGF0aFN0YXR1cyBleHRlbmRzIFZEb21SZW5kZXJlcjxQYXRoU3RhdHVzLk1vZGVsPiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgUGF0aFN0YXR1cyBzdGF0dXMgaXRlbS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdHM6IFBhdGhTdGF0dXMuSU9wdGlvbnMpIHtcbiAgICBzdXBlcihuZXcgUGF0aFN0YXR1cy5Nb2RlbChvcHRzLmRvY01hbmFnZXIpKTtcbiAgICB0aGlzLm5vZGUudGl0bGUgPSB0aGlzLm1vZGVsLnBhdGg7XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIHRoZSBzdGF0dXMgaXRlbS5cbiAgICovXG4gIHJlbmRlcigpIHtcbiAgICByZXR1cm4gKFxuICAgICAgPFBhdGhTdGF0dXNDb21wb25lbnRcbiAgICAgICAgZnVsbFBhdGg9e3RoaXMubW9kZWwhLnBhdGh9XG4gICAgICAgIG5hbWU9e3RoaXMubW9kZWwhLm5hbWUhfVxuICAgICAgLz5cbiAgICApO1xuICB9XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIFBhdGhTdGF0dXMgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBQYXRoU3RhdHVzIHtcbiAgLyoqXG4gICAqIEEgVkRvbU1vZGVsIGZvciByZW5kZXJpbmcgdGhlIFBhdGhTdGF0dXMgc3RhdHVzIGl0ZW0uXG4gICAqL1xuICBleHBvcnQgY2xhc3MgTW9kZWwgZXh0ZW5kcyBWRG9tTW9kZWwge1xuICAgIC8qKlxuICAgICAqIENvbnN0cnVjdCBhIG5ldyBtb2RlbC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBkb2NNYW5hZ2VyOiB0aGUgYXBwbGljYXRpb24gZG9jdW1lbnQgbWFuYWdlci4gVXNlZCB0byBjaGVja1xuICAgICAqICAgd2hldGhlciB0aGUgY3VycmVudCB3aWRnZXQgaXMgYSBkb2N1bWVudC5cbiAgICAgKi9cbiAgICBjb25zdHJ1Y3Rvcihkb2NNYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyKSB7XG4gICAgICBzdXBlcigpO1xuICAgICAgdGhpcy5fZG9jTWFuYWdlciA9IGRvY01hbmFnZXI7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgcGF0aCBmb3IgdGhlIGFwcGxpY2F0aW9uLlxuICAgICAqL1xuICAgIGdldCBwYXRoKCk6IHN0cmluZyB7XG4gICAgICByZXR1cm4gdGhpcy5fcGF0aDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmFtZSBvZiB0aGUgY3VycmVudCBhY3Rpdml0eS5cbiAgICAgKi9cbiAgICBnZXQgbmFtZSgpOiBzdHJpbmcge1xuICAgICAgcmV0dXJuIHRoaXMuX25hbWU7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgd2lkZ2V0IGZvciB0aGUgYXBwbGljYXRpb24uXG4gICAgICovXG4gICAgZ2V0IHdpZGdldCgpOiBXaWRnZXQgfCBudWxsIHtcbiAgICAgIHJldHVybiB0aGlzLl93aWRnZXQ7XG4gICAgfVxuICAgIHNldCB3aWRnZXQod2lkZ2V0OiBXaWRnZXQgfCBudWxsKSB7XG4gICAgICBjb25zdCBvbGRXaWRnZXQgPSB0aGlzLl93aWRnZXQ7XG4gICAgICBpZiAob2xkV2lkZ2V0ICE9PSBudWxsKSB7XG4gICAgICAgIGNvbnN0IG9sZENvbnRleHQgPSB0aGlzLl9kb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQob2xkV2lkZ2V0KTtcbiAgICAgICAgaWYgKG9sZENvbnRleHQpIHtcbiAgICAgICAgICBvbGRDb250ZXh0LnBhdGhDaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy5fb25QYXRoQ2hhbmdlKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBvbGRXaWRnZXQudGl0bGUuY2hhbmdlZC5kaXNjb25uZWN0KHRoaXMuX29uVGl0bGVDaGFuZ2UpO1xuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IG9sZFN0YXRlID0gdGhpcy5fZ2V0QWxsU3RhdGUoKTtcbiAgICAgIHRoaXMuX3dpZGdldCA9IHdpZGdldDtcbiAgICAgIGlmICh0aGlzLl93aWRnZXQgPT09IG51bGwpIHtcbiAgICAgICAgdGhpcy5fcGF0aCA9ICcnO1xuICAgICAgICB0aGlzLl9uYW1lID0gJyc7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBjb25zdCB3aWRnZXRDb250ZXh0ID0gdGhpcy5fZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KHRoaXMuX3dpZGdldCk7XG4gICAgICAgIGlmICh3aWRnZXRDb250ZXh0KSB7XG4gICAgICAgICAgdGhpcy5fcGF0aCA9IHdpZGdldENvbnRleHQucGF0aDtcbiAgICAgICAgICB0aGlzLl9uYW1lID0gUGF0aEV4dC5iYXNlbmFtZSh3aWRnZXRDb250ZXh0LnBhdGgpO1xuXG4gICAgICAgICAgd2lkZ2V0Q29udGV4dC5wYXRoQ2hhbmdlZC5jb25uZWN0KHRoaXMuX29uUGF0aENoYW5nZSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgdGhpcy5fcGF0aCA9ICcnO1xuICAgICAgICAgIHRoaXMuX25hbWUgPSB0aGlzLl93aWRnZXQudGl0bGUubGFiZWw7XG5cbiAgICAgICAgICB0aGlzLl93aWRnZXQudGl0bGUuY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uVGl0bGVDaGFuZ2UpO1xuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIHRoaXMuX3RyaWdnZXJDaGFuZ2Uob2xkU3RhdGUsIHRoaXMuX2dldEFsbFN0YXRlKCkpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlYWN0IHRvIGEgdGl0bGUgY2hhbmdlIGZvciB0aGUgY3VycmVudCB3aWRnZXQuXG4gICAgICovXG4gICAgcHJpdmF0ZSBfb25UaXRsZUNoYW5nZSA9ICh0aXRsZTogVGl0bGU8V2lkZ2V0PikgPT4ge1xuICAgICAgY29uc3Qgb2xkU3RhdGUgPSB0aGlzLl9nZXRBbGxTdGF0ZSgpO1xuICAgICAgdGhpcy5fbmFtZSA9IHRpdGxlLmxhYmVsO1xuICAgICAgdGhpcy5fdHJpZ2dlckNoYW5nZShvbGRTdGF0ZSwgdGhpcy5fZ2V0QWxsU3RhdGUoKSk7XG4gICAgfTtcblxuICAgIC8qKlxuICAgICAqIFJlYWN0IHRvIGEgcGF0aCBjaGFuZ2UgZm9yIHRoZSBjdXJyZW50IGRvY3VtZW50LlxuICAgICAqL1xuICAgIHByaXZhdGUgX29uUGF0aENoYW5nZSA9IChcbiAgICAgIF9kb2N1bWVudE1vZGVsOiBEb2N1bWVudFJlZ2lzdHJ5LklDb250ZXh0PERvY3VtZW50UmVnaXN0cnkuSU1vZGVsPixcbiAgICAgIG5ld1BhdGg6IHN0cmluZ1xuICAgICkgPT4ge1xuICAgICAgY29uc3Qgb2xkU3RhdGUgPSB0aGlzLl9nZXRBbGxTdGF0ZSgpO1xuICAgICAgdGhpcy5fcGF0aCA9IG5ld1BhdGg7XG4gICAgICB0aGlzLl9uYW1lID0gUGF0aEV4dC5iYXNlbmFtZShuZXdQYXRoKTtcblxuICAgICAgdGhpcy5fdHJpZ2dlckNoYW5nZShvbGRTdGF0ZSwgdGhpcy5fZ2V0QWxsU3RhdGUoKSk7XG4gICAgfTtcblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgY3VycmVudCBzdGF0ZSBvZiB0aGUgbW9kZWwuXG4gICAgICovXG4gICAgcHJpdmF0ZSBfZ2V0QWxsU3RhdGUoKTogW3N0cmluZywgc3RyaW5nXSB7XG4gICAgICByZXR1cm4gW3RoaXMuX3BhdGgsIHRoaXMuX25hbWVdO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRyaWdnZXIgYSBzdGF0ZSBjaGFuZ2UgdG8gcmVyZW5kZXIuXG4gICAgICovXG4gICAgcHJpdmF0ZSBfdHJpZ2dlckNoYW5nZShcbiAgICAgIG9sZFN0YXRlOiBbc3RyaW5nLCBzdHJpbmddLFxuICAgICAgbmV3U3RhdGU6IFtzdHJpbmcsIHN0cmluZ11cbiAgICApIHtcbiAgICAgIGlmIChvbGRTdGF0ZVswXSAhPT0gbmV3U3RhdGVbMF0gfHwgb2xkU3RhdGVbMV0gIT09IG5ld1N0YXRlWzFdKSB7XG4gICAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICBwcml2YXRlIF9wYXRoOiBzdHJpbmcgPSAnJztcbiAgICBwcml2YXRlIF9uYW1lOiBzdHJpbmcgPSAnJztcbiAgICBwcml2YXRlIF93aWRnZXQ6IFdpZGdldCB8IG51bGwgPSBudWxsO1xuICAgIHByaXZhdGUgX2RvY01hbmFnZXI6IElEb2N1bWVudE1hbmFnZXI7XG4gIH1cblxuICAvKipcbiAgICogT3B0aW9ucyBmb3IgY3JlYXRpbmcgdGhlIFBhdGhTdGF0dXMgd2lkZ2V0LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGFwcGxpY2F0aW9uIGRvY3VtZW50IG1hbmFnZXIuXG4gICAgICovXG4gICAgZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcjtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBEb2N1bWVudFJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCBtYW5hZ2VzIHRoZSBhdXRvIHNhdmluZyBvZiBhIGRvY3VtZW50LlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIEltcGxlbWVudHMgaHR0cHM6Ly9naXRodWIuY29tL2lweXRob24vaXB5dGhvbi93aWtpL0lQRVAtMTU6LUF1dG9zYXZpbmctdGhlLUlQeXRob24tTm90ZWJvb2suXG4gKi9cbmV4cG9ydCBjbGFzcyBTYXZlSGFuZGxlciBpbXBsZW1lbnRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBzYXZlIGhhbmRsZXIuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBTYXZlSGFuZGxlci5JT3B0aW9ucykge1xuICAgIHRoaXMuX2NvbnRleHQgPSBvcHRpb25zLmNvbnRleHQ7XG4gICAgY29uc3QgaW50ZXJ2YWwgPSBvcHRpb25zLnNhdmVJbnRlcnZhbCB8fCAxMjA7XG4gICAgdGhpcy5fbWluSW50ZXJ2YWwgPSBpbnRlcnZhbCAqIDEwMDA7XG4gICAgdGhpcy5faW50ZXJ2YWwgPSB0aGlzLl9taW5JbnRlcnZhbDtcbiAgICAvLyBSZXN0YXJ0IHRoZSB0aW1lciB3aGVuIHRoZSBjb250ZW50cyBtb2RlbCBpcyB1cGRhdGVkLlxuICAgIHRoaXMuX2NvbnRleHQuZmlsZUNoYW5nZWQuY29ubmVjdCh0aGlzLl9zZXRUaW1lciwgdGhpcyk7XG4gICAgdGhpcy5fY29udGV4dC5kaXNwb3NlZC5jb25uZWN0KHRoaXMuZGlzcG9zZSwgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNhdmUgaW50ZXJ2YWwgdXNlZCBieSB0aGUgdGltZXIgKGluIHNlY29uZHMpLlxuICAgKi9cbiAgZ2V0IHNhdmVJbnRlcnZhbCgpOiBudW1iZXIge1xuICAgIHJldHVybiB0aGlzLl9pbnRlcnZhbCAvIDEwMDA7XG4gIH1cbiAgc2V0IHNhdmVJbnRlcnZhbCh2YWx1ZTogbnVtYmVyKSB7XG4gICAgdGhpcy5fbWluSW50ZXJ2YWwgPSB0aGlzLl9pbnRlcnZhbCA9IHZhbHVlICogMTAwMDtcbiAgICBpZiAodGhpcy5faXNBY3RpdmUpIHtcbiAgICAgIHRoaXMuX3NldFRpbWVyKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEdldCB3aGV0aGVyIHRoZSBoYW5kbGVyIGlzIGFjdGl2ZS5cbiAgICovXG4gIGdldCBpc0FjdGl2ZSgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNBY3RpdmU7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHdoZXRoZXIgdGhlIHNhdmUgaGFuZGxlciBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyB1c2VkIGJ5IHRoZSBzYXZlIGhhbmRsZXIuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgY2xlYXJUaW1lb3V0KHRoaXMuX2F1dG9zYXZlVGltZXIpO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogU3RhcnQgdGhlIGF1dG9zYXZlci5cbiAgICovXG4gIHN0YXJ0KCk6IHZvaWQge1xuICAgIHRoaXMuX2lzQWN0aXZlID0gdHJ1ZTtcbiAgICB0aGlzLl9zZXRUaW1lcigpO1xuICB9XG5cbiAgLyoqXG4gICAqIFN0b3AgdGhlIGF1dG9zYXZlci5cbiAgICovXG4gIHN0b3AoKTogdm9pZCB7XG4gICAgdGhpcy5faXNBY3RpdmUgPSBmYWxzZTtcbiAgICBjbGVhclRpbWVvdXQodGhpcy5fYXV0b3NhdmVUaW1lcik7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSB0aW1lci5cbiAgICovXG4gIHByaXZhdGUgX3NldFRpbWVyKCk6IHZvaWQge1xuICAgIGNsZWFyVGltZW91dCh0aGlzLl9hdXRvc2F2ZVRpbWVyKTtcbiAgICBpZiAoIXRoaXMuX2lzQWN0aXZlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2F1dG9zYXZlVGltZXIgPSB3aW5kb3cuc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICB0aGlzLl9zYXZlKCk7XG4gICAgfSwgdGhpcy5faW50ZXJ2YWwpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhbiBhdXRvc2F2ZSB0aW1lb3V0LlxuICAgKi9cbiAgcHJpdmF0ZSBfc2F2ZSgpOiB2b2lkIHtcbiAgICBjb25zdCBjb250ZXh0ID0gdGhpcy5fY29udGV4dDtcblxuICAgIC8vIFRyaWdnZXIgdGhlIG5leHQgdXBkYXRlLlxuICAgIHRoaXMuX3NldFRpbWVyKCk7XG5cbiAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBCYWlsIGlmIHRoZSBtb2RlbCBpcyBub3QgZGlydHkgb3IgdGhlIGZpbGUgaXMgbm90IHdyaXRhYmxlLCBvciB0aGUgZGlhbG9nXG4gICAgLy8gaXMgYWxyZWFkeSBzaG93aW5nLlxuICAgIGNvbnN0IHdyaXRhYmxlID0gY29udGV4dC5jb250ZW50c01vZGVsICYmIGNvbnRleHQuY29udGVudHNNb2RlbC53cml0YWJsZTtcbiAgICBpZiAoIXdyaXRhYmxlIHx8ICFjb250ZXh0Lm1vZGVsLmRpcnR5IHx8IHRoaXMuX2luRGlhbG9nKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3Qgc3RhcnQgPSBuZXcgRGF0ZSgpLmdldFRpbWUoKTtcbiAgICBjb250ZXh0XG4gICAgICAuc2F2ZSgpXG4gICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgZHVyYXRpb24gPSBuZXcgRGF0ZSgpLmdldFRpbWUoKSAtIHN0YXJ0O1xuICAgICAgICAvLyBOZXcgc2F2ZSBpbnRlcnZhbDogaGlnaGVyIG9mIDEweCBzYXZlIGR1cmF0aW9uIG9yIG1pbiBpbnRlcnZhbC5cbiAgICAgICAgdGhpcy5faW50ZXJ2YWwgPSBNYXRoLm1heChcbiAgICAgICAgICB0aGlzLl9tdWx0aXBsaWVyICogZHVyYXRpb24sXG4gICAgICAgICAgdGhpcy5fbWluSW50ZXJ2YWxcbiAgICAgICAgKTtcbiAgICAgICAgLy8gUmVzdGFydCB0aGUgdXBkYXRlIHRvIHBpY2sgdXAgdGhlIG5ldyBpbnRlcnZhbC5cbiAgICAgICAgdGhpcy5fc2V0VGltZXIoKTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goZXJyID0+IHtcbiAgICAgICAgLy8gSWYgdGhlIHVzZXIgY2FuY2VsZWQgdGhlIHNhdmUsIGRvIG5vdGhpbmcuXG4gICAgICAgIC8vIEZJWE1FLVRSQU5TOiBJcyB0aGlzIGFmZmVjdGVkIGJ5IGxvY2FsaXphdGlvbj9cbiAgICAgICAgaWYgKGVyci5tZXNzYWdlID09PSAnQ2FuY2VsJykge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICAvLyBPdGhlcndpc2UsIGxvZyB0aGUgZXJyb3IuXG4gICAgICAgIGNvbnNvbGUuZXJyb3IoJ0Vycm9yIGluIEF1dG8tU2F2ZScsIGVyci5tZXNzYWdlKTtcbiAgICAgIH0pO1xuICB9XG5cbiAgcHJpdmF0ZSBfYXV0b3NhdmVUaW1lciA9IC0xO1xuICBwcml2YXRlIF9taW5JbnRlcnZhbCA9IC0xO1xuICBwcml2YXRlIF9pbnRlcnZhbCA9IC0xO1xuICBwcml2YXRlIF9jb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQ7XG4gIHByaXZhdGUgX2lzQWN0aXZlID0gZmFsc2U7XG4gIHByaXZhdGUgX2luRGlhbG9nID0gZmFsc2U7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfbXVsdGlwbGllciA9IDEwO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgU2F2ZUhhbmRsZXJgIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgU2F2ZUhhbmRsZXIge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBjcmVhdGUgYSBzYXZlIGhhbmRsZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY29udGV4dCBhc3NvY2lhdGVkIHdpdGggdGhlIGZpbGUuXG4gICAgICovXG4gICAgY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIG1pbmltdW0gc2F2ZSBpbnRlcnZhbCBpbiBzZWNvbmRzIChkZWZhdWx0IGlzIHR3byBtaW51dGVzKS5cbiAgICAgKi9cbiAgICBzYXZlSW50ZXJ2YWw/OiBudW1iZXI7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgVkRvbU1vZGVsLCBWRG9tUmVuZGVyZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBEb2N1bWVudFJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgVGV4dEl0ZW0gfSBmcm9tICdAanVweXRlcmxhYi9zdGF0dXNiYXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBJRG9jdW1lbnRNYW5hZ2VyIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBTYXZpbmdTdGF0dXNDb21wb25lbnQgc3RhdGljcy5cbiAqL1xubmFtZXNwYWNlIFNhdmluZ1N0YXR1c0NvbXBvbmVudCB7XG4gIC8qKlxuICAgKiBUaGUgcHJvcHMgZm9yIHRoZSBTYXZpbmdTdGF0dXNDb21wb25lbnQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wcyB7XG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgc2F2aW5nIHN0YXR1cywgYWZ0ZXIgdHJhbnNsYXRpb24uXG4gICAgICovXG4gICAgZmlsZVN0YXR1czogc3RyaW5nO1xuICB9XG59XG5cbi8qKlxuICogQSBwdXJlIGZ1bmN0aW9uYWwgY29tcG9uZW50IGZvciBhIFNhdmluZyBzdGF0dXMgaXRlbS5cbiAqXG4gKiBAcGFyYW0gcHJvcHMgLSB0aGUgcHJvcHMgZm9yIHRoZSBjb21wb25lbnQuXG4gKlxuICogQHJldHVybnMgYSB0c3ggY29tcG9uZW50IGZvciByZW5kZXJpbmcgdGhlIHNhdmluZyBzdGF0ZS5cbiAqL1xuZnVuY3Rpb24gU2F2aW5nU3RhdHVzQ29tcG9uZW50KFxuICBwcm9wczogU2F2aW5nU3RhdHVzQ29tcG9uZW50LklQcm9wc1xuKTogUmVhY3QuUmVhY3RFbGVtZW50PFNhdmluZ1N0YXR1c0NvbXBvbmVudC5JUHJvcHM+IHtcbiAgcmV0dXJuIDxUZXh0SXRlbSBzb3VyY2U9e3Byb3BzLmZpbGVTdGF0dXN9IC8+O1xufVxuXG4vKipcbiAqIFRoZSBhbW91bnQgb2YgdGltZSAoaW4gbXMpIHRvIHJldGFpbiB0aGUgc2F2aW5nIGNvbXBsZXRlZCBtZXNzYWdlXG4gKiBiZWZvcmUgaGlkaW5nIHRoZSBzdGF0dXMgaXRlbS5cbiAqL1xuY29uc3QgU0FWSU5HX0NPTVBMRVRFX01FU1NBR0VfTUlMTElTID0gMjAwMDtcblxuLyoqXG4gKiBBIFZEb21SZW5kZXJlciBmb3IgYSBzYXZpbmcgc3RhdHVzIGl0ZW0uXG4gKi9cbmV4cG9ydCBjbGFzcyBTYXZpbmdTdGF0dXMgZXh0ZW5kcyBWRG9tUmVuZGVyZXI8U2F2aW5nU3RhdHVzLk1vZGVsPiB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgU2F2aW5nU3RhdHVzIGl0ZW0uXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRzOiBTYXZpbmdTdGF0dXMuSU9wdGlvbnMpIHtcbiAgICBzdXBlcihuZXcgU2F2aW5nU3RhdHVzLk1vZGVsKG9wdHMuZG9jTWFuYWdlcikpO1xuICAgIGNvbnN0IHRyYW5zbGF0b3IgPSBvcHRzLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICB0aGlzLl9zdGF0dXNNYXAgPSB7XG4gICAgICBjb21wbGV0ZWQ6IHRyYW5zLl9fKCdTYXZpbmcgY29tcGxldGVkJyksXG4gICAgICBzdGFydGVkOiB0cmFucy5fXygnU2F2aW5nIHN0YXJ0ZWQnKSxcbiAgICAgIGZhaWxlZDogdHJhbnMuX18oJ1NhdmluZyBmYWlsZWQnKVxuICAgIH07XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIHRoZSBTYXZpbmdTdGF0dXMgaXRlbS5cbiAgICovXG4gIHJlbmRlcigpIHtcbiAgICBpZiAodGhpcy5tb2RlbCA9PT0gbnVsbCB8fCB0aGlzLm1vZGVsLnN0YXR1cyA9PT0gbnVsbCkge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiAoXG4gICAgICAgIDxTYXZpbmdTdGF0dXNDb21wb25lbnRcbiAgICAgICAgICBmaWxlU3RhdHVzPXt0aGlzLl9zdGF0dXNNYXBbdGhpcy5tb2RlbC5zdGF0dXNdfVxuICAgICAgICAvPlxuICAgICAgKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9zdGF0dXNNYXA6IFJlY29yZDxEb2N1bWVudFJlZ2lzdHJ5LlNhdmVTdGF0ZSwgc3RyaW5nPjtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgU2F2aW5nU3RhdHVzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgU2F2aW5nU3RhdHVzIHtcbiAgLyoqXG4gICAqIEEgVkRvbU1vZGVsIGZvciB0aGUgU2F2aW5nU3RhdHVzIGl0ZW0uXG4gICAqL1xuICBleHBvcnQgY2xhc3MgTW9kZWwgZXh0ZW5kcyBWRG9tTW9kZWwge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyBTYXZpbmdTdGF0dXMgbW9kZWwuXG4gICAgICovXG4gICAgY29uc3RydWN0b3IoZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcikge1xuICAgICAgc3VwZXIoKTtcblxuICAgICAgdGhpcy5fc3RhdHVzID0gbnVsbDtcbiAgICAgIHRoaXMud2lkZ2V0ID0gbnVsbDtcbiAgICAgIHRoaXMuX2RvY01hbmFnZXIgPSBkb2NNYW5hZ2VyO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IHN0YXR1cyBvZiB0aGUgbW9kZWwuXG4gICAgICovXG4gICAgZ2V0IHN0YXR1cygpOiBEb2N1bWVudFJlZ2lzdHJ5LlNhdmVTdGF0ZSB8IG51bGwge1xuICAgICAgcmV0dXJuIHRoaXMuX3N0YXR1cyE7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgd2lkZ2V0IGZvciB0aGUgbW9kZWwuIEFueSB3aWRnZXQgY2FuIGJlIGFzc2lnbmVkLFxuICAgICAqIGJ1dCBpdCBvbmx5IGhhcyBhbnkgZWZmZWN0IGlmIHRoZSB3aWRnZXQgaXMgYW4gSURvY3VtZW50IHdpZGdldFxuICAgICAqIGtub3duIHRvIHRoZSBhcHBsaWNhdGlvbiBkb2N1bWVudCBtYW5hZ2VyLlxuICAgICAqL1xuICAgIGdldCB3aWRnZXQoKSB7XG4gICAgICByZXR1cm4gdGhpcy5fd2lkZ2V0O1xuICAgIH1cbiAgICBzZXQgd2lkZ2V0KHdpZGdldDogV2lkZ2V0IHwgbnVsbCkge1xuICAgICAgY29uc3Qgb2xkV2lkZ2V0ID0gdGhpcy5fd2lkZ2V0O1xuICAgICAgaWYgKG9sZFdpZGdldCAhPT0gbnVsbCkge1xuICAgICAgICBjb25zdCBvbGRDb250ZXh0ID0gdGhpcy5fZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KG9sZFdpZGdldCk7XG4gICAgICAgIGlmIChvbGRDb250ZXh0KSB7XG4gICAgICAgICAgb2xkQ29udGV4dC5zYXZlU3RhdGUuZGlzY29ubmVjdCh0aGlzLl9vblN0YXR1c0NoYW5nZSk7XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgdGhpcy5fd2lkZ2V0ID0gd2lkZ2V0O1xuICAgICAgaWYgKHRoaXMuX3dpZGdldCA9PT0gbnVsbCkge1xuICAgICAgICB0aGlzLl9zdGF0dXMgPSBudWxsO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0Q29udGV4dCA9IHRoaXMuX2RvY01hbmFnZXIuY29udGV4dEZvcldpZGdldCh0aGlzLl93aWRnZXQpO1xuICAgICAgICBpZiAod2lkZ2V0Q29udGV4dCkge1xuICAgICAgICAgIHdpZGdldENvbnRleHQuc2F2ZVN0YXRlLmNvbm5lY3QodGhpcy5fb25TdGF0dXNDaGFuZ2UpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVhY3QgdG8gYSBzYXZpbmcgc3RhdHVzIGNoYW5nZSBmcm9tIHRoZSBjdXJyZW50IGRvY3VtZW50IHdpZGdldC5cbiAgICAgKi9cbiAgICBwcml2YXRlIF9vblN0YXR1c0NoYW5nZSA9IChcbiAgICAgIF9kb2N1bWVudE1vZGVsOiBEb2N1bWVudFJlZ2lzdHJ5LklDb250ZXh0PERvY3VtZW50UmVnaXN0cnkuSU1vZGVsPixcbiAgICAgIG5ld1N0YXR1czogRG9jdW1lbnRSZWdpc3RyeS5TYXZlU3RhdGVcbiAgICApID0+IHtcbiAgICAgIHRoaXMuX3N0YXR1cyA9IG5ld1N0YXR1cztcblxuICAgICAgaWYgKHRoaXMuX3N0YXR1cyA9PT0gJ2NvbXBsZXRlZCcpIHtcbiAgICAgICAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICAgICAgdGhpcy5fc3RhdHVzID0gbnVsbDtcbiAgICAgICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gICAgICAgIH0sIFNBVklOR19DT01QTEVURV9NRVNTQUdFX01JTExJUyk7XG4gICAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICAgIH1cbiAgICB9O1xuXG4gICAgcHJpdmF0ZSBfc3RhdHVzOiBEb2N1bWVudFJlZ2lzdHJ5LlNhdmVTdGF0ZSB8IG51bGwgPSBudWxsO1xuICAgIHByaXZhdGUgX3dpZGdldDogV2lkZ2V0IHwgbnVsbCA9IG51bGw7XG4gICAgcHJpdmF0ZSBfZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBjcmVhdGluZyBhIG5ldyBTYXZlU3RhdHVzIGl0ZW1cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBhcHBsaWNhdGlvbiBkb2N1bWVudCBtYW5hZ2VyLlxuICAgICAqL1xuICAgIGRvY01hbmFnZXI6IElEb2N1bWVudE1hbmFnZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgRG9jdW1lbnRSZWdpc3RyeSwgSURvY3VtZW50V2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgQ29udGVudHMsIEtlcm5lbCwgU2VydmljZU1hbmFnZXIgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKiB0c2xpbnQ6ZGlzYWJsZSAqL1xuLyoqXG4gKiBUaGUgZG9jdW1lbnQgcmVnaXN0cnkgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJRG9jdW1lbnRNYW5hZ2VyID0gbmV3IFRva2VuPElEb2N1bWVudE1hbmFnZXI+KFxuICAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlcjpJRG9jdW1lbnRNYW5hZ2VyJ1xuKTtcbi8qIHRzbGludDplbmFibGUgKi9cblxuLyoqXG4gKiBUaGUgaW50ZXJmYWNlIGZvciBhIGRvY3VtZW50IG1hbmFnZXIuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSURvY3VtZW50TWFuYWdlciBleHRlbmRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIFRoZSByZWdpc3RyeSB1c2VkIGJ5IHRoZSBtYW5hZ2VyLlxuICAgKi9cbiAgcmVhZG9ubHkgcmVnaXN0cnk6IERvY3VtZW50UmVnaXN0cnk7XG5cbiAgLyoqXG4gICAqIFRoZSBzZXJ2aWNlIG1hbmFnZXIgdXNlZCBieSB0aGUgbWFuYWdlci5cbiAgICovXG4gIHJlYWRvbmx5IHNlcnZpY2VzOiBTZXJ2aWNlTWFuYWdlci5JTWFuYWdlcjtcblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIG9uZSBvZiB0aGUgZG9jdW1lbnRzIGlzIGFjdGl2YXRlZC5cbiAgICovXG4gIHJlYWRvbmx5IGFjdGl2YXRlUmVxdWVzdGVkOiBJU2lnbmFsPHRoaXMsIHN0cmluZz47XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdG8gYXV0b3NhdmUgZG9jdW1lbnRzLlxuICAgKi9cbiAgYXV0b3NhdmU6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIERldGVybWluZXMgdGhlIHRpbWUgaW50ZXJ2YWwgZm9yIGF1dG9zYXZlIGluIHNlY29uZHMuXG4gICAqL1xuICBhdXRvc2F2ZUludGVydmFsOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIENsb25lIGEgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gVGhlIHNvdXJjZSB3aWRnZXQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgbmV3IHdpZGdldCBvciBgdW5kZWZpbmVkYC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiAgVXNlcyB0aGUgc2FtZSB3aWRnZXQgZmFjdG9yeSBhbmQgY29udGV4dCBhcyB0aGUgc291cmNlLCBvciByZXR1cm5zXG4gICAqICBgdW5kZWZpbmVkYCBpZiB0aGUgc291cmNlIHdpZGdldCBpcyBub3QgbWFuYWdlZCBieSB0aGlzIG1hbmFnZXIuXG4gICAqL1xuICBjbG9uZVdpZGdldCh3aWRnZXQ6IFdpZGdldCk6IElEb2N1bWVudFdpZGdldCB8IHVuZGVmaW5lZDtcblxuICAvKipcbiAgICogQ2xvc2UgYWxsIG9mIHRoZSBvcGVuIGRvY3VtZW50cy5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHJlc29sdmluZyB3aGVuIHRoZSB3aWRnZXRzIGFyZSBjbG9zZWQuXG4gICAqL1xuICBjbG9zZUFsbCgpOiBQcm9taXNlPHZvaWQ+O1xuXG4gIC8qKlxuICAgKiBDbG9zZSB0aGUgd2lkZ2V0cyBhc3NvY2lhdGVkIHdpdGggYSBnaXZlbiBwYXRoLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aCAtIFRoZSB0YXJnZXQgcGF0aC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHJlc29sdmluZyB3aGVuIHRoZSB3aWRnZXRzIGFyZSBjbG9zZWQuXG4gICAqL1xuICBjbG9zZUZpbGUocGF0aDogc3RyaW5nKTogUHJvbWlzZTx2b2lkPjtcblxuICAvKipcbiAgICogR2V0IHRoZSBkb2N1bWVudCBjb250ZXh0IGZvciBhIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldCAtIFRoZSB3aWRnZXQgb2YgaW50ZXJlc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBjb250ZXh0IGFzc29jaWF0ZWQgd2l0aCB0aGUgd2lkZ2V0LCBvciBgdW5kZWZpbmVkYCBpZiBubyBzdWNoXG4gICAqIGNvbnRleHQgZXhpc3RzLlxuICAgKi9cbiAgY29udGV4dEZvcldpZGdldCh3aWRnZXQ6IFdpZGdldCk6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dCB8IHVuZGVmaW5lZDtcblxuICAvKipcbiAgICogQ29weSBhIGZpbGUuXG4gICAqXG4gICAqIEBwYXJhbSBmcm9tRmlsZSAtIFRoZSBmdWxsIHBhdGggb2YgdGhlIG9yaWdpbmFsIGZpbGUuXG4gICAqXG4gICAqIEBwYXJhbSB0b0RpciAtIFRoZSBmdWxsIHBhdGggdG8gdGhlIHRhcmdldCBkaXJlY3RvcnkuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB3aGljaCByZXNvbHZlcyB0byB0aGUgY29udGVudHMgb2YgdGhlIGZpbGUuXG4gICAqL1xuICBjb3B5KGZyb21GaWxlOiBzdHJpbmcsIHRvRGlyOiBzdHJpbmcpOiBQcm9taXNlPENvbnRlbnRzLklNb2RlbD47XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBmaWxlIGFuZCByZXR1cm4gdGhlIHdpZGdldCB1c2VkIHRvIHZpZXcgaXQuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoIC0gVGhlIGZpbGUgcGF0aCB0byBjcmVhdGUuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXROYW1lIC0gVGhlIG5hbWUgb2YgdGhlIHdpZGdldCBmYWN0b3J5IHRvIHVzZS4gJ2RlZmF1bHQnIHdpbGwgdXNlIHRoZSBkZWZhdWx0IHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIGtlcm5lbCAtIEFuIG9wdGlvbmFsIGtlcm5lbCBuYW1lL2lkIHRvIG92ZXJyaWRlIHRoZSBkZWZhdWx0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgY3JlYXRlZCB3aWRnZXQsIG9yIGB1bmRlZmluZWRgLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgZnVuY3Rpb24gd2lsbCByZXR1cm4gYHVuZGVmaW5lZGAgaWYgYSB2YWxpZCB3aWRnZXQgZmFjdG9yeVxuICAgKiBjYW5ub3QgYmUgZm91bmQuXG4gICAqL1xuICBjcmVhdGVOZXcoXG4gICAgcGF0aDogc3RyaW5nLFxuICAgIHdpZGdldE5hbWU/OiBzdHJpbmcsXG4gICAga2VybmVsPzogUGFydGlhbDxLZXJuZWwuSU1vZGVsPlxuICApOiBXaWRnZXQgfCB1bmRlZmluZWQ7XG5cbiAgLyoqXG4gICAqIERlbGV0ZSBhIGZpbGUuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoIC0gVGhlIGZ1bGwgcGF0aCB0byB0aGUgZmlsZSB0byBiZSBkZWxldGVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2Ugd2hpY2ggcmVzb2x2ZXMgd2hlbiB0aGUgZmlsZSBpcyBkZWxldGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIElmIHRoZXJlIGlzIGEgcnVubmluZyBzZXNzaW9uIGFzc29jaWF0ZWQgd2l0aCB0aGUgZmlsZSBhbmQgbm8gb3RoZXJcbiAgICogc2Vzc2lvbnMgYXJlIHVzaW5nIHRoZSBrZXJuZWwsIHRoZSBzZXNzaW9uIHdpbGwgYmUgc2h1dCBkb3duLlxuICAgKi9cbiAgZGVsZXRlRmlsZShwYXRoOiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+O1xuXG4gIC8qKlxuICAgKiBTZWUgaWYgYSB3aWRnZXQgYWxyZWFkeSBleGlzdHMgZm9yIHRoZSBnaXZlbiBwYXRoIGFuZCB3aWRnZXQgbmFtZS5cbiAgICpcbiAgICogQHBhcmFtIHBhdGggLSBUaGUgZmlsZSBwYXRoIHRvIHVzZS5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldE5hbWUgLSBUaGUgbmFtZSBvZiB0aGUgd2lkZ2V0IGZhY3RvcnkgdG8gdXNlLiAnZGVmYXVsdCcgd2lsbCB1c2UgdGhlIGRlZmF1bHQgd2lkZ2V0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgZm91bmQgd2lkZ2V0LCBvciBgdW5kZWZpbmVkYC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGNhbiBiZSB1c2VkIHRvIGZpbmQgYW4gZXhpc3Rpbmcgd2lkZ2V0IGluc3RlYWQgb2Ygb3BlbmluZ1xuICAgKiBhIG5ldyB3aWRnZXQuXG4gICAqL1xuICBmaW5kV2lkZ2V0KFxuICAgIHBhdGg6IHN0cmluZyxcbiAgICB3aWRnZXROYW1lPzogc3RyaW5nIHwgbnVsbFxuICApOiBJRG9jdW1lbnRXaWRnZXQgfCB1bmRlZmluZWQ7XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB1bnRpdGxlZCBmaWxlLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBmaWxlIGNvbnRlbnQgY3JlYXRpb24gb3B0aW9ucy5cbiAgICovXG4gIG5ld1VudGl0bGVkKG9wdGlvbnM6IENvbnRlbnRzLklDcmVhdGVPcHRpb25zKTogUHJvbWlzZTxDb250ZW50cy5JTW9kZWw+O1xuXG4gIC8qKlxuICAgKiBPcGVuIGEgZmlsZSBhbmQgcmV0dXJuIHRoZSB3aWRnZXQgdXNlZCB0byB2aWV3IGl0LlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aCAtIFRoZSBmaWxlIHBhdGggdG8gb3Blbi5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldE5hbWUgLSBUaGUgbmFtZSBvZiB0aGUgd2lkZ2V0IGZhY3RvcnkgdG8gdXNlLiAnZGVmYXVsdCcgd2lsbCB1c2UgdGhlIGRlZmF1bHQgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0ga2VybmVsIC0gQW4gb3B0aW9uYWwga2VybmVsIG5hbWUvaWQgdG8gb3ZlcnJpZGUgdGhlIGRlZmF1bHQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBjcmVhdGVkIHdpZGdldCwgb3IgYHVuZGVmaW5lZGAuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBmdW5jdGlvbiB3aWxsIHJldHVybiBgdW5kZWZpbmVkYCBpZiBhIHZhbGlkIHdpZGdldCBmYWN0b3J5XG4gICAqIGNhbm5vdCBiZSBmb3VuZC5cbiAgICovXG4gIG9wZW4oXG4gICAgcGF0aDogc3RyaW5nLFxuICAgIHdpZGdldE5hbWU/OiBzdHJpbmcsXG4gICAga2VybmVsPzogUGFydGlhbDxLZXJuZWwuSU1vZGVsPixcbiAgICBvcHRpb25zPzogRG9jdW1lbnRSZWdpc3RyeS5JT3Blbk9wdGlvbnNcbiAgKTogSURvY3VtZW50V2lkZ2V0IHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBPcGVuIGEgZmlsZSBhbmQgcmV0dXJuIHRoZSB3aWRnZXQgdXNlZCB0byB2aWV3IGl0LlxuICAgKiBSZXZlYWxzIGFuIGFscmVhZHkgZXhpc3RpbmcgZWRpdG9yLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aCAtIFRoZSBmaWxlIHBhdGggdG8gb3Blbi5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldE5hbWUgLSBUaGUgbmFtZSBvZiB0aGUgd2lkZ2V0IGZhY3RvcnkgdG8gdXNlLiAnZGVmYXVsdCcgd2lsbCB1c2UgdGhlIGRlZmF1bHQgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0ga2VybmVsIC0gQW4gb3B0aW9uYWwga2VybmVsIG5hbWUvaWQgdG8gb3ZlcnJpZGUgdGhlIGRlZmF1bHQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBjcmVhdGVkIHdpZGdldCwgb3IgYHVuZGVmaW5lZGAuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBmdW5jdGlvbiB3aWxsIHJldHVybiBgdW5kZWZpbmVkYCBpZiBhIHZhbGlkIHdpZGdldCBmYWN0b3J5XG4gICAqIGNhbm5vdCBiZSBmb3VuZC5cbiAgICovXG4gIG9wZW5PclJldmVhbChcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgd2lkZ2V0TmFtZT86IHN0cmluZyxcbiAgICBrZXJuZWw/OiBQYXJ0aWFsPEtlcm5lbC5JTW9kZWw+LFxuICAgIG9wdGlvbnM/OiBEb2N1bWVudFJlZ2lzdHJ5LklPcGVuT3B0aW9uc1xuICApOiBJRG9jdW1lbnRXaWRnZXQgfCB1bmRlZmluZWQ7XG5cbiAgLyoqXG4gICAqIE92ZXJ3cml0ZSBhIGZpbGUuXG4gICAqXG4gICAqIEBwYXJhbSBvbGRQYXRoIC0gVGhlIGZ1bGwgcGF0aCB0byB0aGUgb3JpZ2luYWwgZmlsZS5cbiAgICpcbiAgICogQHBhcmFtIG5ld1BhdGggLSBUaGUgZnVsbCBwYXRoIHRvIHRoZSBuZXcgZmlsZS5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIGNvbnRhaW5pbmcgdGhlIG5ldyBmaWxlIGNvbnRlbnRzIG1vZGVsLlxuICAgKi9cbiAgb3ZlcndyaXRlKG9sZFBhdGg6IHN0cmluZywgbmV3UGF0aDogc3RyaW5nKTogUHJvbWlzZTxDb250ZW50cy5JTW9kZWw+O1xuXG4gIC8qKlxuICAgKiBSZW5hbWUgYSBmaWxlIG9yIGRpcmVjdG9yeS5cbiAgICpcbiAgICogQHBhcmFtIG9sZFBhdGggLSBUaGUgZnVsbCBwYXRoIHRvIHRoZSBvcmlnaW5hbCBmaWxlLlxuICAgKlxuICAgKiBAcGFyYW0gbmV3UGF0aCAtIFRoZSBmdWxsIHBhdGggdG8gdGhlIG5ldyBmaWxlLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgY29udGFpbmluZyB0aGUgbmV3IGZpbGUgY29udGVudHMgbW9kZWwuICBUaGUgcHJvbWlzZVxuICAgKiB3aWxsIHJlamVjdCBpZiB0aGUgbmV3UGF0aCBhbHJlYWR5IGV4aXN0cy4gIFVzZSBbW292ZXJ3cml0ZV1dIHRvIG92ZXJ3cml0ZVxuICAgKiBhIGZpbGUuXG4gICAqL1xuICByZW5hbWUob2xkUGF0aDogc3RyaW5nLCBuZXdQYXRoOiBzdHJpbmcpOiBQcm9taXNlPENvbnRlbnRzLklNb2RlbD47XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IERpYWxvZywgc2hvd0RpYWxvZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFRpbWUgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHsgRG9jdW1lbnRSZWdpc3RyeSwgSURvY3VtZW50V2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgQ29udGVudHMgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBBcnJheUV4dCwgZWFjaCwgZmlsdGVyLCBmaW5kLCBtYXAsIHRvQXJyYXkgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBEaXNwb3NhYmxlU2V0LCBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJTWVzc2FnZUhhbmRsZXIsIE1lc3NhZ2UsIE1lc3NhZ2VMb29wIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgQXR0YWNoZWRQcm9wZXJ0eSB9IGZyb20gJ0BsdW1pbm8vcHJvcGVydGllcyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGRvY3VtZW50IHdpZGdldHMuXG4gKi9cbmNvbnN0IERPQ1VNRU5UX0NMQVNTID0gJ2pwLURvY3VtZW50JztcblxuLyoqXG4gKiBBIGNsYXNzIHRoYXQgbWFpbnRhaW5zIHRoZSBsaWZlY3ljbGUgb2YgZmlsZS1iYWNrZWQgd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGNsYXNzIERvY3VtZW50V2lkZ2V0TWFuYWdlciBpbXBsZW1lbnRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBkb2N1bWVudCB3aWRnZXQgbWFuYWdlci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IERvY3VtZW50V2lkZ2V0TWFuYWdlci5JT3B0aW9ucykge1xuICAgIHRoaXMuX3JlZ2lzdHJ5ID0gb3B0aW9ucy5yZWdpc3RyeTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIG9uZSBvZiB0aGUgZG9jdW1lbnRzIGlzIGFjdGl2YXRlZC5cbiAgICovXG4gIGdldCBhY3RpdmF0ZVJlcXVlc3RlZCgpOiBJU2lnbmFsPHRoaXMsIHN0cmluZz4ge1xuICAgIHJldHVybiB0aGlzLl9hY3RpdmF0ZVJlcXVlc3RlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUZXN0IHdoZXRoZXIgdGhlIGRvY3VtZW50IHdpZGdldCBtYW5hZ2VyIGlzIGRpc3Bvc2VkLlxuICAgKi9cbiAgZ2V0IGlzRGlzcG9zZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIHVzZWQgYnkgdGhlIHdpZGdldCBtYW5hZ2VyLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuICAgIFNpZ25hbC5kaXNjb25uZWN0UmVjZWl2ZXIodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgd2lkZ2V0IGZvciBhIGRvY3VtZW50IGFuZCBoYW5kbGUgaXRzIGxpZmVjeWNsZS5cbiAgICpcbiAgICogQHBhcmFtIGZhY3RvcnkgLSBUaGUgd2lkZ2V0IGZhY3RvcnkuXG4gICAqXG4gICAqIEBwYXJhbSBjb250ZXh0IC0gVGhlIGRvY3VtZW50IGNvbnRleHQgb2JqZWN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHdpZGdldCBjcmVhdGVkIGJ5IHRoZSBmYWN0b3J5LlxuICAgKlxuICAgKiBAdGhyb3dzIElmIHRoZSBmYWN0b3J5IGlzIG5vdCByZWdpc3RlcmVkLlxuICAgKi9cbiAgY3JlYXRlV2lkZ2V0KFxuICAgIGZhY3Rvcnk6IERvY3VtZW50UmVnaXN0cnkuV2lkZ2V0RmFjdG9yeSxcbiAgICBjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHRcbiAgKTogSURvY3VtZW50V2lkZ2V0IHtcbiAgICBjb25zdCB3aWRnZXQgPSBmYWN0b3J5LmNyZWF0ZU5ldyhjb250ZXh0KTtcbiAgICB0aGlzLl9pbml0aWFsaXplV2lkZ2V0KHdpZGdldCwgZmFjdG9yeSwgY29udGV4dCk7XG4gICAgcmV0dXJuIHdpZGdldDtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGVuIGEgbmV3IHdpZGdldCBpcyBjcmVhdGVkLCB3ZSBuZWVkIHRvIGhvb2sgaXQgdXBcbiAgICogd2l0aCBzb21lIHNpZ25hbHMsIHVwZGF0ZSB0aGUgd2lkZ2V0IGV4dGVuc2lvbnMgKGZvclxuICAgKiB0aGlzIGtpbmQgb2Ygd2lkZ2V0KSBpbiB0aGUgZG9jcmVnaXN0cnksIGFtb25nXG4gICAqIG90aGVyIHRoaW5ncy5cbiAgICovXG4gIHByaXZhdGUgX2luaXRpYWxpemVXaWRnZXQoXG4gICAgd2lkZ2V0OiBJRG9jdW1lbnRXaWRnZXQsXG4gICAgZmFjdG9yeTogRG9jdW1lbnRSZWdpc3RyeS5XaWRnZXRGYWN0b3J5LFxuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dFxuICApIHtcbiAgICBQcml2YXRlLmZhY3RvcnlQcm9wZXJ0eS5zZXQod2lkZ2V0LCBmYWN0b3J5KTtcbiAgICAvLyBIYW5kbGUgd2lkZ2V0IGV4dGVuc2lvbnMuXG4gICAgY29uc3QgZGlzcG9zYWJsZXMgPSBuZXcgRGlzcG9zYWJsZVNldCgpO1xuICAgIGVhY2godGhpcy5fcmVnaXN0cnkud2lkZ2V0RXh0ZW5zaW9ucyhmYWN0b3J5Lm5hbWUpLCBleHRlbmRlciA9PiB7XG4gICAgICBjb25zdCBkaXNwb3NhYmxlID0gZXh0ZW5kZXIuY3JlYXRlTmV3KHdpZGdldCwgY29udGV4dCk7XG4gICAgICBpZiAoZGlzcG9zYWJsZSkge1xuICAgICAgICBkaXNwb3NhYmxlcy5hZGQoZGlzcG9zYWJsZSk7XG4gICAgICB9XG4gICAgfSk7XG4gICAgUHJpdmF0ZS5kaXNwb3NhYmxlc1Byb3BlcnR5LnNldCh3aWRnZXQsIGRpc3Bvc2FibGVzKTtcbiAgICB3aWRnZXQuZGlzcG9zZWQuY29ubmVjdCh0aGlzLl9vbldpZGdldERpc3Bvc2VkLCB0aGlzKTtcblxuICAgIHRoaXMuYWRvcHRXaWRnZXQoY29udGV4dCwgd2lkZ2V0KTtcbiAgICBjb250ZXh0LmZpbGVDaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25GaWxlQ2hhbmdlZCwgdGhpcyk7XG4gICAgY29udGV4dC5wYXRoQ2hhbmdlZC5jb25uZWN0KHRoaXMuX29uUGF0aENoYW5nZWQsIHRoaXMpO1xuICAgIHZvaWQgY29udGV4dC5yZWFkeS50aGVuKCgpID0+IHtcbiAgICAgIHZvaWQgdGhpcy5zZXRDYXB0aW9uKHdpZGdldCk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSW5zdGFsbCB0aGUgbWVzc2FnZSBob29rIGZvciB0aGUgd2lkZ2V0IGFuZCBhZGQgdG8gbGlzdFxuICAgKiBvZiBrbm93biB3aWRnZXRzLlxuICAgKlxuICAgKiBAcGFyYW0gY29udGV4dCAtIFRoZSBkb2N1bWVudCBjb250ZXh0IG9iamVjdC5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldCAtIFRoZSB3aWRnZXQgdG8gYWRvcHQuXG4gICAqL1xuICBhZG9wdFdpZGdldChcbiAgICBjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQsXG4gICAgd2lkZ2V0OiBJRG9jdW1lbnRXaWRnZXRcbiAgKTogdm9pZCB7XG4gICAgY29uc3Qgd2lkZ2V0cyA9IFByaXZhdGUud2lkZ2V0c1Byb3BlcnR5LmdldChjb250ZXh0KTtcbiAgICB3aWRnZXRzLnB1c2god2lkZ2V0KTtcbiAgICBNZXNzYWdlTG9vcC5pbnN0YWxsTWVzc2FnZUhvb2sod2lkZ2V0LCB0aGlzKTtcbiAgICB3aWRnZXQuYWRkQ2xhc3MoRE9DVU1FTlRfQ0xBU1MpO1xuICAgIHdpZGdldC50aXRsZS5jbG9zYWJsZSA9IHRydWU7XG4gICAgd2lkZ2V0LmRpc3Bvc2VkLmNvbm5lY3QodGhpcy5fd2lkZ2V0RGlzcG9zZWQsIHRoaXMpO1xuICAgIFByaXZhdGUuY29udGV4dFByb3BlcnR5LnNldCh3aWRnZXQsIGNvbnRleHQpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNlZSBpZiBhIHdpZGdldCBhbHJlYWR5IGV4aXN0cyBmb3IgdGhlIGdpdmVuIGNvbnRleHQgYW5kIHdpZGdldCBuYW1lLlxuICAgKlxuICAgKiBAcGFyYW0gY29udGV4dCAtIFRoZSBkb2N1bWVudCBjb250ZXh0IG9iamVjdC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIGZvdW5kIHdpZGdldCwgb3IgYHVuZGVmaW5lZGAuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBjYW4gYmUgdXNlZCB0byB1c2UgYW4gZXhpc3Rpbmcgd2lkZ2V0IGluc3RlYWQgb2Ygb3BlbmluZ1xuICAgKiBhIG5ldyB3aWRnZXQuXG4gICAqL1xuICBmaW5kV2lkZ2V0KFxuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dCxcbiAgICB3aWRnZXROYW1lOiBzdHJpbmdcbiAgKTogSURvY3VtZW50V2lkZ2V0IHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCB3aWRnZXRzID0gUHJpdmF0ZS53aWRnZXRzUHJvcGVydHkuZ2V0KGNvbnRleHQpO1xuICAgIGlmICghd2lkZ2V0cykge1xuICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9XG4gICAgcmV0dXJuIGZpbmQod2lkZ2V0cywgd2lkZ2V0ID0+IHtcbiAgICAgIGNvbnN0IGZhY3RvcnkgPSBQcml2YXRlLmZhY3RvcnlQcm9wZXJ0eS5nZXQod2lkZ2V0KTtcbiAgICAgIGlmICghZmFjdG9yeSkge1xuICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICB9XG4gICAgICByZXR1cm4gZmFjdG9yeS5uYW1lID09PSB3aWRnZXROYW1lO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgZG9jdW1lbnQgY29udGV4dCBmb3IgYSB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgLSBUaGUgd2lkZ2V0IG9mIGludGVyZXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgY29udGV4dCBhc3NvY2lhdGVkIHdpdGggdGhlIHdpZGdldCwgb3IgYHVuZGVmaW5lZGAuXG4gICAqL1xuICBjb250ZXh0Rm9yV2lkZ2V0KHdpZGdldDogV2lkZ2V0KTogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0IHwgdW5kZWZpbmVkIHtcbiAgICByZXR1cm4gUHJpdmF0ZS5jb250ZXh0UHJvcGVydHkuZ2V0KHdpZGdldCk7XG4gIH1cblxuICAvKipcbiAgICogQ2xvbmUgYSB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgLSBUaGUgc291cmNlIHdpZGdldC5cbiAgICpcbiAgICogQHJldHVybnMgQSBuZXcgd2lkZ2V0IG9yIGB1bmRlZmluZWRgLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqICBVc2VzIHRoZSBzYW1lIHdpZGdldCBmYWN0b3J5IGFuZCBjb250ZXh0IGFzIHRoZSBzb3VyY2UsIG9yIHRocm93c1xuICAgKiAgaWYgdGhlIHNvdXJjZSB3aWRnZXQgaXMgbm90IG1hbmFnZWQgYnkgdGhpcyBtYW5hZ2VyLlxuICAgKi9cbiAgY2xvbmVXaWRnZXQod2lkZ2V0OiBXaWRnZXQpOiBJRG9jdW1lbnRXaWRnZXQgfCB1bmRlZmluZWQge1xuICAgIGNvbnN0IGNvbnRleHQgPSBQcml2YXRlLmNvbnRleHRQcm9wZXJ0eS5nZXQod2lkZ2V0KTtcbiAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgIHJldHVybiB1bmRlZmluZWQ7XG4gICAgfVxuICAgIGNvbnN0IGZhY3RvcnkgPSBQcml2YXRlLmZhY3RvcnlQcm9wZXJ0eS5nZXQod2lkZ2V0KTtcbiAgICBpZiAoIWZhY3RvcnkpIHtcbiAgICAgIHJldHVybiB1bmRlZmluZWQ7XG4gICAgfVxuICAgIGNvbnN0IG5ld1dpZGdldCA9IGZhY3RvcnkuY3JlYXRlTmV3KGNvbnRleHQsIHdpZGdldCBhcyBJRG9jdW1lbnRXaWRnZXQpO1xuICAgIHRoaXMuX2luaXRpYWxpemVXaWRnZXQobmV3V2lkZ2V0LCBmYWN0b3J5LCBjb250ZXh0KTtcbiAgICByZXR1cm4gbmV3V2lkZ2V0O1xuICB9XG5cbiAgLyoqXG4gICAqIENsb3NlIHRoZSB3aWRnZXRzIGFzc29jaWF0ZWQgd2l0aCBhIGdpdmVuIGNvbnRleHQuXG4gICAqXG4gICAqIEBwYXJhbSBjb250ZXh0IC0gVGhlIGRvY3VtZW50IGNvbnRleHQgb2JqZWN0LlxuICAgKi9cbiAgY2xvc2VXaWRnZXRzKGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IHdpZGdldHMgPSBQcml2YXRlLndpZGdldHNQcm9wZXJ0eS5nZXQoY29udGV4dCk7XG4gICAgcmV0dXJuIFByb21pc2UuYWxsKFxuICAgICAgdG9BcnJheShtYXAod2lkZ2V0cywgd2lkZ2V0ID0+IHRoaXMub25DbG9zZSh3aWRnZXQpKSlcbiAgICApLnRoZW4oKCkgPT4gdW5kZWZpbmVkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSB3aWRnZXRzIGFzc29jaWF0ZWQgd2l0aCBhIGdpdmVuIGNvbnRleHRcbiAgICogcmVnYXJkbGVzcyBvZiB0aGUgd2lkZ2V0J3MgZGlydHkgc3RhdGUuXG4gICAqXG4gICAqIEBwYXJhbSBjb250ZXh0IC0gVGhlIGRvY3VtZW50IGNvbnRleHQgb2JqZWN0LlxuICAgKi9cbiAgZGVsZXRlV2lkZ2V0cyhjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCB3aWRnZXRzID0gUHJpdmF0ZS53aWRnZXRzUHJvcGVydHkuZ2V0KGNvbnRleHQpO1xuICAgIHJldHVybiBQcm9taXNlLmFsbChcbiAgICAgIHRvQXJyYXkobWFwKHdpZGdldHMsIHdpZGdldCA9PiB0aGlzLm9uRGVsZXRlKHdpZGdldCkpKVxuICAgICkudGhlbigoKSA9PiB1bmRlZmluZWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIEZpbHRlciBhIG1lc3NhZ2Ugc2VudCB0byBhIG1lc3NhZ2UgaGFuZGxlci5cbiAgICpcbiAgICogQHBhcmFtIGhhbmRsZXIgLSBUaGUgdGFyZ2V0IGhhbmRsZXIgb2YgdGhlIG1lc3NhZ2UuXG4gICAqXG4gICAqIEBwYXJhbSBtc2cgLSBUaGUgbWVzc2FnZSBkaXNwYXRjaGVkIHRvIHRoZSBoYW5kbGVyLlxuICAgKlxuICAgKiBAcmV0dXJucyBgZmFsc2VgIGlmIHRoZSBtZXNzYWdlIHNob3VsZCBiZSBmaWx0ZXJlZCwgb2YgYHRydWVgXG4gICAqICAgaWYgdGhlIG1lc3NhZ2Ugc2hvdWxkIGJlIGRpc3BhdGNoZWQgdG8gdGhlIGhhbmRsZXIgYXMgbm9ybWFsLlxuICAgKi9cbiAgbWVzc2FnZUhvb2soaGFuZGxlcjogSU1lc3NhZ2VIYW5kbGVyLCBtc2c6IE1lc3NhZ2UpOiBib29sZWFuIHtcbiAgICBzd2l0Y2ggKG1zZy50eXBlKSB7XG4gICAgICBjYXNlICdjbG9zZS1yZXF1ZXN0JzpcbiAgICAgICAgdm9pZCB0aGlzLm9uQ2xvc2UoaGFuZGxlciBhcyBXaWRnZXQpO1xuICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICBjYXNlICdhY3RpdmF0ZS1yZXF1ZXN0Jzoge1xuICAgICAgICBjb25zdCBjb250ZXh0ID0gdGhpcy5jb250ZXh0Rm9yV2lkZ2V0KGhhbmRsZXIgYXMgV2lkZ2V0KTtcbiAgICAgICAgaWYgKGNvbnRleHQpIHtcbiAgICAgICAgICB0aGlzLl9hY3RpdmF0ZVJlcXVlc3RlZC5lbWl0KGNvbnRleHQucGF0aCk7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBjYXB0aW9uIGZvciB3aWRnZXQgdGl0bGUuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgLSBUaGUgdGFyZ2V0IHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBhc3luYyBzZXRDYXB0aW9uKHdpZGdldDogV2lkZ2V0KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IGNvbnRleHQgPSBQcml2YXRlLmNvbnRleHRQcm9wZXJ0eS5nZXQod2lkZ2V0KTtcbiAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgbW9kZWwgPSBjb250ZXh0LmNvbnRlbnRzTW9kZWw7XG4gICAgaWYgKCFtb2RlbCkge1xuICAgICAgd2lkZ2V0LnRpdGxlLmNhcHRpb24gPSAnJztcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgcmV0dXJuIGNvbnRleHRcbiAgICAgIC5saXN0Q2hlY2twb2ludHMoKVxuICAgICAgLnRoZW4oKGNoZWNrcG9pbnRzOiBDb250ZW50cy5JQ2hlY2twb2ludE1vZGVsW10pID0+IHtcbiAgICAgICAgaWYgKHdpZGdldC5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IGxhc3QgPSBjaGVja3BvaW50c1tjaGVja3BvaW50cy5sZW5ndGggLSAxXTtcbiAgICAgICAgY29uc3QgY2hlY2twb2ludCA9IGxhc3QgPyBUaW1lLmZvcm1hdChsYXN0Lmxhc3RfbW9kaWZpZWQpIDogJ05vbmUnO1xuICAgICAgICBsZXQgY2FwdGlvbiA9IHRyYW5zLl9fKFxuICAgICAgICAgICdOYW1lOiAlMVxcblBhdGg6ICUyXFxuJyxcbiAgICAgICAgICBtb2RlbCEubmFtZSxcbiAgICAgICAgICBtb2RlbCEucGF0aFxuICAgICAgICApO1xuICAgICAgICBpZiAoY29udGV4dCEubW9kZWwucmVhZE9ubHkpIHtcbiAgICAgICAgICBjYXB0aW9uICs9IHRyYW5zLl9fKCdSZWFkLW9ubHknKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBjYXB0aW9uICs9XG4gICAgICAgICAgICB0cmFucy5fXygnTGFzdCBTYXZlZDogJTFcXG4nLCBUaW1lLmZvcm1hdChtb2RlbCEubGFzdF9tb2RpZmllZCkpICtcbiAgICAgICAgICAgIHRyYW5zLl9fKCdMYXN0IENoZWNrcG9pbnQ6ICUxJywgY2hlY2twb2ludCk7XG4gICAgICAgIH1cbiAgICAgICAgd2lkZ2V0LnRpdGxlLmNhcHRpb24gPSBjYXB0aW9uO1xuICAgICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAnY2xvc2UtcmVxdWVzdCdgIG1lc3NhZ2VzLlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gVGhlIHRhcmdldCB3aWRnZXQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdpdGggd2hldGhlciB0aGUgd2lkZ2V0IHdhcyBjbG9zZWQuXG4gICAqL1xuICBwcm90ZWN0ZWQgYXN5bmMgb25DbG9zZSh3aWRnZXQ6IFdpZGdldCk6IFByb21pc2U8Ym9vbGVhbj4ge1xuICAgIC8vIEhhbmRsZSBkaXJ0eSBzdGF0ZS5cbiAgICBjb25zdCBbc2hvdWxkQ2xvc2UsIGlnbm9yZVNhdmVdID0gYXdhaXQgdGhpcy5fbWF5YmVDbG9zZShcbiAgICAgIHdpZGdldCxcbiAgICAgIHRoaXMudHJhbnNsYXRvclxuICAgICk7XG4gICAgaWYgKHdpZGdldC5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKHNob3VsZENsb3NlKSB7XG4gICAgICBpZiAoIWlnbm9yZVNhdmUpIHtcbiAgICAgICAgY29uc3QgY29udGV4dCA9IFByaXZhdGUuY29udGV4dFByb3BlcnR5LmdldCh3aWRnZXQpO1xuICAgICAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoY29udGV4dC5jb250ZW50c01vZGVsPy53cml0YWJsZSkge1xuICAgICAgICAgIGF3YWl0IGNvbnRleHQuc2F2ZSgpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGF3YWl0IGNvbnRleHQuc2F2ZUFzKCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIGlmICh3aWRnZXQuaXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIHdpZGdldC5kaXNwb3NlKCk7XG4gICAgfVxuICAgIHJldHVybiBzaG91bGRDbG9zZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHdpZGdldCByZWdhcmRsZXNzIG9mIHdpZGdldCdzIGRpcnR5IHN0YXRlLlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gVGhlIHRhcmdldCB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25EZWxldGUod2lkZ2V0OiBXaWRnZXQpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICB3aWRnZXQuZGlzcG9zZSgpO1xuICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUodm9pZCAwKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBc2sgdGhlIHVzZXIgd2hldGhlciB0byBjbG9zZSBhbiB1bnNhdmVkIGZpbGUuXG4gICAqL1xuICBwcml2YXRlIF9tYXliZUNsb3NlKFxuICAgIHdpZGdldDogV2lkZ2V0LFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApOiBQcm9taXNlPFtib29sZWFuLCBib29sZWFuXT4ge1xuICAgIHRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgLy8gQmFpbCBpZiB0aGUgbW9kZWwgaXMgbm90IGRpcnR5IG9yIG90aGVyIHdpZGdldHMgYXJlIHVzaW5nIHRoZSBtb2RlbC4pXG4gICAgY29uc3QgY29udGV4dCA9IFByaXZhdGUuY29udGV4dFByb3BlcnR5LmdldCh3aWRnZXQpO1xuICAgIGlmICghY29udGV4dCkge1xuICAgICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZShbdHJ1ZSwgdHJ1ZV0pO1xuICAgIH1cbiAgICBsZXQgd2lkZ2V0cyA9IFByaXZhdGUud2lkZ2V0c1Byb3BlcnR5LmdldChjb250ZXh0KTtcbiAgICBpZiAoIXdpZGdldHMpIHtcbiAgICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUoW3RydWUsIHRydWVdKTtcbiAgICB9XG4gICAgLy8gRmlsdGVyIGJ5IHdoZXRoZXIgdGhlIGZhY3RvcmllcyBhcmUgcmVhZCBvbmx5LlxuICAgIHdpZGdldHMgPSB0b0FycmF5KFxuICAgICAgZmlsdGVyKHdpZGdldHMsIHdpZGdldCA9PiB7XG4gICAgICAgIGNvbnN0IGZhY3RvcnkgPSBQcml2YXRlLmZhY3RvcnlQcm9wZXJ0eS5nZXQod2lkZ2V0KTtcbiAgICAgICAgaWYgKCFmYWN0b3J5KSB7XG4gICAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBmYWN0b3J5LnJlYWRPbmx5ID09PSBmYWxzZTtcbiAgICAgIH0pXG4gICAgKTtcbiAgICBjb25zdCBmYWN0b3J5ID0gUHJpdmF0ZS5mYWN0b3J5UHJvcGVydHkuZ2V0KHdpZGdldCk7XG4gICAgaWYgKCFmYWN0b3J5KSB7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKFt0cnVlLCB0cnVlXSk7XG4gICAgfVxuICAgIGNvbnN0IG1vZGVsID0gY29udGV4dC5tb2RlbDtcbiAgICBpZiAoIW1vZGVsLmRpcnR5IHx8IHdpZGdldHMubGVuZ3RoID4gMSB8fCBmYWN0b3J5LnJlYWRPbmx5KSB7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKFt0cnVlLCB0cnVlXSk7XG4gICAgfVxuICAgIGNvbnN0IGZpbGVOYW1lID0gd2lkZ2V0LnRpdGxlLmxhYmVsO1xuICAgIGNvbnN0IHNhdmVMYWJlbCA9IGNvbnRleHQuY29udGVudHNNb2RlbD8ud3JpdGFibGVcbiAgICAgID8gdHJhbnMuX18oJ1NhdmUnKVxuICAgICAgOiB0cmFucy5fXygnU2F2ZSBhcycpO1xuICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgIHRpdGxlOiB0cmFucy5fXygnU2F2ZSB5b3VyIHdvcmsnKSxcbiAgICAgIGJvZHk6IHRyYW5zLl9fKCdTYXZlIGNoYW5nZXMgaW4gXCIlMVwiIGJlZm9yZSBjbG9zaW5nPycsIGZpbGVOYW1lKSxcbiAgICAgIGJ1dHRvbnM6IFtcbiAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnQ2FuY2VsJykgfSksXG4gICAgICAgIERpYWxvZy53YXJuQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdEaXNjYXJkJykgfSksXG4gICAgICAgIERpYWxvZy5va0J1dHRvbih7IGxhYmVsOiBzYXZlTGFiZWwgfSlcbiAgICAgIF1cbiAgICB9KS50aGVuKHJlc3VsdCA9PiB7XG4gICAgICByZXR1cm4gW3Jlc3VsdC5idXR0b24uYWNjZXB0LCByZXN1bHQuYnV0dG9uLmRpc3BsYXlUeXBlID09PSAnd2FybiddO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgZGlzcG9zYWwgb2YgYSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF93aWRnZXREaXNwb3NlZCh3aWRnZXQ6IFdpZGdldCk6IHZvaWQge1xuICAgIGNvbnN0IGNvbnRleHQgPSBQcml2YXRlLmNvbnRleHRQcm9wZXJ0eS5nZXQod2lkZ2V0KTtcbiAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3Qgd2lkZ2V0cyA9IFByaXZhdGUud2lkZ2V0c1Byb3BlcnR5LmdldChjb250ZXh0KTtcbiAgICBpZiAoIXdpZGdldHMpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgLy8gUmVtb3ZlIHRoZSB3aWRnZXQuXG4gICAgQXJyYXlFeHQucmVtb3ZlRmlyc3RPZih3aWRnZXRzLCB3aWRnZXQpO1xuICAgIC8vIERpc3Bvc2Ugb2YgdGhlIGNvbnRleHQgaWYgdGhpcyBpcyB0aGUgbGFzdCB3aWRnZXQgdXNpbmcgaXQuXG4gICAgaWYgKCF3aWRnZXRzLmxlbmd0aCkge1xuICAgICAgY29udGV4dC5kaXNwb3NlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgZGlzcG9zYWwgb2YgYSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9vbldpZGdldERpc3Bvc2VkKHdpZGdldDogV2lkZ2V0KTogdm9pZCB7XG4gICAgY29uc3QgZGlzcG9zYWJsZXMgPSBQcml2YXRlLmRpc3Bvc2FibGVzUHJvcGVydHkuZ2V0KHdpZGdldCk7XG4gICAgZGlzcG9zYWJsZXMuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGZpbGUgY2hhbmdlZCBzaWduYWwgZm9yIGEgY29udGV4dC5cbiAgICovXG4gIHByaXZhdGUgX29uRmlsZUNoYW5nZWQoY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0KTogdm9pZCB7XG4gICAgY29uc3Qgd2lkZ2V0cyA9IFByaXZhdGUud2lkZ2V0c1Byb3BlcnR5LmdldChjb250ZXh0KTtcbiAgICBlYWNoKHdpZGdldHMsIHdpZGdldCA9PiB7XG4gICAgICB2b2lkIHRoaXMuc2V0Q2FwdGlvbih3aWRnZXQpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIHBhdGggY2hhbmdlZCBzaWduYWwgZm9yIGEgY29udGV4dC5cbiAgICovXG4gIHByaXZhdGUgX29uUGF0aENoYW5nZWQoY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0KTogdm9pZCB7XG4gICAgY29uc3Qgd2lkZ2V0cyA9IFByaXZhdGUud2lkZ2V0c1Byb3BlcnR5LmdldChjb250ZXh0KTtcbiAgICBlYWNoKHdpZGdldHMsIHdpZGdldCA9PiB7XG4gICAgICB2b2lkIHRoaXMuc2V0Q2FwdGlvbih3aWRnZXQpO1xuICAgIH0pO1xuICB9XG5cbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF9yZWdpc3RyeTogRG9jdW1lbnRSZWdpc3RyeTtcbiAgcHJpdmF0ZSBfYWN0aXZhdGVSZXF1ZXN0ZWQgPSBuZXcgU2lnbmFsPHRoaXMsIHN0cmluZz4odGhpcyk7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgZG9jdW1lbnQgd2lkZ2V0IG1hbmFnZXIgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBEb2N1bWVudFdpZGdldE1hbmFnZXIge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBpbml0aWFsaXplIGEgZG9jdW1lbnQgd2lkZ2V0IG1hbmFnZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBBIGRvY3VtZW50IHJlZ2lzdHJ5IGluc3RhbmNlLlxuICAgICAqL1xuICAgIHJlZ2lzdHJ5OiBEb2N1bWVudFJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFwcGxpY2F0aW9uIGxhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICB9XG59XG5cbi8qKlxuICogQSBwcml2YXRlIG5hbWVzcGFjZSBmb3IgRG9jdW1lbnRNYW5hZ2VyIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIEEgcHJpdmF0ZSBhdHRhY2hlZCBwcm9wZXJ0eSBmb3IgYSB3aWRnZXQgY29udGV4dC5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBjb250ZXh0UHJvcGVydHkgPSBuZXcgQXR0YWNoZWRQcm9wZXJ0eTxcbiAgICBXaWRnZXQsXG4gICAgRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0IHwgdW5kZWZpbmVkXG4gID4oe1xuICAgIG5hbWU6ICdjb250ZXh0JyxcbiAgICBjcmVhdGU6ICgpID0+IHVuZGVmaW5lZFxuICB9KTtcblxuICAvKipcbiAgICogQSBwcml2YXRlIGF0dGFjaGVkIHByb3BlcnR5IGZvciBhIHdpZGdldCBmYWN0b3J5LlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGZhY3RvcnlQcm9wZXJ0eSA9IG5ldyBBdHRhY2hlZFByb3BlcnR5PFxuICAgIFdpZGdldCxcbiAgICBEb2N1bWVudFJlZ2lzdHJ5LldpZGdldEZhY3RvcnkgfCB1bmRlZmluZWRcbiAgPih7XG4gICAgbmFtZTogJ2ZhY3RvcnknLFxuICAgIGNyZWF0ZTogKCkgPT4gdW5kZWZpbmVkXG4gIH0pO1xuXG4gIC8qKlxuICAgKiBBIHByaXZhdGUgYXR0YWNoZWQgcHJvcGVydHkgZm9yIHRoZSB3aWRnZXRzIGFzc29jaWF0ZWQgd2l0aCBhIGNvbnRleHQuXG4gICAqL1xuICBleHBvcnQgY29uc3Qgd2lkZ2V0c1Byb3BlcnR5ID0gbmV3IEF0dGFjaGVkUHJvcGVydHk8XG4gICAgRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0LFxuICAgIElEb2N1bWVudFdpZGdldFtdXG4gID4oe1xuICAgIG5hbWU6ICd3aWRnZXRzJyxcbiAgICBjcmVhdGU6ICgpID0+IFtdXG4gIH0pO1xuXG4gIC8qKlxuICAgKiBBIHByaXZhdGUgYXR0YWNoZWQgcHJvcGVydHkgZm9yIGEgd2lkZ2V0J3MgZGlzcG9zYWJsZXMuXG4gICAqL1xuICBleHBvcnQgY29uc3QgZGlzcG9zYWJsZXNQcm9wZXJ0eSA9IG5ldyBBdHRhY2hlZFByb3BlcnR5PFxuICAgIFdpZGdldCxcbiAgICBEaXNwb3NhYmxlU2V0XG4gID4oe1xuICAgIG5hbWU6ICdkaXNwb3NhYmxlcycsXG4gICAgY3JlYXRlOiAoKSA9PiBuZXcgRGlzcG9zYWJsZVNldCgpXG4gIH0pO1xufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==