(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_shared-models_lib_index_js"],{

/***/ "../packages/shared-models/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/shared-models/lib/index.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "YBaseCell": () => (/* reexport safe */ _ymodels__WEBPACK_IMPORTED_MODULE_0__.YBaseCell),
/* harmony export */   "YCodeCell": () => (/* reexport safe */ _ymodels__WEBPACK_IMPORTED_MODULE_0__.YCodeCell),
/* harmony export */   "YDocument": () => (/* reexport safe */ _ymodels__WEBPACK_IMPORTED_MODULE_0__.YDocument),
/* harmony export */   "YFile": () => (/* reexport safe */ _ymodels__WEBPACK_IMPORTED_MODULE_0__.YFile),
/* harmony export */   "YMarkdownCell": () => (/* reexport safe */ _ymodels__WEBPACK_IMPORTED_MODULE_0__.YMarkdownCell),
/* harmony export */   "YNotebook": () => (/* reexport safe */ _ymodels__WEBPACK_IMPORTED_MODULE_0__.YNotebook),
/* harmony export */   "YRawCell": () => (/* reexport safe */ _ymodels__WEBPACK_IMPORTED_MODULE_0__.YRawCell),
/* harmony export */   "createCellFromType": () => (/* reexport safe */ _ymodels__WEBPACK_IMPORTED_MODULE_0__.createCellFromType),
/* harmony export */   "createStandaloneCell": () => (/* reexport safe */ _ymodels__WEBPACK_IMPORTED_MODULE_0__.createStandaloneCell),
/* harmony export */   "convertYMapEventToMapChange": () => (/* reexport safe */ _utils__WEBPACK_IMPORTED_MODULE_1__.convertYMapEventToMapChange),
/* harmony export */   "createMutex": () => (/* reexport safe */ _utils__WEBPACK_IMPORTED_MODULE_1__.createMutex)
/* harmony export */ });
/* harmony import */ var _ymodels__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ymodels */ "../packages/shared-models/lib/ymodels.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils */ "../packages/shared-models/lib/utils.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module shared-models
 */





/***/ }),

/***/ "../packages/shared-models/lib/utils.js":
/*!**********************************************!*\
  !*** ../packages/shared-models/lib/utils.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "convertYMapEventToMapChange": () => (/* binding */ convertYMapEventToMapChange),
/* harmony export */   "createMutex": () => (/* binding */ createMutex)
/* harmony export */ });
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
function convertYMapEventToMapChange(event) {
    let changes = new Map();
    event.changes.keys.forEach((event, key) => {
        changes.set(key, {
            action: event.action,
            oldValue: event.oldValue,
            newValue: this.ymeta.get(key)
        });
    });
    return changes;
}
/**
 * Creates a mutual exclude function with the following property:
 *
 * ```js
 * const mutex = createMutex()
 * mutex(() => {
 *   // This function is immediately executed
 *   mutex(() => {
 *     // This function is not executed, as the mutex is already active.
 *   })
 * })
 * ```
 */
const createMutex = () => {
    let token = true;
    return (f) => {
        if (token) {
            token = false;
            try {
                f();
            }
            finally {
                token = true;
            }
        }
    };
};


/***/ }),

/***/ "../packages/shared-models/lib/ymodels.js":
/*!************************************************!*\
  !*** ../packages/shared-models/lib/ymodels.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "YDocument": () => (/* binding */ YDocument),
/* harmony export */   "YFile": () => (/* binding */ YFile),
/* harmony export */   "YNotebook": () => (/* binding */ YNotebook),
/* harmony export */   "createCellFromType": () => (/* binding */ createCellFromType),
/* harmony export */   "createStandaloneCell": () => (/* binding */ createStandaloneCell),
/* harmony export */   "YBaseCell": () => (/* binding */ YBaseCell),
/* harmony export */   "YCodeCell": () => (/* binding */ YCodeCell),
/* harmony export */   "YRawCell": () => (/* binding */ YRawCell),
/* harmony export */   "YMarkdownCell": () => (/* binding */ YMarkdownCell),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var y_protocols_awareness__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! y-protocols/awareness */ "../node_modules/y-protocols/awareness.js");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




const deepCopy = (o) => JSON.parse(JSON.stringify(o));
class YDocument {
    constructor() {
        this.isDisposed = false;
        this.ydoc = new yjs__WEBPACK_IMPORTED_MODULE_3__.Doc();
        this.source = this.ydoc.getText('source');
        this.ystate = this.ydoc.getMap('state');
        this.undoManager = new yjs__WEBPACK_IMPORTED_MODULE_3__.UndoManager([this.source], {
            trackedOrigins: new Set([this])
        });
        this.awareness = new y_protocols_awareness__WEBPACK_IMPORTED_MODULE_2__.Awareness(this.ydoc);
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
    }
    get dirty() {
        return this.ystate.get('dirty');
    }
    set dirty(value) {
        this.transact(() => {
            this.ystate.set('dirty', value);
        }, false);
    }
    /**
     * Perform a transaction. While the function f is called, all changes to the shared
     * document are bundled into a single event.
     */
    transact(f, undoable = true) {
        this.ydoc.transact(f, undoable ? this : null);
    }
    /**
     * Dispose of the resources.
     */
    dispose() {
        this.isDisposed = true;
        this.ydoc.destroy();
    }
    /**
     * Whether the object can undo changes.
     */
    canUndo() {
        return this.undoManager.undoStack.length > 0;
    }
    /**
     * Whether the object can redo changes.
     */
    canRedo() {
        return this.undoManager.redoStack.length > 0;
    }
    /**
     * Undo an operation.
     */
    undo() {
        this.undoManager.undo();
    }
    /**
     * Redo an operation.
     */
    redo() {
        this.undoManager.redo();
    }
    /**
     * Clear the change stack.
     */
    clearUndoHistory() {
        this.undoManager.clear();
    }
    /**
     * The changed signal.
     */
    get changed() {
        return this._changed;
    }
}
class YFile extends YDocument {
    constructor() {
        super();
        /**
         * Handle a change to the ymodel.
         */
        this._modelObserver = (event) => {
            const changes = {};
            changes.sourceChange = event.changes.delta;
            this._changed.emit(changes);
        };
        /**
         * Handle a change to the ystate.
         */
        this._onStateChanged = (event) => {
            const stateChange = [];
            event.keysChanged.forEach(key => {
                const change = event.changes.keys.get(key);
                if (change) {
                    stateChange.push({
                        name: key,
                        oldValue: change.oldValue,
                        newValue: this.ystate.get(key)
                    });
                }
            });
            this._changed.emit({ stateChange });
        };
        this.ysource = this.ydoc.getText('source');
        this.ysource.observe(this._modelObserver);
        this.ystate.observe(this._onStateChanged);
    }
    /**
     * Dispose of the resources.
     */
    dispose() {
        this.ysource.unobserve(this._modelObserver);
        this.ystate.unobserve(this._onStateChanged);
    }
    static create() {
        return new YFile();
    }
    /**
     * Gets cell's source.
     *
     * @returns Cell's source.
     */
    getSource() {
        return this.ysource.toString();
    }
    /**
     * Sets cell's source.
     *
     * @param value: New source.
     */
    setSource(value) {
        this.transact(() => {
            const ytext = this.ysource;
            ytext.delete(0, ytext.length);
            ytext.insert(0, value);
        });
    }
    /**
     * Replace content from `start' to `end` with `value`.
     *
     * @param start: The start index of the range to replace (inclusive).
     *
     * @param end: The end index of the range to replace (exclusive).
     *
     * @param value: New source (optional).
     */
    updateSource(start, end, value = '') {
        this.transact(() => {
            const ysource = this.ysource;
            // insert and then delete.
            // This ensures that the cursor position is adjusted after the replaced content.
            ysource.insert(start, value);
            ysource.delete(start + value.length, end - start);
        });
    }
}
/**
 * Shared implementation of the Shared Document types.
 *
 * Shared cells can be inserted into a SharedNotebook.
 * Shared cells only start emitting events when they are connected to a SharedNotebook.
 *
 * "Standalone" cells must not be inserted into a (Shared)Notebook.
 * Standalone cells emit events immediately after they have been created, but they must not
 * be included into a (Shared)Notebook.
 */
class YNotebook extends YDocument {
    constructor(options) {
        super();
        /**
         * Handle a change to the list of cells.
         */
        this._onYCellsChanged = (event) => {
            // update the type⇔cell mapping by iterating through the added/removed types
            event.changes.added.forEach(item => {
                const type = item.content.type;
                if (!this._ycellMapping.has(type)) {
                    this._ycellMapping.set(type, createCellFromType(type));
                }
                const cell = this._ycellMapping.get(type);
                cell._notebook = this;
                if (!this.disableDocumentWideUndoRedo) {
                    cell._undoManager = this.undoManager;
                }
                else {
                    cell._undoManager = new yjs__WEBPACK_IMPORTED_MODULE_3__.UndoManager([cell.ymodel], {});
                }
            });
            event.changes.deleted.forEach(item => {
                const type = item.content.type;
                const model = this._ycellMapping.get(type);
                if (model) {
                    model.dispose();
                    this._ycellMapping.delete(type);
                }
            });
            let index = 0;
            // this reflects the event.changes.delta, but replaces the content of delta.insert with ycells
            const cellsChange = [];
            event.changes.delta.forEach((d) => {
                if (d.insert != null) {
                    const insertedCells = d.insert.map((ycell) => this._ycellMapping.get(ycell));
                    cellsChange.push({ insert: insertedCells });
                    this.cells.splice(index, 0, ...insertedCells);
                    index += d.insert.length;
                }
                else if (d.delete != null) {
                    cellsChange.push(d);
                    this.cells.splice(index, d.delete);
                }
                else if (d.retain != null) {
                    cellsChange.push(d);
                    index += d.retain;
                }
            });
            this._changed.emit({
                cellsChange: cellsChange
            });
        };
        /**
         * Handle a change to the ystate.
         */
        this._onMetadataChanged = (event) => {
            if (event.keysChanged.has('metadata')) {
                const change = event.changes.keys.get('metadata');
                const metadataChange = {
                    oldValue: (change === null || change === void 0 ? void 0 : change.oldValue) ? change.oldValue : undefined,
                    newValue: this.getMetadata()
                };
                this._changed.emit({ metadataChange });
            }
        };
        /**
         * Handle a change to the ystate.
         */
        this._onStateChanged = (event) => {
            const stateChange = [];
            event.keysChanged.forEach(key => {
                const change = event.changes.keys.get(key);
                if (change) {
                    stateChange.push({
                        name: key,
                        oldValue: change.oldValue,
                        newValue: this.ystate.get(key)
                    });
                }
            });
            this._changed.emit({ stateChange });
        };
        this.ycells = this.ydoc.getArray('cells');
        this.ymeta = this.ydoc.getMap('meta');
        this.ymodel = this.ydoc.getMap('model');
        this.undoManager = new yjs__WEBPACK_IMPORTED_MODULE_3__.UndoManager([this.ycells], {
            trackedOrigins: new Set([this])
        });
        this._ycellMapping = new Map();
        this._disableDocumentWideUndoRedo = options.disableDocumentWideUndoRedo;
        this.ycells.observe(this._onYCellsChanged);
        this.cells = this.ycells.toArray().map(ycell => {
            if (!this._ycellMapping.has(ycell)) {
                this._ycellMapping.set(ycell, createCellFromType(ycell));
            }
            return this._ycellMapping.get(ycell);
        });
        this.ymeta.observe(this._onMetadataChanged);
        this.ystate.observe(this._onStateChanged);
    }
    get nbformat() {
        return this.ystate.get('nbformat');
    }
    set nbformat(value) {
        this.transact(() => {
            this.ystate.set('nbformat', value);
        }, false);
    }
    get nbformat_minor() {
        return this.ystate.get('nbformatMinor');
    }
    set nbformat_minor(value) {
        this.transact(() => {
            this.ystate.set('nbformatMinor', value);
        }, false);
    }
    /**
     * Dispose of the resources.
     */
    dispose() {
        this.ycells.unobserve(this._onYCellsChanged);
        this.ymeta.unobserve(this._onMetadataChanged);
        this.ystate.unobserve(this._onStateChanged);
    }
    /**
     * Get a shared cell by index.
     *
     * @param index: Cell's position.
     *
     * @returns The requested shared cell.
     */
    getCell(index) {
        return this.cells[index];
    }
    /**
     * Insert a shared cell into a specific position.
     *
     * @param index: Cell's position.
     *
     * @param cell: Cell to insert.
     */
    insertCell(index, cell) {
        this.insertCells(index, [cell]);
    }
    /**
     * Insert a list of shared cells into a specific position.
     *
     * @param index: Position to insert the cells.
     *
     * @param cells: Array of shared cells to insert.
     */
    insertCells(index, cells) {
        cells.forEach(cell => {
            this._ycellMapping.set(cell.ymodel, cell);
            if (!this.disableDocumentWideUndoRedo) {
                cell.undoManager = this.undoManager;
            }
        });
        this.transact(() => {
            this.ycells.insert(index, cells.map(cell => cell.ymodel));
        });
    }
    /**
     * Move a cell.
     *
     * @param fromIndex: Index of the cell to move.
     *
     * @param toIndex: New position of the cell.
     */
    moveCell(fromIndex, toIndex) {
        this.transact(() => {
            const fromCell = this.getCell(fromIndex).clone();
            this.deleteCell(fromIndex);
            this.insertCell(toIndex, fromCell);
        });
    }
    /**
     * Remove a cell.
     *
     * @param index: Index of the cell to remove.
     */
    deleteCell(index) {
        this.deleteCellRange(index, index + 1);
    }
    /**
     * Remove a range of cells.
     *
     * @param from: The start index of the range to remove (inclusive).
     *
     * @param to: The end index of the range to remove (exclusive).
     */
    deleteCellRange(from, to) {
        this.transact(() => {
            this.ycells.delete(from, to - from);
        });
    }
    /**
     * Returns the metadata associated with the notebook.
     *
     * @returns Notebook's metadata.
     */
    getMetadata() {
        const meta = this.ymeta.get('metadata');
        return meta ? deepCopy(meta) : {};
    }
    /**
     * Sets the metadata associated with the notebook.
     *
     * @param metadata: Notebook's metadata.
     */
    setMetadata(value) {
        this.ymeta.set('metadata', deepCopy(value));
    }
    /**
     * Updates the metadata associated with the notebook.
     *
     * @param value: Metadata's attribute to update.
     */
    updateMetadata(value) {
        // TODO: Maybe modify only attributes instead of replacing the whole metadata?
        this.ymeta.set('metadata', Object.assign({}, this.getMetadata(), value));
    }
    /**
     * Create a new YNotebook.
     */
    static create(disableDocumentWideUndoRedo) {
        return new YNotebook({ disableDocumentWideUndoRedo });
    }
    /**
     * Wether the the undo/redo logic should be
     * considered on the full document across all cells.
     *
     * @return The disableDocumentWideUndoRedo setting.
     */
    get disableDocumentWideUndoRedo() {
        return this._disableDocumentWideUndoRedo;
    }
}
/**
 * Create a new shared cell given the type.
 */
const createCellFromType = (type) => {
    switch (type.get('cell_type')) {
        case 'code':
            return new YCodeCell(type);
        case 'markdown':
            return new YMarkdownCell(type);
        case 'raw':
            return new YRawCell(type);
        default:
            throw new Error('Found unknown cell type');
    }
};
/**
 * Create a new standalone cell given the type.
 */
