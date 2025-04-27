(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_settingeditor_lib_index_js"],{

/***/ "../packages/settingeditor/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/settingeditor/lib/index.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SettingEditor": () => (/* reexport safe */ _settingeditor__WEBPACK_IMPORTED_MODULE_0__.SettingEditor),
/* harmony export */   "ISettingEditorTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_1__.ISettingEditorTracker)
/* harmony export */ });
/* harmony import */ var _settingeditor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./settingeditor */ "../packages/settingeditor/lib/settingeditor.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../packages/settingeditor/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module settingeditor
 */




/***/ }),

/***/ "../packages/settingeditor/lib/inspector.js":
/*!**************************************************!*\
  !*** ../packages/settingeditor/lib/inspector.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "createInspector": () => (/* binding */ createInspector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/inspector */ "webpack/sharing/consume/default/@jupyterlab/inspector/@jupyterlab/inspector");
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




/**
 * Create a raw editor inspector.
 */
function createInspector(editor, rendermime, translator) {
    translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
    const trans = translator.load('jupyterlab');
    const connector = new InspectorConnector(editor, translator);
    const inspector = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_0__.InspectorPanel({
        initialContent: trans.__('Any errors will be listed here'),
        translator: translator
    });
    const handler = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_0__.InspectionHandler({
        connector,
        rendermime: rendermime ||
            new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.RenderMimeRegistry({
                initialFactories: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.standardRendererFactories,
                translator: translator
            })
    });
    inspector.addClass('jp-SettingsDebug');
    inspector.source = handler;
    handler.editor = editor.source;
    return inspector;
}
/**
 * The data connector used to populate a code inspector.
 *
 * #### Notes
 * This data connector debounces fetch requests to throttle them at no more than
 * one request per 100ms. This means that using the connector to populate
 * multiple client objects can lead to missed fetch responses.
 */
class InspectorConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__.DataConnector {
    constructor(editor, translator) {
        super();
        this._current = 0;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        this._editor = editor;
        this._trans = this.translator.load('jupyterlab');
    }
    /**
     * Fetch inspection requests.
     */
    fetch(request) {
        return new Promise(resolve => {
            // Debounce requests at a rate of 100ms.
            const current = (this._current = window.setTimeout(() => {
                if (current !== this._current) {
                    return resolve(undefined);
                }
                const errors = this._validate(request.text);
                if (!errors) {
                    return resolve({
                        data: { 'text/markdown': this._trans.__('No errors found') },
                        metadata: {}
                    });
                }
                resolve({ data: Private.render(errors), metadata: {} });
            }, 100));
        });
    }
    _validate(raw) {
        const editor = this._editor;
        if (!editor.settings) {
            return null;
        }
        const { id, schema, version } = editor.settings;
        const data = { composite: {}, user: {} };
        const validator = editor.registry.validator;
        return validator.validateData({ data, id, raw, schema, version }, false);
    }
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Render validation errors as an HTML string.
     */
    function render(errors) {
        return { 'text/markdown': errors.map(renderError).join('') };
    }
    Private.render = render;
    /**
     * Render an individual validation error as a markdown string.
     */
    function renderError(error) {
        var _a;
        switch (error.keyword) {
            case 'additionalProperties':
                return `**\`[additional property error]\`**
          \`${(_a = error.params) === null || _a === void 0 ? void 0 : _a.additionalProperty}\` is not a valid property`;
            case 'syntax':
                return `**\`[syntax error]\`** *${error.message}*`;
            case 'type':
                return `**\`[type error]\`**
          \`${error.dataPath}\` ${error.message}`;
            default:
                return `**\`[error]\`** *${error.message}*`;
        }
    }
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/settingeditor/lib/plugineditor.js":
/*!*****************************************************!*\
  !*** ../packages/settingeditor/lib/plugineditor.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PluginEditor": () => (/* binding */ PluginEditor)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _raweditor__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./raweditor */ "../packages/settingeditor/lib/raweditor.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/






/**
 * The class name added to all plugin editors.
 */
const PLUGIN_EDITOR_CLASS = 'jp-PluginEditor';
/**
 * An individual plugin settings editor.
 */
class PluginEditor extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Create a new plugin editor.
     *
     * @param options - The plugin editor instantiation options.
     */
    constructor(options) {
        super();
        this._settings = null;
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this.addClass(PLUGIN_EDITOR_CLASS);
        const { commands, editorFactory, registry, rendermime, translator } = options;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        // TODO: Remove this layout. We were using this before when we
        // when we had a way to switch between the raw and table editor
        // Now, the raw editor is the only child and probably could merged into
        // this class directly in the future.
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.StackedLayout());
        const { onSaveError } = Private;
        this.raw = this._rawEditor = new _raweditor__WEBPACK_IMPORTED_MODULE_5__.RawEditor({
            commands,
            editorFactory,
            onSaveError,
            registry,
            rendermime,
            translator
        });
        this._rawEditor.handleMoved.connect(this._onStateChanged, this);
        layout.addWidget(this._rawEditor);
    }
    /**
     * Tests whether the settings have been modified and need saving.
     */
    get isDirty() {
        return this._rawEditor.isDirty;
    }
    /**
     * The plugin settings being edited.
     */
    get settings() {
        return this._settings;
    }
    set settings(settings) {
        if (this._settings === settings) {
            return;
        }
        const raw = this._rawEditor;
        this._settings = raw.settings = settings;
        this.update();
    }
    /**
     * The plugin editor layout state.
     */
    get state() {
        const plugin = this._settings ? this._settings.id : '';
        const { sizes } = this._rawEditor;
        return { plugin, sizes };
    }
    set state(state) {
        if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(this.state, state)) {
            return;
        }
        this._rawEditor.sizes = state.sizes;
        this.update();
    }
    /**
     * A signal that emits when editor layout state changes and needs to be saved.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * If the editor is in a dirty state, confirm that the user wants to leave.
     */
    confirm() {
        if (this.isHidden || !this.isAttached || !this.isDirty) {
            return Promise.resolve(undefined);
        }
        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
            title: this._trans.__('You have unsaved changes.'),
            body: this._trans.__('Do you want to leave without saving?'),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: this._trans.__('Cancel') }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: this._trans.__('Ok') })
            ]
        }).then(result => {
            if (!result.button.accept) {
                throw new Error('User canceled.');
            }
        });
    }
    /**
     * Dispose of the resources held by the plugin editor.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        this._rawEditor.dispose();
    }
    /**
     * Handle `after-attach` messages.
     */
    onAfterAttach(msg) {
        this.update();
    }
    /**
     * Handle `'update-request'` messages.
     */
    onUpdateRequest(msg) {
        const raw = this._rawEditor;
        const settings = this._settings;
        if (!settings) {
            this.hide();
            return;
        }
        this.show();
        raw.show();
    }
    /**
     * Handle layout state changes that need to be saved.
     */
    _onStateChanged() {
        this.stateChanged.emit(undefined);
    }
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Handle save errors.
     */
    function onSaveError(reason, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = translator.load('jupyterlab');
        console.error(`Saving setting editor value failed: ${reason.message}`);
        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
            title: trans.__('Your changes were not saved.'),
            body: reason.message,
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: trans.__('Ok') })]
        });
    }
    Private.onSaveError = onSaveError;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/settingeditor/lib/pluginlist.js":
/*!***************************************************!*\
  !*** ../packages/settingeditor/lib/pluginlist.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PluginList": () => (/* binding */ PluginList)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_5__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/






/**
 * A list of plugins with editable settings.
 */
class PluginList extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    /**
     * Create a new plugin list.
     */
    constructor(options) {
        super();
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._scrollTop = 0;
        this._selection = '';
        this.registry = options.registry;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        this.addClass('jp-PluginList');
        this._confirm = options.confirm;
        this.registry.pluginChanged.connect(() => {
            this.update();
        }, this);
    }
    /**
     * A signal emitted when a list user interaction happens.
     */
    get changed() {
        return this._changed;
    }
    /**
     * The selection value of the plugin list.
     */
    get scrollTop() {
        var _a;
        return (_a = this.node.querySelector('ul')) === null || _a === void 0 ? void 0 : _a.scrollTop;
    }
    /**
     * The selection value of the plugin list.
     */
    get selection() {
        return this._selection;
    }
    set selection(selection) {
        if (this._selection === selection) {
            return;
        }
        this._selection = selection;
        this.update();
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the plugin list's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'mousedown':
                this._evtMousedown(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `'after-attach'` messages.
     */
    onAfterAttach(msg) {
        this.node.addEventListener('mousedown', this);
        this.update();
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        this.node.removeEventListener('mousedown', this);
    }
    /**
     * Handle `'update-request'` messages.
     */
    onUpdateRequest(msg) {
        const { node, registry } = this;
        const selection = this._selection;
        const translation = this.translator;
        Private.populateList(registry, selection, node, translation);
        const ul = node.querySelector('ul');
        if (ul && this._scrollTop !== undefined) {
            ul.scrollTop = this._scrollTop;
        }
    }
    /**
     * Handle the `'mousedown'` event for the plugin list.
     *
     * @param event - The DOM event sent to the widget
     */
    _evtMousedown(event) {
        event.preventDefault();
        let target = event.target;
        let id = target.getAttribute('data-id');
        if (id === this._selection) {
            return;
        }
        if (!id) {
            while (!id && target !== this.node) {
                target = target.parentElement;
                id = target.getAttribute('data-id');
            }
        }
        if (!id) {
            return;
        }
        this._confirm()
            .then(() => {
            this._scrollTop = this.scrollTop;
            this._selection = id;
            this._changed.emit(undefined);
            this.update();
        })
            .catch(() => {
            /* no op */
        });
    }
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * The JupyterLab plugin schema key for the setting editor
     * icon class of a plugin.
     */
    const ICON_KEY = 'jupyter.lab.setting-icon';
    /**
     * The JupyterLab plugin schema key for the setting editor
     * icon class of a plugin.
     */
    const ICON_CLASS_KEY = 'jupyter.lab.setting-icon-class';
    /**
     * The JupyterLab plugin schema key for the setting editor
     * icon label of a plugin.
     */
    const ICON_LABEL_KEY = 'jupyter.lab.setting-icon-label';
    /**
     * Check the plugin for a rendering hint's value.
     *
     * #### Notes
     * The order of priority for overridden hints is as follows, from most
     * important to least:
     * 1. Data set by the end user in a settings file.
     * 2. Data set by the plugin author as a schema default.
     * 3. Data set by the plugin author as a top-level key of the schema.
     */
    function getHint(key, registry, plugin) {
        // First, give priority to checking if the hint exists in the user data.
        let hint = plugin.data.user[key];
        // Second, check to see if the hint exists in composite data, which folds
        // in default values from the schema.
        if (!hint) {
            hint = plugin.data.composite[key];
        }
        // Third, check to see if the plugin schema has defined the hint.
        if (!hint) {
            hint = plugin.schema[key];
        }
        // Finally, use the defaults from the registry schema.
        if (!hint) {
            const { properties } = registry.schema;
            hint = properties && properties[key] && properties[key].default;
        }
        return typeof hint === 'string' ? hint : '';
    }
    /**
     * Populate the plugin list.
     */
    function populateList(registry, selection, node, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const plugins = sortPlugins(registry).filter(plugin => {
            const { schema } = plugin;
            const deprecated = schema['jupyter.lab.setting-deprecated'] === true;
            const editable = Object.keys(schema.properties || {}).length > 0;
            const extensible = schema.additionalProperties !== false;
            return !deprecated && (editable || extensible);
        });
        const items = plugins.map(plugin => {
            const { id, schema, version } = plugin;
            const title = typeof schema.title === 'string'
                ? trans._p('schema', schema.title)
                : id;
            const description = typeof schema.description === 'string'
                ? trans._p('schema', schema.description)
                : '';
            const itemTitle = `${description}\n${id}\n${version}`;
            const icon = getHint(ICON_KEY, registry, plugin);
            const iconClass = getHint(ICON_CLASS_KEY, registry, plugin);
            const iconTitle = getHint(ICON_LABEL_KEY, registry, plugin);
            return (react__WEBPACK_IMPORTED_MODULE_4__.createElement("li", { className: id === selection ? 'jp-mod-selected' : '', "data-id": id, key: id, title: itemTitle },
                react__WEBPACK_IMPORTED_MODULE_4__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon.resolveReact, { icon: icon || (iconClass ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.settingsIcon), iconClass: (0,_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.classes)(iconClass, 'jp-Icon'), title: iconTitle, tag: "span", stylesheet: "settingsEditor" }),
                react__WEBPACK_IMPORTED_MODULE_4__.createElement("span", null, title)));
        });
        react_dom__WEBPACK_IMPORTED_MODULE_5__.unmountComponentAtNode(node);
        react_dom__WEBPACK_IMPORTED_MODULE_5__.render(react__WEBPACK_IMPORTED_MODULE_4__.createElement("ul", null, items), node);
    }
    Private.populateList = populateList;
    /**
     * Sort a list of plugins by title and ID.
     */
    function sortPlugins(registry) {
        return Object.keys(registry.plugins)
            .map(plugin => registry.plugins[plugin])
            .sort((a, b) => {
            return (a.schema.title || a.id).localeCompare(b.schema.title || b.id);
        });
    }
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/settingeditor/lib/raweditor.js":
/*!**************************************************!*\
  !*** ../packages/settingeditor/lib/raweditor.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RawEditor": () => (/* binding */ RawEditor)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _inspector__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./inspector */ "../packages/settingeditor/lib/inspector.js");
/* harmony import */ var _splitpanel__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./splitpanel */ "../packages/settingeditor/lib/splitpanel.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * A class name added to all raw editors.
 */
const RAW_EDITOR_CLASS = 'jp-SettingsRawEditor';
/**
 * A class name added to the user settings editor.
 */
const USER_CLASS = 'jp-SettingsRawEditor-user';
/**
 * A class name added to the user editor when there are validation errors.
 */
const ERROR_CLASS = 'jp-mod-error';
/**
 * A raw JSON settings editor.
 */
class RawEditor extends _splitpanel__WEBPACK_IMPORTED_MODULE_5__.SplitPanel {
    /**
     * Create a new plugin editor.
     */
    constructor(options) {
        super({
            orientation: 'horizontal',
            renderer: _splitpanel__WEBPACK_IMPORTED_MODULE_5__.SplitPanel.defaultRenderer,
            spacing: 1
        });
        this._canRevert = false;
        this._canSave = false;
        this._commandsChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._settings = null;
        this._toolbar = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar();
        const { commands, editorFactory, registry, translator } = options;
        this.registry = registry;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this._commands = commands;
        // Create read-only defaults editor.
        const defaults = (this._defaults = new _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.CodeEditorWrapper({
            model: new _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.CodeEditor.Model(),
            factory: editorFactory
        }));
        defaults.editor.model.value.text = '';
        defaults.editor.model.mimeType = 'text/javascript';
        defaults.editor.setOption('readOnly', true);
        // Create read-write user settings editor.
        const user = (this._user = new _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.CodeEditorWrapper({
            model: new _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.CodeEditor.Model(),
            factory: editorFactory,
            config: { lineNumbers: true }
        }));
        user.addClass(USER_CLASS);
        user.editor.model.mimeType = 'text/javascript';
        user.editor.model.value.changed.connect(this._onTextChanged, this);
        // Create and set up an inspector.
        this._inspector = (0,_inspector__WEBPACK_IMPORTED_MODULE_6__.createInspector)(this, options.rendermime, this.translator);
        this.addClass(RAW_EDITOR_CLASS);
        // FIXME-TRANS: onSaveError must have an optional translator?
        this._onSaveError = options.onSaveError;
        this.addWidget(Private.defaultsEditor(defaults, this.translator));
        this.addWidget(Private.userEditor(user, this._toolbar, this._inspector, this.translator));
    }
    /**
     * Whether the raw editor revert functionality is enabled.
     */
    get canRevert() {
        return this._canRevert;
    }
    /**
     * Whether the raw editor save functionality is enabled.
     */
    get canSave() {
        return this._canSave;
    }
    /**
     * Emits when the commands passed in at instantiation change.
     */
    get commandsChanged() {
        return this._commandsChanged;
    }
    /**
     * Tests whether the settings have been modified and need saving.
     */
    get isDirty() {
        var _a, _b;
        return (_b = this._user.editor.model.value.text !== ((_a = this._settings) === null || _a === void 0 ? void 0 : _a.raw)) !== null && _b !== void 0 ? _b : '';
    }
    /**
     * The plugin settings being edited.
     */
    get settings() {
        return this._settings;
    }
    set settings(settings) {
        if (!settings && !this._settings) {
            return;
        }
        const samePlugin = settings && this._settings && settings.plugin === this._settings.plugin;
        if (samePlugin) {
            return;
        }
        const defaults = this._defaults;
        const user = this._user;
        // Disconnect old settings change handler.
        if (this._settings) {
            this._settings.changed.disconnect(this._onSettingsChanged, this);
        }
        if (settings) {
            this._settings = settings;
            this._settings.changed.connect(this._onSettingsChanged, this);
            this._onSettingsChanged();
        }
        else {
            this._settings = null;
            defaults.editor.model.value.text = '';
            user.editor.model.value.text = '';
        }
        this.update();
    }
    /**
     * Get the relative sizes of the two editor panels.
     */
    get sizes() {
        return this.relativeSizes();
    }
    set sizes(sizes) {
        this.setRelativeSizes(sizes);
    }
    /**
     * The inspectable source editor for user input.
     */
    get source() {
        return this._user.editor;
    }
    /**
     * Dispose of the resources held by the raw editor.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        this._defaults.dispose();
        this._user.dispose();
    }
    /**
     * Revert the editor back to original settings.
     */
    revert() {
        var _a, _b;
        this._user.editor.model.value.text = (_b = (_a = this.settings) === null || _a === void 0 ? void 0 : _a.raw) !== null && _b !== void 0 ? _b : '';
        this._updateToolbar(false, false);
    }
    /**
     * Save the contents of the raw editor.
     */
    save() {
        if (!this.isDirty || !this._settings) {
            return Promise.resolve(undefined);
        }
        const settings = this._settings;
        const source = this._user.editor.model.value.text;
        return settings
            .save(source)
            .then(() => {
            this._updateToolbar(false, false);
        })
            .catch(reason => {
            this._updateToolbar(true, false);
            this._onSaveError(reason, this.translator);
        });
    }
    /**
     * Handle `after-attach` messages.
     */
    onAfterAttach(msg) {
        Private.populateToolbar(this._commands, this._toolbar);
        this.update();
    }
    /**
     * Handle `'update-request'` messages.
     */
    onUpdateRequest(msg) {
        const settings = this._settings;
        const defaults = this._defaults;
        const user = this._user;
        if (settings) {
            defaults.editor.refresh();
            user.editor.refresh();
        }
    }
    /**
     * Handle text changes in the underlying editor.
     */
    _onTextChanged() {
        const raw = this._user.editor.model.value.text;
        const settings = this._settings;
        this.removeClass(ERROR_CLASS);
        // If there are no settings loaded or there are no changes, bail.
        if (!settings || settings.raw === raw) {
            this._updateToolbar(false, false);
            return;
        }
        const errors = settings.validate(raw);
        if (errors) {
            this.addClass(ERROR_CLASS);
            this._updateToolbar(true, false);
            return;
        }
        this._updateToolbar(true, true);
    }
    /**
     * Handle updates to the settings.
     */
    _onSettingsChanged() {
        var _a, _b;
        const settings = this._settings;
        const defaults = this._defaults;
        const user = this._user;
        defaults.editor.model.value.text = (_a = settings === null || settings === void 0 ? void 0 : settings.annotatedDefaults()) !== null && _a !== void 0 ? _a : '';
        user.editor.model.value.text = (_b = settings === null || settings === void 0 ? void 0 : settings.raw) !== null && _b !== void 0 ? _b : '';
    }
    _updateToolbar(revert = this._canRevert, save = this._canSave) {
        const commands = this._commands;
        this._canRevert = revert;
        this._canSave = save;
        this._commandsChanged.emit([commands.revert, commands.save]);
    }
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Returns the wrapped setting defaults editor.
     */
    function defaultsEditor(editor, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget();
        const layout = (widget.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.BoxLayout({ spacing: 0 }));
        const banner = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget();
        const bar = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar();
        const defaultTitle = trans.__('System Defaults');
        banner.node.innerText = defaultTitle;
        bar.insertItem(0, 'banner', banner);
        layout.addWidget(bar);
        layout.addWidget(editor);
        return widget;
    }
    Private.defaultsEditor = defaultsEditor;
    /**
     * Populate the raw editor toolbar.
     */
    function populateToolbar(commands, toolbar) {
        const { registry, revert, save } = commands;
        toolbar.addItem('spacer', _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar.createSpacerItem());
        // Note the button order. The rationale here is that no matter what state
        // the toolbar is in, the relative location of the revert button in the
        // toolbar remains the same.
        [revert, save].forEach(name => {
            const item = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.CommandToolbarButton({ commands: registry, id: name });
            toolbar.addItem(name, item);
        });
    }
    Private.populateToolbar = populateToolbar;
    /**
     * Returns the wrapped user overrides editor.
     */
    function userEditor(editor, toolbar, inspector, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const userTitle = trans.__('User Preferences');
        const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget();
        const layout = (widget.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.BoxLayout({ spacing: 0 }));
        const banner = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget();
        banner.node.innerText = userTitle;
        toolbar.insertItem(0, 'banner', banner);
        layout.addWidget(toolbar);
        layout.addWidget(editor);
        layout.addWidget(inspector);
        return widget;
    }
    Private.userEditor = userEditor;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/settingeditor/lib/settingeditor.js":
/*!******************************************************!*\
  !*** ../packages/settingeditor/lib/settingeditor.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SettingEditor": () => (/* binding */ SettingEditor)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _plugineditor__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./plugineditor */ "../packages/settingeditor/lib/plugineditor.js");
/* harmony import */ var _pluginlist__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./pluginlist */ "../packages/settingeditor/lib/pluginlist.js");
/* harmony import */ var _splitpanel__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./splitpanel */ "../packages/settingeditor/lib/splitpanel.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/









/**
 * The ratio panes in the setting editor.
 */
const DEFAULT_LAYOUT = {
    sizes: [1, 3],
    container: {
        editor: 'raw',
        plugin: '',
        sizes: [1, 1]
    }
};
/**
 * An interface for modifying and saving application settings.
 */
class SettingEditor extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    /**
     * Create a new setting editor.
     */
    constructor(options) {
        super();
        this._fetching = null;
        this._saving = false;
        this._state = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepCopy(DEFAULT_LAYOUT);
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        this.addClass('jp-SettingEditor');
        this.key = options.key;
        this.state = options.state;
        const { commands, editorFactory, rendermime } = options;
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.PanelLayout());
        const registry = (this.registry = options.registry);
        const panel = (this._panel = new _splitpanel__WEBPACK_IMPORTED_MODULE_6__.SplitPanel({
            orientation: 'horizontal',
            renderer: _splitpanel__WEBPACK_IMPORTED_MODULE_6__.SplitPanel.defaultRenderer,
            spacing: 1
        }));
        const instructions = (this._instructions = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget());
        const editor = (this._editor = new _plugineditor__WEBPACK_IMPORTED_MODULE_7__.PluginEditor({
            commands,
            editorFactory,
            registry,
            rendermime,
            translator: this.translator
        }));
        const confirm = () => editor.confirm();
        const list = (this._list = new _pluginlist__WEBPACK_IMPORTED_MODULE_8__.PluginList({
            confirm,
            registry,
            translator: this.translator
        }));
        const when = options.when;
        instructions.addClass('jp-SettingEditorInstructions');
        Private.populateInstructionsNode(instructions.node, this.translator);
        if (when) {
            this._when = Array.isArray(when) ? Promise.all(when) : when;
        }
        panel.addClass('jp-SettingEditor-main');
        layout.addWidget(panel);
        panel.addWidget(list);
        panel.addWidget(instructions);
        _splitpanel__WEBPACK_IMPORTED_MODULE_6__.SplitPanel.setStretch(list, 0);
        _splitpanel__WEBPACK_IMPORTED_MODULE_6__.SplitPanel.setStretch(instructions, 1);
        _splitpanel__WEBPACK_IMPORTED_MODULE_6__.SplitPanel.setStretch(editor, 1);
        editor.stateChanged.connect(this._onStateChanged, this);
        list.changed.connect(this._onStateChanged, this);
        panel.handleMoved.connect(this._onStateChanged, this);
    }
    /**
     * Whether the raw editor revert functionality is enabled.
     */
    get canRevertRaw() {
        return this._editor.raw.canRevert;
    }
    /**
     * Whether the raw editor save functionality is enabled.
     */
    get canSaveRaw() {
        return this._editor.raw.canSave;
    }
    /**
     * Emits when the commands passed in at instantiation change.
     */
    get commandsChanged() {
        return this._editor.raw.commandsChanged;
    }
    /**
     * The currently loaded settings.
     */
    get settings() {
        return this._editor.settings;
    }
    /**
     * The inspectable raw user editor source for the currently loaded settings.
     */
    get source() {
        return this._editor.raw.source;
    }
    /**
     * Dispose of the resources held by the setting editor.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        this._editor.dispose();
        this._instructions.dispose();
        this._list.dispose();
        this._panel.dispose();
    }
    /**
     * Revert raw editor back to original settings.
     */
    revert() {
        this._editor.raw.revert();
    }
    /**
     * Save the contents of the raw editor.
     */
    save() {
        return this._editor.raw.save();
    }
    /**
     * Handle `'after-attach'` messages.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        this._panel.hide();
        this._fetchState()
            .then(() => {
            this._panel.show();
            this._setState();
        })
            .catch(reason => {
            console.error('Fetching setting editor state failed', reason);
            this._panel.show();
            this._setState();
        });
    }
    /**
     * Handle `'close-request'` messages.
     */
    onCloseRequest(msg) {
        this._editor
            .confirm()
            .then(() => {
            super.onCloseRequest(msg);
            this.dispose();
        })
            .catch(() => {
            /* no op */
        });
    }
    /**
     * Get the state of the panel.
     */
    _fetchState() {
        if (this._fetching) {
            return this._fetching;
        }
        const { key, state } = this;
        const promises = [state.fetch(key), this._when];
        return (this._fetching = Promise.all(promises).then(([value]) => {
            this._fetching = null;
            if (this._saving) {
                return;
            }
            this._state = Private.normalizeState(value, this._state);
        }));
    }
    /**
     * Handle root level layout state changes.
     */
    async _onStateChanged() {
        this._state.sizes = this._panel.relativeSizes();
        this._state.container = this._editor.state;
        this._state.container.plugin = this._list.selection;
        try {
            await this._saveState();
        }
        catch (error) {
            console.error('Saving setting editor state failed', error);
        }
        this._setState();
    }
    /**
     * Set the state of the setting editor.
     */
    async _saveState() {
        const { key, state } = this;
        const value = this._state;
        this._saving = true;
        try {
            await state.save(key, value);
            this._saving = false;
        }
        catch (error) {
            this._saving = false;
            throw error;
        }
    }
    /**
     * Set the layout sizes.
     */
    _setLayout() {
        const editor = this._editor;
        const panel = this._panel;
        const state = this._state;
        editor.state = state.container;
        // Allow the message queue (which includes fit requests that might disrupt
        // setting relative sizes) to clear before setting sizes.
        requestAnimationFrame(() => {
            panel.setRelativeSizes(state.sizes);
        });
    }
    /**
     * Set the presets of the setting editor.
     */
    _setState() {
        const editor = this._editor;
        const list = this._list;
        const panel = this._panel;
        const { container } = this._state;
        if (!container.plugin) {
            editor.settings = null;
            list.selection = '';
            this._setLayout();
            return;
        }
        if (editor.settings && editor.settings.id === container.plugin) {
            this._setLayout();
            return;
        }
        const instructions = this._instructions;
        this.registry
            .load(container.plugin)
            .then(settings => {
            if (instructions.isAttached) {
                instructions.parent = null;
            }
            if (!editor.isAttached) {
                panel.addWidget(editor);
            }
            editor.settings = settings;
            list.selection = container.plugin;
            this._setLayout();
        })
            .catch(reason => {
            console.error(`Loading ${container.plugin} settings failed.`, reason);
            list.selection = this._state.container.plugin = '';
            editor.settings = null;
            this._setLayout();
        });
    }
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Populate the instructions text node.
     */
    function populateInstructionsNode(node, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        const trans = translator.load('jupyterlab');
        react_dom__WEBPACK_IMPORTED_MODULE_5__.render(react__WEBPACK_IMPORTED_MODULE_4__.createElement(react__WEBPACK_IMPORTED_MODULE_4__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_4__.createElement("h2", null,
                react__WEBPACK_IMPORTED_MODULE_4__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.jupyterIcon.react, { className: "jp-SettingEditorInstructions-icon", tag: "span", elementPosition: "center", height: "auto", width: "60px" }),
                react__WEBPACK_IMPORTED_MODULE_4__.createElement("span", { className: "jp-SettingEditorInstructions-title" }, "Settings")),
            react__WEBPACK_IMPORTED_MODULE_4__.createElement("span", { className: "jp-SettingEditorInstructions-text" }, trans.__('Select a plugin from the list to view and edit its preferences.'))), node);
    }
    Private.populateInstructionsNode = populateInstructionsNode;
    /**
     * Return a normalized restored layout state that defaults to the presets.
     */
    function normalizeState(saved, current) {
        if (!saved) {
            return _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepCopy(DEFAULT_LAYOUT);
        }
        if (!('sizes' in saved) || !numberArray(saved.sizes)) {
            saved.sizes = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepCopy(DEFAULT_LAYOUT.sizes);
        }
        if (!('container' in saved)) {
            saved.container = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepCopy(DEFAULT_LAYOUT.container);
            return saved;
        }
        const container = 'container' in saved &&
            saved.container &&
            typeof saved.container === 'object'
            ? saved.container
            : {};
        saved.container = {
            plugin: typeof container.plugin === 'string'
                ? container.plugin
                : DEFAULT_LAYOUT.container.plugin,
            sizes: numberArray(container.sizes)
                ? container.sizes
                : _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepCopy(DEFAULT_LAYOUT.container.sizes)
        };
        return saved;
    }
    Private.normalizeState = normalizeState;
    /**
     * Tests whether an array consists exclusively of numbers.
     */
    function numberArray(value) {
        return Array.isArray(value) && value.every(x => typeof x === 'number');
    }
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/settingeditor/lib/splitpanel.js":
/*!***************************************************!*\
  !*** ../packages/settingeditor/lib/splitpanel.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SplitPanel": () => (/* binding */ SplitPanel)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/


