(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_statedb_lib_index_js"],{

/***/ "../packages/statedb/lib/dataconnector.js":
/*!************************************************!*\
  !*** ../packages/statedb/lib/dataconnector.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DataConnector = void 0;
/**
 * An abstract class that adheres to the data connector interface.
 *
 * @typeparam T - The basic entity response type a service's connector.
 *
 * @typeparam U - The basic entity request type, which is conventionally the
 * same as the response type but may be different if a service's implementation
 * requires input data to be different from output responses. Defaults to `T`.
 *
 * @typeparam V - The basic token applied to a request, conventionally a string
 * ID or filter, but may be set to a different type when an implementation
 * requires it. Defaults to `string`.
 *
 * @typeparam W - The type of the optional `query` parameter of the `list`
 * method. Defaults to `string`.
 *
 * #### Notes
 * The only abstract method in this class is the `fetch` method, which must be
 * reimplemented by all subclasses. The `remove` and `save` methods have a
 * default implementation that returns a promise that will always reject. This
 * class is a convenience superclass for connectors that only need to `fetch`.
 */
class DataConnector {
    /**
     * Retrieve the list of items available from the data connector.
     *
     * @param query - The optional query filter to apply to the connector request.
     *
     * @returns A promise that always rejects with an error.
     *
     * #### Notes
     * Subclasses should reimplement if they support a back-end that can list.
     */
    async list(query) {
        throw new Error('DataConnector#list method has not been implemented.');
    }
    /**
     * Remove a value using the data connector.
     *
     * @param id - The identifier for the data being removed.
     *
     * @returns A promise that always rejects with an error.
     *
     * #### Notes
     * Subclasses should reimplement if they support a back-end that can remove.
     */
    async remove(id) {
        throw new Error('DataConnector#remove method has not been implemented.');
    }
    /**
     * Save a value using the data connector.
     *
     * @param id - The identifier for the data being saved.
     *
     * @param value - The data being saved.
     *
     * @returns A promise that always rejects with an error.
     *
     * #### Notes
     * Subclasses should reimplement if they support a back-end that can save.
     */
    async save(id, value) {
        throw new Error('DataConnector#save method has not been implemented.');
    }
}
exports.DataConnector = DataConnector;


/***/ }),

/***/ "../packages/statedb/lib/index.js":
/*!****************************************!*\
  !*** ../packages/statedb/lib/index.js ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module statedb
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__exportStar(__webpack_require__(/*! ./dataconnector */ "../packages/statedb/lib/dataconnector.js"), exports);
__exportStar(__webpack_require__(/*! ./interfaces */ "../packages/statedb/lib/interfaces.js"), exports);
__exportStar(__webpack_require__(/*! ./restorablepool */ "../packages/statedb/lib/restorablepool.js"), exports);
__exportStar(__webpack_require__(/*! ./statedb */ "../packages/statedb/lib/statedb.js"), exports);
__exportStar(__webpack_require__(/*! ./tokens */ "../packages/statedb/lib/tokens.js"), exports);


/***/ }),

/***/ "../packages/statedb/lib/interfaces.js":
/*!*********************************************!*\
  !*** ../packages/statedb/lib/interfaces.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));


/***/ }),

/***/ "../packages/statedb/lib/restorablepool.js":
/*!*************************************************!*\
  !*** ../packages/statedb/lib/restorablepool.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RestorablePool = void 0;
const coreutils_1 = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
const properties_1 = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
const signaling_1 = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/**
 * An object pool that supports restoration.
 *
 * @typeparam T - The type of object being tracked.
 */
class RestorablePool {
    /**
     * Create a new restorable pool.
     *
     * @param options - The instantiation options for a restorable pool.
     */
    constructor(options) {
        this._added = new signaling_1.Signal(this);
        this._current = null;
        this._currentChanged = new signaling_1.Signal(this);
        this._hasRestored = false;
        this._isDisposed = false;
        this._objects = new Set();
        this._restore = null;
        this._restored = new coreutils_1.PromiseDelegate();
        this._updated = new signaling_1.Signal(this);
        this.namespace = options.namespace;
    }
    /**
     * A signal emitted when an object object is added.
     *
     * #### Notes
     * This signal will only fire when an object is added to the pool.
     * It will not fire if an object injected into the pool.
     */
    get added() {
        return this._added;
    }
    /**
     * The current object.
     *
     * #### Notes
     * The restorable pool does not set `current`. It is intended for client use.
     *
     * If `current` is set to an object that does not exist in the pool, it is a
     * no-op.
     */
    get current() {
        return this._current;
    }
    set current(obj) {
        if (this._current === obj) {
            return;
        }
        if (obj !== null && this._objects.has(obj)) {
            this._current = obj;
            this._currentChanged.emit(this._current);
        }
    }
    /**
     * A signal emitted when the current widget changes.
     */
    get currentChanged() {
        return this._currentChanged;
    }
    /**
     * Test whether the pool is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A promise resolved when the restorable pool has been restored.
     */
    get restored() {
        return this._restored.promise;
    }
    /**
     * The number of objects held by the pool.
     */
    get size() {
        return this._objects.size;
    }
    /**
     * A signal emitted when an object is updated.
     */
    get updated() {
        return this._updated;
    }
    /**
     * Add a new object to the pool.
     *
     * @param obj - The object object being added.
     *
     * #### Notes
     * The object passed into the pool is added synchronously; its existence in
     * the pool can be checked with the `has()` method. The promise this method
     * returns resolves after the object has been added and saved to an underlying
     * restoration connector, if one is available.
     */
    async add(obj) {
        var _a, _b;
        if (obj.isDisposed) {
            const warning = 'A disposed object cannot be added.';
            console.warn(warning, obj);
            throw new Error(warning);
        }
        if (this._objects.has(obj)) {
            const warning = 'This object already exists in the pool.';
            console.warn(warning, obj);
            throw new Error(warning);
        }
        this._objects.add(obj);
        obj.disposed.connect(this._onInstanceDisposed, this);
        if (Private.injectedProperty.get(obj)) {
            return;
        }
        if (this._restore) {
            const { connector } = this._restore;
            const objName = this._restore.name(obj);
            if (objName) {
                const name = `${this.namespace}:${objName}`;
                const data = (_b = (_a = this._restore).args) === null || _b === void 0 ? void 0 : _b.call(_a, obj);
                Private.nameProperty.set(obj, name);
                await connector.save(name, { data });
            }
        }
        // Emit the added signal.
        this._added.emit(obj);
    }
    /**
     * Dispose of the resources held by the pool.
     *
     * #### Notes
     * Disposing a pool does not affect the underlying data in the data connector,
     * it simply disposes the client-side pool without making any connector calls.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._current = null;
        this._isDisposed = true;
        this._objects.clear();
        signaling_1.Signal.clearData(this);
    }
    /**
     * Find the first object in the pool that satisfies a filter function.
     *
     * @param - fn The filter function to call on each object.
     */
    find(fn) {
        const values = this._objects.values();
        for (const value of values) {
            if (fn(value)) {
                return value;
            }
        }
        return undefined;
    }
    /**
     * Iterate through each object in the pool.
     *
     * @param fn - The function to call on each object.
     */
    forEach(fn) {
        this._objects.forEach(fn);
    }
    /**
     * Filter the objects in the pool based on a predicate.
     *
     * @param fn - The function by which to filter.
     */
    filter(fn) {
        const filtered = [];
        this.forEach(obj => {
            if (fn(obj)) {
                filtered.push(obj);
            }
        });
        return filtered;
    }
    /**
     * Inject an object into the restorable pool without the pool handling its
     * restoration lifecycle.
     *
     * @param obj - The object to inject into the pool.
     */
    inject(obj) {
        Private.injectedProperty.set(obj, true);
        return this.add(obj);
    }
    /**
     * Check if this pool has the specified object.
     *
     * @param obj - The object whose existence is being checked.
     */
    has(obj) {
        return this._objects.has(obj);
    }
    /**
     * Restore the objects in this pool's namespace.
     *
     * @param options - The configuration options that describe restoration.
     *
     * @returns A promise that resolves when restoration has completed.
     *
     * #### Notes
     * This function should almost never be invoked by client code. Its primary
     * use case is to be invoked by a layout restorer plugin that handles
     * multiple restorable pools and, when ready, asks them each to restore their
     * respective objects.
     */
    async restore(options) {
        if (this._hasRestored) {
            throw new Error('This pool has already been restored.');
        }
        this._hasRestored = true;
        const { command, connector, registry, when } = options;
        const namespace = this.namespace;
        const promises = when
            ? [connector.list(namespace)].concat(when)
            : [connector.list(namespace)];
        this._restore = options;
        const [saved] = await Promise.all(promises);
        const values = await Promise.all(saved.ids.map(async (id, index) => {
            const value = saved.values[index];
            const args = value && value.data;
            if (args === undefined) {
                return connector.remove(id);
            }
            // Execute the command and if it fails, delete the state restore data.
            return registry
                .execute(command, args)
                .catch(() => connector.remove(id));
        }));
        this._restored.resolve();
        return values;
    }
    /**
     * Save the restore data for a given object.
     *
     * @param obj - The object being saved.
     */
    async save(obj) {
        var _a, _b;
        const injected = Private.injectedProperty.get(obj);
        if (!this._restore || !this.has(obj) || injected) {
            return;
        }
        const { connector } = this._restore;
        const objName = this._restore.name(obj);
        const oldName = Private.nameProperty.get(obj);
        const newName = objName ? `${this.namespace}:${objName}` : '';
        if (oldName && oldName !== newName) {
            await connector.remove(oldName);
        }
        // Set the name property irrespective of whether the new name is null.
        Private.nameProperty.set(obj, newName);
        if (newName) {
            const data = (_b = (_a = this._restore).args) === null || _b === void 0 ? void 0 : _b.call(_a, obj);
            await connector.save(newName, { data });
        }
        if (oldName !== newName) {
            this._updated.emit(obj);
        }
    }
    /**
     * Clean up after disposed objects.
     */
    _onInstanceDisposed(obj) {
        this._objects.delete(obj);
        if (obj === this._current) {
            this._current = null;
            this._currentChanged.emit(this._current);
        }
        if (Private.injectedProperty.get(obj)) {
            return;
        }
        if (!this._restore) {
            return;
        }
        const { connector } = this._restore;
        const name = Private.nameProperty.get(obj);
        if (name) {
            void connector.remove(name);
        }
    }
}
exports.RestorablePool = RestorablePool;
/*
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property to indicate whether an object has been injected.
     */
    Private.injectedProperty = new properties_1.AttachedProperty({
        name: 'injected',
        create: () => false
    });
    /**
     * An attached property for an object's ID.
     */
    Private.nameProperty = new properties_1.AttachedProperty({
        name: 'name',
        create: () => ''
    });
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/statedb/lib/statedb.js":
/*!******************************************!*\
  !*** ../packages/statedb/lib/statedb.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.StateDB = void 0;
const signaling_1 = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/**
 * The default concrete implementation of a state database.
 */
