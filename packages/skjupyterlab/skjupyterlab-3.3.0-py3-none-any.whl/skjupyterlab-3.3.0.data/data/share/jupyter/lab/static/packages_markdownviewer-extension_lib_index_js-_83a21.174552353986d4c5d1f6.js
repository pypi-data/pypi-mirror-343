(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_markdownviewer-extension_lib_index_js-_83a21"],{

/***/ "../packages/markdownviewer-extension/lib/index.js":
/*!*********************************************************!*\
  !*** ../packages/markdownviewer-extension/lib/index.js ***!
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
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/markdownviewer */ "webpack/sharing/consume/default/@jupyterlab/markdownviewer/@jupyterlab/markdownviewer");
/* harmony import */ var _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module markdownviewer-extension
 */







/**
 * The command IDs used by the markdownviewer plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.markdownPreview = 'markdownviewer:open';
    CommandIDs.markdownEditor = 'markdownviewer:edit';
})(CommandIDs || (CommandIDs = {}));
/**
 * The name of the factory that creates markdown viewer widgets.
 */
const FACTORY = 'Markdown Preview';
/**
 * The markdown viewer plugin.
 */
const plugin = {
    activate,
    id: '@jupyterlab/markdownviewer-extension:plugin',
    provides: _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__.IMarkdownViewerTracker,
    requires: [_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry],
    autoStart: true
};
/**
 * Activate the markdown viewer plugin.
 */
