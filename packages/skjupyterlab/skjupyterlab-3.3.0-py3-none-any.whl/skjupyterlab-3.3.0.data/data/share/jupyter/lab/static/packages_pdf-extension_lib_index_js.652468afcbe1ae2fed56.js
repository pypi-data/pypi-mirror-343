(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_pdf-extension_lib_index_js"],{

/***/ "../packages/pdf-extension/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/pdf-extension/lib/index.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RenderedPDF": () => (/* binding */ RenderedPDF),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module pdf-extension
 */



/**
 * The MIME type for PDF.
 */
const MIME_TYPE = 'application/pdf';
/**
 * A class for rendering a PDF document.
 */
class RenderedPDF extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor() {
        super();
        this._base64 = '';
        this._disposable = null;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        this.addClass('jp-PDFContainer');
        // We put the object in an iframe, which seems to have a better chance
        // of retaining its scroll position upon tab focusing, moving around etc.
        const iframe = document.createElement('iframe');
        this.node.appendChild(iframe);
        // The iframe content window is not available until the onload event.
        iframe.onload = () => {
            const body = iframe.contentWindow.document.createElement('body');
            body.style.margin = '0px';
            iframe.contentWindow.document.body = body;
            this._object = iframe.contentWindow.document.createElement('object');
            // work around for https://discussions.apple.com/thread/252247740
            // Detect if running on Desktop Safari
            if (!window.safari) {
                this._object.type = MIME_TYPE;
            }
            this._object.width = '100%';
            this._object.height = '100%';
            body.appendChild(this._object);
            this._ready.resolve(void 0);
        };
    }
    /**
     * Render PDF into this widget's node.
     */
    async renderModel(model) {
        await this._ready.promise;
        const data = model.data[MIME_TYPE];
        if (!data ||
            (data.length === this._base64.length && data === this._base64)) {
            // If there is no data, or if the string has not changed, we do not
            // need to re-parse the data and rerender. We do, however, check
            // for a fragment if the user wants to scroll the output.
            if (model.metadata.fragment && this._object.data) {
                const url = this._object.data;
                this._object.data = `${url.split('#')[0]}${model.metadata.fragment}`;
            }
            // For some opaque reason, Firefox seems to loose its scroll position
            // upon unhiding a PDF. But triggering a refresh of the URL makes it
            // find it again. No idea what the reason for this is.
            if (Private.IS_FIREFOX) {
                this._object.data = this._object.data; // eslint-disable-line
            }
            return Promise.resolve(void 0);
        }
        this._base64 = data;
        const blob = Private.b64toBlob(data, MIME_TYPE);
        // Release reference to any previous object url.
        if (this._disposable) {
            this._disposable.dispose();
        }
        let objectUrl = URL.createObjectURL(blob);
        if (model.metadata.fragment) {
            objectUrl += model.metadata.fragment;
        }
        this._object.data = objectUrl;
        // Set the disposable release the object URL.
        this._disposable = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            try {
                URL.revokeObjectURL(objectUrl);
            }
            catch (error) {
                /* no-op */
            }
        });
        return;
    }
    /**
     * Handle a `before-hide` message.
     */
    onBeforeHide() {
        // Dispose of any URL fragment before hiding the widget
        // so that it is not remembered upon show. Only Firefox
        // seems to have a problem with this.
        if (Private.IS_FIREFOX) {
            this._object.data = this._object.data.split('#')[0];
        }
    }
    /**
     * Dispose of the resources held by the pdf widget.
     */
    dispose() {
        if (this._disposable) {
            this._disposable.dispose();
        }
        super.dispose();
    }
}
/**
 * A mime renderer factory for PDF data.
 */
const rendererFactory = {
    safe: false,
    mimeTypes: [MIME_TYPE],
    defaultRank: 100,
    createRenderer: options => new RenderedPDF()
};
const extensions = [
    {
        id: '@jupyterlab/pdf-extension:factory',
        rendererFactory,
        dataType: 'string',
        documentWidgetFactoryOptions: {
            name: 'PDF',
            modelName: 'base64',
            primaryFileType: 'PDF',
            fileTypes: ['PDF'],
            defaultFor: ['PDF']
        }
    }
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extensions);
/**
 * A namespace for PDF widget private data.
 */