class StateDB {
    /**
     * Create a new state database.
     *
     * @param options - The instantiation options for a state database.
     */
    constructor(options = {}) {
        this._changed = new signaling_1.Signal(this);
        const { connector, transform } = options;
        this._connector = connector || new StateDB.Connector();
        if (!transform) {
            this._ready = Promise.resolve(undefined);
        }
        else {
            this._ready = transform.then(transformation => {
                const { contents, type } = transformation;
                switch (type) {
                    case 'cancel':
                        return;
                    case 'clear':
                        return this._clear();
                    case 'merge':
                        return this._merge(contents || {});
                    case 'overwrite':
                        return this._overwrite(contents || {});
                    default:
                        return;
                }
            });
        }
    }
    /**
     * A signal that emits the change type any time a value changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Clear the entire database.
     */
    async clear() {
        await this._ready;
        await this._clear();
    }
    /**
     * Retrieve a saved bundle from the database.
     *
     * @param id - The identifier used to retrieve a data bundle.
     *
     * @returns A promise that bears a data payload if available.
     *
     * #### Notes
     * The `id` values of stored items in the state database are formatted:
     * `'namespace:identifier'`, which is the same convention that command
     * identifiers in JupyterLab use as well. While this is not a technical
     * requirement for `fetch()`, `remove()`, and `save()`, it *is* necessary for
     * using the `list(namespace: string)` method.
     *
     * The promise returned by this method may be rejected if an error occurs in
     * retrieving the data. Non-existence of an `id` will succeed with the `value`
     * `undefined`.
     */
    async fetch(id) {
        await this._ready;
        return this._fetch(id);
    }
    /**
     * Retrieve all the saved bundles for a namespace.
     *
     * @param filter - The namespace prefix to retrieve.
     *
     * @returns A promise that bears a collection of payloads for a namespace.
     *
     * #### Notes
     * Namespaces are entirely conventional entities. The `id` values of stored
     * items in the state database are formatted: `'namespace:identifier'`, which
     * is the same convention that command identifiers in JupyterLab use as well.
     *
     * If there are any errors in retrieving the data, they will be logged to the
     * console in order to optimistically return any extant data without failing.
     * This promise will always succeed.
     */
    async list(namespace) {
        await this._ready;
        return this._list(namespace);
    }
    /**
     * Remove a value from the database.
     *
     * @param id - The identifier for the data being removed.
     *
     * @returns A promise that is rejected if remove fails and succeeds otherwise.
     */
    async remove(id) {
        await this._ready;
        await this._remove(id);
        this._changed.emit({ id, type: 'remove' });
    }
    /**
     * Save a value in the database.
     *
     * @param id - The identifier for the data being saved.
     *
     * @param value - The data being saved.
     *
     * @returns A promise that is rejected if saving fails and succeeds otherwise.
     *
     * #### Notes
     * The `id` values of stored items in the state database are formatted:
     * `'namespace:identifier'`, which is the same convention that command
     * identifiers in JupyterLab use as well. While this is not a technical
     * requirement for `fetch()`, `remove()`, and `save()`, it *is* necessary for
     * using the `list(namespace: string)` method.
     */
    async save(id, value) {
        await this._ready;
        await this._save(id, value);
        this._changed.emit({ id, type: 'save' });
    }
    /**
     * Return a serialized copy of the state database's entire contents.
     *
     * @returns A promise that resolves with the database contents as JSON.
     */
    async toJSON() {
        await this._ready;
        const { ids, values } = await this._list();
        return values.reduce((acc, val, idx) => {
            acc[ids[idx]] = val;
            return acc;
        }, {});
    }
    /**
     * Clear the entire database.
     */
    async _clear() {
        await Promise.all((await this._list()).ids.map(id => this._remove(id)));
    }
    /**
     * Fetch a value from the database.
     */
    async _fetch(id) {
        const value = await this._connector.fetch(id);
        if (value) {
            return JSON.parse(value).v;
        }
    }
    /**
     * Fetch a list from the database.
     */
    async _list(namespace = '') {
        const { ids, values } = await this._connector.list(namespace);
        return {
            ids,
            values: values.map(val => JSON.parse(val).v)
        };
    }
    /**
     * Merge data into the state database.
     */
    async _merge(contents) {
        await Promise.all(Object.keys(contents).map(key => contents[key] && this._save(key, contents[key])));
    }
    /**
     * Overwrite the entire database with new contents.
     */
    async _overwrite(contents) {
        await this._clear();
        await this._merge(contents);
    }
    /**
     * Remove a key in the database.
     */
    async _remove(id) {
        return this._connector.remove(id);
    }
    /**
     * Save a key and its value in the database.
     */
    async _save(id, value) {
        return this._connector.save(id, JSON.stringify({ v: value }));
    }
}
exports.StateDB = StateDB;
/**
 * A namespace for StateDB statics.
 */
(function (StateDB) {
    /**
     * An in-memory string key/value data connector.
     */
    class Connector {
        constructor() {
            this._storage = {};
        }
        /**
         * Retrieve an item from the data connector.
         */
        async fetch(id) {
            return this._storage[id];
        }
        /**
         * Retrieve the list of items available from the data connector.
         *
         * @param namespace - If not empty, only keys whose first token before `:`
         * exactly match `namespace` will be returned, e.g. `foo` in `foo:bar`.
         */
        async list(namespace = '') {
            return Object.keys(this._storage).reduce((acc, val) => {
                if (namespace === '' ? true : namespace === val.split(':')[0]) {
                    acc.ids.push(val);
                    acc.values.push(this._storage[val]);
                }
                return acc;
            }, { ids: [], values: [] });
        }
        /**
         * Remove a value using the data connector.
         */
        async remove(id) {
            delete this._storage[id];
        }
        /**
         * Save a value using the data connector.
         */
        async save(id, value) {
            this._storage[id] = value;
        }
    }
    StateDB.Connector = Connector;
})(StateDB = exports.StateDB || (exports.StateDB = {}));


/***/ }),

/***/ "../packages/statedb/lib/tokens.js":
/*!*****************************************!*\
  !*** ../packages/statedb/lib/tokens.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.IStateDB = void 0;
const coreutils_1 = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* tslint:disable */
/**
 * The default state database token.
 */
