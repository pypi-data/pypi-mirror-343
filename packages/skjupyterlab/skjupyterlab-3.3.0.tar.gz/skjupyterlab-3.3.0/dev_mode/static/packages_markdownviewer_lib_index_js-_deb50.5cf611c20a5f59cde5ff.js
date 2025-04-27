(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_markdownviewer_lib_index_js-_deb50"],{

/***/ "../packages/markdownviewer/lib/index.js":
/*!***********************************************!*\
  !*** ../packages/markdownviewer/lib/index.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMarkdownViewerTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.IMarkdownViewerTracker),
/* harmony export */   "MarkdownDocument": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.MarkdownDocument),
/* harmony export */   "MarkdownViewer": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.MarkdownViewer),
/* harmony export */   "MarkdownViewerFactory": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.MarkdownViewerFactory)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "../packages/markdownviewer/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/markdownviewer/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module markdownviewer
 */




/***/ }),

/***/ "../packages/markdownviewer/lib/tokens.js":
/*!************************************************!*\
  !*** ../packages/markdownviewer/lib/tokens.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMarkdownViewerTracker": () => (/* binding */ IMarkdownViewerTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The markdownviewer tracker token.
 */
const IMarkdownViewerTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/markdownviewer:IMarkdownViewerTracker');


/***/ }),

/***/ "../packages/markdownviewer/lib/widget.js":
/*!************************************************!*\
  !*** ../packages/markdownviewer/lib/widget.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MarkdownViewer": () => (/* binding */ MarkdownViewer),
/* harmony export */   "MarkdownDocument": () => (/* binding */ MarkdownDocument),
/* harmony export */   "MarkdownViewerFactory": () => (/* binding */ MarkdownViewerFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * The class name added to a markdown viewer.
 */
const MARKDOWNVIEWER_CLASS = 'jp-MarkdownViewer';
/**
 * The markdown MIME type.
 */
const MIMETYPE = 'text/markdown';
/**
 * A widget for markdown documents.
 */
class MarkdownViewer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget {
    /**
     * Construct a new markdown viewer widget.
     */
    constructor(options) {
        super();
        this._config = Object.assign({}, MarkdownViewer.defaultConfig);
        this._fragment = '';
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.PromiseDelegate();
        this._isRendering = false;
        this._renderRequested = false;
        this.context = options.context;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.renderer = options.renderer;
        this.node.tabIndex = 0;
        this.addClass(MARKDOWNVIEWER_CLASS);
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.StackedLayout());
        layout.addWidget(this.renderer);
        void this.context.ready.then(async () => {
            await this._render();
            // Throttle the rendering rate of the widget.
            this._monitor = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.ActivityMonitor({
                signal: this.context.model.contentChanged,
                timeout: this._config.renderTimeout
            });
            this._monitor.activityStopped.connect(this.update, this);
            this._ready.resolve(undefined);
        });
    }
    /**
     * A promise that resolves when the markdown viewer is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Set URI fragment identifier.
     */
    setFragment(fragment) {
        this._fragment = fragment;
        this.update();
    }
    /**
     * Set a config option for the markdown viewer.
     */
    setOption(option, value) {
        if (this._config[option] === value) {
            return;
        }
        this._config[option] = value;
        const { style } = this.renderer.node;
        switch (option) {
            case 'fontFamily':
                style.setProperty('font-family', value);
                break;
            case 'fontSize':
                style.setProperty('font-size', value ? value + 'px' : null);
                break;
            case 'hideFrontMatter':
                this.update();
                break;
            case 'lineHeight':
                style.setProperty('line-height', value ? value.toString() : null);
                break;
            case 'lineWidth': {
                const padding = value ? `calc(50% - ${value / 2}ch)` : null;
                style.setProperty('padding-left', padding);
                style.setProperty('padding-right', padding);
                break;
            }
            case 'renderTimeout':
                if (this._monitor) {
                    this._monitor.timeout = value;
                }
                break;
            default:
                break;
        }
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        if (this._monitor) {
            this._monitor.dispose();
        }
        this._monitor = null;
        super.dispose();
    }
    /**
     * Handle an `update-request` message to the widget.
     */
    onUpdateRequest(msg) {
        if (this.context.isReady && !this.isDisposed) {
            void this._render();
            this._fragment = '';
        }
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.focus();
    }
    /**
     * Render the mime content.
     */
    async _render() {
        if (this.isDisposed) {
            return;
        }
        // Since rendering is async, we note render requests that happen while we
        // actually are rendering for a future rendering.
        if (this._isRendering) {
            this._renderRequested = true;
            return;
        }
        // Set up for this rendering pass.
        this._renderRequested = false;
        const { context } = this;
        const { model } = context;
        const source = model.toString();
        const data = {};
        // If `hideFrontMatter`is true remove front matter.
        data[MIMETYPE] = this._config.hideFrontMatter
            ? Private.removeFrontMatter(source)
            : source;
        const mimeModel = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.MimeModel({
            data,
            metadata: { fragment: this._fragment }
        });
        try {
            // Do the rendering asynchronously.
            this._isRendering = true;
            await this.renderer.renderModel(mimeModel);
            this._isRendering = false;
            // If there is an outstanding request to render, go ahead and render
            if (this._renderRequested) {
                return this._render();
            }
        }
        catch (reason) {
            // Dispose the document if rendering fails.
            requestAnimationFrame(() => {
                this.dispose();
            });
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)(this._trans.__('Renderer Failure: %1', context.path), reason);
        }
    }
}
/**
 * The namespace for MarkdownViewer class statics.
 */
