(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_mainmenu-extension_lib_index_js"],{

/***/ "../packages/mainmenu-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/mainmenu-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "createEditMenu": () => (/* binding */ createEditMenu),
/* harmony export */   "createFileMenu": () => (/* binding */ createFileMenu),
/* harmony export */   "createKernelMenu": () => (/* binding */ createKernelMenu),
/* harmony export */   "createViewMenu": () => (/* binding */ createViewMenu),
/* harmony export */   "createRunMenu": () => (/* binding */ createRunMenu),
/* harmony export */   "createTabsMenu": () => (/* binding */ createTabsMenu),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_9__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mainmenu-extension
 */










const PLUGIN_ID = '@jupyterlab/mainmenu-extension:plugin';
/**
 * A namespace for command IDs of semantic extension points.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.openEdit = 'editmenu:open';
    CommandIDs.undo = 'editmenu:undo';
    CommandIDs.redo = 'editmenu:redo';
    CommandIDs.clearCurrent = 'editmenu:clear-current';
    CommandIDs.clearAll = 'editmenu:clear-all';
    CommandIDs.find = 'editmenu:find';
    CommandIDs.goToLine = 'editmenu:go-to-line';
    CommandIDs.openFile = 'filemenu:open';
    CommandIDs.closeAndCleanup = 'filemenu:close-and-cleanup';
    CommandIDs.createConsole = 'filemenu:create-console';
    CommandIDs.shutdown = 'filemenu:shutdown';
    CommandIDs.logout = 'filemenu:logout';
    CommandIDs.openKernel = 'kernelmenu:open';
    CommandIDs.interruptKernel = 'kernelmenu:interrupt';
    CommandIDs.reconnectToKernel = 'kernelmenu:reconnect-to-kernel';
    CommandIDs.restartKernel = 'kernelmenu:restart';
    CommandIDs.restartKernelAndClear = 'kernelmenu:restart-and-clear';
    CommandIDs.changeKernel = 'kernelmenu:change';
    CommandIDs.shutdownKernel = 'kernelmenu:shutdown';
    CommandIDs.shutdownAllKernels = 'kernelmenu:shutdownAll';
    CommandIDs.openView = 'viewmenu:open';
    CommandIDs.wordWrap = 'viewmenu:word-wrap';
    CommandIDs.lineNumbering = 'viewmenu:line-numbering';
    CommandIDs.matchBrackets = 'viewmenu:match-brackets';
    CommandIDs.openRun = 'runmenu:open';
    CommandIDs.run = 'runmenu:run';
    CommandIDs.runAll = 'runmenu:run-all';
    CommandIDs.restartAndRunAll = 'runmenu:restart-and-run-all';
    CommandIDs.runAbove = 'runmenu:run-above';
    CommandIDs.runBelow = 'runmenu:run-below';
    CommandIDs.openTabs = 'tabsmenu:open';
    CommandIDs.activateById = 'tabsmenu:activate-by-id';
    CommandIDs.activatePreviouslyUsedTab = 'tabsmenu:activate-previously-used-tab';
    CommandIDs.openSettings = 'settingsmenu:open';
    CommandIDs.openHelp = 'helpmenu:open';
    CommandIDs.openFirst = 'mainmenu:open-first';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing an interface to the main menu.
 */
const plugin = {
    id: PLUGIN_ID,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry],
    provides: _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
    activate: async (app, router, translator, palette, labShell, registry) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const menu = new _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.MainMenu(commands);
        menu.id = 'jp-MainMenu';
        menu.addClass('jp-scrollbar-tiny');
        // Built menu from settings
        if (registry) {
            await Private.loadSettingsMenu(registry, (aMenu) => {
                menu.addMenu(aMenu, { rank: aMenu.rank });
            }, options => _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.MainMenu.generateMenu(commands, options, trans), translator);
        }
        // Only add quit button if the back-end supports it by checking page config.
        const quitButton = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('quitButton').toLowerCase();
        menu.fileMenu.quitEntry = quitButton === 'true';
        // Create the application menus.
        createEditMenu(app, menu.editMenu, trans);
        createFileMenu(app, menu.fileMenu, router, trans);
        createKernelMenu(app, menu.kernelMenu, trans);
        createRunMenu(app, menu.runMenu, trans);
        createViewMenu(app, menu.viewMenu, trans);
        // The tabs menu relies on lab shell functionality.
        if (labShell) {
            createTabsMenu(app, menu.tabsMenu, labShell, trans);
        }
        // Create commands to open the main application menus.
        const activateMenu = (item) => {
            menu.activeMenu = item;
            menu.openActiveMenu();
        };
        commands.addCommand(CommandIDs.openEdit, {
            label: trans.__('Open Edit Menu'),
            execute: () => activateMenu(menu.editMenu)
        });
        commands.addCommand(CommandIDs.openFile, {
            label: trans.__('Open File Menu'),
            execute: () => activateMenu(menu.fileMenu)
        });
        commands.addCommand(CommandIDs.openKernel, {
            label: trans.__('Open Kernel Menu'),
            execute: () => activateMenu(menu.kernelMenu)
        });
        commands.addCommand(CommandIDs.openRun, {
            label: trans.__('Open Run Menu'),
            execute: () => activateMenu(menu.runMenu)
        });
        commands.addCommand(CommandIDs.openView, {
            label: trans.__('Open View Menu'),
            execute: () => activateMenu(menu.viewMenu)
        });
        commands.addCommand(CommandIDs.openSettings, {
            label: trans.__('Open Settings Menu'),
            execute: () => activateMenu(menu.settingsMenu)
        });
        commands.addCommand(CommandIDs.openTabs, {
            label: trans.__('Open Tabs Menu'),
            execute: () => activateMenu(menu.tabsMenu)
        });
        commands.addCommand(CommandIDs.openHelp, {
            label: trans.__('Open Help Menu'),
            execute: () => activateMenu(menu.helpMenu)
        });
        commands.addCommand(CommandIDs.openFirst, {
            label: trans.__('Open First Menu'),
            execute: () => {
                menu.activeIndex = 0;
                menu.openActiveMenu();
            }
        });
        if (palette) {
            // Add some of the commands defined here to the command palette.
            palette.addItem({
                command: CommandIDs.shutdown,
                category: trans.__('Main Area')
            });
            palette.addItem({
                command: CommandIDs.logout,
                category: trans.__('Main Area')
            });
            palette.addItem({
                command: CommandIDs.shutdownAllKernels,
                category: trans.__('Kernel Operations')
            });
            palette.addItem({
                command: CommandIDs.activatePreviouslyUsedTab,
                category: trans.__('Main Area')
            });
        }
        app.shell.add(menu, 'menu', { rank: 100 });
        return menu;
    }
};
/**
 * Create the basic `Edit` menu.
 */
function createEditMenu(app, menu, trans) {
    const commands = app.commands;
    // Add the undo/redo commands the the Edit menu.
    commands.addCommand(CommandIDs.undo, {
        label: trans.__('Undo'),
        isEnabled: Private.delegateEnabled(app, menu.undoers, 'undo'),
        execute: Private.delegateExecute(app, menu.undoers, 'undo')
    });
    commands.addCommand(CommandIDs.redo, {
        label: trans.__('Redo'),
        isEnabled: Private.delegateEnabled(app, menu.undoers, 'redo'),
        execute: Private.delegateExecute(app, menu.undoers, 'redo')
    });
    // Add the clear commands to the Edit menu.
    commands.addCommand(CommandIDs.clearCurrent, {
        label: () => {
            const enabled = Private.delegateEnabled(app, menu.clearers, 'clearCurrent')();
            let localizedLabel = trans.__('Clear');
            if (enabled) {
                localizedLabel = Private.delegateLabel(app, menu.clearers, 'clearCurrentLabel');
            }
            return localizedLabel;
        },
        isEnabled: Private.delegateEnabled(app, menu.clearers, 'clearCurrent'),
        execute: Private.delegateExecute(app, menu.clearers, 'clearCurrent')
    });
    commands.addCommand(CommandIDs.clearAll, {
        label: () => {
            const enabled = Private.delegateEnabled(app, menu.clearers, 'clearAll')();
            let localizedLabel = trans.__('Clear All');
            if (enabled) {
                localizedLabel = Private.delegateLabel(app, menu.clearers, 'clearAllLabel');
            }
            return localizedLabel;
        },
        isEnabled: Private.delegateEnabled(app, menu.clearers, 'clearAll'),
        execute: Private.delegateExecute(app, menu.clearers, 'clearAll')
    });
    commands.addCommand(CommandIDs.goToLine, {
        label: trans.__('Go to Line…'),
        isEnabled: Private.delegateEnabled(app, menu.goToLiners, 'goToLine'),
        execute: Private.delegateExecute(app, menu.goToLiners, 'goToLine')
    });
}
/**
 * Create the basic `File` menu.
 */
function createFileMenu(app, menu, router, trans) {
    const commands = app.commands;
    // Add a delegator command for closing and cleaning up an activity.
    // This one is a bit different, in that we consider it enabled
    // even if it cannot find a delegate for the activity.
    // In that case, we instead call the application `close` command.
    commands.addCommand(CommandIDs.closeAndCleanup, {
        label: () => {
            const localizedLabel = Private.delegateLabel(app, menu.closeAndCleaners, 'closeAndCleanupLabel');
            return localizedLabel ? localizedLabel : trans.__('Close and Shutdown');
        },
        isEnabled: () => !!app.shell.currentWidget && !!app.shell.currentWidget.title.closable,
        execute: () => {
            // Check if we have a registered delegate. If so, call that.
            if (Private.delegateEnabled(app, menu.closeAndCleaners, 'closeAndCleanup')()) {
                return Private.delegateExecute(app, menu.closeAndCleaners, 'closeAndCleanup')();
            }
            // If we have no delegate, call the top-level application close.
            return app.commands.execute('application:close');
        }
    });
    // Add a delegator command for creating a console for an activity.
    commands.addCommand(CommandIDs.createConsole, {
        label: () => {
            const localizedLabel = Private.delegateLabel(app, menu.consoleCreators, 'createConsoleLabel');
            return localizedLabel
                ? localizedLabel
                : trans.__('New Console for Activity');
        },
        isEnabled: Private.delegateEnabled(app, menu.consoleCreators, 'createConsole'),
        execute: Private.delegateExecute(app, menu.consoleCreators, 'createConsole')
    });
    commands.addCommand(CommandIDs.shutdown, {
        label: trans.__('Shut Down'),
        caption: trans.__('Shut down JupyterLab'),
        isVisible: () => menu.quitEntry,
        isEnabled: () => menu.quitEntry,
        execute: () => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shutdown confirmation'),
                body: trans.__('Please confirm you want to shut down JupyterLab.'),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Shut Down') })
                ]
            }).then(async (result) => {
                if (result.button.accept) {
                    const setting = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.makeSettings();
                    const apiURL = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(setting.baseUrl, 'api/shutdown');
                    // Shutdown all kernel and terminal sessions before shutting down the server
                    // If this fails, we continue execution so we can post an api/shutdown request
                    try {
                        await Promise.all([
                            app.serviceManager.sessions.shutdownAll(),
                            app.serviceManager.terminals.shutdownAll()
                        ]);
                    }
                    catch (e) {
                        // Do nothing
                        console.log(`Failed to shutdown sessions and terminals: ${e}`);
                    }
                    return _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.makeRequest(apiURL, { method: 'POST' }, setting)
                        .then(result => {
                        if (result.ok) {
                            // Close this window if the shutdown request has been successful
                            const body = document.createElement('div');
                            const p1 = document.createElement('p');
                            p1.textContent = trans.__('You have shut down the Jupyter server. You can now close this tab.');
                            const p2 = document.createElement('p');
                            p2.textContent = trans.__('To use JupyterLab again, you will need to relaunch it.');
                            body.appendChild(p1);
                            body.appendChild(p2);
                            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                                title: trans.__('Server stopped'),
                                body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__.Widget({ node: body }),
                                buttons: []
                            });
                            window.close();
                        }
                        else {
                            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.ResponseError(result);
                        }
                    })
                        .catch(data => {
                        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.NetworkError(data);
                    });
                }
            });
        }
    });
    commands.addCommand(CommandIDs.logout, {
        label: trans.__('Log Out'),
        caption: trans.__('Log out of JupyterLab'),
        isVisible: () => menu.quitEntry,
        isEnabled: () => menu.quitEntry,
        execute: () => {
            router.navigate('/logout', { hard: true });
        }
    });
}
/**
 * Create the basic `Kernel` menu.
 */
