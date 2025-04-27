(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_attachments_lib_index_js-_0ab41"],{

/***/ "../packages/attachments/lib/index.js":
/*!********************************************!*\
  !*** ../packages/attachments/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AttachmentsModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_0__.AttachmentsModel),
/* harmony export */   "AttachmentsResolver": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_0__.AttachmentsResolver)
/* harmony export */ });
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./model */ "../packages/attachments/lib/model.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module attachments
 */



/***/ }),

/***/ "../packages/attachments/lib/model.js":
/*!********************************************!*\
  !*** ../packages/attachments/lib/model.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AttachmentsModel": () => (/* binding */ AttachmentsModel),
/* harmony export */   "AttachmentsResolver": () => (/* binding */ AttachmentsResolver)
/* harmony export */ });
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The default implementation of the IAttachmentsModel.
 */
class AttachmentsModel {
    /**
     * Construct a new observable outputs instance.
     */
    constructor(options = {}) {
        this._map = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableMap();
        this._isDisposed = false;
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._modelDB = null;
        this._serialized = null;
        this._changeGuard = false;
        this.contentFactory =
            options.contentFactory || AttachmentsModel.defaultContentFactory;
        if (options.values) {
            for (const key of Object.keys(options.values)) {
                if (options.values[key] !== undefined) {
                    this.set(key, options.values[key]);
                }
            }
        }
        this._map.changed.connect(this._onMapChanged, this);
        // If we are given a IModelDB, keep an up-to-date
        // serialized copy of the AttachmentsModel in it.
        if (options.modelDB) {
            this._modelDB = options.modelDB;
            this._serialized = this._modelDB.createValue('attachments');
            if (this._serialized.get()) {
                this.fromJSON(this._serialized.get());
            }
            else {
                this._serialized.set(this.toJSON());
            }
            this._serialized.changed.connect(this._onSerializedChanged, this);
        }
    }
    /**
     * A signal emitted when the model state changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * A signal emitted when the model changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * The keys of the attachments in the model.
     */
    get keys() {
        return this._map.keys();
    }
    /**
     * Get the length of the items in the model.
     */
    get length() {
        return this._map.keys().length;
    }
    /**
     * Test whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._map.dispose();
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
    /**
     * Whether the specified key is set.
     */
    has(key) {
        return this._map.has(key);
    }
    /**
     * Get an item at the specified key.
     */
    get(key) {
        return this._map.get(key);
    }
    /**
     * Set the value at the specified key.
     */
    set(key, value) {
        // Normalize stream data.
        const item = this._createItem({ value });
        this._map.set(key, item);
    }
    /**
     * Remove the attachment whose name is the specified key
     */
    remove(key) {
        this._map.delete(key);
    }
    /**
     * Clear all of the attachments.
     */
    clear() {
        this._map.values().forEach((item) => {
            item.dispose();
        });
        this._map.clear();
    }
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * This will clear any existing data.
     */
    fromJSON(values) {
        this.clear();
        Object.keys(values).forEach(key => {
            if (values[key] !== undefined) {
                this.set(key, values[key]);
            }
        });
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        const ret = {};
        for (const key of this._map.keys()) {
            ret[key] = this._map.get(key).toJSON();
        }
        return ret;
    }
    /**
     * Create an attachment item and hook up its signals.
     */
    _createItem(options) {
        const factory = this.contentFactory;
        const item = factory.createAttachmentModel(options);
        item.changed.connect(this._onGenericChange, this);
        return item;
    }
    /**
     * Handle a change to the list.
     */
    _onMapChanged(sender, args) {
        if (this._serialized && !this._changeGuard) {
            this._changeGuard = true;
            this._serialized.set(this.toJSON());
            this._changeGuard = false;
        }
        this._changed.emit(args);
        this._stateChanged.emit(void 0);
    }
    /**
     * If the serialized version of the outputs have changed due to a remote
     * action, then update the model accordingly.
     */
    _onSerializedChanged(sender, args) {
        if (!this._changeGuard) {
            this._changeGuard = true;
            this.fromJSON(args.newValue);
            this._changeGuard = false;
        }
    }
    /**
     * Handle a change to an item.
     */
    _onGenericChange() {
        this._stateChanged.emit(void 0);
    }
}
/**
 * The namespace for AttachmentsModel class statics.
 */
(function (AttachmentsModel) {
    /**
     * The default implementation of a `IAttachmentsModel.IContentFactory`.
     */
    class ContentFactory {
        /**
         * Create an attachment model.
         */
        createAttachmentModel(options) {
            return new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.AttachmentModel(options);
        }
    }
    AttachmentsModel.ContentFactory = ContentFactory;
    /**
     * The default attachment model factory.
     */
    AttachmentsModel.defaultContentFactory = new ContentFactory();
})(AttachmentsModel || (AttachmentsModel = {}));
/**
 * A resolver for cell attachments 'attachment:filename'.
 *
 * Will resolve to a data: url.
 */