const createStandaloneCell = (cellType, id) => {
    switch (cellType) {
        case 'markdown':
            return YMarkdownCell.createStandalone(id);
        case 'code':
            return YCodeCell.createStandalone(id);
        default:
            // raw
            return YRawCell.createStandalone(id);
    }
};
class YBaseCell {
    constructor(ymodel) {
        /**
         * The notebook that this cell belongs to.
         */
        this._notebook = null;
        /**
         * Whether the cell is standalone or not.
         *
         * If the cell is standalone. It cannot be
         * inserted into a YNotebook because the Yjs model is already
         * attached to an anonymous Y.Doc instance.
         */
        this.isStandalone = false;
        /**
         * Handle a change to the ymodel.
         */
        this._modelObserver = (events) => {
            const changes = {};
            const sourceEvent = events.find(event => event.target === this.ymodel.get('source'));
            if (sourceEvent) {
                changes.sourceChange = sourceEvent.changes.delta;
            }
            const outputEvent = events.find(event => event.target === this.ymodel.get('outputs'));
            if (outputEvent) {
                changes.outputsChange = outputEvent.changes.delta;
            }
            const modelEvent = events.find(event => event.target === this.ymodel);
            if (modelEvent && modelEvent.keysChanged.has('metadata')) {
                const change = modelEvent.changes.keys.get('metadata');
                changes.metadataChange = {
                    oldValue: (change === null || change === void 0 ? void 0 : change.oldValue) ? change.oldValue : undefined,
                    newValue: this.getMetadata()
                };
            }
            if (modelEvent && modelEvent.keysChanged.has('execution_count')) {
                const change = modelEvent.changes.keys.get('execution_count');
                changes.executionCountChange = {
                    oldValue: change.oldValue,
                    newValue: this.ymodel.get('execution_count')
                };
            }
            // The model allows us to replace the complete source with a new string. We express this in the Delta format
            // as a replace of the complete string.
            const ysource = this.ymodel.get('source');
            if (modelEvent && modelEvent.keysChanged.has('source')) {
                changes.sourceChange = [
                    { delete: this._prevSourceLength },
                    { insert: ysource.toString() }
                ];
            }
            this._prevSourceLength = ysource.length;
            this._changed.emit(changes);
        };
        this.isDisposed = false;
        this._undoManager = null;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this.ymodel = ymodel;
        const ysource = ymodel.get('source');
        this._prevSourceLength = ysource ? ysource.length : 0;
        this.ymodel.observeDeep(this._modelObserver);
        this._awareness = null;
    }
    get ysource() {
        return this.ymodel.get('source');
    }
    get awareness() {
        var _a, _b, _c;
        return (_c = (_a = this._awareness) !== null && _a !== void 0 ? _a : (_b = this.notebook) === null || _b === void 0 ? void 0 : _b.awareness) !== null && _c !== void 0 ? _c : null;
    }
    /**
     * Perform a transaction. While the function f is called, all changes to the shared
     * document are bundled into a single event.
     */
    transact(f, undoable = true) {
        this.notebook && undoable
            ? this.notebook.transact(f)
            : this.ymodel.doc.transact(f, this);
    }
    /**
     * The notebook that this cell belongs to.
     */
    get undoManager() {
        var _a;
        if (!this.notebook) {
            return this._undoManager;
        }
        return ((_a = this.notebook) === null || _a === void 0 ? void 0 : _a.disableDocumentWideUndoRedo) ? this._undoManager
            : this.notebook.undoManager;
    }
    /**
     * Set the undoManager when adding new cells.
     */
    set undoManager(undoManager) {
        this._undoManager = undoManager;
    }
    /**
     * Undo an operation.
     */
    undo() {
        var _a;
        (_a = this.undoManager) === null || _a === void 0 ? void 0 : _a.undo();
    }
    /**
     * Redo an operation.
     */
    redo() {
        var _a;
        (_a = this.undoManager) === null || _a === void 0 ? void 0 : _a.redo();
    }
    /**
     * Whether the object can undo changes.
     */
    canUndo() {
        return !!this.undoManager && this.undoManager.undoStack.length > 0;
    }
    /**
     * Whether the object can redo changes.
     */
    canRedo() {
        return !!this.undoManager && this.undoManager.redoStack.length > 0;
    }
    /**
     * Clear the change stack.
     */
    clearUndoHistory() {
        var _a;
        (_a = this.undoManager) === null || _a === void 0 ? void 0 : _a.clear();
    }
    /**
     * The notebook that this cell belongs to.
     */
    get notebook() {
        return this._notebook;
    }
    /**
     * Create a new YRawCell that can be inserted into a YNotebook
     */
    static create(id = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.UUID.uuid4()) {
        const ymodel = new yjs__WEBPACK_IMPORTED_MODULE_3__.Map();
        const ysource = new yjs__WEBPACK_IMPORTED_MODULE_3__.Text();
        ymodel.set('source', ysource);
        ymodel.set('metadata', {});
        ymodel.set('cell_type', this.prototype.cell_type);
        ymodel.set('id', id);
        return new this(ymodel);
    }
    /**
     * Create a new YRawCell that works standalone. It cannot be
     * inserted into a YNotebook because the Yjs model is already
     * attached to an anonymous Y.Doc instance.
     */
    static createStandalone(id) {
        const cell = this.create(id);
        cell.isStandalone = true;
        const doc = new yjs__WEBPACK_IMPORTED_MODULE_3__.Doc();
        doc.getArray().insert(0, [cell.ymodel]);
        cell._awareness = new y_protocols_awareness__WEBPACK_IMPORTED_MODULE_2__.Awareness(doc);
        cell._undoManager = new yjs__WEBPACK_IMPORTED_MODULE_3__.UndoManager([cell.ymodel], {
            trackedOrigins: new Set([cell])
        });
        return cell;
    }
    /**
     * Clone the cell.
     *
     * @todo clone should only be available in the specific implementations i.e. ISharedCodeCell
     */
    clone() {
        const ymodel = new yjs__WEBPACK_IMPORTED_MODULE_3__.Map();
        const ysource = new yjs__WEBPACK_IMPORTED_MODULE_3__.Text(this.getSource());
        ymodel.set('source', ysource);
        ymodel.set('metadata', this.getMetadata());
        ymodel.set('cell_type', this.cell_type);
        ymodel.set('id', this.getId());
        const Self = this.constructor;
        const clone = new Self(ymodel);
        // TODO The assignment of the undoManager does not work for a clone.
        // See https://github.com/jupyterlab/jupyterlab/issues/11035
        clone._undoManager = this.undoManager;
        return clone;
    }
    /**
     * The changed signal.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Dispose of the resources.
     */
    dispose() {
        this.ymodel.unobserveDeep(this._modelObserver);
    }
    /**
     * Gets the cell attachments.
     *
     * @returns The cell attachments.
     */
    getAttachments() {
        return this.ymodel.get('attachments');
    }
    /**
     * Sets the cell attachments
     *
     * @param attachments: The cell attachments.
     */
    setAttachments(attachments) {
        this.transact(() => {
            if (attachments == null) {
                this.ymodel.delete('attachments');
            }
            else {
                this.ymodel.set('attachments', attachments);
            }
        });
    }
    /**
     * Get cell id.
     *
     * @returns Cell id
     */
    getId() {
        return this.ymodel.get('id');
    }
    /**
     * Gets cell's source.
     *
     * @returns Cell's source.
     */
    getSource() {
        return this.ymodel.get('source').toString();
    }
    /**
     * Sets cell's source.
     *
     * @param value: New source.
     */
    setSource(value) {
        const ytext = this.ymodel.get('source');
        this.transact(() => {
            ytext.delete(0, ytext.length);
            ytext.insert(0, value);
        });
        // @todo Do we need proper replace semantic? This leads to issues in editor bindings because they don't switch source.
        // this.ymodel.set('source', new Y.Text(value));
    }
    /**
     * Replace content from `start' to `end` with `value`.
     *
     * @param start: The start index of the range to replace (inclusive).
     *
     * @param end: The end index of the range to replace (exclusive).
     *
     * @param value: New source (optional).
     */
    updateSource(start, end, value = '') {
        this.transact(() => {
            const ysource = this.ysource;
            // insert and then delete.
            // This ensures that the cursor position is adjusted after the replaced content.
            ysource.insert(start, value);
            ysource.delete(start + value.length, end - start);
        });
    }
    /**
     * The type of the cell.
     */
    get cell_type() {
        throw new Error('A YBaseCell must not be constructed');
    }
    /**
     * Returns the metadata associated with the notebook.
     *
     * @returns Notebook's metadata.
     */
    getMetadata() {
        return deepCopy(this.ymodel.get('metadata'));
    }
    /**
     * Sets the metadata associated with the notebook.
     *
     * @param metadata: Notebook's metadata.
     */
    setMetadata(value) {
        this.transact(() => {
            this.ymodel.set('metadata', deepCopy(value));
        });
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return {
            id: this.getId(),
            cell_type: this.cell_type,
            source: this.getSource(),
            metadata: this.getMetadata()
        };
    }
}
class YCodeCell extends YBaseCell {
    /**
     * The type of the cell.
     */
    get cell_type() {
        return 'code';
    }
    /**
     * The code cell's prompt number. Will be null if the cell has not been run.
     */
    get execution_count() {
        return this.ymodel.get('execution_count');
    }
    /**
     * The code cell's prompt number. Will be null if the cell has not been run.
     */
    set execution_count(count) {
        this.transact(() => {
            this.ymodel.set('execution_count', count);
        });
    }
    /**
     * Execution, display, or stream outputs.
     */
    getOutputs() {
        return deepCopy(this.ymodel.get('outputs').toArray());
    }
    /**
     * Replace all outputs.
     */
    setOutputs(outputs) {
        const youtputs = this.ymodel.get('outputs');
        this.transact(() => {
            youtputs.delete(0, youtputs.length);
            youtputs.insert(0, outputs);
        }, false);
    }
    /**
     * Replace content from `start' to `end` with `outputs`.
     *
     * @param start: The start index of the range to replace (inclusive).
     *
     * @param end: The end index of the range to replace (exclusive).
     *
     * @param outputs: New outputs (optional).
     */
    updateOutputs(start, end, outputs = []) {
        const youtputs = this.ymodel.get('outputs');
        const fin = end < youtputs.length ? end - start : youtputs.length - start;
        this.transact(() => {
            youtputs.delete(start, fin);
            youtputs.insert(start, outputs);
        }, false);
    }
    /**
     * Create a new YCodeCell that can be inserted into a YNotebook
     */
    static create(id) {
        const cell = super.create(id);
        cell.ymodel.set('execution_count', 0); // for some default value
        cell.ymodel.set('outputs', new yjs__WEBPACK_IMPORTED_MODULE_3__.Array());
        return cell;
    }
    /**
     * Create a new YCodeCell that works standalone. It cannot be
     * inserted into a YNotebook because the Yjs model is already
     * attached to an anonymous Y.Doc instance.
     */
    static createStandalone(id) {
        const cell = super.createStandalone(id);
        cell.ymodel.set('execution_count', null); // for some default value
        cell.ymodel.set('outputs', new yjs__WEBPACK_IMPORTED_MODULE_3__.Array());
        return cell;
    }
    /**
     * Create a new YCodeCell that can be inserted into a YNotebook
     *
     * @todo clone should only be available in the specific implementations i.e. ISharedCodeCell
     */
    clone() {
        const cell = super.clone();
        const youtputs = new yjs__WEBPACK_IMPORTED_MODULE_3__.Array();
        youtputs.insert(0, this.getOutputs());
        cell.ymodel.set('execution_count', this.execution_count); // for some default value
        cell.ymodel.set('outputs', youtputs);
        return cell;
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return {
            id: this.getId(),
            cell_type: 'code',
            source: this.getSource(),
            metadata: this.getMetadata(),
            outputs: this.getOutputs(),
            execution_count: this.execution_count
        };
    }
}
class YRawCell extends YBaseCell {
    /**
     * Create a new YRawCell that can be inserted into a YNotebook
     */
    static create(id) {
        return super.create(id);
    }
    /**
     * Create a new YRawCell that works standalone. It cannot be
     * inserted into a YNotebook because the Yjs model is already
     * attached to an anonymous Y.Doc instance.
     */
    static createStandalone(id) {
        return super.createStandalone(id);
    }
    /**
     * String identifying the type of cell.
     */
    get cell_type() {
        return 'raw';
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return {
            id: this.getId(),
            cell_type: 'raw',
            source: this.getSource(),
            metadata: this.getMetadata(),
            attachments: this.getAttachments()
        };
    }
}
class YMarkdownCell extends YBaseCell {
    /**
     * Create a new YMarkdownCell that can be inserted into a YNotebook
     */
    static create(id) {
        return super.create(id);
    }
    /**
     * Create a new YMarkdownCell that works standalone. It cannot be
     * inserted into a YNotebook because the Yjs model is already
     * attached to an anonymous Y.Doc instance.
     */
    static createStandalone(id) {
        return super.createStandalone(id);
    }
    /**
     * String identifying the type of cell.
     */
    get cell_type() {
        return 'markdown';
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return {
            id: this.getId(),
            cell_type: 'markdown',
            source: this.getSource(),
            metadata: this.getMetadata(),
            attachments: this.getAttachments()
        };
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (YNotebook);


/***/ }),

/***/ "../node_modules/y-protocols/awareness.js":
/*!************************************************!*\
  !*** ../node_modules/y-protocols/awareness.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "outdatedTimeout": () => (/* binding */ outdatedTimeout),
/* harmony export */   "Awareness": () => (/* binding */ Awareness),
/* harmony export */   "removeAwarenessStates": () => (/* binding */ removeAwarenessStates),
/* harmony export */   "encodeAwarenessUpdate": () => (/* binding */ encodeAwarenessUpdate),
/* harmony export */   "modifyAwarenessUpdate": () => (/* binding */ modifyAwarenessUpdate),
/* harmony export */   "applyAwarenessUpdate": () => (/* binding */ applyAwarenessUpdate)
/* harmony export */ });
/* harmony import */ var lib0_encoding__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! lib0/encoding */ "../node_modules/lib0/encoding.js");
/* harmony import */ var lib0_decoding__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! lib0/decoding */ "../node_modules/lib0/decoding.js");
/* harmony import */ var lib0_time__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! lib0/time */ "../node_modules/lib0/time.js");
/* harmony import */ var lib0_math__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! lib0/math */ "../node_modules/lib0/math.js");
/* harmony import */ var lib0_observable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! lib0/observable */ "../node_modules/lib0/observable.js");
/* harmony import */ var lib0_function__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! lib0/function */ "../node_modules/lib0/function.js");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_0__);
/**
 * @module awareness-protocol
 */







 // eslint-disable-line

const outdatedTimeout = 30000

/**
 * @typedef {Object} MetaClientState
 * @property {number} MetaClientState.clock
 * @property {number} MetaClientState.lastUpdated unix timestamp
 */

/**
 * The Awareness class implements a simple shared state protocol that can be used for non-persistent data like awareness information
 * (cursor, username, status, ..). Each client can update its own local state and listen to state changes of
 * remote clients. Every client may set a state of a remote peer to `null` to mark the client as offline.
 *
 * Each client is identified by a unique client id (something we borrow from `doc.clientID`). A client can override
 * its own state by propagating a message with an increasing timestamp (`clock`). If such a message is received, it is
 * applied if the known state of that client is older than the new state (`clock < newClock`). If a client thinks that
 * a remote client is offline, it may propagate a message with
 * `{ clock: currentClientClock, state: null, client: remoteClient }`. If such a
 * message is received, and the known clock of that client equals the received clock, it will override the state with `null`.
 *
 * Before a client disconnects, it should propagate a `null` state with an updated clock.
 *
 * Awareness states must be updated every 30 seconds. Otherwise the Awareness instance will delete the client state.
 *
 * @extends {Observable<string>}
 */
class Awareness extends lib0_observable__WEBPACK_IMPORTED_MODULE_1__.Observable {
  /**
   * @param {Y.Doc} doc
   */
  constructor (doc) {
    super()
    this.doc = doc
    /**
     * @type {number}
     */
    this.clientID = doc.clientID
    /**
     * Maps from client id to client state
     * @type {Map<number, Object<string, any>>}
     */
    this.states = new Map()
    /**
     * @type {Map<number, MetaClientState>}
     */
    this.meta = new Map()
    this._checkInterval = /** @type {any} */ (setInterval(() => {
      const now = lib0_time__WEBPACK_IMPORTED_MODULE_2__.getUnixTime()
      if (this.getLocalState() !== null && (outdatedTimeout / 2 <= now - /** @type {{lastUpdated:number}} */ (this.meta.get(this.clientID)).lastUpdated)) {
        // renew local clock
        this.setLocalState(this.getLocalState())
      }
      /**
       * @type {Array<number>}
       */
      const remove = []
      this.meta.forEach((meta, clientid) => {
        if (clientid !== this.clientID && outdatedTimeout <= now - meta.lastUpdated && this.states.has(clientid)) {
          remove.push(clientid)
        }
      })
      if (remove.length > 0) {
        removeAwarenessStates(this, remove, 'timeout')
      }
    }, lib0_math__WEBPACK_IMPORTED_MODULE_3__.floor(outdatedTimeout / 10)))
    doc.on('destroy', () => {
      this.destroy()
    })
    this.setLocalState({})
  }

  destroy () {
    this.emit('destroy', [this])
    this.setLocalState(null)
    super.destroy()
    clearInterval(this._checkInterval)
  }

  /**
   * @return {Object<string,any>|null}
   */
  getLocalState () {
    return this.states.get(this.clientID) || null
  }

  /**
   * @param {Object<string,any>|null} state
   */
  setLocalState (state) {
    const clientID = this.clientID
    const currLocalMeta = this.meta.get(clientID)
    const clock = currLocalMeta === undefined ? 0 : currLocalMeta.clock + 1
    const prevState = this.states.get(clientID)
    if (state === null) {
      this.states.delete(clientID)
    } else {
      this.states.set(clientID, state)
    }
    this.meta.set(clientID, {
      clock,
      lastUpdated: lib0_time__WEBPACK_IMPORTED_MODULE_2__.getUnixTime()
    })
    const added = []
    const updated = []
    const filteredUpdated = []
    const removed = []
    if (state === null) {
      removed.push(clientID)
    } else if (prevState == null) {
      if (state != null) {
        added.push(clientID)
      }
    } else {
      updated.push(clientID)
      if (!lib0_function__WEBPACK_IMPORTED_MODULE_4__.equalityDeep(prevState, state)) {
        filteredUpdated.push(clientID)
      }
    }
    if (added.length > 0 || filteredUpdated.length > 0 || removed.length > 0) {
      this.emit('change', [{ added, updated: filteredUpdated, removed }, 'local'])
    }
    this.emit('update', [{ added, updated, removed }, 'local'])
  }

  /**
   * @param {string} field
   * @param {any} value
   */
  setLocalStateField (field, value) {
    const state = this.getLocalState()
    if (state !== null) {
      this.setLocalState({
        ...state,
        [field]: value
      })
    }
  }

  /**
   * @return {Map<number,Object<string,any>>}
   */
  getStates () {
    return this.states
  }
}

/**
 * Mark (remote) clients as inactive and remove them from the list of active peers.
 * This change will be propagated to remote clients.
 *
 * @param {Awareness} awareness
 * @param {Array<number>} clients
 * @param {any} origin
 */
const removeAwarenessStates = (awareness, clients, origin) => {
  const removed = []
  for (let i = 0; i < clients.length; i++) {
    const clientID = clients[i]
    if (awareness.states.has(clientID)) {
      awareness.states.delete(clientID)
      if (clientID === awareness.clientID) {
        const curMeta = /** @type {MetaClientState} */ (awareness.meta.get(clientID))
        awareness.meta.set(clientID, {
          clock: curMeta.clock + 1,
          lastUpdated: lib0_time__WEBPACK_IMPORTED_MODULE_2__.getUnixTime()
        })
      }
      removed.push(clientID)
    }
  }
  if (removed.length > 0) {
    awareness.emit('change', [{ added: [], updated: [], removed }, origin])
    awareness.emit('update', [{ added: [], updated: [], removed }, origin])
  }
}

/**
 * @param {Awareness} awareness
 * @param {Array<number>} clients
 * @return {Uint8Array}
 */
const encodeAwarenessUpdate = (awareness, clients, states = awareness.states) => {
  const len = clients.length
  const encoder = lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.createEncoder()
  lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.writeVarUint(encoder, len)
  for (let i = 0; i < len; i++) {
    const clientID = clients[i]
    const state = states.get(clientID) || null
    const clock = /** @type {MetaClientState} */ (awareness.meta.get(clientID)).clock
    lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.writeVarUint(encoder, clientID)
    lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.writeVarUint(encoder, clock)
    lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.writeVarString(encoder, JSON.stringify(state))
  }
  return lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.toUint8Array(encoder)
}

/**
 * Modify the content of an awareness update before re-encoding it to an awareness update.
 *
 * This might be useful when you have a central server that wants to ensure that clients
 * cant hijack somebody elses identity.
 *
 * @param {Uint8Array} update
 * @param {function(any):any} modify
 * @return {Uint8Array}
 */
const modifyAwarenessUpdate = (update, modify) => {
  const decoder = lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.createDecoder(update)
  const encoder = lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.createEncoder()
  const len = lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.readVarUint(decoder)
  lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.writeVarUint(encoder, len)
  for (let i = 0; i < len; i++) {
    const clientID = lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.readVarUint(decoder)
    const clock = lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.readVarUint(decoder)
    const state = JSON.parse(lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.readVarString(decoder))
    const modifiedState = modify(state)
    lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.writeVarUint(encoder, clientID)
    lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.writeVarUint(encoder, clock)
    lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.writeVarString(encoder, JSON.stringify(modifiedState))
  }
  return lib0_encoding__WEBPACK_IMPORTED_MODULE_5__.toUint8Array(encoder)
}

/**
 * @param {Awareness} awareness
 * @param {Uint8Array} update
 * @param {any} origin This will be added to the emitted change event
 */
