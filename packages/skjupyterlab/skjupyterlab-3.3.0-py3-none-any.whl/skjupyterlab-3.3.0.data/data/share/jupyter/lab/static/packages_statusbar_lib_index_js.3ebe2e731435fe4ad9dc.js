(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_statusbar_lib_index_js"],{

/***/ "../packages/statusbar/lib/components/group.js":
/*!*****************************************************!*\
  !*** ../packages/statusbar/lib/components/group.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GroupItem": () => (/* binding */ GroupItem)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var typestyle_lib__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! typestyle/lib */ "../node_modules/typestyle/lib/index.js");
/* harmony import */ var _style_layout__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/layout */ "../packages/statusbar/lib/style/layout.js");
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



const groupItemLayout = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_1__.style)(_style_layout__WEBPACK_IMPORTED_MODULE_2__.centeredFlex, _style_layout__WEBPACK_IMPORTED_MODULE_2__.leftToRight);
/**
 * A tsx component for a set of items logically grouped together.
 */
function GroupItem(props) {
    const { spacing, children, className } = props, rest = __rest(props, ["spacing", "children", "className"]);
    const numChildren = react__WEBPACK_IMPORTED_MODULE_0__.Children.count(children);
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", Object.assign({ className: (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_1__.classes)(groupItemLayout, className) }, rest), react__WEBPACK_IMPORTED_MODULE_0__.Children.map(children, (child, i) => {
        if (i === 0) {
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { marginRight: `${spacing}px` } }, child);
        }
        else if (i === numChildren - 1) {
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { marginLeft: `${spacing}px` } }, child);
        }
        else {
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { margin: `0px ${spacing}px` } }, child);
        }
    })));
}


/***/ }),

/***/ "../packages/statusbar/lib/components/hover.js":
/*!*****************************************************!*\
  !*** ../packages/statusbar/lib/components/hover.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "showPopup": () => (/* binding */ showPopup),
/* harmony export */   "Popup": () => (/* binding */ Popup)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var typestyle_lib__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! typestyle/lib */ "../node_modules/typestyle/lib/index.js");
/* harmony import */ var _style_statusbar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/statusbar */ "../packages/statusbar/lib/style/statusbar.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




const hoverItem = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_2__.style)({
    boxShadow: '0px 4px 4px rgba(0, 0, 0, 0.25)'
});
/**
 * Create and show a popup component.
 *
 * @param options - options for the popup
 *
 * @returns the popup that was created.
 */
function showPopup(options) {
    const dialog = new Popup(options);
    dialog.launch();
    return dialog;
}
/**
 * A class for a Popup widget.
 */
class Popup extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
     * Construct a new Popup.
     */
    constructor(options) {
        super();
        this._body = options.body;
        this._body.addClass(hoverItem);
        this._anchor = options.anchor;
        this._align = options.align;
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.PanelLayout());
        layout.addWidget(options.body);
        this._body.node.addEventListener('resize', () => {
            this.update();
        });
    }
    /**
     * Attach the popup widget to the page.
     */
    launch() {
        this._setGeometry();
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget.attach(this, document.body);
        this.update();
        this._anchor.addClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.clickedItem);
        this._anchor.removeClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.interactiveItem);
    }
    /**
     * Handle `'update'` messages for the widget.
     */
    onUpdateRequest(msg) {
        this._setGeometry();
        super.onUpdateRequest(msg);
    }
    /**
     * Handle `'after-attach'` messages for the widget.
     */
    onAfterAttach(msg) {
        document.addEventListener('click', this, false);
        this.node.addEventListener('keydown', this, false);
        window.addEventListener('resize', this, false);
    }
    /**
     * Handle `'after-detach'` messages for the widget.
     */
    onAfterDetach(msg) {
        document.removeEventListener('click', this, false);
        this.node.removeEventListener('keydown', this, false);
        window.removeEventListener('resize', this, false);
    }
    /**
     * Handle `'resize'` messages for the widget.
     */
    onResize() {
        this.update();
    }
    /**
     * Dispose of the widget.
     */
    dispose() {
        super.dispose();
        this._anchor.removeClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.clickedItem);
        this._anchor.addClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.interactiveItem);
    }
    /**
     * Handle DOM events for the widget.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'keydown':
                this._evtKeydown(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            case 'resize':
                this.onResize();
                break;
            default:
                break;
        }
    }
    _evtClick(event) {
        if (!!event.target &&
            !(this._body.node.contains(event.target) ||
                this._anchor.node.contains(event.target))) {
            this.dispose();
        }
    }
    _evtKeydown(event) {
        // Check for escape key
        switch (event.keyCode) {
            case 27: // Escape.
                event.stopPropagation();
                event.preventDefault();
                this.dispose();
                break;
            default:
                break;
        }
    }
    _setGeometry() {
        let aligned = 0;
        const anchorRect = this._anchor.node.getBoundingClientRect();
        const bodyRect = this._body.node.getBoundingClientRect();
        if (this._align === 'right') {
            aligned = -(bodyRect.width - anchorRect.width);
        }
        const style = window.getComputedStyle(this._body.node);
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.HoverBox.setGeometry({
            anchor: anchorRect,
            host: document.body,
            maxHeight: 500,
            minHeight: 20,
            node: this._body.node,
            offset: {
                horizontal: aligned
            },
            privilege: 'forceAbove',
            style
        });
    }
}


/***/ }),

/***/ "../packages/statusbar/lib/components/index.js":
/*!*****************************************************!*\
  !*** ../packages/statusbar/lib/components/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GroupItem": () => (/* reexport safe */ _group__WEBPACK_IMPORTED_MODULE_0__.GroupItem),
/* harmony export */   "Popup": () => (/* reexport safe */ _hover__WEBPACK_IMPORTED_MODULE_1__.Popup),
/* harmony export */   "showPopup": () => (/* reexport safe */ _hover__WEBPACK_IMPORTED_MODULE_1__.showPopup),
/* harmony export */   "ProgressBar": () => (/* reexport safe */ _progressBar__WEBPACK_IMPORTED_MODULE_2__.ProgressBar),
/* harmony export */   "TextItem": () => (/* reexport safe */ _text__WEBPACK_IMPORTED_MODULE_3__.TextItem)
/* harmony export */ });
/* harmony import */ var _group__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./group */ "../packages/statusbar/lib/components/group.js");
/* harmony import */ var _hover__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./hover */ "../packages/statusbar/lib/components/hover.js");
/* harmony import */ var _progressBar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./progressBar */ "../packages/statusbar/lib/components/progressBar.js");
/* harmony import */ var _text__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./text */ "../packages/statusbar/lib/components/text.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/***/ }),

/***/ "../packages/statusbar/lib/components/progressBar.js":
/*!***********************************************************!*\
  !*** ../packages/statusbar/lib/components/progressBar.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ProgressBar": () => (/* binding */ ProgressBar)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_progressBar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/progressBar */ "../packages/statusbar/lib/style/progressBar.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A functional tsx component for a progress bar.
 */
function ProgressBar(props) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_progressBar__WEBPACK_IMPORTED_MODULE_1__.progressBarItem },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(Filler, { percentage: props.percentage })));
}
/**
 * A functional tsx component for a partially filled div.
 */
function Filler(props) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_progressBar__WEBPACK_IMPORTED_MODULE_1__.fillerItem, style: {
            width: `${props.percentage}px`
        } }));
}


/***/ }),

/***/ "../packages/statusbar/lib/components/text.js":
/*!****************************************************!*\
  !*** ../packages/statusbar/lib/components/text.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TextItem": () => (/* binding */ TextItem)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var typestyle_lib__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! typestyle/lib */ "../node_modules/typestyle/lib/index.js");
/* harmony import */ var _style_text__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/text */ "../packages/statusbar/lib/style/text.js");
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
 * A functional tsx component for a text item.
 */
function TextItem(props) {
    const { title, source, className } = props, rest = __rest(props, ["title", "source", "className"]);
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", Object.assign({ className: (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_1__.classes)(_style_text__WEBPACK_IMPORTED_MODULE_2__.textItem, className), title: title }, rest), source));
}


/***/ }),

/***/ "../packages/statusbar/lib/defaults/index.js":
/*!***************************************************!*\
  !*** ../packages/statusbar/lib/defaults/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelStatus": () => (/* reexport safe */ _kernelStatus__WEBPACK_IMPORTED_MODULE_0__.KernelStatus),
/* harmony export */   "LineCol": () => (/* reexport safe */ _lineCol__WEBPACK_IMPORTED_MODULE_1__.LineCol),
/* harmony export */   "RunningSessions": () => (/* reexport safe */ _runningSessions__WEBPACK_IMPORTED_MODULE_2__.RunningSessions)
/* harmony export */ });
/* harmony import */ var _kernelStatus__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./kernelStatus */ "../packages/statusbar/lib/defaults/kernelStatus.js");
/* harmony import */ var _lineCol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./lineCol */ "../packages/statusbar/lib/defaults/lineCol.js");
/* harmony import */ var _runningSessions__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./runningSessions */ "../packages/statusbar/lib/defaults/runningSessions.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/***/ }),

/***/ "../packages/statusbar/lib/defaults/kernelStatus.js":
/*!**********************************************************!*\
  !*** ../packages/statusbar/lib/defaults/kernelStatus.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelStatus": () => (/* binding */ KernelStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var ___WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! .. */ "../packages/statusbar/lib/index.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * A pure functional component for rendering kernel status.
 */
function KernelStatusComponent(props) {
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    const trans = translator.load('jupyterlab');
    let statusText = '';
    if (props.status) {
        statusText = ` | ${props.status}`;
    }
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(___WEBPACK_IMPORTED_MODULE_4__.TextItem, { onClick: props.handleClick, source: `${props.kernelName}${statusText}`, title: trans.__('Change kernel for %1', props.activityName) }));
}
/**
 * A VDomRenderer widget for displaying the status of a kernel.
 */
class KernelStatus extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Construct the kernel status widget.
     */
    constructor(opts, translator) {
        super(new KernelStatus.Model(translator));
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._handleClick = opts.onClick;
        this.addClass(___WEBPACK_IMPORTED_MODULE_4__.interactiveItem);
    }
    /**
     * Render the kernel status item.
     */
    render() {
        if (this.model === null) {
            return null;
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(KernelStatusComponent, { status: this.model.status, kernelName: this.model.kernelName, activityName: this.model.activityName, handleClick: this._handleClick, translator: this.translator }));
        }
    }
}
/**
 * A namespace for KernelStatus statics.
 */
(function (KernelStatus) {
    /**
     * A VDomModel for the kernel status indicator.
     */
    class Model extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
        constructor(translator) {
            super();
            /**
             * React to changes to the kernel status.
             */
            this._onKernelStatusChanged = () => {
                var _a;
                this._kernelStatus = (_a = this._sessionContext) === null || _a === void 0 ? void 0 : _a.kernelDisplayStatus;
                this.stateChanged.emit(void 0);
            };
            /**
             * React to changes in the kernel.
             */
            this._onKernelChanged = (_sessionContext, change) => {
                var _a;
                const oldState = this._getAllState();
                // sync setting of status and display name
                this._kernelStatus = (_a = this._sessionContext) === null || _a === void 0 ? void 0 : _a.kernelDisplayStatus;
                this._kernelName = _sessionContext.kernelDisplayName;
                this._triggerChange(oldState, this._getAllState());
            };
            this._activityName = 'activity'; // FIXME-TRANS:?
            this._kernelStatus = '';
            this._sessionContext = null;
            translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
            this._trans = translator.load('jupyterlab');
            this._kernelName = this._trans.__('No Kernel!');
            // TODO-FIXME: this mapping is duplicated in apputils/toolbar.tsx
            this._statusNames = {
                unknown: this._trans.__('Unknown'),
                starting: this._trans.__('Starting'),
                idle: this._trans.__('Idle'),
                busy: this._trans.__('Busy'),
                terminating: this._trans.__('Terminating'),
                restarting: this._trans.__('Restarting'),
                autorestarting: this._trans.__('Autorestarting'),
                dead: this._trans.__('Dead'),
                connected: this._trans.__('Connected'),
                connecting: this._trans.__('Connecting'),
                disconnected: this._trans.__('Disconnected'),
                initializing: this._trans.__('Initializing'),
                '': ''
            };
        }
        /**
         * The name of the kernel.
         */
        get kernelName() {
            return this._kernelName;
        }
        /**
         * The current status of the kernel.
         */
        get status() {
            return this._kernelStatus
                ? this._statusNames[this._kernelStatus]
                : undefined;
        }
        /**
         * A display name for the activity.
         */
        get activityName() {
            return this._activityName;
        }
        set activityName(val) {
            const oldVal = this._activityName;
            if (oldVal === val) {
                return;
            }
            this._activityName = val;
            this.stateChanged.emit(void 0);
        }
        /**
         * The current client session associated with the kernel status indicator.
         */
        get sessionContext() {
            return this._sessionContext;
        }
        set sessionContext(sessionContext) {
            var _a, _b, _c;
            (_a = this._sessionContext) === null || _a === void 0 ? void 0 : _a.statusChanged.disconnect(this._onKernelStatusChanged);
            (_b = this._sessionContext) === null || _b === void 0 ? void 0 : _b.kernelChanged.disconnect(this._onKernelChanged);
            const oldState = this._getAllState();
            this._sessionContext = sessionContext;
            this._kernelStatus = sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.kernelDisplayStatus;
            this._kernelName = (_c = sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.kernelDisplayName) !== null && _c !== void 0 ? _c : this._trans.__('No Kernel');
            sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.statusChanged.connect(this._onKernelStatusChanged, this);
            sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.connectionStatusChanged.connect(this._onKernelStatusChanged, this);
            sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.kernelChanged.connect(this._onKernelChanged, this);
            this._triggerChange(oldState, this._getAllState());
        }
        _getAllState() {
            return [this._kernelName, this._kernelStatus, this._activityName];
        }
        _triggerChange(oldState, newState) {
            if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(oldState, newState)) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    KernelStatus.Model = Model;
})(KernelStatus || (KernelStatus = {}));


/***/ }),

/***/ "../packages/statusbar/lib/defaults/lineCol.js":
/*!*****************************************************!*\
  !*** ../packages/statusbar/lib/defaults/lineCol.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LineCol": () => (/* binding */ LineCol)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var typestyle_lib__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! typestyle/lib */ "../node_modules/typestyle/lib/index.js");
/* harmony import */ var ___WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! .. */ "../packages/statusbar/lib/index.js");
/* harmony import */ var _style_lineForm__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/lineForm */ "../packages/statusbar/lib/style/lineForm.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * A component for rendering a "go-to-line" form.
 */
class LineFormComponent extends (react__WEBPACK_IMPORTED_MODULE_3___default().Component) {
    /**
     * Construct a new LineFormComponent.
     */
    constructor(props) {
        super(props);
        /**
         * Handle a change to the value in the input field.
         */
        this._handleChange = (event) => {
            this.setState({ value: event.currentTarget.value });
        };
        /**
         * Handle submission of the input field.
         */
        this._handleSubmit = (event) => {
            event.preventDefault();
            const value = parseInt(this._textInput.value, 10);
            if (!isNaN(value) &&
                isFinite(value) &&
                1 <= value &&
                value <= this.props.maxLine) {
                this.props.handleSubmit(value);
            }
            return false;
        };
        /**
         * Handle focusing of the input field.
         */
        this._handleFocus = () => {
            this.setState({ hasFocus: true });
        };
        /**
         * Handle blurring of the input field.
         */
        this._handleBlur = () => {
            this.setState({ hasFocus: false });
        };
        this._textInput = null;
        this.translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.state = {
            value: '',
            hasFocus: false
        };
    }
    /**
     * Focus the element on mount.
     */
    componentDidMount() {
        this._textInput.focus();
    }
    /**
     * Render the LineFormComponent.
     */
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: _style_lineForm__WEBPACK_IMPORTED_MODULE_6__.lineFormSearch },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("form", { name: "lineColumnForm", onSubmit: this._handleSubmit, noValidate: true },
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_4__.classes)(_style_lineForm__WEBPACK_IMPORTED_MODULE_6__.lineFormWrapper, 'lm-lineForm-wrapper', this.state.hasFocus ? _style_lineForm__WEBPACK_IMPORTED_MODULE_6__.lineFormWrapperFocusWithin : undefined) },
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("input", { type: "text", className: _style_lineForm__WEBPACK_IMPORTED_MODULE_6__.lineFormInput, onChange: this._handleChange, onFocus: this._handleFocus, onBlur: this._handleBlur, value: this.state.value, ref: input => {
                            this._textInput = input;
                        } }),
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: _style_lineForm__WEBPACK_IMPORTED_MODULE_6__.lineFormButtonDiv },
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.lineFormIcon.react, { className: _style_lineForm__WEBPACK_IMPORTED_MODULE_6__.lineFormButtonIcon, elementPosition: "center" }),
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement("input", { type: "submit", className: _style_lineForm__WEBPACK_IMPORTED_MODULE_6__.lineFormButton, value: "" }))),
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("label", { className: _style_lineForm__WEBPACK_IMPORTED_MODULE_6__.lineFormCaption }, this._trans.__('Go to line number between 1 and %1', this.props.maxLine)))));
    }
}
/**
 * A pure functional component for rendering a line/column
 * status item.
 */
function LineColComponent(props) {
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    const trans = translator.load('jupyterlab');
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(___WEBPACK_IMPORTED_MODULE_5__.TextItem, { onClick: props.handleClick, source: trans.__('Ln %1, Col %2', props.line, props.column), title: trans.__('Go to line number…') }));
}
/**
 * A widget implementing a line/column status item.
 */
class LineCol extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Construct a new LineCol status item.
     */
    constructor(translator) {
        super(new LineCol.Model());
        this._popup = null;
        this.addClass(___WEBPACK_IMPORTED_MODULE_5__.interactiveItem);
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    }
    /**
     * Render the status item.
     */
    render() {
        if (this.model === null) {
            return null;
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(LineColComponent, { line: this.model.line, column: this.model.column, translator: this.translator, handleClick: () => this._handleClick() }));
        }
    }
    /**
     * A click handler for the widget.
     */
    _handleClick() {
        if (this._popup) {
            this._popup.dispose();
        }
        const body = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_3___default().createElement(LineFormComponent, { handleSubmit: val => this._handleSubmit(val), currentLine: this.model.line, maxLine: this.model.editor.lineCount, translator: this.translator }));
        this._popup = (0,___WEBPACK_IMPORTED_MODULE_5__.showPopup)({
            body: body,
            anchor: this,
            align: 'right'
        });
    }
    /**
     * Handle submission for the widget.
     */
    _handleSubmit(value) {
        this.model.editor.setCursorPosition({ line: value - 1, column: 0 });
        this._popup.dispose();
        this.model.editor.focus();
    }
}
/**
 * A namespace for LineCol statics.
 */
