(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_celltags_lib_index_js"],{

/***/ "../packages/celltags/lib/addwidget.js":
/*!*********************************************!*\
  !*** ../packages/celltags/lib/addwidget.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AddWidget": () => (/* binding */ AddWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);



/**
 * A widget which hosts a cell tags area.
 */
class AddWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    /**
     * Construct a new tag widget.
     */
    constructor(translator) {
        super();
        this.parent = null;
        this.input = document.createElement('input');
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.addClass('tag');
        this.editing = false;
        this.buildTag();
    }
    /**
     * Create input box with icon and attach to this.node.
     */
    buildTag() {
        const text = this.input || document.createElement('input');
        text.value = this._trans.__('Add Tag');
        text.contentEditable = 'true';
        text.className = 'add-tag';
        text.style.width = '49px';
        this.input = text;
        const tag = document.createElement('div');
        tag.className = 'tag-holder';
        tag.appendChild(text);
        const iconContainer = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.addIcon.element({
            tag: 'span',
            elementPosition: 'center',
            height: '18px',
            width: '18px',
            marginLeft: '3px',
            marginRight: '-5px'
        });
        this.addClass('unapplied-tag');
        tag.appendChild(iconContainer);
        this.node.appendChild(tag);
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach() {
        this.node.addEventListener('mousedown', this);
        this.input.addEventListener('keydown', this);
        this.input.addEventListener('focus', this);
        this.input.addEventListener('blur', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach() {
        this.node.removeEventListener('mousedown', this);
        this.input.removeEventListener('keydown', this);
        this.input.removeEventListener('focus', this);
        this.input.removeEventListener('blur', this);
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'mousedown':
                this._evtMouseDown(event);
                break;
            case 'keydown':
                this._evtKeyDown(event);
                break;
            case 'blur':
                this._evtBlur();
                break;
            case 'focus':
                this._evtFocus();
                break;
            default:
                break;
        }
    }
    /**
     * Handle the `'mousedown'` event for the input box.
     *
     * @param event - The DOM event sent to the widget
     */
    _evtMouseDown(event) {
        if (!this.editing) {
            this.editing = true;
            this.input.value = '';
            this.input.focus();
        }
        else if (event.target !== this.input) {
            if (this.input.value !== '') {
                const value = this.input.value;
                this.parent.addTag(value);
                this.input.blur();
                this._evtBlur();
            }
        }
        event.preventDefault();
    }
    /**
     * Handle the `'focus'` event for the input box.
     */
    _evtFocus() {
        if (!this.editing) {
            this.input.blur();
        }
    }
    /**
     * Handle the `'keydown'` event for the input box.
     *
     * @param event - The DOM event sent to the widget
     */
    _evtKeyDown(event) {
        const tmp = document.createElement('span');
        tmp.className = 'add-tag';
        tmp.innerHTML = this.input.value;
        // set width to the pixel length of the text
        document.body.appendChild(tmp);
        this.input.style.width = tmp.getBoundingClientRect().width + 8 + 'px';
        document.body.removeChild(tmp);
        // if they hit Enter, add the tag and reset state
        if (event.keyCode === 13) {
            const value = this.input.value;
            this.parent.addTag(value);
            this.input.blur();
            this._evtBlur();
        }
    }
    /**
     * Handle the `'focusout'` event for the input box.
     */
    _evtBlur() {
        if (this.editing) {
            this.editing = false;
            this.input.value = this._trans.__('Add Tag');
            this.input.style.width = '49px';
        }
    }
}


/***/ }),

/***/ "../packages/celltags/lib/index.js":
/*!*****************************************!*\
  !*** ../packages/celltags/lib/index.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AddWidget": () => (/* reexport safe */ _addwidget__WEBPACK_IMPORTED_MODULE_0__.AddWidget),
/* harmony export */   "TagTool": () => (/* reexport safe */ _tool__WEBPACK_IMPORTED_MODULE_1__.TagTool),
/* harmony export */   "TagWidget": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.TagWidget)
/* harmony export */ });
/* harmony import */ var _addwidget__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./addwidget */ "../packages/celltags/lib/addwidget.js");
/* harmony import */ var _tool__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tool */ "../packages/celltags/lib/tool.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "../packages/celltags/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module celltags
 */





/***/ }),

/***/ "../packages/celltags/lib/tool.js":
/*!****************************************!*\
  !*** ../packages/celltags/lib/tool.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TagTool": () => (/* binding */ TagTool)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _addwidget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./addwidget */ "../packages/celltags/lib/addwidget.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widget */ "../packages/celltags/lib/widget.js");






/**
 * A Tool for tag operations.
 */
