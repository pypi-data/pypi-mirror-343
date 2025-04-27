(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_logconsole_lib_index_js"],{

/***/ "../packages/logconsole/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/logconsole/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LogOutputModel": () => (/* reexport safe */ _logger__WEBPACK_IMPORTED_MODULE_0__.LogOutputModel),
/* harmony export */   "Logger": () => (/* reexport safe */ _logger__WEBPACK_IMPORTED_MODULE_0__.Logger),
/* harmony export */   "LoggerOutputAreaModel": () => (/* reexport safe */ _logger__WEBPACK_IMPORTED_MODULE_0__.LoggerOutputAreaModel),
/* harmony export */   "LoggerRegistry": () => (/* reexport safe */ _registry__WEBPACK_IMPORTED_MODULE_1__.LoggerRegistry),
/* harmony export */   "ILoggerRegistry": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_2__.ILoggerRegistry),
/* harmony export */   "LogConsolePanel": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.LogConsolePanel),
/* harmony export */   "ScrollingWidget": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.ScrollingWidget)
/* harmony export */ });
/* harmony import */ var _logger__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./logger */ "../packages/logconsole/lib/logger.js");
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./registry */ "../packages/logconsole/lib/registry.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "../packages/logconsole/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widget */ "../packages/logconsole/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module logconsole
 */






/***/ }),

/***/ "../packages/logconsole/lib/logger.js":
/*!********************************************!*\
  !*** ../packages/logconsole/lib/logger.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LogOutputModel": () => (/* binding */ LogOutputModel),
/* harmony export */   "LoggerOutputAreaModel": () => (/* binding */ LoggerOutputAreaModel),
/* harmony export */   "Logger": () => (/* binding */ Logger)
/* harmony export */ });
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __rest = (undefined && undefined.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};



/**
 * Log Output Model with timestamp which provides
 * item information for Output Area Model.
 */
class LogOutputModel extends _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.OutputModel {
    /**
     * Construct a LogOutputModel.
     *
     * @param options - The model initialization options.
     */
    constructor(options) {
        super(options);
        this.timestamp = new Date(options.value.timestamp);
        this.level = options.value.level;
    }
}
/**
 * Implementation of `IContentFactory` for Output Area Model
 * which creates LogOutputModel instances.
 */
class LogConsoleModelContentFactory extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputAreaModel.ContentFactory {
    /**
     * Create a rendermime output model from notebook output.
     */
    createOutputModel(options) {
        return new LogOutputModel(options);
    }
}
/**
 * Output Area Model implementation which is able to
 * limit number of outputs stored.
 */
class LoggerOutputAreaModel extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputAreaModel {
    constructor(_a) {
        var { maxLength } = _a, options = __rest(_a, ["maxLength"]);
        super(options);
        this.maxLength = maxLength;
    }
    /**
     * Add an output, which may be combined with previous output.
     *
     * @returns The total number of outputs.
     *
     * #### Notes
     * The output bundle is copied. Contiguous stream outputs of the same `name`
     * are combined. The oldest outputs are possibly removed to ensure the total
     * number of outputs is at most `.maxLength`.
     */
    add(output) {
        super.add(output);
        this._applyMaxLength();
        return this.length;
    }
    /**
     * Whether an output should combine with the previous output.
     *
     * We combine if the two outputs are in the same second, which is the
     * resolution for our time display.
     */
    shouldCombine(options) {
        const { value, lastModel } = options;
        const oldSeconds = Math.trunc(lastModel.timestamp.getTime() / 1000);
        const newSeconds = Math.trunc(value.timestamp / 1000);
        return oldSeconds === newSeconds;
    }
    /**
     * Get an item at the specified index.
     */
    get(index) {
        return super.get(index);
    }
    /**
     * Maximum number of outputs to store in the model.
     */
    get maxLength() {
        return this._maxLength;
    }
    set maxLength(value) {
        this._maxLength = value;
        this._applyMaxLength();
    }
    /**
     * Manually apply length limit.
     */
    _applyMaxLength() {
        if (this.list.length > this._maxLength) {
            this.list.removeRange(0, this.list.length - this._maxLength);
        }
    }
}
/**
 * A concrete implementation of ILogger.
 */
class Logger {
    /**
     * Construct a Logger.
     *
     * @param source - The name of the log source.
     */
    constructor(options) {
        this._isDisposed = false;
        this._contentChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._rendermime = null;
        this._version = 0;
        this._level = 'warning';
        this.source = options.source;
        this.outputAreaModel = new LoggerOutputAreaModel({
            contentFactory: new LogConsoleModelContentFactory(),
            maxLength: options.maxLength
        });
    }
    /**
     * The maximum number of outputs stored.
     *
     * #### Notes
     * Oldest entries will be trimmed to ensure the length is at most
     * `.maxLength`.
     */
    get maxLength() {
        return this.outputAreaModel.maxLength;
    }
    set maxLength(value) {
        this.outputAreaModel.maxLength = value;
    }
    /**
     * The level of outputs logged
     */
    get level() {
        return this._level;
    }
    set level(newValue) {
        const oldValue = this._level;
        if (oldValue === newValue) {
            return;
        }
        this._level = newValue;
        this._log({
            output: {
                output_type: 'display_data',
                data: {
                    'text/plain': `Log level set to ${newValue}`
                }
            },
            level: 'metadata'
        });
        this._stateChanged.emit({ name: 'level', oldValue, newValue });
    }
    /**
     * Number of outputs logged.
     */
    get length() {
        return this.outputAreaModel.length;
    }
    /**
     * A signal emitted when the list of log messages changes.
     */
    get contentChanged() {
        return this._contentChanged;
    }
    /**
     * A signal emitted when the log state changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * Rendermime to use when rendering outputs logged.
     */
    get rendermime() {
        return this._rendermime;
    }
    set rendermime(value) {
        if (value !== this._rendermime) {
            const oldValue = this._rendermime;
            const newValue = (this._rendermime = value);
            this._stateChanged.emit({ name: 'rendermime', oldValue, newValue });
        }
    }
    /**
     * The number of messages that have ever been stored.
     */
    get version() {
        return this._version;
    }
    /**
     * Log an output to logger.
     *
     * @param log - The output to be logged.
     */
    log(log) {
        // Filter by our current log level
        if (Private.LogLevel[log.level] <
            Private.LogLevel[this._level]) {
            return;
        }
        let output = null;
        switch (log.type) {
            case 'text':
                output = {
                    output_type: 'display_data',
                    data: {
                        'text/plain': log.data
                    }
                };
                break;
            case 'html':
                output = {
                    output_type: 'display_data',
                    data: {
                        'text/html': log.data
                    }
                };
                break;
            case 'output':
                output = log.data;
                break;
            default:
                break;
        }
        if (output) {
            this._log({
                output,
                level: log.level
            });
        }
    }
    /**
     * Clear all outputs logged.
     */
    clear() {
        this.outputAreaModel.clear(false);
        this._contentChanged.emit('clear');
    }
    /**
     * Add a checkpoint to the log.
     */
    checkpoint() {
        this._log({
            output: {
                output_type: 'display_data',
                data: {
                    'text/html': '<hr/>'
                }
            },
            level: 'metadata'
        });
    }
    /**
     * Whether the logger is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the logger.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.clear();
        this._rendermime = null;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
    _log(options) {
        // First, make sure our version reflects the new message so things
        // triggering from the signals below have the correct version.
        this._version++;
        // Next, trigger any displays of the message
        this.outputAreaModel.add(Object.assign(Object.assign({}, options.output), { timestamp: Date.now(), level: options.level }));
        // Finally, tell people that the message was appended (and possibly
        // already displayed).
        this._contentChanged.emit('append');
    }
}
var Private;
(function (Private) {
    let LogLevel;
    (function (LogLevel) {
        LogLevel[LogLevel["debug"] = 0] = "debug";
        LogLevel[LogLevel["info"] = 1] = "info";
        LogLevel[LogLevel["warning"] = 2] = "warning";
        LogLevel[LogLevel["error"] = 3] = "error";
        LogLevel[LogLevel["critical"] = 4] = "critical";
        LogLevel[LogLevel["metadata"] = 5] = "metadata";
    })(LogLevel = Private.LogLevel || (Private.LogLevel = {}));
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/logconsole/lib/registry.js":
/*!**********************************************!*\
  !*** ../packages/logconsole/lib/registry.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LoggerRegistry": () => (/* binding */ LoggerRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _logger__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./logger */ "../packages/logconsole/lib/logger.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A concrete implementation of ILoggerRegistry.
 */
class LoggerRegistry {
    /**
     * Construct a LoggerRegistry.
     *
     * @param defaultRendermime - Default rendermime to render outputs
     * with when logger is not supplied with one.
     */
    constructor(options) {
        this._loggers = new Map();
        this._registryChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._isDisposed = false;
        this._defaultRendermime = options.defaultRendermime;
        this._maxLength = options.maxLength;
    }
    /**
     * Get the logger for the specified source.
     *
     * @param source - The name of the log source.
     *
     * @returns The logger for the specified source.
     */
    getLogger(source) {
        const loggers = this._loggers;
        let logger = loggers.get(source);
        if (logger) {
            return logger;
        }
        logger = new _logger__WEBPACK_IMPORTED_MODULE_1__.Logger({ source, maxLength: this.maxLength });
        logger.rendermime = this._defaultRendermime;
        loggers.set(source, logger);
        this._registryChanged.emit('append');
        return logger;
    }
    /**
     * Get all loggers registered.
     *
     * @returns The array containing all registered loggers.
     */
    getLoggers() {
        return Array.from(this._loggers.values());
    }
    /**
     * A signal emitted when the logger registry changes.
     */
    get registryChanged() {
        return this._registryChanged;
    }
    /**
     * The max length for loggers.
     */
    get maxLength() {
        return this._maxLength;
    }
    set maxLength(value) {
        this._maxLength = value;
        this._loggers.forEach(logger => {
            logger.maxLength = value;
        });
    }
    /**
     * Whether the register is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the registry and all loggers.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._loggers.forEach(x => x.dispose());
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "../packages/logconsole/lib/tokens.js":
/*!********************************************!*\
  !*** ../packages/logconsole/lib/tokens.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ILoggerRegistry": () => (/* binding */ ILoggerRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The Logger Registry token.
 */
const ILoggerRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/logconsole:ILoggerRegistry');


/***/ }),

/***/ "../packages/logconsole/lib/widget.js":
/*!********************************************!*\
  !*** ../packages/logconsole/lib/widget.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ScrollingWidget": () => (/* binding */ ScrollingWidget),
/* harmony export */   "LogConsolePanel": () => (/* binding */ LogConsolePanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __rest = (undefined && undefined.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};




function toTitleCase(value) {
    return value.length === 0 ? value : value[0].toUpperCase() + value.slice(1);
}
/**
 * Log console output prompt implementation
 */
class LogConsoleOutputPrompt extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor() {
        super();
        this._timestampNode = document.createElement('div');
        this.node.append(this._timestampNode);
    }
    /**
     * Date & time when output is logged.
     */
    set timestamp(value) {
        this._timestamp = value;
        this._timestampNode.innerHTML = this._timestamp.toLocaleTimeString();
        this.update();
    }
    /**
     * Log level
     */
    set level(value) {
        this._level = value;
        this.node.dataset.logLevel = value;
        this.update();
    }
    update() {
        if (this._level !== undefined && this._timestamp !== undefined) {
            this.node.title = `${this._timestamp.toLocaleString()}; ${toTitleCase(this._level)} level`;
        }
    }
}
/**
 * Output Area implementation displaying log outputs
 * with prompts showing log timestamps.
 */
class LogConsoleOutputArea extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputArea {
    /**
     * Create an output item with a prompt and actual output
     */
    createOutputItem(model) {
        const panel = super.createOutputItem(model);
        if (panel === null) {
            // Could not render model
            return null;
        }
        // first widget in panel is prompt of type LoggerOutputPrompt
        const prompt = panel.widgets[0];
        prompt.timestamp = model.timestamp;
        prompt.level = model.level;
        return panel;
    }
    /**
     * Handle an input request from a kernel by doing nothing.
     */
    onInputRequest(msg, future) {
        return;
    }
}
/**
 * Implementation of `IContentFactory` for Output Area
 * which creates custom output prompts.
 */
class LogConsoleContentFactory extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputArea.ContentFactory {
    /**
     * Create the output prompt for the widget.
     */
    createOutputPrompt() {
        return new LogConsoleOutputPrompt();
    }
}
/**
 * Implements a panel which supports pinning the position to the end if it is
 * scrolled to the end.
 *
 * #### Notes
 * This is useful for log viewing components or chat components that append
 * elements at the end. We would like to automatically scroll when the user
 * has scrolled to the bottom, but not change the scrolling when the user has
 * changed the scroll position.
 */
class ScrollingWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor(_a) {
        var { content } = _a, options = __rest(_a, ["content"]);
        super(options);
        this._observer = null;
        this.addClass('jp-Scrolling');
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.PanelLayout());
        layout.addWidget(content);
        this._content = content;
        this._sentinel = document.createElement('div');
        this.node.appendChild(this._sentinel);
    }
    /**
     * The content widget.
     */
    get content() {
        return this._content;
    }
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        // defer so content gets a chance to attach first
        requestAnimationFrame(() => {
            this._sentinel.scrollIntoView();
            this._scrollHeight = this.node.scrollHeight;
        });
        // Set up intersection observer for the sentinel
        if (typeof IntersectionObserver !== 'undefined') {
            this._observer = new IntersectionObserver(args => {
                this._handleScroll(args);
            }, { root: this.node, threshold: 1 });
            this._observer.observe(this._sentinel);
        }
    }
    onBeforeDetach(msg) {
        if (this._observer) {
            this._observer.disconnect();
        }
    }
    onAfterShow(msg) {
        if (this._tracking) {
            this._sentinel.scrollIntoView();
        }
    }
    _handleScroll([entry]) {
        if (entry.isIntersecting) {
            this._tracking = true;
        }
        else if (this.isVisible) {
            const currentHeight = this.node.scrollHeight;
            if (currentHeight === this._scrollHeight) {
                // Likely the user scrolled manually
                this._tracking = false;
            }
            else {
                // We assume we scrolled because our size changed, so scroll to the end.
                this._sentinel.scrollIntoView();
                this._scrollHeight = currentHeight;
                this._tracking = true;
            }
        }
    }
}
/**
 * A StackedPanel implementation that creates Output Areas
 * for each log source and activates as source is switched.
 */
class LogConsolePanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.StackedPanel {
    /**
     * Construct a LogConsolePanel instance.
     *
     * @param loggerRegistry - The logger registry that provides
     * logs to be displayed.
     */
    constructor(loggerRegistry, translator) {
        super();
        this._outputAreas = new Map();
        this._source = null;
        this._sourceChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._sourceDisplayed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._loggersWatched = new Set();
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._loggerRegistry = loggerRegistry;
        this.addClass('jp-LogConsolePanel');
        loggerRegistry.registryChanged.connect((sender, args) => {
            this._bindLoggerSignals();
        }, this);
        this._bindLoggerSignals();
        this._placeholder = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget();
        this._placeholder.addClass('jp-LogConsoleListPlaceholder');
        this.addWidget(this._placeholder);
    }
    /**
     * The logger registry providing the logs.
     */
    get loggerRegistry() {
        return this._loggerRegistry;
    }
    /**
     * The current logger.
     */
    get logger() {
        if (this.source === null) {
            return null;
        }
        return this.loggerRegistry.getLogger(this.source);
    }
    /**
     * The log source displayed
     */
    get source() {
        return this._source;
    }
    set source(name) {
        if (name === this._source) {
            return;
        }
        const oldValue = this._source;
        const newValue = (this._source = name);
        this._showOutputFromSource(newValue);
        this._handlePlaceholder();
        this._sourceChanged.emit({ oldValue, newValue, name: 'source' });
    }
    /**
     * The source version displayed.
     */
    get sourceVersion() {
        const source = this.source;
        return source !== null
            ? this._loggerRegistry.getLogger(source).version
            : null;
    }
    /**
     * Signal for source changes
     */
    get sourceChanged() {
        return this._sourceChanged;
    }
    /**
     * Signal for source changes
     */
    get sourceDisplayed() {
        return this._sourceDisplayed;
    }
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        this._updateOutputAreas();
        this._showOutputFromSource(this._source);
        this._handlePlaceholder();
    }
    onAfterShow(msg) {
        super.onAfterShow(msg);
        if (this.source !== null) {
            this._sourceDisplayed.emit({
                source: this.source,
                version: this.sourceVersion
            });
        }
    }
    _bindLoggerSignals() {
        const loggers = this._loggerRegistry.getLoggers();
        for (const logger of loggers) {
            if (this._loggersWatched.has(logger.source)) {
                continue;
            }
            logger.contentChanged.connect((sender, args) => {
                this._updateOutputAreas();
                this._handlePlaceholder();
            }, this);
            logger.stateChanged.connect((sender, change) => {
                if (change.name !== 'rendermime') {
                    return;
                }
                const viewId = `source:${sender.source}`;
                const outputArea = this._outputAreas.get(viewId);
                if (outputArea) {
                    if (change.newValue) {
                        // cast away readonly
                        outputArea.rendermime = change.newValue;
                    }
                    else {
                        outputArea.dispose();
                    }
                }
            }, this);
            this._loggersWatched.add(logger.source);
        }
    }
    _showOutputFromSource(source) {
        // If the source is null, pick a unique name so all output areas hide.
        const viewId = source === null ? 'null source' : `source:${source}`;
        this._outputAreas.forEach((outputArea, name) => {
            var _a, _b;
            // Show/hide the output area parents, the scrolling windows.
            if (outputArea.id === viewId) {
                (_a = outputArea.parent) === null || _a === void 0 ? void 0 : _a.show();
                if (outputArea.isVisible) {
                    this._sourceDisplayed.emit({
                        source: this.source,
                        version: this.sourceVersion
                    });
                }
            }
            else {
                (_b = outputArea.parent) === null || _b === void 0 ? void 0 : _b.hide();
            }
        });
        const title = source === null
            ? this._trans.__('Log Console')
            : this._trans.__('Log: %1', source);
        this.title.label = title;
        this.title.caption = title;
    }
    _handlePlaceholder() {
        if (this.source === null) {
            this._placeholder.node.textContent = this._trans.__('No source selected.');
            this._placeholder.show();
        }
        else if (this._loggerRegistry.getLogger(this.source).length === 0) {
            this._placeholder.node.textContent = this._trans.__('No log messages.');
            this._placeholder.show();
        }
        else {
            this._placeholder.hide();
            this._placeholder.node.textContent = '';
        }
    }
    _updateOutputAreas() {
        const loggerIds = new Set();
        const loggers = this._loggerRegistry.getLoggers();
        for (const logger of loggers) {
            const source = logger.source;
            const viewId = `source:${source}`;
            loggerIds.add(viewId);
            // add view for logger if not exist
            if (!this._outputAreas.has(viewId)) {
                const outputArea = new LogConsoleOutputArea({
                    rendermime: logger.rendermime,
                    contentFactory: new LogConsoleContentFactory(),
                    model: logger.outputAreaModel
                });
                outputArea.id = viewId;
                // Attach the output area so it is visible, so the accounting
                // functions below record the outputs actually displayed.
                const w = new ScrollingWidget({
                    content: outputArea
                });
                this.addWidget(w);
                this._outputAreas.set(viewId, outputArea);
                // This is where the source object is associated with the output area.
                // We capture the source from this environment in the closure.
                const outputUpdate = (sender) => {
                    // If the current log console panel source is the source associated
                    // with this output area, and the output area is visible, then emit
                    // the logConsolePanel source displayed signal.
                    if (this.source === source && sender.isVisible) {
                        // We assume that the output area has been updated to the current
                        // version of the source.
                        this._sourceDisplayed.emit({
                            source: this.source,
                            version: this.sourceVersion
                        });
                    }
                };
                // Notify messages were displayed any time the output area is updated
                // and update for any outputs rendered on construction.
                outputArea.outputLengthChanged.connect(outputUpdate, this);
                // Since the output area was attached above, we can rely on its
                // visibility to account for the messages displayed.
                outputUpdate(outputArea);
            }
        }
        // remove output areas that do not have corresponding loggers anymore
        const viewIds = this._outputAreas.keys();
        for (const viewId of viewIds) {
            if (!loggerIds.has(viewId)) {
                const outputArea = this._outputAreas.get(viewId);
                outputArea === null || outputArea === void 0 ? void 0 : outputArea.dispose();
                this._outputAreas.delete(viewId);
            }
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbG9nY29uc29sZS9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2xvZ2NvbnNvbGUvc3JjL2xvZ2dlci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbG9nY29uc29sZS9zcmMvcmVnaXN0cnkudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2xvZ2NvbnNvbGUvc3JjL3Rva2Vucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbG9nY29uc29sZS9zcmMvd2lkZ2V0LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFFc0I7QUFDRTtBQUNGO0FBQ0E7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1Z6QiwwQ0FBMEM7QUFDMUMsMkRBQTJEOzs7Ozs7Ozs7Ozs7QUFHZ0I7QUFLM0M7QUFDb0I7QUEwQ3BEOzs7R0FHRztBQUNJLE1BQU0sY0FBZSxTQUFRLCtEQUFXO0lBQzdDOzs7O09BSUc7SUFDSCxZQUFZLE9BQWdDO1FBQzFDLEtBQUssQ0FBQyxPQUFPLENBQUMsQ0FBQztRQUVmLElBQUksQ0FBQyxTQUFTLEdBQUcsSUFBSSxJQUFJLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxTQUFTLENBQUMsQ0FBQztRQUNuRCxJQUFJLENBQUMsS0FBSyxHQUFHLE9BQU8sQ0FBQyxLQUFLLENBQUMsS0FBSyxDQUFDO0lBQ25DLENBQUM7Q0FXRjtBQVdEOzs7R0FHRztBQUNILE1BQU0sNkJBQThCLFNBQVEsa0ZBQThCO0lBQ3hFOztPQUVHO0lBQ0gs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QUMsQ0FBQztnQkFDM0QsK0RBQStEO2dCQUMvRCxvREFBb0Q7Z0JBQ3BELFlBQVksQ0FBQyxVQUFVLENBQUMsQ0FBQzthQUMxQjtTQUNGO1FBRUQscUVBQXFFO1FBQ3JFLE1BQU0sT0FBTyxHQUFHLElBQUksQ0FBQyxZQUFZLENBQUMsSUFBSSxFQUFFLENBQUM7UUFFekMsS0FBSyxNQUFNLE1BQU0sSUFBSSxPQUFPLEVBQUU7WUFDNUIsSUFBSSxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLEVBQUU7Z0JBQzFCLE1BQU0sVUFBVSxHQUFHLElBQUksQ0FBQyxZQUFZLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQyxDQUFDO2dCQUNqRCxVQUFVLGFBQVYsVUFBVSx1QkFBVixVQUFVLENBQUUsT0FBTyxHQUFHO2dCQUN0QixJQUFJLENBQUMsWUFBWSxDQUFDLE1BQU0sQ0FBQyxNQUFNLENBQUMsQ0FBQzthQUNsQztTQUNGO0lBQ0gsQ0FBQztDQWNGIiwiZmlsZSI6InBhY2thZ2VzX2xvZ2NvbnNvbGVfbGliX2luZGV4X2pzLjZlMWVkMDI5Mzk4ZGQ1NmUxMWNlLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbG9nY29uc29sZVxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vbG9nZ2VyJztcbmV4cG9ydCAqIGZyb20gJy4vcmVnaXN0cnknO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuZXhwb3J0ICogZnJvbSAnLi93aWRnZXQnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgKiBhcyBuYmZvcm1hdCBmcm9tICdAanVweXRlcmxhYi9uYmZvcm1hdCc7XG5pbXBvcnQgeyBJT3V0cHV0QXJlYU1vZGVsLCBPdXRwdXRBcmVhTW9kZWwgfSBmcm9tICdAanVweXRlcmxhYi9vdXRwdXRhcmVhJztcbmltcG9ydCB7XG4gIElPdXRwdXRNb2RlbCxcbiAgSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgT3V0cHV0TW9kZWxcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQge1xuICBJQ29udGVudENoYW5nZSxcbiAgSUxvZ2dlcixcbiAgSUxvZ2dlck91dHB1dEFyZWFNb2RlbCxcbiAgSUxvZ1BheWxvYWQsXG4gIElTdGF0ZUNoYW5nZSxcbiAgTG9nTGV2ZWxcbn0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEFsbCBzZXZlcml0eSBsZXZlbHMsIGluY2x1ZGluZyBhbiBpbnRlcm5hbCBvbmUgZm9yIG1ldGFkYXRhLlxuICovXG50eXBlIEZ1bGxMb2dMZXZlbCA9IExvZ0xldmVsIHwgJ21ldGFkYXRhJztcblxuLyoqXG4gKiBDdXN0b20gTm90ZWJvb2sgT3V0cHV0IHdpdGggbG9nIGluZm8uXG4gKi9cbnR5cGUgSUxvZ091dHB1dCA9IG5iZm9ybWF0LklPdXRwdXQgJiB7XG4gIC8qKlxuICAgKiBEYXRlICYgdGltZSB3aGVuIG91dHB1dCBpcyBsb2dnZWQgaW4gaW50ZWdlciByZXByZXNlbnRhdGlvbi5cbiAgICovXG4gIHRpbWVzdGFtcDogbnVtYmVyO1xuXG4gIC8qKlxuICAgKiBMb2cgbGV2ZWxcbiAgICovXG4gIGxldmVsOiBGdWxsTG9nTGV2ZWw7XG59O1xuXG5leHBvcnQgaW50ZXJmYWNlIElMb2dPdXRwdXRNb2RlbCBleHRlbmRzIElPdXRwdXRNb2RlbCB7XG4gIC8qKlxuICAgKiBEYXRlICYgdGltZSB3aGVuIG91dHB1dCBpcyBsb2dnZWQuXG4gICAqL1xuICByZWFkb25seSB0aW1lc3RhbXA6IERhdGU7XG5cbiAgLyoqXG4gICAqIExvZyBsZXZlbFxuICAgKi9cbiAgcmVhZG9ubHkgbGV2ZWw6IEZ1bGxMb2dMZXZlbDtcbn1cblxuLyoqXG4gKiBMb2cgT3V0cHV0IE1vZGVsIHdpdGggdGltZXN0YW1wIHdoaWNoIHByb3ZpZGVzXG4gKiBpdGVtIGluZm9ybWF0aW9uIGZvciBPdXRwdXQgQXJlYSBNb2RlbC5cbiAqL1xuZXhwb3J0IGNsYXNzIExvZ091dHB1dE1vZGVsIGV4dGVuZHMgT3V0cHV0TW9kZWwgaW1wbGVtZW50cyBJTG9nT3V0cHV0TW9kZWwge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgTG9nT3V0cHV0TW9kZWwuXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIG1vZGVsIGluaXRpYWxpemF0aW9uIG9wdGlvbnMuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBMb2dPdXRwdXRNb2RlbC5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuXG4gICAgdGhpcy50aW1lc3RhbXAgPSBuZXcgRGF0ZShvcHRpb25zLnZhbHVlLnRpbWVzdGFtcCk7XG4gICAgdGhpcy5sZXZlbCA9IG9wdGlvbnMudmFsdWUubGV2ZWw7XG4gIH1cblxuICAvKipcbiAgICogRGF0ZSAmIHRpbWUgd2hlbiBvdXRwdXQgaXMgbG9nZ2VkLlxuICAgKi9cbiAgcmVhZG9ubHkgdGltZXN0YW1wOiBEYXRlO1xuXG4gIC8qKlxuICAgKiBMb2cgbGV2ZWxcbiAgICovXG4gIHJlYWRvbmx5IGxldmVsOiBGdWxsTG9nTGV2ZWw7XG59XG5cbi8qKlxuICogTG9nIE91dHB1dCBNb2RlbCBuYW1lc3BhY2UgdGhhdCBkZWZpbmVzIGluaXRpYWxpemF0aW9uIG9wdGlvbnMuXG4gKi9cbm5hbWVzcGFjZSBMb2dPdXRwdXRNb2RlbCB7XG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMgZXh0ZW5kcyBJT3V0cHV0TW9kZWwuSU9wdGlvbnMge1xuICAgIHZhbHVlOiBJTG9nT3V0cHV0O1xuICB9XG59XG5cbi8qKlxuICogSW1wbGVtZW50YXRpb24gb2YgYElDb250ZW50RmFjdG9yeWAgZm9yIE91dHB1dCBBcmVhIE1vZGVsXG4gKiB3aGljaCBjcmVhdGVzIExvZ091dHB1dE1vZGVsIGluc3RhbmNlcy5cbiAqL1xuY2xhc3MgTG9nQ29uc29sZU1vZGVsQ29udGVudEZhY3RvcnkgZXh0ZW5kcyBPdXRwdXRBcmVhTW9kZWwuQ29udGVudEZhY3Rvcnkge1xuICAvKipcbiAgICogQ3JlYXRlIGEgcmVuZGVybWltZSBvdXRwdXQgbW9kZWwgZnJvbSBub3RlYm9vayBvdXRwdXQuXG4gICAqL1xuICBjcmVhdGVPdXRwdXRNb2RlbChvcHRpb25zOiBMb2dPdXRwdXRNb2RlbC5JT3B0aW9ucyk6IExvZ091dHB1dE1vZGVsIHtcbiAgICByZXR1cm4gbmV3IExvZ091dHB1dE1vZGVsKG9wdGlvbnMpO1xuICB9XG59XG5cbi8qKlxuICogT3V0cHV0IEFyZWEgTW9kZWwgaW1wbGVtZW50YXRpb24gd2hpY2ggaXMgYWJsZSB0b1xuICogbGltaXQgbnVtYmVyIG9mIG91dHB1dHMgc3RvcmVkLlxuICovXG5leHBvcnQgY2xhc3MgTG9nZ2VyT3V0cHV0QXJlYU1vZGVsXG4gIGV4dGVuZHMgT3V0cHV0QXJlYU1vZGVsXG4gIGltcGxlbWVudHMgSUxvZ2dlck91dHB1dEFyZWFNb2RlbCB7XG4gIGNvbnN0cnVjdG9yKHsgbWF4TGVuZ3RoLCAuLi5vcHRpb25zIH06IExvZ2dlck91dHB1dEFyZWFNb2RlbC5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICAgIHRoaXMubWF4TGVuZ3RoID0gbWF4TGVuZ3RoO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhbiBvdXRwdXQsIHdoaWNoIG1heSBiZSBjb21iaW5lZCB3aXRoIHByZXZpb3VzIG91dHB1dC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIHRvdGFsIG51bWJlciBvZiBvdXRwdXRzLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBvdXRwdXQgYnVuZGxlIGlzIGNvcGllZC4gQ29udGlndW91cyBzdHJlYW0gb3V0cHV0cyBvZiB0aGUgc2FtZSBgbmFtZWBcbiAgICogYXJlIGNvbWJpbmVkLiBUaGUgb2xkZXN0IG91dHB1dHMgYXJlIHBvc3NpYmx5IHJlbW92ZWQgdG8gZW5zdXJlIHRoZSB0b3RhbFxuICAgKiBudW1iZXIgb2Ygb3V0cHV0cyBpcyBhdCBtb3N0IGAubWF4TGVuZ3RoYC5cbiAgICovXG4gIGFkZChvdXRwdXQ6IElMb2dPdXRwdXQpOiBudW1iZXIge1xuICAgIHN1cGVyLmFkZChvdXRwdXQpO1xuICAgIHRoaXMuX2FwcGx5TWF4TGVuZ3RoKCk7XG4gICAgcmV0dXJuIHRoaXMubGVuZ3RoO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgYW4gb3V0cHV0IHNob3VsZCBjb21iaW5lIHdpdGggdGhlIHByZXZpb3VzIG91dHB1dC5cbiAgICpcbiAgICogV2UgY29tYmluZSBpZiB0aGUgdHdvIG91dHB1dHMgYXJlIGluIHRoZSBzYW1lIHNlY29uZCwgd2hpY2ggaXMgdGhlXG4gICAqIHJlc29sdXRpb24gZm9yIG91ciB0aW1lIGRpc3BsYXkuXG4gICAqL1xuICBwcm90ZWN0ZWQgc2hvdWxkQ29tYmluZShvcHRpb25zOiB7XG4gICAgdmFsdWU6IElMb2dPdXRwdXQ7XG4gICAgbGFzdE1vZGVsOiBJTG9nT3V0cHV0TW9kZWw7XG4gIH0pOiBib29sZWFuIHtcbiAgICBjb25zdCB7IHZhbHVlLCBsYXN0TW9kZWwgfSA9IG9wdGlvbnM7XG5cbiAgICBjb25zdCBvbGRTZWNvbmRzID0gTWF0aC50cnVuYyhsYXN0TW9kZWwudGltZXN0YW1wLmdldFRpbWUoKSAvIDEwMDApO1xuICAgIGNvbnN0IG5ld1NlY29uZHMgPSBNYXRoLnRydW5jKHZhbHVlLnRpbWVzdGFtcCAvIDEwMDApO1xuXG4gICAgcmV0dXJuIG9sZFNlY29uZHMgPT09IG5ld1NlY29uZHM7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGFuIGl0ZW0gYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICovXG4gIGdldChpbmRleDogbnVtYmVyKTogSUxvZ091dHB1dE1vZGVsIHtcbiAgICByZXR1cm4gc3VwZXIuZ2V0KGluZGV4KSBhcyBJTG9nT3V0cHV0TW9kZWw7XG4gIH1cblxuICAvKipcbiAgICogTWF4aW11bSBudW1iZXIgb2Ygb3V0cHV0cyB0byBzdG9yZSBpbiB0aGUgbW9kZWwuXG4gICAqL1xuICBnZXQgbWF4TGVuZ3RoKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX21heExlbmd0aDtcbiAgfVxuICBzZXQgbWF4TGVuZ3RoKHZhbHVlOiBudW1iZXIpIHtcbiAgICB0aGlzLl9tYXhMZW5ndGggPSB2YWx1ZTtcbiAgICB0aGlzLl9hcHBseU1heExlbmd0aCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIE1hbnVhbGx5IGFwcGx5IGxlbmd0aCBsaW1pdC5cbiAgICovXG4gIHByaXZhdGUgX2FwcGx5TWF4TGVuZ3RoKCkge1xuICAgIGlmICh0aGlzLmxpc3QubGVuZ3RoID4gdGhpcy5fbWF4TGVuZ3RoKSB7XG4gICAgICB0aGlzLmxpc3QucmVtb3ZlUmFuZ2UoMCwgdGhpcy5saXN0Lmxlbmd0aCAtIHRoaXMuX21heExlbmd0aCk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfbWF4TGVuZ3RoOiBudW1iZXI7XG59XG5cbmV4cG9ydCBuYW1lc3BhY2UgTG9nZ2VyT3V0cHV0QXJlYU1vZGVsIHtcbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyBleHRlbmRzIElPdXRwdXRBcmVhTW9kZWwuSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBtYXhpbXVtIG51bWJlciBvZiBtZXNzYWdlcyBzdG9yZWQuXG4gICAgICovXG4gICAgbWF4TGVuZ3RoOiBudW1iZXI7XG4gIH1cbn1cblxuLyoqXG4gKiBBIGNvbmNyZXRlIGltcGxlbWVudGF0aW9uIG9mIElMb2dnZXIuXG4gKi9cbmV4cG9ydCBjbGFzcyBMb2dnZXIgaW1wbGVtZW50cyBJTG9nZ2VyIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIExvZ2dlci5cbiAgICpcbiAgICogQHBhcmFtIHNvdXJjZSAtIFRoZSBuYW1lIG9mIHRoZSBsb2cgc291cmNlLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogTG9nZ2VyLklPcHRpb25zKSB7XG4gICAgdGhpcy5zb3VyY2UgPSBvcHRpb25zLnNvdXJjZTtcbiAgICB0aGlzLm91dHB1dEFyZWFNb2RlbCA9IG5ldyBMb2dnZXJPdXRwdXRBcmVhTW9kZWwoe1xuICAgICAgY29udGVudEZhY3Rvcnk6IG5ldyBMb2dDb25zb2xlTW9kZWxDb250ZW50RmFjdG9yeSgpLFxuICAgICAgbWF4TGVuZ3RoOiBvcHRpb25zLm1heExlbmd0aFxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBtYXhpbXVtIG51bWJlciBvZiBvdXRwdXRzIHN0b3JlZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBPbGRlc3QgZW50cmllcyB3aWxsIGJlIHRyaW1tZWQgdG8gZW5zdXJlIHRoZSBsZW5ndGggaXMgYXQgbW9zdFxuICAgKiBgLm1heExlbmd0aGAuXG4gICAqL1xuICBnZXQgbWF4TGVuZ3RoKCkge1xuICAgIHJldHVybiB0aGlzLm91dHB1dEFyZWFNb2RlbC5tYXhMZW5ndGg7XG4gIH1cbiAgc2V0IG1heExlbmd0aCh2YWx1ZTogbnVtYmVyKSB7XG4gICAgdGhpcy5vdXRwdXRBcmVhTW9kZWwubWF4TGVuZ3RoID0gdmFsdWU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGxldmVsIG9mIG91dHB1dHMgbG9nZ2VkXG4gICAqL1xuICBnZXQgbGV2ZWwoKTogTG9nTGV2ZWwge1xuICAgIHJldHVybiB0aGlzLl9sZXZlbDtcbiAgfVxuICBzZXQgbGV2ZWwobmV3VmFsdWU6IExvZ0xldmVsKSB7XG4gICAgY29uc3Qgb2xkVmFsdWUgPSB0aGlzLl9sZXZlbDtcbiAgICBpZiAob2xkVmFsdWUgPT09IG5ld1ZhbHVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2xldmVsID0gbmV3VmFsdWU7XG4gICAgdGhpcy5fbG9nKHtcbiAgICAgIG91dHB1dDoge1xuICAgICAgICBvdXRwdXRfdHlwZTogJ2Rpc3BsYXlfZGF0YScsXG4gICAgICAgIGRhdGE6IHtcbiAgICAgICAgICAndGV4dC9wbGFpbic6IGBMb2cgbGV2ZWwgc2V0IHRvICR7bmV3VmFsdWV9YFxuICAgICAgICB9XG4gICAgICB9LFxuICAgICAgbGV2ZWw6ICdtZXRhZGF0YSdcbiAgICB9KTtcbiAgICB0aGlzLl9zdGF0ZUNoYW5nZWQuZW1pdCh7IG5hbWU6ICdsZXZlbCcsIG9sZFZhbHVlLCBuZXdWYWx1ZSB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBOdW1iZXIgb2Ygb3V0cHV0cyBsb2dnZWQuXG4gICAqL1xuICBnZXQgbGVuZ3RoKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMub3V0cHV0QXJlYU1vZGVsLmxlbmd0aDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGxpc3Qgb2YgbG9nIG1lc3NhZ2VzIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgY29udGVudENoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCBJQ29udGVudENoYW5nZT4ge1xuICAgIHJldHVybiB0aGlzLl9jb250ZW50Q2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGxvZyBzdGF0ZSBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IHN0YXRlQ2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElTdGF0ZUNoYW5nZT4ge1xuICAgIHJldHVybiB0aGlzLl9zdGF0ZUNoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVybWltZSB0byB1c2Ugd2hlbiByZW5kZXJpbmcgb3V0cHV0cyBsb2dnZWQuXG4gICAqL1xuICBnZXQgcmVuZGVybWltZSgpOiBJUmVuZGVyTWltZVJlZ2lzdHJ5IHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuX3JlbmRlcm1pbWU7XG4gIH1cbiAgc2V0IHJlbmRlcm1pbWUodmFsdWU6IElSZW5kZXJNaW1lUmVnaXN0cnkgfCBudWxsKSB7XG4gICAgaWYgKHZhbHVlICE9PSB0aGlzLl9yZW5kZXJtaW1lKSB7XG4gICAgICBjb25zdCBvbGRWYWx1ZSA9IHRoaXMuX3JlbmRlcm1pbWU7XG4gICAgICBjb25zdCBuZXdWYWx1ZSA9ICh0aGlzLl9yZW5kZXJtaW1lID0gdmFsdWUpO1xuICAgICAgdGhpcy5fc3RhdGVDaGFuZ2VkLmVtaXQoeyBuYW1lOiAncmVuZGVybWltZScsIG9sZFZhbHVlLCBuZXdWYWx1ZSB9KTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIG51bWJlciBvZiBtZXNzYWdlcyB0aGF0IGhhdmUgZXZlciBiZWVuIHN0b3JlZC5cbiAgICovXG4gIGdldCB2ZXJzaW9uKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX3ZlcnNpb247XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNvdXJjZSBmb3IgdGhlIGxvZ2dlci5cbiAgICovXG4gIHJlYWRvbmx5IHNvdXJjZTogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBUaGUgb3V0cHV0IGFyZWEgbW9kZWwgdXNlZCBmb3IgdGhlIGxvZ2dlci5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIHdpbGwgdXN1YWxseSBub3QgYmUgYWNjZXNzZWQgZGlyZWN0bHkuIEl0IGlzIGEgcHVibGljIGF0dHJpYnV0ZSBzb1xuICAgKiB0aGF0IHRoZSByZW5kZXJlciBjYW4gYWNjZXNzIGl0LlxuICAgKi9cbiAgcmVhZG9ubHkgb3V0cHV0QXJlYU1vZGVsOiBMb2dnZXJPdXRwdXRBcmVhTW9kZWw7XG5cbiAgLyoqXG4gICAqIExvZyBhbiBvdXRwdXQgdG8gbG9nZ2VyLlxuICAgKlxuICAgKiBAcGFyYW0gbG9nIC0gVGhlIG91dHB1dCB0byBiZSBsb2dnZWQuXG4gICAqL1xuICBsb2cobG9nOiBJTG9nUGF5bG9hZCkge1xuICAgIC8vIEZpbHRlciBieSBvdXIgY3VycmVudCBsb2cgbGV2ZWxcbiAgICBpZiAoXG4gICAgICBQcml2YXRlLkxvZ0xldmVsW2xvZy5sZXZlbCBhcyBrZXlvZiB0eXBlb2YgUHJpdmF0ZS5Mb2dMZXZlbF0gPFxuICAgICAgUHJpdmF0ZS5Mb2dMZXZlbFt0aGlzLl9sZXZlbCBhcyBrZXlvZiB0eXBlb2YgUHJpdmF0ZS5Mb2dMZXZlbF1cbiAgICApIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgbGV0IG91dHB1dDogbmJmb3JtYXQuSU91dHB1dCB8IG51bGwgPSBudWxsO1xuICAgIHN3aXRjaCAobG9nLnR5cGUpIHtcbiAgICAgIGNhc2UgJ3RleHQnOlxuICAgICAgICBvdXRwdXQgPSB7XG4gICAgICAgICAgb3V0cHV0X3R5cGU6ICdkaXNwbGF5X2RhdGEnLFxuICAgICAgICAgIGRhdGE6IHtcbiAgICAgICAgICAgICd0ZXh0L3BsYWluJzogbG9nLmRhdGFcbiAgICAgICAgICB9XG4gICAgICAgIH07XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnaHRtbCc6XG4gICAgICAgIG91dHB1dCA9IHtcbiAgICAgICAgICBvdXRwdXRfdHlwZTogJ2Rpc3BsYXlfZGF0YScsXG4gICAgICAgICAgZGF0YToge1xuICAgICAgICAgICAgJ3RleHQvaHRtbCc6IGxvZy5kYXRhXG4gICAgICAgICAgfVxuICAgICAgICB9O1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ291dHB1dCc6XG4gICAgICAgIG91dHB1dCA9IGxvZy5kYXRhO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cblxuICAgIGlmIChvdXRwdXQpIHtcbiAgICAgIHRoaXMuX2xvZyh7XG4gICAgICAgIG91dHB1dCxcbiAgICAgICAgbGV2ZWw6IGxvZy5sZXZlbFxuICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIENsZWFyIGFsbCBvdXRwdXRzIGxvZ2dlZC5cbiAgICovXG4gIGNsZWFyKCkge1xuICAgIHRoaXMub3V0cHV0QXJlYU1vZGVsLmNsZWFyKGZhbHNlKTtcbiAgICB0aGlzLl9jb250ZW50Q2hhbmdlZC5lbWl0KCdjbGVhcicpO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIGNoZWNrcG9pbnQgdG8gdGhlIGxvZy5cbiAgICovXG4gIGNoZWNrcG9pbnQoKSB7XG4gICAgdGhpcy5fbG9nKHtcbiAgICAgIG91dHB1dDoge1xuICAgICAgICBvdXRwdXRfdHlwZTogJ2Rpc3BsYXlfZGF0YScsXG4gICAgICAgIGRhdGE6IHtcbiAgICAgICAgICAndGV4dC9odG1sJzogJzxoci8+J1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAgbGV2ZWw6ICdtZXRhZGF0YSdcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBsb2dnZXIgaXMgZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIHRoZSBsb2dnZXIuXG4gICAqL1xuICBkaXNwb3NlKCkge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgdGhpcy5jbGVhcigpO1xuICAgIHRoaXMuX3JlbmRlcm1pbWUgPSBudWxsITtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICB9XG5cbiAgcHJpdmF0ZSBfbG9nKG9wdGlvbnM6IHsgb3V0cHV0OiBuYmZvcm1hdC5JT3V0cHV0OyBsZXZlbDogRnVsbExvZ0xldmVsIH0pIHtcbiAgICAvLyBGaXJzdCwgbWFrZSBzdXJlIG91ciB2ZXJzaW9uIHJlZmxlY3RzIHRoZSBuZXcgbWVzc2FnZSBzbyB0aGluZ3NcbiAgICAvLyB0cmlnZ2VyaW5nIGZyb20gdGhlIHNpZ25hbHMgYmVsb3cgaGF2ZSB0aGUgY29ycmVjdCB2ZXJzaW9uLlxuICAgIHRoaXMuX3ZlcnNpb24rKztcblxuICAgIC8vIE5leHQsIHRyaWdnZXIgYW55IGRpc3BsYXlzIG9mIHRoZSBtZXNzYWdlXG4gICAgdGhpcy5vdXRwdXRBcmVhTW9kZWwuYWRkKHtcbiAgICAgIC4uLm9wdGlvbnMub3V0cHV0LFxuICAgICAgdGltZXN0YW1wOiBEYXRlLm5vdygpLFxuICAgICAgbGV2ZWw6IG9wdGlvbnMubGV2ZWxcbiAgICB9KTtcblxuICAgIC8vIEZpbmFsbHksIHRlbGwgcGVvcGxlIHRoYXQgdGhlIG1lc3NhZ2Ugd2FzIGFwcGVuZGVkIChhbmQgcG9zc2libHlcbiAgICAvLyBhbHJlYWR5IGRpc3BsYXllZCkuXG4gICAgdGhpcy5fY29udGVudENoYW5nZWQuZW1pdCgnYXBwZW5kJyk7XG4gIH1cblxuICBwcml2YXRlIF9pc0Rpc3Bvc2VkID0gZmFsc2U7XG4gIHByaXZhdGUgX2NvbnRlbnRDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBJQ29udGVudENoYW5nZT4odGhpcyk7XG4gIHByaXZhdGUgX3N0YXRlQ2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgSVN0YXRlQ2hhbmdlPih0aGlzKTtcbiAgcHJpdmF0ZSBfcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeSB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF92ZXJzaW9uID0gMDtcbiAgcHJpdmF0ZSBfbGV2ZWw6IExvZ0xldmVsID0gJ3dhcm5pbmcnO1xufVxuXG5leHBvcnQgbmFtZXNwYWNlIExvZ2dlciB7XG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBsb2cgc291cmNlIGlkZW50aWZpZXIuXG4gICAgICovXG4gICAgc291cmNlOiBzdHJpbmc7XG4gICAgLyoqXG4gICAgICogVGhlIG1heGltdW0gbnVtYmVyIG9mIG1lc3NhZ2VzIHRvIHN0b3JlLlxuICAgICAqL1xuICAgIG1heExlbmd0aDogbnVtYmVyO1xuICB9XG59XG5cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgZXhwb3J0IGVudW0gTG9nTGV2ZWwge1xuICAgIGRlYnVnLFxuICAgIGluZm8sXG4gICAgd2FybmluZyxcbiAgICBlcnJvcixcbiAgICBjcml0aWNhbCxcbiAgICBtZXRhZGF0YVxuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IExvZ2dlciB9IGZyb20gJy4vbG9nZ2VyJztcbmltcG9ydCB7IElMb2dnZXIsIElMb2dnZXJSZWdpc3RyeSwgSUxvZ2dlclJlZ2lzdHJ5Q2hhbmdlIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEEgY29uY3JldGUgaW1wbGVtZW50YXRpb24gb2YgSUxvZ2dlclJlZ2lzdHJ5LlxuICovXG5leHBvcnQgY2xhc3MgTG9nZ2VyUmVnaXN0cnkgaW1wbGVtZW50cyBJTG9nZ2VyUmVnaXN0cnkge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgTG9nZ2VyUmVnaXN0cnkuXG4gICAqXG4gICAqIEBwYXJhbSBkZWZhdWx0UmVuZGVybWltZSAtIERlZmF1bHQgcmVuZGVybWltZSB0byByZW5kZXIgb3V0cHV0c1xuICAgKiB3aXRoIHdoZW4gbG9nZ2VyIGlzIG5vdCBzdXBwbGllZCB3aXRoIG9uZS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IExvZ2dlclJlZ2lzdHJ5LklPcHRpb25zKSB7XG4gICAgdGhpcy5fZGVmYXVsdFJlbmRlcm1pbWUgPSBvcHRpb25zLmRlZmF1bHRSZW5kZXJtaW1lO1xuICAgIHRoaXMuX21heExlbmd0aCA9IG9wdGlvbnMubWF4TGVuZ3RoO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgbG9nZ2VyIGZvciB0aGUgc3BlY2lmaWVkIHNvdXJjZS5cbiAgICpcbiAgICogQHBhcmFtIHNvdXJjZSAtIFRoZSBuYW1lIG9mIHRoZSBsb2cgc291cmNlLlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgbG9nZ2VyIGZvciB0aGUgc3BlY2lmaWVkIHNvdXJjZS5cbiAgICovXG4gIGdldExvZ2dlcihzb3VyY2U6IHN0cmluZyk6IElMb2dnZXIge1xuICAgIGNvbnN0IGxvZ2dlcnMgPSB0aGlzLl9sb2dnZXJzO1xuICAgIGxldCBsb2dnZXIgPSBsb2dnZXJzLmdldChzb3VyY2UpO1xuICAgIGlmIChsb2dnZXIpIHtcbiAgICAgIHJldHVybiBsb2dnZXI7XG4gICAgfVxuXG4gICAgbG9nZ2VyID0gbmV3IExvZ2dlcih7IHNvdXJjZSwgbWF4TGVuZ3RoOiB0aGlzLm1heExlbmd0aCB9KTtcbiAgICBsb2dnZXIucmVuZGVybWltZSA9IHRoaXMuX2RlZmF1bHRSZW5kZXJtaW1lO1xuICAgIGxvZ2dlcnMuc2V0KHNvdXJjZSwgbG9nZ2VyKTtcblxuICAgIHRoaXMuX3JlZ2lzdHJ5Q2hhbmdlZC5lbWl0KCdhcHBlbmQnKTtcblxuICAgIHJldHVybiBsb2dnZXI7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGFsbCBsb2dnZXJzIHJlZ2lzdGVyZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBhcnJheSBjb250YWluaW5nIGFsbCByZWdpc3RlcmVkIGxvZ2dlcnMuXG4gICAqL1xuICBnZXRMb2dnZXJzKCk6IElMb2dnZXJbXSB7XG4gICAgcmV0dXJuIEFycmF5LmZyb20odGhpcy5fbG9nZ2Vycy52YWx1ZXMoKSk7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBsb2dnZXIgcmVnaXN0cnkgY2hhbmdlcy5cbiAgICovXG4gIGdldCByZWdpc3RyeUNoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCBJTG9nZ2VyUmVnaXN0cnlDaGFuZ2U+IHtcbiAgICByZXR1cm4gdGhpcy5fcmVnaXN0cnlDaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBtYXggbGVuZ3RoIGZvciBsb2dnZXJzLlxuICAgKi9cbiAgZ2V0IG1heExlbmd0aCgpOiBudW1iZXIge1xuICAgIHJldHVybiB0aGlzLl9tYXhMZW5ndGg7XG4gIH1cbiAgc2V0IG1heExlbmd0aCh2YWx1ZTogbnVtYmVyKSB7XG4gICAgdGhpcy5fbWF4TGVuZ3RoID0gdmFsdWU7XG4gICAgdGhpcy5fbG9nZ2Vycy5mb3JFYWNoKGxvZ2dlciA9PiB7XG4gICAgICBsb2dnZXIubWF4TGVuZ3RoID0gdmFsdWU7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgcmVnaXN0ZXIgaXMgZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIHRoZSByZWdpc3RyeSBhbmQgYWxsIGxvZ2dlcnMuXG4gICAqL1xuICBkaXNwb3NlKCkge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgdGhpcy5fbG9nZ2Vycy5mb3JFYWNoKHggPT4geC5kaXNwb3NlKCkpO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICBwcml2YXRlIF9kZWZhdWx0UmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcbiAgcHJpdmF0ZSBfbG9nZ2VycyA9IG5ldyBNYXA8c3RyaW5nLCBJTG9nZ2VyPigpO1xuICBwcml2YXRlIF9tYXhMZW5ndGg6IG51bWJlcjtcbiAgcHJpdmF0ZSBfcmVnaXN0cnlDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBJTG9nZ2VyUmVnaXN0cnlDaGFuZ2U+KHRoaXMpO1xuICBwcml2YXRlIF9pc0Rpc3Bvc2VkID0gZmFsc2U7XG59XG5cbmV4cG9ydCBuYW1lc3BhY2UgTG9nZ2VyUmVnaXN0cnkge1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICBkZWZhdWx0UmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcbiAgICBtYXhMZW5ndGg6IG51bWJlcjtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJQ2hhbmdlZEFyZ3MgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0ICogYXMgbmJmb3JtYXQgZnJvbSAnQGp1cHl0ZXJsYWIvbmJmb3JtYXQnO1xuaW1wb3J0IHsgSU91dHB1dEFyZWFNb2RlbCB9IGZyb20gJ0BqdXB5dGVybGFiL291dHB1dGFyZWEnO1xuaW1wb3J0IHsgSVJlbmRlck1pbWVSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuXG4vKiB0c2xpbnQ6ZGlzYWJsZSAqL1xuLyoqXG4gKiBUaGUgTG9nZ2VyIFJlZ2lzdHJ5IHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSUxvZ2dlclJlZ2lzdHJ5ID0gbmV3IFRva2VuPElMb2dnZXJSZWdpc3RyeT4oXG4gICdAanVweXRlcmxhYi9sb2djb25zb2xlOklMb2dnZXJSZWdpc3RyeSdcbik7XG5cbmV4cG9ydCB0eXBlIElMb2dnZXJSZWdpc3RyeUNoYW5nZSA9ICdhcHBlbmQnO1xuXG4vKipcbiAqIEEgTG9nZ2VyIFJlZ2lzdHJ5IHRoYXQgcmVnaXN0ZXJzIGFuZCBwcm92aWRlcyBsb2dnZXJzIGJ5IHNvdXJjZS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJTG9nZ2VyUmVnaXN0cnkgZXh0ZW5kcyBJRGlzcG9zYWJsZSB7XG4gIC8qKlxuICAgKiBHZXQgdGhlIGxvZ2dlciBmb3IgdGhlIHNwZWNpZmllZCBzb3VyY2UuXG4gICAqXG4gICAqIEBwYXJhbSBzb3VyY2UgLSBUaGUgbmFtZSBvZiB0aGUgbG9nIHNvdXJjZS5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIGxvZ2dlciBmb3IgdGhlIHNwZWNpZmllZCBzb3VyY2UuXG4gICAqL1xuICBnZXRMb2dnZXIoc291cmNlOiBzdHJpbmcpOiBJTG9nZ2VyO1xuICAvKipcbiAgICogR2V0IGFsbCBsb2dnZXJzIHJlZ2lzdGVyZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBhcnJheSBjb250YWluaW5nIGFsbCByZWdpc3RlcmVkIGxvZ2dlcnMuXG4gICAqL1xuICBnZXRMb2dnZXJzKCk6IElMb2dnZXJbXTtcblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBsb2dnZXIgcmVnaXN0cnkgY2hhbmdlcy5cbiAgICovXG4gIHJlYWRvbmx5IHJlZ2lzdHJ5Q2hhbmdlZDogSVNpZ25hbDx0aGlzLCBJTG9nZ2VyUmVnaXN0cnlDaGFuZ2U+O1xufVxuXG4vKipcbiAqIExvZyBzZXZlcml0eSBsZXZlbFxuICovXG5leHBvcnQgdHlwZSBMb2dMZXZlbCA9ICdjcml0aWNhbCcgfCAnZXJyb3InIHwgJ3dhcm5pbmcnIHwgJ2luZm8nIHwgJ2RlYnVnJztcblxuLyoqXG4gKiBUaGUgYmFzZSBsb2cgcGF5bG9hZCB0eXBlLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElMb2dQYXlsb2FkQmFzZSB7XG4gIC8qKlxuICAgKiBUeXBlIG9mIGxvZyBkYXRhLlxuICAgKi9cbiAgdHlwZTogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBMb2cgbGV2ZWxcbiAgICovXG4gIGxldmVsOiBMb2dMZXZlbDtcblxuICAvKipcbiAgICogRGF0YVxuICAgKi9cbiAgZGF0YTogYW55O1xufVxuXG4vKipcbiAqIFBsYWluIHRleHQgbG9nIHBheWxvYWQuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVRleHRMb2cgZXh0ZW5kcyBJTG9nUGF5bG9hZEJhc2Uge1xuICAvKipcbiAgICogVHlwZSBvZiBsb2cgZGF0YS5cbiAgICovXG4gIHR5cGU6ICd0ZXh0JztcbiAgLyoqXG4gICAqIExvZyBkYXRhIGFzIHBsYWluIHRleHQuXG4gICAqL1xuICBkYXRhOiBzdHJpbmc7XG59XG5cbi8qKlxuICogSFRNTCBsb2cgcGF5bG9hZC5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJSHRtbExvZyBleHRlbmRzIElMb2dQYXlsb2FkQmFzZSB7XG4gIC8qKlxuICAgKiBUeXBlIG9mIGxvZyBkYXRhLlxuICAgKi9cbiAgdHlwZTogJ2h0bWwnO1xuICAvKipcbiAgICogTG9nIGRhdGEgYXMgSFRNTCBzdHJpbmcuXG4gICAqL1xuICBkYXRhOiBzdHJpbmc7XG59XG5cbi8qKlxuICogTm90ZWJvb2sga2VybmVsIG91dHB1dCBsb2cgcGF5bG9hZC5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJT3V0cHV0TG9nIGV4dGVuZHMgSUxvZ1BheWxvYWRCYXNlIHtcbiAgLyoqXG4gICAqIFR5cGUgb2YgbG9nIGRhdGEuXG4gICAqL1xuICB0eXBlOiAnb3V0cHV0JztcbiAgLyoqXG4gICAqIExvZyBkYXRhIGFzIE5vdGVib29rIGtlcm5lbCBvdXRwdXQuXG4gICAqL1xuICBkYXRhOiBuYmZvcm1hdC5JT3V0cHV0O1xufVxuXG4vKipcbiAqIExvZyBwYXlsb2FkIHVuaW9uIHR5cGUuXG4gKi9cbmV4cG9ydCB0eXBlIElMb2dQYXlsb2FkID0gSVRleHRMb2cgfCBJSHRtbExvZyB8IElPdXRwdXRMb2c7XG5cbmV4cG9ydCB0eXBlIElDb250ZW50Q2hhbmdlID0gJ2FwcGVuZCcgfCAnY2xlYXInO1xuXG5leHBvcnQgdHlwZSBJU3RhdGVDaGFuZ2UgPVxuICB8IElDaGFuZ2VkQXJnczxcbiAgICAgIElSZW5kZXJNaW1lUmVnaXN0cnkgfCBudWxsLFxuICAgICAgSVJlbmRlck1pbWVSZWdpc3RyeSB8IG51bGwsXG4gICAgICAncmVuZGVybWltZSdcbiAgICA+XG4gIHwgSUNoYW5nZWRBcmdzPExvZ0xldmVsLCBMb2dMZXZlbCwgJ2xldmVsJz47XG5cbmV4cG9ydCBpbnRlcmZhY2UgSUxvZ2dlck91dHB1dEFyZWFNb2RlbCBleHRlbmRzIElPdXRwdXRBcmVhTW9kZWwge1xuICAvKipcbiAgICogVGhlIG1heGltdW0gbnVtYmVyIG9mIG91dHB1dHMgdG8gc3RvcmUuXG4gICAqL1xuICBtYXhMZW5ndGg6IG51bWJlcjtcbn1cblxuLyoqXG4gKiBBIExvZ2dlciB0aGF0IG1hbmFnZXMgbG9ncyBmcm9tIGEgcGFydGljdWxhciBzb3VyY2UuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUxvZ2dlciBleHRlbmRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIE51bWJlciBvZiBvdXRwdXRzIGxvZ2dlZC5cbiAgICovXG4gIHJlYWRvbmx5IGxlbmd0aDogbnVtYmVyO1xuICAvKipcbiAgICogTWF4IG51bWJlciBvZiBtZXNzYWdlcy5cbiAgICovXG4gIG1heExlbmd0aDogbnVtYmVyO1xuICAvKipcbiAgICogTG9nIGxldmVsLlxuICAgKi9cbiAgbGV2ZWw6IExvZ0xldmVsO1xuICAvKipcbiAgICogUmVuZGVybWltZSB0byB1c2Ugd2hlbiByZW5kZXJpbmcgb3V0cHV0cyBsb2dnZWQuXG4gICAqL1xuICByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5IHwgbnVsbDtcbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbG9nIG1vZGVsIGNoYW5nZXMuXG4gICAqL1xuICByZWFkb25seSBjb250ZW50Q2hhbmdlZDogSVNpZ25hbDx0aGlzLCBJQ29udGVudENoYW5nZT47XG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIHJlbmRlcm1pbWUgY2hhbmdlcy5cbiAgICovXG4gIHJlYWRvbmx5IHN0YXRlQ2hhbmdlZDogSVNpZ25hbDx0aGlzLCBJU3RhdGVDaGFuZ2U+O1xuICAvKipcbiAgICogVGhlIG5hbWUgb2YgdGhlIGxvZyBzb3VyY2UuXG4gICAqL1xuICByZWFkb25seSBzb3VyY2U6IHN0cmluZztcbiAgLyoqXG4gICAqIE91dHB1dCBBcmVhIE1vZGVsIHVzZWQgdG8gbWFuYWdlIGxvZyBzdG9yYWdlIGluIG1lbW9yeS5cbiAgICovXG4gIHJlYWRvbmx5IG91dHB1dEFyZWFNb2RlbDogSUxvZ2dlck91dHB1dEFyZWFNb2RlbDtcbiAgLyoqXG4gICAqIFRoZSBjdW11bGF0aXZlIG51bWJlciBvZiBtZXNzYWdlcyB0aGUgbG9nIGhhcyBzdG9yZWQuXG4gICAqL1xuICByZWFkb25seSB2ZXJzaW9uOiBudW1iZXI7XG4gIC8qKlxuICAgKiBMb2cgYW4gb3V0cHV0IHRvIGxvZ2dlci5cbiAgICpcbiAgICogQHBhcmFtIGxvZyAtIFRoZSBvdXRwdXQgdG8gYmUgbG9nZ2VkLlxuICAgKi9cbiAgbG9nKGxvZzogSUxvZ1BheWxvYWQpOiB2b2lkO1xuICAvKipcbiAgICogQWRkIGEgY2hlY2twb2ludCBpbiB0aGUgbG9nLlxuICAgKi9cbiAgY2hlY2twb2ludCgpOiB2b2lkO1xuICAvKipcbiAgICogQ2xlYXIgYWxsIG91dHB1dHMgbG9nZ2VkLlxuICAgKi9cbiAgY2xlYXIoKTogdm9pZDtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSUNoYW5nZWRBcmdzIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCAqIGFzIG5iZm9ybWF0IGZyb20gJ0BqdXB5dGVybGFiL25iZm9ybWF0JztcbmltcG9ydCB7IElPdXRwdXRQcm9tcHQsIE91dHB1dEFyZWEgfSBmcm9tICdAanVweXRlcmxhYi9vdXRwdXRhcmVhJztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IEtlcm5lbCwgS2VybmVsTWVzc2FnZSB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFBhbmVsLCBQYW5lbExheW91dCwgU3RhY2tlZFBhbmVsLCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgTG9nZ2VyT3V0cHV0QXJlYU1vZGVsLCBMb2dPdXRwdXRNb2RlbCB9IGZyb20gJy4vbG9nZ2VyJztcbmltcG9ydCB7XG4gIElDb250ZW50Q2hhbmdlLFxuICBJTG9nZ2VyLFxuICBJTG9nZ2VyUmVnaXN0cnksXG4gIElMb2dnZXJSZWdpc3RyeUNoYW5nZSxcbiAgSVN0YXRlQ2hhbmdlLFxuICBMb2dMZXZlbFxufSBmcm9tICcuL3Rva2Vucyc7XG5cbmZ1bmN0aW9uIHRvVGl0bGVDYXNlKHZhbHVlOiBzdHJpbmcpIHtcbiAgcmV0dXJuIHZhbHVlLmxlbmd0aCA9PT0gMCA/IHZhbHVlIDogdmFsdWVbMF0udG9VcHBlckNhc2UoKSArIHZhbHVlLnNsaWNlKDEpO1xufVxuXG4vKipcbiAqIEFsbCBzZXZlcml0eSBsZXZlbHMsIGluY2x1ZGluZyBhbiBpbnRlcm5hbCBvbmUgZm9yIG1ldGFkYXRhLlxuICovXG50eXBlIEZ1bGxMb2dMZXZlbCA9IExvZ0xldmVsIHwgJ21ldGFkYXRhJztcblxuLyoqXG4gKiBMb2cgY29uc29sZSBvdXRwdXQgcHJvbXB0IGltcGxlbWVudGF0aW9uXG4gKi9cbmNsYXNzIExvZ0NvbnNvbGVPdXRwdXRQcm9tcHQgZXh0ZW5kcyBXaWRnZXQgaW1wbGVtZW50cyBJT3V0cHV0UHJvbXB0IHtcbiAgY29uc3RydWN0b3IoKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl90aW1lc3RhbXBOb2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgdGhpcy5ub2RlLmFwcGVuZCh0aGlzLl90aW1lc3RhbXBOb2RlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEYXRlICYgdGltZSB3aGVuIG91dHB1dCBpcyBsb2dnZWQuXG4gICAqL1xuICBzZXQgdGltZXN0YW1wKHZhbHVlOiBEYXRlKSB7XG4gICAgdGhpcy5fdGltZXN0YW1wID0gdmFsdWU7XG4gICAgdGhpcy5fdGltZXN0YW1wTm9kZS5pbm5lckhUTUwgPSB0aGlzLl90aW1lc3RhbXAudG9Mb2NhbGVUaW1lU3RyaW5nKCk7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBMb2cgbGV2ZWxcbiAgICovXG4gIHNldCBsZXZlbCh2YWx1ZTogRnVsbExvZ0xldmVsKSB7XG4gICAgdGhpcy5fbGV2ZWwgPSB2YWx1ZTtcbiAgICB0aGlzLm5vZGUuZGF0YXNldC5sb2dMZXZlbCA9IHZhbHVlO1xuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICB1cGRhdGUoKSB7XG4gICAgaWYgKHRoaXMuX2xldmVsICE9PSB1bmRlZmluZWQgJiYgdGhpcy5fdGltZXN0YW1wICE9PSB1bmRlZmluZWQpIHtcbiAgICAgIHRoaXMubm9kZS50aXRsZSA9IGAke3RoaXMuX3RpbWVzdGFtcC50b0xvY2FsZVN0cmluZygpfTsgJHt0b1RpdGxlQ2FzZShcbiAgICAgICAgdGhpcy5fbGV2ZWxcbiAgICAgICl9IGxldmVsYDtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIGV4ZWN1dGlvbiBjb3VudCBmb3IgdGhlIHByb21wdC5cbiAgICovXG4gIGV4ZWN1dGlvbkNvdW50OiBuYmZvcm1hdC5FeGVjdXRpb25Db3VudDtcblxuICBwcml2YXRlIF90aW1lc3RhbXA6IERhdGU7XG4gIHByaXZhdGUgX2xldmVsOiBGdWxsTG9nTGV2ZWw7XG4gIHByaXZhdGUgX3RpbWVzdGFtcE5vZGU6IEhUTUxEaXZFbGVtZW50O1xufVxuXG4vKipcbiAqIE91dHB1dCBBcmVhIGltcGxlbWVudGF0aW9uIGRpc3BsYXlpbmcgbG9nIG91dHB1dHNcbiAqIHdpdGggcHJvbXB0cyBzaG93aW5nIGxvZyB0aW1lc3RhbXBzLlxuICovXG5jbGFzcyBMb2dDb25zb2xlT3V0cHV0QXJlYSBleHRlbmRzIE91dHB1dEFyZWEge1xuICAvKipcbiAgICogT3V0cHV0IGFyZWEgbW9kZWwgdXNlZCBieSB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcmVhZG9ubHkgbW9kZWw6IExvZ2dlck91dHB1dEFyZWFNb2RlbDtcblxuICAvKipcbiAgICogQ3JlYXRlIGFuIG91dHB1dCBpdGVtIHdpdGggYSBwcm9tcHQgYW5kIGFjdHVhbCBvdXRwdXRcbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVPdXRwdXRJdGVtKG1vZGVsOiBMb2dPdXRwdXRNb2RlbCk6IFdpZGdldCB8IG51bGwge1xuICAgIGNvbnN0IHBhbmVsID0gc3VwZXIuY3JlYXRlT3V0cHV0SXRlbShtb2RlbCkgYXMgUGFuZWw7XG4gICAgaWYgKHBhbmVsID09PSBudWxsKSB7XG4gICAgICAvLyBDb3VsZCBub3QgcmVuZGVyIG1vZGVsXG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG5cbiAgICAvLyBmaXJzdCB3aWRnZXQgaW4gcGFuZWwgaXMgcHJvbXB0IG9mIHR5cGUgTG9nZ2VyT3V0cHV0UHJvbXB0XG4gICAgY29uc3QgcHJvbXB0ID0gcGFuZWwud2lkZ2V0c1swXSBhcyBMb2dDb25zb2xlT3V0cHV0UHJvbXB0O1xuICAgIHByb21wdC50aW1lc3RhbXAgPSBtb2RlbC50aW1lc3RhbXA7XG4gICAgcHJvbXB0LmxldmVsID0gbW9kZWwubGV2ZWw7XG4gICAgcmV0dXJuIHBhbmVsO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhbiBpbnB1dCByZXF1ZXN0IGZyb20gYSBrZXJuZWwgYnkgZG9pbmcgbm90aGluZy5cbiAgICovXG4gIHByb3RlY3RlZCBvbklucHV0UmVxdWVzdChcbiAgICBtc2c6IEtlcm5lbE1lc3NhZ2UuSUlucHV0UmVxdWVzdE1zZyxcbiAgICBmdXR1cmU6IEtlcm5lbC5JU2hlbGxGdXR1cmVcbiAgKTogdm9pZCB7XG4gICAgcmV0dXJuO1xuICB9XG59XG5cbi8qKlxuICogSW1wbGVtZW50YXRpb24gb2YgYElDb250ZW50RmFjdG9yeWAgZm9yIE91dHB1dCBBcmVhXG4gKiB3aGljaCBjcmVhdGVzIGN1c3RvbSBvdXRwdXQgcHJvbXB0cy5cbiAqL1xuY2xhc3MgTG9nQ29uc29sZUNvbnRlbnRGYWN0b3J5IGV4dGVuZHMgT3V0cHV0QXJlYS5Db250ZW50RmFjdG9yeSB7XG4gIC8qKlxuICAgKiBDcmVhdGUgdGhlIG91dHB1dCBwcm9tcHQgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBjcmVhdGVPdXRwdXRQcm9tcHQoKTogTG9nQ29uc29sZU91dHB1dFByb21wdCB7XG4gICAgcmV0dXJuIG5ldyBMb2dDb25zb2xlT3V0cHV0UHJvbXB0KCk7XG4gIH1cbn1cblxuLyoqXG4gKiBJbXBsZW1lbnRzIGEgcGFuZWwgd2hpY2ggc3VwcG9ydHMgcGlubmluZyB0aGUgcG9zaXRpb24gdG8gdGhlIGVuZCBpZiBpdCBpc1xuICogc2Nyb2xsZWQgdG8gdGhlIGVuZC5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiBUaGlzIGlzIHVzZWZ1bCBmb3IgbG9nIHZpZXdpbmcgY29tcG9uZW50cyBvciBjaGF0IGNvbXBvbmVudHMgdGhhdCBhcHBlbmRcbiAqIGVsZW1lbnRzIGF0IHRoZSBlbmQuIFdlIHdvdWxkIGxpa2UgdG8gYXV0b21hdGljYWxseSBzY3JvbGwgd2hlbiB0aGUgdXNlclxuICogaGFzIHNjcm9sbGVkIHRvIHRoZSBib3R0b20sIGJ1dCBub3QgY2hhbmdlIHRoZSBzY3JvbGxpbmcgd2hlbiB0aGUgdXNlciBoYXNcbiAqIGNoYW5nZWQgdGhlIHNjcm9sbCBwb3NpdGlvbi5cbiAqL1xuZXhwb3J0IGNsYXNzIFNjcm9sbGluZ1dpZGdldDxUIGV4dGVuZHMgV2lkZ2V0PiBleHRlbmRzIFdpZGdldCB7XG4gIGNvbnN0cnVjdG9yKHsgY29udGVudCwgLi4ub3B0aW9ucyB9OiBTY3JvbGxpbmdXaWRnZXQuSU9wdGlvbnM8VD4pIHtcbiAgICBzdXBlcihvcHRpb25zKTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1TY3JvbGxpbmcnKTtcbiAgICBjb25zdCBsYXlvdXQgPSAodGhpcy5sYXlvdXQgPSBuZXcgUGFuZWxMYXlvdXQoKSk7XG4gICAgbGF5b3V0LmFkZFdpZGdldChjb250ZW50KTtcblxuICAgIHRoaXMuX2NvbnRlbnQgPSBjb250ZW50O1xuICAgIHRoaXMuX3NlbnRpbmVsID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgdGhpcy5ub2RlLmFwcGVuZENoaWxkKHRoaXMuX3NlbnRpbmVsKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY29udGVudCB3aWRnZXQuXG4gICAqL1xuICBnZXQgY29udGVudCgpOiBUIHtcbiAgICByZXR1cm4gdGhpcy5fY29udGVudDtcbiAgfVxuXG4gIHByb3RlY3RlZCBvbkFmdGVyQXR0YWNoKG1zZzogTWVzc2FnZSkge1xuICAgIHN1cGVyLm9uQWZ0ZXJBdHRhY2gobXNnKTtcbiAgICAvLyBkZWZlciBzbyBjb250ZW50IGdldHMgYSBjaGFuY2UgdG8gYXR0YWNoIGZpcnN0XG4gICAgcmVxdWVzdEFuaW1hdGlvbkZyYW1lKCgpID0+IHtcbiAgICAgIHRoaXMuX3NlbnRpbmVsLnNjcm9sbEludG9WaWV3KCk7XG4gICAgICB0aGlzLl9zY3JvbGxIZWlnaHQgPSB0aGlzLm5vZGUuc2Nyb2xsSGVpZ2h0O1xuICAgIH0pO1xuXG4gICAgLy8gU2V0IHVwIGludGVyc2VjdGlvbiBvYnNlcnZlciBmb3IgdGhlIHNlbnRpbmVsXG4gICAgaWYgKHR5cGVvZiBJbnRlcnNlY3Rpb25PYnNlcnZlciAhPT0gJ3VuZGVmaW5lZCcpIHtcbiAgICAgIHRoaXMuX29ic2VydmVyID0gbmV3IEludGVyc2VjdGlvbk9ic2VydmVyKFxuICAgICAgICBhcmdzID0+IHtcbiAgICAgICAgICB0aGlzLl9oYW5kbGVTY3JvbGwoYXJncyk7XG4gICAgICAgIH0sXG4gICAgICAgIHsgcm9vdDogdGhpcy5ub2RlLCB0aHJlc2hvbGQ6IDEgfVxuICAgICAgKTtcbiAgICAgIHRoaXMuX29ic2VydmVyLm9ic2VydmUodGhpcy5fc2VudGluZWwpO1xuICAgIH1cbiAgfVxuXG4gIHByb3RlY3RlZCBvbkJlZm9yZURldGFjaChtc2c6IE1lc3NhZ2UpIHtcbiAgICBpZiAodGhpcy5fb2JzZXJ2ZXIpIHtcbiAgICAgIHRoaXMuX29ic2VydmVyLmRpc2Nvbm5lY3QoKTtcbiAgICB9XG4gIH1cblxuICBwcm90ZWN0ZWQgb25BZnRlclNob3cobXNnOiBNZXNzYWdlKSB7XG4gICAgaWYgKHRoaXMuX3RyYWNraW5nKSB7XG4gICAgICB0aGlzLl9zZW50aW5lbC5zY3JvbGxJbnRvVmlldygpO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX2hhbmRsZVNjcm9sbChbZW50cnldOiBJbnRlcnNlY3Rpb25PYnNlcnZlckVudHJ5W10pIHtcbiAgICBpZiAoZW50cnkuaXNJbnRlcnNlY3RpbmcpIHtcbiAgICAgIHRoaXMuX3RyYWNraW5nID0gdHJ1ZTtcbiAgICB9IGVsc2UgaWYgKHRoaXMuaXNWaXNpYmxlKSB7XG4gICAgICBjb25zdCBjdXJyZW50SGVpZ2h0ID0gdGhpcy5ub2RlLnNjcm9sbEhlaWdodDtcbiAgICAgIGlmIChjdXJyZW50SGVpZ2h0ID09PSB0aGlzLl9zY3JvbGxIZWlnaHQpIHtcbiAgICAgICAgLy8gTGlrZWx5IHRoZSB1c2VyIHNjcm9sbGVkIG1hbnVhbGx5XG4gICAgICAgIHRoaXMuX3RyYWNraW5nID0gZmFsc2U7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICAvLyBXZSBhc3N1bWUgd2Ugc2Nyb2xsZWQgYmVjYXVzZSBvdXIgc2l6ZSBjaGFuZ2VkLCBzbyBzY3JvbGwgdG8gdGhlIGVuZC5cbiAgICAgICAgdGhpcy5fc2VudGluZWwuc2Nyb2xsSW50b1ZpZXcoKTtcbiAgICAgICAgdGhpcy5fc2Nyb2xsSGVpZ2h0ID0gY3VycmVudEhlaWdodDtcbiAgICAgICAgdGhpcy5fdHJhY2tpbmcgPSB0cnVlO1xuICAgICAgfVxuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX2NvbnRlbnQ6IFQ7XG4gIHByaXZhdGUgX29ic2VydmVyOiBJbnRlcnNlY3Rpb25PYnNlcnZlciB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9zY3JvbGxIZWlnaHQ6IG51bWJlcjtcbiAgcHJpdmF0ZSBfc2VudGluZWw6IEhUTUxEaXZFbGVtZW50O1xuICBwcml2YXRlIF90cmFja2luZzogYm9vbGVhbjtcbn1cblxuZXhwb3J0IG5hbWVzcGFjZSBTY3JvbGxpbmdXaWRnZXQge1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zPFQgZXh0ZW5kcyBXaWRnZXQ+IGV4dGVuZHMgV2lkZ2V0LklPcHRpb25zIHtcbiAgICBjb250ZW50OiBUO1xuICB9XG59XG5cbi8qKlxuICogQSBTdGFja2VkUGFuZWwgaW1wbGVtZW50YXRpb24gdGhhdCBjcmVhdGVzIE91dHB1dCBBcmVhc1xuICogZm9yIGVhY2ggbG9nIHNvdXJjZSBhbmQgYWN0aXZhdGVzIGFzIHNvdXJjZSBpcyBzd2l0Y2hlZC5cbiAqL1xuZXhwb3J0IGNsYXNzIExvZ0NvbnNvbGVQYW5lbCBleHRlbmRzIFN0YWNrZWRQYW5lbCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBMb2dDb25zb2xlUGFuZWwgaW5zdGFuY2UuXG4gICAqXG4gICAqIEBwYXJhbSBsb2dnZXJSZWdpc3RyeSAtIFRoZSBsb2dnZXIgcmVnaXN0cnkgdGhhdCBwcm92aWRlc1xuICAgKiBsb2dzIHRvIGJlIGRpc3BsYXllZC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKGxvZ2dlclJlZ2lzdHJ5OiBJTG9nZ2VyUmVnaXN0cnksIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcikge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl90cmFucyA9IHRoaXMudHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgdGhpcy5fbG9nZ2VyUmVnaXN0cnkgPSBsb2dnZXJSZWdpc3RyeTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1Mb2dDb25zb2xlUGFuZWwnKTtcblxuICAgIGxvZ2dlclJlZ2lzdHJ5LnJlZ2lzdHJ5Q2hhbmdlZC5jb25uZWN0KFxuICAgICAgKHNlbmRlcjogSUxvZ2dlclJlZ2lzdHJ5LCBhcmdzOiBJTG9nZ2VyUmVnaXN0cnlDaGFuZ2UpID0+IHtcbiAgICAgICAgdGhpcy5fYmluZExvZ2dlclNpZ25hbHMoKTtcbiAgICAgIH0sXG4gICAgICB0aGlzXG4gICAgKTtcblxuICAgIHRoaXMuX2JpbmRMb2dnZXJTaWduYWxzKCk7XG5cbiAgICB0aGlzLl9wbGFjZWhvbGRlciA9IG5ldyBXaWRnZXQoKTtcbiAgICB0aGlzLl9wbGFjZWhvbGRlci5hZGRDbGFzcygnanAtTG9nQ29uc29sZUxpc3RQbGFjZWhvbGRlcicpO1xuICAgIHRoaXMuYWRkV2lkZ2V0KHRoaXMuX3BsYWNlaG9sZGVyKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbG9nZ2VyIHJlZ2lzdHJ5IHByb3ZpZGluZyB0aGUgbG9ncy5cbiAgICovXG4gIGdldCBsb2dnZXJSZWdpc3RyeSgpOiBJTG9nZ2VyUmVnaXN0cnkge1xuICAgIHJldHVybiB0aGlzLl9sb2dnZXJSZWdpc3RyeTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY3VycmVudCBsb2dnZXIuXG4gICAqL1xuICBnZXQgbG9nZ2VyKCk6IElMb2dnZXIgfCBudWxsIHtcbiAgICBpZiAodGhpcy5zb3VyY2UgPT09IG51bGwpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5sb2dnZXJSZWdpc3RyeS5nZXRMb2dnZXIodGhpcy5zb3VyY2UpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBsb2cgc291cmNlIGRpc3BsYXllZFxuICAgKi9cbiAgZ2V0IHNvdXJjZSgpOiBzdHJpbmcgfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fc291cmNlO1xuICB9XG4gIHNldCBzb3VyY2UobmFtZTogc3RyaW5nIHwgbnVsbCkge1xuICAgIGlmIChuYW1lID09PSB0aGlzLl9zb3VyY2UpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3Qgb2xkVmFsdWUgPSB0aGlzLl9zb3VyY2U7XG4gICAgY29uc3QgbmV3VmFsdWUgPSAodGhpcy5fc291cmNlID0gbmFtZSk7XG4gICAgdGhpcy5fc2hvd091dHB1dEZyb21Tb3VyY2UobmV3VmFsdWUpO1xuICAgIHRoaXMuX2hhbmRsZVBsYWNlaG9sZGVyKCk7XG4gICAgdGhpcy5fc291cmNlQ2hhbmdlZC5lbWl0KHsgb2xkVmFsdWUsIG5ld1ZhbHVlLCBuYW1lOiAnc291cmNlJyB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgc291cmNlIHZlcnNpb24gZGlzcGxheWVkLlxuICAgKi9cbiAgZ2V0IHNvdXJjZVZlcnNpb24oKTogbnVtYmVyIHwgbnVsbCB7XG4gICAgY29uc3Qgc291cmNlID0gdGhpcy5zb3VyY2U7XG4gICAgcmV0dXJuIHNvdXJjZSAhPT0gbnVsbFxuICAgICAgPyB0aGlzLl9sb2dnZXJSZWdpc3RyeS5nZXRMb2dnZXIoc291cmNlKS52ZXJzaW9uXG4gICAgICA6IG51bGw7XG4gIH1cblxuICAvKipcbiAgICogU2lnbmFsIGZvciBzb3VyY2UgY2hhbmdlc1xuICAgKi9cbiAgZ2V0IHNvdXJjZUNoYW5nZWQoKTogSVNpZ25hbDxcbiAgICB0aGlzLFxuICAgIElDaGFuZ2VkQXJnczxzdHJpbmcgfCBudWxsLCBzdHJpbmcgfCBudWxsLCAnc291cmNlJz5cbiAgPiB7XG4gICAgcmV0dXJuIHRoaXMuX3NvdXJjZUNoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogU2lnbmFsIGZvciBzb3VyY2UgY2hhbmdlc1xuICAgKi9cbiAgZ2V0IHNvdXJjZURpc3BsYXllZCgpOiBJU2lnbmFsPHRoaXMsIElTb3VyY2VEaXNwbGF5ZWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fc291cmNlRGlzcGxheWVkO1xuICB9XG5cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgc3VwZXIub25BZnRlckF0dGFjaChtc2cpO1xuICAgIHRoaXMuX3VwZGF0ZU91dHB1dEFyZWFzKCk7XG4gICAgdGhpcy5fc2hvd091dHB1dEZyb21Tb3VyY2UodGhpcy5fc291cmNlKTtcbiAgICB0aGlzLl9oYW5kbGVQbGFjZWhvbGRlcigpO1xuICB9XG5cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJTaG93KG1zZzogTWVzc2FnZSkge1xuICAgIHN1cGVyLm9uQWZ0ZXJTaG93KG1zZyk7XG4gICAgaWYgKHRoaXMuc291cmNlICE9PSBudWxsKSB7XG4gICAgICB0aGlzLl9zb3VyY2VEaXNwbGF5ZWQuZW1pdCh7XG4gICAgICAgIHNvdXJjZTogdGhpcy5zb3VyY2UsXG4gICAgICAgIHZlcnNpb246IHRoaXMuc291cmNlVmVyc2lvblxuICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfYmluZExvZ2dlclNpZ25hbHMoKSB7XG4gICAgY29uc3QgbG9nZ2VycyA9IHRoaXMuX2xvZ2dlclJlZ2lzdHJ5LmdldExvZ2dlcnMoKTtcbiAgICBmb3IgKGNvbnN0IGxvZ2dlciBvZiBsb2dnZXJzKSB7XG4gICAgICBpZiAodGhpcy5fbG9nZ2Vyc1dhdGNoZWQuaGFzKGxvZ2dlci5zb3VyY2UpKSB7XG4gICAgICAgIGNvbnRpbnVlO1xuICAgICAgfVxuXG4gICAgICBsb2dnZXIuY29udGVudENoYW5nZWQuY29ubmVjdCgoc2VuZGVyOiBJTG9nZ2VyLCBhcmdzOiBJQ29udGVudENoYW5nZSkgPT4ge1xuICAgICAgICB0aGlzLl91cGRhdGVPdXRwdXRBcmVhcygpO1xuICAgICAgICB0aGlzLl9oYW5kbGVQbGFjZWhvbGRlcigpO1xuICAgICAgfSwgdGhpcyk7XG5cbiAgICAgIGxvZ2dlci5zdGF0ZUNoYW5nZWQuY29ubmVjdCgoc2VuZGVyOiBJTG9nZ2VyLCBjaGFuZ2U6IElTdGF0ZUNoYW5nZSkgPT4ge1xuICAgICAgICBpZiAoY2hhbmdlLm5hbWUgIT09ICdyZW5kZXJtaW1lJykge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCB2aWV3SWQgPSBgc291cmNlOiR7c2VuZGVyLnNvdXJjZX1gO1xuICAgICAgICBjb25zdCBvdXRwdXRBcmVhID0gdGhpcy5fb3V0cHV0QXJlYXMuZ2V0KHZpZXdJZCk7XG4gICAgICAgIGlmIChvdXRwdXRBcmVhKSB7XG4gICAgICAgICAgaWYgKGNoYW5nZS5uZXdWYWx1ZSkge1xuICAgICAgICAgICAgLy8gY2FzdCBhd2F5IHJlYWRvbmx5XG4gICAgICAgICAgICAob3V0cHV0QXJlYS5yZW5kZXJtaW1lIGFzIElSZW5kZXJNaW1lUmVnaXN0cnkpID0gY2hhbmdlLm5ld1ZhbHVlO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBvdXRwdXRBcmVhLmRpc3Bvc2UoKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0sIHRoaXMpO1xuXG4gICAgICB0aGlzLl9sb2dnZXJzV2F0Y2hlZC5hZGQobG9nZ2VyLnNvdXJjZSk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfc2hvd091dHB1dEZyb21Tb3VyY2Uoc291cmNlOiBzdHJpbmcgfCBudWxsKSB7XG4gICAgLy8gSWYgdGhlIHNvdXJjZSBpcyBudWxsLCBwaWNrIGEgdW5pcXVlIG5hbWUgc28gYWxsIG91dHB1dCBhcmVhcyBoaWRlLlxuICAgIGNvbnN0IHZpZXdJZCA9IHNvdXJjZSA9PT0gbnVsbCA/ICdudWxsIHNvdXJjZScgOiBgc291cmNlOiR7c291cmNlfWA7XG5cbiAgICB0aGlzLl9vdXRwdXRBcmVhcy5mb3JFYWNoKFxuICAgICAgKG91dHB1dEFyZWE6IExvZ0NvbnNvbGVPdXRwdXRBcmVhLCBuYW1lOiBzdHJpbmcpID0+IHtcbiAgICAgICAgLy8gU2hvdy9oaWRlIHRoZSBvdXRwdXQgYXJlYSBwYXJlbnRzLCB0aGUgc2Nyb2xsaW5nIHdpbmRvd3MuXG4gICAgICAgIGlmIChvdXRwdXRBcmVhLmlkID09PSB2aWV3SWQpIHtcbiAgICAgICAgICBvdXRwdXRBcmVhLnBhcmVudD8uc2hvdygpO1xuICAgICAgICAgIGlmIChvdXRwdXRBcmVhLmlzVmlzaWJsZSkge1xuICAgICAgICAgICAgdGhpcy5fc291cmNlRGlzcGxheWVkLmVtaXQoe1xuICAgICAgICAgICAgICBzb3VyY2U6IHRoaXMuc291cmNlLFxuICAgICAgICAgICAgICB2ZXJzaW9uOiB0aGlzLnNvdXJjZVZlcnNpb25cbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBvdXRwdXRBcmVhLnBhcmVudD8uaGlkZSgpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgKTtcblxuICAgIGNvbnN0IHRpdGxlID1cbiAgICAgIHNvdXJjZSA9PT0gbnVsbFxuICAgICAgICA/IHRoaXMuX3RyYW5zLl9fKCdMb2cgQ29uc29sZScpXG4gICAgICAgIDogdGhpcy5fdHJhbnMuX18oJ0xvZzogJTEnLCBzb3VyY2UpO1xuICAgIHRoaXMudGl0bGUubGFiZWwgPSB0aXRsZTtcbiAgICB0aGlzLnRpdGxlLmNhcHRpb24gPSB0aXRsZTtcbiAgfVxuXG4gIHByaXZhdGUgX2hhbmRsZVBsYWNlaG9sZGVyKCkge1xuICAgIGlmICh0aGlzLnNvdXJjZSA9PT0gbnVsbCkge1xuICAgICAgdGhpcy5fcGxhY2Vob2xkZXIubm9kZS50ZXh0Q29udGVudCA9IHRoaXMuX3RyYW5zLl9fKFxuICAgICAgICAnTm8gc291cmNlIHNlbGVjdGVkLidcbiAgICAgICk7XG4gICAgICB0aGlzLl9wbGFjZWhvbGRlci5zaG93KCk7XG4gICAgfSBlbHNlIGlmICh0aGlzLl9sb2dnZXJSZWdpc3RyeS5nZXRMb2dnZXIodGhpcy5zb3VyY2UpLmxlbmd0aCA9PT0gMCkge1xuICAgICAgdGhpcy5fcGxhY2Vob2xkZXIubm9kZS50ZXh0Q29udGVudCA9IHRoaXMuX3RyYW5zLl9fKCdObyBsb2cgbWVzc2FnZXMuJyk7XG4gICAgICB0aGlzLl9wbGFjZWhvbGRlci5zaG93KCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX3BsYWNlaG9sZGVyLmhpZGUoKTtcbiAgICAgIHRoaXMuX3BsYWNlaG9sZGVyLm5vZGUudGV4dENvbnRlbnQgPSAnJztcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF91cGRhdGVPdXRwdXRBcmVhcygpIHtcbiAgICBjb25zdCBsb2dnZXJJZHMgPSBuZXcgU2V0PHN0cmluZz4oKTtcbiAgICBjb25zdCBsb2dnZXJzID0gdGhpcy5fbG9nZ2VyUmVnaXN0cnkuZ2V0TG9nZ2VycygpO1xuXG4gICAgZm9yIChjb25zdCBsb2dnZXIgb2YgbG9nZ2Vycykge1xuICAgICAgY29uc3Qgc291cmNlID0gbG9nZ2VyLnNvdXJjZTtcbiAgICAgIGNvbnN0IHZpZXdJZCA9IGBzb3VyY2U6JHtzb3VyY2V9YDtcbiAgICAgIGxvZ2dlcklkcy5hZGQodmlld0lkKTtcblxuICAgICAgLy8gYWRkIHZpZXcgZm9yIGxvZ2dlciBpZiBub3QgZXhpc3RcbiAgICAgIGlmICghdGhpcy5fb3V0cHV0QXJlYXMuaGFzKHZpZXdJZCkpIHtcbiAgICAgICAgY29uc3Qgb3V0cHV0QXJlYSA9IG5ldyBMb2dDb25zb2xlT3V0cHV0QXJlYSh7XG4gICAgICAgICAgcmVuZGVybWltZTogbG9nZ2VyLnJlbmRlcm1pbWUhLFxuICAgICAgICAgIGNvbnRlbnRGYWN0b3J5OiBuZXcgTG9nQ29uc29sZUNvbnRlbnRGYWN0b3J5KCksXG4gICAgICAgICAgbW9kZWw6IGxvZ2dlci5vdXRwdXRBcmVhTW9kZWxcbiAgICAgICAgfSk7XG4gICAgICAgIG91dHB1dEFyZWEuaWQgPSB2aWV3SWQ7XG5cbiAgICAgICAgLy8gQXR0YWNoIHRoZSBvdXRwdXQgYXJlYSBzbyBpdCBpcyB2aXNpYmxlLCBzbyB0aGUgYWNjb3VudGluZ1xuICAgICAgICAvLyBmdW5jdGlvbnMgYmVsb3cgcmVjb3JkIHRoZSBvdXRwdXRzIGFjdHVhbGx5IGRpc3BsYXllZC5cbiAgICAgICAgY29uc3QgdyA9IG5ldyBTY3JvbGxpbmdXaWRnZXQoe1xuICAgICAgICAgIGNvbnRlbnQ6IG91dHB1dEFyZWFcbiAgICAgICAgfSk7XG4gICAgICAgIHRoaXMuYWRkV2lkZ2V0KHcpO1xuICAgICAgICB0aGlzLl9vdXRwdXRBcmVhcy5zZXQodmlld0lkLCBvdXRwdXRBcmVhKTtcblxuICAgICAgICAvLyBUaGlzIGlzIHdoZXJlIHRoZSBzb3VyY2Ugb2JqZWN0IGlzIGFzc29jaWF0ZWQgd2l0aCB0aGUgb3V0cHV0IGFyZWEuXG4gICAgICAgIC8vIFdlIGNhcHR1cmUgdGhlIHNvdXJjZSBmcm9tIHRoaXMgZW52aXJvbm1lbnQgaW4gdGhlIGNsb3N1cmUuXG4gICAgICAgIGNvbnN0IG91dHB1dFVwZGF0ZSA9IChzZW5kZXI6IExvZ0NvbnNvbGVPdXRwdXRBcmVhKSA9PiB7XG4gICAgICAgICAgLy8gSWYgdGhlIGN1cnJlbnQgbG9nIGNvbnNvbGUgcGFuZWwgc291cmNlIGlzIHRoZSBzb3VyY2UgYXNzb2NpYXRlZFxuICAgICAgICAgIC8vIHdpdGggdGhpcyBvdXRwdXQgYXJlYSwgYW5kIHRoZSBvdXRwdXQgYXJlYSBpcyB2aXNpYmxlLCB0aGVuIGVtaXRcbiAgICAgICAgICAvLyB0aGUgbG9nQ29uc29sZVBhbmVsIHNvdXJjZSBkaXNwbGF5ZWQgc2lnbmFsLlxuICAgICAgICAgIGlmICh0aGlzLnNvdXJjZSA9PT0gc291cmNlICYmIHNlbmRlci5pc1Zpc2libGUpIHtcbiAgICAgICAgICAgIC8vIFdlIGFzc3VtZSB0aGF0IHRoZSBvdXRwdXQgYXJlYSBoYXMgYmVlbiB1cGRhdGVkIHRvIHRoZSBjdXJyZW50XG4gICAgICAgICAgICAvLyB2ZXJzaW9uIG9mIHRoZSBzb3VyY2UuXG4gICAgICAgICAgICB0aGlzLl9zb3VyY2VEaXNwbGF5ZWQuZW1pdCh7XG4gICAgICAgICAgICAgIHNvdXJjZTogdGhpcy5zb3VyY2UsXG4gICAgICAgICAgICAgIHZlcnNpb246IHRoaXMuc291cmNlVmVyc2lvblxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfVxuICAgICAgICB9O1xuICAgICAgICAvLyBOb3RpZnkgbWVzc2FnZXMgd2VyZSBkaXNwbGF5ZWQgYW55IHRpbWUgdGhlIG91dHB1dCBhcmVhIGlzIHVwZGF0ZWRcbiAgICAgICAgLy8gYW5kIHVwZGF0ZSBmb3IgYW55IG91dHB1dHMgcmVuZGVyZWQgb24gY29uc3RydWN0aW9uLlxuICAgICAgICBvdXRwdXRBcmVhLm91dHB1dExlbmd0aENoYW5nZWQuY29ubmVjdChvdXRwdXRVcGRhdGUsIHRoaXMpO1xuICAgICAgICAvLyBTaW5jZSB0aGUgb3V0cHV0IGFyZWEgd2FzIGF0dGFjaGVkIGFib3ZlLCB3ZSBjYW4gcmVseSBvbiBpdHNcbiAgICAgICAgLy8gdmlzaWJpbGl0eSB0byBhY2NvdW50IGZvciB0aGUgbWVzc2FnZXMgZGlzcGxheWVkLlxuICAgICAgICBvdXRwdXRVcGRhdGUob3V0cHV0QXJlYSk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgLy8gcmVtb3ZlIG91dHB1dCBhcmVhcyB0aGF0IGRvIG5vdCBoYXZlIGNvcnJlc3BvbmRpbmcgbG9nZ2VycyBhbnltb3JlXG4gICAgY29uc3Qgdmlld0lkcyA9IHRoaXMuX291dHB1dEFyZWFzLmtleXMoKTtcblxuICAgIGZvciAoY29uc3Qgdmlld0lkIG9mIHZpZXdJZHMpIHtcbiAgICAgIGlmICghbG9nZ2VySWRzLmhhcyh2aWV3SWQpKSB7XG4gICAgICAgIGNvbnN0IG91dHB1dEFyZWEgPSB0aGlzLl9vdXRwdXRBcmVhcy5nZXQodmlld0lkKTtcbiAgICAgICAgb3V0cHV0QXJlYT8uZGlzcG9zZSgpO1xuICAgICAgICB0aGlzLl9vdXRwdXRBcmVhcy5kZWxldGUodmlld0lkKTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfbG9nZ2VyUmVnaXN0cnk6IElMb2dnZXJSZWdpc3RyeTtcbiAgcHJpdmF0ZSBfb3V0cHV0QXJlYXMgPSBuZXcgTWFwPHN0cmluZywgTG9nQ29uc29sZU91dHB1dEFyZWE+KCk7XG4gIHByaXZhdGUgX3NvdXJjZTogc3RyaW5nIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX3NvdXJjZUNoYW5nZWQgPSBuZXcgU2lnbmFsPFxuICAgIHRoaXMsXG4gICAgSUNoYW5nZWRBcmdzPHN0cmluZyB8IG51bGwsIHN0cmluZyB8IG51bGwsICdzb3VyY2UnPlxuICA+KHRoaXMpO1xuICBwcml2YXRlIF9zb3VyY2VEaXNwbGF5ZWQgPSBuZXcgU2lnbmFsPHRoaXMsIElTb3VyY2VEaXNwbGF5ZWQ+KHRoaXMpO1xuICBwcml2YXRlIF9wbGFjZWhvbGRlcjogV2lkZ2V0O1xuICBwcml2YXRlIF9sb2dnZXJzV2F0Y2hlZDogU2V0PHN0cmluZz4gPSBuZXcgU2V0KCk7XG59XG5cbmV4cG9ydCBpbnRlcmZhY2UgSVNvdXJjZURpc3BsYXllZCB7XG4gIHNvdXJjZTogc3RyaW5nIHwgbnVsbDtcbiAgdmVyc2lvbjogbnVtYmVyIHwgbnVsbDtcbn1cbiJdLCJzb3VyY2VSb290IjoiIn0=