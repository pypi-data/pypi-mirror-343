(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_translation-extension_lib_index_js-_3c190"],{

/***/ "../packages/translation-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/translation-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* ----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module translation-extension
 */





/**
 * A namespace for command IDs.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.installAdditionalLanguages = 'jupyterlab-translation:install-additional-languages';
})(CommandIDs || (CommandIDs = {}));
/**
 * Translation plugins
 */
const PLUGIN_ID = '@jupyterlab/translation-extension:plugin';
const translator = {
    id: '@jupyterlab/translation:translator',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    provides: _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator,
    activate: async (app, paths, settings) => {
        const setting = await settings.load(PLUGIN_ID);
        const currentLocale = setting.get('locale').composite;
        let stringsPrefix = setting.get('stringsPrefix')
            .composite;
        const displayStringsPrefix = setting.get('displayStringsPrefix')
            .composite;
        stringsPrefix = displayStringsPrefix ? stringsPrefix : '';
        const serverSettings = app.serviceManager.serverSettings;
        const translationManager = new _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.TranslationManager(paths.urls.translations, stringsPrefix, serverSettings);
        await translationManager.fetch(currentLocale);
        return translationManager;
    }
};
/**
 * Initialization data for the extension.
 */
const langMenu = {
    id: PLUGIN_ID,
    requires: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__.IMainMenu, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    autoStart: true,
    activate: (app, mainMenu, settings, translator) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        let currentLocale;
        /**
         * Load the settings for this extension
         *
         * @param setting Extension settings
         */
        function loadSetting(setting) {
            // Read the settings and convert to the correct type
            currentLocale = setting.get('locale').composite;
        }
        settings
            .load(PLUGIN_ID)
            .then(setting => {
            var _a;
            // Read the settings
            loadSetting(setting);
            document.documentElement.lang = currentLocale;
            // Listen for your plugin setting changes using Signal
            setting.changed.connect(loadSetting);
            // Create a languages menu
            const languagesMenu = (_a = mainMenu.settingsMenu.items.find(item => {
                var _a;
                return item.type === 'submenu' &&
                    ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-settings-language';
            })) === null || _a === void 0 ? void 0 : _a.submenu;
            let command;
            const serverSettings = app.serviceManager.serverSettings;
            // Get list of available locales
            (0,_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.requestTranslationsAPI)('', '', {}, serverSettings)
                .then(data => {
                for (const locale in data['data']) {
                    const value = data['data'][locale];
                    const displayName = value.displayName;
                    const nativeName = value.nativeName;
                    const toggled = displayName === nativeName;
                    const label = toggled
                        ? `${displayName}`
                        : `${displayName} - ${nativeName}`;
                    // Add a command per language
                    command = `jupyterlab-translation:${locale}`;
                    commands.addCommand(command, {
                        label: label,
                        caption: label,
                        isEnabled: () => !toggled,
                        isVisible: () => true,
                        isToggled: () => toggled,
                        execute: () => {
                            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                                title: trans.__('Change interface language?'),
                                body: trans.__('After changing the interface language to %1, you will need to reload JupyterLab to see the changes.', label),
                                buttons: [
                                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Cancel') }),
                                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Change and reload') })
                                ]
                            }).then(result => {
                                if (result.button.accept) {
                                    setting
                                        .set('locale', locale)
                                        .then(() => {
                                        window.location.reload();
                                    })
                                        .catch(reason => {
                                        console.error(reason);
                                    });
                                }
                            });
                        }
                    });
                    // Add the language command to the menu
                    if (languagesMenu) {
                        languagesMenu.addItem({
                            command,
                            args: {}
                        });
                    }
                }
            })
                .catch(reason => {
                console.error(`Available locales errored!\n${reason}`);
            });
        })
            .catch(reason => {
            console.error(`The jupyterlab translation extension appears to be missing.\n${reason}`);
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [translator, langMenu];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdHJhbnNsYXRpb24tZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFLOEI7QUFDeUI7QUFDVDtBQUNjO0FBSzlCO0FBRWpDOztHQUVHO0FBQ0ksSUFBVSxVQUFVLENBRzFCO0FBSEQsV0FBaUIsVUFBVTtJQUNaLHFDQUEwQixHQUNyQyxxREFBcUQsQ0FBQztBQUMxRCxDQUFDLEVBSGdCLFVBQVUsS0FBVixVQUFVLFFBRzFCO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLFNBQVMsR0FBRywwQ0FBMEMsQ0FBQztBQUU3RCxNQUFNLFVBQVUsR0FBdUM7SUFDckQsRUFBRSxFQUFFLG9DQUFvQztJQUN4QyxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxDQUFDLDJFQUFzQixFQUFFLHlFQUFnQixDQUFDO0lBQ3BELFFBQVEsRUFBRSxnRUFBVztJQUNyQixRQUFRLEVBQUUsS0FBSyxFQUNiLEdBQW9CLEVBQ3BCLEtBQTZCLEVBQzdCLFFBQTBCLEVBQzFCLEVBQUU7UUFDRixNQUFNLE9BQU8sR0FBRyxNQUFNLFFBQVEsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLENBQUM7UUFDL0MsTUFBTSxhQUFhLEdBQVcsT0FBTyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQyxTQUFtQixDQUFDO1FBQ3hFLElBQUksYUFBYSxHQUFXLE9BQU8sQ0FBQyxHQUFHLENBQUMsZUFBZSxDQUFDO2FBQ3JELFNBQW1CLENBQUM7UUFDdkIsTUFBTSxvQkFBb0IsR0FBWSxPQUFPLENBQUMsR0FBRyxDQUFDLHNCQUFzQixDQUFDO2FBQ3RFLFNBQW9CLENBQUM7UUFDeEIsYUFBYSxHQUFHLG9CQUFvQixDQUFDLENBQUMsQ0FBQyxhQUFhLENBQUMsQ0FBQyxDQUFDLEVB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QztpQkFDRCxLQUFLLENBQUMsTUFBTSxDQUFDLEVBQUU7Z0JBQ2QsT0FBTyxDQUFDLEtBQUssQ0FBQywrQkFBK0IsTUFBTSxFQUFFLENBQUMsQ0FBQztZQUN6RCxDQUFDLENBQUMsQ0FBQztRQUNQLENBQUMsQ0FBQzthQUNELEtBQUssQ0FBQyxNQUFNLENBQUMsRUFBRTtZQUNkLE9BQU8sQ0FBQyxLQUFLLENBQ1gsZ0VBQWdFLE1BQU0sRUFBRSxDQUN6RSxDQUFDO1FBQ0osQ0FBQyxDQUFDLENBQUM7SUFDUCxDQUFDO0NBQ0YsQ0FBQztBQUVGOztHQUVHO0FBQ0gsTUFBTSxPQUFPLEdBQWlDLENBQUMsVUFBVSxFQUFFLFFBQVEsQ0FBQyxDQUFDO0FBQ3JFLGlFQUFlLE9BQU8sRUFBQyIsImZpbGUiOiJwYWNrYWdlc190cmFuc2xhdGlvbi1leHRlbnNpb25fbGliX2luZGV4X2pzLV8zYzE5MC5mMGVhMDg4MDJiODZiZTAwOTVhNC5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSB0cmFuc2xhdGlvbi1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBEaWFsb2csIHNob3dEaWFsb2cgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJTWFpbk1lbnUgfSBmcm9tICdAanVweXRlcmxhYi9tYWlubWVudSc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICByZXF1ZXN0VHJhbnNsYXRpb25zQVBJLFxuICBUcmFuc2xhdGlvbk1hbmFnZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBjb21tYW5kIElEcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IGluc3RhbGxBZGRpdGlvbmFsTGFuZ3VhZ2VzID1cbiAgICAnanVweXRlcmxhYi10cmFuc2xhdGlvbjppbnN0YWxsLWFkZGl0aW9uYWwtbGFuZ3VhZ2VzJztcbn1cblxuLyoqXG4gKiBUcmFuc2xhdGlvbiBwbHVnaW5zXG4gKi9cbmNvbnN0IFBMVUdJTl9JRCA9ICdAanVweXRlcmxhYi90cmFuc2xhdGlvbi1leHRlbnNpb246cGx1Z2luJztcblxuY29uc3QgdHJhbnNsYXRvcjogSnVweXRlckZyb250RW5kUGx1Z2luPElUcmFuc2xhdG9yPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi90cmFuc2xhdGlvbjp0cmFuc2xhdG9yJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0p1cHl0ZXJGcm9udEVuZC5JUGF0aHMsIElTZXR0aW5nUmVnaXN0cnldLFxuICBwcm92aWRlczogSVRyYW5zbGF0b3IsXG4gIGFjdGl2YXRlOiBhc3luYyAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgcGF0aHM6IEp1cHl0ZXJGcm9udEVuZC5JUGF0aHMsXG4gICAgc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnlcbiAgKSA9PiB7XG4gICAgY29uc3Qgc2V0dGluZyA9IGF3YWl0IHNldHRpbmdzLmxvYWQoUExVR0lOX0lEKTtcbiAgICBjb25zdCBjdXJyZW50TG9jYWxlOiBzdHJpbmcgPSBzZXR0aW5nLmdldCgnbG9jYWxlJykuY29tcG9zaXRlIGFzIHN0cmluZztcbiAgICBsZXQgc3RyaW5nc1ByZWZpeDogc3RyaW5nID0gc2V0dGluZy5nZXQoJ3N0cmluZ3NQcmVmaXgnKVxuICAgICAgLmNvbXBvc2l0ZSBhcyBzdHJpbmc7XG4gICAgY29uc3QgZGlzcGxheVN0cmluZ3NQcmVmaXg6IGJvb2xlYW4gPSBzZXR0aW5nLmdldCgnZGlzcGxheVN0cmluZ3NQcmVmaXgnKVxuICAgICAgLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgIHN0cmluZ3NQcmVmaXggPSBkaXNwbGF5U3RyaW5nc1ByZWZpeCA/IHN0cmluZ3NQcmVmaXggOiAnJztcbiAgICBjb25zdCBzZXJ2ZXJTZXR0aW5ncyA9IGFwcC5zZXJ2aWNlTWFuYWdlci5zZXJ2ZXJTZXR0aW5ncztcbiAgICBjb25zdCB0cmFuc2xhdGlvbk1hbmFnZXIgPSBuZXcgVHJhbnNsYXRpb25NYW5hZ2VyKFxuICAgICAgcGF0aHMudXJscy50cmFuc2xhdGlvbnMsXG4gICAgICBzdHJpbmdzUHJlZml4LFxuICAgICAgc2VydmVyU2V0dGluZ3NcbiAgICApO1xuICAgIGF3YWl0IHRyYW5zbGF0aW9uTWFuYWdlci5mZXRjaChjdXJyZW50TG9jYWxlKTtcbiAgICByZXR1cm4gdHJhbnNsYXRpb25NYW5hZ2VyO1xuICB9XG59O1xuXG4vKipcbiAqIEluaXRpYWxpemF0aW9uIGRhdGEgZm9yIHRoZSBleHRlbnNpb24uXG4gKi9cbmNvbnN0IGxhbmdNZW51OiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiBQTFVHSU5fSUQsXG4gIHJlcXVpcmVzOiBbSU1haW5NZW51LCBJU2V0dGluZ1JlZ2lzdHJ5LCBJVHJhbnNsYXRvcl0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBtYWluTWVudTogSU1haW5NZW51LFxuICAgIHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICkgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGxldCBjdXJyZW50TG9jYWxlOiBzdHJpbmc7XG4gICAgLyoqXG4gICAgICogTG9hZCB0aGUgc2V0dGluZ3MgZm9yIHRoaXMgZXh0ZW5zaW9uXG4gICAgICpcbiAgICAgKiBAcGFyYW0gc2V0dGluZyBFeHRlbnNpb24gc2V0dGluZ3NcbiAgICAgKi9cbiAgICBmdW5jdGlvbiBsb2FkU2V0dGluZyhzZXR0aW5nOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyk6IHZvaWQge1xuICAgICAgLy8gUmVhZCB0aGUgc2V0dGluZ3MgYW5kIGNvbnZlcnQgdG8gdGhlIGNvcnJlY3QgdHlwZVxuICAgICAgY3VycmVudExvY2FsZSA9IHNldHRpbmcuZ2V0KCdsb2NhbGUnKS5jb21wb3NpdGUgYXMgc3RyaW5nO1xuICAgIH1cblxuICAgIHNldHRpbmdzXG4gICAgICAubG9hZChQTFVHSU5fSUQpXG4gICAgICAudGhlbihzZXR0aW5nID0+IHtcbiAgICAgICAgLy8gUmVhZCB0aGUgc2V0dGluZ3NcbiAgICAgICAgbG9hZFNldHRpbmcoc2V0dGluZyk7XG4gICAgICAgIGRvY3VtZW50LmRvY3VtZW50RWxlbWVudC5sYW5nID0gY3VycmVudExvY2FsZTtcblxuICAgICAgICAvLyBMaXN0ZW4gZm9yIHlvdXIgcGx1Z2luIHNldHRpbmcgY2hhbmdlcyB1c2luZyBTaWduYWxcbiAgICAgICAgc2V0dGluZy5jaGFuZ2VkLmNvbm5lY3QobG9hZFNldHRpbmcpO1xuXG4gICAgICAgIC8vIENyZWF0ZSBhIGxhbmd1YWdlcyBtZW51XG4gICAgICAgIGNvbnN0IGxhbmd1YWdlc01lbnUgPSBtYWluTWVudS5zZXR0aW5nc01lbnUuaXRlbXMuZmluZChcbiAgICAgICAgICBpdGVtID0+XG4gICAgICAgICAgICBpdGVtLnR5cGUgPT09ICdzdWJtZW51JyAmJlxuICAgICAgICAgICAgaXRlbS5zdWJtZW51Py5pZCA9PT0gJ2pwLW1haW5tZW51LXNldHRpbmdzLWxhbmd1YWdlJ1xuICAgICAgICApPy5zdWJtZW51O1xuXG4gICAgICAgIGxldCBjb21tYW5kOiBzdHJpbmc7XG5cbiAgICAgICAgY29uc3Qgc2VydmVyU2V0dGluZ3MgPSBhcHAuc2VydmljZU1hbmFnZXIuc2VydmVyU2V0dGluZ3M7XG4gICAgICAgIC8vIEdldCBsaXN0IG9mIGF2YWlsYWJsZSBsb2NhbGVzXG4gICAgICAgIHJlcXVlc3RUcmFuc2xhdGlvbnNBUEk8YW55PignJywgJycsIHt9LCBzZXJ2ZXJTZXR0aW5ncylcbiAgICAgICAgICAudGhlbihkYXRhID0+IHtcbiAgICAgICAgICAgIGZvciAoY29uc3QgbG9jYWxlIGluIGRhdGFbJ2RhdGEnXSkge1xuICAgICAgICAgICAgICBjb25zdCB2YWx1ZSA9IGRhdGFbJ2RhdGEnXVtsb2NhbGVdO1xuICAgICAgICAgICAgICBjb25zdCBkaXNwbGF5TmFtZSA9IHZhbHVlLmRpc3BsYXlOYW1lO1xuICAgICAgICAgICAgICBjb25zdCBuYXRpdmVOYW1lID0gdmFsdWUubmF0aXZlTmFtZTtcbiAgICAgICAgICAgICAgY29uc3QgdG9nZ2xlZCA9IGRpc3BsYXlOYW1lID09PSBuYXRpdmVOYW1lO1xuICAgICAgICAgICAgICBjb25zdCBsYWJlbCA9IHRvZ2dsZWRcbiAgICAgICAgICAgICAgICA/IGAke2Rpc3BsYXlOYW1lfWBcbiAgICAgICAgICAgICAgICA6IGAke2Rpc3BsYXlOYW1lfSAtICR7bmF0aXZlTmFtZX1gO1xuXG4gICAgICAgICAgICAgIC8vIEFkZCBhIGNvbW1hbmQgcGVyIGxhbmd1YWdlXG4gICAgICAgICAgICAgIGNvbW1hbmQgPSBganVweXRlcmxhYi10cmFuc2xhdGlvbjoke2xvY2FsZX1gO1xuICAgICAgICAgICAgICBjb21tYW5kcy5hZGRDb21tYW5kKGNvbW1hbmQsIHtcbiAgICAgICAgICAgICAgICBsYWJlbDogbGFiZWwsXG4gICAgICAgICAgICAgICAgY2FwdGlvbjogbGFiZWwsXG4gICAgICAgICAgICAgICAgaXNFbmFibGVkOiAoKSA9PiAhdG9nZ2xlZCxcbiAgICAgICAgICAgICAgICBpc1Zpc2libGU6ICgpID0+IHRydWUsXG4gICAgICAgICAgICAgICAgaXNUb2dnbGVkOiAoKSA9PiB0b2dnbGVkLFxuICAgICAgICAgICAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgICAgICAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgICAgICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdDaGFuZ2UgaW50ZXJmYWNlIGxhbmd1YWdlPycpLFxuICAgICAgICAgICAgICAgICAgICBib2R5OiB0cmFucy5fXyhcbiAgICAgICAgICAgICAgICAgICAgICAnQWZ0ZXIgY2hhbmdpbmcgdGhlIGludGVyZmFjZSBsYW5ndWFnZSB0byAlMSwgeW91IHdpbGwgbmVlZCB0byByZWxvYWQgSnVweXRlckxhYiB0byBzZWUgdGhlIGNoYW5nZXMuJyxcbiAgICAgICAgICAgICAgICAgICAgICBsYWJlbFxuICAgICAgICAgICAgICAgICAgICApLFxuICAgICAgICAgICAgICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgICAgICAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnQ2FuY2VsJykgfSksXG4gICAgICAgICAgICAgICAgICAgICAgRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdDaGFuZ2UgYW5kIHJlbG9hZCcpIH0pXG4gICAgICAgICAgICAgICAgICAgIF1cbiAgICAgICAgICAgICAgICAgIH0pLnRoZW4ocmVzdWx0ID0+IHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgICAgICAgICAgICAgICAgc2V0dGluZ1xuICAgICAgICAgICAgICAgICAgICAgICAgLnNldCgnbG9jYWxlJywgbG9jYWxlKVxuICAgICAgICAgICAgICAgICAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICB3aW5kb3cubG9jYXRpb24ucmVsb2FkKCk7XG4gICAgICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICAgICAgICAgLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IocmVhc29uKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIH0pO1xuXG4gICAgICAgICAgICAgIC8vIEFkZCB0aGUgbGFuZ3VhZ2UgY29tbWFuZCB0byB0aGUgbWVudVxuICAgICAgICAgICAgICBpZiAobGFuZ3VhZ2VzTWVudSkge1xuICAgICAgICAgICAgICAgIGxhbmd1YWdlc01lbnUuYWRkSXRlbSh7XG4gICAgICAgICAgICAgICAgICBjb21tYW5kLFxuICAgICAgICAgICAgICAgICAgYXJnczoge31cbiAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH0pXG4gICAgICAgICAgLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgICAgICBjb25zb2xlLmVycm9yKGBBdmFpbGFibGUgbG9jYWxlcyBlcnJvcmVkIVxcbiR7cmVhc29ufWApO1xuICAgICAgICAgIH0pO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICBjb25zb2xlLmVycm9yKFxuICAgICAgICAgIGBUaGUganVweXRlcmxhYiB0cmFuc2xhdGlvbiBleHRlbnNpb24gYXBwZWFycyB0byBiZSBtaXNzaW5nLlxcbiR7cmVhc29ufWBcbiAgICAgICAgKTtcbiAgICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2lucyBhcyBkZWZhdWx0LlxuICovXG5jb25zdCBwbHVnaW5zOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48YW55PltdID0gW3RyYW5zbGF0b3IsIGxhbmdNZW51XTtcbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG4iXSwic291cmNlUm9vdCI6IiJ9