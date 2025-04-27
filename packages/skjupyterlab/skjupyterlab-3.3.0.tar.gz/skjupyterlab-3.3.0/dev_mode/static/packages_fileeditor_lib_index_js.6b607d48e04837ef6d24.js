(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_fileeditor_lib_index_js"],{

/***/ "../packages/fileeditor/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/fileeditor/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TabSpaceStatus": () => (/* reexport safe */ _tabspacestatus__WEBPACK_IMPORTED_MODULE_0__.TabSpaceStatus),
/* harmony export */   "IEditorTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_1__.IEditorTracker),
/* harmony export */   "FileEditor": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.FileEditor),
/* harmony export */   "FileEditorCodeWrapper": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.FileEditorCodeWrapper),
/* harmony export */   "FileEditorFactory": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.FileEditorFactory)
/* harmony export */ });
/* harmony import */ var _tabspacestatus__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tabspacestatus */ "../packages/fileeditor/lib/tabspacestatus.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../packages/fileeditor/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "../packages/fileeditor/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module fileeditor
 */





/***/ }),

/***/ "../packages/fileeditor/lib/tabspacestatus.js":
/*!****************************************************!*\
  !*** ../packages/fileeditor/lib/tabspacestatus.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TabSpaceStatus": () => (/* binding */ TabSpaceStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A pure functional component for rendering the TabSpace status.
 */
function TabSpaceComponent(props) {
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
    const trans = translator.load('jupyterlab');
    const description = props.isSpaces
        ? trans.__('Spaces')
        : trans.__('Tab Size');
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { onClick: props.handleClick, source: `${description}: ${props.tabSpace}`, title: trans.__('Change Tab indentation…') }));
}
/**
 * A VDomRenderer for a tabs vs. spaces status item.
 */
class TabSpaceStatus extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Create a new tab/space status item.
     */
    constructor(options) {
        super(new TabSpaceStatus.Model());
        this._popup = null;
        this._menu = options.menu;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this.addClass(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.interactiveItem);
    }
    /**
     * Render the TabSpace status item.
     */
    render() {
        if (!this.model || !this.model.config) {
            return null;
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(TabSpaceComponent, { isSpaces: this.model.config.insertSpaces, tabSpace: this.model.config.tabSize, handleClick: () => this._handleClick(), translator: this.translator }));
        }
    }
    /**
     * Handle a click on the status item.
     */
    _handleClick() {
        const menu = this._menu;
        if (this._popup) {
            this._popup.dispose();
        }
        menu.aboutToClose.connect(this._menuClosed, this);
        this._popup = (0,_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.showPopup)({
            body: menu,
            anchor: this,
            align: 'right'
        });
    }
    _menuClosed() {
        this.removeClass(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.clickedItem);
    }
}
/**
 * A namespace for TabSpace statics.
 */
(function (TabSpaceStatus) {
    /**
     * A VDomModel for the TabSpace status item.
     */
    class Model extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
        constructor() {
            super(...arguments);
            this._config = null;
        }
        /**
         * The editor config from the settings system.
         */
        get config() {
            return this._config;
        }
        set config(val) {
            const oldConfig = this._config;
            this._config = val;
            this._triggerChange(oldConfig, this._config);
        }
        _triggerChange(oldValue, newValue) {
            const oldSpaces = oldValue && oldValue.insertSpaces;
            const oldSize = oldValue && oldValue.tabSize;
            const newSpaces = newValue && newValue.insertSpaces;
            const newSize = newValue && newValue.tabSize;
            if (oldSpaces !== newSpaces || oldSize !== newSize) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    TabSpaceStatus.Model = Model;
})(TabSpaceStatus || (TabSpaceStatus = {}));


/***/ }),

/***/ "../packages/fileeditor/lib/tokens.js":
/*!********************************************!*\
  !*** ../packages/fileeditor/lib/tokens.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IEditorTracker": () => (/* binding */ IEditorTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The editor tracker token.
 */
const IEditorTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/fileeditor:IEditorTracker');
/* tslint:enable */


/***/ }),

/***/ "../packages/fileeditor/lib/widget.js":
/*!********************************************!*\
  !*** ../packages/fileeditor/lib/widget.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FileEditorCodeWrapper": () => (/* binding */ FileEditorCodeWrapper),
