(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_terminal-extension_lib_index_js"],{

/***/ "../packages/terminal-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/terminal-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "addCommands": () => (/* binding */ addCommands)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_running__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/running */ "webpack/sharing/consume/default/@jupyterlab/running/@jupyterlab/running");
/* harmony import */ var _jupyterlab_running__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_running__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/terminal */ "webpack/sharing/consume/default/@jupyterlab/terminal/@jupyterlab/terminal");
/* harmony import */ var _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_10__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module terminal-extension
 */











/**
 * The command IDs used by the terminal plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'terminal:create-new';
    CommandIDs.open = 'terminal:open';
    CommandIDs.refresh = 'terminal:refresh';
    CommandIDs.increaseFont = 'terminal:increase-font';
    CommandIDs.decreaseFont = 'terminal:decrease-font';
    CommandIDs.setTheme = 'terminal:set-theme';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default terminal extension.
 */
const plugin = {
    activate,
    id: '@jupyterlab/terminal-extension:plugin',
    provides: _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_6__.ITerminalTracker,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    optional: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager,
        _jupyterlab_running__WEBPACK_IMPORTED_MODULE_4__.IRunningSessionManagers
    ],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the terminal plugin.
 */
function activate(app, settingRegistry, translator, palette, launcher, restorer, mainMenu, themeManager, runningSessionManagers) {
    const trans = translator.load('jupyterlab');
    const { serviceManager, commands } = app;
    const category = trans.__('Terminal');
    const namespace = 'terminal';
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    // Bail if there are no terminals available.
    if (!serviceManager.terminals.isAvailable()) {
        console.warn('Disabling terminals plugin because they are not available on the server');
        return tracker;
    }
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.createNew,
            args: widget => ({ name: widget.content.session.name }),
            name: widget => widget.content.session.name
        });
    }
    // The cached terminal options from the setting editor.
    const options = {};
    /**
     * Update the cached option values.
     */
    function updateOptions(settings) {
        // Update the cached options by doing a shallow copy of key/values.
        // This is needed because options is passed and used in addcommand-palette and needs
        // to reflect the current cached values.
        Object.keys(settings.composite).forEach((key) => {
            options[key] = settings.composite[key];
        });
    }
    /**
     * Update terminal
     */
    function updateTerminal(widget) {
        const terminal = widget.content;
        if (!terminal) {
            return;
        }
        Object.keys(options).forEach((key) => {
            terminal.setOption(key, options[key]);
        });
    }
    /**
     * Update the settings of the current tracker instances.
     */
    function updateTracker() {
        tracker.forEach(widget => updateTerminal(widget));
    }
    // Fetch the initial state of the settings.
    settingRegistry
        .load(plugin.id)
        .then(settings => {
        updateOptions(settings);
        updateTracker();
        settings.changed.connect(() => {
            updateOptions(settings);
            updateTracker();
        });
    })
        .catch(Private.showErrorMessage);
    // Subscribe to changes in theme. This is needed as the theme
    // is computed dynamically based on the string value and DOM
    // properties.
    themeManager === null || themeManager === void 0 ? void 0 : themeManager.themeChanged.connect((sender, args) => {
        tracker.forEach(widget => {
            const terminal = widget.content;
            if (terminal.getOption('theme') === 'inherit') {
                terminal.setOption('theme', 'inherit');
            }
        });
    });
    addCommands(app, tracker, settingRegistry, translator, options);
    if (mainMenu) {
        // Add "Terminal Theme" menu below "Theme" menu.
        const themeMenu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__.Menu({ commands });
        themeMenu.title.label = trans._p('menu', 'Terminal Theme');
        themeMenu.addItem({
            command: CommandIDs.setTheme,
            args: {
                theme: 'inherit',
                displayName: trans.__('Inherit'),
                isPalette: false
            }
        });
        themeMenu.addItem({
            command: CommandIDs.setTheme,
            args: {
                theme: 'light',
                displayName: trans.__('Light'),
                isPalette: false
            }
        });
        themeMenu.addItem({
            command: CommandIDs.setTheme,
            args: { theme: 'dark', displayName: trans.__('Dark'), isPalette: false }
        });
        // Add some commands to the "View" menu.
        mainMenu.settingsMenu.addGroup([
            { command: CommandIDs.increaseFont },
            { command: CommandIDs.decreaseFont },
            { type: 'submenu', submenu: themeMenu }
        ], 40);
        // Add terminal creation to the file menu.
        mainMenu.fileMenu.newMenu.addItem({
            command: CommandIDs.createNew,
            rank: 20
        });
        // Add terminal close-and-shutdown to the file menu.
        mainMenu.fileMenu.closeAndCleaners.add({
            tracker,
            closeAndCleanupLabel: (n) => trans.__('Shutdown Terminal'),
            closeAndCleanup: (current) => {
                // The widget is automatically disposed upon session shutdown.
                return current.content.session.shutdown();
            }
        });
    }
    if (palette) {
        // Add command palette items.
        [
            CommandIDs.createNew,
            CommandIDs.refresh,
            CommandIDs.increaseFont,
            CommandIDs.decreaseFont
        ].forEach(command => {
            palette.addItem({ command, category, args: { isPalette: true } });
        });
        palette.addItem({
            command: CommandIDs.setTheme,
            category,
            args: {
                theme: 'inherit',
                displayName: trans.__('Inherit'),
                isPalette: true
            }
        });
        palette.addItem({
            command: CommandIDs.setTheme,
            category,
            args: { theme: 'light', displayName: trans.__('Light'), isPalette: true }
        });
        palette.addItem({
            command: CommandIDs.setTheme,
            category,
            args: { theme: 'dark', displayName: trans.__('Dark'), isPalette: true }
        });
    }
    // Add a launcher item if the launcher is available.
    if (launcher) {
        launcher.add({
            command: CommandIDs.createNew,
            category: trans.__('Other'),
            rank: 0
        });
    }
    // Add a sessions manager if the running extension is available
    if (runningSessionManagers) {
        addRunningSessionManager(runningSessionManagers, app, translator);
    }
    return tracker;
}
/**
 * Add the running terminal manager to the running panel.
 */
