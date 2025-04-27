(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_hub-extension_lib_index_js-_92650"],{

/***/ "../packages/hub-extension/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/hub-extension/lib/index.js ***!
  \**********************************************/
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
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module hub-extension
 */




/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.controlPanel = 'hub:control-panel';
    CommandIDs.logout = 'hub:logout';
    CommandIDs.restart = 'hub:restart';
})(CommandIDs || (CommandIDs = {}));
/**
 * Activate the jupyterhub extension.
 */
function activateHubExtension(app, paths, translator, palette) {
    const trans = translator.load('jupyterlab');
    const hubHost = paths.urls.hubHost || '';
    const hubPrefix = paths.urls.hubPrefix || '';
    const hubUser = paths.urls.hubUser || '';
    const hubServerName = paths.urls.hubServerName || '';
    const baseUrl = paths.urls.base;
    // Bail if not running on JupyterHub.
    if (!hubPrefix) {
        return;
    }
    console.debug('hub-extension: Found configuration ', {
        hubHost: hubHost,
        hubPrefix: hubPrefix
    });
    // If hubServerName is set, use JupyterHub 1.0 URL.
    const restartUrl = hubServerName
        ? hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(hubPrefix, 'spawn', hubUser, hubServerName)
        : hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(hubPrefix, 'spawn');
    const { commands } = app;
    commands.addCommand(CommandIDs.restart, {
        label: trans.__('Restart Server'),
        caption: trans.__('Request that the Hub restart this server'),
        execute: () => {
            window.open(restartUrl, '_blank');
        }
    });
    commands.addCommand(CommandIDs.controlPanel, {
        label: trans.__('Hub Control Panel'),
        caption: trans.__('Open the Hub control panel in a new browser tab'),
        execute: () => {
            window.open(hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(hubPrefix, 'home'), '_blank');
        }
    });
    commands.addCommand(CommandIDs.logout, {
        label: trans.__('Log Out'),
        caption: trans.__('Log out of the Hub'),
        execute: () => {
            window.location.href = hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(baseUrl, 'logout');
        }
    });
    // Add palette items.
    if (palette) {
        const category = trans.__('Hub');
        palette.addItem({ category, command: CommandIDs.controlPanel });
        palette.addItem({ category, command: CommandIDs.logout });
    }
}
/**
 * Initialization data for the hub-extension.
 */
const hubExtension = {
    activate: activateHubExtension,
    id: 'jupyter.extensions.hub-extension',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true
};
/**
 * Plugin to load menu description based on settings file
 */
const hubExtensionMenu = {
    activate: () => void 0,
    id: 'jupyter.extensions.hub-extension:plugin',
    autoStart: true
};
/**
 * The default JupyterLab connection lost provider. This may be overridden
 * to provide custom behavior when a connection to the server is lost.
 *
 * If the application is being deployed within a JupyterHub context,
 * this will provide a dialog that prompts the user to restart the server.
 * Otherwise, it shows an error dialog.
 */
