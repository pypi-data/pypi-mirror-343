(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_mathjax2-extension_lib_index_js-_1d6d1"],{

/***/ "../packages/mathjax2-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/mathjax2-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_mathjax2__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/mathjax2 */ "webpack/sharing/consume/default/@jupyterlab/mathjax2/@jupyterlab/mathjax2");
/* harmony import */ var _jupyterlab_mathjax2__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mathjax2__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module mathjax2-extension
 */



/**
 * The MathJax latexTypesetter plugin.
 */
const plugin = {
    id: '@jupyterlab/mathjax2-extension:plugin',
    autoStart: true,
    provides: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.ILatexTypesetter,
    activate: () => {
        const [urlParam, configParam] = ['fullMathjaxUrl', 'mathjaxConfig'];
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption(urlParam);
        const config = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption(configParam);
        if (!url) {
            const message = `${plugin.id} uses '${urlParam}' and '${configParam}' in PageConfig ` +
                `to operate but '${urlParam}' was not found.`;
            throw new Error(message);
        }
        return new _jupyterlab_mathjax2__WEBPACK_IMPORTED_MODULE_1__.MathJaxTypesetter({ url, config });
    }
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWF0aGpheDItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBR2dEO0FBQ007QUFDQztBQUUxRDs7R0FFRztBQUNILE1BQU0sTUFBTSxHQUE0QztJQUN0RCxFQUFFLEVBQUUsdUNBQXVDO0lBQzNDLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLG9FQUFnQjtJQUMxQixRQUFRLEVBQUUsR0FBRyxFQUFFO1FBQ2IsTUFBTSxDQUFDLFFBQVEsRUFBRSxXQUFXLENBQUMsR0FBRyxDQUFDLGdCQUFnQixFQUFFLGVBQWUsQ0FBQyxDQUFDO1FBQ3BFLE1BQU0sR0FBRyxHQUFHLHVFQUFvQixDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBQzNDLE1BQU0sTUFBTSxHQUFHLHVFQUFvQixDQUFDLFdBQVcsQ0FBQyxDQUFDO1FBRWpELElBQUksQ0FBQyxHQUFHLEVBQUU7WUFDUixNQUFNLE9BQU8sR0FDWCxHQUFHLE1BQU0sQ0FBQyxFQUFFLFVBQVUsUUFBUSxVQUFVLFdBQVcsa0JBQWtCO2dCQUNyRSxtQkFBbUIsUUFBUSxrQkFBa0IsQ0FBQztZQUVoRCxNQUFNLElBQUksS0FBSyxDQUFDLE9BQU8sQ0FBQyxDQUFDO1NBQzFCO1FBRUQsT0FBTyxJQUFJLG1FQUFpQixDQUFDLEVBQUUsR0FBRyxFQUFFLE1BQU0sRUFBRSxDQUFDLENBQUM7SUFDaEQsQ0FBQztDQUNGLENBQUM7QUFFRjs7R0FFRztBQUNILGlFQUFlLE1BQU0sRUFBQyIsImZpbGUiOiJwYWNrYWdlc19tYXRoamF4Mi1leHRlbnNpb25fbGliX2luZGV4X2pzLV8xZDZkMS5mMjRlZjczMmRlMTdjMTBhMGUwMi5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbWF0aGpheDItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHsgSnVweXRlckZyb250RW5kUGx1Z2luIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgUGFnZUNvbmZpZyB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBNYXRoSmF4VHlwZXNldHRlciB9IGZyb20gJ0BqdXB5dGVybGFiL21hdGhqYXgyJztcbmltcG9ydCB7IElMYXRleFR5cGVzZXR0ZXIgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcblxuLyoqXG4gKiBUaGUgTWF0aEpheCBsYXRleFR5cGVzZXR0ZXIgcGx1Z2luLlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTGF0ZXhUeXBlc2V0dGVyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9tYXRoamF4Mi1leHRlbnNpb246cGx1Z2luJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSUxhdGV4VHlwZXNldHRlcixcbiAgYWN0aXZhdGU6ICgpID0+IHtcbiAgICBjb25zdCBbdXJsUGFyYW0sIGNvbmZpZ1BhcmFtXSA9IFsnZnVsbE1hdGhqYXhVcmwnLCAnbWF0aGpheENvbmZpZyddO1xuICAgIGNvbnN0IHVybCA9IFBhZ2VDb25maWcuZ2V0T3B0aW9uKHVybFBhcmFtKTtcbiAgICBjb25zdCBjb25maWcgPSBQYWdlQ29uZmlnLmdldE9wdGlvbihjb25maWdQYXJhbSk7XG5cbiAgICBpZiAoIXVybCkge1xuICAgICAgY29uc3QgbWVzc2FnZSA9XG4gICAgICAgIGAke3BsdWdpbi5pZH0gdXNlcyAnJHt1cmxQYXJhbX0nIGFuZCAnJHtjb25maWdQYXJhbX0nIGluIFBhZ2VDb25maWcgYCArXG4gICAgICAgIGB0byBvcGVyYXRlIGJ1dCAnJHt1cmxQYXJhbX0nIHdhcyBub3QgZm91bmQuYDtcblxuICAgICAgdGhyb3cgbmV3IEVycm9yKG1lc3NhZ2UpO1xuICAgIH1cblxuICAgIHJldHVybiBuZXcgTWF0aEpheFR5cGVzZXR0ZXIoeyB1cmwsIGNvbmZpZyB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbiBhcyBkZWZhdWx0LlxuICovXG5leHBvcnQgZGVmYXVsdCBwbHVnaW47XG4iXSwic291cmNlUm9vdCI6IiJ9