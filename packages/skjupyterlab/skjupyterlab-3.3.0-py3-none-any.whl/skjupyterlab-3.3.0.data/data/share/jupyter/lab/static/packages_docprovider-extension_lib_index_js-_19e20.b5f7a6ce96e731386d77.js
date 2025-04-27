(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_docprovider-extension_lib_index_js-_19e20"],{

/***/ "../packages/docprovider-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/docprovider-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docprovider */ "webpack/sharing/consume/default/@jupyterlab/docprovider/@jupyterlab/docprovider");
/* harmony import */ var _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module docprovider-extension
 */



/**
 * The default document provider plugin
 */
const docProviderPlugin = {
    id: '@jupyterlab/docprovider-extension:plugin',
    provides: _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_1__.IDocumentProviderFactory,
    activate: (app) => {
        const server = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(server.wsUrl, 'api/yjs');
        const collaborative = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('collaborative') == 'true' ? true : false;
        const factory = (options) => {
            return collaborative
                ? new _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_1__.WebSocketProviderWithLocks(Object.assign(Object.assign({}, options), { url }))
                : new _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_1__.ProviderMock();
        };
        return factory;
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [docProviderPlugin];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jcHJvdmlkZXItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNd0Q7QUFNMUI7QUFDdUI7QUFFeEQ7O0dBRUc7QUFDSCxNQUFNLGlCQUFpQixHQUFvRDtJQUN6RSxFQUFFLEVBQUUsMENBQTBDO0lBQzlDLFFBQVEsRUFBRSw2RUFBd0I7SUFDbEMsUUFBUSxFQUFFLENBQUMsR0FBb0IsRUFBNEIsRUFBRTtRQUMzRCxNQUFNLE1BQU0sR0FBRywrRUFBNkIsRUFBRSxDQUFDO1FBQy9DLE1BQU0sR0FBRyxHQUFHLDhEQUFXLENBQUMsTUFBTSxDQUFDLEtBQUssRUFBRSxTQUFTLENBQUMsQ0FBQztRQUNqRCxNQUFNLGFBQWEsR0FDakIsdUVBQW9CLENBQUMsZUFBZSxDQUFDLElBQUksTUFBTSxDQUFDLENBQUMsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQztRQUNqRSxNQUFNLE9BQU8sR0FBRyxDQUNkLE9BQTBDLEVBQ3ZCLEVBQUU7WUFDckIsT0FBTyxhQUFhO2dCQUNsQixDQUFDLENBQUMsSUFBSSwrRUFBMEIsaUNBQ3pCLE9BQU8sS0FDVixHQUFHLElBQ0g7Z0JBQ0osQ0FBQyxDQUFDLElBQUksaUVBQVksRUFBRSxDQUFDO1FBQ3pCLENBQUMsQ0FBQztRQUNGLE9BQU8sT0FBTyxDQUFDO0lBQ2pCLENBQUM7Q0FDRixDQUFDO0FBRUY7O0dBRUc7QUFDSCxNQUFNLE9BQU8sR0FBaUMsQ0FBQyxpQkFBaUIsQ0FBQyxDQUFDO0FBQ2xFLGlFQUFlLE9BQU8sRUFBQyIsImZpbGUiOiJwYWNrYWdlc19kb2Nwcm92aWRlci1leHRlbnNpb25fbGliX2luZGV4X2pzLV8xOWUyMC5iNWY3YTZjZTk2ZTczMTM4NmQ3Ny5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGRvY3Byb3ZpZGVyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IFBhZ2VDb25maWcsIFVSTEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBJRG9jdW1lbnRQcm92aWRlcixcbiAgSURvY3VtZW50UHJvdmlkZXJGYWN0b3J5LFxuICBQcm92aWRlck1vY2ssXG4gIFdlYlNvY2tldFByb3ZpZGVyV2l0aExvY2tzXG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY3Byb3ZpZGVyJztcbmltcG9ydCB7IFNlcnZlckNvbm5lY3Rpb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgZG9jdW1lbnQgcHJvdmlkZXIgcGx1Z2luXG4gKi9cbmNvbnN0IGRvY1Byb3ZpZGVyUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SURvY3VtZW50UHJvdmlkZXJGYWN0b3J5PiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kb2Nwcm92aWRlci1leHRlbnNpb246cGx1Z2luJyxcbiAgcHJvdmlkZXM6IElEb2N1bWVudFByb3ZpZGVyRmFjdG9yeSxcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZCk6IElEb2N1bWVudFByb3ZpZGVyRmFjdG9yeSA9PiB7XG4gICAgY29uc3Qgc2VydmVyID0gU2VydmVyQ29ubmVjdGlvbi5tYWtlU2V0dGluZ3MoKTtcbiAgICBjb25zdCB1cmwgPSBVUkxFeHQuam9pbihzZXJ2ZXIud3NVcmwsICdhcGkveWpzJyk7XG4gICAgY29uc3QgY29sbGFib3JhdGl2ZSA9XG4gICAgICBQYWdlQ29uZmlnLmdldE9wdGlvbignY29sbGFib3JhdGl2ZScpID09ICd0cnVlJyA/IHRydWUgOiBmYWxzZTtcbiAgICBjb25zdCBmYWN0b3J5ID0gKFxuICAgICAgb3B0aW9uczogSURvY3VtZW50UHJvdmlkZXJGYWN0b3J5LklPcHRpb25zXG4gICAgKTogSURvY3VtZW50UHJvdmlkZXIgPT4ge1xuICAgICAgcmV0dXJuIGNvbGxhYm9yYXRpdmVcbiAgICAgICAgPyBuZXcgV2ViU29ja2V0UHJvdmlkZXJXaXRoTG9ja3Moe1xuICAgICAgICAgICAgLi4ub3B0aW9ucyxcbiAgICAgICAgICAgIHVybFxuICAgICAgICAgIH0pXG4gICAgICAgIDogbmV3IFByb3ZpZGVyTW9jaygpO1xuICAgIH07XG4gICAgcmV0dXJuIGZhY3Rvcnk7XG4gIH1cbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbZG9jUHJvdmlkZXJQbHVnaW5dO1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcbiJdLCJzb3VyY2VSb290IjoiIn0=