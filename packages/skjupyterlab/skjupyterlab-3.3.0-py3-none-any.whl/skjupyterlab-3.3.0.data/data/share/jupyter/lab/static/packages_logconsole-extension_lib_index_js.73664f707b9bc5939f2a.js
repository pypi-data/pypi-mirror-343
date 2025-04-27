(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_logconsole-extension_lib_index_js"],{

/***/ "../packages/logconsole-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/logconsole-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LogLevelSwitcher": () => (/* binding */ LogLevelSwitcher),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole/@jupyterlab/logconsole");
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _status__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./status */ "../packages/logconsole-extension/lib/status.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module logconsole-extension
 */












const LOG_CONSOLE_PLUGIN_ID = '@jupyterlab/logconsole-extension:plugin';
/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.addCheckpoint = 'logconsole:add-checkpoint';
    CommandIDs.clear = 'logconsole:clear';
    CommandIDs.open = 'logconsole:open';
    CommandIDs.setLevel = 'logconsole:set-level';
})(CommandIDs || (CommandIDs = {}));
/**
 * The Log Console extension.
 */
const logConsolePlugin = {
    activate: activateLogConsole,
    id: LOG_CONSOLE_PLUGIN_ID,
    provides: _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__.ILoggerRegistry,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry, _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.IStatusBar],
    autoStart: true
};
/**
 * Activate the Log Console extension.
 */
function activateLogConsole(app, labShell, rendermime, nbtracker, translator, palette, restorer, settingRegistry, statusBar) {
    const trans = translator.load('jupyterlab');
    let logConsoleWidget = null;
    let logConsolePanel = null;
    const loggerRegistry = new _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__.LoggerRegistry({
        defaultRendermime: rendermime,
        // The maxLength is reset below from settings
        maxLength: 1000
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'logconsole'
    });
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.open,
            name: () => 'logconsole'
        });
    }
    const status = new _status__WEBPACK_IMPORTED_MODULE_11__.LogConsoleStatus({
        loggerRegistry: loggerRegistry,
        handleClick: () => {
            var _a;
            if (!logConsoleWidget) {
                createLogConsoleWidget({
                    insertMode: 'split-bottom',
                    ref: (_a = app.shell.currentWidget) === null || _a === void 0 ? void 0 : _a.id
                });
            }
            else {
                app.shell.activateById(logConsoleWidget.id);
            }
        },
        translator
    });
    const createLogConsoleWidget = (options = {}) => {
        logConsolePanel = new _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__.LogConsolePanel(loggerRegistry, translator);
        logConsolePanel.source =
            options.source !== undefined
                ? options.source
                : nbtracker.currentWidget
                    ? nbtracker.currentWidget.context.path
                    : null;
        logConsoleWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: logConsolePanel });
        logConsoleWidget.addClass('jp-LogConsole');
        logConsoleWidget.title.closable = true;
        logConsoleWidget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.listIcon;
        logConsoleWidget.title.label = trans.__('Log Console');
        const addCheckpointButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButton({
            commands: app.commands,
            id: CommandIDs.addCheckpoint
        });
        const clearButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButton({
            commands: app.commands,
            id: CommandIDs.clear
        });
        logConsoleWidget.toolbar.addItem('lab-log-console-add-checkpoint', addCheckpointButton);
        logConsoleWidget.toolbar.addItem('lab-log-console-clear', clearButton);
        logConsoleWidget.toolbar.addItem('level', new LogLevelSwitcher(logConsoleWidget.content, translator));
        logConsolePanel.sourceChanged.connect(() => {
            app.commands.notifyCommandChanged();
        });
        logConsolePanel.sourceDisplayed.connect((panel, { source, version }) => {
            status.model.sourceDisplayed(source, version);
        });
        logConsoleWidget.disposed.connect(() => {
            logConsoleWidget = null;
            logConsolePanel = null;
            app.commands.notifyCommandChanged();
        });
        app.shell.add(logConsoleWidget, 'down', {
            ref: options.ref,
            mode: options.insertMode
        });
        void tracker.add(logConsoleWidget);
        app.shell.activateById(logConsoleWidget.id);
        logConsoleWidget.update();
        app.commands.notifyCommandChanged();
    };
    app.commands.addCommand(CommandIDs.open, {
        label: trans.__('Show Log Console'),
        execute: (options = {}) => {
            // Toggle the display
            if (logConsoleWidget) {
                logConsoleWidget.dispose();
            }
            else {
                createLogConsoleWidget(options);
            }
        },
        isToggled: () => {
            return logConsoleWidget !== null;
        }
    });
    app.commands.addCommand(CommandIDs.addCheckpoint, {
        execute: () => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.checkpoint();
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.addIcon,
        isEnabled: () => !!logConsolePanel && logConsolePanel.source !== null,
        label: trans.__('Add Checkpoint')
    });
    app.commands.addCommand(CommandIDs.clear, {
        execute: () => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.clear();
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.clearIcon,
        isEnabled: () => !!logConsolePanel && logConsolePanel.source !== null,
        label: trans.__('Clear Log')
    });
    function toTitleCase(value) {
        return value.length === 0 ? value : value[0].toUpperCase() + value.slice(1);
    }
    app.commands.addCommand(CommandIDs.setLevel, {
        // TODO: find good icon class
        execute: (args) => {
            if (logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) {
                logConsolePanel.logger.level = args.level;
            }
        },
        isEnabled: () => !!logConsolePanel && logConsolePanel.source !== null,
        label: args => trans.__('Set Log Level to %1', toTitleCase(args.level))
    });
    if (palette) {
        palette.addItem({
            command: CommandIDs.open,
            category: trans.__('Main Area')
        });
    }
    if (statusBar) {
        statusBar.registerStatusItem('@jupyterlab/logconsole-extension:status', {
            item: status,
            align: 'left',
            isActive: () => { var _a; return ((_a = status.model) === null || _a === void 0 ? void 0 : _a.version) > 0; },
            activeStateChanged: status.model.stateChanged
        });
    }
    function setSource(newValue) {
        if (logConsoleWidget && newValue === logConsoleWidget) {
            // Do not change anything if we are just focusing on ourselves
            return;
        }
        let source;
        if (newValue && nbtracker.has(newValue)) {
            source = newValue.context.path;
        }
        else {
            source = null;
        }
        if (logConsolePanel) {
            logConsolePanel.source = source;
        }
        status.model.source = source;
    }
    void app.restored.then(() => {
        // Set source only after app is restored in order to allow restorer to
        // restore previous source first, which may set the renderer
        setSource(labShell.currentWidget);
        labShell.currentChanged.connect((_, { newValue }) => setSource(newValue));
    });
    if (settingRegistry) {
        const updateSettings = (settings) => {
            loggerRegistry.maxLength = settings.get('maxLogEntries')
                .composite;
            status.model.flashEnabled = settings.get('flash').composite;
        };
        Promise.all([settingRegistry.load(LOG_CONSOLE_PLUGIN_ID), app.restored])
            .then(([settings]) => {
            updateSettings(settings);
            settings.changed.connect(settings => {
                updateSettings(settings);
            });
        })
            .catch((reason) => {
            console.error(reason.message);
        });
    }
    return loggerRegistry;
}
/**
 * A toolbar widget that switches log levels.
 */
class LogLevelSwitcher extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Construct a new cell type switcher.
     */
    constructor(widget, translator) {
        super();
        /**
         * Handle `change` events for the HTMLSelect component.
         */
        this.handleChange = (event) => {
            if (this._logConsole.logger) {
                this._logConsole.logger.level = event.target.value;
            }
            this.update();
        };
        /**
         * Handle `keydown` events for the HTMLSelect component.
         */
        this.handleKeyDown = (event) => {
            if (event.keyCode === 13) {
                this._logConsole.activate();
            }
        };
        this._id = `level-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.UUID.uuid4()}`;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.addClass('jp-LogConsole-toolbarLogLevel');
        this._logConsole = widget;
        if (widget.source) {
            this.update();
        }
        widget.sourceChanged.connect(this._updateSource, this);
    }
    _updateSource(sender, { oldValue, newValue }) {
        // Transfer stateChanged handler to new source logger
        if (oldValue !== null) {
            const logger = sender.loggerRegistry.getLogger(oldValue);
            logger.stateChanged.disconnect(this.update, this);
        }
        if (newValue !== null) {
            const logger = sender.loggerRegistry.getLogger(newValue);
            logger.stateChanged.connect(this.update, this);
        }
        this.update();
    }
    render() {
        const logger = this._logConsole.logger;
        return (react__WEBPACK_IMPORTED_MODULE_10__.createElement(react__WEBPACK_IMPORTED_MODULE_10__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_10__.createElement("label", { htmlFor: this._id, className: logger === null
                    ? 'jp-LogConsole-toolbarLogLevel-disabled'
                    : undefined }, this._trans.__('Log Level:')),
            react__WEBPACK_IMPORTED_MODULE_10__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.HTMLSelect, { id: this._id, className: "jp-LogConsole-toolbarLogLevelDropdown", onChange: this.handleChange, onKeyDown: this.handleKeyDown, value: logger === null || logger === void 0 ? void 0 : logger.level, "aria-label": this._trans.__('Log level'), disabled: logger === null, options: logger === null
                    ? []
                    : [
                        [this._trans.__('Critical'), 'Critical'],
                        [this._trans.__('Error'), 'Error'],
                        [this._trans.__('Warning'), 'Warning'],
                        [this._trans.__('Info'), 'Info'],
                        [this._trans.__('Debug'), 'Debug']
                    ].map(data => ({
                        label: data[0],
                        value: data[1].toLowerCase()
                    })) })));
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (logConsolePlugin);