function createKernelMenu(app, menu, trans) {
    const commands = app.commands;
    commands.addCommand(CommandIDs.interruptKernel, {
        label: trans.__('Interrupt Kernel'),
        isEnabled: Private.delegateEnabled(app, menu.kernelUsers, 'interruptKernel'),
        execute: Private.delegateExecute(app, menu.kernelUsers, 'interruptKernel')
    });
    commands.addCommand(CommandIDs.reconnectToKernel, {
        label: trans.__('Reconnect to Kernel'),
        isEnabled: Private.delegateEnabled(app, menu.kernelUsers, 'reconnectToKernel'),
        execute: Private.delegateExecute(app, menu.kernelUsers, 'reconnectToKernel')
    });
    commands.addCommand(CommandIDs.restartKernel, {
        label: trans.__('Restart Kernel…'),
        isEnabled: Private.delegateEnabled(app, menu.kernelUsers, 'restartKernel'),
        execute: Private.delegateExecute(app, menu.kernelUsers, 'restartKernel')
    });
    commands.addCommand(CommandIDs.restartKernelAndClear, {
        label: () => {
            const enabled = Private.delegateEnabled(app, menu.kernelUsers, 'restartKernelAndClear')();
            let localizedLabel = trans.__('Restart Kernel and Clear…');
            if (enabled) {
                localizedLabel = Private.delegateLabel(app, menu.kernelUsers, 'restartKernelAndClearLabel');
            }
            return localizedLabel;
        },
        isEnabled: Private.delegateEnabled(app, menu.kernelUsers, 'restartKernelAndClear'),
        execute: Private.delegateExecute(app, menu.kernelUsers, 'restartKernelAndClear')
    });
    commands.addCommand(CommandIDs.changeKernel, {
        label: trans.__('Change Kernel…'),
        isEnabled: Private.delegateEnabled(app, menu.kernelUsers, 'changeKernel'),
        execute: Private.delegateExecute(app, menu.kernelUsers, 'changeKernel')
    });
    commands.addCommand(CommandIDs.shutdownKernel, {
        label: trans.__('Shut Down Kernel'),
        isEnabled: Private.delegateEnabled(app, menu.kernelUsers, 'shutdownKernel'),
        execute: Private.delegateExecute(app, menu.kernelUsers, 'shutdownKernel')
    });
    commands.addCommand(CommandIDs.shutdownAllKernels, {
        label: trans.__('Shut Down All Kernels…'),
        isEnabled: () => {
            return app.serviceManager.sessions.running().next() !== undefined;
        },
        execute: () => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shut Down All?'),
                body: trans.__('Shut down all kernels?'),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Dismiss') }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Shut Down All') })
                ]
            }).then(result => {
                if (result.button.accept) {
                    return app.serviceManager.sessions.shutdownAll();
                }
            });
        }
    });
}
/**
 * Create the basic `View` menu.
 */
function createViewMenu(app, menu, trans) {
    const commands = app.commands;
    commands.addCommand(CommandIDs.lineNumbering, {
        label: trans.__('Show Line Numbers'),
        isEnabled: Private.delegateEnabled(app, menu.editorViewers, 'toggleLineNumbers'),
        isToggled: Private.delegateToggled(app, menu.editorViewers, 'lineNumbersToggled'),
        execute: Private.delegateExecute(app, menu.editorViewers, 'toggleLineNumbers')
    });
    commands.addCommand(CommandIDs.matchBrackets, {
        label: trans.__('Match Brackets'),
        isEnabled: Private.delegateEnabled(app, menu.editorViewers, 'toggleMatchBrackets'),
        isToggled: Private.delegateToggled(app, menu.editorViewers, 'matchBracketsToggled'),
        execute: Private.delegateExecute(app, menu.editorViewers, 'toggleMatchBrackets')
    });
    commands.addCommand(CommandIDs.wordWrap, {
        label: trans.__('Wrap Words'),
        isEnabled: Private.delegateEnabled(app, menu.editorViewers, 'toggleWordWrap'),
        isToggled: Private.delegateToggled(app, menu.editorViewers, 'wordWrapToggled'),
        execute: Private.delegateExecute(app, menu.editorViewers, 'toggleWordWrap')
    });
}
/**
 * Create the basic `Run` menu.
 */
function createRunMenu(app, menu, trans) {
    const commands = app.commands;
    commands.addCommand(CommandIDs.run, {
        label: () => {
            const localizedLabel = Private.delegateLabel(app, menu.codeRunners, 'runLabel');
            const enabled = Private.delegateEnabled(app, menu.codeRunners, 'run')();
            return enabled ? localizedLabel : trans.__('Run Selected');
        },
        isEnabled: Private.delegateEnabled(app, menu.codeRunners, 'run'),
        execute: Private.delegateExecute(app, menu.codeRunners, 'run')
    });
    commands.addCommand(CommandIDs.runAll, {
        label: () => {
            let localizedLabel = trans.__('Run All');
            const enabled = Private.delegateEnabled(app, menu.codeRunners, 'runAll')();
            if (enabled) {
                localizedLabel = Private.delegateLabel(app, menu.codeRunners, 'runAllLabel');
            }
            return localizedLabel;
        },
        isEnabled: Private.delegateEnabled(app, menu.codeRunners, 'runAll'),
        execute: Private.delegateExecute(app, menu.codeRunners, 'runAll')
    });
    commands.addCommand(CommandIDs.restartAndRunAll, {
        label: () => {
            let localizedLabel = trans.__('Restart Kernel and Run All');
            const enabled = Private.delegateEnabled(app, menu.codeRunners, 'restartAndRunAll')();
            if (enabled) {
                localizedLabel = Private.delegateLabel(app, menu.codeRunners, 'restartAndRunAllLabel');
            }
            return localizedLabel;
        },
        isEnabled: Private.delegateEnabled(app, menu.codeRunners, 'restartAndRunAll'),
        execute: Private.delegateExecute(app, menu.codeRunners, 'restartAndRunAll')
    });
}
/**
 * Create the basic `Tabs` menu.
 */
