(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_property-inspector_lib_index_js-_1a420"],{

/***/ "../packages/property-inspector/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/property-inspector/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IPropertyInspectorProvider": () => (/* reexport safe */ _token__WEBPACK_IMPORTED_MODULE_4__.IPropertyInspectorProvider),
/* harmony export */   "SideBarPropertyInspectorProvider": () => (/* binding */ SideBarPropertyInspectorProvider)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _token__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./token */ "../packages/property-inspector/lib/token.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module property-inspector
 */






/**
 * The implementation of the PropertyInspector.
 */
class PropertyInspectorProvider extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    /**
     * Construct a new Property Inspector.
     */
    constructor() {
        super();
        this._tracker = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.FocusTracker();
        this._inspectors = new Map();
        this.addClass('jp-PropertyInspector');
        this._tracker = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.FocusTracker();
        this._tracker.currentChanged.connect(this._onCurrentChanged, this);
    }
    /**
     * Register a widget in the property inspector provider.
     *
     * @param widget The owner widget to register.
     */
    register(widget) {
        if (this._inspectors.has(widget)) {
            throw new Error('Widget is already registered');
        }
        const inspector = new Private.PropertyInspector(widget);
        widget.disposed.connect(this._onWidgetDisposed, this);
        this._inspectors.set(widget, inspector);
        inspector.onAction.connect(this._onInspectorAction, this);
        this._tracker.add(widget);
        return inspector;
    }
    /**
     * The current widget being tracked by the inspector.
     */
    get currentWidget() {
        return this._tracker.currentWidget;
    }
    /**
     * Refresh the content for the current widget.
     */
    refresh() {
        const current = this._tracker.currentWidget;
        if (!current) {
            this.setContent(null);
            return;
        }
        const inspector = this._inspectors.get(current);
        if (inspector) {
            this.setContent(inspector.content);
        }
    }
    /**
     * Handle the disposal of a widget.
     */
    _onWidgetDisposed(sender) {
        const inspector = this._inspectors.get(sender);
        if (inspector) {
            inspector.dispose();
            this._inspectors.delete(sender);
        }
    }
    /**
     * Handle inspector actions.
     */
    _onInspectorAction(sender, action) {
        const owner = sender.owner;
        const current = this._tracker.currentWidget;
        switch (action) {
            case 'content':
                if (current === owner) {
                    this.setContent(sender.content);
                }
                break;
            case 'dispose':
                if (owner) {
                    this._tracker.remove(owner);
                    this._inspectors.delete(owner);
                }
                break;
            case 'show-panel':
                if (current === owner) {
                    this.showPanel();
                }
                break;
            default:
                throw new Error('Unsupported inspector action');
        }
    }
    /**
     * Handle a change to the current widget in the tracker.
     */
    _onCurrentChanged() {
        const current = this._tracker.currentWidget;
        if (current) {
            const inspector = this._inspectors.get(current);
            const content = inspector.content;
            this.setContent(content);
        }
        else {
            this.setContent(null);
        }
    }
}
/**
 * A class that adds a property inspector provider to the
 * JupyterLab sidebar.
 */
