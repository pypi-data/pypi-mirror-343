(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_codeeditor_lib_index_js"],{

/***/ "../packages/codeeditor/lib/editor.js":
/*!********************************************!*\
  !*** ../packages/codeeditor/lib/editor.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeEditor": () => (/* binding */ CodeEditor)
/* harmony export */ });
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_shared_models__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/shared-models */ "webpack/sharing/consume/default/@jupyterlab/shared-models/@jupyterlab/shared-models");
/* harmony import */ var _jupyterlab_shared_models__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_shared_models__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



const globalModelDBMutex = _jupyterlab_shared_models__WEBPACK_IMPORTED_MODULE_1__.createMutex();
/**
 * A namespace for code editors.
 *
 * #### Notes
 * - A code editor is a set of common assumptions which hold for all concrete editors.
 * - Changes in implementations of the code editor should only be caused by changes in concrete editors.
 * - Common JLab services which are based on the code editor should belong to `IEditorServices`.
 */
var CodeEditor;
(function (CodeEditor) {
    /**
     * The default selection style.
     */
    CodeEditor.defaultSelectionStyle = {
        className: '',
        displayName: '',
        color: 'black'
    };
    /**
     * The default implementation of the editor model.
     */
    class Model {
        /**
         * Construct a new Model.
         */
        constructor(options) {
            this._isDisposed = false;
            this._mimeTypeChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
            this._sharedModelSwitched = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
            options = options || {};
            if (options.modelDB) {
                this.modelDB = options.modelDB;
            }
            else {
                this.modelDB = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ModelDB();
            }
            this.sharedModel = _jupyterlab_shared_models__WEBPACK_IMPORTED_MODULE_1__.createStandaloneCell(this.type, options.id);
            this.sharedModel.changed.connect(this._onSharedModelChanged, this);
            const value = this.modelDB.createString('value');
            value.changed.connect(this._onModelDBValueChanged, this);
            value.text = value.text || options.value || '';
            const mimeType = this.modelDB.createValue('mimeType');
            mimeType.changed.connect(this._onModelDBMimeTypeChanged, this);
            mimeType.set(options.mimeType || 'text/plain');
            this.modelDB.createMap('selections');
        }
        /**
         * When we initialize a cell model, we create a standalone model that cannot be shared in a YNotebook.
         * Call this function to re-initialize the local representation based on a fresh shared model (e.g. models.YFile or models.YCodeCell).
         *
         * @param sharedModel
         * @param reinitialize Whether to reinitialize the shared model.
         */
        switchSharedModel(sharedModel, reinitialize) {
            if (reinitialize) {
                // update local modeldb
                // @todo also change metadata
                this.value.text = sharedModel.getSource();
            }
            this.sharedModel.changed.disconnect(this._onSharedModelChanged, this);
            // clone model retrieve a shared (not standalone) model
            this.sharedModel = sharedModel;
            this.sharedModel.changed.connect(this._onSharedModelChanged, this);
            this._sharedModelSwitched.emit(true);
        }
        /**
         * We update the modeldb store when the shared model changes.
         * To ensure that we don't run into infinite loops, we wrap this call in a "mutex".
         * The "mutex" ensures that the wrapped code can only be executed by either the sharedModelChanged handler
         * or the modelDB change handler.
         */
        _onSharedModelChanged(sender, change) {
            globalModelDBMutex(() => {
                if (change.sourceChange) {
                    const value = this.modelDB.get('value');
                    let currpos = 0;
                    change.sourceChange.forEach(delta => {
                        if (delta.insert != null) {
                            value.insert(currpos, delta.insert);
                            currpos += delta.insert.length;
                        }
                        else if (delta.delete != null) {
                            value.remove(currpos, currpos + delta.delete);
                        }
                        else if (delta.retain != null) {
                            currpos += delta.retain;
                        }
                    });
                }
            });
        }
        /**
         * Handle a change to the modelDB value.
         */
        _onModelDBValueChanged(value, event) {
            globalModelDBMutex(() => {
                this.sharedModel.transact(() => {
                    switch (event.type) {
                        case 'insert':
                            this.sharedModel.updateSource(event.start, event.start, event.value);
                            break;
                        case 'remove':
                            this.sharedModel.updateSource(event.start, event.end);
                            break;
                        default:
                            this.sharedModel.setSource(value.text);
                            break;
                    }
                });
            });
        }
        get type() {
            return 'code';
        }
        /**
         * A signal emitted when a mimetype changes.
         */
        get mimeTypeChanged() {
            return this._mimeTypeChanged;
        }
        /**
         * A signal emitted when the shared model was switched.
         */
        get sharedModelSwitched() {
            return this._sharedModelSwitched;
        }
        /**
         * Get the value of the model.
         */
        get value() {
            return this.modelDB.get('value');
        }
        /**
         * Get the selections for the model.
         */
        get selections() {
            return this.modelDB.get('selections');
        }
        /**
         * A mime type of the model.
         */
        get mimeType() {
            return this.modelDB.getValue('mimeType');
        }
        set mimeType(newValue) {
            const oldValue = this.mimeType;
            if (oldValue === newValue) {
                return;
            }
            this.modelDB.setValue('mimeType', newValue);
        }
        /**
         * Whether the model is disposed.
         */
        get isDisposed() {
            return this._isDisposed;
        }
        /**
         * Dispose of the resources used by the model.
         */
        dispose() {
            if (this._isDisposed) {
                return;
            }
            this._isDisposed = true;
            _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
        }
        _onModelDBMimeTypeChanged(mimeType, args) {
            this._mimeTypeChanged.emit({
                name: 'mimeType',
                oldValue: args.oldValue,
                newValue: args.newValue
            });
        }
    }
    CodeEditor.Model = Model;
    /**
     * The default configuration options for an editor.
     */
    CodeEditor.defaultConfig = {
        cursorBlinkRate: 530,
        fontFamily: null,
        fontSize: null,
        lineHeight: null,
        lineNumbers: false,
        lineWrap: 'on',
        wordWrapColumn: 80,
        readOnly: false,
        tabSize: 4,
        insertSpaces: true,
        matchBrackets: true,
        autoClosingBrackets: false,
        handlePaste: true,
        rulers: [],
        codeFolding: false,
        showTrailingSpace: false
    };
})(CodeEditor || (CodeEditor = {}));


/***/ }),

/***/ "../packages/codeeditor/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/codeeditor/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeEditor": () => (/* reexport safe */ _editor__WEBPACK_IMPORTED_MODULE_0__.CodeEditor),
/* harmony export */   "JSONEditor": () => (/* reexport safe */ _jsoneditor__WEBPACK_IMPORTED_MODULE_1__.JSONEditor),
/* harmony export */   "CodeEditorWrapper": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.CodeEditorWrapper),
/* harmony export */   "IEditorMimeTypeService": () => (/* reexport safe */ _mimetype__WEBPACK_IMPORTED_MODULE_3__.IEditorMimeTypeService),
/* harmony export */   "IEditorServices": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.IEditorServices)
/* harmony export */ });
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./editor */ "../packages/codeeditor/lib/editor.js");
/* harmony import */ var _jsoneditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./jsoneditor */ "../packages/codeeditor/lib/jsoneditor.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "../packages/codeeditor/lib/widget.js");
/* harmony import */ var _mimetype__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./mimetype */ "../packages/codeeditor/lib/mimetype.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tokens */ "../packages/codeeditor/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module codeeditor
 */








/***/ }),

/***/ "../packages/codeeditor/lib/jsoneditor.js":
/*!************************************************!*\
  !*** ../packages/codeeditor/lib/jsoneditor.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JSONEditor": () => (/* binding */ JSONEditor)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./editor */ "../packages/codeeditor/lib/editor.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The class name added to a JSONEditor instance.
 */
const JSONEDITOR_CLASS = 'jp-JSONEditor';
/**
 * The class name added when the Metadata editor contains invalid JSON.
 */
const ERROR_CLASS = 'jp-mod-error';
/**
 * The class name added to the editor host node.
 */
const HOST_CLASS = 'jp-JSONEditor-host';
/**
 * The class name added to the header area.
 */
const HEADER_CLASS = 'jp-JSONEditor-header';
/**
 * A widget for editing observable JSON.
 */
class JSONEditor extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    /**
     * Construct a new JSON editor.
     */
    constructor(options) {
        super();
        this._dataDirty = false;
        this._inputDirty = false;
        this._source = null;
        this._originalValue = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.emptyObject;
        this._changeGuard = false;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.addClass(JSONEDITOR_CLASS);
        this.headerNode = document.createElement('div');
        this.headerNode.className = HEADER_CLASS;
        this.revertButtonNode = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.undoIcon.element({
            tag: 'span',
            title: this._trans.__('Revert changes to data')
        });
        this.commitButtonNode = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.checkIcon.element({
            tag: 'span',
            title: this._trans.__('Commit changes to data'),
            marginLeft: '8px'
        });
        this.editorHostNode = document.createElement('div');
        this.editorHostNode.className = HOST_CLASS;
        this.headerNode.appendChild(this.revertButtonNode);
        this.headerNode.appendChild(this.commitButtonNode);
        this.node.appendChild(this.headerNode);
        this.node.appendChild(this.editorHostNode);
        const model = new _editor__WEBPACK_IMPORTED_MODULE_4__.CodeEditor.Model();
        model.value.text = this._trans.__('No data!');
        model.mimeType = 'application/json';
        model.value.changed.connect(this._onValueChanged, this);
        this.model = model;
        this.editor = options.editorFactory({ host: this.editorHostNode, model });
        this.editor.setOption('readOnly', true);
    }
    /**
     * The observable source.
     */
    get source() {
        return this._source;
    }
    set source(value) {
        if (this._source === value) {
            return;
        }
        if (this._source) {
            this._source.changed.disconnect(this._onSourceChanged, this);
        }
        this._source = value;
        this.editor.setOption('readOnly', value === null);
        if (value) {
            value.changed.connect(this._onSourceChanged, this);
        }
        this._setValue();
    }
    /**
     * Get whether the editor is dirty.
     */
    get isDirty() {
        return this._dataDirty || this._inputDirty;
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'blur':
                this._evtBlur(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        const node = this.editorHostNode;
        node.addEventListener('blur', this, true);
        node.addEventListener('click', this, true);
        this.revertButtonNode.hidden = true;
        this.commitButtonNode.hidden = true;
        this.headerNode.addEventListener('click', this);
        if (this.isVisible) {
            this.update();
        }
    }
    /**
     * Handle `after-show` messages for the widget.
     */
    onAfterShow(msg) {
        this.update();
    }
    /**
     * Handle `update-request` messages for the widget.
     */
    onUpdateRequest(msg) {
        this.editor.refresh();
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.editorHostNode;
        node.removeEventListener('blur', this, true);
        node.removeEventListener('click', this, true);
        this.headerNode.removeEventListener('click', this);
    }
    /**
     * Handle a change to the metadata of the source.
     */
    _onSourceChanged(sender, args) {
        if (this._changeGuard) {
            return;
        }
        if (this._inputDirty || this.editor.hasFocus()) {
            this._dataDirty = true;
            return;
        }
        this._setValue();
    }
    /**
     * Handle change events.
     */
    _onValueChanged() {
        let valid = true;
        try {
            const value = JSON.parse(this.editor.model.value.text);
            this.removeClass(ERROR_CLASS);
            this._inputDirty =
                !this._changeGuard && !_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(value, this._originalValue);
        }
        catch (err) {
            this.addClass(ERROR_CLASS);
            this._inputDirty = true;
            valid = false;
        }
        this.revertButtonNode.hidden = !this._inputDirty;
        this.commitButtonNode.hidden = !valid || !this._inputDirty;
    }
    /**
     * Handle blur events for the text area.
     */
    _evtBlur(event) {
        // Update the metadata if necessary.
        if (!this._inputDirty && this._dataDirty) {
            this._setValue();
        }
    }
    /**
     * Handle click events for the buttons.
     */
    _evtClick(event) {
        const target = event.target;
        if (this.revertButtonNode.contains(target)) {
            this._setValue();
        }
        else if (this.commitButtonNode.contains(target)) {
            if (!this.commitButtonNode.hidden && !this.hasClass(ERROR_CLASS)) {
                this._changeGuard = true;
                this._mergeContent();
                this._changeGuard = false;
                this._setValue();
            }
        }
        else if (this.editorHostNode.contains(target)) {
            this.editor.focus();
        }
    }
    /**
     * Merge the user content.
     */
    _mergeContent() {
        const model = this.editor.model;
        const old = this._originalValue;
        const user = JSON.parse(model.value.text);
        const source = this.source;
        if (!source) {
            return;
        }
        // If it is in user and has changed from old, set in new.
        for (const key in user) {
            if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(user[key], old[key] || null)) {
                source.set(key, user[key]);
            }
        }
        // If it was in old and is not in user, remove from source.
        for (const key in old) {
            if (!(key in user)) {
                source.delete(key);
            }
        }
    }
    /**
     * Set the value given the owner contents.
     */
    _setValue() {
        this._dataDirty = false;
        this._inputDirty = false;
        this.revertButtonNode.hidden = true;
        this.commitButtonNode.hidden = true;
        this.removeClass(ERROR_CLASS);
        const model = this.editor.model;
        const content = this._source ? this._source.toJSON() : {};
        this._changeGuard = true;
        if (content === void 0) {
            model.value.text = this._trans.__('No data!');
            this._originalValue = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.emptyObject;
        }
        else {
            const value = JSON.stringify(content, null, 4);
            model.value.text = value;
            this._originalValue = content;
            // Move the cursor to within the brace.
            if (value.length > 1 && value[0] === '{') {
                this.editor.setCursorPosition({ line: 0, column: 1 });
            }
        }
        this.editor.refresh();
        this._changeGuard = false;
        this.commitButtonNode.hidden = true;
        this.revertButtonNode.hidden = true;
    }
}


/***/ }),

/***/ "../packages/codeeditor/lib/mimetype.js":
/*!**********************************************!*\
  !*** ../packages/codeeditor/lib/mimetype.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IEditorMimeTypeService": () => (/* binding */ IEditorMimeTypeService)
/* harmony export */ });
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * A namespace for `IEditorMimeTypeService`.
 */
var IEditorMimeTypeService;
(function (IEditorMimeTypeService) {
    /**
     * The default mime type.
     */
    IEditorMimeTypeService.defaultMimeType = 'text/plain';
})(IEditorMimeTypeService || (IEditorMimeTypeService = {}));


/***/ }),

/***/ "../packages/codeeditor/lib/tokens.js":
/*!********************************************!*\
  !*** ../packages/codeeditor/lib/tokens.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IEditorServices": () => (/* binding */ IEditorServices)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * Code editor services token.
 */
const IEditorServices = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/codeeditor:IEditorServices');


/***/ }),

/***/ "../packages/codeeditor/lib/widget.js":
/*!********************************************!*\
  !*** ../packages/codeeditor/lib/widget.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeEditorWrapper": () => (/* binding */ CodeEditorWrapper)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The class name added to an editor widget that has a primary selection.
 */
