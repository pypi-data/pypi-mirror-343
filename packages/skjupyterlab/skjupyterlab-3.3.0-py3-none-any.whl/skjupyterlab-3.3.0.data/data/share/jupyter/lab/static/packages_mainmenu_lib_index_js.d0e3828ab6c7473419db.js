(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_mainmenu_lib_index_js"],{

/***/ "../packages/mainmenu/lib/edit.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/edit.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EditMenu": () => (/* binding */ EditMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Edit menu for the application.
 */
class EditMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the edit menu.
     */
    constructor(options) {
        super(options);
        this.undoers = new Set();
        this.clearers = new Set();
        this.goToLiners = new Set();
    }
    /**
     * Dispose of the resources held by the edit menu.
     */
    dispose() {
        this.undoers.clear();
        this.clearers.clear();
        super.dispose();
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/file.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/file.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FileMenu": () => (/* binding */ FileMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible FileMenu for the application.
 */
class FileMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    constructor(options) {
        super(options);
        this.quitEntry = false;
        // Create the "New" submenu.
        this.closeAndCleaners = new Set();
        this.consoleCreators = new Set();
    }
    /**
     * The New submenu.
     */
    get newMenu() {
        var _a, _b;
        if (!this._newMenu) {
            this._newMenu = (_b = (_a = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.find)(this.items, menu => { var _a; return ((_a = menu.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-file-new'; })) === null || _a === void 0 ? void 0 : _a.submenu) !== null && _b !== void 0 ? _b : new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu({
                commands: this.commands
            });
        }
        return this._newMenu;
    }
    /**
     * Dispose of the resources held by the file menu.
     */
    dispose() {
        var _a;
        (_a = this._newMenu) === null || _a === void 0 ? void 0 : _a.dispose();
        this.consoleCreators.clear();
        super.dispose();
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/help.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/help.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HelpMenu": () => (/* binding */ HelpMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Help menu for the application.
 */
class HelpMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the help menu.
     */
    constructor(options) {
        super(options);
        this.kernelUsers = new Set();
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/index.js":
/*!*****************************************!*\
  !*** ../packages/mainmenu/lib/index.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MainMenu": () => (/* reexport safe */ _mainmenu__WEBPACK_IMPORTED_MODULE_0__.MainMenu),
/* harmony export */   "EditMenu": () => (/* reexport safe */ _edit__WEBPACK_IMPORTED_MODULE_1__.EditMenu),
/* harmony export */   "FileMenu": () => (/* reexport safe */ _file__WEBPACK_IMPORTED_MODULE_2__.FileMenu),
/* harmony export */   "HelpMenu": () => (/* reexport safe */ _help__WEBPACK_IMPORTED_MODULE_3__.HelpMenu),
/* harmony export */   "KernelMenu": () => (/* reexport safe */ _kernel__WEBPACK_IMPORTED_MODULE_4__.KernelMenu),
/* harmony export */   "RunMenu": () => (/* reexport safe */ _run__WEBPACK_IMPORTED_MODULE_5__.RunMenu),
/* harmony export */   "SettingsMenu": () => (/* reexport safe */ _settings__WEBPACK_IMPORTED_MODULE_6__.SettingsMenu),
/* harmony export */   "ViewMenu": () => (/* reexport safe */ _view__WEBPACK_IMPORTED_MODULE_7__.ViewMenu),
/* harmony export */   "TabsMenu": () => (/* reexport safe */ _tabs__WEBPACK_IMPORTED_MODULE_8__.TabsMenu),
/* harmony export */   "IMainMenu": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_9__.IMainMenu),
/* harmony export */   "IJupyterLabMenu": () => (/* reexport safe */ _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_10__.IRankedMenu),
/* harmony export */   "JupyterLabMenu": () => (/* reexport safe */ _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_10__.RankedMenu)
/* harmony export */ });
/* harmony import */ var _mainmenu__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./mainmenu */ "../packages/mainmenu/lib/mainmenu.js");
/* harmony import */ var _edit__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./edit */ "../packages/mainmenu/lib/edit.js");
/* harmony import */ var _file__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./file */ "../packages/mainmenu/lib/file.js");
/* harmony import */ var _help__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./help */ "../packages/mainmenu/lib/help.js");
/* harmony import */ var _kernel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./kernel */ "../packages/mainmenu/lib/kernel.js");
/* harmony import */ var _run__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./run */ "../packages/mainmenu/lib/run.js");
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./settings */ "../packages/mainmenu/lib/settings.js");
/* harmony import */ var _view__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./view */ "../packages/mainmenu/lib/view.js");
/* harmony import */ var _tabs__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs */ "../packages/mainmenu/lib/tabs.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tokens */ "../packages/mainmenu/lib/tokens.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_10__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mainmenu
 */










/**
 * @deprecated since version 3.1
 */



/***/ }),

/***/ "../packages/mainmenu/lib/kernel.js":
/*!******************************************!*\
  !*** ../packages/mainmenu/lib/kernel.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelMenu": () => (/* binding */ KernelMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Kernel menu for the application.
 */
class KernelMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the kernel menu.
     */
    constructor(options) {
        super(options);
        this.kernelUsers = new Set();
    }
    /**
     * Dispose of the resources held by the kernel menu.
     */
    dispose() {
        this.kernelUsers.clear();
        super.dispose();
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/mainmenu.js":
/*!********************************************!*\
  !*** ../packages/mainmenu/lib/mainmenu.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MainMenu": () => (/* binding */ MainMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _edit__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./edit */ "../packages/mainmenu/lib/edit.js");
/* harmony import */ var _file__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./file */ "../packages/mainmenu/lib/file.js");
/* harmony import */ var _help__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./help */ "../packages/mainmenu/lib/help.js");
/* harmony import */ var _kernel__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./kernel */ "../packages/mainmenu/lib/kernel.js");
/* harmony import */ var _run__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./run */ "../packages/mainmenu/lib/run.js");
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./settings */ "../packages/mainmenu/lib/settings.js");
/* harmony import */ var _tabs__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs */ "../packages/mainmenu/lib/tabs.js");
/* harmony import */ var _view__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./view */ "../packages/mainmenu/lib/view.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.











/**
 * The main menu class.  It is intended to be used as a singleton.
 */
