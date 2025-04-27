(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_launcher_lib_index_js"],{

/***/ "../packages/launcher/lib/index.js":
/*!*****************************************!*\
  !*** ../packages/launcher/lib/index.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ILauncher": () => (/* binding */ ILauncher),
/* harmony export */   "LauncherModel": () => (/* binding */ LauncherModel),
/* harmony export */   "Launcher": () => (/* binding */ Launcher)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_8__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module launcher
 */









/**
 * The class name added to Launcher instances.
 */
const LAUNCHER_CLASS = 'jp-Launcher';
/* tslint:disable */
/**
 * The launcher token.
 */
const ILauncher = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.Token('@jupyterlab/launcher:ILauncher');
/**
 * LauncherModel keeps track of the path to working directory and has a list of
 * LauncherItems, which the Launcher will render.
 */
class LauncherModel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
    constructor() {
        super(...arguments);
        this._items = [];
    }
    /**
     * Add a command item to the launcher, and trigger re-render event for parent
     * widget.
     *
     * @param options - The specification options for a launcher item.
     *
     * @returns A disposable that will remove the item from Launcher, and trigger
     * re-render event for parent widget.
     *
     */
    add(options) {
        // Create a copy of the options to circumvent mutations to the original.
        const item = Private.createItem(options);
        this._items.push(item);
        this.stateChanged.emit(void 0);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_5__.DisposableDelegate(() => {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayExt.removeFirstOf(this._items, item);
            this.stateChanged.emit(void 0);
        });
    }
    /**
     * Return an iterator of launcher items.
     */
    items() {
        return new _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayIterator(this._items);
    }
}
/**
 * A virtual-DOM-based widget for the Launcher.
 */
class Launcher extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Construct a new launcher widget.
     */
    constructor(options) {
        super(options.model);
        this._pending = false;
        this._cwd = '';
        this._cwd = options.cwd;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._callback = options.callback;
        this._commands = options.commands;
        this.addClass(LAUNCHER_CLASS);
    }
    /**
     * The cwd of the launcher.
     */
    get cwd() {
        return this._cwd;
    }
    set cwd(value) {
        this._cwd = value;
        this.update();
    }
    /**
     * Whether there is a pending item being launched.
     */
    get pending() {
        return this._pending;
    }
    set pending(value) {
        this._pending = value;
    }
    /**
     * Render the launcher to virtual DOM nodes.
     */
    render() {
        // Bail if there is no model.
        if (!this.model) {
            return null;
        }
        const knownCategories = [
            this._trans.__('Notebook'),
            this._trans.__('Console'),
            this._trans.__('Other')
        ];
        const kernelCategories = [
            this._trans.__('Notebook'),
            this._trans.__('Console')
        ];
        // First group-by categories
        const categories = Object.create(null);
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(this.model.items(), (item, index) => {
            const cat = item.category || this._trans.__('Other');
            if (!(cat in categories)) {
                categories[cat] = [];
            }
            categories[cat].push(item);
        });
        // Within each category sort by rank
        for (const cat in categories) {
            categories[cat] = categories[cat].sort((a, b) => {
                return Private.sortCmp(a, b, this._cwd, this._commands);
            });
        }
        // Variable to help create sections
        const sections = [];
        let section;
        // Assemble the final ordered list of categories, beginning with
        // KNOWN_CATEGORIES.
        const orderedCategories = [];
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(knownCategories, (cat, index) => {
            orderedCategories.push(cat);
        });
        for (const cat in categories) {
            if (knownCategories.indexOf(cat) === -1) {
                orderedCategories.push(cat);
            }
        }
        // Now create the sections for each category
        orderedCategories.forEach(cat => {
            if (!categories[cat]) {
                return;
            }
            const item = categories[cat][0];
            const args = Object.assign(Object.assign({}, item.args), { cwd: this.cwd });
            const kernel = kernelCategories.indexOf(cat) > -1;
            // DEPRECATED: remove _icon when lumino 2.0 is adopted
            // if icon is aliasing iconClass, don't use it
            const iconClass = this._commands.iconClass(item.command, args);
            const _icon = this._commands.icon(item.command, args);
            const icon = _icon === iconClass ? undefined : _icon;
            if (cat in categories) {
                section = (react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-Launcher-section", key: cat },
                    react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-Launcher-sectionHeader" },
                        react__WEBPACK_IMPORTED_MODULE_8__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon.resolveReact, { icon: icon, iconClass: (0,_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.classes)(iconClass, 'jp-Icon-cover'), stylesheet: "launcherSection" }),
                        react__WEBPACK_IMPORTED_MODULE_8__.createElement("h2", { className: "jp-Launcher-sectionTitle" }, cat)),
                    react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-Launcher-cardContainer" }, (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.toArray)((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.map)(categories[cat], (item) => {
                        return Card(kernel, item, this, this._commands, this._trans, this._callback);
                    })))));
                sections.push(section);
            }
        });
        // Wrap the sections in body and content divs.
        return (react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-Launcher-body" },
            react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-Launcher-content" },
                react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-Launcher-cwd" },
                    react__WEBPACK_IMPORTED_MODULE_8__.createElement("h3", null, this.cwd)),
                sections)));
    }
}
/**
 * A pure tsx component for a launcher card.
 *
 * @param kernel - whether the item takes uses a kernel.
 *
 * @param item - the launcher item to render.
 *
 * @param launcher - the Launcher instance to which this is added.
 *
 * @param launcherCallback - a callback to call after an item has been launched.
 *
 * @returns a vdom `VirtualElement` for the launcher card.
 */
function Card(kernel, item, launcher, commands, trans, launcherCallback) {
    // Get some properties of the command
    const command = item.command;
    const args = Object.assign(Object.assign({}, item.args), { cwd: launcher.cwd });
    const caption = commands.caption(command, args);
    const label = commands.label(command, args);
    const title = kernel ? label : caption || label;
    // Build the onclick handler.
    const onclick = () => {
        // If an item has already been launched,
        // don't try to launch another.
        if (launcher.pending === true) {
            return;
        }
        launcher.pending = true;
        void commands
            .execute(command, Object.assign(Object.assign({}, item.args), { cwd: launcher.cwd }))
            .then(value => {
            launcher.pending = false;
            if (value instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__.Widget) {
                launcherCallback(value);
                launcher.dispose();
            }
        })
            .catch(err => {
            launcher.pending = false;
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)(trans._p('Error', 'Launcher Error'), err);
        });
    };
    // With tabindex working, you can now pick a kernel by tabbing around and
    // pressing Enter.
    const onkeypress = (event) => {
        if (event.key === 'Enter') {
            onclick();
        }
    };
    // DEPRECATED: remove _icon when lumino 2.0 is adopted
    // if icon is aliasing iconClass, don't use it
    const iconClass = commands.iconClass(command, args);
    const _icon = commands.icon(command, args);
    const icon = _icon === iconClass ? undefined : _icon;
    // Return the VDOM element.
    return (react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-LauncherCard", title: title, onClick: onclick, onKeyPress: onkeypress, tabIndex: 0, "data-category": item.category || trans.__('Other'), key: Private.keyProperty.get(item) },
        react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-LauncherCard-icon" }, kernel ? (item.kernelIconUrl ? (react__WEBPACK_IMPORTED_MODULE_8__.createElement("img", { src: item.kernelIconUrl, className: "jp-Launcher-kernelIcon" })) : (react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-LauncherCard-noKernelIcon" }, label[0].toUpperCase()))) : (react__WEBPACK_IMPORTED_MODULE_8__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon.resolveReact, { icon: icon, iconClass: (0,_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.classes)(iconClass, 'jp-Icon-cover'), stylesheet: "launcherCard" }))),
        react__WEBPACK_IMPORTED_MODULE_8__.createElement("div", { className: "jp-LauncherCard-label", title: title },
            react__WEBPACK_IMPORTED_MODULE_8__.createElement("p", null, label))));
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * An incrementing counter for keys.
     */
    let id = 0;
    /**
     * An attached property for an item's key.
     */
    Private.keyProperty = new _lumino_properties__WEBPACK_IMPORTED_MODULE_6__.AttachedProperty({
        name: 'key',
        create: () => id++
    });
    /**
     * Create a fully specified item given item options.
     */
    function createItem(options) {
        return Object.assign(Object.assign({}, options), { category: options.category || '', rank: options.rank !== undefined ? options.rank : Infinity });
    }
    Private.createItem = createItem;
    /**
     * A sort comparison function for a launcher item.
     */
    function sortCmp(a, b, cwd, commands) {
        // First, compare by rank.
        const r1 = a.rank;
        const r2 = b.rank;
        if (r1 !== r2 && r1 !== undefined && r2 !== undefined) {
            return r1 < r2 ? -1 : 1; // Infinity safe
        }
        // Finally, compare by display name.
        const aLabel = commands.label(a.command, Object.assign(Object.assign({}, a.args), { cwd }));
        const bLabel = commands.label(b.command, Object.assign(Object.assign({}, b.args), { cwd }));
        return aLabel.localeCompare(bLabel);
    }
    Private.sortCmp = sortCmp;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbGF1bmNoZXIvc3JjL2luZGV4LnRzeCJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU0yQjtBQUtHO0FBQzRCO0FBUWxDO0FBRW1DO0FBQ087QUFDZjtBQUNiO0FBQ1Y7QUFFL0I7O0dBRUc7QUFDSCxNQUFNLGNBQWMsR0FBRyxhQUFhLENBQUM7QUFFckMsb0JBQW9CO0FBQ3BCOztHQUVHO0FBQ0ksTUFBTSxTQUFTLEdBQUcsSUFBSSxvREFBSyxDQUFZLGdDQUFnQyxDQUFDLENBQUM7QUFvQmhGOzs7R0FHRztBQUNJLE1BQU0sYUFBYyxTQUFRLDJEQUFTO0lBQTVDOztRQStCVSxXQUFNLEdBQTZCLEVBQUUsQ0FBQztJQUNoRCxDQUFDO0lBL0JDOzs7Ozs7Ozs7T0FTRztJQUNILEdBQUcsQ0FBQyxPQUErQjtRQUNqQyx3RUFBd0U7UUFDeEUsTUFBTSxJQUFJLEdBQUcsT0FBTyxDQUFDLFVBQVUsQ0FBQyxPQUFPLENBQUMsQ0FBQztRQUV6QyxJQUFJLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUN2QixJQUFJLENBQUMsWUFBWSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDO1FBRS9CLE9BQU8sSUFBSSxrRUFBa0IsQ0FBQyxHQUFHLEVBQUU7WUFDakMscUVBQXNCLENBQUMsSUFBSSxDQUFDLE1BQU0sRUFBRSxJQUFJLENBQUMsQ0FBQztZQUMxQyxJQUFJLENBQUMsWUFBWSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDO1FBQ2pDLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVEOztPQUVHO0lBQ0gsS0FBSztRQUNILE9BQU8sSUFBSSw0REFBYSxDQUFDLElBQUksQ0FBQyxNQUFNLENBQUMsQ0FBQztJQUN4QyxDQUFDO0NBR0Y7QUFFRDs7R0FFRztBQUNJLE1BQU0sUUFBUyxTQUFRLDhEQUEyQjtJQUN2RDs7T0FFRztJQUNILFlBQVksT0FBMkI7UUFDckMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxLQUFLLENBQUMsQ0FBQztRQWtKZixhQUFRLEdBQUcsS0FBSyxDQUFDO1FBQ2pCLFNBQUksR0FBRyxFQUFFLENBQUM7UUFsSmhCLElBQUksQ0FBQyxJQUFJLEdBQUcsT0FBTyxDQUFDLEdBQUcsQ0FBQztRQUN4QixJQUFJLENBQUMsVUFBVSxHQUFHLE9BQU8sQ0FBQyxVQUFVLElBQUksbUVBQWMsQ0FBQztRQUN2RCxJQUFJLENBQUMsTUFBTSxHQUFHLElBQUksQ0FBQyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQ2pELElBQUksQ0FBQyxTQUFTLEdBQUcsT0FBTyxDQUFDLFFBQVEsQ0FBQztRQUNsQyxJQUFJLENBQUMsU0FBUyxHQUFHLE9BQU8sQ0FBQyxRQUFRLENBQUM7UUFDbEMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxjQUFjLENBQUMsQ0FBQztJQUNoQyxDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLEdBQUc7UUFDTCxPQUFPLElBQUksQ0FBQyxJQUFJLENBQUM7SUFDbkIsQ0FBQztJQUNELElBQUksR0FBRyxDQUFDLEtBQWE7UUFDbkIsSUFBSSxDQUFDLElBQUksR0FBRyxLQUFLLENBQUM7UUFDbEIsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO0lBQ2hCLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksT0FBTztRQUNULE9BQU8sSUFBSSxDQUFDLFFBQVEsQ0FBQztJQUN2QixDQUFDO0lBQ0QsSUFBSSxPQUFPLENBQUMsS0FBYztRQUN4QixJQUFJLENBQUMsUUFBUSxHQUFHLEtBQUssQ0FBQztJQUN4QixDQUFDO0lBRUQ7O09BRUc7SUFDTyxNQUFNO1FBQ2QsNkJBQTZCO1FBQzdCLElBQUksQ0FBQyxJQUFJLENBQUMsS0FBSyxFQUFFO1lBQ2YsT0FBTyxJQUFJLENBQUM7U0FDYjtRQUVELE1BQU0sZUFBZSxHQUFHO1lBQ3RCLElBQUksQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQztZQUMxQixJQUFJLENBQUMsTUFBTSxDQUFDLEVBQUUsQ0FBQyxTQUFTLENBQUM7WUFDekIsSUFBSSxDQUFDLE1BQU0sQ0FBQyxFQUFFLENBQUMsT0FBTyxDQUFDO1NBQ3hCLENBQUM7UUFDRixNQUFNLGdCQUFnQixHQUFHO1lBQ3ZCLElBQUksQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQztZQUMxQixJQUFJLENBQUMsTUFBTSxDQUFDLEVBQUUsQ0FBQyxTQUFTLENBQUM7U0FDMUIsQ0FBQztRQUVGLDRCQUE0QjtRQUM1QixNQUFNLFVBQVUsR0FBRyxNQUFNLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxDQUFDO1FBQ3ZDLHVEQUFJLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxLQUFLLEVBQUUsRUFBRSxDQUFDLElBQUksRUFBRSxLQUFLLEVBQUUsRUFBRTtZQUN2QyxNQUFNLEdBQUcsR0FBRyxJQUFJLENBQUMsUUFBUSxJQUFJLElBQUksQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLE9BQU8sQ0FBQyxDQUFDO1lBQ3JELElBQUksQ0FBQyxDQUFDLEdBQUcsSUFBSSxVQUFVLENBQUMsRUFBRTtnQkFDeEIsVUFBVSxDQUFDLEdBQUcsQ0FBQyxHQUFHLEVBQUUsQ0FBQzthQUN0QjtZQUNELFVBQVUsQ0FBQyxHQUFHLENBQUMsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLENBQUM7UUFDN0IsQ0FBQyxDQUFDLENBQUM7UUFDSCxvQ0FBb0M7UUFDcEMsS0FBSyxNQUFNLEdBQUcsSUFBSSxVQUFVLEVBQUU7WUFDNUIsVUFBVSxDQUFDLEdBQUcsQ0FBQyxHQUFHLFVBQVUsQ0FBQyxHQUFHLENBQUMsQ0FBQyxJQUFJLENBQ3BDLENBQUMsQ0FBeUIsRUFBRSxDQUF5QixFQUFFLEVBQUU7Z0JBQ3ZELE9BQU8sT0FBTyxDQUFDLE9BQU8sQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUFFLElBQUksQ0FBQyxJQUFJLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQyxDQUFDO1lBQzFELENBQUMsQ0FDRixDQUFDO1NBQ0g7UUFFRCxtQ0FBbUM7UUFDbkMsTUFBTSxRQUFRLEdBQThCLEVBQUUsQ0FBQztRQUMvQyxJQUFJLE9BQWdDLENBQUM7UUFFckMsZ0VBQWdFO1FBQ2hFLG9CQUFvQjtRQUNwQixNQUFNLGlCQUFpQixHQUFhLEVBQUUsQ0FBQztRQUN2Qyx1REFBSSxDQUFDLGVBQWUsRUFBRSxDQUFDLEdBQUcsRUFBRSxLQUFLLEVBQUUsRUFBRTtZQUNuQyxpQkFBaUIsQ0FBQyxJQUFJLENBQUMsR0FBRyxDQUFDLENBQUM7UUFDOUIsQ0FBQyxDQUFDLENBQUM7UUFDSCxLQUFLLE1BQU0sR0FBRyxJQUFJLFVBQVUsRUFBRTtZQUM1QixJQUFJLGVBQWUsQ0FBQyxPQUFPLENBQUMsR0FBRyxDQUFDLEtBQUssQ0FBQyxDQUFDLEVBQUU7Z0JBQ3ZDLGlCQUFpQixDQUFDLElBQUksQ0FBQyxHQUFHLENBQUMsQ0FBQzthQUM3QjtTQUNGO1FBRUQsNENBQTRDO1FBQzVDLGlCQUFpQixDQUFDLE9BQU8sQ0FBQyxHQUFHLENBQUMsRUFBRTtZQUM5QixJQUFJLENBQUMsVUFBVSxDQUFDLEdBQUcsQ0FBQyxFQUFFO2dCQUNwQixPQUFPO2FBQ1I7WUFDRCxNQUFNLElBQUksR0FBRyxVQUFVLENBQUMsR0FBRyxDQUFDLENBQUMsQ0FBQyxDQUEyQixDQUFDO1lBQzFELE1BQU0sSUFBSSxtQ0FBUSxJQUFJLENBQUMsSUFBSSxLQUFFLEdBQUcsRUFBRSxJQUFJLENBQUMsR0FBRyxHQUFFLENBQUM7WUFDN0MsTUFBTSxNQUFNLEdBQUcsZ0JBQWdCLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDO1lBRWxELHNEQUFzRDtZQUN0RCw4Q0FBOEM7WUFDOUMsTUFBTSxTQUFTLEdBQUcsSUFBSSxDQUFDLFNBQVMsQ0FBQyxTQUFTLENBQUMsSUFBSSxDQUFDLE9BQU8sRUFBRSxJQUFJLENBQUMsQ0FBQztZQUMvRCxNQUFNLEtBQUssR0FBRyxJQUFJLENBQUMsU0FBUyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsT0FBTyxFQUFFLElBQUksQ0FBQyxDQUFDO1lBQ3RELE1BQU0sSUFBSSxHQUFHLEtBQUssS0FBSyxTQUFTLENBQUMsQ0FBQyxDQUFDLFNBQVMsQ0FBQyxDQUFDLENBQUMsS0FBSyxDQUFDO1lBRXJELElBQUksR0FBRyxJQUFJLFVBQVUsRUFBRTtnQkFDckIsT0FBTyxHQUFHLENBQ1IsMERBQUssU0FBUyxFQUFDLHFCQUFxQixFQUFDLEdBQUcsRUFBRSxHQUFHO29CQUMzQywwREFBSyxTQUFTLEVBQUMsMkJBQTJCO3dCQUN4QyxpREFBQywyRUFBb0IsSUFDbkIsSUFBSSxFQUFFLElBQUksRUFDVixTQUFTLEVBQUUsa0VBQU8sQ0FBQyxTQUFTLEVBQUUsZUFBZSxDQUFDLEVBQzlDLFVBQVUsRUFBQyxpQkFBaUIsR0FDNUI7d0JBQ0YseURBQUksU0FBUyxFQUFDLDBCQUEwQixJQUFFLEdBQUcsQ0FBTSxDQUMvQztvQkFDTiwwREFBSyxTQUFTLEVBQUMsMkJBQTJCLElBQ3ZDLDBEQUFPLENBQ04sc0RBQUcsQ0FBQyxVQUFVLENBQUMsR0FBRyxDQUFDLEVBQUUsQ0FBQyxJQUE0QixFQUFFLEVBQUU7d0JBQ3BELE9BQU8sSUFBSSxDQUNULE1BQU0sRUFDTixJQUFJLEVBQ0osSUFBSSxFQUNKLElBQUksQ0FBQyxTQUFTLEVBQ2QsSUFBSSxDQUFDLE1BQU0sRUFDWCxJQUFJLENBQUMsU0FBUyxDQUNmLENBQUM7b0JBQ0osQ0FBQyxDQUFDLENBQ0gsQ0FDRyxDQUNGLENBQ1AsQ0FBQztnQkFDRixRQUFRLENBQUMsSUFBSSxDQUFDLE9BQU8sQ0FBQyxDQUFDO2FBQ3hCO1FBQ0gsQ0FBQyxDQUFDLENBQUM7UUFFSCw4Q0FBOEM7UUFDOUMsT0FBTyxDQUNMLDBEQUFLLFNBQVMsRUFBQyxrQkFBa0I7WUFDL0IsMERBQUssU0FBUyxFQUFDLHFCQUFxQjtnQkFDbEMsMERBQUssU0FBUyxFQUFDLGlCQUFpQjtvQkFDOUIsNkRBQUssSUFBSSxDQUFDLEdBQUcsQ0FBTSxDQUNmO2dCQUNMLFFBQVEsQ0FDTCxDQUNGLENBQ1AsQ0FBQztJQUNKLENBQUM7Q0FRRjtBQXFHRDs7Ozs7Ozs7Ozs7O0dBWUc7QUFDSCxTQUFTLElBQUksQ0FDWCxNQUFlLEVBQ2YsSUFBNEIsRUFDNUIsUUFBa0IsRUFDbEIsUUFBeUIsRUFDekIsS0FBd0IsRUFDeEIsZ0JBQTBDO0lBRTFDLHFDQUFxQztJQUNyQyxNQUFNLE9BQU8sR0FBRyxJQUFJLENBQUMsT0FBTyxDQUFDO0lBQzdCLE1BQU0sSUFBSSxtQ0FBUSxJQUFJLENBQUMsSUFBSSxLQUFFLEdBQUcsRUFBRSxRQUFRLENBQUMsR0FBRyxHQUFFLENBQUM7SUFDakQsTUFBTSxPQUFPLEdBQUcsUUFBUSxDQUFDLE9BQU8sQ0FBQyxPQUFPLEVBQUUsSUFBSSxDQUFDLENBQUM7SUFDaEQsTUFBTSxLQUFLLEdBQUcsUUFBUSxDQUFDLEtBQUssQ0FBQyxPQUFPLEVBQUUsSUFBSSxDQUFDLENBQUM7SUFDNUMsTUFBTSxLQUFLLEdBQUcsTUFBTSxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLE9BQU8sSUFBSSxLQUFLLENBQUM7SUFFaEQsNkJBQTZCO0lBQzdCLE1BQU0sT0FBTyxHQUFHLEdBQUcsRUFBRTtRQUNuQix3Q0FBd0M7UUFDeEMsK0JBQStCO1FBQy9CLElBQUksUUFBUSxDQUFDLE9BQU8sS0FBSyxJQUFJLEVBQUU7WUFDN0IsT0FBTztTQUNSO1FBQ0QsUUFBUSxDQUFDLE9BQU8sR0FBRyxJQUFJLENBQUM7UUFDeEIsS0FBSyxRQUFRO2FBQ1YsT0FBTyxDQUFDLE9BQU8sa0NBQ1gsSUFBSSxDQUFDLElBQUksS0FDWixHQUFHLEVBQUUsUUFBUSxDQUFDLEdBQUcsSUFDakI7YUFDRCxJQUFJLENBQUMsS0FBSyxDQUFDLEVBQUU7WUFDWixRQUFRLENBQUMsT0FBTyxHQUFHLEtBQUssQ0FBQztZQUN6QixJQUFJLEtBQUssWUFBWSxtREFBTSxFQUFFO2dCQUMzQixnQkFBZ0IsQ0FBQyxLQUFLLENBQUMsQ0FBQztnQkFDeEIsUUFBUSxDQUFDLE9BQU8sRUFBRSxDQUFDO2FBQ3BCO1FBQ0gsQ0FBQyxDQUFDO2FBQ0QsS0FBSyxDQUFDLEdBQUcsQ0FBQyxFQUFFO1lBQ1gsUUFBUSxDQUFDLE9BQU8sR0FBRyxLQUFLLENBQUM7WUFDekIsS0FBSyxzRUFBZ0IsQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUFDLE9BQU8sRUFBRSxnQkFBZ0IsQ0FBQyxFQUFFLEdBQUcsQ0FBQyxDQUFDO1FBQ2xFLENBQUMsQ0FBQyxDQUFDO0lBQ1AsQ0FBQyxDQUFDO0lBRUYseUVBQXlFO0lBQ3pFLGtCQUFrQjtJQUNsQixNQUFNLFVBQVUsR0FBRyxDQUFDLEtBQTBCLEVBQUUsRUFBRTtRQUNoRCxJQUFJLEtBQUssQ0FBQyxHQUFHLEtBQUssT0FBTyxFQUFFO1lBQ3pCLE9BQU8sRUFBRSxDQUFDO1NBQ1g7SUFDSCxDQUFDLENBQUM7SUFFRixzREFBc0Q7SUFDdEQsOENBQThDO0lBQzlDLE1BQU0sU0FBUyxHQUFHLFFBQVEsQ0FBQyxTQUFTLENBQUMsT0FBTyxFQUFFLElBQUksQ0FBQyxDQUFDO0lBQ3BELE1BQU0sS0FBSyxHQUFHLFFBQVEsQ0FBQyxJQUFJLENBQUMsT0FBTyxFQUFFLElBQUksQ0FBQyxDQUFDO0lBQzNDLE1BQU0sSUFBSSxHQUFHLEtBQUssS0FBSyxTQUFTLENBQUMsQ0FBQyxDQUFDLFNBQVMsQ0FBQyxDQUFDLENBQUMsS0FBSyxDQUFDO0lBRXJELDJCQUEyQjtJQUMzQixPQUFPLENBQ0wsMERBQ0UsU0FBUyxFQUFDLGlCQUFpQixFQUMzQixLQUFLLEVBQUUsS0FBSyxFQUNaLE9BQU8sRUFBRSxPQUFPLEVBQ2hCLFVBQVUsRUFBRSxVQUFVLEVBQ3RCLFFBQVEsRUFBRSxDQUFDLG1CQUNJLElBQUksQ0FBQyxRQUFRLElBQUksS0FBSyxDQUFDLEVBQUUsQ0FBQyxPQUFPLENBQUMsRUFDakQsR0FBRyxFQUFFLE9BQU8sQ0FBQyxXQUFXLENBQUMsR0FBRyxDQUFDLElBQUksQ0FBQztRQUVsQywwREFBSyxTQUFTLEVBQUMsc0JBQXNCLElBQ2xDLE1BQU0sQ0FBQyxDQUFDLENBQUMsQ0FDUixJQUFJLENBQUMsYUFBYSxDQUFDLENBQUMsQ0FBQyxDQUNuQiwwREFBSyxHQUFHLEVBQUUsSUFBSSxDQUFDLGFBQWEsRUFBRSxTQUFTLEVBQUMsd0JBQXdCLEdBQUcsQ0FDcEUsQ0FBQyxDQUFDLENBQUMsQ0FDRiwwREFBSyxTQUFTLEVBQUMsOEJBQThCLElBQzFDLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQyxXQUFXLEVBQUUsQ0FDbkIsQ0FDUCxDQUNGLENBQUMsQ0FBQyxDQUFDLENBQ0YsaURBQUMsMkVBQW9CLElBQ25CLElBQUksRUFBRSxJQUFJLEVBQ1YsU0FBUyxFQUFFLGtFQUFPLENBQUMsU0FBUyxFQUFFLGVBQWUsQ0FBQyxFQUM5QyxVQUFVLEVBQUMsY0FBYyxHQUN6QixDQUNILENBQ0c7UUFDTiwwREFBSyxTQUFTLEVBQUMsdUJBQXVCLEVBQUMsS0FBSyxFQUFFLEtBQUs7WUFDakQsNERBQUksS0FBSyxDQUFLLENBQ1YsQ0FDRixDQUNQLENBQUM7QUFDSixDQUFDO0FBRUQ7O0dBRUc7QUFDSCxJQUFVLE9BQU8sQ0FtRGhCO0FBbkRELFdBQVUsT0FBTztJQUNmOztPQUVHO0lBQ0gsSUFBSSxFQUFFLEdBQUcsQ0FBQyxDQUFDO0lBRVg7O09BRUc7SUFDVSxtQkFBVyxHQUFHLElBQUksZ0VBQWdCLENBRzdDO1FBQ0EsSUFBSSxFQUFFLEtBQUs7UUFDWCxNQUFNLEVBQUUsR0FBRyxFQUFFLENBQUMsRUFBRSxFQUFFO0tBQ25CLENBQUMsQ0FBQztJQUVIOztPQUVHO0lBQ0gsU0FBZ0IsVUFBVSxDQUN4QixPQUErQjtRQUUvQix1Q0FDSyxPQUFPLEtBQ1YsUUFBUSxFQUFFLE9BQU8sQ0FBQyxRQUFRLElBQUksRUFBRSxFQUNoQyxJQUFJLEVBQUUsT0FBTyxDQUFDLElBQUksS0FBSyxTQUFTLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLFFBQVEsSUFDMUQ7SUFDSixDQUFDO0lBUmUsa0JBQVUsYUFRekI7SUFFRDs7T0FFRztJQUNILFNBQWdCLE9BQU8sQ0FDckIsQ0FBeUIsRUFDekIsQ0FBeUIsRUFDekIsR0FBVyxFQUNYLFFBQXlCO1FBRXpCLDBCQUEwQjtRQUMxQixNQUFNLEVBQUUsR0FBRyxDQUFDLENBQUMsSUFBSSxDQUFDO1FBQ2xCLE1BQU0sRUFBRSxHQUFHLENBQUMsQ0FBQyxJQUFJLENBQUM7UUFDbEIsSUFBSSxFQUFFLEtBQUssRUFBRSxJQUFJLEVBQUUsS0FBSyxTQUFTLElBQUksRUFBRSxLQUFLLFNBQVMsRUFBRTtZQUNyRCxPQUFPLEVBQUUsR0FBRyxFQUFFLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxnQkFBZ0I7U0FDMUM7UUFFRCxvQ0FBb0M7UUFDcEMsTUFBTSxNQUFNLEdBQUcsUUFBUSxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUMsT0FBTyxrQ0FBTyxDQUFDLENBQUMsSUFBSSxLQUFFLEdBQUcsSUFBRyxDQUFDO1FBQzdELE1BQU0sTUFBTSxHQUFHLFFBQVEsQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLE9BQU8sa0NBQU8sQ0FBQyxDQUFDLElBQUksS0FBRSxHQUFHLElBQUcsQ0FBQztRQUM3RCxPQUFPLE1BQU0sQ0FBQyxhQUFhLENBQUMsTUFBTSxDQUFDLENBQUM7SUFDdEMsQ0FBQztJQWpCZSxlQUFPLFVBaUJ0QjtBQUNILENBQUMsRUFuRFMsT0FBTyxLQUFQLE9BQU8sUUFtRGhCIiwiZmlsZSI6InBhY2thZ2VzX2xhdW5jaGVyX2xpYl9pbmRleF9qcy4zOWYzOTE2NWZiZTcxNTViNzhhMi5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGxhdW5jaGVyXG4gKi9cblxuaW1wb3J0IHtcbiAgc2hvd0Vycm9yTWVzc2FnZSxcbiAgVkRvbU1vZGVsLFxuICBWRG9tUmVuZGVyZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIG51bGxUcmFuc2xhdG9yLFxuICBUcmFuc2xhdGlvbkJ1bmRsZVxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBjbGFzc2VzLCBMYWJJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQge1xuICBBcnJheUV4dCxcbiAgQXJyYXlJdGVyYXRvcixcbiAgZWFjaCxcbiAgSUl0ZXJhdG9yLFxuICBtYXAsXG4gIHRvQXJyYXlcbn0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHsgQ29tbWFuZFJlZ2lzdHJ5IH0gZnJvbSAnQGx1bWluby9jb21tYW5kcyc7XG5pbXBvcnQgeyBSZWFkb25seUpTT05PYmplY3QsIFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgRGlzcG9zYWJsZURlbGVnYXRlLCBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBBdHRhY2hlZFByb3BlcnR5IH0gZnJvbSAnQGx1bWluby9wcm9wZXJ0aWVzJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gTGF1bmNoZXIgaW5zdGFuY2VzLlxuICovXG5jb25zdCBMQVVOQ0hFUl9DTEFTUyA9ICdqcC1MYXVuY2hlcic7XG5cbi8qIHRzbGludDpkaXNhYmxlICovXG4vKipcbiAqIFRoZSBsYXVuY2hlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElMYXVuY2hlciA9IG5ldyBUb2tlbjxJTGF1bmNoZXI+KCdAanVweXRlcmxhYi9sYXVuY2hlcjpJTGF1bmNoZXInKTtcbi8qIHRzbGludDplbmFibGUgKi9cblxuLyoqXG4gKiBUaGUgbGF1bmNoZXIgaW50ZXJmYWNlLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElMYXVuY2hlciB7XG4gIC8qKlxuICAgKiBBZGQgYSBjb21tYW5kIGl0ZW0gdG8gdGhlIGxhdW5jaGVyLCBhbmQgdHJpZ2dlciByZS1yZW5kZXIgZXZlbnQgZm9yIHBhcmVudFxuICAgKiB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIHNwZWNpZmljYXRpb24gb3B0aW9ucyBmb3IgYSBsYXVuY2hlciBpdGVtLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGRpc3Bvc2FibGUgdGhhdCB3aWxsIHJlbW92ZSB0aGUgaXRlbSBmcm9tIExhdW5jaGVyLCBhbmQgdHJpZ2dlclxuICAgKiByZS1yZW5kZXIgZXZlbnQgZm9yIHBhcmVudCB3aWRnZXQuXG4gICAqXG4gICAqL1xuICBhZGQob3B0aW9uczogSUxhdW5jaGVyLklJdGVtT3B0aW9ucyk6IElEaXNwb3NhYmxlO1xufVxuXG4vKipcbiAqIExhdW5jaGVyTW9kZWwga2VlcHMgdHJhY2sgb2YgdGhlIHBhdGggdG8gd29ya2luZyBkaXJlY3RvcnkgYW5kIGhhcyBhIGxpc3Qgb2ZcbiAqIExhdW5jaGVySXRlbXMsIHdoaWNoIHRoZSBMYXVuY2hlciB3aWxsIHJlbmRlci5cbiAqL1xuZXhwb3J0IGNsYXNzIExhdW5jaGVyTW9kZWwgZXh0ZW5kcyBWRG9tTW9kZWwgaW1wbGVtZW50cyBJTGF1bmNoZXIge1xuICAvKipcbiAgICogQWRkIGEgY29tbWFuZCBpdGVtIHRvIHRoZSBsYXVuY2hlciwgYW5kIHRyaWdnZXIgcmUtcmVuZGVyIGV2ZW50IGZvciBwYXJlbnRcbiAgICogd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBzcGVjaWZpY2F0aW9uIG9wdGlvbnMgZm9yIGEgbGF1bmNoZXIgaXRlbS5cbiAgICpcbiAgICogQHJldHVybnMgQSBkaXNwb3NhYmxlIHRoYXQgd2lsbCByZW1vdmUgdGhlIGl0ZW0gZnJvbSBMYXVuY2hlciwgYW5kIHRyaWdnZXJcbiAgICogcmUtcmVuZGVyIGV2ZW50IGZvciBwYXJlbnQgd2lkZ2V0LlxuICAgKlxuICAgKi9cbiAgYWRkKG9wdGlvbnM6IElMYXVuY2hlci5JSXRlbU9wdGlvbnMpOiBJRGlzcG9zYWJsZSB7XG4gICAgLy8gQ3JlYXRlIGEgY29weSBvZiB0aGUgb3B0aW9ucyB0byBjaXJjdW12ZW50IG11dGF0aW9ucyB0byB0aGUgb3JpZ2luYWwuXG4gICAgY29uc3QgaXRlbSA9IFByaXZhdGUuY3JlYXRlSXRlbShvcHRpb25zKTtcblxuICAgIHRoaXMuX2l0ZW1zLnB1c2goaXRlbSk7XG4gICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuXG4gICAgcmV0dXJuIG5ldyBEaXNwb3NhYmxlRGVsZWdhdGUoKCkgPT4ge1xuICAgICAgQXJyYXlFeHQucmVtb3ZlRmlyc3RPZih0aGlzLl9pdGVtcywgaXRlbSk7XG4gICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJuIGFuIGl0ZXJhdG9yIG9mIGxhdW5jaGVyIGl0ZW1zLlxuICAgKi9cbiAgaXRlbXMoKTogSUl0ZXJhdG9yPElMYXVuY2hlci5JSXRlbU9wdGlvbnM+IHtcbiAgICByZXR1cm4gbmV3IEFycmF5SXRlcmF0b3IodGhpcy5faXRlbXMpO1xuICB9XG5cbiAgcHJpdmF0ZSBfaXRlbXM6IElMYXVuY2hlci5JSXRlbU9wdGlvbnNbXSA9IFtdO1xufVxuXG4vKipcbiAqIEEgdmlydHVhbC1ET00tYmFzZWQgd2lkZ2V0IGZvciB0aGUgTGF1bmNoZXIuXG4gKi9cbmV4cG9ydCBjbGFzcyBMYXVuY2hlciBleHRlbmRzIFZEb21SZW5kZXJlcjxMYXVuY2hlck1vZGVsPiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgbGF1bmNoZXIgd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogSUxhdW5jaGVyLklPcHRpb25zKSB7XG4gICAgc3VwZXIob3B0aW9ucy5tb2RlbCk7XG4gICAgdGhpcy5fY3dkID0gb3B0aW9ucy5jd2Q7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gb3B0aW9ucy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX3RyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICB0aGlzLl9jYWxsYmFjayA9IG9wdGlvbnMuY2FsbGJhY2s7XG4gICAgdGhpcy5fY29tbWFuZHMgPSBvcHRpb25zLmNvbW1hbmRzO1xuICAgIHRoaXMuYWRkQ2xhc3MoTEFVTkNIRVJfQ0xBU1MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjd2Qgb2YgdGhlIGxhdW5jaGVyLlxuICAgKi9cbiAgZ2V0IGN3ZCgpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLl9jd2Q7XG4gIH1cbiAgc2V0IGN3ZCh2YWx1ZTogc3RyaW5nKSB7XG4gICAgdGhpcy5fY3dkID0gdmFsdWU7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZXJlIGlzIGEgcGVuZGluZyBpdGVtIGJlaW5nIGxhdW5jaGVkLlxuICAgKi9cbiAgZ2V0IHBlbmRpbmcoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX3BlbmRpbmc7XG4gIH1cbiAgc2V0IHBlbmRpbmcodmFsdWU6IGJvb2xlYW4pIHtcbiAgICB0aGlzLl9wZW5kaW5nID0gdmFsdWU7XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIHRoZSBsYXVuY2hlciB0byB2aXJ0dWFsIERPTSBub2Rlcy5cbiAgICovXG4gIHByb3RlY3RlZCByZW5kZXIoKTogUmVhY3QuUmVhY3RFbGVtZW50PGFueT4gfCBudWxsIHtcbiAgICAvLyBCYWlsIGlmIHRoZXJlIGlzIG5vIG1vZGVsLlxuICAgIGlmICghdGhpcy5tb2RlbCkge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuXG4gICAgY29uc3Qga25vd25DYXRlZ29yaWVzID0gW1xuICAgICAgdGhpcy5fdHJhbnMuX18oJ05vdGVib29rJyksXG4gICAgICB0aGlzLl90cmFucy5fXygnQ29uc29sZScpLFxuICAgICAgdGhpcy5fdHJhbnMuX18oJ090aGVyJylcbiAgICBdO1xuICAgIGNvbnN0IGtlcm5lbENhdGVnb3JpZXMgPSBbXG4gICAgICB0aGlzLl90cmFucy5fXygnTm90ZWJvb2snKSxcbiAgICAgIHRoaXMuX3RyYW5zLl9fKCdDb25zb2xlJylcbiAgICBdO1xuXG4gICAgLy8gRmlyc3QgZ3JvdXAtYnkgY2F0ZWdvcmllc1xuICAgIGNvbnN0IGNhdGVnb3JpZXMgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuICAgIGVhY2godGhpcy5tb2RlbC5pdGVtcygpLCAoaXRlbSwgaW5kZXgpID0+IHtcbiAgICAgIGNvbnN0IGNhdCA9IGl0ZW0uY2F0ZWdvcnkgfHwgdGhpcy5fdHJhbnMuX18oJ090aGVyJyk7XG4gICAgICBpZiAoIShjYXQgaW4gY2F0ZWdvcmllcykpIHtcbiAgICAgICAgY2F0ZWdvcmllc1tjYXRdID0gW107XG4gICAgICB9XG4gICAgICBjYXRlZ29yaWVzW2NhdF0ucHVzaChpdGVtKTtcbiAgICB9KTtcbiAgICAvLyBXaXRoaW4gZWFjaCBjYXRlZ29yeSBzb3J0IGJ5IHJhbmtcbiAgICBmb3IgKGNvbnN0IGNhdCBpbiBjYXRlZ29yaWVzKSB7XG4gICAgICBjYXRlZ29yaWVzW2NhdF0gPSBjYXRlZ29yaWVzW2NhdF0uc29ydChcbiAgICAgICAgKGE6IElMYXVuY2hlci5JSXRlbU9wdGlvbnMsIGI6IElMYXVuY2hlci5JSXRlbU9wdGlvbnMpID0+IHtcbiAgICAgICAgICByZXR1cm4gUHJpdmF0ZS5zb3J0Q21wKGEsIGIsIHRoaXMuX2N3ZCwgdGhpcy5fY29tbWFuZHMpO1xuICAgICAgICB9XG4gICAgICApO1xuICAgIH1cblxuICAgIC8vIFZhcmlhYmxlIHRvIGhlbHAgY3JlYXRlIHNlY3Rpb25zXG4gICAgY29uc3Qgc2VjdGlvbnM6IFJlYWN0LlJlYWN0RWxlbWVudDxhbnk+W10gPSBbXTtcbiAgICBsZXQgc2VjdGlvbjogUmVhY3QuUmVhY3RFbGVtZW50PGFueT47XG5cbiAgICAvLyBBc3NlbWJsZSB0aGUgZmluYWwgb3JkZXJlZCBsaXN0IG9mIGNhdGVnb3JpZXMsIGJlZ2lubmluZyB3aXRoXG4gICAgLy8gS05PV05fQ0FURUdPUklFUy5cbiAgICBjb25zdCBvcmRlcmVkQ2F0ZWdvcmllczogc3RyaW5nW10gPSBbXTtcbiAgICBlYWNoKGtub3duQ2F0ZWdvcmllcywgKGNhdCwgaW5kZXgpID0+IHtcbiAgICAgIG9yZGVyZWRDYXRlZ29yaWVzLnB1c2goY2F0KTtcbiAgICB9KTtcbiAgICBmb3IgKGNvbnN0IGNhdCBpbiBjYXRlZ29yaWVzKSB7XG4gICAgICBpZiAoa25vd25DYXRlZ29yaWVzLmluZGV4T2YoY2F0KSA9PT0gLTEpIHtcbiAgICAgICAgb3JkZXJlZENhdGVnb3JpZXMucHVzaChjYXQpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIE5vdyBjcmVhdGUgdGhlIHNlY3Rpb25zIGZvciBlYWNoIGNhdGVnb3J5XG4gICAgb3JkZXJlZENhdGVnb3JpZXMuZm9yRWFjaChjYXQgPT4ge1xuICAgICAgaWYgKCFjYXRlZ29yaWVzW2NhdF0pIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgaXRlbSA9IGNhdGVnb3JpZXNbY2F0XVswXSBhcyBJTGF1bmNoZXIuSUl0ZW1PcHRpb25zO1xuICAgICAgY29uc3QgYXJncyA9IHsgLi4uaXRlbS5hcmdzLCBjd2Q6IHRoaXMuY3dkIH07XG4gICAgICBjb25zdCBrZXJuZWwgPSBrZXJuZWxDYXRlZ29yaWVzLmluZGV4T2YoY2F0KSA+IC0xO1xuXG4gICAgICAvLyBERVBSRUNBVEVEOiByZW1vdmUgX2ljb24gd2hlbiBsdW1pbm8gMi4wIGlzIGFkb3B0ZWRcbiAgICAgIC8vIGlmIGljb24gaXMgYWxpYXNpbmcgaWNvbkNsYXNzLCBkb24ndCB1c2UgaXRcbiAgICAgIGNvbnN0IGljb25DbGFzcyA9IHRoaXMuX2NvbW1hbmRzLmljb25DbGFzcyhpdGVtLmNvbW1hbmQsIGFyZ3MpO1xuICAgICAgY29uc3QgX2ljb24gPSB0aGlzLl9jb21tYW5kcy5pY29uKGl0ZW0uY29tbWFuZCwgYXJncyk7XG4gICAgICBjb25zdCBpY29uID0gX2ljb24gPT09IGljb25DbGFzcyA/IHVuZGVmaW5lZCA6IF9pY29uO1xuXG4gICAgICBpZiAoY2F0IGluIGNhdGVnb3JpZXMpIHtcbiAgICAgICAgc2VjdGlvbiA9IChcbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUxhdW5jaGVyLXNlY3Rpb25cIiBrZXk9e2NhdH0+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUxhdW5jaGVyLXNlY3Rpb25IZWFkZXJcIj5cbiAgICAgICAgICAgICAgPExhYkljb24ucmVzb2x2ZVJlYWN0XG4gICAgICAgICAgICAgICAgaWNvbj17aWNvbn1cbiAgICAgICAgICAgICAgICBpY29uQ2xhc3M9e2NsYXNzZXMoaWNvbkNsYXNzLCAnanAtSWNvbi1jb3ZlcicpfVxuICAgICAgICAgICAgICAgIHN0eWxlc2hlZXQ9XCJsYXVuY2hlclNlY3Rpb25cIlxuICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICA8aDIgY2xhc3NOYW1lPVwianAtTGF1bmNoZXItc2VjdGlvblRpdGxlXCI+e2NhdH08L2gyPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUxhdW5jaGVyLWNhcmRDb250YWluZXJcIj5cbiAgICAgICAgICAgICAge3RvQXJyYXkoXG4gICAgICAgICAgICAgICAgbWFwKGNhdGVnb3JpZXNbY2F0XSwgKGl0ZW06IElMYXVuY2hlci5JSXRlbU9wdGlvbnMpID0+IHtcbiAgICAgICAgICAgICAgICAgIHJldHVybiBDYXJkKFxuICAgICAgICAgICAgICAgICAgICBrZXJuZWwsXG4gICAgICAgICAgICAgICAgICAgIGl0ZW0sXG4gICAgICAgICAgICAgICAgICAgIHRoaXMsXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuX2NvbW1hbmRzLFxuICAgICAgICAgICAgICAgICAgICB0aGlzLl90cmFucyxcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5fY2FsbGJhY2tcbiAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuICAgICAgICBzZWN0aW9ucy5wdXNoKHNlY3Rpb24pO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gV3JhcCB0aGUgc2VjdGlvbnMgaW4gYm9keSBhbmQgY29udGVudCBkaXZzLlxuICAgIHJldHVybiAoXG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUxhdW5jaGVyLWJvZHlcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1MYXVuY2hlci1jb250ZW50XCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1MYXVuY2hlci1jd2RcIj5cbiAgICAgICAgICAgIDxoMz57dGhpcy5jd2R9PC9oMz5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICB7c2VjdGlvbnN9XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgKTtcbiAgfVxuXG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF9jb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5O1xuICBwcml2YXRlIF9jYWxsYmFjazogKHdpZGdldDogV2lkZ2V0KSA9PiB2b2lkO1xuICBwcml2YXRlIF9wZW5kaW5nID0gZmFsc2U7XG4gIHByaXZhdGUgX2N3ZCA9ICcnO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGBJTGF1bmNoZXJgIGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSUxhdW5jaGVyIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGEgTGF1bmNoZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgbW9kZWwgb2YgdGhlIGxhdW5jaGVyLlxuICAgICAqL1xuICAgIG1vZGVsOiBMYXVuY2hlck1vZGVsO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGN3ZCBvZiB0aGUgbGF1bmNoZXIuXG4gICAgICovXG4gICAgY3dkOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29tbWFuZCByZWdpc3RyeSB1c2VkIGJ5IHRoZSBsYXVuY2hlci5cbiAgICAgKi9cbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFwcGxpY2F0aW9uIGxhbmd1YWdlIHRyYW5zbGF0aW9uLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjYWxsYmFjayB1c2VkIHdoZW4gYW4gaXRlbSBpcyBsYXVuY2hlZC5cbiAgICAgKi9cbiAgICBjYWxsYmFjazogKHdpZGdldDogV2lkZ2V0KSA9PiB2b2lkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGEgbGF1bmNoZXIgaXRlbS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUl0ZW1PcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY29tbWFuZCBJRCBmb3IgdGhlIGxhdW5jaGVyIGl0ZW0uXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSWYgdGhlIGNvbW1hbmQncyBgZXhlY3V0ZWAgbWV0aG9kIHJldHVybnMgYSBgV2lkZ2V0YCBvclxuICAgICAqIGEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdpdGggYSBgV2lkZ2V0YCwgdGhlbiB0aGF0IHdpZGdldCB3aWxsXG4gICAgICogcmVwbGFjZSB0aGUgbGF1bmNoZXIgaW4gdGhlIHNhbWUgbG9jYXRpb24gb2YgdGhlIGFwcGxpY2F0aW9uXG4gICAgICogc2hlbGwuIElmIHRoZSBgZXhlY3V0ZWAgbWV0aG9kIGRvZXMgc29tZXRoaW5nIGVsc2VcbiAgICAgKiAoaS5lLiwgY3JlYXRlIGEgbW9kYWwgZGlhbG9nKSwgdGhlbiB0aGUgbGF1bmNoZXIgd2lsbCBub3QgYmVcbiAgICAgKiBkaXNwb3NlZC5cbiAgICAgKi9cbiAgICBjb21tYW5kOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXJndW1lbnRzIGdpdmVuIHRvIHRoZSBjb21tYW5kIGZvclxuICAgICAqIGNyZWF0aW5nIHRoZSBsYXVuY2hlciBpdGVtLlxuICAgICAqXG4gICAgICogIyMjIE5vdGVzXG4gICAgICogVGhlIGxhdW5jaGVyIHdpbGwgYWxzbyBhZGQgdGhlIGN1cnJlbnQgd29ya2luZ1xuICAgICAqIGRpcmVjdG9yeSBvZiB0aGUgZmlsZWJyb3dzZXIgaW4gdGhlIGBjd2RgIGZpZWxkXG4gICAgICogb2YgdGhlIGFyZ3MsIHdoaWNoIGEgY29tbWFuZCBtYXkgdXNlIHRvIGNyZWF0ZVxuICAgICAqIHRoZSBhY3Rpdml0eSB3aXRoIHJlc3BlY3QgdG8gdGhlIHJpZ2h0IGRpcmVjdG9yeS5cbiAgICAgKi9cbiAgICBhcmdzPzogUmVhZG9ubHlKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNhdGVnb3J5IGZvciB0aGUgbGF1bmNoZXIgaXRlbS5cbiAgICAgKlxuICAgICAqIFRoZSBkZWZhdWx0IHZhbHVlIGlzIGFuIGVtcHR5IHN0cmluZy5cbiAgICAgKi9cbiAgICBjYXRlZ29yeT86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSByYW5rIGZvciB0aGUgbGF1bmNoZXIgaXRlbS5cbiAgICAgKlxuICAgICAqIFRoZSByYW5rIGlzIHVzZWQgd2hlbiBvcmRlcmluZyBsYXVuY2hlciBpdGVtcyBmb3IgZGlzcGxheS4gQWZ0ZXIgZ3JvdXBpbmdcbiAgICAgKiBpbnRvIGNhdGVnb3JpZXMsIGl0ZW1zIGFyZSBzb3J0ZWQgaW4gdGhlIGZvbGxvd2luZyBvcmRlcjpcbiAgICAgKiAgIDEuIFJhbmsgKGxvd2VyIGlzIGJldHRlcilcbiAgICAgKiAgIDMuIERpc3BsYXkgTmFtZSAobG9jYWxlIG9yZGVyKVxuICAgICAqXG4gICAgICogVGhlIGRlZmF1bHQgcmFuayBpcyBgSW5maW5pdHlgLlxuICAgICAqL1xuICAgIHJhbms/OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBGb3IgaXRlbXMgdGhhdCBoYXZlIGEga2VybmVsIGFzc29jaWF0ZWQgd2l0aCB0aGVtLCB0aGUgVVJMIG9mIHRoZSBrZXJuZWxcbiAgICAgKiBpY29uLlxuICAgICAqXG4gICAgICogVGhpcyBpcyBub3QgYSBDU1MgY2xhc3MsIGJ1dCB0aGUgVVJMIHRoYXQgcG9pbnRzIHRvIHRoZSBpY29uIGluIHRoZSBrZXJuZWxcbiAgICAgKiBzcGVjLlxuICAgICAqL1xuICAgIGtlcm5lbEljb25Vcmw/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBNZXRhZGF0YSBhYm91dCB0aGUgaXRlbS4gIFRoaXMgY2FuIGJlIHVzZWQgYnkgdGhlIGxhdW5jaGVyIHRvXG4gICAgICogYWZmZWN0IGhvdyB0aGUgaXRlbSBpcyBkaXNwbGF5ZWQuXG4gICAgICovXG4gICAgbWV0YWRhdGE/OiBSZWFkb25seUpTT05PYmplY3Q7XG4gIH1cbn1cblxuLyoqXG4gKiBBIHB1cmUgdHN4IGNvbXBvbmVudCBmb3IgYSBsYXVuY2hlciBjYXJkLlxuICpcbiAqIEBwYXJhbSBrZXJuZWwgLSB3aGV0aGVyIHRoZSBpdGVtIHRha2VzIHVzZXMgYSBrZXJuZWwuXG4gKlxuICogQHBhcmFtIGl0ZW0gLSB0aGUgbGF1bmNoZXIgaXRlbSB0byByZW5kZXIuXG4gKlxuICogQHBhcmFtIGxhdW5jaGVyIC0gdGhlIExhdW5jaGVyIGluc3RhbmNlIHRvIHdoaWNoIHRoaXMgaXMgYWRkZWQuXG4gKlxuICogQHBhcmFtIGxhdW5jaGVyQ2FsbGJhY2sgLSBhIGNhbGxiYWNrIHRvIGNhbGwgYWZ0ZXIgYW4gaXRlbSBoYXMgYmVlbiBsYXVuY2hlZC5cbiAqXG4gKiBAcmV0dXJucyBhIHZkb20gYFZpcnR1YWxFbGVtZW50YCBmb3IgdGhlIGxhdW5jaGVyIGNhcmQuXG4gKi9cbmZ1bmN0aW9uIENhcmQoXG4gIGtlcm5lbDogYm9vbGVhbixcbiAgaXRlbTogSUxhdW5jaGVyLklJdGVtT3B0aW9ucyxcbiAgbGF1bmNoZXI6IExhdW5jaGVyLFxuICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGUsXG4gIGxhdW5jaGVyQ2FsbGJhY2s6ICh3aWRnZXQ6IFdpZGdldCkgPT4gdm9pZFxuKTogUmVhY3QuUmVhY3RFbGVtZW50PGFueT4ge1xuICAvLyBHZXQgc29tZSBwcm9wZXJ0aWVzIG9mIHRoZSBjb21tYW5kXG4gIGNvbnN0IGNvbW1hbmQgPSBpdGVtLmNvbW1hbmQ7XG4gIGNvbnN0IGFyZ3MgPSB7IC4uLml0ZW0uYXJncywgY3dkOiBsYXVuY2hlci5jd2QgfTtcbiAgY29uc3QgY2FwdGlvbiA9IGNvbW1hbmRzLmNhcHRpb24oY29tbWFuZCwgYXJncyk7XG4gIGNvbnN0IGxhYmVsID0gY29tbWFuZHMubGFiZWwoY29tbWFuZCwgYXJncyk7XG4gIGNvbnN0IHRpdGxlID0ga2VybmVsID8gbGFiZWwgOiBjYXB0aW9uIHx8IGxhYmVsO1xuXG4gIC8vIEJ1aWxkIHRoZSBvbmNsaWNrIGhhbmRsZXIuXG4gIGNvbnN0IG9uY2xpY2sgPSAoKSA9PiB7XG4gICAgLy8gSWYgYW4gaXRlbSBoYXMgYWxyZWFkeSBiZWVuIGxhdW5jaGVkLFxuICAgIC8vIGRvbid0IHRyeSB0byBsYXVuY2ggYW5vdGhlci5cbiAgICBpZiAobGF1bmNoZXIucGVuZGluZyA9PT0gdHJ1ZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBsYXVuY2hlci5wZW5kaW5nID0gdHJ1ZTtcbiAgICB2b2lkIGNvbW1hbmRzXG4gICAgICAuZXhlY3V0ZShjb21tYW5kLCB7XG4gICAgICAgIC4uLml0ZW0uYXJncyxcbiAgICAgICAgY3dkOiBsYXVuY2hlci5jd2RcbiAgICAgIH0pXG4gICAgICAudGhlbih2YWx1ZSA9PiB7XG4gICAgICAgIGxhdW5jaGVyLnBlbmRpbmcgPSBmYWxzZTtcbiAgICAgICAgaWYgKHZhbHVlIGluc3RhbmNlb2YgV2lkZ2V0KSB7XG4gICAgICAgICAgbGF1bmNoZXJDYWxsYmFjayh2YWx1ZSk7XG4gICAgICAgICAgbGF1bmNoZXIuZGlzcG9zZSgpO1xuICAgICAgICB9XG4gICAgICB9KVxuICAgICAgLmNhdGNoKGVyciA9PiB7XG4gICAgICAgIGxhdW5jaGVyLnBlbmRpbmcgPSBmYWxzZTtcbiAgICAgICAgdm9pZCBzaG93RXJyb3JNZXNzYWdlKHRyYW5zLl9wKCdFcnJvcicsICdMYXVuY2hlciBFcnJvcicpLCBlcnIpO1xuICAgICAgfSk7XG4gIH07XG5cbiAgLy8gV2l0aCB0YWJpbmRleCB3b3JraW5nLCB5b3UgY2FuIG5vdyBwaWNrIGEga2VybmVsIGJ5IHRhYmJpbmcgYXJvdW5kIGFuZFxuICAvLyBwcmVzc2luZyBFbnRlci5cbiAgY29uc3Qgb25rZXlwcmVzcyA9IChldmVudDogUmVhY3QuS2V5Ym9hcmRFdmVudCkgPT4ge1xuICAgIGlmIChldmVudC5rZXkgPT09ICdFbnRlcicpIHtcbiAgICAgIG9uY2xpY2soKTtcbiAgICB9XG4gIH07XG5cbiAgLy8gREVQUkVDQVRFRDogcmVtb3ZlIF9pY29uIHdoZW4gbHVtaW5vIDIuMCBpcyBhZG9wdGVkXG4gIC8vIGlmIGljb24gaXMgYWxpYXNpbmcgaWNvbkNsYXNzLCBkb24ndCB1c2UgaXRcbiAgY29uc3QgaWNvbkNsYXNzID0gY29tbWFuZHMuaWNvbkNsYXNzKGNvbW1hbmQsIGFyZ3MpO1xuICBjb25zdCBfaWNvbiA9IGNvbW1hbmRzLmljb24oY29tbWFuZCwgYXJncyk7XG4gIGNvbnN0IGljb24gPSBfaWNvbiA9PT0gaWNvbkNsYXNzID8gdW5kZWZpbmVkIDogX2ljb247XG5cbiAgLy8gUmV0dXJuIHRoZSBWRE9NIGVsZW1lbnQuXG4gIHJldHVybiAoXG4gICAgPGRpdlxuICAgICAgY2xhc3NOYW1lPVwianAtTGF1bmNoZXJDYXJkXCJcbiAgICAgIHRpdGxlPXt0aXRsZX1cbiAgICAgIG9uQ2xpY2s9e29uY2xpY2t9XG4gICAgICBvbktleVByZXNzPXtvbmtleXByZXNzfVxuICAgICAgdGFiSW5kZXg9ezB9XG4gICAgICBkYXRhLWNhdGVnb3J5PXtpdGVtLmNhdGVnb3J5IHx8IHRyYW5zLl9fKCdPdGhlcicpfVxuICAgICAga2V5PXtQcml2YXRlLmtleVByb3BlcnR5LmdldChpdGVtKX1cbiAgICA+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUxhdW5jaGVyQ2FyZC1pY29uXCI+XG4gICAgICAgIHtrZXJuZWwgPyAoXG4gICAgICAgICAgaXRlbS5rZXJuZWxJY29uVXJsID8gKFxuICAgICAgICAgICAgPGltZyBzcmM9e2l0ZW0ua2VybmVsSWNvblVybH0gY2xhc3NOYW1lPVwianAtTGF1bmNoZXIta2VybmVsSWNvblwiIC8+XG4gICAgICAgICAgKSA6IChcbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtTGF1bmNoZXJDYXJkLW5vS2VybmVsSWNvblwiPlxuICAgICAgICAgICAgICB7bGFiZWxbMF0udG9VcHBlckNhc2UoKX1cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIClcbiAgICAgICAgKSA6IChcbiAgICAgICAgICA8TGFiSWNvbi5yZXNvbHZlUmVhY3RcbiAgICAgICAgICAgIGljb249e2ljb259XG4gICAgICAgICAgICBpY29uQ2xhc3M9e2NsYXNzZXMoaWNvbkNsYXNzLCAnanAtSWNvbi1jb3ZlcicpfVxuICAgICAgICAgICAgc3R5bGVzaGVldD1cImxhdW5jaGVyQ2FyZFwiXG4gICAgICAgICAgLz5cbiAgICAgICAgKX1cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1MYXVuY2hlckNhcmQtbGFiZWxcIiB0aXRsZT17dGl0bGV9PlxuICAgICAgICA8cD57bGFiZWx9PC9wPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+XG4gICk7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgbW9kdWxlIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQW4gaW5jcmVtZW50aW5nIGNvdW50ZXIgZm9yIGtleXMuXG4gICAqL1xuICBsZXQgaWQgPSAwO1xuXG4gIC8qKlxuICAgKiBBbiBhdHRhY2hlZCBwcm9wZXJ0eSBmb3IgYW4gaXRlbSdzIGtleS5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBrZXlQcm9wZXJ0eSA9IG5ldyBBdHRhY2hlZFByb3BlcnR5PFxuICAgIElMYXVuY2hlci5JSXRlbU9wdGlvbnMsXG4gICAgbnVtYmVyXG4gID4oe1xuICAgIG5hbWU6ICdrZXknLFxuICAgIGNyZWF0ZTogKCkgPT4gaWQrK1xuICB9KTtcblxuICAvKipcbiAgICogQ3JlYXRlIGEgZnVsbHkgc3BlY2lmaWVkIGl0ZW0gZ2l2ZW4gaXRlbSBvcHRpb25zLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZUl0ZW0oXG4gICAgb3B0aW9uczogSUxhdW5jaGVyLklJdGVtT3B0aW9uc1xuICApOiBJTGF1bmNoZXIuSUl0ZW1PcHRpb25zIHtcbiAgICByZXR1cm4ge1xuICAgICAgLi4ub3B0aW9ucyxcbiAgICAgIGNhdGVnb3J5OiBvcHRpb25zLmNhdGVnb3J5IHx8ICcnLFxuICAgICAgcmFuazogb3B0aW9ucy5yYW5rICE9PSB1bmRlZmluZWQgPyBvcHRpb25zLnJhbmsgOiBJbmZpbml0eVxuICAgIH07XG4gIH1cblxuICAvKipcbiAgICogQSBzb3J0IGNvbXBhcmlzb24gZnVuY3Rpb24gZm9yIGEgbGF1bmNoZXIgaXRlbS5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBzb3J0Q21wKFxuICAgIGE6IElMYXVuY2hlci5JSXRlbU9wdGlvbnMsXG4gICAgYjogSUxhdW5jaGVyLklJdGVtT3B0aW9ucyxcbiAgICBjd2Q6IHN0cmluZyxcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5XG4gICk6IG51bWJlciB7XG4gICAgLy8gRmlyc3QsIGNvbXBhcmUgYnkgcmFuay5cbiAgICBjb25zdCByMSA9IGEucmFuaztcbiAgICBjb25zdCByMiA9IGIucmFuaztcbiAgICBpZiAocjEgIT09IHIyICYmIHIxICE9PSB1bmRlZmluZWQgJiYgcjIgIT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuIHIxIDwgcjIgPyAtMSA6IDE7IC8vIEluZmluaXR5IHNhZmVcbiAgICB9XG5cbiAgICAvLyBGaW5hbGx5LCBjb21wYXJlIGJ5IGRpc3BsYXkgbmFtZS5cbiAgICBjb25zdCBhTGFiZWwgPSBjb21tYW5kcy5sYWJlbChhLmNvbW1hbmQsIHsgLi4uYS5hcmdzLCBjd2QgfSk7XG4gICAgY29uc3QgYkxhYmVsID0gY29tbWFuZHMubGFiZWwoYi5jb21tYW5kLCB7IC4uLmIuYXJncywgY3dkIH0pO1xuICAgIHJldHVybiBhTGFiZWwubG9jYWxlQ29tcGFyZShiTGFiZWwpO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9