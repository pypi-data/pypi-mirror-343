(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_tooltip_lib_index_js-_51c41"],{

/***/ "../packages/tooltip/lib/index.js":
/*!****************************************!*\
  !*** ../packages/tooltip/lib/index.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITooltipManager": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.ITooltipManager),
/* harmony export */   "Tooltip": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.Tooltip)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "../packages/tooltip/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/tooltip/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module tooltip
 */




/***/ }),

/***/ "../packages/tooltip/lib/tokens.js":
/*!*****************************************!*\
  !*** ../packages/tooltip/lib/tokens.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITooltipManager": () => (/* binding */ ITooltipManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The tooltip manager token.
 */
const ITooltipManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/tooltip:ITooltipManager');


/***/ }),

/***/ "../packages/tooltip/lib/widget.js":
/*!*****************************************!*\
  !*** ../packages/tooltip/lib/widget.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Tooltip": () => (/* binding */ Tooltip)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The class name added to each tooltip.
 */
const TOOLTIP_CLASS = 'jp-Tooltip';
/**
 * The class name added to the tooltip content.
 */
const CONTENT_CLASS = 'jp-Tooltip-content';
/**
 * The class added to the body when a tooltip exists on the page.
 */
const BODY_CLASS = 'jp-mod-tooltip';
/**
 * The minimum height of a tooltip widget.
 */
const MIN_HEIGHT = 20;
/**
 * The maximum height of a tooltip widget.
 */
const MAX_HEIGHT = 250;
/**
 * A flag to indicate that event handlers are caught in the capture phase.
 */
const USE_CAPTURE = true;
/**
 * A tooltip widget.
 */
