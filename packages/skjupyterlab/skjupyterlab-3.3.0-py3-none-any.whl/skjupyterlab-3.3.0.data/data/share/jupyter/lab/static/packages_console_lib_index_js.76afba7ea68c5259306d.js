(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_console_lib_index_js"],{

/***/ "../packages/console/lib/foreign.js":
/*!******************************************!*\
  !*** ../packages/console/lib/foreign.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ForeignHandler": () => (/* binding */ ForeignHandler)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

const FOREIGN_CELL_CLASS = 'jp-CodeConsole-foreignCell';
/**
 * A handler for capturing API messages from other sessions that should be
 * rendered in a given parent.
 */
class ForeignHandler {
    /**
     * Construct a new foreign message handler.
     */
    constructor(options) {
        this._enabled = false;
        this._isDisposed = false;
        this.sessionContext = options.sessionContext;
        this.sessionContext.iopubMessage.connect(this.onIOPubMessage, this);
        this._parent = options.parent;
    }
    /**
     * Set whether the handler is able to inject foreign cells into a console.
     */
    get enabled() {
        return this._enabled;
    }
    set enabled(value) {
        this._enabled = value;
    }
    /**
     * The foreign handler's parent receiver.
     */
    get parent() {
        return this._parent;
    }
    /**
     * Test whether the handler is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the resources held by the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
    /**
     * Handler IOPub messages.
     *
     * @returns `true` if the message resulted in a new cell injection or a
     * previously injected cell being updated and `false` for all other messages.
     */
    onIOPubMessage(sender, msg) {
        var _a;
        // Only process messages if foreign cell injection is enabled.
        if (!this._enabled) {
            return false;
        }
        const kernel = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return false;
        }
        // Check whether this message came from an external session.
        const parent = this._parent;
        const session = msg.parent_header.session;
        if (session === kernel.clientId) {
            return false;
        }
        const msgType = msg.header.msg_type;
        const parentHeader = msg.parent_header;
        const parentMsgId = parentHeader.msg_id;
        let cell;
        switch (msgType) {
            case 'execute_input': {
                const inputMsg = msg;
                cell = this._newCell(parentMsgId);
                const model = cell.model;
                model.executionCount = inputMsg.content.execution_count;
                model.value.text = inputMsg.content.code;
                model.trusted = true;
                parent.update();
                return true;
            }
            case 'execute_result':
            case 'display_data':
            case 'stream':
            case 'error': {
                cell = this._parent.getCell(parentMsgId);
                if (!cell) {
                    return false;
                }
                const output = Object.assign(Object.assign({}, msg.content), { output_type: msgType });
                cell.model.outputs.add(output);
                parent.update();
                return true;
            }
            case 'clear_output': {
                const wait = msg.content.wait;
                cell = this._parent.getCell(parentMsgId);
                if (cell) {
                    cell.model.outputs.clear(wait);
                }
                return true;
            }
            default:
                return false;
        }
    }
    /**
     * Create a new code cell for an input originated from a foreign session.
     */
    _newCell(parentMsgId) {
        const cell = this.parent.createCodeCell();
        cell.addClass(FOREIGN_CELL_CLASS);
        this._parent.addCell(cell, parentMsgId);
        return cell;
    }
}


/***/ }),

/***/ "../packages/console/lib/history.js":
/*!******************************************!*\
  !*** ../packages/console/lib/history.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ConsoleHistory": () => (/* binding */ ConsoleHistory)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A console history manager object.
 */
class ConsoleHistory {
    /**
     * Construct a new console history object.
     */
    constructor(options) {
        this._cursor = 0;
        this._hasSession = false;
        this._history = [];
        this._placeholder = '';
        this._setByHistory = false;
        this._isDisposed = false;
        this._editor = null;
        this._filtered = [];
        this.sessionContext = options.sessionContext;
        void this._handleKernel();
        this.sessionContext.kernelChanged.connect(this._handleKernel, this);
    }
    /**
     * The current editor used by the history manager.
     */
    get editor() {
        return this._editor;
    }
    set editor(value) {
        if (this._editor === value) {
            return;
        }
        const prev = this._editor;
        if (prev) {
            prev.edgeRequested.disconnect(this.onEdgeRequest, this);
            prev.model.value.changed.disconnect(this.onTextChange, this);
        }
        this._editor = value;
        if (value) {
            value.edgeRequested.connect(this.onEdgeRequest, this);
            value.model.value.changed.connect(this.onTextChange, this);
        }
    }
    /**
     * The placeholder text that a history session began with.
     */
    get placeholder() {
        return this._placeholder;
    }
    /**
     * Get whether the console history manager is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the console history manager.
     */
    dispose() {
        this._isDisposed = true;
        this._history.length = 0;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
    /**
     * Get the previous item in the console history.
     *
     * @param placeholder - The placeholder string that gets temporarily added
     * to the history only for the duration of one history session. If multiple
     * placeholders are sent within a session, only the first one is accepted.
     *
     * @returns A Promise for console command text or `undefined` if unavailable.
     */
    back(placeholder) {
        if (!this._hasSession) {
            this._hasSession = true;
            this._placeholder = placeholder;
            // Filter the history with the placeholder string.
            this.setFilter(placeholder);
            this._cursor = this._filtered.length - 1;
        }
        --this._cursor;
        this._cursor = Math.max(0, this._cursor);
        const content = this._filtered[this._cursor];
        return Promise.resolve(content);
    }
    /**
     * Get the next item in the console history.
     *
     * @param placeholder - The placeholder string that gets temporarily added
     * to the history only for the duration of one history session. If multiple
     * placeholders are sent within a session, only the first one is accepted.
     *
     * @returns A Promise for console command text or `undefined` if unavailable.
     */
    forward(placeholder) {
        if (!this._hasSession) {
            this._hasSession = true;
            this._placeholder = placeholder;
            // Filter the history with the placeholder string.
            this.setFilter(placeholder);
            this._cursor = this._filtered.length;
        }
        ++this._cursor;
        this._cursor = Math.min(this._filtered.length - 1, this._cursor);
        const content = this._filtered[this._cursor];
        return Promise.resolve(content);
    }
    /**
     * Add a new item to the bottom of history.
     *
     * @param item The item being added to the bottom of history.
     *
     * #### Notes
     * If the item being added is undefined or empty, it is ignored. If the item
     * being added is the same as the last item in history, it is ignored as well
     * so that the console's history will consist of no contiguous repetitions.
     */
    push(item) {
        if (item && item !== this._history[this._history.length - 1]) {
            this._history.push(item);
        }
        this.reset();
    }
    /**
     * Reset the history navigation state, i.e., start a new history session.
     */
    reset() {
        this._cursor = this._history.length;
        this._hasSession = false;
        this._placeholder = '';
    }
    /**
     * Populate the history collection on history reply from a kernel.
     *
     * @param value The kernel message history reply.
     *
     * #### Notes
     * History entries have the shape:
     * [session: number, line: number, input: string]
     * Contiguous duplicates are stripped out of the API response.
     */
    onHistory(value) {
        this._history.length = 0;
        let last = '';
        let current = '';
        if (value.content.status === 'ok') {
            for (let i = 0; i < value.content.history.length; i++) {
                current = value.content.history[i][2];
                if (current !== last) {
                    this._history.push((last = current));
                }
            }
        }
        // Reset the history navigation cursor back to the bottom.
        this._cursor = this._history.length;
    }
    /**
     * Handle a text change signal from the editor.
     */
    onTextChange() {
        if (this._setByHistory) {
            this._setByHistory = false;
            return;
        }
        this.reset();
    }
    /**
     * Handle an edge requested signal.
     */
    onEdgeRequest(editor, location) {
        const model = editor.model;
        const source = model.value.text;
        if (location === 'top' || location === 'topLine') {
            void this.back(source).then(value => {
                if (this.isDisposed || !value) {
                    return;
                }
                if (model.value.text === value) {
                    return;
                }
                this._setByHistory = true;
                model.value.text = value;
                let columnPos = 0;
                columnPos = value.indexOf('\n');
                if (columnPos < 0) {
                    columnPos = value.length;
                }
                editor.setCursorPosition({ line: 0, column: columnPos });
            });
        }
        else {
            void this.forward(source).then(value => {
                if (this.isDisposed) {
                    return;
                }
                const text = value || this.placeholder;
                if (model.value.text === text) {
                    return;
                }
                this._setByHistory = true;
                model.value.text = text;
                const pos = editor.getPositionAt(text.length);
                if (pos) {
                    editor.setCursorPosition(pos);
                }
            });
        }
    }
    /**
     * Handle the current kernel changing.
     */
    async _handleKernel() {
        var _a;
        const kernel = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            this._history.length = 0;
            return;
        }
        return kernel.requestHistory(Private.initialRequest).then(v => {
            this.onHistory(v);
        });
    }
    /**
     * Set the filter data.
     *
     * @param filterStr - The string to use when filtering the data.
     */
    setFilter(filterStr = '') {
        // Apply the new filter and remove contiguous duplicates.
        this._filtered.length = 0;
        let last = '';
        let current = '';
        for (let i = 0; i < this._history.length; i++) {
            current = this._history[i];
            if (current !== last &&
                filterStr === current.slice(0, filterStr.length)) {
                this._filtered.push((last = current));
            }
        }
        this._filtered.push(filterStr);
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    Private.initialRequest = {
        output: false,
        raw: true,
        hist_access_type: 'tail',
        n: 500
    };
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/console/lib/index.js":
/*!****************************************!*\
  !*** ../packages/console/lib/index.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ForeignHandler": () => (/* reexport safe */ _foreign__WEBPACK_IMPORTED_MODULE_0__.ForeignHandler),
/* harmony export */   "ConsoleHistory": () => (/* reexport safe */ _history__WEBPACK_IMPORTED_MODULE_1__.ConsoleHistory),
/* harmony export */   "ConsolePanel": () => (/* reexport safe */ _panel__WEBPACK_IMPORTED_MODULE_2__.ConsolePanel),
/* harmony export */   "IConsoleTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.IConsoleTracker),
/* harmony export */   "CodeConsole": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_4__.CodeConsole)
/* harmony export */ });
/* harmony import */ var _foreign__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./foreign */ "../packages/console/lib/foreign.js");
/* harmony import */ var _history__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./history */ "../packages/console/lib/history.js");
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./panel */ "../packages/console/lib/panel.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tokens */ "../packages/console/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widget */ "../packages/console/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module console
 */







/***/ }),

/***/ "../packages/console/lib/panel.js":
/*!****************************************!*\
  !*** ../packages/console/lib/panel.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ConsolePanel": () => (/* binding */ ConsolePanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./widget */ "../packages/console/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to console panels.
 */
const PANEL_CLASS = 'jp-ConsolePanel';
/**
 * A panel which contains a console and the ability to add other children.
 */
class ConsolePanel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget {
    /**
     * Construct a console panel.
     */
    constructor(options) {
        super({ content: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Panel() });
        this._executed = null;
        this._connected = null;
        this.addClass(PANEL_CLASS);
        let { rendermime, mimeTypeService, path, basePath, name, manager, modelFactory, sessionContext, translator } = options;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        const trans = this.translator.load('jupyterlab');
        const contentFactory = (this.contentFactory =
            options.contentFactory || ConsolePanel.defaultContentFactory);
        const count = Private.count++;
        if (!path) {
            path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(basePath || '', `console-${count}-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.UUID.uuid4()}`);
        }
        sessionContext = this._sessionContext =
            sessionContext ||
                new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.SessionContext({
                    sessionManager: manager.sessions,
                    specsManager: manager.kernelspecs,
                    path,
                    name: name || trans.__('Console %1', count),
                    type: 'console',
                    kernelPreference: options.kernelPreference,
                    setBusy: options.setBusy
                });
        const resolver = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.RenderMimeRegistry.UrlResolver({
            session: sessionContext,
            contents: manager.contents
        });
        rendermime = rendermime.clone({ resolver });
        this.console = contentFactory.createConsole({
            rendermime,
            sessionContext: sessionContext,
            mimeTypeService,
            contentFactory,
            modelFactory
        });
        this.content.addWidget(this.console);
        void sessionContext.initialize().then(async (value) => {
            if (value) {
                await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.sessionContextDialogs.selectKernel(sessionContext);
            }
            this._connected = new Date();
            this._updateTitlePanel();
        });
        this.console.executed.connect(this._onExecuted, this);
        this._updateTitlePanel();
        sessionContext.kernelChanged.connect(this._updateTitlePanel, this);
        sessionContext.propertyChanged.connect(this._updateTitlePanel, this);
        this.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.consoleIcon;
        this.title.closable = true;
        this.id = `console-${count}`;
    }
    /**
     * The session used by the panel.
     */
    get sessionContext() {
        return this._sessionContext;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        this.sessionContext.dispose();
        this.console.dispose();
        super.dispose();
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        const prompt = this.console.promptCell;
        if (prompt) {
            prompt.editor.focus();
        }
    }
    /**
     * Handle `'close-request'` messages.
     */
    onCloseRequest(msg) {
        super.onCloseRequest(msg);
        this.dispose();
    }
    /**
     * Handle a console execution.
     */
    _onExecuted(sender, args) {
        this._executed = args;
        this._updateTitlePanel();
    }
    /**
     * Update the console panel title.
     */
    _updateTitlePanel() {
        Private.updateTitle(this, this._connected, this._executed, this.translator);
    }
}
/**
 * A namespace for ConsolePanel statics.
 */
(function (ConsolePanel) {
    /**
     * Default implementation of `IContentFactory`.
     */
    class ContentFactory extends _widget__WEBPACK_IMPORTED_MODULE_7__.CodeConsole.ContentFactory {
        /**
         * Create a new console panel.
         */
        createConsole(options) {
            return new _widget__WEBPACK_IMPORTED_MODULE_7__.CodeConsole(options);
        }
    }
    ConsolePanel.ContentFactory = ContentFactory;
    /**
     * A default code console content factory.
     */
    ConsolePanel.defaultContentFactory = new ContentFactory();
    /* tslint:disable */
    /**
     * The console renderer token.
     */
    ConsolePanel.IContentFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.Token('@jupyterlab/console:IContentFactory');
    /* tslint:enable */
})(ConsolePanel || (ConsolePanel = {}));
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * The counter for new consoles.
     */
    Private.count = 1;
    /**
     * Update the title of a console panel.
     */
    function updateTitle(panel, connected, executed, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const sessionContext = panel.console.sessionContext.session;
        if (sessionContext) {
            // FIXME:
            let caption = trans.__('Name: %1\n', sessionContext.name) +
                trans.__('Directory: %1\n', _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.dirname(sessionContext.path)) +
                trans.__('Kernel: %1', panel.console.sessionContext.kernelDisplayName);
            if (connected) {
                caption += trans.__('\nConnected: %1', _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.Time.format(connected.toISOString()));
            }
            if (executed) {
                caption += trans.__('\nLast Execution: %1');
            }
            panel.title.label = sessionContext.name;
            panel.title.caption = caption;
        }
        else {
            panel.title.label = trans.__('Console');
            panel.title.caption = '';
        }
    }
    Private.updateTitle = updateTitle;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/console/lib/tokens.js":
/*!*****************************************!*\
  !*** ../packages/console/lib/tokens.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IConsoleTracker": () => (/* binding */ IConsoleTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The console tracker token.
 */
const IConsoleTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/console:IConsoleTracker');


/***/ }),

/***/ "../packages/console/lib/widget.js":
/*!*****************************************!*\
  !*** ../packages/console/lib/widget.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeConsole": () => (/* binding */ CodeConsole)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/dragdrop */ "webpack/sharing/consume/default/@lumino/dragdrop/@lumino/dragdrop");
/* harmony import */ var _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_dragdrop__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _history__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./history */ "../packages/console/lib/history.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The data attribute added to a widget that has an active kernel.
 */
const KERNEL_USER = 'jpKernelUser';
/**
 * The data attribute added to a widget can run code.
 */
const CODE_RUNNER = 'jpCodeRunner';
/**
 * The class name added to console widgets.
 */
const CONSOLE_CLASS = 'jp-CodeConsole';
/**
 * The class added to console cells
 */
const CONSOLE_CELL_CLASS = 'jp-Console-cell';
/**
 * The class name added to the console banner.
 */
const BANNER_CLASS = 'jp-CodeConsole-banner';
/**
 * The class name of the active prompt cell.
 */
const PROMPT_CLASS = 'jp-CodeConsole-promptCell';
/**
 * The class name of the panel that holds cell content.
 */
const CONTENT_CLASS = 'jp-CodeConsole-content';
/**
 * The class name of the panel that holds prompts.
 */
const INPUT_CLASS = 'jp-CodeConsole-input';
/**
 * The timeout in ms for execution requests to the kernel.
 */
const EXECUTION_TIMEOUT = 250;
/**
 * The mimetype used for Jupyter cell data.
 */
const JUPYTER_CELL_MIME = 'application/vnd.jupyter.cells';
/**
 * A widget containing a Jupyter console.
 *
 * #### Notes
 * The CodeConsole class is intended to be used within a ConsolePanel
 * instance. Under most circumstances, it is not instantiated by user code.
 */