function activate(app, rendermime, translator, restorer, settingRegistry) {
    const trans = translator.load('jupyterlab');
    const { commands, docRegistry } = app;
    // Add the markdown renderer factory.
    rendermime.addFactory(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.markdownRendererFactory);
    const namespace = 'markdownviewer-widget';
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    let config = Object.assign({}, _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__.MarkdownViewer.defaultConfig);
    /**
     * Update the settings of a widget.
     */
    function updateWidget(widget) {
        Object.keys(config).forEach((k) => {
            var _a;
            widget.setOption(k, (_a = config[k]) !== null && _a !== void 0 ? _a : null);
        });
    }
    if (settingRegistry) {
        const updateSettings = (settings) => {
            config = settings.composite;
            tracker.forEach(widget => {
                updateWidget(widget.content);
            });
        };
        // Fetch the initial state of the settings.
        settingRegistry
            .load(plugin.id)
            .then((settings) => {
            settings.changed.connect(() => {
                updateSettings(settings);
            });
            updateSettings(settings);
        })
            .catch((reason) => {
            console.error(reason.message);
        });
    }
    // Register the MarkdownViewer factory.
    const factory = new _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__.MarkdownViewerFactory({
        rendermime,
        name: FACTORY,
        primaryFileType: docRegistry.getFileType('markdown'),
        fileTypes: ['markdown'],
        defaultRendered: ['markdown']
    });
    factory.widgetCreated.connect((sender, widget) => {
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        // Handle the settings of new widgets.
        updateWidget(widget.content);
        void tracker.add(widget);
    });
    docRegistry.addWidgetFactory(factory);
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY }),
            name: widget => widget.context.path
        });
    }
    commands.addCommand(CommandIDs.markdownPreview, {
        label: trans.__('Markdown Preview'),
        execute: args => {
            const path = args['path'];
            if (typeof path !== 'string') {
                return;
            }
            return commands.execute('docmanager:open', {
                path,
                factory: FACTORY,
                options: args['options']
            });
        }
    });
    commands.addCommand(CommandIDs.markdownEditor, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (!widget) {
                return;
            }
            const path = widget.context.path;
            return commands.execute('docmanager:open', {
                path,
                factory: 'Editor',
                options: {
                    mode: 'split-right'
                }
            });
        },
        isVisible: () => {
            const widget = tracker.currentWidget;
            return ((widget && _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.extname(widget.context.path) === '.md') || false);
        },
        label: trans.__('Show Markdown Editor')
    });
    return tracker;
}
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFya2Rvd252aWV3ZXItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU04QjtBQUNvQjtBQUNMO0FBTVo7QUFJSjtBQUMrQjtBQUNUO0FBRXREOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBR25CO0FBSEQsV0FBVSxVQUFVO0lBQ0wsMEJBQWUsR0FBRyxxQkFBcUIsQ0FBQztJQUN4Qyx5QkFBYyxHQUFHLHFCQUFxQixDQUFDO0FBQ3RELENBQUMsRUFIUyxVQUFVLEtBQVYsVUFBVSxRQUduQjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxPQUFPLEdBQUcsa0JBQWtCLENBQUM7QUFFbkM7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBa0Q7SUFDNUQsUUFBUTtJQUNSLEVBQUUsRUFBRSw2Q0FBNkM7SUFDakQsUUFBUSxFQUFFLDhFQUFzQjtJQUNoQyxRQUFRLEVBQUUsQ0FBQyx1RUFBbUIsRUFBRSxnRUFBVyxDQUFDO0lBQzVDLFFBQVEsRUFBRSxDQUFDLG9FQUFlLEVBQUUseUVBQWdCLENBQUM7SUFDN0MsU0FBUyxFQUFFLElBQUk7Q0FDaEIsQ0FBQztBQUVGOztHQUVHO0FBQ0gsU0FBUyxRQUFRLENBQ2YsR0FBb0IsRUFDcEIsVUFBK0IsRUFDL0IsVUFBdUIsRUFDdkIsUUFBZ0MsRUFDaEMsZUFBd0M7SUFFeEMsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUM1QyxNQUFNLEVBQUUsUUFBUSxFQUFFLFdBQVcsRUFBRSxHQUFHLEdBQUcsQ0FBQztJQUV0QyxxQ0FBcUM7SUFDckMsVUFBVSxDQUFDLFVBQVUsQ0FBQywyRUFBdUIsQ0FBQyxDQUFDO0lBRS9DLE1BQU0sU0FBUyxH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Q0FBQyxzQkFBc0IsQ0FBQztLQUN4QyxDQUFDLENBQUM7SUFFSCxPQUFPLE9BQU8sQ0FBQztBQUNqQixDQUFDO0FBRUQ7O0dBRUc7QUFDSCxpRUFBZSxNQUFNLEVBQUMiLCJmaWxlIjoicGFja2FnZXNfbWFya2Rvd252aWV3ZXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy1fODNhMjEuMTc0NTUyMzUzOTg2ZDRjNWQxZjYuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBtYXJrZG93bnZpZXdlci1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGF5b3V0UmVzdG9yZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IFdpZGdldFRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBQYXRoRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIElNYXJrZG93blZpZXdlclRyYWNrZXIsXG4gIE1hcmtkb3duRG9jdW1lbnQsXG4gIE1hcmtkb3duVmlld2VyLFxuICBNYXJrZG93blZpZXdlckZhY3Rvcnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvbWFya2Rvd252aWV3ZXInO1xuaW1wb3J0IHtcbiAgSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgbWFya2Rvd25SZW5kZXJlckZhY3Rvcnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBtYXJrZG93bnZpZXdlciBwbHVnaW4uXG4gKi9cbm5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IG1hcmtkb3duUHJldmlldyA9ICdtYXJrZG93bnZpZXdlcjpvcGVuJztcbiAgZXhwb3J0IGNvbnN0IG1hcmtkb3duRWRpdG9yID0gJ21hcmtkb3dudmlld2VyOmVkaXQnO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lIG9mIHRoZSBmYWN0b3J5IHRoYXQgY3JlYXRlcyBtYXJrZG93biB2aWV3ZXIgd2lkZ2V0cy5cbiAqL1xuY29uc3QgRkFDVE9SWSA9ICdNYXJrZG93biBQcmV2aWV3JztcblxuLyoqXG4gKiBUaGUgbWFya2Rvd24gdmlld2VyIHBsdWdpbi5cbiAqL1xuY29uc3QgcGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SU1hcmtkb3duVmlld2VyVHJhY2tlcj4gPSB7XG4gIGFjdGl2YXRlLFxuICBpZDogJ0BqdXB5dGVybGFiL21hcmtkb3dudmlld2VyLWV4dGVuc2lvbjpwbHVnaW4nLFxuICBwcm92aWRlczogSU1hcmtkb3duVmlld2VyVHJhY2tlcixcbiAgcmVxdWlyZXM6IFtJUmVuZGVyTWltZVJlZ2lzdHJ5LCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUxheW91dFJlc3RvcmVyLCBJU2V0dGluZ1JlZ2lzdHJ5XSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBtYXJrZG93biB2aWV3ZXIgcGx1Z2luLlxuICovXG5mdW5jdGlvbiBhY3RpdmF0ZShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbCxcbiAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5IHwgbnVsbFxuKTogSU1hcmtkb3duVmlld2VyVHJhY2tlciB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgY29tbWFuZHMsIGRvY1JlZ2lzdHJ5IH0gPSBhcHA7XG5cbiAgLy8gQWRkIHRoZSBtYXJrZG93biByZW5kZXJlciBmYWN0b3J5LlxuICByZW5kZXJtaW1lLmFkZEZhY3RvcnkobWFya2Rvd25SZW5kZXJlckZhY3RvcnkpO1xuXG4gIGNvbnN0IG5hbWVzcGFjZSA9ICdtYXJrZG93bnZpZXdlci13aWRnZXQnO1xuICBjb25zdCB0cmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8TWFya2Rvd25Eb2N1bWVudD4oe1xuICAgIG5hbWVzcGFjZVxuICB9KTtcblxuICBsZXQgY29uZmlnOiBQYXJ0aWFsPE1hcmtkb3duVmlld2VyLklDb25maWc+ID0ge1xuICAgIC4uLk1hcmtkb3duVmlld2VyLmRlZmF1bHRDb25maWdcbiAgfTtcblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBzZXR0aW5ncyBvZiBhIHdpZGdldC5cbiAgICovXG4gIGZ1bmN0aW9uIHVwZGF0ZVdpZGdldCh3aWRnZXQ6IE1hcmtkb3duVmlld2VyKTogdm9pZCB7XG4gICAgT2JqZWN0LmtleXMoY29uZmlnKS5mb3JFYWNoKChrOiBrZXlvZiBNYXJrZG93blZpZXdlci5JQ29uZmlnKSA9PiB7XG4gICAgICB3aWRnZXQuc2V0T3B0aW9uKGssIGNvbmZpZ1trXSA/PyBudWxsKTtcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICBjb25zdCB1cGRhdGVTZXR0aW5ncyA9IChzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MpID0+IHtcbiAgICAgIGNvbmZpZyA9IHNldHRpbmdzLmNvbXBvc2l0ZSBhcyBQYXJ0aWFsPE1hcmtkb3duVmlld2VyLklDb25maWc+O1xuICAgICAgdHJhY2tlci5mb3JFYWNoKHdpZGdldCA9PiB7XG4gICAgICAgIHVwZGF0ZVdpZGdldCh3aWRnZXQuY29udGVudCk7XG4gICAgICB9KTtcbiAgICB9O1xuXG4gICAgLy8gRmV0Y2ggdGhlIGluaXRpYWwgc3RhdGUgb2YgdGhlIHNldHRpbmdzLlxuICAgIHNldHRpbmdSZWdpc3RyeVxuICAgICAgLmxvYWQocGx1Z2luLmlkKVxuICAgICAgLnRoZW4oKHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncykgPT4ge1xuICAgICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgICAgfSk7XG4gICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goKHJlYXNvbjogRXJyb3IpID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcihyZWFzb24ubWVzc2FnZSk7XG4gICAgICB9KTtcbiAgfVxuXG4gIC8vIFJlZ2lzdGVyIHRoZSBNYXJrZG93blZpZXdlciBmYWN0b3J5LlxuICBjb25zdCBmYWN0b3J5ID0gbmV3IE1hcmtkb3duVmlld2VyRmFjdG9yeSh7XG4gICAgcmVuZGVybWltZSxcbiAgICBuYW1lOiBGQUNUT1JZLFxuICAgIHByaW1hcnlGaWxlVHlwZTogZG9jUmVnaXN0cnkuZ2V0RmlsZVR5cGUoJ21hcmtkb3duJyksXG4gICAgZmlsZVR5cGVzOiBbJ21hcmtkb3duJ10sXG4gICAgZGVmYXVsdFJlbmRlcmVkOiBbJ21hcmtkb3duJ11cbiAgfSk7XG4gIGZhY3Rvcnkud2lkZ2V0Q3JlYXRlZC5jb25uZWN0KChzZW5kZXIsIHdpZGdldCkgPT4ge1xuICAgIC8vIE5vdGlmeSB0aGUgd2lkZ2V0IHRyYWNrZXIgaWYgcmVzdG9yZSBkYXRhIG5lZWRzIHRvIHVwZGF0ZS5cbiAgICB3aWRnZXQuY29udGV4dC5wYXRoQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHZvaWQgdHJhY2tlci5zYXZlKHdpZGdldCk7XG4gICAgfSk7XG4gICAgLy8gSGFuZGxlIHRoZSBzZXR0aW5ncyBvZiBuZXcgd2lkZ2V0cy5cbiAgICB1cGRhdGVXaWRnZXQod2lkZ2V0LmNvbnRlbnQpO1xuICAgIHZvaWQgdHJhY2tlci5hZGQod2lkZ2V0KTtcbiAgfSk7XG4gIGRvY1JlZ2lzdHJ5LmFkZFdpZGdldEZhY3RvcnkoZmFjdG9yeSk7XG5cbiAgLy8gSGFuZGxlIHN0YXRlIHJlc3RvcmF0aW9uLlxuICBpZiAocmVzdG9yZXIpIHtcbiAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwge1xuICAgICAgY29tbWFuZDogJ2RvY21hbmFnZXI6b3BlbicsXG4gICAgICBhcmdzOiB3aWRnZXQgPT4gKHsgcGF0aDogd2lkZ2V0LmNvbnRleHQucGF0aCwgZmFjdG9yeTogRkFDVE9SWSB9KSxcbiAgICAgIG5hbWU6IHdpZGdldCA9PiB3aWRnZXQuY29udGV4dC5wYXRoXG4gICAgfSk7XG4gIH1cblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubWFya2Rvd25QcmV2aWV3LCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdNYXJrZG93biBQcmV2aWV3JyksXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBwYXRoID0gYXJnc1sncGF0aCddO1xuICAgICAgaWYgKHR5cGVvZiBwYXRoICE9PSAnc3RyaW5nJykge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnZG9jbWFuYWdlcjpvcGVuJywge1xuICAgICAgICBwYXRoLFxuICAgICAgICBmYWN0b3J5OiBGQUNUT1JZLFxuICAgICAgICBvcHRpb25zOiBhcmdzWydvcHRpb25zJ11cbiAgICAgIH0pO1xuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm1hcmtkb3duRWRpdG9yLCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgcGF0aCA9IHdpZGdldC5jb250ZXh0LnBhdGg7XG4gICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnZG9jbWFuYWdlcjpvcGVuJywge1xuICAgICAgICBwYXRoLFxuICAgICAgICBmYWN0b3J5OiAnRWRpdG9yJyxcbiAgICAgICAgb3B0aW9uczoge1xuICAgICAgICAgIG1vZGU6ICdzcGxpdC1yaWdodCdcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfSxcbiAgICBpc1Zpc2libGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICAgIHJldHVybiAoXG4gICAgICAgICh3aWRnZXQgJiYgUGF0aEV4dC5leHRuYW1lKHdpZGdldC5jb250ZXh0LnBhdGgpID09PSAnLm1kJykgfHwgZmFsc2VcbiAgICAgICk7XG4gICAgfSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Nob3cgTWFya2Rvd24gRWRpdG9yJylcbiAgfSk7XG5cbiAgcmV0dXJuIHRyYWNrZXI7XG59XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW4gYXMgZGVmYXVsdC5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2luO1xuIl0sInNvdXJjZVJvb3QiOiIifQ==