(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_statusbar-extension_lib_index_js"],{

/***/ "../packages/statusbar-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../packages/statusbar-extension/lib/index.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "STATUSBAR_PLUGIN_ID": () => (/* binding */ STATUSBAR_PLUGIN_ID),
/* harmony export */   "kernelStatus": () => (/* binding */ kernelStatus),
/* harmony export */   "lineColItem": () => (/* binding */ lineColItem),
/* harmony export */   "runningSessionsItem": () => (/* binding */ runningSessionsItem),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands/@lumino/commands");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_commands__WEBPACK_IMPORTED_MODULE_9__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module statusbar-extension
 */










const STATUSBAR_PLUGIN_ID = '@jupyterlab/statusbar-extension:plugin';
/**
 * Initialization data for the statusbar extension.
 */
const statusBar = {
    id: STATUSBAR_PLUGIN_ID,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    provides: _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.IStatusBar,
    autoStart: true,
    activate: (app, translator, labShell, settingRegistry, palette) => {
        const trans = translator.load('jupyterlab');
        const statusBar = new _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.StatusBar();
        statusBar.id = 'jp-main-statusbar';
        app.shell.add(statusBar, 'bottom');
        // If available, connect to the shell's layout modified signal.
        if (labShell) {
            labShell.layoutModified.connect(() => {
                statusBar.update();
            });
        }
        const category = trans.__('Main Area');
        const command = 'statusbar:toggle';
        app.commands.addCommand(command, {
            label: trans.__('Show Status Bar'),
            execute: (args) => {
                statusBar.setHidden(statusBar.isVisible);
                if (settingRegistry) {
                    void settingRegistry.set(STATUSBAR_PLUGIN_ID, 'visible', statusBar.isVisible);
                }
            },
            isToggled: () => statusBar.isVisible
        });
        if (palette) {
            palette.addItem({ command, category });
        }
        if (settingRegistry) {
            const loadSettings = settingRegistry.load(STATUSBAR_PLUGIN_ID);
            const updateSettings = (settings) => {
                const visible = settings.get('visible').composite;
                statusBar.setHidden(!visible);
            };
            Promise.all([loadSettings, app.restored])
                .then(([settings]) => {
                updateSettings(settings);
                settings.changed.connect(settings => {
                    updateSettings(settings);
                });
            })
                .catch((reason) => {
                console.error(reason.message);
            });
        }
        return statusBar;
    },
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette]
};
/**
 * A plugin that provides a kernel status item to the status bar.
 */
const kernelStatus = {
    id: '@jupyterlab/statusbar-extension:kernel-status',
    autoStart: true,
    requires: [
        _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.IStatusBar,
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.INotebookTracker,
        _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__.IConsoleTracker,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator
    ],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs],
    activate: (app, statusBar, notebookTracker, consoleTracker, labShell, translator, sessionDialogs) => {
        // When the status item is clicked, launch the kernel
        // selection dialog for the current session.
        let currentSession = null;
        const changeKernel = async () => {
            if (!currentSession) {
                return;
            }
            await (sessionDialogs || _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.sessionContextDialogs).selectKernel(currentSession, translator);
        };
        // Create the status item.
        const item = new _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.KernelStatus({ onClick: changeKernel }, translator);
        // When the title of the active widget changes, update the label
        // of the hover text.
        const onTitleChanged = (title) => {
            item.model.activityName = title.label;
        };
        // Keep the session object on the status item up-to-date.
        labShell.currentChanged.connect((_, change) => {
            const { oldValue, newValue } = change;
            // Clean up after the old value if it exists,
            // listen for changes to the title of the activity
            if (oldValue) {
                oldValue.title.changed.disconnect(onTitleChanged);
            }
            if (newValue) {
                newValue.title.changed.connect(onTitleChanged);
            }
            // Grab the session off of the current widget, if it exists.
            if (newValue && consoleTracker.has(newValue)) {
                currentSession = newValue.sessionContext;
            }
            else if (newValue && notebookTracker.has(newValue)) {
                currentSession = newValue.sessionContext;
            }
            else {
                currentSession = null;
            }
            item.model.sessionContext = currentSession;
        });
        statusBar.registerStatusItem('@jupyterlab/statusbar-extension:kernel-status', {
            item,
            align: 'left',
            rank: 1,
            isActive: () => {
                const current = labShell.currentWidget;
                return (!!current &&
                    (notebookTracker.has(current) || consoleTracker.has(current)));
            }
        });
    }
};
/**
 * A plugin providing a line/column status item to the application.
 */
const lineColItem = {
    id: '@jupyterlab/statusbar-extension:line-col-status',
    autoStart: true,
    requires: [
        _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.IStatusBar,
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.INotebookTracker,
        _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorTracker,
        _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__.IConsoleTracker,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator
    ],
    activate: (_, statusBar, notebookTracker, editorTracker, consoleTracker, labShell, translator) => {
        const item = new _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.LineCol(translator);
        const onActiveCellChanged = (notebook, cell) => {
            item.model.editor = cell && cell.editor;
        };
        const onPromptCreated = (console, prompt) => {
            item.model.editor = prompt && prompt.editor;
        };
        labShell.currentChanged.connect((_, change) => {
            const { oldValue, newValue } = change;
            // Check if we need to disconnect the console listener
            // or the notebook active cell listener
            if (oldValue && consoleTracker.has(oldValue)) {
                oldValue.console.promptCellCreated.disconnect(onPromptCreated);
            }
            else if (oldValue && notebookTracker.has(oldValue)) {
                oldValue.content.activeCellChanged.disconnect(onActiveCellChanged);
            }
            // Wire up the new editor to the model if it exists
            if (newValue && consoleTracker.has(newValue)) {
                newValue.console.promptCellCreated.connect(onPromptCreated);
                const prompt = newValue.console.promptCell;
                item.model.editor = prompt && prompt.editor;
            }
            else if (newValue && notebookTracker.has(newValue)) {
                newValue.content.activeCellChanged.connect(onActiveCellChanged);
                const cell = newValue.content.activeCell;
                item.model.editor = cell && cell.editor;
            }
            else if (newValue && editorTracker.has(newValue)) {
                item.model.editor = newValue.content.editor;
            }
            else {
                item.model.editor = null;
            }
        });
        // Add the status item to the status bar.
        statusBar.registerStatusItem('@jupyterlab/statusbar-extension:line-col-status', {
            item,
            align: 'right',
            rank: 2,
            isActive: () => {
                const current = labShell.currentWidget;
                return (!!current &&
                    (notebookTracker.has(current) ||
                        editorTracker.has(current) ||
                        consoleTracker.has(current)));
            }
        });
    }
};
/*
 * A plugin providing running terminals and sessions information
 * to the status bar.
 */
const runningSessionsItem = {
    id: '@jupyterlab/statusbar-extension:running-sessions-status',
    autoStart: true,
    requires: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.IStatusBar, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    activate: (app, statusBar, translator) => {
        const item = new _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.RunningSessions({
            onClick: () => app.shell.activateById('jp-running-sessions'),
            serviceManager: app.serviceManager,
            translator
        });
        statusBar.registerStatusItem('@jupyterlab/statusbar-extension:running-sessions-status', {
            item,
            align: 'left',
            rank: 0
        });
    }
};
/**
 * The simple interface mode switch in the status bar.
 */