(function (LineCol) {
    /**
     * A VDom model for a status item tracking the line/column of an editor.
     */
    class Model extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
        constructor() {
            super(...arguments);
            /**
             * React to a change in the cursors of the current editor.
             */
            this._onSelectionChanged = () => {
                const oldState = this._getAllState();
                const pos = this.editor.getCursorPosition();
                this._line = pos.line + 1;
                this._column = pos.column + 1;
                this._triggerChange(oldState, this._getAllState());
            };
            this._line = 1;
            this._column = 1;
            this._editor = null;
        }
        /**
         * The current editor of the model.
         */
        get editor() {
            return this._editor;
        }
        set editor(editor) {
            const oldEditor = this._editor;
            if (oldEditor) {
                oldEditor.model.selections.changed.disconnect(this._onSelectionChanged);
            }
            const oldState = this._getAllState();
            this._editor = editor;
            if (!this._editor) {
                this._column = 1;
                this._line = 1;
            }
            else {
                this._editor.model.selections.changed.connect(this._onSelectionChanged);
                const pos = this._editor.getCursorPosition();
                this._column = pos.column + 1;
                this._line = pos.line + 1;
            }
            this._triggerChange(oldState, this._getAllState());
        }
        /**
         * The current line of the model.
         */
        get line() {
            return this._line;
        }
        /**
         * The current column of the model.
         */
        get column() {
            return this._column;
        }
        _getAllState() {
            return [this._line, this._column];
        }
        _triggerChange(oldState, newState) {
            if (oldState[0] !== newState[0] || oldState[1] !== newState[1]) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    LineCol.Model = Model;
})(LineCol || (LineCol = {}));


/***/ }),

/***/ "../packages/statusbar/lib/defaults/runningSessions.js":
/*!*************************************************************!*\
  !*** ../packages/statusbar/lib/defaults/runningSessions.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunningSessions": () => (/* binding */ RunningSessions)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var ___WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! .. */ "../packages/statusbar/lib/index.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * Half spacing between subitems in a status item.
 */
const HALF_SPACING = 4;
/**
 * A pure functional component for rendering kernel and terminal sessions.
 *
 * @param props: the props for the component.
 *
 * @returns a tsx component for the running sessions.
 */
function RunningSessionsComponent(props) {
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(___WEBPACK_IMPORTED_MODULE_4__.GroupItem, { spacing: HALF_SPACING, onClick: props.handleClick },
        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(___WEBPACK_IMPORTED_MODULE_4__.GroupItem, { spacing: HALF_SPACING },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(___WEBPACK_IMPORTED_MODULE_4__.TextItem, { source: props.terminals }),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.terminalIcon.react, { left: '1px', top: '3px', stylesheet: 'statusBar' })),
        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(___WEBPACK_IMPORTED_MODULE_4__.GroupItem, { spacing: HALF_SPACING },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(___WEBPACK_IMPORTED_MODULE_4__.TextItem, { source: props.sessions }),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.kernelIcon.react, { top: '2px', stylesheet: 'statusBar' }))));
}
/**
 * A VDomRenderer for a RunningSessions status item.
 */
class RunningSessions extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Create a new RunningSessions widget.
     */
    constructor(opts) {
        super(new RunningSessions.Model());
        this._serviceManager = opts.serviceManager;
        this._handleClick = opts.onClick;
        this.translator = opts.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterload');
        this._serviceManager.sessions.runningChanged.connect(this._onSessionsRunningChanged, this);
        this._serviceManager.terminals.runningChanged.connect(this._onTerminalsRunningChanged, this);
        this.addClass(___WEBPACK_IMPORTED_MODULE_4__.interactiveItem);
    }
    /**
     * Render the running sessions widget.
     */
    render() {
        if (!this.model) {
            return null;
        }
        // TODO-TRANS: Should probably be handled differently.
        // This is more localizable friendly: "Terminals: %1 | Kernels: %2"
        this.title.caption = this._trans.__('%1 Terminals, %2 Kernel sessions', this.model.terminals, this.model.sessions);
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(RunningSessionsComponent, { sessions: this.model.sessions, terminals: this.model.terminals, handleClick: this._handleClick }));
    }
    /**
     * Dispose of the status item.
     */
    dispose() {
        super.dispose();
        this._serviceManager.sessions.runningChanged.disconnect(this._onSessionsRunningChanged, this);
        this._serviceManager.terminals.runningChanged.disconnect(this._onTerminalsRunningChanged, this);
    }
    /**
     * Set the number of kernel sessions when the list changes.
     */
    _onSessionsRunningChanged(manager, sessions) {
        this.model.sessions = sessions.length;
    }
    /**
     * Set the number of terminal sessions when the list changes.
     */
    _onTerminalsRunningChanged(manager, terminals) {
        this.model.terminals = terminals.length;
    }
}
/**
 * A namespace for RunningSessions statics.
 */
(function (RunningSessions) {
    /**
     * A VDomModel for the RunningSessions status item.
     */
    class Model extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
        constructor() {
            super(...arguments);
            this._terminals = 0;
            this._sessions = 0;
        }
        /**
         * The number of active kernel sessions.
         */
        get sessions() {
            return this._sessions;
        }
        set sessions(sessions) {
            const oldSessions = this._sessions;
            this._sessions = sessions;
            if (oldSessions !== this._sessions) {
                this.stateChanged.emit(void 0);
            }
        }
        /**
         * The number of active terminal sessions.
         */
        get terminals() {
            return this._terminals;
        }
        set terminals(terminals) {
            const oldTerminals = this._terminals;
            this._terminals = terminals;
            if (oldTerminals !== this._terminals) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    RunningSessions.Model = Model;
})(RunningSessions || (RunningSessions = {}));


/***/ }),

/***/ "../packages/statusbar/lib/index.js":
/*!******************************************!*\
  !*** ../packages/statusbar/lib/index.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GroupItem": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.GroupItem),
/* harmony export */   "Popup": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.Popup),
/* harmony export */   "ProgressBar": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.ProgressBar),
/* harmony export */   "TextItem": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.TextItem),
/* harmony export */   "showPopup": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.showPopup),
/* harmony export */   "KernelStatus": () => (/* reexport safe */ _defaults__WEBPACK_IMPORTED_MODULE_1__.KernelStatus),
/* harmony export */   "LineCol": () => (/* reexport safe */ _defaults__WEBPACK_IMPORTED_MODULE_1__.LineCol),
/* harmony export */   "RunningSessions": () => (/* reexport safe */ _defaults__WEBPACK_IMPORTED_MODULE_1__.RunningSessions),
/* harmony export */   "StatusBar": () => (/* reexport safe */ _statusbar__WEBPACK_IMPORTED_MODULE_2__.StatusBar),
/* harmony export */   "clickedItem": () => (/* reexport safe */ _style_statusbar__WEBPACK_IMPORTED_MODULE_3__.clickedItem),
/* harmony export */   "interactiveItem": () => (/* reexport safe */ _style_statusbar__WEBPACK_IMPORTED_MODULE_3__.interactiveItem),
/* harmony export */   "item": () => (/* reexport safe */ _style_statusbar__WEBPACK_IMPORTED_MODULE_3__.item),
/* harmony export */   "leftSide": () => (/* reexport safe */ _style_statusbar__WEBPACK_IMPORTED_MODULE_3__.leftSide),
/* harmony export */   "rightSide": () => (/* reexport safe */ _style_statusbar__WEBPACK_IMPORTED_MODULE_3__.rightSide),
/* harmony export */   "side": () => (/* reexport safe */ _style_statusbar__WEBPACK_IMPORTED_MODULE_3__.side),
/* harmony export */   "statusBar": () => (/* reexport safe */ _style_statusbar__WEBPACK_IMPORTED_MODULE_3__.statusBar),
/* harmony export */   "IStatusBar": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.IStatusBar)
/* harmony export */ });
/* harmony import */ var _components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./components */ "../packages/statusbar/lib/components/index.js");
/* harmony import */ var _defaults__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./defaults */ "../packages/statusbar/lib/defaults/index.js");
/* harmony import */ var _statusbar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./statusbar */ "../packages/statusbar/lib/statusbar.js");
/* harmony import */ var _style_statusbar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./style/statusbar */ "../packages/statusbar/lib/style/statusbar.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tokens */ "../packages/statusbar/lib/tokens.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module statusbar
 */







/***/ }),

/***/ "../packages/statusbar/lib/statusbar.js":
/*!**********************************************!*\
  !*** ../packages/statusbar/lib/statusbar.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "StatusBar": () => (/* binding */ StatusBar)
/* harmony export */ });
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _style_statusbar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./style/statusbar */ "../packages/statusbar/lib/style/statusbar.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * Main status bar object which contains all items.
 */
class StatusBar extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor() {
        super();
        this._leftRankItems = [];
        this._rightRankItems = [];
        this._statusItems = {};
        this._disposables = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableSet();
        this.addClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.statusBar);
        const rootLayout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout());
        const leftPanel = (this._leftSide = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel());
        const middlePanel = (this._middlePanel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel());
        const rightPanel = (this._rightSide = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel());
        leftPanel.addClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.side);
        leftPanel.addClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.leftSide);
        middlePanel.addClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.side);
        rightPanel.addClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.side);
        rightPanel.addClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.rightSide);
        rootLayout.addWidget(leftPanel);
        rootLayout.addWidget(middlePanel);
        rootLayout.addWidget(rightPanel);
    }
    /**
     * Register a new status item.
     *
     * @param id - a unique id for the status item.
     *
     * @param statusItem - The item to add to the status bar.
     */
    registerStatusItem(id, statusItem) {
        if (id in this._statusItems) {
            throw new Error(`Status item ${id} already registered.`);
        }
        // Populate defaults for the optional properties of the status item.
        const fullStatusItem = Object.assign(Object.assign({}, Private.statusItemDefaults), statusItem);
        const { align, item, rank } = fullStatusItem;
        // Connect the activeStateChanged signal to refreshing the status item,
        // if the signal was provided.
        const onActiveStateChanged = () => {
            this._refreshItem(id);
        };
        if (fullStatusItem.activeStateChanged) {
            fullStatusItem.activeStateChanged.connect(onActiveStateChanged);
        }
        const rankItem = { id, rank };
        fullStatusItem.item.addClass(_style_statusbar__WEBPACK_IMPORTED_MODULE_3__.item);
        this._statusItems[id] = fullStatusItem;
        if (align === 'left') {
            const insertIndex = this._findInsertIndex(this._leftRankItems, rankItem);
            if (insertIndex === -1) {
                this._leftSide.addWidget(item);
                this._leftRankItems.push(rankItem);
            }
            else {
                _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.insert(this._leftRankItems, insertIndex, rankItem);
                this._leftSide.insertWidget(insertIndex, item);
            }
        }
        else if (align === 'right') {
            const insertIndex = this._findInsertIndex(this._rightRankItems, rankItem);
            if (insertIndex === -1) {
                this._rightSide.addWidget(item);
                this._rightRankItems.push(rankItem);
            }
            else {
                _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.insert(this._rightRankItems, insertIndex, rankItem);
                this._rightSide.insertWidget(insertIndex, item);
            }
        }
        else {
            this._middlePanel.addWidget(item);
        }
        this._refreshItem(id); // Initially refresh the status item.
        const disposable = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            delete this._statusItems[id];
            if (fullStatusItem.activeStateChanged) {
                fullStatusItem.activeStateChanged.disconnect(onActiveStateChanged);
            }
            item.parent = null;
            item.dispose();
        });
        this._disposables.add(disposable);
        return disposable;
    }
    /**
     * Dispose of the status bar.
     */
    dispose() {
        this._leftRankItems.length = 0;
        this._rightRankItems.length = 0;
        this._disposables.dispose();
        super.dispose();
    }
    /**
     * Handle an 'update-request' message to the status bar.
     */
    onUpdateRequest(msg) {
        this._refreshAll();
        super.onUpdateRequest(msg);
    }
    _findInsertIndex(side, newItem) {
        return _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.findFirstIndex(side, item => item.rank > newItem.rank);
    }
    _refreshItem(id) {
        const statusItem = this._statusItems[id];
        if (statusItem.isActive()) {
            statusItem.item.show();
            statusItem.item.update();
        }
        else {
            statusItem.item.hide();
        }
    }
    _refreshAll() {
        Object.keys(this._statusItems).forEach(id => {
            this._refreshItem(id);
        });
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Default options for a status item, less the item itself.
     */
    Private.statusItemDefaults = {
        align: 'left',
        rank: 0,
        isActive: () => true,
        activeStateChanged: undefined
    };
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/statusbar/lib/style/layout.js":
/*!*************************************************!*\
  !*** ../packages/statusbar/lib/style/layout.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "centeredFlex": () => (/* binding */ centeredFlex),
/* harmony export */   "leftToRight": () => (/* binding */ leftToRight),
/* harmony export */   "rightToLeft": () => (/* binding */ rightToLeft),
/* harmony export */   "equiDistant": () => (/* binding */ equiDistant)
/* harmony export */ });
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
const centeredFlex = {
    display: 'flex',
    alignItems: 'center'
};
const leftToRight = {
    flexDirection: 'row'
};
const rightToLeft = {
    flexDirection: 'row-reverse'
};
const equiDistant = {
    justifyContent: 'space-between'
};


/***/ }),

/***/ "../packages/statusbar/lib/style/lineForm.js":
/*!***************************************************!*\
  !*** ../packages/statusbar/lib/style/lineForm.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "hoverItem": () => (/* binding */ hoverItem),
/* harmony export */   "lineFormSearch": () => (/* binding */ lineFormSearch),
/* harmony export */   "lineFormCaption": () => (/* binding */ lineFormCaption),
/* harmony export */   "baseLineForm": () => (/* binding */ baseLineForm),
/* harmony export */   "lineFormButtonDiv": () => (/* binding */ lineFormButtonDiv),
/* harmony export */   "lineFormButtonIcon": () => (/* binding */ lineFormButtonIcon),
/* harmony export */   "lineFormButton": () => (/* binding */ lineFormButton),
/* harmony export */   "lineFormWrapper": () => (/* binding */ lineFormWrapper),
/* harmony export */   "lineFormWrapperFocusWithin": () => (/* binding */ lineFormWrapperFocusWithin),
/* harmony export */   "lineFormInput": () => (/* binding */ lineFormInput)
/* harmony export */ });
/* harmony import */ var typestyle_lib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle/lib */ "../node_modules/typestyle/lib/index.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

const hoverItem = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    boxShadow: '0px 4px 4px rgba(0, 0, 0, 0.25)'
});
const lineFormSearch = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    padding: '4px 12px',
    backgroundColor: 'var(--jp-layout-color2)',
    boxShadow: 'var(--jp-toolbar-box-shadow)',
    zIndex: 2,
    fontSize: 'var(--jp-ui-font-size1)'
});
const lineFormCaption = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    fontSize: 'var(--jp-ui-font-size0)',
    lineHeight: 'var(--jp-ui-font-size1)',
    marginTop: '4px',
    color: 'var(--jp-ui-font-color0)'
});
const baseLineForm = {
    border: 'none',
    borderRadius: '0px',
    position: 'absolute',
    backgroundSize: '16px',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    outline: 'none',
    top: '0px',
    right: '0px'
};
const lineFormButtonDiv = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)(baseLineForm, {
    top: '4px',
    right: '8px',
    height: '24px',
    padding: '0px 12px',
    width: '12px'
});
const lineFormButtonIcon = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)(baseLineForm, {
    backgroundColor: 'var(--jp-brand-color1)',
    height: '100%',
    width: '100%',
    boxSizing: 'border-box',
    padding: '4px 6px'
});
const lineFormButton = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)(baseLineForm, {
    backgroundColor: 'transparent',
    height: '100%',
    width: '100%',
    boxSizing: 'border-box'
});
const lineFormWrapper = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    overflow: 'hidden',
    padding: '0px 8px',
    border: '1px solid var(--jp-border-color0)',
    backgroundColor: 'var(--jp-input-active-background)',
    height: '22px'
});
const lineFormWrapperFocusWithin = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    border: 'var(--jp-border-width) solid var(--md-blue-500)',
    boxShadow: 'inset 0 0 4px var(--md-blue-300)'
});
const lineFormInput = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    background: 'transparent',
    width: '200px',
    height: '100%',
    border: 'none',
    outline: 'none',
    color: 'var(--jp-ui-font-color0)',
    lineHeight: '28px'
});


/***/ }),

/***/ "../packages/statusbar/lib/style/progressBar.js":
/*!******************************************************!*\
  !*** ../packages/statusbar/lib/style/progressBar.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "progressBarItem": () => (/* binding */ progressBarItem),
/* harmony export */   "fillerItem": () => (/* binding */ fillerItem)
/* harmony export */ });
/* harmony import */ var typestyle_lib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle/lib */ "../node_modules/typestyle/lib/index.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

const progressBarItem = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    background: 'black',
    height: '10px',
    width: '100px',
    border: '1px solid black',
    borderRadius: '3px',
    marginLeft: '4px',
    overflow: 'hidden'
});
const fillerItem = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    background: 'var(--jp-brand-color2)',
    height: '10px'
});


/***/ }),

/***/ "../packages/statusbar/lib/style/statusbar.js":
/*!****************************************************!*\
  !*** ../packages/statusbar/lib/style/statusbar.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "statusBar": () => (/* binding */ statusBar),
/* harmony export */   "side": () => (/* binding */ side),
/* harmony export */   "leftSide": () => (/* binding */ leftSide),
/* harmony export */   "rightSide": () => (/* binding */ rightSide),
/* harmony export */   "item": () => (/* binding */ item),
/* harmony export */   "clickedItem": () => (/* binding */ clickedItem),
/* harmony export */   "interactiveItem": () => (/* binding */ interactiveItem)
/* harmony export */ });
/* harmony import */ var typestyle_lib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle/lib */ "../node_modules/typestyle/lib/index.js");
/* harmony import */ var _layout__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./layout */ "../packages/statusbar/lib/style/layout.js");
/* harmony import */ var _text__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./text */ "../packages/statusbar/lib/style/text.js");
/* harmony import */ var _variables__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./variables */ "../packages/statusbar/lib/style/variables.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