const connectionlost = {
    id: '@jupyterlab/apputils-extension:connectionlost',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    activate: (app, paths, translator) => {
        const trans = translator.load('jupyterlab');
        const hubPrefix = paths.urls.hubPrefix || '';
        const baseUrl = paths.urls.base;
        // Return the default error message if not running on JupyterHub.
        if (!hubPrefix) {
            return _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ConnectionLost;
        }
        // If we are running on JupyterHub, return a dialog
        // that prompts the user to restart their server.
        let showingError = false;
        const onConnectionLost = async (manager, err) => {
            if (showingError) {
                return;
            }
            showingError = true;
            const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Server unavailable or unreachable'),
                body: trans.__('Your server at %1 is not running.\nWould you like to restart it?', baseUrl),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Restart') }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Dismiss') })
                ]
            });
            showingError = false;
            if (result.button.accept) {
                await app.commands.execute(CommandIDs.restart);
            }
        };
        return onConnectionLost;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IConnectionLost
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([
    hubExtension,
    hubExtensionMenu,
    connectionlost
]);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaHViLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBOzs7K0VBRytFO0FBQy9FOzs7R0FHRztBQU84QjtBQUMwQztBQUM1QjtBQUVPO0FBRXREOztHQUVHO0FBQ0ksSUFBVSxVQUFVLENBTTFCO0FBTkQsV0FBaUIsVUFBVTtJQUNaLHVCQUFZLEdBQVcsbUJBQW1CLENBQUM7SUFFM0MsaUJBQU0sR0FBVyxZQUFZLENBQUM7SUFFOUIsa0JBQU8sR0FBVyxhQUFhLENBQUM7QUFDL0MsQ0FBQyxFQU5nQixVQUFVLEtBQVYsVUFBVSxRQU0xQjtBQUVEOztHQUVHO0FBQ0gsU0FBUyxvQkFBb0IsQ0FDM0IsR0FBb0IsRUFDcEIsS0FBNkIsRUFDN0IsVUFBdUIsRUFDdkIsT0FBK0I7SUFFL0IsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUM1QyxNQUFNLE9BQU8sR0FBRyxLQUFLLENBQUMsSUFBSSxDQUFDLE9BQU8sSUFBSSxFQUFFLENBQUM7SUFDekMsTUFBTSxTQUFTLEdBQUcsS0FBSyxDQUFDLElBQUksQ0FBQyxTQUFTLElBQUksRUFBRSxDQUFDO0lBQzdDLE1BQU0sT0FBTyxHQUFHLEtBQUssQ0FBQyxJQUFJLENBQUMsT0FBTyxJQUFJLEVBQUUsQ0FBQztJQUN6QyxNQUFNLGFBQWEsR0FBRyxLQUFLLENBQUMsSUFBSSxDQUFDLGFBQWEsSUFBSSxFQUFFLENBQUM7SUFDckQsTUFBTSxPQUFPLEdBQUcsS0FBSyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUM7SUFFaEMscUNBQXFDO0lBQ3JDLElBQUksQ0FBQyxTQUFTLEVBQUU7UUFDZCxPQUFPO0tBQ1I7SUFFRCxPQUFPLENBQUMsS0FBSyxDQUFDLHFDQUFxQyxFQUFFO1FBQ25ELE9BQU8sRUFB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Q0FBQztRQUNGLE9BQU8sZ0JBQWdCLENBQUM7SUFDMUIsQ0FBQztJQUNELFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLG9FQUFlO0NBQzFCLENBQUM7QUFFRixpRUFBZTtJQUNiLFlBQVk7SUFDWixnQkFBZ0I7SUFDaEIsY0FBYztDQUNpQixFQUFDIiwiZmlsZSI6InBhY2thZ2VzX2h1Yi1leHRlbnNpb25fbGliX2luZGV4X2pzLV85MjY1MC4wZDJiZjBkMzkzNDc1ZDdlOTQ1Yy5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgaHViLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIENvbm5lY3Rpb25Mb3N0LFxuICBJQ29ubmVjdGlvbkxvc3QsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IERpYWxvZywgSUNvbW1hbmRQYWxldHRlLCBzaG93RGlhbG9nIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgVVJMRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7IFNlcnZlckNvbm5lY3Rpb24sIFNlcnZpY2VNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIHBsdWdpbi5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IGNvbnRyb2xQYW5lbDogc3RyaW5nID0gJ2h1Yjpjb250cm9sLXBhbmVsJztcblxuICBleHBvcnQgY29uc3QgbG9nb3V0OiBzdHJpbmcgPSAnaHViOmxvZ291dCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlc3RhcnQ6IHN0cmluZyA9ICdodWI6cmVzdGFydCc7XG59XG5cbi8qKlxuICogQWN0aXZhdGUgdGhlIGp1cHl0ZXJodWIgZXh0ZW5zaW9uLlxuICovXG5mdW5jdGlvbiBhY3RpdmF0ZUh1YkV4dGVuc2lvbihcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHBhdGhzOiBKdXB5dGVyRnJvbnRFbmQuSVBhdGhzLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuKTogdm9pZCB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IGh1Ykhvc3QgPSBwYXRocy51cmxzLmh1Ykhvc3QgfHwgJyc7XG4gIGNvbnN0IGh1YlByZWZpeCA9IHBhdGhzLnVybHMuaHViUHJlZml4IHx8ICcnO1xuICBjb25zdCBodWJVc2VyID0gcGF0aHMudXJscy5odWJVc2VyIHx8ICcnO1xuICBjb25zdCBodWJTZXJ2ZXJOYW1lID0gcGF0aHMudXJscy5odWJTZXJ2ZXJOYW1lIHx8ICcnO1xuICBjb25zdCBiYXNlVXJsID0gcGF0aHMudXJscy5iYXNlO1xuXG4gIC8vIEJhaWwgaWYgbm90IHJ1bm5pbmcgb24gSnVweXRlckh1Yi5cbiAgaWYgKCFodWJQcmVmaXgpIHtcbiAgICByZXR1cm47XG4gIH1cblxuICBjb25zb2xlLmRlYnVnKCdodWItZXh0ZW5zaW9uOiBGb3VuZCBjb25maWd1cmF0aW9uICcsIHtcbiAgICBodWJIb3N0OiBodWJIb3N0LFxuICAgIGh1YlByZWZpeDogaHViUHJlZml4XG4gIH0pO1xuXG4gIC8vIElmIGh1YlNlcnZlck5hbWUgaXMgc2V0LCB1c2UgSnVweXRlckh1YiAxLjAgVVJMLlxuICBjb25zdCByZXN0YXJ0VXJsID0gaHViU2VydmVyTmFtZVxuICAgID8gaHViSG9zdCArIFVSTEV4dC5qb2luKGh1YlByZWZpeCwgJ3NwYXduJywgaHViVXNlciwgaHViU2VydmVyTmFtZSlcbiAgICA6IGh1Ykhvc3QgKyBVUkxFeHQuam9pbihodWJQcmVmaXgsICdzcGF3bicpO1xuXG4gIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVzdGFydCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnUmVzdGFydCBTZXJ2ZXInKSxcbiAgICBjYXB0aW9uOiB0cmFucy5fXygnUmVxdWVzdCB0aGF0IHRoZSBIdWIgcmVzdGFydCB0aGlzIHNlcnZlcicpLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIHdpbmRvdy5vcGVuKHJlc3RhcnRVcmwsICdfYmxhbmsnKTtcbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb250cm9sUGFuZWwsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0h1YiBDb250cm9sIFBhbmVsJyksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ09wZW4gdGhlIEh1YiBjb250cm9sIHBhbmVsIGluIGEgbmV3IGJyb3dzZXIgdGFiJyksXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgd2luZG93Lm9wZW4oaHViSG9zdCArIFVSTEV4dC5qb2luKGh1YlByZWZpeCwgJ2hvbWUnKSwgJ19ibGFuaycpO1xuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmxvZ291dCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnTG9nIE91dCcpLFxuICAgIGNhcHRpb246IHRyYW5zLl9fKCdMb2cgb3V0IG9mIHRoZSBIdWInKSxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICB3aW5kb3cubG9jYXRpb24uaHJlZiA9IGh1Ykhvc3QgKyBVUkxFeHQuam9pbihiYXNlVXJsLCAnbG9nb3V0Jyk7XG4gICAgfVxuICB9KTtcblxuICAvLyBBZGQgcGFsZXR0ZSBpdGVtcy5cbiAgaWYgKHBhbGV0dGUpIHtcbiAgICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdIdWInKTtcbiAgICBwYWxldHRlLmFkZEl0ZW0oeyBjYXRlZ29yeSwgY29tbWFuZDogQ29tbWFuZElEcy5jb250cm9sUGFuZWwgfSk7XG4gICAgcGFsZXR0ZS5hZGRJdGVtKHsgY2F0ZWdvcnksIGNvbW1hbmQ6IENvbW1hbmRJRHMubG9nb3V0IH0pO1xuICB9XG59XG5cbi8qKlxuICogSW5pdGlhbGl6YXRpb24gZGF0YSBmb3IgdGhlIGh1Yi1leHRlbnNpb24uXG4gKi9cbmNvbnN0IGh1YkV4dGVuc2lvbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBhY3RpdmF0ZTogYWN0aXZhdGVIdWJFeHRlbnNpb24sXG4gIGlkOiAnanVweXRlci5leHRlbnNpb25zLmh1Yi1leHRlbnNpb24nLFxuICByZXF1aXJlczogW0p1cHl0ZXJGcm9udEVuZC5JUGF0aHMsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJQ29tbWFuZFBhbGV0dGVdLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogUGx1Z2luIHRvIGxvYWQgbWVudSBkZXNjcmlwdGlvbiBiYXNlZCBvbiBzZXR0aW5ncyBmaWxlXG4gKi9cbmNvbnN0IGh1YkV4dGVuc2lvbk1lbnU6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgYWN0aXZhdGU6ICgpID0+IHZvaWQgMCxcbiAgaWQ6ICdqdXB5dGVyLmV4dGVuc2lvbnMuaHViLWV4dGVuc2lvbjpwbHVnaW4nLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgSnVweXRlckxhYiBjb25uZWN0aW9uIGxvc3QgcHJvdmlkZXIuIFRoaXMgbWF5IGJlIG92ZXJyaWRkZW5cbiAqIHRvIHByb3ZpZGUgY3VzdG9tIGJlaGF2aW9yIHdoZW4gYSBjb25uZWN0aW9uIHRvIHRoZSBzZXJ2ZXIgaXMgbG9zdC5cbiAqXG4gKiBJZiB0aGUgYXBwbGljYXRpb24gaXMgYmVpbmcgZGVwbG95ZWQgd2l0aGluIGEgSnVweXRlckh1YiBjb250ZXh0LFxuICogdGhpcyB3aWxsIHByb3ZpZGUgYSBkaWFsb2cgdGhhdCBwcm9tcHRzIHRoZSB1c2VyIHRvIHJlc3RhcnQgdGhlIHNlcnZlci5cbiAqIE90aGVyd2lzZSwgaXQgc2hvd3MgYW4gZXJyb3IgZGlhbG9nLlxuICovXG5jb25zdCBjb25uZWN0aW9ubG9zdDogSnVweXRlckZyb250RW5kUGx1Z2luPElDb25uZWN0aW9uTG9zdD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMtZXh0ZW5zaW9uOmNvbm5lY3Rpb25sb3N0JyxcbiAgcmVxdWlyZXM6IFtKdXB5dGVyRnJvbnRFbmQuSVBhdGhzLCBJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgcGF0aHM6IEp1cHl0ZXJGcm9udEVuZC5JUGF0aHMsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKTogSUNvbm5lY3Rpb25Mb3N0ID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IGh1YlByZWZpeCA9IHBhdGhzLnVybHMuaHViUHJlZml4IHx8ICcnO1xuICAgIGNvbnN0IGJhc2VVcmwgPSBwYXRocy51cmxzLmJhc2U7XG5cbiAgICAvLyBSZXR1cm4gdGhlIGRlZmF1bHQgZXJyb3IgbWVzc2FnZSBpZiBub3QgcnVubmluZyBvbiBKdXB5dGVySHViLlxuICAgIGlmICghaHViUHJlZml4KSB7XG4gICAgICByZXR1cm4gQ29ubmVjdGlvbkxvc3Q7XG4gICAgfVxuXG4gICAgLy8gSWYgd2UgYXJlIHJ1bm5pbmcgb24gSnVweXRlckh1YiwgcmV0dXJuIGEgZGlhbG9nXG4gICAgLy8gdGhhdCBwcm9tcHRzIHRoZSB1c2VyIHRvIHJlc3RhcnQgdGhlaXIgc2VydmVyLlxuICAgIGxldCBzaG93aW5nRXJyb3IgPSBmYWxzZTtcbiAgICBjb25zdCBvbkNvbm5lY3Rpb25Mb3N0OiBJQ29ubmVjdGlvbkxvc3QgPSBhc3luYyAoXG4gICAgICBtYW5hZ2VyOiBTZXJ2aWNlTWFuYWdlci5JTWFuYWdlcixcbiAgICAgIGVycjogU2VydmVyQ29ubmVjdGlvbi5OZXR3b3JrRXJyb3JcbiAgICApOiBQcm9taXNlPHZvaWQ+ID0+IHtcbiAgICAgIGlmIChzaG93aW5nRXJyb3IpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgc2hvd2luZ0Vycm9yID0gdHJ1ZTtcbiAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IHNob3dEaWFsb2coe1xuICAgICAgICB0aXRsZTogdHJhbnMuX18oJ1NlcnZlciB1bmF2YWlsYWJsZSBvciB1bnJlYWNoYWJsZScpLFxuICAgICAgICBib2R5OiB0cmFucy5fXyhcbiAgICAgICAgICAnWW91ciBzZXJ2ZXIgYXQgJTEgaXMgbm90IHJ1bm5pbmcuXFxuV291bGQgeW91IGxpa2UgdG8gcmVzdGFydCBpdD8nLFxuICAgICAgICAgIGJhc2VVcmxcbiAgICAgICAgKSxcbiAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgIERpYWxvZy5va0J1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnUmVzdGFydCcpIH0pLFxuICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0Rpc21pc3MnKSB9KVxuICAgICAgICBdXG4gICAgICB9KTtcbiAgICAgIHNob3dpbmdFcnJvciA9IGZhbHNlO1xuICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgIGF3YWl0IGFwcC5jb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMucmVzdGFydCk7XG4gICAgICB9XG4gICAgfTtcbiAgICByZXR1cm4gb25Db25uZWN0aW9uTG9zdDtcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSUNvbm5lY3Rpb25Mb3N0XG59O1xuXG5leHBvcnQgZGVmYXVsdCBbXG4gIGh1YkV4dGVuc2lvbixcbiAgaHViRXh0ZW5zaW9uTWVudSxcbiAgY29ubmVjdGlvbmxvc3Rcbl0gYXMgSnVweXRlckZyb250RW5kUGx1Z2luPGFueT5bXTtcbiJdLCJzb3VyY2VSb290IjoiIn0=