class SideBarPropertyInspectorProvider extends PropertyInspectorProvider {
    /**
     * Construct a new Side Bar Property Inspector.
     */
    constructor(labshell, placeholder, translator) {
        super();
        this._labshell = labshell;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.SingletonLayout());
        if (placeholder) {
            this._placeholder = placeholder;
        }
        else {
            const node = document.createElement('div');
            const content = document.createElement('div');
            content.textContent = this._trans.__('No properties to inspect.');
            content.className = 'jp-PropertyInspector-placeholderContent';
            node.appendChild(content);
            this._placeholder = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget({ node });
            this._placeholder.addClass('jp-PropertyInspector-placeholder');
        }
        layout.widget = this._placeholder;
        labshell.currentChanged.connect(this._onShellCurrentChanged, this);
        this._onShellCurrentChanged();
    }
    /**
     * Set the content of the sidebar panel.
     */
    setContent(content) {
        const layout = this.layout;
        if (layout.widget) {
            layout.widget.removeClass('jp-PropertyInspector-content');
            layout.removeWidget(layout.widget);
        }
        if (!content) {
            content = this._placeholder;
        }
        content.addClass('jp-PropertyInspector-content');
        layout.widget = content;
    }
    /**
     * Show the sidebar panel.
     */
    showPanel() {
        this._labshell.activateById(this.id);
    }
    /**
     * Handle the case when the current widget is not in our tracker.
     */
    _onShellCurrentChanged() {
        const current = this.currentWidget;
        if (!current) {
            this.setContent(null);
            return;
        }
        const currentShell = this._labshell.currentWidget;
        if (currentShell === null || currentShell === void 0 ? void 0 : currentShell.node.contains(current.node)) {
            this.refresh();
        }
        else {
            this.setContent(null);
        }
    }
}
/**
 * A namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * An implementation of the property inspector used by the
     * property inspector provider.
     */
    class PropertyInspector {
        /**
         * Construct a new property inspector.
         */
        constructor(owner) {
            this._isDisposed = false;
            this._content = null;
            this._owner = null;
            this._onAction = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
            this._owner = owner;
        }
        /**
         * The owner widget for the property inspector.
         */
        get owner() {
            return this._owner;
        }
        /**
         * The current content for the property inspector.
         */
        get content() {
            return this._content;
        }
        /**
         * Whether the property inspector is disposed.
         */
        get isDisposed() {
            return this._isDisposed;
        }
        /**
         * A signal used for actions related to the property inspector.
         */
        get onAction() {
            return this._onAction;
        }
        /**
         * Show the property inspector panel.
         */
        showPanel() {
            if (this._isDisposed) {
                return;
            }
            this._onAction.emit('show-panel');
        }
        /**
         * Render the property inspector content.
         */
        render(widget) {
            if (this._isDisposed) {
                return;
            }
            if (widget instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget) {
                this._content = widget;
            }
            else {
                this._content = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget.create(widget);
            }
            this._onAction.emit('content');
        }
        /**
         * Dispose of the property inspector.
         */
        dispose() {
            if (this._isDisposed) {
                return;
            }
            this._isDisposed = true;
            this._content = null;
            this._owner = null;
            _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
        }
    }
    Private.PropertyInspector = PropertyInspector;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/property-inspector/lib/token.js":
/*!***************************************************!*\
  !*** ../packages/property-inspector/lib/token.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IPropertyInspectorProvider": () => (/* binding */ IPropertyInspectorProvider)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The property inspector provider token.
 */