class AttachmentsResolver {
    /**
     * Create an attachments resolver object.
     */
    constructor(options) {
        this._parent = options.parent || null;
        this._model = options.model;
    }
    /**
     * Resolve a relative url to a correct server path.
     */
    async resolveUrl(url) {
        if (this._parent && !url.startsWith('attachment:')) {
            return this._parent.resolveUrl(url);
        }
        return url;
    }
    /**
     * Get the download url of a given absolute server path.
     *
     * #### Notes
     * The returned URL may include a query parameter.
     */
    async getDownloadUrl(path) {
        if (this._parent && !path.startsWith('attachment:')) {
            return this._parent.getDownloadUrl(path);
        }
        // Return a data URL with the data of the url
        const key = path.slice('attachment:'.length);
        const attachment = this._model.get(key);
        if (attachment === undefined) {
            // Resolve with unprocessed path, to show as broken image
            return path;
        }
        const { data } = attachment;
        const mimeType = Object.keys(data)[0];
        // Only support known safe types:
        if (mimeType === undefined ||
            _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.imageRendererFactory.mimeTypes.indexOf(mimeType) === -1) {
            throw new Error(`Cannot render unknown image mime type "${mimeType}".`);
        }
        const dataUrl = `data:${mimeType};base64,${data[mimeType]}`;
        return dataUrl;
    }
    /**
     * Whether the URL should be handled by the resolver
     * or not.
     */
    isLocal(url) {
        var _a, _b, _c;
        if (this._parent && !url.startsWith('attachment:')) {
            return (_c = (_b = (_a = this._parent).isLocal) === null || _b === void 0 ? void 0 : _b.call(_a, url)) !== null && _c !== void 0 ? _c : true;
        }
        return true;
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvYXR0YWNobWVudHMvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9hdHRhY2htZW50cy9zcmMvbW9kZWwudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBRXFCOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1R4QiwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBUzFCO0FBS0Q7QUFHb0I7QUFpSHBEOztHQUVHO0FBQ0ksTUFBTSxnQkFBZ0I7SUFDM0I7O09BRUc7SUFDSCxZQUFZLFVBQXNDLEVBQUU7UUFnTTVDLFNBQUksR0FBRyxJQUFJLGtFQUFhLEVBQW9CLENBQUM7UUFDN0MsZ0JBQVcsR0FBRyxLQUFLLENBQUM7UUFDcEIsa0JBQWEsR0FBRyxJQUFJLHFEQUFNLENBQTBCLElBQUksQ0FBQyxDQUFDO1FBQzFELGFBQVEsR0FBRyxJQUFJLHFEQUFNLENBQXNDLElBQUksQ0FBQyxDQUFDO1FBQ2pFLGFBQVEsR0FBb0IsSUFBSSxDQUFDO1FBQ2pDLGdCQUFXLEdBQTRCLElBQUksQ0FBQztRQUM1QyxpQkFBWSxHQUFHLEtBQUssQ0FBQztRQXJNM0IsSUFBSSxDQUFDLGNBQWM7WUFDakIsT0FBTyxDQUFDLGNBQWMsSUFBSSxnQkFBZ0IsQ0FBQyxxQkFBcUIsQ0FBQztRQUNuRSxJQUFJLE9BQU8sQ0FBQyxNQUFNLEVBQUU7WUFDbEIsS0FBSyxNQUFNLEdBQUcsSUFBSSxNQUFNLENBQUMsSUFBSSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsRUFBRTtnQkFDN0MsSUFBSSxPQUFPLENBQUMsTUFBTSxDQUFDLEdBQUcsQ0FBQyxLQUFLLFNBQVMsRUFBRTtvQkFDckMsSUFBSSxDQUFDLEdBQUcsQ0FBQyxHQUFHLEVBQUUsT0FBTyxDQUFD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QSxNQUFNLElBQUksS0FBSyxDQUFDLDBDQUEwQyxRQUFRLElBQUksQ0FBQyxDQUFDO1NBQ3pFO1FBQ0QsTUFBTSxPQUFPLEdBQUcsUUFBUSxRQUFRLFdBQVcsSUFBSSxDQUFDLFFBQVEsQ0FBQyxFQUFFLENBQUM7UUFDNUQsT0FBTyxPQUFPLENBQUM7SUFDakIsQ0FBQztJQUVEOzs7T0FHRztJQUNILE9BQU8sQ0FBQyxHQUFXOztRQUNqQixJQUFJLElBQUksQ0FBQyxPQUFPLElBQUksQ0FBQyxHQUFHLENBQUMsVUFBVSxDQUFDLGFBQWEsQ0FBQyxFQUFFO1lBQ2xELG1CQUFPLFVBQUksQ0FBQyxPQUFPLEVBQUMsT0FBTyxtREFBRyxHQUFHLG9DQUFLLElBQUksQ0FBQztTQUM1QztRQUNELE9BQU8sSUFBSSxDQUFDO0lBQ2QsQ0FBQztDQUlGIiwiZmlsZSI6InBhY2thZ2VzX2F0dGFjaG1lbnRzX2xpYl9pbmRleF9qcy1fMGFiNDEuMmIyNGFhNmJiMzJmNzRmM2ZkMzcuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGF0dGFjaG1lbnRzXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9tb2RlbCc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIG5iZm9ybWF0IGZyb20gJ0BqdXB5dGVybGFiL25iZm9ybWF0JztcbmltcG9ydCB7XG4gIElNb2RlbERCLFxuICBJT2JzZXJ2YWJsZU1hcCxcbiAgSU9ic2VydmFibGVWYWx1ZSxcbiAgT2JzZXJ2YWJsZU1hcCxcbiAgT2JzZXJ2YWJsZVZhbHVlXG59IGZyb20gJ0BqdXB5dGVybGFiL29ic2VydmFibGVzJztcbmltcG9ydCB7XG4gIEF0dGFjaG1lbnRNb2RlbCxcbiAgSUF0dGFjaG1lbnRNb2RlbCxcbiAgaW1hZ2VSZW5kZXJlckZhY3Rvcnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJUmVuZGVyTWltZSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUtaW50ZXJmYWNlcyc7XG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5cbi8qKlxuICogVGhlIG1vZGVsIGZvciBhdHRhY2htZW50cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJQXR0YWNobWVudHNNb2RlbCBleHRlbmRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbW9kZWwgc3RhdGUgY2hhbmdlcy5cbiAgICovXG4gIHJlYWRvbmx5IHN0YXRlQ2hhbmdlZDogSVNpZ25hbDxJQXR0YWNobWVudHNNb2RlbCwgdm9pZD47XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbW9kZWwgY2hhbmdlcy5cbiAgICovXG4gIHJlYWRvbmx5IGNoYW5nZWQ6IElTaWduYWw8SUF0dGFjaG1lbnRzTW9kZWwsIElBdHRhY2htZW50c01vZGVsLkNoYW5nZWRBcmdzPjtcblxuICAvKipcbiAgICogVGhlIGxlbmd0aCBvZiB0aGUgaXRlbXMgaW4gdGhlIG1vZGVsLlxuICAgKi9cbiAgcmVhZG9ubHkgbGVuZ3RoOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFRoZSBrZXlzIG9mIHRoZSBhdHRhY2htZW50cyBpbiB0aGUgbW9kZWwuXG4gICAqL1xuICByZWFkb25seSBrZXlzOiBSZWFkb25seUFycmF5PHN0cmluZz47XG5cbiAgLyoqXG4gICAqIFRoZSBhdHRhY2htZW50IGNvbnRlbnQgZmFjdG9yeSB1c2VkIGJ5IHRoZSBtb2RlbC5cbiAgICovXG4gIHJlYWRvbmx5IGNvbnRlbnRGYWN0b3J5OiBJQXR0YWNobWVudHNNb2RlbC5JQ29udGVudEZhY3Rvcnk7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIHNwZWNpZmllZCBrZXkgaXMgc2V0LlxuICAgKi9cbiAgaGFzKGtleTogc3RyaW5nKTogYm9vbGVhbjtcblxuICAvKipcbiAgICogR2V0IGFuIGl0ZW0gZm9yIHRoZSBzcGVjaWZpZWQga2V5LlxuICAgKi9cbiAgZ2V0KGtleTogc3RyaW5nKTogSUF0dGFjaG1lbnRNb2RlbCB8IHVuZGVmaW5lZDtcblxuICAvKipcbiAgICogU2V0IHRoZSB2YWx1ZSBvZiB0aGUgc3BlY2lmaWVkIGtleS5cbiAgICovXG4gIHNldChrZXk6IHN0cmluZywgYXR0YWNobWVudDogbmJmb3JtYXQuSU1pbWVCdW5kbGUpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgdGhlIGF0dGFjaG1lbnQgd2hvc2UgbmFtZSBpcyB0aGUgc3BlY2lmaWVkIGtleS5cbiAgICogTm90ZSB0aGF0IHRoaXMgaXMgb3B0aW9uYWwgb25seSB1bnRpbCBKdXB5dGVybGFiIDIuMCByZWxlYXNlLlxuICAgKi9cbiAgcmVtb3ZlOiAoa2V5OiBzdHJpbmcpID0+IHZvaWQ7XG5cbiAgLyoqXG4gICAqIENsZWFyIGFsbCBvZiB0aGUgYXR0YWNobWVudHMuXG4gICAqL1xuICBjbGVhcigpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBEZXNlcmlhbGl6ZSB0aGUgbW9kZWwgZnJvbSBKU09OLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgd2lsbCBjbGVhciBhbnkgZXhpc3RpbmcgZGF0YS5cbiAgICovXG4gIGZyb21KU09OKHZhbHVlczogbmJmb3JtYXQuSUF0dGFjaG1lbnRzKTogdm9pZDtcblxuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IG5iZm9ybWF0LklBdHRhY2htZW50cztcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBJQXR0YWNobWVudHNNb2RlbCBpbnRlcmZhY2VzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElBdHRhY2htZW50c01vZGVsIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGEgYXR0YWNobWVudHMgbW9kZWwuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgaW5pdGlhbCB2YWx1ZXMgZm9yIHRoZSBtb2RlbC5cbiAgICAgKi9cbiAgICB2YWx1ZXM/OiBuYmZvcm1hdC5JQXR0YWNobWVudHM7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXR0YWNobWVudCBjb250ZW50IGZhY3RvcnkgdXNlZCBieSB0aGUgbW9kZWwuXG4gICAgICpcbiAgICAgKiBJZiBub3QgZ2l2ZW4sIGEgZGVmYXVsdCBmYWN0b3J5IHdpbGwgYmUgdXNlZC5cbiAgICAgKi9cbiAgICBjb250ZW50RmFjdG9yeT86IElDb250ZW50RmFjdG9yeTtcblxuICAgIC8qKlxuICAgICAqIEFuIG9wdGlvbmFsIElNb2RlbERCIHRvIHN0b3JlIHRoZSBhdHRhY2htZW50cyBtb2RlbC5cbiAgICAgKi9cbiAgICBtb2RlbERCPzogSU1vZGVsREI7XG4gIH1cblxuICAvKipcbiAgICogQSB0eXBlIGFsaWFzIGZvciBjaGFuZ2VkIGFyZ3MuXG4gICAqL1xuICBleHBvcnQgdHlwZSBDaGFuZ2VkQXJncyA9IElPYnNlcnZhYmxlTWFwLklDaGFuZ2VkQXJnczxJQXR0YWNobWVudE1vZGVsPjtcblxuICAvKipcbiAgICogVGhlIGludGVyZmFjZSBmb3IgYW4gYXR0YWNobWVudCBjb250ZW50IGZhY3RvcnkuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDb250ZW50RmFjdG9yeSB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGFuIGF0dGFjaG1lbnQgbW9kZWwuXG4gICAgICovXG4gICAgY3JlYXRlQXR0YWNobWVudE1vZGVsKG9wdGlvbnM6IElBdHRhY2htZW50TW9kZWwuSU9wdGlvbnMpOiBJQXR0YWNobWVudE1vZGVsO1xuICB9XG59XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgaW1wbGVtZW50YXRpb24gb2YgdGhlIElBdHRhY2htZW50c01vZGVsLlxuICovXG5leHBvcnQgY2xhc3MgQXR0YWNobWVudHNNb2RlbCBpbXBsZW1lbnRzIElBdHRhY2htZW50c01vZGVsIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBvYnNlcnZhYmxlIG91dHB1dHMgaW5zdGFuY2UuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJQXR0YWNobWVudHNNb2RlbC5JT3B0aW9ucyA9IHt9KSB7XG4gICAgdGhpcy5jb250ZW50RmFjdG9yeSA9XG4gICAgICBvcHRpb25zLmNvbnRlbnRGYWN0b3J5IHx8IEF0dGFjaG1lbnRzTW9kZWwuZGVmYXVsdENvbnRlbnRGYWN0b3J5O1xuICAgIGlmIChvcHRpb25zLnZhbHVlcykge1xuICAgICAgZm9yIChjb25zdCBrZXkgb2YgT2JqZWN0LmtleXMob3B0aW9ucy52YWx1ZXMpKSB7XG4gICAgICAgIGlmIChvcHRpb25zLnZhbHVlc1trZXldICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICB0aGlzLnNldChrZXksIG9wdGlvbnMudmFsdWVzW2tleV0hKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICB0aGlzLl9tYXAuY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uTWFwQ2hhbmdlZCwgdGhpcyk7XG5cbiAgICAvLyBJZiB3ZSBhcmUgZ2l2ZW4gYSBJTW9kZWxEQiwga2VlcCBhbiB1cC10by1kYXRlXG4gICAgLy8gc2VyaWFsaXplZCBjb3B5IG9mIHRoZSBBdHRhY2htZW50c01vZGVsIGluIGl0LlxuICAgIGlmIChvcHRpb25zLm1vZGVsREIpIHtcbiAgICAgIHRoaXMuX21vZGVsREIgPSBvcHRpb25zLm1vZGVsREI7XG4gICAgICB0aGlzLl9zZXJpYWxpemVkID0gdGhpcy5fbW9kZWxEQi5jcmVhdGVWYWx1ZSgnYXR0YWNobWVudHMnKTtcbiAgICAgIGlmICh0aGlzLl9zZXJpYWxpemVkLmdldCgpKSB7XG4gICAgICAgIHRoaXMuZnJvbUpTT04odGhpcy5fc2VyaWFsaXplZC5nZXQoKSBhcyBuYmZvcm1hdC5JQXR0YWNobWVudHMpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgdGhpcy5fc2VyaWFsaXplZC5zZXQodGhpcy50b0pTT04oKSk7XG4gICAgICB9XG4gICAgICB0aGlzLl9zZXJpYWxpemVkLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vblNlcmlhbGl6ZWRDaGFuZ2VkLCB0aGlzKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBtb2RlbCBzdGF0ZSBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IHN0YXRlQ2hhbmdlZCgpOiBJU2lnbmFsPElBdHRhY2htZW50c01vZGVsLCB2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3N0YXRlQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIG1vZGVsIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgY2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElBdHRhY2htZW50c01vZGVsLkNoYW5nZWRBcmdzPiB7XG4gICAgcmV0dXJuIHRoaXMuX2NoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGtleXMgb2YgdGhlIGF0dGFjaG1lbnRzIGluIHRoZSBtb2RlbC5cbiAgICovXG4gIGdldCBrZXlzKCk6IFJlYWRvbmx5QXJyYXk8c3RyaW5nPiB7XG4gICAgcmV0dXJuIHRoaXMuX21hcC5rZXlzKCk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBsZW5ndGggb2YgdGhlIGl0ZW1zIGluIHRoZSBtb2RlbC5cbiAgICovXG4gIGdldCBsZW5ndGgoKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy5fbWFwLmtleXMoKS5sZW5ndGg7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGF0dGFjaG1lbnQgY29udGVudCBmYWN0b3J5IHVzZWQgYnkgdGhlIG1vZGVsLlxuICAgKi9cbiAgcmVhZG9ubHkgY29udGVudEZhY3Rvcnk6IElBdHRhY2htZW50c01vZGVsLklDb250ZW50RmFjdG9yeTtcblxuICAvKipcbiAgICogVGVzdCB3aGV0aGVyIHRoZSBtb2RlbCBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyB1c2VkIGJ5IHRoZSBtb2RlbC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICB0aGlzLl9tYXAuZGlzcG9zZSgpO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgc3BlY2lmaWVkIGtleSBpcyBzZXQuXG4gICAqL1xuICBoYXMoa2V5OiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fbWFwLmhhcyhrZXkpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhbiBpdGVtIGF0IHRoZSBzcGVjaWZpZWQga2V5LlxuICAgKi9cbiAgZ2V0KGtleTogc3RyaW5nKTogSUF0dGFjaG1lbnRNb2RlbCB8IHVuZGVmaW5lZCB7XG4gICAgcmV0dXJuIHRoaXMuX21hcC5nZXQoa2V5KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHZhbHVlIGF0IHRoZSBzcGVjaWZpZWQga2V5LlxuICAgKi9cbiAgc2V0KGtleTogc3RyaW5nLCB2YWx1ZTogbmJmb3JtYXQuSU1pbWVCdW5kbGUpOiB2b2lkIHtcbiAgICAvLyBOb3JtYWxpemUgc3RyZWFtIGRhdGEuXG4gICAgY29uc3QgaXRlbSA9IHRoaXMuX2NyZWF0ZUl0ZW0oeyB2YWx1ZSB9KTtcbiAgICB0aGlzLl9tYXAuc2V0KGtleSwgaXRlbSk7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIHRoZSBhdHRhY2htZW50IHdob3NlIG5hbWUgaXMgdGhlIHNwZWNpZmllZCBrZXlcbiAgICovXG4gIHJlbW92ZShrZXk6IHN0cmluZyk6IHZvaWQge1xuICAgIHRoaXMuX21hcC5kZWxldGUoa2V5KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhciBhbGwgb2YgdGhlIGF0dGFjaG1lbnRzLlxuICAgKi9cbiAgY2xlYXIoKTogdm9pZCB7XG4gICAgdGhpcy5fbWFwLnZhbHVlcygpLmZvckVhY2goKGl0ZW06IElBdHRhY2htZW50TW9kZWwpID0+IHtcbiAgICAgIGl0ZW0uZGlzcG9zZSgpO1xuICAgIH0pO1xuICAgIHRoaXMuX21hcC5jbGVhcigpO1xuICB9XG5cbiAgLyoqXG4gICAqIERlc2VyaWFsaXplIHRoZSBtb2RlbCBmcm9tIEpTT04uXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyB3aWxsIGNsZWFyIGFueSBleGlzdGluZyBkYXRhLlxuICAgKi9cbiAgZnJvbUpTT04odmFsdWVzOiBuYmZvcm1hdC5JQXR0YWNobWVudHMpIHtcbiAgICB0aGlzLmNsZWFyKCk7XG4gICAgT2JqZWN0LmtleXModmFsdWVzKS5mb3JFYWNoKGtleSA9PiB7XG4gICAgICBpZiAodmFsdWVzW2tleV0gIT09IHVuZGVmaW5lZCkge1xuICAgICAgICB0aGlzLnNldChrZXksIHZhbHVlc1trZXldISk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IG5iZm9ybWF0LklBdHRhY2htZW50cyB7XG4gICAgY29uc3QgcmV0OiBuYmZvcm1hdC5JQXR0YWNobWVudHMgPSB7fTtcbiAgICBmb3IgKGNvbnN0IGtleSBvZiB0aGlzLl9tYXAua2V5cygpKSB7XG4gICAgICByZXRba2V5XSA9IHRoaXMuX21hcC5nZXQoa2V5KSEudG9KU09OKCk7XG4gICAgfVxuICAgIHJldHVybiByZXQ7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGFuIGF0dGFjaG1lbnQgaXRlbSBhbmQgaG9vayB1cCBpdHMgc2lnbmFscy5cbiAgICovXG4gIHByaXZhdGUgX2NyZWF0ZUl0ZW0ob3B0aW9uczogSUF0dGFjaG1lbnRNb2RlbC5JT3B0aW9ucyk6IElBdHRhY2htZW50TW9kZWwge1xuICAgIGNvbnN0IGZhY3RvcnkgPSB0aGlzLmNvbnRlbnRGYWN0b3J5O1xuICAgIGNvbnN0IGl0ZW0gPSBmYWN0b3J5LmNyZWF0ZUF0dGFjaG1lbnRNb2RlbChvcHRpb25zKTtcbiAgICBpdGVtLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkdlbmVyaWNDaGFuZ2UsIHRoaXMpO1xuICAgIHJldHVybiBpdGVtO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgbGlzdC5cbiAgICovXG4gIHByaXZhdGUgX29uTWFwQ2hhbmdlZChcbiAgICBzZW5kZXI6IElPYnNlcnZhYmxlTWFwPElBdHRhY2htZW50TW9kZWw+LFxuICAgIGFyZ3M6IElPYnNlcnZhYmxlTWFwLklDaGFuZ2VkQXJnczxJQXR0YWNobWVudE1vZGVsPlxuICApIHtcbiAgICBpZiAodGhpcy5fc2VyaWFsaXplZCAmJiAhdGhpcy5fY2hhbmdlR3VhcmQpIHtcbiAgICAgIHRoaXMuX2NoYW5nZUd1YXJkID0gdHJ1ZTtcbiAgICAgIHRoaXMuX3NlcmlhbGl6ZWQuc2V0KHRoaXMudG9KU09OKCkpO1xuICAgICAgdGhpcy5fY2hhbmdlR3VhcmQgPSBmYWxzZTtcbiAgICB9XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KGFyZ3MpO1xuICAgIHRoaXMuX3N0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gIH1cblxuICAvKipcbiAgICogSWYgdGhlIHNlcmlhbGl6ZWQgdmVyc2lvbiBvZiB0aGUgb3V0cHV0cyBoYXZlIGNoYW5nZWQgZHVlIHRvIGEgcmVtb3RlXG4gICAqIGFjdGlvbiwgdGhlbiB1cGRhdGUgdGhlIG1vZGVsIGFjY29yZGluZ2x5LlxuICAgKi9cbiAgcHJpdmF0ZSBfb25TZXJpYWxpemVkQ2hhbmdlZChcbiAgICBzZW5kZXI6IElPYnNlcnZhYmxlVmFsdWUsXG4gICAgYXJnczogT2JzZXJ2YWJsZVZhbHVlLklDaGFuZ2VkQXJnc1xuICApIHtcbiAgICBpZiAoIXRoaXMuX2NoYW5nZUd1YXJkKSB7XG4gICAgICB0aGlzLl9jaGFuZ2VHdWFyZCA9IHRydWU7XG4gICAgICB0aGlzLmZyb21KU09OKGFyZ3MubmV3VmFsdWUgYXMgbmJmb3JtYXQuSUF0dGFjaG1lbnRzKTtcbiAgICAgIHRoaXMuX2NoYW5nZUd1YXJkID0gZmFsc2U7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byBhbiBpdGVtLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25HZW5lcmljQ2hhbmdlKCk6IHZvaWQge1xuICAgIHRoaXMuX3N0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gIH1cblxuICBwcml2YXRlIF9tYXAgPSBuZXcgT2JzZXJ2YWJsZU1hcDxJQXR0YWNobWVudE1vZGVsPigpO1xuICBwcml2YXRlIF9pc0Rpc3Bvc2VkID0gZmFsc2U7XG4gIHByaXZhdGUgX3N0YXRlQ2hhbmdlZCA9IG5ldyBTaWduYWw8SUF0dGFjaG1lbnRzTW9kZWwsIHZvaWQ+KHRoaXMpO1xuICBwcml2YXRlIF9jaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBJQXR0YWNobWVudHNNb2RlbC5DaGFuZ2VkQXJncz4odGhpcyk7XG4gIHByaXZhdGUgX21vZGVsREI6IElNb2RlbERCIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX3NlcmlhbGl6ZWQ6IElPYnNlcnZhYmxlVmFsdWUgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfY2hhbmdlR3VhcmQgPSBmYWxzZTtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBBdHRhY2htZW50c01vZGVsIGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgQXR0YWNobWVudHNNb2RlbCB7XG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBpbXBsZW1lbnRhdGlvbiBvZiBhIGBJQXR0YWNobWVudHNNb2RlbC5JQ29udGVudEZhY3RvcnlgLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIENvbnRlbnRGYWN0b3J5IGltcGxlbWVudHMgSUF0dGFjaG1lbnRzTW9kZWwuSUNvbnRlbnRGYWN0b3J5IHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYW4gYXR0YWNobWVudCBtb2RlbC5cbiAgICAgKi9cbiAgICBjcmVhdGVBdHRhY2htZW50TW9kZWwoXG4gICAgICBvcHRpb25zOiBJQXR0YWNobWVudE1vZGVsLklPcHRpb25zXG4gICAgKTogSUF0dGFjaG1lbnRNb2RlbCB7XG4gICAgICByZXR1cm4gbmV3IEF0dGFjaG1lbnRNb2RlbChvcHRpb25zKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRlZmF1bHQgYXR0YWNobWVudCBtb2RlbCBmYWN0b3J5LlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRDb250ZW50RmFjdG9yeSA9IG5ldyBDb250ZW50RmFjdG9yeSgpO1xufVxuXG4vKipcbiAqIEEgcmVzb2x2ZXIgZm9yIGNlbGwgYXR0YWNobWVudHMgJ2F0dGFjaG1lbnQ6ZmlsZW5hbWUnLlxuICpcbiAqIFdpbGwgcmVzb2x2ZSB0byBhIGRhdGE6IHVybC5cbiAqL1xuZXhwb3J0IGNsYXNzIEF0dGFjaG1lbnRzUmVzb2x2ZXIgaW1wbGVtZW50cyBJUmVuZGVyTWltZS5JUmVzb2x2ZXIge1xuICAvKipcbiAgICogQ3JlYXRlIGFuIGF0dGFjaG1lbnRzIHJlc29sdmVyIG9iamVjdC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IEF0dGFjaG1lbnRzUmVzb2x2ZXIuSU9wdGlvbnMpIHtcbiAgICB0aGlzLl9wYXJlbnQgPSBvcHRpb25zLnBhcmVudCB8fCBudWxsO1xuICAgIHRoaXMuX21vZGVsID0gb3B0aW9ucy5tb2RlbDtcbiAgfVxuICAvKipcbiAgICogUmVzb2x2ZSBhIHJlbGF0aXZlIHVybCB0byBhIGNvcnJlY3Qgc2VydmVyIHBhdGguXG4gICAqL1xuICBhc3luYyByZXNvbHZlVXJsKHVybDogc3RyaW5nKTogUHJvbWlzZTxzdHJpbmc+IHtcbiAgICBpZiAodGhpcy5fcGFyZW50ICYmICF1cmwuc3RhcnRzV2l0aCgnYXR0YWNobWVudDonKSkge1xuICAgICAgcmV0dXJuIHRoaXMuX3BhcmVudC5yZXNvbHZlVXJsKHVybCk7XG4gICAgfVxuICAgIHJldHVybiB1cmw7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBkb3dubG9hZCB1cmwgb2YgYSBnaXZlbiBhYnNvbHV0ZSBzZXJ2ZXIgcGF0aC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgcmV0dXJuZWQgVVJMIG1heSBpbmNsdWRlIGEgcXVlcnkgcGFyYW1ldGVyLlxuICAgKi9cbiAgYXN5bmMgZ2V0RG93bmxvYWRVcmwocGF0aDogc3RyaW5nKTogUHJvbWlzZTxzdHJpbmc+IHtcbiAgICBpZiAodGhpcy5fcGFyZW50ICYmICFwYXRoLnN0YXJ0c1dpdGgoJ2F0dGFjaG1lbnQ6JykpIHtcbiAgICAgIHJldHVybiB0aGlzLl9wYXJlbnQuZ2V0RG93bmxvYWRVcmwocGF0aCk7XG4gICAgfVxuICAgIC8vIFJldHVybiBhIGRhdGEgVVJMIHdpdGggdGhlIGRhdGEgb2YgdGhlIHVybFxuICAgIGNvbnN0IGtleSA9IHBhdGguc2xpY2UoJ2F0dGFjaG1lbnQ6Jy5sZW5ndGgpO1xuICAgIGNvbnN0IGF0dGFjaG1lbnQgPSB0aGlzLl9tb2RlbC5nZXQoa2V5KTtcbiAgICBpZiAoYXR0YWNobWVudCA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAvLyBSZXNvbHZlIHdpdGggdW5wcm9jZXNzZWQgcGF0aCwgdG8gc2hvdyBhcyBicm9rZW4gaW1hZ2VcbiAgICAgIHJldHVybiBwYXRoO1xuICAgIH1cbiAgICBjb25zdCB7IGRhdGEgfSA9IGF0dGFjaG1lbnQ7XG4gICAgY29uc3QgbWltZVR5cGUgPSBPYmplY3Qua2V5cyhkYXRhKVswXTtcbiAgICAvLyBPbmx5IHN1cHBvcnQga25vd24gc2FmZSB0eXBlczpcbiAgICBpZiAoXG4gICAgICBtaW1lVHlwZSA9PT0gdW5kZWZpbmVkIHx8XG4gICAgICBpbWFnZVJlbmRlcmVyRmFjdG9yeS5taW1lVHlwZXMuaW5kZXhPZihtaW1lVHlwZSkgPT09IC0xXG4gICAgKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYENhbm5vdCByZW5kZXIgdW5rbm93biBpbWFnZSBtaW1lIHR5cGUgXCIke21pbWVUeXBlfVwiLmApO1xuICAgIH1cbiAgICBjb25zdCBkYXRhVXJsID0gYGRhdGE6JHttaW1lVHlwZX07YmFzZTY0LCR7ZGF0YVttaW1lVHlwZV19YDtcbiAgICByZXR1cm4gZGF0YVVybDtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBVUkwgc2hvdWxkIGJlIGhhbmRsZWQgYnkgdGhlIHJlc29sdmVyXG4gICAqIG9yIG5vdC5cbiAgICovXG4gIGlzTG9jYWwodXJsOiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICBpZiAodGhpcy5fcGFyZW50ICYmICF1cmwuc3RhcnRzV2l0aCgnYXR0YWNobWVudDonKSkge1xuICAgICAgcmV0dXJuIHRoaXMuX3BhcmVudC5pc0xvY2FsPy4odXJsKSA/PyB0cnVlO1xuICAgIH1cbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxuXG4gIHByaXZhdGUgX21vZGVsOiBJQXR0YWNobWVudHNNb2RlbDtcbiAgcHJpdmF0ZSBfcGFyZW50OiBJUmVuZGVyTWltZS5JUmVzb2x2ZXIgfCBudWxsO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGBBdHRhY2htZW50c1Jlc29sdmVyYCBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIEF0dGFjaG1lbnRzUmVzb2x2ZXIge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBjcmVhdGUgYW4gQXR0YWNobWVudHNSZXNvbHZlci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBhdHRhY2htZW50cyBtb2RlbCB0byByZXNvbHZlIGFnYWluc3QuXG4gICAgICovXG4gICAgbW9kZWw6IElBdHRhY2htZW50c01vZGVsO1xuXG4gICAgLyoqXG4gICAgICogQSBwYXJlbnQgcmVzb2x2ZXIgdG8gdXNlIGlmIHRoZSBVUkwvcGF0aCBpcyBub3QgZm9yIGFuIGF0dGFjaG1lbnQuXG4gICAgICovXG4gICAgcGFyZW50PzogSVJlbmRlck1pbWUuSVJlc29sdmVyO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9