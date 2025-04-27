(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_documentsearch-extension_lib_index_js-_65150"],{

/***/ "../packages/documentsearch-extension/lib/index.js":
/*!*********************************************************!*\
  !*** ../packages/documentsearch-extension/lib/index.js ***!
  \*********************************************************/
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
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/documentsearch */ "webpack/sharing/consume/default/@jupyterlab/documentsearch/@jupyterlab/documentsearch");
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module documentsearch-extension
 */




const SEARCHABLE_CLASS = 'jp-mod-searchable';
const labShellWidgetListener = {
    id: '@jupyterlab/documentsearch:labShellWidgetListener',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.ISearchProviderRegistry],
    autoStart: true,
    activate: (app, labShell, registry) => {
        // If a given widget is searchable, apply the searchable class.
        // If it's not searchable, remove the class.
        const transformWidgetSearchability = (widget) => {
            if (!widget) {
                return;
            }
            const providerForWidget = registry.getProviderForWidget(widget);
            if (providerForWidget) {
                widget.addClass(SEARCHABLE_CLASS);
            }
            if (!providerForWidget) {
                widget.removeClass(SEARCHABLE_CLASS);
            }
        };
        // Update searchability of the active widget when the registry
        // changes, in case a provider for the current widget was added
        // or removed
        registry.changed.connect(() => transformWidgetSearchability(labShell.activeWidget));
        // Apply the searchable class only to the active widget if it is actually
        // searchable. Remove the searchable class from a widget when it's
        // no longer active.
        labShell.activeChanged.connect((_, args) => {
            const oldWidget = args.oldValue;
            if (oldWidget) {
                oldWidget.removeClass(SEARCHABLE_CLASS);
            }
            transformWidgetSearchability(args.newValue);
        });
    }
};
/**
 * Initialization data for the document-search extension.
 */