function addRunningSessionManager(managers, app, translator) {
    const trans = translator.load('jupyterlab');
    const manager = app.serviceManager.terminals;
    managers.add({
        name: trans.__('Terminals'),
        running: () => (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__.toArray)(manager.running()).map(model => new RunningTerminal(model)),
        shutdownAll: () => manager.shutdownAll(),
        refreshRunning: () => manager.refreshRunning(),
        runningChanged: manager.runningChanged,
        shutdownLabel: trans.__('Shut Down'),
        shutdownAllLabel: trans.__('Shut Down All'),
        shutdownAllConfirmationText: trans.__('Are you sure you want to permanently shut down all running terminals?')
    });
    class RunningTerminal {
        constructor(model) {
            this._model = model;
        }
        open() {
            void app.commands.execute('terminal:open', { name: this._model.name });
        }
        icon() {
            return _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.terminalIcon;
        }
        label() {
            return `terminals/${this._model.name}`;
        }
        shutdown() {
            return manager.shutdown(this._model.name);
        }
    }
}
/**
 * Add the commands for the terminal.
 */
function addCommands(app, tracker, settingRegistry, translator, options) {
    const trans = translator.load('jupyterlab');
    const { commands, serviceManager } = app;
    // Add terminal commands.
    commands.addCommand(CommandIDs.createNew, {
        label: args => args['isPalette'] ? trans.__('New Terminal') : trans.__('Terminal'),
        caption: trans.__('Start a new terminal session'),
        icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.terminalIcon),
        execute: async (args) => {
            // wait for the widget to lazy load
            let Terminal;
            try {
                Terminal = (await Private.ensureWidget()).Terminal;
            }
            catch (err) {
                Private.showErrorMessage(err);
                return;
            }
            const name = args['name'];
            const session = await (name
                ? serviceManager.terminals.connectTo({ model: { name } })
                : serviceManager.terminals.startNew());
            const term = new Terminal(session, options, translator);
            term.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.terminalIcon;
            term.title.label = '...';
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: term });
            app.shell.add(main);
            void tracker.add(main);
            app.shell.activateById(main.id);
            return main;
        }
    });
    commands.addCommand(CommandIDs.open, {
        execute: args => {
            const name = args['name'];
            // Check for a running terminal with the given name.
            const widget = tracker.find(value => {
                const content = value.content;
                return content.session.name === name || false;
            });
            if (widget) {
                app.shell.activateById(widget.id);
            }
            else {
                // Otherwise, create a new terminal with a given name.
                return commands.execute(CommandIDs.createNew, { name });
            }
        }
    });
    commands.addCommand(CommandIDs.refresh, {
        label: trans.__('Refresh Terminal'),
        caption: trans.__('Refresh the current terminal session'),
        execute: async () => {
            const current = tracker.currentWidget;
            if (!current) {
                return;
            }
            app.shell.activateById(current.id);
            try {
                await current.content.refresh();
                if (current) {
                    current.content.activate();
                }
            }
            catch (err) {
                Private.showErrorMessage(err);
            }
        },
        isEnabled: () => tracker.currentWidget !== null
    });
    commands.addCommand(CommandIDs.increaseFont, {
        label: trans.__('Increase Terminal Font Size'),
        execute: async () => {
            const { fontSize } = options;
            if (fontSize && fontSize < 72) {
                try {
                    await settingRegistry.set(plugin.id, 'fontSize', fontSize + 1);
                }
                catch (err) {
                    Private.showErrorMessage(err);
                }
            }
        }
    });
    commands.addCommand(CommandIDs.decreaseFont, {
        label: trans.__('Decrease Terminal Font Size'),
        execute: async () => {
            const { fontSize } = options;
            if (fontSize && fontSize > 9) {
                try {
                    await settingRegistry.set(plugin.id, 'fontSize', fontSize - 1);
                }
                catch (err) {
                    Private.showErrorMessage(err);
                }
            }
        }
    });
    const themeDisplayedName = {
        inherit: trans.__('Inherit'),
        light: trans.__('Light'),
        dark: trans.__('Dark')
    };
    commands.addCommand(CommandIDs.setTheme, {
        label: args => {
            const theme = args['theme'];
            const displayName = theme in themeDisplayedName
                ? themeDisplayedName[theme]
                : trans.__(theme[0].toUpperCase() + theme.slice(1));
            return args['isPalette']
                ? trans.__('Use Terminal Theme: %1', displayName)
                : displayName;
        },
        caption: trans.__('Set the terminal theme'),
        isToggled: args => {
            const { theme } = options;
            return args['theme'] === theme;
        },
        execute: async (args) => {
            const theme = args['theme'];
            try {
                await settingRegistry.set(plugin.id, 'theme', theme);
                commands.notifyCommandChanged(CommandIDs.setTheme);
            }
            catch (err) {
                console.log(err);
                Private.showErrorMessage(err);
            }
        }
    });
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Lazy-load the widget (and xterm library and addons)
     */
    function ensureWidget() {
        if (Private.widgetReady) {
            return Private.widgetReady;
        }
        Private.widgetReady = Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_xterm-addon-fit_lib_xterm-addon-fit_js-node_modules_xterm_lib_xterm_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_messaging_lumino_messaging"), __webpack_require__.e("webpack_sharing_consume_default_lumino_domutils_lumino_domutils"), __webpack_require__.e("packages_terminal_lib_widget_js")]).then(__webpack_require__.bind(__webpack_require__, /*! @jupyterlab/terminal/lib/widget */ "../packages/terminal/lib/widget.js"));
        return Private.widgetReady;
    }
    Private.ensureWidget = ensureWidget;
    /**
     *  Utility function for consistent error reporting
     */
    function showErrorMessage(error) {
        console.error(`Failed to configure ${plugin.id}: ${error.message}`);
    }
    Private.showErrorMessage = showErrorMessage;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdGVybWluYWwtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU04QjtBQU1IO0FBQ21CO0FBQ1c7QUFDb0I7QUFFakI7QUFDSTtBQUdiO0FBQ0c7QUFDYjtBQUNMO0FBRXZDOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBWW5CO0FBWkQsV0FBVSxVQUFVO0lBQ0wsb0JBQVMsR0FBRyxxQkFBcUIsQ0FBQztJQUVsQyxlQUFJLEdBQUcsZUFBZSxDQUFDO0lBRXZCLGtCQUFPLEdBQUcsa0JBQWtCLENBQUM7SUFFN0IsdUJBQVksR0FBRyx3QkFBd0IsQ0FBQztJQUV4Qyx1QkFBWSxHQUFHLHdCQUF3QixDQUFDO0lBRXhDLG1CQUFRLEdBQUcsb0JBQW9CLENBQUM7QUFDL0MsQ0FBQyxFQVpTLFVBQVUsS0FBVixVQUFVLFFBWW5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBNEM7SUFDdEQsUUFBUTtJQUNSLEVBQUUsRUFBRSx1Q0FBdUM7SUFDM0MsUUFBUSxFQUFFLGtFQUFnQjtJQUMxQixRQUFRLEVBQUUsQ0FBQyx5RUFBZ0IsRUFBRSxnRUFBVyxDQUFDO0lBQ3pDLFFBQVEsRUFBRTtRQUNSLGlFQUFlO1FBQ2YsMkRBQVM7UUFDVCxvRUFBZTtRQUNmLDJEQUFTO1FBQ1QsK0RBQWE7UUFDYix3RUFBdUI7S0FDeEI7SUFDRCxTQUFTLEVBQUUsSUFBSTtDQUNoQixDQUFDO0FBRUY7O0dBRUc7QUFDSCxpRUFBZSxNQUFNLEVBQUM7QUFFdEI7O0dBRUc7QUFDSCxTQUFTLFFBQVEsQ0FDZixHQUFvQixFQUNwQixlQUFpQyxFQUNqQyxVQUF1QixFQUN2QixPQUErQixFQUMvQixRQUEwQixFQUMxQixRQUFn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SSxDQUFDLE9BQU8sQ0FBQyxLQUFLLEtBQUssQ0FBQztRQUNqQyxDQUFDO1FBQ0QsT0FBTyxFQUFFLEtBQUssRUFBQyxJQUFJLEVBQUMsRUFBRTtZQUNwQixNQUFNLEtBQUssR0FBRyxJQUFJLENBQUMsT0FBTyxDQUFvQixDQUFDO1lBQy9DLElBQUk7Z0JBQ0YsTUFBTSxlQUFlLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQyxFQUFFLEVBQUUsT0FBTyxFQUFFLEtBQUssQ0FBQyxDQUFDO2dCQUNyRCxRQUFRLENBQUMsb0JBQW9CLENBQUMsVUFBVSxDQUFDLFFBQVEsQ0FBQyxDQUFDO2FBQ3BEO1lBQUMsT0FBTyxHQUFHLEVBQUU7Z0JBQ1osT0FBTyxDQUFDLEdBQUcsQ0FBQyxHQUFHLENBQUMsQ0FBQztnQkFDakIsT0FBTyxDQUFDLGdCQUFnQixDQUFDLEdBQUcsQ0FBQyxDQUFDO2FBQy9CO1FBQ0gsQ0FBQztLQUNGLENBQUMsQ0FBQztBQUNMLENBQUM7QUFFRDs7R0FFRztBQUNILElBQVUsT0FBTyxDQXlCaEI7QUF6QkQsV0FBVSxPQUFPO0lBTWY7O09BRUc7SUFDSCxTQUFnQixZQUFZO1FBQzFCLElBQUksbUJBQVcsRUFBRTtZQUNmLE9BQU8sbUJBQVcsQ0FBQztTQUNwQjtRQUVELG1CQUFXLEdBQUcsK2xCQUF5QyxDQUFDO1FBRXhELE9BQU8sbUJBQVcsQ0FBQztJQUNyQixDQUFDO0lBUmUsb0JBQVksZUFRM0I7SUFFRDs7T0FFRztJQUNILFNBQWdCLGdCQUFnQixDQUFDLEtBQVk7UUFDM0MsT0FBTyxDQUFDLEtBQUssQ0FBQyx1QkFBdUIsTUFBTSxDQUFDLEVBQUUsS0FBSyxLQUFLLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztJQUN0RSxDQUFDO0lBRmUsd0JBQWdCLG1CQUUvQjtBQUNILENBQUMsRUF6QlMsT0FBTyxLQUFQLE9BQU8sUUF5QmhCIiwiZmlsZSI6InBhY2thZ2VzX3Rlcm1pbmFsLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuYTJiODQ5OWE1YjUzNmUwZDU3ZmIuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSB0ZXJtaW5hbC1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGF5b3V0UmVzdG9yZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgSVRoZW1lTWFuYWdlcixcbiAgTWFpbkFyZWFXaWRnZXQsXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSUxhdW5jaGVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbGF1bmNoZXInO1xuaW1wb3J0IHsgSUZpbGVNZW51LCBJTWFpbk1lbnUgfSBmcm9tICdAanVweXRlcmxhYi9tYWlubWVudSc7XG5pbXBvcnQgeyBJUnVubmluZ1Nlc3Npb25NYW5hZ2VycywgSVJ1bm5pbmdTZXNzaW9ucyB9IGZyb20gJ0BqdXB5dGVybGFiL3J1bm5pbmcnO1xuaW1wb3J0IHsgVGVybWluYWwgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElUZXJtaW5hbCwgSVRlcm1pbmFsVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL3Rlcm1pbmFsJztcbi8vIE5hbWUtb25seSBpbXBvcnQgc28gYXMgdG8gbm90IHRyaWdnZXIgaW5jbHVzaW9uIGluIG1haW4gYnVuZGxlXG5pbXBvcnQgKiBhcyBXaWRnZXRNb2R1bGVUeXBlIGZyb20gJ0BqdXB5dGVybGFiL3Rlcm1pbmFsL2xpYi93aWRnZXQnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyB0ZXJtaW5hbEljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IHRvQXJyYXkgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBNZW51IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgdGVybWluYWwgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjcmVhdGVOZXcgPSAndGVybWluYWw6Y3JlYXRlLW5ldyc7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW4gPSAndGVybWluYWw6b3Blbic7XG5cbiAgZXhwb3J0IGNvbnN0IHJlZnJlc2ggPSAndGVybWluYWw6cmVmcmVzaCc7XG5cbiAgZXhwb3J0IGNvbnN0IGluY3JlYXNlRm9udCA9ICd0ZXJtaW5hbDppbmNyZWFzZS1mb250JztcblxuICBleHBvcnQgY29uc3QgZGVjcmVhc2VGb250ID0gJ3Rlcm1pbmFsOmRlY3JlYXNlLWZvbnQnO1xuXG4gIGV4cG9ydCBjb25zdCBzZXRUaGVtZSA9ICd0ZXJtaW5hbDpzZXQtdGhlbWUnO1xufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IHRlcm1pbmFsIGV4dGVuc2lvbi5cbiAqL1xuY29uc3QgcGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SVRlcm1pbmFsVHJhY2tlcj4gPSB7XG4gIGFjdGl2YXRlLFxuICBpZDogJ0BqdXB5dGVybGFiL3Rlcm1pbmFsLWV4dGVuc2lvbjpwbHVnaW4nLFxuICBwcm92aWRlczogSVRlcm1pbmFsVHJhY2tlcixcbiAgcmVxdWlyZXM6IFtJU2V0dGluZ1JlZ2lzdHJ5LCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbXG4gICAgSUNvbW1hbmRQYWxldHRlLFxuICAgIElMYXVuY2hlcixcbiAgICBJTGF5b3V0UmVzdG9yZXIsXG4gICAgSU1haW5NZW51LFxuICAgIElUaGVtZU1hbmFnZXIsXG4gICAgSVJ1bm5pbmdTZXNzaW9uTWFuYWdlcnNcbiAgXSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2luIGFzIGRlZmF1bHQuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcblxuLyoqXG4gKiBBY3RpdmF0ZSB0aGUgdGVybWluYWwgcGx1Z2luLlxuICovXG5mdW5jdGlvbiBhY3RpdmF0ZShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGwsXG4gIGxhdW5jaGVyOiBJTGF1bmNoZXIgfCBudWxsLFxuICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbCxcbiAgbWFpbk1lbnU6IElNYWluTWVudSB8IG51bGwsXG4gIHRoZW1lTWFuYWdlcjogSVRoZW1lTWFuYWdlciB8IG51bGwsXG4gIHJ1bm5pbmdTZXNzaW9uTWFuYWdlcnM6IElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzIHwgbnVsbFxuKTogSVRlcm1pbmFsVHJhY2tlciB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgc2VydmljZU1hbmFnZXIsIGNvbW1hbmRzIH0gPSBhcHA7XG4gIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ1Rlcm1pbmFsJyk7XG4gIGNvbnN0IG5hbWVzcGFjZSA9ICd0ZXJtaW5hbCc7XG4gIGNvbnN0IHRyYWNrZXIgPSBuZXcgV2lkZ2V0VHJhY2tlcjxNYWluQXJlYVdpZGdldDxJVGVybWluYWwuSVRlcm1pbmFsPj4oe1xuICAgIG5hbWVzcGFjZVxuICB9KTtcblxuICAvLyBCYWlsIGlmIHRoZXJlIGFyZSBubyB0ZXJtaW5hbHMgYXZhaWxhYmxlLlxuICBpZiAoIXNlcnZpY2VNYW5hZ2VyLnRlcm1pbmFscy5pc0F2YWlsYWJsZSgpKSB7XG4gICAgY29uc29sZS53YXJuKFxuICAgICAgJ0Rpc2FibGluZyB0ZXJtaW5hbHMgcGx1Z2luIGJlY2F1c2UgdGhleSBhcmUgbm90IGF2YWlsYWJsZSBvbiB0aGUgc2VydmVyJ1xuICAgICk7XG4gICAgcmV0dXJuIHRyYWNrZXI7XG4gIH1cblxuICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gIGlmIChyZXN0b3Jlcikge1xuICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZSh0cmFja2VyLCB7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLmNyZWF0ZU5ldyxcbiAgICAgIGFyZ3M6IHdpZGdldCA9PiAoeyBuYW1lOiB3aWRnZXQuY29udGVudC5zZXNzaW9uLm5hbWUgfSksXG4gICAgICBuYW1lOiB3aWRnZXQgPT4gd2lkZ2V0LmNvbnRlbnQuc2Vzc2lvbi5uYW1lXG4gICAgfSk7XG4gIH1cblxuICAvLyBUaGUgY2FjaGVkIHRlcm1pbmFsIG9wdGlvbnMgZnJvbSB0aGUgc2V0dGluZyBlZGl0b3IuXG4gIGNvbnN0IG9wdGlvbnM6IFBhcnRpYWw8SVRlcm1pbmFsLklPcHRpb25zPiA9IHt9O1xuXG4gIC8qKlxuICAgKiBVcGRhdGUgdGhlIGNhY2hlZCBvcHRpb24gdmFsdWVzLlxuICAgKi9cbiAgZnVuY3Rpb24gdXBkYXRlT3B0aW9ucyhzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MpOiB2b2lkIHtcbiAgICAvLyBVcGRhdGUgdGhlIGNhY2hlZCBvcHRpb25zIGJ5IGRvaW5nIGEgc2hhbGxvdyBjb3B5IG9mIGtleS92YWx1ZXMuXG4gICAgLy8gVGhpcyBpcyBuZWVkZWQgYmVjYXVzZSBvcHRpb25zIGlzIHBhc3NlZCBhbmQgdXNlZCBpbiBhZGRjb21tYW5kLXBhbGV0dGUgYW5kIG5lZWRzXG4gICAgLy8gdG8gcmVmbGVjdCB0aGUgY3VycmVudCBjYWNoZWQgdmFsdWVzLlxuICAgIE9iamVjdC5rZXlzKHNldHRpbmdzLmNvbXBvc2l0ZSkuZm9yRWFjaCgoa2V5OiBrZXlvZiBJVGVybWluYWwuSU9wdGlvbnMpID0+IHtcbiAgICAgIChvcHRpb25zIGFzIGFueSlba2V5XSA9IHNldHRpbmdzLmNvbXBvc2l0ZVtrZXldO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0ZXJtaW5hbFxuICAgKi9cbiAgZnVuY3Rpb24gdXBkYXRlVGVybWluYWwod2lkZ2V0OiBNYWluQXJlYVdpZGdldDxJVGVybWluYWwuSVRlcm1pbmFsPik6IHZvaWQge1xuICAgIGNvbnN0IHRlcm1pbmFsID0gd2lkZ2V0LmNvbnRlbnQ7XG4gICAgaWYgKCF0ZXJtaW5hbCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBPYmplY3Qua2V5cyhvcHRpb25zKS5mb3JFYWNoKChrZXk6IGtleW9mIElUZXJtaW5hbC5JT3B0aW9ucykgPT4ge1xuICAgICAgdGVybWluYWwuc2V0T3B0aW9uKGtleSwgb3B0aW9uc1trZXldKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBVcGRhdGUgdGhlIHNldHRpbmdzIG9mIHRoZSBjdXJyZW50IHRyYWNrZXIgaW5zdGFuY2VzLlxuICAgKi9cbiAgZnVuY3Rpb24gdXBkYXRlVHJhY2tlcigpOiB2b2lkIHtcbiAgICB0cmFja2VyLmZvckVhY2god2lkZ2V0ID0+IHVwZGF0ZVRlcm1pbmFsKHdpZGdldCkpO1xuICB9XG5cbiAgLy8gRmV0Y2ggdGhlIGluaXRpYWwgc3RhdGUgb2YgdGhlIHNldHRpbmdzLlxuICBzZXR0aW5nUmVnaXN0cnlcbiAgICAubG9hZChwbHVnaW4uaWQpXG4gICAgLnRoZW4oc2V0dGluZ3MgPT4ge1xuICAgICAgdXBkYXRlT3B0aW9ucyhzZXR0aW5ncyk7XG4gICAgICB1cGRhdGVUcmFja2VyKCk7XG4gICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICB1cGRhdGVPcHRpb25zKHNldHRpbmdzKTtcbiAgICAgICAgdXBkYXRlVHJhY2tlcigpO1xuICAgICAgfSk7XG4gICAgfSlcbiAgICAuY2F0Y2goUHJpdmF0ZS5zaG93RXJyb3JNZXNzYWdlKTtcblxuICAvLyBTdWJzY3JpYmUgdG8gY2hhbmdlcyBpbiB0aGVtZS4gVGhpcyBpcyBuZWVkZWQgYXMgdGhlIHRoZW1lXG4gIC8vIGlzIGNvbXB1dGVkIGR5bmFtaWNhbGx5IGJhc2VkIG9uIHRoZSBzdHJpbmcgdmFsdWUgYW5kIERPTVxuICAvLyBwcm9wZXJ0aWVzLlxuICB0aGVtZU1hbmFnZXI/LnRoZW1lQ2hhbmdlZC5jb25uZWN0KChzZW5kZXIsIGFyZ3MpID0+IHtcbiAgICB0cmFja2VyLmZvckVhY2god2lkZ2V0ID0+IHtcbiAgICAgIGNvbnN0IHRlcm1pbmFsID0gd2lkZ2V0LmNvbnRlbnQ7XG4gICAgICBpZiAodGVybWluYWwuZ2V0T3B0aW9uKCd0aGVtZScpID09PSAnaW5oZXJpdCcpIHtcbiAgICAgICAgdGVybWluYWwuc2V0T3B0aW9uKCd0aGVtZScsICdpbmhlcml0Jyk7XG4gICAgICB9XG4gICAgfSk7XG4gIH0pO1xuXG4gIGFkZENvbW1hbmRzKGFwcCwgdHJhY2tlciwgc2V0dGluZ1JlZ2lzdHJ5LCB0cmFuc2xhdG9yLCBvcHRpb25zKTtcblxuICBpZiAobWFpbk1lbnUpIHtcbiAgICAvLyBBZGQgXCJUZXJtaW5hbCBUaGVtZVwiIG1lbnUgYmVsb3cgXCJUaGVtZVwiIG1lbnUuXG4gICAgY29uc3QgdGhlbWVNZW51ID0gbmV3IE1lbnUoeyBjb21tYW5kcyB9KTtcbiAgICB0aGVtZU1lbnUudGl0bGUubGFiZWwgPSB0cmFucy5fcCgnbWVudScsICdUZXJtaW5hbCBUaGVtZScpO1xuICAgIHRoZW1lTWVudS5hZGRJdGVtKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuc2V0VGhlbWUsXG4gICAgICBhcmdzOiB7XG4gICAgICAgIHRoZW1lOiAnaW5oZXJpdCcsXG4gICAgICAgIGRpc3BsYXlOYW1lOiB0cmFucy5fXygnSW5oZXJpdCcpLFxuICAgICAgICBpc1BhbGV0dGU6IGZhbHNlXG4gICAgICB9XG4gICAgfSk7XG4gICAgdGhlbWVNZW51LmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5zZXRUaGVtZSxcbiAgICAgIGFyZ3M6IHtcbiAgICAgICAgdGhlbWU6ICdsaWdodCcsXG4gICAgICAgIGRpc3BsYXlOYW1lOiB0cmFucy5fXygnTGlnaHQnKSxcbiAgICAgICAgaXNQYWxldHRlOiBmYWxzZVxuICAgICAgfVxuICAgIH0pO1xuICAgIHRoZW1lTWVudS5hZGRJdGVtKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuc2V0VGhlbWUsXG4gICAgICBhcmdzOiB7IHRoZW1lOiAnZGFyaycsIGRpc3BsYXlOYW1lOiB0cmFucy5fXygnRGFyaycpLCBpc1BhbGV0dGU6IGZhbHNlIH1cbiAgICB9KTtcblxuICAgIC8vIEFkZCBzb21lIGNvbW1hbmRzIHRvIHRoZSBcIlZpZXdcIiBtZW51LlxuICAgIG1haW5NZW51LnNldHRpbmdzTWVudS5hZGRHcm91cChcbiAgICAgIFtcbiAgICAgICAgeyBjb21tYW5kOiBDb21tYW5kSURzLmluY3JlYXNlRm9udCB9LFxuICAgICAgICB7IGNvbW1hbmQ6IENvbW1hbmRJRHMuZGVjcmVhc2VGb250IH0sXG4gICAgICAgIHsgdHlwZTogJ3N1Ym1lbnUnLCBzdWJtZW51OiB0aGVtZU1lbnUgfVxuICAgICAgXSxcbiAgICAgIDQwXG4gICAgKTtcblxuICAgIC8vIEFkZCB0ZXJtaW5hbCBjcmVhdGlvbiB0byB0aGUgZmlsZSBtZW51LlxuICAgIG1haW5NZW51LmZpbGVNZW51Lm5ld01lbnUuYWRkSXRlbSh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLmNyZWF0ZU5ldyxcbiAgICAgIHJhbms6IDIwXG4gICAgfSk7XG5cbiAgICAvLyBBZGQgdGVybWluYWwgY2xvc2UtYW5kLXNodXRkb3duIHRvIHRoZSBmaWxlIG1lbnUuXG4gICAgbWFpbk1lbnUuZmlsZU1lbnUuY2xvc2VBbmRDbGVhbmVycy5hZGQoe1xuICAgICAgdHJhY2tlcixcbiAgICAgIGNsb3NlQW5kQ2xlYW51cExhYmVsOiAobjogbnVtYmVyKSA9PiB0cmFucy5fXygnU2h1dGRvd24gVGVybWluYWwnKSxcbiAgICAgIGNsb3NlQW5kQ2xlYW51cDogKGN1cnJlbnQ6IE1haW5BcmVhV2lkZ2V0PElUZXJtaW5hbC5JVGVybWluYWw+KSA9PiB7XG4gICAgICAgIC8vIFRoZSB3aWRnZXQgaXMgYXV0b21hdGljYWxseSBkaXNwb3NlZCB1cG9uIHNlc3Npb24gc2h1dGRvd24uXG4gICAgICAgIHJldHVybiBjdXJyZW50LmNvbnRlbnQuc2Vzc2lvbi5zaHV0ZG93bigpO1xuICAgICAgfVxuICAgIH0gYXMgSUZpbGVNZW51LklDbG9zZUFuZENsZWFuZXI8TWFpbkFyZWFXaWRnZXQ8SVRlcm1pbmFsLklUZXJtaW5hbD4+KTtcbiAgfVxuXG4gIGlmIChwYWxldHRlKSB7XG4gICAgLy8gQWRkIGNvbW1hbmQgcGFsZXR0ZSBpdGVtcy5cbiAgICBbXG4gICAgICBDb21tYW5kSURzLmNyZWF0ZU5ldyxcbiAgICAgIENvbW1hbmRJRHMucmVmcmVzaCxcbiAgICAgIENvbW1hbmRJRHMuaW5jcmVhc2VGb250LFxuICAgICAgQ29tbWFuZElEcy5kZWNyZWFzZUZvbnRcbiAgICBdLmZvckVhY2goY29tbWFuZCA9PiB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kLCBjYXRlZ29yeSwgYXJnczogeyBpc1BhbGV0dGU6IHRydWUgfSB9KTtcbiAgICB9KTtcbiAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5zZXRUaGVtZSxcbiAgICAgIGNhdGVnb3J5LFxuICAgICAgYXJnczoge1xuICAgICAgICB0aGVtZTogJ2luaGVyaXQnLFxuICAgICAgICBkaXNwbGF5TmFtZTogdHJhbnMuX18oJ0luaGVyaXQnKSxcbiAgICAgICAgaXNQYWxldHRlOiB0cnVlXG4gICAgICB9XG4gICAgfSk7XG4gICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuc2V0VGhlbWUsXG4gICAgICBjYXRlZ29yeSxcbiAgICAgIGFyZ3M6IHsgdGhlbWU6ICdsaWdodCcsIGRpc3BsYXlOYW1lOiB0cmFucy5fXygnTGlnaHQnKSwgaXNQYWxldHRlOiB0cnVlIH1cbiAgICB9KTtcbiAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5zZXRUaGVtZSxcbiAgICAgIGNhdGVnb3J5LFxuICAgICAgYXJnczogeyB0aGVtZTogJ2RhcmsnLCBkaXNwbGF5TmFtZTogdHJhbnMuX18oJ0RhcmsnKSwgaXNQYWxldHRlOiB0cnVlIH1cbiAgICB9KTtcbiAgfVxuXG4gIC8vIEFkZCBhIGxhdW5jaGVyIGl0ZW0gaWYgdGhlIGxhdW5jaGVyIGlzIGF2YWlsYWJsZS5cbiAgaWYgKGxhdW5jaGVyKSB7XG4gICAgbGF1bmNoZXIuYWRkKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuY3JlYXRlTmV3LFxuICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdPdGhlcicpLFxuICAgICAgcmFuazogMFxuICAgIH0pO1xuICB9XG5cbiAgLy8gQWRkIGEgc2Vzc2lvbnMgbWFuYWdlciBpZiB0aGUgcnVubmluZyBleHRlbnNpb24gaXMgYXZhaWxhYmxlXG4gIGlmIChydW5uaW5nU2Vzc2lvbk1hbmFnZXJzKSB7XG4gICAgYWRkUnVubmluZ1Nlc3Npb25NYW5hZ2VyKHJ1bm5pbmdTZXNzaW9uTWFuYWdlcnMsIGFwcCwgdHJhbnNsYXRvcik7XG4gIH1cblxuICByZXR1cm4gdHJhY2tlcjtcbn1cblxuLyoqXG4gKiBBZGQgdGhlIHJ1bm5pbmcgdGVybWluYWwgbWFuYWdlciB0byB0aGUgcnVubmluZyBwYW5lbC5cbiAqL1xuZnVuY3Rpb24gYWRkUnVubmluZ1Nlc3Npb25NYW5hZ2VyKFxuICBtYW5hZ2VyczogSVJ1bm5pbmdTZXNzaW9uTWFuYWdlcnMsXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuKSB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IG1hbmFnZXIgPSBhcHAuc2VydmljZU1hbmFnZXIudGVybWluYWxzO1xuXG4gIG1hbmFnZXJzLmFkZCh7XG4gICAgbmFtZTogdHJhbnMuX18oJ1Rlcm1pbmFscycpLFxuICAgIHJ1bm5pbmc6ICgpID0+XG4gICAgICB0b0FycmF5KG1hbmFnZXIucnVubmluZygpKS5tYXAobW9kZWwgPT4gbmV3IFJ1bm5pbmdUZXJtaW5hbChtb2RlbCkpLFxuICAgIHNodXRkb3duQWxsOiAoKSA9PiBtYW5hZ2VyLnNodXRkb3duQWxsKCksXG4gICAgcmVmcmVzaFJ1bm5pbmc6ICgpID0+IG1hbmFnZXIucmVmcmVzaFJ1bm5pbmcoKSxcbiAgICBydW5uaW5nQ2hhbmdlZDogbWFuYWdlci5ydW5uaW5nQ2hhbmdlZCxcbiAgICBzaHV0ZG93bkxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duJyksXG4gICAgc2h1dGRvd25BbGxMYWJlbDogdHJhbnMuX18oJ1NodXQgRG93biBBbGwnKSxcbiAgICBzaHV0ZG93bkFsbENvbmZpcm1hdGlvblRleHQ6IHRyYW5zLl9fKFxuICAgICAgJ0FyZSB5b3Ugc3VyZSB5b3Ugd2FudCB0byBwZXJtYW5lbnRseSBzaHV0IGRvd24gYWxsIHJ1bm5pbmcgdGVybWluYWxzPydcbiAgICApXG4gIH0pO1xuXG4gIGNsYXNzIFJ1bm5pbmdUZXJtaW5hbCBpbXBsZW1lbnRzIElSdW5uaW5nU2Vzc2lvbnMuSVJ1bm5pbmdJdGVtIHtcbiAgICBjb25zdHJ1Y3Rvcihtb2RlbDogVGVybWluYWwuSU1vZGVsKSB7XG4gICAgICB0aGlzLl9tb2RlbCA9IG1vZGVsO1xuICAgIH1cbiAgICBvcGVuKCkge1xuICAgICAgdm9pZCBhcHAuY29tbWFuZHMuZXhlY3V0ZSgndGVybWluYWw6b3BlbicsIHsgbmFtZTogdGhpcy5fbW9kZWwubmFtZSB9KTtcbiAgICB9XG4gICAgaWNvbigpIHtcbiAgICAgIHJldHVybiB0ZXJtaW5hbEljb247XG4gICAgfVxuICAgIGxhYmVsKCkge1xuICAgICAgcmV0dXJuIGB0ZXJtaW5hbHMvJHt0aGlzLl9tb2RlbC5uYW1lfWA7XG4gICAgfVxuICAgIHNodXRkb3duKCkge1xuICAgICAgcmV0dXJuIG1hbmFnZXIuc2h1dGRvd24odGhpcy5fbW9kZWwubmFtZSk7XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfbW9kZWw6IFRlcm1pbmFsLklNb2RlbDtcbiAgfVxufVxuXG4vKipcbiAqIEFkZCB0aGUgY29tbWFuZHMgZm9yIHRoZSB0ZXJtaW5hbC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGFkZENvbW1hbmRzKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgdHJhY2tlcjogV2lkZ2V0VHJhY2tlcjxNYWluQXJlYVdpZGdldDxJVGVybWluYWwuSVRlcm1pbmFsPj4sXG4gIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIG9wdGlvbnM6IFBhcnRpYWw8SVRlcm1pbmFsLklPcHRpb25zPlxuKTogdm9pZCB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgY29tbWFuZHMsIHNlcnZpY2VNYW5hZ2VyIH0gPSBhcHA7XG5cbiAgLy8gQWRkIHRlcm1pbmFsIGNvbW1hbmRzLlxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY3JlYXRlTmV3LCB7XG4gICAgbGFiZWw6IGFyZ3MgPT5cbiAgICAgIGFyZ3NbJ2lzUGFsZXR0ZSddID8gdHJhbnMuX18oJ05ldyBUZXJtaW5hbCcpIDogdHJhbnMuX18oJ1Rlcm1pbmFsJyksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ1N0YXJ0IGEgbmV3IHRlcm1pbmFsIHNlc3Npb24nKSxcbiAgICBpY29uOiBhcmdzID0+IChhcmdzWydpc1BhbGV0dGUnXSA/IHVuZGVmaW5lZCA6IHRlcm1pbmFsSWNvbiksXG4gICAgZXhlY3V0ZTogYXN5bmMgYXJncyA9PiB7XG4gICAgICAvLyB3YWl0IGZvciB0aGUgd2lkZ2V0IHRvIGxhenkgbG9hZFxuICAgICAgbGV0IFRlcm1pbmFsOiB0eXBlb2YgV2lkZ2V0TW9kdWxlVHlwZS5UZXJtaW5hbDtcbiAgICAgIHRyeSB7XG4gICAgICAgIFRlcm1pbmFsID0gKGF3YWl0IFByaXZhdGUuZW5zdXJlV2lkZ2V0KCkpLlRlcm1pbmFsO1xuICAgICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICAgIFByaXZhdGUuc2hvd0Vycm9yTWVzc2FnZShlcnIpO1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IG5hbWUgPSBhcmdzWyduYW1lJ10gYXMgc3RyaW5nO1xuXG4gICAgICBjb25zdCBzZXNzaW9uID0gYXdhaXQgKG5hbWVcbiAgICAgICAgPyBzZXJ2aWNlTWFuYWdlci50ZXJtaW5hbHMuY29ubmVjdFRvKHsgbW9kZWw6IHsgbmFtZSB9IH0pXG4gICAgICAgIDogc2VydmljZU1hbmFnZXIudGVybWluYWxzLnN0YXJ0TmV3KCkpO1xuXG4gICAgICBjb25zdCB0ZXJtID0gbmV3IFRlcm1pbmFsKHNlc3Npb24sIG9wdGlvbnMsIHRyYW5zbGF0b3IpO1xuXG4gICAgICB0ZXJtLnRpdGxlLmljb24gPSB0ZXJtaW5hbEljb247XG4gICAgICB0ZXJtLnRpdGxlLmxhYmVsID0gJy4uLic7XG5cbiAgICAgIGNvbnN0IG1haW4gPSBuZXcgTWFpbkFyZWFXaWRnZXQoeyBjb250ZW50OiB0ZXJtIH0pO1xuICAgICAgYXBwLnNoZWxsLmFkZChtYWluKTtcbiAgICAgIHZvaWQgdHJhY2tlci5hZGQobWFpbik7XG4gICAgICBhcHAuc2hlbGwuYWN0aXZhdGVCeUlkKG1haW4uaWQpO1xuICAgICAgcmV0dXJuIG1haW47XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3Blbiwge1xuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgbmFtZSA9IGFyZ3NbJ25hbWUnXSBhcyBzdHJpbmc7XG4gICAgICAvLyBDaGVjayBmb3IgYSBydW5uaW5nIHRlcm1pbmFsIHdpdGggdGhlIGdpdmVuIG5hbWUuXG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmZpbmQodmFsdWUgPT4ge1xuICAgICAgICBjb25zdCBjb250ZW50ID0gdmFsdWUuY29udGVudDtcbiAgICAgICAgcmV0dXJuIGNvbnRlbnQuc2Vzc2lvbi5uYW1lID09PSBuYW1lIHx8IGZhbHNlO1xuICAgICAgfSk7XG4gICAgICBpZiAod2lkZ2V0KSB7XG4gICAgICAgIGFwcC5zaGVsbC5hY3RpdmF0ZUJ5SWQod2lkZ2V0LmlkKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIC8vIE90aGVyd2lzZSwgY3JlYXRlIGEgbmV3IHRlcm1pbmFsIHdpdGggYSBnaXZlbiBuYW1lLlxuICAgICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLmNyZWF0ZU5ldywgeyBuYW1lIH0pO1xuICAgICAgfVxuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJlZnJlc2gsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1JlZnJlc2ggVGVybWluYWwnKSxcbiAgICBjYXB0aW9uOiB0cmFucy5fXygnUmVmcmVzaCB0aGUgY3VycmVudCB0ZXJtaW5hbCBzZXNzaW9uJyksXG4gICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3QgY3VycmVudCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICAgIGlmICghY3VycmVudCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBhcHAuc2hlbGwuYWN0aXZhdGVCeUlkKGN1cnJlbnQuaWQpO1xuICAgICAgdHJ5IHtcbiAgICAgICAgYXdhaXQgY3VycmVudC5jb250ZW50LnJlZnJlc2goKTtcbiAgICAgICAgaWYgKGN1cnJlbnQpIHtcbiAgICAgICAgICBjdXJyZW50LmNvbnRlbnQuYWN0aXZhdGUoKTtcbiAgICAgICAgfVxuICAgICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICAgIFByaXZhdGUuc2hvd0Vycm9yTWVzc2FnZShlcnIpO1xuICAgICAgfVxuICAgIH0sXG4gICAgaXNFbmFibGVkOiAoKSA9PiB0cmFja2VyLmN1cnJlbnRXaWRnZXQgIT09IG51bGxcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmluY3JlYXNlRm9udCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnSW5jcmVhc2UgVGVybWluYWwgRm9udCBTaXplJyksXG4gICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3QgeyBmb250U2l6ZSB9ID0gb3B0aW9ucztcbiAgICAgIGlmIChmb250U2l6ZSAmJiBmb250U2l6ZSA8IDcyKSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgYXdhaXQgc2V0dGluZ1JlZ2lzdHJ5LnNldChwbHVnaW4uaWQsICdmb250U2l6ZScsIGZvbnRTaXplICsgMSk7XG4gICAgICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgICAgIFByaXZhdGUuc2hvd0Vycm9yTWVzc2FnZShlcnIpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuZGVjcmVhc2VGb250LCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdEZWNyZWFzZSBUZXJtaW5hbCBGb250IFNpemUnKSxcbiAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICBjb25zdCB7IGZvbnRTaXplIH0gPSBvcHRpb25zO1xuICAgICAgaWYgKGZvbnRTaXplICYmIGZvbnRTaXplID4gOSkge1xuICAgICAgICB0cnkge1xuICAgICAgICAgIGF3YWl0IHNldHRpbmdSZWdpc3RyeS5zZXQocGx1Z2luLmlkLCAnZm9udFNpemUnLCBmb250U2l6ZSAtIDEpO1xuICAgICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgICBQcml2YXRlLnNob3dFcnJvck1lc3NhZ2UoZXJyKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgfSk7XG5cbiAgY29uc3QgdGhlbWVEaXNwbGF5ZWROYW1lID0ge1xuICAgIGluaGVyaXQ6IHRyYW5zLl9fKCdJbmhlcml0JyksXG4gICAgbGlnaHQ6IHRyYW5zLl9fKCdMaWdodCcpLFxuICAgIGRhcms6IHRyYW5zLl9fKCdEYXJrJylcbiAgfTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2V0VGhlbWUsIHtcbiAgICBsYWJlbDogYXJncyA9PiB7XG4gICAgICBjb25zdCB0aGVtZSA9IGFyZ3NbJ3RoZW1lJ10gYXMgc3RyaW5nO1xuICAgICAgY29uc3QgZGlzcGxheU5hbWUgPVxuICAgICAgICB0aGVtZSBpbiB0aGVtZURpc3BsYXllZE5hbWVcbiAgICAgICAgICA/IHRoZW1lRGlzcGxheWVkTmFtZVt0aGVtZSBhcyBrZXlvZiB0eXBlb2YgdGhlbWVEaXNwbGF5ZWROYW1lXVxuICAgICAgICAgIDogdHJhbnMuX18odGhlbWVbMF0udG9VcHBlckNhc2UoKSArIHRoZW1lLnNsaWNlKDEpKTtcbiAgICAgIHJldHVybiBhcmdzWydpc1BhbGV0dGUnXVxuICAgICAgICA/IHRyYW5zLl9fKCdVc2UgVGVybWluYWwgVGhlbWU6ICUxJywgZGlzcGxheU5hbWUpXG4gICAgICAgIDogZGlzcGxheU5hbWU7XG4gICAgfSxcbiAgICBjYXB0aW9uOiB0cmFucy5fXygnU2V0IHRoZSB0ZXJtaW5hbCB0aGVtZScpLFxuICAgIGlzVG9nZ2xlZDogYXJncyA9PiB7XG4gICAgICBjb25zdCB7IHRoZW1lIH0gPSBvcHRpb25zO1xuICAgICAgcmV0dXJuIGFyZ3NbJ3RoZW1lJ10gPT09IHRoZW1lO1xuICAgIH0sXG4gICAgZXhlY3V0ZTogYXN5bmMgYXJncyA9PiB7XG4gICAgICBjb25zdCB0aGVtZSA9IGFyZ3NbJ3RoZW1lJ10gYXMgSVRlcm1pbmFsLlRoZW1lO1xuICAgICAgdHJ5IHtcbiAgICAgICAgYXdhaXQgc2V0dGluZ1JlZ2lzdHJ5LnNldChwbHVnaW4uaWQsICd0aGVtZScsIHRoZW1lKTtcbiAgICAgICAgY29tbWFuZHMubm90aWZ5Q29tbWFuZENoYW5nZWQoQ29tbWFuZElEcy5zZXRUaGVtZSk7XG4gICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgY29uc29sZS5sb2coZXJyKTtcbiAgICAgICAgUHJpdmF0ZS5zaG93RXJyb3JNZXNzYWdlKGVycik7XG4gICAgICB9XG4gICAgfVxuICB9KTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBIFByb21pc2UgZm9yIHRoZSBpbml0aWFsIGxvYWQgb2YgdGhlIHRlcm1pbmFsIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBsZXQgd2lkZ2V0UmVhZHk6IFByb21pc2U8dHlwZW9mIFdpZGdldE1vZHVsZVR5cGU+O1xuXG4gIC8qKlxuICAgKiBMYXp5LWxvYWQgdGhlIHdpZGdldCAoYW5kIHh0ZXJtIGxpYnJhcnkgYW5kIGFkZG9ucylcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBlbnN1cmVXaWRnZXQoKTogUHJvbWlzZTx0eXBlb2YgV2lkZ2V0TW9kdWxlVHlwZT4ge1xuICAgIGlmICh3aWRnZXRSZWFkeSkge1xuICAgICAgcmV0dXJuIHdpZGdldFJlYWR5O1xuICAgIH1cblxuICAgIHdpZGdldFJlYWR5ID0gaW1wb3J0KCdAanVweXRlcmxhYi90ZXJtaW5hbC9saWIvd2lkZ2V0Jyk7XG5cbiAgICByZXR1cm4gd2lkZ2V0UmVhZHk7XG4gIH1cblxuICAvKipcbiAgICogIFV0aWxpdHkgZnVuY3Rpb24gZm9yIGNvbnNpc3RlbnQgZXJyb3IgcmVwb3J0aW5nXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gc2hvd0Vycm9yTWVzc2FnZShlcnJvcjogRXJyb3IpOiB2b2lkIHtcbiAgICBjb25zb2xlLmVycm9yKGBGYWlsZWQgdG8gY29uZmlndXJlICR7cGx1Z2luLmlkfTogJHtlcnJvci5tZXNzYWdlfWApO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9