const IPropertyInspectorProvider = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/property-inspector:IPropertyInspectorProvider');


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcHJvcGVydHktaW5zcGVjdG9yL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcHJvcGVydHktaW5zcGVjdG9yL3NyYy90b2tlbi50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBR2dEO0FBS2xCO0FBQ21CO0FBQ29CO0FBRUM7QUFFZjtBQUUxRDs7R0FFRztBQUNILE1BQWUseUJBQ2IsU0FBUSxtREFBTTtJQUVkOztPQUVHO0lBQ0g7UUFDRSxLQUFLLEVBQUUsQ0FBQztRQStHRixhQUFRLEdBQUcsSUFBSSx5REFBWSxFQUFFLENBQUM7UUFDOUIsZ0JBQVcsR0FBRyxJQUFJLEdBQUcsRUFBcUMsQ0FBQztRQS9HakUsSUFBSSxDQUFDLFFBQVEsQ0FBQyxzQkFBc0IsQ0FBQyxDQUFDO1FBQ3RDLElBQUksQ0FBQyxRQUFRLEdBQUcsSUFBSSx5REFBWSxFQUFFLENBQUM7UUFDbkMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxjQUFjLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxpQkFBaUIsRUFBRSxJQUFJLENBQUMsQ0FBQztJQUNyRSxDQUFDO0lBRUQ7Ozs7T0FJRztJQUNILFFBQVEsQ0FBQyxNQUFjO1FBQ3JCLElBQUksSUFBSSxDQUFDLFdBQVcsQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLEVBQUU7WUFDaEMsTUFBTSxJQUFJLEtBQUssQ0FBQyw4QkFBOEIsQ0FBQyxDQUFDO1NBQ2pEO1FBQ0QsTUFBTSxTQUFTLEdBQUcsSUFBSSxPQUFPLENBQUMsaUJBQWlCLENBQUMsTUFBTSxDQUFDLENBQUM7UUFDeEQsTUFBTSxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLGlCQUFpQixF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QztRQUVEOztXQUVHO1FBQ0gsT0FBTztZQUNMLElBQUksSUFBSSxDQUFDLFdBQVcsRUFBRTtnQkFDcEIsT0FBTzthQUNSO1lBQ0QsSUFBSSxDQUFDLFdBQVcsR0FBRyxJQUFJLENBQUM7WUFDeEIsSUFBSSxDQUFDLFFBQVEsR0FBRyxJQUFJLENBQUM7WUFDckIsSUFBSSxDQUFDLE1BQU0sR0FBRyxJQUFJLENBQUM7WUFDbkIsK0RBQWdCLENBQUMsSUFBSSxDQUFDLENBQUM7UUFDekIsQ0FBQztLQVNGO0lBakZZLHlCQUFpQixvQkFpRjdCO0FBQ0gsQ0FBQyxFQTVGUyxPQUFPLEtBQVAsT0FBTyxRQTRGaEI7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ2pVRCwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBRWpCO0FBa0QxQzs7R0FFRztBQUNJLE1BQU0sMEJBQTBCLEdBQUcsSUFBSSxvREFBSyxDQUNqRCwyREFBMkQsQ0FDNUQsQ0FBQyIsImZpbGUiOiJwYWNrYWdlc19wcm9wZXJ0eS1pbnNwZWN0b3JfbGliX2luZGV4X2pzLV8xYTQyMC4zZWNjZmUyZjBhNDhmZTUyOGI4Ni5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHByb3BlcnR5LWluc3BlY3RvclxuICovXG5cbmltcG9ydCB7IElMYWJTaGVsbCB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IFJlYWN0V2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIG51bGxUcmFuc2xhdG9yLFxuICBUcmFuc2xhdGlvbkJ1bmRsZVxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBGb2N1c1RyYWNrZXIsIFNpbmdsZXRvbkxheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IElQcm9wZXJ0eUluc3BlY3RvciwgSVByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXIgfSBmcm9tICcuL3Rva2VuJztcblxuZXhwb3J0IHsgSVByb3BlcnR5SW5zcGVjdG9yLCBJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlciB9O1xuXG4vKipcbiAqIFRoZSBpbXBsZW1lbnRhdGlvbiBvZiB0aGUgUHJvcGVydHlJbnNwZWN0b3IuXG4gKi9cbmFic3RyYWN0IGNsYXNzIFByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXJcbiAgZXh0ZW5kcyBXaWRnZXRcbiAgaW1wbGVtZW50cyBJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlciB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgUHJvcGVydHkgSW5zcGVjdG9yLlxuICAgKi9cbiAgY29uc3RydWN0b3IoKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1Qcm9wZXJ0eUluc3BlY3RvcicpO1xuICAgIHRoaXMuX3RyYWNrZXIgPSBuZXcgRm9jdXNUcmFja2VyKCk7XG4gICAgdGhpcy5fdHJhY2tlci5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KHRoaXMuX29uQ3VycmVudENoYW5nZWQsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlZ2lzdGVyIGEgd2lkZ2V0IGluIHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgcHJvdmlkZXIuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgVGhlIG93bmVyIHdpZGdldCB0byByZWdpc3Rlci5cbiAgICovXG4gIHJlZ2lzdGVyKHdpZGdldDogV2lkZ2V0KTogSVByb3BlcnR5SW5zcGVjdG9yIHtcbiAgICBpZiAodGhpcy5faW5zcGVjdG9ycy5oYXMod2lkZ2V0KSkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCdXaWRnZXQgaXMgYWxyZWFkeSByZWdpc3RlcmVkJyk7XG4gICAgfVxuICAgIGNvbnN0IGluc3BlY3RvciA9IG5ldyBQcml2YXRlLlByb3BlcnR5SW5zcGVjdG9yKHdpZGdldCk7XG4gICAgd2lkZ2V0LmRpc3Bvc2VkLmNvbm5lY3QodGhpcy5fb25XaWRnZXREaXNwb3NlZCwgdGhpcyk7XG4gICAgdGhpcy5faW5zcGVjdG9ycy5zZXQod2lkZ2V0LCBpbnNwZWN0b3IpO1xuICAgIGluc3BlY3Rvci5vbkFjdGlvbi5jb25uZWN0KHRoaXMuX29uSW5zcGVjdG9yQWN0aW9uLCB0aGlzKTtcbiAgICB0aGlzLl90cmFja2VyLmFkZCh3aWRnZXQpO1xuICAgIHJldHVybiBpbnNwZWN0b3I7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGN1cnJlbnQgd2lkZ2V0IGJlaW5nIHRyYWNrZWQgYnkgdGhlIGluc3BlY3Rvci5cbiAgICovXG4gIHByb3RlY3RlZCBnZXQgY3VycmVudFdpZGdldCgpOiBXaWRnZXQgfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICB9XG5cbiAgLyoqXG4gICAqIFJlZnJlc2ggdGhlIGNvbnRlbnQgZm9yIHRoZSBjdXJyZW50IHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCByZWZyZXNoKCk6IHZvaWQge1xuICAgIGNvbnN0IGN1cnJlbnQgPSB0aGlzLl90cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICB0aGlzLnNldENvbnRlbnQobnVsbCk7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IGluc3BlY3RvciA9IHRoaXMuX2luc3BlY3RvcnMuZ2V0KGN1cnJlbnQpO1xuICAgIGlmIChpbnNwZWN0b3IpIHtcbiAgICAgIHRoaXMuc2V0Q29udGVudChpbnNwZWN0b3IuY29udGVudCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFNob3cgdGhlIHByb3ZpZGVyIHBhbmVsLlxuICAgKi9cbiAgcHJvdGVjdGVkIGFic3RyYWN0IHNob3dQYW5lbCgpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBTZXQgdGhlIGNvbnRlbnQgb2YgdGhlIHByb3ZpZGVyLlxuICAgKi9cbiAgcHJvdGVjdGVkIGFic3RyYWN0IHNldENvbnRlbnQoY29udGVudDogV2lkZ2V0IHwgbnVsbCk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgZGlzcG9zYWwgb2YgYSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9vbldpZGdldERpc3Bvc2VkKHNlbmRlcjogV2lkZ2V0KTogdm9pZCB7XG4gICAgY29uc3QgaW5zcGVjdG9yID0gdGhpcy5faW5zcGVjdG9ycy5nZXQoc2VuZGVyKTtcbiAgICBpZiAoaW5zcGVjdG9yKSB7XG4gICAgICBpbnNwZWN0b3IuZGlzcG9zZSgpO1xuICAgICAgdGhpcy5faW5zcGVjdG9ycy5kZWxldGUoc2VuZGVyKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGluc3BlY3RvciBhY3Rpb25zLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25JbnNwZWN0b3JBY3Rpb24oXG4gICAgc2VuZGVyOiBQcml2YXRlLlByb3BlcnR5SW5zcGVjdG9yLFxuICAgIGFjdGlvbjogUHJpdmF0ZS5Qcm9wZXJ0eUluc3BlY3RvckFjdGlvblxuICApIHtcbiAgICBjb25zdCBvd25lciA9IHNlbmRlci5vd25lcjtcbiAgICBjb25zdCBjdXJyZW50ID0gdGhpcy5fdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgIHN3aXRjaCAoYWN0aW9uKSB7XG4gICAgICBjYXNlICdjb250ZW50JzpcbiAgICAgICAgaWYgKGN1cnJlbnQgPT09IG93bmVyKSB7XG4gICAgICAgICAgdGhpcy5zZXRDb250ZW50KHNlbmRlci5jb250ZW50KTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2Rpc3Bvc2UnOlxuICAgICAgICBpZiAob3duZXIpIHtcbiAgICAgICAgICB0aGlzLl90cmFja2VyLnJlbW92ZShvd25lcik7XG4gICAgICAgICAgdGhpcy5faW5zcGVjdG9ycy5kZWxldGUob3duZXIpO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnc2hvdy1wYW5lbCc6XG4gICAgICAgIGlmIChjdXJyZW50ID09PSBvd25lcikge1xuICAgICAgICAgIHRoaXMuc2hvd1BhbmVsKCk7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICB0aHJvdyBuZXcgRXJyb3IoJ1Vuc3VwcG9ydGVkIGluc3BlY3RvciBhY3Rpb24nKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSBjdXJyZW50IHdpZGdldCBpbiB0aGUgdHJhY2tlci5cbiAgICovXG4gIHByaXZhdGUgX29uQ3VycmVudENoYW5nZWQoKTogdm9pZCB7XG4gICAgY29uc3QgY3VycmVudCA9IHRoaXMuX3RyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICBpZiAoY3VycmVudCkge1xuICAgICAgY29uc3QgaW5zcGVjdG9yID0gdGhpcy5faW5zcGVjdG9ycy5nZXQoY3VycmVudCk7XG4gICAgICBjb25zdCBjb250ZW50ID0gaW5zcGVjdG9yIS5jb250ZW50O1xuICAgICAgdGhpcy5zZXRDb250ZW50KGNvbnRlbnQpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLnNldENvbnRlbnQobnVsbCk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfdHJhY2tlciA9IG5ldyBGb2N1c1RyYWNrZXIoKTtcbiAgcHJpdmF0ZSBfaW5zcGVjdG9ycyA9IG5ldyBNYXA8V2lkZ2V0LCBQcml2YXRlLlByb3BlcnR5SW5zcGVjdG9yPigpO1xufVxuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCBhZGRzIGEgcHJvcGVydHkgaW5zcGVjdG9yIHByb3ZpZGVyIHRvIHRoZVxuICogSnVweXRlckxhYiBzaWRlYmFyLlxuICovXG5leHBvcnQgY2xhc3MgU2lkZUJhclByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXIgZXh0ZW5kcyBQcm9wZXJ0eUluc3BlY3RvclByb3ZpZGVyIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBTaWRlIEJhciBQcm9wZXJ0eSBJbnNwZWN0b3IuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihcbiAgICBsYWJzaGVsbDogSUxhYlNoZWxsLFxuICAgIHBsYWNlaG9sZGVyPzogV2lkZ2V0LFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuX2xhYnNoZWxsID0gbGFic2hlbGw7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl90cmFucyA9IHRoaXMudHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgbGF5b3V0ID0gKHRoaXMubGF5b3V0ID0gbmV3IFNpbmdsZXRvbkxheW91dCgpKTtcbiAgICBpZiAocGxhY2Vob2xkZXIpIHtcbiAgICAgIHRoaXMuX3BsYWNlaG9sZGVyID0gcGxhY2Vob2xkZXI7XG4gICAgfSBlbHNlIHtcbiAgICAgIGNvbnN0IG5vZGUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICAgIGNvbnN0IGNvbnRlbnQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICAgIGNvbnRlbnQudGV4dENvbnRlbnQgPSB0aGlzLl90cmFucy5fXygnTm8gcHJvcGVydGllcyB0byBpbnNwZWN0LicpO1xuICAgICAgY29udGVudC5jbGFzc05hbWUgPSAnanAtUHJvcGVydHlJbnNwZWN0b3ItcGxhY2Vob2xkZXJDb250ZW50JztcbiAgICAgIG5vZGUuYXBwZW5kQ2hpbGQoY29udGVudCk7XG4gICAgICB0aGlzLl9wbGFjZWhvbGRlciA9IG5ldyBXaWRnZXQoeyBub2RlIH0pO1xuICAgICAgdGhpcy5fcGxhY2Vob2xkZXIuYWRkQ2xhc3MoJ2pwLVByb3BlcnR5SW5zcGVjdG9yLXBsYWNlaG9sZGVyJyk7XG4gICAgfVxuICAgIGxheW91dC53aWRnZXQgPSB0aGlzLl9wbGFjZWhvbGRlcjtcbiAgICBsYWJzaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KHRoaXMuX29uU2hlbGxDdXJyZW50Q2hhbmdlZCwgdGhpcyk7XG4gICAgdGhpcy5fb25TaGVsbEN1cnJlbnRDaGFuZ2VkKCk7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBjb250ZW50IG9mIHRoZSBzaWRlYmFyIHBhbmVsLlxuICAgKi9cbiAgcHJvdGVjdGVkIHNldENvbnRlbnQoY29udGVudDogV2lkZ2V0IHwgbnVsbCk6IHZvaWQge1xuICAgIGNvbnN0IGxheW91dCA9IHRoaXMubGF5b3V0IGFzIFNpbmdsZXRvbkxheW91dDtcbiAgICBpZiAobGF5b3V0LndpZGdldCkge1xuICAgICAgbGF5b3V0LndpZGdldC5yZW1vdmVDbGFzcygnanAtUHJvcGVydHlJbnNwZWN0b3ItY29udGVudCcpO1xuICAgICAgbGF5b3V0LnJlbW92ZVdpZGdldChsYXlvdXQud2lkZ2V0KTtcbiAgICB9XG4gICAgaWYgKCFjb250ZW50KSB7XG4gICAgICBjb250ZW50ID0gdGhpcy5fcGxhY2Vob2xkZXI7XG4gICAgfVxuICAgIGNvbnRlbnQuYWRkQ2xhc3MoJ2pwLVByb3BlcnR5SW5zcGVjdG9yLWNvbnRlbnQnKTtcbiAgICBsYXlvdXQud2lkZ2V0ID0gY29udGVudDtcbiAgfVxuXG4gIC8qKlxuICAgKiBTaG93IHRoZSBzaWRlYmFyIHBhbmVsLlxuICAgKi9cbiAgc2hvd1BhbmVsKCk6IHZvaWQge1xuICAgIHRoaXMuX2xhYnNoZWxsLmFjdGl2YXRlQnlJZCh0aGlzLmlkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGNhc2Ugd2hlbiB0aGUgY3VycmVudCB3aWRnZXQgaXMgbm90IGluIG91ciB0cmFja2VyLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25TaGVsbEN1cnJlbnRDaGFuZ2VkKCk6IHZvaWQge1xuICAgIGNvbnN0IGN1cnJlbnQgPSB0aGlzLmN1cnJlbnRXaWRnZXQ7XG4gICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICB0aGlzLnNldENvbnRlbnQobnVsbCk7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IGN1cnJlbnRTaGVsbCA9IHRoaXMuX2xhYnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgaWYgKGN1cnJlbnRTaGVsbD8ubm9kZS5jb250YWlucyhjdXJyZW50Lm5vZGUpKSB7XG4gICAgICB0aGlzLnJlZnJlc2goKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5zZXRDb250ZW50KG51bGwpO1xuICAgIH1cbiAgfVxuXG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF9sYWJzaGVsbDogSUxhYlNoZWxsO1xuICBwcml2YXRlIF9wbGFjZWhvbGRlcjogV2lkZ2V0O1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBtb2R1bGUgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBIHR5cGUgYWxpYXMgZm9yIHRoZSBhY3Rpb25zIGEgcHJvcGVydHkgaW5zcGVjdG9yIGNhbiB0YWtlLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgUHJvcGVydHlJbnNwZWN0b3JBY3Rpb24gPSAnY29udGVudCcgfCAnZGlzcG9zZScgfCAnc2hvdy1wYW5lbCc7XG5cbiAgLyoqXG4gICAqIEFuIGltcGxlbWVudGF0aW9uIG9mIHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgdXNlZCBieSB0aGVcbiAgICogcHJvcGVydHkgaW5zcGVjdG9yIHByb3ZpZGVyLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIFByb3BlcnR5SW5zcGVjdG9yIGltcGxlbWVudHMgSVByb3BlcnR5SW5zcGVjdG9yIHtcbiAgICAvKipcbiAgICAgKiBDb25zdHJ1Y3QgYSBuZXcgcHJvcGVydHkgaW5zcGVjdG9yLlxuICAgICAqL1xuICAgIGNvbnN0cnVjdG9yKG93bmVyOiBXaWRnZXQpIHtcbiAgICAgIHRoaXMuX293bmVyID0gb3duZXI7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIG93bmVyIHdpZGdldCBmb3IgdGhlIHByb3BlcnR5IGluc3BlY3Rvci5cbiAgICAgKi9cbiAgICBnZXQgb3duZXIoKTogV2lkZ2V0IHwgbnVsbCB7XG4gICAgICByZXR1cm4gdGhpcy5fb3duZXI7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgY29udGVudCBmb3IgdGhlIHByb3BlcnR5IGluc3BlY3Rvci5cbiAgICAgKi9cbiAgICBnZXQgY29udGVudCgpOiBXaWRnZXQgfCBudWxsIHtcbiAgICAgIHJldHVybiB0aGlzLl9jb250ZW50O1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdGhlIHByb3BlcnR5IGluc3BlY3RvciBpcyBkaXNwb3NlZC5cbiAgICAgKi9cbiAgICBnZXQgaXNEaXNwb3NlZCgpIHtcbiAgICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIHVzZWQgZm9yIGFjdGlvbnMgcmVsYXRlZCB0byB0aGUgcHJvcGVydHkgaW5zcGVjdG9yLlxuICAgICAqL1xuICAgIGdldCBvbkFjdGlvbigpOiBJU2lnbmFsPFByb3BlcnR5SW5zcGVjdG9yLCBQcm9wZXJ0eUluc3BlY3RvckFjdGlvbj4ge1xuICAgICAgcmV0dXJuIHRoaXMuX29uQWN0aW9uO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFNob3cgdGhlIHByb3BlcnR5IGluc3BlY3RvciBwYW5lbC5cbiAgICAgKi9cbiAgICBzaG93UGFuZWwoKTogdm9pZCB7XG4gICAgICBpZiAodGhpcy5faXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICB0aGlzLl9vbkFjdGlvbi5lbWl0KCdzaG93LXBhbmVsJyk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVuZGVyIHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgY29udGVudC5cbiAgICAgKi9cbiAgICByZW5kZXIod2lkZ2V0OiBXaWRnZXQgfCBSZWFjdC5SZWFjdEVsZW1lbnQpOiB2b2lkIHtcbiAgICAgIGlmICh0aGlzLl9pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGlmICh3aWRnZXQgaW5zdGFuY2VvZiBXaWRnZXQpIHtcbiAgICAgICAgdGhpcy5fY29udGVudCA9IHdpZGdldDtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuX2NvbnRlbnQgPSBSZWFjdFdpZGdldC5jcmVhdGUod2lkZ2V0KTtcbiAgICAgIH1cbiAgICAgIHRoaXMuX29uQWN0aW9uLmVtaXQoJ2NvbnRlbnQnKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBEaXNwb3NlIG9mIHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IuXG4gICAgICovXG4gICAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICAgIGlmICh0aGlzLl9pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuICAgICAgdGhpcy5fY29udGVudCA9IG51bGw7XG4gICAgICB0aGlzLl9vd25lciA9IG51bGw7XG4gICAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICAgIH1cblxuICAgIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgICBwcml2YXRlIF9jb250ZW50OiBXaWRnZXQgfCBudWxsID0gbnVsbDtcbiAgICBwcml2YXRlIF9vd25lcjogV2lkZ2V0IHwgbnVsbCA9IG51bGw7XG4gICAgcHJpdmF0ZSBfb25BY3Rpb24gPSBuZXcgU2lnbmFsPFxuICAgICAgUHJvcGVydHlJbnNwZWN0b3IsXG4gICAgICBQcml2YXRlLlByb3BlcnR5SW5zcGVjdG9yQWN0aW9uXG4gICAgPih0aGlzKTtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbi8qKlxuICogQSBwcm9wZXJ0eSBpbnNwZWN0b3IgaW50ZXJmYWNlIHByb3ZpZGVkIHdoZW4gcmVnaXN0ZXJpbmdcbiAqIHRvIGEgcHJvcGVydHkgaW5zcGVjdG9yIHByb3ZpZGVyLiAgQWxsb3dzIGFuIG93bmVyIHdpZGdldFxuICogdG8gc2V0IHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgY29udGVudCBmb3IgaXRzZWxmLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElQcm9wZXJ0eUluc3BlY3RvciBleHRlbmRzIElEaXNwb3NhYmxlIHtcbiAgLypcbiAgICogUmVuZGVyIHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgY29udGVudC5cbiAgICpcbiAgICogSWYgdGhlIG93bmVyIHdpZGdldCBpcyBub3QgdGhlIG1vc3QgcmVjZW50bHkgZm9jdXNlZCxcbiAgICogVGhlIGNvbnRlbnQgd2lsbCBub3QgYmUgc2hvd24gdW50aWwgdGhhdCB3aWRnZXRcbiAgICogaXMgZm9jdXNlZC5cbiAgICpcbiAgICogQHBhcmFtIGNvbnRlbnQgLSB0aGUgd2lkZ2V0IG9yIHJlYWN0IGVsZW1lbnQgdG8gcmVuZGVyLlxuICAgKi9cbiAgcmVuZGVyKGNvbnRlbnQ6IFdpZGdldCB8IFJlYWN0LlJlYWN0RWxlbWVudCk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIFNob3cgdGhlIHByb3BlcnR5IGluc3BlY3RvciBwYW5lbC5cbiAgICpcbiAgICogSWYgdGhlIG93bmVyIHdpZGdldCBpcyBub3QgdGhlIG1vc3QgcmVjZW50bHkgZm9jdXNlZCxcbiAgICogdGhpcyBpcyBhIG5vLW9wLiAgSXQgc2hvdWxkIGJlIHRyaWdnZXJlZCBieSBhIHVzZXJcbiAgICogYWN0aW9uLlxuICAgKi9cbiAgc2hvd1BhbmVsKCk6IHZvaWQ7XG59XG5cbi8qKlxuICogQSBwcm92aWRlciBmb3IgcHJvcGVydHkgaW5zcGVjdG9ycy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlciB7XG4gIC8qKlxuICAgKiBSZWdpc3RlciBhIHdpZGdldCBpbiB0aGUgcHJvcGVydHkgaW5zcGVjdG9yIHByb3ZpZGVyLlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IFRoZSBvd25lciB3aWRnZXQgd2hvc2UgcHJvcGVydGllcyB3aWxsIGJlIGluc3BlY3RlZC5cbiAgICpcbiAgICogIyMgTm90ZXNcbiAgICogT25seSBvbmUgcHJvcGVydHkgaW5zcGVjdG9yIGNhbiBiZSBwcm92aWRlZCBmb3IgZWFjaCB3aWRnZXQuXG4gICAqIFJlZ2lzdGVyaW5nIHRoZSBzYW1lIHdpZGdldCB0d2ljZSB3aWxsIHJlc3VsdCBpbiBhbiBlcnJvci5cbiAgICogQSB3aWRnZXQgY2FuIGJlIHVucmVnaXN0ZXJlZCBieSBkaXNwb3Npbmcgb2YgaXRzIHByb3BlcnR5XG4gICAqIGluc3BlY3Rvci5cbiAgICovXG4gIHJlZ2lzdGVyKHdpZGdldDogV2lkZ2V0KTogSVByb3BlcnR5SW5zcGVjdG9yO1xufVxuXG4vKipcbiAqIFRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgcHJvdmlkZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlciA9IG5ldyBUb2tlbjxJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlcj4oXG4gICdAanVweXRlcmxhYi9wcm9wZXJ0eS1pbnNwZWN0b3I6SVByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXInXG4pO1xuIl0sInNvdXJjZVJvb3QiOiIifQ==