(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_csvviewer-extension_lib_index_js"],{

/***/ "../packages/csvviewer-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../packages/csvviewer-extension/lib/index.js ***!
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
/* harmony import */ var _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/csvviewer */ "webpack/sharing/consume/default/@jupyterlab/csvviewer/@jupyterlab/csvviewer");
/* harmony import */ var _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/documentsearch */ "webpack/sharing/consume/default/@jupyterlab/documentsearch/@jupyterlab/documentsearch");
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid/@lumino/datagrid");
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_datagrid__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _searchprovider__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./searchprovider */ "../packages/csvviewer-extension/lib/searchprovider.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module csvviewer-extension
 */








/**
 * The name of the factories that creates widgets.
 */
const FACTORY_CSV = 'CSVTable';
const FACTORY_TSV = 'TSVTable';
/**
 * The CSV file handler extension.
 */
const csv = {
    activate: activateCsv,
    id: '@jupyterlab/csvviewer-extension:csv',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_4__.IMainMenu,
        _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_3__.ISearchProviderRegistry
    ],
    autoStart: true
};
/**
 * The TSV file handler extension.
 */
const tsv = {
    activate: activateTsv,
    id: '@jupyterlab/csvviewer-extension:tsv',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_4__.IMainMenu,
        _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_3__.ISearchProviderRegistry
    ],
    autoStart: true
};
/**
 * Connect menu entries for find and go to line.
 */
function addMenuEntries(mainMenu, tracker, translator) {
    const trans = translator.load('jupyterlab');
    // Add go to line capability to the edit menu.
    mainMenu.editMenu.goToLiners.add({
        tracker,
        goToLine: (widget) => {
            return _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getNumber({
                title: trans.__('Go to Line'),
                value: 0
            }).then(value => {
                if (value.button.accept && value.value !== null) {
                    widget.content.goToLine(value.value);
                }
            });
        }
    });
}
/**
 * Activate cssviewer extension for CSV files
 */
function activateCsv(app, translator, restorer, themeManager, mainMenu, searchregistry) {
    const factory = new _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_2__.CSVViewerFactory({
        name: FACTORY_CSV,
        fileTypes: ['csv'],
        defaultFor: ['csv'],
        readOnly: true,
        translator
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'csvviewer'
    });
    // The current styles for the data grids.
    let style = Private.LIGHT_STYLE;
    let rendererConfig = Private.LIGHT_TEXT_CONFIG;
    if (restorer) {
        // Handle state restoration.
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY_CSV }),
            name: widget => widget.context.path
        });
    }
    app.docRegistry.addWidgetFactory(factory);
    const ft = app.docRegistry.getFileType('csv');
    factory.widgetCreated.connect((sender, widget) => {
        // Track the widget.
        void tracker.add(widget);
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        if (ft) {
            widget.title.icon = ft.icon;
            widget.title.iconClass = ft.iconClass;
            widget.title.iconLabel = ft.iconLabel;
        }
        // Set the theme for the new widget.
        widget.content.style = style;
        widget.content.rendererConfig = rendererConfig;
    });
    // Keep the themes up-to-date.
    const updateThemes = () => {
        const isLight = themeManager && themeManager.theme
            ? themeManager.isLight(themeManager.theme)
            : true;
        style = isLight ? Private.LIGHT_STYLE : Private.DARK_STYLE;
        rendererConfig = isLight
            ? Private.LIGHT_TEXT_CONFIG
            : Private.DARK_TEXT_CONFIG;
        tracker.forEach(grid => {
            grid.content.style = style;
            grid.content.rendererConfig = rendererConfig;
        });
    };
    if (themeManager) {
        themeManager.themeChanged.connect(updateThemes);
    }
    if (mainMenu) {
        addMenuEntries(mainMenu, tracker, translator);
    }
    if (searchregistry) {
        searchregistry.register('csv', _searchprovider__WEBPACK_IMPORTED_MODULE_7__.CSVSearchProvider);
    }
}
/**
 * Activate cssviewer extension for TSV files
 */
function activateTsv(app, translator, restorer, themeManager, mainMenu, searchregistry) {
    const factory = new _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_2__.TSVViewerFactory({
        name: FACTORY_TSV,
        fileTypes: ['tsv'],
        defaultFor: ['tsv'],
        readOnly: true,
        translator
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'tsvviewer'
    });
    // The current styles for the data grids.
    let style = Private.LIGHT_STYLE;
    let rendererConfig = Private.LIGHT_TEXT_CONFIG;
    if (restorer) {
        // Handle state restoration.
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY_TSV }),
            name: widget => widget.context.path
        });
    }
    app.docRegistry.addWidgetFactory(factory);
    const ft = app.docRegistry.getFileType('tsv');
    factory.widgetCreated.connect((sender, widget) => {
        // Track the widget.
        void tracker.add(widget);
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        if (ft) {
            widget.title.icon = ft.icon;
            widget.title.iconClass = ft.iconClass;
            widget.title.iconLabel = ft.iconLabel;
        }
        // Set the theme for the new widget.
        widget.content.style = style;
        widget.content.rendererConfig = rendererConfig;
    });
    // Keep the themes up-to-date.
    const updateThemes = () => {
        const isLight = themeManager && themeManager.theme
            ? themeManager.isLight(themeManager.theme)
            : true;
        style = isLight ? Private.LIGHT_STYLE : Private.DARK_STYLE;
        rendererConfig = isLight
            ? Private.LIGHT_TEXT_CONFIG
            : Private.DARK_TEXT_CONFIG;
        tracker.forEach(grid => {
            grid.content.style = style;
            grid.content.rendererConfig = rendererConfig;
        });
    };
    if (themeManager) {
        themeManager.themeChanged.connect(updateThemes);
    }
    if (mainMenu) {
        addMenuEntries(mainMenu, tracker, translator);
    }
    if (searchregistry) {
        searchregistry.register('tsv', _searchprovider__WEBPACK_IMPORTED_MODULE_7__.CSVSearchProvider);
    }
}
/**
 * Export the plugins as default.
 */