/* harmony export */   "FileEditor": () => (/* binding */ FileEditor),
/* harmony export */   "FileEditorFactory": () => (/* binding */ FileEditorFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The data attribute added to a widget that can run code.
 */
const CODE_RUNNER = 'jpCodeRunner';
/**
 * The data attribute added to a widget that can undo.
 */
const UNDOER = 'jpUndoer';
/**
 * A code editor wrapper for the file editor.
 */
class FileEditorCodeWrapper extends _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__.CodeEditorWrapper {
    /**
     * Construct a new editor widget.
     */
    constructor(options) {
        super({
            factory: options.factory,
            model: options.context.model
        });
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.PromiseDelegate();
        const context = (this._context = options.context);
        const editor = this.editor;
        this.addClass('jp-FileEditorCodeWrapper');
        this.node.dataset[CODE_RUNNER] = 'true';
        this.node.dataset[UNDOER] = 'true';
        editor.model.value.text = context.model.toString();
        void context.ready.then(() => {
            this._onContextReady();
        });
        if (context.model.modelDB.isCollaborative) {
            const modelDB = context.model.modelDB;
            void modelDB.connected.then(() => {
                const collaborators = modelDB.collaborators;
                if (!collaborators) {
                    return;
                }
                // Setup the selection style for collaborators
                const localCollaborator = collaborators.localCollaborator;
                this.editor.uuid = localCollaborator.sessionId;
                this.editor.selectionStyle = Object.assign(Object.assign({}, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__.CodeEditor.defaultSelectionStyle), { color: localCollaborator.color });
                collaborators.changed.connect(this._onCollaboratorsChanged, this);
                // Trigger an initial onCollaboratorsChanged event.
                this._onCollaboratorsChanged();
            });
        }
    }
    /**
     * Get the context for the editor widget.
     */
    get context() {
        return this._context;
    }
    /**
     * A promise that resolves when the file editor is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Handle actions that should be taken when the context is ready.
     */
    _onContextReady() {
        if (this.isDisposed) {
            return;
        }
        const contextModel = this._context.model;
        const editor = this.editor;
        const editorModel = editor.model;
        // Set the editor model value.
        editorModel.value.text = contextModel.toString();
        // Prevent the initial loading from disk from being in the editor history.
        editor.clearHistory();
        // Wire signal connections.
        contextModel.contentChanged.connect(this._onContentChanged, this);
        // Resolve the ready promise.
        this._ready.resolve(undefined);
    }
    /**
     * Handle a change in context model content.
     */
    _onContentChanged() {
        const editorModel = this.editor.model;
        const oldValue = editorModel.value.text;
        const newValue = this._context.model.toString();
        if (oldValue !== newValue) {
            editorModel.value.text = newValue;
        }
    }
    /**
     * Handle a change to the collaborators on the model
     * by updating UI elements associated with them.
     */
    _onCollaboratorsChanged() {
        // If there are selections corresponding to non-collaborators,
        // they are stale and should be removed.
        const collaborators = this._context.model.modelDB.collaborators;
        if (!collaborators) {
            return;
        }
        for (const key of this.editor.model.selections.keys()) {
            if (!collaborators.has(key)) {
                this.editor.model.selections.delete(key);
            }
        }
    }
}
/**
 * A widget for editors.
 */
class FileEditor extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Construct a new editor widget.
     */
    constructor(options) {
        super();
        this.addClass('jp-FileEditor');
        const context = (this._context = options.context);
        this._mimeTypeService = options.mimeTypeService;
        const editorWidget = (this.editorWidget = new FileEditorCodeWrapper(options));
        this.editor = editorWidget.editor;
        this.model = editorWidget.model;
        // Listen for changes to the path.
        context.pathChanged.connect(this._onPathChanged, this);
        this._onPathChanged();
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.StackedLayout());
        layout.addWidget(editorWidget);
    }
    /**
     * Get the context for the editor widget.
     */
    get context() {
        return this.editorWidget.context;
    }
    /**
     * A promise that resolves when the file editor is ready.
     */
    get ready() {
        return this.editorWidget.ready;
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the widget's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        if (!this.model) {
            return;
        }
        switch (event.type) {
            case 'mousedown':
                this._ensureFocus();
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        const node = this.node;
        node.addEventListener('mousedown', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.node;
        node.removeEventListener('mousedown', this);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this._ensureFocus();
    }
    /**
     * Ensure that the widget has focus.
     */
    _ensureFocus() {
        if (!this.editor.hasFocus()) {
            this.editor.focus();
        }
    }
    /**
     * Handle a change to the path.
     */
    _onPathChanged() {
        const editor = this.editor;
        const localPath = this._context.localPath;
        editor.model.mimeType = this._mimeTypeService.getMimeTypeByFilePath(localPath);
    }
}
/**
 * A widget factory for editors.
 */
class FileEditorFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.ABCWidgetFactory {
    /**
     * Construct a new editor widget factory.
     */
    constructor(options) {
        super(options.factoryOptions);
        this._services = options.editorServices;
    }
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const func = this._services.factoryService.newDocumentEditor;
        const factory = options => {
            return func(options);
        };
        const content = new FileEditor({
            factory,
            context,
            mimeTypeService: this._services.mimeTypeService
        });
        content.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.textEditorIcon;
        const widget = new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget({ content, context });
        return widget;
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZmlsZWVkaXRvci9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2ZpbGVlZGl0b3Ivc3JjL3RhYnNwYWNlc3RhdHVzLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZmlsZWVkaXRvci9zcmMvdG9rZW5zLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9maWxlZWRpdG9yL3NyYy93aWRnZXQudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQUU4QjtBQUNSO0FBQ0E7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1R6QiwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBRUk7QUFRaEM7QUFDdUM7QUFFNUM7QUFpQzFCOztHQUVHO0FBQ0gsU0FBUyxpQkFBaUIsQ0FDeEIsS0FBK0I7SUFFL0IsTUFBTSxVQUFVLEdBQUcsS0FBSyxDQUFDLFVBQVUsSUFBSSxtRUFBYyxDQUFDO0lBQ3RELE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7SUFDNUMsTUFBTSxXQUFXLEdBQUcsS0FBSyxDQUFDLFFBQVE7UUFDaEMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsUUFBUSxDQUFDO1FBQ3BCLENBQUMsQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQyxDQUFDO0lBQ3pCLE9BQU8sQ0FDTCwyREFBQywyREFBUSxJQUNQLE9BQU8sRUFBRSxLQUFLLENBQUMsV0FBVyxFQUMxQixNQUFNLEVBQUUsR0FBRyxXQUFXLEtBQUssS0FBSyxDQUFDLFFBQVEsRUFB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cl9saWJfaW5kZXhfanMuNmI2MDdkNDhlMDQ4MzdlZjZkMjQuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBmaWxlZWRpdG9yXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi90YWJzcGFjZXN0YXR1cyc7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG5leHBvcnQgKiBmcm9tICcuL3dpZGdldCc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFZEb21Nb2RlbCwgVkRvbVJlbmRlcmVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgQ29kZUVkaXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0IHtcbiAgY2xpY2tlZEl0ZW0sXG4gIGludGVyYWN0aXZlSXRlbSxcbiAgUG9wdXAsXG4gIHNob3dQb3B1cCxcbiAgVGV4dEl0ZW1cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IE1lbnUgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgVGFiU3BhY2VDb21wb25lbnQgc3RhdGljcy5cbiAqL1xubmFtZXNwYWNlIFRhYlNwYWNlQ29tcG9uZW50IHtcbiAgLyoqXG4gICAqIFRoZSBwcm9wcyBmb3IgVGFiU3BhY2VDb21wb25lbnQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wcyB7XG4gICAgLyoqXG4gICAgICogVGhlIG51bWJlciBvZiBzcGFjZXMgdG8gaW5zZXJ0IG9uIHRhYi5cbiAgICAgKi9cbiAgICB0YWJTcGFjZTogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byB1c2Ugc3BhY2VzIG9yIHRhYnMuXG4gICAgICovXG4gICAgaXNTcGFjZXM6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG5cbiAgICAvKipcbiAgICAgKiBBIGNsaWNrIGhhbmRsZXIgZm9yIHRoZSBUYWJTcGFjZSBjb21wb25lbnQuIEJ5IGRlZmF1bHRcbiAgICAgKiBvcGVucyBhIG1lbnUgYWxsb3dpbmcgdGhlIHVzZXIgdG8gc2VsZWN0IHRhYnMgdnMgc3BhY2VzLlxuICAgICAqL1xuICAgIGhhbmRsZUNsaWNrOiAoKSA9PiB2b2lkO1xuICB9XG59XG5cbi8qKlxuICogQSBwdXJlIGZ1bmN0aW9uYWwgY29tcG9uZW50IGZvciByZW5kZXJpbmcgdGhlIFRhYlNwYWNlIHN0YXR1cy5cbiAqL1xuZnVuY3Rpb24gVGFiU3BhY2VDb21wb25lbnQoXG4gIHByb3BzOiBUYWJTcGFjZUNvbXBvbmVudC5JUHJvcHNcbik6IFJlYWN0LlJlYWN0RWxlbWVudDxUYWJTcGFjZUNvbXBvbmVudC5JUHJvcHM+IHtcbiAgY29uc3QgdHJhbnNsYXRvciA9IHByb3BzLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IGRlc2NyaXB0aW9uID0gcHJvcHMuaXNTcGFjZXNcbiAgICA/IHRyYW5zLl9fKCdTcGFjZXMnKVxuICAgIDogdHJhbnMuX18oJ1RhYiBTaXplJyk7XG4gIHJldHVybiAoXG4gICAgPFRleHRJdGVtXG4gICAgICBvbkNsaWNrPXtwcm9wcy5oYW5kbGVDbGlja31cbiAgICAgIHNvdXJjZT17YCR7ZGVzY3JpcHRpb259OiAke3Byb3BzLnRhYlNwYWNlfWB9XG4gICAgICB0aXRsZT17dHJhbnMuX18oJ0NoYW5nZSBUYWIgaW5kZW50YXRpb27igKYnKX1cbiAgICAvPlxuICApO1xufVxuXG4vKipcbiAqIEEgVkRvbVJlbmRlcmVyIGZvciBhIHRhYnMgdnMuIHNwYWNlcyBzdGF0dXMgaXRlbS5cbiAqL1xuZXhwb3J0IGNsYXNzIFRhYlNwYWNlU3RhdHVzIGV4dGVuZHMgVkRvbVJlbmRlcmVyPFRhYlNwYWNlU3RhdHVzLk1vZGVsPiB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgdGFiL3NwYWNlIHN0YXR1cyBpdGVtLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogVGFiU3BhY2VTdGF0dXMuSU9wdGlvbnMpIHtcbiAgICBzdXBlcihuZXcgVGFiU3BhY2VTdGF0dXMuTW9kZWwoKSk7XG4gICAgdGhpcy5fbWVudSA9IG9wdGlvbnMubWVudTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5hZGRDbGFzcyhpbnRlcmFjdGl2ZUl0ZW0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciB0aGUgVGFiU3BhY2Ugc3RhdHVzIGl0ZW0uXG4gICAqL1xuICByZW5kZXIoKTogUmVhY3QuUmVhY3RFbGVtZW50PFRhYlNwYWNlQ29tcG9uZW50LklQcm9wcz4gfCBudWxsIHtcbiAgICBpZiAoIXRoaXMubW9kZWwgfHwgIXRoaXMubW9kZWwuY29uZmlnKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIChcbiAgICAgICAgPFRhYlNwYWNlQ29tcG9uZW50XG4gICAgICAgICAgaXNTcGFjZXM9e3RoaXMubW9kZWwuY29uZmlnLmluc2VydFNwYWNlc31cbiAgICAgICAgICB0YWJTcGFjZT17dGhpcy5tb2RlbC5jb25maWcudGFiU2l6ZX1cbiAgICAgICAgICBoYW5kbGVDbGljaz17KCkgPT4gdGhpcy5faGFuZGxlQ2xpY2soKX1cbiAgICAgICAgICB0cmFuc2xhdG9yPXt0aGlzLnRyYW5zbGF0b3J9XG4gICAgICAgIC8+XG4gICAgICApO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjbGljayBvbiB0aGUgc3RhdHVzIGl0ZW0uXG4gICAqL1xuICBwcml2YXRlIF9oYW5kbGVDbGljaygpOiB2b2lkIHtcbiAgICBjb25zdCBtZW51ID0gdGhpcy5fbWVudTtcbiAgICBpZiAodGhpcy5fcG9wdXApIHtcbiAgICAgIHRoaXMuX3BvcHVwLmRpc3Bvc2UoKTtcbiAgICB9XG5cbiAgICBtZW51LmFib3V0VG9DbG9zZS5jb25uZWN0KHRoaXMuX21lbnVDbG9zZWQsIHRoaXMpO1xuXG4gICAgdGhpcy5fcG9wdXAgPSBzaG93UG9wdXAoe1xuICAgICAgYm9keTogbWVudSxcbiAgICAgIGFuY2hvcjogdGhpcyxcbiAgICAgIGFsaWduOiAncmlnaHQnXG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9tZW51Q2xvc2VkKCk6IHZvaWQge1xuICAgIHRoaXMucmVtb3ZlQ2xhc3MoY2xpY2tlZEl0ZW0pO1xuICB9XG5cbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF9tZW51OiBNZW51O1xuICBwcml2YXRlIF9wb3B1cDogUG9wdXAgfCBudWxsID0gbnVsbDtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgVGFiU3BhY2Ugc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBUYWJTcGFjZVN0YXR1cyB7XG4gIC8qKlxuICAgKiBBIFZEb21Nb2RlbCBmb3IgdGhlIFRhYlNwYWNlIHN0YXR1cyBpdGVtLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIE1vZGVsIGV4dGVuZHMgVkRvbU1vZGVsIHtcbiAgICAvKipcbiAgICAgKiBUaGUgZWRpdG9yIGNvbmZpZyBmcm9tIHRoZSBzZXR0aW5ncyBzeXN0ZW0uXG4gICAgICovXG4gICAgZ2V0IGNvbmZpZygpOiBDb2RlRWRpdG9yLklDb25maWcgfCBudWxsIHtcbiAgICAgIHJldHVybiB0aGlzLl9jb25maWc7XG4gICAgfVxuICAgIHNldCBjb25maWcodmFsOiBDb2RlRWRpdG9yLklDb25maWcgfCBudWxsKSB7XG4gICAgICBjb25zdCBvbGRDb25maWcgPSB0aGlzLl9jb25maWc7XG4gICAgICB0aGlzLl9jb25maWcgPSB2YWw7XG4gICAgICB0aGlzLl90cmlnZ2VyQ2hhbmdlKG9sZENvbmZpZywgdGhpcy5fY29uZmlnKTtcbiAgICB9XG5cbiAgICBwcml2YXRlIF90cmlnZ2VyQ2hhbmdlKFxuICAgICAgb2xkVmFsdWU6IENvZGVFZGl0b3IuSUNvbmZpZyB8IG51bGwsXG4gICAgICBuZXdWYWx1ZTogQ29kZUVkaXRvci5JQ29uZmlnIHwgbnVsbFxuICAgICk6IHZvaWQge1xuICAgICAgY29uc3Qgb2xkU3BhY2VzID0gb2xkVmFsdWUgJiYgb2xkVmFsdWUuaW5zZXJ0U3BhY2VzO1xuICAgICAgY29uc3Qgb2xkU2l6ZSA9IG9sZFZhbHVlICYmIG9sZFZhbHVlLnRhYlNpemU7XG4gICAgICBjb25zdCBuZXdTcGFjZXMgPSBuZXdWYWx1ZSAmJiBuZXdWYWx1ZS5pbnNlcnRTcGFjZXM7XG4gICAgICBjb25zdCBuZXdTaXplID0gbmV3VmFsdWUgJiYgbmV3VmFsdWUudGFiU2l6ZTtcbiAgICAgIGlmIChvbGRTcGFjZXMgIT09IG5ld1NwYWNlcyB8fCBvbGRTaXplICE9PSBuZXdTaXplKSB7XG4gICAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICBwcml2YXRlIF9jb25maWc6IENvZGVFZGl0b3IuSUNvbmZpZyB8IG51bGwgPSBudWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIE9wdGlvbnMgZm9yIGNyZWF0aW5nIGEgVGFiU3BhY2Ugc3RhdHVzIGl0ZW0uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBBIG1lbnUgdG8gb3BlbiB3aGVuIGNsaWNraW5nIG9uIHRoZSBzdGF0dXMgaXRlbS4gVGhpcyBzaG91bGQgYWxsb3dcbiAgICAgKiB0aGUgdXNlciB0byBtYWtlIGEgZGlmZmVyZW50IHNlbGVjdGlvbiBhYm91dCB0YWJzL3NwYWNlcy5cbiAgICAgKi9cbiAgICBtZW51OiBNZW51O1xuXG4gICAgLyoqXG4gICAgICogTGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVdpZGdldFRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJRG9jdW1lbnRXaWRnZXQgfSBmcm9tICdAanVweXRlcmxhYi9kb2NyZWdpc3RyeSc7XG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IEZpbGVFZGl0b3IgfSBmcm9tICcuL3dpZGdldCc7XG5cbi8qKlxuICogQSBjbGFzcyB0aGF0IHRyYWNrcyBlZGl0b3Igd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJRWRpdG9yVHJhY2tlclxuICBleHRlbmRzIElXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4ge31cblxuLyogdHNsaW50OmRpc2FibGUgKi9cbi8qKlxuICogVGhlIGVkaXRvciB0cmFja2VyIHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSUVkaXRvclRyYWNrZXIgPSBuZXcgVG9rZW48SUVkaXRvclRyYWNrZXI+KFxuICAnQGp1cHl0ZXJsYWIvZmlsZWVkaXRvcjpJRWRpdG9yVHJhY2tlcidcbik7XG4vKiB0c2xpbnQ6ZW5hYmxlICovXG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7XG4gIENvZGVFZGl0b3IsXG4gIENvZGVFZGl0b3JXcmFwcGVyLFxuICBJRWRpdG9yTWltZVR5cGVTZXJ2aWNlLFxuICBJRWRpdG9yU2VydmljZXNcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQge1xuICBBQkNXaWRnZXRGYWN0b3J5LFxuICBEb2N1bWVudFJlZ2lzdHJ5LFxuICBEb2N1bWVudFdpZGdldCxcbiAgSURvY3VtZW50V2lkZ2V0XG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IHRleHRFZGl0b3JJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBQcm9taXNlRGVsZWdhdGUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgU3RhY2tlZExheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgZGF0YSBhdHRyaWJ1dGUgYWRkZWQgdG8gYSB3aWRnZXQgdGhhdCBjYW4gcnVuIGNvZGUuXG4gKi9cbmNvbnN0IENPREVfUlVOTkVSID0gJ2pwQ29kZVJ1bm5lcic7XG5cbi8qKlxuICogVGhlIGRhdGEgYXR0cmlidXRlIGFkZGVkIHRvIGEgd2lkZ2V0IHRoYXQgY2FuIHVuZG8uXG4gKi9cbmNvbnN0IFVORE9FUiA9ICdqcFVuZG9lcic7XG5cbi8qKlxuICogQSBjb2RlIGVkaXRvciB3cmFwcGVyIGZvciB0aGUgZmlsZSBlZGl0b3IuXG4gKi9cbmV4cG9ydCBjbGFzcyBGaWxlRWRpdG9yQ29kZVdyYXBwZXIgZXh0ZW5kcyBDb2RlRWRpdG9yV3JhcHBlciB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgZWRpdG9yIHdpZGdldC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IEZpbGVFZGl0b3IuSU9wdGlvbnMpIHtcbiAgICBzdXBlcih7XG4gICAgICBmYWN0b3J5OiBvcHRpb25zLmZhY3RvcnksXG4gICAgICBtb2RlbDogb3B0aW9ucy5jb250ZXh0Lm1vZGVsXG4gICAgfSk7XG5cbiAgICBjb25zdCBjb250ZXh0ID0gKHRoaXMuX2NvbnRleHQgPSBvcHRpb25zLmNvbnRleHQpO1xuICAgIGNvbnN0IGVkaXRvciA9IHRoaXMuZWRpdG9yO1xuXG4gICAgdGhpcy5hZGRDbGFzcygnanAtRmlsZUVkaXRvckNvZGVXcmFwcGVyJyk7XG4gICAgdGhpcy5ub2RlLmRhdGFzZXRbQ09ERV9SVU5ORVJdID0gJ3RydWUnO1xuICAgIHRoaXMubm9kZS5kYXRhc2V0W1VORE9FUl0gPSAndHJ1ZSc7XG5cbiAgICBlZGl0b3IubW9kZWwudmFsdWUudGV4dCA9IGNvbnRleHQubW9kZWwudG9TdHJpbmcoKTtcbiAgICB2b2lkIGNvbnRleHQucmVhZHkudGhlbigoKSA9PiB7XG4gICAgICB0aGlzLl9vbkNvbnRleHRSZWFkeSgpO1xuICAgIH0pO1xuXG4gICAgaWYgKGNvbnRleHQubW9kZWwubW9kZWxEQi5pc0NvbGxhYm9yYXRpdmUpIHtcbiAgICAgIGNvbnN0IG1vZGVsREIgPSBjb250ZXh0Lm1vZGVsLm1vZGVsREI7XG4gICAgICB2b2lkIG1vZGVsREIuY29ubmVjdGVkLnRoZW4oKCkgPT4ge1xuICAgICAgICBjb25zdCBjb2xsYWJvcmF0b3JzID0gbW9kZWxEQi5jb2xsYWJvcmF0b3JzO1xuICAgICAgICBpZiAoIWNvbGxhYm9yYXRvcnMpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICAvLyBTZXR1cCB0aGUgc2VsZWN0aW9uIHN0eWxlIGZvciBjb2xsYWJvcmF0b3JzXG4gICAgICAgIGNvbnN0IGxvY2FsQ29sbGFib3JhdG9yID0gY29sbGFib3JhdG9ycy5sb2NhbENvbGxhYm9yYXRvcjtcbiAgICAgICAgdGhpcy5lZGl0b3IudXVpZCA9IGxvY2FsQ29sbGFib3JhdG9yLnNlc3Npb25JZDtcblxuICAgICAgICB0aGlzLmVkaXRvci5zZWxlY3Rpb25TdHlsZSA9IHtcbiAgICAgICAgICAuLi5Db2RlRWRpdG9yLmRlZmF1bHRTZWxlY3Rpb25TdHlsZSxcbiAgICAgICAgICBjb2xvcjogbG9jYWxDb2xsYWJvcmF0b3IuY29sb3JcbiAgICAgICAgfTtcblxuICAgICAgICBjb2xsYWJvcmF0b3JzLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkNvbGxhYm9yYXRvcnNDaGFuZ2VkLCB0aGlzKTtcbiAgICAgICAgLy8gVHJpZ2dlciBhbiBpbml0aWFsIG9uQ29sbGFib3JhdG9yc0NoYW5nZWQgZXZlbnQuXG4gICAgICAgIHRoaXMuX29uQ29sbGFib3JhdG9yc0NoYW5nZWQoKTtcbiAgICAgIH0pO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGNvbnRleHQgZm9yIHRoZSBlZGl0b3Igd2lkZ2V0LlxuICAgKi9cbiAgZ2V0IGNvbnRleHQoKTogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0IHtcbiAgICByZXR1cm4gdGhpcy5fY29udGV4dDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBmaWxlIGVkaXRvciBpcyByZWFkeS5cbiAgICovXG4gIGdldCByZWFkeSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fcmVhZHkucHJvbWlzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYWN0aW9ucyB0aGF0IHNob3VsZCBiZSB0YWtlbiB3aGVuIHRoZSBjb250ZXh0IGlzIHJlYWR5LlxuICAgKi9cbiAgcHJpdmF0ZSBfb25Db250ZXh0UmVhZHkoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBjb250ZXh0TW9kZWwgPSB0aGlzLl9jb250ZXh0Lm1vZGVsO1xuICAgIGNvbnN0IGVkaXRvciA9IHRoaXMuZWRpdG9yO1xuICAgIGNvbnN0IGVkaXRvck1vZGVsID0gZWRpdG9yLm1vZGVsO1xuXG4gICAgLy8gU2V0IHRoZSBlZGl0b3IgbW9kZWwgdmFsdWUuXG4gICAgZWRpdG9yTW9kZWwudmFsdWUudGV4dCA9IGNvbnRleHRNb2RlbC50b1N0cmluZygpO1xuXG4gICAgLy8gUHJldmVudCB0aGUgaW5pdGlhbCBsb2FkaW5nIGZyb20gZGlzayBmcm9tIGJlaW5nIGluIHRoZSBlZGl0b3IgaGlzdG9yeS5cbiAgICBlZGl0b3IuY2xlYXJIaXN0b3J5KCk7XG5cbiAgICAvLyBXaXJlIHNpZ25hbCBjb25uZWN0aW9ucy5cbiAgICBjb250ZXh0TW9kZWwuY29udGVudENoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkNvbnRlbnRDaGFuZ2VkLCB0aGlzKTtcblxuICAgIC8vIFJlc29sdmUgdGhlIHJlYWR5IHByb21pc2UuXG4gICAgdGhpcy5fcmVhZHkucmVzb2x2ZSh1bmRlZmluZWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSBpbiBjb250ZXh0IG1vZGVsIGNvbnRlbnQuXG4gICAqL1xuICBwcml2YXRlIF9vbkNvbnRlbnRDaGFuZ2VkKCk6IHZvaWQge1xuICAgIGNvbnN0IGVkaXRvck1vZGVsID0gdGhpcy5lZGl0b3IubW9kZWw7XG4gICAgY29uc3Qgb2xkVmFsdWUgPSBlZGl0b3JNb2RlbC52YWx1ZS50ZXh0O1xuICAgIGNvbnN0IG5ld1ZhbHVlID0gdGhpcy5fY29udGV4dC5tb2RlbC50b1N0cmluZygpO1xuXG4gICAgaWYgKG9sZFZhbHVlICE9PSBuZXdWYWx1ZSkge1xuICAgICAgZWRpdG9yTW9kZWwudmFsdWUudGV4dCA9IG5ld1ZhbHVlO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIGNvbGxhYm9yYXRvcnMgb24gdGhlIG1vZGVsXG4gICAqIGJ5IHVwZGF0aW5nIFVJIGVsZW1lbnRzIGFzc29jaWF0ZWQgd2l0aCB0aGVtLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25Db2xsYWJvcmF0b3JzQ2hhbmdlZCgpOiB2b2lkIHtcbiAgICAvLyBJZiB0aGVyZSBhcmUgc2VsZWN0aW9ucyBjb3JyZXNwb25kaW5nIHRvIG5vbi1jb2xsYWJvcmF0b3JzLFxuICAgIC8vIHRoZXkgYXJlIHN0YWxlIGFuZCBzaG91bGQgYmUgcmVtb3ZlZC5cbiAgICBjb25zdCBjb2xsYWJvcmF0b3JzID0gdGhpcy5fY29udGV4dC5tb2RlbC5tb2RlbERCLmNvbGxhYm9yYXRvcnM7XG4gICAgaWYgKCFjb2xsYWJvcmF0b3JzKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGZvciAoY29uc3Qga2V5IG9mIHRoaXMuZWRpdG9yLm1vZGVsLnNlbGVjdGlvbnMua2V5cygpKSB7XG4gICAgICBpZiAoIWNvbGxhYm9yYXRvcnMuaGFzKGtleSkpIHtcbiAgICAgICAgdGhpcy5lZGl0b3IubW9kZWwuc2VsZWN0aW9ucy5kZWxldGUoa2V5KTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICBwcm90ZWN0ZWQgX2NvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dDtcbiAgcHJpdmF0ZSBfcmVhZHkgPSBuZXcgUHJvbWlzZURlbGVnYXRlPHZvaWQ+KCk7XG59XG5cbi8qKlxuICogQSB3aWRnZXQgZm9yIGVkaXRvcnMuXG4gKi9cbmV4cG9ydCBjbGFzcyBGaWxlRWRpdG9yIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBlZGl0b3Igd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogRmlsZUVkaXRvci5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtRmlsZUVkaXRvcicpO1xuXG4gICAgY29uc3QgY29udGV4dCA9ICh0aGlzLl9jb250ZXh0ID0gb3B0aW9ucy5jb250ZXh0KTtcbiAgICB0aGlzLl9taW1lVHlwZVNlcnZpY2UgPSBvcHRpb25zLm1pbWVUeXBlU2VydmljZTtcblxuICAgIGNvbnN0IGVkaXRvcldpZGdldCA9ICh0aGlzLmVkaXRvcldpZGdldCA9IG5ldyBGaWxlRWRpdG9yQ29kZVdyYXBwZXIoXG4gICAgICBvcHRpb25zXG4gICAgKSk7XG4gICAgdGhpcy5lZGl0b3IgPSBlZGl0b3JXaWRnZXQuZWRpdG9yO1xuICAgIHRoaXMubW9kZWwgPSBlZGl0b3JXaWRnZXQubW9kZWw7XG5cbiAgICAvLyBMaXN0ZW4gZm9yIGNoYW5nZXMgdG8gdGhlIHBhdGguXG4gICAgY29udGV4dC5wYXRoQ2hhbmdlZC5jb25uZWN0KHRoaXMuX29uUGF0aENoYW5nZWQsIHRoaXMpO1xuICAgIHRoaXMuX29uUGF0aENoYW5nZWQoKTtcblxuICAgIGNvbnN0IGxheW91dCA9ICh0aGlzLmxheW91dCA9IG5ldyBTdGFja2VkTGF5b3V0KCkpO1xuICAgIGxheW91dC5hZGRXaWRnZXQoZWRpdG9yV2lkZ2V0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGNvbnRleHQgZm9yIHRoZSBlZGl0b3Igd2lkZ2V0LlxuICAgKi9cbiAgZ2V0IGNvbnRleHQoKTogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0IHtcbiAgICByZXR1cm4gdGhpcy5lZGl0b3JXaWRnZXQuY29udGV4dDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBmaWxlIGVkaXRvciBpcyByZWFkeS5cbiAgICovXG4gIGdldCByZWFkeSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5lZGl0b3JXaWRnZXQucmVhZHk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBET00gZXZlbnRzIGZvciB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIG1ldGhvZCBpbXBsZW1lbnRzIHRoZSBET00gYEV2ZW50TGlzdGVuZXJgIGludGVyZmFjZSBhbmQgaXNcbiAgICogY2FsbGVkIGluIHJlc3BvbnNlIHRvIGV2ZW50cyBvbiB0aGUgd2lkZ2V0J3Mgbm9kZS4gSXQgc2hvdWxkXG4gICAqIG5vdCBiZSBjYWxsZWQgZGlyZWN0bHkgYnkgdXNlciBjb2RlLlxuICAgKi9cbiAgaGFuZGxlRXZlbnQoZXZlbnQ6IEV2ZW50KTogdm9pZCB7XG4gICAgaWYgKCF0aGlzLm1vZGVsKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHN3aXRjaCAoZXZlbnQudHlwZSkge1xuICAgICAgY2FzZSAnbW91c2Vkb3duJzpcbiAgICAgICAgdGhpcy5fZW5zdXJlRm9jdXMoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBhZnRlci1hdHRhY2hgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgc3VwZXIub25BZnRlckF0dGFjaChtc2cpO1xuICAgIGNvbnN0IG5vZGUgPSB0aGlzLm5vZGU7XG4gICAgbm9kZS5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGJlZm9yZS1kZXRhY2hgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQmVmb3JlRGV0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGNvbnN0IG5vZGUgPSB0aGlzLm5vZGU7XG4gICAgbm9kZS5yZW1vdmVFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhY3RpdmF0ZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fZW5zdXJlRm9jdXMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBFbnN1cmUgdGhhdCB0aGUgd2lkZ2V0IGhhcyBmb2N1cy5cbiAgICovXG4gIHByaXZhdGUgX2Vuc3VyZUZvY3VzKCk6IHZvaWQge1xuICAgIGlmICghdGhpcy5lZGl0b3IuaGFzRm9jdXMoKSkge1xuICAgICAgdGhpcy5lZGl0b3IuZm9jdXMoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSBwYXRoLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25QYXRoQ2hhbmdlZCgpOiB2b2lkIHtcbiAgICBjb25zdCBlZGl0b3IgPSB0aGlzLmVkaXRvcjtcbiAgICBjb25zdCBsb2NhbFBhdGggPSB0aGlzLl9jb250ZXh0LmxvY2FsUGF0aDtcblxuICAgIGVkaXRvci5tb2RlbC5taW1lVHlwZSA9IHRoaXMuX21pbWVUeXBlU2VydmljZS5nZXRNaW1lVHlwZUJ5RmlsZVBhdGgoXG4gICAgICBsb2NhbFBhdGhcbiAgICApO1xuICB9XG5cbiAgcHJpdmF0ZSBlZGl0b3JXaWRnZXQ6IEZpbGVFZGl0b3JDb2RlV3JhcHBlcjtcbiAgcHVibGljIG1vZGVsOiBDb2RlRWRpdG9yLklNb2RlbDtcbiAgcHVibGljIGVkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yO1xuICBwcm90ZWN0ZWQgX2NvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dDtcbiAgcHJpdmF0ZSBfbWltZVR5cGVTZXJ2aWNlOiBJRWRpdG9yTWltZVR5cGVTZXJ2aWNlO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGVkaXRvciB3aWRnZXQgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBGaWxlRWRpdG9yIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGFuIGVkaXRvciB3aWRnZXQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBBIGNvZGUgZWRpdG9yIGZhY3RvcnkuXG4gICAgICovXG4gICAgZmFjdG9yeTogQ29kZUVkaXRvci5GYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIG1pbWUgdHlwZSBzZXJ2aWNlIGZvciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIG1pbWVUeXBlU2VydmljZTogSUVkaXRvck1pbWVUeXBlU2VydmljZTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBkb2N1bWVudCBjb250ZXh0IGFzc29jaWF0ZWQgd2l0aCB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29kZUNvbnRleHQ7XG4gIH1cbn1cblxuLyoqXG4gKiBBIHdpZGdldCBmYWN0b3J5IGZvciBlZGl0b3JzLlxuICovXG5leHBvcnQgY2xhc3MgRmlsZUVkaXRvckZhY3RvcnkgZXh0ZW5kcyBBQkNXaWRnZXRGYWN0b3J5PFxuICBJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4sXG4gIERvY3VtZW50UmVnaXN0cnkuSUNvZGVNb2RlbFxuPiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgZWRpdG9yIHdpZGdldCBmYWN0b3J5LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogRmlsZUVkaXRvckZhY3RvcnkuSU9wdGlvbnMpIHtcbiAgICBzdXBlcihvcHRpb25zLmZhY3RvcnlPcHRpb25zKTtcbiAgICB0aGlzLl9zZXJ2aWNlcyA9IG9wdGlvbnMuZWRpdG9yU2VydmljZXM7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHdpZGdldCBnaXZlbiBhIGNvbnRleHQuXG4gICAqL1xuICBwcm90ZWN0ZWQgY3JlYXRlTmV3V2lkZ2V0KFxuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29kZUNvbnRleHRcbiAgKTogSURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+IHtcbiAgICBjb25zdCBmdW5jID0gdGhpcy5fc2VydmljZXMuZmFjdG9yeVNlcnZpY2UubmV3RG9jdW1lbnRFZGl0b3I7XG4gICAgY29uc3QgZmFjdG9yeTogQ29kZUVkaXRvci5GYWN0b3J5ID0gb3B0aW9ucyA9PiB7XG4gICAgICByZXR1cm4gZnVuYyhvcHRpb25zKTtcbiAgICB9O1xuICAgIGNvbnN0IGNvbnRlbnQgPSBuZXcgRmlsZUVkaXRvcih7XG4gICAgICBmYWN0b3J5LFxuICAgICAgY29udGV4dCxcbiAgICAgIG1pbWVUeXBlU2VydmljZTogdGhpcy5fc2VydmljZXMubWltZVR5cGVTZXJ2aWNlXG4gICAgfSk7XG5cbiAgICBjb250ZW50LnRpdGxlLmljb24gPSB0ZXh0RWRpdG9ySWNvbjtcbiAgICBjb25zdCB3aWRnZXQgPSBuZXcgRG9jdW1lbnRXaWRnZXQoeyBjb250ZW50LCBjb250ZXh0IH0pO1xuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cblxuICBwcml2YXRlIF9zZXJ2aWNlczogSUVkaXRvclNlcnZpY2VzO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGBGaWxlRWRpdG9yRmFjdG9yeWAgY2xhc3Mgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBGaWxlRWRpdG9yRmFjdG9yeSB7XG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB1c2VkIHRvIGNyZWF0ZSBhbiBlZGl0b3Igd2lkZ2V0IGZhY3RvcnkuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgZWRpdG9yIHNlcnZpY2VzIHVzZWQgYnkgdGhlIGZhY3RvcnkuXG4gICAgICovXG4gICAgZWRpdG9yU2VydmljZXM6IElFZGl0b3JTZXJ2aWNlcztcblxuICAgIC8qKlxuICAgICAqIFRoZSBmYWN0b3J5IG9wdGlvbnMgYXNzb2NpYXRlZCB3aXRoIHRoZSBmYWN0b3J5LlxuICAgICAqL1xuICAgIGZhY3RvcnlPcHRpb25zOiBEb2N1bWVudFJlZ2lzdHJ5LklXaWRnZXRGYWN0b3J5T3B0aW9uczxcbiAgICAgIElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPlxuICAgID47XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0=