const modeSwitch = {
    id: '@jupyterlab/statusbar-extension:mode-switch',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator, _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.IStatusBar],
    activate: (app, shell, translator, statusBar) => {
        const trans = translator.load('jupyterlab');
        const modeSwitch = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.Switch();
        modeSwitch.id = 'jp-single-document-mode';
        modeSwitch.valueChanged.connect((_, args) => {
            shell.mode = args.newValue ? 'single-document' : 'multiple-document';
        });
        shell.modeChanged.connect((_, mode) => {
            modeSwitch.value = mode === 'single-document';
        });
        modeSwitch.value = shell.mode === 'single-document';
        // Show the current file browser shortcut in its title.
        const updateModeSwitchTitle = () => {
            const binding = app.commands.keyBindings.find(b => b.command === 'application:toggle-mode');
            if (binding) {
                const ks = _lumino_commands__WEBPACK_IMPORTED_MODULE_9__.CommandRegistry.formatKeystroke(binding.keys.join(' '));
                modeSwitch.caption = trans.__('Simple Interface (%1)', ks);
            }
            else {
                modeSwitch.caption = trans.__('Simple Interface');
            }
        };
        updateModeSwitchTitle();
        app.commands.keyBindingChanged.connect(() => {
            updateModeSwitchTitle();
        });
        modeSwitch.label = trans.__('Simple');
        statusBar.registerStatusItem('@jupyterlab/statusbar-extension:mode-switch', {
            item: modeSwitch,
            align: 'left',
            rank: -1
        });
    },
    autoStart: true
};
const plugins = [
    statusBar,
    lineColItem,
    kernelStatus,
    runningSessionsItem,
    modeSwitch
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTThCO0FBTUg7QUFNRDtBQUV1QztBQUt0QztBQUNpQztBQU9oQztBQUN1QjtBQUNIO0FBQ0E7QUFHNUMsTUFBTSxtQkFBbUIsR0FBRyx3Q0FBd0MsQ0FBQztBQUU1RTs7R0FFRztBQUNILE1BQU0sU0FBUyxHQUFzQztJQUNuRCxFQUFFLEVBQUUsbUJBQW1CO0lBQ3ZCLFFBQVEsRUFBRSxDQUFDLGdFQUFXLENBQUM7SUFDdkIsUUFBUSxFQUFFLDZEQUFVO0lBQ3BCLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQ1IsR0FBb0IsRUFDcEIsVUFBdUIsRUFDdkIsUUFBMEIsRUFDMUIsZUFBd0MsRUFDeEMsT0FBK0IsRUFDL0IsRUFBRTtRQUNGLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7UUFDNUMsTUFBTSxTQUFTLEdBQUcsSUFBSSw0REFBUyxFQUFFLENBQUM7UUFDbEMsU0FBUyxDQUFDLEVBQUUsR0FBRyxtQkFBbUIsQ0FBQztRQUNuQyxHQUFHLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxTQUFTLEVBQUUsUUFBUSxDQUFDLENBQUM7UUFFbkMsK0RBQStEO1FBQy9ELElBQUksUUFBUSxFQUFFO1lBQ1osUUFBUSxDQUFDLGNBQWMsQ0FBQyxPQUFPLENBQUMsR0FBRyxFQUFFO2dCQUNuQyxTQUFTLENBQUMsTUFBTSxFQUFFLENBQUM7WUFDckIsQ0FBQyxDQUFDLENBQUM7U0FDSjtRQUVELE1BQU0sUUFBUSxHQUFXLEtBQUssQ0FBQyxFQUFFLENBQUMsV0FBVyxDQUFDLENBQUM7UUFDL0MsTUFBTSxPQUFPLEdBQVcsa0JBQWtCLENBQUM7UUFFM0MsR0FBRyxDQUFDLFFBQVEsQ0FBQyxVQUFVLENBQUMsT0FBTyxFQUFFO1lBQy9CLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGlCQUFpQixDQUFDO1lBQ2xDLE9BQU8sRUFBRSxDQUFDLElBQVMsRUFBRSxFQUFFO2dCQUNyQixTQUFTLENBQUMsU0FBUyxDQUFDLFNBQVMsQ0FBQyxTQUFTLENBQUMsQ0FBQztnQkFDekMsSUFBSSxlQUFlLEVBQUU7b0JBQ25CLEtBQUssZUFBZSxDQUFDLEdBQUcsQ0FDdEIsbUJBQW1CLEVBQ25CLFNBQVMsRUFDVCxTQUFTLENBQUMsU0FBUyxDQUNwQixDQUFDO2lCQUNIO1lBQ0gsQ0FBQztZQUNELFNBQVMsRUFBRSxHQUFHLEVBQUUsQ0FBQyxTQUFTLENBQUMsU0FBUztTQUNyQyxDQUFDLENBQUM7UUFFSCxJQUFJLE9BQU8sRUFBRTtZQUNYLE9BQU8sQ0FBQyxPQUFPLENBQUMsRUFBRSxPQUFPLEVBQUUsUUFBUSxFQUFFLENBQUMsQ0FBQztTQUN4QztRQUVELElBQUksZUFBZSxFQUFFO1lBQ25CLE1BQU0sWUFBWSxHQUFHLGVBQWUsQ0FBQyxJQUFJLENBQUMsbUJBQW1CLENBQUMsQ0FBQztZQUMvRCxNQUFNLGNBQWMsR0FBRyxDQUFDLFFBQW9DLEVBQVEsRUFBRTtnQkFDcEUsTUFBTSxPQUFPLEdBQUcsUUFBUSxDQUFDLEdBQUcsQ0FBQyxTQUFTLENBQUMsQ0FBQyxTQUFvQixDQUFDO2dCQUM3RCxTQUFTLENBQUMsU0FBUyxDQUFDLENBQUMsT0FBTyxDQUFDLENBQUM7WUFDaEMsQ0FBQyxDQUFDO1lBRUYsT0FBTyxDQUFDLEdBQUcsQ0FBQyxDQUFDLFlBQVksRUFBRSxHQUFHLENBQUMsUUFBUSxDQUFDLENBQUM7aUJBQ3RDLElBQUksQ0FBQyxDQUFDLENBQUMsUUFBUSxDQUFDLEVBQUUsRUFBRTtnQkFDbkIsY0FBYyxDQUFDLFFBQVEsQ0FBQyxDQUFDO2dCQUN6QixRQUFRLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxRQUFRLENBQUMsRUFBRTtvQkFDbEMsY0FBYyxDQUFDLFFBQVEsQ0FBQyxDQUFDO2dCQUMzQixDQUFDLENBQUMsQ0FBQztZQUNMLENBQUMsQ0FBQztpQkFDRCxLQUFLLENBQUMsQ0FBQyxNQUFhLEVBQUUsRUFBRTtnQkFDdkIsT0FBTyxDQUFDLEtBQUssQ0FBQyxNQUFNLENBQUMsT0FBTyxDQUFDLENBQUM7WUFDaEMsQ0FBQyxDQUFDLENBQUM7U0FDTjtRQUVELE9BQU8sU0FBUyxDQUFDO0lBQ25CLENBQUM7SUFDRCxRQUFRLEVBQUUsQ0FBQyw4REFBUyxFQUFFLHlFQUFnQixFQUFFLGlFQUFlLENBQUM7Q0FDekQsQ0FBQztBQUVGOztHQUVHO0FBQ0ksTUFBTSxZQUFZLEdBQWdDO0lBQ3ZELEVBQUUsRUFBRSwrQ0FBK0M7SUFDbkQsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUU7UUFDUiw2REFBVTtRQUNWLGtFQUFnQjtRQUNoQixnRUFBZTtRQUNmLDhEQUFTO1FBQ1QsZ0VBQVc7S0FDWjtJQUNELFFBQVEsRUFBRSxDQUFDLHdFQUFzQixDQUFDO0lBQ2xDLFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLFNBQXFCLEVBQ3JCLGVBQWlDLEVBQ2pDLGNBQStCLEVBQy9CLFFBQW1CLEVBQ25CLFVBQXVCLEVBQ3ZCLGNBQTZDLEVBQzdDLEVBQUU7UUFDRixxREFBcUQ7UUFDckQsNENBQTRDO1FBQzVDLElBQUksY0FBYyxHQUEyQixJQUFJLENBQUM7UUFDbEQsTUFBTSxZQUFZLEdBQUcsS0FBSyxJQUFJLEVBQUU7WUFDOUIsSUFBSSxDQUFDLGNBQWMsRUFBRTtnQkFDbkIsT0FBTzthQUNSO1lBQ0QsTUFBTSxDQUFDLGNBQWMsSUFBSSx1RUFBcUIsQ0FBQyxDQUFDLFlBQVksQ0FDMUQsY0FBYyxFQUNkLFVBQVUsQ0FDWCxDQUFDO1FBQ0osQ0FBQyxDQUFDO1FBRUYsMEJBQTBCO1FBQzFCLE1BQU0sSUFBSSxHQUFHLElBQUksK0RBQVksQ0FBQyxFQUFFLE9BQU8sRUFBRSxZQUFZLEVBQUUsRUFBRSxVQUFVLENBQUMsQ0FBQztRQUVyRSxnRUFBZ0U7UUFDaEUscUJBQXFCO1FBQ3JCLE1BQU0sY0FBYyxHQUFHLENBQUMsS0FBb0IsRUFBRSxFQUFFO1lBQzlDLElBQUksQ0FBQyxLQUFNLENBQUMsWUFBWSxHQUFHLEtBQUssQ0FBQyxLQUFLLENBQUM7UUFDekMsQ0FBQyxDQUFDO1FBRUYseURBQXlEO1FBQ3pELFFBQVEsQ0FBQyxjQUFjLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyxFQUFFLE1BQU0sRUFBRSxFQUFFO1lBQzVDLE1BQU0sRUFBRSxRQUFRLEVBQUUsUUFBUSxFQUFFLEdBQUcsTUFBTSxDQUFDO1lBRXRDLDZDQUE2QztZQUM3QyxrREFBa0Q7WUFDbEQsSUFBSSxRQUFRLEVBQUU7Z0JBQ1osUUFBUSxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsVUFBVSxDQUFDLGNBQWMsQ0FBQyxDQUFDO2FBQ25EO1lBQ0QsSUFBSSxRQUFRLEVBQUU7Z0JBQ1osUUFBUSxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLGNBQWMsQ0FBQyxDQUFDO2FBQ2hEO1lBRUQsNERBQTREO1lBQzVELElBQUksUUFBUSxJQUFJLGNBQWMsQ0FBQyxHQUFHLENBQUMsUUFBUSxDQUFDLEVBQUU7Z0JBQzVDLGNBQWMsR0FBSSxRQUF5QixDQUFDLGNBQWMsQ0FBQzthQUM1RDtpQkFBTSxJQUFJLFFBQVEsSUFBSSxlQUFlLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxFQUFFO2dCQUNwRCxjQUFjLEdBQUksUUFBMEIsQ0FBQyxjQUFjLENBQUM7YUFDN0Q7aUJBQU07Z0JBQ0wsY0FBYyxHQUFHLElBQUksQ0FBQzthQUN2QjtZQUNELElBQUksQ0FBQyxLQUFNLENBQUMsY0FBYyxHQUFHLGNBQWMsQ0FBQztRQUM5QyxDQUFDLENBQUMsQ0FBQztRQUVILFNBQVMsQ0FBQyxrQkFBa0IsQ0FDMUIsK0NBQStDLEVBQy9DO1lBQ0UsSUFBSTtZQUNKLEtBQUssRUFBRSxNQUFNO1lBQ2IsSUFBSSxFQUFFLENBQUM7WUFDUCxRQUFRLEVBQUUsR0FBRyxFQUFFO2dCQUNiLE1BQU0sT0FBTyxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUM7Z0JBQ3ZDLE9BQU8sQ0FDTCxDQUFDLENBQUMsT0FBTztvQkFDVCxDQUFDLGVBQWUsQ0FBQyxHQUFHLENBQUMsT0FBTyxDQUFDLElBQUksY0FBYyxDQUFDLEdBQUcsQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUM5RCxDQUFDO1lBQ0osQ0FBQztTQUNGLENBQ0YsQ0FBQztJQUNKLENBQUM7Q0FDRixDQUFDO0FBRUY7O0dBRUc7QUFDSSxNQUFNLFdBQVcsR0FBZ0M7SUFDdEQsRUFBRSxFQUFFLGlEQUFpRDtJQUNyRCxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRTtRQUNSLDZEQUFVO1FBQ1Ysa0VBQWdCO1FBQ2hCLGtFQUFjO1FBQ2QsZ0VBQWU7UUFDZiw4REFBUztRQUNULGdFQUFXO0tBQ1o7SUFDRCxRQUFRLEVBQUUsQ0FDUixDQUFrQixFQUNsQixTQUFxQixFQUNyQixlQUFpQyxFQUNqQyxhQUE2QixFQUM3QixjQUErQixFQUMvQixRQUFtQixFQUNuQixVQUF1QixFQUN2QixFQUFFO1FBQ0YsTUFBTSxJQUFJLEdBQUcsSUFBSSwwREFBTyxDQUFDLFVBQVUsQ0FBQyxDQUFDO1FBRXJDLE1BQU0sbUJBQW1CLEdBQUcsQ0FBQyxRQUFrQixFQUFFLElBQVUsRUFBRSxFQUFFO1lBQzdELElBQUksQ0FBQyxLQUFNLENBQUMsTUFBTSxHQUFHLElBQUksSUFBSSxJQUFJLENBQUMsTUFBTSxDQUFDO1FBQzNDLENBQUMsQ0FBQztRQUVGLE1BQU0sZUFBZSxHQUFHLENBQUMsT0FBb0IsRUFBRSxNQUFnQixFQUFFLEVBQUU7WUFDakUsSUFBSSxDQUFDLEtBQU0sQ0FBQyxNQUFNLEdBQUcsTUFBTSxJQUFJLE1BQU0sQ0FBQyxNQUFNLENBQUM7UUFDL0MsQ0FBQyxDQUFDO1FBRUYsUUFBUSxDQUFDLGNBQWMsQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLEVBQUUsTUFBTSxFQUFFLEVBQUU7WUFDNUMsTUFBTSxFQUFFLFFBQVEsRUFBRSxRQUFRLEVBQUUsR0FBRyxNQUFNLENBQUM7WUFFdEMsc0RBQXNEO1lBQ3RELHVDQUF1QztZQUN2QyxJQUFJLFFBQVEsSUFBSSxjQUFjLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxFQUFFO2dCQUMzQyxRQUF5QixDQUFDLE9BQU8sQ0FBQyxpQkFBaUIsQ0FBQyxVQUFVLENBQzdELGVBQWUsQ0FDaEIsQ0FBQzthQUNIO2lCQUFNLElBQUksUUFBUSxJQUFJLGVBQWUsQ0FBQyxHQUFHLENBQUMsUUFBUSxDQUFDLEVBQUU7Z0JBQ25ELFFBQTBCLENBQUMsT0FBTyxDQUFDLGlCQUFpQixDQUFDLFVBQVUsQ0FDOUQsbUJBQW1CLENBQ3BCLENBQUM7YUFDSDtZQUVELG1EQUFtRDtZQUNuRCxJQUFJLFFBQVEsSUFBSSxjQUFjLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxFQUFFO2dCQUMzQyxRQUF5QixDQUFDLE9BQU8sQ0FBQyxpQkFBaUIsQ0FBQyxPQUFPLENBQzFELGVBQWUsQ0FDaEIsQ0FBQztnQkFDRixNQUFNLE1BQU0sR0FBSSxRQUF5QixDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUM7Z0JBQzdELElBQUksQ0FBQyxLQUFNLENBQUMsTUFBTSxHQUFHLE1BQU0sSUFBSSxNQUFNLENBQUMsTUFBTSxDQUFDO2FBQzlDO2lCQUFNLElBQUksUUFBUSxJQUFJLGVBQWUsQ0FBQyxHQUFHLENBQUMsUUFBUSxDQUFDLEVBQUU7Z0JBQ25ELFFBQTBCLENBQUMsT0FBTyxDQUFDLGlCQUFpQixDQUFDLE9BQU8sQ0FDM0QsbUJBQW1CLENBQ3BCLENBQUM7Z0JBQ0YsTUFBTSxJQUFJLEdBQUksUUFBMEIsQ0FBQyxPQUFPLENBQUMsVUFBVSxDQUFDO2dCQUM1RCxJQUFJLENBQUMsS0FBTSxDQUFDLE1BQU0sR0FBRyxJQUFJLElBQUksSUFBSSxDQUFDLE1BQU0sQ0FBQzthQUMxQztpQkFBTSxJQUFJLFFBQVEsSUFBSSxhQUFhLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxFQUFFO2dCQUNsRCxJQUFJLENBQUMsS0FBTSxDQUFDLE1BQU0sR0FBSSxRQUVwQixDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUM7YUFDbkI7aUJBQU07Z0JBQ0wsSUFBSSxDQUFDLEtBQU0sQ0FBQyxNQUFNLEdBQUcsSUFBSSxDQUFDO2FBQzNCO1FBQ0gsQ0FBQyxDQUFDLENBQUM7UUFFSCx5Q0FBeUM7UUFDekMsU0FBUyxDQUFDLGtCQUFrQixDQUMxQixpREFBaUQsRUFDakQ7WUFDRSxJQUFJO1lBQ0osS0FBSyxFQUFFLE9BQU87WUFDZCxJQUFJLEVBQUUsQ0FBQztZQUNQLFFBQVEsRUFBRSxHQUFHLEVBQUU7Z0JBQ2IsTUFBTSxPQUFPLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQztnQkFDdkMsT0FBTyxDQUNMLENBQUMsQ0FBQyxPQUFPO29CQUNULENBQUMsZUFBZSxDQUFDLEdBQUcsQ0FBQyxPQUFPLENBQUM7d0JBQzNCLGFBQWEsQ0FBQyxHQUFHLENBQUMsT0FBTyxDQUFDO3dCQUMxQixjQUFjLENBQUMsR0FBRyxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQy9CLENBQUM7WUFDSixDQUFDO1NBQ0YsQ0FDRixDQUFDO0lBQ0osQ0FBQztDQUNGLENBQUM7QUFFRjs7O0dBR0c7QUFDSSxNQUFNLG1CQUFtQixHQUFnQztJQUM5RCxFQUFFLEVBQUUseURBQXlEO0lBQzdELFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQUMsNkRBQVUsRUFBRSxnRUFBVyxDQUFDO0lBQ25DLFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLFNBQXFCLEVBQ3JCLFVBQXVCLEVBQ3ZCLEVBQUU7UUFDRixNQUFNLElBQUksR0FBRyxJQUFJLGtFQUFlLENBQUM7WUFDL0IsT0FBTyxFQUFFLEdBQUcsRUFBRSxDQUFDLEdBQUcsQ0FBQyxLQUFLLENBQUMsWUFBWSxDQUFDLHFCQUFxQixDQUFDO1lBQzVELGNBQWMsRUFBRSxHQUFHLENBQUMsY0FBYztZQUNsQyxVQUFVO1NBQ1gsQ0FBQyxDQUFDO1FBRUgsU0FBUyxDQUFDLGtCQUFrQixDQUMxQix5REFBeUQsRUFDekQ7WUFDRSxJQUFJO1lBQ0osS0FBSyxFQUFFLE1BQU07WUFDYixJQUFJLEVBQUUsQ0FBQztTQUNSLENBQ0YsQ0FBQztJQUNKLENBQUM7Q0FDRixDQUFDO0FBRUY7O0dBRUc7QUFDSCxNQUFNLFVBQVUsR0FBZ0M7SUFDOUMsRUFBRSxFQUFFLDZDQUE2QztJQUNqRCxRQUFRLEVBQUUsQ0FBQyw4REFBUyxFQUFFLGdFQUFXLEVBQUUsNkRBQVUsQ0FBQztJQUM5QyxRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixLQUFnQixFQUNoQixVQUF1QixFQUN2QixTQUFxQixFQUNyQixFQUFFO1FBQ0YsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztRQUM1QyxNQUFNLFVBQVUsR0FBRyxJQUFJLDZEQUFNLEVBQUUsQ0FBQztRQUNoQyxVQUFVLENBQUMsRUFBRSxHQUFHLHlCQUF5QixDQUFDO1FBRTFDLFVBQVUsQ0FBQyxZQUFZLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyxFQUFFLElBQUksRUFBRSxFQUFFO1lBQzFDLEtBQUssQ0FBQyxJQUFJLEdBQUcsSUFBSSxDQUFDLFFBQVEsQ0FBQyxDQUFDLENBQUMsaUJBQWlCLENBQUMsQ0FBQyxDQUFDLG1CQUFtQixDQUFDO1FBQ3ZFLENBQUMsQ0FBQyxDQUFDO1FBQ0gsS0FBSyxDQUFDLFdBQVcsQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLEVBQUUsSUFBSSxFQUFFLEVBQUU7WUFDcEMsVUFBVSxDQUFDLEtBQUssR0FBRyxJQUFJLEtBQUssaUJBQWlCLENBQUM7UUFDaEQsQ0FBQyxDQUFDLENBQUM7UUFDSCxVQUFVLENBQUMsS0FBSyxHQUFHLEtBQUssQ0FBQyxJQUFJLEtBQUssaUJBQWlCLENBQUM7UUFFcEQsdURBQXVEO1FBQ3ZELE1BQU0scUJBQXFCLEdBQUcsR0FBRyxFQUFFO1lBQ2pDLE1BQU0sT0FBTyxHQUFHLEdBQUcsQ0FBQyxRQUFRLENBQUMsV0FBVyxDQUFDLElBQUksQ0FDM0MsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxDQUFDLENBQUMsT0FBTyxLQUFLLHlCQUF5QixDQUM3QyxDQUFDO1lBQ0YsSUFBSSxPQUFPLEVBQUU7Z0JBQ1gsTUFBTSxFQUFFLEdBQUcsNkVBQStCLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsR0FBRyxDQUFDLENBQUMsQ0FBQztnQkFDbkUsVUFBVSxDQUFDLE9BQU8sR0FBRyxLQUFLLENBQUMsRUFBRSxDQUFDLHVCQUF1QixFQUFFLEVBQUUsQ0FBQyxDQUFDO2FBQzVEO2lCQUFNO2dCQUNMLFVBQVUsQ0FBQyxPQUFPLEdBQUcsS0FBSyxDQUFDLEVBQUUsQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO2FBQ25EO1FBQ0gsQ0FBQyxDQUFDO1FBQ0YscUJBQXFCLEVBQUUsQ0FBQztRQUN4QixHQUFHLENBQUMsUUFBUSxDQUFDLGlCQUFpQixDQUFDLE9BQU8sQ0FBQyxHQUFHLEVBQUU7WUFDMUMscUJBQXFCLEVBQUUsQ0FBQztRQUMxQixDQUFDLENBQUMsQ0FBQztRQUVILFVBQVUsQ0FBQyxLQUFLLEdBQUcsS0FBSyxDQUFDLEVBQUUsQ0FBQyxRQUFRLENBQUMsQ0FBQztRQUV0QyxTQUFTLENBQUMsa0JBQWtCLENBQzFCLDZDQUE2QyxFQUM3QztZQUNFLElBQUksRUFBRSxVQUFVO1lBQ2hCLEtBQUssRUFBRSxNQUFNO1lBQ2IsSUFBSSxFQUFFLENBQUMsQ0FBQztTQUNULENBQ0YsQ0FBQztJQUNKLENBQUM7SUFDRCxTQUFTLEVBQUUsSUFBSTtDQUNoQixDQUFDO0FBRUYsTUFBTSxPQUFPLEdBQWlDO0lBQzVDLFNBQVM7SUFDVCxXQUFXO0lBQ1gsWUFBWTtJQUNaLG1CQUFtQjtJQUNuQixVQUFVO0NBQ1gsQ0FBQztBQUVGLGlFQUFlLE9BQU8sRUFBQyIsImZpbGUiOiJwYWNrYWdlc19zdGF0dXNiYXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy43NWM5NmVhMGQ3NTdkNTRiNDE1NS5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHN0YXR1c2Jhci1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGFiU2hlbGwsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgSVNlc3Npb25Db250ZXh0LFxuICBJU2Vzc2lvbkNvbnRleHREaWFsb2dzLFxuICBzZXNzaW9uQ29udGV4dERpYWxvZ3Ncbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgQ2VsbCwgQ29kZUNlbGwgfSBmcm9tICdAanVweXRlcmxhYi9jZWxscyc7XG5pbXBvcnQge1xuICBDb2RlQ29uc29sZSxcbiAgQ29uc29sZVBhbmVsLFxuICBJQ29uc29sZVRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvY29uc29sZSc7XG5pbXBvcnQgeyBJRG9jdW1lbnRXaWRnZXQgfSBmcm9tICdAanVweXRlcmxhYi9kb2NyZWdpc3RyeSc7XG5pbXBvcnQgeyBGaWxlRWRpdG9yLCBJRWRpdG9yVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2ZpbGVlZGl0b3InO1xuaW1wb3J0IHtcbiAgSU5vdGVib29rVHJhY2tlcixcbiAgTm90ZWJvb2ssXG4gIE5vdGVib29rUGFuZWxcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvbm90ZWJvb2snO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQge1xuICBJU3RhdHVzQmFyLFxuICBLZXJuZWxTdGF0dXMsXG4gIExpbmVDb2wsXG4gIFJ1bm5pbmdTZXNzaW9ucyxcbiAgU3RhdHVzQmFyXG59IGZyb20gJ0BqdXB5dGVybGFiL3N0YXR1c2Jhcic7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IFN3aXRjaCB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgQ29tbWFuZFJlZ2lzdHJ5IH0gZnJvbSAnQGx1bWluby9jb21tYW5kcyc7XG5pbXBvcnQgeyBUaXRsZSwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuZXhwb3J0IGNvbnN0IFNUQVRVU0JBUl9QTFVHSU5fSUQgPSAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyLWV4dGVuc2lvbjpwbHVnaW4nO1xuXG4vKipcbiAqIEluaXRpYWxpemF0aW9uIGRhdGEgZm9yIHRoZSBzdGF0dXNiYXIgZXh0ZW5zaW9uLlxuICovXG5jb25zdCBzdGF0dXNCYXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJU3RhdHVzQmFyPiA9IHtcbiAgaWQ6IFNUQVRVU0JBUl9QTFVHSU5fSUQsXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3JdLFxuICBwcm92aWRlczogSVN0YXR1c0JhcixcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsLFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSB8IG51bGwsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHN0YXR1c0JhciA9IG5ldyBTdGF0dXNCYXIoKTtcbiAgICBzdGF0dXNCYXIuaWQgPSAnanAtbWFpbi1zdGF0dXNiYXInO1xuICAgIGFwcC5zaGVsbC5hZGQoc3RhdHVzQmFyLCAnYm90dG9tJyk7XG5cbiAgICAvLyBJZiBhdmFpbGFibGUsIGNvbm5lY3QgdG8gdGhlIHNoZWxsJ3MgbGF5b3V0IG1vZGlmaWVkIHNpZ25hbC5cbiAgICBpZiAobGFiU2hlbGwpIHtcbiAgICAgIGxhYlNoZWxsLmxheW91dE1vZGlmaWVkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICBzdGF0dXNCYXIudXBkYXRlKCk7XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBjb25zdCBjYXRlZ29yeTogc3RyaW5nID0gdHJhbnMuX18oJ01haW4gQXJlYScpO1xuICAgIGNvbnN0IGNvbW1hbmQ6IHN0cmluZyA9ICdzdGF0dXNiYXI6dG9nZ2xlJztcblxuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKGNvbW1hbmQsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnU2hvdyBTdGF0dXMgQmFyJyksXG4gICAgICBleGVjdXRlOiAoYXJnczogYW55KSA9PiB7XG4gICAgICAgIHN0YXR1c0Jhci5zZXRIaWRkZW4oc3RhdHVzQmFyLmlzVmlzaWJsZSk7XG4gICAgICAgIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICAgICAgICB2b2lkIHNldHRpbmdSZWdpc3RyeS5zZXQoXG4gICAgICAgICAgICBTVEFUVVNCQVJfUExVR0lOX0lELFxuICAgICAgICAgICAgJ3Zpc2libGUnLFxuICAgICAgICAgICAgc3RhdHVzQmFyLmlzVmlzaWJsZVxuICAgICAgICAgICk7XG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBpc1RvZ2dsZWQ6ICgpID0+IHN0YXR1c0Jhci5pc1Zpc2libGVcbiAgICB9KTtcblxuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kLCBjYXRlZ29yeSB9KTtcbiAgICB9XG5cbiAgICBpZiAoc2V0dGluZ1JlZ2lzdHJ5KSB7XG4gICAgICBjb25zdCBsb2FkU2V0dGluZ3MgPSBzZXR0aW5nUmVnaXN0cnkubG9hZChTVEFUVVNCQVJfUExVR0lOX0lEKTtcbiAgICAgIGNvbnN0IHVwZGF0ZVNldHRpbmdzID0gKHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyk6IHZvaWQgPT4ge1xuICAgICAgICBjb25zdCB2aXNpYmxlID0gc2V0dGluZ3MuZ2V0KCd2aXNpYmxlJykuY29tcG9zaXRlIGFzIGJvb2xlYW47XG4gICAgICAgIHN0YXR1c0Jhci5zZXRIaWRkZW4oIXZpc2libGUpO1xuICAgICAgfTtcblxuICAgICAgUHJvbWlzZS5hbGwoW2xvYWRTZXR0aW5ncywgYXBwLnJlc3RvcmVkXSlcbiAgICAgICAgLnRoZW4oKFtzZXR0aW5nc10pID0+IHtcbiAgICAgICAgICB1cGRhdGVTZXR0aW5ncyhzZXR0aW5ncyk7XG4gICAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KHNldHRpbmdzID0+IHtcbiAgICAgICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgICAgICB9KTtcbiAgICAgICAgfSlcbiAgICAgICAgLmNhdGNoKChyZWFzb246IEVycm9yKSA9PiB7XG4gICAgICAgICAgY29uc29sZS5lcnJvcihyZWFzb24ubWVzc2FnZSk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIHJldHVybiBzdGF0dXNCYXI7XG4gIH0sXG4gIG9wdGlvbmFsOiBbSUxhYlNoZWxsLCBJU2V0dGluZ1JlZ2lzdHJ5LCBJQ29tbWFuZFBhbGV0dGVdXG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHRoYXQgcHJvdmlkZXMgYSBrZXJuZWwgc3RhdHVzIGl0ZW0gdG8gdGhlIHN0YXR1cyBiYXIuXG4gKi9cbmV4cG9ydCBjb25zdCBrZXJuZWxTdGF0dXM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9zdGF0dXNiYXItZXh0ZW5zaW9uOmtlcm5lbC1zdGF0dXMnLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbXG4gICAgSVN0YXR1c0JhcixcbiAgICBJTm90ZWJvb2tUcmFja2VyLFxuICAgIElDb25zb2xlVHJhY2tlcixcbiAgICBJTGFiU2hlbGwsXG4gICAgSVRyYW5zbGF0b3JcbiAgXSxcbiAgb3B0aW9uYWw6IFtJU2Vzc2lvbkNvbnRleHREaWFsb2dzXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzdGF0dXNCYXI6IElTdGF0dXNCYXIsXG4gICAgbm90ZWJvb2tUcmFja2VyOiBJTm90ZWJvb2tUcmFja2VyLFxuICAgIGNvbnNvbGVUcmFja2VyOiBJQ29uc29sZVRyYWNrZXIsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBzZXNzaW9uRGlhbG9nczogSVNlc3Npb25Db250ZXh0RGlhbG9ncyB8IG51bGxcbiAgKSA9PiB7XG4gICAgLy8gV2hlbiB0aGUgc3RhdHVzIGl0ZW0gaXMgY2xpY2tlZCwgbGF1bmNoIHRoZSBrZXJuZWxcbiAgICAvLyBzZWxlY3Rpb24gZGlhbG9nIGZvciB0aGUgY3VycmVudCBzZXNzaW9uLlxuICAgIGxldCBjdXJyZW50U2Vzc2lvbjogSVNlc3Npb25Db250ZXh0IHwgbnVsbCA9IG51bGw7XG4gICAgY29uc3QgY2hhbmdlS2VybmVsID0gYXN5bmMgKCkgPT4ge1xuICAgICAgaWYgKCFjdXJyZW50U2Vzc2lvbikge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBhd2FpdCAoc2Vzc2lvbkRpYWxvZ3MgfHwgc2Vzc2lvbkNvbnRleHREaWFsb2dzKS5zZWxlY3RLZXJuZWwoXG4gICAgICAgIGN1cnJlbnRTZXNzaW9uLFxuICAgICAgICB0cmFuc2xhdG9yXG4gICAgICApO1xuICAgIH07XG5cbiAgICAvLyBDcmVhdGUgdGhlIHN0YXR1cyBpdGVtLlxuICAgIGNvbnN0IGl0ZW0gPSBuZXcgS2VybmVsU3RhdHVzKHsgb25DbGljazogY2hhbmdlS2VybmVsIH0sIHRyYW5zbGF0b3IpO1xuXG4gICAgLy8gV2hlbiB0aGUgdGl0bGUgb2YgdGhlIGFjdGl2ZSB3aWRnZXQgY2hhbmdlcywgdXBkYXRlIHRoZSBsYWJlbFxuICAgIC8vIG9mIHRoZSBob3ZlciB0ZXh0LlxuICAgIGNvbnN0IG9uVGl0bGVDaGFuZ2VkID0gKHRpdGxlOiBUaXRsZTxXaWRnZXQ+KSA9PiB7XG4gICAgICBpdGVtLm1vZGVsIS5hY3Rpdml0eU5hbWUgPSB0aXRsZS5sYWJlbDtcbiAgICB9O1xuXG4gICAgLy8gS2VlcCB0aGUgc2Vzc2lvbiBvYmplY3Qgb24gdGhlIHN0YXR1cyBpdGVtIHVwLXRvLWRhdGUuXG4gICAgbGFiU2hlbGwuY3VycmVudENoYW5nZWQuY29ubmVjdCgoXywgY2hhbmdlKSA9PiB7XG4gICAgICBjb25zdCB7IG9sZFZhbHVlLCBuZXdWYWx1ZSB9ID0gY2hhbmdlO1xuXG4gICAgICAvLyBDbGVhbiB1cCBhZnRlciB0aGUgb2xkIHZhbHVlIGlmIGl0IGV4aXN0cyxcbiAgICAgIC8vIGxpc3RlbiBmb3IgY2hhbmdlcyB0byB0aGUgdGl0bGUgb2YgdGhlIGFjdGl2aXR5XG4gICAgICBpZiAob2xkVmFsdWUpIHtcbiAgICAgICAgb2xkVmFsdWUudGl0bGUuY2hhbmdlZC5kaXNjb25uZWN0KG9uVGl0bGVDaGFuZ2VkKTtcbiAgICAgIH1cbiAgICAgIGlmIChuZXdWYWx1ZSkge1xuICAgICAgICBuZXdWYWx1ZS50aXRsZS5jaGFuZ2VkLmNvbm5lY3Qob25UaXRsZUNoYW5nZWQpO1xuICAgICAgfVxuXG4gICAgICAvLyBHcmFiIHRoZSBzZXNzaW9uIG9mZiBvZiB0aGUgY3VycmVudCB3aWRnZXQsIGlmIGl0IGV4aXN0cy5cbiAgICAgIGlmIChuZXdWYWx1ZSAmJiBjb25zb2xlVHJhY2tlci5oYXMobmV3VmFsdWUpKSB7XG4gICAgICAgIGN1cnJlbnRTZXNzaW9uID0gKG5ld1ZhbHVlIGFzIENvbnNvbGVQYW5lbCkuc2Vzc2lvbkNvbnRleHQ7XG4gICAgICB9IGVsc2UgaWYgKG5ld1ZhbHVlICYmIG5vdGVib29rVHJhY2tlci5oYXMobmV3VmFsdWUpKSB7XG4gICAgICAgIGN1cnJlbnRTZXNzaW9uID0gKG5ld1ZhbHVlIGFzIE5vdGVib29rUGFuZWwpLnNlc3Npb25Db250ZXh0O1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgY3VycmVudFNlc3Npb24gPSBudWxsO1xuICAgICAgfVxuICAgICAgaXRlbS5tb2RlbCEuc2Vzc2lvbkNvbnRleHQgPSBjdXJyZW50U2Vzc2lvbjtcbiAgICB9KTtcblxuICAgIHN0YXR1c0Jhci5yZWdpc3RlclN0YXR1c0l0ZW0oXG4gICAgICAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyLWV4dGVuc2lvbjprZXJuZWwtc3RhdHVzJyxcbiAgICAgIHtcbiAgICAgICAgaXRlbSxcbiAgICAgICAgYWxpZ246ICdsZWZ0JyxcbiAgICAgICAgcmFuazogMSxcbiAgICAgICAgaXNBY3RpdmU6ICgpID0+IHtcbiAgICAgICAgICBjb25zdCBjdXJyZW50ID0gbGFiU2hlbGwuY3VycmVudFdpZGdldDtcbiAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgISFjdXJyZW50ICYmXG4gICAgICAgICAgICAobm90ZWJvb2tUcmFja2VyLmhhcyhjdXJyZW50KSB8fCBjb25zb2xlVHJhY2tlci5oYXMoY3VycmVudCkpXG4gICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICk7XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gcHJvdmlkaW5nIGEgbGluZS9jb2x1bW4gc3RhdHVzIGl0ZW0gdG8gdGhlIGFwcGxpY2F0aW9uLlxuICovXG5leHBvcnQgY29uc3QgbGluZUNvbEl0ZW06IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9zdGF0dXNiYXItZXh0ZW5zaW9uOmxpbmUtY29sLXN0YXR1cycsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtcbiAgICBJU3RhdHVzQmFyLFxuICAgIElOb3RlYm9va1RyYWNrZXIsXG4gICAgSUVkaXRvclRyYWNrZXIsXG4gICAgSUNvbnNvbGVUcmFja2VyLFxuICAgIElMYWJTaGVsbCxcbiAgICBJVHJhbnNsYXRvclxuICBdLFxuICBhY3RpdmF0ZTogKFxuICAgIF86IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzdGF0dXNCYXI6IElTdGF0dXNCYXIsXG4gICAgbm90ZWJvb2tUcmFja2VyOiBJTm90ZWJvb2tUcmFja2VyLFxuICAgIGVkaXRvclRyYWNrZXI6IElFZGl0b3JUcmFja2VyLFxuICAgIGNvbnNvbGVUcmFja2VyOiBJQ29uc29sZVRyYWNrZXIsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApID0+IHtcbiAgICBjb25zdCBpdGVtID0gbmV3IExpbmVDb2wodHJhbnNsYXRvcik7XG5cbiAgICBjb25zdCBvbkFjdGl2ZUNlbGxDaGFuZ2VkID0gKG5vdGVib29rOiBOb3RlYm9vaywgY2VsbDogQ2VsbCkgPT4ge1xuICAgICAgaXRlbS5tb2RlbCEuZWRpdG9yID0gY2VsbCAmJiBjZWxsLmVkaXRvcjtcbiAgICB9O1xuXG4gICAgY29uc3Qgb25Qcm9tcHRDcmVhdGVkID0gKGNvbnNvbGU6IENvZGVDb25zb2xlLCBwcm9tcHQ6IENvZGVDZWxsKSA9PiB7XG4gICAgICBpdGVtLm1vZGVsIS5lZGl0b3IgPSBwcm9tcHQgJiYgcHJvbXB0LmVkaXRvcjtcbiAgICB9O1xuXG4gICAgbGFiU2hlbGwuY3VycmVudENoYW5nZWQuY29ubmVjdCgoXywgY2hhbmdlKSA9PiB7XG4gICAgICBjb25zdCB7IG9sZFZhbHVlLCBuZXdWYWx1ZSB9ID0gY2hhbmdlO1xuXG4gICAgICAvLyBDaGVjayBpZiB3ZSBuZWVkIHRvIGRpc2Nvbm5lY3QgdGhlIGNvbnNvbGUgbGlzdGVuZXJcbiAgICAgIC8vIG9yIHRoZSBub3RlYm9vayBhY3RpdmUgY2VsbCBsaXN0ZW5lclxuICAgICAgaWYgKG9sZFZhbHVlICYmIGNvbnNvbGVUcmFja2VyLmhhcyhvbGRWYWx1ZSkpIHtcbiAgICAgICAgKG9sZFZhbHVlIGFzIENvbnNvbGVQYW5lbCkuY29uc29sZS5wcm9tcHRDZWxsQ3JlYXRlZC5kaXNjb25uZWN0KFxuICAgICAgICAgIG9uUHJvbXB0Q3JlYXRlZFxuICAgICAgICApO1xuICAgICAgfSBlbHNlIGlmIChvbGRWYWx1ZSAmJiBub3RlYm9va1RyYWNrZXIuaGFzKG9sZFZhbHVlKSkge1xuICAgICAgICAob2xkVmFsdWUgYXMgTm90ZWJvb2tQYW5lbCkuY29udGVudC5hY3RpdmVDZWxsQ2hhbmdlZC5kaXNjb25uZWN0KFxuICAgICAgICAgIG9uQWN0aXZlQ2VsbENoYW5nZWRcbiAgICAgICAgKTtcbiAgICAgIH1cblxuICAgICAgLy8gV2lyZSB1cCB0aGUgbmV3IGVkaXRvciB0byB0aGUgbW9kZWwgaWYgaXQgZXhpc3RzXG4gICAgICBpZiAobmV3VmFsdWUgJiYgY29uc29sZVRyYWNrZXIuaGFzKG5ld1ZhbHVlKSkge1xuICAgICAgICAobmV3VmFsdWUgYXMgQ29uc29sZVBhbmVsKS5jb25zb2xlLnByb21wdENlbGxDcmVhdGVkLmNvbm5lY3QoXG4gICAgICAgICAgb25Qcm9tcHRDcmVhdGVkXG4gICAgICAgICk7XG4gICAgICAgIGNvbnN0IHByb21wdCA9IChuZXdWYWx1ZSBhcyBDb25zb2xlUGFuZWwpLmNvbnNvbGUucHJvbXB0Q2VsbDtcbiAgICAgICAgaXRlbS5tb2RlbCEuZWRpdG9yID0gcHJvbXB0ICYmIHByb21wdC5lZGl0b3I7XG4gICAgICB9IGVsc2UgaWYgKG5ld1ZhbHVlICYmIG5vdGVib29rVHJhY2tlci5oYXMobmV3VmFsdWUpKSB7XG4gICAgICAgIChuZXdWYWx1ZSBhcyBOb3RlYm9va1BhbmVsKS5jb250ZW50LmFjdGl2ZUNlbGxDaGFuZ2VkLmNvbm5lY3QoXG4gICAgICAgICAgb25BY3RpdmVDZWxsQ2hhbmdlZFxuICAgICAgICApO1xuICAgICAgICBjb25zdCBjZWxsID0gKG5ld1ZhbHVlIGFzIE5vdGVib29rUGFuZWwpLmNvbnRlbnQuYWN0aXZlQ2VsbDtcbiAgICAgICAgaXRlbS5tb2RlbCEuZWRpdG9yID0gY2VsbCAmJiBjZWxsLmVkaXRvcjtcbiAgICAgIH0gZWxzZSBpZiAobmV3VmFsdWUgJiYgZWRpdG9yVHJhY2tlci5oYXMobmV3VmFsdWUpKSB7XG4gICAgICAgIGl0ZW0ubW9kZWwhLmVkaXRvciA9IChuZXdWYWx1ZSBhcyBJRG9jdW1lbnRXaWRnZXQ8XG4gICAgICAgICAgRmlsZUVkaXRvclxuICAgICAgICA+KS5jb250ZW50LmVkaXRvcjtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGl0ZW0ubW9kZWwhLmVkaXRvciA9IG51bGw7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBBZGQgdGhlIHN0YXR1cyBpdGVtIHRvIHRoZSBzdGF0dXMgYmFyLlxuICAgIHN0YXR1c0Jhci5yZWdpc3RlclN0YXR1c0l0ZW0oXG4gICAgICAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyLWV4dGVuc2lvbjpsaW5lLWNvbC1zdGF0dXMnLFxuICAgICAge1xuICAgICAgICBpdGVtLFxuICAgICAgICBhbGlnbjogJ3JpZ2h0JyxcbiAgICAgICAgcmFuazogMixcbiAgICAgICAgaXNBY3RpdmU6ICgpID0+IHtcbiAgICAgICAgICBjb25zdCBjdXJyZW50ID0gbGFiU2hlbGwuY3VycmVudFdpZGdldDtcbiAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgISFjdXJyZW50ICYmXG4gICAgICAgICAgICAobm90ZWJvb2tUcmFja2VyLmhhcyhjdXJyZW50KSB8fFxuICAgICAgICAgICAgICBlZGl0b3JUcmFja2VyLmhhcyhjdXJyZW50KSB8fFxuICAgICAgICAgICAgICBjb25zb2xlVHJhY2tlci5oYXMoY3VycmVudCkpXG4gICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICk7XG4gIH1cbn07XG5cbi8qXG4gKiBBIHBsdWdpbiBwcm92aWRpbmcgcnVubmluZyB0ZXJtaW5hbHMgYW5kIHNlc3Npb25zIGluZm9ybWF0aW9uXG4gKiB0byB0aGUgc3RhdHVzIGJhci5cbiAqL1xuZXhwb3J0IGNvbnN0IHJ1bm5pbmdTZXNzaW9uc0l0ZW06IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9zdGF0dXNiYXItZXh0ZW5zaW9uOnJ1bm5pbmctc2Vzc2lvbnMtc3RhdHVzJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lTdGF0dXNCYXIsIElUcmFuc2xhdG9yXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzdGF0dXNCYXI6IElTdGF0dXNCYXIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKSA9PiB7XG4gICAgY29uc3QgaXRlbSA9IG5ldyBSdW5uaW5nU2Vzc2lvbnMoe1xuICAgICAgb25DbGljazogKCkgPT4gYXBwLnNoZWxsLmFjdGl2YXRlQnlJZCgnanAtcnVubmluZy1zZXNzaW9ucycpLFxuICAgICAgc2VydmljZU1hbmFnZXI6IGFwcC5zZXJ2aWNlTWFuYWdlcixcbiAgICAgIHRyYW5zbGF0b3JcbiAgICB9KTtcblxuICAgIHN0YXR1c0Jhci5yZWdpc3RlclN0YXR1c0l0ZW0oXG4gICAgICAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyLWV4dGVuc2lvbjpydW5uaW5nLXNlc3Npb25zLXN0YXR1cycsXG4gICAgICB7XG4gICAgICAgIGl0ZW0sXG4gICAgICAgIGFsaWduOiAnbGVmdCcsXG4gICAgICAgIHJhbms6IDBcbiAgICAgIH1cbiAgICApO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBzaW1wbGUgaW50ZXJmYWNlIG1vZGUgc3dpdGNoIGluIHRoZSBzdGF0dXMgYmFyLlxuICovXG5jb25zdCBtb2RlU3dpdGNoOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyLWV4dGVuc2lvbjptb2RlLXN3aXRjaCcsXG4gIHJlcXVpcmVzOiBbSUxhYlNoZWxsLCBJVHJhbnNsYXRvciwgSVN0YXR1c0Jhcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgc2hlbGw6IElMYWJTaGVsbCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBzdGF0dXNCYXI6IElTdGF0dXNCYXJcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBtb2RlU3dpdGNoID0gbmV3IFN3aXRjaCgpO1xuICAgIG1vZGVTd2l0Y2guaWQgPSAnanAtc2luZ2xlLWRvY3VtZW50LW1vZGUnO1xuXG4gICAgbW9kZVN3aXRjaC52YWx1ZUNoYW5nZWQuY29ubmVjdCgoXywgYXJncykgPT4ge1xuICAgICAgc2hlbGwubW9kZSA9IGFyZ3MubmV3VmFsdWUgPyAnc2luZ2xlLWRvY3VtZW50JyA6ICdtdWx0aXBsZS1kb2N1bWVudCc7XG4gICAgfSk7XG4gICAgc2hlbGwubW9kZUNoYW5nZWQuY29ubmVjdCgoXywgbW9kZSkgPT4ge1xuICAgICAgbW9kZVN3aXRjaC52YWx1ZSA9IG1vZGUgPT09ICdzaW5nbGUtZG9jdW1lbnQnO1xuICAgIH0pO1xuICAgIG1vZGVTd2l0Y2gudmFsdWUgPSBzaGVsbC5tb2RlID09PSAnc2luZ2xlLWRvY3VtZW50JztcblxuICAgIC8vIFNob3cgdGhlIGN1cnJlbnQgZmlsZSBicm93c2VyIHNob3J0Y3V0IGluIGl0cyB0aXRsZS5cbiAgICBjb25zdCB1cGRhdGVNb2RlU3dpdGNoVGl0bGUgPSAoKSA9PiB7XG4gICAgICBjb25zdCBiaW5kaW5nID0gYXBwLmNvbW1hbmRzLmtleUJpbmRpbmdzLmZpbmQoXG4gICAgICAgIGIgPT4gYi5jb21tYW5kID09PSAnYXBwbGljYXRpb246dG9nZ2xlLW1vZGUnXG4gICAgICApO1xuICAgICAgaWYgKGJpbmRpbmcpIHtcbiAgICAgICAgY29uc3Qga3MgPSBDb21tYW5kUmVnaXN0cnkuZm9ybWF0S2V5c3Ryb2tlKGJpbmRpbmcua2V5cy5qb2luKCcgJykpO1xuICAgICAgICBtb2RlU3dpdGNoLmNhcHRpb24gPSB0cmFucy5fXygnU2ltcGxlIEludGVyZmFjZSAoJTEpJywga3MpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgbW9kZVN3aXRjaC5jYXB0aW9uID0gdHJhbnMuX18oJ1NpbXBsZSBJbnRlcmZhY2UnKTtcbiAgICAgIH1cbiAgICB9O1xuICAgIHVwZGF0ZU1vZGVTd2l0Y2hUaXRsZSgpO1xuICAgIGFwcC5jb21tYW5kcy5rZXlCaW5kaW5nQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHVwZGF0ZU1vZGVTd2l0Y2hUaXRsZSgpO1xuICAgIH0pO1xuXG4gICAgbW9kZVN3aXRjaC5sYWJlbCA9IHRyYW5zLl9fKCdTaW1wbGUnKTtcblxuICAgIHN0YXR1c0Jhci5yZWdpc3RlclN0YXR1c0l0ZW0oXG4gICAgICAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyLWV4dGVuc2lvbjptb2RlLXN3aXRjaCcsXG4gICAgICB7XG4gICAgICAgIGl0ZW06IG1vZGVTd2l0Y2gsXG4gICAgICAgIGFsaWduOiAnbGVmdCcsXG4gICAgICAgIHJhbms6IC0xXG4gICAgICB9XG4gICAgKTtcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG5jb25zdCBwbHVnaW5zOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48YW55PltdID0gW1xuICBzdGF0dXNCYXIsXG4gIGxpbmVDb2xJdGVtLFxuICBrZXJuZWxTdGF0dXMsXG4gIHJ1bm5pbmdTZXNzaW9uc0l0ZW0sXG4gIG1vZGVTd2l0Y2hcbl07XG5cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG4iXSwic291cmNlUm9vdCI6IiJ9