function createTabsMenu(app, menu, labShell, trans) {
    const commands = app.commands;
    // A list of the active tabs in the main area.
    const tabGroup = [];
    // A disposable for getting rid of the out-of-date tabs list.
    let disposable;
    // Command to activate a widget by id.
    commands.addCommand(CommandIDs.activateById, {
        label: args => {
            const id = args['id'] || '';
            const widget = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__.find)(app.shell.widgets('main'), w => w.id === id);
            return (widget && widget.title.label) || '';
        },
        isToggled: args => {
            const id = args['id'] || '';
            return !!app.shell.currentWidget && app.shell.currentWidget.id === id;
        },
        execute: args => app.shell.activateById(args['id'] || '')
    });
    let previousId = '';
    // Command to toggle between the current
    // tab and the last modified tab.
    commands.addCommand(CommandIDs.activatePreviouslyUsedTab, {
        label: trans.__('Activate Previously Used Tab'),
        isEnabled: () => !!previousId,
        execute: () => commands.execute(CommandIDs.activateById, { id: previousId })
    });
    if (labShell) {
        void app.restored.then(() => {
            // Iterate over the current widgets in the
            // main area, and add them to the tab group
            // of the menu.
            const populateTabs = () => {
                // remove the previous tab list
                if (disposable && !disposable.isDisposed) {
                    disposable.dispose();
                }
                tabGroup.length = 0;
                let isPreviouslyUsedTabAttached = false;
                (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__.each)(app.shell.widgets('main'), widget => {
                    if (widget.id === previousId) {
                        isPreviouslyUsedTabAttached = true;
                    }
                    tabGroup.push({
                        command: CommandIDs.activateById,
                        args: { id: widget.id }
                    });
                });
                disposable = menu.addGroup(tabGroup, 1);
                previousId = isPreviouslyUsedTabAttached ? previousId : '';
            };
            populateTabs();
            labShell.layoutModified.connect(() => {
                populateTabs();
            });
            // Update the ID of the previous active tab if a new tab is selected.
            labShell.currentChanged.connect((_, args) => {
                const widget = args.oldValue;
                if (!widget) {
                    return;
                }
                previousId = widget.id;
            });
        });
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * A namespace for Private data.
 */
var Private;
(function (Private) {
    /**
     * Return the first value of the iterable that satisfies the predicate
     * function.
     */
    function find(it, predicate) {
        for (const value of it) {
            if (predicate(value)) {
                return value;
            }
        }
        return undefined;
    }
    /**
     * A utility function that delegates a portion of a label to an IMenuExtender.
     */
    function delegateLabel(app, s, label) {
        const widget = app.shell.currentWidget;
        const extender = widget
            ? find(s, value => value.tracker.has(widget))
            : undefined;
        if (!extender) {
            return '';
        }
        else {
            const count = extender.tracker.size;
            // Coerce the result to be a string. When Typedoc is updated to use
            // Typescript 2.8, we can possibly use conditional types to get Typescript
            // to recognize this is a string.
            return extender[label](count);
        }
    }
    Private.delegateLabel = delegateLabel;
    /**
     * A utility function that delegates command execution
     * to an IMenuExtender.
     */
    function delegateExecute(app, s, executor) {
        return () => {
            const widget = app.shell.currentWidget;
            const extender = widget
                ? find(s, value => value.tracker.has(widget))
                : undefined;
            if (!extender) {
                return Promise.resolve(void 0);
            }
            // Coerce the result to be a function. When Typedoc is updated to use
            // Typescript 2.8, we can possibly use conditional types to get Typescript
            // to recognize this is a function.
            const f = extender[executor];
            return f(widget);
        };
    }
    Private.delegateExecute = delegateExecute;
    /**
     * A utility function that delegates whether a command is enabled
     * to an IMenuExtender.
     */
    function delegateEnabled(app, s, executor) {
        return () => {
            const widget = app.shell.currentWidget;
            const extender = widget
                ? find(s, value => value.tracker.has(widget))
                : undefined;
            return (!!extender &&
                !!extender[executor] &&
                (extender.isEnabled && widget ? extender.isEnabled(widget) : true));
        };
    }
    Private.delegateEnabled = delegateEnabled;
    /**
     * A utility function that delegates whether a command is toggled
     * for an IMenuExtender.
     */
    function delegateToggled(app, s, toggled) {
        return () => {
            const widget = app.shell.currentWidget;
            const extender = widget
                ? find(s, value => value.tracker.has(widget))
                : undefined;
            // Coerce extender[toggled] to be a function. When Typedoc is updated to use
            // Typescript 2.8, we can possibly use conditional types to get Typescript
            // to recognize this is a function.
            return (!!extender &&
                !!extender[toggled] &&
                !!widget &&
                !!extender[toggled](widget));
        };
    }
    Private.delegateToggled = delegateToggled;
    async function displayInformation(trans) {
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Information'),
            body: trans.__('Menu customization has changed. You will need to reload JupyterLab to see the changes.'),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Reload') })
            ]
        });
        if (result.button.accept) {
            location.reload();
        }
    }
    async function loadSettingsMenu(registry, addMenu, menuFactory, translator) {
        var _a;
        const trans = translator.load('jupyterlab');
        let canonical;
        let loaded = {};
        /**
         * Populate the plugin's schema defaults.
         */
        function populate(schema) {
            var _a, _b;
            loaded = {};
            const pluginDefaults = Object.keys(registry.plugins)
                .map(plugin => {
                var _a, _b;
                const menus = (_b = (_a = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.main) !== null && _b !== void 0 ? _b : [];
                loaded[plugin] = menus;
                return menus;
            })
                .concat([(_b = (_a = schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.main) !== null && _b !== void 0 ? _b : []])
                .reduceRight((acc, val) => _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(acc, val, true), schema.properties.menus.default);
            // Apply default value as last step to take into account overrides.json
            // The standard default being [] as the plugin must use `jupyter.lab.menus.main`
            // to define their default value.
            schema.properties.menus.default = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(pluginDefaults, schema.properties.menus.default, true)
                // flatten one level
                .sort((a, b) => { var _a, _b; return ((_a = a.rank) !== null && _a !== void 0 ? _a : Infinity) - ((_b = b.rank) !== null && _b !== void 0 ? _b : Infinity); });
        }
        // Transform the plugin object to return different schema than the default.
        registry.transform(PLUGIN_ID, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.menus) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    menus: (_d = plugin.data.user.menus) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    menus: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(defaults, user.menus)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                return {
                    data: plugin.data,
                    id: plugin.id,
                    raw: plugin.raw,
                    schema: canonical,
                    version: plugin.version
                };
            }
        });
        // Repopulate the canonical variable after the setting registry has
        // preloaded all initial plugins.
        canonical = null;
        const settings = await registry.load(PLUGIN_ID);
        const currentMenus = (_a = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__.JSONExt.deepCopy(settings.composite.menus)) !== null && _a !== void 0 ? _a : [];
        const menus = new Array();
        // Create menu for non-disabled element
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.createMenus(currentMenus
            .filter(menu => !menu.disabled)
            .map(menu => {
            var _a;
            return Object.assign(Object.assign({}, menu), { items: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.filterDisabledItems((_a = menu.items) !== null && _a !== void 0 ? _a : []) });
        }), menuFactory).forEach(menu => {
            menus.push(menu);
            addMenu(menu);
        });
        settings.changed.connect(() => {
            var _a;
            // As extension may change menu through API, prompt the user to reload if the
            // menu has been updated.
            const newMenus = (_a = settings.composite.menus) !== null && _a !== void 0 ? _a : [];
            if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__.JSONExt.deepEqual(currentMenus, newMenus)) {
                void displayInformation(trans);
            }
        });
        registry.pluginChanged.connect(async (sender, plugin) => {
            var _a, _b, _c;
            if (plugin !== PLUGIN_ID) {
                // If the plugin changed its menu.
                const oldMenus = (_a = loaded[plugin]) !== null && _a !== void 0 ? _a : [];
                const newMenus = (_c = (_b = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _b === void 0 ? void 0 : _b.main) !== null && _c !== void 0 ? _c : [];
                if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__.JSONExt.deepEqual(oldMenus, newMenus)) {
                    if (loaded[plugin]) {
                        // The plugin has changed, request the user to reload the UI - this should not happen
                        await displayInformation(trans);
                    }
                    else {
                        // The plugin was not yet loaded when the menu was built => update the menu
                        loaded[plugin] = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__.JSONExt.deepCopy(newMenus);
                        // Merge potential disabled state
                        const toAdd = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(newMenus, currentMenus, false, false)
                            .filter(menu => !menu.disabled)
                            .map(menu => {
                            var _a;
                            return Object.assign(Object.assign({}, menu), { items: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.filterDisabledItems((_a = menu.items) !== null && _a !== void 0 ? _a : []) });
                        });
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.updateMenus(menus, toAdd, menuFactory).forEach(menu => {
                            addMenu(menu);
                        });
                    }
                }
            }
        });
    }
    Private.loadSettingsMenu = loadSettingsMenu;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFPOEI7QUFNSDtBQUM2QjtBQVk3QjtBQUMwQjtBQUN3QjtBQUNQO0FBQzFCO0FBQ0g7QUFFRztBQUUvQyxNQUFNLFNBQVMsR0FBRyx1Q0FBdUMsQ0FBQztBQUUxRDs7R0FFRztBQUNJLElBQVUsVUFBVSxDQXlFMUI7QUF6RUQsV0FBaUIsVUFBVTtJQUNaLG1CQUFRLEdBQUcsZUFBZSxDQUFDO0lBRTNCLGVBQUksR0FBRyxlQUFlLENBQUM7SUFFdkIsZUFBSSxHQUFHLGVBQWUsQ0FBQztJQUV2Qix1QkFBWSxHQUFHLHdCQUF3QixDQUFDO0lBRXhDLG1CQUFRLEdBQUcsb0JBQW9CLENBQUM7SUFFaEMsZUFBSSxHQUFHLGVBQWUsQ0FBQztJQUV2QixtQkFBUSxHQUFHLHFCQUFxQixDQUFDO0lBRWpDLG1CQUFRLEdBQUcsZUFBZSxDQUFDO0lBRTNCLDBCQUFlLEdBQUcsNEJBQTRCLENBQUM7SUFFL0Msd0JBQWEsR0FBRyx5QkFBeUIsQ0FBQztJQUUxQyxtQkFBUSxHQUFHLG1CQUFtQixDQUFDO0lBRS9CLGlCQUFNLEdBQUcsaUJBQWlCLENBQUM7SUFFM0IscUJBQVUsR0FBRyxpQkFBaUIsQ0FBQztJQUUvQiwwQkFBZSxHQUFHLHNCQUFzQixDQUFDO0lBRXpDLDRCQUFpQixHQUFHLGdDQUFnQyxDQUFDO0lBRXJELHdCQUFhLEdBQUcsb0JBQW9CLENBQUM7SUFFckMsZ0NBQXFCLEdBQUcsOEJBQThCLENBQUM7SUFFdkQsdUJBQVksR0FBRyxtQkFBbUIsQ0FBQztJQUVuQyx5QkFBYyxHQUFHLHFCQUFxQixDQUFDO0lBRXZDLDZCQUFr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QUMsTUFBTSxDQUFFLENBQUMsTUFBTSxDQUFDLG1CQUFtQixDQUFDLDBDQUFFLElBQUksbUNBQUksRUFBRSxDQUFDO2dCQUNwRSxJQUFJLENBQUMsZ0VBQWlCLENBQUMsUUFBUSxFQUFFLFFBQVEsQ0FBQyxFQUFFO29CQUMxQyxJQUFJLE1BQU0sQ0FBQyxNQUFNLENBQUMsRUFBRTt3QkFDbEIscUZBQXFGO3dCQUNyRixNQUFNLGtCQUFrQixDQUFDLEtBQUssQ0FBQyxDQUFDO3FCQUNqQzt5QkFBTTt3QkFDTCwyRUFBMkU7d0JBQzNFLE1BQU0sQ0FBQyxNQUFNLENBQUMsR0FBRywrREFBZ0IsQ0FBQyxRQUFRLENBQUMsQ0FBQzt3QkFDNUMsaUNBQWlDO3dCQUNqQyxNQUFNLEtBQUssR0FBRyx1RkFBOEIsQ0FDMUMsUUFBUSxFQUNSLFlBQVksRUFDWixLQUFLLEVBQ0wsS0FBSyxDQUNOOzZCQUNFLE1BQU0sQ0FBQyxJQUFJLENBQUMsRUFBRSxDQUFDLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQzs2QkFDOUIsR0FBRyxDQUFDLElBQUksQ0FBQyxFQUFFOzs0QkFDVix1Q0FDSyxJQUFJLEtBQ1AsS0FBSyxFQUFFLDRGQUFtQyxPQUFDLElBQUksQ0FBQyxLQUFLLG1DQUFJLEVBQUUsQ0FBQyxJQUM1RDt3QkFDSixDQUFDLENBQUMsQ0FBQzt3QkFFTCx5RUFBdUIsQ0FBQyxLQUFLLEVBQUUsS0FBSyxFQUFFLFdBQVcsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsRUFBRTs0QkFDaEUsT0FBTyxDQUFDLElBQUksQ0FBQyxDQUFDO3dCQUNoQixDQUFDLENBQUMsQ0FBQztxQkFDSjtpQkFDRjthQUNGO1FBQ0gsQ0FBQyxDQUFDLENBQUM7SUFDTCxDQUFDO0lBdEpxQix3QkFBZ0IsbUJBc0pyQztBQUNILENBQUMsRUEzUlMsT0FBTyxLQUFQLE9BQU8sUUEyUmhCIiwiZmlsZSI6InBhY2thZ2VzX21haW5tZW51LWV4dGVuc2lvbl9saWJfaW5kZXhfanMuOWMzMGQzNzEwODU5YTczZTUxMzYuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBtYWlubWVudS1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGFiU2hlbGwsXG4gIElSb3V0ZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIERpYWxvZyxcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBNZW51RmFjdG9yeSxcbiAgc2hvd0RpYWxvZ1xufSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBQYWdlQ29uZmlnLCBVUkxFeHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHtcbiAgSUVkaXRNZW51LFxuICBJRmlsZU1lbnUsXG4gIElLZXJuZWxNZW51LFxuICBJTWFpbk1lbnUsXG4gIElNZW51RXh0ZW5kZXIsXG4gIElSdW5NZW51LFxuICBJVGFic01lbnUsXG4gIElWaWV3TWVudSxcbiAgSnVweXRlckxhYk1lbnUsXG4gIE1haW5NZW51XG59IGZyb20gJ0BqdXB5dGVybGFiL21haW5tZW51JztcbmltcG9ydCB7IFNlcnZlckNvbm5lY3Rpb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5LCBTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIFRyYW5zbGF0aW9uQnVuZGxlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgZWFjaCwgZmluZCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IEpTT05FeHQgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBNZW51LCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG5jb25zdCBQTFVHSU5fSUQgPSAnQGp1cHl0ZXJsYWIvbWFpbm1lbnUtZXh0ZW5zaW9uOnBsdWdpbic7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGNvbW1hbmQgSURzIG9mIHNlbWFudGljIGV4dGVuc2lvbiBwb2ludHMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBvcGVuRWRpdCA9ICdlZGl0bWVudTpvcGVuJztcblxuICBleHBvcnQgY29uc3QgdW5kbyA9ICdlZGl0bWVudTp1bmRvJztcblxuICBleHBvcnQgY29uc3QgcmVkbyA9ICdlZGl0bWVudTpyZWRvJztcblxuICBleHBvcnQgY29uc3QgY2xlYXJDdXJyZW50ID0gJ2VkaXRtZW51OmNsZWFyLWN1cnJlbnQnO1xuXG4gIGV4cG9ydCBjb25zdCBjbGVhckFsbCA9ICdlZGl0bWVudTpjbGVhci1hbGwnO1xuXG4gIGV4cG9ydCBjb25zdCBmaW5kID0gJ2VkaXRtZW51OmZpbmQnO1xuXG4gIGV4cG9ydCBjb25zdCBnb1RvTGluZSA9ICdlZGl0bWVudTpnby10by1saW5lJztcblxuICBleHBvcnQgY29uc3Qgb3BlbkZpbGUgPSAnZmlsZW1lbnU6b3Blbic7XG5cbiAgZXhwb3J0IGNvbnN0IGNsb3NlQW5kQ2xlYW51cCA9ICdmaWxlbWVudTpjbG9zZS1hbmQtY2xlYW51cCc7XG5cbiAgZXhwb3J0IGNvbnN0IGNyZWF0ZUNvbnNvbGUgPSAnZmlsZW1lbnU6Y3JlYXRlLWNvbnNvbGUnO1xuXG4gIGV4cG9ydCBjb25zdCBzaHV0ZG93biA9ICdmaWxlbWVudTpzaHV0ZG93bic7XG5cbiAgZXhwb3J0IGNvbnN0IGxvZ291dCA9ICdmaWxlbWVudTpsb2dvdXQnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuS2VybmVsID0gJ2tlcm5lbG1lbnU6b3Blbic7XG5cbiAgZXhwb3J0IGNvbnN0IGludGVycnVwdEtlcm5lbCA9ICdrZXJuZWxtZW51OmludGVycnVwdCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlY29ubmVjdFRvS2VybmVsID0gJ2tlcm5lbG1lbnU6cmVjb25uZWN0LXRvLWtlcm5lbCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlc3RhcnRLZXJuZWwgPSAna2VybmVsbWVudTpyZXN0YXJ0JztcblxuICBleHBvcnQgY29uc3QgcmVzdGFydEtlcm5lbEFuZENsZWFyID0gJ2tlcm5lbG1lbnU6cmVzdGFydC1hbmQtY2xlYXInO1xuXG4gIGV4cG9ydCBjb25zdCBjaGFuZ2VLZXJuZWwgPSAna2VybmVsbWVudTpjaGFuZ2UnO1xuXG4gIGV4cG9ydCBjb25zdCBzaHV0ZG93bktlcm5lbCA9ICdrZXJuZWxtZW51OnNodXRkb3duJztcblxuICBleHBvcnQgY29uc3Qgc2h1dGRvd25BbGxLZXJuZWxzID0gJ2tlcm5lbG1lbnU6c2h1dGRvd25BbGwnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuVmlldyA9ICd2aWV3bWVudTpvcGVuJztcblxuICBleHBvcnQgY29uc3Qgd29yZFdyYXAgPSAndmlld21lbnU6d29yZC13cmFwJztcblxuICBleHBvcnQgY29uc3QgbGluZU51bWJlcmluZyA9ICd2aWV3bWVudTpsaW5lLW51bWJlcmluZyc7XG5cbiAgZXhwb3J0IGNvbnN0IG1hdGNoQnJhY2tldHMgPSAndmlld21lbnU6bWF0Y2gtYnJhY2tldHMnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuUnVuID0gJ3J1bm1lbnU6b3Blbic7XG5cbiAgZXhwb3J0IGNvbnN0IHJ1biA9ICdydW5tZW51OnJ1bic7XG5cbiAgZXhwb3J0IGNvbnN0IHJ1bkFsbCA9ICdydW5tZW51OnJ1bi1hbGwnO1xuXG4gIGV4cG9ydCBjb25zdCByZXN0YXJ0QW5kUnVuQWxsID0gJ3J1bm1lbnU6cmVzdGFydC1hbmQtcnVuLWFsbCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJ1bkFib3ZlID0gJ3J1bm1lbnU6cnVuLWFib3ZlJztcblxuICBleHBvcnQgY29uc3QgcnVuQmVsb3cgPSAncnVubWVudTpydW4tYmVsb3cnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuVGFicyA9ICd0YWJzbWVudTpvcGVuJztcblxuICBleHBvcnQgY29uc3QgYWN0aXZhdGVCeUlkID0gJ3RhYnNtZW51OmFjdGl2YXRlLWJ5LWlkJztcblxuICBleHBvcnQgY29uc3QgYWN0aXZhdGVQcmV2aW91c2x5VXNlZFRhYiA9XG4gICAgJ3RhYnNtZW51OmFjdGl2YXRlLXByZXZpb3VzbHktdXNlZC10YWInO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuU2V0dGluZ3MgPSAnc2V0dGluZ3NtZW51Om9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuSGVscCA9ICdoZWxwbWVudTpvcGVuJztcblxuICBleHBvcnQgY29uc3Qgb3BlbkZpcnN0ID0gJ21haW5tZW51Om9wZW4tZmlyc3QnO1xufVxuXG4vKipcbiAqIEEgc2VydmljZSBwcm92aWRpbmcgYW4gaW50ZXJmYWNlIHRvIHRoZSBtYWluIG1lbnUuXG4gKi9cbmNvbnN0IHBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElNYWluTWVudT4gPSB7XG4gIGlkOiBQTFVHSU5fSUQsXG4gIHJlcXVpcmVzOiBbSVJvdXRlciwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZSwgSUxhYlNoZWxsLCBJU2V0dGluZ1JlZ2lzdHJ5XSxcbiAgcHJvdmlkZXM6IElNYWluTWVudSxcbiAgYWN0aXZhdGU6IGFzeW5jIChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICByb3V0ZXI6IElSb3V0ZXIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsIHwgbnVsbCxcbiAgICByZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSB8IG51bGxcbiAgKTogUHJvbWlzZTxJTWFpbk1lbnU+ID0+IHtcbiAgICBjb25zdCB7IGNvbW1hbmRzIH0gPSBhcHA7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIGNvbnN0IG1lbnUgPSBuZXcgTWFpbk1lbnUoY29tbWFuZHMpO1xuICAgIG1lbnUuaWQgPSAnanAtTWFpbk1lbnUnO1xuICAgIG1lbnUuYWRkQ2xhc3MoJ2pwLXNjcm9sbGJhci10aW55Jyk7XG5cbiAgICAvLyBCdWlsdCBtZW51IGZyb20gc2V0dGluZ3NcbiAgICBpZiAocmVnaXN0cnkpIHtcbiAgICAgIGF3YWl0IFByaXZhdGUubG9hZFNldHRpbmdzTWVudShcbiAgICAgICAgcmVnaXN0cnksXG4gICAgICAgIChhTWVudTogSnVweXRlckxhYk1lbnUpID0+IHtcbiAgICAgICAgICBtZW51LmFkZE1lbnUoYU1lbnUsIHsgcmFuazogYU1lbnUucmFuayB9KTtcbiAgICAgICAgfSxcbiAgICAgICAgb3B0aW9ucyA9PiBNYWluTWVudS5nZW5lcmF0ZU1lbnUoY29tbWFuZHMsIG9wdGlvbnMsIHRyYW5zKSxcbiAgICAgICAgdHJhbnNsYXRvclxuICAgICAgKTtcbiAgICB9XG5cbiAgICAvLyBPbmx5IGFkZCBxdWl0IGJ1dHRvbiBpZiB0aGUgYmFjay1lbmQgc3VwcG9ydHMgaXQgYnkgY2hlY2tpbmcgcGFnZSBjb25maWcuXG4gICAgY29uc3QgcXVpdEJ1dHRvbiA9IFBhZ2VDb25maWcuZ2V0T3B0aW9uKCdxdWl0QnV0dG9uJykudG9Mb3dlckNhc2UoKTtcbiAgICBtZW51LmZpbGVNZW51LnF1aXRFbnRyeSA9IHF1aXRCdXR0b24gPT09ICd0cnVlJztcblxuICAgIC8vIENyZWF0ZSB0aGUgYXBwbGljYXRpb24gbWVudXMuXG4gICAgY3JlYXRlRWRpdE1lbnUoYXBwLCBtZW51LmVkaXRNZW51LCB0cmFucyk7XG4gICAgY3JlYXRlRmlsZU1lbnUoYXBwLCBtZW51LmZpbGVNZW51LCByb3V0ZXIsIHRyYW5zKTtcbiAgICBjcmVhdGVLZXJuZWxNZW51KGFwcCwgbWVudS5rZXJuZWxNZW51LCB0cmFucyk7XG4gICAgY3JlYXRlUnVuTWVudShhcHAsIG1lbnUucnVuTWVudSwgdHJhbnMpO1xuICAgIGNyZWF0ZVZpZXdNZW51KGFwcCwgbWVudS52aWV3TWVudSwgdHJhbnMpO1xuXG4gICAgLy8gVGhlIHRhYnMgbWVudSByZWxpZXMgb24gbGFiIHNoZWxsIGZ1bmN0aW9uYWxpdHkuXG4gICAgaWYgKGxhYlNoZWxsKSB7XG4gICAgICBjcmVhdGVUYWJzTWVudShhcHAsIG1lbnUudGFic01lbnUsIGxhYlNoZWxsLCB0cmFucyk7XG4gICAgfVxuXG4gICAgLy8gQ3JlYXRlIGNvbW1hbmRzIHRvIG9wZW4gdGhlIG1haW4gYXBwbGljYXRpb24gbWVudXMuXG4gICAgY29uc3QgYWN0aXZhdGVNZW51ID0gKGl0ZW06IE1lbnUpID0+IHtcbiAgICAgIG1lbnUuYWN0aXZlTWVudSA9IGl0ZW07XG4gICAgICBtZW51Lm9wZW5BY3RpdmVNZW51KCk7XG4gICAgfTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuRWRpdCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIEVkaXQgTWVudScpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4gYWN0aXZhdGVNZW51KG1lbnUuZWRpdE1lbnUpXG4gICAgfSk7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW5GaWxlLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ09wZW4gRmlsZSBNZW51JyksXG4gICAgICBleGVjdXRlOiAoKSA9PiBhY3RpdmF0ZU1lbnUobWVudS5maWxlTWVudSlcbiAgICB9KTtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3Blbktlcm5lbCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIEtlcm5lbCBNZW51JyksXG4gICAgICBleGVjdXRlOiAoKSA9PiBhY3RpdmF0ZU1lbnUobWVudS5rZXJuZWxNZW51KVxuICAgIH0pO1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuUnVuLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ09wZW4gUnVuIE1lbnUnKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IGFjdGl2YXRlTWVudShtZW51LnJ1bk1lbnUpXG4gICAgfSk7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW5WaWV3LCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ09wZW4gVmlldyBNZW51JyksXG4gICAgICBleGVjdXRlOiAoKSA9PiBhY3RpdmF0ZU1lbnUobWVudS52aWV3TWVudSlcbiAgICB9KTtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3BlblNldHRpbmdzLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ09wZW4gU2V0dGluZ3MgTWVudScpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4gYWN0aXZhdGVNZW51KG1lbnUuc2V0dGluZ3NNZW51KVxuICAgIH0pO1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuVGFicywge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIFRhYnMgTWVudScpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4gYWN0aXZhdGVNZW51KG1lbnUudGFic01lbnUpXG4gICAgfSk7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW5IZWxwLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ09wZW4gSGVscCBNZW51JyksXG4gICAgICBleGVjdXRlOiAoKSA9PiBhY3RpdmF0ZU1lbnUobWVudS5oZWxwTWVudSlcbiAgICB9KTtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3BlbkZpcnN0LCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ09wZW4gRmlyc3QgTWVudScpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBtZW51LmFjdGl2ZUluZGV4ID0gMDtcbiAgICAgICAgbWVudS5vcGVuQWN0aXZlTWVudSgpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgIC8vIEFkZCBzb21lIG9mIHRoZSBjb21tYW5kcyBkZWZpbmVkIGhlcmUgdG8gdGhlIGNvbW1hbmQgcGFsZXR0ZS5cbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuc2h1dGRvd24sXG4gICAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnTWFpbiBBcmVhJylcbiAgICAgIH0pO1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5sb2dvdXQsXG4gICAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnTWFpbiBBcmVhJylcbiAgICAgIH0pO1xuXG4gICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLnNodXRkb3duQWxsS2VybmVscyxcbiAgICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdLZXJuZWwgT3BlcmF0aW9ucycpXG4gICAgICB9KTtcblxuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5hY3RpdmF0ZVByZXZpb3VzbHlVc2VkVGFiLFxuICAgICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ01haW4gQXJlYScpXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBhcHAuc2hlbGwuYWRkKG1lbnUsICdtZW51JywgeyByYW5rOiAxMDAgfSk7XG5cbiAgICByZXR1cm4gbWVudTtcbiAgfVxufTtcblxuLyoqXG4gKiBDcmVhdGUgdGhlIGJhc2ljIGBFZGl0YCBtZW51LlxuICovXG5leHBvcnQgZnVuY3Rpb24gY3JlYXRlRWRpdE1lbnUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBtZW51OiBJRWRpdE1lbnUsXG4gIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuKTogdm9pZCB7XG4gIGNvbnN0IGNvbW1hbmRzID0gYXBwLmNvbW1hbmRzO1xuXG4gIC8vIEFkZCB0aGUgdW5kby9yZWRvIGNvbW1hbmRzIHRoZSB0aGUgRWRpdCBtZW51LlxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMudW5kbywge1xuICAgIGxhYmVsOiB0cmFucy5fXygnVW5kbycpLFxuICAgIGlzRW5hYmxlZDogUHJpdmF0ZS5kZWxlZ2F0ZUVuYWJsZWQoYXBwLCBtZW51LnVuZG9lcnMsICd1bmRvJyksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoYXBwLCBtZW51LnVuZG9lcnMsICd1bmRvJylcbiAgfSk7XG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZWRvLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSZWRvJyksXG4gICAgaXNFbmFibGVkOiBQcml2YXRlLmRlbGVnYXRlRW5hYmxlZChhcHAsIG1lbnUudW5kb2VycywgJ3JlZG8nKSxcbiAgICBleGVjdXRlOiBQcml2YXRlLmRlbGVnYXRlRXhlY3V0ZShhcHAsIG1lbnUudW5kb2VycywgJ3JlZG8nKVxuICB9KTtcblxuICAvLyBBZGQgdGhlIGNsZWFyIGNvbW1hbmRzIHRvIHRoZSBFZGl0IG1lbnUuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jbGVhckN1cnJlbnQsIHtcbiAgICBsYWJlbDogKCkgPT4ge1xuICAgICAgY29uc3QgZW5hYmxlZCA9IFByaXZhdGUuZGVsZWdhdGVFbmFibGVkKFxuICAgICAgICBhcHAsXG4gICAgICAgIG1lbnUuY2xlYXJlcnMsXG4gICAgICAgICdjbGVhckN1cnJlbnQnXG4gICAgICApKCk7XG4gICAgICBsZXQgbG9jYWxpemVkTGFiZWwgPSB0cmFucy5fXygnQ2xlYXInKTtcbiAgICAgIGlmIChlbmFibGVkKSB7XG4gICAgICAgIGxvY2FsaXplZExhYmVsID0gUHJpdmF0ZS5kZWxlZ2F0ZUxhYmVsKFxuICAgICAgICAgIGFwcCxcbiAgICAgICAgICBtZW51LmNsZWFyZXJzLFxuICAgICAgICAgICdjbGVhckN1cnJlbnRMYWJlbCdcbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBsb2NhbGl6ZWRMYWJlbDtcbiAgICB9LFxuICAgIGlzRW5hYmxlZDogUHJpdmF0ZS5kZWxlZ2F0ZUVuYWJsZWQoYXBwLCBtZW51LmNsZWFyZXJzLCAnY2xlYXJDdXJyZW50JyksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoYXBwLCBtZW51LmNsZWFyZXJzLCAnY2xlYXJDdXJyZW50JylcbiAgfSk7XG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jbGVhckFsbCwge1xuICAgIGxhYmVsOiAoKSA9PiB7XG4gICAgICBjb25zdCBlbmFibGVkID0gUHJpdmF0ZS5kZWxlZ2F0ZUVuYWJsZWQoYXBwLCBtZW51LmNsZWFyZXJzLCAnY2xlYXJBbGwnKSgpO1xuICAgICAgbGV0IGxvY2FsaXplZExhYmVsID0gdHJhbnMuX18oJ0NsZWFyIEFsbCcpO1xuICAgICAgaWYgKGVuYWJsZWQpIHtcbiAgICAgICAgbG9jYWxpemVkTGFiZWwgPSBQcml2YXRlLmRlbGVnYXRlTGFiZWwoXG4gICAgICAgICAgYXBwLFxuICAgICAgICAgIG1lbnUuY2xlYXJlcnMsXG4gICAgICAgICAgJ2NsZWFyQWxsTGFiZWwnXG4gICAgICAgICk7XG4gICAgICB9XG4gICAgICByZXR1cm4gbG9jYWxpemVkTGFiZWw7XG4gICAgfSxcbiAgICBpc0VuYWJsZWQ6IFByaXZhdGUuZGVsZWdhdGVFbmFibGVkKGFwcCwgbWVudS5jbGVhcmVycywgJ2NsZWFyQWxsJyksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoYXBwLCBtZW51LmNsZWFyZXJzLCAnY2xlYXJBbGwnKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuZ29Ub0xpbmUsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0dvIHRvIExpbmXigKYnKSxcbiAgICBpc0VuYWJsZWQ6IFByaXZhdGUuZGVsZWdhdGVFbmFibGVkKGFwcCwgbWVudS5nb1RvTGluZXJzLCAnZ29Ub0xpbmUnKSxcbiAgICBleGVjdXRlOiBQcml2YXRlLmRlbGVnYXRlRXhlY3V0ZShhcHAsIG1lbnUuZ29Ub0xpbmVycywgJ2dvVG9MaW5lJylcbiAgfSk7XG59XG5cbi8qKlxuICogQ3JlYXRlIHRoZSBiYXNpYyBgRmlsZWAgbWVudS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZUZpbGVNZW51KFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgbWVudTogSUZpbGVNZW51LFxuICByb3V0ZXI6IElSb3V0ZXIsXG4gIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuKTogdm9pZCB7XG4gIGNvbnN0IGNvbW1hbmRzID0gYXBwLmNvbW1hbmRzO1xuXG4gIC8vIEFkZCBhIGRlbGVnYXRvciBjb21tYW5kIGZvciBjbG9zaW5nIGFuZCBjbGVhbmluZyB1cCBhbiBhY3Rpdml0eS5cbiAgLy8gVGhpcyBvbmUgaXMgYSBiaXQgZGlmZmVyZW50LCBpbiB0aGF0IHdlIGNvbnNpZGVyIGl0IGVuYWJsZWRcbiAgLy8gZXZlbiBpZiBpdCBjYW5ub3QgZmluZCBhIGRlbGVnYXRlIGZvciB0aGUgYWN0aXZpdHkuXG4gIC8vIEluIHRoYXQgY2FzZSwgd2UgaW5zdGVhZCBjYWxsIHRoZSBhcHBsaWNhdGlvbiBgY2xvc2VgIGNvbW1hbmQuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jbG9zZUFuZENsZWFudXAsIHtcbiAgICBsYWJlbDogKCkgPT4ge1xuICAgICAgY29uc3QgbG9jYWxpemVkTGFiZWwgPSBQcml2YXRlLmRlbGVnYXRlTGFiZWwoXG4gICAgICAgIGFwcCxcbiAgICAgICAgbWVudS5jbG9zZUFuZENsZWFuZXJzLFxuICAgICAgICAnY2xvc2VBbmRDbGVhbnVwTGFiZWwnXG4gICAgICApO1xuICAgICAgcmV0dXJuIGxvY2FsaXplZExhYmVsID8gbG9jYWxpemVkTGFiZWwgOiB0cmFucy5fXygnQ2xvc2UgYW5kIFNodXRkb3duJyk7XG4gICAgfSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+XG4gICAgICAhIWFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0ICYmICEhYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQudGl0bGUuY2xvc2FibGUsXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgLy8gQ2hlY2sgaWYgd2UgaGF2ZSBhIHJlZ2lzdGVyZWQgZGVsZWdhdGUuIElmIHNvLCBjYWxsIHRoYXQuXG4gICAgICBpZiAoXG4gICAgICAgIFByaXZhdGUuZGVsZWdhdGVFbmFibGVkKGFwcCwgbWVudS5jbG9zZUFuZENsZWFuZXJzLCAnY2xvc2VBbmRDbGVhbnVwJykoKVxuICAgICAgKSB7XG4gICAgICAgIHJldHVybiBQcml2YXRlLmRlbGVnYXRlRXhlY3V0ZShcbiAgICAgICAgICBhcHAsXG4gICAgICAgICAgbWVudS5jbG9zZUFuZENsZWFuZXJzLFxuICAgICAgICAgICdjbG9zZUFuZENsZWFudXAnXG4gICAgICAgICkoKTtcbiAgICAgIH1cbiAgICAgIC8vIElmIHdlIGhhdmUgbm8gZGVsZWdhdGUsIGNhbGwgdGhlIHRvcC1sZXZlbCBhcHBsaWNhdGlvbiBjbG9zZS5cbiAgICAgIHJldHVybiBhcHAuY29tbWFuZHMuZXhlY3V0ZSgnYXBwbGljYXRpb246Y2xvc2UnKTtcbiAgICB9XG4gIH0pO1xuXG4gIC8vIEFkZCBhIGRlbGVnYXRvciBjb21tYW5kIGZvciBjcmVhdGluZyBhIGNvbnNvbGUgZm9yIGFuIGFjdGl2aXR5LlxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY3JlYXRlQ29uc29sZSwge1xuICAgIGxhYmVsOiAoKSA9PiB7XG4gICAgICBjb25zdCBsb2NhbGl6ZWRMYWJlbCA9IFByaXZhdGUuZGVsZWdhdGVMYWJlbChcbiAgICAgICAgYXBwLFxuICAgICAgICBtZW51LmNvbnNvbGVDcmVhdG9ycyxcbiAgICAgICAgJ2NyZWF0ZUNvbnNvbGVMYWJlbCdcbiAgICAgICk7XG4gICAgICByZXR1cm4gbG9jYWxpemVkTGFiZWxcbiAgICAgICAgPyBsb2NhbGl6ZWRMYWJlbFxuICAgICAgICA6IHRyYW5zLl9fKCdOZXcgQ29uc29sZSBmb3IgQWN0aXZpdHknKTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZDogUHJpdmF0ZS5kZWxlZ2F0ZUVuYWJsZWQoXG4gICAgICBhcHAsXG4gICAgICBtZW51LmNvbnNvbGVDcmVhdG9ycyxcbiAgICAgICdjcmVhdGVDb25zb2xlJ1xuICAgICksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoYXBwLCBtZW51LmNvbnNvbGVDcmVhdG9ycywgJ2NyZWF0ZUNvbnNvbGUnKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2h1dGRvd24sIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1NodXQgRG93bicpLFxuICAgIGNhcHRpb246IHRyYW5zLl9fKCdTaHV0IGRvd24gSnVweXRlckxhYicpLFxuICAgIGlzVmlzaWJsZTogKCkgPT4gbWVudS5xdWl0RW50cnksXG4gICAgaXNFbmFibGVkOiAoKSA9PiBtZW51LnF1aXRFbnRyeSxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICAgIHRpdGxlOiB0cmFucy5fXygnU2h1dGRvd24gY29uZmlybWF0aW9uJyksXG4gICAgICAgIGJvZHk6IHRyYW5zLl9fKCdQbGVhc2UgY29uZmlybSB5b3Ugd2FudCB0byBzaHV0IGRvd24gSnVweXRlckxhYi4nKSxcbiAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oKSxcbiAgICAgICAgICBEaWFsb2cud2FybkJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duJykgfSlcbiAgICAgICAgXVxuICAgICAgfSkudGhlbihhc3luYyByZXN1bHQgPT4ge1xuICAgICAgICBpZiAocmVzdWx0LmJ1dHRvbi5hY2NlcHQpIHtcbiAgICAgICAgICBjb25zdCBzZXR0aW5nID0gU2VydmVyQ29ubmVjdGlvbi5tYWtlU2V0dGluZ3MoKTtcbiAgICAgICAgICBjb25zdCBhcGlVUkwgPSBVUkxFeHQuam9pbihzZXR0aW5nLmJhc2VVcmwsICdhcGkvc2h1dGRvd24nKTtcblxuICAgICAgICAgIC8vIFNodXRkb3duIGFsbCBrZXJuZWwgYW5kIHRlcm1pbmFsIHNlc3Npb25zIGJlZm9yZSBzaHV0dGluZyBkb3duIHRoZSBzZXJ2ZXJcbiAgICAgICAgICAvLyBJZiB0aGlzIGZhaWxzLCB3ZSBjb250aW51ZSBleGVjdXRpb24gc28gd2UgY2FuIHBvc3QgYW4gYXBpL3NodXRkb3duIHJlcXVlc3RcbiAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgYXdhaXQgUHJvbWlzZS5hbGwoW1xuICAgICAgICAgICAgICBhcHAuc2VydmljZU1hbmFnZXIuc2Vzc2lvbnMuc2h1dGRvd25BbGwoKSxcbiAgICAgICAgICAgICAgYXBwLnNlcnZpY2VNYW5hZ2VyLnRlcm1pbmFscy5zaHV0ZG93bkFsbCgpXG4gICAgICAgICAgICBdKTtcbiAgICAgICAgICB9IGNhdGNoIChlKSB7XG4gICAgICAgICAgICAvLyBEbyBub3RoaW5nXG4gICAgICAgICAgICBjb25zb2xlLmxvZyhgRmFpbGVkIHRvIHNodXRkb3duIHNlc3Npb25zIGFuZCB0ZXJtaW5hbHM6ICR7ZX1gKTtcbiAgICAgICAgICB9XG5cbiAgICAgICAgICByZXR1cm4gU2VydmVyQ29ubmVjdGlvbi5tYWtlUmVxdWVzdChcbiAgICAgICAgICAgIGFwaVVSTCxcbiAgICAgICAgICAgIHsgbWV0aG9kOiAnUE9TVCcgfSxcbiAgICAgICAgICAgIHNldHRpbmdcbiAgICAgICAgICApXG4gICAgICAgICAgICAudGhlbihyZXN1bHQgPT4ge1xuICAgICAgICAgICAgICBpZiAocmVzdWx0Lm9rKSB7XG4gICAgICAgICAgICAgICAgLy8gQ2xvc2UgdGhpcyB3aW5kb3cgaWYgdGhlIHNodXRkb3duIHJlcXVlc3QgaGFzIGJlZW4gc3VjY2Vzc2Z1bFxuICAgICAgICAgICAgICAgIGNvbnN0IGJvZHkgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICAgICAgICAgICAgICBjb25zdCBwMSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ3AnKTtcbiAgICAgICAgICAgICAgICBwMS50ZXh0Q29udGVudCA9IHRyYW5zLl9fKFxuICAgICAgICAgICAgICAgICAgJ1lvdSBoYXZlIHNodXQgZG93biB0aGUgSnVweXRlciBzZXJ2ZXIuIFlvdSBjYW4gbm93IGNsb3NlIHRoaXMgdGFiLidcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIGNvbnN0IHAyID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgncCcpO1xuICAgICAgICAgICAgICAgIHAyLnRleHRDb250ZW50ID0gdHJhbnMuX18oXG4gICAgICAgICAgICAgICAgICAnVG8gdXNlIEp1cHl0ZXJMYWIgYWdhaW4sIHlvdSB3aWxsIG5lZWQgdG8gcmVsYXVuY2ggaXQuJ1xuICAgICAgICAgICAgICAgICk7XG5cbiAgICAgICAgICAgICAgICBib2R5LmFwcGVuZENoaWxkKHAxKTtcbiAgICAgICAgICAgICAgICBib2R5LmFwcGVuZENoaWxkKHAyKTtcbiAgICAgICAgICAgICAgICB2b2lkIHNob3dEaWFsb2coe1xuICAgICAgICAgICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdTZXJ2ZXIgc3RvcHBlZCcpLFxuICAgICAgICAgICAgICAgICAgYm9keTogbmV3IFdpZGdldCh7IG5vZGU6IGJvZHkgfSksXG4gICAgICAgICAgICAgICAgICBidXR0b25zOiBbXVxuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICAgIHdpbmRvdy5jbG9zZSgpO1xuICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHRocm93IG5ldyBTZXJ2ZXJDb25uZWN0aW9uLlJlc3BvbnNlRXJyb3IocmVzdWx0KTtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSlcbiAgICAgICAgICAgIC5jYXRjaChkYXRhID0+IHtcbiAgICAgICAgICAgICAgdGhyb3cgbmV3IFNlcnZlckNvbm5lY3Rpb24uTmV0d29ya0Vycm9yKGRhdGEpO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmxvZ291dCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnTG9nIE91dCcpLFxuICAgIGNhcHRpb246IHRyYW5zLl9fKCdMb2cgb3V0IG9mIEp1cHl0ZXJMYWInKSxcbiAgICBpc1Zpc2libGU6ICgpID0+IG1lbnUucXVpdEVudHJ5LFxuICAgIGlzRW5hYmxlZDogKCkgPT4gbWVudS5xdWl0RW50cnksXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgcm91dGVyLm5hdmlnYXRlKCcvbG9nb3V0JywgeyBoYXJkOiB0cnVlIH0pO1xuICAgIH1cbiAgfSk7XG59XG5cbi8qKlxuICogQ3JlYXRlIHRoZSBiYXNpYyBgS2VybmVsYCBtZW51LlxuICovXG5leHBvcnQgZnVuY3Rpb24gY3JlYXRlS2VybmVsTWVudShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIG1lbnU6IElLZXJuZWxNZW51LFxuICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGVcbik6IHZvaWQge1xuICBjb25zdCBjb21tYW5kcyA9IGFwcC5jb21tYW5kcztcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaW50ZXJydXB0S2VybmVsLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdJbnRlcnJ1cHQgS2VybmVsJyksXG4gICAgaXNFbmFibGVkOiBQcml2YXRlLmRlbGVnYXRlRW5hYmxlZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUua2VybmVsVXNlcnMsXG4gICAgICAnaW50ZXJydXB0S2VybmVsJ1xuICAgICksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoYXBwLCBtZW51Lmtlcm5lbFVzZXJzLCAnaW50ZXJydXB0S2VybmVsJylcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJlY29ubmVjdFRvS2VybmVsLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSZWNvbm5lY3QgdG8gS2VybmVsJyksXG4gICAgaXNFbmFibGVkOiBQcml2YXRlLmRlbGVnYXRlRW5hYmxlZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUua2VybmVsVXNlcnMsXG4gICAgICAncmVjb25uZWN0VG9LZXJuZWwnXG4gICAgKSxcbiAgICBleGVjdXRlOiBQcml2YXRlLmRlbGVnYXRlRXhlY3V0ZShhcHAsIG1lbnUua2VybmVsVXNlcnMsICdyZWNvbm5lY3RUb0tlcm5lbCcpXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZXN0YXJ0S2VybmVsLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSZXN0YXJ0IEtlcm5lbOKApicpLFxuICAgIGlzRW5hYmxlZDogUHJpdmF0ZS5kZWxlZ2F0ZUVuYWJsZWQoYXBwLCBtZW51Lmtlcm5lbFVzZXJzLCAncmVzdGFydEtlcm5lbCcpLFxuICAgIGV4ZWN1dGU6IFByaXZhdGUuZGVsZWdhdGVFeGVjdXRlKGFwcCwgbWVudS5rZXJuZWxVc2VycywgJ3Jlc3RhcnRLZXJuZWwnKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVzdGFydEtlcm5lbEFuZENsZWFyLCB7XG4gICAgbGFiZWw6ICgpID0+IHtcbiAgICAgIGNvbnN0IGVuYWJsZWQgPSBQcml2YXRlLmRlbGVnYXRlRW5hYmxlZChcbiAgICAgICAgYXBwLFxuICAgICAgICBtZW51Lmtlcm5lbFVzZXJzLFxuICAgICAgICAncmVzdGFydEtlcm5lbEFuZENsZWFyJ1xuICAgICAgKSgpO1xuICAgICAgbGV0IGxvY2FsaXplZExhYmVsID0gdHJhbnMuX18oJ1Jlc3RhcnQgS2VybmVsIGFuZCBDbGVhcuKApicpO1xuICAgICAgaWYgKGVuYWJsZWQpIHtcbiAgICAgICAgbG9jYWxpemVkTGFiZWwgPSBQcml2YXRlLmRlbGVnYXRlTGFiZWwoXG4gICAgICAgICAgYXBwLFxuICAgICAgICAgIG1lbnUua2VybmVsVXNlcnMsXG4gICAgICAgICAgJ3Jlc3RhcnRLZXJuZWxBbmRDbGVhckxhYmVsJ1xuICAgICAgICApO1xuICAgICAgfVxuICAgICAgcmV0dXJuIGxvY2FsaXplZExhYmVsO1xuICAgIH0sXG4gICAgaXNFbmFibGVkOiBQcml2YXRlLmRlbGVnYXRlRW5hYmxlZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUua2VybmVsVXNlcnMsXG4gICAgICAncmVzdGFydEtlcm5lbEFuZENsZWFyJ1xuICAgICksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoXG4gICAgICBhcHAsXG4gICAgICBtZW51Lmtlcm5lbFVzZXJzLFxuICAgICAgJ3Jlc3RhcnRLZXJuZWxBbmRDbGVhcidcbiAgICApXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jaGFuZ2VLZXJuZWwsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0NoYW5nZSBLZXJuZWzigKYnKSxcbiAgICBpc0VuYWJsZWQ6IFByaXZhdGUuZGVsZWdhdGVFbmFibGVkKGFwcCwgbWVudS5rZXJuZWxVc2VycywgJ2NoYW5nZUtlcm5lbCcpLFxuICAgIGV4ZWN1dGU6IFByaXZhdGUuZGVsZWdhdGVFeGVjdXRlKGFwcCwgbWVudS5rZXJuZWxVc2VycywgJ2NoYW5nZUtlcm5lbCcpXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zaHV0ZG93bktlcm5lbCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duIEtlcm5lbCcpLFxuICAgIGlzRW5hYmxlZDogUHJpdmF0ZS5kZWxlZ2F0ZUVuYWJsZWQoYXBwLCBtZW51Lmtlcm5lbFVzZXJzLCAnc2h1dGRvd25LZXJuZWwnKSxcbiAgICBleGVjdXRlOiBQcml2YXRlLmRlbGVnYXRlRXhlY3V0ZShhcHAsIG1lbnUua2VybmVsVXNlcnMsICdzaHV0ZG93bktlcm5lbCcpXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zaHV0ZG93bkFsbEtlcm5lbHMsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1NodXQgRG93biBBbGwgS2VybmVsc+KApicpLFxuICAgIGlzRW5hYmxlZDogKCkgPT4ge1xuICAgICAgcmV0dXJuIGFwcC5zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucy5ydW5uaW5nKCkubmV4dCgpICE9PSB1bmRlZmluZWQ7XG4gICAgfSxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICAgIHRpdGxlOiB0cmFucy5fXygnU2h1dCBEb3duIEFsbD8nKSxcbiAgICAgICAgYm9keTogdHJhbnMuX18oJ1NodXQgZG93biBhbGwga2VybmVscz8nKSxcbiAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0Rpc21pc3MnKSB9KSxcbiAgICAgICAgICBEaWFsb2cud2FybkJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duIEFsbCcpIH0pXG4gICAgICAgIF1cbiAgICAgIH0pLnRoZW4ocmVzdWx0ID0+IHtcbiAgICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgICAgcmV0dXJuIGFwcC5zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucy5zaHV0ZG93bkFsbCgpO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG4gIH0pO1xufVxuXG4vKipcbiAqIENyZWF0ZSB0aGUgYmFzaWMgYFZpZXdgIG1lbnUuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBjcmVhdGVWaWV3TWVudShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIG1lbnU6IElWaWV3TWVudSxcbiAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4pOiB2b2lkIHtcbiAgY29uc3QgY29tbWFuZHMgPSBhcHAuY29tbWFuZHM7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmxpbmVOdW1iZXJpbmcsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Nob3cgTGluZSBOdW1iZXJzJyksXG4gICAgaXNFbmFibGVkOiBQcml2YXRlLmRlbGVnYXRlRW5hYmxlZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUuZWRpdG9yVmlld2VycyxcbiAgICAgICd0b2dnbGVMaW5lTnVtYmVycydcbiAgICApLFxuICAgIGlzVG9nZ2xlZDogUHJpdmF0ZS5kZWxlZ2F0ZVRvZ2dsZWQoXG4gICAgICBhcHAsXG4gICAgICBtZW51LmVkaXRvclZpZXdlcnMsXG4gICAgICAnbGluZU51bWJlcnNUb2dnbGVkJ1xuICAgICksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoXG4gICAgICBhcHAsXG4gICAgICBtZW51LmVkaXRvclZpZXdlcnMsXG4gICAgICAndG9nZ2xlTGluZU51bWJlcnMnXG4gICAgKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubWF0Y2hCcmFja2V0cywge1xuICAgIGxhYmVsOiB0cmFucy5fXygnTWF0Y2ggQnJhY2tldHMnKSxcbiAgICBpc0VuYWJsZWQ6IFByaXZhdGUuZGVsZWdhdGVFbmFibGVkKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5lZGl0b3JWaWV3ZXJzLFxuICAgICAgJ3RvZ2dsZU1hdGNoQnJhY2tldHMnXG4gICAgKSxcbiAgICBpc1RvZ2dsZWQ6IFByaXZhdGUuZGVsZWdhdGVUb2dnbGVkKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5lZGl0b3JWaWV3ZXJzLFxuICAgICAgJ21hdGNoQnJhY2tldHNUb2dnbGVkJ1xuICAgICksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoXG4gICAgICBhcHAsXG4gICAgICBtZW51LmVkaXRvclZpZXdlcnMsXG4gICAgICAndG9nZ2xlTWF0Y2hCcmFja2V0cydcbiAgICApXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy53b3JkV3JhcCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnV3JhcCBXb3JkcycpLFxuICAgIGlzRW5hYmxlZDogUHJpdmF0ZS5kZWxlZ2F0ZUVuYWJsZWQoXG4gICAgICBhcHAsXG4gICAgICBtZW51LmVkaXRvclZpZXdlcnMsXG4gICAgICAndG9nZ2xlV29yZFdyYXAnXG4gICAgKSxcbiAgICBpc1RvZ2dsZWQ6IFByaXZhdGUuZGVsZWdhdGVUb2dnbGVkKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5lZGl0b3JWaWV3ZXJzLFxuICAgICAgJ3dvcmRXcmFwVG9nZ2xlZCdcbiAgICApLFxuICAgIGV4ZWN1dGU6IFByaXZhdGUuZGVsZWdhdGVFeGVjdXRlKGFwcCwgbWVudS5lZGl0b3JWaWV3ZXJzLCAndG9nZ2xlV29yZFdyYXAnKVxuICB9KTtcbn1cblxuLyoqXG4gKiBDcmVhdGUgdGhlIGJhc2ljIGBSdW5gIG1lbnUuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBjcmVhdGVSdW5NZW51KFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgbWVudTogSVJ1bk1lbnUsXG4gIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuKTogdm9pZCB7XG4gIGNvbnN0IGNvbW1hbmRzID0gYXBwLmNvbW1hbmRzO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5ydW4sIHtcbiAgICBsYWJlbDogKCkgPT4ge1xuICAgICAgY29uc3QgbG9jYWxpemVkTGFiZWwgPSBQcml2YXRlLmRlbGVnYXRlTGFiZWwoXG4gICAgICAgIGFwcCxcbiAgICAgICAgbWVudS5jb2RlUnVubmVycyxcbiAgICAgICAgJ3J1bkxhYmVsJ1xuICAgICAgKTtcbiAgICAgIGNvbnN0IGVuYWJsZWQgPSBQcml2YXRlLmRlbGVnYXRlRW5hYmxlZChhcHAsIG1lbnUuY29kZVJ1bm5lcnMsICdydW4nKSgpO1xuICAgICAgcmV0dXJuIGVuYWJsZWQgPyBsb2NhbGl6ZWRMYWJlbCA6IHRyYW5zLl9fKCdSdW4gU2VsZWN0ZWQnKTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZDogUHJpdmF0ZS5kZWxlZ2F0ZUVuYWJsZWQoYXBwLCBtZW51LmNvZGVSdW5uZXJzLCAncnVuJyksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoYXBwLCBtZW51LmNvZGVSdW5uZXJzLCAncnVuJylcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJ1bkFsbCwge1xuICAgIGxhYmVsOiAoKSA9PiB7XG4gICAgICBsZXQgbG9jYWxpemVkTGFiZWwgPSB0cmFucy5fXygnUnVuIEFsbCcpO1xuICAgICAgY29uc3QgZW5hYmxlZCA9IFByaXZhdGUuZGVsZWdhdGVFbmFibGVkKFxuICAgICAgICBhcHAsXG4gICAgICAgIG1lbnUuY29kZVJ1bm5lcnMsXG4gICAgICAgICdydW5BbGwnXG4gICAgICApKCk7XG4gICAgICBpZiAoZW5hYmxlZCkge1xuICAgICAgICBsb2NhbGl6ZWRMYWJlbCA9IFByaXZhdGUuZGVsZWdhdGVMYWJlbChcbiAgICAgICAgICBhcHAsXG4gICAgICAgICAgbWVudS5jb2RlUnVubmVycyxcbiAgICAgICAgICAncnVuQWxsTGFiZWwnXG4gICAgICAgICk7XG4gICAgICB9XG4gICAgICByZXR1cm4gbG9jYWxpemVkTGFiZWw7XG4gICAgfSxcbiAgICBpc0VuYWJsZWQ6IFByaXZhdGUuZGVsZWdhdGVFbmFibGVkKGFwcCwgbWVudS5jb2RlUnVubmVycywgJ3J1bkFsbCcpLFxuICAgIGV4ZWN1dGU6IFByaXZhdGUuZGVsZWdhdGVFeGVjdXRlKGFwcCwgbWVudS5jb2RlUnVubmVycywgJ3J1bkFsbCcpXG4gIH0pO1xuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVzdGFydEFuZFJ1bkFsbCwge1xuICAgIGxhYmVsOiAoKSA9PiB7XG4gICAgICBsZXQgbG9jYWxpemVkTGFiZWwgPSB0cmFucy5fXygnUmVzdGFydCBLZXJuZWwgYW5kIFJ1biBBbGwnKTtcbiAgICAgIGNvbnN0IGVuYWJsZWQgPSBQcml2YXRlLmRlbGVnYXRlRW5hYmxlZChcbiAgICAgICAgYXBwLFxuICAgICAgICBtZW51LmNvZGVSdW5uZXJzLFxuICAgICAgICAncmVzdGFydEFuZFJ1bkFsbCdcbiAgICAgICkoKTtcbiAgICAgIGlmIChlbmFibGVkKSB7XG4gICAgICAgIGxvY2FsaXplZExhYmVsID0gUHJpdmF0ZS5kZWxlZ2F0ZUxhYmVsKFxuICAgICAgICAgIGFwcCxcbiAgICAgICAgICBtZW51LmNvZGVSdW5uZXJzLFxuICAgICAgICAgICdyZXN0YXJ0QW5kUnVuQWxsTGFiZWwnXG4gICAgICAgICk7XG4gICAgICB9XG4gICAgICByZXR1cm4gbG9jYWxpemVkTGFiZWw7XG4gICAgfSxcbiAgICBpc0VuYWJsZWQ6IFByaXZhdGUuZGVsZWdhdGVFbmFibGVkKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5jb2RlUnVubmVycyxcbiAgICAgICdyZXN0YXJ0QW5kUnVuQWxsJ1xuICAgICksXG4gICAgZXhlY3V0ZTogUHJpdmF0ZS5kZWxlZ2F0ZUV4ZWN1dGUoYXBwLCBtZW51LmNvZGVSdW5uZXJzLCAncmVzdGFydEFuZFJ1bkFsbCcpXG4gIH0pO1xufVxuXG4vKipcbiAqIENyZWF0ZSB0aGUgYmFzaWMgYFRhYnNgIG1lbnUuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBjcmVhdGVUYWJzTWVudShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIG1lbnU6IElUYWJzTWVudSxcbiAgbGFiU2hlbGw6IElMYWJTaGVsbCB8IG51bGwsXG4gIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuKTogdm9pZCB7XG4gIGNvbnN0IGNvbW1hbmRzID0gYXBwLmNvbW1hbmRzO1xuXG4gIC8vIEEgbGlzdCBvZiB0aGUgYWN0aXZlIHRhYnMgaW4gdGhlIG1haW4gYXJlYS5cbiAgY29uc3QgdGFiR3JvdXA6IE1lbnUuSUl0ZW1PcHRpb25zW10gPSBbXTtcbiAgLy8gQSBkaXNwb3NhYmxlIGZvciBnZXR0aW5nIHJpZCBvZiB0aGUgb3V0LW9mLWRhdGUgdGFicyBsaXN0LlxuICBsZXQgZGlzcG9zYWJsZTogSURpc3Bvc2FibGU7XG5cbiAgLy8gQ29tbWFuZCB0byBhY3RpdmF0ZSBhIHdpZGdldCBieSBpZC5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmFjdGl2YXRlQnlJZCwge1xuICAgIGxhYmVsOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGlkID0gYXJnc1snaWQnXSB8fCAnJztcbiAgICAgIGNvbnN0IHdpZGdldCA9IGZpbmQoYXBwLnNoZWxsLndpZGdldHMoJ21haW4nKSwgdyA9PiB3LmlkID09PSBpZCk7XG4gICAgICByZXR1cm4gKHdpZGdldCAmJiB3aWRnZXQudGl0bGUubGFiZWwpIHx8ICcnO1xuICAgIH0sXG4gICAgaXNUb2dnbGVkOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGlkID0gYXJnc1snaWQnXSB8fCAnJztcbiAgICAgIHJldHVybiAhIWFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0ICYmIGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0LmlkID09PSBpZDtcbiAgICB9LFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4gYXBwLnNoZWxsLmFjdGl2YXRlQnlJZCgoYXJnc1snaWQnXSBhcyBzdHJpbmcpIHx8ICcnKVxuICB9KTtcblxuICBsZXQgcHJldmlvdXNJZCA9ICcnO1xuICAvLyBDb21tYW5kIHRvIHRvZ2dsZSBiZXR3ZWVuIHRoZSBjdXJyZW50XG4gIC8vIHRhYiBhbmQgdGhlIGxhc3QgbW9kaWZpZWQgdGFiLlxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuYWN0aXZhdGVQcmV2aW91c2x5VXNlZFRhYiwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnQWN0aXZhdGUgUHJldmlvdXNseSBVc2VkIFRhYicpLFxuICAgIGlzRW5hYmxlZDogKCkgPT4gISFwcmV2aW91c0lkLFxuICAgIGV4ZWN1dGU6ICgpID0+IGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5hY3RpdmF0ZUJ5SWQsIHsgaWQ6IHByZXZpb3VzSWQgfSlcbiAgfSk7XG5cbiAgaWYgKGxhYlNoZWxsKSB7XG4gICAgdm9pZCBhcHAucmVzdG9yZWQudGhlbigoKSA9PiB7XG4gICAgICAvLyBJdGVyYXRlIG92ZXIgdGhlIGN1cnJlbnQgd2lkZ2V0cyBpbiB0aGVcbiAgICAgIC8vIG1haW4gYXJlYSwgYW5kIGFkZCB0aGVtIHRvIHRoZSB0YWIgZ3JvdXBcbiAgICAgIC8vIG9mIHRoZSBtZW51LlxuICAgICAgY29uc3QgcG9wdWxhdGVUYWJzID0gKCkgPT4ge1xuICAgICAgICAvLyByZW1vdmUgdGhlIHByZXZpb3VzIHRhYiBsaXN0XG4gICAgICAgIGlmIChkaXNwb3NhYmxlICYmICFkaXNwb3NhYmxlLmlzRGlzcG9zZWQpIHtcbiAgICAgICAgICBkaXNwb3NhYmxlLmRpc3Bvc2UoKTtcbiAgICAgICAgfVxuICAgICAgICB0YWJHcm91cC5sZW5ndGggPSAwO1xuXG4gICAgICAgIGxldCBpc1ByZXZpb3VzbHlVc2VkVGFiQXR0YWNoZWQgPSBmYWxzZTtcbiAgICAgICAgZWFjaChhcHAuc2hlbGwud2lkZ2V0cygnbWFpbicpLCB3aWRnZXQgPT4ge1xuICAgICAgICAgIGlmICh3aWRnZXQuaWQgPT09IHByZXZpb3VzSWQpIHtcbiAgICAgICAgICAgIGlzUHJldmlvdXNseVVzZWRUYWJBdHRhY2hlZCA9IHRydWU7XG4gICAgICAgICAgfVxuICAgICAgICAgIHRhYkdyb3VwLnB1c2goe1xuICAgICAgICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5hY3RpdmF0ZUJ5SWQsXG4gICAgICAgICAgICBhcmdzOiB7IGlkOiB3aWRnZXQuaWQgfVxuICAgICAgICAgIH0pO1xuICAgICAgICB9KTtcbiAgICAgICAgZGlzcG9zYWJsZSA9IG1lbnUuYWRkR3JvdXAodGFiR3JvdXAsIDEpO1xuICAgICAgICBwcmV2aW91c0lkID0gaXNQcmV2aW91c2x5VXNlZFRhYkF0dGFjaGVkID8gcHJldmlvdXNJZCA6ICcnO1xuICAgICAgfTtcbiAgICAgIHBvcHVsYXRlVGFicygpO1xuICAgICAgbGFiU2hlbGwubGF5b3V0TW9kaWZpZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgIHBvcHVsYXRlVGFicygpO1xuICAgICAgfSk7XG4gICAgICAvLyBVcGRhdGUgdGhlIElEIG9mIHRoZSBwcmV2aW91cyBhY3RpdmUgdGFiIGlmIGEgbmV3IHRhYiBpcyBzZWxlY3RlZC5cbiAgICAgIGxhYlNoZWxsLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QoKF8sIGFyZ3MpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gYXJncy5vbGRWYWx1ZTtcbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgcHJldmlvdXNJZCA9IHdpZGdldC5pZDtcbiAgICAgIH0pO1xuICAgIH0pO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgUHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBSZXR1cm4gdGhlIGZpcnN0IHZhbHVlIG9mIHRoZSBpdGVyYWJsZSB0aGF0IHNhdGlzZmllcyB0aGUgcHJlZGljYXRlXG4gICAqIGZ1bmN0aW9uLlxuICAgKi9cbiAgZnVuY3Rpb24gZmluZDxUPihcbiAgICBpdDogSXRlcmFibGU8VD4sXG4gICAgcHJlZGljYXRlOiAodmFsdWU6IFQpID0+IGJvb2xlYW5cbiAgKTogVCB8IHVuZGVmaW5lZCB7XG4gICAgZm9yIChjb25zdCB2YWx1ZSBvZiBpdCkge1xuICAgICAgaWYgKHByZWRpY2F0ZSh2YWx1ZSkpIHtcbiAgICAgICAgcmV0dXJuIHZhbHVlO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gdW5kZWZpbmVkO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgdXRpbGl0eSBmdW5jdGlvbiB0aGF0IGRlbGVnYXRlcyBhIHBvcnRpb24gb2YgYSBsYWJlbCB0byBhbiBJTWVudUV4dGVuZGVyLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGRlbGVnYXRlTGFiZWw8RSBleHRlbmRzIElNZW51RXh0ZW5kZXI8V2lkZ2V0Pj4oXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgczogU2V0PEU+LFxuICAgIGxhYmVsOiBrZXlvZiBFXG4gICk6IHN0cmluZyB7XG4gICAgY29uc3Qgd2lkZ2V0ID0gYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgY29uc3QgZXh0ZW5kZXIgPSB3aWRnZXRcbiAgICAgID8gZmluZChzLCB2YWx1ZSA9PiB2YWx1ZS50cmFja2VyLmhhcyh3aWRnZXQhKSlcbiAgICAgIDogdW5kZWZpbmVkO1xuXG4gICAgaWYgKCFleHRlbmRlcikge1xuICAgICAgcmV0dXJuICcnO1xuICAgIH0gZWxzZSB7XG4gICAgICBjb25zdCBjb3VudDogbnVtYmVyID0gZXh0ZW5kZXIudHJhY2tlci5zaXplO1xuXG4gICAgICAvLyBDb2VyY2UgdGhlIHJlc3VsdCB0byBiZSBhIHN0cmluZy4gV2hlbiBUeXBlZG9jIGlzIHVwZGF0ZWQgdG8gdXNlXG4gICAgICAvLyBUeXBlc2NyaXB0IDIuOCwgd2UgY2FuIHBvc3NpYmx5IHVzZSBjb25kaXRpb25hbCB0eXBlcyB0byBnZXQgVHlwZXNjcmlwdFxuICAgICAgLy8gdG8gcmVjb2duaXplIHRoaXMgaXMgYSBzdHJpbmcuXG4gICAgICByZXR1cm4gKGV4dGVuZGVyW2xhYmVsXSBhcyBhbnkpKGNvdW50KSBhcyBzdHJpbmc7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEEgdXRpbGl0eSBmdW5jdGlvbiB0aGF0IGRlbGVnYXRlcyBjb21tYW5kIGV4ZWN1dGlvblxuICAgKiB0byBhbiBJTWVudUV4dGVuZGVyLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGRlbGVnYXRlRXhlY3V0ZTxFIGV4dGVuZHMgSU1lbnVFeHRlbmRlcjxXaWRnZXQ+PihcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzOiBTZXQ8RT4sXG4gICAgZXhlY3V0b3I6IGtleW9mIEVcbiAgKTogKCkgPT4gUHJvbWlzZTxhbnk+IHtcbiAgICByZXR1cm4gKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBjb25zdCBleHRlbmRlciA9IHdpZGdldFxuICAgICAgICA/IGZpbmQocywgdmFsdWUgPT4gdmFsdWUudHJhY2tlci5oYXMod2lkZ2V0ISkpXG4gICAgICAgIDogdW5kZWZpbmVkO1xuICAgICAgaWYgKCFleHRlbmRlcikge1xuICAgICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKHZvaWQgMCk7XG4gICAgICB9XG4gICAgICAvLyBDb2VyY2UgdGhlIHJlc3VsdCB0byBiZSBhIGZ1bmN0aW9uLiBXaGVuIFR5cGVkb2MgaXMgdXBkYXRlZCB0byB1c2VcbiAgICAgIC8vIFR5cGVzY3JpcHQgMi44LCB3ZSBjYW4gcG9zc2libHkgdXNlIGNvbmRpdGlvbmFsIHR5cGVzIHRvIGdldCBUeXBlc2NyaXB0XG4gICAgICAvLyB0byByZWNvZ25pemUgdGhpcyBpcyBhIGZ1bmN0aW9uLlxuICAgICAgY29uc3QgZiA9IChleHRlbmRlcltleGVjdXRvcl0gYXMgYW55KSBhcyAodzogV2lkZ2V0KSA9PiBQcm9taXNlPGFueT47XG4gICAgICByZXR1cm4gZih3aWRnZXQhKTtcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIEEgdXRpbGl0eSBmdW5jdGlvbiB0aGF0IGRlbGVnYXRlcyB3aGV0aGVyIGEgY29tbWFuZCBpcyBlbmFibGVkXG4gICAqIHRvIGFuIElNZW51RXh0ZW5kZXIuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZGVsZWdhdGVFbmFibGVkPEUgZXh0ZW5kcyBJTWVudUV4dGVuZGVyPFdpZGdldD4+KFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHM6IFNldDxFPixcbiAgICBleGVjdXRvcjoga2V5b2YgRVxuICApOiAoKSA9PiBib29sZWFuIHtcbiAgICByZXR1cm4gKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBjb25zdCBleHRlbmRlciA9IHdpZGdldFxuICAgICAgICA/IGZpbmQocywgdmFsdWUgPT4gdmFsdWUudHJhY2tlci5oYXMod2lkZ2V0ISkpXG4gICAgICAgIDogdW5kZWZpbmVkO1xuICAgICAgcmV0dXJuIChcbiAgICAgICAgISFleHRlbmRlciAmJlxuICAgICAgICAhIWV4dGVuZGVyW2V4ZWN1dG9yXSAmJlxuICAgICAgICAoZXh0ZW5kZXIuaXNFbmFibGVkICYmIHdpZGdldCA/IGV4dGVuZGVyLmlzRW5hYmxlZCh3aWRnZXQpIDogdHJ1ZSlcbiAgICAgICk7XG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHV0aWxpdHkgZnVuY3Rpb24gdGhhdCBkZWxlZ2F0ZXMgd2hldGhlciBhIGNvbW1hbmQgaXMgdG9nZ2xlZFxuICAgKiBmb3IgYW4gSU1lbnVFeHRlbmRlci5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBkZWxlZ2F0ZVRvZ2dsZWQ8RSBleHRlbmRzIElNZW51RXh0ZW5kZXI8V2lkZ2V0Pj4oXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgczogU2V0PEU+LFxuICAgIHRvZ2dsZWQ6IGtleW9mIEVcbiAgKTogKCkgPT4gYm9vbGVhbiB7XG4gICAgcmV0dXJuICgpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0O1xuICAgICAgY29uc3QgZXh0ZW5kZXIgPSB3aWRnZXRcbiAgICAgICAgPyBmaW5kKHMsIHZhbHVlID0+IHZhbHVlLnRyYWNrZXIuaGFzKHdpZGdldCEpKVxuICAgICAgICA6IHVuZGVmaW5lZDtcbiAgICAgIC8vIENvZXJjZSBleHRlbmRlclt0b2dnbGVkXSB0byBiZSBhIGZ1bmN0aW9uLiBXaGVuIFR5cGVkb2MgaXMgdXBkYXRlZCB0byB1c2VcbiAgICAgIC8vIFR5cGVzY3JpcHQgMi44LCB3ZSBjYW4gcG9zc2libHkgdXNlIGNvbmRpdGlvbmFsIHR5cGVzIHRvIGdldCBUeXBlc2NyaXB0XG4gICAgICAvLyB0byByZWNvZ25pemUgdGhpcyBpcyBhIGZ1bmN0aW9uLlxuICAgICAgcmV0dXJuIChcbiAgICAgICAgISFleHRlbmRlciAmJlxuICAgICAgICAhIWV4dGVuZGVyW3RvZ2dsZWRdICYmXG4gICAgICAgICEhd2lkZ2V0ICYmXG4gICAgICAgICEhKChleHRlbmRlclt0b2dnbGVkXSBhcyBhbnkpIGFzICh3OiBXaWRnZXQpID0+ICgpID0+IGJvb2xlYW4pKHdpZGdldClcbiAgICAgICk7XG4gICAgfTtcbiAgfVxuXG4gIGFzeW5jIGZ1bmN0aW9uIGRpc3BsYXlJbmZvcm1hdGlvbih0cmFuczogVHJhbnNsYXRpb25CdW5kbGUpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCByZXN1bHQgPSBhd2FpdCBzaG93RGlhbG9nKHtcbiAgICAgIHRpdGxlOiB0cmFucy5fXygnSW5mb3JtYXRpb24nKSxcbiAgICAgIGJvZHk6IHRyYW5zLl9fKFxuICAgICAgICAnTWVudSBjdXN0b21pemF0aW9uIGhhcyBjaGFuZ2VkLiBZb3Ugd2lsbCBuZWVkIHRvIHJlbG9hZCBKdXB5dGVyTGFiIHRvIHNlZSB0aGUgY2hhbmdlcy4nXG4gICAgICApLFxuICAgICAgYnV0dG9uczogW1xuICAgICAgICBEaWFsb2cuY2FuY2VsQnV0dG9uKCksXG4gICAgICAgIERpYWxvZy5va0J1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnUmVsb2FkJykgfSlcbiAgICAgIF1cbiAgICB9KTtcblxuICAgIGlmIChyZXN1bHQuYnV0dG9uLmFjY2VwdCkge1xuICAgICAgbG9jYXRpb24ucmVsb2FkKCk7XG4gICAgfVxuICB9XG5cbiAgZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGxvYWRTZXR0aW5nc01lbnUoXG4gICAgcmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgYWRkTWVudTogKG1lbnU6IE1lbnUpID0+IHZvaWQsXG4gICAgbWVudUZhY3Rvcnk6IChvcHRpb25zOiBJTWFpbk1lbnUuSU1lbnVPcHRpb25zKSA9PiBKdXB5dGVyTGFiTWVudSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGxldCBjYW5vbmljYWw6IElTZXR0aW5nUmVnaXN0cnkuSVNjaGVtYSB8IG51bGw7XG4gICAgbGV0IGxvYWRlZDogeyBbbmFtZTogc3RyaW5nXTogSVNldHRpbmdSZWdpc3RyeS5JTWVudVtdIH0gPSB7fTtcblxuICAgIC8qKlxuICAgICAqIFBvcHVsYXRlIHRoZSBwbHVnaW4ncyBzY2hlbWEgZGVmYXVsdHMuXG4gICAgICovXG4gICAgZnVuY3Rpb24gcG9wdWxhdGUoc2NoZW1hOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWEpIHtcbiAgICAgIGxvYWRlZCA9IHt9O1xuICAgICAgY29uc3QgcGx1Z2luRGVmYXVsdHMgPSBPYmplY3Qua2V5cyhyZWdpc3RyeS5wbHVnaW5zKVxuICAgICAgICAubWFwKHBsdWdpbiA9PiB7XG4gICAgICAgICAgY29uc3QgbWVudXMgPVxuICAgICAgICAgICAgcmVnaXN0cnkucGx1Z2luc1twbHVnaW5dIS5zY2hlbWFbJ2p1cHl0ZXIubGFiLm1lbnVzJ10/Lm1haW4gPz8gW107XG4gICAgICAgICAgbG9hZGVkW3BsdWdpbl0gPSBtZW51cztcbiAgICAgICAgICByZXR1cm4gbWVudXM7XG4gICAgICAgIH0pXG4gICAgICAgIC5jb25jYXQoW3NjaGVtYVsnanVweXRlci5sYWIubWVudXMnXT8ubWFpbiA/PyBbXV0pXG4gICAgICAgIC5yZWR1Y2VSaWdodChcbiAgICAgICAgICAoYWNjLCB2YWwpID0+IFNldHRpbmdSZWdpc3RyeS5yZWNvbmNpbGVNZW51cyhhY2MsIHZhbCwgdHJ1ZSksXG4gICAgICAgICAgc2NoZW1hLnByb3BlcnRpZXMhLm1lbnVzLmRlZmF1bHQgYXMgYW55W11cbiAgICAgICAgKTtcblxuICAgICAgLy8gQXBwbHkgZGVmYXVsdCB2YWx1ZSBhcyBsYXN0IHN0ZXAgdG8gdGFrZSBpbnRvIGFjY291bnQgb3ZlcnJpZGVzLmpzb25cbiAgICAgIC8vIFRoZSBzdGFuZGFyZCBkZWZhdWx0IGJlaW5nIFtdIGFzIHRoZSBwbHVnaW4gbXVzdCB1c2UgYGp1cHl0ZXIubGFiLm1lbnVzLm1haW5gXG4gICAgICAvLyB0byBkZWZpbmUgdGhlaXIgZGVmYXVsdCB2YWx1ZS5cbiAgICAgIHNjaGVtYS5wcm9wZXJ0aWVzIS5tZW51cy5kZWZhdWx0ID0gU2V0dGluZ1JlZ2lzdHJ5LnJlY29uY2lsZU1lbnVzKFxuICAgICAgICBwbHVnaW5EZWZhdWx0cyxcbiAgICAgICAgc2NoZW1hLnByb3BlcnRpZXMhLm1lbnVzLmRlZmF1bHQgYXMgYW55W10sXG4gICAgICAgIHRydWVcbiAgICAgIClcbiAgICAgICAgLy8gZmxhdHRlbiBvbmUgbGV2ZWxcbiAgICAgICAgLnNvcnQoKGEsIGIpID0+IChhLnJhbmsgPz8gSW5maW5pdHkpIC0gKGIucmFuayA/PyBJbmZpbml0eSkpO1xuICAgIH1cblxuICAgIC8vIFRyYW5zZm9ybSB0aGUgcGx1Z2luIG9iamVjdCB0byByZXR1cm4gZGlmZmVyZW50IHNjaGVtYSB0aGFuIHRoZSBkZWZhdWx0LlxuICAgIHJlZ2lzdHJ5LnRyYW5zZm9ybShQTFVHSU5fSUQsIHtcbiAgICAgIGNvbXBvc2U6IHBsdWdpbiA9PiB7XG4gICAgICAgIC8vIE9ubHkgb3ZlcnJpZGUgdGhlIGNhbm9uaWNhbCBzY2hlbWEgdGhlIGZpcnN0IHRpbWUuXG4gICAgICAgIGlmICghY2Fub25pY2FsKSB7XG4gICAgICAgICAgY2Fub25pY2FsID0gSlNPTkV4dC5kZWVwQ29weShwbHVnaW4uc2NoZW1hKTtcbiAgICAgICAgICBwb3B1bGF0ZShjYW5vbmljYWwpO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgZGVmYXVsdHMgPSBjYW5vbmljYWwucHJvcGVydGllcz8ubWVudXM/LmRlZmF1bHQgPz8gW107XG4gICAgICAgIGNvbnN0IHVzZXIgPSB7XG4gICAgICAgICAgbWVudXM6IHBsdWdpbi5kYXRhLnVzZXIubWVudXMgPz8gW11cbiAgICAgICAgfTtcbiAgICAgICAgY29uc3QgY29tcG9zaXRlID0ge1xuICAgICAgICAgIG1lbnVzOiBTZXR0aW5nUmVnaXN0cnkucmVjb25jaWxlTWVudXMoXG4gICAgICAgICAgICBkZWZhdWx0cyBhcyBJU2V0dGluZ1JlZ2lzdHJ5LklNZW51W10sXG4gICAgICAgICAgICB1c2VyLm1lbnVzIGFzIElTZXR0aW5nUmVnaXN0cnkuSU1lbnVbXVxuICAgICAgICAgIClcbiAgICAgICAgfTtcblxuICAgICAgICBwbHVnaW4uZGF0YSA9IHsgY29tcG9zaXRlLCB1c2VyIH07XG5cbiAgICAgICAgcmV0dXJuIHBsdWdpbjtcbiAgICAgIH0sXG4gICAgICBmZXRjaDogcGx1Z2luID0+IHtcbiAgICAgICAgLy8gT25seSBvdmVycmlkZSB0aGUgY2Fub25pY2FsIHNjaGVtYSB0aGUgZmlyc3QgdGltZS5cbiAgICAgICAgaWYgKCFjYW5vbmljYWwpIHtcbiAgICAgICAgICBjYW5vbmljYWwgPSBKU09ORXh0LmRlZXBDb3B5KHBsdWdpbi5zY2hlbWEpO1xuICAgICAgICAgIHBvcHVsYXRlKGNhbm9uaWNhbCk7XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIGRhdGE6IHBsdWdpbi5kYXRhLFxuICAgICAgICAgIGlkOiBwbHVnaW4uaWQsXG4gICAgICAgICAgcmF3OiBwbHVnaW4ucmF3LFxuICAgICAgICAgIHNjaGVtYTogY2Fub25pY2FsLFxuICAgICAgICAgIHZlcnNpb246IHBsdWdpbi52ZXJzaW9uXG4gICAgICAgIH07XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBSZXBvcHVsYXRlIHRoZSBjYW5vbmljYWwgdmFyaWFibGUgYWZ0ZXIgdGhlIHNldHRpbmcgcmVnaXN0cnkgaGFzXG4gICAgLy8gcHJlbG9hZGVkIGFsbCBpbml0aWFsIHBsdWdpbnMuXG4gICAgY2Fub25pY2FsID0gbnVsbDtcblxuICAgIGNvbnN0IHNldHRpbmdzID0gYXdhaXQgcmVnaXN0cnkubG9hZChQTFVHSU5fSUQpO1xuXG4gICAgY29uc3QgY3VycmVudE1lbnVzOiBJU2V0dGluZ1JlZ2lzdHJ5LklNZW51W10gPVxuICAgICAgSlNPTkV4dC5kZWVwQ29weShzZXR0aW5ncy5jb21wb3NpdGUubWVudXMgYXMgYW55KSA/PyBbXTtcbiAgICBjb25zdCBtZW51cyA9IG5ldyBBcnJheTxNZW51PigpO1xuICAgIC8vIENyZWF0ZSBtZW51IGZvciBub24tZGlzYWJsZWQgZWxlbWVudFxuICAgIE1lbnVGYWN0b3J5LmNyZWF0ZU1lbnVzKFxuICAgICAgY3VycmVudE1lbnVzXG4gICAgICAgIC5maWx0ZXIobWVudSA9PiAhbWVudS5kaXNhYmxlZClcbiAgICAgICAgLm1hcChtZW51ID0+IHtcbiAgICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgLi4ubWVudSxcbiAgICAgICAgICAgIGl0ZW1zOiBTZXR0aW5nUmVnaXN0cnkuZmlsdGVyRGlzYWJsZWRJdGVtcyhtZW51Lml0ZW1zID8/IFtdKVxuICAgICAgICAgIH07XG4gICAgICAgIH0pLFxuICAgICAgbWVudUZhY3RvcnlcbiAgICApLmZvckVhY2gobWVudSA9PiB7XG4gICAgICBtZW51cy5wdXNoKG1lbnUpO1xuICAgICAgYWRkTWVudShtZW51KTtcbiAgICB9KTtcblxuICAgIHNldHRpbmdzLmNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAvLyBBcyBleHRlbnNpb24gbWF5IGNoYW5nZSBtZW51IHRocm91Z2ggQVBJLCBwcm9tcHQgdGhlIHVzZXIgdG8gcmVsb2FkIGlmIHRoZVxuICAgICAgLy8gbWVudSBoYXMgYmVlbiB1cGRhdGVkLlxuICAgICAgY29uc3QgbmV3TWVudXMgPSAoc2V0dGluZ3MuY29tcG9zaXRlLm1lbnVzIGFzIGFueSkgPz8gW107XG4gICAgICBpZiAoIUpTT05FeHQuZGVlcEVxdWFsKGN1cnJlbnRNZW51cywgbmV3TWVudXMpKSB7XG4gICAgICAgIHZvaWQgZGlzcGxheUluZm9ybWF0aW9uKHRyYW5zKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIHJlZ2lzdHJ5LnBsdWdpbkNoYW5nZWQuY29ubmVjdChhc3luYyAoc2VuZGVyLCBwbHVnaW4pID0+IHtcbiAgICAgIGlmIChwbHVnaW4gIT09IFBMVUdJTl9JRCkge1xuICAgICAgICAvLyBJZiB0aGUgcGx1Z2luIGNoYW5nZWQgaXRzIG1lbnUuXG4gICAgICAgIGNvbnN0IG9sZE1lbnVzID0gbG9hZGVkW3BsdWdpbl0gPz8gW107XG4gICAgICAgIGNvbnN0IG5ld01lbnVzID1cbiAgICAgICAgICByZWdpc3RyeS5wbHVnaW5zW3BsdWdpbl0hLnNjaGVtYVsnanVweXRlci5sYWIubWVudXMnXT8ubWFpbiA/PyBbXTtcbiAgICAgICAgaWYgKCFKU09ORXh0LmRlZXBFcXVhbChvbGRNZW51cywgbmV3TWVudXMpKSB7XG4gICAgICAgICAgaWYgKGxvYWRlZFtwbHVnaW5dKSB7XG4gICAgICAgICAgICAvLyBUaGUgcGx1Z2luIGhhcyBjaGFuZ2VkLCByZXF1ZXN0IHRoZSB1c2VyIHRvIHJlbG9hZCB0aGUgVUkgLSB0aGlzIHNob3VsZCBub3QgaGFwcGVuXG4gICAgICAgICAgICBhd2FpdCBkaXNwbGF5SW5mb3JtYXRpb24odHJhbnMpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAvLyBUaGUgcGx1Z2luIHdhcyBub3QgeWV0IGxvYWRlZCB3aGVuIHRoZSBtZW51IHdhcyBidWlsdCA9PiB1cGRhdGUgdGhlIG1lbnVcbiAgICAgICAgICAgIGxvYWRlZFtwbHVnaW5dID0gSlNPTkV4dC5kZWVwQ29weShuZXdNZW51cyk7XG4gICAgICAgICAgICAvLyBNZXJnZSBwb3RlbnRpYWwgZGlzYWJsZWQgc3RhdGVcbiAgICAgICAgICAgIGNvbnN0IHRvQWRkID0gU2V0dGluZ1JlZ2lzdHJ5LnJlY29uY2lsZU1lbnVzKFxuICAgICAgICAgICAgICBuZXdNZW51cyxcbiAgICAgICAgICAgICAgY3VycmVudE1lbnVzLFxuICAgICAgICAgICAgICBmYWxzZSxcbiAgICAgICAgICAgICAgZmFsc2VcbiAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgLmZpbHRlcihtZW51ID0+ICFtZW51LmRpc2FibGVkKVxuICAgICAgICAgICAgICAubWFwKG1lbnUgPT4ge1xuICAgICAgICAgICAgICAgIHJldHVybiB7XG4gICAgICAgICAgICAgICAgICAuLi5tZW51LFxuICAgICAgICAgICAgICAgICAgaXRlbXM6IFNldHRpbmdSZWdpc3RyeS5maWx0ZXJEaXNhYmxlZEl0ZW1zKG1lbnUuaXRlbXMgPz8gW10pXG4gICAgICAgICAgICAgICAgfTtcbiAgICAgICAgICAgICAgfSk7XG5cbiAgICAgICAgICAgIE1lbnVGYWN0b3J5LnVwZGF0ZU1lbnVzKG1lbnVzLCB0b0FkZCwgbWVudUZhY3RvcnkpLmZvckVhY2gobWVudSA9PiB7XG4gICAgICAgICAgICAgIGFkZE1lbnUobWVudSk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==