class Tooltip extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    /**
     * Instantiate a tooltip.
     */
    constructor(options) {
        super();
        this._content = null;
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout());
        const model = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.MimeModel({ data: options.bundle });
        this.anchor = options.anchor;
        this.addClass(TOOLTIP_CLASS);
        this.hide();
        this._editor = options.editor;
        this._position = options.position;
        this._rendermime = options.rendermime;
        const mimeType = this._rendermime.preferredMimeType(options.bundle, 'any');
        if (!mimeType) {
            return;
        }
        this._content = this._rendermime.createRenderer(mimeType);
        this._content
            .renderModel(model)
            .then(() => this._setGeometry())
            .catch(error => console.error('tooltip rendering failed', error));
        this._content.addClass(CONTENT_CLASS);
        layout.addWidget(this._content);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this._content) {
            this._content.dispose();
            this._content = null;
        }
        super.dispose();
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
        if (this.isHidden || this.isDisposed) {
            return;
        }
        const { node } = this;
        const target = event.target;
        switch (event.type) {
            case 'keydown':
                if (node.contains(target)) {
                    return;
                }
                this.dispose();
                break;
            case 'mousedown':
                if (node.contains(target)) {
                    this.activate();
                    return;
                }
                this.dispose();
                break;
            case 'scroll':
                this._evtScroll(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.tabIndex = 0;
        this.node.focus();
    }
    /**
     * Handle `'after-attach'` messages.
     */
    onAfterAttach(msg) {
        document.body.classList.add(BODY_CLASS);
        document.addEventListener('keydown', this, USE_CAPTURE);
        document.addEventListener('mousedown', this, USE_CAPTURE);
        this.anchor.node.addEventListener('scroll', this, USE_CAPTURE);
        this.update();
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        document.body.classList.remove(BODY_CLASS);
        document.removeEventListener('keydown', this, USE_CAPTURE);
        document.removeEventListener('mousedown', this, USE_CAPTURE);
        this.anchor.node.removeEventListener('scroll', this, USE_CAPTURE);
    }
    /**
     * Handle `'update-request'` messages.
     */
    onUpdateRequest(msg) {
        if (this.isHidden) {
            this.show();
        }
        this._setGeometry();
        super.onUpdateRequest(msg);
    }
    /**
     * Handle scroll events for the widget
     */
    _evtScroll(event) {
        // All scrolls except scrolls in the actual hover box node may cause the
        // referent editor that anchors the node to move, so the only scroll events
        // that can safely be ignored are ones that happen inside the hovering node.
        if (this.node.contains(event.target)) {
            return;
        }
        this.update();
    }
    /**
     * Find the position of the first character of the current token.
     */
    _getTokenPosition() {
        const editor = this._editor;
        const cursor = editor.getCursorPosition();
        const end = editor.getOffsetAt(cursor);
        const line = editor.getLine(cursor.line);
        if (!line) {
            return;
        }
        const tokens = line.substring(0, end).split(/\W+/);
        const last = tokens[tokens.length - 1];
        const start = last ? end - last.length : end;
        return editor.getPositionAt(start);
    }
    /**
     * Set the geometry of the tooltip widget.
     */
    _setGeometry() {
        // determine position for hover box placement
        const position = this._position ? this._position : this._getTokenPosition();
        if (!position) {
            return;
        }
        const editor = this._editor;
        const anchor = editor.getCoordinateForPosition(position);
        const style = window.getComputedStyle(this.node);
        const paddingLeft = parseInt(style.paddingLeft, 10) || 0;
        // Calculate the geometry of the tooltip.
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.HoverBox.setGeometry({
            anchor,
            host: editor.host,
            maxHeight: MAX_HEIGHT,
            minHeight: MIN_HEIGHT,
            node: this.node,
            offset: { horizontal: -1 * paddingLeft },
            privilege: 'below',
            style: style
        });
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdG9vbHRpcC9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3Rvb2x0aXAvc3JjL3Rva2Vucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdG9vbHRpcC9zcmMvd2lkZ2V0LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQUVzQjtBQUNBOzs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNSekIsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUtqQjtBQUcxQyxvQkFBb0I7QUFDcEI7O0dBRUc7QUFDSSxNQUFNLGVBQWUsR0FBRyxJQUFJLG9EQUFLLENBQ3RDLHFDQUFxQyxDQUN0QyxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDZkYsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUVYO0FBTWhCO0FBR3NCO0FBRXREOztHQUVHO0FBQ0gsTUFBTSxhQUFhLEdBQUcsWUFBWSxDQUFDO0FBRW5DOztHQUVHO0FBQ0gsTUFBTSxhQUFhLEdBQUcsb0JBQW9CLENBQUM7QUFFM0M7O0dBRUc7QUFDSCxNQUFNLFVBQVUsR0FBRyxnQkFBZ0IsQ0FBQztBQUVwQzs7R0FFRztBQUNILE1BQU0sVUFBVSxHQUFHLEVBQUUsQ0FBQztBQUV0Qjs7R0FFRztBQUNILE1BQU0sVUFBVSxHQUFHLEdBQUcsQ0FBQztBQUV2Qjs7R0FFRztBQUNILE1BQU0sV0FBVyxHQUFHLElBQUksQ0FBQztBQUV6Qjs7R0FFRztBQUNJLE1BQU0sT0FBUSxTQUFRLG1EQUFNO0lBQ2pDOztPQUVHO0lBQ0gsWUFBWSxPQUF5QjtRQUNuQyxLQUFLLEVBQUUsQ0FBQztRQTBMRixhQUFRLEdBQWlDLElBQUksQ0FBQztRQXhM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QUVELE1BQU0sTUFBTSxHQUFHLElBQUksQ0FBQyxPQUFPLENBQUM7UUFFNUIsTUFBTSxNQUFNLEdBQUcsTUFBTSxDQUFDLHdCQUF3QixDQUFDLFFBQVEsQ0FBZSxDQUFDO1FBQ3ZFLE1BQU0sS0FBSyxHQUFHLE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLENBQUM7UUFDakQsTUFBTSxXQUFXLEdBQUcsUUFBUSxDQUFDLEtBQUssQ0FBQyxXQUFZLEVBQUUsRUFBRSxDQUFDLElBQUksQ0FBQyxDQUFDO1FBRTFELHlDQUF5QztRQUN6QyxzRUFBb0IsQ0FBQztZQUNuQixNQUFNO1lBQ04sSUFBSSxFQUFFLE1BQU0sQ0FBQyxJQUFJO1lBQ2pCLFNBQVMsRUFBRSxVQUFVO1lBQ3JCLFNBQVMsRUFBRSxVQUFVO1lBQ3JCLElBQUksRUFBRSxJQUFJLENBQUMsSUFBSTtZQUNmLE1BQU0sRUFBRSxFQUFFLFVBQVUsRUFBRSxDQUFDLENBQUMsR0FBRyxXQUFXLEVBQUU7WUFDeEMsU0FBUyxFQUFFLE9BQU87WUFDbEIsS0FBSyxFQUFFLEtBQUs7U0FDYixDQUFDLENBQUM7SUFDTCxDQUFDO0NBTUYiLCJmaWxlIjoicGFja2FnZXNfdG9vbHRpcF9saWJfaW5kZXhfanMtXzUxYzQxLmNiMDc4MWRkMTM1MmMxM2Q3NGMwLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdG9vbHRpcFxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vdG9rZW5zJztcbmV4cG9ydCAqIGZyb20gJy4vd2lkZ2V0JztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgQ29kZUVkaXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0IHsgSVJlbmRlck1pbWVSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgS2VybmVsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKiB0c2xpbnQ6ZGlzYWJsZSAqL1xuLyoqXG4gKiBUaGUgdG9vbHRpcCBtYW5hZ2VyIHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSVRvb2x0aXBNYW5hZ2VyID0gbmV3IFRva2VuPElUb29sdGlwTWFuYWdlcj4oXG4gICdAanVweXRlcmxhYi90b29sdGlwOklUb29sdGlwTWFuYWdlcidcbik7XG4vKiB0c2xpbnQ6ZW5hYmxlICovXG5cbi8qKlxuICogQSBtYW5hZ2VyIHRvIHJlZ2lzdGVyIHRvb2x0aXBzIHdpdGggcGFyZW50IHdpZGdldHMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVRvb2x0aXBNYW5hZ2VyIHtcbiAgLyoqXG4gICAqIEludm9rZSBhIHRvb2x0aXAuXG4gICAqL1xuICBpbnZva2Uob3B0aW9uczogSVRvb2x0aXBNYW5hZ2VyLklPcHRpb25zKTogdm9pZDtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYElDb21wbGV0aW9uTWFuYWdlcmAgaW50ZXJmYWNlIHNwZWNpZmljYXRpb25zLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElUb29sdGlwTWFuYWdlciB7XG4gIC8qKlxuICAgKiBBbiBpbnRlcmZhY2UgZm9yIHRvb2x0aXAtY29tcGF0aWJsZSBvYmplY3RzLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIHJlZmVyZW50IGFuY2hvciB0aGUgdG9vbHRpcCBmb2xsb3dzLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGFuY2hvcjogV2lkZ2V0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJlZmVyZW50IGVkaXRvciBmb3IgdGhlIHRvb2x0aXAuXG4gICAgICovXG4gICAgcmVhZG9ubHkgZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3I7XG5cbiAgICAvKipcbiAgICAgKiBUaGUga2VybmVsIHRoZSB0b29sdGlwIGNvbW11bmljYXRlcyB3aXRoIHRvIHBvcHVsYXRlIGl0c2VsZi5cbiAgICAgKi9cbiAgICByZWFkb25seSBrZXJuZWw6IEtlcm5lbC5JS2VybmVsQ29ubmVjdGlvbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSByZW5kZXJlciB0aGUgdG9vbHRpcCB1c2VzIHRvIHJlbmRlciBBUEkgcmVzcG9uc2VzLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnk7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSG92ZXJCb3ggfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQge1xuICBJUmVuZGVyTWltZSxcbiAgSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgTWltZU1vZGVsXG59IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgSlNPTk9iamVjdCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBQYW5lbExheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBlYWNoIHRvb2x0aXAuXG4gKi9cbmNvbnN0IFRPT0xUSVBfQ0xBU1MgPSAnanAtVG9vbHRpcCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gdGhlIHRvb2x0aXAgY29udGVudC5cbiAqL1xuY29uc3QgQ09OVEVOVF9DTEFTUyA9ICdqcC1Ub29sdGlwLWNvbnRlbnQnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBhZGRlZCB0byB0aGUgYm9keSB3aGVuIGEgdG9vbHRpcCBleGlzdHMgb24gdGhlIHBhZ2UuXG4gKi9cbmNvbnN0IEJPRFlfQ0xBU1MgPSAnanAtbW9kLXRvb2x0aXAnO1xuXG4vKipcbiAqIFRoZSBtaW5pbXVtIGhlaWdodCBvZiBhIHRvb2x0aXAgd2lkZ2V0LlxuICovXG5jb25zdCBNSU5fSEVJR0hUID0gMjA7XG5cbi8qKlxuICogVGhlIG1heGltdW0gaGVpZ2h0IG9mIGEgdG9vbHRpcCB3aWRnZXQuXG4gKi9cbmNvbnN0IE1BWF9IRUlHSFQgPSAyNTA7XG5cbi8qKlxuICogQSBmbGFnIHRvIGluZGljYXRlIHRoYXQgZXZlbnQgaGFuZGxlcnMgYXJlIGNhdWdodCBpbiB0aGUgY2FwdHVyZSBwaGFzZS5cbiAqL1xuY29uc3QgVVNFX0NBUFRVUkUgPSB0cnVlO1xuXG4vKipcbiAqIEEgdG9vbHRpcCB3aWRnZXQuXG4gKi9cbmV4cG9ydCBjbGFzcyBUb29sdGlwIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIEluc3RhbnRpYXRlIGEgdG9vbHRpcC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IFRvb2x0aXAuSU9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuXG4gICAgY29uc3QgbGF5b3V0ID0gKHRoaXMubGF5b3V0ID0gbmV3IFBhbmVsTGF5b3V0KCkpO1xuICAgIGNvbnN0IG1vZGVsID0gbmV3IE1pbWVNb2RlbCh7IGRhdGE6IG9wdGlvbnMuYnVuZGxlIH0pO1xuXG4gICAgdGhpcy5hbmNob3IgPSBvcHRpb25zLmFuY2hvcjtcbiAgICB0aGlzLmFkZENsYXNzKFRPT0xUSVBfQ0xBU1MpO1xuICAgIHRoaXMuaGlkZSgpO1xuICAgIHRoaXMuX2VkaXRvciA9IG9wdGlvbnMuZWRpdG9yO1xuICAgIHRoaXMuX3Bvc2l0aW9uID0gb3B0aW9ucy5wb3NpdGlvbjtcbiAgICB0aGlzLl9yZW5kZXJtaW1lID0gb3B0aW9ucy5yZW5kZXJtaW1lO1xuXG4gICAgY29uc3QgbWltZVR5cGUgPSB0aGlzLl9yZW5kZXJtaW1lLnByZWZlcnJlZE1pbWVUeXBlKG9wdGlvbnMuYnVuZGxlLCAnYW55Jyk7XG5cbiAgICBpZiAoIW1pbWVUeXBlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgdGhpcy5fY29udGVudCA9IHRoaXMuX3JlbmRlcm1pbWUuY3JlYXRlUmVuZGVyZXIobWltZVR5cGUpO1xuICAgIHRoaXMuX2NvbnRlbnRcbiAgICAgIC5yZW5kZXJNb2RlbChtb2RlbClcbiAgICAgIC50aGVuKCgpID0+IHRoaXMuX3NldEdlb21ldHJ5KCkpXG4gICAgICAuY2F0Y2goZXJyb3IgPT4gY29uc29sZS5lcnJvcigndG9vbHRpcCByZW5kZXJpbmcgZmFpbGVkJywgZXJyb3IpKTtcbiAgICB0aGlzLl9jb250ZW50LmFkZENsYXNzKENPTlRFTlRfQ0xBU1MpO1xuICAgIGxheW91dC5hZGRXaWRnZXQodGhpcy5fY29udGVudCk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGFuY2hvciB3aWRnZXQgdGhhdCB0aGUgdG9vbHRpcCB3aWRnZXQgdHJhY2tzLlxuICAgKi9cbiAgcmVhZG9ubHkgYW5jaG9yOiBXaWRnZXQ7XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSB3aWRnZXQuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9jb250ZW50KSB7XG4gICAgICB0aGlzLl9jb250ZW50LmRpc3Bvc2UoKTtcbiAgICAgIHRoaXMuX2NvbnRlbnQgPSBudWxsO1xuICAgIH1cbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBET00gZXZlbnRzIGZvciB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIG1ldGhvZCBpbXBsZW1lbnRzIHRoZSBET00gYEV2ZW50TGlzdGVuZXJgIGludGVyZmFjZSBhbmQgaXNcbiAgICogY2FsbGVkIGluIHJlc3BvbnNlIHRvIGV2ZW50cyBvbiB0aGUgZG9jayBwYW5lbCdzIG5vZGUuIEl0IHNob3VsZFxuICAgKiBub3QgYmUgY2FsbGVkIGRpcmVjdGx5IGJ5IHVzZXIgY29kZS5cbiAgICovXG4gIGhhbmRsZUV2ZW50KGV2ZW50OiBFdmVudCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzSGlkZGVuIHx8IHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IHsgbm9kZSB9ID0gdGhpcztcbiAgICBjb25zdCB0YXJnZXQgPSBldmVudC50YXJnZXQgYXMgSFRNTEVsZW1lbnQ7XG5cbiAgICBzd2l0Y2ggKGV2ZW50LnR5cGUpIHtcbiAgICAgIGNhc2UgJ2tleWRvd24nOlxuICAgICAgICBpZiAobm9kZS5jb250YWlucyh0YXJnZXQpKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuZGlzcG9zZSgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ21vdXNlZG93bic6XG4gICAgICAgIGlmIChub2RlLmNvbnRhaW5zKHRhcmdldCkpIHtcbiAgICAgICAgICB0aGlzLmFjdGl2YXRlKCk7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuZGlzcG9zZSgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3Njcm9sbCc6XG4gICAgICAgIHRoaXMuX2V2dFNjcm9sbChldmVudCBhcyBNb3VzZUV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAnYWN0aXZhdGUtcmVxdWVzdCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWN0aXZhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHRoaXMubm9kZS50YWJJbmRleCA9IDA7XG4gICAgdGhpcy5ub2RlLmZvY3VzKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAnYWZ0ZXItYXR0YWNoJ2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBkb2N1bWVudC5ib2R5LmNsYXNzTGlzdC5hZGQoQk9EWV9DTEFTUyk7XG4gICAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIHRoaXMsIFVTRV9DQVBUVVJFKTtcbiAgICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzLCBVU0VfQ0FQVFVSRSk7XG4gICAgdGhpcy5hbmNob3Iubm9kZS5hZGRFdmVudExpc3RlbmVyKCdzY3JvbGwnLCB0aGlzLCBVU0VfQ0FQVFVSRSk7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGJlZm9yZS1kZXRhY2hgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQmVmb3JlRGV0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGRvY3VtZW50LmJvZHkuY2xhc3NMaXN0LnJlbW92ZShCT0RZX0NMQVNTKTtcbiAgICBkb2N1bWVudC5yZW1vdmVFdmVudExpc3RlbmVyKCdrZXlkb3duJywgdGhpcywgVVNFX0NBUFRVUkUpO1xuICAgIGRvY3VtZW50LnJlbW92ZUV2ZW50TGlzdGVuZXIoJ21vdXNlZG93bicsIHRoaXMsIFVTRV9DQVBUVVJFKTtcbiAgICB0aGlzLmFuY2hvci5ub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ3Njcm9sbCcsIHRoaXMsIFVTRV9DQVBUVVJFKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCd1cGRhdGUtcmVxdWVzdCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uVXBkYXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0hpZGRlbikge1xuICAgICAgdGhpcy5zaG93KCk7XG4gICAgfVxuICAgIHRoaXMuX3NldEdlb21ldHJ5KCk7XG4gICAgc3VwZXIub25VcGRhdGVSZXF1ZXN0KG1zZyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHNjcm9sbCBldmVudHMgZm9yIHRoZSB3aWRnZXRcbiAgICovXG4gIHByaXZhdGUgX2V2dFNjcm9sbChldmVudDogTW91c2VFdmVudCkge1xuICAgIC8vIEFsbCBzY3JvbGxzIGV4Y2VwdCBzY3JvbGxzIGluIHRoZSBhY3R1YWwgaG92ZXIgYm94IG5vZGUgbWF5IGNhdXNlIHRoZVxuICAgIC8vIHJlZmVyZW50IGVkaXRvciB0aGF0IGFuY2hvcnMgdGhlIG5vZGUgdG8gbW92ZSwgc28gdGhlIG9ubHkgc2Nyb2xsIGV2ZW50c1xuICAgIC8vIHRoYXQgY2FuIHNhZmVseSBiZSBpZ25vcmVkIGFyZSBvbmVzIHRoYXQgaGFwcGVuIGluc2lkZSB0aGUgaG92ZXJpbmcgbm9kZS5cbiAgICBpZiAodGhpcy5ub2RlLmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBIVE1MRWxlbWVudCkpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEZpbmQgdGhlIHBvc2l0aW9uIG9mIHRoZSBmaXJzdCBjaGFyYWN0ZXIgb2YgdGhlIGN1cnJlbnQgdG9rZW4uXG4gICAqL1xuICBwcml2YXRlIF9nZXRUb2tlblBvc2l0aW9uKCk6IENvZGVFZGl0b3IuSVBvc2l0aW9uIHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCBlZGl0b3IgPSB0aGlzLl9lZGl0b3I7XG4gICAgY29uc3QgY3Vyc29yID0gZWRpdG9yLmdldEN1cnNvclBvc2l0aW9uKCk7XG4gICAgY29uc3QgZW5kID0gZWRpdG9yLmdldE9mZnNldEF0KGN1cnNvcik7XG4gICAgY29uc3QgbGluZSA9IGVkaXRvci5nZXRMaW5lKGN1cnNvci5saW5lKTtcblxuICAgIGlmICghbGluZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IHRva2VucyA9IGxpbmUuc3Vic3RyaW5nKDAsIGVuZCkuc3BsaXQoL1xcVysvKTtcbiAgICBjb25zdCBsYXN0ID0gdG9rZW5zW3Rva2Vucy5sZW5ndGggLSAxXTtcbiAgICBjb25zdCBzdGFydCA9IGxhc3QgPyBlbmQgLSBsYXN0Lmxlbmd0aCA6IGVuZDtcbiAgICByZXR1cm4gZWRpdG9yLmdldFBvc2l0aW9uQXQoc3RhcnQpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgZ2VvbWV0cnkgb2YgdGhlIHRvb2x0aXAgd2lkZ2V0LlxuICAgKi9cbiAgcHJpdmF0ZSBfc2V0R2VvbWV0cnkoKTogdm9pZCB7XG4gICAgLy8gZGV0ZXJtaW5lIHBvc2l0aW9uIGZvciBob3ZlciBib3ggcGxhY2VtZW50XG4gICAgY29uc3QgcG9zaXRpb24gPSB0aGlzLl9wb3NpdGlvbiA/IHRoaXMuX3Bvc2l0aW9uIDogdGhpcy5fZ2V0VG9rZW5Qb3NpdGlvbigpO1xuXG4gICAgaWYgKCFwb3NpdGlvbikge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IGVkaXRvciA9IHRoaXMuX2VkaXRvcjtcblxuICAgIGNvbnN0IGFuY2hvciA9IGVkaXRvci5nZXRDb29yZGluYXRlRm9yUG9zaXRpb24ocG9zaXRpb24pIGFzIENsaWVudFJlY3Q7XG4gICAgY29uc3Qgc3R5bGUgPSB3aW5kb3cuZ2V0Q29tcHV0ZWRTdHlsZSh0aGlzLm5vZGUpO1xuICAgIGNvbnN0IHBhZGRpbmdMZWZ0ID0gcGFyc2VJbnQoc3R5bGUucGFkZGluZ0xlZnQhLCAxMCkgfHwgMDtcblxuICAgIC8vIENhbGN1bGF0ZSB0aGUgZ2VvbWV0cnkgb2YgdGhlIHRvb2x0aXAuXG4gICAgSG92ZXJCb3guc2V0R2VvbWV0cnkoe1xuICAgICAgYW5jaG9yLFxuICAgICAgaG9zdDogZWRpdG9yLmhvc3QsXG4gICAgICBtYXhIZWlnaHQ6IE1BWF9IRUlHSFQsXG4gICAgICBtaW5IZWlnaHQ6IE1JTl9IRUlHSFQsXG4gICAgICBub2RlOiB0aGlzLm5vZGUsXG4gICAgICBvZmZzZXQ6IHsgaG9yaXpvbnRhbDogLTEgKiBwYWRkaW5nTGVmdCB9LFxuICAgICAgcHJpdmlsZWdlOiAnYmVsb3cnLFxuICAgICAgc3R5bGU6IHN0eWxlXG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9jb250ZW50OiBJUmVuZGVyTWltZS5JUmVuZGVyZXIgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3I7XG4gIHByaXZhdGUgX3Bvc2l0aW9uOiBDb2RlRWRpdG9yLklQb3NpdGlvbiB8IHVuZGVmaW5lZDtcbiAgcHJpdmF0ZSBfcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgdG9vbHRpcCB3aWRnZXQgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBUb29sdGlwIHtcbiAgLyoqXG4gICAqIEluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgYSB0b29sdGlwIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBhbmNob3Igd2lkZ2V0IHRoYXQgdGhlIHRvb2x0aXAgd2lkZ2V0IHRyYWNrcy5cbiAgICAgKi9cbiAgICBhbmNob3I6IFdpZGdldDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBkYXRhIHRoYXQgcG9wdWxhdGVzIHRoZSB0b29sdGlwIHdpZGdldC5cbiAgICAgKi9cbiAgICBidW5kbGU6IEpTT05PYmplY3Q7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZWRpdG9yIHJlZmVyZW50IG9mIHRoZSB0b29sdGlwIG1vZGVsLlxuICAgICAqL1xuICAgIGVkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJlbmRlcm1pbWUgaW5zdGFuY2UgdXNlZCBieSB0aGUgdG9vbHRpcCBtb2RlbC5cbiAgICAgKi9cbiAgICByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogUG9zaXRpb24gYXQgd2hpY2ggdGhlIHRvb2x0aXAgc2hvdWxkIGJlIHBsYWNlZC5cbiAgICAgKlxuICAgICAqIElmIG5vdCBnaXZlbiwgdGhlIHBvc2l0aW9uIG9mIHRoZSBmaXJzdCBjaGFyYWN0ZXJcbiAgICAgKiBpbiB0aGUgY3VycmVudCB0b2tlbiB3aWxsIGJlIHVzZWQuXG4gICAgICovXG4gICAgcG9zaXRpb24/OiBDb2RlRWRpdG9yLklQb3NpdGlvbjtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==