const itemPadding = {
    paddingLeft: _variables__WEBPACK_IMPORTED_MODULE_3__.default.itemPadding,
    paddingRight: _variables__WEBPACK_IMPORTED_MODULE_3__.default.itemPadding
};
const interactiveHover = {
    $nest: {
        '&:hover': {
            backgroundColor: _variables__WEBPACK_IMPORTED_MODULE_3__.default.hoverColor
        }
    }
};
const clicked = {
    backgroundColor: _variables__WEBPACK_IMPORTED_MODULE_3__.default.clickColor,
    $nest: {
        ['.' + _text__WEBPACK_IMPORTED_MODULE_2__.textItem]: {
            color: _variables__WEBPACK_IMPORTED_MODULE_3__.default.textClickColor
        }
    }
};
const statusBar = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    background: _variables__WEBPACK_IMPORTED_MODULE_3__.default.backgroundColor,
    minHeight: _variables__WEBPACK_IMPORTED_MODULE_3__.default.height,
    justifyContent: 'space-between',
    paddingLeft: _variables__WEBPACK_IMPORTED_MODULE_3__.default.statusBarPadding,
    paddingRight: _variables__WEBPACK_IMPORTED_MODULE_3__.default.statusBarPadding
}, _layout__WEBPACK_IMPORTED_MODULE_1__.centeredFlex);
const side = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)(_layout__WEBPACK_IMPORTED_MODULE_1__.centeredFlex);
const leftSide = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)(_layout__WEBPACK_IMPORTED_MODULE_1__.leftToRight);
const rightSide = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)(_layout__WEBPACK_IMPORTED_MODULE_1__.rightToLeft);
const item = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)({
    maxHeight: _variables__WEBPACK_IMPORTED_MODULE_3__.default.height,
    marginLeft: _variables__WEBPACK_IMPORTED_MODULE_3__.default.itemMargin,
    marginRight: _variables__WEBPACK_IMPORTED_MODULE_3__.default.itemMargin,
    height: _variables__WEBPACK_IMPORTED_MODULE_3__.default.height,
    whiteSpace: _variables__WEBPACK_IMPORTED_MODULE_3__.default.whiteSpace,
    textOverflow: _variables__WEBPACK_IMPORTED_MODULE_3__.default.textOverflow,
    color: _variables__WEBPACK_IMPORTED_MODULE_3__.default.textColor
}, itemPadding);
const clickedItem = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)(clicked);
const interactiveItem = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)(interactiveHover);


/***/ }),

/***/ "../packages/statusbar/lib/style/text.js":
/*!***********************************************!*\
  !*** ../packages/statusbar/lib/style/text.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "baseText": () => (/* binding */ baseText),
/* harmony export */   "textItem": () => (/* binding */ textItem)
/* harmony export */ });
/* harmony import */ var typestyle_lib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle/lib */ "../node_modules/typestyle/lib/index.js");
/* harmony import */ var _variables__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./variables */ "../packages/statusbar/lib/style/variables.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


const baseText = {
    fontSize: _variables__WEBPACK_IMPORTED_MODULE_1__.default.fontSize,
    fontFamily: _variables__WEBPACK_IMPORTED_MODULE_1__.default.fontFamily
};
const textItem = (0,typestyle_lib__WEBPACK_IMPORTED_MODULE_0__.style)(baseText, {
    lineHeight: '24px',
    color: _variables__WEBPACK_IMPORTED_MODULE_1__.default.textColor
});


/***/ }),

/***/ "../packages/statusbar/lib/style/variables.js":
/*!****************************************************!*\
  !*** ../packages/statusbar/lib/style/variables.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
    hoverColor: 'var(--jp-layout-color3)',
    clickColor: 'var(--jp-brand-color1)',
    backgroundColor: 'var(--jp-layout-color2)',
    height: 'var(--jp-statusbar-height)',
    fontSize: 'var(--jp-ui-font-size1)',
    fontFamily: 'var(--jp-ui-font-family)',
    textColor: 'var(--jp-ui-font-color1)',
    textClickColor: 'white',
    itemMargin: '2px',
    itemPadding: '6px',
    statusBarPadding: '10px',
    interItemHalfSpacing: '2px',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis'
});


/***/ }),

/***/ "../packages/statusbar/lib/tokens.js":
/*!*******************************************!*\
  !*** ../packages/statusbar/lib/tokens.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IStatusBar": () => (/* binding */ IStatusBar)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// tslint:disable-next-line:variable-name
