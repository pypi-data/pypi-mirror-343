(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_inspector_lib_index_js"],{

/***/ "../packages/inspector/lib/handler.js":
/*!********************************************!*\
  !*** ../packages/inspector/lib/handler.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "InspectionHandler": () => (/* binding */ InspectionHandler)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/polling */ "webpack/sharing/consume/default/@lumino/polling/@lumino/polling");
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_polling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * An object that handles code inspection.
 */
class InspectionHandler {
    /**
     * Construct a new inspection handler for a widget.
     */
    constructor(options) {
        this._cleared = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._disposed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._editor = null;
        this._inspected = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._isDisposed = false;
        this._pending = 0;
        this._standby = true;
        this._lastInspectedReply = null;
        this._connector = options.connector;
        this._rendermime = options.rendermime;
        this._debouncer = new _lumino_polling__WEBPACK_IMPORTED_MODULE_3__.Debouncer(this.onEditorChange.bind(this), 250);
    }
    /**
     * A signal emitted when the inspector should clear all items.
     */
    get cleared() {
        return this._cleared;
    }
    /**
     * A signal emitted when the handler is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * A signal emitted when an inspector value is generated.
     */
    get inspected() {
        return this._inspected;
    }
    /**
     * The editor widget used by the inspection handler.
     */
    get editor() {
        return this._editor;
    }
    set editor(newValue) {
        if (newValue === this._editor) {
            return;
        }
        // Remove all of our listeners.
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.disconnectReceiver(this);
        const editor = (this._editor = newValue);
        if (editor) {
            // Clear the inspector in preparation for a new editor.
            this._cleared.emit(void 0);
            // Call onEditorChange to cover the case where the user changes
            // the active cell
            this.onEditorChange();
            editor.model.selections.changed.connect(this._onChange, this);
            editor.model.value.changed.connect(this._onChange, this);
        }
    }
    /**
     * Indicates whether the handler makes API inspection requests or stands by.
     *
     * #### Notes
     * The use case for this attribute is to limit the API traffic when no
     * inspector is visible.
     */
    get standby() {
        return this._standby;
    }
    set standby(value) {
        this._standby = value;
    }
    /**
     * Get whether the inspection handler is disposed.
     *
     * #### Notes
     * This is a read-only property.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._disposed.emit(void 0);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.clearData(this);
    }
    /**
     * Handle a text changed signal from an editor.
     *
     * #### Notes
     * Update the hints inspector based on a text change.
     */
    onEditorChange(customText) {
        // If the handler is in standby mode, bail.
        if (this._standby) {
            return;
        }
        const editor = this.editor;
        if (!editor) {
            return;
        }
        const text = customText ? customText : editor.model.value.text;
        const position = editor.getCursorPosition();
        const offset = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.Text.jsIndexToCharIndex(editor.getOffsetAt(position), text);
        const update = { content: null };
        const pending = ++this._pending;
        void this._connector
            .fetch({ offset, text })
            .then(reply => {
            // If handler has been disposed or a newer request is pending, bail.
            if (!reply || this.isDisposed || pending !== this._pending) {
                this._lastInspectedReply = null;
                this._inspected.emit(update);
                return;
            }
            const { data } = reply;
            // Do not update if there would be no change.
            if (this._lastInspectedReply &&
                _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(this._lastInspectedReply, data)) {
                return;
            }
            const mimeType = this._rendermime.preferredMimeType(data);
            if (mimeType) {
                const widget = this._rendermime.createRenderer(mimeType);
                const model = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.MimeModel({ data });
                void widget.renderModel(model);
                update.content = widget;
            }
            this._lastInspectedReply = reply.data;
            this._inspected.emit(update);
        })
            .catch(reason => {
            // Since almost all failures are benign, fail silently.
            this._lastInspectedReply = null;
            this._inspected.emit(update);
        });
    }
    /**
     * Handle changes to the editor state, debouncing.
     */
    _onChange() {
        void this._debouncer.invoke();
    }
}


/***/ }),

/***/ "../packages/inspector/lib/index.js":
/*!******************************************!*\
  !*** ../packages/inspector/lib/index.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "InspectionHandler": () => (/* reexport safe */ _handler__WEBPACK_IMPORTED_MODULE_0__.InspectionHandler),
/* harmony export */   "InspectorPanel": () => (/* reexport safe */ _inspector__WEBPACK_IMPORTED_MODULE_1__.InspectorPanel),
/* harmony export */   "KernelConnector": () => (/* reexport safe */ _kernelconnector__WEBPACK_IMPORTED_MODULE_2__.KernelConnector),
/* harmony export */   "IInspector": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.IInspector)
/* harmony export */ });
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./handler */ "../packages/inspector/lib/handler.js");
/* harmony import */ var _inspector__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./inspector */ "../packages/inspector/lib/inspector.js");
/* harmony import */ var _kernelconnector__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./kernelconnector */ "../packages/inspector/lib/kernelconnector.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tokens */ "../packages/inspector/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module inspector
 */






/***/ }),

/***/ "../packages/inspector/lib/inspector.js":
/*!**********************************************!*\
  !*** ../packages/inspector/lib/inspector.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "InspectorPanel": () => (/* binding */ InspectorPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The class name added to inspector panels.
 */
const PANEL_CLASS = 'jp-Inspector';
/**
 * The class name added to inspector content.
 */
const CONTENT_CLASS = 'jp-Inspector-content';
/**
 * The class name added to default inspector content.
 */
const DEFAULT_CONTENT_CLASS = 'jp-Inspector-default-content';
/**
 * A panel which contains a set of inspectors.
 */
class InspectorPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel {
    /**
     * Construct an inspector.
     */
    constructor(options = {}) {
        super();
        this._source = null;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        if (options.initialContent instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget) {
            this._content = options.initialContent;
        }
        else if (typeof options.initialContent === 'string') {
            this._content = InspectorPanel._generateContentWidget(`<p>${options.initialContent}</p>`);
        }
        else {
            this._content = InspectorPanel._generateContentWidget('<p>' +
                this._trans.__('Click on a function to see documentation.') +
                '</p>');
        }
        this.addClass(PANEL_CLASS);
        this.layout.addWidget(this._content);
    }
    /**
     * Print in iframe
     */
    [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.symbol]() {
        return () => _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.printWidget(this);
    }
    /**
     * The source of events the inspector panel listens for.
     */
    get source() {
        return this._source;
    }
    set source(source) {
        if (this._source === source) {
            return;
        }
        // Disconnect old signal handler.
        if (this._source) {
            this._source.standby = true;
            this._source.inspected.disconnect(this.onInspectorUpdate, this);
            this._source.disposed.disconnect(this.onSourceDisposed, this);
        }
        // Reject a source that is already disposed.
        if (source && source.isDisposed) {
            source = null;
        }
        // Update source.
        this._source = source;
        // Connect new signal handler.
        if (this._source) {
            this._source.standby = false;
            this._source.inspected.connect(this.onInspectorUpdate, this);
            this._source.disposed.connect(this.onSourceDisposed, this);
        }
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.source = null;
        super.dispose();
    }
    /**
     * Handle inspector update signals.
     */
    onInspectorUpdate(sender, args) {
        const { content } = args;
        // Update the content of the inspector widget.
        if (!content || content === this._content) {
            return;
        }
        this._content.dispose();
        this._content = content;
        content.addClass(CONTENT_CLASS);
        this.layout.addWidget(content);
    }
    /**
     * Handle source disposed signals.
     */
    onSourceDisposed(sender, args) {
        this.source = null;
    }
    /**
     * Generate content widget from string
     */
    static _generateContentWidget(message) {
        const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget();
        widget.node.innerHTML = message;
        widget.addClass(CONTENT_CLASS);
        widget.addClass(DEFAULT_CONTENT_CLASS);
        return widget;
    }
}


/***/ }),

/***/ "../packages/inspector/lib/kernelconnector.js":
/*!****************************************************!*\
  !*** ../packages/inspector/lib/kernelconnector.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelConnector": () => (/* binding */ KernelConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The default connector for making inspection requests from the Jupyter API.
 */
class KernelConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new kernel connector for inspection requests.
     *
     * @param options - The instantiation options for the kernel connector.
     */
    constructor(options) {
        super();
        this._sessionContext = options.sessionContext;
    }
    /**
     * Fetch inspection requests.
     *
     * @param request - The inspection request text and details.
     */
    fetch(request) {
        var _a;
        const kernel = (_a = this._sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return Promise.reject(new Error('Inspection fetch requires a kernel.'));
        }
        const contents = {
            code: request.text,
            cursor_pos: request.offset,
            detail_level: 1
        };
        return kernel.requestInspect(contents).then(msg => {
            const response = msg.content;
            if (response.status !== 'ok' || !response.found) {
                throw new Error('Inspection fetch failed to return successfully.');
            }
            return { data: response.data, metadata: response.metadata };
        });
    }
}


/***/ }),

/***/ "../packages/inspector/lib/tokens.js":
/*!*******************************************!*\
  !*** ../packages/inspector/lib/tokens.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IInspector": () => (/* binding */ IInspector)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The inspector panel token.
 */
const IInspector = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/inspector:IInspector');


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW5zcGVjdG9yL3NyYy9oYW5kbGVyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9pbnNwZWN0b3Ivc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9pbnNwZWN0b3Ivc3JjL2luc3BlY3Rvci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW5zcGVjdG9yL3NyYy9rZXJuZWxjb25uZWN0b3IudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2luc3BlY3Rvci9zcmMvdG9rZW5zLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUdkO0FBQzJCO0FBRVI7QUFFcEI7QUFDUTtBQUdwRDs7R0FFRztBQUNJLE1BQU0saUJBQWlCO0lBQzVCOztPQUVHO0lBQ0gsWUFBWSxPQUFtQztRQThKdkMsYUFBUSxHQUFHLElBQUkscURBQU0sQ0FBMEIsSUFBSSxDQUFDLENBQUM7UUFNckQsY0FBUyxHQUFHLElBQUkscURBQU0sQ0FBYSxJQUFJLENBQUMsQ0FBQztRQUN6QyxZQUFPLEdBQThCLElBQUksQ0FBQztRQUMxQyxlQUFVLEdBQUcsSUFBSSxxREFBTSxDQUFvQyxJQUFJLENBQUMsQ0FBQztRQUNqRSxnQkFBVyxHQUFHLEtBQUssQ0FBQztRQUNwQixhQUFRLEdBQUcsQ0FBQyxDQUFDO1FBRWIsYUFBUSxHQUFHLElBQUksQ0FBQztRQUVoQix3QkFBbUIsR0FBNEMsSUFBSSxDQUFDO1FBM0sxRSxJQUFJLENBQUMsVUFBVSxHQUFHLE9BQU8sQ0FBQyxTQUFTLENBQUM7UUFD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QyxHQUFHLENBQUMsRUFBRTtZQUNoRCxNQUFNLFFBQVEsR0FBRyxHQUFHLENBQUMsT0FBTyxDQUFDO1lBRTdCLElBQUksUUFBUSxDQUFDLE1BQU0sS0FBSyxJQUFJLElBQUksQ0FBQyxRQUFRLENBQUMsS0FBSyxFQUFFO2dCQUMvQyxNQUFNLElBQUksS0FBSyxDQUFDLGlEQUFpRCxDQUFDLENBQUM7YUFDcEU7WUFFRCxPQUFPLEVBQUUsSUFBSSxFQUFFLFFBQVEsQ0FBQyxJQUFJLEVBQUUsUUFBUSxFQUFFLFFBQVEsQ0FBQyxRQUFRLEVBQUUsQ0FBQztRQUM5RCxDQUFDLENBQUMsQ0FBQztJQUNMLENBQUM7Q0FHRjs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDMURELDBDQUEwQztBQUMxQywyREFBMkQ7QUFFakI7QUFJMUMsb0JBQW9CO0FBQ3BCOztHQUVHO0FBQ0ksTUFBTSxVQUFVLEdBQUcsSUFBSSxvREFBSyxDQUNqQyxrQ0FBa0MsQ0FDbkMsQ0FBQyIsImZpbGUiOiJwYWNrYWdlc19pbnNwZWN0b3JfbGliX2luZGV4X2pzLjNhNGRkMmI1OGI2YWVkNGEyZjlmLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQgeyBUZXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnksIE1pbWVNb2RlbCB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgSURhdGFDb25uZWN0b3IgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7IEpTT05FeHQsIFJlYWRvbmx5SlNPTk9iamVjdCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IERlYm91bmNlciB9IGZyb20gJ0BsdW1pbm8vcG9sbGluZyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBJSW5zcGVjdG9yIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEFuIG9iamVjdCB0aGF0IGhhbmRsZXMgY29kZSBpbnNwZWN0aW9uLlxuICovXG5leHBvcnQgY2xhc3MgSW5zcGVjdGlvbkhhbmRsZXIgaW1wbGVtZW50cyBJRGlzcG9zYWJsZSwgSUluc3BlY3Rvci5JSW5zcGVjdGFibGUge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IGluc3BlY3Rpb24gaGFuZGxlciBmb3IgYSB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJbnNwZWN0aW9uSGFuZGxlci5JT3B0aW9ucykge1xuICAgIHRoaXMuX2Nvbm5lY3RvciA9IG9wdGlvbnMuY29ubmVjdG9yO1xuICAgIHRoaXMuX3JlbmRlcm1pbWUgPSBvcHRpb25zLnJlbmRlcm1pbWU7XG4gICAgdGhpcy5fZGVib3VuY2VyID0gbmV3IERlYm91bmNlcih0aGlzLm9uRWRpdG9yQ2hhbmdlLmJpbmQodGhpcyksIDI1MCk7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBpbnNwZWN0b3Igc2hvdWxkIGNsZWFyIGFsbCBpdGVtcy5cbiAgICovXG4gIGdldCBjbGVhcmVkKCk6IElTaWduYWw8SW5zcGVjdGlvbkhhbmRsZXIsIHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fY2xlYXJlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGhhbmRsZXIgaXMgZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgZGlzcG9zZWQoKTogSVNpZ25hbDxJbnNwZWN0aW9uSGFuZGxlciwgdm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9kaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gYW4gaW5zcGVjdG9yIHZhbHVlIGlzIGdlbmVyYXRlZC5cbiAgICovXG4gIGdldCBpbnNwZWN0ZWQoKTogSVNpZ25hbDxJbnNwZWN0aW9uSGFuZGxlciwgSUluc3BlY3Rvci5JSW5zcGVjdG9yVXBkYXRlPiB7XG4gICAgcmV0dXJuIHRoaXMuX2luc3BlY3RlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZWRpdG9yIHdpZGdldCB1c2VkIGJ5IHRoZSBpbnNwZWN0aW9uIGhhbmRsZXIuXG4gICAqL1xuICBnZXQgZWRpdG9yKCk6IENvZGVFZGl0b3IuSUVkaXRvciB8IG51bGwge1xuICAgIHJldHVybiB0aGlzLl9lZGl0b3I7XG4gIH1cbiAgc2V0IGVkaXRvcihuZXdWYWx1ZTogQ29kZUVkaXRvci5JRWRpdG9yIHwgbnVsbCkge1xuICAgIGlmIChuZXdWYWx1ZSA9PT0gdGhpcy5fZWRpdG9yKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIC8vIFJlbW92ZSBhbGwgb2Ygb3VyIGxpc3RlbmVycy5cbiAgICBTaWduYWwuZGlzY29ubmVjdFJlY2VpdmVyKHRoaXMpO1xuXG4gICAgY29uc3QgZWRpdG9yID0gKHRoaXMuX2VkaXRvciA9IG5ld1ZhbHVlKTtcbiAgICBpZiAoZWRpdG9yKSB7XG4gICAgICAvLyBDbGVhciB0aGUgaW5zcGVjdG9yIGluIHByZXBhcmF0aW9uIGZvciBhIG5ldyBlZGl0b3IuXG4gICAgICB0aGlzLl9jbGVhcmVkLmVtaXQodm9pZCAwKTtcbiAgICAgIC8vIENhbGwgb25FZGl0b3JDaGFuZ2UgdG8gY292ZXIgdGhlIGNhc2Ugd2hlcmUgdGhlIHVzZXIgY2hhbmdlc1xuICAgICAgLy8gdGhlIGFjdGl2ZSBjZWxsXG4gICAgICB0aGlzLm9uRWRpdG9yQ2hhbmdlKCk7XG4gICAgICBlZGl0b3IubW9kZWwuc2VsZWN0aW9ucy5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25DaGFuZ2UsIHRoaXMpO1xuICAgICAgZWRpdG9yLm1vZGVsLnZhbHVlLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkNoYW5nZSwgdGhpcyk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEluZGljYXRlcyB3aGV0aGVyIHRoZSBoYW5kbGVyIG1ha2VzIEFQSSBpbnNwZWN0aW9uIHJlcXVlc3RzIG9yIHN0YW5kcyBieS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgdXNlIGNhc2UgZm9yIHRoaXMgYXR0cmlidXRlIGlzIHRvIGxpbWl0IHRoZSBBUEkgdHJhZmZpYyB3aGVuIG5vXG4gICAqIGluc3BlY3RvciBpcyB2aXNpYmxlLlxuICAgKi9cbiAgZ2V0IHN0YW5kYnkoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX3N0YW5kYnk7XG4gIH1cbiAgc2V0IHN0YW5kYnkodmFsdWU6IGJvb2xlYW4pIHtcbiAgICB0aGlzLl9zdGFuZGJ5ID0gdmFsdWU7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHdoZXRoZXIgdGhlIGluc3BlY3Rpb24gaGFuZGxlciBpcyBkaXNwb3NlZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGlzIGEgcmVhZC1vbmx5IHByb3BlcnR5LlxuICAgKi9cbiAgZ2V0IGlzRGlzcG9zZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIHVzZWQgYnkgdGhlIGhhbmRsZXIuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgdGhpcy5fZGlzcG9zZWQuZW1pdCh2b2lkIDApO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgdGV4dCBjaGFuZ2VkIHNpZ25hbCBmcm9tIGFuIGVkaXRvci5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBVcGRhdGUgdGhlIGhpbnRzIGluc3BlY3RvciBiYXNlZCBvbiBhIHRleHQgY2hhbmdlLlxuICAgKi9cbiAgb25FZGl0b3JDaGFuZ2UoY3VzdG9tVGV4dD86IHN0cmluZyk6IHZvaWQge1xuICAgIC8vIElmIHRoZSBoYW5kbGVyIGlzIGluIHN0YW5kYnkgbW9kZSwgYmFpbC5cbiAgICBpZiAodGhpcy5fc3RhbmRieSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IGVkaXRvciA9IHRoaXMuZWRpdG9yO1xuXG4gICAgaWYgKCFlZGl0b3IpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgdGV4dCA9IGN1c3RvbVRleHQgPyBjdXN0b21UZXh0IDogZWRpdG9yLm1vZGVsLnZhbHVlLnRleHQ7XG4gICAgY29uc3QgcG9zaXRpb24gPSBlZGl0b3IuZ2V0Q3Vyc29yUG9zaXRpb24oKTtcbiAgICBjb25zdCBvZmZzZXQgPSBUZXh0LmpzSW5kZXhUb0NoYXJJbmRleChlZGl0b3IuZ2V0T2Zmc2V0QXQocG9zaXRpb24pLCB0ZXh0KTtcbiAgICBjb25zdCB1cGRhdGU6IElJbnNwZWN0b3IuSUluc3BlY3RvclVwZGF0ZSA9IHsgY29udGVudDogbnVsbCB9O1xuXG4gICAgY29uc3QgcGVuZGluZyA9ICsrdGhpcy5fcGVuZGluZztcblxuICAgIHZvaWQgdGhpcy5fY29ubmVjdG9yXG4gICAgICAuZmV0Y2goeyBvZmZzZXQsIHRleHQgfSlcbiAgICAgIC50aGVuKHJlcGx5ID0+IHtcbiAgICAgICAgLy8gSWYgaGFuZGxlciBoYXMgYmVlbiBkaXNwb3NlZCBvciBhIG5ld2VyIHJlcXVlc3QgaXMgcGVuZGluZywgYmFpbC5cbiAgICAgICAgaWYgKCFyZXBseSB8fCB0aGlzLmlzRGlzcG9zZWQgfHwgcGVuZGluZyAhPT0gdGhpcy5fcGVuZGluZykge1xuICAgICAgICAgIHRoaXMuX2xhc3RJbnNwZWN0ZWRSZXBseSA9IG51bGw7XG4gICAgICAgICAgdGhpcy5faW5zcGVjdGVkLmVtaXQodXBkYXRlKTtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCB7IGRhdGEgfSA9IHJlcGx5O1xuXG4gICAgICAgIC8vIERvIG5vdCB1cGRhdGUgaWYgdGhlcmUgd291bGQgYmUgbm8gY2hhbmdlLlxuICAgICAgICBpZiAoXG4gICAgICAgICAgdGhpcy5fbGFzdEluc3BlY3RlZFJlcGx5ICYmXG4gICAgICAgICAgSlNPTkV4dC5kZWVwRXF1YWwodGhpcy5fbGFzdEluc3BlY3RlZFJlcGx5LCBkYXRhKVxuICAgICAgICApIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBtaW1lVHlwZSA9IHRoaXMuX3JlbmRlcm1pbWUucHJlZmVycmVkTWltZVR5cGUoZGF0YSk7XG4gICAgICAgIGlmIChtaW1lVHlwZSkge1xuICAgICAgICAgIGNvbnN0IHdpZGdldCA9IHRoaXMuX3JlbmRlcm1pbWUuY3JlYXRlUmVuZGVyZXIobWltZVR5cGUpO1xuICAgICAgICAgIGNvbnN0IG1vZGVsID0gbmV3IE1pbWVNb2RlbCh7IGRhdGEgfSk7XG5cbiAgICAgICAgICB2b2lkIHdpZGdldC5yZW5kZXJNb2RlbChtb2RlbCk7XG4gICAgICAgICAgdXBkYXRlLmNvbnRlbnQgPSB3aWRnZXQ7XG4gICAgICAgIH1cblxuICAgICAgICB0aGlzLl9sYXN0SW5zcGVjdGVkUmVwbHkgPSByZXBseS5kYXRhO1xuICAgICAgICB0aGlzLl9pbnNwZWN0ZWQuZW1pdCh1cGRhdGUpO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICAvLyBTaW5jZSBhbG1vc3QgYWxsIGZhaWx1cmVzIGFyZSBiZW5pZ24sIGZhaWwgc2lsZW50bHkuXG4gICAgICAgIHRoaXMuX2xhc3RJbnNwZWN0ZWRSZXBseSA9IG51bGw7XG4gICAgICAgIHRoaXMuX2luc3BlY3RlZC5lbWl0KHVwZGF0ZSk7XG4gICAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgY2hhbmdlcyB0byB0aGUgZWRpdG9yIHN0YXRlLCBkZWJvdW5jaW5nLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25DaGFuZ2UoKTogdm9pZCB7XG4gICAgdm9pZCB0aGlzLl9kZWJvdW5jZXIuaW52b2tlKCk7XG4gIH1cblxuICBwcml2YXRlIF9jbGVhcmVkID0gbmV3IFNpZ25hbDxJbnNwZWN0aW9uSGFuZGxlciwgdm9pZD4odGhpcyk7XG4gIHByaXZhdGUgX2Nvbm5lY3RvcjogSURhdGFDb25uZWN0b3I8XG4gICAgSW5zcGVjdGlvbkhhbmRsZXIuSVJlcGx5LFxuICAgIHZvaWQsXG4gICAgSW5zcGVjdGlvbkhhbmRsZXIuSVJlcXVlc3RcbiAgPjtcbiAgcHJpdmF0ZSBfZGlzcG9zZWQgPSBuZXcgU2lnbmFsPHRoaXMsIHZvaWQ+KHRoaXMpO1xuICBwcml2YXRlIF9lZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvciB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9pbnNwZWN0ZWQgPSBuZXcgU2lnbmFsPHRoaXMsIElJbnNwZWN0b3IuSUluc3BlY3RvclVwZGF0ZT4odGhpcyk7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfcGVuZGluZyA9IDA7XG4gIHByaXZhdGUgX3JlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnk7XG4gIHByaXZhdGUgX3N0YW5kYnkgPSB0cnVlO1xuICBwcml2YXRlIF9kZWJvdW5jZXI6IERlYm91bmNlcjtcbiAgcHJpdmF0ZSBfbGFzdEluc3BlY3RlZFJlcGx5OiBJbnNwZWN0aW9uSGFuZGxlci5JUmVwbHlbJ2RhdGEnXSB8IG51bGwgPSBudWxsO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBpbnNwZWN0aW9uIGhhbmRsZXIgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJbnNwZWN0aW9uSGFuZGxlciB7XG4gIC8qKlxuICAgKiBUaGUgaW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBhbiBpbnNwZWN0aW9uIGhhbmRsZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY29ubmVjdG9yIHVzZWQgdG8gbWFrZSBpbnNwZWN0aW9uIHJlcXVlc3RzLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoZSBvbmx5IG1ldGhvZCBvZiB0aGlzIGNvbm5lY3RvciB0aGF0IHdpbGwgZXZlciBiZSBjYWxsZWQgaXMgYGZldGNoYCwgc29cbiAgICAgKiBpdCBpcyBhY2NlcHRhYmxlIGZvciB0aGUgb3RoZXIgbWV0aG9kcyB0byBiZSBzaW1wbGUgZnVuY3Rpb25zIHRoYXQgcmV0dXJuXG4gICAgICogcmVqZWN0ZWQgcHJvbWlzZXMuXG4gICAgICovXG4gICAgY29ubmVjdG9yOiBJRGF0YUNvbm5lY3RvcjxJUmVwbHksIHZvaWQsIElSZXF1ZXN0PjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBtaW1lIHJlbmRlcmVyIGZvciB0aGUgaW5zcGVjdGlvbiBoYW5kbGVyLlxuICAgICAqL1xuICAgIHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnk7XG4gIH1cblxuICAvKipcbiAgICogQSByZXBseSB0byBhbiBpbnNwZWN0aW9uIHJlcXVlc3QuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElSZXBseSB7XG4gICAgLyoqXG4gICAgICogVGhlIE1JTUUgYnVuZGxlIGRhdGEgcmV0dXJuZWQgZnJvbSBhbiBpbnNwZWN0aW9uIHJlcXVlc3QuXG4gICAgICovXG4gICAgZGF0YTogUmVhZG9ubHlKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogQW55IG1ldGFkYXRhIHRoYXQgYWNjb21wYW5pZXMgdGhlIE1JTUUgYnVuZGxlIHJldHVybmluZyBmcm9tIGEgcmVxdWVzdC5cbiAgICAgKi9cbiAgICBtZXRhZGF0YTogUmVhZG9ubHlKU09OT2JqZWN0O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBkZXRhaWxzIG9mIGFuIGluc3BlY3Rpb24gcmVxdWVzdC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVJlcXVlc3Qge1xuICAgIC8qKlxuICAgICAqIFRoZSBjdXJzb3Igb2Zmc2V0IHBvc2l0aW9uIHdpdGhpbiB0aGUgdGV4dCBiZWluZyBpbnNwZWN0ZWQuXG4gICAgICovXG4gICAgb2Zmc2V0OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdGV4dCBiZWluZyBpbnNwZWN0ZWQuXG4gICAgICovXG4gICAgdGV4dDogc3RyaW5nO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBpbnNwZWN0b3JcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL2hhbmRsZXInO1xuZXhwb3J0ICogZnJvbSAnLi9pbnNwZWN0b3InO1xuZXhwb3J0ICogZnJvbSAnLi9rZXJuZWxjb25uZWN0b3InO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBQcmludGluZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgUGFuZWwsIFBhbmVsTGF5b3V0LCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgSUluc3BlY3RvciB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBpbnNwZWN0b3IgcGFuZWxzLlxuICovXG5jb25zdCBQQU5FTF9DTEFTUyA9ICdqcC1JbnNwZWN0b3InO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGluc3BlY3RvciBjb250ZW50LlxuICovXG5jb25zdCBDT05URU5UX0NMQVNTID0gJ2pwLUluc3BlY3Rvci1jb250ZW50JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBkZWZhdWx0IGluc3BlY3RvciBjb250ZW50LlxuICovXG5jb25zdCBERUZBVUxUX0NPTlRFTlRfQ0xBU1MgPSAnanAtSW5zcGVjdG9yLWRlZmF1bHQtY29udGVudCc7XG5cbi8qKlxuICogQSBwYW5lbCB3aGljaCBjb250YWlucyBhIHNldCBvZiBpbnNwZWN0b3JzLlxuICovXG5leHBvcnQgY2xhc3MgSW5zcGVjdG9yUGFuZWxcbiAgZXh0ZW5kcyBQYW5lbFxuICBpbXBsZW1lbnRzIElJbnNwZWN0b3IsIFByaW50aW5nLklQcmludGFibGUge1xuICAvKipcbiAgICogQ29uc3RydWN0IGFuIGluc3BlY3Rvci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IEluc3BlY3RvclBhbmVsLklPcHRpb25zID0ge30pIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IG9wdGlvbnMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl90cmFucyA9IHRoaXMudHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgICBpZiAob3B0aW9ucy5pbml0aWFsQ29udGVudCBpbnN0YW5jZW9mIFdpZGdldCkge1xuICAgICAgdGhpcy5fY29udGVudCA9IG9wdGlvbnMuaW5pdGlhbENvbnRlbnQ7XG4gICAgfSBlbHNlIGlmICh0eXBlb2Ygb3B0aW9ucy5pbml0aWFsQ29udGVudCA9PT0gJ3N0cmluZycpIHtcbiAgICAgIHRoaXMuX2NvbnRlbnQgPSBJbnNwZWN0b3JQYW5lbC5fZ2VuZXJhdGVDb250ZW50V2lkZ2V0KFxuICAgICAgICBgPHA+JHtvcHRpb25zLmluaXRpYWxDb250ZW50fTwvcD5gXG4gICAgICApO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9jb250ZW50ID0gSW5zcGVjdG9yUGFuZWwuX2dlbmVyYXRlQ29udGVudFdpZGdldChcbiAgICAgICAgJzxwPicgK1xuICAgICAgICAgIHRoaXMuX3RyYW5zLl9fKCdDbGljayBvbiBhIGZ1bmN0aW9uIHRvIHNlZSBkb2N1bWVudGF0aW9uLicpICtcbiAgICAgICAgICAnPC9wPidcbiAgICAgICk7XG4gICAgfVxuXG4gICAgdGhpcy5hZGRDbGFzcyhQQU5FTF9DTEFTUyk7XG4gICAgKHRoaXMubGF5b3V0IGFzIFBhbmVsTGF5b3V0KS5hZGRXaWRnZXQodGhpcy5fY29udGVudCk7XG4gIH1cblxuICAvKipcbiAgICogUHJpbnQgaW4gaWZyYW1lXG4gICAqL1xuICBbUHJpbnRpbmcuc3ltYm9sXSgpIHtcbiAgICByZXR1cm4gKCkgPT4gUHJpbnRpbmcucHJpbnRXaWRnZXQodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNvdXJjZSBvZiBldmVudHMgdGhlIGluc3BlY3RvciBwYW5lbCBsaXN0ZW5zIGZvci5cbiAgICovXG4gIGdldCBzb3VyY2UoKTogSUluc3BlY3Rvci5JSW5zcGVjdGFibGUgfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fc291cmNlO1xuICB9XG4gIHNldCBzb3VyY2Uoc291cmNlOiBJSW5zcGVjdG9yLklJbnNwZWN0YWJsZSB8IG51bGwpIHtcbiAgICBpZiAodGhpcy5fc291cmNlID09PSBzb3VyY2UpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBEaXNjb25uZWN0IG9sZCBzaWduYWwgaGFuZGxlci5cbiAgICBpZiAodGhpcy5fc291cmNlKSB7XG4gICAgICB0aGlzLl9zb3VyY2Uuc3RhbmRieSA9IHRydWU7XG4gICAgICB0aGlzLl9zb3VyY2UuaW5zcGVjdGVkLmRpc2Nvbm5lY3QodGhpcy5vbkluc3BlY3RvclVwZGF0ZSwgdGhpcyk7XG4gICAgICB0aGlzLl9zb3VyY2UuZGlzcG9zZWQuZGlzY29ubmVjdCh0aGlzLm9uU291cmNlRGlzcG9zZWQsIHRoaXMpO1xuICAgIH1cblxuICAgIC8vIFJlamVjdCBhIHNvdXJjZSB0aGF0IGlzIGFscmVhZHkgZGlzcG9zZWQuXG4gICAgaWYgKHNvdXJjZSAmJiBzb3VyY2UuaXNEaXNwb3NlZCkge1xuICAgICAgc291cmNlID0gbnVsbDtcbiAgICB9XG5cbiAgICAvLyBVcGRhdGUgc291cmNlLlxuICAgIHRoaXMuX3NvdXJjZSA9IHNvdXJjZTtcblxuICAgIC8vIENvbm5lY3QgbmV3IHNpZ25hbCBoYW5kbGVyLlxuICAgIGlmICh0aGlzLl9zb3VyY2UpIHtcbiAgICAgIHRoaXMuX3NvdXJjZS5zdGFuZGJ5ID0gZmFsc2U7XG4gICAgICB0aGlzLl9zb3VyY2UuaW5zcGVjdGVkLmNvbm5lY3QodGhpcy5vbkluc3BlY3RvclVwZGF0ZSwgdGhpcyk7XG4gICAgICB0aGlzLl9zb3VyY2UuZGlzcG9zZWQuY29ubmVjdCh0aGlzLm9uU291cmNlRGlzcG9zZWQsIHRoaXMpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuc291cmNlID0gbnVsbDtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGluc3BlY3RvciB1cGRhdGUgc2lnbmFscy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkluc3BlY3RvclVwZGF0ZShcbiAgICBzZW5kZXI6IGFueSxcbiAgICBhcmdzOiBJSW5zcGVjdG9yLklJbnNwZWN0b3JVcGRhdGVcbiAgKTogdm9pZCB7XG4gICAgY29uc3QgeyBjb250ZW50IH0gPSBhcmdzO1xuXG4gICAgLy8gVXBkYXRlIHRoZSBjb250ZW50IG9mIHRoZSBpbnNwZWN0b3Igd2lkZ2V0LlxuICAgIGlmICghY29udGVudCB8fCBjb250ZW50ID09PSB0aGlzLl9jb250ZW50KSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2NvbnRlbnQuZGlzcG9zZSgpO1xuXG4gICAgdGhpcy5fY29udGVudCA9IGNvbnRlbnQ7XG4gICAgY29udGVudC5hZGRDbGFzcyhDT05URU5UX0NMQVNTKTtcbiAgICAodGhpcy5sYXlvdXQgYXMgUGFuZWxMYXlvdXQpLmFkZFdpZGdldChjb250ZW50KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgc291cmNlIGRpc3Bvc2VkIHNpZ25hbHMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25Tb3VyY2VEaXNwb3NlZChzZW5kZXI6IGFueSwgYXJnczogdm9pZCk6IHZvaWQge1xuICAgIHRoaXMuc291cmNlID0gbnVsbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZW5lcmF0ZSBjb250ZW50IHdpZGdldCBmcm9tIHN0cmluZ1xuICAgKi9cbiAgcHJpdmF0ZSBzdGF0aWMgX2dlbmVyYXRlQ29udGVudFdpZGdldChtZXNzYWdlOiBzdHJpbmcpOiBXaWRnZXQge1xuICAgIGNvbnN0IHdpZGdldCA9IG5ldyBXaWRnZXQoKTtcbiAgICB3aWRnZXQubm9kZS5pbm5lckhUTUwgPSBtZXNzYWdlO1xuICAgIHdpZGdldC5hZGRDbGFzcyhDT05URU5UX0NMQVNTKTtcbiAgICB3aWRnZXQuYWRkQ2xhc3MoREVGQVVMVF9DT05URU5UX0NMQVNTKTtcblxuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfY29udGVudDogV2lkZ2V0O1xuICBwcml2YXRlIF9zb3VyY2U6IElJbnNwZWN0b3IuSUluc3BlY3RhYmxlIHwgbnVsbCA9IG51bGw7XG59XG5cbmV4cG9ydCBuYW1lc3BhY2UgSW5zcGVjdG9yUGFuZWwge1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICBpbml0aWFsQ29udGVudD86IFdpZGdldCB8IHN0cmluZyB8IHVuZGVmaW5lZDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBhcHBsaWNhdGlvbiBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJU2Vzc2lvbkNvbnRleHQgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBLZXJuZWxNZXNzYWdlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgRGF0YUNvbm5lY3RvciB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXRlZGInO1xuaW1wb3J0IHsgSW5zcGVjdGlvbkhhbmRsZXIgfSBmcm9tICcuL2hhbmRsZXInO1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGNvbm5lY3RvciBmb3IgbWFraW5nIGluc3BlY3Rpb24gcmVxdWVzdHMgZnJvbSB0aGUgSnVweXRlciBBUEkuXG4gKi9cbmV4cG9ydCBjbGFzcyBLZXJuZWxDb25uZWN0b3IgZXh0ZW5kcyBEYXRhQ29ubmVjdG9yPFxuICBJbnNwZWN0aW9uSGFuZGxlci5JUmVwbHksXG4gIHZvaWQsXG4gIEluc3BlY3Rpb25IYW5kbGVyLklSZXF1ZXN0XG4+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBrZXJuZWwgY29ubmVjdG9yIGZvciBpbnNwZWN0aW9uIHJlcXVlc3RzLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIHRoZSBrZXJuZWwgY29ubmVjdG9yLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogS2VybmVsQ29ubmVjdG9yLklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl9zZXNzaW9uQ29udGV4dCA9IG9wdGlvbnMuc2Vzc2lvbkNvbnRleHQ7XG4gIH1cblxuICAvKipcbiAgICogRmV0Y2ggaW5zcGVjdGlvbiByZXF1ZXN0cy5cbiAgICpcbiAgICogQHBhcmFtIHJlcXVlc3QgLSBUaGUgaW5zcGVjdGlvbiByZXF1ZXN0IHRleHQgYW5kIGRldGFpbHMuXG4gICAqL1xuICBmZXRjaChcbiAgICByZXF1ZXN0OiBJbnNwZWN0aW9uSGFuZGxlci5JUmVxdWVzdFxuICApOiBQcm9taXNlPEluc3BlY3Rpb25IYW5kbGVyLklSZXBseT4ge1xuICAgIGNvbnN0IGtlcm5lbCA9IHRoaXMuX3Nlc3Npb25Db250ZXh0LnNlc3Npb24/Lmtlcm5lbDtcblxuICAgIGlmICgha2VybmVsKSB7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZWplY3QobmV3IEVycm9yKCdJbnNwZWN0aW9uIGZldGNoIHJlcXVpcmVzIGEga2VybmVsLicpKTtcbiAgICB9XG5cbiAgICBjb25zdCBjb250ZW50czogS2VybmVsTWVzc2FnZS5JSW5zcGVjdFJlcXVlc3RNc2dbJ2NvbnRlbnQnXSA9IHtcbiAgICAgIGNvZGU6IHJlcXVlc3QudGV4dCxcbiAgICAgIGN1cnNvcl9wb3M6IHJlcXVlc3Qub2Zmc2V0LFxuICAgICAgZGV0YWlsX2xldmVsOiAxXG4gICAgfTtcblxuICAgIHJldHVybiBrZXJuZWwucmVxdWVzdEluc3BlY3QoY29udGVudHMpLnRoZW4obXNnID0+IHtcbiAgICAgIGNvbnN0IHJlc3BvbnNlID0gbXNnLmNvbnRlbnQ7XG5cbiAgICAgIGlmIChyZXNwb25zZS5zdGF0dXMgIT09ICdvaycgfHwgIXJlc3BvbnNlLmZvdW5kKSB7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcignSW5zcGVjdGlvbiBmZXRjaCBmYWlsZWQgdG8gcmV0dXJuIHN1Y2Nlc3NmdWxseS4nKTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHsgZGF0YTogcmVzcG9uc2UuZGF0YSwgbWV0YWRhdGE6IHJlc3BvbnNlLm1ldGFkYXRhIH07XG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9zZXNzaW9uQ29udGV4dDogSVNlc3Npb25Db250ZXh0O1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBrZXJuZWwgY29ubmVjdG9yIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgS2VybmVsQ29ubmVjdG9yIHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGFuIGluc3BlY3Rpb24gaGFuZGxlci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBzZXNzaW9uIGNvbnRleHQgdXNlZCB0byBtYWtlIEFQSSByZXF1ZXN0cyB0byB0aGUga2VybmVsLlxuICAgICAqL1xuICAgIHNlc3Npb25Db250ZXh0OiBJU2Vzc2lvbkNvbnRleHQ7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyogdHNsaW50OmRpc2FibGUgKi9cbi8qKlxuICogVGhlIGluc3BlY3RvciBwYW5lbCB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElJbnNwZWN0b3IgPSBuZXcgVG9rZW48SUluc3BlY3Rvcj4oXG4gICdAanVweXRlcmxhYi9pbnNwZWN0b3I6SUluc3BlY3Rvcidcbik7XG4vKiB0c2xpbnQ6ZW5hYmxlICovXG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBhbiBpbnNwZWN0b3IuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUluc3BlY3RvciB7XG4gIC8qKlxuICAgKiBUaGUgc291cmNlIG9mIGV2ZW50cyB0aGUgaW5zcGVjdG9yIGxpc3RlbnMgZm9yLlxuICAgKi9cbiAgc291cmNlOiBJSW5zcGVjdG9yLklJbnNwZWN0YWJsZSB8IG51bGw7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGluc3BlY3RvciBpbnRlcmZhY2VzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElJbnNwZWN0b3Ige1xuICAvKipcbiAgICogVGhlIGRlZmluaXRpb24gb2YgYW4gaW5zcGVjdGFibGUgc291cmNlLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJSW5zcGVjdGFibGUge1xuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgaW5zcGVjdG9yIHNob3VsZCBjbGVhciBhbGwgaXRlbXMuXG4gICAgICovXG4gICAgY2xlYXJlZDogSVNpZ25hbDxhbnksIHZvaWQ+O1xuXG4gICAgLyoqXG4gICAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBpbnNwZWN0YWJsZSBpcyBkaXNwb3NlZC5cbiAgICAgKi9cbiAgICBkaXNwb3NlZDogSVNpZ25hbDxhbnksIHZvaWQ+O1xuXG4gICAgLyoqXG4gICAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIGFuIGluc3BlY3RvciB2YWx1ZSBpcyBnZW5lcmF0ZWQuXG4gICAgICovXG4gICAgaW5zcGVjdGVkOiBJU2lnbmFsPGFueSwgSUluc3BlY3RvclVwZGF0ZT47XG5cbiAgICAvKipcbiAgICAgKiBUZXN0IHdoZXRoZXIgdGhlIGluc3BlY3RhYmxlIGhhcyBiZWVuIGRpc3Bvc2VkLlxuICAgICAqL1xuICAgIGlzRGlzcG9zZWQ6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBJbmRpY2F0ZXMgd2hldGhlciB0aGUgaW5zcGVjdGFibGUgc291cmNlIGVtaXRzIHNpZ25hbHMuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhlIHVzZSBjYXNlIGZvciB0aGlzIGF0dHJpYnV0ZSBpcyB0byBsaW1pdCB0aGUgQVBJIHRyYWZmaWMgd2hlbiBub1xuICAgICAqIGluc3BlY3RvciBpcyB2aXNpYmxlLiBJdCBjYW4gYmUgbW9kaWZpZWQgYnkgdGhlIGNvbnN1bWVyIG9mIHRoZSBzb3VyY2UuXG4gICAgICovXG4gICAgc3RhbmRieTogYm9vbGVhbjtcbiAgICAvKipcbiAgICAgKiBIYW5kbGUgYSB0ZXh0IGNoYW5nZWQgc2lnbmFsIGZyb20gYW4gZWRpdG9yLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFVwZGF0ZSB0aGUgaGludHMgaW5zcGVjdG9yIGJhc2VkIG9uIGEgdGV4dCBjaGFuZ2UuXG4gICAgICovXG4gICAgb25FZGl0b3JDaGFuZ2UoY3VzdG9tVGV4dD86IHN0cmluZyk6IHZvaWQ7XG4gIH1cblxuICAvKipcbiAgICogQW4gdXBkYXRlIHZhbHVlIGZvciBjb2RlIGluc3BlY3RvcnMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElJbnNwZWN0b3JVcGRhdGUge1xuICAgIC8qKlxuICAgICAqIFRoZSBjb250ZW50IGJlaW5nIHNlbnQgdG8gdGhlIGluc3BlY3RvciBmb3IgZGlzcGxheS5cbiAgICAgKi9cbiAgICBjb250ZW50OiBXaWRnZXQgfCBudWxsO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9