(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_vdom_lib_index_js"],{

/***/ "../packages/vdom/lib/index.js":
/*!*************************************!*\
  !*** ../packages/vdom/lib/index.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IVDOMTracker": () => (/* binding */ IVDOMTracker),
/* harmony export */   "RenderedVDOM": () => (/* binding */ RenderedVDOM)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _nteract_transform_vdom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @nteract/transform-vdom */ "../node_modules/@nteract/transform-vdom/lib/index.js");
/* harmony import */ var _nteract_transform_vdom__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_nteract_transform_vdom__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module vdom
 */





/**
 * The CSS class to add to the VDOM Widget.
 */
const CSS_CLASS = 'jp-RenderedVDOM';
/**
 * The VDOM tracker token.
 */
const IVDOMTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/vdom:IVDOMTracker');
/**
 * A renderer for declarative virtual DOM content.
 */
class RenderedVDOM extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
     * Create a new widget for rendering DOM.
     */
    constructor(options, context) {
        super();
        /**
         * Handle events for VDOM element.
         */
        this.handleVDOMEvent = (targetName, event) => {
            var _a, _b;
            // When a VDOM element's event handler is called, send a serialized
            // representation of the event to the registered comm channel for the
            // kernel to handle
            if (this._timer) {
                window.clearTimeout(this._timer);
            }
            const kernel = (_b = (_a = this._sessionContext) === null || _a === void 0 ? void 0 : _a.session) === null || _b === void 0 ? void 0 : _b.kernel;
            if (kernel) {
                this._timer = window.setTimeout(() => {
                    if (!this._comms[targetName]) {
                        this._comms[targetName] = kernel.createComm(targetName);
                        this._comms[targetName].open();
                    }
                    this._comms[targetName].send(JSON.stringify(event));
                }, 16);
            }
        };
        this._comms = {};
        this.addClass(CSS_CLASS);
        this.addClass('jp-RenderedHTML');
        this.addClass('jp-RenderedHTMLCommon');
        this._mimeType = options.mimeType;
        if (context) {
            this._sessionContext = context.sessionContext;
        }
    }
    /**
     * Dispose of the widget.
     */
    dispose() {
        // Dispose of comm disposables
        for (const targetName in this._comms) {
            this._comms[targetName].dispose();
        }
        super.dispose();
    }
    /**
     * Called before the widget is detached from the DOM.
     */
    onBeforeDetach(msg) {
        // Dispose of React component(s).
        react_dom__WEBPACK_IMPORTED_MODULE_4__.unmountComponentAtNode(this.node);
    }
    /**
     * Render VDOM into this widget's node.
     */
    renderModel(model) {
        return new Promise((resolve, reject) => {
            const data = model.data[this._mimeType];
            react_dom__WEBPACK_IMPORTED_MODULE_4__.render(react__WEBPACK_IMPORTED_MODULE_3__.createElement((_nteract_transform_vdom__WEBPACK_IMPORTED_MODULE_2___default()), { data: data, onVDOMEvent: this.handleVDOMEvent }), this.node, () => {
                resolve();
            });
        });
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdmRvbS9zcmMvaW5kZXgudHN4Il0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTXVDO0FBRUQ7QUFDdUI7QUFDakM7QUFDTztBQUV0Qzs7R0FFRztBQUNILE1BQU0sU0FBUyxHQUFHLGlCQUFpQixDQUFDO0FBT3BDOztHQUVHO0FBQ0ksTUFBTSxZQUFZLEdBQUcsSUFBSSxvREFBSyxDQUNuQywrQkFBK0IsQ0FDaEMsQ0FBQztBQUVGOztHQUVHO0FBQ0ksTUFBTSxZQUFhLFNBQVEsbURBQU07SUFDdEM7O09BRUc7SUFDSCxZQUNFLE9BQXFDLEVBQ3JDLE9BQTREO1FBRTVELEtBQUssRUFBRSxDQUFDO1FBNkNWOztXQUVHO1FBQ0gsb0JBQWUsR0FBRyxDQUFDLFVBQWtCLEVBQUUsS0FBMkIsRUFBUSxFQUFFOztZQUMxRSxtRUFBbUU7WUFDbkUscUVBQXFFO1lBQ3JFLG1CQUFtQjtZQUNuQixJQUFJLElBQUksQ0FBQyxNQUFNLEVBQUU7Z0JBQ2YsTUFBTSxDQUFDLFlBQVksQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLENBQUM7YUFDbEM7WUFDRCxNQUFNLE1BQU0sZUFBRyxJQUFJLENBQUMsZUFBZSwwQ0FBRSxPQUFPLDBDQUFFLE1BQU0sQ0FBQztZQUNyRCxJQUFJLE1BQU0sRUFBRTtnQkFDVixJQUFJLENBQUMsTUFBTSxHQUFHLE1BQU0sQ0FBQyxVQUFVLENBQUMsR0FBRyxFQUFFO29CQUNuQyxJQUFJLENBQUMsSUFBSSxDQUFDLE1BQU0sQ0FBQyxVQUFVLENBQUMsRUFBRTt3QkFDNUIsSUFBSSxDQUFDLE1BQU0sQ0FBQyxVQUFVLENBQUMsR0FBRyxNQUFNLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxDQUFDO3dCQUN4RCxJQUFJLENBQUMsTUFBTSxDQUFDLFVBQVUsQ0FBQyxDQUFDLElBQUksRUFBRSxDQUFDO3FCQUNoQztvQkFDRCxJQUFJLENBQUMsTUFBTSxDQUFDLFVBQVUsQ0FBQyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUM7Z0JBQ3RELENBQUMsRUFBRSxFQUFFLENBQUMsQ0FBQzthQUNSO1FBQ0gsQ0FBQyxDQUFDO1FBSU0sV0FBTSxHQUEyQyxFQUFFLENBQUM7UUFwRTFELElBQUksQ0FBQyxRQUFRLENBQUMsU0FBUyxDQUFDLENBQUM7UUFDekIsSUFBSSxDQUFDLFFBQVEsQ0FBQyxpQkFBaUIsQ0FBQyxDQUFDO1FBQ2pDLElBQUksQ0FBQyxRQUFRLENBQUMsdUJBQXVCLENBQUMsQ0FBQztRQUN2QyxJQUFJLENBQUMsU0FBUyxHQUFHLE9BQU8sQ0FBQyxRQUFRLENBQUM7UUFDbEMsSUFBSSxPQUFPLEVBQUU7WUFDWCxJQUFJLENBQUMsZUFBZSxHQUFHLE9BQU8sQ0FBQyxjQUFjLENBQUM7U0FDL0M7SUFDSCxDQUFDO0lBRUQ7O09BRUc7SUFDSCxPQUFPO1FBQ0wsOEJBQThCO1FBQzlCLEtBQUssTUFBTSxVQUFVLElBQUksSUFBSSxDQUFDLE1BQU0sRUFBRTtZQUNwQyxJQUFJLENBQUMsTUFBTSxDQUFDLFVBQVUsQ0FBQyxDQUFDLE9BQU8sRUFBRSxDQUFDO1NBQ25DO1FBQ0QsS0FBSyxDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQ2xCLENBQUM7SUFFRDs7T0FFRztJQUNPLGNBQWMsQ0FBQyxHQUFZO1FBQ25DLGlDQUFpQztRQUNqQyw2REFBK0IsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDN0MsQ0FBQztJQUVEOztPQUVHO0lBQ0gsV0FBVyxDQUFDLEtBQTZCO1FBQ3ZDLE9BQU8sSUFBSSxPQUFPLENBQUMsQ0FBQyxPQUFPLEVBQUUsTUFBTSxFQUFFLEVBQUU7WUFDckMsTUFBTSxJQUFJLEdBQUcsS0FBSyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFRLENBQUM7WUFDL0MsNkNBQWUsQ0FDYixpREFBQyxnRUFBSSxJQUFDLElBQUksRUFBRSxJQUFJLEVBQUUsV0FBVyxFQUFFLElBQUksQ0FBQyxlQUFlLEdBQUksRUFDdkQsSUFBSSxDQUFDLElBQUksRUFDVCxHQUFHLEVBQUU7Z0JBQ0gsT0FBTyxFQUFFLENBQUM7WUFDWixDQUFDLENBQ0YsQ0FBQztRQUNKLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztDQTRCRiIsImZpbGUiOiJwYWNrYWdlc192ZG9tX2xpYl9pbmRleF9qcy5lMzE5MzFmNmU5NWEzNDQwNGE1Ni5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHZkb21cbiAqL1xuXG5pbXBvcnQgeyBJU2Vzc2lvbkNvbnRleHQsIElXaWRnZXRUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgRG9jdW1lbnRSZWdpc3RyeSwgTWltZURvY3VtZW50IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgSVJlbmRlck1pbWUgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lLWludGVyZmFjZXMnO1xuaW1wb3J0IHsgS2VybmVsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCBWRE9NLCB7IFNlcmlhbGl6ZWRFdmVudCB9IGZyb20gJ0BudGVyYWN0L3RyYW5zZm9ybS12ZG9tJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCAqIGFzIFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7XG5cbi8qKlxuICogVGhlIENTUyBjbGFzcyB0byBhZGQgdG8gdGhlIFZET00gV2lkZ2V0LlxuICovXG5jb25zdCBDU1NfQ0xBU1MgPSAnanAtUmVuZGVyZWRWRE9NJztcblxuLyoqXG4gKiBBIGNsYXNzIHRoYXQgdHJhY2tzIFZET00gd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJVkRPTVRyYWNrZXIgZXh0ZW5kcyBJV2lkZ2V0VHJhY2tlcjxNaW1lRG9jdW1lbnQ+IHt9XG5cbi8qKlxuICogVGhlIFZET00gdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElWRE9NVHJhY2tlciA9IG5ldyBUb2tlbjxJVkRPTVRyYWNrZXI+KFxuICAnQGp1cHl0ZXJsYWIvdmRvbTpJVkRPTVRyYWNrZXInXG4pO1xuXG4vKipcbiAqIEEgcmVuZGVyZXIgZm9yIGRlY2xhcmF0aXZlIHZpcnR1YWwgRE9NIGNvbnRlbnQuXG4gKi9cbmV4cG9ydCBjbGFzcyBSZW5kZXJlZFZET00gZXh0ZW5kcyBXaWRnZXQgaW1wbGVtZW50cyBJUmVuZGVyTWltZS5JUmVuZGVyZXIge1xuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHdpZGdldCBmb3IgcmVuZGVyaW5nIERPTS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKFxuICAgIG9wdGlvbnM6IElSZW5kZXJNaW1lLklSZW5kZXJlck9wdGlvbnMsXG4gICAgY29udGV4dD86IERvY3VtZW50UmVnaXN0cnkuSUNvbnRleHQ8RG9jdW1lbnRSZWdpc3RyeS5JTW9kZWw+XG4gICkge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcyhDU1NfQ0xBU1MpO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLVJlbmRlcmVkSFRNTCcpO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLVJlbmRlcmVkSFRNTENvbW1vbicpO1xuICAgIHRoaXMuX21pbWVUeXBlID0gb3B0aW9ucy5taW1lVHlwZTtcbiAgICBpZiAoY29udGV4dCkge1xuICAgICAgdGhpcy5fc2Vzc2lvbkNvbnRleHQgPSBjb250ZXh0LnNlc3Npb25Db250ZXh0O1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSB3aWRnZXQuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIC8vIERpc3Bvc2Ugb2YgY29tbSBkaXNwb3NhYmxlc1xuICAgIGZvciAoY29uc3QgdGFyZ2V0TmFtZSBpbiB0aGlzLl9jb21tcykge1xuICAgICAgdGhpcy5fY29tbXNbdGFyZ2V0TmFtZV0uZGlzcG9zZSgpO1xuICAgIH1cbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogQ2FsbGVkIGJlZm9yZSB0aGUgd2lkZ2V0IGlzIGRldGFjaGVkIGZyb20gdGhlIERPTS5cbiAgICovXG4gIHByb3RlY3RlZCBvbkJlZm9yZURldGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICAvLyBEaXNwb3NlIG9mIFJlYWN0IGNvbXBvbmVudChzKS5cbiAgICBSZWFjdERPTS51bm1vdW50Q29tcG9uZW50QXROb2RlKHRoaXMubm9kZSk7XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIFZET00gaW50byB0aGlzIHdpZGdldCdzIG5vZGUuXG4gICAqL1xuICByZW5kZXJNb2RlbChtb2RlbDogSVJlbmRlck1pbWUuSU1pbWVNb2RlbCk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICBjb25zdCBkYXRhID0gbW9kZWwuZGF0YVt0aGlzLl9taW1lVHlwZV0gYXMgYW55O1xuICAgICAgUmVhY3RET00ucmVuZGVyKFxuICAgICAgICA8VkRPTSBkYXRhPXtkYXRhfSBvblZET01FdmVudD17dGhpcy5oYW5kbGVWRE9NRXZlbnR9IC8+LFxuICAgICAgICB0aGlzLm5vZGUsXG4gICAgICAgICgpID0+IHtcbiAgICAgICAgICByZXNvbHZlKCk7XG4gICAgICAgIH1cbiAgICAgICk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGV2ZW50cyBmb3IgVkRPTSBlbGVtZW50LlxuICAgKi9cbiAgaGFuZGxlVkRPTUV2ZW50ID0gKHRhcmdldE5hbWU6IHN0cmluZywgZXZlbnQ6IFNlcmlhbGl6ZWRFdmVudDxhbnk+KTogdm9pZCA9PiB7XG4gICAgLy8gV2hlbiBhIFZET00gZWxlbWVudCdzIGV2ZW50IGhhbmRsZXIgaXMgY2FsbGVkLCBzZW5kIGEgc2VyaWFsaXplZFxuICAgIC8vIHJlcHJlc2VudGF0aW9uIG9mIHRoZSBldmVudCB0byB0aGUgcmVnaXN0ZXJlZCBjb21tIGNoYW5uZWwgZm9yIHRoZVxuICAgIC8vIGtlcm5lbCB0byBoYW5kbGVcbiAgICBpZiAodGhpcy5fdGltZXIpIHtcbiAgICAgIHdpbmRvdy5jbGVhclRpbWVvdXQodGhpcy5fdGltZXIpO1xuICAgIH1cbiAgICBjb25zdCBrZXJuZWwgPSB0aGlzLl9zZXNzaW9uQ29udGV4dD8uc2Vzc2lvbj8ua2VybmVsO1xuICAgIGlmIChrZXJuZWwpIHtcbiAgICAgIHRoaXMuX3RpbWVyID0gd2luZG93LnNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgICBpZiAoIXRoaXMuX2NvbW1zW3RhcmdldE5hbWVdKSB7XG4gICAgICAgICAgdGhpcy5fY29tbXNbdGFyZ2V0TmFtZV0gPSBrZXJuZWwuY3JlYXRlQ29tbSh0YXJnZXROYW1lKTtcbiAgICAgICAgICB0aGlzLl9jb21tc1t0YXJnZXROYW1lXS5vcGVuKCk7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5fY29tbXNbdGFyZ2V0TmFtZV0uc2VuZChKU09OLnN0cmluZ2lmeShldmVudCkpO1xuICAgICAgfSwgMTYpO1xuICAgIH1cbiAgfTtcblxuICBwcml2YXRlIF9taW1lVHlwZTogc3RyaW5nO1xuICBwcml2YXRlIF9zZXNzaW9uQ29udGV4dD86IElTZXNzaW9uQ29udGV4dDtcbiAgcHJpdmF0ZSBfY29tbXM6IHsgW3RhcmdldE5hbWU6IHN0cmluZ106IEtlcm5lbC5JQ29tbSB9ID0ge307XG4gIHByaXZhdGUgX3RpbWVyOiBudW1iZXI7XG59XG4iXSwic291cmNlUm9vdCI6IiJ9