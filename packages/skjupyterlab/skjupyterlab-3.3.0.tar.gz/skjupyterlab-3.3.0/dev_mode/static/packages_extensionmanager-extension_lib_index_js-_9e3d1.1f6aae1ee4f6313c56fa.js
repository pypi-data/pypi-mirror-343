(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_extensionmanager-extension_lib_index_js-_9e3d1"],{

/***/ "../packages/extensionmanager-extension/lib/index.js":
/*!***********************************************************!*\
  !*** ../packages/extensionmanager-extension/lib/index.js ***!
  \***********************************************************/
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
/* harmony import */ var _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/extensionmanager */ "webpack/sharing/consume/default/@jupyterlab/extensionmanager/@jupyterlab/extensionmanager");
/* harmony import */ var _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module extensionmanager-extension
 */






const PLUGIN_ID = '@jupyterlab/extensionmanager-extension:plugin';
/**
 * IDs of the commands added by this extension.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.toggle = 'extensionmanager:toggle';
})(CommandIDs || (CommandIDs = {}));
/**
 * The extension manager plugin.
 */
const plugin = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: async (app, registry, translator, labShell, restorer, palette) => {
        const trans = translator.load('jupyterlab');
        const settings = await registry.load(plugin.id);
        let enabled = settings.composite['enabled'] === true;
        const { commands, serviceManager } = app;
        let view;
        const createView = () => {
            const v = new _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__.ExtensionView(app, serviceManager, settings, translator);
            v.id = 'extensionmanager.main-view';
            v.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.extensionIcon;
            v.title.caption = trans.__('Extension Manager');
            if (restorer) {
                restorer.add(v, v.id);
            }
            return v;
        };
        if (enabled && labShell) {
            view = createView();
            view.node.setAttribute('role', 'region');
            view.node.setAttribute('aria-label', trans.__('Extension Manager section'));
            labShell.add(view, 'left', { rank: 1000 });
        }
        // If the extension is enabled or disabled,
        // add or remove it from the left area.
        Promise.all([app.restored, registry.load(PLUGIN_ID)])
            .then(([, settings]) => {
            settings.changed.connect(async () => {
                enabled = settings.composite['enabled'] === true;
                if (enabled && !(view === null || view === void 0 ? void 0 : view.isAttached)) {
                    const accepted = await Private.showWarning(trans);
                    if (!accepted) {
                        void settings.set('enabled', false);
                        return;
                    }
                    view = view || createView();
                    view.node.setAttribute('role', 'region');
                    view.node.setAttribute('aria-label', trans.__('Extension Manager section'));
                    if (labShell) {
                        labShell.add(view, 'left', { rank: 1000 });
                    }
                }
                else if (!enabled && (view === null || view === void 0 ? void 0 : view.isAttached)) {
                    app.commands.notifyCommandChanged(CommandIDs.toggle);
                    view.close();
                }
            });
        })
            .catch(reason => {
            console.error(`Something went wrong when reading the settings.\n${reason}`);
        });
        commands.addCommand(CommandIDs.toggle, {
            label: trans.__('Enable Extension Manager'),
            execute: () => {
                if (registry) {
                    void registry.set(plugin.id, 'enabled', !enabled);
                }
            },
            isToggled: () => enabled,
            isEnabled: () => serviceManager.builder.isAvailable
        });
        const category = trans.__('Extension Manager');
        const command = CommandIDs.toggle;
        if (palette) {
            palette.addItem({ command, category });
        }
    }
};
/**
 * Export the plugin as the default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * A namespace for module-private functions.
 */
