(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_completer-extension_lib_index_js"],{

/***/ "../packages/completer-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../packages/completer-extension/lib/index.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/completer */ "webpack/sharing/consume/default/@jupyterlab/completer/@jupyterlab/completer");
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module completer-extension
 */






/**
 * The command IDs used by the completer plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.invoke = 'completer:invoke';
    CommandIDs.invokeConsole = 'completer:invoke-console';
    CommandIDs.invokeNotebook = 'completer:invoke-notebook';
    CommandIDs.invokeFile = 'completer:invoke-file';
    CommandIDs.select = 'completer:select';
    CommandIDs.selectConsole = 'completer:select-console';
    CommandIDs.selectNotebook = 'completer:select-notebook';
    CommandIDs.selectFile = 'completer:select-file';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin providing code completion for editors.
 */
const manager = {
    id: '@jupyterlab/completer-extension:manager',
    autoStart: true,
    provides: _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionManager,
    activate: (app) => {
        const handlers = {};
        app.commands.addCommand(CommandIDs.invoke, {
            execute: args => {
                const id = args && args['id'];
                if (!id) {
                    return;
                }
                const handler = handlers[id];
                if (handler) {
                    handler.invoke();
                }
            }
        });
        app.commands.addCommand(CommandIDs.select, {
            execute: args => {
                const id = args && args['id'];
                if (!id) {
                    return;
                }
                const handler = handlers[id];
                if (handler) {
                    handler.completer.selectActive();
                }
            }
        });
        return {
            register: (completable, renderer = _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.Completer.defaultRenderer) => {
                const { connector, editor, parent } = completable;
                const model = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.CompleterModel();
                const completer = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.Completer({ editor, model, renderer });
                const handler = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.CompletionHandler({
                    completer,
                    connector
                });
                const id = parent.id;
                // Hide the widget when it first loads.
                completer.hide();
                // Associate the handler with the parent widget.
                handlers[id] = handler;
                // Set the handler's editor.
                handler.editor = editor;
                // Attach the completer widget.
                _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget.attach(completer, document.body);
                // Listen for parent disposal.
                parent.disposed.connect(() => {
                    delete handlers[id];
                    model.dispose();
                    completer.dispose();
                    handler.dispose();
                });
                return handler;
            }
        };
    }
};
/**
 * An extension that registers consoles for code completion.
 */
const consoles = {
    id: '@jupyterlab/completer-extension:consoles',
    requires: [_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionManager, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__.IConsoleTracker],
    autoStart: true,
    activate: (app, manager, consoles) => {
        // Create a handler for each console that is created.
        consoles.widgetAdded.connect((sender, widget) => {
            var _a, _b;
            const anchor = widget.console;
            const editor = (_b = (_a = anchor.promptCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
            const session = anchor.sessionContext.session;
            // TODO: CompletionConnector assumes editor and session are not null
            const connector = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.CompletionConnector({ session, editor });
            const handler = manager.register({ connector, editor, parent: widget });
            const updateConnector = () => {
                var _a, _b;
                const editor = (_b = (_a = anchor.promptCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
                const session = anchor.sessionContext.session;
                handler.editor = editor;
                // TODO: CompletionConnector assumes editor and session are not null
                handler.connector = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.CompletionConnector({ session, editor });
            };
            // Update the handler whenever the prompt or session changes
            anchor.promptCellCreated.connect(updateConnector);
            anchor.sessionContext.sessionChanged.connect(updateConnector);
        });
        // Add console completer invoke command.
        app.commands.addCommand(CommandIDs.invokeConsole, {
            execute: () => {
                const id = consoles.currentWidget && consoles.currentWidget.id;
                if (id) {
                    return app.commands.execute(CommandIDs.invoke, { id });
                }
            }
        });
        // Add console completer select command.
        app.commands.addCommand(CommandIDs.selectConsole, {
            execute: () => {
                const id = consoles.currentWidget && consoles.currentWidget.id;
                if (id) {
                    return app.commands.execute(CommandIDs.select, { id });
                }
            }
        });
        // Set enter key for console completer select command.
        app.commands.addKeyBinding({
            command: CommandIDs.selectConsole,
            keys: ['Enter'],
            selector: `.jp-ConsolePanel .jp-mod-completer-active`
        });
    }
};
/**
 * An extension that registers notebooks for code completion.
 */
const notebooks = {
    id: '@jupyterlab/completer-extension:notebooks',
    requires: [_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker],
    autoStart: true,
    activate: (app, manager, notebooks) => {
        // Create a handler for each notebook that is created.
        notebooks.widgetAdded.connect((sender, panel) => {
            var _a, _b;
            const editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
            const session = panel.sessionContext.session;
            // TODO: CompletionConnector assumes editor and session are not null
            const connector = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.CompletionConnector({ session, editor });
            const handler = manager.register({ connector, editor, parent: panel });
            const updateConnector = () => {
                var _a, _b;
                const editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
                const session = panel.sessionContext.session;
                handler.editor = editor;
                // TODO: CompletionConnector assumes editor and session are not null
                handler.connector = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.CompletionConnector({ session, editor });
            };
            // Update the handler whenever the prompt or session changes
            panel.content.activeCellChanged.connect(updateConnector);
            panel.sessionContext.sessionChanged.connect(updateConnector);
        });
        // Add notebook completer command.
        app.commands.addCommand(CommandIDs.invokeNotebook, {
            execute: () => {
                var _a;
                const panel = notebooks.currentWidget;
                if (panel && ((_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.type) === 'code') {
                    return app.commands.execute(CommandIDs.invoke, { id: panel.id });
                }
            }
        });
        // Add notebook completer select command.
        app.commands.addCommand(CommandIDs.selectNotebook, {
            execute: () => {
                const id = notebooks.currentWidget && notebooks.currentWidget.id;
                if (id) {
                    return app.commands.execute(CommandIDs.select, { id });
                }
            }
        });
        // Set enter key for notebook completer select command.
        app.commands.addKeyBinding({
            command: CommandIDs.selectNotebook,
            keys: ['Enter'],
            selector: `.jp-Notebook .jp-mod-completer-active`
        });
    }
};
/**
 * An extension that registers file editors for completion.
 */
const files = {
    id: '@jupyterlab/completer-extension:files',
    requires: [_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionManager, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorTracker],
    autoStart: true,
    activate: (app, manager, editorTracker) => {
        // Keep a list of active ISessions so that we can
        // clean them up when they are no longer needed.
        const activeSessions = {};
        // When a new file editor is created, make the completer for it.
        editorTracker.widgetAdded.connect((sender, widget) => {
            const sessions = app.serviceManager.sessions;
            const editor = widget.content.editor;
            const contextConnector = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ContextConnector({ editor });
            // Initially create the handler with the contextConnector.
            // If a kernel session is found matching this file editor,
            // it will be replaced in onRunningChanged().
            const handler = manager.register({
                connector: contextConnector,
                editor,
                parent: widget
            });
            // When the list of running sessions changes,
            // check to see if there are any kernels with a
            // matching path for this file editor.
            const onRunningChanged = (sender, models) => {
                const oldSession = activeSessions[widget.id];
                // Search for a matching path.
                const model = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.find)(models, m => m.path === widget.context.path);
                if (model) {
                    // If there is a matching path, but it is the same
                    // session as we previously had, do nothing.
                    if (oldSession && oldSession.id === model.id) {
                        return;
                    }
                    // Otherwise, dispose of the old session and reset to
                    // a new CompletionConnector.
                    if (oldSession) {
                        delete activeSessions[widget.id];
                        oldSession.dispose();
                    }
                    const session = sessions.connectTo({ model });
                    handler.connector = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.CompletionConnector({ session, editor });
                    activeSessions[widget.id] = session;
                }
                else {
                    // If we didn't find a match, make sure
                    // the connector is the contextConnector and
                    // dispose of any previous connection.
                    handler.connector = contextConnector;
                    if (oldSession) {
                        delete activeSessions[widget.id];
                        oldSession.dispose();
                    }
                }
            };
            onRunningChanged(sessions, (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.toArray)(sessions.running()));
            sessions.runningChanged.connect(onRunningChanged);
            // When the widget is disposed, do some cleanup.
            widget.disposed.connect(() => {
                sessions.runningChanged.disconnect(onRunningChanged);
                const session = activeSessions[widget.id];
                if (session) {
                    delete activeSessions[widget.id];
                    session.dispose();
                }
            });
        });
        // Add console completer invoke command.
        app.commands.addCommand(CommandIDs.invokeFile, {
            execute: () => {
                const id = editorTracker.currentWidget && editorTracker.currentWidget.id;
                if (id) {
                    return app.commands.execute(CommandIDs.invoke, { id });
                }
            }
        });
        // Add console completer select command.
        app.commands.addCommand(CommandIDs.selectFile, {
            execute: () => {
                const id = editorTracker.currentWidget && editorTracker.currentWidget.id;
                if (id) {
                    return app.commands.execute(CommandIDs.select, { id });
                }
            }
        });
        // Set enter key for console completer select command.
        app.commands.addKeyBinding({
            command: CommandIDs.selectFile,
            keys: ['Enter'],
            selector: `.jp-FileEditor .jp-mod-completer-active`
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    manager,
    consoles,
    notebooks,
    files
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29tcGxldGVyLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBYTRCO0FBQ3VCO0FBQ0U7QUFDQTtBQUVOO0FBQ1Q7QUFFekM7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FnQm5CO0FBaEJELFdBQVUsVUFBVTtJQUNMLGlCQUFNLEdBQUcsa0JBQWtCLENBQUM7SUFFNUIsd0JBQWEsR0FBRywwQkFBMEIsQ0FBQztJQUUzQyx5QkFBYyxHQUFHLDJCQUEyQixDQUFDO0lBRTdDLHFCQUFVLEdBQUcsdUJBQXVCLENBQUM7SUFFckMsaUJBQU0sR0FBRyxrQkFBa0IsQ0FBQztJQUU1Qix3QkFBYSxHQUFHLDBCQUEwQixDQUFDO0lBRTNDLHlCQUFjLEdBQUcsMkJBQTJCLENBQUM7SUFFN0MscUJBQVUsR0FBRyx1QkFBdUIsQ0FBQztBQUNwRCxDQUFDLEVBaEJTLFVBQVUsS0FBVixVQUFVLFFBZ0JuQjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxPQUFPLEdBQThDO0lBQ3pELEVBQUUsRUFBRSx5Q0FBeUM7SUFDN0MsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUscUVBQWtCO0lBQzVCLFFBQVEsRUFBRSxDQUFDLEdBQW9CLEVBQXNCLEVBQUU7UUFDckQsTUFBTSxRQUFRLEdBQXdDLEVBQUUsQ0FBQztRQUV6RCxHQUFHLENBQUMsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsTUFBTSxFQUFFO1lBQ3pDLE9BQU8sRUFBRSxJQUFJLENBQUMsRUFBRTtnQkFDZCxNQUFNLEVBQUUsR0FBRyxJQUFJLElBQUssSUFBSSxDQUFDLElBQUksQ0FBWSxDQUFDO2dCQUMxQyxJQUFJLENBQUMsRUFBRSxFQUFFO29CQUNQLE9BQU87aUJB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QUFDLEVBQUUsQ0FBQztnQkFFaEUsSUFBSSxFQUFFLEVBQUU7b0JBQ04sT0FBTyxHQUFHLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUMsTUFBTSxFQUFFLEVBQUUsRUFBRSxFQUFFLENBQUMsQ0FBQztpQkFDeEQ7WUFDSCxDQUFDO1NBQ0YsQ0FBQyxDQUFDO1FBRUgsd0NBQXdDO1FBQ3hDLEdBQUcsQ0FBQyxRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxVQUFVLEVBQUU7WUFDN0MsT0FBTyxFQUFFLEdBQUcsRUFBRTtnQkFDWixNQUFNLEVBQUUsR0FDTixhQUFhLENBQUMsYUFBYSxJQUFJLGFBQWEsQ0FBQyxhQUFhLENBQUMsRUFBRSxDQUFDO2dCQUVoRSxJQUFJLEVBQUUsRUFBRTtvQkFDTixPQUFPLEdBQUcsQ0FBQyxRQUFRLENBQUMsT0FBTyxDQUFDLFVBQVUsQ0FBQyxNQUFNLEVBQUUsRUFBRSxFQUFFLEVBQUUsQ0FBQyxDQUFDO2lCQUN4RDtZQUNILENBQUM7U0FDRixDQUFDLENBQUM7UUFFSCxzREFBc0Q7UUFDdEQsR0FBRyxDQUFDLFFBQVEsQ0FBQyxhQUFhLENBQUM7WUFDekIsT0FBTyxFQUFFLFVBQVUsQ0FBQyxVQUFVO1lBQzlCLElBQUksRUFBRSxDQUFDLE9BQU8sQ0FBQztZQUNmLFFBQVEsRUFBRSx5Q0FBeUM7U0FDcEQsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztDQUNGLENBQUM7QUFFRjs7R0FFRztBQUNILE1BQU0sT0FBTyxHQUFpQztJQUM1QyxPQUFPO0lBQ1AsUUFBUTtJQUNSLFNBQVM7SUFDVCxLQUFLO0NBQ04sQ0FBQztBQUNGLGlFQUFlLE9BQU8sRUFBQyIsImZpbGUiOiJwYWNrYWdlc19jb21wbGV0ZXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy5mYzZhZjc4MzAyMzZkYTBlZWRiNS5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGNvbXBsZXRlci1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBDb21wbGV0ZXIsXG4gIENvbXBsZXRlck1vZGVsLFxuICBDb21wbGV0aW9uQ29ubmVjdG9yLFxuICBDb21wbGV0aW9uSGFuZGxlcixcbiAgQ29udGV4dENvbm5lY3RvcixcbiAgSUNvbXBsZXRpb25NYW5hZ2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL2NvbXBsZXRlcic7XG5pbXBvcnQgeyBJQ29uc29sZVRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9jb25zb2xlJztcbmltcG9ydCB7IElFZGl0b3JUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZmlsZWVkaXRvcic7XG5pbXBvcnQgeyBJTm90ZWJvb2tUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbm90ZWJvb2snO1xuaW1wb3J0IHsgU2Vzc2lvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IGZpbmQsIHRvQXJyYXkgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBjb21wbGV0ZXIgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBpbnZva2UgPSAnY29tcGxldGVyOmludm9rZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGludm9rZUNvbnNvbGUgPSAnY29tcGxldGVyOmludm9rZS1jb25zb2xlJztcblxuICBleHBvcnQgY29uc3QgaW52b2tlTm90ZWJvb2sgPSAnY29tcGxldGVyOmludm9rZS1ub3RlYm9vayc7XG5cbiAgZXhwb3J0IGNvbnN0IGludm9rZUZpbGUgPSAnY29tcGxldGVyOmludm9rZS1maWxlJztcblxuICBleHBvcnQgY29uc3Qgc2VsZWN0ID0gJ2NvbXBsZXRlcjpzZWxlY3QnO1xuXG4gIGV4cG9ydCBjb25zdCBzZWxlY3RDb25zb2xlID0gJ2NvbXBsZXRlcjpzZWxlY3QtY29uc29sZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNlbGVjdE5vdGVib29rID0gJ2NvbXBsZXRlcjpzZWxlY3Qtbm90ZWJvb2snO1xuXG4gIGV4cG9ydCBjb25zdCBzZWxlY3RGaWxlID0gJ2NvbXBsZXRlcjpzZWxlY3QtZmlsZSc7XG59XG5cbi8qKlxuICogQSBwbHVnaW4gcHJvdmlkaW5nIGNvZGUgY29tcGxldGlvbiBmb3IgZWRpdG9ycy5cbiAqL1xuY29uc3QgbWFuYWdlcjogSnVweXRlckZyb250RW5kUGx1Z2luPElDb21wbGV0aW9uTWFuYWdlcj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvY29tcGxldGVyLWV4dGVuc2lvbjptYW5hZ2VyJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSUNvbXBsZXRpb25NYW5hZ2VyLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kKTogSUNvbXBsZXRpb25NYW5hZ2VyID0+IHtcbiAgICBjb25zdCBoYW5kbGVyczogeyBbaWQ6IHN0cmluZ106IENvbXBsZXRpb25IYW5kbGVyIH0gPSB7fTtcblxuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaW52b2tlLCB7XG4gICAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgaWQgPSBhcmdzICYmIChhcmdzWydpZCddIGFzIHN0cmluZyk7XG4gICAgICAgIGlmICghaWQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBoYW5kbGVyID0gaGFuZGxlcnNbaWRdO1xuICAgICAgICBpZiAoaGFuZGxlcikge1xuICAgICAgICAgIGhhbmRsZXIuaW52b2tlKCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2VsZWN0LCB7XG4gICAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgaWQgPSBhcmdzICYmIChhcmdzWydpZCddIGFzIHN0cmluZyk7XG4gICAgICAgIGlmICghaWQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBoYW5kbGVyID0gaGFuZGxlcnNbaWRdO1xuICAgICAgICBpZiAoaGFuZGxlcikge1xuICAgICAgICAgIGhhbmRsZXIuY29tcGxldGVyLnNlbGVjdEFjdGl2ZSgpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICByZXR1cm4ge1xuICAgICAgcmVnaXN0ZXI6IChcbiAgICAgICAgY29tcGxldGFibGU6IElDb21wbGV0aW9uTWFuYWdlci5JQ29tcGxldGFibGUsXG4gICAgICAgIHJlbmRlcmVyOiBDb21wbGV0ZXIuSVJlbmRlcmVyID0gQ29tcGxldGVyLmRlZmF1bHRSZW5kZXJlclxuICAgICAgKTogSUNvbXBsZXRpb25NYW5hZ2VyLklDb21wbGV0YWJsZUF0dHJpYnV0ZXMgPT4ge1xuICAgICAgICBjb25zdCB7IGNvbm5lY3RvciwgZWRpdG9yLCBwYXJlbnQgfSA9IGNvbXBsZXRhYmxlO1xuICAgICAgICBjb25zdCBtb2RlbCA9IG5ldyBDb21wbGV0ZXJNb2RlbCgpO1xuICAgICAgICBjb25zdCBjb21wbGV0ZXIgPSBuZXcgQ29tcGxldGVyKHsgZWRpdG9yLCBtb2RlbCwgcmVuZGVyZXIgfSk7XG4gICAgICAgIGNvbnN0IGhhbmRsZXIgPSBuZXcgQ29tcGxldGlvbkhhbmRsZXIoe1xuICAgICAgICAgIGNvbXBsZXRlcixcbiAgICAgICAgICBjb25uZWN0b3JcbiAgICAgICAgfSk7XG4gICAgICAgIGNvbnN0IGlkID0gcGFyZW50LmlkO1xuXG4gICAgICAgIC8vIEhpZGUgdGhlIHdpZGdldCB3aGVuIGl0IGZpcnN0IGxvYWRzLlxuICAgICAgICBjb21wbGV0ZXIuaGlkZSgpO1xuXG4gICAgICAgIC8vIEFzc29jaWF0ZSB0aGUgaGFuZGxlciB3aXRoIHRoZSBwYXJlbnQgd2lkZ2V0LlxuICAgICAgICBoYW5kbGVyc1tpZF0gPSBoYW5kbGVyO1xuXG4gICAgICAgIC8vIFNldCB0aGUgaGFuZGxlcidzIGVkaXRvci5cbiAgICAgICAgaGFuZGxlci5lZGl0b3IgPSBlZGl0b3I7XG5cbiAgICAgICAgLy8gQXR0YWNoIHRoZSBjb21wbGV0ZXIgd2lkZ2V0LlxuICAgICAgICBXaWRnZXQuYXR0YWNoKGNvbXBsZXRlciwgZG9jdW1lbnQuYm9keSk7XG5cbiAgICAgICAgLy8gTGlzdGVuIGZvciBwYXJlbnQgZGlzcG9zYWwuXG4gICAgICAgIHBhcmVudC5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgICBkZWxldGUgaGFuZGxlcnNbaWRdO1xuICAgICAgICAgIG1vZGVsLmRpc3Bvc2UoKTtcbiAgICAgICAgICBjb21wbGV0ZXIuZGlzcG9zZSgpO1xuICAgICAgICAgIGhhbmRsZXIuZGlzcG9zZSgpO1xuICAgICAgICB9KTtcblxuICAgICAgICByZXR1cm4gaGFuZGxlcjtcbiAgICAgIH1cbiAgICB9O1xuICB9XG59O1xuXG4vKipcbiAqIEFuIGV4dGVuc2lvbiB0aGF0IHJlZ2lzdGVycyBjb25zb2xlcyBmb3IgY29kZSBjb21wbGV0aW9uLlxuICovXG5jb25zdCBjb25zb2xlczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvbXBsZXRlci1leHRlbnNpb246Y29uc29sZXMnLFxuICByZXF1aXJlczogW0lDb21wbGV0aW9uTWFuYWdlciwgSUNvbnNvbGVUcmFja2VyXSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElDb21wbGV0aW9uTWFuYWdlcixcbiAgICBjb25zb2xlczogSUNvbnNvbGVUcmFja2VyXG4gICk6IHZvaWQgPT4ge1xuICAgIC8vIENyZWF0ZSBhIGhhbmRsZXIgZm9yIGVhY2ggY29uc29sZSB0aGF0IGlzIGNyZWF0ZWQuXG4gICAgY29uc29sZXMud2lkZ2V0QWRkZWQuY29ubmVjdCgoc2VuZGVyLCB3aWRnZXQpID0+IHtcbiAgICAgIGNvbnN0IGFuY2hvciA9IHdpZGdldC5jb25zb2xlO1xuICAgICAgY29uc3QgZWRpdG9yID0gYW5jaG9yLnByb21wdENlbGw/LmVkaXRvciA/PyBudWxsO1xuICAgICAgY29uc3Qgc2Vzc2lvbiA9IGFuY2hvci5zZXNzaW9uQ29udGV4dC5zZXNzaW9uO1xuICAgICAgLy8gVE9ETzogQ29tcGxldGlvbkNvbm5lY3RvciBhc3N1bWVzIGVkaXRvciBhbmQgc2Vzc2lvbiBhcmUgbm90IG51bGxcbiAgICAgIGNvbnN0IGNvbm5lY3RvciA9IG5ldyBDb21wbGV0aW9uQ29ubmVjdG9yKHsgc2Vzc2lvbiwgZWRpdG9yIH0pO1xuICAgICAgY29uc3QgaGFuZGxlciA9IG1hbmFnZXIucmVnaXN0ZXIoeyBjb25uZWN0b3IsIGVkaXRvciwgcGFyZW50OiB3aWRnZXQgfSk7XG5cbiAgICAgIGNvbnN0IHVwZGF0ZUNvbm5lY3RvciA9ICgpID0+IHtcbiAgICAgICAgY29uc3QgZWRpdG9yID0gYW5jaG9yLnByb21wdENlbGw/LmVkaXRvciA/PyBudWxsO1xuICAgICAgICBjb25zdCBzZXNzaW9uID0gYW5jaG9yLnNlc3Npb25Db250ZXh0LnNlc3Npb247XG5cbiAgICAgICAgaGFuZGxlci5lZGl0b3IgPSBlZGl0b3I7XG4gICAgICAgIC8vIFRPRE86IENvbXBsZXRpb25Db25uZWN0b3IgYXNzdW1lcyBlZGl0b3IgYW5kIHNlc3Npb24gYXJlIG5vdCBudWxsXG4gICAgICAgIGhhbmRsZXIuY29ubmVjdG9yID0gbmV3IENvbXBsZXRpb25Db25uZWN0b3IoeyBzZXNzaW9uLCBlZGl0b3IgfSk7XG4gICAgICB9O1xuXG4gICAgICAvLyBVcGRhdGUgdGhlIGhhbmRsZXIgd2hlbmV2ZXIgdGhlIHByb21wdCBvciBzZXNzaW9uIGNoYW5nZXNcbiAgICAgIGFuY2hvci5wcm9tcHRDZWxsQ3JlYXRlZC5jb25uZWN0KHVwZGF0ZUNvbm5lY3Rvcik7XG4gICAgICBhbmNob3Iuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbkNoYW5nZWQuY29ubmVjdCh1cGRhdGVDb25uZWN0b3IpO1xuICAgIH0pO1xuXG4gICAgLy8gQWRkIGNvbnNvbGUgY29tcGxldGVyIGludm9rZSBjb21tYW5kLlxuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaW52b2tlQ29uc29sZSwge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCBpZCA9IGNvbnNvbGVzLmN1cnJlbnRXaWRnZXQgJiYgY29uc29sZXMuY3VycmVudFdpZGdldC5pZDtcblxuICAgICAgICBpZiAoaWQpIHtcbiAgICAgICAgICByZXR1cm4gYXBwLmNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5pbnZva2UsIHsgaWQgfSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIC8vIEFkZCBjb25zb2xlIGNvbXBsZXRlciBzZWxlY3QgY29tbWFuZC5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNlbGVjdENvbnNvbGUsIHtcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgY29uc3QgaWQgPSBjb25zb2xlcy5jdXJyZW50V2lkZ2V0ICYmIGNvbnNvbGVzLmN1cnJlbnRXaWRnZXQuaWQ7XG5cbiAgICAgICAgaWYgKGlkKSB7XG4gICAgICAgICAgcmV0dXJuIGFwcC5jb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMuc2VsZWN0LCB7IGlkIH0pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBTZXQgZW50ZXIga2V5IGZvciBjb25zb2xlIGNvbXBsZXRlciBzZWxlY3QgY29tbWFuZC5cbiAgICBhcHAuY29tbWFuZHMuYWRkS2V5QmluZGluZyh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLnNlbGVjdENvbnNvbGUsXG4gICAgICBrZXlzOiBbJ0VudGVyJ10sXG4gICAgICBzZWxlY3RvcjogYC5qcC1Db25zb2xlUGFuZWwgLmpwLW1vZC1jb21wbGV0ZXItYWN0aXZlYFxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIEFuIGV4dGVuc2lvbiB0aGF0IHJlZ2lzdGVycyBub3RlYm9va3MgZm9yIGNvZGUgY29tcGxldGlvbi5cbiAqL1xuY29uc3Qgbm90ZWJvb2tzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvY29tcGxldGVyLWV4dGVuc2lvbjpub3RlYm9va3MnLFxuICByZXF1aXJlczogW0lDb21wbGV0aW9uTWFuYWdlciwgSU5vdGVib29rVHJhY2tlcl0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBtYW5hZ2VyOiBJQ29tcGxldGlvbk1hbmFnZXIsXG4gICAgbm90ZWJvb2tzOiBJTm90ZWJvb2tUcmFja2VyXG4gICk6IHZvaWQgPT4ge1xuICAgIC8vIENyZWF0ZSBhIGhhbmRsZXIgZm9yIGVhY2ggbm90ZWJvb2sgdGhhdCBpcyBjcmVhdGVkLlxuICAgIG5vdGVib29rcy53aWRnZXRBZGRlZC5jb25uZWN0KChzZW5kZXIsIHBhbmVsKSA9PiB7XG4gICAgICBjb25zdCBlZGl0b3IgPSBwYW5lbC5jb250ZW50LmFjdGl2ZUNlbGw/LmVkaXRvciA/PyBudWxsO1xuICAgICAgY29uc3Qgc2Vzc2lvbiA9IHBhbmVsLnNlc3Npb25Db250ZXh0LnNlc3Npb247XG4gICAgICAvLyBUT0RPOiBDb21wbGV0aW9uQ29ubmVjdG9yIGFzc3VtZXMgZWRpdG9yIGFuZCBzZXNzaW9uIGFyZSBub3QgbnVsbFxuICAgICAgY29uc3QgY29ubmVjdG9yID0gbmV3IENvbXBsZXRpb25Db25uZWN0b3IoeyBzZXNzaW9uLCBlZGl0b3IgfSk7XG4gICAgICBjb25zdCBoYW5kbGVyID0gbWFuYWdlci5yZWdpc3Rlcih7IGNvbm5lY3RvciwgZWRpdG9yLCBwYXJlbnQ6IHBhbmVsIH0pO1xuXG4gICAgICBjb25zdCB1cGRhdGVDb25uZWN0b3IgPSAoKSA9PiB7XG4gICAgICAgIGNvbnN0IGVkaXRvciA9IHBhbmVsLmNvbnRlbnQuYWN0aXZlQ2VsbD8uZWRpdG9yID8/IG51bGw7XG4gICAgICAgIGNvbnN0IHNlc3Npb24gPSBwYW5lbC5zZXNzaW9uQ29udGV4dC5zZXNzaW9uO1xuXG4gICAgICAgIGhhbmRsZXIuZWRpdG9yID0gZWRpdG9yO1xuICAgICAgICAvLyBUT0RPOiBDb21wbGV0aW9uQ29ubmVjdG9yIGFzc3VtZXMgZWRpdG9yIGFuZCBzZXNzaW9uIGFyZSBub3QgbnVsbFxuICAgICAgICBoYW5kbGVyLmNvbm5lY3RvciA9IG5ldyBDb21wbGV0aW9uQ29ubmVjdG9yKHsgc2Vzc2lvbiwgZWRpdG9yIH0pO1xuICAgICAgfTtcblxuICAgICAgLy8gVXBkYXRlIHRoZSBoYW5kbGVyIHdoZW5ldmVyIHRoZSBwcm9tcHQgb3Igc2Vzc2lvbiBjaGFuZ2VzXG4gICAgICBwYW5lbC5jb250ZW50LmFjdGl2ZUNlbGxDaGFuZ2VkLmNvbm5lY3QodXBkYXRlQ29ubmVjdG9yKTtcbiAgICAgIHBhbmVsLnNlc3Npb25Db250ZXh0LnNlc3Npb25DaGFuZ2VkLmNvbm5lY3QodXBkYXRlQ29ubmVjdG9yKTtcbiAgICB9KTtcblxuICAgIC8vIEFkZCBub3RlYm9vayBjb21wbGV0ZXIgY29tbWFuZC5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmludm9rZU5vdGVib29rLCB7XG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHBhbmVsID0gbm90ZWJvb2tzLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIGlmIChwYW5lbCAmJiBwYW5lbC5jb250ZW50LmFjdGl2ZUNlbGw/Lm1vZGVsLnR5cGUgPT09ICdjb2RlJykge1xuICAgICAgICAgIHJldHVybiBhcHAuY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLmludm9rZSwgeyBpZDogcGFuZWwuaWQgfSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIC8vIEFkZCBub3RlYm9vayBjb21wbGV0ZXIgc2VsZWN0IGNvbW1hbmQuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zZWxlY3ROb3RlYm9vaywge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCBpZCA9IG5vdGVib29rcy5jdXJyZW50V2lkZ2V0ICYmIG5vdGVib29rcy5jdXJyZW50V2lkZ2V0LmlkO1xuXG4gICAgICAgIGlmIChpZCkge1xuICAgICAgICAgIHJldHVybiBhcHAuY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLnNlbGVjdCwgeyBpZCB9KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gU2V0IGVudGVyIGtleSBmb3Igbm90ZWJvb2sgY29tcGxldGVyIHNlbGVjdCBjb21tYW5kLlxuICAgIGFwcC5jb21tYW5kcy5hZGRLZXlCaW5kaW5nKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuc2VsZWN0Tm90ZWJvb2ssXG4gICAgICBrZXlzOiBbJ0VudGVyJ10sXG4gICAgICBzZWxlY3RvcjogYC5qcC1Ob3RlYm9vayAuanAtbW9kLWNvbXBsZXRlci1hY3RpdmVgXG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogQW4gZXh0ZW5zaW9uIHRoYXQgcmVnaXN0ZXJzIGZpbGUgZWRpdG9ycyBmb3IgY29tcGxldGlvbi5cbiAqL1xuY29uc3QgZmlsZXM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9jb21wbGV0ZXItZXh0ZW5zaW9uOmZpbGVzJyxcbiAgcmVxdWlyZXM6IFtJQ29tcGxldGlvbk1hbmFnZXIsIElFZGl0b3JUcmFja2VyXSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElDb21wbGV0aW9uTWFuYWdlcixcbiAgICBlZGl0b3JUcmFja2VyOiBJRWRpdG9yVHJhY2tlclxuICApOiB2b2lkID0+IHtcbiAgICAvLyBLZWVwIGEgbGlzdCBvZiBhY3RpdmUgSVNlc3Npb25zIHNvIHRoYXQgd2UgY2FuXG4gICAgLy8gY2xlYW4gdGhlbSB1cCB3aGVuIHRoZXkgYXJlIG5vIGxvbmdlciBuZWVkZWQuXG4gICAgY29uc3QgYWN0aXZlU2Vzc2lvbnM6IHtcbiAgICAgIFtpZDogc3RyaW5nXTogU2Vzc2lvbi5JU2Vzc2lvbkNvbm5lY3Rpb247XG4gICAgfSA9IHt9O1xuXG4gICAgLy8gV2hlbiBhIG5ldyBmaWxlIGVkaXRvciBpcyBjcmVhdGVkLCBtYWtlIHRoZSBjb21wbGV0ZXIgZm9yIGl0LlxuICAgIGVkaXRvclRyYWNrZXIud2lkZ2V0QWRkZWQuY29ubmVjdCgoc2VuZGVyLCB3aWRnZXQpID0+IHtcbiAgICAgIGNvbnN0IHNlc3Npb25zID0gYXBwLnNlcnZpY2VNYW5hZ2VyLnNlc3Npb25zO1xuICAgICAgY29uc3QgZWRpdG9yID0gd2lkZ2V0LmNvbnRlbnQuZWRpdG9yO1xuICAgICAgY29uc3QgY29udGV4dENvbm5lY3RvciA9IG5ldyBDb250ZXh0Q29ubmVjdG9yKHsgZWRpdG9yIH0pO1xuXG4gICAgICAvLyBJbml0aWFsbHkgY3JlYXRlIHRoZSBoYW5kbGVyIHdpdGggdGhlIGNvbnRleHRDb25uZWN0b3IuXG4gICAgICAvLyBJZiBhIGtlcm5lbCBzZXNzaW9uIGlzIGZvdW5kIG1hdGNoaW5nIHRoaXMgZmlsZSBlZGl0b3IsXG4gICAgICAvLyBpdCB3aWxsIGJlIHJlcGxhY2VkIGluIG9uUnVubmluZ0NoYW5nZWQoKS5cbiAgICAgIGNvbnN0IGhhbmRsZXIgPSBtYW5hZ2VyLnJlZ2lzdGVyKHtcbiAgICAgICAgY29ubmVjdG9yOiBjb250ZXh0Q29ubmVjdG9yLFxuICAgICAgICBlZGl0b3IsXG4gICAgICAgIHBhcmVudDogd2lkZ2V0XG4gICAgICB9KTtcblxuICAgICAgLy8gV2hlbiB0aGUgbGlzdCBvZiBydW5uaW5nIHNlc3Npb25zIGNoYW5nZXMsXG4gICAgICAvLyBjaGVjayB0byBzZWUgaWYgdGhlcmUgYXJlIGFueSBrZXJuZWxzIHdpdGggYVxuICAgICAgLy8gbWF0Y2hpbmcgcGF0aCBmb3IgdGhpcyBmaWxlIGVkaXRvci5cbiAgICAgIGNvbnN0IG9uUnVubmluZ0NoYW5nZWQgPSAoXG4gICAgICAgIHNlbmRlcjogU2Vzc2lvbi5JTWFuYWdlcixcbiAgICAgICAgbW9kZWxzOiBTZXNzaW9uLklNb2RlbFtdXG4gICAgICApID0+IHtcbiAgICAgICAgY29uc3Qgb2xkU2Vzc2lvbiA9IGFjdGl2ZVNlc3Npb25zW3dpZGdldC5pZF07XG4gICAgICAgIC8vIFNlYXJjaCBmb3IgYSBtYXRjaGluZyBwYXRoLlxuICAgICAgICBjb25zdCBtb2RlbCA9IGZpbmQobW9kZWxzLCBtID0+IG0ucGF0aCA9PT0gd2lkZ2V0LmNvbnRleHQucGF0aCk7XG4gICAgICAgIGlmIChtb2RlbCkge1xuICAgICAgICAgIC8vIElmIHRoZXJlIGlzIGEgbWF0Y2hpbmcgcGF0aCwgYnV0IGl0IGlzIHRoZSBzYW1lXG4gICAgICAgICAgLy8gc2Vzc2lvbiBhcyB3ZSBwcmV2aW91c2x5IGhhZCwgZG8gbm90aGluZy5cbiAgICAgICAgICBpZiAob2xkU2Vzc2lvbiAmJiBvbGRTZXNzaW9uLmlkID09PSBtb2RlbC5pZCkge1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgIH1cbiAgICAgICAgICAvLyBPdGhlcndpc2UsIGRpc3Bvc2Ugb2YgdGhlIG9sZCBzZXNzaW9uIGFuZCByZXNldCB0b1xuICAgICAgICAgIC8vIGEgbmV3IENvbXBsZXRpb25Db25uZWN0b3IuXG4gICAgICAgICAgaWYgKG9sZFNlc3Npb24pIHtcbiAgICAgICAgICAgIGRlbGV0ZSBhY3RpdmVTZXNzaW9uc1t3aWRnZXQuaWRdO1xuICAgICAgICAgICAgb2xkU2Vzc2lvbi5kaXNwb3NlKCk7XG4gICAgICAgICAgfVxuICAgICAgICAgIGNvbnN0IHNlc3Npb24gPSBzZXNzaW9ucy5jb25uZWN0VG8oeyBtb2RlbCB9KTtcbiAgICAgICAgICBoYW5kbGVyLmNvbm5lY3RvciA9IG5ldyBDb21wbGV0aW9uQ29ubmVjdG9yKHsgc2Vzc2lvbiwgZWRpdG9yIH0pO1xuICAgICAgICAgIGFjdGl2ZVNlc3Npb25zW3dpZGdldC5pZF0gPSBzZXNzaW9uO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIC8vIElmIHdlIGRpZG4ndCBmaW5kIGEgbWF0Y2gsIG1ha2Ugc3VyZVxuICAgICAgICAgIC8vIHRoZSBjb25uZWN0b3IgaXMgdGhlIGNvbnRleHRDb25uZWN0b3IgYW5kXG4gICAgICAgICAgLy8gZGlzcG9zZSBvZiBhbnkgcHJldmlvdXMgY29ubmVjdGlvbi5cbiAgICAgICAgICBoYW5kbGVyLmNvbm5lY3RvciA9IGNvbnRleHRDb25uZWN0b3I7XG4gICAgICAgICAgaWYgKG9sZFNlc3Npb24pIHtcbiAgICAgICAgICAgIGRlbGV0ZSBhY3RpdmVTZXNzaW9uc1t3aWRnZXQuaWRdO1xuICAgICAgICAgICAgb2xkU2Vzc2lvbi5kaXNwb3NlKCk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9O1xuICAgICAgb25SdW5uaW5nQ2hhbmdlZChzZXNzaW9ucywgdG9BcnJheShzZXNzaW9ucy5ydW5uaW5nKCkpKTtcbiAgICAgIHNlc3Npb25zLnJ1bm5pbmdDaGFuZ2VkLmNvbm5lY3Qob25SdW5uaW5nQ2hhbmdlZCk7XG5cbiAgICAgIC8vIFdoZW4gdGhlIHdpZGdldCBpcyBkaXNwb3NlZCwgZG8gc29tZSBjbGVhbnVwLlxuICAgICAgd2lkZ2V0LmRpc3Bvc2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICBzZXNzaW9ucy5ydW5uaW5nQ2hhbmdlZC5kaXNjb25uZWN0KG9uUnVubmluZ0NoYW5nZWQpO1xuICAgICAgICBjb25zdCBzZXNzaW9uID0gYWN0aXZlU2Vzc2lvbnNbd2lkZ2V0LmlkXTtcbiAgICAgICAgaWYgKHNlc3Npb24pIHtcbiAgICAgICAgICBkZWxldGUgYWN0aXZlU2Vzc2lvbnNbd2lkZ2V0LmlkXTtcbiAgICAgICAgICBzZXNzaW9uLmRpc3Bvc2UoKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfSk7XG5cbiAgICAvLyBBZGQgY29uc29sZSBjb21wbGV0ZXIgaW52b2tlIGNvbW1hbmQuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5pbnZva2VGaWxlLCB7XG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGNvbnN0IGlkID1cbiAgICAgICAgICBlZGl0b3JUcmFja2VyLmN1cnJlbnRXaWRnZXQgJiYgZWRpdG9yVHJhY2tlci5jdXJyZW50V2lkZ2V0LmlkO1xuXG4gICAgICAgIGlmIChpZCkge1xuICAgICAgICAgIHJldHVybiBhcHAuY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLmludm9rZSwgeyBpZCB9KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gQWRkIGNvbnNvbGUgY29tcGxldGVyIHNlbGVjdCBjb21tYW5kLlxuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2VsZWN0RmlsZSwge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCBpZCA9XG4gICAgICAgICAgZWRpdG9yVHJhY2tlci5jdXJyZW50V2lkZ2V0ICYmIGVkaXRvclRyYWNrZXIuY3VycmVudFdpZGdldC5pZDtcblxuICAgICAgICBpZiAoaWQpIHtcbiAgICAgICAgICByZXR1cm4gYXBwLmNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5zZWxlY3QsIHsgaWQgfSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIC8vIFNldCBlbnRlciBrZXkgZm9yIGNvbnNvbGUgY29tcGxldGVyIHNlbGVjdCBjb21tYW5kLlxuICAgIGFwcC5jb21tYW5kcy5hZGRLZXlCaW5kaW5nKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuc2VsZWN0RmlsZSxcbiAgICAgIGtleXM6IFsnRW50ZXInXSxcbiAgICAgIHNlbGVjdG9yOiBgLmpwLUZpbGVFZGl0b3IgLmpwLW1vZC1jb21wbGV0ZXItYWN0aXZlYFxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2lucyBhcyBkZWZhdWx0LlxuICovXG5jb25zdCBwbHVnaW5zOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48YW55PltdID0gW1xuICBtYW5hZ2VyLFxuICBjb25zb2xlcyxcbiAgbm90ZWJvb2tzLFxuICBmaWxlc1xuXTtcbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG4iXSwic291cmNlUm9vdCI6IiJ9