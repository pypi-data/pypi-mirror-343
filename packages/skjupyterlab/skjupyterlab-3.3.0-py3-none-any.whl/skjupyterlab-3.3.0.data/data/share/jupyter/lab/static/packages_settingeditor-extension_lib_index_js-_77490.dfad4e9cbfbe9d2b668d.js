(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_settingeditor-extension_lib_index_js-_77490"],{

/***/ "../packages/settingeditor-extension/lib/index.js":
/*!********************************************************!*\
  !*** ../packages/settingeditor-extension/lib/index.js ***!
  \********************************************************/
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
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingeditor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingeditor */ "webpack/sharing/consume/default/@jupyterlab/settingeditor/@jupyterlab/settingeditor");
/* harmony import */ var _jupyterlab_settingeditor__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingeditor__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module settingeditor-extension
 */









/**
 * The command IDs used by the setting editor.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'settingeditor:open';
    CommandIDs.revert = 'settingeditor:revert';
    CommandIDs.save = 'settingeditor:save';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default setting editor extension.
 */
const plugin = {
    id: '@jupyterlab/settingeditor-extension:plugin',
    requires: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry,
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices,
        _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6__.IStateDB,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IRenderMimeRegistry,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator
    ],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true,
    provides: _jupyterlab_settingeditor__WEBPACK_IMPORTED_MODULE_4__.ISettingEditorTracker,
    activate
};
/**
 * Activate the setting editor extension.
 */
