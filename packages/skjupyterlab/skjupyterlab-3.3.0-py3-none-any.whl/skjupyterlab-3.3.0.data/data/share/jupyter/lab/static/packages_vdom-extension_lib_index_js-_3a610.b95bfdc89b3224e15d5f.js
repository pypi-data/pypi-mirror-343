(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_vdom-extension_lib_index_js-_3a610"],{

/***/ "../packages/vdom-extension/lib/index.js":
/*!***********************************************!*\
  !*** ../packages/vdom-extension/lib/index.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MIME_TYPE": () => (/* binding */ MIME_TYPE),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_vdom__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/vdom */ "webpack/sharing/consume/default/@jupyterlab/vdom/@jupyterlab/vdom");
/* harmony import */ var _jupyterlab_vdom__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_vdom__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module vdom-extension
 */







/**
 * The MIME type for VDOM.
 */
const MIME_TYPE = 'application/vdom.v1+json';
/**
 * The name of the factory that creates VDOM widgets.
 */
const FACTORY_NAME = 'VDOM';
const plugin = {
    id: '@jupyterlab/vdom-extension:factory',
    requires: [_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry],
    optional: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _jupyterlab_vdom__WEBPACK_IMPORTED_MODULE_6__.IVDOMTracker,
    autoStart: true,
    activate: (app, rendermime, notebooks, restorer) => {
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'vdom-widget'
        });
        // Add a renderer factory to application rendermime registry.
        rendermime.addFactory({
            safe: false,
            mimeTypes: [MIME_TYPE],
            createRenderer: options => new _jupyterlab_vdom__WEBPACK_IMPORTED_MODULE_6__.RenderedVDOM(options)
        }, 0);
        if (notebooks) {
            notebooks.widgetAdded.connect((sender, panel) => {
                // Get the notebook's context and rendermime;
                const { context, content: { rendermime } } = panel;
                // Add the renderer factory to the notebook's rendermime registry;
                rendermime.addFactory({
                    safe: false,
                    mimeTypes: [MIME_TYPE],
                    createRenderer: options => new _jupyterlab_vdom__WEBPACK_IMPORTED_MODULE_6__.RenderedVDOM(options, context)
                }, 0);
            });
        }
        app.docRegistry.addFileType({
            name: 'vdom',
            mimeTypes: [MIME_TYPE],
            extensions: ['.vdom', '.vdom.json'],
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.reactIcon
        });
        const factory = new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.MimeDocumentFactory({
            renderTimeout: 1000,
            dataType: 'json',
            rendermime,
            name: FACTORY_NAME,
            primaryFileType: app.docRegistry.getFileType('vdom'),
            fileTypes: ['vdom', 'json'],
            defaultFor: ['vdom']
        });
        factory.widgetCreated.connect((sender, widget) => {
            widget.context.pathChanged.connect(() => {
                void tracker.save(widget);
            });
            void tracker.add(widget);
        });
        // Add widget factory to document registry.
        app.docRegistry.addWidgetFactory(factory);
        if (restorer) {
            // Handle state restoration.
            void restorer.restore(tracker, {
                command: 'docmanager:open',
                args: widget => ({
                    path: widget.context.path,
                    factory: FACTORY_NAME
                }),
                name: widget => widget.context.path
            });
        }
        return tracker;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdmRvbS1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU04QjtBQUNvQjtBQUN1QjtBQUNwQjtBQUNLO0FBQ1A7QUFDUTtBQUU5RDs7R0FFRztBQUNJLE1BQU0sU0FBUyxHQUFHLDBCQUEwQixDQUFDO0FBRXBEOztHQUVHO0FBQ0gsTUFBTSxZQUFZLEdBQUcsTUFBTSxDQUFDO0FBRTVCLE1BQU0sTUFBTSxHQUF3QztJQUNsRCxFQUFFLEVBQUUsb0NBQW9DO0lBQ3hDLFFBQVEsRUFBRSxDQUFDLHVFQUFtQixDQUFDO0lBQy9CLFFBQVEsRUFBRSxDQUFDLGtFQUFnQixFQUFFLG9FQUFlLENBQUM7SUFDN0MsUUFBUSxFQUFFLDBEQUFZO0lBQ3RCLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQ1IsR0FBb0IsRUFDcEIsVUFBK0IsRUFDL0IsU0FBa0MsRUFDbEMsUUFBZ0MsRUFDaEMsRUFBRTtRQUNGLE1BQU0sT0FBTyxHQUFHLElBQUksK0RBQWEsQ0FBZTtZQUM5QyxTQUFTLEVBQUUsYUFBYTtTQUN6QixDQUFDLENBQUM7UUFFSCw2REFBNkQ7UUFDN0QsVUFBVSxDQUFDLFVBQVUsQ0FDbkI7WUFDRSxJQUFJLEVBQUUsS0FBSztZQUNYLFNBQVMsRUFBRSxDQUFDLFNBQVMsQ0FBQztZQUN0QixjQUFjLEVBQUUsT0FBTyxDQUFDLEVBQUUsQ0FBQyxJQUFJLDBEQUFZLENBQUMsT0FBTyxDQUFDO1NBQ3JELEVBQ0QsQ0FBQyxDQUNGLENBQUM7UUFFRixJQUFJLFNBQVMsRUFBRTtZQUNiLFNBQVMsQ0FBQyxXQUFXLENBQUMsT0FBTyxDQUFDLENBQUMsTUFBTSxFQUFFLEtBQUssRUFBRSxFQUFFO2dCQUM5Qyw2Q0FBNkM7Z0JBQzdDLE1BQU0sRUFDSixPQUFPLEVBQ1AsT0FBTyxFQUFFLEVBQUUsVUFBVSxFQUFFLEVBQ3hCLEdBQUcsS0FBSyxDQUFDO2dCQUVWLGtFQUFrRTtnQkFDbEUsVUFBVSxDQUFDLFVBQVUsQ0FDbkI7b0JBQ0UsSUFBSSxFQUFFLEtBQUs7b0JBQ1gsU0FBUyxFQUFFLENBQUMsU0FBUyxDQUFDO29CQUN0QixjQUFjLEVBQUUsT0FBTyxDQUFDLEVBQUUsQ0FBQyxJQUFJLDBEQUFZLENBQUMsT0FBTyxFQUFFLE9BQU8sQ0FBQztpQkFDOUQsRUFDRCxDQUFDLENBQ0YsQ0FBQztZQUNKLENBQUMsQ0FBQyxDQUFDO1NBQ0o7UUFFRCxHQUFHLENBQUMsV0FBVyxDQUFDLFdBQVcsQ0FBQztZQUMxQixJQUFJLEVBQUUsTUFBTTtZQUNaLFNBQVMsRUFBRSxDQUFDLFNBQVMsQ0FBQztZQUN0QixVQUFVLEVBQUUsQ0FBQyxPQUFPLEVBQUUsWUFBWSxDQUFDO1lBQ25DLElBQUksRUFBRSxnRUFBUztTQUNoQixDQUFDLENBQUM7UUFFSCxNQUFNLE9BQU8sR0FBRyxJQUFJLHdFQUFtQixDQUFDO1lBQ3RDLGFBQWEsRUFBRSxJQUFJO1lBQ25CLFFBQVEsRUFBRSxNQUFNO1lBQ2hCLFVBQVU7WUFDVixJQUFJLEVBQUUsWUFBWTtZQUNsQixlQUFlLEVBQUUsR0FBRyxDQUFDLFdBQVcsQ0FBQyxXQUFXLENBQUMsTUFBTSxDQUFFO1lBQ3JELFNBQVMsRUFBRSxDQUFDLE1BQU0sRUFBRSxNQUFNLENBQUM7WUFDM0IsVUFBVSxFQUFFLENBQUMsTUFBTSxDQUFDO1NBQ3JCLENBQUMsQ0FBQztRQUVILE9BQU8sQ0FBQyxhQUFhLENBQUMsT0FBTyxDQUFDLENBQUMsTUFBTSxFQUFFLE1BQU0sRUFBRSxFQUFFO1lBQy9DLE1BQU0sQ0FBQyxPQUFPLENBQUMsV0FBVyxDQUFDLE9BQU8sQ0FBQyxHQUFHLEVBQUU7Z0JBQ3RDLEtBQUssT0FBTyxDQUFDLElBQUksQ0FBQyxNQUFNLENBQUMsQ0FBQztZQUM1QixDQUFDLENBQUMsQ0FBQztZQUNILEtBQUssT0FBTyxDQUFDLEdBQUcsQ0FBQyxNQUFNLENBQUMsQ0FBQztRQUMzQixDQUFDLENBQUMsQ0FBQztRQUVILDJDQUEyQztRQUMzQyxHQUFHLENBQUMsV0FBVyxDQUFDLGdCQUFnQixDQUFDLE9BQU8sQ0FBQyxDQUFDO1FBRTFDLElBQUksUUFBUSxFQUFFO1lBQ1osNEJBQTRCO1lBQzVCLEtBQUssUUFBUSxDQUFDLE9BQU8sQ0FBQyxPQUFPLEVBQUU7Z0JBQzdCLE9BQU8sRUFBRSxpQkFBaUI7Z0JBQzFCLElBQUksRUFBRSxNQUFNLENBQUMsRUFBRSxDQUFDLENBQUM7b0JBQ2YsSUFBSSxFQUFFLE1BQU0sQ0FBQyxPQUFPLENBQUMsSUFBSTtvQkFDekIsT0FBTyxFQUFFLFlBQVk7aUJBQ3RCLENBQUM7Z0JBQ0YsSUFBSSxFQUFFLE1BQU0sQ0FBQyxFQUFFLENBQUMsTUFBTSxDQUFDLE9BQU8sQ0FBQyxJQUFJO2FBQ3BDLENBQUMsQ0FBQztTQUNKO1FBRUQsT0FBTyxPQUFPLENBQUM7SUFDakIsQ0FBQztDQUNGLENBQUM7QUFFRixpRUFBZSxNQUFNLEVBQUMiLCJmaWxlIjoicGFja2FnZXNfdmRvbS1leHRlbnNpb25fbGliX2luZGV4X2pzLV8zYTYxMC5iOTViZmRjODliMzIyNGUxNWQ1Zi5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHZkb20tZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBXaWRnZXRUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgTWltZURvY3VtZW50LCBNaW1lRG9jdW1lbnRGYWN0b3J5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgSU5vdGVib29rVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IHJlYWN0SWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgSVZET01UcmFja2VyLCBSZW5kZXJlZFZET00gfSBmcm9tICdAanVweXRlcmxhYi92ZG9tJztcblxuLyoqXG4gKiBUaGUgTUlNRSB0eXBlIGZvciBWRE9NLlxuICovXG5leHBvcnQgY29uc3QgTUlNRV9UWVBFID0gJ2FwcGxpY2F0aW9uL3Zkb20udjEranNvbic7XG5cbi8qKlxuICogVGhlIG5hbWUgb2YgdGhlIGZhY3RvcnkgdGhhdCBjcmVhdGVzIFZET00gd2lkZ2V0cy5cbiAqL1xuY29uc3QgRkFDVE9SWV9OQU1FID0gJ1ZET00nO1xuXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJVkRPTVRyYWNrZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL3Zkb20tZXh0ZW5zaW9uOmZhY3RvcnknLFxuICByZXF1aXJlczogW0lSZW5kZXJNaW1lUmVnaXN0cnldLFxuICBvcHRpb25hbDogW0lOb3RlYm9va1RyYWNrZXIsIElMYXlvdXRSZXN0b3Jlcl0sXG4gIHByb3ZpZGVzOiBJVkRPTVRyYWNrZXIsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5LFxuICAgIG5vdGVib29rczogSU5vdGVib29rVHJhY2tlciB8IG51bGwsXG4gICAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPE1pbWVEb2N1bWVudD4oe1xuICAgICAgbmFtZXNwYWNlOiAndmRvbS13aWRnZXQnXG4gICAgfSk7XG5cbiAgICAvLyBBZGQgYSByZW5kZXJlciBmYWN0b3J5IHRvIGFwcGxpY2F0aW9uIHJlbmRlcm1pbWUgcmVnaXN0cnkuXG4gICAgcmVuZGVybWltZS5hZGRGYWN0b3J5KFxuICAgICAge1xuICAgICAgICBzYWZlOiBmYWxzZSxcbiAgICAgICAgbWltZVR5cGVzOiBbTUlNRV9UWVBFXSxcbiAgICAgICAgY3JlYXRlUmVuZGVyZXI6IG9wdGlvbnMgPT4gbmV3IFJlbmRlcmVkVkRPTShvcHRpb25zKVxuICAgICAgfSxcbiAgICAgIDBcbiAgICApO1xuXG4gICAgaWYgKG5vdGVib29rcykge1xuICAgICAgbm90ZWJvb2tzLndpZGdldEFkZGVkLmNvbm5lY3QoKHNlbmRlciwgcGFuZWwpID0+IHtcbiAgICAgICAgLy8gR2V0IHRoZSBub3RlYm9vaydzIGNvbnRleHQgYW5kIHJlbmRlcm1pbWU7XG4gICAgICAgIGNvbnN0IHtcbiAgICAgICAgICBjb250ZXh0LFxuICAgICAgICAgIGNvbnRlbnQ6IHsgcmVuZGVybWltZSB9XG4gICAgICAgIH0gPSBwYW5lbDtcblxuICAgICAgICAvLyBBZGQgdGhlIHJlbmRlcmVyIGZhY3RvcnkgdG8gdGhlIG5vdGVib29rJ3MgcmVuZGVybWltZSByZWdpc3RyeTtcbiAgICAgICAgcmVuZGVybWltZS5hZGRGYWN0b3J5KFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHNhZmU6IGZhbHNlLFxuICAgICAgICAgICAgbWltZVR5cGVzOiBbTUlNRV9UWVBFXSxcbiAgICAgICAgICAgIGNyZWF0ZVJlbmRlcmVyOiBvcHRpb25zID0+IG5ldyBSZW5kZXJlZFZET00ob3B0aW9ucywgY29udGV4dClcbiAgICAgICAgICB9LFxuICAgICAgICAgIDBcbiAgICAgICAgKTtcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGFwcC5kb2NSZWdpc3RyeS5hZGRGaWxlVHlwZSh7XG4gICAgICBuYW1lOiAndmRvbScsXG4gICAgICBtaW1lVHlwZXM6IFtNSU1FX1RZUEVdLFxuICAgICAgZXh0ZW5zaW9uczogWycudmRvbScsICcudmRvbS5qc29uJ10sXG4gICAgICBpY29uOiByZWFjdEljb25cbiAgICB9KTtcblxuICAgIGNvbnN0IGZhY3RvcnkgPSBuZXcgTWltZURvY3VtZW50RmFjdG9yeSh7XG4gICAgICByZW5kZXJUaW1lb3V0OiAxMDAwLFxuICAgICAgZGF0YVR5cGU6ICdqc29uJyxcbiAgICAgIHJlbmRlcm1pbWUsXG4gICAgICBuYW1lOiBGQUNUT1JZX05BTUUsXG4gICAgICBwcmltYXJ5RmlsZVR5cGU6IGFwcC5kb2NSZWdpc3RyeS5nZXRGaWxlVHlwZSgndmRvbScpISxcbiAgICAgIGZpbGVUeXBlczogWyd2ZG9tJywgJ2pzb24nXSxcbiAgICAgIGRlZmF1bHRGb3I6IFsndmRvbSddXG4gICAgfSk7XG5cbiAgICBmYWN0b3J5LndpZGdldENyZWF0ZWQuY29ubmVjdCgoc2VuZGVyLCB3aWRnZXQpID0+IHtcbiAgICAgIHdpZGdldC5jb250ZXh0LnBhdGhDaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICB2b2lkIHRyYWNrZXIuc2F2ZSh3aWRnZXQpO1xuICAgICAgfSk7XG4gICAgICB2b2lkIHRyYWNrZXIuYWRkKHdpZGdldCk7XG4gICAgfSk7XG5cbiAgICAvLyBBZGQgd2lkZ2V0IGZhY3RvcnkgdG8gZG9jdW1lbnQgcmVnaXN0cnkuXG4gICAgYXBwLmRvY1JlZ2lzdHJ5LmFkZFdpZGdldEZhY3RvcnkoZmFjdG9yeSk7XG5cbiAgICBpZiAocmVzdG9yZXIpIHtcbiAgICAgIC8vIEhhbmRsZSBzdGF0ZSByZXN0b3JhdGlvbi5cbiAgICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZSh0cmFja2VyLCB7XG4gICAgICAgIGNvbW1hbmQ6ICdkb2NtYW5hZ2VyOm9wZW4nLFxuICAgICAgICBhcmdzOiB3aWRnZXQgPT4gKHtcbiAgICAgICAgICBwYXRoOiB3aWRnZXQuY29udGV4dC5wYXRoLFxuICAgICAgICAgIGZhY3Rvcnk6IEZBQ1RPUllfTkFNRVxuICAgICAgICB9KSxcbiAgICAgICAgbmFtZTogd2lkZ2V0ID0+IHdpZGdldC5jb250ZXh0LnBhdGhcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIHJldHVybiB0cmFja2VyO1xuICB9XG59O1xuXG5leHBvcnQgZGVmYXVsdCBwbHVnaW47XG4iXSwic291cmNlUm9vdCI6IiJ9