class TagTool extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookTools.Tool {
    /**
     * Construct a new tag Tool.
     *
     * @param tracker - The notebook tracker.
     */
    constructor(tracker, app, translator) {
        super();
        this.tagList = [];
        this.label = false;
        app;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.tracker = tracker;
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.PanelLayout();
        this.createTagInput();
        this.addClass('jp-TagTool');
    }
    /**
     * Add an AddWidget input box to the layout.
     */
    createTagInput() {
        const layout = this.layout;
        const input = new _addwidget__WEBPACK_IMPORTED_MODULE_4__.AddWidget(this.translator);
        input.id = 'add-tag';
        layout.insertWidget(0, input);
    }
    /**
     * Check whether a tag is applied to the current active cell
     *
     * @param name - The name of the tag.
     *
     * @returns A boolean representing whether it is applied.
     */
    checkApplied(name) {
        var _a;
        const activeCell = (_a = this.tracker) === null || _a === void 0 ? void 0 : _a.activeCell;
        if (activeCell) {
            const tags = activeCell.model.metadata.get('tags');
            if (tags) {
                return tags.includes(name);
            }
        }
        return false;
    }
    /**
     * Add a tag to the current active cell.
     *
     * @param name - The name of the tag.
     */
    addTag(name) {
        var _a, _b;
        const cell = (_a = this.tracker) === null || _a === void 0 ? void 0 : _a.activeCell;
        if (cell) {
            const oldTags = [
                ...((_b = cell.model.metadata.get('tags')) !== null && _b !== void 0 ? _b : [])
            ];
            let tagsToAdd = name.split(/[,\s]+/);
            tagsToAdd = tagsToAdd.filter(tag => tag !== '' && !oldTags.includes(tag));
            cell.model.metadata.set('tags', oldTags.concat(tagsToAdd));
            this.refreshTags();
            this.loadActiveTags();
        }
    }
    /**
     * Remove a tag from the current active cell.
     *
     * @param name - The name of the tag.
     */
    removeTag(name) {
        var _a, _b;
        const cell = (_a = this.tracker) === null || _a === void 0 ? void 0 : _a.activeCell;
        if (cell) {
            const oldTags = [
                ...((_b = cell.model.metadata.get('tags')) !== null && _b !== void 0 ? _b : [])
            ];
            let tags = oldTags.filter(tag => tag !== name);
            cell.model.metadata.set('tags', tags);
            if (tags.length === 0) {
                cell.model.metadata.delete('tags');
            }
            this.refreshTags();
            this.loadActiveTags();
        }
    }
    /**
     * Update each tag widget to represent whether it is applied to the current
     * active cell.
     */
    loadActiveTags() {
        const layout = this.layout;
        for (const widget of layout.widgets) {
            widget.update();
        }
    }
    /**
     * Pull from cell metadata all the tags used in the notebook and update the
     * stored tag list.
     */
    pullTags() {
        var _a, _b, _c;
        const notebook = (_a = this.tracker) === null || _a === void 0 ? void 0 : _a.currentWidget;
        const cells = (_c = (_b = notebook === null || notebook === void 0 ? void 0 : notebook.model) === null || _b === void 0 ? void 0 : _b.cells) !== null && _c !== void 0 ? _c : [];
        const allTags = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.reduce)(cells, (allTags, cell) => {
            var _a;
            const tags = (_a = cell.metadata.get('tags')) !== null && _a !== void 0 ? _a : [];
            return [...allTags, ...tags];
        }, []);
        this.tagList = [...new Set(allTags)].filter(tag => tag !== '');
    }
    /**
     * Pull the most recent list of tags and update the tag widgets - dispose if
     * the tag no longer exists, and create new widgets for new tags.
     */
    refreshTags() {
        this.pullTags();
        const layout = this.layout;
        const tagWidgets = layout.widgets.filter(w => w.id !== 'add-tag');
        tagWidgets.forEach(widget => {
            if (!this.tagList.includes(widget.name)) {
                widget.dispose();
            }
        });
        const tagWidgetNames = tagWidgets.map(w => w.name);
        this.tagList.forEach(tag => {
            if (!tagWidgetNames.includes(tag)) {
                const idx = layout.widgets.length - 1;
                layout.insertWidget(idx, new _widget__WEBPACK_IMPORTED_MODULE_5__.TagWidget(tag));
            }
        });
    }
    /**
     * Validate the 'tags' of cell metadata, ensuring it is a list of strings and
     * that each string doesn't include spaces.
     */
    validateTags(cell, tags) {
        tags = tags.filter(tag => typeof tag === 'string');
        tags = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.reduce)(tags, (allTags, tag) => {
            return [...allTags, ...tag.split(/[,\s]+/)];
        }, []);
        const validTags = [...new Set(tags)].filter(tag => tag !== '');
        cell.model.metadata.set('tags', validTags);
        this.refreshTags();
        this.loadActiveTags();
    }
    /**
     * Handle a change to the active cell.
     */
    onActiveCellChanged() {
        this.loadActiveTags();
    }
    /**
     * Get all tags once available.
     */
    onAfterShow() {
        this.refreshTags();
        this.loadActiveTags();
    }
    /**
     * Upon attach, add label if it doesn't already exist and listen for changes
     * from the notebook tracker.
     */
    onAfterAttach() {
        if (!this.label) {
            const label = document.createElement('label');
            label.textContent = this._trans.__('Cell Tags');
            label.className = 'tag-label';
            this.parent.node.insertBefore(label, this.node);
            this.label = true;
        }
        if (this.tracker.currentWidget) {
            void this.tracker.currentWidget.context.ready.then(() => {
                this.refreshTags();
                this.loadActiveTags();
            });
            this.tracker.currentWidget.model.cells.changed.connect(() => {
                this.refreshTags();
                this.loadActiveTags();
            });
            this.tracker.currentWidget.content.activeCellChanged.connect(() => {
                this.refreshTags();
                this.loadActiveTags();
            });
        }
        this.tracker.currentChanged.connect(() => {
            this.refreshTags();
            this.loadActiveTags();
        });
    }
    /**
     * Handle a change to active cell metadata.
     */
    onActiveCellMetadataChanged() {
        const tags = this.tracker.activeCell.model.metadata.get('tags');
        let taglist = [];
        if (tags) {
            if (typeof tags === 'string') {
                taglist.push(tags);
            }
            else {
                taglist = tags;
            }
        }
        this.validateTags(this.tracker.activeCell, taglist);
    }
}


/***/ }),

/***/ "../packages/celltags/lib/widget.js":
/*!******************************************!*\
  !*** ../packages/celltags/lib/widget.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TagWidget": () => (/* binding */ TagWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);


/**
 * A widget which hosts a cell tags area.
 */
class TagWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
     * Construct a new tag widget.
     */
    constructor(name) {
        super();
        this.parent = null;
        this.applied = true;
        this.name = name;
        this.addClass('tag');
        this.buildTag();
    }
    /**
     * Create tag div with icon and attach to this.node.
     */
    buildTag() {
        const text = document.createElement('span');
        text.textContent = this.name;
        text.style.textOverflow = 'ellipsis';
        const tag = document.createElement('div');
        tag.className = 'tag-holder';
        tag.appendChild(text);
        const iconContainer = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.checkIcon.element({
            tag: 'span',
            elementPosition: 'center',
            height: '18px',
            width: '18px',
            marginLeft: '5px',
            marginRight: '-3px'
        });
        if (this.applied) {
            this.addClass('applied-tag');
        }
        else {
            this.addClass('unapplied-tag');
            iconContainer.style.display = 'none';
        }
        tag.appendChild(iconContainer);
        this.node.appendChild(tag);
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach() {
        this.node.addEventListener('mousedown', this);
        this.node.addEventListener('mouseover', this);
        this.node.addEventListener('mouseout', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach() {
        this.node.removeEventListener('mousedown', this);
        this.node.removeEventListener('mouseover', this);
        this.node.removeEventListener('mouseout', this);
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'mousedown':
                this._evtClick();
                break;
            case 'mouseover':
                this._evtMouseOver();
                break;
            case 'mouseout':
                this._evtMouseOut();
                break;
            default:
                break;
        }
    }
    /**
     * Handle `update-request` messages. Check if applied to current active cell.
     */
    onUpdateRequest() {
        var _a;
        const applied = (_a = this.parent) === null || _a === void 0 ? void 0 : _a.checkApplied(this.name);
        if (applied !== this.applied) {
            this.toggleApplied();
        }
    }
    /**
     * Update styling to reflect whether tag is applied to current active cell.
     */
    toggleApplied() {
        var _a, _b;
        if (this.applied) {
            this.removeClass('applied-tag');
            ((_a = this.node.firstChild) === null || _a === void 0 ? void 0 : _a.lastChild).style.display =
                'none';
            this.addClass('unapplied-tag');
        }
        else {
            this.removeClass('unapplied-tag');
            ((_b = this.node.firstChild) === null || _b === void 0 ? void 0 : _b.lastChild).style.display =
                'inline-block';
            this.addClass('applied-tag');
        }
        this.applied = !this.applied;
    }
    /**
     * Handle the `'click'` event for the widget.
     */
    _evtClick() {
        var _a, _b;
        if (this.applied) {
            (_a = this.parent) === null || _a === void 0 ? void 0 : _a.removeTag(this.name);
        }
        else {
            (_b = this.parent) === null || _b === void 0 ? void 0 : _b.addTag(this.name);
        }
        this.toggleApplied();
    }
    /**
     * Handle the `'mouseover'` event for the widget.
     */
    _evtMouseOver() {
        this.node.classList.add('tag-hover');
    }
    /**
     * Handle the `'mouseout'` event for the widget.
     */
    _evtMouseOut() {
        this.node.classList.remove('tag-hover');
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY2VsbHRhZ3Mvc3JjL2FkZHdpZGdldC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY2VsbHRhZ3Mvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jZWxsdGFncy9zcmMvdG9vbC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY2VsbHRhZ3Mvc3JjL3dpZGdldC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBSWlDO0FBQ21CO0FBQ1g7QUFHekM7O0dBRUc7QUFDSSxNQUFNLFNBQVUsU0FBUSxtREFBTTtJQUNuQzs7T0FFRztJQUNILFlBQVksVUFBd0I7UUFDbEMsS0FBSyxFQUFFLENBQUM7UUFrSkgsV0FBTSxHQUFtQixJQUFJLENBQUM7UUFFN0IsVUFBSyxHQUFxQixRQUFRLENBQUMsYUFBYSxDQUFDLE9BQU8sQ0FBQyxDQUFDO1FBbkpoRSxJQUFJLENBQUMsVUFBVSxHQUFHLFVBQVUsSUFBSSxtRUFBYyxDQUFDO1FBQy9DLElBQUksQ0FBQyxNQUFNLEdBQUcsSUFBSSxDQUFDLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7UUFDakQsSUFBSSxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsQ0FBQztRQUNyQixJQUFJLENBQUMsT0FBTyxHQUFHLEtBQUssQ0FBQztRQUNyQixJQUFJLENBQUMsUUFBUSxFQUFFLENBQUM7SUFDbEIsQ0FBQztJQUVEOztPQUVHO0lBQ0gsUUFBUTtRQUNOLE1BQU0sSUFBSSxHQUFHLElBQUksQ0FBQyxLQUFLLElBQUksUUFBUSxDQUFDLGFBQWEsQ0FBQyxPQUFPLENBQUMsQ0FBQztRQUMzRCxJQUFJLENBQUMs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QUFNLENBQUMsV0FBVyxDQUFDLENBQUM7SUFDM0QsQ0FBQztDQUtGIiwiZmlsZSI6InBhY2thZ2VzX2NlbGx0YWdzX2xpYl9pbmRleF9qcy5iOGE2NzNlMmQ3ZDUxYWFlYWIzOS5qcyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgYWRkSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IFRhZ1Rvb2wgfSBmcm9tICcuL3Rvb2wnO1xuXG4vKipcbiAqIEEgd2lkZ2V0IHdoaWNoIGhvc3RzIGEgY2VsbCB0YWdzIGFyZWEuXG4gKi9cbmV4cG9ydCBjbGFzcyBBZGRXaWRnZXQgZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IHRhZyB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3Rvcih0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3IpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5fdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ3RhZycpO1xuICAgIHRoaXMuZWRpdGluZyA9IGZhbHNlO1xuICAgIHRoaXMuYnVpbGRUYWcoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgaW5wdXQgYm94IHdpdGggaWNvbiBhbmQgYXR0YWNoIHRvIHRoaXMubm9kZS5cbiAgICovXG4gIGJ1aWxkVGFnKCkge1xuICAgIGNvbnN0IHRleHQgPSB0aGlzLmlucHV0IHx8IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2lucHV0Jyk7XG4gICAgdGV4dC52YWx1ZSA9IHRoaXMuX3RyYW5zLl9fKCdBZGQgVGFnJyk7XG4gICAgdGV4dC5jb250ZW50RWRpdGFibGUgPSAndHJ1ZSc7XG4gICAgdGV4dC5jbGFzc05hbWUgPSAnYWRkLXRhZyc7XG4gICAgdGV4dC5zdHlsZS53aWR0aCA9ICc0OXB4JztcbiAgICB0aGlzLmlucHV0ID0gdGV4dDtcbiAgICBjb25zdCB0YWcgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICB0YWcuY2xhc3NOYW1lID0gJ3RhZy1ob2xkZXInO1xuICAgIHRhZy5hcHBlbmRDaGlsZCh0ZXh0KTtcbiAgICBjb25zdCBpY29uQ29udGFpbmVyID0gYWRkSWNvbi5lbGVtZW50KHtcbiAgICAgIHRhZzogJ3NwYW4nLFxuICAgICAgZWxlbWVudFBvc2l0aW9uOiAnY2VudGVyJyxcbiAgICAgIGhlaWdodDogJzE4cHgnLFxuICAgICAgd2lkdGg6ICcxOHB4JyxcbiAgICAgIG1hcmdpbkxlZnQ6ICczcHgnLFxuICAgICAgbWFyZ2luUmlnaHQ6ICctNXB4J1xuICAgIH0pO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ3VuYXBwbGllZC10YWcnKTtcbiAgICB0YWcuYXBwZW5kQ2hpbGQoaWNvbkNvbnRhaW5lcik7XG4gICAgdGhpcy5ub2RlLmFwcGVuZENoaWxkKHRhZyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBhZnRlci1hdHRhY2hgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgb25BZnRlckF0dGFjaCgpIHtcbiAgICB0aGlzLm5vZGUuYWRkRXZlbnRMaXN0ZW5lcignbW91c2Vkb3duJywgdGhpcyk7XG4gICAgdGhpcy5pbnB1dC5hZGRFdmVudExpc3RlbmVyKCdrZXlkb3duJywgdGhpcyk7XG4gICAgdGhpcy5pbnB1dC5hZGRFdmVudExpc3RlbmVyKCdmb2N1cycsIHRoaXMpO1xuICAgIHRoaXMuaW5wdXQuYWRkRXZlbnRMaXN0ZW5lcignYmx1cicsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYmVmb3JlLWRldGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBvbkJlZm9yZURldGFjaCgpIHtcbiAgICB0aGlzLm5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignbW91c2Vkb3duJywgdGhpcyk7XG4gICAgdGhpcy5pbnB1dC5yZW1vdmVFdmVudExpc3RlbmVyKCdrZXlkb3duJywgdGhpcyk7XG4gICAgdGhpcy5pbnB1dC5yZW1vdmVFdmVudExpc3RlbmVyKCdmb2N1cycsIHRoaXMpO1xuICAgIHRoaXMuaW5wdXQucmVtb3ZlRXZlbnRMaXN0ZW5lcignYmx1cicsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgRE9NIGV2ZW50cyBmb3IgdGhlIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIGV2ZW50IC0gVGhlIERPTSBldmVudCBzZW50IHRvIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgaW1wbGVtZW50cyB0aGUgRE9NIGBFdmVudExpc3RlbmVyYCBpbnRlcmZhY2UgYW5kIGlzXG4gICAqIGNhbGxlZCBpbiByZXNwb25zZSB0byBldmVudHMgb24gdGhlIGRvY2sgcGFuZWwncyBub2RlLiBJdCBzaG91bGRcbiAgICogbm90IGJlIGNhbGxlZCBkaXJlY3RseSBieSB1c2VyIGNvZGUuXG4gICAqL1xuICBoYW5kbGVFdmVudChldmVudDogRXZlbnQpOiB2b2lkIHtcbiAgICBzd2l0Y2ggKGV2ZW50LnR5cGUpIHtcbiAgICAgIGNhc2UgJ21vdXNlZG93bic6XG4gICAgICAgIHRoaXMuX2V2dE1vdXNlRG93bihldmVudCBhcyBNb3VzZUV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdrZXlkb3duJzpcbiAgICAgICAgdGhpcy5fZXZ0S2V5RG93bihldmVudCBhcyBLZXlib2FyZEV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdibHVyJzpcbiAgICAgICAgdGhpcy5fZXZ0Qmx1cigpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2ZvY3VzJzpcbiAgICAgICAgdGhpcy5fZXZ0Rm9jdXMoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBgJ21vdXNlZG93bidgIGV2ZW50IGZvciB0aGUgaW5wdXQgYm94LlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldFxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0TW91c2VEb3duKGV2ZW50OiBNb3VzZUV2ZW50KSB7XG4gICAgaWYgKCF0aGlzLmVkaXRpbmcpIHtcbiAgICAgIHRoaXMuZWRpdGluZyA9IHRydWU7XG4gICAgICB0aGlzLmlucHV0LnZhbHVlID0gJyc7XG4gICAgICB0aGlzLmlucHV0LmZvY3VzKCk7XG4gICAgfSBlbHNlIGlmIChldmVudC50YXJnZXQgIT09IHRoaXMuaW5wdXQpIHtcbiAgICAgIGlmICh0aGlzLmlucHV0LnZhbHVlICE9PSAnJykge1xuICAgICAgICBjb25zdCB2YWx1ZSA9IHRoaXMuaW5wdXQudmFsdWU7XG4gICAgICAgICh0aGlzLnBhcmVudCBhcyBUYWdUb29sKS5hZGRUYWcodmFsdWUpO1xuICAgICAgICB0aGlzLmlucHV0LmJsdXIoKTtcbiAgICAgICAgdGhpcy5fZXZ0Qmx1cigpO1xuICAgICAgfVxuICAgIH1cbiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgYCdmb2N1cydgIGV2ZW50IGZvciB0aGUgaW5wdXQgYm94LlxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0Rm9jdXMoKSB7XG4gICAgaWYgKCF0aGlzLmVkaXRpbmcpIHtcbiAgICAgIHRoaXMuaW5wdXQuYmx1cigpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGAna2V5ZG93bidgIGV2ZW50IGZvciB0aGUgaW5wdXQgYm94LlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldFxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0S2V5RG93bihldmVudDogS2V5Ym9hcmRFdmVudCkge1xuICAgIGNvbnN0IHRtcCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ3NwYW4nKTtcbiAgICB0bXAuY2xhc3NOYW1lID0gJ2FkZC10YWcnO1xuICAgIHRtcC5pbm5lckhUTUwgPSB0aGlzLmlucHV0LnZhbHVlO1xuICAgIC8vIHNldCB3aWR0aCB0byB0aGUgcGl4ZWwgbGVuZ3RoIG9mIHRoZSB0ZXh0XG4gICAgZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZCh0bXApO1xuICAgIHRoaXMuaW5wdXQuc3R5bGUud2lkdGggPSB0bXAuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCkud2lkdGggKyA4ICsgJ3B4JztcbiAgICBkb2N1bWVudC5ib2R5LnJlbW92ZUNoaWxkKHRtcCk7XG4gICAgLy8gaWYgdGhleSBoaXQgRW50ZXIsIGFkZCB0aGUgdGFnIGFuZCByZXNldCBzdGF0ZVxuICAgIGlmIChldmVudC5rZXlDb2RlID09PSAxMykge1xuICAgICAgY29uc3QgdmFsdWUgPSB0aGlzLmlucHV0LnZhbHVlO1xuICAgICAgKHRoaXMucGFyZW50IGFzIFRhZ1Rvb2wpLmFkZFRhZyh2YWx1ZSk7XG4gICAgICB0aGlzLmlucHV0LmJsdXIoKTtcbiAgICAgIHRoaXMuX2V2dEJsdXIoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBgJ2ZvY3Vzb3V0J2AgZXZlbnQgZm9yIHRoZSBpbnB1dCBib3guXG4gICAqL1xuICBwcml2YXRlIF9ldnRCbHVyKCkge1xuICAgIGlmICh0aGlzLmVkaXRpbmcpIHtcbiAgICAgIHRoaXMuZWRpdGluZyA9IGZhbHNlO1xuICAgICAgdGhpcy5pbnB1dC52YWx1ZSA9IHRoaXMuX3RyYW5zLl9fKCdBZGQgVGFnJyk7XG4gICAgICB0aGlzLmlucHV0LnN0eWxlLndpZHRoID0gJzQ5cHgnO1xuICAgIH1cbiAgfVxuXG4gIHB1YmxpYyBwYXJlbnQ6IFRhZ1Rvb2wgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBlZGl0aW5nOiBib29sZWFuO1xuICBwcml2YXRlIGlucHV0OiBIVE1MSW5wdXRFbGVtZW50ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaW5wdXQnKTtcbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF90cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBjZWxsdGFnc1xuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vYWRkd2lkZ2V0JztcbmV4cG9ydCAqIGZyb20gJy4vdG9vbCc7XG5leHBvcnQgKiBmcm9tICcuL3dpZGdldCc7XG4iLCJpbXBvcnQgeyBKdXB5dGVyRnJvbnRFbmQgfSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBDZWxsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY2VsbHMnO1xuaW1wb3J0IHsgSU5vdGVib29rVHJhY2tlciwgTm90ZWJvb2tUb29scyB9IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgcmVkdWNlIH0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHsgUGFuZWxMYXlvdXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgQWRkV2lkZ2V0IH0gZnJvbSAnLi9hZGR3aWRnZXQnO1xuaW1wb3J0IHsgVGFnV2lkZ2V0IH0gZnJvbSAnLi93aWRnZXQnO1xuXG4vKipcbiAqIEEgVG9vbCBmb3IgdGFnIG9wZXJhdGlvbnMuXG4gKi9cbmV4cG9ydCBjbGFzcyBUYWdUb29sIGV4dGVuZHMgTm90ZWJvb2tUb29scy5Ub29sIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyB0YWcgVG9vbC5cbiAgICpcbiAgICogQHBhcmFtIHRyYWNrZXIgLSBUaGUgbm90ZWJvb2sgdHJhY2tlci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKFxuICAgIHRyYWNrZXI6IElOb3RlYm9va1RyYWNrZXIsXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yXG4gICkge1xuICAgIHN1cGVyKCk7XG4gICAgYXBwO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5fdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIHRoaXMudHJhY2tlciA9IHRyYWNrZXI7XG4gICAgdGhpcy5sYXlvdXQgPSBuZXcgUGFuZWxMYXlvdXQoKTtcbiAgICB0aGlzLmNyZWF0ZVRhZ0lucHV0KCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtVGFnVG9vbCcpO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhbiBBZGRXaWRnZXQgaW5wdXQgYm94IHRvIHRoZSBsYXlvdXQuXG4gICAqL1xuICBjcmVhdGVUYWdJbnB1dCgpIHtcbiAgICBjb25zdCBsYXlvdXQgPSB0aGlzLmxheW91dCBhcyBQYW5lbExheW91dDtcbiAgICBjb25zdCBpbnB1dCA9IG5ldyBBZGRXaWRnZXQodGhpcy50cmFuc2xhdG9yKTtcbiAgICBpbnB1dC5pZCA9ICdhZGQtdGFnJztcbiAgICBsYXlvdXQuaW5zZXJ0V2lkZ2V0KDAsIGlucHV0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDaGVjayB3aGV0aGVyIGEgdGFnIGlzIGFwcGxpZWQgdG8gdGhlIGN1cnJlbnQgYWN0aXZlIGNlbGxcbiAgICpcbiAgICogQHBhcmFtIG5hbWUgLSBUaGUgbmFtZSBvZiB0aGUgdGFnLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGJvb2xlYW4gcmVwcmVzZW50aW5nIHdoZXRoZXIgaXQgaXMgYXBwbGllZC5cbiAgICovXG4gIGNoZWNrQXBwbGllZChuYW1lOiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICBjb25zdCBhY3RpdmVDZWxsID0gdGhpcy50cmFja2VyPy5hY3RpdmVDZWxsO1xuICAgIGlmIChhY3RpdmVDZWxsKSB7XG4gICAgICBjb25zdCB0YWdzID0gYWN0aXZlQ2VsbC5tb2RlbC5tZXRhZGF0YS5nZXQoJ3RhZ3MnKSBhcyBzdHJpbmdbXTtcbiAgICAgIGlmICh0YWdzKSB7XG4gICAgICAgIHJldHVybiB0YWdzLmluY2x1ZGVzKG5hbWUpO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgdGFnIHRvIHRoZSBjdXJyZW50IGFjdGl2ZSBjZWxsLlxuICAgKlxuICAgKiBAcGFyYW0gbmFtZSAtIFRoZSBuYW1lIG9mIHRoZSB0YWcuXG4gICAqL1xuICBhZGRUYWcobmFtZTogc3RyaW5nKSB7XG4gICAgY29uc3QgY2VsbCA9IHRoaXMudHJhY2tlcj8uYWN0aXZlQ2VsbDtcbiAgICBpZiAoY2VsbCkge1xuICAgICAgY29uc3Qgb2xkVGFncyA9IFtcbiAgICAgICAgLi4uKChjZWxsLm1vZGVsLm1ldGFkYXRhLmdldCgndGFncycpIGFzIHN0cmluZ1tdKSA/PyBbXSlcbiAgICAgIF07XG4gICAgICBsZXQgdGFnc1RvQWRkID0gbmFtZS5zcGxpdCgvWyxcXHNdKy8pO1xuICAgICAgdGFnc1RvQWRkID0gdGFnc1RvQWRkLmZpbHRlcih0YWcgPT4gdGFnICE9PSAnJyAmJiAhb2xkVGFncy5pbmNsdWRlcyh0YWcpKTtcbiAgICAgIGNlbGwubW9kZWwubWV0YWRhdGEuc2V0KCd0YWdzJywgb2xkVGFncy5jb25jYXQodGFnc1RvQWRkKSk7XG4gICAgICB0aGlzLnJlZnJlc2hUYWdzKCk7XG4gICAgICB0aGlzLmxvYWRBY3RpdmVUYWdzKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhIHRhZyBmcm9tIHRoZSBjdXJyZW50IGFjdGl2ZSBjZWxsLlxuICAgKlxuICAgKiBAcGFyYW0gbmFtZSAtIFRoZSBuYW1lIG9mIHRoZSB0YWcuXG4gICAqL1xuICByZW1vdmVUYWcobmFtZTogc3RyaW5nKSB7XG4gICAgY29uc3QgY2VsbCA9IHRoaXMudHJhY2tlcj8uYWN0aXZlQ2VsbDtcbiAgICBpZiAoY2VsbCkge1xuICAgICAgY29uc3Qgb2xkVGFncyA9IFtcbiAgICAgICAgLi4uKChjZWxsLm1vZGVsLm1ldGFkYXRhLmdldCgndGFncycpIGFzIHN0cmluZ1tdKSA/PyBbXSlcbiAgICAgIF07XG4gICAgICBsZXQgdGFncyA9IG9sZFRhZ3MuZmlsdGVyKHRhZyA9PiB0YWcgIT09IG5hbWUpO1xuICAgICAgY2VsbC5tb2RlbC5tZXRhZGF0YS5zZXQoJ3RhZ3MnLCB0YWdzKTtcbiAgICAgIGlmICh0YWdzLmxlbmd0aCA9PT0gMCkge1xuICAgICAgICBjZWxsLm1vZGVsLm1ldGFkYXRhLmRlbGV0ZSgndGFncycpO1xuICAgICAgfVxuICAgICAgdGhpcy5yZWZyZXNoVGFncygpO1xuICAgICAgdGhpcy5sb2FkQWN0aXZlVGFncygpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBVcGRhdGUgZWFjaCB0YWcgd2lkZ2V0IHRvIHJlcHJlc2VudCB3aGV0aGVyIGl0IGlzIGFwcGxpZWQgdG8gdGhlIGN1cnJlbnRcbiAgICogYWN0aXZlIGNlbGwuXG4gICAqL1xuICBsb2FkQWN0aXZlVGFncygpIHtcbiAgICBjb25zdCBsYXlvdXQgPSB0aGlzLmxheW91dCBhcyBQYW5lbExheW91dDtcbiAgICBmb3IgKGNvbnN0IHdpZGdldCBvZiBsYXlvdXQud2lkZ2V0cykge1xuICAgICAgd2lkZ2V0LnVwZGF0ZSgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBQdWxsIGZyb20gY2VsbCBtZXRhZGF0YSBhbGwgdGhlIHRhZ3MgdXNlZCBpbiB0aGUgbm90ZWJvb2sgYW5kIHVwZGF0ZSB0aGVcbiAgICogc3RvcmVkIHRhZyBsaXN0LlxuICAgKi9cbiAgcHVsbFRhZ3MoKSB7XG4gICAgY29uc3Qgbm90ZWJvb2sgPSB0aGlzLnRyYWNrZXI/LmN1cnJlbnRXaWRnZXQ7XG4gICAgY29uc3QgY2VsbHMgPSBub3RlYm9vaz8ubW9kZWw/LmNlbGxzID8/IFtdO1xuICAgIGNvbnN0IGFsbFRhZ3MgPSByZWR1Y2UoXG4gICAgICBjZWxscyxcbiAgICAgIChhbGxUYWdzOiBzdHJpbmdbXSwgY2VsbCkgPT4ge1xuICAgICAgICBjb25zdCB0YWdzID0gKGNlbGwubWV0YWRhdGEuZ2V0KCd0YWdzJykgYXMgc3RyaW5nW10pID8/IFtdO1xuICAgICAgICByZXR1cm4gWy4uLmFsbFRhZ3MsIC4uLnRhZ3NdO1xuICAgICAgfSxcbiAgICAgIFtdXG4gICAgKTtcbiAgICB0aGlzLnRhZ0xpc3QgPSBbLi4ubmV3IFNldChhbGxUYWdzKV0uZmlsdGVyKHRhZyA9PiB0YWcgIT09ICcnKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBQdWxsIHRoZSBtb3N0IHJlY2VudCBsaXN0IG9mIHRhZ3MgYW5kIHVwZGF0ZSB0aGUgdGFnIHdpZGdldHMgLSBkaXNwb3NlIGlmXG4gICAqIHRoZSB0YWcgbm8gbG9uZ2VyIGV4aXN0cywgYW5kIGNyZWF0ZSBuZXcgd2lkZ2V0cyBmb3IgbmV3IHRhZ3MuXG4gICAqL1xuICByZWZyZXNoVGFncygpIHtcbiAgICB0aGlzLnB1bGxUYWdzKCk7XG4gICAgY29uc3QgbGF5b3V0ID0gdGhpcy5sYXlvdXQgYXMgUGFuZWxMYXlvdXQ7XG4gICAgY29uc3QgdGFnV2lkZ2V0cyA9IGxheW91dC53aWRnZXRzLmZpbHRlcih3ID0+IHcuaWQgIT09ICdhZGQtdGFnJyk7XG4gICAgdGFnV2lkZ2V0cy5mb3JFYWNoKHdpZGdldCA9PiB7XG4gICAgICBpZiAoIXRoaXMudGFnTGlzdC5pbmNsdWRlcygod2lkZ2V0IGFzIFRhZ1dpZGdldCkubmFtZSkpIHtcbiAgICAgICAgd2lkZ2V0LmRpc3Bvc2UoKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgICBjb25zdCB0YWdXaWRnZXROYW1lcyA9IHRhZ1dpZGdldHMubWFwKHcgPT4gKHcgYXMgVGFnV2lkZ2V0KS5uYW1lKTtcbiAgICB0aGlzLnRhZ0xpc3QuZm9yRWFjaCh0YWcgPT4ge1xuICAgICAgaWYgKCF0YWdXaWRnZXROYW1lcy5pbmNsdWRlcyh0YWcpKSB7XG4gICAgICAgIGNvbnN0IGlkeCA9IGxheW91dC53aWRnZXRzLmxlbmd0aCAtIDE7XG4gICAgICAgIGxheW91dC5pbnNlcnRXaWRnZXQoaWR4LCBuZXcgVGFnV2lkZ2V0KHRhZykpO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFZhbGlkYXRlIHRoZSAndGFncycgb2YgY2VsbCBtZXRhZGF0YSwgZW5zdXJpbmcgaXQgaXMgYSBsaXN0IG9mIHN0cmluZ3MgYW5kXG4gICAqIHRoYXQgZWFjaCBzdHJpbmcgZG9lc24ndCBpbmNsdWRlIHNwYWNlcy5cbiAgICovXG4gIHZhbGlkYXRlVGFncyhjZWxsOiBDZWxsLCB0YWdzOiBzdHJpbmdbXSkge1xuICAgIHRhZ3MgPSB0YWdzLmZpbHRlcih0YWcgPT4gdHlwZW9mIHRhZyA9PT0gJ3N0cmluZycpO1xuICAgIHRhZ3MgPSByZWR1Y2UoXG4gICAgICB0YWdzLFxuICAgICAgKGFsbFRhZ3M6IHN0cmluZ1tdLCB0YWcpID0+IHtcbiAgICAgICAgcmV0dXJuIFsuLi5hbGxUYWdzLCAuLi50YWcuc3BsaXQoL1ssXFxzXSsvKV07XG4gICAgICB9LFxuICAgICAgW11cbiAgICApO1xuICAgIGNvbnN0IHZhbGlkVGFncyA9IFsuLi5uZXcgU2V0KHRhZ3MpXS5maWx0ZXIodGFnID0+IHRhZyAhPT0gJycpO1xuICAgIGNlbGwubW9kZWwubWV0YWRhdGEuc2V0KCd0YWdzJywgdmFsaWRUYWdzKTtcbiAgICB0aGlzLnJlZnJlc2hUYWdzKCk7XG4gICAgdGhpcy5sb2FkQWN0aXZlVGFncygpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgYWN0aXZlIGNlbGwuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmVDZWxsQ2hhbmdlZCgpOiB2b2lkIHtcbiAgICB0aGlzLmxvYWRBY3RpdmVUYWdzKCk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGFsbCB0YWdzIG9uY2UgYXZhaWxhYmxlLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJTaG93KCkge1xuICAgIHRoaXMucmVmcmVzaFRhZ3MoKTtcbiAgICB0aGlzLmxvYWRBY3RpdmVUYWdzKCk7XG4gIH1cblxuICAvKipcbiAgICogVXBvbiBhdHRhY2gsIGFkZCBsYWJlbCBpZiBpdCBkb2Vzbid0IGFscmVhZHkgZXhpc3QgYW5kIGxpc3RlbiBmb3IgY2hhbmdlc1xuICAgKiBmcm9tIHRoZSBub3RlYm9vayB0cmFja2VyLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2goKSB7XG4gICAgaWYgKCF0aGlzLmxhYmVsKSB7XG4gICAgICBjb25zdCBsYWJlbCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2xhYmVsJyk7XG4gICAgICBsYWJlbC50ZXh0Q29udGVudCA9IHRoaXMuX3RyYW5zLl9fKCdDZWxsIFRhZ3MnKTtcbiAgICAgIGxhYmVsLmNsYXNzTmFtZSA9ICd0YWctbGFiZWwnO1xuICAgICAgdGhpcy5wYXJlbnQhLm5vZGUuaW5zZXJ0QmVmb3JlKGxhYmVsLCB0aGlzLm5vZGUpO1xuICAgICAgdGhpcy5sYWJlbCA9IHRydWU7XG4gICAgfVxuICAgIGlmICh0aGlzLnRyYWNrZXIuY3VycmVudFdpZGdldCkge1xuICAgICAgdm9pZCB0aGlzLnRyYWNrZXIuY3VycmVudFdpZGdldC5jb250ZXh0LnJlYWR5LnRoZW4oKCkgPT4ge1xuICAgICAgICB0aGlzLnJlZnJlc2hUYWdzKCk7XG4gICAgICAgIHRoaXMubG9hZEFjdGl2ZVRhZ3MoKTtcbiAgICAgIH0pO1xuICAgICAgdGhpcy50cmFja2VyLmN1cnJlbnRXaWRnZXQubW9kZWwhLmNlbGxzLmNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgIHRoaXMucmVmcmVzaFRhZ3MoKTtcbiAgICAgICAgdGhpcy5sb2FkQWN0aXZlVGFncygpO1xuICAgICAgfSk7XG4gICAgICB0aGlzLnRyYWNrZXIuY3VycmVudFdpZGdldC5jb250ZW50LmFjdGl2ZUNlbGxDaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICB0aGlzLnJlZnJlc2hUYWdzKCk7XG4gICAgICAgIHRoaXMubG9hZEFjdGl2ZVRhZ3MoKTtcbiAgICAgIH0pO1xuICAgIH1cbiAgICB0aGlzLnRyYWNrZXIuY3VycmVudENoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICB0aGlzLnJlZnJlc2hUYWdzKCk7XG4gICAgICB0aGlzLmxvYWRBY3RpdmVUYWdzKCk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIGFjdGl2ZSBjZWxsIG1ldGFkYXRhLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWN0aXZlQ2VsbE1ldGFkYXRhQ2hhbmdlZCgpOiB2b2lkIHtcbiAgICBjb25zdCB0YWdzID0gdGhpcy50cmFja2VyLmFjdGl2ZUNlbGwhLm1vZGVsLm1ldGFkYXRhLmdldChcbiAgICAgICd0YWdzJ1xuICAgICkgYXMgc3RyaW5nW107XG4gICAgbGV0IHRhZ2xpc3Q6IHN0cmluZ1tdID0gW107XG4gICAgaWYgKHRhZ3MpIHtcbiAgICAgIGlmICh0eXBlb2YgdGFncyA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgdGFnbGlzdC5wdXNoKHRhZ3MpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgdGFnbGlzdCA9IHRhZ3MgYXMgc3RyaW5nW107XG4gICAgICB9XG4gICAgfVxuICAgIHRoaXMudmFsaWRhdGVUYWdzKHRoaXMudHJhY2tlci5hY3RpdmVDZWxsISwgdGFnbGlzdCk7XG4gIH1cblxuICBwdWJsaWMgdHJhY2tlcjogSU5vdGVib29rVHJhY2tlcjtcbiAgcHJpdmF0ZSB0YWdMaXN0OiBzdHJpbmdbXSA9IFtdO1xuICBwcml2YXRlIGxhYmVsOiBib29sZWFuID0gZmFsc2U7XG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xufVxuIiwiaW1wb3J0IHsgY2hlY2tJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgVGFnVG9vbCB9IGZyb20gJy4vdG9vbCc7XG5cbi8qKlxuICogQSB3aWRnZXQgd2hpY2ggaG9zdHMgYSBjZWxsIHRhZ3MgYXJlYS5cbiAqL1xuZXhwb3J0IGNsYXNzIFRhZ1dpZGdldCBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgdGFnIHdpZGdldC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG5hbWU6IHN0cmluZykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hcHBsaWVkID0gdHJ1ZTtcbiAgICB0aGlzLm5hbWUgPSBuYW1lO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ3RhZycpO1xuICAgIHRoaXMuYnVpbGRUYWcoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgdGFnIGRpdiB3aXRoIGljb24gYW5kIGF0dGFjaCB0byB0aGlzLm5vZGUuXG4gICAqL1xuICBidWlsZFRhZygpIHtcbiAgICBjb25zdCB0ZXh0ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnc3BhbicpO1xuICAgIHRleHQudGV4dENvbnRlbnQgPSB0aGlzLm5hbWU7XG4gICAgdGV4dC5zdHlsZS50ZXh0T3ZlcmZsb3cgPSAnZWxsaXBzaXMnO1xuICAgIGNvbnN0IHRhZyA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIHRhZy5jbGFzc05hbWUgPSAndGFnLWhvbGRlcic7XG4gICAgdGFnLmFwcGVuZENoaWxkKHRleHQpO1xuICAgIGNvbnN0IGljb25Db250YWluZXIgPSBjaGVja0ljb24uZWxlbWVudCh7XG4gICAgICB0YWc6ICdzcGFuJyxcbiAgICAgIGVsZW1lbnRQb3NpdGlvbjogJ2NlbnRlcicsXG4gICAgICBoZWlnaHQ6ICcxOHB4JyxcbiAgICAgIHdpZHRoOiAnMThweCcsXG4gICAgICBtYXJnaW5MZWZ0OiAnNXB4JyxcbiAgICAgIG1hcmdpblJpZ2h0OiAnLTNweCdcbiAgICB9KTtcbiAgICBpZiAodGhpcy5hcHBsaWVkKSB7XG4gICAgICB0aGlzLmFkZENsYXNzKCdhcHBsaWVkLXRhZycpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLmFkZENsYXNzKCd1bmFwcGxpZWQtdGFnJyk7XG4gICAgICBpY29uQ29udGFpbmVyLnN0eWxlLmRpc3BsYXkgPSAnbm9uZSc7XG4gICAgfVxuICAgIHRhZy5hcHBlbmRDaGlsZChpY29uQ29udGFpbmVyKTtcbiAgICB0aGlzLm5vZGUuYXBwZW5kQ2hpbGQodGFnKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGFmdGVyLWF0dGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBvbkFmdGVyQXR0YWNoKCkge1xuICAgIHRoaXMubm9kZS5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzKTtcbiAgICB0aGlzLm5vZGUuYWRkRXZlbnRMaXN0ZW5lcignbW91c2VvdmVyJywgdGhpcyk7XG4gICAgdGhpcy5ub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ21vdXNlb3V0JywgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBiZWZvcmUtZGV0YWNoYCBtZXNzYWdlcyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIG9uQmVmb3JlRGV0YWNoKCkge1xuICAgIHRoaXMubm9kZS5yZW1vdmVFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzKTtcbiAgICB0aGlzLm5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignbW91c2VvdmVyJywgdGhpcyk7XG4gICAgdGhpcy5ub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ21vdXNlb3V0JywgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBET00gZXZlbnRzIGZvciB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIG1ldGhvZCBpbXBsZW1lbnRzIHRoZSBET00gYEV2ZW50TGlzdGVuZXJgIGludGVyZmFjZSBhbmQgaXNcbiAgICogY2FsbGVkIGluIHJlc3BvbnNlIHRvIGV2ZW50cyBvbiB0aGUgZG9jayBwYW5lbCdzIG5vZGUuIEl0IHNob3VsZFxuICAgKiBub3QgYmUgY2FsbGVkIGRpcmVjdGx5IGJ5IHVzZXIgY29kZS5cbiAgICovXG4gIGhhbmRsZUV2ZW50KGV2ZW50OiBFdmVudCk6IHZvaWQge1xuICAgIHN3aXRjaCAoZXZlbnQudHlwZSkge1xuICAgICAgY2FzZSAnbW91c2Vkb3duJzpcbiAgICAgICAgdGhpcy5fZXZ0Q2xpY2soKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdtb3VzZW92ZXInOlxuICAgICAgICB0aGlzLl9ldnRNb3VzZU92ZXIoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdtb3VzZW91dCc6XG4gICAgICAgIHRoaXMuX2V2dE1vdXNlT3V0KCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgdXBkYXRlLXJlcXVlc3RgIG1lc3NhZ2VzLiBDaGVjayBpZiBhcHBsaWVkIHRvIGN1cnJlbnQgYWN0aXZlIGNlbGwuXG4gICAqL1xuICBvblVwZGF0ZVJlcXVlc3QoKSB7XG4gICAgY29uc3QgYXBwbGllZCA9IHRoaXMucGFyZW50Py5jaGVja0FwcGxpZWQodGhpcy5uYW1lKTtcbiAgICBpZiAoYXBwbGllZCAhPT0gdGhpcy5hcHBsaWVkKSB7XG4gICAgICB0aGlzLnRvZ2dsZUFwcGxpZWQoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVXBkYXRlIHN0eWxpbmcgdG8gcmVmbGVjdCB3aGV0aGVyIHRhZyBpcyBhcHBsaWVkIHRvIGN1cnJlbnQgYWN0aXZlIGNlbGwuXG4gICAqL1xuICB0b2dnbGVBcHBsaWVkKCkge1xuICAgIGlmICh0aGlzLmFwcGxpZWQpIHtcbiAgICAgIHRoaXMucmVtb3ZlQ2xhc3MoJ2FwcGxpZWQtdGFnJyk7XG4gICAgICAodGhpcy5ub2RlLmZpcnN0Q2hpbGQ/Lmxhc3RDaGlsZCBhcyBIVE1MU3BhbkVsZW1lbnQpLnN0eWxlLmRpc3BsYXkgPVxuICAgICAgICAnbm9uZSc7XG4gICAgICB0aGlzLmFkZENsYXNzKCd1bmFwcGxpZWQtdGFnJyk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMucmVtb3ZlQ2xhc3MoJ3VuYXBwbGllZC10YWcnKTtcbiAgICAgICh0aGlzLm5vZGUuZmlyc3RDaGlsZD8ubGFzdENoaWxkIGFzIEhUTUxTcGFuRWxlbWVudCkuc3R5bGUuZGlzcGxheSA9XG4gICAgICAgICdpbmxpbmUtYmxvY2snO1xuICAgICAgdGhpcy5hZGRDbGFzcygnYXBwbGllZC10YWcnKTtcbiAgICB9XG4gICAgdGhpcy5hcHBsaWVkID0gIXRoaXMuYXBwbGllZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGAnY2xpY2snYCBldmVudCBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByaXZhdGUgX2V2dENsaWNrKCkge1xuICAgIGlmICh0aGlzLmFwcGxpZWQpIHtcbiAgICAgIHRoaXMucGFyZW50Py5yZW1vdmVUYWcodGhpcy5uYW1lKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5wYXJlbnQ/LmFkZFRhZyh0aGlzLm5hbWUpO1xuICAgIH1cbiAgICB0aGlzLnRvZ2dsZUFwcGxpZWQoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGAnbW91c2VvdmVyJ2AgZXZlbnQgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9ldnRNb3VzZU92ZXIoKSB7XG4gICAgKHRoaXMubm9kZSBhcyBIVE1MRWxlbWVudCkuY2xhc3NMaXN0LmFkZCgndGFnLWhvdmVyJyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBgJ21vdXNlb3V0J2AgZXZlbnQgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9ldnRNb3VzZU91dCgpIHtcbiAgICAodGhpcy5ub2RlIGFzIEhUTUxFbGVtZW50KS5jbGFzc0xpc3QucmVtb3ZlKCd0YWctaG92ZXInKTtcbiAgfVxuXG4gIHB1YmxpYyBuYW1lOiBzdHJpbmc7XG4gIHByaXZhdGUgYXBwbGllZDogYm9vbGVhbjtcbiAgcHVibGljIHBhcmVudDogVGFnVG9vbCB8IG51bGwgPSBudWxsO1xufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==