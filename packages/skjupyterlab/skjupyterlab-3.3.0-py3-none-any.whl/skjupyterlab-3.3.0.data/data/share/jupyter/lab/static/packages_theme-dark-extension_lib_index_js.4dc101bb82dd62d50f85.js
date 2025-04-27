(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_theme-dark-extension_lib_index_js"],{

/***/ "../packages/theme-dark-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/theme-dark-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module theme-dark-extension
 */


/**
 * A plugin for the Jupyter Dark Theme.
 */
const plugin = {
    id: '@jupyterlab/theme-dark-extension:plugin',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.ITranslator],
    activate: (app, manager, translator) => {
        const trans = translator.load('jupyterlab');
        const style = '@jupyterlab/theme-dark-extension/index.css';
        manager.register({
            name: 'JupyterLab Dark',
            displayName: trans.__('JupyterLab Dark'),
            isLight: false,
            themeScrollbars: true,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    },
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdGhlbWUtZGFyay1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNa0Q7QUFDQztBQUV0RDs7R0FFRztBQUNILE1BQU0sTUFBTSxHQUFnQztJQUMxQyxFQUFFLEVBQUUseUNBQXlDO0lBQzdDLFFBQVEsRUFBRSxDQUFDLCtEQUFhLEVBQUUsZ0VBQVcsQ0FBQztJQUN0QyxRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixPQUFzQixFQUN0QixVQUF1QixFQUN2QixFQUFFO1FBQ0YsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztRQUM1QyxNQUFNLEtBQUssR0FBRyw0Q0FBNEMsQ0FBQztRQUMzRCxPQUFPLENBQUMsUUFBUSxDQUFDO1lBQ2YsSUFBSSxFQUFFLGlCQUFpQjtZQUN2QixXQUFXLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxpQkFBaUIsQ0FBQztZQUN4QyxPQUFPLEVBQUUsS0FBSztZQUNkLGVBQWUsRUFBRSxJQUFJO1lBQ3JCLElBQUksRUFBRSxHQUFHLEVBQUUsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQztZQUNsQyxNQUFNLEVBQUUsR0FBRyxFQUFFLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxTQUFTLENBQUM7U0FDekMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUNELFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRixpRUFBZSxNQUFNLEVBQUMiLCJmaWxlIjoicGFja2FnZXNfdGhlbWUtZGFyay1leHRlbnNpb25fbGliX2luZGV4X2pzLjRkYzEwMWJiODJkZDYyZDUwZjg1LmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdGhlbWUtZGFyay1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJVGhlbWVNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbi8qKlxuICogQSBwbHVnaW4gZm9yIHRoZSBKdXB5dGVyIERhcmsgVGhlbWUuXG4gKi9cbmNvbnN0IHBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL3RoZW1lLWRhcmstZXh0ZW5zaW9uOnBsdWdpbicsXG4gIHJlcXVpcmVzOiBbSVRoZW1lTWFuYWdlciwgSVRyYW5zbGF0b3JdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElUaGVtZU1hbmFnZXIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBzdHlsZSA9ICdAanVweXRlcmxhYi90aGVtZS1kYXJrLWV4dGVuc2lvbi9pbmRleC5jc3MnO1xuICAgIG1hbmFnZXIucmVnaXN0ZXIoe1xuICAgICAgbmFtZTogJ0p1cHl0ZXJMYWIgRGFyaycsXG4gICAgICBkaXNwbGF5TmFtZTogdHJhbnMuX18oJ0p1cHl0ZXJMYWIgRGFyaycpLFxuICAgICAgaXNMaWdodDogZmFsc2UsXG4gICAgICB0aGVtZVNjcm9sbGJhcnM6IHRydWUsXG4gICAgICBsb2FkOiAoKSA9PiBtYW5hZ2VyLmxvYWRDU1Moc3R5bGUpLFxuICAgICAgdW5sb2FkOiAoKSA9PiBQcm9taXNlLnJlc29sdmUodW5kZWZpbmVkKVxuICAgIH0pO1xuICB9LFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcbiJdLCJzb3VyY2VSb290IjoiIn0=