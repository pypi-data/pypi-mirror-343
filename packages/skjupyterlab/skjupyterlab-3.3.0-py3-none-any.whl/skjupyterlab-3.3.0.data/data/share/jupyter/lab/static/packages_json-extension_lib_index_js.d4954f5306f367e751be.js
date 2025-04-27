(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_json-extension_lib_index_js"],{

/***/ "../packages/json-extension/lib/component.js":
/*!***************************************************!*\
  !*** ../packages/json-extension/lib/component.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Component": () => (/* binding */ Component)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react_highlighter__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react-highlighter */ "webpack/sharing/consume/default/react-highlighter/react-highlighter");
/* harmony import */ var react_highlighter__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react_highlighter__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react_json_tree__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react-json-tree */ "webpack/sharing/consume/default/react-json-tree/react-json-tree");
/* harmony import */ var react_json_tree__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react_json_tree__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * A component that renders JSON data as a collapsible tree.
 */
class Component extends react__WEBPACK_IMPORTED_MODULE_3__.Component {
    constructor() {
        super(...arguments);
        this.state = { filter: '', value: '' };
        this.timer = 0;
        this.handleChange = (event) => {
            const { value } = event.target;
            this.setState({ value });
            window.clearTimeout(this.timer);
            this.timer = window.setTimeout(() => {
                this.setState({ filter: value });
            }, 300);
        };
    }
    render() {
        const translator = this.props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const { data, metadata } = this.props;
        const root = metadata && metadata.root ? metadata.root : 'root';
        const keyPaths = this.state.filter
            ? filterPaths(data, this.state.filter, [root])
            : [root];
        return (react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "container" },
            react__WEBPACK_IMPORTED_MODULE_3__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.InputGroup, { className: "filter", type: "text", placeholder: trans.__('Filter…'), onChange: this.handleChange, value: this.state.value, rightIcon: "ui-components:search" }),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement((react_json_tree__WEBPACK_IMPORTED_MODULE_5___default()), { data: data, collectionLimit: 100, theme: {
                    extend: theme,
                    valueLabel: 'cm-variable',
                    valueText: 'cm-string',
                    nestedNodeItemString: 'cm-comment'
                }, invertTheme: false, keyPath: [root], getItemString: (type, data, itemType, itemString) => Array.isArray(data) ? (
                // Always display array type and the number of items i.e. "[] 2 items".
                react__WEBPACK_IMPORTED_MODULE_3__.createElement("span", null,
                    itemType,
                    " ",
                    itemString)) : Object.keys(data).length === 0 ? (
                // Only display object type when it's empty i.e. "{}".
                react__WEBPACK_IMPORTED_MODULE_3__.createElement("span", null, itemType)) : (null // Upstream typings don't accept null, but it should be ok
                ), labelRenderer: ([label, type]) => {
                    // let className = 'cm-variable';
                    // if (type === 'root') {
                    //   className = 'cm-variable-2';
                    // }
                    // if (type === 'array') {
                    //   className = 'cm-variable-2';
                    // }
                    // if (type === 'Object') {
                    //   className = 'cm-variable-3';
                    // }
                    return (react__WEBPACK_IMPORTED_MODULE_3__.createElement("span", { className: "cm-keyword" },
                        react__WEBPACK_IMPORTED_MODULE_3__.createElement((react_highlighter__WEBPACK_IMPORTED_MODULE_4___default()), { search: this.state.filter, matchStyle: { backgroundColor: 'yellow' } }, `${label}: `)));
                }, valueRenderer: raw => {
                    let className = 'cm-string';
                    if (typeof raw === 'number') {
                        className = 'cm-number';
                    }
                    if (raw === 'true' || raw === 'false') {
                        className = 'cm-keyword';
                    }
                    return (react__WEBPACK_IMPORTED_MODULE_3__.createElement("span", { className: className },
                        react__WEBPACK_IMPORTED_MODULE_3__.createElement((react_highlighter__WEBPACK_IMPORTED_MODULE_4___default()), { search: this.state.filter, matchStyle: { backgroundColor: 'yellow' } }, `${raw}`)));
                }, shouldExpandNode: (keyPath, data, level) => metadata && metadata.expanded
                    ? true
                    : keyPaths.join(',').includes(keyPath.join(',')) })));
    }
}
// Provide an invalid theme object (this is on purpose!) to invalidate the
// react-json-tree's inline styles that override CodeMirror CSS classes
const theme = {
    scheme: 'jupyter',
    base00: 'invalid',
    base01: 'invalid',
    base02: 'invalid',
    base03: 'invalid',
    base04: 'invalid',
    base05: 'invalid',
    base06: 'invalid',
    base07: 'invalid',
    base08: 'invalid',
    base09: 'invalid',
    base0A: 'invalid',
    base0B: 'invalid',
    base0C: 'invalid',
    base0D: 'invalid',
    base0E: 'invalid',
    base0F: 'invalid',
    author: 'invalid'
};
function objectIncludes(data, query) {
    return JSON.stringify(data).includes(query);
}
function filterPaths(data, query, parent = ['root']) {
    if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.isArray(data)) {
        return data.reduce((result, item, index) => {
            if (item && typeof item === 'object' && objectIncludes(item, query)) {
                return [
                    ...result,
                    [index, ...parent].join(','),
                    ...filterPaths(item, query, [index, ...parent])
                ];
            }
            return result;
        }, []);
    }
    if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.isObject(data)) {
        return Object.keys(data).reduce((result, key) => {
            const item = data[key];
            if (item &&
                typeof item === 'object' &&
                (key.includes(query) || objectIncludes(item, query))) {
                return [
                    ...result,
                    [key, ...parent].join(','),
                    ...filterPaths(item, query, [key, ...parent])
                ];
            }
            return result;
        }, []);
    }
    return [];
}


/***/ }),

/***/ "../packages/json-extension/lib/index.js":
/*!***********************************************!*\
  !*** ../packages/json-extension/lib/index.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MIME_TYPE": () => (/* binding */ MIME_TYPE),
/* harmony export */   "RenderedJSON": () => (/* binding */ RenderedJSON),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./component */ "../packages/json-extension/lib/component.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module json-extension
 */






/**
 * The CSS class to add to the JSON Widget.
 */
const CSS_CLASS = 'jp-RenderedJSON';
/**
 * The MIME type for JSON.
 */
const MIME_TYPE = 'application/json';
/**
 * A renderer for JSON data.
 */
class RenderedJSON extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    /**
     * Create a new widget for rendering JSON.
     */
    constructor(options) {
        super();
        this.addClass(CSS_CLASS);
        this.addClass('CodeMirror');
        this.addClass('cm-s-jupyter');
        this._mimeType = options.mimeType;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    }
    [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.symbol]() {
        return () => _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.printWidget(this);
    }
    /**
     * Render JSON into this widget's node.
     */
    renderModel(model) {
        const data = (model.data[this._mimeType] || {});
        const metadata = (model.metadata[this._mimeType] || {});
        return new Promise((resolve, reject) => {
            react_dom__WEBPACK_IMPORTED_MODULE_4__.render(react__WEBPACK_IMPORTED_MODULE_3__.createElement(_component__WEBPACK_IMPORTED_MODULE_5__.Component, { data: data, metadata: metadata, translator: this.translator }), this.node, () => {
                resolve();
            });
        });
    }
    /**
     * Called before the widget is detached from the DOM.
     */
    onBeforeDetach(msg) {
        // Unmount the component so it can tear down.
        react_dom__WEBPACK_IMPORTED_MODULE_4__.unmountComponentAtNode(this.node);
    }
}
/**
 * A mime renderer factory for JSON data.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [MIME_TYPE],
    createRenderer: options => new RenderedJSON(options)
};
const extensions = [
    {
        id: '@jupyterlab/json-extension:factory',
        rendererFactory,
        rank: 0,
        dataType: 'json',
        documentWidgetFactoryOptions: {
            name: 'JSON',
            primaryFileType: 'json',
            fileTypes: ['json', 'notebook', 'geojson'],
            defaultFor: ['json']
        }
    }
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extensions);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvanNvbi1leHRlbnNpb24vc3JjL2NvbXBvbmVudC50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2pzb24tZXh0ZW5zaW9uL3NyYy9pbmRleC50c3giXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFVztBQUNmO0FBQ3VCO0FBQy9DO0FBQ1c7QUFDSDtBQXVCdkM7O0dBRUc7QUFDSSxNQUFNLFNBQVUsU0FBUSw0Q0FBK0I7SUFBOUQ7O1FBQ0UsVUFBSyxHQUFHLEVBQUUsTUFBTSxFQUFFLEVBQUUsRUFBRSxLQUFLLEVBQUUsRUFBRSxFQUFFLENBQUM7UUFFbEMsVUFBSyxHQUFXLENBQUMsQ0FBQztRQUVsQixpQkFBWSxHQUFHLENBQUMsS0FBMEMsRUFBRSxFQUFFO1lBQzVELE1BQU0sRUFBRSxLQUFLLEVBQUUsR0FBRyxLQUFLLENBQUMsTUFBTSxDQUFDO1lBQy9CLElBQUksQ0FBQyxRQUFRLENBQUMsRUFBRSxLQUFLLEVBQUUsQ0FBQyxDQUFDO1lBQ3pCLE1BQU0sQ0FBQyxZQUFZLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxDQUFDO1lBQ2hDLElBQUksQ0FBQyxLQUFLLEdBQUcsTUFBTSxDQUFDLFVBQVUsQ0FBQyxHQUFHLEVBQUU7Z0JBQ2xDLElBQUksQ0FBQyxRQUFRLENBQUMsRUFBRSxNQUFNLEVBQUUsS0FBSyxFQUFFLENBQUMsQ0FBQztZQUNuQyxDQUFDLEVBQUUsR0FBRyxDQUFDLENBQUM7UUFDVixDQUFDLENBQUM7SUErRkosQ0FBQztJQTdGQyxNQUFNO1FBQ0osTUFBTSxVQUFVLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQyxVQUFVLElBQUksbUVBQWMsQ0FBQztRQUMzRCxNQUFNLEtBQUssR0FBRyxVQUFVLENB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QUMiLCJmaWxlIjoicGFja2FnZXNfanNvbi1leHRlbnNpb25fbGliX2luZGV4X2pzLmQ0OTU0ZjUzMDZmMzY3ZTc1MWJlLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBJbnB1dEdyb3VwIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBKU09OQXJyYXksIEpTT05FeHQsIEpTT05PYmplY3QsIEpTT05WYWx1ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBIaWdobGlnaHQgZnJvbSAncmVhY3QtaGlnaGxpZ2h0ZXInO1xuaW1wb3J0IEpTT05UcmVlIGZyb20gJ3JlYWN0LWpzb24tdHJlZSc7XG5cbi8qKlxuICogVGhlIHByb3BlcnRpZXMgZm9yIHRoZSBKU09OIHRyZWUgY29tcG9uZW50LlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElQcm9wcyB7XG4gIGRhdGE6IE5vbk51bGxhYmxlPEpTT05WYWx1ZT47XG4gIG1ldGFkYXRhPzogSlNPTk9iamVjdDtcblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIGxhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAqL1xuICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG59XG5cbi8qKlxuICogVGhlIHN0YXRlIG9mIHRoZSBKU09OIHRyZWUgY29tcG9uZW50LlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElTdGF0ZSB7XG4gIGZpbHRlcj86IHN0cmluZztcbiAgdmFsdWU6IHN0cmluZztcbn1cblxuLyoqXG4gKiBBIGNvbXBvbmVudCB0aGF0IHJlbmRlcnMgSlNPTiBkYXRhIGFzIGEgY29sbGFwc2libGUgdHJlZS5cbiAqL1xuZXhwb3J0IGNsYXNzIENvbXBvbmVudCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudDxJUHJvcHMsIElTdGF0ZT4ge1xuICBzdGF0ZSA9IHsgZmlsdGVyOiAnJywgdmFsdWU6ICcnIH07XG5cbiAgdGltZXI6IG51bWJlciA9IDA7XG5cbiAgaGFuZGxlQ2hhbmdlID0gKGV2ZW50OiBSZWFjdC5DaGFuZ2VFdmVudDxIVE1MSW5wdXRFbGVtZW50PikgPT4ge1xuICAgIGNvbnN0IHsgdmFsdWUgfSA9IGV2ZW50LnRhcmdldDtcbiAgICB0aGlzLnNldFN0YXRlKHsgdmFsdWUgfSk7XG4gICAgd2luZG93LmNsZWFyVGltZW91dCh0aGlzLnRpbWVyKTtcbiAgICB0aGlzLnRpbWVyID0gd2luZG93LnNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgdGhpcy5zZXRTdGF0ZSh7IGZpbHRlcjogdmFsdWUgfSk7XG4gICAgfSwgMzAwKTtcbiAgfTtcblxuICByZW5kZXIoKSB7XG4gICAgY29uc3QgdHJhbnNsYXRvciA9IHRoaXMucHJvcHMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgY29uc3QgeyBkYXRhLCBtZXRhZGF0YSB9ID0gdGhpcy5wcm9wcztcbiAgICBjb25zdCByb290ID0gbWV0YWRhdGEgJiYgbWV0YWRhdGEucm9vdCA/IChtZXRhZGF0YS5yb290IGFzIHN0cmluZykgOiAncm9vdCc7XG4gICAgY29uc3Qga2V5UGF0aHMgPSB0aGlzLnN0YXRlLmZpbHRlclxuICAgICAgPyBmaWx0ZXJQYXRocyhkYXRhLCB0aGlzLnN0YXRlLmZpbHRlciwgW3Jvb3RdKVxuICAgICAgOiBbcm9vdF07XG4gICAgcmV0dXJuIChcbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG4gICAgICAgIDxJbnB1dEdyb3VwXG4gICAgICAgICAgY2xhc3NOYW1lPVwiZmlsdGVyXCJcbiAgICAgICAgICB0eXBlPVwidGV4dFwiXG4gICAgICAgICAgcGxhY2Vob2xkZXI9e3RyYW5zLl9fKCdGaWx0ZXLigKYnKX1cbiAgICAgICAgICBvbkNoYW5nZT17dGhpcy5oYW5kbGVDaGFuZ2V9XG4gICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUudmFsdWV9XG4gICAgICAgICAgcmlnaHRJY29uPVwidWktY29tcG9uZW50czpzZWFyY2hcIlxuICAgICAgICAvPlxuICAgICAgICA8SlNPTlRyZWVcbiAgICAgICAgICBkYXRhPXtkYXRhfVxuICAgICAgICAgIGNvbGxlY3Rpb25MaW1pdD17MTAwfVxuICAgICAgICAgIHRoZW1lPXt7XG4gICAgICAgICAgICBleHRlbmQ6IHRoZW1lLFxuICAgICAgICAgICAgdmFsdWVMYWJlbDogJ2NtLXZhcmlhYmxlJyxcbiAgICAgICAgICAgIHZhbHVlVGV4dDogJ2NtLXN0cmluZycsXG4gICAgICAgICAgICBuZXN0ZWROb2RlSXRlbVN0cmluZzogJ2NtLWNvbW1lbnQnXG4gICAgICAgICAgfX1cbiAgICAgICAgICBpbnZlcnRUaGVtZT17ZmFsc2V9XG4gICAgICAgICAga2V5UGF0aD17W3Jvb3RdfVxuICAgICAgICAgIGdldEl0ZW1TdHJpbmc9eyh0eXBlLCBkYXRhLCBpdGVtVHlwZSwgaXRlbVN0cmluZykgPT5cbiAgICAgICAgICAgIEFycmF5LmlzQXJyYXkoZGF0YSkgPyAoXG4gICAgICAgICAgICAgIC8vIEFsd2F5cyBkaXNwbGF5IGFycmF5IHR5cGUgYW5kIHRoZSBudW1iZXIgb2YgaXRlbXMgaS5lLiBcIltdIDIgaXRlbXNcIi5cbiAgICAgICAgICAgICAgPHNwYW4+XG4gICAgICAgICAgICAgICAge2l0ZW1UeXBlfSB7aXRlbVN0cmluZ31cbiAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgKSA6IE9iamVjdC5rZXlzKGRhdGEpLmxlbmd0aCA9PT0gMCA/IChcbiAgICAgICAgICAgICAgLy8gT25seSBkaXNwbGF5IG9iamVjdCB0eXBlIHdoZW4gaXQncyBlbXB0eSBpLmUuIFwie31cIi5cbiAgICAgICAgICAgICAgPHNwYW4+e2l0ZW1UeXBlfTwvc3Bhbj5cbiAgICAgICAgICAgICkgOiAoXG4gICAgICAgICAgICAgIG51bGwhIC8vIFVwc3RyZWFtIHR5cGluZ3MgZG9uJ3QgYWNjZXB0IG51bGwsIGJ1dCBpdCBzaG91bGQgYmUgb2tcbiAgICAgICAgICAgIClcbiAgICAgICAgICB9XG4gICAgICAgICAgbGFiZWxSZW5kZXJlcj17KFtsYWJlbCwgdHlwZV0pID0+IHtcbiAgICAgICAgICAgIC8vIGxldCBjbGFzc05hbWUgPSAnY20tdmFyaWFibGUnO1xuICAgICAgICAgICAgLy8gaWYgKHR5cGUgPT09ICdyb290Jykge1xuICAgICAgICAgICAgLy8gICBjbGFzc05hbWUgPSAnY20tdmFyaWFibGUtMic7XG4gICAgICAgICAgICAvLyB9XG4gICAgICAgICAgICAvLyBpZiAodHlwZSA9PT0gJ2FycmF5Jykge1xuICAgICAgICAgICAgLy8gICBjbGFzc05hbWUgPSAnY20tdmFyaWFibGUtMic7XG4gICAgICAgICAgICAvLyB9XG4gICAgICAgICAgICAvLyBpZiAodHlwZSA9PT0gJ09iamVjdCcpIHtcbiAgICAgICAgICAgIC8vICAgY2xhc3NOYW1lID0gJ2NtLXZhcmlhYmxlLTMnO1xuICAgICAgICAgICAgLy8gfVxuICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwiY20ta2V5d29yZFwiPlxuICAgICAgICAgICAgICAgIDxIaWdobGlnaHRcbiAgICAgICAgICAgICAgICAgIHNlYXJjaD17dGhpcy5zdGF0ZS5maWx0ZXJ9XG4gICAgICAgICAgICAgICAgICBtYXRjaFN0eWxlPXt7IGJhY2tncm91bmRDb2xvcjogJ3llbGxvdycgfX1cbiAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICB7YCR7bGFiZWx9OiBgfVxuICAgICAgICAgICAgICAgIDwvSGlnaGxpZ2h0PlxuICAgICAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICAgICApO1xuICAgICAgICAgIH19XG4gICAgICAgICAgdmFsdWVSZW5kZXJlcj17cmF3ID0+IHtcbiAgICAgICAgICAgIGxldCBjbGFzc05hbWUgPSAnY20tc3RyaW5nJztcbiAgICAgICAgICAgIGlmICh0eXBlb2YgcmF3ID09PSAnbnVtYmVyJykge1xuICAgICAgICAgICAgICBjbGFzc05hbWUgPSAnY20tbnVtYmVyJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGlmIChyYXcgPT09ICd0cnVlJyB8fCByYXcgPT09ICdmYWxzZScpIHtcbiAgICAgICAgICAgICAgY2xhc3NOYW1lID0gJ2NtLWtleXdvcmQnO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPXtjbGFzc05hbWV9PlxuICAgICAgICAgICAgICAgIDxIaWdobGlnaHRcbiAgICAgICAgICAgICAgICAgIHNlYXJjaD17dGhpcy5zdGF0ZS5maWx0ZXJ9XG4gICAgICAgICAgICAgICAgICBtYXRjaFN0eWxlPXt7IGJhY2tncm91bmRDb2xvcjogJ3llbGxvdycgfX1cbiAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICB7YCR7cmF3fWB9XG4gICAgICAgICAgICAgICAgPC9IaWdobGlnaHQ+XG4gICAgICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgICAgICk7XG4gICAgICAgICAgfX1cbiAgICAgICAgICBzaG91bGRFeHBhbmROb2RlPXsoa2V5UGF0aCwgZGF0YSwgbGV2ZWwpID0+XG4gICAgICAgICAgICBtZXRhZGF0YSAmJiBtZXRhZGF0YS5leHBhbmRlZFxuICAgICAgICAgICAgICA/IHRydWVcbiAgICAgICAgICAgICAgOiBrZXlQYXRocy5qb2luKCcsJykuaW5jbHVkZXMoa2V5UGF0aC5qb2luKCcsJykpXG4gICAgICAgICAgfVxuICAgICAgICAvPlxuICAgICAgPC9kaXY+XG4gICAgKTtcbiAgfVxufVxuXG4vLyBQcm92aWRlIGFuIGludmFsaWQgdGhlbWUgb2JqZWN0ICh0aGlzIGlzIG9uIHB1cnBvc2UhKSB0byBpbnZhbGlkYXRlIHRoZVxuLy8gcmVhY3QtanNvbi10cmVlJ3MgaW5saW5lIHN0eWxlcyB0aGF0IG92ZXJyaWRlIENvZGVNaXJyb3IgQ1NTIGNsYXNzZXNcbmNvbnN0IHRoZW1lID0ge1xuICBzY2hlbWU6ICdqdXB5dGVyJyxcbiAgYmFzZTAwOiAnaW52YWxpZCcsXG4gIGJhc2UwMTogJ2ludmFsaWQnLFxuICBiYXNlMDI6ICdpbnZhbGlkJyxcbiAgYmFzZTAzOiAnaW52YWxpZCcsXG4gIGJhc2UwNDogJ2ludmFsaWQnLFxuICBiYXNlMDU6ICdpbnZhbGlkJyxcbiAgYmFzZTA2OiAnaW52YWxpZCcsXG4gIGJhc2UwNzogJ2ludmFsaWQnLFxuICBiYXNlMDg6ICdpbnZhbGlkJyxcbiAgYmFzZTA5OiAnaW52YWxpZCcsXG4gIGJhc2UwQTogJ2ludmFsaWQnLFxuICBiYXNlMEI6ICdpbnZhbGlkJyxcbiAgYmFzZTBDOiAnaW52YWxpZCcsXG4gIGJhc2UwRDogJ2ludmFsaWQnLFxuICBiYXNlMEU6ICdpbnZhbGlkJyxcbiAgYmFzZTBGOiAnaW52YWxpZCcsXG4gIGF1dGhvcjogJ2ludmFsaWQnXG59O1xuXG5mdW5jdGlvbiBvYmplY3RJbmNsdWRlcyhkYXRhOiBKU09OVmFsdWUsIHF1ZXJ5OiBzdHJpbmcpOiBib29sZWFuIHtcbiAgcmV0dXJuIEpTT04uc3RyaW5naWZ5KGRhdGEpLmluY2x1ZGVzKHF1ZXJ5KTtcbn1cblxuZnVuY3Rpb24gZmlsdGVyUGF0aHMoXG4gIGRhdGE6IE5vbk51bGxhYmxlPEpTT05WYWx1ZT4sXG4gIHF1ZXJ5OiBzdHJpbmcsXG4gIHBhcmVudDogSlNPTkFycmF5ID0gWydyb290J11cbik6IEpTT05BcnJheSB7XG4gIGlmIChKU09ORXh0LmlzQXJyYXkoZGF0YSkpIHtcbiAgICByZXR1cm4gZGF0YS5yZWR1Y2UoKHJlc3VsdDogSlNPTkFycmF5LCBpdGVtOiBKU09OVmFsdWUsIGluZGV4OiBudW1iZXIpID0+IHtcbiAgICAgIGlmIChpdGVtICYmIHR5cGVvZiBpdGVtID09PSAnb2JqZWN0JyAmJiBvYmplY3RJbmNsdWRlcyhpdGVtLCBxdWVyeSkpIHtcbiAgICAgICAgcmV0dXJuIFtcbiAgICAgICAgICAuLi5yZXN1bHQsXG4gICAgICAgICAgW2luZGV4LCAuLi5wYXJlbnRdLmpvaW4oJywnKSxcbiAgICAgICAgICAuLi5maWx0ZXJQYXRocyhpdGVtLCBxdWVyeSwgW2luZGV4LCAuLi5wYXJlbnRdKVxuICAgICAgICBdO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHJlc3VsdDtcbiAgICB9LCBbXSkgYXMgSlNPTkFycmF5O1xuICB9XG4gIGlmIChKU09ORXh0LmlzT2JqZWN0KGRhdGEpKSB7XG4gICAgcmV0dXJuIE9iamVjdC5rZXlzKGRhdGEpLnJlZHVjZSgocmVzdWx0OiBKU09OQXJyYXksIGtleTogc3RyaW5nKSA9PiB7XG4gICAgICBjb25zdCBpdGVtID0gZGF0YVtrZXldO1xuICAgICAgaWYgKFxuICAgICAgICBpdGVtICYmXG4gICAgICAgIHR5cGVvZiBpdGVtID09PSAnb2JqZWN0JyAmJlxuICAgICAgICAoa2V5LmluY2x1ZGVzKHF1ZXJ5KSB8fCBvYmplY3RJbmNsdWRlcyhpdGVtLCBxdWVyeSkpXG4gICAgICApIHtcbiAgICAgICAgcmV0dXJuIFtcbiAgICAgICAgICAuLi5yZXN1bHQsXG4gICAgICAgICAgW2tleSwgLi4ucGFyZW50XS5qb2luKCcsJyksXG4gICAgICAgICAgLi4uZmlsdGVyUGF0aHMoaXRlbSwgcXVlcnksIFtrZXksIC4uLnBhcmVudF0pXG4gICAgICAgIF07XG4gICAgICB9XG4gICAgICByZXR1cm4gcmVzdWx0O1xuICAgIH0sIFtdKTtcbiAgfVxuICByZXR1cm4gW107XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBqc29uLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7IFByaW50aW5nIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSVJlbmRlck1pbWUgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lLWludGVyZmFjZXMnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgSlNPTk9iamVjdCwgSlNPTlZhbHVlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgKiBhcyBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IHsgQ29tcG9uZW50IH0gZnJvbSAnLi9jb21wb25lbnQnO1xuXG4vKipcbiAqIFRoZSBDU1MgY2xhc3MgdG8gYWRkIHRvIHRoZSBKU09OIFdpZGdldC5cbiAqL1xuY29uc3QgQ1NTX0NMQVNTID0gJ2pwLVJlbmRlcmVkSlNPTic7XG5cbi8qKlxuICogVGhlIE1JTUUgdHlwZSBmb3IgSlNPTi5cbiAqL1xuZXhwb3J0IGNvbnN0IE1JTUVfVFlQRSA9ICdhcHBsaWNhdGlvbi9qc29uJztcblxuLyoqXG4gKiBBIHJlbmRlcmVyIGZvciBKU09OIGRhdGEuXG4gKi9cbmV4cG9ydCBjbGFzcyBSZW5kZXJlZEpTT05cbiAgZXh0ZW5kcyBXaWRnZXRcbiAgaW1wbGVtZW50cyBJUmVuZGVyTWltZS5JUmVuZGVyZXIsIFByaW50aW5nLklQcmludGFibGUge1xuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHdpZGdldCBmb3IgcmVuZGVyaW5nIEpTT04uXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmVuZGVyTWltZS5JUmVuZGVyZXJPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLmFkZENsYXNzKENTU19DTEFTUyk7XG4gICAgdGhpcy5hZGRDbGFzcygnQ29kZU1pcnJvcicpO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ2NtLXMtanVweXRlcicpO1xuICAgIHRoaXMuX21pbWVUeXBlID0gb3B0aW9ucy5taW1lVHlwZTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gIH1cblxuICBbUHJpbnRpbmcuc3ltYm9sXSgpIHtcbiAgICByZXR1cm4gKCkgPT4gUHJpbnRpbmcucHJpbnRXaWRnZXQodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIEpTT04gaW50byB0aGlzIHdpZGdldCdzIG5vZGUuXG4gICAqL1xuICByZW5kZXJNb2RlbChtb2RlbDogSVJlbmRlck1pbWUuSU1pbWVNb2RlbCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IGRhdGEgPSAobW9kZWwuZGF0YVt0aGlzLl9taW1lVHlwZV0gfHwge30pIGFzIE5vbk51bGxhYmxlPEpTT05WYWx1ZT47XG4gICAgY29uc3QgbWV0YWRhdGEgPSAobW9kZWwubWV0YWRhdGFbdGhpcy5fbWltZVR5cGVdIHx8IHt9KSBhcyBKU09OT2JqZWN0O1xuICAgIHJldHVybiBuZXcgUHJvbWlzZTx2b2lkPigocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICAgIDxDb21wb25lbnRcbiAgICAgICAgICBkYXRhPXtkYXRhfVxuICAgICAgICAgIG1ldGFkYXRhPXttZXRhZGF0YX1cbiAgICAgICAgICB0cmFuc2xhdG9yPXt0aGlzLnRyYW5zbGF0b3J9XG4gICAgICAgIC8+LFxuICAgICAgICB0aGlzLm5vZGUsXG4gICAgICAgICgpID0+IHtcbiAgICAgICAgICByZXNvbHZlKCk7XG4gICAgICAgIH1cbiAgICAgICk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQ2FsbGVkIGJlZm9yZSB0aGUgd2lkZ2V0IGlzIGRldGFjaGVkIGZyb20gdGhlIERPTS5cbiAgICovXG4gIHByb3RlY3RlZCBvbkJlZm9yZURldGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICAvLyBVbm1vdW50IHRoZSBjb21wb25lbnQgc28gaXQgY2FuIHRlYXIgZG93bi5cbiAgICBSZWFjdERPTS51bm1vdW50Q29tcG9uZW50QXROb2RlKHRoaXMubm9kZSk7XG4gIH1cblxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfbWltZVR5cGU6IHN0cmluZztcbn1cblxuLyoqXG4gKiBBIG1pbWUgcmVuZGVyZXIgZmFjdG9yeSBmb3IgSlNPTiBkYXRhLlxuICovXG5leHBvcnQgY29uc3QgcmVuZGVyZXJGYWN0b3J5OiBJUmVuZGVyTWltZS5JUmVuZGVyZXJGYWN0b3J5ID0ge1xuICBzYWZlOiB0cnVlLFxuICBtaW1lVHlwZXM6IFtNSU1FX1RZUEVdLFxuICBjcmVhdGVSZW5kZXJlcjogb3B0aW9ucyA9PiBuZXcgUmVuZGVyZWRKU09OKG9wdGlvbnMpXG59O1xuXG5jb25zdCBleHRlbnNpb25zOiBJUmVuZGVyTWltZS5JRXh0ZW5zaW9uIHwgSVJlbmRlck1pbWUuSUV4dGVuc2lvbltdID0gW1xuICB7XG4gICAgaWQ6ICdAanVweXRlcmxhYi9qc29uLWV4dGVuc2lvbjpmYWN0b3J5JyxcbiAgICByZW5kZXJlckZhY3RvcnksXG4gICAgcmFuazogMCxcbiAgICBkYXRhVHlwZTogJ2pzb24nLFxuICAgIGRvY3VtZW50V2lkZ2V0RmFjdG9yeU9wdGlvbnM6IHtcbiAgICAgIG5hbWU6ICdKU09OJyxcbiAgICAgIHByaW1hcnlGaWxlVHlwZTogJ2pzb24nLFxuICAgICAgZmlsZVR5cGVzOiBbJ2pzb24nLCAnbm90ZWJvb2snLCAnZ2VvanNvbiddLFxuICAgICAgZGVmYXVsdEZvcjogWydqc29uJ11cbiAgICB9XG4gIH1cbl07XG5cbmV4cG9ydCBkZWZhdWx0IGV4dGVuc2lvbnM7XG4iXSwic291cmNlUm9vdCI6IiJ9