var Private;
(function (Private) {
    /**
     * Show a warning dialog about extension security.
     *
     * @returns whether the user accepted the dialog.
     */
    async function showWarning(trans) {
        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Enable Extension Manager?'),
            body: trans.__(`Thanks for trying out JupyterLab's extension manager.
The JupyterLab development team is excited to have a robust
third-party extension community.
However, we cannot vouch for every extension,
and some may introduce security risks.
Do you want to continue?`),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Disable') }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Enable') })
            ]
        }).then(result => {
            return result.button.accept;
        });
    }
    Private.showWarning = showWarning;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZXh0ZW5zaW9ubWFuYWdlci1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU84QjtBQUMwQztBQUNkO0FBQ0U7QUFDVTtBQUNmO0FBRTFELE1BQU0sU0FBUyxHQUFHLCtDQUErQyxDQUFDO0FBRWxFOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBRW5CO0FBRkQsV0FBVSxVQUFVO0lBQ0wsaUJBQU0sR0FBRyx5QkFBeUIsQ0FBQztBQUNsRCxDQUFDLEVBRlMsVUFBVSxLQUFWLFVBQVUsUUFFbkI7QUFFRDs7R0FFRztBQUNILE1BQU0sTUFBTSxHQUFnQztJQUMxQyxFQUFFLEVBQUUsU0FBUztJQUNiLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQUMseUVBQWdCLEVBQUUsZ0VBQVcsQ0FBQztJQUN6QyxRQUFRLEVBQUUsQ0FBQyw4REFBUyxFQUFFLG9FQUFlLEVBQUUsaUVBQWUsQ0FBQztJQUN2RCxRQUFRLEVBQUUsS0FBSyxFQUNiLEdBQW9CLEVBQ3BCLFFBQTBCLEVBQzFCLFVBQXVCLEVBQ3ZCLFFBQTBCLEVBQzFCLFFBQWdDLEVBQ2hDLE9BQStCLEVBQy9CLEVBQUU7UUFDRixNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQzVDLE1BQU0sUUFBUSxHQUFHLE1BQU0sUUFBUSxDQUFDLElBQUksQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLENBQUM7UUFDaEQsSUFBSSxPQUFPLEdBQUcsUUFBUSxDQUFDLFNBQVMsQ0FBQyxTQUFTLENBQUMsS0FBSyxJQUFJLENBQUM7UUFFckQsTUFBTSxFQUFFLFFBQVEsRUFBRSxjQUFjLEVBQUUsR0FBRyxHQUFHLENBQUM7UUFD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Q0FBQyxTQUFTLENBQUMsRUFBRSxDQUFDO2dCQUNuRCxtRUFBaUIsQ0FBQyxFQUFFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFFBQVEsQ0FBQyxFQUFFLENBQUM7YUFDakQ7U0FDRixDQUFDLENBQUMsSUFBSSxDQUFDLE1BQU0sQ0FBQyxFQUFFO1lBQ2YsT0FBTyxNQUFNLENBQUMsTUFBTSxDQUFDLE1BQU0sQ0FBQztRQUM5QixDQUFDLENBQUMsQ0FBQztJQUNMLENBQUM7SUFsQnFCLG1CQUFXLGNBa0JoQztBQUNILENBQUMsRUF6QlMsT0FBTyxLQUFQLE9BQU8sUUF5QmhCIiwiZmlsZSI6InBhY2thZ2VzX2V4dGVuc2lvbm1hbmFnZXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy1fOWUzZDEuMWY2YWFlMWVlNGY2MzEzYzU2ZmEuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBleHRlbnNpb25tYW5hZ2VyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTaGVsbCxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBEaWFsb2csIElDb21tYW5kUGFsZXR0ZSwgc2hvd0RpYWxvZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IEV4dGVuc2lvblZpZXcgfSBmcm9tICdAanVweXRlcmxhYi9leHRlbnNpb25tYW5hZ2VyJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIFRyYW5zbGF0aW9uQnVuZGxlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgZXh0ZW5zaW9uSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuXG5jb25zdCBQTFVHSU5fSUQgPSAnQGp1cHl0ZXJsYWIvZXh0ZW5zaW9ubWFuYWdlci1leHRlbnNpb246cGx1Z2luJztcblxuLyoqXG4gKiBJRHMgb2YgdGhlIGNvbW1hbmRzIGFkZGVkIGJ5IHRoaXMgZXh0ZW5zaW9uLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCB0b2dnbGUgPSAnZXh0ZW5zaW9ubWFuYWdlcjp0b2dnbGUnO1xufVxuXG4vKipcbiAqIFRoZSBleHRlbnNpb24gbWFuYWdlciBwbHVnaW4uXG4gKi9cbmNvbnN0IHBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogUExVR0lOX0lELFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSVNldHRpbmdSZWdpc3RyeSwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lMYWJTaGVsbCwgSUxheW91dFJlc3RvcmVyLCBJQ29tbWFuZFBhbGV0dGVdLFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsLFxuICAgIHJlc3RvcmVyOiBJTGF5b3V0UmVzdG9yZXIgfCBudWxsLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBzZXR0aW5ncyA9IGF3YWl0IHJlZ2lzdHJ5LmxvYWQocGx1Z2luLmlkKTtcbiAgICBsZXQgZW5hYmxlZCA9IHNldHRpbmdzLmNvbXBvc2l0ZVsnZW5hYmxlZCddID09PSB0cnVlO1xuXG4gICAgY29uc3QgeyBjb21tYW5kcywgc2VydmljZU1hbmFnZXIgfSA9IGFwcDtcbiAgICBsZXQgdmlldzogRXh0ZW5zaW9uVmlldyB8IHVuZGVmaW5lZDtcblxuICAgIGNvbnN0IGNyZWF0ZVZpZXcgPSAoKSA9PiB7XG4gICAgICBjb25zdCB2ID0gbmV3IEV4dGVuc2lvblZpZXcoYXBwLCBzZXJ2aWNlTWFuYWdlciwgc2V0dGluZ3MsIHRyYW5zbGF0b3IpO1xuICAgICAgdi5pZCA9ICdleHRlbnNpb25tYW5hZ2VyLm1haW4tdmlldyc7XG4gICAgICB2LnRpdGxlLmljb24gPSBleHRlbnNpb25JY29uO1xuICAgICAgdi50aXRsZS5jYXB0aW9uID0gdHJhbnMuX18oJ0V4dGVuc2lvbiBNYW5hZ2VyJyk7XG4gICAgICBpZiAocmVzdG9yZXIpIHtcbiAgICAgICAgcmVzdG9yZXIuYWRkKHYsIHYuaWQpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHY7XG4gICAgfTtcblxuICAgIGlmIChlbmFibGVkICYmIGxhYlNoZWxsKSB7XG4gICAgICB2aWV3ID0gY3JlYXRlVmlldygpO1xuICAgICAgdmlldy5ub2RlLnNldEF0dHJpYnV0ZSgncm9sZScsICdyZWdpb24nKTtcbiAgICAgIHZpZXcubm9kZS5zZXRBdHRyaWJ1dGUoXG4gICAgICAgICdhcmlhLWxhYmVsJyxcbiAgICAgICAgdHJhbnMuX18oJ0V4dGVuc2lvbiBNYW5hZ2VyIHNlY3Rpb24nKVxuICAgICAgKTtcbiAgICAgIGxhYlNoZWxsLmFkZCh2aWV3LCAnbGVmdCcsIHsgcmFuazogMTAwMCB9KTtcbiAgICB9XG5cbiAgICAvLyBJZiB0aGUgZXh0ZW5zaW9uIGlzIGVuYWJsZWQgb3IgZGlzYWJsZWQsXG4gICAgLy8gYWRkIG9yIHJlbW92ZSBpdCBmcm9tIHRoZSBsZWZ0IGFyZWEuXG4gICAgUHJvbWlzZS5hbGwoW2FwcC5yZXN0b3JlZCwgcmVnaXN0cnkubG9hZChQTFVHSU5fSUQpXSlcbiAgICAgIC50aGVuKChbLCBzZXR0aW5nc10pID0+IHtcbiAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KGFzeW5jICgpID0+IHtcbiAgICAgICAgICBlbmFibGVkID0gc2V0dGluZ3MuY29tcG9zaXRlWydlbmFibGVkJ10gPT09IHRydWU7XG4gICAgICAgICAgaWYgKGVuYWJsZWQgJiYgIXZpZXc/LmlzQXR0YWNoZWQpIHtcbiAgICAgICAgICAgIGNvbnN0IGFjY2VwdGVkID0gYXdhaXQgUHJpdmF0ZS5zaG93V2FybmluZyh0cmFucyk7XG4gICAgICAgICAgICBpZiAoIWFjY2VwdGVkKSB7XG4gICAgICAgICAgICAgIHZvaWQgc2V0dGluZ3Muc2V0KCdlbmFibGVkJywgZmFsc2UpO1xuICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICB2aWV3ID0gdmlldyB8fCBjcmVhdGVWaWV3KCk7XG4gICAgICAgICAgICB2aWV3Lm5vZGUuc2V0QXR0cmlidXRlKCdyb2xlJywgJ3JlZ2lvbicpO1xuICAgICAgICAgICAgdmlldy5ub2RlLnNldEF0dHJpYnV0ZShcbiAgICAgICAgICAgICAgJ2FyaWEtbGFiZWwnLFxuICAgICAgICAgICAgICB0cmFucy5fXygnRXh0ZW5zaW9uIE1hbmFnZXIgc2VjdGlvbicpXG4gICAgICAgICAgICApO1xuICAgICAgICAgICAgaWYgKGxhYlNoZWxsKSB7XG4gICAgICAgICAgICAgIGxhYlNoZWxsLmFkZCh2aWV3LCAnbGVmdCcsIHsgcmFuazogMTAwMCB9KTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9IGVsc2UgaWYgKCFlbmFibGVkICYmIHZpZXc/LmlzQXR0YWNoZWQpIHtcbiAgICAgICAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZChDb21tYW5kSURzLnRvZ2dsZSk7XG4gICAgICAgICAgICB2aWV3LmNsb3NlKCk7XG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcihcbiAgICAgICAgICBgU29tZXRoaW5nIHdlbnQgd3Jvbmcgd2hlbiByZWFkaW5nIHRoZSBzZXR0aW5ncy5cXG4ke3JlYXNvbn1gXG4gICAgICAgICk7XG4gICAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGUsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnRW5hYmxlIEV4dGVuc2lvbiBNYW5hZ2VyJyksXG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGlmIChyZWdpc3RyeSkge1xuICAgICAgICAgIHZvaWQgcmVnaXN0cnkuc2V0KHBsdWdpbi5pZCwgJ2VuYWJsZWQnLCAhZW5hYmxlZCk7XG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBpc1RvZ2dsZWQ6ICgpID0+IGVuYWJsZWQsXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHNlcnZpY2VNYW5hZ2VyLmJ1aWxkZXIuaXNBdmFpbGFibGVcbiAgICB9KTtcblxuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0V4dGVuc2lvbiBNYW5hZ2VyJyk7XG4gICAgY29uc3QgY29tbWFuZCA9IENvbW1hbmRJRHMudG9nZ2xlO1xuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kLCBjYXRlZ29yeSB9KTtcbiAgICB9XG4gIH1cbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW4gYXMgdGhlIGRlZmF1bHQuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgbW9kdWxlLXByaXZhdGUgZnVuY3Rpb25zLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBTaG93IGEgd2FybmluZyBkaWFsb2cgYWJvdXQgZXh0ZW5zaW9uIHNlY3VyaXR5LlxuICAgKlxuICAgKiBAcmV0dXJucyB3aGV0aGVyIHRoZSB1c2VyIGFjY2VwdGVkIHRoZSBkaWFsb2cuXG4gICAqL1xuICBleHBvcnQgYXN5bmMgZnVuY3Rpb24gc2hvd1dhcm5pbmcoXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICk6IFByb21pc2U8Ym9vbGVhbj4ge1xuICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgIHRpdGxlOiB0cmFucy5fXygnRW5hYmxlIEV4dGVuc2lvbiBNYW5hZ2VyPycpLFxuICAgICAgYm9keTogdHJhbnMuX18oYFRoYW5rcyBmb3IgdHJ5aW5nIG91dCBKdXB5dGVyTGFiJ3MgZXh0ZW5zaW9uIG1hbmFnZXIuXG5UaGUgSnVweXRlckxhYiBkZXZlbG9wbWVudCB0ZWFtIGlzIGV4Y2l0ZWQgdG8gaGF2ZSBhIHJvYnVzdFxudGhpcmQtcGFydHkgZXh0ZW5zaW9uIGNvbW11bml0eS5cbkhvd2V2ZXIsIHdlIGNhbm5vdCB2b3VjaCBmb3IgZXZlcnkgZXh0ZW5zaW9uLFxuYW5kIHNvbWUgbWF5IGludHJvZHVjZSBzZWN1cml0eSByaXNrcy5cbkRvIHlvdSB3YW50IHRvIGNvbnRpbnVlP2ApLFxuICAgICAgYnV0dG9uczogW1xuICAgICAgICBEaWFsb2cuY2FuY2VsQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdEaXNhYmxlJykgfSksXG4gICAgICAgIERpYWxvZy53YXJuQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdFbmFibGUnKSB9KVxuICAgICAgXVxuICAgIH0pLnRoZW4ocmVzdWx0ID0+IHtcbiAgICAgIHJldHVybiByZXN1bHQuYnV0dG9uLmFjY2VwdDtcbiAgICB9KTtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ==