(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_vega5-extension_lib_index_js"],{

/***/ "../packages/vega5-extension/lib/index.js":
/*!************************************************!*\
  !*** ../packages/vega5-extension/lib/index.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "VEGA_MIME_TYPE": () => (/* binding */ VEGA_MIME_TYPE),
/* harmony export */   "VEGALITE3_MIME_TYPE": () => (/* binding */ VEGALITE3_MIME_TYPE),
/* harmony export */   "VEGALITE4_MIME_TYPE": () => (/* binding */ VEGALITE4_MIME_TYPE),
/* harmony export */   "RenderedVega": () => (/* binding */ RenderedVega),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module vega5-extension
 */

/**
 * The CSS class to add to the Vega and Vega-Lite widget.
 */
const VEGA_COMMON_CLASS = 'jp-RenderedVegaCommon5';
/**
 * The CSS class to add to the Vega.
 */
const VEGA_CLASS = 'jp-RenderedVega5';
/**
 * The CSS class to add to the Vega-Lite.
 */
const VEGALITE_CLASS = 'jp-RenderedVegaLite';
/**
 * The MIME type for Vega.
 *
 * #### Notes
 * The version of this follows the major version of Vega.
 */
const VEGA_MIME_TYPE = 'application/vnd.vega.v5+json';
/**
 * The MIME type for Vega-Lite.
 *
 * #### Notes
 * The version of this follows the major version of Vega-Lite.
 */
const VEGALITE3_MIME_TYPE = 'application/vnd.vegalite.v3+json';
/**
 * The MIME type for Vega-Lite.
 *
 * #### Notes
 * The version of this follows the major version of Vega-Lite.
 */
const VEGALITE4_MIME_TYPE = 'application/vnd.vegalite.v4+json';
/**
 * A widget for rendering Vega or Vega-Lite data, for usage with rendermime.
 */
