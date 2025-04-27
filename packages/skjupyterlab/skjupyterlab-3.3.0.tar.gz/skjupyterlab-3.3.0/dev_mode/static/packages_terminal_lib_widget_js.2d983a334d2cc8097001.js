(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_terminal_lib_widget_js"],{

/***/ "../packages/terminal/lib/tokens.js":
/*!******************************************!*\
  !*** ../packages/terminal/lib/tokens.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITerminalTracker": () => (/* binding */ ITerminalTracker),
/* harmony export */   "ITerminal": () => (/* binding */ ITerminal)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The editor tracker token.
 */
const ITerminalTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/terminal:ITerminalTracker');
/* tslint:enable */
/**
 * The namespace for terminals. Separated from the widget so it can be lazy
 * loaded.
 */
var ITerminal;
(function (ITerminal) {
    /**
     * The default options used for creating terminals.
     */
    ITerminal.defaultOptions = {
        theme: 'inherit',
        fontFamily: 'Menlo, Consolas, "DejaVu Sans Mono", monospace',
        fontSize: 13,
        lineHeight: 1.0,
        scrollback: 1000,
        shutdownOnClose: false,
        cursorBlink: true,
        initialCommand: '',
        screenReaderMode: false,
        pasteWithCtrlV: true,
        autoFit: true,
        macOptionIsMeta: false
    };
})(ITerminal || (ITerminal = {}));


/***/ }),

/***/ "../packages/terminal/lib/widget.js":
/*!******************************************!*\
  !*** ../packages/terminal/lib/widget.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Terminal": () => (/* binding */ Terminal)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/domutils */ "webpack/sharing/consume/default/@lumino/domutils/@lumino/domutils");
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_domutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging/@lumino/messaging");
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_messaging__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var xterm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! xterm */ "../node_modules/xterm/lib/xterm.js");
/* harmony import */ var xterm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(xterm__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var xterm_addon_fit__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! xterm-addon-fit */ "../node_modules/xterm-addon-fit/lib/xterm-addon-fit.js");
/* harmony import */ var xterm_addon_fit__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(xterm_addon_fit__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var ___WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! . */ "../packages/terminal/lib/tokens.js");
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
 * The class name added to a terminal widget.
 */
const TERMINAL_CLASS = 'jp-Terminal';
/**
 * The class name added to a terminal body.
 */
const TERMINAL_BODY_CLASS = 'jp-Terminal-body';
/**
 * A widget which manages a terminal session.
 */
class Terminal extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    /**
     * Construct a new terminal widget.
     *
     * @param session - The terminal session object.
     *
     * @param options - The terminal configuration options.
     *
     * @param translator - The language translator.
     */
    constructor(session, options = {}, translator) {
        super();
        this._needsResize = true;
        this._termOpened = false;
        this._offsetWidth = -1;
        this._offsetHeight = -1;
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        this._trans = translator.load('jupyterlab');
        this.session = session;
        // Initialize settings.
        this._options = Object.assign(Object.assign({}, ___WEBPACK_IMPORTED_MODULE_6__.ITerminal.defaultOptions), options);
        const _a = this._options, { theme } = _a, other = __rest(_a, ["theme"]);
        const xtermOptions = Object.assign({ theme: Private.getXTermTheme(theme) }, other);
        this.addClass(TERMINAL_CLASS);
        this._setThemeAttribute(theme);
        // Create the xterm.
        this._term = new xterm__WEBPACK_IMPORTED_MODULE_4__.Terminal(xtermOptions);
        this._fitAddon = new xterm_addon_fit__WEBPACK_IMPORTED_MODULE_5__.FitAddon();
        this._term.loadAddon(this._fitAddon);
        this._initializeTerm();
        this.id = `jp-Terminal-${Private.id++}`;
        this.title.label = this._trans.__('Terminal');
        session.messageReceived.connect(this._onMessage, this);
        session.disposed.connect(this.dispose, this);
        if (session.connectionStatus === 'connected') {
            this._initialConnection();
        }
        else {
            session.connectionStatusChanged.connect(this._initialConnection, this);
        }
    }
    _setThemeAttribute(theme) {
        if (this.isDisposed) {
            return;
        }
        this.node.setAttribute('data-term-theme', theme ? theme.toLowerCase() : 'inherit');
    }
    _initialConnection() {
        if (this.isDisposed) {
            return;
        }
        if (this.session.connectionStatus !== 'connected') {
            return;
        }
        this.title.label = this._trans.__('Terminal %1', this.session.name);
        this._setSessionSize();
        if (this._options.initialCommand) {
            this.session.send({
                type: 'stdin',
                content: [this._options.initialCommand + '\r']
            });
        }
        // Only run this initial connection logic once.
        this.session.connectionStatusChanged.disconnect(this._initialConnection, this);
    }
    /**
     * Get a config option for the terminal.
     */
    getOption(option) {
        return this._options[option];
    }
    /**
     * Set a config option for the terminal.
     */
    setOption(option, value) {
        if (option !== 'theme' &&
            (this._options[option] === value || option === 'initialCommand')) {
            return;
        }
        this._options[option] = value;
        switch (option) {
            case 'shutdownOnClose': // Do not transmit to XTerm
                break;
            case 'theme':
                this._term.setOption('theme', Private.getXTermTheme(value));
                this._setThemeAttribute(value);
                break;
            default:
                this._term.setOption(option, value);
                break;
        }
        this._needsResize = true;
        this.update();
    }
    /**
     * Dispose of the resources held by the terminal widget.
     */
    dispose() {
        if (!this.session.isDisposed) {
            if (this.getOption('shutdownOnClose')) {
                this.session.shutdown().catch(reason => {
                    console.error(`Terminal not shut down: ${reason}`);
                });
            }
        }
        this._term.dispose();
        super.dispose();
    }
    /**
     * Refresh the terminal session.
     *
     * #### Notes
     * Failure to reconnect to the session should be caught appropriately
     */
    async refresh() {
        if (!this.isDisposed) {
            await this.session.reconnect();
            this._term.clear();
        }
    }
    /**
     * Process a message sent to the widget.
     *
     * @param msg - The message sent to the widget.
     *
     * #### Notes
     * Subclasses may reimplement this method as needed.
     */
    processMessage(msg) {
        super.processMessage(msg);
        switch (msg.type) {
            case 'fit-request':
                this.onFitRequest(msg);
                break;
            default:
                break;
        }
    }
    /**
     * Set the size of the terminal when attached if dirty.
     */
    onAfterAttach(msg) {
        this.update();
    }
    /**
     * Set the size of the terminal when shown if dirty.
     */
    onAfterShow(msg) {
        this.update();
    }
    /**
     * On resize, use the computed row and column sizes to resize the terminal.
     */
    onResize(msg) {
        this._offsetWidth = msg.width;
        this._offsetHeight = msg.height;
        this._needsResize = true;
        this.update();
    }
    /**
     * A message handler invoked on an `'update-request'` message.
     */
    onUpdateRequest(msg) {
        var _a;
        if (!this.isVisible || !this.isAttached) {
            return;
        }
        // Open the terminal if necessary.
        if (!this._termOpened) {
            this._term.open(this.node);
            (_a = this._term.element) === null || _a === void 0 ? void 0 : _a.classList.add(TERMINAL_BODY_CLASS);
            this._termOpened = true;
        }
        if (this._needsResize) {
            this._resizeTerminal();
        }
    }
    /**
     * A message handler invoked on an `'fit-request'` message.
     */
    onFitRequest(msg) {
        const resize = _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget.ResizeMessage.UnknownSize;
        _lumino_messaging__WEBPACK_IMPORTED_MODULE_2__.MessageLoop.sendMessage(this, resize);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this._term.focus();
    }
    /**
     * Initialize the terminal object.
     */
    _initializeTerm() {
        const term = this._term;
        term.onData((data) => {
            if (this.isDisposed) {
                return;
            }
            this.session.send({
                type: 'stdin',
                content: [data]
            });
        });
        term.onTitleChange((title) => {
            this.title.label = title;
        });
        // Do not add any Ctrl+C/Ctrl+V handling on macOS,
        // where Cmd+C/Cmd+V works as intended.
        if (_lumino_domutils__WEBPACK_IMPORTED_MODULE_1__.Platform.IS_MAC) {
            return;
        }
        term.attachCustomKeyEventHandler(event => {
            if (event.ctrlKey && event.key === 'c' && term.hasSelection()) {
                // Return so that the usual OS copy happens
                // instead of interrupt signal.
                return false;
            }
            if (event.ctrlKey && event.key === 'v' && this._options.pasteWithCtrlV) {
                // Return so that the usual paste happens.
                return false;
            }
            return true;
        });
    }
    /**
     * Handle a message from the terminal session.
     */
    _onMessage(sender, msg) {
        switch (msg.type) {
            case 'stdout':
                if (msg.content) {
                    this._term.write(msg.content[0]);
                }
                break;
            case 'disconnect':
                this._term.write('\r\n\r\n[Finished… Term Session]\r\n');
                break;
            default:
                break;
        }
    }
    /**
     * Resize the terminal based on computed geometry.
     */
    _resizeTerminal() {
        if (this._options.autoFit) {
            this._fitAddon.fit();
        }
        if (this._offsetWidth === -1) {
            this._offsetWidth = this.node.offsetWidth;
        }
        if (this._offsetHeight === -1) {
            this._offsetHeight = this.node.offsetHeight;
        }
        this._setSessionSize();
        this._needsResize = false;
    }
    /**
     * Set the size of the terminal in the session.
     */
    _setSessionSize() {
        const content = [
            this._term.rows,
            this._term.cols,
            this._offsetHeight,
            this._offsetWidth
        ];
        if (!this.isDisposed) {
            this.session.send({ type: 'set_size', content });
        }
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An incrementing counter for ids.
     */
    Private.id = 0;
    /**
     * The light terminal theme.
     */
    Private.lightTheme = {
        foreground: '#000',
        background: '#fff',
        cursor: '#616161',
        cursorAccent: '#F5F5F5',
        selection: 'rgba(97, 97, 97, 0.3)' // md-grey-700
    };
    /**
     * The dark terminal theme.
     */
    Private.darkTheme = {
        foreground: '#fff',
        background: '#000',
        cursor: '#fff',
        cursorAccent: '#000',
        selection: 'rgba(255, 255, 255, 0.3)'
    };
    /**
     * The current theme.
     */
    Private.inheritTheme = () => ({
        foreground: getComputedStyle(document.body)
            .getPropertyValue('--jp-ui-font-color0')
            .trim(),
        background: getComputedStyle(document.body)
            .getPropertyValue('--jp-layout-color0')
            .trim(),
        cursor: getComputedStyle(document.body)
            .getPropertyValue('--jp-ui-font-color1')
            .trim(),
        cursorAccent: getComputedStyle(document.body)
            .getPropertyValue('--jp-ui-inverse-font-color0')
            .trim(),
        selection: getComputedStyle(document.body)
            .getPropertyValue('--jp-ui-font-color3')
            .trim()
    });
    function getXTermTheme(theme) {
        switch (theme) {
            case 'light':
                return Private.lightTheme;
            case 'dark':
                return Private.darkTheme;
            case 'inherit':
            default:
                return Private.inheritTheme();
        }
    }
    Private.getXTermTheme = getXTermTheme;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdGVybWluYWwvc3JjL3Rva2Vucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdGVybWluYWwvc3JjL3dpZGdldC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUlqQjtBQVMxQyxvQkFBb0I7QUFDcEI7O0dBRUc7QUFDSSxNQUFNLGdCQUFnQixHQUFHLElBQUksb0RBQUssQ0FDdkMsdUNBQXVDLENBQ3hDLENBQUM7QUFDRixtQkFBbUI7QUFFbkI7OztHQUdHO0FBQ0ksSUFBVSxTQUFTLENBMkh6QjtBQTNIRCxXQUFpQixTQUFTO0lBMEZ4Qjs7T0FFRztJQUNVLHdCQUFjLEdBQWE7UUFDdEMsS0FBSyxFQUFFLFNBQVM7UUFDaEIsVUFBVSxFQUFFLGdEQUFnRDtRQUM1RCxRQUFRLEVBQUUsRUFBRTtRQUNaLFVBQVUsRUFBRSxHQUFHO1FBQ2YsVUFBVSxFQUFFLElBQUk7UUFDaEIsZUFBZSxFQUFFLEtBQUs7UUFDdEIsV0FBVyxFQUFFLElBQUk7UUFDakIsY0FBYyxFQUFFLEVBQUU7UUFDbEIsZ0JBQWdCLEVBQUUsS0FBSztRQUN2QixjQUFjLEVBQUUsSUFBSTtRQUNwQixPQUFPLEVBQUUsSUFBSTtRQUNiLGVBQWUsRUFBRSxLQUFLO0tBQ3ZCLENBQUM7QUFpQkosQ0FBQyxFQTNIZ0IsU0FBUyxLQUFULFNBQVMsUUEySHpCOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ3RKRCwwQ0FBMEM7QUFDMUMsMkRBQTJEOzs7Ozs7Ozs7Ozs7QUFPMUI7QUFDVztBQUNhO0FBQ2hCO0FBQ0M7QUFDQztBQUNiO0FBRTlCOztHQUVHO0FBQ0gsTUFBTSxjQUFjLEdBQUcsYUFBYSxDQUFDO0FBRXJDOztHQUVHO0FBQ0gsTUFBTSxtQkFBbUIsR0FB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Q0FBQzthQUN2QyxnQkFBZ0IsQ0FBQyxxQkFBcUIsQ0FBQzthQUN2QyxJQUFJLEVBQUU7S0FDVixDQUFDLENBQUM7SUFFSCxTQUFnQixhQUFhLENBQzNCLEtBQXNCO1FBRXRCLFFBQVEsS0FBSyxFQUFFO1lBQ2IsS0FBSyxPQUFPO2dCQUNWLE9BQU8sa0JBQVUsQ0FBQztZQUNwQixLQUFLLE1BQU07Z0JBQ1QsT0FBTyxpQkFBUyxDQUFDO1lBQ25CLEtBQUssU0FBUyxDQUFDO1lBQ2Y7Z0JBQ0UsT0FBTyxvQkFBWSxFQUFFLENBQUM7U0FDekI7SUFDSCxDQUFDO0lBWmUscUJBQWEsZ0JBWTVCO0FBQ0gsQ0FBQyxFQTlEUyxPQUFPLEtBQVAsT0FBTyxRQThEaEIiLCJmaWxlIjoicGFja2FnZXNfdGVybWluYWxfbGliX3dpZGdldF9qcy4yZDk4M2EzMzRkMmNjODA5NzAwMS5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVdpZGdldFRyYWNrZXIsIE1haW5BcmVhV2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgVGVybWluYWwgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogQSBjbGFzcyB0aGF0IHRyYWNrcyBlZGl0b3Igd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJVGVybWluYWxUcmFja2VyXG4gIGV4dGVuZHMgSVdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8SVRlcm1pbmFsLklUZXJtaW5hbD4+IHt9XG5cbi8qIHRzbGludDpkaXNhYmxlICovXG4vKipcbiAqIFRoZSBlZGl0b3IgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElUZXJtaW5hbFRyYWNrZXIgPSBuZXcgVG9rZW48SVRlcm1pbmFsVHJhY2tlcj4oXG4gICdAanVweXRlcmxhYi90ZXJtaW5hbDpJVGVybWluYWxUcmFja2VyJ1xuKTtcbi8qIHRzbGludDplbmFibGUgKi9cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciB0ZXJtaW5hbHMuIFNlcGFyYXRlZCBmcm9tIHRoZSB3aWRnZXQgc28gaXQgY2FuIGJlIGxhenlcbiAqIGxvYWRlZC5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJVGVybWluYWwge1xuICBleHBvcnQgaW50ZXJmYWNlIElUZXJtaW5hbCBleHRlbmRzIFdpZGdldCB7XG4gICAgLyoqXG4gICAgICogVGhlIHRlcm1pbmFsIHNlc3Npb24gYXNzb2NpYXRlZCB3aXRoIHRoZSB3aWRnZXQuXG4gICAgICovXG4gICAgc2Vzc2lvbjogVGVybWluYWwuSVRlcm1pbmFsQ29ubmVjdGlvbjtcblxuICAgIC8qKlxuICAgICAqIEdldCBhIGNvbmZpZyBvcHRpb24gZm9yIHRoZSB0ZXJtaW5hbC5cbiAgICAgKi9cbiAgICBnZXRPcHRpb248SyBleHRlbmRzIGtleW9mIElPcHRpb25zPihvcHRpb246IEspOiBJT3B0aW9uc1tLXTtcblxuICAgIC8qKlxuICAgICAqIFNldCBhIGNvbmZpZyBvcHRpb24gZm9yIHRoZSB0ZXJtaW5hbC5cbiAgICAgKi9cbiAgICBzZXRPcHRpb248SyBleHRlbmRzIGtleW9mIElPcHRpb25zPihvcHRpb246IEssIHZhbHVlOiBJT3B0aW9uc1tLXSk6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBSZWZyZXNoIHRoZSB0ZXJtaW5hbCBzZXNzaW9uLlxuICAgICAqL1xuICAgIHJlZnJlc2goKTogUHJvbWlzZTx2b2lkPjtcbiAgfVxuICAvKipcbiAgICogT3B0aW9ucyBmb3IgdGhlIHRlcm1pbmFsIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBmb250IGZhbWlseSB1c2VkIHRvIHJlbmRlciB0ZXh0LlxuICAgICAqL1xuICAgIGZvbnRGYW1pbHk/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZm9udCBzaXplIG9mIHRoZSB0ZXJtaW5hbCBpbiBwaXhlbHMuXG4gICAgICovXG4gICAgZm9udFNpemU6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBsaW5lIGhlaWdodCB1c2VkIHRvIHJlbmRlciB0ZXh0LlxuICAgICAqL1xuICAgIGxpbmVIZWlnaHQ/OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdGhlbWUgb2YgdGhlIHRlcm1pbmFsLlxuICAgICAqL1xuICAgIHRoZW1lOiBUaGVtZTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBhbW91bnQgb2YgYnVmZmVyIHNjcm9sbGJhY2sgdG8gYmUgdXNlZFxuICAgICAqIHdpdGggdGhlIHRlcm1pbmFsXG4gICAgICovXG4gICAgc2Nyb2xsYmFjaz86IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gc2h1dCBkb3duIHRoZSBzZXNzaW9uIHdoZW4gY2xvc2luZyBhIHRlcm1pbmFsIG9yIG5vdC5cbiAgICAgKi9cbiAgICBzaHV0ZG93bk9uQ2xvc2U6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGJsaW5rIHRoZSBjdXJzb3IuICBDYW4gb25seSBiZSBzZXQgYXQgc3RhcnR1cC5cbiAgICAgKi9cbiAgICBjdXJzb3JCbGluazogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIEFuIG9wdGlvbmFsIGNvbW1hbmQgdG8gcnVuIHdoZW4gdGhlIHNlc3Npb24gc3RhcnRzLlxuICAgICAqL1xuICAgIGluaXRpYWxDb21tYW5kOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGVuYWJsZSBzY3JlZW4gcmVhZGVyIHN1cHBvcnQuXG4gICAgICovXG4gICAgc2NyZWVuUmVhZGVyTW9kZTogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gZW5hYmxlIHVzaW5nIEN0cmwrViB0byBwYXN0ZS5cbiAgICAgKlxuICAgICAqIFRoaXMgc2V0dGluZyBoYXMgbm8gZWZmZWN0IG9uIG1hY09TLCB3aGVyZSBDbWQrViBpcyBhdmFpbGFibGUuXG4gICAgICovXG4gICAgcGFzdGVXaXRoQ3RybFY6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGF1dG8tZml0IHRoZSB0ZXJtaW5hbCB0byBpdHMgaG9zdCBlbGVtZW50IHNpemUuXG4gICAgICovXG4gICAgYXV0b0ZpdD86IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBUcmVhdCBvcHRpb24gYXMgbWV0YSBrZXkgb24gbWFjT1MuXG4gICAgICovXG4gICAgbWFjT3B0aW9uSXNNZXRhPzogYm9vbGVhbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBvcHRpb25zIHVzZWQgZm9yIGNyZWF0aW5nIHRlcm1pbmFscy5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBkZWZhdWx0T3B0aW9uczogSU9wdGlvbnMgPSB7XG4gICAgdGhlbWU6ICdpbmhlcml0JyxcbiAgICBmb250RmFtaWx5OiAnTWVubG8sIENvbnNvbGFzLCBcIkRlamFWdSBTYW5zIE1vbm9cIiwgbW9ub3NwYWNlJyxcbiAgICBmb250U2l6ZTogMTMsXG4gICAgbGluZUhlaWdodDogMS4wLFxuICAgIHNjcm9sbGJhY2s6IDEwMDAsXG4gICAgc2h1dGRvd25PbkNsb3NlOiBmYWxzZSxcbiAgICBjdXJzb3JCbGluazogdHJ1ZSxcbiAgICBpbml0aWFsQ29tbWFuZDogJycsXG4gICAgc2NyZWVuUmVhZGVyTW9kZTogZmFsc2UsIC8vIEZhbHNlIGJ5IGRlZmF1bHQsIGNhbiBjYXVzZSBzY3JvbGxiYXIgbW91c2UgaW50ZXJhY3Rpb24gaXNzdWVzLlxuICAgIHBhc3RlV2l0aEN0cmxWOiB0cnVlLFxuICAgIGF1dG9GaXQ6IHRydWUsXG4gICAgbWFjT3B0aW9uSXNNZXRhOiBmYWxzZVxuICB9O1xuXG4gIC8qKlxuICAgKiBBIHR5cGUgZm9yIHRoZSB0ZXJtaW5hbCB0aGVtZS5cbiAgICovXG4gIGV4cG9ydCB0eXBlIFRoZW1lID0gJ2xpZ2h0JyB8ICdkYXJrJyB8ICdpbmhlcml0JztcblxuICAvKipcbiAgICogQSB0eXBlIGZvciB0aGUgdGVybWluYWwgdGhlbWUuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElUaGVtZU9iamVjdCB7XG4gICAgZm9yZWdyb3VuZDogc3RyaW5nO1xuICAgIGJhY2tncm91bmQ6IHN0cmluZztcbiAgICBjdXJzb3I6IHN0cmluZztcbiAgICBjdXJzb3JBY2NlbnQ6IHN0cmluZztcbiAgICBzZWxlY3Rpb246IHN0cmluZztcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUZXJtaW5hbCBhcyBUZXJtaW5hbE5TIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIG51bGxUcmFuc2xhdG9yLFxuICBUcmFuc2xhdGlvbkJ1bmRsZVxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBQbGF0Zm9ybSB9IGZyb20gJ0BsdW1pbm8vZG9tdXRpbHMnO1xuaW1wb3J0IHsgTWVzc2FnZSwgTWVzc2FnZUxvb3AgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgVGVybWluYWwgYXMgWHRlcm0gfSBmcm9tICd4dGVybSc7XG5pbXBvcnQgeyBGaXRBZGRvbiB9IGZyb20gJ3h0ZXJtLWFkZG9uLWZpdCc7XG5pbXBvcnQgeyBJVGVybWluYWwgfSBmcm9tICcuJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhIHRlcm1pbmFsIHdpZGdldC5cbiAqL1xuY29uc3QgVEVSTUlOQUxfQ0xBU1MgPSAnanAtVGVybWluYWwnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgdGVybWluYWwgYm9keS5cbiAqL1xuY29uc3QgVEVSTUlOQUxfQk9EWV9DTEFTUyA9ICdqcC1UZXJtaW5hbC1ib2R5JztcblxuLyoqXG4gKiBBIHdpZGdldCB3aGljaCBtYW5hZ2VzIGEgdGVybWluYWwgc2Vzc2lvbi5cbiAqL1xuZXhwb3J0IGNsYXNzIFRlcm1pbmFsIGV4dGVuZHMgV2lkZ2V0IGltcGxlbWVudHMgSVRlcm1pbmFsLklUZXJtaW5hbCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgdGVybWluYWwgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gc2Vzc2lvbiAtIFRoZSB0ZXJtaW5hbCBzZXNzaW9uIG9iamVjdC5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgdGVybWluYWwgY29uZmlndXJhdGlvbiBvcHRpb25zLlxuICAgKlxuICAgKiBAcGFyYW0gdHJhbnNsYXRvciAtIFRoZSBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgKi9cbiAgY29uc3RydWN0b3IoXG4gICAgc2Vzc2lvbjogVGVybWluYWxOUy5JVGVybWluYWxDb25uZWN0aW9uLFxuICAgIG9wdGlvbnM6IFBhcnRpYWw8SVRlcm1pbmFsLklPcHRpb25zPiA9IHt9LFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApIHtcbiAgICBzdXBlcigpO1xuICAgIHRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX3RyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgdGhpcy5zZXNzaW9uID0gc2Vzc2lvbjtcblxuICAgIC8vIEluaXRpYWxpemUgc2V0dGluZ3MuXG4gICAgdGhpcy5fb3B0aW9ucyA9IHsgLi4uSVRlcm1pbmFsLmRlZmF1bHRPcHRpb25zLCAuLi5vcHRpb25zIH07XG5cbiAgICBjb25zdCB7IHRoZW1lLCAuLi5vdGhlciB9ID0gdGhpcy5fb3B0aW9ucztcbiAgICBjb25zdCB4dGVybU9wdGlvbnMgPSB7XG4gICAgICB0aGVtZTogUHJpdmF0ZS5nZXRYVGVybVRoZW1lKHRoZW1lKSxcbiAgICAgIC4uLm90aGVyXG4gICAgfTtcblxuICAgIHRoaXMuYWRkQ2xhc3MoVEVSTUlOQUxfQ0xBU1MpO1xuXG4gICAgdGhpcy5fc2V0VGhlbWVBdHRyaWJ1dGUodGhlbWUpO1xuXG4gICAgLy8gQ3JlYXRlIHRoZSB4dGVybS5cbiAgICB0aGlzLl90ZXJtID0gbmV3IFh0ZXJtKHh0ZXJtT3B0aW9ucyk7XG4gICAgdGhpcy5fZml0QWRkb24gPSBuZXcgRml0QWRkb24oKTtcbiAgICB0aGlzLl90ZXJtLmxvYWRBZGRvbih0aGlzLl9maXRBZGRvbik7XG5cbiAgICB0aGlzLl9pbml0aWFsaXplVGVybSgpO1xuXG4gICAgdGhpcy5pZCA9IGBqcC1UZXJtaW5hbC0ke1ByaXZhdGUuaWQrK31gO1xuICAgIHRoaXMudGl0bGUubGFiZWwgPSB0aGlzLl90cmFucy5fXygnVGVybWluYWwnKTtcblxuICAgIHNlc3Npb24ubWVzc2FnZVJlY2VpdmVkLmNvbm5lY3QodGhpcy5fb25NZXNzYWdlLCB0aGlzKTtcbiAgICBzZXNzaW9uLmRpc3Bvc2VkLmNvbm5lY3QodGhpcy5kaXNwb3NlLCB0aGlzKTtcblxuICAgIGlmIChzZXNzaW9uLmNvbm5lY3Rpb25TdGF0dXMgPT09ICdjb25uZWN0ZWQnKSB7XG4gICAgICB0aGlzLl9pbml0aWFsQ29ubmVjdGlvbigpO1xuICAgIH0gZWxzZSB7XG4gICAgICBzZXNzaW9uLmNvbm5lY3Rpb25TdGF0dXNDaGFuZ2VkLmNvbm5lY3QodGhpcy5faW5pdGlhbENvbm5lY3Rpb24sIHRoaXMpO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX3NldFRoZW1lQXR0cmlidXRlKHRoZW1lOiBzdHJpbmcgfCBudWxsIHwgdW5kZWZpbmVkKSB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRoaXMubm9kZS5zZXRBdHRyaWJ1dGUoXG4gICAgICAnZGF0YS10ZXJtLXRoZW1lJyxcbiAgICAgIHRoZW1lID8gdGhlbWUudG9Mb3dlckNhc2UoKSA6ICdpbmhlcml0J1xuICAgICk7XG4gIH1cblxuICBwcml2YXRlIF9pbml0aWFsQ29ubmVjdGlvbigpIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgaWYgKHRoaXMuc2Vzc2lvbi5jb25uZWN0aW9uU3RhdHVzICE9PSAnY29ubmVjdGVkJykge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRoaXMudGl0bGUubGFiZWwgPSB0aGlzLl90cmFucy5fXygnVGVybWluYWwgJTEnLCB0aGlzLnNlc3Npb24ubmFtZSk7XG4gICAgdGhpcy5fc2V0U2Vzc2lvblNpemUoKTtcbiAgICBpZiAodGhpcy5fb3B0aW9ucy5pbml0aWFsQ29tbWFuZCkge1xuICAgICAgdGhpcy5zZXNzaW9uLnNlbmQoe1xuICAgICAgICB0eXBlOiAnc3RkaW4nLFxuICAgICAgICBjb250ZW50OiBbdGhpcy5fb3B0aW9ucy5pbml0aWFsQ29tbWFuZCArICdcXHInXVxuICAgICAgfSk7XG4gICAgfVxuXG4gICAgLy8gT25seSBydW4gdGhpcyBpbml0aWFsIGNvbm5lY3Rpb24gbG9naWMgb25jZS5cbiAgICB0aGlzLnNlc3Npb24uY29ubmVjdGlvblN0YXR1c0NoYW5nZWQuZGlzY29ubmVjdChcbiAgICAgIHRoaXMuX2luaXRpYWxDb25uZWN0aW9uLFxuICAgICAgdGhpc1xuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHRlcm1pbmFsIHNlc3Npb24gYXNzb2NpYXRlZCB3aXRoIHRoZSB3aWRnZXQuXG4gICAqL1xuICByZWFkb25seSBzZXNzaW9uOiBUZXJtaW5hbE5TLklUZXJtaW5hbENvbm5lY3Rpb247XG5cbiAgLyoqXG4gICAqIEdldCBhIGNvbmZpZyBvcHRpb24gZm9yIHRoZSB0ZXJtaW5hbC5cbiAgICovXG4gIGdldE9wdGlvbjxLIGV4dGVuZHMga2V5b2YgSVRlcm1pbmFsLklPcHRpb25zPihcbiAgICBvcHRpb246IEtcbiAgKTogSVRlcm1pbmFsLklPcHRpb25zW0tdIHtcbiAgICByZXR1cm4gdGhpcy5fb3B0aW9uc1tvcHRpb25dO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCBhIGNvbmZpZyBvcHRpb24gZm9yIHRoZSB0ZXJtaW5hbC5cbiAgICovXG4gIHNldE9wdGlvbjxLIGV4dGVuZHMga2V5b2YgSVRlcm1pbmFsLklPcHRpb25zPihcbiAgICBvcHRpb246IEssXG4gICAgdmFsdWU6IElUZXJtaW5hbC5JT3B0aW9uc1tLXVxuICApOiB2b2lkIHtcbiAgICBpZiAoXG4gICAgICBvcHRpb24gIT09ICd0aGVtZScgJiZcbiAgICAgICh0aGlzLl9vcHRpb25zW29wdGlvbl0gPT09IHZhbHVlIHx8IG9wdGlvbiA9PT0gJ2luaXRpYWxDb21tYW5kJylcbiAgICApIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLl9vcHRpb25zW29wdGlvbl0gPSB2YWx1ZTtcblxuICAgIHN3aXRjaCAob3B0aW9uKSB7XG4gICAgICBjYXNlICdzaHV0ZG93bk9uQ2xvc2UnOiAvLyBEbyBub3QgdHJhbnNtaXQgdG8gWFRlcm1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICd0aGVtZSc6XG4gICAgICAgIHRoaXMuX3Rlcm0uc2V0T3B0aW9uKFxuICAgICAgICAgICd0aGVtZScsXG4gICAgICAgICAgUHJpdmF0ZS5nZXRYVGVybVRoZW1lKHZhbHVlIGFzIElUZXJtaW5hbC5UaGVtZSlcbiAgICAgICAgKTtcbiAgICAgICAgdGhpcy5fc2V0VGhlbWVBdHRyaWJ1dGUodmFsdWUgYXMgSVRlcm1pbmFsLlRoZW1lKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICB0aGlzLl90ZXJtLnNldE9wdGlvbihvcHRpb24sIHZhbHVlKTtcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuXG4gICAgdGhpcy5fbmVlZHNSZXNpemUgPSB0cnVlO1xuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHRlcm1pbmFsIHdpZGdldC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKCF0aGlzLnNlc3Npb24uaXNEaXNwb3NlZCkge1xuICAgICAgaWYgKHRoaXMuZ2V0T3B0aW9uKCdzaHV0ZG93bk9uQ2xvc2UnKSkge1xuICAgICAgICB0aGlzLnNlc3Npb24uc2h1dGRvd24oKS5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICAgIGNvbnNvbGUuZXJyb3IoYFRlcm1pbmFsIG5vdCBzaHV0IGRvd246ICR7cmVhc29ufWApO1xuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9XG4gICAgdGhpcy5fdGVybS5kaXNwb3NlKCk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlZnJlc2ggdGhlIHRlcm1pbmFsIHNlc3Npb24uXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogRmFpbHVyZSB0byByZWNvbm5lY3QgdG8gdGhlIHNlc3Npb24gc2hvdWxkIGJlIGNhdWdodCBhcHByb3ByaWF0ZWx5XG4gICAqL1xuICBhc3luYyByZWZyZXNoKCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGlmICghdGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICBhd2FpdCB0aGlzLnNlc3Npb24ucmVjb25uZWN0KCk7XG4gICAgICB0aGlzLl90ZXJtLmNsZWFyKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFByb2Nlc3MgYSBtZXNzYWdlIHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIG1zZyAtIFRoZSBtZXNzYWdlIHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBTdWJjbGFzc2VzIG1heSByZWltcGxlbWVudCB0aGlzIG1ldGhvZCBhcyBuZWVkZWQuXG4gICAqL1xuICBwcm9jZXNzTWVzc2FnZShtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBzdXBlci5wcm9jZXNzTWVzc2FnZShtc2cpO1xuICAgIHN3aXRjaCAobXNnLnR5cGUpIHtcbiAgICAgIGNhc2UgJ2ZpdC1yZXF1ZXN0JzpcbiAgICAgICAgdGhpcy5vbkZpdFJlcXVlc3QobXNnKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBzaXplIG9mIHRoZSB0ZXJtaW5hbCB3aGVuIGF0dGFjaGVkIGlmIGRpcnR5LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHNpemUgb2YgdGhlIHRlcm1pbmFsIHdoZW4gc2hvd24gaWYgZGlydHkuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlclNob3cobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBPbiByZXNpemUsIHVzZSB0aGUgY29tcHV0ZWQgcm93IGFuZCBjb2x1bW4gc2l6ZXMgdG8gcmVzaXplIHRoZSB0ZXJtaW5hbC5cbiAgICovXG4gIHByb3RlY3RlZCBvblJlc2l6ZShtc2c6IFdpZGdldC5SZXNpemVNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fb2Zmc2V0V2lkdGggPSBtc2cud2lkdGg7XG4gICAgdGhpcy5fb2Zmc2V0SGVpZ2h0ID0gbXNnLmhlaWdodDtcbiAgICB0aGlzLl9uZWVkc1Jlc2l6ZSA9IHRydWU7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIG1lc3NhZ2UgaGFuZGxlciBpbnZva2VkIG9uIGFuIGAndXBkYXRlLXJlcXVlc3QnYCBtZXNzYWdlLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uVXBkYXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBpZiAoIXRoaXMuaXNWaXNpYmxlIHx8ICF0aGlzLmlzQXR0YWNoZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBPcGVuIHRoZSB0ZXJtaW5hbCBpZiBuZWNlc3NhcnkuXG4gICAgaWYgKCF0aGlzLl90ZXJtT3BlbmVkKSB7XG4gICAgICB0aGlzLl90ZXJtLm9wZW4odGhpcy5ub2RlKTtcbiAgICAgIHRoaXMuX3Rlcm0uZWxlbWVudD8uY2xhc3NMaXN0LmFkZChURVJNSU5BTF9CT0RZX0NMQVNTKTtcbiAgICAgIHRoaXMuX3Rlcm1PcGVuZWQgPSB0cnVlO1xuICAgIH1cblxuICAgIGlmICh0aGlzLl9uZWVkc1Jlc2l6ZSkge1xuICAgICAgdGhpcy5fcmVzaXplVGVybWluYWwoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQSBtZXNzYWdlIGhhbmRsZXIgaW52b2tlZCBvbiBhbiBgJ2ZpdC1yZXF1ZXN0J2AgbWVzc2FnZS5cbiAgICovXG4gIHByb3RlY3RlZCBvbkZpdFJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgY29uc3QgcmVzaXplID0gV2lkZ2V0LlJlc2l6ZU1lc3NhZ2UuVW5rbm93blNpemU7XG4gICAgTWVzc2FnZUxvb3Auc2VuZE1lc3NhZ2UodGhpcywgcmVzaXplKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhY3RpdmF0ZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fdGVybS5mb2N1cygpO1xuICB9XG5cbiAgLyoqXG4gICAqIEluaXRpYWxpemUgdGhlIHRlcm1pbmFsIG9iamVjdC5cbiAgICovXG4gIHByaXZhdGUgX2luaXRpYWxpemVUZXJtKCk6IHZvaWQge1xuICAgIGNvbnN0IHRlcm0gPSB0aGlzLl90ZXJtO1xuICAgIHRlcm0ub25EYXRhKChkYXRhOiBzdHJpbmcpID0+IHtcbiAgICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgdGhpcy5zZXNzaW9uLnNlbmQoe1xuICAgICAgICB0eXBlOiAnc3RkaW4nLFxuICAgICAgICBjb250ZW50OiBbZGF0YV1cbiAgICAgIH0pO1xuICAgIH0pO1xuXG4gICAgdGVybS5vblRpdGxlQ2hhbmdlKCh0aXRsZTogc3RyaW5nKSA9PiB7XG4gICAgICB0aGlzLnRpdGxlLmxhYmVsID0gdGl0bGU7XG4gICAgfSk7XG5cbiAgICAvLyBEbyBub3QgYWRkIGFueSBDdHJsK0MvQ3RybCtWIGhhbmRsaW5nIG9uIG1hY09TLFxuICAgIC8vIHdoZXJlIENtZCtDL0NtZCtWIHdvcmtzIGFzIGludGVuZGVkLlxuICAgIGlmIChQbGF0Zm9ybS5JU19NQUMpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0ZXJtLmF0dGFjaEN1c3RvbUtleUV2ZW50SGFuZGxlcihldmVudCA9PiB7XG4gICAgICBpZiAoZXZlbnQuY3RybEtleSAmJiBldmVudC5rZXkgPT09ICdjJyAmJiB0ZXJtLmhhc1NlbGVjdGlvbigpKSB7XG4gICAgICAgIC8vIFJldHVybiBzbyB0aGF0IHRoZSB1c3VhbCBPUyBjb3B5IGhhcHBlbnNcbiAgICAgICAgLy8gaW5zdGVhZCBvZiBpbnRlcnJ1cHQgc2lnbmFsLlxuICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICB9XG5cbiAgICAgIGlmIChldmVudC5jdHJsS2V5ICYmIGV2ZW50LmtleSA9PT0gJ3YnICYmIHRoaXMuX29wdGlvbnMucGFzdGVXaXRoQ3RybFYpIHtcbiAgICAgICAgLy8gUmV0dXJuIHNvIHRoYXQgdGhlIHVzdWFsIHBhc3RlIGhhcHBlbnMuXG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgbWVzc2FnZSBmcm9tIHRoZSB0ZXJtaW5hbCBzZXNzaW9uLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25NZXNzYWdlKFxuICAgIHNlbmRlcjogVGVybWluYWxOUy5JVGVybWluYWxDb25uZWN0aW9uLFxuICAgIG1zZzogVGVybWluYWxOUy5JTWVzc2FnZVxuICApOiB2b2lkIHtcbiAgICBzd2l0Y2ggKG1zZy50eXBlKSB7XG4gICAgICBjYXNlICdzdGRvdXQnOlxuICAgICAgICBpZiAobXNnLmNvbnRlbnQpIHtcbiAgICAgICAgICB0aGlzLl90ZXJtLndyaXRlKG1zZy5jb250ZW50WzBdIGFzIHN0cmluZyk7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdkaXNjb25uZWN0JzpcbiAgICAgICAgdGhpcy5fdGVybS53cml0ZSgnXFxyXFxuXFxyXFxuW0ZpbmlzaGVk4oCmIFRlcm0gU2Vzc2lvbl1cXHJcXG4nKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogUmVzaXplIHRoZSB0ZXJtaW5hbCBiYXNlZCBvbiBjb21wdXRlZCBnZW9tZXRyeS5cbiAgICovXG4gIHByaXZhdGUgX3Jlc2l6ZVRlcm1pbmFsKCkge1xuICAgIGlmICh0aGlzLl9vcHRpb25zLmF1dG9GaXQpIHtcbiAgICAgIHRoaXMuX2ZpdEFkZG9uLmZpdCgpO1xuICAgIH1cbiAgICBpZiAodGhpcy5fb2Zmc2V0V2lkdGggPT09IC0xKSB7XG4gICAgICB0aGlzLl9vZmZzZXRXaWR0aCA9IHRoaXMubm9kZS5vZmZzZXRXaWR0aDtcbiAgICB9XG4gICAgaWYgKHRoaXMuX29mZnNldEhlaWdodCA9PT0gLTEpIHtcbiAgICAgIHRoaXMuX29mZnNldEhlaWdodCA9IHRoaXMubm9kZS5vZmZzZXRIZWlnaHQ7XG4gICAgfVxuICAgIHRoaXMuX3NldFNlc3Npb25TaXplKCk7XG4gICAgdGhpcy5fbmVlZHNSZXNpemUgPSBmYWxzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHNpemUgb2YgdGhlIHRlcm1pbmFsIGluIHRoZSBzZXNzaW9uLlxuICAgKi9cbiAgcHJpdmF0ZSBfc2V0U2Vzc2lvblNpemUoKTogdm9pZCB7XG4gICAgY29uc3QgY29udGVudCA9IFtcbiAgICAgIHRoaXMuX3Rlcm0ucm93cyxcbiAgICAgIHRoaXMuX3Rlcm0uY29scyxcbiAgICAgIHRoaXMuX29mZnNldEhlaWdodCxcbiAgICAgIHRoaXMuX29mZnNldFdpZHRoXG4gICAgXTtcbiAgICBpZiAoIXRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgdGhpcy5zZXNzaW9uLnNlbmQoeyB0eXBlOiAnc2V0X3NpemUnLCBjb250ZW50IH0pO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgcmVhZG9ubHkgX3Rlcm06IFh0ZXJtO1xuICBwcml2YXRlIHJlYWRvbmx5IF9maXRBZGRvbjogRml0QWRkb247XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfbmVlZHNSZXNpemUgPSB0cnVlO1xuICBwcml2YXRlIF90ZXJtT3BlbmVkID0gZmFsc2U7XG4gIHByaXZhdGUgX29mZnNldFdpZHRoID0gLTE7XG4gIHByaXZhdGUgX29mZnNldEhlaWdodCA9IC0xO1xuICBwcml2YXRlIF9vcHRpb25zOiBJVGVybWluYWwuSU9wdGlvbnM7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQW4gaW5jcmVtZW50aW5nIGNvdW50ZXIgZm9yIGlkcy5cbiAgICovXG4gIGV4cG9ydCBsZXQgaWQgPSAwO1xuXG4gIC8qKlxuICAgKiBUaGUgbGlnaHQgdGVybWluYWwgdGhlbWUuXG4gICAqL1xuICBleHBvcnQgY29uc3QgbGlnaHRUaGVtZTogSVRlcm1pbmFsLklUaGVtZU9iamVjdCA9IHtcbiAgICBmb3JlZ3JvdW5kOiAnIzAwMCcsXG4gICAgYmFja2dyb3VuZDogJyNmZmYnLFxuICAgIGN1cnNvcjogJyM2MTYxNjEnLCAvLyBtZC1ncmV5LTcwMFxuICAgIGN1cnNvckFjY2VudDogJyNGNUY1RjUnLCAvLyBtZC1ncmV5LTEwMFxuICAgIHNlbGVjdGlvbjogJ3JnYmEoOTcsIDk3LCA5NywgMC4zKScgLy8gbWQtZ3JleS03MDBcbiAgfTtcblxuICAvKipcbiAgICogVGhlIGRhcmsgdGVybWluYWwgdGhlbWUuXG4gICAqL1xuICBleHBvcnQgY29uc3QgZGFya1RoZW1lOiBJVGVybWluYWwuSVRoZW1lT2JqZWN0ID0ge1xuICAgIGZvcmVncm91bmQ6ICcjZmZmJyxcbiAgICBiYWNrZ3JvdW5kOiAnIzAwMCcsXG4gICAgY3Vyc29yOiAnI2ZmZicsXG4gICAgY3Vyc29yQWNjZW50OiAnIzAwMCcsXG4gICAgc2VsZWN0aW9uOiAncmdiYSgyNTUsIDI1NSwgMjU1LCAwLjMpJ1xuICB9O1xuXG4gIC8qKlxuICAgKiBUaGUgY3VycmVudCB0aGVtZS5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBpbmhlcml0VGhlbWUgPSAoKTogSVRlcm1pbmFsLklUaGVtZU9iamVjdCA9PiAoe1xuICAgIGZvcmVncm91bmQ6IGdldENvbXB1dGVkU3R5bGUoZG9jdW1lbnQuYm9keSlcbiAgICAgIC5nZXRQcm9wZXJ0eVZhbHVlKCctLWpwLXVpLWZvbnQtY29sb3IwJylcbiAgICAgIC50cmltKCksXG4gICAgYmFja2dyb3VuZDogZ2V0Q29tcHV0ZWRTdHlsZShkb2N1bWVudC5ib2R5KVxuICAgICAgLmdldFByb3BlcnR5VmFsdWUoJy0tanAtbGF5b3V0LWNvbG9yMCcpXG4gICAgICAudHJpbSgpLFxuICAgIGN1cnNvcjogZ2V0Q29tcHV0ZWRTdHlsZShkb2N1bWVudC5ib2R5KVxuICAgICAgLmdldFByb3BlcnR5VmFsdWUoJy0tanAtdWktZm9udC1jb2xvcjEnKVxuICAgICAgLnRyaW0oKSxcbiAgICBjdXJzb3JBY2NlbnQ6IGdldENvbXB1dGVkU3R5bGUoZG9jdW1lbnQuYm9keSlcbiAgICAgIC5nZXRQcm9wZXJ0eVZhbHVlKCctLWpwLXVpLWludmVyc2UtZm9udC1jb2xvcjAnKVxuICAgICAgLnRyaW0oKSxcbiAgICBzZWxlY3Rpb246IGdldENvbXB1dGVkU3R5bGUoZG9jdW1lbnQuYm9keSlcbiAgICAgIC5nZXRQcm9wZXJ0eVZhbHVlKCctLWpwLXVpLWZvbnQtY29sb3IzJylcbiAgICAgIC50cmltKClcbiAgfSk7XG5cbiAgZXhwb3J0IGZ1bmN0aW9uIGdldFhUZXJtVGhlbWUoXG4gICAgdGhlbWU6IElUZXJtaW5hbC5UaGVtZVxuICApOiBJVGVybWluYWwuSVRoZW1lT2JqZWN0IHtcbiAgICBzd2l0Y2ggKHRoZW1lKSB7XG4gICAgICBjYXNlICdsaWdodCc6XG4gICAgICAgIHJldHVybiBsaWdodFRoZW1lO1xuICAgICAgY2FzZSAnZGFyayc6XG4gICAgICAgIHJldHVybiBkYXJrVGhlbWU7XG4gICAgICBjYXNlICdpbmhlcml0JzpcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIHJldHVybiBpbmhlcml0VGhlbWUoKTtcbiAgICB9XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0=