(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_observables_lib_index_js"],{

/***/ "../packages/observables/lib/index.js":
/*!********************************************!*\
  !*** ../packages/observables/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ModelDB": () => (/* reexport safe */ _modeldb__WEBPACK_IMPORTED_MODULE_0__.ModelDB),
/* harmony export */   "ObservableValue": () => (/* reexport safe */ _modeldb__WEBPACK_IMPORTED_MODULE_0__.ObservableValue),
/* harmony export */   "ObservableJSON": () => (/* reexport safe */ _observablejson__WEBPACK_IMPORTED_MODULE_1__.ObservableJSON),
/* harmony export */   "ObservableList": () => (/* reexport safe */ _observablelist__WEBPACK_IMPORTED_MODULE_2__.ObservableList),
/* harmony export */   "ObservableMap": () => (/* reexport safe */ _observablemap__WEBPACK_IMPORTED_MODULE_3__.ObservableMap),
/* harmony export */   "ObservableString": () => (/* reexport safe */ _observablestring__WEBPACK_IMPORTED_MODULE_4__.ObservableString),
/* harmony export */   "ObservableUndoableList": () => (/* reexport safe */ _undoablelist__WEBPACK_IMPORTED_MODULE_5__.ObservableUndoableList)
/* harmony export */ });
/* harmony import */ var _modeldb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./modeldb */ "../packages/observables/lib/modeldb.js");
/* harmony import */ var _observablejson__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./observablejson */ "../packages/observables/lib/observablejson.js");
/* harmony import */ var _observablelist__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./observablelist */ "../packages/observables/lib/observablelist.js");
/* harmony import */ var _observablemap__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./observablemap */ "../packages/observables/lib/observablemap.js");
/* harmony import */ var _observablestring__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./observablestring */ "../packages/observables/lib/observablestring.js");
/* harmony import */ var _undoablelist__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./undoablelist */ "../packages/observables/lib/undoablelist.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module observables
 */








/***/ }),

/***/ "../packages/observables/lib/modeldb.js":
/*!**********************************************!*\
  !*** ../packages/observables/lib/modeldb.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableValue": () => (/* binding */ ObservableValue),
/* harmony export */   "ModelDB": () => (/* binding */ ModelDB)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _observablejson__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./observablejson */ "../packages/observables/lib/observablejson.js");
/* harmony import */ var _observablemap__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./observablemap */ "../packages/observables/lib/observablemap.js");
/* harmony import */ var _observablestring__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./observablestring */ "../packages/observables/lib/observablestring.js");
/* harmony import */ var _undoablelist__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./undoablelist */ "../packages/observables/lib/undoablelist.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * A concrete implementation of an `IObservableValue`.
 */
class ObservableValue {
    /**
     * Constructor for the value.
     *
     * @param initialValue: the starting value for the `ObservableValue`.
     */
    constructor(initialValue = null) {
        this._value = null;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._isDisposed = false;
        this._value = initialValue;
    }
    /**
     * The observable type.
     */
    get type() {
        return 'Value';
    }
    /**
     * Whether the value has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * The changed signal.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Get the current value, or `undefined` if it has not been set.
     */
    get() {
        return this._value;
    }
    /**
     * Set the current value.
     */
    set(value) {
        const oldValue = this._value;
        if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.JSONExt.deepEqual(oldValue, value)) {
            return;
        }
        this._value = value;
        this._changed.emit({
            oldValue: oldValue,
            newValue: value
        });
    }
    /**
     * Dispose of the resources held by the value.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
        this._value = null;
    }
}
/**
 * The namespace for the `ObservableValue` class statics.
 */
(function (ObservableValue) {
    /**
     * The changed args object emitted by the `IObservableValue`.
     */
    class IChangedArgs {
    }
    ObservableValue.IChangedArgs = IChangedArgs;
})(ObservableValue || (ObservableValue = {}));
/**
 * A concrete implementation of an `IModelDB`.
 */
class ModelDB {
    /**
     * Constructor for the `ModelDB`.
     */
    constructor(options = {}) {
        /**
         * Whether the model has been populated with
         * any model values.
         */
        this.isPrepopulated = false;
        /**
         * Whether the model is collaborative.
         */
        this.isCollaborative = false;
        /**
         * A promise resolved when the model is connected
         * to its backend. For the in-memory ModelDB it
         * is immediately resolved.
         */
        this.connected = Promise.resolve(void 0);
        this._toDispose = false;
        this._isDisposed = false;
        this._disposables = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableSet();
        this._basePath = options.basePath || '';
        if (options.baseDB) {
            this._db = options.baseDB;
        }
        else {
            this._db = new _observablemap__WEBPACK_IMPORTED_MODULE_3__.ObservableMap();
            this._toDispose = true;
        }
    }
    /**
     * The base path for the `ModelDB`. This is prepended
     * to all the paths that are passed in to the member
     * functions of the object.
     */
    get basePath() {
        return this._basePath;
    }
    /**
     * Whether the database is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Get a value for a path.
     *
     * @param path: the path for the object.
     *
     * @returns an `IObservable`.
     */
    get(path) {
        return this._db.get(this._resolvePath(path));
    }
    /**
     * Whether the `IModelDB` has an object at this path.
     *
     * @param path: the path for the object.
     *
     * @returns a boolean for whether an object is at `path`.
     */
    has(path) {
        return this._db.has(this._resolvePath(path));
    }
    /**
     * Create a string and insert it in the database.
     *
     * @param path: the path for the string.
     *
     * @returns the string that was created.
     */
    createString(path) {
        const str = new _observablestring__WEBPACK_IMPORTED_MODULE_4__.ObservableString();
        this._disposables.add(str);
        this.set(path, str);
        return str;
    }
    /**
     * Create an undoable list and insert it in the database.
     *
     * @param path: the path for the list.
     *
     * @returns the list that was created.
     *
     * #### Notes
     * The list can only store objects that are simple
     * JSON Objects and primitives.
     */
    createList(path) {
        const vec = new _undoablelist__WEBPACK_IMPORTED_MODULE_5__.ObservableUndoableList(new _undoablelist__WEBPACK_IMPORTED_MODULE_5__.ObservableUndoableList.IdentitySerializer());
        this._disposables.add(vec);
        this.set(path, vec);
        return vec;
    }
    /**
     * Create a map and insert it in the database.
     *
     * @param path: the path for the map.
     *
     * @returns the map that was created.
     *
     * #### Notes
     * The map can only store objects that are simple
     * JSON Objects and primitives.
     */
    createMap(path) {
        const map = new _observablejson__WEBPACK_IMPORTED_MODULE_6__.ObservableJSON();
        this._disposables.add(map);
        this.set(path, map);
        return map;
    }
    /**
     * Create an opaque value and insert it in the database.
     *
     * @param path: the path for the value.
     *
     * @returns the value that was created.
     */
    createValue(path) {
        const val = new ObservableValue();
        this._disposables.add(val);
        this.set(path, val);
        return val;
    }
    /**
     * Get a value at a path, or `undefined if it has not been set
     * That value must already have been created using `createValue`.
     *
     * @param path: the path for the value.
     */
    getValue(path) {
        const val = this.get(path);
        if (!val || val.type !== 'Value') {
            throw Error('Can only call getValue for an ObservableValue');
        }
        return val.get();
    }
    /**
     * Set a value at a path. That value must already have
     * been created using `createValue`.
     *
     * @param path: the path for the value.
     *
     * @param value: the new value.
     */
    setValue(path, value) {
        const val = this.get(path);
        if (!val || val.type !== 'Value') {
            throw Error('Can only call setValue on an ObservableValue');
        }
        val.set(value);
    }
    /**
     * Create a view onto a subtree of the model database.
     *
     * @param basePath: the path for the root of the subtree.
     *
     * @returns an `IModelDB` with a view onto the original
     *   `IModelDB`, with `basePath` prepended to all paths.
     */
    view(basePath) {
        const view = new ModelDB({ basePath, baseDB: this });
        this._disposables.add(view);
        return view;
    }
    /**
     * Set a value at a path. Not intended to
     * be called by user code, instead use the
     * `create*` factory methods.
     *
     * @param path: the path to set the value at.
     *
     * @param value: the value to set at the path.
     */
    set(path, value) {
        this._db.set(this._resolvePath(path), value);
    }
    /**
     * Dispose of the resources held by the database.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        if (this._toDispose) {
            this._db.dispose();
        }
        this._disposables.dispose();
    }
    /**
     * Compute the fully resolved path for a path argument.
     */
    _resolvePath(path) {
        if (this._basePath) {
            path = this._basePath + '.' + path;
        }
        return path;
    }
}


/***/ }),

/***/ "../packages/observables/lib/observablejson.js":
/*!*****************************************************!*\
  !*** ../packages/observables/lib/observablejson.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableJSON": () => (/* binding */ ObservableJSON)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging/@lumino/messaging");
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_messaging__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _observablemap__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./observablemap */ "../packages/observables/lib/observablemap.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A concrete Observable map for JSON data.
 */
class ObservableJSON extends _observablemap__WEBPACK_IMPORTED_MODULE_2__.ObservableMap {
    /**
     * Construct a new observable JSON object.
     */
    constructor(options = {}) {
        super({
            itemCmp: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.JSONExt.deepEqual,
            values: options.values
        });
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        const out = Object.create(null);
        const keys = this.keys();
        for (const key of keys) {
            const value = this.get(key);
            if (value !== undefined) {
                out[key] = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.JSONExt.deepCopy(value);
            }
        }
        return out;
    }
}
/**
 * The namespace for ObservableJSON static data.
 */
(function (ObservableJSON) {
    /**
     * An observable JSON change message.
     */
    class ChangeMessage extends _lumino_messaging__WEBPACK_IMPORTED_MODULE_1__.Message {
        /**
         * Create a new metadata changed message.
         */
        constructor(type, args) {
            super(type);
            this.args = args;
        }
    }
    ObservableJSON.ChangeMessage = ChangeMessage;
})(ObservableJSON || (ObservableJSON = {}));


/***/ }),

/***/ "../packages/observables/lib/observablelist.js":
/*!*****************************************************!*\
  !*** ../packages/observables/lib/observablelist.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableList": () => (/* binding */ ObservableList)
/* harmony export */ });
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A concrete implementation of [[IObservableList]].
 */
class ObservableList {
    /**
     * Construct a new observable map.
     */
    constructor(options = {}) {
        this._array = [];
        this._isDisposed = false;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        if (options.values !== void 0) {
            (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(options.values, value => {
                this._array.push(value);
            });
        }
        this._itemCmp = options.itemCmp || Private.itemCmp;
    }
    /**
     * The type of this object.
     */
    get type() {
        return 'List';
    }
    /**
     * A signal emitted when the list has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * The length of the list.
     */
    get length() {
        return this._array.length;
    }
    /**
     * Test whether the list has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the list.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.clearData(this);
        this.clear();
    }
    /**
     * Create an iterator over the values in the list.
     *
     * @returns A new iterator starting at the front of the list.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     */
    iter() {
        return new _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayIterator(this._array);
    }
    /**
     * Get the value at the specified index.
     *
     * @param index - The positive integer index of interest.
     *
     * @returns The value at the specified index.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral or out of range.
     */
    get(index) {
        return this._array[index];
    }
    /**
     * Set the value at the specified index.
     *
     * @param index - The positive integer index of interest.
     *
     * @param value - The value to set at the specified index.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral or out of range.
     */
    set(index, value) {
        const oldValue = this._array[index];
        if (value === undefined) {
            throw new Error('Cannot set an undefined item');
        }
        // Bail if the value does not change.
        const itemCmp = this._itemCmp;
        if (itemCmp(oldValue, value)) {
            return;
        }
        this._array[index] = value;
        this._changed.emit({
            type: 'set',
            oldIndex: index,
            newIndex: index,
            oldValues: [oldValue],
            newValues: [value]
        });
    }
    /**
     * Add a value to the end of the list.
     *
     * @param value - The value to add to the end of the list.
     *
     * @returns The new length of the list.
     *
     * #### Complexity
     * Constant.
     *
     * #### Notes
     * By convention, the oldIndex is set to -1 to indicate
     * an push operation.
     *
     * #### Iterator Validity
     * No changes.
     */
    push(value) {
        const num = this._array.push(value);
        this._changed.emit({
            type: 'add',
            oldIndex: -1,
            newIndex: this.length - 1,
            oldValues: [],
            newValues: [value]
        });
        return num;
    }
    /**
     * Insert a value into the list at a specific index.
     *
     * @param index - The index at which to insert the value.
     *
     * @param value - The value to set at the specified index.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * The `index` will be clamped to the bounds of the list.
     *
     * By convention, the oldIndex is set to -2 to indicate
     * an insert operation.
     *
     * The value -2 as oldIndex can be used to distinguish from the push
     * method which will use a value -1.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral.
     */
    insert(index, value) {
        if (index === this._array.length) {
            this._array.push(value);
        }
        else {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.insert(this._array, index, value);
        }
        this._changed.emit({
            type: 'add',
            oldIndex: -2,
            newIndex: index,
            oldValues: [],
            newValues: [value]
        });
    }
    /**
     * Remove the first occurrence of a value from the list.
     *
     * @param value - The value of interest.
     *
     * @returns The index of the removed value, or `-1` if the value
     *   is not contained in the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * Iterators pointing at the removed value and beyond are invalidated.
     */
    removeValue(value) {
        const itemCmp = this._itemCmp;
        const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.findFirstIndex(this._array, item => {
            return itemCmp(item, value);
        });
        this.remove(index);
        return index;
    }
    /**
     * Remove and return the value at a specific index.
     *
     * @param index - The index of the value of interest.
     *
     * @returns The value at the specified index, or `undefined` if the
     *   index is out of range.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * Iterators pointing at the removed value and beyond are invalidated.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral.
     */
    remove(index) {
        const value = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.removeAt(this._array, index);
        if (value === undefined) {
            return;
        }
        this._changed.emit({
            type: 'remove',
            oldIndex: index,
            newIndex: -1,
            newValues: [],
            oldValues: [value]
        });
        return value;
    }
    /**
     * Remove all values from the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * All current iterators are invalidated.
     */
    clear() {
        const copy = this._array.slice();
        this._array.length = 0;
        this._changed.emit({
            type: 'remove',
            oldIndex: 0,
            newIndex: 0,
            newValues: [],
            oldValues: copy
        });
    }
    /**
     * Move a value from one index to another.
     *
     * @parm fromIndex - The index of the element to move.
     *
     * @param toIndex - The index to move the element to.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * Iterators pointing at the lesser of the `fromIndex` and the `toIndex`
     * and beyond are invalidated.
     *
     * #### Undefined Behavior
     * A `fromIndex` or a `toIndex` which is non-integral.
     */
    move(fromIndex, toIndex) {
        if (this.length <= 1 || fromIndex === toIndex) {
            return;
        }
        const values = [this._array[fromIndex]];
        _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.move(this._array, fromIndex, toIndex);
        this._changed.emit({
            type: 'move',
            oldIndex: fromIndex,
            newIndex: toIndex,
            oldValues: values,
            newValues: values
        });
    }
    /**
     * Push a set of values to the back of the list.
     *
     * @param values - An iterable or array-like set of values to add.
     *
     * @returns The new length of the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Notes
     * By convention, the oldIndex is set to -1 to indicate
     * an push operation.
     *
     * #### Iterator Validity
     * No changes.
     */
    pushAll(values) {
        const newIndex = this.length;
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(values, value => {
            this._array.push(value);
        });
        this._changed.emit({
            type: 'add',
            oldIndex: -1,
            newIndex,
            oldValues: [],
            newValues: (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.toArray)(values)
        });
        return this.length;
    }
    /**
     * Insert a set of items into the list at the specified index.
     *
     * @param index - The index at which to insert the values.
     *
     * @param values - The values to insert at the specified index.
     *
     * #### Complexity.
     * Linear.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * The `index` will be clamped to the bounds of the list.
     * By convention, the oldIndex is set to -2 to indicate
     * an insert operation.
     *
     * #### Undefined Behavior.
     * An `index` which is non-integral.
     */
    insertAll(index, values) {
        const newIndex = index;
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(values, value => {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.insert(this._array, index++, value);
        });
        this._changed.emit({
            type: 'add',
            oldIndex: -2,
            newIndex,
            oldValues: [],
            newValues: (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.toArray)(values)
        });
    }
    /**
     * Remove a range of items from the list.
     *
     * @param startIndex - The start index of the range to remove (inclusive).
     *
     * @param endIndex - The end index of the range to remove (exclusive).
     *
     * @returns The new length of the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * Iterators pointing to the first removed value and beyond are invalid.
     *
     * #### Undefined Behavior
     * A `startIndex` or `endIndex` which is non-integral.
     */
    removeRange(startIndex, endIndex) {
        const oldValues = this._array.slice(startIndex, endIndex);
        for (let i = startIndex; i < endIndex; i++) {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.removeAt(this._array, startIndex);
        }
        this._changed.emit({
            type: 'remove',
            oldIndex: startIndex,
            newIndex: -1,
            oldValues,
            newValues: []
        });
        return this.length;
    }
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The default strict equality item cmp.
     */
    function itemCmp(first, second) {
        return first === second;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/observables/lib/observablemap.js":
/*!****************************************************!*\
  !*** ../packages/observables/lib/observablemap.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableMap": () => (/* binding */ ObservableMap)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A concrete implementation of IObservableMap<T>.
 */
class ObservableMap {
    /**
     * Construct a new observable map.
     */
    constructor(options = {}) {
        this._map = new Map();
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._isDisposed = false;
        this._itemCmp = options.itemCmp || Private.itemCmp;
        if (options.values) {
            for (const key in options.values) {
                this._map.set(key, options.values[key]);
            }
        }
    }
    /**
     * The type of the Observable.
     */
    get type() {
        return 'Map';
    }
    /**
     * A signal emitted when the map has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Whether this map has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * The number of key-value pairs in the map.
     */
    get size() {
        return this._map.size;
    }
    /**
     * Set a key-value pair in the map
     *
     * @param key - The key to set.
     *
     * @param value - The value for the key.
     *
     * @returns the old value for the key, or undefined
     *   if that did not exist.
     *
     * @throws if the new value is undefined.
     *
     * #### Notes
     * This is a no-op if the value does not change.
     */
    set(key, value) {
        const oldVal = this._map.get(key);
        if (value === undefined) {
            throw Error('Cannot set an undefined value, use remove');
        }
        // Bail if the value does not change.
        const itemCmp = this._itemCmp;
        if (oldVal !== undefined && itemCmp(oldVal, value)) {
            return oldVal;
        }
        this._map.set(key, value);
        this._changed.emit({
            type: oldVal ? 'change' : 'add',
            key: key,
            oldValue: oldVal,
            newValue: value
        });
        return oldVal;
    }
    /**
     * Get a value for a given key.
     *
     * @param key - the key.
     *
     * @returns the value for that key.
     */
    get(key) {
        return this._map.get(key);
    }
    /**
     * Check whether the map has a key.
     *
     * @param key - the key to check.
     *
     * @returns `true` if the map has the key, `false` otherwise.
     */
    has(key) {
        return this._map.has(key);
    }
    /**
     * Get a list of the keys in the map.
     *
     * @returns - a list of keys.
     */
    keys() {
        const keyList = [];
        this._map.forEach((v, k) => {
            keyList.push(k);
        });
        return keyList;
    }
    /**
     * Get a list of the values in the map.
     *
     * @returns - a list of values.
     */
    values() {
        const valList = [];
        this._map.forEach((v, k) => {
            valList.push(v);
        });
        return valList;
    }
    /**
     * Remove a key from the map
     *
     * @param key - the key to remove.
     *
     * @returns the value of the given key,
     *   or undefined if that does not exist.
     *
     * #### Notes
     * This is a no-op if the value does not change.
     */
    delete(key) {
        const oldVal = this._map.get(key);
        const removed = this._map.delete(key);
        if (removed) {
            this._changed.emit({
                type: 'remove',
                key: key,
                oldValue: oldVal,
                newValue: undefined
            });
        }
        return oldVal;
    }
    /**
     * Set the ObservableMap to an empty map.
     */
    clear() {
        // Delete one by one to emit the correct signals.
        const keyList = this.keys();
        for (let i = 0; i < keyList.length; i++) {
            this.delete(keyList[i]);
        }
    }
    /**
     * Dispose of the resources held by the map.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
        this._map.clear();
    }
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The default strict equality item comparator.
     */
    function itemCmp(first, second) {
        return first === second;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/observables/lib/observablestring.js":
/*!*******************************************************!*\
  !*** ../packages/observables/lib/observablestring.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableString": () => (/* binding */ ObservableString)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A concrete implementation of [[IObservableString]]
 */
class ObservableString {
    /**
     * Construct a new observable string.
     */
    constructor(initialText = '') {
        this._text = '';
        this._isDisposed = false;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._text = initialText;
    }
    /**
     * The type of the Observable.
     */
    get type() {
        return 'String';
    }
    /**
     * A signal emitted when the string has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Set the value of the string.
     */
    set text(value) {
        if (value.length === this._text.length && value === this._text) {
            return;
        }
        this._text = value;
        this._changed.emit({
            type: 'set',
            start: 0,
            end: value.length,
            value: value
        });
    }
    /**
     * Get the value of the string.
     */
    get text() {
        return this._text;
    }
    /**
     * Insert a substring.
     *
     * @param index - The starting index.
     *
     * @param text - The substring to insert.
     */
    insert(index, text) {
        this._text = this._text.slice(0, index) + text + this._text.slice(index);
        this._changed.emit({
            type: 'insert',
            start: index,
            end: index + text.length,
            value: text
        });
    }
    /**
     * Remove a substring.
     *
     * @param start - The starting index.
     *
     * @param end - The ending index.
     */
    remove(start, end) {
        const oldValue = this._text.slice(start, end);
        this._text = this._text.slice(0, start) + this._text.slice(end);
        this._changed.emit({
            type: 'remove',
            start: start,
            end: end,
            value: oldValue
        });
    }
    /**
     * Set the ObservableString to an empty string.
     */
    clear() {
        this.text = '';
    }
    /**
     * Test whether the string has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the string.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
        this.clear();
    }
}


/***/ }),

/***/ "../packages/observables/lib/undoablelist.js":
/*!***************************************************!*\
  !*** ../packages/observables/lib/undoablelist.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableUndoableList": () => (/* binding */ ObservableUndoableList)
/* harmony export */ });
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _observablelist__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./observablelist */ "../packages/observables/lib/observablelist.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A concrete implementation of an observable undoable list.
 */