const IStatusBar = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/statusbar:IStatusBar');


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyL3NyYy9jb21wb25lbnRzL2dyb3VwLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyL3NyYy9jb21wb25lbnRzL2hvdmVyLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyL3NyYy9jb21wb25lbnRzL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL2NvbXBvbmVudHMvcHJvZ3Jlc3NCYXIudHN4Iiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL2NvbXBvbmVudHMvdGV4dC50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXR1c2Jhci9zcmMvZGVmYXVsdHMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXR1c2Jhci9zcmMvZGVmYXVsdHMva2VybmVsU3RhdHVzLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyL3NyYy9kZWZhdWx0cy9saW5lQ29sLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyL3NyYy9kZWZhdWx0cy9ydW5uaW5nU2Vzc2lvbnMudHN4Iiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL3N0YXR1c2Jhci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyL3NyYy9zdHlsZS9sYXlvdXQudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXR1c2Jhci9zcmMvc3R5bGUvbGluZUZvcm0udHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXR1c2Jhci9zcmMvc3R5bGUvcHJvZ3Jlc3NCYXIudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXR1c2Jhci9zcmMvc3R5bGUvc3RhdHVzYmFyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL3N0eWxlL3RleHQudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXR1c2Jhci9zcmMvc3R5bGUvdmFyaWFibGVzLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL3Rva2Vucy50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7Ozs7Ozs7Ozs7OztBQUU1QjtBQUNnQjtBQUNhO0FBRTVELE1BQU0sZUFBZSxHQUFHLG9EQUFLLENBQUMsdURBQVksRUFBRSxzREFBVyxDQUFDLENBQUM7QUFFekQ7O0dBRUc7QUFDSSxTQUFTLFNBQVMsQ0FDdkIsS0FBOEQ7SUFFOUQsTUFBTSxFQUFFLE9BQU8sRUFBRSxRQUFRLEVBQUUsU0FBUyxLQUFjLEtBQUssRUFB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QyxVQUFVLEVBQUUsMEJBQTBCO0lBQ3RDLFNBQVMsRUFBRSwwQkFBMEI7SUFDckMsY0FBYyxFQUFFLE9BQU87SUFDdkIsVUFBVSxFQUFFLEtBQUs7SUFDakIsV0FBVyxFQUFFLEtBQUs7SUFDbEIsZ0JBQWdCLEVBQUUsTUFBTTtJQUN4QixvQkFBb0IsRUFBRSxLQUFLO0lBQzNCLFVBQVUsRUFBRSxRQUErQjtJQUMzQyxZQUFZLEVBQUUsVUFBVTtDQUN6QixFQUFDOzs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNuQkYsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUVqQjtBQUsxQyx5Q0FBeUM7QUFDbEMsTUFBTSxVQUFVLEdBQUcsSUFBSSxvREFBSyxDQUNqQyxrQ0FBa0MsQ0FDbkMsQ0FBQyIsImZpbGUiOiJwYWNrYWdlc19zdGF0dXNiYXJfbGliX2luZGV4X2pzLjNlYmUyZTczMTQzNWZlNGFkOWRjLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBjbGFzc2VzLCBzdHlsZSB9IGZyb20gJ3R5cGVzdHlsZS9saWInO1xuaW1wb3J0IHsgY2VudGVyZWRGbGV4LCBsZWZ0VG9SaWdodCB9IGZyb20gJy4uL3N0eWxlL2xheW91dCc7XG5cbmNvbnN0IGdyb3VwSXRlbUxheW91dCA9IHN0eWxlKGNlbnRlcmVkRmxleCwgbGVmdFRvUmlnaHQpO1xuXG4vKipcbiAqIEEgdHN4IGNvbXBvbmVudCBmb3IgYSBzZXQgb2YgaXRlbXMgbG9naWNhbGx5IGdyb3VwZWQgdG9nZXRoZXIuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBHcm91cEl0ZW0oXG4gIHByb3BzOiBHcm91cEl0ZW0uSVByb3BzICYgUmVhY3QuSFRNTEF0dHJpYnV0ZXM8SFRNTERpdkVsZW1lbnQ+XG4pOiBSZWFjdC5SZWFjdEVsZW1lbnQ8R3JvdXBJdGVtLklQcm9wcz4ge1xuICBjb25zdCB7IHNwYWNpbmcsIGNoaWxkcmVuLCBjbGFzc05hbWUsIC4uLnJlc3QgfSA9IHByb3BzO1xuICBjb25zdCBudW1DaGlsZHJlbiA9IFJlYWN0LkNoaWxkcmVuLmNvdW50KGNoaWxkcmVuKTtcblxuICByZXR1cm4gKFxuICAgIDxkaXYgY2xhc3NOYW1lPXtjbGFzc2VzKGdyb3VwSXRlbUxheW91dCwgY2xhc3NOYW1lKX0gey4uLnJlc3R9PlxuICAgICAge1JlYWN0LkNoaWxkcmVuLm1hcChjaGlsZHJlbiwgKGNoaWxkLCBpKSA9PiB7XG4gICAgICAgIGlmIChpID09PSAwKSB7XG4gICAgICAgICAgcmV0dXJuIDxkaXYgc3R5bGU9e3sgbWFyZ2luUmlnaHQ6IGAke3NwYWNpbmd9cHhgIH19PntjaGlsZH08L2Rpdj47XG4gICAgICAgIH0gZWxzZSBpZiAoaSA9PT0gbnVtQ2hpbGRyZW4gLSAxKSB7XG4gICAgICAgICAgcmV0dXJuIDxkaXYgc3R5bGU9e3sgbWFyZ2luTGVmdDogYCR7c3BhY2luZ31weGAgfX0+e2NoaWxkfTwvZGl2PjtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXR1cm4gPGRpdiBzdHlsZT17eyBtYXJnaW46IGAwcHggJHtzcGFjaW5nfXB4YCB9fT57Y2hpbGR9PC9kaXY+O1xuICAgICAgICB9XG4gICAgICB9KX1cbiAgICA8L2Rpdj5cbiAgKTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgR3JvdXBJdGVtIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgR3JvdXBJdGVtIHtcbiAgLyoqXG4gICAqIFByb3BzIGZvciB0aGUgR3JvdXBJdGVtLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIFRoZSBzcGFjaW5nLCBpbiBweCwgYmV0d2VlbiB0aGUgaXRlbXMgaW4gdGhlIGdyb3VwLlxuICAgICAqL1xuICAgIHNwYWNpbmc6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBpdGVtcyB0byBhcnJhbmdlIGluIGEgZ3JvdXAuXG4gICAgICovXG4gICAgY2hpbGRyZW46IEpTWC5FbGVtZW50W107XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSG92ZXJCb3ggfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgUGFuZWxMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBzdHlsZSB9IGZyb20gJ3R5cGVzdHlsZS9saWInO1xuaW1wb3J0IHsgY2xpY2tlZEl0ZW0sIGludGVyYWN0aXZlSXRlbSB9IGZyb20gJy4uL3N0eWxlL3N0YXR1c2Jhcic7XG5cbmNvbnN0IGhvdmVySXRlbSA9IHN0eWxlKHtcbiAgYm94U2hhZG93OiAnMHB4IDRweCA0cHggcmdiYSgwLCAwLCAwLCAwLjI1KSdcbn0pO1xuXG4vKipcbiAqIENyZWF0ZSBhbmQgc2hvdyBhIHBvcHVwIGNvbXBvbmVudC5cbiAqXG4gKiBAcGFyYW0gb3B0aW9ucyAtIG9wdGlvbnMgZm9yIHRoZSBwb3B1cFxuICpcbiAqIEByZXR1cm5zIHRoZSBwb3B1cCB0aGF0IHdhcyBjcmVhdGVkLlxuICovXG5leHBvcnQgZnVuY3Rpb24gc2hvd1BvcHVwKG9wdGlvbnM6IFBvcHVwLklPcHRpb25zKTogUG9wdXAge1xuICBjb25zdCBkaWFsb2cgPSBuZXcgUG9wdXAob3B0aW9ucyk7XG4gIGRpYWxvZy5sYXVuY2goKTtcbiAgcmV0dXJuIGRpYWxvZztcbn1cblxuLyoqXG4gKiBBIGNsYXNzIGZvciBhIFBvcHVwIHdpZGdldC5cbiAqL1xuZXhwb3J0IGNsYXNzIFBvcHVwIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBQb3B1cC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IFBvcHVwLklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl9ib2R5ID0gb3B0aW9ucy5ib2R5O1xuICAgIHRoaXMuX2JvZHkuYWRkQ2xhc3MoaG92ZXJJdGVtKTtcbiAgICB0aGlzLl9hbmNob3IgPSBvcHRpb25zLmFuY2hvcjtcbiAgICB0aGlzLl9hbGlnbiA9IG9wdGlvbnMuYWxpZ247XG4gICAgY29uc3QgbGF5b3V0ID0gKHRoaXMubGF5b3V0ID0gbmV3IFBhbmVsTGF5b3V0KCkpO1xuICAgIGxheW91dC5hZGRXaWRnZXQob3B0aW9ucy5ib2R5KTtcbiAgICB0aGlzLl9ib2R5Lm5vZGUuYWRkRXZlbnRMaXN0ZW5lcigncmVzaXplJywgKCkgPT4ge1xuICAgICAgdGhpcy51cGRhdGUoKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBdHRhY2ggdGhlIHBvcHVwIHdpZGdldCB0byB0aGUgcGFnZS5cbiAgICovXG4gIGxhdW5jaCgpIHtcbiAgICB0aGlzLl9zZXRHZW9tZXRyeSgpO1xuICAgIFdpZGdldC5hdHRhY2godGhpcywgZG9jdW1lbnQuYm9keSk7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgICB0aGlzLl9hbmNob3IuYWRkQ2xhc3MoY2xpY2tlZEl0ZW0pO1xuICAgIHRoaXMuX2FuY2hvci5yZW1vdmVDbGFzcyhpbnRlcmFjdGl2ZUl0ZW0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ3VwZGF0ZSdgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uVXBkYXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLl9zZXRHZW9tZXRyeSgpO1xuICAgIHN1cGVyLm9uVXBkYXRlUmVxdWVzdChtc2cpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ2FmdGVyLWF0dGFjaCdgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCB0aGlzLCBmYWxzZSk7XG4gICAgdGhpcy5ub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCB0aGlzLCBmYWxzZSk7XG4gICAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ3Jlc2l6ZScsIHRoaXMsIGZhbHNlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhZnRlci1kZXRhY2gnYCBtZXNzYWdlcyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFmdGVyRGV0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGRvY3VtZW50LnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcywgZmFsc2UpO1xuICAgIHRoaXMubm9kZS5yZW1vdmVFdmVudExpc3RlbmVyKCdrZXlkb3duJywgdGhpcywgZmFsc2UpO1xuICAgIHdpbmRvdy5yZW1vdmVFdmVudExpc3RlbmVyKCdyZXNpemUnLCB0aGlzLCBmYWxzZSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAncmVzaXplJ2AgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25SZXNpemUoKTogdm9pZCB7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSB3aWRnZXQuXG4gICAqL1xuICBkaXNwb3NlKCkge1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgICB0aGlzLl9hbmNob3IucmVtb3ZlQ2xhc3MoY2xpY2tlZEl0ZW0pO1xuICAgIHRoaXMuX2FuY2hvci5hZGRDbGFzcyhpbnRlcmFjdGl2ZUl0ZW0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBET00gZXZlbnRzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgaGFuZGxlRXZlbnQoZXZlbnQ6IEV2ZW50KTogdm9pZCB7XG4gICAgc3dpdGNoIChldmVudC50eXBlKSB7XG4gICAgICBjYXNlICdrZXlkb3duJzpcbiAgICAgICAgdGhpcy5fZXZ0S2V5ZG93bihldmVudCBhcyBLZXlib2FyZEV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdjbGljayc6XG4gICAgICAgIHRoaXMuX2V2dENsaWNrKGV2ZW50IGFzIE1vdXNlRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3Jlc2l6ZSc6XG4gICAgICAgIHRoaXMub25SZXNpemUoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9ldnRDbGljayhldmVudDogTW91c2VFdmVudCk6IHZvaWQge1xuICAgIGlmIChcbiAgICAgICEhZXZlbnQudGFyZ2V0ICYmXG4gICAgICAhKFxuICAgICAgICB0aGlzLl9ib2R5Lm5vZGUuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50KSB8fFxuICAgICAgICB0aGlzLl9hbmNob3Iubm9kZS5jb250YWlucyhldmVudC50YXJnZXQgYXMgSFRNTEVsZW1lbnQpXG4gICAgICApXG4gICAgKSB7XG4gICAgICB0aGlzLmRpc3Bvc2UoKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9ldnRLZXlkb3duKGV2ZW50OiBLZXlib2FyZEV2ZW50KTogdm9pZCB7XG4gICAgLy8gQ2hlY2sgZm9yIGVzY2FwZSBrZXlcbiAgICBzd2l0Y2ggKGV2ZW50LmtleUNvZGUpIHtcbiAgICAgIGNhc2UgMjc6IC8vIEVzY2FwZS5cbiAgICAgICAgZXZlbnQuc3RvcFByb3BhZ2F0aW9uKCk7XG4gICAgICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICAgIHRoaXMuZGlzcG9zZSgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX3NldEdlb21ldHJ5KCk6IHZvaWQge1xuICAgIGxldCBhbGlnbmVkID0gMDtcbiAgICBjb25zdCBhbmNob3JSZWN0ID0gdGhpcy5fYW5jaG9yLm5vZGUuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCk7XG4gICAgY29uc3QgYm9keVJlY3QgPSB0aGlzLl9ib2R5Lm5vZGUuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCk7XG4gICAgaWYgKHRoaXMuX2FsaWduID09PSAncmlnaHQnKSB7XG4gICAgICBhbGlnbmVkID0gLShib2R5UmVjdC53aWR0aCAtIGFuY2hvclJlY3Qud2lkdGgpO1xuICAgIH1cbiAgICBjb25zdCBzdHlsZSA9IHdpbmRvdy5nZXRDb21wdXRlZFN0eWxlKHRoaXMuX2JvZHkubm9kZSk7XG4gICAgSG92ZXJCb3guc2V0R2VvbWV0cnkoe1xuICAgICAgYW5jaG9yOiBhbmNob3JSZWN0LFxuICAgICAgaG9zdDogZG9jdW1lbnQuYm9keSxcbiAgICAgIG1heEhlaWdodDogNTAwLFxuICAgICAgbWluSGVpZ2h0OiAyMCxcbiAgICAgIG5vZGU6IHRoaXMuX2JvZHkubm9kZSxcbiAgICAgIG9mZnNldDoge1xuICAgICAgICBob3Jpem9udGFsOiBhbGlnbmVkXG4gICAgICB9LFxuICAgICAgcHJpdmlsZWdlOiAnZm9yY2VBYm92ZScsXG4gICAgICBzdHlsZVxuICAgIH0pO1xuICB9XG5cbiAgcHJpdmF0ZSBfYm9keTogV2lkZ2V0O1xuICBwcml2YXRlIF9hbmNob3I6IFdpZGdldDtcbiAgcHJpdmF0ZSBfYWxpZ246ICdsZWZ0JyB8ICdyaWdodCcgfCB1bmRlZmluZWQ7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIFBvcHVwIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgUG9wdXAge1xuICAvKipcbiAgICogT3B0aW9ucyBmb3IgY3JlYXRpbmcgYSBQb3B1cCB3aWRnZXQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY29udGVudCBvZiB0aGUgcG9wdXAuXG4gICAgICovXG4gICAgYm9keTogV2lkZ2V0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHdpZGdldCB0byB3aGljaCB3ZSBhcmUgYXR0YWNoaW5nIHRoZSBwb3B1cC5cbiAgICAgKi9cbiAgICBhbmNob3I6IFdpZGdldDtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gYWxpZ24gdGhlIHBvcHVwIHRvIHRoZSBsZWZ0IG9yIHRoZSByaWdodCBvZiB0aGUgYW5jaG9yLlxuICAgICAqL1xuICAgIGFsaWduPzogJ2xlZnQnIHwgJ3JpZ2h0JztcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5leHBvcnQgKiBmcm9tICcuL2dyb3VwJztcbmV4cG9ydCAqIGZyb20gJy4vaG92ZXInO1xuZXhwb3J0ICogZnJvbSAnLi9wcm9ncmVzc0Jhcic7XG5leHBvcnQgKiBmcm9tICcuL3RleHQnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBmaWxsZXJJdGVtLCBwcm9ncmVzc0Jhckl0ZW0gfSBmcm9tICcuLi9zdHlsZS9wcm9ncmVzc0Jhcic7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIFByb2dyZXNzQmFyIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgUHJvZ3Jlc3NCYXIge1xuICAvKipcbiAgICogUHJvcHMgZm9yIHRoZSBQcm9ncmVzc0Jhci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVByb3BzIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBwcm9ncmVzcyBwZXJjZW50YWdlLCBmcm9tIDAgdG8gMTAwXG4gICAgICovXG4gICAgcGVyY2VudGFnZTogbnVtYmVyO1xuICB9XG59XG5cbi8qKlxuICogQSBmdW5jdGlvbmFsIHRzeCBjb21wb25lbnQgZm9yIGEgcHJvZ3Jlc3MgYmFyLlxuICovXG5leHBvcnQgZnVuY3Rpb24gUHJvZ3Jlc3NCYXIocHJvcHM6IFByb2dyZXNzQmFyLklQcm9wcykge1xuICByZXR1cm4gKFxuICAgIDxkaXYgY2xhc3NOYW1lPXtwcm9ncmVzc0Jhckl0ZW19PlxuICAgICAgPEZpbGxlciBwZXJjZW50YWdlPXtwcm9wcy5wZXJjZW50YWdlfSAvPlxuICAgIDwvZGl2PlxuICApO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBGaWxsZXIgc3RhdGljcy5cbiAqL1xubmFtZXNwYWNlIEZpbGxlciB7XG4gIC8qKlxuICAgKiBQcm9wcyBmb3IgdGhlIEZpbGxlciBjb21wb25lbnQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wcyB7XG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgcGVyY2VudGFnZSBmaWxsZWQsIGZyb20gMCB0byAxMDBcbiAgICAgKi9cbiAgICBwZXJjZW50YWdlOiBudW1iZXI7XG4gIH1cbn1cblxuLyoqXG4gKiBBIGZ1bmN0aW9uYWwgdHN4IGNvbXBvbmVudCBmb3IgYSBwYXJ0aWFsbHkgZmlsbGVkIGRpdi5cbiAqL1xuZnVuY3Rpb24gRmlsbGVyKHByb3BzOiBGaWxsZXIuSVByb3BzKSB7XG4gIHJldHVybiAoXG4gICAgPGRpdlxuICAgICAgY2xhc3NOYW1lPXtmaWxsZXJJdGVtfVxuICAgICAgc3R5bGU9e3tcbiAgICAgICAgd2lkdGg6IGAke3Byb3BzLnBlcmNlbnRhZ2V9cHhgXG4gICAgICB9fVxuICAgIC8+XG4gICk7XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IGNsYXNzZXMgfSBmcm9tICd0eXBlc3R5bGUvbGliJztcbmltcG9ydCB7IHRleHRJdGVtIH0gZnJvbSAnLi4vc3R5bGUvdGV4dCc7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIFRleHRJdGVtIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgVGV4dEl0ZW0ge1xuICAvKipcbiAgICogUHJvcHMgZm9yIGEgVGV4dEl0ZW0uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wcyB7XG4gICAgLyoqXG4gICAgICogVGhlIGNvbnRlbnQgb2YgdGhlIHRleHQgaXRlbS5cbiAgICAgKi9cbiAgICBzb3VyY2U6IHN0cmluZyB8IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIEhvdmVyIHRleHQgdG8gZ2l2ZSB0byB0aGUgbm9kZS5cbiAgICAgKi9cbiAgICB0aXRsZT86IHN0cmluZztcbiAgfVxufVxuXG4vKipcbiAqIEEgZnVuY3Rpb25hbCB0c3ggY29tcG9uZW50IGZvciBhIHRleHQgaXRlbS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIFRleHRJdGVtKFxuICBwcm9wczogVGV4dEl0ZW0uSVByb3BzICYgUmVhY3QuSFRNTEF0dHJpYnV0ZXM8SFRNTFNwYW5FbGVtZW50PlxuKTogUmVhY3QuUmVhY3RFbGVtZW50PFRleHRJdGVtLklQcm9wcz4ge1xuICBjb25zdCB7IHRpdGxlLCBzb3VyY2UsIGNsYXNzTmFtZSwgLi4ucmVzdCB9ID0gcHJvcHM7XG4gIHJldHVybiAoXG4gICAgPHNwYW4gY2xhc3NOYW1lPXtjbGFzc2VzKHRleHRJdGVtLCBjbGFzc05hbWUpfSB0aXRsZT17dGl0bGV9IHsuLi5yZXN0fT5cbiAgICAgIHtzb3VyY2V9XG4gICAgPC9zcGFuPlxuICApO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5leHBvcnQgKiBmcm9tICcuL2tlcm5lbFN0YXR1cyc7XG5leHBvcnQgKiBmcm9tICcuL2xpbmVDb2wnO1xuZXhwb3J0ICogZnJvbSAnLi9ydW5uaW5nU2Vzc2lvbnMnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJU2Vzc2lvbkNvbnRleHQsIFZEb21Nb2RlbCwgVkRvbVJlbmRlcmVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgU2Vzc2lvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgSlNPTkFycmF5LCBKU09ORXh0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IGludGVyYWN0aXZlSXRlbSwgVGV4dEl0ZW0gfSBmcm9tICcuLic7XG5cbi8qKlxuICogQSBwdXJlIGZ1bmN0aW9uYWwgY29tcG9uZW50IGZvciByZW5kZXJpbmcga2VybmVsIHN0YXR1cy5cbiAqL1xuZnVuY3Rpb24gS2VybmVsU3RhdHVzQ29tcG9uZW50KFxuICBwcm9wczogS2VybmVsU3RhdHVzQ29tcG9uZW50LklQcm9wc1xuKTogUmVhY3QuUmVhY3RFbGVtZW50PEtlcm5lbFN0YXR1c0NvbXBvbmVudC5JUHJvcHM+IHtcbiAgY29uc3QgdHJhbnNsYXRvciA9IHByb3BzLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGxldCBzdGF0dXNUZXh0ID0gJyc7XG4gIGlmIChwcm9wcy5zdGF0dXMpIHtcbiAgICBzdGF0dXNUZXh0ID0gYCB8ICR7cHJvcHMuc3RhdHVzfWA7XG4gIH1cbiAgcmV0dXJuIChcbiAgICA8VGV4dEl0ZW1cbiAgICAgIG9uQ2xpY2s9e3Byb3BzLmhhbmRsZUNsaWNrfVxuICAgICAgc291cmNlPXtgJHtwcm9wcy5rZXJuZWxOYW1lfSR7c3RhdHVzVGV4dH1gfVxuICAgICAgdGl0bGU9e3RyYW5zLl9fKCdDaGFuZ2Uga2VybmVsIGZvciAlMScsIHByb3BzLmFjdGl2aXR5TmFtZSl9XG4gICAgLz5cbiAgKTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgS2VybmVsU3RhdHVzQ29tcG9uZW50IHN0YXRpY3MuXG4gKi9cbm5hbWVzcGFjZSBLZXJuZWxTdGF0dXNDb21wb25lbnQge1xuICAvKipcbiAgICogUHJvcHMgZm9yIHRoZSBrZXJuZWwgc3RhdHVzIGNvbXBvbmVudC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVByb3BzIHtcbiAgICAvKipcbiAgICAgKiBBIGNsaWNrIGhhbmRsZXIgZm9yIHRoZSBrZXJuZWwgc3RhdHVzIGNvbXBvbmVudC4gQnkgZGVmYXVsdFxuICAgICAqIHdlIGhhdmUgaXQgYnJpbmcgdXAgdGhlIGtlcm5lbCBjaGFuZ2UgZGlhbG9nLlxuICAgICAqL1xuICAgIGhhbmRsZUNsaWNrOiAoKSA9PiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG5hbWUgdGhlIGtlcm5lbC5cbiAgICAgKi9cbiAgICBrZXJuZWxOYW1lOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmFtZSBvZiB0aGUgYWN0aXZpdHkgdXNpbmcgdGhlIGtlcm5lbC5cbiAgICAgKi9cbiAgICBhY3Rpdml0eU5hbWU6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBzdGF0dXMgb2YgdGhlIGtlcm5lbC5cbiAgICAgKi9cbiAgICBzdGF0dXM/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cbn1cblxuLyoqXG4gKiBBIFZEb21SZW5kZXJlciB3aWRnZXQgZm9yIGRpc3BsYXlpbmcgdGhlIHN0YXR1cyBvZiBhIGtlcm5lbC5cbiAqL1xuZXhwb3J0IGNsYXNzIEtlcm5lbFN0YXR1cyBleHRlbmRzIFZEb21SZW5kZXJlcjxLZXJuZWxTdGF0dXMuTW9kZWw+IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCB0aGUga2VybmVsIHN0YXR1cyB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRzOiBLZXJuZWxTdGF0dXMuSU9wdGlvbnMsIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcikge1xuICAgIHN1cGVyKG5ldyBLZXJuZWxTdGF0dXMuTW9kZWwodHJhbnNsYXRvcikpO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5faGFuZGxlQ2xpY2sgPSBvcHRzLm9uQ2xpY2s7XG4gICAgdGhpcy5hZGRDbGFzcyhpbnRlcmFjdGl2ZUl0ZW0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciB0aGUga2VybmVsIHN0YXR1cyBpdGVtLlxuICAgKi9cbiAgcmVuZGVyKCkge1xuICAgIGlmICh0aGlzLm1vZGVsID09PSBudWxsKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIChcbiAgICAgICAgPEtlcm5lbFN0YXR1c0NvbXBvbmVudFxuICAgICAgICAgIHN0YXR1cz17dGhpcy5tb2RlbC5zdGF0dXN9XG4gICAgICAgICAga2VybmVsTmFtZT17dGhpcy5tb2RlbC5rZXJuZWxOYW1lfVxuICAgICAgICAgIGFjdGl2aXR5TmFtZT17dGhpcy5tb2RlbC5hY3Rpdml0eU5hbWV9XG4gICAgICAgICAgaGFuZGxlQ2xpY2s9e3RoaXMuX2hhbmRsZUNsaWNrfVxuICAgICAgICAgIHRyYW5zbGF0b3I9e3RoaXMudHJhbnNsYXRvcn1cbiAgICAgICAgLz5cbiAgICAgICk7XG4gICAgfVxuICB9XG5cbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX2hhbmRsZUNsaWNrOiAoKSA9PiB2b2lkO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBLZXJuZWxTdGF0dXMgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBLZXJuZWxTdGF0dXMge1xuICAvKipcbiAgICogQSBWRG9tTW9kZWwgZm9yIHRoZSBrZXJuZWwgc3RhdHVzIGluZGljYXRvci5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBNb2RlbCBleHRlbmRzIFZEb21Nb2RlbCB7XG4gICAgY29uc3RydWN0b3IodHJhbnNsYXRvcj86IElUcmFuc2xhdG9yKSB7XG4gICAgICBzdXBlcigpO1xuICAgICAgdHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgICB0aGlzLl90cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgICAgdGhpcy5fa2VybmVsTmFtZSA9IHRoaXMuX3RyYW5zLl9fKCdObyBLZXJuZWwhJyk7XG4gICAgICAvLyBUT0RPLUZJWE1FOiB0aGlzIG1hcHBpbmcgaXMgZHVwbGljYXRlZCBpbiBhcHB1dGlscy90b29sYmFyLnRzeFxuICAgICAgdGhpcy5fc3RhdHVzTmFtZXMgPSB7XG4gICAgICAgIHVua25vd246IHRoaXMuX3RyYW5zLl9fKCdVbmtub3duJyksXG4gICAgICAgIHN0YXJ0aW5nOiB0aGlzLl90cmFucy5fXygnU3RhcnRpbmcnKSxcbiAgICAgICAgaWRsZTogdGhpcy5fdHJhbnMuX18oJ0lkbGUnKSxcbiAgICAgICAgYnVzeTogdGhpcy5fdHJhbnMuX18oJ0J1c3knKSxcbiAgICAgICAgdGVybWluYXRpbmc6IHRoaXMuX3RyYW5zLl9fKCdUZXJtaW5hdGluZycpLFxuICAgICAgICByZXN0YXJ0aW5nOiB0aGlzLl90cmFucy5fXygnUmVzdGFydGluZycpLFxuICAgICAgICBhdXRvcmVzdGFydGluZzogdGhpcy5fdHJhbnMuX18oJ0F1dG9yZXN0YXJ0aW5nJyksXG4gICAgICAgIGRlYWQ6IHRoaXMuX3RyYW5zLl9fKCdEZWFkJyksXG4gICAgICAgIGNvbm5lY3RlZDogdGhpcy5fdHJhbnMuX18oJ0Nvbm5lY3RlZCcpLFxuICAgICAgICBjb25uZWN0aW5nOiB0aGlzLl90cmFucy5fXygnQ29ubmVjdGluZycpLFxuICAgICAgICBkaXNjb25uZWN0ZWQ6IHRoaXMuX3RyYW5zLl9fKCdEaXNjb25uZWN0ZWQnKSxcbiAgICAgICAgaW5pdGlhbGl6aW5nOiB0aGlzLl90cmFucy5fXygnSW5pdGlhbGl6aW5nJyksXG4gICAgICAgICcnOiAnJ1xuICAgICAgfTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmFtZSBvZiB0aGUga2VybmVsLlxuICAgICAqL1xuICAgIGdldCBrZXJuZWxOYW1lKCkge1xuICAgICAgcmV0dXJuIHRoaXMuX2tlcm5lbE5hbWU7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgc3RhdHVzIG9mIHRoZSBrZXJuZWwuXG4gICAgICovXG4gICAgZ2V0IHN0YXR1cygpIHtcbiAgICAgIHJldHVybiB0aGlzLl9rZXJuZWxTdGF0dXNcbiAgICAgICAgPyB0aGlzLl9zdGF0dXNOYW1lc1t0aGlzLl9rZXJuZWxTdGF0dXNdXG4gICAgICAgIDogdW5kZWZpbmVkO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgZGlzcGxheSBuYW1lIGZvciB0aGUgYWN0aXZpdHkuXG4gICAgICovXG4gICAgZ2V0IGFjdGl2aXR5TmFtZSgpOiBzdHJpbmcge1xuICAgICAgcmV0dXJuIHRoaXMuX2FjdGl2aXR5TmFtZTtcbiAgICB9XG4gICAgc2V0IGFjdGl2aXR5TmFtZSh2YWw6IHN0cmluZykge1xuICAgICAgY29uc3Qgb2xkVmFsID0gdGhpcy5fYWN0aXZpdHlOYW1lO1xuICAgICAgaWYgKG9sZFZhbCA9PT0gdmFsKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHRoaXMuX2FjdGl2aXR5TmFtZSA9IHZhbDtcbiAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBjbGllbnQgc2Vzc2lvbiBhc3NvY2lhdGVkIHdpdGggdGhlIGtlcm5lbCBzdGF0dXMgaW5kaWNhdG9yLlxuICAgICAqL1xuICAgIGdldCBzZXNzaW9uQ29udGV4dCgpOiBJU2Vzc2lvbkNvbnRleHQgfCBudWxsIHtcbiAgICAgIHJldHVybiB0aGlzLl9zZXNzaW9uQ29udGV4dDtcbiAgICB9XG4gICAgc2V0IHNlc3Npb25Db250ZXh0KHNlc3Npb25Db250ZXh0OiBJU2Vzc2lvbkNvbnRleHQgfCBudWxsKSB7XG4gICAgICB0aGlzLl9zZXNzaW9uQ29udGV4dD8uc3RhdHVzQ2hhbmdlZC5kaXNjb25uZWN0KFxuICAgICAgICB0aGlzLl9vbktlcm5lbFN0YXR1c0NoYW5nZWRcbiAgICAgICk7XG4gICAgICB0aGlzLl9zZXNzaW9uQ29udGV4dD8ua2VybmVsQ2hhbmdlZC5kaXNjb25uZWN0KHRoaXMuX29uS2VybmVsQ2hhbmdlZCk7XG5cbiAgICAgIGNvbnN0IG9sZFN0YXRlID0gdGhpcy5fZ2V0QWxsU3RhdGUoKTtcbiAgICAgIHRoaXMuX3Nlc3Npb25Db250ZXh0ID0gc2Vzc2lvbkNvbnRleHQ7XG4gICAgICB0aGlzLl9rZXJuZWxTdGF0dXMgPSBzZXNzaW9uQ29udGV4dD8ua2VybmVsRGlzcGxheVN0YXR1cztcbiAgICAgIHRoaXMuX2tlcm5lbE5hbWUgPVxuICAgICAgICBzZXNzaW9uQ29udGV4dD8ua2VybmVsRGlzcGxheU5hbWUgPz8gdGhpcy5fdHJhbnMuX18oJ05vIEtlcm5lbCcpO1xuICAgICAgc2Vzc2lvbkNvbnRleHQ/LnN0YXR1c0NoYW5nZWQuY29ubmVjdCh0aGlzLl9vbktlcm5lbFN0YXR1c0NoYW5nZWQsIHRoaXMpO1xuICAgICAgc2Vzc2lvbkNvbnRleHQ/LmNvbm5lY3Rpb25TdGF0dXNDaGFuZ2VkLmNvbm5lY3QoXG4gICAgICAgIHRoaXMuX29uS2VybmVsU3RhdHVzQ2hhbmdlZCxcbiAgICAgICAgdGhpc1xuICAgICAgKTtcbiAgICAgIHNlc3Npb25Db250ZXh0Py5rZXJuZWxDaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25LZXJuZWxDaGFuZ2VkLCB0aGlzKTtcbiAgICAgIHRoaXMuX3RyaWdnZXJDaGFuZ2Uob2xkU3RhdGUsIHRoaXMuX2dldEFsbFN0YXRlKCkpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlYWN0IHRvIGNoYW5nZXMgdG8gdGhlIGtlcm5lbCBzdGF0dXMuXG4gICAgICovXG4gICAgcHJpdmF0ZSBfb25LZXJuZWxTdGF0dXNDaGFuZ2VkID0gKCkgPT4ge1xuICAgICAgdGhpcy5fa2VybmVsU3RhdHVzID0gdGhpcy5fc2Vzc2lvbkNvbnRleHQ/Lmtlcm5lbERpc3BsYXlTdGF0dXM7XG4gICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gICAgfTtcblxuICAgIC8qKlxuICAgICAqIFJlYWN0IHRvIGNoYW5nZXMgaW4gdGhlIGtlcm5lbC5cbiAgICAgKi9cbiAgICBwcml2YXRlIF9vbktlcm5lbENoYW5nZWQgPSAoXG4gICAgICBfc2Vzc2lvbkNvbnRleHQ6IElTZXNzaW9uQ29udGV4dCxcbiAgICAgIGNoYW5nZTogU2Vzc2lvbi5JU2Vzc2lvbkNvbm5lY3Rpb24uSUtlcm5lbENoYW5nZWRBcmdzXG4gICAgKSA9PiB7XG4gICAgICBjb25zdCBvbGRTdGF0ZSA9IHRoaXMuX2dldEFsbFN0YXRlKCk7XG5cbiAgICAgIC8vIHN5bmMgc2V0dGluZyBvZiBzdGF0dXMgYW5kIGRpc3BsYXkgbmFtZVxuICAgICAgdGhpcy5fa2VybmVsU3RhdHVzID0gdGhpcy5fc2Vzc2lvbkNvbnRleHQ/Lmtlcm5lbERpc3BsYXlTdGF0dXM7XG4gICAgICB0aGlzLl9rZXJuZWxOYW1lID0gX3Nlc3Npb25Db250ZXh0Lmtlcm5lbERpc3BsYXlOYW1lO1xuICAgICAgdGhpcy5fdHJpZ2dlckNoYW5nZShvbGRTdGF0ZSwgdGhpcy5fZ2V0QWxsU3RhdGUoKSk7XG4gICAgfTtcblxuICAgIHByaXZhdGUgX2dldEFsbFN0YXRlKCk6IFByaXZhdGUuU3RhdGUge1xuICAgICAgcmV0dXJuIFt0aGlzLl9rZXJuZWxOYW1lLCB0aGlzLl9rZXJuZWxTdGF0dXMsIHRoaXMuX2FjdGl2aXR5TmFtZV07XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfdHJpZ2dlckNoYW5nZShvbGRTdGF0ZTogUHJpdmF0ZS5TdGF0ZSwgbmV3U3RhdGU6IFByaXZhdGUuU3RhdGUpIHtcbiAgICAgIGlmIChKU09ORXh0LmRlZXBFcXVhbChvbGRTdGF0ZSBhcyBKU09OQXJyYXksIG5ld1N0YXRlIGFzIEpTT05BcnJheSkpIHtcbiAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgfVxuICAgIH1cblxuICAgIHByb3RlY3RlZCB0cmFuc2xhdGlvbjogSVRyYW5zbGF0b3I7XG4gICAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICAgIHByaXZhdGUgX2FjdGl2aXR5TmFtZTogc3RyaW5nID0gJ2FjdGl2aXR5JzsgLy8gRklYTUUtVFJBTlM6P1xuICAgIHByaXZhdGUgX2tlcm5lbE5hbWU6IHN0cmluZzsgLy8gSW5pdGlhbGl6ZWQgaW4gY29uc3RydWN0b3IgZHVlIHRvIGxvY2FsaXphdGlvblxuICAgIHByaXZhdGUgX2tlcm5lbFN0YXR1czogSVNlc3Npb25Db250ZXh0Lktlcm5lbERpc3BsYXlTdGF0dXMgfCB1bmRlZmluZWQgPSAnJztcbiAgICBwcml2YXRlIF9zZXNzaW9uQ29udGV4dDogSVNlc3Npb25Db250ZXh0IHwgbnVsbCA9IG51bGw7XG4gICAgcHJpdmF0ZSByZWFkb25seSBfc3RhdHVzTmFtZXM6IFJlY29yZDxcbiAgICAgIElTZXNzaW9uQ29udGV4dC5LZXJuZWxEaXNwbGF5U3RhdHVzLFxuICAgICAgc3RyaW5nXG4gICAgPjtcbiAgfVxuXG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBjcmVhdGluZyBhIEtlcm5lbFN0YXR1cyBvYmplY3QuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBBIGNsaWNrIGhhbmRsZXIgZm9yIHRoZSBpdGVtLiBCeSBkZWZhdWx0XG4gICAgICogd2UgbGF1bmNoIGEga2VybmVsIHNlbGVjdGlvbiBkaWFsb2cuXG4gICAgICovXG4gICAgb25DbGljazogKCkgPT4gdm9pZDtcbiAgfVxufVxuXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIGV4cG9ydCB0eXBlIFN0YXRlID0gW3N0cmluZywgc3RyaW5nIHwgdW5kZWZpbmVkLCBzdHJpbmddO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBSZWFjdFdpZGdldCwgVkRvbU1vZGVsLCBWRG9tUmVuZGVyZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IGxpbmVGb3JtSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IGNsYXNzZXMgfSBmcm9tICd0eXBlc3R5bGUvbGliJztcbmltcG9ydCB7IGludGVyYWN0aXZlSXRlbSwgUG9wdXAsIHNob3dQb3B1cCwgVGV4dEl0ZW0gfSBmcm9tICcuLic7XG5pbXBvcnQge1xuICBsaW5lRm9ybUJ1dHRvbixcbiAgbGluZUZvcm1CdXR0b25EaXYsXG4gIGxpbmVGb3JtQnV0dG9uSWNvbixcbiAgbGluZUZvcm1DYXB0aW9uLFxuICBsaW5lRm9ybUlucHV0LFxuICBsaW5lRm9ybVNlYXJjaCxcbiAgbGluZUZvcm1XcmFwcGVyLFxuICBsaW5lRm9ybVdyYXBwZXJGb2N1c1dpdGhpblxufSBmcm9tICcuLi9zdHlsZS9saW5lRm9ybSc7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIExpbmVGb3JtQ29tcG9uZW50IHN0YXRpY3MuXG4gKi9cbm5hbWVzcGFjZSBMaW5lRm9ybUNvbXBvbmVudCB7XG4gIC8qKlxuICAgKiBUaGUgcHJvcHMgZm9yIExpbmVGb3JtQ29tcG9uZW50LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIEEgY2FsbGJhY2sgZm9yIHdoZW4gdGhlIGZvcm0gaXMgc3VibWl0dGVkLlxuICAgICAqL1xuICAgIGhhbmRsZVN1Ym1pdDogKHZhbHVlOiBudW1iZXIpID0+IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBsaW5lIG9mIHRoZSBmb3JtLlxuICAgICAqL1xuICAgIGN1cnJlbnRMaW5lOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbWF4aW11bSBsaW5lIHRoZSBmb3JtIGNhbiB0YWtlICh0eXBpY2FsbHkgdGhlXG4gICAgICogbWF4aW11bSBsaW5lIG9mIHRoZSByZWxldmFudCBlZGl0b3IpLlxuICAgICAqL1xuICAgIG1heExpbmU6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBhcHBsaWNhdGlvbiBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgcHJvcHMgZm9yIExpbmVGb3JtQ29tcG9uZW50LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJU3RhdGUge1xuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IHZhbHVlIG9mIHRoZSBmb3JtLlxuICAgICAqL1xuICAgIHZhbHVlOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBmb3JtIGhhcyBmb2N1cy5cbiAgICAgKi9cbiAgICBoYXNGb2N1czogYm9vbGVhbjtcbiAgfVxufVxuXG4vKipcbiAqIEEgY29tcG9uZW50IGZvciByZW5kZXJpbmcgYSBcImdvLXRvLWxpbmVcIiBmb3JtLlxuICovXG5jbGFzcyBMaW5lRm9ybUNvbXBvbmVudCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudDxcbiAgTGluZUZvcm1Db21wb25lbnQuSVByb3BzLFxuICBMaW5lRm9ybUNvbXBvbmVudC5JU3RhdGVcbj4ge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IExpbmVGb3JtQ29tcG9uZW50LlxuICAgKi9cbiAgY29uc3RydWN0b3IocHJvcHM6IExpbmVGb3JtQ29tcG9uZW50LklQcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBwcm9wcy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX3RyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgdmFsdWU6ICcnLFxuICAgICAgaGFzRm9jdXM6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBGb2N1cyB0aGUgZWxlbWVudCBvbiBtb3VudC5cbiAgICovXG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIHRoaXMuX3RleHRJbnB1dCEuZm9jdXMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgdGhlIExpbmVGb3JtQ29tcG9uZW50LlxuICAgKi9cbiAgcmVuZGVyKCkge1xuICAgIHJldHVybiAoXG4gICAgICA8ZGl2IGNsYXNzTmFtZT17bGluZUZvcm1TZWFyY2h9PlxuICAgICAgICA8Zm9ybSBuYW1lPVwibGluZUNvbHVtbkZvcm1cIiBvblN1Ym1pdD17dGhpcy5faGFuZGxlU3VibWl0fSBub1ZhbGlkYXRlPlxuICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgIGNsYXNzTmFtZT17Y2xhc3NlcyhcbiAgICAgICAgICAgICAgbGluZUZvcm1XcmFwcGVyLFxuICAgICAgICAgICAgICAnbG0tbGluZUZvcm0td3JhcHBlcicsXG4gICAgICAgICAgICAgIHRoaXMuc3RhdGUuaGFzRm9jdXMgPyBsaW5lRm9ybVdyYXBwZXJGb2N1c1dpdGhpbiA6IHVuZGVmaW5lZFxuICAgICAgICAgICAgKX1cbiAgICAgICAgICA+XG4gICAgICAgICAgICA8aW5wdXRcbiAgICAgICAgICAgICAgdHlwZT1cInRleHRcIlxuICAgICAgICAgICAgICBjbGFzc05hbWU9e2xpbmVGb3JtSW5wdXR9XG4gICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLl9oYW5kbGVDaGFuZ2V9XG4gICAgICAgICAgICAgIG9uRm9jdXM9e3RoaXMuX2hhbmRsZUZvY3VzfVxuICAgICAgICAgICAgICBvbkJsdXI9e3RoaXMuX2hhbmRsZUJsdXJ9XG4gICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnZhbHVlfVxuICAgICAgICAgICAgICByZWY9e2lucHV0ID0+IHtcbiAgICAgICAgICAgICAgICB0aGlzLl90ZXh0SW5wdXQgPSBpbnB1dDtcbiAgICAgICAgICAgICAgfX1cbiAgICAgICAgICAgIC8+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT17bGluZUZvcm1CdXR0b25EaXZ9PlxuICAgICAgICAgICAgICA8bGluZUZvcm1JY29uLnJlYWN0XG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lPXtsaW5lRm9ybUJ1dHRvbkljb259XG4gICAgICAgICAgICAgICAgZWxlbWVudFBvc2l0aW9uPVwiY2VudGVyXCJcbiAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJzdWJtaXRcIiBjbGFzc05hbWU9e2xpbmVGb3JtQnV0dG9ufSB2YWx1ZT1cIlwiIC8+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8bGFiZWwgY2xhc3NOYW1lPXtsaW5lRm9ybUNhcHRpb259PlxuICAgICAgICAgICAge3RoaXMuX3RyYW5zLl9fKFxuICAgICAgICAgICAgICAnR28gdG8gbGluZSBudW1iZXIgYmV0d2VlbiAxIGFuZCAlMScsXG4gICAgICAgICAgICAgIHRoaXMucHJvcHMubWF4TGluZVxuICAgICAgICAgICAgKX1cbiAgICAgICAgICA8L2xhYmVsPlxuICAgICAgICA8L2Zvcm0+XG4gICAgICA8L2Rpdj5cbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgdmFsdWUgaW4gdGhlIGlucHV0IGZpZWxkLlxuICAgKi9cbiAgcHJpdmF0ZSBfaGFuZGxlQ2hhbmdlID0gKGV2ZW50OiBSZWFjdC5DaGFuZ2VFdmVudDxIVE1MSW5wdXRFbGVtZW50PikgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoeyB2YWx1ZTogZXZlbnQuY3VycmVudFRhcmdldC52YWx1ZSB9KTtcbiAgfTtcblxuICAvKipcbiAgICogSGFuZGxlIHN1Ym1pc3Npb24gb2YgdGhlIGlucHV0IGZpZWxkLlxuICAgKi9cbiAgcHJpdmF0ZSBfaGFuZGxlU3VibWl0ID0gKGV2ZW50OiBSZWFjdC5Gb3JtRXZlbnQ8SFRNTEZvcm1FbGVtZW50PikgPT4ge1xuICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG5cbiAgICBjb25zdCB2YWx1ZSA9IHBhcnNlSW50KHRoaXMuX3RleHRJbnB1dCEudmFsdWUsIDEwKTtcbiAgICBpZiAoXG4gICAgICAhaXNOYU4odmFsdWUpICYmXG4gICAgICBpc0Zpbml0ZSh2YWx1ZSkgJiZcbiAgICAgIDEgPD0gdmFsdWUgJiZcbiAgICAgIHZhbHVlIDw9IHRoaXMucHJvcHMubWF4TGluZVxuICAgICkge1xuICAgICAgdGhpcy5wcm9wcy5oYW5kbGVTdWJtaXQodmFsdWUpO1xuICAgIH1cblxuICAgIHJldHVybiBmYWxzZTtcbiAgfTtcblxuICAvKipcbiAgICogSGFuZGxlIGZvY3VzaW5nIG9mIHRoZSBpbnB1dCBmaWVsZC5cbiAgICovXG4gIHByaXZhdGUgX2hhbmRsZUZvY3VzID0gKCkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoeyBoYXNGb2N1czogdHJ1ZSB9KTtcbiAgfTtcblxuICAvKipcbiAgICogSGFuZGxlIGJsdXJyaW5nIG9mIHRoZSBpbnB1dCBmaWVsZC5cbiAgICovXG4gIHByaXZhdGUgX2hhbmRsZUJsdXIgPSAoKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7IGhhc0ZvY3VzOiBmYWxzZSB9KTtcbiAgfTtcblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfdGV4dElucHV0OiBIVE1MSW5wdXRFbGVtZW50IHwgbnVsbCA9IG51bGw7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIExpbmVDb2xDb21wb25lbnQuXG4gKi9cbm5hbWVzcGFjZSBMaW5lQ29sQ29tcG9uZW50IHtcbiAgLyoqXG4gICAqIFByb3BzIGZvciBMaW5lQ29sQ29tcG9uZW50LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IGxpbmUgbnVtYmVyLlxuICAgICAqL1xuICAgIGxpbmU6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IGNvbHVtbiBudW1iZXIuXG4gICAgICovXG4gICAgY29sdW1uOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG5cbiAgICAvKipcbiAgICAgKiBBIGNsaWNrIGhhbmRsZXIgZm9yIHRoZSBMaW5lQ29sQ29tcG9uZW50LCB3aGljaFxuICAgICAqIHdlIHVzZSB0byBsYXVuY2ggdGhlIExpbmVGb3JtQ29tcG9uZW50LlxuICAgICAqL1xuICAgIGhhbmRsZUNsaWNrOiAoKSA9PiB2b2lkO1xuICB9XG59XG5cbi8qKlxuICogQSBwdXJlIGZ1bmN0aW9uYWwgY29tcG9uZW50IGZvciByZW5kZXJpbmcgYSBsaW5lL2NvbHVtblxuICogc3RhdHVzIGl0ZW0uXG4gKi9cbmZ1bmN0aW9uIExpbmVDb2xDb21wb25lbnQoXG4gIHByb3BzOiBMaW5lQ29sQ29tcG9uZW50LklQcm9wc1xuKTogUmVhY3QuUmVhY3RFbGVtZW50PExpbmVDb2xDb21wb25lbnQuSVByb3BzPiB7XG4gIGNvbnN0IHRyYW5zbGF0b3IgPSBwcm9wcy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICByZXR1cm4gKFxuICAgIDxUZXh0SXRlbVxuICAgICAgb25DbGljaz17cHJvcHMuaGFuZGxlQ2xpY2t9XG4gICAgICBzb3VyY2U9e3RyYW5zLl9fKCdMbiAlMSwgQ29sICUyJywgcHJvcHMubGluZSwgcHJvcHMuY29sdW1uKX1cbiAgICAgIHRpdGxlPXt0cmFucy5fXygnR28gdG8gbGluZSBudW1iZXLigKYnKX1cbiAgICAvPlxuICApO1xufVxuXG4vKipcbiAqIEEgd2lkZ2V0IGltcGxlbWVudGluZyBhIGxpbmUvY29sdW1uIHN0YXR1cyBpdGVtLlxuICovXG5leHBvcnQgY2xhc3MgTGluZUNvbCBleHRlbmRzIFZEb21SZW5kZXJlcjxMaW5lQ29sLk1vZGVsPiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgTGluZUNvbCBzdGF0dXMgaXRlbS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcikge1xuICAgIHN1cGVyKG5ldyBMaW5lQ29sLk1vZGVsKCkpO1xuICAgIHRoaXMuYWRkQ2xhc3MoaW50ZXJhY3RpdmVJdGVtKTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciB0aGUgc3RhdHVzIGl0ZW0uXG4gICAqL1xuICByZW5kZXIoKTogUmVhY3QuUmVhY3RFbGVtZW50PExpbmVDb2xDb21wb25lbnQuSVByb3BzPiB8IG51bGwge1xuICAgIGlmICh0aGlzLm1vZGVsID09PSBudWxsKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIChcbiAgICAgICAgPExpbmVDb2xDb21wb25lbnRcbiAgICAgICAgICBsaW5lPXt0aGlzLm1vZGVsLmxpbmV9XG4gICAgICAgICAgY29sdW1uPXt0aGlzLm1vZGVsLmNvbHVtbn1cbiAgICAgICAgICB0cmFuc2xhdG9yPXt0aGlzLnRyYW5zbGF0b3J9XG4gICAgICAgICAgaGFuZGxlQ2xpY2s9eygpID0+IHRoaXMuX2hhbmRsZUNsaWNrKCl9XG4gICAgICAgIC8+XG4gICAgICApO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBIGNsaWNrIGhhbmRsZXIgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9oYW5kbGVDbGljaygpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fcG9wdXApIHtcbiAgICAgIHRoaXMuX3BvcHVwLmRpc3Bvc2UoKTtcbiAgICB9XG4gICAgY29uc3QgYm9keSA9IFJlYWN0V2lkZ2V0LmNyZWF0ZShcbiAgICAgIDxMaW5lRm9ybUNvbXBvbmVudFxuICAgICAgICBoYW5kbGVTdWJtaXQ9e3ZhbCA9PiB0aGlzLl9oYW5kbGVTdWJtaXQodmFsKX1cbiAgICAgICAgY3VycmVudExpbmU9e3RoaXMubW9kZWwhLmxpbmV9XG4gICAgICAgIG1heExpbmU9e3RoaXMubW9kZWwhLmVkaXRvciEubGluZUNvdW50fVxuICAgICAgICB0cmFuc2xhdG9yPXt0aGlzLnRyYW5zbGF0b3J9XG4gICAgICAvPlxuICAgICk7XG5cbiAgICB0aGlzLl9wb3B1cCA9IHNob3dQb3B1cCh7XG4gICAgICBib2R5OiBib2R5LFxuICAgICAgYW5jaG9yOiB0aGlzLFxuICAgICAgYWxpZ246ICdyaWdodCdcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgc3VibWlzc2lvbiBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByaXZhdGUgX2hhbmRsZVN1Ym1pdCh2YWx1ZTogbnVtYmVyKTogdm9pZCB7XG4gICAgdGhpcy5tb2RlbCEuZWRpdG9yIS5zZXRDdXJzb3JQb3NpdGlvbih7IGxpbmU6IHZhbHVlIC0gMSwgY29sdW1uOiAwIH0pO1xuICAgIHRoaXMuX3BvcHVwIS5kaXNwb3NlKCk7XG4gICAgdGhpcy5tb2RlbCEuZWRpdG9yIS5mb2N1cygpO1xuICB9XG5cbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF9wb3B1cDogUG9wdXAgfCBudWxsID0gbnVsbDtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgTGluZUNvbCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIExpbmVDb2wge1xuICAvKipcbiAgICogQSBWRG9tIG1vZGVsIGZvciBhIHN0YXR1cyBpdGVtIHRyYWNraW5nIHRoZSBsaW5lL2NvbHVtbiBvZiBhbiBlZGl0b3IuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgTW9kZWwgZXh0ZW5kcyBWRG9tTW9kZWwge1xuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IGVkaXRvciBvZiB0aGUgbW9kZWwuXG4gICAgICovXG4gICAgZ2V0IGVkaXRvcigpOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsIHtcbiAgICAgIHJldHVybiB0aGlzLl9lZGl0b3I7XG4gICAgfVxuICAgIHNldCBlZGl0b3IoZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsKSB7XG4gICAgICBjb25zdCBvbGRFZGl0b3IgPSB0aGlzLl9lZGl0b3I7XG4gICAgICBpZiAob2xkRWRpdG9yKSB7XG4gICAgICAgIG9sZEVkaXRvci5tb2RlbC5zZWxlY3Rpb25zLmNoYW5nZWQuZGlzY29ubmVjdCh0aGlzLl9vblNlbGVjdGlvbkNoYW5nZWQpO1xuICAgICAgfVxuXG4gICAgICBjb25zdCBvbGRTdGF0ZSA9IHRoaXMuX2dldEFsbFN0YXRlKCk7XG4gICAgICB0aGlzLl9lZGl0b3IgPSBlZGl0b3I7XG4gICAgICBpZiAoIXRoaXMuX2VkaXRvcikge1xuICAgICAgICB0aGlzLl9jb2x1bW4gPSAxO1xuICAgICAgICB0aGlzLl9saW5lID0gMTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuX2VkaXRvci5tb2RlbC5zZWxlY3Rpb25zLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vblNlbGVjdGlvbkNoYW5nZWQpO1xuXG4gICAgICAgIGNvbnN0IHBvcyA9IHRoaXMuX2VkaXRvci5nZXRDdXJzb3JQb3NpdGlvbigpO1xuICAgICAgICB0aGlzLl9jb2x1bW4gPSBwb3MuY29sdW1uICsgMTtcbiAgICAgICAgdGhpcy5fbGluZSA9IHBvcy5saW5lICsgMTtcbiAgICAgIH1cblxuICAgICAgdGhpcy5fdHJpZ2dlckNoYW5nZShvbGRTdGF0ZSwgdGhpcy5fZ2V0QWxsU3RhdGUoKSk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgbGluZSBvZiB0aGUgbW9kZWwuXG4gICAgICovXG4gICAgZ2V0IGxpbmUoKTogbnVtYmVyIHtcbiAgICAgIHJldHVybiB0aGlzLl9saW5lO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IGNvbHVtbiBvZiB0aGUgbW9kZWwuXG4gICAgICovXG4gICAgZ2V0IGNvbHVtbigpOiBudW1iZXIge1xuICAgICAgcmV0dXJuIHRoaXMuX2NvbHVtbjtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZWFjdCB0byBhIGNoYW5nZSBpbiB0aGUgY3Vyc29ycyBvZiB0aGUgY3VycmVudCBlZGl0b3IuXG4gICAgICovXG4gICAgcHJpdmF0ZSBfb25TZWxlY3Rpb25DaGFuZ2VkID0gKCkgPT4ge1xuICAgICAgY29uc3Qgb2xkU3RhdGUgPSB0aGlzLl9nZXRBbGxTdGF0ZSgpO1xuICAgICAgY29uc3QgcG9zID0gdGhpcy5lZGl0b3IhLmdldEN1cnNvclBvc2l0aW9uKCk7XG4gICAgICB0aGlzLl9saW5lID0gcG9zLmxpbmUgKyAxO1xuICAgICAgdGhpcy5fY29sdW1uID0gcG9zLmNvbHVtbiArIDE7XG5cbiAgICAgIHRoaXMuX3RyaWdnZXJDaGFuZ2Uob2xkU3RhdGUsIHRoaXMuX2dldEFsbFN0YXRlKCkpO1xuICAgIH07XG5cbiAgICBwcml2YXRlIF9nZXRBbGxTdGF0ZSgpOiBbbnVtYmVyLCBudW1iZXJdIHtcbiAgICAgIHJldHVybiBbdGhpcy5fbGluZSwgdGhpcy5fY29sdW1uXTtcbiAgICB9XG5cbiAgICBwcml2YXRlIF90cmlnZ2VyQ2hhbmdlKFxuICAgICAgb2xkU3RhdGU6IFtudW1iZXIsIG51bWJlcl0sXG4gICAgICBuZXdTdGF0ZTogW251bWJlciwgbnVtYmVyXVxuICAgICkge1xuICAgICAgaWYgKG9sZFN0YXRlWzBdICE9PSBuZXdTdGF0ZVswXSB8fCBvbGRTdGF0ZVsxXSAhPT0gbmV3U3RhdGVbMV0pIHtcbiAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgfVxuICAgIH1cblxuICAgIHByaXZhdGUgX2xpbmU6IG51bWJlciA9IDE7XG4gICAgcHJpdmF0ZSBfY29sdW1uOiBudW1iZXIgPSAxO1xuICAgIHByaXZhdGUgX2VkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yIHwgbnVsbCA9IG51bGw7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgVkRvbU1vZGVsLCBWRG9tUmVuZGVyZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQge1xuICBTZXJ2aWNlTWFuYWdlcixcbiAgU2Vzc2lvbixcbiAgU2Vzc2lvbk1hbmFnZXIsXG4gIFRlcm1pbmFsLFxuICBUZXJtaW5hbE1hbmFnZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIG51bGxUcmFuc2xhdG9yLFxuICBUcmFuc2xhdGlvbkJ1bmRsZVxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBrZXJuZWxJY29uLCB0ZXJtaW5hbEljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBHcm91cEl0ZW0sIGludGVyYWN0aXZlSXRlbSwgVGV4dEl0ZW0gfSBmcm9tICcuLic7XG5cbi8qKlxuICogSGFsZiBzcGFjaW5nIGJldHdlZW4gc3ViaXRlbXMgaW4gYSBzdGF0dXMgaXRlbS5cbiAqL1xuY29uc3QgSEFMRl9TUEFDSU5HID0gNDtcblxuLyoqXG4gKiBBIHB1cmUgZnVuY3Rpb25hbCBjb21wb25lbnQgZm9yIHJlbmRlcmluZyBrZXJuZWwgYW5kIHRlcm1pbmFsIHNlc3Npb25zLlxuICpcbiAqIEBwYXJhbSBwcm9wczogdGhlIHByb3BzIGZvciB0aGUgY29tcG9uZW50LlxuICpcbiAqIEByZXR1cm5zIGEgdHN4IGNvbXBvbmVudCBmb3IgdGhlIHJ1bm5pbmcgc2Vzc2lvbnMuXG4gKi9cbmZ1bmN0aW9uIFJ1bm5pbmdTZXNzaW9uc0NvbXBvbmVudChcbiAgcHJvcHM6IFJ1bm5pbmdTZXNzaW9uc0NvbXBvbmVudC5JUHJvcHNcbik6IFJlYWN0LlJlYWN0RWxlbWVudDxSdW5uaW5nU2Vzc2lvbnNDb21wb25lbnQuSVByb3BzPiB7XG4gIHJldHVybiAoXG4gICAgPEdyb3VwSXRlbSBzcGFjaW5nPXtIQUxGX1NQQUNJTkd9IG9uQ2xpY2s9e3Byb3BzLmhhbmRsZUNsaWNrfT5cbiAgICAgIDxHcm91cEl0ZW0gc3BhY2luZz17SEFMRl9TUEFDSU5HfT5cbiAgICAgICAgPFRleHRJdGVtIHNvdXJjZT17cHJvcHMudGVybWluYWxzfSAvPlxuICAgICAgICA8dGVybWluYWxJY29uLnJlYWN0IGxlZnQ9eycxcHgnfSB0b3A9eyczcHgnfSBzdHlsZXNoZWV0PXsnc3RhdHVzQmFyJ30gLz5cbiAgICAgIDwvR3JvdXBJdGVtPlxuICAgICAgPEdyb3VwSXRlbSBzcGFjaW5nPXtIQUxGX1NQQUNJTkd9PlxuICAgICAgICA8VGV4dEl0ZW0gc291cmNlPXtwcm9wcy5zZXNzaW9uc30gLz5cbiAgICAgICAgPGtlcm5lbEljb24ucmVhY3QgdG9wPXsnMnB4J30gc3R5bGVzaGVldD17J3N0YXR1c0Jhcid9IC8+XG4gICAgICA8L0dyb3VwSXRlbT5cbiAgICA8L0dyb3VwSXRlbT5cbiAgKTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgUnVubmluZ1Nlc3Npb25zQ29tcG9uZW50cyBzdGF0aWNzLlxuICovXG5uYW1lc3BhY2UgUnVubmluZ1Nlc3Npb25zQ29tcG9uZW50IHtcbiAgLyoqXG4gICAqIFRoZSBwcm9wcyBmb3IgcmVuZGVyaW5nIHRoZSBSdW5uaW5nU2Vzc2lvbnNDb21wb25lbnQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wcyB7XG4gICAgLyoqXG4gICAgICogQSBjbGljayBoYW5kbGVyIGZvciB0aGUgY29tcG9uZW50LiBCeSBkZWZhdWx0IHRoaXMgaXMgdXNlZFxuICAgICAqIHRvIGFjdGl2YXRlIHRoZSBydW5uaW5nIHNlc3Npb25zIHNpZGUgcGFuZWwuXG4gICAgICovXG4gICAgaGFuZGxlQ2xpY2s6ICgpID0+IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbnVtYmVyIG9mIHJ1bm5pbmcga2VybmVsIHNlc3Npb25zLlxuICAgICAqL1xuICAgIHNlc3Npb25zOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbnVtYmVyIG9mIGFjdGl2ZSB0ZXJtaW5hbCBzZXNzaW9ucy5cbiAgICAgKi9cbiAgICB0ZXJtaW5hbHM6IG51bWJlcjtcbiAgfVxufVxuXG4vKipcbiAqIEEgVkRvbVJlbmRlcmVyIGZvciBhIFJ1bm5pbmdTZXNzaW9ucyBzdGF0dXMgaXRlbS5cbiAqL1xuZXhwb3J0IGNsYXNzIFJ1bm5pbmdTZXNzaW9ucyBleHRlbmRzIFZEb21SZW5kZXJlcjxSdW5uaW5nU2Vzc2lvbnMuTW9kZWw+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBSdW5uaW5nU2Vzc2lvbnMgd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0czogUnVubmluZ1Nlc3Npb25zLklPcHRpb25zKSB7XG4gICAgc3VwZXIobmV3IFJ1bm5pbmdTZXNzaW9ucy5Nb2RlbCgpKTtcbiAgICB0aGlzLl9zZXJ2aWNlTWFuYWdlciA9IG9wdHMuc2VydmljZU1hbmFnZXI7XG4gICAgdGhpcy5faGFuZGxlQ2xpY2sgPSBvcHRzLm9uQ2xpY2s7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gb3B0cy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX3RyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsb2FkJyk7XG5cbiAgICB0aGlzLl9zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucy5ydW5uaW5nQ2hhbmdlZC5jb25uZWN0KFxuICAgICAgdGhpcy5fb25TZXNzaW9uc1J1bm5pbmdDaGFuZ2VkLFxuICAgICAgdGhpc1xuICAgICk7XG4gICAgdGhpcy5fc2VydmljZU1hbmFnZXIudGVybWluYWxzLnJ1bm5pbmdDaGFuZ2VkLmNvbm5lY3QoXG4gICAgICB0aGlzLl9vblRlcm1pbmFsc1J1bm5pbmdDaGFuZ2VkLFxuICAgICAgdGhpc1xuICAgICk7XG5cbiAgICB0aGlzLmFkZENsYXNzKGludGVyYWN0aXZlSXRlbSk7XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIHRoZSBydW5uaW5nIHNlc3Npb25zIHdpZGdldC5cbiAgICovXG4gIHJlbmRlcigpIHtcbiAgICBpZiAoIXRoaXMubW9kZWwpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICAvLyBUT0RPLVRSQU5TOiBTaG91bGQgcHJvYmFibHkgYmUgaGFuZGxlZCBkaWZmZXJlbnRseS5cbiAgICAvLyBUaGlzIGlzIG1vcmUgbG9jYWxpemFibGUgZnJpZW5kbHk6IFwiVGVybWluYWxzOiAlMSB8IEtlcm5lbHM6ICUyXCJcbiAgICB0aGlzLnRpdGxlLmNhcHRpb24gPSB0aGlzLl90cmFucy5fXyhcbiAgICAgICclMSBUZXJtaW5hbHMsICUyIEtlcm5lbCBzZXNzaW9ucycsXG4gICAgICB0aGlzLm1vZGVsLnRlcm1pbmFscyxcbiAgICAgIHRoaXMubW9kZWwhLnNlc3Npb25zXG4gICAgKTtcbiAgICByZXR1cm4gKFxuICAgICAgPFJ1bm5pbmdTZXNzaW9uc0NvbXBvbmVudFxuICAgICAgICBzZXNzaW9ucz17dGhpcy5tb2RlbC5zZXNzaW9uc31cbiAgICAgICAgdGVybWluYWxzPXt0aGlzLm1vZGVsLnRlcm1pbmFsc31cbiAgICAgICAgaGFuZGxlQ2xpY2s9e3RoaXMuX2hhbmRsZUNsaWNrfVxuICAgICAgLz5cbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHN0YXR1cyBpdGVtLlxuICAgKi9cbiAgZGlzcG9zZSgpIHtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG5cbiAgICB0aGlzLl9zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucy5ydW5uaW5nQ2hhbmdlZC5kaXNjb25uZWN0KFxuICAgICAgdGhpcy5fb25TZXNzaW9uc1J1bm5pbmdDaGFuZ2VkLFxuICAgICAgdGhpc1xuICAgICk7XG4gICAgdGhpcy5fc2VydmljZU1hbmFnZXIudGVybWluYWxzLnJ1bm5pbmdDaGFuZ2VkLmRpc2Nvbm5lY3QoXG4gICAgICB0aGlzLl9vblRlcm1pbmFsc1J1bm5pbmdDaGFuZ2VkLFxuICAgICAgdGhpc1xuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBudW1iZXIgb2Yga2VybmVsIHNlc3Npb25zIHdoZW4gdGhlIGxpc3QgY2hhbmdlcy5cbiAgICovXG4gIHByaXZhdGUgX29uU2Vzc2lvbnNSdW5uaW5nQ2hhbmdlZChcbiAgICBtYW5hZ2VyOiBTZXNzaW9uTWFuYWdlcixcbiAgICBzZXNzaW9uczogU2Vzc2lvbi5JTW9kZWxbXVxuICApOiB2b2lkIHtcbiAgICB0aGlzLm1vZGVsIS5zZXNzaW9ucyA9IHNlc3Npb25zLmxlbmd0aDtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIG51bWJlciBvZiB0ZXJtaW5hbCBzZXNzaW9ucyB3aGVuIHRoZSBsaXN0IGNoYW5nZXMuXG4gICAqL1xuICBwcml2YXRlIF9vblRlcm1pbmFsc1J1bm5pbmdDaGFuZ2VkKFxuICAgIG1hbmFnZXI6IFRlcm1pbmFsTWFuYWdlcixcbiAgICB0ZXJtaW5hbHM6IFRlcm1pbmFsLklNb2RlbFtdXG4gICk6IHZvaWQge1xuICAgIHRoaXMubW9kZWwhLnRlcm1pbmFscyA9IHRlcm1pbmFscy5sZW5ndGg7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfaGFuZGxlQ2xpY2s6ICgpID0+IHZvaWQ7XG4gIHByaXZhdGUgX3NlcnZpY2VNYW5hZ2VyOiBTZXJ2aWNlTWFuYWdlcjtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgUnVubmluZ1Nlc3Npb25zIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgUnVubmluZ1Nlc3Npb25zIHtcbiAgLyoqXG4gICAqIEEgVkRvbU1vZGVsIGZvciB0aGUgUnVubmluZ1Nlc3Npb25zIHN0YXR1cyBpdGVtLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIE1vZGVsIGV4dGVuZHMgVkRvbU1vZGVsIHtcbiAgICAvKipcbiAgICAgKiBUaGUgbnVtYmVyIG9mIGFjdGl2ZSBrZXJuZWwgc2Vzc2lvbnMuXG4gICAgICovXG4gICAgZ2V0IHNlc3Npb25zKCk6IG51bWJlciB7XG4gICAgICByZXR1cm4gdGhpcy5fc2Vzc2lvbnM7XG4gICAgfVxuICAgIHNldCBzZXNzaW9ucyhzZXNzaW9uczogbnVtYmVyKSB7XG4gICAgICBjb25zdCBvbGRTZXNzaW9ucyA9IHRoaXMuX3Nlc3Npb25zO1xuICAgICAgdGhpcy5fc2Vzc2lvbnMgPSBzZXNzaW9ucztcblxuICAgICAgaWYgKG9sZFNlc3Npb25zICE9PSB0aGlzLl9zZXNzaW9ucykge1xuICAgICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIG51bWJlciBvZiBhY3RpdmUgdGVybWluYWwgc2Vzc2lvbnMuXG4gICAgICovXG4gICAgZ2V0IHRlcm1pbmFscygpOiBudW1iZXIge1xuICAgICAgcmV0dXJuIHRoaXMuX3Rlcm1pbmFscztcbiAgICB9XG4gICAgc2V0IHRlcm1pbmFscyh0ZXJtaW5hbHM6IG51bWJlcikge1xuICAgICAgY29uc3Qgb2xkVGVybWluYWxzID0gdGhpcy5fdGVybWluYWxzO1xuICAgICAgdGhpcy5fdGVybWluYWxzID0gdGVybWluYWxzO1xuXG4gICAgICBpZiAob2xkVGVybWluYWxzICE9PSB0aGlzLl90ZXJtaW5hbHMpIHtcbiAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgfVxuICAgIH1cblxuICAgIHByaXZhdGUgX3Rlcm1pbmFsczogbnVtYmVyID0gMDtcbiAgICBwcml2YXRlIF9zZXNzaW9uczogbnVtYmVyID0gMDtcbiAgfVxuXG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBjcmVhdGluZyBhIFJ1bm5pbmdTZXNzaW9ucyBpdGVtLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGFwcGxpY2F0aW9uIHNlcnZpY2UgbWFuYWdlci5cbiAgICAgKi9cbiAgICBzZXJ2aWNlTWFuYWdlcjogU2VydmljZU1hbmFnZXI7XG5cbiAgICAvKipcbiAgICAgKiBBIGNsaWNrIGhhbmRsZXIgZm9yIHRoZSBpdGVtLiBCeSBkZWZhdWx0IHRoaXMgaXMgdXNlZFxuICAgICAqIHRvIGFjdGl2YXRlIHRoZSBydW5uaW5nIHNlc3Npb25zIHNpZGUgcGFuZWwuXG4gICAgICovXG4gICAgb25DbGljazogKCkgPT4gdm9pZDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBhcHBsaWNhdGlvbiBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxufVxuIiwiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBzdGF0dXNiYXJcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL2NvbXBvbmVudHMnO1xuZXhwb3J0ICogZnJvbSAnLi9kZWZhdWx0cyc7XG5leHBvcnQgKiBmcm9tICcuL3N0YXR1c2Jhcic7XG5leHBvcnQgKiBmcm9tICcuL3N0eWxlL3N0YXR1c2Jhcic7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IEFycmF5RXh0IH0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHtcbiAgRGlzcG9zYWJsZURlbGVnYXRlLFxuICBEaXNwb3NhYmxlU2V0LFxuICBJRGlzcG9zYWJsZVxufSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IFBhbmVsLCBQYW5lbExheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7XG4gIHN0YXR1c0JhciBhcyBiYXJTdHlsZSxcbiAgaXRlbSBhcyBpdGVtU3R5bGUsXG4gIGxlZnRTaWRlIGFzIGxlZnRTaWRlU3R5bGUsXG4gIHJpZ2h0U2lkZSBhcyByaWdodFNpZGVTdHlsZSxcbiAgc2lkZSBhcyBzaWRlU3R5bGVcbn0gZnJvbSAnLi9zdHlsZS9zdGF0dXNiYXInO1xuaW1wb3J0IHsgSVN0YXR1c0JhciB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBNYWluIHN0YXR1cyBiYXIgb2JqZWN0IHdoaWNoIGNvbnRhaW5zIGFsbCBpdGVtcy5cbiAqL1xuZXhwb3J0IGNsYXNzIFN0YXR1c0JhciBleHRlbmRzIFdpZGdldCBpbXBsZW1lbnRzIElTdGF0dXNCYXIge1xuICBjb25zdHJ1Y3RvcigpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuYWRkQ2xhc3MoYmFyU3R5bGUpO1xuXG4gICAgY29uc3Qgcm9vdExheW91dCA9ICh0aGlzLmxheW91dCA9IG5ldyBQYW5lbExheW91dCgpKTtcblxuICAgIGNvbnN0IGxlZnRQYW5lbCA9ICh0aGlzLl9sZWZ0U2lkZSA9IG5ldyBQYW5lbCgpKTtcbiAgICBjb25zdCBtaWRkbGVQYW5lbCA9ICh0aGlzLl9taWRkbGVQYW5lbCA9IG5ldyBQYW5lbCgpKTtcbiAgICBjb25zdCByaWdodFBhbmVsID0gKHRoaXMuX3JpZ2h0U2lkZSA9IG5ldyBQYW5lbCgpKTtcblxuICAgIGxlZnRQYW5lbC5hZGRDbGFzcyhzaWRlU3R5bGUpO1xuICAgIGxlZnRQYW5lbC5hZGRDbGFzcyhsZWZ0U2lkZVN0eWxlKTtcblxuICAgIG1pZGRsZVBhbmVsLmFkZENsYXNzKHNpZGVTdHlsZSk7XG5cbiAgICByaWdodFBhbmVsLmFkZENsYXNzKHNpZGVTdHlsZSk7XG4gICAgcmlnaHRQYW5lbC5hZGRDbGFzcyhyaWdodFNpZGVTdHlsZSk7XG5cbiAgICByb290TGF5b3V0LmFkZFdpZGdldChsZWZ0UGFuZWwpO1xuICAgIHJvb3RMYXlvdXQuYWRkV2lkZ2V0KG1pZGRsZVBhbmVsKTtcbiAgICByb290TGF5b3V0LmFkZFdpZGdldChyaWdodFBhbmVsKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZWdpc3RlciBhIG5ldyBzdGF0dXMgaXRlbS5cbiAgICpcbiAgICogQHBhcmFtIGlkIC0gYSB1bmlxdWUgaWQgZm9yIHRoZSBzdGF0dXMgaXRlbS5cbiAgICpcbiAgICogQHBhcmFtIHN0YXR1c0l0ZW0gLSBUaGUgaXRlbSB0byBhZGQgdG8gdGhlIHN0YXR1cyBiYXIuXG4gICAqL1xuICByZWdpc3RlclN0YXR1c0l0ZW0oaWQ6IHN0cmluZywgc3RhdHVzSXRlbTogSVN0YXR1c0Jhci5JSXRlbSk6IElEaXNwb3NhYmxlIHtcbiAgICBpZiAoaWQgaW4gdGhpcy5fc3RhdHVzSXRlbXMpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgU3RhdHVzIGl0ZW0gJHtpZH0gYWxyZWFkeSByZWdpc3RlcmVkLmApO1xuICAgIH1cblxuICAgIC8vIFBvcHVsYXRlIGRlZmF1bHRzIGZvciB0aGUgb3B0aW9uYWwgcHJvcGVydGllcyBvZiB0aGUgc3RhdHVzIGl0ZW0uXG4gICAgY29uc3QgZnVsbFN0YXR1c0l0ZW0gPSB7XG4gICAgICAuLi5Qcml2YXRlLnN0YXR1c0l0ZW1EZWZhdWx0cyxcbiAgICAgIC4uLnN0YXR1c0l0ZW1cbiAgICB9IGFzIFByaXZhdGUuSUZ1bGxJdGVtO1xuICAgIGNvbnN0IHsgYWxpZ24sIGl0ZW0sIHJhbmsgfSA9IGZ1bGxTdGF0dXNJdGVtO1xuXG4gICAgLy8gQ29ubmVjdCB0aGUgYWN0aXZlU3RhdGVDaGFuZ2VkIHNpZ25hbCB0byByZWZyZXNoaW5nIHRoZSBzdGF0dXMgaXRlbSxcbiAgICAvLyBpZiB0aGUgc2lnbmFsIHdhcyBwcm92aWRlZC5cbiAgICBjb25zdCBvbkFjdGl2ZVN0YXRlQ2hhbmdlZCA9ICgpID0+IHtcbiAgICAgIHRoaXMuX3JlZnJlc2hJdGVtKGlkKTtcbiAgICB9O1xuICAgIGlmIChmdWxsU3RhdHVzSXRlbS5hY3RpdmVTdGF0ZUNoYW5nZWQpIHtcbiAgICAgIGZ1bGxTdGF0dXNJdGVtLmFjdGl2ZVN0YXRlQ2hhbmdlZC5jb25uZWN0KG9uQWN0aXZlU3RhdGVDaGFuZ2VkKTtcbiAgICB9XG5cbiAgICBjb25zdCByYW5rSXRlbSA9IHsgaWQsIHJhbmsgfTtcblxuICAgIGZ1bGxTdGF0dXNJdGVtLml0ZW0uYWRkQ2xhc3MoaXRlbVN0eWxlKTtcbiAgICB0aGlzLl9zdGF0dXNJdGVtc1tpZF0gPSBmdWxsU3RhdHVzSXRlbTtcblxuICAgIGlmIChhbGlnbiA9PT0gJ2xlZnQnKSB7XG4gICAgICBjb25zdCBpbnNlcnRJbmRleCA9IHRoaXMuX2ZpbmRJbnNlcnRJbmRleCh0aGlzLl9sZWZ0UmFua0l0ZW1zLCByYW5rSXRlbSk7XG4gICAgICBpZiAoaW5zZXJ0SW5kZXggPT09IC0xKSB7XG4gICAgICAgIHRoaXMuX2xlZnRTaWRlLmFkZFdpZGdldChpdGVtKTtcbiAgICAgICAgdGhpcy5fbGVmdFJhbmtJdGVtcy5wdXNoKHJhbmtJdGVtKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIEFycmF5RXh0Lmluc2VydCh0aGlzLl9sZWZ0UmFua0l0ZW1zLCBpbnNlcnRJbmRleCwgcmFua0l0ZW0pO1xuICAgICAgICB0aGlzLl9sZWZ0U2lkZS5pbnNlcnRXaWRnZXQoaW5zZXJ0SW5kZXgsIGl0ZW0pO1xuICAgICAgfVxuICAgIH0gZWxzZSBpZiAoYWxpZ24gPT09ICdyaWdodCcpIHtcbiAgICAgIGNvbnN0IGluc2VydEluZGV4ID0gdGhpcy5fZmluZEluc2VydEluZGV4KHRoaXMuX3JpZ2h0UmFua0l0ZW1zLCByYW5rSXRlbSk7XG4gICAgICBpZiAoaW5zZXJ0SW5kZXggPT09IC0xKSB7XG4gICAgICAgIHRoaXMuX3JpZ2h0U2lkZS5hZGRXaWRnZXQoaXRlbSk7XG4gICAgICAgIHRoaXMuX3JpZ2h0UmFua0l0ZW1zLnB1c2gocmFua0l0ZW0pO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgQXJyYXlFeHQuaW5zZXJ0KHRoaXMuX3JpZ2h0UmFua0l0ZW1zLCBpbnNlcnRJbmRleCwgcmFua0l0ZW0pO1xuICAgICAgICB0aGlzLl9yaWdodFNpZGUuaW5zZXJ0V2lkZ2V0KGluc2VydEluZGV4LCBpdGVtKTtcbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5fbWlkZGxlUGFuZWwuYWRkV2lkZ2V0KGl0ZW0pO1xuICAgIH1cbiAgICB0aGlzLl9yZWZyZXNoSXRlbShpZCk7IC8vIEluaXRpYWxseSByZWZyZXNoIHRoZSBzdGF0dXMgaXRlbS5cblxuICAgIGNvbnN0IGRpc3Bvc2FibGUgPSBuZXcgRGlzcG9zYWJsZURlbGVnYXRlKCgpID0+IHtcbiAgICAgIGRlbGV0ZSB0aGlzLl9zdGF0dXNJdGVtc1tpZF07XG4gICAgICBpZiAoZnVsbFN0YXR1c0l0ZW0uYWN0aXZlU3RhdGVDaGFuZ2VkKSB7XG4gICAgICAgIGZ1bGxTdGF0dXNJdGVtLmFjdGl2ZVN0YXRlQ2hhbmdlZC5kaXNjb25uZWN0KG9uQWN0aXZlU3RhdGVDaGFuZ2VkKTtcbiAgICAgIH1cbiAgICAgIGl0ZW0ucGFyZW50ID0gbnVsbDtcbiAgICAgIGl0ZW0uZGlzcG9zZSgpO1xuICAgIH0pO1xuICAgIHRoaXMuX2Rpc3Bvc2FibGVzLmFkZChkaXNwb3NhYmxlKTtcbiAgICByZXR1cm4gZGlzcG9zYWJsZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSBzdGF0dXMgYmFyLlxuICAgKi9cbiAgZGlzcG9zZSgpIHtcbiAgICB0aGlzLl9sZWZ0UmFua0l0ZW1zLmxlbmd0aCA9IDA7XG4gICAgdGhpcy5fcmlnaHRSYW5rSXRlbXMubGVuZ3RoID0gMDtcbiAgICB0aGlzLl9kaXNwb3NhYmxlcy5kaXNwb3NlKCk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhbiAndXBkYXRlLXJlcXVlc3QnIG1lc3NhZ2UgdG8gdGhlIHN0YXR1cyBiYXIuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25VcGRhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSkge1xuICAgIHRoaXMuX3JlZnJlc2hBbGwoKTtcbiAgICBzdXBlci5vblVwZGF0ZVJlcXVlc3QobXNnKTtcbiAgfVxuXG4gIHByaXZhdGUgX2ZpbmRJbnNlcnRJbmRleChcbiAgICBzaWRlOiBQcml2YXRlLklSYW5rSXRlbVtdLFxuICAgIG5ld0l0ZW06IFByaXZhdGUuSVJhbmtJdGVtXG4gICk6IG51bWJlciB7XG4gICAgcmV0dXJuIEFycmF5RXh0LmZpbmRGaXJzdEluZGV4KHNpZGUsIGl0ZW0gPT4gaXRlbS5yYW5rID4gbmV3SXRlbS5yYW5rKTtcbiAgfVxuXG4gIHByaXZhdGUgX3JlZnJlc2hJdGVtKGlkOiBzdHJpbmcpIHtcbiAgICBjb25zdCBzdGF0dXNJdGVtID0gdGhpcy5fc3RhdHVzSXRlbXNbaWRdO1xuICAgIGlmIChzdGF0dXNJdGVtLmlzQWN0aXZlKCkpIHtcbiAgICAgIHN0YXR1c0l0ZW0uaXRlbS5zaG93KCk7XG4gICAgICBzdGF0dXNJdGVtLml0ZW0udXBkYXRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0YXR1c0l0ZW0uaXRlbS5oaWRlKCk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfcmVmcmVzaEFsbCgpOiB2b2lkIHtcbiAgICBPYmplY3Qua2V5cyh0aGlzLl9zdGF0dXNJdGVtcykuZm9yRWFjaChpZCA9PiB7XG4gICAgICB0aGlzLl9yZWZyZXNoSXRlbShpZCk7XG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9sZWZ0UmFua0l0ZW1zOiBQcml2YXRlLklSYW5rSXRlbVtdID0gW107XG4gIHByaXZhdGUgX3JpZ2h0UmFua0l0ZW1zOiBQcml2YXRlLklSYW5rSXRlbVtdID0gW107XG4gIHByaXZhdGUgX3N0YXR1c0l0ZW1zOiB7IFtpZDogc3RyaW5nXTogUHJpdmF0ZS5JRnVsbEl0ZW0gfSA9IHt9O1xuICBwcml2YXRlIF9kaXNwb3NhYmxlcyA9IG5ldyBEaXNwb3NhYmxlU2V0KCk7XG4gIHByaXZhdGUgX2xlZnRTaWRlOiBQYW5lbDtcbiAgcHJpdmF0ZSBfbWlkZGxlUGFuZWw6IFBhbmVsO1xuICBwcml2YXRlIF9yaWdodFNpZGU6IFBhbmVsO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIGZ1bmN0aW9uYWxpdHkuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgdHlwZSBPbWl0PFQsIEsgZXh0ZW5kcyBrZXlvZiBUPiA9IFBpY2s8VCwgRXhjbHVkZTxrZXlvZiBULCBLPj47XG4gIC8qKlxuICAgKiBEZWZhdWx0IG9wdGlvbnMgZm9yIGEgc3RhdHVzIGl0ZW0sIGxlc3MgdGhlIGl0ZW0gaXRzZWxmLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IHN0YXR1c0l0ZW1EZWZhdWx0czogT21pdDxJU3RhdHVzQmFyLklJdGVtLCAnaXRlbSc+ID0ge1xuICAgIGFsaWduOiAnbGVmdCcsXG4gICAgcmFuazogMCxcbiAgICBpc0FjdGl2ZTogKCkgPT4gdHJ1ZSxcbiAgICBhY3RpdmVTdGF0ZUNoYW5nZWQ6IHVuZGVmaW5lZFxuICB9O1xuXG4gIC8qKlxuICAgKiBBbiBpbnRlcmZhY2UgZm9yIHN0b3JpbmcgdGhlIHJhbmsgb2YgYSBzdGF0dXMgaXRlbS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVJhbmtJdGVtIHtcbiAgICBpZDogc3RyaW5nO1xuICAgIHJhbms6IG51bWJlcjtcbiAgfVxuXG4gIGV4cG9ydCB0eXBlIERlZmF1bHRLZXlzID0gJ2FsaWduJyB8ICdyYW5rJyB8ICdpc0FjdGl2ZSc7XG5cbiAgLyoqXG4gICAqIFR5cGUgb2Ygc3RhdHVzYmFyIGl0ZW0gd2l0aCBkZWZhdWx0cyBmaWxsZWQgaW4uXG4gICAqL1xuICBleHBvcnQgdHlwZSBJRnVsbEl0ZW0gPSBSZXF1aXJlZDxQaWNrPElTdGF0dXNCYXIuSUl0ZW0sIERlZmF1bHRLZXlzPj4gJlxuICAgIE9taXQ8SVN0YXR1c0Jhci5JSXRlbSwgRGVmYXVsdEtleXM+O1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBOZXN0ZWRDU1NQcm9wZXJ0aWVzIH0gZnJvbSAndHlwZXN0eWxlL2xpYi90eXBlcyc7XG5cbmV4cG9ydCBjb25zdCBjZW50ZXJlZEZsZXg6IE5lc3RlZENTU1Byb3BlcnRpZXMgPSB7XG4gIGRpc3BsYXk6ICdmbGV4JyxcbiAgYWxpZ25JdGVtczogJ2NlbnRlcidcbn07XG5cbmV4cG9ydCBjb25zdCBsZWZ0VG9SaWdodDogTmVzdGVkQ1NTUHJvcGVydGllcyA9IHtcbiAgZmxleERpcmVjdGlvbjogJ3Jvdydcbn07XG5cbmV4cG9ydCBjb25zdCByaWdodFRvTGVmdDogTmVzdGVkQ1NTUHJvcGVydGllcyA9IHtcbiAgZmxleERpcmVjdGlvbjogJ3Jvdy1yZXZlcnNlJ1xufTtcblxuZXhwb3J0IGNvbnN0IGVxdWlEaXN0YW50OiBOZXN0ZWRDU1NQcm9wZXJ0aWVzID0ge1xuICBqdXN0aWZ5Q29udGVudDogJ3NwYWNlLWJldHdlZW4nXG59O1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBzdHlsZSB9IGZyb20gJ3R5cGVzdHlsZS9saWInO1xuaW1wb3J0IHsgTmVzdGVkQ1NTUHJvcGVydGllcyB9IGZyb20gJ3R5cGVzdHlsZS9saWIvdHlwZXMnO1xuXG5leHBvcnQgY29uc3QgaG92ZXJJdGVtID0gc3R5bGUoe1xuICBib3hTaGFkb3c6ICcwcHggNHB4IDRweCByZ2JhKDAsIDAsIDAsIDAuMjUpJ1xufSk7XG5cbmV4cG9ydCBjb25zdCBsaW5lRm9ybVNlYXJjaCA9IHN0eWxlKHtcbiAgcGFkZGluZzogJzRweCAxMnB4JyxcbiAgYmFja2dyb3VuZENvbG9yOiAndmFyKC0tanAtbGF5b3V0LWNvbG9yMiknLFxuICBib3hTaGFkb3c6ICd2YXIoLS1qcC10b29sYmFyLWJveC1zaGFkb3cpJyxcbiAgekluZGV4OiAyLFxuICBmb250U2l6ZTogJ3ZhcigtLWpwLXVpLWZvbnQtc2l6ZTEpJ1xufSk7XG5cbmV4cG9ydCBjb25zdCBsaW5lRm9ybUNhcHRpb24gPSBzdHlsZSh7XG4gIGZvbnRTaXplOiAndmFyKC0tanAtdWktZm9udC1zaXplMCknLFxuICBsaW5lSGVpZ2h0OiAndmFyKC0tanAtdWktZm9udC1zaXplMSknLFxuICBtYXJnaW5Ub3A6ICc0cHgnLFxuICBjb2xvcjogJ3ZhcigtLWpwLXVpLWZvbnQtY29sb3IwKSdcbn0pO1xuXG5leHBvcnQgY29uc3QgYmFzZUxpbmVGb3JtOiBOZXN0ZWRDU1NQcm9wZXJ0aWVzID0ge1xuICBib3JkZXI6ICdub25lJyxcbiAgYm9yZGVyUmFkaXVzOiAnMHB4JyxcbiAgcG9zaXRpb246ICdhYnNvbHV0ZScsXG4gIGJhY2tncm91bmRTaXplOiAnMTZweCcsXG4gIGJhY2tncm91bmRSZXBlYXQ6ICduby1yZXBlYXQnLFxuICBiYWNrZ3JvdW5kUG9zaXRpb246ICdjZW50ZXInLFxuICBvdXRsaW5lOiAnbm9uZScsXG4gIHRvcDogJzBweCcsXG4gIHJpZ2h0OiAnMHB4J1xufTtcblxuZXhwb3J0IGNvbnN0IGxpbmVGb3JtQnV0dG9uRGl2ID0gc3R5bGUoYmFzZUxpbmVGb3JtLCB7XG4gIHRvcDogJzRweCcsXG4gIHJpZ2h0OiAnOHB4JyxcbiAgaGVpZ2h0OiAnMjRweCcsXG4gIHBhZGRpbmc6ICcwcHggMTJweCcsXG4gIHdpZHRoOiAnMTJweCdcbn0pO1xuXG5leHBvcnQgY29uc3QgbGluZUZvcm1CdXR0b25JY29uID0gc3R5bGUoYmFzZUxpbmVGb3JtLCB7XG4gIGJhY2tncm91bmRDb2xvcjogJ3ZhcigtLWpwLWJyYW5kLWNvbG9yMSknLFxuICBoZWlnaHQ6ICcxMDAlJyxcbiAgd2lkdGg6ICcxMDAlJyxcbiAgYm94U2l6aW5nOiAnYm9yZGVyLWJveCcsXG4gIHBhZGRpbmc6ICc0cHggNnB4J1xufSk7XG5cbmV4cG9ydCBjb25zdCBsaW5lRm9ybUJ1dHRvbiA9IHN0eWxlKGJhc2VMaW5lRm9ybSwge1xuICBiYWNrZ3JvdW5kQ29sb3I6ICd0cmFuc3BhcmVudCcsXG4gIGhlaWdodDogJzEwMCUnLFxuICB3aWR0aDogJzEwMCUnLFxuICBib3hTaXppbmc6ICdib3JkZXItYm94J1xufSk7XG5cbmV4cG9ydCBjb25zdCBsaW5lRm9ybVdyYXBwZXIgPSBzdHlsZSh7XG4gIG92ZXJmbG93OiAnaGlkZGVuJyxcbiAgcGFkZGluZzogJzBweCA4cHgnLFxuICBib3JkZXI6ICcxcHggc29saWQgdmFyKC0tanAtYm9yZGVyLWNvbG9yMCknLFxuICBiYWNrZ3JvdW5kQ29sb3I6ICd2YXIoLS1qcC1pbnB1dC1hY3RpdmUtYmFja2dyb3VuZCknLFxuICBoZWlnaHQ6ICcyMnB4J1xufSk7XG5cbmV4cG9ydCBjb25zdCBsaW5lRm9ybVdyYXBwZXJGb2N1c1dpdGhpbiA9IHN0eWxlKHtcbiAgYm9yZGVyOiAndmFyKC0tanAtYm9yZGVyLXdpZHRoKSBzb2xpZCB2YXIoLS1tZC1ibHVlLTUwMCknLFxuICBib3hTaGFkb3c6ICdpbnNldCAwIDAgNHB4IHZhcigtLW1kLWJsdWUtMzAwKSdcbn0pO1xuXG5leHBvcnQgY29uc3QgbGluZUZvcm1JbnB1dCA9IHN0eWxlKHtcbiAgYmFja2dyb3VuZDogJ3RyYW5zcGFyZW50JyxcbiAgd2lkdGg6ICcyMDBweCcsXG4gIGhlaWdodDogJzEwMCUnLFxuICBib3JkZXI6ICdub25lJyxcbiAgb3V0bGluZTogJ25vbmUnLFxuICBjb2xvcjogJ3ZhcigtLWpwLXVpLWZvbnQtY29sb3IwKScsXG4gIGxpbmVIZWlnaHQ6ICcyOHB4J1xufSk7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IHN0eWxlIH0gZnJvbSAndHlwZXN0eWxlL2xpYic7XG5cbmV4cG9ydCBjb25zdCBwcm9ncmVzc0Jhckl0ZW0gPSBzdHlsZSh7XG4gIGJhY2tncm91bmQ6ICdibGFjaycsXG4gIGhlaWdodDogJzEwcHgnLFxuICB3aWR0aDogJzEwMHB4JyxcbiAgYm9yZGVyOiAnMXB4IHNvbGlkIGJsYWNrJyxcbiAgYm9yZGVyUmFkaXVzOiAnM3B4JyxcbiAgbWFyZ2luTGVmdDogJzRweCcsXG4gIG92ZXJmbG93OiAnaGlkZGVuJ1xufSk7XG5cbmV4cG9ydCBjb25zdCBmaWxsZXJJdGVtID0gc3R5bGUoe1xuICBiYWNrZ3JvdW5kOiAndmFyKC0tanAtYnJhbmQtY29sb3IyKScsXG4gIGhlaWdodDogJzEwcHgnXG59KTtcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgc3R5bGUgfSBmcm9tICd0eXBlc3R5bGUvbGliJztcbmltcG9ydCB7IGNlbnRlcmVkRmxleCwgbGVmdFRvUmlnaHQsIHJpZ2h0VG9MZWZ0IH0gZnJvbSAnLi9sYXlvdXQnO1xuaW1wb3J0IHsgdGV4dEl0ZW0gfSBmcm9tICcuL3RleHQnO1xuaW1wb3J0IHZhcnMgZnJvbSAnLi92YXJpYWJsZXMnO1xuXG5jb25zdCBpdGVtUGFkZGluZyA9IHtcbiAgcGFkZGluZ0xlZnQ6IHZhcnMuaXRlbVBhZGRpbmcsXG4gIHBhZGRpbmdSaWdodDogdmFycy5pdGVtUGFkZGluZ1xufTtcblxuY29uc3QgaW50ZXJhY3RpdmVIb3ZlciA9IHtcbiAgJG5lc3Q6IHtcbiAgICAnJjpob3Zlcic6IHtcbiAgICAgIGJhY2tncm91bmRDb2xvcjogdmFycy5ob3ZlckNvbG9yXG4gICAgfVxuICB9XG59O1xuXG5jb25zdCBjbGlja2VkID0ge1xuICBiYWNrZ3JvdW5kQ29sb3I6IHZhcnMuY2xpY2tDb2xvcixcbiAgJG5lc3Q6IHtcbiAgICBbJy4nICsgdGV4dEl0ZW1dOiB7XG4gICAgICBjb2xvcjogdmFycy50ZXh0Q2xpY2tDb2xvclxuICAgIH1cbiAgfVxufTtcblxuZXhwb3J0IGNvbnN0IHN0YXR1c0JhciA9IHN0eWxlKFxuICB7XG4gICAgYmFja2dyb3VuZDogdmFycy5iYWNrZ3JvdW5kQ29sb3IsXG4gICAgbWluSGVpZ2h0OiB2YXJzLmhlaWdodCxcbiAgICBqdXN0aWZ5Q29udGVudDogJ3NwYWNlLWJldHdlZW4nLFxuICAgIHBhZGRpbmdMZWZ0OiB2YXJzLnN0YXR1c0JhclBhZGRpbmcsXG4gICAgcGFkZGluZ1JpZ2h0OiB2YXJzLnN0YXR1c0JhclBhZGRpbmdcbiAgfSxcbiAgY2VudGVyZWRGbGV4XG4pO1xuXG5leHBvcnQgY29uc3Qgc2lkZSA9IHN0eWxlKGNlbnRlcmVkRmxleCk7XG5cbmV4cG9ydCBjb25zdCBsZWZ0U2lkZSA9IHN0eWxlKGxlZnRUb1JpZ2h0KTtcblxuZXhwb3J0IGNvbnN0IHJpZ2h0U2lkZSA9IHN0eWxlKHJpZ2h0VG9MZWZ0KTtcblxuZXhwb3J0IGNvbnN0IGl0ZW0gPSBzdHlsZShcbiAge1xuICAgIG1heEhlaWdodDogdmFycy5oZWlnaHQsXG4gICAgbWFyZ2luTGVmdDogdmFycy5pdGVtTWFyZ2luLFxuICAgIG1hcmdpblJpZ2h0OiB2YXJzLml0ZW1NYXJnaW4sXG4gICAgaGVpZ2h0OiB2YXJzLmhlaWdodCxcbiAgICB3aGl0ZVNwYWNlOiB2YXJzLndoaXRlU3BhY2UsXG4gICAgdGV4dE92ZXJmbG93OiB2YXJzLnRleHRPdmVyZmxvdyxcbiAgICBjb2xvcjogdmFycy50ZXh0Q29sb3JcbiAgfSxcbiAgaXRlbVBhZGRpbmdcbik7XG5cbmV4cG9ydCBjb25zdCBjbGlja2VkSXRlbSA9IHN0eWxlKGNsaWNrZWQpO1xuZXhwb3J0IGNvbnN0IGludGVyYWN0aXZlSXRlbSA9IHN0eWxlKGludGVyYWN0aXZlSG92ZXIpO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBzdHlsZSB9IGZyb20gJ3R5cGVzdHlsZS9saWInO1xuaW1wb3J0IHsgTmVzdGVkQ1NTUHJvcGVydGllcyB9IGZyb20gJ3R5cGVzdHlsZS9saWIvdHlwZXMnO1xuaW1wb3J0IHZhcnMgZnJvbSAnLi92YXJpYWJsZXMnO1xuXG5leHBvcnQgY29uc3QgYmFzZVRleHQ6IE5lc3RlZENTU1Byb3BlcnRpZXMgPSB7XG4gIGZvbnRTaXplOiB2YXJzLmZvbnRTaXplLFxuICBmb250RmFtaWx5OiB2YXJzLmZvbnRGYW1pbHlcbn07XG5cbmV4cG9ydCBjb25zdCB0ZXh0SXRlbSA9IHN0eWxlKGJhc2VUZXh0LCB7XG4gIGxpbmVIZWlnaHQ6ICcyNHB4JyxcbiAgY29sb3I6IHZhcnMudGV4dENvbG9yXG59KTtcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbmltcG9ydCB7IFByb3BlcnR5IH0gZnJvbSAnY3NzdHlwZSc7XG5cbmV4cG9ydCBkZWZhdWx0IHtcbiAgaG92ZXJDb2xvcjogJ3ZhcigtLWpwLWxheW91dC1jb2xvcjMpJyxcbiAgY2xpY2tDb2xvcjogJ3ZhcigtLWpwLWJyYW5kLWNvbG9yMSknLFxuICBiYWNrZ3JvdW5kQ29sb3I6ICd2YXIoLS1qcC1sYXlvdXQtY29sb3IyKScsXG4gIGhlaWdodDogJ3ZhcigtLWpwLXN0YXR1c2Jhci1oZWlnaHQpJyxcbiAgZm9udFNpemU6ICd2YXIoLS1qcC11aS1mb250LXNpemUxKScsXG4gIGZvbnRGYW1pbHk6ICd2YXIoLS1qcC11aS1mb250LWZhbWlseSknLFxuICB0ZXh0Q29sb3I6ICd2YXIoLS1qcC11aS1mb250LWNvbG9yMSknLFxuICB0ZXh0Q2xpY2tDb2xvcjogJ3doaXRlJyxcbiAgaXRlbU1hcmdpbjogJzJweCcsXG4gIGl0ZW1QYWRkaW5nOiAnNnB4JyxcbiAgc3RhdHVzQmFyUGFkZGluZzogJzEwcHgnLFxuICBpbnRlckl0ZW1IYWxmU3BhY2luZzogJzJweCcsIC8vIHRoaXMgYW1vdW50IGFjY291bnRzIGZvciBoYWxmIHRoZSBzcGFjaW5nIGJldHdlZW4gaXRlbXNcbiAgd2hpdGVTcGFjZTogJ25vd3JhcCcgYXMgUHJvcGVydHkuV2hpdGVTcGFjZSxcbiAgdGV4dE92ZXJmbG93OiAnZWxsaXBzaXMnXG59O1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vLyB0c2xpbnQ6ZGlzYWJsZS1uZXh0LWxpbmU6dmFyaWFibGUtbmFtZVxuZXhwb3J0IGNvbnN0IElTdGF0dXNCYXIgPSBuZXcgVG9rZW48SVN0YXR1c0Jhcj4oXG4gICdAanVweXRlcmxhYi9zdGF0dXNiYXI6SVN0YXR1c0Jhcidcbik7XG5cbi8qKlxuICogTWFpbiBzdGF0dXMgYmFyIG9iamVjdCB3aGljaCBjb250YWlucyBhbGwgd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJU3RhdHVzQmFyIHtcbiAgLyoqXG4gICAqIFJlZ2lzdGVyIGEgbmV3IHN0YXR1cyBpdGVtLlxuICAgKlxuICAgKiBAcGFyYW0gaWQgLSBhIHVuaXF1ZSBpZCBmb3IgdGhlIHN0YXR1cyBpdGVtLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBvcHRpb25zIGZvciBob3cgdG8gYWRkIHRoZSBzdGF0dXMgaXRlbS5cbiAgICpcbiAgICogQHJldHVybnMgYW4gYElEaXNwb3NhYmxlYCB0aGF0IGNhbiBiZSBkaXNwb3NlZCB0byByZW1vdmUgdGhlIGl0ZW0uXG4gICAqL1xuICByZWdpc3RlclN0YXR1c0l0ZW0oaWQ6IHN0cmluZywgc3RhdHVzSXRlbTogSVN0YXR1c0Jhci5JSXRlbSk6IElEaXNwb3NhYmxlO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBzdGF0dXMgYmFyIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVN0YXR1c0JhciB7XG4gIGV4cG9ydCB0eXBlIEFsaWdubWVudCA9ICdyaWdodCcgfCAnbGVmdCcgfCAnbWlkZGxlJztcblxuICAvKipcbiAgICogT3B0aW9ucyBmb3Igc3RhdHVzIGJhciBpdGVtcy5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUl0ZW0ge1xuICAgIC8qKlxuICAgICAqIFRoZSBpdGVtIHRvIGFkZCB0byB0aGUgc3RhdHVzIGJhci5cbiAgICAgKi9cbiAgICBpdGVtOiBXaWRnZXQ7XG5cbiAgICAvKipcbiAgICAgKiBXaGljaCBzaWRlIHRvIHBsYWNlIGl0ZW0uXG4gICAgICogUGVybWFuZW50IGl0ZW1zIGFyZSBpbnRlbmRlZCBmb3IgdGhlIHJpZ2h0IGFuZCBsZWZ0IHNpZGUsXG4gICAgICogd2l0aCBtb3JlIHRyYW5zaWVudCBpdGVtcyBpbiB0aGUgbWlkZGxlLlxuICAgICAqL1xuICAgIGFsaWduPzogQWxpZ25tZW50O1xuXG4gICAgLyoqXG4gICAgICogIE9yZGVyaW5nIG9mIEl0ZW1zIC0tIGhpZ2hlciByYW5rIGl0ZW1zIGFyZSBjbG9zZXIgdG8gdGhlIG1pZGRsZS5cbiAgICAgKi9cbiAgICByYW5rPzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0aGUgaXRlbSBpcyBzaG93biBvciBoaWRkZW4uXG4gICAgICovXG4gICAgaXNBY3RpdmU/OiAoKSA9PiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogQSBzaWduYWwgdGhhdCBpcyBmaXJlZCB3aGVuIHRoZSBpdGVtIGFjdGl2ZSBzdGF0ZSBjaGFuZ2VzLlxuICAgICAqL1xuICAgIGFjdGl2ZVN0YXRlQ2hhbmdlZD86IElTaWduYWw8YW55LCB2b2lkPjtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==