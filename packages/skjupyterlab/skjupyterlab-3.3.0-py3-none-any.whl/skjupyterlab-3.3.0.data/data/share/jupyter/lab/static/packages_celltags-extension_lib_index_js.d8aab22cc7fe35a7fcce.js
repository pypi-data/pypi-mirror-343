(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_celltags-extension_lib_index_js"],{

/***/ "../packages/celltags-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/celltags-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_celltags__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/celltags */ "webpack/sharing/consume/default/@jupyterlab/celltags/@jupyterlab/celltags");
/* harmony import */ var _jupyterlab_celltags__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_celltags__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module celltags-extension
 */



/**
 * Initialization data for the celltags extension.
 */
const celltags = {
    id: '@jupyterlab/celltags',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTools, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator],
    activate: (app, tools, tracker, translator) => {
        const tool = new _jupyterlab_celltags__WEBPACK_IMPORTED_MODULE_1__.TagTool(tracker, app, translator);
        tools.addItem({ tool: tool, rank: 1.6 });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (celltags);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY2VsbHRhZ3MtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFPcUU7QUFFekI7QUFFTztBQUV0RDs7R0FFRztBQUNILE1BQU0sUUFBUSxHQUFnQztJQUM1QyxFQUFFLEVBQUUsc0JBQXNCO0lBQzFCLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQUMsZ0VBQWMsRUFBRSxrRUFBZ0IsRUFBRSxnRUFBVyxDQUFDO0lBQ3pELFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLEtBQXFCLEVBQ3JCLE9BQXlCLEVBQ3pCLFVBQXVCLEVBQ3ZCLEVBQUU7UUFDRixNQUFNLElBQUksR0FBRyxJQUFJLHlEQUFPLENBQUMsT0FBTyxFQUFFLEdBQUcsRUFBRSxVQUFVLENBQUMsQ0FBQztRQUNuRCxLQUFLLENBQUMsT0FBTyxDQUFDLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxJQUFJLEVBQUUsR0FBRyxFQUFFLENBQUMsQ0FBQztJQUMzQyxDQUFDO0NBQ0YsQ0FBQztBQUVGLGlFQUFlLFFBQVEsRUFBQyIsImZpbGUiOiJwYWNrYWdlc19jZWxsdGFncy1leHRlbnNpb25fbGliX2luZGV4X2pzLmQ4YWFiMjJjYzdmZTM1YTdmY2NlLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY2VsbHRhZ3MtZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuXG5pbXBvcnQgeyBJTm90ZWJvb2tUb29scywgSU5vdGVib29rVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcblxuaW1wb3J0IHsgVGFnVG9vbCB9IGZyb20gJ0BqdXB5dGVybGFiL2NlbGx0YWdzJztcblxuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbi8qKlxuICogSW5pdGlhbGl6YXRpb24gZGF0YSBmb3IgdGhlIGNlbGx0YWdzIGV4dGVuc2lvbi5cbiAqL1xuY29uc3QgY2VsbHRhZ3M6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9jZWxsdGFncycsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJTm90ZWJvb2tUb29scywgSU5vdGVib29rVHJhY2tlciwgSVRyYW5zbGF0b3JdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHRvb2xzOiBJTm90ZWJvb2tUb29scyxcbiAgICB0cmFja2VyOiBJTm90ZWJvb2tUcmFja2VyLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICkgPT4ge1xuICAgIGNvbnN0IHRvb2wgPSBuZXcgVGFnVG9vbCh0cmFja2VyLCBhcHAsIHRyYW5zbGF0b3IpO1xuICAgIHRvb2xzLmFkZEl0ZW0oeyB0b29sOiB0b29sLCByYW5rOiAxLjYgfSk7XG4gIH1cbn07XG5cbmV4cG9ydCBkZWZhdWx0IGNlbGx0YWdzO1xuIl0sInNvdXJjZVJvb3QiOiIifQ==