/***/ }),

/***/ "../packages/logconsole-extension/lib/status.js":
/*!******************************************************!*\
  !*** ../packages/logconsole-extension/lib/status.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LogConsoleStatus": () => (/* binding */ LogConsoleStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * A pure functional component for a Log Console status item.
 *
 * @param props - the props for the component.
 *
 * @returns a tsx component for rendering the Log Console status.
 */
function LogConsoleStatusComponent(props) {
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
    const trans = translator.load('jupyterlab');
    let title = '';
    if (props.newMessages > 0) {
        title = trans.__('%1 new messages, %2 log entries for %3', props.newMessages, props.logEntries, props.source);
    }
    else {
        title += trans.__('%1 log entries for %2', props.logEntries, props.source);
    }
    return (react__WEBPACK_IMPORTED_MODULE_5___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.GroupItem, { spacing: 0, onClick: props.handleClick, title: title },
        react__WEBPACK_IMPORTED_MODULE_5___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.listIcon.react, { top: '2px', stylesheet: 'statusBar' }),
        props.newMessages > 0 ? react__WEBPACK_IMPORTED_MODULE_5___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { source: props.newMessages }) : react__WEBPACK_IMPORTED_MODULE_5___default().createElement((react__WEBPACK_IMPORTED_MODULE_5___default().Fragment), null)));
}
/**
 * A VDomRenderer widget for displaying the status of Log Console logs.
 */
class LogConsoleStatus extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Construct the log console status widget.
     *
     * @param options - The status widget initialization options.
     */
    constructor(options) {
        super(new LogConsoleStatus.Model(options.loggerRegistry));
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this._handleClick = options.handleClick;
        this.addClass(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.interactiveItem);
        this.addClass('jp-LogConsoleStatusItem');
    }
    /**
     * Render the log console status item.
     */
    render() {
        if (this.model === null || this.model.version === 0) {
            return null;
        }
        const { flashEnabled, messages, source, version, versionDisplayed, versionNotified } = this.model;
        if (source !== null && flashEnabled && version > versionNotified) {
            this._flashHighlight();
            this.model.sourceNotified(source, version);
        }
        else if (source !== null && flashEnabled && version > versionDisplayed) {
            this._showHighlighted();
        }
        else {
            this._clearHighlight();
        }
        return (react__WEBPACK_IMPORTED_MODULE_5___default().createElement(LogConsoleStatusComponent, { handleClick: this._handleClick, logEntries: messages, newMessages: version - versionDisplayed, source: this.model.source, translator: this.translator }));
    }
    _flashHighlight() {
        this._showHighlighted();
        // To make sure the browser triggers the animation, we remove the class,
        // wait for an animation frame, then add it back
        this.removeClass('jp-LogConsole-flash');
        requestAnimationFrame(() => {
            this.addClass('jp-LogConsole-flash');
        });
    }
    _showHighlighted() {
        this.addClass('jp-mod-selected');
    }
    _clearHighlight() {
        this.removeClass('jp-LogConsole-flash');
        this.removeClass('jp-mod-selected');
    }
}
/**
 * A namespace for Log Console log status.
 */
