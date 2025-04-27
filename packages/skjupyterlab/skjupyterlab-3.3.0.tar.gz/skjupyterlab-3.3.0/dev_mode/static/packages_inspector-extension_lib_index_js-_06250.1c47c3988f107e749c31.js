(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_inspector-extension_lib_index_js-_06250"],{

/***/ "../packages/inspector-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../packages/inspector-extension/lib/index.js ***!
  \****************************************************/
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
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/inspector */ "webpack/sharing/consume/default/@jupyterlab/inspector/@jupyterlab/inspector");
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module inspector-extension
 */








/**
 * The command IDs used by the inspector plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'inspector:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing code introspection.
 */
const inspector = {
    id: '@jupyterlab/inspector-extension:inspector',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__.ILauncher, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.IInspector,
    autoStart: true,
    activate: (app, translator, palette, launcher, restorer) => {
        const trans = translator.load('jupyterlab');
        const { commands, shell } = app;
        const command = CommandIDs.open;
        const label = trans.__('Show Contextual Help');
        const namespace = 'inspector';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace
        });
        function isInspectorOpen() {
            return inspector && !inspector.isDisposed;
        }
        let source = null;
        let inspector;
        function openInspector(args) {
            var _a;
            if (!isInspectorOpen()) {
                inspector = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                    content: new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.InspectorPanel({ translator })
                });
                inspector.id = 'jp-inspector';
                inspector.title.label = label;
                inspector.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.inspectorIcon;
                void tracker.add(inspector);
                source = source && !source.isDisposed ? source : null;
                inspector.content.source = source;
                (_a = inspector.content.source) === null || _a === void 0 ? void 0 : _a.onEditorChange(args);
            }
            if (!inspector.isAttached) {
                shell.add(inspector, 'main', { activate: false, mode: 'split-right' });
            }
            shell.activateById(inspector.id);
            return inspector;
        }
        // Add command to registry.
        commands.addCommand(command, {
            caption: trans.__('Live updating code documentation from the active kernel'),
            isEnabled: () => !inspector ||
                inspector.isDisposed ||
                !inspector.isAttached ||
                !inspector.isVisible,
            label,
            icon: args => (args.isLauncher ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.inspectorIcon : undefined),
            execute: args => {
                var _a;
                const text = args && args.text;
                const refresh = args && args.refresh;
                // if inspector is open, see if we need a refresh
                if (isInspectorOpen() && refresh)
                    (_a = inspector.content.source) === null || _a === void 0 ? void 0 : _a.onEditorChange(text);
                else
                    openInspector(text);
            }
        });
        // Add command to UI where possible.
        if (palette) {
            palette.addItem({ command, category: label });
        }
        if (launcher) {
            launcher.add({ command, args: { isLauncher: true } });
        }
        // Handle state restoration.
        if (restorer) {
            void restorer.restore(tracker, { command, name: () => 'inspector' });
        }
        // Create a proxy to pass the `source` to the current inspector.
        const proxy = Object.defineProperty({}, 'source', {
            get: () => !inspector || inspector.isDisposed ? null : inspector.content.source,
            set: (src) => {
                source = src && !src.isDisposed ? src : null;
                if (inspector && !inspector.isDisposed) {
                    inspector.content.source = source;
                }
            }
        });
        return proxy;
    }
};
/**
 * An extension that registers consoles for inspection.
 */
