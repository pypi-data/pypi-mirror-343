(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_htmlviewer-extension_lib_index_js-_82691"],{

/***/ "../packages/htmlviewer-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/htmlviewer-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/htmlviewer */ "webpack/sharing/consume/default/@jupyterlab/htmlviewer/@jupyterlab/htmlviewer");
/* harmony import */ var _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module htmlviewer-extension
 */





/**
 * Command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.trustHTML = 'htmlviewer:trust-html';
})(CommandIDs || (CommandIDs = {}));
/**
 * The HTML file handler extension.
 */
const htmlPlugin = {
    activate: activateHTMLViewer,
    id: '@jupyterlab/htmlviewer-extension:plugin',
    provides: _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__.IHTMLViewerTracker,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    autoStart: true
};
/**
 * Activate the HTMLViewer extension.
 */
function activateHTMLViewer(app, translator, palette, restorer) {
    // Add an HTML file type to the docregistry.
    const trans = translator.load('jupyterlab');
    const ft = {
        name: 'html',
        contentType: 'file',
        fileFormat: 'text',
        displayName: trans.__('HTML File'),
        extensions: ['.html'],
        mimeTypes: ['text/html'],
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.html5Icon
    };
    app.docRegistry.addFileType(ft);
    // Create a new viewer factory.
    const factory = new _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__.HTMLViewerFactory({
        name: trans.__('HTML Viewer'),
        fileTypes: ['html'],
        defaultFor: ['html'],
        readOnly: true
    });
    // Create a widget tracker for HTML documents.
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'htmlviewer'
    });
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: 'HTML Viewer' }),
            name: widget => widget.context.path
        });
    }
    app.docRegistry.addWidgetFactory(factory);
    factory.widgetCreated.connect((sender, widget) => {
        var _a, _b;
        // Track the widget.
        void tracker.add(widget);
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        // Notify the application when the trust state changes so it
        // can update any renderings of the trust command.
        widget.trustedChanged.connect(() => {
            app.commands.notifyCommandChanged(CommandIDs.trustHTML);
        });
        widget.title.icon = ft.icon;
        widget.title.iconClass = (_a = ft.iconClass) !== null && _a !== void 0 ? _a : '';
        widget.title.iconLabel = (_b = ft.iconLabel) !== null && _b !== void 0 ? _b : '';
    });
    // Add a command to trust the active HTML document,
    // allowing script executions in its context.
    app.commands.addCommand(CommandIDs.trustHTML, {
        label: trans.__('Trust HTML File'),
        isEnabled: () => !!tracker.currentWidget,
        isToggled: () => {
            const current = tracker.currentWidget;
            if (!current) {
                return false;
            }
            const sandbox = current.content.sandbox;
            return sandbox.indexOf('allow-scripts') !== -1;
        },
        execute: () => {
            const current = tracker.currentWidget;
            if (!current) {
                return false;
            }
            current.trusted = !current.trusted;
        }
    });
    if (palette) {
        palette.addItem({
            command: CommandIDs.trustHTML,
            category: trans.__('File Operations')
        });
    }
    return tracker;
}
/**
 * Export the plugins as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (htmlPlugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaHRtbHZpZXdlci1leHRlbnNpb24vc3JjL2luZGV4LnRzeCJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBOzs7K0VBRytFO0FBQy9FOzs7R0FHRztBQU04QjtBQUNxQztBQU10QztBQUNzQjtBQUNBO0FBRXREOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBRW5CO0FBRkQsV0FBVSxVQUFVO0lBQ0wsb0JBQVMsR0FBRyx1QkFBdUIsQ0FBQztBQUNuRCxDQUFDLEVBRlMsVUFBVSxLQUFWLFVBQVUsUUFFbkI7QUFFRDs7R0FFRztBQUNILE1BQU0sVUFBVSxHQUE4QztJQUM1RCxRQUFRLEVBQUUsa0JBQWtCO0lBQzVCLEVBQUUsRUFBRSx5Q0FBeUM7SUFDN0MsUUFBUSxFQUFFLHNFQUFrQjtJQUM1QixRQUFRLEVBQUUsQ0FBQyxnRUFBVyxDQUFDO0lBQ3ZCLFFBQVEsRUFBRSxDQUFDLGlFQUFlLEVBQUUsb0VBQWUsQ0FBQztJQUM1QyxTQUFTLEVBQUUsSUFBSTtDQUNoQixDQUFDO0FBRUY7O0dBRUc7QUFDSCxTQUFTLGtCQUFrQixDQUN6QixHQUFvQixFQUNwQixVQUF1QixFQUN2QixPQUErQixFQUMvQixRQUFnQztJQUVoQyw0Q0FBNEM7SUFDNUMsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUM1QyxNQUFNLEVBQUUsR0FBK0I7UUFDckMsSUFBSSxFQUFFLE1BQU07UUFDWixXQUFXLEVBQUUsTUFBTTtRQUNuQixVQUFVLEVBQUUsTUFBTTtRQUNsQixXQUFXLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxXQUFXLENBQUM7UUFDbEMsVUFBVSxFQUFFLENBQUMsT0FBTyxDQUFDO1FBQ3JCLFNBQVMsRUFBRSxDQUFDLFdBQVcsQ0FBQztRQUN4QixJQUFJLEVBQUUsZ0VBQVM7S0FDaEIs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SUFBSSxDQUFDLE9BQU8sRUFBRTtnQkFDWixPQUFPLEtBQUssQ0FBQzthQUNkO1lBQ0QsT0FBTyxDQUFDLE9BQU8sR0FBRyxDQUFDLE9BQU8sQ0FBQyxPQUFPLENBQUM7UUFDckMsQ0FBQztLQUNGLENBQUMsQ0FBQztJQUNILElBQUksT0FBTyxFQUFFO1FBQ1gsT0FBTyxDQUFDLE9BQU8sQ0FBQztZQUNkLE9BQU8sRUFBRSxVQUFVLENBQUMsU0FBUztZQUM3QixRQUFRLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxpQkFBaUIsQ0FBQztTQUN0QyxDQUFDLENBQUM7S0FDSjtJQUVELE9BQU8sT0FBTyxDQUFDO0FBQ2pCLENBQUM7QUFDRDs7R0FFRztBQUNILGlFQUFlLFVBQVUsRUFBQyIsImZpbGUiOiJwYWNrYWdlc19odG1sdmlld2VyLWV4dGVuc2lvbl9saWJfaW5kZXhfanMtXzgyNjkxLmU3ZDcxNDgxYmZjYTk1ZWU0YmIxLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBodG1sdmlld2VyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYXlvdXRSZXN0b3JlcixcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgSUNvbW1hbmRQYWxldHRlLCBXaWRnZXRUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgRG9jdW1lbnRSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIEhUTUxWaWV3ZXIsXG4gIEhUTUxWaWV3ZXJGYWN0b3J5LFxuICBJSFRNTFZpZXdlclRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvaHRtbHZpZXdlcic7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IGh0bWw1SWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuXG4vKipcbiAqIENvbW1hbmQgSURzIHVzZWQgYnkgdGhlIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgdHJ1c3RIVE1MID0gJ2h0bWx2aWV3ZXI6dHJ1c3QtaHRtbCc7XG59XG5cbi8qKlxuICogVGhlIEhUTUwgZmlsZSBoYW5kbGVyIGV4dGVuc2lvbi5cbiAqL1xuY29uc3QgaHRtbFBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElIVE1MVmlld2VyVHJhY2tlcj4gPSB7XG4gIGFjdGl2YXRlOiBhY3RpdmF0ZUhUTUxWaWV3ZXIsXG4gIGlkOiAnQGp1cHl0ZXJsYWIvaHRtbHZpZXdlci1leHRlbnNpb246cGx1Z2luJyxcbiAgcHJvdmlkZXM6IElIVE1MVmlld2VyVHJhY2tlcixcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUNvbW1hbmRQYWxldHRlLCBJTGF5b3V0UmVzdG9yZXJdLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogQWN0aXZhdGUgdGhlIEhUTUxWaWV3ZXIgZXh0ZW5zaW9uLlxuICovXG5mdW5jdGlvbiBhY3RpdmF0ZUhUTUxWaWV3ZXIoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGxcbik6IElIVE1MVmlld2VyVHJhY2tlciB7XG4gIC8vIEFkZCBhbiBIVE1MIGZpbGUgdHlwZSB0byB0aGUgZG9jcmVnaXN0cnkuXG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IGZ0OiBEb2N1bWVudFJlZ2lzdHJ5LklGaWxlVHlwZSA9IHtcbiAgICBuYW1lOiAnaHRtbCcsXG4gICAgY29udGVudFR5cGU6ICdmaWxlJyxcbiAgICBmaWxlRm9ybWF0OiAndGV4dCcsXG4gICAgZGlzcGxheU5hbWU6IHRyYW5zLl9fKCdIVE1MIEZpbGUnKSxcbiAgICBleHRlbnNpb25zOiBbJy5odG1sJ10sXG4gICAgbWltZVR5cGVzOiBbJ3RleHQvaHRtbCddLFxuICAgIGljb246IGh0bWw1SWNvblxuICB9O1xuICBhcHAuZG9jUmVnaXN0cnkuYWRkRmlsZVR5cGUoZnQpO1xuXG4gIC8vIENyZWF0ZSBhIG5ldyB2aWV3ZXIgZmFjdG9yeS5cbiAgY29uc3QgZmFjdG9yeSA9IG5ldyBIVE1MVmlld2VyRmFjdG9yeSh7XG4gICAgbmFtZTogdHJhbnMuX18oJ0hUTUwgVmlld2VyJyksXG4gICAgZmlsZVR5cGVzOiBbJ2h0bWwnXSxcbiAgICBkZWZhdWx0Rm9yOiBbJ2h0bWwnXSxcbiAgICByZWFkT25seTogdHJ1ZVxuICB9KTtcblxuICAvLyBDcmVhdGUgYSB3aWRnZXQgdHJhY2tlciBmb3IgSFRNTCBkb2N1bWVudHMuXG4gIGNvbnN0IHRyYWNrZXIgPSBuZXcgV2lkZ2V0VHJhY2tlcjxIVE1MVmlld2VyPih7XG4gICAgbmFtZXNwYWNlOiAnaHRtbHZpZXdlcidcbiAgfSk7XG5cbiAgLy8gSGFuZGxlIHN0YXRlIHJlc3RvcmF0aW9uLlxuICBpZiAocmVzdG9yZXIpIHtcbiAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwge1xuICAgICAgY29tbWFuZDogJ2RvY21hbmFnZXI6b3BlbicsXG4gICAgICBhcmdzOiB3aWRnZXQgPT4gKHsgcGF0aDogd2lkZ2V0LmNvbnRleHQucGF0aCwgZmFjdG9yeTogJ0hUTUwgVmlld2VyJyB9KSxcbiAgICAgIG5hbWU6IHdpZGdldCA9PiB3aWRnZXQuY29udGV4dC5wYXRoXG4gICAgfSk7XG4gIH1cblxuICBhcHAuZG9jUmVnaXN0cnkuYWRkV2lkZ2V0RmFjdG9yeShmYWN0b3J5KTtcbiAgZmFjdG9yeS53aWRnZXRDcmVhdGVkLmNvbm5lY3QoKHNlbmRlciwgd2lkZ2V0KSA9PiB7XG4gICAgLy8gVHJhY2sgdGhlIHdpZGdldC5cbiAgICB2b2lkIHRyYWNrZXIuYWRkKHdpZGdldCk7XG4gICAgLy8gTm90aWZ5IHRoZSB3aWRnZXQgdHJhY2tlciBpZiByZXN0b3JlIGRhdGEgbmVlZHMgdG8gdXBkYXRlLlxuICAgIHdpZGdldC5jb250ZXh0LnBhdGhDaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgdm9pZCB0cmFja2VyLnNhdmUod2lkZ2V0KTtcbiAgICB9KTtcbiAgICAvLyBOb3RpZnkgdGhlIGFwcGxpY2F0aW9uIHdoZW4gdGhlIHRydXN0IHN0YXRlIGNoYW5nZXMgc28gaXRcbiAgICAvLyBjYW4gdXBkYXRlIGFueSByZW5kZXJpbmdzIG9mIHRoZSB0cnVzdCBjb21tYW5kLlxuICAgIHdpZGdldC50cnVzdGVkQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZChDb21tYW5kSURzLnRydXN0SFRNTCk7XG4gICAgfSk7XG5cbiAgICB3aWRnZXQudGl0bGUuaWNvbiA9IGZ0Lmljb24hO1xuICAgIHdpZGdldC50aXRsZS5pY29uQ2xhc3MgPSBmdC5pY29uQ2xhc3MgPz8gJyc7XG4gICAgd2lkZ2V0LnRpdGxlLmljb25MYWJlbCA9IGZ0Lmljb25MYWJlbCA/PyAnJztcbiAgfSk7XG5cbiAgLy8gQWRkIGEgY29tbWFuZCB0byB0cnVzdCB0aGUgYWN0aXZlIEhUTUwgZG9jdW1lbnQsXG4gIC8vIGFsbG93aW5nIHNjcmlwdCBleGVjdXRpb25zIGluIGl0cyBjb250ZXh0LlxuICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRydXN0SFRNTCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnVHJ1c3QgSFRNTCBGaWxlJyksXG4gICAgaXNFbmFibGVkOiAoKSA9PiAhIXRyYWNrZXIuY3VycmVudFdpZGdldCxcbiAgICBpc1RvZ2dsZWQ6ICgpID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuICAgICAgY29uc3Qgc2FuZGJveCA9IGN1cnJlbnQuY29udGVudC5zYW5kYm94O1xuICAgICAgcmV0dXJuIHNhbmRib3guaW5kZXhPZignYWxsb3ctc2NyaXB0cycpICE9PSAtMTtcbiAgICB9LFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuICAgICAgY3VycmVudC50cnVzdGVkID0gIWN1cnJlbnQudHJ1c3RlZDtcbiAgICB9XG4gIH0pO1xuICBpZiAocGFsZXR0ZSkge1xuICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLnRydXN0SFRNTCxcbiAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnRmlsZSBPcGVyYXRpb25zJylcbiAgICB9KTtcbiAgfVxuXG4gIHJldHVybiB0cmFja2VyO1xufVxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbnMgYXMgZGVmYXVsdC5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgaHRtbFBsdWdpbjtcbiJdLCJzb3VyY2VSb290IjoiIn0=