(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_tooltip-extension_lib_index_js-_d8641"],{

/***/ "../packages/tooltip-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../packages/tooltip-extension/lib/index.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/tooltip */ "webpack/sharing/consume/default/@jupyterlab/tooltip/@jupyterlab/tooltip");
/* harmony import */ var _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module tooltip-extension
 */








/**
 * The command IDs used by the tooltip plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.dismiss = 'tooltip:dismiss';
    CommandIDs.launchConsole = 'tooltip:launch-console';
    CommandIDs.launchNotebook = 'tooltip:launch-notebook';
    CommandIDs.launchFile = 'tooltip:launch-file';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main tooltip manager plugin.
 */
const manager = {
    id: '@jupyterlab/tooltip-extension:manager',
    autoStart: true,
    provides: _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager,
    activate: (app) => {
        let tooltip = null;
        // Add tooltip dismiss command.
        app.commands.addCommand(CommandIDs.dismiss, {
            execute: () => {
                if (tooltip) {
                    tooltip.dispose();
                    tooltip = null;
                }
            }
        });
        return {
            invoke(options) {
                const detail = 0;
                const { anchor, editor, kernel, rendermime } = options;
                if (tooltip) {
                    tooltip.dispose();
                    tooltip = null;
                }
                return Private.fetch({ detail, editor, kernel })
                    .then(bundle => {
                    tooltip = new _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.Tooltip({ anchor, bundle, editor, rendermime });
                    _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__.Widget.attach(tooltip, document.body);
                })
                    .catch(() => {
                    /* Fails silently. */
                });
            }
        };
    }
};
/**
 * The console tooltip plugin.
 */
const consoles = {
    id: '@jupyterlab/tooltip-extension:consoles',
    autoStart: true,
    requires: [_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__.IConsoleTracker],
    activate: (app, manager, consoles) => {
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchConsole, {
            execute: () => {
                var _a, _b;
                const parent = consoles.currentWidget;
                if (!parent) {
                    return;
                }
                const anchor = parent.console;
                const editor = (_a = anchor.promptCell) === null || _a === void 0 ? void 0 : _a.editor;
                const kernel = (_b = anchor.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel;
                const rendermime = anchor.rendermime;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor, editor, kernel, rendermime });
                }
            }
        });
    }
};
/**
 * The notebook tooltip plugin.
 */
const notebooks = {
    id: '@jupyterlab/tooltip-extension:notebooks',
    autoStart: true,
    requires: [_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker],
    activate: (app, manager, notebooks) => {
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchNotebook, {
            execute: () => {
                var _a, _b;
                const parent = notebooks.currentWidget;
                if (!parent) {
                    return;
                }
                const anchor = parent.content;
                const editor = (_a = anchor.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                const kernel = (_b = parent.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel;
                const rendermime = anchor.rendermime;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor, editor, kernel, rendermime });
                }
            }
        });
    }
};
/**
 * The file editor tooltip plugin.
 */
