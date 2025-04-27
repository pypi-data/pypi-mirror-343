(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_htmlviewer_lib_index_js-_fa501"],{

/***/ "../packages/htmlviewer/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/htmlviewer/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IHTMLViewerTracker": () => (/* binding */ IHTMLViewerTracker),
/* harmony export */   "HTMLViewer": () => (/* binding */ HTMLViewer),
/* harmony export */   "HTMLViewerFactory": () => (/* binding */ HTMLViewerFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_7__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module htmlviewer
 */








/**
 * The HTML viewer tracker token.
 */
const IHTMLViewerTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.Token('@jupyterlab/htmlviewer:IHTMLViewerTracker');
/**
 * The timeout to wait for change activity to have ceased before rendering.
 */
const RENDER_TIMEOUT = 1000;
/**
 * The CSS class to add to the HTMLViewer Widget.
 */
const CSS_CLASS = 'jp-HTMLViewer';
/**
 * A viewer widget for HTML documents.
 *
 * #### Notes
 * The iframed HTML document can pose a potential security risk,
 * since it can execute Javascript, and make same-origin requests
 * to the server, thereby executing arbitrary Javascript.
 *
 * Here, we sandbox the iframe so that it can't execute Javascript
 * or launch any popups. We allow one exception: 'allow-same-origin'
 * requests, so that local HTML documents can access CSS, images,
 * etc from the files system.
 */
class HTMLViewer extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.DocumentWidget {
    /**
     * Create a new widget for rendering HTML.
     */
    constructor(options) {
        super(Object.assign(Object.assign({}, options), { content: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IFrame({ sandbox: ['allow-same-origin'] }) }));
        this._renderPending = false;
        this._parser = new DOMParser();
        this._monitor = null;
        this._objectUrl = '';
        this._trustedChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_6__.Signal(this);
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        const trans = this.translator.load('jupyterlab');
        this.content.addClass(CSS_CLASS);
        void this.context.ready.then(() => {
            this.update();
            // Throttle the rendering rate of the widget.
            this._monitor = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.ActivityMonitor({
                signal: this.context.model.contentChanged,
                timeout: RENDER_TIMEOUT
            });
            this._monitor.activityStopped.connect(this.update, this);
        });
        // Make a refresh button for the toolbar.
        this.toolbar.addItem('refresh', new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.refreshIcon,
            onClick: async () => {
                if (!this.context.model.dirty) {
                    await this.context.revert();
                    this.update();
                }
            },
            tooltip: trans.__('Rerender HTML Document')
        }));
        // Make a trust button for the toolbar.
        this.toolbar.addItem('trust', _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_7__.createElement(Private.TrustButtonComponent, { htmlDocument: this, translator: this.translator })));
    }
    /**
     * Whether the HTML document is trusted. If trusted,
     * it can execute Javascript in the iframe sandbox.
     */
    get trusted() {
        return this.content.sandbox.indexOf('allow-scripts') !== -1;
    }
    set trusted(value) {
        if (this.trusted === value) {
            return;
        }
        if (value) {
            this.content.sandbox = Private.trusted;
        }
        else {
            this.content.sandbox = Private.untrusted;
        }
        // eslint-disable-next-line
        this.content.url = this.content.url; // Force a refresh.
        this._trustedChanged.emit(value);
    }
    /**
     * Emitted when the trust state of the document changes.
     */
    get trustedChanged() {
        return this._trustedChanged;
    }
    /**
     * Dispose of resources held by the html viewer.
     */
    dispose() {
        if (this._objectUrl) {
            try {
                URL.revokeObjectURL(this._objectUrl);
            }
            catch (error) {
                /* no-op */
            }
        }
        super.dispose();
    }
    /**
     * Handle and update request.
     */
    onUpdateRequest() {
        if (this._renderPending) {
            return;
        }
        this._renderPending = true;
        void this._renderModel().then(() => (this._renderPending = false));
    }
    /**
     * Render HTML in IFrame into this widget's node.
     */
    async _renderModel() {
        let data = this.context.model.toString();
        data = await this._setBase(data);
        // Set the new iframe url.
        const blob = new Blob([data], { type: 'text/html' });
        const oldUrl = this._objectUrl;
        this._objectUrl = URL.createObjectURL(blob);
        this.content.url = this._objectUrl;
        // Release reference to any previous object url.
        if (oldUrl) {
            try {
                URL.revokeObjectURL(oldUrl);
            }
            catch (error) {
                /* no-op */
            }
        }
        return;
    }
    /**
     * Set a <base> element in the HTML string so that the iframe
     * can correctly dereference relative links.
     */
    async _setBase(data) {
        const doc = this._parser.parseFromString(data, 'text/html');
        let base = doc.querySelector('base');
        if (!base) {
            base = doc.createElement('base');
            doc.head.insertBefore(base, doc.head.firstChild);
        }
        const path = this.context.path;
        const baseUrl = await this.context.urlResolver.getDownloadUrl(path);
        // Set the base href, plus a fake name for the url of this
        // document. The fake name doesn't really matter, as long
        // as the document can dereference relative links to resources
        // (e.g. CSS and scripts).
        base.href = baseUrl;
        base.target = '_self';
        return doc.documentElement.innerHTML;
    }
}
/**
 * A widget factory for HTMLViewers.
 */
class HTMLViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        return new HTMLViewer({ context });
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Sandbox exceptions for untrusted HTML.
     */
    Private.untrusted = [];
    /**
     * Sandbox exceptions for trusted HTML.
     */
    Private.trusted = ['allow-scripts'];
    /**
     * React component for a trusted button.
     *
     * This wraps the ToolbarButtonComponent and watches for trust changes.
     */
    function TrustButtonComponent(props) {
        const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        const trans = translator.load('jupyterlab');
        return (react__WEBPACK_IMPORTED_MODULE_7__.createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.UseSignal, { signal: props.htmlDocument.trustedChanged, initialSender: props.htmlDocument }, session => (react__WEBPACK_IMPORTED_MODULE_7__.createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButtonComponent, { className: "", onClick: () => (props.htmlDocument.trusted = !props.htmlDocument.trusted), tooltip: trans.__(`Whether the HTML file is trusted.
Trusting the file allows scripts to run in it,
which may result in security risks.
Only enable for files you trust.`), label: props.htmlDocument.trusted
                ? trans.__('Distrust HTML')
                : trans.__('Trust HTML') }))));
    }
    Private.TrustButtonComponent = TrustButtonComponent;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaHRtbHZpZXdlci9zcmMvaW5kZXgudHN4Il0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFTMkI7QUFDMEI7QUFNdkI7QUFDcUM7QUFDZDtBQUNkO0FBQ1U7QUFDckI7QUFPL0I7O0dBRUc7QUFDSSxNQUFNLGtCQUFrQixHQUFHLElBQUksb0RBQUssQ0FDekMsMkNBQTJDLENBQzVDLENBQUM7QUFDRjs7R0FFRztBQUNILE1BQU0sY0FBYyxHQUFHLElBQUksQ0FBQztBQUU1Qjs7R0FFRztBQUNILE1BQU0sU0FBUyxHQUFHLGVBQWUsQ0FBQztBQUVsQzs7Ozs7Ozs7Ozs7O0dBWUc7QUFDSSxNQUFNLFVBQ1gsU0FBUSxtRUFBc0I7SUFFOUI7O09BRUc7SUFDSCxZQUFZLE9BQStDO1FBQ3pELEtBQUssaUNBQ0EsT0FBTyxLQUNWLE9BQU8sRUFBRSxJQUFJLHdEQUFNLENBQUMsRUFBRSxPQUFPLEVBQUUsQ0FBQyxtQkFBbUIsQ0FBQyxFQUFFLENBQUMsSUFDdkQsQ0FBQztRQThJRyxtQkFBYyxHQUFHLEtBQUssQ0FBQztRQUN2QixZQUFPLEdBQUcsSUFBSSxTQUFTLEVBQUUsQ0FBQztRQUMxQixhQUFRLEdBR0wsSUFBSSxDQUFDO1FBQ1IsZUFBVSxHQUFXLEVBQUUsQ0FBQztRQUN4QixvQkFBZSxHQUFHLElBQUkscURBQU0sQ0FBZ0IsSUFBSSxDQUFDLENBQUM7UUFwSnhELElBQUksQ0FBQyxVQUFVLEdBQUcsT0FBTyxDQUFDLFVBQVUsSUFBSSxtRUFBYyxDQUFDO1FBQ3ZELE1BQU0sS0FBSyxHQUFHLElBQUksQ0FBQyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQ2pELElBQUksQ0FBQyxPQUFPLENBQUMsUUFBUSxDQUFDLFNBQVMsQ0FBQyxDQUFD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T0FBTyxDQUFDLEVBQUUsQ0FBQyxDQUNWLGlEQUFDLHdFQUFzQixJQUNyQixTQUFTLEVBQUMsRUFBRSxFQUNaLE9BQU8sRUFBRSxHQUFHLEVBQUUsQ0FDWixDQUFDLEtBQUssQ0FBQyxZQUFZLENBQUMsT0FBTyxHQUFHLENBQUMsS0FBSyxDQUFDLFlBQVksQ0FBQyxPQUFPLENBQUMsRUFFNUQsT0FBTyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUM7OztpQ0FHRyxDQUFDLEVBQ3RCLEtBQUssRUFDSCxLQUFLLENBQUMsWUFBWSxDQUFDLE9BQU87Z0JBQ3hCLENBQUMsQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUFDLGVBQWUsQ0FBQztnQkFDM0IsQ0FBQyxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsWUFBWSxDQUFDLEdBRTVCLENBQ0gsQ0FDUyxDQUNiLENBQUM7SUFDSixDQUFDO0lBM0JlLDRCQUFvQix1QkEyQm5DO0FBQ0gsQ0FBQyxFQTdEUyxPQUFPLEtBQVAsT0FBTyxRQTZEaEIiLCJmaWxlIjoicGFja2FnZXNfaHRtbHZpZXdlcl9saWJfaW5kZXhfanMtX2ZhNTAxLmViNWIyZWYxMDNhMmJiNjhkODNlLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBodG1sdmlld2VyXG4gKi9cblxuaW1wb3J0IHtcbiAgSUZyYW1lLFxuICBJV2lkZ2V0VHJhY2tlcixcbiAgUmVhY3RXaWRnZXQsXG4gIFRvb2xiYXJCdXR0b24sXG4gIFRvb2xiYXJCdXR0b25Db21wb25lbnQsXG4gIFVzZVNpZ25hbFxufSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBBY3Rpdml0eU1vbml0b3IgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHtcbiAgQUJDV2lkZ2V0RmFjdG9yeSxcbiAgRG9jdW1lbnRSZWdpc3RyeSxcbiAgRG9jdW1lbnRXaWRnZXQsXG4gIElEb2N1bWVudFdpZGdldFxufSBmcm9tICdAanVweXRlcmxhYi9kb2NyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyByZWZyZXNoSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbi8qKlxuICogQSBjbGFzcyB0aGF0IHRyYWNrcyBIVE1MIHZpZXdlciB3aWRnZXRzLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElIVE1MVmlld2VyVHJhY2tlciBleHRlbmRzIElXaWRnZXRUcmFja2VyPEhUTUxWaWV3ZXI+IHt9XG5cbi8qKlxuICogVGhlIEhUTUwgdmlld2VyIHRyYWNrZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJSFRNTFZpZXdlclRyYWNrZXIgPSBuZXcgVG9rZW48SUhUTUxWaWV3ZXJUcmFja2VyPihcbiAgJ0BqdXB5dGVybGFiL2h0bWx2aWV3ZXI6SUhUTUxWaWV3ZXJUcmFja2VyJ1xuKTtcbi8qKlxuICogVGhlIHRpbWVvdXQgdG8gd2FpdCBmb3IgY2hhbmdlIGFjdGl2aXR5IHRvIGhhdmUgY2Vhc2VkIGJlZm9yZSByZW5kZXJpbmcuXG4gKi9cbmNvbnN0IFJFTkRFUl9USU1FT1VUID0gMTAwMDtcblxuLyoqXG4gKiBUaGUgQ1NTIGNsYXNzIHRvIGFkZCB0byB0aGUgSFRNTFZpZXdlciBXaWRnZXQuXG4gKi9cbmNvbnN0IENTU19DTEFTUyA9ICdqcC1IVE1MVmlld2VyJztcblxuLyoqXG4gKiBBIHZpZXdlciB3aWRnZXQgZm9yIEhUTUwgZG9jdW1lbnRzLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIFRoZSBpZnJhbWVkIEhUTUwgZG9jdW1lbnQgY2FuIHBvc2UgYSBwb3RlbnRpYWwgc2VjdXJpdHkgcmlzayxcbiAqIHNpbmNlIGl0IGNhbiBleGVjdXRlIEphdmFzY3JpcHQsIGFuZCBtYWtlIHNhbWUtb3JpZ2luIHJlcXVlc3RzXG4gKiB0byB0aGUgc2VydmVyLCB0aGVyZWJ5IGV4ZWN1dGluZyBhcmJpdHJhcnkgSmF2YXNjcmlwdC5cbiAqXG4gKiBIZXJlLCB3ZSBzYW5kYm94IHRoZSBpZnJhbWUgc28gdGhhdCBpdCBjYW4ndCBleGVjdXRlIEphdmFzY3JpcHRcbiAqIG9yIGxhdW5jaCBhbnkgcG9wdXBzLiBXZSBhbGxvdyBvbmUgZXhjZXB0aW9uOiAnYWxsb3ctc2FtZS1vcmlnaW4nXG4gKiByZXF1ZXN0cywgc28gdGhhdCBsb2NhbCBIVE1MIGRvY3VtZW50cyBjYW4gYWNjZXNzIENTUywgaW1hZ2VzLFxuICogZXRjIGZyb20gdGhlIGZpbGVzIHN5c3RlbS5cbiAqL1xuZXhwb3J0IGNsYXNzIEhUTUxWaWV3ZXJcbiAgZXh0ZW5kcyBEb2N1bWVudFdpZGdldDxJRnJhbWU+XG4gIGltcGxlbWVudHMgSURvY3VtZW50V2lkZ2V0PElGcmFtZT4ge1xuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHdpZGdldCBmb3IgcmVuZGVyaW5nIEhUTUwuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBEb2N1bWVudFdpZGdldC5JT3B0aW9uc09wdGlvbmFsQ29udGVudCkge1xuICAgIHN1cGVyKHtcbiAgICAgIC4uLm9wdGlvbnMsXG4gICAgICBjb250ZW50OiBuZXcgSUZyYW1lKHsgc2FuZGJveDogWydhbGxvdy1zYW1lLW9yaWdpbiddIH0pXG4gICAgfSk7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gb3B0aW9ucy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIGNvbnN0IHRyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICB0aGlzLmNvbnRlbnQuYWRkQ2xhc3MoQ1NTX0NMQVNTKTtcblxuICAgIHZvaWQgdGhpcy5jb250ZXh0LnJlYWR5LnRoZW4oKCkgPT4ge1xuICAgICAgdGhpcy51cGRhdGUoKTtcbiAgICAgIC8vIFRocm90dGxlIHRoZSByZW5kZXJpbmcgcmF0ZSBvZiB0aGUgd2lkZ2V0LlxuICAgICAgdGhpcy5fbW9uaXRvciA9IG5ldyBBY3Rpdml0eU1vbml0b3Ioe1xuICAgICAgICBzaWduYWw6IHRoaXMuY29udGV4dC5tb2RlbC5jb250ZW50Q2hhbmdlZCxcbiAgICAgICAgdGltZW91dDogUkVOREVSX1RJTUVPVVRcbiAgICAgIH0pO1xuICAgICAgdGhpcy5fbW9uaXRvci5hY3Rpdml0eVN0b3BwZWQuY29ubmVjdCh0aGlzLnVwZGF0ZSwgdGhpcyk7XG4gICAgfSk7XG5cbiAgICAvLyBNYWtlIGEgcmVmcmVzaCBidXR0b24gZm9yIHRoZSB0b29sYmFyLlxuICAgIHRoaXMudG9vbGJhci5hZGRJdGVtKFxuICAgICAgJ3JlZnJlc2gnLFxuICAgICAgbmV3IFRvb2xiYXJCdXR0b24oe1xuICAgICAgICBpY29uOiByZWZyZXNoSWNvbixcbiAgICAgICAgb25DbGljazogYXN5bmMgKCkgPT4ge1xuICAgICAgICAgIGlmICghdGhpcy5jb250ZXh0Lm1vZGVsLmRpcnR5KSB7XG4gICAgICAgICAgICBhd2FpdCB0aGlzLmNvbnRleHQucmV2ZXJ0KCk7XG4gICAgICAgICAgICB0aGlzLnVwZGF0ZSgpO1xuICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgdG9vbHRpcDogdHJhbnMuX18oJ1JlcmVuZGVyIEhUTUwgRG9jdW1lbnQnKVxuICAgICAgfSlcbiAgICApO1xuICAgIC8vIE1ha2UgYSB0cnVzdCBidXR0b24gZm9yIHRoZSB0b29sYmFyLlxuICAgIHRoaXMudG9vbGJhci5hZGRJdGVtKFxuICAgICAgJ3RydXN0JyxcbiAgICAgIFJlYWN0V2lkZ2V0LmNyZWF0ZShcbiAgICAgICAgPFByaXZhdGUuVHJ1c3RCdXR0b25Db21wb25lbnRcbiAgICAgICAgICBodG1sRG9jdW1lbnQ9e3RoaXN9XG4gICAgICAgICAgdHJhbnNsYXRvcj17dGhpcy50cmFuc2xhdG9yfVxuICAgICAgICAvPlxuICAgICAgKVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgSFRNTCBkb2N1bWVudCBpcyB0cnVzdGVkLiBJZiB0cnVzdGVkLFxuICAgKiBpdCBjYW4gZXhlY3V0ZSBKYXZhc2NyaXB0IGluIHRoZSBpZnJhbWUgc2FuZGJveC5cbiAgICovXG4gIGdldCB0cnVzdGVkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLmNvbnRlbnQuc2FuZGJveC5pbmRleE9mKCdhbGxvdy1zY3JpcHRzJykgIT09IC0xO1xuICB9XG4gIHNldCB0cnVzdGVkKHZhbHVlOiBib29sZWFuKSB7XG4gICAgaWYgKHRoaXMudHJ1c3RlZCA9PT0gdmFsdWUpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgaWYgKHZhbHVlKSB7XG4gICAgICB0aGlzLmNvbnRlbnQuc2FuZGJveCA9IFByaXZhdGUudHJ1c3RlZDtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5jb250ZW50LnNhbmRib3ggPSBQcml2YXRlLnVudHJ1c3RlZDtcbiAgICB9XG4gICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lXG4gICAgdGhpcy5jb250ZW50LnVybCA9IHRoaXMuY29udGVudC51cmw7IC8vIEZvcmNlIGEgcmVmcmVzaC5cbiAgICB0aGlzLl90cnVzdGVkQ2hhbmdlZC5lbWl0KHZhbHVlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBFbWl0dGVkIHdoZW4gdGhlIHRydXN0IHN0YXRlIG9mIHRoZSBkb2N1bWVudCBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IHRydXN0ZWRDaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgYm9vbGVhbj4ge1xuICAgIHJldHVybiB0aGlzLl90cnVzdGVkQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBodG1sIHZpZXdlci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX29iamVjdFVybCkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgVVJMLnJldm9rZU9iamVjdFVSTCh0aGlzLl9vYmplY3RVcmwpO1xuICAgICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgICAgLyogbm8tb3AgKi9cbiAgICAgIH1cbiAgICB9XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhbmQgdXBkYXRlIHJlcXVlc3QuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25VcGRhdGVSZXF1ZXN0KCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9yZW5kZXJQZW5kaW5nKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX3JlbmRlclBlbmRpbmcgPSB0cnVlO1xuICAgIHZvaWQgdGhpcy5fcmVuZGVyTW9kZWwoKS50aGVuKCgpID0+ICh0aGlzLl9yZW5kZXJQZW5kaW5nID0gZmFsc2UpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgSFRNTCBpbiBJRnJhbWUgaW50byB0aGlzIHdpZGdldCdzIG5vZGUuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9yZW5kZXJNb2RlbCgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBsZXQgZGF0YSA9IHRoaXMuY29udGV4dC5tb2RlbC50b1N0cmluZygpO1xuICAgIGRhdGEgPSBhd2FpdCB0aGlzLl9zZXRCYXNlKGRhdGEpO1xuXG4gICAgLy8gU2V0IHRoZSBuZXcgaWZyYW1lIHVybC5cbiAgICBjb25zdCBibG9iID0gbmV3IEJsb2IoW2RhdGFdLCB7IHR5cGU6ICd0ZXh0L2h0bWwnIH0pO1xuICAgIGNvbnN0IG9sZFVybCA9IHRoaXMuX29iamVjdFVybDtcbiAgICB0aGlzLl9vYmplY3RVcmwgPSBVUkwuY3JlYXRlT2JqZWN0VVJMKGJsb2IpO1xuICAgIHRoaXMuY29udGVudC51cmwgPSB0aGlzLl9vYmplY3RVcmw7XG5cbiAgICAvLyBSZWxlYXNlIHJlZmVyZW5jZSB0byBhbnkgcHJldmlvdXMgb2JqZWN0IHVybC5cbiAgICBpZiAob2xkVXJsKSB7XG4gICAgICB0cnkge1xuICAgICAgICBVUkwucmV2b2tlT2JqZWN0VVJMKG9sZFVybCk7XG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICAvKiBuby1vcCAqL1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm47XG4gIH1cblxuICAvKipcbiAgICogU2V0IGEgPGJhc2U+IGVsZW1lbnQgaW4gdGhlIEhUTUwgc3RyaW5nIHNvIHRoYXQgdGhlIGlmcmFtZVxuICAgKiBjYW4gY29ycmVjdGx5IGRlcmVmZXJlbmNlIHJlbGF0aXZlIGxpbmtzLlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfc2V0QmFzZShkYXRhOiBzdHJpbmcpOiBQcm9taXNlPHN0cmluZz4ge1xuICAgIGNvbnN0IGRvYyA9IHRoaXMuX3BhcnNlci5wYXJzZUZyb21TdHJpbmcoZGF0YSwgJ3RleHQvaHRtbCcpO1xuICAgIGxldCBiYXNlID0gZG9jLnF1ZXJ5U2VsZWN0b3IoJ2Jhc2UnKTtcbiAgICBpZiAoIWJhc2UpIHtcbiAgICAgIGJhc2UgPSBkb2MuY3JlYXRlRWxlbWVudCgnYmFzZScpO1xuICAgICAgZG9jLmhlYWQuaW5zZXJ0QmVmb3JlKGJhc2UsIGRvYy5oZWFkLmZpcnN0Q2hpbGQpO1xuICAgIH1cbiAgICBjb25zdCBwYXRoID0gdGhpcy5jb250ZXh0LnBhdGg7XG4gICAgY29uc3QgYmFzZVVybCA9IGF3YWl0IHRoaXMuY29udGV4dC51cmxSZXNvbHZlci5nZXREb3dubG9hZFVybChwYXRoKTtcblxuICAgIC8vIFNldCB0aGUgYmFzZSBocmVmLCBwbHVzIGEgZmFrZSBuYW1lIGZvciB0aGUgdXJsIG9mIHRoaXNcbiAgICAvLyBkb2N1bWVudC4gVGhlIGZha2UgbmFtZSBkb2Vzbid0IHJlYWxseSBtYXR0ZXIsIGFzIGxvbmdcbiAgICAvLyBhcyB0aGUgZG9jdW1lbnQgY2FuIGRlcmVmZXJlbmNlIHJlbGF0aXZlIGxpbmtzIHRvIHJlc291cmNlc1xuICAgIC8vIChlLmcuIENTUyBhbmQgc2NyaXB0cykuXG4gICAgYmFzZS5ocmVmID0gYmFzZVVybDtcbiAgICBiYXNlLnRhcmdldCA9ICdfc2VsZic7XG4gICAgcmV0dXJuIGRvYy5kb2N1bWVudEVsZW1lbnQuaW5uZXJIVE1MO1xuICB9XG5cbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF9yZW5kZXJQZW5kaW5nID0gZmFsc2U7XG4gIHByaXZhdGUgX3BhcnNlciA9IG5ldyBET01QYXJzZXIoKTtcbiAgcHJpdmF0ZSBfbW9uaXRvcjogQWN0aXZpdHlNb25pdG9yPFxuICAgIERvY3VtZW50UmVnaXN0cnkuSU1vZGVsLFxuICAgIHZvaWRcbiAgPiB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9vYmplY3RVcmw6IHN0cmluZyA9ICcnO1xuICBwcml2YXRlIF90cnVzdGVkQ2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgYm9vbGVhbj4odGhpcyk7XG59XG5cbi8qKlxuICogQSB3aWRnZXQgZmFjdG9yeSBmb3IgSFRNTFZpZXdlcnMuXG4gKi9cbmV4cG9ydCBjbGFzcyBIVE1MVmlld2VyRmFjdG9yeSBleHRlbmRzIEFCQ1dpZGdldEZhY3Rvcnk8SFRNTFZpZXdlcj4ge1xuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHdpZGdldCBnaXZlbiBhIGNvbnRleHQuXG4gICAqL1xuICBwcm90ZWN0ZWQgY3JlYXRlTmV3V2lkZ2V0KGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dCk6IEhUTUxWaWV3ZXIge1xuICAgIHJldHVybiBuZXcgSFRNTFZpZXdlcih7IGNvbnRleHQgfSk7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBTYW5kYm94IGV4Y2VwdGlvbnMgZm9yIHVudHJ1c3RlZCBIVE1MLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IHVudHJ1c3RlZDogSUZyYW1lLlNhbmRib3hFeGNlcHRpb25zW10gPSBbXTtcblxuICAvKipcbiAgICogU2FuZGJveCBleGNlcHRpb25zIGZvciB0cnVzdGVkIEhUTUwuXG4gICAqL1xuICBleHBvcnQgY29uc3QgdHJ1c3RlZDogSUZyYW1lLlNhbmRib3hFeGNlcHRpb25zW10gPSBbJ2FsbG93LXNjcmlwdHMnXTtcblxuICAvKipcbiAgICogTmFtZXNwYWNlIGZvciBUcnVzdGVkQnV0dG9uLlxuICAgKi9cbiAgZXhwb3J0IG5hbWVzcGFjZSBUcnVzdEJ1dHRvbkNvbXBvbmVudCB7XG4gICAgLyoqXG4gICAgICogSW50ZXJmYWNlIGZvciBUcnVzdGVkQnV0dG9uIHByb3BzLlxuICAgICAqL1xuICAgIGV4cG9ydCBpbnRlcmZhY2UgSVByb3BzIHtcbiAgICAgIGh0bWxEb2N1bWVudDogSFRNTFZpZXdlcjtcblxuICAgICAgLyoqXG4gICAgICAgKiBMYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAgICovXG4gICAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFJlYWN0IGNvbXBvbmVudCBmb3IgYSB0cnVzdGVkIGJ1dHRvbi5cbiAgICpcbiAgICogVGhpcyB3cmFwcyB0aGUgVG9vbGJhckJ1dHRvbkNvbXBvbmVudCBhbmQgd2F0Y2hlcyBmb3IgdHJ1c3QgY2hhbmdlcy5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBUcnVzdEJ1dHRvbkNvbXBvbmVudChwcm9wczogVHJ1c3RCdXR0b25Db21wb25lbnQuSVByb3BzKSB7XG4gICAgY29uc3QgdHJhbnNsYXRvciA9IHByb3BzLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICByZXR1cm4gKFxuICAgICAgPFVzZVNpZ25hbFxuICAgICAgICBzaWduYWw9e3Byb3BzLmh0bWxEb2N1bWVudC50cnVzdGVkQ2hhbmdlZH1cbiAgICAgICAgaW5pdGlhbFNlbmRlcj17cHJvcHMuaHRtbERvY3VtZW50fVxuICAgICAgPlxuICAgICAgICB7c2Vzc2lvbiA9PiAoXG4gICAgICAgICAgPFRvb2xiYXJCdXR0b25Db21wb25lbnRcbiAgICAgICAgICAgIGNsYXNzTmFtZT1cIlwiXG4gICAgICAgICAgICBvbkNsaWNrPXsoKSA9PlxuICAgICAgICAgICAgICAocHJvcHMuaHRtbERvY3VtZW50LnRydXN0ZWQgPSAhcHJvcHMuaHRtbERvY3VtZW50LnRydXN0ZWQpXG4gICAgICAgICAgICB9XG4gICAgICAgICAgICB0b29sdGlwPXt0cmFucy5fXyhgV2hldGhlciB0aGUgSFRNTCBmaWxlIGlzIHRydXN0ZWQuXG5UcnVzdGluZyB0aGUgZmlsZSBhbGxvd3Mgc2NyaXB0cyB0byBydW4gaW4gaXQsXG53aGljaCBtYXkgcmVzdWx0IGluIHNlY3VyaXR5IHJpc2tzLlxuT25seSBlbmFibGUgZm9yIGZpbGVzIHlvdSB0cnVzdC5gKX1cbiAgICAgICAgICAgIGxhYmVsPXtcbiAgICAgICAgICAgICAgcHJvcHMuaHRtbERvY3VtZW50LnRydXN0ZWRcbiAgICAgICAgICAgICAgICA/IHRyYW5zLl9fKCdEaXN0cnVzdCBIVE1MJylcbiAgICAgICAgICAgICAgICA6IHRyYW5zLl9fKCdUcnVzdCBIVE1MJylcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAvPlxuICAgICAgICApfVxuICAgICAgPC9Vc2VTaWduYWw+XG4gICAgKTtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==