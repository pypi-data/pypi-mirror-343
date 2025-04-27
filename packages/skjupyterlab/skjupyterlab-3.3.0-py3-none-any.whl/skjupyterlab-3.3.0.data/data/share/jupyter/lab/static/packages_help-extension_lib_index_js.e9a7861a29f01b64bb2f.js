(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_help-extension_lib_index_js"],{

/***/ "../packages/help-extension/lib/index.js":
/*!***********************************************!*\
  !*** ../packages/help-extension/lib/index.js ***!
  \***********************************************/
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
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _licenses__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./licenses */ "../packages/help-extension/lib/licenses.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module help-extension
 */








/**
 * The command IDs used by the help plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'help:open';
    CommandIDs.about = 'help:about';
    CommandIDs.activate = 'help:activate';
    CommandIDs.close = 'help:close';
    CommandIDs.show = 'help:show';
    CommandIDs.hide = 'help:hide';
    CommandIDs.launchClassic = 'help:launch-classic-notebook';
    CommandIDs.jupyterForum = 'help:jupyter-forum';
    CommandIDs.licenses = 'help:licenses';
    CommandIDs.licenseReport = 'help:license-report';
    CommandIDs.refreshLicenses = 'help:licenses-refresh';
})(CommandIDs || (CommandIDs = {}));
/**
 * A flag denoting whether the application is loaded over HTTPS.
 */
const LAB_IS_SECURE = window.location.protocol === 'https:';
/**
 * The class name added to the help widget.
 */
const HELP_CLASS = 'jp-Help';
/**
 * Add a command to show an About dialog.
 */
const about = {
    id: '@jupyterlab/help-extension:about',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, palette) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        commands.addCommand(CommandIDs.about, {
            label: trans.__('About %1', app.name),
            execute: () => {
                // Create the header of the about dialog
                const versionNumber = trans.__('Version %1', app.version);
                const versionInfo = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-version-info" },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-version" }, versionNumber)));
                const title = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-header" },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.jupyterIcon.react, { margin: "7px 9.5px", height: "auto", width: "58px" }),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "jp-About-header-info" },
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.jupyterlabWordmarkIcon.react, { height: "auto", width: "196px" }),
                        versionInfo)));
                // Create the body of the about dialog
                const jupyterURL = 'https://jupyter.org/about.html';
                const contributorsURL = 'https://github.com/jupyterlab/jupyterlab/graphs/contributors';
                const externalLinks = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-externalLinks" },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("a", { href: contributorsURL, target: "_blank", rel: "noopener noreferrer", className: "jp-Button-flat" }, trans.__('CONTRIBUTOR LIST')),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("a", { href: jupyterURL, target: "_blank", rel: "noopener noreferrer", className: "jp-Button-flat" }, trans.__('ABOUT PROJECT JUPYTER'))));
                const copyright = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-copyright" }, trans.__('© 2015-2021 Project Jupyter Contributors')));
                const body = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "jp-About-body" },
                    externalLinks,
                    copyright));
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title,
                    body,
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.createButton({
                            label: trans.__('Dismiss'),
                            className: 'jp-About-button jp-mod-reject jp-mod-styled'
                        })
                    ]
                });
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.about, category });
        }
    }
};
/**
 * A plugin to add a command to open the Classic Notebook interface.
 */
const launchClassic = {
    id: '@jupyterlab/help-extension:launch-classic',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, palette) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        commands.addCommand(CommandIDs.launchClassic, {
            label: trans.__('Launch Classic Notebook'),
            execute: () => {
                window.open(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getBaseUrl() + 'tree');
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.launchClassic, category });
        }
    }
};
/**
 * A plugin to add a command to open the Jupyter Forum.
 */
const jupyterForum = {
    id: '@jupyterlab/help-extension:jupyter-forum',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, palette) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        commands.addCommand(CommandIDs.jupyterForum, {
            label: trans.__('Jupyter Forum'),
            execute: () => {
                window.open('https://discourse.jupyter.org/c/jupyterlab');
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.jupyterForum, category });
        }
    }
};
/**
 * A plugin to add a list of resources to the help menu.
 */
const resources = {
    id: '@jupyterlab/help-extension:resources',
    autoStart: true,
    requires: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, mainMenu, translator, palette, restorer) => {
        const trans = translator.load('jupyterlab');
        let counter = 0;
        const category = trans.__('Help');
        const namespace = 'help-doc';
        const { commands, shell, serviceManager } = app;
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({ namespace });
        const resources = [
            {
                text: trans.__('JupyterLab Reference'),
                url: 'https://jupyterlab.readthedocs.io/en/3.2.x/'
            },
            {
                text: trans.__('JupyterLab FAQ'),
                url: 'https://jupyterlab.readthedocs.io/en/3.2.x/getting_started/faq.html'
            },
            {
                text: trans.__('Jupyter Reference'),
                url: 'https://jupyter.org/documentation'
            },
            {
                text: trans.__('Markdown Reference'),
                url: 'https://commonmark.org/help/'
            }
        ];
        resources.sort((a, b) => {
            return a.text.localeCompare(b.text);
        });
        // Handle state restoration.
        if (restorer) {
            void restorer.restore(tracker, {
                command: CommandIDs.open,
                args: widget => ({
                    url: widget.content.url,
                    text: widget.content.title.label
                }),
                name: widget => widget.content.url
            });
        }
        /**
         * Create a new HelpWidget widget.
         */
        function newHelpWidget(url, text) {
            // Allow scripts and forms so that things like
            // readthedocs can use their search functionality.
            // We *don't* allow same origin requests, which
            // can prevent some content from being loaded onto the
            // help pages.
            const content = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IFrame({
                sandbox: ['allow-scripts', 'allow-forms']
            });
            content.url = url;
            content.addClass(HELP_CLASS);
            content.title.label = text;
            content.id = `${namespace}-${++counter}`;
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
            widget.addClass('jp-Help');
            return widget;
        }
        // Populate the Help menu.
        const helpMenu = mainMenu.helpMenu;
        const resourcesGroup = resources.map(args => ({
            args,
            command: CommandIDs.open
        }));
        helpMenu.addGroup(resourcesGroup, 10);
        // Generate a cache of the kernel help links.
        const kernelInfoCache = new Map();
        serviceManager.sessions.runningChanged.connect((m, sessions) => {
            var _a;
            // If a new session has been added, it is at the back
            // of the session list. If one has changed or stopped,
            // it does not hurt to check it.
            if (!sessions.length) {
                return;
            }
            const sessionModel = sessions[sessions.length - 1];
            if (!sessionModel.kernel ||
                kernelInfoCache.has(sessionModel.kernel.name)) {
                return;
            }
            const session = serviceManager.sessions.connectTo({
                model: sessionModel,
                kernelConnectionOptions: { handleComms: false }
            });
            void ((_a = session.kernel) === null || _a === void 0 ? void 0 : _a.info.then(kernelInfo => {
                var _a, _b;
                const name = session.kernel.name;
                // Check the cache second time so that, if two callbacks get scheduled,
                // they don't try to add the same commands.
                if (kernelInfoCache.has(name)) {
                    return;
                }
                // Set the Kernel Info cache.
                kernelInfoCache.set(name, kernelInfo);
                // Utility function to check if the current widget
                // has registered itself with the help menu.
                const usesKernel = () => {
                    let result = false;
                    const widget = app.shell.currentWidget;
                    if (!widget) {
                        return result;
                    }
                    helpMenu.kernelUsers.forEach(u => {
                        var _a;
                        if (u.tracker.has(widget) && ((_a = u.getKernel(widget)) === null || _a === void 0 ? void 0 : _a.name) === name) {
                            result = true;
                        }
                    });
                    return result;
                };
                // Add the kernel banner to the Help Menu.
                const bannerCommand = `help-menu-${name}:banner`;
                const spec = (_b = (_a = serviceManager.kernelspecs) === null || _a === void 0 ? void 0 : _a.specs) === null || _b === void 0 ? void 0 : _b.kernelspecs[name];
                if (!spec) {
                    return;
                }
                const kernelName = spec.display_name;
                let kernelIconUrl = spec.resources['logo-64x64'];
                commands.addCommand(bannerCommand, {
                    label: trans.__('About the %1 Kernel', kernelName),
                    isVisible: usesKernel,
                    isEnabled: usesKernel,
                    execute: () => {
                        // Create the header of the about dialog
                        const headerLogo = react__WEBPACK_IMPORTED_MODULE_6__.createElement("img", { src: kernelIconUrl });
                        const title = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-header" },
                            headerLogo,
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "jp-About-header-info" }, kernelName)));
                        const banner = react__WEBPACK_IMPORTED_MODULE_6__.createElement("pre", null, kernelInfo.banner);
                        const body = react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "jp-About-body" }, banner);
                        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title,
                            body,
                            buttons: [
                                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.createButton({
                                    label: trans.__('Dismiss'),
                                    className: 'jp-About-button jp-mod-reject jp-mod-styled'
                                })
                            ]
                        });
                    }
                });
                helpMenu.addGroup([{ command: bannerCommand }], 20);
                // Add the kernel info help_links to the Help menu.
                const kernelGroup = [];
                (kernelInfo.help_links || []).forEach(link => {
                    const commandId = `help-menu-${name}:${link.text}`;
                    commands.addCommand(commandId, {
                        label: link.text,
                        isVisible: usesKernel,
                        isEnabled: usesKernel,
                        execute: () => {
                            return commands.execute(CommandIDs.open, link);
                        }
                    });
                    kernelGroup.push({ command: commandId });
                });
                helpMenu.addGroup(kernelGroup, 21);
                // Dispose of the session object since we no longer need it.
                session.dispose();
            }));
        });
        commands.addCommand(CommandIDs.open, {
            label: args => args['text'],
            execute: args => {
                const url = args['url'];
                const text = args['text'];
                const newBrowserTab = args['newBrowserTab'] || false;
                // If help resource will generate a mixed content error, load externally.
                if (newBrowserTab ||
                    (LAB_IS_SECURE && _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.parse(url).protocol !== 'https:')) {
                    window.open(url);
                    return;
                }
                const widget = newHelpWidget(url, text);
                void tracker.add(widget);
                shell.add(widget, 'main');
                return widget;
            }
        });
        if (palette) {
            resources.forEach(args => {
                palette.addItem({ args, command: CommandIDs.open, category });
            });
            palette.addItem({
                args: { reload: true },
                command: 'apputils:reset',
                category
            });
        }
    }
};
/**
 * A plugin to add a licenses reporting tools.
 */
const licenses = {
    id: '@jupyterlab/help-extension:licenses',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, translator, menu, palette, restorer) => {
        // bail if no license API is available from the server
        if (!_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('licensesUrl')) {
            return;
        }
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        // translation strings
        const category = trans.__('Help');
        const downloadAsText = trans.__('Download All Licenses as');
        const licensesText = trans.__('Licenses');
        const refreshLicenses = trans.__('Refresh Licenses');
        // an incrementer for license widget ids
        let counter = 0;
        const licensesUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getBaseUrl(), _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('licensesUrl')) + '/';
        const licensesNamespace = 'help-licenses';
        const licensesTracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: licensesNamespace
        });
        /**
         * Return a full license report format based on a format name
         */
        function formatOrDefault(format) {
            return (_licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.REPORT_FORMATS[format] ||
                _licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.REPORT_FORMATS[_licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.DEFAULT_FORMAT]);
        }
        /**
         * Create a MainAreaWidget for a license viewer
         */
        function createLicenseWidget(args) {
            const licensesModel = new _licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.Model(Object.assign(Object.assign({}, args), { licensesUrl,
                trans, serverSettings: app.serviceManager.serverSettings }));
            const content = new _licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses({ model: licensesModel });
            content.id = `${licensesNamespace}-${++counter}`;
            content.title.label = licensesText;
            content.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.copyrightIcon;
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                content,
                reveal: licensesModel.licensesReady
            });
            main.toolbar.addItem('refresh-licenses', new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButton({
                id: CommandIDs.refreshLicenses,
                args: { noLabel: 1 },
                commands
            }));
            main.toolbar.addItem('spacer', _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Toolbar.createSpacerItem());
            for (const format of Object.keys(_licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.REPORT_FORMATS)) {
                const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButton({
                    id: CommandIDs.licenseReport,
                    args: { format, noLabel: 1 },
                    commands
                });
                main.toolbar.addItem(`download-${format}`, button);
            }
            return main;
        }
        // register license-related commands
        commands.addCommand(CommandIDs.licenses, {
            label: licensesText,
            execute: (args) => {
                const licenseMain = createLicenseWidget(args);
                shell.add(licenseMain, 'main');
                // add to tracker so it can be restored, and update when choices change
                void licensesTracker.add(licenseMain);
                licenseMain.content.model.trackerDataChanged.connect(() => {
                    void licensesTracker.save(licenseMain);
                });
                return licenseMain;
            }
        });
        commands.addCommand(CommandIDs.refreshLicenses, {
            label: args => (args.noLabel ? '' : refreshLicenses),
            caption: refreshLicenses,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.refreshIcon,
            execute: async () => {
                var _a;
                return (_a = licensesTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model.initLicenses();
            }
        });
        commands.addCommand(CommandIDs.licenseReport, {
            label: args => {
                if (args.noLabel) {
                    return '';
                }
                const format = formatOrDefault(`${args.format}`);
                return `${downloadAsText} ${format.title}`;
            },
            caption: args => {
                const format = formatOrDefault(`${args.format}`);
                return `${downloadAsText} ${format.title}`;
            },
            icon: args => {
                const format = formatOrDefault(`${args.format}`);
                return format.icon;
            },
            execute: async (args) => {
                var _a;
                const format = formatOrDefault(`${args.format}`);
                return await ((_a = licensesTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model.download({
                    format: format.id
                }));
            }
        });
        // handle optional integrations
        if (palette) {
            palette.addItem({ command: CommandIDs.licenses, category });
        }
        if (menu) {
            const helpMenu = menu.helpMenu;
            helpMenu.addGroup([{ command: CommandIDs.licenses }], 0);
        }
        if (restorer) {
            void restorer.restore(licensesTracker, {
                command: CommandIDs.licenses,
                name: widget => 'licenses',
                args: widget => {
                    const { currentBundleName, currentPackageIndex, packageFilter } = widget.content.model;
                    const args = {
                        currentBundleName,
                        currentPackageIndex,
                        packageFilter
                    };
                    return args;
                }
            });
        }
    }
};
const plugins = [
    about,
    launchClassic,
    jupyterForum,
    resources,
    licenses
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "../packages/help-extension/lib/licenses.js":
/*!**************************************************!*\
  !*** ../packages/help-extension/lib/licenses.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Licenses": () => (/* binding */ Licenses)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/virtualdom */ "webpack/sharing/consume/default/@lumino/virtualdom/@lumino/virtualdom");
/* harmony import */ var _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_virtualdom__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * A license viewer
 */