class MainMenu extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.MenuBar {
    /**
     * Construct the main menu bar.
     */
    constructor(commands) {
        super();
        this._items = [];
        this._commands = commands;
    }
    /**
     * The application "Edit" menu.
     */
    get editMenu() {
        if (!this._editMenu) {
            this._editMenu = new _edit__WEBPACK_IMPORTED_MODULE_3__.EditMenu({
                commands: this._commands,
                rank: 2,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._editMenu;
    }
    /**
     * The application "File" menu.
     */
    get fileMenu() {
        if (!this._fileMenu) {
            this._fileMenu = new _file__WEBPACK_IMPORTED_MODULE_4__.FileMenu({
                commands: this._commands,
                rank: 1,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._fileMenu;
    }
    /**
     * The application "Help" menu.
     */
    get helpMenu() {
        if (!this._helpMenu) {
            this._helpMenu = new _help__WEBPACK_IMPORTED_MODULE_5__.HelpMenu({
                commands: this._commands,
                rank: 1000,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._helpMenu;
    }
    /**
     * The application "Kernel" menu.
     */
    get kernelMenu() {
        if (!this._kernelMenu) {
            this._kernelMenu = new _kernel__WEBPACK_IMPORTED_MODULE_6__.KernelMenu({
                commands: this._commands,
                rank: 5,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._kernelMenu;
    }
    /**
     * The application "Run" menu.
     */
    get runMenu() {
        if (!this._runMenu) {
            this._runMenu = new _run__WEBPACK_IMPORTED_MODULE_7__.RunMenu({
                commands: this._commands,
                rank: 4,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._runMenu;
    }
    /**
     * The application "Settings" menu.
     */
    get settingsMenu() {
        if (!this._settingsMenu) {
            this._settingsMenu = new _settings__WEBPACK_IMPORTED_MODULE_8__.SettingsMenu({
                commands: this._commands,
                rank: 999,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._settingsMenu;
    }
    /**
     * The application "View" menu.
     */
    get viewMenu() {
        if (!this._viewMenu) {
            this._viewMenu = new _view__WEBPACK_IMPORTED_MODULE_9__.ViewMenu({
                commands: this._commands,
                rank: 3,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._viewMenu;
    }
    /**
     * The application "Tabs" menu.
     */
    get tabsMenu() {
        if (!this._tabsMenu) {
            this._tabsMenu = new _tabs__WEBPACK_IMPORTED_MODULE_10__.TabsMenu({
                commands: this._commands,
                rank: 500,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._tabsMenu;
    }
    /**
     * Add a new menu to the main menu bar.
     */
    addMenu(menu, options = {}) {
        if (_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.firstIndexOf(this.menus, menu) > -1) {
            return;
        }
        // override default renderer with svg-supporting renderer
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.overrideDefaultRenderer(menu);
        const rank = 'rank' in options
            ? options.rank
            : 'rank' in menu
                ? menu.rank
                : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.IRankedMenu.DEFAULT_RANK;
        const rankItem = { menu, rank };
        const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.upperBound(this._items, rankItem, Private.itemCmp);
        // Upon disposal, remove the menu and its rank reference.
        menu.disposed.connect(this._onMenuDisposed, this);
        _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.insert(this._items, index, rankItem);
        /**
         * Create a new menu.
         */
        this.insertMenu(index, menu);
        // Link the menu to the API - backward compatibility when switching to menu description in settings
        switch (menu.id) {
            case 'jp-mainmenu-file':
                if (!this._fileMenu && menu instanceof _file__WEBPACK_IMPORTED_MODULE_4__.FileMenu) {
                    this._fileMenu = menu;
                }
                break;
            case 'jp-mainmenu-edit':
                if (!this._editMenu && menu instanceof _edit__WEBPACK_IMPORTED_MODULE_3__.EditMenu) {
                    this._editMenu = menu;
                }
                break;
            case 'jp-mainmenu-view':
                if (!this._viewMenu && menu instanceof _view__WEBPACK_IMPORTED_MODULE_9__.ViewMenu) {
                    this._viewMenu = menu;
                }
                break;
            case 'jp-mainmenu-run':
                if (!this._runMenu && menu instanceof _run__WEBPACK_IMPORTED_MODULE_7__.RunMenu) {
                    this._runMenu = menu;
                }
                break;
            case 'jp-mainmenu-kernel':
                if (!this._kernelMenu && menu instanceof _kernel__WEBPACK_IMPORTED_MODULE_6__.KernelMenu) {
                    this._kernelMenu = menu;
                }
                break;
            case 'jp-mainmenu-tabs':
                if (!this._tabsMenu && menu instanceof _tabs__WEBPACK_IMPORTED_MODULE_10__.TabsMenu) {
                    this._tabsMenu = menu;
                }
                break;
            case 'jp-mainmenu-settings':
                if (!this._settingsMenu && menu instanceof _settings__WEBPACK_IMPORTED_MODULE_8__.SettingsMenu) {
                    this._settingsMenu = menu;
                }
                break;
            case 'jp-mainmenu-help':
                if (!this._helpMenu && menu instanceof _help__WEBPACK_IMPORTED_MODULE_5__.HelpMenu) {
                    this._helpMenu = menu;
                }
                break;
        }
    }
    /**
     * Dispose of the resources held by the menu bar.
     */
    dispose() {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        (_a = this._editMenu) === null || _a === void 0 ? void 0 : _a.dispose();
        (_b = this._fileMenu) === null || _b === void 0 ? void 0 : _b.dispose();
        (_c = this._helpMenu) === null || _c === void 0 ? void 0 : _c.dispose();
        (_d = this._kernelMenu) === null || _d === void 0 ? void 0 : _d.dispose();
        (_e = this._runMenu) === null || _e === void 0 ? void 0 : _e.dispose();
        (_f = this._settingsMenu) === null || _f === void 0 ? void 0 : _f.dispose();
        (_g = this._viewMenu) === null || _g === void 0 ? void 0 : _g.dispose();
        (_h = this._tabsMenu) === null || _h === void 0 ? void 0 : _h.dispose();
        super.dispose();
    }
    /**
     * Generate the menu.
     *
     * @param commands The command registry
     * @param options The main menu options.
     * @param trans - The application language translator.
     */
    static generateMenu(commands, options, trans) {
        let menu;
        const { id, label, rank } = options;
        switch (id) {
            case 'jp-mainmenu-file':
                menu = new _file__WEBPACK_IMPORTED_MODULE_4__.FileMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-edit':
                menu = new _edit__WEBPACK_IMPORTED_MODULE_3__.EditMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-view':
                menu = new _view__WEBPACK_IMPORTED_MODULE_9__.ViewMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-run':
                menu = new _run__WEBPACK_IMPORTED_MODULE_7__.RunMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-kernel':
                menu = new _kernel__WEBPACK_IMPORTED_MODULE_6__.KernelMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-tabs':
                menu = new _tabs__WEBPACK_IMPORTED_MODULE_10__.TabsMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-settings':
                menu = new _settings__WEBPACK_IMPORTED_MODULE_8__.SettingsMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-help':
                menu = new _help__WEBPACK_IMPORTED_MODULE_5__.HelpMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            default:
                menu = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
        }
        if (label) {
            menu.title.label = trans._p('menu', label);
        }
        return menu;
    }
    /**
     * Handle the disposal of a menu.
     */
    _onMenuDisposed(menu) {
        this.removeMenu(menu);
        const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.findFirstIndex(this._items, item => item.menu === menu);
        if (index !== -1) {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.removeAt(this._items, index);
        }
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * A comparator function for menu rank items.
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/mainmenu/lib/run.js":
/*!***************************************!*\
  !*** ../packages/mainmenu/lib/run.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunMenu": () => (/* binding */ RunMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Run menu for the application.
 */
class RunMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the run menu.
     */
    constructor(options) {
        super(options);
        this.codeRunners = new Set();
    }
    /**
     * Dispose of the resources held by the run menu.
     */
    dispose() {
        this.codeRunners.clear();
        super.dispose();
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/settings.js":
/*!********************************************!*\
  !*** ../packages/mainmenu/lib/settings.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SettingsMenu": () => (/* binding */ SettingsMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Settings menu for the application.
 */
class SettingsMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the settings menu.
     */
    constructor(options) {
        super(options);
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/tabs.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/tabs.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TabsMenu": () => (/* binding */ TabsMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Tabs menu for the application.
 */
class TabsMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the tabs menu.
     */
    constructor(options) {
        super(options);
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/tokens.js":
/*!******************************************!*\
  !*** ../packages/mainmenu/lib/tokens.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMainMenu": () => (/* binding */ IMainMenu)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The main menu token.
 */
const IMainMenu = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/mainmenu:IMainMenu');


/***/ }),

/***/ "../packages/mainmenu/lib/view.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/view.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ViewMenu": () => (/* binding */ ViewMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible View menu for the application.
 */
class ViewMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the view menu.
     */
    constructor(options) {
        super(options);
        this.editorViewers = new Set();
    }
    /**
     * Dispose of the resources held by the view menu.
     */
    dispose() {
        this.editorViewers.clear();
        super.dispose();
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUvc3JjL2VkaXQudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21haW5tZW51L3NyYy9maWxlLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYWlubWVudS9zcmMvaGVscC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYWlubWVudS9zcmMva2VybmVsLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYWlubWVudS9zcmMvbWFpbm1lbnUudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21haW5tZW51L3NyYy9ydW4udHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21haW5tZW51L3NyYy9zZXR0aW5ncy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUvc3JjL3RhYnMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21haW5tZW51L3NyYy90b2tlbnMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21haW5tZW51L3NyYy92aWV3LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFB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O1FBQ2YsSUFBSSxDQUFDLGFBQWEsR0FBRyxJQUFJLEdBQUcsRUFBbUMsQ0FBQztJQUNsRSxDQUFDO0lBT0Q7O09BRUc7SUFDSCxPQUFPO1FBQ0wsSUFBSSxDQUFDLGFBQWEsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUMzQixLQUFLLENBQUMsT0FBTyxFQUFFLENBQUM7SUFDbEIsQ0FBQztDQUNGIiwiZmlsZSI6InBhY2thZ2VzX21haW5tZW51X2xpYl9pbmRleF9qcy5kMGUzODI4YWI2Yzc0NzM0MTlkYi5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVJhbmtlZE1lbnUsIFJhbmtlZE1lbnUgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBJTWVudUV4dGVuZGVyIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3IgYW4gRWRpdCBtZW51LlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElFZGl0TWVudSBleHRlbmRzIElSYW5rZWRNZW51IHtcbiAgLyoqXG4gICAqIEEgc2V0IHN0b3JpbmcgSVVuZG9lcnMgZm9yIHRoZSBFZGl0IG1lbnUuXG4gICAqL1xuICByZWFkb25seSB1bmRvZXJzOiBTZXQ8SUVkaXRNZW51LklVbmRvZXI8V2lkZ2V0Pj47XG5cbiAgLyoqXG4gICAqIEEgc2V0IHN0b3JpbmcgSUNsZWFyZXJzIGZvciB0aGUgRWRpdCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgY2xlYXJlcnM6IFNldDxJRWRpdE1lbnUuSUNsZWFyZXI8V2lkZ2V0Pj47XG5cbiAgLyoqXG4gICAqIEEgc2V0IHN0b3JpbmcgSUdvVG9MaW5lcnMgZm9yIHRoZSBFZGl0IG1lbnUuXG4gICAqL1xuICByZWFkb25seSBnb1RvTGluZXJzOiBTZXQ8SUVkaXRNZW51LklHb1RvTGluZXI8V2lkZ2V0Pj47XG59XG5cbi8qKlxuICogQW4gZXh0ZW5zaWJsZSBFZGl0IG1lbnUgZm9yIHRoZSBhcHBsaWNhdGlvbi5cbiAqL1xuZXhwb3J0IGNsYXNzIEVkaXRNZW51IGV4dGVuZHMgUmFua2VkTWVudSBpbXBsZW1lbnRzIElFZGl0TWVudSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgdGhlIGVkaXQgbWVudS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IElSYW5rZWRNZW51LklPcHRpb25zKSB7XG4gICAgc3VwZXIob3B0aW9ucyk7XG5cbiAgICB0aGlzLnVuZG9lcnMgPSBuZXcgU2V0PElFZGl0TWVudS5JVW5kb2VyPFdpZGdldD4+KCk7XG5cbiAgICB0aGlzLmNsZWFyZXJzID0gbmV3IFNldDxJRWRpdE1lbnUuSUNsZWFyZXI8V2lkZ2V0Pj4oKTtcblxuICAgIHRoaXMuZ29Ub0xpbmVycyA9IG5ldyBTZXQ8SUVkaXRNZW51LklHb1RvTGluZXI8V2lkZ2V0Pj4oKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNldCBzdG9yaW5nIElVbmRvZXJzIGZvciB0aGUgRWRpdCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgdW5kb2VyczogU2V0PElFZGl0TWVudS5JVW5kb2VyPFdpZGdldD4+O1xuXG4gIC8qKlxuICAgKiBBIHNldCBzdG9yaW5nIElDbGVhcmVycyBmb3IgdGhlIEVkaXQgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGNsZWFyZXJzOiBTZXQ8SUVkaXRNZW51LklDbGVhcmVyPFdpZGdldD4+O1xuXG4gIC8qKlxuICAgKiBBIHNldCBzdG9yaW5nIElHb1RvTGluZXJzIGZvciB0aGUgRWRpdCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgZ29Ub0xpbmVyczogU2V0PElFZGl0TWVudS5JR29Ub0xpbmVyPFdpZGdldD4+O1xuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgZWRpdCBtZW51LlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICB0aGlzLnVuZG9lcnMuY2xlYXIoKTtcbiAgICB0aGlzLmNsZWFyZXJzLmNsZWFyKCk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG59XG5cbi8qKlxuICogTmFtZXNwYWNlIGZvciBJRWRpdE1lbnVcbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJRWRpdE1lbnUge1xuICAvKipcbiAgICogSW50ZXJmYWNlIGZvciBhbiBhY3Rpdml0eSB0aGF0IHVzZXMgVW5kby9SZWRvLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJVW5kb2VyPFQgZXh0ZW5kcyBXaWRnZXQ+IGV4dGVuZHMgSU1lbnVFeHRlbmRlcjxUPiB7XG4gICAgLyoqXG4gICAgICogRXhlY3V0ZSBhbiB1bmRvIGNvbW1hbmQgZm9yIHRoZSBhY3Rpdml0eS5cbiAgICAgKi9cbiAgICB1bmRvPzogKHdpZGdldDogVCkgPT4gdm9pZDtcblxuICAgIC8qKlxuICAgICAqIEV4ZWN1dGUgYSByZWRvIGNvbW1hbmQgZm9yIHRoZSBhY3Rpdml0eS5cbiAgICAgKi9cbiAgICByZWRvPzogKHdpZGdldDogVCkgPT4gdm9pZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbnRlcmZhY2UgZm9yIGFuIGFjdGl2aXR5IHRoYXQgd2FudHMgdG8gcmVnaXN0ZXIgYSAnQ2xlYXIuLi4nIG1lbnUgaXRlbVxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ2xlYXJlcjxUIGV4dGVuZHMgV2lkZ2V0PiBleHRlbmRzIElNZW51RXh0ZW5kZXI8VD4ge1xuICAgIC8qKlxuICAgICAqIEEgZnVuY3Rpb24gdG8gY3JlYXRlIHRoZSBsYWJlbCBmb3IgdGhlIGBjbGVhckN1cnJlbnRgYWN0aW9uLlxuICAgICAqXG4gICAgICogVGhpcyBmdW5jdGlvbiByZWNlaXZlcyB0aGUgbnVtYmVyIG9mIGl0ZW1zIGBuYCB0byBiZSBhYmxlIHRvIHByb3ZpZGVkXG4gICAgICogY29ycmVjdCBwbHVyYWxpemVkIGZvcm1zIG9mIHRyYW5zbGF0aW9ucy5cbiAgICAgKi9cbiAgICBjbGVhckN1cnJlbnRMYWJlbD86IChuOiBudW1iZXIpID0+IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEEgZnVuY3Rpb24gdG8gY3JlYXRlIHRoZSBsYWJlbCBmb3IgdGhlIGBjbGVhckFsbGBhY3Rpb24uXG4gICAgICpcbiAgICAgKiBUaGlzIGZ1bmN0aW9uIHJlY2VpdmVzIHRoZSBudW1iZXIgb2YgaXRlbXMgYG5gIHRvIGJlIGFibGUgdG8gcHJvdmlkZWRcbiAgICAgKiBjb3JyZWN0IHBsdXJhbGl6ZWQgZm9ybXMgb2YgdHJhbnNsYXRpb25zLlxuICAgICAqL1xuICAgIGNsZWFyQWxsTGFiZWw/OiAobjogbnVtYmVyKSA9PiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIGNsZWFyIHRoZSBjdXJyZW50bHkgcG9ydGlvbiBvZiBhY3Rpdml0eS5cbiAgICAgKi9cbiAgICBjbGVhckN1cnJlbnQ/OiAod2lkZ2V0OiBUKSA9PiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0byBjbGVhciBhbGwgb2YgYW4gYWN0aXZpdHkuXG4gICAgICovXG4gICAgY2xlYXJBbGw/OiAod2lkZ2V0OiBUKSA9PiB2b2lkO1xuICB9XG5cbiAgLyoqXG4gICAqIEludGVyZmFjZSBmb3IgYW4gYWN0aXZpdHkgdGhhdCB1c2VzIEdvIHRvIExpbmUuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElHb1RvTGluZXI8VCBleHRlbmRzIFdpZGdldD4gZXh0ZW5kcyBJTWVudUV4dGVuZGVyPFQ+IHtcbiAgICAvKipcbiAgICAgKiBFeGVjdXRlIGEgZ28gdG8gbGluZSBjb21tYW5kIGZvciB0aGUgYWN0aXZpdHkuXG4gICAgICovXG4gICAgZ29Ub0xpbmU/OiAod2lkZ2V0OiBUKSA9PiB2b2lkO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElSYW5rZWRNZW51LCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBmaW5kIH0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IElNZW51RXh0ZW5kZXIgfSBmcm9tICcuL3Rva2Vucyc7XG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBhIEZpbGUgbWVudS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJRmlsZU1lbnUgZXh0ZW5kcyBJUmFua2VkTWVudSB7XG4gIC8qKlxuICAgKiBPcHRpb24gdG8gYWRkIGEgYFF1aXRgIGVudHJ5IGluIHRoZSBGaWxlIG1lbnVcbiAgICovXG4gIHF1aXRFbnRyeTogYm9vbGVhbjtcblxuICAvKipcbiAgICogQSBzdWJtZW51IGZvciBjcmVhdGluZyBuZXcgZmlsZXMvbGF1bmNoaW5nIG5ldyBhY3Rpdml0aWVzLlxuICAgKi9cbiAgcmVhZG9ubHkgbmV3TWVudTogSVJhbmtlZE1lbnU7XG5cbiAgLyoqXG4gICAqIFRoZSBjbG9zZSBhbmQgY2xlYW51cCBleHRlbnNpb24gcG9pbnQuXG4gICAqL1xuICByZWFkb25seSBjbG9zZUFuZENsZWFuZXJzOiBTZXQ8SUZpbGVNZW51LklDbG9zZUFuZENsZWFuZXI8V2lkZ2V0Pj47XG5cbiAgLyoqXG4gICAqIEEgc2V0IHN0b3JpbmcgSUNvbnNvbGVDcmVhdG9ycyBmb3IgdGhlIEZpbGUgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGNvbnNvbGVDcmVhdG9yczogU2V0PElGaWxlTWVudS5JQ29uc29sZUNyZWF0b3I8V2lkZ2V0Pj47XG59XG5cbi8qKlxuICogQW4gZXh0ZW5zaWJsZSBGaWxlTWVudSBmb3IgdGhlIGFwcGxpY2F0aW9uLlxuICovXG5leHBvcnQgY2xhc3MgRmlsZU1lbnUgZXh0ZW5kcyBSYW5rZWRNZW51IGltcGxlbWVudHMgSUZpbGVNZW51IHtcbiAgY29uc3RydWN0b3Iob3B0aW9uczogSVJhbmtlZE1lbnUuSU9wdGlvbnMpIHtcbiAgICBzdXBlcihvcHRpb25zKTtcbiAgICB0aGlzLnF1aXRFbnRyeSA9IGZhbHNlO1xuXG4gICAgLy8gQ3JlYXRlIHRoZSBcIk5ld1wiIHN1Ym1lbnUuXG4gICAgdGhpcy5jbG9zZUFuZENsZWFuZXJzID0gbmV3IFNldDxJRmlsZU1lbnUuSUNsb3NlQW5kQ2xlYW5lcjxXaWRnZXQ+PigpO1xuICAgIHRoaXMuY29uc29sZUNyZWF0b3JzID0gbmV3IFNldDxJRmlsZU1lbnUuSUNvbnNvbGVDcmVhdG9yPFdpZGdldD4+KCk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIE5ldyBzdWJtZW51LlxuICAgKi9cbiAgZ2V0IG5ld01lbnUoKTogUmFua2VkTWVudSB7XG4gICAgaWYgKCF0aGlzLl9uZXdNZW51KSB7XG4gICAgICB0aGlzLl9uZXdNZW51ID1cbiAgICAgICAgKGZpbmQodGhpcy5pdGVtcywgbWVudSA9PiBtZW51LnN1Ym1lbnU/LmlkID09PSAnanAtbWFpbm1lbnUtZmlsZS1uZXcnKVxuICAgICAgICAgID8uc3VibWVudSBhcyBSYW5rZWRNZW51KSA/P1xuICAgICAgICBuZXcgUmFua2VkTWVudSh7XG4gICAgICAgICAgY29tbWFuZHM6IHRoaXMuY29tbWFuZHNcbiAgICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLl9uZXdNZW51O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjbG9zZSBhbmQgY2xlYW51cCBleHRlbnNpb24gcG9pbnQuXG4gICAqL1xuICByZWFkb25seSBjbG9zZUFuZENsZWFuZXJzOiBTZXQ8SUZpbGVNZW51LklDbG9zZUFuZENsZWFuZXI8V2lkZ2V0Pj47XG5cbiAgLyoqXG4gICAqIEEgc2V0IHN0b3JpbmcgSUNvbnNvbGVDcmVhdG9ycyBmb3IgdGhlIEtlcm5lbCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgY29uc29sZUNyZWF0b3JzOiBTZXQ8SUZpbGVNZW51LklDb25zb2xlQ3JlYXRvcjxXaWRnZXQ+PjtcblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIGZpbGUgbWVudS5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgdGhpcy5fbmV3TWVudT8uZGlzcG9zZSgpO1xuICAgIHRoaXMuY29uc29sZUNyZWF0b3JzLmNsZWFyKCk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIE9wdGlvbiB0byBhZGQgYSBgUXVpdGAgZW50cnkgaW4gRmlsZSBtZW51XG4gICAqL1xuICBwdWJsaWMgcXVpdEVudHJ5OiBib29sZWFuO1xuXG4gIHByaXZhdGUgX25ld01lbnU6IFJhbmtlZE1lbnU7XG59XG5cbi8qKlxuICogTmFtZXNwYWNlIGZvciBJRmlsZU1lbnVcbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJRmlsZU1lbnUge1xuICAvKipcbiAgICogSW50ZXJmYWNlIGZvciBhbiBhY3Rpdml0eSB0aGF0IGhhcyBzb21lIGNsZWFudXAgYWN0aW9uIGFzc29jaWF0ZWRcbiAgICogd2l0aCBpdCBpbiBhZGRpdGlvbiB0byBtZXJlbHkgY2xvc2luZyBpdHMgd2lkZ2V0IGluIHRoZSBtYWluIGFyZWEuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDbG9zZUFuZENsZWFuZXI8VCBleHRlbmRzIFdpZGdldD4gZXh0ZW5kcyBJTWVudUV4dGVuZGVyPFQ+IHtcbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIGNyZWF0ZSB0aGUgbGFiZWwgZm9yIHRoZSBgY2xvc2VBbmRDbGVhbnVwYGFjdGlvbi5cbiAgICAgKlxuICAgICAqIFRoaXMgZnVuY3Rpb24gcmVjZWl2ZXMgdGhlIG51bWJlciBvZiBpdGVtcyBgbmAgdG8gYmUgYWJsZSB0byBwcm92aWRlZFxuICAgICAqIGNvcnJlY3QgcGx1cmFsaXplZCBmb3JtcyBvZiB0cmFuc2xhdGlvbnMuXG4gICAgICovXG4gICAgY2xvc2VBbmRDbGVhbnVwTGFiZWw/OiAobjogbnVtYmVyKSA9PiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIHBlcmZvcm0gdGhlIGNsb3NlIGFuZCBjbGVhbnVwIGFjdGlvbi5cbiAgICAgKi9cbiAgICBjbG9zZUFuZENsZWFudXA6ICh3aWRnZXQ6IFQpID0+IFByb21pc2U8dm9pZD47XG4gIH1cblxuICAvKipcbiAgICogSW50ZXJmYWNlIGZvciBhIGNvbW1hbmQgdG8gY3JlYXRlIGEgY29uc29sZSBmb3IgYW4gYWN0aXZpdHkuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDb25zb2xlQ3JlYXRvcjxUIGV4dGVuZHMgV2lkZ2V0PiBleHRlbmRzIElNZW51RXh0ZW5kZXI8VD4ge1xuICAgIC8qKlxuICAgICAqIEEgZnVuY3Rpb24gdG8gY3JlYXRlIHRoZSBsYWJlbCBmb3IgdGhlIGBjcmVhdGVDb25zb2xlYGFjdGlvbi5cbiAgICAgKlxuICAgICAqIFRoaXMgZnVuY3Rpb24gcmVjZWl2ZXMgdGhlIG51bWJlciBvZiBpdGVtcyBgbmAgdG8gYmUgYWJsZSB0byBwcm92aWRlZFxuICAgICAqIGNvcnJlY3QgcGx1cmFsaXplZCBmb3JtcyBvZiB0cmFuc2xhdGlvbnMuXG4gICAgICovXG4gICAgY3JlYXRlQ29uc29sZUxhYmVsPzogKG46IG51bWJlcikgPT4gc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGZ1bmN0aW9uIHRvIGNyZWF0ZSB0aGUgY29uc29sZS5cbiAgICAgKi9cbiAgICBjcmVhdGVDb25zb2xlOiAod2lkZ2V0OiBUKSA9PiBQcm9taXNlPHZvaWQ+O1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IEtlcm5lbCB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElSYW5rZWRNZW51LCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgSU1lbnVFeHRlbmRlciB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBBbiBpbnRlcmZhY2UgZm9yIGEgSGVscCBtZW51LlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElIZWxwTWVudSBleHRlbmRzIElSYW5rZWRNZW51IHtcbiAgLyoqXG4gICAqIEEgc2V0IG9mIGtlcm5lbCB1c2VycyBmb3IgdGhlIGhlbHAgbWVudS5cbiAgICogVGhpcyBpcyB1c2VkIHRvIHBvcHVsYXRlIGFkZGl0aW9uYWwgaGVscFxuICAgKiBsaW5rcyBwcm92aWRlZCBieSB0aGUga2VybmVsIG9mIGEgd2lkZ2V0LlxuICAgKi9cbiAgcmVhZG9ubHkga2VybmVsVXNlcnM6IFNldDxJSGVscE1lbnUuSUtlcm5lbFVzZXI8V2lkZ2V0Pj47XG59XG5cbi8qKlxuICogQW4gZXh0ZW5zaWJsZSBIZWxwIG1lbnUgZm9yIHRoZSBhcHBsaWNhdGlvbi5cbiAqL1xuZXhwb3J0IGNsYXNzIEhlbHBNZW51IGV4dGVuZHMgUmFua2VkTWVudSBpbXBsZW1lbnRzIElIZWxwTWVudSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgdGhlIGhlbHAgbWVudS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IElSYW5rZWRNZW51LklPcHRpb25zKSB7XG4gICAgc3VwZXIob3B0aW9ucyk7XG4gICAgdGhpcy5rZXJuZWxVc2VycyA9IG5ldyBTZXQ8SUhlbHBNZW51LklLZXJuZWxVc2VyPFdpZGdldD4+KCk7XG4gIH1cblxuICAvKipcbiAgICogQSBzZXQgb2Yga2VybmVsIHVzZXJzIGZvciB0aGUgaGVscCBtZW51LlxuICAgKiBUaGlzIGlzIHVzZWQgdG8gcG9wdWxhdGUgYWRkaXRpb25hbCBoZWxwXG4gICAqIGxpbmtzIHByb3ZpZGVkIGJ5IHRoZSBrZXJuZWwgb2YgYSB3aWRnZXQuXG4gICAqL1xuICByZWFkb25seSBrZXJuZWxVc2VyczogU2V0PElIZWxwTWVudS5JS2VybmVsVXNlcjxXaWRnZXQ+Pjtcbn1cblxuLyoqXG4gKiBOYW1lc3BhY2UgZm9yIElIZWxwTWVudVxuICovXG5leHBvcnQgbmFtZXNwYWNlIElIZWxwTWVudSB7XG4gIC8qKlxuICAgKiBJbnRlcmZhY2UgZm9yIGEgS2VybmVsIHVzZXIgdG8gcmVnaXN0ZXIgaXRzZWxmXG4gICAqIHdpdGggdGhlIElIZWxwTWVudSdzIHNlbWFudGljIGV4dGVuc2lvbiBwb2ludHMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElLZXJuZWxVc2VyPFQgZXh0ZW5kcyBXaWRnZXQ+IGV4dGVuZHMgSU1lbnVFeHRlbmRlcjxUPiB7XG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0byBnZXQgdGhlIGtlcm5lbCBmb3IgYSB3aWRnZXQuXG4gICAgICovXG4gICAgZ2V0S2VybmVsOiAod2lkZ2V0OiBUKSA9PiBLZXJuZWwuSUtlcm5lbENvbm5lY3Rpb24gfCBudWxsO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBtYWlubWVudVxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vbWFpbm1lbnUnO1xuZXhwb3J0ICogZnJvbSAnLi9lZGl0JztcbmV4cG9ydCAqIGZyb20gJy4vZmlsZSc7XG5leHBvcnQgKiBmcm9tICcuL2hlbHAnO1xuZXhwb3J0ICogZnJvbSAnLi9rZXJuZWwnO1xuZXhwb3J0ICogZnJvbSAnLi9ydW4nO1xuZXhwb3J0ICogZnJvbSAnLi9zZXR0aW5ncyc7XG5leHBvcnQgKiBmcm9tICcuL3ZpZXcnO1xuZXhwb3J0ICogZnJvbSAnLi90YWJzJztcbmV4cG9ydCAqIGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBAZGVwcmVjYXRlZCBzaW5jZSB2ZXJzaW9uIDMuMVxuICovXG5leHBvcnQge1xuICBJUmFua2VkTWVudSBhcyBJSnVweXRlckxhYk1lbnUsXG4gIFJhbmtlZE1lbnUgYXMgSnVweXRlckxhYk1lbnVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElSYW5rZWRNZW51LCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgSU1lbnVFeHRlbmRlciB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBBbiBpbnRlcmZhY2UgZm9yIGEgS2VybmVsIG1lbnUuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUtlcm5lbE1lbnUgZXh0ZW5kcyBJUmFua2VkTWVudSB7XG4gIC8qKlxuICAgKiBBIHNldCBzdG9yaW5nIElLZXJuZWxVc2VycyBmb3IgdGhlIEtlcm5lbCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkga2VybmVsVXNlcnM6IFNldDxJS2VybmVsTWVudS5JS2VybmVsVXNlcjxXaWRnZXQ+Pjtcbn1cblxuLyoqXG4gKiBBbiBleHRlbnNpYmxlIEtlcm5lbCBtZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBLZXJuZWxNZW51IGV4dGVuZHMgUmFua2VkTWVudSBpbXBsZW1lbnRzIElLZXJuZWxNZW51IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCB0aGUga2VybmVsIG1lbnUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICAgIHRoaXMua2VybmVsVXNlcnMgPSBuZXcgU2V0PElLZXJuZWxNZW51LklLZXJuZWxVc2VyPFdpZGdldD4+KCk7XG4gIH1cblxuICAvKipcbiAgICogQSBzZXQgc3RvcmluZyBJS2VybmVsVXNlcnMgZm9yIHRoZSBLZXJuZWwgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGtlcm5lbFVzZXJzOiBTZXQ8SUtlcm5lbE1lbnUuSUtlcm5lbFVzZXI8V2lkZ2V0Pj47XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBrZXJuZWwgbWVudS5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgdGhpcy5rZXJuZWxVc2Vycy5jbGVhcigpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxufVxuXG4vKipcbiAqIE5hbWVzcGFjZSBmb3IgSUtlcm5lbE1lbnVcbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJS2VybmVsTWVudSB7XG4gIC8qKlxuICAgKiBJbnRlcmZhY2UgZm9yIGEgS2VybmVsIHVzZXIgdG8gcmVnaXN0ZXIgaXRzZWxmXG4gICAqIHdpdGggdGhlIElLZXJuZWxNZW51J3Mgc2VtYW50aWMgZXh0ZW5zaW9uIHBvaW50cy5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUtlcm5lbFVzZXI8VCBleHRlbmRzIFdpZGdldD4gZXh0ZW5kcyBJTWVudUV4dGVuZGVyPFQ+IHtcbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIGludGVycnVwdCB0aGUga2VybmVsLlxuICAgICAqL1xuICAgIGludGVycnVwdEtlcm5lbD86ICh3aWRnZXQ6IFQpID0+IFByb21pc2U8dm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIHJlY29ubmVjdCB0byB0aGUga2VybmVsXG4gICAgICovXG4gICAgcmVjb25uZWN0VG9LZXJuZWw/OiAod2lkZ2V0OiBUKSA9PiBQcm9taXNlPHZvaWQ+O1xuXG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0byByZXN0YXJ0IHRoZSBrZXJuZWwsIHdoaWNoXG4gICAgICogcmV0dXJucyBhIHByb21pc2Ugb2Ygd2hldGhlciB0aGUga2VybmVsIHdhcyByZXN0YXJ0ZWQuXG4gICAgICovXG4gICAgcmVzdGFydEtlcm5lbD86ICh3aWRnZXQ6IFQpID0+IFByb21pc2U8Ym9vbGVhbj47XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIHJlc3RhcnQgdGhlIGtlcm5lbCBhbmQgY2xlYXIgdGhlIHdpZGdldCwgd2hpY2hcbiAgICAgKiByZXR1cm5zIGEgcHJvbWlzZSBvZiB3aGV0aGVyIHRoZSBrZXJuZWwgd2FzIHJlc3RhcnRlZC5cbiAgICAgKi9cbiAgICByZXN0YXJ0S2VybmVsQW5kQ2xlYXI/OiAod2lkZ2V0OiBUKSA9PiBQcm9taXNlPGJvb2xlYW4+O1xuXG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0byBjaGFuZ2UgdGhlIGtlcm5lbC5cbiAgICAgKi9cbiAgICBjaGFuZ2VLZXJuZWw/OiAod2lkZ2V0OiBUKSA9PiBQcm9taXNlPHZvaWQ+O1xuXG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0byBzaHV0IGRvd24gdGhlIGtlcm5lbC5cbiAgICAgKi9cbiAgICBzaHV0ZG93bktlcm5lbD86ICh3aWRnZXQ6IFQpID0+IFByb21pc2U8dm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIHJldHVybiB0aGUgbGFiZWwgYXNzb2NpYXRlZCB0byB0aGUgYHJlc3RhcnRLZXJuZWxBbmRDbGVhcmAgYWN0aW9uLlxuICAgICAqXG4gICAgICogVGhpcyBmdW5jdGlvbiByZWNlaXZlcyB0aGUgbnVtYmVyIG9mIGl0ZW1zIGBuYCB0byBiZSBhYmxlIHRvIHByb3ZpZGVkXG4gICAgICogY29ycmVjdCBwbHVyYWxpemVkIGZvcm1zIG9mIHRyYW5zbGF0aW9ucy5cbiAgICAgKi9cbiAgICByZXN0YXJ0S2VybmVsQW5kQ2xlYXJMYWJlbD86IChuOiBudW1iZXIpID0+IHN0cmluZztcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUcmFuc2xhdGlvbkJ1bmRsZSB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IElSYW5rZWRNZW51LCBNZW51U3ZnLCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBBcnJheUV4dCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHsgTWVudSwgTWVudUJhciB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBFZGl0TWVudSB9IGZyb20gJy4vZWRpdCc7XG5pbXBvcnQgeyBGaWxlTWVudSB9IGZyb20gJy4vZmlsZSc7XG5pbXBvcnQgeyBIZWxwTWVudSB9IGZyb20gJy4vaGVscCc7XG5pbXBvcnQgeyBLZXJuZWxNZW51IH0gZnJvbSAnLi9rZXJuZWwnO1xuaW1wb3J0IHsgUnVuTWVudSB9IGZyb20gJy4vcnVuJztcbmltcG9ydCB7IFNldHRpbmdzTWVudSB9IGZyb20gJy4vc2V0dGluZ3MnO1xuaW1wb3J0IHsgVGFic01lbnUgfSBmcm9tICcuL3RhYnMnO1xuaW1wb3J0IHsgSU1haW5NZW51IH0gZnJvbSAnLi90b2tlbnMnO1xuaW1wb3J0IHsgVmlld01lbnUgfSBmcm9tICcuL3ZpZXcnO1xuXG4vKipcbiAqIFRoZSBtYWluIG1lbnUgY2xhc3MuICBJdCBpcyBpbnRlbmRlZCB0byBiZSB1c2VkIGFzIGEgc2luZ2xldG9uLlxuICovXG5leHBvcnQgY2xhc3MgTWFpbk1lbnUgZXh0ZW5kcyBNZW51QmFyIGltcGxlbWVudHMgSU1haW5NZW51IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCB0aGUgbWFpbiBtZW51IGJhci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnkpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuX2NvbW1hbmRzID0gY29tbWFuZHM7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiRWRpdFwiIG1lbnUuXG4gICAqL1xuICBnZXQgZWRpdE1lbnUoKTogRWRpdE1lbnUge1xuICAgIGlmICghdGhpcy5fZWRpdE1lbnUpIHtcbiAgICAgIHRoaXMuX2VkaXRNZW51ID0gbmV3IEVkaXRNZW51KHtcbiAgICAgICAgY29tbWFuZHM6IHRoaXMuX2NvbW1hbmRzLFxuICAgICAgICByYW5rOiAyLFxuICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5fZWRpdE1lbnU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiRmlsZVwiIG1lbnUuXG4gICAqL1xuICBnZXQgZmlsZU1lbnUoKTogRmlsZU1lbnUge1xuICAgIGlmICghdGhpcy5fZmlsZU1lbnUpIHtcbiAgICAgIHRoaXMuX2ZpbGVNZW51ID0gbmV3IEZpbGVNZW51KHtcbiAgICAgICAgY29tbWFuZHM6IHRoaXMuX2NvbW1hbmRzLFxuICAgICAgICByYW5rOiAxLFxuICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5fZmlsZU1lbnU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiSGVscFwiIG1lbnUuXG4gICAqL1xuICBnZXQgaGVscE1lbnUoKTogSGVscE1lbnUge1xuICAgIGlmICghdGhpcy5faGVscE1lbnUpIHtcbiAgICAgIHRoaXMuX2hlbHBNZW51ID0gbmV3IEhlbHBNZW51KHtcbiAgICAgICAgY29tbWFuZHM6IHRoaXMuX2NvbW1hbmRzLFxuICAgICAgICByYW5rOiAxMDAwLFxuICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5faGVscE1lbnU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiS2VybmVsXCIgbWVudS5cbiAgICovXG4gIGdldCBrZXJuZWxNZW51KCk6IEtlcm5lbE1lbnUge1xuICAgIGlmICghdGhpcy5fa2VybmVsTWVudSkge1xuICAgICAgdGhpcy5fa2VybmVsTWVudSA9IG5ldyBLZXJuZWxNZW51KHtcbiAgICAgICAgY29tbWFuZHM6IHRoaXMuX2NvbW1hbmRzLFxuICAgICAgICByYW5rOiA1LFxuICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5fa2VybmVsTWVudTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJSdW5cIiBtZW51LlxuICAgKi9cbiAgZ2V0IHJ1bk1lbnUoKTogUnVuTWVudSB7XG4gICAgaWYgKCF0aGlzLl9ydW5NZW51KSB7XG4gICAgICB0aGlzLl9ydW5NZW51ID0gbmV3IFJ1bk1lbnUoe1xuICAgICAgICBjb21tYW5kczogdGhpcy5fY29tbWFuZHMsXG4gICAgICAgIHJhbms6IDQsXG4gICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLl9ydW5NZW51O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBhcHBsaWNhdGlvbiBcIlNldHRpbmdzXCIgbWVudS5cbiAgICovXG4gIGdldCBzZXR0aW5nc01lbnUoKTogU2V0dGluZ3NNZW51IHtcbiAgICBpZiAoIXRoaXMuX3NldHRpbmdzTWVudSkge1xuICAgICAgdGhpcy5fc2V0dGluZ3NNZW51ID0gbmV3IFNldHRpbmdzTWVudSh7XG4gICAgICAgIGNvbW1hbmRzOiB0aGlzLl9jb21tYW5kcyxcbiAgICAgICAgcmFuazogOTk5LFxuICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5fc2V0dGluZ3NNZW51O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBhcHBsaWNhdGlvbiBcIlZpZXdcIiBtZW51LlxuICAgKi9cbiAgZ2V0IHZpZXdNZW51KCk6IFZpZXdNZW51IHtcbiAgICBpZiAoIXRoaXMuX3ZpZXdNZW51KSB7XG4gICAgICB0aGlzLl92aWV3TWVudSA9IG5ldyBWaWV3TWVudSh7XG4gICAgICAgIGNvbW1hbmRzOiB0aGlzLl9jb21tYW5kcyxcbiAgICAgICAgcmFuazogMyxcbiAgICAgICAgcmVuZGVyZXI6IE1lbnVTdmcuZGVmYXVsdFJlbmRlcmVyXG4gICAgICB9KTtcbiAgICB9XG4gICAgcmV0dXJuIHRoaXMuX3ZpZXdNZW51O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBhcHBsaWNhdGlvbiBcIlRhYnNcIiBtZW51LlxuICAgKi9cbiAgZ2V0IHRhYnNNZW51KCk6IFRhYnNNZW51IHtcbiAgICBpZiAoIXRoaXMuX3RhYnNNZW51KSB7XG4gICAgICB0aGlzLl90YWJzTWVudSA9IG5ldyBUYWJzTWVudSh7XG4gICAgICAgIGNvbW1hbmRzOiB0aGlzLl9jb21tYW5kcyxcbiAgICAgICAgcmFuazogNTAwLFxuICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5fdGFic01lbnU7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgbmV3IG1lbnUgdG8gdGhlIG1haW4gbWVudSBiYXIuXG4gICAqL1xuICBhZGRNZW51KG1lbnU6IE1lbnUsIG9wdGlvbnM6IElNYWluTWVudS5JQWRkT3B0aW9ucyA9IHt9KTogdm9pZCB7XG4gICAgaWYgKEFycmF5RXh0LmZpcnN0SW5kZXhPZih0aGlzLm1lbnVzLCBtZW51KSA+IC0xKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gb3ZlcnJpZGUgZGVmYXVsdCByZW5kZXJlciB3aXRoIHN2Zy1zdXBwb3J0aW5nIHJlbmRlcmVyXG4gICAgTWVudVN2Zy5vdmVycmlkZURlZmF1bHRSZW5kZXJlcihtZW51KTtcblxuICAgIGNvbnN0IHJhbmsgPVxuICAgICAgJ3JhbmsnIGluIG9wdGlvbnNcbiAgICAgICAgPyBvcHRpb25zLnJhbmtcbiAgICAgICAgOiAncmFuaycgaW4gbWVudVxuICAgICAgICA/IChtZW51IGFzIGFueSkucmFua1xuICAgICAgICA6IElSYW5rZWRNZW51LkRFRkFVTFRfUkFOSztcbiAgICBjb25zdCByYW5rSXRlbSA9IHsgbWVudSwgcmFuayB9O1xuICAgIGNvbnN0IGluZGV4ID0gQXJyYXlFeHQudXBwZXJCb3VuZCh0aGlzLl9pdGVtcywgcmFua0l0ZW0sIFByaXZhdGUuaXRlbUNtcCk7XG5cbiAgICAvLyBVcG9uIGRpc3Bvc2FsLCByZW1vdmUgdGhlIG1lbnUgYW5kIGl0cyByYW5rIHJlZmVyZW5jZS5cbiAgICBtZW51LmRpc3Bvc2VkLmNvbm5lY3QodGhpcy5fb25NZW51RGlzcG9zZWQsIHRoaXMpO1xuXG4gICAgQXJyYXlFeHQuaW5zZXJ0KHRoaXMuX2l0ZW1zLCBpbmRleCwgcmFua0l0ZW0pO1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyBtZW51LlxuICAgICAqL1xuICAgIHRoaXMuaW5zZXJ0TWVudShpbmRleCwgbWVudSk7XG5cbiAgICAvLyBMaW5rIHRoZSBtZW51IHRvIHRoZSBBUEkgLSBiYWNrd2FyZCBjb21wYXRpYmlsaXR5IHdoZW4gc3dpdGNoaW5nIHRvIG1lbnUgZGVzY3JpcHRpb24gaW4gc2V0dGluZ3NcbiAgICBzd2l0Y2ggKG1lbnUuaWQpIHtcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LWZpbGUnOlxuICAgICAgICBpZiAoIXRoaXMuX2ZpbGVNZW51ICYmIG1lbnUgaW5zdGFuY2VvZiBGaWxlTWVudSkge1xuICAgICAgICAgIHRoaXMuX2ZpbGVNZW51ID0gbWVudTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LWVkaXQnOlxuICAgICAgICBpZiAoIXRoaXMuX2VkaXRNZW51ICYmIG1lbnUgaW5zdGFuY2VvZiBFZGl0TWVudSkge1xuICAgICAgICAgIHRoaXMuX2VkaXRNZW51ID0gbWVudTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LXZpZXcnOlxuICAgICAgICBpZiAoIXRoaXMuX3ZpZXdNZW51ICYmIG1lbnUgaW5zdGFuY2VvZiBWaWV3TWVudSkge1xuICAgICAgICAgIHRoaXMuX3ZpZXdNZW51ID0gbWVudTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LXJ1bic6XG4gICAgICAgIGlmICghdGhpcy5fcnVuTWVudSAmJiBtZW51IGluc3RhbmNlb2YgUnVuTWVudSkge1xuICAgICAgICAgIHRoaXMuX3J1bk1lbnUgPSBtZW51O1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUta2VybmVsJzpcbiAgICAgICAgaWYgKCF0aGlzLl9rZXJuZWxNZW51ICYmIG1lbnUgaW5zdGFuY2VvZiBLZXJuZWxNZW51KSB7XG4gICAgICAgICAgdGhpcy5fa2VybmVsTWVudSA9IG1lbnU7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS10YWJzJzpcbiAgICAgICAgaWYgKCF0aGlzLl90YWJzTWVudSAmJiBtZW51IGluc3RhbmNlb2YgVGFic01lbnUpIHtcbiAgICAgICAgICB0aGlzLl90YWJzTWVudSA9IG1lbnU7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS1zZXR0aW5ncyc6XG4gICAgICAgIGlmICghdGhpcy5fc2V0dGluZ3NNZW51ICYmIG1lbnUgaW5zdGFuY2VvZiBTZXR0aW5nc01lbnUpIHtcbiAgICAgICAgICB0aGlzLl9zZXR0aW5nc01lbnUgPSBtZW51O1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUtaGVscCc6XG4gICAgICAgIGlmICghdGhpcy5faGVscE1lbnUgJiYgbWVudSBpbnN0YW5jZW9mIEhlbHBNZW51KSB7XG4gICAgICAgICAgdGhpcy5faGVscE1lbnUgPSBtZW51O1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgbWVudSBiYXIuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIHRoaXMuX2VkaXRNZW51Py5kaXNwb3NlKCk7XG4gICAgdGhpcy5fZmlsZU1lbnU/LmRpc3Bvc2UoKTtcbiAgICB0aGlzLl9oZWxwTWVudT8uZGlzcG9zZSgpO1xuICAgIHRoaXMuX2tlcm5lbE1lbnU/LmRpc3Bvc2UoKTtcbiAgICB0aGlzLl9ydW5NZW51Py5kaXNwb3NlKCk7XG4gICAgdGhpcy5fc2V0dGluZ3NNZW51Py5kaXNwb3NlKCk7XG4gICAgdGhpcy5fdmlld01lbnU/LmRpc3Bvc2UoKTtcbiAgICB0aGlzLl90YWJzTWVudT8uZGlzcG9zZSgpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZW5lcmF0ZSB0aGUgbWVudS5cbiAgICpcbiAgICogQHBhcmFtIGNvbW1hbmRzIFRoZSBjb21tYW5kIHJlZ2lzdHJ5XG4gICAqIEBwYXJhbSBvcHRpb25zIFRoZSBtYWluIG1lbnUgb3B0aW9ucy5cbiAgICogQHBhcmFtIHRyYW5zIC0gVGhlIGFwcGxpY2F0aW9uIGxhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAqL1xuICBzdGF0aWMgZ2VuZXJhdGVNZW51KFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnksXG4gICAgb3B0aW9uczogSU1haW5NZW51LklNZW51T3B0aW9ucyxcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGVcbiAgKTogUmFua2VkTWVudSB7XG4gICAgbGV0IG1lbnU6IFJhbmtlZE1lbnU7XG4gICAgY29uc3QgeyBpZCwgbGFiZWwsIHJhbmsgfSA9IG9wdGlvbnM7XG4gICAgc3dpdGNoIChpZCkge1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUtZmlsZSc6XG4gICAgICAgIG1lbnUgPSBuZXcgRmlsZU1lbnUoe1xuICAgICAgICAgIGNvbW1hbmRzLFxuICAgICAgICAgIHJhbmssXG4gICAgICAgICAgcmVuZGVyZXI6IE1lbnVTdmcuZGVmYXVsdFJlbmRlcmVyXG4gICAgICAgIH0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LWVkaXQnOlxuICAgICAgICBtZW51ID0gbmV3IEVkaXRNZW51KHtcbiAgICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgICByYW5rLFxuICAgICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgICB9KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS12aWV3JzpcbiAgICAgICAgbWVudSA9IG5ldyBWaWV3TWVudSh7XG4gICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgcmFuayxcbiAgICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgICAgfSk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUtcnVuJzpcbiAgICAgICAgbWVudSA9IG5ldyBSdW5NZW51KHtcbiAgICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgICByYW5rLFxuICAgICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgICB9KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS1rZXJuZWwnOlxuICAgICAgICBtZW51ID0gbmV3IEtlcm5lbE1lbnUoe1xuICAgICAgICAgIGNvbW1hbmRzLFxuICAgICAgICAgIHJhbmssXG4gICAgICAgICAgcmVuZGVyZXI6IE1lbnVTdmcuZGVmYXVsdFJlbmRlcmVyXG4gICAgICAgIH0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LXRhYnMnOlxuICAgICAgICBtZW51ID0gbmV3IFRhYnNNZW51KHtcbiAgICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgICByYW5rLFxuICAgICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgICB9KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS1zZXR0aW5ncyc6XG4gICAgICAgIG1lbnUgPSBuZXcgU2V0dGluZ3NNZW51KHtcbiAgICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgICByYW5rLFxuICAgICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgICB9KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS1oZWxwJzpcbiAgICAgICAgbWVudSA9IG5ldyBIZWxwTWVudSh7XG4gICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgcmFuayxcbiAgICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgICAgfSk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgbWVudSA9IG5ldyBSYW5rZWRNZW51KHtcbiAgICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgICByYW5rLFxuICAgICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBpZiAobGFiZWwpIHtcbiAgICAgIG1lbnUudGl0bGUubGFiZWwgPSB0cmFucy5fcCgnbWVudScsIGxhYmVsKTtcbiAgICB9XG5cbiAgICByZXR1cm4gbWVudTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGRpc3Bvc2FsIG9mIGEgbWVudS5cbiAgICovXG4gIHByaXZhdGUgX29uTWVudURpc3Bvc2VkKG1lbnU6IE1lbnUpOiB2b2lkIHtcbiAgICB0aGlzLnJlbW92ZU1lbnUobWVudSk7XG4gICAgY29uc3QgaW5kZXggPSBBcnJheUV4dC5maW5kRmlyc3RJbmRleChcbiAgICAgIHRoaXMuX2l0ZW1zLFxuICAgICAgaXRlbSA9PiBpdGVtLm1lbnUgPT09IG1lbnVcbiAgICApO1xuICAgIGlmIChpbmRleCAhPT0gLTEpIHtcbiAgICAgIEFycmF5RXh0LnJlbW92ZUF0KHRoaXMuX2l0ZW1zLCBpbmRleCk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeTtcbiAgcHJpdmF0ZSBfaXRlbXM6IFByaXZhdGUuSVJhbmtJdGVtW10gPSBbXTtcbiAgcHJpdmF0ZSBfZWRpdE1lbnU6IEVkaXRNZW51O1xuICBwcml2YXRlIF9maWxlTWVudTogRmlsZU1lbnU7XG4gIHByaXZhdGUgX2hlbHBNZW51OiBIZWxwTWVudTtcbiAgcHJpdmF0ZSBfa2VybmVsTWVudTogS2VybmVsTWVudTtcbiAgcHJpdmF0ZSBfcnVuTWVudTogUnVuTWVudTtcbiAgcHJpdmF0ZSBfc2V0dGluZ3NNZW51OiBTZXR0aW5nc01lbnU7XG4gIHByaXZhdGUgX3ZpZXdNZW51OiBWaWV3TWVudTtcbiAgcHJpdmF0ZSBfdGFic01lbnU6IFRhYnNNZW51O1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIEFuIG9iamVjdCB3aGljaCBob2xkcyBhIG1lbnUgYW5kIGl0cyBzb3J0IHJhbmsuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElSYW5rSXRlbSB7XG4gICAgLyoqXG4gICAgICogVGhlIG1lbnUgZm9yIHRoZSBpdGVtLlxuICAgICAqL1xuICAgIG1lbnU6IE1lbnU7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc29ydCByYW5rIG9mIHRoZSBtZW51LlxuICAgICAqL1xuICAgIHJhbms6IG51bWJlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIGNvbXBhcmF0b3IgZnVuY3Rpb24gZm9yIG1lbnUgcmFuayBpdGVtcy5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBpdGVtQ21wKGZpcnN0OiBJUmFua0l0ZW0sIHNlY29uZDogSVJhbmtJdGVtKTogbnVtYmVyIHtcbiAgICByZXR1cm4gZmlyc3QucmFuayAtIHNlY29uZC5yYW5rO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElSYW5rZWRNZW51LCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgSU1lbnVFeHRlbmRlciB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBBbiBpbnRlcmZhY2UgZm9yIGEgUnVuIG1lbnUuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVJ1bk1lbnUgZXh0ZW5kcyBJUmFua2VkTWVudSB7XG4gIC8qKlxuICAgKiBBIHNldCBzdG9yaW5nIElDb2RlUnVubmVyIGZvciB0aGUgUnVuIG1lbnUuXG4gICAqXG4gICAqICMjIyBOb3Rlc1xuICAgKiBUaGUga2V5IGZvciB0aGUgc2V0IG1heSBiZSB1c2VkIGluIG1lbnUgbGFiZWxzLlxuICAgKi9cbiAgcmVhZG9ubHkgY29kZVJ1bm5lcnM6IFNldDxJUnVuTWVudS5JQ29kZVJ1bm5lcjxXaWRnZXQ+Pjtcbn1cblxuLyoqXG4gKiBBbiBleHRlbnNpYmxlIFJ1biBtZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBSdW5NZW51IGV4dGVuZHMgUmFua2VkTWVudSBpbXBsZW1lbnRzIElSdW5NZW51IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCB0aGUgcnVuIG1lbnUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICAgIHRoaXMuY29kZVJ1bm5lcnMgPSBuZXcgU2V0PElSdW5NZW51LklDb2RlUnVubmVyPFdpZGdldD4+KCk7XG4gIH1cblxuICAvKipcbiAgICogQSBzZXQgc3RvcmluZyBJQ29kZVJ1bm5lciBmb3IgdGhlIFJ1biBtZW51LlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogVGhlIGtleSBmb3IgdGhlIHNldCBtYXkgYmUgdXNlZCBpbiBtZW51IGxhYmVscy5cbiAgICovXG4gIHJlYWRvbmx5IGNvZGVSdW5uZXJzOiBTZXQ8SVJ1bk1lbnUuSUNvZGVSdW5uZXI8V2lkZ2V0Pj47XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBydW4gbWVudS5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgdGhpcy5jb2RlUnVubmVycy5jbGVhcigpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBSdW5NZW51IHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVJ1bk1lbnUge1xuICAvKipcbiAgICogQW4gb2JqZWN0IHRoYXQgcnVucyBjb2RlLCB3aGljaCBtYXkgYmVcbiAgICogcmVnaXN0ZXJlZCB3aXRoIHRoZSBSdW4gbWVudS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUNvZGVSdW5uZXI8VCBleHRlbmRzIFdpZGdldD4gZXh0ZW5kcyBJTWVudUV4dGVuZGVyPFQ+IHtcbiAgICAvKipcbiAgICAgKiBSZXR1cm4gdGhlIGxhYmVsIGFzc29jaWF0ZWQgdG8gdGhlIGBydW5gIGZ1bmN0aW9uLlxuICAgICAqXG4gICAgICogVGhpcyBmdW5jdGlvbiByZWNlaXZlcyB0aGUgbnVtYmVyIG9mIGl0ZW1zIGBuYCB0byBiZSBhYmxlIHRvIHByb3ZpZGVkXG4gICAgICogY29ycmVjdCBwbHVyYWxpemVkIGZvcm1zIG9mIHRyYW5zbGF0aW9ucy5cbiAgICAgKi9cbiAgICBydW5MYWJlbD86IChuOiBudW1iZXIpID0+IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFJldHVybiB0aGUgbGFiZWwgYXNzb2NpYXRlZCB0byB0aGUgYHJ1bkFsbExhYmVsYCBmdW5jdGlvbi5cbiAgICAgKlxuICAgICAqIFRoaXMgZnVuY3Rpb24gcmVjZWl2ZXMgdGhlIG51bWJlciBvZiBpdGVtcyBgbmAgdG8gYmUgYWJsZSB0byBwcm92aWRlZFxuICAgICAqIGNvcnJlY3QgcGx1cmFsaXplZCBmb3JtcyBvZiB0cmFuc2xhdGlvbnMuXG4gICAgICovXG4gICAgcnVuQWxsTGFiZWw/OiAobjogbnVtYmVyKSA9PiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBSZXR1cm4gdGhlIGxhYmVsIGFzc29jaWF0ZWQgdG8gdGhlIGByZXN0YXJ0QW5kUnVuQWxsTGFiZWxgIGZ1bmN0aW9uLlxuICAgICAqXG4gICAgICogVGhpcyBmdW5jdGlvbiByZWNlaXZlcyB0aGUgbnVtYmVyIG9mIGl0ZW1zIGBuYCB0byBiZSBhYmxlIHRvIHByb3ZpZGVkXG4gICAgICogY29ycmVjdCBwbHVyYWxpemVkIGZvcm1zIG9mIHRyYW5zbGF0aW9ucy5cbiAgICAgKi9cbiAgICByZXN0YXJ0QW5kUnVuQWxsTGFiZWw/OiAobjogbnVtYmVyKSA9PiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIHJ1biBhIGNodW5rIG9mIGNvZGUuXG4gICAgICovXG4gICAgcnVuPzogKHdpZGdldDogVCkgPT4gUHJvbWlzZTx2b2lkPjtcblxuICAgIC8qKlxuICAgICAqIEEgZnVuY3Rpb24gdG8gcnVuIHRoZSBlbnRpcmV0eSBvZiB0aGUgY29kZSBob3N0ZWQgYnkgdGhlIHdpZGdldC5cbiAgICAgKi9cbiAgICBydW5BbGw/OiAod2lkZ2V0OiBUKSA9PiBQcm9taXNlPHZvaWQ+O1xuXG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0byByZXN0YXJ0IGFuZCBydW4gYWxsIHRoZSBjb2RlIGhvc3RlZCBieSB0aGUgd2lkZ2V0LCB3aGljaFxuICAgICAqIHJldHVybnMgYSBwcm9taXNlIG9mIHdoZXRoZXIgdGhlIGFjdGlvbiB3YXMgcGVyZm9ybWVkLlxuICAgICAqL1xuICAgIHJlc3RhcnRBbmRSdW5BbGw/OiAod2lkZ2V0OiBUKSA9PiBQcm9taXNlPGJvb2xlYW4+O1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElSYW5rZWRNZW51LCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBhIFNldHRpbmdzIG1lbnUuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVNldHRpbmdzTWVudSBleHRlbmRzIElSYW5rZWRNZW51IHt9XG5cbi8qKlxuICogQW4gZXh0ZW5zaWJsZSBTZXR0aW5ncyBtZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBTZXR0aW5nc01lbnUgZXh0ZW5kcyBSYW5rZWRNZW51IGltcGxlbWVudHMgSVNldHRpbmdzTWVudSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgdGhlIHNldHRpbmdzIG1lbnUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElSYW5rZWRNZW51LCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBhIFRhYnMgbWVudS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJVGFic01lbnUgZXh0ZW5kcyBJUmFua2VkTWVudSB7fVxuXG4vKipcbiAqIEFuIGV4dGVuc2libGUgVGFicyBtZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBUYWJzTWVudSBleHRlbmRzIFJhbmtlZE1lbnUgaW1wbGVtZW50cyBJVGFic01lbnUge1xuICAvKipcbiAgICogQ29uc3RydWN0IHRoZSB0YWJzIG1lbnUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElXaWRnZXRUcmFja2VyLCBNZW51RmFjdG9yeSB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgTWVudSwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IElFZGl0TWVudSB9IGZyb20gJy4vZWRpdCc7XG5pbXBvcnQgeyBJRmlsZU1lbnUgfSBmcm9tICcuL2ZpbGUnO1xuaW1wb3J0IHsgSUhlbHBNZW51IH0gZnJvbSAnLi9oZWxwJztcbmltcG9ydCB7IElLZXJuZWxNZW51IH0gZnJvbSAnLi9rZXJuZWwnO1xuaW1wb3J0IHsgSVJ1bk1lbnUgfSBmcm9tICcuL3J1bic7XG5pbXBvcnQgeyBJU2V0dGluZ3NNZW51IH0gZnJvbSAnLi9zZXR0aW5ncyc7XG5pbXBvcnQgeyBJVGFic01lbnUgfSBmcm9tICcuL3RhYnMnO1xuaW1wb3J0IHsgSVZpZXdNZW51IH0gZnJvbSAnLi92aWV3JztcblxuLyogdHNsaW50OmRpc2FibGUgKi9cbi8qKlxuICogVGhlIG1haW4gbWVudSB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElNYWluTWVudSA9IG5ldyBUb2tlbjxJTWFpbk1lbnU+KCdAanVweXRlcmxhYi9tYWlubWVudTpJTWFpbk1lbnUnKTtcbi8qIHRzbGludDplbmFibGUgKi9cblxuLyoqXG4gKiBBIGJhc2UgaW50ZXJmYWNlIGZvciBhIGNvbnN1bWVyIG9mIG9uZSBvZiB0aGUgbWVudVxuICogc2VtYW50aWMgZXh0ZW5zaW9uIHBvaW50cy4gVGhlIElNZW51RXh0ZW5kZXIgZ2l2ZXNcbiAqIGEgd2lkZ2V0IHRyYWNrZXIgd2hpY2ggaXMgY2hlY2tlZCB3aGVuIHRoZSBtZW51XG4gKiBpcyBkZWNpZGluZyB3aGljaCBJTWVudUV4dGVuZGVyIHRvIGRlbGVnYXRlIHRvIHVwb25cbiAqIHNlbGVjdGlvbiBvZiB0aGUgbWVudSBpdGVtLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElNZW51RXh0ZW5kZXI8VCBleHRlbmRzIFdpZGdldD4ge1xuICAvKipcbiAgICogQSB3aWRnZXQgdHJhY2tlciBmb3IgaWRlbnRpZnlpbmcgdGhlIGFwcHJvcHJpYXRlIGV4dGVuZGVyLlxuICAgKi9cbiAgdHJhY2tlcjogSVdpZGdldFRyYWNrZXI8VD47XG5cbiAgLyoqXG4gICAqIEFuIGFkZGl0aW9uYWwgZnVuY3Rpb24gdGhhdCBkZXRlcm1pbmVzIHdoZXRoZXIgdGhlIGV4dGVuZGVyXG4gICAqIGlzIGVuYWJsZWQuIEJ5IGRlZmF1bHQgaXQgaXMgY29uc2lkZXJlZCBlbmFibGVkIGlmIHRoZSBhcHBsaWNhdGlvblxuICAgKiBhY3RpdmUgd2lkZ2V0IGlzIGNvbnRhaW5lZCBpbiB0aGUgYHRyYWNrZXJgLiBJZiB0aGlzIGlzIGFsc29cbiAgICogcHJvdmlkZWQsIHRoZSBjcml0ZXJpb24gaXMgZXF1aXZhbGVudCB0b1xuICAgKiBgdHJhY2tlci5oYXMod2lkZ2V0KSAmJiBleHRlbmRlci5pc0VuYWJsZWQod2lkZ2V0KWBcbiAgICovXG4gIGlzRW5hYmxlZD86ICh3aWRnZXQ6IFQpID0+IGJvb2xlYW47XG59XG5cbi8qKlxuICogVGhlIG1haW4gbWVudSBpbnRlcmZhY2UuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU1haW5NZW51IHtcbiAgLyoqXG4gICAqIEFkZCBhIG5ldyBtZW51IHRvIHRoZSBtYWluIG1lbnUgYmFyLlxuICAgKi9cbiAgYWRkTWVudShtZW51OiBNZW51LCBvcHRpb25zPzogSU1haW5NZW51LklBZGRPcHRpb25zKTogdm9pZDtcblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiRmlsZVwiIG1lbnUuXG4gICAqL1xuICByZWFkb25seSBmaWxlTWVudTogSUZpbGVNZW51O1xuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJFZGl0XCIgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGVkaXRNZW51OiBJRWRpdE1lbnU7XG5cbiAgLyoqXG4gICAqIFRoZSBhcHBsaWNhdGlvbiBcIlZpZXdcIiBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgdmlld01lbnU6IElWaWV3TWVudTtcblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiSGVscFwiIG1lbnUuXG4gICAqL1xuICByZWFkb25seSBoZWxwTWVudTogSUhlbHBNZW51O1xuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJLZXJuZWxcIiBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkga2VybmVsTWVudTogSUtlcm5lbE1lbnU7XG5cbiAgLyoqXG4gICAqIFRoZSBhcHBsaWNhdGlvbiBcIlJ1blwiIG1lbnUuXG4gICAqL1xuICByZWFkb25seSBydW5NZW51OiBJUnVuTWVudTtcblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiU2V0dGluZ3NcIiBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgc2V0dGluZ3NNZW51OiBJU2V0dGluZ3NNZW51O1xuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJUYWJzXCIgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IHRhYnNNZW51OiBJVGFic01lbnU7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgSU1haW5NZW51IGF0dGFjaGVkIGludGVyZmFjZXMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSU1haW5NZW51IHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gYWRkIGEgbWVudSB0byB0aGUgbWFpbiBtZW51LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQWRkT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIHJhbmsgb3JkZXIgb2YgdGhlIG1lbnUgYW1vbmcgaXRzIHNpYmxpbmdzLlxuICAgICAqL1xuICAgIHJhbms/OiBudW1iZXI7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgYW4gSU1haW5NZW51LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTWVudU9wdGlvbnMgZXh0ZW5kcyBNZW51RmFjdG9yeS5JTWVudU9wdGlvbnMge31cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVJhbmtlZE1lbnUsIFJhbmtlZE1lbnUgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBJTWVudUV4dGVuZGVyIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3IgYSBWaWV3IG1lbnUuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVZpZXdNZW51IGV4dGVuZHMgSVJhbmtlZE1lbnUge1xuICAvKipcbiAgICogQSBzZXQgc3RvcmluZyBJS2VybmVsVXNlcnMgZm9yIHRoZSBLZXJuZWwgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGVkaXRvclZpZXdlcnM6IFNldDxJVmlld01lbnUuSUVkaXRvclZpZXdlcjxXaWRnZXQ+Pjtcbn1cblxuLyoqXG4gKiBBbiBleHRlbnNpYmxlIFZpZXcgbWVudSBmb3IgdGhlIGFwcGxpY2F0aW9uLlxuICovXG5leHBvcnQgY2xhc3MgVmlld01lbnUgZXh0ZW5kcyBSYW5rZWRNZW51IGltcGxlbWVudHMgSVZpZXdNZW51IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCB0aGUgdmlldyBtZW51LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogSVJhbmtlZE1lbnUuSU9wdGlvbnMpIHtcbiAgICBzdXBlcihvcHRpb25zKTtcbiAgICB0aGlzLmVkaXRvclZpZXdlcnMgPSBuZXcgU2V0PElWaWV3TWVudS5JRWRpdG9yVmlld2VyPFdpZGdldD4+KCk7XG4gIH1cblxuICAvKipcbiAgICogQSBzZXQgc3RvcmluZyBJRWRpdG9yVmlld2VycyBmb3IgdGhlIFZpZXcgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGVkaXRvclZpZXdlcnM6IFNldDxJVmlld01lbnUuSUVkaXRvclZpZXdlcjxXaWRnZXQ+PjtcblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHZpZXcgbWVudS5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgdGhpcy5lZGl0b3JWaWV3ZXJzLmNsZWFyKCk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG59XG5cbi8qKlxuICogTmFtZXNwYWNlIGZvciBJVmlld01lbnUuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVZpZXdNZW51IHtcbiAgLyoqXG4gICAqIEludGVyZmFjZSBmb3IgYSB0ZXh0IGVkaXRvciB2aWV3ZXIgdG8gcmVnaXN0ZXJcbiAgICogaXRzZWxmIHdpdGggdGhlIHRleHQgZWRpdG9yIGV4dGVuc2lvbiBwb2ludHMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElFZGl0b3JWaWV3ZXI8VCBleHRlbmRzIFdpZGdldD4gZXh0ZW5kcyBJTWVudUV4dGVuZGVyPFQ+IHtcbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIHNob3cgbGluZSBudW1iZXJzIGluIHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgdG9nZ2xlTGluZU51bWJlcnM/OiAod2lkZ2V0OiBUKSA9PiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byB3b3JkLXdyYXAgdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICB0b2dnbGVXb3JkV3JhcD86ICh3aWRnZXQ6IFQpID0+IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIG1hdGNoIGJyYWNrZXRzIGluIHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgdG9nZ2xlTWF0Y2hCcmFja2V0cz86ICh3aWRnZXQ6IFQpID0+IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIGxpbmUgbnVtYmVycyBhcmUgdG9nZ2xlZC5cbiAgICAgKi9cbiAgICBsaW5lTnVtYmVyc1RvZ2dsZWQ/OiAod2lkZ2V0OiBUKSA9PiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB3b3JkIHdyYXAgaXMgdG9nZ2xlZC5cbiAgICAgKi9cbiAgICB3b3JkV3JhcFRvZ2dsZWQ/OiAod2lkZ2V0OiBUKSA9PiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciBtYXRjaCBicmFja2V0cyBpcyB0b2dnbGVkLlxuICAgICAqL1xuICAgIG1hdGNoQnJhY2tldHNUb2dnbGVkPzogKHdpZGdldDogVCkgPT4gYm9vbGVhbjtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==