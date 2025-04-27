(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_toc-extension_lib_index_js-_6a850"],{

/***/ "../packages/toc-extension/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/toc-extension/lib/index.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/markdownviewer */ "webpack/sharing/consume/default/@jupyterlab/markdownviewer/@jupyterlab/markdownviewer");
/* harmony import */ var _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/toc */ "webpack/sharing/consume/default/@jupyterlab/toc/@jupyterlab/toc");
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_10__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module toc-extension
 */











/**
 * The command IDs used by TOC item.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.runCells = 'toc:run-cells';
})(CommandIDs || (CommandIDs = {}));
/**
 * Activates the ToC extension.
 *
 * @private
 * @param app - Jupyter application
 * @param docmanager - document manager
 * @param rendermime - rendered MIME registry
 * @param translator - translator
 * @param editorTracker - editor tracker
 * @param restorer - application layout restorer
 * @param labShell - Jupyter lab shell
 * @param markdownViewerTracker - Markdown viewer tracker
 * @param notebookTracker - notebook tracker
 * @param settingRegistry - setting registry
 * @returns table of contents registry
 */
async function activateTOC(app, docmanager, rendermime, translator, editorTracker, restorer, labShell, markdownViewerTracker, notebookTracker, settingRegistry) {
    const trans = translator.load('jupyterlab');
    // Create the ToC widget:
    const toc = new _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__.TableOfContents({
        docmanager,
        rendermime,
        translator
    });
    // Create the ToC registry:
    const registry = new _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__.TableOfContentsRegistry();
    // Add the ToC to the left area:
    toc.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.tocIcon;
    toc.title.caption = trans.__('Table of Contents');
    toc.id = 'table-of-contents';
    toc.node.setAttribute('role', 'region');
    toc.node.setAttribute('aria-label', trans.__('Table of Contents section'));
    app.shell.add(toc, 'left', { rank: 400 });
    app.commands.addCommand(CommandIDs.runCells, {
        execute: args => {
            if (!notebookTracker) {
                return null;
            }
            const panel = notebookTracker.currentWidget;
            if (panel == null) {
                return;
            }
            const cells = panel.content.widgets;
            if (cells === undefined) {
                return;
            }
            const activeCell = toc.activeEntry.cellRef;
            if (activeCell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_10__.MarkdownCell) {
                let level = activeCell.headingInfo.level;
                for (let i = cells.indexOf(activeCell) + 1; i < cells.length; i++) {
                    const cell = cells[i];
                    if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_10__.MarkdownCell && cell.headingInfo.level <= level) {
                        break;
                    }
                    if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_10__.CodeCell) {
                        void _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_10__.CodeCell.execute(cell, panel.sessionContext);
                    }
                }
            }
            else {
                if (activeCell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_10__.CodeCell) {
                    void _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_10__.CodeCell.execute(activeCell, panel.sessionContext);
                }
            }
        },
        label: trans.__('Run Cell(s)')
    });
    app.contextMenu.addItem({
        selector: '.jp-tocItem',
        command: CommandIDs.runCells
    });
    if (restorer) {
        // Add the ToC widget to the application restorer:
        restorer.add(toc, '@jupyterlab/toc:plugin');
    }
    // Attempt to load plugin settings:
    let settings;
    if (settingRegistry) {
        try {
            settings = await settingRegistry.load('@jupyterlab/toc-extension:plugin');
        }
        catch (error) {
            console.error(`Failed to load settings for the Table of Contents extension.\n\n${error}`);
        }
    }
    // Create a notebook generator:
    if (notebookTracker) {
        const notebookGenerator = (0,_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__.createNotebookGenerator)(notebookTracker, toc, rendermime.sanitizer, translator, settings);
        registry.add(notebookGenerator);
    }
    // Create a Markdown generator:
    if (editorTracker) {
        const markdownGenerator = (0,_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__.createMarkdownGenerator)(editorTracker, toc, rendermime.sanitizer, translator, settings);
        registry.add(markdownGenerator);
        // Create a LaTeX generator:
        const latexGenerator = (0,_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__.createLatexGenerator)(editorTracker);
        registry.add(latexGenerator);
        // Create a Python generator:
        const pythonGenerator = (0,_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__.createPythonGenerator)(editorTracker);
        registry.add(pythonGenerator);
    }
    // Create a rendered Markdown generator:
    if (markdownViewerTracker) {
        const renderedMarkdownGenerator = (0,_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__.createRenderedMarkdownGenerator)(markdownViewerTracker, toc, rendermime.sanitizer, translator, settings);
        registry.add(renderedMarkdownGenerator);
    }
    // Update the ToC when the active widget changes:
    if (labShell) {
        labShell.currentChanged.connect(onConnect);
    }
    return registry;
    /**
     * Callback invoked when the active widget changes.
     *
     * @private
     */
    function onConnect() {
        let widget = app.shell.currentWidget;
        if (!widget) {
            return;
        }
        let generator = registry.find(widget);
        if (!generator) {
            // If the previously used widget is still available, stick with it.
            // Otherwise, set the current ToC widget to null.
            if (toc.current && toc.current.widget.isDisposed) {
                toc.current = null;
            }
            return;
        }
        toc.current = { widget, generator };
    }
}
/**
 * Initialization data for the ToC extension.
 *
 * @private
 */