(function (LogConsoleStatus) {
    /**
     * A VDomModel for the LogConsoleStatus item.
     */
    class Model extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
        /**
         * Create a new LogConsoleStatus model.
         *
         * @param loggerRegistry - The logger registry providing the logs.
         */
        constructor(loggerRegistry) {
            super();
            /**
             * A signal emitted when the flash enablement changes.
             */
            this.flashEnabledChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
            this._flashEnabled = true;
            this._source = null;
            /**
             * The view status of each source.
             *
             * #### Notes
             * Keys are source names, value is a list of two numbers. The first
             * represents the version of the messages that was last displayed to the
             * user, the second represents the version that we last notified the user
             * about.
             */
            this._sourceVersion = new Map();
            this._loggerRegistry = loggerRegistry;
            this._loggerRegistry.registryChanged.connect(this._handleLogRegistryChange, this);
            this._handleLogRegistryChange();
        }
        /**
         * Number of messages currently in the current source.
         */
        get messages() {
            if (this._source === null) {
                return 0;
            }
            const logger = this._loggerRegistry.getLogger(this._source);
            return logger.length;
        }
        /**
         * The number of messages ever stored by the current source.
         */
        get version() {
            if (this._source === null) {
                return 0;
            }
            const logger = this._loggerRegistry.getLogger(this._source);
            return logger.version;
        }
        /**
         * The name of the active log source
         */
        get source() {
            return this._source;
        }
        set source(name) {
            if (this._source === name) {
                return;
            }
            this._source = name;
            // refresh rendering
            this.stateChanged.emit();
        }
        /**
         * The last source version that was displayed.
         */
        get versionDisplayed() {
            var _a, _b;
            if (this._source === null) {
                return 0;
            }
            return (_b = (_a = this._sourceVersion.get(this._source)) === null || _a === void 0 ? void 0 : _a.lastDisplayed) !== null && _b !== void 0 ? _b : 0;
        }
        /**
         * The last source version we notified the user about.
         */
        get versionNotified() {
            var _a, _b;
            if (this._source === null) {
                return 0;
            }
            return (_b = (_a = this._sourceVersion.get(this._source)) === null || _a === void 0 ? void 0 : _a.lastNotified) !== null && _b !== void 0 ? _b : 0;
        }
        /**
         * Flag to toggle flashing when new logs added.
         */
        get flashEnabled() {
            return this._flashEnabled;
        }
        set flashEnabled(enabled) {
            if (this._flashEnabled === enabled) {
                return;
            }
            this._flashEnabled = enabled;
            this.flashEnabledChanged.emit();
            // refresh rendering
            this.stateChanged.emit();
        }
        /**
         * Record the last source version displayed to the user.
         *
         * @param source - The name of the log source.
         * @param version - The version of the log that was displayed.
         *
         * #### Notes
         * This will also update the last notified version so that the last
         * notified version is always at least the last displayed version.
         */
        sourceDisplayed(source, version) {
            if (source === null || version === null) {
                return;
            }
            const versions = this._sourceVersion.get(source);
            let change = false;
            if (versions.lastDisplayed < version) {
                versions.lastDisplayed = version;
                change = true;
            }
            if (versions.lastNotified < version) {
                versions.lastNotified = version;
                change = true;
            }
            if (change && source === this._source) {
                this.stateChanged.emit();
            }
        }
        /**
         * Record a source version we notified the user about.
         *
         * @param source - The name of the log source.
         * @param version - The version of the log.
         */
        sourceNotified(source, version) {
            if (source === null) {
                return;
            }
            const versions = this._sourceVersion.get(source);
            if (versions.lastNotified < version) {
                versions.lastNotified = version;
                if (source === this._source) {
                    this.stateChanged.emit();
                }
            }
        }
        _handleLogRegistryChange() {
            const loggers = this._loggerRegistry.getLoggers();
            for (const logger of loggers) {
                if (!this._sourceVersion.has(logger.source)) {
                    logger.contentChanged.connect(this._handleLogContentChange, this);
                    this._sourceVersion.set(logger.source, {
                        lastDisplayed: 0,
                        lastNotified: 0
                    });
                }
            }
        }
        _handleLogContentChange({ source }, change) {
            if (source === this._source) {
                this.stateChanged.emit();
            }
        }
    }
    LogConsoleStatus.Model = Model;
})(LogConsoleStatus || (LogConsoleStatus = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbG9nY29uc29sZS1leHRlbnNpb24vc3JjL2luZGV4LnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbG9nY29uc29sZS1leHRlbnNpb24vc3JjL3N0YXR1cy50c3giXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTzhCO0FBT0g7QUFPRTtBQUN1QztBQUNWO0FBQ0U7QUFDWjtBQUtsQjtBQU1FO0FBQ007QUFFVjtBQUNhO0FBRTVDLE1BQU0scUJBQXFCLEdBQUcseUNBQXlDLENBQUM7QUFFeEU7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FLbkI7QUFMRCxXQUFVLFVBQVU7SUFDTCx3QkFBYSxHQUFHLDJCQUEyQixDQUFDO0lBQzVDLGdCQUFLLEdBQUcsa0JBQWtCLENBQUM7SUFDM0IsZUFBSSxHQUFHLGlCQUFpQixDQUFDO0lBQ3pCLG1CQUFRLEdBQUcsc0JBQXNCLENBQUM7QUFDakQsQ0FBQyxFQUxTLFVBQVUsS0FBVixVQUFVLFFBS25CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLGdCQUFnQixHQUEyQztJQUMvRCxRQUFRLEVBQUUsa0JBQWtCO0lBQzVCLEVBQUUsRUFBRSxxQkFBcUI7SUFDekIsUUFBUSxFQUFFLG1FQUFlO0lBQ3pCLFFBQVEsRUFBRSxDQUFDLDhEQUFTLEVBQUUsdUVBQW1CLEVBQUUsa0VBQWdCLEVBQUUsZ0VBQVcsQ0FBQztJQUN6RSxRQUFRLEVBQUUsQ0FBQyxpRUFBZSxFQUFFLG9FQUFlLEVBQUUseUVBQWdCLEVBQUUsNkRBQVUsQ0FBQztJQUMxRSxTQUFTLEVBQUUsSUFBSTtDQUNoQixDQUFDO0FBRUY7O0dBRUc7QUFDSCxTQUFTLGtCQUFrQixDQUN6QixHQUFv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T0FBTyxFQUFFO2dCQUM1QixJQUFJLENBQUMsSUFBSSxDQUFDLGNBQWMsQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLE1BQU0sQ0FBQyxFQUFFO29CQUMzQyxNQUFNLENBQUMsY0FBYyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsdUJBQXVCLEVBQUUsSUFBSSxDQUFDLENBQUM7b0JBQ2xFLElBQUksQ0FBQyxjQUFjLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQyxNQUFNLEVBQUU7d0JBQ3JDLGFBQWEsRUFBRSxDQUFDO3dCQUNoQixZQUFZLEVBQUUsQ0FBQztxQkFDaEIsQ0FBQyxDQUFDO2lCQUNKO2FBQ0Y7UUFDSCxDQUFDO1FBRU8sdUJBQXVCLENBQzdCLEVBQUUsTUFBTSxFQUFXLEVBQ25CLE1BQXNCO1lBRXRCLElBQUksTUFBTSxLQUFLLElBQUksQ0FBQyxPQUFPLEVBQUU7Z0JBQzNCLElBQUksQ0FBQyxZQUFZLENBQUMsSUFBSSxFQUFFLENBQUM7YUFDMUI7UUFDSCxDQUFDO0tBbUJGO0lBdkxZLHNCQUFLLFFBdUxqQjtBQTJCSCxDQUFDLEVBdE5nQixnQkFBZ0IsS0FBaEIsZ0JBQWdCLFFBc05oQyIsImZpbGUiOiJwYWNrYWdlc19sb2djb25zb2xlLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuNzM2NjRmNzA3YjliYzU5MzlmMmEuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBsb2djb25zb2xlLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTaGVsbCxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBDb21tYW5kVG9vbGJhckJ1dHRvbixcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBNYWluQXJlYVdpZGdldCxcbiAgUmVhY3RXaWRnZXQsXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSUNoYW5nZWRBcmdzIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIElMb2dnZXJSZWdpc3RyeSxcbiAgTG9nQ29uc29sZVBhbmVsLFxuICBMb2dnZXJSZWdpc3RyeSxcbiAgTG9nTGV2ZWxcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvbG9nY29uc29sZSc7XG5pbXBvcnQgeyBJTm90ZWJvb2tUcmFja2VyLCBOb3RlYm9va1BhbmVsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbm90ZWJvb2snO1xuaW1wb3J0IHsgSVJlbmRlck1pbWVSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJU3RhdHVzQmFyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgYWRkSWNvbixcbiAgY2xlYXJJY29uLFxuICBIVE1MU2VsZWN0LFxuICBsaXN0SWNvblxufSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFVVSUQgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBEb2NrTGF5b3V0LCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgTG9nQ29uc29sZVN0YXR1cyB9IGZyb20gJy4vc3RhdHVzJztcblxuY29uc3QgTE9HX0NPTlNPTEVfUExVR0lOX0lEID0gJ0BqdXB5dGVybGFiL2xvZ2NvbnNvbGUtZXh0ZW5zaW9uOnBsdWdpbic7XG5cbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgYWRkQ2hlY2twb2ludCA9ICdsb2djb25zb2xlOmFkZC1jaGVja3BvaW50JztcbiAgZXhwb3J0IGNvbnN0IGNsZWFyID0gJ2xvZ2NvbnNvbGU6Y2xlYXInO1xuICBleHBvcnQgY29uc3Qgb3BlbiA9ICdsb2djb25zb2xlOm9wZW4nO1xuICBleHBvcnQgY29uc3Qgc2V0TGV2ZWwgPSAnbG9nY29uc29sZTpzZXQtbGV2ZWwnO1xufVxuXG4vKipcbiAqIFRoZSBMb2cgQ29uc29sZSBleHRlbnNpb24uXG4gKi9cbmNvbnN0IGxvZ0NvbnNvbGVQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTG9nZ2VyUmVnaXN0cnk+ID0ge1xuICBhY3RpdmF0ZTogYWN0aXZhdGVMb2dDb25zb2xlLFxuICBpZDogTE9HX0NPTlNPTEVfUExVR0lOX0lELFxuICBwcm92aWRlczogSUxvZ2dlclJlZ2lzdHJ5LFxuICByZXF1aXJlczogW0lMYWJTaGVsbCwgSVJlbmRlck1pbWVSZWdpc3RyeSwgSU5vdGVib29rVHJhY2tlciwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZSwgSUxheW91dFJlc3RvcmVyLCBJU2V0dGluZ1JlZ2lzdHJ5LCBJU3RhdHVzQmFyXSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBMb2cgQ29uc29sZSBleHRlbnNpb24uXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlTG9nQ29uc29sZShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIGxhYlNoZWxsOiBJTGFiU2hlbGwsXG4gIHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIG5idHJhY2tlcjogSU5vdGVib29rVHJhY2tlcixcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGwsXG4gIHJlc3RvcmVyOiBJTGF5b3V0UmVzdG9yZXIgfCBudWxsLFxuICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsLFxuICBzdGF0dXNCYXI6IElTdGF0dXNCYXIgfCBudWxsXG4pOiBJTG9nZ2VyUmVnaXN0cnkge1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBsZXQgbG9nQ29uc29sZVdpZGdldDogTWFpbkFyZWFXaWRnZXQ8TG9nQ29uc29sZVBhbmVsPiB8IG51bGwgPSBudWxsO1xuICBsZXQgbG9nQ29uc29sZVBhbmVsOiBMb2dDb25zb2xlUGFuZWwgfCBudWxsID0gbnVsbDtcblxuICBjb25zdCBsb2dnZXJSZWdpc3RyeSA9IG5ldyBMb2dnZXJSZWdpc3RyeSh7XG4gICAgZGVmYXVsdFJlbmRlcm1pbWU6IHJlbmRlcm1pbWUsXG4gICAgLy8gVGhlIG1heExlbmd0aCBpcyByZXNldCBiZWxvdyBmcm9tIHNldHRpbmdzXG4gICAgbWF4TGVuZ3RoOiAxMDAwXG4gIH0pO1xuXG4gIGNvbnN0IHRyYWNrZXIgPSBuZXcgV2lkZ2V0VHJhY2tlcjxNYWluQXJlYVdpZGdldDxMb2dDb25zb2xlUGFuZWw+Pih7XG4gICAgbmFtZXNwYWNlOiAnbG9nY29uc29sZSdcbiAgfSk7XG5cbiAgaWYgKHJlc3RvcmVyKSB7XG4gICAgdm9pZCByZXN0b3Jlci5yZXN0b3JlKHRyYWNrZXIsIHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMub3BlbixcbiAgICAgIG5hbWU6ICgpID0+ICdsb2djb25zb2xlJ1xuICAgIH0pO1xuICB9XG5cbiAgY29uc3Qgc3RhdHVzID0gbmV3IExvZ0NvbnNvbGVTdGF0dXMoe1xuICAgIGxvZ2dlclJlZ2lzdHJ5OiBsb2dnZXJSZWdpc3RyeSxcbiAgICBoYW5kbGVDbGljazogKCkgPT4ge1xuICAgICAgaWYgKCFsb2dDb25zb2xlV2lkZ2V0KSB7XG4gICAgICAgIGNyZWF0ZUxvZ0NvbnNvbGVXaWRnZXQoe1xuICAgICAgICAgIGluc2VydE1vZGU6ICdzcGxpdC1ib3R0b20nLFxuICAgICAgICAgIHJlZjogYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ/LmlkXG4gICAgICAgIH0pO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgYXBwLnNoZWxsLmFjdGl2YXRlQnlJZChsb2dDb25zb2xlV2lkZ2V0LmlkKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIHRyYW5zbGF0b3JcbiAgfSk7XG5cbiAgaW50ZXJmYWNlIElMb2dDb25zb2xlT3B0aW9ucyB7XG4gICAgc291cmNlPzogc3RyaW5nO1xuICAgIGluc2VydE1vZGU/OiBEb2NrTGF5b3V0Lkluc2VydE1vZGU7XG4gICAgcmVmPzogc3RyaW5nO1xuICB9XG5cbiAgY29uc3QgY3JlYXRlTG9nQ29uc29sZVdpZGdldCA9IChvcHRpb25zOiBJTG9nQ29uc29sZU9wdGlvbnMgPSB7fSkgPT4ge1xuICAgIGxvZ0NvbnNvbGVQYW5lbCA9IG5ldyBMb2dDb25zb2xlUGFuZWwobG9nZ2VyUmVnaXN0cnksIHRyYW5zbGF0b3IpO1xuXG4gICAgbG9nQ29uc29sZVBhbmVsLnNvdXJjZSA9XG4gICAgICBvcHRpb25zLnNvdXJjZSAhPT0gdW5kZWZpbmVkXG4gICAgICAgID8gb3B0aW9ucy5zb3VyY2VcbiAgICAgICAgOiBuYnRyYWNrZXIuY3VycmVudFdpZGdldFxuICAgICAgICA/IG5idHJhY2tlci5jdXJyZW50V2lkZ2V0LmNvbnRleHQucGF0aFxuICAgICAgICA6IG51bGw7XG5cbiAgICBsb2dDb25zb2xlV2lkZ2V0ID0gbmV3IE1haW5BcmVhV2lkZ2V0KHsgY29udGVudDogbG9nQ29uc29sZVBhbmVsIH0pO1xuICAgIGxvZ0NvbnNvbGVXaWRnZXQuYWRkQ2xhc3MoJ2pwLUxvZ0NvbnNvbGUnKTtcbiAgICBsb2dDb25zb2xlV2lkZ2V0LnRpdGxlLmNsb3NhYmxlID0gdHJ1ZTtcbiAgICBsb2dDb25zb2xlV2lkZ2V0LnRpdGxlLmljb24gPSBsaXN0SWNvbjtcbiAgICBsb2dDb25zb2xlV2lkZ2V0LnRpdGxlLmxhYmVsID0gdHJhbnMuX18oJ0xvZyBDb25zb2xlJyk7XG5cbiAgICBjb25zdCBhZGRDaGVja3BvaW50QnV0dG9uID0gbmV3IENvbW1hbmRUb29sYmFyQnV0dG9uKHtcbiAgICAgIGNvbW1hbmRzOiBhcHAuY29tbWFuZHMsXG4gICAgICBpZDogQ29tbWFuZElEcy5hZGRDaGVja3BvaW50XG4gICAgfSk7XG5cbiAgICBjb25zdCBjbGVhckJ1dHRvbiA9IG5ldyBDb21tYW5kVG9vbGJhckJ1dHRvbih7XG4gICAgICBjb21tYW5kczogYXBwLmNvbW1hbmRzLFxuICAgICAgaWQ6IENvbW1hbmRJRHMuY2xlYXJcbiAgICB9KTtcblxuICAgIGxvZ0NvbnNvbGVXaWRnZXQudG9vbGJhci5hZGRJdGVtKFxuICAgICAgJ2xhYi1sb2ctY29uc29sZS1hZGQtY2hlY2twb2ludCcsXG4gICAgICBhZGRDaGVja3BvaW50QnV0dG9uXG4gICAgKTtcbiAgICBsb2dDb25zb2xlV2lkZ2V0LnRvb2xiYXIuYWRkSXRlbSgnbGFiLWxvZy1jb25zb2xlLWNsZWFyJywgY2xlYXJCdXR0b24pO1xuXG4gICAgbG9nQ29uc29sZVdpZGdldC50b29sYmFyLmFkZEl0ZW0oXG4gICAgICAnbGV2ZWwnLFxuICAgICAgbmV3IExvZ0xldmVsU3dpdGNoZXIobG9nQ29uc29sZVdpZGdldC5jb250ZW50LCB0cmFuc2xhdG9yKVxuICAgICk7XG5cbiAgICBsb2dDb25zb2xlUGFuZWwuc291cmNlQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZCgpO1xuICAgIH0pO1xuXG4gICAgbG9nQ29uc29sZVBhbmVsLnNvdXJjZURpc3BsYXllZC5jb25uZWN0KChwYW5lbCwgeyBzb3VyY2UsIHZlcnNpb24gfSkgPT4ge1xuICAgICAgc3RhdHVzLm1vZGVsLnNvdXJjZURpc3BsYXllZChzb3VyY2UsIHZlcnNpb24pO1xuICAgIH0pO1xuXG4gICAgbG9nQ29uc29sZVdpZGdldC5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIGxvZ0NvbnNvbGVXaWRnZXQgPSBudWxsO1xuICAgICAgbG9nQ29uc29sZVBhbmVsID0gbnVsbDtcbiAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZCgpO1xuICAgIH0pO1xuXG4gICAgYXBwLnNoZWxsLmFkZChsb2dDb25zb2xlV2lkZ2V0LCAnZG93bicsIHtcbiAgICAgIHJlZjogb3B0aW9ucy5yZWYsXG4gICAgICBtb2RlOiBvcHRpb25zLmluc2VydE1vZGVcbiAgICB9KTtcbiAgICB2b2lkIHRyYWNrZXIuYWRkKGxvZ0NvbnNvbGVXaWRnZXQpO1xuICAgIGFwcC5zaGVsbC5hY3RpdmF0ZUJ5SWQobG9nQ29uc29sZVdpZGdldC5pZCk7XG5cbiAgICBsb2dDb25zb2xlV2lkZ2V0LnVwZGF0ZSgpO1xuICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZCgpO1xuICB9O1xuXG4gIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3Blbiwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnU2hvdyBMb2cgQ29uc29sZScpLFxuICAgIGV4ZWN1dGU6IChvcHRpb25zOiBJTG9nQ29uc29sZU9wdGlvbnMgPSB7fSkgPT4ge1xuICAgICAgLy8gVG9nZ2xlIHRoZSBkaXNwbGF5XG4gICAgICBpZiAobG9nQ29uc29sZVdpZGdldCkge1xuICAgICAgICBsb2dDb25zb2xlV2lkZ2V0LmRpc3Bvc2UoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGNyZWF0ZUxvZ0NvbnNvbGVXaWRnZXQob3B0aW9ucyk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc1RvZ2dsZWQ6ICgpID0+IHtcbiAgICAgIHJldHVybiBsb2dDb25zb2xlV2lkZ2V0ICE9PSBudWxsO1xuICAgIH1cbiAgfSk7XG5cbiAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5hZGRDaGVja3BvaW50LCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgbG9nQ29uc29sZVBhbmVsPy5sb2dnZXI/LmNoZWNrcG9pbnQoKTtcbiAgICB9LFxuICAgIGljb246IGFkZEljb24sXG4gICAgaXNFbmFibGVkOiAoKSA9PiAhIWxvZ0NvbnNvbGVQYW5lbCAmJiBsb2dDb25zb2xlUGFuZWwuc291cmNlICE9PSBudWxsLFxuICAgIGxhYmVsOiB0cmFucy5fXygnQWRkIENoZWNrcG9pbnQnKVxuICB9KTtcblxuICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNsZWFyLCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgbG9nQ29uc29sZVBhbmVsPy5sb2dnZXI/LmNsZWFyKCk7XG4gICAgfSxcbiAgICBpY29uOiBjbGVhckljb24sXG4gICAgaXNFbmFibGVkOiAoKSA9PiAhIWxvZ0NvbnNvbGVQYW5lbCAmJiBsb2dDb25zb2xlUGFuZWwuc291cmNlICE9PSBudWxsLFxuICAgIGxhYmVsOiB0cmFucy5fXygnQ2xlYXIgTG9nJylcbiAgfSk7XG5cbiAgZnVuY3Rpb24gdG9UaXRsZUNhc2UodmFsdWU6IHN0cmluZykge1xuICAgIHJldHVybiB2YWx1ZS5sZW5ndGggPT09IDAgPyB2YWx1ZSA6IHZhbHVlWzBdLnRvVXBwZXJDYXNlKCkgKyB2YWx1ZS5zbGljZSgxKTtcbiAgfVxuXG4gIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2V0TGV2ZWwsIHtcbiAgICAvLyBUT0RPOiBmaW5kIGdvb2QgaWNvbiBjbGFzc1xuICAgIGV4ZWN1dGU6IChhcmdzOiB7IGxldmVsOiBMb2dMZXZlbCB9KSA9PiB7XG4gICAgICBpZiAobG9nQ29uc29sZVBhbmVsPy5sb2dnZXIpIHtcbiAgICAgICAgbG9nQ29uc29sZVBhbmVsLmxvZ2dlci5sZXZlbCA9IGFyZ3MubGV2ZWw7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+ICEhbG9nQ29uc29sZVBhbmVsICYmIGxvZ0NvbnNvbGVQYW5lbC5zb3VyY2UgIT09IG51bGwsXG4gICAgbGFiZWw6IGFyZ3MgPT5cbiAgICAgIHRyYW5zLl9fKCdTZXQgTG9nIExldmVsIHRvICUxJywgdG9UaXRsZUNhc2UoYXJncy5sZXZlbCBhcyBzdHJpbmcpKVxuICB9KTtcblxuICBpZiAocGFsZXR0ZSkge1xuICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLm9wZW4sXG4gICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ01haW4gQXJlYScpXG4gICAgfSk7XG4gIH1cbiAgaWYgKHN0YXR1c0Jhcikge1xuICAgIHN0YXR1c0Jhci5yZWdpc3RlclN0YXR1c0l0ZW0oJ0BqdXB5dGVybGFiL2xvZ2NvbnNvbGUtZXh0ZW5zaW9uOnN0YXR1cycsIHtcbiAgICAgIGl0ZW06IHN0YXR1cyxcbiAgICAgIGFsaWduOiAnbGVmdCcsXG4gICAgICBpc0FjdGl2ZTogKCkgPT4gc3RhdHVzLm1vZGVsPy52ZXJzaW9uID4gMCxcbiAgICAgIGFjdGl2ZVN0YXRlQ2hhbmdlZDogc3RhdHVzLm1vZGVsIS5zdGF0ZUNoYW5nZWRcbiAgICB9KTtcbiAgfVxuXG4gIGZ1bmN0aW9uIHNldFNvdXJjZShuZXdWYWx1ZTogV2lkZ2V0IHwgbnVsbCkge1xuICAgIGlmIChsb2dDb25zb2xlV2lkZ2V0ICYmIG5ld1ZhbHVlID09PSBsb2dDb25zb2xlV2lkZ2V0KSB7XG4gICAgICAvLyBEbyBub3QgY2hhbmdlIGFueXRoaW5nIGlmIHdlIGFyZSBqdXN0IGZvY3VzaW5nIG9uIG91cnNlbHZlc1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGxldCBzb3VyY2U6IHN0cmluZyB8IG51bGw7XG4gICAgaWYgKG5ld1ZhbHVlICYmIG5idHJhY2tlci5oYXMobmV3VmFsdWUpKSB7XG4gICAgICBzb3VyY2UgPSAobmV3VmFsdWUgYXMgTm90ZWJvb2tQYW5lbCkuY29udGV4dC5wYXRoO1xuICAgIH0gZWxzZSB7XG4gICAgICBzb3VyY2UgPSBudWxsO1xuICAgIH1cbiAgICBpZiAobG9nQ29uc29sZVBhbmVsKSB7XG4gICAgICBsb2dDb25zb2xlUGFuZWwuc291cmNlID0gc291cmNlO1xuICAgIH1cbiAgICBzdGF0dXMubW9kZWwuc291cmNlID0gc291cmNlO1xuICB9XG4gIHZvaWQgYXBwLnJlc3RvcmVkLnRoZW4oKCkgPT4ge1xuICAgIC8vIFNldCBzb3VyY2Ugb25seSBhZnRlciBhcHAgaXMgcmVzdG9yZWQgaW4gb3JkZXIgdG8gYWxsb3cgcmVzdG9yZXIgdG9cbiAgICAvLyByZXN0b3JlIHByZXZpb3VzIHNvdXJjZSBmaXJzdCwgd2hpY2ggbWF5IHNldCB0aGUgcmVuZGVyZXJcbiAgICBzZXRTb3VyY2UobGFiU2hlbGwuY3VycmVudFdpZGdldCk7XG4gICAgbGFiU2hlbGwuY3VycmVudENoYW5nZWQuY29ubmVjdCgoXywgeyBuZXdWYWx1ZSB9KSA9PiBzZXRTb3VyY2UobmV3VmFsdWUpKTtcbiAgfSk7XG5cbiAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgIGNvbnN0IHVwZGF0ZVNldHRpbmdzID0gKHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyk6IHZvaWQgPT4ge1xuICAgICAgbG9nZ2VyUmVnaXN0cnkubWF4TGVuZ3RoID0gc2V0dGluZ3MuZ2V0KCdtYXhMb2dFbnRyaWVzJylcbiAgICAgICAgLmNvbXBvc2l0ZSBhcyBudW1iZXI7XG4gICAgICBzdGF0dXMubW9kZWwuZmxhc2hFbmFibGVkID0gc2V0dGluZ3MuZ2V0KCdmbGFzaCcpLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgIH07XG5cbiAgICBQcm9taXNlLmFsbChbc2V0dGluZ1JlZ2lzdHJ5LmxvYWQoTE9HX0NPTlNPTEVfUExVR0lOX0lEKSwgYXBwLnJlc3RvcmVkXSlcbiAgICAgIC50aGVuKChbc2V0dGluZ3NdKSA9PiB7XG4gICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KHNldHRpbmdzID0+IHtcbiAgICAgICAgICB1cGRhdGVTZXR0aW5ncyhzZXR0aW5ncyk7XG4gICAgICAgIH0pO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICBjb25zb2xlLmVycm9yKHJlYXNvbi5tZXNzYWdlKTtcbiAgICAgIH0pO1xuICB9XG5cbiAgcmV0dXJuIGxvZ2dlclJlZ2lzdHJ5O1xufVxuXG4vKipcbiAqIEEgdG9vbGJhciB3aWRnZXQgdGhhdCBzd2l0Y2hlcyBsb2cgbGV2ZWxzLlxuICovXG5leHBvcnQgY2xhc3MgTG9nTGV2ZWxTd2l0Y2hlciBleHRlbmRzIFJlYWN0V2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBjZWxsIHR5cGUgc3dpdGNoZXIuXG4gICAqL1xuICBjb25zdHJ1Y3Rvcih3aWRnZXQ6IExvZ0NvbnNvbGVQYW5lbCwgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX3RyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1Mb2dDb25zb2xlLXRvb2xiYXJMb2dMZXZlbCcpO1xuICAgIHRoaXMuX2xvZ0NvbnNvbGUgPSB3aWRnZXQ7XG4gICAgaWYgKHdpZGdldC5zb3VyY2UpIHtcbiAgICAgIHRoaXMudXBkYXRlKCk7XG4gICAgfVxuICAgIHdpZGdldC5zb3VyY2VDaGFuZ2VkLmNvbm5lY3QodGhpcy5fdXBkYXRlU291cmNlLCB0aGlzKTtcbiAgfVxuXG4gIHByaXZhdGUgX3VwZGF0ZVNvdXJjZShcbiAgICBzZW5kZXI6IExvZ0NvbnNvbGVQYW5lbCxcbiAgICB7IG9sZFZhbHVlLCBuZXdWYWx1ZSB9OiBJQ2hhbmdlZEFyZ3M8c3RyaW5nIHwgbnVsbD5cbiAgKSB7XG4gICAgLy8gVHJhbnNmZXIgc3RhdGVDaGFuZ2VkIGhhbmRsZXIgdG8gbmV3IHNvdXJjZSBsb2dnZXJcbiAgICBpZiAob2xkVmFsdWUgIT09IG51bGwpIHtcbiAgICAgIGNvbnN0IGxvZ2dlciA9IHNlbmRlci5sb2dnZXJSZWdpc3RyeS5nZXRMb2dnZXIob2xkVmFsdWUpO1xuICAgICAgbG9nZ2VyLnN0YXRlQ2hhbmdlZC5kaXNjb25uZWN0KHRoaXMudXBkYXRlLCB0aGlzKTtcbiAgICB9XG4gICAgaWYgKG5ld1ZhbHVlICE9PSBudWxsKSB7XG4gICAgICBjb25zdCBsb2dnZXIgPSBzZW5kZXIubG9nZ2VyUmVnaXN0cnkuZ2V0TG9nZ2VyKG5ld1ZhbHVlKTtcbiAgICAgIGxvZ2dlci5zdGF0ZUNoYW5nZWQuY29ubmVjdCh0aGlzLnVwZGF0ZSwgdGhpcyk7XG4gICAgfVxuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBjaGFuZ2VgIGV2ZW50cyBmb3IgdGhlIEhUTUxTZWxlY3QgY29tcG9uZW50LlxuICAgKi9cbiAgaGFuZGxlQ2hhbmdlID0gKGV2ZW50OiBSZWFjdC5DaGFuZ2VFdmVudDxIVE1MU2VsZWN0RWxlbWVudD4pOiB2b2lkID0+IHtcbiAgICBpZiAodGhpcy5fbG9nQ29uc29sZS5sb2dnZXIpIHtcbiAgICAgIHRoaXMuX2xvZ0NvbnNvbGUubG9nZ2VyLmxldmVsID0gZXZlbnQudGFyZ2V0LnZhbHVlIGFzIExvZ0xldmVsO1xuICAgIH1cbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9O1xuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGtleWRvd25gIGV2ZW50cyBmb3IgdGhlIEhUTUxTZWxlY3QgY29tcG9uZW50LlxuICAgKi9cbiAgaGFuZGxlS2V5RG93biA9IChldmVudDogUmVhY3QuS2V5Ym9hcmRFdmVudCk6IHZvaWQgPT4ge1xuICAgIGlmIChldmVudC5rZXlDb2RlID09PSAxMykge1xuICAgICAgdGhpcy5fbG9nQ29uc29sZS5hY3RpdmF0ZSgpO1xuICAgIH1cbiAgfTtcblxuICByZW5kZXIoKSB7XG4gICAgY29uc3QgbG9nZ2VyID0gdGhpcy5fbG9nQ29uc29sZS5sb2dnZXI7XG4gICAgcmV0dXJuIChcbiAgICAgIDw+XG4gICAgICAgIDxsYWJlbFxuICAgICAgICAgIGh0bWxGb3I9e3RoaXMuX2lkfVxuICAgICAgICAgIGNsYXNzTmFtZT17XG4gICAgICAgICAgICBsb2dnZXIgPT09IG51bGxcbiAgICAgICAgICAgICAgPyAnanAtTG9nQ29uc29sZS10b29sYmFyTG9nTGV2ZWwtZGlzYWJsZWQnXG4gICAgICAgICAgICAgIDogdW5kZWZpbmVkXG4gICAgICAgICAgfVxuICAgICAgICA+XG4gICAgICAgICAge3RoaXMuX3RyYW5zLl9fKCdMb2cgTGV2ZWw6Jyl9XG4gICAgICAgIDwvbGFiZWw+XG4gICAgICAgIDxIVE1MU2VsZWN0XG4gICAgICAgICAgaWQ9e3RoaXMuX2lkfVxuICAgICAgICAgIGNsYXNzTmFtZT1cImpwLUxvZ0NvbnNvbGUtdG9vbGJhckxvZ0xldmVsRHJvcGRvd25cIlxuICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmhhbmRsZUNoYW5nZX1cbiAgICAgICAgICBvbktleURvd249e3RoaXMuaGFuZGxlS2V5RG93bn1cbiAgICAgICAgICB2YWx1ZT17bG9nZ2VyPy5sZXZlbH1cbiAgICAgICAgICBhcmlhLWxhYmVsPXt0aGlzLl90cmFucy5fXygnTG9nIGxldmVsJyl9XG4gICAgICAgICAgZGlzYWJsZWQ9e2xvZ2dlciA9PT0gbnVsbH1cbiAgICAgICAgICBvcHRpb25zPXtcbiAgICAgICAgICAgIGxvZ2dlciA9PT0gbnVsbFxuICAgICAgICAgICAgICA/IFtdXG4gICAgICAgICAgICAgIDogW1xuICAgICAgICAgICAgICAgICAgW3RoaXMuX3RyYW5zLl9fKCdDcml0aWNhbCcpLCAnQ3JpdGljYWwnXSxcbiAgICAgICAgICAgICAgICAgIFt0aGlzLl90cmFucy5fXygnRXJyb3InKSwgJ0Vycm9yJ10sXG4gICAgICAgICAgICAgICAgICBbdGhpcy5fdHJhbnMuX18oJ1dhcm5pbmcnKSwgJ1dhcm5pbmcnXSxcbiAgICAgICAgICAgICAgICAgIFt0aGlzLl90cmFucy5fXygnSW5mbycpLCAnSW5mbyddLFxuICAgICAgICAgICAgICAgICAgW3RoaXMuX3RyYW5zLl9fKCdEZWJ1ZycpLCAnRGVidWcnXVxuICAgICAgICAgICAgICAgIF0ubWFwKGRhdGEgPT4gKHtcbiAgICAgICAgICAgICAgICAgIGxhYmVsOiBkYXRhWzBdLFxuICAgICAgICAgICAgICAgICAgdmFsdWU6IGRhdGFbMV0udG9Mb3dlckNhc2UoKVxuICAgICAgICAgICAgICAgIH0pKVxuICAgICAgICAgIH1cbiAgICAgICAgLz5cbiAgICAgIDwvPlxuICAgICk7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfbG9nQ29uc29sZTogTG9nQ29uc29sZVBhbmVsO1xuICBwcml2YXRlIF9pZCA9IGBsZXZlbC0ke1VVSUQudXVpZDQoKX1gO1xufVxuXG5leHBvcnQgZGVmYXVsdCBsb2dDb25zb2xlUGx1Z2luO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBWRG9tTW9kZWwsIFZEb21SZW5kZXJlciB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7XG4gIElDb250ZW50Q2hhbmdlLFxuICBJTG9nZ2VyLFxuICBJTG9nZ2VyUmVnaXN0cnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvbG9nY29uc29sZSc7XG5pbXBvcnQgeyBHcm91cEl0ZW0sIGludGVyYWN0aXZlSXRlbSwgVGV4dEl0ZW0gfSBmcm9tICdAanVweXRlcmxhYi9zdGF0dXNiYXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgbGlzdEljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbi8qKlxuICogQSBwdXJlIGZ1bmN0aW9uYWwgY29tcG9uZW50IGZvciBhIExvZyBDb25zb2xlIHN0YXR1cyBpdGVtLlxuICpcbiAqIEBwYXJhbSBwcm9wcyAtIHRoZSBwcm9wcyBmb3IgdGhlIGNvbXBvbmVudC5cbiAqXG4gKiBAcmV0dXJucyBhIHRzeCBjb21wb25lbnQgZm9yIHJlbmRlcmluZyB0aGUgTG9nIENvbnNvbGUgc3RhdHVzLlxuICovXG5mdW5jdGlvbiBMb2dDb25zb2xlU3RhdHVzQ29tcG9uZW50KFxuICBwcm9wczogTG9nQ29uc29sZVN0YXR1c0NvbXBvbmVudC5JUHJvcHNcbik6IFJlYWN0LlJlYWN0RWxlbWVudDxMb2dDb25zb2xlU3RhdHVzQ29tcG9uZW50LklQcm9wcz4ge1xuICBjb25zdCB0cmFuc2xhdG9yID0gcHJvcHMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgbGV0IHRpdGxlID0gJyc7XG4gIGlmIChwcm9wcy5uZXdNZXNzYWdlcyA+IDApIHtcbiAgICB0aXRsZSA9IHRyYW5zLl9fKFxuICAgICAgJyUxIG5ldyBtZXNzYWdlcywgJTIgbG9nIGVudHJpZXMgZm9yICUzJyxcbiAgICAgIHByb3BzLm5ld01lc3NhZ2VzLFxuICAgICAgcHJvcHMubG9nRW50cmllcyxcbiAgICAgIHByb3BzLnNvdXJjZVxuICAgICk7XG4gIH0gZWxzZSB7XG4gICAgdGl0bGUgKz0gdHJhbnMuX18oJyUxIGxvZyBlbnRyaWVzIGZvciAlMicsIHByb3BzLmxvZ0VudHJpZXMsIHByb3BzLnNvdXJjZSk7XG4gIH1cbiAgcmV0dXJuIChcbiAgICA8R3JvdXBJdGVtIHNwYWNpbmc9ezB9IG9uQ2xpY2s9e3Byb3BzLmhhbmRsZUNsaWNrfSB0aXRsZT17dGl0bGV9PlxuICAgICAgPGxpc3RJY29uLnJlYWN0IHRvcD17JzJweCd9IHN0eWxlc2hlZXQ9eydzdGF0dXNCYXInfSAvPlxuICAgICAge3Byb3BzLm5ld01lc3NhZ2VzID4gMCA/IDxUZXh0SXRlbSBzb3VyY2U9e3Byb3BzLm5ld01lc3NhZ2VzfSAvPiA6IDw+PC8+fVxuICAgIDwvR3JvdXBJdGVtPlxuICApO1xufVxuXG4vKlxuICogQSBuYW1lc3BhY2UgZm9yIExvZ0NvbnNvbGVTdGF0dXNDb21wb25lbnQuXG4gKi9cbm5hbWVzcGFjZSBMb2dDb25zb2xlU3RhdHVzQ29tcG9uZW50IHtcbiAgLyoqXG4gICAqIFRoZSBwcm9wcyBmb3IgdGhlIExvZ0NvbnNvbGVTdGF0dXNDb21wb25lbnQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wcyB7XG4gICAgLyoqXG4gICAgICogQSBjbGljayBoYW5kbGVyIGZvciB0aGUgaXRlbS4gQnkgZGVmYXVsdFxuICAgICAqIExvZyBDb25zb2xlIHBhbmVsIGlzIGxhdW5jaGVkLlxuICAgICAqL1xuICAgIGhhbmRsZUNsaWNrOiAoKSA9PiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogTnVtYmVyIG9mIGxvZyBlbnRyaWVzLlxuICAgICAqL1xuICAgIGxvZ0VudHJpZXM6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIE51bWJlciBvZiBuZXcgbG9nIG1lc3NhZ2VzLlxuICAgICAqL1xuICAgIG5ld01lc3NhZ2VzOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBMb2cgc291cmNlIG5hbWVcbiAgICAgKi9cbiAgICBzb3VyY2U6IHN0cmluZyB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvclxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxufVxuXG4vKipcbiAqIEEgVkRvbVJlbmRlcmVyIHdpZGdldCBmb3IgZGlzcGxheWluZyB0aGUgc3RhdHVzIG9mIExvZyBDb25zb2xlIGxvZ3MuXG4gKi9cbmV4cG9ydCBjbGFzcyBMb2dDb25zb2xlU3RhdHVzIGV4dGVuZHMgVkRvbVJlbmRlcmVyPExvZ0NvbnNvbGVTdGF0dXMuTW9kZWw+IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCB0aGUgbG9nIGNvbnNvbGUgc3RhdHVzIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgc3RhdHVzIHdpZGdldCBpbml0aWFsaXphdGlvbiBvcHRpb25zLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogTG9nQ29uc29sZVN0YXR1cy5JT3B0aW9ucykge1xuICAgIHN1cGVyKG5ldyBMb2dDb25zb2xlU3RhdHVzLk1vZGVsKG9wdGlvbnMubG9nZ2VyUmVnaXN0cnkpKTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5faGFuZGxlQ2xpY2sgPSBvcHRpb25zLmhhbmRsZUNsaWNrO1xuICAgIHRoaXMuYWRkQ2xhc3MoaW50ZXJhY3RpdmVJdGVtKTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1Mb2dDb25zb2xlU3RhdHVzSXRlbScpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciB0aGUgbG9nIGNvbnNvbGUgc3RhdHVzIGl0ZW0uXG4gICAqL1xuICByZW5kZXIoKSB7XG4gICAgaWYgKHRoaXMubW9kZWwgPT09IG51bGwgfHwgdGhpcy5tb2RlbC52ZXJzaW9uID09PSAwKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG5cbiAgICBjb25zdCB7XG4gICAgICBmbGFzaEVuYWJsZWQsXG4gICAgICBtZXNzYWdlcyxcbiAgICAgIHNvdXJjZSxcbiAgICAgIHZlcnNpb24sXG4gICAgICB2ZXJzaW9uRGlzcGxheWVkLFxuICAgICAgdmVyc2lvbk5vdGlmaWVkXG4gICAgfSA9IHRoaXMubW9kZWw7XG4gICAgaWYgKHNvdXJjZSAhPT0gbnVsbCAmJiBmbGFzaEVuYWJsZWQgJiYgdmVyc2lvbiA+IHZlcnNpb25Ob3RpZmllZCkge1xuICAgICAgdGhpcy5fZmxhc2hIaWdobGlnaHQoKTtcbiAgICAgIHRoaXMubW9kZWwuc291cmNlTm90aWZpZWQoc291cmNlLCB2ZXJzaW9uKTtcbiAgICB9IGVsc2UgaWYgKHNvdXJjZSAhPT0gbnVsbCAmJiBmbGFzaEVuYWJsZWQgJiYgdmVyc2lvbiA+IHZlcnNpb25EaXNwbGF5ZWQpIHtcbiAgICAgIHRoaXMuX3Nob3dIaWdobGlnaHRlZCgpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9jbGVhckhpZ2hsaWdodCgpO1xuICAgIH1cblxuICAgIHJldHVybiAoXG4gICAgICA8TG9nQ29uc29sZVN0YXR1c0NvbXBvbmVudFxuICAgICAgICBoYW5kbGVDbGljaz17dGhpcy5faGFuZGxlQ2xpY2t9XG4gICAgICAgIGxvZ0VudHJpZXM9e21lc3NhZ2VzfVxuICAgICAgICBuZXdNZXNzYWdlcz17dmVyc2lvbiAtIHZlcnNpb25EaXNwbGF5ZWR9XG4gICAgICAgIHNvdXJjZT17dGhpcy5tb2RlbC5zb3VyY2V9XG4gICAgICAgIHRyYW5zbGF0b3I9e3RoaXMudHJhbnNsYXRvcn1cbiAgICAgIC8+XG4gICAgKTtcbiAgfVxuXG4gIHByaXZhdGUgX2ZsYXNoSGlnaGxpZ2h0KCkge1xuICAgIHRoaXMuX3Nob3dIaWdobGlnaHRlZCgpO1xuXG4gICAgLy8gVG8gbWFrZSBzdXJlIHRoZSBicm93c2VyIHRyaWdnZXJzIHRoZSBhbmltYXRpb24sIHdlIHJlbW92ZSB0aGUgY2xhc3MsXG4gICAgLy8gd2FpdCBmb3IgYW4gYW5pbWF0aW9uIGZyYW1lLCB0aGVuIGFkZCBpdCBiYWNrXG4gICAgdGhpcy5yZW1vdmVDbGFzcygnanAtTG9nQ29uc29sZS1mbGFzaCcpO1xuICAgIHJlcXVlc3RBbmltYXRpb25GcmFtZSgoKSA9PiB7XG4gICAgICB0aGlzLmFkZENsYXNzKCdqcC1Mb2dDb25zb2xlLWZsYXNoJyk7XG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9zaG93SGlnaGxpZ2h0ZWQoKSB7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtbW9kLXNlbGVjdGVkJyk7XG4gIH1cblxuICBwcml2YXRlIF9jbGVhckhpZ2hsaWdodCgpIHtcbiAgICB0aGlzLnJlbW92ZUNsYXNzKCdqcC1Mb2dDb25zb2xlLWZsYXNoJyk7XG4gICAgdGhpcy5yZW1vdmVDbGFzcygnanAtbW9kLXNlbGVjdGVkJyk7XG4gIH1cblxuICByZWFkb25seSB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfaGFuZGxlQ2xpY2s6ICgpID0+IHZvaWQ7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIExvZyBDb25zb2xlIGxvZyBzdGF0dXMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgTG9nQ29uc29sZVN0YXR1cyB7XG4gIC8qKlxuICAgKiBBIFZEb21Nb2RlbCBmb3IgdGhlIExvZ0NvbnNvbGVTdGF0dXMgaXRlbS5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBNb2RlbCBleHRlbmRzIFZEb21Nb2RlbCB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IExvZ0NvbnNvbGVTdGF0dXMgbW9kZWwuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gbG9nZ2VyUmVnaXN0cnkgLSBUaGUgbG9nZ2VyIHJlZ2lzdHJ5IHByb3ZpZGluZyB0aGUgbG9ncy5cbiAgICAgKi9cbiAgICBjb25zdHJ1Y3Rvcihsb2dnZXJSZWdpc3RyeTogSUxvZ2dlclJlZ2lzdHJ5KSB7XG4gICAgICBzdXBlcigpO1xuXG4gICAgICB0aGlzLl9sb2dnZXJSZWdpc3RyeSA9IGxvZ2dlclJlZ2lzdHJ5O1xuICAgICAgdGhpcy5fbG9nZ2VyUmVnaXN0cnkucmVnaXN0cnlDaGFuZ2VkLmNvbm5lY3QoXG4gICAgICAgIHRoaXMuX2hhbmRsZUxvZ1JlZ2lzdHJ5Q2hhbmdlLFxuICAgICAgICB0aGlzXG4gICAgICApO1xuICAgICAgdGhpcy5faGFuZGxlTG9nUmVnaXN0cnlDaGFuZ2UoKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBOdW1iZXIgb2YgbWVzc2FnZXMgY3VycmVudGx5IGluIHRoZSBjdXJyZW50IHNvdXJjZS5cbiAgICAgKi9cbiAgICBnZXQgbWVzc2FnZXMoKTogbnVtYmVyIHtcbiAgICAgIGlmICh0aGlzLl9zb3VyY2UgPT09IG51bGwpIHtcbiAgICAgICAgcmV0dXJuIDA7XG4gICAgICB9XG4gICAgICBjb25zdCBsb2dnZXIgPSB0aGlzLl9sb2dnZXJSZWdpc3RyeS5nZXRMb2dnZXIodGhpcy5fc291cmNlKTtcbiAgICAgIHJldHVybiBsb2dnZXIubGVuZ3RoO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBudW1iZXIgb2YgbWVzc2FnZXMgZXZlciBzdG9yZWQgYnkgdGhlIGN1cnJlbnQgc291cmNlLlxuICAgICAqL1xuICAgIGdldCB2ZXJzaW9uKCk6IG51bWJlciB7XG4gICAgICBpZiAodGhpcy5fc291cmNlID09PSBudWxsKSB7XG4gICAgICAgIHJldHVybiAwO1xuICAgICAgfVxuICAgICAgY29uc3QgbG9nZ2VyID0gdGhpcy5fbG9nZ2VyUmVnaXN0cnkuZ2V0TG9nZ2VyKHRoaXMuX3NvdXJjZSk7XG4gICAgICByZXR1cm4gbG9nZ2VyLnZlcnNpb247XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIG5hbWUgb2YgdGhlIGFjdGl2ZSBsb2cgc291cmNlXG4gICAgICovXG4gICAgZ2V0IHNvdXJjZSgpOiBzdHJpbmcgfCBudWxsIHtcbiAgICAgIHJldHVybiB0aGlzLl9zb3VyY2U7XG4gICAgfVxuXG4gICAgc2V0IHNvdXJjZShuYW1lOiBzdHJpbmcgfCBudWxsKSB7XG4gICAgICBpZiAodGhpcy5fc291cmNlID09PSBuYW1lKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cblxuICAgICAgdGhpcy5fc291cmNlID0gbmFtZTtcblxuICAgICAgLy8gcmVmcmVzaCByZW5kZXJpbmdcbiAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQoKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbGFzdCBzb3VyY2UgdmVyc2lvbiB0aGF0IHdhcyBkaXNwbGF5ZWQuXG4gICAgICovXG4gICAgZ2V0IHZlcnNpb25EaXNwbGF5ZWQoKTogbnVtYmVyIHtcbiAgICAgIGlmICh0aGlzLl9zb3VyY2UgPT09IG51bGwpIHtcbiAgICAgICAgcmV0dXJuIDA7XG4gICAgICB9XG4gICAgICByZXR1cm4gdGhpcy5fc291cmNlVmVyc2lvbi5nZXQodGhpcy5fc291cmNlKT8ubGFzdERpc3BsYXllZCA/PyAwO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBsYXN0IHNvdXJjZSB2ZXJzaW9uIHdlIG5vdGlmaWVkIHRoZSB1c2VyIGFib3V0LlxuICAgICAqL1xuICAgIGdldCB2ZXJzaW9uTm90aWZpZWQoKTogbnVtYmVyIHtcbiAgICAgIGlmICh0aGlzLl9zb3VyY2UgPT09IG51bGwpIHtcbiAgICAgICAgcmV0dXJuIDA7XG4gICAgICB9XG4gICAgICByZXR1cm4gdGhpcy5fc291cmNlVmVyc2lvbi5nZXQodGhpcy5fc291cmNlKT8ubGFzdE5vdGlmaWVkID8/IDA7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogRmxhZyB0byB0b2dnbGUgZmxhc2hpbmcgd2hlbiBuZXcgbG9ncyBhZGRlZC5cbiAgICAgKi9cbiAgICBnZXQgZmxhc2hFbmFibGVkKCk6IGJvb2xlYW4ge1xuICAgICAgcmV0dXJuIHRoaXMuX2ZsYXNoRW5hYmxlZDtcbiAgICB9XG5cbiAgICBzZXQgZmxhc2hFbmFibGVkKGVuYWJsZWQ6IGJvb2xlYW4pIHtcbiAgICAgIGlmICh0aGlzLl9mbGFzaEVuYWJsZWQgPT09IGVuYWJsZWQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuXG4gICAgICB0aGlzLl9mbGFzaEVuYWJsZWQgPSBlbmFibGVkO1xuICAgICAgdGhpcy5mbGFzaEVuYWJsZWRDaGFuZ2VkLmVtaXQoKTtcblxuICAgICAgLy8gcmVmcmVzaCByZW5kZXJpbmdcbiAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQoKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZWNvcmQgdGhlIGxhc3Qgc291cmNlIHZlcnNpb24gZGlzcGxheWVkIHRvIHRoZSB1c2VyLlxuICAgICAqXG4gICAgICogQHBhcmFtIHNvdXJjZSAtIFRoZSBuYW1lIG9mIHRoZSBsb2cgc291cmNlLlxuICAgICAqIEBwYXJhbSB2ZXJzaW9uIC0gVGhlIHZlcnNpb24gb2YgdGhlIGxvZyB0aGF0IHdhcyBkaXNwbGF5ZWQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhpcyB3aWxsIGFsc28gdXBkYXRlIHRoZSBsYXN0IG5vdGlmaWVkIHZlcnNpb24gc28gdGhhdCB0aGUgbGFzdFxuICAgICAqIG5vdGlmaWVkIHZlcnNpb24gaXMgYWx3YXlzIGF0IGxlYXN0IHRoZSBsYXN0IGRpc3BsYXllZCB2ZXJzaW9uLlxuICAgICAqL1xuICAgIHNvdXJjZURpc3BsYXllZChzb3VyY2U6IHN0cmluZyB8IG51bGwsIHZlcnNpb246IG51bWJlciB8IG51bGwpIHtcbiAgICAgIGlmIChzb3VyY2UgPT09IG51bGwgfHwgdmVyc2lvbiA9PT0gbnVsbCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBjb25zdCB2ZXJzaW9ucyA9IHRoaXMuX3NvdXJjZVZlcnNpb24uZ2V0KHNvdXJjZSkhO1xuICAgICAgbGV0IGNoYW5nZSA9IGZhbHNlO1xuICAgICAgaWYgKHZlcnNpb25zLmxhc3REaXNwbGF5ZWQgPCB2ZXJzaW9uKSB7XG4gICAgICAgIHZlcnNpb25zLmxhc3REaXNwbGF5ZWQgPSB2ZXJzaW9uO1xuICAgICAgICBjaGFuZ2UgPSB0cnVlO1xuICAgICAgfVxuICAgICAgaWYgKHZlcnNpb25zLmxhc3ROb3RpZmllZCA8IHZlcnNpb24pIHtcbiAgICAgICAgdmVyc2lvbnMubGFzdE5vdGlmaWVkID0gdmVyc2lvbjtcbiAgICAgICAgY2hhbmdlID0gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIGlmIChjaGFuZ2UgJiYgc291cmNlID09PSB0aGlzLl9zb3VyY2UpIHtcbiAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlY29yZCBhIHNvdXJjZSB2ZXJzaW9uIHdlIG5vdGlmaWVkIHRoZSB1c2VyIGFib3V0LlxuICAgICAqXG4gICAgICogQHBhcmFtIHNvdXJjZSAtIFRoZSBuYW1lIG9mIHRoZSBsb2cgc291cmNlLlxuICAgICAqIEBwYXJhbSB2ZXJzaW9uIC0gVGhlIHZlcnNpb24gb2YgdGhlIGxvZy5cbiAgICAgKi9cbiAgICBzb3VyY2VOb3RpZmllZChzb3VyY2U6IHN0cmluZyB8IG51bGwsIHZlcnNpb246IG51bWJlcikge1xuICAgICAgaWYgKHNvdXJjZSA9PT0gbnVsbCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBjb25zdCB2ZXJzaW9ucyA9IHRoaXMuX3NvdXJjZVZlcnNpb24uZ2V0KHNvdXJjZSk7XG4gICAgICBpZiAodmVyc2lvbnMhLmxhc3ROb3RpZmllZCA8IHZlcnNpb24pIHtcbiAgICAgICAgdmVyc2lvbnMhLmxhc3ROb3RpZmllZCA9IHZlcnNpb247XG4gICAgICAgIGlmIChzb3VyY2UgPT09IHRoaXMuX3NvdXJjZSkge1xuICAgICAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQoKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cblxuICAgIHByaXZhdGUgX2hhbmRsZUxvZ1JlZ2lzdHJ5Q2hhbmdlKCkge1xuICAgICAgY29uc3QgbG9nZ2VycyA9IHRoaXMuX2xvZ2dlclJlZ2lzdHJ5LmdldExvZ2dlcnMoKTtcbiAgICAgIGZvciAoY29uc3QgbG9nZ2VyIG9mIGxvZ2dlcnMpIHtcbiAgICAgICAgaWYgKCF0aGlzLl9zb3VyY2VWZXJzaW9uLmhhcyhsb2dnZXIuc291cmNlKSkge1xuICAgICAgICAgIGxvZ2dlci5jb250ZW50Q2hhbmdlZC5jb25uZWN0KHRoaXMuX2hhbmRsZUxvZ0NvbnRlbnRDaGFuZ2UsIHRoaXMpO1xuICAgICAgICAgIHRoaXMuX3NvdXJjZVZlcnNpb24uc2V0KGxvZ2dlci5zb3VyY2UsIHtcbiAgICAgICAgICAgIGxhc3REaXNwbGF5ZWQ6IDAsXG4gICAgICAgICAgICBsYXN0Tm90aWZpZWQ6IDBcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cblxuICAgIHByaXZhdGUgX2hhbmRsZUxvZ0NvbnRlbnRDaGFuZ2UoXG4gICAgICB7IHNvdXJjZSB9OiBJTG9nZ2VyLFxuICAgICAgY2hhbmdlOiBJQ29udGVudENoYW5nZVxuICAgICkge1xuICAgICAgaWYgKHNvdXJjZSA9PT0gdGhpcy5fc291cmNlKSB7XG4gICAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQoKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGZsYXNoIGVuYWJsZW1lbnQgY2hhbmdlcy5cbiAgICAgKi9cbiAgICBwdWJsaWMgZmxhc2hFbmFibGVkQ2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgdm9pZD4odGhpcyk7XG4gICAgcHJpdmF0ZSBfZmxhc2hFbmFibGVkOiBib29sZWFuID0gdHJ1ZTtcbiAgICBwcml2YXRlIF9sb2dnZXJSZWdpc3RyeTogSUxvZ2dlclJlZ2lzdHJ5O1xuICAgIHByaXZhdGUgX3NvdXJjZTogc3RyaW5nIHwgbnVsbCA9IG51bGw7XG4gICAgLyoqXG4gICAgICogVGhlIHZpZXcgc3RhdHVzIG9mIGVhY2ggc291cmNlLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIEtleXMgYXJlIHNvdXJjZSBuYW1lcywgdmFsdWUgaXMgYSBsaXN0IG9mIHR3byBudW1iZXJzLiBUaGUgZmlyc3RcbiAgICAgKiByZXByZXNlbnRzIHRoZSB2ZXJzaW9uIG9mIHRoZSBtZXNzYWdlcyB0aGF0IHdhcyBsYXN0IGRpc3BsYXllZCB0byB0aGVcbiAgICAgKiB1c2VyLCB0aGUgc2Vjb25kIHJlcHJlc2VudHMgdGhlIHZlcnNpb24gdGhhdCB3ZSBsYXN0IG5vdGlmaWVkIHRoZSB1c2VyXG4gICAgICogYWJvdXQuXG4gICAgICovXG4gICAgcHJpdmF0ZSBfc291cmNlVmVyc2lvbjogTWFwPHN0cmluZywgSVZlcnNpb25JbmZvPiA9IG5ldyBNYXAoKTtcbiAgfVxuXG4gIGludGVyZmFjZSBJVmVyc2lvbkluZm8ge1xuICAgIGxhc3REaXNwbGF5ZWQ6IG51bWJlcjtcbiAgICBsYXN0Tm90aWZpZWQ6IG51bWJlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBjcmVhdGluZyBhIG5ldyBMb2dDb25zb2xlU3RhdHVzIGl0ZW1cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBsb2dnZXIgcmVnaXN0cnkgcHJvdmlkaW5nIHRoZSBsb2dzLlxuICAgICAqL1xuICAgIGxvZ2dlclJlZ2lzdHJ5OiBJTG9nZ2VyUmVnaXN0cnk7XG5cbiAgICAvKipcbiAgICAgKiBBIGNsaWNrIGhhbmRsZXIgZm9yIHRoZSBpdGVtLiBCeSBkZWZhdWx0XG4gICAgICogTG9nIENvbnNvbGUgcGFuZWwgaXMgbGF1bmNoZWQuXG4gICAgICovXG4gICAgaGFuZGxlQ2xpY2s6ICgpID0+IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBMYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==