(function (MarkdownViewer) {
    /**
     * The default configuration options for an editor.
     */
    MarkdownViewer.defaultConfig = {
        fontFamily: null,
        fontSize: null,
        lineHeight: null,
        lineWidth: null,
        hideFrontMatter: true,
        renderTimeout: 1000
    };
})(MarkdownViewer || (MarkdownViewer = {}));
/**
 * A document widget for markdown content.
 */
class MarkdownDocument extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.DocumentWidget {
    setFragment(fragment) {
        this.content.setFragment(fragment);
    }
}
/**
 * A widget factory for markdown viewers.
 */
class MarkdownViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.ABCWidgetFactory {
    /**
     * Construct a new markdown viewer widget factory.
     */
    constructor(options) {
        super(Private.createRegistryOptions(options));
        this._fileType = options.primaryFileType;
        this._rendermime = options.rendermime;
    }
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        var _a, _b, _c, _d, _e;
        const rendermime = this._rendermime.clone({
            resolver: context.urlResolver
        });
        const renderer = rendermime.createRenderer(MIMETYPE);
        const content = new MarkdownViewer({ context, renderer });
        content.title.icon = (_a = this._fileType) === null || _a === void 0 ? void 0 : _a.icon;
        content.title.iconClass = (_c = (_b = this._fileType) === null || _b === void 0 ? void 0 : _b.iconClass) !== null && _c !== void 0 ? _c : '';
        content.title.iconLabel = (_e = (_d = this._fileType) === null || _d === void 0 ? void 0 : _d.iconLabel) !== null && _e !== void 0 ? _e : '';
        const widget = new MarkdownDocument({ content, context });
        return widget;
    }
}
/**
 * A namespace for markdown viewer widget private data.
 */