exports.IStateDB = new coreutils_1.Token('@jupyterlab/coreutils:IStateDB');


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdGVkYi9zcmMvZGF0YWNvbm5lY3Rvci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdGVkYi9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXRlZGIvc3JjL2ludGVyZmFjZXMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXRlZGIvc3JjL3Jlc3RvcmFibGVwb29sLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0ZWRiL3NyYy9zdGF0ZWRiLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0ZWRiL3NyYy90b2tlbnMudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7OztBQUkzRDs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0dBcUJHO0FBQ0gsTUFBc0IsYUFBYTtJQWVqQzs7Ozs7Ozs7O09BU0c7SUFDSCxLQUFLLENBQUMsSUFBSSxDQUFDLEtBQVM7UUFDbEIsTUFBTSxJQUFJLEtBQUssQ0FBQyxxREFBcUQsQ0FBQyxDQUFDO0lBQ3pFLENBQUM7SUFFRDs7Ozs7Ozs7O09BU0c7SUFDSCxLQUFLLENBQUMsTUFBTSxDQUFDLEVBQUs7UUFDaEIsTUFBTSxJQUFJLEtBQUssQ0FBQyx1REFBdUQsQ0FBQyxDQUFDO0lBQzNFLENBQUM7SUFFRDs7Ozs7Ozs7Ozs7T0FXRztJQUNILEtBQUssQ0FBQyxJQUFJLENBQUMsRUFBSyxFQUFFLEtBQVE7UUFDeEIsTUFBTSxJQUFJLEtBQUssQ0FBQyxxREFBcUQsQ0FBQyxD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SUFBSSxDQUFDLFFBQVEsQ0FBQyxFQUFFLENBQUMsR0FBRyxLQUFLLENBQUM7UUFDNUIsQ0FBQztLQUdGO0lBMUNZLGlCQUFTLFlBMENyQjtBQUNILENBQUMsRUExR2dCLE9BQU8sR0FBUCxlQUFPLEtBQVAsZUFBTyxRQTBHdkI7Ozs7Ozs7Ozs7Ozs7QUM1VUQsMENBQTBDO0FBQzFDLDJEQUEyRDs7O0FBRTNELHdJQUFvRTtBQUdwRSxvQkFBb0I7QUFDcEI7O0dBRUc7QUFDVSxnQkFBUSxHQUFHLElBQUksaUJBQUssQ0FBVyxnQ0FBZ0MsQ0FBQyxDQUFDIiwiZmlsZSI6InBhY2thZ2VzX3N0YXRlZGJfbGliX2luZGV4X2pzLjc3OWMwZmQxMzg0YjM0YTYyYTViLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJRGF0YUNvbm5lY3RvciB9IGZyb20gJy4vaW50ZXJmYWNlcyc7XG5cbi8qKlxuICogQW4gYWJzdHJhY3QgY2xhc3MgdGhhdCBhZGhlcmVzIHRvIHRoZSBkYXRhIGNvbm5lY3RvciBpbnRlcmZhY2UuXG4gKlxuICogQHR5cGVwYXJhbSBUIC0gVGhlIGJhc2ljIGVudGl0eSByZXNwb25zZSB0eXBlIGEgc2VydmljZSdzIGNvbm5lY3Rvci5cbiAqXG4gKiBAdHlwZXBhcmFtIFUgLSBUaGUgYmFzaWMgZW50aXR5IHJlcXVlc3QgdHlwZSwgd2hpY2ggaXMgY29udmVudGlvbmFsbHkgdGhlXG4gKiBzYW1lIGFzIHRoZSByZXNwb25zZSB0eXBlIGJ1dCBtYXkgYmUgZGlmZmVyZW50IGlmIGEgc2VydmljZSdzIGltcGxlbWVudGF0aW9uXG4gKiByZXF1aXJlcyBpbnB1dCBkYXRhIHRvIGJlIGRpZmZlcmVudCBmcm9tIG91dHB1dCByZXNwb25zZXMuIERlZmF1bHRzIHRvIGBUYC5cbiAqXG4gKiBAdHlwZXBhcmFtIFYgLSBUaGUgYmFzaWMgdG9rZW4gYXBwbGllZCB0byBhIHJlcXVlc3QsIGNvbnZlbnRpb25hbGx5IGEgc3RyaW5nXG4gKiBJRCBvciBmaWx0ZXIsIGJ1dCBtYXkgYmUgc2V0IHRvIGEgZGlmZmVyZW50IHR5cGUgd2hlbiBhbiBpbXBsZW1lbnRhdGlvblxuICogcmVxdWlyZXMgaXQuIERlZmF1bHRzIHRvIGBzdHJpbmdgLlxuICpcbiAqIEB0eXBlcGFyYW0gVyAtIFRoZSB0eXBlIG9mIHRoZSBvcHRpb25hbCBgcXVlcnlgIHBhcmFtZXRlciBvZiB0aGUgYGxpc3RgXG4gKiBtZXRob2QuIERlZmF1bHRzIHRvIGBzdHJpbmdgLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIFRoZSBvbmx5IGFic3RyYWN0IG1ldGhvZCBpbiB0aGlzIGNsYXNzIGlzIHRoZSBgZmV0Y2hgIG1ldGhvZCwgd2hpY2ggbXVzdCBiZVxuICogcmVpbXBsZW1lbnRlZCBieSBhbGwgc3ViY2xhc3Nlcy4gVGhlIGByZW1vdmVgIGFuZCBgc2F2ZWAgbWV0aG9kcyBoYXZlIGFcbiAqIGRlZmF1bHQgaW1wbGVtZW50YXRpb24gdGhhdCByZXR1cm5zIGEgcHJvbWlzZSB0aGF0IHdpbGwgYWx3YXlzIHJlamVjdC4gVGhpc1xuICogY2xhc3MgaXMgYSBjb252ZW5pZW5jZSBzdXBlcmNsYXNzIGZvciBjb25uZWN0b3JzIHRoYXQgb25seSBuZWVkIHRvIGBmZXRjaGAuXG4gKi9cbmV4cG9ydCBhYnN0cmFjdCBjbGFzcyBEYXRhQ29ubmVjdG9yPFQsIFUgPSBULCBWID0gc3RyaW5nLCBXID0gc3RyaW5nPlxuICBpbXBsZW1lbnRzIElEYXRhQ29ubmVjdG9yPFQsIFUsIFYsIFc+IHtcbiAgLyoqXG4gICAqIFJldHJpZXZlIGFuIGl0ZW0gZnJvbSB0aGUgZGF0YSBjb25uZWN0b3IuXG4gICAqXG4gICAqIEBwYXJhbSBpZCAtIFRoZSBpZGVudGlmaWVyIHVzZWQgdG8gcmV0cmlldmUgYW4gaXRlbS5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2l0aCBhIGRhdGEgcGF5bG9hZCBpZiBhdmFpbGFibGUuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIHByb21pc2UgcmV0dXJuZWQgYnkgdGhpcyBtZXRob2QgbWF5IGJlIHJlamVjdGVkIGlmIGFuIGVycm9yIG9jY3VycyBpblxuICAgKiByZXRyaWV2aW5nIHRoZSBkYXRhLiBOb25leGlzdGVuY2Ugb2YgYW4gYGlkYCB3aWxsIHN1Y2NlZWQgd2l0aCBgdW5kZWZpbmVkYC5cbiAgICovXG4gIGFic3RyYWN0IGZldGNoKGlkOiBWKTogUHJvbWlzZTxUIHwgdW5kZWZpbmVkPjtcblxuICAvKipcbiAgICogUmV0cmlldmUgdGhlIGxpc3Qgb2YgaXRlbXMgYXZhaWxhYmxlIGZyb20gdGhlIGRhdGEgY29ubmVjdG9yLlxuICAgKlxuICAgKiBAcGFyYW0gcXVlcnkgLSBUaGUgb3B0aW9uYWwgcXVlcnkgZmlsdGVyIHRvIGFwcGx5IHRvIHRoZSBjb25uZWN0b3IgcmVxdWVzdC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgYWx3YXlzIHJlamVjdHMgd2l0aCBhbiBlcnJvci5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBTdWJjbGFzc2VzIHNob3VsZCByZWltcGxlbWVudCBpZiB0aGV5IHN1cHBvcnQgYSBiYWNrLWVuZCB0aGF0IGNhbiBsaXN0LlxuICAgKi9cbiAgYXN5bmMgbGlzdChxdWVyeT86IFcpOiBQcm9taXNlPHsgaWRzOiBWW107IHZhbHVlczogVFtdIH0+IHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoJ0RhdGFDb25uZWN0b3IjbGlzdCBtZXRob2QgaGFzIG5vdCBiZWVuIGltcGxlbWVudGVkLicpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhIHZhbHVlIHVzaW5nIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICpcbiAgICogQHBhcmFtIGlkIC0gVGhlIGlkZW50aWZpZXIgZm9yIHRoZSBkYXRhIGJlaW5nIHJlbW92ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGFsd2F5cyByZWplY3RzIHdpdGggYW4gZXJyb3IuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogU3ViY2xhc3NlcyBzaG91bGQgcmVpbXBsZW1lbnQgaWYgdGhleSBzdXBwb3J0IGEgYmFjay1lbmQgdGhhdCBjYW4gcmVtb3ZlLlxuICAgKi9cbiAgYXN5bmMgcmVtb3ZlKGlkOiBWKTogUHJvbWlzZTxhbnk+IHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoJ0RhdGFDb25uZWN0b3IjcmVtb3ZlIG1ldGhvZCBoYXMgbm90IGJlZW4gaW1wbGVtZW50ZWQuJyk7XG4gIH1cblxuICAvKipcbiAgICogU2F2ZSBhIHZhbHVlIHVzaW5nIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICpcbiAgICogQHBhcmFtIGlkIC0gVGhlIGlkZW50aWZpZXIgZm9yIHRoZSBkYXRhIGJlaW5nIHNhdmVkLlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgZGF0YSBiZWluZyBzYXZlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgYWx3YXlzIHJlamVjdHMgd2l0aCBhbiBlcnJvci5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBTdWJjbGFzc2VzIHNob3VsZCByZWltcGxlbWVudCBpZiB0aGV5IHN1cHBvcnQgYSBiYWNrLWVuZCB0aGF0IGNhbiBzYXZlLlxuICAgKi9cbiAgYXN5bmMgc2F2ZShpZDogViwgdmFsdWU6IFUpOiBQcm9taXNlPGFueT4ge1xuICAgIHRocm93IG5ldyBFcnJvcignRGF0YUNvbm5lY3RvciNzYXZlIG1ldGhvZCBoYXMgbm90IGJlZW4gaW1wbGVtZW50ZWQuJyk7XG4gIH1cbn1cbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgc3RhdGVkYlxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vZGF0YWNvbm5lY3Rvcic7XG5leHBvcnQgKiBmcm9tICcuL2ludGVyZmFjZXMnO1xuZXhwb3J0ICogZnJvbSAnLi9yZXN0b3JhYmxlcG9vbCc7XG5leHBvcnQgKiBmcm9tICcuL3N0YXRlZGInO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBDb21tYW5kUmVnaXN0cnkgfSBmcm9tICdAbHVtaW5vL2NvbW1hbmRzJztcbmltcG9ydCB7XG4gIFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3QsXG4gIFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZVxufSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJRGlzcG9zYWJsZSwgSU9ic2VydmFibGVEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5cbi8qKlxuICogVGhlIGRlc2NyaXB0aW9uIG9mIGEgZ2VuZXJhbCBwdXJwb3NlIGRhdGEgY29ubmVjdG9yLlxuICpcbiAqIEB0eXBlcGFyYW0gVCAtIFRoZSBiYXNpYyBlbnRpdHkgcmVzcG9uc2UgdHlwZSBhIHNlcnZpY2UncyBjb25uZWN0b3IuXG4gKlxuICogQHR5cGVwYXJhbSBVIC0gVGhlIGJhc2ljIGVudGl0eSByZXF1ZXN0IHR5cGUsIHdoaWNoIGlzIGNvbnZlbnRpb25hbGx5IHRoZVxuICogc2FtZSBhcyB0aGUgcmVzcG9uc2UgdHlwZSBidXQgbWF5IGJlIGRpZmZlcmVudCBpZiBhIHNlcnZpY2UncyBpbXBsZW1lbnRhdGlvblxuICogcmVxdWlyZXMgaW5wdXQgZGF0YSB0byBiZSBkaWZmZXJlbnQgZnJvbSBvdXRwdXQgcmVzcG9uc2VzLiBEZWZhdWx0cyB0byBgVGAuXG4gKlxuICogQHR5cGVwYXJhbSBWIC0gVGhlIGJhc2ljIHRva2VuIGFwcGxpZWQgdG8gYSByZXF1ZXN0LCBjb252ZW50aW9uYWxseSBhIHN0cmluZ1xuICogSUQgb3IgZmlsdGVyLCBidXQgbWF5IGJlIHNldCB0byBhIGRpZmZlcmVudCB0eXBlIHdoZW4gYW4gaW1wbGVtZW50YXRpb25cbiAqIHJlcXVpcmVzIGl0LiBEZWZhdWx0cyB0byBgc3RyaW5nYC5cbiAqXG4gKiBAdHlwZXBhcmFtIFcgLSBUaGUgdHlwZSBvZiB0aGUgb3B0aW9uYWwgYHF1ZXJ5YCBwYXJhbWV0ZXIgb2YgdGhlIGBsaXN0YFxuICogbWV0aG9kLiBEZWZhdWx0cyB0byBgc3RyaW5nYDtcbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJRGF0YUNvbm5lY3RvcjxULCBVID0gVCwgViA9IHN0cmluZywgVyA9IHN0cmluZz4ge1xuICAvKipcbiAgICogUmV0cmlldmUgYW4gaXRlbSBmcm9tIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICpcbiAgICogQHBhcmFtIGlkIC0gVGhlIGlkZW50aWZpZXIgdXNlZCB0byByZXRyaWV2ZSBhbiBpdGVtLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBiZWFycyBhIGRhdGEgcGF5bG9hZCBpZiBhdmFpbGFibGUuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIHByb21pc2UgcmV0dXJuZWQgYnkgdGhpcyBtZXRob2QgbWF5IGJlIHJlamVjdGVkIGlmIGFuIGVycm9yIG9jY3VycyBpblxuICAgKiByZXRyaWV2aW5nIHRoZSBkYXRhLiBOb25leGlzdGVuY2Ugb2YgYW4gYGlkYCByZXNvbHZlcyB3aXRoIGB1bmRlZmluZWRgLlxuICAgKi9cbiAgZmV0Y2goaWQ6IFYpOiBQcm9taXNlPFQgfCB1bmRlZmluZWQ+O1xuXG4gIC8qKlxuICAgKiBSZXRyaWV2ZSB0aGUgbGlzdCBvZiBpdGVtcyBhdmFpbGFibGUgZnJvbSB0aGUgZGF0YSBjb25uZWN0b3IuXG4gICAqXG4gICAqIEBwYXJhbSBxdWVyeSAtIFRoZSBvcHRpb25hbCBxdWVyeSBmaWx0ZXIgdG8gYXBwbHkgdG8gdGhlIGNvbm5lY3RvciByZXF1ZXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBiZWFycyBhIGxpc3Qgb2YgYHZhbHVlc2AgYW5kIGFuIGFzc29jaWF0ZWQgbGlzdCBvZlxuICAgKiBmZXRjaCBgaWRzYC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgcHJvbWlzZSByZXR1cm5lZCBieSB0aGlzIG1ldGhvZCBtYXkgYmUgcmVqZWN0ZWQgaWYgYW4gZXJyb3Igb2NjdXJzIGluXG4gICAqIHJldHJpZXZpbmcgdGhlIGRhdGEuIFRoZSB0d28gbGlzdHMgd2lsbCBhbHdheXMgYmUgdGhlIHNhbWUgc2l6ZS4gSWYgdGhlcmVcbiAgICogaXMgbm8gZGF0YSwgdGhpcyBtZXRob2Qgd2lsbCBzdWNjZWVkIHdpdGggZW1wdHkgYGlkc2AgYW5kIGB2YWx1ZXNgLlxuICAgKi9cbiAgbGlzdChxdWVyeT86IFcpOiBQcm9taXNlPHsgaWRzOiBWW107IHZhbHVlczogVFtdIH0+O1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSB2YWx1ZSB1c2luZyB0aGUgZGF0YSBjb25uZWN0b3IuXG4gICAqXG4gICAqIEBwYXJhbSBpZCAtIFRoZSBpZGVudGlmaWVyIGZvciB0aGUgZGF0YSBiZWluZyByZW1vdmVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBpcyByZWplY3RlZCBpZiByZW1vdmUgZmFpbHMgYW5kIHN1Y2NlZWRzIG90aGVyd2lzZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIHByb21pc2UgbWF5IHJlc29sdmUgd2l0aCBhIGJhY2stZW5kIHJlc3BvbnNlIG9yIGB1bmRlZmluZWRgLlxuICAgKiBFeGlzdGVuY2Ugb2YgcmVzb2x2ZWQgY29udGVudCBpbiB0aGUgcHJvbWlzZSBpcyBub3QgcHJlc2NyaWJlZCBhbmQgbXVzdCBiZVxuICAgKiB0ZXN0ZWQgZm9yLiBGb3IgZXhhbXBsZSwgc29tZSBiYWNrLWVuZHMgbWF5IHJldHVybiBhIGNvcHkgb2YgdGhlIGl0ZW0gb2ZcbiAgICogdHlwZSBgVGAgYmVpbmcgcmVtb3ZlZCB3aGlsZSBvdGhlcnMgbWF5IHJldHVybiBubyBjb250ZW50LlxuICAgKi9cbiAgcmVtb3ZlKGlkOiBWKTogUHJvbWlzZTxhbnk+O1xuXG4gIC8qKlxuICAgKiBTYXZlIGEgdmFsdWUgdXNpbmcgdGhlIGRhdGEgY29ubmVjdG9yLlxuICAgKlxuICAgKiBAcGFyYW0gaWQgLSBUaGUgaWRlbnRpZmllciBmb3IgdGhlIGRhdGEgYmVpbmcgc2F2ZWQuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSBkYXRhIGJlaW5nIHNhdmVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBpcyByZWplY3RlZCBpZiBzYXZpbmcgZmFpbHMgYW5kIHN1Y2NlZWRzIG90aGVyd2lzZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIHByb21pc2UgbWF5IHJlc29sdmUgd2l0aCBhIGJhY2stZW5kIHJlc3BvbnNlIG9yIGB1bmRlZmluZWRgLlxuICAgKiBFeGlzdGVuY2Ugb2YgcmVzb2x2ZWQgY29udGVudCBpbiB0aGUgcHJvbWlzZSBpcyBub3QgcHJlc2NyaWJlZCBhbmQgbXVzdCBiZVxuICAgKiB0ZXN0ZWQgZm9yLiBGb3IgZXhhbXBsZSwgc29tZSBiYWNrLWVuZHMgbWF5IHJldHVybiBhIGNvcHkgb2YgdGhlIGl0ZW0gb2ZcbiAgICogdHlwZSBgVGAgYmVpbmcgc2F2ZWQgd2hpbGUgb3RoZXJzIG1heSByZXR1cm4gbm8gY29udGVudC5cbiAgICovXG4gIHNhdmUoaWQ6IFYsIHZhbHVlOiBVKTogUHJvbWlzZTxhbnk+O1xufVxuXG4vKipcbiAqIEEgcG9vbCBvZiBvYmplY3RzIHdob3NlIGRpc3Bvc2FibGUgbGlmZWN5Y2xlIGlzIHRyYWNrZWQuXG4gKlxuICogQHR5cGVwYXJhbSBUIC0gVGhlIHR5cGUgb2Ygb2JqZWN0IGhlbGQgaW4gdGhlIHBvb2wuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU9iamVjdFBvb2w8VCBleHRlbmRzIElPYnNlcnZhYmxlRGlzcG9zYWJsZT5cbiAgZXh0ZW5kcyBJRGlzcG9zYWJsZSB7XG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gYW4gb2JqZWN0IGlzIGFkZGVkLlxuICAgKlxuICAgKiAjIyMjXG4gICAqIFRoaXMgc2lnbmFsIGRvZXMgbm90IGVtaXQgaWYgYW4gb2JqZWN0IGlzIGFkZGVkIHVzaW5nIGBpbmplY3QoKWAuXG4gICAqL1xuICByZWFkb25seSBhZGRlZDogSVNpZ25hbDx0aGlzLCBUPjtcblxuICAvKipcbiAgICogVGhlIGN1cnJlbnQgb2JqZWN0LlxuICAgKi9cbiAgcmVhZG9ubHkgY3VycmVudDogVCB8IG51bGw7XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgY3VycmVudCBvYmplY3QgY2hhbmdlcy5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBJZiB0aGUgbGFzdCBvYmplY3QgYmVpbmcgdHJhY2tlZCBpcyBkaXNwb3NlZCwgYG51bGxgIHdpbGwgYmUgZW1pdHRlZC5cbiAgICovXG4gIHJlYWRvbmx5IGN1cnJlbnRDaGFuZ2VkOiBJU2lnbmFsPHRoaXMsIFQgfCBudWxsPjtcblxuICAvKipcbiAgICogVGhlIG51bWJlciBvZiBvYmplY3RzIGhlbGQgYnkgdGhlIHBvb2wuXG4gICAqL1xuICByZWFkb25seSBzaXplOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBhbiBvYmplY3QgaXMgdXBkYXRlZC5cbiAgICovXG4gIHJlYWRvbmx5IHVwZGF0ZWQ6IElTaWduYWw8dGhpcywgVD47XG5cbiAgLyoqXG4gICAqIEZpbmQgdGhlIGZpcnN0IG9iamVjdCBpbiB0aGUgcG9vbCB0aGF0IHNhdGlzZmllcyBhIGZpbHRlciBmdW5jdGlvbi5cbiAgICpcbiAgICogQHBhcmFtIC0gZm4gVGhlIGZpbHRlciBmdW5jdGlvbiB0byBjYWxsIG9uIGVhY2ggb2JqZWN0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIElmIG5vdGhpbmcgaXMgZm91bmQsIHRoZSB2YWx1ZSByZXR1cm5lZCBpcyBgdW5kZWZpbmVkYC5cbiAgICovXG4gIGZpbmQoZm46IChvYmo6IFQpID0+IGJvb2xlYW4pOiBUIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBJdGVyYXRlIHRocm91Z2ggZWFjaCBvYmplY3QgaW4gdGhlIHBvb2wuXG4gICAqXG4gICAqIEBwYXJhbSBmbiAtIFRoZSBmdW5jdGlvbiB0byBjYWxsIG9uIGVhY2ggb2JqZWN0LlxuICAgKi9cbiAgZm9yRWFjaChmbjogKG9iajogVCkgPT4gdm9pZCk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIEZpbHRlciB0aGUgb2JqZWN0cyBpbiB0aGUgcG9vbCBiYXNlZCBvbiBhIHByZWRpY2F0ZS5cbiAgICpcbiAgICogQHBhcmFtIGZuIC0gVGhlIGZ1bmN0aW9uIGJ5IHdoaWNoIHRvIGZpbHRlci5cbiAgICovXG4gIGZpbHRlcihmbjogKG9iajogVCkgPT4gYm9vbGVhbik6IFRbXTtcblxuICAvKipcbiAgICogQ2hlY2sgaWYgdGhpcyBwb29sIGhhcyB0aGUgc3BlY2lmaWVkIG9iamVjdC5cbiAgICpcbiAgICogQHBhcmFtIG9iaiAtIFRoZSBvYmplY3Qgd2hvc2UgZXhpc3RlbmNlIGlzIGJlaW5nIGNoZWNrZWQuXG4gICAqL1xuICBoYXMob2JqOiBUKTogYm9vbGVhbjtcbn1cblxuLyoqXG4gKiBBbiBpbnRlcmZhY2UgZm9yIGEgc3RhdGUgcmVzdG9yZXIuXG4gKlxuICogQHR5cGVwYXJhbSBUIC0gVGhlIHJlc3RvcmFibGUgY29sbGVjdGlvbidzIHR5cGUuXG4gKlxuICogQHR5cGVwYXJhbSBVIC0gVGhlIHR5cGUgb2Ygb2JqZWN0IGhlbGQgYnkgdGhlIHJlc3RvcmFibGUgY29sbGVjdGlvbi5cbiAqXG4gKiBAdHlwZXBhcmFtIFYgLSBUaGUgYHJlc3RvcmVkYCBwcm9taXNlIHJlc29sdXRpb24gdHlwZS4gRGVmYXVsdHMgdG8gYGFueWAuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVJlc3RvcmVyPFxuICBUIGV4dGVuZHMgSVJlc3RvcmFibGU8VT4gPSBJUmVzdG9yYWJsZTxJT2JzZXJ2YWJsZURpc3Bvc2FibGU+LFxuICBVIGV4dGVuZHMgSU9ic2VydmFibGVEaXNwb3NhYmxlID0gSU9ic2VydmFibGVEaXNwb3NhYmxlLFxuICBWID0gYW55XG4+IHtcbiAgLyoqXG4gICAqIFJlc3RvcmUgdGhlIG9iamVjdHMgaW4gYSBnaXZlbiByZXN0b3JhYmxlIGNvbGxlY3Rpb24uXG4gICAqXG4gICAqIEBwYXJhbSByZXN0b3JhYmxlIC0gVGhlIHJlc3RvcmFibGUgY29sbGVjdGlvbiBiZWluZyByZXN0b3JlZC5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgY29uZmlndXJhdGlvbiBvcHRpb25zIHRoYXQgZGVzY3JpYmUgcmVzdG9yYXRpb24uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHNldHRsZXMgd2hlbiByZXN0b3JlZCB3aXRoIGBhbnlgIHJlc3VsdHMuXG4gICAqXG4gICAqL1xuICByZXN0b3JlKHJlc3RvcmFibGU6IFQsIG9wdGlvbnM6IElSZXN0b3JhYmxlLklPcHRpb25zPFU+KTogUHJvbWlzZTxWPjtcblxuICAvKipcbiAgICogQSBwcm9taXNlIHRoYXQgc2V0dGxlcyB3aGVuIHRoZSBjb2xsZWN0aW9uIGhhcyBiZWVuIHJlc3RvcmVkLlxuICAgKi9cbiAgcmVhZG9ubHkgcmVzdG9yZWQ6IFByb21pc2U8Vj47XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGBJUmVzdG9yZXJgIGludGVyZmFjZSBkZWZpbml0aW9ucy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJUmVzdG9yZXIge1xuICAvKipcbiAgICogVGhlIHN0YXRlIHJlc3RvcmF0aW9uIGNvbmZpZ3VyYXRpb24gb3B0aW9ucy5cbiAgICpcbiAgICogQHR5cGVwYXJhbSBUIC0gVGhlIHR5cGUgb2Ygb2JqZWN0IGhlbGQgYnkgdGhlIHJlc3RvcmFibGUgY29sbGVjdGlvbi5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnM8VCBleHRlbmRzIElPYnNlcnZhYmxlRGlzcG9zYWJsZT4ge1xuICAgIC8qKlxuICAgICAqIFRoZSBjb21tYW5kIHRvIGV4ZWN1dGUgd2hlbiByZXN0b3JpbmcgaW5zdGFuY2VzLlxuICAgICAqL1xuICAgIGNvbW1hbmQ6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEEgZnVuY3Rpb24gdGhhdCByZXR1cm5zIHRoZSBhcmdzIG5lZWRlZCB0byByZXN0b3JlIGFuIGluc3RhbmNlLlxuICAgICAqL1xuICAgIGFyZ3M/OiAob2JqOiBUKSA9PiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0aGF0IHJldHVybnMgYSB1bmlxdWUgcGVyc2lzdGVudCBuYW1lIGZvciB0aGlzIGluc3RhbmNlLlxuICAgICAqL1xuICAgIG5hbWU6IChvYmo6IFQpID0+IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBwb2ludCBhZnRlciB3aGljaCBpdCBpcyBzYWZlIHRvIHJlc3RvcmUgc3RhdGUuXG4gICAgICovXG4gICAgd2hlbj86IFByb21pc2U8YW55PiB8IEFycmF5PFByb21pc2U8YW55Pj47XG4gIH1cbn1cblxuLyoqXG4gKiBBbiBpbnRlcmZhY2UgZm9yIG9iamVjdHMgdGhhdCBjYW4gYmUgcmVzdG9yZWQuXG4gKlxuICogQHR5cGVwYXJhbSBUIC0gVGhlIHR5cGUgb2Ygb2JqZWN0IGhlbGQgYnkgdGhlIHJlc3RvcmFibGUgY29sbGVjdGlvbi5cbiAqXG4gKiBAdHlwZXBhcmFtIFUgLSBUaGUgYHJlc3RvcmVkYCBwcm9taXNlIHJlc29sdXRpb24gdHlwZS4gRGVmYXVsdHMgdG8gYGFueWAuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVJlc3RvcmFibGU8VCBleHRlbmRzIElPYnNlcnZhYmxlRGlzcG9zYWJsZSwgVSA9IGFueT4ge1xuICAvKipcbiAgICogUmVzdG9yZSB0aGUgb2JqZWN0cyBpbiB0aGlzIHJlc3RvcmFibGUgY29sbGVjdGlvbi5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgY29uZmlndXJhdGlvbiBvcHRpb25zIHRoYXQgZGVzY3JpYmUgcmVzdG9yYXRpb24uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHNldHRsZXMgd2hlbiByZXN0b3JlZCB3aXRoIGBhbnlgIHJlc3VsdHMuXG4gICAqXG4gICAqL1xuICByZXN0b3JlKG9wdGlvbnM6IElSZXN0b3JhYmxlLklPcHRpb25zPFQ+KTogUHJvbWlzZTxVPjtcblxuICAvKipcbiAgICogQSBwcm9taXNlIHRoYXQgc2V0dGxlcyB3aGVuIHRoZSBjb2xsZWN0aW9uIGhhcyBiZWVuIHJlc3RvcmVkLlxuICAgKi9cbiAgcmVhZG9ubHkgcmVzdG9yZWQ6IFByb21pc2U8VT47XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGBJUmVzdG9yYWJsZWAgaW50ZXJmYWNlIGRlZmluaXRpb25zLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElSZXN0b3JhYmxlIHtcbiAgLyoqXG4gICAqIFRoZSBzdGF0ZSByZXN0b3JhdGlvbiBjb25maWd1cmF0aW9uIG9wdGlvbnMuXG4gICAqXG4gICAqIEB0eXBlcGFyYW0gVCAtIFRoZSB0eXBlIG9mIG9iamVjdCBoZWxkIGJ5IHRoZSByZXN0b3JhYmxlIGNvbGxlY3Rpb24uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zPFQgZXh0ZW5kcyBJT2JzZXJ2YWJsZURpc3Bvc2FibGU+XG4gICAgZXh0ZW5kcyBJUmVzdG9yZXIuSU9wdGlvbnM8VD4ge1xuICAgIC8qKlxuICAgICAqIFRoZSBkYXRhIGNvbm5lY3RvciB0byBmZXRjaCByZXN0b3JlIGRhdGEuXG4gICAgICovXG4gICAgY29ubmVjdG9yOiBJRGF0YUNvbm5lY3RvcjxSZWFkb25seVBhcnRpYWxKU09OVmFsdWU+O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNvbW1hbmQgcmVnaXN0cnkgd2hpY2ggaG9sZHMgdGhlIHJlc3RvcmUgY29tbWFuZC5cbiAgICAgKi9cbiAgICByZWdpc3RyeTogQ29tbWFuZFJlZ2lzdHJ5O1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFByb21pc2VEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElPYnNlcnZhYmxlRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBBdHRhY2hlZFByb3BlcnR5IH0gZnJvbSAnQGx1bWluby9wcm9wZXJ0aWVzJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IElPYmplY3RQb29sLCBJUmVzdG9yYWJsZSB9IGZyb20gJy4vaW50ZXJmYWNlcyc7XG5cbi8qKlxuICogQW4gb2JqZWN0IHBvb2wgdGhhdCBzdXBwb3J0cyByZXN0b3JhdGlvbi5cbiAqXG4gKiBAdHlwZXBhcmFtIFQgLSBUaGUgdHlwZSBvZiBvYmplY3QgYmVpbmcgdHJhY2tlZC5cbiAqL1xuZXhwb3J0IGNsYXNzIFJlc3RvcmFibGVQb29sPFxuICBUIGV4dGVuZHMgSU9ic2VydmFibGVEaXNwb3NhYmxlID0gSU9ic2VydmFibGVEaXNwb3NhYmxlXG4+IGltcGxlbWVudHMgSU9iamVjdFBvb2w8VD4sIElSZXN0b3JhYmxlPFQ+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyByZXN0b3JhYmxlIHBvb2wuXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIGluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgYSByZXN0b3JhYmxlIHBvb2wuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBSZXN0b3JhYmxlUG9vbC5JT3B0aW9ucykge1xuICAgIHRoaXMubmFtZXNwYWNlID0gb3B0aW9ucy5uYW1lc3BhY2U7XG4gIH1cblxuICAvKipcbiAgICogQSBuYW1lc3BhY2UgZm9yIGFsbCB0cmFja2VkIG9iamVjdHMuXG4gICAqL1xuICByZWFkb25seSBuYW1lc3BhY2U6IHN0cmluZztcblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIGFuIG9iamVjdCBvYmplY3QgaXMgYWRkZWQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBzaWduYWwgd2lsbCBvbmx5IGZpcmUgd2hlbiBhbiBvYmplY3QgaXMgYWRkZWQgdG8gdGhlIHBvb2wuXG4gICAqIEl0IHdpbGwgbm90IGZpcmUgaWYgYW4gb2JqZWN0IGluamVjdGVkIGludG8gdGhlIHBvb2wuXG4gICAqL1xuICBnZXQgYWRkZWQoKTogSVNpZ25hbDx0aGlzLCBUPiB7XG4gICAgcmV0dXJuIHRoaXMuX2FkZGVkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjdXJyZW50IG9iamVjdC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgcmVzdG9yYWJsZSBwb29sIGRvZXMgbm90IHNldCBgY3VycmVudGAuIEl0IGlzIGludGVuZGVkIGZvciBjbGllbnQgdXNlLlxuICAgKlxuICAgKiBJZiBgY3VycmVudGAgaXMgc2V0IHRvIGFuIG9iamVjdCB0aGF0IGRvZXMgbm90IGV4aXN0IGluIHRoZSBwb29sLCBpdCBpcyBhXG4gICAqIG5vLW9wLlxuICAgKi9cbiAgZ2V0IGN1cnJlbnQoKTogVCB8IG51bGwge1xuICAgIHJldHVybiB0aGlzLl9jdXJyZW50O1xuICB9XG4gIHNldCBjdXJyZW50KG9iajogVCB8IG51bGwpIHtcbiAgICBpZiAodGhpcy5fY3VycmVudCA9PT0gb2JqKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGlmIChvYmogIT09IG51bGwgJiYgdGhpcy5fb2JqZWN0cy5oYXMob2JqKSkge1xuICAgICAgdGhpcy5fY3VycmVudCA9IG9iajtcbiAgICAgIHRoaXMuX2N1cnJlbnRDaGFuZ2VkLmVtaXQodGhpcy5fY3VycmVudCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgY3VycmVudCB3aWRnZXQgY2hhbmdlcy5cbiAgICovXG4gIGdldCBjdXJyZW50Q2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIFQgfCBudWxsPiB7XG4gICAgcmV0dXJuIHRoaXMuX2N1cnJlbnRDaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRlc3Qgd2hldGhlciB0aGUgcG9vbCBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcHJvbWlzZSByZXNvbHZlZCB3aGVuIHRoZSByZXN0b3JhYmxlIHBvb2wgaGFzIGJlZW4gcmVzdG9yZWQuXG4gICAqL1xuICBnZXQgcmVzdG9yZWQoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3Jlc3RvcmVkLnByb21pc2U7XG4gIH1cblxuICAvKipcbiAgICogVGhlIG51bWJlciBvZiBvYmplY3RzIGhlbGQgYnkgdGhlIHBvb2wuXG4gICAqL1xuICBnZXQgc2l6ZSgpOiBudW1iZXIge1xuICAgIHJldHVybiB0aGlzLl9vYmplY3RzLnNpemU7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIGFuIG9iamVjdCBpcyB1cGRhdGVkLlxuICAgKi9cbiAgZ2V0IHVwZGF0ZWQoKTogSVNpZ25hbDx0aGlzLCBUPiB7XG4gICAgcmV0dXJuIHRoaXMuX3VwZGF0ZWQ7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgbmV3IG9iamVjdCB0byB0aGUgcG9vbC5cbiAgICpcbiAgICogQHBhcmFtIG9iaiAtIFRoZSBvYmplY3Qgb2JqZWN0IGJlaW5nIGFkZGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBvYmplY3QgcGFzc2VkIGludG8gdGhlIHBvb2wgaXMgYWRkZWQgc3luY2hyb25vdXNseTsgaXRzIGV4aXN0ZW5jZSBpblxuICAgKiB0aGUgcG9vbCBjYW4gYmUgY2hlY2tlZCB3aXRoIHRoZSBgaGFzKClgIG1ldGhvZC4gVGhlIHByb21pc2UgdGhpcyBtZXRob2RcbiAgICogcmV0dXJucyByZXNvbHZlcyBhZnRlciB0aGUgb2JqZWN0IGhhcyBiZWVuIGFkZGVkIGFuZCBzYXZlZCB0byBhbiB1bmRlcmx5aW5nXG4gICAqIHJlc3RvcmF0aW9uIGNvbm5lY3RvciwgaWYgb25lIGlzIGF2YWlsYWJsZS5cbiAgICovXG4gIGFzeW5jIGFkZChvYmo6IFQpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBpZiAob2JqLmlzRGlzcG9zZWQpIHtcbiAgICAgIGNvbnN0IHdhcm5pbmcgPSAnQSBkaXNwb3NlZCBvYmplY3QgY2Fubm90IGJlIGFkZGVkLic7XG4gICAgICBjb25zb2xlLndhcm4od2FybmluZywgb2JqKTtcbiAgICAgIHRocm93IG5ldyBFcnJvcih3YXJuaW5nKTtcbiAgICB9XG5cbiAgICBpZiAodGhpcy5fb2JqZWN0cy5oYXMob2JqKSkge1xuICAgICAgY29uc3Qgd2FybmluZyA9ICdUaGlzIG9iamVjdCBhbHJlYWR5IGV4aXN0cyBpbiB0aGUgcG9vbC4nO1xuICAgICAgY29uc29sZS53YXJuKHdhcm5pbmcsIG9iaik7XG4gICAgICB0aHJvdyBuZXcgRXJyb3Iod2FybmluZyk7XG4gICAgfVxuXG4gICAgdGhpcy5fb2JqZWN0cy5hZGQob2JqKTtcbiAgICBvYmouZGlzcG9zZWQuY29ubmVjdCh0aGlzLl9vbkluc3RhbmNlRGlzcG9zZWQsIHRoaXMpO1xuXG4gICAgaWYgKFByaXZhdGUuaW5qZWN0ZWRQcm9wZXJ0eS5nZXQob2JqKSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGlmICh0aGlzLl9yZXN0b3JlKSB7XG4gICAgICBjb25zdCB7IGNvbm5lY3RvciB9ID0gdGhpcy5fcmVzdG9yZTtcbiAgICAgIGNvbnN0IG9iak5hbWUgPSB0aGlzLl9yZXN0b3JlLm5hbWUob2JqKTtcblxuICAgICAgaWYgKG9iak5hbWUpIHtcbiAgICAgICAgY29uc3QgbmFtZSA9IGAke3RoaXMubmFtZXNwYWNlfToke29iak5hbWV9YDtcbiAgICAgICAgY29uc3QgZGF0YSA9IHRoaXMuX3Jlc3RvcmUuYXJncz8uKG9iaik7XG5cbiAgICAgICAgUHJpdmF0ZS5uYW1lUHJvcGVydHkuc2V0KG9iaiwgbmFtZSk7XG4gICAgICAgIGF3YWl0IGNvbm5lY3Rvci5zYXZlKG5hbWUsIHsgZGF0YSB9KTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBFbWl0IHRoZSBhZGRlZCBzaWduYWwuXG4gICAgdGhpcy5fYWRkZWQuZW1pdChvYmopO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBwb29sLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIERpc3Bvc2luZyBhIHBvb2wgZG9lcyBub3QgYWZmZWN0IHRoZSB1bmRlcmx5aW5nIGRhdGEgaW4gdGhlIGRhdGEgY29ubmVjdG9yLFxuICAgKiBpdCBzaW1wbHkgZGlzcG9zZXMgdGhlIGNsaWVudC1zaWRlIHBvb2wgd2l0aG91dCBtYWtpbmcgYW55IGNvbm5lY3RvciBjYWxscy5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9jdXJyZW50ID0gbnVsbDtcbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICB0aGlzLl9vYmplY3RzLmNsZWFyKCk7XG4gICAgU2lnbmFsLmNsZWFyRGF0YSh0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBGaW5kIHRoZSBmaXJzdCBvYmplY3QgaW4gdGhlIHBvb2wgdGhhdCBzYXRpc2ZpZXMgYSBmaWx0ZXIgZnVuY3Rpb24uXG4gICAqXG4gICAqIEBwYXJhbSAtIGZuIFRoZSBmaWx0ZXIgZnVuY3Rpb24gdG8gY2FsbCBvbiBlYWNoIG9iamVjdC5cbiAgICovXG4gIGZpbmQoZm46IChvYmo6IFQpID0+IGJvb2xlYW4pOiBUIHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCB2YWx1ZXMgPSB0aGlzLl9vYmplY3RzLnZhbHVlcygpO1xuICAgIGZvciAoY29uc3QgdmFsdWUgb2YgdmFsdWVzKSB7XG4gICAgICBpZiAoZm4odmFsdWUpKSB7XG4gICAgICAgIHJldHVybiB2YWx1ZTtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBJdGVyYXRlIHRocm91Z2ggZWFjaCBvYmplY3QgaW4gdGhlIHBvb2wuXG4gICAqXG4gICAqIEBwYXJhbSBmbiAtIFRoZSBmdW5jdGlvbiB0byBjYWxsIG9uIGVhY2ggb2JqZWN0LlxuICAgKi9cbiAgZm9yRWFjaChmbjogKG9iajogVCkgPT4gdm9pZCk6IHZvaWQge1xuICAgIHRoaXMuX29iamVjdHMuZm9yRWFjaChmbik7XG4gIH1cblxuICAvKipcbiAgICogRmlsdGVyIHRoZSBvYmplY3RzIGluIHRoZSBwb29sIGJhc2VkIG9uIGEgcHJlZGljYXRlLlxuICAgKlxuICAgKiBAcGFyYW0gZm4gLSBUaGUgZnVuY3Rpb24gYnkgd2hpY2ggdG8gZmlsdGVyLlxuICAgKi9cbiAgZmlsdGVyKGZuOiAob2JqOiBUKSA9PiBib29sZWFuKTogVFtdIHtcbiAgICBjb25zdCBmaWx0ZXJlZDogVFtdID0gW107XG4gICAgdGhpcy5mb3JFYWNoKG9iaiA9PiB7XG4gICAgICBpZiAoZm4ob2JqKSkge1xuICAgICAgICBmaWx0ZXJlZC5wdXNoKG9iaik7XG4gICAgICB9XG4gICAgfSk7XG4gICAgcmV0dXJuIGZpbHRlcmVkO1xuICB9XG5cbiAgLyoqXG4gICAqIEluamVjdCBhbiBvYmplY3QgaW50byB0aGUgcmVzdG9yYWJsZSBwb29sIHdpdGhvdXQgdGhlIHBvb2wgaGFuZGxpbmcgaXRzXG4gICAqIHJlc3RvcmF0aW9uIGxpZmVjeWNsZS5cbiAgICpcbiAgICogQHBhcmFtIG9iaiAtIFRoZSBvYmplY3QgdG8gaW5qZWN0IGludG8gdGhlIHBvb2wuXG4gICAqL1xuICBpbmplY3Qob2JqOiBUKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgUHJpdmF0ZS5pbmplY3RlZFByb3BlcnR5LnNldChvYmosIHRydWUpO1xuICAgIHJldHVybiB0aGlzLmFkZChvYmopO1xuICB9XG5cbiAgLyoqXG4gICAqIENoZWNrIGlmIHRoaXMgcG9vbCBoYXMgdGhlIHNwZWNpZmllZCBvYmplY3QuXG4gICAqXG4gICAqIEBwYXJhbSBvYmogLSBUaGUgb2JqZWN0IHdob3NlIGV4aXN0ZW5jZSBpcyBiZWluZyBjaGVja2VkLlxuICAgKi9cbiAgaGFzKG9iajogVCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9vYmplY3RzLmhhcyhvYmopO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlc3RvcmUgdGhlIG9iamVjdHMgaW4gdGhpcyBwb29sJ3MgbmFtZXNwYWNlLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBjb25maWd1cmF0aW9uIG9wdGlvbnMgdGhhdCBkZXNjcmliZSByZXN0b3JhdGlvbi5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiByZXN0b3JhdGlvbiBoYXMgY29tcGxldGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgZnVuY3Rpb24gc2hvdWxkIGFsbW9zdCBuZXZlciBiZSBpbnZva2VkIGJ5IGNsaWVudCBjb2RlLiBJdHMgcHJpbWFyeVxuICAgKiB1c2UgY2FzZSBpcyB0byBiZSBpbnZva2VkIGJ5IGEgbGF5b3V0IHJlc3RvcmVyIHBsdWdpbiB0aGF0IGhhbmRsZXNcbiAgICogbXVsdGlwbGUgcmVzdG9yYWJsZSBwb29scyBhbmQsIHdoZW4gcmVhZHksIGFza3MgdGhlbSBlYWNoIHRvIHJlc3RvcmUgdGhlaXJcbiAgICogcmVzcGVjdGl2ZSBvYmplY3RzLlxuICAgKi9cbiAgYXN5bmMgcmVzdG9yZShvcHRpb25zOiBJUmVzdG9yYWJsZS5JT3B0aW9uczxUPik6IFByb21pc2U8YW55PiB7XG4gICAgaWYgKHRoaXMuX2hhc1Jlc3RvcmVkKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoJ1RoaXMgcG9vbCBoYXMgYWxyZWFkeSBiZWVuIHJlc3RvcmVkLicpO1xuICAgIH1cblxuICAgIHRoaXMuX2hhc1Jlc3RvcmVkID0gdHJ1ZTtcblxuICAgIGNvbnN0IHsgY29tbWFuZCwgY29ubmVjdG9yLCByZWdpc3RyeSwgd2hlbiB9ID0gb3B0aW9ucztcbiAgICBjb25zdCBuYW1lc3BhY2UgPSB0aGlzLm5hbWVzcGFjZTtcbiAgICBjb25zdCBwcm9taXNlcyA9IHdoZW5cbiAgICAgID8gW2Nvbm5lY3Rvci5saXN0KG5hbWVzcGFjZSldLmNvbmNhdCh3aGVuKVxuICAgICAgOiBbY29ubmVjdG9yLmxpc3QobmFtZXNwYWNlKV07XG5cbiAgICB0aGlzLl9yZXN0b3JlID0gb3B0aW9ucztcblxuICAgIGNvbnN0IFtzYXZlZF0gPSBhd2FpdCBQcm9taXNlLmFsbChwcm9taXNlcyk7XG4gICAgY29uc3QgdmFsdWVzID0gYXdhaXQgUHJvbWlzZS5hbGwoXG4gICAgICBzYXZlZC5pZHMubWFwKGFzeW5jIChpZCwgaW5kZXgpID0+IHtcbiAgICAgICAgY29uc3QgdmFsdWUgPSBzYXZlZC52YWx1ZXNbaW5kZXhdO1xuICAgICAgICBjb25zdCBhcmdzID0gdmFsdWUgJiYgKHZhbHVlIGFzIGFueSkuZGF0YTtcblxuICAgICAgICBpZiAoYXJncyA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgcmV0dXJuIGNvbm5lY3Rvci5yZW1vdmUoaWQpO1xuICAgICAgICB9XG5cbiAgICAgICAgLy8gRXhlY3V0ZSB0aGUgY29tbWFuZCBhbmQgaWYgaXQgZmFpbHMsIGRlbGV0ZSB0aGUgc3RhdGUgcmVzdG9yZSBkYXRhLlxuICAgICAgICByZXR1cm4gcmVnaXN0cnlcbiAgICAgICAgICAuZXhlY3V0ZShjb21tYW5kLCBhcmdzKVxuICAgICAgICAgIC5jYXRjaCgoKSA9PiBjb25uZWN0b3IucmVtb3ZlKGlkKSk7XG4gICAgICB9KVxuICAgICk7XG4gICAgdGhpcy5fcmVzdG9yZWQucmVzb2x2ZSgpO1xuICAgIHJldHVybiB2YWx1ZXM7XG4gIH1cblxuICAvKipcbiAgICogU2F2ZSB0aGUgcmVzdG9yZSBkYXRhIGZvciBhIGdpdmVuIG9iamVjdC5cbiAgICpcbiAgICogQHBhcmFtIG9iaiAtIFRoZSBvYmplY3QgYmVpbmcgc2F2ZWQuXG4gICAqL1xuICBhc3luYyBzYXZlKG9iajogVCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IGluamVjdGVkID0gUHJpdmF0ZS5pbmplY3RlZFByb3BlcnR5LmdldChvYmopO1xuXG4gICAgaWYgKCF0aGlzLl9yZXN0b3JlIHx8ICF0aGlzLmhhcyhvYmopIHx8IGluamVjdGVkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3QgeyBjb25uZWN0b3IgfSA9IHRoaXMuX3Jlc3RvcmU7XG4gICAgY29uc3Qgb2JqTmFtZSA9IHRoaXMuX3Jlc3RvcmUubmFtZShvYmopO1xuICAgIGNvbnN0IG9sZE5hbWUgPSBQcml2YXRlLm5hbWVQcm9wZXJ0eS5nZXQob2JqKTtcbiAgICBjb25zdCBuZXdOYW1lID0gb2JqTmFtZSA/IGAke3RoaXMubmFtZXNwYWNlfToke29iak5hbWV9YCA6ICcnO1xuXG4gICAgaWYgKG9sZE5hbWUgJiYgb2xkTmFtZSAhPT0gbmV3TmFtZSkge1xuICAgICAgYXdhaXQgY29ubmVjdG9yLnJlbW92ZShvbGROYW1lKTtcbiAgICB9XG5cbiAgICAvLyBTZXQgdGhlIG5hbWUgcHJvcGVydHkgaXJyZXNwZWN0aXZlIG9mIHdoZXRoZXIgdGhlIG5ldyBuYW1lIGlzIG51bGwuXG4gICAgUHJpdmF0ZS5uYW1lUHJvcGVydHkuc2V0KG9iaiwgbmV3TmFtZSk7XG5cbiAgICBpZiAobmV3TmFtZSkge1xuICAgICAgY29uc3QgZGF0YSA9IHRoaXMuX3Jlc3RvcmUuYXJncz8uKG9iaik7XG4gICAgICBhd2FpdCBjb25uZWN0b3Iuc2F2ZShuZXdOYW1lLCB7IGRhdGEgfSk7XG4gICAgfVxuXG4gICAgaWYgKG9sZE5hbWUgIT09IG5ld05hbWUpIHtcbiAgICAgIHRoaXMuX3VwZGF0ZWQuZW1pdChvYmopO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhbiB1cCBhZnRlciBkaXNwb3NlZCBvYmplY3RzLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25JbnN0YW5jZURpc3Bvc2VkKG9iajogVCk6IHZvaWQge1xuICAgIHRoaXMuX29iamVjdHMuZGVsZXRlKG9iaik7XG5cbiAgICBpZiAob2JqID09PSB0aGlzLl9jdXJyZW50KSB7XG4gICAgICB0aGlzLl9jdXJyZW50ID0gbnVsbDtcbiAgICAgIHRoaXMuX2N1cnJlbnRDaGFuZ2VkLmVtaXQodGhpcy5fY3VycmVudCk7XG4gICAgfVxuXG4gICAgaWYgKFByaXZhdGUuaW5qZWN0ZWRQcm9wZXJ0eS5nZXQob2JqKSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGlmICghdGhpcy5fcmVzdG9yZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IHsgY29ubmVjdG9yIH0gPSB0aGlzLl9yZXN0b3JlO1xuICAgIGNvbnN0IG5hbWUgPSBQcml2YXRlLm5hbWVQcm9wZXJ0eS5nZXQob2JqKTtcblxuICAgIGlmIChuYW1lKSB7XG4gICAgICB2b2lkIGNvbm5lY3Rvci5yZW1vdmUobmFtZSk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfYWRkZWQgPSBuZXcgU2lnbmFsPHRoaXMsIFQ+KHRoaXMpO1xuICBwcml2YXRlIF9jdXJyZW50OiBUIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX2N1cnJlbnRDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBUIHwgbnVsbD4odGhpcyk7XG4gIHByaXZhdGUgX2hhc1Jlc3RvcmVkID0gZmFsc2U7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfb2JqZWN0cyA9IG5ldyBTZXQ8VD4oKTtcbiAgcHJpdmF0ZSBfcmVzdG9yZTogSVJlc3RvcmFibGUuSU9wdGlvbnM8VD4gfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfcmVzdG9yZWQgPSBuZXcgUHJvbWlzZURlbGVnYXRlPHZvaWQ+KCk7XG4gIHByaXZhdGUgX3VwZGF0ZWQgPSBuZXcgU2lnbmFsPHRoaXMsIFQ+KHRoaXMpO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgUmVzdG9yYWJsZVBvb2xgIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgUmVzdG9yYWJsZVBvb2wge1xuICAvKipcbiAgICogVGhlIGluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgdGhlIHJlc3RvcmFibGUgcG9vbC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIEEgbmFtZXNwYWNlIGRlc2lnbmF0aW5nIG9iamVjdHMgZnJvbSB0aGlzIHBvb2wuXG4gICAgICovXG4gICAgbmFtZXNwYWNlOiBzdHJpbmc7XG4gIH1cbn1cblxuLypcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIEFuIGF0dGFjaGVkIHByb3BlcnR5IHRvIGluZGljYXRlIHdoZXRoZXIgYW4gb2JqZWN0IGhhcyBiZWVuIGluamVjdGVkLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGluamVjdGVkUHJvcGVydHkgPSBuZXcgQXR0YWNoZWRQcm9wZXJ0eTxcbiAgICBJT2JzZXJ2YWJsZURpc3Bvc2FibGUsXG4gICAgYm9vbGVhblxuICA+KHtcbiAgICBuYW1lOiAnaW5qZWN0ZWQnLFxuICAgIGNyZWF0ZTogKCkgPT4gZmFsc2VcbiAgfSk7XG5cbiAgLyoqXG4gICAqIEFuIGF0dGFjaGVkIHByb3BlcnR5IGZvciBhbiBvYmplY3QncyBJRC5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBuYW1lUHJvcGVydHkgPSBuZXcgQXR0YWNoZWRQcm9wZXJ0eTxcbiAgICBJT2JzZXJ2YWJsZURpc3Bvc2FibGUsXG4gICAgc3RyaW5nXG4gID4oe1xuICAgIG5hbWU6ICduYW1lJyxcbiAgICBjcmVhdGU6ICgpID0+ICcnXG4gIH0pO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBJRGF0YUNvbm5lY3RvciB9IGZyb20gJy4vaW50ZXJmYWNlcyc7XG5pbXBvcnQgeyBJU3RhdGVEQiB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBjb25jcmV0ZSBpbXBsZW1lbnRhdGlvbiBvZiBhIHN0YXRlIGRhdGFiYXNlLlxuICovXG5leHBvcnQgY2xhc3MgU3RhdGVEQjxcbiAgVCBleHRlbmRzIFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSA9IFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZVxuPiBpbXBsZW1lbnRzIElTdGF0ZURCPFQ+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBzdGF0ZSBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgaW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBhIHN0YXRlIGRhdGFiYXNlLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogU3RhdGVEQi5JT3B0aW9uczxUPiA9IHt9KSB7XG4gICAgY29uc3QgeyBjb25uZWN0b3IsIHRyYW5zZm9ybSB9ID0gb3B0aW9ucztcblxuICAgIHRoaXMuX2Nvbm5lY3RvciA9IGNvbm5lY3RvciB8fCBuZXcgU3RhdGVEQi5Db25uZWN0b3IoKTtcbiAgICBpZiAoIXRyYW5zZm9ybSkge1xuICAgICAgdGhpcy5fcmVhZHkgPSBQcm9taXNlLnJlc29sdmUodW5kZWZpbmVkKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5fcmVhZHkgPSB0cmFuc2Zvcm0udGhlbih0cmFuc2Zvcm1hdGlvbiA9PiB7XG4gICAgICAgIGNvbnN0IHsgY29udGVudHMsIHR5cGUgfSA9IHRyYW5zZm9ybWF0aW9uO1xuXG4gICAgICAgIHN3aXRjaCAodHlwZSkge1xuICAgICAgICAgIGNhc2UgJ2NhbmNlbCc6XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgY2FzZSAnY2xlYXInOlxuICAgICAgICAgICAgcmV0dXJuIHRoaXMuX2NsZWFyKCk7XG4gICAgICAgICAgY2FzZSAnbWVyZ2UnOlxuICAgICAgICAgICAgcmV0dXJuIHRoaXMuX21lcmdlKGNvbnRlbnRzIHx8IHt9KTtcbiAgICAgICAgICBjYXNlICdvdmVyd3JpdGUnOlxuICAgICAgICAgICAgcmV0dXJuIHRoaXMuX292ZXJ3cml0ZShjb250ZW50cyB8fCB7fSk7XG4gICAgICAgICAgZGVmYXVsdDpcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIHRoYXQgZW1pdHMgdGhlIGNoYW5nZSB0eXBlIGFueSB0aW1lIGEgdmFsdWUgY2hhbmdlcy5cbiAgICovXG4gIGdldCBjaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgU3RhdGVEQi5DaGFuZ2U+IHtcbiAgICByZXR1cm4gdGhpcy5fY2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhciB0aGUgZW50aXJlIGRhdGFiYXNlLlxuICAgKi9cbiAgYXN5bmMgY2xlYXIoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgYXdhaXQgdGhpcy5fcmVhZHk7XG4gICAgYXdhaXQgdGhpcy5fY2xlYXIoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXRyaWV2ZSBhIHNhdmVkIGJ1bmRsZSBmcm9tIHRoZSBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIGlkIC0gVGhlIGlkZW50aWZpZXIgdXNlZCB0byByZXRyaWV2ZSBhIGRhdGEgYnVuZGxlLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBiZWFycyBhIGRhdGEgcGF5bG9hZCBpZiBhdmFpbGFibGUuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIGBpZGAgdmFsdWVzIG9mIHN0b3JlZCBpdGVtcyBpbiB0aGUgc3RhdGUgZGF0YWJhc2UgYXJlIGZvcm1hdHRlZDpcbiAgICogYCduYW1lc3BhY2U6aWRlbnRpZmllcidgLCB3aGljaCBpcyB0aGUgc2FtZSBjb252ZW50aW9uIHRoYXQgY29tbWFuZFxuICAgKiBpZGVudGlmaWVycyBpbiBKdXB5dGVyTGFiIHVzZSBhcyB3ZWxsLiBXaGlsZSB0aGlzIGlzIG5vdCBhIHRlY2huaWNhbFxuICAgKiByZXF1aXJlbWVudCBmb3IgYGZldGNoKClgLCBgcmVtb3ZlKClgLCBhbmQgYHNhdmUoKWAsIGl0ICppcyogbmVjZXNzYXJ5IGZvclxuICAgKiB1c2luZyB0aGUgYGxpc3QobmFtZXNwYWNlOiBzdHJpbmcpYCBtZXRob2QuXG4gICAqXG4gICAqIFRoZSBwcm9taXNlIHJldHVybmVkIGJ5IHRoaXMgbWV0aG9kIG1heSBiZSByZWplY3RlZCBpZiBhbiBlcnJvciBvY2N1cnMgaW5cbiAgICogcmV0cmlldmluZyB0aGUgZGF0YS4gTm9uLWV4aXN0ZW5jZSBvZiBhbiBgaWRgIHdpbGwgc3VjY2VlZCB3aXRoIHRoZSBgdmFsdWVgXG4gICAqIGB1bmRlZmluZWRgLlxuICAgKi9cbiAgYXN5bmMgZmV0Y2goaWQ6IHN0cmluZyk6IFByb21pc2U8VCB8IHVuZGVmaW5lZD4ge1xuICAgIGF3YWl0IHRoaXMuX3JlYWR5O1xuICAgIHJldHVybiB0aGlzLl9mZXRjaChpZCk7XG4gIH1cblxuICAvKipcbiAgICogUmV0cmlldmUgYWxsIHRoZSBzYXZlZCBidW5kbGVzIGZvciBhIG5hbWVzcGFjZS5cbiAgICpcbiAgICogQHBhcmFtIGZpbHRlciAtIFRoZSBuYW1lc3BhY2UgcHJlZml4IHRvIHJldHJpZXZlLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBiZWFycyBhIGNvbGxlY3Rpb24gb2YgcGF5bG9hZHMgZm9yIGEgbmFtZXNwYWNlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIE5hbWVzcGFjZXMgYXJlIGVudGlyZWx5IGNvbnZlbnRpb25hbCBlbnRpdGllcy4gVGhlIGBpZGAgdmFsdWVzIG9mIHN0b3JlZFxuICAgKiBpdGVtcyBpbiB0aGUgc3RhdGUgZGF0YWJhc2UgYXJlIGZvcm1hdHRlZDogYCduYW1lc3BhY2U6aWRlbnRpZmllcidgLCB3aGljaFxuICAgKiBpcyB0aGUgc2FtZSBjb252ZW50aW9uIHRoYXQgY29tbWFuZCBpZGVudGlmaWVycyBpbiBKdXB5dGVyTGFiIHVzZSBhcyB3ZWxsLlxuICAgKlxuICAgKiBJZiB0aGVyZSBhcmUgYW55IGVycm9ycyBpbiByZXRyaWV2aW5nIHRoZSBkYXRhLCB0aGV5IHdpbGwgYmUgbG9nZ2VkIHRvIHRoZVxuICAgKiBjb25zb2xlIGluIG9yZGVyIHRvIG9wdGltaXN0aWNhbGx5IHJldHVybiBhbnkgZXh0YW50IGRhdGEgd2l0aG91dCBmYWlsaW5nLlxuICAgKiBUaGlzIHByb21pc2Ugd2lsbCBhbHdheXMgc3VjY2VlZC5cbiAgICovXG4gIGFzeW5jIGxpc3QobmFtZXNwYWNlOiBzdHJpbmcpOiBQcm9taXNlPHsgaWRzOiBzdHJpbmdbXTsgdmFsdWVzOiBUW10gfT4ge1xuICAgIGF3YWl0IHRoaXMuX3JlYWR5O1xuICAgIHJldHVybiB0aGlzLl9saXN0KG5hbWVzcGFjZSk7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIGEgdmFsdWUgZnJvbSB0aGUgZGF0YWJhc2UuXG4gICAqXG4gICAqIEBwYXJhbSBpZCAtIFRoZSBpZGVudGlmaWVyIGZvciB0aGUgZGF0YSBiZWluZyByZW1vdmVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBpcyByZWplY3RlZCBpZiByZW1vdmUgZmFpbHMgYW5kIHN1Y2NlZWRzIG90aGVyd2lzZS5cbiAgICovXG4gIGFzeW5jIHJlbW92ZShpZDogc3RyaW5nKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgYXdhaXQgdGhpcy5fcmVhZHk7XG4gICAgYXdhaXQgdGhpcy5fcmVtb3ZlKGlkKTtcbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoeyBpZCwgdHlwZTogJ3JlbW92ZScgfSk7XG4gIH1cblxuICAvKipcbiAgICogU2F2ZSBhIHZhbHVlIGluIHRoZSBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIGlkIC0gVGhlIGlkZW50aWZpZXIgZm9yIHRoZSBkYXRhIGJlaW5nIHNhdmVkLlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgZGF0YSBiZWluZyBzYXZlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgaXMgcmVqZWN0ZWQgaWYgc2F2aW5nIGZhaWxzIGFuZCBzdWNjZWVkcyBvdGhlcndpc2UuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIGBpZGAgdmFsdWVzIG9mIHN0b3JlZCBpdGVtcyBpbiB0aGUgc3RhdGUgZGF0YWJhc2UgYXJlIGZvcm1hdHRlZDpcbiAgICogYCduYW1lc3BhY2U6aWRlbnRpZmllcidgLCB3aGljaCBpcyB0aGUgc2FtZSBjb252ZW50aW9uIHRoYXQgY29tbWFuZFxuICAgKiBpZGVudGlmaWVycyBpbiBKdXB5dGVyTGFiIHVzZSBhcyB3ZWxsLiBXaGlsZSB0aGlzIGlzIG5vdCBhIHRlY2huaWNhbFxuICAgKiByZXF1aXJlbWVudCBmb3IgYGZldGNoKClgLCBgcmVtb3ZlKClgLCBhbmQgYHNhdmUoKWAsIGl0ICppcyogbmVjZXNzYXJ5IGZvclxuICAgKiB1c2luZyB0aGUgYGxpc3QobmFtZXNwYWNlOiBzdHJpbmcpYCBtZXRob2QuXG4gICAqL1xuICBhc3luYyBzYXZlKGlkOiBzdHJpbmcsIHZhbHVlOiBUKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgYXdhaXQgdGhpcy5fcmVhZHk7XG4gICAgYXdhaXQgdGhpcy5fc2F2ZShpZCwgdmFsdWUpO1xuICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7IGlkLCB0eXBlOiAnc2F2ZScgfSk7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJuIGEgc2VyaWFsaXplZCBjb3B5IG9mIHRoZSBzdGF0ZSBkYXRhYmFzZSdzIGVudGlyZSBjb250ZW50cy5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2l0aCB0aGUgZGF0YWJhc2UgY29udGVudHMgYXMgSlNPTi5cbiAgICovXG4gIGFzeW5jIHRvSlNPTigpOiBQcm9taXNlPHsgcmVhZG9ubHkgW2lkOiBzdHJpbmddOiBUIH0+IHtcbiAgICBhd2FpdCB0aGlzLl9yZWFkeTtcblxuICAgIGNvbnN0IHsgaWRzLCB2YWx1ZXMgfSA9IGF3YWl0IHRoaXMuX2xpc3QoKTtcblxuICAgIHJldHVybiB2YWx1ZXMucmVkdWNlKChhY2MsIHZhbCwgaWR4KSA9PiB7XG4gICAgICBhY2NbaWRzW2lkeF1dID0gdmFsO1xuICAgICAgcmV0dXJuIGFjYztcbiAgICB9LCB7fSBhcyB7IFtpZDogc3RyaW5nXTogVCB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhciB0aGUgZW50aXJlIGRhdGFiYXNlLlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfY2xlYXIoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgYXdhaXQgUHJvbWlzZS5hbGwoKGF3YWl0IHRoaXMuX2xpc3QoKSkuaWRzLm1hcChpZCA9PiB0aGlzLl9yZW1vdmUoaWQpKSk7XG4gIH1cblxuICAvKipcbiAgICogRmV0Y2ggYSB2YWx1ZSBmcm9tIHRoZSBkYXRhYmFzZS5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX2ZldGNoKGlkOiBzdHJpbmcpOiBQcm9taXNlPFQgfCB1bmRlZmluZWQ+IHtcbiAgICBjb25zdCB2YWx1ZSA9IGF3YWl0IHRoaXMuX2Nvbm5lY3Rvci5mZXRjaChpZCk7XG5cbiAgICBpZiAodmFsdWUpIHtcbiAgICAgIHJldHVybiAoSlNPTi5wYXJzZSh2YWx1ZSkgYXMgUHJpdmF0ZS5FbnZlbG9wZSkudiBhcyBUO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBGZXRjaCBhIGxpc3QgZnJvbSB0aGUgZGF0YWJhc2UuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9saXN0KG5hbWVzcGFjZSA9ICcnKTogUHJvbWlzZTx7IGlkczogc3RyaW5nW107IHZhbHVlczogVFtdIH0+IHtcbiAgICBjb25zdCB7IGlkcywgdmFsdWVzIH0gPSBhd2FpdCB0aGlzLl9jb25uZWN0b3IubGlzdChuYW1lc3BhY2UpO1xuXG4gICAgcmV0dXJuIHtcbiAgICAgIGlkcyxcbiAgICAgIHZhbHVlczogdmFsdWVzLm1hcCh2YWwgPT4gKEpTT04ucGFyc2UodmFsKSBhcyBQcml2YXRlLkVudmVsb3BlKS52IGFzIFQpXG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBNZXJnZSBkYXRhIGludG8gdGhlIHN0YXRlIGRhdGFiYXNlLlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfbWVyZ2UoY29udGVudHM6IFN0YXRlREIuQ29udGVudDxUPik6IFByb21pc2U8dm9pZD4ge1xuICAgIGF3YWl0IFByb21pc2UuYWxsKFxuICAgICAgT2JqZWN0LmtleXMoY29udGVudHMpLm1hcChcbiAgICAgICAga2V5ID0+IGNvbnRlbnRzW2tleV0gJiYgdGhpcy5fc2F2ZShrZXksIGNvbnRlbnRzW2tleV0hKVxuICAgICAgKVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogT3ZlcndyaXRlIHRoZSBlbnRpcmUgZGF0YWJhc2Ugd2l0aCBuZXcgY29udGVudHMuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9vdmVyd3JpdGUoY29udGVudHM6IFN0YXRlREIuQ29udGVudDxUPik6IFByb21pc2U8dm9pZD4ge1xuICAgIGF3YWl0IHRoaXMuX2NsZWFyKCk7XG4gICAgYXdhaXQgdGhpcy5fbWVyZ2UoY29udGVudHMpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhIGtleSBpbiB0aGUgZGF0YWJhc2UuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9yZW1vdmUoaWQ6IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9jb25uZWN0b3IucmVtb3ZlKGlkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTYXZlIGEga2V5IGFuZCBpdHMgdmFsdWUgaW4gdGhlIGRhdGFiYXNlLlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfc2F2ZShpZDogc3RyaW5nLCB2YWx1ZTogVCk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9jb25uZWN0b3Iuc2F2ZShpZCwgSlNPTi5zdHJpbmdpZnkoeyB2OiB2YWx1ZSB9KSk7XG4gIH1cblxuICBwcml2YXRlIF9jaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBTdGF0ZURCLkNoYW5nZT4odGhpcyk7XG4gIHByaXZhdGUgX2Nvbm5lY3RvcjogSURhdGFDb25uZWN0b3I8c3RyaW5nPjtcbiAgcHJpdmF0ZSBfcmVhZHk6IFByb21pc2U8dm9pZD47XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIFN0YXRlREIgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBTdGF0ZURCIHtcbiAgLyoqXG4gICAqIEEgc3RhdGUgZGF0YWJhc2UgY2hhbmdlLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgQ2hhbmdlID0ge1xuICAgIC8qKlxuICAgICAqIFRoZSBrZXkgb2YgdGhlIGRhdGFiYXNlIGl0ZW0gdGhhdCB3YXMgY2hhbmdlZC5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGlzIGZpZWxkIGlzIHNldCB0byBgbnVsbGAgZm9yIGdsb2JhbCBjaGFuZ2VzIChpLmUuIGBjbGVhcmApLlxuICAgICAqL1xuICAgIGlkOiBzdHJpbmcgfCBudWxsO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHR5cGUgb2YgY2hhbmdlLlxuICAgICAqL1xuICAgIHR5cGU6ICdjbGVhcicgfCAncmVtb3ZlJyB8ICdzYXZlJztcbiAgfTtcblxuICAvKipcbiAgICogQSBkYXRhIHRyYW5zZm9ybWF0aW9uIHRoYXQgY2FuIGJlIGFwcGxpZWQgdG8gYSBzdGF0ZSBkYXRhYmFzZS5cbiAgICovXG4gIGV4cG9ydCB0eXBlIERhdGFUcmFuc2Zvcm08XG4gICAgVCBleHRlbmRzIFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSA9IFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZVxuICA+ID0ge1xuICAgIC8qXG4gICAgICogVGhlIGNoYW5nZSBvcGVyYXRpb24gYmVpbmcgYXBwbGllZC5cbiAgICAgKi9cbiAgICB0eXBlOiAnY2FuY2VsJyB8ICdjbGVhcicgfCAnbWVyZ2UnIHwgJ292ZXJ3cml0ZSc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29udGVudHMgb2YgdGhlIGNoYW5nZSBvcGVyYXRpb24uXG4gICAgICovXG4gICAgY29udGVudHM6IENvbnRlbnQ8VD4gfCBudWxsO1xuICB9O1xuXG4gIC8qKlxuICAgKiBEYXRhYmFzZSBjb250ZW50IG1hcFxuICAgKi9cbiAgZXhwb3J0IHR5cGUgQ29udGVudDxUPiA9IHsgW2lkOiBzdHJpbmddOiBUIHwgdW5kZWZpbmVkIH07XG5cbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgc3RhdGUgZGF0YWJhc2UuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zPFxuICAgIFQgZXh0ZW5kcyBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUgPSBSZWFkb25seVBhcnRpYWxKU09OVmFsdWVcbiAgPiB7XG4gICAgLyoqXG4gICAgICogT3B0aW9uYWwgc3RyaW5nIGtleS92YWx1ZSBjb25uZWN0b3IuIERlZmF1bHRzIHRvIGluLW1lbW9yeSBjb25uZWN0b3IuXG4gICAgICovXG4gICAgY29ubmVjdG9yPzogSURhdGFDb25uZWN0b3I8c3RyaW5nPjtcblxuICAgIC8qKlxuICAgICAqIEFuIG9wdGlvbmFsIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aXRoIGEgZGF0YSB0cmFuc2Zvcm1hdGlvbiB0aGF0IGlzXG4gICAgICogYXBwbGllZCB0byB0aGUgZGF0YWJhc2UgY29udGVudHMgYmVmb3JlIHRoZSBkYXRhYmFzZSBiZWdpbnMgcmVzb2x2aW5nXG4gICAgICogY2xpZW50IHJlcXVlc3RzLlxuICAgICAqL1xuICAgIHRyYW5zZm9ybT86IFByb21pc2U8RGF0YVRyYW5zZm9ybTxUPj47XG4gIH1cblxuICAvKipcbiAgICogQW4gaW4tbWVtb3J5IHN0cmluZyBrZXkvdmFsdWUgZGF0YSBjb25uZWN0b3IuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgQ29ubmVjdG9yIGltcGxlbWVudHMgSURhdGFDb25uZWN0b3I8c3RyaW5nPiB7XG4gICAgLyoqXG4gICAgICogUmV0cmlldmUgYW4gaXRlbSBmcm9tIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICAgKi9cbiAgICBhc3luYyBmZXRjaChpZDogc3RyaW5nKTogUHJvbWlzZTxzdHJpbmc+IHtcbiAgICAgIHJldHVybiB0aGlzLl9zdG9yYWdlW2lkXTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZXRyaWV2ZSB0aGUgbGlzdCBvZiBpdGVtcyBhdmFpbGFibGUgZnJvbSB0aGUgZGF0YSBjb25uZWN0b3IuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gbmFtZXNwYWNlIC0gSWYgbm90IGVtcHR5LCBvbmx5IGtleXMgd2hvc2UgZmlyc3QgdG9rZW4gYmVmb3JlIGA6YFxuICAgICAqIGV4YWN0bHkgbWF0Y2ggYG5hbWVzcGFjZWAgd2lsbCBiZSByZXR1cm5lZCwgZS5nLiBgZm9vYCBpbiBgZm9vOmJhcmAuXG4gICAgICovXG4gICAgYXN5bmMgbGlzdChuYW1lc3BhY2UgPSAnJyk6IFByb21pc2U8eyBpZHM6IHN0cmluZ1tdOyB2YWx1ZXM6IHN0cmluZ1tdIH0+IHtcbiAgICAgIHJldHVybiBPYmplY3Qua2V5cyh0aGlzLl9zdG9yYWdlKS5yZWR1Y2UoXG4gICAgICAgIChhY2MsIHZhbCkgPT4ge1xuICAgICAgICAgIGlmIChuYW1lc3BhY2UgPT09ICcnID8gdHJ1ZSA6IG5hbWVzcGFjZSA9PT0gdmFsLnNwbGl0KCc6JylbMF0pIHtcbiAgICAgICAgICAgIGFjYy5pZHMucHVzaCh2YWwpO1xuICAgICAgICAgICAgYWNjLnZhbHVlcy5wdXNoKHRoaXMuX3N0b3JhZ2VbdmFsXSk7XG4gICAgICAgICAgfVxuICAgICAgICAgIHJldHVybiBhY2M7XG4gICAgICAgIH0sXG4gICAgICAgIHsgaWRzOiBbXSBhcyBzdHJpbmdbXSwgdmFsdWVzOiBbXSBhcyBzdHJpbmdbXSB9XG4gICAgICApO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlbW92ZSBhIHZhbHVlIHVzaW5nIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICAgKi9cbiAgICBhc3luYyByZW1vdmUoaWQ6IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgICAgZGVsZXRlIHRoaXMuX3N0b3JhZ2VbaWRdO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFNhdmUgYSB2YWx1ZSB1c2luZyB0aGUgZGF0YSBjb25uZWN0b3IuXG4gICAgICovXG4gICAgYXN5bmMgc2F2ZShpZDogc3RyaW5nLCB2YWx1ZTogc3RyaW5nKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICB0aGlzLl9zdG9yYWdlW2lkXSA9IHZhbHVlO1xuICAgIH1cblxuICAgIHByaXZhdGUgX3N0b3JhZ2U6IHsgW2tleTogc3RyaW5nXTogc3RyaW5nIH0gPSB7fTtcbiAgfVxufVxuXG4vKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgbW9kdWxlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIEFuIGVudmVsb3BlIGFyb3VuZCBhIEpTT04gdmFsdWUgc3RvcmVkIGluIHRoZSBzdGF0ZSBkYXRhYmFzZS5cbiAgICovXG4gIGV4cG9ydCB0eXBlIEVudmVsb3BlID0geyByZWFkb25seSB2OiBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUgfTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlLCBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEYXRhQ29ubmVjdG9yIH0gZnJvbSAnLi9pbnRlcmZhY2VzJztcblxuLyogdHNsaW50OmRpc2FibGUgKi9cbi8qKlxuICogVGhlIGRlZmF1bHQgc3RhdGUgZGF0YWJhc2UgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJU3RhdGVEQiA9IG5ldyBUb2tlbjxJU3RhdGVEQj4oJ0BqdXB5dGVybGFiL2NvcmV1dGlsczpJU3RhdGVEQicpO1xuLyogdHNsaW50OmVuYWJsZSAqL1xuXG4vKipcbiAqIFRoZSBkZXNjcmlwdGlvbiBvZiBhIHN0YXRlIGRhdGFiYXNlLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElTdGF0ZURCPFxuICBUIGV4dGVuZHMgUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlID0gUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlXG4+IGV4dGVuZHMgSURhdGFDb25uZWN0b3I8VD4ge1xuICAvKipcbiAgICogUmV0dXJuIGEgc2VyaWFsaXplZCBjb3B5IG9mIHRoZSBzdGF0ZSBkYXRhYmFzZSdzIGVudGlyZSBjb250ZW50cy5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgYmVhcnMgdGhlIGRhdGFiYXNlIGNvbnRlbnRzIGFzIEpTT04uXG4gICAqL1xuICB0b0pTT04oKTogUHJvbWlzZTx7IFtpZDogc3RyaW5nXTogVCB9Pjtcbn1cbiJdLCJzb3VyY2VSb290IjoiIn0=