class CodeConsole extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget {
    /**
     * Construct a console widget.
     */
    constructor(options) {
        super();
        this._banner = null;
        this._executed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._mimetype = 'text/x-ipython';
        this._msgIds = new Map();
        this._msgIdCells = new Map();
        this._promptCellCreated = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._dragData = null;
        this._drag = null;
        this._focusedCell = null;
        this.addClass(CONSOLE_CLASS);
        this.node.dataset[KERNEL_USER] = 'true';
        this.node.dataset[CODE_RUNNER] = 'true';
        this.node.tabIndex = -1; // Allow the widget to take focus.
        // Create the panels that hold the content and input.
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.PanelLayout());
        this._cells = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__.ObservableList();
        this._content = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Panel();
        this._input = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Panel();
        this.contentFactory =
            options.contentFactory || CodeConsole.defaultContentFactory;
        this.modelFactory = options.modelFactory || CodeConsole.defaultModelFactory;
        this.rendermime = options.rendermime;
        this.sessionContext = options.sessionContext;
        this._mimeTypeService = options.mimeTypeService;
        // Add top-level CSS classes.
        this._content.addClass(CONTENT_CLASS);
        this._input.addClass(INPUT_CLASS);
        // Insert the content and input panes into the widget.
        layout.addWidget(this._content);
        layout.addWidget(this._input);
        this._history = new _history__WEBPACK_IMPORTED_MODULE_7__.ConsoleHistory({
            sessionContext: this.sessionContext
        });
        void this._onKernelChanged();
        this.sessionContext.kernelChanged.connect(this._onKernelChanged, this);
        this.sessionContext.statusChanged.connect(this._onKernelStatusChanged, this);
    }
    /**
     * A signal emitted when the console finished executing its prompt cell.
     */
    get executed() {
        return this._executed;
    }
    /**
     * A signal emitted when a new prompt cell is created.
     */
    get promptCellCreated() {
        return this._promptCellCreated;
    }
    /**
     * The list of content cells in the console.
     *
     * #### Notes
     * This list does not include the current banner or the prompt for a console.
     * It may include previous banners as raw cells.
     */
    get cells() {
        return this._cells;
    }
    /*
     * The console input prompt cell.
     */
    get promptCell() {
        const inputLayout = this._input.layout;
        return inputLayout.widgets[0] || null;
    }
    /**
     * Add a new cell to the content panel.
     *
     * @param cell - The code cell widget being added to the content panel.
     *
     * @param msgId - The optional execution message id for the cell.
     *
     * #### Notes
     * This method is meant for use by outside classes that want to add cells to a
     * console. It is distinct from the `inject` method in that it requires
     * rendered code cell widgets and does not execute them (though it can store
     * the execution message id).
     */
    addCell(cell, msgId) {
        cell.addClass(CONSOLE_CELL_CLASS);
        this._content.addWidget(cell);
        this._cells.push(cell);
        if (msgId) {
            this._msgIds.set(msgId, cell);
            this._msgIdCells.set(cell, msgId);
        }
        cell.disposed.connect(this._onCellDisposed, this);
        this.update();
    }
    /**
     * Add a banner cell.
     */
    addBanner() {
        if (this._banner) {
            // An old banner just becomes a normal cell now.
            const cell = this._banner;
            this._cells.push(this._banner);
            cell.disposed.connect(this._onCellDisposed, this);
        }
        // Create the banner.
        const model = this.modelFactory.createRawCell({});
        model.value.text = '...';
        const banner = (this._banner = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.RawCell({
            model,
            contentFactory: this.contentFactory,
            placeholder: false
        })).initializeState();
        banner.addClass(BANNER_CLASS);
        banner.readOnly = true;
        this._content.addWidget(banner);
    }
    /**
     * Clear the code cells.
     */
    clear() {
        // Dispose all the content cells
        const cells = this._cells;
        while (cells.length > 0) {
            cells.get(0).dispose();
        }
    }
    /**
     * Create a new cell with the built-in factory.
     */
    createCodeCell() {
        const factory = this.contentFactory;
        const options = this._createCodeCellOptions();
        const cell = factory.createCodeCell(options);
        cell.readOnly = true;
        cell.model.mimeType = this._mimetype;
        return cell;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        // Do nothing if already disposed.
        if (this.isDisposed) {
            return;
        }
        this._cells.clear();
        this._msgIdCells = null;
        this._msgIds = null;
        this._history.dispose();
        super.dispose();
    }
    /**
     * Execute the current prompt.
     *
     * @param force - Whether to force execution without checking code
     * completeness.
     *
     * @param timeout - The length of time, in milliseconds, that the execution
     * should wait for the API to determine whether code being submitted is
     * incomplete before attempting submission anyway. The default value is `250`.
     */
    async execute(force = false, timeout = EXECUTION_TIMEOUT) {
        var _a, _b;
        if (((_b = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.status) === 'dead') {
            return;
        }
        const promptCell = this.promptCell;
        if (!promptCell) {
            throw new Error('Cannot execute without a prompt cell');
        }
        promptCell.model.trusted = true;
        if (force) {
            // Create a new prompt cell before kernel execution to allow typeahead.
            this.newPromptCell();
            await this._execute(promptCell);
            return;
        }
        // Check whether we should execute.
        const shouldExecute = await this._shouldExecute(timeout);
        if (this.isDisposed) {
            return;
        }
        if (shouldExecute) {
            // Create a new prompt cell before kernel execution to allow typeahead.
            this.newPromptCell();
            this.promptCell.editor.focus();
            await this._execute(promptCell);
        }
        else {
            // add a newline if we shouldn't execute
            promptCell.editor.newIndentedLine();
        }
    }
    /**
     * Get a cell given a message id.
     *
     * @param msgId - The message id.
     */
    getCell(msgId) {
        return this._msgIds.get(msgId);
    }
    /**
     * Inject arbitrary code for the console to execute immediately.
     *
     * @param code - The code contents of the cell being injected.
     *
     * @returns A promise that indicates when the injected cell's execution ends.
     */
    inject(code, metadata = {}) {
        const cell = this.createCodeCell();
        cell.model.value.text = code;
        for (const key of Object.keys(metadata)) {
            cell.model.metadata.set(key, metadata[key]);
        }
        this.addCell(cell);
        return this._execute(cell);
    }
    /**
     * Insert a line break in the prompt cell.
     */
    insertLinebreak() {
        const promptCell = this.promptCell;
        if (!promptCell) {
            return;
        }
        promptCell.editor.newIndentedLine();
    }
    /**
     * Replaces the selected text in the prompt cell.
     *
     * @param text - The text to replace the selection.
     */
    replaceSelection(text) {
        var _a, _b;
        const promptCell = this.promptCell;
        if (!promptCell) {
            return;
        }
        (_b = (_a = promptCell.editor).replaceSelection) === null || _b === void 0 ? void 0 : _b.call(_a, text);
    }
    /**
     * Serialize the output.
     *
     * #### Notes
     * This only serializes the code cells and the prompt cell if it exists, and
     * skips any old banner cells.
     */
    serialize() {
        const cells = [];
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.each)(this._cells, cell => {
            const model = cell.model;
            if ((0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.isCodeCellModel)(model)) {
                cells.push(model.toJSON());
            }
        });
        if (this.promptCell) {
            cells.push(this.promptCell.model.toJSON());
        }
        return cells;
    }
    /**
     * Handle `mousedown` events for the widget.
     */
    _evtMouseDown(event) {
        const { button, shiftKey } = event;
        // We only handle main or secondary button actions.
        if (!(button === 0 || button === 2) ||
            // Shift right-click gives the browser default behavior.
            (shiftKey && button === 2)) {
            return;
        }
        let target = event.target;
        const cellFilter = (node) => node.classList.contains(CONSOLE_CELL_CLASS);
        let cellIndex = _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CellDragUtils.findCell(target, this._cells, cellFilter);
        if (cellIndex === -1) {
            // `event.target` sometimes gives an orphaned node in
            // Firefox 57, which can have `null` anywhere in its parent line. If we fail
            // to find a cell using `event.target`, try again using a target
            // reconstructed from the position of the click event.
            target = document.elementFromPoint(event.clientX, event.clientY);
            cellIndex = _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CellDragUtils.findCell(target, this._cells, cellFilter);
        }
        if (cellIndex === -1) {
            return;
        }
        const cell = this._cells.get(cellIndex);
        const targetArea = _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CellDragUtils.detectTargetArea(cell, event.target);
        if (targetArea === 'prompt') {
            this._dragData = {
                pressX: event.clientX,
                pressY: event.clientY,
                index: cellIndex
            };
            this._focusedCell = cell;
            document.addEventListener('mouseup', this, true);
            document.addEventListener('mousemove', this, true);
            event.preventDefault();
        }
    }
    /**
     * Handle `mousemove` event of widget
     */
    _evtMouseMove(event) {
        const data = this._dragData;
        if (data &&
            _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CellDragUtils.shouldStartDrag(data.pressX, data.pressY, event.clientX, event.clientY)) {
            void this._startDrag(data.index, event.clientX, event.clientY);
        }
    }
    /**
     * Start a drag event
     */
    _startDrag(index, clientX, clientY) {
        const cellModel = this._focusedCell.model;
        const selected = [cellModel.toJSON()];
        const dragImage = _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CellDragUtils.createCellDragImage(this._focusedCell, selected);
        this._drag = new _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_4__.Drag({
            mimeData: new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.MimeData(),
            dragImage,
            proposedAction: 'copy',
            supportedActions: 'copy',
            source: this
        });
        this._drag.mimeData.setData(JUPYTER_CELL_MIME, selected);
        const textContent = cellModel.value.text;
        this._drag.mimeData.setData('text/plain', textContent);
        this._focusedCell = null;
        document.removeEventListener('mousemove', this, true);
        document.removeEventListener('mouseup', this, true);
        return this._drag.start(clientX, clientY).then(() => {
            if (this.isDisposed) {
                return;
            }
            this._drag = null;
            this._dragData = null;
        });
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event -The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'keydown':
                this._evtKeyDown(event);
                break;
            case 'mousedown':
                this._evtMouseDown(event);
                break;
            case 'mousemove':
                this._evtMouseMove(event);
                break;
            case 'mouseup':
                this._evtMouseUp(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after_attach` messages for the widget.
     */
    onAfterAttach(msg) {
        const node = this.node;
        node.addEventListener('keydown', this, true);
        node.addEventListener('click', this);
        node.addEventListener('mousedown', this);
        // Create a prompt if necessary.
        if (!this.promptCell) {
            this.newPromptCell();
        }
        else {
            this.promptCell.editor.focus();
            this.update();
        }
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.node;
        node.removeEventListener('keydown', this, true);
        node.removeEventListener('click', this);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        const editor = this.promptCell && this.promptCell.editor;
        if (editor) {
            editor.focus();
        }
        this.update();
    }
    /**
     * Make a new prompt cell.
     */
    newPromptCell() {
        let promptCell = this.promptCell;
        const input = this._input;
        // Make the last prompt read-only, clear its signals, and move to content.
        if (promptCell) {
            promptCell.readOnly = true;
            promptCell.removeClass(PROMPT_CLASS);
            _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal.clearData(promptCell.editor);
            const child = input.widgets[0];
            child.parent = null;
            this.addCell(promptCell);
        }
        // Create the new prompt cell.
        const factory = this.contentFactory;
        const options = this._createCodeCellOptions();
        promptCell = factory.createCodeCell(options);
        promptCell.model.mimeType = this._mimetype;
        promptCell.addClass(PROMPT_CLASS);
        // Add the prompt cell to the DOM, making `this.promptCell` valid again.
        this._input.addWidget(promptCell);
        // Suppress the default "Enter" key handling.
        const editor = promptCell.editor;
        editor.addKeydownHandler(this._onEditorKeydown);
        this._history.editor = editor;
        this._promptCellCreated.emit(promptCell);
    }
    /**
     * Handle `update-request` messages.
     */
    onUpdateRequest(msg) {
        Private.scrollToBottom(this._content.node);
    }
    /**
     * Handle the `'keydown'` event for the widget.
     */
    _evtKeyDown(event) {
        const editor = this.promptCell && this.promptCell.editor;
        if (!editor) {
            return;
        }
        if (event.keyCode === 13 && !editor.hasFocus()) {
            event.preventDefault();
            editor.focus();
        }
        else if (event.keyCode === 27 && editor.hasFocus()) {
            // Set to command mode
            event.preventDefault();
            event.stopPropagation();
            this.node.focus();
        }
    }
    /**
     * Handle the `'mouseup'` event for the widget.
     */
    _evtMouseUp(event) {
        if (this.promptCell &&
            this.promptCell.node.contains(event.target)) {
            this.promptCell.editor.focus();
        }
    }
    /**
     * Execute the code in the current prompt cell.
     */
    _execute(cell) {
        const source = cell.model.value.text;
        this._history.push(source);
        // If the source of the console is just "clear", clear the console as we
        // do in IPython or QtConsole.
        if (source === 'clear' || source === '%clear') {
            this.clear();
            return Promise.resolve(void 0);
        }
        cell.model.contentChanged.connect(this.update, this);
        const onSuccess = (value) => {
            if (this.isDisposed) {
                return;
            }
            if (value && value.content.status === 'ok') {
                const content = value.content;
                // Use deprecated payloads for backwards compatibility.
                if (content.payload && content.payload.length) {
                    const setNextInput = content.payload.filter(i => {
                        return i.source === 'set_next_input';
                    })[0];
                    if (setNextInput) {
                        const text = setNextInput.text;
                        // Ignore the `replace` value and always set the next cell.
                        cell.model.value.text = text;
                    }
                }
            }
            else if (value && value.content.status === 'error') {
                (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.each)(this._cells, (cell) => {
                    if (cell.model.executionCount === null) {
                        cell.setPrompt('');
                    }
                });
            }
            cell.model.contentChanged.disconnect(this.update, this);
            this.update();
            this._executed.emit(new Date());
        };
        const onFailure = () => {
            if (this.isDisposed) {
                return;
            }
            cell.model.contentChanged.disconnect(this.update, this);
            this.update();
        };
        return _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell.execute(cell, this.sessionContext).then(onSuccess, onFailure);
    }
    /**
     * Update the console based on the kernel info.
     */
    _handleInfo(info) {
        if (info.status !== 'ok') {
            this._banner.model.value.text = 'Error in getting kernel banner';
            return;
        }
        this._banner.model.value.text = info.banner;
        const lang = info.language_info;
        this._mimetype = this._mimeTypeService.getMimeTypeByLanguage(lang);
        if (this.promptCell) {
            this.promptCell.model.mimeType = this._mimetype;
        }
    }
    /**
     * Create the options used to initialize a code cell widget.
     */
    _createCodeCellOptions() {
        const contentFactory = this.contentFactory;
        const modelFactory = this.modelFactory;
        const model = modelFactory.createCodeCell({});
        const rendermime = this.rendermime;
        return { model, rendermime, contentFactory, placeholder: false };
    }
    /**
     * Handle cell disposed signals.
     */
    _onCellDisposed(sender, args) {
        if (!this.isDisposed) {
            this._cells.removeValue(sender);
            const msgId = this._msgIdCells.get(sender);
            if (msgId) {
                this._msgIdCells.delete(sender);
                this._msgIds.delete(msgId);
            }
        }
    }
    /**
     * Test whether we should execute the prompt cell.
     */
    _shouldExecute(timeout) {
        const promptCell = this.promptCell;
        if (!promptCell) {
            return Promise.resolve(false);
        }
        const model = promptCell.model;
        const code = model.value.text;
        return new Promise((resolve, reject) => {
            var _a;
            const timer = setTimeout(() => {
                resolve(true);
            }, timeout);
            const kernel = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (!kernel) {
                resolve(false);
                return;
            }
            kernel
                .requestIsComplete({ code })
                .then(isComplete => {
                clearTimeout(timer);
                if (this.isDisposed) {
                    resolve(false);
                }
                if (isComplete.content.status !== 'incomplete') {
                    resolve(true);
                    return;
                }
                resolve(false);
            })
                .catch(() => {
                resolve(true);
            });
        });
    }
    /**
     * Handle a keydown event on an editor.
     */
    _onEditorKeydown(editor, event) {
        // Suppress "Enter" events.
        return event.keyCode === 13;
    }
    /**
     * Handle a change to the kernel.
     */
    async _onKernelChanged() {
        var _a;
        this.clear();
        if (this._banner) {
            this._banner.dispose();
            this._banner = null;
        }
        this.addBanner();
        if ((_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) {
            this._handleInfo(await this.sessionContext.session.kernel.info);
        }
    }
    /**
     * Handle a change to the kernel status.
     */
    async _onKernelStatusChanged() {
        var _a;
        const kernel = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if ((kernel === null || kernel === void 0 ? void 0 : kernel.status) === 'restarting') {
            this.addBanner();
            this._handleInfo(await (kernel === null || kernel === void 0 ? void 0 : kernel.info));
        }
    }
}
/**
 * A namespace for CodeConsole statics.
 */
(function (CodeConsole) {
    /**
     * Default implementation of `IContentFactory`.
     */
    class ContentFactory extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.Cell.ContentFactory {
        /**
         * Create a new code cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createCodeCell(options) {
            if (!options.contentFactory) {
                options.contentFactory = this;
            }
            return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell(options).initializeState();
        }
        /**
         * Create a new raw cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createRawCell(options) {
            if (!options.contentFactory) {
                options.contentFactory = this;
            }
            return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.RawCell(options).initializeState();
        }
    }
    CodeConsole.ContentFactory = ContentFactory;
    /**
     * A default content factory for the code console.
     */
    CodeConsole.defaultContentFactory = new ContentFactory();
    /**
     * The default implementation of an `IModelFactory`.
     */
    class ModelFactory {
        /**
         * Create a new cell model factory.
         */
        constructor(options = {}) {
            this.codeCellContentFactory =
                options.codeCellContentFactory || _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCellModel.defaultContentFactory;
        }
        /**
         * Create a new code cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new code cell. If a source cell is provided, the
         *   new cell will be initialized with the data from the source.
         *   If the contentFactory is not provided, the instance
         *   `codeCellContentFactory` will be used.
         */
        createCodeCell(options) {
            if (!options.contentFactory) {
                options.contentFactory = this.codeCellContentFactory;
            }
            return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCellModel(options);
        }
        /**
         * Create a new raw cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new raw cell. If a source cell is provided, the
         *   new cell will be initialized with the data from the source.
         */
        createRawCell(options) {
            return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.RawCellModel(options);
        }
    }
    CodeConsole.ModelFactory = ModelFactory;
    /**
     * The default `ModelFactory` instance.
     */
    CodeConsole.defaultModelFactory = new ModelFactory({});
})(CodeConsole || (CodeConsole = {}));
/**
 * A namespace for console widget private data.
 */
var Private;
(function (Private) {
    /**
     * Jump to the bottom of a node.
     *
     * @param node - The scrollable element.
     */
    function scrollToBottom(node) {
        node.scrollTop = node.scrollHeight - node.clientHeight;
    }
    Private.scrollToBottom = scrollToBottom;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29uc29sZS9zcmMvZm9yZWlnbi50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29uc29sZS9zcmMvaGlzdG9yeS50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29uc29sZS9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvbnNvbGUvc3JjL3BhbmVsLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb25zb2xlL3NyYy90b2tlbnMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvbnNvbGUvc3JjL3dpZGdldC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBT2hCO0FBRTNDLE1BQU0sa0JBQWtCLEdBQUcsNEJBQTRCLENBQUM7QUFFeEQ7OztHQUdHO0FBQ0ksTUFBTSxjQUFjO0lBQ3pCOztPQUVHO0lBQ0gsWUFBWSxPQUFnQztRQTZIcEMsYUFBUSxHQUFHLEtBQUssQ0FBQztRQUVqQixnQkFBVyxHQUFHLEtBQUssQ0FBQztRQTlIMUIsSUFBSSxDQUFDLGNBQWMsR0FBRyxPQUFPLENBQUMsY0FBYyxDQUFDO1FBQzdDLElBQUksQ0FBQyxjQUFjLENBQUMsWUFBWSxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsY0FBYyxFQUFFLElBQUksQ0FBQyxDQUFDO1FBQ3BFLElBQUksQ0FBQyxPQUFPLEdBQUcsT0FBTyxDQUFDLE1BQU0sQ0FBQztJQUNoQyxDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLE9BQU87UUFDVCxP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QUFJLENBQUMsc0JBQXNCO2dCQUN6QixPQUFPLENBQUMsc0JBQXNCLElBQUksa0ZBQW1DLENBQUM7UUFDMUUsQ0FBQztRQU9EOzs7Ozs7Ozs7V0FTRztRQUNILGNBQWMsQ0FBQyxPQUErQjtZQUM1QyxJQUFJLENBQUMsT0FBTyxDQUFDLGNBQWMsRUFBRTtnQkFDM0IsT0FBTyxDQUFDLGNBQWMsR0FBRyxJQUFJLENBQUMsc0JBQXNCLENBQUM7YUFDdEQ7WUFDRCxPQUFPLElBQUksNERBQWEsQ0FBQyxPQUFPLENBQUMsQ0FBQztRQUNwQyxDQUFDO1FBRUQ7Ozs7Ozs7V0FPRztRQUNILGFBQWEsQ0FBQyxPQUEyQjtZQUN2QyxPQUFPLElBQUksMkRBQVksQ0FBQyxPQUFPLENBQUMsQ0FBQztRQUNuQyxDQUFDO0tBQ0Y7SUExQ1ksd0JBQVksZUEwQ3hCO0lBWUQ7O09BRUc7SUFDVSwrQkFBbUIsR0FBRyxJQUFJLFlBQVksQ0FBQyxFQUFFLENBQUMsQ0FBQztBQUMxRCxDQUFDLEVBM0xnQixXQUFXLEtBQVgsV0FBVyxRQTJMM0I7QUFFRDs7R0FFRztBQUNILElBQVUsT0FBTyxDQVNoQjtBQVRELFdBQVUsT0FBTztJQUNmOzs7O09BSUc7SUFDSCxTQUFnQixjQUFjLENBQUMsSUFBaUI7UUFDOUMsSUFBSSxDQUFDLFNBQVMsR0FBRyxJQUFJLENBQUMsWUFBWSxHQUFHLElBQUksQ0FBQyxZQUFZLENBQUM7SUFDekQsQ0FBQztJQUZlLHNCQUFjLGlCQUU3QjtBQUNILENBQUMsRUFUUyxPQUFPLEtBQVAsT0FBTyxRQVNoQiIsImZpbGUiOiJwYWNrYWdlc19jb25zb2xlX2xpYl9pbmRleF9qcy43NmFmYmE3ZWE2OGM1MjU5MzA2ZC5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVNlc3Npb25Db250ZXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgQ29kZUNlbGwgfSBmcm9tICdAanVweXRlcmxhYi9jZWxscyc7XG5pbXBvcnQgKiBhcyBuYmZvcm1hdCBmcm9tICdAanVweXRlcmxhYi9uYmZvcm1hdCc7XG5pbXBvcnQgeyBLZXJuZWxNZXNzYWdlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuXG5jb25zdCBGT1JFSUdOX0NFTExfQ0xBU1MgPSAnanAtQ29kZUNvbnNvbGUtZm9yZWlnbkNlbGwnO1xuXG4vKipcbiAqIEEgaGFuZGxlciBmb3IgY2FwdHVyaW5nIEFQSSBtZXNzYWdlcyBmcm9tIG90aGVyIHNlc3Npb25zIHRoYXQgc2hvdWxkIGJlXG4gKiByZW5kZXJlZCBpbiBhIGdpdmVuIHBhcmVudC5cbiAqL1xuZXhwb3J0IGNsYXNzIEZvcmVpZ25IYW5kbGVyIGltcGxlbWVudHMgSURpc3Bvc2FibGUge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IGZvcmVpZ24gbWVzc2FnZSBoYW5kbGVyLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogRm9yZWlnbkhhbmRsZXIuSU9wdGlvbnMpIHtcbiAgICB0aGlzLnNlc3Npb25Db250ZXh0ID0gb3B0aW9ucy5zZXNzaW9uQ29udGV4dDtcbiAgICB0aGlzLnNlc3Npb25Db250ZXh0LmlvcHViTWVzc2FnZS5jb25uZWN0KHRoaXMub25JT1B1Yk1lc3NhZ2UsIHRoaXMpO1xuICAgIHRoaXMuX3BhcmVudCA9IG9wdGlvbnMucGFyZW50O1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCB3aGV0aGVyIHRoZSBoYW5kbGVyIGlzIGFibGUgdG8gaW5qZWN0IGZvcmVpZ24gY2VsbHMgaW50byBhIGNvbnNvbGUuXG4gICAqL1xuICBnZXQgZW5hYmxlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fZW5hYmxlZDtcbiAgfVxuICBzZXQgZW5hYmxlZCh2YWx1ZTogYm9vbGVhbikge1xuICAgIHRoaXMuX2VuYWJsZWQgPSB2YWx1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY2xpZW50IHNlc3Npb24gdXNlZCBieSB0aGUgZm9yZWlnbiBoYW5kbGVyLlxuICAgKi9cbiAgcmVhZG9ubHkgc2Vzc2lvbkNvbnRleHQ6IElTZXNzaW9uQ29udGV4dDtcblxuICAvKipcbiAgICogVGhlIGZvcmVpZ24gaGFuZGxlcidzIHBhcmVudCByZWNlaXZlci5cbiAgICovXG4gIGdldCBwYXJlbnQoKTogRm9yZWlnbkhhbmRsZXIuSVJlY2VpdmVyIHtcbiAgICByZXR1cm4gdGhpcy5fcGFyZW50O1xuICB9XG5cbiAgLyoqXG4gICAqIFRlc3Qgd2hldGhlciB0aGUgaGFuZGxlciBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2UgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBoYW5kbGVyLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlciBJT1B1YiBtZXNzYWdlcy5cbiAgICpcbiAgICogQHJldHVybnMgYHRydWVgIGlmIHRoZSBtZXNzYWdlIHJlc3VsdGVkIGluIGEgbmV3IGNlbGwgaW5qZWN0aW9uIG9yIGFcbiAgICogcHJldmlvdXNseSBpbmplY3RlZCBjZWxsIGJlaW5nIHVwZGF0ZWQgYW5kIGBmYWxzZWAgZm9yIGFsbCBvdGhlciBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvbklPUHViTWVzc2FnZShcbiAgICBzZW5kZXI6IElTZXNzaW9uQ29udGV4dCxcbiAgICBtc2c6IEtlcm5lbE1lc3NhZ2UuSUlPUHViTWVzc2FnZVxuICApOiBib29sZWFuIHtcbiAgICAvLyBPbmx5IHByb2Nlc3MgbWVzc2FnZXMgaWYgZm9yZWlnbiBjZWxsIGluamVjdGlvbiBpcyBlbmFibGVkLlxuICAgIGlmICghdGhpcy5fZW5hYmxlZCkge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgICBjb25zdCBrZXJuZWwgPSB0aGlzLnNlc3Npb25Db250ZXh0LnNlc3Npb24/Lmtlcm5lbDtcbiAgICBpZiAoIWtlcm5lbCkge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cblxuICAgIC8vIENoZWNrIHdoZXRoZXIgdGhpcyBtZXNzYWdlIGNhbWUgZnJvbSBhbiBleHRlcm5hbCBzZXNzaW9uLlxuICAgIGNvbnN0IHBhcmVudCA9IHRoaXMuX3BhcmVudDtcbiAgICBjb25zdCBzZXNzaW9uID0gKG1zZy5wYXJlbnRfaGVhZGVyIGFzIEtlcm5lbE1lc3NhZ2UuSUhlYWRlcikuc2Vzc2lvbjtcbiAgICBpZiAoc2Vzc2lvbiA9PT0ga2VybmVsLmNsaWVudElkKSB7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuICAgIGNvbnN0IG1zZ1R5cGUgPSBtc2cuaGVhZGVyLm1zZ190eXBlO1xuICAgIGNvbnN0IHBhcmVudEhlYWRlciA9IG1zZy5wYXJlbnRfaGVhZGVyIGFzIEtlcm5lbE1lc3NhZ2UuSUhlYWRlcjtcbiAgICBjb25zdCBwYXJlbnRNc2dJZCA9IHBhcmVudEhlYWRlci5tc2dfaWQgYXMgc3RyaW5nO1xuICAgIGxldCBjZWxsOiBDb2RlQ2VsbCB8IHVuZGVmaW5lZDtcbiAgICBzd2l0Y2ggKG1zZ1R5cGUpIHtcbiAgICAgIGNhc2UgJ2V4ZWN1dGVfaW5wdXQnOiB7XG4gICAgICAgIGNvbnN0IGlucHV0TXNnID0gbXNnIGFzIEtlcm5lbE1lc3NhZ2UuSUV4ZWN1dGVJbnB1dE1zZztcbiAgICAgICAgY2VsbCA9IHRoaXMuX25ld0NlbGwocGFyZW50TXNnSWQpO1xuICAgICAgICBjb25zdCBtb2RlbCA9IGNlbGwubW9kZWw7XG4gICAgICAgIG1vZGVsLmV4ZWN1dGlvbkNvdW50ID0gaW5wdXRNc2cuY29udGVudC5leGVjdXRpb25fY291bnQ7XG4gICAgICAgIG1vZGVsLnZhbHVlLnRleHQgPSBpbnB1dE1zZy5jb250ZW50LmNvZGU7XG4gICAgICAgIG1vZGVsLnRydXN0ZWQgPSB0cnVlO1xuICAgICAgICBwYXJlbnQudXBkYXRlKCk7XG4gICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgfVxuICAgICAgY2FzZSAnZXhlY3V0ZV9yZXN1bHQnOlxuICAgICAgY2FzZSAnZGlzcGxheV9kYXRhJzpcbiAgICAgIGNhc2UgJ3N0cmVhbSc6XG4gICAgICBjYXNlICdlcnJvcic6IHtcbiAgICAgICAgY2VsbCA9IHRoaXMuX3BhcmVudC5nZXRDZWxsKHBhcmVudE1zZ0lkKTtcbiAgICAgICAgaWYgKCFjZWxsKSB7XG4gICAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IG91dHB1dDogbmJmb3JtYXQuSU91dHB1dCA9IHtcbiAgICAgICAgICAuLi5tc2cuY29udGVudCxcbiAgICAgICAgICBvdXRwdXRfdHlwZTogbXNnVHlwZVxuICAgICAgICB9O1xuICAgICAgICBjZWxsLm1vZGVsLm91dHB1dHMuYWRkKG91dHB1dCk7XG4gICAgICAgIHBhcmVudC51cGRhdGUoKTtcbiAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICB9XG4gICAgICBjYXNlICdjbGVhcl9vdXRwdXQnOiB7XG4gICAgICAgIGNvbnN0IHdhaXQgPSAobXNnIGFzIEtlcm5lbE1lc3NhZ2UuSUNsZWFyT3V0cHV0TXNnKS5jb250ZW50LndhaXQ7XG4gICAgICAgIGNlbGwgPSB0aGlzLl9wYXJlbnQuZ2V0Q2VsbChwYXJlbnRNc2dJZCk7XG4gICAgICAgIGlmIChjZWxsKSB7XG4gICAgICAgICAgY2VsbC5tb2RlbC5vdXRwdXRzLmNsZWFyKHdhaXQpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgfVxuICAgICAgZGVmYXVsdDpcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgY29kZSBjZWxsIGZvciBhbiBpbnB1dCBvcmlnaW5hdGVkIGZyb20gYSBmb3JlaWduIHNlc3Npb24uXG4gICAqL1xuICBwcml2YXRlIF9uZXdDZWxsKHBhcmVudE1zZ0lkOiBzdHJpbmcpOiBDb2RlQ2VsbCB7XG4gICAgY29uc3QgY2VsbCA9IHRoaXMucGFyZW50LmNyZWF0ZUNvZGVDZWxsKCk7XG4gICAgY2VsbC5hZGRDbGFzcyhGT1JFSUdOX0NFTExfQ0xBU1MpO1xuICAgIHRoaXMuX3BhcmVudC5hZGRDZWxsKGNlbGwsIHBhcmVudE1zZ0lkKTtcbiAgICByZXR1cm4gY2VsbDtcbiAgfVxuXG4gIHByaXZhdGUgX2VuYWJsZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfcGFyZW50OiBGb3JlaWduSGFuZGxlci5JUmVjZWl2ZXI7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYEZvcmVpZ25IYW5kbGVyYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIEZvcmVpZ25IYW5kbGVyIHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgZm9yZWlnbiBoYW5kbGVyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGNsaWVudCBzZXNzaW9uIHVzZWQgYnkgdGhlIGZvcmVpZ24gaGFuZGxlci5cbiAgICAgKi9cbiAgICBzZXNzaW9uQ29udGV4dDogSVNlc3Npb25Db250ZXh0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHBhcmVudCBpbnRvIHdoaWNoIHRoZSBoYW5kbGVyIHdpbGwgaW5qZWN0IGNvZGUgY2VsbHMuXG4gICAgICovXG4gICAgcGFyZW50OiBJUmVjZWl2ZXI7XG4gIH1cblxuICAvKipcbiAgICogQSByZWNlaXZlciBvZiBuZXdseSBjcmVhdGVkIGZvcmVpZ24gY2VsbHMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElSZWNlaXZlciB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgY2VsbC5cbiAgICAgKi9cbiAgICBjcmVhdGVDb2RlQ2VsbCgpOiBDb2RlQ2VsbDtcblxuICAgIC8qKlxuICAgICAqIEFkZCBhIG5ld2x5IGNyZWF0ZWQgY2VsbC5cbiAgICAgKi9cbiAgICBhZGRDZWxsKGNlbGw6IENvZGVDZWxsLCBtc2dJZDogc3RyaW5nKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIFRyaWdnZXIgYSByZW5kZXJpbmcgdXBkYXRlIG9uIHRoZSByZWNlaXZlci5cbiAgICAgKi9cbiAgICB1cGRhdGUoKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIEdldCBhIGNlbGwgYXNzb2NpYXRlZCB3aXRoIGEgbWVzc2FnZSBpZC5cbiAgICAgKi9cbiAgICBnZXRDZWxsKG1zZ0lkOiBzdHJpbmcpOiBDb2RlQ2VsbCB8IHVuZGVmaW5lZDtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJU2Vzc2lvbkNvbnRleHQgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQgeyBLZXJuZWxNZXNzYWdlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuXG4vKipcbiAqIFRoZSBkZWZpbml0aW9uIG9mIGEgY29uc29sZSBoaXN0b3J5IG1hbmFnZXIgb2JqZWN0LlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElDb25zb2xlSGlzdG9yeSBleHRlbmRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIFRoZSBzZXNzaW9uIGNvbnRleHQgdXNlZCBieSB0aGUgZm9yZWlnbiBoYW5kbGVyLlxuICAgKi9cbiAgcmVhZG9ubHkgc2Vzc2lvbkNvbnRleHQ6IElTZXNzaW9uQ29udGV4dDtcblxuICAvKipcbiAgICogVGhlIGN1cnJlbnQgZWRpdG9yIHVzZWQgYnkgdGhlIGhpc3Rvcnkgd2lkZ2V0LlxuICAgKi9cbiAgZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsO1xuXG4gIC8qKlxuICAgKiBUaGUgcGxhY2Vob2xkZXIgdGV4dCB0aGF0IGEgaGlzdG9yeSBzZXNzaW9uIGJlZ2FuIHdpdGguXG4gICAqL1xuICByZWFkb25seSBwbGFjZWhvbGRlcjogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHByZXZpb3VzIGl0ZW0gaW4gdGhlIGNvbnNvbGUgaGlzdG9yeS5cbiAgICpcbiAgICogQHBhcmFtIHBsYWNlaG9sZGVyIC0gVGhlIHBsYWNlaG9sZGVyIHN0cmluZyB0aGF0IGdldHMgdGVtcG9yYXJpbHkgYWRkZWRcbiAgICogdG8gdGhlIGhpc3Rvcnkgb25seSBmb3IgdGhlIGR1cmF0aW9uIG9mIG9uZSBoaXN0b3J5IHNlc3Npb24uIElmIG11bHRpcGxlXG4gICAqIHBsYWNlaG9sZGVycyBhcmUgc2VudCB3aXRoaW4gYSBzZXNzaW9uLCBvbmx5IHRoZSBmaXJzdCBvbmUgaXMgYWNjZXB0ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgUHJvbWlzZSBmb3IgY29uc29sZSBjb21tYW5kIHRleHQgb3IgYHVuZGVmaW5lZGAgaWYgdW5hdmFpbGFibGUuXG4gICAqL1xuICBiYWNrKHBsYWNlaG9sZGVyOiBzdHJpbmcpOiBQcm9taXNlPHN0cmluZz47XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgbmV4dCBpdGVtIGluIHRoZSBjb25zb2xlIGhpc3RvcnkuXG4gICAqXG4gICAqIEBwYXJhbSBwbGFjZWhvbGRlciAtIFRoZSBwbGFjZWhvbGRlciBzdHJpbmcgdGhhdCBnZXRzIHRlbXBvcmFyaWx5IGFkZGVkXG4gICAqIHRvIHRoZSBoaXN0b3J5IG9ubHkgZm9yIHRoZSBkdXJhdGlvbiBvZiBvbmUgaGlzdG9yeSBzZXNzaW9uLiBJZiBtdWx0aXBsZVxuICAgKiBwbGFjZWhvbGRlcnMgYXJlIHNlbnQgd2l0aGluIGEgc2Vzc2lvbiwgb25seSB0aGUgZmlyc3Qgb25lIGlzIGFjY2VwdGVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIFByb21pc2UgZm9yIGNvbnNvbGUgY29tbWFuZCB0ZXh0IG9yIGB1bmRlZmluZWRgIGlmIHVuYXZhaWxhYmxlLlxuICAgKi9cbiAgZm9yd2FyZChwbGFjZWhvbGRlcjogc3RyaW5nKTogUHJvbWlzZTxzdHJpbmc+O1xuXG4gIC8qKlxuICAgKiBBZGQgYSBuZXcgaXRlbSB0byB0aGUgYm90dG9tIG9mIGhpc3RvcnkuXG4gICAqXG4gICAqIEBwYXJhbSBpdGVtIFRoZSBpdGVtIGJlaW5nIGFkZGVkIHRvIHRoZSBib3R0b20gb2YgaGlzdG9yeS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBJZiB0aGUgaXRlbSBiZWluZyBhZGRlZCBpcyB1bmRlZmluZWQgb3IgZW1wdHksIGl0IGlzIGlnbm9yZWQuIElmIHRoZSBpdGVtXG4gICAqIGJlaW5nIGFkZGVkIGlzIHRoZSBzYW1lIGFzIHRoZSBsYXN0IGl0ZW0gaW4gaGlzdG9yeSwgaXQgaXMgaWdub3JlZCBhcyB3ZWxsXG4gICAqIHNvIHRoYXQgdGhlIGNvbnNvbGUncyBoaXN0b3J5IHdpbGwgY29uc2lzdCBvZiBubyBjb250aWd1b3VzIHJlcGV0aXRpb25zLlxuICAgKi9cbiAgcHVzaChpdGVtOiBzdHJpbmcpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBSZXNldCB0aGUgaGlzdG9yeSBuYXZpZ2F0aW9uIHN0YXRlLCBpLmUuLCBzdGFydCBhIG5ldyBoaXN0b3J5IHNlc3Npb24uXG4gICAqL1xuICByZXNldCgpOiB2b2lkO1xufVxuXG4vKipcbiAqIEEgY29uc29sZSBoaXN0b3J5IG1hbmFnZXIgb2JqZWN0LlxuICovXG5leHBvcnQgY2xhc3MgQ29uc29sZUhpc3RvcnkgaW1wbGVtZW50cyBJQ29uc29sZUhpc3Rvcnkge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IGNvbnNvbGUgaGlzdG9yeSBvYmplY3QuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBDb25zb2xlSGlzdG9yeS5JT3B0aW9ucykge1xuICAgIHRoaXMuc2Vzc2lvbkNvbnRleHQgPSBvcHRpb25zLnNlc3Npb25Db250ZXh0O1xuICAgIHZvaWQgdGhpcy5faGFuZGxlS2VybmVsKCk7XG4gICAgdGhpcy5zZXNzaW9uQ29udGV4dC5rZXJuZWxDaGFuZ2VkLmNvbm5lY3QodGhpcy5faGFuZGxlS2VybmVsLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY2xpZW50IHNlc3Npb24gdXNlZCBieSB0aGUgZm9yZWlnbiBoYW5kbGVyLlxuICAgKi9cbiAgcmVhZG9ubHkgc2Vzc2lvbkNvbnRleHQ6IElTZXNzaW9uQ29udGV4dDtcblxuICAvKipcbiAgICogVGhlIGN1cnJlbnQgZWRpdG9yIHVzZWQgYnkgdGhlIGhpc3RvcnkgbWFuYWdlci5cbiAgICovXG4gIGdldCBlZGl0b3IoKTogQ29kZUVkaXRvci5JRWRpdG9yIHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuX2VkaXRvcjtcbiAgfVxuICBzZXQgZWRpdG9yKHZhbHVlOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsKSB7XG4gICAgaWYgKHRoaXMuX2VkaXRvciA9PT0gdmFsdWUpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCBwcmV2ID0gdGhpcy5fZWRpdG9yO1xuICAgIGlmIChwcmV2KSB7XG4gICAgICBwcmV2LmVkZ2VSZXF1ZXN0ZWQuZGlzY29ubmVjdCh0aGlzLm9uRWRnZVJlcXVlc3QsIHRoaXMpO1xuICAgICAgcHJldi5tb2RlbC52YWx1ZS5jaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy5vblRleHRDaGFuZ2UsIHRoaXMpO1xuICAgIH1cblxuICAgIHRoaXMuX2VkaXRvciA9IHZhbHVlO1xuXG4gICAgaWYgKHZhbHVlKSB7XG4gICAgICB2YWx1ZS5lZGdlUmVxdWVzdGVkLmNvbm5lY3QodGhpcy5vbkVkZ2VSZXF1ZXN0LCB0aGlzKTtcbiAgICAgIHZhbHVlLm1vZGVsLnZhbHVlLmNoYW5nZWQuY29ubmVjdCh0aGlzLm9uVGV4dENoYW5nZSwgdGhpcyk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBwbGFjZWhvbGRlciB0ZXh0IHRoYXQgYSBoaXN0b3J5IHNlc3Npb24gYmVnYW4gd2l0aC5cbiAgICovXG4gIGdldCBwbGFjZWhvbGRlcigpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLl9wbGFjZWhvbGRlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgd2hldGhlciB0aGUgY29uc29sZSBoaXN0b3J5IG1hbmFnZXIgaXMgZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgY29uc29sZSBoaXN0b3J5IG1hbmFnZXIuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuICAgIHRoaXMuX2hpc3RvcnkubGVuZ3RoID0gMDtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgcHJldmlvdXMgaXRlbSBpbiB0aGUgY29uc29sZSBoaXN0b3J5LlxuICAgKlxuICAgKiBAcGFyYW0gcGxhY2Vob2xkZXIgLSBUaGUgcGxhY2Vob2xkZXIgc3RyaW5nIHRoYXQgZ2V0cyB0ZW1wb3JhcmlseSBhZGRlZFxuICAgKiB0byB0aGUgaGlzdG9yeSBvbmx5IGZvciB0aGUgZHVyYXRpb24gb2Ygb25lIGhpc3Rvcnkgc2Vzc2lvbi4gSWYgbXVsdGlwbGVcbiAgICogcGxhY2Vob2xkZXJzIGFyZSBzZW50IHdpdGhpbiBhIHNlc3Npb24sIG9ubHkgdGhlIGZpcnN0IG9uZSBpcyBhY2NlcHRlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBQcm9taXNlIGZvciBjb25zb2xlIGNvbW1hbmQgdGV4dCBvciBgdW5kZWZpbmVkYCBpZiB1bmF2YWlsYWJsZS5cbiAgICovXG4gIGJhY2socGxhY2Vob2xkZXI6IHN0cmluZyk6IFByb21pc2U8c3RyaW5nPiB7XG4gICAgaWYgKCF0aGlzLl9oYXNTZXNzaW9uKSB7XG4gICAgICB0aGlzLl9oYXNTZXNzaW9uID0gdHJ1ZTtcbiAgICAgIHRoaXMuX3BsYWNlaG9sZGVyID0gcGxhY2Vob2xkZXI7XG4gICAgICAvLyBGaWx0ZXIgdGhlIGhpc3Rvcnkgd2l0aCB0aGUgcGxhY2Vob2xkZXIgc3RyaW5nLlxuICAgICAgdGhpcy5zZXRGaWx0ZXIocGxhY2Vob2xkZXIpO1xuICAgICAgdGhpcy5fY3Vyc29yID0gdGhpcy5fZmlsdGVyZWQubGVuZ3RoIC0gMTtcbiAgICB9XG5cbiAgICAtLXRoaXMuX2N1cnNvcjtcbiAgICB0aGlzLl9jdXJzb3IgPSBNYXRoLm1heCgwLCB0aGlzLl9jdXJzb3IpO1xuICAgIGNvbnN0IGNvbnRlbnQgPSB0aGlzLl9maWx0ZXJlZFt0aGlzLl9jdXJzb3JdO1xuICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUoY29udGVudCk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBuZXh0IGl0ZW0gaW4gdGhlIGNvbnNvbGUgaGlzdG9yeS5cbiAgICpcbiAgICogQHBhcmFtIHBsYWNlaG9sZGVyIC0gVGhlIHBsYWNlaG9sZGVyIHN0cmluZyB0aGF0IGdldHMgdGVtcG9yYXJpbHkgYWRkZWRcbiAgICogdG8gdGhlIGhpc3Rvcnkgb25seSBmb3IgdGhlIGR1cmF0aW9uIG9mIG9uZSBoaXN0b3J5IHNlc3Npb24uIElmIG11bHRpcGxlXG4gICAqIHBsYWNlaG9sZGVycyBhcmUgc2VudCB3aXRoaW4gYSBzZXNzaW9uLCBvbmx5IHRoZSBmaXJzdCBvbmUgaXMgYWNjZXB0ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgUHJvbWlzZSBmb3IgY29uc29sZSBjb21tYW5kIHRleHQgb3IgYHVuZGVmaW5lZGAgaWYgdW5hdmFpbGFibGUuXG4gICAqL1xuICBmb3J3YXJkKHBsYWNlaG9sZGVyOiBzdHJpbmcpOiBQcm9taXNlPHN0cmluZz4ge1xuICAgIGlmICghdGhpcy5faGFzU2Vzc2lvbikge1xuICAgICAgdGhpcy5faGFzU2Vzc2lvbiA9IHRydWU7XG4gICAgICB0aGlzLl9wbGFjZWhvbGRlciA9IHBsYWNlaG9sZGVyO1xuICAgICAgLy8gRmlsdGVyIHRoZSBoaXN0b3J5IHdpdGggdGhlIHBsYWNlaG9sZGVyIHN0cmluZy5cbiAgICAgIHRoaXMuc2V0RmlsdGVyKHBsYWNlaG9sZGVyKTtcbiAgICAgIHRoaXMuX2N1cnNvciA9IHRoaXMuX2ZpbHRlcmVkLmxlbmd0aDtcbiAgICB9XG5cbiAgICArK3RoaXMuX2N1cnNvcjtcbiAgICB0aGlzLl9jdXJzb3IgPSBNYXRoLm1pbih0aGlzLl9maWx0ZXJlZC5sZW5ndGggLSAxLCB0aGlzLl9jdXJzb3IpO1xuICAgIGNvbnN0IGNvbnRlbnQgPSB0aGlzLl9maWx0ZXJlZFt0aGlzLl9jdXJzb3JdO1xuICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUoY29udGVudCk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgbmV3IGl0ZW0gdG8gdGhlIGJvdHRvbSBvZiBoaXN0b3J5LlxuICAgKlxuICAgKiBAcGFyYW0gaXRlbSBUaGUgaXRlbSBiZWluZyBhZGRlZCB0byB0aGUgYm90dG9tIG9mIGhpc3RvcnkuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogSWYgdGhlIGl0ZW0gYmVpbmcgYWRkZWQgaXMgdW5kZWZpbmVkIG9yIGVtcHR5LCBpdCBpcyBpZ25vcmVkLiBJZiB0aGUgaXRlbVxuICAgKiBiZWluZyBhZGRlZCBpcyB0aGUgc2FtZSBhcyB0aGUgbGFzdCBpdGVtIGluIGhpc3RvcnksIGl0IGlzIGlnbm9yZWQgYXMgd2VsbFxuICAgKiBzbyB0aGF0IHRoZSBjb25zb2xlJ3MgaGlzdG9yeSB3aWxsIGNvbnNpc3Qgb2Ygbm8gY29udGlndW91cyByZXBldGl0aW9ucy5cbiAgICovXG4gIHB1c2goaXRlbTogc3RyaW5nKTogdm9pZCB7XG4gICAgaWYgKGl0ZW0gJiYgaXRlbSAhPT0gdGhpcy5faGlzdG9yeVt0aGlzLl9oaXN0b3J5Lmxlbmd0aCAtIDFdKSB7XG4gICAgICB0aGlzLl9oaXN0b3J5LnB1c2goaXRlbSk7XG4gICAgfVxuICAgIHRoaXMucmVzZXQoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXNldCB0aGUgaGlzdG9yeSBuYXZpZ2F0aW9uIHN0YXRlLCBpLmUuLCBzdGFydCBhIG5ldyBoaXN0b3J5IHNlc3Npb24uXG4gICAqL1xuICByZXNldCgpOiB2b2lkIHtcbiAgICB0aGlzLl9jdXJzb3IgPSB0aGlzLl9oaXN0b3J5Lmxlbmd0aDtcbiAgICB0aGlzLl9oYXNTZXNzaW9uID0gZmFsc2U7XG4gICAgdGhpcy5fcGxhY2Vob2xkZXIgPSAnJztcbiAgfVxuXG4gIC8qKlxuICAgKiBQb3B1bGF0ZSB0aGUgaGlzdG9yeSBjb2xsZWN0aW9uIG9uIGhpc3RvcnkgcmVwbHkgZnJvbSBhIGtlcm5lbC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlIFRoZSBrZXJuZWwgbWVzc2FnZSBoaXN0b3J5IHJlcGx5LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIEhpc3RvcnkgZW50cmllcyBoYXZlIHRoZSBzaGFwZTpcbiAgICogW3Nlc3Npb246IG51bWJlciwgbGluZTogbnVtYmVyLCBpbnB1dDogc3RyaW5nXVxuICAgKiBDb250aWd1b3VzIGR1cGxpY2F0ZXMgYXJlIHN0cmlwcGVkIG91dCBvZiB0aGUgQVBJIHJlc3BvbnNlLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uSGlzdG9yeSh2YWx1ZTogS2VybmVsTWVzc2FnZS5JSGlzdG9yeVJlcGx5TXNnKTogdm9pZCB7XG4gICAgdGhpcy5faGlzdG9yeS5sZW5ndGggPSAwO1xuICAgIGxldCBsYXN0ID0gJyc7XG4gICAgbGV0IGN1cnJlbnQgPSAnJztcbiAgICBpZiAodmFsdWUuY29udGVudC5zdGF0dXMgPT09ICdvaycpIHtcbiAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgdmFsdWUuY29udGVudC5oaXN0b3J5Lmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIGN1cnJlbnQgPSAodmFsdWUuY29udGVudC5oaXN0b3J5W2ldIGFzIHN0cmluZ1tdKVsyXTtcbiAgICAgICAgaWYgKGN1cnJlbnQgIT09IGxhc3QpIHtcbiAgICAgICAgICB0aGlzLl9oaXN0b3J5LnB1c2goKGxhc3QgPSBjdXJyZW50KSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gICAgLy8gUmVzZXQgdGhlIGhpc3RvcnkgbmF2aWdhdGlvbiBjdXJzb3IgYmFjayB0byB0aGUgYm90dG9tLlxuICAgIHRoaXMuX2N1cnNvciA9IHRoaXMuX2hpc3RvcnkubGVuZ3RoO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIHRleHQgY2hhbmdlIHNpZ25hbCBmcm9tIHRoZSBlZGl0b3IuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25UZXh0Q2hhbmdlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9zZXRCeUhpc3RvcnkpIHtcbiAgICAgIHRoaXMuX3NldEJ5SGlzdG9yeSA9IGZhbHNlO1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLnJlc2V0KCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGFuIGVkZ2UgcmVxdWVzdGVkIHNpZ25hbC5cbiAgICovXG4gIHByb3RlY3RlZCBvbkVkZ2VSZXF1ZXN0KFxuICAgIGVkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yLFxuICAgIGxvY2F0aW9uOiBDb2RlRWRpdG9yLkVkZ2VMb2NhdGlvblxuICApOiB2b2lkIHtcbiAgICBjb25zdCBtb2RlbCA9IGVkaXRvci5tb2RlbDtcbiAgICBjb25zdCBzb3VyY2UgPSBtb2RlbC52YWx1ZS50ZXh0O1xuXG4gICAgaWYgKGxvY2F0aW9uID09PSAndG9wJyB8fCBsb2NhdGlvbiA9PT0gJ3RvcExpbmUnKSB7XG4gICAgICB2b2lkIHRoaXMuYmFjayhzb3VyY2UpLnRoZW4odmFsdWUgPT4ge1xuICAgICAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkIHx8ICF2YWx1ZSkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBpZiAobW9kZWwudmFsdWUudGV4dCA9PT0gdmFsdWUpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5fc2V0QnlIaXN0b3J5ID0gdHJ1ZTtcbiAgICAgICAgbW9kZWwudmFsdWUudGV4dCA9IHZhbHVlO1xuICAgICAgICBsZXQgY29sdW1uUG9zID0gMDtcbiAgICAgICAgY29sdW1uUG9zID0gdmFsdWUuaW5kZXhPZignXFxuJyk7XG4gICAgICAgIGlmIChjb2x1bW5Qb3MgPCAwKSB7XG4gICAgICAgICAgY29sdW1uUG9zID0gdmFsdWUubGVuZ3RoO1xuICAgICAgICB9XG4gICAgICAgIGVkaXRvci5zZXRDdXJzb3JQb3NpdGlvbih7IGxpbmU6IDAsIGNvbHVtbjogY29sdW1uUG9zIH0pO1xuICAgICAgfSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHZvaWQgdGhpcy5mb3J3YXJkKHNvdXJjZSkudGhlbih2YWx1ZSA9PiB7XG4gICAgICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgdGV4dCA9IHZhbHVlIHx8IHRoaXMucGxhY2Vob2xkZXI7XG4gICAgICAgIGlmIChtb2RlbC52YWx1ZS50ZXh0ID09PSB0ZXh0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuX3NldEJ5SGlzdG9yeSA9IHRydWU7XG4gICAgICAgIG1vZGVsLnZhbHVlLnRleHQgPSB0ZXh0O1xuICAgICAgICBjb25zdCBwb3MgPSBlZGl0b3IuZ2V0UG9zaXRpb25BdCh0ZXh0Lmxlbmd0aCk7XG4gICAgICAgIGlmIChwb3MpIHtcbiAgICAgICAgICBlZGl0b3Iuc2V0Q3Vyc29yUG9zaXRpb24ocG9zKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgY3VycmVudCBrZXJuZWwgY2hhbmdpbmcuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9oYW5kbGVLZXJuZWwoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3Qga2VybmVsID0gdGhpcy5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw7XG4gICAgaWYgKCFrZXJuZWwpIHtcbiAgICAgIHRoaXMuX2hpc3RvcnkubGVuZ3RoID0gMDtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICByZXR1cm4ga2VybmVsLnJlcXVlc3RIaXN0b3J5KFByaXZhdGUuaW5pdGlhbFJlcXVlc3QpLnRoZW4odiA9PiB7XG4gICAgICB0aGlzLm9uSGlzdG9yeSh2KTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIGZpbHRlciBkYXRhLlxuICAgKlxuICAgKiBAcGFyYW0gZmlsdGVyU3RyIC0gVGhlIHN0cmluZyB0byB1c2Ugd2hlbiBmaWx0ZXJpbmcgdGhlIGRhdGEuXG4gICAqL1xuICBwcm90ZWN0ZWQgc2V0RmlsdGVyKGZpbHRlclN0cjogc3RyaW5nID0gJycpOiB2b2lkIHtcbiAgICAvLyBBcHBseSB0aGUgbmV3IGZpbHRlciBhbmQgcmVtb3ZlIGNvbnRpZ3VvdXMgZHVwbGljYXRlcy5cbiAgICB0aGlzLl9maWx0ZXJlZC5sZW5ndGggPSAwO1xuXG4gICAgbGV0IGxhc3QgPSAnJztcbiAgICBsZXQgY3VycmVudCA9ICcnO1xuXG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCB0aGlzLl9oaXN0b3J5Lmxlbmd0aDsgaSsrKSB7XG4gICAgICBjdXJyZW50ID0gdGhpcy5faGlzdG9yeVtpXTtcbiAgICAgIGlmIChcbiAgICAgICAgY3VycmVudCAhPT0gbGFzdCAmJlxuICAgICAgICBmaWx0ZXJTdHIgPT09IGN1cnJlbnQuc2xpY2UoMCwgZmlsdGVyU3RyLmxlbmd0aClcbiAgICAgICkge1xuICAgICAgICB0aGlzLl9maWx0ZXJlZC5wdXNoKChsYXN0ID0gY3VycmVudCkpO1xuICAgICAgfVxuICAgIH1cblxuICAgIHRoaXMuX2ZpbHRlcmVkLnB1c2goZmlsdGVyU3RyKTtcbiAgfVxuXG4gIHByaXZhdGUgX2N1cnNvciA9IDA7XG4gIHByaXZhdGUgX2hhc1Nlc3Npb24gPSBmYWxzZTtcbiAgcHJpdmF0ZSBfaGlzdG9yeTogc3RyaW5nW10gPSBbXTtcbiAgcHJpdmF0ZSBfcGxhY2Vob2xkZXI6IHN0cmluZyA9ICcnO1xuICBwcml2YXRlIF9zZXRCeUhpc3RvcnkgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xuICBwcml2YXRlIF9lZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvciB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9maWx0ZXJlZDogc3RyaW5nW10gPSBbXTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgQ29uc29sZUhpc3Rvcnkgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDb25zb2xlSGlzdG9yeSB7XG4gIC8qKlxuICAgKiBUaGUgaW5pdGlhbGl6YXRpb24gb3B0aW9ucyBmb3IgYSBjb25zb2xlIGhpc3Rvcnkgb2JqZWN0LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGNsaWVudCBzZXNzaW9uIHVzZWQgYnkgdGhlIGZvcmVpZ24gaGFuZGxlci5cbiAgICAgKi9cbiAgICBzZXNzaW9uQ29udGV4dDogSVNlc3Npb25Db250ZXh0O1xuICB9XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICBleHBvcnQgY29uc3QgaW5pdGlhbFJlcXVlc3Q6IEtlcm5lbE1lc3NhZ2UuSUhpc3RvcnlSZXF1ZXN0TXNnWydjb250ZW50J10gPSB7XG4gICAgb3V0cHV0OiBmYWxzZSxcbiAgICByYXc6IHRydWUsXG4gICAgaGlzdF9hY2Nlc3NfdHlwZTogJ3RhaWwnLFxuICAgIG46IDUwMFxuICB9O1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY29uc29sZVxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vZm9yZWlnbic7XG5leHBvcnQgKiBmcm9tICcuL2hpc3RvcnknO1xuZXhwb3J0ICogZnJvbSAnLi9wYW5lbCc7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG5leHBvcnQgKiBmcm9tICcuL3dpZGdldCc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7XG4gIElTZXNzaW9uQ29udGV4dCxcbiAgTWFpbkFyZWFXaWRnZXQsXG4gIFNlc3Npb25Db250ZXh0LFxuICBzZXNzaW9uQ29udGV4dERpYWxvZ3Ncbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSUVkaXRvck1pbWVUeXBlU2VydmljZSB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0IHsgUGF0aEV4dCwgVGltZSwgVVJMRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIFJlbmRlck1pbWVSZWdpc3RyeVxufSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IFNlcnZpY2VNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgY29uc29sZUljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFRva2VuLCBVVUlEIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IFBhbmVsIH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IENvZGVDb25zb2xlIH0gZnJvbSAnLi93aWRnZXQnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGNvbnNvbGUgcGFuZWxzLlxuICovXG5jb25zdCBQQU5FTF9DTEFTUyA9ICdqcC1Db25zb2xlUGFuZWwnO1xuXG4vKipcbiAqIEEgcGFuZWwgd2hpY2ggY29udGFpbnMgYSBjb25zb2xlIGFuZCB0aGUgYWJpbGl0eSB0byBhZGQgb3RoZXIgY2hpbGRyZW4uXG4gKi9cbmV4cG9ydCBjbGFzcyBDb25zb2xlUGFuZWwgZXh0ZW5kcyBNYWluQXJlYVdpZGdldDxQYW5lbD4ge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgY29uc29sZSBwYW5lbC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IENvbnNvbGVQYW5lbC5JT3B0aW9ucykge1xuICAgIHN1cGVyKHsgY29udGVudDogbmV3IFBhbmVsKCkgfSk7XG4gICAgdGhpcy5hZGRDbGFzcyhQQU5FTF9DTEFTUyk7XG4gICAgbGV0IHtcbiAgICAgIHJlbmRlcm1pbWUsXG4gICAgICBtaW1lVHlwZVNlcnZpY2UsXG4gICAgICBwYXRoLFxuICAgICAgYmFzZVBhdGgsXG4gICAgICBuYW1lLFxuICAgICAgbWFuYWdlcixcbiAgICAgIG1vZGVsRmFjdG9yeSxcbiAgICAgIHNlc3Npb25Db250ZXh0LFxuICAgICAgdHJhbnNsYXRvclxuICAgIH0gPSBvcHRpb25zO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgY29uc3QgY29udGVudEZhY3RvcnkgPSAodGhpcy5jb250ZW50RmFjdG9yeSA9XG4gICAgICBvcHRpb25zLmNvbnRlbnRGYWN0b3J5IHx8IENvbnNvbGVQYW5lbC5kZWZhdWx0Q29udGVudEZhY3RvcnkpO1xuICAgIGNvbnN0IGNvdW50ID0gUHJpdmF0ZS5jb3VudCsrO1xuICAgIGlmICghcGF0aCkge1xuICAgICAgcGF0aCA9IFVSTEV4dC5qb2luKGJhc2VQYXRoIHx8ICcnLCBgY29uc29sZS0ke2NvdW50fS0ke1VVSUQudXVpZDQoKX1gKTtcbiAgICB9XG5cbiAgICBzZXNzaW9uQ29udGV4dCA9IHRoaXMuX3Nlc3Npb25Db250ZXh0ID1cbiAgICAgIHNlc3Npb25Db250ZXh0IHx8XG4gICAgICBuZXcgU2Vzc2lvbkNvbnRleHQoe1xuICAgICAgICBzZXNzaW9uTWFuYWdlcjogbWFuYWdlci5zZXNzaW9ucyxcbiAgICAgICAgc3BlY3NNYW5hZ2VyOiBtYW5hZ2VyLmtlcm5lbHNwZWNzLFxuICAgICAgICBwYXRoLFxuICAgICAgICBuYW1lOiBuYW1lIHx8IHRyYW5zLl9fKCdDb25zb2xlICUxJywgY291bnQpLFxuICAgICAgICB0eXBlOiAnY29uc29sZScsXG4gICAgICAgIGtlcm5lbFByZWZlcmVuY2U6IG9wdGlvbnMua2VybmVsUHJlZmVyZW5jZSxcbiAgICAgICAgc2V0QnVzeTogb3B0aW9ucy5zZXRCdXN5XG4gICAgICB9KTtcblxuICAgIGNvbnN0IHJlc29sdmVyID0gbmV3IFJlbmRlck1pbWVSZWdpc3RyeS5VcmxSZXNvbHZlcih7XG4gICAgICBzZXNzaW9uOiBzZXNzaW9uQ29udGV4dCxcbiAgICAgIGNvbnRlbnRzOiBtYW5hZ2VyLmNvbnRlbnRzXG4gICAgfSk7XG4gICAgcmVuZGVybWltZSA9IHJlbmRlcm1pbWUuY2xvbmUoeyByZXNvbHZlciB9KTtcblxuICAgIHRoaXMuY29uc29sZSA9IGNvbnRlbnRGYWN0b3J5LmNyZWF0ZUNvbnNvbGUoe1xuICAgICAgcmVuZGVybWltZSxcbiAgICAgIHNlc3Npb25Db250ZXh0OiBzZXNzaW9uQ29udGV4dCxcbiAgICAgIG1pbWVUeXBlU2VydmljZSxcbiAgICAgIGNvbnRlbnRGYWN0b3J5LFxuICAgICAgbW9kZWxGYWN0b3J5XG4gICAgfSk7XG4gICAgdGhpcy5jb250ZW50LmFkZFdpZGdldCh0aGlzLmNvbnNvbGUpO1xuXG4gICAgdm9pZCBzZXNzaW9uQ29udGV4dC5pbml0aWFsaXplKCkudGhlbihhc3luYyB2YWx1ZSA9PiB7XG4gICAgICBpZiAodmFsdWUpIHtcbiAgICAgICAgYXdhaXQgc2Vzc2lvbkNvbnRleHREaWFsb2dzLnNlbGVjdEtlcm5lbChzZXNzaW9uQ29udGV4dCEpO1xuICAgICAgfVxuICAgICAgdGhpcy5fY29ubmVjdGVkID0gbmV3IERhdGUoKTtcbiAgICAgIHRoaXMuX3VwZGF0ZVRpdGxlUGFuZWwoKTtcbiAgICB9KTtcblxuICAgIHRoaXMuY29uc29sZS5leGVjdXRlZC5jb25uZWN0KHRoaXMuX29uRXhlY3V0ZWQsIHRoaXMpO1xuICAgIHRoaXMuX3VwZGF0ZVRpdGxlUGFuZWwoKTtcbiAgICBzZXNzaW9uQ29udGV4dC5rZXJuZWxDaGFuZ2VkLmNvbm5lY3QodGhpcy5fdXBkYXRlVGl0bGVQYW5lbCwgdGhpcyk7XG4gICAgc2Vzc2lvbkNvbnRleHQucHJvcGVydHlDaGFuZ2VkLmNvbm5lY3QodGhpcy5fdXBkYXRlVGl0bGVQYW5lbCwgdGhpcyk7XG5cbiAgICB0aGlzLnRpdGxlLmljb24gPSBjb25zb2xlSWNvbjtcbiAgICB0aGlzLnRpdGxlLmNsb3NhYmxlID0gdHJ1ZTtcbiAgICB0aGlzLmlkID0gYGNvbnNvbGUtJHtjb3VudH1gO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb250ZW50IGZhY3RvcnkgdXNlZCBieSB0aGUgY29uc29sZSBwYW5lbC5cbiAgICovXG4gIHJlYWRvbmx5IGNvbnRlbnRGYWN0b3J5OiBDb25zb2xlUGFuZWwuSUNvbnRlbnRGYWN0b3J5O1xuXG4gIC8qKlxuICAgKiBUaGUgY29uc29sZSB3aWRnZXQgdXNlZCBieSB0aGUgcGFuZWwuXG4gICAqL1xuICBjb25zb2xlOiBDb2RlQ29uc29sZTtcblxuICAvKipcbiAgICogVGhlIHNlc3Npb24gdXNlZCBieSB0aGUgcGFuZWwuXG4gICAqL1xuICBnZXQgc2Vzc2lvbkNvbnRleHQoKTogSVNlc3Npb25Db250ZXh0IHtcbiAgICByZXR1cm4gdGhpcy5fc2Vzc2lvbkNvbnRleHQ7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgdGhpcy5zZXNzaW9uQ29udGV4dC5kaXNwb3NlKCk7XG4gICAgdGhpcy5jb25zb2xlLmRpc3Bvc2UoKTtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAnYWN0aXZhdGUtcmVxdWVzdCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWN0aXZhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGNvbnN0IHByb21wdCA9IHRoaXMuY29uc29sZS5wcm9tcHRDZWxsO1xuICAgIGlmIChwcm9tcHQpIHtcbiAgICAgIHByb21wdC5lZGl0b3IuZm9jdXMoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAnY2xvc2UtcmVxdWVzdCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQ2xvc2VSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHN1cGVyLm9uQ2xvc2VSZXF1ZXN0KG1zZyk7XG4gICAgdGhpcy5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY29uc29sZSBleGVjdXRpb24uXG4gICAqL1xuICBwcml2YXRlIF9vbkV4ZWN1dGVkKHNlbmRlcjogQ29kZUNvbnNvbGUsIGFyZ3M6IERhdGUpIHtcbiAgICB0aGlzLl9leGVjdXRlZCA9IGFyZ3M7XG4gICAgdGhpcy5fdXBkYXRlVGl0bGVQYW5lbCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgY29uc29sZSBwYW5lbCB0aXRsZS5cbiAgICovXG4gIHByaXZhdGUgX3VwZGF0ZVRpdGxlUGFuZWwoKTogdm9pZCB7XG4gICAgUHJpdmF0ZS51cGRhdGVUaXRsZSh0aGlzLCB0aGlzLl9jb25uZWN0ZWQsIHRoaXMuX2V4ZWN1dGVkLCB0aGlzLnRyYW5zbGF0b3IpO1xuICB9XG5cbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX2V4ZWN1dGVkOiBEYXRlIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX2Nvbm5lY3RlZDogRGF0ZSB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9zZXNzaW9uQ29udGV4dDogSVNlc3Npb25Db250ZXh0O1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBDb25zb2xlUGFuZWwgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDb25zb2xlUGFuZWwge1xuICAvKipcbiAgICogVGhlIGluaXRpYWxpemF0aW9uIG9wdGlvbnMgZm9yIGEgY29uc29sZSBwYW5lbC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSByZW5kZXJtaW1lIGluc3RhbmNlIHVzZWQgYnkgdGhlIHBhbmVsLlxuICAgICAqL1xuICAgIHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnk7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29udGVudCBmYWN0b3J5IGZvciB0aGUgcGFuZWwuXG4gICAgICovXG4gICAgY29udGVudEZhY3Rvcnk6IElDb250ZW50RmFjdG9yeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBzZXJ2aWNlIG1hbmFnZXIgdXNlZCBieSB0aGUgcGFuZWwuXG4gICAgICovXG4gICAgbWFuYWdlcjogU2VydmljZU1hbmFnZXIuSU1hbmFnZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcGF0aCBvZiBhbiBleGlzdGluZyBjb25zb2xlLlxuICAgICAqL1xuICAgIHBhdGg/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYmFzZSBwYXRoIGZvciBhIG5ldyBjb25zb2xlLlxuICAgICAqL1xuICAgIGJhc2VQYXRoPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG5hbWUgb2YgdGhlIGNvbnNvbGUuXG4gICAgICovXG4gICAgbmFtZT86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEEga2VybmVsIHByZWZlcmVuY2UuXG4gICAgICovXG4gICAga2VybmVsUHJlZmVyZW5jZT86IElTZXNzaW9uQ29udGV4dC5JS2VybmVsUHJlZmVyZW5jZTtcblxuICAgIC8qKlxuICAgICAqIEFuIGV4aXN0aW5nIHNlc3Npb24gY29udGV4dCB0byB1c2UuXG4gICAgICovXG4gICAgc2Vzc2lvbkNvbnRleHQ/OiBJU2Vzc2lvbkNvbnRleHQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbW9kZWwgZmFjdG9yeSBmb3IgdGhlIGNvbnNvbGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIG1vZGVsRmFjdG9yeT86IENvZGVDb25zb2xlLklNb2RlbEZhY3Rvcnk7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2VydmljZSB1c2VkIHRvIGxvb2sgdXAgbWltZSB0eXBlcy5cbiAgICAgKi9cbiAgICBtaW1lVHlwZVNlcnZpY2U6IElFZGl0b3JNaW1lVHlwZVNlcnZpY2U7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIGNhbGwgd2hlbiB0aGUga2VybmVsIGlzIGJ1c3kuXG4gICAgICovXG4gICAgc2V0QnVzeT86ICgpID0+IElEaXNwb3NhYmxlO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb25zb2xlIHBhbmVsIHJlbmRlcmVyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29udGVudEZhY3RvcnkgZXh0ZW5kcyBDb2RlQ29uc29sZS5JQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyBjb25zb2xlIHBhbmVsLlxuICAgICAqL1xuICAgIGNyZWF0ZUNvbnNvbGUob3B0aW9uczogQ29kZUNvbnNvbGUuSU9wdGlvbnMpOiBDb2RlQ29uc29sZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEZWZhdWx0IGltcGxlbWVudGF0aW9uIG9mIGBJQ29udGVudEZhY3RvcnlgLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIENvbnRlbnRGYWN0b3J5XG4gICAgZXh0ZW5kcyBDb2RlQ29uc29sZS5Db250ZW50RmFjdG9yeVxuICAgIGltcGxlbWVudHMgSUNvbnRlbnRGYWN0b3J5IHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgY29uc29sZSBwYW5lbC5cbiAgICAgKi9cbiAgICBjcmVhdGVDb25zb2xlKG9wdGlvbnM6IENvZGVDb25zb2xlLklPcHRpb25zKTogQ29kZUNvbnNvbGUge1xuICAgICAgcmV0dXJuIG5ldyBDb2RlQ29uc29sZShvcHRpb25zKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQSBuYW1lc3BhY2UgZm9yIHRoZSBjb25zb2xlIHBhbmVsIGNvbnRlbnQgZmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBuYW1lc3BhY2UgQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIE9wdGlvbnMgZm9yIHRoZSBjb2RlIGNvbnNvbGUgY29udGVudCBmYWN0b3J5LlxuICAgICAqL1xuICAgIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMgZXh0ZW5kcyBDb2RlQ29uc29sZS5Db250ZW50RmFjdG9yeS5JT3B0aW9ucyB7fVxuICB9XG5cbiAgLyoqXG4gICAqIEEgZGVmYXVsdCBjb2RlIGNvbnNvbGUgY29udGVudCBmYWN0b3J5LlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRDb250ZW50RmFjdG9yeTogSUNvbnRlbnRGYWN0b3J5ID0gbmV3IENvbnRlbnRGYWN0b3J5KCk7XG5cbiAgLyogdHNsaW50OmRpc2FibGUgKi9cbiAgLyoqXG4gICAqIFRoZSBjb25zb2xlIHJlbmRlcmVyIHRva2VuLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IElDb250ZW50RmFjdG9yeSA9IG5ldyBUb2tlbjxJQ29udGVudEZhY3Rvcnk+KFxuICAgICdAanVweXRlcmxhYi9jb25zb2xlOklDb250ZW50RmFjdG9yeSdcbiAgKTtcbiAgLyogdHNsaW50OmVuYWJsZSAqL1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIFRoZSBjb3VudGVyIGZvciBuZXcgY29uc29sZXMuXG4gICAqL1xuICBleHBvcnQgbGV0IGNvdW50ID0gMTtcblxuICAvKipcbiAgICogVXBkYXRlIHRoZSB0aXRsZSBvZiBhIGNvbnNvbGUgcGFuZWwuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gdXBkYXRlVGl0bGUoXG4gICAgcGFuZWw6IENvbnNvbGVQYW5lbCxcbiAgICBjb25uZWN0ZWQ6IERhdGUgfCBudWxsLFxuICAgIGV4ZWN1dGVkOiBEYXRlIHwgbnVsbCxcbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3JcbiAgKSB7XG4gICAgdHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIGNvbnN0IHNlc3Npb25Db250ZXh0ID0gcGFuZWwuY29uc29sZS5zZXNzaW9uQ29udGV4dC5zZXNzaW9uO1xuICAgIGlmIChzZXNzaW9uQ29udGV4dCkge1xuICAgICAgLy8gRklYTUU6XG4gICAgICBsZXQgY2FwdGlvbiA9XG4gICAgICAgIHRyYW5zLl9fKCdOYW1lOiAlMVxcbicsIHNlc3Npb25Db250ZXh0Lm5hbWUpICtcbiAgICAgICAgdHJhbnMuX18oJ0RpcmVjdG9yeTogJTFcXG4nLCBQYXRoRXh0LmRpcm5hbWUoc2Vzc2lvbkNvbnRleHQucGF0aCkpICtcbiAgICAgICAgdHJhbnMuX18oJ0tlcm5lbDogJTEnLCBwYW5lbC5jb25zb2xlLnNlc3Npb25Db250ZXh0Lmtlcm5lbERpc3BsYXlOYW1lKTtcblxuICAgICAgaWYgKGNvbm5lY3RlZCkge1xuICAgICAgICBjYXB0aW9uICs9IHRyYW5zLl9fKFxuICAgICAgICAgICdcXG5Db25uZWN0ZWQ6ICUxJyxcbiAgICAgICAgICBUaW1lLmZvcm1hdChjb25uZWN0ZWQudG9JU09TdHJpbmcoKSlcbiAgICAgICAgKTtcbiAgICAgIH1cblxuICAgICAgaWYgKGV4ZWN1dGVkKSB7XG4gICAgICAgIGNhcHRpb24gKz0gdHJhbnMuX18oJ1xcbkxhc3QgRXhlY3V0aW9uOiAlMScpO1xuICAgICAgfVxuICAgICAgcGFuZWwudGl0bGUubGFiZWwgPSBzZXNzaW9uQ29udGV4dC5uYW1lO1xuICAgICAgcGFuZWwudGl0bGUuY2FwdGlvbiA9IGNhcHRpb247XG4gICAgfSBlbHNlIHtcbiAgICAgIHBhbmVsLnRpdGxlLmxhYmVsID0gdHJhbnMuX18oJ0NvbnNvbGUnKTtcbiAgICAgIHBhbmVsLnRpdGxlLmNhcHRpb24gPSAnJztcbiAgICB9XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVdpZGdldFRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IENvbnNvbGVQYW5lbCB9IGZyb20gJy4vcGFuZWwnO1xuXG4vKiB0c2xpbnQ6ZGlzYWJsZSAqL1xuLyoqXG4gKiBUaGUgY29uc29sZSB0cmFja2VyIHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSUNvbnNvbGVUcmFja2VyID0gbmV3IFRva2VuPElDb25zb2xlVHJhY2tlcj4oXG4gICdAanVweXRlcmxhYi9jb25zb2xlOklDb25zb2xlVHJhY2tlcidcbik7XG4vKiB0c2xpbnQ6ZW5hYmxlICovXG5cbi8qKlxuICogQSBjbGFzcyB0aGF0IHRyYWNrcyBjb25zb2xlIHdpZGdldHMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUNvbnNvbGVUcmFja2VyIGV4dGVuZHMgSVdpZGdldFRyYWNrZXI8Q29uc29sZVBhbmVsPiB7fVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJU2Vzc2lvbkNvbnRleHQgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQge1xuICBDZWxsLFxuICBDZWxsRHJhZ1V0aWxzLFxuICBDZWxsTW9kZWwsXG4gIENvZGVDZWxsLFxuICBDb2RlQ2VsbE1vZGVsLFxuICBJQ29kZUNlbGxNb2RlbCxcbiAgSVJhd0NlbGxNb2RlbCxcbiAgaXNDb2RlQ2VsbE1vZGVsLFxuICBSYXdDZWxsLFxuICBSYXdDZWxsTW9kZWxcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvY2VsbHMnO1xuaW1wb3J0IHsgQ29kZUVkaXRvciwgSUVkaXRvck1pbWVUeXBlU2VydmljZSB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0ICogYXMgbmJmb3JtYXQgZnJvbSAnQGp1cHl0ZXJsYWIvbmJmb3JtYXQnO1xuaW1wb3J0IHsgSU9ic2VydmFibGVMaXN0LCBPYnNlcnZhYmxlTGlzdCB9IGZyb20gJ0BqdXB5dGVybGFiL29ic2VydmFibGVzJztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IEtlcm5lbE1lc3NhZ2UgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBlYWNoIH0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHsgSlNPTk9iamVjdCwgTWltZURhdGEgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBEcmFnIH0gZnJvbSAnQGx1bWluby9kcmFnZHJvcCc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgUGFuZWwsIFBhbmVsTGF5b3V0LCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgQ29uc29sZUhpc3RvcnksIElDb25zb2xlSGlzdG9yeSB9IGZyb20gJy4vaGlzdG9yeSc7XG5cbi8qKlxuICogVGhlIGRhdGEgYXR0cmlidXRlIGFkZGVkIHRvIGEgd2lkZ2V0IHRoYXQgaGFzIGFuIGFjdGl2ZSBrZXJuZWwuXG4gKi9cbmNvbnN0IEtFUk5FTF9VU0VSID0gJ2pwS2VybmVsVXNlcic7XG5cbi8qKlxuICogVGhlIGRhdGEgYXR0cmlidXRlIGFkZGVkIHRvIGEgd2lkZ2V0IGNhbiBydW4gY29kZS5cbiAqL1xuY29uc3QgQ09ERV9SVU5ORVIgPSAnanBDb2RlUnVubmVyJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBjb25zb2xlIHdpZGdldHMuXG4gKi9cbmNvbnN0IENPTlNPTEVfQ0xBU1MgPSAnanAtQ29kZUNvbnNvbGUnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBhZGRlZCB0byBjb25zb2xlIGNlbGxzXG4gKi9cbmNvbnN0IENPTlNPTEVfQ0VMTF9DTEFTUyA9ICdqcC1Db25zb2xlLWNlbGwnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHRoZSBjb25zb2xlIGJhbm5lci5cbiAqL1xuY29uc3QgQkFOTkVSX0NMQVNTID0gJ2pwLUNvZGVDb25zb2xlLWJhbm5lcic7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgb2YgdGhlIGFjdGl2ZSBwcm9tcHQgY2VsbC5cbiAqL1xuY29uc3QgUFJPTVBUX0NMQVNTID0gJ2pwLUNvZGVDb25zb2xlLXByb21wdENlbGwnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIG9mIHRoZSBwYW5lbCB0aGF0IGhvbGRzIGNlbGwgY29udGVudC5cbiAqL1xuY29uc3QgQ09OVEVOVF9DTEFTUyA9ICdqcC1Db2RlQ29uc29sZS1jb250ZW50JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBvZiB0aGUgcGFuZWwgdGhhdCBob2xkcyBwcm9tcHRzLlxuICovXG5jb25zdCBJTlBVVF9DTEFTUyA9ICdqcC1Db2RlQ29uc29sZS1pbnB1dCc7XG5cbi8qKlxuICogVGhlIHRpbWVvdXQgaW4gbXMgZm9yIGV4ZWN1dGlvbiByZXF1ZXN0cyB0byB0aGUga2VybmVsLlxuICovXG5jb25zdCBFWEVDVVRJT05fVElNRU9VVCA9IDI1MDtcblxuLyoqXG4gKiBUaGUgbWltZXR5cGUgdXNlZCBmb3IgSnVweXRlciBjZWxsIGRhdGEuXG4gKi9cbmNvbnN0IEpVUFlURVJfQ0VMTF9NSU1FID0gJ2FwcGxpY2F0aW9uL3ZuZC5qdXB5dGVyLmNlbGxzJztcblxuLyoqXG4gKiBBIHdpZGdldCBjb250YWluaW5nIGEgSnVweXRlciBjb25zb2xlLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIFRoZSBDb2RlQ29uc29sZSBjbGFzcyBpcyBpbnRlbmRlZCB0byBiZSB1c2VkIHdpdGhpbiBhIENvbnNvbGVQYW5lbFxuICogaW5zdGFuY2UuIFVuZGVyIG1vc3QgY2lyY3Vtc3RhbmNlcywgaXQgaXMgbm90IGluc3RhbnRpYXRlZCBieSB1c2VyIGNvZGUuXG4gKi9cbmV4cG9ydCBjbGFzcyBDb2RlQ29uc29sZSBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBjb25zb2xlIHdpZGdldC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IENvZGVDb25zb2xlLklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLmFkZENsYXNzKENPTlNPTEVfQ0xBU1MpO1xuICAgIHRoaXMubm9kZS5kYXRhc2V0W0tFUk5FTF9VU0VSXSA9ICd0cnVlJztcbiAgICB0aGlzLm5vZGUuZGF0YXNldFtDT0RFX1JVTk5FUl0gPSAndHJ1ZSc7XG4gICAgdGhpcy5ub2RlLnRhYkluZGV4ID0gLTE7IC8vIEFsbG93IHRoZSB3aWRnZXQgdG8gdGFrZSBmb2N1cy5cblxuICAgIC8vIENyZWF0ZSB0aGUgcGFuZWxzIHRoYXQgaG9sZCB0aGUgY29udGVudCBhbmQgaW5wdXQuXG4gICAgY29uc3QgbGF5b3V0ID0gKHRoaXMubGF5b3V0ID0gbmV3IFBhbmVsTGF5b3V0KCkpO1xuICAgIHRoaXMuX2NlbGxzID0gbmV3IE9ic2VydmFibGVMaXN0PENlbGw+KCk7XG4gICAgdGhpcy5fY29udGVudCA9IG5ldyBQYW5lbCgpO1xuICAgIHRoaXMuX2lucHV0ID0gbmV3IFBhbmVsKCk7XG5cbiAgICB0aGlzLmNvbnRlbnRGYWN0b3J5ID1cbiAgICAgIG9wdGlvbnMuY29udGVudEZhY3RvcnkgfHwgQ29kZUNvbnNvbGUuZGVmYXVsdENvbnRlbnRGYWN0b3J5O1xuICAgIHRoaXMubW9kZWxGYWN0b3J5ID0gb3B0aW9ucy5tb2RlbEZhY3RvcnkgfHwgQ29kZUNvbnNvbGUuZGVmYXVsdE1vZGVsRmFjdG9yeTtcbiAgICB0aGlzLnJlbmRlcm1pbWUgPSBvcHRpb25zLnJlbmRlcm1pbWU7XG4gICAgdGhpcy5zZXNzaW9uQ29udGV4dCA9IG9wdGlvbnMuc2Vzc2lvbkNvbnRleHQ7XG4gICAgdGhpcy5fbWltZVR5cGVTZXJ2aWNlID0gb3B0aW9ucy5taW1lVHlwZVNlcnZpY2U7XG5cbiAgICAvLyBBZGQgdG9wLWxldmVsIENTUyBjbGFzc2VzLlxuICAgIHRoaXMuX2NvbnRlbnQuYWRkQ2xhc3MoQ09OVEVOVF9DTEFTUyk7XG4gICAgdGhpcy5faW5wdXQuYWRkQ2xhc3MoSU5QVVRfQ0xBU1MpO1xuXG4gICAgLy8gSW5zZXJ0IHRoZSBjb250ZW50IGFuZCBpbnB1dCBwYW5lcyBpbnRvIHRoZSB3aWRnZXQuXG4gICAgbGF5b3V0LmFkZFdpZGdldCh0aGlzLl9jb250ZW50KTtcbiAgICBsYXlvdXQuYWRkV2lkZ2V0KHRoaXMuX2lucHV0KTtcblxuICAgIHRoaXMuX2hpc3RvcnkgPSBuZXcgQ29uc29sZUhpc3Rvcnkoe1xuICAgICAgc2Vzc2lvbkNvbnRleHQ6IHRoaXMuc2Vzc2lvbkNvbnRleHRcbiAgICB9KTtcblxuICAgIHZvaWQgdGhpcy5fb25LZXJuZWxDaGFuZ2VkKCk7XG5cbiAgICB0aGlzLnNlc3Npb25Db250ZXh0Lmtlcm5lbENoYW5nZWQuY29ubmVjdCh0aGlzLl9vbktlcm5lbENoYW5nZWQsIHRoaXMpO1xuICAgIHRoaXMuc2Vzc2lvbkNvbnRleHQuc3RhdHVzQ2hhbmdlZC5jb25uZWN0KFxuICAgICAgdGhpcy5fb25LZXJuZWxTdGF0dXNDaGFuZ2VkLFxuICAgICAgdGhpc1xuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBjb25zb2xlIGZpbmlzaGVkIGV4ZWN1dGluZyBpdHMgcHJvbXB0IGNlbGwuXG4gICAqL1xuICBnZXQgZXhlY3V0ZWQoKTogSVNpZ25hbDx0aGlzLCBEYXRlPiB7XG4gICAgcmV0dXJuIHRoaXMuX2V4ZWN1dGVkO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBhIG5ldyBwcm9tcHQgY2VsbCBpcyBjcmVhdGVkLlxuICAgKi9cbiAgZ2V0IHByb21wdENlbGxDcmVhdGVkKCk6IElTaWduYWw8dGhpcywgQ29kZUNlbGw+IHtcbiAgICByZXR1cm4gdGhpcy5fcHJvbXB0Q2VsbENyZWF0ZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGNvbnRlbnQgZmFjdG9yeSB1c2VkIGJ5IHRoZSBjb25zb2xlLlxuICAgKi9cbiAgcmVhZG9ubHkgY29udGVudEZhY3Rvcnk6IENvZGVDb25zb2xlLklDb250ZW50RmFjdG9yeTtcblxuICAvKipcbiAgICogVGhlIG1vZGVsIGZhY3RvcnkgZm9yIHRoZSBjb25zb2xlIHdpZGdldC5cbiAgICovXG4gIHJlYWRvbmx5IG1vZGVsRmFjdG9yeTogQ29kZUNvbnNvbGUuSU1vZGVsRmFjdG9yeTtcblxuICAvKipcbiAgICogVGhlIHJlbmRlcm1pbWUgaW5zdGFuY2UgdXNlZCBieSB0aGUgY29uc29sZS5cbiAgICovXG4gIHJlYWRvbmx5IHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnk7XG5cbiAgLyoqXG4gICAqIFRoZSBjbGllbnQgc2Vzc2lvbiB1c2VkIGJ5IHRoZSBjb25zb2xlLlxuICAgKi9cbiAgcmVhZG9ubHkgc2Vzc2lvbkNvbnRleHQ6IElTZXNzaW9uQ29udGV4dDtcblxuICAvKipcbiAgICogVGhlIGxpc3Qgb2YgY29udGVudCBjZWxscyBpbiB0aGUgY29uc29sZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGxpc3QgZG9lcyBub3QgaW5jbHVkZSB0aGUgY3VycmVudCBiYW5uZXIgb3IgdGhlIHByb21wdCBmb3IgYSBjb25zb2xlLlxuICAgKiBJdCBtYXkgaW5jbHVkZSBwcmV2aW91cyBiYW5uZXJzIGFzIHJhdyBjZWxscy5cbiAgICovXG4gIGdldCBjZWxscygpOiBJT2JzZXJ2YWJsZUxpc3Q8Q2VsbD4ge1xuICAgIHJldHVybiB0aGlzLl9jZWxscztcbiAgfVxuXG4gIC8qXG4gICAqIFRoZSBjb25zb2xlIGlucHV0IHByb21wdCBjZWxsLlxuICAgKi9cbiAgZ2V0IHByb21wdENlbGwoKTogQ29kZUNlbGwgfCBudWxsIHtcbiAgICBjb25zdCBpbnB1dExheW91dCA9IHRoaXMuX2lucHV0LmxheW91dCBhcyBQYW5lbExheW91dDtcbiAgICByZXR1cm4gKGlucHV0TGF5b3V0LndpZGdldHNbMF0gYXMgQ29kZUNlbGwpIHx8IG51bGw7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgbmV3IGNlbGwgdG8gdGhlIGNvbnRlbnQgcGFuZWwuXG4gICAqXG4gICAqIEBwYXJhbSBjZWxsIC0gVGhlIGNvZGUgY2VsbCB3aWRnZXQgYmVpbmcgYWRkZWQgdG8gdGhlIGNvbnRlbnQgcGFuZWwuXG4gICAqXG4gICAqIEBwYXJhbSBtc2dJZCAtIFRoZSBvcHRpb25hbCBleGVjdXRpb24gbWVzc2FnZSBpZCBmb3IgdGhlIGNlbGwuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgaXMgbWVhbnQgZm9yIHVzZSBieSBvdXRzaWRlIGNsYXNzZXMgdGhhdCB3YW50IHRvIGFkZCBjZWxscyB0byBhXG4gICAqIGNvbnNvbGUuIEl0IGlzIGRpc3RpbmN0IGZyb20gdGhlIGBpbmplY3RgIG1ldGhvZCBpbiB0aGF0IGl0IHJlcXVpcmVzXG4gICAqIHJlbmRlcmVkIGNvZGUgY2VsbCB3aWRnZXRzIGFuZCBkb2VzIG5vdCBleGVjdXRlIHRoZW0gKHRob3VnaCBpdCBjYW4gc3RvcmVcbiAgICogdGhlIGV4ZWN1dGlvbiBtZXNzYWdlIGlkKS5cbiAgICovXG4gIGFkZENlbGwoY2VsbDogQ29kZUNlbGwsIG1zZ0lkPzogc3RyaW5nKSB7XG4gICAgY2VsbC5hZGRDbGFzcyhDT05TT0xFX0NFTExfQ0xBU1MpO1xuICAgIHRoaXMuX2NvbnRlbnQuYWRkV2lkZ2V0KGNlbGwpO1xuICAgIHRoaXMuX2NlbGxzLnB1c2goY2VsbCk7XG4gICAgaWYgKG1zZ0lkKSB7XG4gICAgICB0aGlzLl9tc2dJZHMuc2V0KG1zZ0lkLCBjZWxsKTtcbiAgICAgIHRoaXMuX21zZ0lkQ2VsbHMuc2V0KGNlbGwsIG1zZ0lkKTtcbiAgICB9XG4gICAgY2VsbC5kaXNwb3NlZC5jb25uZWN0KHRoaXMuX29uQ2VsbERpc3Bvc2VkLCB0aGlzKTtcbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIGJhbm5lciBjZWxsLlxuICAgKi9cbiAgYWRkQmFubmVyKCkge1xuICAgIGlmICh0aGlzLl9iYW5uZXIpIHtcbiAgICAgIC8vIEFuIG9sZCBiYW5uZXIganVzdCBiZWNvbWVzIGEgbm9ybWFsIGNlbGwgbm93LlxuICAgICAgY29uc3QgY2VsbCA9IHRoaXMuX2Jhbm5lcjtcbiAgICAgIHRoaXMuX2NlbGxzLnB1c2godGhpcy5fYmFubmVyKTtcbiAgICAgIGNlbGwuZGlzcG9zZWQuY29ubmVjdCh0aGlzLl9vbkNlbGxEaXNwb3NlZCwgdGhpcyk7XG4gICAgfVxuICAgIC8vIENyZWF0ZSB0aGUgYmFubmVyLlxuICAgIGNvbnN0IG1vZGVsID0gdGhpcy5tb2RlbEZhY3RvcnkuY3JlYXRlUmF3Q2VsbCh7fSk7XG4gICAgbW9kZWwudmFsdWUudGV4dCA9ICcuLi4nO1xuICAgIGNvbnN0IGJhbm5lciA9ICh0aGlzLl9iYW5uZXIgPSBuZXcgUmF3Q2VsbCh7XG4gICAgICBtb2RlbCxcbiAgICAgIGNvbnRlbnRGYWN0b3J5OiB0aGlzLmNvbnRlbnRGYWN0b3J5LFxuICAgICAgcGxhY2Vob2xkZXI6IGZhbHNlXG4gICAgfSkpLmluaXRpYWxpemVTdGF0ZSgpO1xuICAgIGJhbm5lci5hZGRDbGFzcyhCQU5ORVJfQ0xBU1MpO1xuICAgIGJhbm5lci5yZWFkT25seSA9IHRydWU7XG4gICAgdGhpcy5fY29udGVudC5hZGRXaWRnZXQoYmFubmVyKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhciB0aGUgY29kZSBjZWxscy5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQge1xuICAgIC8vIERpc3Bvc2UgYWxsIHRoZSBjb250ZW50IGNlbGxzXG4gICAgY29uc3QgY2VsbHMgPSB0aGlzLl9jZWxscztcbiAgICB3aGlsZSAoY2VsbHMubGVuZ3RoID4gMCkge1xuICAgICAgY2VsbHMuZ2V0KDApLmRpc3Bvc2UoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IGNlbGwgd2l0aCB0aGUgYnVpbHQtaW4gZmFjdG9yeS5cbiAgICovXG4gIGNyZWF0ZUNvZGVDZWxsKCk6IENvZGVDZWxsIHtcbiAgICBjb25zdCBmYWN0b3J5ID0gdGhpcy5jb250ZW50RmFjdG9yeTtcbiAgICBjb25zdCBvcHRpb25zID0gdGhpcy5fY3JlYXRlQ29kZUNlbGxPcHRpb25zKCk7XG4gICAgY29uc3QgY2VsbCA9IGZhY3RvcnkuY3JlYXRlQ29kZUNlbGwob3B0aW9ucyk7XG4gICAgY2VsbC5yZWFkT25seSA9IHRydWU7XG4gICAgY2VsbC5tb2RlbC5taW1lVHlwZSA9IHRoaXMuX21pbWV0eXBlO1xuICAgIHJldHVybiBjZWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSB3aWRnZXQuXG4gICAqL1xuICBkaXNwb3NlKCkge1xuICAgIC8vIERvIG5vdGhpbmcgaWYgYWxyZWFkeSBkaXNwb3NlZC5cbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2NlbGxzLmNsZWFyKCk7XG4gICAgdGhpcy5fbXNnSWRDZWxscyA9IG51bGwhO1xuICAgIHRoaXMuX21zZ0lkcyA9IG51bGwhO1xuICAgIHRoaXMuX2hpc3RvcnkuZGlzcG9zZSgpO1xuXG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEV4ZWN1dGUgdGhlIGN1cnJlbnQgcHJvbXB0LlxuICAgKlxuICAgKiBAcGFyYW0gZm9yY2UgLSBXaGV0aGVyIHRvIGZvcmNlIGV4ZWN1dGlvbiB3aXRob3V0IGNoZWNraW5nIGNvZGVcbiAgICogY29tcGxldGVuZXNzLlxuICAgKlxuICAgKiBAcGFyYW0gdGltZW91dCAtIFRoZSBsZW5ndGggb2YgdGltZSwgaW4gbWlsbGlzZWNvbmRzLCB0aGF0IHRoZSBleGVjdXRpb25cbiAgICogc2hvdWxkIHdhaXQgZm9yIHRoZSBBUEkgdG8gZGV0ZXJtaW5lIHdoZXRoZXIgY29kZSBiZWluZyBzdWJtaXR0ZWQgaXNcbiAgICogaW5jb21wbGV0ZSBiZWZvcmUgYXR0ZW1wdGluZyBzdWJtaXNzaW9uIGFueXdheS4gVGhlIGRlZmF1bHQgdmFsdWUgaXMgYDI1MGAuXG4gICAqL1xuICBhc3luYyBleGVjdXRlKGZvcmNlID0gZmFsc2UsIHRpbWVvdXQgPSBFWEVDVVRJT05fVElNRU9VVCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGlmICh0aGlzLnNlc3Npb25Db250ZXh0LnNlc3Npb24/Lmtlcm5lbD8uc3RhdHVzID09PSAnZGVhZCcpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCBwcm9tcHRDZWxsID0gdGhpcy5wcm9tcHRDZWxsO1xuICAgIGlmICghcHJvbXB0Q2VsbCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCdDYW5ub3QgZXhlY3V0ZSB3aXRob3V0IGEgcHJvbXB0IGNlbGwnKTtcbiAgICB9XG4gICAgcHJvbXB0Q2VsbC5tb2RlbC50cnVzdGVkID0gdHJ1ZTtcblxuICAgIGlmIChmb3JjZSkge1xuICAgICAgLy8gQ3JlYXRlIGEgbmV3IHByb21wdCBjZWxsIGJlZm9yZSBrZXJuZWwgZXhlY3V0aW9uIHRvIGFsbG93IHR5cGVhaGVhZC5cbiAgICAgIHRoaXMubmV3UHJvbXB0Q2VsbCgpO1xuICAgICAgYXdhaXQgdGhpcy5fZXhlY3V0ZShwcm9tcHRDZWxsKTtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBDaGVjayB3aGV0aGVyIHdlIHNob3VsZCBleGVjdXRlLlxuICAgIGNvbnN0IHNob3VsZEV4ZWN1dGUgPSBhd2FpdCB0aGlzLl9zaG91bGRFeGVjdXRlKHRpbWVvdXQpO1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgaWYgKHNob3VsZEV4ZWN1dGUpIHtcbiAgICAgIC8vIENyZWF0ZSBhIG5ldyBwcm9tcHQgY2VsbCBiZWZvcmUga2VybmVsIGV4ZWN1dGlvbiB0byBhbGxvdyB0eXBlYWhlYWQuXG4gICAgICB0aGlzLm5ld1Byb21wdENlbGwoKTtcbiAgICAgIHRoaXMucHJvbXB0Q2VsbCEuZWRpdG9yLmZvY3VzKCk7XG4gICAgICBhd2FpdCB0aGlzLl9leGVjdXRlKHByb21wdENlbGwpO1xuICAgIH0gZWxzZSB7XG4gICAgICAvLyBhZGQgYSBuZXdsaW5lIGlmIHdlIHNob3VsZG4ndCBleGVjdXRlXG4gICAgICBwcm9tcHRDZWxsLmVkaXRvci5uZXdJbmRlbnRlZExpbmUoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogR2V0IGEgY2VsbCBnaXZlbiBhIG1lc3NhZ2UgaWQuXG4gICAqXG4gICAqIEBwYXJhbSBtc2dJZCAtIFRoZSBtZXNzYWdlIGlkLlxuICAgKi9cbiAgZ2V0Q2VsbChtc2dJZDogc3RyaW5nKTogQ29kZUNlbGwgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiB0aGlzLl9tc2dJZHMuZ2V0KG1zZ0lkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbmplY3QgYXJiaXRyYXJ5IGNvZGUgZm9yIHRoZSBjb25zb2xlIHRvIGV4ZWN1dGUgaW1tZWRpYXRlbHkuXG4gICAqXG4gICAqIEBwYXJhbSBjb2RlIC0gVGhlIGNvZGUgY29udGVudHMgb2YgdGhlIGNlbGwgYmVpbmcgaW5qZWN0ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGluZGljYXRlcyB3aGVuIHRoZSBpbmplY3RlZCBjZWxsJ3MgZXhlY3V0aW9uIGVuZHMuXG4gICAqL1xuICBpbmplY3QoY29kZTogc3RyaW5nLCBtZXRhZGF0YTogSlNPTk9iamVjdCA9IHt9KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgY2VsbCA9IHRoaXMuY3JlYXRlQ29kZUNlbGwoKTtcbiAgICBjZWxsLm1vZGVsLnZhbHVlLnRleHQgPSBjb2RlO1xuICAgIGZvciAoY29uc3Qga2V5IG9mIE9iamVjdC5rZXlzKG1ldGFkYXRhKSkge1xuICAgICAgY2VsbC5tb2RlbC5tZXRhZGF0YS5zZXQoa2V5LCBtZXRhZGF0YVtrZXldKTtcbiAgICB9XG4gICAgdGhpcy5hZGRDZWxsKGNlbGwpO1xuICAgIHJldHVybiB0aGlzLl9leGVjdXRlKGNlbGwpO1xuICB9XG5cbiAgLyoqXG4gICAqIEluc2VydCBhIGxpbmUgYnJlYWsgaW4gdGhlIHByb21wdCBjZWxsLlxuICAgKi9cbiAgaW5zZXJ0TGluZWJyZWFrKCk6IHZvaWQge1xuICAgIGNvbnN0IHByb21wdENlbGwgPSB0aGlzLnByb21wdENlbGw7XG4gICAgaWYgKCFwcm9tcHRDZWxsKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHByb21wdENlbGwuZWRpdG9yLm5ld0luZGVudGVkTGluZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlcGxhY2VzIHRoZSBzZWxlY3RlZCB0ZXh0IGluIHRoZSBwcm9tcHQgY2VsbC5cbiAgICpcbiAgICogQHBhcmFtIHRleHQgLSBUaGUgdGV4dCB0byByZXBsYWNlIHRoZSBzZWxlY3Rpb24uXG4gICAqL1xuICByZXBsYWNlU2VsZWN0aW9uKHRleHQ6IHN0cmluZyk6IHZvaWQge1xuICAgIGNvbnN0IHByb21wdENlbGwgPSB0aGlzLnByb21wdENlbGw7XG4gICAgaWYgKCFwcm9tcHRDZWxsKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHByb21wdENlbGwuZWRpdG9yLnJlcGxhY2VTZWxlY3Rpb24/Lih0ZXh0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXJpYWxpemUgdGhlIG91dHB1dC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIG9ubHkgc2VyaWFsaXplcyB0aGUgY29kZSBjZWxscyBhbmQgdGhlIHByb21wdCBjZWxsIGlmIGl0IGV4aXN0cywgYW5kXG4gICAqIHNraXBzIGFueSBvbGQgYmFubmVyIGNlbGxzLlxuICAgKi9cbiAgc2VyaWFsaXplKCk6IG5iZm9ybWF0LklDb2RlQ2VsbFtdIHtcbiAgICBjb25zdCBjZWxsczogbmJmb3JtYXQuSUNvZGVDZWxsW10gPSBbXTtcbiAgICBlYWNoKHRoaXMuX2NlbGxzLCBjZWxsID0+IHtcbiAgICAgIGNvbnN0IG1vZGVsID0gY2VsbC5tb2RlbDtcbiAgICAgIGlmIChpc0NvZGVDZWxsTW9kZWwobW9kZWwpKSB7XG4gICAgICAgIGNlbGxzLnB1c2gobW9kZWwudG9KU09OKCkpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgaWYgKHRoaXMucHJvbXB0Q2VsbCkge1xuICAgICAgY2VsbHMucHVzaCh0aGlzLnByb21wdENlbGwubW9kZWwudG9KU09OKCkpO1xuICAgIH1cbiAgICByZXR1cm4gY2VsbHM7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBtb3VzZWRvd25gIGV2ZW50cyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByaXZhdGUgX2V2dE1vdXNlRG93bihldmVudDogTW91c2VFdmVudCk6IHZvaWQge1xuICAgIGNvbnN0IHsgYnV0dG9uLCBzaGlmdEtleSB9ID0gZXZlbnQ7XG5cbiAgICAvLyBXZSBvbmx5IGhhbmRsZSBtYWluIG9yIHNlY29uZGFyeSBidXR0b24gYWN0aW9ucy5cbiAgICBpZiAoXG4gICAgICAhKGJ1dHRvbiA9PT0gMCB8fCBidXR0b24gPT09IDIpIHx8XG4gICAgICAvLyBTaGlmdCByaWdodC1jbGljayBnaXZlcyB0aGUgYnJvd3NlciBkZWZhdWx0IGJlaGF2aW9yLlxuICAgICAgKHNoaWZ0S2V5ICYmIGJ1dHRvbiA9PT0gMilcbiAgICApIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBsZXQgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgIGNvbnN0IGNlbGxGaWx0ZXIgPSAobm9kZTogSFRNTEVsZW1lbnQpID0+XG4gICAgICBub2RlLmNsYXNzTGlzdC5jb250YWlucyhDT05TT0xFX0NFTExfQ0xBU1MpO1xuICAgIGxldCBjZWxsSW5kZXggPSBDZWxsRHJhZ1V0aWxzLmZpbmRDZWxsKHRhcmdldCwgdGhpcy5fY2VsbHMsIGNlbGxGaWx0ZXIpO1xuXG4gICAgaWYgKGNlbGxJbmRleCA9PT0gLTEpIHtcbiAgICAgIC8vIGBldmVudC50YXJnZXRgIHNvbWV0aW1lcyBnaXZlcyBhbiBvcnBoYW5lZCBub2RlIGluXG4gICAgICAvLyBGaXJlZm94IDU3LCB3aGljaCBjYW4gaGF2ZSBgbnVsbGAgYW55d2hlcmUgaW4gaXRzIHBhcmVudCBsaW5lLiBJZiB3ZSBmYWlsXG4gICAgICAvLyB0byBmaW5kIGEgY2VsbCB1c2luZyBgZXZlbnQudGFyZ2V0YCwgdHJ5IGFnYWluIHVzaW5nIGEgdGFyZ2V0XG4gICAgICAvLyByZWNvbnN0cnVjdGVkIGZyb20gdGhlIHBvc2l0aW9uIG9mIHRoZSBjbGljayBldmVudC5cbiAgICAgIHRhcmdldCA9IGRvY3VtZW50LmVsZW1lbnRGcm9tUG9pbnQoXG4gICAgICAgIGV2ZW50LmNsaWVudFgsXG4gICAgICAgIGV2ZW50LmNsaWVudFlcbiAgICAgICkgYXMgSFRNTEVsZW1lbnQ7XG4gICAgICBjZWxsSW5kZXggPSBDZWxsRHJhZ1V0aWxzLmZpbmRDZWxsKHRhcmdldCwgdGhpcy5fY2VsbHMsIGNlbGxGaWx0ZXIpO1xuICAgIH1cblxuICAgIGlmIChjZWxsSW5kZXggPT09IC0xKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3QgY2VsbCA9IHRoaXMuX2NlbGxzLmdldChjZWxsSW5kZXgpO1xuXG4gICAgY29uc3QgdGFyZ2V0QXJlYTogQ2VsbERyYWdVdGlscy5JQ2VsbFRhcmdldEFyZWEgPSBDZWxsRHJhZ1V0aWxzLmRldGVjdFRhcmdldEFyZWEoXG4gICAgICBjZWxsLFxuICAgICAgZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50XG4gICAgKTtcblxuICAgIGlmICh0YXJnZXRBcmVhID09PSAncHJvbXB0Jykge1xuICAgICAgdGhpcy5fZHJhZ0RhdGEgPSB7XG4gICAgICAgIHByZXNzWDogZXZlbnQuY2xpZW50WCxcbiAgICAgICAgcHJlc3NZOiBldmVudC5jbGllbnRZLFxuICAgICAgICBpbmRleDogY2VsbEluZGV4XG4gICAgICB9O1xuXG4gICAgICB0aGlzLl9mb2N1c2VkQ2VsbCA9IGNlbGw7XG5cbiAgICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ21vdXNldXAnLCB0aGlzLCB0cnVlKTtcbiAgICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ21vdXNlbW92ZScsIHRoaXMsIHRydWUpO1xuICAgICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBtb3VzZW1vdmVgIGV2ZW50IG9mIHdpZGdldFxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0TW91c2VNb3ZlKGV2ZW50OiBNb3VzZUV2ZW50KSB7XG4gICAgY29uc3QgZGF0YSA9IHRoaXMuX2RyYWdEYXRhO1xuICAgIGlmIChcbiAgICAgIGRhdGEgJiZcbiAgICAgIENlbGxEcmFnVXRpbHMuc2hvdWxkU3RhcnREcmFnKFxuICAgICAgICBkYXRhLnByZXNzWCxcbiAgICAgICAgZGF0YS5wcmVzc1ksXG4gICAgICAgIGV2ZW50LmNsaWVudFgsXG4gICAgICAgIGV2ZW50LmNsaWVudFlcbiAgICAgIClcbiAgICApIHtcbiAgICAgIHZvaWQgdGhpcy5fc3RhcnREcmFnKGRhdGEuaW5kZXgsIGV2ZW50LmNsaWVudFgsIGV2ZW50LmNsaWVudFkpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBTdGFydCBhIGRyYWcgZXZlbnRcbiAgICovXG4gIHByaXZhdGUgX3N0YXJ0RHJhZyhcbiAgICBpbmRleDogbnVtYmVyLFxuICAgIGNsaWVudFg6IG51bWJlcixcbiAgICBjbGllbnRZOiBudW1iZXJcbiAgKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgY2VsbE1vZGVsID0gdGhpcy5fZm9jdXNlZENlbGwhLm1vZGVsIGFzIElDb2RlQ2VsbE1vZGVsO1xuICAgIGNvbnN0IHNlbGVjdGVkOiBuYmZvcm1hdC5JQ2VsbFtdID0gW2NlbGxNb2RlbC50b0pTT04oKV07XG5cbiAgICBjb25zdCBkcmFnSW1hZ2UgPSBDZWxsRHJhZ1V0aWxzLmNyZWF0ZUNlbGxEcmFnSW1hZ2UoXG4gICAgICB0aGlzLl9mb2N1c2VkQ2VsbCEsXG4gICAgICBzZWxlY3RlZFxuICAgICk7XG5cbiAgICB0aGlzLl9kcmFnID0gbmV3IERyYWcoe1xuICAgICAgbWltZURhdGE6IG5ldyBNaW1lRGF0YSgpLFxuICAgICAgZHJhZ0ltYWdlLFxuICAgICAgcHJvcG9zZWRBY3Rpb246ICdjb3B5JyxcbiAgICAgIHN1cHBvcnRlZEFjdGlvbnM6ICdjb3B5JyxcbiAgICAgIHNvdXJjZTogdGhpc1xuICAgIH0pO1xuXG4gICAgdGhpcy5fZHJhZy5taW1lRGF0YS5zZXREYXRhKEpVUFlURVJfQ0VMTF9NSU1FLCBzZWxlY3RlZCk7XG4gICAgY29uc3QgdGV4dENvbnRlbnQgPSBjZWxsTW9kZWwudmFsdWUudGV4dDtcbiAgICB0aGlzLl9kcmFnLm1pbWVEYXRhLnNldERhdGEoJ3RleHQvcGxhaW4nLCB0ZXh0Q29udGVudCk7XG5cbiAgICB0aGlzLl9mb2N1c2VkQ2VsbCA9IG51bGw7XG5cbiAgICBkb2N1bWVudC5yZW1vdmVFdmVudExpc3RlbmVyKCdtb3VzZW1vdmUnLCB0aGlzLCB0cnVlKTtcbiAgICBkb2N1bWVudC5yZW1vdmVFdmVudExpc3RlbmVyKCdtb3VzZXVwJywgdGhpcywgdHJ1ZSk7XG4gICAgcmV0dXJuIHRoaXMuX2RyYWcuc3RhcnQoY2xpZW50WCwgY2xpZW50WSkudGhlbigoKSA9PiB7XG4gICAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHRoaXMuX2RyYWcgPSBudWxsO1xuICAgICAgdGhpcy5fZHJhZ0RhdGEgPSBudWxsO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgRE9NIGV2ZW50cyBmb3IgdGhlIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIGV2ZW50IC1UaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIG1ldGhvZCBpbXBsZW1lbnRzIHRoZSBET00gYEV2ZW50TGlzdGVuZXJgIGludGVyZmFjZSBhbmQgaXNcbiAgICogY2FsbGVkIGluIHJlc3BvbnNlIHRvIGV2ZW50cyBvbiB0aGUgbm90ZWJvb2sgcGFuZWwncyBub2RlLiBJdCBzaG91bGRcbiAgICogbm90IGJlIGNhbGxlZCBkaXJlY3RseSBieSB1c2VyIGNvZGUuXG4gICAqL1xuICBoYW5kbGVFdmVudChldmVudDogRXZlbnQpOiB2b2lkIHtcbiAgICBzd2l0Y2ggKGV2ZW50LnR5cGUpIHtcbiAgICAgIGNhc2UgJ2tleWRvd24nOlxuICAgICAgICB0aGlzLl9ldnRLZXlEb3duKGV2ZW50IGFzIEtleWJvYXJkRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ21vdXNlZG93bic6XG4gICAgICAgIHRoaXMuX2V2dE1vdXNlRG93bihldmVudCBhcyBNb3VzZUV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdtb3VzZW1vdmUnOlxuICAgICAgICB0aGlzLl9ldnRNb3VzZU1vdmUoZXZlbnQgYXMgTW91c2VFdmVudCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnbW91c2V1cCc6XG4gICAgICAgIHRoaXMuX2V2dE1vdXNlVXAoZXZlbnQgYXMgTW91c2VFdmVudCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYWZ0ZXJfYXR0YWNoYCBtZXNzYWdlcyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFmdGVyQXR0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGNvbnN0IG5vZGUgPSB0aGlzLm5vZGU7XG4gICAgbm9kZS5hZGRFdmVudExpc3RlbmVyKCdrZXlkb3duJywgdGhpcywgdHJ1ZSk7XG4gICAgbm9kZS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIHRoaXMpO1xuICAgIG5vZGUuYWRkRXZlbnRMaXN0ZW5lcignbW91c2Vkb3duJywgdGhpcyk7XG4gICAgLy8gQ3JlYXRlIGEgcHJvbXB0IGlmIG5lY2Vzc2FyeS5cbiAgICBpZiAoIXRoaXMucHJvbXB0Q2VsbCkge1xuICAgICAgdGhpcy5uZXdQcm9tcHRDZWxsKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMucHJvbXB0Q2VsbC5lZGl0b3IuZm9jdXMoKTtcbiAgICAgIHRoaXMudXBkYXRlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYmVmb3JlLWRldGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgY29uc3Qgbm9kZSA9IHRoaXMubm9kZTtcbiAgICBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCB0aGlzLCB0cnVlKTtcbiAgICBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAnYWN0aXZhdGUtcmVxdWVzdCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWN0aXZhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGNvbnN0IGVkaXRvciA9IHRoaXMucHJvbXB0Q2VsbCAmJiB0aGlzLnByb21wdENlbGwuZWRpdG9yO1xuICAgIGlmIChlZGl0b3IpIHtcbiAgICAgIGVkaXRvci5mb2N1cygpO1xuICAgIH1cbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIE1ha2UgYSBuZXcgcHJvbXB0IGNlbGwuXG4gICAqL1xuICBwcm90ZWN0ZWQgbmV3UHJvbXB0Q2VsbCgpOiB2b2lkIHtcbiAgICBsZXQgcHJvbXB0Q2VsbCA9IHRoaXMucHJvbXB0Q2VsbDtcbiAgICBjb25zdCBpbnB1dCA9IHRoaXMuX2lucHV0O1xuXG4gICAgLy8gTWFrZSB0aGUgbGFzdCBwcm9tcHQgcmVhZC1vbmx5LCBjbGVhciBpdHMgc2lnbmFscywgYW5kIG1vdmUgdG8gY29udGVudC5cbiAgICBpZiAocHJvbXB0Q2VsbCkge1xuICAgICAgcHJvbXB0Q2VsbC5yZWFkT25seSA9IHRydWU7XG4gICAgICBwcm9tcHRDZWxsLnJlbW92ZUNsYXNzKFBST01QVF9DTEFTUyk7XG4gICAgICBTaWduYWwuY2xlYXJEYXRhKHByb21wdENlbGwuZWRpdG9yKTtcbiAgICAgIGNvbnN0IGNoaWxkID0gaW5wdXQud2lkZ2V0c1swXTtcbiAgICAgIGNoaWxkLnBhcmVudCA9IG51bGw7XG4gICAgICB0aGlzLmFkZENlbGwocHJvbXB0Q2VsbCk7XG4gICAgfVxuXG4gICAgLy8gQ3JlYXRlIHRoZSBuZXcgcHJvbXB0IGNlbGwuXG4gICAgY29uc3QgZmFjdG9yeSA9IHRoaXMuY29udGVudEZhY3Rvcnk7XG4gICAgY29uc3Qgb3B0aW9ucyA9IHRoaXMuX2NyZWF0ZUNvZGVDZWxsT3B0aW9ucygpO1xuICAgIHByb21wdENlbGwgPSBmYWN0b3J5LmNyZWF0ZUNvZGVDZWxsKG9wdGlvbnMpO1xuICAgIHByb21wdENlbGwubW9kZWwubWltZVR5cGUgPSB0aGlzLl9taW1ldHlwZTtcbiAgICBwcm9tcHRDZWxsLmFkZENsYXNzKFBST01QVF9DTEFTUyk7XG5cbiAgICAvLyBBZGQgdGhlIHByb21wdCBjZWxsIHRvIHRoZSBET00sIG1ha2luZyBgdGhpcy5wcm9tcHRDZWxsYCB2YWxpZCBhZ2Fpbi5cbiAgICB0aGlzLl9pbnB1dC5hZGRXaWRnZXQocHJvbXB0Q2VsbCk7XG5cbiAgICAvLyBTdXBwcmVzcyB0aGUgZGVmYXVsdCBcIkVudGVyXCIga2V5IGhhbmRsaW5nLlxuICAgIGNvbnN0IGVkaXRvciA9IHByb21wdENlbGwuZWRpdG9yO1xuICAgIGVkaXRvci5hZGRLZXlkb3duSGFuZGxlcih0aGlzLl9vbkVkaXRvcktleWRvd24pO1xuXG4gICAgdGhpcy5faGlzdG9yeS5lZGl0b3IgPSBlZGl0b3I7XG4gICAgdGhpcy5fcHJvbXB0Q2VsbENyZWF0ZWQuZW1pdChwcm9tcHRDZWxsKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYHVwZGF0ZS1yZXF1ZXN0YCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvblVwZGF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgUHJpdmF0ZS5zY3JvbGxUb0JvdHRvbSh0aGlzLl9jb250ZW50Lm5vZGUpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgYCdrZXlkb3duJ2AgZXZlbnQgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9ldnRLZXlEb3duKGV2ZW50OiBLZXlib2FyZEV2ZW50KTogdm9pZCB7XG4gICAgY29uc3QgZWRpdG9yID0gdGhpcy5wcm9tcHRDZWxsICYmIHRoaXMucHJvbXB0Q2VsbC5lZGl0b3I7XG4gICAgaWYgKCFlZGl0b3IpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgaWYgKGV2ZW50LmtleUNvZGUgPT09IDEzICYmICFlZGl0b3IuaGFzRm9jdXMoKSkge1xuICAgICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcbiAgICAgIGVkaXRvci5mb2N1cygpO1xuICAgIH0gZWxzZSBpZiAoZXZlbnQua2V5Q29kZSA9PT0gMjcgJiYgZWRpdG9yLmhhc0ZvY3VzKCkpIHtcbiAgICAgIC8vIFNldCB0byBjb21tYW5kIG1vZGVcbiAgICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICBldmVudC5zdG9wUHJvcGFnYXRpb24oKTtcbiAgICAgIHRoaXMubm9kZS5mb2N1cygpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGAnbW91c2V1cCdgIGV2ZW50IGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0TW91c2VVcChldmVudDogTW91c2VFdmVudCk6IHZvaWQge1xuICAgIGlmIChcbiAgICAgIHRoaXMucHJvbXB0Q2VsbCAmJlxuICAgICAgdGhpcy5wcm9tcHRDZWxsLm5vZGUuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50KVxuICAgICkge1xuICAgICAgdGhpcy5wcm9tcHRDZWxsLmVkaXRvci5mb2N1cygpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBFeGVjdXRlIHRoZSBjb2RlIGluIHRoZSBjdXJyZW50IHByb21wdCBjZWxsLlxuICAgKi9cbiAgcHJpdmF0ZSBfZXhlY3V0ZShjZWxsOiBDb2RlQ2VsbCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IHNvdXJjZSA9IGNlbGwubW9kZWwudmFsdWUudGV4dDtcbiAgICB0aGlzLl9oaXN0b3J5LnB1c2goc291cmNlKTtcbiAgICAvLyBJZiB0aGUgc291cmNlIG9mIHRoZSBjb25zb2xlIGlzIGp1c3QgXCJjbGVhclwiLCBjbGVhciB0aGUgY29uc29sZSBhcyB3ZVxuICAgIC8vIGRvIGluIElQeXRob24gb3IgUXRDb25zb2xlLlxuICAgIGlmIChzb3VyY2UgPT09ICdjbGVhcicgfHwgc291cmNlID09PSAnJWNsZWFyJykge1xuICAgICAgdGhpcy5jbGVhcigpO1xuICAgICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZSh2b2lkIDApO1xuICAgIH1cbiAgICBjZWxsLm1vZGVsLmNvbnRlbnRDaGFuZ2VkLmNvbm5lY3QodGhpcy51cGRhdGUsIHRoaXMpO1xuICAgIGNvbnN0IG9uU3VjY2VzcyA9ICh2YWx1ZTogS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcGx5TXNnKSA9PiB7XG4gICAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGlmICh2YWx1ZSAmJiB2YWx1ZS5jb250ZW50LnN0YXR1cyA9PT0gJ29rJykge1xuICAgICAgICBjb25zdCBjb250ZW50ID0gdmFsdWUuY29udGVudDtcbiAgICAgICAgLy8gVXNlIGRlcHJlY2F0ZWQgcGF5bG9hZHMgZm9yIGJhY2t3YXJkcyBjb21wYXRpYmlsaXR5LlxuICAgICAgICBpZiAoY29udGVudC5wYXlsb2FkICYmIGNvbnRlbnQucGF5bG9hZC5sZW5ndGgpIHtcbiAgICAgICAgICBjb25zdCBzZXROZXh0SW5wdXQgPSBjb250ZW50LnBheWxvYWQuZmlsdGVyKGkgPT4ge1xuICAgICAgICAgICAgcmV0dXJuIChpIGFzIGFueSkuc291cmNlID09PSAnc2V0X25leHRfaW5wdXQnO1xuICAgICAgICAgIH0pWzBdO1xuICAgICAgICAgIGlmIChzZXROZXh0SW5wdXQpIHtcbiAgICAgICAgICAgIGNvbnN0IHRleHQgPSAoc2V0TmV4dElucHV0IGFzIGFueSkudGV4dDtcbiAgICAgICAgICAgIC8vIElnbm9yZSB0aGUgYHJlcGxhY2VgIHZhbHVlIGFuZCBhbHdheXMgc2V0IHRoZSBuZXh0IGNlbGwuXG4gICAgICAgICAgICBjZWxsLm1vZGVsLnZhbHVlLnRleHQgPSB0ZXh0O1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSBlbHNlIGlmICh2YWx1ZSAmJiB2YWx1ZS5jb250ZW50LnN0YXR1cyA9PT0gJ2Vycm9yJykge1xuICAgICAgICBlYWNoKHRoaXMuX2NlbGxzLCAoY2VsbDogQ29kZUNlbGwpID0+IHtcbiAgICAgICAgICBpZiAoY2VsbC5tb2RlbC5leGVjdXRpb25Db3VudCA9PT0gbnVsbCkge1xuICAgICAgICAgICAgY2VsbC5zZXRQcm9tcHQoJycpO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgICBjZWxsLm1vZGVsLmNvbnRlbnRDaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy51cGRhdGUsIHRoaXMpO1xuICAgICAgdGhpcy51cGRhdGUoKTtcbiAgICAgIHRoaXMuX2V4ZWN1dGVkLmVtaXQobmV3IERhdGUoKSk7XG4gICAgfTtcbiAgICBjb25zdCBvbkZhaWx1cmUgPSAoKSA9PiB7XG4gICAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNlbGwubW9kZWwuY29udGVudENoYW5nZWQuZGlzY29ubmVjdCh0aGlzLnVwZGF0ZSwgdGhpcyk7XG4gICAgICB0aGlzLnVwZGF0ZSgpO1xuICAgIH07XG4gICAgcmV0dXJuIENvZGVDZWxsLmV4ZWN1dGUoY2VsbCwgdGhpcy5zZXNzaW9uQ29udGV4dCkudGhlbihcbiAgICAgIG9uU3VjY2VzcyxcbiAgICAgIG9uRmFpbHVyZVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBjb25zb2xlIGJhc2VkIG9uIHRoZSBrZXJuZWwgaW5mby5cbiAgICovXG4gIHByaXZhdGUgX2hhbmRsZUluZm8oaW5mbzogS2VybmVsTWVzc2FnZS5JSW5mb1JlcGx5TXNnWydjb250ZW50J10pOiB2b2lkIHtcbiAgICBpZiAoaW5mby5zdGF0dXMgIT09ICdvaycpIHtcbiAgICAgIHRoaXMuX2Jhbm5lciEubW9kZWwudmFsdWUudGV4dCA9ICdFcnJvciBpbiBnZXR0aW5nIGtlcm5lbCBiYW5uZXInO1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9iYW5uZXIhLm1vZGVsLnZhbHVlLnRleHQgPSBpbmZvLmJhbm5lcjtcbiAgICBjb25zdCBsYW5nID0gaW5mby5sYW5ndWFnZV9pbmZvIGFzIG5iZm9ybWF0LklMYW5ndWFnZUluZm9NZXRhZGF0YTtcbiAgICB0aGlzLl9taW1ldHlwZSA9IHRoaXMuX21pbWVUeXBlU2VydmljZS5nZXRNaW1lVHlwZUJ5TGFuZ3VhZ2UobGFuZyk7XG4gICAgaWYgKHRoaXMucHJvbXB0Q2VsbCkge1xuICAgICAgdGhpcy5wcm9tcHRDZWxsLm1vZGVsLm1pbWVUeXBlID0gdGhpcy5fbWltZXR5cGU7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSB0aGUgb3B0aW9ucyB1c2VkIHRvIGluaXRpYWxpemUgYSBjb2RlIGNlbGwgd2lkZ2V0LlxuICAgKi9cbiAgcHJpdmF0ZSBfY3JlYXRlQ29kZUNlbGxPcHRpb25zKCk6IENvZGVDZWxsLklPcHRpb25zIHtcbiAgICBjb25zdCBjb250ZW50RmFjdG9yeSA9IHRoaXMuY29udGVudEZhY3Rvcnk7XG4gICAgY29uc3QgbW9kZWxGYWN0b3J5ID0gdGhpcy5tb2RlbEZhY3Rvcnk7XG4gICAgY29uc3QgbW9kZWwgPSBtb2RlbEZhY3RvcnkuY3JlYXRlQ29kZUNlbGwoe30pO1xuICAgIGNvbnN0IHJlbmRlcm1pbWUgPSB0aGlzLnJlbmRlcm1pbWU7XG4gICAgcmV0dXJuIHsgbW9kZWwsIHJlbmRlcm1pbWUsIGNvbnRlbnRGYWN0b3J5LCBwbGFjZWhvbGRlcjogZmFsc2UgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgY2VsbCBkaXNwb3NlZCBzaWduYWxzLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25DZWxsRGlzcG9zZWQoc2VuZGVyOiBDZWxsLCBhcmdzOiB2b2lkKTogdm9pZCB7XG4gICAgaWYgKCF0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHRoaXMuX2NlbGxzLnJlbW92ZVZhbHVlKHNlbmRlcik7XG4gICAgICBjb25zdCBtc2dJZCA9IHRoaXMuX21zZ0lkQ2VsbHMuZ2V0KHNlbmRlciBhcyBDb2RlQ2VsbCk7XG4gICAgICBpZiAobXNnSWQpIHtcbiAgICAgICAgdGhpcy5fbXNnSWRDZWxscy5kZWxldGUoc2VuZGVyIGFzIENvZGVDZWxsKTtcbiAgICAgICAgdGhpcy5fbXNnSWRzLmRlbGV0ZShtc2dJZCk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFRlc3Qgd2hldGhlciB3ZSBzaG91bGQgZXhlY3V0ZSB0aGUgcHJvbXB0IGNlbGwuXG4gICAqL1xuICBwcml2YXRlIF9zaG91bGRFeGVjdXRlKHRpbWVvdXQ6IG51bWJlcik6IFByb21pc2U8Ym9vbGVhbj4ge1xuICAgIGNvbnN0IHByb21wdENlbGwgPSB0aGlzLnByb21wdENlbGw7XG4gICAgaWYgKCFwcm9tcHRDZWxsKSB7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKGZhbHNlKTtcbiAgICB9XG4gICAgY29uc3QgbW9kZWwgPSBwcm9tcHRDZWxsLm1vZGVsO1xuICAgIGNvbnN0IGNvZGUgPSBtb2RlbC52YWx1ZS50ZXh0O1xuICAgIHJldHVybiBuZXcgUHJvbWlzZTxib29sZWFuPigocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICBjb25zdCB0aW1lciA9IHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgICByZXNvbHZlKHRydWUpO1xuICAgICAgfSwgdGltZW91dCk7XG4gICAgICBjb25zdCBrZXJuZWwgPSB0aGlzLnNlc3Npb25Db250ZXh0LnNlc3Npb24/Lmtlcm5lbDtcbiAgICAgIGlmICgha2VybmVsKSB7XG4gICAgICAgIHJlc29sdmUoZmFsc2UpO1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBrZXJuZWxcbiAgICAgICAgLnJlcXVlc3RJc0NvbXBsZXRlKHsgY29kZSB9KVxuICAgICAgICAudGhlbihpc0NvbXBsZXRlID0+IHtcbiAgICAgICAgICBjbGVhclRpbWVvdXQodGltZXIpO1xuICAgICAgICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgICAgICAgIHJlc29sdmUoZmFsc2UpO1xuICAgICAgICAgIH1cbiAgICAgICAgICBpZiAoaXNDb21wbGV0ZS5jb250ZW50LnN0YXR1cyAhPT0gJ2luY29tcGxldGUnKSB7XG4gICAgICAgICAgICByZXNvbHZlKHRydWUpO1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgIH1cbiAgICAgICAgICByZXNvbHZlKGZhbHNlKTtcbiAgICAgICAgfSlcbiAgICAgICAgLmNhdGNoKCgpID0+IHtcbiAgICAgICAgICByZXNvbHZlKHRydWUpO1xuICAgICAgICB9KTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBrZXlkb3duIGV2ZW50IG9uIGFuIGVkaXRvci5cbiAgICovXG4gIHByaXZhdGUgX29uRWRpdG9yS2V5ZG93bihlZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvciwgZXZlbnQ6IEtleWJvYXJkRXZlbnQpIHtcbiAgICAvLyBTdXBwcmVzcyBcIkVudGVyXCIgZXZlbnRzLlxuICAgIHJldHVybiBldmVudC5rZXlDb2RlID09PSAxMztcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIGtlcm5lbC5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX29uS2VybmVsQ2hhbmdlZCgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICB0aGlzLmNsZWFyKCk7XG4gICAgaWYgKHRoaXMuX2Jhbm5lcikge1xuICAgICAgdGhpcy5fYmFubmVyLmRpc3Bvc2UoKTtcbiAgICAgIHRoaXMuX2Jhbm5lciA9IG51bGw7XG4gICAgfVxuICAgIHRoaXMuYWRkQmFubmVyKCk7XG4gICAgaWYgKHRoaXMuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbj8ua2VybmVsKSB7XG4gICAgICB0aGlzLl9oYW5kbGVJbmZvKGF3YWl0IHRoaXMuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbi5rZXJuZWwuaW5mbyk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUga2VybmVsIHN0YXR1cy5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX29uS2VybmVsU3RhdHVzQ2hhbmdlZCgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCBrZXJuZWwgPSB0aGlzLnNlc3Npb25Db250ZXh0LnNlc3Npb24/Lmtlcm5lbDtcbiAgICBpZiAoa2VybmVsPy5zdGF0dXMgPT09ICdyZXN0YXJ0aW5nJykge1xuICAgICAgdGhpcy5hZGRCYW5uZXIoKTtcbiAgICAgIHRoaXMuX2hhbmRsZUluZm8oYXdhaXQga2VybmVsPy5pbmZvKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9iYW5uZXI6IFJhd0NlbGwgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfY2VsbHM6IElPYnNlcnZhYmxlTGlzdDxDZWxsPjtcbiAgcHJpdmF0ZSBfY29udGVudDogUGFuZWw7XG4gIHByaXZhdGUgX2V4ZWN1dGVkID0gbmV3IFNpZ25hbDx0aGlzLCBEYXRlPih0aGlzKTtcbiAgcHJpdmF0ZSBfaGlzdG9yeTogSUNvbnNvbGVIaXN0b3J5O1xuICBwcml2YXRlIF9pbnB1dDogUGFuZWw7XG4gIHByaXZhdGUgX21pbWV0eXBlID0gJ3RleHQveC1pcHl0aG9uJztcbiAgcHJpdmF0ZSBfbWltZVR5cGVTZXJ2aWNlOiBJRWRpdG9yTWltZVR5cGVTZXJ2aWNlO1xuICBwcml2YXRlIF9tc2dJZHMgPSBuZXcgTWFwPHN0cmluZywgQ29kZUNlbGw+KCk7XG4gIHByaXZhdGUgX21zZ0lkQ2VsbHMgPSBuZXcgTWFwPENvZGVDZWxsLCBzdHJpbmc+KCk7XG4gIHByaXZhdGUgX3Byb21wdENlbGxDcmVhdGVkID0gbmV3IFNpZ25hbDx0aGlzLCBDb2RlQ2VsbD4odGhpcyk7XG4gIHByaXZhdGUgX2RyYWdEYXRhOiB7XG4gICAgcHJlc3NYOiBudW1iZXI7XG4gICAgcHJlc3NZOiBudW1iZXI7XG4gICAgaW5kZXg6IG51bWJlcjtcbiAgfSB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9kcmFnOiBEcmFnIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX2ZvY3VzZWRDZWxsOiBDZWxsIHwgbnVsbCA9IG51bGw7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIENvZGVDb25zb2xlIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgQ29kZUNvbnNvbGUge1xuICAvKipcbiAgICogVGhlIGluaXRpYWxpemF0aW9uIG9wdGlvbnMgZm9yIGEgY29uc29sZSB3aWRnZXQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY29udGVudCBmYWN0b3J5IGZvciB0aGUgY29uc29sZSB3aWRnZXQuXG4gICAgICovXG4gICAgY29udGVudEZhY3Rvcnk6IElDb250ZW50RmFjdG9yeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBtb2RlbCBmYWN0b3J5IGZvciB0aGUgY29uc29sZSB3aWRnZXQuXG4gICAgICovXG4gICAgbW9kZWxGYWN0b3J5PzogSU1vZGVsRmFjdG9yeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBtaW1lIHJlbmRlcmVyIGZvciB0aGUgY29uc29sZSB3aWRnZXQuXG4gICAgICovXG4gICAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjbGllbnQgc2Vzc2lvbiBmb3IgdGhlIGNvbnNvbGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIHNlc3Npb25Db250ZXh0OiBJU2Vzc2lvbkNvbnRleHQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2VydmljZSB1c2VkIHRvIGxvb2sgdXAgbWltZSB0eXBlcy5cbiAgICAgKi9cbiAgICBtaW1lVHlwZVNlcnZpY2U6IElFZGl0b3JNaW1lVHlwZVNlcnZpY2U7XG4gIH1cblxuICAvKipcbiAgICogQSBjb250ZW50IGZhY3RvcnkgZm9yIGNvbnNvbGUgY2hpbGRyZW4uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDb250ZW50RmFjdG9yeSBleHRlbmRzIENlbGwuSUNvbnRlbnRGYWN0b3J5IHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgY29kZSBjZWxsIHdpZGdldC5cbiAgICAgKi9cbiAgICBjcmVhdGVDb2RlQ2VsbChvcHRpb25zOiBDb2RlQ2VsbC5JT3B0aW9ucyk6IENvZGVDZWxsO1xuXG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IHJhdyBjZWxsIHdpZGdldC5cbiAgICAgKi9cbiAgICBjcmVhdGVSYXdDZWxsKG9wdGlvbnM6IFJhd0NlbGwuSU9wdGlvbnMpOiBSYXdDZWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIERlZmF1bHQgaW1wbGVtZW50YXRpb24gb2YgYElDb250ZW50RmFjdG9yeWAuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgQ29udGVudEZhY3RvcnlcbiAgICBleHRlbmRzIENlbGwuQ29udGVudEZhY3RvcnlcbiAgICBpbXBsZW1lbnRzIElDb250ZW50RmFjdG9yeSB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IGNvZGUgY2VsbCB3aWRnZXQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSWYgbm8gY2VsbCBjb250ZW50IGZhY3RvcnkgaXMgcGFzc2VkIGluIHdpdGggdGhlIG9wdGlvbnMsIHRoZSBvbmUgb24gdGhlXG4gICAgICogbm90ZWJvb2sgY29udGVudCBmYWN0b3J5IGlzIHVzZWQuXG4gICAgICovXG4gICAgY3JlYXRlQ29kZUNlbGwob3B0aW9uczogQ29kZUNlbGwuSU9wdGlvbnMpOiBDb2RlQ2VsbCB7XG4gICAgICBpZiAoIW9wdGlvbnMuY29udGVudEZhY3RvcnkpIHtcbiAgICAgICAgb3B0aW9ucy5jb250ZW50RmFjdG9yeSA9IHRoaXM7XG4gICAgICB9XG4gICAgICByZXR1cm4gbmV3IENvZGVDZWxsKG9wdGlvbnMpLmluaXRpYWxpemVTdGF0ZSgpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyByYXcgY2VsbCB3aWRnZXQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSWYgbm8gY2VsbCBjb250ZW50IGZhY3RvcnkgaXMgcGFzc2VkIGluIHdpdGggdGhlIG9wdGlvbnMsIHRoZSBvbmUgb24gdGhlXG4gICAgICogbm90ZWJvb2sgY29udGVudCBmYWN0b3J5IGlzIHVzZWQuXG4gICAgICovXG4gICAgY3JlYXRlUmF3Q2VsbChvcHRpb25zOiBSYXdDZWxsLklPcHRpb25zKTogUmF3Q2VsbCB7XG4gICAgICBpZiAoIW9wdGlvbnMuY29udGVudEZhY3RvcnkpIHtcbiAgICAgICAgb3B0aW9ucy5jb250ZW50RmFjdG9yeSA9IHRoaXM7XG4gICAgICB9XG4gICAgICByZXR1cm4gbmV3IFJhd0NlbGwob3B0aW9ucykuaW5pdGlhbGl6ZVN0YXRlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEEgbmFtZXNwYWNlIGZvciB0aGUgY29kZSBjb25zb2xlIGNvbnRlbnQgZmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBuYW1lc3BhY2UgQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIEFuIGluaXRpYWxpemUgb3B0aW9ucyBmb3IgYENvbnRlbnRGYWN0b3J5YC5cbiAgICAgKi9cbiAgICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIGV4dGVuZHMgQ2VsbC5JQ29udGVudEZhY3Rvcnkge31cbiAgfVxuXG4gIC8qKlxuICAgKiBBIGRlZmF1bHQgY29udGVudCBmYWN0b3J5IGZvciB0aGUgY29kZSBjb25zb2xlLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRDb250ZW50RmFjdG9yeTogSUNvbnRlbnRGYWN0b3J5ID0gbmV3IENvbnRlbnRGYWN0b3J5KCk7XG5cbiAgLyoqXG4gICAqIEEgbW9kZWwgZmFjdG9yeSBmb3IgYSBjb25zb2xlIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU1vZGVsRmFjdG9yeSB7XG4gICAgLyoqXG4gICAgICogVGhlIGZhY3RvcnkgZm9yIGNvZGUgY2VsbCBjb250ZW50LlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGNvZGVDZWxsQ29udGVudEZhY3Rvcnk6IENvZGVDZWxsTW9kZWwuSUNvbnRlbnRGYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IGNvZGUgY2VsbC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIG9wdGlvbnMgdXNlZCB0byBjcmVhdGUgdGhlIGNlbGwuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBBIG5ldyBjb2RlIGNlbGwuIElmIGEgc291cmNlIGNlbGwgaXMgcHJvdmlkZWQsIHRoZVxuICAgICAqICAgbmV3IGNlbGwgd2lsbCBiZSBpbml0aWFsaXplZCB3aXRoIHRoZSBkYXRhIGZyb20gdGhlIHNvdXJjZS5cbiAgICAgKi9cbiAgICBjcmVhdGVDb2RlQ2VsbChvcHRpb25zOiBDb2RlQ2VsbE1vZGVsLklPcHRpb25zKTogSUNvZGVDZWxsTW9kZWw7XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgcmF3IGNlbGwuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIHRoZSBjZWxsLlxuICAgICAqXG4gICAgICogQHJldHVybnMgQSBuZXcgcmF3IGNlbGwuIElmIGEgc291cmNlIGNlbGwgaXMgcHJvdmlkZWQsIHRoZVxuICAgICAqICAgbmV3IGNlbGwgd2lsbCBiZSBpbml0aWFsaXplZCB3aXRoIHRoZSBkYXRhIGZyb20gdGhlIHNvdXJjZS5cbiAgICAgKi9cbiAgICBjcmVhdGVSYXdDZWxsKG9wdGlvbnM6IENlbGxNb2RlbC5JT3B0aW9ucyk6IElSYXdDZWxsTW9kZWw7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRlZmF1bHQgaW1wbGVtZW50YXRpb24gb2YgYW4gYElNb2RlbEZhY3RvcnlgLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIE1vZGVsRmFjdG9yeSB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IGNlbGwgbW9kZWwgZmFjdG9yeS5cbiAgICAgKi9cbiAgICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJTW9kZWxGYWN0b3J5T3B0aW9ucyA9IHt9KSB7XG4gICAgICB0aGlzLmNvZGVDZWxsQ29udGVudEZhY3RvcnkgPVxuICAgICAgICBvcHRpb25zLmNvZGVDZWxsQ29udGVudEZhY3RvcnkgfHwgQ29kZUNlbGxNb2RlbC5kZWZhdWx0Q29udGVudEZhY3Rvcnk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGZhY3RvcnkgZm9yIG91dHB1dCBhcmVhIG1vZGVscy5cbiAgICAgKi9cbiAgICByZWFkb25seSBjb2RlQ2VsbENvbnRlbnRGYWN0b3J5OiBDb2RlQ2VsbE1vZGVsLklDb250ZW50RmFjdG9yeTtcblxuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyBjb2RlIGNlbGwuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gc291cmNlIC0gVGhlIGRhdGEgdG8gdXNlIGZvciB0aGUgb3JpZ2luYWwgc291cmNlIGRhdGEuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBBIG5ldyBjb2RlIGNlbGwuIElmIGEgc291cmNlIGNlbGwgaXMgcHJvdmlkZWQsIHRoZVxuICAgICAqICAgbmV3IGNlbGwgd2lsbCBiZSBpbml0aWFsaXplZCB3aXRoIHRoZSBkYXRhIGZyb20gdGhlIHNvdXJjZS5cbiAgICAgKiAgIElmIHRoZSBjb250ZW50RmFjdG9yeSBpcyBub3QgcHJvdmlkZWQsIHRoZSBpbnN0YW5jZVxuICAgICAqICAgYGNvZGVDZWxsQ29udGVudEZhY3RvcnlgIHdpbGwgYmUgdXNlZC5cbiAgICAgKi9cbiAgICBjcmVhdGVDb2RlQ2VsbChvcHRpb25zOiBDb2RlQ2VsbE1vZGVsLklPcHRpb25zKTogSUNvZGVDZWxsTW9kZWwge1xuICAgICAgaWYgKCFvcHRpb25zLmNvbnRlbnRGYWN0b3J5KSB7XG4gICAgICAgIG9wdGlvbnMuY29udGVudEZhY3RvcnkgPSB0aGlzLmNvZGVDZWxsQ29udGVudEZhY3Rvcnk7XG4gICAgICB9XG4gICAgICByZXR1cm4gbmV3IENvZGVDZWxsTW9kZWwob3B0aW9ucyk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IHJhdyBjZWxsLlxuICAgICAqXG4gICAgICogQHBhcmFtIHNvdXJjZSAtIFRoZSBkYXRhIHRvIHVzZSBmb3IgdGhlIG9yaWdpbmFsIHNvdXJjZSBkYXRhLlxuICAgICAqXG4gICAgICogQHJldHVybnMgQSBuZXcgcmF3IGNlbGwuIElmIGEgc291cmNlIGNlbGwgaXMgcHJvdmlkZWQsIHRoZVxuICAgICAqICAgbmV3IGNlbGwgd2lsbCBiZSBpbml0aWFsaXplZCB3aXRoIHRoZSBkYXRhIGZyb20gdGhlIHNvdXJjZS5cbiAgICAgKi9cbiAgICBjcmVhdGVSYXdDZWxsKG9wdGlvbnM6IENlbGxNb2RlbC5JT3B0aW9ucyk6IElSYXdDZWxsTW9kZWwge1xuICAgICAgcmV0dXJuIG5ldyBSYXdDZWxsTW9kZWwob3B0aW9ucyk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gaW5pdGlhbGl6ZSBhIGBNb2RlbEZhY3RvcnlgLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTW9kZWxGYWN0b3J5T3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGZhY3RvcnkgZm9yIG91dHB1dCBhcmVhIG1vZGVscy5cbiAgICAgKi9cbiAgICBjb2RlQ2VsbENvbnRlbnRGYWN0b3J5PzogQ29kZUNlbGxNb2RlbC5JQ29udGVudEZhY3Rvcnk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRlZmF1bHQgYE1vZGVsRmFjdG9yeWAgaW5zdGFuY2UuXG4gICAqL1xuICBleHBvcnQgY29uc3QgZGVmYXVsdE1vZGVsRmFjdG9yeSA9IG5ldyBNb2RlbEZhY3Rvcnkoe30pO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBjb25zb2xlIHdpZGdldCBwcml2YXRlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIEp1bXAgdG8gdGhlIGJvdHRvbSBvZiBhIG5vZGUuXG4gICAqXG4gICAqIEBwYXJhbSBub2RlIC0gVGhlIHNjcm9sbGFibGUgZWxlbWVudC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBzY3JvbGxUb0JvdHRvbShub2RlOiBIVE1MRWxlbWVudCk6IHZvaWQge1xuICAgIG5vZGUuc2Nyb2xsVG9wID0gbm9kZS5zY3JvbGxIZWlnaHQgLSBub2RlLmNsaWVudEhlaWdodDtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==