const HAS_SELECTION_CLASS = 'jp-mod-has-primary-selection';
/**
 * The class name added to an editor widget that has a cursor/selection
 * within the whitespace at the beginning of a line
 */
const HAS_IN_LEADING_WHITESPACE_CLASS = 'jp-mod-in-leading-whitespace';
/**
 * A class used to indicate a drop target.
 */
const DROP_TARGET_CLASS = 'jp-mod-dropTarget';
/**
 * RegExp to test for leading whitespace
 */
const leadingWhitespaceRe = /^\s+$/;
/**
 * A widget which hosts a code editor.
 */
class CodeEditorWrapper extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Construct a new code editor widget.
     */
    constructor(options) {
        super();
        this._hasRefreshedSinceAttach = false;
        const editor = (this.editor = options.factory({
            host: this.node,
            model: options.model,
            uuid: options.uuid,
            config: options.config,
            selectionStyle: options.selectionStyle
        }));
        editor.model.selections.changed.connect(this._onSelectionsChanged, this);
        this._updateOnShow = options.updateOnShow !== false;
    }
    /**
     * Get the model used by the widget.
     */
    get model() {
        return this.editor.model;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        this.editor.dispose();
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'lm-dragenter':
                this._evtDragEnter(event);
                break;
            case 'lm-dragleave':
                this._evtDragLeave(event);
                break;
            case 'lm-dragover':
                this._evtDragOver(event);
                break;
            case 'lm-drop':
                this._evtDrop(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.editor.focus();
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        const node = this.node;
        node.addEventListener('lm-dragenter', this);
        node.addEventListener('lm-dragleave', this);
        node.addEventListener('lm-dragover', this);
        node.addEventListener('lm-drop', this);
        // We have to refresh at least once after attaching,
        // while visible.
        this._hasRefreshedSinceAttach = false;
        if (this.isVisible) {
            this.update();
        }
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.node;
        node.removeEventListener('lm-dragenter', this);
        node.removeEventListener('lm-dragleave', this);
        node.removeEventListener('lm-dragover', this);
        node.removeEventListener('lm-drop', this);
    }
    /**
     * A message handler invoked on an `'after-show'` message.
     */
    onAfterShow(msg) {
        if (this._updateOnShow || !this._hasRefreshedSinceAttach) {
            this.update();
        }
    }
    /**
     * A message handler invoked on a `'resize'` message.
     */
    onResize(msg) {
        if (msg.width >= 0 && msg.height >= 0) {
            this.editor.setSize(msg);
        }
        else if (this.isVisible) {
            this.editor.resizeToFit();
        }
    }
    /**
     * A message handler invoked on an `'update-request'` message.
     */
    onUpdateRequest(msg) {
        if (this.isVisible) {
            this._hasRefreshedSinceAttach = true;
            this.editor.refresh();
        }
    }
    /**
     * Handle a change in model selections.
     */
    _onSelectionsChanged() {
        const { start, end } = this.editor.getSelection();
        if (start.column !== end.column || start.line !== end.line) {
            // a selection was made
            this.addClass(HAS_SELECTION_CLASS);
            this.removeClass(HAS_IN_LEADING_WHITESPACE_CLASS);
        }
        else {
            // the cursor was placed
            this.removeClass(HAS_SELECTION_CLASS);
            if (this.editor
                .getLine(end.line)
                .slice(0, end.column)
                .match(leadingWhitespaceRe)) {
                this.addClass(HAS_IN_LEADING_WHITESPACE_CLASS);
            }
            else {
                this.removeClass(HAS_IN_LEADING_WHITESPACE_CLASS);
            }
        }
    }
    /**
     * Handle the `'lm-dragenter'` event for the widget.
     */
    _evtDragEnter(event) {
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        this.addClass('jp-mod-dropTarget');
    }
    /**
     * Handle the `'lm-dragleave'` event for the widget.
     */
    _evtDragLeave(event) {
        this.removeClass(DROP_TARGET_CLASS);
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
    }
    /**
     * Handle the `'lm-dragover'` event for the widget.
     */
    _evtDragOver(event) {
        this.removeClass(DROP_TARGET_CLASS);
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = 'copy';
        this.addClass(DROP_TARGET_CLASS);
    }
    /**
     * Handle the `'lm-drop'` event for the widget.
     */
    _evtDrop(event) {
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        const coordinate = {
            top: event.y,
            bottom: event.y,
            left: event.x,
            right: event.x,
            x: event.x,
            y: event.y,
            width: 0,
            height: 0
        };
        const position = this.editor.getPositionForCoordinate(coordinate);
        if (position === null) {
            return;
        }
        this.removeClass(DROP_TARGET_CLASS);
        event.preventDefault();
        event.stopPropagation();
        if (event.proposedAction === 'none') {
            event.dropAction = 'none';
            return;
        }
        const offset = this.editor.getOffsetAt(position);
        this.model.value.insert(offset, data);
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Given a MimeData instance, extract the first text data, if any.
     */
    function findTextData(mime) {
        const types = mime.types();
        const textType = types.find(t => t.indexOf('text') === 0);
        if (textType === undefined) {
            return undefined;
        }
        return mime.getData(textType);
    }
    Private.findTextData = findTextData;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29kZWVkaXRvci9zcmMvZWRpdG9yLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb2RlZWRpdG9yL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29kZWVkaXRvci9zcmMvanNvbmVkaXRvci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29kZWVkaXRvci9zcmMvbWltZXR5cGUudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvZGVlZGl0b3Ivc3JjL3Rva2Vucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29kZWVkaXRvci9zcmMvd2lkZ2V0LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBVzFCO0FBQ21CO0FBSUE7QUFFcEQsTUFBTSxrQkFBa0IsR0FBRyxrRUFBa0IsRUFBRSxDQUFDO0FBRWhEOzs7Ozs7O0dBT0c7QUFDSSxJQUFVLFVBQVUsQ0FtMUIxQjtBQW4xQkQsV0FBaUIsVUFBVTtJQStFekI7O09BRUc7SUFDVSxnQ0FBcUIsR0FBb0I7UUFDcEQsU0FBUyxFQUFFLEVBQUU7UUFDYixXQUFXLEVBQUUsRUFBRTtRQUNmLEtBQUssRUFBRSxPQUFPO0tBQ2YsQ0FBQztJQTJHRjs7T0FFRztJQUNILE1BQWEsS0FBSztRQUNoQjs7V0FFRztRQUNILFlBQVksT0FBd0I7WUE4TDVCLGdCQUFXLEdBQUcsS0FBSyxDQUFDO1lBQ3BCLHFCQUFnQixHQUFHLElBQUkscURBQU0sQ0FBNkIsSUFBSSxD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Q0FBQyxFQVpTLE9BQU8sS0FBUCxPQUFPLFFBWWhCIiwiZmlsZSI6InBhY2thZ2VzX2NvZGVlZGl0b3JfbGliX2luZGV4X2pzLmVkNWEwZmMxYWRmZjAwMDUxMGVhLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJQ2hhbmdlZEFyZ3MgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0ICogYXMgbmJmb3JtYXQgZnJvbSAnQGp1cHl0ZXJsYWIvbmJmb3JtYXQnO1xuaW1wb3J0IHtcbiAgSU1vZGVsREIsXG4gIElPYnNlcnZhYmxlTWFwLFxuICBJT2JzZXJ2YWJsZVN0cmluZyxcbiAgSU9ic2VydmFibGVWYWx1ZSxcbiAgTW9kZWxEQixcbiAgT2JzZXJ2YWJsZVZhbHVlXG59IGZyb20gJ0BqdXB5dGVybGFiL29ic2VydmFibGVzJztcbmltcG9ydCAqIGFzIG1vZGVscyBmcm9tICdAanVweXRlcmxhYi9zaGFyZWQtbW9kZWxzJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgSlNPTk9iamVjdCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcblxuY29uc3QgZ2xvYmFsTW9kZWxEQk11dGV4ID0gbW9kZWxzLmNyZWF0ZU11dGV4KCk7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGNvZGUgZWRpdG9ycy5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiAtIEEgY29kZSBlZGl0b3IgaXMgYSBzZXQgb2YgY29tbW9uIGFzc3VtcHRpb25zIHdoaWNoIGhvbGQgZm9yIGFsbCBjb25jcmV0ZSBlZGl0b3JzLlxuICogLSBDaGFuZ2VzIGluIGltcGxlbWVudGF0aW9ucyBvZiB0aGUgY29kZSBlZGl0b3Igc2hvdWxkIG9ubHkgYmUgY2F1c2VkIGJ5IGNoYW5nZXMgaW4gY29uY3JldGUgZWRpdG9ycy5cbiAqIC0gQ29tbW9uIEpMYWIgc2VydmljZXMgd2hpY2ggYXJlIGJhc2VkIG9uIHRoZSBjb2RlIGVkaXRvciBzaG91bGQgYmVsb25nIHRvIGBJRWRpdG9yU2VydmljZXNgLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIENvZGVFZGl0b3Ige1xuICAvKipcbiAgICogQSB6ZXJvLWJhc2VkIHBvc2l0aW9uIGluIHRoZSBlZGl0b3IuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQb3NpdGlvbiBleHRlbmRzIEpTT05PYmplY3Qge1xuICAgIC8qKlxuICAgICAqIFRoZSBjdXJzb3IgbGluZSBudW1iZXIuXG4gICAgICovXG4gICAgcmVhZG9ubHkgbGluZTogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnNvciBjb2x1bW4gbnVtYmVyLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGNvbHVtbjogbnVtYmVyO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBkaW1lbnNpb24gb2YgYW4gZWxlbWVudC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSURpbWVuc2lvbiB7XG4gICAgLyoqXG4gICAgICogVGhlIHdpZHRoIG9mIGFuIGVsZW1lbnQgaW4gcGl4ZWxzLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IHdpZHRoOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgaGVpZ2h0IG9mIGFuIGVsZW1lbnQgaW4gcGl4ZWxzLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGhlaWdodDogbnVtYmVyO1xuICB9XG5cbiAgLyoqXG4gICAqIEFuIGludGVyZmFjZSBkZXNjcmliaW5nIGVkaXRvciBzdGF0ZSBjb29yZGluYXRlcy5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUNvb3JkaW5hdGUgZXh0ZW5kcyBKU09OT2JqZWN0LCBDbGllbnRSZWN0IHt9XG5cbiAgLyoqXG4gICAqIEEgcmFuZ2UuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElSYW5nZSBleHRlbmRzIEpTT05PYmplY3Qge1xuICAgIC8qKlxuICAgICAqIFRoZSBwb3NpdGlvbiBvZiB0aGUgZmlyc3QgY2hhcmFjdGVyIGluIHRoZSBjdXJyZW50IHJhbmdlLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIElmIHRoaXMgcG9zaXRpb24gaXMgZ3JlYXRlciB0aGFuIFtlbmRdIHRoZW4gdGhlIHJhbmdlIGlzIGNvbnNpZGVyZWRcbiAgICAgKiB0byBiZSBiYWNrd2FyZC5cbiAgICAgKi9cbiAgICByZWFkb25seSBzdGFydDogSVBvc2l0aW9uO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHBvc2l0aW9uIG9mIHRoZSBsYXN0IGNoYXJhY3RlciBpbiB0aGUgY3VycmVudCByYW5nZS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBJZiB0aGlzIHBvc2l0aW9uIGlzIGxlc3MgdGhhbiBbc3RhcnRdIHRoZW4gdGhlIHJhbmdlIGlzIGNvbnNpZGVyZWRcbiAgICAgKiB0byBiZSBiYWNrd2FyZC5cbiAgICAgKi9cbiAgICByZWFkb25seSBlbmQ6IElQb3NpdGlvbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNlbGVjdGlvbiBzdHlsZS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVNlbGVjdGlvblN0eWxlIGV4dGVuZHMgSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogQSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgc2VsZWN0aW9uLlxuICAgICAqL1xuICAgIGNsYXNzTmFtZTogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogQSBkaXNwbGF5IG5hbWUgYWRkZWQgdG8gYSBzZWxlY3Rpb24uXG4gICAgICovXG4gICAgZGlzcGxheU5hbWU6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEEgY29sb3IgZm9yIFVJIGVsZW1lbnRzLlxuICAgICAqL1xuICAgIGNvbG9yOiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRlZmF1bHQgc2VsZWN0aW9uIHN0eWxlLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRTZWxlY3Rpb25TdHlsZTogSVNlbGVjdGlvblN0eWxlID0ge1xuICAgIGNsYXNzTmFtZTogJycsXG4gICAgZGlzcGxheU5hbWU6ICcnLFxuICAgIGNvbG9yOiAnYmxhY2snXG4gIH07XG5cbiAgLyoqXG4gICAqIEEgdGV4dCBzZWxlY3Rpb24uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElUZXh0U2VsZWN0aW9uIGV4dGVuZHMgSVJhbmdlIHtcbiAgICAvKipcbiAgICAgKiBUaGUgdXVpZCBvZiB0aGUgdGV4dCBzZWxlY3Rpb24gb3duZXIuXG4gICAgICovXG4gICAgcmVhZG9ubHkgdXVpZDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHN0eWxlIG9mIHRoaXMgc2VsZWN0aW9uLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IHN0eWxlOiBJU2VsZWN0aW9uU3R5bGU7XG4gIH1cblxuICAvKipcbiAgICogQW4gaW50ZXJmYWNlIGZvciBhIHRleHQgdG9rZW4sIHN1Y2ggYXMgYSB3b3JkLCBrZXl3b3JkLCBvciB2YXJpYWJsZS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVRva2VuIHtcbiAgICAvKipcbiAgICAgKiBUaGUgdmFsdWUgb2YgdGhlIHRva2VuLlxuICAgICAqL1xuICAgIHZhbHVlOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgb2Zmc2V0IG9mIHRoZSB0b2tlbiBpbiB0aGUgY29kZSBlZGl0b3IuXG4gICAgICovXG4gICAgb2Zmc2V0OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBBbiBvcHRpb25hbCB0eXBlIGZvciB0aGUgdG9rZW4uXG4gICAgICovXG4gICAgdHlwZT86IHN0cmluZztcbiAgfVxuXG4gIC8qKlxuICAgKiBBbiBpbnRlcmZhY2UgdG8gbWFuYWdlIHNlbGVjdGlvbnMgYnkgc2VsZWN0aW9uIG93bmVycy5cbiAgICpcbiAgICogIyMjIyBEZWZpbml0aW9uc1xuICAgKiAtIGEgdXNlciBjb2RlIHRoYXQgaGFzIGFuIGFzc29jaWF0ZWQgdXVpZCBpcyBjYWxsZWQgYSBzZWxlY3Rpb24gb3duZXIsIHNlZSBgQ29kZUVkaXRvci5JU2VsZWN0aW9uT3duZXJgXG4gICAqIC0gYSBzZWxlY3Rpb24gYmVsb25ncyB0byBhIHNlbGVjdGlvbiBvd25lciBvbmx5IGlmIGl0IGlzIGFzc29jaWF0ZWQgd2l0aCB0aGUgb3duZXIgYnkgYW4gdXVpZCwgc2VlIGBDb2RlRWRpdG9yLklUZXh0U2VsZWN0aW9uYFxuICAgKlxuICAgKiAjIyMjIFJlYWQgYWNjZXNzXG4gICAqIC0gYW55IHVzZXIgY29kZSBjYW4gb2JzZXJ2ZSBhbnkgc2VsZWN0aW9uXG4gICAqXG4gICAqICMjIyMgV3JpdGUgYWNjZXNzXG4gICAqIC0gaWYgYSB1c2VyIGNvZGUgaXMgYSBzZWxlY3Rpb24gb3duZXIgdGhlbjpcbiAgICogICAtIGl0IGNhbiBjaGFuZ2Ugc2VsZWN0aW9ucyBiZWxvbmdpbmcgdG8gaXRcbiAgICogICAtIGJ1dCBpdCBtdXN0IG5vdCBjaGFuZ2Ugc2VsZWN0aW9ucyBiZWxvbmdpbmcgdG8gb3RoZXIgc2VsZWN0aW9uIG93bmVyc1xuICAgKiAtIG90aGVyd2lzZSBpdCBtdXN0IG5vdCBjaGFuZ2UgYW55IHNlbGVjdGlvblxuICAgKi9cblxuICAvKipcbiAgICogQW4gZWRpdG9yIG1vZGVsLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTW9kZWwgZXh0ZW5kcyBJRGlzcG9zYWJsZSB7XG4gICAgLyoqXG4gICAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIGEgcHJvcGVydHkgY2hhbmdlcy5cbiAgICAgKi9cbiAgICBtaW1lVHlwZUNoYW5nZWQ6IElTaWduYWw8SU1vZGVsLCBJQ2hhbmdlZEFyZ3M8c3RyaW5nPj47XG5cbiAgICAvKipcbiAgICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIHNoYXJlZCBtb2RlbCB3YXMgc3dpdGNoZWQuXG4gICAgICovXG4gICAgc2hhcmVkTW9kZWxTd2l0Y2hlZDogSVNpZ25hbDxJTW9kZWwsIGJvb2xlYW4+O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHRleHQgc3RvcmVkIGluIHRoZSBtb2RlbC5cbiAgICAgKi9cbiAgICByZWFkb25seSB2YWx1ZTogSU9ic2VydmFibGVTdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBBIG1pbWUgdHlwZSBvZiB0aGUgbW9kZWwuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSXQgaXMgbmV2ZXIgYG51bGxgLCB0aGUgZGVmYXVsdCBtaW1lIHR5cGUgaXMgYHRleHQvcGxhaW5gLlxuICAgICAqL1xuICAgIG1pbWVUeXBlOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudGx5IHNlbGVjdGVkIGNvZGUuXG4gICAgICovXG4gICAgcmVhZG9ubHkgc2VsZWN0aW9uczogSU9ic2VydmFibGVNYXA8SVRleHRTZWxlY3Rpb25bXT47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdW5kZXJseWluZyBgSU1vZGVsREJgIGluc3RhbmNlIGluIHdoaWNoIG1vZGVsXG4gICAgICogZGF0YSBpcyBzdG9yZWQuXG4gICAgICovXG4gICAgcmVhZG9ubHkgbW9kZWxEQjogSU1vZGVsREI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2hhcmVkIG1vZGVsIGZvciB0aGUgY2VsbCBlZGl0b3IuXG4gICAgICovXG4gICAgcmVhZG9ubHkgc2hhcmVkTW9kZWw6IG1vZGVscy5JU2hhcmVkVGV4dDtcblxuICAgIC8qKlxuICAgICAqIFdoZW4gd2UgaW5pdGlhbGl6ZSBhIGNlbGwgbW9kZWwsIHdlIGNyZWF0ZSBhIHN0YW5kYWxvbmUgY2VsbCBtb2RlbCB0aGF0IGNhbm5vdCBiZSBzaGFyZWQgaW4gYSBZTm90ZWJvb2suXG4gICAgICogQ2FsbCB0aGlzIGZ1bmN0aW9uIHRvIHJlLWluaXRpYWxpemUgdGhlIGxvY2FsIHJlcHJlc2VudGF0aW9uIGJhc2VkIG9uIGEgZnJlc2ggc2hhcmVkIG1vZGVsIChlLmcuIG1vZGVscy5ZRmlsZSBvciBtb2RlbHMuWUNvZGVDZWxsKS5cbiAgICAgKi9cbiAgICBzd2l0Y2hTaGFyZWRNb2RlbChcbiAgICAgIHNoYXJlZE1vZGVsOiBtb2RlbHMuSVNoYXJlZFRleHQsXG4gICAgICByZWluaXRpYWxpemU6IGJvb2xlYW5cbiAgICApOiB2b2lkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IGltcGxlbWVudGF0aW9uIG9mIHRoZSBlZGl0b3IgbW9kZWwuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgTW9kZWwgaW1wbGVtZW50cyBJTW9kZWwge1xuICAgIC8qKlxuICAgICAqIENvbnN0cnVjdCBhIG5ldyBNb2RlbC5cbiAgICAgKi9cbiAgICBjb25zdHJ1Y3RvcihvcHRpb25zPzogTW9kZWwuSU9wdGlvbnMpIHtcbiAgICAgIG9wdGlvbnMgPSBvcHRpb25zIHx8IHt9O1xuXG4gICAgICBpZiAob3B0aW9ucy5tb2RlbERCKSB7XG4gICAgICAgIHRoaXMubW9kZWxEQiA9IG9wdGlvbnMubW9kZWxEQjtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMubW9kZWxEQiA9IG5ldyBNb2RlbERCKCk7XG4gICAgICB9XG4gICAgICB0aGlzLnNoYXJlZE1vZGVsID0gbW9kZWxzLmNyZWF0ZVN0YW5kYWxvbmVDZWxsKFxuICAgICAgICB0aGlzLnR5cGUsXG4gICAgICAgIG9wdGlvbnMuaWRcbiAgICAgICkgYXMgbW9kZWxzLklTaGFyZWRUZXh0O1xuICAgICAgdGhpcy5zaGFyZWRNb2RlbC5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25TaGFyZWRNb2RlbENoYW5nZWQsIHRoaXMpO1xuXG4gICAgICBjb25zdCB2YWx1ZSA9IHRoaXMubW9kZWxEQi5jcmVhdGVTdHJpbmcoJ3ZhbHVlJyk7XG4gICAgICB2YWx1ZS5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25Nb2RlbERCVmFsdWVDaGFuZ2VkLCB0aGlzKTtcbiAgICAgIHZhbHVlLnRleHQgPSB2YWx1ZS50ZXh0IHx8IG9wdGlvbnMudmFsdWUgfHwgJyc7XG5cbiAgICAgIGNvbnN0IG1pbWVUeXBlID0gdGhpcy5tb2RlbERCLmNyZWF0ZVZhbHVlKCdtaW1lVHlwZScpO1xuICAgICAgbWltZVR5cGUuY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uTW9kZWxEQk1pbWVUeXBlQ2hhbmdlZCwgdGhpcyk7XG4gICAgICBtaW1lVHlwZS5zZXQob3B0aW9ucy5taW1lVHlwZSB8fCAndGV4dC9wbGFpbicpO1xuXG4gICAgICB0aGlzLm1vZGVsREIuY3JlYXRlTWFwKCdzZWxlY3Rpb25zJyk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogV2hlbiB3ZSBpbml0aWFsaXplIGEgY2VsbCBtb2RlbCwgd2UgY3JlYXRlIGEgc3RhbmRhbG9uZSBtb2RlbCB0aGF0IGNhbm5vdCBiZSBzaGFyZWQgaW4gYSBZTm90ZWJvb2suXG4gICAgICogQ2FsbCB0aGlzIGZ1bmN0aW9uIHRvIHJlLWluaXRpYWxpemUgdGhlIGxvY2FsIHJlcHJlc2VudGF0aW9uIGJhc2VkIG9uIGEgZnJlc2ggc2hhcmVkIG1vZGVsIChlLmcuIG1vZGVscy5ZRmlsZSBvciBtb2RlbHMuWUNvZGVDZWxsKS5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBzaGFyZWRNb2RlbFxuICAgICAqIEBwYXJhbSByZWluaXRpYWxpemUgV2hldGhlciB0byByZWluaXRpYWxpemUgdGhlIHNoYXJlZCBtb2RlbC5cbiAgICAgKi9cbiAgICBwdWJsaWMgc3dpdGNoU2hhcmVkTW9kZWwoXG4gICAgICBzaGFyZWRNb2RlbDogbW9kZWxzLklTaGFyZWRUZXh0LFxuICAgICAgcmVpbml0aWFsaXplPzogYm9vbGVhblxuICAgICk6IHZvaWQge1xuICAgICAgaWYgKHJlaW5pdGlhbGl6ZSkge1xuICAgICAgICAvLyB1cGRhdGUgbG9jYWwgbW9kZWxkYlxuICAgICAgICAvLyBAdG9kbyBhbHNvIGNoYW5nZSBtZXRhZGF0YVxuICAgICAgICB0aGlzLnZhbHVlLnRleHQgPSBzaGFyZWRNb2RlbC5nZXRTb3VyY2UoKTtcbiAgICAgIH1cbiAgICAgIHRoaXMuc2hhcmVkTW9kZWwuY2hhbmdlZC5kaXNjb25uZWN0KHRoaXMuX29uU2hhcmVkTW9kZWxDaGFuZ2VkLCB0aGlzKTtcbiAgICAgIC8vIGNsb25lIG1vZGVsIHJldHJpZXZlIGEgc2hhcmVkIChub3Qgc3RhbmRhbG9uZSkgbW9kZWxcbiAgICAgIHRoaXMuc2hhcmVkTW9kZWwgPSBzaGFyZWRNb2RlbDtcbiAgICAgIHRoaXMuc2hhcmVkTW9kZWwuY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uU2hhcmVkTW9kZWxDaGFuZ2VkLCB0aGlzKTtcbiAgICAgIHRoaXMuX3NoYXJlZE1vZGVsU3dpdGNoZWQuZW1pdCh0cnVlKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBXZSB1cGRhdGUgdGhlIG1vZGVsZGIgc3RvcmUgd2hlbiB0aGUgc2hhcmVkIG1vZGVsIGNoYW5nZXMuXG4gICAgICogVG8gZW5zdXJlIHRoYXQgd2UgZG9uJ3QgcnVuIGludG8gaW5maW5pdGUgbG9vcHMsIHdlIHdyYXAgdGhpcyBjYWxsIGluIGEgXCJtdXRleFwiLlxuICAgICAqIFRoZSBcIm11dGV4XCIgZW5zdXJlcyB0aGF0IHRoZSB3cmFwcGVkIGNvZGUgY2FuIG9ubHkgYmUgZXhlY3V0ZWQgYnkgZWl0aGVyIHRoZSBzaGFyZWRNb2RlbENoYW5nZWQgaGFuZGxlclxuICAgICAqIG9yIHRoZSBtb2RlbERCIGNoYW5nZSBoYW5kbGVyLlxuICAgICAqL1xuICAgIHByb3RlY3RlZCBfb25TaGFyZWRNb2RlbENoYW5nZWQoXG4gICAgICBzZW5kZXI6IG1vZGVscy5JU2hhcmVkQmFzZUNlbGw8YW55PixcbiAgICAgIGNoYW5nZTogbW9kZWxzLkNlbGxDaGFuZ2U8bmJmb3JtYXQuSUJhc2VDZWxsTWV0YWRhdGE+XG4gICAgKTogdm9pZCB7XG4gICAgICBnbG9iYWxNb2RlbERCTXV0ZXgoKCkgPT4ge1xuICAgICAgICBpZiAoY2hhbmdlLnNvdXJjZUNoYW5nZSkge1xuICAgICAgICAgIGNvbnN0IHZhbHVlID0gdGhpcy5tb2RlbERCLmdldCgndmFsdWUnKSBhcyBJT2JzZXJ2YWJsZVN0cmluZztcbiAgICAgICAgICBsZXQgY3VycnBvcyA9IDA7XG4gICAgICAgICAgY2hhbmdlLnNvdXJjZUNoYW5nZS5mb3JFYWNoKGRlbHRhID0+IHtcbiAgICAgICAgICAgIGlmIChkZWx0YS5pbnNlcnQgIT0gbnVsbCkge1xuICAgICAgICAgICAgICB2YWx1ZS5pbnNlcnQoY3VycnBvcywgZGVsdGEuaW5zZXJ0KTtcbiAgICAgICAgICAgICAgY3VycnBvcyArPSBkZWx0YS5pbnNlcnQubGVuZ3RoO1xuICAgICAgICAgICAgfSBlbHNlIGlmIChkZWx0YS5kZWxldGUgIT0gbnVsbCkge1xuICAgICAgICAgICAgICB2YWx1ZS5yZW1vdmUoY3VycnBvcywgY3VycnBvcyArIGRlbHRhLmRlbGV0ZSk7XG4gICAgICAgICAgICB9IGVsc2UgaWYgKGRlbHRhLnJldGFpbiAhPSBudWxsKSB7XG4gICAgICAgICAgICAgIGN1cnJwb3MgKz0gZGVsdGEucmV0YWluO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIG1vZGVsREIgdmFsdWUuXG4gICAgICovXG4gICAgcHJpdmF0ZSBfb25Nb2RlbERCVmFsdWVDaGFuZ2VkKFxuICAgICAgdmFsdWU6IElPYnNlcnZhYmxlU3RyaW5nLFxuICAgICAgZXZlbnQ6IElPYnNlcnZhYmxlU3RyaW5nLklDaGFuZ2VkQXJnc1xuICAgICk6IHZvaWQge1xuICAgICAgZ2xvYmFsTW9kZWxEQk11dGV4KCgpID0+IHtcbiAgICAgICAgdGhpcy5zaGFyZWRNb2RlbC50cmFuc2FjdCgoKSA9PiB7XG4gICAgICAgICAgc3dpdGNoIChldmVudC50eXBlKSB7XG4gICAgICAgICAgICBjYXNlICdpbnNlcnQnOlxuICAgICAgICAgICAgICB0aGlzLnNoYXJlZE1vZGVsLnVwZGF0ZVNvdXJjZShcbiAgICAgICAgICAgICAgICBldmVudC5zdGFydCxcbiAgICAgICAgICAgICAgICBldmVudC5zdGFydCxcbiAgICAgICAgICAgICAgICBldmVudC52YWx1ZVxuICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIGNhc2UgJ3JlbW92ZSc6XG4gICAgICAgICAgICAgIHRoaXMuc2hhcmVkTW9kZWwudXBkYXRlU291cmNlKGV2ZW50LnN0YXJ0LCBldmVudC5lbmQpO1xuICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICAgIHRoaXMuc2hhcmVkTW9kZWwuc2V0U291cmNlKHZhbHVlLnRleHQpO1xuICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgICAgfSk7XG4gICAgfVxuXG4gICAgZ2V0IHR5cGUoKTogbmJmb3JtYXQuQ2VsbFR5cGUge1xuICAgICAgcmV0dXJuICdjb2RlJztcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2hhcmVkIG1vZGVsIGZvciB0aGUgY2VsbCBlZGl0b3IuXG4gICAgICovXG4gICAgc2hhcmVkTW9kZWw6IG1vZGVscy5JU2hhcmVkVGV4dDtcblxuICAgIC8qKlxuICAgICAqIFRoZSB1bmRlcmx5aW5nIGBJTW9kZWxEQmAgaW5zdGFuY2UgaW4gd2hpY2ggbW9kZWxcbiAgICAgKiBkYXRhIGlzIHN0b3JlZC5cbiAgICAgKi9cbiAgICByZWFkb25seSBtb2RlbERCOiBJTW9kZWxEQjtcblxuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBhIG1pbWV0eXBlIGNoYW5nZXMuXG4gICAgICovXG4gICAgZ2V0IG1pbWVUeXBlQ2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElDaGFuZ2VkQXJnczxzdHJpbmc+PiB7XG4gICAgICByZXR1cm4gdGhpcy5fbWltZVR5cGVDaGFuZ2VkO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgc2hhcmVkIG1vZGVsIHdhcyBzd2l0Y2hlZC5cbiAgICAgKi9cbiAgICBnZXQgc2hhcmVkTW9kZWxTd2l0Y2hlZCgpOiBJU2lnbmFsPHRoaXMsIGJvb2xlYW4+IHtcbiAgICAgIHJldHVybiB0aGlzLl9zaGFyZWRNb2RlbFN3aXRjaGVkO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgdmFsdWUgb2YgdGhlIG1vZGVsLlxuICAgICAqL1xuICAgIGdldCB2YWx1ZSgpOiBJT2JzZXJ2YWJsZVN0cmluZyB7XG4gICAgICByZXR1cm4gdGhpcy5tb2RlbERCLmdldCgndmFsdWUnKSBhcyBJT2JzZXJ2YWJsZVN0cmluZztcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIHNlbGVjdGlvbnMgZm9yIHRoZSBtb2RlbC5cbiAgICAgKi9cbiAgICBnZXQgc2VsZWN0aW9ucygpOiBJT2JzZXJ2YWJsZU1hcDxJVGV4dFNlbGVjdGlvbltdPiB7XG4gICAgICByZXR1cm4gdGhpcy5tb2RlbERCLmdldCgnc2VsZWN0aW9ucycpIGFzIElPYnNlcnZhYmxlTWFwPElUZXh0U2VsZWN0aW9uW10+O1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgbWltZSB0eXBlIG9mIHRoZSBtb2RlbC5cbiAgICAgKi9cbiAgICBnZXQgbWltZVR5cGUoKTogc3RyaW5nIHtcbiAgICAgIHJldHVybiB0aGlzLm1vZGVsREIuZ2V0VmFsdWUoJ21pbWVUeXBlJykgYXMgc3RyaW5nO1xuICAgIH1cbiAgICBzZXQgbWltZVR5cGUobmV3VmFsdWU6IHN0cmluZykge1xuICAgICAgY29uc3Qgb2xkVmFsdWUgPSB0aGlzLm1pbWVUeXBlO1xuICAgICAgaWYgKG9sZFZhbHVlID09PSBuZXdWYWx1ZSkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICB0aGlzLm1vZGVsREIuc2V0VmFsdWUoJ21pbWVUeXBlJywgbmV3VmFsdWUpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdGhlIG1vZGVsIGlzIGRpc3Bvc2VkLlxuICAgICAqL1xuICAgIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIHVzZWQgYnkgdGhlIG1vZGVsLlxuICAgICAqL1xuICAgIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgICBpZiAodGhpcy5faXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfb25Nb2RlbERCTWltZVR5cGVDaGFuZ2VkKFxuICAgICAgbWltZVR5cGU6IElPYnNlcnZhYmxlVmFsdWUsXG4gICAgICBhcmdzOiBPYnNlcnZhYmxlVmFsdWUuSUNoYW5nZWRBcmdzXG4gICAgKTogdm9pZCB7XG4gICAgICB0aGlzLl9taW1lVHlwZUNoYW5nZWQuZW1pdCh7XG4gICAgICAgIG5hbWU6ICdtaW1lVHlwZScsXG4gICAgICAgIG9sZFZhbHVlOiBhcmdzLm9sZFZhbHVlIGFzIHN0cmluZyxcbiAgICAgICAgbmV3VmFsdWU6IGFyZ3MubmV3VmFsdWUgYXMgc3RyaW5nXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBwcml2YXRlIF9pc0Rpc3Bvc2VkID0gZmFsc2U7XG4gICAgcHJpdmF0ZSBfbWltZVR5cGVDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBJQ2hhbmdlZEFyZ3M8c3RyaW5nPj4odGhpcyk7XG4gICAgcHJpdmF0ZSBfc2hhcmVkTW9kZWxTd2l0Y2hlZCA9IG5ldyBTaWduYWw8dGhpcywgYm9vbGVhbj4odGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogQSBzZWxlY3Rpb24gb3duZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElTZWxlY3Rpb25Pd25lciB7XG4gICAgLyoqXG4gICAgICogVGhlIHV1aWQgb2YgdGhpcyBzZWxlY3Rpb24gb3duZXIuXG4gICAgICovXG4gICAgdXVpZDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogUmV0dXJucyB0aGUgcHJpbWFyeSBwb3NpdGlvbiBvZiB0aGUgY3Vyc29yLCBuZXZlciBgbnVsbGAuXG4gICAgICovXG4gICAgZ2V0Q3Vyc29yUG9zaXRpb24oKTogSVBvc2l0aW9uO1xuXG4gICAgLyoqXG4gICAgICogU2V0IHRoZSBwcmltYXJ5IHBvc2l0aW9uIG9mIHRoZSBjdXJzb3IuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gcG9zaXRpb24gLSBUaGUgbmV3IHByaW1hcnkgcG9zaXRpb24uXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhpcyB3aWxsIHJlbW92ZSBhbnkgc2Vjb25kYXJ5IGN1cnNvcnMuXG4gICAgICovXG4gICAgc2V0Q3Vyc29yUG9zaXRpb24ocG9zaXRpb246IElQb3NpdGlvbik6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBSZXR1cm5zIHRoZSBwcmltYXJ5IHNlbGVjdGlvbiwgbmV2ZXIgYG51bGxgLlxuICAgICAqL1xuICAgIGdldFNlbGVjdGlvbigpOiBJUmFuZ2U7XG5cbiAgICAvKipcbiAgICAgKiBTZXQgdGhlIHByaW1hcnkgc2VsZWN0aW9uLlxuICAgICAqXG4gICAgICogQHBhcmFtIHNlbGVjdGlvbiAtIFRoZSBkZXNpcmVkIHNlbGVjdGlvbiByYW5nZS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGlzIHdpbGwgcmVtb3ZlIGFueSBzZWNvbmRhcnkgY3Vyc29ycy5cbiAgICAgKi9cbiAgICBzZXRTZWxlY3Rpb24oc2VsZWN0aW9uOiBJUmFuZ2UpOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogR2V0cyB0aGUgc2VsZWN0aW9ucyBmb3IgYWxsIHRoZSBjdXJzb3JzLCBuZXZlciBgbnVsbGAgb3IgZW1wdHkuXG4gICAgICovXG4gICAgZ2V0U2VsZWN0aW9ucygpOiBJUmFuZ2VbXTtcblxuICAgIC8qKlxuICAgICAqIFNldHMgdGhlIHNlbGVjdGlvbnMgZm9yIGFsbCB0aGUgY3Vyc29ycy5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBzZWxlY3Rpb25zIC0gVGhlIG5ldyBzZWxlY3Rpb25zLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIEN1cnNvcnMgd2lsbCBiZSByZW1vdmVkIG9yIGFkZGVkLCBhcyBuZWNlc3NhcnkuXG4gICAgICogUGFzc2luZyBhbiBlbXB0eSBhcnJheSByZXNldHMgYSBjdXJzb3IgcG9zaXRpb24gdG8gdGhlIHN0YXJ0IG9mIGFcbiAgICAgKiBkb2N1bWVudC5cbiAgICAgKi9cbiAgICBzZXRTZWxlY3Rpb25zKHNlbGVjdGlvbnM6IElSYW5nZVtdKTogdm9pZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIGtleWRvd24gaGFuZGxlciB0eXBlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFJldHVybiBgdHJ1ZWAgdG8gcHJldmVudCB0aGUgZGVmYXVsdCBoYW5kbGluZyBvZiB0aGUgZXZlbnQgYnkgdGhlXG4gICAqIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCB0eXBlIEtleWRvd25IYW5kbGVyID0gKFxuICAgIGluc3RhbmNlOiBJRWRpdG9yLFxuICAgIGV2ZW50OiBLZXlib2FyZEV2ZW50XG4gICkgPT4gYm9vbGVhbjtcblxuICAvKipcbiAgICogVGhlIGxvY2F0aW9uIG9mIHJlcXVlc3RlZCBlZGdlcy5cbiAgICovXG4gIGV4cG9ydCB0eXBlIEVkZ2VMb2NhdGlvbiA9ICd0b3AnIHwgJ3RvcExpbmUnIHwgJ2JvdHRvbSc7XG5cbiAgLyoqXG4gICAqIEEgd2lkZ2V0IHRoYXQgcHJvdmlkZXMgYSBjb2RlIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUVkaXRvciBleHRlbmRzIElTZWxlY3Rpb25Pd25lciwgSURpc3Bvc2FibGUge1xuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBlaXRoZXIgdGhlIHRvcCBvciBib3R0b20gZWRnZSBpcyByZXF1ZXN0ZWQuXG4gICAgICovXG4gICAgcmVhZG9ubHkgZWRnZVJlcXVlc3RlZDogSVNpZ25hbDxJRWRpdG9yLCBFZGdlTG9jYXRpb24+O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGRlZmF1bHQgc2VsZWN0aW9uIHN0eWxlIGZvciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIHNlbGVjdGlvblN0eWxlOiBDb2RlRWRpdG9yLklTZWxlY3Rpb25TdHlsZTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBET00gbm9kZSB0aGF0IGhvc3RzIHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgcmVhZG9ubHkgaG9zdDogSFRNTEVsZW1lbnQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbW9kZWwgdXNlZCBieSB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IG1vZGVsOiBJTW9kZWw7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgaGVpZ2h0IG9mIGEgbGluZSBpbiB0aGUgZWRpdG9yIGluIHBpeGVscy5cbiAgICAgKi9cbiAgICByZWFkb25seSBsaW5lSGVpZ2h0OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgd2lkZ2V0IG9mIGEgY2hhcmFjdGVyIGluIHRoZSBlZGl0b3IgaW4gcGl4ZWxzLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGNoYXJXaWR0aDogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSBudW1iZXIgb2YgbGluZXMgaW4gdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICByZWFkb25seSBsaW5lQ291bnQ6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIEdldCBhIGNvbmZpZyBvcHRpb24gZm9yIHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgZ2V0T3B0aW9uPEsgZXh0ZW5kcyBrZXlvZiBJQ29uZmlnPihvcHRpb246IEspOiBJQ29uZmlnW0tdO1xuXG4gICAgLyoqXG4gICAgICogU2V0IGEgY29uZmlnIG9wdGlvbiBmb3IgdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICBzZXRPcHRpb248SyBleHRlbmRzIGtleW9mIElDb25maWc+KG9wdGlvbjogSywgdmFsdWU6IElDb25maWdbS10pOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogU2V0IGNvbmZpZyBvcHRpb25zIGZvciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIHNldE9wdGlvbnM8SyBleHRlbmRzIGtleW9mIElDb25maWc+KG9wdGlvbnM6IElDb25maWdPcHRpb25zPEs+W10pOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogUmV0dXJucyB0aGUgY29udGVudCBmb3IgdGhlIGdpdmVuIGxpbmUgbnVtYmVyLlxuICAgICAqXG4gICAgICogQHBhcmFtIGxpbmUgLSBUaGUgbGluZSBvZiBpbnRlcmVzdC5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIFRoZSB2YWx1ZSBvZiB0aGUgbGluZS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBMaW5lcyBhcmUgMC1iYXNlZCwgYW5kIGFjY2Vzc2luZyBhIGxpbmUgb3V0IG9mIHJhbmdlIHJldHVybnNcbiAgICAgKiBgdW5kZWZpbmVkYC5cbiAgICAgKi9cbiAgICBnZXRMaW5lKGxpbmU6IG51bWJlcik6IHN0cmluZyB8IHVuZGVmaW5lZDtcblxuICAgIC8qKlxuICAgICAqIEZpbmQgYW4gb2Zmc2V0IGZvciB0aGUgZ2l2ZW4gcG9zaXRpb24uXG4gICAgICpcbiAgICAgKiBAcGFyYW0gcG9zaXRpb24gLSBUaGUgcG9zaXRpb24gb2YgaW50ZXJlc3QuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBUaGUgb2Zmc2V0IGF0IHRoZSBwb3NpdGlvbiwgY2xhbXBlZCB0byB0aGUgZXh0ZW50IG9mIHRoZVxuICAgICAqIGVkaXRvciBjb250ZW50cy5cbiAgICAgKi9cbiAgICBnZXRPZmZzZXRBdChwb3NpdGlvbjogSVBvc2l0aW9uKTogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogRmluZCBhIHBvc2l0aW9uIGZvciB0aGUgZ2l2ZW4gb2Zmc2V0LlxuICAgICAqXG4gICAgICogQHBhcmFtIG9mZnNldCAtIFRoZSBvZmZzZXQgb2YgaW50ZXJlc3QuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBUaGUgcG9zaXRpb24gYXQgdGhlIG9mZnNldCwgY2xhbXBlZCB0byB0aGUgZXh0ZW50IG9mIHRoZVxuICAgICAqIGVkaXRvciBjb250ZW50cy5cbiAgICAgKi9cbiAgICBnZXRQb3NpdGlvbkF0KG9mZnNldDogbnVtYmVyKTogSVBvc2l0aW9uIHwgdW5kZWZpbmVkO1xuXG4gICAgLyoqXG4gICAgICogVW5kbyBvbmUgZWRpdCAoaWYgYW55IHVuZG8gZXZlbnRzIGFyZSBzdG9yZWQpLlxuICAgICAqL1xuICAgIHVuZG8oKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIFJlZG8gb25lIHVuZG9uZSBlZGl0LlxuICAgICAqL1xuICAgIHJlZG8oKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIENsZWFyIHRoZSB1bmRvIGhpc3RvcnkuXG4gICAgICovXG4gICAgY2xlYXJIaXN0b3J5KCk6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBCcmluZ3MgYnJvd3NlciBmb2N1cyB0byB0aGlzIGVkaXRvciB0ZXh0LlxuICAgICAqL1xuICAgIGZvY3VzKCk6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBUZXN0IHdoZXRoZXIgdGhlIGVkaXRvciBoYXMga2V5Ym9hcmQgZm9jdXMuXG4gICAgICovXG4gICAgaGFzRm9jdXMoKTogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIEV4cGxpY2l0bHkgYmx1ciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIGJsdXIoKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIFJlcGFpbnQgdGhlIGVkaXRvci5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBBIHJlcGFpbnRlZCBlZGl0b3Igc2hvdWxkIGZpdCB0byBpdHMgaG9zdCBub2RlLlxuICAgICAqL1xuICAgIHJlZnJlc2goKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIFJlc2l6ZSB0aGUgZWRpdG9yIHRvIGZpdCBpdHMgaG9zdCBub2RlLlxuICAgICAqL1xuICAgIHJlc2l6ZVRvRml0KCk6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBBZGQgYSBrZXlkb3duIGhhbmRsZXIgdG8gdGhlIGVkaXRvci5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBoYW5kbGVyIC0gQSBrZXlkb3duIGhhbmRsZXIuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBBIGRpc3Bvc2FibGUgdGhhdCBjYW4gYmUgdXNlZCB0byByZW1vdmUgdGhlIGhhbmRsZXIuXG4gICAgICovXG4gICAgYWRkS2V5ZG93bkhhbmRsZXIoaGFuZGxlcjogS2V5ZG93bkhhbmRsZXIpOiBJRGlzcG9zYWJsZTtcblxuICAgIC8qKlxuICAgICAqIFNldCB0aGUgc2l6ZSBvZiB0aGUgZWRpdG9yLlxuICAgICAqXG4gICAgICogQHBhcmFtIHNpemUgLSBUaGUgZGVzaXJlZCBzaXplLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFVzZSBgbnVsbGAgaWYgdGhlIHNpemUgaXMgdW5rbm93bi5cbiAgICAgKi9cbiAgICBzZXRTaXplKHNpemU6IElEaW1lbnNpb24gfCBudWxsKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIFJldmVhbHMgdGhlIGdpdmVuIHBvc2l0aW9uIGluIHRoZSBlZGl0b3IuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gcG9zaXRpb24gLSBUaGUgZGVzaXJlZCBwb3NpdGlvbiB0byByZXZlYWwuXG4gICAgICovXG4gICAgcmV2ZWFsUG9zaXRpb24ocG9zaXRpb246IElQb3NpdGlvbik6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBSZXZlYWxzIHRoZSBnaXZlbiBzZWxlY3Rpb24gaW4gdGhlIGVkaXRvci5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBwb3NpdGlvbiAtIFRoZSBkZXNpcmVkIHNlbGVjdGlvbiB0byByZXZlYWwuXG4gICAgICovXG4gICAgcmV2ZWFsU2VsZWN0aW9uKHNlbGVjdGlvbjogSVJhbmdlKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgd2luZG93IGNvb3JkaW5hdGVzIGdpdmVuIGEgY3Vyc29yIHBvc2l0aW9uLlxuICAgICAqXG4gICAgICogQHBhcmFtIHBvc2l0aW9uIC0gVGhlIGRlc2lyZWQgcG9zaXRpb24uXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBUaGUgY29vcmRpbmF0ZXMgb2YgdGhlIHBvc2l0aW9uLlxuICAgICAqL1xuICAgIGdldENvb3JkaW5hdGVGb3JQb3NpdGlvbihwb3NpdGlvbjogSVBvc2l0aW9uKTogSUNvb3JkaW5hdGU7XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIGN1cnNvciBwb3NpdGlvbiBnaXZlbiB3aW5kb3cgY29vcmRpbmF0ZXMuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gY29vcmRpbmF0ZSAtIFRoZSBkZXNpcmVkIGNvb3JkaW5hdGUuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBUaGUgcG9zaXRpb24gb2YgdGhlIGNvb3JkaW5hdGVzLCBvciBudWxsIGlmIG5vdFxuICAgICAqICAgY29udGFpbmVkIGluIHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgZ2V0UG9zaXRpb25Gb3JDb29yZGluYXRlKGNvb3JkaW5hdGU6IElDb29yZGluYXRlKTogSVBvc2l0aW9uIHwgbnVsbDtcblxuICAgIC8qKlxuICAgICAqIEluc2VydHMgYSBuZXcgbGluZSBhdCB0aGUgY3Vyc29yIHBvc2l0aW9uIGFuZCBpbmRlbnRzIGl0LlxuICAgICAqL1xuICAgIG5ld0luZGVudGVkTGluZSgpOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogR2V0cyB0aGUgdG9rZW4gYXQgYSBnaXZlbiBwb3NpdGlvbi5cbiAgICAgKi9cbiAgICBnZXRUb2tlbkZvclBvc2l0aW9uKHBvc2l0aW9uOiBJUG9zaXRpb24pOiBJVG9rZW47XG5cbiAgICAvKipcbiAgICAgKiBHZXRzIHRoZSBsaXN0IG9mIHRva2VucyBmb3IgdGhlIGVkaXRvciBtb2RlbC5cbiAgICAgKi9cbiAgICBnZXRUb2tlbnMoKTogSVRva2VuW107XG5cbiAgICAvKipcbiAgICAgKiBSZXBsYWNlcyBzZWxlY3Rpb24gd2l0aCB0aGUgZ2l2ZW4gdGV4dC5cbiAgICAgKi9cbiAgICByZXBsYWNlU2VsZWN0aW9uPyh0ZXh0OiBzdHJpbmcpOiB2b2lkO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgZmFjdG9yeSB1c2VkIHRvIGNyZWF0ZSBhIGNvZGUgZWRpdG9yLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgRmFjdG9yeSA9IChvcHRpb25zOiBJT3B0aW9ucykgPT4gQ29kZUVkaXRvci5JRWRpdG9yO1xuXG4gIC8qKlxuICAgKiBUaGUgY29uZmlndXJhdGlvbiBvcHRpb25zIGZvciBhbiBlZGl0b3IuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDb25maWcge1xuICAgIC8qKlxuICAgICAqIEhhbGYtcGVyaW9kIGluIG1pbGxpc2Vjb25kcyB1c2VkIGZvciBjdXJzb3IgYmxpbmtpbmcuXG4gICAgICogQnkgc2V0dGluZyB0aGlzIHRvIHplcm8sIGJsaW5raW5nIGNhbiBiZSBkaXNhYmxlZC5cbiAgICAgKiBBIG5lZ2F0aXZlIHZhbHVlIGhpZGVzIHRoZSBjdXJzb3IgZW50aXJlbHkuXG4gICAgICovXG4gICAgY3Vyc29yQmxpbmtSYXRlOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBVc2VyIHByZWZlcnJlZCBmb250IGZhbWlseSBmb3IgdGV4dCBlZGl0b3JzLlxuICAgICAqL1xuICAgIGZvbnRGYW1pbHk6IHN0cmluZyB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBVc2VyIHByZWZlcnJlZCBzaXplIGluIHBpeGVsIG9mIHRoZSBmb250IHVzZWQgaW4gdGV4dCBlZGl0b3JzLlxuICAgICAqL1xuICAgIGZvbnRTaXplOiBudW1iZXIgfCBudWxsO1xuXG4gICAgLyoqXG4gICAgICogVXNlciBwcmVmZXJyZWQgdGV4dCBsaW5lIGhlaWdodCwgYXMgYSBtdWx0aXBsaWVyIG9mIGZvbnQgc2l6ZS5cbiAgICAgKi9cbiAgICBsaW5lSGVpZ2h0OiBudW1iZXIgfCBudWxsO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciBsaW5lIG51bWJlcnMgc2hvdWxkIGJlIGRpc3BsYXllZC5cbiAgICAgKi9cbiAgICBsaW5lTnVtYmVyczogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIENvbnRyb2wgdGhlIGxpbmUgd3JhcHBpbmcgb2YgdGhlIGVkaXRvci4gUG9zc2libGUgdmFsdWVzIGFyZTpcbiAgICAgKiAtIFwib2ZmXCIsIGxpbmVzIHdpbGwgbmV2ZXIgd3JhcC5cbiAgICAgKiAtIFwib25cIiwgbGluZXMgd2lsbCB3cmFwIGF0IHRoZSB2aWV3cG9ydCBib3JkZXIuXG4gICAgICogLSBcIndvcmRXcmFwQ29sdW1uXCIsIGxpbmVzIHdpbGwgd3JhcCBhdCBgd29yZFdyYXBDb2x1bW5gLlxuICAgICAqIC0gXCJib3VuZGVkXCIsIGxpbmVzIHdpbGwgd3JhcCBhdCBtaW5pbXVtIGJldHdlZW4gdmlld3BvcnQgd2lkdGggYW5kIHdvcmRXcmFwQ29sdW1uLlxuICAgICAqL1xuICAgIGxpbmVXcmFwOiAnb2ZmJyB8ICdvbicgfCAnd29yZFdyYXBDb2x1bW4nIHwgJ2JvdW5kZWQnO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0aGUgZWRpdG9yIGlzIHJlYWQtb25seS5cbiAgICAgKi9cbiAgICByZWFkT25seTogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBudW1iZXIgb2Ygc3BhY2VzIGEgdGFiIGlzIGVxdWFsIHRvLlxuICAgICAqL1xuICAgIHRhYlNpemU6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gaW5zZXJ0IHNwYWNlcyB3aGVuIHByZXNzaW5nIFRhYi5cbiAgICAgKi9cbiAgICBpbnNlcnRTcGFjZXM6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGhpZ2hsaWdodCBtYXRjaGluZyBicmFja2V0cyB3aGVuIG9uZSBvZiB0aGVtIGlzIHNlbGVjdGVkLlxuICAgICAqL1xuICAgIG1hdGNoQnJhY2tldHM6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGF1dG9tYXRpY2FsbHkgY2xvc2UgYnJhY2tldHMgYWZ0ZXIgb3BlbmluZyB0aGVtLlxuICAgICAqL1xuICAgIGF1dG9DbG9zaW5nQnJhY2tldHM6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBlZGl0b3Igc2hvdWxkIGhhbmRsZSBwYXN0ZSBldmVudHMuXG4gICAgICovXG4gICAgaGFuZGxlUGFzdGU/OiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNvbHVtbiB3aGVyZSB0byBicmVhayB0ZXh0IGxpbmUuXG4gICAgICovXG4gICAgd29yZFdyYXBDb2x1bW46IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIENvbHVtbiBpbmRleCBhdCB3aGljaCBydWxlcnMgc2hvdWxkIGJlIGFkZGVkLlxuICAgICAqL1xuICAgIHJ1bGVyczogQXJyYXk8bnVtYmVyPjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gYWxsb3cgY29kZSBmb2xkaW5nXG4gICAgICovXG4gICAgY29kZUZvbGRpbmc6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGhpZ2hsaWdodCB0cmFpbGluZyB3aGl0ZXNwYWNlXG4gICAgICovXG4gICAgc2hvd1RyYWlsaW5nU3BhY2U6IGJvb2xlYW47XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRlZmF1bHQgY29uZmlndXJhdGlvbiBvcHRpb25zIGZvciBhbiBlZGl0b3IuXG4gICAqL1xuICBleHBvcnQgY29uc3QgZGVmYXVsdENvbmZpZzogSUNvbmZpZyA9IHtcbiAgICBjdXJzb3JCbGlua1JhdGU6IDUzMCxcbiAgICBmb250RmFtaWx5OiBudWxsLFxuICAgIGZvbnRTaXplOiBudWxsLFxuICAgIGxpbmVIZWlnaHQ6IG51bGwsXG4gICAgbGluZU51bWJlcnM6IGZhbHNlLFxuICAgIGxpbmVXcmFwOiAnb24nLFxuICAgIHdvcmRXcmFwQ29sdW1uOiA4MCxcbiAgICByZWFkT25seTogZmFsc2UsXG4gICAgdGFiU2l6ZTogNCxcbiAgICBpbnNlcnRTcGFjZXM6IHRydWUsXG4gICAgbWF0Y2hCcmFja2V0czogdHJ1ZSxcbiAgICBhdXRvQ2xvc2luZ0JyYWNrZXRzOiBmYWxzZSxcbiAgICBoYW5kbGVQYXN0ZTogdHJ1ZSxcbiAgICBydWxlcnM6IFtdLFxuICAgIGNvZGVGb2xkaW5nOiBmYWxzZSxcbiAgICBzaG93VHJhaWxpbmdTcGFjZTogZmFsc2VcbiAgfTtcblxuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBzZXQgc2V2ZXJhbCBvcHRpb25zIGF0IG9uY2Ugd2l0aCBzZXRPcHRpb25zLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29uZmlnT3B0aW9uczxLIGV4dGVuZHMga2V5b2YgSUNvbmZpZz4ge1xuICAgIEs6IElDb25maWdbS107XG4gIH1cblxuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBpbml0aWFsaXplIGFuIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBob3N0IHdpZGdldCB1c2VkIGJ5IHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgaG9zdDogSFRNTEVsZW1lbnQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbW9kZWwgdXNlZCBieSB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIG1vZGVsOiBJTW9kZWw7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZGVzaXJlZCB1dWlkIGZvciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIHV1aWQ/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZGVmYXVsdCBzZWxlY3Rpb24gc3R5bGUgZm9yIHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgc2VsZWN0aW9uU3R5bGU/OiBQYXJ0aWFsPENvZGVFZGl0b3IuSVNlbGVjdGlvblN0eWxlPjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjb25maWd1cmF0aW9uIG9wdGlvbnMgZm9yIHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgY29uZmlnPzogUGFydGlhbDxJQ29uZmlnPjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjb25maWd1cmF0aW9uIG9wdGlvbnMgZm9yIHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICB9XG5cbiAgZXhwb3J0IG5hbWVzcGFjZSBNb2RlbCB7XG4gICAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgICBpZD86IHN0cmluZztcbiAgICAgIC8qKlxuICAgICAgICogVGhlIGluaXRpYWwgdmFsdWUgb2YgdGhlIG1vZGVsLlxuICAgICAgICovXG4gICAgICB2YWx1ZT86IHN0cmluZztcblxuICAgICAgLyoqXG4gICAgICAgKiBUaGUgbWltZXR5cGUgb2YgdGhlIG1vZGVsLlxuICAgICAgICovXG4gICAgICBtaW1lVHlwZT86IHN0cmluZztcblxuICAgICAgLyoqXG4gICAgICAgKiBBbiBvcHRpb25hbCBtb2RlbERCIGZvciBzdG9yaW5nIG1vZGVsIHN0YXRlLlxuICAgICAgICovXG4gICAgICBtb2RlbERCPzogSU1vZGVsREI7XG4gICAgfVxuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBjb2RlZWRpdG9yXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9lZGl0b3InO1xuZXhwb3J0ICogZnJvbSAnLi9qc29uZWRpdG9yJztcbmV4cG9ydCAqIGZyb20gJy4vd2lkZ2V0JztcbmV4cG9ydCAqIGZyb20gJy4vZmFjdG9yeSc7XG5leHBvcnQgKiBmcm9tICcuL21pbWV0eXBlJztcbmV4cG9ydCAqIGZyb20gJy4vdG9rZW5zJztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSU9ic2VydmFibGVKU09OIH0gZnJvbSAnQGp1cHl0ZXJsYWIvb2JzZXJ2YWJsZXMnO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIG51bGxUcmFuc2xhdG9yLFxuICBUcmFuc2xhdGlvbkJ1bmRsZVxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBjaGVja0ljb24sIHVuZG9JY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQge1xuICBKU09ORXh0LFxuICBKU09OT2JqZWN0LFxuICBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0XG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgQ29kZUVkaXRvciB9IGZyb20gJy4vZWRpdG9yJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhIEpTT05FZGl0b3IgaW5zdGFuY2UuXG4gKi9cbmNvbnN0IEpTT05FRElUT1JfQ0xBU1MgPSAnanAtSlNPTkVkaXRvcic7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgd2hlbiB0aGUgTWV0YWRhdGEgZWRpdG9yIGNvbnRhaW5zIGludmFsaWQgSlNPTi5cbiAqL1xuY29uc3QgRVJST1JfQ0xBU1MgPSAnanAtbW9kLWVycm9yJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byB0aGUgZWRpdG9yIGhvc3Qgbm9kZS5cbiAqL1xuY29uc3QgSE9TVF9DTEFTUyA9ICdqcC1KU09ORWRpdG9yLWhvc3QnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHRoZSBoZWFkZXIgYXJlYS5cbiAqL1xuY29uc3QgSEVBREVSX0NMQVNTID0gJ2pwLUpTT05FZGl0b3ItaGVhZGVyJztcblxuLyoqXG4gKiBBIHdpZGdldCBmb3IgZWRpdGluZyBvYnNlcnZhYmxlIEpTT04uXG4gKi9cbmV4cG9ydCBjbGFzcyBKU09ORWRpdG9yIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBKU09OIGVkaXRvci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IEpTT05FZGl0b3IuSU9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IG9wdGlvbnMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl90cmFucyA9IHRoaXMudHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgdGhpcy5hZGRDbGFzcyhKU09ORURJVE9SX0NMQVNTKTtcblxuICAgIHRoaXMuaGVhZGVyTm9kZSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIHRoaXMuaGVhZGVyTm9kZS5jbGFzc05hbWUgPSBIRUFERVJfQ0xBU1M7XG5cbiAgICB0aGlzLnJldmVydEJ1dHRvbk5vZGUgPSB1bmRvSWNvbi5lbGVtZW50KHtcbiAgICAgIHRhZzogJ3NwYW4nLFxuICAgICAgdGl0bGU6IHRoaXMuX3RyYW5zLl9fKCdSZXZlcnQgY2hhbmdlcyB0byBkYXRhJylcbiAgICB9KTtcblxuICAgIHRoaXMuY29tbWl0QnV0dG9uTm9kZSA9IGNoZWNrSWNvbi5lbGVtZW50KHtcbiAgICAgIHRhZzogJ3NwYW4nLFxuICAgICAgdGl0bGU6IHRoaXMuX3RyYW5zLl9fKCdDb21taXQgY2hhbmdlcyB0byBkYXRhJyksXG4gICAgICBtYXJnaW5MZWZ0OiAnOHB4J1xuICAgIH0pO1xuXG4gICAgdGhpcy5lZGl0b3JIb3N0Tm9kZSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIHRoaXMuZWRpdG9ySG9zdE5vZGUuY2xhc3NOYW1lID0gSE9TVF9DTEFTUztcblxuICAgIHRoaXMuaGVhZGVyTm9kZS5hcHBlbmRDaGlsZCh0aGlzLnJldmVydEJ1dHRvbk5vZGUpO1xuICAgIHRoaXMuaGVhZGVyTm9kZS5hcHBlbmRDaGlsZCh0aGlzLmNvbW1pdEJ1dHRvbk5vZGUpO1xuXG4gICAgdGhpcy5ub2RlLmFwcGVuZENoaWxkKHRoaXMuaGVhZGVyTm9kZSk7XG4gICAgdGhpcy5ub2RlLmFwcGVuZENoaWxkKHRoaXMuZWRpdG9ySG9zdE5vZGUpO1xuXG4gICAgY29uc3QgbW9kZWwgPSBuZXcgQ29kZUVkaXRvci5Nb2RlbCgpO1xuXG4gICAgbW9kZWwudmFsdWUudGV4dCA9IHRoaXMuX3RyYW5zLl9fKCdObyBkYXRhIScpO1xuICAgIG1vZGVsLm1pbWVUeXBlID0gJ2FwcGxpY2F0aW9uL2pzb24nO1xuICAgIG1vZGVsLnZhbHVlLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vblZhbHVlQ2hhbmdlZCwgdGhpcyk7XG4gICAgdGhpcy5tb2RlbCA9IG1vZGVsO1xuICAgIHRoaXMuZWRpdG9yID0gb3B0aW9ucy5lZGl0b3JGYWN0b3J5KHsgaG9zdDogdGhpcy5lZGl0b3JIb3N0Tm9kZSwgbW9kZWwgfSk7XG4gICAgdGhpcy5lZGl0b3Iuc2V0T3B0aW9uKCdyZWFkT25seScsIHRydWUpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb2RlIGVkaXRvciB1c2VkIGJ5IHRoZSBlZGl0b3IuXG4gICAqL1xuICByZWFkb25seSBlZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvcjtcblxuICAvKipcbiAgICogVGhlIGNvZGUgZWRpdG9yIG1vZGVsIHVzZWQgYnkgdGhlIGVkaXRvci5cbiAgICovXG4gIHJlYWRvbmx5IG1vZGVsOiBDb2RlRWRpdG9yLklNb2RlbDtcblxuICAvKipcbiAgICogVGhlIGVkaXRvciBob3N0IG5vZGUgdXNlZCBieSB0aGUgSlNPTiBlZGl0b3IuXG4gICAqL1xuICByZWFkb25seSBoZWFkZXJOb2RlOiBIVE1MRGl2RWxlbWVudDtcblxuICAvKipcbiAgICogVGhlIGVkaXRvciBob3N0IG5vZGUgdXNlZCBieSB0aGUgSlNPTiBlZGl0b3IuXG4gICAqL1xuICByZWFkb25seSBlZGl0b3JIb3N0Tm9kZTogSFRNTERpdkVsZW1lbnQ7XG5cbiAgLyoqXG4gICAqIFRoZSByZXZlcnQgYnV0dG9uIHVzZWQgYnkgdGhlIEpTT04gZWRpdG9yLlxuICAgKi9cbiAgcmVhZG9ubHkgcmV2ZXJ0QnV0dG9uTm9kZTogSFRNTFNwYW5FbGVtZW50O1xuXG4gIC8qKlxuICAgKiBUaGUgY29tbWl0IGJ1dHRvbiB1c2VkIGJ5IHRoZSBKU09OIGVkaXRvci5cbiAgICovXG4gIHJlYWRvbmx5IGNvbW1pdEJ1dHRvbk5vZGU6IEhUTUxTcGFuRWxlbWVudDtcblxuICAvKipcbiAgICogVGhlIG9ic2VydmFibGUgc291cmNlLlxuICAgKi9cbiAgZ2V0IHNvdXJjZSgpOiBJT2JzZXJ2YWJsZUpTT04gfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fc291cmNlO1xuICB9XG4gIHNldCBzb3VyY2UodmFsdWU6IElPYnNlcnZhYmxlSlNPTiB8IG51bGwpIHtcbiAgICBpZiAodGhpcy5fc291cmNlID09PSB2YWx1ZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBpZiAodGhpcy5fc291cmNlKSB7XG4gICAgICB0aGlzLl9zb3VyY2UuY2hhbmdlZC5kaXNjb25uZWN0KHRoaXMuX29uU291cmNlQ2hhbmdlZCwgdGhpcyk7XG4gICAgfVxuICAgIHRoaXMuX3NvdXJjZSA9IHZhbHVlO1xuICAgIHRoaXMuZWRpdG9yLnNldE9wdGlvbigncmVhZE9ubHknLCB2YWx1ZSA9PT0gbnVsbCk7XG4gICAgaWYgKHZhbHVlKSB7XG4gICAgICB2YWx1ZS5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25Tb3VyY2VDaGFuZ2VkLCB0aGlzKTtcbiAgICB9XG4gICAgdGhpcy5fc2V0VmFsdWUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgd2hldGhlciB0aGUgZWRpdG9yIGlzIGRpcnR5LlxuICAgKi9cbiAgZ2V0IGlzRGlydHkoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2RhdGFEaXJ0eSB8fCB0aGlzLl9pbnB1dERpcnR5O1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgRE9NIGV2ZW50cyBmb3IgdGhlIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIGV2ZW50IC0gVGhlIERPTSBldmVudCBzZW50IHRvIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgaW1wbGVtZW50cyB0aGUgRE9NIGBFdmVudExpc3RlbmVyYCBpbnRlcmZhY2UgYW5kIGlzXG4gICAqIGNhbGxlZCBpbiByZXNwb25zZSB0byBldmVudHMgb24gdGhlIG5vdGVib29rIHBhbmVsJ3Mgbm9kZS4gSXQgc2hvdWxkXG4gICAqIG5vdCBiZSBjYWxsZWQgZGlyZWN0bHkgYnkgdXNlciBjb2RlLlxuICAgKi9cbiAgaGFuZGxlRXZlbnQoZXZlbnQ6IEV2ZW50KTogdm9pZCB7XG4gICAgc3dpdGNoIChldmVudC50eXBlKSB7XG4gICAgICBjYXNlICdibHVyJzpcbiAgICAgICAgdGhpcy5fZXZ0Qmx1cihldmVudCBhcyBGb2N1c0V2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdjbGljayc6XG4gICAgICAgIHRoaXMuX2V2dENsaWNrKGV2ZW50IGFzIE1vdXNlRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGFmdGVyLWF0dGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBjb25zdCBub2RlID0gdGhpcy5lZGl0b3JIb3N0Tm9kZTtcbiAgICBub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2JsdXInLCB0aGlzLCB0cnVlKTtcbiAgICBub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcywgdHJ1ZSk7XG4gICAgdGhpcy5yZXZlcnRCdXR0b25Ob2RlLmhpZGRlbiA9IHRydWU7XG4gICAgdGhpcy5jb21taXRCdXR0b25Ob2RlLmhpZGRlbiA9IHRydWU7XG4gICAgdGhpcy5oZWFkZXJOb2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcyk7XG4gICAgaWYgKHRoaXMuaXNWaXNpYmxlKSB7XG4gICAgICB0aGlzLnVwZGF0ZSgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGFmdGVyLXNob3dgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJTaG93KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGB1cGRhdGUtcmVxdWVzdGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25VcGRhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHRoaXMuZWRpdG9yLnJlZnJlc2goKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGJlZm9yZS1kZXRhY2hgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQmVmb3JlRGV0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGNvbnN0IG5vZGUgPSB0aGlzLmVkaXRvckhvc3ROb2RlO1xuICAgIG5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignYmx1cicsIHRoaXMsIHRydWUpO1xuICAgIG5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignY2xpY2snLCB0aGlzLCB0cnVlKTtcbiAgICB0aGlzLmhlYWRlck5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignY2xpY2snLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIG1ldGFkYXRhIG9mIHRoZSBzb3VyY2UuXG4gICAqL1xuICBwcml2YXRlIF9vblNvdXJjZUNoYW5nZWQoXG4gICAgc2VuZGVyOiBJT2JzZXJ2YWJsZUpTT04sXG4gICAgYXJnczogSU9ic2VydmFibGVKU09OLklDaGFuZ2VkQXJnc1xuICApIHtcbiAgICBpZiAodGhpcy5fY2hhbmdlR3VhcmQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgaWYgKHRoaXMuX2lucHV0RGlydHkgfHwgdGhpcy5lZGl0b3IuaGFzRm9jdXMoKSkge1xuICAgICAgdGhpcy5fZGF0YURpcnR5ID0gdHJ1ZTtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5fc2V0VmFsdWUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgY2hhbmdlIGV2ZW50cy5cbiAgICovXG4gIHByaXZhdGUgX29uVmFsdWVDaGFuZ2VkKCk6IHZvaWQge1xuICAgIGxldCB2YWxpZCA9IHRydWU7XG4gICAgdHJ5IHtcbiAgICAgIGNvbnN0IHZhbHVlID0gSlNPTi5wYXJzZSh0aGlzLmVkaXRvci5tb2RlbC52YWx1ZS50ZXh0KTtcbiAgICAgIHRoaXMucmVtb3ZlQ2xhc3MoRVJST1JfQ0xBU1MpO1xuICAgICAgdGhpcy5faW5wdXREaXJ0eSA9XG4gICAgICAgICF0aGlzLl9jaGFuZ2VHdWFyZCAmJiAhSlNPTkV4dC5kZWVwRXF1YWwodmFsdWUsIHRoaXMuX29yaWdpbmFsVmFsdWUpO1xuICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgdGhpcy5hZGRDbGFzcyhFUlJPUl9DTEFTUyk7XG4gICAgICB0aGlzLl9pbnB1dERpcnR5ID0gdHJ1ZTtcbiAgICAgIHZhbGlkID0gZmFsc2U7XG4gICAgfVxuICAgIHRoaXMucmV2ZXJ0QnV0dG9uTm9kZS5oaWRkZW4gPSAhdGhpcy5faW5wdXREaXJ0eTtcbiAgICB0aGlzLmNvbW1pdEJ1dHRvbk5vZGUuaGlkZGVuID0gIXZhbGlkIHx8ICF0aGlzLl9pbnB1dERpcnR5O1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBibHVyIGV2ZW50cyBmb3IgdGhlIHRleHQgYXJlYS5cbiAgICovXG4gIHByaXZhdGUgX2V2dEJsdXIoZXZlbnQ6IEZvY3VzRXZlbnQpOiB2b2lkIHtcbiAgICAvLyBVcGRhdGUgdGhlIG1ldGFkYXRhIGlmIG5lY2Vzc2FyeS5cbiAgICBpZiAoIXRoaXMuX2lucHV0RGlydHkgJiYgdGhpcy5fZGF0YURpcnR5KSB7XG4gICAgICB0aGlzLl9zZXRWYWx1ZSgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgY2xpY2sgZXZlbnRzIGZvciB0aGUgYnV0dG9ucy5cbiAgICovXG4gIHByaXZhdGUgX2V2dENsaWNrKGV2ZW50OiBNb3VzZUV2ZW50KTogdm9pZCB7XG4gICAgY29uc3QgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgIGlmICh0aGlzLnJldmVydEJ1dHRvbk5vZGUuY29udGFpbnModGFyZ2V0KSkge1xuICAgICAgdGhpcy5fc2V0VmFsdWUoKTtcbiAgICB9IGVsc2UgaWYgKHRoaXMuY29tbWl0QnV0dG9uTm9kZS5jb250YWlucyh0YXJnZXQpKSB7XG4gICAgICBpZiAoIXRoaXMuY29tbWl0QnV0dG9uTm9kZS5oaWRkZW4gJiYgIXRoaXMuaGFzQ2xhc3MoRVJST1JfQ0xBU1MpKSB7XG4gICAgICAgIHRoaXMuX2NoYW5nZUd1YXJkID0gdHJ1ZTtcbiAgICAgICAgdGhpcy5fbWVyZ2VDb250ZW50KCk7XG4gICAgICAgIHRoaXMuX2NoYW5nZUd1YXJkID0gZmFsc2U7XG4gICAgICAgIHRoaXMuX3NldFZhbHVlKCk7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmICh0aGlzLmVkaXRvckhvc3ROb2RlLmNvbnRhaW5zKHRhcmdldCkpIHtcbiAgICAgIHRoaXMuZWRpdG9yLmZvY3VzKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIE1lcmdlIHRoZSB1c2VyIGNvbnRlbnQuXG4gICAqL1xuICBwcml2YXRlIF9tZXJnZUNvbnRlbnQoKTogdm9pZCB7XG4gICAgY29uc3QgbW9kZWwgPSB0aGlzLmVkaXRvci5tb2RlbDtcbiAgICBjb25zdCBvbGQgPSB0aGlzLl9vcmlnaW5hbFZhbHVlO1xuICAgIGNvbnN0IHVzZXIgPSBKU09OLnBhcnNlKG1vZGVsLnZhbHVlLnRleHQpIGFzIEpTT05PYmplY3Q7XG4gICAgY29uc3Qgc291cmNlID0gdGhpcy5zb3VyY2U7XG4gICAgaWYgKCFzb3VyY2UpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBJZiBpdCBpcyBpbiB1c2VyIGFuZCBoYXMgY2hhbmdlZCBmcm9tIG9sZCwgc2V0IGluIG5ldy5cbiAgICBmb3IgKGNvbnN0IGtleSBpbiB1c2VyKSB7XG4gICAgICBpZiAoIUpTT05FeHQuZGVlcEVxdWFsKHVzZXJba2V5XSwgb2xkW2tleV0gfHwgbnVsbCkpIHtcbiAgICAgICAgc291cmNlLnNldChrZXksIHVzZXJba2V5XSk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgLy8gSWYgaXQgd2FzIGluIG9sZCBhbmQgaXMgbm90IGluIHVzZXIsIHJlbW92ZSBmcm9tIHNvdXJjZS5cbiAgICBmb3IgKGNvbnN0IGtleSBpbiBvbGQpIHtcbiAgICAgIGlmICghKGtleSBpbiB1c2VyKSkge1xuICAgICAgICBzb3VyY2UuZGVsZXRlKGtleSk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgdmFsdWUgZ2l2ZW4gdGhlIG93bmVyIGNvbnRlbnRzLlxuICAgKi9cbiAgcHJpdmF0ZSBfc2V0VmFsdWUoKTogdm9pZCB7XG4gICAgdGhpcy5fZGF0YURpcnR5ID0gZmFsc2U7XG4gICAgdGhpcy5faW5wdXREaXJ0eSA9IGZhbHNlO1xuICAgIHRoaXMucmV2ZXJ0QnV0dG9uTm9kZS5oaWRkZW4gPSB0cnVlO1xuICAgIHRoaXMuY29tbWl0QnV0dG9uTm9kZS5oaWRkZW4gPSB0cnVlO1xuICAgIHRoaXMucmVtb3ZlQ2xhc3MoRVJST1JfQ0xBU1MpO1xuICAgIGNvbnN0IG1vZGVsID0gdGhpcy5lZGl0b3IubW9kZWw7XG4gICAgY29uc3QgY29udGVudCA9IHRoaXMuX3NvdXJjZSA/IHRoaXMuX3NvdXJjZS50b0pTT04oKSA6IHt9O1xuICAgIHRoaXMuX2NoYW5nZUd1YXJkID0gdHJ1ZTtcbiAgICBpZiAoY29udGVudCA9PT0gdm9pZCAwKSB7XG4gICAgICBtb2RlbC52YWx1ZS50ZXh0ID0gdGhpcy5fdHJhbnMuX18oJ05vIGRhdGEhJyk7XG4gICAgICB0aGlzLl9vcmlnaW5hbFZhbHVlID0gSlNPTkV4dC5lbXB0eU9iamVjdDtcbiAgICB9IGVsc2Uge1xuICAgICAgY29uc3QgdmFsdWUgPSBKU09OLnN0cmluZ2lmeShjb250ZW50LCBudWxsLCA0KTtcbiAgICAgIG1vZGVsLnZhbHVlLnRleHQgPSB2YWx1ZTtcbiAgICAgIHRoaXMuX29yaWdpbmFsVmFsdWUgPSBjb250ZW50O1xuICAgICAgLy8gTW92ZSB0aGUgY3Vyc29yIHRvIHdpdGhpbiB0aGUgYnJhY2UuXG4gICAgICBpZiAodmFsdWUubGVuZ3RoID4gMSAmJiB2YWx1ZVswXSA9PT0gJ3snKSB7XG4gICAgICAgIHRoaXMuZWRpdG9yLnNldEN1cnNvclBvc2l0aW9uKHsgbGluZTogMCwgY29sdW1uOiAxIH0pO1xuICAgICAgfVxuICAgIH1cbiAgICB0aGlzLmVkaXRvci5yZWZyZXNoKCk7XG4gICAgdGhpcy5fY2hhbmdlR3VhcmQgPSBmYWxzZTtcbiAgICB0aGlzLmNvbW1pdEJ1dHRvbk5vZGUuaGlkZGVuID0gdHJ1ZTtcbiAgICB0aGlzLnJldmVydEJ1dHRvbk5vZGUuaGlkZGVuID0gdHJ1ZTtcbiAgfVxuXG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF9kYXRhRGlydHkgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfaW5wdXREaXJ0eSA9IGZhbHNlO1xuICBwcml2YXRlIF9zb3VyY2U6IElPYnNlcnZhYmxlSlNPTiB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9vcmlnaW5hbFZhbHVlOiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0ID0gSlNPTkV4dC5lbXB0eU9iamVjdDtcbiAgcHJpdmF0ZSBfY2hhbmdlR3VhcmQgPSBmYWxzZTtcbn1cblxuLyoqXG4gKiBUaGUgc3RhdGljIG5hbWVzcGFjZSBKU09ORWRpdG9yIGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSlNPTkVkaXRvciB7XG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB1c2VkIHRvIGluaXRpYWxpemUgYSBqc29uIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBlZGl0b3IgZmFjdG9yeSB1c2VkIGJ5IHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgZWRpdG9yRmFjdG9yeTogQ29kZUVkaXRvci5GYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGxhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIG5iZm9ybWF0IGZyb20gJ0BqdXB5dGVybGFiL25iZm9ybWF0JztcblxuLyoqXG4gKiBUaGUgbWltZSB0eXBlIHNlcnZpY2Ugb2YgYSBjb2RlIGVkaXRvci5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJRWRpdG9yTWltZVR5cGVTZXJ2aWNlIHtcbiAgLyoqXG4gICAqIEdldCBhIG1pbWUgdHlwZSBmb3IgdGhlIGdpdmVuIGxhbmd1YWdlIGluZm8uXG4gICAqXG4gICAqIEBwYXJhbSBpbmZvIC0gVGhlIGxhbmd1YWdlIGluZm9ybWF0aW9uLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHZhbGlkIG1pbWV0eXBlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIElmIGEgbWltZSB0eXBlIGNhbm5vdCBiZSBmb3VuZCByZXR1cm5zIHRoZSBkZWZhdWx0IG1pbWUgdHlwZSBgdGV4dC9wbGFpbmAsIG5ldmVyIGBudWxsYC5cbiAgICovXG4gIGdldE1pbWVUeXBlQnlMYW5ndWFnZShpbmZvOiBuYmZvcm1hdC5JTGFuZ3VhZ2VJbmZvTWV0YWRhdGEpOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIEdldCBhIG1pbWUgdHlwZSBmb3IgdGhlIGdpdmVuIGZpbGUgcGF0aC5cbiAgICpcbiAgICogQHBhcmFtIGZpbGVQYXRoIC0gVGhlIGZ1bGwgcGF0aCB0byB0aGUgZmlsZS5cbiAgICpcbiAgICogQHJldHVybnMgQSB2YWxpZCBtaW1ldHlwZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBJZiBhIG1pbWUgdHlwZSBjYW5ub3QgYmUgZm91bmQgcmV0dXJucyB0aGUgZGVmYXVsdCBtaW1lIHR5cGUgYHRleHQvcGxhaW5gLCBuZXZlciBgbnVsbGAuXG4gICAqL1xuICBnZXRNaW1lVHlwZUJ5RmlsZVBhdGgoZmlsZVBhdGg6IHN0cmluZyk6IHN0cmluZztcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYElFZGl0b3JNaW1lVHlwZVNlcnZpY2VgLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElFZGl0b3JNaW1lVHlwZVNlcnZpY2Uge1xuICAvKipcbiAgICogVGhlIGRlZmF1bHQgbWltZSB0eXBlLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRNaW1lVHlwZTogc3RyaW5nID0gJ3RleHQvcGxhaW4nO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElFZGl0b3JGYWN0b3J5U2VydmljZSB9IGZyb20gJy4vZmFjdG9yeSc7XG5pbXBvcnQgeyBJRWRpdG9yTWltZVR5cGVTZXJ2aWNlIH0gZnJvbSAnLi9taW1ldHlwZSc7XG5cbi8qIHRzbGludDpkaXNhYmxlICovXG4vKipcbiAqIENvZGUgZWRpdG9yIHNlcnZpY2VzIHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSUVkaXRvclNlcnZpY2VzID0gbmV3IFRva2VuPElFZGl0b3JTZXJ2aWNlcz4oXG4gICdAanVweXRlcmxhYi9jb2RlZWRpdG9yOklFZGl0b3JTZXJ2aWNlcydcbik7XG4vKiB0c2xpbnQ6ZW5hYmxlICovXG5cbi8qKlxuICogQ29kZSBlZGl0b3Igc2VydmljZXMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUVkaXRvclNlcnZpY2VzIHtcbiAgLyoqXG4gICAqIFRoZSBjb2RlIGVkaXRvciBmYWN0b3J5LlxuICAgKi9cbiAgcmVhZG9ubHkgZmFjdG9yeVNlcnZpY2U6IElFZGl0b3JGYWN0b3J5U2VydmljZTtcblxuICAvKipcbiAgICogVGhlIGVkaXRvciBtaW1lIHR5cGUgc2VydmljZS5cbiAgICovXG4gIHJlYWRvbmx5IG1pbWVUeXBlU2VydmljZTogSUVkaXRvck1pbWVUeXBlU2VydmljZTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgTWltZURhdGEgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJRHJhZ0V2ZW50IH0gZnJvbSAnQGx1bWluby9kcmFnZHJvcCc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IENvZGVFZGl0b3IgfSBmcm9tICcuLyc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYW4gZWRpdG9yIHdpZGdldCB0aGF0IGhhcyBhIHByaW1hcnkgc2VsZWN0aW9uLlxuICovXG5jb25zdCBIQVNfU0VMRUNUSU9OX0NMQVNTID0gJ2pwLW1vZC1oYXMtcHJpbWFyeS1zZWxlY3Rpb24nO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGFuIGVkaXRvciB3aWRnZXQgdGhhdCBoYXMgYSBjdXJzb3Ivc2VsZWN0aW9uXG4gKiB3aXRoaW4gdGhlIHdoaXRlc3BhY2UgYXQgdGhlIGJlZ2lubmluZyBvZiBhIGxpbmVcbiAqL1xuY29uc3QgSEFTX0lOX0xFQURJTkdfV0hJVEVTUEFDRV9DTEFTUyA9ICdqcC1tb2QtaW4tbGVhZGluZy13aGl0ZXNwYWNlJztcblxuLyoqXG4gKiBBIGNsYXNzIHVzZWQgdG8gaW5kaWNhdGUgYSBkcm9wIHRhcmdldC5cbiAqL1xuY29uc3QgRFJPUF9UQVJHRVRfQ0xBU1MgPSAnanAtbW9kLWRyb3BUYXJnZXQnO1xuXG4vKipcbiAqIFJlZ0V4cCB0byB0ZXN0IGZvciBsZWFkaW5nIHdoaXRlc3BhY2VcbiAqL1xuY29uc3QgbGVhZGluZ1doaXRlc3BhY2VSZSA9IC9eXFxzKyQvO1xuXG4vKipcbiAqIEEgd2lkZ2V0IHdoaWNoIGhvc3RzIGEgY29kZSBlZGl0b3IuXG4gKi9cbmV4cG9ydCBjbGFzcyBDb2RlRWRpdG9yV3JhcHBlciBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgY29kZSBlZGl0b3Igd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogQ29kZUVkaXRvcldyYXBwZXIuSU9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuICAgIGNvbnN0IGVkaXRvciA9ICh0aGlzLmVkaXRvciA9IG9wdGlvbnMuZmFjdG9yeSh7XG4gICAgICBob3N0OiB0aGlzLm5vZGUsXG4gICAgICBtb2RlbDogb3B0aW9ucy5tb2RlbCxcbiAgICAgIHV1aWQ6IG9wdGlvbnMudXVpZCxcbiAgICAgIGNvbmZpZzogb3B0aW9ucy5jb25maWcsXG4gICAgICBzZWxlY3Rpb25TdHlsZTogb3B0aW9ucy5zZWxlY3Rpb25TdHlsZVxuICAgIH0pKTtcbiAgICBlZGl0b3IubW9kZWwuc2VsZWN0aW9ucy5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25TZWxlY3Rpb25zQ2hhbmdlZCwgdGhpcyk7XG4gICAgdGhpcy5fdXBkYXRlT25TaG93ID0gb3B0aW9ucy51cGRhdGVPblNob3cgIT09IGZhbHNlO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgZWRpdG9yIHdyYXBwZWQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIHJlYWRvbmx5IGVkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yO1xuXG4gIC8qKlxuICAgKiBHZXQgdGhlIG1vZGVsIHVzZWQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIGdldCBtb2RlbCgpOiBDb2RlRWRpdG9yLklNb2RlbCB7XG4gICAgcmV0dXJuIHRoaXMuZWRpdG9yLm1vZGVsO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSB3aWRnZXQuXG4gICAqL1xuICBkaXNwb3NlKCkge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICAgIHRoaXMuZWRpdG9yLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIERPTSBldmVudHMgZm9yIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSBldmVudCAtIFRoZSBET00gZXZlbnQgc2VudCB0byB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgbWV0aG9kIGltcGxlbWVudHMgdGhlIERPTSBgRXZlbnRMaXN0ZW5lcmAgaW50ZXJmYWNlIGFuZCBpc1xuICAgKiBjYWxsZWQgaW4gcmVzcG9uc2UgdG8gZXZlbnRzIG9uIHRoZSBub3RlYm9vayBwYW5lbCdzIG5vZGUuIEl0IHNob3VsZFxuICAgKiBub3QgYmUgY2FsbGVkIGRpcmVjdGx5IGJ5IHVzZXIgY29kZS5cbiAgICovXG4gIGhhbmRsZUV2ZW50KGV2ZW50OiBFdmVudCk6IHZvaWQge1xuICAgIHN3aXRjaCAoZXZlbnQudHlwZSkge1xuICAgICAgY2FzZSAnbG0tZHJhZ2VudGVyJzpcbiAgICAgICAgdGhpcy5fZXZ0RHJhZ0VudGVyKGV2ZW50IGFzIElEcmFnRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2xtLWRyYWdsZWF2ZSc6XG4gICAgICAgIHRoaXMuX2V2dERyYWdMZWF2ZShldmVudCBhcyBJRHJhZ0V2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdsbS1kcmFnb3Zlcic6XG4gICAgICAgIHRoaXMuX2V2dERyYWdPdmVyKGV2ZW50IGFzIElEcmFnRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2xtLWRyb3AnOlxuICAgICAgICB0aGlzLl9ldnREcm9wKGV2ZW50IGFzIElEcmFnRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhY3RpdmF0ZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5lZGl0b3IuZm9jdXMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIG1lc3NhZ2UgaGFuZGxlciBpbnZva2VkIG9uIGFuIGAnYWZ0ZXItYXR0YWNoJ2AgbWVzc2FnZS5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFmdGVyQXR0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHN1cGVyLm9uQWZ0ZXJBdHRhY2gobXNnKTtcbiAgICBjb25zdCBub2RlID0gdGhpcy5ub2RlO1xuICAgIG5vZGUuYWRkRXZlbnRMaXN0ZW5lcignbG0tZHJhZ2VudGVyJywgdGhpcyk7XG4gICAgbm9kZS5hZGRFdmVudExpc3RlbmVyKCdsbS1kcmFnbGVhdmUnLCB0aGlzKTtcbiAgICBub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2xtLWRyYWdvdmVyJywgdGhpcyk7XG4gICAgbm9kZS5hZGRFdmVudExpc3RlbmVyKCdsbS1kcm9wJywgdGhpcyk7XG4gICAgLy8gV2UgaGF2ZSB0byByZWZyZXNoIGF0IGxlYXN0IG9uY2UgYWZ0ZXIgYXR0YWNoaW5nLFxuICAgIC8vIHdoaWxlIHZpc2libGUuXG4gICAgdGhpcy5faGFzUmVmcmVzaGVkU2luY2VBdHRhY2ggPSBmYWxzZTtcbiAgICBpZiAodGhpcy5pc1Zpc2libGUpIHtcbiAgICAgIHRoaXMudXBkYXRlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYmVmb3JlLWRldGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgY29uc3Qgbm9kZSA9IHRoaXMubm9kZTtcbiAgICBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2xtLWRyYWdlbnRlcicsIHRoaXMpO1xuICAgIG5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignbG0tZHJhZ2xlYXZlJywgdGhpcyk7XG4gICAgbm9kZS5yZW1vdmVFdmVudExpc3RlbmVyKCdsbS1kcmFnb3ZlcicsIHRoaXMpO1xuICAgIG5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignbG0tZHJvcCcsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgbWVzc2FnZSBoYW5kbGVyIGludm9rZWQgb24gYW4gYCdhZnRlci1zaG93J2AgbWVzc2FnZS5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFmdGVyU2hvdyhtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fdXBkYXRlT25TaG93IHx8ICF0aGlzLl9oYXNSZWZyZXNoZWRTaW5jZUF0dGFjaCkge1xuICAgICAgdGhpcy51cGRhdGUoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQSBtZXNzYWdlIGhhbmRsZXIgaW52b2tlZCBvbiBhIGAncmVzaXplJ2AgbWVzc2FnZS5cbiAgICovXG4gIHByb3RlY3RlZCBvblJlc2l6ZShtc2c6IFdpZGdldC5SZXNpemVNZXNzYWdlKTogdm9pZCB7XG4gICAgaWYgKG1zZy53aWR0aCA+PSAwICYmIG1zZy5oZWlnaHQgPj0gMCkge1xuICAgICAgdGhpcy5lZGl0b3Iuc2V0U2l6ZShtc2cpO1xuICAgIH0gZWxzZSBpZiAodGhpcy5pc1Zpc2libGUpIHtcbiAgICAgIHRoaXMuZWRpdG9yLnJlc2l6ZVRvRml0KCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEEgbWVzc2FnZSBoYW5kbGVyIGludm9rZWQgb24gYW4gYCd1cGRhdGUtcmVxdWVzdCdgIG1lc3NhZ2UuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25VcGRhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzVmlzaWJsZSkge1xuICAgICAgdGhpcy5faGFzUmVmcmVzaGVkU2luY2VBdHRhY2ggPSB0cnVlO1xuICAgICAgdGhpcy5lZGl0b3IucmVmcmVzaCgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgaW4gbW9kZWwgc2VsZWN0aW9ucy5cbiAgICovXG4gIHByaXZhdGUgX29uU2VsZWN0aW9uc0NoYW5nZWQoKTogdm9pZCB7XG4gICAgY29uc3QgeyBzdGFydCwgZW5kIH0gPSB0aGlzLmVkaXRvci5nZXRTZWxlY3Rpb24oKTtcblxuICAgIGlmIChzdGFydC5jb2x1bW4gIT09IGVuZC5jb2x1bW4gfHwgc3RhcnQubGluZSAhPT0gZW5kLmxpbmUpIHtcbiAgICAgIC8vIGEgc2VsZWN0aW9uIHdhcyBtYWRlXG4gICAgICB0aGlzLmFkZENsYXNzKEhBU19TRUxFQ1RJT05fQ0xBU1MpO1xuICAgICAgdGhpcy5yZW1vdmVDbGFzcyhIQVNfSU5fTEVBRElOR19XSElURVNQQUNFX0NMQVNTKTtcbiAgICB9IGVsc2Uge1xuICAgICAgLy8gdGhlIGN1cnNvciB3YXMgcGxhY2VkXG4gICAgICB0aGlzLnJlbW92ZUNsYXNzKEhBU19TRUxFQ1RJT05fQ0xBU1MpO1xuXG4gICAgICBpZiAoXG4gICAgICAgIHRoaXMuZWRpdG9yXG4gICAgICAgICAgLmdldExpbmUoZW5kLmxpbmUpIVxuICAgICAgICAgIC5zbGljZSgwLCBlbmQuY29sdW1uKVxuICAgICAgICAgIC5tYXRjaChsZWFkaW5nV2hpdGVzcGFjZVJlKVxuICAgICAgKSB7XG4gICAgICAgIHRoaXMuYWRkQ2xhc3MoSEFTX0lOX0xFQURJTkdfV0hJVEVTUEFDRV9DTEFTUyk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLnJlbW92ZUNsYXNzKEhBU19JTl9MRUFESU5HX1dISVRFU1BBQ0VfQ0xBU1MpO1xuICAgICAgfVxuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGAnbG0tZHJhZ2VudGVyJ2AgZXZlbnQgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9ldnREcmFnRW50ZXIoZXZlbnQ6IElEcmFnRXZlbnQpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5lZGl0b3IuZ2V0T3B0aW9uKCdyZWFkT25seScpID09PSB0cnVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IGRhdGEgPSBQcml2YXRlLmZpbmRUZXh0RGF0YShldmVudC5taW1lRGF0YSk7XG4gICAgaWYgKGRhdGEgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgIGV2ZW50LnN0b3BQcm9wYWdhdGlvbigpO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLW1vZC1kcm9wVGFyZ2V0Jyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBgJ2xtLWRyYWdsZWF2ZSdgIGV2ZW50IGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0RHJhZ0xlYXZlKGV2ZW50OiBJRHJhZ0V2ZW50KTogdm9pZCB7XG4gICAgdGhpcy5yZW1vdmVDbGFzcyhEUk9QX1RBUkdFVF9DTEFTUyk7XG4gICAgaWYgKHRoaXMuZWRpdG9yLmdldE9wdGlvbigncmVhZE9ubHknKSA9PT0gdHJ1ZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBkYXRhID0gUHJpdmF0ZS5maW5kVGV4dERhdGEoZXZlbnQubWltZURhdGEpO1xuICAgIGlmIChkYXRhID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcbiAgICBldmVudC5zdG9wUHJvcGFnYXRpb24oKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGAnbG0tZHJhZ292ZXInYCBldmVudCBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByaXZhdGUgX2V2dERyYWdPdmVyKGV2ZW50OiBJRHJhZ0V2ZW50KTogdm9pZCB7XG4gICAgdGhpcy5yZW1vdmVDbGFzcyhEUk9QX1RBUkdFVF9DTEFTUyk7XG4gICAgaWYgKHRoaXMuZWRpdG9yLmdldE9wdGlvbigncmVhZE9ubHknKSA9PT0gdHJ1ZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBkYXRhID0gUHJpdmF0ZS5maW5kVGV4dERhdGEoZXZlbnQubWltZURhdGEpO1xuICAgIGlmIChkYXRhID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcbiAgICBldmVudC5zdG9wUHJvcGFnYXRpb24oKTtcbiAgICBldmVudC5kcm9wQWN0aW9uID0gJ2NvcHknO1xuICAgIHRoaXMuYWRkQ2xhc3MoRFJPUF9UQVJHRVRfQ0xBU1MpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgYCdsbS1kcm9wJ2AgZXZlbnQgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9ldnREcm9wKGV2ZW50OiBJRHJhZ0V2ZW50KTogdm9pZCB7XG4gICAgaWYgKHRoaXMuZWRpdG9yLmdldE9wdGlvbigncmVhZE9ubHknKSA9PT0gdHJ1ZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBkYXRhID0gUHJpdmF0ZS5maW5kVGV4dERhdGEoZXZlbnQubWltZURhdGEpO1xuICAgIGlmIChkYXRhID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgY29vcmRpbmF0ZSA9IHtcbiAgICAgIHRvcDogZXZlbnQueSxcbiAgICAgIGJvdHRvbTogZXZlbnQueSxcbiAgICAgIGxlZnQ6IGV2ZW50LngsXG4gICAgICByaWdodDogZXZlbnQueCxcbiAgICAgIHg6IGV2ZW50LngsXG4gICAgICB5OiBldmVudC55LFxuICAgICAgd2lkdGg6IDAsXG4gICAgICBoZWlnaHQ6IDBcbiAgICB9O1xuICAgIGNvbnN0IHBvc2l0aW9uID0gdGhpcy5lZGl0b3IuZ2V0UG9zaXRpb25Gb3JDb29yZGluYXRlKGNvb3JkaW5hdGUpO1xuICAgIGlmIChwb3NpdGlvbiA9PT0gbnVsbCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLnJlbW92ZUNsYXNzKERST1BfVEFSR0VUX0NMQVNTKTtcbiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgIGV2ZW50LnN0b3BQcm9wYWdhdGlvbigpO1xuICAgIGlmIChldmVudC5wcm9wb3NlZEFjdGlvbiA9PT0gJ25vbmUnKSB7XG4gICAgICBldmVudC5kcm9wQWN0aW9uID0gJ25vbmUnO1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBvZmZzZXQgPSB0aGlzLmVkaXRvci5nZXRPZmZzZXRBdChwb3NpdGlvbik7XG4gICAgdGhpcy5tb2RlbC52YWx1ZS5pbnNlcnQob2Zmc2V0LCBkYXRhKTtcbiAgfVxuXG4gIHByaXZhdGUgX3VwZGF0ZU9uU2hvdzogYm9vbGVhbjtcbiAgcHJpdmF0ZSBfaGFzUmVmcmVzaGVkU2luY2VBdHRhY2ggPSBmYWxzZTtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciB0aGUgYENvZGVFZGl0b3JXcmFwcGVyYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIENvZGVFZGl0b3JXcmFwcGVyIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gaW5pdGlhbGl6ZSBhIGNvZGUgZWRpdG9yIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIEEgY29kZSBlZGl0b3IgZmFjdG9yeS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGUgd2lkZ2V0IG5lZWRzIGEgZmFjdG9yeSBhbmQgYSBtb2RlbCBpbnN0ZWFkIG9mIGEgYENvZGVFZGl0b3IuSUVkaXRvcmBcbiAgICAgKiBvYmplY3QgYmVjYXVzZSBpdCBuZWVkcyB0byBwcm92aWRlIGl0cyBvd24gbm9kZSBhcyB0aGUgaG9zdC5cbiAgICAgKi9cbiAgICBmYWN0b3J5OiBDb2RlRWRpdG9yLkZhY3Rvcnk7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbW9kZWwgdXNlZCB0byBpbml0aWFsaXplIHRoZSBjb2RlIGVkaXRvci5cbiAgICAgKi9cbiAgICBtb2RlbDogQ29kZUVkaXRvci5JTW9kZWw7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZGVzaXJlZCB1dWlkIGZvciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIHV1aWQ/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29uZmlndXJhdGlvbiBvcHRpb25zIGZvciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIGNvbmZpZz86IFBhcnRpYWw8Q29kZUVkaXRvci5JQ29uZmlnPjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBkZWZhdWx0IHNlbGVjdGlvbiBzdHlsZSBmb3IgdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICBzZWxlY3Rpb25TdHlsZT86IENvZGVFZGl0b3IuSVNlbGVjdGlvblN0eWxlO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byBzZW5kIGFuIHVwZGF0ZSByZXF1ZXN0IHRvIHRoZSBlZGl0b3Igd2hlbiBpdCBpcyBzaG93bi5cbiAgICAgKi9cbiAgICB1cGRhdGVPblNob3c/OiBib29sZWFuO1xuICB9XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZnVuY3Rpb25hbGl0eS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogR2l2ZW4gYSBNaW1lRGF0YSBpbnN0YW5jZSwgZXh0cmFjdCB0aGUgZmlyc3QgdGV4dCBkYXRhLCBpZiBhbnkuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZmluZFRleHREYXRhKG1pbWU6IE1pbWVEYXRhKTogc3RyaW5nIHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCB0eXBlcyA9IG1pbWUudHlwZXMoKTtcbiAgICBjb25zdCB0ZXh0VHlwZSA9IHR5cGVzLmZpbmQodCA9PiB0LmluZGV4T2YoJ3RleHQnKSA9PT0gMCk7XG4gICAgaWYgKHRleHRUeXBlID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybiB1bmRlZmluZWQ7XG4gICAgfVxuICAgIHJldHVybiBtaW1lLmdldERhdGEodGV4dFR5cGUpIGFzIHN0cmluZztcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==