class Licenses extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.SplitPanel {
    constructor(options) {
        super();
        this.addClass('jp-Licenses');
        this.model = options.model;
        this.initLeftPanel();
        this.initFilters();
        this.initBundles();
        this.initGrid();
        this.initLicenseText();
        this.setRelativeSizes([1, 2, 3]);
        void this.model.initLicenses().then(() => this._updateBundles());
        this.model.trackerDataChanged.connect(() => {
            this.title.label = this.model.title;
        });
    }
    /**
     * Handle disposing of the widget
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._bundles.currentChanged.disconnect(this.onBundleSelected, this);
        this.model.dispose();
        super.dispose();
    }
    /**
     * Initialize the left area for filters and bundles
     */
    initLeftPanel() {
        this._leftPanel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Panel();
        this._leftPanel.addClass('jp-Licenses-FormArea');
        this.addWidget(this._leftPanel);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.SplitPanel.setStretch(this._leftPanel, 1);
    }
    /**
     * Initialize the filters
     */
    initFilters() {
        this._filters = new Licenses.Filters(this.model);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.SplitPanel.setStretch(this._filters, 1);
        this._leftPanel.addWidget(this._filters);
    }
    /**
     * Initialize the listing of available bundles
     */
    initBundles() {
        this._bundles = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.TabBar({
            orientation: 'vertical',
            renderer: new Licenses.BundleTabRenderer(this.model)
        });
        this._bundles.addClass('jp-Licenses-Bundles');
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.SplitPanel.setStretch(this._bundles, 1);
        this._leftPanel.addWidget(this._bundles);
        this._bundles.currentChanged.connect(this.onBundleSelected, this);
        this.model.stateChanged.connect(() => this._bundles.update());
    }
    /**
     * Initialize the listing of packages within the current bundle
     */
    initGrid() {
        this._grid = new Licenses.Grid(this.model);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.SplitPanel.setStretch(this._grid, 1);
        this.addWidget(this._grid);
    }
    /**
     * Initialize the full text of the current package
     */
    initLicenseText() {
        this._licenseText = new Licenses.FullText(this.model);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.SplitPanel.setStretch(this._grid, 1);
        this.addWidget(this._licenseText);
    }
    /**
     * Event handler for updating the model with the current bundle
     */
    onBundleSelected() {
        var _a;
        if ((_a = this._bundles.currentTitle) === null || _a === void 0 ? void 0 : _a.label) {
            this.model.currentBundleName = this._bundles.currentTitle.label;
        }
    }
    /**
     * Update the bundle tabs.
     */
    _updateBundles() {
        this._bundles.clearTabs();
        let i = 0;
        const { currentBundleName } = this.model;
        let currentIndex = 0;
        for (const bundle of this.model.bundleNames) {
            const tab = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget();
            tab.title.label = bundle;
            if (bundle === currentBundleName) {
                currentIndex = i;
            }
            this._bundles.insertTab(++i, tab.title);
        }
        this._bundles.currentIndex = currentIndex;
    }
}
/** A namespace for license components */
(function (Licenses) {
    /**
     * License report formats understood by the server (once lower-cased)
     */
    Licenses.REPORT_FORMATS = {
        markdown: {
            id: 'markdown',
            title: 'Markdown',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.markdownIcon
        },
        csv: {
            id: 'csv',
            title: 'CSV',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.spreadsheetIcon
        },
        json: {
            id: 'csv',
            title: 'JSON',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.jsonIcon
        }
    };
    /**
     * The default format (most human-readable)
     */
    Licenses.DEFAULT_FORMAT = 'markdown';
    /**
     * A model for license data
     */
    class Model extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
        constructor(options) {
            super();
            this._selectedPackageChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
            this._trackerDataChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
            this._currentPackageIndex = 0;
            this._licensesReady = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.PromiseDelegate();
            this._packageFilter = {};
            this._trans = options.trans;
            this._licensesUrl = options.licensesUrl;
            this._serverSettings =
                options.serverSettings || _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
            if (options.currentBundleName) {
                this._currentBundleName = options.currentBundleName;
            }
            if (options.packageFilter) {
                this._packageFilter = options.packageFilter;
            }
            if (options.currentPackageIndex) {
                this._currentPackageIndex = options.currentPackageIndex;
            }
        }
        /**
         * Handle the initial request for the licenses from the server.
         */
        async initLicenses() {
            try {
                const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(this._licensesUrl, {}, this._serverSettings);
                this._serverResponse = await response.json();
                this._licensesReady.resolve();
                this.stateChanged.emit(void 0);
            }
            catch (err) {
                this._licensesReady.reject(err);
            }
        }
        /**
         * Create a temporary download link, and emulate clicking it to trigger a named
         * file download.
         */
        async download(options) {
            const url = `${this._licensesUrl}?format=${options.format}&download=1`;
            const element = document.createElement('a');
            element.href = url;
            element.download = '';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            return void 0;
        }
        /**
         * A promise that resolves when the licenses from the server change
         */
        get selectedPackageChanged() {
            return this._selectedPackageChanged;
        }
        /**
         * A promise that resolves when the trackable data changes
         */
        get trackerDataChanged() {
            return this._trackerDataChanged;
        }
        /**
         * The names of the license bundles available
         */
        get bundleNames() {
            var _a;
            return Object.keys(((_a = this._serverResponse) === null || _a === void 0 ? void 0 : _a.bundles) || {});
        }
        /**
         * The current license bundle
         */
        get currentBundleName() {
            if (this._currentBundleName) {
                return this._currentBundleName;
            }
            if (this.bundleNames.length) {
                return this.bundleNames[0];
            }
            return null;
        }
        /**
         * Set the current license bundle, and reset the selected index
         */
        set currentBundleName(currentBundleName) {
            if (this._currentBundleName !== currentBundleName) {
                this._currentBundleName = currentBundleName;
                this.stateChanged.emit(void 0);
                this._trackerDataChanged.emit(void 0);
            }
        }
        /**
         * A promise that resolves when the licenses are available from the server
         */
        get licensesReady() {
            return this._licensesReady.promise;
        }
        /**
         * All the license bundles, keyed by the distributing packages
         */
        get bundles() {
            var _a;
            return ((_a = this._serverResponse) === null || _a === void 0 ? void 0 : _a.bundles) || {};
        }
        /**
         * The index of the currently-selected package within its license bundle
         */
        get currentPackageIndex() {
            return this._currentPackageIndex;
        }
        /**
         * Update the currently-selected package within its license bundle
         */
        set currentPackageIndex(currentPackageIndex) {
            if (this._currentPackageIndex === currentPackageIndex) {
                return;
            }
            this._currentPackageIndex = currentPackageIndex;
            this._selectedPackageChanged.emit(void 0);
            this.stateChanged.emit(void 0);
            this._trackerDataChanged.emit(void 0);
        }
        /**
         * The license data for the currently-selected package
         */
        get currentPackage() {
            var _a;
            if (this.currentBundleName &&
                this.bundles &&
                this._currentPackageIndex != null) {
                return this.getFilteredPackages(((_a = this.bundles[this.currentBundleName]) === null || _a === void 0 ? void 0 : _a.packages) || [])[this._currentPackageIndex];
            }
            return null;
        }
        /**
         * A translation bundle
         */
        get trans() {
            return this._trans;
        }
        get title() {
            return `${this._currentBundleName || ''} ${this._trans.__('Licenses')}`.trim();
        }
        /**
         * The current package filter
         */
        get packageFilter() {
            return this._packageFilter;
        }
        set packageFilter(packageFilter) {
            this._packageFilter = packageFilter;
            this.stateChanged.emit(void 0);
            this._trackerDataChanged.emit(void 0);
        }
        /**
         * Get filtered packages from current bundle where at least one token of each
         * key is present.
         */
        getFilteredPackages(allRows) {
            let rows = [];
            let filters = Object.entries(this._packageFilter)
                .filter(([k, v]) => v && `${v}`.trim().length)
                .map(([k, v]) => [k, `${v}`.toLowerCase().trim().split(' ')]);
            for (const row of allRows) {
                let keyHits = 0;
                for (const [key, bits] of filters) {
                    let bitHits = 0;
                    let rowKeyValue = `${row[key]}`.toLowerCase();
                    for (const bit of bits) {
                        if (rowKeyValue.includes(bit)) {
                            bitHits += 1;
                        }
                    }
                    if (bitHits) {
                        keyHits += 1;
                    }
                }
                if (keyHits === filters.length) {
                    rows.push(row);
                }
            }
            return Object.values(rows);
        }
    }
    Licenses.Model = Model;
    /**
     * A filter form for limiting the packages displayed
     */
    class Filters extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
        constructor(model) {
            super(model);
            /**
             * Render a filter input
             */
            this.renderFilter = (key) => {
                const value = this.model.packageFilter[key] || '';
                return (react__WEBPACK_IMPORTED_MODULE_7__.createElement("input", { type: "text", name: key, defaultValue: value, className: "jp-mod-styled", onInput: this.onFilterInput }));
            };
            /**
             * Handle a filter input changing
             */
            this.onFilterInput = (evt) => {
                const input = evt.currentTarget;
                const { name, value } = input;
                this.model.packageFilter = Object.assign(Object.assign({}, this.model.packageFilter), { [name]: value });
            };
            this.addClass('jp-Licenses-Filters');
            this.addClass('jp-RenderedHTMLCommon');
        }
        render() {
            const { trans } = this.model;
            return (react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_7__.createElement("label", null,
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("strong", null, trans.__('Filter Licenses By'))),
                react__WEBPACK_IMPORTED_MODULE_7__.createElement("ul", null,
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("li", null,
                        react__WEBPACK_IMPORTED_MODULE_7__.createElement("label", null, trans.__('Package')),
                        this.renderFilter('name')),
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("li", null,
                        react__WEBPACK_IMPORTED_MODULE_7__.createElement("label", null, trans.__('Version')),
                        this.renderFilter('versionInfo')),
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("li", null,
                        react__WEBPACK_IMPORTED_MODULE_7__.createElement("label", null, trans.__('License')),
                        this.renderFilter('licenseId'))),
                react__WEBPACK_IMPORTED_MODULE_7__.createElement("label", null,
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("strong", null, trans.__('Distributions')))));
        }
    }
    Licenses.Filters = Filters;
    /**
     * A fancy bundle renderer with the package count
     */
    class BundleTabRenderer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.TabBar.Renderer {
        constructor(model) {
            super();
            this.closeIconSelector = '.lm-TabBar-tabCloseIcon';
            this.model = model;
        }
        /**
         * Render a full bundle
         */
        renderTab(data) {
            let title = data.title.caption;
            let key = this.createTabKey(data);
            let style = this.createTabStyle(data);
            let className = this.createTabClass(data);
            let dataset = this.createTabDataset(data);
            return _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_5__.h.li({ key, className, title, style, dataset }, this.renderIcon(data), this.renderLabel(data), this.renderCountBadge(data));
        }
        /**
         * Render the package count
         */
        renderCountBadge(data) {
            const bundle = data.title.label;
            const { bundles } = this.model;
            const packages = this.model.getFilteredPackages((bundles && bundle ? bundles[bundle].packages : []) || []);
            return _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_5__.h.label({}, `${packages.length}`);
        }
    }
    Licenses.BundleTabRenderer = BundleTabRenderer;
    /**
     * A grid of licenses
     */
    class Grid extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
        constructor(model) {
            super(model);
            /**
             * Render a single package's license information
             */
            this.renderRow = (row, index) => {
                const selected = index === this.model.currentPackageIndex;
                const onCheck = () => (this.model.currentPackageIndex = index);
                return (react__WEBPACK_IMPORTED_MODULE_7__.createElement("tr", { key: row.name, className: selected ? 'jp-mod-selected' : '', onClick: onCheck },
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("td", null,
                        react__WEBPACK_IMPORTED_MODULE_7__.createElement("input", { type: "radio", name: "show-package-license", value: index, onChange: onCheck, checked: selected })),
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("th", null, row.name),
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("td", null,
                        react__WEBPACK_IMPORTED_MODULE_7__.createElement("code", null, row.versionInfo)),
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("td", null,
                        react__WEBPACK_IMPORTED_MODULE_7__.createElement("code", null, row.licenseId))));
            };
            this.addClass('jp-Licenses-Grid');
            this.addClass('jp-RenderedHTMLCommon');
        }
        /**
         * Render a grid of package license information
         */
        render() {
            var _a;
            const { bundles, currentBundleName, trans } = this.model;
            const filteredPackages = this.model.getFilteredPackages(bundles && currentBundleName
                ? ((_a = bundles[currentBundleName]) === null || _a === void 0 ? void 0 : _a.packages) || []
                : []);
            if (!filteredPackages.length) {
                return (react__WEBPACK_IMPORTED_MODULE_7__.createElement("blockquote", null,
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("em", null, trans.__('No Packages found'))));
            }
            return (react__WEBPACK_IMPORTED_MODULE_7__.createElement("form", null,
                react__WEBPACK_IMPORTED_MODULE_7__.createElement("table", null,
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("thead", null,
                        react__WEBPACK_IMPORTED_MODULE_7__.createElement("tr", null,
                            react__WEBPACK_IMPORTED_MODULE_7__.createElement("td", null),
                            react__WEBPACK_IMPORTED_MODULE_7__.createElement("th", null, trans.__('Package')),
                            react__WEBPACK_IMPORTED_MODULE_7__.createElement("th", null, trans.__('Version')),
                            react__WEBPACK_IMPORTED_MODULE_7__.createElement("th", null, trans.__('License')))),
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("tbody", null, filteredPackages.map(this.renderRow)))));
        }
    }
    Licenses.Grid = Grid;
    /**
     * A package's full license text
     */
    class FullText extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
        constructor(model) {
            super(model);
            this.addClass('jp-Licenses-Text');
            this.addClass('jp-RenderedHTMLCommon');
            this.addClass('jp-RenderedMarkdown');
        }
        /**
         * Render the license text, or a null state if no package is selected
         */
        render() {
            const { currentPackage, trans } = this.model;
            let head = '';
            let quote = trans.__('No Package selected');
            let code = '';
            if (currentPackage) {
                const { name, versionInfo, licenseId, extractedText } = currentPackage;
                head = `${name} v${versionInfo}`;
                quote = `${trans.__('License')}: ${licenseId || trans.__('No License ID found')}`;
                code = extractedText || trans.__('No License Text found');
            }
            return [
                react__WEBPACK_IMPORTED_MODULE_7__.createElement("h1", { key: "h1" }, head),
                react__WEBPACK_IMPORTED_MODULE_7__.createElement("blockquote", { key: "quote" },
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("em", null, quote)),
                react__WEBPACK_IMPORTED_MODULE_7__.createElement("code", { key: "code" }, code)
            ];
        }
    }
    Licenses.FullText = FullText;
})(Licenses || (Licenses = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaGVscC1leHRlbnNpb24vc3JjL2luZGV4LnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaGVscC1leHRlbnNpb24vc3JjL2xpY2Vuc2VzLnRzeCJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFVSDtBQUM2QjtBQUNWO0FBRUs7QUFNbkI7QUFHSjtBQUNPO0FBRXRDOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBc0JuQjtBQXRCRCxXQUFVLFVBQVU7SUFDTCxlQUFJLEdBQUcsV0FBVyxDQUFDO0lBRW5CLGdCQUFLLEdBQUcsWUFBWSxDQUFDO0lBRXJCLG1CQUFRLEdBQUcsZUFBZSxDQUFDO0lBRTNCLGdCQUFLLEdBQUcsWUFBWSxDQUFDO0lBRXJCLGVBQUksR0FBRyxXQUFXLENBQUM7SUFFbkIsZUFBSSxHQUFHLFdBQVcsQ0FBQztJQUVuQix3QkFBYSxHQUFHLDhCQUE4QixDQUFDO0lBRS9DLHVCQUFZLEdBQUcsb0JBQW9CLENBQUM7SUFFcEMsbUJBQVEsR0FBRyxlQUFlLENBQUM7SUFFM0Isd0JBQWEsR0FBRyxxQkFBcUIsQ0FBQztJQUV0QywwQkFBZSxHQUFHLHVCQUF1QixDQUFDO0FBQ3pELENBQUMsRUF0QlMsVUFBVSxLQUFWLFVBQVUsUUFzQm5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLGFBQWEsR0FBRyxNQUFNLENBQUMsUUFBUSxDQUFDLFFBQVEsS0FBSyxRQUFRLENBQUM7QUFFNUQ7O0dBRUc7QUFDSCxNQUFNLFVBQVUsR0FBRyxTQUFTLENBQUM7QUFFN0I7O0dBRUc7QUFDSCxNQUFNLEtBQUssR0FBZ0M7SUFDekMsRUFBRSxFQUFFLGtDQUFrQztJQUN0QyxTQUFTLEVBQUUsSUFB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QixTQUFTLElBQUksS0FBSyxDQUFDLEVBQUUsQ0FBQyxxQkFBcUIsQ0FDN0MsRUFBRSxDQUFDO2dCQUNILElBQUksR0FBRyxhQUFhLElBQUksS0FBSyxDQUFDLEVBQUUsQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDO2FBQzNEO1lBQ0QsT0FBTztnQkFDTCx5REFBSSxHQUFHLEVBQUMsSUFBSSxJQUFFLElBQUksQ0FBTTtnQkFDeEIsaUVBQVksR0FBRyxFQUFDLE9BQU87b0JBQ3JCLDZEQUFLLEtBQUssQ0FBTSxDQUNMO2dCQUNiLDJEQUFNLEdBQUcsRUFBQyxNQUFNLElBQUUsSUFBSSxDQUFRO2FBQy9CLENBQUM7UUFDSixDQUFDO0tBQ0Y7SUFoQ1ksaUJBQVEsV0FnQ3BCO0FBQ0gsQ0FBQyxFQXRqQmdCLFFBQVEsS0FBUixRQUFRLFFBc2pCeEIiLCJmaWxlIjoicGFja2FnZXNfaGVscC1leHRlbnNpb25fbGliX2luZGV4X2pzLmU5YTc4NjFhMjlmMDFiNjRiYjJmLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgaGVscC1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGF5b3V0UmVzdG9yZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIENvbW1hbmRUb29sYmFyQnV0dG9uLFxuICBEaWFsb2csXG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgSUZyYW1lLFxuICBNYWluQXJlYVdpZGdldCxcbiAgc2hvd0RpYWxvZyxcbiAgVG9vbGJhcixcbiAgV2lkZ2V0VHJhY2tlclxufSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBQYWdlQ29uZmlnLCBVUkxFeHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSU1haW5NZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvbWFpbm1lbnUnO1xuaW1wb3J0IHsgS2VybmVsTWVzc2FnZSB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgY29weXJpZ2h0SWNvbixcbiAganVweXRlckljb24sXG4gIGp1cHl0ZXJsYWJXb3JkbWFya0ljb24sXG4gIHJlZnJlc2hJY29uXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgUmVhZG9ubHlKU09OT2JqZWN0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgTWVudSB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBMaWNlbnNlcyB9IGZyb20gJy4vbGljZW5zZXMnO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBoZWxwIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3Qgb3BlbiA9ICdoZWxwOm9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCBhYm91dCA9ICdoZWxwOmFib3V0JztcblxuICBleHBvcnQgY29uc3QgYWN0aXZhdGUgPSAnaGVscDphY3RpdmF0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGNsb3NlID0gJ2hlbHA6Y2xvc2UnO1xuXG4gIGV4cG9ydCBjb25zdCBzaG93ID0gJ2hlbHA6c2hvdyc7XG5cbiAgZXhwb3J0IGNvbnN0IGhpZGUgPSAnaGVscDpoaWRlJztcblxuICBleHBvcnQgY29uc3QgbGF1bmNoQ2xhc3NpYyA9ICdoZWxwOmxhdW5jaC1jbGFzc2ljLW5vdGVib29rJztcblxuICBleHBvcnQgY29uc3QganVweXRlckZvcnVtID0gJ2hlbHA6anVweXRlci1mb3J1bSc7XG5cbiAgZXhwb3J0IGNvbnN0IGxpY2Vuc2VzID0gJ2hlbHA6bGljZW5zZXMnO1xuXG4gIGV4cG9ydCBjb25zdCBsaWNlbnNlUmVwb3J0ID0gJ2hlbHA6bGljZW5zZS1yZXBvcnQnO1xuXG4gIGV4cG9ydCBjb25zdCByZWZyZXNoTGljZW5zZXMgPSAnaGVscDpsaWNlbnNlcy1yZWZyZXNoJztcbn1cblxuLyoqXG4gKiBBIGZsYWcgZGVub3Rpbmcgd2hldGhlciB0aGUgYXBwbGljYXRpb24gaXMgbG9hZGVkIG92ZXIgSFRUUFMuXG4gKi9cbmNvbnN0IExBQl9JU19TRUNVUkUgPSB3aW5kb3cubG9jYXRpb24ucHJvdG9jb2wgPT09ICdodHRwczonO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHRoZSBoZWxwIHdpZGdldC5cbiAqL1xuY29uc3QgSEVMUF9DTEFTUyA9ICdqcC1IZWxwJztcblxuLyoqXG4gKiBBZGQgYSBjb21tYW5kIHRvIHNob3cgYW4gQWJvdXQgZGlhbG9nLlxuICovXG5jb25zdCBhYm91dDogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2hlbHAtZXh0ZW5zaW9uOmFib3V0JyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJQ29tbWFuZFBhbGV0dGVdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGxcbiAgKTogdm9pZCA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgY2F0ZWdvcnkgPSB0cmFucy5fXygnSGVscCcpO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmFib3V0LCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0Fib3V0ICUxJywgYXBwLm5hbWUpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAvLyBDcmVhdGUgdGhlIGhlYWRlciBvZiB0aGUgYWJvdXQgZGlhbG9nXG4gICAgICAgIGNvbnN0IHZlcnNpb25OdW1iZXIgPSB0cmFucy5fXygnVmVyc2lvbiAlMScsIGFwcC52ZXJzaW9uKTtcbiAgICAgICAgY29uc3QgdmVyc2lvbkluZm8gPSAoXG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwianAtQWJvdXQtdmVyc2lvbi1pbmZvXCI+XG4gICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJqcC1BYm91dC12ZXJzaW9uXCI+e3ZlcnNpb25OdW1iZXJ9PC9zcGFuPlxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgKTtcbiAgICAgICAgY29uc3QgdGl0bGUgPSAoXG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwianAtQWJvdXQtaGVhZGVyXCI+XG4gICAgICAgICAgICA8anVweXRlckljb24ucmVhY3QgbWFyZ2luPVwiN3B4IDkuNXB4XCIgaGVpZ2h0PVwiYXV0b1wiIHdpZHRoPVwiNThweFwiIC8+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUFib3V0LWhlYWRlci1pbmZvXCI+XG4gICAgICAgICAgICAgIDxqdXB5dGVybGFiV29yZG1hcmtJY29uLnJlYWN0IGhlaWdodD1cImF1dG9cIiB3aWR0aD1cIjE5NnB4XCIgLz5cbiAgICAgICAgICAgICAge3ZlcnNpb25JbmZvfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICApO1xuXG4gICAgICAgIC8vIENyZWF0ZSB0aGUgYm9keSBvZiB0aGUgYWJvdXQgZGlhbG9nXG4gICAgICAgIGNvbnN0IGp1cHl0ZXJVUkwgPSAnaHR0cHM6Ly9qdXB5dGVyLm9yZy9hYm91dC5odG1sJztcbiAgICAgICAgY29uc3QgY29udHJpYnV0b3JzVVJMID1cbiAgICAgICAgICAnaHR0cHM6Ly9naXRodWIuY29tL2p1cHl0ZXJsYWIvanVweXRlcmxhYi9ncmFwaHMvY29udHJpYnV0b3JzJztcbiAgICAgICAgY29uc3QgZXh0ZXJuYWxMaW5rcyA9IChcbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJqcC1BYm91dC1leHRlcm5hbExpbmtzXCI+XG4gICAgICAgICAgICA8YVxuICAgICAgICAgICAgICBocmVmPXtjb250cmlidXRvcnNVUkx9XG4gICAgICAgICAgICAgIHRhcmdldD1cIl9ibGFua1wiXG4gICAgICAgICAgICAgIHJlbD1cIm5vb3BlbmVyIG5vcmVmZXJyZXJcIlxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJqcC1CdXR0b24tZmxhdFwiXG4gICAgICAgICAgICA+XG4gICAgICAgICAgICAgIHt0cmFucy5fXygnQ09OVFJJQlVUT1IgTElTVCcpfVxuICAgICAgICAgICAgPC9hPlxuICAgICAgICAgICAgPGFcbiAgICAgICAgICAgICAgaHJlZj17anVweXRlclVSTH1cbiAgICAgICAgICAgICAgdGFyZ2V0PVwiX2JsYW5rXCJcbiAgICAgICAgICAgICAgcmVsPVwibm9vcGVuZXIgbm9yZWZlcnJlclwiXG4gICAgICAgICAgICAgIGNsYXNzTmFtZT1cImpwLUJ1dHRvbi1mbGF0XCJcbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAge3RyYW5zLl9fKCdBQk9VVCBQUk9KRUNUIEpVUFlURVInKX1cbiAgICAgICAgICAgIDwvYT5cbiAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICk7XG4gICAgICAgIGNvbnN0IGNvcHlyaWdodCA9IChcbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJqcC1BYm91dC1jb3B5cmlnaHRcIj5cbiAgICAgICAgICAgIHt0cmFucy5fXygnwqkgMjAxNS0yMDIxIFByb2plY3QgSnVweXRlciBDb250cmlidXRvcnMnKX1cbiAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICk7XG4gICAgICAgIGNvbnN0IGJvZHkgPSAoXG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1BYm91dC1ib2R5XCI+XG4gICAgICAgICAgICB7ZXh0ZXJuYWxMaW5rc31cbiAgICAgICAgICAgIHtjb3B5cmlnaHR9XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG5cbiAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgIHRpdGxlLFxuICAgICAgICAgIGJvZHksXG4gICAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgICAgRGlhbG9nLmNyZWF0ZUJ1dHRvbih7XG4gICAgICAgICAgICAgIGxhYmVsOiB0cmFucy5fXygnRGlzbWlzcycpLFxuICAgICAgICAgICAgICBjbGFzc05hbWU6ICdqcC1BYm91dC1idXR0b24ganAtbW9kLXJlamVjdCBqcC1tb2Qtc3R5bGVkJ1xuICAgICAgICAgICAgfSlcbiAgICAgICAgICBdXG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNvbW1hbmQ6IENvbW1hbmRJRHMuYWJvdXQsIGNhdGVnb3J5IH0pO1xuICAgIH1cbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0byBhZGQgYSBjb21tYW5kIHRvIG9wZW4gdGhlIENsYXNzaWMgTm90ZWJvb2sgaW50ZXJmYWNlLlxuICovXG5jb25zdCBsYXVuY2hDbGFzc2ljOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvaGVscC1leHRlbnNpb246bGF1bmNoLWNsYXNzaWMnLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZV0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuICApOiB2b2lkID0+IHtcbiAgICBjb25zdCB7IGNvbW1hbmRzIH0gPSBhcHA7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdIZWxwJyk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubGF1bmNoQ2xhc3NpYywge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdMYXVuY2ggQ2xhc3NpYyBOb3RlYm9vaycpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICB3aW5kb3cub3BlbihQYWdlQ29uZmlnLmdldEJhc2VVcmwoKSArICd0cmVlJyk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBpZiAocGFsZXR0ZSkge1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZDogQ29tbWFuZElEcy5sYXVuY2hDbGFzc2ljLCBjYXRlZ29yeSB9KTtcbiAgICB9XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gdG8gYWRkIGEgY29tbWFuZCB0byBvcGVuIHRoZSBKdXB5dGVyIEZvcnVtLlxuICovXG5jb25zdCBqdXB5dGVyRm9ydW06IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9oZWxwLWV4dGVuc2lvbjpqdXB5dGVyLWZvcnVtJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJQ29tbWFuZFBhbGV0dGVdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGxcbiAgKTogdm9pZCA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgY2F0ZWdvcnkgPSB0cmFucy5fXygnSGVscCcpO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmp1cHl0ZXJGb3J1bSwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdKdXB5dGVyIEZvcnVtJyksXG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIHdpbmRvdy5vcGVuKCdodHRwczovL2Rpc2NvdXJzZS5qdXB5dGVyLm9yZy9jL2p1cHl0ZXJsYWInKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kOiBDb21tYW5kSURzLmp1cHl0ZXJGb3J1bSwgY2F0ZWdvcnkgfSk7XG4gICAgfVxuICB9XG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHRvIGFkZCBhIGxpc3Qgb2YgcmVzb3VyY2VzIHRvIHRoZSBoZWxwIG1lbnUuXG4gKi9cbmNvbnN0IHJlc291cmNlczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2hlbHAtZXh0ZW5zaW9uOnJlc291cmNlcycsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJTWFpbk1lbnUsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJQ29tbWFuZFBhbGV0dGUsIElMYXlvdXRSZXN0b3Jlcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbWFpbk1lbnU6IElNYWluTWVudSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsLFxuICAgIHJlc3RvcmVyOiBJTGF5b3V0UmVzdG9yZXIgfCBudWxsXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgbGV0IGNvdW50ZXIgPSAwO1xuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0hlbHAnKTtcbiAgICBjb25zdCBuYW1lc3BhY2UgPSAnaGVscC1kb2MnO1xuICAgIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsLCBzZXJ2aWNlTWFuYWdlciB9ID0gYXBwO1xuICAgIGNvbnN0IHRyYWNrZXIgPSBuZXcgV2lkZ2V0VHJhY2tlcjxNYWluQXJlYVdpZGdldDxJRnJhbWU+Pih7IG5hbWVzcGFjZSB9KTtcbiAgICBjb25zdCByZXNvdXJjZXMgPSBbXG4gICAgICB7XG4gICAgICAgIHRleHQ6IHRyYW5zLl9fKCdKdXB5dGVyTGFiIFJlZmVyZW5jZScpLFxuICAgICAgICB1cmw6ICdodHRwczovL2p1cHl0ZXJsYWIucmVhZHRoZWRvY3MuaW8vZW4vMy4yLngvJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdGV4dDogdHJhbnMuX18oJ0p1cHl0ZXJMYWIgRkFRJyksXG4gICAgICAgIHVybDpcbiAgICAgICAgICAnaHR0cHM6Ly9qdXB5dGVybGFiLnJlYWR0aGVkb2NzLmlvL2VuLzMuMi54L2dldHRpbmdfc3RhcnRlZC9mYXEuaHRtbCdcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHRleHQ6IHRyYW5zLl9fKCdKdXB5dGVyIFJlZmVyZW5jZScpLFxuICAgICAgICB1cmw6ICdodHRwczovL2p1cHl0ZXIub3JnL2RvY3VtZW50YXRpb24nXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB0ZXh0OiB0cmFucy5fXygnTWFya2Rvd24gUmVmZXJlbmNlJyksXG4gICAgICAgIHVybDogJ2h0dHBzOi8vY29tbW9ubWFyay5vcmcvaGVscC8nXG4gICAgICB9XG4gICAgXTtcblxuICAgIHJlc291cmNlcy5zb3J0KChhOiBhbnksIGI6IGFueSkgPT4ge1xuICAgICAgcmV0dXJuIGEudGV4dC5sb2NhbGVDb21wYXJlKGIudGV4dCk7XG4gICAgfSk7XG5cbiAgICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gICAgaWYgKHJlc3RvcmVyKSB7XG4gICAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwge1xuICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLm9wZW4sXG4gICAgICAgIGFyZ3M6IHdpZGdldCA9PiAoe1xuICAgICAgICAgIHVybDogd2lkZ2V0LmNvbnRlbnQudXJsLFxuICAgICAgICAgIHRleHQ6IHdpZGdldC5jb250ZW50LnRpdGxlLmxhYmVsXG4gICAgICAgIH0pLFxuICAgICAgICBuYW1lOiB3aWRnZXQgPT4gd2lkZ2V0LmNvbnRlbnQudXJsXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgSGVscFdpZGdldCB3aWRnZXQuXG4gICAgICovXG4gICAgZnVuY3Rpb24gbmV3SGVscFdpZGdldCh1cmw6IHN0cmluZywgdGV4dDogc3RyaW5nKTogTWFpbkFyZWFXaWRnZXQ8SUZyYW1lPiB7XG4gICAgICAvLyBBbGxvdyBzY3JpcHRzIGFuZCBmb3JtcyBzbyB0aGF0IHRoaW5ncyBsaWtlXG4gICAgICAvLyByZWFkdGhlZG9jcyBjYW4gdXNlIHRoZWlyIHNlYXJjaCBmdW5jdGlvbmFsaXR5LlxuICAgICAgLy8gV2UgKmRvbid0KiBhbGxvdyBzYW1lIG9yaWdpbiByZXF1ZXN0cywgd2hpY2hcbiAgICAgIC8vIGNhbiBwcmV2ZW50IHNvbWUgY29udGVudCBmcm9tIGJlaW5nIGxvYWRlZCBvbnRvIHRoZVxuICAgICAgLy8gaGVscCBwYWdlcy5cbiAgICAgIGNvbnN0IGNvbnRlbnQgPSBuZXcgSUZyYW1lKHtcbiAgICAgICAgc2FuZGJveDogWydhbGxvdy1zY3JpcHRzJywgJ2FsbG93LWZvcm1zJ11cbiAgICAgIH0pO1xuICAgICAgY29udGVudC51cmwgPSB1cmw7XG4gICAgICBjb250ZW50LmFkZENsYXNzKEhFTFBfQ0xBU1MpO1xuICAgICAgY29udGVudC50aXRsZS5sYWJlbCA9IHRleHQ7XG4gICAgICBjb250ZW50LmlkID0gYCR7bmFtZXNwYWNlfS0keysrY291bnRlcn1gO1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gbmV3IE1haW5BcmVhV2lkZ2V0KHsgY29udGVudCB9KTtcbiAgICAgIHdpZGdldC5hZGRDbGFzcygnanAtSGVscCcpO1xuICAgICAgcmV0dXJuIHdpZGdldDtcbiAgICB9XG5cbiAgICAvLyBQb3B1bGF0ZSB0aGUgSGVscCBtZW51LlxuICAgIGNvbnN0IGhlbHBNZW51ID0gbWFpbk1lbnUuaGVscE1lbnU7XG5cbiAgICBjb25zdCByZXNvdXJjZXNHcm91cCA9IHJlc291cmNlcy5tYXAoYXJncyA9PiAoe1xuICAgICAgYXJncyxcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMub3BlblxuICAgIH0pKTtcbiAgICBoZWxwTWVudS5hZGRHcm91cChyZXNvdXJjZXNHcm91cCwgMTApO1xuXG4gICAgLy8gR2VuZXJhdGUgYSBjYWNoZSBvZiB0aGUga2VybmVsIGhlbHAgbGlua3MuXG4gICAgY29uc3Qga2VybmVsSW5mb0NhY2hlID0gbmV3IE1hcDxcbiAgICAgIHN0cmluZyxcbiAgICAgIEtlcm5lbE1lc3NhZ2UuSUluZm9SZXBseU1zZ1snY29udGVudCddXG4gICAgPigpO1xuICAgIHNlcnZpY2VNYW5hZ2VyLnNlc3Npb25zLnJ1bm5pbmdDaGFuZ2VkLmNvbm5lY3QoKG0sIHNlc3Npb25zKSA9PiB7XG4gICAgICAvLyBJZiBhIG5ldyBzZXNzaW9uIGhhcyBiZWVuIGFkZGVkLCBpdCBpcyBhdCB0aGUgYmFja1xuICAgICAgLy8gb2YgdGhlIHNlc3Npb24gbGlzdC4gSWYgb25lIGhhcyBjaGFuZ2VkIG9yIHN0b3BwZWQsXG4gICAgICAvLyBpdCBkb2VzIG5vdCBodXJ0IHRvIGNoZWNrIGl0LlxuICAgICAgaWYgKCFzZXNzaW9ucy5sZW5ndGgpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3Qgc2Vzc2lvbk1vZGVsID0gc2Vzc2lvbnNbc2Vzc2lvbnMubGVuZ3RoIC0gMV07XG4gICAgICBpZiAoXG4gICAgICAgICFzZXNzaW9uTW9kZWwua2VybmVsIHx8XG4gICAgICAgIGtlcm5lbEluZm9DYWNoZS5oYXMoc2Vzc2lvbk1vZGVsLmtlcm5lbC5uYW1lKVxuICAgICAgKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IHNlc3Npb24gPSBzZXJ2aWNlTWFuYWdlci5zZXNzaW9ucy5jb25uZWN0VG8oe1xuICAgICAgICBtb2RlbDogc2Vzc2lvbk1vZGVsLFxuICAgICAgICBrZXJuZWxDb25uZWN0aW9uT3B0aW9uczogeyBoYW5kbGVDb21tczogZmFsc2UgfVxuICAgICAgfSk7XG5cbiAgICAgIHZvaWQgc2Vzc2lvbi5rZXJuZWw/LmluZm8udGhlbihrZXJuZWxJbmZvID0+IHtcbiAgICAgICAgY29uc3QgbmFtZSA9IHNlc3Npb24ua2VybmVsIS5uYW1lO1xuXG4gICAgICAgIC8vIENoZWNrIHRoZSBjYWNoZSBzZWNvbmQgdGltZSBzbyB0aGF0LCBpZiB0d28gY2FsbGJhY2tzIGdldCBzY2hlZHVsZWQsXG4gICAgICAgIC8vIHRoZXkgZG9uJ3QgdHJ5IHRvIGFkZCB0aGUgc2FtZSBjb21tYW5kcy5cbiAgICAgICAgaWYgKGtlcm5lbEluZm9DYWNoZS5oYXMobmFtZSkpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgLy8gU2V0IHRoZSBLZXJuZWwgSW5mbyBjYWNoZS5cbiAgICAgICAga2VybmVsSW5mb0NhY2hlLnNldChuYW1lLCBrZXJuZWxJbmZvKTtcblxuICAgICAgICAvLyBVdGlsaXR5IGZ1bmN0aW9uIHRvIGNoZWNrIGlmIHRoZSBjdXJyZW50IHdpZGdldFxuICAgICAgICAvLyBoYXMgcmVnaXN0ZXJlZCBpdHNlbGYgd2l0aCB0aGUgaGVscCBtZW51LlxuICAgICAgICBjb25zdCB1c2VzS2VybmVsID0gKCkgPT4ge1xuICAgICAgICAgIGxldCByZXN1bHQgPSBmYWxzZTtcbiAgICAgICAgICBjb25zdCB3aWRnZXQgPSBhcHAuc2hlbGwuY3VycmVudFdpZGdldDtcbiAgICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgICAgcmV0dXJuIHJlc3VsdDtcbiAgICAgICAgICB9XG4gICAgICAgICAgaGVscE1lbnUua2VybmVsVXNlcnMuZm9yRWFjaCh1ID0+IHtcbiAgICAgICAgICAgIGlmICh1LnRyYWNrZXIuaGFzKHdpZGdldCkgJiYgdS5nZXRLZXJuZWwod2lkZ2V0KT8ubmFtZSA9PT0gbmFtZSkge1xuICAgICAgICAgICAgICByZXN1bHQgPSB0cnVlO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0pO1xuICAgICAgICAgIHJldHVybiByZXN1bHQ7XG4gICAgICAgIH07XG5cbiAgICAgICAgLy8gQWRkIHRoZSBrZXJuZWwgYmFubmVyIHRvIHRoZSBIZWxwIE1lbnUuXG4gICAgICAgIGNvbnN0IGJhbm5lckNvbW1hbmQgPSBgaGVscC1tZW51LSR7bmFtZX06YmFubmVyYDtcbiAgICAgICAgY29uc3Qgc3BlYyA9IHNlcnZpY2VNYW5hZ2VyLmtlcm5lbHNwZWNzPy5zcGVjcz8ua2VybmVsc3BlY3NbbmFtZV07XG4gICAgICAgIGlmICghc3BlYykge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBrZXJuZWxOYW1lID0gc3BlYy5kaXNwbGF5X25hbWU7XG4gICAgICAgIGxldCBrZXJuZWxJY29uVXJsID0gc3BlYy5yZXNvdXJjZXNbJ2xvZ28tNjR4NjQnXTtcbiAgICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChiYW5uZXJDb21tYW5kLCB7XG4gICAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdBYm91dCB0aGUgJTEgS2VybmVsJywga2VybmVsTmFtZSksXG4gICAgICAgICAgaXNWaXNpYmxlOiB1c2VzS2VybmVsLFxuICAgICAgICAgIGlzRW5hYmxlZDogdXNlc0tlcm5lbCxcbiAgICAgICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgICAgICAvLyBDcmVhdGUgdGhlIGhlYWRlciBvZiB0aGUgYWJvdXQgZGlhbG9nXG4gICAgICAgICAgICBjb25zdCBoZWFkZXJMb2dvID0gPGltZyBzcmM9e2tlcm5lbEljb25Vcmx9IC8+O1xuICAgICAgICAgICAgY29uc3QgdGl0bGUgPSAoXG4gICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cImpwLUFib3V0LWhlYWRlclwiPlxuICAgICAgICAgICAgICAgIHtoZWFkZXJMb2dvfVxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtQWJvdXQtaGVhZGVyLWluZm9cIj57a2VybmVsTmFtZX08L2Rpdj5cbiAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIGNvbnN0IGJhbm5lciA9IDxwcmU+e2tlcm5lbEluZm8uYmFubmVyfTwvcHJlPjtcbiAgICAgICAgICAgIGNvbnN0IGJvZHkgPSA8ZGl2IGNsYXNzTmFtZT1cImpwLUFib3V0LWJvZHlcIj57YmFubmVyfTwvZGl2PjtcblxuICAgICAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgICAgICB0aXRsZSxcbiAgICAgICAgICAgICAgYm9keSxcbiAgICAgICAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgICAgICAgIERpYWxvZy5jcmVhdGVCdXR0b24oe1xuICAgICAgICAgICAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdEaXNtaXNzJyksXG4gICAgICAgICAgICAgICAgICBjbGFzc05hbWU6ICdqcC1BYm91dC1idXR0b24ganAtbW9kLXJlamVjdCBqcC1tb2Qtc3R5bGVkJ1xuICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgIF1cbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICAgIGhlbHBNZW51LmFkZEdyb3VwKFt7IGNvbW1hbmQ6IGJhbm5lckNvbW1hbmQgfV0sIDIwKTtcblxuICAgICAgICAvLyBBZGQgdGhlIGtlcm5lbCBpbmZvIGhlbHBfbGlua3MgdG8gdGhlIEhlbHAgbWVudS5cbiAgICAgICAgY29uc3Qga2VybmVsR3JvdXA6IE1lbnUuSUl0ZW1PcHRpb25zW10gPSBbXTtcbiAgICAgICAgKGtlcm5lbEluZm8uaGVscF9saW5rcyB8fCBbXSkuZm9yRWFjaChsaW5rID0+IHtcbiAgICAgICAgICBjb25zdCBjb21tYW5kSWQgPSBgaGVscC1tZW51LSR7bmFtZX06JHtsaW5rLnRleHR9YDtcbiAgICAgICAgICBjb21tYW5kcy5hZGRDb21tYW5kKGNvbW1hbmRJZCwge1xuICAgICAgICAgICAgbGFiZWw6IGxpbmsudGV4dCxcbiAgICAgICAgICAgIGlzVmlzaWJsZTogdXNlc0tlcm5lbCxcbiAgICAgICAgICAgIGlzRW5hYmxlZDogdXNlc0tlcm5lbCxcbiAgICAgICAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5vcGVuLCBsaW5rKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9KTtcbiAgICAgICAgICBrZXJuZWxHcm91cC5wdXNoKHsgY29tbWFuZDogY29tbWFuZElkIH0pO1xuICAgICAgICB9KTtcbiAgICAgICAgaGVscE1lbnUuYWRkR3JvdXAoa2VybmVsR3JvdXAsIDIxKTtcblxuICAgICAgICAvLyBEaXNwb3NlIG9mIHRoZSBzZXNzaW9uIG9iamVjdCBzaW5jZSB3ZSBubyBsb25nZXIgbmVlZCBpdC5cbiAgICAgICAgc2Vzc2lvbi5kaXNwb3NlKCk7XG4gICAgICB9KTtcbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuLCB7XG4gICAgICBsYWJlbDogYXJncyA9PiBhcmdzWyd0ZXh0J10gYXMgc3RyaW5nLFxuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IHVybCA9IGFyZ3NbJ3VybCddIGFzIHN0cmluZztcbiAgICAgICAgY29uc3QgdGV4dCA9IGFyZ3NbJ3RleHQnXSBhcyBzdHJpbmc7XG4gICAgICAgIGNvbnN0IG5ld0Jyb3dzZXJUYWIgPSAoYXJnc1snbmV3QnJvd3NlclRhYiddIGFzIGJvb2xlYW4pIHx8IGZhbHNlO1xuXG4gICAgICAgIC8vIElmIGhlbHAgcmVzb3VyY2Ugd2lsbCBnZW5lcmF0ZSBhIG1peGVkIGNvbnRlbnQgZXJyb3IsIGxvYWQgZXh0ZXJuYWxseS5cbiAgICAgICAgaWYgKFxuICAgICAgICAgIG5ld0Jyb3dzZXJUYWIgfHxcbiAgICAgICAgICAoTEFCX0lTX1NFQ1VSRSAmJiBVUkxFeHQucGFyc2UodXJsKS5wcm90b2NvbCAhPT0gJ2h0dHBzOicpXG4gICAgICAgICkge1xuICAgICAgICAgIHdpbmRvdy5vcGVuKHVybCk7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gbmV3SGVscFdpZGdldCh1cmwsIHRleHQpO1xuICAgICAgICB2b2lkIHRyYWNrZXIuYWRkKHdpZGdldCk7XG4gICAgICAgIHNoZWxsLmFkZCh3aWRnZXQsICdtYWluJyk7XG4gICAgICAgIHJldHVybiB3aWRnZXQ7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBpZiAocGFsZXR0ZSkge1xuICAgICAgcmVzb3VyY2VzLmZvckVhY2goYXJncyA9PiB7XG4gICAgICAgIHBhbGV0dGUuYWRkSXRlbSh7IGFyZ3MsIGNvbW1hbmQ6IENvbW1hbmRJRHMub3BlbiwgY2F0ZWdvcnkgfSk7XG4gICAgICB9KTtcbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICAgIGFyZ3M6IHsgcmVsb2FkOiB0cnVlIH0sXG4gICAgICAgIGNvbW1hbmQ6ICdhcHB1dGlsczpyZXNldCcsXG4gICAgICAgIGNhdGVnb3J5XG4gICAgICB9KTtcbiAgICB9XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gdG8gYWRkIGEgbGljZW5zZXMgcmVwb3J0aW5nIHRvb2xzLlxuICovXG5jb25zdCBsaWNlbnNlczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2hlbHAtZXh0ZW5zaW9uOmxpY2Vuc2VzJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJTWFpbk1lbnUsIElDb21tYW5kUGFsZXR0ZSwgSUxheW91dFJlc3RvcmVyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBtZW51OiBJTWFpbk1lbnUgfCBudWxsLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGwsXG4gICAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGxcbiAgKSA9PiB7XG4gICAgLy8gYmFpbCBpZiBubyBsaWNlbnNlIEFQSSBpcyBhdmFpbGFibGUgZnJvbSB0aGUgc2VydmVyXG4gICAgaWYgKCFQYWdlQ29uZmlnLmdldE9wdGlvbignbGljZW5zZXNVcmwnKSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsIH0gPSBhcHA7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIC8vIHRyYW5zbGF0aW9uIHN0cmluZ3NcbiAgICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdIZWxwJyk7XG4gICAgY29uc3QgZG93bmxvYWRBc1RleHQgPSB0cmFucy5fXygnRG93bmxvYWQgQWxsIExpY2Vuc2VzIGFzJyk7XG4gICAgY29uc3QgbGljZW5zZXNUZXh0ID0gdHJhbnMuX18oJ0xpY2Vuc2VzJyk7XG4gICAgY29uc3QgcmVmcmVzaExpY2Vuc2VzID0gdHJhbnMuX18oJ1JlZnJlc2ggTGljZW5zZXMnKTtcblxuICAgIC8vIGFuIGluY3JlbWVudGVyIGZvciBsaWNlbnNlIHdpZGdldCBpZHNcbiAgICBsZXQgY291bnRlciA9IDA7XG5cbiAgICBjb25zdCBsaWNlbnNlc1VybCA9XG4gICAgICBVUkxFeHQuam9pbihcbiAgICAgICAgUGFnZUNvbmZpZy5nZXRCYXNlVXJsKCksXG4gICAgICAgIFBhZ2VDb25maWcuZ2V0T3B0aW9uKCdsaWNlbnNlc1VybCcpXG4gICAgICApICsgJy8nO1xuXG4gICAgY29uc3QgbGljZW5zZXNOYW1lc3BhY2UgPSAnaGVscC1saWNlbnNlcyc7XG4gICAgY29uc3QgbGljZW5zZXNUcmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8TGljZW5zZXM+Pih7XG4gICAgICBuYW1lc3BhY2U6IGxpY2Vuc2VzTmFtZXNwYWNlXG4gICAgfSk7XG5cbiAgICAvKipcbiAgICAgKiBSZXR1cm4gYSBmdWxsIGxpY2Vuc2UgcmVwb3J0IGZvcm1hdCBiYXNlZCBvbiBhIGZvcm1hdCBuYW1lXG4gICAgICovXG4gICAgZnVuY3Rpb24gZm9ybWF0T3JEZWZhdWx0KGZvcm1hdDogc3RyaW5nKTogTGljZW5zZXMuSVJlcG9ydEZvcm1hdCB7XG4gICAgICByZXR1cm4gKFxuICAgICAgICBMaWNlbnNlcy5SRVBPUlRfRk9STUFUU1tmb3JtYXRdIHx8XG4gICAgICAgIExpY2Vuc2VzLlJFUE9SVF9GT1JNQVRTW0xpY2Vuc2VzLkRFRkFVTFRfRk9STUFUXVxuICAgICAgKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBNYWluQXJlYVdpZGdldCBmb3IgYSBsaWNlbnNlIHZpZXdlclxuICAgICAqL1xuICAgIGZ1bmN0aW9uIGNyZWF0ZUxpY2Vuc2VXaWRnZXQoYXJnczogTGljZW5zZXMuSUNyZWF0ZUFyZ3MpIHtcbiAgICAgIGNvbnN0IGxpY2Vuc2VzTW9kZWwgPSBuZXcgTGljZW5zZXMuTW9kZWwoe1xuICAgICAgICAuLi5hcmdzLFxuICAgICAgICBsaWNlbnNlc1VybCxcbiAgICAgICAgdHJhbnMsXG4gICAgICAgIHNlcnZlclNldHRpbmdzOiBhcHAuc2VydmljZU1hbmFnZXIuc2VydmVyU2V0dGluZ3NcbiAgICAgIH0pO1xuICAgICAgY29uc3QgY29udGVudCA9IG5ldyBMaWNlbnNlcyh7IG1vZGVsOiBsaWNlbnNlc01vZGVsIH0pO1xuICAgICAgY29udGVudC5pZCA9IGAke2xpY2Vuc2VzTmFtZXNwYWNlfS0keysrY291bnRlcn1gO1xuICAgICAgY29udGVudC50aXRsZS5sYWJlbCA9IGxpY2Vuc2VzVGV4dDtcbiAgICAgIGNvbnRlbnQudGl0bGUuaWNvbiA9IGNvcHlyaWdodEljb247XG4gICAgICBjb25zdCBtYWluID0gbmV3IE1haW5BcmVhV2lkZ2V0KHtcbiAgICAgICAgY29udGVudCxcbiAgICAgICAgcmV2ZWFsOiBsaWNlbnNlc01vZGVsLmxpY2Vuc2VzUmVhZHlcbiAgICAgIH0pO1xuXG4gICAgICBtYWluLnRvb2xiYXIuYWRkSXRlbShcbiAgICAgICAgJ3JlZnJlc2gtbGljZW5zZXMnLFxuICAgICAgICBuZXcgQ29tbWFuZFRvb2xiYXJCdXR0b24oe1xuICAgICAgICAgIGlkOiBDb21tYW5kSURzLnJlZnJlc2hMaWNlbnNlcyxcbiAgICAgICAgICBhcmdzOiB7IG5vTGFiZWw6IDEgfSxcbiAgICAgICAgICBjb21tYW5kc1xuICAgICAgICB9KVxuICAgICAgKTtcblxuICAgICAgbWFpbi50b29sYmFyLmFkZEl0ZW0oJ3NwYWNlcicsIFRvb2xiYXIuY3JlYXRlU3BhY2VySXRlbSgpKTtcblxuICAgICAgZm9yIChjb25zdCBmb3JtYXQgb2YgT2JqZWN0LmtleXMoTGljZW5zZXMuUkVQT1JUX0ZPUk1BVFMpKSB7XG4gICAgICAgIGNvbnN0IGJ1dHRvbiA9IG5ldyBDb21tYW5kVG9vbGJhckJ1dHRvbih7XG4gICAgICAgICAgaWQ6IENvbW1hbmRJRHMubGljZW5zZVJlcG9ydCxcbiAgICAgICAgICBhcmdzOiB7IGZvcm1hdCwgbm9MYWJlbDogMSB9LFxuICAgICAgICAgIGNvbW1hbmRzXG4gICAgICAgIH0pO1xuICAgICAgICBtYWluLnRvb2xiYXIuYWRkSXRlbShgZG93bmxvYWQtJHtmb3JtYXR9YCwgYnV0dG9uKTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIG1haW47XG4gICAgfVxuXG4gICAgLy8gcmVnaXN0ZXIgbGljZW5zZS1yZWxhdGVkIGNvbW1hbmRzXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmxpY2Vuc2VzLCB7XG4gICAgICBsYWJlbDogbGljZW5zZXNUZXh0LFxuICAgICAgZXhlY3V0ZTogKGFyZ3M6IGFueSkgPT4ge1xuICAgICAgICBjb25zdCBsaWNlbnNlTWFpbiA9IGNyZWF0ZUxpY2Vuc2VXaWRnZXQoYXJncyBhcyBMaWNlbnNlcy5JQ3JlYXRlQXJncyk7XG4gICAgICAgIHNoZWxsLmFkZChsaWNlbnNlTWFpbiwgJ21haW4nKTtcblxuICAgICAgICAvLyBhZGQgdG8gdHJhY2tlciBzbyBpdCBjYW4gYmUgcmVzdG9yZWQsIGFuZCB1cGRhdGUgd2hlbiBjaG9pY2VzIGNoYW5nZVxuICAgICAgICB2b2lkIGxpY2Vuc2VzVHJhY2tlci5hZGQobGljZW5zZU1haW4pO1xuICAgICAgICBsaWNlbnNlTWFpbi5jb250ZW50Lm1vZGVsLnRyYWNrZXJEYXRhQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgICB2b2lkIGxpY2Vuc2VzVHJhY2tlci5zYXZlKGxpY2Vuc2VNYWluKTtcbiAgICAgICAgfSk7XG4gICAgICAgIHJldHVybiBsaWNlbnNlTWFpbjtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZWZyZXNoTGljZW5zZXMsIHtcbiAgICAgIGxhYmVsOiBhcmdzID0+IChhcmdzLm5vTGFiZWwgPyAnJyA6IHJlZnJlc2hMaWNlbnNlcyksXG4gICAgICBjYXB0aW9uOiByZWZyZXNoTGljZW5zZXMsXG4gICAgICBpY29uOiByZWZyZXNoSWNvbixcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgcmV0dXJuIGxpY2Vuc2VzVHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50Lm1vZGVsLmluaXRMaWNlbnNlcygpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmxpY2Vuc2VSZXBvcnQsIHtcbiAgICAgIGxhYmVsOiBhcmdzID0+IHtcbiAgICAgICAgaWYgKGFyZ3Mubm9MYWJlbCkge1xuICAgICAgICAgIHJldHVybiAnJztcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBmb3JtYXQgPSBmb3JtYXRPckRlZmF1bHQoYCR7YXJncy5mb3JtYXR9YCk7XG4gICAgICAgIHJldHVybiBgJHtkb3dubG9hZEFzVGV4dH0gJHtmb3JtYXQudGl0bGV9YDtcbiAgICAgIH0sXG4gICAgICBjYXB0aW9uOiBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgZm9ybWF0ID0gZm9ybWF0T3JEZWZhdWx0KGAke2FyZ3MuZm9ybWF0fWApO1xuICAgICAgICByZXR1cm4gYCR7ZG93bmxvYWRBc1RleHR9ICR7Zm9ybWF0LnRpdGxlfWA7XG4gICAgICB9LFxuICAgICAgaWNvbjogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IGZvcm1hdCA9IGZvcm1hdE9yRGVmYXVsdChgJHthcmdzLmZvcm1hdH1gKTtcbiAgICAgICAgcmV0dXJuIGZvcm1hdC5pY29uO1xuICAgICAgfSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jIGFyZ3MgPT4ge1xuICAgICAgICBjb25zdCBmb3JtYXQgPSBmb3JtYXRPckRlZmF1bHQoYCR7YXJncy5mb3JtYXR9YCk7XG4gICAgICAgIHJldHVybiBhd2FpdCBsaWNlbnNlc1RyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudC5tb2RlbC5kb3dubG9hZCh7XG4gICAgICAgICAgZm9ybWF0OiBmb3JtYXQuaWRcbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBoYW5kbGUgb3B0aW9uYWwgaW50ZWdyYXRpb25zXG4gICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNvbW1hbmQ6IENvbW1hbmRJRHMubGljZW5zZXMsIGNhdGVnb3J5IH0pO1xuICAgIH1cblxuICAgIGlmIChtZW51KSB7XG4gICAgICBjb25zdCBoZWxwTWVudSA9IG1lbnUuaGVscE1lbnU7XG4gICAgICBoZWxwTWVudS5hZGRHcm91cChbeyBjb21tYW5kOiBDb21tYW5kSURzLmxpY2Vuc2VzIH1dLCAwKTtcbiAgICB9XG5cbiAgICBpZiAocmVzdG9yZXIpIHtcbiAgICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZShsaWNlbnNlc1RyYWNrZXIsIHtcbiAgICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5saWNlbnNlcyxcbiAgICAgICAgbmFtZTogd2lkZ2V0ID0+ICdsaWNlbnNlcycsXG4gICAgICAgIGFyZ3M6IHdpZGdldCA9PiB7XG4gICAgICAgICAgY29uc3Qge1xuICAgICAgICAgICAgY3VycmVudEJ1bmRsZU5hbWUsXG4gICAgICAgICAgICBjdXJyZW50UGFja2FnZUluZGV4LFxuICAgICAgICAgICAgcGFja2FnZUZpbHRlclxuICAgICAgICAgIH0gPSB3aWRnZXQuY29udGVudC5tb2RlbDtcblxuICAgICAgICAgIGNvbnN0IGFyZ3M6IExpY2Vuc2VzLklDcmVhdGVBcmdzID0ge1xuICAgICAgICAgICAgY3VycmVudEJ1bmRsZU5hbWUsXG4gICAgICAgICAgICBjdXJyZW50UGFja2FnZUluZGV4LFxuICAgICAgICAgICAgcGFja2FnZUZpbHRlclxuICAgICAgICAgIH07XG4gICAgICAgICAgcmV0dXJuIGFyZ3MgYXMgUmVhZG9ubHlKU09OT2JqZWN0O1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG4gIH1cbn07XG5cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbXG4gIGFib3V0LFxuICBsYXVuY2hDbGFzc2ljLFxuICBqdXB5dGVyRm9ydW0sXG4gIHJlc291cmNlcyxcbiAgbGljZW5zZXNcbl07XG5cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFZEb21Nb2RlbCwgVkRvbVJlbmRlcmVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgU2VydmVyQ29ubmVjdGlvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IFRyYW5zbGF0aW9uQnVuZGxlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAganNvbkljb24sXG4gIExhYkljb24sXG4gIG1hcmtkb3duSWNvbixcbiAgc3ByZWFkc2hlZXRJY29uXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlLCBSZWFkb25seUpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBoLCBWaXJ0dWFsRWxlbWVudCB9IGZyb20gJ0BsdW1pbm8vdmlydHVhbGRvbSc7XG5pbXBvcnQgeyBQYW5lbCwgU3BsaXRQYW5lbCwgVGFiQmFyLCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG4vKipcbiAqIEEgbGljZW5zZSB2aWV3ZXJcbiAqL1xuZXhwb3J0IGNsYXNzIExpY2Vuc2VzIGV4dGVuZHMgU3BsaXRQYW5lbCB7XG4gIHJlYWRvbmx5IG1vZGVsOiBMaWNlbnNlcy5Nb2RlbDtcblxuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBMaWNlbnNlcy5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtTGljZW5zZXMnKTtcbiAgICB0aGlzLm1vZGVsID0gb3B0aW9ucy5tb2RlbDtcbiAgICB0aGlzLmluaXRMZWZ0UGFuZWwoKTtcbiAgICB0aGlzLmluaXRGaWx0ZXJzKCk7XG4gICAgdGhpcy5pbml0QnVuZGxlcygpO1xuICAgIHRoaXMuaW5pdEdyaWQoKTtcbiAgICB0aGlzLmluaXRMaWNlbnNlVGV4dCgpO1xuICAgIHRoaXMuc2V0UmVsYXRpdmVTaXplcyhbMSwgMiwgM10pO1xuICAgIHZvaWQgdGhpcy5tb2RlbC5pbml0TGljZW5zZXMoKS50aGVuKCgpID0+IHRoaXMuX3VwZGF0ZUJ1bmRsZXMoKSk7XG4gICAgdGhpcy5tb2RlbC50cmFja2VyRGF0YUNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICB0aGlzLnRpdGxlLmxhYmVsID0gdGhpcy5tb2RlbC50aXRsZTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgZGlzcG9zaW5nIG9mIHRoZSB3aWRnZXRcbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9idW5kbGVzLmN1cnJlbnRDaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy5vbkJ1bmRsZVNlbGVjdGVkLCB0aGlzKTtcbiAgICB0aGlzLm1vZGVsLmRpc3Bvc2UoKTtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSW5pdGlhbGl6ZSB0aGUgbGVmdCBhcmVhIGZvciBmaWx0ZXJzIGFuZCBidW5kbGVzXG4gICAqL1xuICBwcm90ZWN0ZWQgaW5pdExlZnRQYW5lbCgpOiB2b2lkIHtcbiAgICB0aGlzLl9sZWZ0UGFuZWwgPSBuZXcgUGFuZWwoKTtcbiAgICB0aGlzLl9sZWZ0UGFuZWwuYWRkQ2xhc3MoJ2pwLUxpY2Vuc2VzLUZvcm1BcmVhJyk7XG4gICAgdGhpcy5hZGRXaWRnZXQodGhpcy5fbGVmdFBhbmVsKTtcbiAgICBTcGxpdFBhbmVsLnNldFN0cmV0Y2godGhpcy5fbGVmdFBhbmVsLCAxKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbml0aWFsaXplIHRoZSBmaWx0ZXJzXG4gICAqL1xuICBwcm90ZWN0ZWQgaW5pdEZpbHRlcnMoKTogdm9pZCB7XG4gICAgdGhpcy5fZmlsdGVycyA9IG5ldyBMaWNlbnNlcy5GaWx0ZXJzKHRoaXMubW9kZWwpO1xuICAgIFNwbGl0UGFuZWwuc2V0U3RyZXRjaCh0aGlzLl9maWx0ZXJzLCAxKTtcbiAgICB0aGlzLl9sZWZ0UGFuZWwuYWRkV2lkZ2V0KHRoaXMuX2ZpbHRlcnMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEluaXRpYWxpemUgdGhlIGxpc3Rpbmcgb2YgYXZhaWxhYmxlIGJ1bmRsZXNcbiAgICovXG4gIHByb3RlY3RlZCBpbml0QnVuZGxlcygpOiB2b2lkIHtcbiAgICB0aGlzLl9idW5kbGVzID0gbmV3IFRhYkJhcih7XG4gICAgICBvcmllbnRhdGlvbjogJ3ZlcnRpY2FsJyxcbiAgICAgIHJlbmRlcmVyOiBuZXcgTGljZW5zZXMuQnVuZGxlVGFiUmVuZGVyZXIodGhpcy5tb2RlbClcbiAgICB9KTtcbiAgICB0aGlzLl9idW5kbGVzLmFkZENsYXNzKCdqcC1MaWNlbnNlcy1CdW5kbGVzJyk7XG4gICAgU3BsaXRQYW5lbC5zZXRTdHJldGNoKHRoaXMuX2J1bmRsZXMsIDEpO1xuICAgIHRoaXMuX2xlZnRQYW5lbC5hZGRXaWRnZXQodGhpcy5fYnVuZGxlcyk7XG4gICAgdGhpcy5fYnVuZGxlcy5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KHRoaXMub25CdW5kbGVTZWxlY3RlZCwgdGhpcyk7XG4gICAgdGhpcy5tb2RlbC5zdGF0ZUNoYW5nZWQuY29ubmVjdCgoKSA9PiB0aGlzLl9idW5kbGVzLnVwZGF0ZSgpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbml0aWFsaXplIHRoZSBsaXN0aW5nIG9mIHBhY2thZ2VzIHdpdGhpbiB0aGUgY3VycmVudCBidW5kbGVcbiAgICovXG4gIHByb3RlY3RlZCBpbml0R3JpZCgpOiB2b2lkIHtcbiAgICB0aGlzLl9ncmlkID0gbmV3IExpY2Vuc2VzLkdyaWQodGhpcy5tb2RlbCk7XG4gICAgU3BsaXRQYW5lbC5zZXRTdHJldGNoKHRoaXMuX2dyaWQsIDEpO1xuICAgIHRoaXMuYWRkV2lkZ2V0KHRoaXMuX2dyaWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIEluaXRpYWxpemUgdGhlIGZ1bGwgdGV4dCBvZiB0aGUgY3VycmVudCBwYWNrYWdlXG4gICAqL1xuICBwcm90ZWN0ZWQgaW5pdExpY2Vuc2VUZXh0KCk6IHZvaWQge1xuICAgIHRoaXMuX2xpY2Vuc2VUZXh0ID0gbmV3IExpY2Vuc2VzLkZ1bGxUZXh0KHRoaXMubW9kZWwpO1xuICAgIFNwbGl0UGFuZWwuc2V0U3RyZXRjaCh0aGlzLl9ncmlkLCAxKTtcbiAgICB0aGlzLmFkZFdpZGdldCh0aGlzLl9saWNlbnNlVGV4dCk7XG4gIH1cblxuICAvKipcbiAgICogRXZlbnQgaGFuZGxlciBmb3IgdXBkYXRpbmcgdGhlIG1vZGVsIHdpdGggdGhlIGN1cnJlbnQgYnVuZGxlXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CdW5kbGVTZWxlY3RlZCgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fYnVuZGxlcy5jdXJyZW50VGl0bGU/LmxhYmVsKSB7XG4gICAgICB0aGlzLm1vZGVsLmN1cnJlbnRCdW5kbGVOYW1lID0gdGhpcy5fYnVuZGxlcy5jdXJyZW50VGl0bGUubGFiZWw7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgYnVuZGxlIHRhYnMuXG4gICAqL1xuICBwcm90ZWN0ZWQgX3VwZGF0ZUJ1bmRsZXMoKTogdm9pZCB7XG4gICAgdGhpcy5fYnVuZGxlcy5jbGVhclRhYnMoKTtcbiAgICBsZXQgaSA9IDA7XG4gICAgY29uc3QgeyBjdXJyZW50QnVuZGxlTmFtZSB9ID0gdGhpcy5tb2RlbDtcbiAgICBsZXQgY3VycmVudEluZGV4ID0gMDtcbiAgICBmb3IgKGNvbnN0IGJ1bmRsZSBvZiB0aGlzLm1vZGVsLmJ1bmRsZU5hbWVzKSB7XG4gICAgICBjb25zdCB0YWIgPSBuZXcgV2lkZ2V0KCk7XG4gICAgICB0YWIudGl0bGUubGFiZWwgPSBidW5kbGU7XG4gICAgICBpZiAoYnVuZGxlID09PSBjdXJyZW50QnVuZGxlTmFtZSkge1xuICAgICAgICBjdXJyZW50SW5kZXggPSBpO1xuICAgICAgfVxuICAgICAgdGhpcy5fYnVuZGxlcy5pbnNlcnRUYWIoKytpLCB0YWIudGl0bGUpO1xuICAgIH1cbiAgICB0aGlzLl9idW5kbGVzLmN1cnJlbnRJbmRleCA9IGN1cnJlbnRJbmRleDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBbiBhcmVhIGZvciBzZWxlY3RpbmcgbGljZW5zZXMgYnkgYnVuZGxlIGFuZCBmaWx0ZXJzXG4gICAqL1xuICBwcm90ZWN0ZWQgX2xlZnRQYW5lbDogUGFuZWw7XG5cbiAgLyoqXG4gICAqIEZpbHRlcnMgb24gdmlzaWJsZSBsaWNlbnNlc1xuICAgKi9cbiAgcHJvdGVjdGVkIF9maWx0ZXJzOiBMaWNlbnNlcy5GaWx0ZXJzO1xuXG4gIC8qKlxuICAgKiBUYWJzIHJlZmxlY3RpbmcgYXZhaWxhYmxlIGJ1bmRsZXNcbiAgICovXG4gIHByb3RlY3RlZCBfYnVuZGxlczogVGFiQmFyPFdpZGdldD47XG5cbiAgLyoqXG4gICAqIEEgZ3JpZCBvZiB0aGUgY3VycmVudCBidW5kbGUncyBwYWNrYWdlcycgbGljZW5zZSBtZXRhZGF0YVxuICAgKi9cbiAgcHJvdGVjdGVkIF9ncmlkOiBMaWNlbnNlcy5HcmlkO1xuXG4gIC8qKlxuICAgKiBUaGUgY3VycmVudGx5LXNlbGVjdGVkIHBhY2thZ2UncyBmdWxsIGxpY2Vuc2UgdGV4dFxuICAgKi9cbiAgcHJvdGVjdGVkIF9saWNlbnNlVGV4dDogTGljZW5zZXMuRnVsbFRleHQ7XG59XG5cbi8qKiBBIG5hbWVzcGFjZSBmb3IgbGljZW5zZSBjb21wb25lbnRzICovXG5leHBvcnQgbmFtZXNwYWNlIExpY2Vuc2VzIHtcbiAgLyoqIFRoZSBpbmZvcm1hdGlvbiBhYm91dCBhIGxpY2Vuc2UgcmVwb3J0IGZvcm1hdCAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUmVwb3J0Rm9ybWF0IHtcbiAgICB0aXRsZTogc3RyaW5nO1xuICAgIGljb246IExhYkljb247XG4gICAgaWQ6IHN0cmluZztcbiAgfVxuXG4gIC8qKlxuICAgKiBMaWNlbnNlIHJlcG9ydCBmb3JtYXRzIHVuZGVyc3Rvb2QgYnkgdGhlIHNlcnZlciAob25jZSBsb3dlci1jYXNlZClcbiAgICovXG4gIGV4cG9ydCBjb25zdCBSRVBPUlRfRk9STUFUUzogUmVjb3JkPHN0cmluZywgSVJlcG9ydEZvcm1hdD4gPSB7XG4gICAgbWFya2Rvd246IHtcbiAgICAgIGlkOiAnbWFya2Rvd24nLFxuICAgICAgdGl0bGU6ICdNYXJrZG93bicsXG4gICAgICBpY29uOiBtYXJrZG93bkljb25cbiAgICB9LFxuICAgIGNzdjoge1xuICAgICAgaWQ6ICdjc3YnLFxuICAgICAgdGl0bGU6ICdDU1YnLFxuICAgICAgaWNvbjogc3ByZWFkc2hlZXRJY29uXG4gICAgfSxcbiAgICBqc29uOiB7XG4gICAgICBpZDogJ2NzdicsXG4gICAgICB0aXRsZTogJ0pTT04nLFxuICAgICAgaWNvbjoganNvbkljb25cbiAgICB9XG4gIH07XG5cbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IGZvcm1hdCAobW9zdCBodW1hbi1yZWFkYWJsZSlcbiAgICovXG4gIGV4cG9ydCBjb25zdCBERUZBVUxUX0ZPUk1BVCA9ICdtYXJrZG93bic7XG5cbiAgLyoqXG4gICAqIE9wdGlvbnMgZm9yIGluc3RhbnRpYXRpbmcgYSBsaWNlbnNlIHZpZXdlclxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgbW9kZWw6IE1vZGVsO1xuICB9XG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBpbnN0YW50aWF0aW5nIGEgbGljZW5zZSBtb2RlbFxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTW9kZWxPcHRpb25zIGV4dGVuZHMgSUNyZWF0ZUFyZ3Mge1xuICAgIGxpY2Vuc2VzVXJsOiBzdHJpbmc7XG4gICAgc2VydmVyU2V0dGluZ3M/OiBTZXJ2ZXJDb25uZWN0aW9uLklTZXR0aW5ncztcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIEpTT04gcmVzcG9uc2UgZnJvbSB0aGUgQVBJXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElMaWNlbnNlUmVzcG9uc2Uge1xuICAgIGJ1bmRsZXM6IHtcbiAgICAgIFtrZXk6IHN0cmluZ106IElMaWNlbnNlQnVuZGxlO1xuICAgIH07XG4gIH1cblxuICAvKipcbiAgICogQSB0b3AtbGV2ZWwgcmVwb3J0IG9mIHRoZSBsaWNlbnNlcyBmb3IgYWxsIGNvZGUgaW5jbHVkZWQgaW4gYSBidW5kbGVcbiAgICpcbiAgICogIyMjIE5vdGVcbiAgICpcbiAgICogVGhpcyBpcyByb3VnaGx5IGluZm9ybWVkIGJ5IHRoZSB0ZXJtcyBkZWZpbmVkIGluIHRoZSBTUERYIHNwZWMsIHRob3VnaCBpcyBub3RcbiAgICogYW4gU1BEWCBEb2N1bWVudCwgc2luY2UgdGhlcmUgc2VlbSB0byBiZSBzZXZlcmFsIChpbmNvbXBhdGlibGUpIHNwZWNzXG4gICAqIGluIHRoYXQgcmVwby5cbiAgICpcbiAgICogQHNlZSBodHRwczovL2dpdGh1Yi5jb20vc3BkeC9zcGR4LXNwZWMvYmxvYi9kZXZlbG9wbWVudC92Mi4yLjEvc2NoZW1hcy9zcGR4LXNjaGVtYS5qc29uXG4gICAqKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTGljZW5zZUJ1bmRsZSBleHRlbmRzIFJlYWRvbmx5SlNPTk9iamVjdCB7XG4gICAgcGFja2FnZXM6IElQYWNrYWdlTGljZW5zZUluZm9bXTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIGJlc3QtZWZmb3J0IHNpbmdsZSBidW5kbGVkIHBhY2thZ2UncyBpbmZvcm1hdGlvbi5cbiAgICpcbiAgICogIyMjIE5vdGVcbiAgICpcbiAgICogVGhpcyBpcyByb3VnaGx5IGluZm9ybWVkIGJ5IFNQRFggYHBhY2thZ2VzYCBhbmQgYGhhc0V4dHJhY3RlZExpY2Vuc2VJbmZvc2AsXG4gICAqIGFzIG1ha2luZyBpdCBjb25mb3JtYW50IHdvdWxkIHZhc3RseSBjb21wbGljYXRlIHRoZSBzdHJ1Y3R1cmUuXG4gICAqXG4gICAqIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3NwZHgvc3BkeC1zcGVjL2Jsb2IvZGV2ZWxvcG1lbnQvdjIuMi4xL3NjaGVtYXMvc3BkeC1zY2hlbWEuanNvblxuICAgKiovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVBhY2thZ2VMaWNlbnNlSW5mbyBleHRlbmRzIFJlYWRvbmx5SlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogdGhlIG5hbWUgb2YgdGhlIHBhY2thZ2UgYXMgaXQgYXBwZWFycyBpbiBwYWNrYWdlLmpzb25cbiAgICAgKi9cbiAgICBuYW1lOiBzdHJpbmc7XG4gICAgLyoqXG4gICAgICogdGhlIHZlcnNpb24gb2YgdGhlIHBhY2thZ2UsIG9yIGFuIGVtcHR5IHN0cmluZyBpZiB1bmtub3duXG4gICAgICovXG4gICAgdmVyc2lvbkluZm86IHN0cmluZztcbiAgICAvKipcbiAgICAgKiBhbiBTUERYIGxpY2Vuc2UgaWRlbnRpZmllciBvciBMaWNlbnNlUmVmLCBvciBhbiBlbXB0eSBzdHJpbmcgaWYgdW5rbm93blxuICAgICAqL1xuICAgIGxpY2Vuc2VJZDogc3RyaW5nO1xuICAgIC8qKlxuICAgICAqIHRoZSB2ZXJiYXRpbSBleHRyYWN0ZWQgdGV4dCBvZiB0aGUgbGljZW5zZSwgb3IgYW4gZW1wdHkgc3RyaW5nIGlmIHVua25vd25cbiAgICAgKi9cbiAgICBleHRyYWN0ZWRUZXh0OiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGZvcm1hdCBpbmZvcm1hdGlvbiBmb3IgYSBkb3dubG9hZFxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJRG93bmxvYWRPcHRpb25zIHtcbiAgICBmb3JtYXQ6IHN0cmluZztcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZmllbGRzIHdoaWNoIGNhbiBiZSBmaWx0ZXJlZFxuICAgKi9cbiAgZXhwb3J0IHR5cGUgVEZpbHRlcktleSA9ICduYW1lJyB8ICd2ZXJzaW9uSW5mbycgfCAnbGljZW5zZUlkJztcblxuICBleHBvcnQgaW50ZXJmYWNlIElDcmVhdGVBcmdzIHtcbiAgICBjdXJyZW50QnVuZGxlTmFtZT86IHN0cmluZyB8IG51bGw7XG4gICAgcGFja2FnZUZpbHRlcj86IFBhcnRpYWw8SVBhY2thZ2VMaWNlbnNlSW5mbz4gfCBudWxsO1xuICAgIGN1cnJlbnRQYWNrYWdlSW5kZXg/OiBudW1iZXIgfCBudWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgbW9kZWwgZm9yIGxpY2Vuc2UgZGF0YVxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIE1vZGVsIGV4dGVuZHMgVkRvbU1vZGVsIGltcGxlbWVudHMgSUNyZWF0ZUFyZ3Mge1xuICAgIGNvbnN0cnVjdG9yKG9wdGlvbnM6IElNb2RlbE9wdGlvbnMpIHtcbiAgICAgIHN1cGVyKCk7XG4gICAgICB0aGlzLl90cmFucyA9IG9wdGlvbnMudHJhbnM7XG4gICAgICB0aGlzLl9saWNlbnNlc1VybCA9IG9wdGlvbnMubGljZW5zZXNVcmw7XG4gICAgICB0aGlzLl9zZXJ2ZXJTZXR0aW5ncyA9XG4gICAgICAgIG9wdGlvbnMuc2VydmVyU2V0dGluZ3MgfHwgU2VydmVyQ29ubmVjdGlvbi5tYWtlU2V0dGluZ3MoKTtcbiAgICAgIGlmIChvcHRpb25zLmN1cnJlbnRCdW5kbGVOYW1lKSB7XG4gICAgICAgIHRoaXMuX2N1cnJlbnRCdW5kbGVOYW1lID0gb3B0aW9ucy5jdXJyZW50QnVuZGxlTmFtZTtcbiAgICAgIH1cbiAgICAgIGlmIChvcHRpb25zLnBhY2thZ2VGaWx0ZXIpIHtcbiAgICAgICAgdGhpcy5fcGFja2FnZUZpbHRlciA9IG9wdGlvbnMucGFja2FnZUZpbHRlcjtcbiAgICAgIH1cbiAgICAgIGlmIChvcHRpb25zLmN1cnJlbnRQYWNrYWdlSW5kZXgpIHtcbiAgICAgICAgdGhpcy5fY3VycmVudFBhY2thZ2VJbmRleCA9IG9wdGlvbnMuY3VycmVudFBhY2thZ2VJbmRleDtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBIYW5kbGUgdGhlIGluaXRpYWwgcmVxdWVzdCBmb3IgdGhlIGxpY2Vuc2VzIGZyb20gdGhlIHNlcnZlci5cbiAgICAgKi9cbiAgICBhc3luYyBpbml0TGljZW5zZXMoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICB0cnkge1xuICAgICAgICBjb25zdCByZXNwb25zZSA9IGF3YWl0IFNlcnZlckNvbm5lY3Rpb24ubWFrZVJlcXVlc3QoXG4gICAgICAgICAgdGhpcy5fbGljZW5zZXNVcmwsXG4gICAgICAgICAge30sXG4gICAgICAgICAgdGhpcy5fc2VydmVyU2V0dGluZ3NcbiAgICAgICAgKTtcbiAgICAgICAgdGhpcy5fc2VydmVyUmVzcG9uc2UgPSBhd2FpdCByZXNwb25zZS5qc29uKCk7XG4gICAgICAgIHRoaXMuX2xpY2Vuc2VzUmVhZHkucmVzb2x2ZSgpO1xuICAgICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgdGhpcy5fbGljZW5zZXNSZWFkeS5yZWplY3QoZXJyKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSB0ZW1wb3JhcnkgZG93bmxvYWQgbGluaywgYW5kIGVtdWxhdGUgY2xpY2tpbmcgaXQgdG8gdHJpZ2dlciBhIG5hbWVkXG4gICAgICogZmlsZSBkb3dubG9hZC5cbiAgICAgKi9cbiAgICBhc3luYyBkb3dubG9hZChvcHRpb25zOiBJRG93bmxvYWRPcHRpb25zKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICBjb25zdCB1cmwgPSBgJHt0aGlzLl9saWNlbnNlc1VybH0/Zm9ybWF0PSR7b3B0aW9ucy5mb3JtYXR9JmRvd25sb2FkPTFgO1xuICAgICAgY29uc3QgZWxlbWVudCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2EnKTtcbiAgICAgIGVsZW1lbnQuaHJlZiA9IHVybDtcbiAgICAgIGVsZW1lbnQuZG93bmxvYWQgPSAnJztcbiAgICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoZWxlbWVudCk7XG4gICAgICBlbGVtZW50LmNsaWNrKCk7XG4gICAgICBkb2N1bWVudC5ib2R5LnJlbW92ZUNoaWxkKGVsZW1lbnQpO1xuICAgICAgcmV0dXJuIHZvaWQgMDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBsaWNlbnNlcyBmcm9tIHRoZSBzZXJ2ZXIgY2hhbmdlXG4gICAgICovXG4gICAgZ2V0IHNlbGVjdGVkUGFja2FnZUNoYW5nZWQoKTogSVNpZ25hbDxNb2RlbCwgdm9pZD4ge1xuICAgICAgcmV0dXJuIHRoaXMuX3NlbGVjdGVkUGFja2FnZUNoYW5nZWQ7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgdHJhY2thYmxlIGRhdGEgY2hhbmdlc1xuICAgICAqL1xuICAgIGdldCB0cmFja2VyRGF0YUNoYW5nZWQoKTogSVNpZ25hbDxNb2RlbCwgdm9pZD4ge1xuICAgICAgcmV0dXJuIHRoaXMuX3RyYWNrZXJEYXRhQ2hhbmdlZDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmFtZXMgb2YgdGhlIGxpY2Vuc2UgYnVuZGxlcyBhdmFpbGFibGVcbiAgICAgKi9cbiAgICBnZXQgYnVuZGxlTmFtZXMoKTogc3RyaW5nW10ge1xuICAgICAgcmV0dXJuIE9iamVjdC5rZXlzKHRoaXMuX3NlcnZlclJlc3BvbnNlPy5idW5kbGVzIHx8IHt9KTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBsaWNlbnNlIGJ1bmRsZVxuICAgICAqL1xuICAgIGdldCBjdXJyZW50QnVuZGxlTmFtZSgpOiBzdHJpbmcgfCBudWxsIHtcbiAgICAgIGlmICh0aGlzLl9jdXJyZW50QnVuZGxlTmFtZSkge1xuICAgICAgICByZXR1cm4gdGhpcy5fY3VycmVudEJ1bmRsZU5hbWU7XG4gICAgICB9XG4gICAgICBpZiAodGhpcy5idW5kbGVOYW1lcy5sZW5ndGgpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuYnVuZGxlTmFtZXNbMF07XG4gICAgICB9XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBTZXQgdGhlIGN1cnJlbnQgbGljZW5zZSBidW5kbGUsIGFuZCByZXNldCB0aGUgc2VsZWN0ZWQgaW5kZXhcbiAgICAgKi9cbiAgICBzZXQgY3VycmVudEJ1bmRsZU5hbWUoY3VycmVudEJ1bmRsZU5hbWU6IHN0cmluZyB8IG51bGwpIHtcbiAgICAgIGlmICh0aGlzLl9jdXJyZW50QnVuZGxlTmFtZSAhPT0gY3VycmVudEJ1bmRsZU5hbWUpIHtcbiAgICAgICAgdGhpcy5fY3VycmVudEJ1bmRsZU5hbWUgPSBjdXJyZW50QnVuZGxlTmFtZTtcbiAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgICB0aGlzLl90cmFja2VyRGF0YUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIGxpY2Vuc2VzIGFyZSBhdmFpbGFibGUgZnJvbSB0aGUgc2VydmVyXG4gICAgICovXG4gICAgZ2V0IGxpY2Vuc2VzUmVhZHkoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICByZXR1cm4gdGhpcy5fbGljZW5zZXNSZWFkeS5wcm9taXNlO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEFsbCB0aGUgbGljZW5zZSBidW5kbGVzLCBrZXllZCBieSB0aGUgZGlzdHJpYnV0aW5nIHBhY2thZ2VzXG4gICAgICovXG4gICAgZ2V0IGJ1bmRsZXMoKTogbnVsbCB8IHsgW2tleTogc3RyaW5nXTogSUxpY2Vuc2VCdW5kbGUgfSB7XG4gICAgICByZXR1cm4gdGhpcy5fc2VydmVyUmVzcG9uc2U/LmJ1bmRsZXMgfHwge307XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGluZGV4IG9mIHRoZSBjdXJyZW50bHktc2VsZWN0ZWQgcGFja2FnZSB3aXRoaW4gaXRzIGxpY2Vuc2UgYnVuZGxlXG4gICAgICovXG4gICAgZ2V0IGN1cnJlbnRQYWNrYWdlSW5kZXgoKTogbnVtYmVyIHwgbnVsbCB7XG4gICAgICByZXR1cm4gdGhpcy5fY3VycmVudFBhY2thZ2VJbmRleDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBVcGRhdGUgdGhlIGN1cnJlbnRseS1zZWxlY3RlZCBwYWNrYWdlIHdpdGhpbiBpdHMgbGljZW5zZSBidW5kbGVcbiAgICAgKi9cbiAgICBzZXQgY3VycmVudFBhY2thZ2VJbmRleChjdXJyZW50UGFja2FnZUluZGV4OiBudW1iZXIgfCBudWxsKSB7XG4gICAgICBpZiAodGhpcy5fY3VycmVudFBhY2thZ2VJbmRleCA9PT0gY3VycmVudFBhY2thZ2VJbmRleCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICB0aGlzLl9jdXJyZW50UGFja2FnZUluZGV4ID0gY3VycmVudFBhY2thZ2VJbmRleDtcbiAgICAgIHRoaXMuX3NlbGVjdGVkUGFja2FnZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgdGhpcy5fdHJhY2tlckRhdGFDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbGljZW5zZSBkYXRhIGZvciB0aGUgY3VycmVudGx5LXNlbGVjdGVkIHBhY2thZ2VcbiAgICAgKi9cbiAgICBnZXQgY3VycmVudFBhY2thZ2UoKTogSVBhY2thZ2VMaWNlbnNlSW5mbyB8IG51bGwge1xuICAgICAgaWYgKFxuICAgICAgICB0aGlzLmN1cnJlbnRCdW5kbGVOYW1lICYmXG4gICAgICAgIHRoaXMuYnVuZGxlcyAmJlxuICAgICAgICB0aGlzLl9jdXJyZW50UGFja2FnZUluZGV4ICE9IG51bGxcbiAgICAgICkge1xuICAgICAgICByZXR1cm4gdGhpcy5nZXRGaWx0ZXJlZFBhY2thZ2VzKFxuICAgICAgICAgIHRoaXMuYnVuZGxlc1t0aGlzLmN1cnJlbnRCdW5kbGVOYW1lXT8ucGFja2FnZXMgfHwgW11cbiAgICAgICAgKVt0aGlzLl9jdXJyZW50UGFja2FnZUluZGV4XTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQSB0cmFuc2xhdGlvbiBidW5kbGVcbiAgICAgKi9cbiAgICBnZXQgdHJhbnMoKTogVHJhbnNsYXRpb25CdW5kbGUge1xuICAgICAgcmV0dXJuIHRoaXMuX3RyYW5zO1xuICAgIH1cblxuICAgIGdldCB0aXRsZSgpOiBzdHJpbmcge1xuICAgICAgcmV0dXJuIGAke3RoaXMuX2N1cnJlbnRCdW5kbGVOYW1lIHx8ICcnfSAke3RoaXMuX3RyYW5zLl9fKFxuICAgICAgICAnTGljZW5zZXMnXG4gICAgICApfWAudHJpbSgpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IHBhY2thZ2UgZmlsdGVyXG4gICAgICovXG4gICAgZ2V0IHBhY2thZ2VGaWx0ZXIoKTogUGFydGlhbDxJUGFja2FnZUxpY2Vuc2VJbmZvPiB7XG4gICAgICByZXR1cm4gdGhpcy5fcGFja2FnZUZpbHRlcjtcbiAgICB9XG5cbiAgICBzZXQgcGFja2FnZUZpbHRlcihwYWNrYWdlRmlsdGVyOiBQYXJ0aWFsPElQYWNrYWdlTGljZW5zZUluZm8+KSB7XG4gICAgICB0aGlzLl9wYWNrYWdlRmlsdGVyID0gcGFja2FnZUZpbHRlcjtcbiAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICAgIHRoaXMuX3RyYWNrZXJEYXRhQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IGZpbHRlcmVkIHBhY2thZ2VzIGZyb20gY3VycmVudCBidW5kbGUgd2hlcmUgYXQgbGVhc3Qgb25lIHRva2VuIG9mIGVhY2hcbiAgICAgKiBrZXkgaXMgcHJlc2VudC5cbiAgICAgKi9cbiAgICBnZXRGaWx0ZXJlZFBhY2thZ2VzKGFsbFJvd3M6IElQYWNrYWdlTGljZW5zZUluZm9bXSk6IElQYWNrYWdlTGljZW5zZUluZm9bXSB7XG4gICAgICBsZXQgcm93czogSVBhY2thZ2VMaWNlbnNlSW5mb1tdID0gW107XG4gICAgICBsZXQgZmlsdGVyczogW3N0cmluZywgc3RyaW5nW11dW10gPSBPYmplY3QuZW50cmllcyh0aGlzLl9wYWNrYWdlRmlsdGVyKVxuICAgICAgICAuZmlsdGVyKChbaywgdl0pID0+IHYgJiYgYCR7dn1gLnRyaW0oKS5sZW5ndGgpXG4gICAgICAgIC5tYXAoKFtrLCB2XSkgPT4gW2ssIGAke3Z9YC50b0xvd2VyQ2FzZSgpLnRyaW0oKS5zcGxpdCgnICcpXSk7XG4gICAgICBmb3IgKGNvbnN0IHJvdyBvZiBhbGxSb3dzKSB7XG4gICAgICAgIGxldCBrZXlIaXRzID0gMDtcbiAgICAgICAgZm9yIChjb25zdCBba2V5LCBiaXRzXSBvZiBmaWx0ZXJzKSB7XG4gICAgICAgICAgbGV0IGJpdEhpdHMgPSAwO1xuICAgICAgICAgIGxldCByb3dLZXlWYWx1ZSA9IGAke3Jvd1trZXldfWAudG9Mb3dlckNhc2UoKTtcbiAgICAgICAgICBmb3IgKGNvbnN0IGJpdCBvZiBiaXRzKSB7XG4gICAgICAgICAgICBpZiAocm93S2V5VmFsdWUuaW5jbHVkZXMoYml0KSkge1xuICAgICAgICAgICAgICBiaXRIaXRzICs9IDE7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfVxuICAgICAgICAgIGlmIChiaXRIaXRzKSB7XG4gICAgICAgICAgICBrZXlIaXRzICs9IDE7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGlmIChrZXlIaXRzID09PSBmaWx0ZXJzLmxlbmd0aCkge1xuICAgICAgICAgIHJvd3MucHVzaChyb3cpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gT2JqZWN0LnZhbHVlcyhyb3dzKTtcbiAgICB9XG5cbiAgICBwcml2YXRlIF9zZWxlY3RlZFBhY2thZ2VDaGFuZ2VkOiBTaWduYWw8TW9kZWwsIHZvaWQ+ID0gbmV3IFNpZ25hbCh0aGlzKTtcbiAgICBwcml2YXRlIF90cmFja2VyRGF0YUNoYW5nZWQ6IFNpZ25hbDxNb2RlbCwgdm9pZD4gPSBuZXcgU2lnbmFsKHRoaXMpO1xuICAgIHByaXZhdGUgX3NlcnZlclJlc3BvbnNlOiBJTGljZW5zZVJlc3BvbnNlIHwgbnVsbDtcbiAgICBwcml2YXRlIF9saWNlbnNlc1VybDogc3RyaW5nO1xuICAgIHByaXZhdGUgX3NlcnZlclNldHRpbmdzOiBTZXJ2ZXJDb25uZWN0aW9uLklTZXR0aW5ncztcbiAgICBwcml2YXRlIF9jdXJyZW50QnVuZGxlTmFtZTogc3RyaW5nIHwgbnVsbDtcbiAgICBwcml2YXRlIF90cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG4gICAgcHJpdmF0ZSBfY3VycmVudFBhY2thZ2VJbmRleDogbnVtYmVyIHwgbnVsbCA9IDA7XG4gICAgcHJpdmF0ZSBfbGljZW5zZXNSZWFkeSA9IG5ldyBQcm9taXNlRGVsZWdhdGU8dm9pZD4oKTtcbiAgICBwcml2YXRlIF9wYWNrYWdlRmlsdGVyOiBQYXJ0aWFsPElQYWNrYWdlTGljZW5zZUluZm8+ID0ge307XG4gIH1cblxuICAvKipcbiAgICogQSBmaWx0ZXIgZm9ybSBmb3IgbGltaXRpbmcgdGhlIHBhY2thZ2VzIGRpc3BsYXllZFxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIEZpbHRlcnMgZXh0ZW5kcyBWRG9tUmVuZGVyZXI8TW9kZWw+IHtcbiAgICBjb25zdHJ1Y3Rvcihtb2RlbDogTW9kZWwpIHtcbiAgICAgIHN1cGVyKG1vZGVsKTtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLUxpY2Vuc2VzLUZpbHRlcnMnKTtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLVJlbmRlcmVkSFRNTENvbW1vbicpO1xuICAgIH1cblxuICAgIHByb3RlY3RlZCByZW5kZXIoKTogSlNYLkVsZW1lbnQge1xuICAgICAgY29uc3QgeyB0cmFucyB9ID0gdGhpcy5tb2RlbDtcbiAgICAgIHJldHVybiAoXG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgPGxhYmVsPlxuICAgICAgICAgICAgPHN0cm9uZz57dHJhbnMuX18oJ0ZpbHRlciBMaWNlbnNlcyBCeScpfTwvc3Ryb25nPlxuICAgICAgICAgIDwvbGFiZWw+XG4gICAgICAgICAgPHVsPlxuICAgICAgICAgICAgPGxpPlxuICAgICAgICAgICAgICA8bGFiZWw+e3RyYW5zLl9fKCdQYWNrYWdlJyl9PC9sYWJlbD5cbiAgICAgICAgICAgICAge3RoaXMucmVuZGVyRmlsdGVyKCduYW1lJyl9XG4gICAgICAgICAgICA8L2xpPlxuICAgICAgICAgICAgPGxpPlxuICAgICAgICAgICAgICA8bGFiZWw+e3RyYW5zLl9fKCdWZXJzaW9uJyl9PC9sYWJlbD5cbiAgICAgICAgICAgICAge3RoaXMucmVuZGVyRmlsdGVyKCd2ZXJzaW9uSW5mbycpfVxuICAgICAgICAgICAgPC9saT5cbiAgICAgICAgICAgIDxsaT5cbiAgICAgICAgICAgICAgPGxhYmVsPnt0cmFucy5fXygnTGljZW5zZScpfTwvbGFiZWw+XG4gICAgICAgICAgICAgIHt0aGlzLnJlbmRlckZpbHRlcignbGljZW5zZUlkJyl9XG4gICAgICAgICAgICA8L2xpPlxuICAgICAgICAgIDwvdWw+XG4gICAgICAgICAgPGxhYmVsPlxuICAgICAgICAgICAgPHN0cm9uZz57dHJhbnMuX18oJ0Rpc3RyaWJ1dGlvbnMnKX08L3N0cm9uZz5cbiAgICAgICAgICA8L2xhYmVsPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVuZGVyIGEgZmlsdGVyIGlucHV0XG4gICAgICovXG4gICAgcHJvdGVjdGVkIHJlbmRlckZpbHRlciA9IChrZXk6IFRGaWx0ZXJLZXkpOiBKU1guRWxlbWVudCA9PiB7XG4gICAgICBjb25zdCB2YWx1ZSA9IHRoaXMubW9kZWwucGFja2FnZUZpbHRlcltrZXldIHx8ICcnO1xuICAgICAgcmV0dXJuIChcbiAgICAgICAgPGlucHV0XG4gICAgICAgICAgdHlwZT1cInRleHRcIlxuICAgICAgICAgIG5hbWU9e2tleX1cbiAgICAgICAgICBkZWZhdWx0VmFsdWU9e3ZhbHVlfVxuICAgICAgICAgIGNsYXNzTmFtZT1cImpwLW1vZC1zdHlsZWRcIlxuICAgICAgICAgIG9uSW5wdXQ9e3RoaXMub25GaWx0ZXJJbnB1dH1cbiAgICAgICAgLz5cbiAgICAgICk7XG4gICAgfTtcblxuICAgIC8qKlxuICAgICAqIEhhbmRsZSBhIGZpbHRlciBpbnB1dCBjaGFuZ2luZ1xuICAgICAqL1xuICAgIHByb3RlY3RlZCBvbkZpbHRlcklucHV0ID0gKFxuICAgICAgZXZ0OiBSZWFjdC5DaGFuZ2VFdmVudDxIVE1MSW5wdXRFbGVtZW50PlxuICAgICk6IHZvaWQgPT4ge1xuICAgICAgY29uc3QgaW5wdXQgPSBldnQuY3VycmVudFRhcmdldDtcbiAgICAgIGNvbnN0IHsgbmFtZSwgdmFsdWUgfSA9IGlucHV0O1xuICAgICAgdGhpcy5tb2RlbC5wYWNrYWdlRmlsdGVyID0geyAuLi50aGlzLm1vZGVsLnBhY2thZ2VGaWx0ZXIsIFtuYW1lXTogdmFsdWUgfTtcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIEEgZmFuY3kgYnVuZGxlIHJlbmRlcmVyIHdpdGggdGhlIHBhY2thZ2UgY291bnRcbiAgICovXG4gIGV4cG9ydCBjbGFzcyBCdW5kbGVUYWJSZW5kZXJlciBleHRlbmRzIFRhYkJhci5SZW5kZXJlciB7XG4gICAgLyoqXG4gICAgICogQSBtb2RlbCBvZiB0aGUgc3RhdGUgb2YgbGljZW5zZSB2aWV3aW5nIGFzIHdlbGwgYXMgdGhlIHVuZGVybHlpbmcgZGF0YVxuICAgICAqL1xuICAgIG1vZGVsOiBNb2RlbDtcblxuICAgIHJlYWRvbmx5IGNsb3NlSWNvblNlbGVjdG9yID0gJy5sbS1UYWJCYXItdGFiQ2xvc2VJY29uJztcblxuICAgIGNvbnN0cnVjdG9yKG1vZGVsOiBNb2RlbCkge1xuICAgICAgc3VwZXIoKTtcbiAgICAgIHRoaXMubW9kZWwgPSBtb2RlbDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW5kZXIgYSBmdWxsIGJ1bmRsZVxuICAgICAqL1xuICAgIHJlbmRlclRhYihkYXRhOiBUYWJCYXIuSVJlbmRlckRhdGE8V2lkZ2V0Pik6IFZpcnR1YWxFbGVtZW50IHtcbiAgICAgIGxldCB0aXRsZSA9IGRhdGEudGl0bGUuY2FwdGlvbjtcbiAgICAgIGxldCBrZXkgPSB0aGlzLmNyZWF0ZVRhYktleShkYXRhKTtcbiAgICAgIGxldCBzdHlsZSA9IHRoaXMuY3JlYXRlVGFiU3R5bGUoZGF0YSk7XG4gICAgICBsZXQgY2xhc3NOYW1lID0gdGhpcy5jcmVhdGVUYWJDbGFzcyhkYXRhKTtcbiAgICAgIGxldCBkYXRhc2V0ID0gdGhpcy5jcmVhdGVUYWJEYXRhc2V0KGRhdGEpO1xuICAgICAgcmV0dXJuIGgubGkoXG4gICAgICAgIHsga2V5LCBjbGFzc05hbWUsIHRpdGxlLCBzdHlsZSwgZGF0YXNldCB9LFxuICAgICAgICB0aGlzLnJlbmRlckljb24oZGF0YSksXG4gICAgICAgIHRoaXMucmVuZGVyTGFiZWwoZGF0YSksXG4gICAgICAgIHRoaXMucmVuZGVyQ291bnRCYWRnZShkYXRhKVxuICAgICAgKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW5kZXIgdGhlIHBhY2thZ2UgY291bnRcbiAgICAgKi9cbiAgICByZW5kZXJDb3VudEJhZGdlKGRhdGE6IFRhYkJhci5JUmVuZGVyRGF0YTxXaWRnZXQ+KTogVmlydHVhbEVsZW1lbnQge1xuICAgICAgY29uc3QgYnVuZGxlID0gZGF0YS50aXRsZS5sYWJlbDtcbiAgICAgIGNvbnN0IHsgYnVuZGxlcyB9ID0gdGhpcy5tb2RlbDtcbiAgICAgIGNvbnN0IHBhY2thZ2VzID0gdGhpcy5tb2RlbC5nZXRGaWx0ZXJlZFBhY2thZ2VzKFxuICAgICAgICAoYnVuZGxlcyAmJiBidW5kbGUgPyBidW5kbGVzW2J1bmRsZV0ucGFja2FnZXMgOiBbXSkgfHwgW11cbiAgICAgICk7XG4gICAgICByZXR1cm4gaC5sYWJlbCh7fSwgYCR7cGFja2FnZXMubGVuZ3RofWApO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBIGdyaWQgb2YgbGljZW5zZXNcbiAgICovXG4gIGV4cG9ydCBjbGFzcyBHcmlkIGV4dGVuZHMgVkRvbVJlbmRlcmVyPExpY2Vuc2VzLk1vZGVsPiB7XG4gICAgY29uc3RydWN0b3IobW9kZWw6IExpY2Vuc2VzLk1vZGVsKSB7XG4gICAgICBzdXBlcihtb2RlbCk7XG4gICAgICB0aGlzLmFkZENsYXNzKCdqcC1MaWNlbnNlcy1HcmlkJyk7XG4gICAgICB0aGlzLmFkZENsYXNzKCdqcC1SZW5kZXJlZEhUTUxDb21tb24nKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW5kZXIgYSBncmlkIG9mIHBhY2thZ2UgbGljZW5zZSBpbmZvcm1hdGlvblxuICAgICAqL1xuICAgIHByb3RlY3RlZCByZW5kZXIoKTogSlNYLkVsZW1lbnQge1xuICAgICAgY29uc3QgeyBidW5kbGVzLCBjdXJyZW50QnVuZGxlTmFtZSwgdHJhbnMgfSA9IHRoaXMubW9kZWw7XG4gICAgICBjb25zdCBmaWx0ZXJlZFBhY2thZ2VzID0gdGhpcy5tb2RlbC5nZXRGaWx0ZXJlZFBhY2thZ2VzKFxuICAgICAgICBidW5kbGVzICYmIGN1cnJlbnRCdW5kbGVOYW1lXG4gICAgICAgICAgPyBidW5kbGVzW2N1cnJlbnRCdW5kbGVOYW1lXT8ucGFja2FnZXMgfHwgW11cbiAgICAgICAgICA6IFtdXG4gICAgICApO1xuICAgICAgaWYgKCFmaWx0ZXJlZFBhY2thZ2VzLmxlbmd0aCkge1xuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgIDxibG9ja3F1b3RlPlxuICAgICAgICAgICAgPGVtPnt0cmFucy5fXygnTm8gUGFja2FnZXMgZm91bmQnKX08L2VtPlxuICAgICAgICAgIDwvYmxvY2txdW90ZT5cbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiAoXG4gICAgICAgIDxmb3JtPlxuICAgICAgICAgIDx0YWJsZT5cbiAgICAgICAgICAgIDx0aGVhZD5cbiAgICAgICAgICAgICAgPHRyPlxuICAgICAgICAgICAgICAgIDx0ZD48L3RkPlxuICAgICAgICAgICAgICAgIDx0aD57dHJhbnMuX18oJ1BhY2thZ2UnKX08L3RoPlxuICAgICAgICAgICAgICAgIDx0aD57dHJhbnMuX18oJ1ZlcnNpb24nKX08L3RoPlxuICAgICAgICAgICAgICAgIDx0aD57dHJhbnMuX18oJ0xpY2Vuc2UnKX08L3RoPlxuICAgICAgICAgICAgICA8L3RyPlxuICAgICAgICAgICAgPC90aGVhZD5cbiAgICAgICAgICAgIDx0Ym9keT57ZmlsdGVyZWRQYWNrYWdlcy5tYXAodGhpcy5yZW5kZXJSb3cpfTwvdGJvZHk+XG4gICAgICAgICAgPC90YWJsZT5cbiAgICAgICAgPC9mb3JtPlxuICAgICAgKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW5kZXIgYSBzaW5nbGUgcGFja2FnZSdzIGxpY2Vuc2UgaW5mb3JtYXRpb25cbiAgICAgKi9cbiAgICBwcm90ZWN0ZWQgcmVuZGVyUm93ID0gKFxuICAgICAgcm93OiBMaWNlbnNlcy5JUGFja2FnZUxpY2Vuc2VJbmZvLFxuICAgICAgaW5kZXg6IG51bWJlclxuICAgICk6IEpTWC5FbGVtZW50ID0+IHtcbiAgICAgIGNvbnN0IHNlbGVjdGVkID0gaW5kZXggPT09IHRoaXMubW9kZWwuY3VycmVudFBhY2thZ2VJbmRleDtcbiAgICAgIGNvbnN0IG9uQ2hlY2sgPSAoKSA9PiAodGhpcy5tb2RlbC5jdXJyZW50UGFja2FnZUluZGV4ID0gaW5kZXgpO1xuICAgICAgcmV0dXJuIChcbiAgICAgICAgPHRyXG4gICAgICAgICAga2V5PXtyb3cubmFtZX1cbiAgICAgICAgICBjbGFzc05hbWU9e3NlbGVjdGVkID8gJ2pwLW1vZC1zZWxlY3RlZCcgOiAnJ31cbiAgICAgICAgICBvbkNsaWNrPXtvbkNoZWNrfVxuICAgICAgICA+XG4gICAgICAgICAgPHRkPlxuICAgICAgICAgICAgPGlucHV0XG4gICAgICAgICAgICAgIHR5cGU9XCJyYWRpb1wiXG4gICAgICAgICAgICAgIG5hbWU9XCJzaG93LXBhY2thZ2UtbGljZW5zZVwiXG4gICAgICAgICAgICAgIHZhbHVlPXtpbmRleH1cbiAgICAgICAgICAgICAgb25DaGFuZ2U9e29uQ2hlY2t9XG4gICAgICAgICAgICAgIGNoZWNrZWQ9e3NlbGVjdGVkfVxuICAgICAgICAgICAgLz5cbiAgICAgICAgICA8L3RkPlxuICAgICAgICAgIDx0aD57cm93Lm5hbWV9PC90aD5cbiAgICAgICAgICA8dGQ+XG4gICAgICAgICAgICA8Y29kZT57cm93LnZlcnNpb25JbmZvfTwvY29kZT5cbiAgICAgICAgICA8L3RkPlxuICAgICAgICAgIDx0ZD5cbiAgICAgICAgICAgIDxjb2RlPntyb3cubGljZW5zZUlkfTwvY29kZT5cbiAgICAgICAgICA8L3RkPlxuICAgICAgICA8L3RyPlxuICAgICAgKTtcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcGFja2FnZSdzIGZ1bGwgbGljZW5zZSB0ZXh0XG4gICAqL1xuICBleHBvcnQgY2xhc3MgRnVsbFRleHQgZXh0ZW5kcyBWRG9tUmVuZGVyZXI8TW9kZWw+IHtcbiAgICBjb25zdHJ1Y3Rvcihtb2RlbDogTW9kZWwpIHtcbiAgICAgIHN1cGVyKG1vZGVsKTtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLUxpY2Vuc2VzLVRleHQnKTtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLVJlbmRlcmVkSFRNTENvbW1vbicpO1xuICAgICAgdGhpcy5hZGRDbGFzcygnanAtUmVuZGVyZWRNYXJrZG93bicpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlbmRlciB0aGUgbGljZW5zZSB0ZXh0LCBvciBhIG51bGwgc3RhdGUgaWYgbm8gcGFja2FnZSBpcyBzZWxlY3RlZFxuICAgICAqL1xuICAgIHByb3RlY3RlZCByZW5kZXIoKTogSlNYLkVsZW1lbnRbXSB7XG4gICAgICBjb25zdCB7IGN1cnJlbnRQYWNrYWdlLCB0cmFucyB9ID0gdGhpcy5tb2RlbDtcbiAgICAgIGxldCBoZWFkID0gJyc7XG4gICAgICBsZXQgcXVvdGUgPSB0cmFucy5fXygnTm8gUGFja2FnZSBzZWxlY3RlZCcpO1xuICAgICAgbGV0IGNvZGUgPSAnJztcbiAgICAgIGlmIChjdXJyZW50UGFja2FnZSkge1xuICAgICAgICBjb25zdCB7IG5hbWUsIHZlcnNpb25JbmZvLCBsaWNlbnNlSWQsIGV4dHJhY3RlZFRleHQgfSA9IGN1cnJlbnRQYWNrYWdlO1xuICAgICAgICBoZWFkID0gYCR7bmFtZX0gdiR7dmVyc2lvbkluZm99YDtcbiAgICAgICAgcXVvdGUgPSBgJHt0cmFucy5fXygnTGljZW5zZScpfTogJHtcbiAgICAgICAgICBsaWNlbnNlSWQgfHwgdHJhbnMuX18oJ05vIExpY2Vuc2UgSUQgZm91bmQnKVxuICAgICAgICB9YDtcbiAgICAgICAgY29kZSA9IGV4dHJhY3RlZFRleHQgfHwgdHJhbnMuX18oJ05vIExpY2Vuc2UgVGV4dCBmb3VuZCcpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIFtcbiAgICAgICAgPGgxIGtleT1cImgxXCI+e2hlYWR9PC9oMT4sXG4gICAgICAgIDxibG9ja3F1b3RlIGtleT1cInF1b3RlXCI+XG4gICAgICAgICAgPGVtPntxdW90ZX08L2VtPlxuICAgICAgICA8L2Jsb2NrcXVvdGU+LFxuICAgICAgICA8Y29kZSBrZXk9XCJjb2RlXCI+e2NvZGV9PC9jb2RlPlxuICAgICAgXTtcbiAgICB9XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0=