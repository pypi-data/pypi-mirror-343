(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_ui-components-extension_lib_index_js"],{

/***/ "../packages/ui-components-extension/lib/index.js":
/*!********************************************************!*\
  !*** ../packages/ui-components-extension/lib/index.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module ui-components-extension
 */

/**
 * Placeholder for future extension that will provide an icon manager class
 * to assist with overriding/replacing particular sets of icons
 */
const labiconManager = {
    id: '@jupyterlab/ui-components-extension:labicon-manager',
    provides: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ILabIconManager,
    autoStart: true,
    activate: (app) => {
        return Object.create(null);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (labiconManager);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdWktY29tcG9uZW50cy1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTXlEO0FBRTVEOzs7R0FHRztBQUNILE1BQU0sY0FBYyxHQUEyQztJQUM3RCxFQUFFLEVBQUUscURBQXFEO0lBQ3pELFFBQVEsRUFBRSxzRUFBZTtJQUN6QixTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxDQUFDLEdBQW9CLEVBQUUsRUFBRTtRQUNqQyxPQUFPLE1BQU0sQ0FBQyxNQUFNLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDN0IsQ0FBQztDQUNGLENBQUM7QUFFRixpRUFBZSxjQUFjLEVBQUMiLCJmaWxlIjoicGFja2FnZXNfdWktY29tcG9uZW50cy1leHRlbnNpb25fbGliX2luZGV4X2pzLjFlZWVmODEwNDA4ZjNjNDI5MWFkLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdWktY29tcG9uZW50cy1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJTGFiSWNvbk1hbmFnZXIgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcblxuLyoqXG4gKiBQbGFjZWhvbGRlciBmb3IgZnV0dXJlIGV4dGVuc2lvbiB0aGF0IHdpbGwgcHJvdmlkZSBhbiBpY29uIG1hbmFnZXIgY2xhc3NcbiAqIHRvIGFzc2lzdCB3aXRoIG92ZXJyaWRpbmcvcmVwbGFjaW5nIHBhcnRpY3VsYXIgc2V0cyBvZiBpY29uc1xuICovXG5jb25zdCBsYWJpY29uTWFuYWdlcjogSnVweXRlckZyb250RW5kUGx1Z2luPElMYWJJY29uTWFuYWdlcj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cy1leHRlbnNpb246bGFiaWNvbi1tYW5hZ2VyJyxcbiAgcHJvdmlkZXM6IElMYWJJY29uTWFuYWdlcixcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kKSA9PiB7XG4gICAgcmV0dXJuIE9iamVjdC5jcmVhdGUobnVsbCk7XG4gIH1cbn07XG5cbmV4cG9ydCBkZWZhdWx0IGxhYmljb25NYW5hZ2VyO1xuIl0sInNvdXJjZVJvb3QiOiIifQ==