const plugins = [csv, tsv];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * The light theme for the data grid.
     */
    Private.LIGHT_STYLE = Object.assign(Object.assign({}, _lumino_datagrid__WEBPACK_IMPORTED_MODULE_6__.DataGrid.defaultStyle), { voidColor: '#F3F3F3', backgroundColor: 'white', headerBackgroundColor: '#EEEEEE', gridLineColor: 'rgba(20, 20, 20, 0.15)', headerGridLineColor: 'rgba(20, 20, 20, 0.25)', rowBackgroundColor: i => (i % 2 === 0 ? '#F5F5F5' : 'white') });
    /**
     * The dark theme for the data grid.
     */
    Private.DARK_STYLE = Object.assign(Object.assign({}, _lumino_datagrid__WEBPACK_IMPORTED_MODULE_6__.DataGrid.defaultStyle), { voidColor: 'black', backgroundColor: '#111111', headerBackgroundColor: '#424242', gridLineColor: 'rgba(235, 235, 235, 0.15)', headerGridLineColor: 'rgba(235, 235, 235, 0.25)', rowBackgroundColor: i => (i % 2 === 0 ? '#212121' : '#111111') });
    /**
     * The light config for the data grid renderer.
     */
    Private.LIGHT_TEXT_CONFIG = {
        textColor: '#111111',
        matchBackgroundColor: '#FFFFE0',
        currentMatchBackgroundColor: '#FFFF00',
        horizontalAlignment: 'right'
    };
    /**
     * The dark config for the data grid renderer.
     */
    Private.DARK_TEXT_CONFIG = {
        textColor: '#F5F5F5',
        matchBackgroundColor: '#838423',
        currentMatchBackgroundColor: '#A3807A',
        horizontalAlignment: 'right'
    };
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/csvviewer-extension/lib/searchprovider.js":
/*!*************************************************************!*\
  !*** ../packages/csvviewer-extension/lib/searchprovider.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CSVSearchProvider": () => (/* binding */ CSVSearchProvider)
/* harmony export */ });
/* harmony import */ var _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/csvviewer */ "webpack/sharing/consume/default/@jupyterlab/csvviewer/@jupyterlab/csvviewer");
/* harmony import */ var _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