const consoles = {
    id: '@jupyterlab/inspector-extension:consoles',
    requires: [_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.IInspector, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__.IConsoleTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, manager, consoles, labShell, translator) => {
        // Maintain association of new consoles with their respective handlers.
        const handlers = {};
        // Create a handler for each console that is created.
        consoles.widgetAdded.connect((sender, parent) => {
            const sessionContext = parent.console.sessionContext;
            const rendermime = parent.console.rendermime;
            const connector = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.KernelConnector({ sessionContext });
            const handler = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.InspectionHandler({ connector, rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            const cell = parent.console.promptCell;
            handler.editor = cell && cell.editor;
            // Listen for prompt creation.
            parent.console.promptCellCreated.connect((sender, cell) => {
                handler.editor = cell && cell.editor;
            });
            // Listen for parent disposal.
            parent.disposed.connect(() => {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of console instances and set inspector source.
        labShell.currentChanged.connect((_, args) => {
            const widget = args.newValue;
            if (!widget || !consoles.has(widget)) {
                return;
            }
            const source = handlers[widget.id];
            if (source) {
                manager.source = source;
            }
        });
    }
};
/**
 * An extension that registers notebooks for inspection.
 */
const notebooks = {
    id: '@jupyterlab/inspector-extension:notebooks',
    requires: [_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.IInspector, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__.INotebookTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, manager, notebooks, labShell) => {
        // Maintain association of new notebooks with their respective handlers.
        const handlers = {};
        // Create a handler for each notebook that is created.
        notebooks.widgetAdded.connect((sender, parent) => {
            const sessionContext = parent.sessionContext;
            const rendermime = parent.content.rendermime;
            const connector = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.KernelConnector({ sessionContext });
            const handler = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.InspectionHandler({ connector, rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            const cell = parent.content.activeCell;
            handler.editor = cell && cell.editor;
            // Listen for active cell changes.
            parent.content.activeCellChanged.connect((sender, cell) => {
                handler.editor = cell && cell.editor;
            });
            // Listen for parent disposal.
            parent.disposed.connect(() => {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of notebook instances and set inspector source.
        labShell.currentChanged.connect((sender, args) => {
            const widget = args.newValue;
            if (!widget || !notebooks.has(widget)) {
                return;
            }
            const source = handlers[widget.id];
            if (source) {
                manager.source = source;
            }
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [inspector, consoles, notebooks];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW5zcGVjdG9yLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU84QjtBQUtIO0FBQ3dCO0FBTXZCO0FBQ2tCO0FBQ087QUFDRjtBQUNJO0FBRTFEOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBRW5CO0FBRkQsV0FBVSxVQUFVO0lBQ0wsZUFBSSxHQUFHLGdCQUFnQixDQUFDO0FBQ3ZDLENBQUMsRUFGUyxVQUFVLEtBQVYsVUFBVSxRQUVuQjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxTQUFTLEdBQXNDO0lBQ25ELEVBQUUsRUFBRSwyQ0FBMkM7SUFDL0MsUUFBUSxFQUFFLENBQUMsZ0VBQVcsQ0FBQztJQUN2QixRQUFRLEVBQUUsQ0FBQyxpRUFBZSxFQUFFLDJEQUFTLEVBQUUsb0VBQWUsQ0FBQztJQUN2RCxRQUFRLEVBQUUsNkRBQVU7SUFDcEIsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixVQUF1QixFQUN2QixPQUErQixFQUMvQixRQUEwQixFQUMxQixRQUFnQyxFQUNwQixFQUFFO1FBQ2QsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztRQUM1QyxNQUFNLEVBQUUsUUFBUSxFQUFFLEtBQUssRUFBRSxHQUFHLEdBQUcsQ0FBQztRQUNoQyxNQUFNLE9BQU8sR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDO1FBQ2hDLE1BQU0sS0FBSyxHQUFHLEtBQUssQ0FBQyxFQUFFLENBQUMsc0JBQXNCLENBQUMsQ0FBQztRQUMvQyxNQUFNLFNBQVMsR0FBRyxXQUFXLENBQUM7UUFDOUIsTUFBTSxPQUFPLEdBQUcsSUFBSSwrREFBYSxDQUFpQztZ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ImZpbGUiOiJwYWNrYWdlc19pbnNwZWN0b3ItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy1fMDYyNTAuMWM0N2MzOTg4ZjEwN2U3NDljMzEuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBpbnNwZWN0b3ItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlNoZWxsLFxuICBJTGF5b3V0UmVzdG9yZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgTWFpbkFyZWFXaWRnZXQsXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSUNvbnNvbGVUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29uc29sZSc7XG5pbXBvcnQge1xuICBJSW5zcGVjdG9yLFxuICBJbnNwZWN0aW9uSGFuZGxlcixcbiAgSW5zcGVjdG9yUGFuZWwsXG4gIEtlcm5lbENvbm5lY3RvclxufSBmcm9tICdAanVweXRlcmxhYi9pbnNwZWN0b3InO1xuaW1wb3J0IHsgSUxhdW5jaGVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbGF1bmNoZXInO1xuaW1wb3J0IHsgSU5vdGVib29rVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgaW5zcGVjdG9ySWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBpbnNwZWN0b3IgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBvcGVuID0gJ2luc3BlY3RvcjpvcGVuJztcbn1cblxuLyoqXG4gKiBBIHNlcnZpY2UgcHJvdmlkaW5nIGNvZGUgaW50cm9zcGVjdGlvbi5cbiAqL1xuY29uc3QgaW5zcGVjdG9yOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUluc3BlY3Rvcj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvaW5zcGVjdG9yLWV4dGVuc2lvbjppbnNwZWN0b3InLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJQ29tbWFuZFBhbGV0dGUsIElMYXVuY2hlciwgSUxheW91dFJlc3RvcmVyXSxcbiAgcHJvdmlkZXM6IElJbnNwZWN0b3IsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsLFxuICAgIGxhdW5jaGVyOiBJTGF1bmNoZXIgfCBudWxsLFxuICAgIHJlc3RvcmVyOiBJTGF5b3V0UmVzdG9yZXIgfCBudWxsXG4gICk6IElJbnNwZWN0b3IgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgICBjb25zdCBjb21tYW5kID0gQ29tbWFuZElEcy5vcGVuO1xuICAgIGNvbnN0IGxhYmVsID0gdHJhbnMuX18oJ1Nob3cgQ29udGV4dHVhbCBIZWxwJyk7XG4gICAgY29uc3QgbmFtZXNwYWNlID0gJ2luc3BlY3Rvcic7XG4gICAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPE1haW5BcmVhV2lkZ2V0PEluc3BlY3RvclBhbmVsPj4oe1xuICAgICAgbmFtZXNwYWNlXG4gICAgfSk7XG5cbiAgICBmdW5jdGlvbiBpc0luc3BlY3Rvck9wZW4oKSB7XG4gICAgICByZXR1cm4gaW5zcGVjdG9yICYmICFpbnNwZWN0b3IuaXNEaXNwb3NlZDtcbiAgICB9XG5cbiAgICBsZXQgc291cmNlOiBJSW5zcGVjdG9yLklJbnNwZWN0YWJsZSB8IG51bGwgPSBudWxsO1xuICAgIGxldCBpbnNwZWN0b3I6IE1haW5BcmVhV2lkZ2V0PEluc3BlY3RvclBhbmVsPjtcbiAgICBmdW5jdGlvbiBvcGVuSW5zcGVjdG9yKGFyZ3M6IHN0cmluZyk6IE1haW5BcmVhV2lkZ2V0PEluc3BlY3RvclBhbmVsPiB7XG4gICAgICBpZiAoIWlzSW5zcGVjdG9yT3BlbigpKSB7XG4gICAgICAgIGluc3BlY3RvciA9IG5ldyBNYWluQXJlYVdpZGdldCh7XG4gICAgICAgICAgY29udGVudDogbmV3IEluc3BlY3RvclBhbmVsKHsgdHJhbnNsYXRvciB9KVxuICAgICAgICB9KTtcbiAgICAgICAgaW5zcGVjdG9yLmlkID0gJ2pwLWluc3BlY3Rvcic7XG4gICAgICAgIGluc3BlY3Rvci50aXRsZS5sYWJlbCA9IGxhYmVsO1xuICAgICAgICBpbnNwZWN0b3IudGl0bGUuaWNvbiA9IGluc3BlY3Rvckljb247XG4gICAgICAgIHZvaWQgdHJhY2tlci5hZGQoaW5zcGVjdG9yKTtcbiAgICAgICAgc291cmNlID0gc291cmNlICYmICFzb3VyY2UuaXNEaXNwb3NlZCA/IHNvdXJjZSA6IG51bGw7XG4gICAgICAgIGluc3BlY3Rvci5jb250ZW50LnNvdXJjZSA9IHNvdXJjZTtcbiAgICAgICAgaW5zcGVjdG9yLmNvbnRlbnQuc291cmNlPy5vbkVkaXRvckNoYW5nZShhcmdzKTtcbiAgICAgIH1cbiAgICAgIGlmICghaW5zcGVjdG9yLmlzQXR0YWNoZWQpIHtcbiAgICAgICAgc2hlbGwuYWRkKGluc3BlY3RvciwgJ21haW4nLCB7IGFjdGl2YXRlOiBmYWxzZSwgbW9kZTogJ3NwbGl0LXJpZ2h0JyB9KTtcbiAgICAgIH1cbiAgICAgIHNoZWxsLmFjdGl2YXRlQnlJZChpbnNwZWN0b3IuaWQpO1xuICAgICAgcmV0dXJuIGluc3BlY3RvcjtcbiAgICB9XG5cbiAgICAvLyBBZGQgY29tbWFuZCB0byByZWdpc3RyeS5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKGNvbW1hbmQsIHtcbiAgICAgIGNhcHRpb246IHRyYW5zLl9fKFxuICAgICAgICAnTGl2ZSB1cGRhdGluZyBjb2RlIGRvY3VtZW50YXRpb24gZnJvbSB0aGUgYWN0aXZlIGtlcm5lbCdcbiAgICAgICksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+XG4gICAgICAgICFpbnNwZWN0b3IgfHxcbiAgICAgICAgaW5zcGVjdG9yLmlzRGlzcG9zZWQgfHxcbiAgICAgICAgIWluc3BlY3Rvci5pc0F0dGFjaGVkIHx8XG4gICAgICAgICFpbnNwZWN0b3IuaXNWaXNpYmxlLFxuICAgICAgbGFiZWwsXG4gICAgICBpY29uOiBhcmdzID0+IChhcmdzLmlzTGF1bmNoZXIgPyBpbnNwZWN0b3JJY29uIDogdW5kZWZpbmVkKSxcbiAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgICBjb25zdCB0ZXh0ID0gYXJncyAmJiAoYXJncy50ZXh0IGFzIHN0cmluZyk7XG4gICAgICAgIGNvbnN0IHJlZnJlc2ggPSBhcmdzICYmIChhcmdzLnJlZnJlc2ggYXMgYm9vbGVhbik7XG4gICAgICAgIC8vIGlmIGluc3BlY3RvciBpcyBvcGVuLCBzZWUgaWYgd2UgbmVlZCBhIHJlZnJlc2hcbiAgICAgICAgaWYgKGlzSW5zcGVjdG9yT3BlbigpICYmIHJlZnJlc2gpXG4gICAgICAgICAgaW5zcGVjdG9yLmNvbnRlbnQuc291cmNlPy5vbkVkaXRvckNoYW5nZSh0ZXh0KTtcbiAgICAgICAgZWxzZSBvcGVuSW5zcGVjdG9yKHRleHQpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gQWRkIGNvbW1hbmQgdG8gVUkgd2hlcmUgcG9zc2libGUuXG4gICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNvbW1hbmQsIGNhdGVnb3J5OiBsYWJlbCB9KTtcbiAgICB9XG4gICAgaWYgKGxhdW5jaGVyKSB7XG4gICAgICBsYXVuY2hlci5hZGQoeyBjb21tYW5kLCBhcmdzOiB7IGlzTGF1bmNoZXI6IHRydWUgfSB9KTtcbiAgICB9XG5cbiAgICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gICAgaWYgKHJlc3RvcmVyKSB7XG4gICAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwgeyBjb21tYW5kLCBuYW1lOiAoKSA9PiAnaW5zcGVjdG9yJyB9KTtcbiAgICB9XG5cbiAgICAvLyBDcmVhdGUgYSBwcm94eSB0byBwYXNzIHRoZSBgc291cmNlYCB0byB0aGUgY3VycmVudCBpbnNwZWN0b3IuXG4gICAgY29uc3QgcHJveHk6IElJbnNwZWN0b3IgPSBPYmplY3QuZGVmaW5lUHJvcGVydHkoe30sICdzb3VyY2UnLCB7XG4gICAgICBnZXQ6ICgpOiBJSW5zcGVjdG9yLklJbnNwZWN0YWJsZSB8IG51bGwgPT5cbiAgICAgICAgIWluc3BlY3RvciB8fCBpbnNwZWN0b3IuaXNEaXNwb3NlZCA/IG51bGwgOiBpbnNwZWN0b3IuY29udGVudC5zb3VyY2UsXG4gICAgICBzZXQ6IChzcmM6IElJbnNwZWN0b3IuSUluc3BlY3RhYmxlIHwgbnVsbCkgPT4ge1xuICAgICAgICBzb3VyY2UgPSBzcmMgJiYgIXNyYy5pc0Rpc3Bvc2VkID8gc3JjIDogbnVsbDtcbiAgICAgICAgaWYgKGluc3BlY3RvciAmJiAhaW5zcGVjdG9yLmlzRGlzcG9zZWQpIHtcbiAgICAgICAgICBpbnNwZWN0b3IuY29udGVudC5zb3VyY2UgPSBzb3VyY2U7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIHJldHVybiBwcm94eTtcbiAgfVxufTtcblxuLyoqXG4gKiBBbiBleHRlbnNpb24gdGhhdCByZWdpc3RlcnMgY29uc29sZXMgZm9yIGluc3BlY3Rpb24uXG4gKi9cbmNvbnN0IGNvbnNvbGVzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvaW5zcGVjdG9yLWV4dGVuc2lvbjpjb25zb2xlcycsXG4gIHJlcXVpcmVzOiBbSUluc3BlY3RvciwgSUNvbnNvbGVUcmFja2VyLCBJTGFiU2hlbGxdLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbWFuYWdlcjogSUluc3BlY3RvcixcbiAgICBjb25zb2xlczogSUNvbnNvbGVUcmFja2VyLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKTogdm9pZCA9PiB7XG4gICAgLy8gTWFpbnRhaW4gYXNzb2NpYXRpb24gb2YgbmV3IGNvbnNvbGVzIHdpdGggdGhlaXIgcmVzcGVjdGl2ZSBoYW5kbGVycy5cbiAgICBjb25zdCBoYW5kbGVyczogeyBbaWQ6IHN0cmluZ106IEluc3BlY3Rpb25IYW5kbGVyIH0gPSB7fTtcblxuICAgIC8vIENyZWF0ZSBhIGhhbmRsZXIgZm9yIGVhY2ggY29uc29sZSB0aGF0IGlzIGNyZWF0ZWQuXG4gICAgY29uc29sZXMud2lkZ2V0QWRkZWQuY29ubmVjdCgoc2VuZGVyLCBwYXJlbnQpID0+IHtcbiAgICAgIGNvbnN0IHNlc3Npb25Db250ZXh0ID0gcGFyZW50LmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQ7XG4gICAgICBjb25zdCByZW5kZXJtaW1lID0gcGFyZW50LmNvbnNvbGUucmVuZGVybWltZTtcbiAgICAgIGNvbnN0IGNvbm5lY3RvciA9IG5ldyBLZXJuZWxDb25uZWN0b3IoeyBzZXNzaW9uQ29udGV4dCB9KTtcbiAgICAgIGNvbnN0IGhhbmRsZXIgPSBuZXcgSW5zcGVjdGlvbkhhbmRsZXIoeyBjb25uZWN0b3IsIHJlbmRlcm1pbWUgfSk7XG5cbiAgICAgIC8vIEFzc29jaWF0ZSB0aGUgaGFuZGxlciB0byB0aGUgd2lkZ2V0LlxuICAgICAgaGFuZGxlcnNbcGFyZW50LmlkXSA9IGhhbmRsZXI7XG5cbiAgICAgIC8vIFNldCB0aGUgaW5pdGlhbCBlZGl0b3IuXG4gICAgICBjb25zdCBjZWxsID0gcGFyZW50LmNvbnNvbGUucHJvbXB0Q2VsbDtcbiAgICAgIGhhbmRsZXIuZWRpdG9yID0gY2VsbCAmJiBjZWxsLmVkaXRvcjtcblxuICAgICAgLy8gTGlzdGVuIGZvciBwcm9tcHQgY3JlYXRpb24uXG4gICAgICBwYXJlbnQuY29uc29sZS5wcm9tcHRDZWxsQ3JlYXRlZC5jb25uZWN0KChzZW5kZXIsIGNlbGwpID0+IHtcbiAgICAgICAgaGFuZGxlci5lZGl0b3IgPSBjZWxsICYmIGNlbGwuZWRpdG9yO1xuICAgICAgfSk7XG5cbiAgICAgIC8vIExpc3RlbiBmb3IgcGFyZW50IGRpc3Bvc2FsLlxuICAgICAgcGFyZW50LmRpc3Bvc2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICBkZWxldGUgaGFuZGxlcnNbcGFyZW50LmlkXTtcbiAgICAgICAgaGFuZGxlci5kaXNwb3NlKCk7XG4gICAgICB9KTtcbiAgICB9KTtcblxuICAgIC8vIEtlZXAgdHJhY2sgb2YgY29uc29sZSBpbnN0YW5jZXMgYW5kIHNldCBpbnNwZWN0b3Igc291cmNlLlxuICAgIGxhYlNoZWxsLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QoKF8sIGFyZ3MpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IGFyZ3MubmV3VmFsdWU7XG4gICAgICBpZiAoIXdpZGdldCB8fCAhY29uc29sZXMuaGFzKHdpZGdldCkpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3Qgc291cmNlID0gaGFuZGxlcnNbd2lkZ2V0LmlkXTtcbiAgICAgIGlmIChzb3VyY2UpIHtcbiAgICAgICAgbWFuYWdlci5zb3VyY2UgPSBzb3VyY2U7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogQW4gZXh0ZW5zaW9uIHRoYXQgcmVnaXN0ZXJzIG5vdGVib29rcyBmb3IgaW5zcGVjdGlvbi5cbiAqL1xuY29uc3Qgbm90ZWJvb2tzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvaW5zcGVjdG9yLWV4dGVuc2lvbjpub3RlYm9va3MnLFxuICByZXF1aXJlczogW0lJbnNwZWN0b3IsIElOb3RlYm9va1RyYWNrZXIsIElMYWJTaGVsbF0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBtYW5hZ2VyOiBJSW5zcGVjdG9yLFxuICAgIG5vdGVib29rczogSU5vdGVib29rVHJhY2tlcixcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsXG4gICk6IHZvaWQgPT4ge1xuICAgIC8vIE1haW50YWluIGFzc29jaWF0aW9uIG9mIG5ldyBub3RlYm9va3Mgd2l0aCB0aGVpciByZXNwZWN0aXZlIGhhbmRsZXJzLlxuICAgIGNvbnN0IGhhbmRsZXJzOiB7IFtpZDogc3RyaW5nXTogSW5zcGVjdGlvbkhhbmRsZXIgfSA9IHt9O1xuXG4gICAgLy8gQ3JlYXRlIGEgaGFuZGxlciBmb3IgZWFjaCBub3RlYm9vayB0aGF0IGlzIGNyZWF0ZWQuXG4gICAgbm90ZWJvb2tzLndpZGdldEFkZGVkLmNvbm5lY3QoKHNlbmRlciwgcGFyZW50KSA9PiB7XG4gICAgICBjb25zdCBzZXNzaW9uQ29udGV4dCA9IHBhcmVudC5zZXNzaW9uQ29udGV4dDtcbiAgICAgIGNvbnN0IHJlbmRlcm1pbWUgPSBwYXJlbnQuY29udGVudC5yZW5kZXJtaW1lO1xuICAgICAgY29uc3QgY29ubmVjdG9yID0gbmV3IEtlcm5lbENvbm5lY3Rvcih7IHNlc3Npb25Db250ZXh0IH0pO1xuICAgICAgY29uc3QgaGFuZGxlciA9IG5ldyBJbnNwZWN0aW9uSGFuZGxlcih7IGNvbm5lY3RvciwgcmVuZGVybWltZSB9KTtcblxuICAgICAgLy8gQXNzb2NpYXRlIHRoZSBoYW5kbGVyIHRvIHRoZSB3aWRnZXQuXG4gICAgICBoYW5kbGVyc1twYXJlbnQuaWRdID0gaGFuZGxlcjtcblxuICAgICAgLy8gU2V0IHRoZSBpbml0aWFsIGVkaXRvci5cbiAgICAgIGNvbnN0IGNlbGwgPSBwYXJlbnQuY29udGVudC5hY3RpdmVDZWxsO1xuICAgICAgaGFuZGxlci5lZGl0b3IgPSBjZWxsICYmIGNlbGwuZWRpdG9yO1xuXG4gICAgICAvLyBMaXN0ZW4gZm9yIGFjdGl2ZSBjZWxsIGNoYW5nZXMuXG4gICAgICBwYXJlbnQuY29udGVudC5hY3RpdmVDZWxsQ2hhbmdlZC5jb25uZWN0KChzZW5kZXIsIGNlbGwpID0+IHtcbiAgICAgICAgaGFuZGxlci5lZGl0b3IgPSBjZWxsICYmIGNlbGwuZWRpdG9yO1xuICAgICAgfSk7XG5cbiAgICAgIC8vIExpc3RlbiBmb3IgcGFyZW50IGRpc3Bvc2FsLlxuICAgICAgcGFyZW50LmRpc3Bvc2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICBkZWxldGUgaGFuZGxlcnNbcGFyZW50LmlkXTtcbiAgICAgICAgaGFuZGxlci5kaXNwb3NlKCk7XG4gICAgICB9KTtcbiAgICB9KTtcblxuICAgIC8vIEtlZXAgdHJhY2sgb2Ygbm90ZWJvb2sgaW5zdGFuY2VzIGFuZCBzZXQgaW5zcGVjdG9yIHNvdXJjZS5cbiAgICBsYWJTaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KChzZW5kZXIsIGFyZ3MpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IGFyZ3MubmV3VmFsdWU7XG4gICAgICBpZiAoIXdpZGdldCB8fCAhbm90ZWJvb2tzLmhhcyh3aWRnZXQpKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IHNvdXJjZSA9IGhhbmRsZXJzW3dpZGdldC5pZF07XG4gICAgICBpZiAoc291cmNlKSB7XG4gICAgICAgIG1hbmFnZXIuc291cmNlID0gc291cmNlO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2lucyBhcyBkZWZhdWx0LlxuICovXG5jb25zdCBwbHVnaW5zOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48YW55PltdID0gW2luc3BlY3RvciwgY29uc29sZXMsIG5vdGVib29rc107XG5leHBvcnQgZGVmYXVsdCBwbHVnaW5zO1xuIl0sInNvdXJjZVJvb3QiOiIifQ==