const files = {
    id: '@jupyterlab/tooltip-extension:files',
    autoStart: true,
    requires: [_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorTracker, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry],
    activate: (app, manager, editorTracker, rendermime) => {
        // Keep a list of active ISessions so that we can
        // clean them up when they are no longer needed.
        const activeSessions = {};
        const sessions = app.serviceManager.sessions;
        // When the list of running sessions changes,
        // check to see if there are any kernels with a
        // matching path for the file editors.
        const onRunningChanged = (sender, models) => {
            editorTracker.forEach(file => {
                const model = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__.find)(models, m => file.context.path === m.path);
                if (model) {
                    const oldSession = activeSessions[file.id];
                    // If there is a matching path, but it is the same
                    // session as we previously had, do nothing.
                    if (oldSession && oldSession.id === model.id) {
                        return;
                    }
                    // Otherwise, dispose of the old session and reset to
                    // a new CompletionConnector.
                    if (oldSession) {
                        delete activeSessions[file.id];
                        oldSession.dispose();
                    }
                    const session = sessions.connectTo({ model });
                    activeSessions[file.id] = session;
                }
                else {
                    const session = activeSessions[file.id];
                    if (session) {
                        session.dispose();
                        delete activeSessions[file.id];
                    }
                }
            });
        };
        onRunningChanged(sessions, (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__.toArray)(sessions.running()));
        sessions.runningChanged.connect(onRunningChanged);
        // Clean up after a widget when it is disposed
        editorTracker.widgetAdded.connect((sender, widget) => {
            widget.disposed.connect(w => {
                const session = activeSessions[w.id];
                if (session) {
                    session.dispose();
                    delete activeSessions[w.id];
                }
            });
        });
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchFile, {
            execute: async () => {
                const parent = editorTracker.currentWidget;
                const kernel = parent &&
                    activeSessions[parent.id] &&
                    activeSessions[parent.id].kernel;
                if (!kernel) {
                    return;
                }
                const anchor = parent.content;
                const editor = anchor === null || anchor === void 0 ? void 0 : anchor.editor;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor, editor, kernel, rendermime });
                }
            }
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
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * A counter for outstanding requests.
     */
    let pending = 0;
    /**
     * Fetch a tooltip's content from the API server.
     */
    function fetch(options) {
        const { detail, editor, kernel } = options;
        const code = editor.model.value.text;
        const position = editor.getCursorPosition();
        const offset = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.Text.jsIndexToCharIndex(editor.getOffsetAt(position), code);
        // Clear hints if the new text value is empty or kernel is unavailable.
        if (!code || !kernel) {
            return Promise.reject(void 0);
        }
        const contents = {
            code,
            cursor_pos: offset,
            detail_level: detail || 0
        };
        const current = ++pending;
        return kernel.requestInspect(contents).then(msg => {
            const value = msg.content;
            // If a newer request is pending, bail.
            if (current !== pending) {
                return Promise.reject(void 0);
            }
            // If request fails or returns negative results, bail.
            if (value.status !== 'ok' || !value.found) {
                return Promise.reject(void 0);
            }
            return Promise.resolve(value.data);
        });
    }
    Private.fetch = fetch;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdG9vbHRpcC1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFPbUQ7QUFDVDtBQUNXO0FBQ0E7QUFDSztBQUVFO0FBQ2I7QUFFVDtBQUV6Qzs7R0FFRztBQUNILElBQVUsVUFBVSxDQVFuQjtBQVJELFdBQVUsVUFBVTtJQUNMLGtCQUFPLEdBQUcsaUJBQWlCLENBQUM7SUFFNUIsd0JBQWEsR0FBRyx3QkFBd0IsQ0FBQztJQUV6Qyx5QkFBYyxHQUFHLHlCQUF5QixDQUFDO0lBRTNDLHFCQUFVLEdBQUcscUJBQXFCLENBQUM7QUFDbEQsQ0FBQyxFQVJTLFVBQVUsS0FBVixVQUFVLFFBUW5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLE9BQU8sR0FBMkM7SUFDdEQsRUFBRSxFQUFFLHVDQUF1QztJQUMzQyxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxnRUFBZTtJQUN6QixRQUFRLEVBQUUsQ0FBQyxHQUFvQixFQUFtQixFQUFFO1FBQ2xELElBQUksT0FBTyxHQUFtQixJQUFJLENBQUM7UUFFbkMsK0JBQStCO1FBQy9CLEdBQUcsQ0FBQyxRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxPQUFPLEVBQUU7WUFDMUMsT0FBTyxFQUFFLEdBQUcsRUFBRTtnQkFDWixJQUFJLE9BQU8sRUFBRTtvQkFDWCxPQUFPLENBQUMsT0FBTyxFQUFFLENBQUM7b0JBQ2xCLE9BQU8sR0FBRyxJQUFJLENBQUM7aUJBQ2hCO1lBQ0gsQ0FBQztTQUNGLENBQUMsQ0FBQztRQUVILE9BQU87WUFDTCxNQUFNLENBQUMsT0FBaUM7Z0JBQ3RDLE1BQU0sTUFBTSxHQUFVLENBQUMsQ0FBQztnQkFDeEIsTUFBTSxFQUFFLE1BQU0sRUFB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QyxPQUFPLE9BQU8sQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLENBQXdCLENBQUM7YUFDdEQ7WUFFRCxPQUFPLE9BQU8sQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO1FBQ3JDLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQWpDZSxhQUFLLFFBaUNwQjtBQUNILENBQUMsRUFoRVMsT0FBTyxLQUFQLE9BQU8sUUFnRWhCIiwiZmlsZSI6InBhY2thZ2VzX3Rvb2x0aXAtZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy1fZDg2NDEuZjM1MzgzMTNiZDkzMDhlMTU3YTAuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSB0b29sdGlwLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IENvZGVFZGl0b3IgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlZWRpdG9yJztcbmltcG9ydCB7IElDb25zb2xlVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2NvbnNvbGUnO1xuaW1wb3J0IHsgVGV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJRWRpdG9yVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2ZpbGVlZGl0b3InO1xuaW1wb3J0IHsgSU5vdGVib29rVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IEtlcm5lbCwgS2VybmVsTWVzc2FnZSwgU2Vzc2lvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElUb29sdGlwTWFuYWdlciwgVG9vbHRpcCB9IGZyb20gJ0BqdXB5dGVybGFiL3Rvb2x0aXAnO1xuaW1wb3J0IHsgZmluZCwgdG9BcnJheSB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSB0b29sdGlwIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgZGlzbWlzcyA9ICd0b29sdGlwOmRpc21pc3MnO1xuXG4gIGV4cG9ydCBjb25zdCBsYXVuY2hDb25zb2xlID0gJ3Rvb2x0aXA6bGF1bmNoLWNvbnNvbGUnO1xuXG4gIGV4cG9ydCBjb25zdCBsYXVuY2hOb3RlYm9vayA9ICd0b29sdGlwOmxhdW5jaC1ub3RlYm9vayc7XG5cbiAgZXhwb3J0IGNvbnN0IGxhdW5jaEZpbGUgPSAndG9vbHRpcDpsYXVuY2gtZmlsZSc7XG59XG5cbi8qKlxuICogVGhlIG1haW4gdG9vbHRpcCBtYW5hZ2VyIHBsdWdpbi5cbiAqL1xuY29uc3QgbWFuYWdlcjogSnVweXRlckZyb250RW5kUGx1Z2luPElUb29sdGlwTWFuYWdlcj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvdG9vbHRpcC1leHRlbnNpb246bWFuYWdlcicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcHJvdmlkZXM6IElUb29sdGlwTWFuYWdlcixcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZCk6IElUb29sdGlwTWFuYWdlciA9PiB7XG4gICAgbGV0IHRvb2x0aXA6IFRvb2x0aXAgfCBudWxsID0gbnVsbDtcblxuICAgIC8vIEFkZCB0b29sdGlwIGRpc21pc3MgY29tbWFuZC5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmRpc21pc3MsIHtcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgaWYgKHRvb2x0aXApIHtcbiAgICAgICAgICB0b29sdGlwLmRpc3Bvc2UoKTtcbiAgICAgICAgICB0b29sdGlwID0gbnVsbDtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgcmV0dXJuIHtcbiAgICAgIGludm9rZShvcHRpb25zOiBJVG9vbHRpcE1hbmFnZXIuSU9wdGlvbnMpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICAgICAgY29uc3QgZGV0YWlsOiAwIHwgMSA9IDA7XG4gICAgICAgIGNvbnN0IHsgYW5jaG9yLCBlZGl0b3IsIGtlcm5lbCwgcmVuZGVybWltZSB9ID0gb3B0aW9ucztcblxuICAgICAgICBpZiAodG9vbHRpcCkge1xuICAgICAgICAgIHRvb2x0aXAuZGlzcG9zZSgpO1xuICAgICAgICAgIHRvb2x0aXAgPSBudWxsO1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIFByaXZhdGUuZmV0Y2goeyBkZXRhaWwsIGVkaXRvciwga2VybmVsIH0pXG4gICAgICAgICAgLnRoZW4oYnVuZGxlID0+IHtcbiAgICAgICAgICAgIHRvb2x0aXAgPSBuZXcgVG9vbHRpcCh7IGFuY2hvciwgYnVuZGxlLCBlZGl0b3IsIHJlbmRlcm1pbWUgfSk7XG4gICAgICAgICAgICBXaWRnZXQuYXR0YWNoKHRvb2x0aXAsIGRvY3VtZW50LmJvZHkpO1xuICAgICAgICAgIH0pXG4gICAgICAgICAgLmNhdGNoKCgpID0+IHtcbiAgICAgICAgICAgIC8qIEZhaWxzIHNpbGVudGx5LiAqL1xuICAgICAgICAgIH0pO1xuICAgICAgfVxuICAgIH07XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIGNvbnNvbGUgdG9vbHRpcCBwbHVnaW4uXG4gKi9cbmNvbnN0IGNvbnNvbGVzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvdG9vbHRpcC1leHRlbnNpb246Y29uc29sZXMnLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSVRvb2x0aXBNYW5hZ2VyLCBJQ29uc29sZVRyYWNrZXJdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElUb29sdGlwTWFuYWdlcixcbiAgICBjb25zb2xlczogSUNvbnNvbGVUcmFja2VyXG4gICk6IHZvaWQgPT4ge1xuICAgIC8vIEFkZCB0b29sdGlwIGxhdW5jaCBjb21tYW5kLlxuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubGF1bmNoQ29uc29sZSwge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCBwYXJlbnQgPSBjb25zb2xlcy5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICAgIGlmICghcGFyZW50KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgYW5jaG9yID0gcGFyZW50LmNvbnNvbGU7XG4gICAgICAgIGNvbnN0IGVkaXRvciA9IGFuY2hvci5wcm9tcHRDZWxsPy5lZGl0b3I7XG4gICAgICAgIGNvbnN0IGtlcm5lbCA9IGFuY2hvci5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw7XG4gICAgICAgIGNvbnN0IHJlbmRlcm1pbWUgPSBhbmNob3IucmVuZGVybWltZTtcblxuICAgICAgICAvLyBJZiBhbGwgY29tcG9uZW50cyBuZWNlc3NhcnkgZm9yIHJlbmRlcmluZyBleGlzdCwgY3JlYXRlIGEgdG9vbHRpcC5cbiAgICAgICAgaWYgKCEhZWRpdG9yICYmICEha2VybmVsICYmICEhcmVuZGVybWltZSkge1xuICAgICAgICAgIHJldHVybiBtYW5hZ2VyLmludm9rZSh7IGFuY2hvciwgZWRpdG9yLCBrZXJuZWwsIHJlbmRlcm1pbWUgfSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBUaGUgbm90ZWJvb2sgdG9vbHRpcCBwbHVnaW4uXG4gKi9cbmNvbnN0IG5vdGVib29rczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL3Rvb2x0aXAtZXh0ZW5zaW9uOm5vdGVib29rcycsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVG9vbHRpcE1hbmFnZXIsIElOb3RlYm9va1RyYWNrZXJdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElUb29sdGlwTWFuYWdlcixcbiAgICBub3RlYm9va3M6IElOb3RlYm9va1RyYWNrZXJcbiAgKTogdm9pZCA9PiB7XG4gICAgLy8gQWRkIHRvb2x0aXAgbGF1bmNoIGNvbW1hbmQuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5sYXVuY2hOb3RlYm9vaywge1xuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCBwYXJlbnQgPSBub3RlYm9va3MuY3VycmVudFdpZGdldDtcblxuICAgICAgICBpZiAoIXBhcmVudCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGFuY2hvciA9IHBhcmVudC5jb250ZW50O1xuICAgICAgICBjb25zdCBlZGl0b3IgPSBhbmNob3IuYWN0aXZlQ2VsbD8uZWRpdG9yO1xuICAgICAgICBjb25zdCBrZXJuZWwgPSBwYXJlbnQuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbj8ua2VybmVsO1xuICAgICAgICBjb25zdCByZW5kZXJtaW1lID0gYW5jaG9yLnJlbmRlcm1pbWU7XG5cbiAgICAgICAgLy8gSWYgYWxsIGNvbXBvbmVudHMgbmVjZXNzYXJ5IGZvciByZW5kZXJpbmcgZXhpc3QsIGNyZWF0ZSBhIHRvb2x0aXAuXG4gICAgICAgIGlmICghIWVkaXRvciAmJiAhIWtlcm5lbCAmJiAhIXJlbmRlcm1pbWUpIHtcbiAgICAgICAgICByZXR1cm4gbWFuYWdlci5pbnZva2UoeyBhbmNob3IsIGVkaXRvciwga2VybmVsLCByZW5kZXJtaW1lIH0pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIGZpbGUgZWRpdG9yIHRvb2x0aXAgcGx1Z2luLlxuICovXG5jb25zdCBmaWxlczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL3Rvb2x0aXAtZXh0ZW5zaW9uOmZpbGVzJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lUb29sdGlwTWFuYWdlciwgSUVkaXRvclRyYWNrZXIsIElSZW5kZXJNaW1lUmVnaXN0cnldLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElUb29sdGlwTWFuYWdlcixcbiAgICBlZGl0b3JUcmFja2VyOiBJRWRpdG9yVHJhY2tlcixcbiAgICByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5XG4gICk6IHZvaWQgPT4ge1xuICAgIC8vIEtlZXAgYSBsaXN0IG9mIGFjdGl2ZSBJU2Vzc2lvbnMgc28gdGhhdCB3ZSBjYW5cbiAgICAvLyBjbGVhbiB0aGVtIHVwIHdoZW4gdGhleSBhcmUgbm8gbG9uZ2VyIG5lZWRlZC5cbiAgICBjb25zdCBhY3RpdmVTZXNzaW9uczoge1xuICAgICAgW2lkOiBzdHJpbmddOiBTZXNzaW9uLklTZXNzaW9uQ29ubmVjdGlvbjtcbiAgICB9ID0ge307XG5cbiAgICBjb25zdCBzZXNzaW9ucyA9IGFwcC5zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucztcbiAgICAvLyBXaGVuIHRoZSBsaXN0IG9mIHJ1bm5pbmcgc2Vzc2lvbnMgY2hhbmdlcyxcbiAgICAvLyBjaGVjayB0byBzZWUgaWYgdGhlcmUgYXJlIGFueSBrZXJuZWxzIHdpdGggYVxuICAgIC8vIG1hdGNoaW5nIHBhdGggZm9yIHRoZSBmaWxlIGVkaXRvcnMuXG4gICAgY29uc3Qgb25SdW5uaW5nQ2hhbmdlZCA9IChcbiAgICAgIHNlbmRlcjogU2Vzc2lvbi5JTWFuYWdlcixcbiAgICAgIG1vZGVsczogU2Vzc2lvbi5JTW9kZWxbXVxuICAgICkgPT4ge1xuICAgICAgZWRpdG9yVHJhY2tlci5mb3JFYWNoKGZpbGUgPT4ge1xuICAgICAgICBjb25zdCBtb2RlbCA9IGZpbmQobW9kZWxzLCBtID0+IGZpbGUuY29udGV4dC5wYXRoID09PSBtLnBhdGgpO1xuICAgICAgICBpZiAobW9kZWwpIHtcbiAgICAgICAgICBjb25zdCBvbGRTZXNzaW9uID0gYWN0aXZlU2Vzc2lvbnNbZmlsZS5pZF07XG4gICAgICAgICAgLy8gSWYgdGhlcmUgaXMgYSBtYXRjaGluZyBwYXRoLCBidXQgaXQgaXMgdGhlIHNhbWVcbiAgICAgICAgICAvLyBzZXNzaW9uIGFzIHdlIHByZXZpb3VzbHkgaGFkLCBkbyBub3RoaW5nLlxuICAgICAgICAgIGlmIChvbGRTZXNzaW9uICYmIG9sZFNlc3Npb24uaWQgPT09IG1vZGVsLmlkKSB7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgfVxuICAgICAgICAgIC8vIE90aGVyd2lzZSwgZGlzcG9zZSBvZiB0aGUgb2xkIHNlc3Npb24gYW5kIHJlc2V0IHRvXG4gICAgICAgICAgLy8gYSBuZXcgQ29tcGxldGlvbkNvbm5lY3Rvci5cbiAgICAgICAgICBpZiAob2xkU2Vzc2lvbikge1xuICAgICAgICAgICAgZGVsZXRlIGFjdGl2ZVNlc3Npb25zW2ZpbGUuaWRdO1xuICAgICAgICAgICAgb2xkU2Vzc2lvbi5kaXNwb3NlKCk7XG4gICAgICAgICAgfVxuICAgICAgICAgIGNvbnN0IHNlc3Npb24gPSBzZXNzaW9ucy5jb25uZWN0VG8oeyBtb2RlbCB9KTtcbiAgICAgICAgICBhY3RpdmVTZXNzaW9uc1tmaWxlLmlkXSA9IHNlc3Npb247XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgY29uc3Qgc2Vzc2lvbiA9IGFjdGl2ZVNlc3Npb25zW2ZpbGUuaWRdO1xuICAgICAgICAgIGlmIChzZXNzaW9uKSB7XG4gICAgICAgICAgICBzZXNzaW9uLmRpc3Bvc2UoKTtcbiAgICAgICAgICAgIGRlbGV0ZSBhY3RpdmVTZXNzaW9uc1tmaWxlLmlkXTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH07XG4gICAgb25SdW5uaW5nQ2hhbmdlZChzZXNzaW9ucywgdG9BcnJheShzZXNzaW9ucy5ydW5uaW5nKCkpKTtcbiAgICBzZXNzaW9ucy5ydW5uaW5nQ2hhbmdlZC5jb25uZWN0KG9uUnVubmluZ0NoYW5nZWQpO1xuXG4gICAgLy8gQ2xlYW4gdXAgYWZ0ZXIgYSB3aWRnZXQgd2hlbiBpdCBpcyBkaXNwb3NlZFxuICAgIGVkaXRvclRyYWNrZXIud2lkZ2V0QWRkZWQuY29ubmVjdCgoc2VuZGVyLCB3aWRnZXQpID0+IHtcbiAgICAgIHdpZGdldC5kaXNwb3NlZC5jb25uZWN0KHcgPT4ge1xuICAgICAgICBjb25zdCBzZXNzaW9uID0gYWN0aXZlU2Vzc2lvbnNbdy5pZF07XG4gICAgICAgIGlmIChzZXNzaW9uKSB7XG4gICAgICAgICAgc2Vzc2lvbi5kaXNwb3NlKCk7XG4gICAgICAgICAgZGVsZXRlIGFjdGl2ZVNlc3Npb25zW3cuaWRdO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9KTtcblxuICAgIC8vIEFkZCB0b29sdGlwIGxhdW5jaCBjb21tYW5kLlxuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubGF1bmNoRmlsZSwge1xuICAgICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgICBjb25zdCBwYXJlbnQgPSBlZGl0b3JUcmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIGNvbnN0IGtlcm5lbCA9XG4gICAgICAgICAgcGFyZW50ICYmXG4gICAgICAgICAgYWN0aXZlU2Vzc2lvbnNbcGFyZW50LmlkXSAmJlxuICAgICAgICAgIGFjdGl2ZVNlc3Npb25zW3BhcmVudC5pZF0ua2VybmVsO1xuICAgICAgICBpZiAoIWtlcm5lbCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBhbmNob3IgPSBwYXJlbnQhLmNvbnRlbnQ7XG4gICAgICAgIGNvbnN0IGVkaXRvciA9IGFuY2hvcj8uZWRpdG9yO1xuXG4gICAgICAgIC8vIElmIGFsbCBjb21wb25lbnRzIG5lY2Vzc2FyeSBmb3IgcmVuZGVyaW5nIGV4aXN0LCBjcmVhdGUgYSB0b29sdGlwLlxuICAgICAgICBpZiAoISFlZGl0b3IgJiYgISFrZXJuZWwgJiYgISFyZW5kZXJtaW1lKSB7XG4gICAgICAgICAgcmV0dXJuIG1hbmFnZXIuaW52b2tlKHsgYW5jaG9yLCBlZGl0b3IsIGtlcm5lbCwgcmVuZGVybWltZSB9KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2lucyBhcyBkZWZhdWx0LlxuICovXG5jb25zdCBwbHVnaW5zOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48YW55PltdID0gW1xuICBtYW5hZ2VyLFxuICBjb25zb2xlcyxcbiAgbm90ZWJvb2tzLFxuICBmaWxlc1xuXTtcbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQSBjb3VudGVyIGZvciBvdXRzdGFuZGluZyByZXF1ZXN0cy5cbiAgICovXG4gIGxldCBwZW5kaW5nID0gMDtcblxuICBleHBvcnQgaW50ZXJmYWNlIElGZXRjaE9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBkZXRhaWwgbGV2ZWwgcmVxdWVzdGVkIGZyb20gdGhlIEFQSS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGUgb25seSBhY2NlcHRhYmxlIHZhbHVlcyBhcmUgMCBhbmQgMS4gVGhlIGRlZmF1bHQgdmFsdWUgaXMgMC5cbiAgICAgKiBAc2VlIGh0dHA6Ly9qdXB5dGVyLWNsaWVudC5yZWFkdGhlZG9jcy5pby9lbi9sYXRlc3QvbWVzc2FnaW5nLmh0bWwjaW50cm9zcGVjdGlvblxuICAgICAqL1xuICAgIGRldGFpbD86IDAgfCAxO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJlZmVyZW50IGVkaXRvciBmb3IgdGhlIHRvb2x0aXAuXG4gICAgICovXG4gICAgZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3I7XG5cbiAgICAvKipcbiAgICAgKiBUaGUga2VybmVsIGFnYWluc3Qgd2hpY2ggdGhlIEFQSSByZXF1ZXN0IHdpbGwgYmUgbWFkZS5cbiAgICAgKi9cbiAgICBrZXJuZWw6IEtlcm5lbC5JS2VybmVsQ29ubmVjdGlvbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBGZXRjaCBhIHRvb2x0aXAncyBjb250ZW50IGZyb20gdGhlIEFQSSBzZXJ2ZXIuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZmV0Y2gob3B0aW9uczogSUZldGNoT3B0aW9ucyk6IFByb21pc2U8SlNPTk9iamVjdD4ge1xuICAgIGNvbnN0IHsgZGV0YWlsLCBlZGl0b3IsIGtlcm5lbCB9ID0gb3B0aW9ucztcbiAgICBjb25zdCBjb2RlID0gZWRpdG9yLm1vZGVsLnZhbHVlLnRleHQ7XG4gICAgY29uc3QgcG9zaXRpb24gPSBlZGl0b3IuZ2V0Q3Vyc29yUG9zaXRpb24oKTtcbiAgICBjb25zdCBvZmZzZXQgPSBUZXh0LmpzSW5kZXhUb0NoYXJJbmRleChlZGl0b3IuZ2V0T2Zmc2V0QXQocG9zaXRpb24pLCBjb2RlKTtcblxuICAgIC8vIENsZWFyIGhpbnRzIGlmIHRoZSBuZXcgdGV4dCB2YWx1ZSBpcyBlbXB0eSBvciBrZXJuZWwgaXMgdW5hdmFpbGFibGUuXG4gICAgaWYgKCFjb2RlIHx8ICFrZXJuZWwpIHtcbiAgICAgIHJldHVybiBQcm9taXNlLnJlamVjdCh2b2lkIDApO1xuICAgIH1cblxuICAgIGNvbnN0IGNvbnRlbnRzOiBLZXJuZWxNZXNzYWdlLklJbnNwZWN0UmVxdWVzdE1zZ1snY29udGVudCddID0ge1xuICAgICAgY29kZSxcbiAgICAgIGN1cnNvcl9wb3M6IG9mZnNldCxcbiAgICAgIGRldGFpbF9sZXZlbDogZGV0YWlsIHx8IDBcbiAgICB9O1xuICAgIGNvbnN0IGN1cnJlbnQgPSArK3BlbmRpbmc7XG5cbiAgICByZXR1cm4ga2VybmVsLnJlcXVlc3RJbnNwZWN0KGNvbnRlbnRzKS50aGVuKG1zZyA9PiB7XG4gICAgICBjb25zdCB2YWx1ZSA9IG1zZy5jb250ZW50O1xuXG4gICAgICAvLyBJZiBhIG5ld2VyIHJlcXVlc3QgaXMgcGVuZGluZywgYmFpbC5cbiAgICAgIGlmIChjdXJyZW50ICE9PSBwZW5kaW5nKSB7XG4gICAgICAgIHJldHVybiBQcm9taXNlLnJlamVjdCh2b2lkIDApIGFzIFByb21pc2U8SlNPTk9iamVjdD47XG4gICAgICB9XG5cbiAgICAgIC8vIElmIHJlcXVlc3QgZmFpbHMgb3IgcmV0dXJucyBuZWdhdGl2ZSByZXN1bHRzLCBiYWlsLlxuICAgICAgaWYgKHZhbHVlLnN0YXR1cyAhPT0gJ29rJyB8fCAhdmFsdWUuZm91bmQpIHtcbiAgICAgICAgcmV0dXJuIFByb21pc2UucmVqZWN0KHZvaWQgMCkgYXMgUHJvbWlzZTxKU09OT2JqZWN0PjtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZSh2YWx1ZS5kYXRhKTtcbiAgICB9KTtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==