var Private;
(function (Private) {
    /**
     * Create the document registry options.
     */
    function createRegistryOptions(options) {
        return Object.assign(Object.assign({}, options), { readOnly: true });
    }
    Private.createRegistryOptions = createRegistryOptions;
    /**
     * Remove YALM front matter from source.
     */
    function removeFrontMatter(source) {
        const re = /^---\n[^]*?\n(---|...)\n/;
        const match = source.match(re);
        if (!match) {
            return source;
        }
        const { length } = match[0];
        return source.slice(length);
    }
    Private.removeFrontMatter = removeFrontMatter;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFya2Rvd252aWV3ZXIvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYXJrZG93bnZpZXdlci9zcmMvdG9rZW5zLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYXJrZG93bnZpZXdlci9zcmMvd2lkZ2V0LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBRXNCO0FBQ0E7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1J6QiwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBR2pCO0FBRzFDOztHQUVHO0FBQ0ksTUFBTSxzQkFBc0IsR0FBRyxJQUFJLG9EQUFLLENBQzdDLG1EQUFtRCxDQUNwRCxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1pGLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFSDtBQUNBO0FBS3ZCO0FBS0Q7QUFLQztBQUMrQjtBQUVSO0FBRXhEOztHQUVHO0FBQ0gsTUFBTSxvQkFBb0IsR0FBRyxtQkFBbUIsQ0FBQztBQUVqRDs7R0FFRztBQUNILE1BQU0sUUFBUSxHQUFHLGVBQWUsQ0FBQztBQUVqQzs7R0FFRztBQUNJLE1BQU0sY0FBZSxTQUFRLG1EQUFNO0lBQ3hDOztPQUVHO0lBQ0gsWUFBWSxPQUFnQztRQUMxQyxLQUFLLEVBQUUsQ0FBQztRQXdLRixZQUFPLHFCQUFRLGNBQWMsQ0FBQyxhQUFhLEVBQUc7UUFDOUMsY0FBUyxHQUFHLEVBQUUsQ0FBQztRQUVmLFdBQU0sR0FBRyxJQUFJLDhEQUFlLEVBQVEsQ0FBQztRQUNyQyxpQkFBWSxHQUFHLEtBQUssQ0FBQztRQUNyQixxQkFBZ0IsR0FBRyxLQUFLLENBQUM7UUE1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aEIiLCJmaWxlIjoicGFja2FnZXNfbWFya2Rvd252aWV3ZXJfbGliX2luZGV4X2pzLV9kZWI1MC41Y2Y2MTFjMjBhNWY1OWNkZTVmZi5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIG1hcmtkb3dudmlld2VyXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuZXhwb3J0ICogZnJvbSAnLi93aWRnZXQnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJV2lkZ2V0VHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgTWFya2Rvd25Eb2N1bWVudCB9IGZyb20gJy4vd2lkZ2V0JztcblxuLyoqXG4gKiBUaGUgbWFya2Rvd252aWV3ZXIgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElNYXJrZG93blZpZXdlclRyYWNrZXIgPSBuZXcgVG9rZW48SU1hcmtkb3duVmlld2VyVHJhY2tlcj4oXG4gICdAanVweXRlcmxhYi9tYXJrZG93bnZpZXdlcjpJTWFya2Rvd25WaWV3ZXJUcmFja2VyJ1xuKTtcblxuLyoqXG4gKiBBIGNsYXNzIHRoYXQgdHJhY2tzIG1hcmtkb3duIHZpZXdlciB3aWRnZXRzLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElNYXJrZG93blZpZXdlclRyYWNrZXJcbiAgZXh0ZW5kcyBJV2lkZ2V0VHJhY2tlcjxNYXJrZG93bkRvY3VtZW50PiB7fVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBzaG93RXJyb3JNZXNzYWdlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgQWN0aXZpdHlNb25pdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIEFCQ1dpZGdldEZhY3RvcnksXG4gIERvY3VtZW50UmVnaXN0cnksXG4gIERvY3VtZW50V2lkZ2V0XG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIElSZW5kZXJNaW1lLFxuICBJUmVuZGVyTWltZVJlZ2lzdHJ5LFxuICBNaW1lTW9kZWxcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IEpTT05PYmplY3QsIFByb21pc2VEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBTdGFja2VkTGF5b3V0LCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgbWFya2Rvd24gdmlld2VyLlxuICovXG5jb25zdCBNQVJLRE9XTlZJRVdFUl9DTEFTUyA9ICdqcC1NYXJrZG93blZpZXdlcic7XG5cbi8qKlxuICogVGhlIG1hcmtkb3duIE1JTUUgdHlwZS5cbiAqL1xuY29uc3QgTUlNRVRZUEUgPSAndGV4dC9tYXJrZG93bic7XG5cbi8qKlxuICogQSB3aWRnZXQgZm9yIG1hcmtkb3duIGRvY3VtZW50cy5cbiAqL1xuZXhwb3J0IGNsYXNzIE1hcmtkb3duVmlld2VyIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBtYXJrZG93biB2aWV3ZXIgd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogTWFya2Rvd25WaWV3ZXIuSU9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuY29udGV4dCA9IG9wdGlvbnMuY29udGV4dDtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5fdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIHRoaXMucmVuZGVyZXIgPSBvcHRpb25zLnJlbmRlcmVyO1xuICAgIHRoaXMubm9kZS50YWJJbmRleCA9IDA7XG4gICAgdGhpcy5hZGRDbGFzcyhNQVJLRE9XTlZJRVdFUl9DTEFTUyk7XG5cbiAgICBjb25zdCBsYXlvdXQgPSAodGhpcy5sYXlvdXQgPSBuZXcgU3RhY2tlZExheW91dCgpKTtcbiAgICBsYXlvdXQuYWRkV2lkZ2V0KHRoaXMucmVuZGVyZXIpO1xuXG4gICAgdm9pZCB0aGlzLmNvbnRleHQucmVhZHkudGhlbihhc3luYyAoKSA9PiB7XG4gICAgICBhd2FpdCB0aGlzLl9yZW5kZXIoKTtcblxuICAgICAgLy8gVGhyb3R0bGUgdGhlIHJlbmRlcmluZyByYXRlIG9mIHRoZSB3aWRnZXQuXG4gICAgICB0aGlzLl9tb25pdG9yID0gbmV3IEFjdGl2aXR5TW9uaXRvcih7XG4gICAgICAgIHNpZ25hbDogdGhpcy5jb250ZXh0Lm1vZGVsLmNvbnRlbnRDaGFuZ2VkLFxuICAgICAgICB0aW1lb3V0OiB0aGlzLl9jb25maWcucmVuZGVyVGltZW91dFxuICAgICAgfSk7XG4gICAgICB0aGlzLl9tb25pdG9yLmFjdGl2aXR5U3RvcHBlZC5jb25uZWN0KHRoaXMudXBkYXRlLCB0aGlzKTtcblxuICAgICAgdGhpcy5fcmVhZHkucmVzb2x2ZSh1bmRlZmluZWQpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIG1hcmtkb3duIHZpZXdlciBpcyByZWFkeS5cbiAgICovXG4gIGdldCByZWFkeSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fcmVhZHkucHJvbWlzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgVVJJIGZyYWdtZW50IGlkZW50aWZpZXIuXG4gICAqL1xuICBzZXRGcmFnbWVudChmcmFnbWVudDogc3RyaW5nKSB7XG4gICAgdGhpcy5fZnJhZ21lbnQgPSBmcmFnbWVudDtcbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCBhIGNvbmZpZyBvcHRpb24gZm9yIHRoZSBtYXJrZG93biB2aWV3ZXIuXG4gICAqL1xuICBzZXRPcHRpb248SyBleHRlbmRzIGtleW9mIE1hcmtkb3duVmlld2VyLklDb25maWc+KFxuICAgIG9wdGlvbjogSyxcbiAgICB2YWx1ZTogTWFya2Rvd25WaWV3ZXIuSUNvbmZpZ1tLXVxuICApOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fY29uZmlnW29wdGlvbl0gPT09IHZhbHVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2NvbmZpZ1tvcHRpb25dID0gdmFsdWU7XG4gICAgY29uc3QgeyBzdHlsZSB9ID0gdGhpcy5yZW5kZXJlci5ub2RlO1xuICAgIHN3aXRjaCAob3B0aW9uKSB7XG4gICAgICBjYXNlICdmb250RmFtaWx5JzpcbiAgICAgICAgc3R5bGUuc2V0UHJvcGVydHkoJ2ZvbnQtZmFtaWx5JywgdmFsdWUgYXMgc3RyaW5nIHwgbnVsbCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnZm9udFNpemUnOlxuICAgICAgICBzdHlsZS5zZXRQcm9wZXJ0eSgnZm9udC1zaXplJywgdmFsdWUgPyB2YWx1ZSArICdweCcgOiBudWxsKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdoaWRlRnJvbnRNYXR0ZXInOlxuICAgICAgICB0aGlzLnVwZGF0ZSgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2xpbmVIZWlnaHQnOlxuICAgICAgICBzdHlsZS5zZXRQcm9wZXJ0eSgnbGluZS1oZWlnaHQnLCB2YWx1ZSA/IHZhbHVlLnRvU3RyaW5nKCkgOiBudWxsKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdsaW5lV2lkdGgnOiB7XG4gICAgICAgIGNvbnN0IHBhZGRpbmcgPSB2YWx1ZSA/IGBjYWxjKDUwJSAtICR7KHZhbHVlIGFzIG51bWJlcikgLyAyfWNoKWAgOiBudWxsO1xuICAgICAgICBzdHlsZS5zZXRQcm9wZXJ0eSgncGFkZGluZy1sZWZ0JywgcGFkZGluZyk7XG4gICAgICAgIHN0eWxlLnNldFByb3BlcnR5KCdwYWRkaW5nLXJpZ2h0JywgcGFkZGluZyk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgY2FzZSAncmVuZGVyVGltZW91dCc6XG4gICAgICAgIGlmICh0aGlzLl9tb25pdG9yKSB7XG4gICAgICAgICAgdGhpcy5fbW9uaXRvci50aW1lb3V0ID0gdmFsdWUgYXMgbnVtYmVyO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSB3aWRnZXQuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgaWYgKHRoaXMuX21vbml0b3IpIHtcbiAgICAgIHRoaXMuX21vbml0b3IuZGlzcG9zZSgpO1xuICAgIH1cbiAgICB0aGlzLl9tb25pdG9yID0gbnVsbDtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGFuIGB1cGRhdGUtcmVxdWVzdGAgbWVzc2FnZSB0byB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uVXBkYXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5jb250ZXh0LmlzUmVhZHkgJiYgIXRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgdm9pZCB0aGlzLl9yZW5kZXIoKTtcbiAgICAgIHRoaXMuX2ZyYWdtZW50ID0gJyc7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ2FjdGl2YXRlLXJlcXVlc3QnYCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFjdGl2YXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLm5vZGUuZm9jdXMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgdGhlIG1pbWUgY29udGVudC5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX3JlbmRlcigpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gU2luY2UgcmVuZGVyaW5nIGlzIGFzeW5jLCB3ZSBub3RlIHJlbmRlciByZXF1ZXN0cyB0aGF0IGhhcHBlbiB3aGlsZSB3ZVxuICAgIC8vIGFjdHVhbGx5IGFyZSByZW5kZXJpbmcgZm9yIGEgZnV0dXJlIHJlbmRlcmluZy5cbiAgICBpZiAodGhpcy5faXNSZW5kZXJpbmcpIHtcbiAgICAgIHRoaXMuX3JlbmRlclJlcXVlc3RlZCA9IHRydWU7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gU2V0IHVwIGZvciB0aGlzIHJlbmRlcmluZyBwYXNzLlxuICAgIHRoaXMuX3JlbmRlclJlcXVlc3RlZCA9IGZhbHNlO1xuICAgIGNvbnN0IHsgY29udGV4dCB9ID0gdGhpcztcbiAgICBjb25zdCB7IG1vZGVsIH0gPSBjb250ZXh0O1xuICAgIGNvbnN0IHNvdXJjZSA9IG1vZGVsLnRvU3RyaW5nKCk7XG4gICAgY29uc3QgZGF0YTogSlNPTk9iamVjdCA9IHt9O1xuICAgIC8vIElmIGBoaWRlRnJvbnRNYXR0ZXJgaXMgdHJ1ZSByZW1vdmUgZnJvbnQgbWF0dGVyLlxuICAgIGRhdGFbTUlNRVRZUEVdID0gdGhpcy5fY29uZmlnLmhpZGVGcm9udE1hdHRlclxuICAgICAgPyBQcml2YXRlLnJlbW92ZUZyb250TWF0dGVyKHNvdXJjZSlcbiAgICAgIDogc291cmNlO1xuICAgIGNvbnN0IG1pbWVNb2RlbCA9IG5ldyBNaW1lTW9kZWwoe1xuICAgICAgZGF0YSxcbiAgICAgIG1ldGFkYXRhOiB7IGZyYWdtZW50OiB0aGlzLl9mcmFnbWVudCB9XG4gICAgfSk7XG5cbiAgICB0cnkge1xuICAgICAgLy8gRG8gdGhlIHJlbmRlcmluZyBhc3luY2hyb25vdXNseS5cbiAgICAgIHRoaXMuX2lzUmVuZGVyaW5nID0gdHJ1ZTtcbiAgICAgIGF3YWl0IHRoaXMucmVuZGVyZXIucmVuZGVyTW9kZWwobWltZU1vZGVsKTtcbiAgICAgIHRoaXMuX2lzUmVuZGVyaW5nID0gZmFsc2U7XG5cbiAgICAgIC8vIElmIHRoZXJlIGlzIGFuIG91dHN0YW5kaW5nIHJlcXVlc3QgdG8gcmVuZGVyLCBnbyBhaGVhZCBhbmQgcmVuZGVyXG4gICAgICBpZiAodGhpcy5fcmVuZGVyUmVxdWVzdGVkKSB7XG4gICAgICAgIHJldHVybiB0aGlzLl9yZW5kZXIoKTtcbiAgICAgIH1cbiAgICB9IGNhdGNoIChyZWFzb24pIHtcbiAgICAgIC8vIERpc3Bvc2UgdGhlIGRvY3VtZW50IGlmIHJlbmRlcmluZyBmYWlscy5cbiAgICAgIHJlcXVlc3RBbmltYXRpb25GcmFtZSgoKSA9PiB7XG4gICAgICAgIHRoaXMuZGlzcG9zZSgpO1xuICAgICAgfSk7XG4gICAgICB2b2lkIHNob3dFcnJvck1lc3NhZ2UoXG4gICAgICAgIHRoaXMuX3RyYW5zLl9fKCdSZW5kZXJlciBGYWlsdXJlOiAlMScsIGNvbnRleHQucGF0aCksXG4gICAgICAgIHJlYXNvblxuICAgICAgKTtcbiAgICB9XG4gIH1cblxuICByZWFkb25seSBjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQ7XG4gIHJlYWRvbmx5IHJlbmRlcmVyOiBJUmVuZGVyTWltZS5JUmVuZGVyZXI7XG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF9jb25maWcgPSB7IC4uLk1hcmtkb3duVmlld2VyLmRlZmF1bHRDb25maWcgfTtcbiAgcHJpdmF0ZSBfZnJhZ21lbnQgPSAnJztcbiAgcHJpdmF0ZSBfbW9uaXRvcjogQWN0aXZpdHlNb25pdG9yPERvY3VtZW50UmVnaXN0cnkuSU1vZGVsLCB2b2lkPiB8IG51bGw7XG4gIHByaXZhdGUgX3JlYWR5ID0gbmV3IFByb21pc2VEZWxlZ2F0ZTx2b2lkPigpO1xuICBwcml2YXRlIF9pc1JlbmRlcmluZyA9IGZhbHNlO1xuICBwcml2YXRlIF9yZW5kZXJSZXF1ZXN0ZWQgPSBmYWxzZTtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBNYXJrZG93blZpZXdlciBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE1hcmtkb3duVmlld2VyIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gaW5pdGlhbGl6ZSBhIE1hcmtkb3duVmlld2VyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogQ29udGV4dFxuICAgICAqL1xuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuSUNvbnRleHQ8RG9jdW1lbnRSZWdpc3RyeS5JTW9kZWw+O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJlbmRlcmVyIGluc3RhbmNlLlxuICAgICAqL1xuICAgIHJlbmRlcmVyOiBJUmVuZGVyTWltZS5JUmVuZGVyZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cblxuICBleHBvcnQgaW50ZXJmYWNlIElDb25maWcge1xuICAgIC8qKlxuICAgICAqIFVzZXIgcHJlZmVycmVkIGZvbnQgZmFtaWx5IGZvciBtYXJrZG93biB2aWV3ZXIuXG4gICAgICovXG4gICAgZm9udEZhbWlseTogc3RyaW5nIHwgbnVsbDtcblxuICAgIC8qKlxuICAgICAqIFVzZXIgcHJlZmVycmVkIHNpemUgaW4gcGl4ZWwgb2YgdGhlIGZvbnQgdXNlZCBpbiBtYXJrZG93biB2aWV3ZXIuXG4gICAgICovXG4gICAgZm9udFNpemU6IG51bWJlciB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBVc2VyIHByZWZlcnJlZCB0ZXh0IGxpbmUgaGVpZ2h0LCBhcyBhIG11bHRpcGxpZXIgb2YgZm9udCBzaXplLlxuICAgICAqL1xuICAgIGxpbmVIZWlnaHQ6IG51bWJlciB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBVc2VyIHByZWZlcnJlZCB0ZXh0IGxpbmUgd2lkdGggZXhwcmVzc2VkIGluIENTUyBjaCB1bml0cy5cbiAgICAgKi9cbiAgICBsaW5lV2lkdGg6IG51bWJlciB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGhpZGUgdGhlIFlBTE0gZnJvbnQgbWF0dGVyLlxuICAgICAqL1xuICAgIGhpZGVGcm9udE1hdHRlcjogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSByZW5kZXIgdGltZW91dC5cbiAgICAgKi9cbiAgICByZW5kZXJUaW1lb3V0OiBudW1iZXI7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRlZmF1bHQgY29uZmlndXJhdGlvbiBvcHRpb25zIGZvciBhbiBlZGl0b3IuXG4gICAqL1xuICBleHBvcnQgY29uc3QgZGVmYXVsdENvbmZpZzogTWFya2Rvd25WaWV3ZXIuSUNvbmZpZyA9IHtcbiAgICBmb250RmFtaWx5OiBudWxsLFxuICAgIGZvbnRTaXplOiBudWxsLFxuICAgIGxpbmVIZWlnaHQ6IG51bGwsXG4gICAgbGluZVdpZHRoOiBudWxsLFxuICAgIGhpZGVGcm9udE1hdHRlcjogdHJ1ZSxcbiAgICByZW5kZXJUaW1lb3V0OiAxMDAwXG4gIH07XG59XG5cbi8qKlxuICogQSBkb2N1bWVudCB3aWRnZXQgZm9yIG1hcmtkb3duIGNvbnRlbnQuXG4gKi9cbmV4cG9ydCBjbGFzcyBNYXJrZG93bkRvY3VtZW50IGV4dGVuZHMgRG9jdW1lbnRXaWRnZXQ8TWFya2Rvd25WaWV3ZXI+IHtcbiAgc2V0RnJhZ21lbnQoZnJhZ21lbnQ6IHN0cmluZyk6IHZvaWQge1xuICAgIHRoaXMuY29udGVudC5zZXRGcmFnbWVudChmcmFnbWVudCk7XG4gIH1cbn1cblxuLyoqXG4gKiBBIHdpZGdldCBmYWN0b3J5IGZvciBtYXJrZG93biB2aWV3ZXJzLlxuICovXG5leHBvcnQgY2xhc3MgTWFya2Rvd25WaWV3ZXJGYWN0b3J5IGV4dGVuZHMgQUJDV2lkZ2V0RmFjdG9yeTxNYXJrZG93bkRvY3VtZW50PiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgbWFya2Rvd24gdmlld2VyIHdpZGdldCBmYWN0b3J5LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogTWFya2Rvd25WaWV3ZXJGYWN0b3J5LklPcHRpb25zKSB7XG4gICAgc3VwZXIoUHJpdmF0ZS5jcmVhdGVSZWdpc3RyeU9wdGlvbnMob3B0aW9ucykpO1xuICAgIHRoaXMuX2ZpbGVUeXBlID0gb3B0aW9ucy5wcmltYXJ5RmlsZVR5cGU7XG4gICAgdGhpcy5fcmVuZGVybWltZSA9IG9wdGlvbnMucmVuZGVybWltZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgd2lkZ2V0IGdpdmVuIGEgY29udGV4dC5cbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVOZXdXaWRnZXQoXG4gICAgY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0XG4gICk6IE1hcmtkb3duRG9jdW1lbnQge1xuICAgIGNvbnN0IHJlbmRlcm1pbWUgPSB0aGlzLl9yZW5kZXJtaW1lLmNsb25lKHtcbiAgICAgIHJlc29sdmVyOiBjb250ZXh0LnVybFJlc29sdmVyXG4gICAgfSk7XG4gICAgY29uc3QgcmVuZGVyZXIgPSByZW5kZXJtaW1lLmNyZWF0ZVJlbmRlcmVyKE1JTUVUWVBFKTtcbiAgICBjb25zdCBjb250ZW50ID0gbmV3IE1hcmtkb3duVmlld2VyKHsgY29udGV4dCwgcmVuZGVyZXIgfSk7XG4gICAgY29udGVudC50aXRsZS5pY29uID0gdGhpcy5fZmlsZVR5cGU/Lmljb24hO1xuICAgIGNvbnRlbnQudGl0bGUuaWNvbkNsYXNzID0gdGhpcy5fZmlsZVR5cGU/Lmljb25DbGFzcyA/PyAnJztcbiAgICBjb250ZW50LnRpdGxlLmljb25MYWJlbCA9IHRoaXMuX2ZpbGVUeXBlPy5pY29uTGFiZWwgPz8gJyc7XG4gICAgY29uc3Qgd2lkZ2V0ID0gbmV3IE1hcmtkb3duRG9jdW1lbnQoeyBjb250ZW50LCBjb250ZXh0IH0pO1xuXG4gICAgcmV0dXJuIHdpZGdldDtcbiAgfVxuXG4gIHByaXZhdGUgX2ZpbGVUeXBlOiBEb2N1bWVudFJlZ2lzdHJ5LklGaWxlVHlwZSB8IHVuZGVmaW5lZDtcbiAgcHJpdmF0ZSBfcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBNYXJrZG93blZpZXdlckZhY3RvcnkgY2xhc3Mgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBNYXJrZG93blZpZXdlckZhY3Rvcnkge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBpbml0aWFsaXplIGEgTWFya2Rvd25WaWV3ZXJGYWN0b3J5LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyBleHRlbmRzIERvY3VtZW50UmVnaXN0cnkuSVdpZGdldEZhY3RvcnlPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgcHJpbWFyeSBmaWxlIHR5cGUgYXNzb2NpYXRlZCB3aXRoIHRoZSBkb2N1bWVudC5cbiAgICAgKi9cbiAgICBwcmltYXJ5RmlsZVR5cGU6IERvY3VtZW50UmVnaXN0cnkuSUZpbGVUeXBlIHwgdW5kZWZpbmVkO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJlbmRlcm1pbWUgaW5zdGFuY2UuXG4gICAgICovXG4gICAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBtYXJrZG93biB2aWV3ZXIgd2lkZ2V0IHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQ3JlYXRlIHRoZSBkb2N1bWVudCByZWdpc3RyeSBvcHRpb25zLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZVJlZ2lzdHJ5T3B0aW9ucyhcbiAgICBvcHRpb25zOiBNYXJrZG93blZpZXdlckZhY3RvcnkuSU9wdGlvbnNcbiAgKTogRG9jdW1lbnRSZWdpc3RyeS5JV2lkZ2V0RmFjdG9yeU9wdGlvbnMge1xuICAgIHJldHVybiB7XG4gICAgICAuLi5vcHRpb25zLFxuICAgICAgcmVhZE9ubHk6IHRydWVcbiAgICB9IGFzIERvY3VtZW50UmVnaXN0cnkuSVdpZGdldEZhY3RvcnlPcHRpb25zO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBZQUxNIGZyb250IG1hdHRlciBmcm9tIHNvdXJjZS5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiByZW1vdmVGcm9udE1hdHRlcihzb3VyY2U6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgY29uc3QgcmUgPSAvXi0tLVxcblteXSo/XFxuKC0tLXwuLi4pXFxuLztcbiAgICBjb25zdCBtYXRjaCA9IHNvdXJjZS5tYXRjaChyZSk7XG4gICAgaWYgKCFtYXRjaCkge1xuICAgICAgcmV0dXJuIHNvdXJjZTtcbiAgICB9XG4gICAgY29uc3QgeyBsZW5ndGggfSA9IG1hdGNoWzBdO1xuICAgIHJldHVybiBzb3VyY2Uuc2xpY2UobGVuZ3RoKTtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==