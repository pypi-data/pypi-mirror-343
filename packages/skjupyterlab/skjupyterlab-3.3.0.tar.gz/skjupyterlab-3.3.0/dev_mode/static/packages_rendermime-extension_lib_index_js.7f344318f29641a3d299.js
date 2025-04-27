(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_rendermime-extension_lib_index_js"],{

/***/ "../packages/rendermime-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/rendermime-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module rendermime-extension
 */




var CommandIDs;
(function (CommandIDs) {
    CommandIDs.handleLink = 'rendermime:handle-local-link';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin providing a rendermime registry.
 */
const plugin = {
    id: '@jupyterlab/rendermime-extension:plugin',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.ILatexTypesetter, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ISanitizer],
    provides: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.IRenderMimeRegistry,
    activate: activate,
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the rendermine plugin.
 */
function activate(app, translator, docManager, latexTypesetter, sanitizer) {
    const trans = translator.load('jupyterlab');
    if (docManager) {
        app.commands.addCommand(CommandIDs.handleLink, {
            label: trans.__('Handle Local Link'),
            execute: args => {
                const path = args['path'];
                const id = args['id'];
                if (!path) {
                    return;
                }
                // First check if the path exists on the server.
                return docManager.services.contents
                    .get(path, { content: false })
                    .then(() => {
                    // Open the link with the default rendered widget factory,
                    // if applicable.
                    const factory = docManager.registry.defaultRenderedWidgetFactory(path);
                    const widget = docManager.openOrReveal(path, factory.name);
                    // Handle the hash if one has been provided.
                    if (widget && id) {
                        widget.setFragment(id);
                    }
                });
            }
        });
    }
    return new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.RenderMimeRegistry({
        initialFactories: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.standardRendererFactories,
        linkHandler: !docManager
            ? undefined
            : {
                handleLink: (node, path, id) => {
                    // If node has the download attribute explicitly set, use the
                    // default browser downloading behavior.
                    if (node.tagName === 'A' && node.hasAttribute('download')) {
                        return;
                    }
                    app.commandLinker.connectNode(node, CommandIDs.handleLink, {
                        path,
                        id
                    });
                }
            },
        latexTypesetter: latexTypesetter !== null && latexTypesetter !== void 0 ? latexTypesetter : undefined,
        translator: translator,
        sanitizer: sanitizer !== null && sanitizer !== void 0 ? sanitizer : undefined
    });
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcmVuZGVybWltZS1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBOzs7K0VBRytFO0FBQy9FOzs7R0FHRztBQU0rQztBQUNRO0FBTTFCO0FBQ3NCO0FBRXRELElBQVUsVUFBVSxDQUVuQjtBQUZELFdBQVUsVUFBVTtJQUNMLHFCQUFVLEdBQUcsOEJBQThCLENBQUM7QUFDM0QsQ0FBQyxFQUZTLFVBQVUsS0FBVixVQUFVLFFBRW5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBK0M7SUFDekQsRUFBRSxFQUFFLHlDQUF5QztJQUM3QyxRQUFRLEVBQUUsQ0FBQyxnRUFBVyxDQUFDO0lBQ3ZCLFFBQVEsRUFBRSxDQUFDLG9FQUFnQixFQUFFLG9FQUFnQixFQUFFLDREQUFVLENBQUM7SUFDMUQsUUFBUSxFQUFFLHVFQUFtQjtJQUM3QixRQUFRLEVBQUUsUUFBUTtJQUNsQixTQUFTLEVBQUUsSUFBSTtDQUNoQixDQUFDO0FBRUY7O0dBRUc7QUFDSCxpRUFBZSxNQUFNLEVBQUM7QUFFdEI7O0dBRUc7QUFDSCxTQUFTLFFBQVEsQ0FDZixHQUFvQixFQUNwQixVQUF1QixFQUN2QixVQUFtQyxFQUNuQyxlQUF3QyxFQUN4QyxTQUE0QjtJQUU1QixNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO0lBQzVDLElBQUksVUFBVSxFQUFFO1FBQ2QsR0FBRyxDQUFDLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLFVBQVUsRUFBRTtZQUM3QyxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxtQkFBbUIsQ0FBQztZQUNwQyxPQUFPLEVBQUUsSUFBSSxDQUFDLEVBQUU7Z0JBQ2QsTUFBTSxJQUFJLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBOEIsQ0FBQztnQkFDdkQsTUFBTSxFQUFFLEdBQUcsSUFBSSxDQUFDLElBQUksQ0FBOEIsQ0FBQztnQkFDbkQsSUFBSSxDQUFDLElBQUksRUFBRTtvQkFDVCxPQUFPO2lCQUNSO2dCQUNELGdEQUFnRDtnQkFDaEQsT0FBTyxVQUFVLENBQUMsUUFBUSxDQUFDLFFBQVE7cUJBQ2hDLEdBQUcsQ0FBQyxJQUFJLEVBQUUsRUFBRSxPQUFPLEVBQUUsS0FBSyxFQUFFLENBQUM7cUJBQzdCLElBQUksQ0FBQyxHQUFHLEVBQUU7b0JBQ1QsMERBQTBEO29CQUMxRCxpQkFBaUI7b0JBQ2pCLE1BQU0sT0FBTyxHQUFHLFVBQVUsQ0FBQyxRQUFRLENBQUMsNEJBQTRCLENBQzlELElBQUksQ0FDTCxDQUFDO29CQUNGLE1BQU0sTUFBTSxHQUFHLFVBQVUsQ0FBQyxZQUFZLENBQUMsSUFBSSxFQUFFLE9BQU8sQ0FBQyxJQUFJLENBQUMsQ0FBQztvQkFFM0QsNENBQTRDO29CQUM1QyxJQUFJLE1BQU0sSUFBSSxFQUFFLEVBQUU7d0JBQ2hCLE1BQU0sQ0FBQyxXQUFXLENBQUMsRUFBRSxDQUFDLENBQUM7cUJBQ3hCO2dCQUNILENBQUMsQ0FBQyxDQUFDO1lBQ1AsQ0FBQztTQUNGLENBQUMsQ0FBQztLQUNKO0lBQ0QsT0FBTyxJQUFJLHNFQUFrQixDQUFDO1FBQzVCLGdCQUFnQixFQUFFLDZFQUF5QjtRQUMzQyxXQUFXLEVBQUUsQ0FBQyxVQUFVO1lBQ3RCLENBQUMsQ0FBQyxTQUFTO1lBQ1gsQ0FBQyxDQUFDO2dCQUNFLFVBQVUsRUFBRSxDQUFDLElBQWlCLEVBQUUsSUFBWSxFQUFFLEVBQVcsRUFBRSxFQUFFO29CQUMzRCw2REFBNkQ7b0JBQzdELHdDQUF3QztvQkFDeEMsSUFBSSxJQUFJLENBQUMsT0FBTyxLQUFLLEdBQUcsSUFBSSxJQUFJLENBQUMsWUFBWSxDQUFDLFVBQVUsQ0FBQyxFQUFFO3dCQUN6RCxPQUFPO3FCQUNSO29CQUNELEdBQUcsQ0FBQyxhQUFhLENBQUMsV0FBVyxDQUFDLElBQUksRUFBRSxVQUFVLENBQUMsVUFBVSxFQUFFO3dCQUN6RCxJQUFJO3dCQUNKLEVBQUU7cUJBQ0gsQ0FBQyxDQUFDO2dCQUNMLENBQUM7YUFDRjtRQUNMLGVBQWUsRUFBRSxlQUFlLGFBQWYsZUFBZSxjQUFmLGVBQWUsR0FBSSxTQUFTO1FBQzdDLFVBQVUsRUFBRSxVQUFVO1FBQ3RCLFNBQVMsRUFBRSxTQUFTLGFBQVQsU0FBUyxjQUFULFNBQVMsR0FBSSxTQUFTO0tBQ2xDLENBQUMsQ0FBQztBQUNMLENBQUMiLCJmaWxlIjoicGFja2FnZXNfcmVuZGVybWltZS1leHRlbnNpb25fbGliX2luZGV4X2pzLjdmMzQ0MzE4ZjI5NjQxYTNkMjk5LmpzIiwic291cmNlc0NvbnRlbnQiOlsiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSByZW5kZXJtaW1lLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IElTYW5pdGl6ZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJRG9jdW1lbnRNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlcic7XG5pbXBvcnQge1xuICBJTGF0ZXhUeXBlc2V0dGVyLFxuICBJUmVuZGVyTWltZVJlZ2lzdHJ5LFxuICBSZW5kZXJNaW1lUmVnaXN0cnksXG4gIHN0YW5kYXJkUmVuZGVyZXJGYWN0b3JpZXNcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcblxubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgaGFuZGxlTGluayA9ICdyZW5kZXJtaW1lOmhhbmRsZS1sb2NhbC1saW5rJztcbn1cblxuLyoqXG4gKiBBIHBsdWdpbiBwcm92aWRpbmcgYSByZW5kZXJtaW1lIHJlZ2lzdHJ5LlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJUmVuZGVyTWltZVJlZ2lzdHJ5PiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9yZW5kZXJtaW1lLWV4dGVuc2lvbjpwbHVnaW4nLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJRG9jdW1lbnRNYW5hZ2VyLCBJTGF0ZXhUeXBlc2V0dGVyLCBJU2FuaXRpemVyXSxcbiAgcHJvdmlkZXM6IElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIGFjdGl2YXRlOiBhY3RpdmF0ZSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2luIGFzIGRlZmF1bHQuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcblxuLyoqXG4gKiBBY3RpdmF0ZSB0aGUgcmVuZGVybWluZSBwbHVnaW4uXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIGRvY01hbmFnZXI6IElEb2N1bWVudE1hbmFnZXIgfCBudWxsLFxuICBsYXRleFR5cGVzZXR0ZXI6IElMYXRleFR5cGVzZXR0ZXIgfCBudWxsLFxuICBzYW5pdGl6ZXI6IElTYW5pdGl6ZXIgfCBudWxsXG4pOiBSZW5kZXJNaW1lUmVnaXN0cnkge1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBpZiAoZG9jTWFuYWdlcikge1xuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaGFuZGxlTGluaywge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdIYW5kbGUgTG9jYWwgTGluaycpLFxuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IHBhdGggPSBhcmdzWydwYXRoJ10gYXMgc3RyaW5nIHwgdW5kZWZpbmVkIHwgbnVsbDtcbiAgICAgICAgY29uc3QgaWQgPSBhcmdzWydpZCddIGFzIHN0cmluZyB8IHVuZGVmaW5lZCB8IG51bGw7XG4gICAgICAgIGlmICghcGF0aCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICAvLyBGaXJzdCBjaGVjayBpZiB0aGUgcGF0aCBleGlzdHMgb24gdGhlIHNlcnZlci5cbiAgICAgICAgcmV0dXJuIGRvY01hbmFnZXIuc2VydmljZXMuY29udGVudHNcbiAgICAgICAgICAuZ2V0KHBhdGgsIHsgY29udGVudDogZmFsc2UgfSlcbiAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAvLyBPcGVuIHRoZSBsaW5rIHdpdGggdGhlIGRlZmF1bHQgcmVuZGVyZWQgd2lkZ2V0IGZhY3RvcnksXG4gICAgICAgICAgICAvLyBpZiBhcHBsaWNhYmxlLlxuICAgICAgICAgICAgY29uc3QgZmFjdG9yeSA9IGRvY01hbmFnZXIucmVnaXN0cnkuZGVmYXVsdFJlbmRlcmVkV2lkZ2V0RmFjdG9yeShcbiAgICAgICAgICAgICAgcGF0aFxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIGNvbnN0IHdpZGdldCA9IGRvY01hbmFnZXIub3Blbk9yUmV2ZWFsKHBhdGgsIGZhY3RvcnkubmFtZSk7XG5cbiAgICAgICAgICAgIC8vIEhhbmRsZSB0aGUgaGFzaCBpZiBvbmUgaGFzIGJlZW4gcHJvdmlkZWQuXG4gICAgICAgICAgICBpZiAod2lkZ2V0ICYmIGlkKSB7XG4gICAgICAgICAgICAgIHdpZGdldC5zZXRGcmFnbWVudChpZCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cbiAgcmV0dXJuIG5ldyBSZW5kZXJNaW1lUmVnaXN0cnkoe1xuICAgIGluaXRpYWxGYWN0b3JpZXM6IHN0YW5kYXJkUmVuZGVyZXJGYWN0b3JpZXMsXG4gICAgbGlua0hhbmRsZXI6ICFkb2NNYW5hZ2VyXG4gICAgICA/IHVuZGVmaW5lZFxuICAgICAgOiB7XG4gICAgICAgICAgaGFuZGxlTGluazogKG5vZGU6IEhUTUxFbGVtZW50LCBwYXRoOiBzdHJpbmcsIGlkPzogc3RyaW5nKSA9PiB7XG4gICAgICAgICAgICAvLyBJZiBub2RlIGhhcyB0aGUgZG93bmxvYWQgYXR0cmlidXRlIGV4cGxpY2l0bHkgc2V0LCB1c2UgdGhlXG4gICAgICAgICAgICAvLyBkZWZhdWx0IGJyb3dzZXIgZG93bmxvYWRpbmcgYmVoYXZpb3IuXG4gICAgICAgICAgICBpZiAobm9kZS50YWdOYW1lID09PSAnQScgJiYgbm9kZS5oYXNBdHRyaWJ1dGUoJ2Rvd25sb2FkJykpIHtcbiAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgYXBwLmNvbW1hbmRMaW5rZXIuY29ubmVjdE5vZGUobm9kZSwgQ29tbWFuZElEcy5oYW5kbGVMaW5rLCB7XG4gICAgICAgICAgICAgIHBhdGgsXG4gICAgICAgICAgICAgIGlkXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgbGF0ZXhUeXBlc2V0dGVyOiBsYXRleFR5cGVzZXR0ZXIgPz8gdW5kZWZpbmVkLFxuICAgIHRyYW5zbGF0b3I6IHRyYW5zbGF0b3IsXG4gICAgc2FuaXRpemVyOiBzYW5pdGl6ZXIgPz8gdW5kZWZpbmVkXG4gIH0pO1xufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==