const applyAwarenessUpdate = (awareness, update, origin) => {
  const decoder = lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.createDecoder(update)
  const timestamp = lib0_time__WEBPACK_IMPORTED_MODULE_2__.getUnixTime()
  const added = []
  const updated = []
  const filteredUpdated = []
  const removed = []
  const len = lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.readVarUint(decoder)
  for (let i = 0; i < len; i++) {
    const clientID = lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.readVarUint(decoder)
    let clock = lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.readVarUint(decoder)
    const state = JSON.parse(lib0_decoding__WEBPACK_IMPORTED_MODULE_6__.readVarString(decoder))
    const clientMeta = awareness.meta.get(clientID)
    const prevState = awareness.states.get(clientID)
    const currClock = clientMeta === undefined ? 0 : clientMeta.clock
    if (currClock < clock || (currClock === clock && state === null && awareness.states.has(clientID))) {
      if (state === null) {
        // never let a remote client remove this local state
        if (clientID === awareness.clientID && awareness.getLocalState() != null) {
          // remote client removed the local state. Do not remote state. Broadcast a message indicating
          // that this client still exists by increasing the clock
          clock++
        } else {
          awareness.states.delete(clientID)
        }
      } else {
        awareness.states.set(clientID, state)
      }
      awareness.meta.set(clientID, {
        clock,
        lastUpdated: timestamp
      })
      if (clientMeta === undefined && state !== null) {
        added.push(clientID)
      } else if (clientMeta !== undefined && state === null) {
        removed.push(clientID)
      } else if (state !== null) {
        if (!lib0_function__WEBPACK_IMPORTED_MODULE_4__.equalityDeep(state, prevState)) {
          filteredUpdated.push(clientID)
        }
        updated.push(clientID)
      }
    }
  }
  if (added.length > 0 || filteredUpdated.length > 0 || removed.length > 0) {
    awareness.emit('change', [{
      added, updated: filteredUpdated, removed
    }, origin])
  }
  if (added.length > 0 || updated.length > 0 || removed.length > 0) {
    awareness.emit('update', [{
      added, updated, removed
    }, origin])
  }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2hhcmVkLW1vZGVscy9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3NoYXJlZC1tb2RlbHMvc3JjL3V0aWxzLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zaGFyZWQtbW9kZWxzL3NyYy95bW9kZWxzLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9ub2RlX21vZHVsZXMveS1wcm90b2NvbHMvYXdhcmVuZXNzLmpzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFFbUI7QUFDSTtBQUNGOzs7Ozs7Ozs7Ozs7Ozs7OztBQ1h4Qjs7OytFQUcrRTtBQUt4RSxTQUFTLDJCQUEyQixDQUN6QyxLQUF1QjtJQUV2QixJQUFJLE9BQU8sR0FBRyxJQUFJLEdBQUcsRUFBRSxDQUFDO0lBQ3hCLEtBQUssQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLE9BQU8sQ0FBQyxDQUFDLEtBQUssRUFBRSxHQUFHLEVBQUUsRUFBRTtRQUN4QyxPQUFPLENBQUMsR0FBRyxDQUFDLEdBQUcsRUFBRTtZQUNmLE1BQU0sRUFBRSxLQUFLLENBQUMsTUFBTTtZQUNwQixRQUFRLEVBQUUsS0FBSyxDQUFDLFFBQVE7WUFDeEIsUUFBUSxFQUFFLElBQUksQ0FBQyxLQUFLLENBQUMsR0FBRyxDQUFDLEdBQUcsQ0FBQztTQUM5QixDQUFDLENBQUM7SUFDTCxDQUFDLENBQUMsQ0FBQztJQUNILE9BQU8sT0FBTyxDQUFDO0FBQ2pCLENBQUM7QUFFRDs7Ozs7Ozs7Ozs7O0dBWUc7QUFDSSxNQUFNLFdBQVcsR0FBRyxHQUE4QixFQUFFO0lBQ3pELElBQUksS0FB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cUI7QUFDdkIsaUJBQWlCLFNBQVM7QUFDMUIscUJBQXFCLHNEQUFvQjtBQUN6QyxrQkFBa0Isc0RBQW9CO0FBQ3RDLDZCQUE2Qix3REFBc0I7QUFDbkQ7QUFDQSxJQUFJLHVEQUFxQjtBQUN6QixJQUFJLHVEQUFxQjtBQUN6QixJQUFJLHlEQUF1QjtBQUMzQjtBQUNBLFNBQVMsdURBQXFCO0FBQzlCOztBQUVBO0FBQ0EsV0FBVyxVQUFVO0FBQ3JCLFdBQVcsV0FBVztBQUN0QixXQUFXLElBQUk7QUFDZjtBQUNPO0FBQ1Asa0JBQWtCLHdEQUFzQjtBQUN4QyxvQkFBb0Isa0RBQWdCO0FBQ3BDO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsY0FBYyxzREFBb0I7QUFDbEMsaUJBQWlCLFNBQVM7QUFDMUIscUJBQXFCLHNEQUFvQjtBQUN6QyxnQkFBZ0Isc0RBQW9CO0FBQ3BDLDZCQUE2Qix3REFBc0I7QUFDbkQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQSxPQUFPO0FBQ1AsYUFBYSx1REFBYztBQUMzQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQSIsImZpbGUiOiJwYWNrYWdlc19zaGFyZWQtbW9kZWxzX2xpYl9pbmRleF9qcy4wNjU4ZmVlZmE1NDY3MzhkNzFkYy5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgc2hhcmVkLW1vZGVsc1xuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vYXBpJztcbmV4cG9ydCAqIGZyb20gJy4veW1vZGVscyc7XG5leHBvcnQgKiBmcm9tICcuL3V0aWxzJztcbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuXG5pbXBvcnQgKiBhcyBZIGZyb20gJ3lqcyc7XG5pbXBvcnQgKiBhcyBtb2RlbHMgZnJvbSAnLi9hcGknO1xuXG5leHBvcnQgZnVuY3Rpb24gY29udmVydFlNYXBFdmVudFRvTWFwQ2hhbmdlKFxuICBldmVudDogWS5ZTWFwRXZlbnQ8YW55PlxuKTogbW9kZWxzLk1hcENoYW5nZSB7XG4gIGxldCBjaGFuZ2VzID0gbmV3IE1hcCgpO1xuICBldmVudC5jaGFuZ2VzLmtleXMuZm9yRWFjaCgoZXZlbnQsIGtleSkgPT4ge1xuICAgIGNoYW5nZXMuc2V0KGtleSwge1xuICAgICAgYWN0aW9uOiBldmVudC5hY3Rpb24sXG4gICAgICBvbGRWYWx1ZTogZXZlbnQub2xkVmFsdWUsXG4gICAgICBuZXdWYWx1ZTogdGhpcy55bWV0YS5nZXQoa2V5KVxuICAgIH0pO1xuICB9KTtcbiAgcmV0dXJuIGNoYW5nZXM7XG59XG5cbi8qKlxuICogQ3JlYXRlcyBhIG11dHVhbCBleGNsdWRlIGZ1bmN0aW9uIHdpdGggdGhlIGZvbGxvd2luZyBwcm9wZXJ0eTpcbiAqXG4gKiBgYGBqc1xuICogY29uc3QgbXV0ZXggPSBjcmVhdGVNdXRleCgpXG4gKiBtdXRleCgoKSA9PiB7XG4gKiAgIC8vIFRoaXMgZnVuY3Rpb24gaXMgaW1tZWRpYXRlbHkgZXhlY3V0ZWRcbiAqICAgbXV0ZXgoKCkgPT4ge1xuICogICAgIC8vIFRoaXMgZnVuY3Rpb24gaXMgbm90IGV4ZWN1dGVkLCBhcyB0aGUgbXV0ZXggaXMgYWxyZWFkeSBhY3RpdmUuXG4gKiAgIH0pXG4gKiB9KVxuICogYGBgXG4gKi9cbmV4cG9ydCBjb25zdCBjcmVhdGVNdXRleCA9ICgpOiAoKGY6ICgpID0+IHZvaWQpID0+IHZvaWQpID0+IHtcbiAgbGV0IHRva2VuID0gdHJ1ZTtcbiAgcmV0dXJuIChmOiBhbnkpOiB2b2lkID0+IHtcbiAgICBpZiAodG9rZW4pIHtcbiAgICAgIHRva2VuID0gZmFsc2U7XG4gICAgICB0cnkge1xuICAgICAgICBmKCk7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICB0b2tlbiA9IHRydWU7XG4gICAgICB9XG4gICAgfVxuICB9O1xufTtcbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuXG5pbXBvcnQgKiBhcyBuYmZvcm1hdCBmcm9tICdAanVweXRlcmxhYi9uYmZvcm1hdCc7XG5pbXBvcnQgeyBVVUlEIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgQXdhcmVuZXNzIH0gZnJvbSAneS1wcm90b2NvbHMvYXdhcmVuZXNzJztcbmltcG9ydCAqIGFzIFkgZnJvbSAneWpzJztcbmltcG9ydCAqIGFzIG1vZGVscyBmcm9tICcuL2FwaSc7XG5pbXBvcnQgeyBEZWx0YSwgSVNoYXJlZE5vdGVib29rIH0gZnJvbSAnLi9hcGknO1xuXG5jb25zdCBkZWVwQ29weSA9IChvOiBhbnkpID0+IEpTT04ucGFyc2UoSlNPTi5zdHJpbmdpZnkobykpO1xuXG4vKipcbiAqIEFic3RyYWN0IGludGVyZmFjZSB0byBkZWZpbmUgU2hhcmVkIE1vZGVscyB0aGF0IGNhbiBiZSBib3VuZCB0byBhIHRleHQgZWRpdG9yIHVzaW5nIGFueSBleGlzdGluZ1xuICogWWpzLWJhc2VkIGVkaXRvciBiaW5kaW5nLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElZVGV4dCBleHRlbmRzIG1vZGVscy5JU2hhcmVkVGV4dCB7XG4gIHJlYWRvbmx5IHlzb3VyY2U6IFkuVGV4dDtcbiAgcmVhZG9ubHkgYXdhcmVuZXNzOiBBd2FyZW5lc3MgfCBudWxsO1xuICByZWFkb25seSB1bmRvTWFuYWdlcjogWS5VbmRvTWFuYWdlciB8IG51bGw7XG59XG5cbmV4cG9ydCB0eXBlIFlDZWxsVHlwZSA9IFlSYXdDZWxsIHwgWUNvZGVDZWxsIHwgWU1hcmtkb3duQ2VsbDtcblxuZXhwb3J0IGNsYXNzIFlEb2N1bWVudDxUPiBpbXBsZW1lbnRzIG1vZGVscy5JU2hhcmVkRG9jdW1lbnQge1xuICBnZXQgZGlydHkoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMueXN0YXRlLmdldCgnZGlydHknKTtcbiAgfVxuXG4gIHNldCBkaXJ0eSh2YWx1ZTogYm9vbGVhbikge1xuICAgIHRoaXMudHJhbnNhY3QoKCkgPT4ge1xuICAgICAgdGhpcy55c3RhdGUuc2V0KCdkaXJ0eScsIHZhbHVlKTtcbiAgICB9LCBmYWxzZSk7XG4gIH1cblxuICAvKipcbiAgICogUGVyZm9ybSBhIHRyYW5zYWN0aW9uLiBXaGlsZSB0aGUgZnVuY3Rpb24gZiBpcyBjYWxsZWQsIGFsbCBjaGFuZ2VzIHRvIHRoZSBzaGFyZWRcbiAgICogZG9jdW1lbnQgYXJlIGJ1bmRsZWQgaW50byBhIHNpbmdsZSBldmVudC5cbiAgICovXG4gIHRyYW5zYWN0KGY6ICgpID0+IHZvaWQsIHVuZG9hYmxlID0gdHJ1ZSk6IHZvaWQge1xuICAgIHRoaXMueWRvYy50cmFuc2FjdChmLCB1bmRvYWJsZSA/IHRoaXMgOiBudWxsKTtcbiAgfVxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICB0aGlzLmlzRGlzcG9zZWQgPSB0cnVlO1xuICAgIHRoaXMueWRvYy5kZXN0cm95KCk7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgb2JqZWN0IGNhbiB1bmRvIGNoYW5nZXMuXG4gICAqL1xuICBjYW5VbmRvKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLnVuZG9NYW5hZ2VyLnVuZG9TdGFjay5sZW5ndGggPiAwO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG9iamVjdCBjYW4gcmVkbyBjaGFuZ2VzLlxuICAgKi9cbiAgY2FuUmVkbygpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy51bmRvTWFuYWdlci5yZWRvU3RhY2subGVuZ3RoID4gMDtcbiAgfVxuXG4gIC8qKlxuICAgKiBVbmRvIGFuIG9wZXJhdGlvbi5cbiAgICovXG4gIHVuZG8oKTogdm9pZCB7XG4gICAgdGhpcy51bmRvTWFuYWdlci51bmRvKCk7XG4gIH1cblxuICAvKipcbiAgICogUmVkbyBhbiBvcGVyYXRpb24uXG4gICAqL1xuICByZWRvKCk6IHZvaWQge1xuICAgIHRoaXMudW5kb01hbmFnZXIucmVkbygpO1xuICB9XG5cbiAgLyoqXG4gICAqIENsZWFyIHRoZSBjaGFuZ2Ugc3RhY2suXG4gICAqL1xuICBjbGVhclVuZG9IaXN0b3J5KCk6IHZvaWQge1xuICAgIHRoaXMudW5kb01hbmFnZXIuY2xlYXIoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY2hhbmdlZCBzaWduYWwuXG4gICAqL1xuICBnZXQgY2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIFQ+IHtcbiAgICByZXR1cm4gdGhpcy5fY2hhbmdlZDtcbiAgfVxuXG4gIHB1YmxpYyBpc0Rpc3Bvc2VkID0gZmFsc2U7XG4gIHB1YmxpYyB5ZG9jID0gbmV3IFkuRG9jKCk7XG4gIHB1YmxpYyBzb3VyY2UgPSB0aGlzLnlkb2MuZ2V0VGV4dCgnc291cmNlJyk7XG4gIHB1YmxpYyB5c3RhdGU6IFkuTWFwPGFueT4gPSB0aGlzLnlkb2MuZ2V0TWFwKCdzdGF0ZScpO1xuICBwdWJsaWMgdW5kb01hbmFnZXIgPSBuZXcgWS5VbmRvTWFuYWdlcihbdGhpcy5zb3VyY2VdLCB7XG4gICAgdHJhY2tlZE9yaWdpbnM6IG5ldyBTZXQoW3RoaXNdKVxuICB9KTtcbiAgcHVibGljIGF3YXJlbmVzcyA9IG5ldyBBd2FyZW5lc3ModGhpcy55ZG9jKTtcbiAgcHJvdGVjdGVkIF9jaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBUPih0aGlzKTtcbn1cblxuZXhwb3J0IGNsYXNzIFlGaWxlXG4gIGV4dGVuZHMgWURvY3VtZW50PG1vZGVscy5GaWxlQ2hhbmdlPlxuICBpbXBsZW1lbnRzIG1vZGVscy5JU2hhcmVkRmlsZSwgbW9kZWxzLklTaGFyZWRUZXh0LCBJWVRleHQge1xuICBjb25zdHJ1Y3RvcigpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMueXNvdXJjZS5vYnNlcnZlKHRoaXMuX21vZGVsT2JzZXJ2ZXIpO1xuICAgIHRoaXMueXN0YXRlLm9ic2VydmUodGhpcy5fb25TdGF0ZUNoYW5nZWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcy5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgdGhpcy55c291cmNlLnVub2JzZXJ2ZSh0aGlzLl9tb2RlbE9ic2VydmVyKTtcbiAgICB0aGlzLnlzdGF0ZS51bm9ic2VydmUodGhpcy5fb25TdGF0ZUNoYW5nZWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgeW1vZGVsLlxuICAgKi9cbiAgcHJpdmF0ZSBfbW9kZWxPYnNlcnZlciA9IChldmVudDogWS5ZVGV4dEV2ZW50KSA9PiB7XG4gICAgY29uc3QgY2hhbmdlczogbW9kZWxzLkZpbGVDaGFuZ2UgPSB7fTtcbiAgICBjaGFuZ2VzLnNvdXJjZUNoYW5nZSA9IGV2ZW50LmNoYW5nZXMuZGVsdGEgYXMgYW55O1xuICAgIHRoaXMuX2NoYW5nZWQuZW1pdChjaGFuZ2VzKTtcbiAgfTtcblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSB5c3RhdGUuXG4gICAqL1xuICBwcml2YXRlIF9vblN0YXRlQ2hhbmdlZCA9IChldmVudDogWS5ZTWFwRXZlbnQ8YW55PikgPT4ge1xuICAgIGNvbnN0IHN0YXRlQ2hhbmdlOiBhbnkgPSBbXTtcblxuICAgIGV2ZW50LmtleXNDaGFuZ2VkLmZvckVhY2goa2V5ID0+IHtcbiAgICAgIGNvbnN0IGNoYW5nZSA9IGV2ZW50LmNoYW5nZXMua2V5cy5nZXQoa2V5KTtcbiAgICAgIGlmIChjaGFuZ2UpIHtcbiAgICAgICAgc3RhdGVDaGFuZ2UucHVzaCh7XG4gICAgICAgICAgbmFtZToga2V5LFxuICAgICAgICAgIG9sZFZhbHVlOiBjaGFuZ2Uub2xkVmFsdWUsXG4gICAgICAgICAgbmV3VmFsdWU6IHRoaXMueXN0YXRlLmdldChrZXkpXG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHsgc3RhdGVDaGFuZ2UgfSk7XG4gIH07XG5cbiAgcHVibGljIHN0YXRpYyBjcmVhdGUoKTogWUZpbGUge1xuICAgIHJldHVybiBuZXcgWUZpbGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXRzIGNlbGwncyBzb3VyY2UuXG4gICAqXG4gICAqIEByZXR1cm5zIENlbGwncyBzb3VyY2UuXG4gICAqL1xuICBwdWJsaWMgZ2V0U291cmNlKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMueXNvdXJjZS50b1N0cmluZygpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldHMgY2VsbCdzIHNvdXJjZS5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlOiBOZXcgc291cmNlLlxuICAgKi9cbiAgcHVibGljIHNldFNvdXJjZSh2YWx1ZTogc3RyaW5nKTogdm9pZCB7XG4gICAgdGhpcy50cmFuc2FjdCgoKSA9PiB7XG4gICAgICBjb25zdCB5dGV4dCA9IHRoaXMueXNvdXJjZTtcbiAgICAgIHl0ZXh0LmRlbGV0ZSgwLCB5dGV4dC5sZW5ndGgpO1xuICAgICAgeXRleHQuaW5zZXJ0KDAsIHZhbHVlKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXBsYWNlIGNvbnRlbnQgZnJvbSBgc3RhcnQnIHRvIGBlbmRgIHdpdGggYHZhbHVlYC5cbiAgICpcbiAgICogQHBhcmFtIHN0YXJ0OiBUaGUgc3RhcnQgaW5kZXggb2YgdGhlIHJhbmdlIHRvIHJlcGxhY2UgKGluY2x1c2l2ZSkuXG4gICAqXG4gICAqIEBwYXJhbSBlbmQ6IFRoZSBlbmQgaW5kZXggb2YgdGhlIHJhbmdlIHRvIHJlcGxhY2UgKGV4Y2x1c2l2ZSkuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZTogTmV3IHNvdXJjZSAob3B0aW9uYWwpLlxuICAgKi9cbiAgcHVibGljIHVwZGF0ZVNvdXJjZShzdGFydDogbnVtYmVyLCBlbmQ6IG51bWJlciwgdmFsdWUgPSAnJyk6IHZvaWQge1xuICAgIHRoaXMudHJhbnNhY3QoKCkgPT4ge1xuICAgICAgY29uc3QgeXNvdXJjZSA9IHRoaXMueXNvdXJjZTtcbiAgICAgIC8vIGluc2VydCBhbmQgdGhlbiBkZWxldGUuXG4gICAgICAvLyBUaGlzIGVuc3VyZXMgdGhhdCB0aGUgY3Vyc29yIHBvc2l0aW9uIGlzIGFkanVzdGVkIGFmdGVyIHRoZSByZXBsYWNlZCBjb250ZW50LlxuICAgICAgeXNvdXJjZS5pbnNlcnQoc3RhcnQsIHZhbHVlKTtcbiAgICAgIHlzb3VyY2UuZGVsZXRlKHN0YXJ0ICsgdmFsdWUubGVuZ3RoLCBlbmQgLSBzdGFydCk7XG4gICAgfSk7XG4gIH1cblxuICBwdWJsaWMgeXNvdXJjZSA9IHRoaXMueWRvYy5nZXRUZXh0KCdzb3VyY2UnKTtcbn1cblxuLyoqXG4gKiBTaGFyZWQgaW1wbGVtZW50YXRpb24gb2YgdGhlIFNoYXJlZCBEb2N1bWVudCB0eXBlcy5cbiAqXG4gKiBTaGFyZWQgY2VsbHMgY2FuIGJlIGluc2VydGVkIGludG8gYSBTaGFyZWROb3RlYm9vay5cbiAqIFNoYXJlZCBjZWxscyBvbmx5IHN0YXJ0IGVtaXR0aW5nIGV2ZW50cyB3aGVuIHRoZXkgYXJlIGNvbm5lY3RlZCB0byBhIFNoYXJlZE5vdGVib29rLlxuICpcbiAqIFwiU3RhbmRhbG9uZVwiIGNlbGxzIG11c3Qgbm90IGJlIGluc2VydGVkIGludG8gYSAoU2hhcmVkKU5vdGVib29rLlxuICogU3RhbmRhbG9uZSBjZWxscyBlbWl0IGV2ZW50cyBpbW1lZGlhdGVseSBhZnRlciB0aGV5IGhhdmUgYmVlbiBjcmVhdGVkLCBidXQgdGhleSBtdXN0IG5vdFxuICogYmUgaW5jbHVkZWQgaW50byBhIChTaGFyZWQpTm90ZWJvb2suXG4gKi9cbmV4cG9ydCBjbGFzcyBZTm90ZWJvb2tcbiAgZXh0ZW5kcyBZRG9jdW1lbnQ8bW9kZWxzLk5vdGVib29rQ2hhbmdlPlxuICBpbXBsZW1lbnRzIG1vZGVscy5JU2hhcmVkTm90ZWJvb2sge1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJU2hhcmVkTm90ZWJvb2suSU9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuX2Rpc2FibGVEb2N1bWVudFdpZGVVbmRvUmVkbyA9IG9wdGlvbnMuZGlzYWJsZURvY3VtZW50V2lkZVVuZG9SZWRvO1xuICAgIHRoaXMueWNlbGxzLm9ic2VydmUodGhpcy5fb25ZQ2VsbHNDaGFuZ2VkKTtcbiAgICB0aGlzLmNlbGxzID0gdGhpcy55Y2VsbHMudG9BcnJheSgpLm1hcCh5Y2VsbCA9PiB7XG4gICAgICBpZiAoIXRoaXMuX3ljZWxsTWFwcGluZy5oYXMoeWNlbGwpKSB7XG4gICAgICAgIHRoaXMuX3ljZWxsTWFwcGluZy5zZXQoeWNlbGwsIGNyZWF0ZUNlbGxGcm9tVHlwZSh5Y2VsbCkpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHRoaXMuX3ljZWxsTWFwcGluZy5nZXQoeWNlbGwpIGFzIFlDZWxsVHlwZTtcbiAgICB9KTtcblxuICAgIHRoaXMueW1ldGEub2JzZXJ2ZSh0aGlzLl9vbk1ldGFkYXRhQ2hhbmdlZCk7XG4gICAgdGhpcy55c3RhdGUub2JzZXJ2ZSh0aGlzLl9vblN0YXRlQ2hhbmdlZCk7XG4gIH1cblxuICBnZXQgbmJmb3JtYXQoKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy55c3RhdGUuZ2V0KCduYmZvcm1hdCcpO1xuICB9XG5cbiAgc2V0IG5iZm9ybWF0KHZhbHVlOiBudW1iZXIpIHtcbiAgICB0aGlzLnRyYW5zYWN0KCgpID0+IHtcbiAgICAgIHRoaXMueXN0YXRlLnNldCgnbmJmb3JtYXQnLCB2YWx1ZSk7XG4gICAgfSwgZmFsc2UpO1xuICB9XG5cbiAgZ2V0IG5iZm9ybWF0X21pbm9yKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMueXN0YXRlLmdldCgnbmJmb3JtYXRNaW5vcicpO1xuICB9XG5cbiAgc2V0IG5iZm9ybWF0X21pbm9yKHZhbHVlOiBudW1iZXIpIHtcbiAgICB0aGlzLnRyYW5zYWN0KCgpID0+IHtcbiAgICAgIHRoaXMueXN0YXRlLnNldCgnbmJmb3JtYXRNaW5vcicsIHZhbHVlKTtcbiAgICB9LCBmYWxzZSk7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICB0aGlzLnljZWxscy51bm9ic2VydmUodGhpcy5fb25ZQ2VsbHNDaGFuZ2VkKTtcbiAgICB0aGlzLnltZXRhLnVub2JzZXJ2ZSh0aGlzLl9vbk1ldGFkYXRhQ2hhbmdlZCk7XG4gICAgdGhpcy55c3RhdGUudW5vYnNlcnZlKHRoaXMuX29uU3RhdGVDaGFuZ2VkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgYSBzaGFyZWQgY2VsbCBieSBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4OiBDZWxsJ3MgcG9zaXRpb24uXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSByZXF1ZXN0ZWQgc2hhcmVkIGNlbGwuXG4gICAqL1xuICBnZXRDZWxsKGluZGV4OiBudW1iZXIpOiBZQ2VsbFR5cGUge1xuICAgIHJldHVybiB0aGlzLmNlbGxzW2luZGV4XTtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbnNlcnQgYSBzaGFyZWQgY2VsbCBpbnRvIGEgc3BlY2lmaWMgcG9zaXRpb24uXG4gICAqXG4gICAqIEBwYXJhbSBpbmRleDogQ2VsbCdzIHBvc2l0aW9uLlxuICAgKlxuICAgKiBAcGFyYW0gY2VsbDogQ2VsbCB0byBpbnNlcnQuXG4gICAqL1xuICBpbnNlcnRDZWxsKGluZGV4OiBudW1iZXIsIGNlbGw6IFlDZWxsVHlwZSk6IHZvaWQge1xuICAgIHRoaXMuaW5zZXJ0Q2VsbHMoaW5kZXgsIFtjZWxsXSk7XG4gIH1cblxuICAvKipcbiAgICogSW5zZXJ0IGEgbGlzdCBvZiBzaGFyZWQgY2VsbHMgaW50byBhIHNwZWNpZmljIHBvc2l0aW9uLlxuICAgKlxuICAgKiBAcGFyYW0gaW5kZXg6IFBvc2l0aW9uIHRvIGluc2VydCB0aGUgY2VsbHMuXG4gICAqXG4gICAqIEBwYXJhbSBjZWxsczogQXJyYXkgb2Ygc2hhcmVkIGNlbGxzIHRvIGluc2VydC5cbiAgICovXG4gIGluc2VydENlbGxzKGluZGV4OiBudW1iZXIsIGNlbGxzOiBZQ2VsbFR5cGVbXSk6IHZvaWQge1xuICAgIGNlbGxzLmZvckVhY2goY2VsbCA9PiB7XG4gICAgICB0aGlzLl95Y2VsbE1hcHBpbmcuc2V0KGNlbGwueW1vZGVsLCBjZWxsKTtcbiAgICAgIGlmICghdGhpcy5kaXNhYmxlRG9jdW1lbnRXaWRlVW5kb1JlZG8pIHtcbiAgICAgICAgY2VsbC51bmRvTWFuYWdlciA9IHRoaXMudW5kb01hbmFnZXI7XG4gICAgICB9XG4gICAgfSk7XG4gICAgdGhpcy50cmFuc2FjdCgoKSA9PiB7XG4gICAgICB0aGlzLnljZWxscy5pbnNlcnQoXG4gICAgICAgIGluZGV4LFxuICAgICAgICBjZWxscy5tYXAoY2VsbCA9PiBjZWxsLnltb2RlbClcbiAgICAgICk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogTW92ZSBhIGNlbGwuXG4gICAqXG4gICAqIEBwYXJhbSBmcm9tSW5kZXg6IEluZGV4IG9mIHRoZSBjZWxsIHRvIG1vdmUuXG4gICAqXG4gICAqIEBwYXJhbSB0b0luZGV4OiBOZXcgcG9zaXRpb24gb2YgdGhlIGNlbGwuXG4gICAqL1xuICBtb3ZlQ2VsbChmcm9tSW5kZXg6IG51bWJlciwgdG9JbmRleDogbnVtYmVyKTogdm9pZCB7XG4gICAgdGhpcy50cmFuc2FjdCgoKSA9PiB7XG4gICAgICBjb25zdCBmcm9tQ2VsbDogYW55ID0gdGhpcy5nZXRDZWxsKGZyb21JbmRleCkuY2xvbmUoKTtcbiAgICAgIHRoaXMuZGVsZXRlQ2VsbChmcm9tSW5kZXgpO1xuICAgICAgdGhpcy5pbnNlcnRDZWxsKHRvSW5kZXgsIGZyb21DZWxsKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBjZWxsLlxuICAgKlxuICAgKiBAcGFyYW0gaW5kZXg6IEluZGV4IG9mIHRoZSBjZWxsIHRvIHJlbW92ZS5cbiAgICovXG4gIGRlbGV0ZUNlbGwoaW5kZXg6IG51bWJlcik6IHZvaWQge1xuICAgIHRoaXMuZGVsZXRlQ2VsbFJhbmdlKGluZGV4LCBpbmRleCArIDEpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhIHJhbmdlIG9mIGNlbGxzLlxuICAgKlxuICAgKiBAcGFyYW0gZnJvbTogVGhlIHN0YXJ0IGluZGV4IG9mIHRoZSByYW5nZSB0byByZW1vdmUgKGluY2x1c2l2ZSkuXG4gICAqXG4gICAqIEBwYXJhbSB0bzogVGhlIGVuZCBpbmRleCBvZiB0aGUgcmFuZ2UgdG8gcmVtb3ZlIChleGNsdXNpdmUpLlxuICAgKi9cbiAgZGVsZXRlQ2VsbFJhbmdlKGZyb206IG51bWJlciwgdG86IG51bWJlcik6IHZvaWQge1xuICAgIHRoaXMudHJhbnNhY3QoKCkgPT4ge1xuICAgICAgdGhpcy55Y2VsbHMuZGVsZXRlKGZyb20sIHRvIC0gZnJvbSk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJucyB0aGUgbWV0YWRhdGEgYXNzb2NpYXRlZCB3aXRoIHRoZSBub3RlYm9vay5cbiAgICpcbiAgICogQHJldHVybnMgTm90ZWJvb2sncyBtZXRhZGF0YS5cbiAgICovXG4gIGdldE1ldGFkYXRhKCk6IG5iZm9ybWF0LklOb3RlYm9va01ldGFkYXRhIHtcbiAgICBjb25zdCBtZXRhID0gdGhpcy55bWV0YS5nZXQoJ21ldGFkYXRhJyk7XG4gICAgcmV0dXJuIG1ldGEgPyBkZWVwQ29weShtZXRhKSA6IHt9O1xuICB9XG5cbiAgLyoqXG4gICAqIFNldHMgdGhlIG1ldGFkYXRhIGFzc29jaWF0ZWQgd2l0aCB0aGUgbm90ZWJvb2suXG4gICAqXG4gICAqIEBwYXJhbSBtZXRhZGF0YTogTm90ZWJvb2sncyBtZXRhZGF0YS5cbiAgICovXG4gIHNldE1ldGFkYXRhKHZhbHVlOiBuYmZvcm1hdC5JTm90ZWJvb2tNZXRhZGF0YSk6IHZvaWQge1xuICAgIHRoaXMueW1ldGEuc2V0KCdtZXRhZGF0YScsIGRlZXBDb3B5KHZhbHVlKSk7XG4gIH1cblxuICAvKipcbiAgICogVXBkYXRlcyB0aGUgbWV0YWRhdGEgYXNzb2NpYXRlZCB3aXRoIHRoZSBub3RlYm9vay5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlOiBNZXRhZGF0YSdzIGF0dHJpYnV0ZSB0byB1cGRhdGUuXG4gICAqL1xuICB1cGRhdGVNZXRhZGF0YSh2YWx1ZTogUGFydGlhbDxuYmZvcm1hdC5JTm90ZWJvb2tNZXRhZGF0YT4pOiB2b2lkIHtcbiAgICAvLyBUT0RPOiBNYXliZSBtb2RpZnkgb25seSBhdHRyaWJ1dGVzIGluc3RlYWQgb2YgcmVwbGFjaW5nIHRoZSB3aG9sZSBtZXRhZGF0YT9cbiAgICB0aGlzLnltZXRhLnNldCgnbWV0YWRhdGEnLCBPYmplY3QuYXNzaWduKHt9LCB0aGlzLmdldE1ldGFkYXRhKCksIHZhbHVlKSk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IFlOb3RlYm9vay5cbiAgICovXG4gIHB1YmxpYyBzdGF0aWMgY3JlYXRlKFxuICAgIGRpc2FibGVEb2N1bWVudFdpZGVVbmRvUmVkbzogYm9vbGVhblxuICApOiBtb2RlbHMuSVNoYXJlZE5vdGVib29rIHtcbiAgICByZXR1cm4gbmV3IFlOb3RlYm9vayh7IGRpc2FibGVEb2N1bWVudFdpZGVVbmRvUmVkbyB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXZXRoZXIgdGhlIHRoZSB1bmRvL3JlZG8gbG9naWMgc2hvdWxkIGJlXG4gICAqIGNvbnNpZGVyZWQgb24gdGhlIGZ1bGwgZG9jdW1lbnQgYWNyb3NzIGFsbCBjZWxscy5cbiAgICpcbiAgICogQHJldHVybiBUaGUgZGlzYWJsZURvY3VtZW50V2lkZVVuZG9SZWRvIHNldHRpbmcuXG4gICAqL1xuICBnZXQgZGlzYWJsZURvY3VtZW50V2lkZVVuZG9SZWRvKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9kaXNhYmxlRG9jdW1lbnRXaWRlVW5kb1JlZG87XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSBsaXN0IG9mIGNlbGxzLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25ZQ2VsbHNDaGFuZ2VkID0gKGV2ZW50OiBZLllBcnJheUV2ZW50PFkuTWFwPGFueT4+KSA9PiB7XG4gICAgLy8gdXBkYXRlIHRoZSB0eXBl4oeUY2VsbCBtYXBwaW5nIGJ5IGl0ZXJhdGluZyB0aHJvdWdoIHRoZSBhZGRlZC9yZW1vdmVkIHR5cGVzXG4gICAgZXZlbnQuY2hhbmdlcy5hZGRlZC5mb3JFYWNoKGl0ZW0gPT4ge1xuICAgICAgY29uc3QgdHlwZSA9IChpdGVtLmNvbnRlbnQgYXMgWS5Db250ZW50VHlwZSkudHlwZSBhcyBZLk1hcDxhbnk+O1xuICAgICAgaWYgKCF0aGlzLl95Y2VsbE1hcHBpbmcuaGFzKHR5cGUpKSB7XG4gICAgICAgIHRoaXMuX3ljZWxsTWFwcGluZy5zZXQodHlwZSwgY3JlYXRlQ2VsbEZyb21UeXBlKHR5cGUpKTtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGNlbGwgPSB0aGlzLl95Y2VsbE1hcHBpbmcuZ2V0KHR5cGUpIGFzIGFueTtcbiAgICAgIGNlbGwuX25vdGVib29rID0gdGhpcztcbiAgICAgIGlmICghdGhpcy5kaXNhYmxlRG9jdW1lbnRXaWRlVW5kb1JlZG8pIHtcbiAgICAgICAgY2VsbC5fdW5kb01hbmFnZXIgPSB0aGlzLnVuZG9NYW5hZ2VyO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgY2VsbC5fdW5kb01hbmFnZXIgPSBuZXcgWS5VbmRvTWFuYWdlcihbY2VsbC55bW9kZWxdLCB7fSk7XG4gICAgICB9XG4gICAgfSk7XG4gICAgZXZlbnQuY2hhbmdlcy5kZWxldGVkLmZvckVhY2goaXRlbSA9PiB7XG4gICAgICBjb25zdCB0eXBlID0gKGl0ZW0uY29udGVudCBhcyBZLkNvbnRlbnRUeXBlKS50eXBlIGFzIFkuTWFwPGFueT47XG4gICAgICBjb25zdCBtb2RlbCA9IHRoaXMuX3ljZWxsTWFwcGluZy5nZXQodHlwZSk7XG4gICAgICBpZiAobW9kZWwpIHtcbiAgICAgICAgbW9kZWwuZGlzcG9zZSgpO1xuICAgICAgICB0aGlzLl95Y2VsbE1hcHBpbmcuZGVsZXRlKHR5cGUpO1xuICAgICAgfVxuICAgIH0pO1xuICAgIGxldCBpbmRleCA9IDA7XG4gICAgLy8gdGhpcyByZWZsZWN0cyB0aGUgZXZlbnQuY2hhbmdlcy5kZWx0YSwgYnV0IHJlcGxhY2VzIHRoZSBjb250ZW50IG9mIGRlbHRhLmluc2VydCB3aXRoIHljZWxsc1xuICAgIGNvbnN0IGNlbGxzQ2hhbmdlOiBEZWx0YTxtb2RlbHMuSVNoYXJlZENlbGxbXT4gPSBbXTtcbiAgICBldmVudC5jaGFuZ2VzLmRlbHRhLmZvckVhY2goKGQ6IGFueSkgPT4ge1xuICAgICAgaWYgKGQuaW5zZXJ0ICE9IG51bGwpIHtcbiAgICAgICAgY29uc3QgaW5zZXJ0ZWRDZWxscyA9IGQuaW5zZXJ0Lm1hcCgoeWNlbGw6IFkuTWFwPGFueT4pID0+XG4gICAgICAgICAgdGhpcy5feWNlbGxNYXBwaW5nLmdldCh5Y2VsbClcbiAgICAgICAgKTtcbiAgICAgICAgY2VsbHNDaGFuZ2UucHVzaCh7IGluc2VydDogaW5zZXJ0ZWRDZWxscyB9KTtcbiAgICAgICAgdGhpcy5jZWxscy5zcGxpY2UoaW5kZXgsIDAsIC4uLmluc2VydGVkQ2VsbHMpO1xuICAgICAgICBpbmRleCArPSBkLmluc2VydC5sZW5ndGg7XG4gICAgICB9IGVsc2UgaWYgKGQuZGVsZXRlICE9IG51bGwpIHtcbiAgICAgICAgY2VsbHNDaGFuZ2UucHVzaChkKTtcbiAgICAgICAgdGhpcy5jZWxscy5zcGxpY2UoaW5kZXgsIGQuZGVsZXRlKTtcbiAgICAgIH0gZWxzZSBpZiAoZC5yZXRhaW4gIT0gbnVsbCkge1xuICAgICAgICBjZWxsc0NoYW5nZS5wdXNoKGQpO1xuICAgICAgICBpbmRleCArPSBkLnJldGFpbjtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7XG4gICAgICBjZWxsc0NoYW5nZTogY2VsbHNDaGFuZ2VcbiAgICB9KTtcbiAgfTtcblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSB5c3RhdGUuXG4gICAqL1xuICBwcml2YXRlIF9vbk1ldGFkYXRhQ2hhbmdlZCA9IChldmVudDogWS5ZTWFwRXZlbnQ8YW55PikgPT4ge1xuICAgIGlmIChldmVudC5rZXlzQ2hhbmdlZC5oYXMoJ21ldGFkYXRhJykpIHtcbiAgICAgIGNvbnN0IGNoYW5nZSA9IGV2ZW50LmNoYW5nZXMua2V5cy5nZXQoJ21ldGFkYXRhJyk7XG4gICAgICBjb25zdCBtZXRhZGF0YUNoYW5nZSA9IHtcbiAgICAgICAgb2xkVmFsdWU6IGNoYW5nZT8ub2xkVmFsdWUgPyBjaGFuZ2UhLm9sZFZhbHVlIDogdW5kZWZpbmVkLFxuICAgICAgICBuZXdWYWx1ZTogdGhpcy5nZXRNZXRhZGF0YSgpXG4gICAgICB9O1xuICAgICAgdGhpcy5fY2hhbmdlZC5lbWl0KHsgbWV0YWRhdGFDaGFuZ2UgfSk7XG4gICAgfVxuICB9O1xuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIHlzdGF0ZS5cbiAgICovXG4gIHByaXZhdGUgX29uU3RhdGVDaGFuZ2VkID0gKGV2ZW50OiBZLllNYXBFdmVudDxhbnk+KSA9PiB7XG4gICAgY29uc3Qgc3RhdGVDaGFuZ2U6IGFueSA9IFtdO1xuICAgIGV2ZW50LmtleXNDaGFuZ2VkLmZvckVhY2goa2V5ID0+IHtcbiAgICAgIGNvbnN0IGNoYW5nZSA9IGV2ZW50LmNoYW5nZXMua2V5cy5nZXQoa2V5KTtcbiAgICAgIGlmIChjaGFuZ2UpIHtcbiAgICAgICAgc3RhdGVDaGFuZ2UucHVzaCh7XG4gICAgICAgICAgbmFtZToga2V5LFxuICAgICAgICAgIG9sZFZhbHVlOiBjaGFuZ2Uub2xkVmFsdWUsXG4gICAgICAgICAgbmV3VmFsdWU6IHRoaXMueXN0YXRlLmdldChrZXkpXG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHsgc3RhdGVDaGFuZ2UgfSk7XG4gIH07XG5cbiAgcHVibGljIHljZWxsczogWS5BcnJheTxZLk1hcDxhbnk+PiA9IHRoaXMueWRvYy5nZXRBcnJheSgnY2VsbHMnKTtcbiAgcHVibGljIHltZXRhOiBZLk1hcDxhbnk+ID0gdGhpcy55ZG9jLmdldE1hcCgnbWV0YScpO1xuICBwdWJsaWMgeW1vZGVsOiBZLk1hcDxhbnk+ID0gdGhpcy55ZG9jLmdldE1hcCgnbW9kZWwnKTtcbiAgcHVibGljIHVuZG9NYW5hZ2VyID0gbmV3IFkuVW5kb01hbmFnZXIoW3RoaXMueWNlbGxzXSwge1xuICAgIHRyYWNrZWRPcmlnaW5zOiBuZXcgU2V0KFt0aGlzXSlcbiAgfSk7XG4gIHByaXZhdGUgX2Rpc2FibGVEb2N1bWVudFdpZGVVbmRvUmVkbzogYm9vbGVhbjtcbiAgcHJpdmF0ZSBfeWNlbGxNYXBwaW5nOiBNYXA8WS5NYXA8YW55PiwgWUNlbGxUeXBlPiA9IG5ldyBNYXAoKTtcbiAgcHVibGljIGNlbGxzOiBZQ2VsbFR5cGVbXTtcbn1cblxuLyoqXG4gKiBDcmVhdGUgYSBuZXcgc2hhcmVkIGNlbGwgZ2l2ZW4gdGhlIHR5cGUuXG4gKi9cbmV4cG9ydCBjb25zdCBjcmVhdGVDZWxsRnJvbVR5cGUgPSAodHlwZTogWS5NYXA8YW55Pik6IFlDZWxsVHlwZSA9PiB7XG4gIHN3aXRjaCAodHlwZS5nZXQoJ2NlbGxfdHlwZScpKSB7XG4gICAgY2FzZSAnY29kZSc6XG4gICAgICByZXR1cm4gbmV3IFlDb2RlQ2VsbCh0eXBlKTtcbiAgICBjYXNlICdtYXJrZG93bic6XG4gICAgICByZXR1cm4gbmV3IFlNYXJrZG93bkNlbGwodHlwZSk7XG4gICAgY2FzZSAncmF3JzpcbiAgICAgIHJldHVybiBuZXcgWVJhd0NlbGwodHlwZSk7XG4gICAgZGVmYXVsdDpcbiAgICAgIHRocm93IG5ldyBFcnJvcignRm91bmQgdW5rbm93biBjZWxsIHR5cGUnKTtcbiAgfVxufTtcblxuLyoqXG4gKiBDcmVhdGUgYSBuZXcgc3RhbmRhbG9uZSBjZWxsIGdpdmVuIHRoZSB0eXBlLlxuICovXG5leHBvcnQgY29uc3QgY3JlYXRlU3RhbmRhbG9uZUNlbGwgPSAoXG4gIGNlbGxUeXBlOiAncmF3JyB8ICdjb2RlJyB8ICdtYXJrZG93bicsXG4gIGlkPzogc3RyaW5nXG4pOiBZQ2VsbFR5cGUgPT4ge1xuICBzd2l0Y2ggKGNlbGxUeXBlKSB7XG4gICAgY2FzZSAnbWFya2Rvd24nOlxuICAgICAgcmV0dXJuIFlNYXJrZG93bkNlbGwuY3JlYXRlU3RhbmRhbG9uZShpZCk7XG4gICAgY2FzZSAnY29kZSc6XG4gICAgICByZXR1cm4gWUNvZGVDZWxsLmNyZWF0ZVN0YW5kYWxvbmUoaWQpO1xuICAgIGRlZmF1bHQ6XG4gICAgICAvLyByYXdcbiAgICAgIHJldHVybiBZUmF3Q2VsbC5jcmVhdGVTdGFuZGFsb25lKGlkKTtcbiAgfVxufTtcblxuZXhwb3J0IGNsYXNzIFlCYXNlQ2VsbDxNZXRhZGF0YSBleHRlbmRzIG1vZGVscy5JU2hhcmVkQmFzZUNlbGxNZXRhZGF0YT5cbiAgaW1wbGVtZW50cyBtb2RlbHMuSVNoYXJlZEJhc2VDZWxsPE1ldGFkYXRhPiwgSVlUZXh0IHtcbiAgY29uc3RydWN0b3IoeW1vZGVsOiBZLk1hcDxhbnk+KSB7XG4gICAgdGhpcy55bW9kZWwgPSB5bW9kZWw7XG4gICAgY29uc3QgeXNvdXJjZSA9IHltb2RlbC5nZXQoJ3NvdXJjZScpO1xuICAgIHRoaXMuX3ByZXZTb3VyY2VMZW5ndGggPSB5c291cmNlID8geXNvdXJjZS5sZW5ndGggOiAwO1xuICAgIHRoaXMueW1vZGVsLm9ic2VydmVEZWVwKHRoaXMuX21vZGVsT2JzZXJ2ZXIpO1xuICAgIHRoaXMuX2F3YXJlbmVzcyA9IG51bGw7XG4gIH1cblxuICBnZXQgeXNvdXJjZSgpOiBZLlRleHQge1xuICAgIHJldHVybiB0aGlzLnltb2RlbC5nZXQoJ3NvdXJjZScpO1xuICB9XG5cbiAgZ2V0IGF3YXJlbmVzcygpOiBBd2FyZW5lc3MgfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fYXdhcmVuZXNzID8/IHRoaXMubm90ZWJvb2s/LmF3YXJlbmVzcyA/PyBudWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIFBlcmZvcm0gYSB0cmFuc2FjdGlvbi4gV2hpbGUgdGhlIGZ1bmN0aW9uIGYgaXMgY2FsbGVkLCBhbGwgY2hhbmdlcyB0byB0aGUgc2hhcmVkXG4gICAqIGRvY3VtZW50IGFyZSBidW5kbGVkIGludG8gYSBzaW5nbGUgZXZlbnQuXG4gICAqL1xuICB0cmFuc2FjdChmOiAoKSA9PiB2b2lkLCB1bmRvYWJsZSA9IHRydWUpOiB2b2lkIHtcbiAgICB0aGlzLm5vdGVib29rICYmIHVuZG9hYmxlXG4gICAgICA/IHRoaXMubm90ZWJvb2sudHJhbnNhY3QoZilcbiAgICAgIDogdGhpcy55bW9kZWwuZG9jIS50cmFuc2FjdChmLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbm90ZWJvb2sgdGhhdCB0aGlzIGNlbGwgYmVsb25ncyB0by5cbiAgICovXG4gIGdldCB1bmRvTWFuYWdlcigpOiBZLlVuZG9NYW5hZ2VyIHwgbnVsbCB7XG4gICAgaWYgKCF0aGlzLm5vdGVib29rKSB7XG4gICAgICByZXR1cm4gdGhpcy5fdW5kb01hbmFnZXI7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLm5vdGVib29rPy5kaXNhYmxlRG9jdW1lbnRXaWRlVW5kb1JlZG9cbiAgICAgID8gdGhpcy5fdW5kb01hbmFnZXJcbiAgICAgIDogdGhpcy5ub3RlYm9vay51bmRvTWFuYWdlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHVuZG9NYW5hZ2VyIHdoZW4gYWRkaW5nIG5ldyBjZWxscy5cbiAgICovXG4gIHNldCB1bmRvTWFuYWdlcih1bmRvTWFuYWdlcjogWS5VbmRvTWFuYWdlciB8IG51bGwpIHtcbiAgICB0aGlzLl91bmRvTWFuYWdlciA9IHVuZG9NYW5hZ2VyO1xuICB9XG5cbiAgLyoqXG4gICAqIFVuZG8gYW4gb3BlcmF0aW9uLlxuICAgKi9cbiAgdW5kbygpOiB2b2lkIHtcbiAgICB0aGlzLnVuZG9NYW5hZ2VyPy51bmRvKCk7XG4gIH1cblxuICAvKipcbiAgICogUmVkbyBhbiBvcGVyYXRpb24uXG4gICAqL1xuICByZWRvKCk6IHZvaWQge1xuICAgIHRoaXMudW5kb01hbmFnZXI/LnJlZG8oKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBvYmplY3QgY2FuIHVuZG8gY2hhbmdlcy5cbiAgICovXG4gIGNhblVuZG8oKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuICEhdGhpcy51bmRvTWFuYWdlciAmJiB0aGlzLnVuZG9NYW5hZ2VyLnVuZG9TdGFjay5sZW5ndGggPiAwO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG9iamVjdCBjYW4gcmVkbyBjaGFuZ2VzLlxuICAgKi9cbiAgY2FuUmVkbygpOiBib29sZWFuIHtcbiAgICByZXR1cm4gISF0aGlzLnVuZG9NYW5hZ2VyICYmIHRoaXMudW5kb01hbmFnZXIucmVkb1N0YWNrLmxlbmd0aCA+IDA7XG4gIH1cblxuICAvKipcbiAgICogQ2xlYXIgdGhlIGNoYW5nZSBzdGFjay5cbiAgICovXG4gIGNsZWFyVW5kb0hpc3RvcnkoKTogdm9pZCB7XG4gICAgdGhpcy51bmRvTWFuYWdlcj8uY2xlYXIoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbm90ZWJvb2sgdGhhdCB0aGlzIGNlbGwgYmVsb25ncyB0by5cbiAgICovXG4gIGdldCBub3RlYm9vaygpOiBZTm90ZWJvb2sgfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fbm90ZWJvb2s7XG4gIH1cblxuICAvKipcbiAgICogVGhlIG5vdGVib29rIHRoYXQgdGhpcyBjZWxsIGJlbG9uZ3MgdG8uXG4gICAqL1xuICBwcm90ZWN0ZWQgX25vdGVib29rOiBZTm90ZWJvb2sgfCBudWxsID0gbnVsbDtcblxuICAvKipcbiAgICogV2hldGhlciB0aGUgY2VsbCBpcyBzdGFuZGFsb25lIG9yIG5vdC5cbiAgICpcbiAgICogSWYgdGhlIGNlbGwgaXMgc3RhbmRhbG9uZS4gSXQgY2Fubm90IGJlXG4gICAqIGluc2VydGVkIGludG8gYSBZTm90ZWJvb2sgYmVjYXVzZSB0aGUgWWpzIG1vZGVsIGlzIGFscmVhZHlcbiAgICogYXR0YWNoZWQgdG8gYW4gYW5vbnltb3VzIFkuRG9jIGluc3RhbmNlLlxuICAgKi9cbiAgaXNTdGFuZGFsb25lID0gZmFsc2U7XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBZUmF3Q2VsbCB0aGF0IGNhbiBiZSBpbnNlcnRlZCBpbnRvIGEgWU5vdGVib29rXG4gICAqL1xuICBwdWJsaWMgc3RhdGljIGNyZWF0ZShpZCA9IFVVSUQudXVpZDQoKSk6IFlCYXNlQ2VsbDxhbnk+IHtcbiAgICBjb25zdCB5bW9kZWwgPSBuZXcgWS5NYXAoKTtcbiAgICBjb25zdCB5c291cmNlID0gbmV3IFkuVGV4dCgpO1xuICAgIHltb2RlbC5zZXQoJ3NvdXJjZScsIHlzb3VyY2UpO1xuICAgIHltb2RlbC5zZXQoJ21ldGFkYXRhJywge30pO1xuICAgIHltb2RlbC5zZXQoJ2NlbGxfdHlwZScsIHRoaXMucHJvdG90eXBlLmNlbGxfdHlwZSk7XG4gICAgeW1vZGVsLnNldCgnaWQnLCBpZCk7XG4gICAgcmV0dXJuIG5ldyB0aGlzKHltb2RlbCk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IFlSYXdDZWxsIHRoYXQgd29ya3Mgc3RhbmRhbG9uZS4gSXQgY2Fubm90IGJlXG4gICAqIGluc2VydGVkIGludG8gYSBZTm90ZWJvb2sgYmVjYXVzZSB0aGUgWWpzIG1vZGVsIGlzIGFscmVhZHlcbiAgICogYXR0YWNoZWQgdG8gYW4gYW5vbnltb3VzIFkuRG9jIGluc3RhbmNlLlxuICAgKi9cbiAgcHVibGljIHN0YXRpYyBjcmVhdGVTdGFuZGFsb25lKGlkPzogc3RyaW5nKTogWUJhc2VDZWxsPGFueT4ge1xuICAgIGNvbnN0IGNlbGwgPSB0aGlzLmNyZWF0ZShpZCk7XG4gICAgY2VsbC5pc1N0YW5kYWxvbmUgPSB0cnVlO1xuICAgIGNvbnN0IGRvYyA9IG5ldyBZLkRvYygpO1xuICAgIGRvYy5nZXRBcnJheSgpLmluc2VydCgwLCBbY2VsbC55bW9kZWxdKTtcbiAgICBjZWxsLl9hd2FyZW5lc3MgPSBuZXcgQXdhcmVuZXNzKGRvYyk7XG4gICAgY2VsbC5fdW5kb01hbmFnZXIgPSBuZXcgWS5VbmRvTWFuYWdlcihbY2VsbC55bW9kZWxdLCB7XG4gICAgICB0cmFja2VkT3JpZ2luczogbmV3IFNldChbY2VsbF0pXG4gICAgfSk7XG4gICAgcmV0dXJuIGNlbGw7XG4gIH1cblxuICAvKipcbiAgICogQ2xvbmUgdGhlIGNlbGwuXG4gICAqXG4gICAqIEB0b2RvIGNsb25lIHNob3VsZCBvbmx5IGJlIGF2YWlsYWJsZSBpbiB0aGUgc3BlY2lmaWMgaW1wbGVtZW50YXRpb25zIGkuZS4gSVNoYXJlZENvZGVDZWxsXG4gICAqL1xuICBwdWJsaWMgY2xvbmUoKTogWUJhc2VDZWxsPGFueT4ge1xuICAgIGNvbnN0IHltb2RlbCA9IG5ldyBZLk1hcCgpO1xuICAgIGNvbnN0IHlzb3VyY2UgPSBuZXcgWS5UZXh0KHRoaXMuZ2V0U291cmNlKCkpO1xuICAgIHltb2RlbC5zZXQoJ3NvdXJjZScsIHlzb3VyY2UpO1xuICAgIHltb2RlbC5zZXQoJ21ldGFkYXRhJywgdGhpcy5nZXRNZXRhZGF0YSgpKTtcbiAgICB5bW9kZWwuc2V0KCdjZWxsX3R5cGUnLCB0aGlzLmNlbGxfdHlwZSk7XG4gICAgeW1vZGVsLnNldCgnaWQnLCB0aGlzLmdldElkKCkpO1xuICAgIGNvbnN0IFNlbGY6IGFueSA9IHRoaXMuY29uc3RydWN0b3I7XG4gICAgY29uc3QgY2xvbmUgPSBuZXcgU2VsZih5bW9kZWwpO1xuICAgIC8vIFRPRE8gVGhlIGFzc2lnbm1lbnQgb2YgdGhlIHVuZG9NYW5hZ2VyIGRvZXMgbm90IHdvcmsgZm9yIGEgY2xvbmUuXG4gICAgLy8gU2VlIGh0dHBzOi8vZ2l0aHViLmNvbS9qdXB5dGVybGFiL2p1cHl0ZXJsYWIvaXNzdWVzLzExMDM1XG4gICAgY2xvbmUuX3VuZG9NYW5hZ2VyID0gdGhpcy51bmRvTWFuYWdlcjtcbiAgICByZXR1cm4gY2xvbmU7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSB5bW9kZWwuXG4gICAqL1xuICBwcml2YXRlIF9tb2RlbE9ic2VydmVyID0gKGV2ZW50czogWS5ZRXZlbnRbXSkgPT4ge1xuICAgIGNvbnN0IGNoYW5nZXM6IG1vZGVscy5DZWxsQ2hhbmdlPE1ldGFkYXRhPiA9IHt9O1xuICAgIGNvbnN0IHNvdXJjZUV2ZW50ID0gZXZlbnRzLmZpbmQoXG4gICAgICBldmVudCA9PiBldmVudC50YXJnZXQgPT09IHRoaXMueW1vZGVsLmdldCgnc291cmNlJylcbiAgICApO1xuICAgIGlmIChzb3VyY2VFdmVudCkge1xuICAgICAgY2hhbmdlcy5zb3VyY2VDaGFuZ2UgPSBzb3VyY2VFdmVudC5jaGFuZ2VzLmRlbHRhIGFzIGFueTtcbiAgICB9XG5cbiAgICBjb25zdCBvdXRwdXRFdmVudCA9IGV2ZW50cy5maW5kKFxuICAgICAgZXZlbnQgPT4gZXZlbnQudGFyZ2V0ID09PSB0aGlzLnltb2RlbC5nZXQoJ291dHB1dHMnKVxuICAgICk7XG4gICAgaWYgKG91dHB1dEV2ZW50KSB7XG4gICAgICBjaGFuZ2VzLm91dHB1dHNDaGFuZ2UgPSBvdXRwdXRFdmVudC5jaGFuZ2VzLmRlbHRhIGFzIGFueTtcbiAgICB9XG5cbiAgICBjb25zdCBtb2RlbEV2ZW50ID0gZXZlbnRzLmZpbmQoZXZlbnQgPT4gZXZlbnQudGFyZ2V0ID09PSB0aGlzLnltb2RlbCkgYXNcbiAgICAgIHwgdW5kZWZpbmVkXG4gICAgICB8IFkuWU1hcEV2ZW50PGFueT47XG4gICAgaWYgKG1vZGVsRXZlbnQgJiYgbW9kZWxFdmVudC5rZXlzQ2hhbmdlZC5oYXMoJ21ldGFkYXRhJykpIHtcbiAgICAgIGNvbnN0IGNoYW5nZSA9IG1vZGVsRXZlbnQuY2hhbmdlcy5rZXlzLmdldCgnbWV0YWRhdGEnKTtcbiAgICAgIGNoYW5nZXMubWV0YWRhdGFDaGFuZ2UgPSB7XG4gICAgICAgIG9sZFZhbHVlOiBjaGFuZ2U/Lm9sZFZhbHVlID8gY2hhbmdlIS5vbGRWYWx1ZSA6IHVuZGVmaW5lZCxcbiAgICAgICAgbmV3VmFsdWU6IHRoaXMuZ2V0TWV0YWRhdGEoKVxuICAgICAgfTtcbiAgICB9XG5cbiAgICBpZiAobW9kZWxFdmVudCAmJiBtb2RlbEV2ZW50LmtleXNDaGFuZ2VkLmhhcygnZXhlY3V0aW9uX2NvdW50JykpIHtcbiAgICAgIGNvbnN0IGNoYW5nZSA9IG1vZGVsRXZlbnQuY2hhbmdlcy5rZXlzLmdldCgnZXhlY3V0aW9uX2NvdW50Jyk7XG4gICAgICBjaGFuZ2VzLmV4ZWN1dGlvbkNvdW50Q2hhbmdlID0ge1xuICAgICAgICBvbGRWYWx1ZTogY2hhbmdlIS5vbGRWYWx1ZSxcbiAgICAgICAgbmV3VmFsdWU6IHRoaXMueW1vZGVsLmdldCgnZXhlY3V0aW9uX2NvdW50JylcbiAgICAgIH07XG4gICAgfVxuXG4gICAgLy8gVGhlIG1vZGVsIGFsbG93cyB1cyB0byByZXBsYWNlIHRoZSBjb21wbGV0ZSBzb3VyY2Ugd2l0aCBhIG5ldyBzdHJpbmcuIFdlIGV4cHJlc3MgdGhpcyBpbiB0aGUgRGVsdGEgZm9ybWF0XG4gICAgLy8gYXMgYSByZXBsYWNlIG9mIHRoZSBjb21wbGV0ZSBzdHJpbmcuXG4gICAgY29uc3QgeXNvdXJjZSA9IHRoaXMueW1vZGVsLmdldCgnc291cmNlJyk7XG4gICAgaWYgKG1vZGVsRXZlbnQgJiYgbW9kZWxFdmVudC5rZXlzQ2hhbmdlZC5oYXMoJ3NvdXJjZScpKSB7XG4gICAgICBjaGFuZ2VzLnNvdXJjZUNoYW5nZSA9IFtcbiAgICAgICAgeyBkZWxldGU6IHRoaXMuX3ByZXZTb3VyY2VMZW5ndGggfSxcbiAgICAgICAgeyBpbnNlcnQ6IHlzb3VyY2UudG9TdHJpbmcoKSB9XG4gICAgICBdO1xuICAgIH1cbiAgICB0aGlzLl9wcmV2U291cmNlTGVuZ3RoID0geXNvdXJjZS5sZW5ndGg7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KGNoYW5nZXMpO1xuICB9O1xuXG4gIC8qKlxuICAgKiBUaGUgY2hhbmdlZCBzaWduYWwuXG4gICAqL1xuICBnZXQgY2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIG1vZGVscy5DZWxsQ2hhbmdlPE1ldGFkYXRhPj4ge1xuICAgIHJldHVybiB0aGlzLl9jaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcy5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgdGhpcy55bW9kZWwudW5vYnNlcnZlRGVlcCh0aGlzLl9tb2RlbE9ic2VydmVyKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXRzIHRoZSBjZWxsIGF0dGFjaG1lbnRzLlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgY2VsbCBhdHRhY2htZW50cy5cbiAgICovXG4gIHB1YmxpYyBnZXRBdHRhY2htZW50cygpOiBuYmZvcm1hdC5JQXR0YWNobWVudHMgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiB0aGlzLnltb2RlbC5nZXQoJ2F0dGFjaG1lbnRzJyk7XG4gIH1cblxuICAvKipcbiAgICogU2V0cyB0aGUgY2VsbCBhdHRhY2htZW50c1xuICAgKlxuICAgKiBAcGFyYW0gYXR0YWNobWVudHM6IFRoZSBjZWxsIGF0dGFjaG1lbnRzLlxuICAgKi9cbiAgcHVibGljIHNldEF0dGFjaG1lbnRzKGF0dGFjaG1lbnRzOiBuYmZvcm1hdC5JQXR0YWNobWVudHMgfCB1bmRlZmluZWQpOiB2b2lkIHtcbiAgICB0aGlzLnRyYW5zYWN0KCgpID0+IHtcbiAgICAgIGlmIChhdHRhY2htZW50cyA9PSBudWxsKSB7XG4gICAgICAgIHRoaXMueW1vZGVsLmRlbGV0ZSgnYXR0YWNobWVudHMnKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMueW1vZGVsLnNldCgnYXR0YWNobWVudHMnLCBhdHRhY2htZW50cyk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGNlbGwgaWQuXG4gICAqXG4gICAqIEByZXR1cm5zIENlbGwgaWRcbiAgICovXG4gIHB1YmxpYyBnZXRJZCgpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLnltb2RlbC5nZXQoJ2lkJyk7XG4gIH1cblxuICAvKipcbiAgICogR2V0cyBjZWxsJ3Mgc291cmNlLlxuICAgKlxuICAgKiBAcmV0dXJucyBDZWxsJ3Mgc291cmNlLlxuICAgKi9cbiAgcHVibGljIGdldFNvdXJjZSgpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLnltb2RlbC5nZXQoJ3NvdXJjZScpLnRvU3RyaW5nKCk7XG4gIH1cblxuICAvKipcbiAgICogU2V0cyBjZWxsJ3Mgc291cmNlLlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWU6IE5ldyBzb3VyY2UuXG4gICAqL1xuICBwdWJsaWMgc2V0U291cmNlKHZhbHVlOiBzdHJpbmcpOiB2b2lkIHtcbiAgICBjb25zdCB5dGV4dCA9IHRoaXMueW1vZGVsLmdldCgnc291cmNlJyk7XG4gICAgdGhpcy50cmFuc2FjdCgoKSA9PiB7XG4gICAgICB5dGV4dC5kZWxldGUoMCwgeXRleHQubGVuZ3RoKTtcbiAgICAgIHl0ZXh0Lmluc2VydCgwLCB2YWx1ZSk7XG4gICAgfSk7XG4gICAgLy8gQHRvZG8gRG8gd2UgbmVlZCBwcm9wZXIgcmVwbGFjZSBzZW1hbnRpYz8gVGhpcyBsZWFkcyB0byBpc3N1ZXMgaW4gZWRpdG9yIGJpbmRpbmdzIGJlY2F1c2UgdGhleSBkb24ndCBzd2l0Y2ggc291cmNlLlxuICAgIC8vIHRoaXMueW1vZGVsLnNldCgnc291cmNlJywgbmV3IFkuVGV4dCh2YWx1ZSkpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlcGxhY2UgY29udGVudCBmcm9tIGBzdGFydCcgdG8gYGVuZGAgd2l0aCBgdmFsdWVgLlxuICAgKlxuICAgKiBAcGFyYW0gc3RhcnQ6IFRoZSBzdGFydCBpbmRleCBvZiB0aGUgcmFuZ2UgdG8gcmVwbGFjZSAoaW5jbHVzaXZlKS5cbiAgICpcbiAgICogQHBhcmFtIGVuZDogVGhlIGVuZCBpbmRleCBvZiB0aGUgcmFuZ2UgdG8gcmVwbGFjZSAoZXhjbHVzaXZlKS5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlOiBOZXcgc291cmNlIChvcHRpb25hbCkuXG4gICAqL1xuICBwdWJsaWMgdXBkYXRlU291cmNlKHN0YXJ0OiBudW1iZXIsIGVuZDogbnVtYmVyLCB2YWx1ZSA9ICcnKTogdm9pZCB7XG4gICAgdGhpcy50cmFuc2FjdCgoKSA9PiB7XG4gICAgICBjb25zdCB5c291cmNlID0gdGhpcy55c291cmNlO1xuICAgICAgLy8gaW5zZXJ0IGFuZCB0aGVuIGRlbGV0ZS5cbiAgICAgIC8vIFRoaXMgZW5zdXJlcyB0aGF0IHRoZSBjdXJzb3IgcG9zaXRpb24gaXMgYWRqdXN0ZWQgYWZ0ZXIgdGhlIHJlcGxhY2VkIGNvbnRlbnQuXG4gICAgICB5c291cmNlLmluc2VydChzdGFydCwgdmFsdWUpO1xuICAgICAgeXNvdXJjZS5kZWxldGUoc3RhcnQgKyB2YWx1ZS5sZW5ndGgsIGVuZCAtIHN0YXJ0KTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgdHlwZSBvZiB0aGUgY2VsbC5cbiAgICovXG4gIGdldCBjZWxsX3R5cGUoKTogYW55IHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoJ0EgWUJhc2VDZWxsIG11c3Qgbm90IGJlIGNvbnN0cnVjdGVkJyk7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJucyB0aGUgbWV0YWRhdGEgYXNzb2NpYXRlZCB3aXRoIHRoZSBub3RlYm9vay5cbiAgICpcbiAgICogQHJldHVybnMgTm90ZWJvb2sncyBtZXRhZGF0YS5cbiAgICovXG4gIGdldE1ldGFkYXRhKCk6IFBhcnRpYWw8TWV0YWRhdGE+IHtcbiAgICByZXR1cm4gZGVlcENvcHkodGhpcy55bW9kZWwuZ2V0KCdtZXRhZGF0YScpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXRzIHRoZSBtZXRhZGF0YSBhc3NvY2lhdGVkIHdpdGggdGhlIG5vdGVib29rLlxuICAgKlxuICAgKiBAcGFyYW0gbWV0YWRhdGE6IE5vdGVib29rJ3MgbWV0YWRhdGEuXG4gICAqL1xuICBzZXRNZXRhZGF0YSh2YWx1ZTogUGFydGlhbDxNZXRhZGF0YT4pOiB2b2lkIHtcbiAgICB0aGlzLnRyYW5zYWN0KCgpID0+IHtcbiAgICAgIHRoaXMueW1vZGVsLnNldCgnbWV0YWRhdGEnLCBkZWVwQ29weSh2YWx1ZSkpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFNlcmlhbGl6ZSB0aGUgbW9kZWwgdG8gSlNPTi5cbiAgICovXG4gIHRvSlNPTigpOiBuYmZvcm1hdC5JQmFzZUNlbGwge1xuICAgIHJldHVybiB7XG4gICAgICBpZDogdGhpcy5nZXRJZCgpLFxuICAgICAgY2VsbF90eXBlOiB0aGlzLmNlbGxfdHlwZSxcbiAgICAgIHNvdXJjZTogdGhpcy5nZXRTb3VyY2UoKSxcbiAgICAgIG1ldGFkYXRhOiB0aGlzLmdldE1ldGFkYXRhKClcbiAgICB9O1xuICB9XG5cbiAgcHVibGljIGlzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHVibGljIHltb2RlbDogWS5NYXA8YW55PjtcbiAgcHJpdmF0ZSBfdW5kb01hbmFnZXI6IFkuVW5kb01hbmFnZXIgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfY2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgbW9kZWxzLkNlbGxDaGFuZ2U8TWV0YWRhdGE+Pih0aGlzKTtcbiAgcHJpdmF0ZSBfcHJldlNvdXJjZUxlbmd0aDogbnVtYmVyO1xuICBwcml2YXRlIF9hd2FyZW5lc3M6IEF3YXJlbmVzcyB8IG51bGw7XG59XG5cbmV4cG9ydCBjbGFzcyBZQ29kZUNlbGxcbiAgZXh0ZW5kcyBZQmFzZUNlbGw8bW9kZWxzLklTaGFyZWRCYXNlQ2VsbE1ldGFkYXRhPlxuICBpbXBsZW1lbnRzIG1vZGVscy5JU2hhcmVkQ29kZUNlbGwge1xuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhlIGNlbGwuXG4gICAqL1xuICBnZXQgY2VsbF90eXBlKCk6ICdjb2RlJyB7XG4gICAgcmV0dXJuICdjb2RlJztcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY29kZSBjZWxsJ3MgcHJvbXB0IG51bWJlci4gV2lsbCBiZSBudWxsIGlmIHRoZSBjZWxsIGhhcyBub3QgYmVlbiBydW4uXG4gICAqL1xuICBnZXQgZXhlY3V0aW9uX2NvdW50KCk6IG51bWJlciB8IG51bGwge1xuICAgIHJldHVybiB0aGlzLnltb2RlbC5nZXQoJ2V4ZWN1dGlvbl9jb3VudCcpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb2RlIGNlbGwncyBwcm9tcHQgbnVtYmVyLiBXaWxsIGJlIG51bGwgaWYgdGhlIGNlbGwgaGFzIG5vdCBiZWVuIHJ1bi5cbiAgICovXG4gIHNldCBleGVjdXRpb25fY291bnQoY291bnQ6IG51bWJlciB8IG51bGwpIHtcbiAgICB0aGlzLnRyYW5zYWN0KCgpID0+IHtcbiAgICAgIHRoaXMueW1vZGVsLnNldCgnZXhlY3V0aW9uX2NvdW50JywgY291bnQpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEV4ZWN1dGlvbiwgZGlzcGxheSwgb3Igc3RyZWFtIG91dHB1dHMuXG4gICAqL1xuICBnZXRPdXRwdXRzKCk6IEFycmF5PG5iZm9ybWF0LklPdXRwdXQ+IHtcbiAgICByZXR1cm4gZGVlcENvcHkodGhpcy55bW9kZWwuZ2V0KCdvdXRwdXRzJykudG9BcnJheSgpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXBsYWNlIGFsbCBvdXRwdXRzLlxuICAgKi9cbiAgc2V0T3V0cHV0cyhvdXRwdXRzOiBBcnJheTxuYmZvcm1hdC5JT3V0cHV0Pik6IHZvaWQge1xuICAgIGNvbnN0IHlvdXRwdXRzID0gdGhpcy55bW9kZWwuZ2V0KCdvdXRwdXRzJykgYXMgWS5BcnJheTxuYmZvcm1hdC5JT3V0cHV0PjtcbiAgICB0aGlzLnRyYW5zYWN0KCgpID0+IHtcbiAgICAgIHlvdXRwdXRzLmRlbGV0ZSgwLCB5b3V0cHV0cy5sZW5ndGgpO1xuICAgICAgeW91dHB1dHMuaW5zZXJ0KDAsIG91dHB1dHMpO1xuICAgIH0sIGZhbHNlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXBsYWNlIGNvbnRlbnQgZnJvbSBgc3RhcnQnIHRvIGBlbmRgIHdpdGggYG91dHB1dHNgLlxuICAgKlxuICAgKiBAcGFyYW0gc3RhcnQ6IFRoZSBzdGFydCBpbmRleCBvZiB0aGUgcmFuZ2UgdG8gcmVwbGFjZSAoaW5jbHVzaXZlKS5cbiAgICpcbiAgICogQHBhcmFtIGVuZDogVGhlIGVuZCBpbmRleCBvZiB0aGUgcmFuZ2UgdG8gcmVwbGFjZSAoZXhjbHVzaXZlKS5cbiAgICpcbiAgICogQHBhcmFtIG91dHB1dHM6IE5ldyBvdXRwdXRzIChvcHRpb25hbCkuXG4gICAqL1xuICB1cGRhdGVPdXRwdXRzKFxuICAgIHN0YXJ0OiBudW1iZXIsXG4gICAgZW5kOiBudW1iZXIsXG4gICAgb3V0cHV0czogQXJyYXk8bmJmb3JtYXQuSU91dHB1dD4gPSBbXVxuICApOiB2b2lkIHtcbiAgICBjb25zdCB5b3V0cHV0cyA9IHRoaXMueW1vZGVsLmdldCgnb3V0cHV0cycpIGFzIFkuQXJyYXk8bmJmb3JtYXQuSU91dHB1dD47XG4gICAgY29uc3QgZmluID0gZW5kIDwgeW91dHB1dHMubGVuZ3RoID8gZW5kIC0gc3RhcnQgOiB5b3V0cHV0cy5sZW5ndGggLSBzdGFydDtcbiAgICB0aGlzLnRyYW5zYWN0KCgpID0+IHtcbiAgICAgIHlvdXRwdXRzLmRlbGV0ZShzdGFydCwgZmluKTtcbiAgICAgIHlvdXRwdXRzLmluc2VydChzdGFydCwgb3V0cHV0cyk7XG4gICAgfSwgZmFsc2UpO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBZQ29kZUNlbGwgdGhhdCBjYW4gYmUgaW5zZXJ0ZWQgaW50byBhIFlOb3RlYm9va1xuICAgKi9cbiAgcHVibGljIHN0YXRpYyBjcmVhdGUoaWQ/OiBzdHJpbmcpOiBZQ29kZUNlbGwge1xuICAgIGNvbnN0IGNlbGwgPSBzdXBlci5jcmVhdGUoaWQpO1xuICAgIGNlbGwueW1vZGVsLnNldCgnZXhlY3V0aW9uX2NvdW50JywgMCk7IC8vIGZvciBzb21lIGRlZmF1bHQgdmFsdWVcbiAgICBjZWxsLnltb2RlbC5zZXQoJ291dHB1dHMnLCBuZXcgWS5BcnJheTxuYmZvcm1hdC5JT3V0cHV0PigpKTtcbiAgICByZXR1cm4gY2VsbCBhcyBhbnk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IFlDb2RlQ2VsbCB0aGF0IHdvcmtzIHN0YW5kYWxvbmUuIEl0IGNhbm5vdCBiZVxuICAgKiBpbnNlcnRlZCBpbnRvIGEgWU5vdGVib29rIGJlY2F1c2UgdGhlIFlqcyBtb2RlbCBpcyBhbHJlYWR5XG4gICAqIGF0dGFjaGVkIHRvIGFuIGFub255bW91cyBZLkRvYyBpbnN0YW5jZS5cbiAgICovXG4gIHB1YmxpYyBzdGF0aWMgY3JlYXRlU3RhbmRhbG9uZShpZD86IHN0cmluZyk6IFlDb2RlQ2VsbCB7XG4gICAgY29uc3QgY2VsbCA9IHN1cGVyLmNyZWF0ZVN0YW5kYWxvbmUoaWQpO1xuICAgIGNlbGwueW1vZGVsLnNldCgnZXhlY3V0aW9uX2NvdW50JywgbnVsbCk7IC8vIGZvciBzb21lIGRlZmF1bHQgdmFsdWVcbiAgICBjZWxsLnltb2RlbC5zZXQoJ291dHB1dHMnLCBuZXcgWS5BcnJheTxuYmZvcm1hdC5JT3V0cHV0PigpKTtcbiAgICByZXR1cm4gY2VsbCBhcyBhbnk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IFlDb2RlQ2VsbCB0aGF0IGNhbiBiZSBpbnNlcnRlZCBpbnRvIGEgWU5vdGVib29rXG4gICAqXG4gICAqIEB0b2RvIGNsb25lIHNob3VsZCBvbmx5IGJlIGF2YWlsYWJsZSBpbiB0aGUgc3BlY2lmaWMgaW1wbGVtZW50YXRpb25zIGkuZS4gSVNoYXJlZENvZGVDZWxsXG4gICAqL1xuICBwdWJsaWMgY2xvbmUoKTogWUNvZGVDZWxsIHtcbiAgICBjb25zdCBjZWxsID0gc3VwZXIuY2xvbmUoKTtcbiAgICBjb25zdCB5b3V0cHV0cyA9IG5ldyBZLkFycmF5PG5iZm9ybWF0LklPdXRwdXQ+KCk7XG4gICAgeW91dHB1dHMuaW5zZXJ0KDAsIHRoaXMuZ2V0T3V0cHV0cygpKTtcbiAgICBjZWxsLnltb2RlbC5zZXQoJ2V4ZWN1dGlvbl9jb3VudCcsIHRoaXMuZXhlY3V0aW9uX2NvdW50KTsgLy8gZm9yIHNvbWUgZGVmYXVsdCB2YWx1ZVxuICAgIGNlbGwueW1vZGVsLnNldCgnb3V0cHV0cycsIHlvdXRwdXRzKTtcbiAgICByZXR1cm4gY2VsbCBhcyBhbnk7XG4gIH1cblxuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IG5iZm9ybWF0LklDb2RlQ2VsbCB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGlkOiB0aGlzLmdldElkKCksXG4gICAgICBjZWxsX3R5cGU6ICdjb2RlJyxcbiAgICAgIHNvdXJjZTogdGhpcy5nZXRTb3VyY2UoKSxcbiAgICAgIG1ldGFkYXRhOiB0aGlzLmdldE1ldGFkYXRhKCksXG4gICAgICBvdXRwdXRzOiB0aGlzLmdldE91dHB1dHMoKSxcbiAgICAgIGV4ZWN1dGlvbl9jb3VudDogdGhpcy5leGVjdXRpb25fY291bnRcbiAgICB9O1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBZUmF3Q2VsbFxuICBleHRlbmRzIFlCYXNlQ2VsbDxtb2RlbHMuSVNoYXJlZEJhc2VDZWxsTWV0YWRhdGE+XG4gIGltcGxlbWVudHMgbW9kZWxzLklTaGFyZWRSYXdDZWxsIHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBZUmF3Q2VsbCB0aGF0IGNhbiBiZSBpbnNlcnRlZCBpbnRvIGEgWU5vdGVib29rXG4gICAqL1xuICBwdWJsaWMgc3RhdGljIGNyZWF0ZShpZD86IHN0cmluZyk6IFlSYXdDZWxsIHtcbiAgICByZXR1cm4gc3VwZXIuY3JlYXRlKGlkKSBhcyBhbnk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IFlSYXdDZWxsIHRoYXQgd29ya3Mgc3RhbmRhbG9uZS4gSXQgY2Fubm90IGJlXG4gICAqIGluc2VydGVkIGludG8gYSBZTm90ZWJvb2sgYmVjYXVzZSB0aGUgWWpzIG1vZGVsIGlzIGFscmVhZHlcbiAgICogYXR0YWNoZWQgdG8gYW4gYW5vbnltb3VzIFkuRG9jIGluc3RhbmNlLlxuICAgKi9cbiAgcHVibGljIHN0YXRpYyBjcmVhdGVTdGFuZGFsb25lKGlkPzogc3RyaW5nKTogWVJhd0NlbGwge1xuICAgIHJldHVybiBzdXBlci5jcmVhdGVTdGFuZGFsb25lKGlkKSBhcyBhbnk7XG4gIH1cblxuICAvKipcbiAgICogU3RyaW5nIGlkZW50aWZ5aW5nIHRoZSB0eXBlIG9mIGNlbGwuXG4gICAqL1xuICBnZXQgY2VsbF90eXBlKCk6ICdyYXcnIHtcbiAgICByZXR1cm4gJ3Jhdyc7XG4gIH1cblxuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IG5iZm9ybWF0LklSYXdDZWxsIHtcbiAgICByZXR1cm4ge1xuICAgICAgaWQ6IHRoaXMuZ2V0SWQoKSxcbiAgICAgIGNlbGxfdHlwZTogJ3JhdycsXG4gICAgICBzb3VyY2U6IHRoaXMuZ2V0U291cmNlKCksXG4gICAgICBtZXRhZGF0YTogdGhpcy5nZXRNZXRhZGF0YSgpLFxuICAgICAgYXR0YWNobWVudHM6IHRoaXMuZ2V0QXR0YWNobWVudHMoKVxuICAgIH07XG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIFlNYXJrZG93bkNlbGxcbiAgZXh0ZW5kcyBZQmFzZUNlbGw8bW9kZWxzLklTaGFyZWRCYXNlQ2VsbE1ldGFkYXRhPlxuICBpbXBsZW1lbnRzIG1vZGVscy5JU2hhcmVkTWFya2Rvd25DZWxsIHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBZTWFya2Rvd25DZWxsIHRoYXQgY2FuIGJlIGluc2VydGVkIGludG8gYSBZTm90ZWJvb2tcbiAgICovXG4gIHB1YmxpYyBzdGF0aWMgY3JlYXRlKGlkPzogc3RyaW5nKTogWU1hcmtkb3duQ2VsbCB7XG4gICAgcmV0dXJuIHN1cGVyLmNyZWF0ZShpZCkgYXMgYW55O1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBZTWFya2Rvd25DZWxsIHRoYXQgd29ya3Mgc3RhbmRhbG9uZS4gSXQgY2Fubm90IGJlXG4gICAqIGluc2VydGVkIGludG8gYSBZTm90ZWJvb2sgYmVjYXVzZSB0aGUgWWpzIG1vZGVsIGlzIGFscmVhZHlcbiAgICogYXR0YWNoZWQgdG8gYW4gYW5vbnltb3VzIFkuRG9jIGluc3RhbmNlLlxuICAgKi9cbiAgcHVibGljIHN0YXRpYyBjcmVhdGVTdGFuZGFsb25lKGlkPzogc3RyaW5nKTogWU1hcmtkb3duQ2VsbCB7XG4gICAgcmV0dXJuIHN1cGVyLmNyZWF0ZVN0YW5kYWxvbmUoaWQpIGFzIGFueTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTdHJpbmcgaWRlbnRpZnlpbmcgdGhlIHR5cGUgb2YgY2VsbC5cbiAgICovXG4gIGdldCBjZWxsX3R5cGUoKTogJ21hcmtkb3duJyB7XG4gICAgcmV0dXJuICdtYXJrZG93bic7XG4gIH1cblxuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IG5iZm9ybWF0LklNYXJrZG93bkNlbGwge1xuICAgIHJldHVybiB7XG4gICAgICBpZDogdGhpcy5nZXRJZCgpLFxuICAgICAgY2VsbF90eXBlOiAnbWFya2Rvd24nLFxuICAgICAgc291cmNlOiB0aGlzLmdldFNvdXJjZSgpLFxuICAgICAgbWV0YWRhdGE6IHRoaXMuZ2V0TWV0YWRhdGEoKSxcbiAgICAgIGF0dGFjaG1lbnRzOiB0aGlzLmdldEF0dGFjaG1lbnRzKClcbiAgICB9O1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IFlOb3RlYm9vaztcbiIsIi8qKlxuICogQG1vZHVsZSBhd2FyZW5lc3MtcHJvdG9jb2xcbiAqL1xuXG5pbXBvcnQgKiBhcyBlbmNvZGluZyBmcm9tICdsaWIwL2VuY29kaW5nJ1xuaW1wb3J0ICogYXMgZGVjb2RpbmcgZnJvbSAnbGliMC9kZWNvZGluZydcbmltcG9ydCAqIGFzIHRpbWUgZnJvbSAnbGliMC90aW1lJ1xuaW1wb3J0ICogYXMgbWF0aCBmcm9tICdsaWIwL21hdGgnXG5pbXBvcnQgeyBPYnNlcnZhYmxlIH0gZnJvbSAnbGliMC9vYnNlcnZhYmxlJ1xuaW1wb3J0ICogYXMgZiBmcm9tICdsaWIwL2Z1bmN0aW9uJ1xuaW1wb3J0ICogYXMgWSBmcm9tICd5anMnIC8vIGVzbGludC1kaXNhYmxlLWxpbmVcblxuZXhwb3J0IGNvbnN0IG91dGRhdGVkVGltZW91dCA9IDMwMDAwXG5cbi8qKlxuICogQHR5cGVkZWYge09iamVjdH0gTWV0YUNsaWVudFN0YXRlXG4gKiBAcHJvcGVydHkge251bWJlcn0gTWV0YUNsaWVudFN0YXRlLmNsb2NrXG4gKiBAcHJvcGVydHkge251bWJlcn0gTWV0YUNsaWVudFN0YXRlLmxhc3RVcGRhdGVkIHVuaXggdGltZXN0YW1wXG4gKi9cblxuLyoqXG4gKiBUaGUgQXdhcmVuZXNzIGNsYXNzIGltcGxlbWVudHMgYSBzaW1wbGUgc2hhcmVkIHN0YXRlIHByb3RvY29sIHRoYXQgY2FuIGJlIHVzZWQgZm9yIG5vbi1wZXJzaXN0ZW50IGRhdGEgbGlrZSBhd2FyZW5lc3MgaW5mb3JtYXRpb25cbiAqIChjdXJzb3IsIHVzZXJuYW1lLCBzdGF0dXMsIC4uKS4gRWFjaCBjbGllbnQgY2FuIHVwZGF0ZSBpdHMgb3duIGxvY2FsIHN0YXRlIGFuZCBsaXN0ZW4gdG8gc3RhdGUgY2hhbmdlcyBvZlxuICogcmVtb3RlIGNsaWVudHMuIEV2ZXJ5IGNsaWVudCBtYXkgc2V0IGEgc3RhdGUgb2YgYSByZW1vdGUgcGVlciB0byBgbnVsbGAgdG8gbWFyayB0aGUgY2xpZW50IGFzIG9mZmxpbmUuXG4gKlxuICogRWFjaCBjbGllbnQgaXMgaWRlbnRpZmllZCBieSBhIHVuaXF1ZSBjbGllbnQgaWQgKHNvbWV0aGluZyB3ZSBib3Jyb3cgZnJvbSBgZG9jLmNsaWVudElEYCkuIEEgY2xpZW50IGNhbiBvdmVycmlkZVxuICogaXRzIG93biBzdGF0ZSBieSBwcm9wYWdhdGluZyBhIG1lc3NhZ2Ugd2l0aCBhbiBpbmNyZWFzaW5nIHRpbWVzdGFtcCAoYGNsb2NrYCkuIElmIHN1Y2ggYSBtZXNzYWdlIGlzIHJlY2VpdmVkLCBpdCBpc1xuICogYXBwbGllZCBpZiB0aGUga25vd24gc3RhdGUgb2YgdGhhdCBjbGllbnQgaXMgb2xkZXIgdGhhbiB0aGUgbmV3IHN0YXRlIChgY2xvY2sgPCBuZXdDbG9ja2ApLiBJZiBhIGNsaWVudCB0aGlua3MgdGhhdFxuICogYSByZW1vdGUgY2xpZW50IGlzIG9mZmxpbmUsIGl0IG1heSBwcm9wYWdhdGUgYSBtZXNzYWdlIHdpdGhcbiAqIGB7IGNsb2NrOiBjdXJyZW50Q2xpZW50Q2xvY2ssIHN0YXRlOiBudWxsLCBjbGllbnQ6IHJlbW90ZUNsaWVudCB9YC4gSWYgc3VjaCBhXG4gKiBtZXNzYWdlIGlzIHJlY2VpdmVkLCBhbmQgdGhlIGtub3duIGNsb2NrIG9mIHRoYXQgY2xpZW50IGVxdWFscyB0aGUgcmVjZWl2ZWQgY2xvY2ssIGl0IHdpbGwgb3ZlcnJpZGUgdGhlIHN0YXRlIHdpdGggYG51bGxgLlxuICpcbiAqIEJlZm9yZSBhIGNsaWVudCBkaXNjb25uZWN0cywgaXQgc2hvdWxkIHByb3BhZ2F0ZSBhIGBudWxsYCBzdGF0ZSB3aXRoIGFuIHVwZGF0ZWQgY2xvY2suXG4gKlxuICogQXdhcmVuZXNzIHN0YXRlcyBtdXN0IGJlIHVwZGF0ZWQgZXZlcnkgMzAgc2Vjb25kcy4gT3RoZXJ3aXNlIHRoZSBBd2FyZW5lc3MgaW5zdGFuY2Ugd2lsbCBkZWxldGUgdGhlIGNsaWVudCBzdGF0ZS5cbiAqXG4gKiBAZXh0ZW5kcyB7T2JzZXJ2YWJsZTxzdHJpbmc+fVxuICovXG5leHBvcnQgY2xhc3MgQXdhcmVuZXNzIGV4dGVuZHMgT2JzZXJ2YWJsZSB7XG4gIC8qKlxuICAgKiBAcGFyYW0ge1kuRG9jfSBkb2NcbiAgICovXG4gIGNvbnN0cnVjdG9yIChkb2MpIHtcbiAgICBzdXBlcigpXG4gICAgdGhpcy5kb2MgPSBkb2NcbiAgICAvKipcbiAgICAgKiBAdHlwZSB7bnVtYmVyfVxuICAgICAqL1xuICAgIHRoaXMuY2xpZW50SUQgPSBkb2MuY2xpZW50SURcbiAgICAvKipcbiAgICAgKiBNYXBzIGZyb20gY2xpZW50IGlkIHRvIGNsaWVudCBzdGF0ZVxuICAgICAqIEB0eXBlIHtNYXA8bnVtYmVyLCBPYmplY3Q8c3RyaW5nLCBhbnk+Pn1cbiAgICAgKi9cbiAgICB0aGlzLnN0YXRlcyA9IG5ldyBNYXAoKVxuICAgIC8qKlxuICAgICAqIEB0eXBlIHtNYXA8bnVtYmVyLCBNZXRhQ2xpZW50U3RhdGU+fVxuICAgICAqL1xuICAgIHRoaXMubWV0YSA9IG5ldyBNYXAoKVxuICAgIHRoaXMuX2NoZWNrSW50ZXJ2YWwgPSAvKiogQHR5cGUge2FueX0gKi8gKHNldEludGVydmFsKCgpID0+IHtcbiAgICAgIGNvbnN0IG5vdyA9IHRpbWUuZ2V0VW5peFRpbWUoKVxuICAgICAgaWYgKHRoaXMuZ2V0TG9jYWxTdGF0ZSgpICE9PSBudWxsICYmIChvdXRkYXRlZFRpbWVvdXQgLyAyIDw9IG5vdyAtIC8qKiBAdHlwZSB7e2xhc3RVcGRhdGVkOm51bWJlcn19ICovICh0aGlzLm1ldGEuZ2V0KHRoaXMuY2xpZW50SUQpKS5sYXN0VXBkYXRlZCkpIHtcbiAgICAgICAgLy8gcmVuZXcgbG9jYWwgY2xvY2tcbiAgICAgICAgdGhpcy5zZXRMb2NhbFN0YXRlKHRoaXMuZ2V0TG9jYWxTdGF0ZSgpKVxuICAgICAgfVxuICAgICAgLyoqXG4gICAgICAgKiBAdHlwZSB7QXJyYXk8bnVtYmVyPn1cbiAgICAgICAqL1xuICAgICAgY29uc3QgcmVtb3ZlID0gW11cbiAgICAgIHRoaXMubWV0YS5mb3JFYWNoKChtZXRhLCBjbGllbnRpZCkgPT4ge1xuICAgICAgICBpZiAoY2xpZW50aWQgIT09IHRoaXMuY2xpZW50SUQgJiYgb3V0ZGF0ZWRUaW1lb3V0IDw9IG5vdyAtIG1ldGEubGFzdFVwZGF0ZWQgJiYgdGhpcy5zdGF0ZXMuaGFzKGNsaWVudGlkKSkge1xuICAgICAgICAgIHJlbW92ZS5wdXNoKGNsaWVudGlkKVxuICAgICAgICB9XG4gICAgICB9KVxuICAgICAgaWYgKHJlbW92ZS5sZW5ndGggPiAwKSB7XG4gICAgICAgIHJlbW92ZUF3YXJlbmVzc1N0YXRlcyh0aGlzLCByZW1vdmUsICd0aW1lb3V0JylcbiAgICAgIH1cbiAgICB9LCBtYXRoLmZsb29yKG91dGRhdGVkVGltZW91dCAvIDEwKSkpXG4gICAgZG9jLm9uKCdkZXN0cm95JywgKCkgPT4ge1xuICAgICAgdGhpcy5kZXN0cm95KClcbiAgICB9KVxuICAgIHRoaXMuc2V0TG9jYWxTdGF0ZSh7fSlcbiAgfVxuXG4gIGRlc3Ryb3kgKCkge1xuICAgIHRoaXMuZW1pdCgnZGVzdHJveScsIFt0aGlzXSlcbiAgICB0aGlzLnNldExvY2FsU3RhdGUobnVsbClcbiAgICBzdXBlci5kZXN0cm95KClcbiAgICBjbGVhckludGVydmFsKHRoaXMuX2NoZWNrSW50ZXJ2YWwpXG4gIH1cblxuICAvKipcbiAgICogQHJldHVybiB7T2JqZWN0PHN0cmluZyxhbnk+fG51bGx9XG4gICAqL1xuICBnZXRMb2NhbFN0YXRlICgpIHtcbiAgICByZXR1cm4gdGhpcy5zdGF0ZXMuZ2V0KHRoaXMuY2xpZW50SUQpIHx8IG51bGxcbiAgfVxuXG4gIC8qKlxuICAgKiBAcGFyYW0ge09iamVjdDxzdHJpbmcsYW55PnxudWxsfSBzdGF0ZVxuICAgKi9cbiAgc2V0TG9jYWxTdGF0ZSAoc3RhdGUpIHtcbiAgICBjb25zdCBjbGllbnRJRCA9IHRoaXMuY2xpZW50SURcbiAgICBjb25zdCBjdXJyTG9jYWxNZXRhID0gdGhpcy5tZXRhLmdldChjbGllbnRJRClcbiAgICBjb25zdCBjbG9jayA9IGN1cnJMb2NhbE1ldGEgPT09IHVuZGVmaW5lZCA/IDAgOiBjdXJyTG9jYWxNZXRhLmNsb2NrICsgMVxuICAgIGNvbnN0IHByZXZTdGF0ZSA9IHRoaXMuc3RhdGVzLmdldChjbGllbnRJRClcbiAgICBpZiAoc3RhdGUgPT09IG51bGwpIHtcbiAgICAgIHRoaXMuc3RhdGVzLmRlbGV0ZShjbGllbnRJRClcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5zdGF0ZXMuc2V0KGNsaWVudElELCBzdGF0ZSlcbiAgICB9XG4gICAgdGhpcy5tZXRhLnNldChjbGllbnRJRCwge1xuICAgICAgY2xvY2ssXG4gICAgICBsYXN0VXBkYXRlZDogdGltZS5nZXRVbml4VGltZSgpXG4gICAgfSlcbiAgICBjb25zdCBhZGRlZCA9IFtdXG4gICAgY29uc3QgdXBkYXRlZCA9IFtdXG4gICAgY29uc3QgZmlsdGVyZWRVcGRhdGVkID0gW11cbiAgICBjb25zdCByZW1vdmVkID0gW11cbiAgICBpZiAoc3RhdGUgPT09IG51bGwpIHtcbiAgICAgIHJlbW92ZWQucHVzaChjbGllbnRJRClcbiAgICB9IGVsc2UgaWYgKHByZXZTdGF0ZSA9PSBudWxsKSB7XG4gICAgICBpZiAoc3RhdGUgIT0gbnVsbCkge1xuICAgICAgICBhZGRlZC5wdXNoKGNsaWVudElEKVxuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICB1cGRhdGVkLnB1c2goY2xpZW50SUQpXG4gICAgICBpZiAoIWYuZXF1YWxpdHlEZWVwKHByZXZTdGF0ZSwgc3RhdGUpKSB7XG4gICAgICAgIGZpbHRlcmVkVXBkYXRlZC5wdXNoKGNsaWVudElEKVxuICAgICAgfVxuICAgIH1cbiAgICBpZiAoYWRkZWQubGVuZ3RoID4gMCB8fCBmaWx0ZXJlZFVwZGF0ZWQubGVuZ3RoID4gMCB8fCByZW1vdmVkLmxlbmd0aCA+IDApIHtcbiAgICAgIHRoaXMuZW1pdCgnY2hhbmdlJywgW3sgYWRkZWQsIHVwZGF0ZWQ6IGZpbHRlcmVkVXBkYXRlZCwgcmVtb3ZlZCB9LCAnbG9jYWwnXSlcbiAgICB9XG4gICAgdGhpcy5lbWl0KCd1cGRhdGUnLCBbeyBhZGRlZCwgdXBkYXRlZCwgcmVtb3ZlZCB9LCAnbG9jYWwnXSlcbiAgfVxuXG4gIC8qKlxuICAgKiBAcGFyYW0ge3N0cmluZ30gZmllbGRcbiAgICogQHBhcmFtIHthbnl9IHZhbHVlXG4gICAqL1xuICBzZXRMb2NhbFN0YXRlRmllbGQgKGZpZWxkLCB2YWx1ZSkge1xuICAgIGNvbnN0IHN0YXRlID0gdGhpcy5nZXRMb2NhbFN0YXRlKClcbiAgICBpZiAoc3RhdGUgIT09IG51bGwpIHtcbiAgICAgIHRoaXMuc2V0TG9jYWxTdGF0ZSh7XG4gICAgICAgIC4uLnN0YXRlLFxuICAgICAgICBbZmllbGRdOiB2YWx1ZVxuICAgICAgfSlcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQHJldHVybiB7TWFwPG51bWJlcixPYmplY3Q8c3RyaW5nLGFueT4+fVxuICAgKi9cbiAgZ2V0U3RhdGVzICgpIHtcbiAgICByZXR1cm4gdGhpcy5zdGF0ZXNcbiAgfVxufVxuXG4vKipcbiAqIE1hcmsgKHJlbW90ZSkgY2xpZW50cyBhcyBpbmFjdGl2ZSBhbmQgcmVtb3ZlIHRoZW0gZnJvbSB0aGUgbGlzdCBvZiBhY3RpdmUgcGVlcnMuXG4gKiBUaGlzIGNoYW5nZSB3aWxsIGJlIHByb3BhZ2F0ZWQgdG8gcmVtb3RlIGNsaWVudHMuXG4gKlxuICogQHBhcmFtIHtBd2FyZW5lc3N9IGF3YXJlbmVzc1xuICogQHBhcmFtIHtBcnJheTxudW1iZXI+fSBjbGllbnRzXG4gKiBAcGFyYW0ge2FueX0gb3JpZ2luXG4gKi9cbmV4cG9ydCBjb25zdCByZW1vdmVBd2FyZW5lc3NTdGF0ZXMgPSAoYXdhcmVuZXNzLCBjbGllbnRzLCBvcmlnaW4pID0+IHtcbiAgY29uc3QgcmVtb3ZlZCA9IFtdXG4gIGZvciAobGV0IGkgPSAwOyBpIDwgY2xpZW50cy5sZW5ndGg7IGkrKykge1xuICAgIGNvbnN0IGNsaWVudElEID0gY2xpZW50c1tpXVxuICAgIGlmIChhd2FyZW5lc3Muc3RhdGVzLmhhcyhjbGllbnRJRCkpIHtcbiAgICAgIGF3YXJlbmVzcy5zdGF0ZXMuZGVsZXRlKGNsaWVudElEKVxuICAgICAgaWYgKGNsaWVudElEID09PSBhd2FyZW5lc3MuY2xpZW50SUQpIHtcbiAgICAgICAgY29uc3QgY3VyTWV0YSA9IC8qKiBAdHlwZSB7TWV0YUNsaWVudFN0YXRlfSAqLyAoYXdhcmVuZXNzLm1ldGEuZ2V0KGNsaWVudElEKSlcbiAgICAgICAgYXdhcmVuZXNzLm1ldGEuc2V0KGNsaWVudElELCB7XG4gICAgICAgICAgY2xvY2s6IGN1ck1ldGEuY2xvY2sgKyAxLFxuICAgICAgICAgIGxhc3RVcGRhdGVkOiB0aW1lLmdldFVuaXhUaW1lKClcbiAgICAgICAgfSlcbiAgICAgIH1cbiAgICAgIHJlbW92ZWQucHVzaChjbGllbnRJRClcbiAgICB9XG4gIH1cbiAgaWYgKHJlbW92ZWQubGVuZ3RoID4gMCkge1xuICAgIGF3YXJlbmVzcy5lbWl0KCdjaGFuZ2UnLCBbeyBhZGRlZDogW10sIHVwZGF0ZWQ6IFtdLCByZW1vdmVkIH0sIG9yaWdpbl0pXG4gICAgYXdhcmVuZXNzLmVtaXQoJ3VwZGF0ZScsIFt7IGFkZGVkOiBbXSwgdXBkYXRlZDogW10sIHJlbW92ZWQgfSwgb3JpZ2luXSlcbiAgfVxufVxuXG4vKipcbiAqIEBwYXJhbSB7QXdhcmVuZXNzfSBhd2FyZW5lc3NcbiAqIEBwYXJhbSB7QXJyYXk8bnVtYmVyPn0gY2xpZW50c1xuICogQHJldHVybiB7VWludDhBcnJheX1cbiAqL1xuZXhwb3J0IGNvbnN0IGVuY29kZUF3YXJlbmVzc1VwZGF0ZSA9IChhd2FyZW5lc3MsIGNsaWVudHMsIHN0YXRlcyA9IGF3YXJlbmVzcy5zdGF0ZXMpID0+IHtcbiAgY29uc3QgbGVuID0gY2xpZW50cy5sZW5ndGhcbiAgY29uc3QgZW5jb2RlciA9IGVuY29kaW5nLmNyZWF0ZUVuY29kZXIoKVxuICBlbmNvZGluZy53cml0ZVZhclVpbnQoZW5jb2RlciwgbGVuKVxuICBmb3IgKGxldCBpID0gMDsgaSA8IGxlbjsgaSsrKSB7XG4gICAgY29uc3QgY2xpZW50SUQgPSBjbGllbnRzW2ldXG4gICAgY29uc3Qgc3RhdGUgPSBzdGF0ZXMuZ2V0KGNsaWVudElEKSB8fCBudWxsXG4gICAgY29uc3QgY2xvY2sgPSAvKiogQHR5cGUge01ldGFDbGllbnRTdGF0ZX0gKi8gKGF3YXJlbmVzcy5tZXRhLmdldChjbGllbnRJRCkpLmNsb2NrXG4gICAgZW5jb2Rpbmcud3JpdGVWYXJVaW50KGVuY29kZXIsIGNsaWVudElEKVxuICAgIGVuY29kaW5nLndyaXRlVmFyVWludChlbmNvZGVyLCBjbG9jaylcbiAgICBlbmNvZGluZy53cml0ZVZhclN0cmluZyhlbmNvZGVyLCBKU09OLnN0cmluZ2lmeShzdGF0ZSkpXG4gIH1cbiAgcmV0dXJuIGVuY29kaW5nLnRvVWludDhBcnJheShlbmNvZGVyKVxufVxuXG4vKipcbiAqIE1vZGlmeSB0aGUgY29udGVudCBvZiBhbiBhd2FyZW5lc3MgdXBkYXRlIGJlZm9yZSByZS1lbmNvZGluZyBpdCB0byBhbiBhd2FyZW5lc3MgdXBkYXRlLlxuICpcbiAqIFRoaXMgbWlnaHQgYmUgdXNlZnVsIHdoZW4geW91IGhhdmUgYSBjZW50cmFsIHNlcnZlciB0aGF0IHdhbnRzIHRvIGVuc3VyZSB0aGF0IGNsaWVudHNcbiAqIGNhbnQgaGlqYWNrIHNvbWVib2R5IGVsc2VzIGlkZW50aXR5LlxuICpcbiAqIEBwYXJhbSB7VWludDhBcnJheX0gdXBkYXRlXG4gKiBAcGFyYW0ge2Z1bmN0aW9uKGFueSk6YW55fSBtb2RpZnlcbiAqIEByZXR1cm4ge1VpbnQ4QXJyYXl9XG4gKi9cbmV4cG9ydCBjb25zdCBtb2RpZnlBd2FyZW5lc3NVcGRhdGUgPSAodXBkYXRlLCBtb2RpZnkpID0+IHtcbiAgY29uc3QgZGVjb2RlciA9IGRlY29kaW5nLmNyZWF0ZURlY29kZXIodXBkYXRlKVxuICBjb25zdCBlbmNvZGVyID0gZW5jb2RpbmcuY3JlYXRlRW5jb2RlcigpXG4gIGNvbnN0IGxlbiA9IGRlY29kaW5nLnJlYWRWYXJVaW50KGRlY29kZXIpXG4gIGVuY29kaW5nLndyaXRlVmFyVWludChlbmNvZGVyLCBsZW4pXG4gIGZvciAobGV0IGkgPSAwOyBpIDwgbGVuOyBpKyspIHtcbiAgICBjb25zdCBjbGllbnRJRCA9IGRlY29kaW5nLnJlYWRWYXJVaW50KGRlY29kZXIpXG4gICAgY29uc3QgY2xvY2sgPSBkZWNvZGluZy5yZWFkVmFyVWludChkZWNvZGVyKVxuICAgIGNvbnN0IHN0YXRlID0gSlNPTi5wYXJzZShkZWNvZGluZy5yZWFkVmFyU3RyaW5nKGRlY29kZXIpKVxuICAgIGNvbnN0IG1vZGlmaWVkU3RhdGUgPSBtb2RpZnkoc3RhdGUpXG4gICAgZW5jb2Rpbmcud3JpdGVWYXJVaW50KGVuY29kZXIsIGNsaWVudElEKVxuICAgIGVuY29kaW5nLndyaXRlVmFyVWludChlbmNvZGVyLCBjbG9jaylcbiAgICBlbmNvZGluZy53cml0ZVZhclN0cmluZyhlbmNvZGVyLCBKU09OLnN0cmluZ2lmeShtb2RpZmllZFN0YXRlKSlcbiAgfVxuICByZXR1cm4gZW5jb2RpbmcudG9VaW50OEFycmF5KGVuY29kZXIpXG59XG5cbi8qKlxuICogQHBhcmFtIHtBd2FyZW5lc3N9IGF3YXJlbmVzc1xuICogQHBhcmFtIHtVaW50OEFycmF5fSB1cGRhdGVcbiAqIEBwYXJhbSB7YW55fSBvcmlnaW4gVGhpcyB3aWxsIGJlIGFkZGVkIHRvIHRoZSBlbWl0dGVkIGNoYW5nZSBldmVudFxuICovXG5leHBvcnQgY29uc3QgYXBwbHlBd2FyZW5lc3NVcGRhdGUgPSAoYXdhcmVuZXNzLCB1cGRhdGUsIG9yaWdpbikgPT4ge1xuICBjb25zdCBkZWNvZGVyID0gZGVjb2RpbmcuY3JlYXRlRGVjb2Rlcih1cGRhdGUpXG4gIGNvbnN0IHRpbWVzdGFtcCA9IHRpbWUuZ2V0VW5peFRpbWUoKVxuICBjb25zdCBhZGRlZCA9IFtdXG4gIGNvbnN0IHVwZGF0ZWQgPSBbXVxuICBjb25zdCBmaWx0ZXJlZFVwZGF0ZWQgPSBbXVxuICBjb25zdCByZW1vdmVkID0gW11cbiAgY29uc3QgbGVuID0gZGVjb2RpbmcucmVhZFZhclVpbnQoZGVjb2RlcilcbiAgZm9yIChsZXQgaSA9IDA7IGkgPCBsZW47IGkrKykge1xuICAgIGNvbnN0IGNsaWVudElEID0gZGVjb2RpbmcucmVhZFZhclVpbnQoZGVjb2RlcilcbiAgICBsZXQgY2xvY2sgPSBkZWNvZGluZy5yZWFkVmFyVWludChkZWNvZGVyKVxuICAgIGNvbnN0IHN0YXRlID0gSlNPTi5wYXJzZShkZWNvZGluZy5yZWFkVmFyU3RyaW5nKGRlY29kZXIpKVxuICAgIGNvbnN0IGNsaWVudE1ldGEgPSBhd2FyZW5lc3MubWV0YS5nZXQoY2xpZW50SUQpXG4gICAgY29uc3QgcHJldlN0YXRlID0gYXdhcmVuZXNzLnN0YXRlcy5nZXQoY2xpZW50SUQpXG4gICAgY29uc3QgY3VyckNsb2NrID0gY2xpZW50TWV0YSA9PT0gdW5kZWZpbmVkID8gMCA6IGNsaWVudE1ldGEuY2xvY2tcbiAgICBpZiAoY3VyckNsb2NrIDwgY2xvY2sgfHwgKGN1cnJDbG9jayA9PT0gY2xvY2sgJiYgc3RhdGUgPT09IG51bGwgJiYgYXdhcmVuZXNzLnN0YXRlcy5oYXMoY2xpZW50SUQpKSkge1xuICAgICAgaWYgKHN0YXRlID09PSBudWxsKSB7XG4gICAgICAgIC8vIG5ldmVyIGxldCBhIHJlbW90ZSBjbGllbnQgcmVtb3ZlIHRoaXMgbG9jYWwgc3RhdGVcbiAgICAgICAgaWYgKGNsaWVudElEID09PSBhd2FyZW5lc3MuY2xpZW50SUQgJiYgYXdhcmVuZXNzLmdldExvY2FsU3RhdGUoKSAhPSBudWxsKSB7XG4gICAgICAgICAgLy8gcmVtb3RlIGNsaWVudCByZW1vdmVkIHRoZSBsb2NhbCBzdGF0ZS4gRG8gbm90IHJlbW90ZSBzdGF0ZS4gQnJvYWRjYXN0IGEgbWVzc2FnZSBpbmRpY2F0aW5nXG4gICAgICAgICAgLy8gdGhhdCB0aGlzIGNsaWVudCBzdGlsbCBleGlzdHMgYnkgaW5jcmVhc2luZyB0aGUgY2xvY2tcbiAgICAgICAgICBjbG9jaysrXG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgYXdhcmVuZXNzLnN0YXRlcy5kZWxldGUoY2xpZW50SUQpXG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGF3YXJlbmVzcy5zdGF0ZXMuc2V0KGNsaWVudElELCBzdGF0ZSlcbiAgICAgIH1cbiAgICAgIGF3YXJlbmVzcy5tZXRhLnNldChjbGllbnRJRCwge1xuICAgICAgICBjbG9jayxcbiAgICAgICAgbGFzdFVwZGF0ZWQ6IHRpbWVzdGFtcFxuICAgICAgfSlcbiAgICAgIGlmIChjbGllbnRNZXRhID09PSB1bmRlZmluZWQgJiYgc3RhdGUgIT09IG51bGwpIHtcbiAgICAgICAgYWRkZWQucHVzaChjbGllbnRJRClcbiAgICAgIH0gZWxzZSBpZiAoY2xpZW50TWV0YSAhPT0gdW5kZWZpbmVkICYmIHN0YXRlID09PSBudWxsKSB7XG4gICAgICAgIHJlbW92ZWQucHVzaChjbGllbnRJRClcbiAgICAgIH0gZWxzZSBpZiAoc3RhdGUgIT09IG51bGwpIHtcbiAgICAgICAgaWYgKCFmLmVxdWFsaXR5RGVlcChzdGF0ZSwgcHJldlN0YXRlKSkge1xuICAgICAgICAgIGZpbHRlcmVkVXBkYXRlZC5wdXNoKGNsaWVudElEKVxuICAgICAgICB9XG4gICAgICAgIHVwZGF0ZWQucHVzaChjbGllbnRJRClcbiAgICAgIH1cbiAgICB9XG4gIH1cbiAgaWYgKGFkZGVkLmxlbmd0aCA+IDAgfHwgZmlsdGVyZWRVcGRhdGVkLmxlbmd0aCA+IDAgfHwgcmVtb3ZlZC5sZW5ndGggPiAwKSB7XG4gICAgYXdhcmVuZXNzLmVtaXQoJ2NoYW5nZScsIFt7XG4gICAgICBhZGRlZCwgdXBkYXRlZDogZmlsdGVyZWRVcGRhdGVkLCByZW1vdmVkXG4gICAgfSwgb3JpZ2luXSlcbiAgfVxuICBpZiAoYWRkZWQubGVuZ3RoID4gMCB8fCB1cGRhdGVkLmxlbmd0aCA+IDAgfHwgcmVtb3ZlZC5sZW5ndGggPiAwKSB7XG4gICAgYXdhcmVuZXNzLmVtaXQoJ3VwZGF0ZScsIFt7XG4gICAgICBhZGRlZCwgdXBkYXRlZCwgcmVtb3ZlZFxuICAgIH0sIG9yaWdpbl0pXG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0=