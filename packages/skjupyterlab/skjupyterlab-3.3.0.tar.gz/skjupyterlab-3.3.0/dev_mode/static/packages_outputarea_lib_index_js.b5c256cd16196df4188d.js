(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_outputarea_lib_index_js"],{

/***/ "../packages/outputarea/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/outputarea/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputAreaModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_0__.OutputAreaModel),
/* harmony export */   "OutputArea": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.OutputArea),
/* harmony export */   "OutputPrompt": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.OutputPrompt),
/* harmony export */   "SimplifiedOutputArea": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.SimplifiedOutputArea),
/* harmony export */   "Stdin": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.Stdin)
/* harmony export */ });
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./model */ "../packages/outputarea/lib/model.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/outputarea/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module outputarea
 */




/***/ }),

/***/ "../packages/outputarea/lib/model.js":
/*!*******************************************!*\
  !*** ../packages/outputarea/lib/model.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputAreaModel": () => (/* binding */ OutputAreaModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/nbformat */ "webpack/sharing/consume/default/@jupyterlab/nbformat/@jupyterlab/nbformat");
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The default implementation of the IOutputAreaModel.
 */
class OutputAreaModel {
    /**
     * Construct a new observable outputs instance.
     */
    constructor(options = {}) {
        /**
         * A flag that is set when we want to clear the output area
         * *after* the next addition to it.
         */
        this.clearNext = false;
        this._trusted = false;
        this._isDisposed = false;
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._trusted = !!options.trusted;
        this.contentFactory =
            options.contentFactory || OutputAreaModel.defaultContentFactory;
        this.list = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__.ObservableList();
        if (options.values) {
            (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(options.values, value => {
                this._add(value);
            });
        }
        this.list.changed.connect(this._onListChanged, this);
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
     * Get the length of the items in the model.
     */
    get length() {
        return this.list ? this.list.length : 0;
    }
    /**
     * Get whether the model is trusted.
     */
    get trusted() {
        return this._trusted;
    }
    /**
     * Set whether the model is trusted.
     *
     * #### Notes
     * Changing the value will cause all of the models to re-set.
     */
    set trusted(value) {
        if (value === this._trusted) {
            return;
        }
        const trusted = (this._trusted = value);
        for (let i = 0; i < this.list.length; i++) {
            let item = this.list.get(i);
            const value = item.toJSON();
            item.dispose();
            item = this._createItem({ value, trusted });
            this.list.set(i, item);
        }
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
        this.list.dispose();
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal.clearData(this);
    }
    /**
     * Get an item at the specified index.
     */
    get(index) {
        return this.list.get(index);
    }
    /**
     * Set the value at the specified index.
     */
    set(index, value) {
        value = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(value);
        // Normalize stream data.
        Private.normalize(value);
        const item = this._createItem({ value, trusted: this._trusted });
        this.list.set(index, item);
    }
    /**
     * Add an output, which may be combined with previous output.
     *
     * @returns The total number of outputs.
     *
     * #### Notes
     * The output bundle is copied.
     * Contiguous stream outputs of the same `name` are combined.
     */
    add(output) {
        // If we received a delayed clear message, then clear now.
        if (this.clearNext) {
            this.clear();
            this.clearNext = false;
        }
        return this._add(output);
    }
    /**
     * Clear all of the output.
     *
     * @param wait Delay clearing the output until the next message is added.
     */
    clear(wait = false) {
        this._lastStream = '';
        if (wait) {
            this.clearNext = true;
            return;
        }
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(this.list, (item) => {
            item.dispose();
        });
        this.list.clear();
    }
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * This will clear any existing data.
     */
    fromJSON(values) {
        this.clear();
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(values, value => {
            this._add(value);
        });
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.toArray)((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.map)(this.list, (output) => output.toJSON()));
    }
    /**
     * Add a copy of the item to the list.
     */
    _add(value) {
        const trusted = this._trusted;
        value = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(value);
        // Normalize the value.
        Private.normalize(value);
        // Consolidate outputs if they are stream outputs of the same kind.
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isStream(value) &&
            this._lastStream &&
            value.name === this._lastName &&
            this.shouldCombine({
                value,
                lastModel: this.list.get(this.length - 1)
            })) {
            // In order to get a list change event, we add the previous
            // text to the current item and replace the previous item.
            // This also replaces the metadata of the last item.
            this._lastStream += value.text;
            this._lastStream = Private.removeOverwrittenChars(this._lastStream);
            value.text = this._lastStream;
            const item = this._createItem({ value, trusted });
            const index = this.length - 1;
            const prev = this.list.get(index);
            prev.dispose();
            this.list.set(index, item);
            return index;
        }
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isStream(value)) {
            value.text = Private.removeOverwrittenChars(value.text);
        }
        // Create the new item.
        const item = this._createItem({ value, trusted });
        // Update the stream information.
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isStream(value)) {
            this._lastStream = value.text;
            this._lastName = value.name;
        }
        else {
            this._lastStream = '';
        }
        // Add the item to our list and return the new length.
        return this.list.push(item);
    }
    /**
     * Whether a new value should be consolidated with the previous output.
     *
     * This will only be called if the minimal criteria of both being stream
     * messages of the same type.
     */
    shouldCombine(options) {
        return true;
    }
    /**
     * Create an output item and hook up its signals.
     */
    _createItem(options) {
        const factory = this.contentFactory;
        const item = factory.createOutputModel(options);
        item.changed.connect(this._onGenericChange, this);
        return item;
    }
    /**
     * Handle a change to the list.
     */
    _onListChanged(sender, args) {
        this._changed.emit(args);
    }
    /**
     * Handle a change to an item.
     */
    _onGenericChange() {
        this._stateChanged.emit(void 0);
    }
}
/**
 * The namespace for OutputAreaModel class statics.
 */
(function (OutputAreaModel) {
    /**
     * The default implementation of a `IModelOutputFactory`.
     */
    class ContentFactory {
        /**
         * Create an output model.
         */
        createOutputModel(options) {
            return new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.OutputModel(options);
        }
    }
    OutputAreaModel.ContentFactory = ContentFactory;
    /**
     * The default output model factory.
     */
    OutputAreaModel.defaultContentFactory = new ContentFactory();
})(OutputAreaModel || (OutputAreaModel = {}));
/**
 * A namespace for module-private functionality.
 */
var Private;
(function (Private) {
    /**
     * Normalize an output.
     */
    function normalize(value) {
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isStream(value)) {
            if (Array.isArray(value.text)) {
                value.text = value.text.join('\n');
            }
        }
    }
    Private.normalize = normalize;
    /**
     * Remove characters that are overridden by backspace characters.
     */
    function fixBackspace(txt) {
        let tmp = txt;
        do {
            txt = tmp;
            // Cancel out anything-but-newline followed by backspace
            tmp = txt.replace(/[^\n]\x08/gm, ''); // eslint-disable-line no-control-regex
        } while (tmp.length < txt.length);
        return txt;
    }
    /**
     * Remove chunks that should be overridden by the effect of
     * carriage return characters.
     */
    function fixCarriageReturn(txt) {
        txt = txt.replace(/\r+\n/gm, '\n'); // \r followed by \n --> newline
        while (txt.search(/\r[^$]/g) > -1) {
            const base = txt.match(/^(.*)\r+/m)[1];
            let insert = txt.match(/\r+(.*)$/m)[1];
            insert = insert + base.slice(insert.length, base.length);
            txt = txt.replace(/\r+.*$/m, '\r').replace(/^.*\r/m, insert);
        }
        return txt;
    }
    /*
     * Remove characters overridden by backspaces and carriage returns
     */
    function removeOverwrittenChars(text) {
        return fixCarriageReturn(fixBackspace(text));
    }
    Private.removeOverwrittenChars = removeOverwrittenChars;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/outputarea/lib/widget.js":
/*!********************************************!*\
  !*** ../packages/outputarea/lib/widget.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputArea": () => (/* binding */ OutputArea),
/* harmony export */   "SimplifiedOutputArea": () => (/* binding */ SimplifiedOutputArea),
/* harmony export */   "OutputPrompt": () => (/* binding */ OutputPrompt),
/* harmony export */   "Stdin": () => (/* binding */ Stdin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var resize_observer_polyfill__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! resize-observer-polyfill */ "../node_modules/resize-observer-polyfill/dist/ResizeObserver.es.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * The class name added to an output area widget.
 */
const OUTPUT_AREA_CLASS = 'jp-OutputArea';
/**
 * The class name added to the direction children of OutputArea
 */
const OUTPUT_AREA_ITEM_CLASS = 'jp-OutputArea-child';
/**
 * The class name added to actual outputs
 */
const OUTPUT_AREA_OUTPUT_CLASS = 'jp-OutputArea-output';
/**
 * The class name added to prompt children of OutputArea.
 */
const OUTPUT_AREA_PROMPT_CLASS = 'jp-OutputArea-prompt';
/**
 * The class name added to OutputPrompt.
 */
const OUTPUT_PROMPT_CLASS = 'jp-OutputPrompt';
/**
 * The class name added to an execution result.
 */
const EXECUTE_CLASS = 'jp-OutputArea-executeResult';
/**
 * The class name added stdin items of OutputArea
 */
const OUTPUT_AREA_STDIN_ITEM_CLASS = 'jp-OutputArea-stdin-item';
/**
 * The class name added to stdin widgets.
 */
const STDIN_CLASS = 'jp-Stdin';
/**
 * The class name added to stdin data prompt nodes.
 */
const STDIN_PROMPT_CLASS = 'jp-Stdin-prompt';
/**
 * The class name added to stdin data input nodes.
 */
const STDIN_INPUT_CLASS = 'jp-Stdin-input';
/** ****************************************************************************
 * OutputArea
 ******************************************************************************/
/**
 * An output area widget.
 *
 * #### Notes
 * The widget model must be set separately and can be changed
 * at any time.  Consumers of the widget must account for a
 * `null` model, and may want to listen to the `modelChanged`
 * signal.
 */
class OutputArea extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget {
    /**
     * Construct an output area widget.
     */
    constructor(options) {
        super();
        /**
         * A public signal used to indicate the number of outputs has changed.
         *
         * #### Notes
         * This is useful for parents who want to apply styling based on the number
         * of outputs. Emits the current number of outputs.
         */
        this.outputLengthChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        /**
         * Handle an iopub message.
         */
        this._onIOPub = (msg) => {
            const model = this.model;
            const msgType = msg.header.msg_type;
            let output;
            const transient = (msg.content.transient || {});
            const displayId = transient['display_id'];
            let targets;
            switch (msgType) {
                case 'execute_result':
                case 'display_data':
                case 'stream':
                case 'error':
                    output = Object.assign(Object.assign({}, msg.content), { output_type: msgType });
                    model.add(output);
                    break;
                case 'clear_output': {
                    const wait = msg.content.wait;
                    model.clear(wait);
                    break;
                }
                case 'update_display_data':
                    output = Object.assign(Object.assign({}, msg.content), { output_type: 'display_data' });
                    targets = this._displayIdMap.get(displayId);
                    if (targets) {
                        for (const index of targets) {
                            model.set(index, output);
                        }
                    }
                    break;
                default:
                    break;
            }
            if (displayId && msgType === 'display_data') {
                targets = this._displayIdMap.get(displayId) || [];
                targets.push(model.length - 1);
                this._displayIdMap.set(displayId, targets);
            }
        };
        /**
         * Handle an execute reply message.
         */
        this._onExecuteReply = (msg) => {
            // API responses that contain a pager are special cased and their type
            // is overridden from 'execute_reply' to 'display_data' in order to
            // render output.
            const model = this.model;
            const content = msg.content;
            if (content.status !== 'ok') {
                return;
            }
            const payload = content && content.payload;
            if (!payload || !payload.length) {
                return;
            }
            const pages = payload.filter((i) => i.source === 'page');
            if (!pages.length) {
                return;
            }
            const page = JSON.parse(JSON.stringify(pages[0]));
            const output = {
                output_type: 'display_data',
                data: page.data,
                metadata: {}
            };
            model.add(output);
        };
        this._minHeightTimeout = null;
        this._displayIdMap = new Map();
        this._outputTracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker({
            namespace: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.UUID.uuid4()
        });
        const model = (this.model = options.model);
        this.addClass(OUTPUT_AREA_CLASS);
        this.rendermime = options.rendermime;
        this.contentFactory =
            options.contentFactory || OutputArea.defaultContentFactory;
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.PanelLayout();
        this.trimmedOutputModels = new Array();
        this.maxNumberOutputs = options.maxNumberOutputs || 0;
        this.headEndIndex = this.maxNumberOutputs;
        for (let i = 0; i < model.length; i++) {
            const output = model.get(i);
            this._insertOutput(i, output);
        }
        model.changed.connect(this.onModelChanged, this);
        model.stateChanged.connect(this.onStateChanged, this);
    }
    /**
     * A read-only sequence of the children widgets in the output area.
     */
    get widgets() {
        return this.layout.widgets;
    }
    /**
     * The kernel future associated with the output area.
     */
    get future() {
        return this._future;
    }
    set future(value) {
        // Bail if the model is disposed.
        if (this.model.isDisposed) {
            throw Error('Model is disposed');
        }
        if (this._future === value) {
            return;
        }
        if (this._future) {
            this._future.dispose();
        }
        this._future = value;
        this.model.clear();
        // Make sure there were no input widgets.
        if (this.widgets.length) {
            this._clear();
            this.outputLengthChanged.emit(this.model.length);
        }
        // Handle published messages.
        value.onIOPub = this._onIOPub;
        // Handle the execute reply.
        value.onReply = this._onExecuteReply;
        // Handle stdin.
        value.onStdin = msg => {
            if (_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.KernelMessage.isInputRequestMsg(msg)) {
                this.onInputRequest(msg, value);
            }
        };
    }
    /**
     * Dispose of the resources used by the output area.
     */
    dispose() {
        if (this._future) {
            this._future.dispose();
            this._future = null;
        }
        this._displayIdMap.clear();
        this._outputTracker.dispose();
        super.dispose();
    }
    /**
     * Follow changes on the model state.
     */
    onModelChanged(sender, args) {
        switch (args.type) {
            case 'add':
                this._insertOutput(args.newIndex, args.newValues[0]);
                this.outputLengthChanged.emit(this.model.length);
                break;
            case 'remove':
                if (this.widgets.length) {
                    // all items removed from model
                    if (this.model.length === 0) {
                        this._clear();
                    }
                    else {
                        // range of items removed from model
                        // remove widgets corresponding to removed model items
                        const startIndex = args.oldIndex;
                        for (let i = 0; i < args.oldValues.length && startIndex < this.widgets.length; ++i) {
                            const widget = this.widgets[startIndex];
                            widget.parent = null;
                            widget.dispose();
                        }
                        // apply item offset to target model item indices in _displayIdMap
                        this._moveDisplayIdIndices(startIndex, args.oldValues.length);
                        // prevent jitter caused by immediate height change
                        this._preventHeightChangeJitter();
                    }
                    this.outputLengthChanged.emit(this.model.length);
                }
                break;
            case 'set':
                this._setOutput(args.newIndex, args.newValues[0]);
                this.outputLengthChanged.emit(this.model.length);
                break;
            default:
                break;
        }
    }
    /**
     * Update indices in _displayIdMap in response to element remove from model items
     * *
     * @param startIndex - The index of first element removed
     *
     * @param count - The number of elements removed from model items
     *
     */
    _moveDisplayIdIndices(startIndex, count) {
        this._displayIdMap.forEach((indices) => {
            const rangeEnd = startIndex + count;
            const numIndices = indices.length;
            // reverse loop in order to prevent removing element affecting the index
            for (let i = numIndices - 1; i >= 0; --i) {
                const index = indices[i];
                // remove model item indices in removed range
                if (index >= startIndex && index < rangeEnd) {
                    indices.splice(i, 1);
                }
                else if (index >= rangeEnd) {
                    // move model item indices that were larger than range end
                    indices[i] -= count;
                }
            }
        });
    }
    /**
     * Follow changes on the output model state.
     */
    onStateChanged(sender) {
        this.trimmedOutputModels = new Array();
        for (let i = 0; i < this.model.length; i++) {
            this._setOutput(i, this.model.get(i));
        }
        this.outputLengthChanged.emit(this.model.length);
    }
    /**
     * Clear the widget inputs and outputs.
     */
    _clear() {
        // Bail if there is no work to do.
        if (!this.widgets.length) {
            return;
        }
        // Remove all of our widgets.
        const length = this.widgets.length;
        for (let i = 0; i < length; i++) {
            const widget = this.widgets[0];
            widget.parent = null;
            widget.dispose();
        }
        // Clear the display id map.
        this._displayIdMap.clear();
        // prevent jitter caused by immediate height change
        this._preventHeightChangeJitter();
    }
    _preventHeightChangeJitter() {
        // When an output area is cleared and then quickly replaced with new
        // content (as happens with @interact in widgets, for example), the
        // quickly changing height can make the page jitter.
        // We introduce a small delay in the minimum height
        // to prevent this jitter.
        const rect = this.node.getBoundingClientRect();
        this.node.style.minHeight = `${rect.height}px`;
        if (this._minHeightTimeout) {
            window.clearTimeout(this._minHeightTimeout);
        }
        this._minHeightTimeout = window.setTimeout(() => {
            if (this.isDisposed) {
                return;
            }
            this.node.style.minHeight = '';
        }, 50);
    }
    /**
     * Handle an input request from a kernel.
     */
    onInputRequest(msg, future) {
        // Add an output widget to the end.
        const factory = this.contentFactory;
        const stdinPrompt = msg.content.prompt;
        const password = msg.content.password;
        const panel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Panel();
        panel.addClass(OUTPUT_AREA_ITEM_CLASS);
        panel.addClass(OUTPUT_AREA_STDIN_ITEM_CLASS);
        const prompt = factory.createOutputPrompt();
        prompt.addClass(OUTPUT_AREA_PROMPT_CLASS);
        panel.addWidget(prompt);
        const input = factory.createStdin({
            prompt: stdinPrompt,
            password,
            future
        });
        input.addClass(OUTPUT_AREA_OUTPUT_CLASS);
        panel.addWidget(input);
        const layout = this.layout;
        layout.addWidget(panel);
        /**
         * Wait for the stdin to complete, add it to the model (so it persists)
         * and remove the stdin widget.
         */
        void input.value.then(value => {
            // Use stdin as the stream so it does not get combined with stdout.
            this.model.add({
                output_type: 'stream',
                name: 'stdin',
                text: value + '\n'
            });
            panel.dispose();
        });
    }
    /**
     * Update an output in the layout in place.
     */
    _setOutput(index, model) {
        if (index >= this.headEndIndex && this.maxNumberOutputs !== 0) {
            this.trimmedOutputModels[index - this.headEndIndex] = model;
            return;
        }
        const layout = this.layout;
        const panel = layout.widgets[index];
        const renderer = (panel.widgets
            ? panel.widgets[1]
            : panel);
        // Check whether it is safe to reuse renderer:
        // - Preferred mime type has not changed
        // - Isolation has not changed
        const mimeType = this.rendermime.preferredMimeType(model.data, model.trusted ? 'any' : 'ensure');
        if (renderer.renderModel &&
            Private.currentPreferredMimetype.get(renderer) === mimeType &&
            OutputArea.isIsolated(mimeType, model.metadata) ===
                renderer instanceof Private.IsolatedRenderer) {
            void renderer.renderModel(model);
        }
        else {
            layout.widgets[index].dispose();
            this._insertOutput(index, model);
        }
    }
    /**
     * Render and insert a single output into the layout.
     *
     * @param index - The index of the output to be inserted.
     * @param model - The model of the output to be inserted.
     */
    _insertOutput(index, model) {
        if (index === 0) {
            this.trimmedOutputModels = new Array();
        }
        if (index === this.maxNumberOutputs && this.maxNumberOutputs !== 0) {
            // TODO Improve style of the display message.
            const separatorModel = this.model.contentFactory.createOutputModel({
                value: {
                    output_type: 'display_data',
                    data: {
                        'text/html': `
              <a style="margin: 10px; text-decoration: none; cursor: pointer;">
                <pre>Output of this cell has been trimmed on the initial display.</pre>
                <pre>Displaying the first ${this.maxNumberOutputs} top outputs.</pre>
                <pre>Click on this message to get the complete output.</pre>
              </a>
              `
                    }
                }
            });
            const onClick = () => this._showTrimmedOutputs();
            const separator = this.createOutputItem(separatorModel);
            separator.node.addEventListener('click', onClick);
            const layout = this.layout;
            layout.insertWidget(this.headEndIndex, separator);
        }
        const output = this._createOutput(model);
        const layout = this.layout;
        if (index < this.maxNumberOutputs || this.maxNumberOutputs === 0) {
            layout.insertWidget(index, output);
        }
        if (index >= this.maxNumberOutputs && this.maxNumberOutputs !== 0) {
            this.trimmedOutputModels.push(model);
        }
        if (!this._outputTracker.has(output)) {
            void this._outputTracker.add(output);
        }
    }
    _createOutput(model) {
        let output = this.createOutputItem(model);
        if (output) {
            output.toggleClass(EXECUTE_CLASS, model.executionCount !== null);
        }
        else {
            output = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget();
        }
        return output;
    }
    /**
     * A widget tracker for individual output widgets in the output area.
     */
    get outputTracker() {
        return this._outputTracker;
    }
    /**
     * Remove the information message related to the trimmed output
     * and show all previously trimmed outputs.
     */
    _showTrimmedOutputs() {
        const layout = this.layout;
        layout.removeWidgetAt(this.headEndIndex);
        for (let i = 0; i < this.trimmedOutputModels.length; i++) {
            const output = this._createOutput(this.trimmedOutputModels[i]);
            layout.insertWidget(this.headEndIndex + i, output);
        }
    }
    /**
     * Create an output item with a prompt and actual output
     *
     * @returns a rendered widget, or null if we cannot render
     * #### Notes
     */
    createOutputItem(model) {
        const output = this.createRenderedMimetype(model);
        if (!output) {
            return null;
        }
        const panel = new Private.OutputPanel();
        panel.addClass(OUTPUT_AREA_ITEM_CLASS);
        const prompt = this.contentFactory.createOutputPrompt();
        prompt.executionCount = model.executionCount;
        prompt.addClass(OUTPUT_AREA_PROMPT_CLASS);
        panel.addWidget(prompt);
        output.addClass(OUTPUT_AREA_OUTPUT_CLASS);
        panel.addWidget(output);
        return panel;
    }
    /**
     * Render a mimetype
     */
    createRenderedMimetype(model) {
        const mimeType = this.rendermime.preferredMimeType(model.data, model.trusted ? 'any' : 'ensure');
        if (!mimeType) {
            return null;
        }
        let output = this.rendermime.createRenderer(mimeType);
        const isolated = OutputArea.isIsolated(mimeType, model.metadata);
        if (isolated === true) {
            output = new Private.IsolatedRenderer(output);
        }
        Private.currentPreferredMimetype.set(output, mimeType);
        output.renderModel(model).catch(error => {
            // Manually append error message to output
            const pre = document.createElement('pre');
            pre.textContent = `Javascript Error: ${error.message}`;
            output.node.appendChild(pre);
            // Remove mime-type-specific CSS classes
            output.node.className = 'lm-Widget jp-RenderedText';
            output.node.setAttribute('data-mime-type', 'application/vnd.jupyter.stderr');
        });
        return output;
    }
}
class SimplifiedOutputArea extends OutputArea {
    /**
     * Handle an input request from a kernel by doing nothing.
     */
    onInputRequest(msg, future) {
        return;
    }
    /**
     * Create an output item without a prompt, just the output widgets
     */
    createOutputItem(model) {
        const output = this.createRenderedMimetype(model);
        if (output) {
            output.addClass(OUTPUT_AREA_OUTPUT_CLASS);
        }
        return output;
    }
}
/**
 * A namespace for OutputArea statics.
 */
(function (OutputArea) {
    /**
     * Execute code on an output area.
     */
    async function execute(code, output, sessionContext, metadata) {
        var _a;
        // Override the default for `stop_on_error`.
        let stopOnError = true;
        if (metadata &&
            Array.isArray(metadata.tags) &&
            metadata.tags.indexOf('raises-exception') !== -1) {
            stopOnError = false;
        }
        const content = {
            code,
            stop_on_error: stopOnError
        };
        const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            throw new Error('Session has no kernel.');
        }
        const future = kernel.requestExecute(content, false, metadata);
        output.future = future;
        return future.done;
    }
    OutputArea.execute = execute;
    function isIsolated(mimeType, metadata) {
        const mimeMd = metadata[mimeType];
        // mime-specific higher priority
        if (mimeMd && mimeMd['isolated'] !== undefined) {
            return !!mimeMd['isolated'];
        }
        else {
            // fallback on global
            return !!metadata['isolated'];
        }
    }
    OutputArea.isIsolated = isIsolated;
    /**
     * The default implementation of `IContentFactory`.
     */
    class ContentFactory {
        /**
         * Create the output prompt for the widget.
         */
        createOutputPrompt() {
            return new OutputPrompt();
        }
        /**
         * Create an stdin widget.
         */
        createStdin(options) {
            return new Stdin(options);
        }
    }
    OutputArea.ContentFactory = ContentFactory;
    /**
     * The default `ContentFactory` instance.
     */
    OutputArea.defaultContentFactory = new ContentFactory();
})(OutputArea || (OutputArea = {}));
/**
 * The default output prompt implementation
 */