const extension = {
    id: '@jupyterlab/documentsearch:plugin',
    provides: _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.ISearchProviderRegistry,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true,
    activate: (app, translator, palette) => {
        const trans = translator.load('jupyterlab');
        // Create registry, retrieve all default providers
        const registry = new _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.SearchProviderRegistry();
        // Register default implementations of the Notebook and CodeMirror search providers
        registry.register('jp-notebookSearchProvider', _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.NotebookSearchProvider);
        registry.register('jp-codeMirrorSearchProvider', _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.CodeMirrorSearchProvider);
        const activeSearches = new Map();
        const startCommand = 'documentsearch:start';
        const startReplaceCommand = 'documentsearch:startWithReplace';
        const nextCommand = 'documentsearch:highlightNext';
        const prevCommand = 'documentsearch:highlightPrevious';
        const currentWidgetHasSearchProvider = () => {
            const currentWidget = app.shell.currentWidget;
            if (!currentWidget) {
                return false;
            }
            return registry.getProviderForWidget(currentWidget) !== undefined;
        };
        const getCurrentWidgetSearchInstance = () => {
            const currentWidget = app.shell.currentWidget;
            if (!currentWidget) {
                return;
            }
            const widgetId = currentWidget.id;
            let searchInstance = activeSearches.get(widgetId);
            if (!searchInstance) {
                const searchProvider = registry.getProviderForWidget(currentWidget);
                if (!searchProvider) {
                    return;
                }
                searchInstance = new _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.SearchInstance(currentWidget, searchProvider, translator);
                activeSearches.set(widgetId, searchInstance);
                // find next and previous are now enabled
                app.commands.notifyCommandChanged();
                searchInstance.disposed.connect(() => {
                    activeSearches.delete(widgetId);
                    // find next and previous are now not enabled
                    app.commands.notifyCommandChanged();
                });
            }
            return searchInstance;
        };
        app.commands.addCommand(startCommand, {
            label: trans.__('Find…'),
            isEnabled: currentWidgetHasSearchProvider,
            execute: () => {
                const searchInstance = getCurrentWidgetSearchInstance();
                if (searchInstance) {
                    searchInstance.focusInput();
                }
            }
        });
        app.commands.addCommand(startReplaceCommand, {
            label: trans.__('Find and Replace…'),
            isEnabled: currentWidgetHasSearchProvider,
            execute: () => {
                const searchInstance = getCurrentWidgetSearchInstance();
                if (searchInstance) {
                    searchInstance.showReplace();
                    searchInstance.focusInput();
                }
            }
        });
        app.commands.addCommand(nextCommand, {
            label: trans.__('Find Next'),
            isEnabled: () => {
                const currentWidget = app.shell.currentWidget;
                if (!currentWidget) {
                    return false;
                }
                return activeSearches.has(currentWidget.id);
            },
            execute: async () => {
                const currentWidget = app.shell.currentWidget;
                if (!currentWidget) {
                    return;
                }
                const instance = activeSearches.get(currentWidget.id);
                if (!instance) {
                    return;
                }
                await instance.provider.highlightNext();
                instance.updateIndices();
            }
        });
        app.commands.addCommand(prevCommand, {
            label: trans.__('Find Previous'),
            isEnabled: () => {
                const currentWidget = app.shell.currentWidget;
                if (!currentWidget) {
                    return false;
                }
                return activeSearches.has(currentWidget.id);
            },
            execute: async () => {
                const currentWidget = app.shell.currentWidget;
                if (!currentWidget) {
                    return;
                }
                const instance = activeSearches.get(currentWidget.id);
                if (!instance) {
                    return;
                }
                await instance.provider.highlightPrevious();
                instance.updateIndices();
            }
        });
        // Add the command to the palette.
        if (palette) {
            palette.addItem({
                command: startCommand,
                category: trans.__('Main Area')
            });
            palette.addItem({
                command: nextCommand,
                category: trans.__('Main Area')
            });
            palette.addItem({
                command: prevCommand,
                category: trans.__('Main Area')
            });
        }
        // Provide the registry to the system.
        return registry;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([extension, labShellWidgetListener]);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jdW1lbnRzZWFyY2gtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU04QjtBQUVzQjtBQVFuQjtBQUVrQjtBQUd0RCxNQUFNLGdCQUFnQixHQUFHLG1CQUFtQixDQUFDO0FBRTdDLE1BQU0sc0JBQXNCLEdBQWdDO0lBQzFELEVBQUUsRUFBRSxtREFBbUQ7SUFDdkQsUUFBUSxFQUFFLENBQUMsOERBQVMsRUFBRSwrRUFBdUIsQ0FBQztJQUM5QyxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLFFBQW1CLEVBQ25CLFFBQWlDLEVBQ2pDLEVBQUU7UUFDRiwrREFBK0Q7UUFDL0QsNENBQTRDO1FBQzVDLE1BQU0sNEJBQTRCLEdBQUcsQ0FBQyxNQUFxQixFQUFFLEVBQUU7WUFDN0QsSUFBSSxDQUFDLE1BQU0sRUFBRTtnQkFDWCxPQUFPO2FBQ1I7WUFDRCxNQUFNLGlCQUFpQixHQUFHLFFBQVEsQ0FBQyxvQkFBb0IsQ0FBQyxNQUFNLENBQUMsQ0FBQztZQUNoRSxJQUFJLGlCQUFpQixFQUFFO2dCQUNyQixNQUFNLENBQUMsUUFBUSxDQUFDLGdCQUFnQixDQUFDLENBQUM7YUFDbkM7WUFDRCxJQUFJLENBQUMsaUJBQWlCLEVBQUU7Z0JBQ3RCLE1BQU0sQ0FBQyxXQUFXLENBQUMsZ0JBQWdCLENBQUMsQ0FBQzthQUN0QztRQUNILENBQUMsQ0FBQztRQUVGLDhEQUE4RDtRQUM5RCwrREFBK0Q7UUFDL0QsYUFBYTtRQUNiLFFBQVEsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLEdBQUcsRUFBRSxDQUM1Qiw0QkFBNEIsQ0FBQyxRQUFRLENBQUMsWUFBWSxDQUFDLENBQ3BELENBQUM7UUFFRix5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QUVELE1BQU0sUUFBUSxDQUFDLFFBQVEsQ0FBQyxpQkFBaUIsRUFBRSxDQUFDO2dCQUM1QyxRQUFRLENBQUMsYUFBYSxFQUFFLENBQUM7WUFDM0IsQ0FBQztTQUNGLENBQUMsQ0FBQztRQUVILGtDQUFrQztRQUNsQyxJQUFJLE9BQU8sRUFBRTtZQUNYLE9BQU8sQ0FBQyxPQUFPLENBQUM7Z0JBQ2QsT0FBTyxFQUFFLFlBQVk7Z0JBQ3JCLFFBQVEsRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFdBQVcsQ0FBQzthQUNoQyxDQUFDLENBQUM7WUFDSCxPQUFPLENBQUMsT0FBTyxDQUFDO2dCQUNkLE9BQU8sRUFBRSxXQUFXO2dCQUNwQixRQUFRLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxXQUFXLENBQUM7YUFDaEMsQ0FBQyxDQUFDO1lBQ0gsT0FBTyxDQUFDLE9BQU8sQ0FBQztnQkFDZCxPQUFPLEVBQUUsV0FBVztnQkFDcEIsUUFBUSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsV0FBVyxDQUFDO2FBQ2hDLENBQUMsQ0FBQztTQUNKO1FBRUQsc0NBQXNDO1FBQ3RDLE9BQU8sUUFBUSxDQUFDO0lBQ2xCLENBQUM7Q0FDRixDQUFDO0FBRUYsaUVBQWUsQ0FBQyxTQUFTLEVBQUUsc0JBQXNCLENBQUMsRUFBQyIsImZpbGUiOiJwYWNrYWdlc19kb2N1bWVudHNlYXJjaC1leHRlbnNpb25fbGliX2luZGV4X2pzLV82NTE1MC45ZThlMDU2ZmZiM2YxOTQ5MjkyNS5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGRvY3VtZW50c2VhcmNoLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTaGVsbCxcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuXG5pbXBvcnQgeyBJQ29tbWFuZFBhbGV0dGUgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5cbmltcG9ydCB7XG4gIENvZGVNaXJyb3JTZWFyY2hQcm92aWRlcixcbiAgSVNlYXJjaFByb3ZpZGVyUmVnaXN0cnksXG4gIE5vdGVib29rU2VhcmNoUHJvdmlkZXIsXG4gIFNlYXJjaEluc3RhbmNlLFxuICBTZWFyY2hQcm92aWRlclJlZ2lzdHJ5XG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY3VtZW50c2VhcmNoJztcblxuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG5jb25zdCBTRUFSQ0hBQkxFX0NMQVNTID0gJ2pwLW1vZC1zZWFyY2hhYmxlJztcblxuY29uc3QgbGFiU2hlbGxXaWRnZXRMaXN0ZW5lcjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2RvY3VtZW50c2VhcmNoOmxhYlNoZWxsV2lkZ2V0TGlzdGVuZXInLFxuICByZXF1aXJlczogW0lMYWJTaGVsbCwgSVNlYXJjaFByb3ZpZGVyUmVnaXN0cnldLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCxcbiAgICByZWdpc3RyeTogSVNlYXJjaFByb3ZpZGVyUmVnaXN0cnlcbiAgKSA9PiB7XG4gICAgLy8gSWYgYSBnaXZlbiB3aWRnZXQgaXMgc2VhcmNoYWJsZSwgYXBwbHkgdGhlIHNlYXJjaGFibGUgY2xhc3MuXG4gICAgLy8gSWYgaXQncyBub3Qgc2VhcmNoYWJsZSwgcmVtb3ZlIHRoZSBjbGFzcy5cbiAgICBjb25zdCB0cmFuc2Zvcm1XaWRnZXRTZWFyY2hhYmlsaXR5ID0gKHdpZGdldDogV2lkZ2V0IHwgbnVsbCkgPT4ge1xuICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgcHJvdmlkZXJGb3JXaWRnZXQgPSByZWdpc3RyeS5nZXRQcm92aWRlckZvcldpZGdldCh3aWRnZXQpO1xuICAgICAgaWYgKHByb3ZpZGVyRm9yV2lkZ2V0KSB7XG4gICAgICAgIHdpZGdldC5hZGRDbGFzcyhTRUFSQ0hBQkxFX0NMQVNTKTtcbiAgICAgIH1cbiAgICAgIGlmICghcHJvdmlkZXJGb3JXaWRnZXQpIHtcbiAgICAgICAgd2lkZ2V0LnJlbW92ZUNsYXNzKFNFQVJDSEFCTEVfQ0xBU1MpO1xuICAgICAgfVxuICAgIH07XG5cbiAgICAvLyBVcGRhdGUgc2VhcmNoYWJpbGl0eSBvZiB0aGUgYWN0aXZlIHdpZGdldCB3aGVuIHRoZSByZWdpc3RyeVxuICAgIC8vIGNoYW5nZXMsIGluIGNhc2UgYSBwcm92aWRlciBmb3IgdGhlIGN1cnJlbnQgd2lkZ2V0IHdhcyBhZGRlZFxuICAgIC8vIG9yIHJlbW92ZWRcbiAgICByZWdpc3RyeS5jaGFuZ2VkLmNvbm5lY3QoKCkgPT5cbiAgICAgIHRyYW5zZm9ybVdpZGdldFNlYXJjaGFiaWxpdHkobGFiU2hlbGwuYWN0aXZlV2lkZ2V0KVxuICAgICk7XG5cbiAgICAvLyBBcHBseSB0aGUgc2VhcmNoYWJsZSBjbGFzcyBvbmx5IHRvIHRoZSBhY3RpdmUgd2lkZ2V0IGlmIGl0IGlzIGFjdHVhbGx5XG4gICAgLy8gc2VhcmNoYWJsZS4gUmVtb3ZlIHRoZSBzZWFyY2hhYmxlIGNsYXNzIGZyb20gYSB3aWRnZXQgd2hlbiBpdCdzXG4gICAgLy8gbm8gbG9uZ2VyIGFjdGl2ZS5cbiAgICBsYWJTaGVsbC5hY3RpdmVDaGFuZ2VkLmNvbm5lY3QoKF8sIGFyZ3MpID0+IHtcbiAgICAgIGNvbnN0IG9sZFdpZGdldCA9IGFyZ3Mub2xkVmFsdWU7XG4gICAgICBpZiAob2xkV2lkZ2V0KSB7XG4gICAgICAgIG9sZFdpZGdldC5yZW1vdmVDbGFzcyhTRUFSQ0hBQkxFX0NMQVNTKTtcbiAgICAgIH1cbiAgICAgIHRyYW5zZm9ybVdpZGdldFNlYXJjaGFiaWxpdHkoYXJncy5uZXdWYWx1ZSk7XG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogSW5pdGlhbGl6YXRpb24gZGF0YSBmb3IgdGhlIGRvY3VtZW50LXNlYXJjaCBleHRlbnNpb24uXG4gKi9cbmNvbnN0IGV4dGVuc2lvbjogSnVweXRlckZyb250RW5kUGx1Z2luPElTZWFyY2hQcm92aWRlclJlZ2lzdHJ5PiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kb2N1bWVudHNlYXJjaDpwbHVnaW4nLFxuICBwcm92aWRlczogSVNlYXJjaFByb3ZpZGVyUmVnaXN0cnksXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZV0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGVcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIC8vIENyZWF0ZSByZWdpc3RyeSwgcmV0cmlldmUgYWxsIGRlZmF1bHQgcHJvdmlkZXJzXG4gICAgY29uc3QgcmVnaXN0cnk6IFNlYXJjaFByb3ZpZGVyUmVnaXN0cnkgPSBuZXcgU2VhcmNoUHJvdmlkZXJSZWdpc3RyeSgpO1xuXG4gICAgLy8gUmVnaXN0ZXIgZGVmYXVsdCBpbXBsZW1lbnRhdGlvbnMgb2YgdGhlIE5vdGVib29rIGFuZCBDb2RlTWlycm9yIHNlYXJjaCBwcm92aWRlcnNcbiAgICByZWdpc3RyeS5yZWdpc3RlcignanAtbm90ZWJvb2tTZWFyY2hQcm92aWRlcicsIE5vdGVib29rU2VhcmNoUHJvdmlkZXIpO1xuICAgIHJlZ2lzdHJ5LnJlZ2lzdGVyKCdqcC1jb2RlTWlycm9yU2VhcmNoUHJvdmlkZXInLCBDb2RlTWlycm9yU2VhcmNoUHJvdmlkZXIpO1xuXG4gICAgY29uc3QgYWN0aXZlU2VhcmNoZXMgPSBuZXcgTWFwPHN0cmluZywgU2VhcmNoSW5zdGFuY2U+KCk7XG5cbiAgICBjb25zdCBzdGFydENvbW1hbmQ6IHN0cmluZyA9ICdkb2N1bWVudHNlYXJjaDpzdGFydCc7XG4gICAgY29uc3Qgc3RhcnRSZXBsYWNlQ29tbWFuZDogc3RyaW5nID0gJ2RvY3VtZW50c2VhcmNoOnN0YXJ0V2l0aFJlcGxhY2UnO1xuICAgIGNvbnN0IG5leHRDb21tYW5kOiBzdHJpbmcgPSAnZG9jdW1lbnRzZWFyY2g6aGlnaGxpZ2h0TmV4dCc7XG4gICAgY29uc3QgcHJldkNvbW1hbmQ6IHN0cmluZyA9ICdkb2N1bWVudHNlYXJjaDpoaWdobGlnaHRQcmV2aW91cyc7XG5cbiAgICBjb25zdCBjdXJyZW50V2lkZ2V0SGFzU2VhcmNoUHJvdmlkZXIgPSAoKSA9PiB7XG4gICAgICBjb25zdCBjdXJyZW50V2lkZ2V0ID0gYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBpZiAoIWN1cnJlbnRXaWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHJlZ2lzdHJ5LmdldFByb3ZpZGVyRm9yV2lkZ2V0KGN1cnJlbnRXaWRnZXQpICE9PSB1bmRlZmluZWQ7XG4gICAgfTtcbiAgICBjb25zdCBnZXRDdXJyZW50V2lkZ2V0U2VhcmNoSW5zdGFuY2UgPSAoKSA9PiB7XG4gICAgICBjb25zdCBjdXJyZW50V2lkZ2V0ID0gYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBpZiAoIWN1cnJlbnRXaWRnZXQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3Qgd2lkZ2V0SWQgPSBjdXJyZW50V2lkZ2V0LmlkO1xuICAgICAgbGV0IHNlYXJjaEluc3RhbmNlID0gYWN0aXZlU2VhcmNoZXMuZ2V0KHdpZGdldElkKTtcbiAgICAgIGlmICghc2VhcmNoSW5zdGFuY2UpIHtcbiAgICAgICAgY29uc3Qgc2VhcmNoUHJvdmlkZXIgPSByZWdpc3RyeS5nZXRQcm92aWRlckZvcldpZGdldChjdXJyZW50V2lkZ2V0KTtcbiAgICAgICAgaWYgKCFzZWFyY2hQcm92aWRlcikge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBzZWFyY2hJbnN0YW5jZSA9IG5ldyBTZWFyY2hJbnN0YW5jZShcbiAgICAgICAgICBjdXJyZW50V2lkZ2V0LFxuICAgICAgICAgIHNlYXJjaFByb3ZpZGVyLFxuICAgICAgICAgIHRyYW5zbGF0b3JcbiAgICAgICAgKTtcblxuICAgICAgICBhY3RpdmVTZWFyY2hlcy5zZXQod2lkZ2V0SWQsIHNlYXJjaEluc3RhbmNlKTtcbiAgICAgICAgLy8gZmluZCBuZXh0IGFuZCBwcmV2aW91cyBhcmUgbm93IGVuYWJsZWRcbiAgICAgICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKCk7XG5cbiAgICAgICAgc2VhcmNoSW5zdGFuY2UuZGlzcG9zZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgICAgYWN0aXZlU2VhcmNoZXMuZGVsZXRlKHdpZGdldElkKTtcbiAgICAgICAgICAvLyBmaW5kIG5leHQgYW5kIHByZXZpb3VzIGFyZSBub3cgbm90IGVuYWJsZWRcbiAgICAgICAgICBhcHAuY29tbWFuZHMubm90aWZ5Q29tbWFuZENoYW5nZWQoKTtcbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgICByZXR1cm4gc2VhcmNoSW5zdGFuY2U7XG4gICAgfTtcblxuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKHN0YXJ0Q29tbWFuZCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdGaW5k4oCmJyksXG4gICAgICBpc0VuYWJsZWQ6IGN1cnJlbnRXaWRnZXRIYXNTZWFyY2hQcm92aWRlcixcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgc2VhcmNoSW5zdGFuY2UgPSBnZXRDdXJyZW50V2lkZ2V0U2VhcmNoSW5zdGFuY2UoKTtcbiAgICAgICAgaWYgKHNlYXJjaEluc3RhbmNlKSB7XG4gICAgICAgICAgc2VhcmNoSW5zdGFuY2UuZm9jdXNJbnB1dCgpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChzdGFydFJlcGxhY2VDb21tYW5kLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0ZpbmQgYW5kIFJlcGxhY2XigKYnKSxcbiAgICAgIGlzRW5hYmxlZDogY3VycmVudFdpZGdldEhhc1NlYXJjaFByb3ZpZGVyLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCBzZWFyY2hJbnN0YW5jZSA9IGdldEN1cnJlbnRXaWRnZXRTZWFyY2hJbnN0YW5jZSgpO1xuICAgICAgICBpZiAoc2VhcmNoSW5zdGFuY2UpIHtcbiAgICAgICAgICBzZWFyY2hJbnN0YW5jZS5zaG93UmVwbGFjZSgpO1xuICAgICAgICAgIHNlYXJjaEluc3RhbmNlLmZvY3VzSW5wdXQoKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQobmV4dENvbW1hbmQsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnRmluZCBOZXh0JyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgY29uc3QgY3VycmVudFdpZGdldCA9IGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0O1xuICAgICAgICBpZiAoIWN1cnJlbnRXaWRnZXQpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGFjdGl2ZVNlYXJjaGVzLmhhcyhjdXJyZW50V2lkZ2V0LmlkKTtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGNvbnN0IGN1cnJlbnRXaWRnZXQgPSBhcHAuc2hlbGwuY3VycmVudFdpZGdldDtcbiAgICAgICAgaWYgKCFjdXJyZW50V2lkZ2V0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IGluc3RhbmNlID0gYWN0aXZlU2VhcmNoZXMuZ2V0KGN1cnJlbnRXaWRnZXQuaWQpO1xuICAgICAgICBpZiAoIWluc3RhbmNlKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgYXdhaXQgaW5zdGFuY2UucHJvdmlkZXIuaGlnaGxpZ2h0TmV4dCgpO1xuICAgICAgICBpbnN0YW5jZS51cGRhdGVJbmRpY2VzKCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChwcmV2Q29tbWFuZCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdGaW5kIFByZXZpb3VzJyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgY29uc3QgY3VycmVudFdpZGdldCA9IGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0O1xuICAgICAgICBpZiAoIWN1cnJlbnRXaWRnZXQpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGFjdGl2ZVNlYXJjaGVzLmhhcyhjdXJyZW50V2lkZ2V0LmlkKTtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGNvbnN0IGN1cnJlbnRXaWRnZXQgPSBhcHAuc2hlbGwuY3VycmVudFdpZGdldDtcbiAgICAgICAgaWYgKCFjdXJyZW50V2lkZ2V0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IGluc3RhbmNlID0gYWN0aXZlU2VhcmNoZXMuZ2V0KGN1cnJlbnRXaWRnZXQuaWQpO1xuICAgICAgICBpZiAoIWluc3RhbmNlKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgYXdhaXQgaW5zdGFuY2UucHJvdmlkZXIuaGlnaGxpZ2h0UHJldmlvdXMoKTtcbiAgICAgICAgaW5zdGFuY2UudXBkYXRlSW5kaWNlcygpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gQWRkIHRoZSBjb21tYW5kIHRvIHRoZSBwYWxldHRlLlxuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICBjb21tYW5kOiBzdGFydENvbW1hbmQsXG4gICAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnTWFpbiBBcmVhJylcbiAgICAgIH0pO1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgY29tbWFuZDogbmV4dENvbW1hbmQsXG4gICAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnTWFpbiBBcmVhJylcbiAgICAgIH0pO1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgY29tbWFuZDogcHJldkNvbW1hbmQsXG4gICAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnTWFpbiBBcmVhJylcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIC8vIFByb3ZpZGUgdGhlIHJlZ2lzdHJ5IHRvIHRoZSBzeXN0ZW0uXG4gICAgcmV0dXJuIHJlZ2lzdHJ5O1xuICB9XG59O1xuXG5leHBvcnQgZGVmYXVsdCBbZXh0ZW5zaW9uLCBsYWJTaGVsbFdpZGdldExpc3RlbmVyXTtcbiJdLCJzb3VyY2VSb290IjoiIn0=