(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_imageviewer_lib_index_js-_2b930"],{

/***/ "../packages/imageviewer/lib/index.js":
/*!********************************************!*\
  !*** ../packages/imageviewer/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IImageTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.IImageTracker),
/* harmony export */   "ImageViewer": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.ImageViewer),
/* harmony export */   "ImageViewerFactory": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.ImageViewerFactory)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "../packages/imageviewer/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/imageviewer/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module imageviewer
 */




/***/ }),

/***/ "../packages/imageviewer/lib/tokens.js":
/*!*********************************************!*\
  !*** ../packages/imageviewer/lib/tokens.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IImageTracker": () => (/* binding */ IImageTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The image tracker token.
 */
const IImageTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/imageviewer:IImageTracker');
/* tslint:enable */


/***/ }),

/***/ "../packages/imageviewer/lib/widget.js":
/*!*********************************************!*\
  !*** ../packages/imageviewer/lib/widget.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ImageViewer": () => (/* binding */ ImageViewer),
/* harmony export */   "ImageViewerFactory": () => (/* binding */ ImageViewerFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The class name added to a imageviewer.
 */
const IMAGE_CLASS = 'jp-ImageViewer';
/**
 * A widget for images.
 */
class ImageViewer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Construct a new image widget.
     */
    constructor(context) {
        super();
        this._scale = 1;
        this._matrix = [1, 0, 0, 1];
        this._colorinversion = 0;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.PromiseDelegate();
        this.context = context;
        this.node.tabIndex = 0;
        this.addClass(IMAGE_CLASS);
        this._img = document.createElement('img');
        this.node.appendChild(this._img);
        this._onTitleChanged();
        context.pathChanged.connect(this._onTitleChanged, this);
        void context.ready.then(() => {
            if (this.isDisposed) {
                return;
            }
            const contents = context.contentsModel;
            this._mimeType = contents.mimetype;
            this._render();
            context.model.contentChanged.connect(this.update, this);
            context.fileChanged.connect(this.update, this);
            this._ready.resolve(void 0);
        });
    }
    /**
     * Print in iframe.
     */
    [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Printing.symbol]() {
        return () => _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Printing.printWidget(this);
    }
    /**
     * A promise that resolves when the image viewer is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * The scale factor for the image.
     */
    get scale() {
        return this._scale;
    }
    set scale(value) {
        if (value === this._scale) {
            return;
        }
        this._scale = value;
        this._updateStyle();
    }
    /**
     * The color inversion of the image.
     */
    get colorinversion() {
        return this._colorinversion;
    }
    set colorinversion(value) {
        if (value === this._colorinversion) {
            return;
        }
        this._colorinversion = value;
        this._updateStyle();
    }
    /**
     * Dispose of resources held by the image viewer.
     */
    dispose() {
        if (this._img.src) {
            URL.revokeObjectURL(this._img.src || '');
        }
        super.dispose();
    }
    /**
     * Reset rotation and flip transformations.
     */
    resetRotationFlip() {
        this._matrix = [1, 0, 0, 1];
        this._updateStyle();
    }
    /**
     * Rotate the image counter-clockwise (left).
     */
    rotateCounterclockwise() {
        this._matrix = Private.prod(this._matrix, Private.rotateCounterclockwiseMatrix);
        this._updateStyle();
    }
    /**
     * Rotate the image clockwise (right).
     */
    rotateClockwise() {
        this._matrix = Private.prod(this._matrix, Private.rotateClockwiseMatrix);
        this._updateStyle();
    }
    /**
     * Flip the image horizontally.
     */
    flipHorizontal() {
        this._matrix = Private.prod(this._matrix, Private.flipHMatrix);
        this._updateStyle();
    }
    /**
     * Flip the image vertically.
     */
    flipVertical() {
        this._matrix = Private.prod(this._matrix, Private.flipVMatrix);
        this._updateStyle();
    }
    /**
     * Handle `update-request` messages for the widget.
     */
    onUpdateRequest(msg) {
        if (this.isDisposed || !this.context.isReady) {
            return;
        }
        this._render();
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.focus();
    }
    /**
     * Handle a change to the title.
     */
    _onTitleChanged() {
        this.title.label = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.basename(this.context.localPath);
    }
    /**
     * Render the widget content.
     */
    _render() {
        const context = this.context;
        const cm = context.contentsModel;
        if (!cm) {
            return;
        }
        const oldurl = this._img.src || '';
        let content = context.model.toString();
        if (cm.format === 'base64') {
            this._img.src = `data:${this._mimeType};base64,${content}`;
        }
        else {
            const a = new Blob([content], { type: this._mimeType });
            this._img.src = URL.createObjectURL(a);
        }
        URL.revokeObjectURL(oldurl);
    }
    /**
     * Update the image CSS style, including the transform and filter.
     */
    _updateStyle() {
        const [a, b, c, d] = this._matrix;
        const [tX, tY] = Private.prodVec(this._matrix, [1, 1]);
        const transform = `matrix(${a}, ${b}, ${c}, ${d}, 0, 0) translate(${tX < 0 ? -100 : 0}%, ${tY < 0 ? -100 : 0}%) `;
        this._img.style.transform = `scale(${this._scale}) ${transform}`;
        this._img.style.filter = `invert(${this._colorinversion})`;
    }
}
/**
 * A widget factory for images.
 */
class ImageViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const content = new ImageViewer(context);
        const widget = new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.DocumentWidget({ content, context });
        return widget;
    }
}
/**
 * A namespace for image widget private data.
 */
var Private;
(function (Private) {
    /**
     * Multiply 2x2 matrices.
     */
    function prod([a11, a12, a21, a22], [b11, b12, b21, b22]) {
        return [
            a11 * b11 + a12 * b21,
            a11 * b12 + a12 * b22,
            a21 * b11 + a22 * b21,
            a21 * b12 + a22 * b22
        ];
    }
    Private.prod = prod;
    /**
     * Multiply a 2x2 matrix and a 2x1 vector.
     */
    function prodVec([a11, a12, a21, a22], [b1, b2]) {
        return [a11 * b1 + a12 * b2, a21 * b1 + a22 * b2];
    }
    Private.prodVec = prodVec;
    /**
     * Clockwise rotation transformation matrix.
     */
    Private.rotateClockwiseMatrix = [0, 1, -1, 0];
    /**
     * Counter-clockwise rotation transformation matrix.
     */
    Private.rotateCounterclockwiseMatrix = [0, -1, 1, 0];
    /**
     * Horizontal flip transformation matrix.
     */
    Private.flipHMatrix = [-1, 0, 0, 1];
    /**
     * Vertical flip transformation matrix.
     */
    Private.flipVMatrix = [1, 0, 0, -1];
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW1hZ2V2aWV3ZXIvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9pbWFnZXZpZXdlci9zcmMvdG9rZW5zLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9pbWFnZXZpZXdlci9zcmMvd2lkZ2V0LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFFc0I7QUFDQTs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDUnpCLDBDQUEwQztBQUMxQywyREFBMkQ7QUFNakI7QUFVMUMsb0JBQW9CO0FBQ3BCOztHQUVHO0FBQ0ksTUFBTSxhQUFhLEdBQUcsSUFBSSxvREFBSyxDQUNwQyx1Q0FBdUMsQ0FDeEMsQ0FBQztBQUNGLG1CQUFtQjs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDeEJuQiwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBRVg7QUFFQTtBQU9mO0FBRW1CO0FBSVg7QUFFekM7O0dBRUc7QUFDSCxNQUFNLFdBQVcsR0FBRyxnQkFBZ0IsQ0FBQztBQUVyQzs7R0FFRztBQUNJLE1BQU0sV0FBWSxTQUFRLG1EQUFNO0lBQ3JDOztPQUVHO0lBQ0gsWUFBWSxPQUFpQztRQUMzQyxLQUFLLEVBQUUsQ0FBQztRQXNMRixXQUFNLEdBQUcsQ0FBQyxDQUFDO1FBQ1gsWUFBTyxHQUFHLENBQUMsQ0FBQyxFQUFFLENBQUMsRUFBRSxDQUFDLEVBQUUsQ0FBQyxDQUFDLENBQUM7UUFDdkIsb0JBQWUsR0FBRyxDQUFDLENBQUM7UUFDcEIsV0FBTSxHQUFHLElBQUksOERBQWUsRUFBUSxDQUFDO1FBeEwzQyxJQUFJLENBQUMsT0FBTyxHQUFHLE9BQU8sQ0FBQztRQUN2QixJQUFJ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QUFJLE9BVW5CO0lBRUQ7O09BRUc7SUFDSCxTQUFnQixPQUFPLENBQ3JCLENBQUMsR0FBRyxFQUFFLEdBQUcsRUFBRSxHQUFHLEVBQUUsR0FBRyxDQUFXLEVBQzlCLENBQUMsRUFBRSxFQUFFLEVBQUUsQ0FBVztRQUVsQixPQUFPLENBQUMsR0FBRyxHQUFHLEVBQUUsR0FBRyxHQUFHLEdBQUcsRUFBRSxFQUFFLEdBQUcsR0FBRyxFQUFFLEdBQUcsR0FBRyxHQUFHLEVBQUUsQ0FBQyxDQUFDO0lBQ3BELENBQUM7SUFMZSxlQUFPLFVBS3RCO0lBRUQ7O09BRUc7SUFDVSw2QkFBcUIsR0FBRyxDQUFDLENBQUMsRUFBRSxDQUFDLEVBQUUsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxDQUFDLENBQUM7SUFFbkQ7O09BRUc7SUFDVSxvQ0FBNEIsR0FBRyxDQUFDLENBQUMsRUFBRSxDQUFDLENBQUMsRUFBRSxDQUFDLEVBQUUsQ0FBQyxDQUFDLENBQUM7SUFFMUQ7O09BRUc7SUFDVSxtQkFBVyxHQUFHLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUFFLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQztJQUV6Qzs7T0FFRztJQUNVLG1CQUFXLEdBQUcsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUFFLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQyxDQUFDO0FBQzNDLENBQUMsRUE3Q1MsT0FBTyxLQUFQLE9BQU8sUUE2Q2hCIiwiZmlsZSI6InBhY2thZ2VzX2ltYWdldmlld2VyX2xpYl9pbmRleF9qcy1fMmI5MzAuZjJhMTVkZmM0ZWQ3YWQwMzE3YTMuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBpbWFnZXZpZXdlclxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vdG9rZW5zJztcbmV4cG9ydCAqIGZyb20gJy4vd2lkZ2V0JztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVdpZGdldFRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5cbmltcG9ydCB7IElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcblxuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5cbmltcG9ydCB7IEltYWdlVmlld2VyIH0gZnJvbSAnLi93aWRnZXQnO1xuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCB0cmFja3MgaW1hZ2Ugd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJSW1hZ2VUcmFja2VyXG4gIGV4dGVuZHMgSVdpZGdldFRyYWNrZXI8SURvY3VtZW50V2lkZ2V0PEltYWdlVmlld2VyPj4ge31cblxuLyogdHNsaW50OmRpc2FibGUgKi9cbi8qKlxuICogVGhlIGltYWdlIHRyYWNrZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJSW1hZ2VUcmFja2VyID0gbmV3IFRva2VuPElJbWFnZVRyYWNrZXI+KFxuICAnQGp1cHl0ZXJsYWIvaW1hZ2V2aWV3ZXI6SUltYWdlVHJhY2tlcidcbik7XG4vKiB0c2xpbnQ6ZW5hYmxlICovXG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFBhdGhFeHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuXG5pbXBvcnQgeyBQcmludGluZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcblxuaW1wb3J0IHtcbiAgQUJDV2lkZ2V0RmFjdG9yeSxcbiAgRG9jdW1lbnRSZWdpc3RyeSxcbiAgRG9jdW1lbnRXaWRnZXQsXG4gIElEb2N1bWVudFdpZGdldFxufSBmcm9tICdAanVweXRlcmxhYi9kb2NyZWdpc3RyeSc7XG5cbmltcG9ydCB7IFByb21pc2VEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcblxuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcblxuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhIGltYWdldmlld2VyLlxuICovXG5jb25zdCBJTUFHRV9DTEFTUyA9ICdqcC1JbWFnZVZpZXdlcic7XG5cbi8qKlxuICogQSB3aWRnZXQgZm9yIGltYWdlcy5cbiAqL1xuZXhwb3J0IGNsYXNzIEltYWdlVmlld2VyIGV4dGVuZHMgV2lkZ2V0IGltcGxlbWVudHMgUHJpbnRpbmcuSVByaW50YWJsZSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgaW1hZ2Ugd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3IoY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0KSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLmNvbnRleHQgPSBjb250ZXh0O1xuICAgIHRoaXMubm9kZS50YWJJbmRleCA9IDA7XG4gICAgdGhpcy5hZGRDbGFzcyhJTUFHRV9DTEFTUyk7XG5cbiAgICB0aGlzLl9pbWcgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdpbWcnKTtcbiAgICB0aGlzLm5vZGUuYXBwZW5kQ2hpbGQodGhpcy5faW1nKTtcblxuICAgIHRoaXMuX29uVGl0bGVDaGFuZ2VkKCk7XG4gICAgY29udGV4dC5wYXRoQ2hhbmdlZC5jb25uZWN0KHRoaXMuX29uVGl0bGVDaGFuZ2VkLCB0aGlzKTtcblxuICAgIHZvaWQgY29udGV4dC5yZWFkeS50aGVuKCgpID0+IHtcbiAgICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgY29udGVudHMgPSBjb250ZXh0LmNvbnRlbnRzTW9kZWwhO1xuICAgICAgdGhpcy5fbWltZVR5cGUgPSBjb250ZW50cy5taW1ldHlwZTtcbiAgICAgIHRoaXMuX3JlbmRlcigpO1xuICAgICAgY29udGV4dC5tb2RlbC5jb250ZW50Q2hhbmdlZC5jb25uZWN0KHRoaXMudXBkYXRlLCB0aGlzKTtcbiAgICAgIGNvbnRleHQuZmlsZUNoYW5nZWQuY29ubmVjdCh0aGlzLnVwZGF0ZSwgdGhpcyk7XG4gICAgICB0aGlzLl9yZWFkeS5yZXNvbHZlKHZvaWQgMCk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogUHJpbnQgaW4gaWZyYW1lLlxuICAgKi9cbiAgW1ByaW50aW5nLnN5bWJvbF0oKSB7XG4gICAgcmV0dXJuICgpID0+IFByaW50aW5nLnByaW50V2lkZ2V0KHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBpbWFnZSB3aWRnZXQncyBjb250ZXh0LlxuICAgKi9cbiAgcmVhZG9ubHkgY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0O1xuXG4gIC8qKlxuICAgKiBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBpbWFnZSB2aWV3ZXIgaXMgcmVhZHkuXG4gICAqL1xuICBnZXQgcmVhZHkoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3JlYWR5LnByb21pc2U7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNjYWxlIGZhY3RvciBmb3IgdGhlIGltYWdlLlxuICAgKi9cbiAgZ2V0IHNjYWxlKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX3NjYWxlO1xuICB9XG4gIHNldCBzY2FsZSh2YWx1ZTogbnVtYmVyKSB7XG4gICAgaWYgKHZhbHVlID09PSB0aGlzLl9zY2FsZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9zY2FsZSA9IHZhbHVlO1xuICAgIHRoaXMuX3VwZGF0ZVN0eWxlKCk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGNvbG9yIGludmVyc2lvbiBvZiB0aGUgaW1hZ2UuXG4gICAqL1xuICBnZXQgY29sb3JpbnZlcnNpb24oKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy5fY29sb3JpbnZlcnNpb247XG4gIH1cbiAgc2V0IGNvbG9yaW52ZXJzaW9uKHZhbHVlOiBudW1iZXIpIHtcbiAgICBpZiAodmFsdWUgPT09IHRoaXMuX2NvbG9yaW52ZXJzaW9uKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2NvbG9yaW52ZXJzaW9uID0gdmFsdWU7XG4gICAgdGhpcy5fdXBkYXRlU3R5bGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBpbWFnZSB2aWV3ZXIuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9pbWcuc3JjKSB7XG4gICAgICBVUkwucmV2b2tlT2JqZWN0VVJMKHRoaXMuX2ltZy5zcmMgfHwgJycpO1xuICAgIH1cbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogUmVzZXQgcm90YXRpb24gYW5kIGZsaXAgdHJhbnNmb3JtYXRpb25zLlxuICAgKi9cbiAgcmVzZXRSb3RhdGlvbkZsaXAoKTogdm9pZCB7XG4gICAgdGhpcy5fbWF0cml4ID0gWzEsIDAsIDAsIDFdO1xuICAgIHRoaXMuX3VwZGF0ZVN0eWxlKCk7XG4gIH1cblxuICAvKipcbiAgICogUm90YXRlIHRoZSBpbWFnZSBjb3VudGVyLWNsb2Nrd2lzZSAobGVmdCkuXG4gICAqL1xuICByb3RhdGVDb3VudGVyY2xvY2t3aXNlKCk6IHZvaWQge1xuICAgIHRoaXMuX21hdHJpeCA9IFByaXZhdGUucHJvZChcbiAgICAgIHRoaXMuX21hdHJpeCxcbiAgICAgIFByaXZhdGUucm90YXRlQ291bnRlcmNsb2Nrd2lzZU1hdHJpeFxuICAgICk7XG4gICAgdGhpcy5fdXBkYXRlU3R5bGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSb3RhdGUgdGhlIGltYWdlIGNsb2Nrd2lzZSAocmlnaHQpLlxuICAgKi9cbiAgcm90YXRlQ2xvY2t3aXNlKCk6IHZvaWQge1xuICAgIHRoaXMuX21hdHJpeCA9IFByaXZhdGUucHJvZCh0aGlzLl9tYXRyaXgsIFByaXZhdGUucm90YXRlQ2xvY2t3aXNlTWF0cml4KTtcbiAgICB0aGlzLl91cGRhdGVTdHlsZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEZsaXAgdGhlIGltYWdlIGhvcml6b250YWxseS5cbiAgICovXG4gIGZsaXBIb3Jpem9udGFsKCk6IHZvaWQge1xuICAgIHRoaXMuX21hdHJpeCA9IFByaXZhdGUucHJvZCh0aGlzLl9tYXRyaXgsIFByaXZhdGUuZmxpcEhNYXRyaXgpO1xuICAgIHRoaXMuX3VwZGF0ZVN0eWxlKCk7XG4gIH1cblxuICAvKipcbiAgICogRmxpcCB0aGUgaW1hZ2UgdmVydGljYWxseS5cbiAgICovXG4gIGZsaXBWZXJ0aWNhbCgpOiB2b2lkIHtcbiAgICB0aGlzLl9tYXRyaXggPSBQcml2YXRlLnByb2QodGhpcy5fbWF0cml4LCBQcml2YXRlLmZsaXBWTWF0cml4KTtcbiAgICB0aGlzLl91cGRhdGVTdHlsZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgdXBkYXRlLXJlcXVlc3RgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uVXBkYXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkIHx8ICF0aGlzLmNvbnRleHQuaXNSZWFkeSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9yZW5kZXIoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhY3RpdmF0ZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5ub2RlLmZvY3VzKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSB0aXRsZS5cbiAgICovXG4gIHByaXZhdGUgX29uVGl0bGVDaGFuZ2VkKCk6IHZvaWQge1xuICAgIHRoaXMudGl0bGUubGFiZWwgPSBQYXRoRXh0LmJhc2VuYW1lKHRoaXMuY29udGV4dC5sb2NhbFBhdGgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciB0aGUgd2lkZ2V0IGNvbnRlbnQuXG4gICAqL1xuICBwcml2YXRlIF9yZW5kZXIoKTogdm9pZCB7XG4gICAgY29uc3QgY29udGV4dCA9IHRoaXMuY29udGV4dDtcbiAgICBjb25zdCBjbSA9IGNvbnRleHQuY29udGVudHNNb2RlbDtcbiAgICBpZiAoIWNtKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IG9sZHVybCA9IHRoaXMuX2ltZy5zcmMgfHwgJyc7XG4gICAgbGV0IGNvbnRlbnQgPSBjb250ZXh0Lm1vZGVsLnRvU3RyaW5nKCk7XG4gICAgaWYgKGNtLmZvcm1hdCA9PT0gJ2Jhc2U2NCcpIHtcbiAgICAgIHRoaXMuX2ltZy5zcmMgPSBgZGF0YToke3RoaXMuX21pbWVUeXBlfTtiYXNlNjQsJHtjb250ZW50fWA7XG4gICAgfSBlbHNlIHtcbiAgICAgIGNvbnN0IGEgPSBuZXcgQmxvYihbY29udGVudF0sIHsgdHlwZTogdGhpcy5fbWltZVR5cGUgfSk7XG4gICAgICB0aGlzLl9pbWcuc3JjID0gVVJMLmNyZWF0ZU9iamVjdFVSTChhKTtcbiAgICB9XG4gICAgVVJMLnJldm9rZU9iamVjdFVSTChvbGR1cmwpO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgaW1hZ2UgQ1NTIHN0eWxlLCBpbmNsdWRpbmcgdGhlIHRyYW5zZm9ybSBhbmQgZmlsdGVyLlxuICAgKi9cbiAgcHJpdmF0ZSBfdXBkYXRlU3R5bGUoKTogdm9pZCB7XG4gICAgY29uc3QgW2EsIGIsIGMsIGRdID0gdGhpcy5fbWF0cml4O1xuICAgIGNvbnN0IFt0WCwgdFldID0gUHJpdmF0ZS5wcm9kVmVjKHRoaXMuX21hdHJpeCwgWzEsIDFdKTtcbiAgICBjb25zdCB0cmFuc2Zvcm0gPSBgbWF0cml4KCR7YX0sICR7Yn0sICR7Y30sICR7ZH0sIDAsIDApIHRyYW5zbGF0ZSgke1xuICAgICAgdFggPCAwID8gLTEwMCA6IDBcbiAgICB9JSwgJHt0WSA8IDAgPyAtMTAwIDogMH0lKSBgO1xuICAgIHRoaXMuX2ltZy5zdHlsZS50cmFuc2Zvcm0gPSBgc2NhbGUoJHt0aGlzLl9zY2FsZX0pICR7dHJhbnNmb3JtfWA7XG4gICAgdGhpcy5faW1nLnN0eWxlLmZpbHRlciA9IGBpbnZlcnQoJHt0aGlzLl9jb2xvcmludmVyc2lvbn0pYDtcbiAgfVxuXG4gIHByaXZhdGUgX21pbWVUeXBlOiBzdHJpbmc7XG4gIHByaXZhdGUgX3NjYWxlID0gMTtcbiAgcHJpdmF0ZSBfbWF0cml4ID0gWzEsIDAsIDAsIDFdO1xuICBwcml2YXRlIF9jb2xvcmludmVyc2lvbiA9IDA7XG4gIHByaXZhdGUgX3JlYWR5ID0gbmV3IFByb21pc2VEZWxlZ2F0ZTx2b2lkPigpO1xuICBwcml2YXRlIF9pbWc6IEhUTUxJbWFnZUVsZW1lbnQ7XG59XG5cbi8qKlxuICogQSB3aWRnZXQgZmFjdG9yeSBmb3IgaW1hZ2VzLlxuICovXG5leHBvcnQgY2xhc3MgSW1hZ2VWaWV3ZXJGYWN0b3J5IGV4dGVuZHMgQUJDV2lkZ2V0RmFjdG9yeTxcbiAgSURvY3VtZW50V2lkZ2V0PEltYWdlVmlld2VyPlxuPiB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgd2lkZ2V0IGdpdmVuIGEgY29udGV4dC5cbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVOZXdXaWRnZXQoXG4gICAgY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5JQ29udGV4dDxEb2N1bWVudFJlZ2lzdHJ5LklNb2RlbD5cbiAgKTogSURvY3VtZW50V2lkZ2V0PEltYWdlVmlld2VyPiB7XG4gICAgY29uc3QgY29udGVudCA9IG5ldyBJbWFnZVZpZXdlcihjb250ZXh0KTtcbiAgICBjb25zdCB3aWRnZXQgPSBuZXcgRG9jdW1lbnRXaWRnZXQoeyBjb250ZW50LCBjb250ZXh0IH0pO1xuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgaW1hZ2Ugd2lkZ2V0IHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogTXVsdGlwbHkgMngyIG1hdHJpY2VzLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHByb2QoXG4gICAgW2ExMSwgYTEyLCBhMjEsIGEyMl06IG51bWJlcltdLFxuICAgIFtiMTEsIGIxMiwgYjIxLCBiMjJdOiBudW1iZXJbXVxuICApOiBudW1iZXJbXSB7XG4gICAgcmV0dXJuIFtcbiAgICAgIGExMSAqIGIxMSArIGExMiAqIGIyMSxcbiAgICAgIGExMSAqIGIxMiArIGExMiAqIGIyMixcbiAgICAgIGEyMSAqIGIxMSArIGEyMiAqIGIyMSxcbiAgICAgIGEyMSAqIGIxMiArIGEyMiAqIGIyMlxuICAgIF07XG4gIH1cblxuICAvKipcbiAgICogTXVsdGlwbHkgYSAyeDIgbWF0cml4IGFuZCBhIDJ4MSB2ZWN0b3IuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcHJvZFZlYyhcbiAgICBbYTExLCBhMTIsIGEyMSwgYTIyXTogbnVtYmVyW10sXG4gICAgW2IxLCBiMl06IG51bWJlcltdXG4gICk6IG51bWJlcltdIHtcbiAgICByZXR1cm4gW2ExMSAqIGIxICsgYTEyICogYjIsIGEyMSAqIGIxICsgYTIyICogYjJdO1xuICB9XG5cbiAgLyoqXG4gICAqIENsb2Nrd2lzZSByb3RhdGlvbiB0cmFuc2Zvcm1hdGlvbiBtYXRyaXguXG4gICAqL1xuICBleHBvcnQgY29uc3Qgcm90YXRlQ2xvY2t3aXNlTWF0cml4ID0gWzAsIDEsIC0xLCAwXTtcblxuICAvKipcbiAgICogQ291bnRlci1jbG9ja3dpc2Ugcm90YXRpb24gdHJhbnNmb3JtYXRpb24gbWF0cml4LlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IHJvdGF0ZUNvdW50ZXJjbG9ja3dpc2VNYXRyaXggPSBbMCwgLTEsIDEsIDBdO1xuXG4gIC8qKlxuICAgKiBIb3Jpem9udGFsIGZsaXAgdHJhbnNmb3JtYXRpb24gbWF0cml4LlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGZsaXBITWF0cml4ID0gWy0xLCAwLCAwLCAxXTtcblxuICAvKipcbiAgICogVmVydGljYWwgZmxpcCB0cmFuc2Zvcm1hdGlvbiBtYXRyaXguXG4gICAqL1xuICBleHBvcnQgY29uc3QgZmxpcFZNYXRyaXggPSBbMSwgMCwgMCwgLTFdO1xufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==