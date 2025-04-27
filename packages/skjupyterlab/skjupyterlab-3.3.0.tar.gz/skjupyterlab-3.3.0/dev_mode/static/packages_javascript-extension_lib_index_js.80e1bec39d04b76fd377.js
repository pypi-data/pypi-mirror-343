(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_javascript-extension_lib_index_js"],{

/***/ "../packages/javascript-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/javascript-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TEXT_JAVASCRIPT_MIMETYPE": () => (/* binding */ TEXT_JAVASCRIPT_MIMETYPE),
/* harmony export */   "APPLICATION_JAVASCRIPT_MIMETYPE": () => (/* binding */ APPLICATION_JAVASCRIPT_MIMETYPE),
/* harmony export */   "ExperimentalRenderedJavascript": () => (/* binding */ ExperimentalRenderedJavascript),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module javascript-extension
 */

const TEXT_JAVASCRIPT_MIMETYPE = 'text/javascript';
const APPLICATION_JAVASCRIPT_MIMETYPE = 'application/javascript';
function evalInContext(code, element, document, window) {
    // eslint-disable-next-line
    return eval(code);
}
class ExperimentalRenderedJavascript extends _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__.RenderedJavaScript {
    render(model) {
        const trans = this.translator.load('jupyterlab');
        const renderJavascript = () => {
            try {
                const data = model.data[this.mimeType];
                if (data) {
                    evalInContext(data, this.node, document, window);
                }
                return Promise.resolve();
            }
            catch (error) {
                return Promise.reject(error);
            }
        };
        if (!model.trusted) {
            // If output is not trusted or if arbitrary Javascript execution is not enabled, render an informative error message
            const pre = document.createElement('pre');
            pre.textContent = trans.__('Are you sure that you want to run arbitrary Javascript within your JupyterLab session?');
            const button = document.createElement('button');
            button.textContent = trans.__('Run');
            this.node.appendChild(pre);
            this.node.appendChild(button);
            button.onclick = event => {
                this.node.textContent = '';
                void renderJavascript();
            };
            return Promise.resolve();
        }
        return renderJavascript();
    }
}
/**
 * A mime renderer factory for text/javascript data.
 */
const rendererFactory = {
    safe: false,
    mimeTypes: [TEXT_JAVASCRIPT_MIMETYPE, APPLICATION_JAVASCRIPT_MIMETYPE],
    createRenderer: options => new ExperimentalRenderedJavascript(options)
};
const extension = {
    id: '@jupyterlab/javascript-extension:factory',
    rendererFactory,
    rank: 0,
    dataType: 'string'
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvamF2YXNjcmlwdC1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQUV5RDtBQUdyRCxNQUFNLHdCQUF3QixHQUFHLGlCQUFpQixDQUFDO0FBQ25ELE1BQU0sK0JBQStCLEdBQUcsd0JBQXdCLENBQUM7QUFFeEUsU0FBUyxhQUFhLENBQ3BCLElBQVksRUFDWixPQUFnQixFQUNoQixRQUFrQixFQUNsQixNQUFjO0lBRWQsMkJBQTJCO0lBQzNCLE9BQU8sSUFBSSxDQUFDLElBQUksQ0FBQyxDQUFDO0FBQ3BCLENBQUM7QUFFTSxNQUFNLDhCQUErQixTQUFRLHNFQUFrQjtJQUNwRSxNQUFNLENBQUMsS0FBNkI7UUFDbEMsTUFBTSxLQUFLLEdBQUcsSUFBSSxDQUFDLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7UUFDakQsTUFBTSxnQkFBZ0IsR0FBRyxHQUFHLEVBQUU7WUFDNUIsSUFBSTtnQkFDRixNQUFNLElBQUksR0FBRyxLQUFLLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQXVCLENBQUM7Z0JBQzdELElBQUksSUFBSSxFQUFFO29CQUNSLGFBQWEsQ0FBQyxJQUFJLEVBQUUsSUFBSSxDQUFDLElBQUksRUFBRSxRQUFRLEVBQUUsTUFBTSxDQUFDLENBQUM7aUJBQ2xEO2dCQUNELE9BQU8sT0FBTyxDQUFDLE9BQU8sRUFBRSxDQUFDO2FBQzFCO1lBQUMsT0FBTyxLQUFLLEVBQUU7Z0JBQ2QsT0FBTyxPQUFPLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxDQUFDO2FBQzlCO1FBQ0gsQ0FBQyxDQUFDO1FBQ0YsSUFBSSxDQUFDLEtBQUssQ0FBQyxPQUFPLEVBQUU7WUFDbEIsb0hBQW9IO1lBQ3BILE1BQU0sR0FBRyxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsS0FBSyxDQUFDLENBQUM7WUFDMUMsR0FBRyxDQUFDLFdBQVcsR0FBRyxLQUFLLENBQUMsRUFBRSxDQUN4Qix3RkFBd0YsQ0FDekYsQ0FBQztZQUNGLE1BQU0sTUFBTSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsUUFBUSxDQUFDLENBQUM7WUFDaEQsTUFBTSxDQUFDLFdBQVcsR0FBRyxLQUFLLENBQUMsRUFBRSxDQUFDLEtBQUssQ0FBQyxDQUFDO1lBRXJDLElBQUksQ0FBQyxJQUFJLENBQUMsV0FBVyxDQUFDLEdBQUcsQ0FBQyxDQUFDO1lBQzNCLElBQUksQ0FBQyxJQUFJLENBQUMsV0FBVyxDQUFDLE1BQU0sQ0FBQyxDQUFDO1lBRTlCLE1BQU0sQ0FBQyxPQUFPLEdBQUcsS0FBSyxDQUFDLEVBQUU7Z0JBQ3ZCLElBQUksQ0FBQyxJQUFJLENBQUMsV0FBVyxHQUFHLEVBQUUsQ0FBQztnQkFDM0IsS0FBSyxnQkFBZ0IsRUFBRSxDQUFDO1lBQzFCLENBQUMsQ0FBQztZQUNGLE9BQU8sT0FBTyxDQUFDLE9BQU8sRUFBRSxDQUFDO1NBQzFCO1FBQ0QsT0FBTyxnQkFBZ0IsRUFBRSxDQUFDO0lBQzVCLENBQUM7Q0FDRjtBQUVEOztHQUVHO0FBQ0ksTUFBTSxlQUFlLEdBQWlDO0lBQzNELElBQUksRUFBRSxLQUFLO0lBQ1gsU0FBUyxFQUFFLENBQUMsd0JBQXdCLEVBQUUsK0JBQStCLENBQUM7SUFDdEUsY0FBYyxFQUFFLE9BQU8sQ0FBQyxFQUFFLENBQUMsSUFBSSw4QkFBOEIsQ0FBQyxPQUFPLENBQUM7Q0FDdkUsQ0FBQztBQUVGLE1BQU0sU0FBUyxHQUEyQjtJQUN4QyxFQUFFLEVBQUUsMENBQTBDO0lBQzlDLGVBQWU7SUFDZixJQUFJLEVBQUUsQ0FBQztJQUNQLFFBQVEsRUFBRSxRQUFRO0NBQ25CLENBQUM7QUFFRixpRUFBZSxTQUFTLEVBQUMiLCJmaWxlIjoicGFja2FnZXNfamF2YXNjcmlwdC1leHRlbnNpb25fbGliX2luZGV4X2pzLjgwZTFiZWMzOWQwNGI3NmZkMzc3LmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgamF2YXNjcmlwdC1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQgeyBSZW5kZXJlZEphdmFTY3JpcHQgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IElSZW5kZXJNaW1lIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZS1pbnRlcmZhY2VzJztcblxuZXhwb3J0IGNvbnN0IFRFWFRfSkFWQVNDUklQVF9NSU1FVFlQRSA9ICd0ZXh0L2phdmFzY3JpcHQnO1xuZXhwb3J0IGNvbnN0IEFQUExJQ0FUSU9OX0pBVkFTQ1JJUFRfTUlNRVRZUEUgPSAnYXBwbGljYXRpb24vamF2YXNjcmlwdCc7XG5cbmZ1bmN0aW9uIGV2YWxJbkNvbnRleHQoXG4gIGNvZGU6IHN0cmluZyxcbiAgZWxlbWVudDogRWxlbWVudCxcbiAgZG9jdW1lbnQ6IERvY3VtZW50LFxuICB3aW5kb3c6IFdpbmRvd1xuKSB7XG4gIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZVxuICByZXR1cm4gZXZhbChjb2RlKTtcbn1cblxuZXhwb3J0IGNsYXNzIEV4cGVyaW1lbnRhbFJlbmRlcmVkSmF2YXNjcmlwdCBleHRlbmRzIFJlbmRlcmVkSmF2YVNjcmlwdCB7XG4gIHJlbmRlcihtb2RlbDogSVJlbmRlck1pbWUuSU1pbWVNb2RlbCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IHRyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCByZW5kZXJKYXZhc2NyaXB0ID0gKCkgPT4ge1xuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc3QgZGF0YSA9IG1vZGVsLmRhdGFbdGhpcy5taW1lVHlwZV0gYXMgc3RyaW5nIHwgdW5kZWZpbmVkO1xuICAgICAgICBpZiAoZGF0YSkge1xuICAgICAgICAgIGV2YWxJbkNvbnRleHQoZGF0YSwgdGhpcy5ub2RlLCBkb2N1bWVudCwgd2luZG93KTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKCk7XG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICByZXR1cm4gUHJvbWlzZS5yZWplY3QoZXJyb3IpO1xuICAgICAgfVxuICAgIH07XG4gICAgaWYgKCFtb2RlbC50cnVzdGVkKSB7XG4gICAgICAvLyBJZiBvdXRwdXQgaXMgbm90IHRydXN0ZWQgb3IgaWYgYXJiaXRyYXJ5IEphdmFzY3JpcHQgZXhlY3V0aW9uIGlzIG5vdCBlbmFibGVkLCByZW5kZXIgYW4gaW5mb3JtYXRpdmUgZXJyb3IgbWVzc2FnZVxuICAgICAgY29uc3QgcHJlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgncHJlJyk7XG4gICAgICBwcmUudGV4dENvbnRlbnQgPSB0cmFucy5fXyhcbiAgICAgICAgJ0FyZSB5b3Ugc3VyZSB0aGF0IHlvdSB3YW50IHRvIHJ1biBhcmJpdHJhcnkgSmF2YXNjcmlwdCB3aXRoaW4geW91ciBKdXB5dGVyTGFiIHNlc3Npb24/J1xuICAgICAgKTtcbiAgICAgIGNvbnN0IGJ1dHRvbiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2J1dHRvbicpO1xuICAgICAgYnV0dG9uLnRleHRDb250ZW50ID0gdHJhbnMuX18oJ1J1bicpO1xuXG4gICAgICB0aGlzLm5vZGUuYXBwZW5kQ2hpbGQocHJlKTtcbiAgICAgIHRoaXMubm9kZS5hcHBlbmRDaGlsZChidXR0b24pO1xuXG4gICAgICBidXR0b24ub25jbGljayA9IGV2ZW50ID0+IHtcbiAgICAgICAgdGhpcy5ub2RlLnRleHRDb250ZW50ID0gJyc7XG4gICAgICAgIHZvaWQgcmVuZGVySmF2YXNjcmlwdCgpO1xuICAgICAgfTtcbiAgICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUoKTtcbiAgICB9XG4gICAgcmV0dXJuIHJlbmRlckphdmFzY3JpcHQoKTtcbiAgfVxufVxuXG4vKipcbiAqIEEgbWltZSByZW5kZXJlciBmYWN0b3J5IGZvciB0ZXh0L2phdmFzY3JpcHQgZGF0YS5cbiAqL1xuZXhwb3J0IGNvbnN0IHJlbmRlcmVyRmFjdG9yeTogSVJlbmRlck1pbWUuSVJlbmRlcmVyRmFjdG9yeSA9IHtcbiAgc2FmZTogZmFsc2UsXG4gIG1pbWVUeXBlczogW1RFWFRfSkFWQVNDUklQVF9NSU1FVFlQRSwgQVBQTElDQVRJT05fSkFWQVNDUklQVF9NSU1FVFlQRV0sXG4gIGNyZWF0ZVJlbmRlcmVyOiBvcHRpb25zID0+IG5ldyBFeHBlcmltZW50YWxSZW5kZXJlZEphdmFzY3JpcHQob3B0aW9ucylcbn07XG5cbmNvbnN0IGV4dGVuc2lvbjogSVJlbmRlck1pbWUuSUV4dGVuc2lvbiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9qYXZhc2NyaXB0LWV4dGVuc2lvbjpmYWN0b3J5JyxcbiAgcmVuZGVyZXJGYWN0b3J5LFxuICByYW5rOiAwLFxuICBkYXRhVHlwZTogJ3N0cmluZydcbn07XG5cbmV4cG9ydCBkZWZhdWx0IGV4dGVuc2lvbjtcbiJdLCJzb3VyY2VSb290IjoiIn0=