class CSVSearchProvider {
    constructor() {
        /**
         * The same list of matches provided by the startQuery promise resolution
         */
        this.matches = [];
        /**
         * The current index of the selected match.
         */
        this.currentMatchIndex = null;
        /**
         * Set to true if the widget under search is read-only, false
         * if it is editable.  Will be used to determine whether to show
         * the replace option.
         */
        this.isReadOnly = true;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
    }
    /**
     * Report whether or not this provider has the ability to search on the given object
     */
    static canSearchOn(domain) {
        // check to see if the CSVSearchProvider can search on the
        // first cell, false indicates another editor is present
        return (domain instanceof _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget && domain.content instanceof _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0__.CSVViewer);
    }
    /**
     * Get an initial query value if applicable so that it can be entered
     * into the search box as an initial query
     *
     * @returns Initial value used to populate the search box.
     */
    getInitialQuery(searchTarget) {
        // CSV Viewer does not support selection
        return null;
    }
    /**
     * Initialize the search using the provided options.  Should update the UI
     * to highlight all matches and "select" whatever the first match should be.
     *
     * @param query A RegExp to be use to perform the search
     * @param searchTarget The widget to be searched
     *
     * @returns A promise that resolves with a list of all matches
     */
    async startQuery(query, searchTarget) {
        this._target = searchTarget;
        this._query = query;
        searchTarget.content.searchService.find(query);
        return this.matches;
    }
    /**
     * Clears state of a search provider to prepare for startQuery to be called
     * in order to start a new query or refresh an existing one.
     *
     * @returns A promise that resolves when the search provider is ready to
     * begin a new search.
     */
    async endQuery() {
        this._target.content.searchService.clear();
    }
    /**
     * Resets UI state as it was before the search process began.  Cleans up and
     * disposes of all internal state.
     *
     * @returns A promise that resolves when all state has been cleaned up.
     */
    async endSearch() {
        this._target.content.searchService.clear();
    }
    /**
     * Move the current match indicator to the next match.
     *
     * @returns A promise that resolves once the action has completed.
     */
    async highlightNext() {
        this._target.content.searchService.find(this._query);
        return undefined;
    }
    /**
     * Move the current match indicator to the previous match.
     *
     * @returns A promise that resolves once the action has completed.
     */
    async highlightPrevious() {
        this._target.content.searchService.find(this._query, true);
        return undefined;
    }
    /**
     * Replace the currently selected match with the provided text
     * Not implemented in the CSV viewer as it is read-only.
     *
     * @returns A promise that resolves once the action has completed.
     */
    async replaceCurrentMatch(newText) {
        return false;
    }
    /**
     * Replace all matches in the notebook with the provided text
     * Not implemented in the CSV viewer as it is read-only.
     *
     * @returns A promise that resolves once the action has completed.
     */
    async replaceAllMatches(newText) {
        return false;
    }
    /**
     * Signal indicating that something in the search has changed, so the UI should update
     */
    get changed() {
        return this._changed;
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY3N2dmlld2VyLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NzdnZpZXdlci1leHRlbnNpb24vc3JjL3NlYXJjaHByb3ZpZGVyLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU04QjtBQUtIO0FBTUM7QUFFc0M7QUFDVDtBQUNOO0FBQ1Y7QUFDUztBQUVyRDs7R0FFRztBQUNILE1BQU0sV0FBVyxHQUFHLFVBQVUsQ0FBQztBQUMvQixNQUFNLFdBQVcsR0FBRyxVQUFVLENBQUM7QUFFL0I7O0dBRUc7QUFDSCxNQUFNLEdBQUcsR0FBZ0M7SUFDdkMsUUFBUSxFQUFFLFdBQVc7SUFDckIsRUFBRSxFQUFFLHFDQUFxQztJQUN6QyxRQUFRLEVBQUUsQ0FBQyxnRUFBVyxDQUFDO0lBQ3ZCLFFBQVEsRUFBRTtRQUNSLG9FQUFlO1FBQ2YsK0RBQWE7UUFDYiwyREFBUztRQUNULCtFQUF1QjtLQUN4QjtJQUNELFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRjs7R0FFRztBQUNILE1BQU0sR0FBRyxHQUFnQztJQUN2QyxRQUFRLEVBQUUsV0FBVztJQUNyQixFQUFFLEVBQUUscUNBQXFDO0lBQ3pDLFFBQVEsRUFBRSxDQUFDLGdFQUFXLENBQUM7SUFDdkIsUUFBUSxFQUFFO1FBQ1Isb0VBQWU7UUFDZiwrREFBYTtRQUNiLDJEQUFTO1FBQ1QsK0VBQXVCO0tBQ3hCO0lBQ0QsU0FBUyxFQUFFLElBQUk7Q0FDaEIsQ0FBQztBQUVGOztHQUVHO0FBQ0gsU0FBUyxjQUFjLENBQ3JCLFFBQW1CLEVBQ25CLE9BQWtELEVBQ2xELFVBQXVCO0lBRXZCLE1BQU0sS0FBSyxH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QztJQUNmLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksT0FBTztRQUNULE9BQU8sSUFBSSxDQUFDLFFBQVEsQ0FBQztJQUN2QixDQUFDO0NBc0JGIiwiZmlsZSI6InBhY2thZ2VzX2NzdnZpZXdlci1leHRlbnNpb25fbGliX2luZGV4X2pzLmIyYmVjMTcyZjFiNTVjMDA1YTFlLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY3N2dmlld2VyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYXlvdXRSZXN0b3JlcixcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgSW5wdXREaWFsb2csXG4gIElUaGVtZU1hbmFnZXIsXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgQ1NWVmlld2VyLFxuICBDU1ZWaWV3ZXJGYWN0b3J5LFxuICBUZXh0UmVuZGVyQ29uZmlnLFxuICBUU1ZWaWV3ZXJGYWN0b3J5XG59IGZyb20gJ0BqdXB5dGVybGFiL2NzdnZpZXdlcic7XG5pbXBvcnQgeyBJRG9jdW1lbnRXaWRnZXQgfSBmcm9tICdAanVweXRlcmxhYi9kb2NyZWdpc3RyeSc7XG5pbXBvcnQgeyBJU2VhcmNoUHJvdmlkZXJSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3VtZW50c2VhcmNoJztcbmltcG9ydCB7IElFZGl0TWVudSwgSU1haW5NZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvbWFpbm1lbnUnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBEYXRhR3JpZCB9IGZyb20gJ0BsdW1pbm8vZGF0YWdyaWQnO1xuaW1wb3J0IHsgQ1NWU2VhcmNoUHJvdmlkZXIgfSBmcm9tICcuL3NlYXJjaHByb3ZpZGVyJztcblxuLyoqXG4gKiBUaGUgbmFtZSBvZiB0aGUgZmFjdG9yaWVzIHRoYXQgY3JlYXRlcyB3aWRnZXRzLlxuICovXG5jb25zdCBGQUNUT1JZX0NTViA9ICdDU1ZUYWJsZSc7XG5jb25zdCBGQUNUT1JZX1RTViA9ICdUU1ZUYWJsZSc7XG5cbi8qKlxuICogVGhlIENTViBmaWxlIGhhbmRsZXIgZXh0ZW5zaW9uLlxuICovXG5jb25zdCBjc3Y6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgYWN0aXZhdGU6IGFjdGl2YXRlQ3N2LFxuICBpZDogJ0BqdXB5dGVybGFiL2NzdnZpZXdlci1leHRlbnNpb246Y3N2JyxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbXG4gICAgSUxheW91dFJlc3RvcmVyLFxuICAgIElUaGVtZU1hbmFnZXIsXG4gICAgSU1haW5NZW51LFxuICAgIElTZWFyY2hQcm92aWRlclJlZ2lzdHJ5XG4gIF0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuLyoqXG4gKiBUaGUgVFNWIGZpbGUgaGFuZGxlciBleHRlbnNpb24uXG4gKi9cbmNvbnN0IHRzdjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBhY3RpdmF0ZTogYWN0aXZhdGVUc3YsXG4gIGlkOiAnQGp1cHl0ZXJsYWIvY3N2dmlld2VyLWV4dGVuc2lvbjp0c3YnLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtcbiAgICBJTGF5b3V0UmVzdG9yZXIsXG4gICAgSVRoZW1lTWFuYWdlcixcbiAgICBJTWFpbk1lbnUsXG4gICAgSVNlYXJjaFByb3ZpZGVyUmVnaXN0cnlcbiAgXSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIENvbm5lY3QgbWVudSBlbnRyaWVzIGZvciBmaW5kIGFuZCBnbyB0byBsaW5lLlxuICovXG5mdW5jdGlvbiBhZGRNZW51RW50cmllcyhcbiAgbWFpbk1lbnU6IElNYWluTWVudSxcbiAgdHJhY2tlcjogV2lkZ2V0VHJhY2tlcjxJRG9jdW1lbnRXaWRnZXQ8Q1NWVmlld2VyPj4sXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4pIHtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgLy8gQWRkIGdvIHRvIGxpbmUgY2FwYWJpbGl0eSB0byB0aGUgZWRpdCBtZW51LlxuICBtYWluTWVudS5lZGl0TWVudS5nb1RvTGluZXJzLmFkZCh7XG4gICAgdHJhY2tlcixcbiAgICBnb1RvTGluZTogKHdpZGdldDogSURvY3VtZW50V2lkZ2V0PENTVlZpZXdlcj4pID0+IHtcbiAgICAgIHJldHVybiBJbnB1dERpYWxvZy5nZXROdW1iZXIoe1xuICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0dvIHRvIExpbmUnKSxcbiAgICAgICAgdmFsdWU6IDBcbiAgICAgIH0pLnRoZW4odmFsdWUgPT4ge1xuICAgICAgICBpZiAodmFsdWUuYnV0dG9uLmFjY2VwdCAmJiB2YWx1ZS52YWx1ZSAhPT0gbnVsbCkge1xuICAgICAgICAgIHdpZGdldC5jb250ZW50LmdvVG9MaW5lKHZhbHVlLnZhbHVlKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuICB9IGFzIElFZGl0TWVudS5JR29Ub0xpbmVyPElEb2N1bWVudFdpZGdldDxDU1ZWaWV3ZXI+Pik7XG59XG5cbi8qKlxuICogQWN0aXZhdGUgY3Nzdmlld2VyIGV4dGVuc2lvbiBmb3IgQ1NWIGZpbGVzXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlQ3N2KFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIHJlc3RvcmVyOiBJTGF5b3V0UmVzdG9yZXIgfCBudWxsLFxuICB0aGVtZU1hbmFnZXI6IElUaGVtZU1hbmFnZXIgfCBudWxsLFxuICBtYWluTWVudTogSU1haW5NZW51IHwgbnVsbCxcbiAgc2VhcmNocmVnaXN0cnk6IElTZWFyY2hQcm92aWRlclJlZ2lzdHJ5IHwgbnVsbFxuKTogdm9pZCB7XG4gIGNvbnN0IGZhY3RvcnkgPSBuZXcgQ1NWVmlld2VyRmFjdG9yeSh7XG4gICAgbmFtZTogRkFDVE9SWV9DU1YsXG4gICAgZmlsZVR5cGVzOiBbJ2NzdiddLFxuICAgIGRlZmF1bHRGb3I6IFsnY3N2J10sXG4gICAgcmVhZE9ubHk6IHRydWUsXG4gICAgdHJhbnNsYXRvclxuICB9KTtcbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxDU1ZWaWV3ZXI+Pih7XG4gICAgbmFtZXNwYWNlOiAnY3N2dmlld2VyJ1xuICB9KTtcblxuICAvLyBUaGUgY3VycmVudCBzdHlsZXMgZm9yIHRoZSBkYXRhIGdyaWRzLlxuICBsZXQgc3R5bGU6IERhdGFHcmlkLlN0eWxlID0gUHJpdmF0ZS5MSUdIVF9TVFlMRTtcbiAgbGV0IHJlbmRlcmVyQ29uZmlnOiBUZXh0UmVuZGVyQ29uZmlnID0gUHJpdmF0ZS5MSUdIVF9URVhUX0NPTkZJRztcblxuICBpZiAocmVzdG9yZXIpIHtcbiAgICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gICAgdm9pZCByZXN0b3Jlci5yZXN0b3JlKHRyYWNrZXIsIHtcbiAgICAgIGNvbW1hbmQ6ICdkb2NtYW5hZ2VyOm9wZW4nLFxuICAgICAgYXJnczogd2lkZ2V0ID0+ICh7IHBhdGg6IHdpZGdldC5jb250ZXh0LnBhdGgsIGZhY3Rvcnk6IEZBQ1RPUllfQ1NWIH0pLFxuICAgICAgbmFtZTogd2lkZ2V0ID0+IHdpZGdldC5jb250ZXh0LnBhdGhcbiAgICB9KTtcbiAgfVxuXG4gIGFwcC5kb2NSZWdpc3RyeS5hZGRXaWRnZXRGYWN0b3J5KGZhY3RvcnkpO1xuICBjb25zdCBmdCA9IGFwcC5kb2NSZWdpc3RyeS5nZXRGaWxlVHlwZSgnY3N2Jyk7XG4gIGZhY3Rvcnkud2lkZ2V0Q3JlYXRlZC5jb25uZWN0KChzZW5kZXIsIHdpZGdldCkgPT4ge1xuICAgIC8vIFRyYWNrIHRoZSB3aWRnZXQuXG4gICAgdm9pZCB0cmFja2VyLmFkZCh3aWRnZXQpO1xuICAgIC8vIE5vdGlmeSB0aGUgd2lkZ2V0IHRyYWNrZXIgaWYgcmVzdG9yZSBkYXRhIG5lZWRzIHRvIHVwZGF0ZS5cbiAgICB3aWRnZXQuY29udGV4dC5wYXRoQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHZvaWQgdHJhY2tlci5zYXZlKHdpZGdldCk7XG4gICAgfSk7XG5cbiAgICBpZiAoZnQpIHtcbiAgICAgIHdpZGdldC50aXRsZS5pY29uID0gZnQuaWNvbiE7XG4gICAgICB3aWRnZXQudGl0bGUuaWNvbkNsYXNzID0gZnQuaWNvbkNsYXNzITtcbiAgICAgIHdpZGdldC50aXRsZS5pY29uTGFiZWwgPSBmdC5pY29uTGFiZWwhO1xuICAgIH1cbiAgICAvLyBTZXQgdGhlIHRoZW1lIGZvciB0aGUgbmV3IHdpZGdldC5cbiAgICB3aWRnZXQuY29udGVudC5zdHlsZSA9IHN0eWxlO1xuICAgIHdpZGdldC5jb250ZW50LnJlbmRlcmVyQ29uZmlnID0gcmVuZGVyZXJDb25maWc7XG4gIH0pO1xuXG4gIC8vIEtlZXAgdGhlIHRoZW1lcyB1cC10by1kYXRlLlxuICBjb25zdCB1cGRhdGVUaGVtZXMgPSAoKSA9PiB7XG4gICAgY29uc3QgaXNMaWdodCA9XG4gICAgICB0aGVtZU1hbmFnZXIgJiYgdGhlbWVNYW5hZ2VyLnRoZW1lXG4gICAgICAgID8gdGhlbWVNYW5hZ2VyLmlzTGlnaHQodGhlbWVNYW5hZ2VyLnRoZW1lKVxuICAgICAgICA6IHRydWU7XG4gICAgc3R5bGUgPSBpc0xpZ2h0ID8gUHJpdmF0ZS5MSUdIVF9TVFlMRSA6IFByaXZhdGUuREFSS19TVFlMRTtcbiAgICByZW5kZXJlckNvbmZpZyA9IGlzTGlnaHRcbiAgICAgID8gUHJpdmF0ZS5MSUdIVF9URVhUX0NPTkZJR1xuICAgICAgOiBQcml2YXRlLkRBUktfVEVYVF9DT05GSUc7XG4gICAgdHJhY2tlci5mb3JFYWNoKGdyaWQgPT4ge1xuICAgICAgZ3JpZC5jb250ZW50LnN0eWxlID0gc3R5bGU7XG4gICAgICBncmlkLmNvbnRlbnQucmVuZGVyZXJDb25maWcgPSByZW5kZXJlckNvbmZpZztcbiAgICB9KTtcbiAgfTtcbiAgaWYgKHRoZW1lTWFuYWdlcikge1xuICAgIHRoZW1lTWFuYWdlci50aGVtZUNoYW5nZWQuY29ubmVjdCh1cGRhdGVUaGVtZXMpO1xuICB9XG5cbiAgaWYgKG1haW5NZW51KSB7XG4gICAgYWRkTWVudUVudHJpZXMobWFpbk1lbnUsIHRyYWNrZXIsIHRyYW5zbGF0b3IpO1xuICB9XG4gIGlmIChzZWFyY2hyZWdpc3RyeSkge1xuICAgIHNlYXJjaHJlZ2lzdHJ5LnJlZ2lzdGVyKCdjc3YnLCBDU1ZTZWFyY2hQcm92aWRlcik7XG4gIH1cbn1cblxuLyoqXG4gKiBBY3RpdmF0ZSBjc3N2aWV3ZXIgZXh0ZW5zaW9uIGZvciBUU1YgZmlsZXNcbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGVUc3YoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGwsXG4gIHRoZW1lTWFuYWdlcjogSVRoZW1lTWFuYWdlciB8IG51bGwsXG4gIG1haW5NZW51OiBJTWFpbk1lbnUgfCBudWxsLFxuICBzZWFyY2hyZWdpc3RyeTogSVNlYXJjaFByb3ZpZGVyUmVnaXN0cnkgfCBudWxsXG4pOiB2b2lkIHtcbiAgY29uc3QgZmFjdG9yeSA9IG5ldyBUU1ZWaWV3ZXJGYWN0b3J5KHtcbiAgICBuYW1lOiBGQUNUT1JZX1RTVixcbiAgICBmaWxlVHlwZXM6IFsndHN2J10sXG4gICAgZGVmYXVsdEZvcjogWyd0c3YnXSxcbiAgICByZWFkT25seTogdHJ1ZSxcbiAgICB0cmFuc2xhdG9yXG4gIH0pO1xuICBjb25zdCB0cmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8SURvY3VtZW50V2lkZ2V0PENTVlZpZXdlcj4+KHtcbiAgICBuYW1lc3BhY2U6ICd0c3Z2aWV3ZXInXG4gIH0pO1xuXG4gIC8vIFRoZSBjdXJyZW50IHN0eWxlcyBmb3IgdGhlIGRhdGEgZ3JpZHMuXG4gIGxldCBzdHlsZTogRGF0YUdyaWQuU3R5bGUgPSBQcml2YXRlLkxJR0hUX1NUWUxFO1xuICBsZXQgcmVuZGVyZXJDb25maWc6IFRleHRSZW5kZXJDb25maWcgPSBQcml2YXRlLkxJR0hUX1RFWFRfQ09ORklHO1xuXG4gIGlmIChyZXN0b3Jlcikge1xuICAgIC8vIEhhbmRsZSBzdGF0ZSByZXN0b3JhdGlvbi5cbiAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwge1xuICAgICAgY29tbWFuZDogJ2RvY21hbmFnZXI6b3BlbicsXG4gICAgICBhcmdzOiB3aWRnZXQgPT4gKHsgcGF0aDogd2lkZ2V0LmNvbnRleHQucGF0aCwgZmFjdG9yeTogRkFDVE9SWV9UU1YgfSksXG4gICAgICBuYW1lOiB3aWRnZXQgPT4gd2lkZ2V0LmNvbnRleHQucGF0aFxuICAgIH0pO1xuICB9XG5cbiAgYXBwLmRvY1JlZ2lzdHJ5LmFkZFdpZGdldEZhY3RvcnkoZmFjdG9yeSk7XG4gIGNvbnN0IGZ0ID0gYXBwLmRvY1JlZ2lzdHJ5LmdldEZpbGVUeXBlKCd0c3YnKTtcbiAgZmFjdG9yeS53aWRnZXRDcmVhdGVkLmNvbm5lY3QoKHNlbmRlciwgd2lkZ2V0KSA9PiB7XG4gICAgLy8gVHJhY2sgdGhlIHdpZGdldC5cbiAgICB2b2lkIHRyYWNrZXIuYWRkKHdpZGdldCk7XG4gICAgLy8gTm90aWZ5IHRoZSB3aWRnZXQgdHJhY2tlciBpZiByZXN0b3JlIGRhdGEgbmVlZHMgdG8gdXBkYXRlLlxuICAgIHdpZGdldC5jb250ZXh0LnBhdGhDaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgdm9pZCB0cmFja2VyLnNhdmUod2lkZ2V0KTtcbiAgICB9KTtcblxuICAgIGlmIChmdCkge1xuICAgICAgd2lkZ2V0LnRpdGxlLmljb24gPSBmdC5pY29uITtcbiAgICAgIHdpZGdldC50aXRsZS5pY29uQ2xhc3MgPSBmdC5pY29uQ2xhc3MhO1xuICAgICAgd2lkZ2V0LnRpdGxlLmljb25MYWJlbCA9IGZ0Lmljb25MYWJlbCE7XG4gICAgfVxuICAgIC8vIFNldCB0aGUgdGhlbWUgZm9yIHRoZSBuZXcgd2lkZ2V0LlxuICAgIHdpZGdldC5jb250ZW50LnN0eWxlID0gc3R5bGU7XG4gICAgd2lkZ2V0LmNvbnRlbnQucmVuZGVyZXJDb25maWcgPSByZW5kZXJlckNvbmZpZztcbiAgfSk7XG5cbiAgLy8gS2VlcCB0aGUgdGhlbWVzIHVwLXRvLWRhdGUuXG4gIGNvbnN0IHVwZGF0ZVRoZW1lcyA9ICgpID0+IHtcbiAgICBjb25zdCBpc0xpZ2h0ID1cbiAgICAgIHRoZW1lTWFuYWdlciAmJiB0aGVtZU1hbmFnZXIudGhlbWVcbiAgICAgICAgPyB0aGVtZU1hbmFnZXIuaXNMaWdodCh0aGVtZU1hbmFnZXIudGhlbWUpXG4gICAgICAgIDogdHJ1ZTtcbiAgICBzdHlsZSA9IGlzTGlnaHQgPyBQcml2YXRlLkxJR0hUX1NUWUxFIDogUHJpdmF0ZS5EQVJLX1NUWUxFO1xuICAgIHJlbmRlcmVyQ29uZmlnID0gaXNMaWdodFxuICAgICAgPyBQcml2YXRlLkxJR0hUX1RFWFRfQ09ORklHXG4gICAgICA6IFByaXZhdGUuREFSS19URVhUX0NPTkZJRztcbiAgICB0cmFja2VyLmZvckVhY2goZ3JpZCA9PiB7XG4gICAgICBncmlkLmNvbnRlbnQuc3R5bGUgPSBzdHlsZTtcbiAgICAgIGdyaWQuY29udGVudC5yZW5kZXJlckNvbmZpZyA9IHJlbmRlcmVyQ29uZmlnO1xuICAgIH0pO1xuICB9O1xuICBpZiAodGhlbWVNYW5hZ2VyKSB7XG4gICAgdGhlbWVNYW5hZ2VyLnRoZW1lQ2hhbmdlZC5jb25uZWN0KHVwZGF0ZVRoZW1lcyk7XG4gIH1cblxuICBpZiAobWFpbk1lbnUpIHtcbiAgICBhZGRNZW51RW50cmllcyhtYWluTWVudSwgdHJhY2tlciwgdHJhbnNsYXRvcik7XG4gIH1cbiAgaWYgKHNlYXJjaHJlZ2lzdHJ5KSB7XG4gICAgc2VhcmNocmVnaXN0cnkucmVnaXN0ZXIoJ3RzdicsIENTVlNlYXJjaFByb3ZpZGVyKTtcbiAgfVxufVxuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2lucyBhcyBkZWZhdWx0LlxuICovXG5jb25zdCBwbHVnaW5zOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48YW55PltdID0gW2NzdiwgdHN2XTtcbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogVGhlIGxpZ2h0IHRoZW1lIGZvciB0aGUgZGF0YSBncmlkLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IExJR0hUX1NUWUxFOiBEYXRhR3JpZC5TdHlsZSA9IHtcbiAgICAuLi5EYXRhR3JpZC5kZWZhdWx0U3R5bGUsXG4gICAgdm9pZENvbG9yOiAnI0YzRjNGMycsXG4gICAgYmFja2dyb3VuZENvbG9yOiAnd2hpdGUnLFxuICAgIGhlYWRlckJhY2tncm91bmRDb2xvcjogJyNFRUVFRUUnLFxuICAgIGdyaWRMaW5lQ29sb3I6ICdyZ2JhKDIwLCAyMCwgMjAsIDAuMTUpJyxcbiAgICBoZWFkZXJHcmlkTGluZUNvbG9yOiAncmdiYSgyMCwgMjAsIDIwLCAwLjI1KScsXG4gICAgcm93QmFja2dyb3VuZENvbG9yOiBpID0+IChpICUgMiA9PT0gMCA/ICcjRjVGNUY1JyA6ICd3aGl0ZScpXG4gIH07XG5cbiAgLyoqXG4gICAqIFRoZSBkYXJrIHRoZW1lIGZvciB0aGUgZGF0YSBncmlkLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IERBUktfU1RZTEU6IERhdGFHcmlkLlN0eWxlID0ge1xuICAgIC4uLkRhdGFHcmlkLmRlZmF1bHRTdHlsZSxcbiAgICB2b2lkQ29sb3I6ICdibGFjaycsXG4gICAgYmFja2dyb3VuZENvbG9yOiAnIzExMTExMScsXG4gICAgaGVhZGVyQmFja2dyb3VuZENvbG9yOiAnIzQyNDI0MicsXG4gICAgZ3JpZExpbmVDb2xvcjogJ3JnYmEoMjM1LCAyMzUsIDIzNSwgMC4xNSknLFxuICAgIGhlYWRlckdyaWRMaW5lQ29sb3I6ICdyZ2JhKDIzNSwgMjM1LCAyMzUsIDAuMjUpJyxcbiAgICByb3dCYWNrZ3JvdW5kQ29sb3I6IGkgPT4gKGkgJSAyID09PSAwID8gJyMyMTIxMjEnIDogJyMxMTExMTEnKVxuICB9O1xuXG4gIC8qKlxuICAgKiBUaGUgbGlnaHQgY29uZmlnIGZvciB0aGUgZGF0YSBncmlkIHJlbmRlcmVyLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IExJR0hUX1RFWFRfQ09ORklHOiBUZXh0UmVuZGVyQ29uZmlnID0ge1xuICAgIHRleHRDb2xvcjogJyMxMTExMTEnLFxuICAgIG1hdGNoQmFja2dyb3VuZENvbG9yOiAnI0ZGRkZFMCcsXG4gICAgY3VycmVudE1hdGNoQmFja2dyb3VuZENvbG9yOiAnI0ZGRkYwMCcsXG4gICAgaG9yaXpvbnRhbEFsaWdubWVudDogJ3JpZ2h0J1xuICB9O1xuXG4gIC8qKlxuICAgKiBUaGUgZGFyayBjb25maWcgZm9yIHRoZSBkYXRhIGdyaWQgcmVuZGVyZXIuXG4gICAqL1xuICBleHBvcnQgY29uc3QgREFSS19URVhUX0NPTkZJRzogVGV4dFJlbmRlckNvbmZpZyA9IHtcbiAgICB0ZXh0Q29sb3I6ICcjRjVGNUY1JyxcbiAgICBtYXRjaEJhY2tncm91bmRDb2xvcjogJyM4Mzg0MjMnLFxuICAgIGN1cnJlbnRNYXRjaEJhY2tncm91bmRDb2xvcjogJyNBMzgwN0EnLFxuICAgIGhvcml6b250YWxBbGlnbm1lbnQ6ICdyaWdodCdcbiAgfTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbmltcG9ydCB7IENTVlZpZXdlciB9IGZyb20gJ0BqdXB5dGVybGFiL2NzdnZpZXdlcic7XG5pbXBvcnQgeyBEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IElTZWFyY2hNYXRjaCwgSVNlYXJjaFByb3ZpZGVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jdW1lbnRzZWFyY2gnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLy8gVGhlIHR5cGUgZm9yIHdoaWNoIGNhblNlYXJjaEZvciByZXR1cm5zIHRydWVcbmV4cG9ydCB0eXBlIENTVkRvY3VtZW50V2lkZ2V0ID0gRG9jdW1lbnRXaWRnZXQ8Q1NWVmlld2VyPjtcblxuZXhwb3J0IGNsYXNzIENTVlNlYXJjaFByb3ZpZGVyIGltcGxlbWVudHMgSVNlYXJjaFByb3ZpZGVyPENTVkRvY3VtZW50V2lkZ2V0PiB7XG4gIC8qKlxuICAgKiBSZXBvcnQgd2hldGhlciBvciBub3QgdGhpcyBwcm92aWRlciBoYXMgdGhlIGFiaWxpdHkgdG8gc2VhcmNoIG9uIHRoZSBnaXZlbiBvYmplY3RcbiAgICovXG4gIHN0YXRpYyBjYW5TZWFyY2hPbihkb21haW46IFdpZGdldCk6IGRvbWFpbiBpcyBDU1ZEb2N1bWVudFdpZGdldCB7XG4gICAgLy8gY2hlY2sgdG8gc2VlIGlmIHRoZSBDU1ZTZWFyY2hQcm92aWRlciBjYW4gc2VhcmNoIG9uIHRoZVxuICAgIC8vIGZpcnN0IGNlbGwsIGZhbHNlIGluZGljYXRlcyBhbm90aGVyIGVkaXRvciBpcyBwcmVzZW50XG4gICAgcmV0dXJuIChcbiAgICAgIGRvbWFpbiBpbnN0YW5jZW9mIERvY3VtZW50V2lkZ2V0ICYmIGRvbWFpbi5jb250ZW50IGluc3RhbmNlb2YgQ1NWVmlld2VyXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgYW4gaW5pdGlhbCBxdWVyeSB2YWx1ZSBpZiBhcHBsaWNhYmxlIHNvIHRoYXQgaXQgY2FuIGJlIGVudGVyZWRcbiAgICogaW50byB0aGUgc2VhcmNoIGJveCBhcyBhbiBpbml0aWFsIHF1ZXJ5XG4gICAqXG4gICAqIEByZXR1cm5zIEluaXRpYWwgdmFsdWUgdXNlZCB0byBwb3B1bGF0ZSB0aGUgc2VhcmNoIGJveC5cbiAgICovXG4gIGdldEluaXRpYWxRdWVyeShzZWFyY2hUYXJnZXQ6IENTVkRvY3VtZW50V2lkZ2V0KTogYW55IHtcbiAgICAvLyBDU1YgVmlld2VyIGRvZXMgbm90IHN1cHBvcnQgc2VsZWN0aW9uXG4gICAgcmV0dXJuIG51bGw7XG4gIH1cblxuICAvKipcbiAgICogSW5pdGlhbGl6ZSB0aGUgc2VhcmNoIHVzaW5nIHRoZSBwcm92aWRlZCBvcHRpb25zLiAgU2hvdWxkIHVwZGF0ZSB0aGUgVUlcbiAgICogdG8gaGlnaGxpZ2h0IGFsbCBtYXRjaGVzIGFuZCBcInNlbGVjdFwiIHdoYXRldmVyIHRoZSBmaXJzdCBtYXRjaCBzaG91bGQgYmUuXG4gICAqXG4gICAqIEBwYXJhbSBxdWVyeSBBIFJlZ0V4cCB0byBiZSB1c2UgdG8gcGVyZm9ybSB0aGUgc2VhcmNoXG4gICAqIEBwYXJhbSBzZWFyY2hUYXJnZXQgVGhlIHdpZGdldCB0byBiZSBzZWFyY2hlZFxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aXRoIGEgbGlzdCBvZiBhbGwgbWF0Y2hlc1xuICAgKi9cbiAgYXN5bmMgc3RhcnRRdWVyeShcbiAgICBxdWVyeTogUmVnRXhwLFxuICAgIHNlYXJjaFRhcmdldDogQ1NWRG9jdW1lbnRXaWRnZXRcbiAgKTogUHJvbWlzZTxJU2VhcmNoTWF0Y2hbXT4ge1xuICAgIHRoaXMuX3RhcmdldCA9IHNlYXJjaFRhcmdldDtcbiAgICB0aGlzLl9xdWVyeSA9IHF1ZXJ5O1xuICAgIHNlYXJjaFRhcmdldC5jb250ZW50LnNlYXJjaFNlcnZpY2UuZmluZChxdWVyeSk7XG4gICAgcmV0dXJuIHRoaXMubWF0Y2hlcztcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhcnMgc3RhdGUgb2YgYSBzZWFyY2ggcHJvdmlkZXIgdG8gcHJlcGFyZSBmb3Igc3RhcnRRdWVyeSB0byBiZSBjYWxsZWRcbiAgICogaW4gb3JkZXIgdG8gc3RhcnQgYSBuZXcgcXVlcnkgb3IgcmVmcmVzaCBhbiBleGlzdGluZyBvbmUuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNlYXJjaCBwcm92aWRlciBpcyByZWFkeSB0b1xuICAgKiBiZWdpbiBhIG5ldyBzZWFyY2guXG4gICAqL1xuICBhc3luYyBlbmRRdWVyeSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICB0aGlzLl90YXJnZXQuY29udGVudC5zZWFyY2hTZXJ2aWNlLmNsZWFyKCk7XG4gIH1cblxuICAvKipcbiAgICogUmVzZXRzIFVJIHN0YXRlIGFzIGl0IHdhcyBiZWZvcmUgdGhlIHNlYXJjaCBwcm9jZXNzIGJlZ2FuLiAgQ2xlYW5zIHVwIGFuZFxuICAgKiBkaXNwb3NlcyBvZiBhbGwgaW50ZXJuYWwgc3RhdGUuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gYWxsIHN0YXRlIGhhcyBiZWVuIGNsZWFuZWQgdXAuXG4gICAqL1xuICBhc3luYyBlbmRTZWFyY2goKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgdGhpcy5fdGFyZ2V0LmNvbnRlbnQuc2VhcmNoU2VydmljZS5jbGVhcigpO1xuICB9XG5cbiAgLyoqXG4gICAqIE1vdmUgdGhlIGN1cnJlbnQgbWF0Y2ggaW5kaWNhdG9yIHRvIHRoZSBuZXh0IG1hdGNoLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyBvbmNlIHRoZSBhY3Rpb24gaGFzIGNvbXBsZXRlZC5cbiAgICovXG4gIGFzeW5jIGhpZ2hsaWdodE5leHQoKTogUHJvbWlzZTxJU2VhcmNoTWF0Y2ggfCB1bmRlZmluZWQ+IHtcbiAgICB0aGlzLl90YXJnZXQuY29udGVudC5zZWFyY2hTZXJ2aWNlLmZpbmQodGhpcy5fcXVlcnkpO1xuICAgIHJldHVybiB1bmRlZmluZWQ7XG4gIH1cblxuICAvKipcbiAgICogTW92ZSB0aGUgY3VycmVudCBtYXRjaCBpbmRpY2F0b3IgdG8gdGhlIHByZXZpb3VzIG1hdGNoLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyBvbmNlIHRoZSBhY3Rpb24gaGFzIGNvbXBsZXRlZC5cbiAgICovXG4gIGFzeW5jIGhpZ2hsaWdodFByZXZpb3VzKCk6IFByb21pc2U8SVNlYXJjaE1hdGNoIHwgdW5kZWZpbmVkPiB7XG4gICAgdGhpcy5fdGFyZ2V0LmNvbnRlbnQuc2VhcmNoU2VydmljZS5maW5kKHRoaXMuX3F1ZXJ5LCB0cnVlKTtcbiAgICByZXR1cm4gdW5kZWZpbmVkO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlcGxhY2UgdGhlIGN1cnJlbnRseSBzZWxlY3RlZCBtYXRjaCB3aXRoIHRoZSBwcm92aWRlZCB0ZXh0XG4gICAqIE5vdCBpbXBsZW1lbnRlZCBpbiB0aGUgQ1NWIHZpZXdlciBhcyBpdCBpcyByZWFkLW9ubHkuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIG9uY2UgdGhlIGFjdGlvbiBoYXMgY29tcGxldGVkLlxuICAgKi9cbiAgYXN5bmMgcmVwbGFjZUN1cnJlbnRNYXRjaChuZXdUZXh0OiBzdHJpbmcpOiBQcm9taXNlPGJvb2xlYW4+IHtcbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cblxuICAvKipcbiAgICogUmVwbGFjZSBhbGwgbWF0Y2hlcyBpbiB0aGUgbm90ZWJvb2sgd2l0aCB0aGUgcHJvdmlkZWQgdGV4dFxuICAgKiBOb3QgaW1wbGVtZW50ZWQgaW4gdGhlIENTViB2aWV3ZXIgYXMgaXQgaXMgcmVhZC1vbmx5LlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyBvbmNlIHRoZSBhY3Rpb24gaGFzIGNvbXBsZXRlZC5cbiAgICovXG4gIGFzeW5jIHJlcGxhY2VBbGxNYXRjaGVzKG5ld1RleHQ6IHN0cmluZyk6IFByb21pc2U8Ym9vbGVhbj4ge1xuICAgIHJldHVybiBmYWxzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTaWduYWwgaW5kaWNhdGluZyB0aGF0IHNvbWV0aGluZyBpbiB0aGUgc2VhcmNoIGhhcyBjaGFuZ2VkLCBzbyB0aGUgVUkgc2hvdWxkIHVwZGF0ZVxuICAgKi9cbiAgZ2V0IGNoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCB2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX2NoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNhbWUgbGlzdCBvZiBtYXRjaGVzIHByb3ZpZGVkIGJ5IHRoZSBzdGFydFF1ZXJ5IHByb21pc2UgcmVzb2x1dGlvblxuICAgKi9cbiAgcmVhZG9ubHkgbWF0Y2hlczogSVNlYXJjaE1hdGNoW10gPSBbXTtcblxuICAvKipcbiAgICogVGhlIGN1cnJlbnQgaW5kZXggb2YgdGhlIHNlbGVjdGVkIG1hdGNoLlxuICAgKi9cbiAgcmVhZG9ubHkgY3VycmVudE1hdGNoSW5kZXg6IG51bWJlciB8IG51bGwgPSBudWxsO1xuXG4gIC8qKlxuICAgKiBTZXQgdG8gdHJ1ZSBpZiB0aGUgd2lkZ2V0IHVuZGVyIHNlYXJjaCBpcyByZWFkLW9ubHksIGZhbHNlXG4gICAqIGlmIGl0IGlzIGVkaXRhYmxlLiAgV2lsbCBiZSB1c2VkIHRvIGRldGVybWluZSB3aGV0aGVyIHRvIHNob3dcbiAgICogdGhlIHJlcGxhY2Ugb3B0aW9uLlxuICAgKi9cbiAgcmVhZG9ubHkgaXNSZWFkT25seSA9IHRydWU7XG5cbiAgcHJpdmF0ZSBfdGFyZ2V0OiBDU1ZEb2N1bWVudFdpZGdldDtcbiAgcHJpdmF0ZSBfcXVlcnk6IFJlZ0V4cDtcbiAgcHJpdmF0ZSBfY2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgdm9pZD4odGhpcyk7XG59XG4iXSwic291cmNlUm9vdCI6IiJ9