var Private;
(function (Private) {
    /**
     * A flag for determining whether the user is using Firefox.
     * There are some different PDF viewer behaviors on Firefox,
     * and we try to address them with this. User agent string parsing
     * is *not* reliable, so this should be considered a best-effort test.
     */
    Private.IS_FIREFOX = /Firefox/.test(navigator.userAgent);
    /**
     * Convert a base64 encoded string to a Blob object.
     * Modified from a snippet found here:
     * https://stackoverflow.com/questions/16245767/creating-a-blob-from-a-base64-string-in-javascript
     *
     * @param b64Data - The base64 encoded data.
     *
     * @param contentType - The mime type of the data.
     *
     * @param sliceSize - The size to chunk the data into for processing.
     *
     * @returns a Blob for the data.
     */
    function b64toBlob(b64Data, contentType = '', sliceSize = 512) {
        const byteCharacters = atob(b64Data);
        const byteArrays = [];
        for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            const slice = byteCharacters.slice(offset, offset + sliceSize);
            const byteNumbers = new Array(slice.length);
            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
        }
        return new Blob(byteArrays, { type: contentType });
    }
    Private.b64toBlob = b64toBlob;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcGRmLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFHaUQ7QUFDSTtBQUNmO0FBRXpDOztHQUVHO0FBQ0gsTUFBTSxTQUFTLEdBQUcsaUJBQWlCLENBQUM7QUFFcEM7O0dBRUc7QUFDSSxNQUFNLFdBQVksU0FBUSxtREFBTTtJQUNyQztRQUNFLEtBQUssRUFBRSxDQUFDO1FBK0ZGLFlBQU8sR0FBRyxFQUFFLENBQUM7UUFDYixnQkFBVyxHQUE4QixJQUFJLENBQUM7UUFFOUMsV0FBTSxHQUFHLElBQUksOERBQWUsRUFBUSxDQUFDO1FBakczQyxJQUFJLENBQUMsUUFBUSxDQUFDLGlCQUFpQixDQUFDLENBQUM7UUFDakMsc0VBQXNFO1FBQ3RFLHlFQUF5RTtRQUN6RSxNQUFNLE1BQU0sR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBQ2hELElBQUksQ0FBQyxJQUFJLENBQUMsV0FBVyxDQUFDLE1BQU0sQ0FBQyxDQUFDO1FBQzlCLHFFQUFxRTtRQUNyRSxNQUFNLENBQUMsTUFBTSxHQUFHLEdBQUcsRUFBRTtZQUNuQixNQUFNLElBQUksR0FBRyxNQUFNLENBQUMsYUFBYyxDQUFDLFFBQVEsQ0FBQyxhQUFhLENBQUMsTUFBTSxDQUFDLENBQUM7WUFDbEUsSUFBSSxDQUFDLEtBQUssQ0FBQyxNQUFNLEdBQUcsS0FBSyxDQUFDO1lBQzFCLE1BQU0sQ0FBQyxhQUFjLENBQUMsUUFBUSxDQUFDLElBQUksR0FBRyxJQUFJLENBQUM7WUFDM0MsSUFBSSxDQUFDLE9BQU8sR0FBRyxNQUFNLENBQUMsYUFBYyxDQUFDLFFBQVEsQ0FBQyxhQUFhLENBQUMsUUFBUSxDQUFDLENBQUM7WUFDdEUsaUVBQWlFO1lB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Q0FBQyxDQUFDO1FBQ3JDLE1BQU0sVUFBVSxHQUFpQixFQUFFLENBQUM7UUFFcEMsS0FBSyxJQUFJLE1BQU0sR0FBRyxDQUFDLEVBQUUsTUFBTSxHQUFHLGNBQWMsQ0FBQyxNQUFNLEVBQUUsTUFBTSxJQUFJLFNBQVMsRUFBRTtZQUN4RSxNQUFNLEtBQUssR0FBRyxjQUFjLENBQUMsS0FBSyxDQUFDLE1BQU0sRUFBRSxNQUFNLEdBQUcsU0FBUyxDQUFDLENBQUM7WUFFL0QsTUFBTSxXQUFXLEdBQUcsSUFBSSxLQUFLLENBQUMsS0FBSyxDQUFDLE1BQU0sQ0FBQyxDQUFDO1lBQzVDLEtBQUssSUFBSSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsR0FBRyxLQUFLLENBQUMsTUFBTSxFQUFFLENBQUMsRUFBRSxFQUFFO2dCQUNyQyxXQUFXLENBQUMsQ0FBQyxDQUFDLEdBQUcsS0FBSyxDQUFDLFVBQVUsQ0FBQyxDQUFDLENBQUMsQ0FBQzthQUN0QztZQUNELE1BQU0sU0FBUyxHQUFHLElBQUksVUFBVSxDQUFDLFdBQVcsQ0FBQyxDQUFDO1lBQzlDLFVBQVUsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLENBQUM7U0FDNUI7UUFFRCxPQUFPLElBQUksSUFBSSxDQUFDLFVBQVUsRUFBRSxFQUFFLElBQUksRUFBRSxXQUFXLEVBQUUsQ0FBQyxDQUFDO0lBQ3JELENBQUM7SUFwQmUsaUJBQVMsWUFvQnhCO0FBQ0gsQ0FBQyxFQTNDUyxPQUFPLEtBQVAsT0FBTyxRQTJDaEIiLCJmaWxlIjoicGFja2FnZXNfcGRmLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuNjUyNDY4YWZjYmUxYWUyZmVkNTYuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBwZGYtZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHsgSVJlbmRlck1pbWUgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lLWludGVyZmFjZXMnO1xuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgRGlzcG9zYWJsZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogVGhlIE1JTUUgdHlwZSBmb3IgUERGLlxuICovXG5jb25zdCBNSU1FX1RZUEUgPSAnYXBwbGljYXRpb24vcGRmJztcblxuLyoqXG4gKiBBIGNsYXNzIGZvciByZW5kZXJpbmcgYSBQREYgZG9jdW1lbnQuXG4gKi9cbmV4cG9ydCBjbGFzcyBSZW5kZXJlZFBERiBleHRlbmRzIFdpZGdldCBpbXBsZW1lbnRzIElSZW5kZXJNaW1lLklSZW5kZXJlciB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtUERGQ29udGFpbmVyJyk7XG4gICAgLy8gV2UgcHV0IHRoZSBvYmplY3QgaW4gYW4gaWZyYW1lLCB3aGljaCBzZWVtcyB0byBoYXZlIGEgYmV0dGVyIGNoYW5jZVxuICAgIC8vIG9mIHJldGFpbmluZyBpdHMgc2Nyb2xsIHBvc2l0aW9uIHVwb24gdGFiIGZvY3VzaW5nLCBtb3ZpbmcgYXJvdW5kIGV0Yy5cbiAgICBjb25zdCBpZnJhbWUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdpZnJhbWUnKTtcbiAgICB0aGlzLm5vZGUuYXBwZW5kQ2hpbGQoaWZyYW1lKTtcbiAgICAvLyBUaGUgaWZyYW1lIGNvbnRlbnQgd2luZG93IGlzIG5vdCBhdmFpbGFibGUgdW50aWwgdGhlIG9ubG9hZCBldmVudC5cbiAgICBpZnJhbWUub25sb2FkID0gKCkgPT4ge1xuICAgICAgY29uc3QgYm9keSA9IGlmcmFtZS5jb250ZW50V2luZG93IS5kb2N1bWVudC5jcmVhdGVFbGVtZW50KCdib2R5Jyk7XG4gICAgICBib2R5LnN0eWxlLm1hcmdpbiA9ICcwcHgnO1xuICAgICAgaWZyYW1lLmNvbnRlbnRXaW5kb3chLmRvY3VtZW50LmJvZHkgPSBib2R5O1xuICAgICAgdGhpcy5fb2JqZWN0ID0gaWZyYW1lLmNvbnRlbnRXaW5kb3chLmRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ29iamVjdCcpO1xuICAgICAgLy8gd29yayBhcm91bmQgZm9yIGh0dHBzOi8vZGlzY3Vzc2lvbnMuYXBwbGUuY29tL3RocmVhZC8yNTIyNDc3NDBcbiAgICAgIC8vIERldGVjdCBpZiBydW5uaW5nIG9uIERlc2t0b3AgU2FmYXJpXG4gICAgICBpZiAoISh3aW5kb3cgYXMgYW55KS5zYWZhcmkpIHtcbiAgICAgICAgdGhpcy5fb2JqZWN0LnR5cGUgPSBNSU1FX1RZUEU7XG4gICAgICB9XG4gICAgICB0aGlzLl9vYmplY3Qud2lkdGggPSAnMTAwJSc7XG4gICAgICB0aGlzLl9vYmplY3QuaGVpZ2h0ID0gJzEwMCUnO1xuICAgICAgYm9keS5hcHBlbmRDaGlsZCh0aGlzLl9vYmplY3QpO1xuICAgICAgdGhpcy5fcmVhZHkucmVzb2x2ZSh2b2lkIDApO1xuICAgIH07XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIFBERiBpbnRvIHRoaXMgd2lkZ2V0J3Mgbm9kZS5cbiAgICovXG4gIGFzeW5jIHJlbmRlck1vZGVsKG1vZGVsOiBJUmVuZGVyTWltZS5JTWltZU1vZGVsKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgYXdhaXQgdGhpcy5fcmVhZHkucHJvbWlzZTtcbiAgICBjb25zdCBkYXRhID0gbW9kZWwuZGF0YVtNSU1FX1RZUEVdIGFzIHN0cmluZyB8IHVuZGVmaW5lZDtcbiAgICBpZiAoXG4gICAgICAhZGF0YSB8fFxuICAgICAgKGRhdGEubGVuZ3RoID09PSB0aGlzLl9iYXNlNjQubGVuZ3RoICYmIGRhdGEgPT09IHRoaXMuX2Jhc2U2NClcbiAgICApIHtcbiAgICAgIC8vIElmIHRoZXJlIGlzIG5vIGRhdGEsIG9yIGlmIHRoZSBzdHJpbmcgaGFzIG5vdCBjaGFuZ2VkLCB3ZSBkbyBub3RcbiAgICAgIC8vIG5lZWQgdG8gcmUtcGFyc2UgdGhlIGRhdGEgYW5kIHJlcmVuZGVyLiBXZSBkbywgaG93ZXZlciwgY2hlY2tcbiAgICAgIC8vIGZvciBhIGZyYWdtZW50IGlmIHRoZSB1c2VyIHdhbnRzIHRvIHNjcm9sbCB0aGUgb3V0cHV0LlxuICAgICAgaWYgKG1vZGVsLm1ldGFkYXRhLmZyYWdtZW50ICYmIHRoaXMuX29iamVjdC5kYXRhKSB7XG4gICAgICAgIGNvbnN0IHVybCA9IHRoaXMuX29iamVjdC5kYXRhO1xuICAgICAgICB0aGlzLl9vYmplY3QuZGF0YSA9IGAke3VybC5zcGxpdCgnIycpWzBdfSR7bW9kZWwubWV0YWRhdGEuZnJhZ21lbnR9YDtcbiAgICAgIH1cbiAgICAgIC8vIEZvciBzb21lIG9wYXF1ZSByZWFzb24sIEZpcmVmb3ggc2VlbXMgdG8gbG9vc2UgaXRzIHNjcm9sbCBwb3NpdGlvblxuICAgICAgLy8gdXBvbiB1bmhpZGluZyBhIFBERi4gQnV0IHRyaWdnZXJpbmcgYSByZWZyZXNoIG9mIHRoZSBVUkwgbWFrZXMgaXRcbiAgICAgIC8vIGZpbmQgaXQgYWdhaW4uIE5vIGlkZWEgd2hhdCB0aGUgcmVhc29uIGZvciB0aGlzIGlzLlxuICAgICAgaWYgKFByaXZhdGUuSVNfRklSRUZPWCkge1xuICAgICAgICB0aGlzLl9vYmplY3QuZGF0YSA9IHRoaXMuX29iamVjdC5kYXRhOyAvLyBlc2xpbnQtZGlzYWJsZS1saW5lXG4gICAgICB9XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKHZvaWQgMCk7XG4gICAgfVxuICAgIHRoaXMuX2Jhc2U2NCA9IGRhdGE7XG4gICAgY29uc3QgYmxvYiA9IFByaXZhdGUuYjY0dG9CbG9iKGRhdGEsIE1JTUVfVFlQRSk7XG5cbiAgICAvLyBSZWxlYXNlIHJlZmVyZW5jZSB0byBhbnkgcHJldmlvdXMgb2JqZWN0IHVybC5cbiAgICBpZiAodGhpcy5fZGlzcG9zYWJsZSkge1xuICAgICAgdGhpcy5fZGlzcG9zYWJsZS5kaXNwb3NlKCk7XG4gICAgfVxuICAgIGxldCBvYmplY3RVcmwgPSBVUkwuY3JlYXRlT2JqZWN0VVJMKGJsb2IpO1xuICAgIGlmIChtb2RlbC5tZXRhZGF0YS5mcmFnbWVudCkge1xuICAgICAgb2JqZWN0VXJsICs9IG1vZGVsLm1ldGFkYXRhLmZyYWdtZW50O1xuICAgIH1cbiAgICB0aGlzLl9vYmplY3QuZGF0YSA9IG9iamVjdFVybDtcblxuICAgIC8vIFNldCB0aGUgZGlzcG9zYWJsZSByZWxlYXNlIHRoZSBvYmplY3QgVVJMLlxuICAgIHRoaXMuX2Rpc3Bvc2FibGUgPSBuZXcgRGlzcG9zYWJsZURlbGVnYXRlKCgpID0+IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIFVSTC5yZXZva2VPYmplY3RVUkwob2JqZWN0VXJsKTtcbiAgICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgIC8qIG5vLW9wICovXG4gICAgICB9XG4gICAgfSk7XG4gICAgcmV0dXJuO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGBiZWZvcmUtaGlkZWAgbWVzc2FnZS5cbiAgICovXG4gIHByb3RlY3RlZCBvbkJlZm9yZUhpZGUoKTogdm9pZCB7XG4gICAgLy8gRGlzcG9zZSBvZiBhbnkgVVJMIGZyYWdtZW50IGJlZm9yZSBoaWRpbmcgdGhlIHdpZGdldFxuICAgIC8vIHNvIHRoYXQgaXQgaXMgbm90IHJlbWVtYmVyZWQgdXBvbiBzaG93LiBPbmx5IEZpcmVmb3hcbiAgICAvLyBzZWVtcyB0byBoYXZlIGEgcHJvYmxlbSB3aXRoIHRoaXMuXG4gICAgaWYgKFByaXZhdGUuSVNfRklSRUZPWCkge1xuICAgICAgdGhpcy5fb2JqZWN0LmRhdGEgPSB0aGlzLl9vYmplY3QuZGF0YS5zcGxpdCgnIycpWzBdO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgcGRmIHdpZGdldC5cbiAgICovXG4gIGRpc3Bvc2UoKSB7XG4gICAgaWYgKHRoaXMuX2Rpc3Bvc2FibGUpIHtcbiAgICAgIHRoaXMuX2Rpc3Bvc2FibGUuZGlzcG9zZSgpO1xuICAgIH1cbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICBwcml2YXRlIF9iYXNlNjQgPSAnJztcbiAgcHJpdmF0ZSBfZGlzcG9zYWJsZTogRGlzcG9zYWJsZURlbGVnYXRlIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX29iamVjdDogSFRNTE9iamVjdEVsZW1lbnQ7XG4gIHByaXZhdGUgX3JlYWR5ID0gbmV3IFByb21pc2VEZWxlZ2F0ZTx2b2lkPigpO1xufVxuXG4vKipcbiAqIEEgbWltZSByZW5kZXJlciBmYWN0b3J5IGZvciBQREYgZGF0YS5cbiAqL1xuZXhwb3J0IGNvbnN0IHJlbmRlcmVyRmFjdG9yeTogSVJlbmRlck1pbWUuSVJlbmRlcmVyRmFjdG9yeSA9IHtcbiAgc2FmZTogZmFsc2UsXG4gIG1pbWVUeXBlczogW01JTUVfVFlQRV0sXG4gIGRlZmF1bHRSYW5rOiAxMDAsXG4gIGNyZWF0ZVJlbmRlcmVyOiBvcHRpb25zID0+IG5ldyBSZW5kZXJlZFBERigpXG59O1xuXG5jb25zdCBleHRlbnNpb25zOiBJUmVuZGVyTWltZS5JRXh0ZW5zaW9uIHwgSVJlbmRlck1pbWUuSUV4dGVuc2lvbltdID0gW1xuICB7XG4gICAgaWQ6ICdAanVweXRlcmxhYi9wZGYtZXh0ZW5zaW9uOmZhY3RvcnknLFxuICAgIHJlbmRlcmVyRmFjdG9yeSxcbiAgICBkYXRhVHlwZTogJ3N0cmluZycsXG4gICAgZG9jdW1lbnRXaWRnZXRGYWN0b3J5T3B0aW9uczoge1xuICAgICAgbmFtZTogJ1BERicsXG4gICAgICBtb2RlbE5hbWU6ICdiYXNlNjQnLFxuICAgICAgcHJpbWFyeUZpbGVUeXBlOiAnUERGJyxcbiAgICAgIGZpbGVUeXBlczogWydQREYnXSxcbiAgICAgIGRlZmF1bHRGb3I6IFsnUERGJ11cbiAgICB9XG4gIH1cbl07XG5cbmV4cG9ydCBkZWZhdWx0IGV4dGVuc2lvbnM7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIFBERiB3aWRnZXQgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBIGZsYWcgZm9yIGRldGVybWluaW5nIHdoZXRoZXIgdGhlIHVzZXIgaXMgdXNpbmcgRmlyZWZveC5cbiAgICogVGhlcmUgYXJlIHNvbWUgZGlmZmVyZW50IFBERiB2aWV3ZXIgYmVoYXZpb3JzIG9uIEZpcmVmb3gsXG4gICAqIGFuZCB3ZSB0cnkgdG8gYWRkcmVzcyB0aGVtIHdpdGggdGhpcy4gVXNlciBhZ2VudCBzdHJpbmcgcGFyc2luZ1xuICAgKiBpcyAqbm90KiByZWxpYWJsZSwgc28gdGhpcyBzaG91bGQgYmUgY29uc2lkZXJlZCBhIGJlc3QtZWZmb3J0IHRlc3QuXG4gICAqL1xuICBleHBvcnQgY29uc3QgSVNfRklSRUZPWDogYm9vbGVhbiA9IC9GaXJlZm94Ly50ZXN0KG5hdmlnYXRvci51c2VyQWdlbnQpO1xuXG4gIC8qKlxuICAgKiBDb252ZXJ0IGEgYmFzZTY0IGVuY29kZWQgc3RyaW5nIHRvIGEgQmxvYiBvYmplY3QuXG4gICAqIE1vZGlmaWVkIGZyb20gYSBzbmlwcGV0IGZvdW5kIGhlcmU6XG4gICAqIGh0dHBzOi8vc3RhY2tvdmVyZmxvdy5jb20vcXVlc3Rpb25zLzE2MjQ1NzY3L2NyZWF0aW5nLWEtYmxvYi1mcm9tLWEtYmFzZTY0LXN0cmluZy1pbi1qYXZhc2NyaXB0XG4gICAqXG4gICAqIEBwYXJhbSBiNjREYXRhIC0gVGhlIGJhc2U2NCBlbmNvZGVkIGRhdGEuXG4gICAqXG4gICAqIEBwYXJhbSBjb250ZW50VHlwZSAtIFRoZSBtaW1lIHR5cGUgb2YgdGhlIGRhdGEuXG4gICAqXG4gICAqIEBwYXJhbSBzbGljZVNpemUgLSBUaGUgc2l6ZSB0byBjaHVuayB0aGUgZGF0YSBpbnRvIGZvciBwcm9jZXNzaW5nLlxuICAgKlxuICAgKiBAcmV0dXJucyBhIEJsb2IgZm9yIHRoZSBkYXRhLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGI2NHRvQmxvYihcbiAgICBiNjREYXRhOiBzdHJpbmcsXG4gICAgY29udGVudFR5cGU6IHN0cmluZyA9ICcnLFxuICAgIHNsaWNlU2l6ZTogbnVtYmVyID0gNTEyXG4gICk6IEJsb2Ige1xuICAgIGNvbnN0IGJ5dGVDaGFyYWN0ZXJzID0gYXRvYihiNjREYXRhKTtcbiAgICBjb25zdCBieXRlQXJyYXlzOiBVaW50OEFycmF5W10gPSBbXTtcblxuICAgIGZvciAobGV0IG9mZnNldCA9IDA7IG9mZnNldCA8IGJ5dGVDaGFyYWN0ZXJzLmxlbmd0aDsgb2Zmc2V0ICs9IHNsaWNlU2l6ZSkge1xuICAgICAgY29uc3Qgc2xpY2UgPSBieXRlQ2hhcmFjdGVycy5zbGljZShvZmZzZXQsIG9mZnNldCArIHNsaWNlU2l6ZSk7XG5cbiAgICAgIGNvbnN0IGJ5dGVOdW1iZXJzID0gbmV3IEFycmF5KHNsaWNlLmxlbmd0aCk7XG4gICAgICBmb3IgKGxldCBpID0gMDsgaSA8IHNsaWNlLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIGJ5dGVOdW1iZXJzW2ldID0gc2xpY2UuY2hhckNvZGVBdChpKTtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGJ5dGVBcnJheSA9IG5ldyBVaW50OEFycmF5KGJ5dGVOdW1iZXJzKTtcbiAgICAgIGJ5dGVBcnJheXMucHVzaChieXRlQXJyYXkpO1xuICAgIH1cblxuICAgIHJldHVybiBuZXcgQmxvYihieXRlQXJyYXlzLCB7IHR5cGU6IGNvbnRlbnRUeXBlIH0pO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9