/**
 * A deprecated split panel that will be removed when the phosphor split panel
 * supports a handle moved signal. See https://github.com/phosphorjs/phosphor/issues/297.
 */
class SplitPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.SplitPanel {
    constructor() {
        super(...arguments);
        /**
         * Emits when the split handle has moved.
         */
        this.handleMoved = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
    }
    handleEvent(event) {
        super.handleEvent(event);
        if (event.type === 'mouseup') {
            this.handleMoved.emit(undefined);
        }
    }
}


/***/ }),

/***/ "../packages/settingeditor/lib/tokens.js":
/*!***********************************************!*\
  !*** ../packages/settingeditor/lib/tokens.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ISettingEditorTracker": () => (/* binding */ ISettingEditorTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/* tslint:disable */
/**
 * The setting editor tracker token.
 */
const ISettingEditorTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/settingeditor:ISettingEditorTracker');


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2V0dGluZ2VkaXRvci9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3NldHRpbmdlZGl0b3Ivc3JjL2luc3BlY3Rvci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2V0dGluZ2VkaXRvci9zcmMvcGx1Z2luZWRpdG9yLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zZXR0aW5nZWRpdG9yL3NyYy9wbHVnaW5saXN0LnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2V0dGluZ2VkaXRvci9zcmMvcmF3ZWRpdG9yLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zZXR0aW5nZWRpdG9yL3NyYy9zZXR0aW5nZWRpdG9yLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2V0dGluZ2VkaXRvci9zcmMvc3BsaXRwYW5lbC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2V0dGluZ2VkaXRvci9zcmMvdG9rZW5zLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQUU2QjtBQUNQOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNSekI7OzsrRUFHK0U7QUFFTDtBQUsxQztBQUVvQjtBQUtuQjtBQUlqQzs7R0FFRztBQUNJLFNBQVMsZUFBZSxDQUM3QixNQUFpQixFQUNqQixVQUFnQyxFQUNoQyxVQUF3QjtJQUV4QixVQUFVLEdBQUcsVUFBVSxJQUFJLG1FQUFjLENBQUM7SUFDMUMsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUM1QyxNQUFNLFNBQVMsR0FBRyxJQUFJLGtCQUFrQixDQUFDLE1BQU0sRUFBRSxVQUFVLENBQUMsQ0FBQztJQUM3RCxNQUFNLFNBQVMsR0FBRyxJQUFJLGlFQUFjLENBQUM7UUFDbkMsY0FBYyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsZ0NBQWdDLENBQUM7UUFDMUQsVUFBVSxFQUFFLFVBQVU7S0FDdkIsQ0FBQyxDQUFDO0lBQ0gsTUFBTSxPQUFPLEdBQUcsSUFBSSxvRUFBaUIsQ0FBQztRQUNwQyxTQUFTO1FBQ1QsVUFBVSxFQUNSLFVBQVU7WUFDVixJQUFJLHNFQUFrQixDQUFDO2dCQUNyQixnQkFBZ0IsRUFBRSw2RUFBeUI7Z0JBQzNDLFVBQVUsRUFBRSxVQUFVO2FBQ3ZCLENBQUM7S0FDTCxDQUFDLENBQUM7SUFFSCxTQUFTLENBQUMsUUFBUSxDQUFDLGtCQUFrQixDQUFDLENBQUM7SUFDdkMsU0FBUyxDQUFDLE1BQU0sR0FBRyxPQUFPLENBQUM7SUFDM0IsT0FBTyxDQUFDLE1BQU0sR0FBRyxNQUFNLENBQUMsTUFBTSxDQUFDO0lBRS9CLE9BQU8sU0FBUyxDQUFDO0FBQ25CLENBQUM7QUFFRDs7Ozs7OztHQU9HO0FBQ0gsTUFBTSxrQkFBbUIsU0FBUSw4REFJaEM7SUFDQyxZQUFZLE1BQWlCLEVBQUUsVUFBd0I7UUFDckQsS0FBSyxFQUFFLENBQUM7UUErQ0YsYUFBUSxHQUFHLENBQUMsQ0FBQztRQTlDbkIsSUFBSSxDQUFDLFVBQVUsR0FBRyxVQUFVLElBQUksbUVBQWMsQ0FBQztRQUMvQyxJQUFJLENBQUMsT0FBTyxHQUFHLE1BQU0sQ0FBQztRQUN0QixJQUFJLENBQUMsTUFBTSxHQUFHLElBQUksQ0FBQyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO0lBQ25ELENBQUM7SUFFRDs7T0FFRztJQUNILEtBQUssQ0FDSCxPQUFtQztRQUVuQyxPQUFPLElBQUksT0FBTyxDQUF1QyxPQUFPLENBQUMsRUFBRTtZQUNqRSx3Q0FBd0M7WUFDeEMsTUFBTSxPQUFPLEdBQUcsQ0FBQyxJQUFJLENBQUMsUUFBUSxHQUFHLE1BQU0sQ0FBQyxVQUFVLENBQUMsR0FBRyxFQUFFO2dCQUN0RCxJQUFJLE9BQU8sS0FBSyxJQUFJLENBQUMsUUFBUSxFQUFFO29CQUM3QixPQUFPLE9BQU8sQ0FBQyxTQUFTLENBQUMsQ0FBQztpQkFDM0I7Z0JBRUQsTUFBTSxNQUFNLEdBQUcsSUFBSSxDQUFDLFNBQVMsQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLENBQUM7Z0JBRTVDLElBQUksQ0FBQyxNQUFNLEVBQUU7b0JBQ1gsT0FBTyxPQUFPLENBQUM7d0JBQ2IsSUFBSSxFQUFFLEVBQUUsZUFBZSxFQUFFLElBQUksQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLGlCQUFpQixDQUFDLEVBQUU7d0JBQzVELFFBQVEsRUFBRSxFQUFFO3FCQUNiLENBQUMsQ0FBQztpQkFDSjtnQkFFRCxPQUFPLENBQUMsRUFBRSxJQUFJLEVBQUUsT0FBTyxDQUFDLE1BQU0sQ0FBQyxNQUFNLENBQUMsRUFBRSxRQUFRLEVBQUUsRUFBRSxFQUFFLENBQUMsQ0FBQztZQUMxRCxDQUFDLEVBQUUsR0FBRyxDQUFDLENBQUMsQ0FBQztRQUNYLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVPLFNBQVMsQ0FBQyxHQUFXO1FBQzNCLE1BQU0sTUFBTSxHQUFHLElBQUksQ0FBQyxPQUFPLENBQUM7UUFDNUIsSUFBSSxDQUFDLE1BQU0sQ0FBQyxRQUFRLEVBQUU7WUFDcEIsT0FBTyxJQUFJLENBQUM7U0FDYjtRQUNELE1BQU0sRUFBRSxFQUFFLEVBQUUsTUFBTSxFQUFFLE9BQU8sRUFBRSxHQUFHLE1BQU0sQ0FBQyxRQUFRLENBQUM7UUFDaEQsTUFBTSxJQUFJLEdBQUcsRUFBRSxTQUFTLEVBQUUsRUFBRSxFQUFFLElBQUksRUFBRSxFQUFFLEVBQUUsQ0FBQztRQUN6QyxNQUFNLFNBQVMsR0FBRyxNQUFNLENBQUMsUUFBUSxDQUFDLFNBQVMsQ0FBQztRQUU1QyxPQUFPLFNBQVMsQ0FBQyxZQUFZLENBQUMsRUFBRSxJQUFJLEVBQUUsRUFBRSxFQUFFLEdBQUcsRUFBRSxNQUFNLEVBQUUsT0FBTyxFQUFFLEVBQUUsS0FBSyxDQUFDLENBQUM7SUFDM0UsQ0FBQztDQU1GO0FBRUQ7O0dBRUc7QUFDSCxJQUFVLE9BQU8sQ0EyQmhCO0FBM0JELFdBQVUsT0FBTztJQUNmOztPQUVHO0lBQ0gsU0FBZ0IsTUFBTSxDQUNwQixNQUFpQztRQUVqQyxPQUFPLEVBQUUsZUFBZSxFQUFFLE1BQU0sQ0FBQyxHQUFHLENBQUMsV0FBVyxDQUFDLENBQUMsSUFBSSxDQUFDLEVBQUUsQ0FBQyxFQUFFLENBQUM7SUFDL0QsQ0FBQztJQUplLGNBQU0sU0FJckI7SUFFRDs7T0FFRztJQUNILFNBQVMsV0FBVyxDQUFDLEtBQThCOztRQUNqRCxRQUFRLEtBQUssQ0FBQyxPQUFPLEVBQUU7WUFDckIsS0FBSyxzQkFBc0I7Z0JBQ3pCLE9BQU87Y0FDRCxXQUFLLENBQUMsTUFBTSwwQ0FBRSxrQkFBa0IsNEJBQTRCLENBQUM7WUFDckUsS0FBSyxRQUFRO2dCQUNYLE9BQU8sMkJBQTJCLEtBQUssQ0FBQyxPQUFPLEdBQUcsQ0FBQztZQUNyRCxLQUFLLE1BQU07Z0JBQ1QsT0FBTztjQUNELEtBQUssQ0FBQyxRQUFRLE1BQU0sS0FBSyxDQUFDLE9BQU8sRUFBRSxDQUFDO1lBQzVDO2dCQUNFLE9BQU8sb0JBQW9CLEtBQUssQ0FBQyxPQUFPLEdBQUcsQ0FBQztTQUMvQztJQUNILENBQUM7QUFDSCxDQUFDLEVBM0JTLE9BQU8sS0FBUCxPQUFPLFFBMkJoQjs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDcEpEOzs7K0VBRytFO0FBRXJCO0FBUXpCO0FBRVc7QUFFUTtBQUNJO0FBQ2hCO0FBR3hDOztHQUVHO0FBQ0gsTUFBTSxtQkFBbUIsR0FBRyxpQkFBaUIsQ0FBQztBQUU5Qzs7R0FFRztBQUNJLE1BQU0sWUFBYSxTQUFRLG1EQUFNO0lBQ3RDOzs7O09BSUc7SUFDSCxZQUFZLE9BQThCO1FBQ3hDLEtBQUssRUFBRSxDQUFDO1FBMEpGLGNBQVMsR0FBc0MsSUFBSSxDQUFDO1FBQ3BELGtCQUFhLEdBQUcsSUFBSSxxREFBTSxDQUFhLElBQUksQ0FBQyxDQUFDO1FBMUpuRCxJQUFJLENBQUMsUUFBUSxDQUFDLG1CQUFtQixDQUFDLENBQUM7UUFFbkMsTUFBTSxFQUNKLFFBQVEsRUFDUixhQUFhLEVBQ2IsUUFBUSxFQUNSLFVBQVUsRUFDVixVQUFVLEVBQ1gsR0FBRyxPQUFPLENBQUM7UUFDWixJQUFJLENBQUMsVUFBVSxHQUFHLFVBQVUsSUFBSSxtRUFBYyxDQUFDO1FBQy9DLElBQUksQ0FBQyxNQUFNLEdBQUcsSUFBSSxDQUFDLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7UUFFakQsOERBQThEO1FBQzlELCtEQUErRDtRQUMvRCx1RUFBdUU7UUFDdkUscUNBQXFDO1FBQ3JDLE1BQU0sTUFBTSxHQUFHLENBQUMsSUFBSSxDQUFDLE1BQU0sR0FBRyxJQUFJLDBEQUFhLEVBQUUsQ0FBQyxDQUFDO1FBQ25ELE1BQU0sRUFBRSxXQUFXLEVBQUUsR0FBRyxPQUFPLENBQUM7UUFFaEMsSUFBSSxDQUFDLEdBQUcsR0FBRyxJQUFJLENBQUMsVUFBVSxHQUFHLElBQUksaURBQVMsQ0FBQztZQUN6QyxRQUFRO1lBQ1IsYUFBYTtZQUNiLFdBQVc7WUFDWCxRQUFRO1lBQ1IsVUFBVTtZQUNWLFVBQVU7U0FDWCxDQUFDLENBQUM7UUFDSCxJQUFJLENBQUMsVUFBVSxDQUFDLFdBQVcsQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLGVBQWUsRUFBRSxJQUFJLENBQUMsQ0FBQztRQUVoRSxNQUFNLENBQUMsU0FBUyxDQUFDLElBQUksQ0FBQyxVQUFVLENBQUMsQ0FBQztJQUNwQyxDQUFDO0lBT0Q7O09BRUc7SUFDSCxJQUFJLE9BQU87UUFDVCxPQUFPLElBQUksQ0FBQyxVQUFVLENBQUMsT0FBTyxDQUFDO0lBQ2pDLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksUUFBUTtRQUNWLE9BQU8sSUFBSSxDQUFDLFNBQVMsQ0FBQztJQUN4QixDQUFDO0lBQ0QsSUFBSSxRQUFRLENBQUMsUUFBMkM7UUFDdEQsSUFBSSxJQUFJLENBQUMsU0FBUyxLQUFLLFFBQVEsRUFBRTtZQUMvQixPQUFPO1NBQ1I7UUFFRCxNQUFNLEdBQUcsR0FBRyxJQUFJLENBQUMsVUFBVSxDQUFDO1FBRTVCLElBQUksQ0FBQyxTQUFTLEdBQUcsR0FBRyxDQUFDLFFBQVEsR0FBRyxRQUFRLENBQUM7UUFDekMsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO0lBQ2hCLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksS0FBSztRQUNQLE1BQU0sTUFBTSxHQUFHLElBQUksQ0FBQyxTQUFTLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUM7UUFDdkQsTUFBTSxFQUFFLEtBQUssRUFBRSxHQUFHLElBQUksQ0FBQyxVQUFVLENBQUM7UUFFbEMsT0FBTyxFQUFFLE1BQU0sRUFBRSxLQUFLLEVBQUUsQ0FBQztJQUMzQixDQUFDO0lBQ0QsSUFBSSxLQUFLLENBQUMsS0FBa0M7UUFDMUMsSUFBSSxnRUFBaUIsQ0FBQyxJQUFJLENBQUMsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFO1lBQ3hDLE9BQU87U0FDUjtRQUVELElBQUksQ0FBQyxVQUFVLENBQUMsS0FBSyxHQUFHLEtBQUssQ0FBQyxLQUFLLENBQUM7UUFDcEMsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO0lBQ2hCLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksWUFBWTtRQUNkLE9BQU8sSUFBSSxDQUFDLGFBQWEsQ0FBQztJQUM1QixDQUFDO0lBRUQ7O09BRUc7SUFDSCxPQUFPO1FBQ0wsSUFBSSxJQUFJLENBQUMsUUFBUSxJQUFJLENBQUMsSUFBSSxDQUFDLFVBQVUsSUFBSSxDQUFDLElBQUksQ0FBQyxPQUFPLEVBQUU7WUFDdEQsT0FBTyxPQUFPLENBQUMsT0FBTyxDQUFDLFNBQVMsQ0FBQyxDQUFDO1NBQ25DO1FBRUQsT0FBTyxnRUFBVSxDQUFDO1lBQ2hCLEtBQUssRUFBRSxJQUFJLENBQUMsTUFBTSxDQUFDLEVBQUUsQ0FBQywyQkFBMkIsQ0FBQztZQUNsRCxJQUFJLEVBQUUsSUFBSSxDQUFDLE1BQU0sQ0FBQyxFQUFFLENBQUMsc0NBQXNDLENBQUM7WUFDNUQsT0FBTyxFQUFFO2dCQUNQLHFFQUFtQixDQUFDLEVBQUUsS0FBSyxFQUFFLElBQUksQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLFFBQVEsQ0FBQyxFQUFFLENBQUM7Z0JBQ3hELGlFQUFlLENBQUMsRUFBRSxLQUFLLEVBQUUsSUFBSSxDQUFDLE1BQU0sQ0FBQyxFQUFFLENBQUMsSUFBSSxDQUFDLEVBQUUsQ0FBQzthQUNqRDtTQUNGLENBQUMsQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLEVBQUU7WUFDZixJQUFJLENBQUMsTUFBTSxDQUFDLE1BQU0sQ0FBQyxNQUFNLEVBQUU7Z0JBQ3pCLE1BQU0sSUFBSSxLQUFLLENBQUMsZ0JBQWdCLENBQUMsQ0FBQzthQUNuQztRQUNILENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVEOztPQUVHO0lBQ0gsT0FBTztRQUNMLElBQUksSUFBSSxDQUFDLFVBQVUsRUFBRTtZQUNuQixPQUFPO1NBQ1I7UUFFRCxLQUFLLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDaEIsSUFBSSxDQUFDLFVBQVUsQ0FBQyxPQUFPLEVBQUUsQ0FBQztJQUM1QixDQUFDO0lBRUQ7O09BRUc7SUFDTyxhQUFhLENBQUMsR0FBWTtRQUNsQyxJQUFJLENBQUMsTUFBTSxFQUFFLENBQUM7SUFDaEIsQ0FBQztJQUVEOztPQUVHO0lBQ08sZUFBZSxDQUFDLEdBQVk7UUFDcEMsTUFBTSxHQUFHLEdBQUcsSUFBSSxDQUFDLFVBQVUsQ0FBQztRQUM1QixNQUFNLFFBQVEsR0FBRyxJQUFJLENBQUMsU0FBUyxDQUFDO1FBRWhDLElBQUksQ0FBQyxRQUFRLEVBQUU7WUFDYixJQUFJLENBQUMsSUFBSSxFQUFFLENBQUM7WUFDWixPQUFPO1NBQ1I7UUFFRCxJQUFJLENBQUMsSUFBSSxFQUFFLENBQUM7UUFDWixHQUFHLENBQUMsSUFBSSxFQUFFLENBQUM7SUFDYixDQUFDO0lBRUQ7O09BRUc7SUFDSyxlQUFlO1FBQ3BCLElBQUksQ0FBQyxZQUFrQyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsQ0FBQztJQUMzRCxDQUFDO0NBT0Y7QUFvREQ7O0dBRUc7QUFDSCxJQUFVLE9BQU8sQ0FjaEI7QUFkRCxXQUFVLE9BQU87SUFDZjs7T0FFRztJQUNILFNBQWdCLFdBQVcsQ0FBQyxNQUFXLEVBQUUsVUFBd0I7UUFDL0QsVUFBVSxHQUFHLFVBQVUsSUFBSSxtRUFBYyxDQUFDO1FBQzFDLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7UUFDNUMsT0FBTyxDQUFDLEtBQUssQ0FBQyx1Q0FBdUMsTUFBTSxDQUFDLE9BQU8sRUFBRSxDQUFDLENBQUM7UUFDdkUsS0FBSyxnRUFBVSxDQUFDO1lBQ2QsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsOEJBQThCLENBQUM7WUFDL0MsSUFBSSxFQUFFLE1BQU0sQ0FBQyxPQUFPO1lBQ3BCLE9BQU8sRUFBRSxDQUFDLGlFQUFlLENBQUMsRUFBRSxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxJQUFJLENBQUMsRUFBRSxDQUFDLENBQUM7U0FDdEQsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQVRlLG1CQUFXLGNBUzFCO0FBQ0gsQ0FBQyxFQWRTLE9BQU8sS0FBUCxPQUFPLFFBY2hCOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDdFFEOzs7K0VBRytFO0FBR1Q7QUFDSztBQUV2QjtBQUNYO0FBQ1Y7QUFDTztBQUV0Qzs7R0FFRztBQUNJLE1BQU0sVUFBVyxTQUFRLG1EQUFNO0lBQ3BDOztPQUVHO0lBQ0gsWUFBWSxPQUE0QjtRQUN0QyxLQUFLLEVBQUUsQ0FBQztRQW9JRixhQUFRLEdBQUcsSUFBSSxxREFBTSxDQUFhLElBQUksQ0FBQyxDQUFDO1FBRXhDLGVBQVUsR0FBdUIsQ0FBQyxDQUFDO1FBQ25DLGVBQVUsR0FBRyxFQUFFLENBQUM7UUF0SXRCLElBQUksQ0FBQyxRQUFRLEdBQUcsT0FBTyxDQUFDLFFBQVEsQ0FBQztRQUNqQyxJQUFJLENBQUMsVUFBVSxHQUFHLE9BQU8sQ0FBQyxVQUFVLElBQUksbUVBQWMsQ0FBQztRQUN2RCxJQUFJLENBQUMsUUFBUSxDQUFDLGVBQWUsQ0FBQyxDQUFDO1FBQy9CLElBQUksQ0FBQyxRQUFRLEdBQUcsT0FBTyxDQUFDLE9BQU8sQ0FBQztRQUNoQyxJQUFJLENBQUMsUUFBUSxDQUFDLGFBQWEsQ0FBQyxPQUFPLENBQUMsR0FBRyxFQUFFO1lBQ3ZDLElBQUksQ0FBQyxNQUFNLEVBQUUsQ0FBQztRQUNoQixDQUFDLEVBQUUsSUFBSSxDQUFDLENBQUM7SUFDWCxDQUFDO0lBT0Q7O09BRUc7SUFDSCxJQUFJLE9BQU87UUFDVCxPQUFPLElBQUksQ0FBQyxRQUFRLENBQUM7SUFDdkIsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxTQUFTOztRQUNYLGFBQU8sSUFBSSxDQUFDLElBQUksQ0FBQyxhQUFhLENBQUMsSUFBSSxDQUFDLDBDQUFFLFNBQVMsQ0FBQztJQUNsRCxDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLFNBQVM7UUFDWCxPQUFPLElBQUksQ0FBQyxVQUFVLENBQUM7SUFDekIsQ0FBQztJQUNELElBQUksU0FBUyxDQUFDLFNBQWlCO1FBQzdCLElBQUksSUFBSSxDQUFDLFVBQVUsS0FBSyxTQUFTLEVBQUU7WUFDakMsT0FBTztTQUNSO1FBQ0QsSUFBSSxDQUFDLFVBQVUsR0FBRyxTQUFTLENBQUM7UUFDNUIsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO0lBQ2hCLENBQUM7SUFFRDs7Ozs7Ozs7O09BU0c7SUFDSCxXQUFXLENBQUMsS0FBWTtRQUN0QixRQUFRLEtBQUssQ0FBQyxJQUFJLEVBQUU7WUFDbEIsS0FBSyxXQUFXO2dCQUNkLElBQUksQ0FBQyxhQUFhLENBQUMsS0FBbUIsQ0FBQyxDQUFDO2dCQUN4QyxNQUFNO1lBQ1I7Z0JBQ0UsTUFBTTtTQUNUO0lBQ0gsQ0FBQztJQUVEOztPQUVHO0lBQ08sYUFBYSxDQUFDLEdBQVk7UUFDbEMsSUFBSSxDQUFDLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyxXQUFXLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFDOUMsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO0lBQ2hCLENBQUM7SUFFRDs7T0FFRztJQUNPLGNBQWMsQ0FBQyxHQUFZO1FBQ25DLElBQUksQ0FBQyxJQUFJLENBQUMsbUJBQW1CLENBQUMsV0FBVyxFQUFFLElBQUksQ0FBQyxDQUFDO0lBQ25ELENBQUM7SUFFRDs7T0FFRztJQUNPLGVBQWUsQ0FBQyxHQUFZO1FBQ3BDLE1BQU0sRUFBRSxJQUFJLEVBQUUsUUFBUSxFQUFFLEdBQUcsSUFBSSxDQUFDO1FBQ2hDLE1BQU0sU0FBUyxHQUFHLElBQUksQ0FBQyxVQUFVLENBQUM7UUFDbEMsTUFBTSxXQUFXLEdBQUcsSUFBSSxDQUFDLFVBQVUsQ0FBQztRQUVwQyxPQUFPLENBQUMsWUFBWSxDQUFDLFFBQVEsRUFBRSxTQUFTLEVBQUUsSUFBSSxFQUFFLFdBQVcsQ0FBQyxDQUFDO1FBQzdELE1BQU0sRUFBRSxHQUFHLElBQUksQ0FBQyxhQUFhLENBQUMsSUFBSSxDQUFDLENBQUM7UUFDcEMsSUFBSSxFQUFFLElBQUksSUFBSSxDQUFDLFVBQVUsS0FBSyxTQUFTLEVBQUU7WUFDdkMsRUFBRSxDQUFDLFNBQVMsR0FBRyxJQUFJLENBQUMsVUFBVSxDQUFDO1NBQ2hDO0lBQ0gsQ0FBQztJQUVEOzs7O09BSUc7SUFDSyxhQUFhLENBQUMsS0FBaUI7UUFDckMsS0FBSyxDQUFDLGNBQWMsRUFBRSxDQUFDO1FBRXZCLElBQUksTUFBTSxHQUFHLEtBQUssQ0FBQyxNQUFxQixDQUFDO1FBQ3pDLElBQUksRUFBRSxHQUFHLE1BQU0sQ0FBQyxZQUFZLENBQUMsU0FBUyxDQUFDLENBQUM7UUFFeEMsSUFBSSxFQUFFLEtBQUssSUFBSSxDQUFDLFVBQVUsRUFBRTtZQUMxQixPQUFPO1NBQ1I7UUFFRCxJQUFJLENBQUMsRUFBRSxFQUFFO1lBQ1AsT0FBTyxDQUFDLEVBQUUsSUFBSSxNQUFNLEtBQUssSUFBSSxDQUFDLElBQUksRUFBRTtnQkFDbEMsTUFBTSxHQUFHLE1BQU0sQ0FBQyxhQUE0QixDQUFDO2dCQUM3QyxFQUFFLEdBQUcsTUFBTSxDQUFDLFlBQVksQ0FBQyxTQUFTLENBQUMsQ0FBQzthQUNyQztTQUNGO1FBRUQsSUFBSSxDQUFDLEVBQUUsRUFBRTtZQUNQLE9BQU87U0FDUjtRQUVELElBQUksQ0FBQyxRQUFRLEVBQUU7YUFDWixJQUFJLENBQUMsR0FBRyxFQUFFO1lBQ1QsSUFBSSxDQUFDLFVBQVUsR0FBRyxJQUFJLENBQUMsU0FBUyxDQUFDO1lBQ2pDLElBQUksQ0FBQyxVQUFVLEdBQUcsRUFBRyxDQUFDO1lBQ3RCLElBQUksQ0FBQyxRQUFRLENBQUMsSUFBSSxDQUFDLFNBQVMsQ0FBQyxDQUFDO1lBQzlCLElBQUksQ0FBQyxNQUFNLEVBQUUsQ0FBQztRQUNoQixDQUFDLENBQUM7YUFDRCxLQUFLLENBQUMsR0FBRyxFQUFFO1lBQ1YsV0FBVztRQUNiLENBQUMsQ0FBQyxDQUFDO0lBQ1AsQ0FBQztDQU9GO0FBZ0NEOztHQUVHO0FBQ0gsSUFBVSxPQUFPLENBNkhoQjtBQTdIRCxXQUFVLE9BQU87SUFDZjs7O09BR0c7SUFDSCxNQUFNLFFBQVEsR0FBRywwQkFBMEIsQ0FBQztJQUU1Qzs7O09BR0c7SUFDSCxNQUFNLGNBQWMsR0FBRyxnQ0FBZ0MsQ0FBQztJQUV4RDs7O09BR0c7SUFDSCxNQUFNLGNBQWMsR0FBRyxnQ0FBZ0MsQ0FBQztJQUV4RDs7Ozs7Ozs7O09BU0c7SUFDSCxTQUFTLE9BQU8sQ0FDZCxHQUFXLEVBQ1gsUUFBMEIsRUFDMUIsTUFBZ0M7UUFFaEMsd0VBQXdFO1FBQ3hFLElBQUksSUFBSSxHQUFHLE1BQU0sQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLEdBQUcsQ0FBQyxDQUFDO1FBRWpDLHlFQUF5RTtRQUN6RSxxQ0FBcUM7UUFDckMsSUFBSSxDQUFDLElBQUksRUFBRTtZQUNULElBQUksR0FBRyxNQUFNLENBQUMsSUFBSSxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsQ0FBQztTQUNuQztRQUVELGlFQUFpRTtRQUNqRSxJQUFJLENBQUMsSUFBSSxFQUFFO1lBQ1QsSUFBSSxHQUFHLE1BQU0sQ0FBQyxNQUFNLENBQUMsR0FBRyxDQUFDLENBQUM7U0FDM0I7UUFFRCxzREFBc0Q7UUFDdEQsSUFBSSxDQUFDLElBQUksRUFBRTtZQUNULE1BQU0sRUFBRSxVQUFVLEVBQUUsR0FBRyxRQUFRLENBQUMsTUFBTSxDQUFDO1lBRXZDLElBQUksR0FBRyxVQUFVLElBQUksVUFBVSxDQUFDLEdBQUcsQ0FBQyxJQUFJLFVBQVUsQ0FBQyxHQUFHLENBQUMsQ0FBQyxPQUFPLENBQUM7U0FDakU7UUFFRCxPQUFPLE9BQU8sSUFBSSxLQUFLLFFBQVEsQ0FBQyxDQUFDLENBQUMsSUFBSSxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUM7SUFDOUMsQ0FBQztJQUVEOztPQUVHO0lBQ0gsU0FBZ0IsWUFBWSxDQUMxQixRQUEwQixFQUMxQixTQUFpQixFQUNqQixJQUFpQixFQUNqQixVQUF3QjtRQUV4QixVQUFVLEdBQUcsVUFBVSxJQUFJLG1FQUFjLENBQUM7UUFDMUMsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztRQUM1QyxNQUFNLE9BQU8sR0FBRyxXQUFXLENBQUMsUUFBUSxDQUFDLENBQUMsTUFBTSxDQUFDLE1BQU0sQ0FBQyxFQUFFO1lBQ3BELE1BQU0sRUFBRSxNQUFNLEVBQUUsR0FBRyxNQUFNLENBQUM7WUFDMUIsTUFBTSxVQUFVLEdBQUcsTUFBTSxDQUFDLGdDQUFnQyxDQUFDLEtBQUssSUFBSSxDQUFDO1lBQ3JFLE1BQU0sUUFBUSxHQUFHLE1BQU0sQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLFVBQVUsSUFBSSxFQUFFLENBQUMsQ0FBQyxNQUFNLEdBQUcsQ0FBQyxDQUFDO1lBQ2pFLE1BQU0sVUFBVSxHQUFHLE1BQU0sQ0FBQyxvQkFBb0IsS0FBSyxLQUFLLENBQUM7WUFFekQsT0FBTyxDQUFDLFVBQVUsSUFBSSxDQUFDLFFBQVEsSUFBSSxVQUFVLENBQUMsQ0FBQztRQUNqRCxDQUFDLENBQUMsQ0FBQztRQUNILE1BQU0sS0FBSyxHQUFHLE9BQU8sQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLEVBQUU7WUFDakMsTUFBTSxFQUFFLEVBQUUsRUFBRSxNQUFNLEVBQUUsT0FBTyxFQUFFLEdBQUcsTUFBTSxDQUFDO1lBQ3ZDLE1BQU0sS0FBSyxHQUNULE9BQU8sTUFBTSxDQUFDLEtBQUssS0FBSyxRQUFRO2dCQUM5QixDQUFDLENBQUMsS0FBSyxDQUFDLEVBQUUsQ0FBQyxRQUFRLEVBQUUsTUFBTSxDQUFDLEtBQUssQ0FBQztnQkFDbEMsQ0FBQyxDQUFDLEVBQUUsQ0FBQztZQUNULE1BQU0sV0FBVyxHQUNmLE9BQU8sTUFBTSxDQUFDLFdBQVcsS0FBSyxRQUFRO2dCQUNwQyxDQUFDLENBQUMsS0FBSyxDQUFDLEVBQUUsQ0FBQyxRQUFRLEVBQUUsTUFBTSxDQUFDLFdBQVcsQ0FBQztnQkFDeEMsQ0FBQyxDQUFDLEVBQUUsQ0FBQztZQUNULE1BQU0sU0FBUyxHQUFHLEdBQUcsV0FBVyxLQUFLLEVBQUUsS0FBSyxPQUFPLEVBQUUsQ0FBQztZQUN0RCxNQUFNLElBQUksR0FBRyxPQUFPLENBQUMsUUFBUSxFQUFFLFFBQVEsRUFBRSxNQUFNLENBQUMsQ0FBQztZQUNqRCxNQUFNLFNBQVMsR0FBRyxPQUFPLENBQUMsY0FBYyxFQUFFLFFBQVEsRUFBRSxNQUFNLENBQUMsQ0FBQztZQUM1RCxNQUFNLFNBQVMsR0FBRyxPQUFPLENBQUMsY0FBYyxFQUFFLFFBQVEsRUFBRSxNQUFNLENBQUMsQ0FBQztZQUU1RCxPQUFPLENBQ0wseURBQ0UsU0FBUyxFQUFFLEVBQUUsS0FBSyxTQUFTLENBQUMsQ0FBQyxDQUFDLGlCQUFpQixDQUFDLENBQUMsQ0FBQyxFQUFFLGFBQzNDLEVBQUUsRUFDWCxHQUFHLEVBQUUsRUFBRSxFQUNQLEtBQUssRUFBRSxTQUFTO2dCQUVoQixpREFBQywyRUFBb0IsSUFDbkIsSUFBSSxFQUFFLElBQUksSUFBSSxDQUFDLFNBQVMsQ0FBQyxDQUFDLENBQUMsU0FBUyxDQUFDLENBQUMsQ0FBQyxtRUFBWSxDQUFDLEVBQ3BELFNBQVMsRUFBRSxrRUFBTyxDQUFDLFNBQVMsRUFBRSxTQUFTLENBQUMsRUFDeEMsS0FBSyxFQUFFLFNBQVMsRUFDaEIsR0FBRyxFQUFDLE1BQU0sRUFDVixVQUFVLEVBQUMsZ0JBQWdCLEdBQzNCO2dCQUNGLCtEQUFPLEtBQUssQ0FBUSxDQUNqQixDQUNOLENBQUM7UUFDSixDQUFDLENBQUMsQ0FBQztRQUVILDZEQUErQixDQUFDLElBQUksQ0FBQyxDQUFDO1FBQ3RDLDZDQUFlLENBQUMsNkRBQUssS0FBSyxDQUFNLEVBQUUsSUFBSSxDQUFDLENBQUM7SUFDMUMsQ0FBQztJQXBEZSxvQkFBWSxlQW9EM0I7SUFFRDs7T0FFRztJQUNILFNBQVMsV0FBVyxDQUFDLFFBQTBCO1FBQzdDLE9BQU8sTUFBTSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsT0FBTyxDQUFDO2FBQ2pDLEdBQUcsQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFFLENBQUM7YUFDeEMsSUFBSSxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsRUFBRSxFQUFFO1lBQ2IsT0FBTyxDQUFDLENBQUMsQ0FBQyxNQUFNLENBQUMsS0FBSyxJQUFJLENBQUMsQ0FBQyxFQUFFLENBQUMsQ0FBQyxhQUFhLENBQUMsQ0FBQyxDQUFDLE1BQU0sQ0FBQyxLQUFLLElBQUksQ0FBQyxDQUFDLEVBQUUsQ0FBQyxDQUFDO1FBQ3hFLENBQUMsQ0FBQyxDQUFDO0lBQ1AsQ0FBQztBQUNILENBQUMsRUE3SFMsT0FBTyxLQUFQLE9BQU8sUUE2SGhCOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDOVRELDBDQUEwQztBQUMxQywyREFBMkQ7QUFFVTtBQUNFO0FBR0Q7QUFHbEI7QUFDQTtBQUNOO0FBQ0o7QUFFMUM7O0dBRUc7QUFDSCxNQUFNLGdCQUFnQixHQUFHLHNCQUFzQixDQUFDO0FBRWhEOztHQUVHO0FBQ0gsTUFBTSxVQUFVLEdBQUcsMkJBQTJCLENBQUM7QUFFL0M7O0dBRUc7QUFDSCxNQUFNLFdBQVcsR0FBRyxjQUFjLENBQUM7QUFFbkM7O0dBRUc7QUFDSSxNQUFNLFNBQVUsU0FBUSxtREFBVTtJQUN2Qzs7T0FFRztJQUNILFlBQVksT0FBMkI7UUFDckMsS0FBSyxDQUFDO1lBQ0osV0FBVyxFQUFFLFlBQVk7WUFDekIsUUFBUSxFQUFFLG1FQUEwQjtZQUNwQyxPQUFPLEVBQUUsQ0FBQztTQUNYLENBQUMsQ0FBQztRQXFQRyxlQUFVLEdBQUcsS0FBSyxDQUFDO1FBQ25CLGFBQVEsR0FBRyxLQUFLLENBQUM7UUFFakIscUJBQWdCLEdBQUcsSUFBSSxxREFBTSxDQUFpQixJQUFJLENBQUMsQ0FBQztRQUlwRCxjQUFTLEdBQXNDLElBQUksQ0FBQztRQUNwRCxhQUFRLEdBQUcsSUFBSSx5REFBTyxFQUFVLENBQUM7UUEzUHZDLE1BQU0sRUFBRSxRQUFRLEVBQUUsYUFBYSxFQUFFLFFBQVEsRUFBRSxVQUFVLEVBQUUsR0FBRyxPQUFPLENBQUM7UUFDbEUsSUFBSSxDQUFDLFFBQVEsR0FBRyxRQUFRLENBQUM7UUFDekIsSUFBSSxDQUFDLFVBQVUsR0FBRyxVQUFVLElBQUksbUVBQWMsQ0FBQztRQUMvQyxJQUFJLENBQUMsU0FBUyxHQUFHLFFBQVEsQ0FBQztRQUUxQixvQ0FBb0M7UUFDcEMsTUFBTSxRQUFRLEdBQUcsQ0FBQyxJQUFJLENBQUMsU0FBUyxHQUFHLElBQUkscUVBQWlCLENBQUM7WUFDdkQsS0FBSyxFQUFFLElBQUksb0VBQWdCLEVBQUU7WUFDN0IsT0FBTyxFQUFFLGFBQWE7U0FDdkIsQ0FBQyxDQUFDLENBQUM7UUFFSixRQUFRLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUMsSUFBSSxHQUFHLEVBQUUsQ0FBQztRQUN0QyxRQUFRLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxRQUFRLEdBQUcsaUJBQWlCLENBQUM7UUFDbkQsUUFBUSxDQUFDLE1BQU0sQ0FBQyxTQUFTLENBQUMsVUFBVSxFQUFFLElBQUksQ0FBQyxDQUFDO1FBRTVDLDBDQUEwQztRQUMxQyxNQUFNLElBQUksR0FBRyxDQUFDLElBQUksQ0FBQyxLQUFLLEdBQUcsSUFBSSxxRUFBaUIsQ0FBQztZQUMvQyxLQUFLLEVBQUUsSUFBSSxvRUFBZ0IsRUFBRTtZQUM3QixPQUFPLEVBQUUsYUFBYTtZQUN0QixNQUFNLEVBQUUsRUFBRSxXQUFXLEVBQUUsSUFBSSxFQUFFO1NBQzlCLENBQUMsQ0FBQyxDQUFDO1FBRUosSUFBSSxDQUFDLFFBQVEsQ0FBQyxVQUFVLENBQUMsQ0FBQztRQUMxQixJQUFJLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxRQUFRLEdBQUcsaUJBQWlCLENBQUM7UUFDL0MsSUFBSSxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLGNBQWMsRUFBRSxJQUFJLENBQUMsQ0FBQztRQUVuRSxrQ0FBa0M7UUFDbEMsSUFBSSxDQUFDLFVBQVUsR0FBRywyREFBZSxDQUMvQixJQUFJLEVBQ0osT0FBTyxDQUFDLFVBQVUsRUFDbEIsSUFBSSxDQUFDLFVBQVUsQ0FDaEIsQ0FBQztRQUVGLElBQUksQ0FBQyxRQUFRLENBQUMsZ0JBQWdCLENBQUMsQ0FBQztRQUNoQyw2REFBNkQ7UUFDN0QsSUFBSSxDQUFDLFlBQVksR0FBRyxPQUFPLENBQUMsV0FBVyxDQUFDO1FBQ3hDLElBQUksQ0FBQyxTQUFTLENBQUMsT0FBTyxDQUFDLGNBQWMsQ0FBQyxRQUFRLEVBQUUsSUFBSSxDQUFDLFVBQVUsQ0FBQyxDQUFDLENBQUM7UUFDbEUsSUFBSSxDQUFDLFNBQVMsQ0FDWixPQUFPLENBQUMsVUFBVSxDQUFDLElBQUksRUFBRSxJQUFJLENBQUMsUUFBUSxFQUFFLElBQUksQ0FBQyxVQUFVLEVBQUUsSUFBSSxDQUFDLFVBQVUsQ0FBQyxDQUMxRSxDQUFDO0lBQ0osQ0FBQztJQU9EOztPQUVHO0lBQ0gsSUFBSSxTQUFTO1FBQ1gsT0FBTyxJQUFJLENBQUMsVUFBVSxDQUFDO0lBQ3pCLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksT0FBTztRQUNULE9BQU8sSUFBSSxDQUFDLFFBQVEsQ0FBQztJQUN2QixDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLGVBQWU7UUFDakIsT0FBTyxJQUFJLENBQUMsZ0JBQWdCLENBQUM7SUFDL0IsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxPQUFPOztRQUNULGFBQU8sSUFBSSxDQUFDLEtBQUssQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQyxJQUFJLFlBQUssSUFBSSxDQUFDLFNBQVMsMENBQUUsR0FBRyxvQ0FBSSxFQUFFLENBQUM7SUFDMUUsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxRQUFRO1FBQ1YsT0FBTyxJQUFJLENBQUMsU0FBUyxDQUFDO0lBQ3hCLENBQUM7SUFDRCxJQUFJLFFBQVEsQ0FBQyxRQUEyQztRQUN0RCxJQUFJLENBQUMsUUFBUSxJQUFJLENBQUMsSUFBSSxDQUFDLFNBQVMsRUFBRTtZQUNoQyxPQUFPO1NBQ1I7UUFFRCxNQUFNLFVBQVUsR0FDZCxRQUFRLElBQUksSUFBSSxDQUFDLFNBQVMsSUFBSSxRQUFRLENBQUMsTUFBTSxLQUFLLElBQUksQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDO1FBRTFFLElBQUksVUFBVSxFQUFFO1lBQ2QsT0FBTztTQUNSO1FBRUQsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLFNBQVMsQ0FBQztRQUNoQyxNQUFNLElBQUksR0FBRyxJQUFJLENBQUMsS0FBSyxDQUFDO1FBRXhCLDBDQUEwQztRQUMxQyxJQUFJLElBQUksQ0FBQyxTQUFTLEVBQUU7WUFDbEIsSUFBSSxDQUFDLFNBQVMsQ0FBQyxPQUFPLENBQUMsVUFBVSxDQUFDLElBQUksQ0FBQyxrQkFBa0IsRUFBRSxJQUFJLENBQUMsQ0FBQztTQUNsRTtRQUVELElBQUksUUFBUSxFQUFFO1lBQ1osSUFBSSxDQUFDLFNBQVMsR0FBRyxRQUFRLENBQUM7WUFDMUIsSUFBSSxDQUFDLFNBQVMsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxrQkFBa0IsRUFBRSxJQUFJLENBQUMsQ0FBQztZQUM5RCxJQUFJLENBQUMsa0JBQWtCLEVBQUUsQ0FBQztTQUMzQjthQUFNO1lBQ0wsSUFBSSxDQUFDLFNBQVMsR0FBRyxJQUFJLENBQUM7WUFDdEIsUUFBUSxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsS0FBSyxDQUFDLElBQUksR0FBRyxFQUFFLENBQUM7WUFDdEMsSUFBSSxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsS0FBSyxDQUFDLElBQUksR0FBRyxFQUFFLENBQUM7U0FDbkM7UUFFRCxJQUFJLENBQUMsTUFBTSxFQUFFLENBQUM7SUFDaEIsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxLQUFLO1FBQ1AsT0FBTyxJQUFJLENBQUMsYUFBYSxFQUFFLENBQUM7SUFDOUIsQ0FBQztJQUNELElBQUksS0FBSyxDQUFDLEtBQWU7UUFDdkIsSUFBSSxDQUFDLGdCQUFnQixDQUFDLEtBQUssQ0FBQyxDQUFDO0lBQy9CLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksTUFBTTtRQUNSLE9BQU8sSUFBSSxDQUFDLEtBQUssQ0FBQyxNQUFNLENBQUM7SUFDM0IsQ0FBQztJQUVEOztPQUVHO0lBQ0gsT0FBTztRQUNMLElBQUksSUFBSSxDQUFDLFVBQVUsRUFBRTtZQUNuQixPQUFPO1NBQ1I7UUFFRCxLQUFLLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDaEIsSUFBSSxDQUFDLFNBQVMsQ0FBQyxPQUFPLEVBQUUsQ0FBQztRQUN6QixJQUFJLENBQUMsS0FBSyxDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQ3ZCLENBQUM7SUFFRDs7T0FFRztJQUNILE1BQU07O1FBQ0osSUFBSSxDQUFDLEtBQUssQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQyxJQUFJLGVBQUcsSUFBSSxDQUFDLFFBQVEsMENBQUUsR0FBRyxtQ0FBSSxFQUFFLENBQUM7UUFDOUQsSUFBSSxDQUFDLGNBQWMsQ0FBQyxLQUFLLEVBQUUsS0FBSyxDQUFDLENBQUM7SUFDcEMsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSTtRQUNGLElBQUksQ0FBQyxJQUFJLENBQUMsT0FBTyxJQUFJLENBQUMsSUFBSSxDQUFDLFNBQVMsRUFBRTtZQUNwQyxPQUFPLE9BQU8sQ0FBQyxPQUFPLENBQUMsU0FBUyxDQUFDLENBQUM7U0FDbkM7UUFFRCxNQUFNLFFBQVEsR0FBRyxJQUFJLENBQUMsU0FBUyxDQUFDO1FBQ2hDLE1BQU0sTUFBTSxHQUFHLElBQUksQ0FBQyxLQUFLLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDO1FBRWxELE9BQU8sUUFBUTthQUNaLElBQUksQ0FBQyxNQUFNLENBQUM7YUFDWixJQUFJLENBQUMsR0FBRyxFQUFFO1lBQ1QsSUFBSSxDQUFDLGNBQWMsQ0FBQyxLQUFLLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFDcEMsQ0FBQyxDQUFDO2FBQ0QsS0FBSyxDQUFDLE1BQU0sQ0FBQyxFQUFFO1lBQ2QsSUFBSSxDQUFDLGNBQWMsQ0FBQyxJQUFJLEVBQUUsS0FBSyxDQUFDLENBQUM7WUFDakMsSUFBSSxDQUFDLFlBQVksQ0FBQyxNQUFNLEVBQUUsSUFBSSxDQUFDLFVBQVUsQ0FBQyxDQUFDO1FBQzdDLENBQUMsQ0FBQyxDQUFDO0lBQ1AsQ0FBQztJQUVEOztPQUVHO0lBQ08sYUFBYSxDQUFDLEdBQVk7UUFDbEMsT0FBTyxDQUFDLGVBQWUsQ0FBQyxJQUFJLENBQUMsU0FBUyxFQUFFLElBQUksQ0FBQyxRQUFRLENBQUMsQ0FBQztRQUN2RCxJQUFJLENBQUMsTUFBTSxFQUFFLENBQUM7SUFDaEIsQ0FBQztJQUVEOztPQUVHO0lBQ08sZUFBZSxDQUFDLEdBQVk7UUFDcEMsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLFNBQVMsQ0FBQztRQUNoQyxNQUFNLFFBQVEsR0FBRyxJQUFJLENBQUMsU0FBUyxDQUFDO1FBQ2hDLE1BQU0sSUFBSSxHQUFHLElBQUksQ0FBQyxLQUFLLENBQUM7UUFFeEIsSUFBSSxRQUFRLEVBQUU7WUFDWixRQUFRLENBQUMsTUFBTSxDQUFDLE9BQU8sRUFBRSxDQUFDO1lBQzFCLElBQUksQ0FBQyxNQUFNLENBQUMsT0FBTyxFQUFFLENBQUM7U0FDdkI7SUFDSCxDQUFDO0lBRUQ7O09BRUc7SUFDSyxjQUFjO1FBQ3BCLE1BQU0sR0FBRyxHQUFHLElBQUksQ0FBQyxLQUFLLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDO1FBQy9DLE1BQU0sUUFBUSxHQUFHLElBQUksQ0FBQyxTQUFTLENBQUM7UUFFaEMsSUFBSSxDQUFDLFdBQVcsQ0FBQyxXQUFXLENBQUMsQ0FBQztRQUU5QixpRUFBaUU7UUFDakUsSUFBSSxDQUFDLFFBQVEsSUFBSSxRQUFRLENBQUMsR0FBRyxLQUFLLEdBQUcsRUFBRTtZQUNyQyxJQUFJLENBQUMsY0FBYyxDQUFDLEtBQUssRUFBRSxLQUFLLENBQUMsQ0FBQztZQUNsQyxPQUFPO1NBQ1I7UUFFRCxNQUFNLE1BQU0sR0FBRyxRQUFRLENBQUMsUUFBUSxDQUFDLEdBQUcsQ0FBQyxDQUFDO1FBRXRDLElBQUksTUFBTSxFQUFFO1lBQ1YsSUFBSSxDQUFDLFFBQVEsQ0FBQyxXQUFXLENBQUMsQ0FBQztZQUMzQixJQUFJLENBQUMsY0FBYyxDQUFDLElBQUksRUFBRSxLQUFLLENBQUMsQ0FBQztZQUNqQyxPQUFPO1NBQ1I7UUFFRCxJQUFJLENBQUMsY0FBYyxDQUFDLElBQUksRUFBRSxJQUFJLENBQUMsQ0FBQztJQUNsQyxDQUFDO0lBRUQ7O09BRUc7SUFDSyxrQkFBa0I7O1FBQ3hCLE1BQU0sUUFBUSxHQUFHLElBQUksQ0FBQyxTQUFTLENBQUM7UUFDaEMsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLFNBQVMsQ0FBQztRQUNoQyxNQUFNLElBQUksR0FBRyxJQUFJLENBQUMsS0FBSyxDQUFDO1FBRXhCLFFBQVEsQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQyxJQUFJLFNBQUcsUUFBUSxhQUFSLFFBQVEsdUJBQVIsUUFBUSxDQUFFLGlCQUFpQixxQ0FBTSxFQUFFLENBQUM7UUFDdkUsSUFBSSxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsS0FBSyxDQUFDLElBQUksU0FBRyxRQUFRLGFBQVIsUUFBUSx1QkFBUixRQUFRLENBQUUsR0FBRyxtQ0FBSSxFQUFFLENBQUM7SUFDckQsQ0FBQztJQUVPLGNBQWMsQ0FBQyxNQUFNLEdBQUcsSUFBSSxDQUFDLFVBQVUsRUFBRSxJQUFJLEdBQUcsSUFBSSxDQUFDLFFBQVE7UUFDbkUsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLFNBQVMsQ0FBQztRQUVoQyxJQUFJLENBQUMsVUFBVSxHQUFHLE1BQU0sQ0FBQztRQUN6QixJQUFJLENBQUMsUUFBUSxHQUFHLElBQUksQ0FBQztRQUNyQixJQUFJLENBQUMsZ0JBQWdCLENBQUMsSUFBSSxDQUFDLENBQUMsUUFBUSxDQUFDLE1BQU0sRUFBRSxRQUFRLENBQUMsSUFBSSxDQUFDLENBQUMsQ0FBQztJQUMvRCxDQUFDO0NBYUY7QUE4REQ7O0dBRUc7QUFDSCxJQUFVLE9BQU8sQ0FvRWhCO0FBcEVELFdBQVUsT0FBTztJQUNmOztPQUVHO0lBQ0gsU0FBZ0IsY0FBYyxDQUM1QixNQUFjLEVBQ2QsVUFBd0I7UUFFeEIsVUFBVSxHQUFHLFVBQVUsSUFBSSxtRUFBYyxDQUFDO1FBQzFDLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7UUFDNUMsTUFBTSxNQUFNLEdBQUcsSUFBSSxtREFBTSxFQUFFLENBQUM7UUFDNUIsTUFBTSxNQUFNLEdBQUcsQ0FBQyxNQUFNLENBQUMsTUFBTSxHQUFHLElBQUksc0RBQVMsQ0FBQyxFQUFFLE9BQU8sRUFBRSxDQUFDLEVBQUUsQ0FBQyxDQUFDLENBQUM7UUFDL0QsTUFBTSxNQUFNLEdBQUcsSUFBSSxtREFBTSxFQUFFLENBQUM7UUFDNUIsTUFBTSxHQUFHLEdBQUcsSUFBSSx5REFBTyxFQUFFLENBQUM7UUFDMUIsTUFBTSxZQUFZLEdBQUcsS0FBSyxDQUFDLEVBQUUsQ0FBQyxpQkFBaUIsQ0FBQyxDQUFDO1FBRWpELE1BQU0sQ0FBQyxJQUFJLENBQUMsU0FBUyxHQUFHLFlBQVksQ0FBQztRQUNyQyxHQUFHLENBQUMsVUFBVSxDQUFDLENBQUMsRUFBRSxRQUFRLEVBQUUsTUFBTSxDQUFDLENBQUM7UUFDcEMsTUFBTSxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsQ0FBQztRQUN0QixNQUFNLENBQUMsU0FBUyxDQUFDLE1BQU0sQ0FBQyxDQUFDO1FBRXpCLE9BQU8sTUFBTSxDQUFDO0lBQ2hCLENBQUM7SUFsQmUsc0JBQWMsaUJBa0I3QjtJQUVEOztPQUVHO0lBQ0gsU0FBZ0IsZUFBZSxDQUM3QixRQUFrQyxFQUNsQyxPQUF3QjtRQUV4QixNQUFNLEVBQUUsUUFBUSxFQUFFLE1BQU0sRUFBRSxJQUFJLEVBQUUsR0FBRyxRQUFRLENBQUM7UUFFNUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxRQUFRLEVBQUUsMEVBQXdCLEVBQUUsQ0FBQyxDQUFDO1FBRXRELHlFQUF5RTtRQUN6RSx1RUFBdUU7UUFDdkUsNEJBQTRCO1FBQzVCLENBQUMsTUFBTSxFQUFFLElBQUksQ0FBQyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsRUFBRTtZQUM1QixNQUFNLElBQUksR0FBRyxJQUFJLHNFQUFvQixDQUFDLEVBQUUsUUFBUSxFQUFFLFFBQVEsRUFBRSxFQUFFLEVBQUUsSUFBSSxFQUFFLENBQUMsQ0FBQztZQUN4RSxPQUFPLENBQUMsT0FBTyxDQUFDLElBQUksRUFBRSxJQUFJLENBQUMsQ0FBQztRQUM5QixDQUFDLENBQUMsQ0FBQztJQUNMLENBQUM7SUFmZSx1QkFBZSxrQkFlOUI7SUFFRDs7T0FFRztJQUNILFNBQWdCLFVBQVUsQ0FDeEIsTUFBYyxFQUNkLE9BQXdCLEVBQ3hCLFNBQWlCLEVBQ2pCLFVBQXdCO1FBRXhCLFVBQVUsR0FBRyxVQUFVLElBQUksbUVBQWMsQ0FBQztRQUMxQyxNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQzVDLE1BQU0sU0FBUyxHQUFHLEtBQUssQ0FBQyxFQUFFLENBQUMsa0JBQWtCLENBQUMsQ0FBQztRQUMvQyxNQUFNLE1BQU0sR0FBRyxJQUFJLG1EQUFNLEVBQUUsQ0FBQztRQUM1QixNQUFNLE1BQU0sR0FBRyxDQUFDLE1BQU0sQ0FBQyxNQUFNLEdBQUcsSUFBSSxzREFBUyxDQUFDLEVBQUUsT0FBTyxFQUFFLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQztRQUMvRCxNQUFNLE1BQU0sR0FBRyxJQUFJLG1EQUFNLEVBQUUsQ0FBQztRQUU1QixNQUFNLENBQUMsSUFBSSxDQUFDLFNBQVMsR0FBRyxTQUFTLENBQUM7UUFDbEMsT0FBTyxDQUFDLFVBQVUsQ0FBQyxDQUFDLEVBQUUsUUFBUSxFQUFFLE1BQU0sQ0FBQyxDQUFDO1FBQ3hDLE1BQU0sQ0FBQyxTQUFTLENBQUMsT0FBTyxDQUFDLENBQUM7UUFDMUIsTUFBTSxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsQ0FBQztRQUN6QixNQUFNLENBQUMsU0FBUyxDQUFDLFNBQVMsQ0FBQyxDQUFDO1FBRTVCLE9BQU8sTUFBTSxDQUFDO0lBQ2hCLENBQUM7SUFwQmUsa0JBQVUsYUFvQnpCO0FBQ0gsQ0FBQyxFQXBFUyxPQUFPLEtBQVAsT0FBTyxRQW9FaEI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUM5YUQ7OzsrRUFHK0U7QUFNVDtBQUNkO0FBRVc7QUFHYjtBQUN2QjtBQUNPO0FBQ1E7QUFDSjtBQUNBO0FBRTFDOztHQUVHO0FBQ0gsTUFBTSxjQUFjLEdBQStCO0lBQ2pELEtBQUssRUFBRSxDQUFDLENBQUMsRUFBRSxDQUFDLENBQUM7SUFDYixTQUFTLEVBQUU7UUFDVCxNQUFNLEVBQUUsS0FBSztRQUNiLE1BQU0sRUFBRSxFQUFFO1FBQ1YsS0FBSyxFQUFFLENBQUMsQ0FBQyxFQUFFLENBQUMsQ0FBQztLQUNkO0NBQ0YsQ0FBQztBQUVGOztHQUVHO0FBQ0ksTUFBTSxhQUFjLFNBQVEsbURBQU07SUFDdkM7O09BRUc7SUFDSCxZQUFZLE9BQStCO1FBQ3pDLEtBQUssRUFBRSxDQUFDO1FBd1JGLGNBQVMsR0FBeUIsSUFBSSxDQUFDO1FBSXZDLFlBQU8sR0FBRyxLQUFLLENBQUM7UUFDaEIsV0FBTSxHQUErQiwrREFBZ0IsQ0FBQyxjQUFjLENBQUMsQ0FBQztRQTVSNUUsSUFBSSxDQUFDLFVBQVUsR0FBRyxPQUFPLENBQUMsVUFBVSxJQUFJLG1FQUFjLENBQUM7UUFDdkQsSUFBSSxDQUFDLFFBQVEsQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO1FBQ2xDLElBQUksQ0FBQyxHQUFHLEdBQUcsT0FBTyxDQUFDLEdBQUcsQ0FBQztRQUN2QixJQUFJLENBQUMsS0FBSyxHQUFHLE9BQU8sQ0FBQyxLQUFLLENBQUM7UUFFM0IsTUFBTSxFQUFFLFFBQVEsRUFBRSxhQUFhLEVBQUUsVUFBVSxFQUFFLEdBQUcsT0FBTyxDQUFDO1FBQ3hELE1BQU0sTUFBTSxHQUFHLENBQUMsSUFBSSxDQUFDLE1BQU0sR0FBRyxJQUFJLHdEQUFXLEVBQUUsQ0FBQyxDQUFDO1FBQ2pELE1BQU0sUUFBUSxHQUFHLENBQUMsSUFBSSxDQUFDLFFBQVEsR0FBRyxPQUFPLENBQUMsUUFBUSxDQUFDLENBQUM7UUFDcEQsTUFBTSxLQUFLLEdBQUcsQ0FBQyxJQUFJLENBQUMsTUFBTSxHQUFHLElBQUksbURBQVUsQ0FBQztZQUMxQyxXQUFXLEVBQUUsWUFBWTtZQUN6QixRQUFRLEVBQUUsbUVBQTBCO1lBQ3BDLE9BQU8sRUFBRSxDQUFDO1NBQ1gsQ0FBQyxDQUFDLENBQUM7UUFDSixNQUFNLFlBQVksR0FBRyxDQUFDLElBQUksQ0FBQyxhQUFhLEdBQUcsSUFBSSxtREFBTSxFQUFFLENBQUMsQ0FBQztRQUN6RCxNQUFNLE1BQU0sR0FBRyxDQUFDLElBQUksQ0FBQyxPQUFPLEdBQUcsSUFBSSx1REFBWSxDQUFDO1lBQzlDLFFBQVE7WUFDUixhQUFhO1lBQ2IsUUFBUTtZQUNSLFVBQVU7WUFDVixVQUFVLEVBQUUsSUFBSSxDQUFDLFVBQVU7U0FDNUIsQ0FBQyxDQUFDLENBQUM7UUFDSixNQUFNLE9BQU8sR0FBRyxHQUFHLEVBQUUsQ0FBQyxNQUFNLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDdkMsTUFBTSxJQUFJLEdBQUcsQ0FBQyxJQUFJLENBQUMsS0FBSyxHQUFHLElBQUksbURBQVUsQ0FBQztZQUN4QyxPQUFPO1lBQ1AsUUFBUTtZQUNSLFVBQVUsRUFBRSxJQUFJLENBQUMsVUFBVTtTQUM1QixDQUFDLENBQUMsQ0FBQztRQUNKLE1BQU0sSUFBSSxHQUFHLE9BQU8sQ0FBQyxJQUFJLENBQUM7UUFFMUIsWUFBWSxDQUFDLFFBQVEsQ0FBQyw4QkFBOEIsQ0FBQyxDQUFDO1FBQ3RELE9BQU8sQ0FBQyx3QkFBd0IsQ0FBQyxZQUFZLENBQUMsSUFBSSxFQUFFLElBQUksQ0FBQyxVQUFVLENBQUMsQ0FBQztRQUVyRSxJQUFJLElBQUksRUFBRTtZQUNSLElBQUksQ0FBQyxLQUFLLEdBQUcsS0FBSyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLENBQUMsSUFBSSxDQUFDO1NBQzdEO1FBRUQsS0FBSyxDQUFDLFFBQVEsQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDO1FBQ3hDLE1BQU0sQ0FBQyxTQUFTLENBQUMsS0FBSyxDQUFDLENBQUM7UUFDeEIsS0FBSyxDQUFDLFNBQVMsQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUN0QixLQUFLLENBQUMsU0FBUyxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBRTlCLDhEQUFxQixDQUFDLElBQUksRUFBRSxDQUFDLENBQUMsQ0FBQztRQUMvQiw4REFBcUIsQ0FBQyxZQUFZLEVBQUUsQ0FBQyxDQUFDLENBQUM7UUFDdkMsOERBQXFCLENBQUMsTUFBTSxFQUFFLENBQUMsQ0FBQyxDQUFDO1FBRWpDLE1BQU0sQ0FBQyxZQUFZLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxlQUFlLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFDeEQsSUFBSSxDQUFDLE9BQU8sQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLGVBQWUsRUFBRSxJQUFJLENBQUMsQ0FBQztRQUNqRCxLQUFLLENBQUMsV0FBVyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsZUFBZSxFQUFFLElBQUksQ0FBQyxDQUFDO0lBQ3hELENBQUM7SUFpQkQ7O09BRUc7SUFDSCxJQUFJLFlBQVk7UUFDZCxPQUFPLElBQUksQ0FBQyxPQUFPLENBQUMsR0FBRyxDQUFDLFNBQVMsQ0FBQztJQUNwQyxDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLFVBQVU7UUFDWixPQUFPLElBQUksQ0FBQyxPQUFPLENBQUMsR0FBRyxDQUFDLE9BQU8sQ0FBQztJQUNsQyxDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLGVBQWU7UUFDakIsT0FBTyxJQUFJLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxlQUFlLENBQUM7SUFDMUMsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxRQUFRO1FBQ1YsT0FBTyxJQUFJLENBQUMsT0FBTyxDQUFDLFFBQVEsQ0FBQztJQUMvQixDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLE1BQU07UUFDUixPQUFPLElBQUksQ0FBQyxPQUFPLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQztJQUNqQyxDQUFDO0lBRUQ7O09BRUc7SUFDSCxPQUFPO1FBQ0wsSUFBSSxJQUFJLENBQUMsVUFBVSxFQUFFO1lBQ25CLE9BQU87U0FDUjtRQUVELEtBQUssQ0FBQyxPQUFPLEVBQUUsQ0FBQztRQUNoQixJQUFJLENBQUMsT0FBTyxDQUFDLE9BQU8sRUFBRSxDQUFDO1FBQ3ZCLElBQUksQ0FBQyxhQUFhLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDN0IsSUFBSSxDQUFDLEtBQUssQ0FBQyxPQUFPLEVBQUUsQ0FBQztRQUNyQixJQUFJLENBQUMsTUFBTSxDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQ3hCLENBQUM7SUFFRDs7T0FFRztJQUNILE1BQU07UUFDSixJQUFJLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxNQUFNLEVBQUUsQ0FBQztJQUM1QixDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJO1FBQ0YsT0FBTyxJQUFJLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxJQUFJLEVBQUUsQ0FBQztJQUNqQyxDQUFDO0lBRUQ7O09BRUc7SUFDTyxhQUFhLENBQUMsR0FBWTtRQUNsQyxLQUFLLENBQUMsYUFBYSxDQUFDLEdBQUcsQ0FBQyxDQUFDO1FBQ3pCLElBQUksQ0FBQyxNQUFNLENBQUMsSUFBSSxFQUFFLENBQUM7UUFDbkIsSUFBSSxDQUFDLFdBQVcsRUFBRTthQUNmLElBQUksQ0FBQyxHQUFHLEVBQUU7WUFDVCxJQUFJLENBQUMsTUFBTSxDQUFDLElBQUksRUFBRSxDQUFDO1lBQ25CLElBQUksQ0FBQyxTQUFTLEVBQUUsQ0FBQztRQUNuQixDQUFDLENBQUM7YUFDRCxLQUFLLENBQUMsTUFBTSxDQUFDLEVBQUU7WUFDZCxPQUFPLENBQUMsS0FBSyxDQUFDLHNDQUFzQyxFQUFFLE1BQU0sQ0FBQyxDQUFDO1lBQzlELElBQUksQ0FBQyxNQUFNLENBQUMsSUFBSSxFQUFFLENBQUM7WUFDbkIsSUFBSSxDQUFDLFNBQVMsRUFBRSxDQUFDO1FBQ25CLENBQUMsQ0FBQyxDQUFDO0lBQ1AsQ0FBQztJQUVEOztPQUVHO0lBQ08sY0FBYyxDQUFDLEdBQVk7UUFDbkMsSUFBSSxDQUFDLE9BQU87YUFDVCxPQUFPLEVBQUU7YUFDVCxJQUFJLENBQUMsR0FBRyxFQUFFO1lBQ1QsS0FBSyxDQUFDLGNBQWMsQ0FBQyxHQUFHLENBQUMsQ0FBQztZQUMxQixJQUFJLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDakIsQ0FBQyxDQUFDO2FBQ0QsS0FBSyxDQUFDLEdBQUcsRUFBRTtZQUNWLFdBQVc7UUFDYixDQUFDLENBQUMsQ0FBQztJQUNQLENBQUM7SUFFRDs7T0FFRztJQUNLLFdBQVc7UUFDakIsSUFBSSxJQUFJLENBQUMsU0FBUyxFQUFFO1lBQ2xCLE9BQU8sSUFBSSxDQUFDLFNBQVMsQ0FBQztTQUN2QjtRQUVELE1BQU0sRUFBRSxHQUFHLEVBQUUsS0FBSyxFQUFFLEdBQUcsSUFBSSxDQUFDO1FBQzVCLE1BQU0sUUFBUSxHQUFHLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQyxHQUFHLENBQUMsRUFBRSxJQUFJLENBQUMsS0FBSyxDQUFDLENBQUM7UUFFaEQsT0FBTyxDQUFDLElBQUksQ0FBQyxTQUFTLEdBQUcsT0FBTyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxFQUFFLEVBQUU7WUFDOUQsSUFBSSxDQUFDLFNBQVMsR0FBRyxJQUFJLENBQUM7WUFFdEIsSUFBSSxJQUFJLENBQUMsT0FBTyxFQUFFO2dCQUNoQixPQUFPO2FBQ1I7WUFFRCxJQUFJLENBQUMsTUFBTSxHQUFHLE9BQU8sQ0FBQyxjQUFjLENBQUMsS0FBSyxFQUFFLElBQUksQ0FBQyxNQUFNLENBQUMsQ0FBQztRQUMzRCxDQUFDLENBQUMsQ0FBQyxDQUFDO0lBQ04sQ0FBQztJQUVEOztPQUVHO0lBQ0ssS0FBSyxDQUFDLGVBQWU7UUFDM0IsSUFBSSxDQUFDLE1BQU0sQ0FBQyxLQUFLLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQyxhQUFhLEVBQUUsQ0FBQztRQUNoRCxJQUFJLENBQUMsTUFBTSxDQUFDLFNBQVMsR0FBRyxJQUFJLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQztRQUMzQyxJQUFJLENBQUMsTUFBTSxDQUFDLFNBQVMsQ0FBQyxNQUFNLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQyxTQUFTLENBQUM7UUFDcEQsSUFBSTtZQUNGLE1BQU0sSUFBSSxDQUFDLFVBQVUsRUFBRSxDQUFDO1NBQ3pCO1FBQUMsT0FBTyxLQUFLLEVBQUU7WUFDZCxPQUFPLENBQUMsS0FBSyxDQUFDLG9DQUFvQyxFQUFFLEtBQUssQ0FBQyxDQUFDO1NBQzVEO1FBQ0QsSUFBSSxDQUFDLFNBQVMsRUFBRSxDQUFDO0lBQ25CLENBQUM7SUFFRDs7T0FFRztJQUNLLEtBQUssQ0FBQyxVQUFVO1FBQ3RCLE1BQU0sRUFBRSxHQUFHLEVBQUUsS0FBSyxFQUFFLEdBQUcsSUFBSSxDQUFDO1FBQzVCLE1BQU0sS0FBSyxHQUFHLElBQUksQ0FBQyxNQUFNLENBQUM7UUFFMUIsSUFBSSxDQUFDLE9BQU8sR0FBRyxJQUFJLENBQUM7UUFDcEIsSUFBSTtZQUNGLE1BQU0sS0FBSyxDQUFDLElBQUksQ0FBQyxHQUFHLEVBQUUsS0FBSyxDQUFDLENBQUM7WUFDN0IsSUFBSSxDQUFDLE9BQU8sR0FBRyxLQUFLLENBQUM7U0FDdEI7UUFBQyxPQUFPLEtBQUssRUFBRTtZQUNkLElBQUksQ0FBQyxPQUFPLEdBQUcsS0FBSyxDQUFDO1lBQ3JCLE1BQU0sS0FBSyxDQUFDO1NBQ2I7SUFDSCxDQUFDO0lBRUQ7O09BRUc7SUFDSyxVQUFVO1FBQ2hCLE1BQU0sTUFBTSxHQUFHLElBQUksQ0FBQyxPQUFPLENBQUM7UUFDNUIsTUFBTSxLQUFLLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQztRQUMxQixNQUFNLEtBQUssR0FBRyxJQUFJLENBQUMsTUFBTSxDQUFDO1FBRTFCLE1BQU0sQ0FBQyxLQUFLLEdBQUcsS0FBSyxDQUFDLFNBQVMsQ0FBQztRQUUvQiwwRUFBMEU7UUFDMUUseURBQXlEO1FBQ3pELHFCQUFxQixDQUFDLEdBQUcsRUFBRTtZQUN6QixLQUFLLENBQUMsZ0JBQWdCLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQyxDQUFDO1FBQ3RDLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVEOztPQUVHO0lBQ0ssU0FBUztRQUNmLE1BQU0sTUFBTSxHQUFHLElBQUksQ0FBQyxPQUFPLENBQUM7UUFDNUIsTUFBTSxJQUFJLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQztRQUN4QixNQUFNLEtBQUssR0FBRyxJQUFJLENBQUMsTUFBTSxDQUFDO1FBQzFCLE1BQU0sRUFBRSxTQUFTLEVBQUUsR0FBRyxJQUFJLENBQUMsTUFBTSxDQUFDO1FBRWxDLElBQUksQ0FBQyxTQUFTLENBQUMsTUFBTSxFQUFFO1lBQ3JCLE1BQU0sQ0FBQyxRQUFRLEdBQUcsSUFBSSxDQUFDO1lBQ3ZCLElBQUksQ0FBQyxTQUFTLEdBQUcsRUFBRSxDQUFDO1lBQ3BCLElBQUksQ0FBQyxVQUFVLEVBQUUsQ0FBQztZQUNsQixPQUFPO1NBQ1I7UUFFRCxJQUFJLE1BQU0sQ0FBQyxRQUFRLElBQUksTUFBTSxDQUFDLFFBQVEsQ0FBQyxFQUFFLEtBQUssU0FBUyxDQUFDLE1BQU0sRUFBRTtZQUM5RCxJQUFJLENBQUMsVUFBVSxFQUFFLENBQUM7WUFDbEIsT0FBTztTQUNSO1FBRUQsTUFBTSxZQUFZLEdBQUcsSUFBSSxDQUFDLGFBQWEsQ0FBQztRQUV4QyxJQUFJLENBQUMsUUFBUTthQUNWLElBQUksQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDO2FBQ3RCLElBQUksQ0FBQyxRQUFRLENBQUMsRUFBRTtZQUNmLElBQUksWUFBWSxDQUFDLFVBQVUsRUFBRTtnQkFDM0IsWUFBWSxDQUFDLE1BQU0sR0FBRyxJQUFJLENBQUM7YUFDNUI7WUFDRCxJQUFJLENBQUMsTUFBTSxDQUFDLFVBQVUsRUFBRTtnQkFDdEIsS0FBSyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsQ0FBQzthQUN6QjtZQUNELE1BQU0sQ0FBQyxRQUFRLEdBQUcsUUFBUSxDQUFDO1lBQzNCLElBQUksQ0FBQyxTQUFTLEdBQUcsU0FBUyxDQUFDLE1BQU0sQ0FBQztZQUNsQyxJQUFJLENBQUMsVUFBVSxFQUFFLENBQUM7UUFDcEIsQ0FBQyxDQUFDO2FBQ0QsS0FBSyxDQUFDLE1BQU0sQ0FBQyxFQUFFO1lBQ2QsT0FBTyxDQUFDLEtBQUssQ0FBQyxXQUFXLFNBQVMsQ0FBQyxNQUFNLG1CQUFtQixFQUFFLE1BQU0sQ0FBQyxDQUFDO1lBQ3RFLElBQUksQ0FBQyxTQUFTLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQyxTQUFTLENBQUMsTUFBTSxHQUFHLEVBQUUsQ0FBQztZQUNuRCxNQUFNLENBQUMsUUFBUSxHQUFHLElBQUksQ0FBQztZQUN2QixJQUFJLENBQUMsVUFBVSxFQUFFLENBQUM7UUFDcEIsQ0FBQyxDQUFDLENBQUM7SUFDUCxDQUFDO0NBV0Y7QUE2RkQ7O0dBRUc7QUFDSCxJQUFVLE9BQU8sQ0E2RWhCO0FBN0VELFdBQVUsT0FBTztJQUNmOztPQUVHO0lBQ0gsU0FBZ0Isd0JBQXdCLENBQ3RDLElBQWlCLEVBQ2pCLFVBQXdCO1FBRXhCLFVBQVUsR0FBRyxVQUFVLElBQUksbUVBQWMsQ0FBQztRQUMxQyxNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQzVDLDZDQUFlLENBQ2IsaURBQUMsMkNBQWM7WUFDYjtnQkFDRSxpREFBQyx3RUFBaUIsSUFDaEIsU0FBUyxFQUFDLG1DQUFtQyxFQUM3QyxHQUFHLEVBQUMsTUFBTSxFQUNWLGVBQWUsRUFBQyxRQUFRLEVBQ3hCLE1BQU0sRUFBQyxNQUFNLEVBQ2IsS0FBSyxFQUFDLE1BQU0sR0FDWjtnQkFDRiwyREFBTSxTQUFTLEVBQUMsb0NBQW9DLGVBQWdCLENBQ2pFO1lBQ0wsMkRBQU0sU0FBUyxFQUFDLG1DQUFtQyxJQUNoRCxLQUFLLENBQUMsRUFBRSxDQUNQLGlFQUFpRSxDQUNsRSxDQUNJLENBQ1EsRUFDakIsSUFBSSxDQUNMLENBQUM7SUFDSixDQUFDO0lBMUJlLGdDQUF3QiwyQkEwQnZDO0lBRUQ7O09BRUc7SUFDSCxTQUFnQixjQUFjLENBQzVCLEtBQXdCLEVBQ3hCLE9BQW1DO1FBRW5DLElBQUksQ0FBQyxLQUFLLEVBQUU7WUFDVixPQUFPLCtEQUFnQixDQUFDLGNBQWMsQ0FBQyxDQUFDO1NBQ3pDO1FBRUQsSUFBSSxDQUFDLENBQUMsT0FBTyxJQUFJLEtBQUssQ0FBQyxJQUFJLENBQUMsV0FBVyxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUMsRUFBRTtZQUNwRCxLQUFLLENBQUMsS0FBSyxHQUFHLCtEQUFnQixDQUFDLGNBQWMsQ0FBQyxLQUFLLENBQUMsQ0FBQztTQUN0RDtRQUNELElBQUksQ0FBQyxDQUFDLFdBQVcsSUFBSSxLQUFLLENBQUMsRUFBRTtZQUMzQixLQUFLLENBQUMsU0FBUyxHQUFHLCtEQUFnQixDQUFDLGNBQWMsQ0FBQyxTQUFTLENBQUMsQ0FBQztZQUM3RCxPQUFPLEtBQW1DLENBQUM7U0FDNUM7UUFFRCxNQUFNLFNBQVMsR0FDYixXQUFXLElBQUksS0FBSztZQUNwQixLQUFLLENBQUMsU0FBUztZQUNmLE9BQU8sS0FBSyxDQUFDLFNBQVMsS0FBSyxRQUFRO1lBQ2pDLENBQUMsQ0FBRSxLQUFLLENBQUMsU0FBd0I7WUFDakMsQ0FBQyxDQUFDLEVBQUUsQ0FBQztRQUVULEtBQUssQ0FBQyxTQUFTLEdBQUc7WUFDaEIsTUFBTSxFQUNKLE9BQU8sU0FBUyxDQUFDLE1BQU0sS0FBSyxRQUFRO2dCQUNsQyxDQUFDLENBQUMsU0FBUyxDQUFDLE1BQU07Z0JBQ2xCLENBQUMsQ0FBQyxjQUFjLENBQUMsU0FBUyxDQUFDLE1BQU07WUFDckMsS0FBSyxFQUFFLFdBQVcsQ0FBQyxTQUFTLENBQUMsS0FBSyxDQUFDO2dCQUNqQyxDQUFDLENBQUMsU0FBUyxDQUFDLEtBQUs7Z0JBQ2pCLENBQUMsQ0FBQywrREFBZ0IsQ0FBQyxjQUFjLENBQUMsU0FBUyxDQUFDLEtBQUssQ0FBQztTQUNyRCxDQUFDO1FBRUYsT0FBTyxLQUFtQyxDQUFDO0lBQzdDLENBQUM7SUFsQ2Usc0JBQWMsaUJBa0M3QjtJQUVEOztPQUVHO0lBQ0gsU0FBUyxXQUFXLENBQUMsS0FBZ0I7UUFDbkMsT0FBTyxLQUFLLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxJQUFJLEtBQUssQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxPQUFPLENBQUMsS0FBSyxRQUFRLENBQUMsQ0FBQztJQUN6RSxDQUFDO0FBQ0gsQ0FBQyxFQTdFUyxPQUFPLEtBQVAsT0FBTyxRQTZFaEI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDdGZEOzs7K0VBRytFO0FBRTNCO0FBQ0c7QUFFdkQ7OztHQUdHO0FBQ0ksTUFBTSxVQUFXLFNBQVEsdURBQU07SUFBdEM7O1FBQ0U7O1dBRUc7UUFDTSxnQkFBVyxHQUF1QixJQUFJLHFEQUFNLENBQVksSUFBSSxDQUFDLENBQUM7SUFTekUsQ0FBQztJQVBDLFdBQVcsQ0FBQyxLQUFZO1FBQ3RCLEtBQUssQ0FBQyxXQUFXLENBQUMsS0FBSyxDQUFDLENBQUM7UUFFekIsSUFBSSxLQUFLLENBQUMsSUFBSSxLQUFLLFNBQVMsRUFBRTtZQUMzQixJQUFJLENBQUMsV0FBaUMsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLENBQUM7U0FDekQ7SUFDSCxDQUFDO0NBQ0Y7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ3pCRCwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBR2pCO0FBRzFDLG9CQUFvQjtBQUNwQjs7R0FFRztBQUNJLE1BQU0scUJBQXFCLEdBQUcsSUFBSSxvREFBSyxDQUM1QyxpREFBaUQsQ0FDbEQsQ0FBQyIsImZpbGUiOiJwYWNrYWdlc19zZXR0aW5nZWRpdG9yX2xpYl9pbmRleF9qcy5kNDM0YzAzNTc3MjIwY2FhYjlmMy5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHNldHRpbmdlZGl0b3JcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL3NldHRpbmdlZGl0b3InO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuIiwiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG5cbmltcG9ydCB7IEluc3BlY3Rpb25IYW5kbGVyLCBJbnNwZWN0b3JQYW5lbCB9IGZyb20gJ0BqdXB5dGVybGFiL2luc3BlY3Rvcic7XG5pbXBvcnQge1xuICBJUmVuZGVyTWltZVJlZ2lzdHJ5LFxuICBSZW5kZXJNaW1lUmVnaXN0cnksXG4gIHN0YW5kYXJkUmVuZGVyZXJGYWN0b3JpZXNcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJU2NoZW1hVmFsaWRhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IERhdGFDb25uZWN0b3IgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgUmVhZG9ubHlKU09OT2JqZWN0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgUmF3RWRpdG9yIH0gZnJvbSAnLi9yYXdlZGl0b3InO1xuXG4vKipcbiAqIENyZWF0ZSBhIHJhdyBlZGl0b3IgaW5zcGVjdG9yLlxuICovXG5leHBvcnQgZnVuY3Rpb24gY3JlYXRlSW5zcGVjdG9yKFxuICBlZGl0b3I6IFJhd0VkaXRvcixcbiAgcmVuZGVybWltZT86IElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuKTogSW5zcGVjdG9yUGFuZWwge1xuICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgY29ubmVjdG9yID0gbmV3IEluc3BlY3RvckNvbm5lY3RvcihlZGl0b3IsIHRyYW5zbGF0b3IpO1xuICBjb25zdCBpbnNwZWN0b3IgPSBuZXcgSW5zcGVjdG9yUGFuZWwoe1xuICAgIGluaXRpYWxDb250ZW50OiB0cmFucy5fXygnQW55IGVycm9ycyB3aWxsIGJlIGxpc3RlZCBoZXJlJyksXG4gICAgdHJhbnNsYXRvcjogdHJhbnNsYXRvclxuICB9KTtcbiAgY29uc3QgaGFuZGxlciA9IG5ldyBJbnNwZWN0aW9uSGFuZGxlcih7XG4gICAgY29ubmVjdG9yLFxuICAgIHJlbmRlcm1pbWU6XG4gICAgICByZW5kZXJtaW1lIHx8XG4gICAgICBuZXcgUmVuZGVyTWltZVJlZ2lzdHJ5KHtcbiAgICAgICAgaW5pdGlhbEZhY3Rvcmllczogc3RhbmRhcmRSZW5kZXJlckZhY3RvcmllcyxcbiAgICAgICAgdHJhbnNsYXRvcjogdHJhbnNsYXRvclxuICAgICAgfSlcbiAgfSk7XG5cbiAgaW5zcGVjdG9yLmFkZENsYXNzKCdqcC1TZXR0aW5nc0RlYnVnJyk7XG4gIGluc3BlY3Rvci5zb3VyY2UgPSBoYW5kbGVyO1xuICBoYW5kbGVyLmVkaXRvciA9IGVkaXRvci5zb3VyY2U7XG5cbiAgcmV0dXJuIGluc3BlY3Rvcjtcbn1cblxuLyoqXG4gKiBUaGUgZGF0YSBjb25uZWN0b3IgdXNlZCB0byBwb3B1bGF0ZSBhIGNvZGUgaW5zcGVjdG9yLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIFRoaXMgZGF0YSBjb25uZWN0b3IgZGVib3VuY2VzIGZldGNoIHJlcXVlc3RzIHRvIHRocm90dGxlIHRoZW0gYXQgbm8gbW9yZSB0aGFuXG4gKiBvbmUgcmVxdWVzdCBwZXIgMTAwbXMuIFRoaXMgbWVhbnMgdGhhdCB1c2luZyB0aGUgY29ubmVjdG9yIHRvIHBvcHVsYXRlXG4gKiBtdWx0aXBsZSBjbGllbnQgb2JqZWN0cyBjYW4gbGVhZCB0byBtaXNzZWQgZmV0Y2ggcmVzcG9uc2VzLlxuICovXG5jbGFzcyBJbnNwZWN0b3JDb25uZWN0b3IgZXh0ZW5kcyBEYXRhQ29ubmVjdG9yPFxuICBJbnNwZWN0aW9uSGFuZGxlci5JUmVwbHksXG4gIHZvaWQsXG4gIEluc3BlY3Rpb25IYW5kbGVyLklSZXF1ZXN0XG4+IHtcbiAgY29uc3RydWN0b3IoZWRpdG9yOiBSYXdFZGl0b3IsIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcikge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl9lZGl0b3IgPSBlZGl0b3I7XG4gICAgdGhpcy5fdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICB9XG5cbiAgLyoqXG4gICAqIEZldGNoIGluc3BlY3Rpb24gcmVxdWVzdHMuXG4gICAqL1xuICBmZXRjaChcbiAgICByZXF1ZXN0OiBJbnNwZWN0aW9uSGFuZGxlci5JUmVxdWVzdFxuICApOiBQcm9taXNlPEluc3BlY3Rpb25IYW5kbGVyLklSZXBseSB8IHVuZGVmaW5lZD4ge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZTxJbnNwZWN0aW9uSGFuZGxlci5JUmVwbHkgfCB1bmRlZmluZWQ+KHJlc29sdmUgPT4ge1xuICAgICAgLy8gRGVib3VuY2UgcmVxdWVzdHMgYXQgYSByYXRlIG9mIDEwMG1zLlxuICAgICAgY29uc3QgY3VycmVudCA9ICh0aGlzLl9jdXJyZW50ID0gd2luZG93LnNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgICBpZiAoY3VycmVudCAhPT0gdGhpcy5fY3VycmVudCkge1xuICAgICAgICAgIHJldHVybiByZXNvbHZlKHVuZGVmaW5lZCk7XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBlcnJvcnMgPSB0aGlzLl92YWxpZGF0ZShyZXF1ZXN0LnRleHQpO1xuXG4gICAgICAgIGlmICghZXJyb3JzKSB7XG4gICAgICAgICAgcmV0dXJuIHJlc29sdmUoe1xuICAgICAgICAgICAgZGF0YTogeyAndGV4dC9tYXJrZG93bic6IHRoaXMuX3RyYW5zLl9fKCdObyBlcnJvcnMgZm91bmQnKSB9LFxuICAgICAgICAgICAgbWV0YWRhdGE6IHt9XG4gICAgICAgICAgfSk7XG4gICAgICAgIH1cblxuICAgICAgICByZXNvbHZlKHsgZGF0YTogUHJpdmF0ZS5yZW5kZXIoZXJyb3JzKSwgbWV0YWRhdGE6IHt9IH0pO1xuICAgICAgfSwgMTAwKSk7XG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF92YWxpZGF0ZShyYXc6IHN0cmluZyk6IElTY2hlbWFWYWxpZGF0b3IuSUVycm9yW10gfCBudWxsIHtcbiAgICBjb25zdCBlZGl0b3IgPSB0aGlzLl9lZGl0b3I7XG4gICAgaWYgKCFlZGl0b3Iuc2V0dGluZ3MpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICBjb25zdCB7IGlkLCBzY2hlbWEsIHZlcnNpb24gfSA9IGVkaXRvci5zZXR0aW5ncztcbiAgICBjb25zdCBkYXRhID0geyBjb21wb3NpdGU6IHt9LCB1c2VyOiB7fSB9O1xuICAgIGNvbnN0IHZhbGlkYXRvciA9IGVkaXRvci5yZWdpc3RyeS52YWxpZGF0b3I7XG5cbiAgICByZXR1cm4gdmFsaWRhdG9yLnZhbGlkYXRlRGF0YSh7IGRhdGEsIGlkLCByYXcsIHNjaGVtYSwgdmVyc2lvbiB9LCBmYWxzZSk7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfY3VycmVudCA9IDA7XG4gIHByaXZhdGUgX2VkaXRvcjogUmF3RWRpdG9yO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIG1vZHVsZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBSZW5kZXIgdmFsaWRhdGlvbiBlcnJvcnMgYXMgYW4gSFRNTCBzdHJpbmcuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcmVuZGVyKFxuICAgIGVycm9yczogSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JbXVxuICApOiBSZWFkb25seUpTT05PYmplY3Qge1xuICAgIHJldHVybiB7ICd0ZXh0L21hcmtkb3duJzogZXJyb3JzLm1hcChyZW5kZXJFcnJvcikuam9pbignJykgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgYW4gaW5kaXZpZHVhbCB2YWxpZGF0aW9uIGVycm9yIGFzIGEgbWFya2Rvd24gc3RyaW5nLlxuICAgKi9cbiAgZnVuY3Rpb24gcmVuZGVyRXJyb3IoZXJyb3I6IElTY2hlbWFWYWxpZGF0b3IuSUVycm9yKTogc3RyaW5nIHtcbiAgICBzd2l0Y2ggKGVycm9yLmtleXdvcmQpIHtcbiAgICAgIGNhc2UgJ2FkZGl0aW9uYWxQcm9wZXJ0aWVzJzpcbiAgICAgICAgcmV0dXJuIGAqKlxcYFthZGRpdGlvbmFsIHByb3BlcnR5IGVycm9yXVxcYCoqXG4gICAgICAgICAgXFxgJHtlcnJvci5wYXJhbXM/LmFkZGl0aW9uYWxQcm9wZXJ0eX1cXGAgaXMgbm90IGEgdmFsaWQgcHJvcGVydHlgO1xuICAgICAgY2FzZSAnc3ludGF4JzpcbiAgICAgICAgcmV0dXJuIGAqKlxcYFtzeW50YXggZXJyb3JdXFxgKiogKiR7ZXJyb3IubWVzc2FnZX0qYDtcbiAgICAgIGNhc2UgJ3R5cGUnOlxuICAgICAgICByZXR1cm4gYCoqXFxgW3R5cGUgZXJyb3JdXFxgKipcbiAgICAgICAgICBcXGAke2Vycm9yLmRhdGFQYXRofVxcYCAke2Vycm9yLm1lc3NhZ2V9YDtcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIHJldHVybiBgKipcXGBbZXJyb3JdXFxgKiogKiR7ZXJyb3IubWVzc2FnZX0qYDtcbiAgICB9XG4gIH1cbn1cbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuXG5pbXBvcnQgeyBEaWFsb2csIHNob3dEaWFsb2cgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQgeyBJUmVuZGVyTWltZVJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgQ29tbWFuZFJlZ2lzdHJ5IH0gZnJvbSAnQGx1bWluby9jb21tYW5kcyc7XG5pbXBvcnQgeyBKU09ORXh0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFN0YWNrZWRMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBSYXdFZGl0b3IgfSBmcm9tICcuL3Jhd2VkaXRvcic7XG5pbXBvcnQgeyBTZXR0aW5nRWRpdG9yIH0gZnJvbSAnLi9zZXR0aW5nZWRpdG9yJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhbGwgcGx1Z2luIGVkaXRvcnMuXG4gKi9cbmNvbnN0IFBMVUdJTl9FRElUT1JfQ0xBU1MgPSAnanAtUGx1Z2luRWRpdG9yJztcblxuLyoqXG4gKiBBbiBpbmRpdmlkdWFsIHBsdWdpbiBzZXR0aW5ncyBlZGl0b3IuXG4gKi9cbmV4cG9ydCBjbGFzcyBQbHVnaW5FZGl0b3IgZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHBsdWdpbiBlZGl0b3IuXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIHBsdWdpbiBlZGl0b3IgaW5zdGFudGlhdGlvbiBvcHRpb25zLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogUGx1Z2luRWRpdG9yLklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLmFkZENsYXNzKFBMVUdJTl9FRElUT1JfQ0xBU1MpO1xuXG4gICAgY29uc3Qge1xuICAgICAgY29tbWFuZHMsXG4gICAgICBlZGl0b3JGYWN0b3J5LFxuICAgICAgcmVnaXN0cnksXG4gICAgICByZW5kZXJtaW1lLFxuICAgICAgdHJhbnNsYXRvclxuICAgIH0gPSBvcHRpb25zO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5fdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgLy8gVE9ETzogUmVtb3ZlIHRoaXMgbGF5b3V0LiBXZSB3ZXJlIHVzaW5nIHRoaXMgYmVmb3JlIHdoZW4gd2VcbiAgICAvLyB3aGVuIHdlIGhhZCBhIHdheSB0byBzd2l0Y2ggYmV0d2VlbiB0aGUgcmF3IGFuZCB0YWJsZSBlZGl0b3JcbiAgICAvLyBOb3csIHRoZSByYXcgZWRpdG9yIGlzIHRoZSBvbmx5IGNoaWxkIGFuZCBwcm9iYWJseSBjb3VsZCBtZXJnZWQgaW50b1xuICAgIC8vIHRoaXMgY2xhc3MgZGlyZWN0bHkgaW4gdGhlIGZ1dHVyZS5cbiAgICBjb25zdCBsYXlvdXQgPSAodGhpcy5sYXlvdXQgPSBuZXcgU3RhY2tlZExheW91dCgpKTtcbiAgICBjb25zdCB7IG9uU2F2ZUVycm9yIH0gPSBQcml2YXRlO1xuXG4gICAgdGhpcy5yYXcgPSB0aGlzLl9yYXdFZGl0b3IgPSBuZXcgUmF3RWRpdG9yKHtcbiAgICAgIGNvbW1hbmRzLFxuICAgICAgZWRpdG9yRmFjdG9yeSxcbiAgICAgIG9uU2F2ZUVycm9yLFxuICAgICAgcmVnaXN0cnksXG4gICAgICByZW5kZXJtaW1lLFxuICAgICAgdHJhbnNsYXRvclxuICAgIH0pO1xuICAgIHRoaXMuX3Jhd0VkaXRvci5oYW5kbGVNb3ZlZC5jb25uZWN0KHRoaXMuX29uU3RhdGVDaGFuZ2VkLCB0aGlzKTtcblxuICAgIGxheW91dC5hZGRXaWRnZXQodGhpcy5fcmF3RWRpdG9yKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgcGx1Z2luIGVkaXRvcidzIHJhdyBlZGl0b3IuXG4gICAqL1xuICByZWFkb25seSByYXc6IFJhd0VkaXRvcjtcblxuICAvKipcbiAgICogVGVzdHMgd2hldGhlciB0aGUgc2V0dGluZ3MgaGF2ZSBiZWVuIG1vZGlmaWVkIGFuZCBuZWVkIHNhdmluZy5cbiAgICovXG4gIGdldCBpc0RpcnR5KCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9yYXdFZGl0b3IuaXNEaXJ0eTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgcGx1Z2luIHNldHRpbmdzIGJlaW5nIGVkaXRlZC5cbiAgICovXG4gIGdldCBzZXR0aW5ncygpOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyB8IG51bGwge1xuICAgIHJldHVybiB0aGlzLl9zZXR0aW5ncztcbiAgfVxuICBzZXQgc2V0dGluZ3Moc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzIHwgbnVsbCkge1xuICAgIGlmICh0aGlzLl9zZXR0aW5ncyA9PT0gc2V0dGluZ3MpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCByYXcgPSB0aGlzLl9yYXdFZGl0b3I7XG5cbiAgICB0aGlzLl9zZXR0aW5ncyA9IHJhdy5zZXR0aW5ncyA9IHNldHRpbmdzO1xuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHBsdWdpbiBlZGl0b3IgbGF5b3V0IHN0YXRlLlxuICAgKi9cbiAgZ2V0IHN0YXRlKCk6IFNldHRpbmdFZGl0b3IuSVBsdWdpbkxheW91dCB7XG4gICAgY29uc3QgcGx1Z2luID0gdGhpcy5fc2V0dGluZ3MgPyB0aGlzLl9zZXR0aW5ncy5pZCA6ICcnO1xuICAgIGNvbnN0IHsgc2l6ZXMgfSA9IHRoaXMuX3Jhd0VkaXRvcjtcblxuICAgIHJldHVybiB7IHBsdWdpbiwgc2l6ZXMgfTtcbiAgfVxuICBzZXQgc3RhdGUoc3RhdGU6IFNldHRpbmdFZGl0b3IuSVBsdWdpbkxheW91dCkge1xuICAgIGlmIChKU09ORXh0LmRlZXBFcXVhbCh0aGlzLnN0YXRlLCBzdGF0ZSkpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLl9yYXdFZGl0b3Iuc2l6ZXMgPSBzdGF0ZS5zaXplcztcbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIHRoYXQgZW1pdHMgd2hlbiBlZGl0b3IgbGF5b3V0IHN0YXRlIGNoYW5nZXMgYW5kIG5lZWRzIHRvIGJlIHNhdmVkLlxuICAgKi9cbiAgZ2V0IHN0YXRlQ2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fc3RhdGVDaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIElmIHRoZSBlZGl0b3IgaXMgaW4gYSBkaXJ0eSBzdGF0ZSwgY29uZmlybSB0aGF0IHRoZSB1c2VyIHdhbnRzIHRvIGxlYXZlLlxuICAgKi9cbiAgY29uZmlybSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBpZiAodGhpcy5pc0hpZGRlbiB8fCAhdGhpcy5pc0F0dGFjaGVkIHx8ICF0aGlzLmlzRGlydHkpIHtcbiAgICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUodW5kZWZpbmVkKTtcbiAgICB9XG5cbiAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICB0aXRsZTogdGhpcy5fdHJhbnMuX18oJ1lvdSBoYXZlIHVuc2F2ZWQgY2hhbmdlcy4nKSxcbiAgICAgIGJvZHk6IHRoaXMuX3RyYW5zLl9fKCdEbyB5b3Ugd2FudCB0byBsZWF2ZSB3aXRob3V0IHNhdmluZz8nKSxcbiAgICAgIGJ1dHRvbnM6IFtcbiAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbih7IGxhYmVsOiB0aGlzLl90cmFucy5fXygnQ2FuY2VsJykgfSksXG4gICAgICAgIERpYWxvZy5va0J1dHRvbih7IGxhYmVsOiB0aGlzLl90cmFucy5fXygnT2snKSB9KVxuICAgICAgXVxuICAgIH0pLnRoZW4ocmVzdWx0ID0+IHtcbiAgICAgIGlmICghcmVzdWx0LmJ1dHRvbi5hY2NlcHQpIHtcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKCdVc2VyIGNhbmNlbGVkLicpO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBwbHVnaW4gZWRpdG9yLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICAgIHRoaXMuX3Jhd0VkaXRvci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBhZnRlci1hdHRhY2hgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCd1cGRhdGUtcmVxdWVzdCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uVXBkYXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBjb25zdCByYXcgPSB0aGlzLl9yYXdFZGl0b3I7XG4gICAgY29uc3Qgc2V0dGluZ3MgPSB0aGlzLl9zZXR0aW5ncztcblxuICAgIGlmICghc2V0dGluZ3MpIHtcbiAgICAgIHRoaXMuaGlkZSgpO1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRoaXMuc2hvdygpO1xuICAgIHJhdy5zaG93KCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGxheW91dCBzdGF0ZSBjaGFuZ2VzIHRoYXQgbmVlZCB0byBiZSBzYXZlZC5cbiAgICovXG4gIHByaXZhdGUgX29uU3RhdGVDaGFuZ2VkKCk6IHZvaWQge1xuICAgICh0aGlzLnN0YXRlQ2hhbmdlZCBhcyBTaWduYWw8YW55LCB2b2lkPikuZW1pdCh1bmRlZmluZWQpO1xuICB9XG5cbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF90cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG4gIHByaXZhdGUgX3Jhd0VkaXRvcjogUmF3RWRpdG9yO1xuICBwcml2YXRlIF9zZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfc3RhdGVDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCB2b2lkPih0aGlzKTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYFBsdWdpbkVkaXRvcmAgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBQbHVnaW5FZGl0b3Ige1xuICAvKipcbiAgICogVGhlIGluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgYSBwbHVnaW4gZWRpdG9yLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIHRvb2xiYXIgY29tbWFuZHMgYW5kIHJlZ2lzdHJ5IGZvciB0aGUgc2V0dGluZyBlZGl0b3IgdG9vbGJhci5cbiAgICAgKi9cbiAgICBjb21tYW5kczoge1xuICAgICAgLyoqXG4gICAgICAgKiBUaGUgY29tbWFuZCByZWdpc3RyeS5cbiAgICAgICAqL1xuICAgICAgcmVnaXN0cnk6IENvbW1hbmRSZWdpc3RyeTtcblxuICAgICAgLyoqXG4gICAgICAgKiBUaGUgcmV2ZXJ0IGNvbW1hbmQgSUQuXG4gICAgICAgKi9cbiAgICAgIHJldmVydDogc3RyaW5nO1xuXG4gICAgICAvKipcbiAgICAgICAqIFRoZSBzYXZlIGNvbW1hbmQgSUQuXG4gICAgICAgKi9cbiAgICAgIHNhdmU6IHN0cmluZztcbiAgICB9O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGVkaXRvciBmYWN0b3J5IHVzZWQgYnkgdGhlIHBsdWdpbiBlZGl0b3IuXG4gICAgICovXG4gICAgZWRpdG9yRmFjdG9yeTogQ29kZUVkaXRvci5GYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHNldHRpbmcgcmVnaXN0cnkgdXNlZCBieSB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIG9wdGlvbmFsIE1JTUUgcmVuZGVyZXIgdG8gdXNlIGZvciByZW5kZXJpbmcgZGVidWcgbWVzc2FnZXMuXG4gICAgICovXG4gICAgcmVuZGVybWltZT86IElSZW5kZXJNaW1lUmVnaXN0cnk7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBtb2R1bGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogSGFuZGxlIHNhdmUgZXJyb3JzLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIG9uU2F2ZUVycm9yKHJlYXNvbjogYW55LCB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3IpOiB2b2lkIHtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnNvbGUuZXJyb3IoYFNhdmluZyBzZXR0aW5nIGVkaXRvciB2YWx1ZSBmYWlsZWQ6ICR7cmVhc29uLm1lc3NhZ2V9YCk7XG4gICAgdm9pZCBzaG93RGlhbG9nKHtcbiAgICAgIHRpdGxlOiB0cmFucy5fXygnWW91ciBjaGFuZ2VzIHdlcmUgbm90IHNhdmVkLicpLFxuICAgICAgYm9keTogcmVhc29uLm1lc3NhZ2UsXG4gICAgICBidXR0b25zOiBbRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdPaycpIH0pXVxuICAgIH0pO1xuICB9XG59XG4iLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cblxuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBjbGFzc2VzLCBMYWJJY29uLCBzZXR0aW5nc0ljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0ICogYXMgUmVhY3RET00gZnJvbSAncmVhY3QtZG9tJztcblxuLyoqXG4gKiBBIGxpc3Qgb2YgcGx1Z2lucyB3aXRoIGVkaXRhYmxlIHNldHRpbmdzLlxuICovXG5leHBvcnQgY2xhc3MgUGx1Z2luTGlzdCBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgcGx1Z2luIGxpc3QuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBQbHVnaW5MaXN0LklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLnJlZ2lzdHJ5ID0gb3B0aW9ucy5yZWdpc3RyeTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtUGx1Z2luTGlzdCcpO1xuICAgIHRoaXMuX2NvbmZpcm0gPSBvcHRpb25zLmNvbmZpcm07XG4gICAgdGhpcy5yZWdpc3RyeS5wbHVnaW5DaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgdGhpcy51cGRhdGUoKTtcbiAgICB9LCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICovXG4gIHJlYWRvbmx5IHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5O1xuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gYSBsaXN0IHVzZXIgaW50ZXJhY3Rpb24gaGFwcGVucy5cbiAgICovXG4gIGdldCBjaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgdm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9jaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBzZWxlY3Rpb24gdmFsdWUgb2YgdGhlIHBsdWdpbiBsaXN0LlxuICAgKi9cbiAgZ2V0IHNjcm9sbFRvcCgpOiBudW1iZXIgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiB0aGlzLm5vZGUucXVlcnlTZWxlY3RvcigndWwnKT8uc2Nyb2xsVG9wO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBzZWxlY3Rpb24gdmFsdWUgb2YgdGhlIHBsdWdpbiBsaXN0LlxuICAgKi9cbiAgZ2V0IHNlbGVjdGlvbigpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLl9zZWxlY3Rpb247XG4gIH1cbiAgc2V0IHNlbGVjdGlvbihzZWxlY3Rpb246IHN0cmluZykge1xuICAgIGlmICh0aGlzLl9zZWxlY3Rpb24gPT09IHNlbGVjdGlvbikge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9zZWxlY3Rpb24gPSBzZWxlY3Rpb247XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIERPTSBldmVudHMgZm9yIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSBldmVudCAtIFRoZSBET00gZXZlbnQgc2VudCB0byB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgbWV0aG9kIGltcGxlbWVudHMgdGhlIERPTSBgRXZlbnRMaXN0ZW5lcmAgaW50ZXJmYWNlIGFuZCBpc1xuICAgKiBjYWxsZWQgaW4gcmVzcG9uc2UgdG8gZXZlbnRzIG9uIHRoZSBwbHVnaW4gbGlzdCdzIG5vZGUuIEl0IHNob3VsZFxuICAgKiBub3QgYmUgY2FsbGVkIGRpcmVjdGx5IGJ5IHVzZXIgY29kZS5cbiAgICovXG4gIGhhbmRsZUV2ZW50KGV2ZW50OiBFdmVudCk6IHZvaWQge1xuICAgIHN3aXRjaCAoZXZlbnQudHlwZSkge1xuICAgICAgY2FzZSAnbW91c2Vkb3duJzpcbiAgICAgICAgdGhpcy5fZXZ0TW91c2Vkb3duKGV2ZW50IGFzIE1vdXNlRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhZnRlci1hdHRhY2gnYCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFmdGVyQXR0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHRoaXMubm9kZS5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzKTtcbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYmVmb3JlLWRldGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5ub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ21vdXNlZG93bicsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ3VwZGF0ZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25VcGRhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGNvbnN0IHsgbm9kZSwgcmVnaXN0cnkgfSA9IHRoaXM7XG4gICAgY29uc3Qgc2VsZWN0aW9uID0gdGhpcy5fc2VsZWN0aW9uO1xuICAgIGNvbnN0IHRyYW5zbGF0aW9uID0gdGhpcy50cmFuc2xhdG9yO1xuXG4gICAgUHJpdmF0ZS5wb3B1bGF0ZUxpc3QocmVnaXN0cnksIHNlbGVjdGlvbiwgbm9kZSwgdHJhbnNsYXRpb24pO1xuICAgIGNvbnN0IHVsID0gbm9kZS5xdWVyeVNlbGVjdG9yKCd1bCcpO1xuICAgIGlmICh1bCAmJiB0aGlzLl9zY3JvbGxUb3AgIT09IHVuZGVmaW5lZCkge1xuICAgICAgdWwuc2Nyb2xsVG9wID0gdGhpcy5fc2Nyb2xsVG9wO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGAnbW91c2Vkb3duJ2AgZXZlbnQgZm9yIHRoZSBwbHVnaW4gbGlzdC5cbiAgICpcbiAgICogQHBhcmFtIGV2ZW50IC0gVGhlIERPTSBldmVudCBzZW50IHRvIHRoZSB3aWRnZXRcbiAgICovXG4gIHByaXZhdGUgX2V2dE1vdXNlZG93bihldmVudDogTW91c2VFdmVudCk6IHZvaWQge1xuICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG5cbiAgICBsZXQgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgIGxldCBpZCA9IHRhcmdldC5nZXRBdHRyaWJ1dGUoJ2RhdGEtaWQnKTtcblxuICAgIGlmIChpZCA9PT0gdGhpcy5fc2VsZWN0aW9uKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgaWYgKCFpZCkge1xuICAgICAgd2hpbGUgKCFpZCAmJiB0YXJnZXQgIT09IHRoaXMubm9kZSkge1xuICAgICAgICB0YXJnZXQgPSB0YXJnZXQucGFyZW50RWxlbWVudCBhcyBIVE1MRWxlbWVudDtcbiAgICAgICAgaWQgPSB0YXJnZXQuZ2V0QXR0cmlidXRlKCdkYXRhLWlkJyk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgaWYgKCFpZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRoaXMuX2NvbmZpcm0oKVxuICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICB0aGlzLl9zY3JvbGxUb3AgPSB0aGlzLnNjcm9sbFRvcDtcbiAgICAgICAgdGhpcy5fc2VsZWN0aW9uID0gaWQhO1xuICAgICAgICB0aGlzLl9jaGFuZ2VkLmVtaXQodW5kZWZpbmVkKTtcbiAgICAgICAgdGhpcy51cGRhdGUoKTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goKCkgPT4ge1xuICAgICAgICAvKiBubyBvcCAqL1xuICAgICAgfSk7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX2NoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIHZvaWQ+KHRoaXMpO1xuICBwcml2YXRlIF9jb25maXJtOiAoKSA9PiBQcm9taXNlPHZvaWQ+O1xuICBwcml2YXRlIF9zY3JvbGxUb3A6IG51bWJlciB8IHVuZGVmaW5lZCA9IDA7XG4gIHByaXZhdGUgX3NlbGVjdGlvbiA9ICcnO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgUGx1Z2luTGlzdGAgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBQbHVnaW5MaXN0IHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgcGx1Z2luIGxpc3QuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRoYXQgYWxsb3dzIGZvciBhc3luY2hyb25vdXNseSBjb25maXJtaW5nIGEgc2VsZWN0aW9uLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc3RcbiAgICAgKiBJZiB0aGUgcHJvbWlzZSByZXR1cm5lZCBieSB0aGUgZnVuY3Rpb24gcmVzb2x2ZXMsIHRoZW4gdGhlIHNlbGVjdGlvbiB3aWxsXG4gICAgICogc3VjY2VlZCBhbmQgZW1pdCBhbiBldmVudC4gSWYgdGhlIHByb21pc2UgcmVqZWN0cywgdGhlIHNlbGVjdGlvbiBpcyBub3RcbiAgICAgKiBtYWRlLlxuICAgICAqL1xuICAgIGNvbmZpcm06ICgpID0+IFByb21pc2U8dm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2V0dGluZyByZWdpc3RyeSBmb3IgdGhlIHBsdWdpbiBsaXN0LlxuICAgICAqL1xuICAgIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHNldHRpbmcgcmVnaXN0cnkgZm9yIHRoZSBwbHVnaW4gbGlzdC5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBtb2R1bGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogVGhlIEp1cHl0ZXJMYWIgcGx1Z2luIHNjaGVtYSBrZXkgZm9yIHRoZSBzZXR0aW5nIGVkaXRvclxuICAgKiBpY29uIGNsYXNzIG9mIGEgcGx1Z2luLlxuICAgKi9cbiAgY29uc3QgSUNPTl9LRVkgPSAnanVweXRlci5sYWIuc2V0dGluZy1pY29uJztcblxuICAvKipcbiAgICogVGhlIEp1cHl0ZXJMYWIgcGx1Z2luIHNjaGVtYSBrZXkgZm9yIHRoZSBzZXR0aW5nIGVkaXRvclxuICAgKiBpY29uIGNsYXNzIG9mIGEgcGx1Z2luLlxuICAgKi9cbiAgY29uc3QgSUNPTl9DTEFTU19LRVkgPSAnanVweXRlci5sYWIuc2V0dGluZy1pY29uLWNsYXNzJztcblxuICAvKipcbiAgICogVGhlIEp1cHl0ZXJMYWIgcGx1Z2luIHNjaGVtYSBrZXkgZm9yIHRoZSBzZXR0aW5nIGVkaXRvclxuICAgKiBpY29uIGxhYmVsIG9mIGEgcGx1Z2luLlxuICAgKi9cbiAgY29uc3QgSUNPTl9MQUJFTF9LRVkgPSAnanVweXRlci5sYWIuc2V0dGluZy1pY29uLWxhYmVsJztcblxuICAvKipcbiAgICogQ2hlY2sgdGhlIHBsdWdpbiBmb3IgYSByZW5kZXJpbmcgaGludCdzIHZhbHVlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBvcmRlciBvZiBwcmlvcml0eSBmb3Igb3ZlcnJpZGRlbiBoaW50cyBpcyBhcyBmb2xsb3dzLCBmcm9tIG1vc3RcbiAgICogaW1wb3J0YW50IHRvIGxlYXN0OlxuICAgKiAxLiBEYXRhIHNldCBieSB0aGUgZW5kIHVzZXIgaW4gYSBzZXR0aW5ncyBmaWxlLlxuICAgKiAyLiBEYXRhIHNldCBieSB0aGUgcGx1Z2luIGF1dGhvciBhcyBhIHNjaGVtYSBkZWZhdWx0LlxuICAgKiAzLiBEYXRhIHNldCBieSB0aGUgcGx1Z2luIGF1dGhvciBhcyBhIHRvcC1sZXZlbCBrZXkgb2YgdGhlIHNjaGVtYS5cbiAgICovXG4gIGZ1bmN0aW9uIGdldEhpbnQoXG4gICAga2V5OiBzdHJpbmcsXG4gICAgcmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgcGx1Z2luOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW5cbiAgKTogc3RyaW5nIHtcbiAgICAvLyBGaXJzdCwgZ2l2ZSBwcmlvcml0eSB0byBjaGVja2luZyBpZiB0aGUgaGludCBleGlzdHMgaW4gdGhlIHVzZXIgZGF0YS5cbiAgICBsZXQgaGludCA9IHBsdWdpbi5kYXRhLnVzZXJba2V5XTtcblxuICAgIC8vIFNlY29uZCwgY2hlY2sgdG8gc2VlIGlmIHRoZSBoaW50IGV4aXN0cyBpbiBjb21wb3NpdGUgZGF0YSwgd2hpY2ggZm9sZHNcbiAgICAvLyBpbiBkZWZhdWx0IHZhbHVlcyBmcm9tIHRoZSBzY2hlbWEuXG4gICAgaWYgKCFoaW50KSB7XG4gICAgICBoaW50ID0gcGx1Z2luLmRhdGEuY29tcG9zaXRlW2tleV07XG4gICAgfVxuXG4gICAgLy8gVGhpcmQsIGNoZWNrIHRvIHNlZSBpZiB0aGUgcGx1Z2luIHNjaGVtYSBoYXMgZGVmaW5lZCB0aGUgaGludC5cbiAgICBpZiAoIWhpbnQpIHtcbiAgICAgIGhpbnQgPSBwbHVnaW4uc2NoZW1hW2tleV07XG4gICAgfVxuXG4gICAgLy8gRmluYWxseSwgdXNlIHRoZSBkZWZhdWx0cyBmcm9tIHRoZSByZWdpc3RyeSBzY2hlbWEuXG4gICAgaWYgKCFoaW50KSB7XG4gICAgICBjb25zdCB7IHByb3BlcnRpZXMgfSA9IHJlZ2lzdHJ5LnNjaGVtYTtcblxuICAgICAgaGludCA9IHByb3BlcnRpZXMgJiYgcHJvcGVydGllc1trZXldICYmIHByb3BlcnRpZXNba2V5XS5kZWZhdWx0O1xuICAgIH1cblxuICAgIHJldHVybiB0eXBlb2YgaGludCA9PT0gJ3N0cmluZycgPyBoaW50IDogJyc7XG4gIH1cblxuICAvKipcbiAgICogUG9wdWxhdGUgdGhlIHBsdWdpbiBsaXN0LlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHBvcHVsYXRlTGlzdChcbiAgICByZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICBzZWxlY3Rpb246IHN0cmluZyxcbiAgICBub2RlOiBIVE1MRWxlbWVudCxcbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3JcbiAgKTogdm9pZCB7XG4gICAgdHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBwbHVnaW5zID0gc29ydFBsdWdpbnMocmVnaXN0cnkpLmZpbHRlcihwbHVnaW4gPT4ge1xuICAgICAgY29uc3QgeyBzY2hlbWEgfSA9IHBsdWdpbjtcbiAgICAgIGNvbnN0IGRlcHJlY2F0ZWQgPSBzY2hlbWFbJ2p1cHl0ZXIubGFiLnNldHRpbmctZGVwcmVjYXRlZCddID09PSB0cnVlO1xuICAgICAgY29uc3QgZWRpdGFibGUgPSBPYmplY3Qua2V5cyhzY2hlbWEucHJvcGVydGllcyB8fCB7fSkubGVuZ3RoID4gMDtcbiAgICAgIGNvbnN0IGV4dGVuc2libGUgPSBzY2hlbWEuYWRkaXRpb25hbFByb3BlcnRpZXMgIT09IGZhbHNlO1xuXG4gICAgICByZXR1cm4gIWRlcHJlY2F0ZWQgJiYgKGVkaXRhYmxlIHx8IGV4dGVuc2libGUpO1xuICAgIH0pO1xuICAgIGNvbnN0IGl0ZW1zID0gcGx1Z2lucy5tYXAocGx1Z2luID0+IHtcbiAgICAgIGNvbnN0IHsgaWQsIHNjaGVtYSwgdmVyc2lvbiB9ID0gcGx1Z2luO1xuICAgICAgY29uc3QgdGl0bGUgPVxuICAgICAgICB0eXBlb2Ygc2NoZW1hLnRpdGxlID09PSAnc3RyaW5nJ1xuICAgICAgICAgID8gdHJhbnMuX3AoJ3NjaGVtYScsIHNjaGVtYS50aXRsZSlcbiAgICAgICAgICA6IGlkO1xuICAgICAgY29uc3QgZGVzY3JpcHRpb24gPVxuICAgICAgICB0eXBlb2Ygc2NoZW1hLmRlc2NyaXB0aW9uID09PSAnc3RyaW5nJ1xuICAgICAgICAgID8gdHJhbnMuX3AoJ3NjaGVtYScsIHNjaGVtYS5kZXNjcmlwdGlvbilcbiAgICAgICAgICA6ICcnO1xuICAgICAgY29uc3QgaXRlbVRpdGxlID0gYCR7ZGVzY3JpcHRpb259XFxuJHtpZH1cXG4ke3ZlcnNpb259YDtcbiAgICAgIGNvbnN0IGljb24gPSBnZXRIaW50KElDT05fS0VZLCByZWdpc3RyeSwgcGx1Z2luKTtcbiAgICAgIGNvbnN0IGljb25DbGFzcyA9IGdldEhpbnQoSUNPTl9DTEFTU19LRVksIHJlZ2lzdHJ5LCBwbHVnaW4pO1xuICAgICAgY29uc3QgaWNvblRpdGxlID0gZ2V0SGludChJQ09OX0xBQkVMX0tFWSwgcmVnaXN0cnksIHBsdWdpbik7XG5cbiAgICAgIHJldHVybiAoXG4gICAgICAgIDxsaVxuICAgICAgICAgIGNsYXNzTmFtZT17aWQgPT09IHNlbGVjdGlvbiA/ICdqcC1tb2Qtc2VsZWN0ZWQnIDogJyd9XG4gICAgICAgICAgZGF0YS1pZD17aWR9XG4gICAgICAgICAga2V5PXtpZH1cbiAgICAgICAgICB0aXRsZT17aXRlbVRpdGxlfVxuICAgICAgICA+XG4gICAgICAgICAgPExhYkljb24ucmVzb2x2ZVJlYWN0XG4gICAgICAgICAgICBpY29uPXtpY29uIHx8IChpY29uQ2xhc3MgPyB1bmRlZmluZWQgOiBzZXR0aW5nc0ljb24pfVxuICAgICAgICAgICAgaWNvbkNsYXNzPXtjbGFzc2VzKGljb25DbGFzcywgJ2pwLUljb24nKX1cbiAgICAgICAgICAgIHRpdGxlPXtpY29uVGl0bGV9XG4gICAgICAgICAgICB0YWc9XCJzcGFuXCJcbiAgICAgICAgICAgIHN0eWxlc2hlZXQ9XCJzZXR0aW5nc0VkaXRvclwiXG4gICAgICAgICAgLz5cbiAgICAgICAgICA8c3Bhbj57dGl0bGV9PC9zcGFuPlxuICAgICAgICA8L2xpPlxuICAgICAgKTtcbiAgICB9KTtcblxuICAgIFJlYWN0RE9NLnVubW91bnRDb21wb25lbnRBdE5vZGUobm9kZSk7XG4gICAgUmVhY3RET00ucmVuZGVyKDx1bD57aXRlbXN9PC91bD4sIG5vZGUpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNvcnQgYSBsaXN0IG9mIHBsdWdpbnMgYnkgdGl0bGUgYW5kIElELlxuICAgKi9cbiAgZnVuY3Rpb24gc29ydFBsdWdpbnMocmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkpOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW5bXSB7XG4gICAgcmV0dXJuIE9iamVjdC5rZXlzKHJlZ2lzdHJ5LnBsdWdpbnMpXG4gICAgICAubWFwKHBsdWdpbiA9PiByZWdpc3RyeS5wbHVnaW5zW3BsdWdpbl0hKVxuICAgICAgLnNvcnQoKGEsIGIpID0+IHtcbiAgICAgICAgcmV0dXJuIChhLnNjaGVtYS50aXRsZSB8fCBhLmlkKS5sb2NhbGVDb21wYXJlKGIuc2NoZW1hLnRpdGxlIHx8IGIuaWQpO1xuICAgICAgfSk7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgQ29tbWFuZFRvb2xiYXJCdXR0b24sIFRvb2xiYXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBDb2RlRWRpdG9yLCBDb2RlRWRpdG9yV3JhcHBlciB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0IHsgSVJlbmRlck1pbWVSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBDb21tYW5kUmVnaXN0cnkgfSBmcm9tICdAbHVtaW5vL2NvbW1hbmRzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBCb3hMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBjcmVhdGVJbnNwZWN0b3IgfSBmcm9tICcuL2luc3BlY3Rvcic7XG5pbXBvcnQgeyBTcGxpdFBhbmVsIH0gZnJvbSAnLi9zcGxpdHBhbmVsJztcblxuLyoqXG4gKiBBIGNsYXNzIG5hbWUgYWRkZWQgdG8gYWxsIHJhdyBlZGl0b3JzLlxuICovXG5jb25zdCBSQVdfRURJVE9SX0NMQVNTID0gJ2pwLVNldHRpbmdzUmF3RWRpdG9yJztcblxuLyoqXG4gKiBBIGNsYXNzIG5hbWUgYWRkZWQgdG8gdGhlIHVzZXIgc2V0dGluZ3MgZWRpdG9yLlxuICovXG5jb25zdCBVU0VSX0NMQVNTID0gJ2pwLVNldHRpbmdzUmF3RWRpdG9yLXVzZXInO1xuXG4vKipcbiAqIEEgY2xhc3MgbmFtZSBhZGRlZCB0byB0aGUgdXNlciBlZGl0b3Igd2hlbiB0aGVyZSBhcmUgdmFsaWRhdGlvbiBlcnJvcnMuXG4gKi9cbmNvbnN0IEVSUk9SX0NMQVNTID0gJ2pwLW1vZC1lcnJvcic7XG5cbi8qKlxuICogQSByYXcgSlNPTiBzZXR0aW5ncyBlZGl0b3IuXG4gKi9cbmV4cG9ydCBjbGFzcyBSYXdFZGl0b3IgZXh0ZW5kcyBTcGxpdFBhbmVsIHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBwbHVnaW4gZWRpdG9yLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogUmF3RWRpdG9yLklPcHRpb25zKSB7XG4gICAgc3VwZXIoe1xuICAgICAgb3JpZW50YXRpb246ICdob3Jpem9udGFsJyxcbiAgICAgIHJlbmRlcmVyOiBTcGxpdFBhbmVsLmRlZmF1bHRSZW5kZXJlcixcbiAgICAgIHNwYWNpbmc6IDFcbiAgICB9KTtcblxuICAgIGNvbnN0IHsgY29tbWFuZHMsIGVkaXRvckZhY3RvcnksIHJlZ2lzdHJ5LCB0cmFuc2xhdG9yIH0gPSBvcHRpb25zO1xuICAgIHRoaXMucmVnaXN0cnkgPSByZWdpc3RyeTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX2NvbW1hbmRzID0gY29tbWFuZHM7XG5cbiAgICAvLyBDcmVhdGUgcmVhZC1vbmx5IGRlZmF1bHRzIGVkaXRvci5cbiAgICBjb25zdCBkZWZhdWx0cyA9ICh0aGlzLl9kZWZhdWx0cyA9IG5ldyBDb2RlRWRpdG9yV3JhcHBlcih7XG4gICAgICBtb2RlbDogbmV3IENvZGVFZGl0b3IuTW9kZWwoKSxcbiAgICAgIGZhY3Rvcnk6IGVkaXRvckZhY3RvcnlcbiAgICB9KSk7XG5cbiAgICBkZWZhdWx0cy5lZGl0b3IubW9kZWwudmFsdWUudGV4dCA9ICcnO1xuICAgIGRlZmF1bHRzLmVkaXRvci5tb2RlbC5taW1lVHlwZSA9ICd0ZXh0L2phdmFzY3JpcHQnO1xuICAgIGRlZmF1bHRzLmVkaXRvci5zZXRPcHRpb24oJ3JlYWRPbmx5JywgdHJ1ZSk7XG5cbiAgICAvLyBDcmVhdGUgcmVhZC13cml0ZSB1c2VyIHNldHRpbmdzIGVkaXRvci5cbiAgICBjb25zdCB1c2VyID0gKHRoaXMuX3VzZXIgPSBuZXcgQ29kZUVkaXRvcldyYXBwZXIoe1xuICAgICAgbW9kZWw6IG5ldyBDb2RlRWRpdG9yLk1vZGVsKCksXG4gICAgICBmYWN0b3J5OiBlZGl0b3JGYWN0b3J5LFxuICAgICAgY29uZmlnOiB7IGxpbmVOdW1iZXJzOiB0cnVlIH1cbiAgICB9KSk7XG5cbiAgICB1c2VyLmFkZENsYXNzKFVTRVJfQ0xBU1MpO1xuICAgIHVzZXIuZWRpdG9yLm1vZGVsLm1pbWVUeXBlID0gJ3RleHQvamF2YXNjcmlwdCc7XG4gICAgdXNlci5lZGl0b3IubW9kZWwudmFsdWUuY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uVGV4dENoYW5nZWQsIHRoaXMpO1xuXG4gICAgLy8gQ3JlYXRlIGFuZCBzZXQgdXAgYW4gaW5zcGVjdG9yLlxuICAgIHRoaXMuX2luc3BlY3RvciA9IGNyZWF0ZUluc3BlY3RvcihcbiAgICAgIHRoaXMsXG4gICAgICBvcHRpb25zLnJlbmRlcm1pbWUsXG4gICAgICB0aGlzLnRyYW5zbGF0b3JcbiAgICApO1xuXG4gICAgdGhpcy5hZGRDbGFzcyhSQVdfRURJVE9SX0NMQVNTKTtcbiAgICAvLyBGSVhNRS1UUkFOUzogb25TYXZlRXJyb3IgbXVzdCBoYXZlIGFuIG9wdGlvbmFsIHRyYW5zbGF0b3I/XG4gICAgdGhpcy5fb25TYXZlRXJyb3IgPSBvcHRpb25zLm9uU2F2ZUVycm9yO1xuICAgIHRoaXMuYWRkV2lkZ2V0KFByaXZhdGUuZGVmYXVsdHNFZGl0b3IoZGVmYXVsdHMsIHRoaXMudHJhbnNsYXRvcikpO1xuICAgIHRoaXMuYWRkV2lkZ2V0KFxuICAgICAgUHJpdmF0ZS51c2VyRWRpdG9yKHVzZXIsIHRoaXMuX3Rvb2xiYXIsIHRoaXMuX2luc3BlY3RvciwgdGhpcy50cmFuc2xhdG9yKVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNldHRpbmcgcmVnaXN0cnkgdXNlZCBieSB0aGUgZWRpdG9yLlxuICAgKi9cbiAgcmVhZG9ubHkgcmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnk7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIHJhdyBlZGl0b3IgcmV2ZXJ0IGZ1bmN0aW9uYWxpdHkgaXMgZW5hYmxlZC5cbiAgICovXG4gIGdldCBjYW5SZXZlcnQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2NhblJldmVydDtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSByYXcgZWRpdG9yIHNhdmUgZnVuY3Rpb25hbGl0eSBpcyBlbmFibGVkLlxuICAgKi9cbiAgZ2V0IGNhblNhdmUoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2NhblNhdmU7XG4gIH1cblxuICAvKipcbiAgICogRW1pdHMgd2hlbiB0aGUgY29tbWFuZHMgcGFzc2VkIGluIGF0IGluc3RhbnRpYXRpb24gY2hhbmdlLlxuICAgKi9cbiAgZ2V0IGNvbW1hbmRzQ2hhbmdlZCgpOiBJU2lnbmFsPGFueSwgc3RyaW5nW10+IHtcbiAgICByZXR1cm4gdGhpcy5fY29tbWFuZHNDaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRlc3RzIHdoZXRoZXIgdGhlIHNldHRpbmdzIGhhdmUgYmVlbiBtb2RpZmllZCBhbmQgbmVlZCBzYXZpbmcuXG4gICAqL1xuICBnZXQgaXNEaXJ0eSgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fdXNlci5lZGl0b3IubW9kZWwudmFsdWUudGV4dCAhPT0gdGhpcy5fc2V0dGluZ3M/LnJhdyA/PyAnJztcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgcGx1Z2luIHNldHRpbmdzIGJlaW5nIGVkaXRlZC5cbiAgICovXG4gIGdldCBzZXR0aW5ncygpOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyB8IG51bGwge1xuICAgIHJldHVybiB0aGlzLl9zZXR0aW5ncztcbiAgfVxuICBzZXQgc2V0dGluZ3Moc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzIHwgbnVsbCkge1xuICAgIGlmICghc2V0dGluZ3MgJiYgIXRoaXMuX3NldHRpbmdzKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3Qgc2FtZVBsdWdpbiA9XG4gICAgICBzZXR0aW5ncyAmJiB0aGlzLl9zZXR0aW5ncyAmJiBzZXR0aW5ncy5wbHVnaW4gPT09IHRoaXMuX3NldHRpbmdzLnBsdWdpbjtcblxuICAgIGlmIChzYW1lUGx1Z2luKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3QgZGVmYXVsdHMgPSB0aGlzLl9kZWZhdWx0cztcbiAgICBjb25zdCB1c2VyID0gdGhpcy5fdXNlcjtcblxuICAgIC8vIERpc2Nvbm5lY3Qgb2xkIHNldHRpbmdzIGNoYW5nZSBoYW5kbGVyLlxuICAgIGlmICh0aGlzLl9zZXR0aW5ncykge1xuICAgICAgdGhpcy5fc2V0dGluZ3MuY2hhbmdlZC5kaXNjb25uZWN0KHRoaXMuX29uU2V0dGluZ3NDaGFuZ2VkLCB0aGlzKTtcbiAgICB9XG5cbiAgICBpZiAoc2V0dGluZ3MpIHtcbiAgICAgIHRoaXMuX3NldHRpbmdzID0gc2V0dGluZ3M7XG4gICAgICB0aGlzLl9zZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25TZXR0aW5nc0NoYW5nZWQsIHRoaXMpO1xuICAgICAgdGhpcy5fb25TZXR0aW5nc0NoYW5nZWQoKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5fc2V0dGluZ3MgPSBudWxsO1xuICAgICAgZGVmYXVsdHMuZWRpdG9yLm1vZGVsLnZhbHVlLnRleHQgPSAnJztcbiAgICAgIHVzZXIuZWRpdG9yLm1vZGVsLnZhbHVlLnRleHQgPSAnJztcbiAgICB9XG5cbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgcmVsYXRpdmUgc2l6ZXMgb2YgdGhlIHR3byBlZGl0b3IgcGFuZWxzLlxuICAgKi9cbiAgZ2V0IHNpemVzKCk6IG51bWJlcltdIHtcbiAgICByZXR1cm4gdGhpcy5yZWxhdGl2ZVNpemVzKCk7XG4gIH1cbiAgc2V0IHNpemVzKHNpemVzOiBudW1iZXJbXSkge1xuICAgIHRoaXMuc2V0UmVsYXRpdmVTaXplcyhzaXplcyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGluc3BlY3RhYmxlIHNvdXJjZSBlZGl0b3IgZm9yIHVzZXIgaW5wdXQuXG4gICAqL1xuICBnZXQgc291cmNlKCk6IENvZGVFZGl0b3IuSUVkaXRvciB7XG4gICAgcmV0dXJuIHRoaXMuX3VzZXIuZWRpdG9yO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSByYXcgZWRpdG9yLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICAgIHRoaXMuX2RlZmF1bHRzLmRpc3Bvc2UoKTtcbiAgICB0aGlzLl91c2VyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXZlcnQgdGhlIGVkaXRvciBiYWNrIHRvIG9yaWdpbmFsIHNldHRpbmdzLlxuICAgKi9cbiAgcmV2ZXJ0KCk6IHZvaWQge1xuICAgIHRoaXMuX3VzZXIuZWRpdG9yLm1vZGVsLnZhbHVlLnRleHQgPSB0aGlzLnNldHRpbmdzPy5yYXcgPz8gJyc7XG4gICAgdGhpcy5fdXBkYXRlVG9vbGJhcihmYWxzZSwgZmFsc2UpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNhdmUgdGhlIGNvbnRlbnRzIG9mIHRoZSByYXcgZWRpdG9yLlxuICAgKi9cbiAgc2F2ZSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBpZiAoIXRoaXMuaXNEaXJ0eSB8fCAhdGhpcy5fc2V0dGluZ3MpIHtcbiAgICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUodW5kZWZpbmVkKTtcbiAgICB9XG5cbiAgICBjb25zdCBzZXR0aW5ncyA9IHRoaXMuX3NldHRpbmdzO1xuICAgIGNvbnN0IHNvdXJjZSA9IHRoaXMuX3VzZXIuZWRpdG9yLm1vZGVsLnZhbHVlLnRleHQ7XG5cbiAgICByZXR1cm4gc2V0dGluZ3NcbiAgICAgIC5zYXZlKHNvdXJjZSlcbiAgICAgIC50aGVuKCgpID0+IHtcbiAgICAgICAgdGhpcy5fdXBkYXRlVG9vbGJhcihmYWxzZSwgZmFsc2UpO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICB0aGlzLl91cGRhdGVUb29sYmFyKHRydWUsIGZhbHNlKTtcbiAgICAgICAgdGhpcy5fb25TYXZlRXJyb3IocmVhc29uLCB0aGlzLnRyYW5zbGF0b3IpO1xuICAgICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBhZnRlci1hdHRhY2hgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgUHJpdmF0ZS5wb3B1bGF0ZVRvb2xiYXIodGhpcy5fY29tbWFuZHMsIHRoaXMuX3Rvb2xiYXIpO1xuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAndXBkYXRlLXJlcXVlc3QnYCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvblVwZGF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgY29uc3Qgc2V0dGluZ3MgPSB0aGlzLl9zZXR0aW5ncztcbiAgICBjb25zdCBkZWZhdWx0cyA9IHRoaXMuX2RlZmF1bHRzO1xuICAgIGNvbnN0IHVzZXIgPSB0aGlzLl91c2VyO1xuXG4gICAgaWYgKHNldHRpbmdzKSB7XG4gICAgICBkZWZhdWx0cy5lZGl0b3IucmVmcmVzaCgpO1xuICAgICAgdXNlci5lZGl0b3IucmVmcmVzaCgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGV4dCBjaGFuZ2VzIGluIHRoZSB1bmRlcmx5aW5nIGVkaXRvci5cbiAgICovXG4gIHByaXZhdGUgX29uVGV4dENoYW5nZWQoKTogdm9pZCB7XG4gICAgY29uc3QgcmF3ID0gdGhpcy5fdXNlci5lZGl0b3IubW9kZWwudmFsdWUudGV4dDtcbiAgICBjb25zdCBzZXR0aW5ncyA9IHRoaXMuX3NldHRpbmdzO1xuXG4gICAgdGhpcy5yZW1vdmVDbGFzcyhFUlJPUl9DTEFTUyk7XG5cbiAgICAvLyBJZiB0aGVyZSBhcmUgbm8gc2V0dGluZ3MgbG9hZGVkIG9yIHRoZXJlIGFyZSBubyBjaGFuZ2VzLCBiYWlsLlxuICAgIGlmICghc2V0dGluZ3MgfHwgc2V0dGluZ3MucmF3ID09PSByYXcpIHtcbiAgICAgIHRoaXMuX3VwZGF0ZVRvb2xiYXIoZmFsc2UsIGZhbHNlKTtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCBlcnJvcnMgPSBzZXR0aW5ncy52YWxpZGF0ZShyYXcpO1xuXG4gICAgaWYgKGVycm9ycykge1xuICAgICAgdGhpcy5hZGRDbGFzcyhFUlJPUl9DTEFTUyk7XG4gICAgICB0aGlzLl91cGRhdGVUb29sYmFyKHRydWUsIGZhbHNlKTtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLl91cGRhdGVUb29sYmFyKHRydWUsIHRydWUpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB1cGRhdGVzIHRvIHRoZSBzZXR0aW5ncy5cbiAgICovXG4gIHByaXZhdGUgX29uU2V0dGluZ3NDaGFuZ2VkKCk6IHZvaWQge1xuICAgIGNvbnN0IHNldHRpbmdzID0gdGhpcy5fc2V0dGluZ3M7XG4gICAgY29uc3QgZGVmYXVsdHMgPSB0aGlzLl9kZWZhdWx0cztcbiAgICBjb25zdCB1c2VyID0gdGhpcy5fdXNlcjtcblxuICAgIGRlZmF1bHRzLmVkaXRvci5tb2RlbC52YWx1ZS50ZXh0ID0gc2V0dGluZ3M/LmFubm90YXRlZERlZmF1bHRzKCkgPz8gJyc7XG4gICAgdXNlci5lZGl0b3IubW9kZWwudmFsdWUudGV4dCA9IHNldHRpbmdzPy5yYXcgPz8gJyc7XG4gIH1cblxuICBwcml2YXRlIF91cGRhdGVUb29sYmFyKHJldmVydCA9IHRoaXMuX2NhblJldmVydCwgc2F2ZSA9IHRoaXMuX2NhblNhdmUpOiB2b2lkIHtcbiAgICBjb25zdCBjb21tYW5kcyA9IHRoaXMuX2NvbW1hbmRzO1xuXG4gICAgdGhpcy5fY2FuUmV2ZXJ0ID0gcmV2ZXJ0O1xuICAgIHRoaXMuX2NhblNhdmUgPSBzYXZlO1xuICAgIHRoaXMuX2NvbW1hbmRzQ2hhbmdlZC5lbWl0KFtjb21tYW5kcy5yZXZlcnQsIGNvbW1hbmRzLnNhdmVdKTtcbiAgfVxuXG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfY2FuUmV2ZXJ0ID0gZmFsc2U7XG4gIHByaXZhdGUgX2NhblNhdmUgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfY29tbWFuZHM6IFJhd0VkaXRvci5JQ29tbWFuZEJ1bmRsZTtcbiAgcHJpdmF0ZSBfY29tbWFuZHNDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBzdHJpbmdbXT4odGhpcyk7XG4gIHByaXZhdGUgX2RlZmF1bHRzOiBDb2RlRWRpdG9yV3JhcHBlcjtcbiAgcHJpdmF0ZSBfaW5zcGVjdG9yOiBXaWRnZXQ7XG4gIHByaXZhdGUgX29uU2F2ZUVycm9yOiAocmVhc29uOiBhbnksIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcikgPT4gdm9pZDtcbiAgcHJpdmF0ZSBfc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX3Rvb2xiYXIgPSBuZXcgVG9vbGJhcjxXaWRnZXQ+KCk7XG4gIHByaXZhdGUgX3VzZXI6IENvZGVFZGl0b3JXcmFwcGVyO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgUmF3RWRpdG9yYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFJhd0VkaXRvciB7XG4gIC8qKlxuICAgKiBUaGUgdG9vbGJhciBjb21tYW5kcyBhbmQgcmVnaXN0cnkgZm9yIHRoZSBzZXR0aW5nIGVkaXRvciB0b29sYmFyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29tbWFuZEJ1bmRsZSB7XG4gICAgLyoqXG4gICAgICogVGhlIGNvbW1hbmQgcmVnaXN0cnkuXG4gICAgICovXG4gICAgcmVnaXN0cnk6IENvbW1hbmRSZWdpc3RyeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSByZXZlcnQgY29tbWFuZCBJRC5cbiAgICAgKi9cbiAgICByZXZlcnQ6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBzYXZlIGNvbW1hbmQgSUQuXG4gICAgICovXG4gICAgc2F2ZTogc3RyaW5nO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgcmF3IGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSB0b29sYmFyIGNvbW1hbmRzIGFuZCByZWdpc3RyeSBmb3IgdGhlIHNldHRpbmcgZWRpdG9yIHRvb2xiYXIuXG4gICAgICovXG4gICAgY29tbWFuZHM6IElDb21tYW5kQnVuZGxlO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGVkaXRvciBmYWN0b3J5IHVzZWQgYnkgdGhlIHJhdyBlZGl0b3IuXG4gICAgICovXG4gICAgZWRpdG9yRmFjdG9yeTogQ29kZUVkaXRvci5GYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0aGUgcmF3IGVkaXRvciBjYWxscyBvbiBzYXZlIGVycm9ycy5cbiAgICAgKi9cbiAgICBvblNhdmVFcnJvcjogKHJlYXNvbjogYW55KSA9PiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHNldHRpbmcgcmVnaXN0cnkgdXNlZCBieSB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIG9wdGlvbmFsIE1JTUUgcmVuZGVyZXIgdG8gdXNlIGZvciByZW5kZXJpbmcgZGVidWcgbWVzc2FnZXMuXG4gICAgICovXG4gICAgcmVuZGVybWltZT86IElSZW5kZXJNaW1lUmVnaXN0cnk7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBtb2R1bGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogUmV0dXJucyB0aGUgd3JhcHBlZCBzZXR0aW5nIGRlZmF1bHRzIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBkZWZhdWx0c0VkaXRvcihcbiAgICBlZGl0b3I6IFdpZGdldCxcbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3JcbiAgKTogV2lkZ2V0IHtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHdpZGdldCA9IG5ldyBXaWRnZXQoKTtcbiAgICBjb25zdCBsYXlvdXQgPSAod2lkZ2V0LmxheW91dCA9IG5ldyBCb3hMYXlvdXQoeyBzcGFjaW5nOiAwIH0pKTtcbiAgICBjb25zdCBiYW5uZXIgPSBuZXcgV2lkZ2V0KCk7XG4gICAgY29uc3QgYmFyID0gbmV3IFRvb2xiYXIoKTtcbiAgICBjb25zdCBkZWZhdWx0VGl0bGUgPSB0cmFucy5fXygnU3lzdGVtIERlZmF1bHRzJyk7XG5cbiAgICBiYW5uZXIubm9kZS5pbm5lclRleHQgPSBkZWZhdWx0VGl0bGU7XG4gICAgYmFyLmluc2VydEl0ZW0oMCwgJ2Jhbm5lcicsIGJhbm5lcik7XG4gICAgbGF5b3V0LmFkZFdpZGdldChiYXIpO1xuICAgIGxheW91dC5hZGRXaWRnZXQoZWRpdG9yKTtcblxuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cblxuICAvKipcbiAgICogUG9wdWxhdGUgdGhlIHJhdyBlZGl0b3IgdG9vbGJhci5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBwb3B1bGF0ZVRvb2xiYXIoXG4gICAgY29tbWFuZHM6IFJhd0VkaXRvci5JQ29tbWFuZEJ1bmRsZSxcbiAgICB0b29sYmFyOiBUb29sYmFyPFdpZGdldD5cbiAgKTogdm9pZCB7XG4gICAgY29uc3QgeyByZWdpc3RyeSwgcmV2ZXJ0LCBzYXZlIH0gPSBjb21tYW5kcztcblxuICAgIHRvb2xiYXIuYWRkSXRlbSgnc3BhY2VyJywgVG9vbGJhci5jcmVhdGVTcGFjZXJJdGVtKCkpO1xuXG4gICAgLy8gTm90ZSB0aGUgYnV0dG9uIG9yZGVyLiBUaGUgcmF0aW9uYWxlIGhlcmUgaXMgdGhhdCBubyBtYXR0ZXIgd2hhdCBzdGF0ZVxuICAgIC8vIHRoZSB0b29sYmFyIGlzIGluLCB0aGUgcmVsYXRpdmUgbG9jYXRpb24gb2YgdGhlIHJldmVydCBidXR0b24gaW4gdGhlXG4gICAgLy8gdG9vbGJhciByZW1haW5zIHRoZSBzYW1lLlxuICAgIFtyZXZlcnQsIHNhdmVdLmZvckVhY2gobmFtZSA9PiB7XG4gICAgICBjb25zdCBpdGVtID0gbmV3IENvbW1hbmRUb29sYmFyQnV0dG9uKHsgY29tbWFuZHM6IHJlZ2lzdHJ5LCBpZDogbmFtZSB9KTtcbiAgICAgIHRvb2xiYXIuYWRkSXRlbShuYW1lLCBpdGVtKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm5zIHRoZSB3cmFwcGVkIHVzZXIgb3ZlcnJpZGVzIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiB1c2VyRWRpdG9yKFxuICAgIGVkaXRvcjogV2lkZ2V0LFxuICAgIHRvb2xiYXI6IFRvb2xiYXI8V2lkZ2V0PixcbiAgICBpbnNwZWN0b3I6IFdpZGdldCxcbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3JcbiAgKTogV2lkZ2V0IHtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHVzZXJUaXRsZSA9IHRyYW5zLl9fKCdVc2VyIFByZWZlcmVuY2VzJyk7XG4gICAgY29uc3Qgd2lkZ2V0ID0gbmV3IFdpZGdldCgpO1xuICAgIGNvbnN0IGxheW91dCA9ICh3aWRnZXQubGF5b3V0ID0gbmV3IEJveExheW91dCh7IHNwYWNpbmc6IDAgfSkpO1xuICAgIGNvbnN0IGJhbm5lciA9IG5ldyBXaWRnZXQoKTtcblxuICAgIGJhbm5lci5ub2RlLmlubmVyVGV4dCA9IHVzZXJUaXRsZTtcbiAgICB0b29sYmFyLmluc2VydEl0ZW0oMCwgJ2Jhbm5lcicsIGJhbm5lcik7XG4gICAgbGF5b3V0LmFkZFdpZGdldCh0b29sYmFyKTtcbiAgICBsYXlvdXQuYWRkV2lkZ2V0KGVkaXRvcik7XG4gICAgbGF5b3V0LmFkZFdpZGdldChpbnNwZWN0b3IpO1xuXG4gICAgcmV0dXJuIHdpZGdldDtcbiAgfVxufVxuIiwiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG5cbmltcG9ydCB7IENvZGVFZGl0b3IgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlZWRpdG9yJztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVN0YXRlREIgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IGp1cHl0ZXJJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBDb21tYW5kUmVnaXN0cnkgfSBmcm9tICdAbHVtaW5vL2NvbW1hbmRzJztcbmltcG9ydCB7IEpTT05FeHQsIEpTT05PYmplY3QsIEpTT05WYWx1ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBJU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgUGFuZWxMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgKiBhcyBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IHsgUGx1Z2luRWRpdG9yIH0gZnJvbSAnLi9wbHVnaW5lZGl0b3InO1xuaW1wb3J0IHsgUGx1Z2luTGlzdCB9IGZyb20gJy4vcGx1Z2lubGlzdCc7XG5pbXBvcnQgeyBTcGxpdFBhbmVsIH0gZnJvbSAnLi9zcGxpdHBhbmVsJztcblxuLyoqXG4gKiBUaGUgcmF0aW8gcGFuZXMgaW4gdGhlIHNldHRpbmcgZWRpdG9yLlxuICovXG5jb25zdCBERUZBVUxUX0xBWU9VVDogU2V0dGluZ0VkaXRvci5JTGF5b3V0U3RhdGUgPSB7XG4gIHNpemVzOiBbMSwgM10sXG4gIGNvbnRhaW5lcjoge1xuICAgIGVkaXRvcjogJ3JhdycsXG4gICAgcGx1Z2luOiAnJyxcbiAgICBzaXplczogWzEsIDFdXG4gIH1cbn07XG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBtb2RpZnlpbmcgYW5kIHNhdmluZyBhcHBsaWNhdGlvbiBzZXR0aW5ncy5cbiAqL1xuZXhwb3J0IGNsYXNzIFNldHRpbmdFZGl0b3IgZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHNldHRpbmcgZWRpdG9yLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogU2V0dGluZ0VkaXRvci5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gb3B0aW9ucy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLVNldHRpbmdFZGl0b3InKTtcbiAgICB0aGlzLmtleSA9IG9wdGlvbnMua2V5O1xuICAgIHRoaXMuc3RhdGUgPSBvcHRpb25zLnN0YXRlO1xuXG4gICAgY29uc3QgeyBjb21tYW5kcywgZWRpdG9yRmFjdG9yeSwgcmVuZGVybWltZSB9ID0gb3B0aW9ucztcbiAgICBjb25zdCBsYXlvdXQgPSAodGhpcy5sYXlvdXQgPSBuZXcgUGFuZWxMYXlvdXQoKSk7XG4gICAgY29uc3QgcmVnaXN0cnkgPSAodGhpcy5yZWdpc3RyeSA9IG9wdGlvbnMucmVnaXN0cnkpO1xuICAgIGNvbnN0IHBhbmVsID0gKHRoaXMuX3BhbmVsID0gbmV3IFNwbGl0UGFuZWwoe1xuICAgICAgb3JpZW50YXRpb246ICdob3Jpem9udGFsJyxcbiAgICAgIHJlbmRlcmVyOiBTcGxpdFBhbmVsLmRlZmF1bHRSZW5kZXJlcixcbiAgICAgIHNwYWNpbmc6IDFcbiAgICB9KSk7XG4gICAgY29uc3QgaW5zdHJ1Y3Rpb25zID0gKHRoaXMuX2luc3RydWN0aW9ucyA9IG5ldyBXaWRnZXQoKSk7XG4gICAgY29uc3QgZWRpdG9yID0gKHRoaXMuX2VkaXRvciA9IG5ldyBQbHVnaW5FZGl0b3Ioe1xuICAgICAgY29tbWFuZHMsXG4gICAgICBlZGl0b3JGYWN0b3J5LFxuICAgICAgcmVnaXN0cnksXG4gICAgICByZW5kZXJtaW1lLFxuICAgICAgdHJhbnNsYXRvcjogdGhpcy50cmFuc2xhdG9yXG4gICAgfSkpO1xuICAgIGNvbnN0IGNvbmZpcm0gPSAoKSA9PiBlZGl0b3IuY29uZmlybSgpO1xuICAgIGNvbnN0IGxpc3QgPSAodGhpcy5fbGlzdCA9IG5ldyBQbHVnaW5MaXN0KHtcbiAgICAgIGNvbmZpcm0sXG4gICAgICByZWdpc3RyeSxcbiAgICAgIHRyYW5zbGF0b3I6IHRoaXMudHJhbnNsYXRvclxuICAgIH0pKTtcbiAgICBjb25zdCB3aGVuID0gb3B0aW9ucy53aGVuO1xuXG4gICAgaW5zdHJ1Y3Rpb25zLmFkZENsYXNzKCdqcC1TZXR0aW5nRWRpdG9ySW5zdHJ1Y3Rpb25zJyk7XG4gICAgUHJpdmF0ZS5wb3B1bGF0ZUluc3RydWN0aW9uc05vZGUoaW5zdHJ1Y3Rpb25zLm5vZGUsIHRoaXMudHJhbnNsYXRvcik7XG5cbiAgICBpZiAod2hlbikge1xuICAgICAgdGhpcy5fd2hlbiA9IEFycmF5LmlzQXJyYXkod2hlbikgPyBQcm9taXNlLmFsbCh3aGVuKSA6IHdoZW47XG4gICAgfVxuXG4gICAgcGFuZWwuYWRkQ2xhc3MoJ2pwLVNldHRpbmdFZGl0b3ItbWFpbicpO1xuICAgIGxheW91dC5hZGRXaWRnZXQocGFuZWwpO1xuICAgIHBhbmVsLmFkZFdpZGdldChsaXN0KTtcbiAgICBwYW5lbC5hZGRXaWRnZXQoaW5zdHJ1Y3Rpb25zKTtcblxuICAgIFNwbGl0UGFuZWwuc2V0U3RyZXRjaChsaXN0LCAwKTtcbiAgICBTcGxpdFBhbmVsLnNldFN0cmV0Y2goaW5zdHJ1Y3Rpb25zLCAxKTtcbiAgICBTcGxpdFBhbmVsLnNldFN0cmV0Y2goZWRpdG9yLCAxKTtcblxuICAgIGVkaXRvci5zdGF0ZUNoYW5nZWQuY29ubmVjdCh0aGlzLl9vblN0YXRlQ2hhbmdlZCwgdGhpcyk7XG4gICAgbGlzdC5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25TdGF0ZUNoYW5nZWQsIHRoaXMpO1xuICAgIHBhbmVsLmhhbmRsZU1vdmVkLmNvbm5lY3QodGhpcy5fb25TdGF0ZUNoYW5nZWQsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBzdGF0ZSBkYXRhYmFzZSBrZXkgZm9yIHRoZSBlZGl0b3IncyBzdGF0ZSBtYW5hZ2VtZW50LlxuICAgKi9cbiAgcmVhZG9ubHkga2V5OiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFRoZSBzZXR0aW5nIHJlZ2lzdHJ5IHVzZWQgYnkgdGhlIGVkaXRvci5cbiAgICovXG4gIHJlYWRvbmx5IHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5O1xuXG4gIC8qKlxuICAgKiBUaGUgc3RhdGUgZGF0YWJhc2UgdXNlZCB0byBzdG9yZSBsYXlvdXQuXG4gICAqL1xuICByZWFkb25seSBzdGF0ZTogSVN0YXRlREI7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIHJhdyBlZGl0b3IgcmV2ZXJ0IGZ1bmN0aW9uYWxpdHkgaXMgZW5hYmxlZC5cbiAgICovXG4gIGdldCBjYW5SZXZlcnRSYXcoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2VkaXRvci5yYXcuY2FuUmV2ZXJ0O1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIHJhdyBlZGl0b3Igc2F2ZSBmdW5jdGlvbmFsaXR5IGlzIGVuYWJsZWQuXG4gICAqL1xuICBnZXQgY2FuU2F2ZVJhdygpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fZWRpdG9yLnJhdy5jYW5TYXZlO1xuICB9XG5cbiAgLyoqXG4gICAqIEVtaXRzIHdoZW4gdGhlIGNvbW1hbmRzIHBhc3NlZCBpbiBhdCBpbnN0YW50aWF0aW9uIGNoYW5nZS5cbiAgICovXG4gIGdldCBjb21tYW5kc0NoYW5nZWQoKTogSVNpZ25hbDxhbnksIHN0cmluZ1tdPiB7XG4gICAgcmV0dXJuIHRoaXMuX2VkaXRvci5yYXcuY29tbWFuZHNDaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjdXJyZW50bHkgbG9hZGVkIHNldHRpbmdzLlxuICAgKi9cbiAgZ2V0IHNldHRpbmdzKCk6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzIHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuX2VkaXRvci5zZXR0aW5ncztcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgaW5zcGVjdGFibGUgcmF3IHVzZXIgZWRpdG9yIHNvdXJjZSBmb3IgdGhlIGN1cnJlbnRseSBsb2FkZWQgc2V0dGluZ3MuXG4gICAqL1xuICBnZXQgc291cmNlKCk6IENvZGVFZGl0b3IuSUVkaXRvciB7XG4gICAgcmV0dXJuIHRoaXMuX2VkaXRvci5yYXcuc291cmNlO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBzZXR0aW5nIGVkaXRvci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgICB0aGlzLl9lZGl0b3IuZGlzcG9zZSgpO1xuICAgIHRoaXMuX2luc3RydWN0aW9ucy5kaXNwb3NlKCk7XG4gICAgdGhpcy5fbGlzdC5kaXNwb3NlKCk7XG4gICAgdGhpcy5fcGFuZWwuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldmVydCByYXcgZWRpdG9yIGJhY2sgdG8gb3JpZ2luYWwgc2V0dGluZ3MuXG4gICAqL1xuICByZXZlcnQoKTogdm9pZCB7XG4gICAgdGhpcy5fZWRpdG9yLnJhdy5yZXZlcnQoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTYXZlIHRoZSBjb250ZW50cyBvZiB0aGUgcmF3IGVkaXRvci5cbiAgICovXG4gIHNhdmUoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX2VkaXRvci5yYXcuc2F2ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ2FmdGVyLWF0dGFjaCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgc3VwZXIub25BZnRlckF0dGFjaChtc2cpO1xuICAgIHRoaXMuX3BhbmVsLmhpZGUoKTtcbiAgICB0aGlzLl9mZXRjaFN0YXRlKClcbiAgICAgIC50aGVuKCgpID0+IHtcbiAgICAgICAgdGhpcy5fcGFuZWwuc2hvdygpO1xuICAgICAgICB0aGlzLl9zZXRTdGF0ZSgpO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICBjb25zb2xlLmVycm9yKCdGZXRjaGluZyBzZXR0aW5nIGVkaXRvciBzdGF0ZSBmYWlsZWQnLCByZWFzb24pO1xuICAgICAgICB0aGlzLl9wYW5lbC5zaG93KCk7XG4gICAgICAgIHRoaXMuX3NldFN0YXRlKCk7XG4gICAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdjbG9zZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25DbG9zZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fZWRpdG9yXG4gICAgICAuY29uZmlybSgpXG4gICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgIHN1cGVyLm9uQ2xvc2VSZXF1ZXN0KG1zZyk7XG4gICAgICAgIHRoaXMuZGlzcG9zZSgpO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaCgoKSA9PiB7XG4gICAgICAgIC8qIG5vIG9wICovXG4gICAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHN0YXRlIG9mIHRoZSBwYW5lbC5cbiAgICovXG4gIHByaXZhdGUgX2ZldGNoU3RhdGUoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgaWYgKHRoaXMuX2ZldGNoaW5nKSB7XG4gICAgICByZXR1cm4gdGhpcy5fZmV0Y2hpbmc7XG4gICAgfVxuXG4gICAgY29uc3QgeyBrZXksIHN0YXRlIH0gPSB0aGlzO1xuICAgIGNvbnN0IHByb21pc2VzID0gW3N0YXRlLmZldGNoKGtleSksIHRoaXMuX3doZW5dO1xuXG4gICAgcmV0dXJuICh0aGlzLl9mZXRjaGluZyA9IFByb21pc2UuYWxsKHByb21pc2VzKS50aGVuKChbdmFsdWVdKSA9PiB7XG4gICAgICB0aGlzLl9mZXRjaGluZyA9IG51bGw7XG5cbiAgICAgIGlmICh0aGlzLl9zYXZpbmcpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuXG4gICAgICB0aGlzLl9zdGF0ZSA9IFByaXZhdGUubm9ybWFsaXplU3RhdGUodmFsdWUsIHRoaXMuX3N0YXRlKTtcbiAgICB9KSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHJvb3QgbGV2ZWwgbGF5b3V0IHN0YXRlIGNoYW5nZXMuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9vblN0YXRlQ2hhbmdlZCgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICB0aGlzLl9zdGF0ZS5zaXplcyA9IHRoaXMuX3BhbmVsLnJlbGF0aXZlU2l6ZXMoKTtcbiAgICB0aGlzLl9zdGF0ZS5jb250YWluZXIgPSB0aGlzLl9lZGl0b3Iuc3RhdGU7XG4gICAgdGhpcy5fc3RhdGUuY29udGFpbmVyLnBsdWdpbiA9IHRoaXMuX2xpc3Quc2VsZWN0aW9uO1xuICAgIHRyeSB7XG4gICAgICBhd2FpdCB0aGlzLl9zYXZlU3RhdGUoKTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgY29uc29sZS5lcnJvcignU2F2aW5nIHNldHRpbmcgZWRpdG9yIHN0YXRlIGZhaWxlZCcsIGVycm9yKTtcbiAgICB9XG4gICAgdGhpcy5fc2V0U3RhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHN0YXRlIG9mIHRoZSBzZXR0aW5nIGVkaXRvci5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX3NhdmVTdGF0ZSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCB7IGtleSwgc3RhdGUgfSA9IHRoaXM7XG4gICAgY29uc3QgdmFsdWUgPSB0aGlzLl9zdGF0ZTtcblxuICAgIHRoaXMuX3NhdmluZyA9IHRydWU7XG4gICAgdHJ5IHtcbiAgICAgIGF3YWl0IHN0YXRlLnNhdmUoa2V5LCB2YWx1ZSk7XG4gICAgICB0aGlzLl9zYXZpbmcgPSBmYWxzZTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgdGhpcy5fc2F2aW5nID0gZmFsc2U7XG4gICAgICB0aHJvdyBlcnJvcjtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBsYXlvdXQgc2l6ZXMuXG4gICAqL1xuICBwcml2YXRlIF9zZXRMYXlvdXQoKTogdm9pZCB7XG4gICAgY29uc3QgZWRpdG9yID0gdGhpcy5fZWRpdG9yO1xuICAgIGNvbnN0IHBhbmVsID0gdGhpcy5fcGFuZWw7XG4gICAgY29uc3Qgc3RhdGUgPSB0aGlzLl9zdGF0ZTtcblxuICAgIGVkaXRvci5zdGF0ZSA9IHN0YXRlLmNvbnRhaW5lcjtcblxuICAgIC8vIEFsbG93IHRoZSBtZXNzYWdlIHF1ZXVlICh3aGljaCBpbmNsdWRlcyBmaXQgcmVxdWVzdHMgdGhhdCBtaWdodCBkaXNydXB0XG4gICAgLy8gc2V0dGluZyByZWxhdGl2ZSBzaXplcykgdG8gY2xlYXIgYmVmb3JlIHNldHRpbmcgc2l6ZXMuXG4gICAgcmVxdWVzdEFuaW1hdGlvbkZyYW1lKCgpID0+IHtcbiAgICAgIHBhbmVsLnNldFJlbGF0aXZlU2l6ZXMoc3RhdGUuc2l6ZXMpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgcHJlc2V0cyBvZiB0aGUgc2V0dGluZyBlZGl0b3IuXG4gICAqL1xuICBwcml2YXRlIF9zZXRTdGF0ZSgpOiB2b2lkIHtcbiAgICBjb25zdCBlZGl0b3IgPSB0aGlzLl9lZGl0b3I7XG4gICAgY29uc3QgbGlzdCA9IHRoaXMuX2xpc3Q7XG4gICAgY29uc3QgcGFuZWwgPSB0aGlzLl9wYW5lbDtcbiAgICBjb25zdCB7IGNvbnRhaW5lciB9ID0gdGhpcy5fc3RhdGU7XG5cbiAgICBpZiAoIWNvbnRhaW5lci5wbHVnaW4pIHtcbiAgICAgIGVkaXRvci5zZXR0aW5ncyA9IG51bGw7XG4gICAgICBsaXN0LnNlbGVjdGlvbiA9ICcnO1xuICAgICAgdGhpcy5fc2V0TGF5b3V0KCk7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgaWYgKGVkaXRvci5zZXR0aW5ncyAmJiBlZGl0b3Iuc2V0dGluZ3MuaWQgPT09IGNvbnRhaW5lci5wbHVnaW4pIHtcbiAgICAgIHRoaXMuX3NldExheW91dCgpO1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IGluc3RydWN0aW9ucyA9IHRoaXMuX2luc3RydWN0aW9ucztcblxuICAgIHRoaXMucmVnaXN0cnlcbiAgICAgIC5sb2FkKGNvbnRhaW5lci5wbHVnaW4pXG4gICAgICAudGhlbihzZXR0aW5ncyA9PiB7XG4gICAgICAgIGlmIChpbnN0cnVjdGlvbnMuaXNBdHRhY2hlZCkge1xuICAgICAgICAgIGluc3RydWN0aW9ucy5wYXJlbnQgPSBudWxsO1xuICAgICAgICB9XG4gICAgICAgIGlmICghZWRpdG9yLmlzQXR0YWNoZWQpIHtcbiAgICAgICAgICBwYW5lbC5hZGRXaWRnZXQoZWRpdG9yKTtcbiAgICAgICAgfVxuICAgICAgICBlZGl0b3Iuc2V0dGluZ3MgPSBzZXR0aW5ncztcbiAgICAgICAgbGlzdC5zZWxlY3Rpb24gPSBjb250YWluZXIucGx1Z2luO1xuICAgICAgICB0aGlzLl9zZXRMYXlvdXQoKTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcihgTG9hZGluZyAke2NvbnRhaW5lci5wbHVnaW59IHNldHRpbmdzIGZhaWxlZC5gLCByZWFzb24pO1xuICAgICAgICBsaXN0LnNlbGVjdGlvbiA9IHRoaXMuX3N0YXRlLmNvbnRhaW5lci5wbHVnaW4gPSAnJztcbiAgICAgICAgZWRpdG9yLnNldHRpbmdzID0gbnVsbDtcbiAgICAgICAgdGhpcy5fc2V0TGF5b3V0KCk7XG4gICAgICB9KTtcbiAgfVxuXG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfZWRpdG9yOiBQbHVnaW5FZGl0b3I7XG4gIHByaXZhdGUgX2ZldGNoaW5nOiBQcm9taXNlPHZvaWQ+IHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX2luc3RydWN0aW9uczogV2lkZ2V0O1xuICBwcml2YXRlIF9saXN0OiBQbHVnaW5MaXN0O1xuICBwcml2YXRlIF9wYW5lbDogU3BsaXRQYW5lbDtcbiAgcHJpdmF0ZSBfc2F2aW5nID0gZmFsc2U7XG4gIHByaXZhdGUgX3N0YXRlOiBTZXR0aW5nRWRpdG9yLklMYXlvdXRTdGF0ZSA9IEpTT05FeHQuZGVlcENvcHkoREVGQVVMVF9MQVlPVVQpO1xuICBwcml2YXRlIF93aGVuOiBQcm9taXNlPGFueT47XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGBTZXR0aW5nRWRpdG9yYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFNldHRpbmdFZGl0b3Ige1xuICAvKipcbiAgICogVGhlIGluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgYSBzZXR0aW5nIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSB0b29sYmFyIGNvbW1hbmRzIGFuZCByZWdpc3RyeSBmb3IgdGhlIHNldHRpbmcgZWRpdG9yIHRvb2xiYXIuXG4gICAgICovXG4gICAgY29tbWFuZHM6IHtcbiAgICAgIC8qKlxuICAgICAgICogVGhlIGNvbW1hbmQgcmVnaXN0cnkuXG4gICAgICAgKi9cbiAgICAgIHJlZ2lzdHJ5OiBDb21tYW5kUmVnaXN0cnk7XG5cbiAgICAgIC8qKlxuICAgICAgICogVGhlIHJldmVydCBjb21tYW5kIElELlxuICAgICAgICovXG4gICAgICByZXZlcnQ6IHN0cmluZztcblxuICAgICAgLyoqXG4gICAgICAgKiBUaGUgc2F2ZSBjb21tYW5kIElELlxuICAgICAgICovXG4gICAgICBzYXZlOiBzdHJpbmc7XG4gICAgfTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBlZGl0b3IgZmFjdG9yeSB1c2VkIGJ5IHRoZSBzZXR0aW5nIGVkaXRvci5cbiAgICAgKi9cbiAgICBlZGl0b3JGYWN0b3J5OiBDb2RlRWRpdG9yLkZhY3Rvcnk7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc3RhdGUgZGF0YWJhc2Uga2V5IGZvciB0aGUgZWRpdG9yJ3Mgc3RhdGUgbWFuYWdlbWVudC5cbiAgICAgKi9cbiAgICBrZXk6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBzZXR0aW5nIHJlZ2lzdHJ5IHRoZSBlZGl0b3IgbW9kaWZpZXMuXG4gICAgICovXG4gICAgcmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnk7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgb3B0aW9uYWwgTUlNRSByZW5kZXJlciB0byB1c2UgZm9yIHJlbmRlcmluZyBkZWJ1ZyBtZXNzYWdlcy5cbiAgICAgKi9cbiAgICByZW5kZXJtaW1lPzogSVJlbmRlck1pbWVSZWdpc3RyeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBzdGF0ZSBkYXRhYmFzZSB1c2VkIHRvIHN0b3JlIGxheW91dC5cbiAgICAgKi9cbiAgICBzdGF0ZTogSVN0YXRlREI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcG9pbnQgYWZ0ZXIgd2hpY2ggdGhlIGVkaXRvciBzaG91bGQgcmVzdG9yZSBpdHMgc3RhdGUuXG4gICAgICovXG4gICAgd2hlbj86IFByb21pc2U8YW55PiB8IEFycmF5PFByb21pc2U8YW55Pj47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGxheW91dCBzdGF0ZSBmb3IgdGhlIHNldHRpbmcgZWRpdG9yLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTGF5b3V0U3RhdGUgZXh0ZW5kcyBKU09OT2JqZWN0IHtcbiAgICAvKipcbiAgICAgKiBUaGUgbGF5b3V0IHN0YXRlIGZvciBhIHBsdWdpbiBlZGl0b3IgY29udGFpbmVyLlxuICAgICAqL1xuICAgIGNvbnRhaW5lcjogSVBsdWdpbkxheW91dDtcblxuICAgIC8qKlxuICAgICAqIFRoZSByZWxhdGl2ZSBzaXplcyBvZiB0aGUgcGx1Z2luIGxpc3QgYW5kIHBsdWdpbiBlZGl0b3IuXG4gICAgICovXG4gICAgc2l6ZXM6IG51bWJlcltdO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBsYXlvdXQgaW5mb3JtYXRpb24gdGhhdCBpcyBzdG9yZWQgYW5kIHJlc3RvcmVkIGZyb20gdGhlIHN0YXRlIGRhdGFiYXNlLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUGx1Z2luTGF5b3V0IGV4dGVuZHMgSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgcGx1Z2luIGJlaW5nIGRpc3BsYXllZC5cbiAgICAgKi9cbiAgICBwbHVnaW46IHN0cmluZztcbiAgICBzaXplczogbnVtYmVyW107XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBtb2R1bGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogUG9wdWxhdGUgdGhlIGluc3RydWN0aW9ucyB0ZXh0IG5vZGUuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcG9wdWxhdGVJbnN0cnVjdGlvbnNOb2RlKFxuICAgIG5vZGU6IEhUTUxFbGVtZW50LFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApOiB2b2lkIHtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIFJlYWN0RE9NLnJlbmRlcihcbiAgICAgIDxSZWFjdC5GcmFnbWVudD5cbiAgICAgICAgPGgyPlxuICAgICAgICAgIDxqdXB5dGVySWNvbi5yZWFjdFxuICAgICAgICAgICAgY2xhc3NOYW1lPVwianAtU2V0dGluZ0VkaXRvckluc3RydWN0aW9ucy1pY29uXCJcbiAgICAgICAgICAgIHRhZz1cInNwYW5cIlxuICAgICAgICAgICAgZWxlbWVudFBvc2l0aW9uPVwiY2VudGVyXCJcbiAgICAgICAgICAgIGhlaWdodD1cImF1dG9cIlxuICAgICAgICAgICAgd2lkdGg9XCI2MHB4XCJcbiAgICAgICAgICAvPlxuICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cImpwLVNldHRpbmdFZGl0b3JJbnN0cnVjdGlvbnMtdGl0bGVcIj5TZXR0aW5nczwvc3Bhbj5cbiAgICAgICAgPC9oMj5cbiAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwianAtU2V0dGluZ0VkaXRvckluc3RydWN0aW9ucy10ZXh0XCI+XG4gICAgICAgICAge3RyYW5zLl9fKFxuICAgICAgICAgICAgJ1NlbGVjdCBhIHBsdWdpbiBmcm9tIHRoZSBsaXN0IHRvIHZpZXcgYW5kIGVkaXQgaXRzIHByZWZlcmVuY2VzLidcbiAgICAgICAgICApfVxuICAgICAgICA8L3NwYW4+XG4gICAgICA8L1JlYWN0LkZyYWdtZW50PixcbiAgICAgIG5vZGVcbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldHVybiBhIG5vcm1hbGl6ZWQgcmVzdG9yZWQgbGF5b3V0IHN0YXRlIHRoYXQgZGVmYXVsdHMgdG8gdGhlIHByZXNldHMuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gbm9ybWFsaXplU3RhdGUoXG4gICAgc2F2ZWQ6IEpTT05PYmplY3QgfCBudWxsLFxuICAgIGN1cnJlbnQ6IFNldHRpbmdFZGl0b3IuSUxheW91dFN0YXRlXG4gICk6IFNldHRpbmdFZGl0b3IuSUxheW91dFN0YXRlIHtcbiAgICBpZiAoIXNhdmVkKSB7XG4gICAgICByZXR1cm4gSlNPTkV4dC5kZWVwQ29weShERUZBVUxUX0xBWU9VVCk7XG4gICAgfVxuXG4gICAgaWYgKCEoJ3NpemVzJyBpbiBzYXZlZCkgfHwgIW51bWJlckFycmF5KHNhdmVkLnNpemVzKSkge1xuICAgICAgc2F2ZWQuc2l6ZXMgPSBKU09ORXh0LmRlZXBDb3B5KERFRkFVTFRfTEFZT1VULnNpemVzKTtcbiAgICB9XG4gICAgaWYgKCEoJ2NvbnRhaW5lcicgaW4gc2F2ZWQpKSB7XG4gICAgICBzYXZlZC5jb250YWluZXIgPSBKU09ORXh0LmRlZXBDb3B5KERFRkFVTFRfTEFZT1VULmNvbnRhaW5lcik7XG4gICAgICByZXR1cm4gc2F2ZWQgYXMgU2V0dGluZ0VkaXRvci5JTGF5b3V0U3RhdGU7XG4gICAgfVxuXG4gICAgY29uc3QgY29udGFpbmVyID1cbiAgICAgICdjb250YWluZXInIGluIHNhdmVkICYmXG4gICAgICBzYXZlZC5jb250YWluZXIgJiZcbiAgICAgIHR5cGVvZiBzYXZlZC5jb250YWluZXIgPT09ICdvYmplY3QnXG4gICAgICAgID8gKHNhdmVkLmNvbnRhaW5lciBhcyBKU09OT2JqZWN0KVxuICAgICAgICA6IHt9O1xuXG4gICAgc2F2ZWQuY29udGFpbmVyID0ge1xuICAgICAgcGx1Z2luOlxuICAgICAgICB0eXBlb2YgY29udGFpbmVyLnBsdWdpbiA9PT0gJ3N0cmluZydcbiAgICAgICAgICA/IGNvbnRhaW5lci5wbHVnaW5cbiAgICAgICAgICA6IERFRkFVTFRfTEFZT1VULmNvbnRhaW5lci5wbHVnaW4sXG4gICAgICBzaXplczogbnVtYmVyQXJyYXkoY29udGFpbmVyLnNpemVzKVxuICAgICAgICA/IGNvbnRhaW5lci5zaXplc1xuICAgICAgICA6IEpTT05FeHQuZGVlcENvcHkoREVGQVVMVF9MQVlPVVQuY29udGFpbmVyLnNpemVzKVxuICAgIH07XG5cbiAgICByZXR1cm4gc2F2ZWQgYXMgU2V0dGluZ0VkaXRvci5JTGF5b3V0U3RhdGU7XG4gIH1cblxuICAvKipcbiAgICogVGVzdHMgd2hldGhlciBhbiBhcnJheSBjb25zaXN0cyBleGNsdXNpdmVseSBvZiBudW1iZXJzLlxuICAgKi9cbiAgZnVuY3Rpb24gbnVtYmVyQXJyYXkodmFsdWU6IEpTT05WYWx1ZSk6IGJvb2xlYW4ge1xuICAgIHJldHVybiBBcnJheS5pc0FycmF5KHZhbHVlKSAmJiB2YWx1ZS5ldmVyeSh4ID0+IHR5cGVvZiB4ID09PSAnbnVtYmVyJyk7XG4gIH1cbn1cbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuXG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBTcGxpdFBhbmVsIGFzIFNQYW5lbCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogQSBkZXByZWNhdGVkIHNwbGl0IHBhbmVsIHRoYXQgd2lsbCBiZSByZW1vdmVkIHdoZW4gdGhlIHBob3NwaG9yIHNwbGl0IHBhbmVsXG4gKiBzdXBwb3J0cyBhIGhhbmRsZSBtb3ZlZCBzaWduYWwuIFNlZSBodHRwczovL2dpdGh1Yi5jb20vcGhvc3Bob3Jqcy9waG9zcGhvci9pc3N1ZXMvMjk3LlxuICovXG5leHBvcnQgY2xhc3MgU3BsaXRQYW5lbCBleHRlbmRzIFNQYW5lbCB7XG4gIC8qKlxuICAgKiBFbWl0cyB3aGVuIHRoZSBzcGxpdCBoYW5kbGUgaGFzIG1vdmVkLlxuICAgKi9cbiAgcmVhZG9ubHkgaGFuZGxlTW92ZWQ6IElTaWduYWw8YW55LCB2b2lkPiA9IG5ldyBTaWduYWw8YW55LCB2b2lkPih0aGlzKTtcblxuICBoYW5kbGVFdmVudChldmVudDogRXZlbnQpOiB2b2lkIHtcbiAgICBzdXBlci5oYW5kbGVFdmVudChldmVudCk7XG5cbiAgICBpZiAoZXZlbnQudHlwZSA9PT0gJ21vdXNldXAnKSB7XG4gICAgICAodGhpcy5oYW5kbGVNb3ZlZCBhcyBTaWduYWw8YW55LCB2b2lkPikuZW1pdCh1bmRlZmluZWQpO1xuICAgIH1cbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJV2lkZ2V0VHJhY2tlciwgTWFpbkFyZWFXaWRnZXQgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IFNldHRpbmdFZGl0b3IgfSBmcm9tICcuL3NldHRpbmdlZGl0b3InO1xuXG4vKiB0c2xpbnQ6ZGlzYWJsZSAqL1xuLyoqXG4gKiBUaGUgc2V0dGluZyBlZGl0b3IgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElTZXR0aW5nRWRpdG9yVHJhY2tlciA9IG5ldyBUb2tlbjxJU2V0dGluZ0VkaXRvclRyYWNrZXI+KFxuICAnQGp1cHl0ZXJsYWIvc2V0dGluZ2VkaXRvcjpJU2V0dGluZ0VkaXRvclRyYWNrZXInXG4pO1xuLyogdHNsaW50OmVuYWJsZSAqL1xuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCB0cmFja3MgdGhlIHNldHRpbmcgZWRpdG9yLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElTZXR0aW5nRWRpdG9yVHJhY2tlclxuICBleHRlbmRzIElXaWRnZXRUcmFja2VyPE1haW5BcmVhV2lkZ2V0PFNldHRpbmdFZGl0b3I+PiB7fVxuIl0sInNvdXJjZVJvb3QiOiIifQ==