const extension = {
    id: '@jupyterlab/toc:plugin',
    autoStart: true,
    provides: _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_7__.ITableOfContentsRegistry,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_5__.IRenderMimeRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    optional: [
        _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorTracker,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__.IMarkdownViewerTracker,
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.INotebookTracker,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__.ISettingRegistry
    ],
    activate: activateTOC
};
/**
 * Exports.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdG9jLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU84QjtBQUN5QjtBQUNGO0FBQ1k7QUFDWjtBQUNLO0FBQ0U7QUFVdEM7QUFDNkI7QUFDRjtBQUVPO0FBRTNEOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBRW5CO0FBRkQsV0FBVSxVQUFVO0lBQ0wsbUJBQVEsR0FBRyxlQUFlLENBQUM7QUFDMUMsQ0FBQyxFQUZTLFVBQVUsS0FBVixVQUFVLFFBRW5CO0FBRUQ7Ozs7Ozs7Ozs7Ozs7OztHQWVHO0FBQ0gsS0FBSyxVQUFVLFdBQVcsQ0FDeEIsR0FBb0IsRUFDcEIsVUFBNEIsRUFDNUIsVUFBK0IsRUFDL0IsVUFBdUIsRUFDdkIsYUFBOEIsRUFDOUIsUUFBMEIsRUFDMUIsUUFBb0IsRUFDcEIscUJBQThDLEVBQzlDLGVBQWtDLEVBQ2xDLGVBQWtDO0lBRWxDLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7SUFDNUMseUJBQXlCO0lBQ3pCLE1BQU0sR0FBRyxHQUFHLElBQUksNERBQWUsQ0FBQztRQUM5QixVQUFVO1FBQ1YsVUFBVTtRQUNWLFVBQVU7S0FDWCxDQUFDLENBQUM7SUFFSCwyQkFBMkI7SUFDM0IsTUFBTSxRQUFRLEdBQUcsSUFBSSxvRUFBUSxFQUFFLENBQUM7SUFFaEMsZ0NBQWdDO0lBQ2hDLEdBQUcsQ0FBQyxLQUFLLENBQUMsSUFBSSxHQUFHLDhEQUFPLENBQUM7SUFDekIsR0FBRyxDQUFDLEtBQUssQ0FBQyxPQUFPLEdBQUcsS0FBSyxDQUFDLEVBQUUsQ0FBQyxtQkFBbUIsQ0FBQyxDQUFDO0lBQ2xELEdBQUcsQ0FBQyxFQUFFLEdBQUcs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Q0FBQztRQUN0QyxJQUFJLENBQUMsU0FBUyxFQUFFO1lBQ2QsbUVBQW1FO1lBQ25FLGlEQUFpRDtZQUNqRCxJQUFJLEdBQUcsQ0FBQyxPQUFPLElBQUksR0FBRyxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsVUFBVSxFQUFFO2dCQUNoRCxHQUFHLENBQUMsT0FBTyxHQUFHLElBQUksQ0FBQzthQUNwQjtZQUNELE9BQU87U0FDUjtRQUNELEdBQUcsQ0FBQyxPQUFPLEdBQUcsRUFBRSxNQUFNLEVBQUUsU0FBUyxFQUFFLENBQUM7SUFDdEMsQ0FBQztBQUNILENBQUM7QUFFRDs7OztHQUlHO0FBQ0gsTUFBTSxTQUFTLEdBQW9EO0lBQ2pFLEVBQUUsRUFBRSx3QkFBd0I7SUFDNUIsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUscUVBQXdCO0lBQ2xDLFFBQVEsRUFBRSxDQUFDLG9FQUFnQixFQUFFLHVFQUFtQixFQUFFLGdFQUFXLENBQUM7SUFDOUQsUUFBUSxFQUFFO1FBQ1Isa0VBQWM7UUFDZCxvRUFBZTtRQUNmLDhEQUFTO1FBQ1QsOEVBQXNCO1FBQ3RCLGtFQUFnQjtRQUNoQix5RUFBZ0I7S0FDakI7SUFDRCxRQUFRLEVBQUUsV0FBVztDQUN0QixDQUFDO0FBRUY7O0dBRUc7QUFDSCxpRUFBZSxTQUFTLEVBQUMiLCJmaWxlIjoicGFja2FnZXNfdG9jLWV4dGVuc2lvbl9saWJfaW5kZXhfanMtXzZhODUwLjRlMmUwYTM0ZWE1MTM5ZTZhNWI5LmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdG9jLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTaGVsbCxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJRG9jdW1lbnRNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlcic7XG5pbXBvcnQgeyBJRWRpdG9yVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2ZpbGVlZGl0b3InO1xuaW1wb3J0IHsgSU1hcmtkb3duVmlld2VyVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL21hcmtkb3dudmlld2VyJztcbmltcG9ydCB7IElOb3RlYm9va1RyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9ub3RlYm9vayc7XG5pbXBvcnQgeyBJUmVuZGVyTWltZVJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIGNyZWF0ZUxhdGV4R2VuZXJhdG9yLFxuICBjcmVhdGVNYXJrZG93bkdlbmVyYXRvcixcbiAgY3JlYXRlTm90ZWJvb2tHZW5lcmF0b3IsXG4gIGNyZWF0ZVB5dGhvbkdlbmVyYXRvcixcbiAgY3JlYXRlUmVuZGVyZWRNYXJrZG93bkdlbmVyYXRvcixcbiAgSVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5LFxuICBUYWJsZU9mQ29udGVudHNSZWdpc3RyeSBhcyBSZWdpc3RyeSxcbiAgVGFibGVPZkNvbnRlbnRzXG59IGZyb20gJ0BqdXB5dGVybGFiL3RvYyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IHRvY0ljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IElOb3RlYm9va0hlYWRpbmcgfSBmcm9tICdAanVweXRlcmxhYi90b2MnO1xuaW1wb3J0IHsgQ29kZUNlbGwsIE1hcmtkb3duQ2VsbCB9IGZyb20gJ0BqdXB5dGVybGFiL2NlbGxzJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSBUT0MgaXRlbS5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgcnVuQ2VsbHMgPSAndG9jOnJ1bi1jZWxscyc7XG59XG5cbi8qKlxuICogQWN0aXZhdGVzIHRoZSBUb0MgZXh0ZW5zaW9uLlxuICpcbiAqIEBwcml2YXRlXG4gKiBAcGFyYW0gYXBwIC0gSnVweXRlciBhcHBsaWNhdGlvblxuICogQHBhcmFtIGRvY21hbmFnZXIgLSBkb2N1bWVudCBtYW5hZ2VyXG4gKiBAcGFyYW0gcmVuZGVybWltZSAtIHJlbmRlcmVkIE1JTUUgcmVnaXN0cnlcbiAqIEBwYXJhbSB0cmFuc2xhdG9yIC0gdHJhbnNsYXRvclxuICogQHBhcmFtIGVkaXRvclRyYWNrZXIgLSBlZGl0b3IgdHJhY2tlclxuICogQHBhcmFtIHJlc3RvcmVyIC0gYXBwbGljYXRpb24gbGF5b3V0IHJlc3RvcmVyXG4gKiBAcGFyYW0gbGFiU2hlbGwgLSBKdXB5dGVyIGxhYiBzaGVsbFxuICogQHBhcmFtIG1hcmtkb3duVmlld2VyVHJhY2tlciAtIE1hcmtkb3duIHZpZXdlciB0cmFja2VyXG4gKiBAcGFyYW0gbm90ZWJvb2tUcmFja2VyIC0gbm90ZWJvb2sgdHJhY2tlclxuICogQHBhcmFtIHNldHRpbmdSZWdpc3RyeSAtIHNldHRpbmcgcmVnaXN0cnlcbiAqIEByZXR1cm5zIHRhYmxlIG9mIGNvbnRlbnRzIHJlZ2lzdHJ5XG4gKi9cbmFzeW5jIGZ1bmN0aW9uIGFjdGl2YXRlVE9DKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgZG9jbWFuYWdlcjogSURvY3VtZW50TWFuYWdlcixcbiAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIGVkaXRvclRyYWNrZXI/OiBJRWRpdG9yVHJhY2tlcixcbiAgcmVzdG9yZXI/OiBJTGF5b3V0UmVzdG9yZXIsXG4gIGxhYlNoZWxsPzogSUxhYlNoZWxsLFxuICBtYXJrZG93blZpZXdlclRyYWNrZXI/OiBJTWFya2Rvd25WaWV3ZXJUcmFja2VyLFxuICBub3RlYm9va1RyYWNrZXI/OiBJTm90ZWJvb2tUcmFja2VyLFxuICBzZXR0aW5nUmVnaXN0cnk/OiBJU2V0dGluZ1JlZ2lzdHJ5XG4pOiBQcm9taXNlPElUYWJsZU9mQ29udGVudHNSZWdpc3RyeT4ge1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAvLyBDcmVhdGUgdGhlIFRvQyB3aWRnZXQ6XG4gIGNvbnN0IHRvYyA9IG5ldyBUYWJsZU9mQ29udGVudHMoe1xuICAgIGRvY21hbmFnZXIsXG4gICAgcmVuZGVybWltZSxcbiAgICB0cmFuc2xhdG9yXG4gIH0pO1xuXG4gIC8vIENyZWF0ZSB0aGUgVG9DIHJlZ2lzdHJ5OlxuICBjb25zdCByZWdpc3RyeSA9IG5ldyBSZWdpc3RyeSgpO1xuXG4gIC8vIEFkZCB0aGUgVG9DIHRvIHRoZSBsZWZ0IGFyZWE6XG4gIHRvYy50aXRsZS5pY29uID0gdG9jSWNvbjtcbiAgdG9jLnRpdGxlLmNhcHRpb24gPSB0cmFucy5fXygnVGFibGUgb2YgQ29udGVudHMnKTtcbiAgdG9jLmlkID0gJ3RhYmxlLW9mLWNvbnRlbnRzJztcbiAgdG9jLm5vZGUuc2V0QXR0cmlidXRlKCdyb2xlJywgJ3JlZ2lvbicpO1xuICB0b2Mubm9kZS5zZXRBdHRyaWJ1dGUoJ2FyaWEtbGFiZWwnLCB0cmFucy5fXygnVGFibGUgb2YgQ29udGVudHMgc2VjdGlvbicpKTtcblxuICBhcHAuc2hlbGwuYWRkKHRvYywgJ2xlZnQnLCB7IHJhbms6IDQwMCB9KTtcblxuICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJ1bkNlbGxzLCB7XG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBpZiAoIW5vdGVib29rVHJhY2tlcikge1xuICAgICAgICByZXR1cm4gbnVsbDtcbiAgICAgIH1cblxuICAgICAgY29uc3QgcGFuZWwgPSBub3RlYm9va1RyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICAgIGlmIChwYW5lbCA9PSBudWxsKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cblxuICAgICAgY29uc3QgY2VsbHMgPSBwYW5lbC5jb250ZW50LndpZGdldHM7XG4gICAgICBpZiAoY2VsbHMgPT09IHVuZGVmaW5lZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IGFjdGl2ZUNlbGwgPSAodG9jLmFjdGl2ZUVudHJ5IGFzIElOb3RlYm9va0hlYWRpbmcpLmNlbGxSZWY7XG5cbiAgICAgIGlmIChhY3RpdmVDZWxsIGluc3RhbmNlb2YgTWFya2Rvd25DZWxsKSB7XG4gICAgICAgIGxldCBsZXZlbCA9IGFjdGl2ZUNlbGwuaGVhZGluZ0luZm8ubGV2ZWw7XG4gICAgICAgIGZvciAobGV0IGkgPSBjZWxscy5pbmRleE9mKGFjdGl2ZUNlbGwpICsgMTsgaSA8IGNlbGxzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgY29uc3QgY2VsbCA9IGNlbGxzW2ldO1xuICAgICAgICAgIGlmIChjZWxsIGluc3RhbmNlb2YgTWFya2Rvd25DZWxsICYmIGNlbGwuaGVhZGluZ0luZm8ubGV2ZWwgPD0gbGV2ZWwpIHtcbiAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgIH1cbiAgICAgICAgICBpZiAoY2VsbCBpbnN0YW5jZW9mIENvZGVDZWxsKSB7XG4gICAgICAgICAgICB2b2lkIENvZGVDZWxsLmV4ZWN1dGUoY2VsbCwgcGFuZWwuc2Vzc2lvbkNvbnRleHQpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSBlbHNlIHtcbiAgICAgICAgaWYgKGFjdGl2ZUNlbGwgaW5zdGFuY2VvZiBDb2RlQ2VsbCkge1xuICAgICAgICAgIHZvaWQgQ29kZUNlbGwuZXhlY3V0ZShhY3RpdmVDZWxsLCBwYW5lbC5zZXNzaW9uQ29udGV4dCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9LFxuICAgIGxhYmVsOiB0cmFucy5fXygnUnVuIENlbGwocyknKVxuICB9KTtcblxuICBhcHAuY29udGV4dE1lbnUuYWRkSXRlbSh7XG4gICAgc2VsZWN0b3I6ICcuanAtdG9jSXRlbScsXG4gICAgY29tbWFuZDogQ29tbWFuZElEcy5ydW5DZWxsc1xuICB9KTtcblxuICBpZiAocmVzdG9yZXIpIHtcbiAgICAvLyBBZGQgdGhlIFRvQyB3aWRnZXQgdG8gdGhlIGFwcGxpY2F0aW9uIHJlc3RvcmVyOlxuICAgIHJlc3RvcmVyLmFkZCh0b2MsICdAanVweXRlcmxhYi90b2M6cGx1Z2luJyk7XG4gIH1cblxuICAvLyBBdHRlbXB0IHRvIGxvYWQgcGx1Z2luIHNldHRpbmdzOlxuICBsZXQgc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzIHwgdW5kZWZpbmVkO1xuICBpZiAoc2V0dGluZ1JlZ2lzdHJ5KSB7XG4gICAgdHJ5IHtcbiAgICAgIHNldHRpbmdzID0gYXdhaXQgc2V0dGluZ1JlZ2lzdHJ5LmxvYWQoJ0BqdXB5dGVybGFiL3RvYy1leHRlbnNpb246cGx1Z2luJyk7XG4gICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgIGNvbnNvbGUuZXJyb3IoXG4gICAgICAgIGBGYWlsZWQgdG8gbG9hZCBzZXR0aW5ncyBmb3IgdGhlIFRhYmxlIG9mIENvbnRlbnRzIGV4dGVuc2lvbi5cXG5cXG4ke2Vycm9yfWBcbiAgICAgICk7XG4gICAgfVxuICB9XG5cbiAgLy8gQ3JlYXRlIGEgbm90ZWJvb2sgZ2VuZXJhdG9yOlxuICBpZiAobm90ZWJvb2tUcmFja2VyKSB7XG4gICAgY29uc3Qgbm90ZWJvb2tHZW5lcmF0b3IgPSBjcmVhdGVOb3RlYm9va0dlbmVyYXRvcihcbiAgICAgIG5vdGVib29rVHJhY2tlcixcbiAgICAgIHRvYyxcbiAgICAgIHJlbmRlcm1pbWUuc2FuaXRpemVyLFxuICAgICAgdHJhbnNsYXRvcixcbiAgICAgIHNldHRpbmdzXG4gICAgKTtcbiAgICByZWdpc3RyeS5hZGQobm90ZWJvb2tHZW5lcmF0b3IpO1xuICB9XG5cbiAgLy8gQ3JlYXRlIGEgTWFya2Rvd24gZ2VuZXJhdG9yOlxuICBpZiAoZWRpdG9yVHJhY2tlcikge1xuICAgIGNvbnN0IG1hcmtkb3duR2VuZXJhdG9yID0gY3JlYXRlTWFya2Rvd25HZW5lcmF0b3IoXG4gICAgICBlZGl0b3JUcmFja2VyLFxuICAgICAgdG9jLFxuICAgICAgcmVuZGVybWltZS5zYW5pdGl6ZXIsXG4gICAgICB0cmFuc2xhdG9yLFxuICAgICAgc2V0dGluZ3NcbiAgICApO1xuICAgIHJlZ2lzdHJ5LmFkZChtYXJrZG93bkdlbmVyYXRvcik7XG5cbiAgICAvLyBDcmVhdGUgYSBMYVRlWCBnZW5lcmF0b3I6XG4gICAgY29uc3QgbGF0ZXhHZW5lcmF0b3IgPSBjcmVhdGVMYXRleEdlbmVyYXRvcihlZGl0b3JUcmFja2VyKTtcbiAgICByZWdpc3RyeS5hZGQobGF0ZXhHZW5lcmF0b3IpO1xuXG4gICAgLy8gQ3JlYXRlIGEgUHl0aG9uIGdlbmVyYXRvcjpcbiAgICBjb25zdCBweXRob25HZW5lcmF0b3IgPSBjcmVhdGVQeXRob25HZW5lcmF0b3IoZWRpdG9yVHJhY2tlcik7XG4gICAgcmVnaXN0cnkuYWRkKHB5dGhvbkdlbmVyYXRvcik7XG4gIH1cblxuICAvLyBDcmVhdGUgYSByZW5kZXJlZCBNYXJrZG93biBnZW5lcmF0b3I6XG4gIGlmIChtYXJrZG93blZpZXdlclRyYWNrZXIpIHtcbiAgICBjb25zdCByZW5kZXJlZE1hcmtkb3duR2VuZXJhdG9yID0gY3JlYXRlUmVuZGVyZWRNYXJrZG93bkdlbmVyYXRvcihcbiAgICAgIG1hcmtkb3duVmlld2VyVHJhY2tlcixcbiAgICAgIHRvYyxcbiAgICAgIHJlbmRlcm1pbWUuc2FuaXRpemVyLFxuICAgICAgdHJhbnNsYXRvcixcbiAgICAgIHNldHRpbmdzXG4gICAgKTtcbiAgICByZWdpc3RyeS5hZGQocmVuZGVyZWRNYXJrZG93bkdlbmVyYXRvcik7XG4gIH1cblxuICAvLyBVcGRhdGUgdGhlIFRvQyB3aGVuIHRoZSBhY3RpdmUgd2lkZ2V0IGNoYW5nZXM6XG4gIGlmIChsYWJTaGVsbCkge1xuICAgIGxhYlNoZWxsLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3Qob25Db25uZWN0KTtcbiAgfVxuXG4gIHJldHVybiByZWdpc3RyeTtcblxuICAvKipcbiAgICogQ2FsbGJhY2sgaW52b2tlZCB3aGVuIHRoZSBhY3RpdmUgd2lkZ2V0IGNoYW5nZXMuXG4gICAqXG4gICAqIEBwcml2YXRlXG4gICAqL1xuICBmdW5jdGlvbiBvbkNvbm5lY3QoKSB7XG4gICAgbGV0IHdpZGdldCA9IGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0O1xuICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGxldCBnZW5lcmF0b3IgPSByZWdpc3RyeS5maW5kKHdpZGdldCk7XG4gICAgaWYgKCFnZW5lcmF0b3IpIHtcbiAgICAgIC8vIElmIHRoZSBwcmV2aW91c2x5IHVzZWQgd2lkZ2V0IGlzIHN0aWxsIGF2YWlsYWJsZSwgc3RpY2sgd2l0aCBpdC5cbiAgICAgIC8vIE90aGVyd2lzZSwgc2V0IHRoZSBjdXJyZW50IFRvQyB3aWRnZXQgdG8gbnVsbC5cbiAgICAgIGlmICh0b2MuY3VycmVudCAmJiB0b2MuY3VycmVudC53aWRnZXQuaXNEaXNwb3NlZCkge1xuICAgICAgICB0b2MuY3VycmVudCA9IG51bGw7XG4gICAgICB9XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRvYy5jdXJyZW50ID0geyB3aWRnZXQsIGdlbmVyYXRvciB9O1xuICB9XG59XG5cbi8qKlxuICogSW5pdGlhbGl6YXRpb24gZGF0YSBmb3IgdGhlIFRvQyBleHRlbnNpb24uXG4gKlxuICogQHByaXZhdGVcbiAqL1xuY29uc3QgZXh0ZW5zaW9uOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5PiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi90b2M6cGx1Z2luJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5LFxuICByZXF1aXJlczogW0lEb2N1bWVudE1hbmFnZXIsIElSZW5kZXJNaW1lUmVnaXN0cnksIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtcbiAgICBJRWRpdG9yVHJhY2tlcixcbiAgICBJTGF5b3V0UmVzdG9yZXIsXG4gICAgSUxhYlNoZWxsLFxuICAgIElNYXJrZG93blZpZXdlclRyYWNrZXIsXG4gICAgSU5vdGVib29rVHJhY2tlcixcbiAgICBJU2V0dGluZ1JlZ2lzdHJ5XG4gIF0sXG4gIGFjdGl2YXRlOiBhY3RpdmF0ZVRPQ1xufTtcblxuLyoqXG4gKiBFeHBvcnRzLlxuICovXG5leHBvcnQgZGVmYXVsdCBleHRlbnNpb247XG4iXSwic291cmNlUm9vdCI6IiJ9