class RenderedVega extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Create a new widget for rendering Vega/Vega-Lite.
     */
    constructor(options) {
        super();
        this._mimeType = options.mimeType;
        this._resolver = options.resolver;
        this.addClass(VEGA_COMMON_CLASS);
        this.addClass(this._mimeType === VEGA_MIME_TYPE ? VEGA_CLASS : VEGALITE_CLASS);
    }
    /**
     * Render Vega/Vega-Lite into this widget's node.
     */
    async renderModel(model) {
        const spec = model.data[this._mimeType];
        if (spec === undefined) {
            return;
        }
        const metadata = model.metadata[this._mimeType];
        const embedOptions = metadata && metadata.embed_options ? metadata.embed_options : {};
        const mode = this._mimeType === VEGA_MIME_TYPE ? 'vega' : 'vega-lite';
        const vega = Private.vega != null ? Private.vega : await Private.ensureVega();
        const el = document.createElement('div');
        // clear the output before attaching a chart
        this.node.textContent = '';
        this.node.appendChild(el);
        if (this._result) {
            this._result.finalize();
        }
        const loader = vega.vega.loader({
            http: { credentials: 'same-origin' }
        });
        const sanitize = async (uri, options) => {
            // Use the resolver for any URIs it wants to handle
            const resolver = this._resolver;
            if ((resolver === null || resolver === void 0 ? void 0 : resolver.isLocal) && resolver.isLocal(uri)) {
                const absPath = await resolver.resolveUrl(uri);
                uri = await resolver.getDownloadUrl(absPath);
            }
            return loader.sanitize(uri, options);
        };
        this._result = await vega.default(el, spec, Object.assign(Object.assign({ actions: true, defaultStyle: true }, embedOptions), { mode, loader: Object.assign(Object.assign({}, loader), { sanitize }) }));
        if (model.data['image/png']) {
            return;
        }
        // Add png representation of vega chart to output
        const imageURL = await this._result.view.toImageURL('png');
        model.setData({
            data: Object.assign(Object.assign({}, model.data), { 'image/png': imageURL.split(',')[1] })
        });
    }
    dispose() {
        if (this._result) {
            this._result.finalize();
        }
        super.dispose();
    }
}
/**
 * A mime renderer factory for vega data.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [VEGA_MIME_TYPE, VEGALITE3_MIME_TYPE, VEGALITE4_MIME_TYPE],
    createRenderer: options => new RenderedVega(options)
};
const extension = {
    id: '@jupyterlab/vega5-extension:factory',
    rendererFactory,
    rank: 57,
    dataType: 'json',
    documentWidgetFactoryOptions: [
        {
            name: 'Vega5',
            primaryFileType: 'vega5',
            fileTypes: ['vega5', 'json'],
            defaultFor: ['vega5']
        },
        {
            name: 'Vega-Lite4',
            primaryFileType: 'vega-lite4',
            fileTypes: ['vega-lite3', 'vega-lite4', 'json'],
            defaultFor: ['vega-lite3', 'vega-lite4']
        }
    ],
    fileTypes: [
        {
            mimeTypes: [VEGA_MIME_TYPE],
            name: 'vega5',
            extensions: ['.vg', '.vg.json', '.vega'],
            icon: 'ui-components:vega'
        },
        {
            mimeTypes: [VEGALITE4_MIME_TYPE],
            name: 'vega-lite4',
            extensions: ['.vl', '.vl.json', '.vegalite'],
            icon: 'ui-components:vega'
        },
        {
            mimeTypes: [VEGALITE3_MIME_TYPE],
            name: 'vega-lite3',
            extensions: [],
            icon: 'ui-components:vega'
        }
    ]
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Lazy-load and cache the vega-embed library
     */
    function ensureVega() {
        if (Private.vegaReady) {
            return Private.vegaReady;
        }
        Private.vegaReady = __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_vega-embed_vega-embed").then(__webpack_require__.t.bind(__webpack_require__, /*! vega-embed */ "webpack/sharing/consume/default/vega-embed/vega-embed", 23));
        return Private.vegaReady;
    }
    Private.ensureVega = ensureVega;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdmVnYTUtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBOzs7K0VBRytFO0FBQy9FOzs7R0FHRztBQUlzQztBQUd6Qzs7R0FFRztBQUNILE1BQU0saUJBQWlCLEdBQUcsd0JBQXdCLENBQUM7QUFFbkQ7O0dBRUc7QUFDSCxNQUFNLFVBQVUsR0FBRyxrQkFBa0IsQ0FBQztBQUV0Qzs7R0FFRztBQUNILE1BQU0sY0FBYyxHQUFHLHFCQUFxQixDQUFDO0FBRTdDOzs7OztHQUtHO0FBQ0ksTUFBTSxjQUFjLEdBQUcsOEJBQThCLENBQUM7QUFFN0Q7Ozs7O0dBS0c7QUFDSSxNQUFNLG1CQUFtQixHQUFHLGtDQUFrQyxDQUFDO0FBRXRFOzs7OztHQUtHO0FBQ0ksTUFBTSxtQkFBbUIsR0FBRyxrQ0FBa0MsQ0FBQztBQUV0RTs7R0FFRztBQUNJLE1BQU0sWUFBYSxTQUFRLG1EQUFNO0lBR3RDOztPQUVHO0lBQ0gsWUFBWSxPQUFxQztRQUMvQyxLQUFLLEVBQUUsQ0FBQztRQUNSLElBQUksQ0FBQyxTQUFTLEdBQUcsT0FBTyxDQUFDLFFBQVEsQ0FBQztRQUNsQyxJQUFJLENBQUMsU0FBUyxHQUFHLE9BQU8sQ0FBQyxRQUFRLENBQUM7UUFDbEMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxpQkFBaUIsQ0FBQyxDQUFDO1FBQ2pDLElBQUksQ0FBQyxRQUFRLENBQ1gsSUFBSSxDQUFDLFNBQVMsS0FBSyxjQUFjLENBQUMsQ0FBQyxDQUFDLFVBQVUsQ0FBQyxDQUFDLENBQUMsY0FBYyxDQUNoRSxDQUFDO0lBQ0osQ0FBQztJQUVEOztPQUVHO0lBQ0gsS0FBSyxDQUFDLFdBQVcsQ0FBQyxLQUE2QjtRQUM3QyxNQUFNLElBQUksR0FBRyxLQUFLLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxTQUFTLENBQTJCLENB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QUUsRUFBRTtZQUNkLElBQUksRUFBRSxvQkFBb0I7U0FDM0I7S0FDRjtDQUNGLENBQUM7QUFFRixpRUFBZSxTQUFTLEVBQUM7QUFFekI7O0dBRUc7QUFDSCxJQUFVLE9BQU8sQ0F1QmhCO0FBdkJELFdBQVUsT0FBTztJQVdmOztPQUVHO0lBQ0gsU0FBZ0IsVUFBVTtRQUN4QixJQUFJLGlCQUFTLEVBQUU7WUFDYixPQUFPLGlCQUFTLENBQUM7U0FDbEI7UUFFRCxpQkFBUyxHQUFHLG1PQUFvQixDQUFDO1FBRWpDLE9BQU8saUJBQVMsQ0FBQztJQUNuQixDQUFDO0lBUmUsa0JBQVUsYUFRekI7QUFDSCxDQUFDLEVBdkJTLE9BQU8sS0FBUCxPQUFPLFFBdUJoQiIsImZpbGUiOiJwYWNrYWdlc192ZWdhNS1leHRlbnNpb25fbGliX2luZGV4X2pzLjZiYzlkZDdlNGVmOTZkNWE0MDBiLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSB2ZWdhNS1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQgeyBJUmVuZGVyTWltZSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUtaW50ZXJmYWNlcyc7XG5pbXBvcnQgeyBKU09OT2JqZWN0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCAqIGFzIFZlZ2FNb2R1bGVUeXBlIGZyb20gJ3ZlZ2EtZW1iZWQnO1xuXG4vKipcbiAqIFRoZSBDU1MgY2xhc3MgdG8gYWRkIHRvIHRoZSBWZWdhIGFuZCBWZWdhLUxpdGUgd2lkZ2V0LlxuICovXG5jb25zdCBWRUdBX0NPTU1PTl9DTEFTUyA9ICdqcC1SZW5kZXJlZFZlZ2FDb21tb241JztcblxuLyoqXG4gKiBUaGUgQ1NTIGNsYXNzIHRvIGFkZCB0byB0aGUgVmVnYS5cbiAqL1xuY29uc3QgVkVHQV9DTEFTUyA9ICdqcC1SZW5kZXJlZFZlZ2E1JztcblxuLyoqXG4gKiBUaGUgQ1NTIGNsYXNzIHRvIGFkZCB0byB0aGUgVmVnYS1MaXRlLlxuICovXG5jb25zdCBWRUdBTElURV9DTEFTUyA9ICdqcC1SZW5kZXJlZFZlZ2FMaXRlJztcblxuLyoqXG4gKiBUaGUgTUlNRSB0eXBlIGZvciBWZWdhLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIFRoZSB2ZXJzaW9uIG9mIHRoaXMgZm9sbG93cyB0aGUgbWFqb3IgdmVyc2lvbiBvZiBWZWdhLlxuICovXG5leHBvcnQgY29uc3QgVkVHQV9NSU1FX1RZUEUgPSAnYXBwbGljYXRpb24vdm5kLnZlZ2EudjUranNvbic7XG5cbi8qKlxuICogVGhlIE1JTUUgdHlwZSBmb3IgVmVnYS1MaXRlLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIFRoZSB2ZXJzaW9uIG9mIHRoaXMgZm9sbG93cyB0aGUgbWFqb3IgdmVyc2lvbiBvZiBWZWdhLUxpdGUuXG4gKi9cbmV4cG9ydCBjb25zdCBWRUdBTElURTNfTUlNRV9UWVBFID0gJ2FwcGxpY2F0aW9uL3ZuZC52ZWdhbGl0ZS52Mytqc29uJztcblxuLyoqXG4gKiBUaGUgTUlNRSB0eXBlIGZvciBWZWdhLUxpdGUuXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhlIHZlcnNpb24gb2YgdGhpcyBmb2xsb3dzIHRoZSBtYWpvciB2ZXJzaW9uIG9mIFZlZ2EtTGl0ZS5cbiAqL1xuZXhwb3J0IGNvbnN0IFZFR0FMSVRFNF9NSU1FX1RZUEUgPSAnYXBwbGljYXRpb24vdm5kLnZlZ2FsaXRlLnY0K2pzb24nO1xuXG4vKipcbiAqIEEgd2lkZ2V0IGZvciByZW5kZXJpbmcgVmVnYSBvciBWZWdhLUxpdGUgZGF0YSwgZm9yIHVzYWdlIHdpdGggcmVuZGVybWltZS5cbiAqL1xuZXhwb3J0IGNsYXNzIFJlbmRlcmVkVmVnYSBleHRlbmRzIFdpZGdldCBpbXBsZW1lbnRzIElSZW5kZXJNaW1lLklSZW5kZXJlciB7XG4gIHByaXZhdGUgX3Jlc3VsdDogVmVnYU1vZHVsZVR5cGUuUmVzdWx0O1xuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgd2lkZ2V0IGZvciByZW5kZXJpbmcgVmVnYS9WZWdhLUxpdGUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmVuZGVyTWltZS5JUmVuZGVyZXJPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl9taW1lVHlwZSA9IG9wdGlvbnMubWltZVR5cGU7XG4gICAgdGhpcy5fcmVzb2x2ZXIgPSBvcHRpb25zLnJlc29sdmVyO1xuICAgIHRoaXMuYWRkQ2xhc3MoVkVHQV9DT01NT05fQ0xBU1MpO1xuICAgIHRoaXMuYWRkQ2xhc3MoXG4gICAgICB0aGlzLl9taW1lVHlwZSA9PT0gVkVHQV9NSU1FX1RZUEUgPyBWRUdBX0NMQVNTIDogVkVHQUxJVEVfQ0xBU1NcbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciBWZWdhL1ZlZ2EtTGl0ZSBpbnRvIHRoaXMgd2lkZ2V0J3Mgbm9kZS5cbiAgICovXG4gIGFzeW5jIHJlbmRlck1vZGVsKG1vZGVsOiBJUmVuZGVyTWltZS5JTWltZU1vZGVsKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3Qgc3BlYyA9IG1vZGVsLmRhdGFbdGhpcy5fbWltZVR5cGVdIGFzIEpTT05PYmplY3QgfCB1bmRlZmluZWQ7XG4gICAgaWYgKHNwZWMgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBtZXRhZGF0YSA9IG1vZGVsLm1ldGFkYXRhW3RoaXMuX21pbWVUeXBlXSBhc1xuICAgICAgfCB7XG4gICAgICAgICAgZW1iZWRfb3B0aW9ucz86IFZlZ2FNb2R1bGVUeXBlLkVtYmVkT3B0aW9ucztcbiAgICAgICAgfVxuICAgICAgfCB1bmRlZmluZWQ7XG4gICAgY29uc3QgZW1iZWRPcHRpb25zID1cbiAgICAgIG1ldGFkYXRhICYmIG1ldGFkYXRhLmVtYmVkX29wdGlvbnMgPyBtZXRhZGF0YS5lbWJlZF9vcHRpb25zIDoge307XG4gICAgY29uc3QgbW9kZTogVmVnYU1vZHVsZVR5cGUuTW9kZSA9XG4gICAgICB0aGlzLl9taW1lVHlwZSA9PT0gVkVHQV9NSU1FX1RZUEUgPyAndmVnYScgOiAndmVnYS1saXRlJztcblxuICAgIGNvbnN0IHZlZ2EgPVxuICAgICAgUHJpdmF0ZS52ZWdhICE9IG51bGwgPyBQcml2YXRlLnZlZ2EgOiBhd2FpdCBQcml2YXRlLmVuc3VyZVZlZ2EoKTtcblxuICAgIGNvbnN0IGVsID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG5cbiAgICAvLyBjbGVhciB0aGUgb3V0cHV0IGJlZm9yZSBhdHRhY2hpbmcgYSBjaGFydFxuICAgIHRoaXMubm9kZS50ZXh0Q29udGVudCA9ICcnO1xuICAgIHRoaXMubm9kZS5hcHBlbmRDaGlsZChlbCk7XG5cbiAgICBpZiAodGhpcy5fcmVzdWx0KSB7XG4gICAgICB0aGlzLl9yZXN1bHQuZmluYWxpemUoKTtcbiAgICB9XG5cbiAgICBjb25zdCBsb2FkZXIgPSB2ZWdhLnZlZ2EubG9hZGVyKHtcbiAgICAgIGh0dHA6IHsgY3JlZGVudGlhbHM6ICdzYW1lLW9yaWdpbicgfVxuICAgIH0pO1xuICAgIGNvbnN0IHNhbml0aXplID0gYXN5bmMgKHVyaTogc3RyaW5nLCBvcHRpb25zOiBhbnkpID0+IHtcbiAgICAgIC8vIFVzZSB0aGUgcmVzb2x2ZXIgZm9yIGFueSBVUklzIGl0IHdhbnRzIHRvIGhhbmRsZVxuICAgICAgY29uc3QgcmVzb2x2ZXIgPSB0aGlzLl9yZXNvbHZlcjtcbiAgICAgIGlmIChyZXNvbHZlcj8uaXNMb2NhbCAmJiByZXNvbHZlci5pc0xvY2FsKHVyaSkpIHtcbiAgICAgICAgY29uc3QgYWJzUGF0aCA9IGF3YWl0IHJlc29sdmVyLnJlc29sdmVVcmwodXJpKTtcbiAgICAgICAgdXJpID0gYXdhaXQgcmVzb2x2ZXIuZ2V0RG93bmxvYWRVcmwoYWJzUGF0aCk7XG4gICAgICB9XG4gICAgICByZXR1cm4gbG9hZGVyLnNhbml0aXplKHVyaSwgb3B0aW9ucyk7XG4gICAgfTtcblxuICAgIHRoaXMuX3Jlc3VsdCA9IGF3YWl0IHZlZ2EuZGVmYXVsdChlbCwgc3BlYywge1xuICAgICAgYWN0aW9uczogdHJ1ZSxcbiAgICAgIGRlZmF1bHRTdHlsZTogdHJ1ZSxcbiAgICAgIC4uLmVtYmVkT3B0aW9ucyxcbiAgICAgIG1vZGUsXG4gICAgICBsb2FkZXI6IHsgLi4ubG9hZGVyLCBzYW5pdGl6ZSB9XG4gICAgfSk7XG5cbiAgICBpZiAobW9kZWwuZGF0YVsnaW1hZ2UvcG5nJ10pIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBBZGQgcG5nIHJlcHJlc2VudGF0aW9uIG9mIHZlZ2EgY2hhcnQgdG8gb3V0cHV0XG4gICAgY29uc3QgaW1hZ2VVUkwgPSBhd2FpdCB0aGlzLl9yZXN1bHQudmlldy50b0ltYWdlVVJMKCdwbmcnKTtcbiAgICBtb2RlbC5zZXREYXRhKHtcbiAgICAgIGRhdGE6IHsgLi4ubW9kZWwuZGF0YSwgJ2ltYWdlL3BuZyc6IGltYWdlVVJMLnNwbGl0KCcsJylbMV0gfVxuICAgIH0pO1xuICB9XG5cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fcmVzdWx0KSB7XG4gICAgICB0aGlzLl9yZXN1bHQuZmluYWxpemUoKTtcbiAgICB9XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgcHJpdmF0ZSBfbWltZVR5cGU6IHN0cmluZztcbiAgcHJpdmF0ZSBfcmVzb2x2ZXI6IElSZW5kZXJNaW1lLklSZXNvbHZlciB8IG51bGw7XG59XG5cbi8qKlxuICogQSBtaW1lIHJlbmRlcmVyIGZhY3RvcnkgZm9yIHZlZ2EgZGF0YS5cbiAqL1xuZXhwb3J0IGNvbnN0IHJlbmRlcmVyRmFjdG9yeTogSVJlbmRlck1pbWUuSVJlbmRlcmVyRmFjdG9yeSA9IHtcbiAgc2FmZTogdHJ1ZSxcbiAgbWltZVR5cGVzOiBbVkVHQV9NSU1FX1RZUEUsIFZFR0FMSVRFM19NSU1FX1RZUEUsIFZFR0FMSVRFNF9NSU1FX1RZUEVdLFxuICBjcmVhdGVSZW5kZXJlcjogb3B0aW9ucyA9PiBuZXcgUmVuZGVyZWRWZWdhKG9wdGlvbnMpXG59O1xuXG5jb25zdCBleHRlbnNpb246IElSZW5kZXJNaW1lLklFeHRlbnNpb24gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvdmVnYTUtZXh0ZW5zaW9uOmZhY3RvcnknLFxuICByZW5kZXJlckZhY3RvcnksXG4gIHJhbms6IDU3LFxuICBkYXRhVHlwZTogJ2pzb24nLFxuICBkb2N1bWVudFdpZGdldEZhY3RvcnlPcHRpb25zOiBbXG4gICAge1xuICAgICAgbmFtZTogJ1ZlZ2E1JyxcbiAgICAgIHByaW1hcnlGaWxlVHlwZTogJ3ZlZ2E1JyxcbiAgICAgIGZpbGVUeXBlczogWyd2ZWdhNScsICdqc29uJ10sXG4gICAgICBkZWZhdWx0Rm9yOiBbJ3ZlZ2E1J11cbiAgICB9LFxuICAgIHtcbiAgICAgIG5hbWU6ICdWZWdhLUxpdGU0JyxcbiAgICAgIHByaW1hcnlGaWxlVHlwZTogJ3ZlZ2EtbGl0ZTQnLFxuICAgICAgZmlsZVR5cGVzOiBbJ3ZlZ2EtbGl0ZTMnLCAndmVnYS1saXRlNCcsICdqc29uJ10sXG4gICAgICBkZWZhdWx0Rm9yOiBbJ3ZlZ2EtbGl0ZTMnLCAndmVnYS1saXRlNCddXG4gICAgfVxuICBdLFxuICBmaWxlVHlwZXM6IFtcbiAgICB7XG4gICAgICBtaW1lVHlwZXM6IFtWRUdBX01JTUVfVFlQRV0sXG4gICAgICBuYW1lOiAndmVnYTUnLFxuICAgICAgZXh0ZW5zaW9uczogWycudmcnLCAnLnZnLmpzb24nLCAnLnZlZ2EnXSxcbiAgICAgIGljb246ICd1aS1jb21wb25lbnRzOnZlZ2EnXG4gICAgfSxcbiAgICB7XG4gICAgICBtaW1lVHlwZXM6IFtWRUdBTElURTRfTUlNRV9UWVBFXSxcbiAgICAgIG5hbWU6ICd2ZWdhLWxpdGU0JyxcbiAgICAgIGV4dGVuc2lvbnM6IFsnLnZsJywgJy52bC5qc29uJywgJy52ZWdhbGl0ZSddLFxuICAgICAgaWNvbjogJ3VpLWNvbXBvbmVudHM6dmVnYSdcbiAgICB9LFxuICAgIHtcbiAgICAgIG1pbWVUeXBlczogW1ZFR0FMSVRFM19NSU1FX1RZUEVdLFxuICAgICAgbmFtZTogJ3ZlZ2EtbGl0ZTMnLFxuICAgICAgZXh0ZW5zaW9uczogW10sXG4gICAgICBpY29uOiAndWktY29tcG9uZW50czp2ZWdhJ1xuICAgIH1cbiAgXVxufTtcblxuZXhwb3J0IGRlZmF1bHQgZXh0ZW5zaW9uO1xuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIG1vZHVsZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBIGNhY2hlZCByZWZlcmVuY2UgdG8gdGhlIHZlZ2EgbGlicmFyeS5cbiAgICovXG4gIGV4cG9ydCBsZXQgdmVnYTogdHlwZW9mIFZlZ2FNb2R1bGVUeXBlO1xuXG4gIC8qKlxuICAgKiBBIFByb21pc2UgZm9yIHRoZSBpbml0aWFsIGxvYWQgb2YgdmVnYS5cbiAgICovXG4gIGV4cG9ydCBsZXQgdmVnYVJlYWR5OiBQcm9taXNlPHR5cGVvZiBWZWdhTW9kdWxlVHlwZT47XG5cbiAgLyoqXG4gICAqIExhenktbG9hZCBhbmQgY2FjaGUgdGhlIHZlZ2EtZW1iZWQgbGlicmFyeVxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGVuc3VyZVZlZ2EoKTogUHJvbWlzZTx0eXBlb2YgVmVnYU1vZHVsZVR5cGU+IHtcbiAgICBpZiAodmVnYVJlYWR5KSB7XG4gICAgICByZXR1cm4gdmVnYVJlYWR5O1xuICAgIH1cblxuICAgIHZlZ2FSZWFkeSA9IGltcG9ydCgndmVnYS1lbWJlZCcpO1xuXG4gICAgcmV0dXJuIHZlZ2FSZWFkeTtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==