function activate(app, restorer, registry, editorServices, state, rendermime, status, translator, palette) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const namespace = 'setting-editor';
    const factoryService = editorServices.factoryService;
    const editorFactory = factoryService.newInlineEditor;
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    let editor;
    // Handle state restoration.
    void restorer.restore(tracker, {
        command: CommandIDs.open,
        args: widget => ({}),
        name: widget => namespace
    });
    commands.addCommand(CommandIDs.open, {
        execute: () => {
            if (tracker.currentWidget) {
                shell.activateById(tracker.currentWidget.id);
                return;
            }
            const key = plugin.id;
            const when = app.restored;
            editor = new _jupyterlab_settingeditor__WEBPACK_IMPORTED_MODULE_4__.SettingEditor({
                commands: {
                    registry: commands,
                    revert: CommandIDs.revert,
                    save: CommandIDs.save
                },
                editorFactory,
                key,
                registry,
                rendermime,
                state,
                translator,
                when
            });
            let disposable = null;
            // Notify the command registry when the visibility status of the setting
            // editor's commands change. The setting editor toolbar listens for this
            // signal from the command registry.
            editor.commandsChanged.connect((sender, args) => {
                args.forEach(id => {
                    commands.notifyCommandChanged(id);
                });
                if (editor.canSaveRaw) {
                    if (!disposable) {
                        disposable = status.setDirty();
                    }
                }
                else if (disposable) {
                    disposable.dispose();
                    disposable = null;
                }
                editor.disposed.connect(() => {
                    if (disposable) {
                        disposable.dispose();
                    }
                });
            });
            editor.id = namespace;
            editor.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.settingsIcon;
            editor.title.label = trans.__('Settings');
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: editor });
            void tracker.add(main);
            shell.add(main);
        },
        label: trans.__('Advanced Settings Editor')
    });
    if (palette) {
        palette.addItem({
            category: trans.__('Settings'),
            command: CommandIDs.open
        });
    }
    commands.addCommand(CommandIDs.revert, {
        execute: () => {
            var _a;
            (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.revert();
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.undoIcon,
        label: trans.__('Revert User Settings'),
        isEnabled: () => { var _a, _b; return (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.canRevertRaw) !== null && _b !== void 0 ? _b : false; }
    });
    commands.addCommand(CommandIDs.save, {
        execute: () => { var _a; return (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.save(); },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.saveIcon,
        label: trans.__('Save User Settings'),
        isEnabled: () => { var _a, _b; return (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.canSaveRaw) !== null && _b !== void 0 ? _b : false; }
    });
    return tracker;
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2V0dGluZ2VkaXRvci1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFPOEI7QUFLSDtBQUMyQjtBQUNJO0FBSTFCO0FBQzRCO0FBQ2hCO0FBQ087QUFDdUI7QUFHN0U7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FNbkI7QUFORCxXQUFVLFVBQVU7SUFDTCxlQUFJLEdBQUcsb0JBQW9CLENBQUM7SUFFNUIsaUJBQU0sR0FBRyxzQkFBc0IsQ0FBQztJQUVoQyxlQUFJLEdBQUcsb0JBQW9CLENBQUM7QUFDM0MsQ0FBQyxFQU5TLFVBQVUsS0FBVixVQUFVLFFBTW5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBaUQ7SUFDM0QsRUFBRSxFQUFFLDRDQUE0QztJQUNoRCxRQUFRLEVBQUU7UUFDUixvRUFBZTtRQUNmLHlFQUFnQjtRQUNoQixtRUFBZTtRQUNmLHlEQUFRO1FBQ1IsdUVBQW1CO1FBQ25CLCtEQUFVO1FBQ1YsZ0VBQVc7S0FDWjtJQUNELFFBQVEsRUFBRSxDQUFDLGlFQUFlLENBQUM7SUFDM0IsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsNEVBQXFCO0lBQy9CLFFBQVE7Q0FDVCxDQUFDO0FBRUY7O0dBRUc7QUFDSCxTQUFTLFFBQVEsQ0FDZixHQUFvQixFQUNwQixRQUF5QixFQUN6QixRQUEwQixFQUMxQixjQUErQixFQUMvQixLQUFlLEVBQ2YsVUFBK0IsRUFDL0IsTUFBa0IsRUFDbEIsVUFBdUIsRUFDdkIsT0FBK0I7SUFFL0IsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUM1QyxNQUFNLEVBQUUsUUFBUSxFQUFFLEtBQUssRUFBRSxHQUFHLEdBQUcsQ0FBQztJQUNoQyxNQUFNLFNBQVMsR0FBRyxnQkFBZ0IsQ0FBQztJQUNuQyxNQUFNLGNBQWMsR0FBRyxjQUFjLENBQUMsY0FBYyxDQUFDO0lBQ3JELE1BQU0sYUFBYSxHQUFHLGNBQWMsQ0FBQyxlQUFlLENBQUM7SUFDckQsTUFBTSxPQUFPLEdBQUcsSUFBSSwrREFBYSxDQUFnQztRQUMvRCxTQUFTO0tBQ1YsQ0FBQyxDQUFDO0lBQ0gsSUFBSSxNQUFxQixDQUFDO0lBRTFCLDRCQUE0QjtJQUM1QixLQUFLLFFBQVEsQ0FBQyxPQUFPLENBQUMsT0FBTyxFQUFFO1FBQzdCLE9BQU8sRUFBRSxVQUFVLENBQUMsSUFBSTtRQUN4QixJQUFJLEVBQUUsTUFBTSxDQUFDLEVBQUUsQ0FBQyxDQUFDLEVBQUUsQ0FBQztRQUNwQixJQUFJLEVBQUUsTUFBTSxDQUFDLEVBQUUsQ0FBQyxTQUFTO0tBQzFCLENBQUMsQ0FBQztJQUVILFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLElBQUksRUFBRTtRQUNuQyxPQUFPLEVBQUUsR0FBRyxFQUFFO1lBQ1osSUFBSSxPQUFPLENBQUMsYUFBYSxFQUFFO2dCQUN6QixLQUFLLENBQUMsWUFBWSxDQUFDLE9BQU8sQ0FBQyxhQUFhLENBQUMsRUFBRSxDQUFDLENBQUM7Z0JBQzdDLE9BQU87YUFDUjtZQUVELE1BQU0sR0FBRyxHQUFHLE1BQU0sQ0FBQyxFQUFFLENBQUM7WUFDdEIsTUFBTSxJQUFJLEdBQUcsR0FBRyxDQUFDLFFBQVEsQ0FBQztZQUUxQixNQUFNLEdBQUcsSUFBSSxvRUFBYSxDQUFDO2dCQUN6QixRQUFRLEVBQUU7b0JBQ1IsUUFBUSxFQUFFLFFBQVE7b0JBQ2xCLE1BQU0sRUFBRSxVQUFVLENBQUMsTUFBTTtvQkFDekIsSUFBSSxFQUFFLFVBQVUsQ0FBQyxJQUFJO2lCQUN0QjtnQkFDRCxhQUFhO2dCQUNiLEdBQUc7Z0JBQ0gsUUFBUTtnQkFDUixVQUFVO2dCQUNWLEtBQUs7Z0JBQ0wsVUFBVTtnQkFDVixJQUFJO2FBQ0wsQ0FBQyxDQUFDO1lBRUgsSUFBSSxVQUFVLEdBQXVCLElBQUksQ0FBQztZQUMxQyx3RUFBd0U7WUFDeEUsd0VBQXdFO1lBQ3hFLG9DQUFvQztZQUNwQyxNQUFNLENBQUMsZUFBZSxDQUFDLE9BQU8sQ0FBQyxDQUFDLE1BQVcsRUFBRSxJQUFjLEVBQUUsRUFBRTtnQkFDN0QsSUFBSSxDQUFDLE9BQU8sQ0FBQyxFQUFFLENBQUMsRUFBRTtvQkFDaEIsUUFBUSxDQUFDLG9CQUFvQixDQUFDLEVBQUUsQ0FBQyxDQUFDO2dCQUNwQyxDQUFDLENBQUMsQ0FBQztnQkFDSCxJQUFJLE1BQU0sQ0FBQyxVQUFVLEVBQUU7b0JBQ3JCLElBQUksQ0FBQyxVQUFVLEVBQUU7d0JBQ2YsVUFBVSxHQUFHLE1BQU0sQ0FBQyxRQUFRLEVBQUUsQ0FBQztxQkFDaEM7aUJBQ0Y7cUJBQU0sSUFBSSxVQUFVLEVBQUU7b0JBQ3JCLFVBQVUsQ0FBQyxPQUFPLEVBQUUsQ0FBQztvQkFDckIsVUFBVSxHQUFHLElBQUksQ0FBQztpQkFDbkI7Z0JBQ0QsTUFBTSxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsR0FBRyxFQUFFO29CQUMzQixJQUFJLFVBQVUsRUFBRTt3QkFDZCxVQUFVLENBQUMsT0FBTyxFQUFFLENBQUM7cUJBQ3RCO2dCQUNILENBQUMsQ0FBQyxDQUFDO1lBQ0wsQ0FBQyxDQUFDLENBQUM7WUFFSCxNQUFNLENBQUMsRUFBRSxHQUFHLFNBQVMsQ0FBQztZQUN0QixNQUFNLENBQUMsS0FBSyxDQUFDLElBQUksR0FBRyxtRUFBWSxDQUFDO1lBQ2pDLE1BQU0sQ0FBQyxLQUFLLENBQUMsS0FBSyxHQUFHLEtBQUssQ0FBQyxFQUFFLENBQUMsVUFBVSxDQUFDLENBQUM7WUFFMUMsTUFBTSxJQUFJLEdBQUcsSUFBSSxnRUFBYyxDQUFDLEVBQUUsT0FBTyxFQUFFLE1BQU0sRUFBRSxDQUFDLENBQUM7WUFDckQsS0FBSyxPQUFPLENBQUMsR0FBRyxDQUFDLElBQUksQ0FBQyxDQUFDO1lBQ3ZCLEtBQUssQ0FBQyxHQUFHLENBQUMsSUFBSSxDQUFDLENBQUM7UUFDbEIsQ0FBQztRQUNELEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLDBCQUEwQixDQUFDO0tBQzVDLENBQUMsQ0FBQztJQUNILElBQUksT0FBTyxFQUFFO1FBQ1gsT0FBTyxDQUFDLE9BQU8sQ0FBQztZQUNkLFFBQVEsRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQztZQUM5QixPQUFPLEVBQUUsVUFBVSxDQUFDLElBQUk7U0FDekIsQ0FBQyxDQUFDO0tBQ0o7SUFFRCxRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxNQUFNLEVBQUU7UUFDckMsT0FBTyxFQUFFLEdBQUcsRUFBRTs7WUFDWixhQUFPLENBQUMsYUFBYSwwQ0FBRSxPQUFPLENBQUMsTUFBTSxHQUFHO1FBQzFDLENBQUM7UUFDRCxJQUFJLEVBQUUsK0RBQVE7UUFDZCxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxzQkFBc0IsQ0FBQztRQUN2QyxTQUFTLEVBQUUsR0FBRyxFQUFFLGtDQUFDLE9BQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sQ0FBQyxZQUFZLG1DQUFJLEtBQUs7S0FDdEUsQ0FBQyxDQUFDO0lBRUgsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsSUFBSSxFQUFFO1FBQ25DLE9BQU8sRUFBRSxHQUFHLEVBQUUsd0JBQUMsT0FBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDLElBQUksS0FBRTtRQUNwRCxJQUFJLEVBQUUsK0RBQVE7UUFDZCxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxvQkFBb0IsQ0FBQztRQUNyQyxTQUFTLEVBQUUsR0FBRyxFQUFFLGtDQUFDLE9BQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sQ0FBQyxVQUFVLG1DQUFJLEtBQUs7S0FDcEUsQ0FBQyxDQUFDO0lBRUgsT0FBTyxPQUFPLENBQUM7QUFDakIsQ0FBQztBQUNELGlFQUFlLE1BQU0sRUFBQyIsImZpbGUiOiJwYWNrYWdlc19zZXR0aW5nZWRpdG9yLWV4dGVuc2lvbl9saWJfaW5kZXhfanMtXzc3NDkwLmRmYWQ0ZTljYmZiZTlkMmI2NjhkLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBzZXR0aW5nZWRpdG9yLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTdGF0dXMsXG4gIElMYXlvdXRSZXN0b3JlcixcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBNYWluQXJlYVdpZGdldCxcbiAgV2lkZ2V0VHJhY2tlclxufSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJRWRpdG9yU2VydmljZXMgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlZWRpdG9yJztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7XG4gIElTZXR0aW5nRWRpdG9yVHJhY2tlcixcbiAgU2V0dGluZ0VkaXRvclxufSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5nZWRpdG9yJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVN0YXRlREIgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgc2F2ZUljb24sIHNldHRpbmdzSWNvbiwgdW5kb0ljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgc2V0dGluZyBlZGl0b3IuXG4gKi9cbm5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IG9wZW4gPSAnc2V0dGluZ2VkaXRvcjpvcGVuJztcblxuICBleHBvcnQgY29uc3QgcmV2ZXJ0ID0gJ3NldHRpbmdlZGl0b3I6cmV2ZXJ0JztcblxuICBleHBvcnQgY29uc3Qgc2F2ZSA9ICdzZXR0aW5nZWRpdG9yOnNhdmUnO1xufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IHNldHRpbmcgZWRpdG9yIGV4dGVuc2lvbi5cbiAqL1xuY29uc3QgcGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SVNldHRpbmdFZGl0b3JUcmFja2VyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9zZXR0aW5nZWRpdG9yLWV4dGVuc2lvbjpwbHVnaW4nLFxuICByZXF1aXJlczogW1xuICAgIElMYXlvdXRSZXN0b3JlcixcbiAgICBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIElFZGl0b3JTZXJ2aWNlcyxcbiAgICBJU3RhdGVEQixcbiAgICBJUmVuZGVyTWltZVJlZ2lzdHJ5LFxuICAgIElMYWJTdGF0dXMsXG4gICAgSVRyYW5zbGF0b3JcbiAgXSxcbiAgb3B0aW9uYWw6IFtJQ29tbWFuZFBhbGV0dGVdLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJU2V0dGluZ0VkaXRvclRyYWNrZXIsXG4gIGFjdGl2YXRlXG59O1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBzZXR0aW5nIGVkaXRvciBleHRlbnNpb24uXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlcixcbiAgcmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gIGVkaXRvclNlcnZpY2VzOiBJRWRpdG9yU2VydmljZXMsXG4gIHN0YXRlOiBJU3RhdGVEQixcbiAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgc3RhdHVzOiBJTGFiU3RhdHVzLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuKTogSVNldHRpbmdFZGl0b3JUcmFja2VyIHtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgY29uc3QgbmFtZXNwYWNlID0gJ3NldHRpbmctZWRpdG9yJztcbiAgY29uc3QgZmFjdG9yeVNlcnZpY2UgPSBlZGl0b3JTZXJ2aWNlcy5mYWN0b3J5U2VydmljZTtcbiAgY29uc3QgZWRpdG9yRmFjdG9yeSA9IGZhY3RvcnlTZXJ2aWNlLm5ld0lubGluZUVkaXRvcjtcbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPE1haW5BcmVhV2lkZ2V0PFNldHRpbmdFZGl0b3I+Pih7XG4gICAgbmFtZXNwYWNlXG4gIH0pO1xuICBsZXQgZWRpdG9yOiBTZXR0aW5nRWRpdG9yO1xuXG4gIC8vIEhhbmRsZSBzdGF0ZSByZXN0b3JhdGlvbi5cbiAgdm9pZCByZXN0b3Jlci5yZXN0b3JlKHRyYWNrZXIsIHtcbiAgICBjb21tYW5kOiBDb21tYW5kSURzLm9wZW4sXG4gICAgYXJnczogd2lkZ2V0ID0+ICh7fSksXG4gICAgbmFtZTogd2lkZ2V0ID0+IG5hbWVzcGFjZVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3Blbiwge1xuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGlmICh0cmFja2VyLmN1cnJlbnRXaWRnZXQpIHtcbiAgICAgICAgc2hlbGwuYWN0aXZhdGVCeUlkKHRyYWNrZXIuY3VycmVudFdpZGdldC5pZCk7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cblxuICAgICAgY29uc3Qga2V5ID0gcGx1Z2luLmlkO1xuICAgICAgY29uc3Qgd2hlbiA9IGFwcC5yZXN0b3JlZDtcblxuICAgICAgZWRpdG9yID0gbmV3IFNldHRpbmdFZGl0b3Ioe1xuICAgICAgICBjb21tYW5kczoge1xuICAgICAgICAgIHJlZ2lzdHJ5OiBjb21tYW5kcyxcbiAgICAgICAgICByZXZlcnQ6IENvbW1hbmRJRHMucmV2ZXJ0LFxuICAgICAgICAgIHNhdmU6IENvbW1hbmRJRHMuc2F2ZVxuICAgICAgICB9LFxuICAgICAgICBlZGl0b3JGYWN0b3J5LFxuICAgICAgICBrZXksXG4gICAgICAgIHJlZ2lzdHJ5LFxuICAgICAgICByZW5kZXJtaW1lLFxuICAgICAgICBzdGF0ZSxcbiAgICAgICAgdHJhbnNsYXRvcixcbiAgICAgICAgd2hlblxuICAgICAgfSk7XG5cbiAgICAgIGxldCBkaXNwb3NhYmxlOiBJRGlzcG9zYWJsZSB8IG51bGwgPSBudWxsO1xuICAgICAgLy8gTm90aWZ5IHRoZSBjb21tYW5kIHJlZ2lzdHJ5IHdoZW4gdGhlIHZpc2liaWxpdHkgc3RhdHVzIG9mIHRoZSBzZXR0aW5nXG4gICAgICAvLyBlZGl0b3IncyBjb21tYW5kcyBjaGFuZ2UuIFRoZSBzZXR0aW5nIGVkaXRvciB0b29sYmFyIGxpc3RlbnMgZm9yIHRoaXNcbiAgICAgIC8vIHNpZ25hbCBmcm9tIHRoZSBjb21tYW5kIHJlZ2lzdHJ5LlxuICAgICAgZWRpdG9yLmNvbW1hbmRzQ2hhbmdlZC5jb25uZWN0KChzZW5kZXI6IGFueSwgYXJnczogc3RyaW5nW10pID0+IHtcbiAgICAgICAgYXJncy5mb3JFYWNoKGlkID0+IHtcbiAgICAgICAgICBjb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZChpZCk7XG4gICAgICAgIH0pO1xuICAgICAgICBpZiAoZWRpdG9yLmNhblNhdmVSYXcpIHtcbiAgICAgICAgICBpZiAoIWRpc3Bvc2FibGUpIHtcbiAgICAgICAgICAgIGRpc3Bvc2FibGUgPSBzdGF0dXMuc2V0RGlydHkoKTtcbiAgICAgICAgICB9XG4gICAgICAgIH0gZWxzZSBpZiAoZGlzcG9zYWJsZSkge1xuICAgICAgICAgIGRpc3Bvc2FibGUuZGlzcG9zZSgpO1xuICAgICAgICAgIGRpc3Bvc2FibGUgPSBudWxsO1xuICAgICAgICB9XG4gICAgICAgIGVkaXRvci5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgICBpZiAoZGlzcG9zYWJsZSkge1xuICAgICAgICAgICAgZGlzcG9zYWJsZS5kaXNwb3NlKCk7XG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH0pO1xuXG4gICAgICBlZGl0b3IuaWQgPSBuYW1lc3BhY2U7XG4gICAgICBlZGl0b3IudGl0bGUuaWNvbiA9IHNldHRpbmdzSWNvbjtcbiAgICAgIGVkaXRvci50aXRsZS5sYWJlbCA9IHRyYW5zLl9fKCdTZXR0aW5ncycpO1xuXG4gICAgICBjb25zdCBtYWluID0gbmV3IE1haW5BcmVhV2lkZ2V0KHsgY29udGVudDogZWRpdG9yIH0pO1xuICAgICAgdm9pZCB0cmFja2VyLmFkZChtYWluKTtcbiAgICAgIHNoZWxsLmFkZChtYWluKTtcbiAgICB9LFxuICAgIGxhYmVsOiB0cmFucy5fXygnQWR2YW5jZWQgU2V0dGluZ3MgRWRpdG9yJylcbiAgfSk7XG4gIGlmIChwYWxldHRlKSB7XG4gICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnU2V0dGluZ3MnKSxcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMub3BlblxuICAgIH0pO1xuICB9XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJldmVydCwge1xuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudC5yZXZlcnQoKTtcbiAgICB9LFxuICAgIGljb246IHVuZG9JY29uLFxuICAgIGxhYmVsOiB0cmFucy5fXygnUmV2ZXJ0IFVzZXIgU2V0dGluZ3MnKSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudC5jYW5SZXZlcnRSYXcgPz8gZmFsc2VcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNhdmUsIHtcbiAgICBleGVjdXRlOiAoKSA9PiB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQuc2F2ZSgpLFxuICAgIGljb246IHNhdmVJY29uLFxuICAgIGxhYmVsOiB0cmFucy5fXygnU2F2ZSBVc2VyIFNldHRpbmdzJyksXG4gICAgaXNFbmFibGVkOiAoKSA9PiB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQuY2FuU2F2ZVJhdyA/PyBmYWxzZVxuICB9KTtcblxuICByZXR1cm4gdHJhY2tlcjtcbn1cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcbiJdLCJzb3VyY2VSb290IjoiIn0=