class ObservableUndoableList extends _observablelist__WEBPACK_IMPORTED_MODULE_1__.ObservableList {
    /**
     * Construct a new undoable observable list.
     */
    constructor(serializer) {
        super();
        this._inCompound = false;
        this._isUndoable = true;
        this._madeCompoundChange = false;
        this._index = -1;
        this._stack = [];
        this._serializer = serializer;
        this.changed.connect(this._onListChanged, this);
    }
    /**
     * Whether the object can redo changes.
     */
    get canRedo() {
        return this._index < this._stack.length - 1;
    }
    /**
     * Whether the object can undo changes.
     */
    get canUndo() {
        return this._index >= 0;
    }
    /**
     * Begin a compound operation.
     *
     * @param isUndoAble - Whether the operation is undoable.
     *   The default is `true`.
     */
    beginCompoundOperation(isUndoAble) {
        this._inCompound = true;
        this._isUndoable = isUndoAble !== false;
        this._madeCompoundChange = false;
    }
    /**
     * End a compound operation.
     */
    endCompoundOperation() {
        this._inCompound = false;
        this._isUndoable = true;
        if (this._madeCompoundChange) {
            this._index++;
        }
    }
    /**
     * Undo an operation.
     */
    undo() {
        if (!this.canUndo) {
            return;
        }
        const changes = this._stack[this._index];
        this._isUndoable = false;
        for (const change of changes.reverse()) {
            this._undoChange(change);
        }
        this._isUndoable = true;
        this._index--;
    }
    /**
     * Redo an operation.
     */
    redo() {
        if (!this.canRedo) {
            return;
        }
        this._index++;
        const changes = this._stack[this._index];
        this._isUndoable = false;
        for (const change of changes) {
            this._redoChange(change);
        }
        this._isUndoable = true;
    }
    /**
     * Clear the change stack.
     */
    clearUndo() {
        this._index = -1;
        this._stack = [];
    }
    /**
     * Handle a change in the list.
     */
    _onListChanged(list, change) {
        if (this.isDisposed || !this._isUndoable) {
            return;
        }
        // Clear everything after this position if necessary.
        if (!this._inCompound || !this._madeCompoundChange) {
            this._stack = this._stack.slice(0, this._index + 1);
        }
        // Copy the change.
        const evt = this._copyChange(change);
        // Put the change in the stack.
        if (this._stack[this._index + 1]) {
            this._stack[this._index + 1].push(evt);
        }
        else {
            this._stack.push([evt]);
        }
        // If not in a compound operation, increase index.
        if (!this._inCompound) {
            this._index++;
        }
        else {
            this._madeCompoundChange = true;
        }
    }
    /**
     * Undo a change event.
     */
    _undoChange(change) {
        let index = 0;
        const serializer = this._serializer;
        switch (change.type) {
            case 'add':
                (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(change.newValues, () => {
                    this.remove(change.newIndex);
                });
                break;
            case 'set':
                index = change.oldIndex;
                (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(change.oldValues, value => {
                    this.set(index++, serializer.fromJSON(value));
                });
                break;
            case 'remove':
                index = change.oldIndex;
                (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(change.oldValues, value => {
                    this.insert(index++, serializer.fromJSON(value));
                });
                break;
            case 'move':
                this.move(change.newIndex, change.oldIndex);
                break;
            default:
                return;
        }
    }
    /**
     * Redo a change event.
     */
    _redoChange(change) {
        let index = 0;
        const serializer = this._serializer;
        switch (change.type) {
            case 'add':
                index = change.newIndex;
                (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(change.newValues, value => {
                    this.insert(index++, serializer.fromJSON(value));
                });
                break;
            case 'set':
                index = change.newIndex;
                (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(change.newValues, value => {
                    this.set(change.newIndex++, serializer.fromJSON(value));
                });
                break;
            case 'remove':
                (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(change.oldValues, () => {
                    this.remove(change.oldIndex);
                });
                break;
            case 'move':
                this.move(change.oldIndex, change.newIndex);
                break;
            default:
                return;
        }
    }
    /**
     * Copy a change as JSON.
     */
    _copyChange(change) {
        const oldValues = [];
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(change.oldValues, value => {
            oldValues.push(this._serializer.toJSON(value));
        });
        const newValues = [];
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.each)(change.newValues, value => {
            newValues.push(this._serializer.toJSON(value));
        });
        return {
            type: change.type,
            oldIndex: change.oldIndex,
            newIndex: change.newIndex,
            oldValues,
            newValues
        };
    }
}
/**
 * Namespace for ObservableUndoableList utilities.
 */
(function (ObservableUndoableList) {
    /**
     * A default, identity serializer.
     */
    class IdentitySerializer {
        /**
         * Identity serialize.
         */
        toJSON(value) {
            return value;
        }
        /**
         * Identity deserialize.
         */
        fromJSON(value) {
            return value;
        }
    }
    ObservableUndoableList.IdentitySerializer = IdentitySerializer;
})(ObservableUndoableList || (ObservableUndoableList = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvb2JzZXJ2YWJsZXMvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9vYnNlcnZhYmxlcy9zcmMvbW9kZWxkYi50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvb2JzZXJ2YWJsZXMvc3JjL29ic2VydmFibGVqc29uLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9vYnNlcnZhYmxlcy9zcmMvb2JzZXJ2YWJsZWxpc3QudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL29ic2VydmFibGVzL3NyYy9vYnNlcnZhYmxlbWFwLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9vYnNlcnZhYmxlcy9zcmMvb2JzZXJ2YWJsZXN0cmluZy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvb2JzZXJ2YWJsZXMvc3JjL3VuZG9hYmxlbGlzdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBRXVCO0FBQ087QUFDQTtBQUNEO0FBQ0c7QUFDSjs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDZC9CLDBDQUEwQztBQUMxQywyREFBMkQ7QUFPaEM7QUFDcUM7QUFDWjtBQUNlO0FBQ0g7QUFDUztBQUlqRDtBQW9PeEI7O0dBRUc7QUFDSSxNQUFNLGVBQWU7SUFDMUI7Ozs7T0FJRztJQUNILFlBQVksZUFBMEIsSUFBSTtRQTJEbEMsV0FBTSxHQUFjLElBQUksQ0FBQztRQUN6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bmRleF9qcy5lMzM2YzJjOWFkOWEyMWJlZjlmNC5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgb2JzZXJ2YWJsZXNcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL21vZGVsZGInO1xuZXhwb3J0ICogZnJvbSAnLi9vYnNlcnZhYmxlanNvbic7XG5leHBvcnQgKiBmcm9tICcuL29ic2VydmFibGVsaXN0JztcbmV4cG9ydCAqIGZyb20gJy4vb2JzZXJ2YWJsZW1hcCc7XG5leHBvcnQgKiBmcm9tICcuL29ic2VydmFibGVzdHJpbmcnO1xuZXhwb3J0ICogZnJvbSAnLi91bmRvYWJsZWxpc3QnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQge1xuICBKU09ORXh0LFxuICBKU09OT2JqZWN0LFxuICBKU09OVmFsdWUsXG4gIFBhcnRpYWxKU09OVmFsdWVcbn0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgRGlzcG9zYWJsZVNldCwgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgSU9ic2VydmFibGVKU09OLCBPYnNlcnZhYmxlSlNPTiB9IGZyb20gJy4vb2JzZXJ2YWJsZWpzb24nO1xuaW1wb3J0IHsgSU9ic2VydmFibGVNYXAsIE9ic2VydmFibGVNYXAgfSBmcm9tICcuL29ic2VydmFibGVtYXAnO1xuaW1wb3J0IHsgSU9ic2VydmFibGVTdHJpbmcsIE9ic2VydmFibGVTdHJpbmcgfSBmcm9tICcuL29ic2VydmFibGVzdHJpbmcnO1xuaW1wb3J0IHtcbiAgSU9ic2VydmFibGVVbmRvYWJsZUxpc3QsXG4gIE9ic2VydmFibGVVbmRvYWJsZUxpc3Rcbn0gZnJvbSAnLi91bmRvYWJsZWxpc3QnO1xuXG4vKipcbiAqIFN0cmluZyB0eXBlIGFubm90YXRpb25zIGZvciBPYnNlcnZhYmxlIG9iamVjdHMgdGhhdCBjYW4gYmVcbiAqIGNyZWF0ZWQgYW5kIHBsYWNlZCBpbiB0aGUgSU1vZGVsREIgaW50ZXJmYWNlLlxuICovXG5leHBvcnQgdHlwZSBPYnNlcnZhYmxlVHlwZSA9ICdNYXAnIHwgJ0xpc3QnIHwgJ1N0cmluZycgfCAnVmFsdWUnO1xuXG4vKipcbiAqIEJhc2UgaW50ZXJmYWNlIGZvciBPYnNlcnZhYmxlIG9iamVjdHMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU9ic2VydmFibGUgZXh0ZW5kcyBJRGlzcG9zYWJsZSB7XG4gIC8qKlxuICAgKiBUaGUgdHlwZSBvZiB0aGlzIG9iamVjdC5cbiAgICovXG4gIHJlYWRvbmx5IHR5cGU6IE9ic2VydmFibGVUeXBlO1xufVxuXG4vKipcbiAqIEludGVyZmFjZSBmb3IgYW4gT2JzZXJ2YWJsZSBvYmplY3QgdGhhdCByZXByZXNlbnRzXG4gKiBhbiBvcGFxdWUgSlNPTiB2YWx1ZS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJT2JzZXJ2YWJsZVZhbHVlIGV4dGVuZHMgSU9ic2VydmFibGUge1xuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhpcyBvYmplY3QuXG4gICAqL1xuICByZWFkb25seSB0eXBlOiAnVmFsdWUnO1xuXG4gIC8qKlxuICAgKiBUaGUgY2hhbmdlZCBzaWduYWwuXG4gICAqL1xuICByZWFkb25seSBjaGFuZ2VkOiBJU2lnbmFsPElPYnNlcnZhYmxlVmFsdWUsIE9ic2VydmFibGVWYWx1ZS5JQ2hhbmdlZEFyZ3M+O1xuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGN1cnJlbnQgdmFsdWUsIG9yIGB1bmRlZmluZWRgIGlmIGl0IGhhcyBub3QgYmVlbiBzZXQuXG4gICAqL1xuICBnZXQoKTogUGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcblxuICAvKipcbiAgICogU2V0IHRoZSB2YWx1ZS5cbiAgICovXG4gIHNldCh2YWx1ZTogUGFydGlhbEpTT05WYWx1ZSk6IHZvaWQ7XG59XG5cbi8qKlxuICogSW50ZXJmYWNlIGZvciBhbiBvYmplY3QgcmVwcmVzZW50aW5nIGEgc2luZ2xlIGNvbGxhYm9yYXRvclxuICogb24gYSByZWFsdGltZSBtb2RlbC5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJQ29sbGFib3JhdG9yIGV4dGVuZHMgSlNPTk9iamVjdCB7XG4gIC8qKlxuICAgKiBBIHVzZXIgaWQgZm9yIHRoZSBjb2xsYWJvcmF0b3IuXG4gICAqIFRoaXMgbWlnaHQgbm90IGJlIHVuaXF1ZSwgaWYgdGhlIHVzZXIgaGFzIG1vcmUgdGhhblxuICAgKiBvbmUgZWRpdGluZyBzZXNzaW9uIGF0IGEgdGltZS5cbiAgICovXG4gIHJlYWRvbmx5IHVzZXJJZDogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBBIHNlc3Npb24gaWQsIHdoaWNoIHNob3VsZCBiZSB1bmlxdWUgdG8gYVxuICAgKiBwYXJ0aWN1bGFyIHZpZXcgb24gYSBjb2xsYWJvcmF0aXZlIG1vZGVsLlxuICAgKi9cbiAgcmVhZG9ubHkgc2Vzc2lvbklkOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIEEgaHVtYW4tcmVhZGFibGUgZGlzcGxheSBuYW1lIGZvciBhIGNvbGxhYm9yYXRvci5cbiAgICovXG4gIHJlYWRvbmx5IGRpc3BsYXlOYW1lOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIEEgY29sb3IgdG8gYmUgdXNlZCB0byBpZGVudGlmeSB0aGUgY29sbGFib3JhdG9yIGluXG4gICAqIFVJIGVsZW1lbnRzLlxuICAgKi9cbiAgcmVhZG9ubHkgY29sb3I6IHN0cmluZztcblxuICAvKipcbiAgICogQSBodW1hbi1yZWFkYWJsZSBzaG9ydCBuYW1lIGZvciBhIGNvbGxhYm9yYXRvciwgZm9yXG4gICAqIHVzZSBpbiBwbGFjZXMgd2hlcmUgdGhlIGZ1bGwgYGRpc3BsYXlOYW1lYCB3b3VsZCB0YWtlXG4gICAqIHRvbyBtdWNoIHNwYWNlLlxuICAgKi9cbiAgcmVhZG9ubHkgc2hvcnROYW1lOiBzdHJpbmc7XG59XG5cbi8qKlxuICogSW50ZXJmYWNlIGZvciBhbiBJT2JzZXJ2YWJsZU1hcCB0aGF0IHRyYWNrcyBjb2xsYWJvcmF0b3JzLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElDb2xsYWJvcmF0b3JNYXAgZXh0ZW5kcyBJT2JzZXJ2YWJsZU1hcDxJQ29sbGFib3JhdG9yPiB7XG4gIC8qKlxuICAgKiBUaGUgbG9jYWwgY29sbGFib3JhdG9yIG9uIGEgbW9kZWwuXG4gICAqL1xuICByZWFkb25seSBsb2NhbENvbGxhYm9yYXRvcjogSUNvbGxhYm9yYXRvcjtcbn1cblxuLyoqXG4gKiBBbiBpbnRlcmZhY2UgZm9yIGEgcGF0aCBiYXNlZCBkYXRhYmFzZSBmb3JcbiAqIGNyZWF0aW5nIGFuZCBzdG9yaW5nIHZhbHVlcywgd2hpY2ggaXMgYWdub3N0aWNcbiAqIHRvIHRoZSBwYXJ0aWN1bGFyIHR5cGUgb2Ygc3RvcmUgaW4gdGhlIGJhY2tlbmQuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU1vZGVsREIgZXh0ZW5kcyBJRGlzcG9zYWJsZSB7XG4gIC8qKlxuICAgKiBUaGUgYmFzZSBwYXRoIGZvciB0aGUgYElNb2RlbERCYC4gVGhpcyBpcyBwcmVwZW5kZWRcbiAgICogdG8gYWxsIHRoZSBwYXRocyB0aGF0IGFyZSBwYXNzZWQgaW4gdG8gdGhlIG1lbWJlclxuICAgKiBmdW5jdGlvbnMgb2YgdGhlIG9iamVjdC5cbiAgICovXG4gIHJlYWRvbmx5IGJhc2VQYXRoOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGRhdGFiYXNlIGhhcyBiZWVuIGRpc3Bvc2VkLlxuICAgKi9cbiAgcmVhZG9ubHkgaXNEaXNwb3NlZDogYm9vbGVhbjtcblxuICAvKipcbiAgICogV2hldGhlciB0aGUgZGF0YWJhc2UgaGFzIGJlZW4gcG9wdWxhdGVkXG4gICAqIHdpdGggbW9kZWwgdmFsdWVzIHByaW9yIHRvIGNvbm5lY3Rpb24uXG4gICAqL1xuICByZWFkb25seSBpc1ByZXBvcHVsYXRlZDogYm9vbGVhbjtcblxuICAvKipcbiAgICogV2hldGhlciB0aGUgZGF0YWJhc2UgaXMgY29sbGFib3JhdGl2ZS5cbiAgICovXG4gIHJlYWRvbmx5IGlzQ29sbGFib3JhdGl2ZTogYm9vbGVhbjtcblxuICAvKipcbiAgICogQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgZGF0YWJhc2VcbiAgICogaGFzIGNvbm5lY3RlZCB0byBpdHMgYmFja2VuZCwgaWYgYW55LlxuICAgKi9cbiAgcmVhZG9ubHkgY29ubmVjdGVkOiBQcm9taXNlPHZvaWQ+O1xuXG4gIC8qKlxuICAgKiBBIG1hcCBvZiB0aGUgY3VycmVudGx5IGFjdGl2ZSBjb2xsYWJvcmF0b3JzXG4gICAqIGZvciB0aGUgZGF0YWJhc2UsIGluY2x1ZGluZyB0aGUgbG9jYWwgdXNlci5cbiAgICovXG4gIHJlYWRvbmx5IGNvbGxhYm9yYXRvcnM/OiBJQ29sbGFib3JhdG9yTWFwO1xuXG4gIC8qKlxuICAgKiBHZXQgYSB2YWx1ZSBmb3IgYSBwYXRoLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSBvYmplY3QuXG4gICAqXG4gICAqIEByZXR1cm5zIGFuIGBJT2JzZXJ2YWJsZWAuXG4gICAqL1xuICBnZXQocGF0aDogc3RyaW5nKTogSU9ic2VydmFibGUgfCB1bmRlZmluZWQ7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGBJTW9kZWxEQmAgaGFzIGFuIG9iamVjdCBhdCB0aGlzIHBhdGguXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIG9iamVjdC5cbiAgICpcbiAgICogQHJldHVybnMgYSBib29sZWFuIGZvciB3aGV0aGVyIGFuIG9iamVjdCBpcyBhdCBgcGF0aGAuXG4gICAqL1xuICBoYXMocGF0aDogc3RyaW5nKTogYm9vbGVhbjtcblxuICAvKipcbiAgICogQ3JlYXRlIGEgc3RyaW5nIGFuZCBpbnNlcnQgaXQgaW4gdGhlIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSBzdHJpbmcuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBzdHJpbmcgdGhhdCB3YXMgY3JlYXRlZC5cbiAgICovXG4gIGNyZWF0ZVN0cmluZyhwYXRoOiBzdHJpbmcpOiBJT2JzZXJ2YWJsZVN0cmluZztcblxuICAvKipcbiAgICogQ3JlYXRlIGFuIHVuZG9hYmxlIGxpc3QgYW5kIGluc2VydCBpdCBpbiB0aGUgZGF0YWJhc2UuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIGxpc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBsaXN0IHRoYXQgd2FzIGNyZWF0ZWQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIGxpc3QgY2FuIG9ubHkgc3RvcmUgb2JqZWN0cyB0aGF0IGFyZSBzaW1wbGVcbiAgICogSlNPTiBPYmplY3RzIGFuZCBwcmltaXRpdmVzLlxuICAgKi9cbiAgY3JlYXRlTGlzdDxUIGV4dGVuZHMgSlNPTlZhbHVlPihwYXRoOiBzdHJpbmcpOiBJT2JzZXJ2YWJsZVVuZG9hYmxlTGlzdDxUPjtcblxuICAvKipcbiAgICogQ3JlYXRlIGEgbWFwIGFuZCBpbnNlcnQgaXQgaW4gdGhlIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSBtYXAuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBtYXAgdGhhdCB3YXMgY3JlYXRlZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgbWFwIGNhbiBvbmx5IHN0b3JlIG9iamVjdHMgdGhhdCBhcmUgc2ltcGxlXG4gICAqIEpTT04gT2JqZWN0cyBhbmQgcHJpbWl0aXZlcy5cbiAgICovXG4gIGNyZWF0ZU1hcChwYXRoOiBzdHJpbmcpOiBJT2JzZXJ2YWJsZUpTT047XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhbiBvcGFxdWUgdmFsdWUgYW5kIGluc2VydCBpdCBpbiB0aGUgZGF0YWJhc2UuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIHZhbHVlLlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgdmFsdWUgdGhhdCB3YXMgY3JlYXRlZC5cbiAgICovXG4gIGNyZWF0ZVZhbHVlKHBhdGg6IHN0cmluZyk6IElPYnNlcnZhYmxlVmFsdWU7XG5cbiAgLyoqXG4gICAqIEdldCBhIHZhbHVlIGF0IGEgcGF0aCwgb3IgYHVuZGVmaW5lZCBpZiBpdCBoYXMgbm90IGJlZW4gc2V0XG4gICAqIFRoYXQgdmFsdWUgbXVzdCBhbHJlYWR5IGhhdmUgYmVlbiBjcmVhdGVkIHVzaW5nIGBjcmVhdGVWYWx1ZWAuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIHZhbHVlLlxuICAgKi9cbiAgZ2V0VmFsdWUocGF0aDogc3RyaW5nKTogSlNPTlZhbHVlIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBTZXQgYSB2YWx1ZSBhdCBhIHBhdGguIFRoYXQgdmFsdWUgbXVzdCBhbHJlYWR5IGhhdmVcbiAgICogYmVlbiBjcmVhdGVkIHVzaW5nIGBjcmVhdGVWYWx1ZWAuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIHZhbHVlLlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWU6IHRoZSBuZXcgdmFsdWUuXG4gICAqL1xuICBzZXRWYWx1ZShwYXRoOiBzdHJpbmcsIHZhbHVlOiBKU09OVmFsdWUpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSB2aWV3IG9udG8gYSBzdWJ0cmVlIG9mIHRoZSBtb2RlbCBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIGJhc2VQYXRoOiB0aGUgcGF0aCBmb3IgdGhlIHJvb3Qgb2YgdGhlIHN1YnRyZWUuXG4gICAqXG4gICAqIEByZXR1cm5zIGFuIGBJTW9kZWxEQmAgd2l0aCBhIHZpZXcgb250byB0aGUgb3JpZ2luYWxcbiAgICogICBgSU1vZGVsREJgLCB3aXRoIGBiYXNlUGF0aGAgcHJlcGVuZGVkIHRvIGFsbCBwYXRocy5cbiAgICovXG4gIHZpZXcoYmFzZVBhdGg6IHN0cmluZyk6IElNb2RlbERCO1xuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgZGF0YWJhc2UuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQ7XG59XG5cbi8qKlxuICogQSBjb25jcmV0ZSBpbXBsZW1lbnRhdGlvbiBvZiBhbiBgSU9ic2VydmFibGVWYWx1ZWAuXG4gKi9cbmV4cG9ydCBjbGFzcyBPYnNlcnZhYmxlVmFsdWUgaW1wbGVtZW50cyBJT2JzZXJ2YWJsZVZhbHVlIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdG9yIGZvciB0aGUgdmFsdWUuXG4gICAqXG4gICAqIEBwYXJhbSBpbml0aWFsVmFsdWU6IHRoZSBzdGFydGluZyB2YWx1ZSBmb3IgdGhlIGBPYnNlcnZhYmxlVmFsdWVgLlxuICAgKi9cbiAgY29uc3RydWN0b3IoaW5pdGlhbFZhbHVlOiBKU09OVmFsdWUgPSBudWxsKSB7XG4gICAgdGhpcy5fdmFsdWUgPSBpbml0aWFsVmFsdWU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIG9ic2VydmFibGUgdHlwZS5cbiAgICovXG4gIGdldCB0eXBlKCk6ICdWYWx1ZScge1xuICAgIHJldHVybiAnVmFsdWUnO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIHZhbHVlIGhhcyBiZWVuIGRpc3Bvc2VkLlxuICAgKi9cbiAgZ2V0IGlzRGlzcG9zZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGNoYW5nZWQgc2lnbmFsLlxuICAgKi9cbiAgZ2V0IGNoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCBPYnNlcnZhYmxlVmFsdWUuSUNoYW5nZWRBcmdzPiB7XG4gICAgcmV0dXJuIHRoaXMuX2NoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBjdXJyZW50IHZhbHVlLCBvciBgdW5kZWZpbmVkYCBpZiBpdCBoYXMgbm90IGJlZW4gc2V0LlxuICAgKi9cbiAgZ2V0KCk6IEpTT05WYWx1ZSB7XG4gICAgcmV0dXJuIHRoaXMuX3ZhbHVlO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgY3VycmVudCB2YWx1ZS5cbiAgICovXG4gIHNldCh2YWx1ZTogSlNPTlZhbHVlKTogdm9pZCB7XG4gICAgY29uc3Qgb2xkVmFsdWUgPSB0aGlzLl92YWx1ZTtcbiAgICBpZiAoSlNPTkV4dC5kZWVwRXF1YWwob2xkVmFsdWUsIHZhbHVlKSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl92YWx1ZSA9IHZhbHVlO1xuICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7XG4gICAgICBvbGRWYWx1ZTogb2xkVmFsdWUsXG4gICAgICBuZXdWYWx1ZTogdmFsdWVcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgdmFsdWUuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gICAgdGhpcy5fdmFsdWUgPSBudWxsO1xuICB9XG5cbiAgcHJpdmF0ZSBfdmFsdWU6IEpTT05WYWx1ZSA9IG51bGw7XG4gIHByaXZhdGUgX2NoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIE9ic2VydmFibGVWYWx1ZS5JQ2hhbmdlZEFyZ3M+KHRoaXMpO1xuICBwcml2YXRlIF9pc0Rpc3Bvc2VkID0gZmFsc2U7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgdGhlIGBPYnNlcnZhYmxlVmFsdWVgIGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgT2JzZXJ2YWJsZVZhbHVlIHtcbiAgLyoqXG4gICAqIFRoZSBjaGFuZ2VkIGFyZ3Mgb2JqZWN0IGVtaXR0ZWQgYnkgdGhlIGBJT2JzZXJ2YWJsZVZhbHVlYC5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBJQ2hhbmdlZEFyZ3Mge1xuICAgIC8qKlxuICAgICAqIFRoZSBvbGQgdmFsdWUuXG4gICAgICovXG4gICAgb2xkVmFsdWU6IEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBuZXcgdmFsdWUuXG4gICAgICovXG4gICAgbmV3VmFsdWU6IEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcbiAgfVxufVxuXG4vKipcbiAqIEEgY29uY3JldGUgaW1wbGVtZW50YXRpb24gb2YgYW4gYElNb2RlbERCYC5cbiAqL1xuZXhwb3J0IGNsYXNzIE1vZGVsREIgaW1wbGVtZW50cyBJTW9kZWxEQiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3RvciBmb3IgdGhlIGBNb2RlbERCYC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IE1vZGVsREIuSUNyZWF0ZU9wdGlvbnMgPSB7fSkge1xuICAgIHRoaXMuX2Jhc2VQYXRoID0gb3B0aW9ucy5iYXNlUGF0aCB8fCAnJztcbiAgICBpZiAob3B0aW9ucy5iYXNlREIpIHtcbiAgICAgIHRoaXMuX2RiID0gb3B0aW9ucy5iYXNlREI7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX2RiID0gbmV3IE9ic2VydmFibGVNYXA8SU9ic2VydmFibGU+KCk7XG4gICAgICB0aGlzLl90b0Rpc3Bvc2UgPSB0cnVlO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgYmFzZSBwYXRoIGZvciB0aGUgYE1vZGVsREJgLiBUaGlzIGlzIHByZXBlbmRlZFxuICAgKiB0byBhbGwgdGhlIHBhdGhzIHRoYXQgYXJlIHBhc3NlZCBpbiB0byB0aGUgbWVtYmVyXG4gICAqIGZ1bmN0aW9ucyBvZiB0aGUgb2JqZWN0LlxuICAgKi9cbiAgZ2V0IGJhc2VQYXRoKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX2Jhc2VQYXRoO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGRhdGFiYXNlIGlzIGRpc3Bvc2VkLlxuICAgKi9cbiAgZ2V0IGlzRGlzcG9zZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgbW9kZWwgaGFzIGJlZW4gcG9wdWxhdGVkIHdpdGhcbiAgICogYW55IG1vZGVsIHZhbHVlcy5cbiAgICovXG4gIHJlYWRvbmx5IGlzUHJlcG9wdWxhdGVkOiBib29sZWFuID0gZmFsc2U7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG1vZGVsIGlzIGNvbGxhYm9yYXRpdmUuXG4gICAqL1xuICByZWFkb25seSBpc0NvbGxhYm9yYXRpdmU6IGJvb2xlYW4gPSBmYWxzZTtcblxuICAvKipcbiAgICogQSBwcm9taXNlIHJlc29sdmVkIHdoZW4gdGhlIG1vZGVsIGlzIGNvbm5lY3RlZFxuICAgKiB0byBpdHMgYmFja2VuZC4gRm9yIHRoZSBpbi1tZW1vcnkgTW9kZWxEQiBpdFxuICAgKiBpcyBpbW1lZGlhdGVseSByZXNvbHZlZC5cbiAgICovXG4gIHJlYWRvbmx5IGNvbm5lY3RlZDogUHJvbWlzZTx2b2lkPiA9IFByb21pc2UucmVzb2x2ZSh2b2lkIDApO1xuXG4gIC8qKlxuICAgKiBHZXQgYSB2YWx1ZSBmb3IgYSBwYXRoLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSBvYmplY3QuXG4gICAqXG4gICAqIEByZXR1cm5zIGFuIGBJT2JzZXJ2YWJsZWAuXG4gICAqL1xuICBnZXQocGF0aDogc3RyaW5nKTogSU9ic2VydmFibGUgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiB0aGlzLl9kYi5nZXQodGhpcy5fcmVzb2x2ZVBhdGgocGF0aCkpO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGBJTW9kZWxEQmAgaGFzIGFuIG9iamVjdCBhdCB0aGlzIHBhdGguXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIG9iamVjdC5cbiAgICpcbiAgICogQHJldHVybnMgYSBib29sZWFuIGZvciB3aGV0aGVyIGFuIG9iamVjdCBpcyBhdCBgcGF0aGAuXG4gICAqL1xuICBoYXMocGF0aDogc3RyaW5nKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2RiLmhhcyh0aGlzLl9yZXNvbHZlUGF0aChwYXRoKSk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgc3RyaW5nIGFuZCBpbnNlcnQgaXQgaW4gdGhlIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSBzdHJpbmcuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBzdHJpbmcgdGhhdCB3YXMgY3JlYXRlZC5cbiAgICovXG4gIGNyZWF0ZVN0cmluZyhwYXRoOiBzdHJpbmcpOiBJT2JzZXJ2YWJsZVN0cmluZyB7XG4gICAgY29uc3Qgc3RyID0gbmV3IE9ic2VydmFibGVTdHJpbmcoKTtcbiAgICB0aGlzLl9kaXNwb3NhYmxlcy5hZGQoc3RyKTtcbiAgICB0aGlzLnNldChwYXRoLCBzdHIpO1xuICAgIHJldHVybiBzdHI7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGFuIHVuZG9hYmxlIGxpc3QgYW5kIGluc2VydCBpdCBpbiB0aGUgZGF0YWJhc2UuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIGxpc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBsaXN0IHRoYXQgd2FzIGNyZWF0ZWQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIGxpc3QgY2FuIG9ubHkgc3RvcmUgb2JqZWN0cyB0aGF0IGFyZSBzaW1wbGVcbiAgICogSlNPTiBPYmplY3RzIGFuZCBwcmltaXRpdmVzLlxuICAgKi9cbiAgY3JlYXRlTGlzdDxUIGV4dGVuZHMgSlNPTlZhbHVlPihwYXRoOiBzdHJpbmcpOiBJT2JzZXJ2YWJsZVVuZG9hYmxlTGlzdDxUPiB7XG4gICAgY29uc3QgdmVjID0gbmV3IE9ic2VydmFibGVVbmRvYWJsZUxpc3Q8VD4oXG4gICAgICBuZXcgT2JzZXJ2YWJsZVVuZG9hYmxlTGlzdC5JZGVudGl0eVNlcmlhbGl6ZXI8VD4oKVxuICAgICk7XG4gICAgdGhpcy5fZGlzcG9zYWJsZXMuYWRkKHZlYyk7XG4gICAgdGhpcy5zZXQocGF0aCwgdmVjKTtcbiAgICByZXR1cm4gdmVjO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG1hcCBhbmQgaW5zZXJ0IGl0IGluIHRoZSBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIHBhdGg6IHRoZSBwYXRoIGZvciB0aGUgbWFwLlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgbWFwIHRoYXQgd2FzIGNyZWF0ZWQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIG1hcCBjYW4gb25seSBzdG9yZSBvYmplY3RzIHRoYXQgYXJlIHNpbXBsZVxuICAgKiBKU09OIE9iamVjdHMgYW5kIHByaW1pdGl2ZXMuXG4gICAqL1xuICBjcmVhdGVNYXAocGF0aDogc3RyaW5nKTogSU9ic2VydmFibGVKU09OIHtcbiAgICBjb25zdCBtYXAgPSBuZXcgT2JzZXJ2YWJsZUpTT04oKTtcbiAgICB0aGlzLl9kaXNwb3NhYmxlcy5hZGQobWFwKTtcbiAgICB0aGlzLnNldChwYXRoLCBtYXApO1xuICAgIHJldHVybiBtYXA7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGFuIG9wYXF1ZSB2YWx1ZSBhbmQgaW5zZXJ0IGl0IGluIHRoZSBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIHBhdGg6IHRoZSBwYXRoIGZvciB0aGUgdmFsdWUuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSB2YWx1ZSB0aGF0IHdhcyBjcmVhdGVkLlxuICAgKi9cbiAgY3JlYXRlVmFsdWUocGF0aDogc3RyaW5nKTogSU9ic2VydmFibGVWYWx1ZSB7XG4gICAgY29uc3QgdmFsID0gbmV3IE9ic2VydmFibGVWYWx1ZSgpO1xuICAgIHRoaXMuX2Rpc3Bvc2FibGVzLmFkZCh2YWwpO1xuICAgIHRoaXMuc2V0KHBhdGgsIHZhbCk7XG4gICAgcmV0dXJuIHZhbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgYSB2YWx1ZSBhdCBhIHBhdGgsIG9yIGB1bmRlZmluZWQgaWYgaXQgaGFzIG5vdCBiZWVuIHNldFxuICAgKiBUaGF0IHZhbHVlIG11c3QgYWxyZWFkeSBoYXZlIGJlZW4gY3JlYXRlZCB1c2luZyBgY3JlYXRlVmFsdWVgLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSB2YWx1ZS5cbiAgICovXG4gIGdldFZhbHVlKHBhdGg6IHN0cmluZyk6IEpTT05WYWx1ZSB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3QgdmFsID0gdGhpcy5nZXQocGF0aCk7XG4gICAgaWYgKCF2YWwgfHwgdmFsLnR5cGUgIT09ICdWYWx1ZScpIHtcbiAgICAgIHRocm93IEVycm9yKCdDYW4gb25seSBjYWxsIGdldFZhbHVlIGZvciBhbiBPYnNlcnZhYmxlVmFsdWUnKTtcbiAgICB9XG4gICAgcmV0dXJuICh2YWwgYXMgT2JzZXJ2YWJsZVZhbHVlKS5nZXQoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgYSB2YWx1ZSBhdCBhIHBhdGguIFRoYXQgdmFsdWUgbXVzdCBhbHJlYWR5IGhhdmVcbiAgICogYmVlbiBjcmVhdGVkIHVzaW5nIGBjcmVhdGVWYWx1ZWAuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIHZhbHVlLlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWU6IHRoZSBuZXcgdmFsdWUuXG4gICAqL1xuICBzZXRWYWx1ZShwYXRoOiBzdHJpbmcsIHZhbHVlOiBKU09OVmFsdWUpOiB2b2lkIHtcbiAgICBjb25zdCB2YWwgPSB0aGlzLmdldChwYXRoKTtcbiAgICBpZiAoIXZhbCB8fCB2YWwudHlwZSAhPT0gJ1ZhbHVlJykge1xuICAgICAgdGhyb3cgRXJyb3IoJ0NhbiBvbmx5IGNhbGwgc2V0VmFsdWUgb24gYW4gT2JzZXJ2YWJsZVZhbHVlJyk7XG4gICAgfVxuICAgICh2YWwgYXMgT2JzZXJ2YWJsZVZhbHVlKS5zZXQodmFsdWUpO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIHZpZXcgb250byBhIHN1YnRyZWUgb2YgdGhlIG1vZGVsIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gYmFzZVBhdGg6IHRoZSBwYXRoIGZvciB0aGUgcm9vdCBvZiB0aGUgc3VidHJlZS5cbiAgICpcbiAgICogQHJldHVybnMgYW4gYElNb2RlbERCYCB3aXRoIGEgdmlldyBvbnRvIHRoZSBvcmlnaW5hbFxuICAgKiAgIGBJTW9kZWxEQmAsIHdpdGggYGJhc2VQYXRoYCBwcmVwZW5kZWQgdG8gYWxsIHBhdGhzLlxuICAgKi9cbiAgdmlldyhiYXNlUGF0aDogc3RyaW5nKTogTW9kZWxEQiB7XG4gICAgY29uc3QgdmlldyA9IG5ldyBNb2RlbERCKHsgYmFzZVBhdGgsIGJhc2VEQjogdGhpcyB9KTtcbiAgICB0aGlzLl9kaXNwb3NhYmxlcy5hZGQodmlldyk7XG4gICAgcmV0dXJuIHZpZXc7XG4gIH1cblxuICAvKipcbiAgICogU2V0IGEgdmFsdWUgYXQgYSBwYXRoLiBOb3QgaW50ZW5kZWQgdG9cbiAgICogYmUgY2FsbGVkIGJ5IHVzZXIgY29kZSwgaW5zdGVhZCB1c2UgdGhlXG4gICAqIGBjcmVhdGUqYCBmYWN0b3J5IG1ldGhvZHMuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCB0byBzZXQgdGhlIHZhbHVlIGF0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWU6IHRoZSB2YWx1ZSB0byBzZXQgYXQgdGhlIHBhdGguXG4gICAqL1xuICBzZXQocGF0aDogc3RyaW5nLCB2YWx1ZTogSU9ic2VydmFibGUpOiB2b2lkIHtcbiAgICB0aGlzLl9kYi5zZXQodGhpcy5fcmVzb2x2ZVBhdGgocGF0aCksIHZhbHVlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgZGF0YWJhc2UuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgaWYgKHRoaXMuX3RvRGlzcG9zZSkge1xuICAgICAgdGhpcy5fZGIuZGlzcG9zZSgpO1xuICAgIH1cbiAgICB0aGlzLl9kaXNwb3NhYmxlcy5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogQ29tcHV0ZSB0aGUgZnVsbHkgcmVzb2x2ZWQgcGF0aCBmb3IgYSBwYXRoIGFyZ3VtZW50LlxuICAgKi9cbiAgcHJpdmF0ZSBfcmVzb2x2ZVBhdGgocGF0aDogc3RyaW5nKTogc3RyaW5nIHtcbiAgICBpZiAodGhpcy5fYmFzZVBhdGgpIHtcbiAgICAgIHBhdGggPSB0aGlzLl9iYXNlUGF0aCArICcuJyArIHBhdGg7XG4gICAgfVxuICAgIHJldHVybiBwYXRoO1xuICB9XG5cbiAgcHJpdmF0ZSBfYmFzZVBhdGg6IHN0cmluZztcbiAgcHJpdmF0ZSBfZGI6IE1vZGVsREIgfCBPYnNlcnZhYmxlTWFwPElPYnNlcnZhYmxlPjtcbiAgcHJpdmF0ZSBfdG9EaXNwb3NlID0gZmFsc2U7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfZGlzcG9zYWJsZXMgPSBuZXcgRGlzcG9zYWJsZVNldCgpO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciB0aGUgYE1vZGVsREJgIGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgTW9kZWxEQiB7XG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBjcmVhdGluZyBhIGBNb2RlbERCYCBvYmplY3QuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDcmVhdGVPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgYmFzZSBwYXRoIHRvIHByZXBlbmQgdG8gYWxsIHRoZSBwYXRoIGFyZ3VtZW50cy5cbiAgICAgKi9cbiAgICBiYXNlUGF0aD86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEEgTW9kZWxEQiB0byB1c2UgYXMgdGhlIHN0b3JlIGZvciB0aGlzXG4gICAgICogTW9kZWxEQi4gSWYgbm9uZSBpcyBnaXZlbiwgaXQgdXNlcyBpdHMgb3duIHN0b3JlLlxuICAgICAqL1xuICAgIGJhc2VEQj86IE1vZGVsREI7XG4gIH1cblxuICAvKipcbiAgICogQSBmYWN0b3J5IGludGVyZmFjZSBmb3IgY3JlYXRpbmcgYElNb2RlbERCYCBvYmplY3RzLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJRmFjdG9yeSB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IGBJTW9kZWxEQmAgaW5zdGFuY2UuXG4gICAgICovXG4gICAgY3JlYXRlTmV3KHBhdGg6IHN0cmluZyk6IElNb2RlbERCO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7XG4gIEpTT05FeHQsXG4gIEpTT05PYmplY3QsXG4gIFBhcnRpYWxKU09OT2JqZWN0LFxuICBSZWFkb25seVBhcnRpYWxKU09OVmFsdWVcbn0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IElPYnNlcnZhYmxlTWFwLCBPYnNlcnZhYmxlTWFwIH0gZnJvbSAnLi9vYnNlcnZhYmxlbWFwJztcblxuLyoqXG4gKiBBbiBvYnNlcnZhYmxlIEpTT04gdmFsdWUuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU9ic2VydmFibGVKU09OXG4gIGV4dGVuZHMgSU9ic2VydmFibGVNYXA8UmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlIHwgdW5kZWZpbmVkPiB7XG4gIC8qKlxuICAgKiBTZXJpYWxpemUgdGhlIG1vZGVsIHRvIEpTT04uXG4gICAqL1xuICB0b0pTT04oKTogUGFydGlhbEpTT05PYmplY3Q7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgSU9ic2VydmFibGVKU09OIHJlbGF0ZWQgaW50ZXJmYWNlcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJT2JzZXJ2YWJsZUpTT04ge1xuICAvKipcbiAgICogQSB0eXBlIGFsaWFzIGZvciBvYnNlcnZhYmxlIEpTT04gY2hhbmdlZCBhcmdzLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgSUNoYW5nZWRBcmdzID0gSU9ic2VydmFibGVNYXAuSUNoYW5nZWRBcmdzPFxuICAgIFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZVxuICA+O1xufVxuXG4vKipcbiAqIEEgY29uY3JldGUgT2JzZXJ2YWJsZSBtYXAgZm9yIEpTT04gZGF0YS5cbiAqL1xuZXhwb3J0IGNsYXNzIE9ic2VydmFibGVKU09OIGV4dGVuZHMgT2JzZXJ2YWJsZU1hcDxSZWFkb25seVBhcnRpYWxKU09OVmFsdWU+IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBvYnNlcnZhYmxlIEpTT04gb2JqZWN0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogT2JzZXJ2YWJsZUpTT04uSU9wdGlvbnMgPSB7fSkge1xuICAgIHN1cGVyKHtcbiAgICAgIGl0ZW1DbXA6IEpTT05FeHQuZGVlcEVxdWFsLFxuICAgICAgdmFsdWVzOiBvcHRpb25zLnZhbHVlc1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFNlcmlhbGl6ZSB0aGUgbW9kZWwgdG8gSlNPTi5cbiAgICovXG4gIHRvSlNPTigpOiBQYXJ0aWFsSlNPTk9iamVjdCB7XG4gICAgY29uc3Qgb3V0OiBQYXJ0aWFsSlNPTk9iamVjdCA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG4gICAgY29uc3Qga2V5cyA9IHRoaXMua2V5cygpO1xuXG4gICAgZm9yIChjb25zdCBrZXkgb2Yga2V5cykge1xuICAgICAgY29uc3QgdmFsdWUgPSB0aGlzLmdldChrZXkpO1xuXG4gICAgICBpZiAodmFsdWUgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICBvdXRba2V5XSA9IEpTT05FeHQuZGVlcENvcHkodmFsdWUpIGFzIFBhcnRpYWxKU09OT2JqZWN0O1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gb3V0O1xuICB9XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgT2JzZXJ2YWJsZUpTT04gc3RhdGljIGRhdGEuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgT2JzZXJ2YWJsZUpTT04ge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlIHRvIGluaXRpYWxpemUgYW4gb2JzZXJ2YWJsZSBKU09OIG9iamVjdC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBvcHRpb25hbCBpbml0aWFsIHZhbHVlIGZvciB0aGUgb2JqZWN0LlxuICAgICAqL1xuICAgIHZhbHVlcz86IEpTT05PYmplY3Q7XG4gIH1cblxuICAvKipcbiAgICogQW4gb2JzZXJ2YWJsZSBKU09OIGNoYW5nZSBtZXNzYWdlLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIENoYW5nZU1lc3NhZ2UgZXh0ZW5kcyBNZXNzYWdlIHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgbWV0YWRhdGEgY2hhbmdlZCBtZXNzYWdlLlxuICAgICAqL1xuICAgIGNvbnN0cnVjdG9yKHR5cGU6IHN0cmluZywgYXJnczogSU9ic2VydmFibGVKU09OLklDaGFuZ2VkQXJncykge1xuICAgICAgc3VwZXIodHlwZSk7XG4gICAgICB0aGlzLmFyZ3MgPSBhcmdzO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBhcmd1bWVudHMgb2YgdGhlIGNoYW5nZS5cbiAgICAgKi9cbiAgICByZWFkb25seSBhcmdzOiBJT2JzZXJ2YWJsZUpTT04uSUNoYW5nZWRBcmdzO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7XG4gIEFycmF5RXh0LFxuICBBcnJheUl0ZXJhdG9yLFxuICBlYWNoLFxuICBJSXRlcmF0b3IsXG4gIEl0ZXJhYmxlT3JBcnJheUxpa2UsXG4gIHRvQXJyYXlcbn0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuXG4vKipcbiAqIEEgbGlzdCB3aGljaCBjYW4gYmUgb2JzZXJ2ZWQgZm9yIGNoYW5nZXMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU9ic2VydmFibGVMaXN0PFQ+IGV4dGVuZHMgSURpc3Bvc2FibGUge1xuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBsaXN0IGhhcyBjaGFuZ2VkLlxuICAgKi9cbiAgcmVhZG9ubHkgY2hhbmdlZDogSVNpZ25hbDx0aGlzLCBJT2JzZXJ2YWJsZUxpc3QuSUNoYW5nZWRBcmdzPFQ+PjtcblxuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhpcyBvYmplY3QuXG4gICAqL1xuICByZWFkb25seSB0eXBlOiAnTGlzdCc7XG5cbiAgLyoqXG4gICAqIFRoZSBsZW5ndGggb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBpcyBhIHJlYWQtb25seSBwcm9wZXJ0eS5cbiAgICovXG4gIGxlbmd0aDogbnVtYmVyO1xuXG4gIC8qKlxuICAgKiBDcmVhdGUgYW4gaXRlcmF0b3Igb3ZlciB0aGUgdmFsdWVzIGluIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBBIG5ldyBpdGVyYXRvciBzdGFydGluZyBhdCB0aGUgZnJvbnQgb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBDb25zdGFudC5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBObyBjaGFuZ2VzLlxuICAgKi9cbiAgaXRlcigpOiBJSXRlcmF0b3I8VD47XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhbGwgdmFsdWVzIGZyb20gdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBMaW5lYXIuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogQWxsIGN1cnJlbnQgaXRlcmF0b3JzIGFyZSBpbnZhbGlkYXRlZC5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgdmFsdWUgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIHBvc2l0aXZlIGludGVnZXIgaW5kZXggb2YgaW50ZXJlc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSB2YWx1ZSBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBbiBgaW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbCBvciBvdXQgb2YgcmFuZ2UuXG4gICAqL1xuICBnZXQoaW5kZXg6IG51bWJlcik6IFQ7XG5cbiAgLyoqXG4gICAqIEluc2VydCBhIHZhbHVlIGludG8gdGhlIGxpc3QgYXQgYSBzcGVjaWZpYyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIGluZGV4IGF0IHdoaWNoIHRvIGluc2VydCB0aGUgdmFsdWUuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSB0byBzZXQgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIExpbmVhci5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBObyBjaGFuZ2VzLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBgaW5kZXhgIHdpbGwgYmUgY2xhbXBlZCB0byB0aGUgYm91bmRzIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBbiBgaW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbC5cbiAgICovXG4gIGluc2VydChpbmRleDogbnVtYmVyLCB2YWx1ZTogVCk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIEluc2VydCBhIHNldCBvZiBpdGVtcyBpbnRvIHRoZSBsaXN0IGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqXG4gICAqIEBwYXJhbSBpbmRleCAtIFRoZSBpbmRleCBhdCB3aGljaCB0byBpbnNlcnQgdGhlIHZhbHVlcy5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlcyAtIFRoZSB2YWx1ZXMgdG8gaW5zZXJ0IGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eS5cbiAgICogTGluZWFyLlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIE5vIGNoYW5nZXMuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIGBpbmRleGAgd2lsbCBiZSBjbGFtcGVkIHRvIHRoZSBib3VuZHMgb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgVW5kZWZpbmVkIEJlaGF2aW9yLlxuICAgKiBBbiBgaW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbC5cbiAgICovXG4gIGluc2VydEFsbChpbmRleDogbnVtYmVyLCB2YWx1ZXM6IEl0ZXJhYmxlT3JBcnJheUxpa2U8VD4pOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBNb3ZlIGEgdmFsdWUgZnJvbSBvbmUgaW5kZXggdG8gYW5vdGhlci5cbiAgICpcbiAgICogQHBhcm0gZnJvbUluZGV4IC0gVGhlIGluZGV4IG9mIHRoZSBlbGVtZW50IHRvIG1vdmUuXG4gICAqXG4gICAqIEBwYXJhbSB0b0luZGV4IC0gVGhlIGluZGV4IHRvIG1vdmUgdGhlIGVsZW1lbnQgdG8uXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBDb25zdGFudC5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBJdGVyYXRvcnMgcG9pbnRpbmcgYXQgdGhlIGxlc3NlciBvZiB0aGUgYGZyb21JbmRleGAgYW5kIHRoZSBgdG9JbmRleGBcbiAgICogYW5kIGJleW9uZCBhcmUgaW52YWxpZGF0ZWQuXG4gICAqXG4gICAqICMjIyMgVW5kZWZpbmVkIEJlaGF2aW9yXG4gICAqIEEgYGZyb21JbmRleGAgb3IgYSBgdG9JbmRleGAgd2hpY2ggaXMgbm9uLWludGVncmFsLlxuICAgKi9cbiAgbW92ZShmcm9tSW5kZXg6IG51bWJlciwgdG9JbmRleDogbnVtYmVyKTogdm9pZDtcblxuICAvKipcbiAgICogQWRkIGEgdmFsdWUgdG8gdGhlIGJhY2sgb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSB0byBhZGQgdG8gdGhlIGJhY2sgb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBuZXcgbGVuZ3RoIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogQ29uc3RhbnQuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogTm8gY2hhbmdlcy5cbiAgICovXG4gIHB1c2godmFsdWU6IFQpOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFB1c2ggYSBzZXQgb2YgdmFsdWVzIHRvIHRoZSBiYWNrIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWVzIC0gQW4gaXRlcmFibGUgb3IgYXJyYXktbGlrZSBzZXQgb2YgdmFsdWVzIHRvIGFkZC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIG5ldyBsZW5ndGggb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBMaW5lYXIuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogTm8gY2hhbmdlcy5cbiAgICovXG4gIHB1c2hBbGwodmFsdWVzOiBJdGVyYWJsZU9yQXJyYXlMaWtlPFQ+KTogbnVtYmVyO1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgYW5kIHJldHVybiB0aGUgdmFsdWUgYXQgYSBzcGVjaWZpYyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIGluZGV4IG9mIHRoZSB2YWx1ZSBvZiBpbnRlcmVzdC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIHZhbHVlIGF0IHRoZSBzcGVjaWZpZWQgaW5kZXgsIG9yIGB1bmRlZmluZWRgIGlmIHRoZVxuICAgKiAgIGluZGV4IGlzIG91dCBvZiByYW5nZS5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIENvbnN0YW50LlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIEl0ZXJhdG9ycyBwb2ludGluZyBhdCB0aGUgcmVtb3ZlZCB2YWx1ZSBhbmQgYmV5b25kIGFyZSBpbnZhbGlkYXRlZC5cbiAgICpcbiAgICogIyMjIyBVbmRlZmluZWQgQmVoYXZpb3JcbiAgICogQW4gYGluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwuXG4gICAqL1xuICByZW1vdmUoaW5kZXg6IG51bWJlcik6IFQgfCB1bmRlZmluZWQ7XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhIHJhbmdlIG9mIGl0ZW1zIGZyb20gdGhlIGxpc3QuXG4gICAqXG4gICAqIEBwYXJhbSBzdGFydEluZGV4IC0gVGhlIHN0YXJ0IGluZGV4IG9mIHRoZSByYW5nZSB0byByZW1vdmUgKGluY2x1c2l2ZSkuXG4gICAqXG4gICAqIEBwYXJhbSBlbmRJbmRleCAtIFRoZSBlbmQgaW5kZXggb2YgdGhlIHJhbmdlIHRvIHJlbW92ZSAoZXhjbHVzaXZlKS5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIG5ldyBsZW5ndGggb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBMaW5lYXIuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogSXRlcmF0b3JzIHBvaW50aW5nIHRvIHRoZSBmaXJzdCByZW1vdmVkIHZhbHVlIGFuZCBiZXlvbmQgYXJlIGludmFsaWQuXG4gICAqXG4gICAqICMjIyMgVW5kZWZpbmVkIEJlaGF2aW9yXG4gICAqIEEgYHN0YXJ0SW5kZXhgIG9yIGBlbmRJbmRleGAgd2hpY2ggaXMgbm9uLWludGVncmFsLlxuICAgKi9cbiAgcmVtb3ZlUmFuZ2Uoc3RhcnRJbmRleDogbnVtYmVyLCBlbmRJbmRleDogbnVtYmVyKTogbnVtYmVyO1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgdGhlIGZpcnN0IG9jY3VycmVuY2Ugb2YgYSB2YWx1ZSBmcm9tIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgb2YgaW50ZXJlc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBpbmRleCBvZiB0aGUgcmVtb3ZlZCB2YWx1ZSwgb3IgYC0xYCBpZiB0aGUgdmFsdWVcbiAgICogICBpcyBub3QgY29udGFpbmVkIGluIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogTGluZWFyLlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIEl0ZXJhdG9ycyBwb2ludGluZyBhdCB0aGUgcmVtb3ZlZCB2YWx1ZSBhbmQgYmV5b25kIGFyZSBpbnZhbGlkYXRlZC5cbiAgICovXG4gIHJlbW92ZVZhbHVlKHZhbHVlOiBUKTogbnVtYmVyO1xuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHZhbHVlIGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqXG4gICAqIEBwYXJhbSBpbmRleCAtIFRoZSBwb3NpdGl2ZSBpbnRlZ2VyIGluZGV4IG9mIGludGVyZXN0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgdG8gc2V0IGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBDb25zdGFudC5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBObyBjaGFuZ2VzLlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBbiBgaW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbCBvciBvdXQgb2YgcmFuZ2UuXG4gICAqL1xuICBzZXQoaW5kZXg6IG51bWJlciwgdmFsdWU6IFQpOiB2b2lkO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIElPYnNlcnZhYmxlTGlzdCByZWxhdGVkIGludGVyZmFjZXMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSU9ic2VydmFibGVMaXN0IHtcbiAgLyoqXG4gICAqIFRoZSBjaGFuZ2UgdHlwZXMgd2hpY2ggb2NjdXIgb24gYW4gb2JzZXJ2YWJsZSBsaXN0LlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgQ2hhbmdlVHlwZSA9XG4gICAgLyoqXG4gICAgICogSXRlbShzKSB3ZXJlIGFkZGVkIHRvIHRoZSBsaXN0LlxuICAgICAqL1xuICAgIHwgJ2FkZCdcblxuICAgIC8qKlxuICAgICAqIEFuIGl0ZW0gd2FzIG1vdmVkIHdpdGhpbiB0aGUgbGlzdC5cbiAgICAgKi9cbiAgICB8ICdtb3ZlJ1xuXG4gICAgLyoqXG4gICAgICogSXRlbShzKSB3ZXJlIHJlbW92ZWQgZnJvbSB0aGUgbGlzdC5cbiAgICAgKi9cbiAgICB8ICdyZW1vdmUnXG5cbiAgICAvKipcbiAgICAgKiBBbiBpdGVtIHdhcyBzZXQgaW4gdGhlIGxpc3QuXG4gICAgICovXG4gICAgfCAnc2V0JztcblxuICAvKipcbiAgICogVGhlIGNoYW5nZWQgYXJncyBvYmplY3Qgd2hpY2ggaXMgZW1pdHRlZCBieSBhbiBvYnNlcnZhYmxlIGxpc3QuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDaGFuZ2VkQXJnczxUPiB7XG4gICAgLyoqXG4gICAgICogVGhlIHR5cGUgb2YgY2hhbmdlIHVuZGVyZ29uZSBieSB0aGUgdmVjdG9yLlxuICAgICAqL1xuICAgIHR5cGU6IENoYW5nZVR5cGU7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmV3IGluZGV4IGFzc29jaWF0ZWQgd2l0aCB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIG5ld0luZGV4OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmV3IHZhbHVlcyBhc3NvY2lhdGVkIHdpdGggdGhlIGNoYW5nZS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGUgdmFsdWVzIHdpbGwgYmUgY29udGlndW91cyBzdGFydGluZyBhdCB0aGUgYG5ld0luZGV4YC5cbiAgICAgKi9cbiAgICBuZXdWYWx1ZXM6IFRbXTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBvbGQgaW5kZXggYXNzb2NpYXRlZCB3aXRoIHRoZSBjaGFuZ2UuXG4gICAgICovXG4gICAgb2xkSW5kZXg6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBvbGQgdmFsdWVzIGFzc29jaWF0ZWQgd2l0aCB0aGUgY2hhbmdlLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoZSB2YWx1ZXMgd2lsbCBiZSBjb250aWd1b3VzIHN0YXJ0aW5nIGF0IHRoZSBgb2xkSW5kZXhgLlxuICAgICAqL1xuICAgIG9sZFZhbHVlczogVFtdO1xuICB9XG59XG5cbi8qKlxuICogQSBjb25jcmV0ZSBpbXBsZW1lbnRhdGlvbiBvZiBbW0lPYnNlcnZhYmxlTGlzdF1dLlxuICovXG5leHBvcnQgY2xhc3MgT2JzZXJ2YWJsZUxpc3Q8VD4gaW1wbGVtZW50cyBJT2JzZXJ2YWJsZUxpc3Q8VD4ge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IG9ic2VydmFibGUgbWFwLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogT2JzZXJ2YWJsZUxpc3QuSU9wdGlvbnM8VD4gPSB7fSkge1xuICAgIGlmIChvcHRpb25zLnZhbHVlcyAhPT0gdm9pZCAwKSB7XG4gICAgICBlYWNoKG9wdGlvbnMudmFsdWVzLCB2YWx1ZSA9PiB7XG4gICAgICAgIHRoaXMuX2FycmF5LnB1c2godmFsdWUpO1xuICAgICAgfSk7XG4gICAgfVxuICAgIHRoaXMuX2l0ZW1DbXAgPSBvcHRpb25zLml0ZW1DbXAgfHwgUHJpdmF0ZS5pdGVtQ21wO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSB0eXBlIG9mIHRoaXMgb2JqZWN0LlxuICAgKi9cbiAgZ2V0IHR5cGUoKTogJ0xpc3QnIHtcbiAgICByZXR1cm4gJ0xpc3QnO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbGlzdCBoYXMgY2hhbmdlZC5cbiAgICovXG4gIGdldCBjaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgSU9ic2VydmFibGVMaXN0LklDaGFuZ2VkQXJnczxUPj4ge1xuICAgIHJldHVybiB0aGlzLl9jaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBsZW5ndGggb2YgdGhlIGxpc3QuXG4gICAqL1xuICBnZXQgbGVuZ3RoKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX2FycmF5Lmxlbmd0aDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUZXN0IHdoZXRoZXIgdGhlIGxpc3QgaGFzIGJlZW4gZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgbGlzdC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX2lzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgU2lnbmFsLmNsZWFyRGF0YSh0aGlzKTtcbiAgICB0aGlzLmNsZWFyKCk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGFuIGl0ZXJhdG9yIG92ZXIgdGhlIHZhbHVlcyBpbiB0aGUgbGlzdC5cbiAgICpcbiAgICogQHJldHVybnMgQSBuZXcgaXRlcmF0b3Igc3RhcnRpbmcgYXQgdGhlIGZyb250IG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogQ29uc3RhbnQuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogTm8gY2hhbmdlcy5cbiAgICovXG4gIGl0ZXIoKTogSUl0ZXJhdG9yPFQ+IHtcbiAgICByZXR1cm4gbmV3IEFycmF5SXRlcmF0b3IodGhpcy5fYXJyYXkpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgdmFsdWUgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIHBvc2l0aXZlIGludGVnZXIgaW5kZXggb2YgaW50ZXJlc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSB2YWx1ZSBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBbiBgaW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbCBvciBvdXQgb2YgcmFuZ2UuXG4gICAqL1xuICBnZXQoaW5kZXg6IG51bWJlcik6IFQge1xuICAgIHJldHVybiB0aGlzLl9hcnJheVtpbmRleF07XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSB2YWx1ZSBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKlxuICAgKiBAcGFyYW0gaW5kZXggLSBUaGUgcG9zaXRpdmUgaW50ZWdlciBpbmRleCBvZiBpbnRlcmVzdC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlIC0gVGhlIHZhbHVlIHRvIHNldCBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogQ29uc3RhbnQuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogTm8gY2hhbmdlcy5cbiAgICpcbiAgICogIyMjIyBVbmRlZmluZWQgQmVoYXZpb3JcbiAgICogQW4gYGluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwgb3Igb3V0IG9mIHJhbmdlLlxuICAgKi9cbiAgc2V0KGluZGV4OiBudW1iZXIsIHZhbHVlOiBUKTogdm9pZCB7XG4gICAgY29uc3Qgb2xkVmFsdWUgPSB0aGlzLl9hcnJheVtpbmRleF07XG4gICAgaWYgKHZhbHVlID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignQ2Fubm90IHNldCBhbiB1bmRlZmluZWQgaXRlbScpO1xuICAgIH1cbiAgICAvLyBCYWlsIGlmIHRoZSB2YWx1ZSBkb2VzIG5vdCBjaGFuZ2UuXG4gICAgY29uc3QgaXRlbUNtcCA9IHRoaXMuX2l0ZW1DbXA7XG4gICAgaWYgKGl0ZW1DbXAob2xkVmFsdWUsIHZhbHVlKSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9hcnJheVtpbmRleF0gPSB2YWx1ZTtcbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ3NldCcsXG4gICAgICBvbGRJbmRleDogaW5kZXgsXG4gICAgICBuZXdJbmRleDogaW5kZXgsXG4gICAgICBvbGRWYWx1ZXM6IFtvbGRWYWx1ZV0sXG4gICAgICBuZXdWYWx1ZXM6IFt2YWx1ZV1cbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSB2YWx1ZSB0byB0aGUgZW5kIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgdG8gYWRkIHRvIHRoZSBlbmQgb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBuZXcgbGVuZ3RoIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogQ29uc3RhbnQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogQnkgY29udmVudGlvbiwgdGhlIG9sZEluZGV4IGlzIHNldCB0byAtMSB0byBpbmRpY2F0ZVxuICAgKiBhbiBwdXNoIG9wZXJhdGlvbi5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBObyBjaGFuZ2VzLlxuICAgKi9cbiAgcHVzaCh2YWx1ZTogVCk6IG51bWJlciB7XG4gICAgY29uc3QgbnVtID0gdGhpcy5fYXJyYXkucHVzaCh2YWx1ZSk7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdhZGQnLFxuICAgICAgb2xkSW5kZXg6IC0xLFxuICAgICAgbmV3SW5kZXg6IHRoaXMubGVuZ3RoIC0gMSxcbiAgICAgIG9sZFZhbHVlczogW10sXG4gICAgICBuZXdWYWx1ZXM6IFt2YWx1ZV1cbiAgICB9KTtcbiAgICByZXR1cm4gbnVtO1xuICB9XG5cbiAgLyoqXG4gICAqIEluc2VydCBhIHZhbHVlIGludG8gdGhlIGxpc3QgYXQgYSBzcGVjaWZpYyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIGluZGV4IGF0IHdoaWNoIHRvIGluc2VydCB0aGUgdmFsdWUuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSB0byBzZXQgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIExpbmVhci5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBObyBjaGFuZ2VzLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBgaW5kZXhgIHdpbGwgYmUgY2xhbXBlZCB0byB0aGUgYm91bmRzIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiBCeSBjb252ZW50aW9uLCB0aGUgb2xkSW5kZXggaXMgc2V0IHRvIC0yIHRvIGluZGljYXRlXG4gICAqIGFuIGluc2VydCBvcGVyYXRpb24uXG4gICAqXG4gICAqIFRoZSB2YWx1ZSAtMiBhcyBvbGRJbmRleCBjYW4gYmUgdXNlZCB0byBkaXN0aW5ndWlzaCBmcm9tIHRoZSBwdXNoXG4gICAqIG1ldGhvZCB3aGljaCB3aWxsIHVzZSBhIHZhbHVlIC0xLlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBbiBgaW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbC5cbiAgICovXG4gIGluc2VydChpbmRleDogbnVtYmVyLCB2YWx1ZTogVCk6IHZvaWQge1xuICAgIGlmIChpbmRleCA9PT0gdGhpcy5fYXJyYXkubGVuZ3RoKSB7XG4gICAgICB0aGlzLl9hcnJheS5wdXNoKHZhbHVlKTtcbiAgICB9IGVsc2Uge1xuICAgICAgQXJyYXlFeHQuaW5zZXJ0KHRoaXMuX2FycmF5LCBpbmRleCwgdmFsdWUpO1xuICAgIH1cbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ2FkZCcsXG4gICAgICBvbGRJbmRleDogLTIsXG4gICAgICBuZXdJbmRleDogaW5kZXgsXG4gICAgICBvbGRWYWx1ZXM6IFtdLFxuICAgICAgbmV3VmFsdWVzOiBbdmFsdWVdXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIHRoZSBmaXJzdCBvY2N1cnJlbmNlIG9mIGEgdmFsdWUgZnJvbSB0aGUgbGlzdC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlIC0gVGhlIHZhbHVlIG9mIGludGVyZXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgaW5kZXggb2YgdGhlIHJlbW92ZWQgdmFsdWUsIG9yIGAtMWAgaWYgdGhlIHZhbHVlXG4gICAqICAgaXMgbm90IGNvbnRhaW5lZCBpbiB0aGUgbGlzdC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIExpbmVhci5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBJdGVyYXRvcnMgcG9pbnRpbmcgYXQgdGhlIHJlbW92ZWQgdmFsdWUgYW5kIGJleW9uZCBhcmUgaW52YWxpZGF0ZWQuXG4gICAqL1xuICByZW1vdmVWYWx1ZSh2YWx1ZTogVCk6IG51bWJlciB7XG4gICAgY29uc3QgaXRlbUNtcCA9IHRoaXMuX2l0ZW1DbXA7XG4gICAgY29uc3QgaW5kZXggPSBBcnJheUV4dC5maW5kRmlyc3RJbmRleCh0aGlzLl9hcnJheSwgaXRlbSA9PiB7XG4gICAgICByZXR1cm4gaXRlbUNtcChpdGVtLCB2YWx1ZSk7XG4gICAgfSk7XG4gICAgdGhpcy5yZW1vdmUoaW5kZXgpO1xuICAgIHJldHVybiBpbmRleDtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYW5kIHJldHVybiB0aGUgdmFsdWUgYXQgYSBzcGVjaWZpYyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIGluZGV4IG9mIHRoZSB2YWx1ZSBvZiBpbnRlcmVzdC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIHZhbHVlIGF0IHRoZSBzcGVjaWZpZWQgaW5kZXgsIG9yIGB1bmRlZmluZWRgIGlmIHRoZVxuICAgKiAgIGluZGV4IGlzIG91dCBvZiByYW5nZS5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIENvbnN0YW50LlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIEl0ZXJhdG9ycyBwb2ludGluZyBhdCB0aGUgcmVtb3ZlZCB2YWx1ZSBhbmQgYmV5b25kIGFyZSBpbnZhbGlkYXRlZC5cbiAgICpcbiAgICogIyMjIyBVbmRlZmluZWQgQmVoYXZpb3JcbiAgICogQW4gYGluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwuXG4gICAqL1xuICByZW1vdmUoaW5kZXg6IG51bWJlcik6IFQgfCB1bmRlZmluZWQge1xuICAgIGNvbnN0IHZhbHVlID0gQXJyYXlFeHQucmVtb3ZlQXQodGhpcy5fYXJyYXksIGluZGV4KTtcbiAgICBpZiAodmFsdWUgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ3JlbW92ZScsXG4gICAgICBvbGRJbmRleDogaW5kZXgsXG4gICAgICBuZXdJbmRleDogLTEsXG4gICAgICBuZXdWYWx1ZXM6IFtdLFxuICAgICAgb2xkVmFsdWVzOiBbdmFsdWVdXG4gICAgfSk7XG4gICAgcmV0dXJuIHZhbHVlO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhbGwgdmFsdWVzIGZyb20gdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBMaW5lYXIuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogQWxsIGN1cnJlbnQgaXRlcmF0b3JzIGFyZSBpbnZhbGlkYXRlZC5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQge1xuICAgIGNvbnN0IGNvcHkgPSB0aGlzLl9hcnJheS5zbGljZSgpO1xuICAgIHRoaXMuX2FycmF5Lmxlbmd0aCA9IDA7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdyZW1vdmUnLFxuICAgICAgb2xkSW5kZXg6IDAsXG4gICAgICBuZXdJbmRleDogMCxcbiAgICAgIG5ld1ZhbHVlczogW10sXG4gICAgICBvbGRWYWx1ZXM6IGNvcHlcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBNb3ZlIGEgdmFsdWUgZnJvbSBvbmUgaW5kZXggdG8gYW5vdGhlci5cbiAgICpcbiAgICogQHBhcm0gZnJvbUluZGV4IC0gVGhlIGluZGV4IG9mIHRoZSBlbGVtZW50IHRvIG1vdmUuXG4gICAqXG4gICAqIEBwYXJhbSB0b0luZGV4IC0gVGhlIGluZGV4IHRvIG1vdmUgdGhlIGVsZW1lbnQgdG8uXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBDb25zdGFudC5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBJdGVyYXRvcnMgcG9pbnRpbmcgYXQgdGhlIGxlc3NlciBvZiB0aGUgYGZyb21JbmRleGAgYW5kIHRoZSBgdG9JbmRleGBcbiAgICogYW5kIGJleW9uZCBhcmUgaW52YWxpZGF0ZWQuXG4gICAqXG4gICAqICMjIyMgVW5kZWZpbmVkIEJlaGF2aW9yXG4gICAqIEEgYGZyb21JbmRleGAgb3IgYSBgdG9JbmRleGAgd2hpY2ggaXMgbm9uLWludGVncmFsLlxuICAgKi9cbiAgbW92ZShmcm9tSW5kZXg6IG51bWJlciwgdG9JbmRleDogbnVtYmVyKTogdm9pZCB7XG4gICAgaWYgKHRoaXMubGVuZ3RoIDw9IDEgfHwgZnJvbUluZGV4ID09PSB0b0luZGV4KSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IHZhbHVlcyA9IFt0aGlzLl9hcnJheVtmcm9tSW5kZXhdXTtcbiAgICBBcnJheUV4dC5tb3ZlKHRoaXMuX2FycmF5LCBmcm9tSW5kZXgsIHRvSW5kZXgpO1xuICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7XG4gICAgICB0eXBlOiAnbW92ZScsXG4gICAgICBvbGRJbmRleDogZnJvbUluZGV4LFxuICAgICAgbmV3SW5kZXg6IHRvSW5kZXgsXG4gICAgICBvbGRWYWx1ZXM6IHZhbHVlcyxcbiAgICAgIG5ld1ZhbHVlczogdmFsdWVzXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogUHVzaCBhIHNldCBvZiB2YWx1ZXMgdG8gdGhlIGJhY2sgb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZXMgLSBBbiBpdGVyYWJsZSBvciBhcnJheS1saWtlIHNldCBvZiB2YWx1ZXMgdG8gYWRkLlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgbmV3IGxlbmd0aCBvZiB0aGUgbGlzdC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIExpbmVhci5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBCeSBjb252ZW50aW9uLCB0aGUgb2xkSW5kZXggaXMgc2V0IHRvIC0xIHRvIGluZGljYXRlXG4gICAqIGFuIHB1c2ggb3BlcmF0aW9uLlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIE5vIGNoYW5nZXMuXG4gICAqL1xuICBwdXNoQWxsKHZhbHVlczogSXRlcmFibGVPckFycmF5TGlrZTxUPik6IG51bWJlciB7XG4gICAgY29uc3QgbmV3SW5kZXggPSB0aGlzLmxlbmd0aDtcbiAgICBlYWNoKHZhbHVlcywgdmFsdWUgPT4ge1xuICAgICAgdGhpcy5fYXJyYXkucHVzaCh2YWx1ZSk7XG4gICAgfSk7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdhZGQnLFxuICAgICAgb2xkSW5kZXg6IC0xLFxuICAgICAgbmV3SW5kZXgsXG4gICAgICBvbGRWYWx1ZXM6IFtdLFxuICAgICAgbmV3VmFsdWVzOiB0b0FycmF5KHZhbHVlcylcbiAgICB9KTtcbiAgICByZXR1cm4gdGhpcy5sZW5ndGg7XG4gIH1cblxuICAvKipcbiAgICogSW5zZXJ0IGEgc2V0IG9mIGl0ZW1zIGludG8gdGhlIGxpc3QgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIGluZGV4IGF0IHdoaWNoIHRvIGluc2VydCB0aGUgdmFsdWVzLlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWVzIC0gVGhlIHZhbHVlcyB0byBpbnNlcnQgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5LlxuICAgKiBMaW5lYXIuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogTm8gY2hhbmdlcy5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgYGluZGV4YCB3aWxsIGJlIGNsYW1wZWQgdG8gdGhlIGJvdW5kcyBvZiB0aGUgbGlzdC5cbiAgICogQnkgY29udmVudGlvbiwgdGhlIG9sZEluZGV4IGlzIHNldCB0byAtMiB0byBpbmRpY2F0ZVxuICAgKiBhbiBpbnNlcnQgb3BlcmF0aW9uLlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvci5cbiAgICogQW4gYGluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwuXG4gICAqL1xuICBpbnNlcnRBbGwoaW5kZXg6IG51bWJlciwgdmFsdWVzOiBJdGVyYWJsZU9yQXJyYXlMaWtlPFQ+KTogdm9pZCB7XG4gICAgY29uc3QgbmV3SW5kZXggPSBpbmRleDtcbiAgICBlYWNoKHZhbHVlcywgdmFsdWUgPT4ge1xuICAgICAgQXJyYXlFeHQuaW5zZXJ0KHRoaXMuX2FycmF5LCBpbmRleCsrLCB2YWx1ZSk7XG4gICAgfSk7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdhZGQnLFxuICAgICAgb2xkSW5kZXg6IC0yLFxuICAgICAgbmV3SW5kZXgsXG4gICAgICBvbGRWYWx1ZXM6IFtdLFxuICAgICAgbmV3VmFsdWVzOiB0b0FycmF5KHZhbHVlcylcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSByYW5nZSBvZiBpdGVtcyBmcm9tIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gc3RhcnRJbmRleCAtIFRoZSBzdGFydCBpbmRleCBvZiB0aGUgcmFuZ2UgdG8gcmVtb3ZlIChpbmNsdXNpdmUpLlxuICAgKlxuICAgKiBAcGFyYW0gZW5kSW5kZXggLSBUaGUgZW5kIGluZGV4IG9mIHRoZSByYW5nZSB0byByZW1vdmUgKGV4Y2x1c2l2ZSkuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBuZXcgbGVuZ3RoIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogTGluZWFyLlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIEl0ZXJhdG9ycyBwb2ludGluZyB0byB0aGUgZmlyc3QgcmVtb3ZlZCB2YWx1ZSBhbmQgYmV5b25kIGFyZSBpbnZhbGlkLlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBIGBzdGFydEluZGV4YCBvciBgZW5kSW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbC5cbiAgICovXG4gIHJlbW92ZVJhbmdlKHN0YXJ0SW5kZXg6IG51bWJlciwgZW5kSW5kZXg6IG51bWJlcik6IG51bWJlciB7XG4gICAgY29uc3Qgb2xkVmFsdWVzID0gdGhpcy5fYXJyYXkuc2xpY2Uoc3RhcnRJbmRleCwgZW5kSW5kZXgpO1xuICAgIGZvciAobGV0IGkgPSBzdGFydEluZGV4OyBpIDwgZW5kSW5kZXg7IGkrKykge1xuICAgICAgQXJyYXlFeHQucmVtb3ZlQXQodGhpcy5fYXJyYXksIHN0YXJ0SW5kZXgpO1xuICAgIH1cbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ3JlbW92ZScsXG4gICAgICBvbGRJbmRleDogc3RhcnRJbmRleCxcbiAgICAgIG5ld0luZGV4OiAtMSxcbiAgICAgIG9sZFZhbHVlcyxcbiAgICAgIG5ld1ZhbHVlczogW11cbiAgICB9KTtcbiAgICByZXR1cm4gdGhpcy5sZW5ndGg7XG4gIH1cblxuICBwcml2YXRlIF9hcnJheTogQXJyYXk8VD4gPSBbXTtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xuICBwcml2YXRlIF9pdGVtQ21wOiAoZmlyc3Q6IFQsIHNlY29uZDogVCkgPT4gYm9vbGVhbjtcbiAgcHJpdmF0ZSBfY2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgSU9ic2VydmFibGVMaXN0LklDaGFuZ2VkQXJnczxUPj4odGhpcyk7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgYE9ic2VydmFibGVMaXN0YCBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE9ic2VydmFibGVMaXN0IHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gaW5pdGlhbGl6ZSBhbiBvYnNlcnZhYmxlIG1hcC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnM8VD4ge1xuICAgIC8qKlxuICAgICAqIEFuIG9wdGlvbmFsIGluaXRpYWwgc2V0IG9mIHZhbHVlcy5cbiAgICAgKi9cbiAgICB2YWx1ZXM/OiBJdGVyYWJsZU9yQXJyYXlMaWtlPFQ+O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGl0ZW0gY29tcGFyaXNvbiBmdW5jdGlvbiBmb3IgY2hhbmdlIGRldGVjdGlvbiBvbiBgc2V0YC5cbiAgICAgKlxuICAgICAqIElmIG5vdCBnaXZlbiwgc3RyaWN0IGA9PT1gIGVxdWFsaXR5IHdpbGwgYmUgdXNlZC5cbiAgICAgKi9cbiAgICBpdGVtQ21wPzogKGZpcnN0OiBULCBzZWNvbmQ6IFQpID0+IGJvb2xlYW47XG4gIH1cbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBtb2R1bGUgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBzdHJpY3QgZXF1YWxpdHkgaXRlbSBjbXAuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gaXRlbUNtcChmaXJzdDogYW55LCBzZWNvbmQ6IGFueSk6IGJvb2xlYW4ge1xuICAgIHJldHVybiBmaXJzdCA9PT0gc2Vjb25kO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IElPYnNlcnZhYmxlIH0gZnJvbSAnLi9tb2RlbGRiJztcblxuLyoqXG4gKiBBIG1hcCB3aGljaCBjYW4gYmUgb2JzZXJ2ZWQgZm9yIGNoYW5nZXMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU9ic2VydmFibGVNYXA8VD4gZXh0ZW5kcyBJRGlzcG9zYWJsZSwgSU9ic2VydmFibGUge1xuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhlIE9ic2VydmFibGUuXG4gICAqL1xuICB0eXBlOiAnTWFwJztcblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBtYXAgaGFzIGNoYW5nZWQuXG4gICAqL1xuICByZWFkb25seSBjaGFuZ2VkOiBJU2lnbmFsPHRoaXMsIElPYnNlcnZhYmxlTWFwLklDaGFuZ2VkQXJnczxUPj47XG5cbiAgLyoqXG4gICAqIFRoZSBudW1iZXIgb2Yga2V5LXZhbHVlIHBhaXJzIGluIHRoZSBtYXAuXG4gICAqL1xuICByZWFkb25seSBzaXplOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFNldCBhIGtleS12YWx1ZSBwYWlyIGluIHRoZSBtYXBcbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBrZXkgdG8gc2V0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgZm9yIHRoZSBrZXkuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBvbGQgdmFsdWUgZm9yIHRoZSBrZXksIG9yIHVuZGVmaW5lZFxuICAgKiAgIGlmIHRoYXQgZGlkIG5vdCBleGlzdC5cbiAgICovXG4gIHNldChrZXk6IHN0cmluZywgdmFsdWU6IFQpOiBUIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBHZXQgYSB2YWx1ZSBmb3IgYSBnaXZlbiBrZXkuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSB0aGUga2V5LlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgdmFsdWUgZm9yIHRoYXQga2V5LlxuICAgKi9cbiAgZ2V0KGtleTogc3RyaW5nKTogVCB8IHVuZGVmaW5lZDtcblxuICAvKipcbiAgICogQ2hlY2sgd2hldGhlciB0aGUgbWFwIGhhcyBhIGtleS5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIHRoZSBrZXkgdG8gY2hlY2suXG4gICAqXG4gICAqIEByZXR1cm5zIGB0cnVlYCBpZiB0aGUgbWFwIGhhcyB0aGUga2V5LCBgZmFsc2VgIG90aGVyd2lzZS5cbiAgICovXG4gIGhhcyhrZXk6IHN0cmluZyk6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIEdldCBhIGxpc3Qgb2YgdGhlIGtleXMgaW4gdGhlIG1hcC5cbiAgICpcbiAgICogQHJldHVybnMgLSBhIGxpc3Qgb2Yga2V5cy5cbiAgICovXG4gIGtleXMoKTogc3RyaW5nW107XG5cbiAgLyoqXG4gICAqIEdldCBhIGxpc3Qgb2YgdGhlIHZhbHVlcyBpbiB0aGUgbWFwLlxuICAgKlxuICAgKiBAcmV0dXJucyAtIGEgbGlzdCBvZiB2YWx1ZXMuXG4gICAqL1xuICB2YWx1ZXMoKTogVFtdO1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBrZXkgZnJvbSB0aGUgbWFwXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSB0aGUga2V5IHRvIHJlbW92ZS5cbiAgICpcbiAgICogQHJldHVybnMgdGhlIHZhbHVlIG9mIHRoZSBnaXZlbiBrZXksXG4gICAqICAgb3IgdW5kZWZpbmVkIGlmIHRoYXQgZG9lcyBub3QgZXhpc3QuXG4gICAqL1xuICBkZWxldGUoa2V5OiBzdHJpbmcpOiBUIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBTZXQgdGhlIE9ic2VydmFibGVNYXAgdG8gYW4gZW1wdHkgbWFwLlxuICAgKi9cbiAgY2xlYXIoKTogdm9pZDtcblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIG1hcC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZDtcbn1cblxuLyoqXG4gKiBUaGUgaW50ZXJmYWNlcyBhc3NvY2lhdGVkIHdpdGggYW4gSU9ic2VydmFibGVNYXAuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSU9ic2VydmFibGVNYXAge1xuICAvKipcbiAgICogVGhlIGNoYW5nZSB0eXBlcyB3aGljaCBvY2N1ciBvbiBhbiBvYnNlcnZhYmxlIG1hcC5cbiAgICovXG4gIGV4cG9ydCB0eXBlIENoYW5nZVR5cGUgPVxuICAgIC8qKlxuICAgICAqIEFuIGVudHJ5IHdhcyBhZGRlZC5cbiAgICAgKi9cbiAgICB8ICdhZGQnXG5cbiAgICAvKipcbiAgICAgKiBBbiBlbnRyeSB3YXMgcmVtb3ZlZC5cbiAgICAgKi9cbiAgICB8ICdyZW1vdmUnXG5cbiAgICAvKipcbiAgICAgKiBBbiBlbnRyeSB3YXMgY2hhbmdlZC5cbiAgICAgKi9cbiAgICB8ICdjaGFuZ2UnO1xuXG4gIC8qKlxuICAgKiBUaGUgY2hhbmdlZCBhcmdzIG9iamVjdCB3aGljaCBpcyBlbWl0dGVkIGJ5IGFuIG9ic2VydmFibGUgbWFwLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ2hhbmdlZEFyZ3M8VD4ge1xuICAgIC8qKlxuICAgICAqIFRoZSB0eXBlIG9mIGNoYW5nZSB1bmRlcmdvbmUgYnkgdGhlIG1hcC5cbiAgICAgKi9cbiAgICB0eXBlOiBDaGFuZ2VUeXBlO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGtleSBvZiB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIGtleTogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG9sZCB2YWx1ZSBvZiB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIG9sZFZhbHVlOiBUIHwgdW5kZWZpbmVkO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG5ldyB2YWx1ZSBvZiB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIG5ld1ZhbHVlOiBUIHwgdW5kZWZpbmVkO1xuICB9XG59XG5cbi8qKlxuICogQSBjb25jcmV0ZSBpbXBsZW1lbnRhdGlvbiBvZiBJT2JzZXJ2YWJsZU1hcDxUPi5cbiAqL1xuZXhwb3J0IGNsYXNzIE9ic2VydmFibGVNYXA8VD4gaW1wbGVtZW50cyBJT2JzZXJ2YWJsZU1hcDxUPiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgb2JzZXJ2YWJsZSBtYXAuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBPYnNlcnZhYmxlTWFwLklPcHRpb25zPFQ+ID0ge30pIHtcbiAgICB0aGlzLl9pdGVtQ21wID0gb3B0aW9ucy5pdGVtQ21wIHx8IFByaXZhdGUuaXRlbUNtcDtcbiAgICBpZiAob3B0aW9ucy52YWx1ZXMpIHtcbiAgICAgIGZvciAoY29uc3Qga2V5IGluIG9wdGlvbnMudmFsdWVzKSB7XG4gICAgICAgIHRoaXMuX21hcC5zZXQoa2V5LCBvcHRpb25zLnZhbHVlc1trZXldKTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhlIE9ic2VydmFibGUuXG4gICAqL1xuICBnZXQgdHlwZSgpOiAnTWFwJyB7XG4gICAgcmV0dXJuICdNYXAnO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbWFwIGhhcyBjaGFuZ2VkLlxuICAgKi9cbiAgZ2V0IGNoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCBJT2JzZXJ2YWJsZU1hcC5JQ2hhbmdlZEFyZ3M8VD4+IHtcbiAgICByZXR1cm4gdGhpcy5fY2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoaXMgbWFwIGhhcyBiZWVuIGRpc3Bvc2VkLlxuICAgKi9cbiAgZ2V0IGlzRGlzcG9zZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIG51bWJlciBvZiBrZXktdmFsdWUgcGFpcnMgaW4gdGhlIG1hcC5cbiAgICovXG4gIGdldCBzaXplKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX21hcC5zaXplO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCBhIGtleS12YWx1ZSBwYWlyIGluIHRoZSBtYXBcbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBrZXkgdG8gc2V0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgZm9yIHRoZSBrZXkuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBvbGQgdmFsdWUgZm9yIHRoZSBrZXksIG9yIHVuZGVmaW5lZFxuICAgKiAgIGlmIHRoYXQgZGlkIG5vdCBleGlzdC5cbiAgICpcbiAgICogQHRocm93cyBpZiB0aGUgbmV3IHZhbHVlIGlzIHVuZGVmaW5lZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGlzIGEgbm8tb3AgaWYgdGhlIHZhbHVlIGRvZXMgbm90IGNoYW5nZS5cbiAgICovXG4gIHNldChrZXk6IHN0cmluZywgdmFsdWU6IFQpOiBUIHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCBvbGRWYWwgPSB0aGlzLl9tYXAuZ2V0KGtleSk7XG4gICAgaWYgKHZhbHVlID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHRocm93IEVycm9yKCdDYW5ub3Qgc2V0IGFuIHVuZGVmaW5lZCB2YWx1ZSwgdXNlIHJlbW92ZScpO1xuICAgIH1cbiAgICAvLyBCYWlsIGlmIHRoZSB2YWx1ZSBkb2VzIG5vdCBjaGFuZ2UuXG4gICAgY29uc3QgaXRlbUNtcCA9IHRoaXMuX2l0ZW1DbXA7XG4gICAgaWYgKG9sZFZhbCAhPT0gdW5kZWZpbmVkICYmIGl0ZW1DbXAob2xkVmFsLCB2YWx1ZSkpIHtcbiAgICAgIHJldHVybiBvbGRWYWw7XG4gICAgfVxuICAgIHRoaXMuX21hcC5zZXQoa2V5LCB2YWx1ZSk7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6IG9sZFZhbCA/ICdjaGFuZ2UnIDogJ2FkZCcsXG4gICAgICBrZXk6IGtleSxcbiAgICAgIG9sZFZhbHVlOiBvbGRWYWwsXG4gICAgICBuZXdWYWx1ZTogdmFsdWVcbiAgICB9KTtcbiAgICByZXR1cm4gb2xkVmFsO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhIHZhbHVlIGZvciBhIGdpdmVuIGtleS5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIHRoZSBrZXkuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSB2YWx1ZSBmb3IgdGhhdCBrZXkuXG4gICAqL1xuICBnZXQoa2V5OiBzdHJpbmcpOiBUIHwgdW5kZWZpbmVkIHtcbiAgICByZXR1cm4gdGhpcy5fbWFwLmdldChrZXkpO1xuICB9XG5cbiAgLyoqXG4gICAqIENoZWNrIHdoZXRoZXIgdGhlIG1hcCBoYXMgYSBrZXkuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSB0aGUga2V5IHRvIGNoZWNrLlxuICAgKlxuICAgKiBAcmV0dXJucyBgdHJ1ZWAgaWYgdGhlIG1hcCBoYXMgdGhlIGtleSwgYGZhbHNlYCBvdGhlcndpc2UuXG4gICAqL1xuICBoYXMoa2V5OiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fbWFwLmhhcyhrZXkpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhIGxpc3Qgb2YgdGhlIGtleXMgaW4gdGhlIG1hcC5cbiAgICpcbiAgICogQHJldHVybnMgLSBhIGxpc3Qgb2Yga2V5cy5cbiAgICovXG4gIGtleXMoKTogc3RyaW5nW10ge1xuICAgIGNvbnN0IGtleUxpc3Q6IHN0cmluZ1tdID0gW107XG4gICAgdGhpcy5fbWFwLmZvckVhY2goKHY6IFQsIGs6IHN0cmluZykgPT4ge1xuICAgICAga2V5TGlzdC5wdXNoKGspO1xuICAgIH0pO1xuICAgIHJldHVybiBrZXlMaXN0O1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhIGxpc3Qgb2YgdGhlIHZhbHVlcyBpbiB0aGUgbWFwLlxuICAgKlxuICAgKiBAcmV0dXJucyAtIGEgbGlzdCBvZiB2YWx1ZXMuXG4gICAqL1xuICB2YWx1ZXMoKTogVFtdIHtcbiAgICBjb25zdCB2YWxMaXN0OiBUW10gPSBbXTtcbiAgICB0aGlzLl9tYXAuZm9yRWFjaCgodjogVCwgazogc3RyaW5nKSA9PiB7XG4gICAgICB2YWxMaXN0LnB1c2godik7XG4gICAgfSk7XG4gICAgcmV0dXJuIHZhbExpc3Q7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIGEga2V5IGZyb20gdGhlIG1hcFxuICAgKlxuICAgKiBAcGFyYW0ga2V5IC0gdGhlIGtleSB0byByZW1vdmUuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSB2YWx1ZSBvZiB0aGUgZ2l2ZW4ga2V5LFxuICAgKiAgIG9yIHVuZGVmaW5lZCBpZiB0aGF0IGRvZXMgbm90IGV4aXN0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgaXMgYSBuby1vcCBpZiB0aGUgdmFsdWUgZG9lcyBub3QgY2hhbmdlLlxuICAgKi9cbiAgZGVsZXRlKGtleTogc3RyaW5nKTogVCB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3Qgb2xkVmFsID0gdGhpcy5fbWFwLmdldChrZXkpO1xuICAgIGNvbnN0IHJlbW92ZWQgPSB0aGlzLl9tYXAuZGVsZXRlKGtleSk7XG4gICAgaWYgKHJlbW92ZWQpIHtcbiAgICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7XG4gICAgICAgIHR5cGU6ICdyZW1vdmUnLFxuICAgICAgICBrZXk6IGtleSxcbiAgICAgICAgb2xkVmFsdWU6IG9sZFZhbCxcbiAgICAgICAgbmV3VmFsdWU6IHVuZGVmaW5lZFxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiBvbGRWYWw7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBPYnNlcnZhYmxlTWFwIHRvIGFuIGVtcHR5IG1hcC5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQge1xuICAgIC8vIERlbGV0ZSBvbmUgYnkgb25lIHRvIGVtaXQgdGhlIGNvcnJlY3Qgc2lnbmFscy5cbiAgICBjb25zdCBrZXlMaXN0ID0gdGhpcy5rZXlzKCk7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBrZXlMaXN0Lmxlbmd0aDsgaSsrKSB7XG4gICAgICB0aGlzLmRlbGV0ZShrZXlMaXN0W2ldKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIG1hcC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICAgIHRoaXMuX21hcC5jbGVhcigpO1xuICB9XG5cbiAgcHJpdmF0ZSBfbWFwOiBNYXA8c3RyaW5nLCBUPiA9IG5ldyBNYXA8c3RyaW5nLCBUPigpO1xuICBwcml2YXRlIF9pdGVtQ21wOiAoZmlyc3Q6IFQsIHNlY29uZDogVCkgPT4gYm9vbGVhbjtcbiAgcHJpdmF0ZSBfY2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgSU9ic2VydmFibGVNYXAuSUNoYW5nZWRBcmdzPFQ+Pih0aGlzKTtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGBPYnNlcnZhYmxlTWFwYCBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE9ic2VydmFibGVNYXAge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBpbml0aWFsaXplIGFuIG9ic2VydmFibGUgbWFwLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9uczxUPiB7XG4gICAgLyoqXG4gICAgICogQW4gb3B0aW9uYWwgaW5pdGlhbCBzZXQgb2YgdmFsdWVzLlxuICAgICAqL1xuICAgIHZhbHVlcz86IHsgW2tleTogc3RyaW5nXTogVCB9O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGl0ZW0gY29tcGFyaXNvbiBmdW5jdGlvbiBmb3IgY2hhbmdlIGRldGVjdGlvbiBvbiBgc2V0YC5cbiAgICAgKlxuICAgICAqIElmIG5vdCBnaXZlbiwgc3RyaWN0IGA9PT1gIGVxdWFsaXR5IHdpbGwgYmUgdXNlZC5cbiAgICAgKi9cbiAgICBpdGVtQ21wPzogKGZpcnN0OiBULCBzZWNvbmQ6IFQpID0+IGJvb2xlYW47XG4gIH1cbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBtb2R1bGUgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBzdHJpY3QgZXF1YWxpdHkgaXRlbSBjb21wYXJhdG9yLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGl0ZW1DbXAoZmlyc3Q6IGFueSwgc2Vjb25kOiBhbnkpOiBib29sZWFuIHtcbiAgICByZXR1cm4gZmlyc3QgPT09IHNlY29uZDtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBJT2JzZXJ2YWJsZSB9IGZyb20gJy4vbW9kZWxkYic7XG5cbi8qKlxuICogQSBzdHJpbmcgd2hpY2ggY2FuIGJlIG9ic2VydmVkIGZvciBjaGFuZ2VzLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElPYnNlcnZhYmxlU3RyaW5nIGV4dGVuZHMgSURpc3Bvc2FibGUsIElPYnNlcnZhYmxlIHtcbiAgLyoqXG4gICAqIFRoZSB0eXBlIG9mIHRoZSBPYnNlcnZhYmxlLlxuICAgKi9cbiAgdHlwZTogJ1N0cmluZyc7XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgc3RyaW5nIGhhcyBjaGFuZ2VkLlxuICAgKi9cbiAgcmVhZG9ubHkgY2hhbmdlZDogSVNpZ25hbDx0aGlzLCBJT2JzZXJ2YWJsZVN0cmluZy5JQ2hhbmdlZEFyZ3M+O1xuXG4gIC8qKlxuICAgKiBUaGUgdmFsdWUgb2YgdGhlIHN0cmluZy5cbiAgICovXG4gIHRleHQ6IHN0cmluZztcblxuICAvKipcbiAgICogSW5zZXJ0IGEgc3Vic3RyaW5nLlxuICAgKlxuICAgKiBAcGFyYW0gaW5kZXggLSBUaGUgc3RhcnRpbmcgaW5kZXguXG4gICAqXG4gICAqIEBwYXJhbSB0ZXh0IC0gVGhlIHN1YnN0cmluZyB0byBpbnNlcnQuXG4gICAqL1xuICBpbnNlcnQoaW5kZXg6IG51bWJlciwgdGV4dDogc3RyaW5nKTogdm9pZDtcblxuICAvKipcbiAgICogUmVtb3ZlIGEgc3Vic3RyaW5nLlxuICAgKlxuICAgKiBAcGFyYW0gc3RhcnQgLSBUaGUgc3RhcnRpbmcgaW5kZXguXG4gICAqXG4gICAqIEBwYXJhbSBlbmQgLSBUaGUgZW5kaW5nIGluZGV4LlxuICAgKi9cbiAgcmVtb3ZlKHN0YXJ0OiBudW1iZXIsIGVuZDogbnVtYmVyKTogdm9pZDtcblxuICAvKipcbiAgICogU2V0IHRoZSBPYnNlcnZhYmxlU3RyaW5nIHRvIGFuIGVtcHR5IHN0cmluZy5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBzdHJpbmcuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQ7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgYElPYnNlcnZhYmxlU3RyaW5nYCBhc3NvY2lhdGUgaW50ZXJmYWNlcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJT2JzZXJ2YWJsZVN0cmluZyB7XG4gIC8qKlxuICAgKiBUaGUgY2hhbmdlIHR5cGVzIHdoaWNoIG9jY3VyIG9uIGFuIG9ic2VydmFibGUgc3RyaW5nLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgQ2hhbmdlVHlwZSA9XG4gICAgLyoqXG4gICAgICogVGV4dCB3YXMgaW5zZXJ0ZWQuXG4gICAgICovXG4gICAgfCAnaW5zZXJ0J1xuXG4gICAgLyoqXG4gICAgICogVGV4dCB3YXMgcmVtb3ZlZC5cbiAgICAgKi9cbiAgICB8ICdyZW1vdmUnXG5cbiAgICAvKipcbiAgICAgKiBUZXh0IHdhcyBzZXQuXG4gICAgICovXG4gICAgfCAnc2V0JztcblxuICAvKipcbiAgICogVGhlIGNoYW5nZWQgYXJncyBvYmplY3Qgd2hpY2ggaXMgZW1pdHRlZCBieSBhbiBvYnNlcnZhYmxlIHN0cmluZy5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUNoYW5nZWRBcmdzIHtcbiAgICAvKipcbiAgICAgKiBUaGUgdHlwZSBvZiBjaGFuZ2UgdW5kZXJnb25lIGJ5IHRoZSBsaXN0LlxuICAgICAqL1xuICAgIHR5cGU6IENoYW5nZVR5cGU7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc3RhcnRpbmcgaW5kZXggb2YgdGhlIGNoYW5nZS5cbiAgICAgKi9cbiAgICBzdGFydDogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGVuZCBpbmRleCBvZiB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIGVuZDogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHZhbHVlIG9mIHRoZSBjaGFuZ2UuXG4gICAgICpcbiAgICAgKiAjIyMgTm90ZXNcbiAgICAgKiBJZiBgQ2hhbmdlVHlwZWAgaXMgYHNldGAsIHRoZW5cbiAgICAgKiB0aGlzIGlzIHRoZSBuZXcgdmFsdWUgb2YgdGhlIHN0cmluZy5cbiAgICAgKlxuICAgICAqIElmIGBDaGFuZ2VUeXBlYCBpcyBgaW5zZXJ0YCB0aGlzIGlzXG4gICAgICogdGhlIHZhbHVlIG9mIHRoZSBpbnNlcnRlZCBzdHJpbmcuXG4gICAgICpcbiAgICAgKiBJZiBgQ2hhbmdlVHlwZWAgaXMgcmVtb3ZlIHRoaXMgaXMgdGhlXG4gICAgICogdmFsdWUgb2YgdGhlIHJlbW92ZWQgc3Vic3RyaW5nLlxuICAgICAqL1xuICAgIHZhbHVlOiBzdHJpbmc7XG4gIH1cbn1cblxuLyoqXG4gKiBBIGNvbmNyZXRlIGltcGxlbWVudGF0aW9uIG9mIFtbSU9ic2VydmFibGVTdHJpbmddXVxuICovXG5leHBvcnQgY2xhc3MgT2JzZXJ2YWJsZVN0cmluZyBpbXBsZW1lbnRzIElPYnNlcnZhYmxlU3RyaW5nIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBvYnNlcnZhYmxlIHN0cmluZy5cbiAgICovXG4gIGNvbnN0cnVjdG9yKGluaXRpYWxUZXh0OiBzdHJpbmcgPSAnJykge1xuICAgIHRoaXMuX3RleHQgPSBpbml0aWFsVGV4dDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgdHlwZSBvZiB0aGUgT2JzZXJ2YWJsZS5cbiAgICovXG4gIGdldCB0eXBlKCk6ICdTdHJpbmcnIHtcbiAgICByZXR1cm4gJ1N0cmluZyc7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBzdHJpbmcgaGFzIGNoYW5nZWQuXG4gICAqL1xuICBnZXQgY2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElPYnNlcnZhYmxlU3RyaW5nLklDaGFuZ2VkQXJncz4ge1xuICAgIHJldHVybiB0aGlzLl9jaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgdmFsdWUgb2YgdGhlIHN0cmluZy5cbiAgICovXG4gIHNldCB0ZXh0KHZhbHVlOiBzdHJpbmcpIHtcbiAgICBpZiAodmFsdWUubGVuZ3RoID09PSB0aGlzLl90ZXh0Lmxlbmd0aCAmJiB2YWx1ZSA9PT0gdGhpcy5fdGV4dCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl90ZXh0ID0gdmFsdWU7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdzZXQnLFxuICAgICAgc3RhcnQ6IDAsXG4gICAgICBlbmQ6IHZhbHVlLmxlbmd0aCxcbiAgICAgIHZhbHVlOiB2YWx1ZVxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgdmFsdWUgb2YgdGhlIHN0cmluZy5cbiAgICovXG4gIGdldCB0ZXh0KCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX3RleHQ7XG4gIH1cblxuICAvKipcbiAgICogSW5zZXJ0IGEgc3Vic3RyaW5nLlxuICAgKlxuICAgKiBAcGFyYW0gaW5kZXggLSBUaGUgc3RhcnRpbmcgaW5kZXguXG4gICAqXG4gICAqIEBwYXJhbSB0ZXh0IC0gVGhlIHN1YnN0cmluZyB0byBpbnNlcnQuXG4gICAqL1xuICBpbnNlcnQoaW5kZXg6IG51bWJlciwgdGV4dDogc3RyaW5nKTogdm9pZCB7XG4gICAgdGhpcy5fdGV4dCA9IHRoaXMuX3RleHQuc2xpY2UoMCwgaW5kZXgpICsgdGV4dCArIHRoaXMuX3RleHQuc2xpY2UoaW5kZXgpO1xuICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7XG4gICAgICB0eXBlOiAnaW5zZXJ0JyxcbiAgICAgIHN0YXJ0OiBpbmRleCxcbiAgICAgIGVuZDogaW5kZXggKyB0ZXh0Lmxlbmd0aCxcbiAgICAgIHZhbHVlOiB0ZXh0XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIGEgc3Vic3RyaW5nLlxuICAgKlxuICAgKiBAcGFyYW0gc3RhcnQgLSBUaGUgc3RhcnRpbmcgaW5kZXguXG4gICAqXG4gICAqIEBwYXJhbSBlbmQgLSBUaGUgZW5kaW5nIGluZGV4LlxuICAgKi9cbiAgcmVtb3ZlKHN0YXJ0OiBudW1iZXIsIGVuZDogbnVtYmVyKTogdm9pZCB7XG4gICAgY29uc3Qgb2xkVmFsdWU6IHN0cmluZyA9IHRoaXMuX3RleHQuc2xpY2Uoc3RhcnQsIGVuZCk7XG4gICAgdGhpcy5fdGV4dCA9IHRoaXMuX3RleHQuc2xpY2UoMCwgc3RhcnQpICsgdGhpcy5fdGV4dC5zbGljZShlbmQpO1xuICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7XG4gICAgICB0eXBlOiAncmVtb3ZlJyxcbiAgICAgIHN0YXJ0OiBzdGFydCxcbiAgICAgIGVuZDogZW5kLFxuICAgICAgdmFsdWU6IG9sZFZhbHVlXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBPYnNlcnZhYmxlU3RyaW5nIHRvIGFuIGVtcHR5IHN0cmluZy5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQge1xuICAgIHRoaXMudGV4dCA9ICcnO1xuICB9XG5cbiAgLyoqXG4gICAqIFRlc3Qgd2hldGhlciB0aGUgc3RyaW5nIGhhcyBiZWVuIGRpc3Bvc2VkLlxuICAgKi9cbiAgZ2V0IGlzRGlzcG9zZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHN0cmluZy5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX2lzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgU2lnbmFsLmNsZWFyRGF0YSh0aGlzKTtcbiAgICB0aGlzLmNsZWFyKCk7XG4gIH1cblxuICBwcml2YXRlIF90ZXh0ID0gJyc7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQ6IGJvb2xlYW4gPSBmYWxzZTtcbiAgcHJpdmF0ZSBfY2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgSU9ic2VydmFibGVTdHJpbmcuSUNoYW5nZWRBcmdzPih0aGlzKTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgZWFjaCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IEpTT05WYWx1ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElPYnNlcnZhYmxlTGlzdCwgT2JzZXJ2YWJsZUxpc3QgfSBmcm9tICcuL29ic2VydmFibGVsaXN0JztcblxuLyoqXG4gKiBBbiBvYmplY3Qgd2hpY2gga25vd3MgaG93IHRvIHNlcmlhbGl6ZSBhbmRcbiAqIGRlc2VyaWFsaXplIHRoZSB0eXBlIFQuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVNlcmlhbGl6ZXI8VD4ge1xuICAvKipcbiAgICogQ29udmVydCB0aGUgb2JqZWN0IHRvIEpTT04uXG4gICAqL1xuICB0b0pTT04odmFsdWU6IFQpOiBKU09OVmFsdWU7XG5cbiAgLyoqXG4gICAqIERlc2VyaWFsaXplIHRoZSBvYmplY3QgZnJvbSBKU09OLlxuICAgKi9cbiAgZnJvbUpTT04odmFsdWU6IEpTT05WYWx1ZSk6IFQ7XG59XG5cbi8qKlxuICogQW4gb2JzZXJ2YWJsZSBsaXN0IHRoYXQgc3VwcG9ydHMgdW5kby9yZWRvLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElPYnNlcnZhYmxlVW5kb2FibGVMaXN0PFQ+IGV4dGVuZHMgSU9ic2VydmFibGVMaXN0PFQ+IHtcbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG9iamVjdCBjYW4gcmVkbyBjaGFuZ2VzLlxuICAgKi9cbiAgcmVhZG9ubHkgY2FuUmVkbzogYm9vbGVhbjtcblxuICAvKipcbiAgICogV2hldGhlciB0aGUgb2JqZWN0IGNhbiB1bmRvIGNoYW5nZXMuXG4gICAqL1xuICByZWFkb25seSBjYW5VbmRvOiBib29sZWFuO1xuXG4gIC8qKlxuICAgKiBCZWdpbiBhIGNvbXBvdW5kIG9wZXJhdGlvbi5cbiAgICpcbiAgICogQHBhcmFtIGlzVW5kb0FibGUgLSBXaGV0aGVyIHRoZSBvcGVyYXRpb24gaXMgdW5kb2FibGUuXG4gICAqICAgVGhlIGRlZmF1bHQgaXMgYGZhbHNlYC5cbiAgICovXG4gIGJlZ2luQ29tcG91bmRPcGVyYXRpb24oaXNVbmRvQWJsZT86IGJvb2xlYW4pOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBFbmQgYSBjb21wb3VuZCBvcGVyYXRpb24uXG4gICAqL1xuICBlbmRDb21wb3VuZE9wZXJhdGlvbigpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBVbmRvIGFuIG9wZXJhdGlvbi5cbiAgICovXG4gIHVuZG8oKTogdm9pZDtcblxuICAvKipcbiAgICogUmVkbyBhbiBvcGVyYXRpb24uXG4gICAqL1xuICByZWRvKCk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIENsZWFyIHRoZSBjaGFuZ2Ugc3RhY2suXG4gICAqL1xuICBjbGVhclVuZG8oKTogdm9pZDtcbn1cblxuLyoqXG4gKiBBIGNvbmNyZXRlIGltcGxlbWVudGF0aW9uIG9mIGFuIG9ic2VydmFibGUgdW5kb2FibGUgbGlzdC5cbiAqL1xuZXhwb3J0IGNsYXNzIE9ic2VydmFibGVVbmRvYWJsZUxpc3Q8VD5cbiAgZXh0ZW5kcyBPYnNlcnZhYmxlTGlzdDxUPlxuICBpbXBsZW1lbnRzIElPYnNlcnZhYmxlVW5kb2FibGVMaXN0PFQ+IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyB1bmRvYWJsZSBvYnNlcnZhYmxlIGxpc3QuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihzZXJpYWxpemVyOiBJU2VyaWFsaXplcjxUPikge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5fc2VyaWFsaXplciA9IHNlcmlhbGl6ZXI7XG4gICAgdGhpcy5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25MaXN0Q2hhbmdlZCwgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgb2JqZWN0IGNhbiByZWRvIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgY2FuUmVkbygpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faW5kZXggPCB0aGlzLl9zdGFjay5sZW5ndGggLSAxO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG9iamVjdCBjYW4gdW5kbyBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IGNhblVuZG8oKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2luZGV4ID49IDA7XG4gIH1cblxuICAvKipcbiAgICogQmVnaW4gYSBjb21wb3VuZCBvcGVyYXRpb24uXG4gICAqXG4gICAqIEBwYXJhbSBpc1VuZG9BYmxlIC0gV2hldGhlciB0aGUgb3BlcmF0aW9uIGlzIHVuZG9hYmxlLlxuICAgKiAgIFRoZSBkZWZhdWx0IGlzIGB0cnVlYC5cbiAgICovXG4gIGJlZ2luQ29tcG91bmRPcGVyYXRpb24oaXNVbmRvQWJsZT86IGJvb2xlYW4pOiB2b2lkIHtcbiAgICB0aGlzLl9pbkNvbXBvdW5kID0gdHJ1ZTtcbiAgICB0aGlzLl9pc1VuZG9hYmxlID0gaXNVbmRvQWJsZSAhPT0gZmFsc2U7XG4gICAgdGhpcy5fbWFkZUNvbXBvdW5kQ2hhbmdlID0gZmFsc2U7XG4gIH1cblxuICAvKipcbiAgICogRW5kIGEgY29tcG91bmQgb3BlcmF0aW9uLlxuICAgKi9cbiAgZW5kQ29tcG91bmRPcGVyYXRpb24oKTogdm9pZCB7XG4gICAgdGhpcy5faW5Db21wb3VuZCA9IGZhbHNlO1xuICAgIHRoaXMuX2lzVW5kb2FibGUgPSB0cnVlO1xuICAgIGlmICh0aGlzLl9tYWRlQ29tcG91bmRDaGFuZ2UpIHtcbiAgICAgIHRoaXMuX2luZGV4Kys7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFVuZG8gYW4gb3BlcmF0aW9uLlxuICAgKi9cbiAgdW5kbygpOiB2b2lkIHtcbiAgICBpZiAoIXRoaXMuY2FuVW5kbykge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBjaGFuZ2VzID0gdGhpcy5fc3RhY2tbdGhpcy5faW5kZXhdO1xuICAgIHRoaXMuX2lzVW5kb2FibGUgPSBmYWxzZTtcbiAgICBmb3IgKGNvbnN0IGNoYW5nZSBvZiBjaGFuZ2VzLnJldmVyc2UoKSkge1xuICAgICAgdGhpcy5fdW5kb0NoYW5nZShjaGFuZ2UpO1xuICAgIH1cbiAgICB0aGlzLl9pc1VuZG9hYmxlID0gdHJ1ZTtcbiAgICB0aGlzLl9pbmRleC0tO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlZG8gYW4gb3BlcmF0aW9uLlxuICAgKi9cbiAgcmVkbygpOiB2b2lkIHtcbiAgICBpZiAoIXRoaXMuY2FuUmVkbykge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pbmRleCsrO1xuICAgIGNvbnN0IGNoYW5nZXMgPSB0aGlzLl9zdGFja1t0aGlzLl9pbmRleF07XG4gICAgdGhpcy5faXNVbmRvYWJsZSA9IGZhbHNlO1xuICAgIGZvciAoY29uc3QgY2hhbmdlIG9mIGNoYW5nZXMpIHtcbiAgICAgIHRoaXMuX3JlZG9DaGFuZ2UoY2hhbmdlKTtcbiAgICB9XG4gICAgdGhpcy5faXNVbmRvYWJsZSA9IHRydWU7XG4gIH1cblxuICAvKipcbiAgICogQ2xlYXIgdGhlIGNoYW5nZSBzdGFjay5cbiAgICovXG4gIGNsZWFyVW5kbygpOiB2b2lkIHtcbiAgICB0aGlzLl9pbmRleCA9IC0xO1xuICAgIHRoaXMuX3N0YWNrID0gW107XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIGluIHRoZSBsaXN0LlxuICAgKi9cbiAgcHJpdmF0ZSBfb25MaXN0Q2hhbmdlZChcbiAgICBsaXN0OiBJT2JzZXJ2YWJsZUxpc3Q8VD4sXG4gICAgY2hhbmdlOiBJT2JzZXJ2YWJsZUxpc3QuSUNoYW5nZWRBcmdzPFQ+XG4gICk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQgfHwgIXRoaXMuX2lzVW5kb2FibGUpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgLy8gQ2xlYXIgZXZlcnl0aGluZyBhZnRlciB0aGlzIHBvc2l0aW9uIGlmIG5lY2Vzc2FyeS5cbiAgICBpZiAoIXRoaXMuX2luQ29tcG91bmQgfHwgIXRoaXMuX21hZGVDb21wb3VuZENoYW5nZSkge1xuICAgICAgdGhpcy5fc3RhY2sgPSB0aGlzLl9zdGFjay5zbGljZSgwLCB0aGlzLl9pbmRleCArIDEpO1xuICAgIH1cbiAgICAvLyBDb3B5IHRoZSBjaGFuZ2UuXG4gICAgY29uc3QgZXZ0ID0gdGhpcy5fY29weUNoYW5nZShjaGFuZ2UpO1xuICAgIC8vIFB1dCB0aGUgY2hhbmdlIGluIHRoZSBzdGFjay5cbiAgICBpZiAodGhpcy5fc3RhY2tbdGhpcy5faW5kZXggKyAxXSkge1xuICAgICAgdGhpcy5fc3RhY2tbdGhpcy5faW5kZXggKyAxXS5wdXNoKGV2dCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX3N0YWNrLnB1c2goW2V2dF0pO1xuICAgIH1cbiAgICAvLyBJZiBub3QgaW4gYSBjb21wb3VuZCBvcGVyYXRpb24sIGluY3JlYXNlIGluZGV4LlxuICAgIGlmICghdGhpcy5faW5Db21wb3VuZCkge1xuICAgICAgdGhpcy5faW5kZXgrKztcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5fbWFkZUNvbXBvdW5kQ2hhbmdlID0gdHJ1ZTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVW5kbyBhIGNoYW5nZSBldmVudC5cbiAgICovXG4gIHByaXZhdGUgX3VuZG9DaGFuZ2UoY2hhbmdlOiBJT2JzZXJ2YWJsZUxpc3QuSUNoYW5nZWRBcmdzPEpTT05WYWx1ZT4pOiB2b2lkIHtcbiAgICBsZXQgaW5kZXggPSAwO1xuICAgIGNvbnN0IHNlcmlhbGl6ZXIgPSB0aGlzLl9zZXJpYWxpemVyO1xuICAgIHN3aXRjaCAoY2hhbmdlLnR5cGUpIHtcbiAgICAgIGNhc2UgJ2FkZCc6XG4gICAgICAgIGVhY2goY2hhbmdlLm5ld1ZhbHVlcywgKCkgPT4ge1xuICAgICAgICAgIHRoaXMucmVtb3ZlKGNoYW5nZS5uZXdJbmRleCk7XG4gICAgICAgIH0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3NldCc6XG4gICAgICAgIGluZGV4ID0gY2hhbmdlLm9sZEluZGV4O1xuICAgICAgICBlYWNoKGNoYW5nZS5vbGRWYWx1ZXMsIHZhbHVlID0+IHtcbiAgICAgICAgICB0aGlzLnNldChpbmRleCsrLCBzZXJpYWxpemVyLmZyb21KU09OKHZhbHVlKSk7XG4gICAgICAgIH0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3JlbW92ZSc6XG4gICAgICAgIGluZGV4ID0gY2hhbmdlLm9sZEluZGV4O1xuICAgICAgICBlYWNoKGNoYW5nZS5vbGRWYWx1ZXMsIHZhbHVlID0+IHtcbiAgICAgICAgICB0aGlzLmluc2VydChpbmRleCsrLCBzZXJpYWxpemVyLmZyb21KU09OKHZhbHVlKSk7XG4gICAgICAgIH0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ21vdmUnOlxuICAgICAgICB0aGlzLm1vdmUoY2hhbmdlLm5ld0luZGV4LCBjaGFuZ2Uub2xkSW5kZXgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIHJldHVybjtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogUmVkbyBhIGNoYW5nZSBldmVudC5cbiAgICovXG4gIHByaXZhdGUgX3JlZG9DaGFuZ2UoY2hhbmdlOiBJT2JzZXJ2YWJsZUxpc3QuSUNoYW5nZWRBcmdzPEpTT05WYWx1ZT4pOiB2b2lkIHtcbiAgICBsZXQgaW5kZXggPSAwO1xuICAgIGNvbnN0IHNlcmlhbGl6ZXIgPSB0aGlzLl9zZXJpYWxpemVyO1xuICAgIHN3aXRjaCAoY2hhbmdlLnR5cGUpIHtcbiAgICAgIGNhc2UgJ2FkZCc6XG4gICAgICAgIGluZGV4ID0gY2hhbmdlLm5ld0luZGV4O1xuICAgICAgICBlYWNoKGNoYW5nZS5uZXdWYWx1ZXMsIHZhbHVlID0+IHtcbiAgICAgICAgICB0aGlzLmluc2VydChpbmRleCsrLCBzZXJpYWxpemVyLmZyb21KU09OKHZhbHVlKSk7XG4gICAgICAgIH0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3NldCc6XG4gICAgICAgIGluZGV4ID0gY2hhbmdlLm5ld0luZGV4O1xuICAgICAgICBlYWNoKGNoYW5nZS5uZXdWYWx1ZXMsIHZhbHVlID0+IHtcbiAgICAgICAgICB0aGlzLnNldChjaGFuZ2UubmV3SW5kZXgrKywgc2VyaWFsaXplci5mcm9tSlNPTih2YWx1ZSkpO1xuICAgICAgICB9KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdyZW1vdmUnOlxuICAgICAgICBlYWNoKGNoYW5nZS5vbGRWYWx1ZXMsICgpID0+IHtcbiAgICAgICAgICB0aGlzLnJlbW92ZShjaGFuZ2Uub2xkSW5kZXgpO1xuICAgICAgICB9KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdtb3ZlJzpcbiAgICAgICAgdGhpcy5tb3ZlKGNoYW5nZS5vbGRJbmRleCwgY2hhbmdlLm5ld0luZGV4KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICByZXR1cm47XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIENvcHkgYSBjaGFuZ2UgYXMgSlNPTi5cbiAgICovXG4gIHByaXZhdGUgX2NvcHlDaGFuZ2UoXG4gICAgY2hhbmdlOiBJT2JzZXJ2YWJsZUxpc3QuSUNoYW5nZWRBcmdzPFQ+XG4gICk6IElPYnNlcnZhYmxlTGlzdC5JQ2hhbmdlZEFyZ3M8SlNPTlZhbHVlPiB7XG4gICAgY29uc3Qgb2xkVmFsdWVzOiBKU09OVmFsdWVbXSA9IFtdO1xuICAgIGVhY2goY2hhbmdlLm9sZFZhbHVlcywgdmFsdWUgPT4ge1xuICAgICAgb2xkVmFsdWVzLnB1c2godGhpcy5fc2VyaWFsaXplci50b0pTT04odmFsdWUpKTtcbiAgICB9KTtcbiAgICBjb25zdCBuZXdWYWx1ZXM6IEpTT05WYWx1ZVtdID0gW107XG4gICAgZWFjaChjaGFuZ2UubmV3VmFsdWVzLCB2YWx1ZSA9PiB7XG4gICAgICBuZXdWYWx1ZXMucHVzaCh0aGlzLl9zZXJpYWxpemVyLnRvSlNPTih2YWx1ZSkpO1xuICAgIH0pO1xuICAgIHJldHVybiB7XG4gICAgICB0eXBlOiBjaGFuZ2UudHlwZSxcbiAgICAgIG9sZEluZGV4OiBjaGFuZ2Uub2xkSW5kZXgsXG4gICAgICBuZXdJbmRleDogY2hhbmdlLm5ld0luZGV4LFxuICAgICAgb2xkVmFsdWVzLFxuICAgICAgbmV3VmFsdWVzXG4gICAgfTtcbiAgfVxuXG4gIHByaXZhdGUgX2luQ29tcG91bmQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfaXNVbmRvYWJsZSA9IHRydWU7XG4gIHByaXZhdGUgX21hZGVDb21wb3VuZENoYW5nZSA9IGZhbHNlO1xuICBwcml2YXRlIF9pbmRleCA9IC0xO1xuICBwcml2YXRlIF9zdGFjazogSU9ic2VydmFibGVMaXN0LklDaGFuZ2VkQXJnczxKU09OVmFsdWU+W11bXSA9IFtdO1xuICBwcml2YXRlIF9zZXJpYWxpemVyOiBJU2VyaWFsaXplcjxUPjtcbn1cblxuLyoqXG4gKiBOYW1lc3BhY2UgZm9yIE9ic2VydmFibGVVbmRvYWJsZUxpc3QgdXRpbGl0aWVzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE9ic2VydmFibGVVbmRvYWJsZUxpc3Qge1xuICAvKipcbiAgICogQSBkZWZhdWx0LCBpZGVudGl0eSBzZXJpYWxpemVyLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIElkZW50aXR5U2VyaWFsaXplcjxUIGV4dGVuZHMgSlNPTlZhbHVlPlxuICAgIGltcGxlbWVudHMgSVNlcmlhbGl6ZXI8VD4ge1xuICAgIC8qKlxuICAgICAqIElkZW50aXR5IHNlcmlhbGl6ZS5cbiAgICAgKi9cbiAgICB0b0pTT04odmFsdWU6IFQpOiBKU09OVmFsdWUge1xuICAgICAgcmV0dXJuIHZhbHVlO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIElkZW50aXR5IGRlc2VyaWFsaXplLlxuICAgICAqL1xuICAgIGZyb21KU09OKHZhbHVlOiBKU09OVmFsdWUpOiBUIHtcbiAgICAgIHJldHVybiB2YWx1ZSBhcyBUO1xuICAgIH1cbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==