class OutputPrompt extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget {
    /*
     * Create an output prompt widget.
     */
    constructor() {
        super();
        this._executionCount = null;
        this.addClass(OUTPUT_PROMPT_CLASS);
    }
    /**
     * The execution count for the prompt.
     */
    get executionCount() {
        return this._executionCount;
    }
    set executionCount(value) {
        this._executionCount = value;
        if (value === null) {
            this.node.textContent = '';
        }
        else {
            this.node.textContent = `[${value}]:`;
        }
    }
}
/**
 * The default stdin widget.
 */
class Stdin extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget {
    /**
     * Construct a new input widget.
     */
    constructor(options) {
        super({
            node: Private.createInputWidgetNode(options.prompt, options.password)
        });
        this._promise = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
        this.addClass(STDIN_CLASS);
        this._input = this.node.getElementsByTagName('input')[0];
        this._input.focus();
        this._future = options.future;
        this._value = options.prompt + ' ';
    }
    /**
     * The value of the widget.
     */
    get value() {
        return this._promise.promise.then(() => this._value);
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        const input = this._input;
        if (event.type === 'keydown') {
            if (event.keyCode === 13) {
                // Enter
                this._future.sendInputReply({
                    status: 'ok',
                    value: input.value
                });
                if (input.type === 'password') {
                    this._value += Array(input.value.length + 1).join('·');
                }
                else {
                    this._value += input.value;
                }
                this._promise.resolve(void 0);
            }
        }
    }
    /**
     * Handle `after-attach` messages sent to the widget.
     */
    onAfterAttach(msg) {
        this._input.addEventListener('keydown', this);
        this.update();
    }
    /**
     * Handle `update-request` messages sent to the widget.
     */
    onUpdateRequest(msg) {
        this._input.focus();
    }
    /**
     * Handle `before-detach` messages sent to the widget.
     */
    onBeforeDetach(msg) {
        this._input.removeEventListener('keydown', this);
    }
}
/** ****************************************************************************
 * Private namespace
 ******************************************************************************/
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Create the node for an InputWidget.
     */
    function createInputWidgetNode(prompt, password) {
        const node = document.createElement('div');
        const promptNode = document.createElement('pre');
        promptNode.className = STDIN_PROMPT_CLASS;
        promptNode.textContent = prompt;
        const input = document.createElement('input');
        input.className = STDIN_INPUT_CLASS;
        if (password) {
            input.type = 'password';
        }
        node.appendChild(promptNode);
        promptNode.appendChild(input);
        return node;
    }
    Private.createInputWidgetNode = createInputWidgetNode;
    /**
     * A renderer for IFrame data.
     */
    class IsolatedRenderer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget {
        /**
         * Create an isolated renderer.
         */
        constructor(wrapped) {
            super({ node: document.createElement('iframe') });
            this.addClass('jp-mod-isolated');
            this._wrapped = wrapped;
            // Once the iframe is loaded, the subarea is dynamically inserted
            const iframe = this.node;
            iframe.frameBorder = '0';
            iframe.scrolling = 'auto';
            iframe.addEventListener('load', () => {
                // Workaround needed by Firefox, to properly render svg inside
                // iframes, see https://stackoverflow.com/questions/10177190/
                // svg-dynamically-added-to-iframe-does-not-render-correctly
                iframe.contentDocument.open();
                // Insert the subarea into the iframe
                // We must directly write the html. At this point, subarea doesn't
                // contain any user content.
                iframe.contentDocument.write(this._wrapped.node.innerHTML);
                iframe.contentDocument.close();
                const body = iframe.contentDocument.body;
                // Adjust the iframe height automatically
                iframe.style.height = `${body.scrollHeight}px`;
                iframe.heightChangeObserver = new resize_observer_polyfill__WEBPACK_IMPORTED_MODULE_6__.default(() => {
                    iframe.style.height = `${body.scrollHeight}px`;
                });
                iframe.heightChangeObserver.observe(body);
            });
        }
        /**
         * Render a mime model.
         *
         * @param model - The mime model to render.
         *
         * @returns A promise which resolves when rendering is complete.
         *
         * #### Notes
         * This method may be called multiple times during the lifetime
         * of the widget to update it if and when new data is available.
         */
        renderModel(model) {
            return this._wrapped.renderModel(model);
        }
    }
    Private.IsolatedRenderer = IsolatedRenderer;
    Private.currentPreferredMimetype = new _lumino_properties__WEBPACK_IMPORTED_MODULE_3__.AttachedProperty({
        name: 'preferredMimetype',
        create: owner => ''
    });
    /**
     * A `Panel` that's focused by a `contextmenu` event.
     */
    class OutputPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Panel {
        /**
         * Construct a new `OutputPanel` widget.
         */
        constructor(options) {
            super(options);
        }
        /**
         * A callback that focuses on the widget.
         */
        _onContext(_) {
            this.node.focus();
        }
        /**
         * Handle `after-attach` messages sent to the widget.
         */
        onAfterAttach(msg) {
            super.onAfterAttach(msg);
            this.node.addEventListener('contextmenu', this._onContext.bind(this));
        }
        /**
         * Handle `before-detach` messages sent to the widget.
         */
        onBeforeDetach(msg) {
            super.onAfterDetach(msg);
            this.node.removeEventListener('contextmenu', this._onContext.bind(this));
        }
    }
    Private.OutputPanel = OutputPanel;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvb3V0cHV0YXJlYS9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL291dHB1dGFyZWEvc3JjL21vZGVsLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9vdXRwdXRhcmVhL3NyYy93aWRnZXQudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBRXFCO0FBQ0M7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNSekIsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUVWO0FBQ3lCO0FBQ1A7QUFDWjtBQUNYO0FBRVE7QUF3SHBEOztHQUVHO0FBQ0ksTUFBTSxlQUFlO0lBQzFCOztPQUVHO0lBQ0gsWUFBWSxVQUFxQyxFQUFFO1FBaU9uRDs7O1dBR0c7UUFDTyxjQUFTLEdBQUcsS0FBSyxDQUFDO1FBcUNwQixhQUFRLEdBQUcsS0FBSyxDQUFDO1FBQ2pCLGdCQUFXLEdBQUcsS0FBSyxDQUFDO1FBQ3BCLGtCQUFhLEdBQUcsSUFBSSxxREFBTSxDQUF5QixJQUFJLENBQUMsQ0FBQztRQUN6RCxhQUFRLEdBQUcsSUFBSSxxREFBTSxDQUFxQyxJQUFJLENBQUMsQ0FBQztRQTVRdEUsSUFBSSxDQUFDLFFBQVEsR0FBRyxDQUFDLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQztRQUNsQyxJQUFJLENBQUMsY0FBYztZQUNqQixPQUFPLENBQUMsY0FBYyxJQUFJLGVBQWUsQ0FBQyxxQkFBcUIsQ0FBQztRQUNsRSxJQUFJLENBQUMsSUFBSSxHQUFHLElBQUksbUVBQWMsRUFBZ0IsQ0FBQztRQUMvQyxJQUFJLE9BQU8sQ0FBQyxNQUFNLEVBQUU7WUFDbEIsdURBQUksQ0FB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QWpJUyxPQUFPLEtBQVAsT0FBTyxRQWlJaEIiLCJmaWxlIjoicGFja2FnZXNfb3V0cHV0YXJlYV9saWJfaW5kZXhfanMuYjVjMjU2Y2QxNjE5NmRmNDE4OGQuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBvdXRwdXRhcmVhXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9tb2RlbCc7XG5leHBvcnQgKiBmcm9tICcuL3dpZGdldCc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIG5iZm9ybWF0IGZyb20gJ0BqdXB5dGVybGFiL25iZm9ybWF0JztcbmltcG9ydCB7IElPYnNlcnZhYmxlTGlzdCwgT2JzZXJ2YWJsZUxpc3QgfSBmcm9tICdAanVweXRlcmxhYi9vYnNlcnZhYmxlcyc7XG5pbXBvcnQgeyBJT3V0cHV0TW9kZWwsIE91dHB1dE1vZGVsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBlYWNoLCBtYXAsIHRvQXJyYXkgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBKU09ORXh0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuXG4vKipcbiAqIFRoZSBtb2RlbCBmb3IgYW4gb3V0cHV0IGFyZWEuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU91dHB1dEFyZWFNb2RlbCBleHRlbmRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbW9kZWwgc3RhdGUgY2hhbmdlcy5cbiAgICovXG4gIHJlYWRvbmx5IHN0YXRlQ2hhbmdlZDogSVNpZ25hbDxJT3V0cHV0QXJlYU1vZGVsLCB2b2lkPjtcblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBtb2RlbCBjaGFuZ2VzLlxuICAgKi9cbiAgcmVhZG9ubHkgY2hhbmdlZDogSVNpZ25hbDxJT3V0cHV0QXJlYU1vZGVsLCBJT3V0cHV0QXJlYU1vZGVsLkNoYW5nZWRBcmdzPjtcblxuICAvKipcbiAgICogVGhlIGxlbmd0aCBvZiB0aGUgaXRlbXMgaW4gdGhlIG1vZGVsLlxuICAgKi9cbiAgcmVhZG9ubHkgbGVuZ3RoOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG91dHB1dCBhcmVhIGlzIHRydXN0ZWQuXG4gICAqL1xuICB0cnVzdGVkOiBib29sZWFuO1xuXG4gIC8qKlxuICAgKiBUaGUgb3V0cHV0IGNvbnRlbnQgZmFjdG9yeSB1c2VkIGJ5IHRoZSBtb2RlbC5cbiAgICovXG4gIHJlYWRvbmx5IGNvbnRlbnRGYWN0b3J5OiBJT3V0cHV0QXJlYU1vZGVsLklDb250ZW50RmFjdG9yeTtcblxuICAvKipcbiAgICogR2V0IGFuIGl0ZW0gYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICovXG4gIGdldChpbmRleDogbnVtYmVyKTogSU91dHB1dE1vZGVsO1xuXG4gIC8qKlxuICAgKiBBZGQgYW4gb3V0cHV0LCB3aGljaCBtYXkgYmUgY29tYmluZWQgd2l0aCBwcmV2aW91cyBvdXRwdXQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSB0b3RhbCBudW1iZXIgb2Ygb3V0cHV0cy5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgb3V0cHV0IGJ1bmRsZSBpcyBjb3BpZWQuXG4gICAqIENvbnRpZ3VvdXMgc3RyZWFtIG91dHB1dHMgb2YgdGhlIHNhbWUgYG5hbWVgIGFyZSBjb21iaW5lZC5cbiAgICovXG4gIGFkZChvdXRwdXQ6IG5iZm9ybWF0LklPdXRwdXQpOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgdmFsdWUgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICovXG4gIHNldChpbmRleDogbnVtYmVyLCBvdXRwdXQ6IG5iZm9ybWF0LklPdXRwdXQpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBDbGVhciBhbGwgb2YgdGhlIG91dHB1dC5cbiAgICpcbiAgICogQHBhcmFtIHdhaXQgLSBEZWxheSBjbGVhcmluZyB0aGUgb3V0cHV0IHVudGlsIHRoZSBuZXh0IG1lc3NhZ2UgaXMgYWRkZWQuXG4gICAqL1xuICBjbGVhcih3YWl0PzogYm9vbGVhbik6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIERlc2VyaWFsaXplIHRoZSBtb2RlbCBmcm9tIEpTT04uXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyB3aWxsIGNsZWFyIGFueSBleGlzdGluZyBkYXRhLlxuICAgKi9cbiAgZnJvbUpTT04odmFsdWVzOiBuYmZvcm1hdC5JT3V0cHV0W10pOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBTZXJpYWxpemUgdGhlIG1vZGVsIHRvIEpTT04uXG4gICAqL1xuICB0b0pTT04oKTogbmJmb3JtYXQuSU91dHB1dFtdO1xuXG4gIC8qKlxuICAgKiBUaGUgbWF4aW11bSBudW1iZXIgb2Ygb3V0cHV0IGl0ZW1zIHRvIGRpc3BsYXkgb24gdG9wIGFuZCBib3R0b20gb2YgY2VsbCBvdXRwdXQuXG4gICAqL1xuICBtYXhOdW1iZXJPdXRwdXRzPzogbnVtYmVyO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIElPdXRwdXRBcmVhTW9kZWwgaW50ZXJmYWNlcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJT3V0cHV0QXJlYU1vZGVsIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGEgb3V0cHV0IGFyZWEgbW9kZWwuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgaW5pdGlhbCB2YWx1ZXMgZm9yIHRoZSBtb2RlbC5cbiAgICAgKi9cbiAgICB2YWx1ZXM/OiBuYmZvcm1hdC5JT3V0cHV0W107XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBvdXRwdXQgaXMgdHJ1c3RlZC4gIFRoZSBkZWZhdWx0IGlzIGZhbHNlLlxuICAgICAqL1xuICAgIHRydXN0ZWQ/OiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG91dHB1dCBjb250ZW50IGZhY3RvcnkgdXNlZCBieSB0aGUgbW9kZWwuXG4gICAgICpcbiAgICAgKiBJZiBub3QgZ2l2ZW4sIGEgZGVmYXVsdCBmYWN0b3J5IHdpbGwgYmUgdXNlZC5cbiAgICAgKi9cbiAgICBjb250ZW50RmFjdG9yeT86IElDb250ZW50RmFjdG9yeTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHR5cGUgYWxpYXMgZm9yIGNoYW5nZWQgYXJncy5cbiAgICovXG4gIGV4cG9ydCB0eXBlIENoYW5nZWRBcmdzID0gSU9ic2VydmFibGVMaXN0LklDaGFuZ2VkQXJnczxJT3V0cHV0TW9kZWw+O1xuXG4gIC8qKlxuICAgKiBUaGUgaW50ZXJmYWNlIGZvciBhbiBvdXRwdXQgY29udGVudCBmYWN0b3J5LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhbiBvdXRwdXQgbW9kZWwuXG4gICAgICovXG4gICAgY3JlYXRlT3V0cHV0TW9kZWwob3B0aW9uczogSU91dHB1dE1vZGVsLklPcHRpb25zKTogSU91dHB1dE1vZGVsO1xuICB9XG59XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgaW1wbGVtZW50YXRpb24gb2YgdGhlIElPdXRwdXRBcmVhTW9kZWwuXG4gKi9cbmV4cG9ydCBjbGFzcyBPdXRwdXRBcmVhTW9kZWwgaW1wbGVtZW50cyBJT3V0cHV0QXJlYU1vZGVsIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBvYnNlcnZhYmxlIG91dHB1dHMgaW5zdGFuY2UuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJT3V0cHV0QXJlYU1vZGVsLklPcHRpb25zID0ge30pIHtcbiAgICB0aGlzLl90cnVzdGVkID0gISFvcHRpb25zLnRydXN0ZWQ7XG4gICAgdGhpcy5jb250ZW50RmFjdG9yeSA9XG4gICAgICBvcHRpb25zLmNvbnRlbnRGYWN0b3J5IHx8IE91dHB1dEFyZWFNb2RlbC5kZWZhdWx0Q29udGVudEZhY3Rvcnk7XG4gICAgdGhpcy5saXN0ID0gbmV3IE9ic2VydmFibGVMaXN0PElPdXRwdXRNb2RlbD4oKTtcbiAgICBpZiAob3B0aW9ucy52YWx1ZXMpIHtcbiAgICAgIGVhY2gob3B0aW9ucy52YWx1ZXMsIHZhbHVlID0+IHtcbiAgICAgICAgdGhpcy5fYWRkKHZhbHVlKTtcbiAgICAgIH0pO1xuICAgIH1cbiAgICB0aGlzLmxpc3QuY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uTGlzdENoYW5nZWQsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbW9kZWwgc3RhdGUgY2hhbmdlcy5cbiAgICovXG4gIGdldCBzdGF0ZUNoYW5nZWQoKTogSVNpZ25hbDxJT3V0cHV0QXJlYU1vZGVsLCB2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3N0YXRlQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIG1vZGVsIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgY2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElPdXRwdXRBcmVhTW9kZWwuQ2hhbmdlZEFyZ3M+IHtcbiAgICByZXR1cm4gdGhpcy5fY2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGxlbmd0aCBvZiB0aGUgaXRlbXMgaW4gdGhlIG1vZGVsLlxuICAgKi9cbiAgZ2V0IGxlbmd0aCgpOiBudW1iZXIge1xuICAgIHJldHVybiB0aGlzLmxpc3QgPyB0aGlzLmxpc3QubGVuZ3RoIDogMDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgd2hldGhlciB0aGUgbW9kZWwgaXMgdHJ1c3RlZC5cbiAgICovXG4gIGdldCB0cnVzdGVkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl90cnVzdGVkO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCB3aGV0aGVyIHRoZSBtb2RlbCBpcyB0cnVzdGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIENoYW5naW5nIHRoZSB2YWx1ZSB3aWxsIGNhdXNlIGFsbCBvZiB0aGUgbW9kZWxzIHRvIHJlLXNldC5cbiAgICovXG4gIHNldCB0cnVzdGVkKHZhbHVlOiBib29sZWFuKSB7XG4gICAgaWYgKHZhbHVlID09PSB0aGlzLl90cnVzdGVkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IHRydXN0ZWQgPSAodGhpcy5fdHJ1c3RlZCA9IHZhbHVlKTtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IHRoaXMubGlzdC5sZW5ndGg7IGkrKykge1xuICAgICAgbGV0IGl0ZW0gPSB0aGlzLmxpc3QuZ2V0KGkpO1xuICAgICAgY29uc3QgdmFsdWUgPSBpdGVtLnRvSlNPTigpO1xuICAgICAgaXRlbS5kaXNwb3NlKCk7XG4gICAgICBpdGVtID0gdGhpcy5fY3JlYXRlSXRlbSh7IHZhbHVlLCB0cnVzdGVkIH0pO1xuICAgICAgdGhpcy5saXN0LnNldChpLCBpdGVtKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIG91dHB1dCBjb250ZW50IGZhY3RvcnkgdXNlZCBieSB0aGUgbW9kZWwuXG4gICAqL1xuICByZWFkb25seSBjb250ZW50RmFjdG9yeTogSU91dHB1dEFyZWFNb2RlbC5JQ29udGVudEZhY3Rvcnk7XG5cbiAgLyoqXG4gICAqIFRlc3Qgd2hldGhlciB0aGUgbW9kZWwgaXMgZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgdXNlZCBieSB0aGUgbW9kZWwuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgdGhpcy5saXN0LmRpc3Bvc2UoKTtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhbiBpdGVtIGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqL1xuICBnZXQoaW5kZXg6IG51bWJlcik6IElPdXRwdXRNb2RlbCB7XG4gICAgcmV0dXJuIHRoaXMubGlzdC5nZXQoaW5kZXgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgdmFsdWUgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICovXG4gIHNldChpbmRleDogbnVtYmVyLCB2YWx1ZTogbmJmb3JtYXQuSU91dHB1dCk6IHZvaWQge1xuICAgIHZhbHVlID0gSlNPTkV4dC5kZWVwQ29weSh2YWx1ZSk7XG4gICAgLy8gTm9ybWFsaXplIHN0cmVhbSBkYXRhLlxuICAgIFByaXZhdGUubm9ybWFsaXplKHZhbHVlKTtcbiAgICBjb25zdCBpdGVtID0gdGhpcy5fY3JlYXRlSXRlbSh7IHZhbHVlLCB0cnVzdGVkOiB0aGlzLl90cnVzdGVkIH0pO1xuICAgIHRoaXMubGlzdC5zZXQoaW5kZXgsIGl0ZW0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhbiBvdXRwdXQsIHdoaWNoIG1heSBiZSBjb21iaW5lZCB3aXRoIHByZXZpb3VzIG91dHB1dC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIHRvdGFsIG51bWJlciBvZiBvdXRwdXRzLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBvdXRwdXQgYnVuZGxlIGlzIGNvcGllZC5cbiAgICogQ29udGlndW91cyBzdHJlYW0gb3V0cHV0cyBvZiB0aGUgc2FtZSBgbmFtZWAgYXJlIGNvbWJpbmVkLlxuICAgKi9cbiAgYWRkKG91dHB1dDogbmJmb3JtYXQuSU91dHB1dCk6IG51bWJlciB7XG4gICAgLy8gSWYgd2UgcmVjZWl2ZWQgYSBkZWxheWVkIGNsZWFyIG1lc3NhZ2UsIHRoZW4gY2xlYXIgbm93LlxuICAgIGlmICh0aGlzLmNsZWFyTmV4dCkge1xuICAgICAgdGhpcy5jbGVhcigpO1xuICAgICAgdGhpcy5jbGVhck5leHQgPSBmYWxzZTtcbiAgICB9XG5cbiAgICByZXR1cm4gdGhpcy5fYWRkKG91dHB1dCk7XG4gIH1cblxuICAvKipcbiAgICogQ2xlYXIgYWxsIG9mIHRoZSBvdXRwdXQuXG4gICAqXG4gICAqIEBwYXJhbSB3YWl0IERlbGF5IGNsZWFyaW5nIHRoZSBvdXRwdXQgdW50aWwgdGhlIG5leHQgbWVzc2FnZSBpcyBhZGRlZC5cbiAgICovXG4gIGNsZWFyKHdhaXQ6IGJvb2xlYW4gPSBmYWxzZSk6IHZvaWQge1xuICAgIHRoaXMuX2xhc3RTdHJlYW0gPSAnJztcbiAgICBpZiAod2FpdCkge1xuICAgICAgdGhpcy5jbGVhck5leHQgPSB0cnVlO1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBlYWNoKHRoaXMubGlzdCwgKGl0ZW06IElPdXRwdXRNb2RlbCkgPT4ge1xuICAgICAgaXRlbS5kaXNwb3NlKCk7XG4gICAgfSk7XG4gICAgdGhpcy5saXN0LmNsZWFyKCk7XG4gIH1cblxuICAvKipcbiAgICogRGVzZXJpYWxpemUgdGhlIG1vZGVsIGZyb20gSlNPTi5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIHdpbGwgY2xlYXIgYW55IGV4aXN0aW5nIGRhdGEuXG4gICAqL1xuICBmcm9tSlNPTih2YWx1ZXM6IG5iZm9ybWF0LklPdXRwdXRbXSkge1xuICAgIHRoaXMuY2xlYXIoKTtcbiAgICBlYWNoKHZhbHVlcywgdmFsdWUgPT4ge1xuICAgICAgdGhpcy5fYWRkKHZhbHVlKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXJpYWxpemUgdGhlIG1vZGVsIHRvIEpTT04uXG4gICAqL1xuICB0b0pTT04oKTogbmJmb3JtYXQuSU91dHB1dFtdIHtcbiAgICByZXR1cm4gdG9BcnJheShtYXAodGhpcy5saXN0LCAob3V0cHV0OiBJT3V0cHV0TW9kZWwpID0+IG91dHB1dC50b0pTT04oKSkpO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIGNvcHkgb2YgdGhlIGl0ZW0gdG8gdGhlIGxpc3QuXG4gICAqL1xuICBwcml2YXRlIF9hZGQodmFsdWU6IG5iZm9ybWF0LklPdXRwdXQpOiBudW1iZXIge1xuICAgIGNvbnN0IHRydXN0ZWQgPSB0aGlzLl90cnVzdGVkO1xuICAgIHZhbHVlID0gSlNPTkV4dC5kZWVwQ29weSh2YWx1ZSk7XG5cbiAgICAvLyBOb3JtYWxpemUgdGhlIHZhbHVlLlxuICAgIFByaXZhdGUubm9ybWFsaXplKHZhbHVlKTtcblxuICAgIC8vIENvbnNvbGlkYXRlIG91dHB1dHMgaWYgdGhleSBhcmUgc3RyZWFtIG91dHB1dHMgb2YgdGhlIHNhbWUga2luZC5cbiAgICBpZiAoXG4gICAgICBuYmZvcm1hdC5pc1N0cmVhbSh2YWx1ZSkgJiZcbiAgICAgIHRoaXMuX2xhc3RTdHJlYW0gJiZcbiAgICAgIHZhbHVlLm5hbWUgPT09IHRoaXMuX2xhc3ROYW1lICYmXG4gICAgICB0aGlzLnNob3VsZENvbWJpbmUoe1xuICAgICAgICB2YWx1ZSxcbiAgICAgICAgbGFzdE1vZGVsOiB0aGlzLmxpc3QuZ2V0KHRoaXMubGVuZ3RoIC0gMSlcbiAgICAgIH0pXG4gICAgKSB7XG4gICAgICAvLyBJbiBvcmRlciB0byBnZXQgYSBsaXN0IGNoYW5nZSBldmVudCwgd2UgYWRkIHRoZSBwcmV2aW91c1xuICAgICAgLy8gdGV4dCB0byB0aGUgY3VycmVudCBpdGVtIGFuZCByZXBsYWNlIHRoZSBwcmV2aW91cyBpdGVtLlxuICAgICAgLy8gVGhpcyBhbHNvIHJlcGxhY2VzIHRoZSBtZXRhZGF0YSBvZiB0aGUgbGFzdCBpdGVtLlxuICAgICAgdGhpcy5fbGFzdFN0cmVhbSArPSB2YWx1ZS50ZXh0IGFzIHN0cmluZztcbiAgICAgIHRoaXMuX2xhc3RTdHJlYW0gPSBQcml2YXRlLnJlbW92ZU92ZXJ3cml0dGVuQ2hhcnModGhpcy5fbGFzdFN0cmVhbSk7XG4gICAgICB2YWx1ZS50ZXh0ID0gdGhpcy5fbGFzdFN0cmVhbTtcbiAgICAgIGNvbnN0IGl0ZW0gPSB0aGlzLl9jcmVhdGVJdGVtKHsgdmFsdWUsIHRydXN0ZWQgfSk7XG4gICAgICBjb25zdCBpbmRleCA9IHRoaXMubGVuZ3RoIC0gMTtcbiAgICAgIGNvbnN0IHByZXYgPSB0aGlzLmxpc3QuZ2V0KGluZGV4KTtcbiAgICAgIHByZXYuZGlzcG9zZSgpO1xuICAgICAgdGhpcy5saXN0LnNldChpbmRleCwgaXRlbSk7XG4gICAgICByZXR1cm4gaW5kZXg7XG4gICAgfVxuXG4gICAgaWYgKG5iZm9ybWF0LmlzU3RyZWFtKHZhbHVlKSkge1xuICAgICAgdmFsdWUudGV4dCA9IFByaXZhdGUucmVtb3ZlT3ZlcndyaXR0ZW5DaGFycyh2YWx1ZS50ZXh0IGFzIHN0cmluZyk7XG4gICAgfVxuXG4gICAgLy8gQ3JlYXRlIHRoZSBuZXcgaXRlbS5cbiAgICBjb25zdCBpdGVtID0gdGhpcy5fY3JlYXRlSXRlbSh7IHZhbHVlLCB0cnVzdGVkIH0pO1xuXG4gICAgLy8gVXBkYXRlIHRoZSBzdHJlYW0gaW5mb3JtYXRpb24uXG4gICAgaWYgKG5iZm9ybWF0LmlzU3RyZWFtKHZhbHVlKSkge1xuICAgICAgdGhpcy5fbGFzdFN0cmVhbSA9IHZhbHVlLnRleHQgYXMgc3RyaW5nO1xuICAgICAgdGhpcy5fbGFzdE5hbWUgPSB2YWx1ZS5uYW1lO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9sYXN0U3RyZWFtID0gJyc7XG4gICAgfVxuXG4gICAgLy8gQWRkIHRoZSBpdGVtIHRvIG91ciBsaXN0IGFuZCByZXR1cm4gdGhlIG5ldyBsZW5ndGguXG4gICAgcmV0dXJuIHRoaXMubGlzdC5wdXNoKGl0ZW0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgYSBuZXcgdmFsdWUgc2hvdWxkIGJlIGNvbnNvbGlkYXRlZCB3aXRoIHRoZSBwcmV2aW91cyBvdXRwdXQuXG4gICAqXG4gICAqIFRoaXMgd2lsbCBvbmx5IGJlIGNhbGxlZCBpZiB0aGUgbWluaW1hbCBjcml0ZXJpYSBvZiBib3RoIGJlaW5nIHN0cmVhbVxuICAgKiBtZXNzYWdlcyBvZiB0aGUgc2FtZSB0eXBlLlxuICAgKi9cbiAgcHJvdGVjdGVkIHNob3VsZENvbWJpbmUob3B0aW9uczoge1xuICAgIHZhbHVlOiBuYmZvcm1hdC5JT3V0cHV0O1xuICAgIGxhc3RNb2RlbDogSU91dHB1dE1vZGVsO1xuICB9KSB7XG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICAvKipcbiAgICogQSBmbGFnIHRoYXQgaXMgc2V0IHdoZW4gd2Ugd2FudCB0byBjbGVhciB0aGUgb3V0cHV0IGFyZWFcbiAgICogKmFmdGVyKiB0aGUgbmV4dCBhZGRpdGlvbiB0byBpdC5cbiAgICovXG4gIHByb3RlY3RlZCBjbGVhck5leHQgPSBmYWxzZTtcblxuICAvKipcbiAgICogQW4gb2JzZXJ2YWJsZSBsaXN0IGNvbnRhaW5pbmcgdGhlIG91dHB1dCBtb2RlbHNcbiAgICogZm9yIHRoaXMgb3V0cHV0IGFyZWEuXG4gICAqL1xuICBwcm90ZWN0ZWQgbGlzdDogSU9ic2VydmFibGVMaXN0PElPdXRwdXRNb2RlbD47XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhbiBvdXRwdXQgaXRlbSBhbmQgaG9vayB1cCBpdHMgc2lnbmFscy5cbiAgICovXG4gIHByaXZhdGUgX2NyZWF0ZUl0ZW0ob3B0aW9uczogSU91dHB1dE1vZGVsLklPcHRpb25zKTogSU91dHB1dE1vZGVsIHtcbiAgICBjb25zdCBmYWN0b3J5ID0gdGhpcy5jb250ZW50RmFjdG9yeTtcbiAgICBjb25zdCBpdGVtID0gZmFjdG9yeS5jcmVhdGVPdXRwdXRNb2RlbChvcHRpb25zKTtcbiAgICBpdGVtLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkdlbmVyaWNDaGFuZ2UsIHRoaXMpO1xuICAgIHJldHVybiBpdGVtO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgbGlzdC5cbiAgICovXG4gIHByaXZhdGUgX29uTGlzdENoYW5nZWQoXG4gICAgc2VuZGVyOiBJT2JzZXJ2YWJsZUxpc3Q8SU91dHB1dE1vZGVsPixcbiAgICBhcmdzOiBJT2JzZXJ2YWJsZUxpc3QuSUNoYW5nZWRBcmdzPElPdXRwdXRNb2RlbD5cbiAgKSB7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KGFyZ3MpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byBhbiBpdGVtLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25HZW5lcmljQ2hhbmdlKCk6IHZvaWQge1xuICAgIHRoaXMuX3N0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gIH1cblxuICBwcml2YXRlIF9sYXN0U3RyZWFtOiBzdHJpbmc7XG4gIHByaXZhdGUgX2xhc3ROYW1lOiAnc3Rkb3V0JyB8ICdzdGRlcnInO1xuICBwcml2YXRlIF90cnVzdGVkID0gZmFsc2U7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfc3RhdGVDaGFuZ2VkID0gbmV3IFNpZ25hbDxJT3V0cHV0QXJlYU1vZGVsLCB2b2lkPih0aGlzKTtcbiAgcHJpdmF0ZSBfY2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgSU91dHB1dEFyZWFNb2RlbC5DaGFuZ2VkQXJncz4odGhpcyk7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgT3V0cHV0QXJlYU1vZGVsIGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgT3V0cHV0QXJlYU1vZGVsIHtcbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IGltcGxlbWVudGF0aW9uIG9mIGEgYElNb2RlbE91dHB1dEZhY3RvcnlgLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIENvbnRlbnRGYWN0b3J5IGltcGxlbWVudHMgSU91dHB1dEFyZWFNb2RlbC5JQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhbiBvdXRwdXQgbW9kZWwuXG4gICAgICovXG4gICAgY3JlYXRlT3V0cHV0TW9kZWwob3B0aW9uczogSU91dHB1dE1vZGVsLklPcHRpb25zKTogSU91dHB1dE1vZGVsIHtcbiAgICAgIHJldHVybiBuZXcgT3V0cHV0TW9kZWwob3B0aW9ucyk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IG91dHB1dCBtb2RlbCBmYWN0b3J5LlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRDb250ZW50RmFjdG9yeSA9IG5ldyBDb250ZW50RmFjdG9yeSgpO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBtb2R1bGUtcHJpdmF0ZSBmdW5jdGlvbmFsaXR5LlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBOb3JtYWxpemUgYW4gb3V0cHV0LlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIG5vcm1hbGl6ZSh2YWx1ZTogbmJmb3JtYXQuSU91dHB1dCk6IHZvaWQge1xuICAgIGlmIChuYmZvcm1hdC5pc1N0cmVhbSh2YWx1ZSkpIHtcbiAgICAgIGlmIChBcnJheS5pc0FycmF5KHZhbHVlLnRleHQpKSB7XG4gICAgICAgIHZhbHVlLnRleHQgPSAodmFsdWUudGV4dCBhcyBzdHJpbmdbXSkuam9pbignXFxuJyk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBjaGFyYWN0ZXJzIHRoYXQgYXJlIG92ZXJyaWRkZW4gYnkgYmFja3NwYWNlIGNoYXJhY3RlcnMuXG4gICAqL1xuICBmdW5jdGlvbiBmaXhCYWNrc3BhY2UodHh0OiBzdHJpbmcpOiBzdHJpbmcge1xuICAgIGxldCB0bXAgPSB0eHQ7XG4gICAgZG8ge1xuICAgICAgdHh0ID0gdG1wO1xuICAgICAgLy8gQ2FuY2VsIG91dCBhbnl0aGluZy1idXQtbmV3bGluZSBmb2xsb3dlZCBieSBiYWNrc3BhY2VcbiAgICAgIHRtcCA9IHR4dC5yZXBsYWNlKC9bXlxcbl1cXHgwOC9nbSwgJycpOyAvLyBlc2xpbnQtZGlzYWJsZS1saW5lIG5vLWNvbnRyb2wtcmVnZXhcbiAgICB9IHdoaWxlICh0bXAubGVuZ3RoIDwgdHh0Lmxlbmd0aCk7XG4gICAgcmV0dXJuIHR4dDtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgY2h1bmtzIHRoYXQgc2hvdWxkIGJlIG92ZXJyaWRkZW4gYnkgdGhlIGVmZmVjdCBvZlxuICAgKiBjYXJyaWFnZSByZXR1cm4gY2hhcmFjdGVycy5cbiAgICovXG4gIGZ1bmN0aW9uIGZpeENhcnJpYWdlUmV0dXJuKHR4dDogc3RyaW5nKTogc3RyaW5nIHtcbiAgICB0eHQgPSB0eHQucmVwbGFjZSgvXFxyK1xcbi9nbSwgJ1xcbicpOyAvLyBcXHIgZm9sbG93ZWQgYnkgXFxuIC0tPiBuZXdsaW5lXG4gICAgd2hpbGUgKHR4dC5zZWFyY2goL1xcclteJF0vZykgPiAtMSkge1xuICAgICAgY29uc3QgYmFzZSA9IHR4dC5tYXRjaCgvXiguKilcXHIrL20pIVsxXTtcbiAgICAgIGxldCBpbnNlcnQgPSB0eHQubWF0Y2goL1xccisoLiopJC9tKSFbMV07XG4gICAgICBpbnNlcnQgPSBpbnNlcnQgKyBiYXNlLnNsaWNlKGluc2VydC5sZW5ndGgsIGJhc2UubGVuZ3RoKTtcbiAgICAgIHR4dCA9IHR4dC5yZXBsYWNlKC9cXHIrLiokL20sICdcXHInKS5yZXBsYWNlKC9eLipcXHIvbSwgaW5zZXJ0KTtcbiAgICB9XG4gICAgcmV0dXJuIHR4dDtcbiAgfVxuXG4gIC8qXG4gICAqIFJlbW92ZSBjaGFyYWN0ZXJzIG92ZXJyaWRkZW4gYnkgYmFja3NwYWNlcyBhbmQgY2FycmlhZ2UgcmV0dXJuc1xuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHJlbW92ZU92ZXJ3cml0dGVuQ2hhcnModGV4dDogc3RyaW5nKTogc3RyaW5nIHtcbiAgICByZXR1cm4gZml4Q2FycmlhZ2VSZXR1cm4oZml4QmFja3NwYWNlKHRleHQpKTtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJU2Vzc2lvbkNvbnRleHQsIFdpZGdldFRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgKiBhcyBuYmZvcm1hdCBmcm9tICdAanVweXRlcmxhYi9uYmZvcm1hdCc7XG5pbXBvcnQgeyBJT3V0cHV0TW9kZWwsIElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IElSZW5kZXJNaW1lIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZS1pbnRlcmZhY2VzJztcbmltcG9ydCB7IEtlcm5lbCwgS2VybmVsTWVzc2FnZSB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7XG4gIEpTT05PYmplY3QsXG4gIFByb21pc2VEZWxlZ2F0ZSxcbiAgUmVhZG9ubHlKU09OT2JqZWN0LFxuICBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0LFxuICBVVUlEXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBBdHRhY2hlZFByb3BlcnR5IH0gZnJvbSAnQGx1bWluby9wcm9wZXJ0aWVzJztcbmltcG9ydCB7IFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFBhbmVsLCBQYW5lbExheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCBSZXNpemVPYnNlcnZlciBmcm9tICdyZXNpemUtb2JzZXJ2ZXItcG9seWZpbGwnO1xuaW1wb3J0IHsgSU91dHB1dEFyZWFNb2RlbCB9IGZyb20gJy4vbW9kZWwnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGFuIG91dHB1dCBhcmVhIHdpZGdldC5cbiAqL1xuY29uc3QgT1VUUFVUX0FSRUFfQ0xBU1MgPSAnanAtT3V0cHV0QXJlYSc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gdGhlIGRpcmVjdGlvbiBjaGlsZHJlbiBvZiBPdXRwdXRBcmVhXG4gKi9cbmNvbnN0IE9VVFBVVF9BUkVBX0lURU1fQ0xBU1MgPSAnanAtT3V0cHV0QXJlYS1jaGlsZCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYWN0dWFsIG91dHB1dHNcbiAqL1xuY29uc3QgT1VUUFVUX0FSRUFfT1VUUFVUX0NMQVNTID0gJ2pwLU91dHB1dEFyZWEtb3V0cHV0JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBwcm9tcHQgY2hpbGRyZW4gb2YgT3V0cHV0QXJlYS5cbiAqL1xuY29uc3QgT1VUUFVUX0FSRUFfUFJPTVBUX0NMQVNTID0gJ2pwLU91dHB1dEFyZWEtcHJvbXB0JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBPdXRwdXRQcm9tcHQuXG4gKi9cbmNvbnN0IE9VVFBVVF9QUk9NUFRfQ0xBU1MgPSAnanAtT3V0cHV0UHJvbXB0JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhbiBleGVjdXRpb24gcmVzdWx0LlxuICovXG5jb25zdCBFWEVDVVRFX0NMQVNTID0gJ2pwLU91dHB1dEFyZWEtZXhlY3V0ZVJlc3VsdCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgc3RkaW4gaXRlbXMgb2YgT3V0cHV0QXJlYVxuICovXG5jb25zdCBPVVRQVVRfQVJFQV9TVERJTl9JVEVNX0NMQVNTID0gJ2pwLU91dHB1dEFyZWEtc3RkaW4taXRlbSc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gc3RkaW4gd2lkZ2V0cy5cbiAqL1xuY29uc3QgU1RESU5fQ0xBU1MgPSAnanAtU3RkaW4nO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHN0ZGluIGRhdGEgcHJvbXB0IG5vZGVzLlxuICovXG5jb25zdCBTVERJTl9QUk9NUFRfQ0xBU1MgPSAnanAtU3RkaW4tcHJvbXB0JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBzdGRpbiBkYXRhIGlucHV0IG5vZGVzLlxuICovXG5jb25zdCBTVERJTl9JTlBVVF9DTEFTUyA9ICdqcC1TdGRpbi1pbnB1dCc7XG5cbi8qKiAqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqXG4gKiBPdXRwdXRBcmVhXG4gKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqL1xuXG4vKipcbiAqIEFuIG91dHB1dCBhcmVhIHdpZGdldC5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiBUaGUgd2lkZ2V0IG1vZGVsIG11c3QgYmUgc2V0IHNlcGFyYXRlbHkgYW5kIGNhbiBiZSBjaGFuZ2VkXG4gKiBhdCBhbnkgdGltZS4gIENvbnN1bWVycyBvZiB0aGUgd2lkZ2V0IG11c3QgYWNjb3VudCBmb3IgYVxuICogYG51bGxgIG1vZGVsLCBhbmQgbWF5IHdhbnQgdG8gbGlzdGVuIHRvIHRoZSBgbW9kZWxDaGFuZ2VkYFxuICogc2lnbmFsLlxuICovXG5leHBvcnQgY2xhc3MgT3V0cHV0QXJlYSBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYW4gb3V0cHV0IGFyZWEgd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogT3V0cHV0QXJlYS5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgY29uc3QgbW9kZWwgPSAodGhpcy5tb2RlbCA9IG9wdGlvbnMubW9kZWwpO1xuICAgIHRoaXMuYWRkQ2xhc3MoT1VUUFVUX0FSRUFfQ0xBU1MpO1xuICAgIHRoaXMucmVuZGVybWltZSA9IG9wdGlvbnMucmVuZGVybWltZTtcbiAgICB0aGlzLmNvbnRlbnRGYWN0b3J5ID1cbiAgICAgIG9wdGlvbnMuY29udGVudEZhY3RvcnkgfHwgT3V0cHV0QXJlYS5kZWZhdWx0Q29udGVudEZhY3Rvcnk7XG4gICAgdGhpcy5sYXlvdXQgPSBuZXcgUGFuZWxMYXlvdXQoKTtcbiAgICB0aGlzLnRyaW1tZWRPdXRwdXRNb2RlbHMgPSBuZXcgQXJyYXk8SU91dHB1dE1vZGVsPigpO1xuICAgIHRoaXMubWF4TnVtYmVyT3V0cHV0cyA9IG9wdGlvbnMubWF4TnVtYmVyT3V0cHV0cyB8fCAwO1xuICAgIHRoaXMuaGVhZEVuZEluZGV4ID0gdGhpcy5tYXhOdW1iZXJPdXRwdXRzO1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgbW9kZWwubGVuZ3RoOyBpKyspIHtcbiAgICAgIGNvbnN0IG91dHB1dCA9IG1vZGVsLmdldChpKTtcbiAgICAgIHRoaXMuX2luc2VydE91dHB1dChpLCBvdXRwdXQpO1xuICAgIH1cbiAgICBtb2RlbC5jaGFuZ2VkLmNvbm5lY3QodGhpcy5vbk1vZGVsQ2hhbmdlZCwgdGhpcyk7XG4gICAgbW9kZWwuc3RhdGVDaGFuZ2VkLmNvbm5lY3QodGhpcy5vblN0YXRlQ2hhbmdlZCwgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIG1vZGVsIHVzZWQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIHJlYWRvbmx5IG1vZGVsOiBJT3V0cHV0QXJlYU1vZGVsO1xuXG4gIC8qKlxuICAgKiBUaGUgY29udGVudCBmYWN0b3J5IHVzZWQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIHJlYWRvbmx5IGNvbnRlbnRGYWN0b3J5OiBPdXRwdXRBcmVhLklDb250ZW50RmFjdG9yeTtcblxuICAvKipcbiAgICogVGhlIHJlbmRlcm1pbWUgaW5zdGFuY2UgdXNlZCBieSB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcmVhZG9ubHkgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcblxuICAvKipcbiAgICogVGhlIGhpZGRlbiBvdXRwdXQgbW9kZWxzLlxuICAgKi9cbiAgcHJpdmF0ZSB0cmltbWVkT3V0cHV0TW9kZWxzOiBJT3V0cHV0TW9kZWxbXTtcblxuICAvKlxuICAgKiBUaGUgbWF4aW11bSBvdXRwdXRzIHRvIHNob3cgaW4gdGhlIHRyaW1tZWRcbiAgICogb3V0cHV0IGFyZWEuXG4gICAqL1xuICBwcml2YXRlIG1heE51bWJlck91dHB1dHM6IG51bWJlcjtcblxuICAvKlxuICAgKiBUaGUgaW5kZXggZm9yIHRoZSBlbmQgb2YgdGhlIGhlYWQgaW4gY2FzZSBvZiB0cmltIG1vZGUuXG4gICAqL1xuICBwcml2YXRlIGhlYWRFbmRJbmRleDogbnVtYmVyO1xuXG4gIC8qKlxuICAgKiBBIHJlYWQtb25seSBzZXF1ZW5jZSBvZiB0aGUgY2hpbGRyZW4gd2lkZ2V0cyBpbiB0aGUgb3V0cHV0IGFyZWEuXG4gICAqL1xuICBnZXQgd2lkZ2V0cygpOiBSZWFkb25seUFycmF5PFdpZGdldD4ge1xuICAgIHJldHVybiAodGhpcy5sYXlvdXQgYXMgUGFuZWxMYXlvdXQpLndpZGdldHM7XG4gIH1cblxuICAvKipcbiAgICogQSBwdWJsaWMgc2lnbmFsIHVzZWQgdG8gaW5kaWNhdGUgdGhlIG51bWJlciBvZiBvdXRwdXRzIGhhcyBjaGFuZ2VkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgaXMgdXNlZnVsIGZvciBwYXJlbnRzIHdobyB3YW50IHRvIGFwcGx5IHN0eWxpbmcgYmFzZWQgb24gdGhlIG51bWJlclxuICAgKiBvZiBvdXRwdXRzLiBFbWl0cyB0aGUgY3VycmVudCBudW1iZXIgb2Ygb3V0cHV0cy5cbiAgICovXG4gIHJlYWRvbmx5IG91dHB1dExlbmd0aENoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIG51bWJlcj4odGhpcyk7XG5cbiAgLyoqXG4gICAqIFRoZSBrZXJuZWwgZnV0dXJlIGFzc29jaWF0ZWQgd2l0aCB0aGUgb3V0cHV0IGFyZWEuXG4gICAqL1xuICBnZXQgZnV0dXJlKCk6IEtlcm5lbC5JU2hlbGxGdXR1cmU8XG4gICAgS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcXVlc3RNc2csXG4gICAgS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcGx5TXNnXG4gID4ge1xuICAgIHJldHVybiB0aGlzLl9mdXR1cmU7XG4gIH1cblxuICBzZXQgZnV0dXJlKFxuICAgIHZhbHVlOiBLZXJuZWwuSVNoZWxsRnV0dXJlPFxuICAgICAgS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcXVlc3RNc2csXG4gICAgICBLZXJuZWxNZXNzYWdlLklFeGVjdXRlUmVwbHlNc2dcbiAgICA+XG4gICkge1xuICAgIC8vIEJhaWwgaWYgdGhlIG1vZGVsIGlzIGRpc3Bvc2VkLlxuICAgIGlmICh0aGlzLm1vZGVsLmlzRGlzcG9zZWQpIHtcbiAgICAgIHRocm93IEVycm9yKCdNb2RlbCBpcyBkaXNwb3NlZCcpO1xuICAgIH1cbiAgICBpZiAodGhpcy5fZnV0dXJlID09PSB2YWx1ZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBpZiAodGhpcy5fZnV0dXJlKSB7XG4gICAgICB0aGlzLl9mdXR1cmUuZGlzcG9zZSgpO1xuICAgIH1cbiAgICB0aGlzLl9mdXR1cmUgPSB2YWx1ZTtcblxuICAgIHRoaXMubW9kZWwuY2xlYXIoKTtcblxuICAgIC8vIE1ha2Ugc3VyZSB0aGVyZSB3ZXJlIG5vIGlucHV0IHdpZGdldHMuXG4gICAgaWYgKHRoaXMud2lkZ2V0cy5sZW5ndGgpIHtcbiAgICAgIHRoaXMuX2NsZWFyKCk7XG4gICAgICB0aGlzLm91dHB1dExlbmd0aENoYW5nZWQuZW1pdCh0aGlzLm1vZGVsLmxlbmd0aCk7XG4gICAgfVxuXG4gICAgLy8gSGFuZGxlIHB1Ymxpc2hlZCBtZXNzYWdlcy5cbiAgICB2YWx1ZS5vbklPUHViID0gdGhpcy5fb25JT1B1YjtcblxuICAgIC8vIEhhbmRsZSB0aGUgZXhlY3V0ZSByZXBseS5cbiAgICB2YWx1ZS5vblJlcGx5ID0gdGhpcy5fb25FeGVjdXRlUmVwbHk7XG5cbiAgICAvLyBIYW5kbGUgc3RkaW4uXG4gICAgdmFsdWUub25TdGRpbiA9IG1zZyA9PiB7XG4gICAgICBpZiAoS2VybmVsTWVzc2FnZS5pc0lucHV0UmVxdWVzdE1zZyhtc2cpKSB7XG4gICAgICAgIHRoaXMub25JbnB1dFJlcXVlc3QobXNnLCB2YWx1ZSk7XG4gICAgICB9XG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgdXNlZCBieSB0aGUgb3V0cHV0IGFyZWEuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9mdXR1cmUpIHtcbiAgICAgIHRoaXMuX2Z1dHVyZS5kaXNwb3NlKCk7XG4gICAgICB0aGlzLl9mdXR1cmUgPSBudWxsITtcbiAgICB9XG4gICAgdGhpcy5fZGlzcGxheUlkTWFwLmNsZWFyKCk7XG4gICAgdGhpcy5fb3V0cHV0VHJhY2tlci5kaXNwb3NlKCk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEZvbGxvdyBjaGFuZ2VzIG9uIHRoZSBtb2RlbCBzdGF0ZS5cbiAgICovXG4gIHByb3RlY3RlZCBvbk1vZGVsQ2hhbmdlZChcbiAgICBzZW5kZXI6IElPdXRwdXRBcmVhTW9kZWwsXG4gICAgYXJnczogSU91dHB1dEFyZWFNb2RlbC5DaGFuZ2VkQXJnc1xuICApOiB2b2lkIHtcbiAgICBzd2l0Y2ggKGFyZ3MudHlwZSkge1xuICAgICAgY2FzZSAnYWRkJzpcbiAgICAgICAgdGhpcy5faW5zZXJ0T3V0cHV0KGFyZ3MubmV3SW5kZXgsIGFyZ3MubmV3VmFsdWVzWzBdKTtcbiAgICAgICAgdGhpcy5vdXRwdXRMZW5ndGhDaGFuZ2VkLmVtaXQodGhpcy5tb2RlbC5sZW5ndGgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3JlbW92ZSc6XG4gICAgICAgIGlmICh0aGlzLndpZGdldHMubGVuZ3RoKSB7XG4gICAgICAgICAgLy8gYWxsIGl0ZW1zIHJlbW92ZWQgZnJvbSBtb2RlbFxuICAgICAgICAgIGlmICh0aGlzLm1vZGVsLmxlbmd0aCA9PT0gMCkge1xuICAgICAgICAgICAgdGhpcy5fY2xlYXIoKTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgLy8gcmFuZ2Ugb2YgaXRlbXMgcmVtb3ZlZCBmcm9tIG1vZGVsXG4gICAgICAgICAgICAvLyByZW1vdmUgd2lkZ2V0cyBjb3JyZXNwb25kaW5nIHRvIHJlbW92ZWQgbW9kZWwgaXRlbXNcbiAgICAgICAgICAgIGNvbnN0IHN0YXJ0SW5kZXggPSBhcmdzLm9sZEluZGV4O1xuICAgICAgICAgICAgZm9yIChcbiAgICAgICAgICAgICAgbGV0IGkgPSAwO1xuICAgICAgICAgICAgICBpIDwgYXJncy5vbGRWYWx1ZXMubGVuZ3RoICYmIHN0YXJ0SW5kZXggPCB0aGlzLndpZGdldHMubGVuZ3RoO1xuICAgICAgICAgICAgICArK2lcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICBjb25zdCB3aWRnZXQgPSB0aGlzLndpZGdldHNbc3RhcnRJbmRleF07XG4gICAgICAgICAgICAgIHdpZGdldC5wYXJlbnQgPSBudWxsO1xuICAgICAgICAgICAgICB3aWRnZXQuZGlzcG9zZSgpO1xuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICAvLyBhcHBseSBpdGVtIG9mZnNldCB0byB0YXJnZXQgbW9kZWwgaXRlbSBpbmRpY2VzIGluIF9kaXNwbGF5SWRNYXBcbiAgICAgICAgICAgIHRoaXMuX21vdmVEaXNwbGF5SWRJbmRpY2VzKHN0YXJ0SW5kZXgsIGFyZ3Mub2xkVmFsdWVzLmxlbmd0aCk7XG5cbiAgICAgICAgICAgIC8vIHByZXZlbnQgaml0dGVyIGNhdXNlZCBieSBpbW1lZGlhdGUgaGVpZ2h0IGNoYW5nZVxuICAgICAgICAgICAgdGhpcy5fcHJldmVudEhlaWdodENoYW5nZUppdHRlcigpO1xuICAgICAgICAgIH1cbiAgICAgICAgICB0aGlzLm91dHB1dExlbmd0aENoYW5nZWQuZW1pdCh0aGlzLm1vZGVsLmxlbmd0aCk7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdzZXQnOlxuICAgICAgICB0aGlzLl9zZXRPdXRwdXQoYXJncy5uZXdJbmRleCwgYXJncy5uZXdWYWx1ZXNbMF0pO1xuICAgICAgICB0aGlzLm91dHB1dExlbmd0aENoYW5nZWQuZW1pdCh0aGlzLm1vZGVsLmxlbmd0aCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSBpbmRpY2VzIGluIF9kaXNwbGF5SWRNYXAgaW4gcmVzcG9uc2UgdG8gZWxlbWVudCByZW1vdmUgZnJvbSBtb2RlbCBpdGVtc1xuICAgKiAqXG4gICAqIEBwYXJhbSBzdGFydEluZGV4IC0gVGhlIGluZGV4IG9mIGZpcnN0IGVsZW1lbnQgcmVtb3ZlZFxuICAgKlxuICAgKiBAcGFyYW0gY291bnQgLSBUaGUgbnVtYmVyIG9mIGVsZW1lbnRzIHJlbW92ZWQgZnJvbSBtb2RlbCBpdGVtc1xuICAgKlxuICAgKi9cbiAgcHJpdmF0ZSBfbW92ZURpc3BsYXlJZEluZGljZXMoc3RhcnRJbmRleDogbnVtYmVyLCBjb3VudDogbnVtYmVyKSB7XG4gICAgdGhpcy5fZGlzcGxheUlkTWFwLmZvckVhY2goKGluZGljZXM6IG51bWJlcltdKSA9PiB7XG4gICAgICBjb25zdCByYW5nZUVuZCA9IHN0YXJ0SW5kZXggKyBjb3VudDtcbiAgICAgIGNvbnN0IG51bUluZGljZXMgPSBpbmRpY2VzLmxlbmd0aDtcbiAgICAgIC8vIHJldmVyc2UgbG9vcCBpbiBvcmRlciB0byBwcmV2ZW50IHJlbW92aW5nIGVsZW1lbnQgYWZmZWN0aW5nIHRoZSBpbmRleFxuICAgICAgZm9yIChsZXQgaSA9IG51bUluZGljZXMgLSAxOyBpID49IDA7IC0taSkge1xuICAgICAgICBjb25zdCBpbmRleCA9IGluZGljZXNbaV07XG4gICAgICAgIC8vIHJlbW92ZSBtb2RlbCBpdGVtIGluZGljZXMgaW4gcmVtb3ZlZCByYW5nZVxuICAgICAgICBpZiAoaW5kZXggPj0gc3RhcnRJbmRleCAmJiBpbmRleCA8IHJhbmdlRW5kKSB7XG4gICAgICAgICAgaW5kaWNlcy5zcGxpY2UoaSwgMSk7XG4gICAgICAgIH0gZWxzZSBpZiAoaW5kZXggPj0gcmFuZ2VFbmQpIHtcbiAgICAgICAgICAvLyBtb3ZlIG1vZGVsIGl0ZW0gaW5kaWNlcyB0aGF0IHdlcmUgbGFyZ2VyIHRoYW4gcmFuZ2UgZW5kXG4gICAgICAgICAgaW5kaWNlc1tpXSAtPSBjb3VudDtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEZvbGxvdyBjaGFuZ2VzIG9uIHRoZSBvdXRwdXQgbW9kZWwgc3RhdGUuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25TdGF0ZUNoYW5nZWQoc2VuZGVyOiBJT3V0cHV0QXJlYU1vZGVsKTogdm9pZCB7XG4gICAgdGhpcy50cmltbWVkT3V0cHV0TW9kZWxzID0gbmV3IEFycmF5PElPdXRwdXRNb2RlbD4oKTtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IHRoaXMubW9kZWwubGVuZ3RoOyBpKyspIHtcbiAgICAgIHRoaXMuX3NldE91dHB1dChpLCB0aGlzLm1vZGVsLmdldChpKSk7XG4gICAgfVxuICAgIHRoaXMub3V0cHV0TGVuZ3RoQ2hhbmdlZC5lbWl0KHRoaXMubW9kZWwubGVuZ3RoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhciB0aGUgd2lkZ2V0IGlucHV0cyBhbmQgb3V0cHV0cy5cbiAgICovXG4gIHByaXZhdGUgX2NsZWFyKCk6IHZvaWQge1xuICAgIC8vIEJhaWwgaWYgdGhlcmUgaXMgbm8gd29yayB0byBkby5cbiAgICBpZiAoIXRoaXMud2lkZ2V0cy5sZW5ndGgpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBSZW1vdmUgYWxsIG9mIG91ciB3aWRnZXRzLlxuICAgIGNvbnN0IGxlbmd0aCA9IHRoaXMud2lkZ2V0cy5sZW5ndGg7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBsZW5ndGg7IGkrKykge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdGhpcy53aWRnZXRzWzBdO1xuICAgICAgd2lkZ2V0LnBhcmVudCA9IG51bGw7XG4gICAgICB3aWRnZXQuZGlzcG9zZSgpO1xuICAgIH1cblxuICAgIC8vIENsZWFyIHRoZSBkaXNwbGF5IGlkIG1hcC5cbiAgICB0aGlzLl9kaXNwbGF5SWRNYXAuY2xlYXIoKTtcblxuICAgIC8vIHByZXZlbnQgaml0dGVyIGNhdXNlZCBieSBpbW1lZGlhdGUgaGVpZ2h0IGNoYW5nZVxuICAgIHRoaXMuX3ByZXZlbnRIZWlnaHRDaGFuZ2VKaXR0ZXIoKTtcbiAgfVxuXG4gIHByaXZhdGUgX3ByZXZlbnRIZWlnaHRDaGFuZ2VKaXR0ZXIoKSB7XG4gICAgLy8gV2hlbiBhbiBvdXRwdXQgYXJlYSBpcyBjbGVhcmVkIGFuZCB0aGVuIHF1aWNrbHkgcmVwbGFjZWQgd2l0aCBuZXdcbiAgICAvLyBjb250ZW50IChhcyBoYXBwZW5zIHdpdGggQGludGVyYWN0IGluIHdpZGdldHMsIGZvciBleGFtcGxlKSwgdGhlXG4gICAgLy8gcXVpY2tseSBjaGFuZ2luZyBoZWlnaHQgY2FuIG1ha2UgdGhlIHBhZ2Ugaml0dGVyLlxuICAgIC8vIFdlIGludHJvZHVjZSBhIHNtYWxsIGRlbGF5IGluIHRoZSBtaW5pbXVtIGhlaWdodFxuICAgIC8vIHRvIHByZXZlbnQgdGhpcyBqaXR0ZXIuXG4gICAgY29uc3QgcmVjdCA9IHRoaXMubm9kZS5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKTtcbiAgICB0aGlzLm5vZGUuc3R5bGUubWluSGVpZ2h0ID0gYCR7cmVjdC5oZWlnaHR9cHhgO1xuICAgIGlmICh0aGlzLl9taW5IZWlnaHRUaW1lb3V0KSB7XG4gICAgICB3aW5kb3cuY2xlYXJUaW1lb3V0KHRoaXMuX21pbkhlaWdodFRpbWVvdXQpO1xuICAgIH1cbiAgICB0aGlzLl9taW5IZWlnaHRUaW1lb3V0ID0gd2luZG93LnNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICB0aGlzLm5vZGUuc3R5bGUubWluSGVpZ2h0ID0gJyc7XG4gICAgfSwgNTApO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhbiBpbnB1dCByZXF1ZXN0IGZyb20gYSBrZXJuZWwuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25JbnB1dFJlcXVlc3QoXG4gICAgbXNnOiBLZXJuZWxNZXNzYWdlLklJbnB1dFJlcXVlc3RNc2csXG4gICAgZnV0dXJlOiBLZXJuZWwuSVNoZWxsRnV0dXJlXG4gICk6IHZvaWQge1xuICAgIC8vIEFkZCBhbiBvdXRwdXQgd2lkZ2V0IHRvIHRoZSBlbmQuXG4gICAgY29uc3QgZmFjdG9yeSA9IHRoaXMuY29udGVudEZhY3Rvcnk7XG4gICAgY29uc3Qgc3RkaW5Qcm9tcHQgPSBtc2cuY29udGVudC5wcm9tcHQ7XG4gICAgY29uc3QgcGFzc3dvcmQgPSBtc2cuY29udGVudC5wYXNzd29yZDtcblxuICAgIGNvbnN0IHBhbmVsID0gbmV3IFBhbmVsKCk7XG4gICAgcGFuZWwuYWRkQ2xhc3MoT1VUUFVUX0FSRUFfSVRFTV9DTEFTUyk7XG4gICAgcGFuZWwuYWRkQ2xhc3MoT1VUUFVUX0FSRUFfU1RESU5fSVRFTV9DTEFTUyk7XG5cbiAgICBjb25zdCBwcm9tcHQgPSBmYWN0b3J5LmNyZWF0ZU91dHB1dFByb21wdCgpO1xuICAgIHByb21wdC5hZGRDbGFzcyhPVVRQVVRfQVJFQV9QUk9NUFRfQ0xBU1MpO1xuICAgIHBhbmVsLmFkZFdpZGdldChwcm9tcHQpO1xuXG4gICAgY29uc3QgaW5wdXQgPSBmYWN0b3J5LmNyZWF0ZVN0ZGluKHtcbiAgICAgIHByb21wdDogc3RkaW5Qcm9tcHQsXG4gICAgICBwYXNzd29yZCxcbiAgICAgIGZ1dHVyZVxuICAgIH0pO1xuICAgIGlucHV0LmFkZENsYXNzKE9VVFBVVF9BUkVBX09VVFBVVF9DTEFTUyk7XG4gICAgcGFuZWwuYWRkV2lkZ2V0KGlucHV0KTtcblxuICAgIGNvbnN0IGxheW91dCA9IHRoaXMubGF5b3V0IGFzIFBhbmVsTGF5b3V0O1xuICAgIGxheW91dC5hZGRXaWRnZXQocGFuZWwpO1xuXG4gICAgLyoqXG4gICAgICogV2FpdCBmb3IgdGhlIHN0ZGluIHRvIGNvbXBsZXRlLCBhZGQgaXQgdG8gdGhlIG1vZGVsIChzbyBpdCBwZXJzaXN0cylcbiAgICAgKiBhbmQgcmVtb3ZlIHRoZSBzdGRpbiB3aWRnZXQuXG4gICAgICovXG4gICAgdm9pZCBpbnB1dC52YWx1ZS50aGVuKHZhbHVlID0+IHtcbiAgICAgIC8vIFVzZSBzdGRpbiBhcyB0aGUgc3RyZWFtIHNvIGl0IGRvZXMgbm90IGdldCBjb21iaW5lZCB3aXRoIHN0ZG91dC5cbiAgICAgIHRoaXMubW9kZWwuYWRkKHtcbiAgICAgICAgb3V0cHV0X3R5cGU6ICdzdHJlYW0nLFxuICAgICAgICBuYW1lOiAnc3RkaW4nLFxuICAgICAgICB0ZXh0OiB2YWx1ZSArICdcXG4nXG4gICAgICB9KTtcbiAgICAgIHBhbmVsLmRpc3Bvc2UoKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBVcGRhdGUgYW4gb3V0cHV0IGluIHRoZSBsYXlvdXQgaW4gcGxhY2UuXG4gICAqL1xuICBwcml2YXRlIF9zZXRPdXRwdXQoaW5kZXg6IG51bWJlciwgbW9kZWw6IElPdXRwdXRNb2RlbCk6IHZvaWQge1xuICAgIGlmIChpbmRleCA+PSB0aGlzLmhlYWRFbmRJbmRleCAmJiB0aGlzLm1heE51bWJlck91dHB1dHMgIT09IDApIHtcbiAgICAgIHRoaXMudHJpbW1lZE91dHB1dE1vZGVsc1tpbmRleCAtIHRoaXMuaGVhZEVuZEluZGV4XSA9IG1vZGVsO1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBsYXlvdXQgPSB0aGlzLmxheW91dCBhcyBQYW5lbExheW91dDtcbiAgICBjb25zdCBwYW5lbCA9IGxheW91dC53aWRnZXRzW2luZGV4XSBhcyBQYW5lbDtcbiAgICBjb25zdCByZW5kZXJlciA9IChwYW5lbC53aWRnZXRzXG4gICAgICA/IHBhbmVsLndpZGdldHNbMV1cbiAgICAgIDogcGFuZWwpIGFzIElSZW5kZXJNaW1lLklSZW5kZXJlcjtcbiAgICAvLyBDaGVjayB3aGV0aGVyIGl0IGlzIHNhZmUgdG8gcmV1c2UgcmVuZGVyZXI6XG4gICAgLy8gLSBQcmVmZXJyZWQgbWltZSB0eXBlIGhhcyBub3QgY2hhbmdlZFxuICAgIC8vIC0gSXNvbGF0aW9uIGhhcyBub3QgY2hhbmdlZFxuICAgIGNvbnN0IG1pbWVUeXBlID0gdGhpcy5yZW5kZXJtaW1lLnByZWZlcnJlZE1pbWVUeXBlKFxuICAgICAgbW9kZWwuZGF0YSxcbiAgICAgIG1vZGVsLnRydXN0ZWQgPyAnYW55JyA6ICdlbnN1cmUnXG4gICAgKTtcbiAgICBpZiAoXG4gICAgICByZW5kZXJlci5yZW5kZXJNb2RlbCAmJlxuICAgICAgUHJpdmF0ZS5jdXJyZW50UHJlZmVycmVkTWltZXR5cGUuZ2V0KHJlbmRlcmVyKSA9PT0gbWltZVR5cGUgJiZcbiAgICAgIE91dHB1dEFyZWEuaXNJc29sYXRlZChtaW1lVHlwZSwgbW9kZWwubWV0YWRhdGEpID09PVxuICAgICAgICByZW5kZXJlciBpbnN0YW5jZW9mIFByaXZhdGUuSXNvbGF0ZWRSZW5kZXJlclxuICAgICkge1xuICAgICAgdm9pZCByZW5kZXJlci5yZW5kZXJNb2RlbChtb2RlbCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIGxheW91dC53aWRnZXRzW2luZGV4XS5kaXNwb3NlKCk7XG4gICAgICB0aGlzLl9pbnNlcnRPdXRwdXQoaW5kZXgsIG1vZGVsKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIGFuZCBpbnNlcnQgYSBzaW5nbGUgb3V0cHV0IGludG8gdGhlIGxheW91dC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIGluZGV4IG9mIHRoZSBvdXRwdXQgdG8gYmUgaW5zZXJ0ZWQuXG4gICAqIEBwYXJhbSBtb2RlbCAtIFRoZSBtb2RlbCBvZiB0aGUgb3V0cHV0IHRvIGJlIGluc2VydGVkLlxuICAgKi9cbiAgcHJpdmF0ZSBfaW5zZXJ0T3V0cHV0KGluZGV4OiBudW1iZXIsIG1vZGVsOiBJT3V0cHV0TW9kZWwpOiB2b2lkIHtcbiAgICBpZiAoaW5kZXggPT09IDApIHtcbiAgICAgIHRoaXMudHJpbW1lZE91dHB1dE1vZGVscyA9IG5ldyBBcnJheTxJT3V0cHV0TW9kZWw+KCk7XG4gICAgfVxuICAgIGlmIChpbmRleCA9PT0gdGhpcy5tYXhOdW1iZXJPdXRwdXRzICYmIHRoaXMubWF4TnVtYmVyT3V0cHV0cyAhPT0gMCkge1xuICAgICAgLy8gVE9ETyBJbXByb3ZlIHN0eWxlIG9mIHRoZSBkaXNwbGF5IG1lc3NhZ2UuXG4gICAgICBjb25zdCBzZXBhcmF0b3JNb2RlbCA9IHRoaXMubW9kZWwuY29udGVudEZhY3RvcnkuY3JlYXRlT3V0cHV0TW9kZWwoe1xuICAgICAgICB2YWx1ZToge1xuICAgICAgICAgIG91dHB1dF90eXBlOiAnZGlzcGxheV9kYXRhJyxcbiAgICAgICAgICBkYXRhOiB7XG4gICAgICAgICAgICAndGV4dC9odG1sJzogYFxuICAgICAgICAgICAgICA8YSBzdHlsZT1cIm1hcmdpbjogMTBweDsgdGV4dC1kZWNvcmF0aW9uOiBub25lOyBjdXJzb3I6IHBvaW50ZXI7XCI+XG4gICAgICAgICAgICAgICAgPHByZT5PdXRwdXQgb2YgdGhpcyBjZWxsIGhhcyBiZWVuIHRyaW1tZWQgb24gdGhlIGluaXRpYWwgZGlzcGxheS48L3ByZT5cbiAgICAgICAgICAgICAgICA8cHJlPkRpc3BsYXlpbmcgdGhlIGZpcnN0ICR7dGhpcy5tYXhOdW1iZXJPdXRwdXRzfSB0b3Agb3V0cHV0cy48L3ByZT5cbiAgICAgICAgICAgICAgICA8cHJlPkNsaWNrIG9uIHRoaXMgbWVzc2FnZSB0byBnZXQgdGhlIGNvbXBsZXRlIG91dHB1dC48L3ByZT5cbiAgICAgICAgICAgICAgPC9hPlxuICAgICAgICAgICAgICBgXG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9KTtcbiAgICAgIGNvbnN0IG9uQ2xpY2sgPSAoKSA9PiB0aGlzLl9zaG93VHJpbW1lZE91dHB1dHMoKTtcbiAgICAgIGNvbnN0IHNlcGFyYXRvciA9IHRoaXMuY3JlYXRlT3V0cHV0SXRlbShzZXBhcmF0b3JNb2RlbCk7XG4gICAgICBzZXBhcmF0b3IhLm5vZGUuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCBvbkNsaWNrKTtcbiAgICAgIGNvbnN0IGxheW91dCA9IHRoaXMubGF5b3V0IGFzIFBhbmVsTGF5b3V0O1xuICAgICAgbGF5b3V0Lmluc2VydFdpZGdldCh0aGlzLmhlYWRFbmRJbmRleCwgc2VwYXJhdG9yISk7XG4gICAgfVxuICAgIGNvbnN0IG91dHB1dCA9IHRoaXMuX2NyZWF0ZU91dHB1dChtb2RlbCk7XG4gICAgY29uc3QgbGF5b3V0ID0gdGhpcy5sYXlvdXQgYXMgUGFuZWxMYXlvdXQ7XG4gICAgaWYgKGluZGV4IDwgdGhpcy5tYXhOdW1iZXJPdXRwdXRzIHx8IHRoaXMubWF4TnVtYmVyT3V0cHV0cyA9PT0gMCkge1xuICAgICAgbGF5b3V0Lmluc2VydFdpZGdldChpbmRleCwgb3V0cHV0KTtcbiAgICB9XG4gICAgaWYgKGluZGV4ID49IHRoaXMubWF4TnVtYmVyT3V0cHV0cyAmJiB0aGlzLm1heE51bWJlck91dHB1dHMgIT09IDApIHtcbiAgICAgIHRoaXMudHJpbW1lZE91dHB1dE1vZGVscy5wdXNoKG1vZGVsKTtcbiAgICB9XG4gICAgaWYgKCF0aGlzLl9vdXRwdXRUcmFja2VyLmhhcyhvdXRwdXQpKSB7XG4gICAgICB2b2lkIHRoaXMuX291dHB1dFRyYWNrZXIuYWRkKG91dHB1dCk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfY3JlYXRlT3V0cHV0KG1vZGVsOiBJT3V0cHV0TW9kZWwpOiBXaWRnZXQge1xuICAgIGxldCBvdXRwdXQgPSB0aGlzLmNyZWF0ZU91dHB1dEl0ZW0obW9kZWwpO1xuICAgIGlmIChvdXRwdXQpIHtcbiAgICAgIG91dHB1dC50b2dnbGVDbGFzcyhFWEVDVVRFX0NMQVNTLCBtb2RlbC5leGVjdXRpb25Db3VudCAhPT0gbnVsbCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIG91dHB1dCA9IG5ldyBXaWRnZXQoKTtcbiAgICB9XG4gICAgcmV0dXJuIG91dHB1dDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHdpZGdldCB0cmFja2VyIGZvciBpbmRpdmlkdWFsIG91dHB1dCB3aWRnZXRzIGluIHRoZSBvdXRwdXQgYXJlYS5cbiAgICovXG4gIGdldCBvdXRwdXRUcmFja2VyKCk6IFdpZGdldFRyYWNrZXI8V2lkZ2V0PiB7XG4gICAgcmV0dXJuIHRoaXMuX291dHB1dFRyYWNrZXI7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIHRoZSBpbmZvcm1hdGlvbiBtZXNzYWdlIHJlbGF0ZWQgdG8gdGhlIHRyaW1tZWQgb3V0cHV0XG4gICAqIGFuZCBzaG93IGFsbCBwcmV2aW91c2x5IHRyaW1tZWQgb3V0cHV0cy5cbiAgICovXG4gIHByaXZhdGUgX3Nob3dUcmltbWVkT3V0cHV0cygpIHtcbiAgICBjb25zdCBsYXlvdXQgPSB0aGlzLmxheW91dCBhcyBQYW5lbExheW91dDtcbiAgICBsYXlvdXQucmVtb3ZlV2lkZ2V0QXQodGhpcy5oZWFkRW5kSW5kZXgpO1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgdGhpcy50cmltbWVkT3V0cHV0TW9kZWxzLmxlbmd0aDsgaSsrKSB7XG4gICAgICBjb25zdCBvdXRwdXQgPSB0aGlzLl9jcmVhdGVPdXRwdXQodGhpcy50cmltbWVkT3V0cHV0TW9kZWxzW2ldKTtcbiAgICAgIGxheW91dC5pbnNlcnRXaWRnZXQodGhpcy5oZWFkRW5kSW5kZXggKyBpLCBvdXRwdXQpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYW4gb3V0cHV0IGl0ZW0gd2l0aCBhIHByb21wdCBhbmQgYWN0dWFsIG91dHB1dFxuICAgKlxuICAgKiBAcmV0dXJucyBhIHJlbmRlcmVkIHdpZGdldCwgb3IgbnVsbCBpZiB3ZSBjYW5ub3QgcmVuZGVyXG4gICAqICMjIyMgTm90ZXNcbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVPdXRwdXRJdGVtKG1vZGVsOiBJT3V0cHV0TW9kZWwpOiBXaWRnZXQgfCBudWxsIHtcbiAgICBjb25zdCBvdXRwdXQgPSB0aGlzLmNyZWF0ZVJlbmRlcmVkTWltZXR5cGUobW9kZWwpO1xuXG4gICAgaWYgKCFvdXRwdXQpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cblxuICAgIGNvbnN0IHBhbmVsID0gbmV3IFByaXZhdGUuT3V0cHV0UGFuZWwoKTtcblxuICAgIHBhbmVsLmFkZENsYXNzKE9VVFBVVF9BUkVBX0lURU1fQ0xBU1MpO1xuXG4gICAgY29uc3QgcHJvbXB0ID0gdGhpcy5jb250ZW50RmFjdG9yeS5jcmVhdGVPdXRwdXRQcm9tcHQoKTtcbiAgICBwcm9tcHQuZXhlY3V0aW9uQ291bnQgPSBtb2RlbC5leGVjdXRpb25Db3VudDtcbiAgICBwcm9tcHQuYWRkQ2xhc3MoT1VUUFVUX0FSRUFfUFJPTVBUX0NMQVNTKTtcbiAgICBwYW5lbC5hZGRXaWRnZXQocHJvbXB0KTtcblxuICAgIG91dHB1dC5hZGRDbGFzcyhPVVRQVVRfQVJFQV9PVVRQVVRfQ0xBU1MpO1xuICAgIHBhbmVsLmFkZFdpZGdldChvdXRwdXQpO1xuICAgIHJldHVybiBwYW5lbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgYSBtaW1ldHlwZVxuICAgKi9cbiAgcHJvdGVjdGVkIGNyZWF0ZVJlbmRlcmVkTWltZXR5cGUobW9kZWw6IElPdXRwdXRNb2RlbCk6IFdpZGdldCB8IG51bGwge1xuICAgIGNvbnN0IG1pbWVUeXBlID0gdGhpcy5yZW5kZXJtaW1lLnByZWZlcnJlZE1pbWVUeXBlKFxuICAgICAgbW9kZWwuZGF0YSxcbiAgICAgIG1vZGVsLnRydXN0ZWQgPyAnYW55JyA6ICdlbnN1cmUnXG4gICAgKTtcblxuICAgIGlmICghbWltZVR5cGUpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICBsZXQgb3V0cHV0ID0gdGhpcy5yZW5kZXJtaW1lLmNyZWF0ZVJlbmRlcmVyKG1pbWVUeXBlKTtcbiAgICBjb25zdCBpc29sYXRlZCA9IE91dHB1dEFyZWEuaXNJc29sYXRlZChtaW1lVHlwZSwgbW9kZWwubWV0YWRhdGEpO1xuICAgIGlmIChpc29sYXRlZCA9PT0gdHJ1ZSkge1xuICAgICAgb3V0cHV0ID0gbmV3IFByaXZhdGUuSXNvbGF0ZWRSZW5kZXJlcihvdXRwdXQpO1xuICAgIH1cbiAgICBQcml2YXRlLmN1cnJlbnRQcmVmZXJyZWRNaW1ldHlwZS5zZXQob3V0cHV0LCBtaW1lVHlwZSk7XG4gICAgb3V0cHV0LnJlbmRlck1vZGVsKG1vZGVsKS5jYXRjaChlcnJvciA9PiB7XG4gICAgICAvLyBNYW51YWxseSBhcHBlbmQgZXJyb3IgbWVzc2FnZSB0byBvdXRwdXRcbiAgICAgIGNvbnN0IHByZSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ3ByZScpO1xuICAgICAgcHJlLnRleHRDb250ZW50ID0gYEphdmFzY3JpcHQgRXJyb3I6ICR7ZXJyb3IubWVzc2FnZX1gO1xuICAgICAgb3V0cHV0Lm5vZGUuYXBwZW5kQ2hpbGQocHJlKTtcblxuICAgICAgLy8gUmVtb3ZlIG1pbWUtdHlwZS1zcGVjaWZpYyBDU1MgY2xhc3Nlc1xuICAgICAgb3V0cHV0Lm5vZGUuY2xhc3NOYW1lID0gJ2xtLVdpZGdldCBqcC1SZW5kZXJlZFRleHQnO1xuICAgICAgb3V0cHV0Lm5vZGUuc2V0QXR0cmlidXRlKFxuICAgICAgICAnZGF0YS1taW1lLXR5cGUnLFxuICAgICAgICAnYXBwbGljYXRpb24vdm5kLmp1cHl0ZXIuc3RkZXJyJ1xuICAgICAgKTtcbiAgICB9KTtcbiAgICByZXR1cm4gb3V0cHV0O1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhbiBpb3B1YiBtZXNzYWdlLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25JT1B1YiA9IChtc2c6IEtlcm5lbE1lc3NhZ2UuSUlPUHViTWVzc2FnZSkgPT4ge1xuICAgIGNvbnN0IG1vZGVsID0gdGhpcy5tb2RlbDtcbiAgICBjb25zdCBtc2dUeXBlID0gbXNnLmhlYWRlci5tc2dfdHlwZTtcbiAgICBsZXQgb3V0cHV0OiBuYmZvcm1hdC5JT3V0cHV0O1xuICAgIGNvbnN0IHRyYW5zaWVudCA9ICgobXNnLmNvbnRlbnQgYXMgYW55KS50cmFuc2llbnQgfHwge30pIGFzIEpTT05PYmplY3Q7XG4gICAgY29uc3QgZGlzcGxheUlkID0gdHJhbnNpZW50WydkaXNwbGF5X2lkJ10gYXMgc3RyaW5nO1xuICAgIGxldCB0YXJnZXRzOiBudW1iZXJbXSB8IHVuZGVmaW5lZDtcblxuICAgIHN3aXRjaCAobXNnVHlwZSkge1xuICAgICAgY2FzZSAnZXhlY3V0ZV9yZXN1bHQnOlxuICAgICAgY2FzZSAnZGlzcGxheV9kYXRhJzpcbiAgICAgIGNhc2UgJ3N0cmVhbSc6XG4gICAgICBjYXNlICdlcnJvcic6XG4gICAgICAgIG91dHB1dCA9IHsgLi4ubXNnLmNvbnRlbnQsIG91dHB1dF90eXBlOiBtc2dUeXBlIH07XG4gICAgICAgIG1vZGVsLmFkZChvdXRwdXQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2NsZWFyX291dHB1dCc6IHtcbiAgICAgICAgY29uc3Qgd2FpdCA9IChtc2cgYXMgS2VybmVsTWVzc2FnZS5JQ2xlYXJPdXRwdXRNc2cpLmNvbnRlbnQud2FpdDtcbiAgICAgICAgbW9kZWwuY2xlYXIod2FpdCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgY2FzZSAndXBkYXRlX2Rpc3BsYXlfZGF0YSc6XG4gICAgICAgIG91dHB1dCA9IHsgLi4ubXNnLmNvbnRlbnQsIG91dHB1dF90eXBlOiAnZGlzcGxheV9kYXRhJyB9O1xuICAgICAgICB0YXJnZXRzID0gdGhpcy5fZGlzcGxheUlkTWFwLmdldChkaXNwbGF5SWQpO1xuICAgICAgICBpZiAodGFyZ2V0cykge1xuICAgICAgICAgIGZvciAoY29uc3QgaW5kZXggb2YgdGFyZ2V0cykge1xuICAgICAgICAgICAgbW9kZWwuc2V0KGluZGV4LCBvdXRwdXQpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBpZiAoZGlzcGxheUlkICYmIG1zZ1R5cGUgPT09ICdkaXNwbGF5X2RhdGEnKSB7XG4gICAgICB0YXJnZXRzID0gdGhpcy5fZGlzcGxheUlkTWFwLmdldChkaXNwbGF5SWQpIHx8IFtdO1xuICAgICAgdGFyZ2V0cy5wdXNoKG1vZGVsLmxlbmd0aCAtIDEpO1xuICAgICAgdGhpcy5fZGlzcGxheUlkTWFwLnNldChkaXNwbGF5SWQsIHRhcmdldHMpO1xuICAgIH1cbiAgfTtcblxuICAvKipcbiAgICogSGFuZGxlIGFuIGV4ZWN1dGUgcmVwbHkgbWVzc2FnZS5cbiAgICovXG4gIHByaXZhdGUgX29uRXhlY3V0ZVJlcGx5ID0gKG1zZzogS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcGx5TXNnKSA9PiB7XG4gICAgLy8gQVBJIHJlc3BvbnNlcyB0aGF0IGNvbnRhaW4gYSBwYWdlciBhcmUgc3BlY2lhbCBjYXNlZCBhbmQgdGhlaXIgdHlwZVxuICAgIC8vIGlzIG92ZXJyaWRkZW4gZnJvbSAnZXhlY3V0ZV9yZXBseScgdG8gJ2Rpc3BsYXlfZGF0YScgaW4gb3JkZXIgdG9cbiAgICAvLyByZW5kZXIgb3V0cHV0LlxuICAgIGNvbnN0IG1vZGVsID0gdGhpcy5tb2RlbDtcbiAgICBjb25zdCBjb250ZW50ID0gbXNnLmNvbnRlbnQ7XG4gICAgaWYgKGNvbnRlbnQuc3RhdHVzICE9PSAnb2snKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IHBheWxvYWQgPSBjb250ZW50ICYmIGNvbnRlbnQucGF5bG9hZDtcbiAgICBpZiAoIXBheWxvYWQgfHwgIXBheWxvYWQubGVuZ3RoKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IHBhZ2VzID0gcGF5bG9hZC5maWx0ZXIoKGk6IGFueSkgPT4gKGkgYXMgYW55KS5zb3VyY2UgPT09ICdwYWdlJyk7XG4gICAgaWYgKCFwYWdlcy5sZW5ndGgpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgcGFnZSA9IEpTT04ucGFyc2UoSlNPTi5zdHJpbmdpZnkocGFnZXNbMF0pKTtcbiAgICBjb25zdCBvdXRwdXQ6IG5iZm9ybWF0LklPdXRwdXQgPSB7XG4gICAgICBvdXRwdXRfdHlwZTogJ2Rpc3BsYXlfZGF0YScsXG4gICAgICBkYXRhOiAocGFnZSBhcyBhbnkpLmRhdGEgYXMgbmJmb3JtYXQuSU1pbWVCdW5kbGUsXG4gICAgICBtZXRhZGF0YToge31cbiAgICB9O1xuICAgIG1vZGVsLmFkZChvdXRwdXQpO1xuICB9O1xuXG4gIHByaXZhdGUgX21pbkhlaWdodFRpbWVvdXQ6IG51bWJlciB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9mdXR1cmU6IEtlcm5lbC5JU2hlbGxGdXR1cmU8XG4gICAgS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcXVlc3RNc2csXG4gICAgS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcGx5TXNnXG4gID47XG4gIHByaXZhdGUgX2Rpc3BsYXlJZE1hcCA9IG5ldyBNYXA8c3RyaW5nLCBudW1iZXJbXT4oKTtcbiAgcHJpdmF0ZSBfb3V0cHV0VHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPFdpZGdldD4oe1xuICAgIG5hbWVzcGFjZTogVVVJRC51dWlkNCgpXG4gIH0pO1xufVxuXG5leHBvcnQgY2xhc3MgU2ltcGxpZmllZE91dHB1dEFyZWEgZXh0ZW5kcyBPdXRwdXRBcmVhIHtcbiAgLyoqXG4gICAqIEhhbmRsZSBhbiBpbnB1dCByZXF1ZXN0IGZyb20gYSBrZXJuZWwgYnkgZG9pbmcgbm90aGluZy5cbiAgICovXG4gIHByb3RlY3RlZCBvbklucHV0UmVxdWVzdChcbiAgICBtc2c6IEtlcm5lbE1lc3NhZ2UuSUlucHV0UmVxdWVzdE1zZyxcbiAgICBmdXR1cmU6IEtlcm5lbC5JU2hlbGxGdXR1cmVcbiAgKTogdm9pZCB7XG4gICAgcmV0dXJuO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhbiBvdXRwdXQgaXRlbSB3aXRob3V0IGEgcHJvbXB0LCBqdXN0IHRoZSBvdXRwdXQgd2lkZ2V0c1xuICAgKi9cbiAgcHJvdGVjdGVkIGNyZWF0ZU91dHB1dEl0ZW0obW9kZWw6IElPdXRwdXRNb2RlbCk6IFdpZGdldCB8IG51bGwge1xuICAgIGNvbnN0IG91dHB1dCA9IHRoaXMuY3JlYXRlUmVuZGVyZWRNaW1ldHlwZShtb2RlbCk7XG4gICAgaWYgKG91dHB1dCkge1xuICAgICAgb3V0cHV0LmFkZENsYXNzKE9VVFBVVF9BUkVBX09VVFBVVF9DTEFTUyk7XG4gICAgfVxuICAgIHJldHVybiBvdXRwdXQ7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgT3V0cHV0QXJlYSBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE91dHB1dEFyZWEge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdG8gY3JlYXRlIGFuIGBPdXRwdXRBcmVhYC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBtb2RlbCB1c2VkIGJ5IHRoZSB3aWRnZXQuXG4gICAgICovXG4gICAgbW9kZWw6IElPdXRwdXRBcmVhTW9kZWw7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29udGVudCBmYWN0b3J5IHVzZWQgYnkgdGhlIHdpZGdldCB0byBjcmVhdGUgY2hpbGRyZW4uXG4gICAgICovXG4gICAgY29udGVudEZhY3Rvcnk/OiBJQ29udGVudEZhY3Rvcnk7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcmVuZGVybWltZSBpbnN0YW5jZSB1c2VkIGJ5IHRoZSB3aWRnZXQuXG4gICAgICovXG4gICAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBtYXhpbXVtIG51bWJlciBvZiBvdXRwdXQgaXRlbXMgdG8gZGlzcGxheSBvbiB0b3AgYW5kIGJvdHRvbSBvZiBjZWxsIG91dHB1dC5cbiAgICAgKi9cbiAgICBtYXhOdW1iZXJPdXRwdXRzPzogbnVtYmVyO1xuICB9XG5cbiAgLyoqXG4gICAqIEV4ZWN1dGUgY29kZSBvbiBhbiBvdXRwdXQgYXJlYS5cbiAgICovXG4gIGV4cG9ydCBhc3luYyBmdW5jdGlvbiBleGVjdXRlKFxuICAgIGNvZGU6IHN0cmluZyxcbiAgICBvdXRwdXQ6IE91dHB1dEFyZWEsXG4gICAgc2Vzc2lvbkNvbnRleHQ6IElTZXNzaW9uQ29udGV4dCxcbiAgICBtZXRhZGF0YT86IEpTT05PYmplY3RcbiAgKTogUHJvbWlzZTxLZXJuZWxNZXNzYWdlLklFeGVjdXRlUmVwbHlNc2cgfCB1bmRlZmluZWQ+IHtcbiAgICAvLyBPdmVycmlkZSB0aGUgZGVmYXVsdCBmb3IgYHN0b3Bfb25fZXJyb3JgLlxuICAgIGxldCBzdG9wT25FcnJvciA9IHRydWU7XG4gICAgaWYgKFxuICAgICAgbWV0YWRhdGEgJiZcbiAgICAgIEFycmF5LmlzQXJyYXkobWV0YWRhdGEudGFncykgJiZcbiAgICAgIG1ldGFkYXRhLnRhZ3MuaW5kZXhPZigncmFpc2VzLWV4Y2VwdGlvbicpICE9PSAtMVxuICAgICkge1xuICAgICAgc3RvcE9uRXJyb3IgPSBmYWxzZTtcbiAgICB9XG4gICAgY29uc3QgY29udGVudDogS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcXVlc3RNc2dbJ2NvbnRlbnQnXSA9IHtcbiAgICAgIGNvZGUsXG4gICAgICBzdG9wX29uX2Vycm9yOiBzdG9wT25FcnJvclxuICAgIH07XG5cbiAgICBjb25zdCBrZXJuZWwgPSBzZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw7XG4gICAgaWYgKCFrZXJuZWwpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignU2Vzc2lvbiBoYXMgbm8ga2VybmVsLicpO1xuICAgIH1cbiAgICBjb25zdCBmdXR1cmUgPSBrZXJuZWwucmVxdWVzdEV4ZWN1dGUoY29udGVudCwgZmFsc2UsIG1ldGFkYXRhKTtcbiAgICBvdXRwdXQuZnV0dXJlID0gZnV0dXJlO1xuICAgIHJldHVybiBmdXR1cmUuZG9uZTtcbiAgfVxuXG4gIGV4cG9ydCBmdW5jdGlvbiBpc0lzb2xhdGVkKFxuICAgIG1pbWVUeXBlOiBzdHJpbmcsXG4gICAgbWV0YWRhdGE6IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3RcbiAgKTogYm9vbGVhbiB7XG4gICAgY29uc3QgbWltZU1kID0gbWV0YWRhdGFbbWltZVR5cGVdIGFzIFJlYWRvbmx5SlNPTk9iamVjdCB8IHVuZGVmaW5lZDtcbiAgICAvLyBtaW1lLXNwZWNpZmljIGhpZ2hlciBwcmlvcml0eVxuICAgIGlmIChtaW1lTWQgJiYgbWltZU1kWydpc29sYXRlZCddICE9PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybiAhIW1pbWVNZFsnaXNvbGF0ZWQnXTtcbiAgICB9IGVsc2Uge1xuICAgICAgLy8gZmFsbGJhY2sgb24gZ2xvYmFsXG4gICAgICByZXR1cm4gISFtZXRhZGF0YVsnaXNvbGF0ZWQnXTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQW4gb3V0cHV0IGFyZWEgd2lkZ2V0IGNvbnRlbnQgZmFjdG9yeS5cbiAgICpcbiAgICogVGhlIGNvbnRlbnQgZmFjdG9yeSBpcyB1c2VkIHRvIGNyZWF0ZSBjaGlsZHJlbiBpbiBhIHdheVxuICAgKiB0aGF0IGNhbiBiZSBjdXN0b21pemVkLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhbiBvdXRwdXQgcHJvbXB0LlxuICAgICAqL1xuICAgIGNyZWF0ZU91dHB1dFByb21wdCgpOiBJT3V0cHV0UHJvbXB0O1xuXG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGFuIHN0ZGluIHdpZGdldC5cbiAgICAgKi9cbiAgICBjcmVhdGVTdGRpbihvcHRpb25zOiBTdGRpbi5JT3B0aW9ucyk6IElTdGRpbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBpbXBsZW1lbnRhdGlvbiBvZiBgSUNvbnRlbnRGYWN0b3J5YC5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBDb250ZW50RmFjdG9yeSBpbXBsZW1lbnRzIElDb250ZW50RmFjdG9yeSB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIHRoZSBvdXRwdXQgcHJvbXB0IGZvciB0aGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIGNyZWF0ZU91dHB1dFByb21wdCgpOiBJT3V0cHV0UHJvbXB0IHtcbiAgICAgIHJldHVybiBuZXcgT3V0cHV0UHJvbXB0KCk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGFuIHN0ZGluIHdpZGdldC5cbiAgICAgKi9cbiAgICBjcmVhdGVTdGRpbihvcHRpb25zOiBTdGRpbi5JT3B0aW9ucyk6IElTdGRpbiB7XG4gICAgICByZXR1cm4gbmV3IFN0ZGluKG9wdGlvbnMpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBgQ29udGVudEZhY3RvcnlgIGluc3RhbmNlLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRDb250ZW50RmFjdG9yeSA9IG5ldyBDb250ZW50RmFjdG9yeSgpO1xufVxuXG4vKiogKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKlxuICogT3V0cHV0UHJvbXB0XG4gKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqL1xuXG4vKipcbiAqIFRoZSBpbnRlcmZhY2UgZm9yIGFuIG91dHB1dCBwcm9tcHQuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU91dHB1dFByb21wdCBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBUaGUgZXhlY3V0aW9uIGNvdW50IGZvciB0aGUgcHJvbXB0LlxuICAgKi9cbiAgZXhlY3V0aW9uQ291bnQ6IG5iZm9ybWF0LkV4ZWN1dGlvbkNvdW50O1xufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IG91dHB1dCBwcm9tcHQgaW1wbGVtZW50YXRpb25cbiAqL1xuZXhwb3J0IGNsYXNzIE91dHB1dFByb21wdCBleHRlbmRzIFdpZGdldCBpbXBsZW1lbnRzIElPdXRwdXRQcm9tcHQge1xuICAvKlxuICAgKiBDcmVhdGUgYW4gb3V0cHV0IHByb21wdCB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3RvcigpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuYWRkQ2xhc3MoT1VUUFVUX1BST01QVF9DTEFTUyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGV4ZWN1dGlvbiBjb3VudCBmb3IgdGhlIHByb21wdC5cbiAgICovXG4gIGdldCBleGVjdXRpb25Db3VudCgpOiBuYmZvcm1hdC5FeGVjdXRpb25Db3VudCB7XG4gICAgcmV0dXJuIHRoaXMuX2V4ZWN1dGlvbkNvdW50O1xuICB9XG4gIHNldCBleGVjdXRpb25Db3VudCh2YWx1ZTogbmJmb3JtYXQuRXhlY3V0aW9uQ291bnQpIHtcbiAgICB0aGlzLl9leGVjdXRpb25Db3VudCA9IHZhbHVlO1xuICAgIGlmICh2YWx1ZSA9PT0gbnVsbCkge1xuICAgICAgdGhpcy5ub2RlLnRleHRDb250ZW50ID0gJyc7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMubm9kZS50ZXh0Q29udGVudCA9IGBbJHt2YWx1ZX1dOmA7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfZXhlY3V0aW9uQ291bnQ6IG5iZm9ybWF0LkV4ZWN1dGlvbkNvdW50ID0gbnVsbDtcbn1cblxuLyoqICoqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKipcbiAqIFN0ZGluXG4gKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqL1xuXG4vKipcbiAqIFRoZSBzdGRpbiBpbnRlcmZhY2VcbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJU3RkaW4gZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogVGhlIHN0ZGluIHZhbHVlLlxuICAgKi9cbiAgcmVhZG9ubHkgdmFsdWU6IFByb21pc2U8c3RyaW5nPjtcbn1cblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBzdGRpbiB3aWRnZXQuXG4gKi9cbmV4cG9ydCBjbGFzcyBTdGRpbiBleHRlbmRzIFdpZGdldCBpbXBsZW1lbnRzIElTdGRpbiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgaW5wdXQgd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogU3RkaW4uSU9wdGlvbnMpIHtcbiAgICBzdXBlcih7XG4gICAgICBub2RlOiBQcml2YXRlLmNyZWF0ZUlucHV0V2lkZ2V0Tm9kZShvcHRpb25zLnByb21wdCwgb3B0aW9ucy5wYXNzd29yZClcbiAgICB9KTtcbiAgICB0aGlzLmFkZENsYXNzKFNURElOX0NMQVNTKTtcbiAgICB0aGlzLl9pbnB1dCA9IHRoaXMubm9kZS5nZXRFbGVtZW50c0J5VGFnTmFtZSgnaW5wdXQnKVswXTtcbiAgICB0aGlzLl9pbnB1dC5mb2N1cygpO1xuICAgIHRoaXMuX2Z1dHVyZSA9IG9wdGlvbnMuZnV0dXJlO1xuICAgIHRoaXMuX3ZhbHVlID0gb3B0aW9ucy5wcm9tcHQgKyAnICc7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHZhbHVlIG9mIHRoZSB3aWRnZXQuXG4gICAqL1xuICBnZXQgdmFsdWUoKTogUHJvbWlzZTxzdHJpbmc+IHtcbiAgICByZXR1cm4gdGhpcy5fcHJvbWlzZS5wcm9taXNlLnRoZW4oKCkgPT4gdGhpcy5fdmFsdWUpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgRE9NIGV2ZW50cyBmb3IgdGhlIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIGV2ZW50IC0gVGhlIERPTSBldmVudCBzZW50IHRvIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgaW1wbGVtZW50cyB0aGUgRE9NIGBFdmVudExpc3RlbmVyYCBpbnRlcmZhY2UgYW5kIGlzXG4gICAqIGNhbGxlZCBpbiByZXNwb25zZSB0byBldmVudHMgb24gdGhlIGRvY2sgcGFuZWwncyBub2RlLiBJdCBzaG91bGRcbiAgICogbm90IGJlIGNhbGxlZCBkaXJlY3RseSBieSB1c2VyIGNvZGUuXG4gICAqL1xuICBoYW5kbGVFdmVudChldmVudDogRXZlbnQpOiB2b2lkIHtcbiAgICBjb25zdCBpbnB1dCA9IHRoaXMuX2lucHV0O1xuICAgIGlmIChldmVudC50eXBlID09PSAna2V5ZG93bicpIHtcbiAgICAgIGlmICgoZXZlbnQgYXMgS2V5Ym9hcmRFdmVudCkua2V5Q29kZSA9PT0gMTMpIHtcbiAgICAgICAgLy8gRW50ZXJcbiAgICAgICAgdGhpcy5fZnV0dXJlLnNlbmRJbnB1dFJlcGx5KHtcbiAgICAgICAgICBzdGF0dXM6ICdvaycsXG4gICAgICAgICAgdmFsdWU6IGlucHV0LnZhbHVlXG4gICAgICAgIH0pO1xuICAgICAgICBpZiAoaW5wdXQudHlwZSA9PT0gJ3Bhc3N3b3JkJykge1xuICAgICAgICAgIHRoaXMuX3ZhbHVlICs9IEFycmF5KGlucHV0LnZhbHVlLmxlbmd0aCArIDEpLmpvaW4oJ8K3Jyk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgdGhpcy5fdmFsdWUgKz0gaW5wdXQudmFsdWU7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5fcHJvbWlzZS5yZXNvbHZlKHZvaWQgMCk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYWZ0ZXItYXR0YWNoYCBtZXNzYWdlcyBzZW50IHRvIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLl9pbnB1dC5hZGRFdmVudExpc3RlbmVyKCdrZXlkb3duJywgdGhpcyk7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYHVwZGF0ZS1yZXF1ZXN0YCBtZXNzYWdlcyBzZW50IHRvIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25VcGRhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHRoaXMuX2lucHV0LmZvY3VzKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBiZWZvcmUtZGV0YWNoYCBtZXNzYWdlcyBzZW50IHRvIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5faW5wdXQucmVtb3ZlRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIHRoaXMpO1xuICB9XG5cbiAgcHJpdmF0ZSBfZnV0dXJlOiBLZXJuZWwuSVNoZWxsRnV0dXJlO1xuICBwcml2YXRlIF9pbnB1dDogSFRNTElucHV0RWxlbWVudDtcbiAgcHJpdmF0ZSBfdmFsdWU6IHN0cmluZztcbiAgcHJpdmF0ZSBfcHJvbWlzZSA9IG5ldyBQcm9taXNlRGVsZWdhdGU8dm9pZD4oKTtcbn1cblxuZXhwb3J0IG5hbWVzcGFjZSBTdGRpbiB7XG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB0byBjcmVhdGUgYSBzdGRpbiB3aWRnZXQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgcHJvbXB0IHRleHQuXG4gICAgICovXG4gICAgcHJvbXB0OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBpbnB1dCBpcyBhIHBhc3N3b3JkLlxuICAgICAqL1xuICAgIHBhc3N3b3JkOiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGtlcm5lbCBmdXR1cmUgYXNzb2NpYXRlZCB3aXRoIHRoZSByZXF1ZXN0LlxuICAgICAqL1xuICAgIGZ1dHVyZTogS2VybmVsLklTaGVsbEZ1dHVyZTtcbiAgfVxufVxuXG4vKiogKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKlxuICogUHJpdmF0ZSBuYW1lc3BhY2VcbiAqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKiovXG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQ3JlYXRlIHRoZSBub2RlIGZvciBhbiBJbnB1dFdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBjcmVhdGVJbnB1dFdpZGdldE5vZGUoXG4gICAgcHJvbXB0OiBzdHJpbmcsXG4gICAgcGFzc3dvcmQ6IGJvb2xlYW5cbiAgKTogSFRNTEVsZW1lbnQge1xuICAgIGNvbnN0IG5vZGUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICBjb25zdCBwcm9tcHROb2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgncHJlJyk7XG4gICAgcHJvbXB0Tm9kZS5jbGFzc05hbWUgPSBTVERJTl9QUk9NUFRfQ0xBU1M7XG4gICAgcHJvbXB0Tm9kZS50ZXh0Q29udGVudCA9IHByb21wdDtcbiAgICBjb25zdCBpbnB1dCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2lucHV0Jyk7XG4gICAgaW5wdXQuY2xhc3NOYW1lID0gU1RESU5fSU5QVVRfQ0xBU1M7XG4gICAgaWYgKHBhc3N3b3JkKSB7XG4gICAgICBpbnB1dC50eXBlID0gJ3Bhc3N3b3JkJztcbiAgICB9XG4gICAgbm9kZS5hcHBlbmRDaGlsZChwcm9tcHROb2RlKTtcbiAgICBwcm9tcHROb2RlLmFwcGVuZENoaWxkKGlucHV0KTtcbiAgICByZXR1cm4gbm9kZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHJlbmRlcmVyIGZvciBJRnJhbWUgZGF0YS5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBJc29sYXRlZFJlbmRlcmVyXG4gICAgZXh0ZW5kcyBXaWRnZXRcbiAgICBpbXBsZW1lbnRzIElSZW5kZXJNaW1lLklSZW5kZXJlciB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGFuIGlzb2xhdGVkIHJlbmRlcmVyLlxuICAgICAqL1xuICAgIGNvbnN0cnVjdG9yKHdyYXBwZWQ6IElSZW5kZXJNaW1lLklSZW5kZXJlcikge1xuICAgICAgc3VwZXIoeyBub2RlOiBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdpZnJhbWUnKSB9KTtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLW1vZC1pc29sYXRlZCcpO1xuXG4gICAgICB0aGlzLl93cmFwcGVkID0gd3JhcHBlZDtcblxuICAgICAgLy8gT25jZSB0aGUgaWZyYW1lIGlzIGxvYWRlZCwgdGhlIHN1YmFyZWEgaXMgZHluYW1pY2FsbHkgaW5zZXJ0ZWRcbiAgICAgIGNvbnN0IGlmcmFtZSA9IHRoaXMubm9kZSBhcyBIVE1MSUZyYW1lRWxlbWVudCAmIHtcbiAgICAgICAgaGVpZ2h0Q2hhbmdlT2JzZXJ2ZXI6IFJlc2l6ZU9ic2VydmVyO1xuICAgICAgfTtcblxuICAgICAgaWZyYW1lLmZyYW1lQm9yZGVyID0gJzAnO1xuICAgICAgaWZyYW1lLnNjcm9sbGluZyA9ICdhdXRvJztcblxuICAgICAgaWZyYW1lLmFkZEV2ZW50TGlzdGVuZXIoJ2xvYWQnLCAoKSA9PiB7XG4gICAgICAgIC8vIFdvcmthcm91bmQgbmVlZGVkIGJ5IEZpcmVmb3gsIHRvIHByb3Blcmx5IHJlbmRlciBzdmcgaW5zaWRlXG4gICAgICAgIC8vIGlmcmFtZXMsIHNlZSBodHRwczovL3N0YWNrb3ZlcmZsb3cuY29tL3F1ZXN0aW9ucy8xMDE3NzE5MC9cbiAgICAgICAgLy8gc3ZnLWR5bmFtaWNhbGx5LWFkZGVkLXRvLWlmcmFtZS1kb2VzLW5vdC1yZW5kZXItY29ycmVjdGx5XG4gICAgICAgIGlmcmFtZS5jb250ZW50RG9jdW1lbnQhLm9wZW4oKTtcblxuICAgICAgICAvLyBJbnNlcnQgdGhlIHN1YmFyZWEgaW50byB0aGUgaWZyYW1lXG4gICAgICAgIC8vIFdlIG11c3QgZGlyZWN0bHkgd3JpdGUgdGhlIGh0bWwuIEF0IHRoaXMgcG9pbnQsIHN1YmFyZWEgZG9lc24ndFxuICAgICAgICAvLyBjb250YWluIGFueSB1c2VyIGNvbnRlbnQuXG4gICAgICAgIGlmcmFtZS5jb250ZW50RG9jdW1lbnQhLndyaXRlKHRoaXMuX3dyYXBwZWQubm9kZS5pbm5lckhUTUwpO1xuXG4gICAgICAgIGlmcmFtZS5jb250ZW50RG9jdW1lbnQhLmNsb3NlKCk7XG5cbiAgICAgICAgY29uc3QgYm9keSA9IGlmcmFtZS5jb250ZW50RG9jdW1lbnQhLmJvZHk7XG5cbiAgICAgICAgLy8gQWRqdXN0IHRoZSBpZnJhbWUgaGVpZ2h0IGF1dG9tYXRpY2FsbHlcbiAgICAgICAgaWZyYW1lLnN0eWxlLmhlaWdodCA9IGAke2JvZHkuc2Nyb2xsSGVpZ2h0fXB4YDtcbiAgICAgICAgaWZyYW1lLmhlaWdodENoYW5nZU9ic2VydmVyID0gbmV3IFJlc2l6ZU9ic2VydmVyKCgpID0+IHtcbiAgICAgICAgICBpZnJhbWUuc3R5bGUuaGVpZ2h0ID0gYCR7Ym9keS5zY3JvbGxIZWlnaHR9cHhgO1xuICAgICAgICB9KTtcbiAgICAgICAgaWZyYW1lLmhlaWdodENoYW5nZU9ic2VydmVyLm9ic2VydmUoYm9keSk7XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW5kZXIgYSBtaW1lIG1vZGVsLlxuICAgICAqXG4gICAgICogQHBhcmFtIG1vZGVsIC0gVGhlIG1pbWUgbW9kZWwgdG8gcmVuZGVyLlxuICAgICAqXG4gICAgICogQHJldHVybnMgQSBwcm9taXNlIHdoaWNoIHJlc29sdmVzIHdoZW4gcmVuZGVyaW5nIGlzIGNvbXBsZXRlLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoaXMgbWV0aG9kIG1heSBiZSBjYWxsZWQgbXVsdGlwbGUgdGltZXMgZHVyaW5nIHRoZSBsaWZldGltZVxuICAgICAqIG9mIHRoZSB3aWRnZXQgdG8gdXBkYXRlIGl0IGlmIGFuZCB3aGVuIG5ldyBkYXRhIGlzIGF2YWlsYWJsZS5cbiAgICAgKi9cbiAgICByZW5kZXJNb2RlbChtb2RlbDogSVJlbmRlck1pbWUuSU1pbWVNb2RlbCk6IFByb21pc2U8dm9pZD4ge1xuICAgICAgcmV0dXJuIHRoaXMuX3dyYXBwZWQucmVuZGVyTW9kZWwobW9kZWwpO1xuICAgIH1cblxuICAgIHByaXZhdGUgX3dyYXBwZWQ6IElSZW5kZXJNaW1lLklSZW5kZXJlcjtcbiAgfVxuXG4gIGV4cG9ydCBjb25zdCBjdXJyZW50UHJlZmVycmVkTWltZXR5cGUgPSBuZXcgQXR0YWNoZWRQcm9wZXJ0eTxcbiAgICBJUmVuZGVyTWltZS5JUmVuZGVyZXIsXG4gICAgc3RyaW5nXG4gID4oe1xuICAgIG5hbWU6ICdwcmVmZXJyZWRNaW1ldHlwZScsXG4gICAgY3JlYXRlOiBvd25lciA9PiAnJ1xuICB9KTtcblxuICAvKipcbiAgICogQSBgUGFuZWxgIHRoYXQncyBmb2N1c2VkIGJ5IGEgYGNvbnRleHRtZW51YCBldmVudC5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBPdXRwdXRQYW5lbCBleHRlbmRzIFBhbmVsIHtcbiAgICAvKipcbiAgICAgKiBDb25zdHJ1Y3QgYSBuZXcgYE91dHB1dFBhbmVsYCB3aWRnZXQuXG4gICAgICovXG4gICAgY29uc3RydWN0b3Iob3B0aW9ucz86IFBhbmVsLklPcHRpb25zKSB7XG4gICAgICBzdXBlcihvcHRpb25zKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBBIGNhbGxiYWNrIHRoYXQgZm9jdXNlcyBvbiB0aGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIHByaXZhdGUgX29uQ29udGV4dChfOiBFdmVudCk6IHZvaWQge1xuICAgICAgdGhpcy5ub2RlLmZvY3VzKCk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogSGFuZGxlIGBhZnRlci1hdHRhY2hgIG1lc3NhZ2VzIHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICAgKi9cbiAgICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICAgIHN1cGVyLm9uQWZ0ZXJBdHRhY2gobXNnKTtcbiAgICAgIHRoaXMubm9kZS5hZGRFdmVudExpc3RlbmVyKCdjb250ZXh0bWVudScsIHRoaXMuX29uQ29udGV4dC5iaW5kKHRoaXMpKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBIYW5kbGUgYGJlZm9yZS1kZXRhY2hgIG1lc3NhZ2VzIHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICAgKi9cbiAgICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgICBzdXBlci5vbkFmdGVyRGV0YWNoKG1zZyk7XG4gICAgICB0aGlzLm5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignY29udGV4dG1lbnUnLCB0aGlzLl9vbkNvbnRleHQuYmluZCh0aGlzKSk7XG4gICAgfVxuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9